# Phase 6 — `sprint rerun-tasks --help` Summary (Step 6.3, L3)

**Date:** 2026-06-02 · **Raw:** `phase6-help.txt`
**Command:** `cd <worktree> && uv run superclaude sprint rerun-tasks --help`

| Field | Value |
|-------|-------|
| Overall result | **REGISTERED** |
| Exit code | 0 |
| Flags present | 12 / 12 (+ `INDEX_PATH` argument) |

## Flag presence checklist (grep against captured `--help`)

| Flag | Present |
|------|---------|
| `--phase` | ✅ |
| `--tasks` | ✅ |
| `--from-reflect-report` | ✅ |
| `--merge-back` / `--no-merge-back` | ✅ (pair) |
| `--dry-run` | ✅ |
| `--include-transitive` | ✅ |
| `--ignore-deps` | ✅ |
| `--force-merge` | ✅ |
| `--allow-loop` | ✅ |
| `--no-verify-checkpoints` | ✅ |
| `--bundle-dir` | ✅ |
| `--restore` | ✅ |

**Assessment:** PASS — the `rerun-tasks` subcommand is registered under the `sprint` group and exposes all 12 documented flags (TDD line 184), exceeding the BUILD_REQUEST 9-flag minimum. `--help` exits 0.
