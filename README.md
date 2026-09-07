# CareerOS

> Treat your career like software: version it, validate it, generate it, and evolve it.

CareerOS is an open-source platform inspired by Platform Engineering and GitOps principles. It treats professional career information as structured, version-controlled data and generates consistent professional artifacts from a single source of truth.

## Why CareerOS?

Professional information is usually duplicated across resumes, LinkedIn, portfolios, personal websites, cover letters, and interview notes. CareerOS reduces that duplication by introducing **Career as Code**.

```text
Career Data
    ↓
Validation
    ↓
CareerOS Domain Model
    ↓
Generators
    ├── Resume
    ├── LinkedIn Draft
    ├── Portfolio
    ├── GitHub Profile
    └── Interview Material
```

## Initial Scope

The first usable version will:

- Load structured career data.
- Validate profile, experience, achievements, skills, education, languages, and projects.
- Generate an ATS-oriented English resume in Markdown.
- Keep private career data separate from the public CareerOS engine.

## Project Documents

- [Vision](VISION.md)
- [Architecture](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Architecture Decision Records](docs/adr/)

## Repository Model

- `career-os`: public engine, schemas, templates, generators, tests, and documentation.
- `career`: private professional data and generated personal outputs.

## Status

CareerOS is currently in **Sprint 0 — Product Foundation**.

## License

CareerOS is released under the [MIT License](LICENSE).
