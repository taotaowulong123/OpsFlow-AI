import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ToolType(str, enum.Enum):
    sql = "sql"
    http = "http"
    browser = "browser"
    file = "file"


class RiskLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Tool(Base):
    __tablename__ = "tools"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool_type: Mapped[ToolType] = mapped_column(Enum(ToolType))
    schema_def: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.low)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    invocations: Mapped[list["ToolInvocation"]] = relationship(back_populates="tool")


class ToolInvocation(Base):
    __tablename__ = "tool_invocations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_step_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("run_steps.id", ondelete="CASCADE"))
    tool_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tools.id", ondelete="CASCADE"))
    input_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    output_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    run_step = relationship("RunStep", back_populates="tool_invocations")
    tool: Mapped["Tool"] = relationship(back_populates="invocations")
