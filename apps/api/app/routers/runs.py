import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.task import TaskRun, RunStep
from app.models.approval import Approval, ApprovalStatus
from app.schemas.task import TaskRunResponse, RunStepResponse
from app.schemas.approval import ApprovalAction, ApprovalResponse

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("", response_model=list[TaskRunResponse])
async def list_runs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TaskRun).options(selectinload(TaskRun.steps)).order_by(TaskRun.started_at.desc())
    )
    return result.scalars().all()


@router.get("/{run_id}", response_model=TaskRunResponse)
async def get_run(run_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TaskRun).options(selectinload(TaskRun.steps)).where(TaskRun.id == run_id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/{run_id}/steps", response_model=list[RunStepResponse])
async def get_run_steps(run_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RunStep).where(RunStep.run_id == run_id).order_by(RunStep.started_at)
    )
    return result.scalars().all()


@router.post("/{run_id}/approve", response_model=ApprovalResponse)
async def approve_run(run_id: uuid.UUID, body: ApprovalAction, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Approval).where(Approval.run_id == run_id, Approval.status == ApprovalStatus.pending)
    )
    approval = result.scalar_one_or_none()
    if not approval:
        raise HTTPException(status_code=404, detail="No pending approval for this run")

    approval.status = ApprovalStatus.approved if body.action.value == "approve" else ApprovalStatus.rejected
    approval.reason = body.reason
    approval.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(approval)
    return approval
