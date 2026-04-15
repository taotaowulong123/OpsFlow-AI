import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.models.approval import Approval
from app.models.task import Task, TaskRun, RunStep, TaskStatus
from app.services.sse import event_bus
from packages.agent_core.graph import build_graph


def _serialize_status(value: Any, default: str = "completed") -> str:
    if value is None:
        return default
    normalized = getattr(value, "value", value)
    if normalized in {"planning", "retrieving", "executing", "reviewing", "matched", "no_match"}:
        return "completed"
    return normalized


def _build_step_payloads(state: dict[str, Any], task: Task) -> list[dict[str, Any]]:
    plan = state.get("plan", [])
    retrieved_docs = state.get("retrieved_docs", [])
    tool_results = state.get("tool_results", [])
    review_result = state.get("review_result", {})
    steps_log = state.get("steps_log", [])

    payloads: list[dict[str, Any]] = []
    for step_log in steps_log:
        node_name = step_log.get("node_name") or step_log.get("node")
        if not node_name:
            continue

        status = _serialize_status(step_log.get("status"), "completed")
        input_data: dict[str, Any] = {}
        output_data: dict[str, Any] = {}
        evidence: dict[str, Any] = {}
        error_message = step_log.get("error")

        if node_name == "skill_router":
            input_data = {"task_description": state.get("task_description", task.description or task.title)}
            output_data = {
                "skill_name": state.get("skill_name"),
                "detail": step_log.get("detail"),
                "score": step_log.get("score"),
            }
        elif node_name == "planner":
            input_data = {"task_description": state.get("task_description", task.description or task.title)}
            output_data = {"plan": plan}
        elif node_name == "retriever":
            input_data = {"plan": plan}
            output_data = {
                "retrieved_docs": retrieved_docs,
                "retrieval_status": state.get("retrieval_status"),
                "detail": state.get("retrieval_detail"),
            }
            evidence = {"documents": retrieved_docs}
        elif node_name == "executor":
            input_data = {"plan": plan, "retrieved_docs": retrieved_docs}
            output_data = {"tool_results": tool_results}
            evidence = {"tool_results": tool_results}
            if not error_message:
                first_error = next(
                    (
                        result.get("error")
                        for result in tool_results
                        if isinstance(result, dict) and result.get("error")
                    ),
                    None,
                )
                error_message = first_error
        elif node_name == "reviewer":
            input_data = {
                "plan": plan,
                "retrieved_docs": retrieved_docs,
                "tool_results": tool_results,
            }
            output_data = {
                "review_result": review_result,
                "final_output": state.get("final_output", ""),
            }
        elif node_name == "approver":
            input_data = {"review_result": review_result}
            output_data = {
                "approval_status": state.get("approval_status"),
                "approval_reason": review_result.get("approval_reason"),
            }
        else:
            output_data = {"detail": step_log.get("detail")}

        payloads.append(
            {
                "node_name": str(node_name),
                "status": status,
                "input_data": input_data or None,
                "output_data": output_data or None,
                "evidence": evidence or None,
                "tokens_used": step_log.get("tokens_used"),
                "latency_ms": step_log.get("latency_ms"),
                "error_message": error_message,
            }
        )

    return payloads


async def execute_task(task_id: uuid.UUID, db: AsyncSession) -> TaskRun:
    task = await db.get(Task, task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")

    task.status = TaskStatus.executing
    run = TaskRun(task_id=task_id, status="running")
    db.add(run)
    await db.commit()
    await db.refresh(run)

    asyncio.create_task(_run_agent(run.id, task.id))
    return run


async def _run_agent(run_id: uuid.UUID, task_id: uuid.UUID) -> None:
    async with async_session() as db:
        task = await db.get(Task, task_id)
        if not task:
            return

        try:
            graph = build_graph()
            final_state = await graph.ainvoke(
                {
                    "task_id": str(task.id),
                    "task_description": task.description or task.title,
                    "db_session": db,
                    "steps_log": [],
                }
            )

            step_payloads = _build_step_payloads(final_state, task)
            approval_step_id: uuid.UUID | None = None

            for payload in step_payloads:
                step = RunStep(
                    run_id=run_id,
                    node_name=payload["node_name"],
                    status=payload["status"],
                    input_data=payload["input_data"],
                    output_data=payload["output_data"],
                    evidence=payload["evidence"],
                    tokens_used=payload["tokens_used"],
                    latency_ms=payload["latency_ms"],
                    error_message=payload["error_message"],
                    finished_at=datetime.now(timezone.utc),
                )
                db.add(step)
                await db.flush()

                if payload["node_name"] == "approver":
                    approval_step_id = step.id

                await event_bus.publish_event(
                    str(task.id),
                    "step_complete",
                    {
                        "run_id": str(run_id),
                        "node": payload["node_name"],
                        "status": payload["status"],
                    },
                )

            run = await db.get(TaskRun, run_id)
            if not run:
                return

            total_tokens = sum(payload.get("tokens_used") or 0 for payload in step_payloads)
            run.total_tokens = total_tokens or None

            review_result = final_state.get("review_result", {})
            approval_pending = final_state.get("approval_status") == "pending"
            has_error = bool(final_state.get("error")) or review_result.get("complete") is False

            if approval_pending:
                run.status = "waiting_approval"
                task.status = TaskStatus.waiting_approval
                if approval_step_id is not None:
                    db.add(
                        Approval(
                            run_id=run_id,
                            step_id=approval_step_id,
                            reason=review_result.get("approval_reason"),
                        )
                    )
                await event_bus.publish_event(
                    str(task.id),
                    "waiting_approval",
                    {"run_id": str(run_id), "status": "waiting_approval"},
                )
            elif has_error:
                run.status = "failed"
                run.finished_at = datetime.now(timezone.utc)
                task.status = TaskStatus.failed
                await event_bus.publish_event(
                    str(task.id),
                    "error",
                    {
                        "run_id": str(run_id),
                        "error": final_state.get("error") or review_result.get("errors") or "Task failed",
                    },
                )
            else:
                run.status = "completed"
                run.finished_at = datetime.now(timezone.utc)
                task.status = TaskStatus.completed
                await event_bus.publish_event(
                    str(task.id),
                    "complete",
                    {"run_id": str(run_id), "status": "completed"},
                )

            await db.commit()

        except Exception as e:
            run = await db.get(TaskRun, run_id)
            if run:
                run.status = "failed"
                run.finished_at = datetime.now(timezone.utc)

            task.status = TaskStatus.failed

            db.add(
                RunStep(
                    run_id=run_id,
                    node_name="system",
                    status="failed",
                    error_message=str(e),
                    finished_at=datetime.now(timezone.utc),
                )
            )
            await db.commit()

            await event_bus.publish_event(
                str(task.id), "error", {"run_id": str(run_id), "error": str(e)}
            )
