# CHANGELOG — EP-AGENT-001

All entries are append-only. Prior entries are never edited (Rule 11).

## v0.1-DRAFT — 2026-10-15

- Initial design packet built. **DESIGN ONLY. Not preregistered.** Not executed. No results.
- Added: README, PREREGISTRATION (v0.1-DRAFT, not filed, no SHA lock), STUDY_PROTOCOL, UNIVERSITY_NON_INTERFERENCE,
  PRIOR_WORK_DISCLOSURE, CLAIM_BOUNDARY, FRAMEWORK_SELECTION, REQUEST_CONTRACT, TEST_MATRIX, EXPECTED_RESULTS.json,
  ANALYSIS_PLAN, PASS_FAIL_RULES, ENVIRONMENT, COST_ESTIMATE, LIMITATIONS, UNIVERSITY_EXPOSURE_LOG.
- Added: four adapter stubs (openai_agents, langgraph, crewai, maf), each labelled NOT AUTHORIZED FOR STUDY EXECUTION.
- Added: five benign fixtures B1–B5.
- Added: setup, validation, and harness self-test scripts; `run_study.py` stub that refuses to run.
- Added: results/ and proofrecords/ placeholders (no data).
- Generated: pre-freeze `MANIFEST.sha256` (working hashes; not a preregistration lock).
- Framework selection: OpenAI Agents SDK 0.24.0, LangGraph 1.2.15, CrewAI 1.15.28, Microsoft Agent Framework 1.22.0.
  Google ADK 2.12.0 deferred (native A2A; UW P2 lane risk).
- Non-interference basis: Master University Non-Interference + Prior-Work Audit (2026-10-15), verdict GO WITH BOUNDARY.

## v0.2-DRAFT — 2026-10-15 (pre-filing corrections; DESIGN ONLY; not filed; not executed; no results)

- Fixtures rescoped to exactly one condition vs B1: **B2** now omits only `current_state_reference` (required by a
  new, identical-in-all-fixtures `contract_completeness_requirement`); evidence verified. **B4** renamed
  `HOLD_EVIDENCE_ABSENT`: `evidence_references = []`, no evidence record (previously a `pending` record). Added
  `single_condition_vs_B1` to all fixtures; `validate_fixtures.py` now enforces one-condition / identical-policy /
  single-action / no-out-of-scope-terms checks.
- Gate wording: DESIGN-SCOPE VERDICT GO WITH BOUNDARY; CURRENT EXECUTION ELIGIBILITY NOT YET ELIGIBLE; NEW-RESEARCH
  GATE PENDING Q8 + Q9. Status line: PREREGISTRATION DRAFT COMPLETE — HOLD FOR Q9 RECONCILIATION.
- Lock definition: final file hashes + MANIFEST.sha256 + git commit hash + timestamp + preregistration record. No
  digital signature (never preregistered). "Signed" wording removed. Current hashes = PRE-FILING CANDIDATE LOCK.
- Explicit v1 scope rule: one agent → one proposed action → ExecutionProof → simulated downstream boundary;
  single-agent parallel tool calls excluded; shared/inherited/propagated authority added to UW P2 exclusions;
  "propagation" of verdicts renamed "return" where it could be confused with authority propagation.
- Explicit statement: no UD/UW student, team, or faculty member has any EP-AGENT-001 role.
- Framework sources verified (PyPI, GitHub, docs). Release-date corrections: MAF 1.22.0 → 2026-10-15 (was
  2026-10-08); CrewAI 1.15.28 → 2026-10-14 (was "(current)"). Versions unchanged.
- Google ADK 2.12.0 reclassified from "deferred" to **eligible candidate** (strict single-agent, single-tool
  configuration possible without A2A or transfer). Inclusion in the v1 matrix is pending Derek Hone's decision; the
  v0.1 deferral entry above is superseded, not edited.
- `UNIVERSITY_EXPOSURE_LOG.md` rewritten with an EP-AGENT-001-specific determination; unreconciled items marked
  UNKNOWN — TO RECONCILE.
- Added `ENGINEERING_COMPATIBILITY_CHECK.md` (install/import check; not an experimental run; no fixture consumed).
- MANIFEST regenerated (PRE-FILING CANDIDATE LOCK).

## v0.3-DRAFT — 2026-10-15 — FINAL PRE-FILING CANDIDATE LOCK (not filed; not executed; no results)

- **Decision recorded (Derek Hone): KEEP v1 AT FOUR FRAMEWORKS.** `openai-agents==0.24.0`, `langgraph==1.2.15`,
  `crewai==1.15.28`, `agent-framework==1.22.0`. Google ADK = ELIGIBLE FUTURE EXTENSION / NOT INCLUDED IN v1 / NO
  CHANGE TO 20-CELL MATRIX. Updated FRAMEWORK_SELECTION, PREREGISTRATION §10, LIMITATIONS, README,
  ENGINEERING_COMPATIBILITY_CHECK, ENVIRONMENT, PASS_FAIL_RULES (stale "ADK not eligible while UW P2 active" line).
- Added `requirements.lock` + `locks/<fw>.lock` (exact pins, sha256 artifact hashes, clean-venv verified) and
  `scripts/setup/generate_and_verify_locks.sh`; `install_all.sh` now installs hash-locked only.
- Added `fixtures/policy/fixture_policy_config.json` and `EXECUTIONPROOF_PIN.md` (item 7 BLOCKED — DEREK CONFIRMATION REQUIRED).
- Replaced adapter stubs: `adapters/ep_client.py` (transport only, no default endpoint), `verify()`/`handle_native()`
  per adapter, `binding.py` per framework. Harness T7 redefined: verify() refuses without an explicit endpoint.
- Added SMOKE-000 + `scripts/smoke/run_smoke.py` + `ENGINEERING_SMOKE_LOG.md` (ENGINEERING SMOKE ONLY — NOT EVIDENCE).
- Added `scripts/analysis/analyze.py` + `selftest_synthetic.py` (SYNTHETIC — NOT EVIDENCE); seed 20261015 frozen.
- PASS_FAIL_RULES v0.3: Step-0 cell labelling, established-PARTIAL precedence, explicit anti-rescue rules.
- `run_study.py` rewritten as a gated runner that refuses (filing record, Q8 formal/Q9 gate record, Derek token,
  manifest) — and refuses unconditionally in v0.3.
- UNIVERSITY_EXPOSURE_LOG §5a: Q9 records reconciliation (Q9 OPEN; two Derek confirmations).


## v0.3.1-DRAFT — 2026-10-16 (Q9 closure; DESIGN ONLY; not filed; not executed; no results)

- UNIVERSITY_EXPOSURE_LOG §5b appended: Q9 **PASSED** on the written-record Gmail search (355 messages, 46 attachments)
  plus Derek Hone's verbatim written confirmation. Status line updated (superseded line retained).
- PREREGISTRATION header: Q9 PASSED; new-research gate pending Q8 only. Checklist item 13 → PASS; item 12 stays OPEN (Q8).
- UNIVERSITY_NON_INTERFERENCE §2: v0.3.1 Q9 update note.
- EXECUTIONPROOF_PIN: v0.3.1 private-implementation hunt appended — **still BLOCKED** (no private repo visible to
  GitHub App; no runnable v2.1 server found). Checklist item 7 unchanged (BLOCKED).
- No change to scope (4 frameworks, 20 cells, B1–B5, one agent, one tool call), fixtures, expected results,
  hypotheses, Request Contract, adapters, or university exclusions. No university contacted.

## v0.3.2-DRAFT — 2026-10-16 (reference-verifier candidate pin; DESIGN ONLY; not filed; not executed; no results)

- EXECUTIONPROOF_PIN: appended "Derek Hone ground truth (2026-10-15)" (verbatim statement; note that it does not
  mean no prior implementation ever existed) and "Candidate pin — ExecutionProof Controlled Reference Verifier for
  EP-AGENT-001": tag `v0.1.1-reference`, commit `279bcb2669e4602ae25e0d745d827a1c8514265e`, API `0.1.1-reference`,
  15-field contract accepted directly, `EP_POLICY_CONFIG` fail-closed, study policy SHA `06b5a7ab…77649d4`,
  config and lock hashes, required reference-implementation disclosure (verbatim). Status: BUILT — CHECKLIST ITEM
  7 REMAINS OPEN pending Derek decision on evidence-reference status mechanism (options a/b/c).
- Load-only startup check of the verifier with the study policy (`GET /health` only): policy SHA `06b5a7ab…`
  reported. No `/verify` call, no study fixture, no ProofRecord, no result.
- PREREGISTRATION: added §18 "PENDING AMENDMENT — DRAFT, NOT FILED" (verbatim reference-implementation statement;
  narrowed claim ceiling). Checklist item 7 → "OPEN — reference verifier built and pinned candidate;
  evidence-status mechanism decision pending" (not PASS). No other PREREGISTRATION text changed.
- No change to scope, fixtures B1–B5, expected results, hypotheses, Request Contract, adapters, policy config, or
  university exclusions. Nothing filed.

## v0.3.3-DRAFT — 2026-10-16 (final reference-verifier pin; evidence registry; DESIGN ONLY; not filed; not executed; no results)

- Derek Hone decision on the evidence-reference status mechanism: **option (a)** — separate, hashed, fail-closed
  evidence registry file.
- Added `fixtures/evidence/study_evidence_registry.json` (schema `ep-evidence-registry/1`, id
  `EP-AGENT-001-STUDY-EVIDENCE-REGISTRY`, version 1, 2 `VERIFIED` records; SHA-256 `b4a84f29…490747d0`). Built by
  static inspection of B1–B5 `evidence_references` only; B4 intentionally has no record. No fixture submitted to `/verify`.
- EXECUTIONPROOF_PIN: appended "Final candidate pin — v0.1.2-reference": tag `v0.1.2-reference`, commit
  `b03365d57880e896c35e72898f8335a1826afe74`, `EP_EVIDENCE_REGISTRY` fail-closed, ProofRecord schema 2, verifier
  manifest `e5356458…11eb69`, 150 dev tests, load-only `/health` check (policy + registry hashes; 0 ProofRecords;
  no `/verify`). Earlier sections retained unedited.
- PREREGISTRATION: version line v0.3.3-DRAFT; "System under integration" → pinned reference verifier; Q8 technical
  freeze readiness → PASS (superseded value retained inline); checklist item 7 → **PASS**; item 12 text updated
  (still OPEN — Q8 formal awaits Derek approval + filing); §18 pending amendment now names `v0.1.2-reference` and
  both artifact hashes (still DRAFT, NOT FILED).
- PREREGISTRATION status line → "HOLD FOR DEREK APPROVAL + FILING" (stale "HOLD FOR Q9 RECONCILIATION" retained inline as superseded; Q9 PASSED in v0.3.1).
- Study policy `fixture_policy_config.json` unchanged (`06b5a7ab…77649d4`). No change to scope, fixtures B1–B5,
  expected results, hypotheses, Request Contract, adapters, or university exclusions. Nothing filed. Not executed.


## v0.3.4-DRAFT — 2026-10-16 (status-line sync; DESIGN ONLY; not filed; not executed; no results)

- Stale status lines brought in line with v0.3.1 (Q9 PASSED) and v0.3.3 (item 7 PASS; reference verifier pinned at
  `v0.1.2-reference` @ `b03365d5`). Every superseded value is kept inline and labelled "superseded".
- README: packet version; status block → "HOLD FOR DEREK APPROVAL + FILING", gate → "PENDING Q8 FORMAL", added pin
  line; §3 gate line; pinned-implementation note (`/verify`, `/proof/{id}`, `/health`; policy/registry loaded via
  `EP_POLICY_CONFIG` / `EP_EVIDENCE_REGISTRY`); artifact map adds `EXECUTIONPROOF_PIN.md`, study policy, and evidence
  registry; PREREGISTRATION and UNIVERSITY_EXPOSURE_LOG rows updated.
- ENVIRONMENT: ExecutionProof row BLOCKED → PINNED (item 7 PASS); evidence-registry hash row; `EP_VERIFY_PATH` note;
  `EP_POLICY_CONFIG` / `EP_EVIDENCE_REGISTRY` rows (verifier-side); policy row clarifies fixture `evidence_records`
  are not read by the pinned verifier.
- UNIVERSITY_NON_INTERFERENCE: study status line; v0.3.3 gate block appended below the v0.2 block (retained);
  §6 Q8 row → technical readiness PASS (v0.3.3); Q9 row → PASSED (v0.3.1); gate result → PENDING Q8 FORMAL.
- PREREGISTRATION: §3 gate line → PENDING Q8 formal; §18 note no longer says the header records item 7 as blocked;
  version-row note. No other text changed.
- LIMITATIONS item 1 and CLAIM_BOUNDARY: pointer to the pinned reference verifier and the §18 pending narrowing
  (DRAFT, NOT FILED — not operative). Claim text, qualifiers, and prohibited claims unchanged.
- UNIVERSITY_EXPOSURE_LOG unchanged (append-only; its top status line already records Q9 PASSED).
- No change to scope, fixtures B1–B5, expected results, hypotheses, Request Contract, adapters, policy, evidence
  registry, protocol steps, or university exclusions. Nothing filed. Not executed.

## v0.3.5-DRAFT — 2026-10-16 (format cleanup only; DESIGN ONLY; not filed; not executed; no results)

- PREREGISTRATION, UNIVERSITY_NON_INTERFERENCE, EXECUTIONPROOF_PIN, ENVIRONMENT now open with the current operative
  status block (design COMPLETE; EP pin PASS; Q9 PASSED; Q8 technical PASS; Q8 formal OPEN — requires Derek approval
  + filing; not filed; not executed; no results; execution not authorized).
- Superseded status lines/blocks moved below the current status into sections labelled HISTORICAL / SUPERSEDED,
  in chronological order. No historical information deleted. EXECUTIONPROOF_PIN: current `v0.1.2-reference` pin
  now first; the earlier BLOCKED / hunt / ground-truth / `v0.1.1-reference` sections follow unedited under history.
- No scientific content changed (RQ, hypotheses, endpoints, expected outcomes, classification rules, frameworks,
  B1–B5, exclusions, university boundaries, claim ceiling). Pin, policy and registry hashes unchanged.
