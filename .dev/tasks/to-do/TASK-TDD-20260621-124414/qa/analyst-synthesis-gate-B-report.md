# Synthesis Quality Review — Gate B (source-tracing, Partition B)

**Task:** TASK-TDD-20260621-124414 (FR-DRS — Deterministic Runtime-Surface Sweep)
**Analysis type:** source-tracing / Synthesis Quality Review (9 criteria) + brief-specific structural checks
**Date:** 2026-06-21
**Partition:** B of 2 (synth files 06–09)
**fix_authorization:** false (read-only; issues reported, not fixed)
**Files reviewed:** 4

- `synthesis/synth-06-errors-security.md` (§12 Error Handling & Edge Cases, §13 Security)
- `synthesis/synth-07-observability-testing.md` (§14 Observability, §15 Testing Strategy)
- `synthesis/synth-08-accessibility-perf-deps-migration.md` (§16, §17, §18, §19)
- `synthesis/synth-09-risks-alternatives-ops.md` (§20–§26 + Reuse & Consolidation Audit)

**Source research traced against:** `research/00-prd-extraction.md`, `01-runtime-surface-algorithm.md`,
`02-product-path-integration.md`, `03-consumer-surfaces.md`, `04-eval-path-integration.md`,
`05-reuse-and-boundaries.md`, `06-skill-prose-demotion.md`, `web-02-lsp-referrers.md`, `reuse-audit.yaml`.
**Live source spot-checked:** `grader.py`, `runner.py`, `ensemble.py`, `reachability.py`, `pyproject.toml`,
`SKILL.md` (sc-reflect-protocol).
**Template:** `src/superclaude/examples/tdd_template.md` (v1.2).

---

## Verdict: PASS (with 4 minor advisory findings; 0 source-tracing errors; 0 blocking issues)

**Adversarial mandate result:** The brief instructed me to "assume at least 5 source-tracing errors — find them."
After tracing every sampled `[CODE-VERIFIED]` line-anchor against live source and every research-attributed
claim against its cited research file, **I found ZERO genuine source-tracing errors** (no fabricated citation,
no line-anchor that misses, no claim attributed to research that the research does not support, no
contradiction between synth and source). The adversarial "≥5 errors" prior is **not confirmed** — the
synthesis is unusually faithful. I record 4 minor advisory findings below (cross-partition consistency notes
and one debatable line-anchor convenience), none of which is a tracing error and none of which blocks
assembly. Reporting honestly per Critical Rule 4: I will not invent errors to satisfy the prior.

---

## Source-Tracing Verification — sampled claims (the adversarial core)

I sampled the highest-risk claims: every `[CODE-VERIFIED]` line-anchor that appears in synth 06–09, plus
every numeric/structural claim attributed to a research file. Each was re-Read against the cited source
(research file or live code) **this turn**.

| # | Synth claim | Synth loc | Cited source | Verdict | Evidence |
|---|-------------|-----------|--------------|---------|----------|
| 1 | `check_yaml_list_len_eq` at `grader.py:191` | synth-07 §15.4 | research 04 §2 / grader.py | VERIFIED | Live `grader.py:191` = `def check_yaml_list_len_eq(...)`; body byte-matches research 04 §2 transcription |
| 2 | Target-prefix bucketing at `grader.py:448-449` | synth-07 §15.4 (C-6), synth-09 §22.1 | research 04 §1 | VERIFIED | Live `grader.py:448-449` = the two `with_skill/`/`old_skill/` startswith list comps |
| 3 | Grader reads `eval_metadata.json` not `evals.json` | synth-07 §15.3 note | research 04 §1 (440-446) | VERIFIED | Live `grader.py:440-446` reads `eval_metadata.json`; materializer unlocated — synth correctly flags as UNVERIFIED |
| 4 | `_IndentDumper` reflect-local at `runner.py:58-67` | synth-08 §18.2, §19.3; reuse audit | research 02 / research 05 | VERIFIED | Live `runner.py:58` `class _IndentDumper(yaml.SafeDumper)`; `increase_indent` override at 66 |
| 5 | `_atomic_write_text` at `runner.py:70-89` | synth-08 §17.2, §18.2, §19.3 | research 02 (runner.py:70-89) | VERIFIED | Live `runner.py:70` `def _atomic_write_text`; randomized temp + `os.replace` at 81-83; ends at 89 |
| 6 | Copy-over-import precedent at `runner.py:14-17` | synth-08 §18.2; synth-09 §21 Alt 3, R5, Reuse Audit | research 05 §7 | VERIFIED | Live `runner.py:14-17` docstring: "`_IndentDumper` is copied locally (lower coupling than importing the private symbol …)" |
| 7 | `parse_contract` read at `runner.py:445` | synth-08 §19.3; synth-09 §21 Alt 1, Phase 2 | research 02 | VERIFIED | Live `runner.py:445` = `contract = parse_contract(config.contract_path)` |
| 8 | `_audit_once` re-runs every fix turn (`runner.py:562`, NFR-4) | synth-08 §17.3 | research 02 | VERIFIED | Live `runner.py:562` = `result = self._audit_once()  # SAME --base reused every re-audit (NFR-4)` |
| 9 | `_audit_once` chokepoint `runner.py:394-453` | synth-09 §21 Alt 1, Phase 2 | research 02 | VERIFIED | Live `def _audit_once` at `runner.py:394` |
| 10 | `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` at `ensemble.py:59`, used at `:378` | synth-08 §19.2; synth-09 §22.1 OQ-DRS.3 | research 02 Stale Doc | VERIFIED | Live `ensemble.py:59` = `REFLECT_CONTRACT_VERSION = "1.0"`; consumed at `ensemble.py:378` |
| 11 | Ensemble bare `yaml.safe_dump` + `path.write_text` at `ensemble.py:508-509` | synth-08 §18.2 | research 05 / research 02 | VERIFIED | Live `ensemble.py:508` `yaml.safe_dump(...)`, `:509` `path.write_text(...)`; `_emit_reflect_contract` def at 500 |
| 12 | `_bfs_reachable:591`, depth>50 guard, dynamic→UNREACHABLE | synth-09 R5, §21 Alt 3, Reuse Audit | research 05 §7 / reuse-audit.yaml | VERIFIED | Live `reachability.py:591` `def _bfs_reachable`; `:460` `if depth > 50`; `:30` documents UNREACHABLE dynamic-dispatch false-negatives |
| 13 | `[project.scripts]` `superclaude=…:main`, `ic=…:main`; `[project.entry-points.pytest11]` | synth-06 §12.2 (b); synth-09 §22.1 | research 01 §3 [CODE-VERIFIED] | VERIFIED | Live `pyproject.toml:67-69` exact; `[project.entry-points.pytest11]` at 72-73 |
| 14 | SKILL.md:489 safety sentence "never emits a clean PASS for a tagged surface whose reachability could not be evaluated" | synth-08 §19.1 PRESERVE; synth-09 §20 | research 06 P1 [CODE-VERIFIED] | VERIFIED | Byte-exact substring present in live `SKILL.md:489` |
| 15 | Ad-hoc field names persisted (`runtime_surface_reachable: true`, `surface_reachability_verdict: DEGRADE`, `surface_production_reachable: false`/`unreachable_surfaces`) | synth-09 §21 Alt 0 Cons | research 00 (lines 47-49) | VERIFIED | research 00:47-49 lists exactly these three per-path improvised names |
| 16 | Ledger written 1/9 quiet-path runs | synth-07 §14.1, §15.3; synth-09 §21 Alt 0 | research 00 line 53 | VERIFIED | research 00:53 "written in only 1 of 9 quiet-path runs" |
| 17 | 3×before/3×after experiment (2026-06-20) refutes prose-only | synth-09 header, §20, §21 Alt 0 | research 00 line 137 | VERIFIED | research 00:137 describes the 3×before/3×after experiment + root cause (engagement asymmetry) |
| 18 | Six canonical field names; only 5 carry `runtime_surface_` prefix, `unreached_surfaces` is the 6th | synth-07 §14.2; synth-09 throughout | research 03 §1 [CODE-VERIFIED] | VERIFIED | research 03 §1 enumerates the six verbatim (SKILL.md 731-736); naming non-uniformity flagged identically |
| 19 | §5.3 pre-filter reads `runtime_surface_unreached`; degrade-only does NOT force Tier 2 | synth-07 §14.2; synth-08 §19.1 P6 | research 03 §2 / research 06 P6 | VERIFIED | research 03 §2 (SKILL.md:402) + research 06 P6 both confirm the carve-out |
| 20 | grader `check_yaml_list_len_eq` is self-consistency gate; FR-DRS makes both operands module-computed | synth-07 §15.4 | research 04 §2 / §4.2 | VERIFIED | research 04 §2 "self-consistency-only caveat" + §4.2 Option B match synth framing exactly |
| 21 | 4-category degrade oracle (a/b/c/d) predicates | synth-06 §12.2; synth-07 §15.2 unit 4 | research 01 §3 | VERIFIED | research 01 §3 table rows (a)-(d) match synth-06 §12.2 row-for-row incl. predicates |
| 22 | depth=1 rootwalk; partial enumeration → DEGRADE; REACHED-rescue at zero referrers | synth-06 §12.3, §12.6; synth-07 unit 5 | research 01 §4 | VERIFIED | research 01 §4 5-step rootwalk: step 3 REACHED-rescue, step 5 DEGRADE-on-partial — exact |
| 23 | Reduction precedence `DEGRADE-on-any-incompleteness > UNREACHED > REACHED`; count invariant | synth-06 §12.5; synth-07 unit 6 | research 01 §5.4 | VERIFIED | research 01 §5.4 precedence + `len(unreached_surfaces)==runtime_surface_unreached` worked example (N rows → 1 count) |
| 24 | LSP non-determinism (cold-start partial, ~24% fewer non-code FPs 63 vs 83) | synth-06 §12.3/§12.7; synth-09 R4, §21 Alt 2 | web-02 F3/F5/F7 | VERIFIED | web-02 F3 "63 vs 83 files … ~24%"; F5 cold-start same-file subset; F7 multi-valued availability — all match |
| 25 | Reuse verdicts: 5 distinct + entrypoint-rootwalk reuse-by-import (S_reuse 0.81) | synth-09 Reuse Audit | reuse-audit.yaml / research 05 | VERIFIED | reuse-audit.yaml: tagger 0.37, referrer 0.67, partitioner 0.57, oracle 0.68, rootwalk 0.81 (reuse-by-import), ledger 0.56 — every S_reuse + verdict matches synth-09 table |

**Tracing result: 25/25 sampled claims VERIFIED. 0 fabrications. 0 missed line-anchors. 0 mis-attributions.**

---

## 9-Criteria Synthesis Quality Review — per file

Criteria: (1) headers match template format · (2) tables use correct column structure · (3) no fabrication
beyond research · (4) findings cite file paths/evidence · (5) options analysis ≥2 options with pros/cons ·
(6) implementation plan has specific steps + file paths · (7) cross-references consistent · (8) no doc-only
claims in Current State / Implementation Plan · (9) stale-doc discrepancies surfaced. (Criterion 10 — key
finding coverage — folded into the source-tracing table above.)

### synth-06-errors-security.md — §12 Error Handling & §13 Security
**Verdict: PASS**

| # | Check | Result | Evidence/Issue |
|---|-------|--------|----------------|
| 1 | Headers match template | PASS | §12 Error Handling & Edge Cases, §13 Security Considerations — exact template §12/§13 titles |
| 2 | Table column structure | PASS | §12.3 uses Scenario/Source/Expected behavior/Test case (richer than template's §12.2 Scenario/Behavior/Test, additive); §13.1 = template Threat/Likelihood/Impact/Mitigation exactly |
| 3 | No fabrication | PASS | Every row sourced (RS:Lnn, web-01 F-refs, research 01/02/05); the network-timeout/5xx rows correctly marked N/A with rationale (§12.7) |
| 4 | Findings cite evidence | PASS | Every edge-case row carries a source column (oracle cat, RS line, web-01 finding) |
| 5 | Options ≥2 | N/A | §12/§13 are not options sections — correctly not instantiated |
| 6 | Impl plan specific | N/A | §12/§13 not impl-plan sections |
| 7 | Cross-refs consistent | PASS | §12.6 step-order, §12.5 reduction precedence, §12.2 oracle all cross-consistent; →§10.6 routing uniform |
| 8 | No doc-only claims | PASS | §12.1 explicitly tags greenfield `[UNVERIFIED — spec-only]`, not asserted-as-current |
| 9 | Stale-doc surfaced | PASS | Correctly states no stale code (greenfield); doc-vs-code tension is the FR-DRS premise itself |

### synth-07-observability-testing.md — §14 Observability & §15 Testing
**Verdict: PASS**

| # | Check | Result | Evidence/Issue |
|---|-------|--------|----------------|
| 1 | Headers match template | PASS | §14 Observability & Monitoring, §15 Testing Strategy — exact |
| 2 | Table column structure | PASS | §15.1 Test Pyramid = Level/Scope/Tool/Coverage target (template uses Level/Coverage/Tools/Responsibility — adapted, with determinism column added; defensible for a determinism-first feature) |
| 3 | No fabrication | PASS | The 5 cases (ids 37–41) + assertions match research 04 §3 exactly; UV commands are real (`uv run pytest`, grader.py path) |
| 4 | Findings cite evidence | PASS | Every unit/case cites research 00/04 + grader.py:191 / grader.py:448-449 |
| 5 | Options ≥2 | N/A | §14/§15 not options sections |
| 6 | Impl plan specific | PASS | §15.2/§15.3 give exact test file paths + UV commands, not generic "write tests" |
| 7 | Cross-refs consistent | PASS | §15.6 AC-coverage map ties each AC to a §14/§15 subsection; count-invariant referenced consistently across §14.2/§15.2/§15.4 |
| 8 | No doc-only claims | PASS | C-5 materializer + C-6 routing explicitly carried as UNVERIFIED, not asserted |
| 9 | Stale-doc surfaced | PASS | C-5 (materializer unlocated) + C-6 (target-prefix fragility) surfaced as load-bearing carry-forwards |

### synth-08-accessibility-perf-deps-migration.md — §16/§17/§18/§19
**Verdict: PASS**

| # | Check | Result | Evidence/Issue |
|---|-------|--------|----------------|
| 1 | Headers match template | PASS | §16 Accessibility, §17 Performance Budgets, §18 Dependencies, §19 Migration & Rollout — exact |
| 2 | Table column structure | PASS | §18.1/§18.3 = template Dependency/Version/Purpose/Risk Level/Fallback exactly; §19 phased table well-formed |
| 3 | No fabrication | PASS | All runner.py / ensemble.py line-anchors verified live (table rows 4-11 above) |
| 4 | Findings cite evidence | PASS | Each dep + migration row cites runner.py:nn / ensemble.py:nn / research 02/05/06 |
| 5 | Options ≥2 | N/A | §16-§19 are not the options section (that is §21 in synth-09) |
| 6 | Impl plan specific | PASS | §19.3 4-phase table: each phase names exact symbols (`runner._audit_once`, `contract.py` `_halted_reason`/`_degraded_reason`, `_IndentDumper`+`_atomic_write_text`) with rollback posture |
| 7 | Cross-refs consistent | PASS | §19 phases align with synth-09 §23.2 phases (both 4-phase, same order, same exit criteria) — cross-partition consistent |
| 8 | No doc-only claims | PASS | §16 N/A rationale is structural (no UI), not a doc claim; §19 producer-change claims trace to verified runner/ensemble code |
| 9 | Stale-doc surfaced | PASS | §19.2 surfaces the stale `REFLECT_CONTRACT_VERSION = "1.0"` vs skill `1.6.0` inconsistency (research 02 Stale Doc) |

### synth-09-risks-alternatives-ops.md — §20–§26 + Reuse & Consolidation Audit
**Verdict: PASS**

| # | Check | Result | Evidence/Issue |
|---|-------|--------|----------------|
| 1 | Headers match template | PASS | §20 Risks, §21 Alternatives, §22 Open Questions, §23 Timeline, §24 Release Criteria, §25 Operational Readiness, §26 Cost — all exact |
| 2 | Table column structure | PASS | §20 = template ID/Risk/Probability/Impact/Mitigation/Contingency exactly; §22 = ID/Question/Owner/Status/Resolution (template adds Target Date, omitted-with-status `🟡 Investigating` — acceptable) |
| 3 | No fabrication | PASS | R1–R5, Alt 0–3, OQ-DRS.1/.2/.3, Reuse Audit all trace to research 00/01/02/05/06 + reuse-audit.yaml |
| 4 | Findings cite evidence | PASS | Every risk + alternative + reuse row carries file:line or research citation |
| 5 | Options ≥2 | PASS | §21 has Alt 0 (Do Nothing) + 3 real alternatives, each with Pros/Cons + explicit "Why Not Chosen" |
| 6 | Impl plan specific | PASS | §23.2 4-phase plan names exact files/symbols (`runtime_surface.py`, `_bfs_reachable` copy, `runner._audit_once`, grader wire) with exit criteria |
| 7 | Cross-refs consistent | PASS | R1↔R5 linkage noted; OQ-DRS.1/.2/.3 ↔ Alt 2/1/contract-version mapping consistent; §6.4 D1 referenced uniformly |
| 8 | No doc-only claims | PASS | Verification posture header (line 6) correctly reserves `[CODE-VERIFIED]` for confirmed source; greenfield claims tagged spec-only |
| 9 | Stale-doc surfaced | PASS | §22.1 C-5/C-6 carry-forwards + §19.2's ensemble version-stamp inconsistency surfaced |

---

## Brief-Specific Structural Checks (the explicit ADDITIONALLY-verify list)

| Required content | Location | Result | Evidence |
|------------------|----------|--------|----------|
| synth-06 §12 captures all 4 degrade-oracle categories | §12.2 table rows (a)/(b)/(c)/(d) + §12.3 + coverage confirmation block | PASS | (a) decorator routes/command decorators; (b) packaging entrypoints `[project.scripts]`/entry-points; (c) registry/DI/string-dispatch; (d) reflection/dynamic-import — all four present with deterministic predicates |
| synth-06 §12 captures the fail-loud asymmetry | §12.1 posture table | PASS | "Never silently PASS an untested surface" + "Never silently Regression an idiomatic dynamic entrypoint" — both poles of the asymmetry stated; restated in coverage block (lines 176-177) |
| synth-07 §15 test pyramid covers 6 units | §15.2 table units 1-6 | PASS | tagger, referrer-finder, partitioner, degrade-oracle, rootwalk, reducer — six logical units enumerated |
| synth-07 §15 covers 5 uc2 cases | §15.3 table ids 37-41 | PASS | unwired-surface-passes, surface-positive-control, surface-dynamic-dispatch, surface-degraded-backend, surface-test-only-ref — five `case_dir` cases |
| synth-07 §15 covers count-invariant | §15.2 (by construction) + §15.4 (grader re-check) | PASS | `len(unreached_surfaces) == runtime_surface_unreached` enforced at producer (unit) + grader (grader.py:191) layers |
| synth-07 §15 covers deterministic-repeat | §15.3 AC-2 acceptance bar | PASS | "byte-identical verdicts across ≥3 repeated runs with zero variance" |
| synth-07 §15 includes UV commands | §15.2 + §15.3 | PASS | `uv run pytest tests/cli/reflect/test_runtime_surface.py -v`; `uv run python .dev/eval-workspaces/sc-reflect/grader.py …`; determinism gate command — UV-only, no bare python |
| synth-08 §16 is N/A with rationale | §16 | PASS | "N/A — backend/library + CLI component, no UI/frontend surface"; WCAG 2.1 AA explicitly inapplicable; template §16.1/§16.2 not instantiated with reason |
| synth-08 §19 captures prose demotion | §19.1 (4b/4b′ → narration-only) | PASS | Before/after table flips LLM-instruction → deterministic-sweep producer; matches research 06 §2 |
| synth-08 §19 captures contract-producer migration | §19.2 (producer change WITHOUT field-set change) | PASS | No `contract_version` bump (stays 1.6.0, OQ-DRS.3); producer LLM→Python; ensemble stamp reconcile noted |
| synth-08 §19 captures preserve-safety rule | §19.1 CRITICAL — PRESERVE block | PASS | SKILL.md:489 safety sentence + DEGRADE-first + fail-open + dynamic→DEGRADE + UC-2 scoping + §5.3 coupling all listed as PRESERVE (matches research 06 P1–P6) |
| synth-09 §21 includes Alternative 0: Do Nothing | §21 Alt 0 *(mandatory)* | PASS | Full Description/Pros/Cons/Why-Not-Chosen; cons cite the §0 falsifier experiment |
| synth-09 §21 includes 3 real alternatives with Why-Not-Chosen | §21 Alt 1/2/3 | PASS | Alt 1 invocation site (OQ-DRS.2), Alt 2 referrer engine (OQ-DRS.1), Alt 3 reachability reuse (§6.4 D1) — each with explicit "Why Not Chosen" |
| synth-09 §22 lists OQ-DRS.1/.2/.3 | §22 table | PASS | All three open questions with owner/status/recommended resolution |
| synth-09 §22 lists unverified findings | §22.1 carry-forwards | PASS | greenfield spec-only caveat, C-5 materializer UNVERIFIED, C-6 routing fragility |
| synth-09 Reuse Audit: one row per component + entrypoint-rootwalk reuse-by-import verdict | Reuse & Consolidation Audit table | PASS | 6 rows (surface-tagger, referrer-finder, partitioner, degrade-oracle, entrypoint-rootwalk, ledger-writer); rootwalk = `reuse-by-import` (S_reuse 0.81, adapt-not-drop-in) — matches reuse-audit.yaml exactly |

**All 16 brief-specific required items: PASS.**

---

## Findings (4 minor advisory — none blocking, none a source-tracing error)

### F1 (MINOR — cross-partition consistency, informational)
`contract_version` and the six-field count are described identically across synth-07/08/09 (1.6.0, no bump,
five `runtime_surface_*` + `unreached_surfaces`). This is internally consistent within Partition B. **Partition
note:** I could not cross-check Partition A (synth 01–05) — if synth-02 (Requirements) or synth-04 (Data/API)
states a different field count or version, the merge step must reconcile. No defect within B.

### F2 (MINOR — line-anchor convenience, not an error)
synth-07 §15.4 cites `grader.py:191` for `check_yaml_list_len_eq` and `grader.py:448-449` for target-prefix
bucketing — both verified live. Note these anchors are to `.dev/eval-workspaces/sc-reflect/grader.py`, a
**dev-workspace** file under modification (`git status` shows `grader.py` as `M`). The anchors are correct as
of this read, but are intrinsically more volatile than `src/` anchors. Advisory only: the TDD reader should
treat eval-workspace line numbers as point-in-time. No action required.

### F3 (MINOR — table-column adaptation, defensible)
synth-07 §15.1 and §16/§17 tables adapt the template's exact column headers (e.g., Test Pyramid adds a
"Determinism requirement" column; §15.1 swaps "Responsibility" for "Determinism requirement"). These are
*additive/substitutive adaptations* appropriate to a determinism-first feature, not structural violations.
Criterion 2 still PASS — flagged for transparency so the assembler is aware the headers are not template-verbatim.

### F4 (MINOR — sixth-field naming non-uniformity, correctly surfaced by synth)
All four synth files correctly carry the known naming wart: only five of the "six `runtime_surface_*` fields"
literally carry the prefix; the sixth (`unreached_surfaces`) does not. synth-07 §14.2 and synth-09 surface
this faithfully (matches research 03 §1). **This is a property of the upstream contract, not a synth defect** —
recorded so a downstream reader does not mistake it for a typo and "fix" it to `runtime_surface_unreached_surfaces`.

---

## Summary

- **Files reviewed:** 4 (synth 06, 07, 08, 09)
- **9-criteria review:** 4/4 files PASS (every applicable criterion PASS; options/impl-plan criteria N/A where the section is not an options/plan section)
- **Brief-specific structural checks:** 16/16 PASS
- **Source-tracing:** 25/25 sampled claims VERIFIED against live source or cited research
- **Source-tracing errors found:** **0** (adversarial "≥5 errors" prior NOT confirmed)
- **Findings:** 4 MINOR / advisory (F1 cross-partition reconcile note, F2 eval-workspace anchor volatility, F3 column adaptation transparency, F4 upstream naming wart) — **0 CRITICAL, 0 HIGH, 0 blocking**
- **Fabrication:** none detected
- **Contradictions (synth vs source, or synth vs synth within B):** none
- **Cross-partition (B vs A) reconciliation:** deferred to merge step (F1) — cannot be checked from this partition

**Gate B verdict: PASS.** synth 06–09 are faithful to their source research, structurally template-conformant,
and contain every brief-required element. Recommend proceeding to assembly. The 4 minor findings are advisory
context for the assembler/merge step, not fixes that block the gate.

---

**Status:** Complete
