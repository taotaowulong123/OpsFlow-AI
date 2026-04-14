"""Skill executor — runs a skill through its LangGraph subgraph."""

from __future__ import annotations

import time
from typing import Any

from packages.skill_engine.loader import SkillContext


class SkillExecutor:
    """Execute a skill by injecting its context into the agent state."""

    async def execute(
        self,
        context: SkillContext,
        user_input: str,
        skill_input: dict[str, Any] | None = None,
        graph_runner: Any = None,
    ) -> dict[str, Any]:
        """Run the skill and return structured output.

        Parameters
        ----------
        context:      Loaded skill context.
        user_input:   Original user task description.
        skill_input:  Parsed input matching the skill's input_schema.
        graph_runner: A compiled LangGraph that accepts an initial state dict.
                      If *None* a stub result is returned (useful for testing).
        """
        start = time.time()

        initial_state: dict[str, Any] = {
            "task_description": user_input,
            "skill_name": context.skill_name,
            "skill_context": context.to_dict(),
            "skill_input": skill_input or {},
            "plan": [],
            "retrieved_docs": [],
            "tool_results": [],
            "steps_log": [],
            "needs_approval": False,
            "approval_status": "",
            "error": None,
        }

        if graph_runner is not None:
            result_state = await graph_runner.ainvoke(initial_state)
        else:
            # Stub for testing without a real graph
            result_state = {
                **initial_state,
                "final_output": f"[stub] Skill '{context.skill_name}' executed for: {user_input}",
            }

        duration_ms = (time.time() - start) * 1000

        return {
            "skill_name": context.skill_name,
            "status": "failed" if result_state.get("error") else "completed",
            "output": result_state.get("final_output", ""),
            "steps_log": result_state.get("steps_log", []),
            "tool_results": result_state.get("tool_results", []),
            "retrieved_docs": result_state.get("retrieved_docs", []),
            "needs_approval": result_state.get("needs_approval", False),
            "approval_status": result_state.get("approval_status", ""),
            "error": result_state.get("error"),
            "duration_ms": duration_ms,
        }
