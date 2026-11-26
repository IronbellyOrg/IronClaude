review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R3, R2 |
| L2 | open | no | overlap | MINOR | - | R3, R1, R2 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | yes | single | MAJOR | - | R1 |
| L5 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L4

#### L4.t3-1 (F1)

- claim: The stated quote rule and allowed `bash -c "python3 x.py"` case let nested shell execution run bare Python without being blocked.
- anchor: "Text inside single quotes, and text inside double quotes, is never a command word"

#### L4.t3-1 (F2)

- claim: The plan does not say how to skip sudo options or test `sudo -u nobody python3 x.py`, leaving a plausible wrapper form unblocked.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env`"

### L5

#### L5.t4-1 (F1)

- claim: The allowed `bash -c` case executes bare Python and bypasses the hook's required block.
- anchor: "bash -c \"python3 x.py\" (quoted text)"

## Other findings

- L1 (MAJOR, open, overlap): The listed allowed cases have no semicolon form, so the chained-forms criterion fails unless an unlisted case is added.
- L2 (MINOR, open, overlap): The fresh-session check is Task 7; Task 6 is the changelog, so the Constraints task number is stale.
- L3 (MAJOR, open, single): ccsession-tag README has a bare nohup python3 line the new hook will block; source scopes the fix to read-parse.md only.

## Reviser brief

Blocking finding ids: L4, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
