import os
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from packages.rag_core.indexer import DocumentIndexer


async def process_document(
    doc_id: str,
    file_path: str,
    db_session: AsyncSession,
) -> dict[str, Any]:
    """Read a file, chunk it, index it, and update document status."""
    ext = os.path.splitext(file_path)[1].lower()
    supported = {".txt", ".md", ".pdf", ".docx"}

    if ext not in supported:
        await _update_status(db_session, doc_id, "failed")
        return {"success": False, "error": f"Unsupported file type: {ext}"}

    try:
        content = _read_file(file_path, ext)
    except Exception as exc:
        await _update_status(db_session, doc_id, "failed")
        return {"success": False, "error": str(exc)}

    if not content.strip():
        await _update_status(db_session, doc_id, "failed")
        return {"success": False, "error": "Empty document."}

    await _update_status(db_session, doc_id, "processing")

    indexer = DocumentIndexer()
    metadata = {"filename": os.path.basename(file_path), "file_type": ext}
    num_chunks = await indexer.index_document(doc_id, content, metadata=metadata, db_session=db_session)

    await _update_status(db_session, doc_id, "indexed")
    return {"success": True, "chunks_indexed": num_chunks}


def _read_file(file_path: str, ext: str) -> str:
    if ext in (".txt", ".md"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    if ext == ".pdf":
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            raise RuntimeError("PyPDF2 is required for PDF processing.")

    if ext == ".docx":
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            raise RuntimeError("python-docx is required for DOCX processing.")

    return ""


async def _update_status(db_session: AsyncSession, doc_id: str, status: str) -> None:
    await db_session.execute(
        text("UPDATE documents SET status = :status WHERE id = :doc_id"),
        {"status": status, "doc_id": doc_id},
    )
    await db_session.commit()
