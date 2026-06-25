# QA Report — Structural / Evidence-Quality Lens (Step QG.2b)

**Topic:** FR-RH2 R6 — widening the reflect Tier-2 adversarial seam (`ensemble.py`)
**Date:** 2026-06-22
**Lens:** evidence-quality (structural) · ADVERSARIAL STANCE · `fix_authorization: false` (report-only)
**Note:** The rf-qa agent delivered this report inline (it does not write `.md` files itself); the orchestrator persisted it here verbatim for the QG.5 consolidation glob.

## Overall Verdict: PASS

Zero issues found. Every code change maps to a real anchor in `ensemble.py`, the frozen-file diff is **independently confirmed EMPTY** (re-run by the agent, not trusted from the recorded proof), the diff-proof file matches the independent observation, and no hallucinated anchors / wrong line refs / overstated coverage were found.

## Items Reviewed (16/16 PASS)

| # | Check | Result |
|---|-------|--------|
| 1 | `AdversarialScoreFn` alias widened to `-> AdversarialResult \| None` (ensemble.py:103) | PASS |
| 2 | `AdversarialResult` dataclass has all 6 fields (ensemble.py:72–99) | PASS |
| 3 | `run_adversarial_scorer` returns `AdversarialResult \| None`; `None` on child failure | PASS |
| 4 | `build_reflect_contract` threads new fields (kwargs + return dict) | PASS |
| 5 | `regression_present:False` literal REPLACED with param | PASS |
| 6 | `unauthorized_deviation_present:False` literal REPLACED | PASS |
| 7 | `needs_human_decision`/`user_decision_required` REPLACED (mirror) | PASS |
| 8 | `deviation_count_by_class` all-zero literal REPLACED with threaded param | PASS |
| 9 | **Independent** frozen-file diff of contract.py + models.py EMPTY (re-run, exit 0) | PASS |
| 10 | Diff-proof file records EMPTY diff, byte-consistent with independent run | PASS |
| 11 | `_halted_reason` routes `regression_present is True` → HALTED (contract.py:315; models HALTED:10) | PASS |
| 12 | Schema claim `merged_output_path \| string\|null` real (research 02:65) | PASS |
| 13 | I12 + U11 present in working tree | PASS |
| 14 | Test fixtures `_distinct_stub`/`_config`/`_FIXED_SCORE` exist | PASS |
| 15 | Referenced baseline file exists | PASS |
| 16 | Red-then-green: new tests pass now (`2 passed`) | PASS |

**Confidence:** 16/16 verified, 100%. Tool engagement: 3 Read + 5 Bash (≈6 grep blocks + 1 pytest).

## Issues Found

None. Adversarial hunt across signature claims, the (independently re-run) frozen-file diff, the schema citation, code-comment line refs, and the red-then-green test claim turned up no fabrications.
