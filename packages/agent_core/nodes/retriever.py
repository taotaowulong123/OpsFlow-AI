import time
from typing import Any

from sqlalchemy import text

from packages.agent_core.state import AgentState
from packages.rag_core.retriever import KnowledgeRetriever
from packages.shared.types import NodeName, TaskStatus


async def retriever_node(state: AgentState) -> dict[str, Any]:
    start = time.perf_counter()
    plan = state.get("plan", [])
    db_session = state.get("db_session")

    # Build a combined query from plan steps that need knowledge_search
    queries = [
        step.get("description", "")
        for step in plan
        if step.get("tool_needed") == "knowledge_search"
    ]

    retrieved_docs: list[dict[str, Any]] = []
    retrieval_status = "skipped"
    retrieval_detail = "No knowledge search requested."

    if queries and db_session is not None:
        chunk_count_result = await db_session.execute(text("SELECT COUNT(*) FROM document_chunks"))
        chunk_count = int(chunk_count_result.scalar() or 0)

        if chunk_count == 0:
            retrieval_detail = "Knowledge base is empty. Skipping retrieval."
        else:
            try:
                retriever = KnowledgeRetriever()
                combined_query = " ".join(queries)
                results = await retriever.retrieve(query=combined_query, top_k=5, db_session=db_session)
                retrieved_docs = [
                    {
                        "content": r.content,
                        "source": r.source,
                        "score": r.score,
                        "chunk_index": r.chunk_index,
                    }
                    for r in results
                ]
                retrieval_status = "completed"
                retrieval_detail = f"Retrieved {len(retrieved_docs)} document chunks."
            except Exception as exc:
                retrieval_status = "skipped"
                retrieval_detail = f"Retrieval skipped: {exc}"

    latency_ms = int((time.perf_counter() - start) * 1000)

    step_log = {
        "node_name": NodeName.retriever,
        "status": TaskStatus.retrieving,
        "latency_ms": latency_ms,
        "detail": retrieval_detail,
    }

    return {
        "retrieved_docs": retrieved_docs,
        "retrieval_status": retrieval_status,
        "retrieval_detail": retrieval_detail,
        "current_node": NodeName.retriever,
        "steps_log": state.get("steps_log", []) + [step_log],
    }
