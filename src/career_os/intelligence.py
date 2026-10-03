from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

TOKEN_RE = re.compile(r"[a-z0-9+#.]+")
STOPWORDS = {
    "and","the","with","for","from","that","this","you","your","our","are","will",
    "have","has","into","using","use","work","working","experience","knowledge",
    "skills","skill","strong","senior","engineer","engineering","software",
}


@dataclass(frozen=True)
class JobRequirement:
    skill: str
    evidence_experience_ids: tuple[str, ...]

    @property
    def matched(self) -> bool:
        return bool(self.evidence_experience_ids)


@dataclass(frozen=True)
class JobAnalysis:
    requirements: tuple[JobRequirement, ...]
    coverage: float

    @property
    def matched(self) -> tuple[JobRequirement, ...]:
        return tuple(item for item in self.requirements if item.matched)

    @property
    def missing(self) -> tuple[JobRequirement, ...]:
        return tuple(item for item in self.requirements if not item.matched)


def _normalize(value: str) -> str:
    return " ".join(TOKEN_RE.findall(value.casefold()))


def _contains_term(text: str, term: str) -> bool:
    normalized_term = _normalize(term)
    if not normalized_term:
        return False
    if " " in normalized_term:
        return normalized_term in text
    return normalized_term in set(text.split())


def extract_skill_requirements(documents: dict[str, Any], description: str) -> list[str]:
    text = _normalize(description)
    found: list[tuple[int, str]] = []
    for skill in documents.get("skills", {}).get("skills", []):
        if not isinstance(skill, dict) or not isinstance(skill.get("name"), str):
            continue
        terms = [skill["name"], *skill.get("aliases", [])]
        positions = []
        for term in terms:
            normalized = _normalize(str(term))
            if normalized and _contains_term(text, normalized):
                positions.append(text.find(normalized))
        if positions:
            found.append((min(positions), skill["name"]))
    found.sort(key=lambda item: (item[0], item[1].casefold()))
    return [name for _, name in found]


def analyze_job(documents: dict[str, Any], description: str) -> JobAnalysis:
    required = extract_skill_requirements(documents, description)
    experiences = documents.get("experience", {}).get("experiences", [])
    requirements: list[JobRequirement] = []
    for skill in required:
        evidence = tuple(
            item["id"]
            for item in experiences
            if isinstance(item, dict)
            and isinstance(item.get("id"), str)
            and skill in item.get("skills", [])
        )
        requirements.append(JobRequirement(skill=skill, evidence_experience_ids=evidence))
    coverage = (len([item for item in requirements if item.matched]) / len(requirements)) if requirements else 0.0
    return JobAnalysis(requirements=tuple(requirements), coverage=coverage)


def analysis_as_dict(analysis: JobAnalysis) -> dict[str, Any]:
    return {
        "coverage": round(analysis.coverage, 4),
        "requirements": [
            {
                "skill": item.skill,
                "matched": item.matched,
                "evidence_experience_ids": list(item.evidence_experience_ids),
            }
            for item in analysis.requirements
        ],
        "missing": [item.skill for item in analysis.missing],
    }
