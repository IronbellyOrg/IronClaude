# Bug A Commit Record — Step 2.2

**Timestamp:** 2026-06-04 05:16
**Commit SHA:** `b9d533ff230d79afb689dde231fb73f45f32217d`
**Branch:** `fix/ci-canonical-brainstorm-hermetic`
**Message:** `fix(ci): track canonical evidence-pack fixtures for CanonicalFixtureParity tests`

## Guards (all PASS)

- `.claude/` staging guard (`git status --porcelain | grep '^[AM] .claude/'`): **EMPTY** — no `.claude/` path staged.
- Exact-path guard (`git diff --cached --name-only`): **exactly 7 paths** (6 fixtures + `.gitignore`), nothing else.
- `git add -f`: **NOT used** — fixtures were already un-ignored by the Step 2.1 negation, so a plain `git add` sufficed.

## Committed files (7) — from `git show --stat`

| file | insertions |
|------|-----------|
| .dev/releases/complete/task-builder-merge/artifacts/D-0056/fixture-F-5-5-5-halt-cycle-2.log | 21 |
| .dev/releases/complete/task-builder-merge/artifacts/D-0057/fixture-pass1-fail2-non-shrinking.log | 25 |
| .dev/releases/complete/task-builder-merge/artifacts/D-0057/fixture-pass1-fail2-shrinking.log | 22 |
| .dev/releases/complete/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-non-shrink.log | 34 |
| .dev/releases/complete/task-builder-merge/artifacts/D-0059/fixture-cross-cycle-dedup-shrinking.log | 45 |
| .dev/releases/complete/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log | 60 |
| .gitignore | 3 |

**Total:** 7 files changed, 210 insertions(+).

## Notes

- The 6 non-target `fixture-*.log` files (D-0030/2cycle, D-0031/enum, D-0032/missing-verdict, D-0056/F-0-skip, D-0056/regression-precedes-monotonicity, D-0057/no-regression-loop-continues) were NOT staged and remain untracked on disk — the accepted known side effect of the broad negation pattern. They are correctly excluded from this commit.
- Commit went through the project pre-commit hooks (incl. verify-sync) without error, consistent with no `.claude/` mutation.
