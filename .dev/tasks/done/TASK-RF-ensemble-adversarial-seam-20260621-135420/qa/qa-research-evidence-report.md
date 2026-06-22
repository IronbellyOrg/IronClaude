# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Wire the adversarial seam in ensemble.py to map real deviation/regression/human-decision/report_path into build_reflect_contract; add regression test asserting derive_verdict != PASS.
**Date:** 2026-06-21
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Scope

Assigned files (5):
- 01-ensemble-seam-inventory.md
- 02-adversarial-child-output-schema.md
- 03-contract-consumer-constraints.md
- 04-test-patterns.md
- 05-template-and-citations.md

Lens focus: EVIDENCE QUALITY — every claim must cite real file paths, line numbers, function names. Adversarial stance: assume errors exist; verify exhaustively.

---

## Verification Log

### Spot-checks performed (well over the mandated 25% of cited anchors)

**ensemble.py (509 lines — R1 said 509: CORRECT)**
- L67 `ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"` — VERIFIED.
- L72 `AdversarialScoreFn = Callable[[list[str], Path], float | None]` — VERIFIED byte-exact.
- L136-145 `run_tier2_ensemble` signature; L141 `adversarial_convergence_score`, L142 `adversarial_score_fn`, L143 `adversarial_unavailable` — VERIFIED.
- L221-232 seam invocation block; both branches assign ONLY a float — VERIFIED (L223 default scorer, L229 fn branch, L225/L231 `output_dir / ADVERSARIAL_SUBRUN_DIR`).
- L234-239 `build_reflect_contract` call passes only swarm path + score float + unavailable bool — VERIFIED.
- L244-249 `run_adversarial_scorer` returns `float | None`; L271 `return extract_convergence_score(parse_adversarial_contract(output_dir))` (the lossy step) — VERIFIED.
- L274-289 `parse_adversarial_contract` (returns full dict) — VERIFIED.
- L292-301 `build_adversarial_prompt` — VERIFIED; L299 literally emits `--suspect-source` (supports R2 inert-flag finding).
- L336-357 `extract_convergence_score` (unwraps `return_contract`, discards all other fields) — VERIFIED.
- L360-407 `build_reflect_contract` field-by-field — **EVERY line in R1's §4 table VERIFIED byte-exact**: status "success" L379, deviation_count_by_class all-zero L385-390, regression_present False L401, unauthorized_deviation_present False L402, needs_human_decision False L403, user_decision_required False L404, report_path via `_select_report_path` L383.
- L488-497 `_select_report_path` — VERIFIED exact (swarm path first, else first worker final_path, else None).
- `_parse_convergence_score` — grep over src/+tests/ returns **ZERO matches**; R1's explicit negative claim ("no such symbol exists; the brief was wrong") is CORRECT.

**contract.py (R3 scope)**
- L40 `_DEVIATION_KEYS = ("authorized", "necessary", "drift", "regression")` — VERIFIED.
- L47-57 `_LOAD_BEARING_BOOL_FIELDS` frozenset (7 members) — VERIFIED exact.
- L90-101 `_extract_deviations` (4-key int dict, coerces absent/malformed to 0) — VERIFIED.
- L307-328 `_halted_reason` slug routing — VERIFIED line-exact: status-failed 311, status-partial 313, regression `is True` 315, unauthorized 317, needs-human-decision 319, user-decision-required 321, deviations regression>0 324, drift>0 326. Strict `is True` identity checks confirmed.
- L65-82 `parse_contract` (returns dict or None; does not validate booleans) — VERIFIED.

**models.py (R3 §4)**
- L38-49 `Verdict.exit_code`: PASS→0, HALTED→10, DEGRADED→11, BLOCKED→2 — VERIFIED exact.

**sc-adversarial-protocol/SKILL.md (CRITICAL R2 verification)**
- grep for `deviation_count_by_class|regression_present|unauthorized_deviation_present|needs_human_decision` over the whole sc-adversarial-protocol/ dir → **ZERO HITS**. R2's decisive "SCORE-ONLY" claim is CONFIRMED: the Mode-A child does NOT emit any of the four reflect-deviation fields.
- L425 "## Return Contract (MANDATORY)"; the 10-field set (merged_output_path 433/451, convergence_score 434/452, artifacts_dir 435/453, status 436/454, base_variant 437/455, unresolved_conflicts 438/456, fallback_mode 439/457, failure_stage 440/458, invocation_method 441/459, unaddressed_invariants 442/460) — VERIFIED byte-exact against R2's §3 table.
- `--suspect-source` over skill + command/adversarial.md → ZERO hits. R2's "inert flag" finding CONFIRMED (emitted at ensemble.py:299 but not a defined/consumed flag).

**Spec `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` (R5 §3.1/§3.2)**
- L295-299 FR-RH2.7 description — VERIFIED verbatim. L303 derive_verdict/exit-code-map-unchanged bullet — VERIFIED verbatim. L304-305 companion bullets — VERIFIED.
- L166-175 §2.2 dataflow Phase (3)→(5), including "(contract.py, UNCHANGED)" and "(runner.py, UNCHANGED)" markers — VERIFIED verbatim.

**OI-1 table `oi1-mapping-table-validated.md` (R5 §3.3)**
- Rows 35/38/39/40 (deviation_count_by_class, regression_present, unauthorized_deviation_present, needs_human_decision) — all VERIFIED verbatim, including the SYNTHESIZED verdict and the "unless the adversarial/reflect domain supplies counts. No swarm equivalent." conditional clause that R5's load-bearing interpretation hinges on.

**QA report `qa-content-ensemble-formation-correctness-report.md` (R5 §3.4)**
- Line 39 CRITICAL #2 row — VERIFIED verbatim: severity CRITICAL, the hard-codes-clean Issue, and the Required Fix ("Change the adversarial seam to return/parse the adversarial contract or result object, not only a float… Add a test where the adversarial seam reports a regression/human-decision and verify `derive_verdict` does not PASS").
- Consolidated findings: line 56 "REJECTED — with rationale" header + lines 84-85 R6 rejection rationale — VERIFIED verbatim. R5's "load-bearing tension" framing (R6 rejected-in-scope vs CRITICAL #2 real-gap; new task changes the oracle) is faithfully grounded.

**Test files (R4 scope)**
- `_const_score` (test_ensemble_stub_integration.py:39-41), `_config` (78-85), `_run` (88-102) — VERIFIED exact.
- `adversarial_score_fn` usages at L93/331/356 + docstring L16 — VERIFIED (R1 §7 + R4 cite both).
- `build_reflect_contract(workers, adversarial_convergence_score=0.86)` at test_ensemble_unit.py:170 — VERIFIED exact.
- `tests/cli/reflect/fixtures/halted_regression.yaml` exists; `regression_present: true` (L11), `regression: 1` (L22) — VERIFIED (R4 §3).

### Minor observations (do NOT block)

- **R2 line-anchor drift (internal-to-R2, not fabrication):** R2 §3 header cites the producer schema at "§L425-460" and "field defs L449-460"; the actual table-row defs run L451-460 (L449 is a blank/header line). One-line off-by-one on the *header* citation; every individual field line (451-460) R2 lists resolves correctly. MINOR.
- **Cross-file note (consumer):** QA CRITICAL #2 (quoted in R5) uses the PRIOR task's line anchors for ensemble.py (`64-65, 194-205, 301-320, 384-390`) which were against an earlier revision; the CURRENT file's anchors are R1's (72, 221-232, 360-407). R5 quotes the QA row verbatim (correct — it is a verbatim citation of an external artifact) and R1/R3/R4 independently re-derive the current anchors. No conflict, no fabrication; the two anchor sets describe the same code at different revisions. Noted for builder awareness only.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | R1 ensemble.py anchors resolve (alias, signature, seam block, builder, parse chain) | PASS | All L67/72/136-145/221-232/234-239/244-271/274-289/292-301/336-357/360-407/488-497 verified by direct Read; file is 509 lines as claimed |
| 2 | R1 build_reflect_contract field-by-field table accuracy | PASS | Every HARD-CODED literal + line number in R1 §4 matches L377-407 byte-exact |
| 3 | R1 negative claim: `_parse_convergence_score` does not exist | PASS | grep src/+tests/ → ZERO matches; brief was wrong, R1 correctly flagged it |
| 4 | R2 CRITICAL "score-only" claim: child omits the 4 deviation fields | PASS | grep over sc-adversarial-protocol/ → ZERO HITS for all four fields |
| 5 | R2 10-field producer schema (SKILL.md L425+) | PASS | All 10 fields + line anchors (433-442 / 451-460) verified verbatim |
| 6 | R2 `--suspect-source` inert-flag finding | PASS | Not defined in skill/command (ZERO hits); emitted at ensemble.py:299; correctly tagged "Unverified impact" |
| 7 | R3 contract.py anchors (_LOAD_BEARING_BOOL_FIELDS, _halted_reason, _extract_deviations) | PASS | L40/47-57/90-101/307-328/65-82 all verified line-exact incl. `is True` identity checks |
| 8 | R3 models.py exit-code map | PASS | L38-49 PASS=0/HALTED=10/DEGRADED=11/BLOCKED=2 verified |
| 9 | R5 spec FR-RH2.7 verbatim quotes (L295-299, 303-305, 166-175) | PASS | All verbatim-accurate incl. UNCHANGED markers |
| 10 | R5 OI-1 rows 35/38/39/40 verbatim | PASS | All four rows + conditional clause verbatim-accurate |
| 11 | R5 QA CRITICAL #2 + consolidated R6 verbatim | PASS | Report line 39 + consolidated 56/84-85 verbatim-accurate |
| 12 | R4 test citations (_const_score, _run, _config, unit:170, fixture) | PASS | All verified exact; halted_regression.yaml fixture exists with claimed shape |
| 13 | No fabricated line numbers / unsupported assertions stated as fact | PASS | Every spot-checked anchor resolved; the one "brief said X" claim (R1) was correctly flagged as NON-existent, not asserted as real |
| 14 | All 5 files Status: Complete + Summary present | PASS | R1/R2/R3/R4/R5 each end with "Status: Complete" + Summary |

## Summary

- Checks passed: 14 / 14
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 02-adversarial-child-output-schema.md §3 header | Header cites producer field-defs at "L449-460"; actual rows are L451-460 (L449 is blank/header). One-line off-by-one on a *header* citation only; all per-field lines resolve. | Optional: change "L449-460" → "L451-460" in the §3 header. Non-blocking — does not affect any conclusion. |

(Note: the QA-CRITICAL-#2 anchors quoted in R5 reference an EARLIER ensemble.py revision. This is NOT an R5 defect — R5 quotes the external artifact verbatim, which is correct citation behavior. R1/R3/R4 independently supply the current-revision anchors. Documented above as a builder-awareness note, not an issue.)

## Confidence Gate

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 0 (via Bash) | Glob: 0 | Bash: 4 (greps + sed + wc). Total verification tool calls (11) >> 5 assigned files. No web research performed (all claims are local code/spec/artifact — Tavily not required this phase).
- The lens (evidence-quality) maps to the 14 checks above; each was verified by opening the cited source, not by trusting the research file.

## Recommendations

- Research evidence quality is exceptionally high. The decisive R2 "score-only" finding — the single most consequential claim for the builder (it changes R6 from a key-rename into a producer-extension/derivation task) — was independently confirmed by grep. Green light for synthesis/build from an evidence-quality standpoint.
- The lone MINOR (R2 §3 header off-by-one) is cosmetic; fix opportunistically or ignore.

---

## VERDICT: PASS

No CRITICAL or IMPORTANT issues. One MINOR (cosmetic header off-by-one in R2). Every spot-checked file:line anchor across ensemble.py, contract.py, models.py, sc-adversarial-protocol/SKILL.md, the spec, the OI-1 table, the QA report, and the test files resolved to exactly what the research claims. The CRITICAL R2 "score-only" claim and R1's `_parse_convergence_score`-does-not-exist negative claim both independently confirmed.

## QA Complete
