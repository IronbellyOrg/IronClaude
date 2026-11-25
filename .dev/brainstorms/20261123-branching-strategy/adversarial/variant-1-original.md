# Proposal 1: one release branch per dashboard release, story branches under it, local merges, one pull request at the end

Written 2026-11-23 for the branching-strategy debate. Facts about the use case come from `CONTEXT.md` in this folder. Evidence IDs (S1 and so on) point to `research-notes.md` in this folder. Anything marked UNVERIFIED was not confirmed.

## 1. Summary

This is the owner's model, made precise. Each dashboard release gets one long-lived release branch cut from `master`. Each user story gets its own branch and its own Orca worktree, cut from the release branch. The coordinator merges each settled story into the release branch locally, one at a time, with a merge commit. Nothing is pushed for review until the release is complete. Then one pull request (opened by `/sc:pr-submit --monitor 3`) takes the whole release into `master`, where CI and the two automatic reviewers run once. The owner merges that one pull request.

It keeps the coordinator, the ledger and the per-story spec/plan/QA pipeline exactly as they are today. Its weak point is that nothing outside the coordinator's own local test run looks at the code until the end, and the end is one large batch.

## 2. Branch names, examples, and the ref-conflict rule

| Kind | Pattern | Example |
|---|---|---|
| Release branch | `<release>/release` | `dash1.3/release` |
| Story branch | `<release>/s<NN>-<slug>` | `dash1.3/s04-token-usage-panel` |
| Fix inside a release | `<release>/fix-<NN>-<slug>` | `dash1.3/fix-01-empty-state` |
| Bug fix on shipped code | `fix/<issue>-<slug>` from `master` | `fix/731-ledger-path` |
| Marker after landing (tag, not branch) | `dash/<release>` | `dash/1.3` |

Ref-conflict rule: a branch name may never be the folder part of another branch name. Git stores branches as files, so `dash1.3` and `dash1.3/s04-x` cannot both exist (verified by the coordinator, CONTEXT.md line 8). Therefore the bare release token (`dash1.3`) is never a branch. The release branch is always the leaf `dash1.3/release`, and stories are its siblings, never its children. The same rule holds if Orca puts `ironbelly/` in front: `ironbelly/dash1.3/release` and `ironbelly/dash1.3/s04-x` coexist. Whether Orca adds that prefix when `--branch` is given is UNVERIFIED (research-notes "Not found / gaps").

Sorting: two-digit story numbers (`s01` to `s99`) sort in creation order. Release tokens sort correctly for the planned list (1.1, 1.105, 1.2 ... 2.0) because "1.1" is a prefix of "1.105"; a future `1.10` would sort wrongly, so do not use it. `git branch --list 'dash1.3/*'` shows one release and all its stories.

The tag `dash/1.3` is placed on the merge commit on `master` after landing. Tags live in a different namespace from branches, so it should not clash; this was not tested (UNVERIFIED).

Creating a story branch with an exact name (worker-start has no `--branch`):
`orca worktree create --branch dash1.3/s04-token-usage-panel --base-branch dash1.3/release --parent-worktree <release worktree> --agent claude`

## 3. Merge flow (text)

```
master            A ------------------------------------------- F ----->
                   \                                           ^
                    \  (cut once, at release start)            |  owner merges ONE PR
                     \                                         |  (merge commit)
dash1.3/release       R0 --- M1 ------- M2 ---- X ---- (final) +
                        \   ^  \        ^       ^
                         s01     s02            master merged in (merge commit), then local test run
                      (one worktree each; coordinator merges with --no-ff, one at a time)
```

Steps:
1. Cut `dash1.3/release` from the current `master`. Commit the planning `.dev/` records and the ledger on it.
2. For each story: create the story worktree from the release tip. The worker runs the story pipeline (spec panel, plan, plan review, implement, per-task QA).
3. Story is "settled": the coordinator does a trial merge (`git merge-tree`, read-only, S21) of the story branch onto the current release tip. If it would conflict, stop (section 4, Q2). If clean, merge with `--no-ff`, then run the full local test suite on the release worktree, then record the merge and the result in the ledger.
4. The next story that was started earlier first merges the new release tip into itself (a merge, never a rebase) and re-runs its checks, then it is merged the same way.
5. When all stories are in: merge `origin/master` into the release branch, run the full local suite again, then run `/sc:pr-submit --monitor 3 --base master` in its own top-level session in the release worktree.
6. Owner merges. The coordinator tags, deletes branches, removes worktrees (Q7), and opens the `master` into `integration` sync pull request (Q8).

## 4. The nine questions

**Q1. Names.** See section 2. One rule (leaf `release`, siblings for stories), carries release number and story id, sortable, works with or without the Orca prefix.

**Q2. Where story work merges, how, who resolves conflicts, what stops two stories colliding.**
- Where: locally, by the coordinator, into `dash1.3/release`. No pull request per story, so no CI and no automatic reviewers per story. The story's own quality gates (spec-compliance QA per task, plan review) are the only gate before the merge, plus the coordinator's full local test run after each merge.
- Method: merge commit (`--no-ff`). One merge commit per story means one `git revert -m 1` removes the whole story later (Q9), and the story's own commits stay in history. Squash would hide that boundary; rebase is not allowed once other branches were cut from the release branch (CONTEXT line 13).
- Conflicts: the coordinator stops and reports, never resolves automatically (worker contract, CONTEXT line 9). The story's worker resolves it in the story worktree by merging the release tip into the story branch, re-runs its gates, and the coordinator retries the merge. A conflict that comes from two stories that wanted the same behaviour goes to the owner as a decision.
- Prevention: (a) each story names the paths it owns at creation, and the two stories running at once must be disjoint; the coordinator checks the claim before starting the second one; (b) shared files (lockfiles, `pyproject.toml`, registries, `__init__` exports) belong to exactly one story or to a first "foundation" story that merges before the others start (S21: one session at a time for dependency changes; ownership boundary written into the prompt); (c) merges are serial, and the full local test run after each merge is the only thing that catches a semantic collision that merges cleanly (S21: worktrees do not prevent semantic conflicts).

**Q3. Keeping the release branch current with `master` and `integration`.**
- `master`: merge `origin/master` into the release branch (merge commit) at three points: at the start, between story merges whenever `master` has moved, and right before the release pull request. Never rebase the release branch after the first story branch was cut from it, and never after it is pushed (`/sc:pr-submit` never rewrites a published branch).
- `integration`: not merged into the release branch. Merging `integration` in would make the release pull request carry Clay's unreleased work into `master`. Instead the coordinator lists the files in open `integration` pull requests at release start and compares them with the stories' path claims; overlaps are raised before the story starts (Q8).
- A story worktree gets later release changes by merging the release branch into the story branch.

**Q4. How the release lands.** One pull request, `dash1.3/release` into `master`, opened by `/sc:pr-submit --monitor 3` in its own top-level session in the release worktree. CI (`test.yml`) and Augment and Codex run once, on the whole release. The owner merges with a merge commit (so story merge commits survive; whether the repository settings allow a merge commit is UNVERIFIED). Release size is the main risk: the reviewers see everything at once, which is the pattern DORA warns about ("regrouping the batches before sending them downstream", S6) and the pattern Faros links to slower reviews and more bugs per PR (S19, vendor data). Mitigation: set a story count when the release is planned so the final diff is reviewable; generate a per-story digest (the ledger lines plus `git log --merges`) into the pull request body; treat the release as "too big" and split it if the branch is open longer than about a week (extrapolated from the one-week batch limit in S6; not a DORA figure for release branches).

**Q5. Feature flags, trunk-based alternatives, are long-lived release branches justified.**
- Flags are not used. The whole point of the branch is that `master` never carries half a release.
- Justification for the long-lived branch: dashboard releases are a deliberate set of stories that should reach `master` together; the coordinator owns merge order; only two stories run at once, so the branch moves slowly. Driessen's own 2020 note says release branches fit software that is released as explicit versions (S3), and Fowler says to use a Release Branch when a releasable mainline cannot be kept at the team's integration frequency (S8).
- The counter-evidence is real: trunk-based sources say branches should live about two days (S1), CD teams "do not do release branches" (S2), and DORA says small batches are the countermeasure to AI-driven instability (S6). This proposal only holds if release branches stay days, not weeks. If they do not, switch to Proposal 3.

**Q6. Hotfixes and bug fixes during a release.**
- A bug in code already shipped on `master`: branch `fix/<issue>-<slug>` from `master`, pull request into `master`. The open release branch picks it up at the next "merge `master` in" step. Because the release branch merges back into `master`, no cherry-pick or back-port is needed (the cherry-pick-only-from-trunk rule in S2 and S9 is for maintenance branches that never merge back).
- A bug in a story already merged into the release: a new `dash1.3/fix-<NN>-<slug>` branch from the release tip, merged locally like a story.
- The 1.1 bug-fix releases: a normal release branch whose stories are all fixes. The 1.105 test-only releases: a normal release branch whose stories only add tests. A one-story release can skip the release branch and use a plain `fix/` or `feat/` branch with one pull request into `master`.

**Q7. Clean-up and what is kept.**
- Story branch and worktree: deleted as soon as the coordinator records the merge and the result is admitted. The story tip stays reachable as the second parent of the merge commit, and that merge commit reaches `master` in the release merge, so no tag is needed.
- Release branch and worktree: deleted after the owner merges and the sync pull request (Q8) is open. Tag `dash/1.3` on the `master` merge commit.
- Kept: `.dev/` records and `sprint-status.yaml` are committed on the release branch and land on `master` with it (CONTEXT lines 13 and 14); the ledger lines; the `.dev/` records of the debate and plan.

**Q8. Fit with `integration` and Clay's habit.** Clay keeps branching from `integration` and opening pull requests into it; nothing changes for Clay while a release is being built. After the release lands on `master`, the coordinator opens a `master` into `integration` pull request so Clay's next branch contains the dashboard release. Who syncs `master` into `integration` today is not stated in CONTEXT: UNVERIFIED. Cost: if Clay's open work touches dashboard files, the collision shows up in that sync pull request, late. The path-claim comparison at release start (Q3) is the only early warning.

**Q9. Failure and rollback.**
- A story goes bad after merging into the release: `git revert -m 1 <story merge commit>` on the release branch (a new commit; published history is never rewritten), or fix forward with a `fix-` branch. If later stories depend on it, revert them in reverse order or fix forward.
- A release fails on `master`: revert the release merge commit on `master` through a revert pull request opened by `/sc:pr-submit`; this removes all stories at once. Re-landing the same branch later needs the revert to be reverted first (general git behaviour, not re-verified here: UNVERIFIED). Prefer a bug-fix release (fix stories on a new release branch cut from `master`) over a re-merge.
- Single stories can still be backed out of a landed release because their merge commits are preserved.

## 5. What it costs

- No CI and no automatic review until the end. Semantic breakage between stories can sit for the length of the release.
- One large review at the end (Augment, Codex and the owner). Review-size risk is the highest of the three proposals.
- The coordinator is a single lane: serial merges, serial conflict handling.
- Long-lived branch: it drifts from `master` and needs merge-in housekeeping.
- Local-only merges are invisible on GitHub; the ledger is the only record of who merged what and when.
- A late `master` into `integration` sync.

## 6. Who it favours

The owner and the coordinator: full control over order and content, one merge decision per release, existing ledger and worker contract unchanged, no change to CI or repository settings. It is neutral to Clay and slightly bad for him at sync time.

## 7. Risks

1. Big-batch review: the strongest evidence in the research (S6, S19) points against it.
2. Hidden semantic collisions: only the coordinator's local test run guards the release branch.
3. Release branch lives too long (AI stories are fast, human review of the final PR is not).
4. Orca prefix behaviour with `--branch` unverified; a prefix surprise could break the leaf rule if someone creates `dash1.3` by hand.
5. A reverted merge cannot simply be merged again (unverified general git behaviour).
6. If the owner later wants an early look at a story, there is no pull request to review it in.

## 8. Sources that support it

- S3 Driessen note: release branches fit explicitly versioned software.
- S8 Fowler: release branch and release train; use a release branch when integration frequency is low.
- S9 Microsoft Release Flow: a release branch per release; fixes start on trunk.
- S21 practitioner guides: serial merges, ownership boundaries, trial merges with `git merge-tree`.
- S10 GitHub stacked PRs doc is not used here; the story merges are local.
- Evidence against: S1, S2, S6, S19 (see Q4 and Q5).
