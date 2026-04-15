import json
import time
from typing import Any

from langchain_openai import ChatOpenAI

from app.core.config import settings
from packages.agent_core.state import AgentState
from packages.shared.types import NodeName, TaskStatus

REVIEWER_SYSTEM_PROMPT = (
    "You are a task reviewer. Given a plan, retrieved documents, and tool execution results, "
    "evaluate whether the task was completed successfully. Check for errors, missing steps, "
    "and insufficient evidence. Determine if any high-risk actions need human approval. "
    "Respond with JSON: {\"complete\": bool, \"errors\": [...], \"needs_approval\": bool, "
    "\"approval_reason\": str|null, \"summary\": str}"
)


async def reviewer_node(state: AgentState) -> dict[str, Any]:
    start = time.perf_counter()

    plan = state.get("plan", [])
    retrieved_docs = state.get("retrieved_docs", [])
    tool_results = state.get("tool_results", [])

    review_input = json.dumps({
        "plan": plan,
        "retrieved_docs": retrieved_docs,
        "tool_results": tool_results,
    }, default=str)

    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )
    response = await llm.ainvoke([
        {"role": "system", "content": REVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": review_input},
    ])

    content = response.content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1] if "\n" in content else content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    try:
        review_result = json.loads(content)
    except json.JSONDecodeError:
        review_result = {"complete": True, "errors": [], "needs_approval": False, "summary": content}

    needs_approval = review_result.get("needs_approval", False)
    final_output = review_result.get("summary", "")
    tokens_used = response.response_metadata.get("token_usage", {}).get("total_tokens", 0)
    latency_ms = int((time.perf_counter() - start) * 1000)

    step_log = {
        "node_name": NodeName.reviewer,
        "status": TaskStatus.reviewing,
        "tokens_used": tokens_used,
        "latency_ms": latency_ms,
    }

    return {
        "review_result": review_result,
        "needs_approval": needs_approval,
        "final_output": final_output,
        "current_node": NodeName.reviewer,
        "steps_log": state.get("steps_log", []) + [step_log],
    }
