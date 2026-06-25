# QA Report — Content lens: diff-vs-research correctness (FR-RH2 R6 adversarial seam)

**Lens:** actionability / correctness-of-diff-vs-research (CONTENT)
**Date:** 2026-06-22
**Phase:** doc-qualitative (adapted: implemented-design-vs-recommended-research-design)
**Fix authorization:** false (REPORT ONLY)
**Adversarial stance:** assumed >=1 divergence existed; searched for it.

---

## Overall Verdict: PASS

The implemented design in `src/superclaude/cli/reflect/ensemble.py` matches the RECOMMENDED
research design (06-gap-fill.md GAP-1/2/4/5, 03-contract-consumer-constraints.md §6, 02 §3,
05 §3.4) on every one of the five mandated checkpoints. Zero divergences found after exhaustive
read of the actual change surface, the actual source file, the actual `runner.py` call site,
and a real `git diff` of the frozen files.

---

## Checkpoint Results (the five mandated checks)

| # | Check | Result | Evidence + research anchor |
|---|-------|--------|----------|
| 1 | `AdversarialResult` placed in `ensemble.py` (NOT `models.py`) | PASS | Dataclass defined `ensemble.py:72-99`. `git diff --stat -- ...models.py` printed nothing (empty, exit 0). Research anchor: 06-gap-fill.md:53-54 ("in `ensemble.py` … to stay clear of NFR-7") and :245-247 / :340 ("place `AdversarialResult` in `ensemble.py` to keep `models.py` byte-clean"). |
| 2 | Default scorer populates `convergence_score`+`report_path` LIVE; 3 booleans + counts default CLEAN | PASS | `run_adversarial_scorer` returns `AdversarialResult(convergence_score=extract_convergence_score(parsed), report_path=_extract_adversarial_report_path(parsed))` — `ensemble.py:349-353`. The 3 booleans + `deviation_count_by_class` are NOT passed, so they take the dataclass clean defaults (`ensemble.py:88-98`: `False`/`False`/`False` + all-zero dict). Research anchor: 06-gap-fill.md:61-65 (GAP-2 design step 3), :88-91 (field-by-field "WIRED, default-clean pending producer"). Non-derivation honored (see check note below). |
| 3 | `extract_convergence_score` + `parse_adversarial_contract` signatures UNCHANGED (wrapped, not replaced) | PASS | `git diff -- ensemble.py \| grep` for `def extract_convergence_score`/`def parse_adversarial_contract` returned `NO_SIGNATURE_LINES_TOUCHED`. Both functions read intact at `ensemble.py:418-439` and `:356-371`; the widened scorer CALLS them (`ensemble.py:349-352`). Research anchor: 06-gap-fill.md:181-183, :210, :219-222 (keep both signatures intact → U10/U5 stay green); 03 §1 P3 note "wrap, don't replace." U10 reported PASS in qa-input-surface.md:15. |
| 4 | `runner.py:425` untouched — positional `run_tier2_ensemble(config)`, no score-fn kwarg | PASS | Read `runner.py:418-426`: line 425 is exactly `run_tier2_ensemble(config)` (positional, no `adversarial_score_fn=`). Research anchor: 06-gap-fill.md:194 (P6 "NONE … calls with positional `config` ONLY"), :335 (P6 insulated). The new `run_tier2_ensemble` keeps `adversarial_score_fn` keyword-only with default `None` (`ensemble.py:173`), so the positional call still resolves to the default-scorer path. |
| 5 | `report_path` reads child `merged_output_path` and prefers it over swarm merged.md only as documented | PASS | `_extract_adversarial_report_path` reads `contract.get("merged_output_path")` (string|null) with the same `return_contract:` unwrap as the score extractor — `ensemble.py:442-457`. `_select_report_path` prefers `adversarial_report_path` first, then swarm, then worker final_path, then None — `ensemble.py:607-624`. Research anchor: 02 §3 line 68 (`merged_output_path \| string\|null` is the Mode-A child field) + §5 line 109-111 (swarm path was the prior source); 05 §3.4 QA CRITICAL #2 verbatim ("Do not set `report_path` to swarm `merged.md` … keep `merged.md` only as a subrun artifact") and 05 §3.5 R5 (line 202: "align `report_path` selection with the now-available adversarial report"). |

---

## Adversarial deep-dive (where I tried to break it)

1. **Non-conflation (GAP-4): could a low/None convergence score auto-flip `regression_present`?**
   NO. `run_adversarial_scorer` never sets `regression_present` from the score — it only fills
   `convergence_score` + `report_path` (`ensemble.py:349-353`). The docstring explicitly pins
   GAP-4 ("`regression_present` is NEVER auto-derived from a low/None convergence score",
   `ensemble.py:331-333`). Matches 06-gap-fill.md:141-150 and 03 §1 (DEGRADE rung 2 vs HALT
   rung 3). PASS.

2. **None-result (child failure) → does the null-convergence DEGRADE fallback survive?**
   YES. On `proc.wait() != 0` the scorer returns `None` (`ensemble.py:347-348`). At the call
   site `adversarial_result is None` leaves `adversarial_convergence_score` at `None`
   (`ensemble.py:268-269`) and every destructured local defaults clean (`ensemble.py:275-297`),
   so `build_reflect_contract` emits `adversarial_convergence_score=None` → at `tier_reached==2`
   `derive_verdict` routes `null-convergence` DEGRADE. Matches 06-gap-fill.md:160-169. PASS.

3. **Type-trap (self-BLOCK): are the load-bearing booleans genuine Python `bool`?**
   YES. Dataclass fields are typed `bool` with literal `False` defaults (`ensemble.py:88-90`);
   the I12 test injects literal `True` (`regression_present=True`). No `"true"`/`1` path exists.
   Matches 03 §3 / §6 type-trap warning (`contract.py:200-209` `malformed-contract-boolean`).
   PASS.

4. **`user_decision_required` mirror:** the builder sets `user_decision_required` =
   `needs_human_decision` (`ensemble.py:523`), preserving the existing mirror semantics rather
   than introducing a 6th independent kwarg. Matches 06-gap-fill.md:90 ("+ mirror
   `user_decision_required`") and the OI-1 disposition. PASS.

5. **FR-RH2.7 frozen-file proof:** `git diff --stat -- contract.py models.py` → empty (exit 0),
   the exact GAP-5 Part-A acceptance command (06-gap-fill.md:240). PASS.

6. **`deviation_count_by_class` None-handling:** the builder normalizes a `None` kwarg back to
   the all-zero dict (`ensemble.py:493-499`), so the call-site's `None` (when no seam ran,
   `ensemble.py:290-294`) still yields a 4-key zero dict in the contract — consistent with
   `_extract_deviations` expectations (03 §2). PASS.

---

## Self-Audit

**(a) Reliance list — items I did NOT re-verify structurally (out of this lens' scope):**
- Relied on qa-input-surface.md's reported pytest results (2353 passed; I12/U11/U10/I1/U6 PASS)
  and the NFR-7 no-nesting / ruff gates — those are structural/test-execution claims owned by
  the structural QA lens, not this content lens.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Check 1 placement — verified by `git diff --stat -- models.py` (empty) + Read of
  `ensemble.py:72-99`, not by trusting the report's prose.
- Check 3 signature-stability — verified by `git diff … | grep` for the two `def` lines
  (`NO_SIGNATURE_LINES_TOUCHED`) + Read of `ensemble.py:418-439`/`:356-371`, independent of the
  report's "wrap not replace" claim.
- Check 4 runner untouched — verified by direct Read of `runner.py:418-426` (positional
  `run_tier2_ensemble(config)`), not by trusting P6's research assertion.
- Check 5 source field — verified `merged_output_path` is the Mode-A child field by reading
  02-adversarial-child-output-schema.md:68 directly, then matched it to
  `_extract_adversarial_report_path` (`ensemble.py:456`).

---

## Summary

- Checkpoints passed: 5 / 5
- Adversarial deep-dive probes passed: 6 / 6
- Divergences from recommended research design: 0
- Critical issues: 0 | Important: 0 | Minor: 0
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 2 (frozen-file diff stat; signature-line grep)

## Recommendations
- None blocking. The diff is a faithful, low-blast-radius realization of the recommended design.
- (Non-blocking, already documented as OQ-PRODUCER in 06-gap-fill.md:102-114): the 3 booleans +
  per-class counts remain default-clean until the sc-adversarial producer emits real signal —
  this is intended scope, not a divergence.

## QA Complete
