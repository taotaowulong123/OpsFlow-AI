from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from packages.toolkits.base import BaseTool


class SQLTool(BaseTool):
    name = "sql_query"
    description = "Execute read-only SQL queries against the database."
    risk_level = "medium"

    def __init__(self, db_session: AsyncSession | None = None):
        self._db_session = db_session

    async def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        query = params.get("query", "").strip()
        if not query:
            return {"success": False, "error": "No query provided."}

        # Only allow SELECT statements
        normalized = query.lstrip().upper()
        if not normalized.startswith("SELECT"):
            return {"success": False, "error": "Only SELECT queries are allowed."}

        forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"]
        for kw in forbidden:
            if kw in normalized:
                return {"success": False, "error": f"Forbidden keyword: {kw}"}

        if self._db_session is None:
            return {"success": False, "error": "No database session available."}

        try:
            result = await self._db_session.execute(text(query))
            columns = list(result.keys())
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            return {"success": True, "rows": rows, "row_count": len(rows)}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
