from typing import Any


def chunk_document(
    content: str,
    chunk_size: int = 500,
    overlap: int = 50,
    metadata: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Split content into overlapping chunks. Supports plain text and markdown."""
    if not content:
        return []

    meta = metadata or {}
    chunks: list[dict[str, Any]] = []

    # Try markdown splitting first: split on headings
    if content.startswith("#") or "\n#" in content:
        sections = _split_markdown(content)
    else:
        sections = [content]

    chunk_index = 0
    for section in sections:
        # Further split each section by chunk_size with overlap
        start = 0
        while start < len(section):
            end = start + chunk_size
            chunk_text = section[start:end].strip()
            if chunk_text:
                chunks.append({
                    "content": chunk_text,
                    "chunk_index": chunk_index,
                    "metadata": meta,
                })
                chunk_index += 1
            start += chunk_size - overlap

    return chunks


def _split_markdown(content: str) -> list[str]:
    """Split markdown by headings, keeping heading with its content."""
    lines = content.split("\n")
    sections: list[str] = []
    current: list[str] = []

    for line in lines:
        if line.startswith("#") and current:
            sections.append("\n".join(current))
            current = [line]
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current))

    return sections
