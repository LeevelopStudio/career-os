from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .loader import CareerLoadError, load_career
from .renderer import write_resume_markdown
from .validator import validate_career


def _print_issues(issues) -> None:
    print("CareerOS validation")
    print()
    for issue in issues:
        print(f"✗ {issue.path}: {issue.message}")
    print()
    print(f"Validation failed: {len(issues)} issue(s).")


def validate_command(root: Path) -> int:
    try:
        documents = load_career(root)
    except CareerLoadError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        return 2

    issues = validate_career(documents)
    if issues:
        _print_issues(issues)
        return 1

    print("✓ Career data is valid.")
    return 0


def build_command(root: Path, output: Path) -> int:
    try:
        documents = load_career(root)
    except CareerLoadError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        return 2

    issues = validate_career(documents)
    if issues:
        _print_issues(issues)
        return 1

    generated = write_resume_markdown(documents, output)
    print(f"✓ Generated {generated}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="career", description="CareerOS command-line interface")
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate_parser = subcommands.add_parser("validate", help="Validate CareerOS source data")
    validate_parser.add_argument("--root", default=".", type=Path, help="Career repository root")

    build_parser = subcommands.add_parser("build", help="Generate career artifacts")
    build_parser.add_argument("artifact", choices=["resume"], help="Artifact to generate")
    build_parser.add_argument("--root", default=".", type=Path, help="Career repository root")
    build_parser.add_argument(
        "--output",
        default=Path("generated/resume-ats-en.md"),
        type=Path,
        help="Generated Markdown path",
    )

    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.command == "validate":
        raise SystemExit(validate_command(args.root))
    if args.command == "build":
        raise SystemExit(build_command(args.root, args.output))
    raise SystemExit(2)


if __name__ == "__main__":
    main()
