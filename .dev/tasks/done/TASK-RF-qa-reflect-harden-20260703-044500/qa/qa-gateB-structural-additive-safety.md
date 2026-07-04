# QA Report — Task Integrity (Gate B: Structural Additive-Safety)

**Topic:** FX7 honest-accounting additive-safety invariance (cli/reflect)
**Date:** 2026-07-03
**Phase:** task-integrity
**Lens:** additive-safety-exemption-invariance
**Fix authorization:** false (REPORT ONLY)
**Fix cycle:** N/A

---

## Overall Verdict: PASS

Adversarial mandate was to find ">=5 non-additive changes." After exhaustive
diff-read + full verdict-path trace + test-suite execution, **zero** non-additive
changes were found. Every one of the 4 changed source files is strictly additive:
new defaulted fields, new None-guarded kwarg, new append-only dict keys. No existing
constant, emitted token, routing branch, field order, or field type was altered.

## Prohibitions Verified (all HOLD)

| # | Prohibition | Result | Evidence (file:line) |
|---|-------------|--------|----------------------|
| 1 | `_VERIFICATION_SKIP_EXEMPTIONS` byte-unchanged | PASS | contract.py:36-38 reads `{"read-only-project", "tool-unavailable", "--no-verify"}`; `git diff` touches NO hunk in lines 25-45 (grep on diff returned "NO diff hunks touch those symbols") |
| 2 | `_DEGRADED_COMPONENTS_HALT_SET` byte-unchanged; `reviewer-shortfall` NOT a member | PASS | contract.py:31-33 reads `{"serena","auggie","env-aliases","evidence-validator","serena:context-excluded"}`; `reviewer-shortfall` absent; no diff hunk touches the symbol |
| 3 | Emitted `verification_skip_reason` byte-unchanged (`"tool-unavailable"`, not flipped) | PASS | ensemble.py:572 emits `"verification_skip_reason": "tool-unavailable"` — appears as a **context line** in the diff (no `+` prefix), i.e. unchanged. It IS an exemption member, so degrade-trigger 12 (contract.py:293-297) does NOT fire — R2-F2 design preserved |
| 4 | `status` NEVER set to `"degraded"` | PASS | ensemble.py:559 sets `"status": "success"` — the only status literal in the builder. Grep for `"degraded"` in ensemble.py returns only comment text at :529. No misroute to tier-mismatch HALTED |
| 5 | No non-int in `deviation_count_by_class.regression`; no `regression:unknown`; `regression_verified` is SEPARATE bool | PASS | ensemble.py:554 defaults `"regression": 0` (int); ensemble.py:579 emits `"regression_verified": False` as a separate key. `_extract_deviations` returns `dict[str,int]` (contract.py:90). No `regression:unknown` written anywhere |
| 6 | New `ReflectResult` fields APPEND-ONLY + DEFAULTED, no reorder/retype | PASS | models.py:154-156 appends `verification_verified/reviewers_verified/regression_verified: bool = False` AFTER `reviewer_grounding_root` and BEFORE `@property outcome` — they are the last fields, all defaulted; dataclass ordering valid (no non-default field follows). Diff has zero `-` lines |
| 7 | `reflect_post` + sidecar keys APPEND-ONLY, no key-order break | PASS | runner.py:117-119 (`_build_reflect_post_value`) and runner.py:238-240 (`write_sidecar`) append the 3 siblings at the END of each dict. Diff has zero `-` lines. test_writeback.py asserts presence-not-exact-order (per code comment at runner.py:115) |
| 8 | Existing consumers of `status`/`regression_present`/`verification_ran`/`verification_skip_reason`/`degraded_components` unaffected | PASS | Full `_degraded_reason` (contract.py:264-310) + `_halted_reason` (contract.py:313-334) traced: NONE read the new `*_verified` siblings; only `_make_result` (contract.py:130-132) maps them for visibility. Trigger 1 uses EXACT membership (`any(token in _DEGRADED_COMPONENTS_HALT_SET ...)`, contract.py:265) — a populated `["reviewer-shortfall"]` list does NOT flip the verdict. 53/53 reflect tests pass |

## Additional Adversarial Checks

| Check | Result | Evidence |
|-------|--------|----------|
| `reviewers_requested` threads REQUESTED (not survived) count | PASS | ensemble.py:191 `reviewers = int(config.reviewers)` (requested from config) → passed as `reviewers_requested=reviewers` at :329. `reviewer_count = len(succeeded)` (:521) is survived. Shortfall test `reviewer_count < reviewers_requested` (:539) is correct semantics |
| None-guard prevents `>= None` TypeError on direct/test calls | PASS | ensemble.py:535-537: `True if reviewers_requested is None else reviewer_count >= reviewers_requested` — vacuous-satisfy on None, never raises |
| New `*_verified` bools NOT registered as verdict-bearing | PASS | grep confirms they are absent from `_LOAD_BEARING_BOOL_FIELDS` (contract.py:47-57). Consistent with visibility-only intent; adding them was optional per research §3.4 |
| No degrade trigger inspects `degraded_components` LENGTH/non-emptiness | PASS | `_degraded_reason` triggers 1-14 (contract.py:264-310): only trigger 1 reads the list, via exact membership. No `if degraded_components:` / `len(...)` truthiness check exists |
| Test diffs additive-only (no weakened/removed assertion masking a behavior change) | PASS | Removed-lines scan across test_ensemble_unit.py, test_verdict_mapping.py, test_writeback.py, pr_submit/conftest.py returned EMPTY — zero `-` assertion lines |
| Two aggressive verdict-DEGRADE routings DEFERRED, not shipped | PASS | Both PENDING files exist under phase-outputs/plans/: `fx7-degrade-on-reviewer-shortfall-DECISION.md` + `fx7-degrade-on-unverified-DECISION.md`. Neither routing appears in the source diff. Research §3.4/§5 warned of exactly these hazards; implementation honored all four |

## Summary
- Prohibitions verified: 8 / 8 PASS
- Additional adversarial checks: 6 / 6 PASS
- Non-additive changes found: 0 (mandate expected >=5; none exist)
- Critical issues: 0
- Tests: 53/53 pass (`tests/cli/reflect/test_ensemble_unit.py`, `test_verdict_mapping.py`, `test_writeback.py`)

## Issues Found
None. No CRITICAL, IMPORTANT, or MINOR issue detected on the additive-safety lens.

## Confidence
**Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

Every prohibition and adversarial check was verified with direct tool evidence
(Read of the current file state + git diff hunk analysis + full verdict-path
symbol trace + live test execution). No item relies on agent claims.

**Tool engagement:** Read: 3 | Grep: 6 | Glob: 0 | Bash: 8

## Recommendations
- Green light on the additive-safety / exemption-invariance lens. The FX7 change
  ships ONLY visible honest-accounting; both verdict-DEGRADE routings remain
  correctly deferred as needs_human_decision PENDINGs.
- No fix required (and none authorized — REPORT ONLY).

## QA Complete
