# QA Report — task-qualitative (numbers-metrics lens) — Phase 4 (P3) storm-bound

**Topic:** sprint-CLI 429 recovery — Phase 4 (P3) storm-bound arithmetic / numeric assertions
**Date:** 2026-06-17
**Phase:** task-qualitative (numbers-metrics lens only)
**Fix cycle:** N/A
**fix_authorization:** false (READ-ONLY)

> Note: this file previously held a Phase 2 (P1 detection fixtures) numbers-metrics report. This
> spawn is the Phase 4 (P3) storm-bound/numeric-assertion lens (distinct scope, distinct claims) and
> writes to the same designated output path. Prior P1 content superseded.

---

## Overall Verdict: PASS

All 7 numeric/arithmetic claims in scope verified against actual test + source code with file:line
evidence. Adversarial stance applied: I attempted to find a wrong literal, a wrong bound, an
off-by-one in the cap boundary, a stale model literal, or a storm-bound collapsed to `≤ cap`. None
found. Every literal matches the spec §4 Layer 3 / edge-case-#3 contract
(`cap ≤ total ≤ cap+(K-1)` AND `total < K×cap`, NOT strictly `≤ cap`).

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | K>1 latch asserts `cap ≤ total ≤ cap+(K-1)` AND `total < K*cap` (NOT `≤ cap`) | none | PASS | test_executor.py:804-805 |
| 2 | always-429 K=1 small-cap asserts EXACTLY `cap` spawns | none | PASS | test_executor.py:828 |
| 3 | single-429×cap asserts exactly `cap` spawns (default cap=8) | none | PASS | test_executor.py:728,754 |
| 4 | single-429→clean asserts `session_resets == 1` | none | PASS | test_executor.py:695 |
| 5 | default `max_session_resets` is 8 | none | PASS | recovery_policy.py:46 |
| 6 | `decide` halts at `attempt == cap` (boundary `<`) | none | PASS | recovery_policy.py:69-71; test_recovery_policy.py:18-19 |
| 7 | cooldown-test `exhausted_model` literal == `"claude-opus-4-8"` | none | PASS | test_executor.py:716; fixture L3 |

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (read-only)

## Detailed verification (PASS/FAIL + severity + file:line)

### Claim 1 — K>1 storm bound asserts `cap ≤ total ≤ cap+(K-1)` AND `total < K*cap` — **PASS**
`tests/sprint/test_executor.py` `test_provider_exhaustion_parallel_latch_bounds_spawn_storm`:
- L789: `cap = 3`
- L788: `tasks = self._independent_tasks(4)` → K = `len(tasks)` = 4
- L803: `assert reset_policy._latch_tripped is True`
- L804: `assert cap <= calls["n"] <= cap + (len(tasks) - 1)` → `3 <= total <= 3+(4-1)=6`. Exactly the
  `cap ≤ total ≤ cap+(K-1)` two-sided bound; lower bound is `cap` (not 0/1), upper bound is
  `cap+(K-1)`=6 (NOT `cap`).
- L805: `assert calls["n"] < len(tasks) * cap` → `total < 4*3 = 12`. The `total < K×cap` no-storm
  guard, asserted SEPARATELY with strict `<`.
Adversarial check: upper bound `cap + (len(tasks)-1)` = 6 is strictly greater than `cap`=3 — the
test does NOT collapse to `≤ cap`, matching spec §4 Layer 3 line 232 and edge-case #3. Arithmetic
self-consistent: `cap+(K-1)=6 < K*cap=12`, so the two assertions cannot mutually contradict for
K≥2, cap≥1. Spec match: spec §6.2 row 5 (research 05-test-verification.md:277,280) prescribes
exactly these two bounds. Severity: none.

### Claim 2 — always-429 K=1 small-cap asserts EXACTLY `cap` spawns — **PASS**
`test_provider_exhaustion_single_worker_stops_exactly_at_small_cap`:
- L815: `cap = 3`
- L816-818: `_make_threadsafe_repeating_factory((1, single_account_429.jsonl))` repeats single-account
  429 every spawn (never escalates to cooldown, never passes) → infinite-loop unless capped.
- L828: `assert calls["n"] == cap` — EXACT equality (`==`), not a bound → exactly 3 spawns
  (infinite-loop guard, spec edge-case #9, research:278).
- L829: terminal status `FAIL_PROVIDER_EXHAUSTED`. Severity: none.

### Claim 3 — single-429×cap asserts exactly `cap` spawns (default cap=8) — **PASS**
`test_provider_exhaustion_single_429_stops_at_cap`:
- L728: `cap = 8` (= production default `max_session_resets=8`).
- L738: `reset_policy=SessionResetPolicy(max_session_resets=cap)`.
- L729-731: threadsafe repeating single-account-429 factory.
- L754: `assert calls["n"] == cap` — EXACT equality → exactly 8 spawns.
- L756: `assert payload["halt_reason"] == "provider_exhaustion"` (persisted halt key verified too).
"default cap=8" faithfully represented (local `cap=8` == recovery_policy.py:46 default). Severity: none.

### Claim 4 — single-429→clean asserts `session_resets == 1` — **PASS**
`test_provider_exhaustion_single_429_then_clean_passes`:
- L677-682: scripted factory `[(1, single_account_429), (0, clean_pass)]` — attempt 1 single-account
  429 (one reset), attempt 2 clean pass.
- L692: `assert calls["n"] == 2` (1 initial + 1 reset).
- L694: `assert results[0].status == TaskStatus.PASS`.
- L695: `assert results[0].session_resets == 1` — EXACTLY one reset. Arithmetic consistent: 2 spawns
  = 1 initial + 1 reset ⇒ `session_resets == 1`. Severity: none.

### Claim 5 — default `max_session_resets` is 8 — **PASS**
`src/superclaude/cli/sprint/recovery_policy.py:46`: `max_session_resets: int = 8  # ≈ account-pool size`.
Matches spec §4 Layer 3 line 211, spec §8 Q5 ("default 8"), and manifest deliverable row
(p3-aggregate.md:17). Severity: none.

### Claim 6 — `decide` halts at `attempt == cap` (boundary `<`) — **PASS**
Source `recovery_policy.py:68-71`:
```
if signal is ProviderFailure.SINGLE_ACCOUNT_LIMIT:
    if attempt < self.max_session_resets:
        return Action.RETRY_NEW_SESSION
    return Action.HALT_MODEL_SWITCH
```
Boundary is strict `<`, so `attempt == cap` falls through to `HALT_MODEL_SWITCH`. Parametrized
truth-table `tests/sprint/test_recovery_policy.py:17-19`:
- L17: `(SINGLE_ACCOUNT_LIMIT, 0, RETRY_NEW_SESSION)`
- L18: `(SINGLE_ACCOUNT_LIMIT, 7, RETRY_NEW_SESSION)` → `7 < 8` ⇒ RETRY (= `decide(SINGLE, cap-1)` → RETRY)
- L19: `(SINGLE_ACCOUNT_LIMIT, 8, HALT_MODEL_SWITCH)` → `8 == cap` ⇒ HALT (= `decide(SINGLE, cap)` → HALT)
Policy fixture uses `SessionResetPolicy(max_session_resets=8)` (test_recovery_policy.py:25).
Adversarial off-by-one check: row at attempt=7 (cap-1) is RETRY and row at attempt=8 (cap) is HALT —
boundary correctly at `==cap`, not `cap-1`/`cap+1`. Resolves the research:481 "UNVERIFIED `<` vs `<=`"
item: confirmed `<`. Severity: none.

### Claim 7 — cooldown-test `exhausted_model` literal == `"claude-opus-4-8"` — **PASS**
- Assertion `tests/sprint/test_executor.py:716`: `assert results[0].exhausted_model == "claude-opus-4-8"`.
- Backing fixture `tests/sprint/fixtures/exhaustion/all_account_cooldown.jsonl:3`:
  `...All credentials for model claude-opus-4-8 are cooling down via provider claude`.
Asserted literal byte-matches the model embedded in the fixture cooldown body, so the
`_RE_ALL_ACCOUNT` named group `model` extracts exactly `claude-opus-4-8`. Cross-checks: spec §4
Layer 5 line 267 and research:141,143 — all agree. No version drift (it is `claude-opus-4-8`, NOT
`claude-opus-4.8` / `claude-3-opus`). Severity: none.

## Actions Taken
None — read-only review (fix_authorization: false).

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was supplied; standalone behavior applies. I performed
independent verification of every numeric claim against source and relied on no rf-qa PASS item.
Independent semantic checks run with own tool engagement:
- Storm-bound arithmetic: independently evaluated `cap+(K-1)=6` and `K*cap=12` from literals at
  test_executor.py:788-789,804-805 and confirmed `6 < 12` (the two assertions cannot contradict).
- Cap-boundary semantics: independently traced `attempt < max_session_resets` at recovery_policy.py:69
  and matched truth-table rows 7→RETRY / 8→HALT (test_recovery_policy.py:18-19).
- Model literal: independently opened the cooldown fixture and byte-compared its embedded model name
  to the test assertion (all_account_cooldown.jsonl:3 vs test_executor.py:716).

## Self-Audit
1. **Factual claims independently verified against source code:** 7/7 numeric claims, each tied to a
   specific file:line (test assertions + production boundary in recovery_policy.py + fixture model
   literal). I evaluated storm-bound arithmetic by hand (`6 < 12`) rather than trusting test names.
2. **Files read to verify claims:** `recovery_policy.py` (full), `test_recovery_policy.py` (full),
   `test_executor.py:602-831` (TestPerTaskOrchestration), `all_account_cooldown.jsonl` (full),
   `p3-aggregate.md` (manifest), `research/05-test-verification.md` §6.2, driving spec
   `sprint-429-recovery-spec.md` §4 Layer 3.
3. **Why trust a PASS:** I did not blind-pass — I adversarially probed each literal. Confirmed the
   storm-bound upper bound is `cap+(K-1)`=6 and NOT `cap`=3 (the exact failure mode the spawn
   warned of); confirmed `==cap` boundary (not off-by-one); confirmed `==` (not loose bound) on the
   cap-spawn tests; byte-matched the model literal against its fixture. K is derived (`len(tasks)=4`)
   so I traced it. Verified `cap+(K-1) < K*cap` so the two storm assertions can't mutually contradict.
4. **Web research:** none performed (all checks local-file-bound); Tavily-first N/A this review.

## Confidence
Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 6 | Grep: 1 | Glob: 0 | Bash: 1
(Read+Grep+Glob = 7 ≥ 7 in-scope checks — tool-engagement minimum met. Each Read targeted a file
holding a specific claim; the Grep located exact test-method line offsets.)

## Recommendations
- None blocking. All Phase 4 storm-bound arithmetic and numeric assertions are correct and match
  spec §4 Layer 3 / edge-case #3. Green light from the numbers-metrics lens.

## QA Complete
