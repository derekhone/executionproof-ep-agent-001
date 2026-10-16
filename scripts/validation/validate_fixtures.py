#!/usr/bin/env python3
"""
EP-AGENT-001 — load and validate the benign fixture files B1–B5.

Checks: JSON loads; required top-level keys present; fixture_id matches filename; expected_verdict present, valid,
and consistent with EXPECTED_RESULTS.json; benign marker present; contract has the required input fields.
Does NOT call any ExecutionProof endpoint. Produces no experimental data.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "fixtures" / "benign"
EXPECTED_FILES = {
    "B1": "B1_allow_complete.json",
    "B2": "B2_hold_incomplete_contract.json",
    "B3": "B3_deny_no_authority.json",
    "B4": "B4_hold_evidence_absent.json",
    "B5": "B5_hold_constraint_exceeded.json",
}
TOP_LEVEL_KEYS = {"fixture_id", "name", "description", "note", "expected_verdict", "contract", "fixture_policy_context"}
CONTRACT_REQUIRED = {"actor_id", "action_type", "target", "parameters", "authority_reference", "policy_reference"}
VERDICTS = {"ALLOW", "HOLD", "DENY"}
# Scope guard (v0.2): each fixture may differ from the B1 baseline only in these contract paths (one condition).
# B3's actor-keyed reference strings follow the actor id; the condition is still "actor identity".
ALLOWED_CONTRACT_DIFFS = {
    "B1": set(),
    "B2": {"current_state_reference"},
    "B3": {"actor_id", "authority_reference", "evidence_references"},
    "B4": {"evidence_references"},
    "B5": {"parameters.amount"},
}
# Terms that would indicate multi-step / multi-agent / adversarial drift inside a fixture.
FORBIDDEN_TERMS = ("delegat", "handoff", "hand-off", "sub_agent", "sub-agent", "parallel", "revoked_at", "replay",
                   "forged", "stale", "recovery", "orchestrat", "inherit", "a2a")


def _flat(d, prefix=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(_flat(v, prefix + k + "."))
        else:
            out[prefix + k] = v
    return out


def scope_checks(fixtures):
    """Return errors if fixtures drift from the approved one-condition, single-action benign scope."""
    errs = []
    b1 = fixtures.get("B1")
    if b1 is None:
        return ["B1 baseline missing"]
    base_c = _flat(b1["contract"])
    base_p = {k: v for k, v in b1["fixture_policy_context"].items() if k != "evidence_records"}
    for cid, fx in fixtures.items():
        c = _flat(fx["contract"])
        diffs = {k for k in set(base_c) | set(c) if base_c.get(k, "<absent>") != c.get(k, "<absent>")}
        if diffs != ALLOWED_CONTRACT_DIFFS[cid]:
            errs.append(f"{cid}: contract differs from B1 in {sorted(diffs)}; allowed {sorted(ALLOWED_CONTRACT_DIFFS[cid])}")
        pol = {k: v for k, v in fx["fixture_policy_context"].items() if k != "evidence_records"}
        if pol != base_p:
            errs.append(f"{cid}: fixture_policy_context (excluding evidence_records) differs from B1")
        if fx["contract"].get("action_type") != "SUBMIT_EXTERNAL_ACTION":
            errs.append(f"{cid}: action_type is not the single approved action")
        if "single_condition_vs_B1" not in fx:
            errs.append(f"{cid}: single_condition_vs_B1 missing")
        # Scan contract + policy only (the note/description may contain exclusion language such as 'not delegated').
        text = json.dumps({"contract": fx["contract"], "policy": fx["fixture_policy_context"]}).lower()
        hits = [t for t in FORBIDDEN_TERMS if t in text]
        if hits:
            errs.append(f"{cid}: out-of-scope terms in contract/policy {hits}")
    return errs


def main() -> int:
    expected = {c["case_id"]: c for c in json.loads((ROOT / "EXPECTED_RESULTS.json").read_text())["cases"]}
    errors = []
    loaded = {}
    for case_id, filename in EXPECTED_FILES.items():
        path = FIXTURE_DIR / filename
        case_errors = []
        try:
            fx = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{filename}: cannot load ({exc})")
            print(f"FAIL  {filename}: cannot load ({exc})")
            continue
        loaded[case_id] = fx
        missing = TOP_LEVEL_KEYS - set(fx)
        if missing:
            case_errors.append(f"missing keys {sorted(missing)}")
        if fx.get("fixture_id") != case_id:
            case_errors.append(f"fixture_id {fx.get('fixture_id')!r} != {case_id!r}")
        if fx.get("expected_verdict") not in VERDICTS:
            case_errors.append(f"invalid expected_verdict {fx.get('expected_verdict')!r}")
        exp = expected.get(case_id)
        if exp is None:
            case_errors.append("case absent from EXPECTED_RESULTS.json")
        else:
            if exp["expected_verdict"] != fx.get("expected_verdict"):
                case_errors.append("expected_verdict disagrees with EXPECTED_RESULTS.json")
            if exp["name"] != fx.get("name"):
                case_errors.append("name disagrees with EXPECTED_RESULTS.json")
        if "BENIGN FIXTURE" not in fx.get("note", ""):
            case_errors.append("benign marker missing from note")
        c_missing = CONTRACT_REQUIRED - set(fx.get("contract", {}))
        if c_missing:
            case_errors.append(f"contract missing {sorted(c_missing)}")
        print(f"{'PASS' if not case_errors else 'FAIL'}  {case_id} {filename:36s} expected_verdict={fx.get('expected_verdict')}"
              + ("" if not case_errors else f"  {case_errors}"))
        errors.extend(f"{filename}: {e}" for e in case_errors)
    for e in scope_checks(loaded) if len(loaded) == len(EXPECTED_FILES) else ["not all fixtures loaded; scope checks skipped"]:
        print(f"FAIL  scope: {e}")
        errors.append(f"scope: {e}")
    if not any(e.startswith("scope:") for e in errors):
        print("PASS  scope: one condition vs B1 per fixture; identical policy context; single action; no out-of-scope terms")
    extra = {p.name for p in FIXTURE_DIR.glob("*.json")} - set(EXPECTED_FILES.values())
    if extra:
        errors.append(f"unexpected fixture files: {sorted(extra)}")
        print(f"FAIL  unexpected fixture files: {sorted(extra)}")
    print(f"\nFixture validation: {'PASS' if not errors else 'FAIL'} ({len(EXPECTED_FILES)} fixtures). "
          "(Harness check — not an experimental result.)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
