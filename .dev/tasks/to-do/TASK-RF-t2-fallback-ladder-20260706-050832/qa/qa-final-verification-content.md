# QA Report — Content/Correctness Verification (Step 6.G11, independent re-run)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832 (reflect Tier-2 fallback model ladder)
**Date:** 2026-07-07
**Phase:** doc/task-qualitative — content verification of 3 PR-review fix commits
**Fix authorization:** false (REPORT ONLY)
**Stance:** adversarial — assumed the fixes were wrong; tried to prove it.
**Commits under scrutiny:** `f0afdaa3` (all_workers), `16e9e1bb` (per-slot stub), `dcc0dcd2` (docstring)

---

## Overall Verdict: PASS

All three fixes are correct, their regression tests are load-bearing and network-free,
and the full `reflect or swarm` suite is green. The adversarial monotonic-diversity
counter-example attempt **failed to find a counter-example** (the fix is provably
verdict-preserving). Zero real issues found.

## Per-Fix Correctness Table

| # | Fix | Claim | Verified | Result |
|---|-----|-------|----------|--------|
| 1 | `f0afdaa3` all_workers | Feeding full augmented set fixes "healthy→partial" + under-reported reviewer_count WITHOUT flipping verdict | Traced `run_tier2_ensemble`→`reduce_wave3`/`determine_status`/`build_reflect_contract`/`derive_verdict`; monotonicity proof; degrade case preserved | PASS |
| 2 | `16e9e1bb` per-slot stub | Stub arm binds distinct, vendor-distinct transport per slot; vendors disjoint from T2 pool; production path unchanged | Read `_diversity._vendor_from_model_id`; ran empirical classification; diffed openai_compat arm (0-change) | PASS |
| 3 | `dcc0dcd2` docstring | `run_fallback_ladder` docstring now correctly describes all_workers vs contributing_workers | Read docstring diff vs actual return (fallback.py:587-594) | PASS |
| 4 | Regression tests | Both assert a signal that FAILS pre-fix; network-free | Reasoned pre-fix values; confirmed StubTransport/injected scorer, no ClaudeProcess/HTTP | PASS |
| 5 | No content regression | `pytest -k "reflect or swarm"` 0 failed | Ran suite | PASS (2566 passed) |

---

## Fix 1 — `f0afdaa3` (feed `all_workers` to reduce_wave3/contract)

**Trace verified (ensemble.py):**
- L389: `normalized_workers = ladder_outcome.all_workers` (was `.contributing_workers`).
- L404-408: `reduce_wave3(normalized_workers, ..., workers_requested=reviewers)`.
- L473/507: `build_reflect_contract(normalized_workers, ..., reviewers_requested=reviewers)`.
- `all_workers` (fallback.py:587) = `list(primaries)` (successes AND failures) + every dispatched fallback worker.

**determine_status (reduce.py:158-216):** `M = success count`, `N = workers_requested`.
Healthy 3/3: pre-fix fed contributing (size-2 subset) → `determine_status(2,3)` = **partial**,
reviewer_count=2. Post-fix feeds 3 primaries → `determine_status(3,3)` = **success**,
reviewer_count=3. Regression reproduced and fixed exactly as claimed.

**Monotonic-diversity counter-example attempt — RESULT: NO COUNTER-EXAMPLE EXISTS.**
Both `compute_model_class_diversity` and `compute_vendor_diversity` (_diversity.py) filter to
`status=="success"` then count DISTINCT model_ids / vendors. `contributing ⊆ full-success-set`
(select_contributing_set only ever returns a subset of successes). Count-of-distinct-values is
**monotonic non-decreasing under superset**, so the full set can never have LOWER model-class or
vendor diversity than the trimmed subset. I attempted the construction "2 same-vendor primary
successes + 1 distinct-vendor fallback": that makes the full set MORE diverse (multi), never less,
and `select_contributing_set` would then also pick a multi subset. The claimed bug direction is
mathematically impossible.

**Verdict-preservation proof (does NOT push degraded→PASS, does NOT flip healthy):**
`satisfies_tier2` = `reviewer_count>=2 AND model_class=="full" AND (vendor=="multi" OR allow_single)`
— all three components monotonic in set size. Therefore:
- **Certifying case:** full set certifies ⟺ contributing certifies; both are multi (or both
  single-with-allow_single_vendor). `derive_verdict` triggers 7/8 (contract.py:280-287) key on
  the same diversity value → identical verdict. reviewer_count rises 2→3 but reviewer_count is
  NOT a gated field (grep of contract.py: only tier_reached/diversity/merge_method/statuses/bools
  gate). `tier_reached` = `2 if reviewer_count>=2` — contributing already ≥2 when certified, so
  identical.
- **Non-certifying (degrade) case:** `select_contributing_set` returns ALL successes (fallback.py:260),
  so `contributing == full-success-set` exactly → identical diversity, identical reviewer_count,
  identical `tier_reached` → **identical DEGRADE**. Genuine-failure case (1 success, fallback fails)
  → reviewer_count=1 → `merge_method="single-reviewer-fallback"` → trigger 10 DEGRADE (exit 11)
  preserved.
- Swarm subrun `status` (partial/success) feeds ONLY `subrun_status`/`subrun_status_partial`
  (telemetry, contract.py L790 "never gated"); the DEGRADE gate (trigger 11a) keys on
  `adversarial_subrun_status`, not the swarm status. So the partial→success change is telemetry-honesty,
  not a verdict change.

**Additive-only confirmed:** `git diff 8d7672b6 HEAD` on `contract.py`, `swarm/models.py`,
`swarm/reduce.py` = **empty (0 diff)**. The verdict-gating module is untouched.

## Fix 2 — `16e9e1bb` (distinct per-slot stub)

**Empirically verified vendor classification (`_vendor_from_model_id`, _diversity.py:39-55):**
- T1 fallback slots: `T1Model01`→`gemini-t1fallback-stub`→**google**; `T1Model02`→`llama-t1fallback-stub`→**meta**. Distinct model_ids AND distinct vendors.
- Third slot (if present) → `claude-*`→anthropic.
- T2 stub pool: qwen / deepseek / openai (gpt) / mistral.
- Disjointness `{google, meta, anthropic} ∩ {qwen, deepseek, openai, mistral} = ∅` — confirmed. So a surviving-primary + fallback mix is always vendor-diverse, and a both-slots-dispatched run (google+meta) restores the Tier-2 vendor-diversity gate.

**Production path unchanged:** the diff touches ONLY the `if transport == "stub"` arm. The
`openai_compat` arm (`make_fallback_slot_factory`, ensemble.py:255-293) is byte-identical — it
already bound distinct per-slot models by ladder position.

## Fix 3 — `dcc0dcd2` (docstring)

Pre-fix docstring said "Returns the contributing worker set (the list handed to
`build_reflect_contract`)" — FALSE after f0afdaa3. New docstring (fallback.py:430-436) correctly
distinguishes `contributing_workers` (certification-basis telemetry only) from `all_workers`
(handed to reduce_wave3/build_reflect_contract). Matches the actual return (fallback.py:589-594)
and the `LadderOutcome` class docstring (fallback.py:85-104). Doc-only, no behavior change.

## Fix 4 — Regression tests are load-bearing + network-free

**`test_gate_on_healthy_pool_not_mismarked_partial_full_reviewer_count`**
(test_ensemble_fallback_engage.py):
- Pre-fix evaluation: contributing=2 → `reviewer_count==3` asserts **fails** (would be 2);
  swarm `status=="success"` asserts **fails** (would be "partial" from `determine_status(2,3)`).
  Two independent load-bearing assertions.
- Network-free: `_all_success_factory` returns `StubTransport`; `adversarial_score_fn=_const_score`
  injected → no `ClaudeProcess`, no HTTP. Confirmed via imports (StubTransport, injected scorer).
- Also asserts `t2_fallback.engaged is False` (healthy primaries meet quorum, ladder never dispatches)
  — the common real-world config (fallback enabled + healthy pool). Verdict PASS/exit 0 asserted.

**`test_resolve_t1_fallback_factory_stub_arm_is_vendor_distinct_per_slot`**
(test_ensemble_fallback_stub.py):
- Pre-fix: single shared `StubTransport(model_id="gemini-t1fallback-stub")` → `m1==m2` →
  `assert m1 != m2` **fails**, and vendor-distinct assert **fails**. Load-bearing.
- Network-free: calls the factory directly, reads `.model`; no dispatch, no transport I/O.

## Fix 5 — Full suite

`VIRTUAL_ENV= uv run pytest tests/ -k "reflect or swarm" -q`
→ **2566 passed, 28 skipped, 8881 deselected, 1 xpassed in 19.63s. 0 failed.**
Matches the `16e9e1bb` commit-message claim (2566 passed).

---

## Confidence

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 4 | Glob: 0 | Bash: 8 (incl. 2 pytest runs + 1 empirical vendor-classification python probe + git diff/show)

## Self-Audit

1. Independently verified claims against source: 5 fix-level claims + monotonicity proof, each
   traced to specific file:line (ensemble.py:389/404/473/799/803-804, reduce.py:158-216,
   contract.py:280-306/366-367, fallback.py:246-260/587-594, _diversity.py:8-55) and 2 executed
   pytest runs + 1 executed python vendor-classification probe.
2. Files read: ensemble.py, fallback.py, contract.py, _diversity.py, reduce.py, both test diffs.
3. Trust basis for the PASS: every load-bearing claim is backed by an executed command
   (empirical vendor table, 2566-pass suite, 0-diff on the gating modules) or a closed
   mathematical argument (monotonic distinct-count under superset), not by assertion.
4. No external web research required (all local-file-bound); Tavily not invoked.

## Issues Found

None. (0 CRITICAL, 0 IMPORTANT, 0 MINOR.)

## QA Complete
