from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class CareerLoadError(RuntimeError):
    pass


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CareerLoadError(f"Missing file: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise CareerLoadError(f"Invalid YAML in {path}: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise CareerLoadError(f"Expected a YAML mapping in {path}")
    return data


def load_career(root: str | Path) -> dict[str, Any]:
    root = Path(root).resolve()
    manifest_path = root / "career-os.yml"
    manifest = _read_yaml(manifest_path)
    source = manifest.get("source")
    if not isinstance(source, dict):
        raise CareerLoadError("career-os.yml must contain a 'source' mapping")

    documents: dict[str, Any] = {"manifest": manifest}
    for key, relative_path in source.items():
        if not isinstance(relative_path, str):
            raise CareerLoadError(f"source.{key} must be a path string")
        documents[key] = _read_yaml(root / relative_path)

    return documents
