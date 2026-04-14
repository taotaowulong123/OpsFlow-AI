import time
from typing import Any

from packages.agent_core.state import AgentState
from packages.shared.types import NodeName, TaskStatus


async def approver_node(state: AgentState) -> dict[str, Any]:
    start = time.perf_counter()
    approval_status = state.get("approval_status", "")

    # If already decided, just pass through
    if approval_status in ("approved", "rejected"):
        latency_ms = int((time.perf_counter() - start) * 1000)
        step_log = {
            "node_name": NodeName.approver,
            "status": TaskStatus.completed if approval_status == "approved" else TaskStatus.failed,
            "latency_ms": latency_ms,
        }
        error = "Task rejected by approver." if approval_status == "rejected" else None
        return {
            "current_node": NodeName.approver,
            "steps_log": state.get("steps_log", []) + [step_log],
            "error": error,
        }

    # Pause for human approval — set status to pending
    step_log = {
        "node_name": NodeName.approver,
        "status": TaskStatus.waiting_approval,
        "latency_ms": 0,
    }

    return {
        "current_node": NodeName.approver,
        "approval_status": "pending",
        "steps_log": state.get("steps_log", []) + [step_log],
    }
