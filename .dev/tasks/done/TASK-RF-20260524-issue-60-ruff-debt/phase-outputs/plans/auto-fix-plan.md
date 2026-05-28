# Auto-Fix Plan — Phase 3 (I001, F401, F541)

**Generated:** 2026-05-25 03:32
**Post-`.dev/`-exclusion counts:**

| Rule | Original Count | Post-Exclusion Count |
|------|---------------|---------------------|
| I001 | 93 | **51** |
| F401 | 49 | **10** |
| F541 | 29 | **0** (all in `.dev/`) |
| **Total** | **171** | **61** |

The `.dev/` exclusion already eliminated all F541 violations and reduced I001/F401 substantially.

## Unique Files Affected (52 total)

Primarily concentrated in:
- `tests/cli/eval/` — ~50 test files
- `src/superclaude/cli/eval/` — a few helpers
- `scripts/` — 3 files (eval_1.py, eval_runner.py, sync_from_framework.py)

## Auto-Fix Command

```bash
uv run ruff check . --fix --select I001,F401,F541
```

## Risk Notes per Rule

| Rule | Risk Level | Notes |
|------|-----------|-------|
| I001 | LOW | Pure import ordering; no semantic change |
| F401 | MEDIUM | Removes unused imports; verify no side-effecting imports (warnings/logging registration) |
| F541 | NONE | No errors to fix; nothing changes |

## Rollback

Per-file: `git checkout HEAD -- <file>`
Whole-phase: `git reset --hard HEAD` (only safe before commit)
