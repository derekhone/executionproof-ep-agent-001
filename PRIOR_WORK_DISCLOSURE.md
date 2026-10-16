# PRIOR-WORK DISCLOSURE — EP-AGENT-001

**Version:** v0.1-DRAFT (2026-10-15)
**Source:** Master University Non-Interference + Prior-Work Audit (2026-10-15), Sections J.1 and J.2, and the RF
canonical corpus ledger (v40, 2026-10-08: 109 experiments / 97 PASS / 9 preserved FAIL / 3 special / 14 families /
93 Zenodo records) as cited by that audit.

All prior work below is RF-run, on RF reference implementations, using RF-authored cases. None of it is
independent validation. All of it is disclosed and preserved (Rule 2: prior work is not interference).

---

## 1. RF prior work relevant to the ExecutionProof boundary

| Artifact | Repo | Exp. ID(s) | DOI / record | Date | Recorded result | Relationship to EP-AGENT-001 |
|---|---|---|---|---|---|---|
| Enterprise Agent Boundary Testbed (ARK corpus) | `executionproof-testbeds` (`ark-493-498/`) | ARK-493 to ARK-498 | 10.5281/zenodo.21462612 (prereg v1.1, SHA `464b9fb8…52952a`) | 2026-07 | 161/161 PASS, 0 leaks (RF-run) | Adversarial/boundary content (bypass, mutation, mid-flight authority change, delegation, tamper). **Not imported.** |
| ARK-496 delegation & self-approval | `executionproof-testbeds` | ARK-496 | 10.5281/zenodo.21462612 | 2026-07 | 8/8 PASS | Closest prior work to UW P2. **Not imported**; delegation excluded from EP-AGENT-001. |
| P01 failure-mode series (ARK) | `executionproof-testbeds` (`P01_COMPLETION_REPORT.md`) | ARK-458 to ARK-482 | Zenodo records 21432645 … 21433485 (25 records) | 2026-07-18 | 25/25 PASS; 20,000 decisions; 100% JS/Python concordance; synthetic, implementation-specific | Exact-action binding, revocation-at-execution, cross-context replay. **Not imported.** |
| ARK hardware boundary series | `executionproof-testbeds` | ARK-441 to ARK-446 | 10.5281/zenodo.21398676 | 2026-07 | 443 PASS; 444 PASS; 445 FAIL → 445b | Background only. |
| Intent-binding series (IB) | `executionproof-testbeds` (`intent-binding/`) | IB-001, IB-002, IB-003 | 10.5281/zenodo.22002829 | 2026-08 | IB-001 FAIL, IB-002 FAIL (preserved); IB-003 PASS 12/12 | Showed deterministic matching can falsely block synonyms before normalization fixes. Relevant as background to *normalization*; EP-AGENT-001 does not test synonym/drift handling. |
| Authority partitioning (AUTH) | `executionproof-testbeds` (`authority-partitioning/`) | AUTH-001, AUTH-002 (cases A01–A18) | 10.5281/zenodo.22002833 | prereg locked 2026-08-15 | Per corpus ledger (results not re-read by the audit) | Single-actor capability grants; non-inheritance invariant. Background for the static authority condition in B3. |
| ExecutionProof production status | `executionproof` (`PRODUCTION-STATUS.md`) | EP-7006, EP-7008 | none | 2026-08 (v1.0.0-public) | Live architecture description (four-engine pipeline) | Describes the system under integration. Records RF-100 §8.4 conformance as "pending independent external review" (UW P4 lane left open). |
| EP security series | `executionproof-testbeds` (`ep-sec-001-009/`) | EP-SEC-001 to 009 (+009b) | not confirmed | 2026 | EP-SEC-009 FAIL → 009b (ledger); README returned 404; **contents unverified** | Provisionally POTENTIALLY BIASING for UD/P1. **Nothing from EP-SEC is used by EP-AGENT-001.** |

Other RF families (WITNESS, BELLWETHER, CHRONO, OMNI, TRINITY, DM, QG, CUDA-EP, EP-PQC) are classified SAFE
BACKGROUND by the audit and have no bearing on EP-AGENT-001's design. FIDELITY is SAFE WITH CLAIM BOUNDARY and is
not used. RF-100 is the formal standard; RF-run work cannot self-certify conformance to it.

## 2. Separation statement

EP-AGENT-001 is intentionally separated from the adversarial and multi-agent prior work above:

1. **It does not import adversarial case tables.** No ARK, P01, ARK-496, EP-SEC, or IB case definition, case list,
   per-cell outcome, or attack-derived input is used in any EP-AGENT-001 fixture.
2. **Its five fixtures (B1–B5) are newly authored**, benign, policy-driven, and correspond one-to-one to the core
   invariants (ALLOW; incomplete → HOLD; authority FAIL → DENY; evidence FAIL → HOLD; constraint FAIL → HOLD).
3. **Its question is different:** integration portability across agent frameworks, not boundary robustness.
4. **Its results cannot serve as an answer key** for UD, UW P1, UW P2, or UW P4 (gate Q3 = NO).
5. **No prior result is reinterpreted, renamed, or suppressed** to frame EP-AGENT-001 as novel.

## 3. What EP-AGENT-001 relies on from prior work

Only the publicly described ExecutionProof architecture and interface family (`PRODUCTION-STATUS.md`, API v2.1):
the decision path, the ALLOW / HOLD / DENY outcome set, the core invariants, and the `/verify` and `/proof/{id}`
interfaces. These are system descriptions, classified SAFE BACKGROUND for all university teams.

## 4. Open items

- EP-SEC contents remain unverified (README 404). Re-check at freeze; EP-AGENT-001 does not depend on them.
- AUTH-001/002 results were not re-read by the audit; cited per ledger only.
- The truncated ARK-493–498 prereg SHA (`464b9fb8…52952a`) is reproduced as cited by the audit; the full value should be copied from the source repository at freeze.
