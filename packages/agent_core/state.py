from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    task_id: str
    task_description: str
    plan: list[dict[str, Any]]
    retrieved_docs: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]
    review_result: dict[str, Any]
    needs_approval: bool
    approval_status: str
    current_node: str
    steps_log: list[dict[str, Any]]
    final_output: str
    error: str | None
    # Skill fields
    skill_name: str | None
    skill_context: dict[str, Any] | None
    skill_input: dict[str, Any] | None
