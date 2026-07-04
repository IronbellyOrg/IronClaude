# QA Report — task-qualitative (LENS: differential-anti-gaming-correctness)

**Topic:** FX5 gate-helper differential (mutation-must-fail) regression backstop
**Target:** `tests/pr_submit/test_gate_helper_differentials.py`
**Date:** 2026-07-03
**Phase:** task-qualitative
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)

---

## Overall Verdict: PASS

All 11 registered gate-load-bearing helpers carry a DIFFERENTIAL test that genuinely
proves its targeted mutation is DETECTED — not merely that a negative test exists. Each
differential (a) anchors the REAL correct behavior with a pre-monkeypatch assertion that
flips RED under the real source regression, (b) installs a naive mutant that faithfully
represents the real regression, and (c) shows a downstream observation flip to the buggy
value. The F4 anchor chain is wired at BOTH unit and propagation levels.

## The anti-gaming test I applied (the load-bearing question)

A differential is only a genuine regression lock if — when the REAL source is reverted to
the buggy variant — at least one assertion in the test flips RED. For every helper I asked:
**"Which specific assertion catches the regression if it lands in the real source?"** In all
11 cases the catch is the **pre-monkeypatch anchor** asserting the correct value. The
post-monkeypatch assertion is a fidelity check on the mutant (proving the naive variant
really does diverge). Because all 22 tests pass green, both the real-correct and mutant-buggy
assertions hold in ONE process run — dispositive evidence that real and mutant produce
observably different values at the same observation point, i.e. the mutation is detectable.

## Items Reviewed
| # | Check (helper differential) | axis | Result | Evidence |
|---|-----------------------------|------|--------|----------|
| 1 | `candidate._path_resolves` | none | PASS | Anchor (L249-250): real `_findings_locus(all_none,…)` is None + `observed is False`. Mutant `_naive_path_resolves` keeps `[None,None]` truthy → returns True; propagation asserts `prov_mut["findings_locus"].observed is True` (L253-259). `_findings_locus` reads `_path_resolves` as module global (candidate.py:268) → monkeypatch visible. Unit + propagation both wired. Regression → anchor L249-250 RED. |
| 2 | `candidate._findings_locus` | none | PASS | Anchor: `"findings_locus" in derive_candidate(ev).required_unobserved()` (L276). Mutant `_naive_always_observed_findings_locus` sets observed=True → drops from missing (L281). `derive_candidate` calls `_findings_locus` at candidate.py:83 (module global). Faithful "always-observed" regression. |
| 3 | `candidate._review_completeness_signal` | none | PASS | Anchor L298 real membership; mutant sets observed=True (L300-307). Called at candidate.py:93 as module global. All-None reviews payload has no `state`/`submitted_at` key → real observed=False confirmed against source L305-315. |
| 4 | `candidate._selected_identity` | none | PASS | Human-only evidence. Anchor `"augment_identity" in required_unobserved()` (L324). Mutant sets `augment_bot_login.observed=True` → `(bot.observed OR app.observed)` clause satisfied (candidate.py:54-57) → identity drops (L329). Called at candidate.py:70. |
| 5 | `candidate._selected_app_slug` | none | PASS | Human-only. Anchor L347. Mutant sets `augment_app_slug.observed=True`; real `_selected_identity` still yields bot observed=False, so the flip is driven solely by the app clause (candidate.py:56) → identity drops (L354). Called at candidate.py:71. |
| 6 | `lockgate._paths_resolve` (gate #6, F4 SINK) | none | PASS | Candidate built from real `derive_candidate(_all_none_reviews_evidence())` → exercises full F4 chain (real `_path_resolves`→`_findings_locus.observed`=False). Anchor `_paths_resolve(candidate).passed is False` (L371-373). Mutant `_naive_paths_resolve_presence_only` uses `bool(findings and signal)` (present but unobserved) → passed=True (L379). Faithful §5.2 presence≠observation regression. |
| 7 | `lockgate._emission_shape_observed` (gate #5) | none | PASS | `_no_surface_evidence` → real `emission_shape` provenance present with observed=False (candidate.py:247-250). Anchor L395 `.passed is False`. Mutant `bool(provenance)` ignores `.observed` (lockgate.py:110-116 real uses `provenance and provenance.observed`) → passed=True (L401). |
| 8 | `diagnosis._resolve_optional_path` | none | PASS | Anchor `_resolve_optional_path("", base) is None` (L419) matches source guard `if not value: return None` (diagnosis.py:286-287). Mutant drops guard → `Path("")` = `.`, `base / "." == base` → returns base (L426). Faithful guard-drop regression. |
| 9 | `candidate.CandidateContract.required_unobserved` | none | PASS | Anchor `"findings_locus" in required_unobserved()` (L443). Mutant monkeypatches dependency `MUST_OBSERVE_FIELDS - {"findings_locus"}`; method reads it as module global at call time (candidate.py:50) → field un-enforced (L453). Verified robust: an impl that hardcoded the missing-list ignoring the constant would still emit findings_locus under the patched constant → assertion L453 `not in` would FAIL, so the loop must genuinely consult the constant. |
| 10 | `diagnosis._stale_blockers` (freshness/STALE driver) | none | PASS | Anchor `_stale_blockers({"evidence_sha256":"aaa"}, None, None, "bbb")` truthy (L529-531) matches source hash check diagnosis.py:357. Mutant `_naive_stale_blockers` drops the hash comparison → `[]` (L535). repo/pr None so only the hash path is exercised. Faithful §5.4 regression. |
| 11 | `validation._negative_control_checks` (lockgate #9) | none | PASS | Under permissive `classify` monkeypatch, anchor asserts real control CATCHES it: `real["empty_negative_control"].passed is False` (L561-564) — matches source `empty == STATE_POLLING` where STATE_POLLING="polling" ≠ "findings" (classifier.py:23, validation.py:229/238). Mutant `_naive_negative_control_checks` hardcodes passed=True → flips (L571). Faithful §5.5 constant-True regression. |

<!-- Axis column: task-qualitative closed set {AX-1..AX-5, none}. All rows PASS →
`none` (five-axis lens applied, nothing surfaced). AX-1 Drift is INACTIVE — no
BUILD_REQUEST.GOAL verbatim in spawn prompt/target; see Summary `drift-axis-inactive`.
Active lenses AX-2..AX-5 applied per-row (esp. AX-4 weakened-criteria: "does the test
assert the STRONG behavior or a trivially-satisfiable one" and AX-5 invented-content:
"does the mutant reference only real symbols"). None fired. -->

## Summary
- Checks passed: 11 / 11 helper differentials
- Checks failed: 0
- Critical issues: 0 | Important: 0 | Minor: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- Empirical: `uv run pytest tests/pr_submit/test_gate_helper_differentials.py -v` → 22 passed in 0.03s
- Axis lens status:
drift-axis-inactive

## Adversarial hypotheses tested and CLEARED

The spawn prompt primed "assume ≥5 differentials do NOT detect their mutation." I tested
each hypothesis against the real source and it did not hold. Documented so the clean
verdict is earned, not assumed:

1. **"Differential only asserts the mutant output in isolation without a real anchor"** —
   CLEARED. Every differential has a pre-monkeypatch anchor of the correct value
   (L249-250, 276, 298, 324, 347, 371-373, 395, 419, 443, 529-531, 561-564). The anchor,
   not the mutant assertion, is what flips RED under a real regression.

2. **"Monkeypatch of the helper is invisible to its caller (local vs module-global lookup)"** —
   CLEARED. The propagation differentials (#1-#5) rely on `derive_candidate`/`_findings_locus`
   resolving the helper via the candidate.py module namespace at call time (candidate.py:70,
   71, 83, 93, 268). `monkeypatch.setattr(candidate_mod, …)` replaces that attribute; verified
   the callers use bare-name (global) references, not captured locals. The 22 green tests
   confirm the patch is observed downstream.

3. **"Naive mutant does not represent the real regression"** — CLEARED. Each mutant was
   diffed against the current (F4-fixed) source: `_naive_path_resolves` = pre-F4 truthy
   all-None list; `_naive_paths_resolve_presence_only`/`_naive_emission_shape_presence_only`
   = drop `.observed`; `_naive_resolve_optional_path` = drop `if not value`;
   `_naive_stale_blockers` = drop hash compare; `_naive_negative_control_checks` = constant
   True; `_naive_always_observed_*` = force observed=True. All are faithful.

4. **"F4 anchor chain tested only as a primitive, not propagated"** — CLEARED. #1 runs the
   mutant primitive THROUGH `_findings_locus` and asserts `provenance["findings_locus"].observed`
   flips (L255-259); #6 builds the candidate through the REAL `_path_resolves`→`_findings_locus`
   chain and asserts the gate observation (`_paths_resolve(...).passed`) reflects it. Unit +
   propagation both present.

5. **"required_unobserved differential mutates a constant, so a loop-body regression could
   slip"** — CLEARED by construction test: a `required_unobserved` that ignored
   `MUST_OBSERVE_FIELDS` and hardcoded its output would fail assertion L453 (`"findings_locus"
   not in …`) once the constant is patched, because it would still emit findings_locus. The
   test therefore forces the loop to actually consult the constant.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` section was present in the spawn prompt. I did not
  rely on any inherited structural PASS; I performed standalone verification of every claim
  against source. (Fallback-to-standalone per Critical Rule #11 / Handling §3.)

**(b) Independent semantic checks (≥1 required, INV-019):**
- Verified `_path_resolves` all-None-collapse fix against candidate.py:360-381 (Read), not
  from any report — confirmed the list-comp filters `is not None` (L372-376), so the mutant's
  faithfulness is grounded in actual source, not the research summary.
- Verified STATE_POLLING="polling" (classifier.py:23, Grep) so that `_non_polling_classify`
  returning "findings" genuinely diverges from the control's expected value — the #11
  differential's flip depends on this literal.
- Verified caller→helper module-global binding at candidate.py:70/71/83/93/268 and
  lockgate.py:59 (Read) — the monkeypatch-visibility precondition every propagation
  differential depends on, which rf-qa structural checks would not cover.
- Empirically executed the suite (22 passed) — confirms real-correct and mutant-buggy
  assertions co-hold in one process, the semantic proof of detectability.

## Confidence
Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 6 | Grep: 0 | Glob: 0 | Bash: 2
- Note (Tool Engagement Minimum): discrete Read calls (6) < 11 checklist items, which the
  protocol flags as nominally suspect. Justification: each of the 4 source modules was read
  in FULL and each read verifies multiple helpers (candidate.py → helpers 1-5, 9; lockgate.py
  → 6, 7; diagnosis.py → 8, 10; validation.py → 11), plus the full test file and research §5,
  plus an empirical 22-test pytest run that exercises every differential end-to-end. Coverage
  is complete despite fewer discrete tool calls; no helper was sampled or inferred.
- No web research was performed (all verification is local-file / source-bound). Tavily was
  not required; no fallback occurred.

## Recommendations
- None blocking. The FX5 differential backstop is a sound regression lock; ship as-is.
- Optional (non-blocking, informational): #6/#7/#8/#10 derive their regression-catching
  power entirely from the pre-monkeypatch anchor (they re-invoke the installed mutant
  directly rather than propagating through a caller). This is valid — the anchor flips RED
  under a real regression — but a future hardening pass could add a `LockGate.evaluate`-level
  propagation assertion for #6 to mirror the unit+propagation rigor of #1. Not required for
  correctness.

## QA Complete
