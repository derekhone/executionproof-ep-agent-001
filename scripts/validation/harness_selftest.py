#!/usr/bin/env python3
"""
EP-AGENT-001 — HARNESS SELF-TEST ONLY.

*** THIS IS NOT EXPERIMENTAL EVIDENCE. ***
It does NOT call any ExecutionProof endpoint, does NOT produce verdicts, does NOT write files, and does NOT reveal
or simulate experimental results. It only checks that the harness plumbing is sound:

  T1  all fixture JSON files load
  T2  every normalizer output validates against the frozen Request Contract schema
  T3  normalization produces all 15 Request Contract fields, for every fixture x framework
  T4  nonce (and request_id) uniqueness across all normalized contracts
  T5  canonical fields and action_hash are identical across the four frameworks for each fixture
      (structural property of the normalizers, not an ExecutionProof decision)
  T6  adapter classes instantiate, and adapter-method normalization equals normalizer output on canonical fields
  T7  every adapter's verify() refuses without an explicit endpoint (ExecutionNotConfigured, a NotImplementedError) — no default network target
  T8  run_study.py refuses to run (NotImplementedError) — execution not authorized
  T9  results/ and proofrecords/ contain only their placeholder files
"""
import importlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
FRAMEWORKS = ("openai_agents", "langgraph", "crewai", "maf")
ADAPTER_CLASSES = {
    "openai_agents": "EPVerificationTool",
    "langgraph": "EPVerifiedToolNode",
    "crewai": "EPVerifiedCrewTool",
    "maf": "EPVerificationMiddleware",
}
ALL_FIELDS = (
    "request_id", "actor_id", "agent_id", "framework_id", "tenant_id", "action_type", "target", "parameters",
    "authority_reference", "evidence_references", "policy_reference", "current_state_reference",
    "requested_at", "nonce", "action_hash",
)
NON_CANONICAL = {"request_id", "framework_id", "nonce", "requested_at"}


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    print("EP-AGENT-001 HARNESS SELF-TEST ONLY — NOT EXPERIMENTAL EVIDENCE — NO ENDPOINT CALLED\n")
    results = []

    def record(test_id: str, ok: bool, detail: str):
        results.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {test_id}  {detail}")

    schema_mod = _load_module(ROOT / "scripts" / "validation" / "validate_schemas.py", "validate_schemas")

    # T1
    fixtures = {}
    for path in sorted((ROOT / "fixtures" / "benign").glob("B*.json")):
        try:
            fixtures[path.stem.split("_")[0]] = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            record("T1", False, f"{path.name} failed to load: {exc}")
    record("T1", len(fixtures) == 5, f"fixtures loaded: {sorted(fixtures)}")

    normalizers = {fw: importlib.import_module(f"adapters.{fw}.normalizer") for fw in FRAMEWORKS}
    contracts = {(fw, cid): normalizers[fw].normalize_to_request_contract(**fx["contract"])
                 for cid, fx in fixtures.items() for fw in FRAMEWORKS}

    # T2
    schema_errors = {k: schema_mod.validate_contract(c) for k, c in contracts.items()}
    bad = {k: v for k, v in schema_errors.items() if v}
    record("T2", not bad, f"schema-valid contracts: {len(contracts) - len(bad)}/{len(contracts)}" + (f" {bad}" if bad else ""))

    # T3
    missing = {k: [f for f in ALL_FIELDS if f not in c] for k, c in contracts.items()}
    missing = {k: v for k, v in missing.items() if v}
    record("T3", not missing and all(len(c) == 15 for c in contracts.values()),
           f"all 15 fields present in {len(contracts) - len(missing)}/{len(contracts)} contracts")

    # T4
    nonces = [c["nonce"] for c in contracts.values()]
    request_ids = [c["request_id"] for c in contracts.values()]
    record("T4", len(set(nonces)) == len(nonces) and len(set(request_ids)) == len(request_ids),
           f"unique nonces {len(set(nonces))}/{len(nonces)}; unique request_ids {len(set(request_ids))}/{len(request_ids)}")

    # T5
    divergent = []
    for cid in fixtures:
        canon = [{k: v for k, v in contracts[(fw, cid)].items() if k not in NON_CANONICAL} for fw in FRAMEWORKS]
        if any(c != canon[0] for c in canon[1:]):
            divergent.append(cid)
    record("T5", not divergent, "canonical fields + action_hash identical across 4 frameworks for each fixture"
           + (f"; divergent: {divergent}" if divergent else ""))

    # T6
    t6_ok, t6_detail = True, []
    for fw in FRAMEWORKS:
        cls = getattr(importlib.import_module(f"adapters.{fw}.adapter"), ADAPTER_CLASSES[fw])
        inst = cls()
        c = inst.normalize_to_request_contract(**fixtures["B1"]["contract"])
        same = {k: v for k, v in c.items() if k not in NON_CANONICAL} == \
               {k: v for k, v in contracts[(fw, "B1")].items() if k not in NON_CANONICAL}
        t6_ok &= same and c["framework_id"] == fw
        t6_detail.append(f"{ADAPTER_CLASSES[fw]}={'ok' if same else 'MISMATCH'}")
    record("T6", t6_ok, ", ".join(t6_detail))

    # T7 — no default network target: verify() must refuse when no endpoint is supplied
    import os
    os.environ.pop("EP_BASE_URL", None)
    refused = []
    for fw in FRAMEWORKS:
        inst = getattr(importlib.import_module(f"adapters.{fw}.adapter"), ADAPTER_CLASSES[fw])()
        try:
            inst.verify(contracts[(fw, "B1")])
            refused.append(False)
        except NotImplementedError:
            refused.append(True)
    record("T7", all(refused), f"verify() refused without endpoint (ExecutionNotConfigured) in {sum(refused)}/4 adapters")

    # T8
    run_study = _load_module(ROOT / "scripts" / "execute" / "run_study.py", "run_study")
    try:
        run_study.main(["--framework", "all"])  # no filing record / gate record / auth token
        record("T8", False, "run_study.main() did not refuse")
    except NotImplementedError:
        record("T8", True, "run_study.main() refused (NotImplementedError)")

    # T9
    res_files = sorted(p.name for p in (ROOT / "results").iterdir())
    pr_files = sorted(p.name for p in (ROOT / "proofrecords").iterdir())
    clean = all(n.startswith("README_PLACEHOLDER") for n in res_files + pr_files)
    record("T9", clean, f"results/={res_files} proofrecords/={pr_files}")

    print(f"\nHarness self-test: {sum(results)}/{len(results)} checks passed. "
          "HARNESS SELF-TEST ONLY — NOT EXPERIMENTAL EVIDENCE — NO VERDICTS PRODUCED.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
