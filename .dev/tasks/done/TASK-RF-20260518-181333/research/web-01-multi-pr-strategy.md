# Web Research — Multi-PR Strategy for feat/hook-sync-and-matcher-fix

**Researcher:** R7 of 7 (External / Web)
**Date:** 2026-05-18
**Scope:** External best practices for splitting a long-lived feature branch into multiple sequential PRs.
**Status:** Complete

## Context Recap (from CLAUDE.md + sibling researcher topic outlines)

- Branch: `feat/hook-sync-and-matcher-fix`, 15 commits ahead of `master`.
- Logical units: sprint runner fixes, task-builder release artifacts, hooks/matcher fix, tests.
- Code volume: ~600 LOC sprint code + ~511 LOC tests + thousands of LOC in `.dev/releases/` evidence artifacts.
- Repo policy (CLAUDE.md): `master ← integration ← feature/*` (git-flow-lite); R3 may confirm whether `integration` actually exists.
- Convention: feature branches only, never commit directly to master.

> **Authority order:** Codebase (R1-R6 findings, CONTRIBUTING.md, PULL_REQUEST_TEMPLATE.md) > Official GitHub/Atlassian/GitLab docs > FAANG/established engineering blogs > random blogs. External research below SUPPLEMENTS but never OVERRIDES verified internal findings.

---

## Area 1 — Stacked / Sequential PR Workflow

### Sources

1. [GitHub Stacked PRs — Typical Workflows (official)](https://github.github.com/gh-stack/guides/workflows/) — **HIGH**
2. [GitHub Stacked PRs — Overview (official)](https://github.github.com/gh-stack/introduction/overview/) — **HIGH**
3. [github/gh-stack repository (official CLI extension)](https://github.com/github/gh-stack) — **HIGH**
4. [Trunk Docs — Work with stacked pull requests](https://docs.trunk.io/merge-queue/using-the-queue/stacked-pull-requests) — **MEDIUM**
5. [Tower Blog — Understanding the Stacked Pull Requests Workflow](https://www.git-tower.com/blog/stacked-prs) — **MEDIUM**
6. [Awesome Code Reviews — Stacked Pull Requests Complete Guide](https://www.awesomecodereviews.com/best-practices/stacked-prs/) — **MEDIUM**

### Key Information

- A "stack" is an ordered series of branches; PR-1 targets `master`, PR-2 targets PR-1's branch, PR-3 targets PR-2's branch, etc. Each PR is small and independently reviewable.
- Foundational changes go at the BOTTOM of the stack; dependent/feature-layer changes go ON TOP.
- After review feedback on PR-N, rebase PR-(N+1) onto the updated PR-N branch.
- Tooling: `gh stack`, `ghstack`, Graphite, `spr`, Aviator `av`, Tower, Trunk Merge Queue — all manage the rebase chain so humans don't have to.
- Manual approach (no tooling): create branch B1 from master, branch B2 from B1, etc. Use `git rebase --onto` when the base moves.

### Relevance to Our Codebase — HIGH

Our branch has 4 logical units (sprint fixes, hooks, task-builder release, tests). A 3–4 PR stack maps naturally. Since R3/R4 will likely confirm the repo uses a git-flow-lite model (no `gh stack` adoption visible), recommend the **manual sequential PR approach** rather than introducing new tooling.

---

## Area 2 — Splitting Long-Lived Branches Into Multiple PRs

### Sources

1. [Stack Overflow — Github: split PR into two PRs by files](https://stackoverflow.com/questions/46574355/github-split-pr-into-two-prs-by-files) — **HIGH**
2. [Stack Overflow — Git: split pull request into smaller PRs](https://stackoverflow.com/a/30773902) — **HIGH**
3. [Branchlet — branch splitting tool](https://www.branchlet.dev/) — **LOW** (tool, not adopted in repo)
4. [Aviator `av` CLI](https://github.com/aviator-co/av) — **LOW** (tool)

### Key Information

Three canonical manual approaches:

| Approach | When to use | Pros | Cons |
|---|---|---|---|
| **Cherry-pick onto fresh branches from master** | Commits are clean, independent | Clean history per PR; no entanglement | Loses original commit hashes; manual conflict handling |
| **Interactive rebase + branch splitting** (`git rebase -i` reorder/edit, then `git branch` at each split point) | Commits interleave but are atomic | Preserves authorship/order | Complex; error-prone with conflicts |
| **New branch + cherry-pick subset** | Want to ship one slice fast and leave the rest on the old branch | Fastest; lowest cognitive load | Old branch carries leftover work; can drift |

For our case (15 commits, 4 logical units, well-separated by file path: `src/superclaude/cli/sprint*` vs `src/superclaude/hooks/*` vs `.dev/releases/current/task-builder-merge/*` vs `tests/*`), **cherry-pick onto fresh branches from master** is cleanest. Commits already use Conventional Commits scopes per R2 expectations, so grouping by scope is straightforward.

### Relevance to Our Codebase — HIGH

Confirms the builder should produce: a cherry-pick plan (which commits → which new branch) rather than `git rebase -i`. Lower risk for a 15-commit branch.

---

## Area 3 — Trunk-Based vs Gitflow for Our Scenario

### Sources

1. [Trunk Based Development — Short-Lived Feature Branches (official site, Paul Hammant)](https://trunkbaseddevelopment.com/short-lived-feature-branches/) — **HIGH**
2. [Atlassian — Trunk-based Development](https://www.atlassian.com/continuous-delivery/branch-deployments-in-continuous-delivery-pipelines) — **HIGH**
3. [Mergify — Trunk-Based Development vs Feature Branches](https://mergify.com/learn/trunk-based-development/vs-feature-branch/) — **MEDIUM**
4. [arXiv — Choosing the Right Git Workflow (2025)](https://arxiv.org/abs/2507.08943) — **MEDIUM**

### Key Information

- Trunk-based: branches live hours-to-days; merge to trunk frequently behind feature flags if needed.
- Gitflow / git-flow-lite: branches live days-to-weeks; explicit integration branch buffers risk before master.
- Long-lived branches (>1 week, >10 commits) are a **smell in both models** — in trunk-based they shouldn't exist; in Gitflow they should already have been merged through `integration`.

### Relevance to Our Codebase — HIGH

CLAUDE.md states `master ← integration ← feature/*` (git-flow-lite). Our 15-commit branch is overdue for integration. **External best practice and project convention agree**: split now, merge the slices through whatever integration channel exists (or directly to master if `integration` is effectively unused — R3 to confirm). Do NOT keep accumulating. The splitting work itself is consistent with both paradigms.

---

## Area 4 — PR Sizing / Review Fatigue

### Sources

1. [Engineering Manager Tools — Pull Request Size: Ideal Limits & How to Enforce Them](https://www.em-tools.io/engineering-metrics/pull-request-size) — **HIGH**
2. [Opensource.com — Anatomy of a Perfect Pull Request](https://opensource.com/article/18/6/anatomy-perfect-pull-request) — **HIGH** (cites the SmartBear/Cisco study, the most-cited empirical source)
3. [minware — Pull Request Size](https://www.minware.com/guide/metrics/pull-request-size) — **MEDIUM**
4. [Umano Guide — Pull Request Size](https://guide.umano.tech/en/articles/5178387-pull-request-size) — **MEDIUM**
5. [Compile N Run — Git Pull Request Size](https://www.compilenrun.com/docs/devops/git/git-best-practices/git-pull-request-size/) — **LOW** (aggregator)

### Key Information (consensus across sources, traced to the SmartBear/Cisco study)

| Bucket | LOC changed | Defect-detection quality |
|---|---|---|
| Small | < 200 | Excellent |
| Medium | 200–400 | Good (review session ~60–90 min) |
| Large | 400–600 | Marked drop |
| XL | > 600 | Defect detection collapses; review becomes rubber-stamp |

Additional heuristics: ≤10 files changed; one logical change per PR; review sessions capped at ~60 min.

### Relevance to Our Codebase — HIGH

Our branch totals:
- Sprint code: ~600 LOC → **borderline large; consider 2 sub-PRs if natural seam exists**.
- Tests: ~511 LOC → **large but reviewable in one PR since tests are read linearly**.
- Hooks/matcher fix: smaller, isolated to `src/superclaude/hooks/` → **small PR**.
- `.dev/releases/` artifacts: thousands of LOC but **evidence, not code** — reviewer reads structure, not every line.

**Key recommendation: separate "evidence-only" PRs from "code-changing" PRs.** Evidence PRs can be approved by structure/spot-check; code PRs need full review. Mixing the two inflates apparent PR size and hides real code review burden.

---

## Area 5 — Multi-PR / Dependent PR Description Templates

### Sources

1. [Graphite — How to track and resolve pull request dependencies in GitHub](https://graphite.com/guides/track-resolve-pr-dependencies-github) — **HIGH**
2. [Socle — Understanding stacked branches](https://www.socle.dev/why-stacking-branches) — **MEDIUM**
3. [SwiftAce — How to Stack Pull Requests](https://swiftace.org/posts/how-to-stack-pull-requests) — **MEDIUM**
4. [Playbooks — stacked-pr-management skill](https://playbooks.com/skills/constellos/claude-code/stacked-pr-management) — **MEDIUM**

### Key Information — Canonical Stacked PR Body Template

```markdown
## Summary
<1–3 sentences on what THIS PR does>

## Stack Position
- **This PR:** Part N of M — <short label>
- **Base branch:** `<previous PR branch>` (or `master` if PR-1)
- **Depends on:** #<previous PR number> (merge first)
- **Blocks:** #<next PR number(s)>

## Changes
- <bullet>
- <bullet>

## Test Plan
- [ ] <verification step>

## Related PRs (full stack)
1. #<n1> — <label> (this PR if N=1)
2. #<n2> — <label>
3. #<n3> — <label>
```

The "Stack Position" + "Related PRs" block is what GitHub UI cannot infer on its own; reviewers rely on it to know merge order.

### Relevance to Our Codebase — HIGH

Builder should encode this template verbatim, with the first PR's body listing all planned siblings even before they exist (placeholders updated as each PR opens).

---

## Area 6 — PR Title Conventions for Split Work

### Sources

1. [DEV — How to Stop Drowning in Giant PRs With Stacked PRs](https://dev.to/alanwest/how-to-stop-drowning-in-giant-pull-requests-with-stacked-prs-2o9d) — **HIGH** (cautions against arbitrary "Part 1/2")
2. [Playbooks — stacked-pr-management](https://playbooks.com/skills/constellos/claude-code/stacked-pr-management) — **MEDIUM**
3. [Socle — Stacked branches](https://www.socle.dev/why-stacking-branches) — **MEDIUM**
4. [Medium — Stacked Diffs: Keeping Phabricator Diffs Small](https://kurtisnusbaum.medium.com/stacked-diffs-keeping-phabricator-diffs-small-d9964f4dcfa6) — **LOW** (older but historically influential)

### Key Information

Three observed patterns in the wild:

| Pattern | Example | Notes |
|---|---|---|
| **Descriptive title only** (no part marker) | `fix(hooks): correct matcher path resolution` | DEV article preferred; each PR should stand on its own. **Best if PRs are independently mergeable.** |
| **Suffix `(N/M)`** | `feat(sprint): runner retry fix (1/4)` | Common; signals stack at-a-glance. **Best if PRs MUST merge in order.** |
| **Prefix `Part N:`** | `Part 1: Database schema` | Phabricator-era; less common on GitHub today. |

The DEV article's warning is important: **don't use `Part 1/Part 2` if each PR isn't independently meaningful** — that hides the real problem (the split is arbitrary).

### Relevance to Our Codebase — HIGH

Our 4 logical units ARE independently meaningful (hooks fix works without sprint fix; tests can ship after either). Recommend the **descriptive-title-only** pattern with Conventional Commits scopes — the `## Stack Position` block in the body carries the ordering information.

If R3 finds that one PR strictly depends on another (e.g., tests reference sprint code changes), use the `(N/M)` suffix for THAT pair only.

---

## Area 7 — Conventional Commits Scope for Multi-Component Commits

### Sources

1. [Conventional Commits specification](https://www.conventionalcommits.org/) — **HIGH**
2. [Commitizen — Monorepo support](https://commitizen-tools.github.io/commitizen/tutorials/monorepo_guidance/) — **HIGH**
3. [commitlint — Commit conventions](https://commitlint.js.org/concepts/commit-conventions.html) — **HIGH**
4. [monorepo-semantic-release — Making Commits](https://dbouwman.github.io/monorepo-semantic-release/pages/guides/making-commits.html) — **MEDIUM**
5. [Pragma — Versioning & Releases](https://www.mintlify.com/canonical/pragma/guides/versioning) — **MEDIUM**

### Key Information

- Spec says scope is **optional** and represents "a section of the codebase" (`fix(parser): ...`).
- For commits spanning multiple components, the common patterns are:
  1. **Comma-separated scopes:** `feat(sprint,tests): retry fix + coverage` — supported by commitlint with `scope-delimiter`, also `monorepo-semantic-release`.
  2. **Broad/parent scope:** `chore(monorepo): ...` or `chore(repo): ...` when nothing more specific applies.
  3. **Omit scope entirely** when truly cross-cutting: `chore: bump linting rules`.
  4. **Split into separate commits** — the spec-pure answer; one commit per scope.

### Relevance to Our Codebase — HIGH

R2 will determine the project's prevailing scope set from recent git history (commits like `feat(task-builder): ...`, `test(task-builder): ...` already follow single-scope-per-commit). **Recommendation: prefer SEPARATE commits over comma-scopes** in this repo, because:

1. It matches the established style visible in recent commits.
2. It enables clean cherry-pick onto fresh branches in Area 2's plan — one commit, one scope, one target PR.
3. Comma-scopes are tooling-dependent; not all parsers accept them.

When a single change truly touches both `sprint` and `tests` and cannot be split (e.g., adding a test that fails without the sprint fix), use the **primary scope** (`feat(sprint): X with coverage`) rather than comma-scopes.

---

## Area 8 — `gh pr create` Body Best Practices

### Sources

1. [GitHub CLI manual — `gh pr create` (official)](https://cli.github.com/manual/gh_pr_create) — **HIGH**
2. [cli/cli issue #6408 — `--body-file` + templates](https://github.com/cli/cli/issues/6408) — **MEDIUM**
3. [PR creation guide with Summary/Test Plan/Checklist sections](https://playbooks.com/skills/rsmdt/the-startup/git-workflow) — **MEDIUM**

### Key Information

Flags relevant to the builder:
- `--title <string>` / `-t`
- `--body <string>` / `-b` — inline body; **shell-quoting hazards for multi-line**
- `--body-file <file>` / `-F` — recommended for multi-line bodies; **use this in the builder**
- `--template <file>` / `-T` — picks a `.github/PULL_REQUEST_TEMPLATE.md` variant
- `--base <branch>` / `-B` — sets target (use this for stacked PRs targeting a sibling branch, not master)
- `--draft` / `-d` — open as draft (good for the second/third PR in a stack while parent is still in review)

Canonical body sections (consensus across templates):
1. `## Summary`
2. `## Changes`
3. `## Test Plan` (Markdown checkbox list — GitHub renders them)
4. `## Breaking Changes` (omit section if none)
5. `## Related PRs` / `## Stack Position` (this is what we add for the stack)

### Relevance to Our Codebase — HIGH

R4 covers project-specific `.github/PULL_REQUEST_TEMPLATE.md`. The builder must:
- Write each PR body to a tempfile via `cat > /tmp/pr-N-body.md <<'EOF' ... EOF` (heredoc — preserves Markdown).
- Invoke `gh pr create --title "..." --body-file /tmp/pr-N-body.md --base <base-branch>`.
- Use `--base master` for PR-1, `--base <PR-1 branch>` for PR-2 only if true dependency (else `--base master`).
- Open PR-2+ as `--draft` until PR-1 merges, then `gh pr ready <num>`.

---

## Key External Findings

1. **Stacked PRs are an established pattern** with official GitHub tooling (`gh-stack`) — but adoption is optional; manual stacking works for short stacks (≤4).
2. **Empirical PR size sweet spot is < 400 LOC changed** (SmartBear/Cisco study, re-cited everywhere); defect detection collapses above 600 LOC.
3. **Evidence/artifact files should be split from code-change files** in separate PRs — reviewer cognitive load is about code, not document count.
4. **Long-lived branches are an anti-pattern in BOTH trunk-based AND Gitflow.** 15 commits / 4 logical units exceeds normal thresholds; splitting now is the right move regardless of paradigm.
5. **Independently-meaningful PRs should use descriptive titles, not `Part 1/Part 2`** (DEV article warning). Reserve `(N/M)` suffix for hard-ordered stacks.
6. **`## Stack Position` + `## Related PRs` blocks in the body** are the standard mechanism for communicating PR dependencies — GitHub UI alone is insufficient.
7. **Cherry-pick onto fresh branches from master** is lower-risk than `git rebase -i` for splitting a 15-commit branch with file-path-aligned logical units.
8. **One Conventional Commits scope per commit** matches the repo's existing style and enables clean cherry-pick splits; reserve comma-scopes/broad scopes only when truly unsplittable.
9. **`gh pr create --body-file` (not `--body`)** is the only reliable way to ship multi-line Markdown bodies from a script.
10. **Stacked PRs after PR-1 should open as `--draft`** until their parent merges, to prevent premature review or accidental merge order violations.

---

## Recommendations from External Research

### R-EXT-1: Stack design — 3–4 PRs, descriptive titles, separate evidence

Split into approximately:
- **PR-1 (code):** `fix(hooks): <matcher path resolution>` — hooks/matcher fix only. Smallest, lowest-risk, ship first.
- **PR-2 (code):** `feat(sprint): <runner retry/correctness fix>` — sprint runner logic + targeted unit tests in the same PR (tests close to code is preferred per R6 likely findings).
- **PR-3 (tests):** `test(task-builder): <integration/regression coverage>` — broader test additions if not bundled in PR-2.
- **PR-4 (evidence):** `docs(task-builder): release artifacts for task-builder-merge` — `.dev/releases/current/task-builder-merge/**` only. Title clearly signals "no production code."

Each PR base = `master` unless R3 identifies a hard dependency. Use stacked bases ONLY where strictly required.

### R-EXT-2: Use cherry-pick, not interactive rebase

Workflow:
```bash
git checkout master && git pull
git checkout -b fix/hooks-matcher
git cherry-pick <hash1> <hash2>  # hooks commits only
# ...repeat for each PR branch
```
This preserves the original `feat/hook-sync-and-matcher-fix` branch as a safety net until all sub-PRs land.

### R-EXT-3: Body template per PR (heredoc + `--body-file`)

```bash
cat > /tmp/pr-1-body.md <<'EOF'
## Summary
<1-3 sentences>

## Stack Position
- **This PR:** 1 of 4 — Hooks matcher fix
- **Base:** `master`
- **Blocks:** #<pr2>, #<pr3>, #<pr4> (no hard dependency — independently mergeable)

## Changes
- <bullet>

## Test Plan
- [ ] `uv run pytest tests/hooks/ -v` passes
- [ ] `make verify-sync` clean

## Related PRs
1. #<this>  — Hooks matcher fix
2. #<pr2>  — Sprint runner retry fix
3. #<pr3>  — Task-builder test coverage
4. #<pr4>  — Task-builder release evidence (docs only)
EOF

gh pr create --title "fix(hooks): correct matcher path resolution" \
             --body-file /tmp/pr-1-body.md \
             --base master
```

### R-EXT-4: Title convention — Conventional Commits prefix, no `(N/M)` suffix

Independently-mergeable PRs get clean titles like `fix(hooks): ...`, `feat(sprint): ...`, `test(task-builder): ...`, `docs(task-builder): ...`. The body's `## Stack Position` carries ordering. Only add `(N/M)` suffix if R3 confirms a hard merge-order dependency.

### R-EXT-5: Size discipline — defer or further-split anything > 400 LOC of CODE

- Sprint code (~600 LOC) exceeds the soft limit. If R1/R5 identify a natural seam (e.g., retry logic vs error reporting), split PR-2 into PR-2a + PR-2b.
- The ~511 LOC test PR is acceptable in one PR (tests review faster than code).
- Evidence PR has high LOC count but low cognitive review cost — call this out explicitly in the PR body so reviewers don't bounce on size alone.

### R-EXT-6: One scope per commit; rebase to enforce before cherry-pick

If any existing commits on `feat/hook-sync-and-matcher-fix` mix scopes (e.g., one commit touches both `sprint/` and `hooks/`), the builder should flag them to the user and either:
- Recommend `git rebase -i` + `git reset HEAD~ && git add -p` to split before cherry-picking, OR
- Document the cross-cutting commit and assign it to the primary-scope PR with a body note.

### R-EXT-7: Draft mode for downstream PRs

Open PR-1 as ready; open PR-2/3/4 as `--draft` if reviewers might otherwise approve and merge them out of order. Convert via `gh pr ready <num>` after upstream merges.

### R-EXT-8: Evidence-only PR gets an explicit reviewer note

PR-4's body should open with a banner: `> **Evidence/documentation only.** No production code changes. Reviewable by structure spot-check rather than line-by-line.` This is the most actionable mitigation for the "thousands of LOC in `.dev/releases/`" problem.

---

## Summary

External best-practice research strongly converges on: **stacked / split PRs with descriptive Conventional-Commits titles, ≤400 LOC of code per PR, stack-position metadata in the body via `gh pr create --body-file`, evidence-only PRs separated from code PRs, and cherry-pick-onto-fresh-branches as the lowest-risk splitting mechanism**. All recommendations are consistent with the repo's git-flow-lite policy and existing commit-scope conventions visible in recent history; none override codebase-internal findings from R1-R6. The builder should encode R-EXT-1 through R-EXT-8 as concrete steps in the PR plan.

**File:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260518-181333/research/web-01-multi-pr-strategy.md`
**Status:** Complete
