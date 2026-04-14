"""Skill registry — scans a directory for skill definitions and indexes them."""

from __future__ import annotations

from pathlib import Path

from packages.skill_engine.manifest import SkillManifest, load_manifest


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, SkillManifest] = {}

    # ------------------------------------------------------------------
    def scan(self, skills_root: Path) -> int:
        """Scan *skills_root* for subdirectories containing SKILL.yaml.
        Returns the number of skills loaded."""
        count = 0
        if not skills_root.is_dir():
            return count
        for child in sorted(skills_root.iterdir()):
            if child.is_dir() and (child / "SKILL.yaml").exists():
                try:
                    manifest = load_manifest(child)
                    self._skills[manifest.name] = manifest
                    count += 1
                except Exception:
                    continue
        return count

    def register(self, manifest: SkillManifest) -> None:
        self._skills[manifest.name] = manifest

    # ------------------------------------------------------------------
    def get_skill(self, name: str) -> SkillManifest | None:
        return self._skills.get(name)

    def list_skills(self) -> list[SkillManifest]:
        return list(self._skills.values())

    def get_skills_by_category(self, category: str) -> list[SkillManifest]:
        return [s for s in self._skills.values() if s.category == category]

    def get_enabled_summaries(self) -> list[dict]:
        """Return lightweight summaries for the skill router (progressive disclosure)."""
        return [
            {
                "name": s.name,
                "display_name": s.display_name,
                "description": s.description,
                "category": s.category,
                "triggers": s.triggers,
                "risk_level": s.risk_level,
            }
            for s in self._skills.values()
        ]
