# Recommendation: D4, may a coordinator's brief authorize a worker's outward actions (and may workers commit)?

Status: COMPLETE (2026-11-02). Built from the resumed `/sc:adversarial` run: Steps 4-5 finished on this date; Steps 1-3 were used as found on disk.
Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. Paths are repo-relative unless absolute. `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `ADV/` = `.dev/orca-command-refactor/decisions/D4/debate/adversarial/`.

## 1. Recommended option, and agreement with the spec
**Recommend option (c) as refined in the debate, "(c′)": no worker ever does anything that leaves the machine, and a worker may make one local git commit only when the user asked for it and the worker sits alone in its own Orca child worktree. Option (b), "never", is the default whenever those conditions are not met.**

This **overturns** the spec's current recommendation, option (a) (`SPEC:346,348`). Option (a) lets a brief authorize a worker to push, open a PR, post to GitHub, install or run paid jobs when the user's instruction names that action.

Why it changed:
- The spec's reason for (a) is that post-release confirms outward steps "unless the user pre-authorized them this session" (`SPEC:348`, quoting `src/superclaude/skills/sc-post-release-protocol/SKILL.md:351`). A worker is a different session. Its only proof of the user's words is the coordinator's quotation, which the worker cannot check. The debate found that citation overstated as support for (a) (`ADV/diff-analysis.md:105`), and (a)'s own advocate conceded it (`ADV/rounds/r1-variant-1.md:38`).
- All three advocates, including the one arguing for (a), ended by recommending (c′) (`ADV/debate-transcript.md:720-722`).
- The same `PRL:351` line is the correct reason for the new answer: outward steps stay with the coordinator, the one session that can still ask the person.

The merged position is `ADV/merged-output.md`; the plan behind it is `ADV/refactor-plan.md`.

## 2. Answer on worker commits
**Yes, but only as a narrow, opt-in exception. Without it, workers make no commits, as the spec says today (`SPEC:156`).** A worker commits only when all of these hold:
1. The brief copies, word for word, the user's own instruction naming a local commit for that Task.
2. The worker runs alone in its own child worktree, created by Orca at Orca's default path. CR-01 trigger T1 requires this (`.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:16-17`).
3. The command has finished and its contract says `worker_status: succeeded`. A `partial` or `blocked` result never gets a commit.

Then the worker:
- reads any coordinator follow-up first;
- refuses on a detached HEAD, on the default branch, or when a file it did not write has appeared;
- makes one plain `git commit --only -- <paths>` of its own files plus `.dev/tasks`;
- never uses `--no-verify`, never pushes;
- reports the commit's ID in its `worker_done` message.

Two further rules:
- A command's own built-in commit step stays off without a person present: post-release's commit, `/sc:task`'s commit and push, and the `/sc:task` failure-report commit (`ADV/rounds/r2-variant-3.md:37`).
- Commits after each `/sc:implement` sub-task wait for the separate #326 feature K3 (`.dev/orca-command-refactor/review/issue-326-evaluation.md:63`).

This matches the git-ownership outcome, hybrid option E: workers commit locally only where the brief grants it, using `--only`, and one owner does every push, PR and comment. Section 6 lists the five places where D4's wording differs from E's.

## 3. Confidence, and the strongest argument that lost
**Confidence: high on the direction, medium on the details.**
- **Direction.** Every one of the 32 debated points was agreed: 28 unanimously and 4 by majority (`ADV/debate-transcript.md:666-667`), and every advocate recommends (c′).
- **Details.** The debate first ended "blocked" on four serious gaps the independent fault-finder found (INV-001, INV-002, INV-016, INV-027; `ADV/debate-transcript.md:693-712`). The merged position closes each one with a new rule, but those rules are written, not run. Base selection was also close:
  - Option (c) beat option (b) by about 3% overall (0.8106 against 0.7850) and won on the tiebreaker, 13 debate points outright against 5 (`ADV/refactor-plan.md`, Overview; `ADV/debate-transcript.md:663`).
  - The Step 3 scoring file still has 11 unfinished sections (`ADV/base-selection.md:132-163`). The base choice was checked against the two finished scoring passes and holds under every resolution of their four disagreements.

**Strongest argument that lost: option (b)'s consistency argument.** The commit permission still rests on the coordinator's quotation of the user, the same relayed authority the spec refuses for Rulings under D2 ("another agent's message" is not acceptance, `src/superclaude/skills/sc-implement-protocol/refs/qa.md:254` on this branch; the spec cites it as `qa.md:238`, a stale line number, `SPEC:334`). Option (b) also has zero risk of moving git HEAD under a running task, with no preconditions.
- (b) won both points at 97% (C-007 and C-003, `ADV/debate-transcript.md:639,643`).
- It lost overall because the risk it guards against is limited to one undoable commit on an isolated branch that a person reviews before any push.
- (b) cannot give issue #326's owner the per-task commit history they asked for (`.dev/orca-command-refactor/review/issue-326-evaluation.md:19`).

## 4. What this means in practice
**What you will see.** Background helpers (workers) do the work and write reports. They never publish anything: they do not push code, open pull requests, comment on GitHub, install onto real machines, start virtual machines or spend money. Only the main assistant you talk to (the coordinator) does those things, in your conversation, and only on the IronbellyOrg/IronClaude fork, never on the public SuperClaude project.

**What you do differently.**
- If you want a saved history of each finished piece of work, say so: for example, "commit after each task on this feature." Each helper that is allowed to save work then runs in its own separate copy of the project (a child worktree, which Orca creates automatically). It saves its work there as one local snapshot (a commit). Nothing leaves your machine.
- If you say nothing, helpers save nothing, as today.
- Before anything is pushed or a pull request is opened, the coordinator shows you the helpers' saved snapshots and waits for your "go". This happens even if you approved pushing earlier, so you always see helper work before it becomes public.
- You will decide what happens to each helper's copy: keep and merge it into the feature, or throw it away.

**What could go wrong.**
- **The coordinator misquotes you.** A helper cannot check that you really asked for a commit. The worst result is one unwanted snapshot in an isolated copy, which you see before anything is published and can discard.
- **The coordinator skips one of its own rules.** For example, it merges while a halted task still needs that copy. The halted task then refuses to resume, and you resolve it by hand. Nothing mechanical stops this today; the rules are instructions.
- **A save attempt is refused.** For example, a stray file appeared, or a pre-commit check failed. The helper reports failure and leaves its work unsaved in its copy for you or the coordinator to save later. No work is lost.
- **Some publishing work waits.** Installing onto a real machine and posting detailed review comments now wait for the coordinator instead of finishing in one go. That is slower, not less safe.

**What it costs to change later.**
- **Loosening to option (a)** (letting a helper publish when you name the action) is an addition: one paragraph and a few flag rules. It is cheap.
- **Tightening to option (b)** (no helper saves at all) is one sentence plus deleting the commit rule. It is also cheap.
- **Undoing published work cannot be done.** That is the reason publishing stays with the coordinator now.

## 5. Exact spec wording change
This replaces the D4 block at `SPEC:345-348`. The supporting edits to WC-5, WC-9, section 2.3, the section 3 rows, the `/sc:git` row, AC-4.2 and section 7.2 are listed after it and in `ADV/refactor-plan.md` Change 9. None of them has been applied: the spec was not edited.

**Replace `SPEC:345-348` with:**

> **D4. May a coordinator's brief authorize a worker's outward actions, and may a worker commit?** (affects post-release, pr-submit under D3 (b), auggie-review `--post-pr`, task `commit`/`push`, and issue #326's per-task commits)
> - (a) **Only when the user's own instruction to the coordinator names that action for that task.** The coordinator quotes the instruction in the brief and passes the command's explicit flag; without it every outward default is off (WC-9).
> - (b) **Never.** Workers make no outward changes and no commits; the coordinator or person performs every commit, push, PR, comment, install and VM step after reading the reports.
> - (c) **Local commits only, under conditions (recommended).** No brief can authorize a worker to do anything that leaves the machine: push, merge into a shared branch, PR, review reply, issue or status comment, project update, remote branch deletion, install on a shared or real target, VM or paid external run. The coordinator does those in its own conversation, only when the user's instruction names the action, and confirms with the person at the moment of action unless that instruction is in its live conversation (`sk/sc-post-release-protocol/SKILL.md:351`). Every GitHub action targets `IronbellyOrg/IronClaude` only, and PRs open only through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`). A worker makes one local commit only when (1) the brief quotes, word for word, the user's instruction naming a local commit for that Task, (2) the worker runs alone in its own child worktree created by Orca (CR-01 trigger T1), and (3) the command has exited with `worker_status: succeeded`. The worker then reads coordinator follow-ups, refuses on a detached HEAD, the default branch or any path outside its report directory, `report_path`, `artifacts` and `.dev/tasks`, commits with `git commit --only -- <paths>` and never `--no-verify`, never pushes, and gives the commit ID in its `worker_done` body. A command's own commit step stays off under `--unattended`. Otherwise (b) applies. Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go.
> - Recommendation: (c). A worker is a separate session whose only evidence of the user's words is the coordinator's quotation (WC-2: it cannot ask), so actions that cannot be taken back stay with the coordinator, which `sk/sc-post-release-protocol/SKILL.md:351` requires to confirm "this session". A local commit on an isolated branch, reviewed before any push, is the one action that is cheap to undo; it gives issue #326 its per-task history. D3 (b) needs D4 (a) and is unavailable under (c).

**Supporting edits (summary; full text in `ADV/refactor-plan.md` Change 9 and `ADV/merged-output.md`):**
- **WC-9 (`SPEC:73`):** "Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (D4). The only git write a brief may authorize is the worker session's end-of-Task local commit under D4's commit rule." Remove the citation `.dev/orca-command-refactor/README.md:31`.
- **WC-5 (`SPEC:69`):** add "If an authorized commit is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason."
- **Section 2.3 (`SPEC:79`):** replace "which outward actions, if any, are authorized (WC-9)" with "whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (D4); no other outward action can be authorized". Add the coordinator duties:
  - review before push;
  - no commit or merge into a worktree with a running worker or a halted `/sc:implement` Task;
  - a grant ends at that Task's `worker_done`;
  - a placement record;
  - distinct plan slugs;
  - an absolute report directory inside a child worktree.
- **Section 3 rows:**
  - auggie-review (`SPEC:123`): `--post-pr` is refused under `--unattended`, and the coordinator posts the summary from `REVIEW.md`.
  - implement (`SPEC:132`): no commit inside the command; per-task commits wait for #326 K3.
  - post-release (`SPEC:136`): VM, real-target install, commit and PR are always off under `--unattended`.
  - task (`SPEC:144`): EXEMPT `commit` and `push` are refused under `--unattended`.
- **`/sc:git` row (`SPEC:156`):** cite `CLAUDE.md:37` and `src/superclaude/core/HOW-WE-WORK.md:324` instead of `README.md:31`. Change "workers make no commits or pushes" to "workers make no pushes, merges or PRs; a worker makes a local commit only under D4".
- **AC-4.2 (`SPEC:275`):** compare these four, before dispatch and after the run:
  - `git -C <worker worktree> log -1 --format=%H`;
  - `git -C <worker worktree> for-each-ref refs/heads`;
  - `git ls-remote origin`;
  - `gh pr list --repo IronbellyOrg/IronClaude --author @me`.

  Pass: no change, or, when a commit was authorized, only new commits on the worker's child branch. Also add one P0 check that a commit-authorized worker started with `--worktree new-child` commits only on its child branch.
- **Section 7.2 (`SPEC:235-236`):** the check's worktree is created by Orca at Orca's default path, never under `.dev/worktrees/`, and the "whether Orca accepts a worktree it did not create is UNVERIFIED" clause is deleted.
- **CR-01's four edits** (`CR-01:28-31`) replace issue-326 evaluation item F2.

## 6. Interactions with D1-D3, D5, git ownership and CR-01
The D1, D2, D3 and git-ownership recommendation files were still being finished when this was written (`decisions/git-ownership/RECOMMENDATION.md` was a stub). The positions below come from each debate's emerging consensus in its `invariant-probe.md` and base selection. Treat them as UNVERIFIED until those recommendations are final.

| Decision | Interaction | Agree or conflict |
|---|---|---|
| D1 (how a command knows no person is present) | D4's rules apply only under `--unattended`. D1's consensus keeps that flag as the switch and adds a worker-session check before each command (`decisions/D1/debate/adversarial/invariant-probe.md:11-16`). The rule that `--unattended` must also reach nested commands (INV-011) belongs to D1 and the per-command rows, not D4. | Agree; no conflict |
| D2 (who gives a Ruling) | D2's consensus keeps "another agent's message is not acceptance" (`qa.md:254`). D4 accepts the coordinator's quotation for one thing only, a local commit. That is a stated inconsistency (C-007, conceded to option (b)), limited by isolation and review before push. D4 also adopts D2's rule that no other Task or merge touches a worktree whose `/sc:implement` Task halted, until the person acts (`decisions/D2/debate/adversarial/invariant-probe.md:14`). | Agree on the halt rule; known, accepted inconsistency on relayed authority |
| D3 (pr-submit as a worker) | D3's consensus is option (a): the coordinator or the person runs `/sc:pr-submit`. It says option (b) "runs only under D4 (a)" (`decisions/D3/debate/adversarial/invariant-probe.md`, "Emerging consensus" item 3). D4 (c′) therefore rules out D3 (b), and AC-4.3 (`SPEC:276`) does not run. | Agree with D3 (a). D3 (b) would need D4 loosened to (a) |
| D5 (Orca nesting depth) | No interaction. D4 adds no worker that starts workers (D5 base selection: keep depth 1, `decisions/D5/debate/adversarial/base-selection.md:202`). | Agree; independent |
| git ownership (hybrid option E) | Same split: workers make local commits only where granted, with `git commit --only -- <paths>`, and one owner does every push, PR and comment (`decisions/git-ownership/debate/adversarial/round2-advocate-e.md:63-87`). There are five wording conflicts, each stated with a resolution in `ADV/refactor-plan.md` under "Changes NOT Being Made":<br>(1) E lets `/sc:task`'s own commit step run when granted; D4 keeps it off.<br>(2) E records each commit ID in the contract's `artifacts`; D4 puts it in the `worker_done` message, because `artifacts` lists files and editing the contract after the commit leaves uncommitted changes.<br>(3) E reports a refused commit as `blocked` or `partial`; D4 reports outcome `failed` and leaves the contract unchanged.<br>(4) E puts worktrees under `.dev/worktrees/`; the user's location rule overrides that.<br>(5) E's opt-in pr-submit worker (O3) is unavailable under D4 (c′). | Agree on the core rule; five explicit conflicts, with D4's wording recommended for the git-ownership text |
| CR-01 (feature worktree hierarchy) | D4's commit condition 2 is CR-01 trigger T1 (`CR-01:17`). CR-01's merge-back by the git owner (`CR-01:23`) is limited by D4: no merge into a worktree with a running worker, or one holding a halted `/sc:implement` Task. Every push that would publish worker commits the person has not seen needs the person's go after they see them. CR-01's note that T1 "only applies if D4 lets a brief authorize commits" (`CR-01:36`) is satisfied. | Agree; D4 adds two limits on merge-back and push |

## 7. Gaps and UNVERIFIED items
- **Step 3 record incomplete (NOT BUILT).** `ADV/base-selection.md` still has 11 `<!-- TODO -->` sections (`ADV/base-selection.md:132-163`). It was not edited, as instructed. The base choice was confirmed from the two finished scoring passes and the debate tally instead (`ADV/refactor-plan.md`, Overview). For the same reason the return contract says `status: partial` (`ADV/return-contract.yaml`).
- **Not run live (UNVERIFIED):**
  - whether `worker-start --worktree new-child --base-branch` works for a worker (the evidence is `--help` output, `CR-01:48`);
  - whether Orca's `--setup run` prepares a child worktree (`CR-01:42`);
  - every new rule in sections 2 and 5, which are design rules with no run behind them.
- **Accepted risks:**
  - The commit rests on the coordinator's quotation (C-007).
  - "Never push" is enforced by instructions only (INV-012).
  - Child-worktree exclusivity is asserted by the coordinator (INV-007).
  - Two runs of the same plan in two worktrees can collide on implement's refs (INV-025).
- **Stale spec citation:** the spec cites the Ruling rule as `qa.md:238` (`SPEC:67`, `SPEC:334`). On this branch it is at `src/superclaude/skills/sc-implement-protocol/refs/qa.md:254`. Fix it at the next spec revision.
- **Sibling decisions not final:** the D1, D2, D3 and git-ownership positions in section 6 come from their debates' consensus files, not from finished recommendations (UNVERIFIED).
- **Review trail:** the merge plan had an independent review (`ADV/refactor-plan-review.md`). The first pass FAILED with 6 blocking findings; after one fix cycle the re-review PASSED. Under PR #343 the 12 minor notes in that file were not fixed. The merge validated PASS (`ADV/merge-log.md:179`).
- **Not done:** the spec was not edited, and nothing was staged, committed, pushed or posted.
