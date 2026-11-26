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
| L1 | open | yes | single | CRITICAL | - | R3 |
| L2 | open | yes | overlap | CRITICAL | - | R3, R1, R2 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | overlap | MAJOR | - | R3, R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The fake source fixture lists no block script, so install_hooks reports failure and every existing fake source test fails while the required test run must pass.
- anchor: "In `src/superclaude/cli/install_hooks.py`, add `\"block-bare-python.sh\"` to `_FRESHNESS_SCRIPTS`"
- anchor2: "`uv run pytest tests/cli/test_install_hooks.py tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -v` passes"

### L2

#### L2.t2b-1 (F2)

- claim: The plan allows a quoted nested command string to run bare python3, contradicting the goal and giving agents a one word way around the gate.
- anchor: "and `bash -c \"python3 ...\"` are not blocked)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t2b-1 (F4)

- claim: The wrapper rule states no option rule for sudo, so a literal skip then next word rule lets a form like sudo with an option flag reach bare python3 undetected.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env` (plus its following options and `NAME=value` words)"

#### L2.t2b-1 (F5)

- claim: The heredoc rule blocks text only heredoc content, which is disclosed as a ceiling but narrows the allowed text only scope.
- anchor: "a heredoc that only writes text whose line starts with `python3` is blocked too"

#### L2.t3-1 (F1)

- claim: The allowed bash -c test executes bare python3, contradicting the goal of blocking commands that run bare Python command words.
- anchor: "bash -c \"python3 x.py\" (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t3-1 (F2)

- claim: Constraint 20 points the fresh-session check to Task 6, but Task 6 is the changelog and the fresh-session check is Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"

#### L2.t3-1 (F3)

- claim: The candidate does not preserve the driving document's explicit requirement to read the issue in full before starting.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F1)

- claim: The allowed-case requirement lets a child shell execute bare python3, contradicting the goal of blocking commands that run it.
- anchor: "`bash -c \"python3 x.py\"` (quoted text)"
- anchor2: "A shipped PreToolUse hook on the `Bash` tool refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t4-1 (F2)

- claim: The wrapper rule does not explain how to skip sudo options, so `sudo -u user python script.py` can pass without detecting the bare Python command.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env`"

#### L2.t4-1 (F4)

- claim: The plan cites the issue but does not carry forward the driving document's instruction to read it in full first.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

## Other findings

- L3 (MAJOR, open, single): The allowed table has no semicolon chained case, so the stated both sides rule is not met without guessing that a quoted semicolon counts.
- L4 (MAJOR, open, overlap): The grep check passes or fails by whether the detection literals are quoted, so it does not prove the script contains no call to python or pip.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
