"""Skill loader — progressive disclosure: loads full skill context only when selected."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.skill_engine.manifest import SkillManifest


@dataclass
class SkillContext:
    """Everything the agent needs to execute a specific skill."""
    skill_name: str
    display_name: str
    description: str
    category: str
    risk_level: str
    prompt_template: str
    tools_allow: list[str] = field(default_factory=list)
    knowledge_collections: list[str] = field(default_factory=list)
    input_schema: dict = field(default_factory=dict)
    output_schema: dict = field(default_factory=dict)
    approval_required_for: list[str] = field(default_factory=list)
    graph_entry: str = ""
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_name": self.skill_name,
            "display_name": self.display_name,
            "description": self.description,
            "category": self.category,
            "risk_level": self.risk_level,
            "prompt_template": self.prompt_template,
            "tools_allow": self.tools_allow,
            "knowledge_collections": self.knowledge_collections,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "approval_required_for": self.approval_required_for,
            "graph_entry": self.graph_entry,
        }


class SkillLoader:
    """Loads a SkillManifest into a full SkillContext for execution."""

    def load(self, manifest: SkillManifest) -> SkillContext:
        ks = manifest.knowledge_scope
        collections = ks.get("collections", []) if isinstance(ks, dict) else []

        return SkillContext(
            skill_name=manifest.name,
            display_name=manifest.display_name,
            description=manifest.description,
            category=manifest.category,
            risk_level=manifest.risk_level,
            prompt_template=manifest.prompt_template,
            tools_allow=manifest.tools_allow,
            knowledge_collections=collections,
            input_schema=manifest.input_schema,
            output_schema=manifest.output_schema,
            approval_required_for=manifest.approval_required_for,
            graph_entry=manifest.graph_entry,
        )
