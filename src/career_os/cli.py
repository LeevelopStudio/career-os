from __future__ import annotations
import argparse
from pathlib import Path
import sys
from .loader import CareerLoadError, load_career
from .renderer import write_resume
from .validator import validate_career

def _print_issues(issues):
    print("CareerOS validation\n")
    for issue in issues: print(f"✗ {issue.path}: {issue.message}")
    print(f"\nValidation failed: {len(issues)} issue(s).")

def validate_command(root: Path)->int:
    try: documents=load_career(root)
    except CareerLoadError as exc: print(f"✗ {exc}",file=sys.stderr); return 2
    issues=validate_career(documents)
    if issues: _print_issues(issues); return 1
    print("✓ Career data is valid."); return 0

def build_command(root:Path,output:Path,profile:str|None,format:str|None)->int:
    try: documents=load_career(root)
    except CareerLoadError as exc: print(f"✗ {exc}",file=sys.stderr); return 2
    issues=validate_career(documents)
    if issues: _print_issues(issues); return 1
    try: generated=write_resume(documents,output,profile_id=profile,format=format)
    except ValueError as exc: print(f"✗ {exc}",file=sys.stderr); return 2
    print(f"✓ Generated {generated}"); return 0

def _parser():
    parser=argparse.ArgumentParser(prog="career",description="CareerOS command-line interface"); sub=parser.add_subparsers(dest="command",required=True)
    v=sub.add_parser("validate",help="Validate CareerOS source data"); v.add_argument("--root",default=".",type=Path)
    b=sub.add_parser("build",help="Generate career artifacts"); b.add_argument("artifact",choices=["resume"]); b.add_argument("--root",default=".",type=Path); b.add_argument("--profile"); b.add_argument("--format",choices=["md","html","pdf","docx"]); b.add_argument("--output",default=Path("generated/resume-ats-en.md"),type=Path)
    return parser

def main():
    args=_parser().parse_args()
    if args.command=="validate": raise SystemExit(validate_command(args.root))
    if args.command=="build": raise SystemExit(build_command(args.root,args.output,args.profile,args.format))
    raise SystemExit(2)

if __name__=="__main__": main()
