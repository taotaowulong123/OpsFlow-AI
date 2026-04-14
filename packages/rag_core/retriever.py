import os
from dataclasses import dataclass
from typing import Any

from langchain_openai import OpenAIEmbeddings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SearchResult:
    content: str
    source: str
    score: float
    chunk_index: int


class KnowledgeRetriever:
    """Retrieves relevant document chunks using pgvector similarity search."""

    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self._embeddings = OpenAIEmbeddings(
            model=embedding_model,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        db_session: AsyncSession | None = None,
    ) -> list[SearchResult]:
        """Embed the query and perform cosine similarity search."""
        if db_session is None:
            return []

        query_embedding = await self._embeddings.aembed_query(query)

        result = await db_session.execute(
            text(
                "SELECT dc.content, dc.chunk_index, d.filename, "
                "1 - (dc.embedding <=> :embedding::vector) AS score "
                "FROM document_chunks dc "
                "JOIN documents d ON d.id = dc.document_id "
                "ORDER BY dc.embedding <=> :embedding::vector "
                "LIMIT :top_k"
            ),
            {"embedding": str(query_embedding), "top_k": top_k},
        )

        rows = result.fetchall()
        return [
            SearchResult(
                content=row[0],
                source=row[1],
                score=float(row[3]),
                chunk_index=int(row[2]),
            )
            for row in rows
        ]
