# Proposal 3: release train, a batch branch cut from `integration`, every story gated by its own pull request, the batch lands in `integration`

Written 2026-11-23 for the branching-strategy debate. Facts about the use case come from `CONTEXT.md` in this folder. Evidence IDs (S1 and so on) point to `research-notes.md` in this folder. Anything marked UNVERIFIED was not confirmed.

## 1. Summary

Each dashboard release is a "train": one batch branch `train/dash1.3`, cut from `integration`. Each story branch is cut from the train branch, and each story is merged into the train branch by a pull request (`/sc:pr-submit --monitor 3 --base train/dash1.3`), so every story gets CI and both automatic reviewers on a small diff, before it joins the batch. CI is switched on for those pull requests with a one-line base-branch pattern in the workflow file. Stories that depend on each other can be stacked. The train departs when its planned stories are in, or at a set time with whatever is in; a story that is not ready simply is not merged into this train and rides the next one (Mozilla and Chrome work this way, S22). The train then lands as one pull request into `integration` (`--base integration`), where CI and both reviewers run once more, and the existing `integration` to `master` promotion ships it.

It keeps the batch isolation of Proposal 1 (no half release in shared branches) and the per-change feedback of Proposal 2 (CI and review on small diffs). It costs a CI change and a decision about who clicks merge on story pull requests.

## 2. Branch names, examples, and the ref-conflict rule

| Kind | Pattern | Example |
|---|---|---|
| Train (batch) branch | `train/<release>` | `train/dash1.3` |
| Story branch | `<release>-s<NN>-<slug>` (flat, not under `train/`) | `dash1.3-s04-token-usage-panel` |
| Sync-from-integration branch | `<release>-sync<N>` | `dash1.3-sync2` |
| Fix inside the train | `<release>-fix<NN>-<slug>` | `dash1.3-fix01-empty-state` |
| Fix on shipped code | `fix/<issue>-<slug>` from `master` | `fix/731-ledger-path` |
| Marker after promotion (tag) | `dash/<release>` | `dash/1.3` |

Ref-conflict rule: two shapes only. The train branch is a leaf inside the folder `train/`; every story-type branch is flat (no slash between release token and story token) and never lives under `train/`. So `train/dash1.3` and `dash1.3-s04-x` cannot collide with each other, and no branch is ever named just `train` or `dash1.3`. CI is turned on by the pattern `train/*` in the `branches` filter of the `pull_request` trigger (S11). If Orca adds `ironbelly/` in front when `--branch` is given, the pattern must be written after checking what Orca produced: UNVERIFIED.

Sorting: `train/dash1.3` groups all trains in one folder; story branches sort by release then story number.

## 3. Merge flow (text)

```
master        A ------------------------------------------------------- (promotion, existing path)
               \                                                          ^
integration    I0 ----------------- I1 ------- I2 --------------------- T (owner merges the train PR)
                \                    \                                    ^
train/dash1.3    t0 --- m1 --- m2 --- S(merge integration in) --- m3 -----+  one PR, --base integration
                  \     ^      ^                                  ^
              dash1.3-s01   dash1.3-s02     ...      dash1.3-s03 (stacked on s02, or after it)
              (story PR into the train: CI + Augment + Codex; merge commit)
```

Steps:
1. Cut `train/dash1.3` from the current `integration` tip. Commit planning `.dev/` records and the ledger on it. Push it (the first push; from now on it is never rewritten).
2. Each story: Orca worktree from the train tip. Worker runs the story pipeline. A top-level session runs `/sc:pr-submit --monitor 3 --base train/dash1.3`.
3. A story pull request that depends on an unmerged story can target that story's branch (a stack; GitHub documents stacks whose bottom pull request targets "any branch, such as a release branch", S10). CI does not run on a pull request whose base is a story branch under the present workflow, so stack only where the lower story merges within hours; otherwise wait.
4. Merge into the train with a merge commit, serially (one at a time; no merge queue, S4: wildcard rules are unsupported). The next waiting story merges the new train tip into itself first.
5. Keep the train current: merge `origin/integration` into it at the start, whenever `integration` changed files that stories own, and right before departure. If that merge conflicts, a `dash1.3-sync<N>` branch is made so a worker resolves it and passes the normal pull request gate; the coordinator never resolves conflicts itself (worker contract, CONTEXT line 9).
6. Departure: `/sc:pr-submit --monitor 3 --base integration` from the train worktree. Owner merges with a merge commit. Tag after promotion.

## 4. The nine questions

**Q1. Names.** See section 2. `train/dash1.3` for the batch, flat story branches. Carries the release number and the story id, no ref conflict, sortable.

**Q2. Where story work merges, how, who resolves conflicts, what stops collisions.**
- Where: into the train branch, by pull request. Each story gets CI and both reviewers on a small diff (S6: small batches; S19: reviewers choke on big diffs). Who clicks merge is an owner decision (Open decision A below): the standing rule is that the owner merges every pull request; this proposal works best if the owner allows the coordinator to merge story pull requests into a `train/*` branch only, once CI is green and both reviewers have settled, and keeps the owner's own click for the train pull request into `integration`.
- Method: merge commit (`--no-ff` equivalent). One merge commit per story, so a story can be reverted whole (Q9) and the story tips stay reachable.
- Conflicts: shown on the pull request; the story's worker resolves by merging the train tip into the story branch (not rebase; `/sc:pr-submit` never rewrites a published branch).
- Prevention: disjoint path claims for stories that run at once; shared files in a first foundation story; serial merges into the train; CI on every story pull request runs against the real train tip, so a semantic collision shows as a red check on the next story's pull request, one story later at worst. Ownership boundaries and one session per dependency change (S21).

**Q3. Keeping the train current with `master` and `integration`.** The train is cut from `integration`, so `integration` is the branch it follows: merge `origin/integration` into it (merge commit, never rebase after the first push) at the start, whenever `integration` touched story paths, and before departure. `master` is not merged in directly; whatever reaches `master` through the usual promotion also reaches `integration`, and an emergency fix on `master` reaches the train through the `master` into `integration` sync that is part of that fix's definition of done (Q6). The merge-in is the main weekly cost of this proposal, because Clay's work lands in `integration` at AI speed (CONTEXT line 16).

**Q4. How the release lands.** Train pull request `train/dash1.3` into `integration`, opened by `/sc:pr-submit --monitor 3 --base integration`. CI (existing `integration` trigger) and both reviewers run once more, over a diff whose stories were each reviewed once already; the second pass is mostly an integration check against whatever Clay merged meanwhile. The owner merges with a merge commit so each story merge stays visible. Then `integration` goes to `master` by the existing promotion at the owner's chosen moment. Important: the release is on `master` only when `integration` is promoted, and that promotion carries Clay's merged work too (the same coupling as Proposal 2). Size: the train pull request is a roll-up; its true review cost was paid per story. If a train grows too large the cadence rule (below) cuts it.

**Q5. Flags, trunk-based alternatives, are long-lived release branches justified.** The batch branch is justified only while it is short. Train rule: the scope floats, the time does not. Set a time box for a train (the owner picks it; the research gives no AI-specific number: Chrome moved from four weeks to two, S22; DORA says anything over a week is too big a batch, S6). At the time box, stories that are not merged ride the next train. This removes the need for flags: unfinished work is "not in the train", not "in but hidden". Flags remain an option for a story that must reach `integration` before the train departs (none planned). If trains routinely run past the time box, move toward Proposal 2.

**Q6. Hotfixes and bug fixes during a release.**
- Bug in shipped code on `master`: `fix/<issue>-<slug>` from `master`, pull request into `master`, then a `master` into `integration` sync pull request, then the train merges `integration` in. The back-port is part of the fix's definition of done, because forgetting it is the classic regression (S2, S9).
- Bug in a merged story inside the train: `dash1.3-fix<NN>-<slug>` pull request into the train.
- Bug in a train already landed in `integration` but not yet on `master`: fix on `integration` as a normal small pull request; the promotion carries it.
- The 1.1 bug-fix releases: a train whose stories are fixes; the 1.105 test-only releases: a train of test stories. A one-story release skips the train and goes as one pull request into `integration` (no train branch for a batch of one).

**Q7. Clean-up and what is kept.** Story branches are deleted by GitHub on merge if "Automatically delete head branches" is on (S12; setting UNVERIFIED), else by the coordinator; worktrees removed after the merge is in the ledger. The train branch is deleted after the owner merges the train pull request and the promotion marker is placed. The ledger `sprint-status.yaml` and the `.dev/` records live on the train branch and land with it (CONTEXT lines 13 and 14), so the convention in CONTEXT is unchanged. Story tips remain reachable through the merge commits.

**Q8. Fit with `integration` and Clay's habit.** The train branch is cut from `integration`, which is Clay's starting point, and lands back in `integration`, where Clay's pull requests already go. A collision with Clay's work is found at merge-in time or at train-pull-request time, in CI, and resolved by a worker; it is never deferred to a later `master` sync. Clay's branches are untouched while a train runs. The planning convention in CONTEXT line 14 ("BMAD planning of release n+1 starts from `master` after release n merges") needs a change here: planning must start from `integration` (or wait for the promotion).

**Q9. Failure and rollback.** A story that goes bad after merging into the train: a revert pull request of that story's merge commit into the train (`git revert -m 1`), or a fix story. A train that fails after landing in `integration`: a revert pull request of the single train merge commit takes out the whole release; individual stories can be reverted instead because their merge commits remain. A release that fails on `master` after promotion: revert the promotion, or fix forward in `integration` and promote again. Re-merging a branch whose merge was reverted needs the revert to be reverted first (general git behaviour; UNVERIFIED here); prefer a fix train.

## 5. What it costs

- One change to `.github/workflows/test.yml` (the `branches` filter on `pull_request` gets `train/*`; S11) and a branch-protection or ruleset entry for `train/*` if the owner wants required checks. This is outside the current "CI only for master and integration" state and needs the owner's approval.
- More pull requests and more CI runs than Proposal 1: each story pays for CI and both reviewers, plus the train pull request. Fewer than Proposal 2 (no slicing of one story into several, no flags).
- A merge-authority decision (Open decision A).
- Merge-in housekeeping against `integration`, and sync branches when it conflicts.
- Stacks are weak here because CI does not cover pull requests based on a story branch; the native GitHub stacked pull requests feature is not assumed available (S10: availability on this plan UNVERIFIED).
- The BMAD planning-from-`master` convention has to move to `integration`.

## 6. Who it favours

A middle path. It favours the owner's batch idea and the coordinator (isolated batch, ledger on the branch, one landing), and it favours Clay's lane because the train is based on and lands in `integration`. It spends more reviewer and CI effort than Proposal 1 to buy early feedback, and less than Proposal 2.

## 7. Risks

1. Merge authority: if the owner insists on clicking every story merge, the train stalls behind the owner just as in Proposal 2.
2. Both bots see each story and then the roll-up; the roll-up review may be mostly noise.
3. A train branch cut from `integration` inherits whatever red or half-done work `integration` has at the cut.
4. The dashboard release depends on the `integration` to `master` promotion cadence, which this proposal does not control.
5. Wrong pattern in the CI filter (the Orca prefix) leaves story pull requests with no CI while everyone assumes they have it. Check by opening one test pull request first.
6. Reviewer behaviour on pull requests whose base is a `train/*` branch (versus the default branch) is UNVERIFIED for Augment and Codex.

## 8. Open decisions this proposal raises (for the debate)

- A. May the coordinator merge story pull requests into `train/*` after CI and both reviewers settle, with the owner clicking only the train pull request? (Yes: trains are practical. No: use Proposal 1 or accept the owner as the merge lane.)
- B. Time box of a train.
- C. Whether to edit `test.yml` now.

## 9. Sources that support it

- S8 Fowler: release train, a release branch only accepts fixes after departure.
- S22 Mozilla and Chrome: schedule-driven releases that go without unready features; Chrome shortened its cycle to cut risk per release.
- S10 GitHub stacked pull requests doc: stacks may target a release branch; designed for AI-agent task sequences.
- S11 GitHub Actions events: CI on pull requests by base-branch pattern.
- S6 DORA small batches: per-story review before regrouping.
- S19 Faros, S21 practitioner guides: review load and conflict handling.
- S2, S9: fix on trunk first, back-port discipline.
- S4: why a merge queue does not fit per-release branches (wildcard rules unsupported, plan limits).
