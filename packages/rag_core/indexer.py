import os
from typing import Any

from langchain_openai import OpenAIEmbeddings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from packages.rag_core.chunker import chunk_document


class DocumentIndexer:
    """Chunks documents, generates embeddings, and stores them in the DB."""

    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self._embeddings = OpenAIEmbeddings(
            model=embedding_model,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
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
