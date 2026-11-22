# Reviewer 2 brief (persona: qa; model class: haiku)

## T1 card excerpt

# Tier 1 reflection card (UC-1, pre-execution)

hypothesis_source: inline-fallback (the orchestrator wrote this card; the plan author is also the executor class, so this card is the part most exposed to self-confirmation and is the reason Tier 2 follows)

Spec: ./source.md (snapshot of the issue 687 spec, 381 lines). Tasklist: TASK-WF-specWorktreeClea-20261120-173546.md (20 tasks, 8 phases, depth deep).

## Coverage

- Pass 1 (labeled IDs by `ID_REGEX`): 0 parsed requirements. The spec labels nothing as R-n, REQ-n, SPEC-n or T-n.
- Pass 2 (quote-pinned inference): 82 inferred rows (`coverage-matrix.md`). Every quote was checked verbatim against its cited line by `artifacts/coverage_match.py`.
- Containment match (threshold 0.6, deterministic): 74 of 82 matched, `coverage_pct_union` 0.9024, `coverage_pct` null (parsed-only is undefined), `S_dev_density` 0.0976.
- Unmapped by the lexical rule: INF-026 (command, not a skill), INF-028 (precheck exits non-zero), INF-035 (first week report only), INF-042 (rule 5 "nothing unsaved"), INF-045 (rule 8 not pinned), INF-048 (never `git worktree prune`), INF-058 (never overwrite a folder), INF-079 (registered where the repo lists commands). The orchestrator believes each is covered in substance (Tasks 14, 18, 18, 6, 6, 2, 9, 15) but the rule is lexical and this belief is unchecked by anyone else.

## Structural signals

- S_scope 20 tasks, S_domains 5 (code, tests, docs, config, infra-like automation), S_dev_density 0.0976.
- Step 1B.2b fired: `inferred_count` 82 is greater than `parsed_count` 0, so `coverage_degraded: parsed-sparse` forbids the Tier 1 stop. Tier 2 is routed by the table-wide pre-filter and by rule 4 (S_domains at least 3).

## Self-identified risks (the orchestrator's own doubts about its plan)

- R1 Order and dependencies. Task 5 (GitHub facts) needs the Orca record from Task 3 and the git record from Task 4; Task 7 (test support) is placed after Task 6 although the fixtures it builds are used by Tasks 3 to 5 only in their acceptance criteria. A reviewer should check that no task's acceptance criteria depend on something a later task creates.
- R2 Scaffolding. Task 2 tells the executor to leave the four verb bodies as stubs that exit 64 until Tasks 11 and 12. The plan says nothing ships as a stub; check that Task 12 really replaces every stub and that its acceptance criteria prove it.
- R3 Safety. The user's run-level safety rule forbids any real removal, any real automation and any push to the evidence repo. Task 1 runs `branch-landed.sh` (which runs `git fetch`) on a real repository and Task 20 runs the script against the real workspace (which runs the same check per worktree through `gh` and `git fetch`). Check whether those are consistent with "dry run only" and with the Constraints section.
- R4 Unbuilt requirement. The spec says `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" with no format. The plan records it as not built (Constraints, Task 12). Check this is an honest reading and not a silent drop.
- R5 Decisions made by the plan where the spec is silent: `/sc:worktrees` on the never-as-worker list (Task 16), the stop outside an IronClaude checkout (Task 14), the default `--out` folder, `/sc:closeout` untouched, the run-evidence pointer prepared as text only (Task 19). Check each for a hidden conflict with a spec section or a pinned test.
- R6 The "never delete a file" constraint (no `unlink`, no `rmtree`, flock lock files left in place, failed scratch folders left in the evidence clone). Check it does not make a spec requirement impossible (for example the archive step 2 "build the folder in a scratch folder" and step 7 repeat runs).
- R7 Test count. The spec asks for about 35 cases in four groups; the plan spreads them over Tasks 7, 8, 10, 13, 18. Check that every bullet of source section 9 lands in some task's body or acceptance criteria.
- R8 Hand-written fixtures for `orca` replies (Task 7) may not match the real Orca output; the only real check is the dry run in Task 20.

## Recommendation

Hand the plan to `/sc:implement` only after a reviewer has confirmed R1, R3 and R7. No change to the plan has been made from this card.

calibration: pending (blind calibration runs in Wave 1D)

Persona lens (qa): coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check that every plan task has acceptance criteria that an executor could actually verify, and that every bullet of spec section 9 (lines 242 to 276) lands in some task.

Instructions for this reviewer (read-only: do not run commands, do not edit any file; audit the evidence in this brief and what you can Read, Grep or Glob). You are reviewing a PLAN (the tasklist) against its SPEC before anyone implements it. Find concrete defects: a spec requirement the plan drops or contradicts, a task whose acceptance criteria cannot be met or depend on something a later task creates, a task that would make an executor break the constraints, a wrong repo fact (file, line, symbol, test name) that you can check with Read/Grep, or a safety problem. Grade each finding: BLOCKING only if correcting it would change a named decision, required behaviour, outcome or acceptance check the plan rests on, or a required deliverable is absent, or following the plan would lose or expose data, break a safety boundary or act outside the stated scope; MEDIUM if it is a real weakness nothing named rests on; NOTE if it is wording or form only. Every finding needs file:line evidence with a short verbatim quote, the consequence, and a suggested fix. A zero-finding result is valid only if you state what you checked. Do not invent findings. Return ONE card as plain markdown with: a `verdict:` line (PASS or FAIL; FAIL only with at least one BLOCKING finding), `self_reported_confidence:` (0.00 to 1.00), `reviewer_model_self_report:` (the model you run as), then `## Findings` (numbered F1, F2 ... each with severity, claim, evidence, consequence, fix), `## Checked and found sound` (bullets with what you verified), `## Coverage gaps` (spec requirements you think the plan misses, with source.md line). Plain English, no em or en dashes.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-20T17:38:06Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687

### .dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/source.md:1-381

````` markdown
# Spec: daily cleanup of merged worktrees, with a saved copy of their workflow files

| Field | Value |
|---|---|
| Issue | IronbellyOrg/IronClaude #687 |
| Status | All 11 decisions answered by Clay on 2026-11-20 and recorded in section 8 as DECIDED. Nothing is built, installed or switched on. |
| Date | 2026-11-20 (written 02:30 UTC; Clay's answers and the orchestrator rollback recorded 17:30 UTC) |
| Repo that owns it | IronbellyOrg/IronClaude (base branch `master`) |
| Replaces | The preliminary spec in the body of #687 (sections 1 to 12). Where they differ, this spec wins; the differences are listed in section 13. |
| Facts | Read-only checks on 2026-11-20 against git, GitHub and Orca. Each statement is either a fact with its source, or marked UNVERIFIED. Nothing was removed, changed, committed or pushed to produce them. The worktree counts in sections 0 and 2 were taken at about 02:30 UTC and not repeated; the state of `origin/master` and of the pull requests named in section 1 was re-checked at 17:20 UTC. |

## 0. Summary in plain English

A script removes git worktrees of our own repos once their work is finished, and nothing else. "Finished" means all of these: the worktree's own pull request is merged, nothing was added after it, the issue it was for is closed, nothing but its own Orca terminals is using it, and it has been idle for 7 days. Before a worktree that holds untracked or ignored workflow files under `.dev/` is removed, those files are copied to a private evidence repo (`IronbellyOrg/run-evidence`) and checked byte for byte against GitHub. If that check fails, the worktree stays. After the check passes, the script closes the worktree's Orca terminals, clears exactly the saved files, and removes the worktree.

It runs by hand through a thin command, and once a day (2:00 AM Central, 08:00 UTC) through an opt-in scheduled Orca automation in each Coder workspace that starts no agent. The first week it only writes a table. It never uses `--force` on a worktree removal, never `git branch -D`, never `rm`, never pushes to a source repo and never deletes a remote branch. Its only push goes to the evidence repo. Tracked edits and commits made after the pull request always keep the worktree.

| Measured 2026-11-20 about 02:30 UTC (read-only, not repeated) | Number |
|---|---|
| Git worktrees of our repos besides the main checkouts | 53 (IronClaude 33, Coder 14, IronFlow 4, IronOrca 2) |
| Of those, listed by Orca | 26 (so 27 are invisible to anything that uses Orca's list alone) |
| Merged by their own pull request | 24 |
| Of those, removable by every rule in this spec today | 13, about 3.1 GB; 4 of them need the evidence copy first |
| Not removable today | 40: 26 with no pull request, 3 merged with later commits, 2 open pull request, 1 closed unmerged, and 8 merged ones kept by a rule (open issue, fresh, in use, or ignored local state) |

## 1. What is already in or in flight (so nothing is built twice)

Checked 2026-11-20.

| Piece | State | What this spec does with it |
|---|---|---|
| The "did it land" check: `/sc:closeout`, issue #668, PR #683 | #668 is closed and PR #683 is merged (the issue body written earlier still says open: out of date). `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh <PR>` takes a pull request number and prints one line: `MERGED`, `OPEN`, `CLOSED`, `NONE` or `UNKNOWN`, with `match=same|differs|unchecked` for a merged one. It decides from pull request state, never from commit ancestry, so a squash merge counts. It is Jay Wedgeworth's `branch-landed.sh` adapted (Apache-2.0, see its `PROVENANCE.md`). | Reuse it. This script does not adopt Jay's `branch-landed.sh` a second time. It finds the pull request number of a worktree's branch with `gh pr list --head`, then calls the check. How the check is reached once installed is UNVERIFIED (section 11, item 3): the skill is not installed in this workspace's home folder. If the check cannot be run or says `UNKNOWN`, the worktree is kept. |
| Where worktrees live and how they are named: #289 (decision issue, open), #322 (proposed write boundary design, open) | Neither is decided. | Not decided here. The script finds worktrees with `git worktree list` in every repo, so it works wherever they sit. Item 4 of #289 ("when to remove a worktree after its pull request merges") is answered by this spec. |
| The issue-polling orchestrator: #655 (open, on hold) | On `origin/master` today (checked 2026-11-20 17:20 UTC): PR #700 (merged 15:07 UTC) rolled the build back; `docs/designs/orchestrator.md` and the `superclaude orchestrator` package are not there; PRs #686 and #690 are drafts. `/sc:closeout` (#668, PR #683) stays. | Nothing to check yet. Nothing in this spec depends on an orchestrator. Issue #655 appears here only as an open issue: it keeps its merged worktrees (rule 4) until it closes. |
| The plan sections of an issue (`## Priority`, `## Fix approach`, `## Test plan`) | Required by `refs/create.md` on `origin/master` (from #651, PR #661). #689 (open) proposes planning everything at creation. | No overlap. #687's body keeps those three headings last and in that order. |
| The daily log of merged pull requests: #669, PR #670 (merged) | Ships `scripts/merged_pr_log_orca_automation.md`, a definition of an opt-in Orca automation whose precheck command starts a script and exits non-zero so Orca starts no agent. | Use the same shape for this script's automation (section 5). |
| The evidence repo | `IronbellyOrg/run-evidence` (private) was created on 2026-11-20. Its `README.md` holds the folder convention and `tools/archive-workspace.sh` holds the archive and verify code. 16 merged workspaces were archived into it by hand that day, checked against GitHub: 477 files, 20 MB. | This spec turns that manual step into the archive step of section 7. |
| Removing worktrees | Nothing automated exists in IronClaude, Coder or IronOrca (searched when the issue was written, 2026-11-20; not repeated). `scripts/cleanup.sh` on `origin/master` clears build artifacts of one checkout and has no worktree handling (read 2026-11-20). The IronClaude `CLAUDE.md` asks for worktrees under `.dev/worktrees/` and forbids the editor's own worktree tool. | This spec is the new build. |
| Scheduling | Orca automations (`orca automations create`, with `--precheck`). Coder #515 (cron in the image) is open. | Use an Orca automation, as the daily log does. No cron. |
| Jay Wedgeworth's published work (Apache-2.0, `github.com/Simple-With-Us/AI-Fleet-Coordinator`) | `scripts/fleet_lanes/retire.py` (rules and code for removing a worktree), `docs/protocols/lane-map.md` (the cleaner contract), `scripts/disk-janitor.sh` (the 30-minute janitor), `scripts/branch-landed.sh` (the landed check). All four were read in full for this spec. | Rules adapted, with his notice kept. Section 12 says rule by rule what was taken, changed or dropped. |

## 2. The problem, with our numbers

Nothing removes merged worktrees and nobody decides when. Measured read-only on 2026-11-20 by reading `git worktree list`, `git status`, `gh pr list --head <branch>` and `orca worktree ps` for every repo Orca knows (IronClaude, Coder, IronFlow, IronOrca, GFxAI, Financials). The scratch scripts are in `/tmp/orca-audit/s687/` and are not part of any repo.

| Verdict, in the order the rules ask | Worktrees | Size |
|---|---|---|
| Merged by its own pull request, HEAD is the pull request's last commit, nothing changed or new | 15 | 6.1 GB |
| Same, but holds untracked files, all under `.dev/` (workflow files that were never in the pull request) | 6 | 3.2 GB |
| Merged, but HEAD differs from the pull request's last commit (one is behind it, two have later commits) | 3 | 2.4 GB |
| Open pull request | 2 | 2.4 GB |
| Pull request closed without merging | 1 | 0.1 GB |
| Branch with no pull request | 26 | 35.1 GB |
| Total | 53 | 49.4 GB |

Applying every rule of section 6 to the 21 merged ones in the first two rows (a read-only dry run):

| Result | Worktrees | Why |
|---|---|---|
| Removable | 13 (9 clean, 4 needing the evidence copy first), about 3.1 GB | Idle 20 to 26 days, no process, no terminal, no issue open, nothing ignored except build output. None of the 13 had an Orca terminal open, so decision 3 (an open terminal no longer keeps a worktree) changes none of today's 13. |
| Kept: issue still open | 4 | `issue-655-pr-c`, `issue-655-pr-d`, `issue-655-spec-pr` (issue #655 is open) and `coder-orca-from-fork` (its pull request names issue #373, which is open) |
| Kept: fresh | 2 | `issue-668-build-p3` and `issue-669`, idle 0 days (and `issue-669` has a process and a terminal in it) |
| Kept: ignored local state | 2 | `pr-submit-monitor-3` and `pr-submit-skill-cleanup` hold ignored `.claude/agent-memory` files, which are local state and not build output. The other 13 hold only build output and generated copies (`__pycache__`, `.venv`, `.codegraph`, `.ruff_cache`, `.pytest_cache`, `.serena/cache`, `uv.lock`, the `.claude/agents`, `commands`, `hooks`, `skills` and `templates` copies that `make sync-dev` rebuilds). |

Other facts that shape the design:

- **Orca lists 26 of the 53.** The 13 removable ones are all among the 27 Orca does not list. A removal that only calls `orca worktree rm` would remove none of them.
- **None of the 13 is in Orca's list, so Orca's own state cannot decide anything for them.** Orca's record for a listed worktree carries `linkedPR` (with the pull request state in this build), `lastActivityAt`, `isPinned` and `workspaceStatus` (which was `in-progress` on 48 of 49 workspaces on 2026-11-18). It carries no dirty flag and no issue state. The script asks `git` and `gh` itself and uses Orca's fields only as hints.
- **The benefit is mostly clutter.** The removable 13 are 3.1 GB of 49.4 GB. The worktrees folder as a whole was 162 GB on 2026-11-20, almost all of it Orca infrastructure and port folders that Clay ruled untouchable.
- **Orca can hide a workspace but the interface offers no archive.** The moon icon in the sidebar means "sleeping" (no terminals open). Clay sees only Delete, not Archive. So the only ways to clear the view are Sleep with "Hide sleeping", or removal. This spec is the removal path.
- **Workflow files never reach GitHub.** The `.dev/issues/<n>/` reports of a run are untracked and never in the pull request, and `.dev/pr-monitor/`, `.dev/eval-runs/`, `.dev/sprint-state/` and every `*.log` are git-ignored. The ignore rules come from the repo's own `.gitignore` (`*.log` since 2025-08-14; `.dev/pr-monitor/` since PR #162) and, in Coder, from a local `.git/info/exclude`. No skill adds them at run time. Removing a worktree deletes these files for good.
- **Run output is large and grows fast.** About 782 MB of untracked and ignored run output sat across the workspaces on 2026-11-19, and six workspaces of the 6.0.0 release alone added about 138 MB in two days. Compressed, the 16 workspaces archived by hand came to 20 MB.

**What went wrong in the manual cleanup of 2026-11-20 (and why this spec has the rules it has).** Sixteen merged workspaces were saved to the evidence repo, checked against GitHub, and then removed with `orca worktree rm --force`. Two of them (`docs-354-leandro-survey-fix` and `419-monitor-review-fixes`) belonged to issues #354 and #419, which were still open. Nothing was lost (both were saved, and both branches are on GitHub), but they should have stayed. That is why rule 4 below checks the issue, and why `--force` is banned in the script.

## 3. What the cleanup does

One script, `scripts/worktree_cleanup.py`, with four verbs and a thin command over it (`/sc:worktrees`, decision 10 in section 8). Dry run is the default for every verb that could remove something; `--apply` is the only way to remove.

| Verb | What it does | Removes anything? |
|---|---|---|
| `list` | Prints a table of every git worktree of every repo of ours, one decision (keep or removable) and one reason per row. | Never |
| `archive <worktree>` | Runs only the evidence step of section 7 on one worktree: copy, push, check against GitHub. | Never (it writes to the evidence repo only) |
| `retire <worktree>` | Removes one worktree whose work is safe, run from outside it, usually right after its pull request merges. Does the archive step first when the worktree needs it. | Only with `--apply` |
| `prune` | Runs the same decision on all worktrees and removes the removable ones. Without `--apply` it prints the table and writes it to a file. | Only with `--apply` |

**The table.** One row per worktree: repo, folder, branch, in Orca (yes or no), pull request and state, issue(s) and state, idle days, size, saved copy (none needed, saved and checked, or failed), decision and reason. The reason is the first rule that failed, in the order of section 6, in plain English.

**What a removal is, in order.** Each step fails closed: if any step cannot be completed or read back, the worktree is kept and the reason is shown.

1. **Save.** If the worktree holds untracked or ignored files under `.dev/`, run the archive step (section 7). Without a `VERIFIED` result the worktree is kept and nothing below happens.
2. **Close its Orca terminals** (only when it has any; decision 3). If everything else passed and only an Orca terminal is open, run `orca terminal close --worktree id:<id> --all`. Orca's own guide says this stops every terminal process in that workspace and removes its terminal tabs, layouts and agent-resume records, and that it reports `unverifiable` when it cannot confirm every process stopped. An `unverifiable` or failed close keeps the worktree. Closing a terminal ends that session for good: this is accepted.
3. **Check again, because a terminal may have been working.** Re-read `git status`, the untracked and ignored file lists, HEAD against the pull request's last commit, and the process scan. Any change since the save and any process still inside the worktree keeps it. The qualifier is the one that already exists, whether there are changes since the merge, and it is checked after the terminals are closed, not before. A busy agent would be making changes, so rules 3, 5 and 7 already cover it.
4. **Clear exactly the saved files** (decision 1). Only the untracked files and the ignored files that were saved and verified, named by exact path from the save's manifest: `git clean -f -x -- <those paths>`, fed through `xargs -0` with `GIT_LITERAL_PATHSPECS=1` so no name is read as a pattern. Never a path that is not in the manifest, never `-d` on a folder as a whole, never a tracked file (decision 2). Tested on 2026-11-20 with git 2.47.3 in a throwaway repository: it removes exactly the listed files (including a name with a space), leaves an unlisted untracked file and an unlisted ignored file alone, and `git clean` has no option to read its paths from a file, hence `xargs`. The reason this step exists: git refuses to remove a worktree that holds untracked files unless forced (tested: "contains modified or untracked files, use --force"; a modified tracked file is refused the same way), but removes one that holds only ignored files (a `.dev/pr-monitor/` folder, a `*.log`, a `.env`) without complaint. So git does not protect ignored local state, and rule 5 in section 6 does.
5. **Remove the worktree.** For a worktree Orca lists: `orca worktree rm --worktree id:<id>` without `--force`. For a worktree Orca does not list (the 13 removable ones today): `git worktree remove <path>` without `--force`. Whether `orca worktree rm` without `--force` refuses a dirty worktree is UNVERIFIED (section 11, item 1); the script checks `git status` itself regardless, as Jay's `retire.py` does. If git or Orca refuses, the worktree is kept and the reason is the refusal.
6. **Remove the local branch with `git branch -d`, never `-D`.** After a squash merge git refuses ("not fully merged", tested), and the branch is then reported as kept, which is not an error. For a worktree removed by Orca, Orca's own help says it also removes the checked-out local branch and keeps any branch whose changes it cannot prove merged; after the manual cleanup of 2026-11-20 the local branch of `docs-354-leandro-survey-fix` was gone. Nothing is lost in git: the branch and its commits remain on GitHub and the worktree can be recreated.
7. **Read back.** Confirm the folder is gone, `git worktree list` no longer shows it and `orca worktree list` no longer shows it. Record the result in the table.

In a dry run (no `--apply`) steps 1 to 7 are not run; the table shows "removable" and, for a worktree with Orca terminals, "its Orca terminals will be closed first".

**In scope for version 1, and nothing else.**
- (a) Git worktrees of our own repos: a repo whose `origin` belongs to IronbellyOrg or IronbellyGroup, found from `orca repo list` plus `git worktree list` in each repo (so worktrees Orca does not list are covered), wherever they sit (Orca's folder, `.dev/worktrees/`, `.claude/worktrees/`).
- (b) The local branch of each removed worktree, with `-d` only.

**Never touched.** Any folder that is not a git worktree of one of our repos, including all Orca infrastructure and port folders (`orca-port-evidence`, `orca-port-tools`, `orca-recipe-*`, `orca-pristine-*`, `orca-old-patched` and similar). As a second guard the script skips any worktree whose folder name starts with `orca-port-`, `orca-recipe-` or `orca-pristine-`, or is `orca-old-patched`, even if git lists it. The guard is anchored at the start of the name, so a worktree such as `coder-orca-port` (a real Coder branch, merged) is not caught by it.

## 4. When it runs and what triggers it

| Trigger | Who or what runs it | What it does |
|---|---|---|
| A pull request merges | The person who owns the worktree runs `retire <worktree>` from outside it. `/sc:closeout` may print the exact command as its last line; it does not run it. | Removes that one worktree if every rule of section 6 holds. |
| A schedule | One Orca automation per Coder workspace, once a day at 2:00 AM Central (08:00 UTC), switched on by that workspace's owner. Opt-in: nobody gets it by installing IronClaude. The name must not start with `coordinator-`. | `prune`. For the first week it only writes the table. After Clay switches it to apply, it removes. |
| By hand | Anyone, any time | `list`, `archive`, `retire` or `prune [--apply]`. |
| Low disk space | Not in version 1 | Nothing (decision 9: not now). |

Jay's janitor runs every 30 minutes because his disk was nearly full (the janitor header says free space gates the heavy work). Ours has about 488 GB free of 1.3 TB (`df`, 2026-11-20), so a daily run is enough. The time is Clay's decision 11: 2:00 AM Central, which is 08:00 UTC in winter (Central Standard Time), at the top of the hour. The cron string is `0 8 * * *` (UTC). In daylight saving time (March to November) 08:00 UTC is 3:00 AM Central. `orca automations create` has a `--timezone` option; whether it lets the schedule stay at 2:00 AM Central all year is UNVERIFIED and proved in step 1 (section 11, item 8). Until then the UTC string stands. The cadence is a setting of the automation, not of the script.

## 5. How it runs, per Coder workspace

**Files (all new; none exist on `origin/master`, checked 2026-11-20).**

| File | What it is |
|---|---|
| `scripts/worktree_cleanup.py` | The script. Python standard library only, no model call anywhere. Run as `uv run --no-project python scripts/worktree_cleanup.py <verb> ...` (the daily log's reason: a plain `uv run` can rewrite `uv.lock`, which an unattended job must not do). |
| `src/superclaude/commands/worktrees.md` | The thin command `/sc:worktrees`. It runs the script and prints the table. It does nothing until run, so it may be installed for everyone. It is a command, not a skill: a skill installs for everyone and would break the opt-in schedule. |
| `scripts/worktree_cleanup_orca_automation.md` | The automation definition, written and switched off, modelled on `scripts/merged_pr_log_orca_automation.md`. |
| Tests under `tests/` | Section 9. |

**One workspace, one run.** Each Coder workspace has its own Orca, its own repos and its own login. The automation is created once in each workspace by the person who owns it, and the script sees only that workspace's worktrees. Two people never remove each other's worktrees. They can both write to the evidence repo, which is built for that (section 7).

**The automation, with no agent.** Orca's automation needs a provider, but a precheck command that exits non-zero makes Orca skip the run and start no agent session. The daily log uses exactly this shape: the precheck starts the script detached and then exits 1.

```
bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv; [ -f ~/.env ] && . ~/.env; set +a; cd <checkout> && setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune --out <out dir> >> <out dir>/run.log 2>&1 < /dev/null &'; exit 1
```

Name: `worktree-cleanup-daily`. Trigger: `0 8 * * *` (UTC; 2:00 AM Central in winter, decision 11). Status: written, not switched on. A run that Orca skips because of the precheck shows as `skipped_precheck` in `orca automations runs`; that is the normal result here, not a failure. Whether the run shows anywhere else is not known (the daily log has the same limit), so the script writes its own dated table and `run.log`.

**Facts come from three places, never from an agent's word.**
- **git:** `git worktree list --porcelain`, `git status --porcelain`, `git rev-parse`, the files `HEAD`, `index` and `logs/HEAD` in each worktree's git folder, `.git/info/exclude`.
- **GitHub, through `gh`:** the pull request of the branch (`gh pr list --head <branch> --state all`), through the landed check of #668; the state of each issue (rule 4).
- **Orca, read only:** `orca repo list`, `orca worktree ps --json` (path, `lastActivityAt`, `isPinned`, `liveTerminalCount`, `linkedPR`, `comment`), `orca reference list --worktree`, `orca terminal list --worktree`.

**Credentials come only from the environment.** `GH_TOKEN` (never read from a file by the script; it is passed to `gh` and to `git push` through the environment). The token must read pull requests and issues in both orgs and push to the evidence repo. Other names, none secret: `RUN_EVIDENCE_REPO` (default `IronbellyOrg/run-evidence`), `RUN_EVIDENCE_DIR` (default `~/workspaces/run-evidence`, the local clone; the script clones it when it is missing), `WORKTREE_CLEANUP_IDLE_DAYS` (default 7). The workspace's own login is a stored file, so the push using only the environment token is UNVERIFIED (section 11, item 5). No token is printed or written to the table, the log or the evidence repo.

**Locks and repeats.** One lock file per repo in the output folder, so two runs cannot remove the same worktree twice; a second run after a removal finds nothing more to do.

**Output.** Each run writes `<out dir>/prune-<UTC timestamp>.md` (the table) and a `.json` of the same rows, and prints one summary: how many removed, kept and failed, and the first reason of each kept group. Exit codes follow Jay's: 0 means the run completed (some worktrees may be kept; read the table), 64 means a usage error or a `retire` of a worktree that is not removable, 69 means a lookup or a removal failed (the table still shows what happened). No output names an agent or a model.

**Rollout ladder** (Jay's "off, warn, enforce"): the definition is written and off; Clay switches it on in his workspace and for the first week it only writes the table (no `--apply`); Clay reads the tables; then Clay edits the automation to add `--apply`. Each other person decides separately for their own workspace.

## 6. The rules (what must be true before anything is removed)

A worktree is removed only when ALL eight rules hold. The rules are checked in this order, and the first one that fails is the reason shown in the table. Every rule fails closed: if the script cannot tell, it keeps the worktree. Adapted from Jay's `retire.py` and `lane-map.md` (section 12 maps each one).

| # | Rule | How it is checked | Reason shown when it fails |
|---|---|---|---|
| 1 | It is a linked worktree of one of our repos that this run may touch. | Not the first (main) entry of `git worktree list`; origin owner is IronbellyOrg or IronbellyGroup; not the folder the script runs in (compared by real path); not locked; folder present; not on the name guard of section 3; HEAD is on a branch. | "main checkout", "not our repo", "this is where the script runs", "locked", "folder missing (reported only)", "detached HEAD" |
| 2 | Its own pull request is MERGED. | The pull request of the worktree's branch from `gh pr list --head <branch> --state all` (newest merged one when there are several), then the landed check of #668 on that number must print `MERGED`. Squash-safe: decided from pull request state, never from commit ancestry. | "no pull request", "pull request #N is open", "pull request #N closed, not merged", "landed check said UNKNOWN" |
| 3 | Nothing was added after the pull request. | HEAD equals the pull request's last head commit (`headRefOid`), or is an ancestor of it. A commit made after it, however small, keeps the worktree. | "N commits after the pull request", "HEAD is not the pull request's head" |
| 4 | The issue it was for is CLOSED. (New; Clay, 2026-11-20.) | Issues are collected from every place below; any one that is OPEN keeps the worktree. Places: the pull request's closing references; every `#N` in the pull request title and body that is an issue (a number that is a pull request is ignored); a number in the branch name or folder name (`docs-354-...`, `419-...`, `issue-655-...`); Orca's card comment (for example `sc:issue IronbellyOrg/IronClaude#669`), its `linkedIssue` and `orca reference list`. No issue found: the rule passes and the table shows "none found". A failed lookup keeps the worktree. | "issue #N is open", "issue lookup failed" |
| 5 | Nothing unsaved is in it. | `git status --porcelain`, then the ignored files. A changed or staged tracked file keeps it. An untracked file outside `.dev/` keeps it. An ignored file outside `.dev/` keeps it unless it is build output or a generated copy (fixed list in the script: `__pycache__`, `.venv`, `.codegraph`, `.ruff_cache`, `.pytest_cache`, `.mypy_cache`, `.serena/cache`, `node_modules`, `dist`, `build`, `uv.lock`, and the `.claude/agents`, `commands`, `hooks`, `skills` and `templates` folders that `make sync-dev` rebuilds); an unknown ignored name is local state and keeps it. Untracked and ignored files under `.dev/` are allowed ONLY after the archive step of section 7 saved them and checked them against GitHub. | "N changed tracked files", "N untracked files outside .dev", "ignored local state: <names>", "saved copy failed: <why>" |
| 6 | Nothing but its own Orca terminals is using it. (Decision 3, Clay, 2026-11-20: an open Orca terminal does not keep a worktree.) | No process has its working folder inside it (reads `/proc/<pid>/cwd` for every readable process; `lsof` is not installed here; if the scan cannot be done, everything is kept). A process inside is tolerated ONLY while the worktree has Orca terminals open, because those terminals run processes with their folder inside; after the save is verified the terminals are closed (`orca terminal close --worktree id:<id> --all`) and every check is run again (section 3, steps 2 and 3), and any process still inside, an unconfirmed close or any change since the save keeps the worktree. Also: no other git checkout inside it (a `.git` file or folder below its top, because `git worktree remove` would delete the inner one with everything uncommitted in it); no git operation in progress (merge, rebase, cherry-pick, revert, bisect, `index.lock`). | "in use: process <pid> (<name>)", "a process is still inside after its Orca terminals were closed", "Orca terminal close not confirmed", "changed since the terminals were closed", "holds another checkout", "git operation in progress" |
| 7 | It has been idle for at least 7 days and was not created in the last 7 days. | The newest of: modification time of `HEAD`, `index` and `logs/HEAD` in the worktree's git folder, the last commit time, and Orca's `lastActivityAt` when Orca lists it. The number is a setting (`WORKTREE_CLEANUP_IDLE_DAYS`); 7 is Jay's, not measured here. | "idle N days (needs 7)" |
| 8 | It is not pinned and nobody asked to keep it. | Orca's `isPinned` is false and there is no `.worktree-keep` file. Nothing may create `.worktree-keep` as a way to protect work: that makes a worktree look unfinished forever (Jay's rule for `.janitor-keep`). | "pinned in Orca", "keep file present" |
**Orchestrator: nothing to check yet.** No tool on `origin/master` keeps a record of which worktrees an automated issue runner is working in (PR #700 rolled the orchestrator build back on 2026-11-20, and #655 is on hold). The earlier draft had a rule for it; it is removed. If such a record exists later, a rule that keeps a worktree named in it is added then. A busy agent in any worktree is already caught by rules 3, 5 and 7.

**Things the script never does.**
- Use `--force` on `orca worktree rm` or on `git worktree remove`, or use `git branch -D`, or run `rm`.
- Remove, reset or stash a tracked edit or a commit made after the pull request. Decision 1 allows `git clean -f -x` for the exact paths saved and verified in the evidence repo and for nothing else: never a path that is not in the save's manifest, never a folder as a whole, never a tracked file. Decision 2: those worktrees are kept.
- Close an Orca terminal of a worktree that has not passed every other rule and whose save is not verified.
- Push to any repo except the evidence repo, or delete any remote branch (Clay's ruling: shared branches are Clay's).
- Run `git worktree prune`, because a missing folder can mean a disk is not mounted (Jay's guard); it reports such a worktree and leaves it.
- Remove anything that is not a git worktree of one of our repos.
- Create, move or change a file inside a worktree it keeps (the archive step reads and copies; it never edits).
- Read a credential from a file, print a credential, or name an agent or a model in any output.

**Review checkouts of other people's pull requests** (Jay's `review-pr-<n>`): we have no such naming, so there is no special rule. Such a worktree has no pull request of its own and is kept.

## 7. The `.dev` archive step (save before removing)

**Why it exists.** A run writes its reports, logs and PR monitor output under `.dev/` in its worktree. Those files are untracked or git-ignored, so they never reach a pull request, and removing the worktree deletes them for good. Clay wants them kept for later mining without putting thousands of run files into the source repos (on `origin/master` today `.dev/` is 94% of IronClaude's files and 552 of its 577 MB, and 78% of Coder's files). They go to one private repo, `IronbellyOrg/run-evidence`, organised by source repo and person.

**How the step works, in order.** It runs inside `retire` and `prune` for any worktree that passed rules 1 to 4, 6 (open Orca terminals allowed), 7 and 8, and by hand as `archive <worktree>`.

1. Needs the merged pull request of rule 2. Without one it refuses (nothing is saved for unmerged work).
2. Build the folder in a scratch folder inside the local clone of the evidence repo (`RUN_EVIDENCE_DIR`, cloned when missing; `git fetch` and a fast-forward first).
3. Copy the untracked files that are not ignored, at their original relative paths, into `files/`. Pack the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of 85 MB when larger (GitHub refuses a file over 100 MB; the largest workspace had 99 MB of ignored run output before compression, so a single file near the limit is unlikely but possible, and the split guards it). Write `saved-paths.txt`, one exact path per line: every untracked file copied and every file inside `ignored.tar.gz` (read back from the archive with `tar -tzf`, files only). This list is the only thing the clearing step of section 3 may delete. Write `MANIFEST.md`: source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, and a SHA-256 of each archive file and of `saved-paths.txt`.
4. Commit in the evidence repo with the message `archive(<repo>): <date> pr<N> <subject>`.
5. `git fetch`, rebase onto `origin/main` if it moved, push. If the push is refused, repeat from the fetch up to 3 times, then stop with "saved copy failed: push refused".
6. Verify: `git fetch`, then the folder on `origin/main` must have the same file count as the local folder and `git diff --quiet origin/main -- <folder>` must pass. Print `VERIFIED <folder> files=<n>`. Anything else is a failure and the worktree is kept.
7. Repeat runs: if the folder already exists, the step verifies it again and re-checks that every file now in the worktree is covered by it (same worktree head and same file list). If something new appeared, it saves a second folder with the suffix `-r2` (then `-r3`). It never overwrites a folder.

**Folder convention.** `<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/`. `<pr-author>` is the GitHub login of the merged pull request's author, so each person's work lands under their own name (an onboarding-guide review by another contributor went to `IronFlow/swill-ib/2026-11-10_pr3_docs-add-onboarding-guide`, the other fifteen of the first batch under `<repo>/clayphi/`). `<YYYY-MM-DD>` is the UTC merge date, `<subject>` is the branch name without the author prefix, slashes turned into hyphens. Example: `IronClaude/clayphi/2026-11-11_pr494_docs-354-leandro-survey-fix`. The repo's `README.md` carries the same convention.

**What was proved on 2026-11-20.** The manual version of this step (a bash tool in the evidence repo) archived 16 merged workspaces, each checked against GitHub: 477 files, 20 MB for what was 782 MB on disk before compression, no file near the limit. This spec moves that logic into the cleanup script (decision 6) and keeps the folder convention unchanged.

**How the step changes the "nothing new or changed" rule.** Clay's ruling was: remove only worktrees whose pull request is MERGED and that hold nothing new or changed that was not in the pull request. Exactly one thing changes:

| What is in the worktree | Before the archive step | After the archive step |
|---|---|---|
| A tracked file edited or staged | Keep | Keep (unchanged) |
| A commit made after the pull request's last commit | Keep | Keep (unchanged; decision 2, decided: kept, not saved and removed) |
| An untracked file outside `.dev/` | Keep | Keep (unchanged) |
| An ignored file outside `.dev/` that is not build output (an environment file, a database, agent memory) | Keep | Keep (unchanged) |
| Build output and generated copies | Allowed | Allowed (unchanged) |
| **An untracked file under `.dev/`** (run reports, notes) | Keep | **Removable, but only if a saved copy of it was verified in the evidence repo** |
| **An ignored file under `.dev/`** (logs, PR monitor output, eval runs, sprint state) | Keep | **Removable, but only if a saved copy of it was verified in the evidence repo** |

In one sentence: nothing new or changed that was not in the pull request, except workflow files under `.dev/` that are saved and verified byte for byte in the evidence repo. The reason is that those files are run output that is never in a pull request by design, and the saved copy is the same bytes. If the save or the check fails for any reason, the exception does not apply and the worktree stays. On today's numbers this exception makes 4 more worktrees removable.

**Clearing the saved files (decision 1, decided).** Git refuses to remove a worktree that holds untracked files (tested, section 3), but removes one that holds only ignored files. Clay's answer: after the save is pushed and verified against GitHub, do whatever is needed to make the worktree removable, for the saved untracked and ignored files only. That is `git clean -f -x` on the exact paths of `saved-paths.txt` (section 3, step 4), with no `--force` on the removal itself. It is not a licence to remove tracked edits or later commits: those keep the worktree (decision 2).

**What is not saved.** Files outside `.dev/`; caches and build output; any worktree that is kept anyway (so a worktree with tracked edits or later commits is not archived by `prune`; `archive` by hand can still save them as a patch and a bundle).

**Secrets.** Credentials never come from a file and are never written to the evidence repo by the script. An ignored file outside `.dev/` (an environment file) keeps the worktree under rule 5, so it is never copied. Run output under `.dev/` can still contain a token a command printed: decision 8.

**Who can write.** Every contributor's workspace pushes to the evidence repo with its own login. Each person writes only inside their own folder, so rebases do not conflict. Granting write access is decision 7.

**Mining later.** Search with `git grep` over `MANIFEST.md` files, or read the folder names; the date, pull request number and subject are in the name. The folder holds a compressed archive of the ignored files and a plain copy of the untracked reports.

## 8. Decisions (all DECIDED by Clay on 2026-11-20)

Clay answered all 11 decisions on 2026-11-20. There are no open questions left in this spec. Earlier rulings, also settled: home is IronClaude; a script run by an Orca automation that starts no agent plus a thin command, not a skill; the schedule is opt-in; only worktrees whose pull request is MERGED are removed; the loose Orca infrastructure and port folders are never touched; never `--force` on a removal, never `git branch -D`, never `rm`, never a push to a source repo, never a remote branch delete; credentials only from the environment; no agent or model named in any output; only a person or the scheduled job applies.

| # | The question | DECIDED (Clay's answer) | What it means for the build |
|---|---|---|---|
| 1 | How are saved untracked files cleared so git will remove the worktree? | YES. After the save to the evidence repo is pushed and verified against GitHub, do whatever is needed to make that worktree removable, for the saved untracked and ignored files only: `git clean` on the exact saved paths, and clearing the ignored files that were saved. Not a licence to force-remove tracked edits or later commits (decision 2). | Section 3 step 4: `git clean -f -x --` on the exact paths of `saved-paths.txt`, through `xargs -0` with literal pathspecs. No `--force` on the removal. |
| 2 | Remove a merged worktree that has tracked edits or commits made after the pull request? | OK as recommended: KEPT, not removed. | Rule 3 and rule 5 keep it; `prune` does not archive it. |
| 3 | An open Orca terminal on a finished, merged worktree: keep or remove? | CHANGED. Clay: if everything is finished and merged and only the Orca terminal is still open, REMOVE it. The only qualifier is the one that already exists: are there changes since it was merged. If there are none, close its Orca terminal first (`orca terminal close`) and then remove the worktree. If there ARE changes since the merge, keep it. A busy agent would be making changes, so the existing rule already covers it. No idle-agent qualifier. | Rule 6 no longer keeps a worktree for an open terminal. Section 3 steps 2 and 3: close the terminals after the save is verified, then check again for changes before anything is cleared or removed. |
| 4 | How far does the "issue is closed" rule look? | STRICT: any issue named by the pull request's closing links, title or body, the branch or folder name, or Orca's card, and any one open keeps the worktree. | Rule 4 as written. `coder-orca-from-fork` stays while #373 is open. |
| 5 | An umbrella issue that stays open (like #655): an exception? | NO EXCEPTION. It keeps its merged worktrees until it closes; no label exception. | Rule 4 as written; no label logic. |
| 6 | Where does the archive code live? | In `scripts/worktree_cleanup.py` (Clay did not want to decide this; the recommendation was taken). `run-evidence` holds data and a README only; its bash tool is retired when the script merges. | Fix approach step 5. |
| 7 | Who may write to the evidence repo? | OK: contributors who run the automation get write access to `run-evidence`, each in their own folder. | As written in section 7. |
| 8 | Check the files for secrets before pushing them? | YES: a names-only secret check before pushing. | A hit keeps the worktree with "possible secret in <file name>" and never prints the value. |
| 9 | Which of Jay's other pieces come later? | NOT NOW. The dependency reaper and every other piece of Jay's later list are out of version 1; not built, and not specified beyond one line under Out of scope. | Section 10 has the one line. The earlier overview table is removed from section 12. |
| 10 | Name and shape. | OK: `scripts/worktree_cleanup.py` plus the command `/sc:worktrees` with `list`, `archive`, `retire`, `prune`. | As written in sections 3 and 5. |
| 11 | Schedule, rollout and idle floor. | YES: daily at 2:00 AM Central, which is 08:00 UTC; Clay does not want odd minutes such as :17, so the top of the hour; first week report only, then Clay switches to apply; idle floor 7 days. | Section 4 and 5: `0 8 * * *`. |

The command is installed for everyone and does nothing until run (decision 10). `/sc:cleanup` and `/sc:cleanup-audit` already exist for other jobs, so a different name avoids confusion.

## 9. Acceptance criteria and tests

**How the tests work.** New folder `tests/worktree_cleanup/` with a `fixtures/` folder, as `tests/merged_pr_log/` does for the daily log. Tests use recorded shapes of `gh`, `git` and `orca` replies (a fake runner that records every command it is asked to run) plus a throwaway repository with real worktrees and a local bare repository standing in for the evidence repo. They never touch a real worktree. Each case must fail if its rule is removed.

**Removal and keep cases**
- [ ] Removable: merged own pull request, HEAD is its last commit, clean, idle 8 days, no process, no Orca terminal, issue closed. The worktree is removed and the local branch is removed with `-d`.
- [ ] Kept, with the reason shown, for each of: the main checkout; a repo that is not ours; the folder the script runs in; a locked worktree; a missing folder (reported, never pruned); a detached HEAD; a name that starts with `orca-port-`, `orca-recipe-` or `orca-pristine-` (while `coder-orca-port` is not caught by the guard); no pull request; an open pull request; a pull request closed without merging; a landed check that says `UNKNOWN` or fails; a commit after the pull request's head; a HEAD that is not the pull request's head; an issue that is open through each of the four places (closing reference, `#N` in the body, a number in the branch name, Orca's card comment); an issue lookup that fails; a changed tracked file; an untracked file outside `.dev/`; an ignored environment file outside `.dev/`; an unknown ignored name; a process with its working folder inside; a failing `/proc` scan (keeps every worktree); a process inside a worktree that has no Orca terminal open; a process still inside after its Orca terminals were closed; an Orca terminal close that is not confirmed (`unverifiable`) or fails; a change that appears between the save and the terminal close (a new commit, a tracked edit, an untracked file outside `.dev/`); a merge, rebase, cherry-pick and `index.lock` in progress; idle 6 days; created 3 days ago; pinned; a keep file.
- [ ] Decision 3: a worktree that passes every rule and has Orca terminals open and a process inside is removed in `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed and the second check finds nothing changed and no process inside; in a dry run the table says "its Orca terminals will be closed first" and no terminal is closed.
- [ ] Allowed and not a reason to keep: ignored build output and generated copies (`__pycache__`, `.venv`, `.codegraph`, `uv.lock`, the `.claude/*` copies).
- [ ] A squash-merged pull request whose commits are not on the base is judged landed from pull request state, not ancestry.
- [ ] A pull request that is merged but whose branch was later reused for new commits keeps the worktree.

**Safety cases**
- [ ] A test records every command the script runs, in every verb and every branch, and fails if any is `--force` on a removal, `git branch -D`, `rm`, `git worktree prune`, a push to anything but the evidence remote, a remote branch delete, `git clean` that is not `git clean -f -x --` followed only by paths that are lines of that worktree's `saved-paths.txt` and issued after `VERIFIED`, or an `orca terminal close` for a worktree before every other rule passed and its save was verified.
- [ ] Dry run is the default and changes nothing (the recorded commands contain no removal); `--apply` removes only rows marked removable.
- [ ] A second run after a removal finds nothing more to do; two runs at once do not both remove the same worktree (one lock per repo).
- [ ] Folders that are not git worktrees of our repos (a plain folder, an Orca port folder) never appear in the table and are never touched.
- [ ] No output names an agent or a model (a test greps the table, the summary and the log). No secret is printed or written; the script never opens a credential file (a test fails on any read of `~/.config/gh/hosts.yml` or `~/.env` by the script itself); `GH_TOKEN` comes from the environment only.

**Archive step cases**
- [ ] A worktree with untracked and ignored `.dev/` files: the folder appears in the evidence repo at `<repo>/<author>/<date>_pr<N>_<subject>/` with `MANIFEST.md` (all fields of section 7), `files/` and `ignored.tar.gz`, `VERIFIED` is printed, and only then is the worktree removed.
- [ ] A failed push (refused three times), a folder that differs from GitHub after the push, and a failed copy each keep the worktree and show "saved copy failed" with the cause.
- [ ] An ignored archive larger than 85 MB is split into parts that join back to the same bytes.
- [ ] An existing folder is never overwritten: a repeat run verifies it and writes `-r2` when new files appeared.
- [ ] Two clones pushing different folders at the same time both end up on `origin/main` after the rebase and retry.
- [ ] A possible secret in a file to be saved (the names-only check of decision 8) keeps the worktree, names the file and never prints the value.
- [ ] Decision 1: exactly the paths in `saved-paths.txt` are cleared (including a name with a space) and nothing else: an untracked file that is not listed, an ignored file that is not listed and every tracked file are still there afterwards, and a path that is not in the list is refused by the runner.
- [ ] Decision 2: a merged worktree with a tracked edit or a commit after the pull request is kept, nothing is cleared, no terminal is closed and nothing is archived by `prune`.

**Facts the tests keep true.** In a throwaway repository: `git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file, and removes one that holds only ignored files; `git branch -d` refuses after a squash merge and the script then reports "kept" and not an error; `git clean -f -x --` with literal pathspecs removes exactly the listed files and leaves unlisted untracked and ignored files and tracked files alone. All observed on 2026-11-20 with git 2.47.3.

**Hand checks and finish**
- [ ] A dry run in Clay's workspace prints a table whose counts match `git worktree list` (53 non-main worktrees on 2026-11-20) and `orca worktree list` (26), checked by hand on one repo, and whose removable rows match the 13 of section 2 as of the day it runs.
- [ ] Jay's files that are adapted keep his Apache-2.0 notice and say what was changed (a `PROVENANCE.md` as #668 has).
- [ ] The regression gate passes: the full test suite, `make lint` and the sync checks that `/sc:pr-submit` runs. No em or en dashes in new files. Finish with `/sc:pr-submit --monitor 3`.

## 10. Out of scope

- Deciding where worktrees live and how they are named (#289, #322).
- Jay's other cleanup pieces (the dependency reaper, "delete branch on merge" as a repository setting, a low-disk trigger, main-checkout sync, the placement watcher and orphan process cleanup): not now (decision 9), not built and not specified here.
- The closeout itself (#668), and anything it already does.
- Deleting any shared or remote branch, or pushing to a source repo.
- Mac-only or server-only parts of Jay's housekeeping (CleanMyMac, launchd, simulators, package caches, process managers).
- Cleaning anything that is not a git worktree of our repos. All Orca infrastructure and port folders are untouchable.
- A repository-wide file cleanup or audit (`/sc:cleanup`, `/sc:cleanup-audit`, `scripts/cleanup.sh`, which clears build artifacts of one checkout and has no worktree handling).
- Hiding or sleeping Orca workspaces (the interface offers Sleep and Delete; the CLI has no archive).
- Moving the loose non-worktree folders (54 when the earlier draft was written; not recounted) or the infrastructure folders, and rewriting git history to shrink the source repos (the saved copy of future run output goes to the evidence repo; what is already tracked on `master` stays).
- Mining the evidence repo (a later job); this spec only keeps the data findable.

## 11. What is unproved, and how it is proved before anything depends on it

These are the only unverified facts the design leans on (the orchestrator state-file item of the earlier draft is removed: nothing to check yet). Step 1 of section 15 proves them, on throwaway worktrees only, and writes the result to `.dev/research/` before the build starts. Each has a fallback that keeps worktrees rather than removing them.

| # | Unproved | How to prove it | If it cannot be proved |
|---|---|---|---|
| 1 | Whether `orca worktree rm` without `--force` refuses a worktree with modified or untracked files, and what it does to the local branch of a squash-merged worktree (observed once: the branch of `docs-354-leandro-survey-fix` was gone after a forced removal). | Create a throwaway worktree with an agent (this workspace's hook refuses `orca worktree create` without `--agent`), make it dirty, run the removal without `--force`. | Use only `git worktree remove` (its refusal is tested) and deregister from Orca if Orca still lists the worktree. |
| 2 | Whether Orca stops listing a worktree that `git worktree remove` removed, and what its sidebar shows meanwhile. | Same throwaway worktree. | Remove through Orca for the worktrees it lists. |
| 3 | How the landed check of #668 is reached once installed. Its script lives at `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh` and takes a pull request number. `~/.claude/skills/sc-closeout-protocol` does not exist in this workspace (checked 2026-11-20), so how a script is to call the check is not known yet. | Read how #683 installs the skill and whether it adds a CLI verb; run the check on a merged and an open pull request. | The script runs `gh pr view <N> --json state,mergedAt` itself for the same answer (MERGED or not) and keeps everything when it cannot tell. This repeats three lines of #668's logic, so only as a fallback. |
| 4 | Reading `/proc/<pid>/cwd` as the check for "a process is inside". Here 33 of 271 entries were unreadable on 2026-11-20 (3 owned by root, the rest processes that exited between the listing and the read). A Coder workspace is single-user. | Define unreadable as: exited meanwhile is ignored; another user's entry is noted and ignored; any other error keeps everything. Test with a fake `/proc`. | Keep every worktree. |
| 5 | A push to the evidence repo with only the environment `GH_TOKEN` (the workspace's own `gh` login is a stored file, which the script must not read). | `git -c credential.helper='!gh auth git-credential' push` with `GH_TOKEN` set and no stored login, against a test repository. | Stop with "saved copy failed: no credentials in the environment"; nothing is removed. |
| 6 | That the precheck shape (start detached, exit 1) produces `skipped_precheck` and no agent session in this Orca build, as the daily log's definition says without re-verifying. | Create the automation disabled, then `orca automations run` it once and read `orca automations runs`. (Run now bypasses the precheck, so also wait for one scheduled tick.) | Use a cron entry in the workspace as a last resort (Coder #515 is open). |
| 7 | Whether Orca's `linkedPR` state can be trusted (it showed `merged` for `issue-669`). | Compare with `gh` on every worktree Orca lists. | Not used as authority in any case; `gh` is the only source for rule 2. |
| 8 | Whether the automation can stay at 2:00 AM Central all year. `orca automations create` has a `--timezone` option (seen in its help); whether it applies to a cron string or only to a preset such as `daily --time 02:00` is not known. The cron string `0 8 * * *` is 2:00 AM Central only in winter. | Create the automation disabled with `--trigger daily --time 02:00 --timezone America/Chicago` and read its next run time with `orca automations show`. | Keep `0 8 * * *` (08:00 UTC, as Clay said); it is 3:00 AM Central in daylight saving time. |
| 9 | Issue numbers taken from branch and folder names do not give false hits. | Test on the 53 real names with a rule of 2 to 4 digits that must exist as an issue in the same repo; pull request numbers are ignored. | A name with a number that is not an issue is simply not a source. |
| 10 | What `orca terminal close --worktree id:<id> --all` does to a worktree that has an agent terminal open: that it ends every process inside, that it reports `unverifiable` when it cannot confirm, and that nothing is written to the worktree meanwhile. The Orca guide documents the first two; neither was run. | On a throwaway worktree created with an agent (as item 1), run it and re-run the `/proc` scan and `git status`. | An unconfirmed or failed close keeps the worktree (already the rule). |

## 12. Jay Wedgeworth's work, rule by rule (Apache-2.0)

Source: `github.com/Simple-With-Us/AI-Fleet-Coordinator` (Apache-2.0, public). Read in full on 2026-11-20: `scripts/fleet_lanes/retire.py` (1,923 lines), `docs/protocols/lane-map.md` (300 lines), `scripts/disk-janitor.sh` (1,161 lines), `scripts/branch-landed.sh` (85 lines). None of it was run. A search of the three code files (`retire.py`, `disk-janitor.sh`, `branch-landed.sh`) for model or inference calls found none: the removal is git, GitHub and process checks in Python and shell. His two housekeeping skills (`housekeeper` and `mac-cleanup`) were not re-read here; the earlier draft says they are instruction files for an agent, and we do not need them.

| Jay's rule or piece | What it does | Ours |
|---|---|---|
| `retire.py`: linked worktree under the lanes root, never the integration tree | Only worktrees in the one agreed folder | Changed: rule 1. Our worktrees sit in several places, so any linked worktree of our repos qualifies, never a main checkout. |
| `retire.py`: the lane belongs to the chosen seat (folder name and `lane.json`) | A person or agent removes only their own lanes | Dropped. Each Coder workspace runs its own automation and sees only its own worktrees. |
| `retire.py`: not locked, no process with its folder inside (`lsof -d cwd`; if `lsof` fails nothing is removed), no git operation in progress, no `.janitor-keep` | "Nothing is using it" | Adopted as rule 6 and rule 8. Changed: `/proc/<pid>/cwd` because `lsof` is not installed here; the worktree's own Orca terminals no longer keep it, they are closed first and everything is checked again (decision 3, Clay); the keep file is `.worktree-keep`. Added from his janitor: a worktree that holds another checkout is never removed, because `git worktree remove` would delete the inner one with everything uncommitted in it. |
| `retire.py`: `git status` clean, and no git-ignored local state (a `.env`, a database) | "Nothing unsaved" | Adopted as rule 5. Changed: files under `.dev/` are allowed after the archive step of section 7. |
| `retire.py`: nothing unpushed (HEAD on a branch that exists on the remote right now, or in the default branch, or held by a merged or closed pull request) | "Nothing is lost" | Changed to rule 3: HEAD equals the merged pull request's last commit or is behind it. GitHub keeps that commit, so a squash merge or a deleted branch does not matter. Stricter than his: no "in the default branch" shortcut. |
| `retire.py`: the work is done (pull request MERGED or CLOSED with none open; or merged into the default branch; or the upstream was deleted; or the tree of HEAD equals a commit on the default branch; or every changed path is byte-identical in a merged pull request commit; or, with the relay down, local evidence) | Many ways to prove "landed" | Changed to rule 2: MERGED only (Clay), through the landed check of #668. The tree and byte-identical proofs, the closed-counts-as-done and the local-evidence fallback are dropped in version 1. A worktree with no pull request of its own, like the three stacked `issue-668` ones, is kept and reported. |
| `retire.py`: review checkouts `review-pr-<n>` are done when the pull request is merged or closed | A special name | Dropped: we have no such naming. |
| `retire.py prune`: kept if active in the last 15 minutes; a lane made and never used is kept 24 hours | Guards for a person's own prune | Replaced by rule 7: 7 days idle, which is Jay's janitor value (`STALE_DAYS=7`), because ours runs unattended for many people. The number is a setting. |
| `retire.py`: remove under a per-repo lock, `git status` again, `git worktree remove` without `--force`, then `git branch -d` (never `-D`; "not fully merged" after a squash is reported as kept) | The removal | Adopted as section 3, with `orca worktree rm` for worktrees Orca lists. `git worktree prune` is never run by us (a missing folder is only reported). |
| `retire.py`: a runner that only allows a fixed list of commands (`check_allowed`) | Safety by construction | Adopted: the script runs commands only through one runner with an allowlist, and a test records every command (section 9). |
| `retire.py`: dry run is the default; exit codes 0, 64, 69 | Interface | Adopted. |
| `branch-landed.sh` | Squash-safe landed check from pull request state | Reused through #668 (PR #683 adapted it; PROVENANCE says what changed). Not adopted a second time. |
| `lane-map.md`, "Cleaners": act only on the doctor's candidate list, never on `SAFE-TO-REMOVE` alone; `git worktree remove`, never `rm -rf`; never create a keep file as protection | A contract for anything that removes checkouts | Adopted. `list` is our doctor and `prune` runs the same decision code in the same run, so it never acts on a stale report. |
| `disk-janitor.sh`: every 30 minutes, only when disk is low, a pressure gate that skips work when load or swap is high | Why his runs often | Not adopted. He runs often because his disk was nearly full; ours has about 488 GB free, so daily and light, with no disk gate and no pressure gate in version 1. |
| `disk-janitor.sh`: the `REAP_WORKTREES` master switch, `WT_REAP_DRYRUN`, a run lock with a heartbeat | Switches and locking | Adopted in spirit: dry run default, a per-repo lock, and the automation itself is the master switch (off until a person switches it on). |

Jay's other cleanup pieces are not part of version 1 (decision 9, Clay: not now); they are named in one line under Out of scope (section 10) and are not specified here.

Where text or code is copied or closely adapted, the file carries Jay's Apache-2.0 notice and a line saying what was changed, as `sc-closeout-protocol/PROVENANCE.md` does.

## 13. Where this spec differs from the preliminary spec in the issue (this spec wins)

| Topic | Preliminary spec said | This spec says | Why |
|---|---|---|---|
| "Nothing new or changed" | Strict: any untracked or ignored file keeps the worktree; finding 3 left 8 merged worktrees kept and offered "copy the workflow folders to an archive" as a later option | Workflow files under `.dev/` are allowed after a verified save in the evidence repo (section 7); everything else stays strict | Clay asked for the save step; it frees 4 more worktrees today and loses nothing |
| The issue the worktree was for | Not a rule | Rule 4: any linked issue still open keeps the worktree | Two workspaces with open issues (#354, #419) were removed by hand on 2026-11-20 |
| Pushes | "Never push" | Never push to a source repo; the one push is to the evidence repo | The save step needs it |
| The landed check | #668 and PR #683 open; build waits | #668 closed, PR #683 merged; reuse it; how it is reached is unproved (section 11, item 3) | State changed on 2026-11-20 |
| Own pull request | Jay's extra proofs kept as a second proof | Only the worktree's own merged pull request counts; stacked worktrees without one are kept and reported | Clay: merged only |
| How a removal is made | `orca worktree rm`, then `git branch -d` | `orca worktree rm` for worktrees Orca lists, `git worktree remove` for the rest (all 13 removable ones today), then `git branch -d` | Orca lists 26 of 53 |
| What counts as running | "Process check" | `/proc/<pid>/cwd` and a nested checkout; the worktree's own Orca terminals are closed first and everything is checked again (decision 3) | `lsof` is not installed; Jay's janitor guards the nested case; Clay's answer to decision 3 |
| The orchestrator | A rule that keeps a worktree named in an orchestrator state file, with citations of its design | Removed: nothing to check yet. PR #700 rolled the orchestrator build back on 2026-11-20 and #655 is on hold; the design file and the state files are not on `master` | Keep only what is true on `origin/master` |
| Clearing and removing | Removal only | Save, close terminals, check again, `git clean -f -x --` on the exact saved paths, remove (section 3) | Clay's answers to decisions 1 and 3 |
| Jay's other pieces | An overview and a recommendation (dependency reaper as version 2) | One line under Out of scope | Clay: not now |
| Schedule | Daily 08:17 UTC | Daily 08:00 UTC, which is 2:00 AM Central in winter | Clay: top of the hour, 2:00 AM Central |
| Counts | 51 worktrees, Orca lists 24 | 53 worktrees, Orca lists 26 (about 02:30 UTC on 2026-11-20, after the 16 removals and new work; not repeated since) | Re-measured |
| Orca's record | "No pull request state" | `worktree ps` shows `linkedPR` with a state in this build; still only a hint | Observed on `issue-669` |
| Decisions for Clay | Six, open | Eleven, all DECIDED by Clay on 2026-11-20 (section 8) | The new steps needed them; Clay answered all of them |
| Test list | 17 keep cases | About 35 cases in 4 groups, including the archive step (section 9) | New rules |
| Idle time | Git folder files and last commit | Same, plus Orca's `lastActivityAt` when Orca lists the worktree | Both are cheap |

## 14. Links

Jay Wedgeworth, `github.com/Simple-With-Us/AI-Fleet-Coordinator` (Apache-2.0):
- Rules and code for removing a worktree: https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/scripts/fleet_lanes/retire.py
- Where every checkout lives, how to retire one, the cleaner contract: https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/docs/protocols/lane-map.md
- The 30-minute janitor (read its retire block and safety notes, not the Mac cache parts): https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/scripts/disk-janitor.sh
- The landed check (reuse through #668): https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/scripts/branch-landed.sh

Ours (IronbellyOrg):
- IronClaude #668 and PR #683 (`/sc:closeout`, the landed check): `src/superclaude/skills/sc-closeout-protocol/`.
- IronClaude #289 (worktree and branch protocol), #322 (write boundary design), #689 (plan everything at creation), #669 and PR #670 (the daily log: the automation pattern in `scripts/merged_pr_log_orca_automation.md`), PR #700 (the rollback of the orchestrator build, merged 2026-11-20), #655 (on hold; named in this spec only as an open issue).
- IronbellyOrg/run-evidence (private): `README.md` for the folder convention, `tools/archive-workspace.sh` for the manual version of the archive step.
- The Priority rule set and the plan-section rule: `src/superclaude/skills/sc-issue-protocol/refs/create.md` on `origin/master`.

Commands used for the facts: `orca worktree list --json`, `orca worktree ps --json`, `orca worktree rm --help`, `orca reference list --worktree <selector> --json`, `orca terminal list --worktree <selector> --json`, `orca automations create --help`, `git worktree list --porcelain`, `gh pr list --head <branch> --state all`. The scratch scripts of the survey and dry run are in `/tmp/orca-audit/s687/` and are not in any repo.

## 15. Plan of work

1. **Prove the unproved** (section 11), on throwaway worktrees only, and write the findings to `.dev/research/worktree-cleanup-proofs.md`. Touches no existing file.
2. **The decisions are made** (section 8). If a proof in step 1 fails, use the fallback named in section 11 for that item; any other change goes back to Clay.
3. **Build** `scripts/worktree_cleanup.py` (command runner with an allowlist, fact gathering from git, `gh` and Orca, rules 1 to 8, the four verbs, the table and its file, locks, the archive step with its secret check and `saved-paths.txt`, the terminal close and second check, the exact-path clearing) and `src/superclaude/commands/worktrees.md`, registered where the repo lists commands. Reuse the landed check of #668.
4. **Test and automate**: `tests/worktree_cleanup/` with fixtures (section 9), and `scripts/worktree_cleanup_orca_automation.md` (written, switched off, modelled on the daily log's). A provenance block with Jay's Apache-2.0 notice at the top of the script.
5. **Retire the manual tool** in the evidence repo (its `tools/archive-workspace.sh` becomes a pointer to the script) if decision 6 is as recommended. A separate small change in that repo.
6. **Dry run in Clay's workspace** and compare the table with `orca worktree list` and `git worktree list` for one repo.
7. **Pull request** with `/sc:pr-submit --monitor 3`.
8. **First week report only**, then Clay switches the automation to apply (not done by the worker).

`````

### .dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/TASK-WF-specWorktreeClea-20261120-173546.md:1-274

````` markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-specWorktreeClea-20261120-173546
version: "1"
priority: Medium
created_date: "2026-11-20"
---

# Daily cleanup of merged worktrees (issue 687): script, command, automation definition and tests

Source: ./source.md
Goal: A person can run `/sc:worktrees` (list, archive, retire, prune) to remove git worktrees of IronbellyOrg repos only when all eight rules of source section 6 hold, after saving untracked and ignored `.dev/` files to the evidence repo and closing the worktree's own Orca terminals; a switched-off Orca automation definition exists for the daily report-only run; the whole feature is proved by tests that use only throwaway repositories and fake `gh`, `git` and `orca` replies.

## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.

## Phase 1: Prove what can be proved, and lay the script foundation

## Task 1: Write the proofs record for source section 11

Create `.dev/research/worktree-cleanup-proofs.md` with one row for each of the ten unproved items of source section 11 (columns: item, status PROVEN or NOT PROVEN, evidence or reason, fallback used by the script). Prove only what needs no write to a real worktree, Orca, GitHub or the evidence repo: item 3 (read how `superclaude install` copies the `sc-closeout-protocol` skill under `src/superclaude/cli/`, whether #683 added a command-line verb for the landed check, and run `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh` once on pull request 700 and once on a number that does not exist, to see `MERGED` and `NONE`); item 4 (write the definition: a process that exited meanwhile is ignored, another user's entry is noted and ignored, any other error keeps everything); item 9 (read-only: take the branch and folder names from `git worktree list --porcelain` of this checkout and show which numbers of 2 to 4 digits the rule would extract). Mark items 1, 2, 5, 6, 7, 8 and 10 NOT PROVEN, because proving them needs a real Orca removal, a real push, an automation or a terminal close, which the safety constraint forbids; for each, copy the fallback of source section 11 and say what the code does because of it (items 1 and 2: remove an Orca-listed worktree with `orca worktree rm` without `--force` and read back, a refusal keeps it; item 5: stop with "saved copy failed: no credentials in the environment" when the push fails; item 6: the automation definition says the `skipped_precheck` result is UNVERIFIED; item 8: keep `0 8 * * *`; item 10: an unconfirmed or failed close keeps the worktree). Also record in the file the answer the script will use for item 3, so Task 5 can follow it: look for `branch-landed.sh` first at `~/.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh`, then at `.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh` under the checkout, then (labelled in-checkout fallback) at `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh`, and when none exists run `gh pr view <N> --json state,mergedAt` for the same MERGED-or-not answer and keep the worktree when it cannot tell.

Acceptance criteria:
- `.dev/research/worktree-cleanup-proofs.md` exists, has exactly ten rows, and every row states PROVEN or NOT PROVEN with the command or reason and the fallback.
- Items 3, 4 and 9 are PROVEN with the output of the commands run (the `MERGED` line for pull request 700 and the `NONE` line for the missing number appear verbatim); items 1, 2, 5, 6, 7, 8 and 10 are NOT PROVEN with the safety reason.
- The file names the branch-landed lookup order and the `gh pr view` fallback exactly as written above.
- No real worktree, Orca automation, Orca terminal, remote branch or evidence repo was touched to produce it (no `--apply`, no `orca worktree rm`, no push).

## Task 2: Create the script skeleton with the allowlisted command runner

Depends on: Task 1

Create `scripts/worktree_cleanup.py` (new, Python standard library only; modelled on the stdlib style of `scripts/merged_pr_log.py`, which has `parse_args` and `main`). Top of the file: Jay Wedgeworth's Apache-2.0 notice block (source `github.com/Simple-With-Us/AI-Fleet-Coordinator`, copyright 2026 Jay Wedgeworth, rules adapted from `scripts/fleet_lanes/retire.py`, `docs/protocols/lane-map.md` and `scripts/disk-janitor.sh`, what was changed: see `scripts/worktree_cleanup_PROVENANCE.md`, which Task 19 writes). Then a plain-English module docstring and these parts: constants (idle floor from `WORKTREE_CLEANUP_IDLE_DAYS` default 7, `RUN_EVIDENCE_REPO` default `IronbellyOrg/run-evidence`, `RUN_EVIDENCE_DIR` default `~/workspaces/run-evidence`, archive part size 85 MB as a module constant so tests can lower it, owners `IronbellyOrg` and `IronbellyGroup`, the name guard `orca-port-`, `orca-recipe-`, `orca-pristine-` as prefixes and `orca-old-patched` as an exact name, the fixed build-output list of source section 6 rule 5, exit codes 0, 64, 69); one `Runner` class that is the only way the script starts an outside program (argument list, no shell, `GH_TOKEN` passed only through the environment of `gh` and `git push`) with a `check_allowed` step, adapted from Jay's runner, that refuses before any process starts: `--force` or `-f` on `orca worktree rm` or `git worktree remove`, `git branch -D`, `rm`, `git worktree prune`, `git push` with a delete flag or a `:ref` refspec, `git push` when the working folder is not the evidence clone, and `git clean` unless it is exactly `-f -x --` (run through `xargs -0` with `GIT_LITERAL_PATHSPECS=1`) and every path on its standard input is one of the paths registered as saved and verified (the registration call is added in Task 11); the runner records every command (argument list and working folder) in a list and has one overridable `_execute` hook so tests can answer `gh`, `orca` and `branch-landed.sh` from recorded shapes while real `git` runs on throwaway repos. Add `parse_args` and `main(argv, runner=None)` with the four verbs `list`, `archive <worktree>`, `retire <worktree>` and `prune`, the flags `--apply` and `--out <dir>` (default `~/.local/state/worktree-cleanup`, chosen so nothing is written inside any worktree), dry run as the default, and the verb bodies as stubs that exit 64 with "not built yet" until Tasks 11 and 12 fill them in. The file never reads `~/.config/gh/hosts.yml` or `~/.env`.

Acceptance criteria:
- `uv run --no-project python scripts/worktree_cleanup.py --help` lists the four verbs and the two flags; `main(["list"], runner=...)` can be called from a test with an injected runner.
- `Runner.check_allowed` raises a dedicated refusal error for each banned shape listed above before any process starts (these refusals are asserted in Task 13's recorder tests).
- An `ast` scan of the file finds only standard library imports and no call to `os.remove`, `os.unlink`, `shutil.rmtree` or a command named `rm`.
- The Apache-2.0 notice block and the pointer to `scripts/worktree_cleanup_PROVENANCE.md` are at the top of the file.

## Phase 2: Facts from Orca, git and GitHub

## Task 3: Add the read-only Orca facts

Depends on: Task 2

In `scripts/worktree_cleanup.py` add the Orca reads of source section 5 ("Facts come from three places"), each through the `Runner` and each returning a small typed record: `orca repo list` (the repos Orca knows, with their folders), `orca worktree ps --json` (path, `lastActivityAt`, `isPinned`, `liveTerminalCount`, `linkedPR`, `comment`, and the worktree id used as `id:<id>`), `orca reference list --worktree <selector>` and `orca terminal list --worktree <selector>`. Orca's `linkedPR` is kept only as a hint and is never used as the authority for rule 2 (source section 11, item 7). A failed or unparseable Orca read is reported as "Orca unavailable" for the facts it would have given; it never aborts the run and never makes a worktree removable: a worktree Orca does not list is treated as not in Orca (it is still found through git, Task 4), and when `orca repo list` itself fails the repo list falls back to the current checkout's repo only and the table says so. The script only ever runs the read verbs here; the close and remove verbs are added in Task 11.

Acceptance criteria:
- A parse function for each of the four reads accepts the recorded shape saved under `tests/worktree_cleanup/fixtures/` by Task 7 and returns the fields named above; a malformed reply yields "Orca unavailable", not an exception.
- No function in this task issues `orca terminal close` or `orca worktree rm`; the recorder test of Task 13 shows only read verbs for these reads.
- `linkedPR` appears in the returned record but no rule function reads it as proof of a merge.

## Task 4: Add the read-only git facts, local state classification and the process scan

Depends on: Task 3

In `scripts/worktree_cleanup.py` add, through the `Runner`: discovery of worktrees as `orca repo list` folders plus `git worktree list --porcelain` run in each repo, so worktrees Orca does not list are found, wherever they sit (source section 3, "In scope"); per worktree the main-checkout flag (first porcelain entry), locked flag, folder present or missing, branch or detached HEAD, `origin` owner (IronbellyOrg or IronbellyGroup, from `git remote get-url origin`), `git rev-parse HEAD`, `git status --porcelain` split into changed tracked files, untracked files outside `.dev/`, untracked files under `.dev/`, and the ignored files from `git status --porcelain --ignored` split into build output and generated copies (the fixed list of source section 6 rule 5, matched on path parts), ignored files under `.dev/`, and unknown ignored names; the idle time as the newest of the modification times of `HEAD`, `index` and `logs/HEAD` in the worktree's own git folder, the last commit time, and Orca's `lastActivityAt` when Orca lists it, plus the creation age; a `.worktree-keep` file check; a git operation in progress check (merge, rebase, cherry-pick, revert, bisect, `index.lock` in the worktree's git folder); a nested checkout check (a `.git` file or folder below the top of the worktree); and the process scan: read `/proc/<pid>/cwd` for every entry, ignore an entry that exited meanwhile, note and ignore an entry of another user, and treat any other error as "scan failed" which keeps every worktree (source section 11, item 4); the `/proc` root is a parameter so tests can pass a fake. The size of each worktree is computed by walking the folder read-only. The script's own folder is compared by real path. The name guard of source section 3 is anchored at the start of the folder name, so `coder-orca-port` is not caught.

Acceptance criteria:
- On a throwaway repository built by Task 7, each fact is returned correctly for a clean worktree, one with a changed tracked file, one with an untracked file outside `.dev/`, one with untracked and ignored files under `.dev/`, one with an ignored environment file outside `.dev/`, and one with only build output.
- The process scan returns "scan failed" for an unreadable-for-another-reason entry in a fake `/proc` and ignores a vanished one and another user's one.
- `orca-port-evidence`, `orca-recipe-x`, `orca-pristine-y` and `orca-old-patched` are on the name guard and `coder-orca-port` is not.
- No git command in this task changes the repository (the recorder test of Task 13 shows read verbs only: `worktree list`, `status`, `rev-parse`, `remote get-url`, `log`, `ls-files`).

## Task 5: Add the GitHub facts: own pull request, landed check and issues

Depends on: Task 4

In `scripts/worktree_cleanup.py` add, through the `Runner`: the pull request of a worktree's branch with `gh pr list --head <branch> --state all --json ...` run with the repo named explicitly (`--repo <owner>/<repo>` taken from that repo's `origin`; never the `{owner}/{repo}` placeholder), choosing the newest merged one when there are several and recording number, state, `headRefOid`, author login, merge date, title, body, closing references and branch; then the landed check by number: run `branch-landed.sh <PR>` with the repo's main checkout as the working folder (the script reads `origin` of the current directory and needs `jq` and one `git fetch`), locating the script by the order recorded in Task 1 (installed copy under `~/.claude/skills/sc-closeout-protocol/scripts/`, then the checkout's `.claude/skills/...`, then the in-checkout `src/superclaude/skills/...` labelled fallback, then `gh pr view <N> --json state,mergedAt` for the same MERGED-or-not answer); the result must be the token `MERGED` for rule 2 to pass, and `UNKNOWN`, a failed call or a missing `jq` means keep. Add issue collection for rule 4 from every place of source section 6 rule 4: the pull request's closing references, every `#N` in the pull request title and body that is an issue (a number that is a pull request is ignored, resolved in the right repo, so Coder #373 is an issue and IronClaude #373 is a merged pull request), a number of 2 to 4 digits in the branch name or folder name that must exist as an issue in the same repo, Orca's card comment (for example `sc:issue IronbellyOrg/IronClaude#669`), its `linkedIssue` and `orca reference list`; each issue's state is read with `gh issue view <N> --repo <R> --json state`; any lookup failure is "issue lookup failed" which keeps the worktree; no issue found passes with "none found". Rule 3 data: whether HEAD equals the pull request's `headRefOid` or is its ancestor (`git merge-base --is-ancestor` run read-only) and how many commits come after it.

Acceptance criteria:
- Every `gh` call in this task carries an explicit `--repo <owner>/<repo>` argument (asserted by the recorder test of Task 13); no call uses `gh api` with a placeholder.
- A squash-merged pull request whose commits are not on the base is returned as merged from pull request state, with no commit-ancestry question asked.
- Issue numbers come back from all four places of the spec's test list (closing reference, `#N` in the body, a number in the branch name, Orca's card comment), with pull request numbers dropped and the repo resolved per number.
- With `branch-landed.sh` absent from all three places, the `gh pr view` fallback answers, and when that also fails the result is "landed check said UNKNOWN".

## Phase 3: The eight rules and their tests

## Task 6: Implement the eight rules in order, with their reasons and the table row

Depends on: Task 5

In `scripts/worktree_cleanup.py` add one decision function that takes the facts of Tasks 3 to 5 plus a save state (`not needed`, `needed`, `verified`, `failed: <why>`) and returns a decision (`removable` or `kept`), the first failed rule and its plain-English reason, and the table row. Apply the eight rules of source section 6 in that order with exactly the reasons shown there: rule 1 (main checkout, not our repo, this is where the script runs, locked, folder missing reported only, name guard, detached HEAD), rule 2 (no pull request, open, closed not merged, landed check UNKNOWN), rule 3 (N commits after the pull request, HEAD is not the pull request's head), rule 4 (issue open, issue lookup failed), rule 5 (changed tracked files, untracked files outside `.dev`, ignored local state with names, `.dev` files allowed only when the save state is `verified`, else "saved copy failed: <why>"), rule 6 (a process inside tolerated only while the worktree has Orca terminals open; otherwise "in use: process <pid> (<name>)"; a failed `/proc` scan keeps everything; holds another checkout; git operation in progress), rule 7 (idle fewer than the floor days, created within the floor days), rule 8 (pinned in Orca, keep file present). Every rule fails closed: a fact that could not be read keeps the worktree. In a dry run a worktree that passes with untracked or ignored `.dev/` files shows `removable` with the saved-copy cell `needed`, and one with Orca terminals open shows the note "its Orca terminals will be closed first". The table row has the columns of source section 3: repo, folder, branch, in Orca, pull request and state, issue(s) and state, idle days, size, saved copy, decision and reason. Add the table renderers (markdown and the same rows as JSON).

Acceptance criteria:
- A pure function (no process started) returns the same decision for the same facts, so tests can call it with hand-built facts.
- For every rule, a worktree that fails only that rule is kept with that rule's reason, and the reasons are the strings of source section 6.
- A worktree with only Orca terminals open and a process inside passes rule 6 in the first pass and carries the note "its Orca terminals will be closed first"; a process inside with no Orca terminal fails rule 6.
- The markdown table has the eleven columns above and the JSON has the same rows.

## Task 7: Build the test support and the "facts the tests keep true" checks

Depends on: Task 6

Create `tests/worktree_cleanup/__init__.py`, `tests/worktree_cleanup/conftest.py`, `tests/worktree_cleanup/fixtures/` and `tests/worktree_cleanup/test_git_facts.py` (new; layout as `tests/merged_pr_log/` has `__init__.py`, `fixtures/` and one test module that loads the script with `importlib.util.spec_from_file_location`). `conftest.py` provides: a loader of `scripts/worktree_cleanup.py`; a recording runner built on the script's `Runner` that answers `gh`, `orca` and `branch-landed.sh` from canned replies and runs real `git`, `tar` and `xargs` only inside throwaway folders under `tmp_path`; a builder for a throwaway repository with real linked worktrees (a clean one, one with a tracked edit, one with untracked and ignored `.dev/` files, one with an ignored environment file, one with only build output, one with a detached HEAD, a locked one) whose `origin` points at a local bare repository, and a second local bare repository standing in for the evidence repo; a fake `/proc` builder. `fixtures/` holds JSON in the recorded shape of `gh pr list`, `gh pr view`, `gh issue view`, `orca repo list`, `orca worktree ps --json`, `orca reference list` and `orca terminal list`; a README line in the module docstring says the shapes are hand-written from the spec and the Orca help, not literal captures (as `tests/merged_pr_log/test_merged_pr_log.py` says). `test_git_facts.py` keeps true the facts of source section 9 "Facts the tests keep true" in a throwaway repository: `git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file and removes one that holds only ignored files; `git branch -d` refuses after a squash merge and the script's removal reports "kept" not an error; `git clean -f -x --` with literal pathspecs removes exactly the listed files (including a name with a space) and leaves unlisted untracked and ignored files and tracked files alone. Use obvious placeholders for any token-shaped value, never a real one.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_git_facts.py -v` passes using only `tmp_path` repositories; no test touches a real worktree.
- The recording runner exposes the full list of commands it was asked to run, and refuses (raises) any command the real `Runner.check_allowed` would refuse.
- The fixtures folder holds one recorded shape for each of the seven replies listed above.
- The three git facts are asserted, including the file name with a space.

## Task 8: Write the removal and keep tests for the eight rules

Depends on: Task 7

Create `tests/worktree_cleanup/test_rules.py` with the first test group of source section 9, each case failing if its rule is removed. Removable case: merged own pull request, HEAD is its last commit, clean, idle 8 days, no process, no Orca terminal, issue closed, so the decision is `removable`. Kept cases, each asserting the reason text, for: the main checkout; a repo that is not ours; the folder the script runs in; a locked worktree; a missing folder (reported, never pruned); a detached HEAD; a name starting with `orca-port-`, `orca-recipe-` or `orca-pristine-` (while `coder-orca-port` is not caught); no pull request; an open pull request; a pull request closed without merging; a landed check that says `UNKNOWN` or fails; a commit after the pull request's head; a HEAD that is not the pull request's head; an issue that is open through each of the four places (closing reference, `#N` in the body, a number in the branch name, Orca's card comment); an issue lookup that fails; a changed tracked file; an untracked file outside `.dev/`; an ignored environment file outside `.dev/`; an unknown ignored name; a process with its working folder inside; a failing `/proc` scan (keeps every worktree); a process inside a worktree that has no Orca terminal open; a merge, rebase, cherry-pick and `index.lock` in progress; idle 6 days; created 3 days ago; pinned; a keep file. Also: ignored build output and generated copies (`__pycache__`, `.venv`, `.codegraph`, `uv.lock`, the `.claude/agents`, `commands`, `hooks`, `skills` and `templates` copies) are allowed and not a reason to keep; a squash-merged pull request whose commits are not on the base is judged landed from pull request state; a pull request that is merged but whose branch was later reused for new commits keeps the worktree.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_rules.py -v` passes and has at least one test for every item listed above.
- Mutation check by hand for one rule per group: temporarily making rule 4 always pass (or rule 3, or rule 6) makes at least one test in this file fail.
- Every kept case asserts the plain-English reason, not only the decision.

## Phase 4: Save before removing

## Task 9: Implement the `.dev` archive step with the names-only secret check

Depends on: Task 6

In `scripts/worktree_cleanup.py` implement source section 7 as one function used by the `archive` verb and by `retire` and `prune`. Order: needs the merged pull request of rule 2 and refuses without one; syncs the local clone of the evidence repo (`RUN_EVIDENCE_DIR`, cloned when missing with the repo from `RUN_EVIDENCE_REPO`; `git fetch` and fast-forward); builds the folder inside a scratch folder in that clone and, when complete, renames it into place (a failed save leaves its scratch folder, named in the log, and deletes nothing); copies untracked files that are not ignored at their relative paths into `files/`; packs the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of the 85 MB module constant when larger; writes `saved-paths.txt` (one exact path per line: every untracked file copied and every file inside the archive, read back with `tar -tzf`, files only) and `MANIFEST.md` (source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, SHA-256 of each archive part and of `saved-paths.txt`); commits with the message `archive(<repo>): <date> pr<N> <subject>`; runs `git fetch`, rebases onto `origin/main` when it moved, pushes, and on a refused push repeats from the fetch up to 3 times then fails with "saved copy failed: push refused"; verifies with `git fetch`, the same file count on `origin/main` and `git diff --quiet origin/main -- <folder>`, and prints `VERIFIED <folder> files=<n>`; the push uses `git -c credential.helper='!gh auth git-credential'` with only the environment `GH_TOKEN` and a failure to authenticate reads "saved copy failed: no credentials in the environment". Folder convention: `<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/` with the UTC merge date and the branch name without the author prefix, slashes turned into hyphens. A repeat run verifies an existing folder again and checks every file now in the worktree is covered; new files go to a second folder with suffix `-r2` then `-r3`; an existing folder is never overwritten. Before copying, a names-only secret check scans the files to be saved for token-shaped content and secret-looking file names; a hit stops the save with "possible secret in <file name>" and never prints or logs the matched value. The step reads and copies and never edits anything inside the worktree. The function returns the verified folder path and the set of saved paths so Task 11 can register them with the runner.

Acceptance criteria:
- Run against a throwaway worktree and a local bare repository, the folder appears at `<repo>/<author>/<date>_pr<N>_<subject>/` with `MANIFEST.md` (all fields above), `files/`, `ignored.tar.gz` and `saved-paths.txt`, and `VERIFIED <folder> files=<n>` is returned.
- A refused push (three times), a folder that differs after the push and a failed copy each return a failure reason beginning "saved copy failed" and leave the worktree untouched.
- With the part size lowered by the test, an ignored archive is split into parts that join back to the same bytes; a second run with new files writes `-r2` and the first folder is byte-identical afterwards.
- A file containing a token-shaped string stops the save, the message names the file, and the string itself appears nowhere in the output, the log or the evidence clone.

## Task 10: Write the archive step tests

Depends on: Task 9, Task 7

Create `tests/worktree_cleanup/test_archive.py` covering the archive group of source section 9: a worktree with untracked and ignored `.dev/` files produces the folder at `<repo>/<author>/<date>_pr<N>_<subject>/` with `MANIFEST.md` carrying every field, `files/` and `ignored.tar.gz`, and `VERIFIED` is printed before anything else would happen; a push refused three times, a folder that differs from the remote after the push, and a failed copy each show "saved copy failed" with the cause; an ignored archive larger than the part size is split into parts that join back to the same bytes (lower the module constant to a few kilobytes); an existing folder is never overwritten and a repeat run verifies it and writes `-r2` when new files appeared; two clones pushing different folders at the same time both end up on `origin/main` after the rebase and retry (two clones of the local bare repository, the second pushing after the first); a possible secret in a file to be saved keeps the worktree, names the file and never prints the value. Build any token-shaped test string at run time from two pieces (for example a prefix plus repeated characters) so no secret-looking literal is committed, and assert the assembled value is absent from captured output and from every file of the evidence clone.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_archive.py -v` passes using only `tmp_path` repositories and local bare remotes.
- Each of the six bullets above has at least one test, and the secret test asserts the value never appears in stdout, stderr, the log or the clone.
- No test in the file pushes to a network remote or reads a credential file.

## Phase 5: Removal pipeline and the four verbs

## Task 11: Implement the removal pipeline: terminal close, second check, exact-path clear, removal, branch, read back

Depends on: Task 9

In `scripts/worktree_cleanup.py` implement steps 1 to 7 of source section 3 ("What a removal is, in order") for one removable worktree under `--apply`, each step failing closed with the reason shown: save (the archive step of Task 9 when the worktree holds untracked or ignored `.dev/` files; without `VERIFIED` stop); close the Orca terminals only when it has any, only after every other rule passed and the save is verified, with `orca terminal close --worktree id:<id> --all` (an `unverifiable` or failed close keeps the worktree: "Orca terminal close not confirmed"); the second check after the close, re-reading `git status`, the untracked and ignored lists, HEAD against the pull request's head and the process scan, where any change since the save keeps it ("changed since the terminals were closed") and any process still inside keeps it ("a process is still inside after its Orca terminals were closed"); clear exactly the saved files by registering the verified `saved-paths.txt` paths with the `Runner` and running `git clean -f -x --` on those paths through `xargs -0` with `GIT_LITERAL_PATHSPECS=1`, never a path outside the list, never `-d`, never a tracked file; remove the worktree (`orca worktree rm --worktree id:<id>` without `--force` when Orca lists it, else `git worktree remove <path>` without `--force`, run from the repo's main checkout and never from inside the worktree, and a refusal keeps it with the refusal text); remove the local branch with `git branch -d` only (check first whether Orca already removed it; a "not fully merged" refusal after a squash merge is reported as "branch kept", not an error); then read back that the folder is gone and that neither `git worktree list` nor `orca worktree list` shows it. A worktree with tracked edits or a commit after the pull request is never archived, never has terminals closed and is never cleared (decision 2). In a dry run none of these steps runs.

Acceptance criteria:
- The order of recorded commands in a test run is: archive commands, `orca terminal close`, the re-check reads, `xargs -0 git clean -f -x --`, the removal, `git branch -d`, the read-back reads.
- `git clean` is issued only after `VERIFIED` and only with paths from `saved-paths.txt`; a path not in the list is refused by the runner before any process starts.
- No recorded command contains `--force`, `-D`, `rm`, `worktree prune`, a remote delete or a push outside the evidence clone.
- A worktree with a tracked edit, or a commit after the pull request, produces no archive, no terminal close and no clear.

## Task 12: Implement the four verbs, the per-repo lock, the output files and the exit codes

Depends on: Task 11

In `scripts/worktree_cleanup.py` fill in the verb bodies: `list` prints the table for every worktree of every repo of ours and never removes; `archive <worktree>` runs only the archive step of Task 9 on one worktree (its help text states that the patch-and-bundle save of tracked edits or later commits mentioned in source section 7 is not built); `retire <worktree>` removes one worktree under `--apply` after the archive step when needed, must be run from outside the worktree, accepts a path or a unique folder name and exits 64 for an unknown or ambiguous selector or a worktree that is not removable; `prune` runs the same decision code on all worktrees in the same run and, with `--apply` only, removes the removable ones through Task 11, while without `--apply` it prints the table and writes `<out dir>/prune-<UTC timestamp>.md` and the `.json` of the same rows. One lock file per repo in the output folder using `fcntl.flock` with a non-blocking exclusive lock and no file deletion: a run that cannot take a repo's lock skips that repo and says "another run holds the lock". Print one summary (how many removed, kept and failed, and the first reason of each kept group). Exit codes: 0 when the run completed, 64 for a usage error or a `retire` of a worktree that is not removable, 69 when a lookup or a removal failed (the table still shows what happened). A second run after a removal finds nothing more to do. Folders that are not git worktrees of our repos never appear. No output names an agent or a model.

Acceptance criteria:
- `list` and `prune` without `--apply` record no removal command; with `--apply`, only rows marked removable are processed.
- Two runs started against the same repo cannot both remove the same worktree (the second reports the lock); a run after a successful removal reports nothing to do.
- The three exit codes behave as described (0 completed, 64 usage or non-removable `retire`, 69 lookup or removal failure) and the summary line carries the three counts.
- `prune` writes both output files under `--out` and writes nothing inside any worktree.

## Task 13: Write the pipeline, terminal, safety and output tests

Depends on: Task 12, Task 8

Create `tests/worktree_cleanup/test_pipeline.py` and `tests/worktree_cleanup/test_safety.py`. Pipeline file: decision 3 (a worktree that passes every rule with Orca terminals open and a process inside is removed under `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed and the second check finds nothing changed and no process inside; in a dry run the table says "its Orca terminals will be closed first" and no terminal is closed); a terminal close that is `unverifiable` or fails keeps the worktree; a process still inside after the close keeps it; a change appearing between the save and the close (a new commit, a tracked edit, an untracked file outside `.dev/`) keeps it; decision 1 (exactly the paths of `saved-paths.txt` are cleared including a name with a space, and an unlisted untracked file, an unlisted ignored file and every tracked file survive, and a path not in the list is refused by the runner); decision 2 (a merged worktree with a tracked edit or a later commit is kept, nothing cleared, no terminal closed, nothing archived by `prune`); the removed worktree's branch is removed with `-d` and a squash-merge refusal reports "branch kept"; a second run finds nothing more to do; two runs at once do not both remove the same worktree; folders that are not git worktrees of our repos never appear in the table and are never touched. Safety file: a recorder test runs every verb on every branch through the recording runner and fails if any recorded command is `--force` on a removal, `git branch -D`, `rm`, `git worktree prune`, a push to anything but the evidence remote, a remote branch delete, a `git clean` that is not `-f -x --` followed only by lines of that worktree's `saved-paths.txt` issued after `VERIFIED`, or an `orca terminal close` for a worktree before every other rule passed and its save was verified; every `gh` call carries `--repo <owner>/<repo>`; dry run is the default and the recorded commands contain no removal; `--apply` removes only rows marked removable; no output (table, summary, log, JSON) names an agent or a model (a test greps for a fixed list of such words); no secret is printed or written and the script never opens `~/.config/gh/hosts.yml` or `~/.env` (patch `open` and `Path.read_text` to fail on those paths); `GH_TOKEN` is read from the environment only; each refusal shape of `Runner.check_allowed` from Task 2 raises.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_pipeline.py tests/worktree_cleanup/test_safety.py -v` passes.
- Mutation check by hand: removing the `VERIFIED` precondition, or letting a path outside the list through, makes a safety test fail; removing the second check makes a pipeline test fail.
- The recorder test inspects the commands of every verb (`list`, `archive`, `retire`, `prune`, with and without `--apply`), not only `prune`.
- The tests together with Tasks 8 and 10 cover every case of source section 9 (about 35 cases in four groups).

## Phase 6: The command and its registrations

## Task 14: Add the `/sc:worktrees` command file and its static test

Depends on: Task 12

Create `src/superclaude/commands/worktrees.md`, modelled on `src/superclaude/commands/closeout.md` (frontmatter with name `worktrees`, version, description, category `workflow`, complexity, `mcp-servers: []`, personas, and `argument-hint: "<list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]"`; sections Triggers, Usage, Options, STOP rules, Examples, Outputs, Boundaries). It is a thin command and a command, not a skill (source section 5): it runs `uv run --no-project python scripts/worktree_cleanup.py <verb> ...` from the top of the current git checkout (`git rev-parse --show-toplevel`) and prints the table; no skill is activated. Decision made by this plan because `scripts/` does not install with the command: when `scripts/worktree_cleanup.py` does not exist at the top of the current checkout, the command stops, runs nothing and prints "`/sc:worktrees` runs only inside an IronClaude checkout that has `scripts/worktree_cleanup.py`". It passes `--apply` only when the person typed it, never adds `--apply` or any force flag, and says in Boundaries that it never merges, never pushes to a source repo, that removal needs `--apply`, and (as `src/superclaude/commands/sweep.md` does in its line 18) that it is for a person only and is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`. Plain English, no em or en dashes, no `src/superclaude/...` path in the text (the repository rule for installed primitives). Then create `tests/commands/test_worktrees_command.py` modelled on `tests/commands/test_closeout_command.py` (static tests of the command file text).

Acceptance criteria:
- `tests/commands/test_worktrees_command.py` passes and asserts: frontmatter fields and the exact `argument-hint`, the four verbs and the `--apply` and `--out` options in the Options table, the outside-a-checkout stop sentence, that none of `--force`, `--yes` or `--unattended` appears as an option, that no `src/superclaude/` path appears, and that the file has no em or en dash.
- `make sync-dev` copies the command to its dev copy and `make verify-sync` is clean for it (the dev copy is gitignored and is not staged).
- `superclaude install`'s glob in `src/superclaude/cli/install_commands.py` picks the file up with no list edit (no change to that file).

## Task 15: Register the command in the routing guide and its pinned tests

Depends on: Task 14

Edit `src/superclaude/core/HOW-WE-WORK.md`: add a `/sc:worktrees` row at the end of the table between the `<!-- other-commands:v1 -->` markers (after `/sc:sweep`), stating when to use it (remove merged worktrees whose pull request is merged, issue closed and idle 7 days, `list` by default, `--apply` to remove, saves `.dev` files to the evidence repo first, for a person, never a worker) and carrying the one line that answers item 4 of #289 ("when to remove a worktree after its pull request merges": after the pull request merges and every rule of the cleanup holds). Edit `tests/core/test_how_we_work_routing_table.py`: add `"sc:worktrees"` to `_OTHER_COMMANDS` (line 27). Edit `tests/recommend/test_routing_refresh.py`: add `"worktrees"` to `_POST_REFRESH_ADDITIONS` (line 36), and extend the comment above it with "and issue #687 adds /sc:worktrees". Then copy the whole guide byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; the level-table block between `<!-- level-table:v1 -->` and `<!-- /level-table -->` is unchanged, so `src/superclaude/core/CLAUDE.md` is not edited (confirm the block is identical in both).

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py -v` passes.
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- The new row contains the `#289` item 4 answer and the words "never a worker".

## Task 16: Put `/sc:worktrees` on the never-as-worker list

Depends on: Task 14

Decision made by this plan: the command closes terminals and removes work, so no worker is ever dispatched to it. Edit the never-as-worker sentence so it reads "... `/sc:pm`, `/sc:sweep`, `/sc:swarm-wizard` and `/sc:worktrees`, plus `/sc:pr-submit` ..." in `src/superclaude/core/WORKER-CONTRACT.md` (line 23) and in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (line 982), and make the same change to the pinned phrase in `tests/skills/test_worker_contract.py` (the `never-as-worker` entry at line 89, which today ends "`/sc:sweep` and " followed by "`/sc:swarm-wizard`...") and add `"/sc:worktrees"` to the `NEVER_AS_WORKER` tuple at line 474. Read `src/superclaude/core/WORKER-CONTRACT.md` line 290 and the other mentions of the list in the developer guide and update any that enumerate the commands. `/sc:worktrees` gets no `## Unattended mode` section (the test `_check_no_unattended_sections` at line 830 requires only the named commands to have one).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -v` passes, including the parametrized never-as-worker check for `/sc:worktrees`.
- The sentence is identical in `WORKER-CONTRACT.md`, the developer guide and the pinned phrase of the test, and `src/superclaude/commands/worktrees.md` has no `## Unattended mode` heading.
- `make sync-dev` and `make verify-sync` are clean.

## Task 17: Document the command in the user guide and the changelog

Depends on: Task 14

Edit `docs/user-guide/commands.md`: add a summary-table row for `/sc:worktrees` next to the `/sc:closeout` and `/sc:sweep` rows (near line 103, columns as the neighbouring rows: link, one-line purpose, file `worktrees.md`, whether it writes: "Yes with `--apply` (removes worktrees, closes their Orca terminals, writes to the evidence repo); report only without it") and a section `### /sc:worktrees - Remove Merged Worktrees` modelled on the `/sc:closeout` section (near line 373): when to use, usage line, options table (`list`, `archive`, `retire`, `prune`, `--apply`, `--out`), the eight rules in plain English, what a removal does in order, the environment names (`GH_TOKEN`, `RUN_EVIDENCE_REPO`, `RUN_EVIDENCE_DIR`, `WORKTREE_CLEANUP_IDLE_DAYS`; no values), exit codes 0, 64 and 69, the opt-in daily automation (definition only, switched off, first week report only), and the stop outside an IronClaude checkout. Edit `CHANGELOG.md` under `## [Unreleased]`: add `### New command: /sc:worktrees and scripts/worktree_cleanup.py (issue 687)` with a short plain-English entry that also names Jay Wedgeworth's adapted rules under Apache-2.0 and the evidence repo, and states that the Orca automation is written but not switched on.

Acceptance criteria:
- The new table row and section exist in `docs/user-guide/commands.md` and the anchor in the row matches the section heading.
- The `CHANGELOG.md` entry sits under `## [Unreleased]` and mentions the switched-off automation, the Apache-2.0 notice and the evidence repo by name.
- No em or en dash in either added text; `uv run pytest tests -k "docs or commands" -q` shows no new failure from these files.

## Phase 7: The switched-off automation and the notices

## Task 18: Write the automation definition (switched off) and its test

Depends on: Task 12

Create `scripts/worktree_cleanup_orca_automation.md`, modelled on `scripts/merged_pr_log_orca_automation.md` (it has the lines `Name:`, `Trigger (UTC):`, `Status:`, then "Why the name and the trigger are what they are", "Command to run (precheck shape)", "Environment variables (names only; no value belongs in any file)", "Human steps, in order" and "When a run fails"). Name: `worktree-cleanup-daily` (never starts with `coordinator-`). Trigger (UTC): `0 8 * * *`, with the note that this is 2:00 AM Central in winter and 3:00 AM in daylight saving time, and that whether `--timezone America/Chicago` can hold 2:00 AM all year is UNVERIFIED (source section 11, item 8). Status: `written, not switched on`. The command is the precheck shape of source section 5: `bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv; [ -f ~/.env ] && . ~/.env; set +a; cd <checkout> && setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune --out <out dir> >> <out dir>/run.log 2>&1 < /dev/null &'; exit 1`, with no `--apply` in it, and the text says the skipped run shows as `skipped_precheck` and that this is UNVERIFIED in this Orca build (item 6). Add the rollout ladder (switched on by each workspace's owner; first week report only; read the tables; then the owner edits the automation to add `--apply`; the worker does none of this), the environment names without values, and "When a run fails". Create `tests/worktree_cleanup/test_automation_definition.py` asserting these fields, that the command contains `prune` and no `--apply`, ends with `exit 1`, that the name does not start with `coordinator-`, that no token value appears, and that there is no em or en dash.

Acceptance criteria:
- `scripts/worktree_cleanup_orca_automation.md` exists with Name `worktree-cleanup-daily`, Trigger `0 8 * * *`, Status `written, not switched on`, and the command above.
- `uv run pytest tests/worktree_cleanup/test_automation_definition.py -v` passes.
- No Orca automation was created, run or switched on to produce the file (definition text only).

## Task 19: Write the provenance file, the NOTICE entry and the evidence-repo pointer text

Depends on: Task 12

Create `scripts/worktree_cleanup_PROVENANCE.md`, modelled on `src/superclaude/skills/sc-closeout-protocol/PROVENANCE.md` (sections: Source, Notices in the adopted files, What changed, What this version adds, Drift review). Its "What changed" table has one row for each of the 14 rows of the table in source section 12 (kept as is, changed or dropped, with the spec's reason). The source table lists `scripts/fleet_lanes/retire.py`, `docs/protocols/lane-map.md` and `scripts/disk-janitor.sh` with line counts from source section 12 and writes "not recorded" for blob and commit pins, because the spec records none and no pin may be invented; `branch-landed.sh` is listed as reused through `/sc:closeout`, not adopted again. It says the Apache License text is at `src/superclaude/skills/sc-closeout-protocol/LICENSE` and the upstream repository has no NOTICE file. Edit `NOTICE` (it lists `sc-closeout-protocol` as component 2 near line 30) to add the next numbered component for `scripts/worktree_cleanup.py`, naming Jay Wedgeworth, the three files whose rules were adapted, Apache-2.0 and the provenance file. Write `./artifacts/run-evidence-pointer.md` in this package with the proposed text for `tools/archive-workspace.sh` (a short pointer to `scripts/worktree_cleanup.py archive`) and the `README.md` note for `IronbellyOrg/run-evidence`, headed "not applied: a separate change in that repo, made by the owner when this merges".

Acceptance criteria:
- `scripts/worktree_cleanup_PROVENANCE.md` has 14 rows in its changed-table, each labelled with one of the three words, and no invented commit or blob pin.
- `NOTICE` has the new component entry and still lists components 1 and 2 unchanged.
- `./artifacts/run-evidence-pointer.md` exists and states it was not applied; no file of the evidence repo was changed or pushed.
- The notice block at the top of `scripts/worktree_cleanup.py` (Task 2) points at the file name used here.

## Phase 8: Dry run in the real workspace

## Task 20: Capture the dry run of the real workspace and compare the counts

Depends on: Task 12, Task 19

Run the finished script against this workspace as a dry run only: `uv run --no-project python scripts/worktree_cleanup.py list` and `uv run --no-project python scripts/worktree_cleanup.py prune --out ./artifacts/dry-run` (never `--apply`; the output folder is inside this package, not inside any worktree being judged; the script's own worktree is on the name list as "this is where the script runs"). Save the printed table and the `prune-<UTC timestamp>.md` and `.json` under `./artifacts/dry-run/` and write `./artifacts/dry-run-report.md` with: the command lines used, that `--apply` was never passed, the count of non-main worktrees of the IronClaude repo from `git worktree list --porcelain` against the number of IronClaude rows in the table, the count of rows with "in Orca" yes against the Orca list count read by the script (this session's launch guard may block typing an Orca command directly; if it does, record that and compare only through the script's own JSON), and the rows marked `removable` listed by folder and reason with a note on how they compare with the 13 of source section 2 as of the day (UNVERIFIED differences are expected and recorded as such, not forced to match). Confirm in the report that a worktree with a commit after its pull request's head, one whose issue is open and one with an ignored environment file (whichever the real data holds, else say none exists) are kept with the right reason, and that a worktree with only an open Orca terminal shows "its Orca terminals will be closed first" if one exists.

Acceptance criteria:
- `./artifacts/dry-run-report.md` exists and states that only `list` and `prune` without `--apply` were run, and the recorded command list in the `.json` output contains no removal, no terminal close, no archive and no push.
- The report gives the git count and the table count for the IronClaude repo, with any difference explained or marked UNVERIFIED.
- Every worktree of the real workspace is still present after the run (`git worktree list --porcelain` has the same entries before and after).
- No real worktree, file or Orca object was removed, moved, cleared, created or switched on to produce the report.
- The report records the results of the regression gate of source section 9 run on the finished change: the full test suite (`uv run pytest`), `make lint`, `make verify-sync`, and a scan of every new file for em and en dashes; any failure is stated, not hidden.
`````

## Coverage slice

All 82 inferred rows (no parsed rows exist). Full matrix: .dev/reflect/pre-TASK-WF-specWorktreeClea-20261120174527/coverage-matrix.md

| id | cite | matched | method | ratio | quote |
|---|---|---|---|---|---|
| INF-001 | source.md:16 | Task 11 | containment | 0.769 | It never uses `--force` on a worktree removal, never `git branch -D`, never `rm`, never pushes to a source repo and never deletes a remote branch. |
| INF-002 | source.md:16 | Task 1 | containment | 0.75 | Its only push goes to the evidence repo. |
| INF-003 | source.md:16 | Task 8 | containment | 0.8 | Tracked edits and commits made after the pull request always keep the worktree. |
| INF-004 | source.md:78 | Task 2 | containment | 0.8 | Dry run is the default for every verb that could remove something; `--apply` is the only way to remove. |
| INF-005 | source.md:82 | Task 6 | containment | 0.833 | Prints a table of every git worktree of every repo of ours, one decision (keep or removable) and one reason per row. |
| INF-006 | source.md:83 | Task 9 | containment | 0.909 | Runs only the evidence step of section 7 on one worktree: copy, push, check against GitHub. |
| INF-007 | source.md:84 | Task 15 | containment | 0.615 | Removes one worktree whose work is safe, run from outside it, usually right after its pull request merges. |
| INF-008 | source.md:85 | Task 12 | containment | 1.0 | Runs the same decision on all worktrees and removes the removable ones. |
| INF-009 | source.md:87 | Task 6 | containment | 0.87 | One row per worktree: repo, folder, branch, in Orca (yes or no), pull request and state, issue(s) and state, idle days, size, saved copy (none needed, saved and checked, or failed), decision and reason. |
| INF-010 | source.md:89 | Task 11 | containment | 0.727 | Each step fails closed: if any step cannot be completed or read back, the worktree is kept and the reason is shown. |
| INF-011 | source.md:91 | Task 13 | containment | 0.625 | Without a `VERIFIED` result the worktree is kept and nothing below happens. |
| INF-012 | source.md:92 | Task 11 | containment | 1.0 | An `unverifiable` or failed close keeps the worktree. |
| INF-013 | source.md:93 | Task 11 | containment | 1.0 | Any change since the save and any process still inside the worktree keeps it. |
| INF-014 | source.md:94 | Task 11 | containment | 0.778 | Never a path that is not in the manifest, never `-d` on a folder as a whole, never a tracked file (decision 2). |
| INF-015 | source.md:95 | Task 11 | containment | 1.0 | For a worktree Orca lists: `orca worktree rm --worktree id:<id>` without `--force`. |
| INF-016 | source.md:95 | Task 13 | containment | 0.833 | For a worktree Orca does not list (the 13 removable ones today): `git worktree remove <path>` without `--force`. |
| INF-017 | source.md:96 | Task 2 | containment | 1.0 | **Remove the local branch with `git branch -d`, never `-D`.** |
| INF-018 | source.md:97 | Task 11 | containment | 0.778 | Confirm the folder is gone, `git worktree list` no longer shows it and `orca worktree list` no longer shows it. |
| INF-019 | source.md:99 | Task 11 | containment | 1.0 | In a dry run (no `--apply`) steps 1 to 7 are not run |
| INF-020 | source.md:102 | Task 4 | containment | 0.824 | a repo whose `origin` belongs to IronbellyOrg or IronbellyGroup, found from `orca repo list` plus `git worktree list` in each repo (so worktrees Orca does not list are covered), wherever they sit |
| INF-021 | source.md:105 | Task 2 | containment | 0.778 | As a second guard the script skips any worktree whose folder name starts with `orca-port-`, `orca-recipe-` or `orca-pristine-`, or is `orca-old-patched`, even if git lists it. |
| INF-022 | source.md:112 | Task 18 | containment | 0.733 | One Orca automation per Coder workspace, once a day at 2:00 AM Central (08:00 UTC), switched on by that workspace's owner. |
| INF-023 | source.md:112 | Task 18 | containment | 1.0 | The name must not start with `coordinator-`. |
| INF-024 | source.md:116 | Task 18 | containment | 0.6 | The cron string is `0 8 * * *` (UTC). |
| INF-025 | source.md:124 | Task 2 | containment | 0.667 | Python standard library only, no model call anywhere. |
| INF-026 | source.md:125 | none | none | 0.375 | It is a command, not a skill: a skill installs for everyone and would break the opt-in schedule. |
| INF-027 | source.md:126 | Task 18 | containment | 1.0 | The automation definition, written and switched off, modelled on `scripts/merged_pr_log_orca_automation.md`. |
| INF-028 | source.md:131 | none | none | 0.417 | a precheck command that exits non-zero makes Orca skip the run and start no agent session. |
| INF-029 | source.md:137 | Task 18 | containment | 0.944 | Name: `worktree-cleanup-daily`. Trigger: `0 8 * * *` (UTC; 2:00 AM Central in winter, decision 11). Status: written, not switched on. |
| INF-030 | source.md:144 | Task 13 | containment | 1.0 | `GH_TOKEN` (never read from a file by the script; it is passed to `gh` and to `git push` through the environment). |
| INF-031 | source.md:146 | Task 12 | containment | 0.944 | One lock file per repo in the output folder, so two runs cannot remove the same worktree twice; a second run after a removal finds nothing more to do. |
| INF-032 | source.md:148 | Task 12 | containment | 1.0 | Each run writes `<out dir>/prune-<UTC timestamp>.md` (the table) and a `.json` of the same rows |
| INF-033 | source.md:148 | Task 12 | containment | 0.821 | Exit codes follow Jay's: 0 means the run completed (some worktrees may be kept; read the table), 64 means a usage error or a `retire` of a worktree that is not removable, 69 means a lookup or a removal failed (the table still shows what happened). |
| INF-034 | source.md:148 | Task 12 | containment | 1.0 | No output names an agent or a model. |
| INF-035 | source.md:150 | none | none | 0.556 | Clay switches it on in his workspace and for the first week it only writes the table (no `--apply`) |
| INF-036 | source.md:154 | Task 6 | containment | 0.667 | A worktree is removed only when ALL eight rules hold. |
| INF-037 | source.md:154 | Task 1 | containment | 0.889 | Every rule fails closed: if the script cannot tell, it keeps the worktree. |
| INF-038 | source.md:158 | Task 12 | containment | 0.667 | It is a linked worktree of one of our repos that this run may touch. |
| INF-039 | source.md:159 | Task 5 | containment | 1.0 | Its own pull request is MERGED. |
| INF-040 | source.md:160 | Task 9 | containment | 0.8 | Nothing was added after the pull request. |
| INF-041 | source.md:161 | Task 6 | containment | 1.0 | The issue it was for is CLOSED. |
| INF-042 | source.md:162 | none | none | 0.5 | Nothing unsaved is in it. |
| INF-043 | source.md:163 | Task 13 | containment | 0.6 | Nothing but its own Orca terminals is using it. |
| INF-044 | source.md:164 | Task 8 | containment | 1.0 | It has been idle for at least 7 days and was not created in the last 7 days. |
| INF-045 | source.md:165 | none | none | 0.5 | It is not pinned and nobody asked to keep it. |
| INF-046 | source.md:170 | Task 11 | containment | 0.867 | Decision 1 allows `git clean -f -x` for the exact paths saved and verified in the evidence repo and for nothing else |
| INF-047 | source.md:171 | Task 11 | containment | 0.909 | Close an Orca terminal of a worktree that has not passed every other rule and whose save is not verified. |
| INF-048 | source.md:173 | none | none | 0.562 | Run `git worktree prune`, because a missing folder can mean a disk is not mounted (Jay's guard); it reports such a worktree and leaves it. |
| INF-049 | source.md:175 | Task 11 | containment | 0.75 | Create, move or change a file inside a worktree it keeps (the archive step reads and copies; it never edits). |
| INF-050 | source.md:176 | Task 12 | containment | 0.75 | Read a credential from a file, print a credential, or name an agent or a model in any output. |
| INF-051 | source.md:186 | Task 9 | containment | 0.833 | Needs the merged pull request of rule 2. Without one it refuses (nothing is saved for unmerged work). |
| INF-052 | source.md:188 | Task 9 | containment | 0.929 | Pack the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of 85 MB when larger |
| INF-053 | source.md:188 | Task 9 | containment | 0.857 | Write `saved-paths.txt`, one exact path per line |
| INF-054 | source.md:188 | Task 9 | containment | 0.96 | Write `MANIFEST.md`: source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, and a SHA-256 of each archive file and of `saved-paths.txt`. |
| INF-055 | source.md:189 | Task 9 | containment | 0.889 | Commit in the evidence repo with the message `archive(<repo>): <date> pr<N> <subject>`. |
| INF-056 | source.md:190 | Task 9 | containment | 1.0 | If the push is refused, repeat from the fetch up to 3 times |
| INF-057 | source.md:191 | Task 6 | containment | 0.8 | Print `VERIFIED <folder> files=<n>`. |
| INF-058 | source.md:192 | none | none | 0.5 | It never overwrites a folder. |
| INF-059 | source.md:194 | Task 9 | containment | 1.0 | `<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/`. |
| INF-060 | source.md:212 | Task 6 | containment | 0.667 | after the save is pushed and verified against GitHub, do whatever is needed to make the worktree removable, for the saved untracked and ignored files only. |
| INF-061 | source.md:235 | Task 9 | containment | 0.667 | YES: a names-only secret check before pushing. |
| INF-062 | source.md:244 | Task 8 | containment | 0.625 | They never touch a real worktree. Each case must fail if its rule is removed. |
| INF-063 | source.md:249 | Task 13 | containment | 1.0 | Decision 3: a worktree that passes every rule and has Orca terminals open and a process inside is removed in `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed |
| INF-064 | source.md:251 | Task 5 | containment | 0.909 | A squash-merged pull request whose commits are not on the base is judged landed from pull request state, not ancestry. |
| INF-065 | source.md:252 | Task 8 | containment | 1.0 | A pull request that is merged but whose branch was later reused for new commits keeps the worktree. |
| INF-066 | source.md:255 | Task 2 | containment | 1.0 | A test records every command the script runs, in every verb and every branch |
| INF-067 | source.md:257 | Task 12 | containment | 0.933 | A second run after a removal finds nothing more to do; two runs at once do not both remove the same worktree (one lock per repo). |
| INF-068 | source.md:259 | Task 13 | containment | 1.0 | No output names an agent or a model (a test greps the table, the summary and the log). |
| INF-069 | source.md:264 | Task 9 | containment | 1.0 | An ignored archive larger than 85 MB is split into parts that join back to the same bytes. |
| INF-070 | source.md:266 | Task 10 | containment | 1.0 | Two clones pushing different folders at the same time both end up on `origin/main` after the rebase and retry. |
| INF-071 | source.md:268 | Task 13 | containment | 0.917 | Decision 1: exactly the paths in `saved-paths.txt` are cleared (including a name with a space) and nothing else |
| INF-072 | source.md:269 | Task 11 | containment | 0.941 | Decision 2: a merged worktree with a tracked edit or a commit after the pull request is kept, nothing is cleared, no terminal is closed and nothing is archived by `prune`. |
| INF-073 | source.md:271 | Task 7 | containment | 1.0 | `git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file, and removes one that holds only ignored files |
| INF-074 | source.md:274 | Task 20 | containment | 0.846 | A dry run in Clay's workspace prints a table whose counts match `git worktree list` |
| INF-075 | source.md:275 | Task 19 | containment | 0.769 | Jay's files that are adapted keep his Apache-2.0 notice and say what was changed |
| INF-076 | source.md:276 | Task 20 | containment | 0.643 | The regression gate passes: the full test suite, `make lint` and the sync checks that `/sc:pr-submit` runs. |
| INF-077 | source.md:276 | Task 17 | containment | 0.8 | No em or en dashes in new files. |
| INF-078 | source.md:373 | Task 1 | containment | 0.7 | on throwaway worktrees only, and write the findings to `.dev/research/worktree-cleanup-proofs.md`. |
| INF-079 | source.md:375 | none | none | 0.556 | registered where the repo lists commands. Reuse the landed check of #668. |
| INF-080 | source.md:376 | Task 2 | containment | 1.0 | A provenance block with Jay's Apache-2.0 notice at the top of the script. |
| INF-081 | source.md:377 | Task 19 | containment | 0.667 | **Retire the manual tool** in the evidence repo (its `tools/archive-workspace.sh` becomes a pointer to the script) |
| INF-082 | source.md:379 | Task 1 | containment | 0.714 | **Pull request** with `/sc:pr-submit --monitor 3`. |
