# LIMITATIONS — EP-AGENT-001

**Version:** v0.3.4-DRAFT (2026-10-16; item 1 pin pointer added) — superseded: v0.2-DRAFT (2026-10-15). These limitations bind every claim made from this study.

1. **Tested versions only.** Results (once they exist) apply only to the versions pinned at freeze:
   openai-agents 0.24.0, langgraph 1.2.15, crewai 1.15.28, agent-framework 1.22.0, and the pinned ExecutionProof
   version/commit. *(v0.3.3 pin: ExecutionProof Controlled Reference Verifier `v0.1.2-reference` @ `b03365d5` — a
   controlled reference implementation, not a production deployment; see `EXECUTIONPROOF_PIN.md` and the
   PREREGISTRATION §18 pending amendment, DRAFT, NOT FILED.)*
2. **Selected frameworks only.** Four of many frameworks. Google ADK is an eligible future extension that is
   NOT included in v1 (Derek Hone decision, 2026-10-15); it is untested, as are AutoGen, AG2, and all
   other frameworks. No generalization to "any framework".
3. **Benign fixtures only.** Five cases (B1–B5). This is not an adversarial evaluation and says nothing about
   behaviour under hostile, malformed, or manipulated input.
4. **Single action archetype.** Only `SUBMIT_EXTERNAL_ACTION` against a mock target.
5. **Local/sandbox execution.** Not production systems; mock downstream effects; latency is host-specific.
6. **Single-agent, single-action paths only.** One agent → one proposed action → `/verify` → simulated downstream
   boundary, one tool call per run. Delegation, handoffs, agent-to-agent calls, shared/inherited authority,
   multi-agent orchestration, and single-agent parallel tool calls are excluded.
7. **Deterministic tool invocation.** Tool arguments come from fixtures, not model reasoning; the study does not
   measure whether an LLM-driven agent chooses to call the tool or fills arguments correctly.
8. **RF-run study.** Not independent reproduction; RF authored the system, adapters, fixtures, and analysis.
9. **Does not address:** adversarial robustness, multi-agent authorization, external conformance, bypass
   resistance, replay resistance, mutation resistance, ProofRecord integrity under attack, false-ALLOW rates.
10. **Claim narrower than evidence.** The claim ceiling in `CLAIM_BOUNDARY.md` governs all reporting.
11. **Snapshot in time.** Framework behaviour at pinned versions may change in future releases; the stub
    integration points in `adapters/` are validated against real framework APIs only at freeze.
12. **Small case count.** Five cases exercise each core invariant once; they demonstrate path portability, not
    coverage of the policy space.
13. **Framework facts as of 2026-10-15.** Versions, release dates, and maintenance status come from design-time
    research and must be re-confirmed at freeze.
