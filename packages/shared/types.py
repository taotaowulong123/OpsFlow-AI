import enum
from dataclasses import dataclass, field
from typing import Any


class TaskStatus(str, enum.Enum):
    pending = "pending"
    planning = "planning"
    retrieving = "retrieving"
    executing = "executing"
    reviewing = "reviewing"
    waiting_approval = "waiting_approval"
    completed = "completed"
    failed = "failed"


class NodeName(str, enum.Enum):
    planner = "planner"
    retriever = "retriever"
    executor = "executor"
    reviewer = "reviewer"
    approver = "approver"


@dataclass
class StepEvent:
    node_name: str
    status: str
    input_data: dict[str, Any] = field(default_factory=dict)
    output_data: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    tokens_used: int = 0
    latency_ms: int = 0
