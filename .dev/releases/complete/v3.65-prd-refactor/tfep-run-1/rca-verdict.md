# TFEP Forensic RCA Verdict — Obligation Scanner Meta-Context Cluster

Date: 2026-04-03
Scope: `tests/roadmap/test_obligation_scanner_meta_context.py` (5 failing tests)
Evidence sources:
- `/config/workspace/IronClaude/.dev/releases/backlog/prd-skill-refactor/tfep-run-1/context.yaml`
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/obligation_scanner.py`
- `/config/workspace/IronClaude/tests/roadmap/test_obligation_scanner_meta_context.py`
- Live run: `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -q`

## Executive conclusion
This cluster is **mixed-cause**:
1) Two failures are **test expectation defects** (expected values conflict with current/meta-context policy semantics).
2) Three failures are **implementation defects/regressions**, primarily from interaction effects between FR-MOD1.9 additions and pre-existing scanner mechanics (line-level context loss in code blocks, over-broad obligation creation in discharge lines, and brittle component matching for discharge).

---

## Per-failing-test forensic verdict

### 1) `test_is_meta_context[Do not remove the mock yet-18-False-double_negation]`
- Observed: expected `False`, got `True`.
- Code path: `_is_meta_context()` checks `_NEGATION_PREFIX_RE` against prefix and returns `True` when prefix contains `not`/`remove`-class cues.
- Root cause: **Test expectation issue**. Current Layer-2 logic intentionally classifies negation/removal-prefixed context as meta-context. The phrase "Do not remove the mock yet" is a negation/control statement, not affirmative scaffold introduction.
- Corrective action: Update expected outcome to `True` (or adjust test case text if intent is to represent affirmative usage).

### 2) `test_is_meta_context[Remove old stubs and add new placeholder-30-False-affirmative_second_term]`
- Observed: expected `False`, got `True`.
- Code path: `_is_meta_context()` evaluates line-level cues (prefix + full-line historical/removal terms); line contains `Remove ...`, which triggers meta-context classification.
- Root cause: **Test expectation issue** for current policy model. The classifier is line-level, not clause-scoped, so the second scaffold term on same line inherits removal/meta cue.
- Corrective action: Either
  - update expectation to `True` for current line-level policy, or
  - split into two lines in fixture if test intends clause-sensitive behavior.

### 3) `test_mixed_real_and_meta_same_document`
- Observed: expected `undischarged_count == 0`, got `3`.
- Evidence from scanner output on this fixture:
  - obligations detected in both creation and discharge/verification lines,
  - all `discharged=False`,
  - high-severity undischarged remained from phase 1 + phase 2.
- Root causes:
  1. **Implementation issue**: scanner still creates obligations on discharge lines (e.g., `Replace placeholder...`, `Wire skeleton...`) because scaffold detection runs before semantic suppression of discharge-intent lines.
  2. **Implementation issue**: component extraction/matching is brittle (`create` vs `replace` extracted as component tokens in observed run), causing `_has_discharge()` dual-condition to fail (`component in later content` mismatch), so obvious replacements are not recognized as discharge.
  3. Secondary: verification line is demoted to MEDIUM as intended, but discharge failure upstream leaves high undischarged count.
- Corrective action: prioritize implementation fix so discharge-intent lines are not treated as new obligations and improve component extraction for stable noun targets.

### 4) `test_code_block_still_medium`
- Observed: expected at least one MEDIUM obligation, got none.
- Fixture: single-line fenced block body (` ```python\nmock_data = {}\n``` `).
- Root cause: **Implementation regression** in code-block demotion path due to section/line context reconstruction:
  - scanner can miss/alter code-block context when phase text is sliced and line context is stripped, causing term detection to lose fenced-block placement and stay HIGH or not produce expected demotion behavior for this minimal fixture.
- Corrective action: harden absolute-position/code-block membership calculation against section slicing and minimal fenced-block inputs; add explicit regression case for single-line code fences.

### 5) `test_discharge_mechanism_unchanged`
- Observed: expected at least one discharged obligation, got none.
- Fixture:
  - Phase 1: `Create stub handler`
  - Phase 2: `Replace stub handler with real implementation`
- Root cause: **Implementation issue (pre-existing logic now exposed by new suite)**:
  - scanner treats phase-2 line as a fresh scaffold obligation (contains `stub`) and
  - discharge matching relies on extracted component string equality/containment; with generic extracted component terms, cross-phase discharge can fail to link phase-1 obligation.
- Corrective action: same as failure #3, plus targeted unit coverage for two-phase `create stub` -> `replace stub` flow.

---

## Classification summary
- Test expectation defects: **2/5** (failures #1, #2)
- Implementation defects/regressions: **3/5** (failures #3, #4, #5)

## Confidence
High (>=0.9): failure signatures reproduced; behavior traced to concrete code paths and runtime evidence.
