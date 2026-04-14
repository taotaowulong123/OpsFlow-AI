import csv
import io
import os
from typing import Any

from packages.toolkits.base import BaseTool

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "./uploads")


class FileTool(BaseTool):
    name = "file_generate"
    description = "Generate files such as markdown reports and CSV exports."
    risk_level = "low"

    async def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        action = params.get("action", "")
        filename = params.get("filename", "output")
        content = params.get("content", "")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        try:
            if action == "generate_markdown":
                filepath = os.path.join(UPLOAD_DIR, f"{filename}.md")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                return {"success": True, "file_path": filepath}

            elif action == "generate_csv":
                rows = params.get("rows", [])
                headers = params.get("headers", [])
                filepath = os.path.join(UPLOAD_DIR, f"{filename}.csv")

                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if headers:
                        writer.writerow(headers)
                    for row in rows:
                        writer.writerow(row if isinstance(row, list) else list(row.values()))
                return {"success": True, "file_path": filepath}

            else:
                return {"success": False, "error": f"Unknown action: {action}"}

        except Exception as exc:
            return {"success": False, "error": str(exc)}
