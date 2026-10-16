"""CrewAI 1.15.28 binding: ONE Agent (allow_delegation=False), ONE Task, ONE BaseTool, sequential Crew.
The tool's _run receives schema-validated kwargs and passes them to handler unchanged."""
import json
from typing import Optional

TOOL_NAME = "ep_verified_action"


def build_crew(handler, llm, task_description: str):
    from crewai import Agent, Crew, Process, Task
    from crewai.tools import BaseTool
    from pydantic import BaseModel

    class EPArgs(BaseModel):
        actor_id: str
        action_type: str
        target: str
        parameters: str  # JSON object string; parsed once by the frozen normalizer
        authority_reference: str
        policy_reference: str
        evidence_references: Optional[list] = None
        current_state_reference: Optional[str] = None

    class EPVerifiedActionTool(BaseTool):
        name: str = TOOL_NAME
        description: str = "Submit ONE proposed action for ExecutionProof verification."
        args_schema: type = EPArgs

        def _run(self, **kwargs) -> str:
            return json.dumps(handler(kwargs), sort_keys=True)

    agent = Agent(role="EP-AGENT-001 single agent", goal="Submit exactly one proposed action.",
                  backstory="Single-agent tool path only.", tools=[EPVerifiedActionTool()], llm=llm,
                  allow_delegation=False, max_iter=3, verbose=False)
    task = Task(description=task_description, expected_output="The verification verdict.", agent=agent)
    return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
