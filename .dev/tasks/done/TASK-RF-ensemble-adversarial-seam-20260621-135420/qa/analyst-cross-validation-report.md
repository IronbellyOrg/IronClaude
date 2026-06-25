# Cross-Validation Report — FR-RH2 R6 Adversarial Seam

**Analysis type:** completeness-verification
**Lens:** cross-validation (inter-file agreement)
**Date:** 2026-06-21
**Track goal:** Wire the adversarial seam in ensemble.py to map real deviation/regression/human-decision/report_path into build_reflect_contract; add regression test asserting derive_verdict != PASS.

**Files cross-validated:**
- 01-ensemble-seam-inventory.md (R1)
- 02-adversarial-child-output-schema.md (R2)
- 03-contract-consumer-constraints.md (R3)
- 04-test-patterns.md (R4)
- 05-template-and-citations.md (R5)

---

## Cross-Validation Focus Areas

### Focus 1 — Line anchors for `build_reflect_contract`, the seam type, and the hard-coded fields (R1 / R3 / R4 consistency)

**Verdict: CONSISTENT (with one harmless line-anchor span variance, see note).**

| Fact | R1 | R3 | R4 | Agreement |
|---|---|---|---|---|
| `build_reflect_contract` location | `ensemble.py:360-407` (sig 360-366) | `ensemble.py:360-407` | `ensemble.py:377-407` (return-dict span) | AGREE — R4's `377-407` is the *returned dict* span, R1/R3's `360-407` is the *whole function* span. Same function; not a contradiction. |
| Seam type `AdversarialScoreFn` | `Callable[[list[str], Path], float \| None]` at **L72** | (not re-cited; defers to R1) | `Callable[[list[str], Path], float \| None]` at **L72** | AGREE exactly (R1 & R4 both L72, identical signature). |
| `deviation_count_by_class` hard-coded all-zero | L385-390 | L385-390 | L385-390 (esp. 385-390) | AGREE exactly. |
| `regression_present: False` | L401 | L401 | L401 | AGREE exactly. |
| `unauthorized_deviation_present: False` | L402 | L402 | (cites 401-404 block) | AGREE. |
| `needs_human_decision: False` | L403 | L403 | (cites 401-404 block) | AGREE. |
| `user_decision_required: False` | L404 | L404 | (cites 401-404 block) | AGREE. |
| `status: "success"` hard-coded | L379 | L379 | (noted, no line) | AGREE. |

No contradiction. The only surface variance is R4 citing `377-407` (return-dict span) where R1/R3 cite `360-407` (full function incl. signature + early-return). Both describe the same `build_reflect_contract`; the field-level line anchors (385-390, 401-404, 379) are **byte-identical across all three files**.

---

### Focus 2 — The adversarial helper names: R1's correction vs R2's corroboration

**Verdict: CONSISTENT — R2 fully corroborates R1's correction. No residual conflict.**

- R1 (L117-121) explicitly states the brief's named helper `_parse_convergence_score` **does not exist**, and names the real helpers `parse_adversarial_contract` (**L274**) and `extract_convergence_score` (**L336**), verified by full-file read + grep returning zero matches for `_parse_convergence_score`.
- R2 independently names the same two helpers with the same anchors: `parse_adversarial_contract(output_dir)` at **`ensemble.py:274-289`** (R2 §2) and `extract_convergence_score(contract)` at **`ensemble.py:336-357`** (R2 §2). R2 never references `_parse_convergence_score` at all.
- Both agree on the parse chain: `extract_convergence_score(parse_adversarial_contract(output_dir))` returned at **L271** (R1 §3 / R2 §1).
- Both agree on the contract-file search order: `<dir>/adversarial/return-contract.yaml` then `<dir>/return-contract.yaml` (R1 §3a L282-285 ≈ R2 §2 L283-284).

The two researchers reached the corrected naming independently and agree on every anchor. The brief's `_parse_convergence_score` is confirmed a non-existent symbol by both.

---

### Focus 3 — Decisive "score-only" finding (R2) vs R1's "full dict already parsed at 274"

**Verdict: CONSISTENT — these are two halves of the same fact, not a contradiction.**

The apparent tension dissolves on close reading:

- **R1's claim** is about the *parse layer inside ensemble.py*: `parse_adversarial_contract` (L274) returns the FULL parsed contract dict, but `extract_convergence_score` (L336) then **discards every field except the score** (R1 §3b L131-136). R1's "full dict already parsed at 274" is strictly about what the ensemble-side parser *receives* — it is available but thrown away at L271/L336.
- **R2's claim** is about the *producer* (the `/sc:adversarial` Mode-A child): the child's `return-contract.yaml` **never emits** `deviation_count_by_class` / `regression_present` / `unauthorized_deviation_present` / `needs_human_decision` in the first place (R2 §3/§4 — grep over the adversarial skill returns ZERO hits; the child's full field set is `merged_output_path`, `convergence_score`, `artifacts_dir`, `status`, `base_variant`, `unresolved_conflicts`, `fallback_mode`, `failure_stage`, `invocation_method`, `unaddressed_invariants`, SKILL.md:431-443).

**Reconciliation:** the "full dict" R1 says is parsed at L274 is the *adversarial child's* contract — which (per R2) contains a convergence score + merge metadata but NOT the reflect deviation taxonomy. So both are true simultaneously:
1. The ensemble parser HAS the whole child dict available (R1) — but
2. That whole child dict is itself score-only w.r.t. the five target fields (R2).

This is an important compounding finding, not a contradiction: **even if R6 stops discarding fields at `extract_convergence_score`, the discarded fields do not contain the deviation taxonomy** — because the producer never wrote them. R2 makes this explicit (§7: R6 "CANNOT be a pure key-rename"). R1 is slightly narrower (it frames the gap as "fields thrown away downstream", R1 §3/§3b) and does NOT independently assert the producer emits them — so R1 does not contradict R2; it simply scopes its claim to the ensemble parse layer. **R3 (§0, §6) and R4 (TL;DR, §3) both side with R2's framing** (the seam carries "NO deviation/regression signal" / fields are "hard-coded clean" with "no path" for a real finding), reinforcing that the fix is NOT a key-rename. R5 §3.5 captures the same as the "load-bearing tension."

**Cross-file caution flag (MINOR, for the builder, not a contradiction):** R1's phrasing ("FR-RH2.7 should map the remaining fields from that already-parsed dict", R1 §3 L114-115, and summary L299-302) *could be read* as implying the deviation fields are recoverable by un-discarding them at L271. R2/R3/R4 establish that is false for four of the five fields (only `convergence_score` and the merged report path are actually present in the child output). The builder must not implement R6 as "stop discarding at extract_convergence_score" alone — that recovers only the score. See Gap G1.

---

### Focus 4 — Mapping target + load-bearing-bool type trap (R3) vs test assertion design (R4)

**Verdict: CONSISTENT — R3 and R4 agree precisely on the regression → HALTED/exit10/reason=regression chain and the bool type trap.**

| Fact | R3 | R4 | Agreement |
|---|---|---|---|
| `regression_present: True` (genuine bool) → HALTED | contract.py:315, reason `regression` (R3 §1 Stage 3, §6 table) | contract.py:315-316 → `"regression"` (R4 §3) | AGREE |
| `deviation_count_by_class.regression >= 1` → HALTED | contract.py:324 (R3 §1, §6) | contract.py:323-324 (R4 §3) | AGREE |
| Either signal alone trips Stage-3 | "Either alone trips Stage-3 HALTED" (R3 §6 L205-206) | "Either path yields the `regression` slug" (R4 §3 L191-193) | AGREE |
| Exit code 10 for HALTED | models.py:38-49, halted→10 (R3 §4) | models.py:39-48, HALTED=10 (R4 §3 L198-199) | AGREE |
| Load-bearing bool trap | `_LOAD_BEARING_BOOL_FIELDS` contract.py:47-57; present non-bool → BLOCKED `malformed-contract-boolean` contract.py:200-209; must emit genuine `bool` not `"true"`/`1` (R3 §3, §6 type-trap L210-213) | same: contract.py:47-57 / 200-209; "the seam MUST set an actual `True`, not `"true"`/`1`" (R4 §3 L182-185) | AGREE exactly |
| Assertion design | `derive_verdict(...).verdict is Verdict.HALTED`, `reason == "regression"`, child_rc=0, expected_tier=2, tier_reached=2 (R3 §6, §7) | `result.verdict is Verdict.HALTED`, `exit_code == 10`, `reason == "regression"`; child_rc=0, expected_tier=2 (R4 §5) | AGREE |
| Clean-path must still PASS | clean builder output → all-zero counts + `regression_present=False` still PASSes (R3 §7 L227-229) | NFR-7 / healthy-ensemble guard; clean path green (R4 §2b, §6) | AGREE |

R4's test sketch (I12) is the operational realization of R3's consumer-side mapping table — they were written to the same target and match on every load-bearing value, including the strict-identity `is True` checks (R3 §1 note L77-80 ≈ R4 §3 L182-185). **No contradiction.**

One reinforcing detail: R4 (§3) adds that the regression must be the *first non-degraded trigger* (keep `convergence_score` non-None so `null-convergence` DEGRADED at contract.py:283-285 doesn't mask it). R3 (§6 table, `adversarial_convergence_score` row) independently notes the same `null-convergence` DEGRADED trigger at contract.py:284. Consistent and complementary.

---

### Focus 5 — FR-RH2.7 "derive_verdict unchanged" as a hard constraint (R3 / R5 consistency)

**Verdict: CONSISTENT — both treat FR-RH2.7 as a hard, non-negotiable backward-compat constraint, citing the same spec anchors.**

- **R3** (§5) quotes FR-RH2.7 from `spec.md:295-305`: `derive_verdict` and the `Verdict` exit-code map (`pass→0, halted→10, degraded→11, blocked→2`) are unchanged; existing reflect contract/verdict tests pass without modification. R3 §5 concludes "the fix is ensemble-side mapping ONLY" and lists the frozen surface (`derive_verdict`, `_halted_reason`, `_degraded_reason`, `_extract_deviations`, `_LOAD_BEARING_BOOL_FIELDS`, `_make_result`, `parse_contract`, `Verdict.exit_code`). Corroborating UNCHANGED markers cited: spec.md:171, 368, 647.
- **R5** (§3.1) quotes the same FR-RH2.7 bullet from `spec.md:303` verbatim ("`derive_verdict` and the `Verdict` exit-code map … are unchanged") plus the full description spec.md:295-299 and companion bullets spec.md:304-305. R5 §4 / §3.5 frames it as "the hard backward-compat constraint on the R6 fix" — no contract field rename/retype, `derive_verdict` + exit-code map byte-unchanged.

Both researchers cite **the same spec lines** (R3: spec.md:295-305; R5: spec.md:303 + 295-299 + 304-305) and reach the **same conclusion** (ensemble-side mapping only; `derive_verdict` frozen). The exit-code map quad (`pass→0, halted→10, degraded→11, blocked→2`) is stated identically by both (R3 §4/§5; R5 §3.1/§2.2 §5.3 spec.md:437-442). **No contradiction.**

---

### Focus 6 — Exit-code map location: R3 (`models.py:38-49`, not contract.py) vs R4

**Verdict: CONSISTENT — both place the exit-code map on `Verdict.exit_code` in `models.py`, NOT in contract.py.**

- **R3** (§4) is explicit: "Lives on the `Verdict` enum, NOT in contract.py: `Verdict.exit_code` property at `src/superclaude/cli/reflect/models.py:38-49`" → PASS→0, HALTED→10, DEGRADED→11, BLOCKED→2 (module docstring restates at models.py:14-17).
- **R4** (§3 L198-199, §7 index) cites the same map at `models.py:39-48`: "Verdict exit codes (`models.py:39-48`): PASS=0, HALTED=10, DEGRADED=11, BLOCKED=2."

Both agree on (a) the file — `models.py`, not contract.py; (b) the enum — `Verdict.exit_code`; (c) the four values. The only variance is the line span (**R3: 38-49** vs **R4: 39-48**) — a one-line difference at each end (R3 likely includes the property decorator/def line and a trailing line; R4 cites the body rows). This is a **trivial span variance, not a contradiction**: both point at the same `Verdict.exit_code` property with identical semantics. R5 (§3.2, spec.md:437-442 `verdict_map_unchanged: {pass:0, halted:10, degraded:11, blocked:2}`) corroborates the same quad from the spec side.

---

## Inter-File Contradiction Summary

**Zero hard contradictions found across the five files.** Every overlap on a load-bearing fact agrees. The four observed variances are all benign:

1. `build_reflect_contract` span: R4 `377-407` (return dict) vs R1/R3 `360-407` (full function) — same function, complementary spans.
2. Exit-code map span: R3 `models.py:38-49` vs R4 `models.py:39-48` — same `Verdict.exit_code` property, ±1 line at each end.
3. R1's "map the remaining fields from the already-parsed dict" framing is narrower than R2/R3/R4's "the producer never emits them" — not contradictory, but the builder must heed R2/R3/R4 (see Gap G1).
4. Focus-3 "score-only" (R2) vs "full dict parsed" (R1) — two compatible halves of one fact (the parsed child dict is itself score-only w.r.t. the five fields).

## Cross-File Convergent Findings (all 5 agree where they overlap)

- The seam alias to widen is `AdversarialScoreFn` at `ensemble.py:72` (R1, R4) and its sibling default scorer `run_adversarial_scorer` (R1 L244, R2 §1) returns the same narrow `float | None`.
- `build_reflect_contract` hard-codes the five target fields clean (R1, R2, R3, R4 — identical anchors 385-390, 401-404) plus `status:"success"` L379 (R1, R3).
- The fix is **ensemble-side mapping ONLY**; `derive_verdict` + exit-code map are frozen by FR-RH2.7 (R3, R5; R2/R4 consistent).
- Minimal correct fix: set `regression_present=True` (genuine bool) and/or `deviation_count_by_class.regression >= 1` (int) → HALTED/exit10/reason=regression (R3, R4).
- The bool type-trap (must emit genuine Python `bool`, never `"true"`/`1`, or self-BLOCK at contract.py:200-209) is independently flagged by R3 and R4.
- The test belongs in `test_ensemble_stub_integration.py` as a new I12 mirroring the I4 negative witness; it is a RED test against today's code (R4), consistent with R3's test-author notes (§7).

## Gaps Identified (cross-validation lens)

### Important Gaps (affect implementation correctness)

- **G1 — The "un-discard the parsed dict" trap.** R1's framing ("map the remaining fields from that already-parsed dict", §3/summary) is correct only for the convergence score and merged report path. R2/R3/R4 establish the four deviation/regression/human-decision fields are **not present in the adversarial child output at all** (R2 §4, grep ZERO hits). If the builder reads only R1, they may implement R6 as "stop discarding fields at `extract_convergence_score`," which recovers nothing for four of five fields. **The task file MUST encode R2's "not a pure key-rename" conclusion** (derive a coarse `regression_present` from convergence-vs-threshold, AND/OR extend the producer's emission) so the executor doesn't build a no-op mapping. R5 §3.5 already captures this as the load-bearing tension — ensure it survives into the task items.

### Minor Gaps (non-blocking, builder awareness)

- **G2 — `report_path` source divergence across tasks.** R1/R2 report `report_path` is currently the swarm `merged_path` via `_select_report_path` (ensemble.py:375/383/488). R5 §3.5 (R5-rejected-row context) notes QA CRITICAL #2's fix says a *faithful adversarial run* should point `report_path` at the adversarial report, "keep merged.md only as a subrun artifact." This is a known, surfaced design choice (not a contradiction), but the five research files do not converge on whether R6 must change `_select_report_path` — R1 §5 lists it as a *possible* threading point, R5 marks it a follow-up alignment. Builder should make this an explicit decision in the task, not leave it implicit.
- **G3 — Inert `--suspect-source` flag (R2 §1, Unverified impact).** R2 flags that `build_adversarial_prompt` emits `--suspect-source`, which `/sc:adversarial` does not define (grep ZERO hits). No other researcher cross-checks this. It does not block R6 (the flag is inert, the debate still runs), but it is an isolated single-source claim worth noting; it is out of scope for the regression-test track but the builder may want a side-note.

## Coverage Note

All five assigned files were read in full. All six requested cross-validation focus areas were evaluated against every file that touches the relevant fact. No file was skipped or skimmed. Citations in this report reproduce the line anchors AS STATED in the research files (this is an inter-file *agreement* audit, not a fresh re-derivation from source — the analyst did not independently re-Read `ensemble.py`/`contract.py`/`models.py`; consistency is judged on whether the five researchers agree with each other, per the lens focus). Where two files cite slightly different line spans for the same symbol, both are reported and reconciled above.

---

## VERDICT: PASS

The five research files are **mutually consistent** on every load-bearing fact across all six cross-validation focus areas. Zero hard contradictions. The four variances are benign (line-span overlaps + one framing-narrowness that is captured as Gap G1). The corroboration is strong: R1's `_parse_convergence_score`→real-helpers correction is independently confirmed by R2; the regression→HALTED/exit10 chain + bool type-trap match exactly between R3 and R4; FR-RH2.7-frozen is cited from the same spec lines by R3 and R5; the exit-code-map location agrees between R3, R4, and R5.

**Gaps are advisory, not blocking** — they flag implementation pitfalls (G1 the no-op-mapping trap; G2 report_path decision; G3 inert flag) for the task builder to encode, but none represents a research contradiction or a coverage hole. Cross-validation passes.
