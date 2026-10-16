"""LangGraph 1.2.15 binding: single-agent / single-tool StateGraph (START -> ep_verified_action -> END).
No supervisor, no subgraphs, no multi-agent routing. The node passes the framework-native tool call
mapping {"name","args","id"} to handler unchanged."""
from typing import TypedDict

TOOL_NAME = "ep_verified_action"


class EPState(TypedDict, total=False):
    tool_call: dict
    result: dict


def build_graph(handler):
    from langgraph.graph import END, START, StateGraph

    def ep_tool_node(state: EPState) -> dict:
        assert state["tool_call"]["name"] == TOOL_NAME
        return {"result": handler(state["tool_call"])}

    g = StateGraph(EPState)
    g.add_node(TOOL_NAME, ep_tool_node)
    g.add_edge(START, TOOL_NAME)
    g.add_edge(TOOL_NAME, END)
    return g.compile()


def run_once(graph, native_arguments: dict, call_id: str = "call-1") -> dict:
    return graph.invoke({"tool_call": {"name": TOOL_NAME, "args": native_arguments, "id": call_id}})
