# From domain map to expert system

## The governing idea

An expert system does not discover absolute truth. It applies an explicit knowledge base to supplied facts and returns conclusions that are reproducible **under those facts, rules, priorities, and assumptions**. Its advantage is inspectability: every conclusion can identify the rule and evidence path that produced it.

For this project, the system's narrow domain is the bridge between Bitcoin's machine-verifiable guarantees and the facts required by traditional finance and law. It should answer questions such as:

- What does the supplied Bitcoin evidence establish?
- Which legal or financial requirement remains unsupported?
- Which existing bridge category and companies address that gap?
- Why did the system reach that conclusion, and what fact would change it?

It must not give legal advice, certify facts it has not observed, or turn missing information into a negative fact.

## Architecture

1. **Ontology and typed facts.** Stable concepts define Bitcoin capabilities, financial requirements, legal requirements, bridge products, companies, jurisdictions, evidence, and decisions. Terms have one documented meaning.
2. **Working memory.** A case supplies facts with provenance, observation date, jurisdiction, and eventually confidence or dispute status. Missing means unknown, not false.
3. **Knowledge base.** Small rules express specialist judgment as conditions and conclusions. Each rule has an identifier, plain-language rationale, priority, sources, owner, review date, and tests.
4. **Inference engine.** Forward chaining matches known facts, places eligible rules on an agenda, resolves conflicts deterministically, fires rules, and repeats until no new fact is derived.
5. **Explanation facility.** Every result supports “how,” “why,” and “why not”: rules fired, facts consumed, conclusions produced, sources used, conflicts found, and missing prerequisites.
6. **Truth and conflict management.** Derived facts retain their justifications. If a premise is withdrawn, dependent conclusions must eventually be withdrawn. Contradictory claims are surfaced, not silently overwritten.
7. **Verification and validation.** Static checks find missing references, duplicate or unreachable rules, cycles, conflicting conclusions, and gaps. Scenario tests compare conclusions with reviewed expert cases.
8. **Knowledge acquisition and governance.** Named domain experts propose rules; research evidence supports them; reviewers approve changes; versions and effective dates make every output reproducible.
9. **Presentation layer.** Reports and PDFs are views over the same facts, rules, proof traces, and sources—not separately maintained truth.

## What makes one great

- **Narrow competence with explicit boundaries.** It says which jurisdiction, product, date, and decision it covers.
- **Abstention as a feature.** Unknown, unsupported, contested, stale, and out-of-scope are first-class outcomes.
- **Semantic precision.** “Key control,” “ownership,” “custody,” “entitlement,” and “authority” are never treated as synonyms.
- **Deterministic, testable behavior.** Identical versioned inputs produce identical outputs. Rule priority is deliberate rather than dependent on file order.
- **Complete explanations.** A reader can inspect the full proof and the absent prerequisites, not merely a prose justification generated after the event.
- **Evidence provenance.** Facts and rules link to primary sources, dates, jurisdictions, and reviewers.
- **Managed uncertainty.** Probabilities, expert confidence, legal ambiguity, and source quality remain distinct instead of being collapsed into one unexplained score.
- **Conflict visibility.** Disagreement between authorities or experts can be legitimate. The system records competing conclusions and escalation rules.
- **Coverage measurement.** A decision table shows which combinations are handled; boundary, counterexample, regression, and adversarial cases are tested.
- **Safe change control.** Proposed rule changes show affected conclusions before publication and preserve prior versions.
- **Human accountability.** The system supports professional judgment and records review; it does not disguise automation as legal authority.

## Role of an LLM

An LLM can translate questions, suggest candidate facts, summarize sources, draft explanations, and help locate missing knowledge. It must not silently create authoritative facts or rules. Candidate extractions require provenance and validation before entering working memory; candidate rules require expert review and tests. The symbolic engine remains the decision authority for governed conclusions.

## Verification programme

For every decision family, maintain:

- positive cases where a rule must fire;
- near-miss cases with one prerequisite absent;
- explicit-false cases, kept distinct from unknown cases;
- contradictory cases that must trigger conflict;
- jurisdiction and effective-date boundary cases;
- expert-approved “golden” cases and regression outputs;
- coverage reports showing facts and rules never exercised.

Static rule checks are necessary but insufficient. Verification asks whether the implementation matches its specification. Validation asks whether the specification and conclusions are appropriate in real professional use. Both require documented assumptions and independent review.

## Delivery stages

**Current kernel:** deterministic forward chaining, priority ordering, open-world semantics, proof traces, and contradiction reporting.

**Next:** schema validation; source, jurisdiction, and effective-date metadata; “why not” explanations; rule linting; golden cases; coverage measurement.

**Later:** justification-based truth maintenance, controlled uncertainty, expert review workflow, impact analysis, and an LLM interface that can only submit cited candidate facts.

The repository should earn the label “expert system” through evaluated domain coverage and expert governance—not merely because it contains an inference engine.
