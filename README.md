# Bitcoin Bridge Research

An open, versioned research project mapping how capital governed by traditional finance and law can move onto the Bitcoin blockchain.

The repository is the research engine. Versioned PDF papers are compiled outputs.

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

Requires Python 3.11 or later and has no third-party runtime dependencies.

```bash
python3 -m src.cli validate
python3 -m src.cli build
python3 -m src.cli build-pdf
python3 -m unittest discover -s tests
```

`build` produces [`generated/market-map.md`](generated/market-map.md), a human-readable view generated from the domain model.

`build-pdf` produces [`output/pdf/domain-map.pdf`](output/pdf/domain-map.pdf) directly from the same model. This is a compact, reproducible research output rather than the separately authored long-form paper.

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
