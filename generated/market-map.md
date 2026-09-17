# Bitcoin Bridge Market Map

Version: `0.3.0`  
Snapshot generated on: `2026-09-18`

Commercial territory forms where companies connect Bitcoin's verifiable state and signing rules to the institutional facts required by finance and law.

## Bitcoin capabilities

### Signature validity

`Verify(pk, m, sig) = 1`

- **pk**: public key
- **m**: exact message or transaction
- **sig**: signature
- **1**: the verification rule accepts the signature

Establishes: The cryptographic verification rule accepted the signature for the supplied data.

### Threshold control

`valid signers >= t of n`

- **valid signers**: participants satisfying the signing policy
- **t**: minimum number required
- **n**: total configured participants
- **>=**: at least

Establishes: The configured cryptographic threshold was satisfied.

### Ledger state

`Balance(U, h) = sum(value(u))`

- **U**: selected set of unspent outputs
- **h**: block height
- **u**: one unspent output
- **sum**: addition of the selected output values

Establishes: The selected unspent outputs existed in the accepted ledger state at the specified height.

## Bridge market

### Access and execution

Companies: **Anchorage Digital**, **Coinbase Custody**, **Fidelity Digital Assets**, **Kraken**, **River**

### Regulated custody

Companies: **Anchorage Digital**, **BitGo**, **Coinbase Custody**, **Copper**, **Fidelity Digital Assets**

### Collaborative custody

Companies: **BitGo**, **Casa**, **Nunchuk**, **Unchained**

### Wallet governance

Companies: **BitGo**, **Copper**, **Fireblocks**, **Fordefi**

### Reserve and audit evidence

Companies: **Kraken**, **River**

### Blockchain attribution

Companies: **Chainalysis**, **Elliptic**, **TRM Labs**

### Succession and continuity

Companies: **Casa**, **Unchained**

## Claims

- **corroborated** - A valid signature does not by itself establish legal ownership or lawful authority. Treatments: bip-322 (supports), icaew-audit (supports).
- **supported** - Institutional crypto safekeeping remains subject to existing custody, fiduciary, information-security, and legal requirements. Treatments: occ-safekeeping (supports).

## Sources

- **BIP-322 Generic Signed Message Format** (`bip-322`, level 5, currency current). Checked on: `2026-09-17`. https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki
- **Bitcoin Developer Guide - Transactions** (`bitcoin-transactions`, level 5, currency current). Checked on: `2026-09-17`. https://developer.bitcoin.org/devguide/transactions.html
- **Crypto-Asset Safekeeping by Banking Organizations** (`occ-safekeeping`, level 3, currency current). Checked on: `2026-09-17`. https://www.occ.gov/news-issuances/news-releases/2025/nr-ia-2025-68a.pdf
- **Considerations for Auditing Cryptocurrencies** (`icaew-audit`, level 4, currency current). Checked on: `2026-09-17`. https://www.icaew.com/technical/technology/blockchain-and-cryptoassets/blockchain-helpsheets/considerations-for-auditing-cryptocurrencies
- **Updated Guidance on Custodial Structures for Customer Protection in the Event of Insolvency** (`nydfs-custody-2025`, level 3, currency current). Checked on: `2026-09-17`. https://www.dfs.ny.gov/industry-guidance/industry-letters/il20250930-updated-guidance-custodial-structures
- **Interpretive Letter 1184: Crypto-Asset Custody and Execution Services** (`occ-il-1184`, level 3, currency current). Checked on: `2026-09-17`. https://www.occ.gov/topics/charters-and-licensing/interpretations-and-decisions/2025/int1184.pdf
- **PROV-O: The PROV Ontology** (`w3c-prov-o`, level 2, currency current). Checked on: `2026-09-17`. https://www.w3.org/TR/prov-o/
- **Verifiable Credentials Data Model v2.0** (`w3c-vc-data-model`, level 2, currency current). Checked on: `2026-09-17`. https://www.w3.org/TR/vc-data-model/
