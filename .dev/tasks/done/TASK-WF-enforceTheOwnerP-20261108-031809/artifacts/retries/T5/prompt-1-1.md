79c92458b77bff1efda856ea8a9b3a4bfb2ac0c8
Review one task for spec compliance.

Task brief: ## Task 5: Record the new decisions in the /sc:issue design docs

Depends on: Task 4

In `docs/designs/sc-issue-claim-pipeline-flag.md`: change the `none` row of the level table (around line 21), P4 (around line 42), the `--pipeline` options row (around line 75), the Wave 7 line (around line 149) and LA-7/ST-9 (around lines 340 and 355) so `none` creates no worktree; add to section 8.3 (around line 184) the first-tab close step from Task 3 and its warning `W-FIRST-TAB-LEFT`; add a dated note to D2 (around line 370) and FO-18 (around line 333) that they stay, and why (the claim must copy files and write the pending record before its agent starts). In `docs/designs/sc-issue-command.md`, update B17 (around line 44) where it says `none` means "worktree only, no agent". Also update the user-facing text: `docs/user-guide/commands.md` lines 367, 379 and 394 (they say `none` creates the worktree and that you run the steps in it), and the `/sc:issue` routing row in `src/superclaude/core/HOW-WE-WORK.md` (line 329); after editing `HOW-WE-WORK.md`, copy it byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` as the project `CLAUDE.md` requires. Cite the owner decisions of 2026-11-08 (including the approval of the first-tab close in place of agent-on-create), `.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/REPORT.md` and the review report `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md`.

Acceptance criteria:
- [T5.AC1] `grep -n "none" docs/designs/sc-issue-claim-pipeline-flag.md` shows no remaining statement that `none` creates a worktree.
- [T5.AC2] Section 8.3 names the `terminal list` and `terminal close` calls and `W-FIRST-TAB-LEFT`.
- [T5.AC3] `uv run pytest tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py tests/core/ -v` still passes (no test pins the changed doc lines, or the pins are updated).
- [T5.AC4] `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference, and `docs/user-guide/commands.md` no longer says `none` creates a worktree.

AC ids: T5.AC1, T5.AC2, T5.AC3, T5.AC4
Global constraints: - Owner decisions recorded 2026-11-08 during planning (they refine the source): a session may not create a worktree for its own use; every worktree gets an agent; the session that creates a worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns its agent(s); a human-created worktree also needs an agent. `/sc:issue --pipeline none` now creates no worktree (it stops after the comments, `issue-summary.md` and `next-steps.md`); the default `--pipeline worktree` and `full` keep launching an agent.
- Deviation from the source, approved by the owner on 2026-11-08 after the pre-execution review (`.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md`, Grounding Gap G-1): for `/sc:issue`, the agent does NOT come with the create. The claim must copy `.dev/issues/<N>/` (including `launch-prompt.md`) into the new worktree, pass the repository check and write the launch-level pending record before the agent starts (a failed copy means no agent), so the script keeps create → copy → `agent launch` and closes Orca's plain first tab itself after a successful copy. FO-18 (no `--agent` on the claim's create) therefore stays. The owner also confirmed on 2026-11-08 that the hook and the script change stay (an instruction-only fix was rejected).
- Only the `--agent` requirement is enforced by the hook. "No worktree for your own use", "the creator owns the agent" and "a human-created worktree needs an agent" stay instruction text.
- Accepted consequences, each reported as a warning, never a failed claim: a failed launch (`W-LAUNCH-FAILED`) leaves a worktree with no agent and no tab (re-run the claim); any post-create path that cannot close the tab (unknown create reply, list failure, AMBIGUOUS, row not listed or not on disk, a failed copy, a later reused match) leaves the plain tab with `W-FIRST-TAB-LEFT`.
- Line anchors in this plan are approximate. Re-read `cmd_worktree`, `finish`, `Outcome.as_dict` and every cited test before editing.
- Evidence for every behaviour claim lives in `.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/` (REPORT.md and tier1-observation.md N1, N8, N10, N13, N14). Orca source citations there are from the local IronOrca checkout; do not change Orca.
- Out of scope: `src/superclaude/core/WORKER-CONTRACT.md` (WC-13; a separate sub-orchestrator/coordinator issue covers it), supervised `worker-start` (already creates worktrees with an agent), closing existing empty tabs, any Orca change.
- Keep: Orca-only worktree creation (`CLAUDE.md:307`, `:312`); never pass Orca link flags (`--issue`, `--pr`, `--linear-issue`, `--reference*`, `--gitlab*`) for this repo; never hardcode `src/superclaude/` paths inside installed primitive text; edit `src/superclaude/...` then `make sync-dev` and `make verify-sync`; never stage `.claude/` paths other than `.claude/settings.json`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Use `uv run` for every Python and pytest command.
Start sha: 79c92458b77bff1efda856ea8a9b3a4bfb2ac0c8
Diff against the start snapshot: read the file .dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/diffs/T5-diff-1-1.patch (`git diff <start> <reviewed tree>` limited to this task's touched files; new files appear in full as additions). Also read the live files it names.
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
