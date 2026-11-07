30ad6cba86190d30a273f11ef980dafd765b1244
Review one task for spec compliance.

Task brief: ## Task 4: Add the Orca check and Wave 7 to the issue skill and claim ref

Depends on: Task 2

Edit `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `tests/skills/test_issue_protocol.py`. Source: design sections 7 (Wave 0, Wave 6, Wave 7), 10 and 11.

In `refs/claim.md` Wave 0 add a new step 3 after `gh auth status` and before the default-branch lookup: run `uv run --no-project python "<skill base>/scripts/orca_worktree.py" preflight`; `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`, before any GitHub or ClickUp write. Replace Wave 6 step 4 ("Print the `next-steps.md` path and STOP") with a hand-off: after both comments are posted, run Wave 7 (and Wave 8, added by a later task); any STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. Add Wave 7: run `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>`, read its JSON, every failure is a warning and the claim `status` stays `success`; print the worktree path, status, match key, the "reused a worktree not created by /sc:issue" line for keys `basename` and `branch`, the "untracked, do not stage" line when no file under the worktree's `.dev/issues/<N>/` is tracked, "run `make sync-dev` there first" when `<wt>/.claude/` is absent and the plan needs an unsynced primitive, and each warning with its remedy line from design section 11 (worktree codes).

In `SKILL.md`: add the `scripts/orca_worktree.py` row to the files table; update the claim-mode paragraph and claim step 1 (Wave 0 check) and step 7 (Wave 6 now continues to the worktree step); add `E-ORCA-REQUIRED` and the worktree warning codes to the error table; keep the file under 500 lines. Update `tests/skills/test_issue_protocol.py`: the files-table test accepts the new script, ST-5 (still five refs, script named and present), ST-6 (preflight in Wave 0 before Wave 1, Wave 7 after the Wave 6 posts).

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_orca_worktree.py` passes.
- `grep -n "src/superclaude" src/superclaude/skills/sc-issue-protocol/SKILL.md src/superclaude/skills/sc-issue-protocol/refs/claim.md` finds nothing.
- `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` reports fewer than 500 lines.

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T4.AC1, T4.AC2, ... in the order of the 'Acceptance criteria:' bullets).
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: 30ad6cba86190d30a273f11ef980dafd765b1244
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T4-r1-1.patch (read it in full); the live files are in the repository for anchor checks
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
