1bcaea8eb93e51e54b433c3439dd20468fb9342e
Review one task for spec compliance.

Task brief: ## Task 15: Register the command in the routing guide and its pinned tests

Depends on: Task 14

Edit `src/superclaude/core/HOW-WE-WORK.md`: add a `/sc:worktrees` row at the end of the table between the `<!-- other-commands:v1 -->` markers (after `/sc:sweep`), stating when to use it (remove merged worktrees whose pull request is merged, issue closed and idle 7 days, `list` by default, `--apply` to remove, saves `.dev` files to the evidence repo first, for a person, never a worker) and carrying the one line that answers item 4 of #289 ("when to remove a worktree after its pull request merges": after the pull request merges and every rule of the cleanup holds). Edit `tests/core/test_how_we_work_routing_table.py`: add `"sc:worktrees"` to `_OTHER_COMMANDS` (line 27). Edit `tests/recommend/test_routing_refresh.py`: add `"worktrees"` to `_POST_REFRESH_ADDITIONS` (line 36), and extend the comment above it with "and issue #687 adds /sc:worktrees". Then copy the whole guide byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; the level-table block between `<!-- level-table:v1 -->` and `<!-- /level-table -->` is unchanged, so `src/superclaude/core/CLAUDE.md` is not edited (confirm the block is identical in both).

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py -v` passes.
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- The new row contains the `#289` item 4 answer and the words "never a worker".

AC ids (in source order): T15.AC1, T15.AC2, T15.AC3
Global constraints: ## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.
- The pull request for this change is opened by the finishing step of the run, `/sc:pr-submit --monitor 3` (source section 15, step 7), after the last task; no task of this plan opens it.
- Corrections the implementer made to this plan before the first task started, from the advisory reflect review of the plan (the list is in `./artifacts/plan-corrections.md`): Task 1 (the item 1 fallback, the open pull request proof, item 7), Task 2 (a positive allowlist runner and its own first tests), Tasks 3 to 5 (their own tests, so no check waits for a later task), Task 7 (shared fixtures only), Tasks 11 and 12 (Orca read back, the command list in the JSON), Task 14 (the write-verb classification), Task 19 (15 rows), Task 20 (dependencies).
Start sha: 1bcaea8eb93e51e54b433c3439dd20468fb9342e
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
index 81a0fe83f..1f1a7c001 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -296,6 +296,7 @@ Additional operations and explicit coordination choices. These entries can be re
 | `/sc:issue` | Claim an existing GitHub issue on the origin repo (`--claim <number or url>`): it assigns the issue to you, checks its accuracy against today's code, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the `--pipeline` level (with no `--pipeline` the level is picked from the issue: `full` for a bug or a simple or medium feature of 16 hours or less, `worktree` for a complex feature, one over 16 hours or one it cannot classify; `full`: implement, with no commit or push; `worktree`: plan, then wait for approval; `--submit` with `full`: also commit, push and open a PR; `none`: no worktree and no agent, you run the steps yourself) and never merges. Create (`--create "<description>"`) files a templated GitHub issue on the origin repo with an issue type, the Complexity field and a mode label. Both post directly to GitHub and write `.dev/issues/`. |
 | `/sc:pm` | Explicit PM coordination with requested strategy/verbosity and available protocol/tools. It can write memory/docs; verify dependencies. Not a default planner, automatic-start guarantee or universal executor-resume method. |
 | `/sc:sweep` | Read-only supervision snapshot of the bound Orca Run, its worktrees and person-started sessions. Writes one dated report under `.dev/sweeps/` and prints JSON; it changes nothing else and recommends nothing. Coordinator or person only, never a worker. |
+| `/sc:worktrees` | Remove git worktrees whose work is finished (`/sc:worktrees list`, `archive`, `retire` or `prune`): a worktree goes only when its own pull request is merged, nothing was added after it, its issues are closed, nothing unsaved is in it and it has been idle for 7 days. Every verb is a dry run that lists each worktree with its reason; `--apply` removes, and the `.dev` files are first saved to the evidence repo. When to remove a worktree after its pull request merges (item 4 of issue 289): after the pull request merges and every rule of the cleanup holds. For a person, never a worker. |
 
 One more user-facing skill: `/confidence-check` checks readiness before implementation. Supporting command protocols are loaded through their command's actual activation directive; do not infer a protocol name from a filename. Self-contained commands are valid. Verify required agents, templates and tools before promising execution.
 
diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index 81a0fe83f..1f1a7c001 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -296,6 +296,7 @@ Additional operations and explicit coordination choices. These entries can be re
 | `/sc:issue` | Claim an existing GitHub issue on the origin repo (`--claim <number or url>`): it assigns the issue to you, checks its accuracy against today's code, writes a summary and a next-step prompt, then creates an Orca worktree and launches an agent in it at the `--pipeline` level (with no `--pipeline` the level is picked from the issue: `full` for a bug or a simple or medium feature of 16 hours or less, `worktree` for a complex feature, one over 16 hours or one it cannot classify; `full`: implement, with no commit or push; `worktree`: plan, then wait for approval; `--submit` with `full`: also commit, push and open a PR; `none`: no worktree and no agent, you run the steps yourself) and never merges. Create (`--create "<description>"`) files a templated GitHub issue on the origin repo with an issue type, the Complexity field and a mode label. Both post directly to GitHub and write `.dev/issues/`. |
 | `/sc:pm` | Explicit PM coordination with requested strategy/verbosity and available protocol/tools. It can write memory/docs; verify dependencies. Not a default planner, automatic-start guarantee or universal executor-resume method. |
 | `/sc:sweep` | Read-only supervision snapshot of the bound Orca Run, its worktrees and person-started sessions. Writes one dated report under `.dev/sweeps/` and prints JSON; it changes nothing else and recommends nothing. Coordinator or person only, never a worker. |
+| `/sc:worktrees` | Remove git worktrees whose work is finished (`/sc:worktrees list`, `archive`, `retire` or `prune`): a worktree goes only when its own pull request is merged, nothing was added after it, its issues are closed, nothing unsaved is in it and it has been idle for 7 days. Every verb is a dry run that lists each worktree with its reason; `--apply` removes, and the `.dev` files are first saved to the evidence repo. When to remove a worktree after its pull request merges (item 4 of issue 289): after the pull request merges and every rule of the cleanup holds. For a person, never a worker. |
 
 One more user-facing skill: `/confidence-check` checks readiness before implementation. Supporting command protocols are loaded through their command's actual activation directive; do not infer a protocol name from a filename. Self-contained commands are valid. Verify required agents, templates and tools before promising execution.
 
diff --git a/tests/core/test_how_we_work_routing_table.py b/tests/core/test_how_we_work_routing_table.py
index 5efce8e5f..bb658281c 100644
--- a/tests/core/test_how_we_work_routing_table.py
+++ b/tests/core/test_how_we_work_routing_table.py
@@ -31,6 +31,7 @@ _OTHER_COMMANDS = {
     "sc:impact",
     "sc:issue",
     "sc:sweep",
+    "sc:worktrees",
     "sc:agent",
     "sc:pm",
 }
diff --git a/tests/recommend/test_routing_refresh.py b/tests/recommend/test_routing_refresh.py
index b1726d500..5c499bb25 100644
--- a/tests/recommend/test_routing_refresh.py
+++ b/tests/recommend/test_routing_refresh.py
@@ -31,9 +31,10 @@ _SKILLS = _REPO / "src/superclaude/skills"
 _PACKAGE = "TASK-RESEARCH-recommend-refresh-20261024-044336"
 # Commands shipped after the frozen routing-refresh research package was written:
 # issue #323 (codegraph adoption, Phase 3) adds /sc:graph and /sc:impact, and
-# issue #302 adds /sc:issue, and issue #668 adds /sc:closeout. The package is
-# frozen, so the shipped set is compared minus these additions.
-_POST_REFRESH_ADDITIONS = {"closeout", "graph", "impact", "issue", "sweep"}
+# issue #302 adds /sc:issue, issue #668 adds /sc:closeout and issue #687 adds
+# /sc:worktrees. The package is frozen, so the shipped set is compared minus these
+# additions.
+_POST_REFRESH_ADDITIONS = {"closeout", "graph", "impact", "issue", "sweep", "worktrees"}
 # Commands removed after the frozen package was written: /sc:spawn (replaced by
 # Orca), build, save, load, improve, cli-portify, index, index-repo and
 # review-translation (moved to the snapshot fork) went in 6.0.0, as did the roadmap,


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

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
