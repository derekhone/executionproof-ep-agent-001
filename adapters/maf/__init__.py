"""
EP-AGENT-001 adapter package: Microsoft Agent Framework (agent-framework 1.22.0)
STATUS: IMPLEMENTED (v0.3) — NOT AUTHORIZED FOR STUDY EXECUTION
"""
from .adapter import EPVerificationMiddleware, FRAMEWORK_PACKAGE, FRAMEWORK_VERSION, NOT_AUTHORIZED_MESSAGE
from .normalizer import FRAMEWORK_ID, normalize_to_request_contract, compute_action_hash

__all__ = [
    "EPVerificationMiddleware", "FRAMEWORK_PACKAGE", "FRAMEWORK_VERSION", "NOT_AUTHORIZED_MESSAGE",
    "FRAMEWORK_ID", "normalize_to_request_contract", "compute_action_hash",
]
