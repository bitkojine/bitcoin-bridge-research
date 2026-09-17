# Evidence and provenance model

The assessment no longer accepts a map of unchecked Boolean facts. It derives facts from reviewed evidence records.

Each record separates:

- the **assertion** being supported, including its subject and Boolean value;
- the **artifact** used as evidence;
- the **issuer** responsible for the artifact;
- the **provenance** of how and when the artifact was obtained;
- the **scope** in which the artifact is relevant and temporally valid; and
- the **review activity**, reviewer, method, date, and disposition.

This structure is informed by [W3C PROV-O](https://www.w3.org/TR/prov-o/), particularly its distinction among entities, activities, and agents, and by the [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/), particularly its treatment of issuer, subject, validity period, status, and evidence. It is not a claim of full conformance to either standard.

## Derivation policy

A fact enters an assessment only when:

1. the case and evidence record pass structural validation;
2. the review status is `accepted`;
3. the evidence covers the case jurisdiction or uses the wildcard `*`;
4. the evidence is valid at the assessment time; and
5. the assertion concerns the case subject.

Rejected, contested, expired, future, and out-of-jurisdiction records are excluded with reasons. Accepted records supporting opposite values for the same fact produce a conflict; the engine does not choose between them.

An `accepted` review is still an assertion by the named reviewer. The software does not authenticate the artifact, issuer, reviewer, hash, or review method. A recorded SHA-256 digest detects changes only if it was computed correctly from the intended artifact and independently trusted.

## Provenance correspondence

| Local concept | PROV-inspired role |
| --- | --- |
| Evidence artifact | Entity |
| Assertion derived from evidence | Entity derived from another entity |
| Issuer | Agent attributed responsibility for the artifact |
| Review | Activity using an artifact and generating an accepted, rejected, or contested assertion |
| Reviewer | Agent associated with the review activity |

The current JSON is intentionally application-specific. RDF, JSON-LD, digital signatures, verifiable credentials, and external identity resolution remain future work.
