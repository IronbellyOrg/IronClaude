3620bd561d2e471cd4bdc7c8f7092371b55ab4a3
Review one task for spec compliance.

Task brief: ## Task 16: Put `/sc:worktrees` on the never-as-worker list

Depends on: Task 14

Decision made by this plan: the command closes terminals and removes work, so no worker is ever dispatched to it. Edit the never-as-worker sentence so it reads "... `/sc:pm`, `/sc:sweep`, `/sc:swarm-wizard` and `/sc:worktrees`, plus `/sc:pr-submit` ..." in `src/superclaude/core/WORKER-CONTRACT.md` (line 23) and in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (line 982), and make the same change to the pinned phrase in `tests/skills/test_worker_contract.py` (the `never-as-worker` entry at line 89, which today ends "`/sc:sweep` and " followed by "`/sc:swarm-wizard`...") and add `"/sc:worktrees"` to the `NEVER_AS_WORKER` tuple at line 474. Read `src/superclaude/core/WORKER-CONTRACT.md` line 290 and the other mentions of the list in the developer guide and update any that enumerate the commands. `/sc:worktrees` gets no `## Unattended mode` section (the test `_check_no_unattended_sections` at line 830 requires only the named commands to have one).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -v` passes, including the parametrized never-as-worker check for `/sc:worktrees`.
- The sentence is identical in `WORKER-CONTRACT.md`, the developer guide and the pinned phrase of the test, and `src/superclaude/commands/worktrees.md` has no `## Unattended mode` heading.
- `make sync-dev` and `make verify-sync` are clean.

AC ids (in source order): T16.AC1, T16.AC2, T16.AC3
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
Start sha: 3620bd561d2e471cd4bdc7c8f7092371b55ab4a3
Diff against the start snapshot: diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index d3c73ef59..8cf91527f 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -979,7 +979,7 @@ Orca can run IronClaude commands as workers under an Orca coordinator (the `/orc
 
 #### Deciding whether a new command can be a worker
 
-- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. These commands are never dispatched as workers and get no `--unattended` mode.
+- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:sweep`, `/sc:swarm-wizard` and `/sc:worktrees`, plus `/sc:pr-submit` while decision D3 keeps it off workers. These commands are never dispatched as workers and get no `--unattended` mode.
 - Per the rollout plan, these are commands whose purpose is orchestration, a conversation with a human, or an outward action that must be authorized, so making them workers would remove their purpose.
 - Adding a command to the list is a maintainer edit of `src/superclaude/core/WORKER-CONTRACT.md` and of `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py`.
 - Any other command gets `--unattended` only after each of its gates has an unattended resolution (WC-2).
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index dfaac01c4..b756e4f09 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -20,7 +20,7 @@ The dispatch preamble that Orca gives each worker is the authority for Orca verb
   - (case 3) the command is on the never-as-worker list; the body still starts `guard refused:`.
 
   A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer. A refusal is report-only: the worker never installs or refreshes a command copy and never rewrites its own brief; the coordinator repairs the cause and creates a new Task (WC-6).
-- **Never-as-worker list**: `/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
+- **Never-as-worker list**: `/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:sweep`, `/sc:swarm-wizard` and `/sc:worktrees`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
 - **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.
   Reading a nested result: when the nested worker contract says `blocked`, the caller stops at that step and writes its own contract with `worker_status: blocked`, `blocked_question` set to the nested question prefixed with the nested command's name, and the nested contract in `artifacts`; when it says `failed`, or no nested contract exists, the caller takes its own documented failure path for that step (fallback, skip and record, or stop), and if that ends the run it writes `worker_status: failed` with the nested command and its reason in `reason`; `succeeded` and `partial` count as the step completing.
 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index c679a6e34..c13975027 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -86,8 +86,8 @@ RULE_PHRASES = {
     "never-as-worker": (
         "**Never-as-worker list**",
         [
-            "`/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:sweep` and "
-            "`/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers"
+            "`/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:sweep`, "
+            "`/sc:swarm-wizard` and `/sc:worktrees`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers"
         ],
     ),
     "nested-propagation": (
@@ -481,6 +481,7 @@ NEVER_AS_WORKER = (
     "/sc:swarm-wizard",
     "/sc:pr-submit",
     "/sc:sweep",
+    "/sc:worktrees",
 )
 
 # The thirteen commands that get an `## Unattended mode` section in P1, in the order


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
