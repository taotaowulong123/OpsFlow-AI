import uuid
from datetime import datetime

from pydantic import BaseModel


class ToolResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    tool_type: str
    schema_def: dict | None = None
    enabled: bool
    risk_level: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ToolInvocationResponse(BaseModel):
    id: uuid.UUID
    run_step_id: uuid.UUID
    tool_id: uuid.UUID
    input_data: dict | None = None
    output_data: dict | None = None
    status: str
    latency_ms: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
