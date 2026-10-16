#!/usr/bin/env python3
"""
EP-AGENT-001 ENGINEERING SMOKE (SMOKE-000 ONLY) — NOT EVIDENCE — OUTSIDE THE STUDY DENOMINATOR.

Run with the framework's own venv python:  <venv>/bin/python scripts/smoke/run_smoke.py --framework <fw>
Uses a deterministic STUB model (no LLM, no API key) and an in-process LOCAL MOCK /verify that returns the
non-study token SMOKE_ACK. Refuses any fixture other than SMOKE-000. Never contacts a real ExecutionProof
instance. Writes nothing to results/ or proofrecords/; prints one JSON summary line.
"""
import argparse, asyncio, json, sys, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts" / "validation"))
FIX = json.loads((ROOT / "fixtures/smoke/SMOKE-000.json").read_text())
assert FIX["fixture_id"] == "SMOKE-000" and FIX["native_arguments"]["action_type"] == "ENGINEERING_SMOKE_PING"
NATIVE = FIX["native_arguments"]
RECEIVED = []


class MockVerify(BaseHTTPRequestHandler):
    def do_POST(self):
        RECEIVED.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
        body = json.dumps(FIX["mock_response"]).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def log_message(self, *a):
        pass


def start_mock():
    srv = HTTPServer(("127.0.0.1", 0), MockVerify)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_port}"


def smoke_openai_agents(handler):
    from agents import Model, ModelResponse
    from agents.usage import Usage
    from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, ResponseOutputText
    from adapters.openai_agents.binding import TOOL_NAME, build_agent, run_once

    class StubModel(Model):
        def __init__(self): self.n = 0
        async def get_response(self, *a, **k):
            self.n += 1
            if self.n == 1:
                out = [ResponseFunctionToolCall(arguments=json.dumps(NATIVE), call_id="call-1", name=TOOL_NAME,
                                                type="function_call", id="fc-1", status="completed")]
            else:
                out = [ResponseOutputMessage(id="m-1", role="assistant", status="completed", type="message",
                       content=[ResponseOutputText(annotations=[], text="SMOKE DONE", type="output_text")])]
            return ModelResponse(output=out, usage=Usage(), response_id=None)
        def stream_response(self, *a, **k): raise NotImplementedError

    agent = build_agent(handler, StubModel())
    assert agent.handoffs == [] and len(agent.tools) == 1 and agent.model_settings.parallel_tool_calls is False
    res = run_once(agent, "SMOKE-000")
    outs = [i.output for i in res.new_items if type(i).__name__ == "ToolCallOutputItem"]
    return json.loads(outs[0]) if outs else None


def smoke_langgraph(handler):
    from adapters.langgraph.binding import build_graph, run_once
    return run_once(build_graph(handler), NATIVE)["result"]


def smoke_crewai(handler):
    from crewai.llms.base_llm import BaseLLM
    from adapters.crewai.binding import TOOL_NAME, build_crew
    args = dict(NATIVE, parameters=json.dumps(NATIVE["parameters"]))

    class StubLLM(BaseLLM):
        n: int = 0
        def call(self, messages, tools=None, callbacks=None, available_functions=None, **kw):
            self.n += 1
            if self.n == 1:
                return f"Thought: submit once\nAction: {TOOL_NAME}\nAction Input: {json.dumps(args)}"
            return "Thought: done\nFinal Answer: SMOKE DONE"
        def supports_function_calling(self): return False
        def supports_stop_words(self): return False
        def get_context_window_size(self): return 8192

    crew = build_crew(handler, StubLLM(model="stub-smoke-llm"), "SMOKE-000: call the tool exactly once.")
    a = crew.agents[0]
    assert a.allow_delegation is False and len(crew.agents) == 1 and len(crew.tasks) == 1
    crew.kickoff()
    return LAST[0] if LAST else None


def smoke_maf(handler):
    import agent_framework as af
    from agent_framework._tools import FunctionInvocationLayer
    from adapters.maf.binding import TOOL_NAME, build_agent

    class StubClient(FunctionInvocationLayer, af.BaseChatClient):
        def _inner_get_response(self, *, messages, stream, options, **kwargs):
            async def _r():
                done = any(getattr(c, "type", None) == "function_result" for m in messages for c in m.contents)
                if done:
                    return af.ChatResponse(messages=[af.Message(role="assistant", contents=[af.Content.from_text("SMOKE DONE")])])
                return af.ChatResponse(messages=[af.Message(role="assistant", contents=[
                    af.Content.from_function_call(call_id="call-1", name=TOOL_NAME, arguments=json.dumps(NATIVE))])])
            return _r()

    agent = build_agent(handler, StubClient())
    asyncio.run(agent.run("SMOKE-000"))
    return LAST[0] if LAST else None


LAST = []


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--framework", required=True,
        choices=["openai_agents", "langgraph", "crewai", "maf"]); ap.add_argument("--fixture", default="SMOKE-000")
    a = ap.parse_args()
    if a.fixture != "SMOKE-000":
        sys.exit("REFUSED: engineering smoke accepts SMOKE-000 only (B1–B5 execution is NOT AUTHORIZED).")
    import importlib
    from validate_schemas import validate_contract
    mod = importlib.import_module(f"adapters.{a.framework}.adapter")
    from harness_selftest import ADAPTER_CLASSES
    inst = getattr(mod, ADAPTER_CLASSES[a.framework])()
    srv, base = start_mock()
    calls = []

    def handler(native):
        calls.append(native)
        out = inst.handle_native(native, base_url=base, verify_path="/verify")
        LAST.append(out)
        return out

    summary = {"label": "ENGINEERING SMOKE ONLY — NOT EVIDENCE", "fixture": "SMOKE-000", "framework": a.framework}
    try:
        ret = globals()[f"smoke_{a.framework}"](handler)
        errs = validate_contract(RECEIVED[0]) if RECEIVED else ["mock received no contract"]
        checks = {
            "imports_ok": True,
            "tool_invoked_exactly_once": len(calls) == 1,
            "contract_schema_valid": not errs,
            "contract_framework_id_matches": bool(RECEIVED) and RECEIVED[0]["framework_id"] == inst.framework_id,
            "mock_verify_reached_once": len(RECEIVED) == 1,
            "return_object_came_back": isinstance(ret, dict) and ret.get("verdict") == "SMOKE_ACK"
                                        and ret.get("proof_record_id") == "smoke-000-mock-ref",
            "no_simulated_downstream_on_non_allow": isinstance(ret, dict) and ret.get("simulated_downstream") is None,
        }
        summary.update(checks=checks, schema_errors=errs, smoke="PASS" if all(checks.values()) else "FAIL")
    except Exception as e:  # report honestly
        summary.update(smoke="FAIL", error=f"{type(e).__name__}: {e}"[:400])
    finally:
        srv.shutdown()
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["smoke"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
