review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R3 |
| L4 | open | yes | overlap | CRITICAL | - | R1, R3 |
| L5 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Fixture lacks the new script so existing installer tests fail after the list addition.
- anchor: "add `\"block-bare-python.sh\"` to `_FRESHNESS_SCRIPTS`"
- anchor2: "`uv run pytest tests/cli/test_install_hooks.py tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -v` passes"

### L3

#### L3.t2b-1 (F3)

- claim: Constraint names Task 6 for work that is in Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"
- anchor2: "## Task 7: Prove the hook blocks the issue's command in a fresh session and in a subagent"

#### L3.t2b-1 (F4)

- claim: Settings path is given as relative ./artifacts file while run cwd is scratch.
- anchor: "From a scratch directory under `/tmp`, run two fresh non-interactive sessions with `claude -p --settings <that file>"

#### L3.t4-1 (B2)

- claim: The constraints assign the fresh-session check to Task 6, but Task 6 is the changelog and Task 7 is the fresh-session proof.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"
- anchor2: "## Task 6: Add the changelog entry"

#### L3.t4-1 (M1)

- claim: The source requires reading the full issue first, but the candidate does not make that a task or execution instruction.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

### L4

#### L4.t2b-1 (F5)

- claim: time, nice and command-without-flag have no test case.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env`"

#### L4.t4-1 (B1)

- claim: The allowed quoted `bash -c` form runs bare python3, so the hook does not block every command that runs a bare Python command.
- anchor: "Text inside single quotes, and text inside double quotes, is never a command word"
- anchor2: "bash -c \"python3 x.py\" (quoted text)"

## Other findings

- L2 (MAJOR, open, single): Allowed list has && and | chaining but no unquoted ; allowed case.
- L5 (MINOR, open, single): Grep check only passes if banned words appear quoted in code.

## Reviser brief

Blocking finding ids: L1, L3, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
