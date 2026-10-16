# ENVIRONMENT — EP-AGENT-001

**Version:** v0.3.5-DRAFT (2026-10-16). Version history: HISTORICAL / SUPERSEDED (end of file) and `CHANGELOG.md`.

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

Items marked *TO PIN AT FREEZE* must be filled in before the preregistration
SHA-256 lock.

| Item | Specification |
|---|---|
| Target OS | Linux (Ubuntu 22.04 LTS or later) or macOS 14+ |
| CPU | x86_64 or arm64 (exact model recorded in results) |
| GPU | Not required |
| Python | 3.11.x (locks generated/verified on CPython 3.11.6; exact patch recorded per run) |
| Package manager | pip, one venv per framework, installs from `requirements.lock` |
| Lockfile | `requirements.lock` (index) + `locks/<fw>.lock` — exact pins with sha256 artifact hashes; verified in clean venvs 2026-10-15 (`scripts/setup/generate_and_verify_locks.sh`). SHA-256s in `MANIFEST.sha256` |
| OpenAI Agents SDK | `openai-agents==0.24.0` |
| LangGraph | `langgraph==1.2.15` |
| CrewAI | `crewai==1.15.28` |
| Microsoft Agent Framework | `agent-framework==1.22.0` |
| ExecutionProof | **PINNED (v0.3.3; checklist item 7 PASS)** — ExecutionProof Controlled Reference Verifier, tag `v0.1.2-reference`, commit `b03365d57880e896c35e72898f8335a1826afe74`, API `0.1.2-reference`, ProofRecord schema 2, verifier `MANIFEST.sha256` `e53564589c4baeaca7bb1e26277c79abcb3f9e012b2f17fb26be19005e11eb69`. Runnable / Reference / Production: YES / YES / NO. Adoption as system under test via PREREGISTRATION §18 amendment (DRAFT, NOT FILED). See `EXECUTIONPROOF_PIN.md`. |
| Study evidence registry hash | `fixtures/evidence/study_evidence_registry.json` sha256 `b4a84f293182cd299b9168f3d38f3fc8f00e56c6bc89bcfa74a6385a490747d0` (schema `ep-evidence-registry/1`, version 1, 2 `VERIFIED` records) |
| Adapter commit | The packet commit labelled FINAL PRE-FILING CANDIDATE LOCK (v0.3) — real adapters in `adapters/*/adapter.py` + `binding.py` |
| Fixture policy configuration hash | `fixtures/policy/fixture_policy_config.json` sha256 `06b5a7ab68696d4d246f7b07f698437ec5713fa1da1113f553a02e04777649d4` (shared rules identical across B1–B5; per-fixture `evidence_records` stay in fixtures but are not read by the pinned verifier — run-time evidence status comes only from the study evidence registry, v0.3.3) |
| Test fixture hashes | Recorded in `MANIFEST.sha256` (unchanged since v0.2) |
| Expected-results hash | `EXPECTED_RESULTS.json` sha256 `af7ea17a34568dd42d01111dd5628ab71003da0b3656e2ee465efb6e016872d9` |
| Harness self-test baseline | Python 3.11.6 on Linux (design environment, 2026-10-15); framework packages not installed in the harness environment |
| Engineering compatibility check | 2026-10-15: each pinned framework (and google-adk 2.12.0, an eligible future extension NOT included in v1) installed in an isolated venv outside the packet and its integration symbols imported — see `ENGINEERING_COMPATIBILITY_CHECK.md`. NOT an experimental run; no fixture consumed |

## Environment variables (non-secret only)

| Variable | Example | Purpose |
|---|---|---|
| `EP_BASE_URL` | *(no default — must be supplied)* | ExecutionProof base URL; adapters refuse without it |
| `EP_VERIFY_PATH` | `/verify` (matches pinned verifier `POST /verify`) | Verify path appended to `EP_BASE_URL` |
| `EP_POLICY_CONFIG` | absolute path to `fixtures/policy/fixture_policy_config.json` | Verifier-side; study policy, fail-closed |
| `EP_EVIDENCE_REGISTRY` | absolute path to `fixtures/evidence/study_evidence_registry.json` | Verifier-side; study evidence registry, fail-closed |
| `EP_TENANT_ID` | `ep-agent-001-test` | Tenant scope written into contracts |
| `EP_AGENT_001_OUTPUT_DIR` | `results/` | Output location (authorized runs only) |
| `EP_AGENT_001_SEED` | `20261015` (frozen v0.3) | Framework-order randomization and bootstrap seed |

No secrets in environment variables, code, fixtures, or logs. If a framework requires a model API key to
initialize, a deterministic stub model is used instead where possible; if a real key is unavoidable it is a
sandbox key with no production access, supplied at runtime, never committed, and its use is approved by Derek
Hone in advance.

## Hard constraints

- No production credentials.
- No live customer systems.
- Mock / sandbox / local downstream effects only (`mock-external-endpoint`, `mock-account-001`).
- No real payments, no real external submissions, no production APIs.
- Cloud ExecutionProof endpoints require Derek Hone's approval before use.

## Verification at run time

`scripts/setup/check_versions.py` must report PASS for every framework in its venv; output is preserved with
the run record.

## HISTORICAL / SUPERSEDED

*Retained in chronological order (Rule 11). None of this is current status.*

- v0.2 (2026-10-15): document version v0.2-DRAFT.
- v0.3 (2026-10-15): ExecutionProof row — **BLOCKED — DEREK CONFIRMATION REQUIRED** (implementation repo/commit/path
  not accessible; see `EXECUTIONPROOF_PIN.md`). `EP_VERIFY_PATH` — `/verify` (packet default; pending Derek confirmation).
- v0.3.3 (2026-10-16): ExecutionProof pinned at `v0.1.2-reference` @ `b03365d5`; checklist item 7 PASS.
- v0.3.4 (2026-10-16): ExecutionProof row synced to the v0.3.3 pin (superseded values kept inline).
