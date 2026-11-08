359e029a25738cc2310da40aebf0784dd401c2ef
Review one task for spec compliance.

Task brief: ## Task 4: Make `--pipeline none` create no worktree

Depends on: Task 3

In `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, Wave 7 ("Runs for every `--pipeline` value") now runs only when `--pipeline` is not `none`; Wave 8 is unchanged (already skipped for `none`). For `none`, the claim ends after both comments are posted; `worktree_status` in the final return contract is `not_requested`, and `worktree_path`, `worktree_branch`, `worktree_match_key` and `worktree_warning` are `null` (update the return-contract block in `src/superclaude/skills/sc-issue-protocol/SKILL.md`, about lines 121-136, keeping its ten keys). Also update every other place that says the worktree is made for every value: `SKILL.md` line 17 and line 170 ("create or reuse the Orca worktree"), lines 90-91 (Wave 6 "continue with Wave 7 and Wave 8"; Wave 7 has no `none` exclusion), and `refs/claim.md` line 93 ("run Wave 7, then Wave 8"), line 97 ("Runs for every `--pipeline` value") and lines 131-136 (Final output "Worktree: <path>" and "Open <wt> and run next-steps there": for `none` they say no worktree and point at the main checkout's `.dev/issues/<N>/next-steps.md`). Lines 89, 92 and 150 of `SKILL.md` already handle `none`; leave them. Keep the Wave 0 Orca check for `none` (design rule P1: Orca is a dependency) and say so in the Wave 0 text. In `src/superclaude/commands/issue.md`, update the `--pipeline` row (line 43: "Every value creates the worktree; `none` launches no agent") to say `none` creates no worktree and launches no agent, and update the lines about `none` at about 77, 80, 88 and 111 (the user runs `next-steps.md` from the main checkout's `.dev/issues/<N>/`). Keep the three values and the default `worktree`. No existing pin quotes the old `none` wording (the ST-9 test around lines 431-463 pins only the Wave 8 skip), so add new pins in `tests/skills/test_issue_protocol.py`: `refs/claim.md` skips Wave 7 for `none`; the `none` Final output has no worktree line and points at the main checkout; the four worktree fields are `null` for `none`.

Acceptance criteria:
- [T4.AC1] `uv run pytest tests/commands/test_issue_command.py tests/skills/test_issue_protocol.py -v` passes.
- [T4.AC2] `grep -n "Every value creates the worktree\|Runs for every \`--pipeline\` value" src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol/refs/claim.md` prints nothing, and `grep -n "create or reuse the Orca worktree" src/superclaude/skills/sc-issue-protocol/SKILL.md` shows only lines that exclude `none`.
- [T4.AC3] `refs/claim.md` Wave 7 states it does not run for `--pipeline none`, and `SKILL.md` shows `worktree_status: not_requested` for `none`.

AC ids: T4.AC1, T4.AC2, T4.AC3
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
Start sha: 359e029a25738cc2310da40aebf0784dd401c2ef
Diff against the start snapshot: read the file .dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/diffs/T4-diff-1-1.patch (`git diff <start> <reviewed tree>` limited to this task's touched files; new files appear in full as additions). Also read the live files it names.
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
