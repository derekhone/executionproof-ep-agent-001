# UNIVERSITY EXPOSURE LOG — EP-AGENT-001 and related ExecutionProof artifacts

**Version:** v0.2-DRAFT (2026-10-15). Append-only from this version onward (Rule 11).
**Purpose:** Rule 13 of the Master University Non-Interference Audit (2026-10-15). Records every artifact shown to
any university team, so that gate question Q9 can be answered with evidence.

**Q9 status: PASSED (v0.3.1, 2026-10-16) — see §5b.** *(Superseded line kept below per Rule 11.)*

~~Q9 status: OPEN — university exposure log not yet reconciled.~~

**Fabrication rule.** Nothing in this log is reconstructed from memory or inference and presented as a record.
Anything not confirmed from a record reviewed for this log is written **UNKNOWN — TO RECONCILE**. Logical
inferences are labelled as inferences and do not close a row.

---

## 1. What Q9 asks for EP-AGENT-001

> **Q9:** Would EP-AGENT-001 execution, or any EP-AGENT-001 student-facing material, interfere with an active
> university project? (Checked against this exposure log.)

Two different kinds of exposure must not be conflated:

| Kind | Governed by | Effect on Q9 for EP-AGENT-001 |
|---|---|---|
| **A. EP-AGENT-001-specific exposure**: the EP-AGENT-001 packet, framework-portability cases, cross-framework metrics, fixtures B1–B5, or EP-AGENT-001 expected outcomes shown to a university team | This log, §3 | Directly determines Q9 |
| **B. Older ARK / P01 / EP-SEC exposure**: whether UD students were shown ARK-493–498 / P01 case-level tables at kickoff or walkthrough | Master Audit (Section D/F/J, open risk #1) | Does **not** automatically fail Q9. It affects UD's student-independence rating, which the Master Audit governs. It matters to EP-AGENT-001 only if it shows overlap with EP-AGENT-001 content |

## 2. No university role in EP-AGENT-001

No University of Dayton or University of Washington student, team, or faculty member has any EP-AGENT-001 role:
not consultant, co-investigator, participant, reviewer, or executor. No EP-AGENT-001 fixtures, expected outcomes,
answer keys, or results are to be shared with any university team while its reserved project is active. Any
future sharing must be logged in §5 before it occurs.

## 3. EP-AGENT-001-specific exposure determination

EP-AGENT-001 was created on **2026-10-15** (packet commit history begins that day). The UD project (CPS 474/574
Team A, Fall 2026) began before that date. UW teams have not been assigned (UW DocuSign unsigned as of this log).

| Content item | UD — kickoff deck / brief / walkthrough (pre-2026-10-15) | UD — follow-up communications | UW P1 | UW P2 | UW P4 |
|---|---|---|---|---|---|
| EP-AGENT-001 packet (any file) | **Not possible if the material predates 2026-10-15** (inference from creation date). Material dates: UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE (no record reviewed); no sharing recorded in RF records available to this audit | No team assigned; nothing recorded | No team assigned; nothing recorded | No team assigned; nothing recorded |
| Framework-portability cases | UNKNOWN — TO RECONCILE (generic framework-integration discussion could exist independently of EP-AGENT-001; contents not reviewed) | UNKNOWN — TO RECONCILE | No team assigned; nothing recorded | No team assigned; nothing recorded | No team assigned; nothing recorded |
| Cross-framework metrics (LOC, setup/dependency burden, adapter latency, friction) | UNKNOWN — TO RECONCILE (contents not reviewed) | UNKNOWN — TO RECONCILE | No team assigned; nothing recorded | No team assigned; nothing recorded | No team assigned; nothing recorded |
| Fixtures B1–B5 (as defined in v0.1/v0.2) | **Not possible if the material predates 2026-10-15** (inference). Material dates: UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | No team assigned; nothing recorded | No team assigned; nothing recorded | No team assigned; nothing recorded |
| EP-AGENT-001 expected outcomes (`EXPECTED_RESULTS.json`) | **Not possible if the material predates 2026-10-15** (inference). Material dates: UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | No team assigned; nothing recorded | No team assigned; nothing recorded | No team assigned; nothing recorded |

"Nothing recorded" means no exposure appears in RF records available to this audit. It is not a confirmed
negative from the university side.

**Current determination:** No EP-AGENT-001-specific exposure is recorded. That cannot yet be confirmed because the
UD kickoff deck, brief, walkthrough, and follow-up communications have not been reviewed, and their dates are not
recorded here. → **Q9 OPEN.**

## 4. Historical entries (TO RECONCILE — do not invent)

| date | university | project | recipient_or_team | artifact_shown | artifact_version_or_hash | repo_or_link | detail_level | headline_only | case_level_outcomes_included | expected_outcomes_included | shared_by | purpose | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UNKNOWN — TO RECONCILE | University of Dayton | UD ExecutionProof Adversarial Boundary Challenge (CPS 474/574 Team A) | UNKNOWN — TO RECONCILE | Brief (`UD_AdversarialBoundaryChallenge_Brief.docx`), kickoff deck (`ExecutionProof_Adversarial_Boundary_Challenge_-_UD_Kickoff_6e7fdf08.pptx`), GitHub/architecture walkthrough, follow-up comms (contents not reviewed for this log) | UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | UNKNOWN — TO RECONCILE | Kind B (ARK/P01) risk governed by Master Audit. Kind A (EP-AGENT-001) inferred impossible for pre-2026-10-15 material; dates unconfirmed |
| UNKNOWN — TO RECONCILE | University of Washington | UW P1 | Team not yet assigned | None recorded | — | — | — | — | — | — | — | — | UW DocuSign unsigned; pitch forum Nov 12/13 2026 |
| UNKNOWN — TO RECONCILE | University of Washington | UW P2 | Team not yet assigned | None recorded | — | — | — | — | — | — | — | — | As above |
| UNKNOWN — TO RECONCILE | University of Washington | UW P4 | Team not yet assigned | None recorded | — | — | — | — | — | — | — | — | As above |

## 5. New entries (EP-AGENT-001 and later)

*(append below; one row per exposure; use the field definitions in §6)*

None recorded as of 2026-10-15.

### 5a. Q9 records reconciliation (2026-10-15, v0.3) — records only; every line cites its source

| Q | Determination | Source |
|---|---|---|
| A. EP-AGENT-001-specific material before 2026-10-15? | **NO packet material existed before 2026-10-15T23:38:54Z** (first commit). | `git log` of this packet: first commit `f32084b` 2026-10-15T23:38:54Z; v0.2 `4524b16` 23:59:09Z; no earlier commits |
| B. Any of it shared with UD? | **No sharing record found.** Packet has no git remote (never pushed); not present in any of Derek's 18 GitHub repos. | `git remote -v` → empty; GitHub repo list (18 repos, queried 2026-10-15) — none named/containing EP-AGENT-001 |
| C. Portability/metrics discussed with UD independently of EP-AGENT-001? | **UNDETERMINED — record not available.** UD brief, kickoff deck, meeting notes, follow-up email and walkthrough records are not in this environment. Only GitHub hit for "portability": `executionproof-testbeds/P01_COMPLETION_REPORT.md` lines 239/350 ("Cross-language portability (JavaScript and Python)", "Dual-Guard Portability") — P01 language portability, not agent-framework portability; whether it was shown to UD is itself unrecorded. | `/home/ubuntu/Uploads` (no UD records); Master Audit (`RF_University_NonInterference_Audit.md`) notes brief/deck/walkthrough unavailable; grep of `executionproof-testbeds` @ `3c415c5` |
| D. Any UW team assigned? | **None recorded** as of 2026-10-14 (UW plans P1/P2/P4; teams expected "in the next few weeks"; DocuSign unsigned; forum Nov 12/13 2026). | RF university-relationship records (status as of 2026-10-14) |
| E. Any UW-facing material referencing EP-AGENT-001? | **None recorded**; the packet was never pushed or shared. | Same as B |

**Q9 status: OPEN.** Smallest confirmation set (Derek, yes/no each):
1. The UD Team A kickoff / GitHub walkthrough / follow-ups did **not** present agent-framework portability, cross-framework metrics, or B1–B5-like fixtures.
2. As of filing, no UW team has been assigned material referencing EP-AGENT-001, and nothing EP-AGENT-001-related has been sent to UD or UW.

### 5b. Q9 closure (v0.3.1, 2026-10-16) — written-record search + Derek Hone confirmation

**Written-record search (2026-10-15, read-only Gmail API, derek@ownerremnantfieldworks.com).** 355 messages
matching `udayton.edu`, `uw.edu`, `Kaatz`, `"Pilot Brief"`, `"university projects"`, plus all Gemini meeting notes;
46 attachments on UD/UW threads text-extracted. Terms searched: `EP-AGENT`, `portab*`, `LangGraph`, `CrewAI`,
`AutoGen`, `Agents SDK`, `cross-framework`, `framework comparison`, `agent framework`, `B1–B5`, `tool call`,
`four frameworks`, `multi-framework`, `framework-agnostic`. Full record: `EP-AGENT-001_FINAL_BLOCKER_RESOLUTION.md` Part 2.

| Q9 sub-question | Determination | Source |
|---|---|---|
| A. UD Team A ever received/discussed cross-framework portability, framework-comparison metrics, B1–B5-like fixtures, or EP-AGENT-001 content? | **NO (records).** Kickoff email + 9 attachments incl. Project Brief and Kickoff Slide Deck (2026-09-21), Gemini kickoff notes (2026-09-21), example-hypotheses email (2026-10-07), "Repos, First Test Cases, and Ownership" email (2026-10-14), all other thread messages: zero hits; scope is adversarial boundary testing only | Gmail message IDs `1a0c505f71585cd6`, `1a0c4f0081e8050b`, `1a1176d5f24eeb31`, `1a13b5dabef54d03` |
| A-gap. Unrecorded 2026-10-14 UD Team A meeting and other unrecorded conversations | **Closed by Derek Hone confirmation** (below) | Derek Hone, written, 2026-10-16 |
| B. Any EP-AGENT-001 material sent to any UW team or assigned project? | **NO (records).** Four UW capstone proposals (P1–P4, 2026-09-03), Kaatz thread (2026-09-03 → 09-17), pitch notice (2026-10-14): no EP-AGENT-001 content; latest UD/UW outbound 2026-10-14 predates packet first commit `f32084b` (2026-10-15T23:38:54Z); packet has no git remote | Gmail; `git log`; `git remote -v` |
| C. Former §5a item C (portability/metrics discussed with UD independently of EP-AGENT-001) | **Resolved NO** by A above + Derek confirmation | As above |

Disclosed adjacencies (**not** exposure): the 2026-10-07 email listed "required evidence missing/incomplete" as a
generic adversarial direction (conceptual overlap with B2/B4 categories only; no fixtures, contract, or framework
content); UW P2 (multi-agent authorization) and P4 (independent conformance) are thematically near EP-AGENT-001's
explicit exclusions, which remain unchanged and university-reserved.

**Derek Hone confirmation (verbatim, given in writing 2026-10-16 UTC):**

> "I, Derek Hone, confirm that in the unrecorded October 14, 2026 UD Team A meeting and in every other unrecorded conversation with UD Team A or any UW team, I did not discuss cross-framework agent portability, framework comparison metrics, the EP-AGENT-001 B1–B5 fixtures, or any other EP-AGENT-001 content."

**Q9: PASSED.** No EP-AGENT-001-specific (Kind A) exposure exists, and no student-facing material is affected by
EP-AGENT-001. Kind B (older ARK/P01) remains governed by the Master Audit. No university was contacted for this
closure. Study scope and university-reserved exclusions are unchanged.

## 6. Field definitions

| Field | Type | Meaning |
|---|---|---|
| `date` | ISO date | Date the artifact was shown/shared |
| `university` | string | University of Dayton / University of Washington |
| `project` | string | UD Adversarial Boundary Challenge / UW P1 / UW P2 / UW P4 |
| `recipient_or_team` | string | Team or role (no personal student data beyond what is necessary) |
| `artifact_shown` | string | Name of slide deck, repo, document, walkthrough |
| `artifact_version_or_hash` | string | Version tag or SHA-256 |
| `repo_or_link` | string | Repo path or URL |
| `detail_level` | enum | `headline` / `summary` / `full` |
| `headline_only` | bool | Only headline results shown |
| `case_level_outcomes_included` | bool | Any per-case outcome table shown |
| `expected_outcomes_included` | bool | Any expected-outcome list shown |
| `shared_by` | string | RF person who shared it |
| `purpose` | string | Why it was shared |
| `notes` | string | Anything else relevant |

## 7. Steps to close Q9 (Derek Hone)

1. Record the dates of the UD brief, kickoff deck, and GitHub/architecture walkthrough, and confirm whether any
   follow-up communication after 2026-10-15 mentioned EP-AGENT-001, framework portability, cross-framework
   metrics, B1–B5, or expected outcomes.
2. Confirm in writing whether any of those materials contained framework-portability cases or cross-framework
   metrics (independent of EP-AGENT-001).
3. Confirm that no UW team has been assigned and no UW-facing material has referenced EP-AGENT-001.
4. Enter each confirmed fact in §4/§5 with its source (file name and date). Replace the matching
   UNKNOWN — TO RECONCILE cell only when a record supports it.
5. Re-run gate Q9. It passes only if no EP-AGENT-001-specific exposure exists that would interfere with an active
   project, and no student-facing material would be affected by EP-AGENT-001 execution.

The older ARK/P01 question (Kind B) stays tracked under the Master Audit. Its resolution is not a precondition for
Q9 unless it reveals EP-AGENT-001-relevant overlap.
