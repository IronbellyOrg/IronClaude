# Synthesis Quality Review — Report C (synth-07, synth-08, synth-09)

**Analyst:** rf-analyst (synthesis-review)
**Date:** 2026-06-20
**Mode:** report-only (`fix_authorization: false`) · ADVERSARIAL STANCE
**Task:** TASK-TDD-20260619-235400 (FR-RH2 — Headless Tier-2 Ensemble Fix)
**Files reviewed (3):**

- `synthesis/synth-07-observability-testing.md` (TDD §14 Observability, §15 Testing Strategy)
- `synthesis/synth-08-perf-deps-migration.md` (TDD §16 Accessibility, §17 Performance, §18 Dependencies, §19 Migration)
- `synthesis/synth-09-risks-alternatives-ops.md` (TDD §20–28 Risks/Alternatives/OQ/Timeline/Release/Ops/Cost/Refs/Glossary)

**Cross-checked against:** `research/` (00, 01, 02, 03, 05, 07, 08, 09, web-01, reuse-audit.yaml), the source spec `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`, and shipped source (`cli/reflect/{contract.py,runner.py,models.py}`, `cli/swarm/{commands.py,reduce.py,dispatch.py,lenses/bare_review.py,recipes/__init__.py}`, `tests/cli/reflect/conftest.py`, `sc-adversarial-protocol/SKILL.md`).

---

## VERDICT: PASS (1 minor finding — cross-file directive-numbering inconsistency)

All three files pass the 9-criteria Synthesis Quality Review. All six special-attention items are **present, correctly placed, and code-grounded**. One real consistency defect (F-1) is surfaced for fix; it is non-blocking for assembly because the underlying facts are all code-verified and unambiguous in their own sections — only the cross-file `D`-label is inconsistent.

---

## Special-Attention Items (all 6 CONFIRMED)

| # | Required item | Where | Verdict | Evidence |
|---|---------------|-------|---------|----------|
| 1 | **Alternative 0: Do Nothing** present in synth-09 §21 | synth-09 §21 L36–52 | ✅ PRESENT | Marked `*(mandatory)*`; has Description / Pros / Cons / Why Not Chosen; cons cite the architectural-guarantee-of-broken-headless-Tier-2 (PRD-extraction L256) and the NFR-7-forbids-the-only-in-process-alternative reasoning. Genuine, not boilerplate. |
| 2 | **OI-1 / Q1 marked BLOCKING** in synth-09 §22 | synth-09 §22 Q1 L115 + blocking note L124 | ✅ PRESENT | Row labeled `Q1 (OI-1, BLOCKING GATE)`, Target `BEFORE any FR-RH2.3 code lands`; reinforced by the §22 "Blocking note" (L124), M0 in §23.1, and DoD L217. Research answer (disjoint schemas, synth-05 §6–7) carried with the "still must be validated against shipped diff" caveat. |
| 3 | **NFR-7 reconciliation** in synth-08 §19 (Layer-B forbids Task/subagent/anthropic + raw subprocess; guard extended to `ensemble.py` via `_NO_NEST_SRCS`) | synth-08 §19.6 L202–219 | ✅ PRESENT | OI-2 = "CONFIRM-with-scope-extension, not a silent bypass." States `_ENSEMBLE_SRC` + `_NO_NEST_SRCS = [_RUNNER_SRC, _ENSEMBLE_SRC]`, loops Layer-B import test + raw-subprocess test over both, **reuses existing regexes (no new regex)**, and correctly notes the raw-subprocess ban stays scoped to the two no-nest modules (NOT package-wide) to preserve `commands.py`'s sanctioned `--tmux subprocess.run`. Recorded amendment text supplied. |
| 4 | **Stub integration test EXPLICITLY avoids the canned-fixture mock-gap** (must not reuse the `ClaudeProcess` MagicMock) | synth-07 §15 L99, §15.3 CRITICAL note L139 | ✅ PRESENT | §15 opening names the load-bearing risk (`make_claude_process_stub` copies `fixtures/*.yaml` → `return-contract.yaml`, so `pass.yaml` `tier_reached:2` is a typed constant). §15.3 CRITICAL (FR-RH2.5 AC-3) MANDATES injecting `StubTransport` at the transport seam, contract **produced by the real reduce step, never pre-written**, and forbids reusing the canned-fixture path. synth-08 §19.6 L219 reinforces ("inject StubTransport, not monkeypatch subprocess"). |
| 5 | **One-reviewer negative witness present and falsifiable** | synth-07 §15.3 I2 L144 + mutation-contrast L158; synth-09 §21 R5 mitigation, §22 Q8, §23 Phase 5, Glossary "Negative witness" L328 | ✅ PRESENT | I2 asserts the I1 positive assertions MUST FAIL for 1 reviewer (`reviewer_count < 2`, `tier_reached != 2`, diversity != "full") — "proving the proof is falsifiable, not vacuous." Mutation-catching contrast (I1 GREEN ↔ I2/I4/I5/I6 RED) is explicit. Grounded in real `_degraded_reason` triggers (L160). |
| 6 | **D4** (recipe binding reuse `bare-review-v1` + net-new lens module) and **D5** (`--suspect-source` unparsed → §22) present | synth-08 §18.2/§19.3 (D4); synth-09 §22 Q4/Q5 (D5) | ✅ PRESENT (see F-1) | D4: synth-08 §19.3 = net-new `lenses/reflect_review.py` + recipe binding reuses `bare-review-v1` (zero recipe edits, Path A). D5: synth-09 Q5 surfaces `--suspect-source` emitted-but-unparsed as `[CODE-CONTRADICTED]`, routed to §22. **Caveat F-1:** synth-09's banner (L10) mislabels the recipe directive — see Finding 1. |

---

## Cross-Validation of Load-Bearing Citations (independent re-read of source)

Adversarial spot-check of every code anchor the special-attention items depend on. **All verified.**

| Claim (file) | Cited location | Actual (re-read) | Verdict |
|---|---|---|---|
| `_resolve_run_transport_factory` is a PRIVATE `_`-prefixed symbol; no public equivalent (synth-08 §18.2 L122; synth-09 Q7) | `commands.py` L612 | `def _resolve_run_transport_factory(` at L612; `_resolve_run_transport` (also private) at L510 | ✅ VERIFIED — coupling-smell claim correct |
| `ensemble-empty` slug absent from reflect code `[CODE-CONTRADICTED]` (synth-09 Q6/D3) | `grep ensemble-empty src/.../reflect/` | **0 hits** in `cli/reflect/`; slug appears only in spec.md L448 | ✅ VERIFIED — contradiction is real |
| `--suspect-source` emitted by lens, absent in adversarial SKILL `[CODE-CONTRADICTED]` (synth-09 Q5/D5) | `bare_review.py` L65–68 / SKILL.md | `--suspect-source {suspect_files}` at `bare_review.py` L67; **0 hits** in `sc-adversarial-protocol/SKILL.md` | ✅ VERIFIED — contradiction is real |
| `_degraded_reason` Triggers 6/7/10 (synth-07 §14.4) | `contract.py` L263-264 / L267-269 / L280-281 | `expected_tier>=2 and tier_reached==1` L263; `t2_model_class_diversity` L267; `merge_method=="single-reviewer-fallback"` L280-281 | ✅ VERIFIED (line numbers exact) |
| `done.json` sentinel (synth-07 §14.1) | `reduce.py` L140 / L402-459 / L456 | `DONE_SENTINEL_FILENAME="done.json"` L140; `emit_done_sentinel` L402; `contract.parent / DONE_SENTINEL_FILENAME` L456; kill path `_emit_killed_done_sentinel` documented L428 | ✅ VERIFIED |
| `bare-review-v1` in recipes REGISTRY/STRATEGIES (synth-08 D4) | `recipes/__init__.py` | `"bare-review-v1"` present; "ports t2_normalize.py (bare-review lens)" | ✅ VERIFIED |
| `_DEFAULT_TIMEOUT_SEC = 180` NFR-010 (synth-08 §17.2) | `dispatch.py` L124 | `_DEFAULT_TIMEOUT_SEC = 180` L124 | ✅ VERIFIED |
| `expected_tier = 2 if config.depth in {"standard","deep"} else 1` at runner.py:403 (synth-08 §19.2) | `runner.py` L403 | exact predicate at L403 | ✅ VERIFIED (verbatim) |
| `make_claude_process_stub` copies fixture → `return-contract.yaml` (synth-07 §15 conftest gap) | `conftest.py` L98-138 | `def make_claude_process_stub()` L99; `(output_dir/"return-contract.yaml").write_bytes(fixture_bytes)` L130 | ✅ VERIFIED |
| `ReflectConfig` in models.py L57-91, append after `max_fix_iterations` L86 (synth-08 §19.2) | `models.py` L57-91 | `class ReflectConfig:` L58; `max_fix_iterations: int` L86 | ✅ VERIFIED |

**Zero fabrications detected.** Every verdict/exit-code, reason slug, field name, and line number sampled traces to read code or spec text. `[UNVERIFIED]` tags are correctly confined to `ensemble.py`-internal names (module does not exist yet) and the spec-vocabulary `ensemble-empty` string.

---

## 9-Criteria Review — Per File

### synth-07 (Observability & Testing) — PASS

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Section headers match template | PASS | §14 = Logging/Metrics/Tracing/Alerts (re-cast as artifact/exit-code observability with justification) ; §15 = Test Pyramid + Unit/Integration/Backward-compat tables. Header banner declares template alignment (L6). |
| 2 | Table column structure correct | PASS | Test-case tables use #/Component/Test case/Expected/FR-NFR; traceability table FR-NFR→Covered-by. Consistent. |
| 3 | No fabrication beyond research | PASS | Every anchor re-verified above. `[UNVERIFIED]` correctly scoped to `ensemble.py` names. |
| 4 | Findings cite file paths + evidence | PASS | `_degraded_reason` line numbers, conftest L98-138, reduce.py sentinel lines — all accurate. |
| 5 | Options analysis ≥2 with pros/cons | N/A for §14/§15 (options live in synth-09 §21) | §15.1 pyramid + §15.3 anti-pattern serve the "why this design" role; acceptable for a testing-strategy section. |
| 6 | Implementation plan specific (file paths, not generic) | PASS | Names exact new test files (`test_ensemble_unit.py`, `test_ensemble_stub_integration.py`), existing files to extend, and `uv run pytest` commands per level. |
| 7 | Cross-references consistent | PASS | §15.5 traceability maps every U/I/B test to an FR/NFR; the conftest-gap risk (§15) ↔ §15.3 CRITICAL ↔ synth-08 §19.6 are mutually consistent. |
| 8 | No doc-only claims in Current/Impl | PASS | All claims code-traced; no doc-sourced architectural assertion stands un-verified. |
| 9 | Stale-doc / CODE-CONTRADICTED surfaced | PASS | `ensemble-empty` UNVERIFIED-as-spec-vocab noted (§14.4 L78); not asserted as current code fact. |
| 10 | Key-finding coverage | PASS | The load-bearing research finding (conftest mock gap, research 07 Parts 3-4) is the spine of §15. Negative-witness contract reflected. |

### synth-08 (Performance, Dependencies, Migration) — PASS

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Section headers match template | PASS | §16 Accessibility (N/A w/ rationale), §17 Performance Budgets, §18 Dependencies (External/Internal/Infra/Risk), §19 Migration & Rollout. |
| 2 | Table column structure correct | PASS | §18.1 Dependency/Version/Purpose/Risk/Fallback; §18.2 Dependency/Symbol/Status/Interface/Risk; §19.1 Phase/Description/Duration/Rollback. |
| 3 | No fabrication | PASS | `_DEFAULT_TIMEOUT_SEC=180`, runner.py:403, ReflectConfig L57-91/L86, private-factory L612 all verified. |
| 4 | Findings cite paths + evidence | PASS | Exact symbols + line numbers throughout; `[CODE-CONTRADICTED]` tags on private-factory-no-public-equiv and `--suspect-source`. |
| 5 | Options ≥2 pros/cons | PASS (deferred) | §18.2 records import-private-vs-recompose decision; full options live in synth-09 §21 (correct division of labor). |
| 6 | Implementation plan specific | PASS | §19.2 3-file chain names models.py tail / config.py resolve_config / commands.py @click.option with exact line anchors; §19.3 net-new lens + register in `lenses/__init__.py`. |
| 7 | Cross-references consistent | PASS (within-file) | §19.6 NFR-7 reconciliation ↔ §17/§18 risk callouts ↔ Cross-Section Notes provenance all align. (Cross-FILE label issue → F-1.) |
| 8 | No doc-only claims | PASS | §16 N/A is a justified scope decision, not a doc claim; all perf/dep facts code-traced. |
| 9 | CODE-CONTRADICTED surfaced | PASS | Private-factory-no-public-equivalent and `--suspect-source` gap both carried as `[CODE-CONTRADICTED]` into §18.2/§18.4. |
| 10 | Key-finding coverage | PASS | OI-1 (ResultContract→reflect translation) flagged as the BLOCKING real work (§18.4); reuse-by-import posture reflected. |

### synth-09 (Risks/Alternatives/OQ/…/Glossary) — PASS (F-1 minor)

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Section headers match template | PASS | §20–28 all present and ordered per template anchor. |
| 2 | Table column structure correct | PASS | §20 ID/Risk/Prob/Impact/Mitigation/Contingency; §22 ID/Question/Owner/Target/Status/Resolution; §25.1 runbook columns correct. |
| 3 | No fabrication | PASS | `ensemble-empty` absence + `--suspect-source` gap independently re-verified (0 hits each). Risk provenance line (L28) attributes R1-R8 to spec §7 L481-490, R9 as synthesis-derived — honest. |
| 4 | Findings cite paths + evidence | PASS | Q5 input-parser flag list, Q6 grep result, Q7 private symbol — all accurate. |
| 5 | Options ≥2 pros/cons | PASS | §21 has Alt 0 (Do Nothing), Alt 1, Alt 2 + the import-vs-subprocess sub-decision, each with Pros/Cons/Why-Not-Chosen. |
| 6 | Implementation plan specific | PASS | §23 milestones M0-M6 + Phase 1-6 deliverables with exact files; §24 DoD enumerates all 9 FR + 8 NFR. |
| 7 | Cross-references consistent | **MINOR FAIL → F-1** | OI/Q ↔ R cross-refs and §27 reference paths are consistent, BUT the binding-directive `D`-labels are inconsistent **across** synth-08 and synth-09 (see Finding 1). |
| 8 | No doc-only claims | PASS | Alternatives + risks grounded in reuse-audit, web-01, and code; no un-verified doc architecture asserted. |
| 9 | CODE-CONTRADICTED surfaced | PASS | Q5 (`--suspect-source`) and Q6 (`ensemble-empty`) both carry the contradiction explicitly into Open Questions, with reconciliation options. |
| 10 | Key-finding coverage | PASS | Reuse-audit S_reuse 0.81, web-01 import-vs-subprocess grounding, and the disjoint-schema OI-1 finding are all reflected in Alternatives + Risks + Open Questions. |

---

## Findings Requiring Fixes

### Finding 1 (MINOR — cross-file consistency, criterion 7): Binding-directive `D`-numbering collides across synth-08 and synth-09

- **Severity:** Minor (does not block assembly; underlying facts all code-verified and unambiguous in-section)
- **Source:** `synth-08-perf-deps-migration.md` L78, L88, L226 vs `synth-09-risks-alternatives-ops.md` L10, L120, L217
- **Issue:** The label `D3` denotes **two different directives** depending on file:
  - **synth-08** binds `D3` = the `max_fix_iterations` default-2 auto-fix cap (§17.4 L78 "default 2 (D3)"; L88; L226 "D3 default `max_fix_iterations=2`"). It binds `D4` = recipe binding + net-new lens, `D7` = 3-file ReflectConfig edit.
  - **synth-09** binds `D3` = the `ensemble-empty` slug absence (banner L10 "**D3** (`ensemble-empty` slug absent…)"; Q6 L120 "Q6 (**D3**…)"; DoD L217 "D3 (Q6)"). It binds `D5` = `--suspect-source` unparsed.
  - A reader/assembler cannot resolve what "D3" means without knowing which file authored the sentence.
- **Spawn-prompt cross-check:** the review brief defines the two directives to confirm as **"D4 (recipe binding reuse bare-review-v1 + net-new lens module)"** and **"D5 (--suspect-source unparsed → §22)."** synth-08 (D4) and synth-09 (D5) each match the brief for their own directive, but synth-09's banner L10 calls the *recipe* directive partner of D5 "D3" rather than "D4", and additionally re-uses "D3" for the `ensemble-empty` item — compounding the collision.
- **Why it matters (adversarial read):** TDD assembly (rf-assembler) concatenates these sections into one document. Two incompatible `D`-glossaries in the same TDD make every `(Dn)` citation ambiguous and will read as an internal contradiction to a downstream reviewer, even though no factual claim is wrong.
- **Required fix (for the authoring agent / assembler, NOT this analyst):** Adopt one canonical directive numbering across synth-07/08/09 (the orchestration BUILD_REQUEST `D`-labels are the source of truth; reconcile against it). Concretely: pick a single label for the recipe-binding directive (the brief uses **D4**) and a single label for the `ensemble-empty` reconciliation and the `max_fix_iterations` cap so no number is overloaded. Note: the spec.md itself contains **no `Dn` tokens** (grep: 0 hits) — the `D`-numbering is an orchestration-layer artifact, so the canonical list must come from the BUILD_REQUEST, not the spec.

---

## Observations (no fix required)

- **O-1 (defensible scoping):** synth-07 §14.4 documents only `_degraded_reason` Triggers 6/7/10, omitting Trigger 11 (null convergence at T2, `contract.py` L283-284). This is intentional ("the three FR-RH2-relevant degraded slugs") and synth-09 §22 footnote separately flags the `adversarial_convergence_score` type as `[UNVERIFIED]`, so Trigger 11 is not silently dropped. Acceptable.
- **O-2 (correct N/A):** synth-08 §16 Accessibility N/A is correctly justified (backend/library, no client surface) and matches the template's "backend services/libraries skip this section" guidance. Not a gap.
- **O-3 (honest gate caveat):** synth-09 Q1 correctly states the OI-1 table is *produced* (synth-04) but **not yet validated against the shipped diff** — it does not over-claim the BLOCKING gate as closed. Good adversarial honesty.

---

## Summary

- **Files reviewed:** 3 — all PASS
- **Special-attention items confirmed:** 6 / 6
- **Load-bearing citations independently re-verified:** 10 / 10 (zero fabrication)
- **Findings:** 1 minor (F-1, cross-file directive-numbering collision; non-blocking)
- **Critical issues blocking assembly:** 0

**Recommendation:** Proceed to assembly. Address F-1 (reconcile the `D`-label glossary across synth-07/08/09 against the BUILD_REQUEST directive list) either before assembly or as an assembler normalization pass — it is a labeling fix, not a content fix, and no factual claim needs to change.
