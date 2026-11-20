9ecf576acf312a4ede8ecfc080b396ec22fc239e
Review one task for spec compliance.

Task brief: ## Task 19: Write the provenance file, the NOTICE entry and the evidence-repo pointer text

Depends on: Task 12

Create `scripts/worktree_cleanup_PROVENANCE.md`, modelled on `src/superclaude/skills/sc-closeout-protocol/PROVENANCE.md` (sections: Source, Notices in the adopted files, What changed, What this version adds, Drift review). Its "What changed" table has one row for each of the 15 rows of the table in source section 12 (lines 314 to 328 of `source.md`; where the spec's own word is not one of the three words, for example replaced, reused, not adopted or adopted in spirit, the row keeps the spec's word beside the closest of the three) (kept as is, changed or dropped, with the spec's reason). The source table lists `scripts/fleet_lanes/retire.py`, `docs/protocols/lane-map.md` and `scripts/disk-janitor.sh` with line counts from source section 12 and writes "not recorded" for blob and commit pins, because the spec records none and no pin may be invented; `branch-landed.sh` is listed as reused through `/sc:closeout`, not adopted again. It says the Apache License text is at `src/superclaude/skills/sc-closeout-protocol/LICENSE` and the upstream repository has no NOTICE file. Edit `NOTICE` (it lists `sc-closeout-protocol` as component 2 near line 30) to add the next numbered component for `scripts/worktree_cleanup.py`, naming Jay Wedgeworth, the three files whose rules were adapted, Apache-2.0 and the provenance file. Write `./artifacts/run-evidence-pointer.md` in this package with the proposed text for `tools/archive-workspace.sh` (a short pointer to `scripts/worktree_cleanup.py archive`) and the `README.md` note for `IronbellyOrg/run-evidence`, headed "not applied: a separate change in that repo, made by the owner when this merges".

Acceptance criteria:
- `scripts/worktree_cleanup_PROVENANCE.md` has 15 rows in its changed-table, each labelled with one of the three words, and no invented commit or blob pin.
- `NOTICE` has the new component entry and still lists components 1 and 2 unchanged.
- `./artifacts/run-evidence-pointer.md` exists and states it was not applied; no file of the evidence repo was changed or pushed.
- The notice block at the top of `scripts/worktree_cleanup.py` (Task 2) points at the file name used here.

AC ids (in source order): T19.AC1, T19.AC2, T19.AC3, T19.AC4
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
Start sha: 9ecf576acf312a4ede8ecfc080b396ec22fc239e
Diff against the start snapshot: diff --git a/NOTICE b/NOTICE
index 71f223fbc..c5beff783 100644
--- a/NOTICE
+++ b/NOTICE
@@ -41,4 +41,19 @@ Third-party components
    source commits, the content hashes and the changes made. The upstream
    repository has no NOTICE file, so there is no further notice to carry.
 
+3. worktree_cleanup (adapted rules)
+   ------------------------------
+   Upstream:  https://github.com/Simple-With-Us/AI-Fleet-Coordinator
+   License:   Apache License, Version 2.0 (Apache-2.0)
+   Location:  scripts/worktree_cleanup.py
+
+   The worktree cleanup script adapts rules from three files written by Jay
+   Wedgeworth (Copyright 2026 Jay Wedgeworth): `scripts/fleet_lanes/retire.py`,
+   `docs/protocols/lane-map.md` and `scripts/disk-janitor.sh`. The Apache License
+   text is kept verbatim at
+   `src/superclaude/skills/sc-closeout-protocol/LICENSE`, and
+   `scripts/worktree_cleanup_PROVENANCE.md` records what was kept, changed or
+   dropped for each rule. The upstream repository has no NOTICE file, so there
+   is no further notice to carry.
+
 ==============================================================================


===== new file: scripts/worktree_cleanup_PROVENANCE.md =====
# worktree_cleanup.py: Provenance of the adapted rules

`scripts/worktree_cleanup.py` adapts rules from three files written by Jay Wedgeworth, used with the owner's approval. This file records the source, the licence, and what was kept, changed or dropped for each rule. The script is rewritten for git worktrees of IronbellyOrg repos; no line of his code is copied as it stands, and the rules are adapted. The root `NOTICE` lists the component.

## Source

| Field | Value |
|---|---|
| Upstream repository | https://github.com/Simple-With-Us/AI-Fleet-Coordinator |
| Author and copyright | Jay Wedgeworth, Copyright 2026 Jay Wedgeworth |
| Licence | Apache License, Version 2.0 (Apache-2.0); the licence text is kept verbatim at `src/superclaude/skills/sc-closeout-protocol/LICENSE` |
| Upstream NOTICE file | none (the upstream repository has no `NOTICE` file, so there is nothing to carry under section 4(d) of the licence) |
| Date read | 2026-11-20, in full; none of it was run |
| Fetched automatically later | never; a drift review compares the files by hand |

| Upstream file | Lines | Git blob | Last commit | Where it went |
|---|---|---|---|---|
| `scripts/fleet_lanes/retire.py` | 1,923 | not recorded | not recorded | the rules and the removal order of `scripts/worktree_cleanup.py` |
| `docs/protocols/lane-map.md` | 300 | not recorded | not recorded | the "Cleaners" contract: `list` is the doctor and `prune` runs the same decision |
| `scripts/disk-janitor.sh` | 1,161 | not recorded | not recorded | the idle floor of 7 days, the run lock, the dry run default and the check for a checkout inside a worktree |
| `scripts/branch-landed.sh` | 85 | not recorded | not recorded | not adopted again: it is reused through `/sc:closeout` (its provenance is in `src/superclaude/skills/sc-closeout-protocol/PROVENANCE.md`) |

The specification records no blob or commit pin for any of these files, so none is written here and none is invented. A search of the three code files for model or inference calls found none.

## Notice in the adapted file

`scripts/worktree_cleanup.py` carries a comment block after the shebang that names the three source files, Jay Wedgeworth's copyright, the Apache License, Version 2.0, a line saying what IronClaude changed, and a pointer to this file.

## What changed

The label is one of three words. `kept as is` means the idea or logic carries over unchanged. `changed` means only the part this setup needs is different, or the text itself changed. `dropped` means it names a surface this setup does not have or a step the issue does not ask for. When the specification used a different word, the row says it after the label.

| # | Upstream rule or piece | Label | What happens here, and why |
|---|---|---|---|
| 1 | `retire.py`: linked worktree under the lanes root, never the integration tree | changed | Rule 1. Our worktrees sit in several places, so any linked worktree of our repos qualifies, never a main checkout. |
| 2 | `retire.py`: the lane belongs to the chosen seat (folder name and `lane.json`) | dropped | Each Coder workspace runs its own automation and sees only its own worktrees. |
| 3 | `retire.py`: not locked, no process with its folder inside, no git operation in progress, no `.janitor-keep` | changed (the specification says adopted) | Rules 6 and 8. It reads `/proc/<pid>/cwd` because `lsof` is not installed here; the worktree's own Orca terminals no longer keep it, they are closed first and everything is checked again; the keep file is `.worktree-keep`. Added from the janitor: a worktree that holds another checkout is never removed. |
| 4 | `retire.py`: `git status` clean, and no git-ignored local state | changed (the specification says adopted) | Rule 5. Files under `.dev/` are allowed after the archive step. |
| 5 | `retire.py`: nothing unpushed (HEAD on a branch that exists on the remote, or in the default branch, or held by a pull request) | changed | Rule 3. HEAD equals the merged pull request's last commit or is behind it. GitHub keeps that commit, so a squash merge or a deleted branch does not matter. Stricter than his: no "in the default branch" shortcut. |
| 6 | `retire.py`: the work is done (pull request merged or closed, or merged into the default branch, or the upstream was deleted, or a tree or byte-identical proof, or local evidence) | changed | Rule 2. Only a merged pull request counts, judged through the landed check. The tree and byte-identical proofs, closed counting as done and the local-evidence fallback are dropped in version 1. |
| 7 | `retire.py`: review checkouts `review-pr-<n>` are done when the pull request is merged or closed | dropped | We have no such naming. |
| 8 | `retire.py prune`: kept if active in the last 15 minutes; a lane made and never used is kept 24 hours | changed (the specification says replaced) | Rule 7. Seven days idle, which is the janitor's value, because this job runs unattended for many people. The number is a setting. |
| 9 | `retire.py`: remove under a per-repo lock, check again, `git worktree remove` without force, then `git branch -d` (never the forced form) | changed (the specification says adopted) | The same order, with the Orca removal for worktrees Orca lists. A branch that git says is not fully merged, as after a squash merge, is reported as kept. `git worktree prune` is never run (a missing folder is only reported). |
| 10 | `retire.py`: a runner that only allows a fixed list of commands (`check_allowed`) | changed (the specification says adopted) | The idea is kept. The script runs commands only through one runner with a positive allowlist of exact argument shapes, and a test records every command. |
| 11 | `retire.py`: dry run is the default; exit codes 0, 64, 69 | kept as is | The same default and the same three exit codes. |
| 12 | `branch-landed.sh` | kept as is (the specification says reused through `/sc:closeout`) | Not adopted a second time: the landed check is the one installed with `/sc:closeout`, and its own provenance file says what was changed there. |
| 13 | `lane-map.md`, "Cleaners": act only on the doctor's candidate list; `git worktree remove`, never `rm -rf`; never create a keep file as protection | kept as is (the specification says adopted) | `list` is the doctor and `prune` runs the same decision code in the same run, so it never acts on a stale report. |
| 14 | `disk-janitor.sh`: every 30 minutes, only when disk is low, with a pressure gate on load and swap | dropped (the specification says not adopted) | He runs often because his disk was nearly full; ours has plenty of space, so the job is daily and light, with no disk gate and no pressure gate in version 1. |
| 15 | `disk-janitor.sh`: the `REAP_WORKTREES` master switch, a dry run switch, a run lock with a heartbeat | changed (the specification says adopted in spirit) | Dry run by default, a per-repo lock, and the automation itself is the master switch (off until a person switches it on). |

Jay's other cleanup pieces (the dependency reaper, "delete branch on merge" as a repository setting, a low-disk trigger, main-checkout sync, the placement watcher and orphan process cleanup) are not part of version 1 and are not specified here.

## What this version adds

Only what the issue asks for: the archive step that saves untracked and ignored `.dev/` files to the evidence repo `IronbellyOrg/run-evidence`, the table and its two output files, the `/sc:worktrees` command, the tests, and a definition of a daily automation that is written and not switched on.

## Drift review

Nothing is fetched automatically. To review drift, read the three upstream files and compare them with the rows above. A later pin would be added to the source table in the same change that updates the script.


===== new file: .dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/run-evidence-pointer.md =====
# Proposed text for the IronbellyOrg/run-evidence repo

**Not applied: a separate change in that repo, made by the owner when this merges.** Nothing in this file has been written to the evidence repo, and no file of that repo was changed or pushed by this plan.

## 1. A pointer in `tools/archive-workspace.sh`

Add this comment near the top of the script, under its existing description:

```text
# To save the untracked and ignored .dev/ files of one finished worktree, use the
# archive step of the worktree cleanup in the IronClaude repo instead of copying by
# hand:
#   uv run --no-project python scripts/worktree_cleanup.py archive <worktree>
# It saves the files into this repo under <repo>/<author>/<date>_pr<N>_<subject>/,
# checks the saved copy against GitHub and prints VERIFIED. It removes nothing.
```

## 2. A note for `README.md`

Add this section to the README of the evidence repo:

```text
## Saves made by the worktree cleanup

The worktree cleanup in the IronClaude repo (`scripts/worktree_cleanup.py`, run through
`/sc:worktrees`) saves the untracked and ignored `.dev/` files of a finished worktree
here before it removes the worktree. Each save is one folder,
`<repo>/<author>/<date>_pr<N>_<subject>/`, with a `MANIFEST.md`, a `files/` folder, an
`ignored.tar.gz` (split into parts when it is large) and a `saved-paths.txt` that lists
exactly the paths that were saved. A folder is never overwritten: a repeat run verifies
it, and new files go to a folder with the suffix `-r2` or `-r3`. A possible secret in a
file stops the save and names the file; the value is never printed.
```

## What the owner does

When the pull request for issue 687 merges, the owner of the evidence repo makes these two edits there as one change. Until then the cleanup works without them.


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
