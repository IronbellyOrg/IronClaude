review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L6

#### L6.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows `bash -c "python3 x.py"` to run bare Python, and that is wrong because the goal says the hook refuses commands that run bare Python.
- anchor: "bash -c \"python3 x.py\""
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L6.t4-1 (F2)

- claim: The source directs the implementer to read the issue in full first; the plan cites the issue but does not carry that instruction.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."
- anchor2: "Read the issue in full first"

#### L6.t4-1 (F3)

- claim: This points to Task 6, which is the changelog task; the live fresh-session check is specified in Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"

## Other findings

- L1 (MAJOR, open, single): Task 4 acceptance runs test_cli_install.py but no task updates its pinned shipped-file lists at lines 138-145 and 415-419, which adding the script breaks.
- L2 (MAJOR, open, single): Existing exact command-list asserts in test_install_hooks.py:276,299,342-345 change when the Bash PreToolUse entry is added, and Task 4 only adds new tests without updating them.
- L3 (MAJOR, open, single): The grep pattern requires a space or end of line after the name, so it misses python3 before ; ) " or at end of a line segment, and the no-bare-call check can pass while a bare call remains.
- L4 (MINOR, open, single): Wrapper handling covers no argument-consuming options for sudo/time/nice/timeout, so forms like sudo -u root python3, time -p python3, nice -n 10 python3 would be missed; document never states these must block.
- L5 (MINOR, open, single): Double-quoted command substitution $(python3 ...) and $(...) inside double quotes executes in bash but is stated as never a command word; document never states this case must block.

## Reviser brief

Blocking finding ids: L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
