review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R3 |
| L2 | open | yes | single | CRITICAL | - | R3 |
| L3 | open | no | overlap | MAJOR | - | R3, R1 |
| L4 | open | no | single | MINOR | - | R3 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | yes | overlap | MAJOR | - | R3, R2, R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: No allowed case contains ';' (count 0), so the Task 2 both-chained-forms criterion cannot pass as ordered.
- anchor: "Chained forms `&&`, `;` and `|` each appear in both a blocked and an allowed case."

### L2

#### L2.t2b-1 (F2)

- claim: New Bash PreToolUse matcher breaks tests/hooks/test_freshness_subagent_start_policy.py (no-Bash-matcher assertion) and no task updates or runs it.
- anchor: "`{\"matcher\": \"Bash\", \"hooks\": [{\"type\": \"command\", \"command\": \"~/.claude/hooks/block-bare-python.sh\", \"timeout\": 3}]}`"

### L6

#### L6.t2b-1 (F7)

- claim: The constraint points the live fresh-session check at Task 6, but that procedure is Task 7; the pointer names the wrong task.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"

#### L6.t3-1 (F1)

- claim: An implementer following this allowance builds a hook that permits `bash -c "python3 x.py"`, which runs bare python3 and contradicts the goal of refusing commands that run it.
- anchor: "`bash -c \"python3 x.py\"` (quoted text);"

#### L6.t3-1 (F2)

- claim: The candidate does not explicitly instruct the implementer to read issue #357 in full before implementation, as the driving document requires.
- anchor: "- Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L6.t4-1 (F1)

- claim: An implementer who follows the allowed-case instruction permits Bash to execute bare python3 through bash -c, contrary to the stated blocking goal.
- anchor: "`bash -c \"python3 x.py\"` (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L6.t4-1 (F3)

- claim: The constraint points to Task 6, which is the changelog task; the fresh-session check is Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook"

## Other findings

- L3 (MAJOR, open, overlap): Options that take a separate argument (sudo -u bob, env -u FOO, nice -n, timeout --signal KILL) make the wrapper word or option the command word, so bare python3 after them is allowed.
- L4 (MINOR, open, single): A spaced bash case (python | python3 | pip | pip3) matches that grep in code, so the check is formatting-sensitive, not robust.
- L5 (MINOR, open, single): tests/unit/test_cli_install.py baseline _PACKAGE_RESOURCES hooks lists omit both new scripts, leaving that inventory stale (subset assertions still pass).

## Reviser brief

Blocking finding ids: L1, L2, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
