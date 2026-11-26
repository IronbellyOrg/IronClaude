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
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Fixture builds scripts dir without block-bare-python.sh, so install_hooks fails and Task 4 pytest acceptance cannot pass without an unstated fixture update.
- anchor: "the name is in `install_hooks._FRESHNESS_SCRIPTS`"

#### L1.t2b-1 (F4)

- claim: Plan runs test_cli_install.py but never updates its _PACKAGE_RESOURCES and _PLUGIN_RESOURCES hooks baselines, leaving the new script outside the installed-package baseline.
- anchor: "uv run pytest tests/cli/test_install_hooks.py tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -v"

### L2

#### L2.t2b-1 (F2)

- claim: Hook allows bash -c 'python3 x.py', which runs bare python3 instead of only mentioning it, contradicting the Goal and Done-when.
- anchor: "bash -c \"python3 ...\"` are not blocked"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t2b-1 (F3)

- claim: Wrapper option handling is specified only for env and timeout, leaving sudo -u, exec -a, time -p and leading redirections unspecified and untested.
- anchor: "`sudo`, `exec`, `nohup`, `time`, `nice`, `env` (plus its following options and `NAME=value` words), `timeout`"

#### L2.t3-1 (F1)

- claim: A text-only heredoc mentioning python3 can be blocked although the goal promises text-only mentions pass.
- anchor: "Lines of a heredoc body are scanned like ordinary lines"

#### L2.t3-1 (F2)

- claim: The plan does not direct the implementer to read issue #357 in full before implementation, as the driving document requires.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows `bash -c "python3 x.py"` to run Python, and that is wrong because it contradicts the requirement to refuse commands that run bare Python.
- anchor: "bash -c \"python3 x.py\" (quoted text)"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t4-1 (F2)

- claim: An implementer who follows the stated text as written builds a hook that blocks a heredoc which only writes text, and that is wrong because the goal says text-only mentions of Python pass.
- anchor: "a heredoc that only writes text whose line starts with `python3` is blocked too."
- anchor2: "lets `uv run python`, `uv pip`, `uvx` and text-only mentions of python through"

#### L2.t4-1 (F3)

- claim: The source requires reading issue #357 in full first, but the plan only references the issue and does not direct the implementer to read it in full.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L2.t4-1 (F4)

- claim: This cross-reference points to Task 6, which is the changelog task; the fresh-session check is Task 7.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"

## Other findings

none.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
