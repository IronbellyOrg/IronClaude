c554091dc16a3ea433df636beb4564a02571a0df
Review one task for spec compliance.

Task brief: ## Task 2: Copy the guide byte for byte to the plugin mirror plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md

Depends on: Task 1

Copy `src/superclaude/core/HOW-WE-WORK.md` over `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` with `cp`. Do not edit the mirror by hand.

Acceptance criteria:
T2.AC1: `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and exits 0.
T2.AC2: `uv run pytest tests/core/test_how_we_work_routing_table.py -q` passes (it reads the guide and the mirror; the `/sc:worktrees` row is unchanged).
Global constraints: ## Constraints

- Test, guide, deck and CLAUDE.md edits only; no production code (nothing under `src/superclaude/cli/`, `scripts/`, hooks or skills changes).
- Never edit or stage anything under `.claude/`. `.dev/tasks/` stays staged.
- ASCII only in the guide section; keep every existing rule that the six answers do not change, in the owner's wording where the source quotes it.
- Decision recorded here: answer 2 says "never stop", so a name whose bare form `<login>/issue-<N>` is over 24 characters is kept and the work goes on. The sentence "create nothing and ask the owner", its key phrase and the "stop" test are replaced. A name that carries words over 24 characters is still an error: drop the words.
- Not in scope (MB-2): reading the digit-run pattern from scripts/worktree_cleanup.py. The user withdrew that item; the hand-copied _NUMBER_RUN of tests/core/test_how_we_work_worktree_policy.py stays as it is.
- The branch `clayphi/issue-289-rest` was created in the reused worktree with `git switch -c` on the owner's order; the guide's "never switch branches in a worktree" line is left as it is.
Start sha: c554091dc16a3ea433df636beb4564a02571a0df
Diff against the start snapshot: --- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -360,9 +360,9 @@
 
 - **New work gets a new worktree and branch.** One writer per worktree; a second writer gets its own. Supervised workers follow `~/.claude/WORKER-CONTRACT.md`.
 - **A fix to delivered work reuses the original worktree while it still exists, after these checks:** same repository, issue and branch; the issue is open (a closed one needs a bug issue `#<M>` named in the fix PR); no other live agent (`orca terminal list`); no uncommitted changes; the PR that counts (`gh pr list --repo <owner>/<repo> --head <branch> --state all`: newest merged, else newest) is merged and none is open. `git fetch origin`, `git merge --ff-only origin/<base>`, check that HEAD moved, and run `orca agent launch`. Any other state (PR closed unmerged, no PR, several worktrees, a worktree missing from `orca worktree list`, anything unknown): stop and ask. A removed worktree means a new one.
-- **Check before `/sc:issue --claim` or a Project Status change.** A claim reuses the worktree it finds and starts its agent at once; the watcher claims by itself. A re-run of the claim's own earlier run (no `launch` entry in its `worktree.json`) is exempt, and so is a handoff of unfinished work after the first session has stopped.
-- **Names:** `<login>/issue-<N>[-<words>]`, at most 24 characters, no spaces; `<login>` is `gh api user --jq .login`. Create with `--name issue-<N>-<words>`; Orca adds the login (use `--branch` if it does not). Words are lowercase letters and digits with no run of 2 to 4 digits (cleanup reads it as an issue). Example: `clayphi/issue-289-wtrule` (24). Drop the words when they do not fit; if even `<login>/issue-<N>` is over 24, create nothing and ask the owner. After creation the agent checks `git branch --show-current` and may run `git branch -m` before any push; never switch branches in a worktree.
-- **Lessons before removal.** The owner pins the worktree when the PR opens. After the merge the owner posts a Lessons comment on the issue (what happened, evidence by PR or commit, action) or "no reusable lesson", runs `/sc:closeout`, then unpins. A person runs `/sc:worktrees archive`, `retire` and `--apply`, and checks that comment first, because cleanup reads none.
+- **Check before `/sc:issue --claim` or a Project Status change.** A claim reuses the worktree it finds and starts its agent at once; the watcher claims by itself. Neither refuses an issue that already has a worktree; the iteration start check asks the owner first. A re-run of the claim's own earlier run (no `launch` entry in its `worktree.json`) is exempt. A handoff of unfinished work after the first session has stopped skips only the already-claimed check: it must still match on repository, issue and branch, because that match proves it is the same work.
+- **Names:** `<login>/issue-<N>[-<words>]`, at most 24 characters, no spaces; `<login>` is `gh api user --jq .login`. Create with `--name issue-<N>-<words>`; Orca adds the login (use `--branch` if it does not). Words are lowercase letters and digits with no run of 2 to 4 digits (cleanup reads it as an issue). Example: `clayphi/issue-289-wtrule` (24). When the words do not fit, drop them and keep `<login>/issue-<N>`; never stop on it, even when that is over 24. A login that has a run of 2 to 4 digits is left out: use `issue-<N>-<words>`. A worktree made by the claim launcher keeps the launcher's `issue-<N>` name. After creation the agent checks `git branch --show-current` and may run `git branch -m` before any push; never switch branches in a worktree.
+- **Lessons before removal.** The owner pins the worktree when the PR opens. After the merge the owner posts a Lessons comment on the issue (what happened, evidence by PR or commit, action) or "no reusable lesson", runs `/sc:closeout`, then unpins. A worktree with no issue keeps its lessons in its own `.dev/` notes; `/sc:worktrees` saves them to the evidence repo before removal (issue 881 covers a worktree with no merged pull request). A person runs `/sc:worktrees archive`, `retire` and `--apply`, and checks that comment first, because cleanup reads none.
 
 ## Orca coordination
 


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