# PREREGISTRATION — EP-AGENT-001

## Cross-Framework ExecutionProof Portability and Integration Study

| Field | Value |
|---|---|
| Study ID | EP-AGENT-001 |
| Version | v0.3.5-DRAFT — FINAL PRE-FILING CANDIDATE LOCK (2026-10-16). Version history: see HISTORICAL / SUPERSEDED below and `CHANGELOG.md` |
| Date | 2026-10-15 |
| Owner / PI | Derek Hone, Remnant Fieldworks Inc. |
| System under integration | ExecutionProof Controlled Reference Verifier, tag `v0.1.2-reference`, commit `b03365d57880e896c35e72898f8335a1826afe74`, `POST /verify` (see `EXECUTIONPROOF_PIN.md`, final candidate pin; adoption via §18 amendment at filing) |
| Study type | Deterministic integration / portability study (RF internal) |

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

DESIGN-SCOPE VERDICT:          GO WITH BOUNDARY
CURRENT EXECUTION ELIGIBILITY: NOT YET ELIGIBLE (pending Q8 formal)
```

**Lock definition (no other lock element exists).** The preregistration lock consists of exactly: (1) the final
SHA-256 hash of every manifest-tracked file, (2) `MANIFEST.sha256` and its own SHA-256, (3) the git commit hash
containing them, (4) the UTC timestamp of that commit, and (5) the preregistration filing record. No digital
signature, signing key, or cryptographic sign-off is part of the lock; none was preregistered.

The hashes currently in `MANIFEST.sha256` are a **FINAL PRE-FILING CANDIDATE LOCK** (not a final preregistration lock). They become the final lock only
after Derek Hone approves the packet in writing and the preregistration is filed. Until then they do not
constitute a preregistration lock.

### HISTORICAL / SUPERSEDED status lines

*Retained in chronological order (Rule 11). None of these is current status; the block above is operative.*

| Version | Superseded status line |
|---|---|
| v0.2 | PREREGISTRATION DRAFT COMPLETE — HOLD FOR Q9 RECONCILIATION; NEW-RESEARCH GATE: PENDING Q8 + Q9 |
| v0.3 | Q8 TECHNICAL FREEZE READINESS: FAIL (checklist item 7 BLOCKED) |
| v0.3.1 | Q9 PASSED; NEW-RESEARCH GATE: PENDING Q8 (item 7 still BLOCKED) |
| v0.3.2 | Candidate pin `v0.1.1-reference` @ `279bcb2669e4602ae25e0d745d827a1c8514265e`; item 7 OPEN |
| v0.3.3 | Final pin `v0.1.2-reference`; item 7 PASS; Q8 technical PASS; status HOLD FOR DEREK APPROVAL + FILING |
| v0.3.4 | Status-line sync across packet documents (superseded values kept inline) |

---

## 1. Primary research question (frozen)

> **RQ:** Can selected AI-agent frameworks integrate with the same ExecutionProof Request Contract and
> verification boundary while preserving the same core ALLOW / HOLD / DENY semantics and ProofRecord linkage
> without modification of the ExecutionProof core decision engine?

## 2. Commercial question (separate — not a scientific endpoint)

> **CQ:** Can an implementation partner retain its preferred agent framework while ExecutionProof remains an
> independent pre-execution verification boundary?

The CQ is recorded for business context only. No endpoint, threshold, or classification in this preregistration
answers the CQ. Scientific results must be reported before, and separately from, any commercial interpretation
(see `CLAIM_BOUNDARY.md` §4).

## 3. Mandatory non-interference language

> "EP-AGENT-001 measures integration portability of the ExecutionProof decision path across selected agent
> frameworks under benign, policy-driven fixtures. It makes no claim about adversarial robustness, multi-agent
> authorization, or independent reproducibility, which are the subject of independent university projects."

> "University Non-Interference Boundary: This study is intentionally limited to framework portability, request
> normalization, verification-interface integration, decision propagation, ProofRecord linkage, and engineering
> integration characteristics. It does not test or resolve active University of Dayton or University of
> Washington adversarial, multi-agent authorization, or independent reproducibility research questions."

Source: Master University Non-Interference + Prior-Work Audit (2026-10-15), Section I — **DESIGN-SCOPE VERDICT:
GO WITH BOUNDARY**. This is a design-scope verdict only. Current execution eligibility: **NOT YET ELIGIBLE**
(new-research gate pending Q8 formal; Q9 PASSED; Q8 technical freeze readiness PASS; see
`UNIVERSITY_NON_INTERFERENCE.md` §6).

**No university role.** No University of Dayton or University of Washington student, team, or faculty member has
any role in EP-AGENT-001 — not consultant, co-investigator, participant, reviewer, or executor. No EP-AGENT-001
fixtures, expected outcomes, answer keys, or results are shared with any university team while its reserved
project is active.

**Interaction pattern (v1, fixed).** One agent → one proposed consequential action → ExecutionProof `/verify` →
simulated downstream boundary. Exactly one tool call per run; single-agent parallel tool calls are excluded.

## 4. System under integration (fixed)

```
Request Contract
→ Authority Engine
→ Evidence Engine
→ Constraint Engine
→ Control Engine
→ ProofRecord™
→ Execution Gateway
```

Core invariants assumed by the expected outcomes (they are the reference semantics, not hypotheses about
robustness):

1. incomplete contract → HOLD
2. Authority FAIL → DENY
3. Authority PASS + Evidence FAIL → HOLD
4. Authority PASS + Constraint FAIL → HOLD
5. all required checks PASS → ALLOW
6. HOLD/DENY may not cross the controlled execution boundary
7. no cached permission assumption
8. current state evaluated at time of request
9. decision provenance preserved

Interfaces used: `/verify` (decision), `/proof/{id}` (ProofRecord retrieval). Policy endpoints
(`/policies/authority`, `/policies/constraints`, `/policies/evidence-verifiers`, `/evidence-schemas`,
`/policies/rails`) are used only to load the fixed fixture policy before execution.

## 5. Hypotheses

| ID | Hypothesis | Failure condition (any one falsifies) |
|---|---|---|
| **H1 — Integration** | Each of the four frameworks can submit the frozen Request Contract to `/verify` through a thin adapter, for all five benign cases, without modification of ExecutionProof core code. | Any framework cannot complete integration for ≥1 case without (a) modifying ExecutionProof core code, or (b) altering the semantics of a frozen Request Contract field. |
| **H2 — Decision fidelity** | For every framework × case cell, the verdict observed by the adapter equals the frozen expected verdict in `EXPECTED_RESULTS.json`. | Any cell where observed verdict ≠ expected verdict (exact string match; no tolerance). |
| **H3 — Core semantic invariance** | For each benign case, the verdicts returned for the four frameworks are identical, and the four normalized contracts are semantically identical on all canonical fields (all fields except `request_id`, `framework_id`, `nonce`, `requested_at`). | Any case where ≥1 framework's verdict differs from the others, or where canonical-field values or `action_hash` differ between frameworks. |
| **H4 — ProofRecord linkage & verdict return** | For every cell, `/verify` returns a ProofRecord reference that resolves via `/proof/{id}`, and the adapter returns both the verdict and the reference, unchanged, into the framework-native tool result of the same single agent. | Any cell where the reference is absent, does not resolve, or is not present unchanged in the framework-native result; or where the verdict string is altered on return. |

H4 is a benign verdict-return and linkage measurement within one agent's single tool call. "Verdict return"
never means authority propagation between agents (UW P2-reserved). It is **not** a test of ProofRecord integrity under
tamper/forgery (UD-reserved) and **not** a containment-resistance test.

## 6. Primary endpoints

Notation: F = {openai_agents, langgraph, crewai, maf} (|F| = 4); C = {B1, B2, B3, B4, B5} (|C| = 5);
cell (f, c); I(·) = indicator (1 if true, else 0); v(f,c) = observed verdict; e(c) = expected verdict.

| ID | Endpoint | Exact formula | PASS threshold |
|---|---|---|---|
| **P1** | Integration completion rate | P1 = Σ_f Σ_c I(integration_complete(f,c)) / 20 | 20/20 (= 1.0) |
| **P2** | Decision fidelity | P2 = Σ_f Σ_c I(v(f,c) = e(c)) / 20 | 1.0 (100%) |
| **P3** | Core semantic invariance (per case) | P3_c = \|{f ∈ F : v(f,c) = v_mode(c)}\| / 4, where v_mode(c) is the most frequent verdict for case c (ties → P3_c = 0.5 or lower as computed) | P3_c = 1.0 for every c ∈ C |
| **P4** | ProofRecord linkage | P4 = Σ_f Σ_c I(proof_ref(f,c) returned ∧ resolves via /proof/{id} ∧ present in framework-native result) / 20 | 20/20 |
| **P5** | Core modification required | P5 = boolean: was any change to ExecutionProof core code, core configuration semantics, or decision logic required for any framework? | false |

`integration_complete(f,c)` = the adapter (i) normalized the fixture into a contract that passes the frozen
schema, (ii) submitted it to `/verify` from inside the framework's native single-agent tool-call path, (iii)
received a well-formed decision response, and (iv) returned that decision to the framework runtime — all without
manual intervention during the run.

## 7. Secondary endpoints (engineering metrics — descriptive only)

| ID | Metric | Measurement method |
|---|---|---|
| S1 | Adapter LOC | Non-blank, non-comment, non-docstring Python lines in `adapters/<f>/adapter.py` + `normalizer.py`, counted by a frozen counting script at freeze; framework-specific lines reported separately from shared logic |
| S2 | Setup burden | Number of documented install/config steps; wall-clock time from clean venv to first successful `/verify` call (time-to-first-verify) |
| S3 | Dependency burden | Count of packages added to the clean lockfile by installing the framework; installed size (MB) of the framework's site-packages delta |
| S4 | Latency — normalization | Time inside `normalize_to_request_contract` (ns resolution, `time.perf_counter_ns`) |
| S5 | Latency — adapter round trip | Time from adapter entry (tool invocation received) to verdict returned to framework, including `/verify` round trip; median and p95 per cell; labelled **RF internal measurement** |
| S6 | Integration friction | Count and description of workarounds, framework-specific code paths, and deviations; qualitative log per framework |
| S7 | Configuration surface | Number of framework-specific configuration keys/objects required by the adapter |

Secondary endpoints never alter the PASS / PARTIAL / FAIL / INCONCLUSIVE classification.

## 8. Benign test matrix

All cases use the single action archetype `SUBMIT_EXTERNAL_ACTION` against a mock target. Each case is applied
identically to all four frameworks (20 cells). Full detail in `TEST_MATRIX.md`.

| Case | Name | Description | Fixture | Expected | Rationale (core invariant) | University-interference check |
|---|---|---|---|---|---|---|
| B1 | ALLOW_COMPLETE | Complete contract; authorized actor; verified evidence present; amount 50 ≤ limit 100 | `fixtures/benign/B1_allow_complete.json` | **ALLOW** | All required checks PASS → ALLOW | PASS — well-formed, benign, no attack vector |
| B2 | HOLD_INCOMPLETE_CONTRACT | Exactly one required benign field absent: `current_state_reference` is omitted, while the fixture policy (`contract_completeness_requirement`) requires it for `SUBMIT_EXTERNAL_ACTION`. Everything else identical to B1 (evidence verified, authorized actor, amount 50). After normalization the field is `null`; `null` under a policy that requires the field = incomplete → HOLD | `fixtures/benign/B2_hold_incomplete_contract.json` | **HOLD** | Incomplete contract → HOLD | PASS — schema-valid, benign omission; not malformed, not adversarial |
| B3 | DENY_NO_AUTHORITY | `actor_id = test-actor-unauthorized` has no authority grant for `SUBMIT_EXTERNAL_ACTION` in the static fixture policy | `fixtures/benign/B3_deny_no_authority.json` | **DENY** | Authority FAIL → DENY | PASS — static "role not granted" policy condition; no revocation, no forgery, no stale authority |
| B4 | HOLD_EVIDENCE_ABSENT | Required benign evidence simply absent: `evidence_references = []` and no evidence record, while the policy requires ≥1 verified reference. Everything else identical to B1 (contract complete incl. `current_state_reference`) | `fixtures/benign/B4_hold_evidence_absent.json` | **HOLD** | Authority PASS + Evidence FAIL → HOLD | PASS — evidence simply absent; no forged, stale, replayed, malformed, manipulated, or adversarial evidence |
| B5 | HOLD_CONSTRAINT_EXCEEDED | `parameters.amount = 101`; fixture policy constraint `amount <= 100` | `fixtures/benign/B5_hold_constraint_exceeded.json` | **HOLD** | Authority PASS + Constraint FAIL → HOLD | PASS — ordinary policy limit; not a parameter mutation or post-verification drift |

## 9. Classification rules (summary — full text in `PASS_FAIL_RULES.md`)

| Class | Exact condition |
|---|---|
| **PASS** | P1 = 20/20 ∧ P2 = 1.0 ∧ P3_c = 1.0 ∀c ∧ P4 = 20/20 ∧ P5 = false |
| **PARTIAL** | Not PASS and not FAIL, and ≥1 framework achieves 5/5 complete, faithful, linked cells with no core modification, while ≥1 framework fails ≥1 cell or requires a material workaround (a framework-specific change outside the adapter, or a documented deviation affecting the contract path) |
| **FAIL** | P5 = true; or ≥2 frameworks cannot use the same frozen contract without changing core semantics; or no framework achieves 5/5 complete, faithful, linked cells |
| **INCONCLUSIVE** | Only the preregistered invalidation conditions: upstream framework defect, environment failure, dependency outage, corrupted artifacts, incomplete execution caused by non-study infrastructure. Never used to rescue a negative result. |

Precedence: FAIL is evaluated first, then INCONCLUSIVE (only if an invalidation condition is documented and the
negative outcome is attributable to it), then PASS, then PARTIAL.

## 10. Frameworks (exact versions; pinned at freeze)

| Framework | Package | Version | License | Integration point (single-agent only) |
|---|---|---|---|---|
| OpenAI Agents SDK | `openai-agents` | 0.24.0 | MIT | Function tool wrapping the verify call; handoffs excluded |
| LangGraph | `langgraph` | 1.2.15 | MIT | Tool executed via `ToolNode`; single-agent graph only |
| CrewAI | `crewai` | 1.15.28 | MIT | `BaseTool` subclass on a single agent, single task; delegation disabled |
| Microsoft Agent Framework | `agent-framework` | 1.22.0 | MIT | `FunctionMiddleware` around function tools (`call_next` only on ALLOW) |

Versions, release dates, licenses, and sources were verified against PyPI, GitHub releases, and official docs on
2026-10-15 (`FRAMEWORK_SELECTION.md` §2a). Framework-native multi-agent features (handoffs, crew delegation,
multi-agent graphs, sub-agents, A2A) are **excluded** and must be disabled or unused. **Single-agent parallel tool
calls are also excluded in v1**: each run makes exactly one tool call (e.g. `parallel_tool_calls=False` where the
framework exposes it). Google ADK 2.12.0 is **not excluded**: it can be configured strictly single-agent,
single-tool without A2A or transfer (`FRAMEWORK_SELECTION.md` §4). Decision recorded 2026-10-15 (Derek Hone): **KEEP v1 AT FOUR FRAMEWORKS — ADK is NOT added to v1.** ADK status:
ELIGIBLE FUTURE EXTENSION / NOT INCLUDED IN v1 / NO CHANGE TO 20-CELL MATRIX. v1 = `openai-agents==0.24.0`,
`langgraph==1.2.15`, `crewai==1.15.28`, `agent-framework==1.22.0`.

## 11. Environment (summary — full text in `ENVIRONMENT.md`)

Linux (Ubuntu 22.04 LTS+) or macOS 14+; x86_64 or arm64; Python 3.11.x; pip with `requirements.lock`;
ExecutionProof local/sandbox instance pinned by version/commit at freeze; no production credentials, no live
customer systems, mock downstream targets only; no secrets in environment variables.

## 12. Analysis plan (summary — full text in `ANALYSIS_PLAN.md`)

Deterministic, descriptive reporting. Binary endpoints as exact counts and percentages. Decision fidelity is exact
agreement with no tolerance. Latency: 5 warmup calls discarded, then 30 measured calls per case per framework;
report median and p95; optional bootstrap 95% CI for the median (1,000 resamples, seed frozen at freeze). Raw
values are reported alongside every summary. No inferential statistics are manufactured for trivial technical
variability.

## 13. Claim ceiling

> **Maximum allowed successful claim:** "In an RF-run internal study, the ExecutionProof `/verify` decision path
> was integrated with four selected agent frameworks (OpenAI Agents SDK 0.24.0, LangGraph 1.2.15, CrewAI 1.15.28,
> Microsoft Agent Framework 1.22.0) through thin single-agent adapters using one frozen Request Contract. Across
> five benign, policy-driven fixtures, all 20 framework × case cells returned the preregistered ALLOW / HOLD /
> DENY verdict with ProofRecord linkage, without modification of the ExecutionProof core decision engine."

Required qualifiers and prohibited claims: `CLAIM_BOUNDARY.md`. Claims remain narrower than evidence.

## 14. Exclusions (UNIVERSITY-RESERVED — not implemented, not executed)

| Excluded item | Reserved for |
|---|---|
| Agent-to-agent delegation / handoff | UW P2 |
| Multi-agent authority / multi-hop delegation | UW P2 |
| Collusion / confused deputy | UW P2 |
| Shared authority, inherited permissions, authority propagation between agents | UW P2 |
| Parallel agents / multi-agent chains / orchestration | UW P2 |
| Single-agent parallel tool calls (excluded from v1 to keep one agent → one action) | v1 scope rule |
| Bypassing the adapter / direct unauthorized tool invocation | UD / UW P1 |
| Replay through adapters | UD / UW P1 |
| Mutation through adapters (incl. post-verification action drift) | UD / UW P1 |
| Adversarial malformed input | UD / UW P1 |
| ProofRecord tamper / forgery | UD |
| Forged, stale, reused, or revoked evidence/authority | UD / UW P1 |
| False-ALLOW hunting / containment-resistance testing | UD / UW P1 |
| Independent reproduction claims | UW P4 |
| External conformance claims | UW P4 |

## 15. Prior-work disclosure (summary — full text in `PRIOR_WORK_DISCLOSURE.md`)

RF has prior, RF-run, implementation-specific work on the EP boundary, including the ARK corpus (ARK-493–498,
10.5281/zenodo.21462612; P01 series ARK-458–482), the intent-binding series IB-001–003
(10.5281/zenodo.22002829; IB-001/002 FAIL preserved, IB-003 PASS), authority partitioning AUTH-001/002
(10.5281/zenodo.22002833), and `PRODUCTION-STATUS.md` (executionproof v1.0.0-public). EP-AGENT-001 is
intentionally separated from all of it: it imports no adversarial case tables, reuses no ARK/EP-SEC cases, and
answers a different question (integration portability).

## 16. Preregistration freeze checklist

All 14 items must be checked, with evidence, before the SHA-256 lock is computed and before any execution
authorization can be requested.

| # | Item | Status |
|---|---|---|
| 1 | Primary RQ, CQ separation, and hypotheses H1–H4 reviewed and frozen | ✔ PASS — consistency audit v0.3: RQ/CQ/H1–H4 unchanged |
| 2 | Primary endpoints P1–P5 formulas and thresholds frozen | ✔ PASS — P1–P5 formulas/thresholds identical across PREREGISTRATION, ANALYSIS_PLAN, PASS_FAIL_RULES |
| 3 | Fixtures B1–B5 frozen; SHA-256 of each fixture recorded | ✔ PASS — B1–B5 hashes in MANIFEST (unchanged since v0.2) |
| 4 | `EXPECTED_RESULTS.json` frozen; SHA-256 recorded | ✔ PASS — sha256 af7ea17a…72d9; verdicts match fixtures |
| 5 | Request Contract schema (`REQUEST_CONTRACT.md`) frozen; normalization rules per framework frozen | ✔ PASS — 20/20 normalized contracts schema-valid |
| 6 | Framework versions pinned in `requirements.lock`; lockfile SHA-256 recorded | ✔ PASS — requirements.lock + locks/<fw>.lock verified in clean venvs |
| 7 | ExecutionProof version/commit pinned; fixture policy configuration hash recorded | ✔ PASS — v0.3.3: `v0.1.2-reference` @ `b03365d5…`; policy `06b5a7ab…77649d4` (unchanged); evidence registry `b4a84f29…490747d0` (Derek Hone option a); load-only `/health` check only |
| 8 | Adapter code implemented (stubs replaced), reviewed for scope (no delegation, no bypass/replay/mutation paths), commit pinned | ✔ PASS — real adapters + bindings; single-agent/single-tool asserted in smoke |
| 9 | Dry-run on a non-study smoke fixture completed (harness only; not B1–B5) and logged as a dry-run, not a result | ✔ PASS — SMOKE-000 engineering smoke 4/4 (ENGINEERING_SMOKE_LOG.md) |
| 10 | Analysis scripts, LOC counting rule, latency protocol, and bootstrap seed frozen | ✔ PASS — analyze.py + synthetic self-test 14/14; seed 20261015 |
| 11 | PASS / PARTIAL / FAIL / INCONCLUSIVE rules and invalidation conditions frozen | ✔ PASS — PASS_FAIL_RULES v0.3 precedence/anti-rescue |
| 12 | 10-question university non-interference gate re-run and recorded (design-scope verdict GO or GO WITH BOUNDARY **and** Q8, Q9 PASSED) | ☐ OPEN — Q9 PASSED (v0.3.1); Q8 technical readiness PASS (v0.3.3); Q8 formal not PASSED (awaiting Derek approval + filing) |
| 13 | `UNIVERSITY_EXPOSURE_LOG.md` reconciled (historical UD entries resolved; UW assignments checked) | ✔ PASS — v0.3.1: Gmail record search (355 msgs, 46 attachments) + Derek Hone written confirmation (§5b) |
| 14 | `MANIFEST.sha256` regenerated and verified (`sha256sum -c`); git commit hash and UTC timestamp recorded; Derek Hone's written approval of the packet recorded; preregistration filing record created (no digital signature is part of the lock) | ☐ OPEN |

## 17. Authorization

Execution requires, in order: (1) completion of the freeze checklist, (2) a SHA-locked preregistration,
(3) a passing new-research gate (Q8 and Q9 PASSED), and (4) Derek Hone's explicit written execution authorization (template in
`EP-AGENT-001_DESIGN_SUMMARY.md`, Section Z). None of these has occurred.

## 18. PENDING AMENDMENT — DRAFT, NOT FILED

This amendment is a draft. It has not been approved by Derek Hone and has not been filed. Until it is approved and
filed, the sections above remain the operative draft text. (The header status lines were updated in v0.3.3 and now
record item 7 PASS and Q8 technical freeze readiness PASS; superseded v0.3.2 wording: "the header status lines,
which still record item 7 as blocked".)

**ExecutionProof under test (verbatim):**

> "ExecutionProof under test is a controlled reference implementation built by Remnant Fieldworks before preregistration filing and before experimental execution. The implementation was frozen by repository commit and configuration hashes before the EP-AGENT-001 experimental matrix was run. The study therefore evaluates portability across selected agent frameworks against this reference implementation and does not establish performance of a separately deployed production ExecutionProof system."

Candidate pin: ExecutionProof Controlled Reference Verifier, tag `v0.1.2-reference`, commit
`b03365d57880e896c35e72898f8335a1826afe74`, loaded with study policy `fixtures/policy/fixture_policy_config.json`
(SHA-256 `06b5a7ab68696d4d246f7b07f698437ec5713fa1da1113f553a02e04777649d4`) via `EP_POLICY_CONFIG` and study
evidence registry `fixtures/evidence/study_evidence_registry.json` (SHA-256
`b4a84f293182cd299b9168f3d38f3fc8f00e56c6bc89bcfa74a6385a490747d0`) via `EP_EVIDENCE_REGISTRY` (details and hashes
in `EXECUTIONPROOF_PIN.md`). Evidence-reference status mechanism: Derek Hone option (a), separate hashed
fail-closed registry. Checklist item 7: PASS (v0.3.3). Superseded v0.3.2 text: candidate `v0.1.1-reference` @
`279bcb2669e4602ae25e0d745d827a1c8514265e`, item 7 OPEN.

**Narrowed claim ceiling (applies if this amendment is adopted):** the §13 maximum claim refers only to the
`/verify` decision path of the pinned ExecutionProof Controlled Reference Verifier (tag `v0.1.2-reference`, commit
`b03365d57880e896c35e72898f8335a1826afe74`, with the study policy and study evidence registry hashes above) and establishes portability
against that pinned reference implementation only; it may not be broadened to any other ExecutionProof build,
deployment, or version.

---

*SHA-256 of this document: final value recorded at filing. Current value in `MANIFEST.sha256` = PRE-FILING CANDIDATE LOCK.*
