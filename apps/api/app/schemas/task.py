import uuid
from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RunStepResponse(BaseModel):
    id: uuid.UUID
    run_id: uuid.UUID
    node_name: str
    status: str
    input_data: dict | None = None
    output_data: dict | None = None
    evidence: dict | None = None
    tokens_used: int | None = None
    latency_ms: int | None = None
    started_at: datetime
    finished_at: datetime | None = None
    error_message: str | None = None

    model_config = {"from_attributes": True}


class TaskRunResponse(BaseModel):
    id: uuid.UUID
    task_id: uuid.UUID
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    total_tokens: int | None = None
    total_cost: float | None = None
    steps: list[RunStepResponse] = []

    model_config = {"from_attributes": True}
