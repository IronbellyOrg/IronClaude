# Fit check: does the GFxAI approach suit the IronClaude release work? (2026-11-23)

Inputs: `CONTEXT.md` (our facts F1 to F11 in the order of its "What the branching has to serve" list: F1 repo, F2 owner's model, F3 ref conflict, F4 AI workers and coordinator, F5 parallelism, F6 pull requests and CI, F7 `worker-start` has no `--branch`, F8 rules, F9 ledger, F10 release numbers, F11 scale; and its nine questions Q1 to Q9), `proposal-4-gfxai.md`, `gfxai-approach.md`, `gfxai-search-log.md`. Marks: UNVERIFIED = I did not read or test it.

## Verdict
ADOPT WITH NAMED CHANGES: take the skeleton (release branch plus work branches under the release name, release lands on `master` by one fully-gated pull request, hotfix from `master` and copied into open releases), and change or add the seven items under "Named changes" below. Do not adopt the GFxAI documents as written.

Two facts about the source that lower its weight, both from the GFxAI repository on 2026-11-23:
1. It is not a settled rule. `git-standards-protocols.md` is version 1.0, status "To Do", "Pending team review", with its Release and Tagging section empty. A 2026-05-19 decision amended it and was not applied. The repository mostly ignores it: of the last 40 merged pull requests about 30 go straight to `master`, and `release/v0.1` is 0 commits ahead and 62 behind `master`.
2. It was written for a human team with deploy environments (Local, Dev, Test, Beta, Prod) and roles. It says nothing about parallel AI sessions, a coordinator, or worktrees.

## Item by item against the facts

| # | Our fact or question | Verdict | Evidence |
|---|---|---|---|
| F1 | `master` is default; `integration` exists; Clay branches from it | FITS in shape, GAP in detail | Source flow `main <- release/* <- feature/*` matches `master <- integration <- feature/*` in shape. Source has no `integration`; the proposal handles it by merging `integration` into the release branch and `master` back into it (MY ADAPTATION, not tested). |
| F2 | One integration branch per dashboard release, one sub-branch per story, release merges to default branch | FITS | This is the source model with one change: the source says a feature branch is a whole feature, "NOT = One task or one user story". Our stories are smaller. Naming adapts; the rule on size does not carry over. |
| F3 | `dash1.3` and `dash1.3/story1` cannot coexist | FITS, SOLVED with proof | Source puts the release under `release/` and work under the release name: `release/proto-demo` and `proto-demo/feature/wizard-integration` both exist in GFxAI today. Same effect as the `dash1.3/release` plus `dash1.3/story-...` option in F3. |
| F4 | AI sessions under a coordinator; coordinator merges settled stories locally; conflict is stopped and reported | CLASHES with the source's merge route, MISSING in the source | Source merges every promotion by pull request and gives "AI Agent" no push, approve or merge right. The source has no coordinator. Named change 1. |
| F5 | Two stories at once, disjoint paths, merges serialised | MISSING | No source rule on disjoint paths or serial merging. Only "Interface-First Design" so parallel work can proceed against mocks. Must come from our own rules. |
| F6 | `/sc:pr-submit` only way to open PRs; own top-level session; never rewrites a published branch; `--base`; CI only for PRs into `master`/`integration`; two automatic reviewers; owner merges | CLASHES in three places | (a) Source wants "Rebase-only policy" in work branches and lets the owner force-push; `pr-submit` forbids rewriting a published branch. (b) Source makes a PR per story into the release branch; here that PR gets no CI and costs two reviewers each. (c) Source wants 2 approvers on `main`; here the owner merges every pull request. Named changes 1 and 2. |
| F7 | `worker-start` has no `--branch`; exact names need `orca worktree create --branch ...` | NEUTRAL | Source says nothing about tools. Naming rule is easy to apply with `--branch`; whether Orca still adds `ironbelly/` is UNVERIFIED. |
| F8 | No commit on master; never touch upstream; no rebase of a branch others branched from; `.dev/` records on the release branch | FITS | Source also forbids direct commits to `main` and `release/*` ("PR Required: Always, Direct Push: No one"). "No rebase of a branch others branched from" is stricter than the source and wins. |
| F9 | Ledger tracked on the release branch, coordinator writes it | MISSING | Source has no ledger. Does not clash; it just lives on the release branch. Nothing to adopt. |
| F10 | Release numbers 1.1, 1.105, 1.2 ... 2.0 are not package versions | GAP | Source names releases by name and version (`investor-demo-1.0`), tags `v1.0.0`. Reusing `v1.3.0` here would look like a package version (package is 6.1.0). Needs our own tag scheme (proposal: `dash-1.3`). |
| F11 | Bursts of 15 to 60 AI-made PRs in days | CLASHES | Source assumes a release lasts "Weeks-months" and a review "Within 24 hours". GFxAI's own large release PR (#147) had 34 commits, 1,384 files and +242,976 lines. It shows what one big landing looks like, not that it works at AI speed. |
| Q1 | Names | FITS | See F3. Add the zero-padded story number for sorting (MY ADAPTATION). |
| Q2 | Where and how stories merge | PARTLY FITS | Squash into release: fits (one revertable commit per story). PR per story: does not fit F4 and F6. Rebase-only: does not fit F6. Named changes 1, 2, 3. |
| Q3 | Keep the release branch current | SOURCE SILENT, PRACTICE HELPS | Source: "up-to-date with target branch" only. GFxAI practice: merged `master` into `feat/OntRAG` twice in two months (#129, #131) and still landed with "file-level rejections". Merge-not-rebase is forced here by F6 and F8. Named change 4. |
| Q4 | How the release lands | FITS | Source: pull request `release/*` into `main`, full tests, two approvals, tag. Matches "one PR per release into master". Source has no `integration` step and no merge method; proposal picks a merge commit. |
| Q5 | Flags or trunk-based; are long-lived branches justified | SOURCE SILENT | One line on feature flags; no trunk-based discussion; no justification of long-lived release branches at AI speed. This question stays open; the source does not help answer it. |
| Q6 | Hotfixes, bug-fix releases, test-only releases | FITS, with gap | Hotfix from `master` and copied into open releases fits F10's bug-fix releases as ordinary small release branches. No numbering for 1.1 / 1.105 in the source. |
| Q7 | Clean-up | SOURCE SILENT, PRACTICE WARNS | Source: "Temporary" and nothing else. GFxAI left 6 `backup/...` branches and a dead `release/v0.1` ("delete branch on merge" off). Needs our own rule (in the proposal). |
| Q8 | Fit with `integration` and Clay | GAP | Source has no permanent integration branch; its archived `development` rule was superseded. Proposal's handling is untested against Clay's habit (12 of 12 recent integration PRs were his, per CONTEXT.md). |
| Q9 | Failure and rollback | SOURCE SILENT | Only hotfix and a "Tech Leads only" emergency override. A tag `stable-revert-point` exists; its use is UNVERIFIED. Revert-by-commit rule is mine. |

## Parts of the source that do NOT fit and should be dropped
- Five environments and Tier 1/2/3 test levels by target branch (the 2026-05-19 decision already replaced them with three CI gates).
- Role table (Tech Lead, Release Manager, Senior Developer) and "2 approvers" on `main`: this repository has one owner who merges.
- Signed commits on `main` and `release/*`: not a rule here (UNVERIFIED whether the fork requires it).
- "Feature branch = whole feature with many stories": our unit is the story.
- "Owner may force-push own branch": contradicts `/sc:pr-submit`.

## Named changes (what "adopt with named changes" means)
1. Story merges into the release branch are local, coordinator-run, squash merges, not pull requests. Reason: a story pull request into a release branch gets no CI (F6), needs its own top-level `pr-submit` session, and brings two reviewers per story at 15 to 60 stories per burst (F11). CI and the two reviewers then run once, on the release pull request. This matches what `CONTEXT.md` F6 already says is "to be confirmed".
2. The release pull request is opened with `/sc:pr-submit --monitor 3 --base master` and the owner merges it (one approval, not two).
3. Drop "rebase-only". Rebase only before the first push; after that, merge. A story branch is never force-pushed.
4. The coordinator merges `master` and `integration` into the release branch between story merges, at least before the release pull request, and merges `master` back into `integration` after the release lands. Never rebase.
5. Add what the source lacks: disjoint paths per parallel story and serial merges (F5); cleanup of story and release branches and worktrees after each merge (Q7); revert-by-commit for a bad story or a failed release (Q9); a release tag `dash-<n>` (F10).
6. Name branches `release/dash1.3` and `dash1.3/story/<nn>-<slug>` (and `bugfix`, `docs`), per F3 and F7.
7. If the owner later wants story pull requests, add `release/**` to the pull-request branches in `.github/workflows/test.yml` first (CONTEXT.md F6 says it covers only `master` and `integration`; I did not read the workflow file myself, UNVERIFIED).

## What I did not read or check
- Last ~120 lines of `git-standards-protocols.md` (pre-commit hooks, security); `development-methodology.md` lines 26-419 beyond grep hits.
- The five repositories not searched (`GFxAI-brownfield-docdrop`, `GFxAI-Product`, `GFxAI_V0.1`, `GFxAI-UE-Manager`, `GFxAI_PixelStreaming`). Any of them could hold a newer or different rule.
- Who wrote the 2025-12-11 text and who made the 2026-05-19 decision (the owner or someone else): UNVERIFIED. If the owner's own statement of the "decided approach" differs from these documents, the owner's statement wins and this file should be re-checked against it.
- This repository's `.github/workflows/test.yml`, worker contract and `/sc:pr-submit` code: relied on the facts in `CONTEXT.md`, not re-read.
