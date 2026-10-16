# EP-AGENT-001 — Study Closeout Summary
**Status: CLOSED — Preregistered mechanical result: PASS, with disclosed execution-procedure deviations.**
Executed 2026-10-16 by Remnant Fieldworks Inc. (PI: Derek Hone). Not rerun, not remediated.

## One-paragraph status
EP-AGENT-001 was a preregistered RF-internal study measuring whether a single pinned ExecutionProof
reference verifier could be integrated across four AI agent frameworks — OpenAI Agents SDK, LangGraph,
CrewAI, and Microsoft Agent Framework — using five frozen benign cases, with the verdict and ProofRecord
returned unchanged to the calling framework. All five primary endpoints passed the preregistered
thresholds (P1=20/20, P2=20/20, P3=1.0 for every case, P4=20/20, P5=false). The first observed result
is the canonical record. No rerun or remediation was performed. The study is closed.

## Narrow external claim (authorized)
> In a preregistered RF-internal study, a pinned ExecutionProof reference verifier integrated across
> OpenAI Agents SDK, LangGraph, CrewAI, and Microsoft Agent Framework across 20 benign framework × case
> cells, with 20/20 decision fidelity and 20/20 ProofRecord linkage, without modifying the core decision
> engine.

**Scope exclusions (must accompany any public use of the above claim):**
Not adversarial. Not multi-agent. Not production validation. Not independently reproduced.
"Demonstrated cross-framework portability across four selected frameworks under the frozen benign
protocol" — the frameworks were integration environments, not validators of ExecutionProof.

## Execution-procedure deviations (permanent record)
Seven deviations are logged in RESULTS_REPORT.md. The most significant is **D-01**: the frozen
`run_study.py` refused to run by design; `execution/cell_runner.py` and `execution/aggregate.py` were
added post-filing to invoke the frozen adapters/bindings/normalizers unchanged using one shared harness
across all four frameworks. The mechanical PASS is recorded with D-01 disclosed. This is not a
zero-deviation run and should not be described as one.

## What is not yet done
- Publication to Zenodo: requires separate authorization (STUDY_PROTOCOL §11.4). → Authorized by Derek 2026-10-16.
- GitHub public release: requires Derek to create the repo and grant access.
- University-reserved work: untouched throughout. Boundary preserved.
- Any follow-on study: would be a separately designed and preregistered EP-AGENT-002 (or R1 only if
  addressing a failure), not a rerun of this study.

## Artifacts
| File | Description |
|---|---|
| RESULTS_REPORT.md | Full results narrative, endpoints table, deviations, claim ceiling |
| ANALYSIS.json | Mechanical classification output (`scripts/analysis/analyze.py`) |
| EXECUTION_AUTHORIZATION.md | Verbatim PI authorization (Derek Hone, 2026-10-15 EDT) |
| raw_cells.json | 20-cell input to analyze.py |
| RESULTS_MANIFEST.sha256 | SHA-256 of every result file |
| proofrecords/<fw>/B*.json | 20 individual ProofRecord JSON files |
| run_logs/<fw>/*.jsonl + run.log | Per-framework decision calls, latency calls, run logs |
| preexec/* | Pre-run checks: manifest verification, verifier /health, version checks, TTFV smoke |

Preregistration: Zenodo 23407844, DOI 10.5281/zenodo.23407844, commit 606d6db.
Execution commit: e8e8fd3c012e5c551b912b465a0f70ee6d9c00a8, tag: ep-agent-001-executed.
