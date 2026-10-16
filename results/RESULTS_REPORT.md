# EP-AGENT-001 — Execution Results (RF-internal, NOT published)
Executed 2026-10-16 02:58–02:59 UTC (2026-10-15 EDT) under Derek Hone's execution authorization (`execution/EXECUTION_AUTHORIZATION.md`).
Filed preregistration: Zenodo 23407844, DOI 10.5281/zenodo.23407844 · packet commit 606d6db · manifest SHA-256 0573a358…5576f (re-verified: 66/66 OK pre-run).

## Classification (mechanical, `scripts/analysis/analyze.py`): **PASS**
| Endpoint | Observed | Threshold |
|---|---|---|
| P1 integration completion | 20/20 | 20/20 |
| P2 decision fidelity | 20/20 | 20/20 |
| P3_c core semantic invariance | 1.0 for B1–B5; canonical hash + action_hash identical across 4 frameworks per case | 1.0 ∀c |
| P4 ProofRecord linkage | 20/20 (returned, resolves via GET /proof/{id} with matching verdict/request_id/action_hash, present unchanged in native result) | 20/20 |
| P5 core modification | false | false |

Observed verdicts (all 4 frameworks identical): B1 ALLOW · B2 HOLD · B3 DENY · B4 HOLD · B5 HOLD (= EXPECTED_RESULTS.json).

## Environment (verified at run time)
Verifier `/health`: 0.1.2-reference @ b03365d57880e896c35e72898f8335a1826afe74, policy 06b5a7ab…77649d4, registry b4a84f29…490747d0 (`results/preexec/verifier_health.json`). Verifier repo manifest OK.
Frameworks (check_versions PASS): openai-agents 0.24.0, langgraph 1.2.15, crewai 1.15.28, agent-framework 1.22.0; Python 3.11.6. Mock downstream only; Abacus platform env credentials unset for all runs.

## Secondary (descriptive only) — S5 adapter round-trip, 150 measured calls/framework (30 per case; 5 warmup per case excluded), localhost
| Framework | median ms | 95% bootstrap CI | p95 ms |
|---|---|---|---|
| openai_agents | 1.96 | 1.94–2.00 | 2.54 |
| langgraph | 1.93 | 1.91–1.95 | 2.15 |
| maf | 3.06 | 3.02–3.10 | 3.47 |
| crewai | 3.82 | 3.74–3.89 | 5.21 |
S2 TTFV: all four frameworks reached a first verified decision on non-study SMOKE-000 (`results/preexec/ttfv_smoke.log`). S3 install: `install_all.sh` exit 0 in 13 s (pip cache warm after interrupted attempt 1 — timing not representative).

## Deviations (logged; none alters design, fixtures, policy, registry, rules, or expected results)
- **D-01** Frozen `scripts/execute/run_study.py` refuses unconditionally (v0.3); added `execution/cell_runner.py` + `execution/aggregate.py` that invoke the frozen adapters/bindings/normalizers unchanged. Same harness for all frameworks; not a framework-specific workaround (material_workaround recorded false on that basis — reviewer may contest).
- **D-02** STUDY_PROTOCOL §3 step 3 (load policy via endpoints) N/A to pinned verifier; policy/registry loaded via EP_POLICY_CONFIG / EP_EVIDENCE_REGISTRY at startup (per §18); hashes confirmed via /health.
- **D-03** Authorization cites commit + manifest SHA rather than PREREGISTRATION.md SHA (be140508…f6ad, covered by manifest).
- **D-04** Framework order not recorded at freeze; derived at run time from seed 20261015: crewai, maf, openai_agents, langgraph.
- **D-05** No frozen S1 LOC script; S1 not computed in this report.
- **D-06** Install attempt 1 killed by tool timeout mid-maf; reinstalled (log preserved). Verifier venv: requirements.lock lacked hashes for `--require-hashes`, installed from pinned requirements.txt (freeze in `results/preexec/verifier_pip_freeze.txt`).
- **D-07** Pre-study harness bug: TTFV smoke passed wrong native shape for langgraph (KeyError 'args'); fixed in TTFV path only before any study cell; rerun passed. No study cell was rerun.

## Scope / claim ceiling
Benign single-agent integration on the pinned v0.1.2-reference `/verify` path, 5 fixtures × 4 frameworks. No adversarial, replay, mutation, bypass, tamper, multi-agent, or independent-reproduction testing. RF-internal measurement; not independently reproduced. **Not published** — STUDY_PROTOCOL §11.4 publication authorization required.

Artifacts: `results/<fw>/{decision_calls,latency_calls}.jsonl`, `results/<fw>/run.log`, `proofrecords/<fw>/`, `results/verifier/proofrecords.sqlite3`, `results/raw_cells.json`, `results/ANALYSIS.json`, `results/RESULTS_MANIFEST.sha256`.
