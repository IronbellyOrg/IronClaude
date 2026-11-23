# Proposal 4: the GFxAI approach, rewritten for this repository (2026-11-23)

Source: the owner's organisation repository IronbellyGroup/GFxAI, `docs/docs-product/ops/git-standards-protocols.md` and `development-methodology.md` (both 2025-12-11, version 1.0, the first a draft marked "Pending team review"), plus the 2026-05-19 decision in the docs audit and what the repository really does. Full evidence is in `gfxai-approach.md` and `gfxai-search-log.md`. Questions are the nine in `CONTEXT.md`.

Marks: FROM SOURCE = the GFxAI text says this. FROM PRACTICE = GFxAI does this in its real history, though no document says so. MY ADAPTATION = my change to fit the facts in CONTEXT.md; the source is silent or says otherwise. UNSPECIFIED = the source has no answer and I add none.

## In one paragraph
Each release gets one temporary branch `release/<release-name>`; the work branches live under the release NAME (not under `release/`), so no git ref conflict arises; each piece of work reaches the release branch by a pull request that is squash-merged; the release lands on `master` by one pull request with the full tests and approvals, then is tagged; emergency fixes branch from `master` and are copied into any open release branch. This is the classic "release branch with feature branches" model, not trunk-based.

## The rules, in order of the nine questions

### 1. Names
- Release branch: `release/dash1.3`. FROM SOURCE (pattern `release/<release-name-version>`, example `release/investor-demo-1.0`).
- Work branches: `dash1.3/<kind>/<id>-<slug>` where kind is `story`, `bugfix` or `docs`, for example `dash1.3/story/01-widget-grid`. FROM SOURCE for the shape `<release>/<feature|bugfix|docs>/<ticket>-<description>`; MY ADAPTATION for the word `story` and a two-digit story number (zero padded so they sort).
- No ref conflict: `release/dash1.3` and `dash1.3/story/01-...` are in different folders, so git accepts both. FROM SOURCE, and FROM PRACTICE (`release/proto-demo` and `proto-demo/feature/wizard-integration` both exist in GFxAI). This is the fix for the `dash1.3` versus `dash1.3/story1` clash recorded in CONTEXT.md.
- Hotfix: `hotfix/<id>-<slug>`. FROM SOURCE.
- Carries the release number and the story id: yes, in the folder and the leaf name. Sorting: yes inside `dash1.3/story/`.
- Orca prefix `ironbelly/`: MY ADAPTATION, not addressed by the source. If `orca worktree create --branch` does not stop the prefix, every name gets `ironbelly/` in front; the rule still holds because the prefix is the same on every branch. UNVERIFIED whether `--branch` keeps the name exact.
- One difference to flag: in the source a feature branch is a WHOLE product feature holding many stories ("NOT = One task or one user story"). The owner's model has one branch per story. The names above follow the owner's model; the source's rule on size is not kept.

### 2. Where story work merges and how
- By pull request from the story branch into `release/dash1.3`, with the tests for that level and at least one review. FROM SOURCE ("Create PR from feature/* into release/* branch").
- Merge method: squash into the release branch (one commit per story). FROM SOURCE ("Squash merge to release").
- Inside a story branch: no merge commits, rebase to stay current. FROM SOURCE ("Rebase-only policy"). It clashes with `/sc:pr-submit`, which never rewrites a published branch; see `gfxai-fit.md`. MY ADAPTATION: rebase only before the first push; after that, merge the release branch into the story branch.
- Who resolves conflicts: the branch owner, because the PR "must be up-to-date with target branch, no merge conflicts". FROM SOURCE. In this repository the owner of a story branch is the story's AI session; MY ADAPTATION: a conflict is stopped and reported to the coordinator, never resolved automatically (worker contract in CONTEXT.md).
- Protection against two AI stories colliding: the source has Interface-First design and mocks so parallel work does not collide, and nothing about file paths. MY ADAPTATION: the two parallel stories name disjoint paths in their specs; the coordinator merges one story at a time.
- Who merges: the source gives AI agents no merge right ("AI Agent: Merge to Main no"). MY ADAPTATION: the coordinator, not the story session, runs the story merge into the release branch; the owner merges the release into `master`.

### 3. Keeping the release branch current with `master` and `integration`
- The source says only that a pull request must be "up-to-date with target branch". UNSPECIFIED for the release branch.
- FROM PRACTICE: GFxAI's long-lived branch `feat/OntRAG` took `master` in by merge twice (pull requests #129 on 2026-03-21 and #131 on 2026-03-23, titled "Merging from main" and "Merging Main In") and still landed as one 1,384-file pull request.
- MY ADAPTATION: merge, never rebase, `master` and `integration` into `release/dash1.3`, done by the coordinator between two story merges (never mid-merge). Reason: stories branch from the release branch, and `/sc:pr-submit` never rewrites a published branch. Do it at least before each release-readiness check and before the release pull request.

### 4. How the release lands
- One pull request `release/dash1.3` into `master`, with the full test tiers, two approvals and sign-off, then a tag and deploy. FROM SOURCE (PR to main needs "Tier 1 + Tier 2 + Tier 3", "Code review, UAT sign-off"; methodology: "Tag: `v1.0.0`").
- Opened with `/sc:pr-submit --monitor 3 --base master`: MY ADAPTATION (the repository's own rule for opening PRs). CI and the two reviewers run once, at that point.
- Not through `integration`: the source has no such branch. MY ADAPTATION: straight into `master`, then `master` is merged back into `integration` so Clay's base is current.
- Merge method for this pull request: UNSPECIFIED in the source. MY ADAPTATION: a merge commit, so the release lands as one revertable unit and each story stays one commit in history.
- Tag: MY ADAPTATION: `dash-1.3` (not `v1.3.0`; the package is 6.1.0 on `master`).
- Size warning, FROM PRACTICE: GFxAI's release-sized pull request #147 had 34 commits, 1,384 files, +242,976 lines and was merged "with file-level rejections".

### 5. Feature flags, trunk-based, long-lived release branches
- The source keeps long-lived release branches; its methodology table calls a release "Weeks-months". It mentions feature flags once ("Feature flags allow partial rollout", in Dev) and has no flag policy and no trunk-based option. FROM SOURCE.
- Whether a release branch is justified at AI speed: UNSPECIFIED; the source does not ask. MY ADAPTATION: keep the release branch (it is the owner's stated model and the progress ledger lives on it) but keep stories short-lived, which GFxAI's 242,976-line landing argues for.

### 6. Hotfixes and bug fixes during a release
- Non-urgent bug found while the release is open: `dash1.3/bugfix/<id>-<slug>`, merged into `release/dash1.3` like a story. FROM SOURCE.
- Urgent production bug: branch from `master`, pull request into `master`, expedited review, then copy the fix into every open release branch by cherry-pick or merge. FROM SOURCE ("Do NOT branch from release/*").
- Bug-fix releases (1.1) and test-only releases (1.105): MY ADAPTATION: each is just another release branch (`release/dash1.1`, `release/dash1.105`) with a short list of `bugfix` or `docs` branches; the source has no numbering scheme for them. UNSPECIFIED.
- Beta freeze: when the release is in final testing, only critical fixes are allowed into the release branch. FROM SOURCE.

### 7. Clean-up
- The source marks all these branches "Temporary" and gives no deletion rule. FROM SOURCE for "temporary"; the rest is MY ADAPTATION.
- MY ADAPTATION: delete a story branch and remove its worktree once its squash commit is in the release branch and recorded in the ledger. Delete the release branch and its worktree once the release pull request is merged into `master` and the tag exists. Keep: the tag, the squash commits, and the `.dev/` records committed on the release branch.
- Why add a rule: FROM PRACTICE GFxAI left 6 `backup/...` branches and `release/v0.1` (0 ahead, 62 behind `master`) because "delete branch on merge" is off and no rule exists.

### 8. Fit with `integration` and Clay's habit
- The source has `main <- release/* <- feature/*`; this repository's CLAUDE.md has `master <- integration <- feature/*`. In both, a middle branch collects work before the production branch. MY ADAPTATION: leave `integration` as it is for Clay's pull requests; a dashboard release does not pass through it; `integration` is merged into `release/dash1.3` before the release pull request (question 3) and receives `master` after the release lands (question 4).
- The source is silent on a permanent integration branch, and its archived rule "Always treat `development` as the main integration branch" was superseded (`docs/archive/AGENTS.md`). UNSPECIFIED.

### 9. Failure and rollback
- The source has no rollback rule; its only recovery text is the hotfix flow and a Tech-Lead emergency override. UNSPECIFIED.
- MY ADAPTATION: a bad story after merging: revert its single squash commit on the release branch with a new commit (no history rewrite). A release that fails on `master`: revert the release's merge commit on `master` (needs the merge-commit landing in question 4), fix on the release branch, and open a new pull request.

## What this proposal needs that the source does not give
Coordinator rules for parallel AI sessions (disjoint paths, serialised merges); a CI trigger for pull requests into `release/**` (this repository's `.github/workflows/test.yml` only runs for pull requests into `master` and `integration`, per CONTEXT.md; MY ADAPTATION: add `release/**` to its pull-request branch list); a rule for who may merge into the release branch; the tag scheme; bug-fix and test-only release naming; cleanup and rollback.
