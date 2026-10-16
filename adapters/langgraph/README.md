# EP-AGENT-001 Adapter — LangGraph

**STATUS: STUB — DESIGN ONLY — NOT AUTHORIZED FOR STUDY EXECUTION**

| Item | Value |
|---|---|
| Package | `langgraph` |
| Pinned version | 1.2.15 |
| `framework_id` | `langgraph` |
| Adapter class | `EPVerifiedToolNode` (`adapter.py`) |
| Normalizer | `normalizer.py` → `normalize_to_request_contract(...)` |
| Native argument source | `tool_call["args"]` on the routed AIMessage |
| Integration point | Tool executed by a `ToolNode` in a single-agent graph; verdict + ProofRecord ref written to ToolMessage / state. |
| Excluded native features | Multi-agent subgraphs, supervisor patterns, `Send` fan-out to other agents (UW P2) |

## Behaviour of this stub

- `normalize_to_request_contract` is implemented and emits all 15 Request Contract fields (see `REQUEST_CONTRACT.md`).
- `verify(...)` and the framework binding method raise `NotImplementedError` with the authorization message.
- The framework package is **not imported**; no network calls are made; `EP_VERIFY_ENDPOINT` is a localhost mock placeholder.
- No credentials, no production endpoints.

## Scope rules (binding)

1. Single-agent tool-call path only: one agent → one proposed action → `/verify` → simulated downstream boundary. Exactly one tool call per run; no single-agent parallel tool calls; no agent-to-agent calls, shared/inherited authority, or multi-agent chains.
2. Benign, well-formed fixture inputs only (B1–B5).
3. No bypass path, no replay, no mutation, no delegation, no ProofRecord manipulation — these are UNIVERSITY-RESERVED.
4. The adapter never decides ALLOW / HOLD / DENY locally; only `/verify` decides.
5. The mock action body runs only after an ALLOW verdict; verdict and `proof_record_id` are returned unchanged in the single agent's tool result.

Replacing this stub with a live implementation is freeze checklist item 8 and requires review for scope before the
preregistration SHA lock. Running it on the study corpus requires Derek Hone's explicit execution authorization.
