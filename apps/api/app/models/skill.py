import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON, Integer, Float, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=False)
    description = Column(Text, default="")
    version = Column(String, default="0.1.0")
    category = Column(String, default="domain")  # domain | action | guardrail | composite
    risk_level = Column(String, default="low")  # low | medium | high
    is_builtin = Column(Boolean, default=True)
    is_enabled = Column(Boolean, default=True)
    triggers = Column(JSON, default=list)
    input_schema = Column(JSON, default=dict)
    tools_allow = Column(JSON, default=list)
    knowledge_scope = Column(JSON, default=dict)
    approval_required_for = Column(JSON, default=list)
    output_schema = Column(JSON, default=dict)
    manifest_json = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SkillRun(Base):
    __tablename__ = "skill_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, nullable=True)
    skill_id = Column(String, nullable=False)
    skill_version = Column(String, default="0.1.0")
    input_json = Column(JSON, default=dict)
    output_json = Column(JSON, nullable=True)
    status = Column(String, default="pending")  # pending | running | completed | failed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    tokens_used = Column(Integer, default=0)
    duration_ms = Column(Float, nullable=True)


class SkillEval(Base):
    __tablename__ = "skill_evals"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    skill_id = Column(String, nullable=False)
    case_name = Column(String, nullable=False)
    input_json = Column(JSON, default=dict)
    expected_behavior = Column(Text, default="")
    actual_output = Column(JSON, nullable=True)
    score = Column(Float, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), nullable=True)
