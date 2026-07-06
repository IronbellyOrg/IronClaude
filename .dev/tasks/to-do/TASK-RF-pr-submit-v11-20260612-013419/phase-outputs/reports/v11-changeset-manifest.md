# V1.1 Complete Change-Set Manifest (Phase 7 Gate A)

The full pr_submit V1.1 change-set across all phases, with the FR/INV/T-IDs each file carries
and the per-phase QA verdict. (`AM` = V1.0 file modified for V1.1; NEW = created this build.)

## Deterministic core (`src/superclaude/pr_submit/`)
| File | V1.1 delta | FR/INV/T | Phase gate |
|---|---|---|---|
| models.py (AM) | +2 MonitorState (S5A/S5B), +4 EventType (33→37), +6 SkillResult fields | §6.1 | P2 (validated) |
| classifier.py (AM) | +STATE_DECLINED, +is_decline, decline-first classify+watermark | FR-9.1, T-1110/1111/1112, EC-23 | P3 PASS |
| detection.py (AM) | +3 DetectionContract fields (+backtick regex), from_yaml | FR-9.1 | P3 PASS |
| __init__.py (AM) | re-export is_decline/STATE_DECLINED | — | P3 PASS |
| run_log.py (AM) | +6th idempotency set, +3 folds (count/add-set/monotone-min), 33→37, 5→6 | FR-10.1/2/4, INV-R3, T-1120/1124 | P4 PASS |
| fsm.py (AM) | +clamp_max_rounds, +5 RunConfig seams, +6 transition edges, INV-001 increment RELOCATED (1 site), +_run_fallback single-shot | FR-8/9/10, INV-001 preserved, INV-R1/R2/R3 | P5 PASS |
| recovery.py | UNCHANGED — OQ-1 PENDING | OQ-1 | P5 |

## Skill (`src/superclaude/skills/sc-pr-submit-protocol/`)
| File | V1.1 delta | Phase gate |
|---|---|---|
| SKILL.md (AM) | Wave 6 S5a + Wave 6b fallback + lazy-load rows + 3 Output Contract fields | P6 PASS |
| refs/augment-poll.md (AM) | 3→4 state (+declined) | P6 PASS |
| refs/loop-guard.md (AM) | +INV-R1/R2/R3, +fallback_round_counter, 33→37, 5→6 | P6 PASS |
| refs/state-machine.md (AM) | +S5a/S5b states + §5.2b topology | P6 PASS |
| refs/detection-contract.md (AM) | +3 decline keys | P3/P6 |
| refs/review-retrigger.md (NEW) | R1 re-trigger surface (gh-bearing, T-104) | P6 PASS |
| refs/auggie-fallback.md (NEW) | R2/R3 fallback (gh-free, CORE_PURE_FILES) | P6 PASS |
| scripts/retrigger-review.sh (NEW) | fork-pinned `gh api` POST, +x, exits 0/2 | P6 PASS |

## Tests (`tests/pr_submit/`)
| File | V1.1 delta | Phase gate |
|---|---|---|
| test_detection_contract.py (AM) | +6 decline/watermark/backtick/co-occurrence tests | P3 PASS |
| test_run_log.py (AM) | +4 (37-enum, append-validation, INV-R3 min-fold, R1/R2 folds) | P4 PASS |
| test_idempotency.py (AM) | +2 (T-1120 strict-once, T-1124 resume) | P4 PASS |
| test_loop_guard.py (AM) | +4 (deferred-increment, INV-R1, INV-R3, fallback cap-1); 9 INV-001 fence-post UNCHANGED | P5 PASS |
| test_review_retrigger.py (NEW) | 7 (R1: T-1101..1106 + T-PUSH-WITHOUT-REREVIEW-NO-TICK) | P5 PASS |
| test_auggie_fallback.py (NEW) | 9 (R2/R3: T-1110..1125 + T-AUGGIE-AT-MOST-ONCE + transition dual-surface) | P5 PASS |
| test_static_grep.py (AM) | +auggie-fallback.md to CORE_PURE_FILES, +T-1101/1105/1115 | P6 PASS |
| fixtures (NEW ×8) | decline-comment/backtick/initial-poll/twice, stale-decline-pre-watermark, rereview-attributed/then-decline, auggie-fallback-findings | P3-5 |

## Totals + per-phase verdicts
- `tests/pr_submit/` = **175 passed** (138 baseline → +37 V1.1).
- Per-phase M3 gates: P3 PASS (1 cycle), P4 PASS (0 cycles), P5 PASS (1 cycle, INV-001 verbatim verified), P6 PASS (1 cycle).
- EXACTLY one `round_counter += 1` (fsm.py); INV-001 edge byte-identical; `len(EventType)==37`; `len(IDEMPOTENCY_SETS)==6`.
- NFR-6: core .py + auggie-fallback.md gh-free; review-retrigger.md + script gh-bearing on T-104 path.
- OQ-1 (recovery.py resume target) PENDING human decision; OQ-2 (terminal reuse) followed.
