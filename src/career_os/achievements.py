from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from .intelligence import JobAnalysis


@dataclass(frozen=True)
class AchievementScore:
    experience_id: str
    highlight_index: int
    text: str
    matched_requirements: tuple[str, ...]
    score: float
    reasons: tuple[str, ...]


def _mentions(text: str, term: str) -> bool:
    # Match whole skill names, including punctuation-bearing names like Node.js.
    escaped = re.escape(term.casefold())
    return re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", text.casefold()) is not None


def rank_achievements(
    documents: dict[str, Any],
    analysis: JobAnalysis,
    profile_id: str | None = None,
) -> list[AchievementScore]:
    """Rank existing achievement text; never synthesize or rewrite a claim.

    Experience-level skills supply *context*, not proof that a specific highlight
    demonstrates every skill listed for its parent experience.
    """
    target = documents.get("target_profiles", {}).get(profile_id, {}) if profile_id else {}
    emphasis = target.get("emphasis", {})
    primary = set(emphasis.get("primary", []))
    secondary = set(emphasis.get("secondary", []))
    catalog = {
        item["name"]: [item["name"], *item.get("aliases", [])]
        for item in documents.get("skills", {}).get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    required = [item.skill for item in analysis.requirements]
    ranked: list[AchievementScore] = []

    for experience in documents.get("experience", {}).get("experiences", []):
        if not isinstance(experience, dict) or not isinstance(experience.get("id"), str):
            continue
        highlights = experience.get("highlights", [])
        if not isinstance(highlights, list):
            continue
        for index, highlight in enumerate(highlights):
            if not isinstance(highlight, str) or not highlight.strip():
                continue
            matches = tuple(
                skill for skill in required
                if any(_mentions(highlight, term) for term in catalog.get(skill, [skill]))
            )
            if not matches:
                continue
            score = sum(3 if skill in primary else 2 if skill in secondary else 1 for skill in matches)
            reasons = tuple(f"Explicitly mentions job requirement: {skill}" for skill in matches)
            ranked.append(AchievementScore(
                experience_id=experience["id"],
                highlight_index=index,
                text=highlight,
                matched_requirements=matches,
                score=float(score),
                reasons=reasons,
            ))
    return sorted(ranked, key=lambda item: (-item.score, item.experience_id, item.highlight_index))
