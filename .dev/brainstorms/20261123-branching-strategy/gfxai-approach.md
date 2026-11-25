# GFxAI branching approach: what the owner's organisation documented (2026-11-23)

Source repository: IronbellyGroup/GFxAI (private, default branch `master`). All facts below come from read-only GitHub calls on 2026-11-23; see `gfxai-search-log.md` for each call. Marks: READ = I read the text; SKIMMED = grep hits only; UNVERIFIED = not checked.

## 1. Where it is documented

| What | Path (all in IronbellyGroup/GFxAI) | Dates | Read? |
|---|---|---|---|
| The branching rules (branch kinds, naming, promotion, protection, PR rules, hotfix) | `docs/docs-product/ops/git-standards-protocols.md` | created and updated 2025-12-11, version 1.0; reached `master` in a merge commit 2026-02-12 (clayphi, "Merge wizard-integration into master (#82)") | READ (about 760 of 880 lines) |
| A worked release example, with a team and AI roles | `docs/docs-product/ops/development-methodology.md` | same dates and same commit | READ (lines 1-25, 420-720) |
| The short rule that AI agents see | `CLAUDE.md` lines 447-456 and `CODEX.md` lines 444-453 | CLAUDE.md last changed 2026-10-20 (clayphi); the branching lines themselves are older (date UNVERIFIED) | READ |
| An audit that calls the two documents stale, plus a dated decision about what to keep | `.dev/tasks/to-do/docs-audit-post-merges/TASK-RESEARCH-docs-audit-20260518-133127/research/22-git-standards-and-methodology.md` | report 2026-05-18; decision recorded 2026-05-19 | READ (parts) |
| Older drafts | `docs/docs-product/product_prework/product-archive/git-protocol-prework.md`, `.../Development Approach.md`, `docs/archive/AGENTS.md` (archived 2026-02-26) | undated or earlier than 2025-12-11 (UNVERIFIED) | SKIMMED / first 30 lines |

Who wrote the 2025-12-11 text is UNVERIFIED. The only history entry is a merge commit by clayphi (the other maintainer of IronClaude per CONTEXT.md; whether `clayphi` is the same person as "Clay" in CONTEXT.md is likely but UNVERIFIED). The methodology example names "Clay" as product manager.

## 2. Status, and where the documents disagree

- `git-standards-protocols.md`: frontmatter `status: "To Do"`, and its own checklist says "Reviewed by engineering-team - Pending team review". So it is a DRAFT version 1.0 that was never marked reviewed or active. Its Section 6 (Release and Tagging) says "To Do (No prework)".
- `development-methodology.md`: `status: "Active"`. Same date.
- The 2026-05-19 decision in the audit report ("Open Question Q1 - RESOLVED (2026-05-19 user decision)", "MUST treat this as binding") changes the rules. It was never written back: the file is still version 1.0 and `docs/devops/git-standards-protocols.md`, the new path the decision names, does not exist on `master` (404). So the decision is DECIDED BUT NOT APPLIED. Who "user" is in that report is UNVERIFIED (the report cites a local path under `/Users/cmerritt/`; who that is, I did not establish).
- `docs/archive/AGENTS.md` (archive, 2026-02-26): "Always treat `development` as the main integration branch." SUPERSEDED (no `development` branch exists).
- `docs/devops/cicd-pipeline-and-deployment-process-guide.md` v4.0 still says "branch from the `develop` branch" in its worked example: a third stale name.

Disagreements, newest word first:

| Point | Document says (2025-12-11) | Newest decision (2026-05-19, not applied) | What the repository does (2026-11-23) |
|---|---|---|---|
| Production branch | `main` | `master` | `master` |
| Release branch name | `release/<name>` | `release/**`, `release-*` or `rel-*` | `release/v0.1`, `release/proto-demo`, `rel-0.01-taskManager`; most work goes straight to `master` |
| Feature branch name | `<release>/feature/<ticket>-<desc>` | keep it, enforced from 2026-05-19 | 4 `proto-demo/feature/...` branches (all older than that date); later branches are plain `feature/...` or `feat/...` |
| Test tiers | Tier 1/2/3 by target branch | Gate 1/2/3 as in the CI file | CI gates run on pull requests only |
| Environments | Local, Dev, Test, Beta, Prod | Local, CI, Staging, Production | not checked |
| Merge into release | squash | not changed | mixed (see `gfxai-search-log.md` section 4) |

The newest source is the 2026-05-19 decision; the most complete source is the 2025-12-11 document. This note uses the document as the base and marks where the decision changes it.

## 3. The rules in plain English (from `git-standards-protocols.md` unless noted)

Branch kinds and names
- `main` (the decision says `master`): production code. Permanent.
- `release/<release-name-version>`, for example `release/investor-demo-1.0`: one branch per release cycle; used to prepare and stabilise a release. Temporary.
- Feature branch `<release-name>/feature/<ticket-id>-<description>`, for example `investor-demo-1.0/feature/GFXA-101-asset-manifest`. A feature branch is a whole PRODUCT FEATURE with many stories and tasks, "NOT = One task or one user story". Temporary.
- `<release-name>/bugfix/<ticket-id>-...` for non-urgent fixes during development and `<release-name>/docs/<ticket-id>-...` for documentation only. Same workflow as a feature.
- `hotfix/<ticket-id>-<description>`: emergency production fix.
- The slash trick: the release branch lives under `release/` and the work branches live under the release NAME, so the two never collide as git refs. Evidence that this works: `release/proto-demo` and `proto-demo/feature/wizard-integration` both exist in GFxAI today.

Where work merges and how
- Work flows: local work -> pull request into the feature branch -> pull request from feature into `release/<name>` -> release is tested -> pull request from `release/<name>` into `main` -> deploy. Each promotion is a pull request ("Create PR from feature/* into release/* branch").
- Merge method: "Squash merge to release" (PRs into `release/*`). "No merge commits in feature branches ... Rebase-only policy".
- Every promotion needs the tests of its level to pass and at least one review; into `main` two approvers (Tech Lead plus one other). Approvals are dismissed when new commits arrive.
- "Branch must be up-to-date with target branch, no merge conflicts."
- Ownership: the person who creates a branch owns it; the owner may push and force-push their own feature branch; anyone else must open a pull request into it and the owner approves.

Parallel work and AI agents
- Parallel work is people (and AI roles) each on their own feature branch under one release. The worked example gives "AI-Developer 1" and "AI-Developer 2" each a feature branch (`release-1.0/feature/GFXA-103-wizard-service`, `...GFXA-104-wizard-ai`). Interfaces are agreed first ("Interface-First Design") so work can proceed in parallel against mocks.
- The role table gives "AI Agent": direct push no, force push no, PR approval no, merge to main no. CLAUDE.md: "NEVER push commits to remote/PR unless the user explicitly requests it."
- NOTHING about git worktrees, a coordinator, serialised merges, or disjoint file paths between parallel AI sessions was found (search terms "worktree", "parallel agents" gave no branching rule). See Section 5.

Releases
- Release branch is frozen in Beta: "no new features allowed; only critical bug fixes". Fixes go through a shortened cycle and then into the release branch.
- After the release pull request merges into `main`: tag `v1.0.0` and deploy (methodology document, Stage 7). Automation can create the release-to-main pull request and generate release notes.
- Signed commits are required on `main` and `release/*` (a rule in the document; GFxAI's live `master` protection has signed commits off).
- Release numbering: the document uses release names with versions (`investor-demo-1.0`, `investor-demo-2.0`). A release is a "packaged set of features, fixes, and improvements".

Hotfixes
- Branch from `main` only, never from `release/*`. Minimal change, tests, expedited review, pull request into `main`, deploy, smoke test. Then "cherry-pick or merge the fix" into any active `release/*` branch.
- Allowed only for critical production bugs, security holes, data integrity, outages.

Feature flags
- One line: in the Dev environment "Feature flags allow partial rollout" (methodology Stage 4). No flag policy otherwise.

Clean-up
- The branch table has a "Lifetime" column: feature, bugfix, docs, hotfix and release branches are "Temporary". No rule says when or who deletes them. GFxAI repository setting "delete branch on merge" is off (live), and branches such as `feat/OntRAG` and `release/v0.1` remain.

Rollback and failure
- No rollback rule for a bad story or a failed release. The only recovery text is the hotfix flow and the emergency override ("Tech Leads only", "Follow-up: Must create follow-up PR within 24 hours"). A tag `stable-revert-point` exists in the repo (a tag name only; its use is UNVERIFIED).

## 4. Reasoning recorded

- The documents give brief reasons only: "Ensures consistent, traceable, and high-quality code contributions" and "clean, professional repository history".
- The prework file adds one design remark: "a feature branch aligns with a product feature. Feature branches are not one task or one user story, they are a full feature (which contains many stories and tasks)".
- No external research (articles, other teams' models) is cited. The release strategy file `merged-release-strategy.md` (2026-03-10, adversarial debate, "convergence: 0.85") is about slicing a feature into releases R0 to R3, not about branches.
- The 2026-05-19 decision gives its rule per dimension ("code" or "doc" as source of truth) but the reason is only "match running code", except for feature-branch naming, which it keeps as "prescriptive going forward".

## 5. What is NOT documented (checked, nothing found)

- Worktrees; coordinators; serialising merges between parallel AI sessions; file-path disjointness between stories.
- How a release branch stays current with `master` (the document only says "up-to-date with target branch"; the real repository merged `master` into `feat/OntRAG` twice by pull request, #129 and #131).
- Whether the release pull request goes through an `integration` branch (no `integration` or `develop` branch exists in GFxAI now).
- Clean-up timing; rollback of a merged story; release-failure handling.
- A release identifier scheme for test-only or bug-fix releases (the owner's 1.1 / 1.105 / 1.2 numbering): not present.
