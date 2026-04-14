import json
import os
import time
from typing import Any

from langchain_openai import ChatOpenAI

from packages.agent_core.state import AgentState
from packages.shared.types import NodeName, TaskStatus

PLANNER_SYSTEM_PROMPT = (
    "You are a task planner. Break down the user's task into concrete executable steps. "
    "Each step should specify what action to take and what tool is needed "
    "(knowledge_search, sql_query, http_request, browser_action, file_generate, or none). "
    "Respond with a JSON array of objects with keys: step_number, action, description, tool_needed."
)


async def planner_node(state: AgentState) -> dict[str, Any]:
    start = time.perf_counter()
    task_description = state.get("task_description", "")

    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o"),
        temperature=0,
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )
    response = await llm.ainvoke([
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {"role": "user", "content": task_description},
    ])

    content = response.content.strip()
    # Strip markdown fences if present
    if content.startswith("```"):
        content = content.split("\n", 1)[1] if "\n" in content else content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    try:
        plan = json.loads(content)
    except json.JSONDecodeError:
        plan = [{"step_number": 1, "action": task_description, "description": task_description, "tool_needed": "none"}]

    tokens_used = response.response_metadata.get("token_usage", {}).get("total_tokens", 0)
    latency_ms = int((time.perf_counter() - start) * 1000)

    step_log = {
        "node_name": NodeName.planner,
        "status": TaskStatus.planning,
        "tokens_used": tokens_used,
        "latency_ms": latency_ms,
    }

    return {
        "plan": plan,
        "current_node": NodeName.planner,
        "steps_log": state.get("steps_log", []) + [step_log],
    }
