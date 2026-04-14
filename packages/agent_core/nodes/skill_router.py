"""Skill router node — matches user task to the best skill before planning."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.agent_core.state import AgentState
from packages.skill_engine.loader import SkillLoader
from packages.skill_engine.registry import SkillRegistry
from packages.skill_engine.router import SkillRouter

# Module-level singletons (initialised on first call)
_registry: SkillRegistry | None = None
_router: SkillRouter | None = None
_loader: SkillLoader | None = None

SKILLS_ROOT = Path(__file__).resolve().parents[3] / "skills"


def _ensure_init() -> tuple[SkillRouter, SkillLoader]:
    global _registry, _router, _loader
    if _registry is None:
        _registry = SkillRegistry()
        _registry.scan(SKILLS_ROOT)
        _router = SkillRouter(_registry)
        _loader = SkillLoader()
    assert _router is not None and _loader is not None
    return _router, _loader


async def skill_router_node(state: AgentState) -> dict[str, Any]:
    """Match the task description to a skill and inject its context into state."""
    router, loader = _ensure_init()

    task = state.get("task_description", "")
    if not task:
        return {}

    matches = router.route(task, top_k=1)
    if not matches:
        return {
            "skill_name": None,
            "skill_context": None,
            "skill_input": None,
            "current_node": "skill_router",
            "steps_log": state.get("steps_log", []) + [
                {"node": "skill_router", "status": "no_match", "detail": "No matching skill found"}
            ],
        }

    best = matches[0]
    context = loader.load(best.manifest)

    return {
        "skill_name": best.name,
        "skill_context": context.to_dict(),
        "skill_input": {},
        "current_node": "skill_router",
        "steps_log": state.get("steps_log", []) + [
            {
                "node": "skill_router",
                "status": "matched",
                "detail": f"Matched skill: {best.manifest.display_name} (score={best.score:.1f})",
                "skill": best.name,
                "score": best.score,
            }
        ],
    }
