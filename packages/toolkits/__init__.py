from typing import Any

from packages.toolkits.base import BaseTool
from packages.toolkits.browser_tool import BrowserTool
from packages.toolkits.file_tool import FileTool
from packages.toolkits.http_tool import HTTPTool
from packages.toolkits.sql_tool import SQLTool

_TOOLS: dict[str, BaseTool] = {
    "sql_query": SQLTool(),
    "http_request": HTTPTool(),
    "browser_action": BrowserTool(),
    "file_generate": FileTool(),
}


def get_tool_by_name(name: str) -> BaseTool | None:
    return _TOOLS.get(name)


__all__ = ["BaseTool", "SQLTool", "HTTPTool", "BrowserTool", "FileTool", "get_tool_by_name"]
