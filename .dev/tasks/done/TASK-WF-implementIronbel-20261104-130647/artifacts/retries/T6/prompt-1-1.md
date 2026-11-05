2715bb769a2bb908092c36189ecf9bec378bc270
Review one task for spec compliance.

Task brief: Task T6 of plan /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md (lines 109-116), verbatim:
## Task 6: Add the changelog entry

Depends on: Task 3

Under `## [Unreleased]` in `CHANGELOG.md`, add a section in the file's existing style (`### <title> (#357)` then `#### Added (...)`) stating: the new PreToolUse `Bash` hook `block-bare-python.sh` blocks bare `python`, `python3`, `pip` and `pip3` command words and points to `uv run python` or `jq`; what it allows (`uv run python`, `uv pip`, `uvx`, text-only mentions); that it fails open; that `superclaude install` installs and registers it; and that `read-parse.md` now uses `uv run --no-project python`.

Acceptance criteria:
- `CHANGELOG.md` has the new `(#357)` section under `## [Unreleased]` and above `## [5.0.0]`; no other section changes (`git diff CHANGELOG.md` shows additions only).

AC ids: T6.AC1 = plan line 116 (new (#357) section under ## [Unreleased] and above ## [5.0.0]; git diff CHANGELOG.md shows additions only).
Implement-time amendments that apply to T6 (recorded at /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/artifacts/amendments.md; the plan file is not edited): AMD-07 (jq precondition stated in the CHANGELOG) and M-CEILINGS (documented ceilings listed in the CHANGELOG entry). Every factual claim in the entry must match the shipped hook /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/src/superclaude/hooks/scripts/block-bare-python.sh, its registration in /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/src/superclaude/hooks/hooks.json and /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/src/superclaude/cli/install_hooks.py, and /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md.
Package root for ./artifacts/ paths: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647. Evidence file: ./artifacts/t6-checks.txt.

Global constraints: plan lines 17-26, verbatim:
## Constraints

- Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), "Proposed fix" and "Done when". Done when, verbatim: a PreToolUse `Bash` hook blocks a command that runs bare `python`, `python3`, `pip` or `pip3`, with a message naming `uv run python` and `jq`; it allows `uv run python`, `uv pip` and `uvx`, and does not block commands that only mention python in arguments, paths or quoted text; tests cover both the blocked and the allowed cases, including commands chained with `&&`, `;` and `|`; `superclaude install` installs and registers the hook, and it fires for subagent Bash calls; `read-parse.md:8` uses `uv run python`; a fresh session that tries `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'` is blocked and pointed to `uv run python` or `jq`.
- Never run `superclaude install` (with or without `--force`) against the live `~/.claude`: other sessions are running. Installer checks use a temporary target path or a temporary HOME only. The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file and never writes to `~/.claude/settings.json` or `~/.claude/hooks/`.
- The hook script is bash plus `jq`, modelled on `src/superclaude/hooks/scripts/freshness-pre-edit.sh`: read the PreToolUse JSON from stdin with `jq`, block with a message on stderr and exit 2, allow with exit 0, never exit 1, and fail open (exit 0) when `jq` is missing, the input is not valid JSON, the tool is not `Bash`, or `tool_input.command` is absent or empty. The hook itself must not run Python.
- Scope of "bare": the command word's basename is exactly `python`, `python3`, `pip` or `pip3` (so `/usr/bin/python3` and `.venv/bin/python` count). Versioned names such as `python3.12` are not part of issue #357 and get no test either way.
- UV for every Python operation in this work (`uv run pytest`, `uv run ruff`); never bare `python`, `python3`, `pip` or `pip3`.
- `src/superclaude/` is the source of truth: run `make sync-dev` after changing hooks or skills, and never stage `.claude/` paths other than `.claude/settings.json`.
- `plugins/superclaude/hooks/hooks.json` already differs from `src/superclaude/hooks/hooks.json` in unrelated entries (ccsession, pragmatic-subagent, auggie matcher). Add only the new registration there; fixing that older drift is out of scope.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included. Staging is not committing.

Start sha: 2715bb769a2bb908092c36189ecf9bec378bc270
Diff against the start snapshot:
diff --git a/CHANGELOG.md b/CHANGELOG.md
index e18e86ad..df26aac7 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,17 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### Hooks: block bare python, python3, pip and pip3 in Bash calls (#357)
+
+#### Added (UV-only Bash hook)
+
+- New PreToolUse `Bash` hook `block-bare-python.sh`. A Bash tool call whose command runs bare `python`, `python3`, `pip` or `pip3` as a command word is blocked (exit 2), and the message tells the agent to use `uv run python` (or `uv pip`, `uvx`) instead, or `jq` to parse JSON. It also fires for subagent Bash calls. The "use UV for all Python" rule was text-only until now, and agents and helper subagents kept breaking it.
+- Allowed: `uv run python`, `uv pip`, `uvx`, and commands that only mention python in arguments, paths, patterns, quoted text, comments or heredoc text, such as `grep -rn python3 src/`, `echo "python3 -c 1"`, `command -v python3` or a multi-line `git commit -m "$(cat <<'EOF' ...)"` message. Commands chained with `&&`, `||`, `;`, `|` or `&`, wrapped in `sudo`, `env`, `timeout`, `nice`, `nohup`, `time`, `exec` or `command`, or nested in `$(...)`, backticks (also inside double quotes), subshells or process substitution are checked word by word. Quoted command words (`"python3" x.py`) and paths (`.venv/bin/python`) count as bare.
+- It fails open (allows the command) when it cannot judge it: `jq` or `awk` missing, input that is not valid JSON, a tool other than Bash, or an empty command. The hook needs `jq`; on a host without `jq` it allows every command.
+- Known limits, commands it does not catch: string arguments to another interpreter (`bash -c "python3 x"`, `eval`, `env -S`), commands started by another program (`xargs python3`, `find -exec python3`), a heredoc piped into a shell (`cat <<'EOF' | bash`), `${...}` parameter expansions, nested backticks written with `\``, versioned names such as `python3.12`, shell commands run by tools other than Bash, and `claude --bare` sessions, which skip settings hooks.
+- `superclaude install` copies the hook to `~/.claude/hooks/` and registers it in `~/.claude/settings.json`; the plugin mirror registers it too.
+- `sc:troubleshoot`'s read/parse probe pack (`refs/probe-packs/read-parse.md`) now runs its seek probe with `uv run --no-project python` instead of bare `python3`.
+
 ## [5.0.0] - 2026-11-02
 
 Major release: codegraph replaces codebase-memory-mcp and Serena, and several commands, flags and core files are removed. Read the [5.0.0 release notes](docs/releases/v5.0.0.md) for the breaking changes and upgrade steps. This is the first versioned section of this changelog; it covers every change since the package version was set to 4.3.5 (2026-06-04), which was never tagged.
=== new file: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/artifacts/t6-checks.txt (full contents, numbered)
     1	$ git diff --numstat -- CHANGELOG.md   (added, deleted)
     2	11	0	CHANGELOG.md
     3	$ grep -n "^## \|(#357)" CHANGELOG.md | head -4
     4	5:## [Unreleased]
     5	7:### Hooks: block bare python, python3, pip and pip3 in Bash calls (#357)
     6	18:## [5.0.0] - 2026-11-02

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
