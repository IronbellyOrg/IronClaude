# Research Completeness Verification — Completeness Lens

**Topic:** FR-RH2 R6 adversarial seam (wire `ensemble.py` adversarial result → `build_reflect_contract`)
**Date:** 2026-06-21
**Files analyzed:** 5 (01-ensemble-seam-inventory, 02-adversarial-child-output-schema, 03-contract-consumer-constraints, 04-test-patterns, 05-template-and-citations)
**Lens:** Completeness (BREADTH — does every area needed to BUILD the task have research coverage?)
**Analyst stance:** Adversarial — find missing coverage, not confirm sufficiency.

---

## Scope note

This is a single-instance analysis (no `assigned_files` partition; all 5 in-scope files read in full). Cross-file checks applied across the full set.

The 8 lens criteria from the spawn prompt are evaluated below, each PASS (with evidence) or FAIL (with specific gaps). A summary verdict and gap list close the report.

---

## Criterion 1 — Seam type + `build_reflect_contract` surface identified with line anchors?

**PASS.**

- The seam alias `AdversarialScoreFn = Callable[[list[str], Path], float | None]` is pinned at `ensemble.py:72` (R1 §1; corroborated R4 §7 index, R2 §1).
- The default scorer `run_adversarial_scorer` (same narrow `float | None` shape, must widen in lockstep) at `ensemble.py:244-249` / `:271` (R1 §3, R2 §1).
- The seam invocation block (both branches assign only a float) at `ensemble.py:221-232` (R1 §2, R4 §3).
- `build_reflect_contract` signature at `ensemble.py:360-366`; forwarding call site at `ensemble.py:234-239` (R1 §2/§4).
- R1 §4 gives a complete field-by-field table of the returned dict (`ensemble.py:377-407`) marking HARD-CODED vs COMPUTED with per-field line anchors — exactly what per-item construction needs.

Multiple files independently cite the same anchors — strong cross-corroboration, no contradiction.

---

## Criterion 2 — Adversarial child's actual emission schema established (mapping feasible, not fabricated)?

**PASS (with a load-bearing caveat that is itself well-documented).**

- R2 §3 establishes the authoritative producer schema: `sc-adversarial-protocol/SKILL.md:431-443` (field defs `:449-460`) — the complete 10-field set the Mode-A child emits.
- R2 §4 provides DECISIVE negative evidence (grep over the adversarial skill = ZERO hits) that the five reflect-deviation target fields are NOT emitted by the child — they live only in reflect's own protocol.
- This is the single most important feasibility discovery: a pure key-rename is NOT possible. R2 §7 enumerates three feasible derivation options. See Criterion 7.

Caveat (documented, not a gap): R2 §1 flags that `build_adversarial_prompt` emits a `--suspect-source` flag the `/sc:adversarial` command does NOT define (`adversarial.md:39-70`) — marked "Unverified impact," inert. Correctly surfaced as a side-finding, not silently assumed.

---

## Criterion 3 — `contract.py` mapping target + FR-RH2.7 constraint documented?

**PASS — strongest-covered criterion.**

- R3 §1 traces the full `derive_verdict` first-match-wins ladder (`contract.py:130-246`): blocked→degraded→halted→pass, with Stage-3 HALTED (`_halted_reason`, `contract.py:307-328`) identified as where findings land.
- R3 §6 provides the explicit mapping-target table: contract key → required type → exact value that makes `derive_verdict` NON-pass → line → adversarial source. Per-item-construction-ready.
- R3 §2 documents `_extract_deviations` shape (`contract.py:90-101`, 4-key int dict).
- R3 §3 documents the `_LOAD_BEARING_BOOL_FIELDS` type-trap (`contract.py:47-57`, `:200-209`): a present non-bool routes BLOCKED/`malformed-contract-boolean` — mapping MUST emit genuine Python `bool`. Non-obvious failure mode, well-flagged (also R4 §3).
- R3 §5 quotes FR-RH2.7 verbatim (`spec.md:295-305`) + three "UNCHANGED" markers (`spec.md:171/368/647`): `derive_verdict` + `Verdict.exit_code` (`models.py:38-49`) FROZEN; fix is ensemble-side ONLY.

---

## Criterion 4 — Test pattern + exact assertion target for the regression test documented?

**PASS — thorough.**

- R4 §1 identifies the test home: `tests/cli/reflect/test_ensemble_stub_integration.py` (I1-I11 family), new test = I12 modeled on the I4 DEGRADED negative-witness.
- R4 §1b quotes the shared `_run` driver (`:88-102`) and `_config` (`:78-85`, `depth="deep"` required so `expected_tier` resolves to 2) — the exact reuse pattern.
- R4 §2 documents stub setup (`_distinct_stub`, `stub_model_id`, `reviewers=3` for a healthy diversity-full survivor ensemble so no degrade masks the regression) and required fixtures (`temp_tasklist`, `patch_git`, conftest.py:46-80).
- R4 §5 provides a concrete (prose-not-final) I12 sketch with the exact assertion target: `result.verdict is not Verdict.PASS` (load-bearing single line), sharpened to `is Verdict.HALTED` / `exit_code == 10` / `reason == "regression"`, plus a provenance assert `contract["regression_present"] is True`.
- R4 §3 explains the red-then-green nature: against current code the test sees `Verdict.PASS` (proves the gap), goes green after the seam widens.
- R4 §4 documents the NFR-7 no-nesting guard constraints (`test_no_nesting_guard.py`): keep `ClaudeProcess` present; no `Task(`, `subagent`, `anthropic`, raw subprocess, async in `ensemble.py`. Critical for the executor to not trip a guard.
- R4 §6 gives the verified pytest invocation (`uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -q`, 12 passed ~0.24s) and the reference fixture `fixtures/halted_regression.yaml` for target contract shape.

---

## Criterion 5 — MDTM template-02 rules + verbatim OI-1 / QA-CRITICAL#2 citation anchors present?

**PASS — comprehensive.**

- R5 §1 extracts the full template-02 ruleset: B2 6-element self-contained items (`template:159-214`), A3 granular breakdown (`:108-112`), D3 no-items-before-Phase-1 (`:286-289`), M3 lens-QA 8-step sequence (`:1059-1096`), I18 mandatory L3 test item for code-modifying tasks (`:688-697`), I17 post-completion validation (`:675-686`), I19/I22 agent-count floors (`:699-741`, `:793-840`).
- R5 §2 captures the frontmatter shape + the two prior-task convention fields (`start_commit`, `executor_model_class`) and the VERBATIM penultimate POST-reflect-wrapper item (prior task line 483) with the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker.
- R5 §3.3 quotes the four OI-1 SYNTHESIZED rows VERBATIM with line anchors (`oi1-mapping-table-validated.md:35,38,39,40`) including the "unless the adversarial/reflect domain supplies counts. No swarm equivalent." conditional clause.
- R5 §3.4 quotes QA CRITICAL #2 VERBATIM (`qa-content-ensemble-formation-correctness-report.md:39`) including the recommended fix (map adversarial result into contract + add a regression test where `derive_verdict` does not PASS).
- R5 §3.5 surfaces the cross-task tension (R6 was REJECTED-with-rationale in the prior task's consolidated findings `:84-85` as correct-within-FR-RH2-scope) and correctly frames the new task as a deliberate scope-expansion follow-up, not re-litigation. This is exactly the nuance the builder needs to cite both anchors.

---

## Criterion 6 — Granularity sufficient for per-item checklist construction (widen-seam, derive/parse, map-fields, report_path, test, verify)?

**PASS.** Each of the six build sub-areas has line-anchored coverage:

| Build sub-area | Coverage | Anchor source |
|---|---|---|
| widen-seam | `AdversarialScoreFn` `ensemble.py:72` + lockstep `run_adversarial_scorer:244-271`; backward-compat surface enumerated | R1 §1/§3/§8 |
| derive/parse | `parse_adversarial_contract:274-289` already returns full dict; `extract_convergence_score:336-357` is the lossy step | R1 §3a/§3b, R2 §2 |
| map-fields | mapping-target table (key→type→non-pass value→source); type-trap (genuine bool) | R3 §6, R3 §3 |
| report_path | `_select_report_path:488-497` (swarm-only today); R5 §3.5 notes R5/R6 alignment to adversarial report | R1 §5, R2 §5, R5 §3.5 |
| test | I12 sketch + `_run`/`_config`/`_distinct_stub` reuse + assertion target + NFR-7 constraints | R4 §1-§6 |
| verify | pytest invocation + clean-path PASS guard (NFR-RH2.6) + halted_regression.yaml shape | R4 §6, R3 §7 |

The R3 §7 "Notes for the test author" and R1 §8 "backward-compat surface" explicitly enumerate every call site that changes — sufficient granularity for atomic per-file items.

---

## Criterion 7 — Score-only-vs-richer-fields discovery resolved with evidence (gates the whole task design)?

**PASS — this is the keystone finding and it is decisively resolved.**

- R2 reaches an explicit **"Decisive finding: SCORE-ONLY"** verdict (§ summary, L151-162) backed by grep negative evidence (R2 §4) and the producer schema (R2 §3).
- The consequence is correctly propagated: the task CANNOT be a pure ensemble-side key-rename. R2 §7 + summary enumerate the feasible paths: (a) derive a coarse regression signal from `convergence_score` vs threshold (immediately feasible from existing emission), and/or (b) EXTEND the producer's emission to write the reflect deviation taxonomy.
- R1 §3a independently corroborates that `parse_adversarial_contract` already returns the FULL dict (the data is available where it exists; it is `extract_convergence_score` that discards it).
- R5 §3.5 ties this to the OI-1 conditional clause and the cross-task tension — the task's PURPOSE is to flip the OI-1 "SYNTHESIZED unless the adversarial domain supplies counts" conditional.

This discovery is the gate for the entire task design and all five files are internally consistent about it. No contradiction across files.

---

## Criterion 8 — Unresolved ambiguities documented, not silently assumed?

**PASS.** Open ambiguities are surfaced rather than assumed:

1. **`_parse_convergence_score` does not exist** — the user brief named a helper that has no matching symbol; R1 §3 NOTE + §summary corrects this (real helpers: `parse_adversarial_contract:274`, `extract_convergence_score:336`). Verified via grep. (A genuine brief error caught, not papered over.)
2. **`--suspect-source` flag mismatch** — R2 §1 flags it as inert / "Unverified impact."
3. **Which derivation path (a vs b)** — R2 §7 explicitly marks options as "for downstream design — NOT decided here," correctly deferring the design decision to the builder rather than pre-committing.
4. **Widened seam return shape** (dataclass vs dict) — R4 §5 explicitly says "depends on R2's widened contract — coordinate with R2's design," shown as two candidate shapes rather than assumed.
5. **`report_path` for faithful adversarial run** — R5 §3.5 (R5 rejected row) notes the tension that for a faithful run `report_path` should be the adversarial report, "keep merged.md only as a subrun artifact"; flagged for alignment.

---

## Cross-file consistency check

No contradictions found across the five files. Shared anchors agree:
- `AdversarialScoreFn @ ensemble.py:72` — R1, R2, R4 agree.
- `build_reflect_contract` hard-codes the five fields — R1 §4, R2 §6, R3 §0, R4 §3 all agree (line refs `377-407`, esp. `385-390`, `401-404`).
- `derive_verdict` frozen by FR-RH2.7, fix ensemble-side only — R3 §5, R5 §3.1 agree.
- SCORE-ONLY child emission — R2 decisive, R1 §3a corroborates the discard point.

Minor anchor-range variance (e.g., QA CRITICAL #2 cites `ensemble.py:301-320, 384-390` for the hard-coded block in the prior-task numbering while R1/R3/R4 cite `377-407`/`385-390` in the current tree) is explained: QA CRITICAL #2 is a VERBATIM quote from the prior task's report against an earlier file state; R5 §3.4 quotes it verbatim by design. The current-tree anchors (R1/R3/R4) are the authoritative build targets. This is a provenance difference, not a contradiction, and R5 handles it correctly by quoting the source verbatim.

---

## Depth / breadth assessment

Expected: BREADTH coverage of all six build sub-areas + the gating score-only discovery. Achieved: every criterion PASS with line-anchored evidence and cross-corroboration. The research notably exceeds breadth into actionable depth (mapping-target table, I12 test sketch, backward-compat call-site enumeration, type-trap warnings) without fabrication — claims are consistently file:line cited.

---

## VERDICT: PASS

All 8 completeness-lens criteria PASS. Every area needed to BUILD the FR-RH2 R6 task has line-anchored research coverage, the keystone score-only-vs-richer-fields discovery is decisively resolved with evidence, and unresolved design ambiguities are explicitly surfaced (not silently assumed) for the builder to decide. No cross-file contradictions.

### Gap list

No blocking gaps. Two non-blocking observations for the builder's awareness (already documented in the research, surfaced here for traceability — NOT failures):

- **N1 (Minor / informational):** The widened-seam return shape (dataclass vs dict) and the derivation path (derive-from-convergence vs extend-producer-emission) are deliberately left open by R2/R4 as design decisions. The builder must make these calls; the research correctly does not pre-decide them. This is correct scoping, not a research gap — noted so the builder expects to resolve it.
- **N2 (Minor / informational):** Anchor-range provenance: QA CRITICAL #2 line numbers (`ensemble.py:301-320`) reflect the prior task's file state; the current-tree authoritative anchors are R1/R3/R4's (`ensemble.py:377-407`). The builder should target the current-tree anchors for edits and use the verbatim QA quote only as citation/justification.

---
