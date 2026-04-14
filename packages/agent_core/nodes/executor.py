import time
from typing import Any

from packages.agent_core.state import AgentState
from packages.shared.types import NodeName, TaskStatus
from packages.toolkits import get_tool_by_name


async def executor_node(state: AgentState) -> dict[str, Any]:
    start = time.perf_counter()
    plan = state.get("plan", [])
    tool_results: list[dict[str, Any]] = []

    for step in plan:
        tool_needed = step.get("tool_needed", "none")
        if tool_needed == "none" or tool_needed == "knowledge_search":
            continue

        tool = get_tool_by_name(tool_needed)
        if tool is None:
            tool_results.append({
                "step_number": step.get("step_number"),
                "tool": tool_needed,
                "input": step.get("description", ""),
                "output": None,
                "success": False,
                "error": f"Unknown tool: {tool_needed}",
            })
            continue

        try:
            result = await tool.execute({"action": step.get("action", ""), "description": step.get("description", "")})
            tool_results.append({
                "step_number": step.get("step_number"),
                "tool": tool_needed,
                "input": step.get("description", ""),
                "output": result,
                "success": True,
            })
        except Exception as exc:
            tool_results.append({
                "step_number": step.get("step_number"),
                "tool": tool_needed,
                "input": step.get("description", ""),
                "output": None,
                "success": False,
                "error": str(exc),
            })

    latency_ms = int((time.perf_counter() - start) * 1000)

    step_log = {
        "node_name": NodeName.executor,
        "status": TaskStatus.executing,
        "latency_ms": latency_ms,
    }

    return {
        "tool_results": tool_results,
        "current_node": NodeName.executor,
        "steps_log": state.get("steps_log", []) + [step_log],
    }
