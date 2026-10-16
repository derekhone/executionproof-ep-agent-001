# ANALYSIS PLAN — EP-AGENT-001

**Version:** v0.2-DRAFT (2026-10-15) — DESIGN ONLY. No data exist.

## 1. Study character

EP-AGENT-001 is a **deterministic integration study**. For a fixed contract and fixed policy, the ExecutionProof
decision is expected to be deterministic; the study asks whether four integration paths deliver that decision
and its ProofRecord linkage intact. Analysis is therefore **descriptive**: exact counts, exact agreement, and
distributional summaries of engineering metrics. No hypothesis tests are run on primary endpoints.

## 2. Primary endpoints (confirmatory)

| Endpoint | Computation | Reporting |
|---|---|---|
| P1 | Σ I(integration_complete) over 20 cells | "k/20 (x%)" plus a 4×5 cell table |
| P2 | Σ I(observed = expected) over 20 cells | "k/20 (x%)"; every mismatch listed with framework, case, observed, expected |
| P3 | Per case: share of frameworks agreeing with the modal verdict | P3_B1…P3_B5 each as "k/4"; any divergence listed; canonical-field and `action_hash` equality reported per case |
| P4 | Σ I(ref returned ∧ resolves ∧ present unchanged in framework-native result) over 20 cells | "k/20"; failures listed by sub-condition |
| P5 | Boolean | true/false with description of any core change |

**Decision fidelity is exact agreement; there is no tolerance.** A verdict is the exact string `ALLOW`, `HOLD`,
or `DENY`; anything else (including errors, timeouts, or null) is a mismatch.

Classification is applied mechanically per `PASS_FAIL_RULES.md`.

## 3. Secondary endpoints (descriptive)

| Metric | Summary |
|---|---|
| S1 Adapter LOC | Integer per framework; shared vs framework-specific lines |
| S2 Setup burden | Step count; time-to-first-verify (s) |
| S3 Dependency burden | Added package count; installed size (MB) |
| S4/S5 Latency | median, p95, min, max per cell; raw values published alongside |
| S6 Integration friction | Count of workarounds/deviations + qualitative notes |
| S7 Configuration surface | Count of framework-specific config keys/objects |

## 4. Latency protocol

- Warmup: **5** calls per case per framework, discarded.
- Sample: **30** measured calls per case per framework (600 measured calls total).
- Timer: `time.perf_counter_ns()`; boundaries defined in `STUDY_PROTOCOL.md` §7.
- Report: median and p95 (p95 = nearest-rank on the 30 samples), plus min/max and the raw vector.
- Optional: bootstrap 95% CI for the median, 1,000 resamples, percentile method, seed **20261015** (frozen v0.3; `EP_AGENT_001_SEED`). Implemented in `scripts/analysis/analyze.py`; validated only by `scripts/analysis/selftest_synthetic.py` (synthetic dummy data — not evidence).
- Label: "RF internal measurement" with host CPU, OS, Python version, and ExecutionProof deployment mode.
- Latency never affects classification.

## 5. Framework comparison table (structure)

| Framework | Version | P1 cells | P2 cells | P4 cells | Core mod? | LOC | Steps | TTFV (s) | Added deps | S5 median (ms) | S5 p95 (ms) | Workarounds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| openai_agents | 0.24.0 | k/5 | k/5 | k/5 | y/n | n | n | x | n | x | x | n |
| langgraph | 1.2.15 | … | … | … | … | … | … | … | … | … | … | … |
| crewai | 1.15.28 | … | … | … | … | … | … | … | … | … | … | … |
| maf | 1.22.0 | … | … | … | … | … | … | … | … | … | … | … |

Raw values are reported alongside any ranking. No framework is declared "best"; differences are reported as
measured values with host context.

## 6. What is not done

- No inferential statistics are manufactured for trivial technical variability (e.g., no t-tests or p-values on
  latency differences of a few milliseconds between frameworks on one host).
- No post-hoc exclusion of cells, frameworks, or latency outliers. Outliers are reported, not removed.
- No pooled "overall score" combining primary and secondary endpoints.
- No re-analysis that changes thresholds after data are seen.

## 7. Deviation handling

- Deviations are logged per `STUDY_PROTOCOL.md` §10 and reported in a dedicated section of the results.
- Any analysis not specified here is labelled **exploratory** and cannot change the classification.
- If an INCONCLUSIVE condition is invoked, the analysis reports all cells that did complete, clearly marked, and
  names the invalidation condition with evidence.

## 8. Missing data

A cell with no usable decision response counts as `integration_complete = false`, a P2 mismatch, and a P4 failure,
unless an INCONCLUSIVE condition is documented for that cell; in that case it is reported as invalidated, not
silently dropped.
