# Research notes: branching strategies for AI-agent-driven development

Date of research: 2026-11-23. Tool used: Tavily (mcp__litellm__Tavily-tavily_search / tavily_extract). No WebSearch/WebFetch fallback needed unless logged below.
Queries use generic wording only (no repo, org or owner names).

Status legend: CONFIRMED = page read with tavily_extract and the claim is on the page. UNVERIFIED = seen in a search snippet only, or not found on the page.

## Sources
(appended below as read)

### S1. trunkbaseddevelopment.com, "Short-Lived Feature Branches"
URL: https://trunkbaseddevelopment.com/short-lived-feature-branches . Read with tavily_extract 2026-11-23. Page date: none shown. CONFIRMED.
- Branch should last "a couple of days"; longer than two days risks becoming a long-lived feature branch.
- One developer per branch (two if pairing); branches are not shared for general development.
- With pull requests and review, the team-size cut-off for committing straight to trunk moved down to about 15 people; with 16 or more, short-lived branches plus CI on them is more productive.
- Forbidden ("breaking the contract"): intermediate merges of part-complete work to trunk unless it can go live alone; merges to other people's short-lived branches; merges to any release branches; other developers joining the branch.
- Pitfall: one pull request per story is a "mental trap"; several small PRs per story is the better practice.

### S2. trunkbaseddevelopment.com, "Branch for release"
URL: https://trunkbaseddevelopment.com/branch-for-release/ . Read 2026-11-23. CONFIRMED.
- Release branches are cut just in time (a few days before release), from trunk (may be an earlier chosen commit), and "should not receive continued development work".
- Fix production bugs on trunk first, then cherry-pick to the release branch; "cherry-picks from the trunk to branch ONLY" (fixing on the release branch and porting back risks a forgotten regression).
- "CD teams do not do release branches": high-throughput CD teams roll forward from trunk.
- Pairing with feature flags: land not-yet-ready work behind a flag so the cut can be from HEAD.

### S3. Vincent Driessen, "A successful Git branching model" (with 2020 note)
URL: https://nvie.com/posts/a-successful-git-branching-model/ . Post dated 2010-01-05; note of reflection 2020-03-05. Read 2026-11-23. CONFIRMED.
- Note (2020): git-flow was conceived for explicitly versioned software or software with several versions supported in the wild; for continuously delivered web apps "adopt a much simpler workflow (like GitHub flow)". "Panaceas don't exist."

### S4. GitHub Docs, "Managing a merge queue"
URL: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue . Read 2026-11-23 (page undated). CONFIRMED.
- Merge queue merges PRs FIFO; each queued PR is validated together with the latest base and the PRs ahead of it, on temporary branches with a special prefix (`gh-readonly-queue/{base_branch}`); a PR that fails is removed and the others are recreated without it.
- GitHub Actions workflows must add the `merge_group` trigger or required checks never report.
- Cannot be enabled on branch protection rules with a wildcard (`*`) in the branch name pattern. Available for public repos owned by an organization, or private repos on GitHub Enterprise Cloud (plan limit matters for a private fork; UNVERIFIED which plan the owner has).
- Useful "on branches that have a relatively high number of pull requests merging each day from many users".

### S5. GitHub Docs, "GitHub flow"
URL: https://docs.github.com/en/get-started/using-github/github-flow . Read 2026-11-23 (undated). CONFIRMED.
- Lightweight branch-based flow: branch from the default branch, commit, open PR, review, merge, delete branch. Short descriptive branch names. (The "main is always deployable" phrase is in search snippets of a third-party page, not confirmed on this page: treat as UNVERIFIED here.)

### S6. DORA, "Working in small batches" (capability page)
URL: https://dora.dev/capabilities/working-in-small-batches . Page says "Last updated: December 8, 2025". Read 2026-11-23. CONFIRMED.
- Small batches amplify the positive effect of AI adoption on product performance; "AI adoption often leads to increased software delivery instability; working in small batches acts as a critical countermeasure".
- A batch longer than a week to complete and check is too big; aim for hours to a couple of days; check small releasable changes into trunk at least once a day.
- Pitfall 2: "working in small batches but then regrouping the batches before sending them downstream for testing or release" delays feedback. (This bears directly on any end-of-release batch PR.)
- AI note: avoid generating massive pull requests; the cognitive load of reviewing machine-generated code may be higher per line.
- Dark launching / feature toggle / branch by abstraction to merge incomplete features to trunk.

### S7. DORA, 2025 report landing page
URL: https://dora.dev/research/2025/dora-report . Read 2026-11-23 (undated landing page). CONFIRMED (limited): "AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses."
- The widely repeated statement "2025: AI adoption positive for throughput, still negative for stability" was seen only in secondary pages (Bitrise, Milestone, QA.tech search snippets, not extracted). The primary report PDF was not read: that exact statement is UNVERIFIED against the primary. The instability claim itself is confirmed on S6.

### S8. Martin Fowler, "Patterns for Managing Source Code Branches"
URL: https://martinfowler.com/articles/branching-patterns.html . Extract undated (the companion "Feature Branch" bliki entry is dated 2020-05-07). Read 2026-11-23, passages returned for my query only. CONFIRMED for the passages below.
- Release train: regular cadence, dates for cutting a release branch; features target a train; once it departs the branch "will only accept fixes".
- Cherry-pick copies one commit and may not apply cleanly if it relies on commits not on the release branch.
- Writing release fixes on mainline is harder and frustrating under schedule pressure (trade-off).
- Key to escaping the long-branch trap is higher integration frequency; if a release-ready mainline cannot be kept, use a Release Branch to stabilise.
- Search snippet (not in extract passages): "Continuous Integration ... scientific evidence that it contributes to higher software delivery performance"; feature branching: "feature code only added when complete", "less frequent merges". Treat as UNVERIFIED on the extracted text, but it is the article's own summary table.

### S9. Microsoft, "Release Flow: How We Do Branching on the VSTS Team"
URL: https://devblogs.microsoft.com/devops/release-flow-how-we-do-branching-on-the-vsts-team . Undated in extract. Read 2026-11-23. CONFIRMED.
- Trunk-based; master is not deployed continuously; a branch per release (per sprint); hotfixes are cherry-picked from master into the release branch; "we always make production changes this way, starting in master" so production never regresses.
- A Microsoft Learn page (learn.microsoft.com/.../how-microsoft-develops-devops) in a search snippet says release branches never merge back to main: snippet only, UNVERIFIED by extract.

### S10. GitHub Docs, "About stacked pull requests"
URL: https://docs.github.com/en/pull-requests/get-started/about-stacked-prs . Undated; the page links carry a "public-preview-2026" campaign tag. Read 2026-11-23. CONFIRMED.
- Bottom PR targets the stack trunk: usually the default branch "though it can be any branch, such as a release branch"; each later PR targets the branch below.
- Explicit "fit for high-volume development ... often with AI agents": one PR per agent task.
- Merge bottom-up; merge-queue aware; same-repository only (no cross-fork); not in GitHub Desktop; merge requirements come from the bottom PR's base branch; CI "triggered by pull requests on your default branch run for all pull requests in the stack". Whether that CI statement holds when the stack trunk is a non-default branch such as `integration`: UNVERIFIED.
- Availability for a private fork on this plan: UNVERIFIED (a third-party page said "GA"; GitHub's own page URL campaign says preview).

### S11. GitHub Docs, "Events that trigger workflows" (pull_request, merge_group)
URL: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows . Undated. Read 2026-11-23. CONFIRMED.
- `pull_request` with a `branches` filter runs only for PRs whose BASE branch matches the pattern, e.g. a base starting with `releases/` (the doc's own example); patterns are allowed. So CI for PRs into per-release branches needs a one-line base-branch pattern in the workflow, nothing else.

### S12. GitHub Docs, "Managing the automatic deletion of branches"
URL: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches . Read 2026-11-23. CONFIRMED: repo admins can enable "Automatically delete head branches" after merge. Whether it is on for this repository: UNVERIFIED.

### S13. Claude Code Docs, "Run parallel sessions with worktrees"
URL: https://code.claude.com/docs/en/worktrees . Read 2026-11-23, extract returned fragments only. PARTIAL.
- New worktrees branch from the repository default branch; setting `worktree.baseRef` accepts "fresh" (default: remote default branch) or a value that branches from current work. Subagent worktrees use the same base; a subagent worktree with no changes is removed automatically, one with changes stays until a periodic sweep.
- Search snippets (not in the extract): `claude --worktree <name>`, `.claude/worktrees/`. Not relied on.

### S14. Cursor Docs, "Worktrees"
URL: https://cursor.com/docs/configuration/worktrees . Undated. Read 2026-11-23. CONFIRMED.
- `/worktree`, `/best-of-n` (same task on several models, each in its own worktree), `/apply-worktree`, `/delete-worktree`; default cap 25 worktrees per machine, auto cleanup (`cursor.worktreeMaxCount`, `cursor.worktreeCleanupIntervalHours`). `/best-of-n` compares runs only and does not merge for you.

### S15. OpenAI Codex docs, "Worktrees"
URL: https://developers.openai.com/codex/environments/git-worktrees . Undated. Read 2026-11-23. CONFIRMED.
- Codex-managed worktrees default to detached HEAD so several can exist without polluting branches; you pick the starting branch (main, a feature branch, or current); a branch created in a worktree (UI default prefix `codex/`) cannot be checked out in any other worktree; the one-branch-per-worktree rule is stated as a protection against races on a branch reference; handoff between Local and Worktree; automatic cleanup setting.

### S16. GitHub Changelog, 2025-07-23, "Agents page: Set the base branch for Copilot coding agent tasks"
URL: https://github.blog/changelog/2025-07-23-agents-page-set-the-base-branch-for-github-copilot-coding-agent-tasks . Read 2026-11-23. CONFIRMED.
- Copilot coding agent creates a new branch from the chosen base and opens a PR targeting that base, useful "if you're using a branching model where work doesn't always start from the default branch". The `copilot/` branch prefix appeared only in a GitHub blog search snippet (not extracted): UNVERIFIED.

### S17. Devin Docs, release notes (entry dated March 19, 2026)
URL: https://docs.devin.ai/release-notes/overview . Read 2026-11-23. CONFIRMED.
- "Devin Manages Devins": a main session coordinates managed Devins, each on its own VM; coordinator role: "scoping the work, monitoring progress, resolving conflicts, and compiling the results". Separate entry: automatic notification when a PR created in a Devin session has merge conflicts. (Vendor docs; no branch layout is described.)

### S18. Anthropic Engineering, "Building a C compiler with parallel Claudes"
URL: https://www.anthropic.com/engineering/building-c-compiler . Date not shown in the extract (UNVERIFIED date). Read 2026-11-23, passages for my query. CONFIRMED for:
- Agents each work in their own container clone and push to a shared upstream; a task is claimed by writing a lock file in `current_tasks/` and git's synchronisation makes a second claimant pick another task.
- Each agent pulls, merges other agents' changes, pushes, removes the lock; "Merge conflicts are frequent, but Claude is smart enough to figure that out." No orchestration agent used. (A research prototype, not a release process; agents commit straight to one shared trunk.)

### S19. Faros AI, "How AI-Generated Code Is Increasing Code Review Burden" (vendor telemetry)
URL: https://www.faros.ai/blog/ai-code-quality-senior-engineer-review-burden . Undated; cites "AI Engineering Report 2026". Read 2026-11-23. CONFIRMED as vendor-reported numbers (not independently audited):
- Under high AI adoption: median time to first PR review +156.6%, average time in PR review +199.6%, median time in PR review +441.5%; average PR size +51.3%, files per PR +59.7%, bugs per PR +54%.
- "31% more PRs merged with no review at all" and "25% of PRs reviewed by AI agents" appeared in a search snippet: UNVERIFIED (not seen in the extract).
- Earlier Faros 2025 figures (+98% PRs merged, review time +91%) were seen only in search snippets of other pages: UNVERIFIED here.

### S20. Unleash Docs, "Trunk-based development with feature flags" (vendor docs)
URL: https://docs.getunleash.io/guides/trunk-based-development . Undated. Read 2026-11-23 (fragments). CONFIRMED:
- Merge small slices at least daily, each leaves trunk green and releasable, incomplete feature unreachable behind a flag.
- Release branches, if needed, are short-lived, cut just in time and never merged back into; flags reduce how often one is needed.
- Retire flags when the rollout is done; create the removal task when the flag reaches 100%.

### S21. Practitioner guides on worktrees and parallel agents (secondary, not authoritative)
URLs read with tavily_extract 2026-11-23, fragments: https://blog.openreplay.com/git-worktrees-ai-agents ; https://nimbalyst.com/blog/git-worktrees-for-ai-coding-agents-complete-guide ; https://zylos.ai/research/2026-02-22-git-worktree-parallel-ai-development . CONFIRMED that each says:
- Integrate serially: merge one branch, update the next from the new main, then merge it. Tasks touching the same files or consuming each other's output are sequenced, not parallelised (openreplay).
- Worktrees do not prevent semantic conflicts; the fix is task decomposition with a written file or module ownership boundary per session; keep dependency (lockfile) changes to one session at a time; the number worth tracking is how many diffs you can read in an hour, not how many agents you can start (nimbalyst).
- A pre-merge trial merge with `git merge-tree` between branch pairs detects conflicts without touching the repository (zylos); "rebase before PR" is called the most widely recommended convention there (zylos: assertion without cited evidence, UNVERIFIED as a statement about the industry).
- A branch can be checked out in only one worktree (openreplay; same rule in S15).

### S22. Mozilla, "Firefox Development Process" (draft) and Chrome for Developers, "two-week release cycle"
URLs: https://mozilla.github.io/process-releases/draft/development_overview (undated draft) ; https://developer.chrome.com/blog/chrome-two-week-release (published 2026-03-03). Read 2026-11-23. CONFIRMED.
- Mozilla: schedule-driven; releases happen at regular intervals whether or not a given feature is ready, and are not delayed to wait for a feature; larger projects are developed in other repositories that track the main one.
- Chrome: from September 2026 a new beta and stable every two weeks (was four); "smaller scope minimizes disruption and simplifies post-release debugging"; branch, beta promotion, stable cut and release are fixed weekdays in a table. (Chromium rule "features not code complete move to the next milestone" is from a third-party snippet only: UNVERIFIED.)

### S23. GitHub merge queue, practitioner and GitHub blog snippets (not extracted)
Search snippets only, not relied on beyond S4: GitHub blog GA announcement says merge queue is "designed for high-performance teams where multiple users regularly commit to a single branch".

## Not found / gaps
- No primary source found that prescribes one branch layout for "AI-agent-driven" teams. Vendor docs (S13 to S17) describe worktree and branch mechanics only; none recommends a release-branch or trunk model. Layout advice for agents comes from practitioner posts (S21) and from the generic trunk-based literature (S1, S2, S6, S8, S9, S20).
- No primary source on how the Augment or Codex automatic reviewers behave on very large or on non-default-base PRs: UNVERIFIED. Treat as a risk for any proposal with a large release PR.
- Not verified here: whether this repository's GitHub plan allows merge queues or native stacked PRs; whether "Automatically delete head branches" is on; whether `/sc:pr-submit` accepts `--head integration`; how Orca applies the `ironbelly/` prefix when `--branch` is given. All four are questions for a local check, not for the web.
- The tag-versus-branch namespace claim (a tag named `dash1.3` next to a branch `dash1.3/release`) was not tested; only the branch-versus-branch conflict was verified, by the coordinator (CONTEXT.md line 8).
