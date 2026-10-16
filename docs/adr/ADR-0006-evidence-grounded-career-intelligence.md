# ADR-0006: Evidence-grounded Career Intelligence

## Status

Accepted

## Context

CareerOS v0.1 can validate one canonical career source and render target-profile resumes. v0.2 introduces job analysis and, later, AI-assisted composition.

A job description is not evidence that a person owns a skill. Allowing a language model or keyword matcher to add unsupported claims would violate CareerOS's single-source-of-truth principle.

## Decision

Career Intelligence is built above the deterministic CareerOS domain model.

The first pipeline is:

```text
Job Description
      |
Requirement Extraction
      |
Canonical Skill Resolution
      |
Career Evidence Matching
      |
Matched / Missing Requirements
      |
Explainable Analysis
```

A requirement is matched only when the canonical career data contains evidence for it. Missing requirements remain explicit gaps.

LLMs may later classify, rank, summarize, or rewrite verified evidence, but they may not create career facts, metrics, employers, skills, or achievements.

## Consequences

- Analysis is reproducible without an LLM.
- Results can explain which experience supports each requirement.
- AI providers remain optional adapters.
- Unsupported job requirements are visible rather than hallucinated into a resume.
- Future scoring can evolve independently from the canonical data model.
