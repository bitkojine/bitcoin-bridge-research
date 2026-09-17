# Contributing

## Principles

1. Separate what Bitcoin proves from what institutions infer or record.
2. Define every mathematical term in plain language.
3. Prefer primary sources and current official documentation.
4. Cite through treatments, not bare lists: every claim records whether each source `supports`, `qualifies`, or `contradicts` it; `corroborated` requires two distinct current supporting sources.
5. Record source currency like a citator: `current`, `superseded` (with `superseded_by`), or `withdrawn`. Withdrawn authority forces `retracted`; contradicting authority forces `contested` — never silently removed.
6. Update `checked_on` dates when rechecking a source, company, or assessment; the snapshot is rebuilt from the model.
7. Register any new fact name used by rules or assessment requirements in `domain/facts.json`; shared vocabulary is enforced by validation.

## Adding a company

- Add a stable company identifier and display name.
- Reference at least one bridge already defined in the model.
- Add a source record.
- Add a claim connecting the company to the bridge.
- Run validation and tests.

## Pull requests

Describe:

- What changed.
- Why it changed.
- Which sources support it.
- Whether any published conclusion becomes stronger, weaker, or contested.

