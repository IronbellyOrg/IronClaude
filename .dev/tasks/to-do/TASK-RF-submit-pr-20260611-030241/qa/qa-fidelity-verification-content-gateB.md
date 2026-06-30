# QA Report — Content Verification (Phase Gate B M4 fidelity fix)

**Topic:** sc:pr-submit recovery tests + docs (post-fidelity-fix)
**Date:** 2026-06-11
**Phase:** report-qualitative / fidelity-fix-verification
**Mode:** `fix_authorization: false` (verify only)
**Scope:** Confirm Branch B/C tests capture spec INTENT (not cosmetic); F-4 wording stays spec-faithful.

---

## Overall Verdict: PASS

The two new tests genuinely capture the spec's INTENT for INV-007 Branch B and Branch C. They are
regression-catching, not cosmetic: each asserts the discriminating behavior the spec mandates and
would fail if recovery wrongly collapsed the branches. The F-4 wording change preserves the
drop-not-downgrade attribution while correctly narrowing the over-broad "identical" claim.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Branch B re-drives push for SAME cycle | PASS | test L289-293 asserts `branch == BRANCH_B_NOT_LANDED` AND `resume_state == MonitorState.S4_PUSHING`; matches spec §12.1 L771-772 ("return to the pre-push path for the same cycle") and recovery.py:123 (`return BRANCH_B_NOT_LANDED, MonitorState.S4_PUSHING`) |
| 2 | Branch B does NOT recompute the fix (no `push_completed` synthesized) | PASS | test L303-305: `completed = [...push_completed]; assert completed == []`. This is the regression-catching assertion — if recovery wrongly marked it completed, this fails. Matches spec L772 "without recomputing the fix" |
| 3 | Branch B appends only `push_aborted_or_not_landed{recovered:true}` | PASS | test L297-302 asserts exactly one `push_aborted_or_not_landed` with `recovered is True`; matches spec L770-771 and recovery.py:116-122 |
| 4 | Branch C → HALT_HUMAN with observed remote SHA | PASS | test L338-339 asserts `branch == BRANCH_C_AMBIGUOUS` AND `resume_state == MonitorState.HALT_HUMAN`; matches spec §12.1 L773 and recovery.py:135 |
| 5 | Branch C records `observed_remote_sha` + reason | PASS | test L341-345 asserts one `terminal_halted` with `reason == "ambiguous_remote_tip"` AND `observed_remote_sha == "zzz999"`; matches spec L773 ("+ observed remote SHA") and recovery.py:128-131 |
| 6 | Tests genuinely exercise `resolve_crash_window` | PASS | both tests call `detect_crash_window(rl)` then `resolve_crash_window(rl, dangling, remote_reachable=False/None, ...)` against a real RunLog with a real dangling `push_initiated` event (test L274-289, L318-335). Not stubs |
| 7 | Coverage rise corroborates real exercise | PASS | fix report L84-86 claims recovery.py 59%→70%; the `remote_reachable is False` branch (recovery.py:113-123) and the ambiguous fall-through (125-135) were previously uncovered (only Branch A path at 102-111 was hit). Independently consistent: 2 new tests cover the 2 previously-dead branches |
| 8 | EventType literals match enum | PASS | `push_aborted_or_not_landed` = models.py:70; `terminal_halted` = models.py:67; `push_completed` = models.py:58. All test string literals match the enum `.value`s |
| 9 | F-4 wording preserves spec-faithful meaning | PASS | finding-verify.md:15-16 still cites auggie SKILL.md:22 as the **verbatim** governing contract (quote intact, L18-19); L22 now reads "states the same drop-not-downgrade principle" instead of "identical contract" — drop-not-downgrade attribution preserved, scope over-claim removed (matches consolidated finding F-4) |
| 10 | New tests pass | PASS | `pytest test_crash_recovery.py` → `test_crash_window_branch_b_not_landed PASSED`, `test_crash_window_branch_c_ambiguous PASSED`, 15 passed |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0

## Spec-Intent Analysis (the core question)

**Branch B is genuinely intent-capturing, not cosmetic.** The decisive evidence is the
`assert completed == []` assertion (test L305). The spec's distinguishing feature of Branch B vs
Branch A is precisely this: Branch A synthesizes `push_completed{recovered:true}` and resumes S5;
Branch B must NOT — it appends `push_aborted_or_not_landed` and re-drives S4 *without recomputing the
fix*. A regression that wrongly routed a not-landed push down the Branch-A path (synthesizing a
completion) would be caught by this assertion. The paired `resume_state == S4_PUSHING` assertion
guards the "same cycle re-drive" half of the rule. Together they fence both halves of spec L771-772.

**Branch C is genuinely intent-capturing.** The spec's distinguishing feature is HALT_HUMAN carrying
the *observed remote SHA* (so a human can adjudicate the unrelated tip). The test asserts both the
HALT terminal state and `observed_remote_sha == "zzz999"` — a regression dropping the observed SHA
(the field that makes the halt actionable) would fail at L345.

**No double-counting / no leniency concern.** Each branch test sets up its own isolated dangling
`push_initiated` and drives the real `detect_crash_window` → `resolve_crash_window` path. The
inputs (`remote_reachable=False` / `=None`) are the exact 3-way discriminator the spec defines, and
the assertions target the spec's discriminating outputs, not incidental side effects.

## Issues Found
None. (No CRITICAL, IMPORTANT, or MINOR content issues in the verified scope.)

## Out-of-Scope Note (not a finding in this scope)
The fix report (L95-99) records a pre-existing `make verify-sync` drift
(`.claude/skills/sc-recommend-protocol` with no `src/` counterpart). This is unrelated to the
F-1..F-4 fidelity fix and outside this verification's scope; the one in-scope synced file
(`finding-verify.md`) is confirmed present and consistent with `src/`. Noted for visibility only.

## Self-Audit
1. **Factual claims verified against source:** 10 — every test assertion cross-checked against
   recovery.py branch logic, spec §12.1 L754-776, and models.py enum values.
2. **Files read to verify:** `recovery.py` (full), `test_crash_recovery.py` (full), `models.py:50-79`
   (EventType enum), `merged-spec.md:740-789` (INV-007 3-way), `finding-verify.md:15-24` (F-4 region),
   plus both QA input reports.
3. **Why trust this with 0 issues:** I did not rely on the fix report's self-claims. I independently
   read recovery.py and confirmed Branch B returns `S4_PUSHING` (L123) and Branch C returns
   `HALT_HUMAN` (L135); I confirmed the `assert completed == []` regression guard exists at test L305;
   I confirmed the enum literals; and I ran the tests live (15 passed). The spec-intent claim rests on
   the `completed == []` / `observed_remote_sha` assertions being the actual discriminators, which I
   traced to spec L771-773.
4. **Web research:** none performed; all verification was local-file and live-test bound.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 3

## QA Complete

## VERDICT: PASS
