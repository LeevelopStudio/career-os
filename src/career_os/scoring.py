from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .intelligence import JobAnalysis


@dataclass(frozen=True)
class EvidenceScore:
    experience_id: str
    matched_skills: tuple[str, ...]
    score: float


def score_experiences(
    documents: dict[str, Any],
    analysis: JobAnalysis,
    profile_id: str | None = None,
) -> list[EvidenceScore]:
    required = {item.skill for item in analysis.requirements}
    if not required:
        return []

    target = documents.get("target_profiles", {}).get(profile_id, {}) if profile_id else {}
    primary = set(target.get("emphasis", {}).get("primary", []))
    secondary = set(target.get("emphasis", {}).get("secondary", []))
    preferred = target.get("preferred_experience_order", [])
    rank = {experience_id: index for index, experience_id in enumerate(preferred)}

    scored: list[EvidenceScore] = []
    for index, item in enumerate(documents.get("experience", {}).get("experiences", [])):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            continue
        matched = tuple(skill for skill in item.get("skills", []) if skill in required)
        if not matched:
            continue

        points = 0.0
        for skill in matched:
            points += 3.0 if skill in primary else 2.0 if skill in secondary else 1.0
        if item.get("current"):
            points += 0.5
        profile_rank = rank.get(item["id"])
        if profile_rank is not None:
            points += max(0.0, 0.5 - profile_rank * 0.05)

        scored.append(EvidenceScore(item["id"], matched, round(points, 2)))

    original = {
        item.get("id"): index
        for index, item in enumerate(documents.get("experience", {}).get("experiences", []))
        if isinstance(item, dict)
    }
    return sorted(
        scored,
        key=lambda item: (-item.score, original.get(item.experience_id, 10_000)),
    )
