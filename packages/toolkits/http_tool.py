from typing import Any

import aiohttp

from packages.toolkits.base import BaseTool


class HTTPTool(BaseTool):
    name = "http_request"
    description = "Make HTTP requests to external APIs."
    risk_level = "low"

    async def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        url = params.get("url", "")
        method = params.get("method", "GET").upper()
        headers = params.get("headers", {})
        body = params.get("body")

        if not url:
            return {"success": False, "error": "No URL provided."}

        # Adjust risk dynamically
        self.risk_level = "low" if method == "GET" else "high"

        try:
            async with aiohttp.ClientSession() as session:
                kwargs: dict[str, Any] = {"headers": headers}
                if body and method in ("POST", "PUT", "PATCH"):
                    kwargs["json"] = body

                async with session.request(method, url, **kwargs) as resp:
                    response_body = await resp.text()
                    return {
                        "success": True,
                        "status_code": resp.status,
                        "headers": dict(resp.headers),
                        "body": response_body,
                    }
        except Exception as exc:
            return {"success": False, "error": str(exc)}
