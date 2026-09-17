# Notice on the relationship between the research paper and the repository model

## What this paper is

`bitcoin-bridge-market-research-draft.pdf` is a separately authored, human-written research essay. It is **not generated** from `domain/model.json` and is **not a report view** over the repository's facts, rules, and sources in the sense described in `research/expert-system-architecture.md`.

## What the repository record supports

- The machine-checkable boundary of this repository is `domain/model.json`: 3 Bitcoin capabilities, 6 finance requirements, 5 legal requirements, 7 bridge categories, 15 companies, 2 claims with source links, and 8 sources.
- Every company the paper names is inventoried in `publications/v0.1.0/PAPER_COMPANIES.json`:
  - `in_model: true` — the name exists in the model register.
  - `in_model: false` with `illustrative_only: true` — the paper names the company, but the repository holds no claim, source, or evidence record for it. This is illustration, not diligence.
- The paper's source list ("official custody, wallet, inheritance, reserve and security documentation from BitGo, Unchained, Casa, Fireblocks, River, Kraken, Anchorage Digital, Fidelity Digital Assets and Chainalysis") is not recorded in `domain/model.json` (which contains 8 sources: BIP-322, Bitcoin Developer Guide, OCC, ICAEW, NYDFS, OCC Interpretive Letter 1184, W3C PROV-O, W3C Verifiable Credentials).

## What should not be inferred

The paper's prose conclusions — for example "the bridge is already a major market" or that any named company is suitable, solvent, licensed, or safe — are the author's interpretation. They are not supported by the repository's 2 claims and 8 sources, and they must not be read as findings of this research system.

## Maintenance rule

Anyone who edits the paper must update `PAPER_COMPANIES.json` so the named-participant inventory stays truthful, or the consistency test (`tests/test_artifacts.py`) fails.