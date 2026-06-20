# Git Remote and Branch Confirmation — Step 1.3

**Captured:** 2026-05-31 04:35 (worktree: `/config/workspace/IronClaude/.claude/worktrees/BareReview/`)

## Remote Configuration

```
origin	https://github.com/IronbellyOrg/IronClaude.git (fetch)
origin	https://github.com/IronbellyOrg/IronClaude.git (push)
```

**Verdict:** PASS — `origin` resolves to `IronbellyOrg/IronClaude.git` (the user's fork), NOT `SuperClaude-Org/SuperClaude_Framework.git` (the upstream parent). Per CLAUDE.md ABSOLUTE RULE: "PR Target = Fork (`IronbellyOrg/IronClaude`), NEVER Upstream". This remote configuration is correct.

## Branch

**Current branch:** `brainstorm/t2-bare-reviewer-adjunct`

**Verdict:** PASS for the "NOT master/main" criterion — this is a feature-scoped branch.

## Advisory Finding (non-blocking)

The current branch (`brainstorm/t2-bare-reviewer-adjunct`) is named for the T2 Bare-Reviewer Adjunct work-stream (per recent commits `8a1bbc72 feat(skills): add sc-bare-review v1.0 — Phase 1 T2 Bare-Reviewer Adjunct` and `c7c140ad feat(brainstorm): T2 bare-reviewer adjunct ...`). The task being executed here is the **roadmap pipeline brittleness-elimination R0+R1 rewrite** — a fundamentally different work-stream.

Before any source-code commit lands in this branch (Phase 2+), the user should likely:

1. Stash or commit any pending T2 bare-reviewer work
2. Create a new branch off `master`/`integration` for this task: e.g. `git checkout -b refactor/roadmap-pipeline-r0-r1-rewrite origin/master`
3. Continue execution on that new branch

The task itself does not require a branch change as Step 1.3 — it only asserts "NOT master/main". So this is logged as advisory and is non-blocking. The user should make this decision before Phase 2 (R0.1 spec-ID registry) writes source files.

## Pre-PR Discipline Reminder (CLAUDE.md ABSOLUTE RULE)

When any PR is opened during this task, the command shape MUST be:

```
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."
```

Never `gh pr create` bare — that defaults to upstream `SuperClaude-Org/SuperClaude_Framework`.
