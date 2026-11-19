# Calibration Report (persisted by the parent from the `confidence-calibrator` agent's returned report)

**Card under calibration**: tier1-card.md (this folder)
**Rubric**: reflection-rubric.md (5-dimension reflect rubric)
**Card tier**: 1 | **Mode**: pre | flags: depth standard, no_escalate false, tier unpinned

## Verification of the card's grounded checks (by the calibrator, by Read)

Verified: `install_core.py:8` `import filecmp` with its only use at :123; the single call at :97; `install_keep.py:10-15` imports stdlib only (no cycle); `same_content` clears the cache first (install_keep.py:22 at the time of the run) and keeps the `OSError` to False behaviour; the test file has no `import os` (lines 3-9) and the neighbour test is at line 101; `PRINCIPLES.md` is shipped (indirectly: `KNOWN_CORE_FILES` and the existing test); the plan passes the quick gate; Task 2's cache-priming design is sound; the F3 plugin check is sound. All five inferred quotes appear verbatim in `source.md` line 1. Not verified by the calibrator (it had only Read): the repo-wide `_same_content` grep. The parent ran it afterwards: the only hits outside `.dev` are `install_core.py:97` and `:121`; there is no other copy of `install_core.py` in the tree.

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.95 | Every check carries a file:line or symbol and each tested one matched; only the repo-wide grep was unverified (now closed by the parent) |
| Coverage completeness | 0.80 | Union coverage 1.00 and all rows mapped, but parsed coverage is null and `coverage_degraded` fires, so the 1.00 anchor is not met |
| Deviation-classification clarity | 0.75 | No deviation claimed; the card never labels anything Aligned, Refinement, Drift or Regression |
| Risk surface coverage | 0.75 | Covers import cycle, test-priming premise, line drift and the fix check; misses the repo-wide references to the private name, the import-order lint and the global cache-clear side effect |
| Recommendation actionability | 0.70 | "Locate by symbol" is concrete; no explicit proceed or fix recommendation with a command |

## Stage-2 trace

| Step | Value | Notes |
|---|---|---|
| arithmetic_mean(five) | 0.79 | (0.95 + 0.80 + 0.75 + 0.75 + 0.70) / 5 |
| S_scope | 2 | at most 5 |
| S_domains | 2 | code, tests |
| S_dev_density | 0.0 | at most 0.05 |
| Threshold check | 0.79 < 0.85 | rubric: C < 0.85 is an automatic ESCALATE |
| Parse-density guard | inferred 5 > parsed 0 | forbids a Tier 1 stop by protocol, whatever C is |
| Structural C-rules | skipped | troubleshoot-only inputs null; not applicable to a reflect calibration |
| **calibrated** | **0.79** | |

## Confidence

- Self-reported (card): 0.92 (not used as input)
- **Calibrated**: 0.79 (delta -0.13; the substance is accurate, the gap is the form the rubric rewards: no deviation labels, no explicit recommendation, a thin risk register, degraded parsed coverage)

## Escalation recommendation

- **Verdict**: ESCALATE (Tier 2)
- **Reason**: `low_confidence` (0.79 < 0.85); the parse-density guard is a second, independent trigger
- No execution restriction (`no_escalate` false, tier unpinned)
- The plan itself looks correct and low-risk; escalating is protocol, not a sign of a plan defect

## Gaps the card missed (calibrator, all minor)

1. Repo-wide references to `_same_content` unconfirmed (closed by the parent: none).
2. Ruff import order: add the relative import in its own block after the stdlib block (the project selects the `I` rules; `install_user_setup.py:31-32` does it this way).
3. Task 2 leaves "different bytes of the same length" unspecified; flip one byte of the shipped content so the bytes really differ.
4. The shared function clears the process-wide `filecmp` cache on every comparison: a speed cost only, not mentioned in the card.
5. The card has no deviation category and no explicit recommendation line (card-form gap).

## Notes
- The card's own Timestamp (01:40:30Z) is later than the clock supplied to the calibrator (01:40:15Z), a clock mismatch with no effect on scoring.
- Skipped inputs: behaviour_definitions_path, tasklist_path, locus_path, assertions_path.
