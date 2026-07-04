# QA Report — task-qualitative (LENS: no-vacuous-pass-and-visibility)

**Topic:** FX7 additive honest-accounting — reviewer-shortfall + `*_verified` visibility
**Date:** 2026-07-03
**Phase:** task-qualitative (content-lens gate B)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Worktree:** /config/workspace/IronClaude/.dev/worktrees/pr209-harden

---

## Overall Verdict: PASS

FX7 as shipped is neither TOOTHLESS nor OVERREACHING when evaluated against its
ACTUAL design (VISIBILITY of vacuity/shortfall, NOT a verdict flip — the
aggressive verdict-DEGRADE routings were deliberately deferred to PENDING
needs_human_decision HALTs). Every genuine shortfall/vacuity is now observable on
four surfaces (contract → ReflectResult → reflect_post frontmatter → sidecar), a
clean full-reviewer run does not wrongly degrade, and both deferral HALTs are
real and un-applied. I could not construct a falsifying counterexample on either
the toothless or overreach axis.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Genuine reviewer-shortfall no longer invisible: emits `reviewers_verified: false` + visible `reviewer-shortfall` token in `degraded_components`; a NEW test asserts VALUES (not just presence) | none | PASS | Builder ensemble.py:535-540 (`reviewers_verified` False-guarded; token appended on `reviewer_count < reviewers_requested`). Named test: `test_fx7_reviewer_shortfall_populates_visible_token_and_unverified_flag` (test_ensemble_unit.py:431-447) asserts `"reviewer-shortfall" in contract["degraded_components"]` AND `contract["reviewers_verified"] is False` — value assertions, not `key in block`. Reinforced at derivation layer by test_verdict_mapping.py:369-388 (`result.reviewers_verified is False`) and writeback layer test_writeback.py:175-207. All 53 reflect-unit tests green. |
| 2 | Clean full-reviewer UNVERIFIED run STILL routes PASS BY DESIGN (R2-F2 exempt) but is VISIBLE via `verification_verified: false` — EXPECTED, not a defect | none | PASS | ensemble.py:571-577 emits `verification_ran: False` + exempt `verification_skip_reason: "tool-unavailable"` + `verification_verified: False`. derive_verdict Trigger 12 (contract.py:294-297) EXEMPTS because skip reason ∈ `_VERIFICATION_SKIP_EXEMPTIONS` → PASS. `test_fx7_vacuous_no_verify_stays_exempt_but_visible` (test_verdict_mapping.py:391-403) asserts Verdict.PASS/exit 0 AND `result.verification_verified is False`. Fixture vacuous_no_verify.yaml (3 reviewers, exempt) confirms. |
| 3 | Both HALTs real: two DECISION.md PENDING files exist, NOT auto-applied; NO test asserts a non-exempt clean-run skip reason or a shortfall→DEGRADED route | none | PASS | Both files exist under phase-outputs/plans/. Each states `Status: PENDING (NOT auto-applied)`, "What was auto-applied: ONLY Option A". `_DEGRADED_COMPONENTS_HALT_SET` byte-unchanged (contract.py:31-33 — no `reviewer-shortfall` member; grep confirms token appears only in benign/PASS contexts). `_VERIFICATION_SKIP_EXEMPTIONS` byte-unchanged (contract.py:36-38). Integration test_i1 (clean PASS) + test_i3 (2-of-3 pass-eligible) still green (6 passed). No test routes reviewer-shortfall→DEGRADED or a non-exempt clean skip reason. |
| 4 | New `*_verified` fields make vacuity observable to a downstream reader (ReflectResult → reflect_post → sidecar) | none | PASS | ReflectResult carries the 3 fields (models.py:158-160). `_make_result` populates via `c.get(..., False)` (contract.py:130-132). Frontmatter: `_build_reflect_post_value` appends all 3 (runner.py:120-122). Sidecar: `write_sidecar` appends all 3 (runner.py:239-241). Full four-surface path proven end-to-end. |
| 5 | ADVERSARIAL: TOOTHLESS — can a shortfall/vacuity remain INVISIBLE after FX7? | none | PASS | Counterexample FALSIFIED — see Counterexample Analysis. |
| 6 | ADVERSARIAL: OVERREACH — can a clean run now WRONGLY degrade? | none | PASS | Counterexample FALSIFIED — see Counterexample Analysis. |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status: drift-axis-inactive

`drift-axis-inactive` — no BUILD_REQUEST.GOAL verbatim was supplied in the spawn
prompt (this is a bespoke content-lens gate, not a task-file pre-execution audit
with a driving GOAL). AX-1 Drift is lens-disabled for this review; AX-2..AX-5
were applied and surfaced nothing (all rows `none`). This annotation lives in the
Summary block per the canonical rule — it is NOT an Axis-column cell value.

## Counterexample Analysis (adversarial construction)

**Toothless axis — "a shortfall/vacuity STILL invisible after FX7 = FAIL":**

- *Real reviewer shortfall (2-of-3).* The production driver ALWAYS threads the
  requested count: `run_tier2_ensemble` passes `reviewers_requested=reviewers`
  (ensemble.py:329), where `reviewers = int(config.reviewers)` (ensemble.py:191,
  default 3 clamped [2,4]). So on a genuine 2-of-3 run the builder emits BOTH
  `reviewers_verified: False` AND the `reviewer-shortfall` token, and both flow to
  ReflectResult → reflect_post → sidecar. Four visible surfaces. Cannot be made
  invisible. FALSIFIED.
- *The only "invisible" path is the None-guard* (`reviewers_requested is None` →
  `reviewers_verified True`, empty `degraded_components`, ensemble.py:535-540).
  That branch is reachable ONLY from direct/unit-test calls that omit the kwarg —
  it is NEVER the production `run_tier2_ensemble` path, which always supplies the
  count. So it is not a real-run invisibility; it is the deliberate additive-safety
  guard for legacy direct callers (asserted by
  test_fx7_emits_verification_visibility_fields_with_none_guard).
- *Vacuous no-verify.* `verification_verified: False` is hard-emitted on EVERY
  ensemble contract (ensemble.py:577), independent of any kwarg, and flows through
  `_make_result`. Always visible. FALSIFIED.

**Overreach axis — "a clean run that now WRONGLY degrades = FAIL":**

- The three `*_verified` fields are read in EXACTLY ONE place — `_make_result`
  (contract.py:130-132). Grep confirms they appear nowhere in `_degraded_reason`
  or `_halted_reason`. They are structurally incapable of flipping a verdict.
- The `reviewer-shortfall` token is NOT a `_DEGRADED_COMPONENTS_HALT_SET` member
  (contract.py:31-33, byte-unchanged), so a 2-of-3 shortfall stays PASS-eligible —
  proven by test_fx7_reviewer_shortfall_token_does_not_over_degrade (PASS/exit 0)
  and the degraded_reviewer_shortfall.yaml fixture routing PASS, and by the
  untouched test_i3.
- A 3-of-3 clean run keeps `degraded_components == []` and the exempt skip reason
  (test_fx7_clean_run_preserves_exempt_skip_reason_and_empty_degraded; test_i1).
  No degrade. FALSIFIED.

**Conclusion:** The shipped FX7 is calibrated exactly to the VISIBILITY design.
It adds honest signal on every real shortfall/vacuity without touching any
routing constant, and it leaves the deliberate R2-F2 / FR-RH2.9 PASS-eligible
behavior intact. Not toothless (signal is emitted and asserted at 3 layers), not
overreaching (routing constants byte-unchanged, new fields non-routing).

## Issues Found
None.

## Actions Taken
None (fix_authorization: false — report only).

## Self-Audit
This gate was NOT handed an `## Inherited Structural Verdict` block; it ran as a
standalone content-lens review. Per Critical Rule #11 the fallback is independent
verification, which is what every row above documents.

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was provided; nothing was relied upon.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Verdict-routing isolation of the new fields — verified by `grep` of contract.py
  showing `verification_verified`/`reviewers_verified`/`regression_verified` occur
  ONLY at contract.py:130-132 (`_make_result`), absent from `_degraded_reason`
  (contract.py:255-310) and `_halted_reason` (contract.py:313-334). This is the
  load-bearing "no overreach" proof; field PRESENCE alone would not establish it.
- HALT_SET / exemption-set immutability — verified by reading contract.py:31-33
  and :36-38 and cross-checking the two DECISION.md files' "byte-unchanged" claims
  against the live source (both hold).
- Production requested-count threading — verified by reading ensemble.py:191 +
  :329 to confirm the None-guard invisibility branch is unreachable in the real
  driver path (the toothless falsifier).
- Test substance (not rubber-stamp) — verified by reading the assertion bodies of
  the four FX7 tests: they assert VALUES (`is False`, token `in` list, `Verdict.PASS`),
  not mere `key in block`. Ran `uv run pytest` on all three named files (53 passed)
  + integration i1/i3 (6 passed).

## Confidence Gate
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 3 | Glob: 0 | Bash: 4
- No web research performed (all verification was local-file + test-execution
  bound); Tavily-first policy not triggered.
- Every check maps to a specific tool call: Reads of research §2c/§3c/§3.4,
  ensemble.py, contract.py, models.py, runner.py, and the three test files;
  Bash for fixtures, DECISION-file discovery, grep of routing isolation +
  HALT_SET, and two pytest runs.

## Recommendations
- PASS — gate B (content / no-vacuous-pass + visibility) is satisfied. Green light
  to proceed. The two PENDING DECISION.md HALTs (verdict-DEGRADE on shortfall /
  on unverified) correctly remain for explicit human authorization before any
  Option-B non-additive routing is entertained; do not auto-apply them.

## QA Complete
