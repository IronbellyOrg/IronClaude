---
phase: 3
gate: PG-3.1
captured: 2026-05-19
task_id: TASK-RF-track-1-20260518-231708
scope: bootstrap_scan.sh two-path lookup patch + 40-sentinel git rm purge + sync verification
---

# Phase 3 Aggregation — for rf-qa task-integrity review (PG-3.2)

This is the SINGLE artifact rf-qa will consume for PG-3 verification. All claims below are evidence-backed by the cited phase-outputs files.

---

## (a) Diff hunks applied to `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh`

### Hunk 1 — line 90 area (exit_code lookup inside `sprints_state` per-release-dir loop)

**Before (single-path, in-release-dir only):**

```bash
  for d in "$base"/*/; do
    [[ -d "$d" ]] || continue
    local name exit_code log_tail manifest_status
    name=$(basename "$d")
    exit_code=""
    [[ -f "$d/.sprint-exitcode" ]] && exit_code=$(tr -d '[:space:]' < "$d/.sprint-exitcode" 2>/dev/null || echo "")
```

**After (two-path lookup — state_dir first, in-release-dir fallback for legacy archives):**

```bash
  for d in "$base"/*/; do
    [[ -d "$d" ]] || continue
    local name exit_code log_tail manifest_status
    name=$(basename "$d")
    exit_code=""
    # Reads .sprint-exitcode from .dev/sprint-state/<release-name>/ (post-FU-001)
    # with fallback to in-release path for legacy archives.
    state_sentinel="$ABS_PROJECT/.dev/sprint-state/$name/.sprint-exitcode"
    if [[ -f "$state_sentinel" ]]; then
      exit_code=$(tr -d '[:space:]' < "$state_sentinel" 2>/dev/null || echo "")
    elif [[ -f "$d/.sprint-exitcode" ]]; then
      exit_code=$(tr -d '[:space:]' < "$d/.sprint-exitcode" 2>/dev/null || echo "")
    fi
```

**Effect:** Reader checks the canonical post-FU-001 location `.dev/sprint-state/<release-name>/.sprint-exitcode` first; only falls back to the legacy in-release-dir path when the state_dir sentinel is absent. Preserves backwards compatibility with pre-FU-001 archive sentinels while the writer (executor.py:1751-1758) now emits exclusively to state_dir.

### Hunk 2 — line ~126 area (`recent_files` collector)

**Before:**

```bash
EXIT_CODES=$(recent_files ".sprint-exitcode" | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')
```

**After (functional behavior unchanged — `find -name` matches both old and new paths; comment added):**

```bash
# recent_files uses find -name so new state_dir paths (.dev/sprint-state/**/.sprint-exitcode) are picked up automatically post-FU-001
EXIT_CODES=$(recent_files ".sprint-exitcode" | awk 'BEGIN{printf "["} {printf "%s\"%s\"", sep, $0; sep=","} END{printf "]"}')
```

**Effect:** No code change required — the existing `recent_files ".sprint-exitcode"` calls `find ... -name ".sprint-exitcode"`, which already walks the entire project tree (`.dev/sprint-state/<release-name>/.sprint-exitcode` matches by basename). A clarifying comment documents post-FU-001 behavior so future maintainers don't re-add a path filter.

---

## (b) `.claude/` and `src/superclaude/` byte-identical sync

- **Source:** `phase-outputs/test-results/phase3-verify-sync.txt`
- **Final status line:** `✅ All components in sync.`
- **All 20 skills present and OK**, including `sc-crash-recovery` (which contains the patched `bootstrap_scan.sh`).
- **Cross-check:** `diff -u src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh .claude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` returned exit code 0 (no diff) at PG-3.1 aggregation time.

---

## (c) Files removed via `git rm`

- **Source:** `phase-outputs/test-results/phase3-git-rm.txt`
- **Line count:** **40** (matches Phase 1 Step 1.5 baseline; no drift).
- **Removal scope:** all `git ls-files`–tracked `.sprint-exitcode` entries under `.dev/releases/{archive,complete,current}/`, including nested per-tasklist subdirectories (e.g. `unified-audit-gating-v1.2.1/tasklist/`, `unified-audit-gating-v1.2.1/test-evidence/live-sprint/`, `v2.13-CLIRunner-PipelineUnification/smoke-test-sprint/`, etc.).
- **Pre-rm redundancy check:** `phase-outputs/discovery/redundancy-check.txt` is empty, confirming every removed sentinel directory retains a paired `execution-log.jsonl` (and typically `manifest.json`) — exit-code information for these historical sprints is preserved in the execution log even after the sentinel removal.

---

## (d) Post-rm `git ls-files | grep -c '\.sprint-exitcode$'` count

- **Source:** `phase-outputs/test-results/phase3-postrm-count.txt`
- **Value:** **`0`**
- **Re-verified at PG-3.1 aggregation time:** `git ls-files | grep -c '\.sprint-exitcode$'` → `0` (independent re-run). Acceptance criterion AC3 met.

---

## (e) Stray untracked entries (Step 3.4 verification)

- **Source:** `phase-outputs/test-results/phase3-git-status-stray.txt`
- **Line count:** 40 — **all** entries begin with `D ` (staged deletes from Step 3.3).
- **NO `??` (untracked) entries** for any `.sprint-exitcode` path.
- **NO `M ` (modified) entries** for any `.sprint-exitcode` path.
- **Conclusion:** The existing `.gitignore` `/.sprint-exitcode` line (added in TASK-RF-20260518-181333 Phase 3 at `.gitignore:222`) continues to suppress the repo-root sentinel case, and the Phase 2 writer migration to `.dev/sprint-state/` prevents new in-release-dir sentinels from materializing. Research §3's "Untracked sibling" observation is no longer reproducible against the post-Phase-2/Phase-3 tree.

---

## Acceptance criteria mapping for PG-3.2

| AC | Statement | Evidence | Status |
|---|---|---|---|
| AC1 | bootstrap_scan.sh lines 90 + 126 patched: state_dir-first read, fallback to in-release-dir for legacy | Section (a) above — both hunks verified inline in current source | PASS |
| AC2 | `.claude/` and `src/superclaude/` byte-identical per `make verify-sync` | Section (b) — phase3-verify-sync.txt ends with "✅ All components in sync." + diff exit 0 | PASS |
| AC3 | `git ls-files \| grep -c '\.sprint-exitcode$'` returns 0 | Section (d) — phase3-postrm-count.txt = 0, re-verified | PASS |
| AC4 | No stray untracked / modified `.sprint-exitcode` entries in `git status` beyond Step 3.3 D-lines | Section (e) — phase3-git-status-stray.txt has 40/40 D-lines, zero `??`/`M ` | PASS |

All four acceptance criteria are PASS based on the evidence captured in `phase-outputs/`.
