review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R2, R3, R1 |
| L2 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Tree has 8 bare python3 -c hits in installed skills; plan replaces only read-parse.md, so 'one' overstates completeness.
- anchor: "and the one bare `python3 -c` in the installed skills is replaced."

#### L1.t2b-1 (F2)

- claim: Constraint cites Task 6 for fresh-session proof but Task 6 is changelog; fresh-session proof is Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"
- anchor2: "## Task 6: Add the changelog entry"

#### L1.t3-1 (F1)

- claim: The allowed case runs bare python3 inside a child shell, so the hook permits a command the goal requires it to block.
- anchor: "`bash -c \"python3 x.py\"` (quoted text)"

#### L1.t3-1 (F2)

- claim: The candidate does not carry the source instruction to read the entire issue before implementation.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."
- anchor2: "Read the issue in full first"

#### L1.t3-1 (F3)

- claim: The safety constraint names Task 6 for the fresh-session check, but that check is Task 7; the task itself repeats the safety instruction correctly.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"
- anchor2: "## Task 7: Prove the hook blocks the issue's command in a fresh session and in a subagent"

#### L1.t4-1 (F1)

- claim: The allowed-case list permits a child shell to execute bare python, contradicting the goal of blocking commands that run bare python.
- anchor: "bash -c \"python3 x.py\""
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L1.t4-1 (F2)

- claim: The source requires reading the issue in full first, but the plan does not direct the implementer to do so before starting.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

## Other findings

- L2 (MAJOR, open, single): Task 1 requires naming the offending word, but Task 2 tests only assert stderr names uv run python and jq.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
