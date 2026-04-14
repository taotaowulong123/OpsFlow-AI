import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    pending = "pending"
    planning = "planning"
    executing = "executing"
    waiting_approval = "waiting_approval"
    completed = "completed"
    failed = "failed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    runs: Mapped[list["TaskRun"]] = relationship(back_populates="task", cascade="all, delete-orphan")


class TaskRun(Base):
    __tablename__ = "task_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(50), default="running")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_cost: Mapped[float | None] = mapped_column(Float, nullable=True)

    task: Mapped["Task"] = relationship(back_populates="runs")
    steps: Mapped[list["RunStep"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class RunStep(Base):
    __tablename__ = "run_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("task_runs.id", ondelete="CASCADE"))
    node_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="running")
    input_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    output_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    evidence: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    run: Mapped["TaskRun"] = relationship(back_populates="steps")
    tool_invocations: Mapped[list["ToolInvocation"]] = relationship(back_populates="run_step")
