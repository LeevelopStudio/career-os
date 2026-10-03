# CareerOS

> Treat your career like software: version it, validate it, generate it, and evolve it.

CareerOS is an open-source **Career as Code** engine inspired by Platform Engineering and GitOps. Professional facts remain in a user-owned source of truth; CareerOS validates that data, selects evidence for a target profile, and renders reproducible career artifacts.

## v0.1 Engine

```text
Career repository
  profile / experience / skills / education / credentials / languages
                         │
                         ▼
                   CareerOS Loader
                         │
                         ▼
                 Domain + Validation
                         │
                         ▼
                  Target Profile
                         │
                         ▼
               Evidence / Skill Selection
                         │
                         ▼
                    Renderers
               MD / HTML / PDF / DOCX
```

The public engine contains no private career data. A private or local career repository owns the facts and invokes CareerOS locally or from CI.

## CLI

```bash
python -m pip install -e .

career validate --root /path/to/career

career build resume \
  --root /path/to/career \
  --profile platform-engineer \
  --format pdf \
  --output generated/resume-platform-engineer-en.pdf
```

Supported resume formats in v0.1 are `md`, `html`, `pdf`, and `docx`.

## Core Model

CareerOS v0.1 models profile data, experiences, domains, canonical skills, education, credentials, languages, and target profiles. Experiences provide evidence for skills; target profiles control prioritization without duplicating career history.

The design deliberately separates facts from presentation:

```text
career facts → validated domain model → target selection → artifact
```

AI is not required to generate a valid artifact and must not become the source of professional facts.

## Automation

The engine has its own test workflow. Consumer career repositories can install CareerOS, validate their source of truth, generate multiple target profiles and formats, and publish the generated files as CI artifacts.

## Project Documents

- [Vision](VISION.md)
- [Architecture](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Architecture Decision Records](docs/adr/)

## Repository Model

- `career-os`: public engine, models, validation, selection, renderers, tests, and documentation.
- consumer career repository: private/user-owned professional data and generated outputs.

## Status

**v0.1 engine implementation** — executable vertical slice with multi-format resume generation and profile targeting.

## License

CareerOS is released under the [MIT License](LICENSE).
