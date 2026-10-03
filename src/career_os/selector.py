from __future__ import annotations

from typing import Any


def select_experiences(documents: dict[str, Any], profile_id: str | None = None) -> list[dict[str, Any]]:
    experiences = list(documents.get("experience", {}).get("experiences", []))
    if not profile_id:
        return experiences

    target = documents.get("target_profiles", {}).get(profile_id)
    if not target:
        raise ValueError(f"Unknown target profile: {profile_id}")

    preferred = target.get("preferred_experience_order", [])
    rank = {experience_id: index for index, experience_id in enumerate(preferred)}
    original = {item.get("id"): index for index, item in enumerate(experiences)}
    return sorted(
        experiences,
        key=lambda item: (
            rank.get(item.get("id"), len(rank)),
            original.get(item.get("id"), len(experiences)),
        ),
    )


def selected_skills(documents: dict[str, Any], experiences: list[dict[str, Any]], profile_id: str | None = None) -> list[str]:
    evidence = {skill for item in experiences for skill in item.get("skills", [])}
    if not profile_id:
        return sorted(evidence)

    target = documents.get("target_profiles", {}).get(profile_id, {})
    priorities = target.get("emphasis", {}).get("primary", []) + target.get("emphasis", {}).get("secondary", [])
    selected = [skill for skill in priorities if skill in evidence]
    selected.extend(sorted(evidence - set(selected)))
    return selected
