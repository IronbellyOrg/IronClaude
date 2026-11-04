a22c474046b73c9a6dae6a2b9e3dc2c6d65b2ea9
Review one task for spec compliance.

Working directory (git worktree): /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall. You may Read files and run read-only git/grep commands there. Do not edit anything.
Task brief: ## Task 3: Make the shim leave the launcher's session and process group at start-up

Depends on: Task 2

In `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` `__main__` (lines 857-872), before `ThreadingServer(LISTEN, Handler)` binds, call `os.setsid()` inside `try/except OSError: pass` (it raises when the process already leads a process group, for example when run by hand in an interactive shell), with a short comment saying why: a shim is shared by many sessions, so terminal or process-group signals aimed at the session that started it must not reach it. No fork, no new import (`os` is already imported), argv and env unchanged.

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k "directly_started_shim" -q` passes.
- `uv run pytest tests/unit/test_ccsession_tiers.py -q` and `uv run pytest tests/unit/test_ccsession_tag.py -q` pass except `test_shim_outlives_the_terminal_that_started_it`, which still fails until Task 4 (its failure reason recorded in ./artifacts/t3-tests.log).
AC ids: T3.AC1 (first bullet), T3.AC2 (second bullet). Task-owned evidence file: .dev/tasks/to-do/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t3-tests.log (written by this task; read it). Context: a pre-execution review of this plan asked that setsid run only when stderr is not a terminal, so a shim started by hand with output on a terminal can still be stopped with Ctrl-C; the implementation includes that guard.
Global constraints: ## Constraints

- Scope is exactly the four files named in the source: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md`. Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341).
- Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them); never edit anything under `~/.claude`, `~/.ccsession` or the running config; never run `superclaude install`, `superclaude update`, `./update.sh` or `install.sh`.
- Doc restrictions (remediation-source.md AC6; doc-context.md in the troubleshoot directory): the shim's argv keeps the script path (ccsession uses `pgrep -f -- "$CC_SHIM_SCRIPT"` at ccsession:722 and users stop shims with `pkill -f local-gateway-alias-proxy.py`); the shim inherits the launching env; no `setsid` binary (macOS has none) and only Python standard library; bash 3.2 syntax; logging stays opt-in; ccsession never stops a running shim.
- Tests: run only named test files and tests that read the edited files; never the full suite and never `tests/cli/eval/` as a directory. Use `uv run` for Python.
- Every throwaway shim or test process started while working is stopped by its exact pid; no temp files left behind.
Start sha: a22c474046b73c9a6dae6a2b9e3dc2c6d65b2ea9
Diff against the start snapshot: the output of `git diff a22c474046b73c9a6dae6a2b9e3dc2c6d65b2ea9 -- src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` in the working directory (the `__main__` block). Run that command to get the exact diff. New untracked file in the touched set: .dev/tasks/to-do/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t3-tests.log (read its full contents).
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

Use finding ids F1.1, F1.2, ... Return the AC marks and finding lines as your final message (plain text, no file writes).
