# GFxAI branching-document search log (2026-11-23)

Scope: read-only GitHub calls (`gh repo view`, `gh api` GET, `gh search code`, `gh pr list/view`) against the owner's organisation repositories. No clone, no fetch, no GitHub or git writes. No credentials read or printed. One scratch file (`/tmp/gfxai-tree-paths.txt`, a list of file paths) was made and deleted; nothing else was written outside this folder.

Status words used below: READ = I opened and read the text. SKIMMED = I read only grep hits or the first part. UNVERIFIED = not opened.

## 1. Repositories searched (in the order the coordinator asked)

| Repo | Default branch | Last push | Result |
|---|---|---|---|
| IronbellyGroup/GFxAI | `master` | 2026-10-21 | Found the branching documents (section 3). |
| IronbellyGroup/GFxAI-Parallel | `main` | 2025-12-06 | Tree has one file, README.md: "Parallel project of GFxAI for AI Development Testing". Nothing on branching. |
| IronbellyGroup/GFxAI-Backlog-md | `main` | 2026-07-27 | A copy of the open-source Backlog.md task tool (992 files). Only branching text: CONTRIBUTING.md line 13, "create a branch named after the task ID". Not the owner's strategy. |
| GFxAI-brownfield-docdrop, GFxAI-Product, GFxAI_V0.1, GFxAI-UE-Manager, GFxAI_PixelStreaming | n/a | n/a | NOT SEARCHED (UNVERIFIED). The coordinator said to widen only if nothing was found; something was found. |

## 2. Calls made (what and why)

1. `gh repo view` on the three first repos: default branch, push date, privacy (all private).
2. `gh api repos/.../branches` on the three repos: the branch names actually used.
3. `gh api repos/.../git/trees/<branch>?recursive=1` on all three: file lists (GFxAI tree has 23,163 entries, not truncated). Filtered the path list for: branch, git, workflow, contribut, release, worktree, merge, trunk, hotfix, parallel, agent, strategy, gitflow, branching.
4. `gh search code --repo IronbellyGroup/GFxAI` for: "branching strategy", "gitflow" (0 hits), "release branch", "integration branch", "trunk-based" (0 hits), "feature branch", "squash", "hotfix". Code search covers the default branch only.
5. `gh api .../contents/<path>` (GET, raw) to read the hits listed in section 3; `gh api .../commits?path=` for dates and authors.
6. `gh pr list --state merged --limit 40` and `gh pr view` (numbers 144, 146, 147, 129) for the merge style and size of real pull requests; `gh api repos/.../branches/master/protection`, `.../branches/release/v0.1/protection`, `.../rulesets`, `.../compare/master...release/v0.1`, `.../tags`, `.../releases` for how the rules are actually set.

## 3. What was found (GFxAI, default branch `master`)

### 3.1 Primary document: the branching rules
- Path: `docs/docs-product/ops/git-standards-protocols.md` (35,340 bytes, 880 lines). READ in full except the last ~120 lines (pre-commit hooks, security section; not about branching).
- Frontmatter: id `GFXAI-GIT-STANDARDS-PROTOCOLS`, `version: "1.0"`, `status: "To Do"`, `created_date: "2025-12-11"`, `updated_date: "2025-12-11"`, `assigned_to: "engineering-team"`. No author named inside the file.
- Only commit the path-filtered history shows: 2026-02-12, clayphi, b89bc48d1, "Merge wizard-integration into master (#82)". So the first appearance on `master` is a merge commit; the true author of the text is UNVERIFIED (the file is dated 2025-12-11 and the same text sits unchanged on feat/OntRAG, release/v0.1, docs/knowledge-brain-tech-reference).
- Its own checklist says Sections 1, 6 (Release and Tagging) and 10 are "To Do" and "Reviewed by engineering-team - Pending team review". Quote: "Section 6: ... **To Do** (No prework)".
- Section 2 "Branching Strategy" and Section 7 "Hotfix Procedures" are marked Done.

### 3.2 Companion document: the worked release example
- Path: `docs/docs-product/ops/development-methodology.md` (721 lines). READ lines 1-25 and 420-720; the rest SKIMMED by grep.
- Frontmatter: `status: "Active"`, created and updated 2025-12-11. Same single history entry (2026-02-12, clayphi, #82).
- Contains a fictional "Release 1.0 - Game Configuration Wizard" walk-through with people (Clay as product manager, two "AI-Developer" roles) each on a branch `release-1.0/feature/GFXA-10x-...`.

### 3.3 Where the rule is surfaced to AI agents
- `CLAUDE.md` section "Git Branching Workflow" (lines 447-456, file last touched 2026-10-20 by clayphi) and the same in `CODEX.md` (lines 444-453). Quote: "Follow PR-based promotion (`feature/bugfix/docs` -> `release/*` -> `main`)". It names the two docs above as "Source of truth".
- Also in CLAUDE.md: "NEVER push commits to remote/PR unless the user explicitly requests it."

### 3.4 Earlier drafts and older rule
- `docs/docs-product/product_prework/product-archive/git-protocol-prework.md` and `.../Development Approach.md`: the pre-draft of the same model (release/X.Y lines, `hotfix/<version>-<description>`). SKIMMED by grep.
- `docs/archive/AGENTS.md` (archived 2026-02-26): older rule "Always treat `development` as the main integration branch" and "Do **not** merge directly into `master` from a feature branch". Superseded by the above (it sits in an archive folder; no `development` branch exists today). READ the first 30 lines.

### 3.5 The audit that says the documents are stale, and the owner decision
- Path: `.dev/tasks/to-do/docs-audit-post-merges/TASK-RESEARCH-docs-audit-20260518-133127/research/22-git-standards-and-methodology.md` (53,371 bytes, dated 2026-05-18, committed in a 2026-10-20 bulk commit by clayphi). READ lines 1-140, 230-260, 308-384, 463-488.
- Its verdict on the primary document: "STALE - material divergence from current `.github/workflows/cicd-pipeline.yml`" and a "wholesale rewrite needed".
- "Open Question Q1 - RESOLVED (2026-05-19 user decision)": rewrite the docs to match the running pipeline, except keep the nested feature-branch naming `<release-name>/feature/<ticket-id>-description` as "enforced future-state". Production branch is `master`; release patterns `release/**`, `release-*`, `rel-*`; feature branches get CI on pull request only. Quote: "Downstream `/task-builder` MUST treat this as binding."
- The rewrite did NOT land: `docs/devops/git-standards-protocols.md` (the new location the decision names) returns 404 on `master`, and the old file still says `version 1.0`, `main`, and Tier 1/2/3. The related task folder is still under `.dev/tasks/to-do/`.

### 3.6 Other documents SKIMMED and judged not to be the branching strategy
- `.dev/releases/current/feature-Ont-RAG/adversarial-release-strategy/merged-release-strategy.md` (2026-03-10): how to split one feature into releases R0 to R3 (scope slicing, blast radius per release). Has one branch-related line (line 453, "Three merge operations: Smaller PRs are more reviewable"). It is about release scope, not branch topology.
- `docs/devops/cicd-pipeline-and-deployment-process-guide.md` (v4.0): CI triggers (`[main, master, 'release/**', 'release-*', 'rel-*']`); its worked example still says "branch from the `develop` branch" (lines 222, 412), another stale line.
- `.dev/research/ironclaude-cicd-adoption-20260603/findings-03-merge-governance.md` (about IronClaude, the repo we are in; not GFxAI's rule).
- `.dev/tasks/to-do/strategic-research/TASK-RESEARCH-agile-workflow-llm-era-20260428-071644/research/02-first-principles.md` line 47: "Release branching / merge-train coordination ... [STILL NEEDED]". An AI-era note that branching survives; no rule.
- `.dev/releases/complete/Wizard_MegaMerge/conflict-resolution/KNOWLEDGE_LOG.md`: record of one large conflict resolution ("Accept master's deletions"). A lesson, not a rule.

## 4. What the repository actually does (not what the documents say)

- Branch names now (about 40 branches): 4 named `proto-demo/feature/...` (nested under the release name, as documented), `release/proto-demo`, `release/v0.1`, `rel-0.01-taskManager`, `feat/OntRAG` plus `feat/OntRAG-r2` and `feat/OntRAG-r2.5-hybrid-norag`, `OntRAG/bugfix/...`, `OntRAG/ci/...`, and many plain `feature/...` and `bugfix/...`. 6 `backup/local-20261019/...` branches.
- Last 40 merged pull requests (#97 to #152): about 30 go `feature|bugfix|chore|cleanup|docs/... -> master` directly. The `release/*` step of the document is not used for them.
- The one real "long-lived branch with sub-branches" case: `feat/OntRAG`. Sub-branches `feat/OntRAG-r2` (#144), `OntRAG/ci/cicd-pipeline-redesign` (#145), `OntRAG/bugfix/pixel-streaming-input-fixes` (#146) merged INTO it; master merged INTO it twice (#129 on 2026-03-21, #131 on 2026-03-23, titled "Merging from main" and "Merging Main In"); then it landed on master as #147 on 2026-05-18: 1,384 files changed, +242,976 / -1,433 lines, 34 commits; merge commit text "Merge PR #147 (Feat/OntRAG) into master with file-level rejections".
- `release/v0.1`: 0 commits ahead, 62 behind master (compare API, 2026-11-23) and not protected: the release branch exists but is not used as the documents say. Tags: `v0.1`, `rel-0.01_taskManager`, `stable-revert-point`, `active`.
- Merge style on master history: mixed. Merge commits with two parents for #146, #147, #148 and merges of master into branches; single-parent commits for #149 and for direct docs commits by one owner. Repo settings: merge commit, squash and rebase all allowed; "delete branch on merge" is off.
- Branch protection on `master` (live API, 2026-11-23): 1 approving review required, code owner review required, stale reviews dismissed, required status check "Claude PR Review", pushes restricted to two users (ironbelly, clayphi), force pushes and deletions off, linear history off, signed commits off. No rulesets. No protection on `release/v0.1`.
- AI agents in this repo: the document's role table gives "AI Agent" no push, no force push, no approval, no merge. CLAUDE.md adds "NEVER push ... unless the user explicitly requests it."

## 5. Verdict of the search
FOUND. One documented approach exists (`git-standards-protocols.md` plus `development-methodology.md`, both dated 2025-12-11, version 1.0), plus a 2026-05-19 owner decision that amends it but was not written back. See `gfxai-approach.md`.

## 6. Limits
- Five repos not searched (see section 1). `gh search code` indexes only default-branch content and can lag; the tree listing of GFxAI `master` (not truncated) was used as the cross-check.
- Who wrote the original 2025-12-11 text is UNVERIFIED.
- Branches other than `master`, `feat/OntRAG`, `release/v0.1`, `release/proto-demo`, `docs/knowledge-brain-tech-reference` were not searched for newer copies of the document (`release/proto-demo` has no copy of it).
