from typing import Any, Callable

from langgraph.graph import END, START, StateGraph

from packages.agent_core.nodes.approver import approver_node
from packages.agent_core.nodes.executor import executor_node
from packages.agent_core.nodes.planner import planner_node
from packages.agent_core.nodes.retriever import retriever_node
from packages.agent_core.nodes.reviewer import reviewer_node
from packages.agent_core.nodes.skill_router import skill_router_node
from packages.agent_core.state import AgentState


def _reviewer_router(state: AgentState) -> str:
    if state.get("needs_approval"):
        return "approver"
    return "completed"


def _approver_router(state: AgentState) -> str:
    status = state.get("approval_status", "")
    if status == "approved":
        return "executor"
    if status == "rejected":
        return "failed"
    # Still pending — treat as failed to avoid infinite loop
    return "failed"


def build_graph(on_step_event: Callable[..., Any] | None = None) -> Any:
    """Build and compile the LangGraph agent workflow.

    Flow: START -> skill_router -> planner -> retriever -> executor -> reviewer -> (approver | END)
    """
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("skill_router", skill_router_node)
    graph.add_node("planner", planner_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("executor", executor_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("approver", approver_node)

    # Edges — skill_router runs first to inject skill context
    graph.add_edge(START, "skill_router")
    graph.add_edge("skill_router", "planner")
    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "executor")
    graph.add_edge("executor", "reviewer")

    # Conditional: reviewer -> approver or completed
    graph.add_conditional_edges(
        "reviewer",
        _reviewer_router,
        {"approver": "approver", "completed": END},
    )

    # Conditional: approver -> executor (approved) or failed
    graph.add_conditional_edges(
        "approver",
        _approver_router,
        {"executor": "executor", "failed": END},
    )

    return graph.compile()
