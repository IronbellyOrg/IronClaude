22d5ec2bf121b1d761a8ba0a52b35de62d7b8f78
Review one task for spec compliance.

Task brief: ## Task 4: Replace the stale worktree examples in CLAUDE.md

In the repository `CLAUDE.md`, section `### Parallel Development with Git Worktrees` (lines about 301 to 342): (a) add after the bullet that starts `- **Existing checkouts under the retired` one bullet: `- **Names:** a worktree and its branch are named as in \`src/superclaude/core/HOW-WE-WORK.md\`, section "Worktrees and branches": branch \`<login>/issue-<N>[-<words>]\`, at most 24 characters, no spaces; create the worktree with \`--name issue-<N>-<words>\` and Orca adds the login.` (plain backticks); (b) replace the example block (the comment line and the `orca worktree create --name pm-agent ...` line) with the comment `# Create a worktree for issue 289, based on origin/integration, with an agent in it (Orca adds the login: the branch is <login>/issue-289-wtrule)` and the line `orca worktree create --name issue-289-wtrule --base-branch origin/integration --agent claude --prompt "<task>"`; keep the `orca worktree list` example; (c) replace the two `Usage` bullets that name worktree `integration` and worktree `pm-agent` with `- Worktree \`issue-289-wtrule\` (branch \`<login>/issue-289-wtrule\`): created by session A with \`--agent claude\`; that agent works there (path from \`orca worktree list\`)` and `- Worktree \`issue-301-hooks\` (another issue): created by session A with \`--agent claude\`; that agent works there`; (d) change the cleanup line `orca worktree rm --worktree name:integration` to `orca worktree rm --worktree name:issue-289-wtrule`. Do not change the first bullet (ownership), the `ABSOLUTE RULE` text, or any line outside that section. `src/superclaude/core/CLAUDE.md` has no stale name example and is not changed.

Acceptance criteria:
T4.AC1: `grep -n 'pm-agent' CLAUDE.md` prints no line from the worktree section (lines 301 to 345); `grep -n 'name:integration' CLAUDE.md` prints nothing.
T4.AC2: Every `orca worktree create` line of the section still contains `--agent`.
T4.AC3: `uv run pytest tests/core/test_claude_md_worktree_rule.py -q` passes after Task 7 (before Task 7 it still passes: nothing it pins was removed).
Global constraints: ## Constraints

- Test, guide, deck and CLAUDE.md edits only; no production code (nothing under `src/superclaude/cli/`, `scripts/`, hooks or skills changes).
- Never edit or stage anything under `.claude/`. `.dev/tasks/` stays staged.
- ASCII only in the guide section; keep every existing rule that the six answers do not change, in the owner's wording where the source quotes it.
- Decision recorded here: answer 2 says "never stop", so a name whose bare form `<login>/issue-<N>` is over 24 characters is kept and the work goes on. The sentence "create nothing and ask the owner", its key phrase and the "stop" test are replaced. A name that carries words over 24 characters is still an error: drop the words.
- Not in scope (MB-2): reading the digit-run pattern from scripts/worktree_cleanup.py. The user withdrew that item; the hand-copied _NUMBER_RUN of tests/core/test_how_we_work_worktree_policy.py stays as it is.
- The branch `clayphi/issue-289-rest` was created in the reused worktree with `git switch -c` on the owner's order; the guide's "never switch branches in a worktree" line is left as it is.
Start sha: 22d5ec2bf121b1d761a8ba0a52b35de62d7b8f78
Diff against the start snapshot: --- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -313,10 +313,11 @@
 - Never pass Orca link flags (`--issue`, `--pr`) for this repo; the fork rule above (`## ABSOLUTE RULE: PR Target = Fork`) governs them.
 - **Exception — internal temporary checkouts:** a CLI, script or test that creates and removes its own checkout keeps using `git worktree add` directly and must work without Orca. The four cases are: the reflect `--isolate-reviewers` review snapshot; the troubleshoot backtest replay; test fixtures in a pytest temporary directory; and the optional read-only release-tag checkout in `/sc:post-release`, removed after the scan.
 - **Existing checkouts under the retired `.dev/worktrees/` location** may stay until their branch is merged, then are removed with `git worktree remove <path>`; no new checkout may be created there.
+- **Names:** a worktree and its branch are named as in `src/superclaude/core/HOW-WE-WORK.md`, section "Worktrees and branches": branch `<login>/issue-<N>[-<words>]`, at most 24 characters, no spaces; create the worktree with `--name issue-<N>-<words>` and Orca adds the login.
 
 ```bash
-# Create a worktree named pm-agent, based on origin/integration, with an agent in it
-orca worktree create --name pm-agent --base-branch origin/integration --agent claude --prompt "<task>"
+# Create a worktree for issue 289, based on origin/integration, with an agent in it (Orca adds the login: the branch is <login>/issue-289-wtrule)
+orca worktree create --name issue-289-wtrule --base-branch origin/integration --agent claude --prompt "<task>"
 
 # Show where Orca put it
 orca worktree list
@@ -332,13 +333,13 @@
 **Usage**:
 
 - Session A: Open the main checkout (current branch); it is the orchestrator that creates the worktrees below
-- Worktree `integration`: created by session A with `--agent claude`; that agent works there (path from `orca worktree list`)
-- Worktree `pm-agent` (feature branch): created by session A with `--agent claude`; that agent works there
+- Worktree `issue-289-wtrule` (branch `<login>/issue-289-wtrule`): created by session A with `--agent claude`; that agent works there (path from `orca worktree list`)
+- Worktree `issue-301-hooks` (another issue): created by session A with `--agent claude`; that agent works there
 
 **Cleanup**:
 
 ```bash
-orca worktree rm --worktree name:integration
+orca worktree rm --worktree name:issue-289-wtrule
 ```
 
 ## 📝 Key Documentation Files


Codegraph context
index_state: fresh
checked_at: 2026-11-26T17:40:41Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-289
call codegraph only when index_state: fresh, never to widen scope

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