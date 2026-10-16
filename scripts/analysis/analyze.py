#!/usr/bin/env python3
"""
EP-AGENT-001 analysis (implements ANALYSIS_PLAN.md v0.3 and PASS_FAIL_RULES.md v0.3 mechanically).
Input: a raw-data JSON file {"cells": [...], "secondary": {...}, "latency_ms": {...}, "p5_core_modified": bool}.
Each cell: framework, case, integration_complete, observed_verdict, expected_verdict, proof_ref_returned,
proof_ref_resolves, proof_ref_unchanged, material_workaround, canonical_hash, invalidation (null | condition
id 1-5), defect (bool: adapter/normalizer/contract/verdict defect observed in this cell).
Never writes to results/ unless an explicit --out path is given by the gated runner. No network access.
"""
import argparse, csv, hashlib, io, json, random, statistics, sys
from collections import Counter

SEED = 20261015  # EP_AGENT_001_SEED — frozen at v0.3 candidate lock
FRAMEWORKS = ["openai_agents", "langgraph", "crewai", "maf"]
CASES = ["B1", "B2", "B3", "B4", "B5"]
BOOT_N = 1000


def cell_ok(c):
    linked = c["proof_ref_returned"] and c["proof_ref_resolves"] and c["proof_ref_unchanged"]
    return (c["integration_complete"] and c["observed_verdict"] == c["expected_verdict"]
            and linked and not c["material_workaround"])


def label(c):
    """VALID or INVALIDATED (PASS_FAIL_RULES Step 0). A defect always makes the cell VALID (no rescue)."""
    if c.get("invalidation") in (1, 2, 3, 4, 5) and not c.get("defect") and not cell_ok(c):
        return "INVALIDATED"
    return "VALID"


def endpoints(cells, p5):
    P1 = sum(bool(c["integration_complete"]) for c in cells)
    P2 = sum(c["observed_verdict"] == c["expected_verdict"] for c in cells)
    P4 = sum(bool(c["proof_ref_returned"] and c["proof_ref_resolves"] and c["proof_ref_unchanged"]) for c in cells)
    P3 = {}
    for k in CASES:
        vs = [c["observed_verdict"] for c in cells if c["case"] == k]
        hs = {c["canonical_hash"] for c in cells if c["case"] == k}
        modal = Counter(vs).most_common(1)[0][1] if vs else 0
        P3[k] = {"agree": modal, "of": len(vs), "P3_c": modal / len(vs) if vs else 0.0, "canonical_hash_identical": len(hs) == 1}
    return {"P1": P1, "P2": P2, "P3": P3, "P4": P4, "P5": bool(p5), "n_cells": len(cells)}


def classify(cells, p5, core_divergence=False, contract_incompatible_frameworks=0):
    labels = {(c["framework"], c["case"]): label(c) for c in cells}
    genuine = {fw: [c for c in cells if c["framework"] == fw and labels[(fw, c["case"])] == "VALID" and not cell_ok(c)] for fw in FRAMEWORKS}
    full = [fw for fw in FRAMEWORKS if all(labels[(fw, c["case"])] == "VALID" and cell_ok(c) for c in cells if c["framework"] == fw)
            and sum(c["framework"] == fw for c in cells) == 5]
    invalidated = [k for k, v in labels.items() if v == "INVALIDATED"]
    if p5 or contract_incompatible_frameworks >= 2 or core_divergence or all(genuine[fw] for fw in FRAMEWORKS):
        return "FAIL", "Step 1: FAIL condition on genuine evidence"
    if full and any(genuine[fw] for fw in FRAMEWORKS):
        return "PARTIAL", "Step 2: established PARTIAL (≥1 fully successful, ≥1 genuine shortfall)"
    if invalidated:
        return "INCONCLUSIVE", f"Step 3: invalidated cells {sorted(invalidated)}; genuine shortfalls reported: {sum(len(v) for v in genuine.values())}"
    if len(full) == 4 and len(cells) == 20:
        return "PASS", "Step 4: all PASS conditions hold"
    return ("PARTIAL", "Step 5") if full else ("FAIL", "Step 5: no fully successful framework")


def p95_nearest_rank(xs):
    s = sorted(xs); return s[max(0, -(-95 * len(s) // 100) - 1)]


def latency(xs, seed=SEED):
    rng = random.Random(seed)
    boots = sorted(statistics.median(rng.choices(xs, k=len(xs))) for _ in range(BOOT_N))
    return {"n": len(xs), "median": statistics.median(xs), "p95": p95_nearest_rank(xs),
            "median_ci95_bootstrap": [boots[int(0.025 * BOOT_N)], boots[int(0.975 * BOOT_N) - 1]], "seed": seed}


def verdict_comparison(cells):
    return [{"framework": c["framework"], "case": c["case"], "expected": c["expected_verdict"],
             "observed": c["observed_verdict"], "match": c["observed_verdict"] == c["expected_verdict"]} for c in cells]


def raw_export_csv(cells):
    buf = io.StringIO(); keys = sorted(cells[0]) if cells else []
    w = csv.DictWriter(buf, fieldnames=keys); w.writeheader(); [w.writerow(c) for c in cells]; return buf.getvalue()


def analyze(data):
    cells = data["cells"]
    cls, why = classify(cells, data.get("p5_core_modified", False), data.get("core_divergence", False),
                        data.get("contract_incompatible_frameworks", 0))
    return {"endpoints": endpoints(cells, data.get("p5_core_modified", False)),
            "classification": cls, "classification_reason": why,
            "secondary": data.get("secondary", {}),  # LOC, setup steps, dependency count, installed size — descriptive only
            "latency": {fw: latency(v) for fw, v in data.get("latency_ms", {}).items()},
            "verdict_comparison": verdict_comparison(cells),
            "proofrecord_reference": [{"framework": c["framework"], "case": c["case"], "returned": c["proof_ref_returned"],
                                       "resolves": c["proof_ref_resolves"], "unchanged": c["proof_ref_unchanged"]} for c in cells],
            "raw_csv_sha256": hashlib.sha256(raw_export_csv(cells).encode()).hexdigest()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("raw"); ap.add_argument("--out")
    a = ap.parse_args(); res = analyze(json.load(open(a.raw)))
    s = json.dumps(res, indent=2, sort_keys=True)
    (open(a.out, "w").write(s) if a.out else print(s))
