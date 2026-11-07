58e8f0c23d2d644528aeed3d019398a3c60b85cf
Review one task for spec compliance.

Task brief: ## Task 7: Add Wave 5 additions, Wave 8, the Plan boundary line and the claim return contract

Depends on: Task 4, Task 5, Task 6

Edit `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md` and `tests/skills/test_issue_protocol.py`. Source: design sections 7 (Wave 5 additions, Wave 8, final output), 10 and 11.

In `templates/next-steps.md` add the line `Plan boundary: after step <K>` under the title. In `refs/claim.md` Wave 5 add: the skill sets `<K>` to the number of the last step before the first step whose command is `/sc:implement` or `/task` (the line reads `Plan boundary: before step 1` when the first step is the implementation step; `--pipeline full` ignores it); for any `--pipeline` value other than `none`, run `uv run --no-project python "<skill base>/scripts/orca_worktree.py" prompt --template "<skill base>/templates/launch-prompt.md" --level <L> [--submit] --number <N> --out "<D>/launch-prompt.md"` before Wave 7 so the copy carries it. Add Wave 8: runs only when `--pipeline` is not `none` and Wave 7 status is `created` or `reused`; run `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]`; never attempted for a `failed` worktree; failures are warnings and the claim stays `success`. Replace the Wave 6 hand-off with the final output of design section 7 (next-steps path, worktree line, launch result lines for launched, already_launched and none, every warning with its remedy line from design section 11 including the three launch codes, then the return contract).

In `SKILL.md`: add the `templates/launch-prompt.md` row to the files table; replace the claim-mode return contract with the ten fields of design section 10 (`pipeline_level`, `submit`, `worktree_status`, `worktree_path`, `worktree_branch`, `worktree_match_key`, `worktree_warning`, `launch_status`, `launch_warning`, `enforcement_hook`), create mode unchanged; add `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `E-CLAIM-ONLY-FLAG` and `E-SUBMIT-NEEDS-FULL` to the error table; update the Will and Will Not lists to match the command file (the skill itself still runs no next-step command; the launched agent does; nothing merges). Add tests ST-4 (no forbidden Orca flag in skill, refs, command or script outside the launch call), ST-7 (`Plan boundary` in the template and the `<K>` rule in the ref), ST-9 (Wave 8 skipped for `none`, prompt file written before Wave 7), ST-10 (the ten contract fields), ST-11 part one (no `src/superclaude/` path in any file of the skill).

Acceptance criteria:
- `uv run pytest tests/skills tests/commands` passes.
- `wc -l src/superclaude/skills/sc-issue-protocol/SKILL.md` reports fewer than 500 lines.
- `grep -rn "src/superclaude" src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol` finds nothing.

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T7.AC1, T7.AC2, ... in the order of the 'Acceptance criteria:' bullets). Section 18 items that touch this task: A3 (the ten claim fields are added to the shared contract of `SKILL.md`; the nine existing fields stay; create mode prints none of the new fields; ST-10 asserts both), A4 (ST-4 compares whole `--` tokens by equality with the forbidden list, ignoring the launch call's `--agent`, `--prompt`, `--surface`; for markdown it scans only lines holding an `orca ` command), A6 (when `<D>/worktree.json` already has a `launch` entry, Wave 5 does not rewrite `<D>/launch-prompt.md`), M-3 (rewrite SKILL.md claim steps 6 and 7 and the claim-mode paragraph), and B-1 (every new line naming a git or gh write verb under the skills tree needs an exact-text entry in `tests/skills/test_worker_contract.py`, which passes). The `templates/launch-prompt.md` files-table row was added in Task 5 and the `E-ORCA-REQUIRED` and worktree warning rows in Task 4. Because the grep in the third criterion also matches binary bytecode caches under the skill folder, read it as a search of the text files (`--include='*.md' --include='*.py'`).
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: 58e8f0c23d2d644528aeed3d019398a3c60b85cf
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T7-r1-1.patch (read it in full); the live files are in the repository for anchor checks
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
