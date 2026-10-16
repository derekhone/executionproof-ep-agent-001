"""Aggregate raw cell records into analyze.py input (mechanical; no judgement calls)."""
import json, hashlib, pathlib
R = pathlib.Path("results"); FWS = ["openai_agents", "langgraph", "crewai", "maf"]
EXCL = {"request_id", "framework_id", "nonce", "requested_at"}
cells, lat = [], {}
for fw in FWS:
    for r in map(json.loads, open(R / fw / "decision_calls.jsonl")):
        c = r.get("normalized_contract") or {}
        canon = {k: v for k, v in c.items() if k not in EXCL}
        ah = (r.get("raw_verify_response") or {}).get("action_hash")
        nat = r.get("framework_native_result") or ""
        nat = nat if isinstance(nat, str) else json.dumps(nat)
        pid = r.get("proof_record_id")
        cells.append(dict(framework=fw, case=r["case_id"],
            integration_complete=bool(r.get("schema_valid") and r.get("http_status") == 200 and r.get("observed_verdict")
                                      and r.get("verdict_in_native_result") and not r.get("manual_intervention") and not r.get("error")),
            observed_verdict=r.get("observed_verdict"), expected_verdict=r["expected_verdict"],
            proof_ref_returned=bool(pid), proof_ref_resolves=bool(r.get("proof_record_resolves") and r.get("proof_verdict_matches")
                                                                   and r.get("proof_request_id_matches") and r.get("proof_action_hash_matches")),
            proof_ref_unchanged=bool(pid and r.get("proof_ref_in_native_result") and pid in nat),
            material_workaround=False,
            canonical_hash=hashlib.sha256(json.dumps(canon, sort_keys=True).encode()).hexdigest(),
            action_hash=ah, invalidation=None, defect=r.get("error")))
    L = [json.loads(l) for l in open(R / fw / "latency_calls.jsonl")]
    if fw == FWS[0]: print("latency keys:", sorted(L[0].keys()))
    key = next(k for k in ("s5_adapter_round_trip_ns", "verify_rtt_ns") if k in L[0])
    meas = [x for x in L if not x.get("warmup", x.get("phase") == "warmup")]
    lat[fw] = [x[key] / 1e6 for x in meas]
    print(fw, "latency n=", len(lat[fw]), "key=", key)
by = {}
for c in cells: by.setdefault(c["case"], set()).add((c["canonical_hash"], c["action_hash"]))
print("cross-framework canonical/action_hash distinct per case:", {k: len(v) for k, v in by.items()})
json.dump({"cells": cells, "latency_ms": lat, "p5_core_modified": False, "secondary": {}}, open(R / "raw_cells.json", "w"), indent=2)
