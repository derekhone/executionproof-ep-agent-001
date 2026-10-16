"""
EP-AGENT-001 Normalizer: Microsoft Agent Framework (agent-framework 1.22.0)
STATUS: STUB — DESIGN ONLY — NOT AUTHORIZED FOR STUDY EXECUTION
SCOPE: Benign, well-formed inputs only. One agent, one function tool, one FunctionMiddleware.
       Multi-agent orchestration is UW P2 reserved and is not implemented.
       Malformed/adversarial input handling is UD / UW P1 reserved and is not implemented.

Native argument source: the function-invocation context arguments seen by FunctionMiddleware.
"""
import hashlib
import json
import secrets
from datetime import datetime, timezone
from typing import Any, Optional

FRAMEWORK_ID = "maf"
DEFAULT_TENANT_ID = "ep-agent-001-test"
CANONICAL_HASH_FIELDS = ("actor_id", "agent_id", "tenant_id", "action_type", "target", "parameters")


def compute_action_hash(contract: dict) -> str:
    """SHA-256 over the deterministic canonical action fields (REQUEST_CONTRACT.md §2)."""
    canonical = json.dumps(
        {k: contract[k] for k in CANONICAL_HASH_FIELDS},
        sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def normalize_to_request_contract(
    actor_id: str,
    action_type: str,
    target: str,
    parameters: dict,
    authority_reference: str,
    policy_reference: str,
    evidence_references: Optional[list] = None,
    current_state_reference: Optional[str] = None,
    tenant_id: str = DEFAULT_TENANT_ID,
) -> dict:
    """
    Normalize framework-native fields into the frozen EP-AGENT-001 Request Contract.
    STUB — normalization logic to be validated before execution.
    """
    requested_at = datetime.now(timezone.utc).isoformat()
    nonce = hashlib.sha256(
        f"{actor_id}:{action_type}:{requested_at}:{secrets.token_hex(16)}".encode()
    ).hexdigest()[:32]
    contract: dict[str, Any] = {
        "request_id": f"ep-{nonce[:8]}",
        "actor_id": actor_id,
        "agent_id": actor_id,  # single-agent: agent_id == actor_id
        "framework_id": FRAMEWORK_ID,
        "tenant_id": tenant_id,
        "action_type": action_type,
        "target": target,
        "parameters": parameters,
        "authority_reference": authority_reference,
        "evidence_references": list(evidence_references) if evidence_references else [],
        "policy_reference": policy_reference,
        "current_state_reference": current_state_reference,
        "requested_at": requested_at,
        "nonce": nonce,
    }
    contract["action_hash"] = compute_action_hash(contract)
    return contract


def extract_native_arguments(invocation_arguments: Any) -> dict:
    """
    MAF: middleware context exposes the function arguments either as a mapping or as a pydantic-style
    model. Convert to a plain dict without altering values. (Exact attribute validated at freeze.)
    """
    if hasattr(invocation_arguments, "model_dump"):
        return dict(invocation_arguments.model_dump())
    return dict(invocation_arguments)
