review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | single | MAJOR | - | R3 |

## Blocking findings

### L3

#### L3.R3 (F1)

- claim: A resumed held guard with mode off can be reported as off, concealing the held state and its required clear-command outcome.
- anchor: "guard_status(guard, mode, ordinal) implementing the first-match mapping of section 4.1 (`off`, `released`, `held`, `user_override`, `unavailable`)."
- anchor2: "Resume and Exit report"

## Other findings

- L1 (MAJOR, open, single): Script exit code for not_open and verify_failed JSON errors is never stated, so an implementer must guess the grouping.
- L2 (MAJOR, open, single): Crash tests require real branches but never state the remote_reachable value that produces each branch, so an implementer must read recovery.py to infer it.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
