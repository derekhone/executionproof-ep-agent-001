"""OpenAI Agents SDK 0.24.0 binding: ONE Agent, ONE FunctionTool, handoffs=[], parallel_tool_calls=False.
The tool receives the framework-native raw JSON argument string and passes it to handler unchanged."""
import json

TOOL_NAME = "ep_verified_action"
PARAMS_SCHEMA = {
    "type": "object",
    "properties": {k: {"type": t} for k, t in [
        ("actor_id", "string"), ("action_type", "string"), ("target", "string"), ("parameters", "object"),
        ("authority_reference", "string"), ("policy_reference", "string"),
        ("evidence_references", "array"), ("current_state_reference", "string")]},
    "required": ["actor_id", "action_type", "target", "parameters", "authority_reference", "policy_reference"],
}


def build_agent(handler, model):
    from agents import Agent, FunctionTool, ModelSettings

    async def _invoke(ctx, raw_arguments: str) -> str:
        return json.dumps(handler(raw_arguments), sort_keys=True)

    tool = FunctionTool(name=TOOL_NAME, description="Submit ONE proposed action for ExecutionProof verification.",
                        params_json_schema=PARAMS_SCHEMA, on_invoke_tool=_invoke, strict_json_schema=False)
    return Agent(name="ep-agent-001-single", instructions=f"Call {TOOL_NAME} exactly once.", tools=[tool],
                 handoffs=[], model=model, model_settings=ModelSettings(parallel_tool_calls=False))


def run_once(agent, prompt: str):
    from agents import Runner
    return Runner.run_sync(agent, prompt, max_turns=3)
