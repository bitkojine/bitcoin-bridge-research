# Species and Precedents — the design covenant

> This document exists to stop future work from inventing machinery. Before adding a concept, a data field, a status, or a rule, find the real-world system that already solves the problem and transplant its semantics. If nothing real exists, say so and mark the gap — do not silently improvise.

## What species is this system?

**A legal-research citator wrapped around an evidence-backed attestation pre-screen.**

It is not an expert system in the research-DB sense, not a blockchain oracle, and not a ratings engine today. Its real family is the set of professional tools that answer "what does the authority actually support, and is that authority still good?" — the same family as a law-firm citator, an audit workpaper, and a sourcing-tracked reference database.

Consequences of the species (borrowed, not invented):

- **Claim statuses are citator treatment signals**, not a private invention.
- **Sources carry authority currency** ("still good law"), exactly like a citator reports on authority.
- **Evidence grading must follow established evidence-grading disciplines**, not a made-up number.
- **A decision-grade outcome requires model-governance discipline** (published methodology, independent validation, monitoring), not a label.

## Precedents to transplant from

| Real-world system | Problem it already solves | What we borrow |
| --- | --- | --- |
| Shepard's Citations / Westlaw KeyCite | Whether a citation supports, distinguishes, questions, or contradicts a proposition, and whether the cited authority is still good law | Source `currency`; per-citation `treatment` signals; `superseded_by`; derived status semantics |
| ISA 500 Audit Evidence (IAASB) | Sufficiency and appropriateness of evidence as a test, not a feeling | The future corroboration test |
| SOC reports (SSAE 18 / ISAE 3402) | Scoped control set + attestation opinion + exclusions | Shape of "independent assurance" requirements |
| Wikidata | Sourced statements with rank (deprecated/normal/preferred), references, full history | Statement-with-source shape and deprecation handling; also what to avoid (loose source quality) |
| OpenSanctions | Ingesting authoritative lists, normalizing, dedupe, publishing provenance | Ingestion and provenance discipline |
| XBRL / US-GAAP taxonomy | A governed, versioned canonical dictionary for facts | `domain/facts.json` as a registered taxonomy |
| CELEX / ELI / ECLI / Akoma Ntoso | Stable machine-readable identifiers and versions for legal documents | Future source/passage identifiers |
| Bluebook pinpoint citations | Passage-level citation discipline | The `Extracted` stage's citation shape |
| GRADE / Cochrane systematic reviews | Disaggregated, pre-registered evidence grading | Replacement for the ad-hoc source `level` 1–5 |
| CLIPS / Drools | Production-rule conflict resolution and explanation at scale | Agenda/priority and explanation engineering |
| Credit-rating methodology governance, SR 11-7 model risk, EU AI Act Annex IV | Published, validated, monitored decision machinery | What "decision-grade" must actually mean |

## What has been transplanted so far

### Citator model (v0.3.0)

- Sources now carry `currency: current | superseded | withdrawn`, with `superseded_by` naming the replacement authority — a citator's "good law" reporting.
- Claims cite sources through `treatments: {source_id, treatment}` where `treatment ∈ supports | qualifies | contradicts` — a citator's signal on each citation.
- Claim statuses are derived-and-checked from treatments + currency, not asserted:

| Status | Requirement (enforced by validation) |
| --- | --- |
| `unverified` | no treatments recorded |
| `supported` | at least one current supporting source; no contradicting authority |
| `corroborated` | at least two distinct current supporting sources; no contradicting authority |
| `contested` | at least one contradicting treatment is cited |
| `stale` | treatments exist but no supporting source is current |
| `retracted` | a cited source has currency `withdrawn` |
| `superseded` | `superseded_by` names newer claims that replace it |

This is Shepard's treatment-signal machinery applied to a Bitcoin research corpus: the status ladder the repository used before (also called `unverified/supported/corroborated/contested/stale/retracted`) was a private invention; the treatment model is the borrowed, real one.

## What is deliberately NOT invented

- No new claim-status vocabulary beyond the citator treatment + currency model.
- No private evidence "validity number" — the existing `level` 1–5 is a known conflation and is next in line to be replaced by the disaggregated GRADE-style fields.
- No invented corroboration test — ISA 500's sufficiency/appropriateness test is the template for the next transplant.

## Gaps (no real-world precedent found yet)

- A bitcoin-specific complement linking *unspent outputs* to institution-facing entitlements has no direct citator analogue; existing on-chain/provenance tooling (address labeling, registry audit) is the closest partial precedent. Marked as a gap, not improvised.