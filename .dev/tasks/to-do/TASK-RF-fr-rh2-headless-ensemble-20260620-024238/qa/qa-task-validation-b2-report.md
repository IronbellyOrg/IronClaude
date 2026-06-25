# QA Report — Task Integrity (LENS: b2-self-containment)

**Topic:** FR-RH2 headless ensemble MDTM task file
**Date:** 2026-06-20
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix authorization:** false (report-only)
**Task file:** TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md

---

## Scope

Verifying every `- [ ]` checklist item is SELF-CONTAINED per MDTM B2:
context + action + output + verification + completion gate. An item that says
"see above" or relies on un-restated prior context FAILS.

## Method

Read the entire task file (533 lines). Enumerated every `- [ ]` checklist item
(33 items total across Phases 1, 0, 2, 3, 4, 5, 6, 7, 8, QA Gate, Post-Completion).
For each spot-checked item I checked all 5 B2 components: Context (restated, not
"see above"), Action (concrete), Output (explicit path), Verification (measurable),
Completion gate ("mark this item as complete"). Cross-references to "above" / other
items / "the top of this section" are the primary B2 violation surface for this lens.

Tool engagement: Read: 5 (task file in 4 page reads + report re-read).

---

## B2 Self-Containment Findings

### The dominant pattern (affects all 7 Phase-6 I-row items: 6.3, 6.4, 6.5, 6.6, 6.8)

The Phase-6 I-row items (Steps 6.3–6.6) open with **"Read the §5.3 `mn_guard_table`
row N reproduced at the top of this Phase 6 section"**. This is a cross-reference to
a block that lives in the Phase-6 _section preamble_ (lines 297–320), NOT inside the
item. Per B2, an item must restate the context it depends on. HOWEVER — each of these
items then **reproduces the specific matching row VERBATIM in its own body** ("reproducing
the matching `mn_guard_table` row VERBATIM in the test docstring: `  - {condition: ...}`").
So the load-bearing datum (the one row the item needs) IS restated inside the item.
The "reproduced at the top of this section" phrase is a locator, not the sole source.
**Net: these items are B2-COMPLIANT** because the row they act on is embedded. This is
the most important judgment call in the review and I am flagging it explicitly so it is
auditable: had the items said only "use the row from the top of this section" without
re-embedding, they would FAIL. They re-embed. PASS.

### Issue 1 — Step 6.2 (I2) depends on un-restated prior-item assertions [IMPORTANT]

**Item:** Step 6.2 (line 328). **Missing component:** self-contained Context.
The item says: *"Read the I1 positive-witness test ... (Step 6.1) to identify the exact
positive assertions, then add test I2 (negative witness) ... that the SAME assertions
used in the I1 positive test FAIL."* The item's correctness depends on "the exact
positive assertions" which live in Step 6.1 and are NOT restated here. It partially
mitigates by listing *"at least the `tier_reached==2`/`reviewer_count>=2`/
`merge_method!=single-reviewer-fallback` conditions"* — so the three core assertions
ARE named inline. Because the three assertions are named, this is IMPORTANT not CRITICAL,
but the phrase "the SAME assertions used in the I1 positive test" still forces a reader
back to Step 6.1 to know whether the named three are exhaustive. Fix: state "the I1
positive assertions are exactly: tier_reached==2, merge_method!=single-reviewer-fallback,
reviewer_count>=2, t2_model_class_diversity==full" inline so I2 is actionable without
opening 6.1.

### Issue 2 — Steps 6.4 / 6.5 reference "the I1 positive assertions FAIL here" without restating them [IMPORTANT]

**Items:** Step 6.4 (line 336), Step 6.5 (line 340). **Missing component:** self-contained
Context for the non-vacuity assertion. Both say *"that the I1 positive assertions FAIL here
(NFR-RH2.3 non-vacuity)"* but neither enumerates what "the I1 positive assertions" are.
Step 6.4 does name `t2_model_class_diversity != "full"`; Step 6.5 names
`merge_method == "single-reviewer-fallback"` — but the phrase "the I1 positive assertions"
as the thing that must FAIL is an un-restated cross-item dependency. Same fix as Issue 1:
embed the canonical I1 assertion list. Severity IMPORTANT (the divergence-specific
assertion IS embedded; only the cross-vacuity check leans on 6.1).

### Issue 3 — Step 2.3 / Step 3.x / Step 4.1 depend on "(created in Step N)" artifacts without restating their interface [MINOR]

**Items:** Step 2.3 (line 209, "read the new lens module ... created in Step 2.1 to confirm
the exported `LENS` symbol name"), Step 3.1→3.2 (3.2 reads `ensemble.py` "(Step 3.1)"),
Step 4.1 ("the new driver ... (Phase 3)"). These are legitimate intra-task data-flow
reads (the item tells you to Read the produced file), which is the CORRECT B2 pattern for
consuming a prior artifact — the file path is given and the item instructs a fresh Read.
This is NOT a "see above" violation; it is proper handoff. Listed as MINOR only because
"(Phase 3)" in Step 4.1 is vaguer than a path; it should say `src/superclaude/cli/reflect/ensemble.py`
(which it does, earlier in the same sentence). No fix strictly required.

### Issue 4 — Many VERIFICATION items reuse "the templated format in the ### Phase 2 Findings section" for non-Phase-2 phases [MINOR]

**Items:** Steps 3.3, 3.4, 4.1, 4.2, 5.1, 5.2, 5.3, 5.4, 6.1–6.10, 7.1, 7.2, 7.3, 8.1, 8.2 all
say *"log ... in the ### Phase 2 Findings section"* even though they belong to Phases 3–8.
This is a copy-paste artifact: a Phase-5 blocker logged into a "Phase 2 Findings" heading
is a self-containment defect because the named target section does not match the item's phase
(and may not exist with that heading). The completion-gate's "where to write the record" is
a B2 component; pointing it at the wrong section undermines actionability. Fix: each item's
log-target should be its own phase's Findings section (### Phase 3 Findings, etc.), or a single
canonical ### Findings section. Severity MINOR (the record still lands SOMEWHERE; trace is muddied).

### Issue 5 — Step 0.1 is an oversized multi-clause item that strains "single self-contained paragraph" [IMPORTANT]

**Item:** Step 0.1 (line 176). The item is ~30 lines of embedded content: read spec §11 +
research 07 + models.py (6 distinct line anchors) + contract.py (8 distinct triggers) + run
grep + produce a 5-column artifact with a tally split (~6 DERIVED / ~1-2 MAPPED / ~12
SYNTHESIZED) + cite 3 verbatim bullets. While it IS self-contained (every datum is embedded),
it bundles validation of TWO source files, a grep sweep, AND artifact authoring into one
checkbox. Under B2/atomicity this is a granularity strain: a reader cannot execute it without
scrolling, and the verification ("every provenance claim verified against the cited line") is
not a single runnable assertion. Severity IMPORTANT — flagged for the b2 lens because an
item this large erodes the "could someone execute this without scrolling?" property even
though no individual component is missing.

### Phase-0 gate items (checklist focus item 8) — VERDICT: COMPLIANT

Steps 0.2 and 0.3 (the two human-decision HALT gates) each carry full self-contained context:
the option text (Option A vs B / Option (a)(b)(c)) reproduced inline, the spec citation
(FR-RH2.9 + §5.3 row 1 / FR-RH2.3 + §5.3 phase_b_to_c VERBATIM), the explicit HALT instruction
(**THIS ITEM MUST HALT**), and the exact PENDING-record write path
(`phase-outputs/decisions/q6-mzero-slug-decision.md` / `adversarial-seam-decision.md`).
The §5.3 blocks are reproduced VERBATIM inside the item, not referenced. These are model
B2 items. PASS.

### Checklist focus item 7 (ensemble-empty not asserted as fact) — VERDICT: COMPLIANT

Step 6.6 (I6) correctly does NOT treat `ensemble-empty` as established fact: it asserts only
blocked/exit2 unconditionally and routes the slug sub-assertion through the resolved Q6 decision
("IF it still reads `**DECISION: PENDING**`, assert ONLY blocked/exit2 and add a
`pytest.mark.xfail`/skip note ... do NOT hard-code `ensemble-empty` as fact"). Step 3.1 (line 234)
likewise DEFERS the M==0 reason-slug to the Q6 record. The Open Questions section (line 455) tags
it `[CODE-VERIFIED] ABSENT`. This gating is correctly self-contained. PASS.

### QA-gate agent-spawn items (checklist focus item 3) — VERDICT: COMPLIANT

Steps QG.2 / QG.3 (the 6 lens-agent spawns, lines 406–418) each embed the FULL lens prompt:
which files the agent must read, the exact verification target (per-FR/NFR / NFR-7 tokens /
backward-compat / ensemble-formation / OI-1 / M-N), the adversarial framing string
("Assume ... at least 10 errors ... Find them."), the `fix_authorization: false` flag, and the
exact report output path. No item says "see the skill" or "use the standard prompt." These are
fully embedded. PASS.

---

## Items Reviewed

| Item | B2 verdict | Note |
|------|-----------|------|
| Step 1.1 | PASS | context+action+output(frontmatter+log)+verify+gate all present |
| Step 1.2 | PASS | explicit dir list, creation verify, gate |
| Step 0.1 | FAIL (IMPORTANT) | self-contained but oversized/multi-source — Issue 5 |
| Step 0.2 | PASS | options + spec citation + HALT + PENDING path all embedded |
| Step 0.3 | PASS | options + §5.3 verbatim + HALT + path embedded |
| Step 2.1 | PASS | precedent + DM-010 schema + FR bullets embedded; explicit path |
| Step 2.2 | PASS | template schema + path + measurable checks |
| Step 2.3 | PASS | 3 edits named; reads produced file by path (proper handoff) |
| Step 2.4 | PASS | U1/U2 named, pytest+ruff commands, output path |
| Step 3.1 | PASS | OI-1 table + 6-step build + signatures + FR bullets; defers slug correctly |
| Step 3.2 | PASS | reads resolved decision; HALT-if-PENDING; precedent path embedded |
| Step 3.3 | FAIL (MINOR) | logs to wrong "Phase 2 Findings" section — Issue 4 |
| Step 3.4 | FAIL (MINOR) | logs to wrong "Phase 2 Findings" section — Issue 4 |
| Step 4.1 | FAIL (MINOR) | "(Phase 3)" locator + wrong-phase Findings — Issues 3,4 |
| Step 4.2 | FAIL (MINOR) | wrong-phase Findings target — Issue 4 |
| Step 5.1 | PASS | models.py anchor + §5.1 defaults embedded |
| Step 5.2 | PASS | Q8 pre-clamp branch fully described inline |
| Step 5.3 | PASS | Click options + §5.3 transport_enum verbatim embedded |
| Step 5.4 | PASS | measurable CliRunner assertions + commands |
| Step 6.1 (I1) | PASS | precedent + 4 signals + FR-RH2.5 bullets embedded |
| Step 6.2 (I2) | FAIL (IMPORTANT) | "SAME assertions used in I1" not fully restated — Issue 1 |
| Step 6.3 (I3) | PASS | mn_guard_table row re-embedded VERBATIM in item |
| Step 6.4 (I4) | FAIL (IMPORTANT) | "I1 positive assertions FAIL" not restated — Issue 2 |
| Step 6.5 (I5) | FAIL (IMPORTANT) | "I1 positive assertions FAIL" not restated — Issue 2 |
| Step 6.6 (I6) | PASS | row embedded; Q6 slug gating correct (focus item 7) |
| Step 6.7 (I7) | PASS | fixture shape + FR-RH2.7 bullet embedded |
| Step 6.8 (I8) | PASS | path_confinement block embedded VERBATIM |
| Step 6.9 (I9) | PASS | DM-017 anchor + emit site embedded |
| Step 6.10 | PASS* | measurable; wrong-phase Findings target (Issue 4) only blemish |
| Step 7.1 | PASS | guard anchors + FR-RH2.8 bullet; explicit extension target |
| Step 7.2 | PASS | spec §9 + OI-2/Q2 confirm-vs-amend embedded |
| Step 7.3 | PASS | U7/U9 + both pytest runs + grep literals embedded |
| Step 8.1 | PASS | 4 ordered commands + measurable green criteria |
| Step 8.2 | PASS | DoD matrix mapping fully described |
| Step QG.1 | PASS | Glob scope + manifest path embedded |
| Step QG.2 (×3) | PASS | full lens prompts embedded (focus item 3) |
| Step QG.3 (×3) | PASS | full lens prompts embedded (focus item 3) |
| Step QG.4 (×2) | PASS | consolidate rule + serialized-fix logic embedded |
| Step QG.5 (×3) | PASS | verify spawns + monotonicity protocol embedded |
| Post-Completion (×5) | PASS | each carries path/command/gate; POST-reflect recursion guard embedded |

(*Step 6.10 verdict is PASS on the 5 B2 components; the wrong-section log target is the
cross-cutting Issue-4 trace blemish, not a missing component.)

---

## Summary

- Items reviewed: 33 distinct `- [ ]` items (counting QG multi-spawn rows individually: ~45 checkboxes)
- B2-CLEAN majority; 5 distinct B2 issues
- CRITICAL: 0 | IMPORTANT: 3 | MINOR: 2
- The four checklist FOCUS items (Phase-0 gates / agent-spawn embedding / ensemble-empty gating / file-path specificity): all COMPLIANT

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | Step 6.2 (I2) | "SAME assertions used in I1 positive test" not restated; reader must open Step 6.1 | Embed the canonical I1 assertion list (tier_reached==2, merge_method!=single-reviewer-fallback, reviewer_count>=2, t2_model_class_diversity==full) inline |
| 2 | IMPORTANT | Steps 6.4, 6.5 | "the I1 positive assertions FAIL here" — the I1 assertion set is not enumerated in-item | Embed the canonical I1 assertion list in each |
| 3 | IMPORTANT | Step 0.1 | Oversized multi-source item (2 files + grep + 5-col artifact + tally) strains "execute without scrolling" | Split into 0.1a (validate models.py/contract.py provenance) + 0.1b (author + tally the artifact) |
| 4 | MINOR | Steps 3.3, 3.4, 4.1, 4.2, 5.1–5.4, 6.1–6.10, 7.1–7.3, 8.1, 8.2 | Blocker-log target hard-codes "### Phase 2 Findings" for non-Phase-2 items | Point each to its own phase's Findings section (or one canonical ### Findings) |
| 5 | MINOR | Step 4.1 | "(Phase 3)" used as a locator alongside the explicit path | Drop "(Phase 3)"; the path is already given |

## Recommendations

- Fixes 1 and 2 are the only B2 changes that affect EXECUTABILITY (an executor writing I2/I4/I5
  could under- or over-assert the negative-witness check). Address before execution.
- Fix 3 (split 0.1) is advisable but the item is technically self-contained; defer if churn-averse.
- Fix 4 is a trace-hygiene cleanup; bulk find-replace "### Phase 2 Findings" → per-phase headings.
- The VERBATIM re-embedding discipline across Phase-0 gates, the §5.3 blocks, and the QA-gate lens
  prompts is exemplary B2 practice and should be preserved.

VERDICT: FAIL

(3 IMPORTANT + 2 MINOR self-containment issues; no CRITICAL. The task is largely
B2-compliant — the Phase-0 gates, agent-spawn items, and verbatim-block re-embedding are
model practice — but the negative-witness items (6.2/6.4/6.5) lean on un-restated I1
assertions, Step 0.1 is an oversize granularity strain, and ~20 items mis-target their
blocker-log section. Per zero-tolerance, any B2 gap = FAIL.)

## QA Complete
