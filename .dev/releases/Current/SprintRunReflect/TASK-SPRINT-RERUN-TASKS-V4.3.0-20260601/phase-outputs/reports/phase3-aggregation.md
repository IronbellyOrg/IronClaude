# Phase 3 Aggregation — Rerun Engine (`rerun_tasks.py`)

**Phase 3 status:** COMPLETE — all 10 main items (3.1–3.10) checked, ready for QA gate.

**Primary artifact:** `src/superclaude/cli/sprint/rerun_tasks.py` — **1425 LOC** (`wc -l`).
(Over the ~280 TDD target; the overage is explicit `debug_log` trace events, multi-paragraph
docstrings, in-code divergence notes, and the widened-signature safety machinery approved during
execution.)

**Lint result:** `All checks passed!` (ruff, run via worktree-absolute path) — see
`phase-outputs/test-results/phase3-lint{.txt,-summary.md}`. One real bug (F821
`verify_checkpoint_files` undefined) plus 2 F401s caught and fixed within Step 3.10.

**Secondary artifact:** `src/superclaude/cli/sprint/config.py` — additive `PHASE_FILE_PATTERN`
widen (R-F4 resolution: makes `phase-Nr-tasklist.md` discoverable). Lint-clean.

## Output files (Phase 3)

| Path | Producer | Size (bytes) |
|------|----------|--------------|
| `src/superclaude/cli/sprint/rerun_tasks.py` | Steps 3.1–3.9 | (1425 lines) |
| `src/superclaude/cli/sprint/config.py` (edit) | R-F4 (Step 3.3 support) | (additive) |
| `phase-outputs/test-results/phase3-lint.txt` | Step 3.10 | 1197 |
| `phase-outputs/test-results/phase3-lint-summary.md` | Step 3.10 | 1676 |
| `phase-outputs/reports/phase3-aggregation.md` | Step PG3.1 | (this file) |

## Public symbols (13 — all grep-verified present)

| Symbol | Section | Purpose |
|--------|---------|---------|
| `TASK_BLOCK_PATTERN` | A | Module regex for `### T<PP>.<TT>` blocks (TDD §T1 line 24) |
| `extract_phase_subset` | A | Slice target task blocks + round-trip validate + SHA + write sub-tasklist |
| `build_rerun_bundle_dir` | B | Claim `rerun-<ts>/` with collision auto-suffix (T8.6) |
| `build_sub_index` | B | Write `tasklist-index-Nr.md` (discoverable by `discover_phases`) |
| `walk_dependencies` | C | Results-driven dep gate + transitive 50%-ceiling (T3) |
| `discover_failed_tasks_from_transcripts` | D | Legacy fallback classifier (T6 lines 122-126) |
| `flip_target_checkboxes` | E | Rerun provenance block + defensive checkbox flip (T4) |
| `restore_checkboxes_on_abort` | E | Byte-exact revert on abort (T4 line 65) |
| `finalize_checkboxes_on_success` | E | Accumulating `rerun_history` on success (T4 line 64) |
| `stash_and_restore_deliverables` | F | Pre-rerun deliverable stash (T8.4) |
| `restore_from_bundle` | F | `--restore` replay |
| `select_default_recoverable_tasks` | F2 | Default-to-FAIL_RECOVERABLE nomination (OQ#3 line 256) |
| `run_rerun_tasks` | G | 15-step orchestration entrypoint (T1-T9; R-F6/R-F7) |

## Ready-for-QA assertion

Phase 3 is **READY FOR rf-qa task-integrity verification**. All 10 items complete; module imports
clean via the worktree interpreter; ruff clean; 13/13 public symbols present; every section
smoke-tested (extract round-trip, bundle discoverability/collision, 6 dep-walk branches, 5
transcript-classification buckets, provenance+restore byte-exactness, stash/restore round-trip,
default nomination, dry-run orchestration). Known approved divergences (R-F4 regex widen, checkbox
results-driven model, `parse_tasklist`/`extract_phase_signals` API corrections, `execute_sprint`
phases/release_dir isolation, widened signatures on `walk_dependencies`/`stash_and_restore_deliverables`)
are documented in `### Phase 3 - Rerun Findings`. The rf-qa gate should adversarially re-verify these
against source.
