from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from .intelligence import analysis_as_dict, analyze_job
from .loader import CareerLoadError, load_career
from .renderer import write_resume
from .validator import validate_career

def _print_issues(issues):
    print("CareerOS validation\n")
    for issue in issues: print(f"✗ {issue.path}: {issue.message}")
    print(f"\nValidation failed: {len(issues)} issue(s).")

def _load_validated(root: Path):
    documents=load_career(root)
    issues=validate_career(documents)
    return documents,issues

def validate_command(root: Path)->int:
    try: documents,issues=_load_validated(root)
    except CareerLoadError as exc: print(f"✗ {exc}",file=sys.stderr); return 2
    if issues: _print_issues(issues); return 1
    print("✓ Career data is valid."); return 0

def build_command(root:Path,output:Path,profile:str|None,format:str|None)->int:
    try: documents,issues=_load_validated(root)
    except CareerLoadError as exc: print(f"✗ {exc}",file=sys.stderr); return 2
    if issues: _print_issues(issues); return 1
    try: generated=write_resume(documents,output,profile_id=profile,format=format)
    except ValueError as exc: print(f"✗ {exc}",file=sys.stderr); return 2
    print(f"✓ Generated {generated}"); return 0

def analyze_job_command(root:Path,job:Path,json_output:bool)->int:
    try: documents,issues=_load_validated(root)
    except CareerLoadError as exc: print(f"✗ {exc}",file=sys.stderr); return 2
    if issues: _print_issues(issues); return 1
    if not job.exists():
        print(f"✗ Missing job description: {job}",file=sys.stderr); return 2
    analysis=analyze_job(documents,job.read_text(encoding="utf-8"))
    if json_output:
        print(json.dumps(analysis_as_dict(analysis),indent=2))
        return 0
    print("CareerOS job analysis\n")
    if not analysis.requirements:
        print("No canonical skill requirements were detected.")
        return 0
    print(f"Evidence coverage: {analysis.coverage:.0%}\n")
    for item in analysis.requirements:
        if item.matched:
            print(f"✓ {item.skill}: {', '.join(item.evidence_experience_ids)}")
        else:
            print(f"○ {item.skill}: no verified career evidence")
    return 0

def _parser():
    parser=argparse.ArgumentParser(prog="career",description="CareerOS command-line interface"); sub=parser.add_subparsers(dest="command",required=True)
    v=sub.add_parser("validate",help="Validate CareerOS source data"); v.add_argument("--root",default=".",type=Path)
    b=sub.add_parser("build",help="Generate career artifacts"); b.add_argument("artifact",choices=["resume"]); b.add_argument("--root",default=".",type=Path); b.add_argument("--profile"); b.add_argument("--format",choices=["md","html","pdf","docx"]); b.add_argument("--output",default=Path("generated/resume-ats-en.md"),type=Path)
    a=sub.add_parser("analyze",help="Analyze external inputs against verified career evidence")
    a_sub=a.add_subparsers(dest="analysis",required=True)
    job=a_sub.add_parser("job",help="Analyze a job description")
    job.add_argument("job",type=Path)
    job.add_argument("--root",default=".",type=Path)
    job.add_argument("--json",action="store_true",dest="json_output")
    return parser

def main():
    args=_parser().parse_args()
    if args.command=="validate": raise SystemExit(validate_command(args.root))
    if args.command=="build": raise SystemExit(build_command(args.root,args.output,args.profile,args.format))
    if args.command=="analyze" and args.analysis=="job": raise SystemExit(analyze_job_command(args.root,args.job,args.json_output))
    raise SystemExit(2)

if __name__=="__main__": main()
