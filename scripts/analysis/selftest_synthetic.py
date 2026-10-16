#!/usr/bin/env python3
"""SYNTHETIC ANALYSIS SELF-TEST / NOT EXPERIMENTAL EVIDENCE. Dummy data only; writes nothing to results/."""
import copy, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze import CASES, FRAMEWORKS, SEED, analyze, classify, latency, p95_nearest_rank, raw_export_csv

BANNER = "SYNTHETIC ANALYSIS SELF-TEST / NOT EXPERIMENTAL EVIDENCE"
EXP = {"B1": "ALLOW", "B2": "HOLD", "B3": "DENY", "B4": "HOLD", "B5": "HOLD"}  # dummy labels for code paths only


def base():
    return [dict(framework=f, case=k, integration_complete=True, observed_verdict=EXP[k], expected_verdict=EXP[k],
                 proof_ref_returned=True, proof_ref_resolves=True, proof_ref_unchanged=True, material_workaround=False,
                 canonical_hash=f"h-{k}", invalidation=None, defect=False) for f in FRAMEWORKS for k in CASES]


def mod(cells, fw, case, **kw):
    c = copy.deepcopy(cells); [x.update(kw) for x in c if x["framework"] == fw and x["case"] == case]; return c


tests = []
def check(name, got, want): tests.append((name, got == want, got, want))

check("all cells ok -> PASS", classify(base(), False)[0], "PASS")
check("one failed cell, three fully successful -> PARTIAL", classify(mod(base(), "crewai", "B3", observed_verdict="ALLOW", defect=True), False)[0], "PARTIAL")
c = base()
for fw in FRAMEWORKS: c = mod(c, fw, "B2", integration_complete=False)
check("every framework genuine shortfall -> FAIL", classify(c, False)[0], "FAIL")
check("P5 true -> FAIL", classify(base(), True)[0], "FAIL")
check("core divergence -> FAIL", classify(base(), False, core_divergence=True)[0], "FAIL")
check("infra-only shortfall -> INCONCLUSIVE", classify(mod(base(), "maf", "B1", integration_complete=False, invalidation=3), False)[0], "INCONCLUSIVE")
check("infra + adapter defect same cell -> no rescue (PARTIAL)", classify(mod(base(), "maf", "B1", integration_complete=False, invalidation=3, defect=True), False)[0], "PARTIAL")
c = base()
for fw in FRAMEWORKS: c = mod(c, fw, "B4", integration_complete=False, invalidation=2, defect=True)
check("infra cannot rescue all-genuine negative -> FAIL", classify(c, False)[0], "FAIL")
c = mod(mod(base(), "langgraph", "B5", observed_verdict="ALLOW"), "maf", "B1", integration_complete=False, invalidation=2)
check("established PARTIAL not converted to INCONCLUSIVE", classify(c, False)[0], "PARTIAL")
check("p95 nearest rank of 1..100 = 95", p95_nearest_rank(list(range(1, 101))), 95)
rng = random.Random(SEED); xs = [rng.uniform(5, 50) for _ in range(30)]
check("bootstrap deterministic under frozen seed", latency(xs) == latency(xs), True)
r = analyze({"cells": base(), "latency_ms": {"langgraph": xs}, "secondary": {"langgraph": {"adapter_loc": 0}}})
check("endpoint counts P1/P2/P4 = 20", (r["endpoints"]["P1"], r["endpoints"]["P2"], r["endpoints"]["P4"]), (20, 20, 20))
check("P3_c = 1.0 per case", all(v["P3_c"] == 1.0 and v["canonical_hash_identical"] for v in r["endpoints"]["P3"].values()), True)
check("raw CSV export has 21 lines", raw_export_csv(base()).count("\n"), 21)

print(BANNER)
for n, ok, g, w in tests: print(f"{'PASS' if ok else 'FAIL'}  {n}" + ("" if ok else f"  got={g} want={w}"))
print(f"{sum(t[1] for t in tests)}/{len(tests)} synthetic checks passed. {BANNER}. Seed={SEED}.")
sys.exit(0 if all(t[1] for t in tests) else 1)
