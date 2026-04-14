import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ApprovalActionEnum(str, Enum):
    approve = "approve"
    reject = "reject"


class ApprovalResponse(BaseModel):
    id: uuid.UUID
    run_id: uuid.UUID
    step_id: uuid.UUID
    status: str
    reason: str | None = None
    created_at: datetime
    resolved_at: datetime | None = None

    model_config = {"from_attributes": True}


class ApprovalAction(BaseModel):
    action: ApprovalActionEnum
    reason: str | None = None
