1eac25cba4c1709db67f80cfbb322ac36e9d3c5c
Review one task for spec compliance.

Task brief: ## Task 17: Document the command in the user guide and the changelog

Depends on: Task 14

Edit `docs/user-guide/commands.md`: add a summary-table row for `/sc:worktrees` next to the `/sc:closeout` and `/sc:sweep` rows (near line 103, columns as the neighbouring rows: link, one-line purpose, file `worktrees.md`, whether it writes: "Yes with `--apply` (removes worktrees, closes their Orca terminals, writes to the evidence repo); report only without it") and a section `### /sc:worktrees - Remove Merged Worktrees` modelled on the `/sc:closeout` section (near line 373): when to use, usage line, options table (`list`, `archive`, `retire`, `prune`, `--apply`, `--out`), the eight rules in plain English, what a removal does in order, the environment names (`GH_TOKEN`, `RUN_EVIDENCE_REPO`, `RUN_EVIDENCE_DIR`, `WORKTREE_CLEANUP_IDLE_DAYS`; no values), exit codes 0, 64 and 69, the opt-in daily automation (definition only, switched off, first week report only), and the stop outside an IronClaude checkout. Edit `CHANGELOG.md` under `## [Unreleased]`: add `### New command: /sc:worktrees and scripts/worktree_cleanup.py (issue 687)` with a short plain-English entry that also names Jay Wedgeworth's adapted rules under Apache-2.0 and the evidence repo, and states that the Orca automation is written but not switched on.

Acceptance criteria:
- The new table row and section exist in `docs/user-guide/commands.md` and the anchor in the row matches the section heading.
- The `CHANGELOG.md` entry sits under `## [Unreleased]` and mentions the switched-off automation, the Apache-2.0 notice and the evidence repo by name.
- No em or en dash in either added text; `uv run pytest tests -k "docs or commands" -q` shows no new failure from these files.

AC ids (in source order): T17.AC1, T17.AC2, T17.AC3
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
Start sha: 1eac25cba4c1709db67f80cfbb322ac36e9d3c5c
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index e6eed1d27..79bab2735 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -4,6 +4,10 @@ All notable changes to IronClaude are documented in this file.
 
 ## [Unreleased]
 
+### New command: /sc:worktrees and scripts/worktree_cleanup.py (issue 687)
+
+- `/sc:worktrees <list|archive|retire|prune>` removes git worktrees of our repos once their work is finished. A worktree goes only when its own pull request is merged, nothing was added after it, its issues are closed, nothing unsaved is in it, nothing but its own Orca terminals is using it, it has been idle for 7 days and it is not pinned. Every verb is a dry run unless `--apply` is typed. Before a removal, the untracked and ignored `.dev/` files are saved to the evidence repo `IronbellyOrg/run-evidence` and checked against GitHub; if anything cannot be read or saved, the worktree is kept and the reason is shown. The script is `scripts/worktree_cleanup.py` (Python standard library only), and the command is on the never-as-worker list. The removal rules are adapted from files of Jay Wedgeworth's AI-Fleet-Coordinator under Apache-2.0; see `scripts/worktree_cleanup_PROVENANCE.md` and `NOTICE`. A definition for a daily Orca automation is in `scripts/worktree_cleanup_orca_automation.md`; it is written and not switched on.
+
 ### worker contract: two gaps left after #700 (follows #697)
 
 - The worker-session duties again say that `ask` and `send` carry no `--to`. WC-17 step 4 now passes `--issue <N>` to `check-approval`, so an approval for another issue with the same plan hash is refused. The "Worktree, then worker" duty now says the worker started right after the claim script is that worktree's agent.
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index 8a722f9b0..a59f91604 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -102,6 +102,7 @@ This page is the per-command reference: exact syntax, options, and what each com
 | [`/sc:issue`](#scissue---github-issue-claim-and-create) | Claim a GitHub issue (assign, accuracy check, summary, next-step prompt, then an Orca worktree and a launched agent) or create a templated issue | `issue.md` | Yes (posts to GitHub; writes `.dev/issues/`) |
 | [`/sc:closeout`](#sccloseout---settle-a-merged-pull-request) | Settle a merged pull request: decide whether its issue is done, then settle the work report entry and the worker's Orca task | `closeout.md` | Yes (posts to GitHub: one note, then one close or one not-done note; updates the entry and the task) |
 | [`/sc:sweep`](#scsweep---read-only-run-worktree-and-session-report) | Read-only snapshot of a Run, its worktrees and person sessions | `sweep.md` | Report only (writes `.dev/sweeps/`) |
+| [`/sc:worktrees`](#scworktrees---remove-merged-worktrees) | List the git worktrees of our repos with the reason each is kept or removable, and remove the ones whose work is finished | `worktrees.md` | Yes with `--apply` (removes worktrees, closes their Orca terminals, writes to the evidence repo); report only without it |
 | `/sc:recommend` | Paste-ready prompt for the right command | `recommend.md` | Report only (inside an IronClaude checkout it writes its cache and telemetry under `.claude/cache/`) |
 | `/sc:init-lite` | Safe audit of project-local context surfaces | `init-lite.md` | Report only |
 | `/sc:pr-submit` | Open fork PR and monitor review fixes | `pr-submit.md` | Yes |
@@ -629,6 +630,62 @@ Full option list: `~/.claude/commands/sc/release-split.md`.
 
 ---
 
+### `/sc:worktrees` - Remove Merged Worktrees
+
+**When to use:** Git worktrees pile up after their pull requests merge. This command lists every worktree of our repos with the reason it is kept or removable, saves the untracked and ignored `.dev/` files of a finished worktree to the evidence repo, and removes the worktrees whose work is safe. Every verb is a dry run unless you type `--apply`. Use it after a pull request merges; the answer to "when do I remove a worktree after its pull request merges" is: after the pull request merges and every rule below holds.
+
+**Syntax:**
+
+```
+/sc:worktrees <list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]
+```
+
+**Options:**
+
+| Argument | What it does |
+|----------|--------------|
+| `list` | Prints the table of every worktree of every repo of ours, with its decision and reason. Removes nothing |
+| `archive <worktree>` | Runs only the save step for one worktree and prints `VERIFIED` when the saved copy matches GitHub. Removes nothing. Saving tracked edits or later commits as a patch and a bundle is not built; such a worktree is kept |
+| `retire <worktree>` | Removes one worktree whose work is safe. Run it from outside that worktree. It takes a path or a unique folder name |
+| `prune` | Applies the same decision to every worktree. Without `--apply` it prints the table and writes `prune-<UTC stamp>.md` and `.json` under `--out`; with `--apply` it removes the removable ones |
+| `--apply` | Actually removes. Without it nothing is removed, closed or cleared |
+| `--out <dir>` | The folder for the table files and the per-repo lock files. Never inside a worktree. Default `~/.local/state/worktree-cleanup` |
+
+**The eight rules.** A worktree is removed only when all of these hold, and the first one that fails is the reason shown: (1) it is a linked worktree of one of our repos, not the main checkout, not the folder you run in, not locked and not detached; (2) its own pull request is merged, judged from the pull request and not from commit ancestry; (3) nothing was added after that pull request; (4) every issue it relates to is closed; (5) nothing unsaved is in it, which means no changed tracked file, no untracked file outside `.dev/` and no ignored file that is not build output; (6) nothing but its own Orca terminals is using it; (7) it has been idle for the idle floor (7 days) and is not new; (8) it is not pinned in Orca and has no keep file. Anything the command cannot read counts as a reason to keep the worktree.
+
+**What a removal does, in order:**
+
+1. Saves the untracked and ignored `.dev/` files to the evidence repo, checks the saved copy against GitHub and prints `VERIFIED`.
+2. Closes the worktree's Orca terminals, only after every rule passed and the save was verified.
+3. Checks the worktree again; a change or a process still inside keeps it.
+4. Clears exactly the saved files, and nothing else.
+5. Removes the worktree without force, removes its local branch with the safe form of the branch delete (a branch that git says is not fully merged, as after a squash merge, is reported as kept), and reads the result back.
+
+A failure at any step keeps the worktree and shows the cause.
+
+**Environment** (names only; the command never prints a value): `GH_TOKEN` (GitHub access for the checks and the evidence push), `RUN_EVIDENCE_REPO` (the evidence repo, default `IronbellyOrg/run-evidence`), `RUN_EVIDENCE_DIR` (the local clone of it) and `WORKTREE_CLEANUP_IDLE_DAYS` (the idle floor, default 7).
+
+**Exit codes:** `0` the run completed; `64` a usage error, or a `retire` of a worktree that is not removable; `69` a lookup or a removal failed (the table still shows what happened).
+
+**The daily automation:** `scripts/worktree_cleanup_orca_automation.md` holds the definition of an Orca automation that would run the cleanup once a day. It is written and not switched on. When it is switched on, its first week should report only. Nothing here creates or runs it.
+
+**Stops outside a checkout:** the command runs only inside an IronClaude checkout that has `scripts/worktree_cleanup.py`; anywhere else it prints that and runs nothing.
+
+**Who may run it:** a person only. It closes terminals and removes work, so it is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`.
+
+**Examples:**
+
+```bash
+/sc:worktrees list
+/sc:worktrees archive issue-687
+/sc:worktrees retire issue-687 --apply
+/sc:worktrees prune --out ~/worktree-reports
+```
+
+**MCP servers:** none
+
+---
+
 ### `/sc:task` - Enhanced Task Management
 
 **When to use:** A small, direct change: one source file plus its test, five edits or fewer, and you know exactly what it should be (level 2 in [How We Work](how-we-work.md)). Work that touches more than one source file or needs more than five edits needs a written plan (`/sc:workflow`, level 3).


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
