# QA Report — Task ↔ Research Alignment (task-integrity)

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Analyst:** rf-analyst (adversarial stance)
**Date:** 2026-07-03
**Task file:** TASK-RF-qa-reflect-harden-20260703-044500.md
**Research dir:** research/ (01-08 + research-notes.md)
**Track goal:** Additively harden RF QA + /sc:reflect vs PR #209 F1-F4 via FX1/FX2/FX3/FX5/FX7 (regression-guards; F1-F4 already fixed at HEAD 46a787da).

---

_Status: COMPLETE._

## Methodology & Scope

Read in full: task file (frontmatter + Overview + Objectives + Execution Context + all Phase 1-5 items + Phase Gates + Post-Completion), research-notes.md, and research 01 (FX3), 02 (FX5), 03 (FX7), 04 (FX2/FX1), 08 (gap-fill G1-G6). Spot-verified cited line-anchors and precedent-test names against 05 (test conventions). Cross-checked every FX target, constraint, edge case, brief-guard test, exclusion, and framing claim in the task against the CODE-VERIFIED research findings (08 G1-G6 authoritative override).

Adversarial stance applied: assumed the builder dropped or misrepresented findings; hunted for under-coverage, fabrication, stale-plan leakage, and internal incoherence.

---

## Lens Item 1 — Per-Fix Target Correctness (task acts on the research-verified target?)

| Fix | Research-verified target (08 G-ref) | Task encoding | Verdict |
|-----|-------------------------------------|---------------|---------|
| **FX3** | New `test_setup_questions_resolution.py`; AST-introspect `questions.py`; SUBSET (not onto, `augment_app_slug` intentionally unreferenced); dynamic `dataclasses.fields`; probe_pr/pr_number F3 trap (01, 08 G5) | Step 2.1-2.3: exactly this — AST-parse via `__file__`, `_answer_default`/`_evidence_attr` collection, `answer_key = answer_attr or attr`, subset direction, dynamic field sets, `ast.Constant` str guard (blocks dynamic-arg bypass), F3-trap `_evidence_attr("pr_number")` | ALIGNED |
| **FX5** | `conftest` `pytest_generate_tests` collector over 4 gate-helper files; negative + DIFFERENTIAL (mutation-must-fail); registry-anchored; marker-free (02, 05, 08 G4/G5) | Step 2.4-2.9: registry-anchored collector, marker-free `pytest_generate_tests`, existence+coverage+drift checks, differential monkeypatch mutation tests | TARGET ALIGNED — **coverage BREADTH under-delivered (see HIGH-1)** |
| **FX7** | `ensemble.py build_reflect_contract` additive: non-exempt skip reason + `degraded_components` + `*_verified` + `regression_verified` boolean; NO exemption edit; NO `status:"degraded"` (03, 08 G6) | Step 3.1-3.6: `reviewers_requested` defaulted kwarg, append `reviewer-shortfall` to `degraded_components`, swap L551 to non-exempt reason (path i), `verification_verified`/`reviewers_verified`/`regression_verified` siblings, exemption byte-unchanged, `status` stays `{success,failed,partial}`, fail-safe HALT clause | ALIGNED |
| **FX2** | Augment `rf-qa-qualitative.md` Code Compatibility items 4-6 IN PLACE; keep 15-count; AX-2; no AX-6 (04, 08 G1/G3) | Step 4.1: Branch A augment items 4-6 in place, header 15 UNCHANGED, annotate AX-2 ≥IMPORTANT, no AX-6, Critical Rules/severity-floor untouched | ALIGNED |
| **FX1** | `reflect-reviewer.md` advisory slot + `deviation-taxonomy.md` advisory dimension (NOT a 5th class) (04, 08 G2) | Step 4.2-4.3: advisory Role note + `persona_lens` value + separate non-gating Output-Format subsection; `## Correctness-gap` parallel dimension mirroring Grounding-gaps, "adds no 5th category", never sets `regression_present` | ALIGNED |

**Notable positive:** research 04 (R4) originally recommended bumping the checklist count "15 → 16" (Branch B, 04:394-395), but 08 G1/G3 later decisively resolved to Branch A (keep 15). The task correctly follows the authoritative gap-fill override and explicitly forbids the 16-bump — evidence the builder navigated the research-internal conflict rather than blindly copying R4.

---

## Lens Item 2 — Fabrication Check (task item asserts an action NOT grounded in research?)

No fabrication found. Every cited symbol, line-anchor, and precedent test resolves to a research finding:
- FX3 field facts (17 `SetupAnswers` fields, `EvidenceBundle` attrs, `augment_app_slug` unreferenced, probe_pr trap) — grounded in 01:20-27,49,71,239-263.
- FX7 precedents (`test_r2f2_build_reflect_contract_emits_honest_verification_fields` :342-364; `test_verification_skip_exemption_not_degraded` :154; `test_verification_not_run_unexempted_is_degraded` :166-177; `test_writeback.py:78-92`) — grounded in 03:229-230,356-364,370.
- FX5 `ValidationReport.passed` (validation.py:62), `required_unobserved` (candidate.py:47), `MUST_OBSERVE_FIELDS` (candidate.py:18) — grounded in 02:45,90,208,215.
- FX2/FX1 anchors (`:670-676`, `:639`, `:660`, `:699-715`, persona_lens `:54`, Behavioral Mindset `:42`, Grounding-gaps `:129-154`, FR-RH1 `:117-127`, Kill List `:154`) — grounded in 04:74-126,215-266,279-348,379-406.
- `--skip-if-pass` fail-closed hardening (Step 3.3c, marked OPTIONAL) — grounded in 03:263-272,395 ("Require `verification_verified is True` before honoring a prior-pass skip; absent-on-old = unverified = fail-closed").

**Stale-plan traps correctly avoided (all 4):** the task's MANDATORY WORKFLOW COMPLIANCE section and phase items do NOT (a) rename a nonexistent `internal-consistency` lens, (b) add a literal 5th deviation category, (c) treat "Phase 2/4" as a pipeline-gate attach point, or (d) edit `_VERIFICATION_SKIP_EXEMPTIONS`. Each stale plan phrase is explicitly flagged CODE-CONTRADICTED and forbidden. PASS.

---

## Lens Item 3 — Research Edge Cases Reflected in Verification Criteria

| Edge case (research) | Reflected in task? |
|----------------------|--------------------|
| Dynamic/variable `getattr` arg bypasses FX3 static check | YES — Step 2.2 assertion (4): every deriver arg must be `ast.Constant` str, else fail |
| Helpers OUTSIDE the FX5 4-file scan (`classify`, `DetectionContract.from_yaml`, `load_evidence`) | YES — Step 2.4 records the explicit scope-boundary NON-GOAL / residual-risk handoff (matches 02:219) |
| `regression:0` consumers must not break (int-coercion) | YES — FX7 constraint: `regression_verified` boolean sibling, NOT `regression:unknown` in int-typed `deviation_count_by_class` (matches 03:326,394) |
| Anti-gaming: differential (mutation-must-fail), not merely "a negative test exists" | YES as a CONSTRAINT (Key Constraints + Steps 2.5/2.6 monkeypatch idiom) — but see HIGH-1 for breadth |

PASS (edge-case intent captured).

---

## Lens Item 4 — Brief-Guard Tests as Post-Edit Verification + sync-dev

Step 4.4 runs `make sync-dev && make verify-sync` then the guard set: `test_five_axes_overlay`, `test_axis_column_populated`, `test_severity_floor_unweakened`, `test_drift_axis_inactive_when_no_goal_baseline`, `test_self_audit_inv_019`, `test_reviewer_readonly_tools`, `test_reviewer_brief_constraints` — a SUPERSET of the lens-named four, correctly adding the three byte-parity tripwires (08 G2). Per-failure remediation guidance is item-embedded (count-bump → restore Branch A; AX-6/N-A leak → restore AX-2; tools-line touched → restore). Step 4.3 correctly notes `deviation-taxonomy.md` has ZERO guarding tests → manual-verify (matches 08 G2:118-126). PASS.

---

## Lens Item 5 — Deferred/Excluded Fixes Represented as Exclusions

FX4 (redundant, subsumed by FX3), FX6 (advisory-annotation-only, not shipped as a gate), FX8/FX9 (deferred) are all in the Task-Overview "Scope exclusions (do NOT create implementation items)". Consistent with research-notes AMBIGUITIES. PASS with **LOW-1** note on FX6 framing.

---

## Lens Item 6 — F1-F4-Already-Fixed Framing Consistency

Consistent throughout: Overview ("REGRESSION-GUARDS, not live-bug fixes"), Phase 2 intro ("post-F1–F4-fix tree"; author to PASS green, FAIL only on regression), Objectives, and each FX item's "already fixed at HEAD 46a787da" framing. Baseline confirmed in Step 1.3 (`git rev-parse HEAD == merge-base == 46a787da`). PASS.

---

## FINDINGS (severity-rated)

### HIGH-1 — FX5 authors negative+differential pairs for only 5 of the ~21 research-mandated gate helpers → task not green-as-written; drops research 02 §4.1-step-3 / §6.2

**Research requirement (02 §4.1 step 3 + §6.2, verbatim):** "Each registered helper needs BOTH a negative-input test and a differential (mutation) test; the collector FAILs RF Phase-4 if either is absent." §4.1 step 1 enumerates a registry of ~21 helpers (candidate 8 + lockgate 4 + diagnosis 4 + validation 5), and §6.3 adds `ValidationReport.passed` and the `*_checks` family (≥22-23).

**What the task actually authors:** Steps 2.5 + 2.6 author negative+differential pairs for EXACTLY FIVE helpers — `candidate._path_resolves`, `lockgate._paths_resolve`, `candidate.CandidateContract.required_unobserved` (2.5) and `diagnosis._stale_blockers`, `validation._negative_control_checks` (2.6). These are precisely the 5 helpers research §5 gave CONCRETE mutation examples for (§5.1-§5.5). `HELPER_TEST_MAP` therefore holds 5 entries.

**The break:** Step 2.7a(1) registers `GATE_LOAD_BEARING_HELPERS` "from the Step 2.4 inventory (≥21)" and Step 2.7a(3)(b) coverage-checks that EACH registered helper has both a `negative` and `differential` entry in `HELPER_TEST_MAP`, FAILing if either is missing. Step 2.8 expects "every FX5 per-helper coverage case green." With 21 registered but only 5 covered, **16 parametrized coverage cases FAIL** — the task cannot reach green as written.

**Either-way trap (no benign reading survives):** if the registry is instead trimmed to the 5 covered helpers, then Step 2.7a(3)(c)'s drift-alarm ("a gate-shaped helper NOT in the registry → FAIL") fires for the other ~16 gate-shaped helpers. With only 5 authored pairs, FX5 cannot pass regardless of registry size.

**Root cause (finding-drop):** the builder acted on research §5's 5 concrete examples but dropped research §4.1-step-3/§6.2's mandate that ALL registered helpers carry pairs. Steps 2.5/2.6 enumerate 5 named helpers; NO item instructs authoring pairs for the remaining ~16 (`lockgate._identity_observed/_emission_shape_observed/_negative_controls_pass`, `candidate._findings_locus/_review_completeness_signal/_observed_severity_path/_selected_identity/_selected_app_slug/_emission_shape`, `diagnosis._resolve_optional_path/_evidence_sha256/_validation_result`, `validation._structure_checks/_surface_checks/_freshness_checks/_identity_checks`, `ValidationReport.passed`).

**Escape-hatch not in research → gate-weakening:** Step 2.7a introduces a "registered helper genuinely lacks a buildable differential → commented registry exemption WITH rationale" clause. Research provides NO such exemption mechanism ("FAILs if either absent"). Practically, a literal executor hitting 16 coverage failures at Step 2.8 (whose guidance is "correct the NEW test") would mass-exempt the 16 → net **5/21 ≈ 24% real differential coverage**, gutting exactly the anti-gaming breadth FX5 exists to provide, and silently violating "ADDITIVE-ONLY: weaken no gate."

**Remediation (pick one, both research-consistent):**
- (A) Add explicit build items authoring negative+differential pairs for ALL registered gate helpers (author the remaining ~16), matching research §6.2; OR
- (B) Narrow `GATE_LOAD_BEARING_HELPERS` + the drift-alarm scope to the 5 differential-anchored helpers and DEMOTE the rest to documented residual-risk NON-GOALS (mirroring research §4.3's own scope-boundary treatment), so coverage and drift-alarm agree and the task is green-as-written — and drop the ad-hoc exemption clause.

Until reconciled, FX5 does not satisfy its Objective 2 ("the collector FAILs on any registered gate helper missing a negative or differential test ... all passing green") as authored.

### MEDIUM-2 — FX5 drift-alarm cannot see the `*_checks` family / dataclass methods it is told to register

Step 2.4 REQUIRES the registry include "the whole `validation._*_checks` builder family" and the two dataclass methods (`required_unobserved`, `ValidationReport.passed`). But Step 2.7a(3)(c) specifies the drift-alarm matches "the gate-shaped pattern in §4.1 step 4" — whose regex (`_(path|paths)_resolv|_resolve_|_findings_|_observed_|_selected_|_stale_|_shape_observed|_review_completeness`) does NOT match `_structure_checks`/`_surface_checks`/`_freshness_checks`/`_identity_checks`/`_negative_control_checks` or the dataclass methods. Research 02 §4.3 EXPLICITLY flags this as the naive-scan blind spot. Consequence: a NEW `_foo_checks` gate helper added later will NOT trip "new gate-shaped helper not registered," so the drift protection research wanted for exactly the flagged family is absent. The task faithfully copied both §4.1-step-1 and §4.1-step-4 but did not reconcile that step-4's pattern is blind to the step-1 family — the gap research raised is inherited, not closed.

### LOW-1 — FX6 excluded outright though research-notes framed it "advisory-only" (parallel to the shipped-advisory FX1)

Research-notes lists disposition as "FX3/FX5/FX7 P0, FX2/FX1 P1, **FX6 advisory-only**, FX4/FX8/FX9 deferred" — grouping FX6 SEPARATELY from the deferred set, the same "advisory-only" label FX1 ships under. The task lumps FX6 with the deferred exclusions ("Not shipped as a gate"). Mitigating: no research file (01-08) scoped FX6 with a target/anchor, so the authoritative research workspace did not commission an FX6 build; excluding it is defensible. Flagged LOW for user confirmation that dropping FX6 (vs shipping it as an FX1-style advisory annotation) is intended.

### LOW-2 — `reviewers_verified` computation under-specified for the `reviewers_requested=None` default

Step 3.2(d) defines `reviewers_verified: <bool: reviewer_count >= reviewers_requested>`, while Step 3.2(a) makes `reviewers_requested: int | None = None` (defaulted for direct-call/test sites). `reviewer_count >= None` raises `TypeError` in Python 3; the item does not specify the None-guard (e.g. `reviewers_requested is None or reviewer_count >= reviewers_requested`). Implementation-precision gap that the L2 build/tests would surface; not a research-drop. Recommend the item state the None-guard explicitly.

### LOW-3 — `persona_lens` described as an "enum" where research shows a free-form "e.g." field

Step 4.2(b) says "formalize a `no-spec-correctness` value in the `persona_lens` enum at :54," but research 04:217 quotes persona_lens as a free-form guidance field with "e.g." examples (correctness-focused, …), not a closed enum. Harmless (adding a value is research-sanctioned, 04:253-262), but the "enum" characterization is imprecise and could mislead an executor into expecting a strict enum declaration to edit.

---

## VERDICT: FAIL

**Blocking issue:** HIGH-1 (FX5 differential coverage). The task is otherwise an unusually faithful research encoding — all 5 fixes hit the correct CODE-VERIFIED targets, no fabrication, all four stale-plan traps explicitly avoided, edge cases and brief-guard tests reflected, framing consistent, and the R4-vs-G1 Branch-A conflict resolved correctly. But FX5 as authored (a) drops research 02 §4.1-step-3/§6.2's mandate that ALL ~21 registered gate helpers carry a negative AND differential pair, authoring only the 5 helpers research gave concrete examples for; (b) is therefore not green-as-written (16 coverage cases — or ~16 drift-alarm cases — fail); and (c) introduces a non-research exemption escape-hatch whose practical use would cut real anti-gaming coverage to ~24% and weaken the gate, contradicting the ADDITIVE-ONLY/weaken-no-gate mandate. Under the RF "any unresolved gap regardless of severity = FAIL" rule, and independently on the HIGH's merits, the gate FAILs.

**Fix to flip to PASS:** reconcile FX5 per HIGH-1 remediation (A) author pairs for all registered helpers, or (B) narrow registry + drift-alarm to the 5 anchored helpers and demote the rest to documented residual-risk non-goals (matching research §4.3), dropping the ad-hoc exemption clause. Address MEDIUM-2 as part of whichever path is chosen. LOW-1/2/3 are advisory precision improvements.

**Severity tally:** HIGH 1 · MEDIUM 1 · LOW 3.

---
_End of report._
