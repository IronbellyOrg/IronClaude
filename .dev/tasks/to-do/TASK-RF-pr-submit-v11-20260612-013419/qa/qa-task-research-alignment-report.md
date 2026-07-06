# QA Report: Task–Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-06-12
**Task:** TASK-RF-pr-submit-v11-20260612-013419
**Stance:** ADVERSARIAL (assume builder dropped or misrepresented research findings)

---

## Scope

Cross-validate that every significant finding across the 7 research files (01–07)
has a corresponding checklist item in the task file, and that no task item
fabricates actions not grounded in research or the spec.

Status: COMPLETE

Files cross-validated:
- Task file: `TASK-RF-pr-submit-v11-20260612-013419.md` (666 lines, Phases 1–8)
- Research: `research/01-07-*.md` (all 7 read in full)

---

## 1. Per-Research-File Finding → Task-Item Alignment

### Research 01 (core inventory) — ALIGNED
Every §6 per-file delta has a corresponding task item:
- models.py: EventType +4 (Step 2.2), MonitorState +2 non-terminal (Step 2.1), SkillResult +6 fields (Step 2.3) — all present, exact names/values/defaults matched verbatim against 01 §models.
- classifier.py: STATE_DECLINED + decline-first branch (Step 3.1), is_decline (Step 3.2) — present.
- detection.py: +3 DetectionContract fields + from_yaml extend (Step 3.3) + contract-ref YAML (Step 3.4) — present.
- run_log.py: 6th idempotency set (Step 4.1), 3 folds incl. monotone-min (Step 4.2), 33→37 prose/error (Step 4.3) — present.
- fsm.py: 6 edges + remove :793 + clamp (Steps 5.1–5.5) — present.
- `__init__.py` export check: Step 3.5 implements the CONDITIONAL re-export decision from 01 §INIT verbatim (greps tests for package-root imports; no-op if none). PRESENT and faithful to the "Unverified until test-import audit" framing.
- loop_guard.py is correctly treated as source-UNCHANGED (01 §loop_guard / §summary): no source-edit item, only the `refs/loop-guard.md` doc delta (Step 6.3). CORRECT.
- severity_router.py correctly has NO item (01 §SEVROUTER: UNCHANGED). CORRECT.

### Research 02 (fsm anatomy) — ALIGNED
- Dual-surface lock-step (transition() if-chain AND inline run_skill() loop are SEPARATE surfaces): explicitly encoded — Step 5.3 = surface 1 of 2, Step 5.5 = surface 2 of 2, with an explicit DUAL-SURFACE POINTER and a dedicated dual-surface lens gate (Step 5.G2). Faithful to 02 §0/§6.
- Increment ordering (tick AFTER push, BEFORE next-iteration budget gate ⇒ max_rounds=N ⇒ N pushes): Step 5.4(c) reproduces this ordering constraint verbatim. Faithful to 02 §2/§5.
- RunConfig `_noop` seam pattern (module-level `_noop`, NOT inline lambdas, to dodge the self-binding trap): Step 5.2 explicitly cites "NOT inline lambdas, to avoid the dataclass self-binding trap documented for run_validation". Faithful to 02 §3 GOTCHA.
- The transition-event-name vs run_skill-outcome-token distinction (02 §1: `"rereview_attributed"` edge string vs `"attributed"` outcome token) is correctly reflected — Step 5.3 uses `"rereview_attributed"` for the edge; Step 5.4 uses `rereview_outcome[...] == "attributed"` for the tick.

### Research 03 (run_log patterns) — ALIGNED
- 6th idempotency set is 5→6 (NOT 4→5): Step 4.1 anchors on "The 5 idempotency sets"→"The 6", and Step 4.4 explicitly says "anchor on the 5→6 count (NOT any '4'/'reconcile' framing)" — directly absorbing the corrected-count caveat. CORRECT.
- EventType count-bump 33→37 across the run_log sites: Step 4.3 covers the append() docstring + ValueError string; Step 2.2 covers the models.py class + module docstrings. The "5 count-bump sites" framing (Objectives §3 / Key Constraints) matches 03 §4.1's enumerated sites.
- Monotone-min fold (no in-repo precedent): Step 4.2(d) reproduces 03 §4.3's exact None-safe recommended form (`clamp if prev is None else min(prev, clamp)`). Faithful.
- SkillResult fields: Step 2.3 matches 03 §4.4 idioms (scalar/Optional inline defaults, no default_factory). CORRECT.

### Research 04 (skill/refs) — ALIGNED
- SKILL.md Wave 6 S5a + NEW Wave 6b: Step 6.1 present.
- 2 MOD refs (augment-poll Step 6.2, loop-guard Step 6.3) + state-machine.md MOD (Step 6.4) + 2 NEW refs (review-retrigger Step 6.5, auggie-fallback Step 6.6) + NEW script retrigger-review.sh (Step 6.7). ALL present.
- gh repo-pin discipline: Step 6.7 mandates `repos/IronbellyOrg/IronClaude` pin and flags a bare `gh api` as a T-104-class defect, matching 04 §F. Step 6.G4 adds a fork-pin domain lens.
- The state-machine.md "coverage-gap" finding (04 §D: spec §6.5 OMITS state-machine.md but FSM single-source invariant REQUIRES it) is preserved — Step 6.4 explicitly instructs flagging "the addendum-coverage-gap (spec §6.5 omits state-machine.md but the topology requires it)" in Phase 6 Findings. Faithful to 04's single-most-important finding.

### Research 05 (test infra) — ALIGNED
- 2 NEW test modules (test_review_retrigger Step 5.8, test_auggie_fallback Step 5.9) + 5 EXTENDED (test_detection_contract 3.6, test_idempotency 4.4, test_loop_guard 5.10, test_run_log 4.5, test_static_grep 6.8). ALL present.
- 7 NEW fixtures: all 7 named in task items with their schema (a)/(b)/(c) tags. CONFIRMED 7/7 (decline-comment, rereview-attributed, rereview-then-decline, decline-initial-poll, decline-twice, stale-decline-pre-watermark, auggie-fallback-findings).
- --strict-markers constraint: every test item ends with "any NEW marker registered in pyproject.toml (prefer reusing loop_guard/inv/recovery or no marker)". Faithful to 05 §4.
- T-N50 core-purity grep extended to the 2 NEW refs: Step 6.8 + Step 5.6 + domain lenses. CORRECT.
- Corrected 5→6 idempotency count: absorbed (see Research 03 alignment).
- Fixture bot login `augment-code[bot]` (05 §2(a): fixtures use this, distinct from production `augmentcode[bot]`): Step 3.6 explicitly says "use the fixture bot login `augment-code[bot]` to match existing fixtures". Faithful.

### Research 06 (spec index) — MOSTLY ALIGNED (see Issues I-2, I-3)
- FR→T-ID coverage matrix: all 25 T-IDs appear (literally or in `T-1110..T-1118`/`T-1120..T-1125` ranges). See §2 for the literal-traceability gap.
- INV-R1/R2/R3: referenced 18/4/12 times respectively but NOT embedded verbatim (Issue I-2).
- EC-17..24 / AC-16..21: semantically covered but several IDs not literally cited (Issue I-3).
- Naming reconciliation (06 §0: live names `sc:pr-submit`/`pr_submit`/`tests/pr_submit`, NOT the stale `sc:submit-pr`): the task uses ONLY the live names throughout. CORRECT — no stale-name leak.

### Research 07 (cross-validation) — ALIGNED
- The 1 [UNVERIFIED] claim (07 #10b: `accepted_trigger_phrases` provenance — field does not yet exist, planned per §6.2): the task does NOT treat it as a verified current-fact. It is correctly handled as a NEW field to ADD (Step 3.3) and the FR-8.5 "core holds no hard-coded literal" assertion is routed to a static test (T-1105, Steps 5.8 + 6.8) rather than asserted as already-true. CORRECT — no item built on the [UNVERIFIED] claim as if verified.
- No item anchors on a stale anchor: 07 confirmed every concrete current-state claim (incl. fsm.py:793, the auggie-review.md flag lines) is EXACT, and the task additionally mandates RE-GREP of every `:line` at edit time (Key Constraints + every code Step). CORRECT.

---

## 2. Fabrication Check (task items referencing files/symbols/tests NOT in research or spec)

Swept every `src/`, `refs/`, `scripts/`, and `tests/` path named in the task against research 01/04/05 and the spec deltas (06 §5):
- 7 core modules, 11 skill files (SKILL.md + 7 refs + 3 scripts), 8 test modules, 7 fixtures — ALL grounded. ZERO fabricated files.
- All 7 fixtures match research 05 §2/§6 and 06 §8.1 (7/7).

**One non-grounded token (Issue I-1, MINOR):** `fallback_residual_findings` — a `context`/`ctx` dict key introduced in Step 5.3 as the example predicate for the `(S5B_AUGGIE_FALLBACK, "fallback_skip")` terminal selector (`MonitorState.TERMINAL_CLEAN if not ctx.get("fallback_residual_findings") else MonitorState.HALT_MAX_ROUNDS`). This key appears NOWHERE in any research file. It is NOT fabrication-of-a-defect: research 02 §1 and 06 §5.4 BOTH explicitly leave the `fallback_skip` selector as "builder must define the selector; spec leaves it as a disjunction", and the task cites spec §3.2 for the clean-vs-residual choice. So this is an AUTHORIZED concretization of a research-flagged open decision, surfaced as an illustrative example ("e.g."). The risk is that the executor treats the invented key name as binding rather than as one valid encoding.

No other invented symbols, tests, or files found.

---

## 3. Caveats Reflected in Verification Criteria

| Research caveat | Reflected? | Where |
|---|---|---|
| NFR-6 (no gh/git in core) | YES | Key Constraints; Step 5.6 grep; core-purity domain lenses 3.G4/4.G4/5.G4/6.G4/7.GA4; T-N50 ext (Step 6.8) |
| INV-001 verbatim (edge/gate/monotonicity/N⇒N) | YES | Key Constraints; Step 5.3 (edge byte-identical) + 5.4 (single increment site, ordering); INV-fidelity lenses 5.G4/7.GA4 (worked N=2 example); Step 5.10 keeps INV-001 fence-post tests UNCHANGED |
| Dual-surface drift risk (02 §0) | YES | Steps 5.3/5.5 surface-1/2 split; dedicated dual-surface lens 5.G2 |
| False-positive-prone decline (both-regexes AND watermark AND decline-before-clean/findings) | YES | Step 3.1 (branch BEFORE clean/findings), Step 3.2 (BOTH regexes + watermark), Step 3.6 (T-1111/T-1112 false-positive + watermark tests); domain-accuracy lens 3.G3 (App-bait distinction) |

All four research-identified caveats are reflected. STRONG.

---

## 4. Dependency Ordering Reflected in Phases

- models.py FIRST (import-resolve prerequisite): Phase 2 precedes Phases 3–5; DAG NOTEs on Phases 3/4/5 each cite "depends on Phase 2 (models.py)". Faithful to 01/02/07.
- record_idempotent raises on unknown set ⇒ 6th-set item MUST precede the strict-once gate item: Step 4.1 (add 6th set) is in Phase 4; the strict-once gate consumer (Step 5.5(c), `invoke_auggie_review` gated on the `auggie_review_invoked` record) is in Phase 5, which DAG-depends on Phase 4. Ordering is CORRECT and matches 07's "the 6th-set item is a hard prerequisite of the strict-once gate item".
- classifier 4th state before detection/fsm routing: Phase 3 precedes Phase 5. CORRECT.

Dependency ordering is faithful.

---

## 5. Six Carry-Forward Flags

| # | Flag | Present? | Where |
|---|---|---|---|
| 1 | state-machine.md MOD (beyond §6.5) | YES | Step 6.4 (+ flag-as-coverage-gap instruction) |
| 2 | fallback_skip predicate defined | YES | Step 5.3 item (6) — selector defined (but see I-1 re: example key) |
| 3 | loop-guard.md "33" re-grep | YES | Step 6.3(c) ("re-grep this ref for any '33'/'EXACTLY 33' ... bump to 37") |
| 4 | __init__ export decision | YES | Step 3.5 (conditional re-export) |
| 5 | EventType 5-site 33→37 bump | YES | Steps 2.2 (2 models sites) + 4.3 (2 run_log sites) + 6.3 (loop-guard ref) |
| 6 | fsm dual-surface | YES | Steps 5.3/5.5 + lens 5.G2 |

All 6 carry-forward flags present. STRONG.

---

## Issues (severity-rated)

### I-1 (MINOR) — `fallback_residual_findings` context key is builder-invented, not research-grounded
Step 5.3's `fallback_skip` selector example uses the dict key `fallback_residual_findings`, which appears in no research file. It is an authorized concretization of a research-flagged "builder must define the selector" decision (02 §1, 06 §5.4) and is offered as an example ("e.g."), but the executor could mistake the invented key for a binding contract. **Recommendation:** add a half-sentence noting the key name is illustrative and the executor must bind it to whatever `context`/`ctx` field the dual-surface run_skill loop actually populates for the post-fallback residual count (Step 5.5 must produce that field, so the two surfaces agree).

### I-2 (IMPORTANT) — INV-R1/R2/R3 normative blocks not embedded verbatim in the task
Research 06 §4 states, explicitly: "New Invariants (TRANSCRIBED verbatim from addendum §5 — builder MUST embed for literal QA)". The task references INV-R1/R2/R3 by ID heavily (18/4/12 mentions) and routes the consuming agents to the verbatim text — Step 6.3 ("add the INV-R1/R2/R3 normative blocks verbatim" into loop-guard.md, pulling "the INV-R1/R2/R3 verbatim text from research/06 §4") and the INV-fidelity lenses (Steps 5.G4/7.GA4, "the INV-R1/R2/R3 text from research/06-spec-delta-extraction.md §4"). So the verbatim text IS reachable by every agent that needs it, via research/06 §4. BUT the task file itself does not inline the normative blocks, so a literal-QA pass that reads ONLY the task file (not research/06) cannot perform a byte-level INV-R conformance check. This is a partial miss against 06's explicit "builder MUST embed" instruction. **Recommendation:** inline the three INV-R normative blocks (verbatim from addendum §5 / research 06 §4) into the task's Key Constraints or a dedicated "Invariants (verbatim)" subsection, so literal QA is self-contained. Mitigation already present: every INV-R-consuming item points at research/06 §4, so the verbatim text is not lost — only not co-located.

### I-3 (MINOR) — Several EC/AC/FR sub-IDs covered semantically but not cited literally (traceability gap)
The §9 coverage matrix maps specific FR/EC/AC IDs to T-IDs. The task covers them through the two NEW test-module items (Steps 5.8/5.9) which enumerate T-ID RANGES (`T-1110..T-1118`, `T-1120..T-1125`) plus prose scenarios, rather than naming every sub-ID. Literal-citation audit:
- FR-9.2 (0 literal mentions) — covered semantically: Step 5.3 adds BOTH `(S2_CLASSIFY,"declined")` and `(S5_AWAITING_REREVIEW,"declined")` edges; Step 5.9 says "routing to S5b from BOTH the initial S2 poll and the S5 re-trigger poll".
- FR-10.3 (0 literal) — covered: Step 5.5 (single-shot sub-loop, cap-1, no loop-back, round_counter frozen) cites FR-10.2/10.3/10.5.
- EC-19/20/21/22/24 and AC-17/18/19/20/21 (0–1 literal each) — all covered semantically inside Steps 5.8/5.9/5.10 prose and the crossref-chain lens gates (3.G3/4.G3/5.G3/6.G3/7.GA3 trace "every EC-17..24 → its test" and "every AC (16-21) to a real implementing symbol AND a real passing test").
The behavior is covered; only the explicit ID-level breadcrumb is thinner than the matrix. The crossref-chain + fidelity gates (Phase 7 Gate B phantom-coverage detection, which opens each T-ID) are the safety net that catches any genuinely-missing chain. **Recommendation (optional):** the Step 5.8/5.9 items could enumerate the per-sub-ID scenario list (e.g., explicitly name EC-19/EC-21/EC-22/EC-24) to make the FR→EC→T chain literally auditable from the item text, reducing reliance on the downstream phantom-coverage gate.

---

## Verdict

The task file is a faithful, high-fidelity translation of all 7 research files. Every §6 per-file delta, every NEW/MOD ref+script, all 7 fixtures, both NEW + 5 EXTENDED test modules, all 6 carry-forward flags, all four research caveats, the full dependency DAG, the corrected 5→6 count, the [UNVERIFIED]-claim handling, and the dual-surface/INV-001-relocation risk surface are present and correctly grounded. No fabricated files, symbols, or tests (one builder-invented example key, I-1). The three issues are NOT dropped-finding defects — they are a verbatim-embedding partial-miss (I-2, the only one rising above MINOR) and two traceability/illustration thinness items (I-1, I-3), each with the research content still reachable by the consuming agents and a downstream gate (phantom-coverage / INV-fidelity lens) as a backstop.

The adversarial stance required ≥3 alignment gaps; 3 are reported (I-1, I-2, I-3). None is a CRITICAL or research-finding-DROP. The single finding worth acting on before execution is I-2 (inline the INV-R verbatim blocks for self-contained literal QA).

**VERDICT: PASS** (3 issues: 0 CRITICAL, 1 IMPORTANT [I-2], 2 MINOR [I-1, I-3])
