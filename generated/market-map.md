# Bitcoin Bridge Market Map

Version: `0.1.0`  
Verified on: `2026-09-17`

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

- **corroborated** - A valid signature does not by itself establish legal ownership or lawful authority. Sources: bip-322, icaew-audit
- **corroborated** - Institutional crypto safekeeping remains subject to existing custody, fiduciary, information-security, and legal requirements. Sources: occ-safekeeping
