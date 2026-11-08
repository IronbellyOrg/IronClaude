0d1379c30ae157c1edbb0d09e02b477f80419639
Review one task for spec compliance.

Task brief: ## Task 2: Register the hook and its mirror, and update every test that enumerates hooks

Depends on: Task 1

Register `~/.claude/hooks/require-orca-worktree-agent.sh` as a PreToolUse `Bash` hook in `src/superclaude/hooks/hooks.json` with its own registration entry and `"timeout": 3`, next to the `block-bare-python.sh` entry. Add `"require-orca-worktree-agent.sh"` with a one-line comment to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py` (beside `block-bare-python.sh`). Copy the script byte-for-byte and executable to `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, and add the same registration to `plugins/superclaude/hooks/hooks.json`. Update the tests that list hooks: the fake script list in `tests/cli/test_install_hooks.py` (around lines 96-104), the hooks package file list in `tests/unit/test_cli_install.py` (around line 139), and the exact Bash-hook set asserted in `tests/hooks/test_freshness_subagent_start_policy.py` (around lines 104-117). In `tests/cli/test_install_hooks.py` add, next to `test_real_hooks_json_registers_block_bare_python` and `test_block_bare_python_script_is_packaged_listed_and_mirrored` (around lines 760-790), the same two checks for the new hook (registered once under matcher `Bash` with timeout 3 in both trees; listed in `_FRESHNESS_SCRIPTS`; source and mirror executable and byte-identical) and an installed-settings check like `_assert_block_bare_python_installed`. `launch-job-identity.sh` (also a PreToolUse Bash hook) replaces the whole input through `updatedInput` and wraps the original command as a quoted argument, and its header says the rewrite order of other hooks is unspecified. Add a test that feeds the new hook the event a governed session would produce for a bare create (the original command, with launch-level state present) and expects exit 2, and record in the artifact that the live order of the two hooks is unverified.

Acceptance criteria:
- [T2.AC1] `uv run pytest tests/cli/test_install_hooks.py tests/unit/test_cli_install.py tests/hooks/test_freshness_subagent_start_policy.py tests/hooks/test_block_bare_python.py tests/cli/test_verify_sync_hooks.py -v` passes (run `tests/cli/test_verify_sync_hooks.py` alone, not in parallel with other source-changing work, because it edits files in place).
- [T2.AC2] `cmp src/superclaude/hooks/scripts/require-orca-worktree-agent.sh plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` reports no difference, and `make verify-sync` exits 0.
- [T2.AC3] The governed-session test exists and passes; `./artifacts/t2-launch-identity-interaction.md` names it and states that the live hook order is unverified.

AC ids: T2.AC1, T2.AC2, T2.AC3
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
Start sha: 0d1379c30ae157c1edbb0d09e02b477f80419639
Diff against the start snapshot: read the file .dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/artifacts/diffs/T2-diff-1-1.patch (`git diff <start> <reviewed tree>` limited to this task's touched files; new files appear in full as additions). Also read the live files it names.
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
