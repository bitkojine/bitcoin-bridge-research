# Mission and Roadmap — Growing the research system

> **Honesty banner:** this roadmap describes where the repository wants to go. None of the later stages exist yet. The only stage that is real today is `Seed`. Treat every Sprout-or-later paragraph as vision, not capability.

> CURRENT-STAGE: Seed

**Mission:** turn a candid idea — that Bitcoin's narrow, machine-verifiable guarantees can be connected to the institutional facts finance and law require — into a system whose knowledge is as verifiable as its kernel.

**Vision:** an evidence-backed, inspectable, decision-grade research system: immutable archived sources, attributed extraction and review, executable corroboration, on-chain reconciliation, and conclusions that can tell you *why* they hold — or refuse to tell you anything at all.

**How we mark progress:** the repository grows like a plant. Each stage has a gate. Nothing progresses by renaming or by prose; it progresses by passing the same kind of honesty tests that already protect the C4 document.

```
Seed ──────► Sprout ──────► Sapling ──────► Tree ──────► Grove
(kernel &   (sources       (evidence-     (connected    (decision-
 honesty     archived)      backed)        & current)    grade)
 tests)
```

---

## Stage 0 — Seed *<— we are here today*

```
        .-.
       /   \         THE SEED — the repository today.
      /  o  \        kernel + honesty tests + a small model.
      \     /
       '---'
   =====^=====       soil = CI. Nothing has germinated yet.
```

**This stage means**
- A working, versioned kernel: `src/expert.py` open-world forward chaining with proof traces; a validated domain model, shared fact registry, rules, and assessment profile; citator-checked claim statuses; a content-addressed source archive; a C4 document that cannot drift; 75 tests that enforce all of it in CI.
- The knowledge is deliberately small and honestly labeled: 3 Bitcoin capabilities, 7 bridge categories, 15 companies, 8 sources (6 frozen), 2 claims, 12 assessment requirements, 20 facts. Interface outruns knowledge; the docs say so.
- Machinery is borrowed, never invented: claim statuses follow the treatment-signal model of legal citators, source currency follows "still good law" reporting, and future evidence grading will follow established audit and systematic-review standards. See `research/precedents.md`.
- Sources are now frozen: 6 of 8 are archived with `sha256` hashes and extracted text, and every claim treatment carries a passage locator and a verbatim quote checked against the frozen text. The two `occ.gov` documents could not be fetched from the archiving host and are recorded as unavailable. Claims remain project-`Interpreted`; nothing is independently attested.

**This stage does NOT mean**
- That any conclusion is true, applicable, or advisable. No real evidence exists: `evidence/claims/` is an empty directory. There are no reviewers, no node access, no API, no readers beyond the maintainer.

**Gate to Sprout (partly automated)**
- The automated gate, enforced by the test suite: `evidence/claims/` is no longer empty. The test suite verifies the `CURRENT-STAGE` marker above against the repository itself, so this document cannot drift.
- The human gate: every claim cites a passage of a content-addressed source snapshot (archive + `sha256`), with the extractor and interpreter attributed. Claims now meet the archive and passage-citation half; attribution of extractor and interpreter, and reproducible extraction, do not yet exist.

---

## Stage 1 — Sprout *(sources archived, provenance recorded)*

```
        |            the first shoot: sources are archived,
       / \           hashed, and cited passage-by-passage.
      /   \
      '   '
   =====^=====
```

**What changes**
- The knowledge base stops trusting URLs. A source archive container stores immutable snapshots with hashes — the exact weakness the README names: *"There are no source snapshots, hashes, passage citations, link checks, or supersession detection."*
- A provenance store records who extracted, interpreted, and will review what, when — shaped by the PROV-O and VC data models already in the source registry.
- `evidence/claims/` fills with real, structurally valid records (the schema `src/assessment.py` already validates).

**Evidence ladder reached:** `Extracted`, moving into `Applicable`.

**This stage does NOT mean:** that extracted passages are true, or that evidence is authentic. Extraction is quoted, not adjudicated.

---

## Stage 2 — Sapling *(evidence-backed)*

```
        Y            the sapling: real case evidence,
       /|\           reviewers, corroboration that must
      /_|_\          actually be demonstrated.
        |
   =====^=====
```

**What changes**
- Real cases: institutions or auditors submit evidence; reviewers attest scoped reasoning; case files go through the full `validate_case` → `derive_facts` → `assess` pipeline instead of synthetic examples.
- `corroborated` stops being a label and becomes an executable test (independence, relevance, sufficiency), turning the README's noted weakness — *"`corroborated` has no formal independence, relevance, or sufficiency test"* — into code.
- The static web UI becomes a real client: the questionnaire drives the assessment engine through an API, and readers exist.

**Evidence ladder reached:** `Applicable` and `Corroborated`, pilot-scope `Case-evidenced`.

**This stage does NOT mean:** that a laid claim is decision-grade, or that any jurisdiction's full body of law is covered.

---

## Stage 3 — Tree *(connected and current)*

```
       ,@,
      _/|\_          the tree: connected to the chain,
       \|/           ingesting regulation, tracking change.
        |
   ~~~~~|~~~~~
```

**What changes**
- A Bitcoin node/RPC edge so on-chain state can be reconciled against assertions like `books_reconcile_to_chain` — converting the model's "Bitcoin proves" capabilities from theory into checks.
- Regulatory and news ingestion, supersession and change detection, so the knowledge base stays current rather than pinned to a `checked_on` date that is metadata, not proof.
- The knowledge base grows ecologically: jurisdiction matrix, more capabilities and requirements, more real companies — each addition accepted only if it passes the same invariants.

**Evidence ladder reached:** `Case-evidenced` with reproducible rule traces over live data.

**This stage does NOT mean:** that the system can hold anyone to a legal conclusion. Court filings still outnumber every output this repo will ever produce.

---

## Stage 4 — Grove *(decision-grade)*

```
      @   @          the grove: multi-jurisdiction,
     /|\ /|\         expert-reviewed, auditable,
      |   |          decision-grade only for the
      |   |          defined use it earned.
   ~~~ ~ ~ ~~~
```

**What changes**
- Expert-reviewed and decision-grade pathways for *defined uses* — a named use standard with evidence, rules, controls, and accountability — matching the top of the evidence ladder.
- Third-party auditability: anyone can replay a trace from archived provenance to conclusion. Attestations travel as verifiable credentials.

**This stage does NOT mean:** universal legal, compliance, or investment advice. The disclaimer in `src/assessment.py` ("A qualified professional must validate...") is a permanent branch, not a stage to outgrow.

---

## What never changes

- **The kernel semantics:** open-world forward chaining — *missing is not false*. `src/expert.py` may grow interfaces but its reasoning guarantees stay.
- **The honesty tests:** existential, invariants keep beating prose at every stage; the C4 and roadmap documents stay machine-checked.
- **The evidence ladder:** `Referenced → Extracted → Interpreted → Applicable → Corroborated → Case-evidenced → Expert-reviewed → Decision-grade`. Stages above move along this ladder; they never abolish it.
- **The disclaimer:** every output remains a research pre-screen pending qualified professional validation, forever.

## How this roadmap stays honest

`RoadmapTests` in `tests/test_artifacts.py` reads the `CURRENT-STAGE` marker above, then checks it against the repository: while `evidence/claims/` is empty, the only honest marker is `Seed`. The moment real evidence lands, the test demands the marker move to `Sprout` — and moving a marker is never sufficient; the stage's gates are the real requirement.

A visitor should read this page and know exactly one thing about today: **the seed is planted, and the soil is the test suite.**
