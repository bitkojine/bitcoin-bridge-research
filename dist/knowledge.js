window.KNOWLEDGE = {
  "model": {
    "meta": {
      "title": "Bitcoin Bridge Market Map",
      "version": "0.2.0",
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
        "level": 5,
        "checked_on": "2026-09-17"
      },
      {
        "id": "bitcoin-transactions",
        "title": "Bitcoin Developer Guide - Transactions",
        "url": "https://developer.bitcoin.org/devguide/transactions.html",
        "level": 5,
        "checked_on": "2026-09-17"
      },
      {
        "id": "occ-safekeeping",
        "title": "Crypto-Asset Safekeeping by Banking Organizations",
        "url": "https://www.occ.gov/news-issuances/news-releases/2025/nr-ia-2025-68a.pdf",
        "level": 3,
        "checked_on": "2026-09-17"
      },
      {
        "id": "icaew-audit",
        "title": "Considerations for Auditing Cryptocurrencies",
        "url": "https://www.icaew.com/technical/technology/blockchain-and-cryptoassets/blockchain-helpsheets/considerations-for-auditing-cryptocurrencies",
        "level": 4,
        "checked_on": "2026-09-17"
      },
      {
        "id": "nydfs-custody-2025",
        "title": "Updated Guidance on Custodial Structures for Customer Protection in the Event of Insolvency",
        "url": "https://www.dfs.ny.gov/industry-guidance/industry-letters/il20250930-updated-guidance-custodial-structures",
        "level": 3,
        "checked_on": "2026-09-17"
      },
      {
        "id": "occ-il-1184",
        "title": "Interpretive Letter 1184: Crypto-Asset Custody and Execution Services",
        "url": "https://www.occ.gov/topics/charters-and-licensing/interpretations-and-decisions/2025/int1184.pdf",
        "level": 3,
        "checked_on": "2026-09-17"
      },
      {
        "id": "w3c-prov-o",
        "title": "PROV-O: The PROV Ontology",
        "url": "https://www.w3.org/TR/prov-o/",
        "level": 2,
        "checked_on": "2026-09-17"
      },
      {
        "id": "w3c-vc-data-model",
        "title": "Verifiable Credentials Data Model v2.0",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "level": 2,
        "checked_on": "2026-09-17"
      }
    ],
    "claims": [
      {
        "id": "signature-not-title",
        "text": "A valid signature does not by itself establish legal ownership or lawful authority.",
        "status": "corroborated",
        "source_ids": [
          "bip-322",
          "icaew-audit"
        ]
      },
      {
        "id": "custody-needs-law",
        "text": "Institutional crypto safekeeping remains subject to existing custody, fiduciary, information-security, and legal requirements.",
        "status": "supported",
        "source_ids": [
          "occ-safekeeping"
        ]
      }
    ]
  },
  "rules": {
    "meta": {
      "version": "0.2.0",
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
    "version": "0.2.0",
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
  }
};
