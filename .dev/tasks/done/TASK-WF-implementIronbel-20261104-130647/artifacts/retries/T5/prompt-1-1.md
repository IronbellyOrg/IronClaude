88fc53e04fdd618482a8d6a277263e0036991c15
Review one task for spec compliance.

Task brief: Task T5 of plan /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md (lines 100-107), verbatim:
## Task 5: Replace the bare `python3` call in the troubleshoot read/parse probe pack

Edit `src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` line 8 so the probe reads `seekable=$(uv run --no-project python -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)`. `uv run --no-project python` is the form the skills already use for helpers run outside a uv project (`src/superclaude/skills/sc-crash-recovery/refs/pipelines.md`, `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`); it is a `uv run python` call that does not sync whatever project the probed path lives in. Change nothing else in the file, then run `make sync-dev`.

Acceptance criteria:
- `grep -n 'python3' src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md` prints nothing, and line 8 contains `uv run --no-project python -c`.
- Feeding that line as a Bash command to `src/superclaude/hooks/scripts/block-bare-python.sh` exits 0 (covered by the Task 2 allowed case).
- `make verify-sync` exits 0.

AC ids: T5.AC1 = plan line 105 (no python3 in read-parse.md; line 8 contains uv run --no-project python -c); T5.AC2 = plan line 106 (feeding that line to the hook exits 0, covered by the Task 2 allowed case); T5.AC3 = plan line 107 (make verify-sync exits 0).
Package root for ./artifacts/ paths: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647. Evidence file: ./artifacts/t5-checks.txt. The Task 2 test file is /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/tests/hooks/test_block_bare_python.py (allowed case id read-parse-line). make sync-dev also refreshed the gitignored .claude/ copies (not staged).

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

Start sha: 88fc53e04fdd618482a8d6a277263e0036991c15
Diff against the start snapshot:
diff --git a/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md b/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md
index 6b03f60b..63cbe95d 100644
--- a/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md
+++ b/src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md
@@ -5,6 +5,6 @@ Loaded by Wave 1.6 S1.6.4 only when a `surviving=yes` producer's primitive kind
 ```bash
 fstype=$(stat -f -c %T "$NODE")          # sysbox-fs: fuseblk
 size=$(stat -c %s "$NODE")               # kernel procfs 0; FUSE emulation 4096
-seekable=$(python3 -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)
+seekable=$(uv run --no-project python -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)
 # add rows only with an incident citation; never a decision input
 ```
=== new file: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/artifacts/t5-checks.txt (full contents, numbered)
     1	$ grep -n 'python3' src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md   (expect no output)
     2	rc=1
     3	$ sed -n 8p src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md
     4	seekable=$(uv run --no-project python -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)
     5	$ hook run on line 8 as a Bash command
     6	rc=0
     7	$ make verify-sync
     8	rc=0
     9	$ git diff --stat
    10	 .../skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md      | 2 +-
    11	 1 file changed, 1 insertion(+), 1 deletion(-)

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
