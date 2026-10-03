# CareerOS Roadmap

The roadmap is outcome-oriented. Dates will be added only after the first implementation language and delivery cadence are agreed.

## Sprint 0 — Product Foundation

- Define vision, mission, principles, and non-goals.
- Document the separation between the public engine and private career data.
- Establish the initial architecture and ADR process.
- Define the first vertical slice and release sequence.

## v0.1.0 — Structured Career Data to Markdown Resume

**Outcome:** A user can validate structured career data and generate an English ATS-oriented resume in Markdown.

- Define the initial domain model.
- Define schemas for profile, experience, achievements, skills, education, certifications, languages, and projects.
- Implement input loading and validation.
- Implement the first resume template.
- Provide fictional public sample data.
- Add automated tests and CI quality gates.

## v0.2.0 — Multiple Resume Views

**Outcome:** The same career source can generate role-focused resume variants.

- Master resume
- ATS resume
- Platform Engineering resume
- Senior Java resume
- Software Architecture resume
- Portuguese and Spanish localization foundations

## v0.3.0 — Document Formats

**Outcome:** Markdown output can be transformed into distribution-ready formats.

- HTML generation
- PDF generation
- DOCX generation
- Deterministic formatting checks
- Release artifacts

## v0.4.0 — Professional Profile Generators

**Outcome:** CareerOS can produce synchronized content for other professional channels.

- LinkedIn About draft
- LinkedIn experience descriptions
- GitHub profile README
- Short and long professional bios

## v0.5.0 — Portfolio and Case Studies

**Outcome:** Projects and achievements can become sanitized public portfolio content.

- Project case-study pages
- Architecture decision summaries
- Static portfolio website
- GitHub Pages deployment

## v0.6.0 — Interview Preparation

**Outcome:** Real experience can be transformed into reusable interview material.

- STAR stories
- Technical deep-dive prompts
- Architecture interview narratives
- Leadership and behavioral examples

## v1.0.0 — Stable CareerOS CLI

**Outcome:** CareerOS provides a documented, stable workflow for managing Career as Code.

Proposed commands:

```text
career init
career validate
career build
career generate resume
career generate linkedin
career generate portfolio
```

## Future Exploration

- Plugin SDK
- Job-description-based resume selection
- AI-assisted drafting with explicit human review
- Schema migration support
- Web interface
- Additional professional domains beyond software engineering
