"""Skill manifest parser — reads SKILL.yaml + supporting files into a structured object."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class SkillManifest:
    name: str
    display_name: str
    description: str
    version: str = "0.1.0"
    category: str = "domain"  # domain | action | guardrail | composite
    triggers: list[str] = field(default_factory=list)
    input_schema: dict = field(default_factory=dict)
    tools_allow: list[str] = field(default_factory=list)
    knowledge_scope: dict = field(default_factory=dict)
    graph_type: str = "langgraph"
    graph_entry: str = ""
    approval_required_for: list[str] = field(default_factory=list)
    output_schema: dict = field(default_factory=dict)
    risk_level: str = "low"  # low | medium | high
    prompt_template: str = ""
    eval_cases: list[dict] = field(default_factory=list)
    # Internal
    skill_dir: Path | None = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "triggers": self.triggers,
            "input_schema": self.input_schema,
            "tools_allow": self.tools_allow,
            "knowledge_scope": self.knowledge_scope,
            "graph_type": self.graph_type,
            "graph_entry": self.graph_entry,
            "approval_required_for": self.approval_required_for,
            "output_schema": self.output_schema,
            "risk_level": self.risk_level,
        }


def load_manifest(skill_dir: Path) -> SkillManifest:
    """Load a SkillManifest from a skill directory containing SKILL.yaml."""
    manifest_path = skill_dir / "SKILL.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No SKILL.yaml in {skill_dir}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    # Read optional supporting files
    prompt_template = ""
    prompt_path = skill_dir / "prompt.md"
    if prompt_path.exists():
        prompt_template = prompt_path.read_text(encoding="utf-8")

    output_schema: dict = {}
    schema_path = skill_dir / "output_schema.json"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            output_schema = json.load(f)

    eval_cases: list[dict] = []
    evals_path = skill_dir / "evals.yaml"
    if evals_path.exists():
        with open(evals_path, "r", encoding="utf-8") as f:
            evals_raw = yaml.safe_load(f)
            eval_cases = evals_raw.get("cases", []) if evals_raw else []

    approval_required_for: list[str] = raw.get("approval", {}).get("required_for", [])
    approval_path = skill_dir / "approval_policy.yaml"
    if approval_path.exists():
        with open(approval_path, "r", encoding="utf-8") as f:
            ap = yaml.safe_load(f)
            approval_required_for = ap.get("required_for", approval_required_for)

    tools_cfg = raw.get("tools", {})
    tools_allow = tools_cfg.get("allow", []) if isinstance(tools_cfg, dict) else []

    ks = raw.get("knowledge_scope", {})
    graph_cfg = raw.get("graph", {})

    return SkillManifest(
        name=raw["name"],
        display_name=raw.get("display_name", raw["name"]),
        description=raw.get("description", ""),
        version=raw.get("version", "0.1.0"),
        category=raw.get("category", "domain"),
        triggers=raw.get("triggers", []),
        input_schema=raw.get("input_schema", {}),
        tools_allow=tools_allow,
        knowledge_scope=ks if isinstance(ks, dict) else {},
        graph_type=graph_cfg.get("type", "langgraph") if isinstance(graph_cfg, dict) else "langgraph",
        graph_entry=graph_cfg.get("entry", "") if isinstance(graph_cfg, dict) else "",
        approval_required_for=approval_required_for,
        output_schema=output_schema,
        risk_level=raw.get("risk_level", "low"),
        prompt_template=prompt_template,
        eval_cases=eval_cases,
        skill_dir=skill_dir,
    )
