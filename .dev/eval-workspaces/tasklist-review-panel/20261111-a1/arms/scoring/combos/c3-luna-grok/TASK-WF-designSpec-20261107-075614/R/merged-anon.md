review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R2 |
| L2 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Resume must release a confirmed fixing push and must hold unless the live head equals target_sha, but it is not given target_sha or this cycle's edit count, so the crash tests cannot pass unless the PR is marked ready without that proof.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger"

## Other findings

- L2 (MINOR, open, single): The protocol and the user guide are told to print different spellings of the same clear command.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
