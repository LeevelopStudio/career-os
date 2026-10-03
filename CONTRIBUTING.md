# Contributing to CareerOS

Thank you for helping improve CareerOS.

## Working Principles

- Understand the problem before choosing a technology.
- Keep private career data outside the public repository.
- Prefer small, reviewable changes.
- Document important decisions with ADRs.
- Add or update tests when behavior changes.
- Never edit generated artifacts as if they were source files.

## Development Workflow

1. Create or select a GitHub issue.
2. Create a focused branch from `main`.
3. Update documentation when the change affects behavior or architecture.
4. Implement the smallest useful vertical slice.
5. Run validation, formatting, linting, and tests.
6. Open a pull request linked to the issue.
7. Explain the problem, decision, trade-offs, and impact in the PR.

## Branch Naming

Examples:

```text
feature/markdown-resume-generator
architecture/domain-model
fix/validation-error-message
docs/privacy-boundaries
```

## Commit Style

CareerOS uses concise Conventional Commit-style messages:

```text
docs: add product vision
feat: generate English Markdown resume
fix: reject invalid employment periods
refactor: isolate template rendering adapter
test: cover achievement validation
```

## Pull Request Expectations

A pull request should include:

- The problem being addressed
- The proposed solution
- Important trade-offs
- How the change was tested
- Documentation or ADR updates
- Security and privacy considerations when relevant

## Architecture Decisions

Create an ADR when a decision:

- Has long-term architectural consequences
- Introduces or replaces a major dependency
- Changes the public data contract
- Changes repository or privacy boundaries
- Is difficult or expensive to reverse

## Privacy and Confidentiality

Do not commit:

- Real private career datasets
- Credentials, tokens, or session data
- Government identifiers or full residential addresses
- Employer-confidential documents or diagrams
- Customer data
- Metrics that cannot be shared publicly

Use fictional data in public examples.

## Code of Conduct

Contributors should communicate respectfully, review ideas rather than people, and create an environment where questions and constructive disagreement are welcome.
