review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <path> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MINOR | - | R2 |
| L2 | open | yes | overlap | MAJOR | - | R2, R1 |
| L3 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L2

#### L2.t2b-1 (F2)

- claim: Notes cite outside-repo default values and omit T1a and T1b slots named in the source, both unverifiable from repo evidence.
- anchor: "(as /etc/aidev02/aienv.d/defaults.sh does: T3Model01 gpt-6.1-terra, T2Model02 glm-5.3"

#### L2.t3-1 (F1)

- claim: The replacement list maps both T2 variables to T2Model02, contradicting the required T2Model01 test update and removing the executor match for the T2Model01 rung.
- anchor: "replace each underscore name with the exported name (T3Model01, T2Model02, T2Model02, T1Model01 and T1Model02)"
- anchor2: "change the assertion at line 597 to the new T2Model01 name"

## Other findings

- L1 (MINOR, open, single): Reference page links a probe file absent from this checkout, leaving a dead link the tests do not catch.
- L3 (MINOR, open, single): Allow-list wording could be read to allow-list the red hit, but the acceptance criterion forbids that outcome.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
