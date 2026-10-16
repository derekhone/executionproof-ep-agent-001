"""Microsoft Agent Framework 1.22.0 binding: ONE Agent, ONE agent_framework.tool, ONE FunctionMiddleware
attached only to that tool path (scope guard). No workflows, orchestrations, A2A, or multi-agent use
(those packages are installed transitively by agent-framework==1.22.0 and are not imported)."""
import json
from typing import Optional

TOOL_NAME = "ep_verified_action"


def build_agent(handler, client):
    import agent_framework as af

    @af.tool(name=TOOL_NAME, description="Submit ONE proposed action for ExecutionProof verification.")
    def ep_verified_action(actor_id: str, action_type: str, target: str, parameters: dict,
                           authority_reference: str, policy_reference: str,
                           evidence_references: Optional[list] = None,
                           current_state_reference: Optional[str] = None) -> str:
        native = {k: v for k, v in dict(actor_id=actor_id, action_type=action_type, target=target,
                  parameters=parameters, authority_reference=authority_reference,
                  policy_reference=policy_reference, evidence_references=evidence_references,
                  current_state_reference=current_state_reference).items() if v is not None}
        return json.dumps(handler(native), sort_keys=True)

    class EPSingleToolPathMiddleware(af.FunctionMiddleware):
        async def process(self, context, call_next):
            if context.function.name != TOOL_NAME:
                raise RuntimeError("EP-AGENT-001: out-of-scope tool invocation refused")
            await call_next()

    return af.Agent(client=client, tools=[ep_verified_action], middleware=[EPSingleToolPathMiddleware()],
                    name="ep-agent-001-single", instructions=f"Call {TOOL_NAME} exactly once.")
