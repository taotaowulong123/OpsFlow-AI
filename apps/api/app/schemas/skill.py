from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SkillBase(BaseModel):
    name: str
    display_name: str
    description: str = ""
    version: str = "0.1.0"
    category: str = "domain"
    risk_level: str = "low"
    is_builtin: bool = True
    is_enabled: bool = True
    triggers: list[str] = []
    input_schema: dict = {}
    tools_allow: list[str] = []
    knowledge_scope: dict = {}
    approval_required_for: list[str] = []
    output_schema: dict = {}


class SkillCreate(SkillBase):
    manifest_json: dict = {}


class SkillRead(SkillBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    manifest_json: dict = {}
    created_at: datetime
    updated_at: datetime


class SkillUpdate(BaseModel):
    is_enabled: bool | None = None
    description: str | None = None
    triggers: list[str] | None = None


class SkillRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    task_id: str | None
    skill_id: str
    skill_version: str
    input_json: dict
    output_json: dict | None
    status: str
    started_at: datetime
    completed_at: datetime | None
    tokens_used: int
    duration_ms: float | None


class SkillEvalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    skill_id: str
    case_name: str
    input_json: dict
    expected_behavior: str
    actual_output: dict | None
    score: float | None
    evaluated_at: datetime | None


class SkillListResponse(BaseModel):
    count: int
    skills: list[SkillRead]
