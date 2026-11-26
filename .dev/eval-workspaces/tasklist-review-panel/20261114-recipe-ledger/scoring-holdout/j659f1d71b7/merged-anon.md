review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L3 | open | yes | single | CRITICAL | - | R3 |

## Blocking findings

### L2

#### L2.t2b-1 (F2)

- claim: ccsession-tag skill scripts contain other bare python3 -c calls, so the uniqueness claim in the Goal is false on the current tree.
- anchor: "the one bare `python3 -c` in the installed skills is replaced."

#### L2.t2b-1 (F3)

- claim: The constraint cites Task 6 for the fresh-session check, but that check is Task 7; Task 6 is the changelog entry.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"

#### L2.t2b-1 (F4)

- claim: Allowing quoted bash -c execution contradicts the Goal's 'refuses any command that runs bare python3', since that form actually runs it.
- anchor: "`bash -c \"python3 x.py\"` (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t3-1 (F1)

- claim: An implementer following the allowed case builds a hook that lets `bash -c "python3 x.py"` run bare Python, bypassing the stated Bash-tool block.
- anchor: "`bash -c \"python3 x.py\" (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t3-1 (F2)

- claim: The plan assigns the fresh-session check to Task 6, but Task 6 is the changelog task and Task 7 specifies the check, so its task assignment contradicts itself.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"
- anchor2: "## Task 6: Add the changelog entry"

#### L2.t3-1 (F3)

- claim: The listed tests do not cover the stated requirement to fail open when jq is missing.
- anchor: "Fail-open cases (exit 0): non-JSON stdin; empty stdin;"

#### L2.t3-1 (F4)

- claim: The source requires reading the issue in full first; the plan identifies the issue and sections but does not carry that instruction explicitly.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F2)

- claim: The plan does not carry forward the source instruction to read the full issue before proceeding.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

### L3

#### L3.t4-1 (F1)

- claim: The hook can allow a quoted executable such as "python3" -c 1 even though Bash runs it as the bare python3 command.
- anchor: "Text inside single quotes, and text inside double quotes, is never a command word"

## Other findings

- L1 (MAJOR, open, single): A natural banned-list string in detection code matches the grep outside comments/message, so the AC can fail a correct script.

## Reviser brief

Blocking finding ids: L2, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
