2a6d533a7b134d443849a355f234aab37bd83538
Review one task for spec compliance.

Task brief: ## Task 6: Update the project worktree rule and its example in `CLAUDE.md`

Depends on: Task 2

In `CLAUDE.md`, section "Parallel Development with Git Worktrees" (rule at lines 307-310, bullets from line 312, example block at lines 318-324): state that every Orca worktree is created with an agent (`orca worktree create --name <name> --agent claude --prompt "<task>"`, plus `--repo`, `--base-branch`, `--parent-worktree`/`--no-parent` as needed), that no session creates a worktree for its own use, that the session creating it becomes its orchestrator (or coordinator under another orchestrator) and owns its agent(s), and that a PreToolUse hook blocks a bare create once it is installed. Insert the ownership point as the first list item at line 312. Change the example at line 320 to carry `--agent claude --prompt "<task>"`, since the hook would block the bare example. Also change line 305 ("give each session its own worktree") and the Usage block at lines 333-337, which tell sessions to open their own worktrees: a worktree is created by its orchestrator with an agent in it. Keep the Orca-only rule, the link-flag bullet and the internal-temporary-checkout exception unchanged. Add a test in `tests/core/` that the project `CLAUDE.md` section from `### Parallel Development with Git Worktrees` to the first following `\n## ` contains `--agent claude`, the phrase `every worktree gets an agent`, the phrase `never create a worktree for your own use`, and the words `orchestrator`, `coordinator` and `owns` in the ownership item (case-insensitive), that the example line contains `--agent`, and that the Orca-only rule, link-flag bullet and temporary-checkout exception are still present.

Acceptance criteria:
- [T6.AC1] The new test passes under `uv run pytest tests/core/ -v`.
- [T6.AC2] `grep -n "orca worktree create --name pm-agent --base-branch origin/master$" CLAUDE.md` prints nothing.

AC ids: T6.AC1, T6.AC2
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
Start sha: 2a6d533a7b134d443849a355f234aab37bd83538
Diff against the start snapshot: read the file .dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/diffs/T6-diff-1-1.patch (`git diff <start> <reviewed tree>` limited to this task's touched files; new files appear in full as additions). Also read the live files it names.
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
