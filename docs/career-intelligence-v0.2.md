# Career Intelligence v0.2 — acceptance and local test

CareerOS v0.2 analyzes a job description against **verified** private career records. It extracts canonical skill names/aliases, calculates experience-level coverage, and ranks only achievement text explicitly mentioning detected requirements. It does not invent facts, rewrite claims, or estimate ATS acceptance probabilities.

## Local verification

From sibling checkout directories `career-os/` and `career/`:

```bash
cd career-os
git fetch origin
git switch feat/v0.2-career-intelligence
git pull --ff-only
python -m pip install -e '.[dev]'
pytest -q
career validate --root ../career
cat > vacancy.txt <<'EOF'
Senior Platform Engineer
Experience with Java, Amazon Web Services (AWS), CI/CD, Kubernetes,
distributed systems and observability.
EOF
career analyze job vacancy.txt --root ../career --profile platform-engineer --achievements
career analyze job vacancy.txt --root ../career --profile platform-engineer --achievements --json > analysis.json
python -m json.tool analysis.json
```

Review detected requirements, missing skills, evidence experience IDs, achievement text, ordering and reasons. Results depend on the private source's current skills/experience data. A missing explicit keyword does **not** prove the person lacks a skill.

## Release acceptance

- [ ] GitHub CI green for the final commit.
- [ ] CLI smoke test passes against a validated example dataset.
- [ ] User reviews a real vacancy against private career data.
- [ ] No personal data or generated private CV committed to this public repository.

## Next scope (not part of v0.2)

Evidence-grounded, vacancy-specific resume composition and presentation cards require separate design, user approval, and provenance rules.
