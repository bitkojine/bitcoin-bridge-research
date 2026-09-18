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
          "quote": "Bendrovė pensijų turtą valdo, naudoja ir juo disponuoja turto patikėjimo teisės pagrindais ... Investicinius sprendimus priima Bendrovės investicijų grupė.",
          "source_id": "allianz-y3-strategy",
          "locator": "Sections 1.3 and 2.4",
          "implication": "A participant cannot instruct Allianz to purchase Bitcoin solely for that participant's pension account."
        },
        {
          "id": "current-investment-perimeter",
          "statement": "The published strategy lists transferable securities, money-market instruments, deposits, venture-capital markets, limited derivatives, collective-investment units and cash as the investment perimeter.",
          "quote": "Pensijų fondo turtas gali būti investuojamas į ... perleidžiamuosius vertybinius popierius ... pinigų rinkos priemones ... indėlius ... kolektyvinio investavimo subjektų vienetus ar akcijas.",
          "source_id": "allianz-y3-strategy",
          "locator": "Sections 3.1–3.7",
          "implication": "Direct Bitcoin is not expressly included in the published strategy; compatibility cannot be presumed."
        },
        {
          "id": "strategy-can-change",
          "statement": "The strategy may be reviewed when previously excluded asset classes emerge and are considered more suitable.",
          "quote": "atsiranda naujos turto klasės, į kurias iki tol nebuvo investuojama, ir kurios laikomos labiau tinkamomis",
          "source_id": "allianz-y3-strategy",
          "locator": "Section 5.3.2",
          "implication": "The published policy contains a governance path for considering a new asset class, but creates no duty to adopt it."
        },
        {
          "id": "participant-transfer-right",
          "statement": "A participant may transfer to another fund managed by the same or another pension company, subject to the governing rules.",
          "quote": "Dalyvis turi teisę pereiti į kitą Bendrovės valdomą pensijų fondą arba į kitos pensijų kaupimo bendrovės valdomą pensijų fondą.",
          "source_id": "lt-standard-rules-2026",
          "locator": "Sections 12.3–12.4 and 45–51",
          "implication": "The participant can choose among eligible pension funds, but the transfer does not place pension assets in a personal Bitcoin wallet."
        },
        {
          "id": "depositary-required",
          "statement": "Pension-fund assets must be held with a depositary; the 2025 report identifies AB SEB bankas as depositary.",
          "quote": "Pensijų turtas turi būti saugomas depozitoriume.",
          "source_id": "lt-standard-rules-2026",
          "locator": "Section 35",
          "implication": "Any direct or indirect Bitcoin route must fit the pension depositary and asset-safekeeping framework."
        },
        {
          "id": "micar-is-not-investment-permission",
          "statement": "MiCAR regulates crypto-asset issuers and service providers and the Bank of Lithuania licenses and supervises covered providers.",
          "quote": "The Bank of Lithuania is responsible for licensing and supervising crypto-asset service providers under MiCAR.",
          "source_id": "lb-micar",
          "locator": "Markets in Crypto-Assets, framework and authorisation sections",
          "implication": "A licensed crypto service provider is relevant infrastructure, but MiCAR licensing alone does not prove that a pension fund may invest in Bitcoin."
        },
        {
          "id": "statutory-crypto-prohibition",
          "statement": "Current Lithuanian pension law prohibits pension assets from being invested in crypto-assets and in securities granting rights to crypto-assets.",
          "quote": "Pensijų turtas negali būti investuotas į ... kriptoturtą ir į suteikiančius į jį teises vertybinius popierius.",
          "source_id": "lt-pension-law-current",
          "locator": "Article 45(3), consolidated version effective 2 May 2026",
          "implication": "Neither a manager decision nor a strategy amendment can make direct Bitcoin or a crypto-right security eligible while this prohibition remains in force."
        },
        {
          "id": "transitional-exit-window",
          "statement": "A participant who joined by 31 December 2025 and has not signed a pension payout agreement may leave the second pillar from 1 January 2026 through 31 December 2027.",
          "quote": "visi pensijų kaupimo dalyviai, pradėję dalyvauti pensijų kaupime iki 2025 m. gruodžio 31 d., bet dar nepasirašę pensijų išmokos sutarties, turės galimybę pasitraukti",
          "source_id": "socmin-pension-system-2026",
          "locator": "Section 'Galimybė pasitraukti ... 2026–2027', paragraphs 1–3",
          "implication": "For an eligible participant, a lawful payout is a currently open bridge from the pension wrapper to personally controlled money; it is not a fund-level Bitcoin allocation."
        },
        {
          "id": "exit-payout-composition",
          "statement": "On transitional exit, the participant receives personally paid contributions and investment return; state and Sodra contributions are converted into additional Sodra pension accounting units.",
          "quote": "galės atsiimti savo lėšomis sumokėtas įmokas ir visą investicinį prieaugį; Už „Sodros“ ir (ar) valstybės biudžeto ... įmokas bus apskaičiuojami papildomi pensijų apskaitos vienetai",
          "source_id": "socmin-pension-system-2026",
          "locator": "Section 'Ką dalyvis atgaus', items 1–2",
          "implication": "The cash amount is not necessarily the portal's entire displayed balance and must be obtained from Allianz before comparing options."
        },
        {
          "id": "partial-withdrawal-right",
          "statement": "Once during participation, a participant may withdraw 25% of accumulated pension assets, capped by qualifying personal 3%-of-salary contributions; a 3% deduction applies before retirement age.",
          "quote": "atsiimti 25 proc. savo pensijų fonde sukaupto turto ... negalės būti didesnė nei bendra paties dalyvio įmokėta suma",
          "source_id": "lb-pension-reform-2026",
          "locator": "Section 3, paragraphs 476–482",
          "implication": "This is a narrower bridge to personal liquidity and has future annuity consequences; it is not equivalent to moving 25% of the total balance into Bitcoin."
        },
        {
          "id": "crypto-ban-was-deliberate",
          "statement": "The legislative materials describe the crypto prohibition as an express policy choice made while expanding pension funds' access to other alternative assets.",
          "quote": "įtvirtinti draudimą pensijų fondams investuoti į kriptoturtą ir į suteikiančius į jį teises vertybinius popierius",
          "source_id": "lt-pension-amendment-explanatory",
          "locator": "Proposed measures, item 4",
          "implication": "The prohibition is not an accidental omission from an otherwise closed list; the legislature considered and expressly excluded this asset category."
        },
        {
          "id": "current-y3-portfolio",
          "statement": "The latest public Y3 portfolio summary uses a 90% MSCI World / 10% short euro-government-bond benchmark and reports holdings through equity funds, index funds, cash and money-market instruments.",
          "quote": "2026 m. 90% MSCI World Index ... 10% Bloomberg Barclays Series-E Euro Govt 1-5 Yr Bond Index",
          "source_id": "allianz-y3-holdings-2025",
          "locator": "Benchmark structure and largest-investments tables, 31 December 2025",
          "implication": "The fund is currently implemented through conventional pooled instruments; no explicit Bitcoin allocation appears in the public summary. This does not prove zero incidental exposure inside underlying companies or funds."
        },
        {
          "id": "alternative-assets-have-limits-not-bans",
          "statement": "The same Lithuanian reform that prohibited crypto proposed controlled access to unlisted securities, real estate, infrastructure and wider derivative use, using exposure limits and risk controls rather than categorical bans.",
          "quote": "į nebiržinius vertybinius popierius – iki 20 procentų ... į nekilnojamąjį turtą ir infrastruktūrą ... iki 30 procentų ... bendra ... suma negali būti didesnė kaip 40 procentų",
          "source_id": "lt-pension-amendment-explanatory",
          "locator": "Proposed measures, items 1–5",
          "implication": "The legislature demonstrated that it knew how to regulate difficult assets proportionally, yet assigned crypto and crypto-right securities a zero limit."
        },
        {
          "id": "eu-prudent-person-portfolio-test",
          "statement": "The EU occupational-pension model applies a prudent-person test to the portfolio as a whole: long-term member interests, security, quality, liquidity, profitability and diversification.",
          "quote": "the assets shall be invested in such a manner as to ensure the security, quality, liquidity and profitability of the portfolio as a whole",
          "source_id": "eu-iorp-ii",
          "locator": "Article 19(1)(a), (c), (d) and (f)",
          "implication": "At EU occupational-pension level, prudence is principally a governed portfolio standard rather than an automatic zero allocation for every unconventional asset."
        },
        {
          "id": "eiopa-crypto-can-face-prudent-person-test",
          "statement": "EIOPA stated that an occupational pension fund investing in crypto-assets should explain how the investment complies with the prudent-person rule; it did not describe EU law as imposing an automatic crypto ban.",
          "quote": "IORPs investing in crypto-assets should explain ... how their decision to invest in crypto-assets complies with ... the Prudent Person Rule",
          "source_id": "eiopa-qa-2128",
          "locator": "Final answer to Q&A 2128",
          "implication": "A risk-governed crypto allocation is conceptually possible in the EU occupational-pension framework, although national law and the legal category of Lithuania's second pillar may impose stricter rules."
        },
        {
          "id": "ec-warns-asset-bans-can-harm-savers",
          "statement": "The European Commission has warned that national asset restrictions can prevent pension beneficiaries from accessing potentially higher returns or more diversified strategies.",
          "quote": "This may prevent members and beneficiaries from accessing potentially higher returns or more diversified investment strategies.",
          "source_id": "ec-supplementary-pensions-2025",
          "locator": "Prudent-person principle discussion, page 12",
          "implication": "Categorical prohibitions themselves require prudential justification; restriction is not automatically synonymous with member protection."
        },
        {
          "id": "official-crypto-risk-case",
          "statement": "The Bank of Lithuania identifies crypto price volatility, cybersecurity and key-loss risk, speculation, possible total loss and weaker MiCA protections than traditional investments.",
          "quote": "Didelis kainų svyravimas ... galimi kibernetiniai išpuoliai, piniginės praradimas ... galite prarasti visas investuotas lėšas",
          "source_id": "lb-crypto-risks",
          "locator": "Risk and retail-investor suitability sections",
          "implication": "There is a genuine prudential case for strict controls; the unresolved question is why those risks require zero exposure instead of sizing, custody and governance constraints."
        },
        {
          "id": "indirect-route-was-reported-open",
          "statement": "An OECD/IOPS survey published before the current Lithuanian amendment reported that Lithuania prohibited direct cryptocurrency investment but allowed crypto-related funds; the current statute is stricter because it also excludes securities granting rights to crypto-assets.",
          "quote": "In Hungary and Lithuania, while direct investment in cryptocurrencies is prohibited, investment in crypto asset-related funds is allowed.",
          "source_id": "oecd-iops-crypto-pensions-2025",
          "locator": "Section 4.2, Regulatory status, page 16",
          "implication": "The policy trajectory appears to have moved from blocking direct holdings to closing at least some wrapper-based exposure. The survey is historical and must not be used as a statement of current Lithuanian law."
        }
      ],
      "policy_inquiry": {
        "question": "Why is the permitted Bitcoin allocation exactly zero when illiquid, leveraged or difficult-to-value assets can be admitted under limits and controls?",
        "current_answer": "The asymmetry is established; a public, Bitcoin-specific proportionality analysis justifying a zero limit has not been found. Official risk concerns are real, but the reviewed legislative material states the ban without demonstrating why less restrictive controls would be inadequate.",
        "observations": [
          "Lithuania permits or expanded access to unlisted securities, real estate, infrastructure, derivatives and alternative-asset channels subject to exposure limits, valuation rules and governance controls.",
          "Crypto-assets and securities granting rights to them receive a categorical zero allocation rather than a concentration limit.",
          "The Bank of Lithuania's stated crypto risks are volatility, cyber and key-loss risk, speculation, total-loss risk and weaker investor protections; these support caution but do not by themselves prove that every non-zero institutional allocation is imprudent.",
          "EU occupational-pension doctrine uses a portfolio-level prudent-person test, and EIOPA has described crypto investment as something that must be justified under that test rather than universally prohibited.",
          "The European Commission has separately warned that categorical national asset restrictions can reduce diversification or expected returns.",
          "An OECD/IOPS survey described Lithuania's earlier position as allowing crypto-related funds despite banning direct cryptocurrency; the 2026 law's added ban on crypto-right securities evidences subsequent tightening.",
          "The older gold prohibition shows that Lithuania's rule historically excludes certain non-sovereign monetary or commodity assets; this pattern predates Bitcoin and is not proof of an anti-Bitcoin motive."
        ],
        "hypotheses": [
          {
            "id": "H1",
            "claim": "The zero limit is a proportionate retirement-saver protection measure.",
            "status": "plausible_but_not_demonstrated",
            "support": "Crypto has high volatility, operational/key risks, uneven market integrity and weaker investor compensation and reporting protections than conventional instruments.",
            "counterevidence": "The law manages other severe liquidity, valuation, leverage and concentration risks through limits and controls, and the public legislative material reviewed does not compare a ban with lower-allocation alternatives.",
            "would_change_assessment": "A published impact or risk analysis showing that capped exposure, regulated custody, valuation and governance controls fail to protect this pension population."
          },
          {
            "id": "H2",
            "claim": "The ban reflects administrative simplicity and supervisory capacity rather than a conclusion that every allocation is economically irrational.",
            "status": "credible_inference",
            "support": "A bright-line ban is easier for managers and depositaries to police than instrument classification, wallet controls, look-through analysis and continuous exposure measurement.",
            "counterevidence": "Lithuania simultaneously accepted supervisory complexity for private assets, real estate, infrastructure and derivatives and expanded the permitted depositary set.",
            "would_change_assessment": "Official records identifying supervisory capacity, implementation cost or depositary readiness as the reason for selecting a ban."
          },
          {
            "id": "H3",
            "claim": "The rule structurally favours issuer-based financial assets over bearer-like monetary assets such as gold and Bitcoin.",
            "status": "effect_established_motive_unproven",
            "support": "Gold, gold-right securities, crypto and crypto-right securities are excluded, while claims on governments, companies, funds, property and alternative structures remain investable within rules.",
            "counterevidence": "The same pattern can arise from custody, valuation and cash-flow concerns without any intention to protect fiat finance or suppress monetary alternatives.",
            "would_change_assessment": "Legislative correspondence, debate or impact analysis explicitly discussing monetary competition, capital-channel objectives or protection of incumbent intermediaries."
          },
          {
            "id": "H4",
            "claim": "The zero limit is inconsistent with a technology-neutral prudent-person framework.",
            "status": "strong_policy_critique_not_legal_conclusion",
            "support": "EU occupational-pension sources frame prudence around total-portfolio risk, diversification and governance; EIOPA contemplated crypto being assessed under that framework.",
            "counterevidence": "Lithuania's second pillar is a specific national, state-supported scheme and the cited IORP material is a comparator, not proof that Article 45(3) is unlawful or directly governed by IORP II.",
            "would_change_assessment": "A controlling EU or Lithuanian legal analysis establishing either that the schemes are comparable and the ban lacks prudential justification, or that their differences fully justify categorical treatment."
          }
        ],
        "limits": "No reviewed primary source proves an intention to stop citizens buying 'sound money.' No constitutional, EU-law or proportionality judgment on Article 45(3) has been identified. The inquiry establishes an unexplained policy asymmetry, not corruption, unlawful conduct or motive."
      },
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
          "status": "established",
          "question": "May a Lithuanian second-pillar pension fund hold Bitcoin directly?",
          "finding": "No under the current statute: Article 45(3) expressly prohibits investing pension assets in crypto-assets.",
          "unlock": "A legislative amendment or authoritative change in the governing law, followed by strategy, fiduciary, custody and depositary approval."
        },
        {
          "id": "B4",
          "status": "established",
          "question": "Could a security granting rights to Bitcoin bypass the direct-crypto prohibition?",
          "finding": "No under the statutory text: Article 45(3) separately prohibits securities granting rights to crypto-assets.",
          "unlock": "A legislative amendment or an authoritative ruling that a specifically analysed instrument is outside that category."
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
        },
        {
          "id": "B7",
          "status": "unknown",
          "question": "Is ordinary equity or a collective-investment unit with incidental Bitcoin exposure outside Article 45(3)?",
          "finding": "The reviewed public sources do not establish the boundary between a prohibited security granting rights to crypto and an otherwise eligible instrument whose issuer or portfolio happens to hold Bitcoin.",
          "unlock": "Instrument-specific classification, look-through analysis and written Lithuanian regulatory or qualified-counsel interpretation."
        }
      ],
      "pathways": [
        {
          "id": "P1",
          "name": "Manager adds direct Bitcoin",
          "state": "prohibited_under_current_law",
          "on_chain": true,
          "requires": [
            "B1",
            "B2",
            "B3",
            "B5",
            "B6"
          ],
          "meaning": "The fund or its controlled custody chain owns Bitcoin represented by on-chain outputs.",
          "warning": "A strategy vote, licensed custodian or technical control design cannot override the statutory prohibition.",
          "legal_basis": "Lithuanian Law on Pension Accumulation, Article 45(3)."
        },
        {
          "id": "P2",
          "name": "Manager buys a security granting rights to Bitcoin",
          "state": "prohibited_under_current_law",
          "on_chain": false,
          "requires": [
            "B1",
            "B2",
            "B4",
            "B5",
            "B6"
          ],
          "meaning": "The pension fund owns a conventional security that grants a claim or right tied to crypto-assets; an upstream issuer or custodian may hold Bitcoin.",
          "warning": "Using a conventional wrapper does not evade the express statutory category, and it would create exposure rather than participant control of Bitcoin.",
          "legal_basis": "Lithuanian Law on Pension Accumulation, Article 45(3)."
        },
        {
          "id": "P3",
          "name": "Participant transfers to another pension fund",
          "state": "legally_available_in_principle",
          "on_chain": false,
          "requires": [],
          "meaning": "The participant moves pension units to another eligible manager or fund if one offers a preferable lawful policy.",
          "warning": "Every Lithuanian second-pillar fund is subject to the same statutory prohibition, so changing manager does not remove it."
        },
        {
          "id": "P4",
          "name": "Eligible participant exits during the 2026–2027 window",
          "state": "potentially_available_subject_to_conditions",
          "on_chain": true,
          "requires": [],
          "meaning": "Personally paid contributions plus investment return are paid to the participant; after payment, those funds are outside the pension fund and may be used personally.",
          "warning": "This exits the pension system rather than changing it. The cash payout is not the whole displayed balance; state and Sodra contributions become pension accounting units. Personal eligibility and consequences must be confirmed."
        },
        {
          "id": "P5",
          "name": "Participant uses the one-time partial-withdrawal right",
          "state": "available_subject_to_personal_limits",
          "on_chain": true,
          "requires": [],
          "meaning": "A qualifying participant receives up to 25% of accumulated assets, limited by qualifying personal contributions, after applicable deductions; only the paid cash could then be used personally.",
          "warning": "This reduces retirement assets, can affect the later annuity calculation and is not evidence that buying Bitcoin is suitable."
        },
        {
          "id": "P6",
          "name": "Manager considers ordinary securities with incidental Bitcoin exposure",
          "state": "researchable",
          "on_chain": false,
          "requires": [
            "B1",
            "B2",
            "B5",
            "B6",
            "B7"
          ],
          "meaning": "The fund buys an otherwise eligible company share or collective-investment unit whose issuer or portfolio has Bitcoin exposure but which may not itself grant rights to crypto-assets.",
          "warning": "This boundary is unresolved in the reviewed public record, may be caught by regulatory interpretation or look-through rules, and does not move participant money on-chain."
        }
      ],
      "participant_actions": [
        "Ask Allianz for an itemised estimate of the cash payable under the 2026–2027 exit route: personal contributions, investment result, state/Sodra component converted to accounting units, timing and any deductions.",
        "Confirm whether participation began by 31 December 2025 and whether any pension payout agreement has been signed.",
        "Ask Allianz for the maximum one-time partial withdrawal, the 3% deduction if applicable and the effect on later annuity calculations.",
        "Ask the Bank of Lithuania for a written interpretation of Article 45(3) for a named instrument before treating any ETP, fund or company share as eligible.",
        "Treat a strategy amendment as downstream of law reform, not as a substitute for it.",
        "Obtain personal pension, tax and investment advice before exit, withdrawal or Bitcoin purchase; this case maps options and does not recommend one."
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
        },
        {
          "id": "lt-pension-law-current",
          "title": "Law on Pension Accumulation, consolidated version effective 2 May 2026",
          "url": "https://www.e-tar.lt/rs/actualedition/TAR.DDA1BD559D9B/yQdnAHlyLa/format/ISO_PDF/",
          "issuer": "Register of Legal Acts of Lithuania",
          "checked_on": "2026-09-18"
        },
        {
          "id": "lb-pension-reform-2026",
          "title": "Current information on pension-system reform from 2026",
          "url": "https://www.lb.lt/aktuali-informacija-apie-pensiju-sistemos-pertvarka-nuo-2026-m",
          "issuer": "Bank of Lithuania",
          "checked_on": "2026-09-18"
        },
        {
          "id": "socmin-pension-system-2026",
          "title": "Pension accumulation system from 1 January 2026",
          "url": "https://socmin.lrv.lt/lt/veiklos-sritys/socialinis-draudimas/pensiju-kaupimo-sistema-nuo-2026-01-01/",
          "issuer": "Lithuanian Ministry of Social Security and Labour",
          "checked_on": "2026-09-18"
        },
        {
          "id": "lt-pension-amendment-explanatory",
          "title": "Explanatory material for pension-accumulation investment amendments",
          "url": "https://e-seimas.lrs.lt/rs/legalact/TAK/1ab9e8313a1911f0a19dcea0bcc863ad/",
          "issuer": "Seimas of the Republic of Lithuania",
          "checked_on": "2026-09-18"
        },
        {
          "id": "allianz-y3-holdings-2025",
          "title": "Allianz Y3 investment-direction summary at 31 December 2025",
          "url": "https://www.allianz.lt/content/dam/onemarketing/cee/avlt/dokumentai/pf/investavimo-krypciu-aprasymai/2025-12-31/Y3-pensiju-fondas.pdf",
          "issuer": "Allianz Lietuva gyvybės draudimas UAB",
          "checked_on": "2026-09-18"
        },
        {
          "id": "eu-iorp-ii",
          "title": "Directive (EU) 2016/2341 on occupational retirement provision",
          "url": "https://eur-lex.europa.eu/eli/dir/2016/2341/2024-01-09/eng",
          "issuer": "European Parliament and Council",
          "checked_on": "2026-09-18"
        },
        {
          "id": "eiopa-qa-2128",
          "title": "EIOPA Q&A 2128: occupational pension investment in crypto-assets",
          "url": "https://www.eiopa.europa.eu/qa-regulation/questions-and-answers-database/2128_en",
          "issuer": "European Insurance and Occupational Pensions Authority",
          "checked_on": "2026-09-18"
        },
        {
          "id": "ec-supplementary-pensions-2025",
          "title": "European Commission communication on supplementary pensions",
          "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52025DC0839",
          "issuer": "European Commission",
          "checked_on": "2026-09-18"
        },
        {
          "id": "lb-crypto-risks",
          "title": "Crypto-assets: uses, regulation and risks",
          "url": "https://www.lb.lt/lt/kriptoturtas",
          "issuer": "Bank of Lithuania",
          "checked_on": "2026-09-18"
        },
        {
          "id": "oecd-iops-crypto-pensions-2025",
          "title": "Supervision of pension investments: crypto-assets and other complex instruments",
          "url": "https://www.oecd.org/content/dam/iops/en/working-papers/WP-43-Supervision-of-pension-investments-overseas-OTC-derivatives-structured-crypto.pdf",
          "issuer": "OECD / International Organisation of Pension Supervisors",
          "checked_on": "2026-09-18"
        }
      ]
    }
  ]
};
