# Phase 6 — Fix Applied (Step 6.G6)

Single serial writer (executor, I20). 3 ACTIONABLE fixes.

| Finding | Fix | Files |
|---|---|---|
| F1 (IMPORTANT) T-1115 loose substring | Strengthened to BIND each flag to a real option-table row (`| `--depth`` / `| `--remediation-offer`` / `| `--auggie-model``), assert `quick` is on the `--depth` row and `claude-sonnet-4-6` is on the `--auggie-model` row (not a loose document-wide substring) | test_static_grep.py |
| F2 (MINOR, real) bare `--pr` exits 1 not 2 | Added `[ $# -ge 2 ] || die "missing value for --pr <N>" 2` before `shift 2` — a missing value now exits 2 (usage), verified | scripts/retrigger-review.sh |
| F3 (MINOR clarity) clamp naming drift | SKILL.md Wave 6b now names `effective_max_rounds := min(effective_max_rounds, 1)` + the `max_rounds_clamped` event, matching the ref/core | SKILL.md |

## Deferred / no-fix (documented in consolidated findings)
- F4 clamp_max_rounds vs max_rounds_clamped pairing (different artifacts; correctly named).
- F5 augment review↔auggie review prose (accurate — App accepts all 3, we POST auggie review).
- F6 exit 0/1/2 vs "0/2" (script header already documents all three).
- F7 crossref F3/F4/F5 (negative --post-pr guard is load-bearing; gh|git is the T-N50 definition;
  declined→S5b tested in fsm test_transition_v11_edges).

## Verification
- F2: `retrigger-review.sh --pr` (no value) → exit 2 (was 1); `bash -n` OK.
- F1: `pytest test_static_grep.py` = 9 passed (T-1115 strengthened, still green).
- `ruff check` + `ruff format` clean on test_static_grep.py.
- F3+F2 touched `src/superclaude/skills` → re-ran `make sync-dev`; pr_submit `src↔.claude` SYNCED
  (diff empty); retrigger script +x in mirror. No `.claude/` path staged.
- (Pre-existing `sc-recommend-protocol` verify-sync drift unchanged — orthogonal to pr_submit.)
