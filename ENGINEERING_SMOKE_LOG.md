# ENGINEERING SMOKE LOG — SMOKE-000 ONLY

**ENGINEERING SMOKE ONLY — NOT EVIDENCE — OUTSIDE THE STUDY DENOMINATOR. No B1–B5 fixture was run. No study
endpoint was contacted. No verdict (ALLOW/HOLD/DENY) was produced: the local mock returns the non-study token
`SMOKE_ACK`.**

- Date: 2026-10-15 (EDT). Host: Linux x86_64, CPython 3.11.6. Venvs: isolated framework venvs outside the packet.
- Fixture: `fixtures/smoke/SMOKE-000.json` (`ENGINEERING_SMOKE_PING` → `smoke-mock-target`; not semantically
  equivalent to B1–B5: different action type, actor, target, parameters; no policy evaluated).
- Model: deterministic stub per framework (no LLM, no API key). Endpoint: in-process mock on 127.0.0.1.
- Runner: `scripts/smoke/run_smoke.py --framework <fw>` (refuses any fixture other than SMOKE-000; verified).

| Framework | Imports | Tool invoked exactly once | Contract schema-valid | framework_id correct | Mock reached once | Return object came back | Smoke |
|---|---|---|---|---|---|---|---|
| openai-agents 0.24.0 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | PASS |
| langgraph 1.2.15 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | PASS |
| crewai 1.15.28 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | PASS |
| agent-framework 1.22.0 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | PASS |

Configuration asserted in-run: OpenAI `handoffs == []`, one tool, `parallel_tool_calls is False`; CrewAI one agent,
one task, `allow_delegation is False`; LangGraph START→single tool node→END; MAF one `af.tool` + one
`FunctionMiddleware` on that tool path. Not verified here: behaviour against a real ExecutionProof build (item 7
blocked), real-LLM tool selection, latency. CrewAI run with `CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true`.
