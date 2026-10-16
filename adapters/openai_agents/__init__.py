"""
EP-AGENT-001 adapter package: OpenAI Agents SDK (openai-agents 0.24.0)
STATUS: IMPLEMENTED (v0.3) — NOT AUTHORIZED FOR STUDY EXECUTION
"""
from .adapter import EPVerificationTool, FRAMEWORK_PACKAGE, FRAMEWORK_VERSION, NOT_AUTHORIZED_MESSAGE
from .normalizer import FRAMEWORK_ID, normalize_to_request_contract, compute_action_hash

__all__ = [
    "EPVerificationTool", "FRAMEWORK_PACKAGE", "FRAMEWORK_VERSION", "NOT_AUTHORIZED_MESSAGE",
    "FRAMEWORK_ID", "normalize_to_request_contract", "compute_action_hash",
]
