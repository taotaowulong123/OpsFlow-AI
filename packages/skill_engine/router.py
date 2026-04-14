"""Skill router — matches a user query to the most relevant skill(s)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from packages.skill_engine.manifest import SkillManifest
from packages.skill_engine.registry import SkillRegistry


@dataclass
class SkillMatch:
    name: str
    score: float
    manifest: SkillManifest


class SkillRouter:
    def __init__(self, registry: SkillRegistry) -> None:
        self._registry = registry

    def route(self, query: str, top_k: int = 3) -> list[SkillMatch]:
        """Return up to *top_k* skills ranked by relevance to *query*."""
        query_lower = query.lower()
        query_tokens = set(re.findall(r"\w+", query_lower))

        matches: list[SkillMatch] = []
        for skill in self._registry.list_skills():
            score = self._score(query_lower, query_tokens, skill)
            if score > 0:
                matches.append(SkillMatch(name=skill.name, score=score, manifest=skill))

        matches.sort(key=lambda m: m.score, reverse=True)
        return matches[:top_k]

    # ------------------------------------------------------------------
    @staticmethod
    def _score(query_lower: str, query_tokens: set[str], skill: SkillManifest) -> float:
        score = 0.0

        # Trigger keyword matching (highest weight)
        for trigger in skill.triggers:
            trigger_l = trigger.lower()
            if trigger_l in query_lower:
                score += 10.0
            else:
                trigger_tokens = set(re.findall(r"\w+", trigger_l))
                overlap = query_tokens & trigger_tokens
                if overlap:
                    score += 3.0 * len(overlap) / max(len(trigger_tokens), 1)

        # Description token overlap
        desc_tokens = set(re.findall(r"\w+", skill.description.lower()))
        desc_overlap = query_tokens & desc_tokens
        if desc_overlap:
            score += 1.0 * len(desc_overlap) / max(len(desc_tokens), 1)

        # Category bonus for common keywords
        category_hints = {
            "domain": {"分析", "analyze", "analysis", "查询", "query", "检索", "search"},
            "action": {"生成", "generate", "创建", "create", "填写", "fill", "提交", "submit"},
            "guardrail": {"检查", "check", "审计", "audit", "验证", "validate"},
        }
        for cat, hints in category_hints.items():
            if skill.category == cat and query_tokens & hints:
                score += 1.5

        return score
