63bc2f2d6ba74a4dfa77e9cc959c9cd975fe8669
Review one task for spec compliance.

Task brief: ## Task 1: Create scripts/orca_worktree.py with its shared helpers and the preflight subcommand

Create `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (Python standard library only, executable-style header like `clickup_claim.py` in the same folder) and `tests/skills/test_issue_orca_worktree.py`. Source: design sections 8 (intro) and 8.1.

The script uses `argparse` subparsers `preflight`, `worktree`, `prompt`, `launch` (the last three are added by later tasks; register only `preflight` now). It prints exactly one JSON object on stdout, exits 0 for every runtime outcome and 2 only for bad arguments (argparse default). A shared `run(argv, timeout)` helper runs a command without a shell, captures output, and returns a failed result (never raises) on timeout, nonzero exit or missing binary. Timeouts: 120 s default, 30 s for `preflight`, 15 s for each `orca terminal read`.

`preflight` runs `orca status --json` and prints `{"ok": true}` only when the command exits 0 and the JSON has `ok: true` and `result.runtime.reachable: true`; otherwise `{"ok": false, "detail": "<first stderr line or why the JSON failed>"}`. A missing `orca` binary gives the same shape.

The test file builds the reusable fixtures for the whole feature: a fake `orca` script written to a temporary directory that logs every argv to a file and answers from per-test JSON, a temporary git repository with an `origin` remote, and a temporary `HOME`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k preflight` passes with cases PF-1 (ok: true) and PF-2 (not reachable, nonzero exit, invalid JSON, and no `orca` on `PATH` each give `ok: false` with a non-empty detail).
- A call with a bad subcommand or missing required argument exits 2.
- A hanging fake `orca` is cut by the timeout and reported as `ok: false`, not as a crash (the timeout is overridable in the test through an environment variable or function argument so the test runs in under 5 seconds).

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T1.AC1, T1.AC2, ... in the order of the 'Acceptance criteria:' bullets).
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: 63bc2f2d6ba74a4dfa77e9cc959c9cd975fe8669
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T1-r1-1.patch (read it in full); the live files are in the repository for anchor checks
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
