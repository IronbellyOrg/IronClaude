# Remote Verification Report — Step 1.2

**Date:** 2026-06-05
**Command run from:** `/config/workspace/IronClaude`

## `git remote -v` output

```
origin	https://github.com/IronbellyOrg/IronClaude.git (fetch)
origin	https://github.com/IronbellyOrg/IronClaude.git (push)
```

## Assessment: PASS

| Check | Result |
|-------|--------|
| `origin` points to `IronbellyOrg/IronClaude.git` | ✅ PASS (fetch + push both correct) |
| `upstream` remote present | None configured locally. Per CLAUDE.md, `upstream` = `SuperClaude-Org/SuperClaude_Framework` is the public parent and is **FORBIDDEN** for push/PR creation unless explicitly authorized in-session. No `upstream` remote exists in this checkout, eliminating the accidental-push vector. |
| `.claude/` staging rule | `.claude/{skills,commands,agents,hooks,templates}/*` must **NEVER** be staged. Only `.claude/settings.json` is permitted. `git add -f` on any `.claude/` path is the violation siren — STOP. |
| Primary checkout state | The primary checkout at `/config/workspace/IronClaude` is **dirty** (branch `feature/prd-spec-flag`, ~20 modified / ~46 untracked). It MUST NOT be stashed, reset, or branch-switched. All work for this task occurs in an isolated worktree off `origin/master` (created in Step 1.3). |

## Fork PR discipline (carried forward to Phase 6)

Mandatory PR command shape:
```
gh pr create --repo IronbellyOrg/IronClaude --base master --head fix/sprint-rerun-pass-recovered ...
```
Never a bare `gh pr create` (defaults to the public upstream parent). Verify the returned URL begins with `https://github.com/IronbellyOrg/IronClaude/pull/`.
