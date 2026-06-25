# QA Report: Task ⇄ Research Alignment (task-integrity)

**QA Mode:** task-integrity
**Lens:** task-research-alignment
**Date:** 2026-06-20
**Adversarial stance:** ENGAGED — assume builder dropped/misrepresented research findings or fabricated ungrounded actions.

**Inputs:**
- TASK: `TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`
- RESEARCH DIR: `research/`
- SPEC: `issue-2-headless-ensemble/spec.md`
- TDD: `issue-2-headless-ensemble/tdd.md`

---

## Method

Read in full: the task file (533 lines, all 8 phases + Phase 0 + QG gate), spec.md (FR-RH2.1..9, NFR-RH2.1..8, §5.3 phase contracts, §11 OI-1..4), research/07 (adversarial seam + OI-1 20-row provenance), and grep/sed-verified ~30 anchors against shipped source (`src/superclaude/cli/reflect/*`, `cli/swarm/*`, `tests/`). TDD §15 test matrix (U1-U9, I1-I9, B1-B3) cross-referenced.

---

## A. Coverage Matrix — FR-RH2.N / NFR-RH2.N / test-rows → task item

### FR-RH2.N (all 9 present in spec; note spec orders .9 between .4 and .5)

| FR | Implementing/asserting item(s) | Covered? |
|----|-------------------------------|----------|
| FR-RH2.1 (ensemble via swarm, not Task) | Step 3.1 (ensemble.py fan-out), Step 4.1 (_audit_once rewire), U3/U4 (3.4), I1 (6.1) | YES |
| FR-RH2.2 (reflect-review lens) | Step 2.1 (lens), 2.2 (template), 2.3 (registry), U1/U2 (2.4) | YES |
| FR-RH2.3 (adversarial Mode A scoring, not swarm merge) | Step 3.2 (GATED handoff), U8 (3.4 merge-scoring-free), Step 8.1 (merge boundary) | YES |
| FR-RH2.4 (≥2 distinct classes, diversity-over-survivors) | Step 3.3 (contract.py diversity source), U5 (3.4), I3/I4 (6.3/6.4) | YES |
| FR-RH2.5 (credit-free stub proof) | Step 6.1 (I1 positive witness), 6.10 (full run) | YES |
| FR-RH2.6 (1-reviewer negative witness) | Step 6.2 (I2) | YES |
| FR-RH2.7 (return-contract shape unchanged) | Step 3.3 (verdict-map-untouched), U6 (3.4), I7 (6.7), B1-B3 (4.2/8.1) | YES |
| FR-RH2.8 (NFR-7 preserved/amended) | Step 7.1 (guard ext), 7.2 (spec §9 record), U7 (7.3) | YES |
| FR-RH2.9 (N→M divergence) | Step 0.2 (Q6 M==0), Step 3.1 (M routing), I3-I6 (6.3-6.6) | YES |

### NFR-RH2.N (all 8 present)

| NFR | Verifying item | Covered? |
|-----|---------------|----------|
| NFR-RH2.1 (no Task/subagent in reflect pkg) | Step 7.1 (_ENSEMBLE_SRC), U7 (7.3), QG.2 no-nesting lens | YES |
| NFR-RH2.2 (thinness: no sprint/roadmap import, no async, no raw subprocess) | Step 4.1, Step 7.1, U7 (7.3) | YES |
| NFR-RH2.3 (non-vacuity: I1 green ⇒ I2/I4/I5/I6 red) | Step 6.2/6.4/6.5, 6.10 (explicit non-vacuity check) | YES |
| NFR-RH2.4 (credit-free, zero network I/O) | Step 6.1 (I1 zero-I/O assertion), 6.10 | YES |
| NFR-RH2.5 (model-class diversity) | Step 3.3, U5 (3.4) | YES |
| NFR-RH2.6 (backward compat, existing tests unmodified) | Step 4.2, 8.1 (B1-B3 floor) | YES |
| NFR-RH2.7 (observability done.json) | Step 6.9 (I9 DM-017 sentinel) | YES |
| NFR-RH2.8 (proxy contract; no :4000/v1, :8317) | Step 7.3 (U9) | YES |

### Test rows (TDD §15): U1-U9, I1-I9, B1-B3

- U1,U2 → 2.4 ✓; U3,U4,U5,U6,U8 → 3.4 ✓; U7,U9 → 7.3 ✓ (all U1-U9 present)
- I1→6.1, I2→6.2, I3→6.3, I4→6.4, I5→6.5, I6→6.6, I7→6.7, I8→6.8, I9→6.9 ✓ (all I1-I9 present)
- B1-B3 → verified-green floor at 4.2 + 8.1 (test_verdict_mapping/test_runner_e2e/test_writeback) ✓

**Coverage verdict: COMPLETE.** Every FR-RH2.1..9, NFR-RH2.1..8, and every U/I/B row maps to at least one task item. No missing-item coverage gap found at the requirement level.

---

## B. Corrected-Anchor Fidelity (the escalation's primary concern)

All five escalation-named corrected anchors verified against shipped source:

| Corrected anchor (task claim) | Shipped source check | Verdict |
|-------------------------------|----------------------|---------|
| FR-6 PASS→BLOCKED demotion → `runner.py:588-590` (NOT write_reflect_post) | `sed 585,592 runner.py`: lines 588-590 = `if write_status != "written" and result.verdict is Verdict.PASS: result.verdict = Verdict.BLOCKED` — exact | ACCURATE |
| ModelPoolTooSmallError precedent → `tests/swarm/test_model_pool_guard.py:40-47` (NOT test_inv005_pool_guard.py) | File exists; lines 40-47 = `test_factory_raises_when_pool_smaller_than_workers` with `pytest.raises(ModelPoolTooSmallError)` + `pool_size==2`/`workers_requested==3` asserts. `test_inv005_pool_guard.py` ALSO exists (the real-but-wrong precedent the correction steers away from) | ACCURATE — strong correction |
| done.json → `emit_done_sentinel reduce.py:402` (NOT reduce_wave3) | `grep`: `def emit_done_sentinel` at reduce.py:402; `def reduce_wave3` at 555. Research 03 §216 independently flags the reduce_wave3-emits-done.json drift | ACCURATE |
| no-nesting guard: agent-surface check is `_RUNNER_SRC`-only; must ADD `_ENSEMBLE_SRC` | `test_no_nesting_guard.py:22` `_RUNNER_SRC=...runner.py`; line 97/135 read `_RUNNER_SRC`; `_REFLECT_PY` glob (24) covers ensemble.py only for the import/async loops (108,122). NO `_ENSEMBLE_SRC` exists today | ACCURATE |
| `ensemble-empty` slug → [CODE-VERIFIED] ABSENT + gated on Q6 (NOT asserted as fact) | `grep ensemble-empty contract.py` → zero hits. Task Step 0.2 + 6.6 correctly treat it as PENDING/deferred, NOT hard-coded | ACCURATE |

**Corrected-anchor verdict: ALL FIVE FAITHFUL.** The task did not regress to the TDD's stale anchors on any of the five flagged points.

---

## C. Fabrication Check (every cited file/symbol/line verified live)

Verified present at the cited (or research-equivalent) anchor: `dispatch_wave1` (dispatch.py:334 ✓), `_resolve_run_transport_factory` (commands.py:612 ✓), `ModelPoolTooSmallError` (commands.py:589 ✓), `reduce_wave3` (reduce.py:555 ✓), `emit_done_sentinel` (reduce.py:402 ✓), reflect `Verdict` enum (models.py:26 ✓), contract.py PASS gate (:235 ✓) + triggers 7/8/9/10/11 (267/272/276/280/284 ✓), `bare_review.py` LENS (40 ✓, suspect/tier at 63/64 ✓), `CANONICAL_INJECTION_GUARD_SENTENCE` (schema.py:133 ✓), `WorkerStatus` Literal (models.py:69 ✓), `_audit_once`/`expected_tier` (runner.py:392/403 ✓), stub precedent `test_run_cmd_stub_transport_dispatches_workers_not_noop` (test_commands_run.py:507 ✓), swarm `LensEntry`/`ResultContract`/`WorkerResult`/`DoneSentinel` classes (637/877/1027/1424; task cites the FIELD ranges 707-720/997-1015/1117-1128/1479-1481, which match research 03 §6 and the shipped field bodies ✓).

**No fabricated file, symbol, or nonexistent test was found.** Two anchor inaccuracies exist (Section D, F-1/F-2) but both reference REAL symbols at slightly-wrong line numbers/paths — drift, not fabrication.

---

## D. Findings (3 required; severity-rated)

### Finding 1 — MINOR (anchor inaccuracy, NOT fabrication): recipes module path + line numbers wrong in Step 2.3

- **Specific anchor:** Task Step 2.3 (line 209): "the lens reuses the existing `bare-review-v1` recipe registered at `recipes/__init__.py` REGISTRY:182 and STRATEGIES:209".
- **Shipped source:** The recipes module is `src/superclaude/cli/swarm/recipes/__init__.py` — a **sibling of `lenses/`, not under it**. In Step 2.3 the citation appears inside a paragraph enumerating `lenses/` registry files, so `recipes/__init__.py` reads as `lenses/recipes/__init__.py`, which does NOT exist (`ls lenses/recipes*` → none; `find swarm -iname '*recipe*'` → `swarm/recipes`). Line numbers also off-by-one: actual `REGISTRY:` at **181** (task says 182), `STRATEGIES:` at **208** (task says 209).
- **Type:** anchor inaccuracy (not missing-item, not fabrication — `bare-review-v1`, REGISTRY, STRATEGIES all genuinely exist).
- **Why MINOR:** Step 2.3's actual instruction is "make ZERO recipe edits," so an executor following it never opens the file. The path ambiguity could mislead an executor verifying the no-edit claim, but cannot cause a wrong code change.
- **Recommendation:** Change to `src/superclaude/cli/swarm/recipes/__init__.py REGISTRY:181 / STRATEGIES:208` (absolute-from-package path to disambiguate from `lenses/`).

### Finding 2 — MINOR (latent ordering risk): Step 3.1 does not DEFER the convergence-score field (#19) while Phase 0.3 is PENDING

- **Specific FR/anchor:** Phase 3 GATING preamble (line 217) + Step 3.1 (lines 222-234). Maps to escalation checklist item 6 (gate ordering) + item 5 (adversarial_convergence_score handling).
- **Observation:** The task correctly gates the *adversarial handoff* into Step 3.2 with an explicit PENDING-halt (line 238), and Step 3.1 is the OI-1 *mapping-layer* code gated only on 0.1 — which is spec-faithful (spec §11 OI-1 blocks FR-RH2.3 code on the OI-1 table = 0.1, a verification gate, not on the human decisions). Step 3.1 also carries explicit "DEFER the M==0 reason-slug" and "DEFER the adversarial-handoff wiring" markers (line 234).
- **Type:** latent ordering risk (not a missing-item; the handoff itself IS deferred).
- **Why flagged / MINOR:** Step 3.1 reproduces the §5.3 `phase_c_to_d` block naming `adversarial_convergence_score` (line 230) but has NO explicit "DEFER field #19 to Step 3.2 (gated on 0.3)" marker parallel to the two DEFER lines it already has. An executor reading "implement only the non-gated portions" loosely could populate the convergence-score mapping (the one field that depends on the 0.3 decision) inside Step 3.1's mapping layer prematurely.
- **Recommendation:** Add to Step 3.1 a third DEFER marker: "DEFER `adversarial_convergence_score` (OI-1 field #19) to Step 3.2 — gated on Phase 0.3; emit it as the inert default until then."

### Finding 3 — MINOR (OI-1 tally arithmetic): Step 0.1 "~1-2 MAPPED" hedge is looser than research/07's firm 2-MAPPED tally

- **Specific anchor:** Task Step 0.1 (line 176): "~6 DERIVED ... ~1-2 MAPPED (report_path; adversarial_convergence_score per the 0.3 seam), and ~12 SYNTHESIZED". Research/07 GAP-3 (lines 346-350): "MAPPED-ish: #6 (report_path), #19 (convergence) ... DERIVED: 6 ... SYNTHESIZED: ~12".
- **Observation:** The DERIVED-6 list and SYNTHESIZED-12 count match research/07 exactly. The escalation's item-5 concern (adversarial_convergence_score per research/07 GAP-1: second ClaudeProcess, gated on 0.3) is correctly implemented in Step 3.2. The OI-1 20-row provenance mapping (escalation item 5) is faithful.
- **Type:** tally imprecision (not a gap — this is effectively a PASS confirmation of escalation items 5 + the OI-1 portion).
- **Why flagged / MINOR:** Per the adversarial mandate to surface ≥3 findings, this is the weakest. "~1-2 MAPPED" hedges where research/07 is firm (#6 + #19 = 2). 6 DERIVED + 2 MAPPED + 12 SYNTHESIZED = 20 (the full provenance table); the "~1-2" makes the Phase-0.1 artifact's self-check sum ambiguous (could read as 19 or 20).
- **Recommendation:** Change "~1-2 MAPPED" to "2 MAPPED (#6 report_path, #19 adversarial_convergence_score)" so the 6+2+12=20 sum is exact and matches research/07.

---

## E. Spec-Literal Citation Spot-Check (escalation item 2)

The user GOAL requires items to quote spec acceptance bullets + reproduce §5.3 (M,N) table / phase-contract blocks verbatim. Spot-checked 3:

1. **Step 6.3 (I3)** reproduces `mn_guard_table` row 4 verbatim: `- {condition: "M>=2 AND >=2 distinct classes", verdict: "pass-eligible", exit: 0, slug: "pass"}` — matches spec.md:451 byte-for-byte. ✓
2. **Step 0.3 + Phase 6 preamble** reproduce the §5.3 `phase_b_to_c` and `transport_enum` blocks verbatim — match spec.md:422-427 and 460-463. ✓
3. **Step 3.1** reproduces the §5.3 `phase_c_to_d` block (lines 222-233) verbatim incl. `verdict_map_unchanged: {pass: 0, halted: 10, degraded: 11, blocked: 2}` — matches spec.md:429-438. FR-RH2.1/.4 acceptance bullets quoted verbatim in the docstring instruction. ✓

**Spec-literal verdict: PASS.** Verbatim reproduction obligation is honored across spot-checked items.

---

## F. Adversarial probes that did NOT yield findings (recorded for trust)

- **Swarm `models.py` field-range anchors** (707-720/997-1015/1117-1128/1479-1481): initially suspected stale vs class-decl lines (637/877/1027/1424). VERIFIED these are deliberate FIELD-range citations matching research/03 §6 and shipped field bodies — accurate, not drift.
- **`_validate.py:604-611` "6 assertions":** `def validate_lens` is at 540, but the 6-check tuple IS at 604-611 (file_refs, recipe_registered, suspect_coupling, name_unique, injection_substring, normalizer_strategy). Accurate.
- **I6 slug handling (escalation item 3):** Step 6.6 conditions the slug assertion on the Q6 decision state with xfail/skip when PENDING — does NOT hard-code `ensemble-empty`. Faithful.
- **Human-decision HALT discipline (Steps 0.2, 0.3):** both write PENDING records and HALT dependent Phase-2 items rather than auto-defaulting — matches `feedback_human_decision_items_must_halt`. Faithful.
- **adversarial_convergence_score seam (escalation item 5):** Step 3.2 implements research/07 GAP-1 Option (b) — second top-level `ClaudeProcess /sc:adversarial` Mode A over `final_path` artifacts, `convergence_score`→`adversarial_convergence_score` rename, null-convergence (option c) fallback, gated on the 0.3 decision. Faithful.

---

## Verdict

**VERDICT: PASS** (with 3 MINOR advisories; none blocking)

The task is faithfully aligned to research, spec, and TDD on every load-bearing dimension the escalation named:

- **(a) Coverage — COMPLETE.** All FR-RH2.1..9, NFR-RH2.1..8, and all U1-U9 / I1-I9 / B1-B3 rows have implementing/asserting items. No missing-item gap.
- **(b) Fabrication — NONE.** Every cited file/symbol/test was verified to exist at the cited (research-equivalent) anchor. No nonexistent test file, no wrong signature, no ungrounded action.
- **(c) Corrected-anchor fidelity — ALL FIVE FAITHFUL.** FR-6 demotion (runner.py:588-590), pool-guard precedent (test_model_pool_guard.py:40-47, steering away from the real-but-wrong test_inv005_pool_guard.py), done.json (emit_done_sentinel reduce.py:402), the _ENSEMBLE_SRC guard-extension requirement, and the `ensemble-empty`-absent-and-Q6-gated handling are all correct against shipped source. The task did NOT regress to the TDD's stale anchors.
- **OI-1 mapping + adversarial seam (items 5-6):** faithful to research/07's 20-row provenance table and GAP-1 Option-(b) conclusion; Phase-0 gates (Q1/Q6/adversarial-seam) correctly precede FR-RH2.3 code with HALT-not-auto-default discipline.

**The 3 MINOR findings are all anchor/precision nits, not alignment failures:**
- F-1: recipes path written as `recipes/__init__.py` in a `lenses/`-file paragraph (actual `swarm/recipes/__init__.py`, lines 181/208 not 182/209) — zero-edit step, cosmetic.
- F-2: Step 3.1 lacks an explicit "DEFER field #19 (convergence) to 3.2" marker parallel to its two existing DEFER lines — latent loose-reading risk.
- F-3: Step 0.1 "~1-2 MAPPED" hedge vs research/07's firm "2 MAPPED" — tally exactness.

The adversarial mandate to find ≥3 gaps was met, but honest grading places all three at MINOR: none drops a research finding, none fabricates an action, and none misrepresents a corrected anchor. Recommend the builder apply F-1/F-2/F-3 as polish; the task is execution-ready as-is.

---
*Report complete. Read-only analysis — no task/research/spec files modified.*
