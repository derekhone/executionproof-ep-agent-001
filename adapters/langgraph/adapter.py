"""
EP-AGENT-001 Adapter: LangGraph (langgraph 1.2.15)
STATUS: IMPLEMENTED (v0.3) — NOT AUTHORIZED FOR STUDY EXECUTION (no default endpoint; gated runner only)
SCOPE: Single-agent graph, single ToolNode path only. Multi-agent subgraphs / fan-out to other agents
       excluded (UW P2 reserved).

Integration point: the verified tool is executed by a LangGraph `ToolNode`. The tool function normalizes
tool_call["args"] into the frozen Request Contract, calls ExecutionProof /verify, invokes the mock action
ONLY on ALLOW, and writes {verdict, proof_record_id} unchanged into the ToolMessage / graph state.
The framework package is NOT imported by this stub.
"""
from typing import Any, Optional

from .. import ep_client
from .normalizer import extract_native_arguments as _extract_native
from .normalizer import (
    DEFAULT_TENANT_ID,
    FRAMEWORK_ID,
    extract_native_arguments,
    normalize_to_request_contract as _normalize,
)

FRAMEWORK_PACKAGE = "langgraph"
FRAMEWORK_VERSION = "1.2.15"
NOT_AUTHORIZED_MESSAGE = (
    "EP-AGENT-001 has not been authorized for execution. "
    "Do not run until Derek Hone grants execution authorization and "
    "the preregistration SHA is locked."
)

# No default network target: the endpoint is supplied explicitly (argument or EP_BASE_URL) — see adapters/ep_client.py


class EPVerifiedToolNode:
    """
    Provides the ExecutionProof-verified tool executed by a LangGraph ToolNode in a single-agent graph.
    """

    def __init__(self, framework_id: str = FRAMEWORK_ID, tenant_id: str = DEFAULT_TENANT_ID):
        if framework_id != FRAMEWORK_ID:
            raise ValueError(f"framework_id must be {FRAMEWORK_ID!r}")
        self.framework_id = framework_id
        self.tenant_id = tenant_id

    def normalize_to_request_contract(
        self,
        actor_id: str,
        action_type: str,
        target: str,
        parameters: dict,
        authority_reference: str,
        policy_reference: str,
        evidence_references: Optional[list] = None,
        current_state_reference: Optional[str] = None,
    ) -> dict:
        """
        Normalize framework-native fields into the frozen EP-AGENT-001 Request Contract.
        Normalization is frozen (REQUEST_CONTRACT.md); adapters translate syntax only.
        """
        return _normalize(
            actor_id=actor_id,
            action_type=action_type,
            target=target,
            parameters=parameters,
            authority_reference=authority_reference,
            policy_reference=policy_reference,
            evidence_references=evidence_references,
            current_state_reference=current_state_reference,
            tenant_id=self.tenant_id,
        )

    def normalize_tool_call(self, tool_call: Any) -> dict:
        """Normalize a LangGraph tool call ({"name", "args", "id"}) into the Request Contract."""
        return self.normalize_to_request_contract(**extract_native_arguments(tool_call))

    def verify(self, contract: dict, base_url: str = None, verify_path: str = None) -> dict:
        """POST the frozen Request Contract to ExecutionProof; returns {verdict, proof_record_id, raw} unchanged.
        Refuses (ExecutionNotConfigured, a NotImplementedError) when no endpoint is supplied."""
        return ep_client.post_verify(contract, base_url=base_url, verify_path=verify_path)

    def handle_native(self, native_call, base_url: str = None, verify_path: str = None) -> dict:
        """Framework-native tool call -> Request Contract -> /verify -> verdict + proof reference
        (+ simulated downstream on ALLOW only). Translation of syntax only; no local verdict logic."""
        contract = self.normalize_to_request_contract(**_extract_native(native_call))
        return ep_client.finalize(contract, self.verify(contract, base_url=base_url, verify_path=verify_path))
