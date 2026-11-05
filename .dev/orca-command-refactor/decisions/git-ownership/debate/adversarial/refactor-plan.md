# Refactoring Plan: Merge into Base (Variant 5, option E)

## Overview
- Base: Variant 5 (`variant-5-original.md`, option E: sole-writer workers may commit locally; the coordinator owns every outward action). Selected in `base-selection.md` by the level-1 tiebreaker.
- Incorporating strengths from: V1 (A), V2 (B), V3 (C), V4 (D), Advocate E's Round 2 corrections, the Round 2.5 invariant probe, and CR-01 (`.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md`).
- Planned changes: 18 (5 of them mandatory, one per HIGH UNADDRESSED invariant).
- Risk level: Medium overall. Most changes add conditions to existing rows; Changes 6, 9 and 10 alter a stated rule, and Change 9 runs against the spec's current D4 recommendation.
- Citation keys: `V<n>:L` = line L of `variant-<n>-original.md`; `SPEC` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `EVAL` = `.dev/orca-command-refactor/review/issue-326-evaluation.md`; `CR01` = the CR-01 file above; `implement/` = `src/superclaude/skills/sc-implement-protocol/`; `pr-submit/` = `src/superclaude/skills/sc-pr-submit-protocol/`. Every repo path:line below was re-read on 2026-11-02 after merged PR #343.

## Fixed constraints (applied as given, not debated)
- **FC-1. Worktrees are created by Orca at Orca's default paths, never under `.dev/worktrees/`.** This overrides V5:11 (`CLAUDE.md:299-302`), the debate's C2 rule (`debate-transcript.md:1196`), EVAL F2's `.dev/worktrees/<run>-<n>/` (`EVAL:52`) and `SPEC:235`. The user resolved this on 2026-11-02 (`CR01:41`); the repo-wide refactor of the `.dev/worktrees/` rule is planned separately and is out of this plan's scope.
- **FC-2. SuperClaude upstream is never pushed to or interacted with; every GitHub action targets `IronbellyOrg/IronClaude`.** Repo rule `CLAUDE.md:41-47`; pr-submit already resolves the target from `origin` and refuses a misrouted PR URL (`pr-submit/SKILL.md:267`). Orca records this repo's project as `github:superclaude-org/superclaude_framework`, so Orca's issue and PR linking is not used until that identity resolves to the fork (`CR01:45`).
- **FC-3. Merged PR #343 changed review rules.** Only blocking findings fail a review, and review loops cap at 2 fix cycles. Checked effect on git ownership: in `/sc:implement`, #343 changed only the convergence and repair wording (`implement/refs/retry.md:147,149,193`: at most 1 repair per attempt and 2 per task; reverts at most 3, adviser route only) and two wording lines (`implement/refs/qa.md`, `implement/refs/ledger.md`); the git mechanics the debate relied on are unchanged: Q0 private-index snapshot (`implement/SKILL.md:111`), pin refs (`implement/SKILL.md:113,116`), the HEAD-not-moved check (`implement/refs/retry.md:41`), the revert domain and its `.dev/` exclusion (`implement/refs/retry.md:201-207`) and the restore-or-delete step (`implement/refs/retry.md:220`). pr-submit's `--max-rounds` default is 2 with a hard cap of 5 (`src/superclaude/commands/pr-submit.md:47`).
- **FC-4. CR-01 is the placement model.** CR-01's feature worktree with conditional child worktrees (`CR01:14-24`) is E's placement rule (B's P1 plus C's M1, `CR01:21`). The merge adopts it and states two differences (Change 7).

## Planned Changes

### Change 1: Worktree creation and placement by Orca, feature worktree plus conditional children (FC-1, FC-4, CR-01)
- **Source**: CR-01 sections 2 and 5.1 (`CR01:14-24,41`); invariant probe INV-028 (`invariant-probe.md:36`).
- **Target**: Base, table row 2 (V5:11) (replace).
- **Rationale**: Fixed constraint FC-1. INV-028 (MEDIUM) showed V5:11 and the debate's C2 rule clash with how Orca creates worktrees: `worker-start` has no path option, and a raw `git worktree add` worktree skips Orca's setup.
- **Integration point**: Row 2 becomes: the coordinator creates every worktree through Orca at Orca's default location: one feature worktree per feature (the coordinator runs there), and a child worktree per worker with `worker-start --worktree new-child --base-branch <feature branch> --setup run` only when a Change 7 trigger applies. No worker is dispatched into a child until its setup has succeeded (`CR01:24`). Never raw `git worktree add`, never `.dev/worktrees/`.
- **Risk**: Medium. Whether Orca's setup hook runs `make sync-dev`, creates the Python environment and indexes the code graph is UNVERIFIED (`CR01:42`).

### Change 2: Merge-back and removal of child worktrees, with a fuller removal guard (CR-01, INV-004)
- **Source**: CR-01 section 2.4 and open questions 3-4 (`CR01:23,43-44`); V5:11 F3 guard; INV-004 (`invariant-probe.md:12`).
- **Target**: Base, table row 2 (V5:11) (append) and a new row "Merge a child branch into the feature branch".
- **Rationale**: V5 names removal but not merge-back. INV-004 (MEDIUM): a worktree can hold uncommitted state the run still needs (pr-submit `fix_commit_failed` leaves edits in the tree, `pr-submit/SKILL.md:318`; a halted implement run keeps its ledger and retries there).
- **Integration point**: After a child's result is admitted (`SPEC:81-85`), the coordinator merges the child branch into the feature branch under Change 4's conditions, then removes the child with `orca worktree rm` and deletes its branch; a discarded experiment is removed without merging. A merge conflict stops and is reported, never auto-resolved. Removal guard: never remove a worktree or branch with unmerged commits, an open PR, uncommitted changes, an unfinished `/sc:implement` ledger, or a contract or report directory not yet read, without the user's instruction. The feature branch is merged into a child only between Tasks, never while a worker runs in it.
- **Risk**: Low (adds conditions).

### Change 3: Outward actions row: fork target, PR-head position, PR owner, pr-submit cap (FC-2, FC-3, M1, X-004)
- **Source**: C's M1 and Advocate E's N5 (`round2-advocate-e.md:43`; `debate-transcript.md:1226`); A's reading of Orca's review-ownership rule (`round2-advocate-e.md:28`); FC-2; FC-3.
- **Target**: Base, table row 1 (V5:10) (append conditions); the "merge into a shared branch" item moves to Change 4.
- **Rationale**: pr-submit binds to the checkout it runs in and HALTs `pr_head_mismatch` when that checkout is not the PR head (`pr-submit/SKILL.md:268,316`); it has no path flag (`src/superclaude/commands/pr-submit.md:8`), so under D3 (a) the coordinator itself must stand in the PR-head checkout with no other writer for the whole loop. Orca's rule ties PR preparation to the owner the user's plan names (`[G:cl] 62-65`, per V1:42).
- **Integration point**: Row 1 conditions become: only when the user's instruction names the action; every GitHub action targets `IronbellyOrg/IronClaude` (never the upstream parent, never Orca's issue or PR linking until its project identity resolves to the fork); PRs only through `/sc:pr-submit --monitor 3`, run from the PR-head checkout with no other writer there for the whole loop (`--max-rounds` default 2, cap 5); the plan or brief records the PR owner.
- **Risk**: Medium. Whether a coordinator can move its session to another checkout mid-run without side effects is UNVERIFIED (`round2-advocate-e.md:43`).

### Change 4 (mandatory, INV-025): merges into a shared branch only at quiescence
- **Source**: invariant probe smallest change (`invariant-probe.md:56`); B's concession B7 (`invariant-probe.md:33`).
- **Target**: Base, new row "Merge into the feature branch or another shared branch", placed after row 3 (V5:12).
- **Rationale**: A merge moves HEAD in the worktree where that branch is checked out and triggers implement's `head-moved` check (`implement/refs/retry.md:41,44`); V5 listed it as an outward action with no quiescence condition.
- **Integration point**: Owner: coordinator. Condition: only in the worktree where the branch is checked out, only when the placement map shows no other writer there, with the porcelain check of Change 5, stopping and reporting on a hook failure or conflict.
- **Risk**: Low.

### Change 5: Coordinator commit in a shared worktree: `--only`, porcelain cross-check, hooks, empty commit, durable placement map (A-002, N2, INV-001, INV-020)
- **Source**: Advocate E's C1, N2 and C3 (`debate-transcript.md:1195,1197,1220`); INV-001 and INV-020 (`invariant-probe.md:9,28`).
- **Target**: Base, table row 3 (V5:12) (replace condition).
- **Rationale**: Explicit-path `git add` is not enough when other paths are already staged; pr-submit already commits with `git commit --only -- <paths>` for this reason (`pr-submit/SKILL.md:274`). INV-020: a commit with nothing to commit exits non-zero and must not read as a hook failure. INV-001: the placement map must survive compaction or a coordinator crash.
- **Integration point**: Condition becomes: no worker runs in that worktree (placement map plus `worker-list`); compare `git status --porcelain` with the settled contracts and report unlisted paths, never sweep them; `git add -- <paths>` for contract paths plus `.dev/tasks` (`CLAUDE.md:37`), then `git commit --only -- <paths>`; nothing to commit is success, recorded as "no commit"; a hook rewrite or failure stops and is reported, never `--no-verify`. The placement map is a coordinator duty (section 2.3) kept in a file in the feature worktree's run notes and in each `worker-start --comment`.
- **Risk**: Low.

### Change 6: Worker local-commit lane (A's conditions 1-3, W1-W6, conflict fixes 3 and 4)
- **Source**: A's conditions 1-3 (`round2-advocate-a.md:30-32`); Advocate E's W1-W6, N4, N6, B8 (`debate-transcript.md:1203-1208,1225,1227`); `EVAL:74`.
- **Target**: Base, table row 4 (V5:13) (replace condition).
- **Rationale**: Off by default, because per-task commits are "an authorized option, never a default" (`EVAL:74`). Conflict fix 3: A's condition 2 required `--worktree new-*` for the Task, which bars `/sc:implement` and pr-submit resumes that must run in the existing worktree holding their ledger or run-log (N4). Conflict fix 4: every commit uses `--only` (N2).
- **Integration point**: Row 4 condition becomes: (W1) the brief quotes the user's instruction naming local commits for this run and branch; never push, merge or PR. (W2) The worker is placed, new or by exact selector `id:<worktree id>` for a resume, in a child worktree created for this run and recorded with no other writer: no other worker, no coordinator git, no person or taken-over terminal, no Agent-tool fan-out outside a batch. (W3) `/sc:implement`: only between a task's `complete` line and the next task's Q0, never inside a parallel batch; dormant until #326 K3 exists (`EVAL:63`); other commands: at their own authorized commit step or after the command finishes. (W4) The worker session runs `check` immediately before each commit; a follow-up may revoke or narrow the grant, never widen it. (W5) If `git status --porcelain` shows a path the worker did not write, it commits nothing and reports `blocked`. (W6) `git add -- <paths>` plus `.dev/tasks`, `git commit --only -- <paths>`, each SHA in the contract's `artifacts`; a hook failure gives `partial` or `blocked`, never `--no-verify`; a found `index.lock` gives `blocked` with the path.
- **Risk**: Medium. W4 cannot be written into K3's own text, because commands may not call Orca (SA-2, `SPEC:170`; INV-009), so it rests on the worker session.

### Change 7: Placement triggers for child worktrees (P1 amended, INV-006 mandatory, CR-01 T1-T4)
- **Source**: B's P1 (`round2-advocate-e.md:41-42`); INV-006 (`invariant-probe.md:14,54`); N7 (`debate-transcript.md:1228`); CR-01 triggers (`CR01:16-20`).
- **Target**: Base, new section "Placement" after the table.
- **Rationale**: INV-006 (HIGH): CR-01's T2 and B's P1(b) fire only when another worker writes outside `.dev/`, but the retry ladder also reverts files written by the coordinator, the person, a taken-over terminal or a hook (`implement/refs/managed-workspace.md:85`; `implement/refs/retry.md:220`).
- **Integration point**: A worker gets its own child worktree when (T1) its brief grants local commits; (T2, amended) it runs `/sc:implement` and any writer other than itself may write outside `.dev/` in that worktree during the run, unless the coordinator records the checkout as having no other writer for the whole run; (T3) it runs a pr-submit loop; (T4) it is a parallel experiment to compare or discard; (T5, new) its command writes the user index, unless that step is refused under `--unattended`. Report-only workers share the feature worktree, with every report directory under `.dev/` (outside the revert domain, `implement/refs/retry.md:207`). Differences from CR-01: T2 widened to any writer (INV-006); T5 added (N3).
- **Risk**: Medium. More child worktrees mean more setup and cleanup (V5:46).

### Change 8: Per-PR pr-submit opt-in as a named exception (C's M2-M3, conflict fix 2)
- **Source**: Advocate E's O3 (`debate-transcript.md:1192`); C's M2-M3 (`round2-advocate-e.md:44-45`); K1 (`round2-advocate-e.md:51`).
- **Target**: Base, new table row after row 1.
- **Rationale**: Conflict fix 2: A's condition 4 ("workers otherwise never commit, move HEAD or touch remotes") contradicts a pr-submit worker, which commits a fix, moves HEAD and pushes (`pr-submit/SKILL.md:274`). The opt-in must be a named exception.
- **Integration point**: Row: "pr-submit for one PR, as a worker Task". Owner: one worker per PR. Condition: only under D3 (b), only when the user asks for parallel PR monitoring, only after a test shows an Orca chat-tab worker satisfies pr-submit's "never headless / detached" rule (`pr-submit/SKILL.md:303`; UNVERIFIED today); the Task runs in that PR's head child worktree with no other writer; the brief quotes the instruction naming the PR; a HALT ends the Task `blocked`; resume is a new Task with `--resume <run-log.jsonl>` (`SPEC:137`), fresh terminal by default, same terminal optional. **Amendment (orchestrator, after the first merge pass found a new contradiction):** the document title changes from "every outward action has one owner, the coordinator" to "the coordinator owns every outward action, except a per-PR pr-submit worker the user explicitly opts into", so the title no longer contradicts this row.
- **Risk**: Medium. INV-015: a pr-submit HALT fires mid-loop, so under WC-3 it can never be asked; every HALT costs a new Task.

### Change 9 (mandatory, INV-026): narrow D4 so a brief can authorize local commits only
- **Source**: INV-026 smallest change (`invariant-probe.md:57`); N3 (`debate-transcript.md:1221-1224`).
- **Target**: Base, "Safety and authorization" (V5:22-25) (insert) and "Implementation cost" (V5:40-41) (spec wording list).
- **Rationale**: V5:24 rests the worker's authority on "D4 (a)", but D4 (a) as worded also lets a brief authorize worker outward actions (`SPEC:345-348`): post-release commit, push and PR (`SPEC:136`), auggie-review `--post-pr` (`SPEC:123`), and `/sc:task` push (`SPEC:144`). That contradicts E's core rule that every outward action belongs to the coordinator.
- **Integration point**: A brief may authorize a worker's local commits only (Change 6). Outward actions are never authorized through a brief (D4 (b) for outward actions), except the per-PR opt-in (Change 8). Under `--unattended`: post-release's commit, push and PR steps, auggie-review's posting and `/sc:task`'s push are refused; `/sc:task`'s commit runs only under the Change 6 lane.
- **Risk**: High. It reverses the spec's current D4 recommendation for outward actions; the user decides D4.

### Change 10 (mandatory, INV-024): no `git add` by any worker under `--unattended`, including `.dev/tasks`
- **Source**: INV-024 smallest change (`invariant-probe.md:55`); orchestrator check (`debate-transcript.md:21`).
- **Target**: Base, new "Invariant" row replacing row 5 (V5:14), and the spec wording list.
- **Rationale**: Every worker session loads the repo rule "`.dev/tasks/` is always staged (`git add .dev/tasks`)" (`CLAUDE.md:37`), and implement, workflow and the task executor repeat it (`implement/refs/managed-workspace.md:36`; `implement/refs/ledger.md:3`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:28`; `src/superclaude/skills/task/SKILL.md:35`). Two report-only workers sharing a worktree then contend for `index.lock` and leave staged paths that pr-submit records as `OPERATOR_PENDING` (`pr-submit/SKILL.md:272`).
- **Integration point**: Under `--unattended`, a worker never runs `git add`, including `git add .dev/tasks`, except a granted worker inside Change 6 and a per-PR opt-in worker inside Change 8 (pr-submit stages its fix with `git add -- <paths>`, `pr-submit/SKILL.md:274`; amendment by the orchestrator after the first merge pass found this contradiction). `.dev/tasks` staging is done by the git owner at each commit (Change 5) and at the end of the run, so the repo rule still holds for the run. The worker contract and the skill files above defer staging under `--unattended`.
- **Risk**: High. It changes how an absolute repo rule is applied in worker sessions; the user should confirm the one-clause amendment.

### Change 11: Invariant row restated precisely (A's condition 4; replaces V5:14)
- **Source**: A's condition 4 (`round2-advocate-a.md:33`); Advocate E's G1 (`debate-transcript.md:1211`); concession E14 (`round2-advocate-e.md:26`).
- **Target**: Base, table row 5 (V5:14) (replace).
- **Rationale**: Row 5 is false as written for `/sc:implement`, which writes pin refs (`implement/SKILL.md:113,116`), builds a private index (`implement/SKILL.md:111`) and restores or deletes worktree files on revert (`implement/refs/retry.md:220`).
- **Integration point**: "Outside the worker lane (Change 6) and the per-PR opt-in (Change 8), a worker never writes the user index, never commits, never moves HEAD and never touches a remote. `/sc:implement`'s private-index snapshots, its refs under `refs/superclaude/implement/` and its revert stay allowed; Change 7 confines the revert. The coordinator never runs one managed package in two worktrees at once."
- **Risk**: Low.

### Change 12 (mandatory, INV-032): a write-verb audit test gates the invariant
- **Source**: INV-032 smallest change (`invariant-probe.md:58`); reflect's worktree verbs (`debate-transcript.md:22`).
- **Target**: Base, "Implementation cost" (V5:40-41) (append).
- **Rationale**: The rule set is not shown sufficient: no audit of git and gh write verbs in the installed primitives was done, and the probe found more cases than N3 (reflect's `git worktree add/remove`, post-release's worktree).
- **Integration point**: A test (pytest, `uv run pytest`) scans the installed skills, commands and agents for git and gh write verbs (`add`, `commit`, `push`, `merge`, `worktree add/remove`, `stash`, `update-ref`, `gh pr`, `gh api` posts) and fails unless each hit is allowed by Change 11, refused under `--unattended`, or on an explicit allowlist with a reason. The invariant is stated as holding only after this test passes.
- **Risk**: Low.

### Change 13: Optional git guard (D's Layers 1 and 2) with conflict fixes 1 and 4
- **Source**: D's guard (`round2-advocate-d.md:44-80`); Advocate E's N1 and K7 (`debate-transcript.md:1219`; `round2-advocate-e.md:57`); INV-014 (`invariant-probe.md:22`).
- **Target**: Base, new short section "Optional guard".
- **Rationale**: Conflict fix 1: Layer 1 blocks `git add -A` and fails closed on compound commands, which would stop every `/sc:implement` task at Q0 (`implement/SKILL.md:111`) and every revert (`implement/refs/retry.md:199,238-240`). INV-014: a text exemption for `GIT_INDEX_FILE=` cannot be checked soundly. Conflict fix 4: Layer 2's grammar lists `commit -m` but not `commit --only`.
- **Integration point**: The guard is a recommended control, never a dependency of any safety claim. Layer 1 stays off by default until a corpus test passes every git and gh command template in the installed primitives (including implement's Q0 and revert) and a live test under the run's permission mode passes. Layer 2 (committer subagent) accepts `add -- <paths>` and `commit --only -- <paths>`, is installed only to `~/.claude/agents/`, and is not used when Orca provenance is requested.
- **Risk**: Low (optional).

### Change 14: Recovery wording corrected (B8, E11)
- **Source**: B8 and concession E11 (`round2-advocate-e.md:23`).
- **Target**: Base, "Recovery" (V5:28) (replace).
- **Rationale**: "the retry Task (WC-6) checks for it first" describes a step no command has.
- **Integration point**: "A Task that finds `index.lock` in its worktree stops `blocked` and names the path; only the coordinator or the person removes it, after proving no git process runs. Commits made before the crash survive."
- **Risk**: Low.

### Change 15: Shared refs corrected (INV-005, INV-003, E4)
- **Source**: INV-005 and INV-003 (`invariant-probe.md:11,13`); E4 (`round2-advocate-e.md:16`).
- **Target**: Base, "Correctness under parallel workers" (V5:17,19) (replace).
- **Rationale**: "no two git writers share a lock" (V5:17) is overbroad: refs and `packed-refs` live in the common directory. In managed mode the slug is the package id, so two worktrees running one plan collide by construction (`implement/SKILL.md:113`).
- **Integration point**: Index and HEAD are per worktree; refs are shared. Never run one managed package in two worktrees at once; parallel experiments of one plan need separate package copies. Ref-lock contention is a known, UNVERIFIED-in-practice limit.
- **Risk**: Low.

### Change 16: Success criteria for each git action (base weakness: Completeness 4)
- **Source**: rubric gap, NOT MET for every variant (`base-selection.md`, Completeness 4; R#2-R#5).
- **Target**: Base, new short section "When a git action counts as done".
- **Rationale**: No variant defined done-ness; a SHA in a contract is a record, not a criterion (`scoring-reconcile.md:11`).
- **Integration point**: Local commit: HEAD advanced, the commit holds exactly the listed paths, and the SHA is reported. Nothing to commit: reported as "no commit", not a failure. PR: the URL's owner and repo are `IronbellyOrg/IronClaude` and the run-log is the contract artifact. Merge: the branch tip contains the child tip, no conflict markers, and the worktree is quiescent again. Removal: the worktree and branch are gone and nothing on the removal-guard list was lost.
- **Risk**: Low.

### Change 17: Risks with probability, impact and mitigation (base weakness: Risk 1-2)
- **Source**: rubric gap, NOT MET for every variant (`base-selection.md`, Risk Coverage 1-2); invariant probe MEDIUM findings.
- **Target**: Base, "Weaknesses" (V5:43-46) (restructure into a risk table).
- **Rationale**: Weaknesses were listed without probability, impact or mitigation (`scoring-pass-1.md:143-152`).
- **Integration point**: A table with at least the three V5 weaknesses plus the open MEDIUM invariants that bear on the design (INV-002, 007, 008, 015, 022, 027, 029, 033), each with probability, impact and mitigation or "open".
- **Risk**: Low.

### Change 18: Terms defined on first use (base weakness: Clarity 4)
- **Source**: rubric gap, NOT MET for every variant (`scoring-pass-1.md:126-130`).
- **Target**: Base, new short "Terms" list after the title.
- **Rationale**: Spec IDs (D3, D4, WC-n, K3, F3) and "quiescent point" were used undefined.
- **Integration point**: One line each for coordinator, worker, outward action, local commit, quiescent point, sole writer, feature and child worktree, placement map, K3, D3, D4, WC-9, WC-11.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-001, C-003 (V3) | A long-lived git session owns every git action | C's own advocate withdrew it (Round 2 C4); retention is debugging-only (`debate-transcript.md:23`) and one session serializes loops (C-009, `debate-transcript.md:1303`). Its per-action record survives only in the per-PR opt-in (Change 8). |
| C-003, X-003 (V2) | Workers push and open PRs | Every advocate placed outward actions with the coordinator by default (`debate-transcript.md:1297,1308`); WC-9 exists to prevent worker outward actions (`SPEC:73`). |
| C-001 (V4) | A coordinator subagent as the git owner | It cannot run pr-submit, which must be top-level (`pr-submit/SKILL.md:47-49`), so it is never a complete owner (V4:32). It survives only as optional Layer 2 (Change 13). |
| C-002 (V1) | No worker commits at all; per-task commits wait for K3 under the coordinator | The lane is kept, default off, because `/sc:task` already has an authorized commit step under `SPEC:144` that needs a guard now (N3), and K3's boundary must be fixed by this spec (`EVAL:63`). |
| V1:8 | "Workers never run a mutating git command" | False for `/sc:implement` (N3; Change 11 states the precise invariant). |
| C-006 | Who carries the context load: D's committer offload against C's per-PR Task | Split in the debate (55%, `debate-transcript.md:1300`). Not resolved; both stay available (Change 13 Layer 2, Change 8). Reported as an unresolved conflict. |
| A's condition 2 as written | Worker started with `--worktree new-*` for that Task | Bars resume Tasks that must run in the existing worktree (N4); amended to "new or by exact selector" (Change 6). |
| D's Layer 1 on by default | Settings-level deny-list in every session now | Would block `/sc:implement`'s Q0 and revert (N1); its text exemption is unsound (INV-014). Off until the corpus and live tests pass (Change 13). |
| EVAL F2 location | Experiment worktrees under `.dev/worktrees/<run>-<n>/` (`EVAL:52`) | Overridden by FC-1. |
| MEDIUM and LOW invariants not made mandatory | INV-002, 003 (partly), 005 (partly), 007-010, 014-015, 017-018, 022, 027, 029, 031, 033 | The no-convergence rule makes only HIGH items mandatory (`debate-transcript.md:1327`). INV-001, 004, 020 and 028 are folded in because they fit the touched rows (Changes 1, 2, 5); the rest are listed as open risks (Change 17). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | Children start without `.claude/` copies or a Python environment; workers fail at start | Keep the shared feature worktree only; run setup by hand before dispatch |
| 2 | Low | A worktree with needed state is removed | Removal guard list; `orca worktree rm` refuses only what Orca checks, so the coordinator checks first |
| 3 | Medium | pr-submit HALTs `pr_head_mismatch` when the coordinator is not in the PR-head checkout | pr-submit pushes nothing on that HALT (`pr-submit/SKILL.md:316`) |
| 4 | Low | A merge halts a running implement task | Revert to V5's wording (merge as plain outward action) |
| 5 | Low | A commit sweeps a staged path | `--only` prevents it; fallback is V5:12 wording |
| 6 | Medium | A granted worker commits the wrong paths | Local and reversible (V5:24); tripwire W5 fails closed |
| 7 | Medium | Too many child worktrees | Triggers are conditional; report-only work shares the feature worktree |
| 8 | Medium | A worker counts as headless and pr-submit refuses | Opt-in stays disabled until the attended-mode test passes |
| 9 | High | Conflicts with the spec's D4 (a) recommendation | User decision on D4; if D4 (a) stands for outward actions, INV-026 stays open |
| 10 | High | Changes how an absolute repo rule applies in workers | User confirms; otherwise INV-024 stays open and report-only workers need their own worktrees |
| 11 | Low | Wording | Revert to A's condition 4 |
| 12 | Low | Test finds hits that need policy decisions | Allowlist with reasons |
| 13 | Low | Guard blocks a legitimate command | Optional and off by default |
| 14-18 | Low | Wording or documentation | Remove the added text |

## Review Status
- [x] Auto-approved (default; `--interactive` was not set, `diff-analysis.md:13`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-02 (session clock; resumed after the 16:28 UTC interruption)
- Flagged for user review: Changes 9 and 10 (they touch the user's open decision D4 and an absolute repo rule).
