# ADR-0002: Represent Career Information as Configuration as Code

- Status: Accepted
- Date: 2026-08-03

## Context

Traditional career documents mix data, wording, presentation, and output format in the same file. That makes reuse, validation, localization, and automation difficult.

## Decision

CareerOS will represent professional information as structured, declarative configuration that can be versioned, validated, reviewed, and transformed into multiple outputs.

The first implementation will separate career data from templates and generation logic.

## Consequences

### Positive

- Data can be validated before generation.
- Templates can evolve independently from career history.
- The same information can support different languages and job targets.
- Pull requests can review career changes as structured diffs.

### Negative

- Structured configuration may feel less familiar than editing Word documents.
- Validation rules must balance consistency with flexibility.
- A stable schema and migration strategy will eventually be necessary.

## Alternatives Considered

### Use Markdown as both source data and final document

Rejected as the primary model because free-form Markdown is difficult to validate and reuse across multiple views.

### Use a database from the beginning

Deferred because it adds operational complexity before the domain model and workflows are proven.
