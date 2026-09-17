# Bitcoin Bridge Research

An open, versioned research project mapping how capital governed by traditional finance and law can move onto the Bitcoin blockchain.

The repository is the research engine. Versioned PDF papers are compiled outputs.

It now also contains the first expert-system kernel: explicit rules can infer assessments from supplied case facts and return a machine-readable proof trace.

## Brutal truth: the current state

This repository is an early research prototype with a small rule engine and a useful local browser. Calling it an “expert system” describes the architecture we are building toward; it does **not** mean the repository currently contains the breadth, validation, maintenance process, or professional judgment of an expert.

No lawyer, fiduciary, auditor, financial institution, custodian, investor, or beneficiary should rely on its output for a real decision.

### The entire knowledge inventory

As of version `0.1.0`, the structured model contains:

| Item | Count | Honest interpretation |
| --- | ---: | --- |
| Bitcoin capabilities | 3 | Signature validity, threshold control, and selected ledger state—not a complete Bitcoin model |
| Finance requirements | 6 | Headline categories, not an institutional control framework |
| Legal requirements | 5 | General concepts, not the law of any jurisdiction |
| Bridge categories | 7 | A research taxonomy that has not been independently validated |
| Companies | 15 | Representative names with coarse category assignments, not current due diligence |
| Material claims | 2 | Far too few to support broad conclusions |
| Sources | 6 | A tiny evidence base; source-level labels do not validate our interpretation |
| Executable inference rules | 3 | A demonstration of reasoning mechanics, not domain coverage |
| Assessment profiles | 1 | A US-oriented custody pre-review assembled from limited federal banking and New York guidance |
| Assessment requirements | 12 | Research prompts, not a complete compliance checklist |
| Scenario cases | 12 | Authored regression examples, not independently reviewed real cases |
| Automated tests | 15 | Software checks; none prove legal or professional correctness |

Those numbers matter. The interface may look substantial, but the underlying knowledge is still small.

### What demonstrably works

- Structured JSON connects Bitcoin capabilities, financial and legal requirements, bridge categories, companies, claims, and sources through stable identifiers.
- Validation catches some duplicate identifiers, broken references, missing definitions, invalid statuses, and malformed or unsourced rules and assessment requirements.
- A deterministic forward-chaining engine can match supplied facts, derive conclusions, record which rule fired, retain source identifiers, and expose contradictory values.
- Missing facts remain `unknown`; they are not silently converted to `false`.
- The engine has a basic “why not?” mechanism that can list unmet prerequisites for a requested conclusion.
- The custody pre-review separates evidenced requirements, explicit gaps, missing information, invalid values, and conditional sub-custodian requirements.
- Markdown and compact PDF outputs can be generated from the domain model.
- The static web interface lets a human search the present model, inspect relationships and source links, read the system's limits, and interact with the custody questionnaire.
- Given the same repository version and inputs, the code produces repeatable outputs.

### What the web interface really is

- It is a static HTML, CSS, and JavaScript application served from `dist/`. There is no application server, database, account system, or API.
- It reads a generated snapshot of repository JSON. Changes to the domain files do not appear until `python3 -m src.build_web` is run again.
- Its search is simple client-side text matching, not semantic search, retrieval-augmented generation, or an LLM.
- It does not save assessments. Refreshing or closing the page loses the user's selections.
- It does not accept evidence files, verify documents, execute Bitcoin signature checks, query a node, inspect transactions, or authenticate people.
- The browser questionnaire currently reimplements the assessment decision logic in JavaScript instead of calling the Python assessment engine. Tests cover the Python implementation, so the two implementations could drift.
- Source links leave the application and open the publisher's page. The repository does not archive source text or prove that a linked page still says what our model claims.
- “Verified on” is repository metadata, not proof that every fact and company classification was rechecked on that date.
- There is no news feed. There is no crawler, regulator monitor, change detector, alerting system, or automatic update process.

### What the system cannot establish

- It cannot establish that a user-supplied fact is true. At present, `true` means only that someone entered `true`.
- It cannot establish legal ownership, beneficial entitlement, legal identity, capacity, authority, consent, voluntariness, death, succession, negligence, or compliance from a Bitcoin key, address, balance, or signature.
- It cannot prove that every wallet, key copy, liability, agreement, beneficiary, transaction, side arrangement, or relevant event was disclosed.
- It cannot prove that “exclusive control” exists merely because one key or signature was demonstrated. Undisclosed copies may exist.
- It cannot determine whether a custodian, trust company, bank, adviser, product, or arrangement is licensed, qualified, lawful, solvent, safe, or suitable now.
- It cannot give legal, tax, accounting, audit, investment, custody, compliance, cybersecurity, or fiduciary advice.
- Its PDF is not a certification, audit opinion, proof of reserves, legal instrument, compliance report, or regulatory filing.

### Missing expert-system capabilities

- No meaningful coverage of any complete body of law, regulation, accounting standards, audit standards, Bitcoin operations, or institutional policy.
- No jurisdiction engine, applicability analysis, effective-date logic, amendment history, precedent hierarchy, exceptions, safe harbors, or conflicting-authority resolution.
- No evidentiary provenance for case inputs: no document hashes, issuer identity, signatures, custody chain, observation method, reviewer, or expiry.
- No full truth-maintenance system. The engine does not maintain a live session that retracts every dependent conclusion when premises change.
- No calibrated uncertainty model. Source quality, factual confidence, legal ambiguity, and expert disagreement are not yet represented separately.
- No expert knowledge-acquisition or approval workflow, named reviewers, rule ownership, four-eyes approval, change impact analysis, or signed releases.
- No independently reviewed golden cases, real-world validation set, coverage measurement, error-rate measurement, or usability evidence.
- No production controls: authentication, authorization, encryption design, audit log, rate limiting, backup, monitoring, incident response, or threat model.
- No continuous integration or automated freshness checks against external sources.

### Known research weaknesses

- Company classifications are broad and can become stale quickly. They should be treated as hypotheses to verify, not vendor recommendations.
- The evidence-level scale describes the kind of source, but it is crude. A regulator's document can be authoritative about one institution and irrelevant to another; reproducibility does not automatically mean legal weight.
- The custody assessment combines US federal banking guidance with New York virtual-currency guidance. That combination is useful for research but does not automatically apply to a particular institution, state, customer, product, or transaction.
- A requirement marked “evidenced” says nothing about the quality, completeness, freshness, authenticity, or legal sufficiency of the evidence unless a qualified reviewer has actually checked it.
- The existing scenario cases were written by the project, for the project. Passing them proves internal consistency, not external validity.

### The honest achievement—and the next bottleneck

The repository proves that a small amount of domain knowledge can be represented, linked to sources, checked structurally, executed deterministically, explained, tested, published, and explored in one codebase.

It does **not** prove that the encoded knowledge is complete, applicable, current, or professionally correct. The primary bottleneck is now expert-reviewed knowledge and evidence provenance—not more interface polish, more rules written by a model, or a larger language model.

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
