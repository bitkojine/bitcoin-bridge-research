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

## Philosophical audit: ontology, epistemology, and axiology

These terms are not decorative research language. They expose three different ways this system can be wrong:

- **Ontological error:** the model contains the wrong kinds of things or relationships.
- **Epistemic error:** the system claims more than its evidence justifies.
- **Axiological error:** the system optimizes for the wrong values, people, or harms.

The shorthand is useful but incomplete: ontology asks what exists; epistemology asks what can be known and on what grounds; axiology asks what is valuable and how values compare. Epistemology is not merely “methodology,” and axiology is not merely “bias.” For background, see the Stanford Encyclopedia of Philosophy on [metaphysics and ontology](https://plato.stanford.edu/entries/plato-metaphysics/), [epistemology](https://plato.stanford.edu/archives/fall2018/entries/epistemology/), [the analysis of knowledge](https://plato.stanford.edu/entries/knowledge-analysis/), and [value theory](https://plato.stanford.edu/archives/spr2023/entries/value-theory/).

### Ontology: what this repository says exists

The repository's current operational ontology recognizes these types of things:

| Entity | What the repository currently means by it |
| --- | --- |
| Bitcoin capability | A narrow property that Bitcoin's verification rules can establish, such as signature validity, threshold satisfaction, or selected ledger state |
| Finance requirement | A fact or control an institutional financial arrangement may require beyond native Bitcoin verification |
| Legal requirement | A legally relevant concept such as ownership, capacity, authority, succession, or remedy |
| Bridge | A product or institutional function connecting Bitcoin capabilities to financial or legal requirements |
| Company | A named market participant assigned to one or more bridge categories |
| Claim | A proposition asserted by the research project |
| Source | A URL and metadata record offered in support of claims, rules, or requirements |
| Rule | An explicit conditional mapping from supplied facts to a derived conclusion |
| Case fact | A value supplied to the inference or assessment code; currently usually a Boolean |
| Assessment requirement | An evidence question used by one pre-review workflow |
| Outcome | A computed label such as `not_ready` or `insufficient_information` |

The principal modeled relationships are:

```text
BitcoinCapability ---supports---> Bridge
FinanceRequirement --required_by-> Bridge
LegalRequirement ----required_by-> Bridge
Company -------------assigned_to-> Bridge
Claim -------------supported_by-> Source
Rule -----------------uses_facts-> Conclusion
AssessmentRequirement-cites-----> Source
```

The most important ontological commitment is that **cryptographic control, legal ownership, beneficial entitlement, identity, authority, and consent are different relationships**. A valid Bitcoin signature belongs to the ontology of cryptographic verification. It is not transformed into legal title merely by attaching a person's name to it.

#### Ontological limits and category problems

- The JSON schema is a software vocabulary, not proof that its categories correspond perfectly to reality.
- `Bridge` is a project-created analytical category. It is not a standard legal, accounting, or Bitcoin category, and its seven subcategories have not been validated by independent experts.
- `Company` is radically under-modeled. A brand may contain several legal entities, licenses, jurisdictions, products, custody models, and changing contractual roles; the repository currently collapses these into one name.
- `Source` is modeled mostly as a URL. The actual document, author, issuing authority, publication history, relevant passage, jurisdiction, legal status, and supersession relationships are not fully modeled.
- Law is under-modeled as five general nouns. Statutes, regulations, cases, contracts, guidance, legal tests, exceptions, burdens of proof, remedies, and conflicts of law are not represented as distinct entities.
- Time is under-modeled. A global verification date is not a temporal model for individual facts, rules, products, licenses, or authorities.
- Jurisdiction is described in prose but is not a first-class entity participating in inference.
- Evidence is not yet a first-class case object. A Boolean such as `legal_authority_evidenced: true` collapses the document, issuer, subject, reviewer, review method, scope, date, authenticity, expiry, and unresolved exceptions into one bit.
- Persons, organizations, accounts, wallets, descriptors, keys, UTXOs, transactions, contracts, trusts, estates, beneficiaries, regulators, courts, and auditors are discussed but not yet fully represented as typed entities.
- The system has no identity-resolution model. It cannot know whether two names, keys, accounts, subsidiaries, or documents refer to the same real-world entity.

The brutal conclusion: this is presently a **taxonomy with a few executable propositions**, not a mature domain ontology.

### Epistemology: what this repository can claim to know

The repository currently has four possible epistemic inputs:

1. **Bitcoin verification rules**, represented by simplified formulas and technical sources.
2. **External publications**, represented by source metadata and URLs.
3. **Project-authored interpretation**, represented by claims, category assignments, assessment requirements, and rules.
4. **User-supplied case facts**, accepted as inputs without authentication.

Its current epistemic mechanisms are limited:

- Claim statuses distinguish `unverified`, `supported`, `corroborated`, `contested`, `stale`, and `retracted`.
- Evidence levels classify the general kind of source.
- Rules expose their conditions, conclusions, and source identifiers.
- Open-world handling prevents a missing fact from becoming a negative fact.
- Conflict reporting preserves incompatible values instead of silently overwriting them.
- Proof traces explain how a conclusion was mechanically derived from the accepted premises.

Those mechanisms improve transparency, but they do not establish knowledge. A proof trace proves only:

> Given these encoded premises and this rule version, the program produced this conclusion.

It does **not** prove that the premises are true, that the rule is legally valid, that its sources apply, or that the conclusion is correct in the world.

#### Current epistemic ladder

The system should distinguish these levels, but does not yet enforce all of them:

```text
Referenced     A source URL was recorded.
Extracted      A specific passage was captured accurately.
Interpreted    The project stated what that passage means.
Applicable     Jurisdiction, entity, product, role, and date were matched.
Corroborated   Independent relevant evidence supports the proposition.
Case-evidenced Authentic evidence supports the proposition in this case.
Expert-reviewed A qualified reviewer accepted the reasoning within a stated scope.
Decision-grade The evidence, rules, controls, and accountability meet a defined use standard.
```

Today, much of the repository is only at **referenced** or **project-interpreted**. The interface can make that material easy to browse, but presentation quality must not be confused with epistemic maturity.

#### Epistemic weaknesses

- Most citations point to whole documents or pages, not exact passages, sections, quotations, or archived versions.
- A source identifier attached to a rule does not demonstrate that the source entails the rule.
- The source-level hierarchy mixes authority, independence, and reproducibility into one number. Those are different epistemic properties.
- A primary source can be authoritative about what an institution said while still being weak evidence that the statement is true.
- Company self-description may be the best source for a product feature and a poor source for safety, solvency, effectiveness, or legal status.
- Regulatory guidance may be highly relevant but nonbinding, jurisdiction-limited, superseded, or addressed only to specific regulated entities.
- The system records little contrary evidence and has no systematic source-disagreement model.
- It has no source snapshots, content hashes, passage-level citations, automated link checking, or supersession detection.
- It has no named researcher, extractor, interpreter, legal reviewer, or approval record attached to individual propositions.
- `corroborated` is not backed by a formal test for independence, relevance, or sufficiency.
- Company-to-bridge assignments generally lack claim-by-claim citations and verification dates.
- The assessment accepts unchecked Boolean assertions. It does not inspect the evidence it tells the user to obtain.
- The system has not been tested against external expert judgments, so accuracy, recall, false-assurance risk, and inter-reviewer agreement are unknown.

The brutal conclusion: the repository can currently show **what it asserts, where it looked, and how code transformed inputs**. It cannot yet show that it knows its conclusions in a professionally defensible sense.

### Axiology: what this repository values

This project is not value-neutral. Its founding purpose is to study how money governed by traditional finance and law can move onto Bitcoin. That framing already treats such movement as worth investigating and focuses attention on enabling bridges rather than asking only whether the movement should happen.

The repository currently expresses these values:

- **Truth over persuasion:** expose missing knowledge and contradictory evidence rather than manufacture certainty.
- **Restraint over fluent guessing:** prefer `unknown` and `insufficient_information` to an unsupported affirmative conclusion.
- **Traceability over authority theater:** conclusions should expose their facts, rules, and sources.
- **Reproducibility over discretionary opacity:** the same versioned inputs should produce the same mechanical result.
- **Separation of powers:** cryptography should not silently decide legal ownership, and legal language should not pretend to alter Bitcoin's verification rules.
- **Protection against false assurance:** an explicit failed requirement currently produces `not_ready`; missing evidence prevents `ready_for_expert_review`.
- **Human accountability:** consequential conclusions should remain reviewable by identifiable qualified people.
- **Open criticism:** the public repository should make assumptions and errors inspectable.

#### Hidden and contestable value choices

- The project privileges an institutional lens: custodians, banks, lawyers, trustees, auditors, and regulators. Individual self-custody, privacy, permissionlessness, resistance to seizure, and people excluded by traditional finance receive less representation.
- The first assessment privileges US federal banking and New York regulatory perspectives. This is a scope choice, not a universal hierarchy of values.
- The system treats institutional readiness as desirable enough to measure. It does not yet model whether a proposed arrangement is desirable for customers, beneficiaries, society, or Bitcoin's decentralization.
- Conservative abstention reduces false assurance but may increase false negatives, cost, delay, and exclusion. The repository has not formally chosen or measured that tradeoff.
- The source hierarchy implicitly privileges institutions and formal publications. Lived experience, operational knowledge, open-source investigation, whistleblowers, and affected users are not adequately represented.
- The company map can confer legitimacy merely by inclusion and visual prominence, even when the repository has performed no due diligence.
- “Compliance,” “safety,” “customer protection,” “privacy,” “autonomy,” “recoverability,” and “censorship resistance” can conflict. The system has no explicit value-conflict procedure.
- The project has not defined whose welfare controls when the interests of asset owners, beneficiaries, fiduciaries, custodians, regulators, creditors, and the wider Bitcoin network diverge.
- A public system can educate and improve accountability, but it can also be used for compliance theater or to make weak arrangements look formally reviewed.

The brutal conclusion: the repository favors transparent, conservative, institution-compatible movement onto Bitcoin. That is a defensible research stance, but it is still a stance. It must be declared, challenged, and prevented from masquerading as neutral truth.

### How the three constrain one another

| If we get this wrong | Resulting failure |
| --- | --- |
| Ontology without epistemology | The system models elegant entities but cannot justify claims about real cases |
| Epistemology without ontology | Evidence is collected against vague or conflated concepts such as control, custody, and ownership |
| Ontology and epistemology without axiology | The system can classify and infer without examining whose interests or harms guide the classifications |
| Axiology without epistemology | Desired outcomes are presented as facts |
| Axiology without ontology | Values attach to abstractions that omit the affected people, rights, institutions, and power relationships |

For every future rule or assessment, the repository should therefore require three answers:

1. **Ontology:** What exact entities, relationships, jurisdiction, role, and time does this rule concern?
2. **Epistemology:** What evidence would justify the premises and conclusion, what would defeat them, and who reviewed the interpretation?
3. **Axiology:** Which value or harm does the rule prioritize, who benefits, who bears the cost, and how are conflicts escalated?

Until the repository can answer those questions at the level of individual claims and cases, its output remains structured research—not expertise.

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
