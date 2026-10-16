"""
EP-AGENT-001 shared ExecutionProof client (transport only).

Adapters translate framework-native syntax into the frozen Request Contract; this module only POSTs the
contract to an explicitly supplied ExecutionProof base URL and returns the response verdict and proof
reference UNCHANGED. It never decides a verdict locally, never alters the contract, and has NO default
network target: if no base URL is supplied (argument or EP_BASE_URL), it refuses.

Endpoint path: defaults to the packet's "/verify" (PREREGISTRATION / REQUEST_CONTRACT). The public
ExecutionProof OpenAPI 2.0.0 documents "/v2/boundaries/{boundaryId}/verify"; the exact path for the frozen
run is BLOCKED — DEREK CONFIRMATION REQUIRED (see EXECUTIONPROOF_PIN.md). Override with EP_VERIFY_PATH.
Downstream action is SIMULATED ONLY and runs only on an ALLOW verdict returned by the endpoint.
"""
import json
import os
import urllib.request

DEFAULT_VERIFY_PATH = "/verify"
NOT_CONFIGURED_MESSAGE = (
    "EP-AGENT-001: no ExecutionProof base URL supplied (argument or EP_BASE_URL). Adapters have no default "
    "network target. Study execution is NOT AUTHORIZED; only the gated runner may supply a study endpoint."
)


class ExecutionNotConfigured(NotImplementedError):
    """Raised when verify() is called without an explicit endpoint (no default network target)."""


def post_verify(contract: dict, base_url: str = None, verify_path: str = None, timeout: float = 10.0) -> dict:
    base_url = base_url or os.environ.get("EP_BASE_URL")
    if not base_url:
        raise ExecutionNotConfigured(NOT_CONFIGURED_MESSAGE)
    path = verify_path or os.environ.get("EP_VERIFY_PATH") or DEFAULT_VERIFY_PATH
    req = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=json.dumps(contract, sort_keys=True).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return {
        "verdict": body.get("verdict"),
        "proof_record_id": body.get("proof_record_id", body.get("proofId")),
        "raw": body,
    }


def simulated_downstream(contract: dict) -> dict:
    """SIMULATED downstream action. Performs no real side effect."""
    return {"simulated": True, "action_type": contract["action_type"], "target": contract["target"],
            "effect": "NONE — SIMULATED ONLY"}


def finalize(contract: dict, ep_response: dict) -> dict:
    """Return verdict + proof reference unchanged; run the simulated downstream only on ALLOW."""
    return {
        "verdict": ep_response["verdict"],
        "proof_record_id": ep_response["proof_record_id"],
        "request_id": contract["request_id"],
        "action_hash": contract["action_hash"],
        "simulated_downstream": simulated_downstream(contract) if ep_response["verdict"] == "ALLOW" else None,
    }
