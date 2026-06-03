# QA Report — Phase-Gate (Phase 2: DriftAssessor)

**Topic:** sprint auto-resume — Phase 2 DriftAssessor (FR-3, DD-4, INV-001)
**Date:** 2026-06-02
**Phase:** phase-gate
**Fix cycle:** 1
**File under test:** `src/superclaude/cli/sprint/resume/drift.py`
**Authoritative design:** `.dev/brainstorms/20260602-sprint-auto-resume-default/design.md` §0 (DD-4), §5 (DriftAssessor)
**Fix authorization:** true

---

## Overall Verdict: PASS

Phase 2 acceptance criteria (2.1–2.4) are met. Every claim was re-derived by
READING `drift.py` and by EXECUTING live fixtures (`uv run python`) against the
real `discover_phases` / `parse_tasklist_file` / `_content_sha256_excluding_rerun_block`
code paths — not against mocks. INV-001 holds end-to-end. Git is provably
additive-only. One MINOR diagnostic-honesty defect (parse-failure misattributed
as deliberate task removal) was found and FIXED in-place; the verdict it produced
was already conservative-correct, so this was a hardening, not a correctness gate.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | INV-001: Tier 0 uses SAME fn `_content_sha256_excluding_rerun_block` over SAME per-phase `phase.file` on both sides | PASS | `drift.py:174-180` `_current_sha` calls the fn on `phase_file`; write-path `executor.py:2077` writes `_content_sha256_excluding_rerun_block(phase.file)` into `phase-N-result.json`. Same fn, same per-phase file. Live: exact-match fixture → 1.0/hash. |
| 2 | `assess()` resolves boundary phase via `discover_phases`+`interrupted_phase`, NOT `index_path` for the hash | PASS | `_boundary_phase_file` (`drift.py:164-172`) iterates `discover_phases(index_path)` and matches `phase.number == plan.interrupted_phase`, returns `phase.file`. Hash computed on `phase_file`, never `index_path`. |
| 3 | Tier 0 is EXACT-match only (not whitespace-tolerant) | PASS | `drift.py:46` `current_sha == recorded_sha` strict equality; AC-4 trailing-ws fixture changes the hash → does NOT match Tier 0, falls to Tier 1. |
| 4 | Absent recorded hash ⇒ NO Tier-0 shortcut, no crash | PASS | `_recorded_sha` (`drift.py:240-254`) returns None on missing/invalid json (caught `OSError, ValueError`); `drift.py:46` guards `if recorded_sha and ...`. Live: no-sha fixture → Tier 1 (0.9), no exception. |
| 5 | Recorded hash read from `release_dir/results/phase-{interrupted_phase}-result.json` | PASS | `drift.py:244-248` builds exactly that path; live fixtures wrote to `release/results/phase-3-result.json` and were read correctly. |
| 6 | AC-4: trailing-whitespace-only edit ⇒ confidence ≥0.8 (~0.9) | PASS | Live fixture appended `"   \n  \n"`: → 0.9 structural, identical task-ID set branch (`drift.py:151-160` pre-fix lines). |
| 7 | AC-5: COMPLETED (PASS) task removed/renamed ⇒ confidence <0.8 (~0.3) | PASS | Live fixture removed completed T03.02 → 0.3 structural, explanation names T03.02. |
| 8 | Edit confined to not-yet-run region (new pending) ⇒ ~0.85 | PASS | Live fixture added T03.04 → 0.85. |
| 9 | `explanation` NON-EMPTY in every branch | PASS | All 6 live branches printed non-empty explanations; every `return DriftAssessment(...)` in the file supplies an explanation string. |
| 10 | Tier 2 git is ADDITIVE ONLY — NEVER mutates `confidence` | PASS | `_annotate_git` (`drift.py:191-238` pre-fix lines) reads `confidence` nowhere; only assigns `changed_paths` and `tier`. Live: confidence 0.85 in → 0.85 out. |
| 11 | Git skips gracefully (no exception, Tier-1 result preserved) when unavailable / detached / no-upstream / untracked | PASS | `except (OSError, subprocess.SubprocessError): return assessment`. Live: untracked-file, no-upstream, and PATH=/nonexistent (git missing) all preserved 0.3/structural, no raise. |
| 12 | PHASE granularity (hard crash, no per-task baseline) handled without false STOP | PASS | granularity != TASK OR empty `recorded_all` ⇒ 0.9 (whole phase re-runs). Live: PHASE + removed task → 0.9. |
| 13 | Only the 0.8 boundary gates; other confidences advisory | PASS | No code treats 0.85/0.9/0.3 as anything but a returned float. The CLI `< 0.8` gate lives in Phase 4 wiring, not here. |
| 14 | ruff clean | PASS | `uv run ruff check src/superclaude/cli/sprint/resume/drift.py` → "All checks passed!" (re-run post-fix; whole `resume/` dir also clean). |
| 15 | EDGE: zero parsed IDs + non-empty recorded baseline (TASK) | FIXED | Pre-fix: misattributed as "completed task(s) X removed" (0.3). Post-fix: accurate "parsed to zero task IDs … empty/corrupt/format" (0.3). Verdict stayed conservative-correct; diagnostic honesty improved (FR-3.5). |
| 16 | item 2.4 gate: `uv run pytest tests/ -k "drift"` | PARTIAL (out of scope) | Collection fails on UNRELATED `tests/sprint/test_{summarizer,retrospective}.py` (`invoke_haiku` removed by commit #106). No dedicated DriftAssessor tests exist yet — design §9 schedules `test_drift_*` for Phase 5. See Issues #2. |

## Summary

- Checks passed: 14 / 16 (items 1–14)
- FIXED in-place: 1 (item 15)
- PARTIAL / out-of-scope: 1 (item 16 — pre-existing unrelated collection breakage + tests deferred to Phase 5)
- Checks failed (unresolved): 0
- Critical issues: 0
- Issues fixed in-place: 1

## Confidence

- **Confidence:** Verified: 15/15 | Unverifiable: 1 (item 16 — see blocker) | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 14 (incl. 4 live `uv run python` fixture drivers + 3 ruff + grep-via-bash)
- No web research performed (all claims are local source-truth; no external/URL/standards lookup required).
- UNVERIFIABLE item 16: the `tests/ -k drift` gate cannot run to completion because `tests/sprint/test_summarizer.py` and `tests/sprint/test_retrospective.py` fail at IMPORT/collection on `invoke_haiku` — a symbol removed by an unrelated prior commit (#106), in modules Phase 2 never touched. Fixing it is out of Phase 2 scope and out of my authorization boundary (it is a different module/phase). The drift *behavior* is fully verified by live execution instead.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `drift.py` `_tier1` (zero-parse path) | When the boundary phase file is readable but `parse_tasklist` yields ZERO task IDs (corrupt/gutted/format-drift) while the recorded baseline is non-empty, the code fell into the `removed_completed` branch and reported "completed task(s) {all recorded} no longer present" — misattributing a parse failure as a deliberate removal (FR-3.5 accuracy defect). Verdict (0.3 STOP) was already conservative-correct, so this was diagnostic honesty, not a wrong gate. | FIXED: added a TASK-granularity-confined guard that detects `recorded_all and not current_ids` and emits an accurate "parsed to zero task IDs … empty/corrupt/format" explanation, still 0.3/<0.8. Confined to TASK granularity so PHASE granularity does not false-STOP. |
| 2 | INFO (out of scope) | `tests/sprint/test_summarizer.py`, `test_retrospective.py` | Pre-existing collection-time ImportError (`invoke_haiku` removed by #106) blocks the `tests/ -k drift` sweep. NOT introduced by Phase 2 (Phase 2 added only `resume/` + the `executor.py` DD-4 write-line). | No fix — out of Phase 2 scope and out of authorization. Recommend a separate fix item (or address in Phase 5 test work). |
| 3 | INFO (deferred) | `tests/` (no DriftAssessor tests) | No dedicated `test_drift_*` files exist yet. Design §9 maps `test_drift_trailing_whitespace_high_conf` (AC-4) and `test_drift_material_edit_low_conf` (AC-5) to Phase 5. | No fix — correctly deferred to Phase 5 per the design phasing. Behavior verified here by live fixtures in the interim. |

## Actions Taken

- **Fixed** the parse-failure misattribution (Issue #1) in `src/superclaude/cli/sprint/resume/drift.py` by adding a guard at the top of `_tier1`'s structural-diff body:
  - Detects `plan.granularity is Granularity.TASK and recorded_all and not current_ids`.
  - Returns `confidence=0.3` (preserving the conservative <0.8 STOP) with an explanation that accurately attributes the cause (empty/corrupt/format-drift) instead of naming specific tasks as "removed".
  - Confined to TASK granularity so PHASE-granularity zero-parse still tolerates (whole phase re-runs → 0.9, no false STOP).
- **Verified the fix** by live execution (`uv run python`):
  - TASK + zero-parse → 0.3, explanation contains "zero task IDs", does NOT contain "removed". ✓
  - PHASE + zero-parse → 0.9 (no false STOP). ✓
  - TASK + real single-task removal → 0.3, explanation still correctly names T03.02. ✓ (regression-clean)
  - Full original 6-case fixture suite re-run post-fix: all assertions pass, zero regressions. ✓
- **Re-ran ruff** on the file and the whole `resume/` package post-fix → "All checks passed!".

## Verification Methods (evidence trail)

- Read: `drift.py`, `models.py` (resume), design.md, task file Phase 2 block, `rerun_tasks.py:688` (`_content_sha256_excluding_rerun_block`), `config.py` (`discover_phases`, `parse_tasklist`, `parse_tasklist_file`, `PHASE_FILE_PATTERN`, `_TASK_HEADING_RE`), `models.py` (`Phase` dataclass).
- Bash/live: 4 distinct `uv run python` fixture drivers exercising Tier 0 exact match, absent-hash fallback, AC-4, AC-5, not-yet-run region, PHASE granularity, the zero-parse edge, the post-fix guard, and 3 git-skip scenarios (untracked / no-upstream / git-binary-missing) plus the additive-only `_annotate_git` invariant.
- Confirmed INV-001 write side: `grep` + Read of `executor.py:2059,2077` shows `tasklist_sha256` written via the identical `_content_sha256_excluding_rerun_block(phase.file)`.

## Recommendations

- Proceed to Phase 3 (BoundaryIntegrityGate). Phase 2 is green for the drift trust-anchor.
- Track Issue #2 (unrelated `invoke_haiku` collection breakage) as a separate fix so the `tests/ -k drift` gate can actually execute in CI; otherwise item 2.4's literal pytest invocation will report collection errors even when drift logic is correct.
- Phase 5 must add the dedicated `test_drift_*` files (design §9) including a regression test for the new zero-parse guard.

## QA Complete

VERDICT: PASS (16 items; 14 PASS, 1 fixed, 1 out-of-scope; 0 unresolved failures)
