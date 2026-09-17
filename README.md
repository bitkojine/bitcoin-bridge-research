# Bitcoin Bridge Research

An open, versioned research project mapping how capital governed by traditional finance and law can move onto the Bitcoin blockchain.

The repository is the research engine. Versioned PDF papers are compiled outputs.

It now also contains the first expert-system kernel: explicit rules can infer assessments from supplied case facts and return a machine-readable proof trace.

## Brutal truth: what this repository is today

This is a promising research scaffold and a functioning expert-system **kernel**. It is not yet an expert system that a lawyer, fiduciary, auditor, financial institution, or Bitcoin custodian should rely on for a real decision.

### What it can do now

- Store a small Bitcoin–finance–law domain map as structured, version-controlled data.
- Relate Bitcoin capabilities, financial requirements, legal requirements, bridge categories, companies, claims, and sources by stable identifiers.
- Check basic structural integrity: duplicate identifiers, broken references, missing equations or term definitions, invalid evidence levels and claim statuses, and malformed or unsourced rules.
- Generate a Markdown market map and a compact PDF from the domain model.
- Apply a small set of explicit rules to facts supplied in JSON.
- Use deterministic forward chaining: the same code, rule version, and facts produce the same output.
- Keep missing information as `unknown` instead of silently treating it as `false`.
- Return a proof trace showing which rule fired, which conditions matched, what it concluded, and which repository sources support the rule.
- Surface incompatible values for the same fact as a conflict instead of silently choosing one.
- Run a twelve-area institutional-custody pre-review and demonstrate its boundary behavior with twelve scenario cases and automated tests.

### What it cannot do yet

- It cannot establish that an input fact is true. The engine currently trusts the JSON supplied to it; it does not authenticate documents, signatures, identities, balances, authority, or provenance.
- It cannot give legal, tax, accounting, investment, custody, compliance, or fiduciary advice.
- It does not encode a meaningful portion of any jurisdiction's law, regulation, accounting standards, institutional policies, or operational practice.
- It cannot determine legal ownership from a Bitcoin signature or address. Cryptographic control and legal entitlement remain separate facts.
- It cannot prove that all wallets, private-key copies, liabilities, agreements, beneficiaries, or relevant events have been disclosed.
- It cannot know whether a signature was voluntary, contemporaneous, properly authorized, or made by the legally relevant person unless external evidence supplies those facts.
- It cannot independently classify companies or keep product, licensing, regulatory, or market information current.
- It has only a handful of inference rules, one assessment profile, and a small source set. Its present conclusions demonstrate the engine and pre-review workflow, not expert-level domain coverage.
- It has no jurisdiction or effective-date reasoning, no exception hierarchy, no treatment of precedent, and no mechanism for resolving conflicting legal authorities.
- It has no calibrated uncertainty model. It can report explicit conflicts, but it cannot responsibly turn evidentiary strength or professional disagreement into a probability.
- It cannot yet explain why a requested conclusion did **not** fire by listing every missing prerequisite.
- It does not retract dependent conclusions when a supporting fact is removed during a live session; full truth maintenance is not implemented.
- It has no expert-review workflow, approval signatures, separation of duties, audit log, access control, or production security model.
- It has not been validated against a substantial set of real, independently reviewed cases or measured for domain coverage, error rates, or professional usefulness.
- Its generated PDF is a research output, not a certification, audit opinion, legal instrument, proof of reserves, or regulatory filing.

### The honest milestone

The repository proves that domain knowledge can be represented, checked, executed, explained, tested, versioned, and published from one codebase. It does **not** prove that the knowledge base is complete or professionally correct. The next constraint is knowledge acquisition and validation by qualified specialists—not adding more artificial intelligence.

## Research thesis

Bitcoin provides narrow, machine-verifiable guarantees: signatures, script satisfaction, ledger state, and cryptographic commitments. Traditional finance and current law additionally require identity, authority, ownership records, liabilities, controls, succession, and remedies.

The market forms at the bridges between those systems.

## Domain model

```text
BitcoinCapability ---supports---> Bridge
FinanceRequirement --requires---> Bridge
LegalRequirement ----requires---> Bridge
Company -------------provides---> Bridge
Claim -------------supported_by-> Source
```

Structured research lives in [`domain/model.json`](domain/model.json). The validator checks identifiers, relationships, equations, term definitions, company references, and evidence links.

## Commands

Requires Python 3.11 or later. Core validation and inference use only the standard library; PDF generation uses ReportLab as declared in `pyproject.toml`.

```bash
python3 -m src.cli validate
python3 -m src.cli build
python3 -m src.cli build-pdf
python3 -m src.cli infer examples/institutional-custody.json
python3 -m src.cli assess examples/custody-readiness-complete.json
python3 -m src.cli assess examples/custody-readiness-gaps.json
python3 -m src.build_web
python3 -m unittest discover -s tests
```

`build` produces [`generated/market-map.md`](generated/market-map.md), a human-readable view generated from the domain model.

`build-pdf` produces [`output/pdf/domain-map.pdf`](output/pdf/domain-map.pdf) directly from the same model. This is a compact, reproducible research output rather than the separately authored long-form paper.

`infer` evaluates a JSON case against [`domain/rules.json`](domain/rules.json). It uses open-world semantics: an absent fact is unknown, never silently false. See [`research/expert-system-architecture.md`](research/expert-system-architecture.md) for the design, quality criteria, safeguards, and roadmap.

`assess` runs the first practical workflow: a US institutional Bitcoin custody pre-review covering twelve evidence areas. It returns `ready_for_expert_review`, `not_ready`, or `insufficient_information`, then lists blocking gaps and missing evidence. The profile is in [`domain/assessments/custody-readiness.json`](domain/assessments/custody-readiness.json). It is research software, not a compliance or legal determination.

`build_web` refreshes the static browser interface in [`dist/`](dist/) from the current domain model, rules, and assessment profile. Serve that directory locally to explore the knowledge base and run the assessment interactively.

## Publications

- [`v0.1.0 research paper`](publications/v0.1.0/bitcoin-bridge-market-research-draft.pdf)
- [`v0.1.0 release notes`](publications/v0.1.0/RELEASE_NOTES.md)

## Evidence policy

Every material claim should identify its source and carry both a status and evidence level.

Statuses: `unverified`, `supported`, `corroborated`, `contested`, `stale`, `retracted`.

Evidence levels:

1. Company marketing
2. Official technical documentation
3. Regulatory or legal filing
4. Independent professional evidence
5. Reproducible primary data

## Scope

The market map is representative, not exhaustive. Company classifications change as products, laws, and institutions evolve. Each publication records its verification date.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Contributions should improve the model, evidence, or interpretation—not merely add prose.
