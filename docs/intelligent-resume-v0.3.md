# Intelligent resume generation (v0.3 prototype)

Build an ATS-friendly resume from the same validated private career data, prioritizing **verbatim** achievements that explicitly match the vacancy. This is deterministic evidence selection, not free-form LLM writing or a claim of ATS success.

```bash
career validate --root ../career
career build resume --root ../career --profile platform-engineer \
  --job vacancy.txt --format md \
  --output ../career/generated/resume-targeted.md \
  --report ../career/generated/resume-targeted-evidence.json
```

Existing `career build resume` without `--job` retains its original behavior. Other existing formats (`html`, `pdf`, `docx`) use the same selected source data.

Review the JSON report for detected requirements, missing evidence, selected highlight indices and fallbacks. A keyword miss does not prove the absence of a skill. Non-matching highlights may be omitted; review the generated resume manually before applying.

## Next iterations

- Human-approved paraphrasing with per-claim provenance
- Better semantic evidence extraction without unsupported inference
- LinkedIn headline/About/experience drafts generated from the same verified data
- Design-oriented presentation card as a separate artifact
