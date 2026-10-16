# CLAIM BOUNDARY — EP-AGENT-001

**Version:** v0.3.4-DRAFT (2026-10-16; pending-narrowing pointer added) — superseded: v0.1-DRAFT (2026-10-15) — Status: DESIGN ONLY. No results exist; no claim below is currently made.

Principle: **claims remain narrower than evidence.**

**Pending narrowing (v0.3.3 pointer; not yet operative):** if the PREREGISTRATION §18 amendment (DRAFT, NOT FILED) is
approved and filed, the §1 claim refers only to the `/verify` decision path of the pinned ExecutionProof Controlled
Reference Verifier (`v0.1.2-reference` @ `b03365d57880e896c35e72898f8335a1826afe74`, with the study policy and
evidence registry hashes in `EXECUTIONPROOF_PIN.md`) and must carry the reference-implementation disclosure. It may
not be broadened to any other ExecutionProof build, deployment, or version. The text below is otherwise unchanged.

---

## 1. Maximum allowed successful claim (verbatim; usable only if the classification is PASS)

> "In an RF-run internal study, the ExecutionProof `/verify` decision path was integrated with four selected agent
> frameworks (OpenAI Agents SDK 0.24.0, LangGraph 1.2.15, CrewAI 1.15.28, Microsoft Agent Framework 1.22.0)
> through thin single-agent adapters using one frozen Request Contract. Across five benign, policy-driven
> fixtures, all 20 framework × case cells returned the preregistered ALLOW / HOLD / DENY verdict with ProofRecord
> linkage, without modification of the ExecutionProof core decision engine."

For PARTIAL, the claim must name exactly which frameworks met which endpoints and which did not. For FAIL, the
failure is reported first and in full. For INCONCLUSIVE, the invalidation condition is named and no portability
claim is made.

## 2. Required qualifiers (every external or internal summary must carry all of these)

1. "RF-run internal study" — never "independent", "third-party", or "external".
2. The exact framework versions tested; no generalization to other versions.
3. "Single-agent tool-call path only"; delegation/handoff features not used.
4. "Five benign, policy-driven fixtures"; "not an adversarial evaluation".
5. "Local/sandbox ExecutionProof instance with mock downstream targets"; not production.
6. Latency figures labelled "RF internal measurement" with host spec.
7. The non-interference statement: "It makes no claim about adversarial robustness, multi-agent authorization, or independent reproducibility, which are the subject of independent university projects."

## 3. Prohibited claims

| # | Prohibited claim or wording | Reason |
|---|---|---|
| 1 | "ExecutionProof works with any / all agent frameworks" | Only four pinned versions tested |
| 2 | "Framework-agnostic" or "universally portable" without the tested-version qualifier | Overgeneralization |
| 3 | "Secure", "attack-resistant", "tamper-proof", "bypass-proof", or "robust" on the basis of this study | No adversarial testing (UD / UW P1) |
| 4 | "Prevents replay", "prevents mutation", "no false-ALLOW" on the basis of this study | Reserved; not tested |
| 5 | Any claim about multi-agent, delegated, or agent-to-agent authorization | Reserved (UW P2); not tested |
| 6 | "Independently validated", "independently reproduced", "reproduced by", "externally verified" | Reserved (UW P4); RF-run |
| 7 | "Conformant", "RF-100 conformant", "certified", "compliant" | Reserved (UW P4); RF cannot self-certify |
| 8 | Calling any university "a validator" or implying university endorsement | Rule 7 |
| 9 | "Production-ready" or "enterprise-proven" on the basis of this study | Sandbox only |
| 10 | "Zero overhead", "negligible latency", or latency comparisons as general performance claims | Internal, host-specific measurement |
| 11 | "Novel" / "first" without a cited literature review supporting it | Novelty not established by this study |
| 12 | Framing results as answering, pre-empting, or anticipating UD or UW findings | Rules 3–4 |
| 13 | Any claim before preregistration SHA lock and authorized execution | No results exist |
| 14 | Re-describing a FAIL or PARTIAL as PASS after remediation | Rule 11; FAIL and fix are two facts |

## 4. Scientific vs. commercial separation rule

1. The scientific record (preregistration, results, classification) is written first and stands alone.
2. The commercial question ("Can an implementation partner retain its preferred agent framework while
   ExecutionProof remains an independent pre-execution verification boundary?") is answered, if at all, in a
   separate document that cites the scientific record and inherits every qualifier in §2.
3. Commercial material may not upgrade the classification, drop qualifiers, or round PARTIAL up to PASS.
4. "Independent" in the CQ refers to architectural separation of the verification boundary from the agent
   framework — never to independent validation. Commercial copy must make that distinction explicit.
5. No result is published or archived (including to Zenodo) without Derek Hone's separate publication authorization.
