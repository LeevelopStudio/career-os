# ADR-0005: Use Python for the CareerOS v0.1 Engine

- Status: Accepted
- Date: 2026-09-09

## Context

CareerOS needs a small, testable command-line engine that can load YAML career data, validate a domain model, render deterministic templates, and later produce Markdown, HTML, PDF, and DOCX artifacts.

Python and Go were considered for the initial implementation. Go offers excellent single-binary distribution and strong portability. Python offers faster delivery for the current problem, mature YAML/schema/template/document-generation libraries, and a lower implementation cost while the domain model is still evolving.

## Decision

CareerOS v0.1 will use Python 3.12+.

The initial implementation will use:

- PyYAML for YAML loading
- Pydantic for domain validation
- Jinja2 for deterministic templates
- pytest for automated tests
- Python standard-library `argparse` for the first CLI surface

GitHub Actions is an orchestration mechanism only. CareerOS business rules and generation logic must remain inside the engine and be executable locally.

## Consequences

### Positive

- Fast path to the first useful vertical slice.
- Strong ecosystem for YAML, validation, templating, PDF, and DOCX work.
- Domain rules can evolve quickly while CareerOS is still discovering its model.
- The same commands can run locally and in CI.

### Negative

- Users need a Python runtime unless a packaged distribution is introduced later.
- Dependency management is broader than a single compiled Go binary.
- Distribution ergonomics may need additional work before v1.0.

## Guardrail

The domain model and application services must not depend on GitHub Actions or a specific delivery platform. If portability, startup time, or distribution become dominant constraints, the implementation language can be revisited with evidence.

## Alternatives Considered

### Go

Go remains a viable future option, particularly if CareerOS evolves toward a single portable binary. It was not selected for v0.1 because the immediate priority is validating the product model and generation pipeline with minimal implementation overhead.
