import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.task import Task, TaskRun
from app.schemas.task import TaskCreate, TaskResponse, TaskRunResponse
from app.services.task_service import execute_task
from app.services.sse import event_bus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(body: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = Task(title=body.title, description=body.description)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("", response_model=list[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).order_by(Task.created_at.desc()))
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/run", response_model=TaskRunResponse)
async def run_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        run = await execute_task(task_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    result = await db.execute(
        select(TaskRun).options(selectinload(TaskRun.steps)).where(TaskRun.id == run.id)
    )
    return result.scalar_one()


@router.get("/{task_id}/stream")
async def stream_task(task_id: uuid.UUID):
    return StreamingResponse(
        event_bus.subscribe_events(str(task_id)),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
