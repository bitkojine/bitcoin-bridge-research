# Bitcoin Bridge Research

An open, versioned research project about the interfaces between Bitcoin, traditional finance, and law. The repository stores a domain model, a small rule engine, a custody pre-review, generated research outputs, and a local browser interface.

## Status

This is an early prototype, not a decision system. “Expert system” describes the intended architecture, not the present level of knowledge or validation. Do not rely on its output for legal, fiduciary, audit, accounting, investment, custody, compliance, or cybersecurity decisions.

### Mission and roadmap

Where this repository is today (seed), and the evidence-backed, decision-grade system it is trying to become, is tracked honestly in [`docs/roadmap.md`](docs/roadmap.md) — including the test that refuses to let that document claim progress the repository has not earned.

### Current inventory

| Item | Count | Scope |
| --- | ---: | --- |
| Bitcoin capabilities | 3 | Signature validity, threshold control, selected ledger state |
| Finance requirements | 6 | Headline categories, not a control framework |
| Legal requirements | 5 | General concepts, not the law of a jurisdiction |
| Bridge categories | 7 | An unvalidated research taxonomy |
| Companies | 15 | Coarse category assignments, not due diligence |
| Material claims | 2 | Insufficient for broad conclusions |
| Sources | 8 | A small evidence base with recorded check dates |
| Inference rules | 3 | Demonstrate mechanics, not domain coverage |
| Fact registry | 20 | Shared vocabulary enforced across rules and assessment |
| Assessment profiles | 1 | US-oriented custody pre-review |
| Assessment requirements | 12 | Research prompts, not a compliance checklist |
| Scenario cases | 12 | Project-authored regressions, not reviewed cases |
| Automated tests | 44 | Software tests, not professional validation |

The interface is more substantial than the knowledge base behind it.

### Implemented

- Structured links among Bitcoin capabilities, finance and legal requirements, bridge categories, companies, claims, and sources.
- Checks for some duplicate identifiers, broken references, missing definitions, invalid statuses, and malformed or unsourced rules and assessment requirements.
- Deterministic forward chaining with open-world semantics: missing is not false.
- Proof traces, conflict reporting, and a basic explanation of unmet prerequisites.
- A shared fact registry (`domain/facts.json`) that inference rules and the assessment must both use; validation fails on vocabulary drift.
- An evidence-backed pre-review that passes its accepted, applicable facts into the inference rules and reports derived conclusions such as `custody_bridge_ready` and `legal_authority_gap`. A rule never fires on missing facts.
- A custody pre-review that separates supported requirements, explicit gaps, missing facts, invalid values, and conditional sub-custodian requirements.
- Evidence records that separate assertions, artifacts, issuers, provenance, jurisdiction and time scope, review activities, and reviewers.
- Fact derivation only from structurally valid, accepted, applicable, unexpired evidence; incompatible accepted assertions produce a conflict.
- Semantic claim-status validation: a claim marked `corroborated` must carry at least two distinct sources; a single source can support but not corroborate.
- Generated Markdown, PDF, and static web views, with regression tests that the generated snapshots are fresh, the web UI boots, and versions agree across knowledge files.
- Client-side search and an interactive custody questionnaire.
- A C4 architecture description (`docs/architecture-c4.md`) whose file references, Level 4 code anchors, CLI subcommands, and snapshot contract table are regression-tested so the document cannot drift from the code it describes.

### Not established or implemented

- Input truth. A supplied `true` value is accepted, not verified.
- Authentication of documents, identities, signatures, balances, authority, or provenance.
- Legal ownership, beneficial entitlement, identity, capacity, authority, consent, death, succession, negligence, or compliance from a Bitcoin key, address, balance, or signature.
- Completeness of wallet, key-copy, liability, agreement, beneficiary, transaction, or event disclosure.
- Exclusive control from a single key or signature demonstration; undisclosed copies may exist.
- Current licensing, qualification, legality, solvency, safety, or suitability of any company, product, or arrangement.
- Material coverage of any complete body of law, regulation, accounting, audit, Bitcoin operations, or institutional policy.
- Jurisdiction and applicability analysis, effective dates, amendment history, precedent, exceptions, safe harbors, or conflicting authorities.
- Authentication of recorded evidence metadata, issuers, reviewers, hashes, signatures, or chains of custody. The schema can record them; the software cannot prove them.
- Full truth maintenance, calibrated uncertainty, expert approval, change-impact analysis, or signed releases.
- Independently reviewed cases, external validation data, coverage measures, error rates, or usability evidence.
- Production controls: authentication, authorization, audit logs, security design, backups, monitoring, or a threat model.
- Continuous integration, link checking, source freshness, regulatory monitoring, news ingestion, or alerts.

The generated PDF is research output, not a certification, audit opinion, proof of reserves, legal instrument, compliance report, or regulatory filing.

### Web interface

The web UI is a static application in `dist/`. It has no server, database, accounts, API, persistence, semantic search, RAG, or LLM. It reads a generated snapshot; run `python3 -m src.build_web` after changing the domain files.

Assessment selections are not saved. The UI cannot upload or inspect evidence, query a Bitcoin node, check signatures, or inspect transactions. Its questionnaire is explicitly an unverified learning sandbox; it does not run the evidence-backed Python assessment. Source links open external pages, but the repository does not archive or hash their contents. The `Snapshot generated on` date shown by the UI is the snapshot build point; the `checked_on` dates recorded on sources and the assessment are metadata, not evidence that every record was rechecked on that date.

## Research thesis

Bitcoin supplies narrow, machine-verifiable guarantees: signature validity, script satisfaction, ledger state, and cryptographic commitments. Finance and law also require facts about identity, authority, ownership, liabilities, controls, succession, and remedies. Products and institutions operate at the interfaces between those systems.

This framing assumes that moving traditionally governed capital onto Bitcoin is worth studying. It does not establish that such a move is desirable in a particular case.

## Ontology, epistemology, and axiology

These identify different failure modes:

- **Ontology:** the model contains the wrong entities or relationships.
- **Epistemology:** a claim exceeds its evidence.
- **Axiology:** the system gives priority to the wrong values, people, or harms.

Ontology concerns what exists; epistemology concerns knowledge and justification; axiology concerns value. Epistemology is not merely methodology, and axiology is not merely bias. Background: [metaphysics and ontology](https://plato.stanford.edu/entries/plato-metaphysics/), [epistemology](https://plato.stanford.edu/archives/fall2018/entries/epistemology/), [knowledge](https://plato.stanford.edu/entries/knowledge-analysis/), and [value theory](https://plato.stanford.edu/archives/spr2023/entries/value-theory/).

### Ontology

The current model recognizes:

| Entity | Meaning here |
| --- | --- |
| Bitcoin capability | A property established by Bitcoin verification rules |
| Finance requirement | A financial fact or control not supplied by Bitcoin alone |
| Legal requirement | A concept such as ownership, capacity, authority, succession, or remedy |
| Bridge | A product or function connecting Bitcoin capabilities to financial or legal requirements |
| Company | A named market participant assigned to bridge categories |
| Claim | A proposition asserted by the project |
| Source | A URL and metadata offered in support |
| Rule | Conditions mapped to a derived conclusion |
| Evidence record | An assertion linked to an artifact, issuer, provenance, scope, and review activity |
| Case fact | A Boolean value derived from accepted, applicable evidence records |
| Assessment requirement | An evidence question in a pre-review |
| Outcome | A computed label such as `not_ready` |

```text
BitcoinCapability ----supports----> Bridge
FinanceRequirement ---required_by-> Bridge
LegalRequirement -----required_by-> Bridge
Company --------------assigned_to-> Bridge
Claim ----------------supported_by-> Source
Rule -----------------uses_facts---> Conclusion
AssessmentRequirement-cites-------> Source
EvidenceRecord -------supports-----> CaseFact
```

Cryptographic control, legal ownership, beneficial entitlement, identity, authority, and consent are distinct. A valid signature establishes a cryptographic result, not legal title.

Current modeling defects:

- The schema is a project vocabulary, not evidence that its categories match reality.
- `Bridge` is not a standard legal, accounting, or Bitcoin category. Its seven categories have not been independently reviewed.
- `Company` collapses brands, legal entities, licenses, jurisdictions, products, contracts, and custody models into one record.
- `Source` is mainly a URL; passages, authors, issuing authority, publication history, jurisdiction, legal status, and supersession are incomplete.
- Five general legal concepts stand in for statutes, regulations, cases, contracts, legal tests, exceptions, burdens, and remedies.
- Jurisdiction and time are not first-class participants in inference.
- The new evidence record preserves artifact, issuer, subject, reviewer, method, scope, jurisdiction, dates, integrity metadata, and review disposition. The final proposition is still Boolean, so contested degrees, partial scope, compound claims, and legal sufficiency remain flattened.
- Persons, organizations, accounts, wallets, descriptors, keys, UTXOs, transactions, contracts, trusts, estates, beneficiaries, regulators, courts, and auditors are not fully typed.
- There is no identity-resolution model for names, keys, accounts, subsidiaries, or documents.

The current model is a taxonomy with a few executable propositions, not a mature ontology.

### Epistemology

The system draws on four kinds of input:

1. Simplified Bitcoin verification rules and technical sources.
2. External publications represented by URLs and metadata.
3. Project-authored claims, classifications, requirements, and rules.
4. User-supplied evidence records whose authenticity is not independently established.

Claim statuses, evidence levels, rule traces, open-world handling, and conflict reporting improve inspectability. They do not establish that a premise is true, a source applies, a rule is valid, or a conclusion is correct. A trace establishes only that a particular rule version transformed accepted premises into an output.

The intended evidence ladder is:

```text
Referenced       A source URL is recorded.
Extracted        A specific passage is captured accurately.
Interpreted      The project states what the passage means.
Applicable       Jurisdiction, entity, product, role, and date match.
Corroborated     Independent relevant evidence supports the proposition.
Case-evidenced   Authentic case evidence supports the proposition.
Expert-reviewed  A qualified reviewer accepts the scoped reasoning.
Decision-grade   Evidence, rules, controls, and accountability meet a defined use standard.
```

Most current material is only referenced or project-interpreted.

Epistemic weaknesses:

- Citations usually identify whole documents, not passages or archived versions.
- Attaching a source ID does not show that the source entails the claim or rule.
- The evidence-level number conflates authority, independence, relevance, and reproducibility.
- Primary sources establish what an institution said, not necessarily that it is true.
- Company material may describe features while remaining poor evidence of safety, solvency, effectiveness, or legal status.
- Regulatory guidance may be nonbinding, jurisdiction-limited, superseded, or addressed only to particular entities.
- Contrary evidence and source disagreement are not modeled systematically.
- There are no source snapshots, hashes, passage citations, link checks, or supersession detection.
- Claims do not identify individual extractors, interpreters, or reviewers.
- `corroborated` has no formal independence, relevance, or sufficiency test.
- Company classifications generally lack claim-level citations and dates.
- The engine checks evidence-record structure, review disposition, jurisdiction, validity period, and conflicts, but it cannot authenticate the record or determine whether the review was competent.
- Accuracy, recall, false-assurance risk, and reviewer agreement are unknown.

The repository can show what it asserts, where it looked, and how code transformed inputs. It cannot yet defend its conclusions as professional knowledge.

### Axiology

The project is not neutral. It studies how traditionally governed capital can move onto Bitcoin, which directs attention toward enabling institutional bridges.

Declared priorities:

- Report missing or conflicting information instead of filling gaps.
- Prefer `unknown` or `insufficient_information` to unsupported approval.
- Expose facts, rules, and sources behind conclusions.
- Produce repeatable results from versioned inputs.
- Keep cryptographic control separate from legal ownership.
- Avoid false assurance: a failed requirement yields `not_ready`; missing evidence prevents readiness.
- Leave consequential judgment with accountable, qualified people.
- Keep assumptions and errors open to criticism.

Contestable choices:

- The institutional focus privileges custodians, banks, lawyers, trustees, auditors, and regulators. Self-custody, privacy, permissionlessness, resistance to seizure, and people excluded by traditional finance receive less attention.
- The first assessment privileges US federal banking and New York regulatory perspectives.
- Measuring institutional readiness does not establish that an arrangement benefits customers, beneficiaries, society, or Bitcoin's decentralization.
- Conservative abstention may reduce false assurance while increasing false negatives, cost, delay, and exclusion; this tradeoff is not measured.
- The source hierarchy privileges institutions and formal publications. Operational knowledge, open-source investigation, whistleblowers, lived experience, and affected users are underrepresented.
- Inclusion in the company map can imply legitimacy despite the absence of due diligence.
- Compliance, safety, customer protection, privacy, autonomy, recoverability, and censorship resistance can conflict. No value-conflict procedure exists.
- The project has not decided whose welfare controls when owners, beneficiaries, fiduciaries, custodians, regulators, creditors, and the Bitcoin network have different interests.
- The system could support education and accountability, or be misused as compliance theater.

The present stance favors transparent, conservative, institution-compatible movement onto Bitcoin. It should be treated as a declared position, not neutral fact.

Every future rule or assessment should answer:

1. **Ontology:** Which entities, relationships, jurisdiction, role, and time does it concern?
2. **Epistemology:** What supports or defeats its premises and conclusion, and who reviewed the interpretation?
3. **Axiology:** Which value or harm does it prioritize, who benefits, who bears the cost, and how are conflicts escalated?

## Domain model

Structured research lives in [`domain/model.json`](domain/model.json). Rules are in [`domain/rules.json`](domain/rules.json); the current assessment is in [`domain/assessments/custody-readiness.json`](domain/assessments/custody-readiness.json).

## Commands

Python 3.11 or later is required. Core validation and inference use the standard library; PDF generation uses ReportLab.

```bash
python3 -m src.cli validate
python3 -m src.cli build
python3 -m src.cli build-pdf
python3 -m src.cli infer examples/institutional-custody.json
python3 -m src.cli assess examples/custody-readiness-complete.json
python3 -m src.cli assess examples/custody-readiness-gaps.json
python3 -m src.build_example_cases
python3 -m src.build_web
python3 -m unittest discover -s tests
```

- `build` writes `generated/market-map.md`.
- `build-pdf` writes `output/pdf/domain-map.pdf` from the model.
- `infer` evaluates JSON facts against the rules and returns a trace.
- `assess` runs the custody pre-review and then passes accepted, applicable evidence facts into the inference rules, reporting derived conclusions such as `custody_bridge_ready` and `legal_authority_gap`.
- `build_example_cases` regenerates the explicitly synthetic evidence cases.
- `build_web` refreshes `dist/knowledge.js` for the static UI.

Validation now enforces the honesty standards as fail-fast checks: claim statuses cannot exceed their sources, rules and assessment requirements must use the shared fact registry, and the model, rules, assessment, and registry versions must agree.

## Publications

- [`v0.1.0 research paper`](publications/v0.1.0/bitcoin-bridge-market-research-draft.pdf)
- [`v0.1.0 release notes`](publications/v0.1.0/RELEASE_NOTES.md)
- [`v0.1.0 paper notice`](publications/v0.1.0/NOTICE.md) — states which paper claims the model supports and which names are illustrative only.

## Evidence policy

Material claims should identify sources and carry a status: `unverified`, `supported`, `corroborated`, `contested`, `stale`, or `retracted`.

The current evidence levels are:

1. Company marketing
2. Official technical documentation
3. Regulatory or legal filing
4. Independent professional evidence
5. Reproducible primary data

This scale is provisional and conflates properties that should be modeled separately.

## Scope and contributions

The market map is representative, not exhaustive. Company classifications and legal sources can become stale. See [`CONTRIBUTING.md`](CONTRIBUTING.md). Contributions should improve the model, evidence, or interpretation rather than add unsupported prose.
