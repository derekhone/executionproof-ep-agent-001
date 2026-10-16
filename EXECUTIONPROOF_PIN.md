# EXECUTIONPROOF PIN — EP-AGENT-001 (checklist item 7)

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

## Current pin — v0.1.2-reference (Derek Hone decision: option (a), 2026-10-16)

**Status: PINNED — CHECKLIST ITEM 7 PASS (technical pin).** This section supersedes the `v0.1.1-reference`
candidate pin for EP-AGENT-001; earlier sections are retained unedited, in chronological order, under HISTORICAL / SUPERSEDED below. Derek Hone chose option
(a): a separate, hashed, fail-closed evidence registry file. Study policy SHA-256 is unchanged.

| Field | Value |
|---|---|
| Implementation name | ExecutionProof Controlled Reference Verifier |
| Repository (local, no remote) | `/home/ubuntu/executionproof-reference-verifier` |
| Branch | `main` |
| Tag | `v0.1.2-reference` (annotated). Earlier tags retained: `v0.1.1-reference` → `279bcb2669e4602ae25e0d745d827a1c8514265e`, `v0.1.0-reference` → `a578823eb686424d5fa39786fbe594d297a2dde6` |
| Commit | `b03365d57880e896c35e72898f8335a1826afe74` |
| API / implementation version | `0.1.2-reference` |
| Verify | `POST /verify` → as v0.1.1 plus `evidence_registry_hash` |
| Proof | `GET /proof/{id}` |
| Health | `GET /health` → `status`, `implementation_version`, `git_commit`, `policy_hash`, `evidence_registry_hash`, `evidence_registry_id`, `evidence_registry_version`, `proofrecord_schema_version` |
| 15-field EP-AGENT-001 contract accepted directly | YES (unchanged) |
| Policy loading | `EP_POLICY_CONFIG` (absolute path), fail-closed (exit 1). A policy containing `rules.evidence_records` is now **rejected** (fail-closed) |
| Evidence loading | `EP_EVIDENCE_REGISTRY` (absolute path), fail-closed (exit 3) if missing, unreadable, relative, malformed, wrong schema, duplicate reference/id, or invalid status |
| Evidence resolution rule | A reference counts only on an exact string match to a registry record whose `status` is exactly `VERIFIED`. Unknown reference → HOLD with `EVIDENCE_REFERENCE_UNKNOWN`. Reference strings are never parsed or inferred from |
| Study policy path / SHA-256 | `/home/ubuntu/EP-AGENT-001/fixtures/policy/fixture_policy_config.json` — `06b5a7ab68696d4d246f7b07f698437ec5713fa1da1113f553a02e04777649d4` (unchanged) |
| Study evidence registry path / SHA-256 | `/home/ubuntu/EP-AGENT-001/fixtures/evidence/study_evidence_registry.json` — `b4a84f293182cd299b9168f3d38f3fc8f00e56c6bc89bcfa74a6385a490747d0` |
| Study registry identity | schema `ep-evidence-registry/1`, id `EP-AGENT-001-STUDY-EVIDENCE-REGISTRY`, version `1`, 2 records (`EP-AGENT-001-EVR-001`, `EP-AGENT-001-EVR-002`, both `VERIFIED`) |
| ProofRecord schema | version 2 (19 columns; adds evidence registry hash, id, version, and schema version). Store refuses schema-1 databases; a fresh DB file is required |
| Implementation config hashes | `requirements.txt` `583da51cb298743be1d697178aa38a2b00fbd1473dd28f1fb5444e266d050eb3`; `pytest.ini` `8fa307d1ef787f3822b949dc90f1b3c405769c4eb97bb2e813b271109d9d8a90`; `.gitignore` `d6235bec62a32ab242c2f52a835bc50f2da3ff5202b4a6f06c88e9a4241b7184` (all unchanged) |
| Development-only artifacts (not used for the study) | `tests/fixtures/dev_policy.json` `d7a6256d0ed14d1b31bfc92847d70eca4449a8eee1e36b1679ca8c791bc9b0f4` (changed: `evidence_records` removed); `tests/fixtures/dev_evidence_registry.json` `bbf199b7853de91c69fbe367bd4d7bff9515083dd09317b783a9102ad0e2a048` (new) |
| Verifier `MANIFEST.sha256` SHA-256 | `e53564589c4baeaca7bb1e26277c79abcb3f9e012b2f17fb26be19005e11eb69` (36 entries; `sha256sum -c` OK) |
| Dependency lock SHA-256 | `requirements.lock` `1e4a988c867df880a23e1586d6d5e3f9340b447dd232a6ee2f9ba903a5de8702` (unchanged since v0.1.0-reference) |
| Development test suite | 150 passed, 1 warning (DEV-REF inputs only; not EP-AGENT-001 evidence) |
| Load-only startup check | 2026-10-16T02:13:12Z, clean tagged commit, `EP_POLICY_CONFIG` = study policy, `EP_EVIDENCE_REGISTRY` = study registry, throwaway DB; only `GET /health` called → `implementation_version` `0.1.2-reference`, `git_commit` `b03365d5…`, `policy_hash` `06b5a7ab…77649d4`, `evidence_registry_hash` `b4a84f29…490747d0`, `proofrecord_schema_version` `2`; server stopped; 0 ProofRecords; 0 POST requests; throwaway DB deleted; no study fixture used |
| Runnable / Reference / Production | YES / YES / NO |

**How the study registry was built (static inspection only).** The `contract.evidence_references` of B1–B5 were
read from the JSON files: B1, B2, B5 → `evidence://verified/test-actor-authorized/identity-check-001`; B3 →
`evidence://verified/test-actor-unauthorized/identity-check-001`; B4 → `[]` (intentionally no registry record).
Each of those fixtures' `fixture_policy_context.evidence_records` lists the same reference with status `verified`
(lowercase); the registry records it in the verifier's canonical status vocabulary as `VERIFIED`. The verifier does
not read `fixture_policy_context`; at run time evidence status comes only from the hashed registry. No fixture was
submitted to `/verify`; no expected verdict was used to choose registry content beyond these transcribed statuses.

**Boundary.** The registry provides deterministic benign evidence status only. It does not model freshness,
revocation, provenance, replay resistance, tampering, or authenticity (out of scope; university-reserved lanes untouched).

**Required disclosure (verbatim, unchanged):**

> "The ExecutionProof implementation used in EP-AGENT-001 is a controlled reference implementation built and frozen before preregistration filing and before experimental execution. EP-AGENT-001 therefore evaluates cross-framework integration portability against this pinned reference implementation, not against an existing production deployment."

---

## HISTORICAL / SUPERSEDED

*Retained unedited in chronological order (Rule 11). Nothing in this section is current status. Superseded by the Current pin above.*

**Historical status (v0.3, superseded): BLOCKED — DEREK CONFIRMATION REQUIRED.** No implementation commit has been invented.

### What could be pinned (verified 2026-10-15)

| Item | Value | Source |
|---|---|---|
| B1–B5 policy config | `fixtures/policy/fixture_policy_config.json` | extracted canonically (sorted JSON) from the shared `fixture_policy_context` of B1–B5; identical across all five |
| Policy config SHA-256 | `06b5a7ab68696d4d246f7b07f698437ec5713fa1da1113f553a02e04777649d4` | `sha256sum` |
| Public contract reference (reference only) | `github.com/derekhone/executionproof`, branch `main`, HEAD `886b5c4b69ce4bc3793d51a075e0b986372ce61b` (2026-08-21); tag `v1.0.0-public` → `3aa3b15a955ebd23d9414fa9a111a8c5b550c502` | shallow clone |
| Public OpenAPI | `docs/openapi.yaml`, `info.version` 2.0.0 (OpenAPI 3.0.3), sha256 `1d65ca5a172df4367ab216ff02e0375ba71733062381dd444febd566fdd66651` | file in public repo |

### What could NOT be pinned — and why

The public repository contains specifications, docs and examples only — **no runnable verifier implementation**.
The controlled implementation is private and not accessible from this environment. Discrepancies to resolve:

| Packet assumption | Public OpenAPI 2.0.0 |
|---|---|
| API family "v2.1" | `info.version: 2.0.0` |
| `POST {EP_BASE_URL}/verify` | `POST /v2/boundaries/{boundaryId}/verify` |
| `GET /proof/{id}` | `GET /v2/proofrecords/{proofId}` |
| 15-field Request Contract body | `VerifyRequest {action, principal, evidence, requestedAt}` |
| Policy load via `/policies/*` | not present in public OpenAPI |

### Derek must supply (one line each)

1. ExecutionProof implementation repo + branch/tag + full commit SHA to run against.
2. API version and exact verify / proof-resolution paths (adapters accept `EP_BASE_URL` + `EP_VERIFY_PATH`; default `/verify`).
3. Whether that build accepts the frozen 15-field Request Contract as-is (if it requires a mapping layer, that layer is a pre-filing amendment, never an in-run change).
4. Configuration files used by that build, and how `fixture_policy_config.json` is loaded (their SHA-256s get recorded here).


### v0.3.1 private-implementation hunt (2026-10-16) — STILL BLOCKED

Read-only search; no endpoint called with any B1–B5 fixture; nothing invented.

| Source | Result |
|---|---|
| Local filesystem (`/home/ubuntu` incl. hidden/config dirs, cloned repos, `.aws`, `.config`) | No `/verify` or ProofRecord-retrieval server; no `policies/authority`, `policies/constraints`, `policies/evidence-verifiers`, `policies/rails`, `evidence-schemas`, `v2.1`, uvicorn/gunicorn service, or ExecutionProof Dockerfile/docker-compose; no `EP_BASE_URL`/ExecutionProof host in env |
| GitHub (Abacus GitHub App) | `GET /user/repos?visibility=private` → **0 repos**. App sees 18 public repos only. Private repos are **not visible**, which is not evidence that they do not exist |
| Hosting clues | `builderexecutionproof.io` (Abacus-hosted web app): HTTP 200 site, but `/api/verify`, `/api/v2/verify`, `/verify`, `/api/health`, `/api/proofrecords`, `/openapi.json` → 404; site states ProofRecords use "a lightweight deterministic fingerprint for local testing" → demo, not the controlled build. `executionproof.io/v2/proofrecords/x` → 404; `api.executionproof.io/health` → 404 |
| Gmail (deploy/host/GitHub notifications) | No ExecutionProof API host, deployment, build ID, or private-repo notification found |
| Abacus projects | Only "Execution Boundary Weekly Production" AI_AGENT projects (content cadence), not a verifier |

Excluded as backend (§6 of the hunt instruction): ARK-498 server, experiment-local gateways, EP-PQC harnesses,
vaultproof-agent-guard, public OpenAPI spec alone.

**Smallest Derek action:** state where the runnable ExecutionProof v2.1 build lives: either (a) grant the Abacus GitHub
App access to that private repo and give its owner/name, or (b) state that no runnable v2.1 build exists yet.


### Derek Hone ground truth (2026-10-15)

Derek Hone's statement, verbatim:

> "I, Derek Hone, confirm that I do not know of an existing runnable private ExecutionProof v2.1 verifier implementation that can currently be identified and pinned for EP-AGENT-001."

Note: this statement records that no runnable private v2.1 verifier can currently be identified and pinned. It
does **not** mean that no prior ExecutionProof implementation ever existed.

### Candidate pin — ExecutionProof Controlled Reference Verifier for EP-AGENT-001

**Status: BUILT — CHECKLIST ITEM 7 REMAINS OPEN pending Derek decision on evidence-reference status mechanism (options a/b/c)**

| Field | Value |
|---|---|
| Implementation name | ExecutionProof Controlled Reference Verifier |
| Repository (local, no remote) | `/home/ubuntu/executionproof-reference-verifier` |
| Branch | `main` |
| Tag | `v0.1.1-reference` (earlier tag `v0.1.0-reference` → `a578823eb686424d5fa39786fbe594d297a2dde6` retained) |
| Commit | `279bcb2669e4602ae25e0d745d827a1c8514265e` |
| API version | `0.1.1-reference` |
| Verify | `POST /verify` → `verdict`, `proof_id`, `proof_record_id` (= `proof_id`), `timestamp` (ISO 8601 UTC = ProofRecord `created_at`), `proof_url`, `execution_authorized`, `reason_codes`, `implementation_version`, `policy_hash` |
| Proof | `GET /proof/{id}` |
| Health | `GET /health` → `status`, `implementation_version`, `git_commit`, `policy_hash` |
| 15-field EP-AGENT-001 contract accepted directly | YES |
| Policy loading mechanism | `EP_POLICY_CONFIG` env var (absolute path); fail-closed — process refuses to start (exit 1) if the file is missing, unreadable, relative, or invalid |
| Study policy expected path | `/home/ubuntu/EP-AGENT-001/fixtures/policy/fixture_policy_config.json` (not copied into the verifier repo) |
| Study policy SHA-256 | `06b5a7ab68696d4d246f7b07f698437ec5713fa1da1113f553a02e04777649d4` |
| Implementation config hashes | `requirements.txt` `583da51cb298743be1d697178aa38a2b00fbd1473dd28f1fb5444e266d050eb3`; `pytest.ini` `8fa307d1ef787f3822b949dc90f1b3c405769c4eb97bb2e813b271109d9d8a90`; `.gitignore` `d6235bec62a32ab242c2f52a835bc50f2da3ff5202b4a6f06c88e9a4241b7184`; development-only policy `tests/fixtures/dev_policy.json` `423ba050de874785d5c4920a78b029784995e1f9705cc97b5a0390f57bab84c5` (not used for the study) |
| Verifier `MANIFEST.sha256` SHA-256 | `09a78d7d31ce219f19cdc90c4180e8416c4dc98d302ed6b8694779bd6912323f` (32 entries) |
| Dependency lock SHA-256 | `requirements.lock` `1e4a988c867df880a23e1586d6d5e3f9340b447dd232a6ee2f9ba903a5de8702` (unchanged from v0.1.0-reference; Python 3.11.6, fastapi 0.143.2, pydantic 2.14.1, uvicorn 0.54.0) |
| Development test suite | 111 passed, 1 warning (DEV-REF inputs only; not EP-AGENT-001 evidence) |
| Load-only startup check | Server started at the tagged commit with `EP_POLICY_CONFIG` = study policy path; only `GET /health` called → `policy_hash` `06b5a7ab…77649d4`, `implementation_version` `0.1.1-reference`, `git_commit` `279bcb26…` (clean); server stopped; 0 ProofRecords; no `/verify` call; no study fixture used |
| Runnable | YES |
| Reference implementation | YES |
| Production implementation | NO |

**Open item blocking item 7 — evidence-reference status mechanism.** The study policy contains no
`evidence_records`, and neither the 15-field contract nor the policy defines how the verifier learns the status of
an evidence reference. With the study policy loaded as-is, evidence-required requests resolve HOLD (fail closed);
this is stated from the verifier code and was not tested with study fixtures. Derek Hone decision required:
(a) separate hashed evidence registry via a new env var (e.g. `EP_EVIDENCE_REGISTRY`) — new verifier commit/tag,
policy SHA unchanged; (b) move `evidence_records` into the study policy — policy SHA changes, packet amendment;
(c) another mechanism. Nothing has been implemented. See the verifier's `POLICY_CONFIG.md` §4.

**Required disclosure (verbatim):**

> "The ExecutionProof implementation used in EP-AGENT-001 is a controlled reference implementation built and frozen before preregistration filing and before experimental execution. EP-AGENT-001 therefore evaluates cross-framework integration portability against this pinned reference implementation, not against an existing production deployment."
