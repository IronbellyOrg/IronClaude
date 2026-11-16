review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 e54e890380e234377e77d17b785d8ad7940fdadc69528f488b0c06b0ff5964f4
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | yes | single | MAJOR | - | R1 |

## Blocking findings

### L3

#### L3.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a master-comparison step that runs `orca worktree create` without `--agent`, and that is wrong because the project instructions say a hook blocks that command without `--agent`.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

## Other findings

- L1 (MAJOR, open, single): Source retry-once rule for empty worker output has no explicit task; skill may stop without retrying.
- L2 (MAJOR, open, single): Closed-task exclusion (API default) from source section 12 is dropped from the script spec.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
