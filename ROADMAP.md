# CareerOS Roadmap

The roadmap is outcome-oriented. CareerOS keeps the deterministic Career as Code engine separate from future AI and SaaS layers.

## Sprint 0 — Product Foundation

- Vision, principles, non-goals, repository boundaries, architecture, ADR process, and first vertical slice.

## v0.1.0 — CareerOS Engine

**Outcome:** A user can keep career facts in a source-of-truth repository, validate them, select a target profile, and generate distribution-ready resume artifacts.

- [x] Career as Code repository model
- [x] Domain model for profile, experience, domains, skills, education, credentials, languages, and target profiles
- [x] Validation and duplicate/reference checks
- [x] Canonical skills taxonomy
- [x] Target-profile selection
- [x] Markdown rendering
- [x] HTML rendering
- [x] PDF rendering
- [x] DOCX rendering
- [x] Engine CI
- [x] Consumer-repository GitHub Actions pipeline
- [x] Generated artifacts kept outside the canonical facts

## v0.2.0 — Career Intelligence

**Outcome:** CareerOS can match a job or goal to verified career evidence without inventing facts.

- Job-description parser
- Requirement and skill matching
- Evidence scoring
- Achievement selection
- ATS-oriented composition
- AI-assisted rewriting with explicit grounding and human review

## v0.3.0 — Multi-person / Multi-domain

**Outcome:** The same engine works for different professions and users.

- Software Engineering reference dataset
- Product Design reference dataset
- Generic domain-model hardening
- Public fictional examples and onboarding

## v0.4.0 — API

**Outcome:** CareerOS capabilities are available without requiring Git or YAML.

- Profile APIs
- Experience and skill APIs
- Job analysis
- Resume generation jobs
- Artifact retrieval
- Versioned schemas

## v1.0.0 — CareerOS SaaS

**Outcome:** CareerOS becomes a self-service career intelligence platform.

- Web application
- Authentication and user-owned career profiles
- Career editor
- Job targeting
- Resume builder and version history
- PDF/DOCX generation
- Portfolio/profile generators
- Subscription/billing layer

## Future Exploration

- LinkedIn and portfolio drafts
- Interview preparation and STAR stories
- Plugin SDK
- Localization
- Schema migrations
- Static career sites
- Additional professional domains
