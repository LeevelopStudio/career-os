from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape


def _environment() -> Environment:
    return Environment(
        loader=PackageLoader("career_os", "templates"),
        autoescape=select_autoescape(default_for_string=False, default=False),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_resume_markdown(documents: dict[str, Any]) -> str:
    template = _environment().get_template("resume-ats-en.md.j2")
    return template.render(
        profile=documents.get("profile", {}).get("profile", {}),
        experiences=documents.get("experience", {}).get("experiences", []),
        education=documents.get("education", {}).get("education", []),
        certifications=documents.get("certifications", {}).get("certifications", []),
        skills=documents.get("skills", {}).get("skills", {}),
    ).strip() + "\n"


def write_resume_markdown(documents: dict[str, Any], output: str | Path) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_resume_markdown(documents), encoding="utf-8")
    return output
