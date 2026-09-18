window.KNOWLEDGE = {
  "model": {
    "meta": {
      "title": "Bitcoin Bridge Market Map",
      "version": "0.3.0",
      "generated_on": "2026-09-18",
      "thesis": "Commercial territory forms where companies connect Bitcoin's verifiable state and signing rules to the institutional facts required by finance and law."
    },
    "bitcoin_capabilities": [
      {
        "id": "signature-validity",
        "name": "Signature validity",
        "formula": "Verify(pk, m, sig) = 1",
        "terms": {
          "pk": "public key",
          "m": "exact message or transaction",
          "sig": "signature",
          "1": "the verification rule accepts the signature"
        },
        "establishes": "The cryptographic verification rule accepted the signature for the supplied data.",
        "does_not_establish": [
          "legal identity",
          "legal ownership",
          "lawful authority",
          "voluntary intent"
        ]
      },
      {
        "id": "threshold-control",
        "name": "Threshold control",
        "formula": "valid signers >= t of n",
        "terms": {
          "valid signers": "participants satisfying the signing policy",
          "t": "minimum number required",
          "n": "total configured participants",
          ">=": "at least"
        },
        "establishes": "The configured cryptographic threshold was satisfied.",
        "does_not_establish": [
          "organizational authority",
          "fiduciary compliance"
        ]
      },
      {
        "id": "ledger-state",
        "name": "Ledger state",
        "formula": "Balance(U, h) = sum(value(u))",
        "terms": {
          "U": "selected set of unspent outputs",
          "h": "block height",
          "u": "one unspent output",
          "sum": "addition of the selected output values"
        },
        "establishes": "The selected unspent outputs existed in the accepted ledger state at the specified height.",
        "does_not_establish": [
          "beneficial ownership",
          "completeness of disclosure"
        ]
      }
    ],
    "finance_requirements": [
      {
        "id": "identity",
        "name": "Client and beneficial-owner identity"
      },
      {
        "id": "asset-entitlement",
        "name": "Account-level asset entitlement"
      },
      {
        "id": "authorization",
        "name": "Authenticated institutional authorization"
      },
      {
        "id": "accounting",
        "name": "Accounting, valuation, and reconciliation"
      },
      {
        "id": "solvency",
        "name": "Asset and liability coverage"
      },
      {
        "id": "recourse",
        "name": "Contractual and regulated recourse"
      }
    ],
    "legal_requirements": [
      {
        "id": "legal-ownership",
        "name": "Legal ownership or beneficial entitlement"
      },
      {
        "id": "legal-capacity",
        "name": "Capacity and legal personality"
      },
      {
        "id": "lawful-authority",
        "name": "Authority under mandate, office, trust, or court order"
      },
      {
        "id": "succession",
        "name": "Death, probate, trust, and beneficiary succession"
      },
      {
        "id": "remedies",
        "name": "Enforceable remedies after fraud, error, or breach"
      }
    ],
    "bridges": [
      {
        "id": "access-execution",
        "name": "Access and execution",
        "bitcoin_capabilities": [
          "ledger-state"
        ],
        "finance_requirements": [
          "accounting"
        ],
        "legal_requirements": []
      },
      {
        "id": "regulated-custody",
        "name": "Regulated custody",
        "bitcoin_capabilities": [
          "signature-validity",
          "threshold-control",
          "ledger-state"
        ],
        "finance_requirements": [
          "identity",
          "asset-entitlement",
          "authorization",
          "recourse"
        ],
        "legal_requirements": [
          "legal-ownership",
          "legal-capacity",
          "lawful-authority",
          "remedies"
        ]
      },
      {
        "id": "collaborative-custody",
        "name": "Collaborative custody",
        "bitcoin_capabilities": [
          "threshold-control"
        ],
        "finance_requirements": [
          "authorization"
        ],
        "legal_requirements": [
          "lawful-authority",
          "succession"
        ]
      },
      {
        "id": "wallet-governance",
        "name": "Wallet governance",
        "bitcoin_capabilities": [
          "signature-validity",
          "threshold-control"
        ],
        "finance_requirements": [
          "authorization"
        ],
        "legal_requirements": [
          "lawful-authority"
        ]
      },
      {
        "id": "reserve-evidence",
        "name": "Reserve and audit evidence",
        "bitcoin_capabilities": [
          "ledger-state",
          "signature-validity"
        ],
        "finance_requirements": [
          "accounting",
          "solvency"
        ],
        "legal_requirements": [
          "legal-ownership"
        ]
      },
      {
        "id": "attribution",
        "name": "Blockchain attribution",
        "bitcoin_capabilities": [
          "ledger-state"
        ],
        "finance_requirements": [
          "identity"
        ],
        "legal_requirements": [
          "legal-capacity"
        ]
      },
      {
        "id": "succession-bridge",
        "name": "Succession and continuity",
        "bitcoin_capabilities": [
          "threshold-control"
        ],
        "finance_requirements": [
          "identity",
          "asset-entitlement"
        ],
        "legal_requirements": [
          "legal-ownership",
          "lawful-authority",
          "succession"
        ]
      }
    ],
    "companies": [
      {
        "id": "coinbase-custody",
        "name": "Coinbase Custody",
        "bridges": [
          "access-execution",
          "regulated-custody"
        ]
      },
      {
        "id": "bitgo",
        "name": "BitGo",
        "bridges": [
          "regulated-custody",
          "wallet-governance",
          "collaborative-custody"
        ]
      },
      {
        "id": "anchorage-digital",
        "name": "Anchorage Digital",
        "bridges": [
          "access-execution",
          "regulated-custody"
        ]
      },
      {
        "id": "fidelity-digital-assets",
        "name": "Fidelity Digital Assets",
        "bridges": [
          "access-execution",
          "regulated-custody"
        ]
      },
      {
        "id": "fireblocks",
        "name": "Fireblocks",
        "bridges": [
          "wallet-governance"
        ]
      },
      {
        "id": "copper",
        "name": "Copper",
        "bridges": [
          "regulated-custody",
          "wallet-governance"
        ]
      },
      {
        "id": "fordefi",
        "name": "Fordefi",
        "bridges": [
          "wallet-governance"
        ]
      },
      {
        "id": "unchained",
        "name": "Unchained",
        "bridges": [
          "collaborative-custody",
          "succession-bridge"
        ]
      },
      {
        "id": "casa",
        "name": "Casa",
        "bridges": [
          "collaborative-custody",
          "succession-bridge"
        ]
      },
      {
        "id": "nunchuk",
        "name": "Nunchuk",
        "bridges": [
          "collaborative-custody"
        ]
      },
      {
        "id": "river",
        "name": "River",
        "bridges": [
          "access-execution",
          "reserve-evidence"
        ]
      },
      {
        "id": "kraken",
        "name": "Kraken",
        "bridges": [
          "access-execution",
          "reserve-evidence"
        ]
      },
      {
        "id": "chainalysis",
        "name": "Chainalysis",
        "bridges": [
          "attribution"
        ]
      },
      {
        "id": "trm-labs",
        "name": "TRM Labs",
        "bridges": [
          "attribution"
        ]
      },
      {
        "id": "elliptic",
        "name": "Elliptic",
        "bridges": [
          "attribution"
        ]
      }
    ],
    "sources": [
      {
        "id": "bip-322",
        "title": "BIP-322 Generic Signed Message Format",
        "url": "https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki",
        "archive_url": "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0322.mediawiki",
        "level": 5,
        "currency": "current",
        "checked_on": "2026-09-17"
      },
      {
        "id": "bitcoin-transactions",
        "title": "Bitcoin Developer Guide - Transactions",
        "url": "https://developer.bitcoin.org/devguide/transactions.html",
        "level": 5,
        "currency": "current",
        "checked_on": "2026-09-17"
      },
      {
        "id": "occ-safekeeping",
        "title": "Crypto-Asset Safekeeping by Banking Organizations",
        "url": "https://www.occ.gov/news-issuances/news-releases/2025/nr-ia-2025-68a.pdf",
        "level": 3,
        "currency": "current",
        "checked_on": "2026-09-17"
      },
      {
        "id": "icaew-audit",
        "title": "Considerations for Auditing Cryptocurrencies",
        "url": "https://www.icaew.com/technical/technology/blockchain-and-cryptoassets/blockchain-helpsheets/considerations-for-auditing-cryptocurrencies",
        "level": 4,
        "currency": "current",
        "checked_on": "2026-09-17"
      },
      {
        "id": "nydfs-custody-2025",
        "title": "Updated Guidance on Custodial Structures for Customer Protection in the Event of Insolvency",
        "url": "https://www.dfs.ny.gov/industry-guidance/industry-letters/il20250930-updated-guidance-custodial-structures",
        "level": 3,
        "currency": "current",
        "checked_on": "2026-09-17"
      },
      {
        "id": "occ-il-1184",
        "title": "Interpretive Letter 1184: Crypto-Asset Custody and Execution Services",
        "url": "https://www.occ.gov/topics/charters-and-licensing/interpretations-and-decisions/2025/int1184.pdf",
        "level": 3,
        "currency": "current",
        "checked_on": "2026-09-17"
      },
      {
        "id": "w3c-prov-o",
        "title": "PROV-O: The PROV Ontology",
        "url": "https://www.w3.org/TR/prov-o/",
        "level": 2,
        "currency": "current",
        "checked_on": "2026-09-17"
      },
      {
        "id": "w3c-vc-data-model",
        "title": "Verifiable Credentials Data Model v2.0",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "level": 2,
        "currency": "current",
        "checked_on": "2026-09-17"
      }
    ],
    "claims": [
      {
        "id": "signature-not-title",
        "text": "A valid signature does not by itself establish legal ownership or lawful authority.",
        "status": "corroborated",
        "treatments": [
          {
            "source_id": "bip-322",
            "treatment": "supports",
            "locator": "Abstract",
            "quote": "A standard for interoperable signed messages based on the Bitcoin Script format, either for proving availability of funds, or for committing to a message as the intended recipient of funds sent to the invoice address."
          },
          {
            "source_id": "icaew-audit",
            "treatment": "supports",
            "locator": "Ownership and Control",
            "quote": "Certain blockchain operations can also obviate the need for third-party intermediaries for the execution of transactions, limiting the information available to prove ownership."
          }
        ]
      },
      {
        "id": "custody-needs-law",
        "text": "Institutional crypto safekeeping remains subject to existing custody, fiduciary, information-security, and legal requirements.",
        "status": "supported",
        "treatments": [
          {
            "source_id": "nydfs-custody-2025",
            "treatment": "supports",
            "locator": "Industry Letter - September 30, 2025: Updated Guidance on Custodial Structures for Customer Protection in the Event of Insolvency",
            "quote": "New York’s virtual currency regulation, 23 NYCRR Part 200, requires BitLicensees to do the following, among other things: hold virtual currency in a manner that protects customer assets; maintain comprehensive books and records; properly disclose the material terms and conditions associated with their products and services, including custody services; and refrain from making any false, misleading, or deceptive representations or omissions in their marketing materials."
          }
        ]
      }
    ]
  },
  "rules": {
    "meta": {
      "version": "0.3.0",
      "semantics": "open-world forward chaining",
      "conflict_resolution": "higher priority first, then rule id",
      "fact_registry": "domain/facts.json"
    },
    "rules": [
      {
        "id": "R-CUSTODY-READY-001",
        "description": "Institutional custody evidence is bridge-ready only when identity, entitlement, control, and legal authority are all evidenced.",
        "priority": 100,
        "when": {
          "all": [
            {
              "fact": "customer_identity_evidenced",
              "equals": true
            },
            {
              "fact": "asset_scope_approved",
              "equals": true
            },
            {
              "fact": "exclusive_control_evidenced",
              "equals": true
            },
            {
              "fact": "legal_authority_evidenced",
              "equals": true
            }
          ]
        },
        "then": [
          {
            "fact": "custody_bridge_ready",
            "value": true
          }
        ],
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "id": "R-AUTHORITY-GAP-001",
        "description": "Cryptographic control without evidence of legal authority leaves a legal-authority gap.",
        "priority": 90,
        "when": {
          "all": [
            {
              "fact": "exclusive_control_evidenced",
              "equals": true
            },
            {
              "fact": "legal_authority_evidenced",
              "equals": false
            }
          ]
        },
        "then": [
          {
            "fact": "legal_authority_gap",
            "value": true
          }
        ],
        "source_ids": [
          "bip-322",
          "icaew-audit"
        ]
      },
      {
        "id": "R-RESERVES-INCOMPLETE-001",
        "description": "Asset evidence without liability evidence cannot establish reserve coverage or solvency.",
        "priority": 80,
        "when": {
          "all": [
            {
              "fact": "bitcoin_assets_evidenced",
              "equals": true
            },
            {
              "fact": "liabilities_evidenced",
              "equals": false
            }
          ]
        },
        "then": [
          {
            "fact": "reserve_assurance_complete",
            "value": false
          }
        ],
        "source_ids": [
          "icaew-audit"
        ]
      }
    ]
  },
  "assessment": {
    "id": "us-institutional-bitcoin-custody-readiness",
    "title": "US Institutional Bitcoin Custody Readiness Assessment",
    "version": "0.3.0",
    "checked_on": "2026-09-17",
    "scope": "Research pre-screen informed by US federal banking guidance and New York virtual-currency custody guidance. It is not a determination of compliance or legal advice.",
    "outcomes": [
      "ready_for_expert_review",
      "not_ready",
      "insufficient_information",
      "conflict"
    ],
    "requirements": [
      {
        "fact": "customer_identity_evidenced",
        "label": "Customer identity and due diligence",
        "evidence_expected": "Current KYC file, beneficial-owner record, risk rating, and approval record.",
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "fact": "legal_authority_evidenced",
        "label": "Legal authority and mandate",
        "evidence_expected": "Executed custody mandate plus current corporate, trust, estate, or court authority for the instructing persons.",
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "fact": "asset_scope_approved",
        "label": "Bitcoin asset and ledger risk assessment",
        "evidence_expected": "Approved Bitcoin-specific technical, operational, legal, compliance, and dependency assessment.",
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "fact": "exclusive_control_evidenced",
        "label": "Control against unilateral transfer by another party",
        "evidence_expected": "Documented key ceremony and control test showing no outside party has information sufficient to transfer unilaterally.",
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "fact": "customer_assets_segregated",
        "label": "Customer-asset segregation",
        "evidence_expected": "Wallet architecture and ledger records separating customer assets from custodian and affiliate assets.",
        "source_ids": [
          "nydfs-custody-2025"
        ]
      },
      {
        "fact": "books_reconcile_to_chain",
        "label": "Books, beneficial interests, and on-chain reconciliation",
        "evidence_expected": "Dated reconciliation tying on-chain balances to internal books and each customer's beneficial interest.",
        "source_ids": [
          "nydfs-custody-2025"
        ]
      },
      {
        "fact": "key_lifecycle_controls_documented",
        "label": "Key generation, storage, use, backup, and deletion controls",
        "evidence_expected": "Approved key-management standard, ceremony records, access matrix, backup inventory, and deletion procedure.",
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "fact": "recovery_and_compromise_plan_tested",
        "label": "Tested loss, compromise, and continuity plans",
        "evidence_expected": "Recent recovery exercise and incident test with results, exceptions, owners, and remediation dates.",
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "fact": "cybersecurity_controls_assessed",
        "label": "Cybersecurity control assessment",
        "evidence_expected": "Current security risk assessment covering custody systems, sensitive key material, access, monitoring, and incident response.",
        "source_ids": [
          "occ-safekeeping"
        ]
      },
      {
        "fact": "subcustodian_due_diligence_complete",
        "label": "Sub-custodian and third-party due diligence",
        "evidence_expected": "Selection diligence, control assessment, insolvency analysis, service agreement, monitoring, and material-event notification terms.",
        "applies_when": {
          "fact": "subcustodian_used",
          "equals": true
        },
        "source_ids": [
          "occ-safekeeping",
          "occ-il-1184"
        ]
      },
      {
        "fact": "customer_agreement_complete",
        "label": "Clear customer agreement, duties, and disclosures",
        "evidence_expected": "Executed agreement covering duties, instructions, storage model, fees, forks, disclosures, liability, and any sub-custody.",
        "source_ids": [
          "occ-safekeeping",
          "nydfs-custody-2025"
        ]
      },
      {
        "fact": "independent_assurance_current",
        "label": "Current independent assurance or audit coverage",
        "evidence_expected": "Current independent audit or assurance work covering key lifecycle, transfers, settlement, IT, and third parties where applicable.",
        "source_ids": [
          "occ-safekeeping"
        ]
      }
    ]
  },
  "evidence": {
    "meta": {
      "generated_on": "2026-09-17",
      "frozen": 6,
      "unavailable": 2
    },
    "snapshots": [
      {
        "source_id": "bip-322",
        "status": "frozen",
        "url": "https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki",
        "archive_url": "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0322.mediawiki",
        "final_url": "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0322.mediawiki",
        "retrieved_at": "2026-09-17T22:29:48+00:00",
        "sha256": "0eb91c5093ef81c462cadffdbe02d4d1638cb270d3ccb47301a6d82860aa0454",
        "bytes": 21361,
        "content_type": "text/plain; charset=utf-8",
        "path": "evidence/sources/bip-322/0eb91c5093ef81c462cadffdbe02d4d1638cb270d3ccb47301a6d82860aa0454.mediawiki",
        "text_path": "evidence/sources/bip-322/0eb91c5093ef81c462cadffdbe02d4d1638cb270d3ccb47301a6d82860aa0454.txt",
        "text_sha256": "0eb91c5093ef81c462cadffdbe02d4d1638cb270d3ccb47301a6d82860aa0454",
        "text_chars": 21361
      },
      {
        "source_id": "bitcoin-transactions",
        "status": "frozen",
        "url": "https://developer.bitcoin.org/devguide/transactions.html",
        "archive_url": "https://developer.bitcoin.org/devguide/transactions.html",
        "final_url": "https://developer.bitcoin.org/devguide/transactions.html",
        "retrieved_at": "2026-09-17T22:29:49+00:00",
        "sha256": "d1a0cafb54f513f74437bfe78e180136a6d2535ebd33312aecce39cc0fe46565",
        "bytes": 68805,
        "content_type": "text/html",
        "path": "evidence/sources/bitcoin-transactions/d1a0cafb54f513f74437bfe78e180136a6d2535ebd33312aecce39cc0fe46565.html",
        "text_path": "evidence/sources/bitcoin-transactions/d1a0cafb54f513f74437bfe78e180136a6d2535ebd33312aecce39cc0fe46565.txt",
        "text_sha256": "0a29e399de5b312e419c61365ce5685f51aed1130d7e6e8ec2a0b8b74ccafd03",
        "text_chars": 33255
      },
      {
        "source_id": "icaew-audit",
        "status": "frozen",
        "url": "https://www.icaew.com/technical/technology/blockchain-and-cryptoassets/blockchain-helpsheets/considerations-for-auditing-cryptocurrencies",
        "archive_url": "https://www.icaew.com/technical/technology/blockchain-and-cryptoassets/blockchain-helpsheets/considerations-for-auditing-cryptocurrencies",
        "final_url": "https://www.icaew.com/technical/technology/blockchain-and-cryptoassets/blockchain-helpsheets/considerations-for-auditing-cryptocurrencies",
        "retrieved_at": "2026-09-17T22:31:09+00:00",
        "sha256": "d372c0af5b76172f602a08279904aefd5c89167ef9088e9882019843cc0715a4",
        "bytes": 495112,
        "content_type": "text/html; charset=utf-8",
        "path": "evidence/sources/icaew-audit/d372c0af5b76172f602a08279904aefd5c89167ef9088e9882019843cc0715a4.html",
        "text_path": "evidence/sources/icaew-audit/d372c0af5b76172f602a08279904aefd5c89167ef9088e9882019843cc0715a4.txt",
        "text_sha256": "641ca4b8f899ffe493ce6874eeea165b6be9c86c4aee3fa38277c479a45daae6",
        "text_chars": 53581
      },
      {
        "source_id": "nydfs-custody-2025",
        "status": "frozen",
        "url": "https://www.dfs.ny.gov/industry-guidance/industry-letters/il20250930-updated-guidance-custodial-structures",
        "archive_url": "https://www.dfs.ny.gov/industry-guidance/industry-letters/il20250930-updated-guidance-custodial-structures",
        "final_url": "https://www.dfs.ny.gov/industry-guidance/industry-letters/il20250930-updated-guidance-custodial-structures",
        "retrieved_at": "2026-09-17T22:31:10+00:00",
        "sha256": "4086ebb8667840585779e0bcc53ac30871ecb7df39bfa78d96bd2ae1879898f4",
        "bytes": 45662,
        "content_type": "text/html; charset=utf-8",
        "path": "evidence/sources/nydfs-custody-2025/4086ebb8667840585779e0bcc53ac30871ecb7df39bfa78d96bd2ae1879898f4.html",
        "text_path": "evidence/sources/nydfs-custody-2025/4086ebb8667840585779e0bcc53ac30871ecb7df39bfa78d96bd2ae1879898f4.txt",
        "text_sha256": "00781b24d2cf1cb65771cecbf2d53123a10377f7f1cababe95befbf09f7004d0",
        "text_chars": 13706
      },
      {
        "source_id": "occ-il-1184",
        "status": "unavailable",
        "url": "https://www.occ.gov/topics/charters-and-licensing/interpretations-and-decisions/2025/int1184.pdf",
        "attempted_at": "2026-09-17T22:32:30+00:00",
        "error": "URLError: <urlopen error timed out>"
      },
      {
        "source_id": "occ-safekeeping",
        "status": "unavailable",
        "url": "https://www.occ.gov/news-issuances/news-releases/2025/nr-ia-2025-68a.pdf",
        "attempted_at": "2026-09-17T22:31:09+00:00",
        "error": "URLError: <urlopen error timed out>"
      },
      {
        "source_id": "w3c-prov-o",
        "status": "frozen",
        "url": "https://www.w3.org/TR/prov-o/",
        "archive_url": "https://www.w3.org/TR/prov-o/",
        "final_url": "https://www.w3.org/TR/prov-o/",
        "retrieved_at": "2026-09-17T22:32:30+00:00",
        "sha256": "6b96671ab84faf12ce3f041aca12c3f93a6df2ed242348810743179a68e69555",
        "bytes": 464179,
        "content_type": "text/html; charset=utf-8",
        "path": "evidence/sources/w3c-prov-o/6b96671ab84faf12ce3f041aca12c3f93a6df2ed242348810743179a68e69555.html",
        "text_path": "evidence/sources/w3c-prov-o/6b96671ab84faf12ce3f041aca12c3f93a6df2ed242348810743179a68e69555.txt",
        "text_sha256": "84b4a4e96d424924291d182ea8f6f6b693a3dae52d98a4702c5f135b116c79d0",
        "text_chars": 185642
      },
      {
        "source_id": "w3c-vc-data-model",
        "status": "frozen",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "archive_url": "https://www.w3.org/TR/vc-data-model/",
        "final_url": "https://www.w3.org/TR/vc-data-model/",
        "retrieved_at": "2026-09-17T22:32:30+00:00",
        "sha256": "a9196a3d0b6601356c4e127bad24f8c7f2c17f6ed22e41b35755a910104156f8",
        "bytes": 1023165,
        "content_type": "text/html; charset=utf-8",
        "path": "evidence/sources/w3c-vc-data-model/a9196a3d0b6601356c4e127bad24f8c7f2c17f6ed22e41b35755a910104156f8.html",
        "text_path": "evidence/sources/w3c-vc-data-model/a9196a3d0b6601356c4e127bad24f8c7f2c17f6ed22e41b35755a910104156f8.txt",
        "text_sha256": "01f291475fb90c115e1210b61bdd86532f09967165dd5b2de623513324188bf0",
        "text_chars": 361645
      }
    ]
  },
  "case_studies": [
    {
      "meta": {
        "id": "allianz-y3-bitcoin",
        "title": "Allianz Y3: pathway to Bitcoin exposure",
        "as_of": "2026-09-18",
        "jurisdiction": "Lithuania / European Union",
        "status": "research",
        "purpose": "Help a pension-fund participant understand what would have to change for Allianz Y3 to obtain lawful Bitcoin exposure or hold Bitcoin-related assets.",
        "not_advice": "Research and question-generation only; not legal, pension, tax or investment advice."
      },
      "transition": {
        "actor": "Allianz Y3 1996–2002 target-group pension fund",
        "manager": "Allianz Lietuva gyvybės draudimas UAB",
        "participant_role": "Beneficiary and unit holder; not portfolio manager or owner of a separately identified wallet balance",
        "from": "A lifecycle pension portfolio implemented primarily through regulated financial instruments and collective-investment vehicles",
        "to": "A portfolio with a defined, lawful and operationally controlled allocation to direct Bitcoin or a Bitcoin-linked financial instrument",
        "decision_question": "Can the manager lawfully and prudently add Bitcoin exposure, through which instrument and custody structure, under whose approval, and with what participant rights?"
      },
      "verified_facts": [
        {
          "id": "manager-controls-assets",
          "statement": "Allianz manages and disposes of fund assets on a trust basis; its investment group makes investment decisions.",
          "source_id": "allianz-y3-strategy",
          "locator": "Sections 1.3 and 2.4",
          "implication": "A participant cannot instruct Allianz to purchase Bitcoin solely for that participant's pension account."
        },
        {
          "id": "current-investment-perimeter",
          "statement": "The published strategy lists transferable securities, money-market instruments, deposits, venture-capital markets, limited derivatives, collective-investment units and cash as the investment perimeter.",
          "source_id": "allianz-y3-strategy",
          "locator": "Sections 3.1–3.7",
          "implication": "Direct Bitcoin is not expressly included in the published strategy; compatibility cannot be presumed."
        },
        {
          "id": "strategy-can-change",
          "statement": "The strategy may be reviewed when previously excluded asset classes emerge and are considered more suitable.",
          "source_id": "allianz-y3-strategy",
          "locator": "Section 5.3.2",
          "implication": "The published policy contains a governance path for considering a new asset class, but creates no duty to adopt it."
        },
        {
          "id": "participant-transfer-right",
          "statement": "A participant may transfer to another fund managed by the same or another pension company, subject to the governing rules.",
          "source_id": "lt-standard-rules-2026",
          "locator": "Sections 12.3–12.4 and 45–51",
          "implication": "The participant can choose among eligible pension funds, but the transfer does not place pension assets in a personal Bitcoin wallet."
        },
        {
          "id": "depositary-required",
          "statement": "Pension-fund assets must be held with a depositary; the 2025 report identifies AB SEB bankas as depositary.",
          "source_id": "lt-standard-rules-2026",
          "locator": "Section 35",
          "implication": "Any direct or indirect Bitcoin route must fit the pension depositary and asset-safekeeping framework."
        },
        {
          "id": "micar-is-not-investment-permission",
          "statement": "MiCAR regulates crypto-asset issuers and service providers and the Bank of Lithuania licenses and supervises covered providers.",
          "source_id": "lb-micar",
          "locator": "Markets in Crypto-Assets, framework and authorisation sections",
          "implication": "A licensed crypto service provider is relevant infrastructure, but MiCAR licensing alone does not prove that a pension fund may invest in Bitcoin."
        }
      ],
      "blockers": [
        {
          "id": "B1",
          "status": "established",
          "question": "Who has investment authority?",
          "finding": "The manager's investment group has authority; the participant does not direct individual holdings.",
          "unlock": "A manager-approved strategy and investment decision."
        },
        {
          "id": "B2",
          "status": "established",
          "question": "Does the current published strategy include direct Bitcoin?",
          "finding": "No express inclusion was found.",
          "unlock": "A documented legal interpretation that it is already eligible, or a formally approved strategy change."
        },
        {
          "id": "B3",
          "status": "unknown",
          "question": "May a Lithuanian second-pillar pension fund hold Bitcoin directly?",
          "finding": "Not established by the sources reviewed so far.",
          "unlock": "Current Lithuanian-law analysis and confirmation from the Bank of Lithuania or qualified Lithuanian pension counsel."
        },
        {
          "id": "B4",
          "status": "unknown",
          "question": "Could an eligible transferable security or collective-investment vehicle provide Bitcoin exposure?",
          "finding": "Potentially compatible in form, but eligibility, concentration, valuation, liquidity and look-through treatment are unverified.",
          "unlock": "Instrument-level legal, regulatory, accounting, risk and depositary review."
        },
        {
          "id": "B5",
          "status": "unknown",
          "question": "Can the depositary safeguard or oversee the proposed structure?",
          "finding": "No evidence reviewed establishes SEB's willingness or operational arrangement for this fund.",
          "unlock": "Depositary acceptance, control design, valuation process and reconciliation evidence."
        },
        {
          "id": "B6",
          "status": "unknown",
          "question": "Would the allocation satisfy participant-interest and lifecycle-risk duties?",
          "finding": "No allocation case, risk budget or fiduciary analysis has been established.",
          "unlock": "A documented investment thesis, sizing rule, liquidity/stress analysis, benchmark treatment and governance approval."
        }
      ],
      "pathways": [
        {
          "id": "P1",
          "name": "Manager adds direct Bitcoin",
          "state": "blocked",
          "on_chain": true,
          "requires": [
            "B1",
            "B2",
            "B3",
            "B5",
            "B6"
          ],
          "meaning": "The fund or its controlled custody chain owns Bitcoin represented by on-chain outputs.",
          "warning": "This is the strongest on-chain route and currently the least legally and operationally established."
        },
        {
          "id": "P2",
          "name": "Manager buys an eligible Bitcoin-linked fund or security",
          "state": "researchable",
          "on_chain": false,
          "requires": [
            "B1",
            "B2",
            "B4",
            "B5",
            "B6"
          ],
          "meaning": "The pension fund owns a conventional financial instrument whose value references Bitcoin; an upstream issuer or custodian may hold Bitcoin.",
          "warning": "This creates price exposure, not participant ownership or control of on-chain Bitcoin."
        },
        {
          "id": "P3",
          "name": "Participant transfers to another pension fund",
          "state": "legally_available_in_principle",
          "on_chain": false,
          "requires": [],
          "meaning": "The participant moves pension units to another eligible manager or fund if one offers a preferable lawful policy.",
          "warning": "No Lithuanian second-pillar fund with verified Bitcoin exposure has yet been identified in this case."
        },
        {
          "id": "P4",
          "name": "Participant obtains a legally permitted payout and buys Bitcoin personally",
          "state": "personal_eligibility_unknown",
          "on_chain": true,
          "requires": [],
          "meaning": "Only assets lawfully paid out cease to be governed as pension-fund assets and could then be used personally.",
          "warning": "Eligibility, amount, timing, deductions and tax consequences depend on current law and personal circumstances."
        }
      ],
      "participant_actions": [
        "Ask Allianz whether direct crypto-assets or Bitcoin-linked ETPs are legally eligible for Y3 and request the exact legal basis for the answer.",
        "Ask whether the investment group has evaluated Bitcoin as a new asset class under strategy section 5.3.2.",
        "Ask which depositary, valuation, liquidity, counterparty and custody requirements would apply to each route.",
        "Ask the Bank of Lithuania whether current second-pillar rules permit direct Bitcoin, a Bitcoin ETP, or a qualifying collective-investment vehicle.",
        "Compare all eligible Lithuanian pension funds for documented Bitcoin exposure; do not infer exposure from generic technology or fintech holdings.",
        "Obtain personal advice before any transfer, contribution suspension or withdrawal decision."
      ],
      "sources": [
        {
          "id": "allianz-y3-strategy",
          "title": "Allianz Y3 investment strategy, effective 1 January 2024",
          "url": "https://www.allianz.lt/content/dam/onemarketing/cee/avlt/dokumentai/pf/investavimo_strategijos/allianz-Y3-1996-2002-tikslines-grupes-pensiju-fondo-investavimo-strategija-20224-01-01.pdf",
          "issuer": "Allianz Lietuva gyvybės draudimas UAB",
          "checked_on": "2026-09-18"
        },
        {
          "id": "lt-standard-rules-2026",
          "title": "Standard target-group pension-fund rules, consolidated from 1 January 2026",
          "url": "https://www.allianz.lt/content/dam/onemarketing/cee/avlt/dokumentai/pf/standartines_taisykles/Standartines-pensiju-fondu-taisykles-nuo-2026-01-01.pdf",
          "issuer": "Bank of Lithuania",
          "checked_on": "2026-09-18"
        },
        {
          "id": "allianz-y3-2025-report",
          "title": "Allianz Y3 annual report 2025",
          "url": "https://www.allianz.lt/content/dam/onemarketing/cee/avlt/dokumentai/ataskaitos/pensiju_fondu_ataskaitos/2025/Allianz-Y3-1996-2002-pensiju-fondo-ataskaita-2025.pdf",
          "issuer": "Allianz Lietuva gyvybės draudimas UAB",
          "checked_on": "2026-09-18"
        },
        {
          "id": "lb-micar",
          "title": "Markets in Crypto-Assets",
          "url": "https://www.lb.lt/en/markets-in-crypto-assets",
          "issuer": "Bank of Lithuania",
          "checked_on": "2026-09-18"
        }
      ]
    }
  ]
};
