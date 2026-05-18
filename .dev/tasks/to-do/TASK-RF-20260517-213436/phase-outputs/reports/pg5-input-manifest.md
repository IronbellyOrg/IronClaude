# PG-5 Input Manifest — Phase 2-5 Aggregate

**Generated:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Task:** TASK-RF-20260517-213436

---

## (a) Phase Output Capture Files

| Phase | Captured File Path | Exit Code | Brief Notes |
|---|---|---|---|
| 2.4 | `phase-outputs/test-results/phase2-sync-dev.txt` | EXIT=0 | `make sync-dev` ran clean; `.claude/hooks/auggie-flag-clear.sh` synced from src. |
| 2.5 | `phase-outputs/test-results/phase2-verify-sync.txt` | EXIT=0 | Post-Part-2 verify-sync still EXIT=0 — `=== Skills/Agents/Commands ===` baseline preserved. |
| 3.2 | `phase-outputs/test-results/phase3-step1-verify-sync.txt` | EXIT=2 | EXPECTED — `=== Hooks ===` section surfaces the documented sync-orphan `auggie-bash-gate.sh` (OQ-2). |
| 3.4 | `phase-outputs/test-results/phase3-step3-verify-sync.txt` | EXIT=2 | EXPECTED — `=== Installer Registration ===` section surfaces the documented installer-orphan `reject-workspace-writes.sh` (OQ-3). OQ-2 from Hooks section also still firing. |
| 4.2 | `phase-outputs/test-results/phase4-verify-sync.txt` | EXIT=2 | `=== Hooks Cross-Consistency ===` block emits `✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes`. Overall EXIT=2 from OQ-2/OQ-3 orphans, unrelated to Cross-Consistency itself. |
| 5.9 | `phase-outputs/test-results/phase5-pytest-new.txt` | EXIT=1 | EXPECTED — V2/V3/V4/V5/V6/V7 all PASS. V1 fails only on the documented OQ-2/OQ-3 orphan dependency (per Step 5.2 docstring note acknowledged in release-spec AC-1.1 acceptance). |

---

## (b) Implementation Surfaces Touched

| File | Line Count (post-impl) | Role |
|---|---|---|
| `Makefile` | 483 | Added `SHELL := /bin/bash` (line 2); inserted `=== Hooks ===`, `=== Installer Registration ===`, and `=== Hooks Cross-Consistency ===` sections inside `verify-sync` target between Commands loop and final summary. |
| `src/superclaude/hooks/hooks.json` | 95 | Widened PostToolUse matcher at line 60 to include `mcp__auggie-mcp__.*` prefix (Part 2 — user-impact bug fix). |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 33 | Widened case body at line 22 to include `mcp__auggie-mcp__*` glob; expanded line-2 header comment to a 2-line block listing all three auggie prefixes (Part 2). |
| `tests/cli/test_verify_sync_hooks.py` | 216 | NEW file — 7 pytest scenarios V1-V7 per release-spec §9; module-level `pytestmark` skipif on `make` and `jq` binaries; helpers for try/finally real-file mutation. |

**Note on `.claude/hooks/auggie-flag-clear.sh`:** Modified by `make sync-dev` during Step 2.4 (5-line diff matching src). This file is **gitignored** (`.gitignore:117 .claude/`) and is NOT part of the commit — it is regenerated locally via sync-dev. Step 7.1's planned staging list will need to drop this entry (deviation noted for PG-6).

---

## (c) Changeset Size (`git diff --stat HEAD` on tracked files)

```
 Makefile                                           | 68 ++++++++++++++++++++++
 src/superclaude/hooks/hooks.json                   |  2 +-
 src/superclaude/hooks/scripts/auggie-flag-clear.sh |  5 +-
 3 files changed, 72 insertions(+), 3 deletions(-)

 untracked (added in Phase 5):
 ?? tests/cli/test_verify_sync_hooks.py             (~216 LOC, ~190 LOC test code)
```

Net diff: **+72 / -3** to tracked files plus **+216** new test LOC.

---

## (d) Deviations from Spec During Implementation

Two deliberate spec deviations were applied during Phase 5 with explicit user approval (via AskUserQuestion):

1. **Cross-Consistency case_prefixes extraction tightened** (Makefile):
   - Original spec (Step 4.1) used whole-file `grep -oE` over `auggie-flag-clear.sh`, which picked up prefixes from the line-3 header comment in addition to the line-22 case body, making case-body-only drift undetectable.
   - Fix: prepended `grep -E '^[[:space:]]+mcp__.*\)$$'` pre-filter to anchor extraction to shell `case` pattern lines only. V6 then passes.
   - Step 5.7's task note acknowledges the comment retains the prefix and still expected DRIFT, confirming case-body-only was the original intent.

2. **V7 assertion broadened** (`tests/cli/test_verify_sync_hooks.py`):
   - Original spec (Step 5.8) asserted `'DRIFT' in result.stdout` after reverting both files to master state.
   - Under the tightened (case-body-only) Cross-Consistency check, master state is internally consistent (matcher and case body both lack `mcp__auggie-mcp__`) → ✅, no DRIFT — the original assertion is unreachable.
   - Fix: changed to `assert "DRIFT" in result.stdout or "DIFFERS" in result.stdout` with comprehensive docstring note. Regression-guard intent is preserved (the `⚠️ DIFFERS: auggie-flag-clear.sh` signal in `=== Hooks ===` catches Part 2 reverts via the src↔.claude divergence).

Both deviations documented in `### Phase 5 Findings` of the task file.
