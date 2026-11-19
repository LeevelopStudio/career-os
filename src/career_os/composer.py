from __future__ import annotations

from copy import deepcopy
from typing import Any

from .achievements import rank_achievements
from .intelligence import analyze_job


def compose_targeted_resume(
    documents: dict[str, Any],
    job_description: str,
    profile_id: str | None = None,
    max_highlights: int = 4,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Select and order existing highlights; never generate career claims.

    Every retained highlight is copied verbatim from the source. Experiences
    remain in the original profile-selected order and are never fabricated.
    """
    if max_highlights < 1:
        raise ValueError("max_highlights must be at least 1")
    result = deepcopy(documents)
    analysis = analyze_job(documents, job_description)
    ranked = rank_achievements(documents, analysis, profile_id)
    by_experience: dict[str, list[Any]] = {}
    for achievement in ranked:
        by_experience.setdefault(achievement.experience_id, []).append(achievement)

    selection = []
    for experience in result.get("experience", {}).get("experiences", []):
        original = experience.get("highlights", [])
        if not isinstance(original, list):
            continue
        ranked_for_experience = by_experience.get(experience.get("id", ""), [])
        indices = [item.highlight_index for item in ranked_for_experience[:max_highlights]]
        # Preserve a representative fallback when a vacancy has no keyword evidence.
        if not indices:
            indices = list(range(min(len(original), max_highlights)))
        experience["highlights"] = [original[index] for index in indices]
        selection.append({
            "experience_id": experience.get("id"),
            "selected_highlight_indices": indices,
            "matched_requirements": sorted({
                requirement for item in ranked_for_experience[:max_highlights]
                for requirement in item.matched_requirements
            }),
            "fallback": not bool(ranked_for_experience),
        })
    report = {
        "coverage": round(analysis.coverage, 4),
        "detected_requirements": [item.skill for item in analysis.requirements],
        "missing_evidence": [item.skill for item in analysis.missing],
        "selection": selection,
        "policy": "Verbatim career evidence only; no generated achievements.",
    }
    return result, report
