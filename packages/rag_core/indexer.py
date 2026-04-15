from typing import Any

from langchain_openai import OpenAIEmbeddings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from packages.rag_core.chunker import chunk_document


class DocumentIndexer:
    """Chunks documents, generates embeddings, and stores them in the DB."""

    def __init__(self, embedding_model: str | None = None):
        self._embeddings = OpenAIEmbeddings(
            model=embedding_model or settings.EMBEDDING_MODEL,
            api_key=settings.EMBEDDING_API_KEY or settings.OPENAI_API_KEY,
            base_url=settings.EMBEDDING_BASE_URL or settings.OPENAI_BASE_URL,
        )

    async def index_document(
        self,
        doc_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
        db_session: AsyncSession | None = None,
    ) -> int:
        """Chunk the document, embed each chunk, and store in DB.

        Returns the number of chunks indexed.
        """
        chunks = chunk_document(content, metadata=metadata or {})
        if not chunks:
            return 0

        texts = [c["content"] for c in chunks]
        embeddings = await self._embeddings.aembed_documents(texts)

        if db_session is not None:
            for chunk, embedding in zip(chunks, embeddings):
                await db_session.execute(
                    text(
                        "INSERT INTO document_chunks (id, document_id, content, chunk_index, metadata, embedding) "
                        "VALUES (gen_random_uuid(), :doc_id, :content, :chunk_index, :metadata, :embedding)"
                    ),
                    {
                        "doc_id": doc_id,
                        "content": chunk["content"],
                        "chunk_index": chunk["chunk_index"],
                        "metadata": str(chunk.get("metadata", {})),
                        "embedding": str(embedding),
                    },
                )
            await db_session.commit()

        return len(chunks)
