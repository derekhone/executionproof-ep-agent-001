# COST ESTIMATE — EP-AGENT-001

**Version:** v0.1-DRAFT (2026-10-15). All figures are **estimates** made at design time, not measurements.

| Item | Estimate | Basis |
|---|---|---|
| Build time | ~16–24 hours | Design (done) + implementing four adapters from stubs + harness wiring + dry-run on a non-study smoke fixture + freeze paperwork |
| Execution time | ~2–4 hours | 20 decision cells + 600 measured latency calls + 100 warmups + setup timing for 4 clean venvs + ProofRecord capture |
| API costs — ExecutionProof | ~$0 on a local/sandbox instance; ~$1–5 if a cloud endpoint is used (estimate) | ~720 `/verify` calls + 20 `/proof/{id}` calls |
| API costs — LLM | ~$0 target | Tool arguments come from fixtures; deterministic stub model / forced tool choice preferred |
| Compute | ~$0 (local laptop/workstation) | No GPU; serial calls |
| Storage | < 10 MB total | JSONL logs, 20 ProofRecords, environment dumps |
| Framework dependencies | $0 | All four frameworks MIT-licensed and free |
| Paid services / subscriptions | None required | — |

**Approval note:** any use of a cloud ExecutionProof endpoint or any paid model API requires Derek Hone's approval
before use.
