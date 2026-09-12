from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from .model import Credential, Education, Experience, ProfileData


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


def _collect_model_errors(prefix: str, model_type, payload: dict[str, Any]) -> list[ValidationIssue]:
    try:
        model_type.model_validate(payload)
        return []
    except ValidationError as exc:
        issues: list[ValidationIssue] = []
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"])
            path = f"{prefix}.{location}" if location else prefix
            issues.append(ValidationIssue(path=path, message=error["msg"]))
        return issues


def _duplicate_id_issues(prefix: str, records: list[dict[str, Any]]) -> list[ValidationIssue]:
    seen: set[str] = set()
    issues: list[ValidationIssue] = []
    for index, record in enumerate(records):
        value = record.get("id")
        if isinstance(value, str):
            if value in seen:
                issues.append(ValidationIssue(f"{prefix}[{index}].id", f"duplicate id '{value}'"))
            seen.add(value)
    return issues


def validate_career(documents: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    profile_doc = documents.get("profile", {})
    profile = profile_doc.get("profile")
    if not isinstance(profile, dict):
        issues.append(ValidationIssue("profile", "missing profile mapping"))
    else:
        issues.extend(_collect_model_errors("profile", ProfileData, profile))

    experience_doc = documents.get("experience", {})
    experiences = experience_doc.get("experiences", [])
    if not isinstance(experiences, list):
        issues.append(ValidationIssue("experiences", "must be a list"))
    else:
        issues.extend(_duplicate_id_issues("experiences", experiences))
        for index, item in enumerate(experiences):
            if not isinstance(item, dict):
                issues.append(ValidationIssue(f"experiences[{index}]", "must be a mapping"))
                continue
            issues.extend(_collect_model_errors(f"experiences[{index}]", Experience, item))

    education_doc = documents.get("education", {})
    education = education_doc.get("education", [])
    if not isinstance(education, list):
        issues.append(ValidationIssue("education", "must be a list"))
    else:
        issues.extend(_duplicate_id_issues("education", education))
        for index, item in enumerate(education):
            if not isinstance(item, dict):
                issues.append(ValidationIssue(f"education[{index}]", "must be a mapping"))
                continue
            issues.extend(_collect_model_errors(f"education[{index}]", Education, item))

    certification_doc = documents.get("certifications", {})
    credentials = certification_doc.get("certifications", [])
    if not isinstance(credentials, list):
        issues.append(ValidationIssue("certifications", "must be a list"))
    else:
        issues.extend(_duplicate_id_issues("certifications", credentials))
        for index, item in enumerate(credentials):
            if not isinstance(item, dict):
                issues.append(ValidationIssue(f"certifications[{index}]", "must be a mapping"))
                continue
            issues.extend(_collect_model_errors(f"certifications[{index}]", Credential, item))

    return issues
