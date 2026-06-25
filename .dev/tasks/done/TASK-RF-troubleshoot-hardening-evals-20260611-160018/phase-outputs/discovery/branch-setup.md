# Branch / Worktree Setup Record

## Resolved state (verified via `git worktree list --porcelain`)

- **Worktree absolute path:** `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
- **Branch name:** `feat/troubleshoot-hardening-evals` (exact)
- **HEAD at creation:** `8cefefde` (= `origin/master` tip — created off `origin/master`, NOT off the impl branch)
- **Status:** Worktree already existed and is correctly attached; reused as-is (no re-create needed).

## Isolation confirmation

- **Impl worktree (SEPARATE):** `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` on branch `feat/troubleshoot-pipeline-hardening`. Confirmed distinct path + distinct branch — no overlap with this evals worktree.
- **Live working-tree HEAD NOT mutated:** the primary worktree `/config/workspace/IronClaude` remains on `fix/prd-advisory-gate`; this build operates only inside the evals worktree.

## PR target (MANDATORY)

PR target MUST be the fork `IronbellyOrg/IronClaude`, NEVER upstream:

```
gh pr create --repo IronbellyOrg/IronClaude --base master --head feat/troubleshoot-hardening-evals --title "..." --body "..."
```

- `origin` = `https://github.com/IronbellyOrg/IronClaude.git` (verified via `git remote -v`).
- Never run a bare `gh pr create` (defaults to upstream parent).
