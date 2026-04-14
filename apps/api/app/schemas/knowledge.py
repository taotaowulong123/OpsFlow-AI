import uuid
from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: uuid.UUID
    filename: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChunkResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    content: str
    chunk_index: int
    metadata_: dict | None = None

    model_config = {"from_attributes": True}


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    content: str
    score: float
    document_name: str
    chunk_index: int
