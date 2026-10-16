# TEST MATRIX — EP-AGENT-001 (benign cases only)

**Version:** v0.2-DRAFT (2026-10-15) — DESIGN ONLY; pre-filing corrections (B2/B4 rescoped to exactly one condition each). Expected verdicts are preregistered expectations, not results.

- Action archetype (all cases): `SUBMIT_EXTERNAL_ACTION` → mock target `mock-external-endpoint`
- Frameworks: openai_agents, langgraph, crewai, maf → 5 cases × 4 frameworks = **20 cells**
- Every case is semantically identical across all four frameworks: the same fixture contract and the same
  fixture policy context are used; only `framework_id`, `request_id`, `nonce`, and `requested_at` differ.
- Every case is one agent → one proposed `SUBMIT_EXTERNAL_ACTION` → `/verify` → simulated downstream boundary.
  No case is multi-step, parallel, stateful, recovery, handoff, delegation, or orchestration.
- Each of B2–B5 differs from the B1 baseline by **exactly one condition** (field `single_condition_vs_B1` in each
  fixture; enforced by `scripts/validation/validate_fixtures.py`).

## Shared fixture policy context (identical in all five fixtures)

| Element | Value |
|---|---|
| Contract completeness requirement | `current_state_reference` required for `SUBMIT_EXTERNAL_ACTION` |
| Authority grants | `test-actor-authorized` → `SUBMIT_EXTERNAL_ACTION` on `mock-external-endpoint` (no other grants) |
| Evidence requirement | ≥1 evidence reference with status `verified` for `SUBMIT_EXTERNAL_ACTION` |
| Constraint | `parameters.amount <= 100` (policy `policy://constraints/submit-external/standard`) |
| Evidence records | Declared per fixture in `fixture_policy_context.evidence_records` (one `verified` record in B1, B2, B3, B5; none in B4) |

## Section 11 university-interference check (applied to every case)

A case PASSES the check only if all are true: (a) input is schema-valid and well-formed; (b) the triggering
condition is an ordinary static policy condition or benign incomplete state; (c) no element is forged, stale,
replayed, reused, revoked, mutated after verification, or tampered; (d) single actor, single agent, no
delegation; (e) no attempt to reach the target outside the adapter; (f) the case does not function as an
answer-key entry for any UD/UW adversarial, multi-agent, or reproduction question.

---

### B1 — ALLOW_COMPLETE

| Field | Value |
|---|---|
| Description | Complete Request Contract. Authorized actor. Required evidence present and verified. Constraint satisfied (amount 50 ≤ 100). |
| Action archetype | SUBMIT_EXTERNAL_ACTION |
| Fixture | `fixtures/benign/B1_allow_complete.json` |
| Expected verdict | **ALLOW** |
| Rationale | All required checks PASS → ALLOW |
| University-interference check | PASS — (a)–(f) satisfied; no attack vector |
| Cross-framework note | Each adapter must return ALLOW and a resolvable ProofRecord reference; the mock action body is invoked only after ALLOW |

### B2 — HOLD_INCOMPLETE_CONTRACT

| Field | Value |
|---|---|
| Description | Exactly one required benign field absent: `current_state_reference` is omitted from the contract, while the fixture policy requires it for `SUBMIT_EXTERNAL_ACTION`. Evidence present and verified; authorized actor; amount 50. All other fields identical to B1. |
| Single condition vs B1 | `contract.current_state_reference` absent |
| Action archetype | SUBMIT_EXTERNAL_ACTION |
| Fixture | `fixtures/benign/B2_hold_incomplete_contract.json` |
| Expected verdict | **HOLD** |
| Rationale | Incomplete contract → HOLD |
| University-interference check | PASS — schema-valid benign omission (an ordinary "not yet supplied" state); not a malformed request, not inadequate/forged evidence |
| Cross-framework note | Normalizers emit `"current_state_reference": null` when the field is absent (never inject a default value). `null` under a policy that requires the field = incomplete contract → HOLD |

### B3 — DENY_NO_AUTHORITY

| Field | Value |
|---|---|
| Description | `actor_id = test-actor-unauthorized` has no authority grant for `SUBMIT_EXTERNAL_ACTION` in the fixture policy. Evidence present and verified; amount within limit. Static policy condition only. |
| Single condition vs B1 | Actor identity (the actor-keyed reference strings follow the actor id; that evidence remains verified) |
| Action archetype | SUBMIT_EXTERNAL_ACTION |
| Fixture | `fixtures/benign/B3_deny_no_authority.json` |
| Expected verdict | **DENY** |
| Rationale | Authority FAIL → DENY |
| University-interference check | PASS — "role not granted" in a static policy. Not a revoked grant, not invalid/forged authority, not a mid-flight authority change, not a delegation attempt |
| Cross-framework note | Identity comes only from the explicit `actor_id` argument; no framework may infer identity from agent name/role |

### B4 — HOLD_EVIDENCE_ABSENT

| Field | Value |
|---|---|
| Description | Required benign evidence simply absent: `evidence_references = []` and no evidence record, while the policy requires ≥1 verified reference. Contract otherwise complete (incl. `current_state_reference`); authorized actor; amount 50. |
| Single condition vs B1 | Required evidence absent |
| Action archetype | SUBMIT_EXTERNAL_ACTION |
| Fixture | `fixtures/benign/B4_hold_evidence_absent.json` |
| Expected verdict | **HOLD** |
| Rationale | Authority PASS + Evidence FAIL → HOLD |
| University-interference check | PASS — evidence simply not supplied. **No** forged, stale, replayed, malformed, manipulated, or adversarial evidence |
| Cross-framework note | Normalizers must emit `"evidence_references": []` (not drop the key, not inject defaults) |

### B5 — HOLD_CONSTRAINT_EXCEEDED

| Field | Value |
|---|---|
| Description | `parameters.amount = 101`; fixture policy constraint `amount <= 100`. Authorized actor; verified evidence. |
| Single condition vs B1 | `parameters.amount = 101` (benign constraint failure) |
| Action archetype | SUBMIT_EXTERNAL_ACTION |
| Fixture | `fixtures/benign/B5_hold_constraint_exceeded.json` |
| Expected verdict | **HOLD** |
| Rationale | Authority PASS + Constraint FAIL → HOLD |
| University-interference check | PASS — an ordinary over-limit request submitted as-is. Not a parameter mutation, not post-verification drift, not a boundary-probing sweep |
| Cross-framework note | `amount` must reach `/verify` as the integer 101 in all frameworks (no coercion, rounding, or string conversion) |

---

## Summary

| Case | Expected | Invariant exercised | Interference check |
|---|---|---|---|
| B1 | ALLOW | all PASS → ALLOW | PASS |
| B2 | HOLD | incomplete (missing `current_state_reference`) → HOLD | PASS |
| B3 | DENY | Authority FAIL → DENY | PASS |
| B4 | HOLD | Evidence FAIL (absent) → HOLD | PASS |
| B5 | HOLD | Constraint FAIL → HOLD | PASS |

No other cases exist. Adding a case requires a pre-execution amendment, new preregistration SHA, and gate re-run;
any added case must also pass the Section 11 check.
