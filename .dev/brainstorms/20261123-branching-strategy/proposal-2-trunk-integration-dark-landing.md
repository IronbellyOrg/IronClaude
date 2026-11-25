# Proposal 2: trunk on `integration`, short-lived story pull requests, unfinished work lands dark, release is a cut and a promotion

Written 2026-11-23 for the branching-strategy debate. Facts about the use case come from `CONTEXT.md` in this folder. Evidence IDs (S1 and so on) point to `research-notes.md` in this folder. Anything marked UNVERIFIED was not confirmed.

## 1. Summary

There is no long-lived release branch during development. `integration` is the trunk, shared with Clay. Each user story is split into one or more small pull requests. Each is a short-lived branch cut from `integration`, opened with `/sc:pr-submit --monitor 3 --base integration`, reviewed by Augment and Codex, checked by CI (which already runs on `integration`), and merged by the owner. A story that is not finished lands "dark": the code is in `integration` but nothing reaches it until the last story of the release, the switch-on story, wires it in or flips a flag. A release is then a decision, not a branch: when the switch-on story has merged, a short-lived `release/dash1.3` branch is cut just in time from `integration` and one pull request takes it into `master`.

This is the trunk-based model the research supports most strongly. It also asks the most of the owner's merge button and of the stories' design.

## 2. Branch names, examples, and the ref-conflict rule

| Kind | Pattern | Example |
|---|---|---|
| Story pull-request branch | `dash<rel>-s<NN>-<slug>` (flat, one hyphen between parts) | `dash1.3-s04-token-usage-panel` |
| Second pull request of the same story | add `-p<N>` | `dash1.3-s04-p2-token-usage-tests` |
| Release cut (just in time) | `release/dash<rel>` | `release/dash1.3` |
| Fix | `fix/<issue>-<slug>` | `fix/731-ledger-path` |
| Marker after landing (tag) | `dash/<rel>` | `dash/1.3` |

Ref-conflict rule: no slash between the release token and the story token. A flat name such as `dash1.3-s04-x` is a leaf with no folder part, so it cannot collide with `dash1.3-s05-y`, with `dash1.3-release`, or with anything else. A slash appears only in a type prefix (`fix/`, `release/`), and no branch is ever named just `fix` or `release`. With the Orca prefix the names are `ironbelly/dash1.3-s04-x`, still flat. Whether Orca adds the prefix when `--branch` is given: UNVERIFIED.

Sorting: `dash1.3-s01` to `dash1.3-s99` sort in story order; `dash1.3-*` groups a release (the story token carries the release number, so this works even though there is no release branch).

## 3. Merge flow (text)

```
master        A ----------------------------------------------- P ----->
               \                                               ^
                \                              owner merges one promotion PR
integration      ● -- ● -- ● -- ● -- ● -- ● -- ● -- ● -- ● ---┤
                  \  /     \  /   \  /            \          (cut just in time, fix-only)
              s01-p1      s02-p1  s01-p2            release/dash1.3 --(cherry-picked fixes)--+
              (each PR: CI + Augment + Codex, owner merges, squash, branch deleted)
```

Steps:
1. Planning (BMAD) splits each story into slices that can each merge alone (hours to a couple of days, S6). The story spec states for each slice whether it is dark by construction (new files nothing imports yet), needs a flag or branch by abstraction (it changes existing behaviour), or is the switch-on slice.
2. Each slice: Orca worktree from the current `integration` tip (`orca worktree create --branch dash1.3-s04-p1-... --base-branch integration --agent claude`). Worker runs the story pipeline, then a top-level session runs `/sc:pr-submit --monitor 3 --base integration`.
3. Before the first push the worker may rebase onto `integration` (nobody branched from it). After the first push only merge `integration` into the branch.
4. Owner merges (squash; one commit per slice). The head branch is deleted by GitHub if "Automatically delete head branches" is on (S12; setting UNVERIFIED) and the coordinator removes the worktree.
5. When the switch-on slice has merged and the owner decides to ship: cut `release/dash1.3` from `integration` (just in time, S2, S9, S20). The coordinator runs the full local suite on it. `/sc:pr-submit --monitor 3 --base master` opens the promotion pull request. Fix-only from then on, by cherry-pick.
6. Owner merges the promotion with a merge commit. Tag `dash/1.3`. Delete `release/dash1.3`.

## 4. The nine questions

**Q1. Names.** See section 2. Flat story branches `dash1.3-s04-slug`, release cut `release/dash1.3`. No folder collision is possible.

**Q2. Where story work merges, how, who resolves conflicts, what stops collisions.**
- Where: directly into `integration`, by pull request, one slice at a time. The merge is the owner's button, not the coordinator's.
- Method: squash, one commit per slice. Easy to revert (Q9). PostHog describes the same shape (short-lived branches squashed into main), but that page was only a search snippet and is not relied on.
- Conflicts: the pull request shows them; the slice's worker resolves by merging `integration` into its branch and pushing a normal commit. The coordinator never merges in this model, so it never has to stop on a conflict; it assigns the fix to the worker.
- Prevention: two slices in parallel must declare disjoint paths; the coordinator sequences any pair that shares a file. Shared files (lockfiles, `pyproject.toml`, registries) go in their own first slice. CI on every slice runs against the real `integration`, so semantic collisions show as a red check, which is the strongest guard of the three proposals (S4 describes the same idea in its queue, which this repository probably cannot use; see Q3 note).
- Dependent slices are not stacked: CI only runs for pull requests into `master` and `integration`, so a pull request whose base is another slice's branch gets no CI. The dependent slice starts after its predecessor merged.

**Q3. Keeping a release branch current.** There is none during development. The story branches are kept current by merging `integration`. `integration` and `master` stay in step by the existing promotion path plus a `master` into `integration` sync pull request after every promotion or emergency fix (who runs it today: UNVERIFIED). The just-in-time `release/dash1.3` branch lives for days at most and is never merged back into `integration`; fixes go to `integration` first and are cherry-picked to it (S2, S9). Note on merge queues: GitHub's merge queue would automate "test against the latest base" but cannot be enabled on wildcard branch rules, and private repositories need an Enterprise Cloud plan (S4); the plan is UNVERIFIED, so this proposal does not depend on it.

**Q4. How the release lands.** The promotion pull request `release/dash1.3` into `master` is opened by `/sc:pr-submit --monitor 3`. CI and both reviewers run again, now over a diff whose slices were each reviewed once already, so the second review is mostly duplicated effort (cost). Important: because `integration` also contains Clay's work, the promotion carries Clay's merged work too. The dashboard release cannot be shipped without it, and Clay's unreleased work cannot be held back. Release size is bounded by the slices: each reviewed unit is small, and the promotion is a roll-up of already reviewed slices. Merge with a merge commit so that `master` and `integration` keep a common history (general git behaviour: UNVERIFIED here).

**Q5. Flags, trunk-based alternatives, are long-lived release branches justified.** This proposal says no. Reasons from the research: trunk-based branches last about two days (S1); DORA calls a batch over a week too big and says small batches are the countermeasure to AI-driven instability (S6); Fowler says higher integration frequency is the way out of long-branch trouble (S8); Faros vendor data shows review queues breaking under big AI diffs (S19). Dark landing replaces the isolation a release branch gave: flags or branch by abstraction (S6, S20). What it costs: flag debt (retire each flag when the release ships, S20), and discipline in how stories are sliced. How practical flags are in this repository's dashboard code is UNVERIFIED and is the first thing to test on one story.

**Q6. Hotfixes and bug fixes during a release.** Normal path: fix on `integration` as a slice, and if the fix must reach shipped code, cherry-pick it into `master` through a pull request (Microsoft Release Flow: fix on trunk first, then cherry-pick, S9; S2). Emergency path when `integration` holds unreleased work that cannot ship: branch `fix/<issue>-<slug>` from `master`, pull request into `master`, then immediately a `master` into `integration` sync pull request as part of the fix's definition of done; this is the one case where the S2 rule (never fix downstream first) is broken on purpose, because here `master` is the downstream production branch. The 1.1 bug-fix releases are ordinary slices followed by a promotion. The 1.105 test-only releases are slices that only add tests; they ship dark or live with no flag.

**Q7. Clean-up and what is kept.** Story branches deleted on merge; worktrees removed by the coordinator after the merge. `release/dash1.3` deleted after the promotion merges; tag `dash/1.3` on the promotion commit. `.dev/` records ride in each slice's pull request. The ledger problem: CONTEXT says `sprint-status.yaml` is tracked on the release branch being executed and written only by the coordinator (line 14). Here there is no release branch, so each ledger update would be a pull request into `integration`, or the ledger lives in the coordinator's own branch until promotion. This is a real mismatch and the biggest process cost of this proposal.

**Q8. Fit with `integration` and Clay's habit.** It is Clay's habit, scaled up: branch from `integration`, short branch, pull request into `integration`. Dashboard slices and Clay's pull requests meet in `integration` continuously, so path collisions surface at once, in CI, instead of at a sync pull request later. The cost is that the owner's sessions and Clay now share review attention (two bots and the owner) and share the promotion decision.

**Q9. Failure and rollback.** A slice that is bad after merging: revert pull request for that one squash commit, or switch its flag off. A release that fails on `master`: flag off for dark features, or revert the promotion merge commit through a revert pull request, or cherry-pick the fix into `release/dash1.3` and promote again. Because each slice is a single small commit, partial rollback is easy, which is the best rollback story of the three proposals.

## 5. What it costs

- The owner clicks merge on every slice. With bursts of 15 to 60 AI-made pull requests in a few days (CONTEXT line 16) that is the heaviest merge load of the three, and "nothing is merged by an agent" is a standing rule.
- Every slice pays for CI plus both reviewers: more CI minutes and more review events. Reviewer saturation is the exact bottleneck reported for AI-heavy teams (S19, vendor data; DORA's AI note in S6).
- Stories must be sliced and designed to land dark. Flags create debt that must be retired (S20).
- The ledger-on-the-release-branch convention does not fit.
- The dashboard release is entangled with Clay's content at promotion time.

## 6. Who it favours

Clay and anyone optimising for flow and continuous integration; the DORA and trunk-based evidence is on its side. It disfavours the owner's coordinator-controlled model and the one-merge-per-release comfort.

## 7. Risks

1. Owner merge load and reviewer load; most likely failure is a queue of ready slices waiting for the owner.
2. Dark landing may not be practical for stories that change existing dashboard behaviour (UNVERIFIED).
3. `integration` can go red because of someone else's merge, stalling all slices (a shared trunk is shared).
4. Promotion bundles Clay's work with the release; a bad Clay change blocks the release.
5. Ledger writes and `.dev/` records become extra pull requests.
6. Flags forgotten after the release ship as permanent dead branches (S20).

## 8. Sources that support it

- S1 trunkbaseddevelopment.com, short-lived branches (two days, many small PRs per story, no merges to release branches).
- S2 trunkbaseddevelopment.com, branch for release (cut just in time, fix on trunk then cherry-pick, CD teams do not branch).
- S6 DORA, small batches (AI countermeasure, one-week limit, dark launching).
- S8 Fowler, integration frequency and release branches.
- S9 Microsoft Release Flow (trunk-based plus a release branch per release).
- S11 GitHub Docs events (CI base-branch filter; here the existing `integration` filter is enough).
- S12 GitHub Docs automatic branch deletion.
- S19 Faros review-burden numbers (vendor, cited as risk).
- S20 Unleash (flags, retire them, short-lived release branches).
