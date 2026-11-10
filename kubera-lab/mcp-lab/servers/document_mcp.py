from __future__ import annotations

import re
from datetime import datetime, timezone

from mcp.server import MCPServer

from shared.policy import evidence_envelope

mcp = MCPServer("kubera-document-mcp")


def _bounded_text(text: str, *, limit: int = 200_000) -> str:
    if len(text) > limit:
        raise ValueError(f"document text exceeds {limit} characters")
    return text


@mcp.tool()
def fingerprint_document(text: str, source_name: str = "supplied_document") -> dict:
    """Create a stable evidence fingerprint for caller-supplied document text."""
    content = _bounded_text(text)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    return {
        "characters": len(content),
        "lines": content.count("\n") + 1 if content else 0,
        "evidence": evidence_envelope(
            source=source_name[:120] or "supplied_document",
            source_url=None,
            payload=content,
            retrieved_at=retrieved_at,
        ),
    }


@mcp.tool()
def find_exact_terms(text: str, terms: list[str]) -> dict:
    """Find exact case-insensitive terms in caller-supplied text without using an LLM."""
    content = _bounded_text(text)
    if len(terms) > 100:
        raise ValueError("Too many terms")
    lowered = content.lower()
    findings = []
    for raw in terms:
        term = str(raw).strip()
        if not term or len(term) > 200:
            continue
        starts = [m.start() for m in re.finditer(re.escape(term.lower()), lowered)]
        findings.append({"term": term, "count": len(starts), "positions": starts[:100],
                         "positions_truncated": len(starts) > 100})
    return {"findings": findings}


@mcp.tool()
def split_document_chunks(text: str, max_chars: int = 4000) -> dict:
    """Split caller-supplied text into bounded chunks for downstream analysis."""
    content = _bounded_text(text)
    if not 500 <= max_chars <= 20_000:
        raise ValueError("max_chars must be between 500 and 20000")
    chunks = [content[i : i + max_chars] for i in range(0, len(content), max_chars)]
    return {"chunk_count": len(chunks), "returned_chunks": min(len(chunks), 200),
            "truncated": len(chunks) > 200, "chunks": chunks[:200]}


@mcp.resource("kubera://document/policy")
def document_policy() -> str:
    return (
        "Document MCP starter works only with text explicitly supplied to the tool. It has no arbitrary filesystem access, "
        "does not upload documents externally and does not treat extraction as legal advice."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
