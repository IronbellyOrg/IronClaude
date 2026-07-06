# QA Report — Task File Qualitative Review (FINAL-PHASE M3 / actionability + test-correctness lens)

**Topic:** pr_submit V1.1 — complete test surface vacuity / discrimination audit
**Date:** 2026-06-12
**Phase:** task-qualitative (final-phase content/actionability)
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## Overall Verdict: PASS

The adversarial mandate was to find ≥5 vacuous tests across the 7 files. After reading
every test and cross-checking each discriminating assertion against the actual production
seam it claims to guard, **I found zero vacuous tests**. Every regression-guard asserts a
behavior that would genuinely flip if the production logic regressed, and every count/fixture
pin is backed by a real, independently-verified artifact. The "expect ≥5 vacuous" prior is
not borne out by the evidence — each candidate was falsified by reading the source.

`unset VIRTUAL_ENV && uv run pytest tests/pr_submit/ -q` → **175 passed in 0.23s**.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | T-PUSH-WITHOUT-REREVIEW-NO-TICK non-vacuous | none | PASS | fsm.py:992-996 `outcome=="timeout"` breaks BEFORE the `round_counter += 1` at :1001. Test asserts `push_count==1` AND `round_counter==0` AND `TERMINAL_TIMEOUT` — discriminates push-happened from tick-happened. If the increment were not relocated below the timeout-break, this fails. |
| 2 | T-AUGGIE-AT-MOST-ONCE cross-entry guard | none | PASS | fsm.py:763 `if not result.auggie_review_invoked:`. Test drives `_run_fallback` TWICE on the SAME result (calls stays 1) then a FRESH result (calls→2). The fresh-result leg proves the recorder is live, not inert — kills the "guard is a no-op recorder" failure mode. Genuinely exercises the strict-once flag. |
| 3 | 9 INV-001 fence-post tests unchanged + discriminating | none | PASS | loop_guard.py:30 `>= max_rounds`; fsm.py:1001 single increment site. test_t626 asserts counter==2 NOT 3 + push_count==2 + cross-checks `round-sequence-residual-x3.json` (verified: expected `{round_counter:2, push_count:2}`). Parametrized matrix spans max_rounds 1/2/3/5 with N→N pushes. A `>`-gate or off-by-one re-introduction fails ≥3 of these. |
| 4 | decline-first co-occurrence test | none | PASS | test_t1110c builds a findings-bearing review + decline comment; asserts `findings_only` → "findings" (sanity) THEN co-occurrence → "declined". The sanity leg proves the review WOULD be findings — so the decline genuinely wins ordering, not a payload that was never findings. Non-tautological. |
| 5 | backtick test (decline-backtick.json) | none | PASS | `decline-backtick.json` independently verified to contain the literal `` `augment review` `` (backtick-wrapped). Test asserts the substring IS present then `is_decline`→True + classify→"declined". Guards QA-F1 (spec-literal `["']?` char class would miss backticks). Real-shape, not a synthetic that the loose regex trivially matches. |
| 6 | INV-R3 monotone-min fold | none | PASS | run_log.py:192-193 `clamp if prev is None else min(prev, clamp)`. Test appends clamp=1 THEN clamp=3 (higher ordered AFTER) and asserts rebuild==1. The deliberate higher-after-lower ordering is what makes it discriminating: a `last-wins` or `max` fold yields 3 and fails. Non-vacuous. |
| 7 | EventType==37 / IDEMPOTENCY_SETS==6 count pins | none | PASS | Live import confirms `len(EventType)==37` and `len(IDEMPOTENCY_SETS)==6` with the 6th = `auggie_review_invoked`. Tests also assert the 4 new members' exact `.value` strings + that an unknown event_type raises. Drift-detector, not a self-referential count. |
| 8 | T-VANISHED-MONO monotonicity | none | PASS | loop_guard.py:63-69 `vanished_rereview` is an explicit no-op; :58 `on_rereview` ticks only on `observed AND attributed`. Test ticks to 2, vanishes (stays 2), then non-attributed re-review returns False + stays 2. Both the no-decrement AND the no-increment-on-unattributed legs are asserted. |
| 9 | Static-grep gates (T-104/T-N50/T-1101/T-1105/T-1115) | none | PASS | These parse REAL command lines (fenced blocks / non-comment .sh lines, backslash-joined) and assert fork-pinning / token-locus / flag-parity against actual files. T-1115 binds each fallback flag to a `\| \`--flag\`` table ROW in auggie-review.md (not loose substring) + guards the invocation line omits `--no-post-pr`. Substantive, not rubber-stamp. |
| 10 | Detection-contract lock gate (T-210) | none | PASS | Asserts shipped contract `locked:false` → `DetectionContractLocked` raised on default load, absent file raises, and the local-override arm path loads locked:true WITHOUT touching shipped source. The override leg proves the HALT is the lock state, not a missing-file accident. |
| 11 | Run-log determinism / redaction (T-N51/T-N52) | none | PASS | T-N51 asserts 3 distinct raw token shapes are absent AND `[REDACTED]` present (positive+negative). T-N52 replays same config twice and tuple-compares 5 decision fields. Neither is a presence-only smoke test. |
| 12 | Idempotency fix_key comment-id independence | none | PASS | test_fresh_comment_no_double_fix asserts `original.comment_id != fresh.comment_id` (precondition) THEN identical fix_key THEN one fix_applied. The inequality precondition makes the same-key claim meaningful — guards the V1.0 double-fix-on-fresh-comment bug. |

## Summary
- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- Vacuous tests found: **0** (adversarial target was ≥5; falsified by source cross-check)

## Issues Found
None. No vacuous, tautological, or non-discriminating tests detected across the 7 files.

## Adversarial probes that were run and came back clean
- **Sanity-leg falsification**: T-1110c and T-1111/T-1112 (decline AND-requirement from both
  sides) each carry a contrasting "would-be-X" leg, so the positive assertion is not a payload
  that was never going to be anything else.
- **Recorder-liveness falsification**: T-AUGGIE-AT-MOST-ONCE's fresh-result leg (calls→2)
  rules out an inert recorder masquerading as a held guard — the single most likely way a
  "strict-once" test goes vacuous.
- **Fold-direction falsification**: the monotone-min test deliberately orders the higher clamp
  AFTER the lower, defeating a last-wins/max regression.
- **Count-pin drift**: EventType==37 and IDEMPOTENCY_SETS==6 verified by live import, not
  trusted from the assertion literal.
- **Fixture reality**: all 8 referenced fixtures exist on disk; decline-backtick and
  round-sequence-residual-x3 contents read directly and matched their expected blocks.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on the prior structural/M-gate PASS for: file existence, import resolution, section
  numbering, test collection. I did not re-verify those; I focused on semantic test-correctness.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Verified fsm.py:1001 increment sits BELOW the timeout/decline breaks (:990, :995) by Reading
  fsm.py:980-1004 — structural pass cannot tell whether the relocation is correct; only reading
  the control-flow ordering does. (T-PUSH-WITHOUT-REREVIEW-NO-TICK non-vacuity.)
- Verified `_run_fallback` strict-once at fsm.py:763 and the run_log min-fold at run_log.py:192
  by Read — confirms the tests guard real branch logic, not just symbol presence.
- Verified EventType==37 / IDEMPOTENCY_SETS==6 by LIVE `uv run python` import (not by trusting
  the test literal) — independent tool evidence that the count-pin tests are drift-detectors.
- Read decline-backtick.json + round-sequence-residual-x3.json directly to confirm fixture
  bodies match the in-test expectations (real-shape, not synthetic-trivial).

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 | Grep: 4 | Glob: 0 | Bash: 5 (1 pytest + 4 verification)
No web research performed (instructed: no web search).

## Recommendations
- None blocking. The V1.1 regression-guard surface is non-vacuous and discriminating; M3
  actionability gate is satisfied. Proceed.

## QA Complete

VERDICT: PASS
