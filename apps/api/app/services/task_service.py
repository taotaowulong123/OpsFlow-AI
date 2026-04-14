import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskRun, RunStep, TaskStatus
from app.services.sse import event_bus


async def execute_task(task_id: uuid.UUID, db: AsyncSession) -> TaskRun:
    task = await db.get(Task, task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")

    task.status = TaskStatus.executing
    run = TaskRun(task_id=task_id, status="running")
    db.add(run)
    await db.commit()
    await db.refresh(run)

    asyncio.create_task(_run_agent(run.id, task, db))
    return run


async def _run_agent(run_id: uuid.UUID, task: Task, db: AsyncSession) -> None:
    try:
        await event_bus.publish_event(
            str(task.id), "step_start", {"run_id": str(run_id), "node": "planning"}
        )

        step = RunStep(
            run_id=run_id,
            node_name="planning",
            status="running",
        )
        db.add(step)
        await db.commit()
        await db.refresh(step)

        # Placeholder: integrate with packages.agent_core graph here
        await asyncio.sleep(0.5)

        step.status = "completed"
        step.finished_at = datetime.now(timezone.utc)
        step.output_data = {"plan": f"Generated plan for: {task.title}"}
        await db.commit()

        await event_bus.publish_event(
            str(task.id), "step_complete", {"run_id": str(run_id), "node": "planning"}
        )

        run = await db.get(TaskRun, run_id)
        if run:
            run.status = "completed"
            run.finished_at = datetime.now(timezone.utc)
        task.status = TaskStatus.completed
        await db.commit()

        await event_bus.publish_event(
            str(task.id), "complete", {"run_id": str(run_id), "status": "completed"}
        )

    except Exception as e:
        run = await db.get(TaskRun, run_id)
        if run:
            run.status = "failed"
            run.finished_at = datetime.now(timezone.utc)
        task.status = TaskStatus.failed
        await db.commit()

        await event_bus.publish_event(
            str(task.id), "error", {"run_id": str(run_id), "error": str(e)}
        )
