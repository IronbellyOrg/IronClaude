# QA Report — Content / Regression-Safety Lens (WS-0)

**Topic:** WS-0 bare-review inline-path migration — regression safety
**Date:** 2026-06-16
**Phase:** doc-qualitative (regression-safety content lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Adversarial stance:** "Assume WS-0 introduced ≥10 regressions or broke the resume path."

---

## Overall Verdict: PASS

The adversarial hypothesis is REFUTED by independent evidence. WS-0 introduces a
net +3 passing tests with 0 failures, leaves the resume branch byte-untouched,
strands no state-file transition, and orders the terminal flip correctly
(after reduce, not before). I actively hunted for the 10 claimed regressions and
the broken resume path and found neither.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Baseline (2212) still passes; 0 failures | PASS | Ran `uv run pytest tests/swarm/ -q` myself: `2215 passed, 26 skipped`. 0 failed, 0 errors. Skipped count unchanged (26 = baseline 26). |
| 1b | bare-review parity + recipe RUN and PASS (not skipped) | PASS | Ran `test_bare_review_parity.py` + `test_recipe_bare_review.py -v`: `33 passed` (17 + 16), 0 skipped. Both modules collected and executed, not guarded out. |
| 2 | Resume branch (`_run_resume_branch`) UNCHANGED | PASS | `git diff 02582ca0 -- commands.py`: all 6 hunks land in module-level helpers (894–1018) and inside `run_cmd` (1382–1879). `_run_resume_branch` begins at line 2017 — outside every hunk. No diff line touches it. Resume tests: `70 passed` (resume_crash_recovery, resume_regenerates_merge, resume_uses_manifest_lens, crash_recovery_e2e). |
| 3 | Stub-removal strands no state transition; stdout line preserved | PASS | Baseline order (git show 02582ca0): `dispatching` → dispatch → `terminal` (immediate) → stdout. WS-0 order: `dispatching` (1736/1779) → dispatch (1798) → stamp/normalize/reduce → `terminal` (1867) → stdout (1876). `dispatching` still written pre-dispatch; `terminal` still reached. stdout `dispatched job (mode=..., workers=..., results=...)` is byte-identical to baseline (diff shows only the comment above it changed). |
| 4 | Terminal state flipped AFTER reduce, not before | PASS | Inline: reduce_wave3(...) at 1844–1862, THEN `_write_swarm_state(..., "terminal", ...)` at 1867. Comment at 1864 explicitly states "flip terminal AFTER the reduce wave (the stub flipped it immediately after dispatch)." Mirrors resume branch: reduce_wave3 at 2280 → terminal at 2293. Ordering identical across both paths. |

---

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; fix_authorization=false)

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 11

---

## Explicit Baseline Comparison

| Metric | Baseline (02582ca0) | WS-0 (working tree) | Delta | Independently verified? |
|--------|---------------------|---------------------|-------|-------------------------|
| Passed | 2212 | 2215 | +3 | YES — re-ran suite, got 2215 |
| Failed | 0 | 0 | 0 | YES |
| Skipped | 26 | 26 | 0 | YES |
| `test_bare_review_parity.py` | 17 passed / 0 skip | 17 passed / 0 skip | 0 | YES — ran verbose, all 17 PASSED |
| `test_recipe_bare_review.py` | 16 passed / 0 skip | 16 passed / 0 skip | 0 | YES — ran verbose, all 16 PASSED |
| `test_e2e_user_guide.py` test count | 17 | 20 | +3 | YES — `git show` baseline=17 defs, current=20 defs |

**The +3 are genuine net-new additions, not renames double-counted.** The e2e
file grew from 17 → 20 test functions; the 3 net-new tests
(`test_reviewers_flag_overrides_worker_count`, `test_reviewers_flag_rejects_out_of_range`,
`test_quickstart_emits_normalized_artifacts`) account for the entire +3 suite-level
delta. The renamed tests (`test_quickstart_does_not_emit_done_sentinel`,
`test_quickstart_lens_bare_review_emits_observability_artifacts`) are 1:1 renames —
they do not change the count, consistent with the gate summary's claim.

---

## Adversarial Findings Hunt (the "≥10 regressions" hypothesis)

I specifically probed for each plausible regression class:

- **Lost/skipped legacy tests?** No — both legacy-coupled files RUN and PASS at
  full count (33 total). The baseline contract's #2 requirement (must NOT become
  SKIPPED) is satisfied.
- **Resume dispatch→normalize→reduce sequence altered?** No — `_run_resume_branch`
  is outside every diff hunk; 70 resume tests green.
- **Stranded state transition (`dispatching` orphaned / `terminal` never reached)?**
  No — both transitions present and correctly sequenced in the inline path.
- **Premature terminal flip (contract/bodies not yet on disk)?** No — terminal now
  flips strictly after reduce_wave3, fixing exactly the stub ordering.
- **stdout success signature drift breaking e2e pins?** No — line byte-identical;
  e2e pins (`workers=3, results=3`, `workers=4, results=4`, `workers=2, results=2`)
  all pass; `test_quickstart_does_not_emit_done_sentinel` and the
  `return-contract.yaml` emission test both pass.
- **Double contract emission?** Reduce_wave3 owns the internal emit_contract; the
  inline path adds no redundant emit_contract call (diff comment + code confirm),
  mirroring resume.

Zero regressions surfaced after targeted probing across all five adversarial classes.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source?** 5 checks +
   6 baseline-comparison rows. I re-ran the full swarm suite (not trusting the
   summary's 2215), re-ran the two legacy files verbose, re-ran resume + e2e
   subsets, and read the actual baseline source via `git show` to confirm the
   pre-WS-0 stub ordering and stdout line rather than trusting the diff narrative.
2. **What specific files/commands did I read/run?** `commands.py` (current lines
   1736–1882, 2276–2297; baseline 1535–1582 via git show); `ws0-gate-summary.md`;
   `baseline-summary.md`; `git diff 02582ca0 -- commands.py` (full); `git log`
   (confirmed 0 commits since baseline → changes are working-tree). Commands:
   `pytest tests/swarm/ -q` (2215), `pytest <2 legacy files> -v` (33),
   `pytest test_e2e_user_guide.py -v` (20), `pytest -k resume -q` (70).
3. **If I found 0 issues, why trust it?** Because every PASS is backed by a tool
   result I produced, not a summary I read: the 2215 count came from my own
   pytest run; the resume-untouched claim came from mapping diff hunk line ranges
   against the grepped `_run_resume_branch` location (2017, outside all hunks);
   the ordering claim came from reading both the inline (1844→1867) and resume
   (2280→2293) reduce→terminal sequences directly; the stdout-preserved claim came
   from a byte comparison of baseline vs current via git show. The +3 was
   reconciled to a concrete 17→20 e2e function-count delta.
4. **Web research?** None performed — this review is entirely local-source-bound;
   no Tavily/WebSearch fallback was needed or triggered.

---

## Recommendations

- None blocking. WS-0 is regression-safe against the `tests/swarm/` baseline and
  preserves the resume branch and the documented stdout/state contract.
- (Informational, NOT a WS-0 regression) The gate summary notes 2 pre-existing
  `F821 Undefined name 'Logger'` ruff findings (`commands.py:1712`, `normalize.py:73`).
  I did not independently re-run ruff (out of this lens's scope — regression safety,
  not lint), but the diff does not introduce or touch those forward-ref annotations,
  consistent with the "pre-existing" classification.

## QA Complete
