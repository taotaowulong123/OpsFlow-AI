import time
from typing import Any

from packages.agent_core.state import AgentState
from packages.shared.types import NodeName, TaskStatus
from packages.toolkits import get_tool_by_name
from packages.toolkits.sql_tool import SQLTool


async def executor_node(state: AgentState) -> dict[str, Any]:
    start = time.perf_counter()
    plan = state.get("plan", [])
    db_session = state.get("db_session")
    tool_results: list[dict[str, Any]] = []

    for step in plan:
        tool_needed = step.get("tool_needed", "none")
        if tool_needed == "none" or tool_needed == "knowledge_search":
            continue

        tool = SQLTool(db_session) if tool_needed == "sql_query" else get_tool_by_name(tool_needed)
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
            params: dict[str, Any] = {
                "action": step.get("action", ""),
                "description": step.get("description", ""),
            }
            if tool_needed == "sql_query":
                params["query"] = step.get("query") or step.get("action") or step.get("description", "")
            elif tool_needed == "http_request":
                params["url"] = step.get("url", "")
                params["method"] = step.get("method", "GET")
                params["body"] = step.get("body")
                params["headers"] = step.get("headers", {})
            elif tool_needed == "browser_action":
                params["url"] = step.get("url", "")
                params["selector"] = step.get("selector", "")
                params["value"] = step.get("value", "")
                params["path"] = step.get("path", "")
            elif tool_needed == "file_generate":
                params["filename"] = step.get("filename", "output")
                params["content"] = step.get("content", "")
                params["headers"] = step.get("headers", [])
                params["rows"] = step.get("rows", [])

            result = await tool.execute(params)
            tool_results.append({
                "step_number": step.get("step_number"),
                "tool": tool_needed,
                "input": params,
                "output": result,
                "success": result.get("success", True) if isinstance(result, dict) else True,
                "error": result.get("error") if isinstance(result, dict) else None,
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
