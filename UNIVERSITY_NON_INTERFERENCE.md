# UNIVERSITY NON-INTERFERENCE — EP-AGENT-001

**Source:** Master University Non-Interference + Prior-Work Audit, 2026-10-15
(`/home/ubuntu/RF_University_NonInterference_Audit.md`, Section I and Section J)
**Version:** v0.3.5-DRAFT (2026-10-16). Version history: §2 HISTORICAL / SUPERSEDED and `CHANGELOG.md`.

```
DESIGN:                        COMPLETE
EXECUTIONPROOF PIN:            PASS
Q9:                            PASSED
Q8 TECHNICAL FREEZE READINESS: PASS
Q8 FORMAL:                     OPEN — REQUIRES DEREK APPROVAL + PREREGISTRATION FILING
PREREGISTRATION:               NOT FILED
EXPERIMENT:                    NOT EXECUTED
RESULTS:                       NONE
EXECUTION:                     NOT AUTHORIZED
```

---

## 1. Active university projects and audit verdicts

| Project | Lane | Audit status |
|---|---|---|
| University of Dayton — ExecutionProof Adversarial Boundary Challenge (CPS 474/574 Team A, Fall 2026) | Adversarial: bypass, replay, action drift / post-verification mutation, forged/stale/reused/inadequate evidence, revoked/invalid authority, malformed requests, ProofRecord integrity, HOLD/DENY containment, downstream-effect testing, false-ALLOW | **YELLOW** |
| University of Washington P1 — Adversarial Execution Boundary Testing | Adversarial / boundary challenge | **YELLOW** |
| University of Washington P2 — Multi-Agent Authorization | Authority, delegation, role relationships, agent-to-agent requests | **YELLOW** |
| University of Washington P4 — Independent Reproducibility & Conformance | Independent reproduction, external conformance | **LIGHT GREEN** |

P1, P2, and P4 are treated as three distinct projects.

## 2. EP-AGENT-001 verdict

```
DESIGN-SCOPE VERDICT:          GO WITH BOUNDARY
CURRENT EXECUTION ELIGIBILITY: NOT YET ELIGIBLE
NEW-RESEARCH GATE:             PENDING Q8 FORMAL
  Q8 TECHNICAL FREEZE READINESS: PASS
  Q8 FORMAL STATUS: OPEN — REQUIRES DEREK APPROVAL + PREREGISTRATION FILING
  Q9: PASSED — UNIVERSITY_EXPOSURE_LOG.md §5b
```

"GO WITH BOUNDARY" is a design-scope verdict only. Execution additionally requires (1) a filed preregistration
lock embedding this boundary, (2) Q8 and Q9 PASSED, and (3) Derek Hone's explicit written execution
authorization. Nothing in this document authorizes execution.

**v1 interaction pattern:** one agent → one proposed consequential action → ExecutionProof `/verify` → simulated
downstream boundary. Exactly one tool call per run; no second agent; no single-agent parallel tool calls.

### HISTORICAL / SUPERSEDED (§2)

*Retained in chronological order (Rule 11). None of this is current status; the block at the top of §2 is operative.*

**v0.2 (2026-10-15) — superseded:** study status "PREREGISTRATION DRAFT COMPLETE — HOLD FOR Q9 RECONCILIATION".

```
DESIGN-SCOPE VERDICT:          GO WITH BOUNDARY
CURRENT EXECUTION ELIGIBILITY: NOT YET ELIGIBLE
NEW-RESEARCH GATE:             PENDING Q8 + Q9
  Q8: Preregistration/freeze integrity not yet complete.
  Q9: University exposure log not yet reconciled.
```

**v0.3.1 update (2026-10-16):** Q9 **PASSED** — `UNIVERSITY_EXPOSURE_LOG.md` §5b. New-research gate now pending Q8 only.

**v0.3.3 update (2026-10-16):** Q8 TECHNICAL FREEZE READINESS **PASS** (checklist item 7 PASS — ExecutionProof
Controlled Reference Verifier pinned at `v0.1.2-reference` @ `b03365d5`; see `EXECUTIONPROOF_PIN.md`). Q8 FORMAL
STATUS remains **OPEN UNTIL DEREK APPROVAL + PREREGISTRATION FILING**. Gate at v0.3.3:

```
DESIGN-SCOPE VERDICT:          GO WITH BOUNDARY
CURRENT EXECUTION ELIGIBILITY: NOT YET ELIGIBLE
NEW-RESEARCH GATE:             PENDING Q8 FORMAL
  Q8 TECHNICAL FREEZE READINESS: PASS (v0.3.3)
  Q8 FORMAL STATUS: OPEN UNTIL DEREK APPROVAL + PREREGISTRATION FILING
  Q9: PASSED (v0.3.1)
```

## 3. SAFE (permitted)

1. Framework adapters — single-agent tool-call path only
2. Request Contract normalization — benign, well-formed inputs **only**
3. `/verify` integration — functional correctness of the call path
4. ProofRecord reference return — the single agent's tool result carries the reference; linkage/storage only; no tamper/forgery
5. Adapter LOC
6. Setup burden
7. Latency — internal adapter overhead; labelled "RF internal measurement"
8. Framework portability — same contract across frameworks, single-agent
9. Dependency burden
10. Integration friction

## 4. MODIFY (permitted only under stated conditions)

1. **ALLOW/HOLD/DENY return to the framework** — HOLD/DENY triggered only by benign, policy-driven fixtures
   (required contract field not supplied, role not granted, required evidence not supplied, amount over limit).
   Each fixture differs from B1 by exactly one condition. Never by attack-derived
   inputs (stale, forged, replayed, revoked). Measures that the decision reaches the framework correctly — not
   whether containment resists attack.
2. **Core-decision invariance** — only on the fixed set of five benign normalized contracts (B1–B5), identical
   across frameworks. Invariance under mutated, replayed, stale, or out-of-adapter inputs is UNIVERSITY-RESERVED.

## 5. UNIVERSITY-RESERVED (excluded — never implemented in EP-AGENT-001)

| # | Excluded item | Reserved for |
|---|---|---|
| 1 | Agent-to-agent delegation / handoff | UW P2 |
| 2 | Multi-agent authority / multi-hop delegation | UW P2 |
| 3 | Collusion / confused deputy | UW P2 |
| 3a | Shared authority / inherited permissions / authority propagation between agents | UW P2 |
| 3b | Parallel agents / multi-agent chains / orchestration | UW P2 |
| 4 | Bypassing the adapter / direct unauthorized tool invocation | UD / UW P1 |
| 5 | Replay through adapters | UD / UW P1 |
| 6 | Mutation through adapters | UD / UW P1 |
| 7 | Adversarial malformed input | UD / UW P1 |
| 8 | ProofRecord tamper / forgery | UD |
| 9 | Independent reproduction claims | UW P4 |
| 10 | External conformance claims | UW P4 |

Implied exclusions derived from the UD lane and applied here as well: forged / stale / reused / inadequate
evidence; revoked or invalid authority; post-verification action drift; downstream-effect resistance testing;
false-ALLOW hunting.

v1 scope rule (not a reservation, a simplification that keeps the study clearly outside UW P2): single-agent
parallel tool calls are excluded; exactly one tool call per run.

## 6. New-research gate (10 questions) applied to EP-AGENT-001

| # | Question | Answer for EP-AGENT-001 |
|---|---|---|
| Q1 | Does the study's primary RQ match a reserved university RQ? | **NO.** EP-AGENT-001's RQ is framework portability, not adversarial evaluation (UD/P1), not multi-agent authorization (P2), not independent reproduction (P4). |
| Q2 | Same SUT, same boundary, same threat model? | SUT is the same (ExecutionProof). Boundary is the same. But the threat model is **DIFFERENT** — EP-AGENT-001 uses benign policy-driven fixtures only, not adversarial. Not all three match → condition not met → **NO.** |
| Q3 | Would results function as an answer key for an active team? | **NO.** Benign portability results do not answer adversarial (UD/P1), multi-agent (P2), or reproduction (P4) questions. |
| Q4 | Adversarial, bypass, replay, mutation, tamper, false-ALLOW? | **NO.** Explicitly excluded. |
| Q5 | More than one agent holding/delegating/exercising authority? | **NO.** Single-agent paths only; delegation excluded. |
| Q6 | Claims using "independent", "external", "reproduced by", "conformant"? | **NO.** Claim ceiling prohibits these. |
| Q7 | Reserved elements removable while preserving a meaningful RF question? | **YES.** Reserved sub-variants are removed from each test case by boundary definition. |
| Q8 | Preregistered with SHA lock, exclusions, claim boundary? | **Q8 TECHNICAL FREEZE READINESS: PASS (v0.3.3)** — checklist item 7 PASS (reference verifier pinned `v0.1.2-reference` @ `b03365d5`); items 1–6, 8–11 PASS. *(History: §6 note below.)* **Q8 FORMAL STATUS: OPEN UNTIL DEREK APPROVAL + PREREGISTRATION FILING.** |
| Q9 | Would EP-AGENT-001 execution or student-facing material interfere with an active university project (exposure log checked)? | **PASSED (v0.3.1)** — written-record Gmail search + Derek Hone written confirmation; `UNIVERSITY_EXPOSURE_LOG.md` §5b. *(History: §6 note below.)* |
| Q10 | Safety/security necessity overriding wait? | **NO.** |

**Gate result:** DESIGN-SCOPE VERDICT **GO WITH BOUNDARY** (Q1–Q6 NO; Q7 YES; Q10 NO). CURRENT EXECUTION ELIGIBILITY **NOT YET ELIGIBLE**. NEW-RESEARCH GATE **PENDING Q8 FORMAL**.

**HISTORICAL / SUPERSEDED (§6), chronological:** v0.2 — Q8: v0.2 draft and PRE-FILING CANDIDATE LOCK exist; final lock requires Derek Hone's written approval and filing. Q9: EP-AGENT-001-specific exposure none recorded in RF records available to this audit; UD kickoff/brief contents UNKNOWN — TO RECONCILE; older ARK/P01 exposure is governed by the Master Audit and does not by itself fail Q9; UW teams not yet assigned; see `UNIVERSITY_EXPOSURE_LOG.md`. Gate: PENDING Q8 + Q9. v0.3 — Q8 technical freeze readiness FAIL (checklist item 7 BLOCKED — ExecutionProof implementation commit not confirmable). Q9 OPEN — records reconciled as far as available (`UNIVERSITY_EXPOSURE_LOG.md` §5a); A, B, D, E: no exposure recorded; C undetermined; two Derek confirmations remain. v0.3.1 — Q9 PASSED. v0.3.3 — Q8 technical freeze readiness PASS (item 7 PASS).

## 7. Applicable permanent rules (from audit Section J)

- Rule 1 (reserved-question), Rule 2 (prior work is not interference), Rule 3 (no answer keys pre-plan),
  Rule 7 (independence language), Rule 10 (audit refresh trigger), Rule 11 (records immutability),
  Rule 12 (gate-before-execute), Rule 13 (exposure log), Rule 14 (completion release).
- Per Rule 10, this gate is re-run at preregistration freeze and whenever a UD or UW primary brief becomes available.
- Per Rule 3, EP-AGENT-001 results (once they exist) are not shared with any university team before that team freezes its own plan, and any sharing is logged per Rule 13.

## 8. Commitment

Remnant Fieldworks commits that EP-AGENT-001 will:

1. Execute only the SAFE and MODIFY cases listed above, under their stated conditions.
2. Execute no UNIVERSITY-RESERVED item, in any adapter, fixture, script, or ad-hoc run.
3. Make no claim of adversarial robustness, multi-agent authorization, independent reproduction, or external conformance.
4. Never describe RF's own work as "independent validation" or any university as "a validator".
5. Log every university-facing exposure of this packet or its results in `UNIVERSITY_EXPOSURE_LOG.md`.
6. Re-run the gate before execution and on any change to university project scope.
7. Assign no University of Dayton or University of Washington student, team, or faculty member any EP-AGENT-001
   role — not consultant, co-investigator, participant, reviewer, or executor.
8. Share no EP-AGENT-001 fixtures, expected outcomes, answer keys, or results with any university team while its
   reserved project is active.

> "University Non-Interference Boundary: This study is intentionally limited to framework portability, request
> normalization, verification-interface integration, decision propagation, ProofRecord linkage, and engineering
> integration characteristics. It does not test or resolve active University of Dayton or University of
> Washington adversarial, multi-agent authorization, or independent reproducibility research questions."
