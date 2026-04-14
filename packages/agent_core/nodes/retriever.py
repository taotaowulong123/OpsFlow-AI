import time
from typing import Any

from packages.agent_core.state import AgentState
from packages.rag_core.retriever import KnowledgeRetriever
from packages.shared.types import NodeName, TaskStatus


async def retriever_node(state: AgentState) -> dict[str, Any]:
    start = time.perf_counter()
    plan = state.get("plan", [])

    # Build a combined query from plan steps that need knowledge_search
    queries = [
        step.get("description", "")
        for step in plan
        if step.get("tool_needed") == "knowledge_search"
    ]

    retrieved_docs: list[dict[str, Any]] = []

    if queries:
        retriever = KnowledgeRetriever()
        combined_query = " ".join(queries)
        results = await retriever.retrieve(query=combined_query, top_k=5)
        retrieved_docs = [
            {
                "content": r.content,
                "source": r.source,
                "score": r.score,
                "chunk_index": r.chunk_index,
            }
            for r in results
        ]

    latency_ms = int((time.perf_counter() - start) * 1000)

    step_log = {
        "node_name": NodeName.retriever,
        "status": TaskStatus.retrieving,
        "latency_ms": latency_ms,
    }

    return {
        "retrieved_docs": retrieved_docs,
        "current_node": NodeName.retriever,
        "steps_log": state.get("steps_log", []) + [step_log],
    }
