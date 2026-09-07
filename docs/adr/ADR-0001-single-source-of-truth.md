# ADR-0001: Use a Single Source of Truth for Career Data

- Status: Accepted
- Date: 2026-08-03

## Context

Professional information is often duplicated across resumes, LinkedIn, portfolios, application forms, websites, and interview notes. Independent copies become inconsistent and expensive to maintain.

## Decision

CareerOS will treat structured career data as the authoritative source. Resumes, profile drafts, portfolio pages, and other artifacts are generated views and must not become competing sources of truth.

## Consequences

### Positive

- Updates become consistent and traceable.
- Multiple outputs can reuse the same reviewed information.
- Version control provides history and reviewability.
- Role-specific artifacts can be generated without copying data.

### Negative

- Users must adopt a structured-data workflow.
- Generated files should not be edited directly.
- Schema evolution and migration will require explicit support.

## Alternatives Considered

### Keep each document independent

Rejected because it preserves duplication and inconsistency.

### Use LinkedIn as the source of truth

Rejected because LinkedIn does not represent all private, detailed, or role-specific career information and cannot be treated as a portable domain model.
