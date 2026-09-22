from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from pydantic import ValidationError
from .model import Credential,Education,Experience,Language,ProfileData,Skill,TargetProfile

@dataclass(frozen=True)
class ValidationIssue:
    path:str; message:str

def _collect(prefix,model,payload):
    try: model.model_validate(payload); return []
    except ValidationError as exc:
        out=[]
        for e in exc.errors():
            loc=".".join(str(p) for p in e["loc"]); out.append(ValidationIssue(f"{prefix}.{loc}" if loc else prefix,e["msg"]))
        return out

def _duplicates(prefix,records):
    seen=set(); out=[]
    for i,r in enumerate(records):
        value=r.get("id") if isinstance(r,dict) else None
        if isinstance(value,str):
            if value in seen: out.append(ValidationIssue(f"{prefix}[{i}].id",f"duplicate id '{value}'"))
            seen.add(value)
    return out

def validate_career(documents:dict[str,Any])->list[ValidationIssue]:
    issues=[]
    profile=documents.get("profile",{}).get("profile")
    if not isinstance(profile,dict): issues.append(ValidationIssue("profile","missing profile mapping"))
    else: issues += _collect("profile",ProfileData,profile)

    experiences=documents.get("experience",{}).get("experiences",[])
    if not isinstance(experiences,list): issues.append(ValidationIssue("experiences","must be a list")); experiences=[]
    else:
        issues += _duplicates("experiences",experiences)
        for i,item in enumerate(experiences):
            if isinstance(item,dict): issues += _collect(f"experiences[{i}]",Experience,item)
            else: issues.append(ValidationIssue(f"experiences[{i}]","must be a mapping"))

    for key,root_key,model in [("education","education",Education),("certifications","certifications",Credential)]:
        records=documents.get(key,{}).get(root_key,[])
        if not isinstance(records,list): issues.append(ValidationIssue(root_key,"must be a list")); continue
        issues += _duplicates(root_key,records)
        for i,item in enumerate(records):
            if isinstance(item,dict): issues += _collect(f"{root_key}[{i}]",model,item)
            else: issues.append(ValidationIssue(f"{root_key}[{i}]","must be a mapping"))

    skills=documents.get("skills",{}).get("skills",[])
    if not isinstance(skills,list): issues.append(ValidationIssue("skills","must be a canonical skill list"))
    else:
        issues += _duplicates("skills",skills)
        names=set()
        for i,item in enumerate(skills):
            if isinstance(item,dict):
                issues += _collect(f"skills[{i}]",Skill,item)
                if isinstance(item.get("name"),str): names.add(item["name"])
            else: issues.append(ValidationIssue(f"skills[{i}]","must be a mapping"))
        for i,item in enumerate(experiences):
            if isinstance(item,dict):
                for skill in item.get("skills",[]):
                    if skill not in names: issues.append(ValidationIssue(f"experiences[{i}].skills",f"unknown canonical skill '{skill}'"))

    languages=documents.get("languages",{}).get("languages",[])
    if isinstance(languages,list):
        for i,item in enumerate(languages):
            if isinstance(item,dict): issues += _collect(f"languages[{i}]",Language,item)

    ids={x.get("id") for x in experiences if isinstance(x,dict)}
    for pid,target in documents.get("target_profiles",{}).items():
        issues += _collect(f"profiles.{pid}",TargetProfile,target)
        for eid in target.get("preferred_experience_order",[]):
            if eid not in ids: issues.append(ValidationIssue(f"profiles.{pid}.preferred_experience_order",f"unknown experience id '{eid}'"))
    return issues
