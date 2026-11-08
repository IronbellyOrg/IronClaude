eaa4ef9f93c647de813eb2bfee32fc338f34ece8
Review one task for spec compliance.

Task brief: ## Task 3: Make `orca_worktree.py worktree` close Orca's plain first tab after a new create

Change `cmd_worktree` and `finish` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (create call at about lines 594-613; new-row handling at about lines 614-646; `finish` at about lines 494-532). The close step runs only when the status is `created` (never on the reused path, which also goes through `finish`), only after `finish`'s git-common-dir check passed and the `.dev/issues/<N>/` copy succeeded, and before the command returns (so before any launch):
- Parse the create's `--json` reply, an envelope `{"ok": …, "result": {…}}`. Read `result.setup` and `result.defaultTabs`. If either reports a setup or default tabs, close nothing and warn. If the reply is missing, not JSON, not `ok`, or the create timed out (the code already continues after `created.timed_out`), close nothing and warn: an unknown reply never leads to a close.
- Otherwise run `orca terminal list --worktree path:<path> --json`; if it lists exactly one terminal and that terminal's `agentIdentity` is absent or empty, close that tab with `orca terminal close --terminal <handle> --tab --json`.
- Any list or close failure, malformed list reply, zero or several terminals, or a terminal with an agent is a non-fatal warning (new code `W-FIRST-TAB-LEFT`, reason in `detail`) and never changes `status`. A failed copy keeps the plain tab and reports its existing copy warning; nothing is closed.
- Add `W-FIRST-TAB-LEFT` to `WARNING_ORDER` (lines 198-206) at a stated rank: `Outcome.as_dict` ranks notes with `min(..., key=WARNING_ORDER.index)`, which raises `ValueError` for an unlisted code. Add it with its remedy line ("close the plain tab in Orca by hand") to the worktree-warning list in `src/superclaude/skills/sc-issue-protocol/SKILL.md` (about line 149) and the Wave 7 table in `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, and make the claim's Final output print `worktree_warning` so an unattended run shows it.
- Update the module docstring (lines 20-30) for the two `terminal` calls.

Update `tests/skills/test_issue_orca_worktree.py`: give the fake Orca `terminal list` and `terminal close` responders; add a valid-JSON create reply fixture for the close path (`created_scene()` returns "opaque, not json", so it cannot drive the close); the exact call list in `test_fo18_exact_commands_and_no_forbidden_flag` (around lines 794-820) uses the valid-reply fixture and gains the two `terminal` calls; the opaque-reply FO-11 test (around lines 552-561) now expects `W-FIRST-TAB-LEFT` and no `terminal` call; add tests for setup reported, default tabs reported, a timed-out create, list failure, malformed list reply, zero terminals, two terminals, one terminal with an agent, close failure (status `created`), a failed copy (no close), a new row whose path belongs to another repository (failed, zero `terminal` calls), a reused worktree (no `terminal` call), and `W-FIRST-TAB-LEFT` as the only note and together with `W-WORKTREE-COPY-FAILED` (JSON printed, no exception). `--agent`, `--prompt` and `--surface` stay only in `cmd_launch`, and no flag from `NEVER_FLAGS` or the link flags is used (`tests/skills/test_issue_protocol.py` around lines 336-370).

Acceptance criteria:
- [T3.AC1] `uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v` passes.
- [T3.AC2] A created-worktree run against the fake Orca with a valid create reply records, in order: `worktree list`, `worktree create`, `worktree list`, `terminal list --worktree path:<wt> --json`, `terminal close --terminal <handle> --tab --json`; the close comes after the copy.
- [T3.AC3] `WARNING_ORDER`, `SKILL.md` and `refs/claim.md` list `W-FIRST-TAB-LEFT`, the last two with its remedy line.

AC ids: T3.AC1, T3.AC2, T3.AC3
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
Start sha: eaa4ef9f93c647de813eb2bfee32fc338f34ece8
Diff against the start snapshot: read the file .dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/diffs/T3-diff-1-1.patch (`git diff <start> <reviewed tree>` limited to this task's touched files; new files appear in full as additions). Also read the live files it names.
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
