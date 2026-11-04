<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 5 (option E, original) -->
<!-- Merge date: 2026-11-02 -->

<!-- Source: Base (original, modified); title per Change #8 amendment -->
# Option E (hybrid): sole-writer workers may commit locally; the coordinator owns every outward action, except a per-PR pr-submit worker the user explicitly opts into

<!-- Source: Base (original) -->
Position paper for the git-ownership debate. Added because the evidence in options A and B splits along one line: local commits are safe for a worker exactly when it is the only writer in its worktree, while outward actions are safe only where the user's authorization is given directly.

<!-- Source: Base (original, modified); citation keys extended with the keys the refactor plan's Overview defines, so the citations carried in by Changes 1-18 resolve -->
Citation keys: as in `option-a.md` (`SPEC`, `CAPS`, `EVAL`, `HWW`, `[G]`, `[G:cl]`, `[G:wc]`, `[G:rc]`, `[G:pl]`, `GITDEMO`). Added by the merge: `SPEC` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `EVAL` = `.dev/orca-command-refactor/review/issue-326-evaluation.md`; `CR01` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md`; `implement/` = `src/superclaude/skills/sc-implement-protocol/`; `pr-submit/` = `src/superclaude/skills/sc-pr-submit-protocol/`; `V<n>:L` = line L of `variant-<n>-original.md`. Debate files (`debate-transcript.md`, `invariant-probe.md`, `round2-advocate-<x>.md`) are in this folder. Repo path:line citations were re-read on 2026-11-02 after merged PR #343, which changed only review convergence and repair wording in `/sc:implement`, not the git mechanics used here (`implement/refs/retry.md:147,149,193`).

<!-- Source: Merge addition (rubric gap Clarity 4, NOT MET for every variant, `scoring-pass-1.md:126-130`), merged per Change #18 -->
## Terms
- **Coordinator:** the top-level Claude session, in the person's main chat, that plans the run, writes briefs, places workers and owns every outward action except under the per-PR opt-in.
- **Worker:** a session the coordinator starts through Orca to run one Task from a brief; it returns a contract.
- **Outward action:** any action visible outside this machine: push, PR, review reply, issue or status comment, project update, remote branch deletion.
- **Local commit:** a commit in a local branch that is not pushed; reversible and invisible outside the machine until the coordinator pushes.
- **Quiescent point:** a moment when no worker, and no other writer, is running in the worktree concerned.
- **Sole writer:** a worker placed in a worktree the coordinator records as having no other writer for the whole run (worker lane, W2).
- **Feature worktree:** the one top-level worktree per feature, on the feature branch, where the coordinator runs (`CR01:15`).
- **Child worktree:** a worktree Orca creates from the feature branch for one worker when a placement trigger applies (`CR01:16`; section "Placement").
- **Placement map:** the coordinator's record of which Task writes in which worktree (section 2.3 duty), kept durably (row "Local commit of settled work").
- **K3:** issue #326's per-task commit step inside `/sc:implement`; it does not exist yet (`EVAL:63`).
- **D3:** the spec's open decision on who runs `/sc:pr-submit`: (a) the coordinator or person only, (b) a worker with pre-authorization for parallel PR monitoring (`SPEC:341-343`).
- **D4:** the spec's open decision on whether a coordinator's brief may authorize a worker's outward actions: (a) only when the user's own instruction names the action, (b) never (`SPEC:345-348`).
- **WC-9:** worker-contract rule "No outward action unless the brief authorizes it" (`SPEC:73`).
- **WC-11:** worker-contract rule "Parallel-safe writes": two workers in one worktree never write the same file (`SPEC:75`).

<!-- Source: Base (original, modified); per-action table kept; rows changed or added per Changes 1-6, 8, 10 and 11. Each row carries its own Source tag in its first cell. -->
## The proposal
Names used below: the **worker lane** is the worker local-commit row (W1-W6); the **per-PR opt-in** is the row "pr-submit for one PR, as a worker Task".

| Action | Owner | Condition |
|---|---|---|
| <!-- Source: Base (original, modified); conditions appended per Change #3 (C's M1, Advocate E's N5, A's reading of [G:cl] 62-65, FC-2, FC-3); the merge item moved to its own row per Change #4 --> Push, PR (always `/sc:pr-submit --monitor 3`), review replies, issue or status comments, project updates, remote branch deletion | Coordinator, in its main chat | Only when the user's own instruction names that action (D4, narrowed in "Safety and authorization"). Every GitHub action targets `IronbellyOrg/IronClaude`, never the SuperClaude upstream parent (`CLAUDE.md:41-47`; pr-submit resolves the target from `origin` and refuses a misrouted PR URL, `pr-submit/SKILL.md:267`). Orca's issue and PR linking is not used until Orca's project identity for this repo, recorded today as the upstream parent, resolves to the fork (`CR01:45`). PRs only through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`), run from the PR-head checkout with no other writer there for the whole loop: pr-submit binds to the checkout it runs in, has no path flag (`src/superclaude/commands/pr-submit.md:8`) and HALTs `pr_head_mismatch` otherwise (`pr-submit/SKILL.md:268,316`). `--max-rounds` default 2, hard cap 5 (`src/superclaude/commands/pr-submit.md:47`). The plan or brief records the PR owner (`[G:cl] 62-65`, per V1:42). Whether a coordinator can move its session to another checkout mid-run without side effects is UNVERIFIED (`round2-advocate-e.md:43`). |
| <!-- Source: Variant 3 (C), M2-M3, via Advocate E's O3 (`debate-transcript.md:1192`; `round2-advocate-e.md:44-45,51`); merged per Change #8 --> pr-submit for one PR, as a worker Task (per-PR opt-in) | One worker per PR | A named exception to the invariant row. Only under D3 (b), only when the user asks for parallel PR monitoring, and only after a test shows an Orca chat-tab worker satisfies pr-submit's "never headless / detached" rule (`pr-submit/SKILL.md:303`; UNVERIFIED today). The Task runs in that PR's head child worktree with no other writer; the brief quotes the user's instruction naming the PR (`SPEC:346`). A HALT ends the Task `blocked`; resume is a new Task with `--resume <run-log.jsonl>` (`SPEC:137`), on a fresh terminal by default, the same terminal optional. |
| <!-- Source: CR-01 sections 2 and 5.1 (`CR01:14-24,41`), INV-028 (`invariant-probe.md:36`); merged per Change #1 (FC-1, FC-4); removal guard widened per Change #2 (INV-004, `invariant-probe.md:12`) --> Create worktrees; remove child worktrees and their local branches | Coordinator | Every worktree is created through Orca at Orca's default location, never with raw `git worktree add` and never under `.dev/worktrees/`: one feature worktree per feature, where the coordinator runs, and a child worktree per worker with `worker-start --worktree new-child --base-branch <feature branch> --setup run` only when a "Placement" trigger applies (`CR01:14-24`). This follows the user's decision of 2026-11-02 (`CR01:41`) and overrides the repo's `.dev/worktrees/` location rule (`CLAUDE.md:299-302`); the repo-wide refactor of that rule is planned separately. No worker is dispatched into a child until its setup has succeeded (`CR01:24`); whether Orca's setup hook runs `make sync-dev`, creates the Python environment and indexes the code graph is UNVERIFIED (`CR01:42`). Removal is `orca worktree rm` plus deletion of the branch, after merge-back (next row). Removal guard: never remove a worktree or branch with unmerged commits, an open PR, uncommitted changes (for example edits left by pr-submit `fix_commit_failed`, `pr-submit/SKILL.md:318`), an unfinished `/sc:implement` ledger, or a contract or report directory not yet read, without the user's instruction (`EVAL:53`, F3). |
| <!-- Source: CR-01 section 2.4 and open questions 3-4 (`CR01:23,43-44`); merged per Change #2 --> Merge a child branch into the feature branch | Coordinator | After the child's result is admitted (`SPEC:81-85`), the coordinator merges the child branch into the feature branch under the conditions of the row "Merge into the feature branch or another shared branch", then removes the child as in the row above. A discarded experiment is removed without merging. A merge conflict stops and is reported, never auto-resolved. The feature branch is merged into a child only between Tasks, never while a worker runs in it. |
| <!-- Source: Base (original, modified); condition replaced per Change #5 (Advocate E's C1, N2, C3, `debate-transcript.md:1195,1197,1220`; INV-001, INV-020, `invariant-probe.md:9,28`) --> Local commit of settled work in a shared worktree | Coordinator | At a quiescent point: no worker runs in that worktree (placement map plus `worker-list`). Compare `git status --porcelain` with the settled contracts and report unlisted paths, never sweep them. Stage with `git add -- <paths>` for contract paths plus `.dev/tasks` (`CLAUDE.md:37`), then commit with `git commit --only -- <paths>`, as pr-submit already does so nothing else in the index is committed (`pr-submit/SKILL.md:274`). Nothing to commit is success, recorded as "no commit". A hook rewrite or failure stops and is reported, never `--no-verify` (`HWW:280`). The placement map is a coordinator duty (section 2.3), kept in a file in the feature worktree's run notes and in each `worker-start --comment`, so it survives compaction or a coordinator crash. |
| <!-- Source: invariant probe smallest change for INV-025 (`invariant-probe.md:56`); B's concession B7 (`invariant-probe.md:33`); merged per Change #4 (mandatory) --> Merge into the feature branch or another shared branch | Coordinator | Only in the worktree where that branch is checked out, only when the placement map shows no other writer there, with the porcelain check of the row above, stopping and reporting on a hook failure or conflict. Reason: a merge moves HEAD in that worktree and triggers `/sc:implement`'s `head-moved` check (`implement/refs/retry.md:41,44`). |
| <!-- Source: Base (original, modified); condition replaced per Change #6 (A's conditions 1-3, `round2-advocate-a.md:30-32`; Advocate E's W1-W6, N4, N6, B8, `debate-transcript.md:1203-1208,1225,1227`; `EVAL:74`) --> Local commit inside a worker's own run (per-task commits, experiment branches): the worker lane | That worker; off by default ("an authorized option, never a default", `EVAL:74`) | **W1.** The brief quotes the user's instruction naming local commits for this run and branch; the lane never covers push, merge or PR. **W2.** The worker is placed, new or by exact selector `id:<worktree id>` for a resume, in a child worktree created for this run and recorded with no other writer: no other worker, no coordinator git, no person or taken-over terminal, no Agent-tool fan-out outside a batch. **W3.** `/sc:implement`: only between a task's `complete` line and the next task's Q0, never inside a parallel batch (`implement/refs/retry.md:41`; `implement/SKILL.md:97,114`); dormant until #326 K3 exists (`EVAL:63`). Other commands: at their own authorized commit step (`/sc:task`, `SPEC:144` as amended) or after the command finishes. **W4.** The worker session runs `check` immediately before each commit (`[G] 85-87`); a follow-up may revoke or narrow the grant, never widen it. W4 cannot be written into K3's own text, because commands may not call Orca (SA-2, `SPEC:170`; INV-009), so it rests on the worker session. **W5.** If `git status --porcelain` shows a path the worker did not write, it commits nothing and reports `blocked`. **W6.** `git add -- <paths>` plus `.dev/tasks`, then `git commit --only -- <paths>`; each SHA goes in the contract's `artifacts`; a hook failure gives `partial` or `blocked`, never `--no-verify`; a found `index.lock` gives `blocked` with the path. |
| <!-- Source: Base (original, modified); row V5:14 replaced by an invariant row per Change #10 (INV-024, `invariant-probe.md:32,55`, mandatory) and restated per Change #11 (A's condition 4, `round2-advocate-a.md:33`; Advocate E's G1, `debate-transcript.md:1211`; concession E14, `round2-advocate-e.md:26`) --> Invariant: any other git write by a worker | No worker | Outside the worker lane and the per-PR opt-in, a worker never writes the user index, never commits, never moves HEAD and never touches a remote. `/sc:implement`'s private-index snapshots (`implement/SKILL.md:111`), its refs under `refs/superclaude/implement/` (`implement/SKILL.md:113,116`) and its revert (`implement/refs/retry.md:220`) stay allowed; the "Placement" triggers confine the revert. The coordinator never runs one managed package in two worktrees at once. Under `--unattended`, a worker never runs `git add`, including `git add .dev/tasks`, except a granted worker inside the worker lane and a per-PR opt-in worker (Change 8), because pr-submit stages its fix with `git add -- <paths>` (`pr-submit/SKILL.md:274`); `.dev/tasks` staging is done by the git owner at each commit (row "Local commit of settled work") and at the end of the run, so the repo rule (`CLAUDE.md:37`) still holds for the run. The invariant holds only after the write-verb audit test passes (see "Implementation cost"). |

<!-- Source: Variant 2 (B), P1 amended (`round2-advocate-e.md:41-42`); INV-006 (`invariant-probe.md:14,54`); N7 (`debate-transcript.md:1228`); CR-01 triggers (`CR01:16-20`); merged per Change #7 (INV-006 mandatory) -->
## Placement
A worker gets its own child worktree, created by Orca as in the worktree row, when any of these holds:
- **T1.** Its brief grants local commits (the worker lane).
- **T2 (amended).** It runs `/sc:implement` and any writer other than itself may write outside `.dev/` in that worktree during the run: another worker, the coordinator, the person, a user-taken-over terminal or a hook. Exception: the coordinator records the checkout as having no other writer for the whole run. Reason: the retry ladder reverts files whoever wrote them (`implement/refs/managed-workspace.md:85`; `implement/refs/retry.md:220`).
- **T3.** It runs a pr-submit loop.
- **T4.** It is a parallel experiment to compare or discard.
- **T5 (new).** Its command writes the user index (N3), unless that step is refused under `--unattended`.

Report-only workers share the feature worktree, with every report directory under `.dev/`, which is outside the revert domain (`implement/refs/retry.md:207`).

Differences from CR-01: T2 is widened from "another worker" to any writer (INV-006), and T5 is added (N3). More child worktrees mean more setup and cleanup (V5:46; see "Risks").

## Correctness under parallel workers
<!-- Source: Base (original, modified); overbroad lock claim narrowed per Change #15 (INV-005, `invariant-probe.md:13`) -->
- **Index lock:** a worker commits only in a worktree where it is the sole writer, and linked worktrees have separate index files (GITDEMO), so no two git writers share an index lock. In a shared worktree only the coordinator commits, at quiescent points. This isolation covers the index and HEAD only; refs are shared (see "Shared refs").

<!-- Source: Base (original) -->
- **HEAD movement:** a worker's own commits move only its own worktree's HEAD (separate HEAD per linked worktree, GITDEMO). `/sc:implement`'s retry ladder stays valid when commits fall between tasks, because each task's baseline is recorded at its own start (`src/superclaude/skills/sc-implement-protocol/SKILL.md:114`; `refs/retry.md:41`) and a parallel batch has no ladder anyway (`SKILL.md:97`). The coordinator never commits in a worktree while an implement worker runs there.

<!-- Source: Base (original, modified); replaced per Change #15 (INV-005 and INV-003, `invariant-probe.md:11,13`; E4, `round2-advocate-e.md:16`) -->
- **Shared refs:** index and HEAD are per worktree; refs are shared across linked worktrees, and refs and `packed-refs` live in the common directory (GITDEMO; INV-005). Implement's pins live under `refs/superclaude/implement/<slug>/T<id>`, and in managed mode the slug is the package id, so two worktrees running one plan collide by construction (`implement/SKILL.md:113`). Rule: never run one managed package in two worktrees at once; parallel experiments of one plan need separate package copies. Ref-lock contention is a known limit, UNVERIFIED in practice.

<!-- Source: Base (original) -->
- **Per-task commits (#326):** possible, because the worker that knows task boundaries is the one committing.

## Safety and authorization
<!-- Source: Base (original, modified); "No worker pushes" qualified for the per-PR opt-in added by Change #8, to avoid a contradiction inside the merged text -->
- Outside the per-PR opt-in, every outward action stays where the person gives the instruction, in the session `/sc:pr-submit` requires (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49`), matching D3 (a) (`SPEC:341`) and the repo PR rule (`CLAUDE.md:50`). No worker pushes outside the per-PR opt-in, so WC-9 stays exactly as strict as today for outward actions (`SPEC:73`).

<!-- Source: Base (original, modified); the worker's authority now rests on the narrowed D4 of Change #9 instead of D4 (a) as worded -->
- A local commit is not outward but still needs the user's ask (`CLAUDE.md:37`; `HWW:282` "Commit locally, show your lead what changed, and push only when they say go"). The worker's authority is the quoted instruction in its brief, under the narrowed D4 in the next item (`SPEC:346`). A local commit is reversible and invisible outside the machine until the coordinator pushes.

<!-- Source: Invariant probe smallest change for INV-026 (`invariant-probe.md:34,57`); N3 (`debate-transcript.md:1221-1224`); merged per Change #9 (mandatory) -->
- **D4 narrowed (INV-026).** A brief may authorize a worker's local commits only (the worker lane). Outward actions are never authorized through a brief (D4 (b) for outward actions), except the per-PR opt-in. Under `--unattended`: post-release's commit, push and PR steps (`SPEC:136`), auggie-review's posting (`--post-pr`, `SPEC:123`) and `/sc:task`'s push (`SPEC:144`) are refused; `/sc:task`'s commit runs only under the worker lane. Reason: D4 (a) as worded also lets a brief authorize those worker outward actions (`SPEC:345-348`), which contradicts the rule that every outward action belongs to the coordinator. This reverses the spec's current D4 (a) recommendation for outward actions; the user decides D4.

<!-- Source: Base (original, modified); audit trail qualified for the per-PR opt-in added by Change #8 -->
- **Audit trail:** worker commits are listed by SHA in contracts; every push, PR and comment is in the coordinator's transcript beside the instruction that authorized it, except under the per-PR opt-in, where pr-submit's run-log is the contract artifact (`SPEC:137`).

## Recovery
<!-- Source: Variant 2 (B), B8, and concession E11 (`round2-advocate-e.md:23`); merged per Change #14 -->
- Worker crash mid-commit: a Task that finds `index.lock` in its worktree stops `blocked` and names the path; only the coordinator or the person removes it, after proving no git process runs. Commits made before the crash survive.

<!-- Source: Base (original, modified); qualified for the per-PR opt-in added by Change #8 -->
- Coordinator crash: as A; no outward action can be half-done by a worker, because workers do none outside the per-PR opt-in, whose own resume is a new Task with `--resume <run-log.jsonl>` (`SPEC:137`). The placement map survives in its file (row "Local commit of settled work").

<!-- Source: Merge addition (rubric gap Completeness 4, NOT MET for every variant, `base-selection.md`; a SHA in a contract is a record, not a criterion, `scoring-reconcile.md:11`); merged per Change #16 -->
## When a git action counts as done
- **Local commit:** HEAD advanced, the commit holds exactly the listed paths, and the SHA is reported.
- **Nothing to commit:** reported as "no commit", not a failure.
- **PR:** the URL's owner and repo are `IronbellyOrg/IronClaude`, and pr-submit's run-log is the contract artifact.
- **Merge:** the branch tip contains the child tip, there are no conflict markers, and the worktree is quiescent again.
- **Removal:** the worktree and branch are gone, and nothing on the removal-guard list was lost.

<!-- Source: Variant 4 (D), Layers 1 and 2 (`round2-advocate-d.md:44-80`); Advocate E's N1 and K7 (`debate-transcript.md:1219`; `round2-advocate-e.md:57`); INV-014 (`invariant-probe.md:22`); merged per Change #13 -->
## Optional guard
D's two-layer guard is a recommended control, never a dependency of any safety claim in this document.
- **Layer 1** (settings-level `PreToolUse` deny-list) stays off by default until a corpus test passes every git and gh command template in the installed primitives, including `/sc:implement`'s Q0 (`implement/SKILL.md:111`) and revert (`implement/refs/retry.md:199,238-240`), and a live test under the run's permission mode passes. As specified it blocks `git add -A` and fails closed on compound commands, which would stop every implement task at Q0 and every revert (N1). A text exemption for `GIT_INDEX_FILE=` cannot be checked soundly (INV-014).
- **Layer 2** (committer subagent) accepts `add -- <paths>` and `commit --only -- <paths>`, is installed only to `~/.claude/agents/`, and is not used when Orca provenance is requested.

<!-- Source: Base (original) -->
## Context load on the coordinator
Lower than A when per-task commits are used (workers write their own messages); equal to A for outward actions, which are few per run.

<!-- Source: Base (original) -->
## Fit with repo PR rules
Exact fit (`CLAUDE.md:50`; `HWW:223`: monitor 3 publishes only the cycle's fix commit to origin).

<!-- Source: Base (original) -->
## How a person works day to day
The person says, for example, "run the plan in its own worktree, commit after each task, and open a PR when it passes". They see commits appear on the experiment branch during the run, and the PR is opened by the coordinator in their own chat. Without that instruction nothing is committed.

## Implementation cost
<!-- Source: Base (original, modified); spec wording list expanded per Changes #9 and #10, with the CR-01 placement wording adopted per Changes #1 and #7 and the 7.2 location per FC-1; "Commands: none" qualified because Change #10 amends four skills -->
Spec wording:
- WC-9 and D4 (`SPEC:73,345-348`): narrowed D4 as in "Safety and authorization": a brief authorizes a worker's local commits only.
- `SPEC:123` (auggie-review `--post-pr`), `SPEC:136` (post-release commit, push and PR) and `SPEC:144` (`/sc:task`: push refused under `--unattended`; commit only under the worker lane) amended to match.
- WC-11 and section 2.3: the placement rule, the feature worktree and the placement map as a durable coordinator duty, using CR-01's wording (`CR01:26-31`) with the T2 widening and T5 addition from "Placement".
- Section 7.2: the disposable worktree is created by Orca at Orca's default location, not under `.dev/worktrees/` (`SPEC:235`; `CR01:41`).
- The `/sc:git` row (`SPEC:156`) and this file's table.
- The worker contract: under `--unattended`, a worker never runs `git add`, including `git add .dev/tasks`, except inside the worker lane and a per-PR opt-in worker (Change 8) (invariant row; `pr-submit/SKILL.md:274`).

Commands and skills: no new command steps in this spec's phases. Four skill files defer `.dev/tasks` staging under `--unattended`: `implement/refs/managed-workspace.md:36`, `implement/refs/ledger.md:3`, `src/superclaude/skills/sc-workflow-protocol/SKILL.md:28` and `src/superclaude/skills/task/SKILL.md:35`. The per-task commit step inside `/sc:implement` stays #326's feature (K3, `EVAL:63`), and until it exists a worker commits only through steps its brief adds after the command finishes.

<!-- Source: Invariant probe smallest change for INV-032 (`invariant-probe.md:58`); reflect's worktree verbs (`debate-transcript.md:22`); merged per Change #12 (mandatory) -->
Write-verb audit test (gates the invariant row): a pytest test, run with `uv run pytest`, scans the installed skills, commands and agents for git and gh write verbs (`add`, `commit`, `push`, `merge`, `worktree add/remove`, `stash`, `update-ref`, `gh pr`, `gh api` posts) and fails unless each hit is allowed by the invariant row, refused under `--unattended`, or on an explicit allowlist with a reason. The invariant is stated as holding only after this test passes. Known hits beyond N3 include reflect's `git worktree add/remove` and post-release's worktree.

<!-- Source: Base (original, modified); "Weaknesses an opponent will press" (V5:43-46) restructured into a risk table per Change #17 (rubric gap Risk Coverage 1-2, `base-selection.md`; `scoring-pass-1.md:143-152`), with the open MEDIUM invariants from `invariant-probe.md:10-41` -->
## Risks
Probability and impact are qualitative estimates from the debate and probe evidence, not measured. "Open" means no rule in this document mitigates the risk yet.

| # | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Two owners for local commits means two rule sets to state and test (V5 weakness 1) | High | Low | The two rows share four predicates and differ in one ("sole writer for the whole run" against "no writer during the commit"), so one test table with one varying column covers both (`round2-advocate-e.md:14`) |
| R2 | A worker running raw git can still make a mistake inside its own worktree, such as wrong paths (V5 weakness 2) | Medium | Low | Local and reversible; W5 tripwire fails closed; `--only` with explicit paths; SHA in the contract for the coordinator's review; optional Layer 2 committer |
| R3 | More worktrees mean more setup and cleanup (V5 weakness 3, F3) | High | Medium | Placement triggers are conditional; report-only work shares the feature worktree; setup before dispatch; removal guard |
| R4 | INV-002: "sole writer" is not an exclusive lease; the coordinator can later place another Task in the same worktree by exact selector | Low | Medium | Open |
| R5 | INV-007: `worker-list` does not see writers in other Runs, other sessions on the machine, or the person, so a quiescence check can miss a writer | Medium | Medium | Partly: the porcelain cross-check reports unlisted paths; otherwise open |
| R6 | INV-008: the W5 touched set is not well defined under `/sc:implement` (batch members, tests, formatters, setup write files) | Medium | Low (fails closed as a false `blocked`) | Open |
| R7 | INV-015: a pr-submit HALT fires mid-loop, so under WC-3 it can never be asked; every HALT costs a new Task | Medium | Low | Accepted cost; resume with `--resume <run-log.jsonl>` (`SPEC:137`) |
| R8 | INV-022: a managed `/sc:implement` worker in a new child worktree does not find a plan that was staged but not committed (`E-MANAGED-INVALID`) | High when a child is used | Medium (fails closed) | Open: needs a coordinator commit with the user's ask, or a copy |
| R9 | INV-027: when the PR head is the branch checked out in the coordinator's worktree, the per-PR Task must run there, which stops the coordinator writing for the whole loop | Medium | Medium | Open |
| R10 | INV-029: experiment branches carry diverging `.dev/tasks` copies, so merge-back conflicts on ledgers and retries | Medium | Medium | Partly: a merge conflict stops and is reported (merge-back row); which branch wins for `.dev/tasks` is open |
| R11 | INV-033: the rule that outward actions need the user's named instruction is enforced only by the model; advocate D reports that the debate session ran with `--dangerously-skip-permissions` (`round2-advocate-d.md:101`, from `ps` on 2026-11-02; not re-checked by the orchestrator) | Low | High | Open; the optional guard's Layer 1, once tested, blocks some forbidden forms only |
