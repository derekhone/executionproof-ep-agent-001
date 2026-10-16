# EP-AGENT-001: Cross-Framework ExecutionProof Integration Study

**Preregistered mechanical result: PASS, with disclosed execution-procedure deviations.**

A preregistered RF-internal study measuring whether a single pinned
ExecutionProof reference verifier preserves ALLOW/HOLD/DENY semantics and ProofRecord linkage across four AI agent frameworks.

| | |
|---|---|
| **Status** | CLOSED — PASS (disclosed deviations) |
| **Preregistration** | [Zenodo 23407844](https://zenodo.org/record/23407844) · DOI [10.5281/zenodo.23407844](https://doi.org/10.5281/zenodo.23407844) |
| **Results** | [Zenodo 23407994](https://zenodo.org/record/23407994) · DOI [10.5281/zenodo.23407994](https://doi.org/10.5281/zenodo.23407994) |
| **Execution commit** | `e8e8fd3`, tag `ep-agent-001-executed` |
| **PI** | Derek Hone, Remnant Fieldworks Inc. |
| **Executed** | 2026-10-16 UTC |

## Narrow authorized claim

> In a preregistered RF-internal study, a pinned ExecutionProof reference verifier integrated across OpenAI Agents SDK, LangGraph, CrewAI, and Microsoft Agent Framework across 20 benign framework × case cells, with 20/20 decision fidelity and 20/20 ProofRecord linkage, without modifying the core decision engine.

**Scope exclusions:** Not adversarial. Not multi-agent. Not production validation. Not independently reproduced. The frameworks were integration environments, not validators of ExecutionProof. Best characterized as: *demonstrated cross-framework portability across four selected frameworks under the frozen benign protocol.*

## Primary endpoints

| Endpoint | Observed | Threshold |
|---|---|---|
| P1 Integration completion | **20/20** | 20/20 |
| P2 Decision fidelity | **20/20** | 20/20 |
| P3 Semantic invariance | **1.0 for all 5 cases** | 1.0 ∀c |
| P4 ProofRecord linkage | **20/20** | 20/20 |
| P5 Core modification | **none** | none |

Observed verdicts (identical across all 4 frameworks): B1 ALLOW · B2 HOLD · B3 DENY · B4 HOLD · B5 HOLD.

## Frameworks tested

| Framework | Version | Result |
|---|---|---|
| OpenAI Agents SDK | 0.24.0 | 5/5 ✓ |
| LangGraph | 1.2.15 | 5/5 ✓ |
| CrewAI | 1.15.28 | 5/5 ✓ |
| Microsoft Agent Framework | 1.22.0 | 5/5 ✓ |

Verifier: ExecutionProof Controlled Reference Verifier v0.1.2-reference, commit `b03365d`.

## Disclosed deviations

Seven execution-procedure deviations (D-01..D-07) are documented in RESULTS_REPORT.md. Most significant: **D-01** — the frozen `scripts/execute/run_study.py` refused to run by design; `execution/cell_runner.py` was added post-filing to invoke the frozen adapters/bindings/normalizers unchanged using one shared harness across all four frameworks. This is **not a zero-deviation run.**

## Repository structure

```
adapters/            Framework adapters (frozen at filing)
fixtures/            Frozen benign cases B1–B5, policy, evidence registry
execution/           Post-filing execution harness (see D-01)
results/             Decision/latency JSONL, run logs, ANALYSIS.json, RESULTS_REPORT.md
proofrecords/        20 ProofRecord JSON files (one per cell)
scripts/             Analysis and setup scripts
filing/              Zenodo filing record
STUDY_CLOSEOUT.md    Closeout summary
PREREGISTRATION.md   Frozen preregistration
STUDY_PROTOCOL.md    Frozen protocol
MANIFEST.sha256      66-file packet manifest
```

## Citation

**Preregistration:**
> Hone, D. (2026). *EP-AGENT-001 Preregistration*. Zenodo. https://doi.org/10.5281/zenodo.23407844

**Results:**
> Hone, D. (2026). *EP-AGENT-001 Results: Cross-Framework Portability of ExecutionProof Reference Verifier Across Four Agent Frameworks (RF-Internal Controlled Study)*. Zenodo. https://doi.org/10.5281/zenodo.23407994

---
*Remnant Fieldworks Inc. — ExecutionProof research program.*
