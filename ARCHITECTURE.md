# CareerOS Architecture

## Context

CareerOS separates a reusable public engine from private professional data. The engine understands a career domain model, validates structured input, and generates multiple outputs without making personal information part of the public codebase.

## System Boundary

```text
Private Career Repository
        │
        │ structured career data
        ▼
CareerOS Input Adapter
        ▼
Validation Layer
        ▼
Career Domain Model
        ▼
Generation Services
        ├── Resume Generator
        ├── LinkedIn Draft Generator
        ├── Portfolio Generator
        └── Interview Material Generator
        ▼
Generated Outputs
```

## Repository Responsibilities

### `career-os`

Owns:

- Data contracts and schemas
- Validation
- Domain model
- Generators
- Templates
- CLI and automation
- Tests and documentation
- Fictional sample data

Must not contain real private career information.

### `career`

Owns:

- Personal profile
- Employment history
- Achievements and projects
- Education and certifications
- Skills and languages
- Private interview notes
- Generated personal outputs

## Initial Domain Model

The first vertical slice will model:

- `Profile`
- `Experience`
- `Achievement`
- `Project`
- `Skill`
- `Education`
- `Certification`
- `Language`

An achievement should support the structure:

```text
Action
  +
Technology or Method
  +
Engineering or Business Impact
```

## Architectural Style

CareerOS will begin as a modular command-line application. The core domain and generation logic should remain independent from file formats, template engines, and delivery mechanisms.

Suggested logical layers:

```text
CLI / Delivery
    ↓
Application Services
    ↓
Domain Model
    ↑
Input, Validation, and Output Adapters
```

## First Vertical Slice

```text
YAML career data
    ↓
Schema validation
    ↓
Domain objects
    ↓
ATS resume template
    ↓
English Markdown resume
```

## Quality Attributes

The architecture prioritizes:

- Maintainability
- Portability
- Deterministic generation
- Extensibility
- Testability
- Clear privacy boundaries
- Helpful validation errors

## Deferred Decisions

The following decisions remain open and require ADRs:

- Implementation language
- YAML and schema libraries
- Template engine
- PDF and DOCX generation strategy
- Plugin model
- Generated artifact storage policy
