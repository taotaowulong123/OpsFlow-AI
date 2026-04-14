from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    name: str = ""
    description: str = ""
    risk_level: str = "low"

    @abstractmethod
    async def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        ...
