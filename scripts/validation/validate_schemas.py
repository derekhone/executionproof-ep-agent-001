#!/usr/bin/env python3
"""
EP-AGENT-001 — validate the frozen Request Contract schema against every fixture.

For each fixture B1–B5 and each of the four adapter normalizers, normalize the fixture contract and validate the
output against REQUEST_CONTRACT_SCHEMA (mirrors REQUEST_CONTRACT.md §5). Dependency-free validator.
Does NOT call any ExecutionProof endpoint. Produces no experimental data.
"""
import importlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "fixtures" / "benign"
FRAMEWORKS = ("openai_agents", "langgraph", "crewai", "maf")

REQUEST_CONTRACT_SCHEMA = {
    "title": "EP-AGENT-001 Request Contract v1.0",
    "required": [
        "request_id", "actor_id", "agent_id", "framework_id", "tenant_id", "action_type", "target",
        "parameters", "authority_reference", "policy_reference", "requested_at", "nonce", "action_hash",
    ],
    "properties": {
        "request_id": "nonempty_str",
        "actor_id": "nonempty_str",
        "agent_id": "nonempty_str",
        "framework_id": ("enum", FRAMEWORKS),
        "tenant_id": "nonempty_str",
        "action_type": "nonempty_str",
        "target": "nonempty_str",
        "parameters": "object",
        "authority_reference": "nonempty_str",
        "evidence_references": "str_array",
        "policy_reference": "nonempty_str",
        "current_state_reference": "str_or_null",
        "requested_at": "datetime",
        "nonce": ("pattern", r"^[0-9a-f]{32}$"),
        "action_hash": ("pattern", r"^[0-9a-f]{64}$"),
    },
    "additionalProperties": False,
}

FIXTURE_CONTRACT_FIELDS = {
    "actor_id", "action_type", "target", "parameters", "authority_reference",
    "evidence_references", "policy_reference", "current_state_reference",
}


def _check(value, rule) -> bool:
    if rule == "nonempty_str":
        return isinstance(value, str) and len(value) > 0
    if rule == "object":
        return isinstance(value, dict)
    if rule == "str_array":
        return isinstance(value, list) and all(isinstance(v, str) for v in value)
    if rule == "str_or_null":
        return value is None or isinstance(value, str)
    if rule == "datetime":
        try:
            datetime.fromisoformat(value)
            return True
        except (TypeError, ValueError):
            return False
    kind, arg = rule
    if kind == "enum":
        return value in arg
    if kind == "pattern":
        return isinstance(value, str) and re.match(arg, value) is not None
    raise ValueError(f"unknown rule {rule!r}")


def validate_contract(contract: dict) -> list:
    """Return a list of error strings (empty list = valid)."""
    errors = []
    for field in REQUEST_CONTRACT_SCHEMA["required"]:
        if field not in contract:
            errors.append(f"missing required field: {field}")
    for field, value in contract.items():
        rule = REQUEST_CONTRACT_SCHEMA["properties"].get(field)
        if rule is None:
            errors.append(f"additional property not allowed: {field}")
        elif not _check(value, rule):
            errors.append(f"invalid value for {field}: {value!r}")
    return errors


def load_normalizer(framework: str):
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    return importlib.import_module(f"adapters.{framework}.normalizer")


def main() -> int:
    fixtures = sorted(FIXTURE_DIR.glob("B*.json"))
    failures = 0
    for path in fixtures:
        fixture = json.loads(path.read_text())
        extra = set(fixture["contract"]) - FIXTURE_CONTRACT_FIELDS
        if extra:
            print(f"FAIL  {path.name}: unexpected fixture contract fields {sorted(extra)}")
            failures += 1
            continue
        for fw in FRAMEWORKS:
            contract = load_normalizer(fw).normalize_to_request_contract(**fixture["contract"])
            errs = validate_contract(contract)
            print(f"{'PASS' if not errs else 'FAIL'}  {path.name:36s} {fw:14s}" + ("" if not errs else f" {errs}"))
            failures += bool(errs)
    print(f"\nSchema validation: {len(fixtures) * len(FRAMEWORKS) - failures}/{len(fixtures) * len(FRAMEWORKS)} "
          f"normalized contracts valid. (Harness check — not an experimental result.)")
    return 0 if failures == 0 and fixtures else 1


if __name__ == "__main__":
    sys.exit(main())
