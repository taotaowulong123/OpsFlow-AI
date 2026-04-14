import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    Vector = None


class DocumentStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    indexed = "indexed"
    failed = "failed"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50))
    file_size: Mapped[int] = mapped_column(Integer)
    status: Mapped[DocumentStatus] = mapped_column(Enum(DocumentStatus), default=DocumentStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    embedding = mapped_column(Vector(1536), nullable=True) if Vector else mapped_column(JSON, nullable=True)

    document: Mapped["Document"] = relationship(back_populates="chunks")
