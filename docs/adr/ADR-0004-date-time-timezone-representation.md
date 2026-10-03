# ADR-0004: Standardize Date, Time, and Timezone Representation

- Status: Accepted
- Date: 2026-09-06

## Context

CareerOS consumes career information from heterogeneous sources such as LinkedIn exports, manually maintained YAML files, imported documents, and generated metadata. These sources may represent dates using inconsistent formats such as `Aug 2024`, `08/2024`, `2024-08`, or localized values such as `Present`, `Current`, and `Atual`.

Inconsistent temporal representation creates ambiguity, complicates validation and localization, and can cause accidental fabrication of precision. For example, an employment record that is only known to have started in August 2021 should not be normalized to `2021-08-01` unless the exact day is known.

Career dates and system timestamps are also different domain concepts. Employment and education periods normally require calendar precision but no timezone, while generated artifacts, imports, and pipeline events require an unambiguous instant in time.

## Decision

CareerOS will use ISO 8601-compatible representations for calendar dates and RFC 3339-compatible representations for timestamps.

### Career dates

Career-related dates must preserve the precision actually known by the source:

```yaml
# Exact date
date: "2026-09-05"

# Month precision
start_date: "2024-08"

# Year precision
year: "2020"
```

Date-looking YAML scalar values must be quoted so CareerOS retains control over parsing instead of relying on YAML parser-specific native date coercion.

Career dates do not carry a timezone unless the domain explicitly requires one.

### Ongoing periods

Ongoing periods must not encode language-dependent sentinel strings such as `Present`, `Current`, or `Atual`.

Use:

```yaml
start_date: "2024-08"
end_date: null
current: true
```

Renderers are responsible for producing localized labels such as `Present`, `atualmente`, or `actualidad`.

### Timestamps

Machine-generated timestamps such as imports, builds, and artifact generation times must use RFC 3339 with an explicit offset. UTC is the canonical storage timezone for system timestamps:

```yaml
generated_at: "2026-09-06T02:43:12Z"
```

When a local timezone has business meaning, store its IANA identifier separately:

```yaml
generated_at: "2026-09-06T02:43:12Z"
timezone: "America/Sao_Paulo"
```

Fixed UTC offsets such as `GMT-3` must not be used as timezone identifiers because they do not model timezone rules.

### Domain model

CareerOS should model career dates separately from timestamps. A future domain representation may distinguish:

- `Year`
- `YearMonth`
- `Date`
- `Timestamp`

The implementation must not infer higher precision than the source provides.

## Consequences

### Positive

- Source data remains deterministic and language-neutral.
- Employment and education dates can be localized consistently at render time.
- LinkedIn and other imports can preserve their original temporal precision.
- Pipelines and generated artifacts use unambiguous timestamps.
- YAML parser differences are minimized.
- CareerOS avoids inventing dates that are not supported by source data.

### Negative

- Validators and domain parsers must support multiple calendar precisions.
- Renderers must handle ongoing periods and localization instead of relying on display strings stored in source data.
- Imported legacy data may require normalization.

## Guardrails

- Never convert `YYYY-MM` to an arbitrary `YYYY-MM-DD` value.
- Never store localized ongoing-period text as source data.
- Never use timezone abbreviations or fixed offsets as canonical timezone identifiers when an IANA timezone is required.
- Keep career dates and machine timestamps as distinct domain concepts.
