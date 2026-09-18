# Bitcoin Bridge Research — C4 Architecture

This is a C4 (Context, Containers, Components, Code) description of the repository, written to be honest about what this system is and is not. It is a discipline document that is itself checked by tests, not a promotional architecture diagram.

## Honest framing

This repository is **not a server-based software product**. There is no API, no database server, no user authentication, no runtime network traffic, and no Bitcoin-node access. C4's "containers" are therefore mapped to the repository's actual *runnable and deployable artifacts* plus the *versioned data store* that functions as its database. Connectors that are not drawn here are things that deliberately do not exist: the web UI never calls the assessment engine, and nothing queries a Bitcoin node.

## Level 1 — System Context

```mermaid
flowchart LR
    subgraph "Bitcoin Bridge Research"
        SYS["Bitcoin Bridge Research
            versioned research knowledge base,
            CLI rule engine, static web UI"]
    end

    Maintainer["Maintainer / researcher"] -->|curates versioned JSON domain| SYS
    Analyst["Analyst"] -->|runs CLI with evidence case files| SYS
    Reader["Reader"] -->|opens static web UI| SYS

    SYS -->|cites archived snapshots, fetched only by the archive command| SOURCES[("Published sources on the internet")]
    GitHub["GitHub"] -->|hosts repo, runs CI| SYS
    Node["Bitcoin network"] -. no connection .- SYS
```

Honest notes:

- Three actors are drawn, but today the only real one is the maintainer. The UI has no registered external users and `evidence/claims/` is an empty directory.
- The Bitcoin network is deliberately not a dependency; nothing in the repository queries it. CI is the only runtime interaction with an external system.

### Snapshot contract

Checked by `ArchitectureDocTests` in `tests/test_artifacts.py`; this table must match the live knowledge files or CI fails.

| metric | value |
|---|---|
| model version | 0.3.0 |
| bitcoin capabilities | 3 |
| finance requirements | 6 |
| legal requirements | 5 |
| bridges | 7 |
| companies | 15 |
| sources | 8 |
| archived source snapshots | 6 |
| claims | 2 |
| assessment requirements | 12 |
| inference rules | 3 |
| fact registry facts | 20 |

## Level 2 — Containers

```mermaid
flowchart LR
    KB["Domain knowledge base
        versioned JSON source of truth
        functions as the database"]
    EV["Evidence archive
        committed source snapshots
        evidence/sources/<id>/<sha256>.<ext>"]

    CLI["Research CLI (Python)"]
    WEB["Static web UI (browser)"]
    ART["Committed artifacts"]
    CI["CI pipeline"]

    WEB -->|reads embedded data, generated at build time| ART
    CLI -->|validates and reads| KB
    CLI -->|archive writes, validate reads| EV
    KB -->|claim treatments cite frozen sources| EV
    CLI -->|writes| ART
    CLI -. "python -m src.build_web" .-> WEB
    CI -->|clone, validate, rebuild-and-diff, unittest| KB
    CI -->|compares| ART
```

### Containers listed

**Domain knowledge base** — versioned, filesystem-backed source of truth, the repository's "database". Files: `domain/model.json`, `domain/rules.json`, `domain/facts.json`, `domain/philosophy.json`, `domain/legal/allianz-y3-eligibility.json`, `domain/assessments/custody-readiness.json`. Every other container reads it; nothing writes it at runtime (only the maintainer edits it).

**Evidence archive** — committed source snapshots under `evidence/sources/`, described by `evidence/sources/manifest.json`. `archive` (the only networked command) fetches each source, stores the exact bytes at `evidence/sources/<id>/<sha256>.<ext>`, writes the extracted text beside them, and records the hash, size, retrieval time, and result. Sources that cannot be fetched are recorded as `unavailable` with the error — never silently dropped. `validate` and CI read the archive offline; `verify-evidence --drift` re-fetches to detect changed bytes. Only claim-cited sources must be frozen for `validate` to pass.

**Research CLI** — the `src/` Python package. Everything except PDF generation runs on the Python standard library; `reportlab` is required only for `build-pdf`.

- CLI subcommands: `validate`, `build`, `build-pdf`, `infer`, `assess`, `study`, `eligibility`, `archive`, `verify-evidence`.
- The argparse choices come from the `COMMANDS` constant in `src/cli.py`.

`build_web` and `build_example_cases` are invoked as `python -m` modules instead of CLI subcommands.

**Static web UI** — `dist/` is plain static files (`dist/index.html`, `dist/app.js`, `dist/knowledge.js`, `dist/styles.css`) for any static host. There is no server and no request-time computation. The questionnaire on the Assess view is a client-side sandbox and does not run the CLI engine.

**Committed artifacts** — generated outputs rebuilt from the domain knowledge base and committed for freshness-checking: `dist/knowledge.js`, `generated/market-map.md`, `output/pdf/domain-map.pdf`. The synthetic cases in `examples/*.json` and the PDF are regenerable, not hand-written.

**CI pipeline** — `.github/workflows/ci.yml` clones, validates domain and knowledge files, rebuilds the generated trees and fails if `git diff` is non-empty, and runs the full test suite.

## Level 3 — Components

### Container: Research CLI

```mermaid
flowchart LR
    subgraph CLI["src/ (Python package)"]
        cli["cli.py
            argument dispatch, validate, validate_versions,
            claim_status_matches_treatments, build_markdown"]
        asm["assessment.py
            validate_case, derive_facts, assess,
            validate_profile, render_markdown"]
        exp["expert.py
            ExpertSystem forward chaining, why_not, validate_rules"]
        pdf["pdf.py build_pdf, reportlab document"]
        bw["build_web.py build, dist/knowledge.js payload"]
        bc["build_example_cases.py builds synthetic evidence cases"]
        ev["evidence.py
            archive_source, run_archive,
            verify_snapshots, verify_pin_cites, check_drift"]
    end
    KB["domain/*.json"] --> cli & asm & exp
    cli -->|assess and infer commands| asm & exp
    asm -->|accepted evidence facts| exp
    exp -->|proof trace and derived conclusions| asm
    cli --> pdf
    cli -->|archive, verify-evidence, validate| ev
    ev --> SNAP["evidence/sources/<id>/<sha256>.*"]
    bw --> ART["dist/knowledge.js"]
    bc --> EX["examples/*.json"]
```

- `src/cli.py` dispatches commands, validates the model, rule, and profile files, and enforces version parity and claim-status semantics.
- `src/assessment.py` validates evidence cases, derives facts only from accepted, applicable, in-scope, non-expired evidence, and maps them onto assessment requirements.
- `src/expert.py` runs deterministic open-world forward chaining ("missing facts remain unknown, never false") and produces proof traces.
- `src/pdf.py` renders the domain model to a PDF; the PDF footer states the model version to prevent it reading like an independent report.
- `src/build_web.py` serializes the model, rules, assessment, decision architecture and legal-eligibility model into `dist/knowledge.js`.
- `src/build_example_cases.py` regenerates the explicitly synthetic evidence cases in `examples/*.json`.
- `src/evidence.py` freezes what claims cite: it archives source bytes, records hashes and extracted text, and verifies offline that every claim-cited source is frozen and every pin-cite quote appears in the frozen text.

### Container: Static web UI (client-side only)

```mermaid
flowchart LR
    subgraph WEB["dist/"]
        idx["index.html - six views: Explore, Assess, Cases, Eligibility, Sources, System"]
        app["app.js
            renderCatalog, renderDetail, renderAssessment,
            source grid, system card"]
        kb["knowledge.js - window.KNOWLEDGE = domain + legal models,
            embedded at build time"]
    end
    app -->|reads| kb
```

Note: `renderAssessment()` in `dist/app.js` only recombines the user's checkbox selections and labels the result "UNVERIFIED SANDBOX RESULT". It does not invoke `src/assessment.py`; only the CLI produces traceable, evidence-backed output. The diagram keeps the two disconnected on purpose.

## Level 4 — Code (key units, not exhaustive)

```mermaid
classDiagram
    class Assertion {
        +value: Any
        +source: str
        +rule_id: str
    }
    class ExpertSystem {
        +rules
        +infer(supplied_facts, targets) dict
        +why_not(targets, known, fired) list
    }
    Assertion --> ExpertSystem : assertion buckets in known facts
```

The following anchors are verified by `ArchitectureDocTests`: each `file:line` must exist, and the named function must be defined at that line.

- `src/cli.py:26` — `claim_status_matches_treatments()`: a `corroborated` status requires at least two distinct current supporting sources; `contested`, `retracted`, and `stale` must match the cited treatments and source currency.
- `src/cli.py:79` — `validate()`: duplicate ids, reference integrity, evidence levels, per-source `checked_on` dates, source currency and `superseded_by`, claim treatments, frozen source snapshots, and pin-cite quotes.
- `src/cli.py:183` — `build_markdown()`: the "Snapshot generated on" header, treatment locators, and the archived Sources appendix.
- `src/cli.py:240` — `validate_versions()`: model, rules, assessment and fact-registry versions must agree.
- `src/evidence.py:135` — `archive_source()`: fetches a source, stores it at `evidence/sources/<id>/<sha256>.<ext>`, and records hash, size, and extracted text.
- `src/evidence.py:198` — `run_archive()`: archives every source, recording unavailable fetches instead of hiding them.
- `src/evidence.py:245` — `verify_snapshots()`: every frozen file must hash-match its manifest entry, and every claim-cited source must be frozen.
- `src/evidence.py:270` — `verify_pin_cites()`: each treatment must carry a literal locator that appears before a quote found in the frozen source text.
- `src/evidence.py:317` — `check_drift()`: re-fetches frozen sources and reports any whose bytes changed.
- `src/assessment.py:20` — `validate_case()`: evidence records must carry artifact, issuer, provenance, scope, and review blocks.
- `src/assessment.py:110` — `derive_facts()`: accepts evidence only if reviewed-accepted, jurisdiction-scoped, and time-valid; incompatible accepted assertions become a conflict.
- `src/assessment.py:153` — `assess()`: outcome ladder (`conflict`, `not_ready`, `insufficient_information`, `ready_for_expert_review`), then feeds satisfied/failed evidence facts into rules for derived conclusions.
- `src/assessment.py:277` — `validate_profile()`: assessment facts and control facts must be registered in the fact registry.
- `src/expert.py:31` — `infer()`: open-world forward chaining with proof traces and explicit conflict reporting.
- `src/expert.py:120` — `validate_rules()`: rule conditions and conclusions must reference registered facts.
- `src/pdf.py:122` — `build_pdf()`: renders only what `domain/model.json` contains; footer prints the model version.

## What this C4 hides (staying honest)

- **The "system" is mostly data, not code.** The knowledge files in `domain/` outsize the Python by far; validation treats the data as the authority.
- **Empty and degenerate surfaces:** `evidence/claims/` is empty, the paper-company index in `publications/v0.1.0/PAPER_COMPANIES.json` marks most companies illustrative-only, and the assessment evidence cases are synthetic. The Allianz Y3 transition study is source-linked research, not a submitted institutional case or professional conclusion.
- **The archive is partial, and says so:** 6 of 8 sources are frozen with hashes and pin-cite quotes; the two OCC documents (both on `occ.gov`) were unreachable from the archiving host and are recorded as `unavailable` with their errors. Only claim-cited sources are required to be frozen, so requirement references to unfrozen sources remain. Pin cites are machine-checked against frozen text, but that text is extracted, not an independent attestation.
- **No external consumers:** the three personas are aspirational; the only externally observable behavior is the CI pipeline.
- **No persistence:** the web UI keeps questionnaire state only in the DOM; closing the tab loses it.
- **The snapshot contract above is a point-in-time count**, not a guarantee of coverage; it exists so this document cannot silently drift from the model it describes.
