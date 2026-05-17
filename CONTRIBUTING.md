# Contributing to SuperClaude Framework

This document captures lightweight contributor conventions for the IronClaude fork. It is intentionally short — the goal is to make it easy to do the right thing by default, not to encode every possible rule.

## CI Hygiene

### The rot-budget rule

**No PR may introduce a *new* lint or test failure.** Pre-existing failures on `master` are allowed to remain — they will be addressed in dedicated rot-cleanup PRs — but a PR that *adds* a failure must fix it before it merges.

This rule keeps two things separate:

- **New regressions** — strictly disallowed; the PR author owns the fix.
- **Inherited rot** — acceptable in any individual PR; tracked separately and cleaned up in focused PRs.

### What counts as a "new failure"

A "new failure" is any lint or test failure that is **NOT present in the most recent CI run on `master`** at the time the PR branch was created.

To check whether a failure in your PR is new or inherited:

1. Look at the latest CI run on `master` (the merge commit your branch was cut from).
2. If the same test ID or lint rule + file:line is failing on `master`, it is **inherited** (acceptable for your PR).
3. If the failure appears on your branch but NOT on the `master` baseline, it is **new** (must be fixed before merge).

When in doubt, run the same check locally on master (`git stash && git checkout master && <run check>`) and compare.

### Pre-PR local checks

Before opening a PR, run these three commands from the repo root:

```bash
uv run ruff check src/ tests/
uv run pytest tests/<changed-area>/ -v
make verify-sync
```

What each one checks:

- `uv run ruff check src/ tests/` — Ruff lint over the whole source + tests tree. Catches new F-class, E-class, I-class, N-class, and W-class violations introduced by your branch.
- `uv run pytest tests/<changed-area>/ -v` — Pytest for the specific subtree your PR modifies (e.g. `tests/audit/` if you touched audit code). Faster than the full suite; catches functional regressions in the area you changed.
- `make verify-sync` — Drift check between `src/superclaude/` (source of truth for skills/agents/commands) and `.claude/` (the synced dev copies). If you edit `src/superclaude/skills/`, `src/superclaude/agents/`, or `src/superclaude/commands/`, run `make sync-dev` before this check.

### Disclaimer: social convention, not a CI-enforced gate

This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate. CI will still pass PRs that violate the rot-budget if the underlying job is green (or if the underlying job has been failing on master and continues to fail at the same level). Enforcement relies on PR reviewers checking the rule during code review.

If you find a PR that violates the rule (a new failure that wasn't present on master), call it out in the review and ask the author to either fix the regression or document why it's acceptable.
