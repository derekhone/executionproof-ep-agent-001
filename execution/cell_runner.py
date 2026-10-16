#!/usr/bin/env python3
"""
EP-AGENT-001 AUTHORIZED EXECUTION — per-framework cell runner (runs INSIDE .venv-<fw>).

Authorization: Derek Hone written execution authorization (execution/EXECUTION_AUTHORIZATION.md).
Implements STUDY_PROTOCOL.md §3–§7 for ONE framework: for each case B1..B5 in order:
  1 decision call -> 5 warmup calls (discarded) -> 30 measured latency calls.
Every call is ONE single-agent framework run that makes exactly ONE tool call, driven by a deterministic stub
model (no LLM, no API key). Tool arguments come verbatim from the frozen fixture. The handler performs exactly
the adapter's handle_native steps (extract -> normalize -> verify -> finalize) using the adapter's own methods,
instrumented for S4/S5 timing and verbatim contract capture. No verdict logic exists in this file.
Writes append-only JSONL under results/<fw>/ and ProofRecords under proofrecords/<fw>/.
"""
import argparse, asyncio, hashlib, importlib, json, sys, time, traceback, urllib.error, urllib.request
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts" / "validation"))
from validate_schemas import validate_contract  # noqa: E402
from adapters import ep_client  # noqa: E402

CASES = ["B1", "B2", "B3", "B4", "B5"]
FILES = {"B1": "B1_allow_complete", "B2": "B2_hold_incomplete_contract", "B3": "B3_deny_no_authority",
         "B4": "B4_hold_evidence_absent", "B5": "B5_hold_constraint_exceeded"}
CLASSES = {"openai_agents": "EPVerificationTool", "langgraph": "EPVerifiedToolNode",
           "crewai": "EPVerifiedCrewTool", "maf": "EPVerificationMiddleware"}
PKG = {"openai_agents": "openai-agents", "langgraph": "langgraph", "crewai": "crewai", "maf": "agent-framework"}
WARMUP, MEASURED = 5, 30


def utc():
    return datetime.now(timezone.utc).isoformat()


class Harness:
    def __init__(self, fw, base):
        self.fw, self.base = fw, base
        self.mod = importlib.import_module(f"adapters.{fw}.adapter")
        self.extract = importlib.import_module(f"adapters.{fw}.normalizer").extract_native_arguments
        self.inst = getattr(self.mod, CLASSES[fw])()
        self.calls = []

    def handler(self, native):
        t0 = time.perf_counter_ns()
        rec = {"native_arguments_received": native}
        n0 = time.perf_counter_ns()
        contract = self.inst.normalize_to_request_contract(**self.extract(native))
        n1 = time.perf_counter_ns()
        rec["normalized_contract"] = json.loads(json.dumps(contract))  # stored verbatim before submission
        rec["verify_request_sent_at"] = utc(); s_ns = time.perf_counter_ns()
        try:
            resp = self.inst.verify(contract, base_url=self.base, verify_path="/verify")
            rec["http_status"] = 200
        except urllib.error.HTTPError as e:
            rec["http_status"] = e.code; rec["raw_error_body"] = e.read().decode("utf-8", "replace")
            rec.update(verify_request_completed_ns=time.perf_counter_ns() - s_ns, verify_response_received_at=utc())
            self.calls.append(rec); raise
        rec["verify_response_received_at"] = utc(); rec["verify_rtt_ns"] = time.perf_counter_ns() - s_ns
        rec["raw_verify_response"] = resp["raw"]
        out = ep_client.finalize(contract, resp)  # same call the adapter handle_native makes
        t1 = time.perf_counter_ns()
        rec.update(s4_normalization_ns=n1 - n0, s5_adapter_round_trip_ns=t1 - t0, adapter_return=out)
        self.calls.append(rec)
        return out


# ---------------- framework runs (deterministic stub models; exactly one tool call per run) ----------------
def run_openai_agents(h, native):
    from agents import Model, ModelResponse
    from agents.usage import Usage
    from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, ResponseOutputText
    from adapters.openai_agents.binding import TOOL_NAME, build_agent, run_once

    class StubModel(Model):
        def __init__(self): self.n = 0
        async def get_response(self, *a, **k):
            self.n += 1
            if self.n == 1:
                out = [ResponseFunctionToolCall(arguments=json.dumps(native), call_id="call-1", name=TOOL_NAME,
                                                type="function_call", id="fc-1", status="completed")]
            else:
                out = [ResponseOutputMessage(id="m-1", role="assistant", status="completed", type="message",
                       content=[ResponseOutputText(annotations=[], text="DONE", type="output_text")])]
            return ModelResponse(output=out, usage=Usage(), response_id=None)
        def stream_response(self, *a, **k): raise NotImplementedError

    agent = build_agent(h.handler, StubModel())
    scope = agent.handoffs == [] and len(agent.tools) == 1 and agent.model_settings.parallel_tool_calls is False
    res = run_once(agent, "EP-AGENT-001")
    outs = [i.output for i in res.new_items if type(i).__name__ == "ToolCallOutputItem"]
    return (outs[0] if outs else None), scope


def run_langgraph(h, native):
    from adapters.langgraph.binding import build_graph, run_once
    state = run_once(build_graph(h.handler), native)
    return json.dumps(state.get("result"), sort_keys=True), True


def run_crewai(h, native):
    from crewai.llms.base_llm import BaseLLM
    from adapters.crewai.binding import TOOL_NAME, build_crew
    args = dict(native, parameters=json.dumps(native["parameters"]))

    class StubLLM(BaseLLM):
        n: int = 0
        def call(self, messages, tools=None, callbacks=None, available_functions=None, **kw):
            self.n += 1
            if self.n == 1:
                return f"Thought: submit once\nAction: {TOOL_NAME}\nAction Input: {json.dumps(args)}"
            text = messages if isinstance(messages, str) else "\n".join(str(m.get("content", "")) for m in messages)
            obs = text.rsplit("Observation:", 1)[-1].strip() if "Observation:" in text else text[-2000:]
            return "Thought: done\nFinal Answer: " + obs.splitlines()[0] if obs else "Thought: done\nFinal Answer: NONE"
        def supports_function_calling(self): return False
        def supports_stop_words(self): return False
        def get_context_window_size(self): return 8192

    crew = build_crew(h.handler, StubLLM(model="stub-ep-agent-001"), "EP-AGENT-001: call the tool exactly once.")
    a = crew.agents[0]
    scope = a.allow_delegation is False and len(crew.agents) == 1 and len(crew.tasks) == 1
    out = crew.kickoff()
    return str(getattr(out, "raw", out)), scope


def run_maf(h, native):
    import agent_framework as af
    from agent_framework._tools import FunctionInvocationLayer
    from adapters.maf.binding import TOOL_NAME, build_agent

    class StubClient(FunctionInvocationLayer, af.BaseChatClient):
        def _inner_get_response(self, *, messages, stream, options, **kwargs):
            async def _r():
                res = [c for m in messages for c in m.contents if getattr(c, "type", None) == "function_result"]
                if res:
                    return af.ChatResponse(messages=[af.Message(role="assistant", contents=[
                        af.Content.from_text(str(getattr(res[-1], "result", res[-1])))])])
                return af.ChatResponse(messages=[af.Message(role="assistant", contents=[
                    af.Content.from_function_call(call_id="call-1", name=TOOL_NAME, arguments=json.dumps(native))])])
            return _r()

    agent = build_agent(h.handler, StubClient())
    resp = asyncio.run(agent.run("EP-AGENT-001"))
    return str(getattr(resp, "text", resp)), True


def get_json(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.status, r.read()


def one_run(h, native):
    n_before = len(h.calls)
    err = None; native_result = None; scope = None
    t0 = time.perf_counter_ns()
    try:
        native_result, scope = globals()[f"run_{h.fw}"](h, native)
    except Exception as e:  # preserved exactly as observed
        err = {"type": type(e).__name__, "message": str(e)[:2000], "traceback": traceback.format_exc()[-6000:]}
    wall = time.perf_counter_ns() - t0
    calls = h.calls[n_before:]
    return {"tool_invocations": len(calls), "calls": calls, "framework_native_result": native_result,
            "single_agent_scope_asserted": scope, "framework_run_wall_ns": wall, "error": err}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", required=True, choices=sorted(CLASSES)); ap.add_argument("--base-url", required=True)
    ap.add_argument("--mode", choices=["study", "ttfv"], default="study")
    a = ap.parse_args()
    h = Harness(a.framework, a.base_url)
    fw = a.framework
    if a.mode == "ttfv":  # S2 time-to-first-verify, non-study smoke fixture (not B1-B5)
        nat = json.loads((ROOT / "fixtures/smoke/SMOKE-000.json").read_text())["native_arguments"]
        try:
            h.handler({"name": "ep_verified_action", "args": dict(nat), "id": "ttfv-1"} if fw == "langgraph" else dict(nat)); print(json.dumps({"ttfv_ok": True, "at": utc()}))
        except Exception as e:
            print(json.dumps({"ttfv_ok": False, "error": f"{type(e).__name__}: {e}", "at": utc()}))
        return 0
    out_dir = ROOT / "results" / fw; pr_dir = ROOT / "proofrecords" / fw
    out_dir.mkdir(parents=True, exist_ok=True); pr_dir.mkdir(parents=True, exist_ok=True)
    version = metadata.version(PKG[fw])
    dec_f = open(out_dir / "decision_calls.jsonl", "a"); lat_f = open(out_dir / "latency_calls.jsonl", "a")
    for case in CASES:
        path = ROOT / "fixtures" / "benign" / f"{FILES[case]}.json"
        raw = path.read_bytes(); fx = json.loads(raw)
        native = dict(fx["contract"])
        r = one_run(h, native)
        c = r["calls"][0] if r["calls"] else {}
        resp = c.get("raw_verify_response") or {}
        pid = resp.get("proof_record_id")
        rec = {"framework_id": fw, "framework_version": version, "case_id": case,
               "fixture_sha256": hashlib.sha256(raw).hexdigest(), "expected_verdict": fx["expected_verdict"],
               "normalized_contract": c.get("normalized_contract"),
               "schema_errors": validate_contract(c["normalized_contract"]) if c.get("normalized_contract") else ["no contract"],
               "verify_request_sent_at": c.get("verify_request_sent_at"),
               "verify_response_received_at": c.get("verify_response_received_at"),
               "http_status": c.get("http_status"), "raw_verify_response": resp or None,
               "raw_error_body": c.get("raw_error_body"),
               "observed_verdict": resp.get("verdict"), "proof_record_id": pid,
               "framework_native_result": r["framework_native_result"], "tool_invocations": r["tool_invocations"],
               "single_agent_scope_asserted": r["single_agent_scope_asserted"], "error": r["error"],
               "s4_normalization_ns": c.get("s4_normalization_ns"), "s5_adapter_round_trip_ns": c.get("s5_adapter_round_trip_ns"),
               "manual_intervention": False, "core_modification": False, "notes": "", "deviation_ids": []}
        rec["schema_valid"] = not rec["schema_errors"]
        nr = rec["framework_native_result"] or ""
        rec["verdict_in_native_result"] = bool(rec["observed_verdict"]) and rec["observed_verdict"] in nr
        rec["proof_ref_in_native_result"] = bool(pid) and pid in nr
        # §6 ProofRecord capture
        rec["proof_record_resolves"] = False
        if pid:
            try:
                st, body = get_json(f"{a.base_url}/proof/{pid}")
                (pr_dir / f"{case}.json").write_bytes(body)
                prj = json.loads(body)
                rec.update(proof_get_status=st, proof_record_sha256=hashlib.sha256(body).hexdigest(),
                           proof_verdict_matches=prj.get("final_verdict") == rec["observed_verdict"],
                           proof_request_id_matches=prj.get("request_id") == (rec["normalized_contract"] or {}).get("request_id"),
                           proof_action_hash_matches=prj.get("action_hash") == (rec["normalized_contract"] or {}).get("action_hash"))
                rec["proof_record_resolves"] = st == 200 and rec["proof_verdict_matches"] and rec["proof_request_id_matches"]
            except Exception as e:
                rec["proof_get_error"] = f"{type(e).__name__}: {e}"
        rec["recorded_at"] = utc()
        dec_f.write(json.dumps(rec, sort_keys=True) + "\n"); dec_f.flush()
        # §7 latency: 5 warmup (discarded from stats, still logged) + 30 measured
        for i in range(WARMUP + MEASURED):
            lr = one_run(h, dict(fx["contract"]))
            lc = lr["calls"][0] if lr["calls"] else {}
            lat_f.write(json.dumps({"framework_id": fw, "case_id": case, "index": i, "phase": "warmup" if i < WARMUP else "measured",
                                    "s4_normalization_ns": lc.get("s4_normalization_ns"),
                                    "s5_adapter_round_trip_ns": lc.get("s5_adapter_round_trip_ns"),
                                    "verify_rtt_ns": lc.get("verify_rtt_ns"),
                                    "verdict": (lc.get("raw_verify_response") or {}).get("verdict"),
                                    "proof_record_id": (lc.get("raw_verify_response") or {}).get("proof_record_id"),
                                    "request_id": (lc.get("normalized_contract") or {}).get("request_id"),
                                    "tool_invocations": lr["tool_invocations"], "error": lr["error"]}, sort_keys=True) + "\n")
        lat_f.flush()
        print(json.dumps({"framework": fw, "case": case, "observed": rec["observed_verdict"], "error": bool(r["error"])}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
