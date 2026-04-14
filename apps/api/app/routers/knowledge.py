import uuid

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.knowledge import Document, DocumentChunk
from app.schemas.knowledge import DocumentResponse, SearchRequest, SearchResult

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document(file: UploadFile, db: AsyncSession = Depends(get_db)):
    import os
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    doc = Document(
        filename=file.filename,
        file_type=file.content_type or "unknown",
        file_size=len(content),
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


@router.get("/documents", response_model=list[DocumentResponse])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).order_by(Document.created_at.desc()))
    return result.scalars().all()


@router.delete("/documents/{doc_id}", status_code=204)
async def delete_document(doc_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    doc = await db.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(doc)
    await db.commit()


@router.post("/search", response_model=list[SearchResult])
async def search_knowledge(body: SearchRequest, db: AsyncSession = Depends(get_db)):
    # Placeholder: integrate vector similarity search here
    result = await db.execute(
        select(DocumentChunk)
        .join(Document)
        .filter(DocumentChunk.content.ilike(f"%{body.query}%"))
        .limit(body.top_k)
    )
    chunks = result.scalars().all()
    return [
        SearchResult(
            content=c.content,
            score=1.0,
            document_name=(await db.get(Document, c.document_id)).filename,
            chunk_index=c.chunk_index,
        )
        for c in chunks
    ]
