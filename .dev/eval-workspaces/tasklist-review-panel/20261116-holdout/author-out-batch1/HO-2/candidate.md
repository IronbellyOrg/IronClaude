---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementIronbel-20261104-130647
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Block bare python, python3, pip and pip3 in Bash with a PreToolUse hook (issue #357)

Source: ./source.md
Goal: A shipped PreToolUse hook on the `Bash` tool refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word, tells the agent to use `uv run python` (or `uv pip`, `uvx`) or `jq` for JSON, lets `uv run python`, `uv pip`, `uvx` and text-only mentions of python through, is installed and registered by `superclaude install`, fires for subagent Bash calls, and the one bare `python3 -c` in the installed skills is replaced.

## Constraints

- Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), "Proposed fix" and "Done when". Done when, verbatim: a PreToolUse `Bash` hook blocks a command that runs bare `python`, `python3`, `pip` or `pip3`, with a message naming `uv run python` and `jq`; it allows `uv run python`, `uv pip` and `uvx`, and does not block commands that only mention python in arguments, paths or quoted text; tests cover both the blocked and the allowed cases, including commands chained with `&&`, `;` and `|`; `superclaude install` installs and registers the hook, and it fires for subagent Bash calls; `read-parse.md:8` uses `uv run python`; a fresh session that tries `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'` is blocked and pointed to `uv run python` or `jq`.
- Never run `superclaude install` (with or without `--force`) against the live `~/.claude`: other sessions are running. Installer checks use a temporary target path or a temporary HOME only. The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file and never writes to `~/.claude/settings.json` or `~/.claude/hooks/`.
- The hook script is bash plus `jq`, modelled on `src/superclaude/hooks/scripts/freshness-pre-edit.sh`: read the PreToolUse JSON from stdin with `jq`, block with a message on stderr and exit 2, allow with exit 0, never exit 1, and fail open (exit 0) when `jq` is missing, the input is not valid JSON, the tool is not `Bash`, or `tool_input.command` is absent or empty. The hook itself must not run Python.
- Scope of "bare": the command word's basename is exactly `python`, `python3`, `pip` or `pip3` (so `/usr/bin/python3` and `.venv/bin/python` count). Versioned names such as `python3.12` are not part of issue #357 and get no test either way.
- UV for every Python operation in this work (`uv run pytest`, `uv run ruff`); never bare `python`, `python3`, `pip` or `pip3`.
- `src/superclaude/` is the source of truth: run `make sync-dev` after changing hooks or skills, and never stage `.claude/` paths other than `.claude/settings.json`.
- `plugins/superclaude/hooks/hooks.json` already differs from `src/superclaude/hooks/hooks.json` in unrelated entries (ccsession, pragmatic-subagent, auggie matcher). Add only the new registration there; fixing that older drift is out of scope.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included. Staging is not committing.

## Phase 1: Hook script

## Task 1: Add the hook script `block-bare-python.sh` and its plugin mirror

Create `src/superclaude/hooks/scripts/block-bare-python.sh` (mode 0755, `#!/usr/bin/env bash`, `set -u`), following the input, block and fail-open pattern of `src/superclaude/hooks/scripts/freshness-pre-edit.sh` (stdin read with `jq`, stderr message plus `exit 2` to block). Copy it byte-for-byte to `plugins/superclaude/hooks/scripts/block-bare-python.sh` (mode 0755).

Detection rules the script implements:

- Read `.tool_name` and `.tool_input.command`. Only `Bash` is checked; anything else exits 0.
- Split the command into simple commands at unquoted `;`, `&&`, `||`, `|`, `&`, newlines, `(`, `)`, `$(` and backticks. Text inside single quotes, and text inside double quotes, is never a command word (so commit messages, `echo "python3 ..."`, `grep 'pip install'` and `bash -c "python3 ..."` are not blocked). Backslash escapes outside single quotes are honoured when tracking quotes.
- In each simple command, skip leading `NAME=value` assignments, the shell keywords `if`, `then`, `elif`, `else`, `do`, `while`, `until`, `!`, `{`, and the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env` (plus its following options and `NAME=value` words), `timeout` (plus its options and its duration argument) and `command` (only when not followed by `-v` or `-V`, so `command -v python3` stays allowed). The next word is the command word.
- Block when the command word's basename is exactly `python`, `python3`, `pip` or `pip3`. `uv`, `uvx`, `which`, `type`, `command -v`, `grep`, `rg`, `ls`, `cat`, `git` and every other command word are allowed, whatever their arguments contain.
- Lines of a heredoc body are scanned like ordinary lines (a heredoc fed to `bash` with a `python3` line would run it). Document this as a known ceiling in a header comment: a heredoc that only writes text whose line starts with `python3` is blocked too.
- Tokenising is done in `jq` (regex `match`/`scan`) or `awk`, not a per-character bash loop, so a 100 KB command is checked in well under the 3-second registration timeout.

Block message on stderr, one or two lines, starting `UV-ONLY BLOCK:`, naming the offending command word, and telling the agent to use `uv run python ...` (or `uv pip ...` / `uvx ...`) instead, or `jq` to parse JSON. Keep a header comment stating the decision contract (allow exit 0, block exit 2 with stderr, never exit 1, fail open) and citing issue #357.

Acceptance criteria:
- `src/superclaude/hooks/scripts/block-bare-python.sh` and `plugins/superclaude/hooks/scripts/block-bare-python.sh` exist, are executable, and are byte-identical (`cmp` exits 0).
- Piping `{"tool_name":"Bash","tool_input":{"command":"echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'"}}` into the script exits 2 and stderr contains `uv run python` and `jq`; the same payload with command `echo '{}' | jq .` exits 0 with empty stderr. Both runs are recorded in `./artifacts/t1-manual-run.txt`.
- The script contains no call to `python`, `python3`, `pip` or `pip3` (`grep -nE '(^|[^a-z_])(python3?|pip3?)( |$)'` on it matches only comments and the message text, recorded in `./artifacts/t1-manual-run.txt`).

## Task 2: Add behaviour tests for the hook script

Depends on: Task 1

Create `tests/hooks/test_block_bare_python.py`, modelled on `tests/hooks/test_freshness_pre_edit_create_case.py` (runs the real script with `subprocess.run(["bash", str(HOOK)], input=json.dumps(payload).encode(), ...)`, HOME pointed into `tmp_path`). Use `pytest.mark.parametrize` for the case tables.

Blocked cases (exit 2, stderr names `uv run python` and `jq`): `python3 -c 1`; `python script.py`; `pip install requests`; `pip3 install x`; `/usr/bin/python3 -V`; `.venv/bin/python -m pytest`; `cd /tmp && python3 x.py`; `ls; python3 x.py`; `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'` (the issue's fresh-session command); `false || pip install x`; `make build & python3 x.py`; a two-line command whose second line is `python3 x.py`; `echo $(python3 -c 1)`; ``echo `python3 -c 1` ``; `(python3 x.py)`; `if python3 -c 1; then echo ok; fi`; `for f in *.py; do python3 "$f"; done`; `FOO=1 python3 x.py`; `env FOO=1 python3 x.py`; `sudo pip install x`; `timeout 30 python3 x.py`; `nohup python3 x.py`; `exec python3 x.py`.

Allowed cases (exit 0, empty stderr): `uv run python -c 1`; `uv run --no-project python x.py`; `uv pip install requests`; `uvx ruff check .`; `cd /tmp && uv run python x.py`; `grep -rn python3 src/`; `rg 'pip install' docs/`; `ls src/python3/lib`; `cat requirements-python.txt`; `echo "python3 -c 1"`; `echo 'pip install x'`; `git commit -m "stop calling python3 directly"`; `bash -c "python3 x.py"` (quoted text); `command -v python3`; `which pip`; `type python3`; `jq . file.json | head`; and the replaced `read-parse.md` line from Task 5 (`seekable=$(uv run --no-project python -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)`).

Fail-open cases (exit 0): non-JSON stdin; empty stdin; `tool_name` `Read` with a `python3` string in its input; `Bash` with no `command` key; `Bash` with empty command. A timing case: a command of about 100 KB of allowed text plus one trailing `; python3 x.py` is blocked and the hook returns in under 1 second.

Acceptance criteria:
- `uv run pytest tests/hooks/test_block_bare_python.py -v` passes, with every case listed above present as its own parametrized id; output saved to `./artifacts/t2-pytest.log`.
- Chained forms `&&`, `;` and `|` each appear in both a blocked and an allowed case.
- `uv run ruff check tests/hooks/test_block_bare_python.py` and `uv run ruff format --check tests/hooks/test_block_bare_python.py` exit 0.

## Phase 2: Registration and install

## Task 3: Register the hook and add it to the installer list

Depends on: Task 1

In `src/superclaude/hooks/hooks.json` and `plugins/superclaude/hooks/hooks.json`, add one `PreToolUse` registration after the existing `Edit|Write` freshness entry: `{"matcher": "Bash", "hooks": [{"type": "command", "command": "~/.claude/hooks/block-bare-python.sh", "timeout": 3}]}`. Change nothing else in either file.

In `src/superclaude/cli/install_hooks.py`, add `"block-bare-python.sh"` to `_FRESHNESS_SCRIPTS` with a short comment (PreToolUse `Bash` UV-only gate, issue #357, fails open, blocks with exit 2), so `_copy_scripts` installs it to `~/.claude/hooks/` and `make verify-sync`'s installer-registration check stays green.

Run `make sync-dev` so `.claude/hooks/block-bare-python.sh` exists for development (not staged).

Acceptance criteria:
- Both `hooks.json` files parse with `jq .` and contain exactly one PreToolUse entry whose command is `~/.claude/hooks/block-bare-python.sh`, with matcher `Bash` and timeout 3; `git diff` of both files shows only that addition.
- `"block-bare-python.sh"` is in `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py`.
- `make verify-sync` exits 0; output saved to `./artifacts/t3-verify-sync.log`.

## Task 4: Add registration and install tests

Depends on: Task 3

In `tests/cli/test_install_hooks.py`, following `test_real_hooks_json_registers_codegraph_session_start` and `test_codegraph_hook_script_is_packaged_listed_and_mirrored`, add:

- `test_real_hooks_json_registers_block_bare_python`, parametrized over `src` and `plugins`: exactly one PreToolUse entry runs `~/.claude/hooks/block-bare-python.sh`, its matcher is `Bash`, and the hook object equals `{"type": "command", "command": "~/.claude/hooks/block-bare-python.sh", "timeout": 3}`.
- `test_block_bare_python_script_is_packaged_listed_and_mirrored`: the name is in `install_hooks._FRESHNESS_SCRIPTS`; source and mirror are executable and byte-identical.
- `test_install_hooks_installs_and_registers_block_bare_python`: call `install_hooks(target_path=tmp_path / ".claude" / "settings.json")` against the real packaged sources; assert `tmp_path/.claude/hooks/block-bare-python.sh` exists and is executable, and the written `settings.json` has a PreToolUse registration with matcher `Bash` running `~/.claude/hooks/block-bare-python.sh`. Assert that the live `Path.home()/.claude/settings.json` is not the target (no write outside `tmp_path`).

Acceptance criteria:
- `uv run pytest tests/cli/test_install_hooks.py tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -v` passes; output saved to `./artifacts/t4-pytest.log`.
- `uv run ruff check tests/cli/test_install_hooks.py` and `uv run ruff format --check tests/cli/test_install_hooks.py` exit 0.

## Phase 3: Skill fix and changelog

## Task 5: Replace the bare `python3` call in the troubleshoot read/parse probe pack

Edit `src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` line 8 so the probe reads `seekable=$(uv run --no-project python -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)`. `uv run --no-project python` is the form the skills already use for helpers run outside a uv project (`src/superclaude/skills/sc-crash-recovery/refs/pipelines.md`, `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`); it is a `uv run python` call that does not sync whatever project the probed path lives in. Change nothing else in the file, then run `make sync-dev`.

Acceptance criteria:
- `grep -n 'python3' src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` prints nothing, and line 8 contains `uv run --no-project python -c`.
- Feeding that line as a Bash command to `src/superclaude/hooks/scripts/block-bare-python.sh` exits 0 (covered by the Task 2 allowed case).
- `make verify-sync` exits 0.

## Task 6: Add the changelog entry

Depends on: Task 3

Under `## [Unreleased]` in `CHANGELOG.md`, add a section in the file's existing style (`### <title> (#357)` then `#### Added (...)`) stating: the new PreToolUse `Bash` hook `block-bare-python.sh` blocks bare `python`, `python3`, `pip` and `pip3` command words and points to `uv run python` or `jq`; what it allows (`uv run python`, `uv pip`, `uvx`, text-only mentions); that it fails open; that `superclaude install` installs and registers it; and that `read-parse.md` now uses `uv run --no-project python`.

Acceptance criteria:
- `CHANGELOG.md` has the new `(#357)` section under `## [Unreleased]` and above `## [5.0.0]`; no other section changes (`git diff CHANGELOG.md` shows additions only).

## Phase 4: Fresh-session proof

## Task 7: Prove the hook blocks the issue's command in a fresh session and in a subagent

Depends on: Task 2, Task 4, Task 5

Without touching `~/.claude/settings.json` or `~/.claude/hooks/`, write a temporary settings file under `./artifacts/t7-settings.json` that registers the repo script by absolute path: `{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "<absolute path to src/superclaude/hooks/scripts/block-bare-python.sh>", "timeout": 3}]}]}}`. From a scratch directory under `/tmp`, run two fresh non-interactive sessions with `claude -p --settings <that file> --permission-mode bypassPermissions --output-format stream-json --verbose`:

- Main session: prompt it to run exactly `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'` with the Bash tool and report the tool result verbatim.
- Subagent: prompt it to spawn one general-purpose subagent through the Agent tool whose only job is to run that same command with Bash and report the result verbatim.

Save each session's full output to `./artifacts/t7-main-session.jsonl` and `./artifacts/t7-subagent-session.jsonl`, and a short summary of what each shows to `./artifacts/t7-summary.md`. If `claude` cannot run here (no auth, network failure), record the exact error in `./artifacts/t7-summary.md` and report the task as blocked; never mark it passed on the unit tests alone.

Acceptance criteria:
- `./artifacts/t7-main-session.jsonl` shows the Bash tool call for the command, its tool result carrying the `UV-ONLY BLOCK:` message naming `uv run python` and `jq`, and no successful run of `python3`.
- `./artifacts/t7-subagent-session.jsonl` shows the same block on the subagent's Bash call (a tool result with `UV-ONLY BLOCK:` from inside the Agent call).
- `./artifacts/t7-summary.md` records the output of `ls -l ~/.claude/hooks/block-bare-python.sh` and `grep -c block-bare-python ~/.claude/settings.json` taken before and after both runs, and the before and after values are identical (the live `~/.claude` was not installed into).
