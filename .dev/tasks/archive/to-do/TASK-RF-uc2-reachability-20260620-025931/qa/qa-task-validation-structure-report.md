# QA Report — Task Integrity (Structure + Phase Ordering Lens)

**Topic:** FR-RSR UC-2 Runtime-Surface Reachability Escalation tasklist
**Date:** 2026-06-20
**Phase:** task-integrity
**Lens:** phase-structure + FR-RSR blocker ordering
**Fix cycle:** N/A (fix_authorization: false)
**Task file:** TASK-RF-uc2-reachability-20260620-025931.md
**Template:** 02

---

## Overall Verdict: FAIL (see full rationale at end). 8/9 checks PASS; 5 issues (2 IMPORTANT, 3 MINOR).

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS (with note) | Read lines 1–65. `id`/`title`/`status`/`type`/`spec_path`/`start_commit`/`executor_model_class`/`template_schema_doc` all present non-empty. `reflect_pre` stub present (L21–28). `reflect_post: ""` stub (L30) correctly left for the wrapper. NOTE: spawn checklist named a `template` field; file uses `template_schema_doc` (L51) — semantically equivalent, not a defect. |
| 2 | Mandatory Template-02 sections present | PASS | Task Overview (L69), Key Objectives (L77), Prerequisites & Dependencies (L90), Execution Context (L115), Detailed Task Instructions w/ 8 phases + Phase Gate (L162–350), Post-Completion Actions (L352), Task Log / Notes (L366). |
| 3 | Blocker ordering correct & explicit | PASS | Prerequisites L94–99 STATES P1 BLOCKS P2–6; oracle+rootwalk "MUST be in place before any UNREACHED verdict can be emitted; the gate on FR-RSR.2's UNREACHED path"; eval TERMINAL. Step 3.2 (L202) restates "no UNREACHED is emittable without the oracle + rootwalk consult". Phase 2 header (L182) + Phase 3 header (L194) restate the gate. Dependencies STATED in item bodies. |
| 4 | Phase ordering follows TDD §23.2 P1–P6 | FAIL (IMPORTANT) | TDD §23.2 (tdd.md L955–964) maps P5(Surface)=FR-RSR.7(contract)+FR-RSR.9. Task places FR-RSR.7 contract in **Phase 3 (Gather)** (Step 3.3, L204–206), not Phase 5/Surface. See Issue #1. Theme spine otherwise honored. |
| 5 | Anti-orphaning: completion items in final phase; POST reflect penultimate | PASS | POST reflect wrapper (L362) immediately precedes the Update-status-to-Done terminal item (L364); Done item explicitly gated on wrapper exit 0. POST reflect is PENULTIMATE. |
| 6 | POST reflect item is FLAT wrapper form | PASS | L362: `superclaude reflect run <taskfile> --depth deep --fix --promote` behind `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, consumes exit code. Explicitly "NO --base, NO --reflect, NO range, NO agent-spawn". Correct FLAT form. |
| 7 | Task Log present; reasonable item count | PASS (with note) | Task Log at L366 with phase-finding subsections. Item count = 30 (see Issue #4). TRACK GOAL expected ~44; materially lower. Flagged MINOR. |
| 8 | FINAL M3 QA gate ≥6 agents, report-only-then-serialized-fix | PASS | Phase Gate (L296–338): 3 rf-qa (PG.2/3/4) + 3 rf-qa-qualitative (PG.5/6/7), ALL `fix_authorization: false`. Consolidation PG.8. ONE serialized I20 fix agent PG.9. Verification PG.10 (≥2 agents) + Retry Monotonicity Protocol + byte-exact halt strings + max 3 cycles. |
| 9 | TB-Add-4 DAG (no cycles); TB-Add-3 OQ refs | PASS | Item-to-item refs form a DAG; handoff files written before read; no back-edge. No OQ-blocked checklist items (OQ-RSR.1–.5 RESOLVED at L444). TB-Add-3 vacuously satisfied. |

## Summary

- Checks passed: 8 / 9 (1 FAIL: check #4 phase ordering vs TDD §23.2)
- Checks failed: 1
- Issues found: 5 (CRITICAL: 0, IMPORTANT: 2, MINOR: 3)
- Issues fixed in-place: 0 (fix_authorization: false — REPORT ONLY)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Phase 3 header (L192–194) + Step 3.3 (L204–206) + Key Objectives item 3 (L83) | **Contract FR-RSR.7 placed in Phase 3 (Gather/P2), contradicting the authoritative TDD §23.2 which maps FR-RSR.7 → P5 (Surface).** TDD §23.2 (tdd.md L963): `P5 \| Surface \| FR-RSR.7, FR-RSR.9`. The task file instead folds the contract into Phase 3 and self-labels it "(P2, parallel)". The TRACK GOAL's authoritative tie-break is "When TDD and spec disagree, TDD wins" — and the TDD table is unambiguous. **Mitigation (why IMPORTANT not CRITICAL):** spec §10's sc:tasklist-specific guidance (spec.md L739) explicitly states "The contract task (FR-RSR.7) is parallelizable with the sweep task," which authorizes co-location with the sweep for a *tasklist* artifact; and the placement is dependency-COHERENT (the §5.3 pre-filter in Phase 4 reads `runtime_surface_unreached`, which Phase-3 contract defines before Phase 4 needs it — moving the contract to P5 would create a forward-reference where Phase 4 reads an undefined field). **Fix:** EITHER (a) relabel the Phase 3 header to drop the misleading "(P2, parallel)" tag and add an explicit reconciliation note: "FR-RSR.7 contract is co-located with the sweep per spec §10 sc:tasklist parallelizability guidance, deviating from TDD §23.2's P5 assignment because the §5.3 Phase-4 gate consumes `runtime_surface_unreached` and must read it as already-defined — a P5 contract would forward-reference an undefined field"; OR (b) move FR-RSR.7 to Phase 6 (Surface) AND reorder so the §5.3 gate's field dependency is still satisfied. Option (a) is preferred (the placement is correct; only the labeling/justification is missing). This reconciliation belongs in the body as a stated decision, not left implicit. |
| 2 | IMPORTANT | TDD §23.2 table (tdd.md L955–964) vs Phase 6 (L240) | **FR-RSR.8 (fail-open) is absent from the TDD §23.2 phase table entirely**, yet the task assigns it to Phase 6 (Surface) co-located with FR-RSR.9. The task gives no stated reconciliation for where FR-RSR.8 sits in the P1–P6 spine. Phase 6 placement is defensible (FR-RSR.8 depends on the Phase-3 sweep and is a surfacing/robustness concern), but an executor cross-checking the task against TDD §23.2 will find no anchor. **Fix:** add a one-line note in the Phase 6 header stating "FR-RSR.8 fail-open is not assigned a discrete phase in TDD §23.2; it is wired here in Surface because it depends on the Phase-3 sweep and the §0.5d availability contract (spec §12.3). It is gated by the Phase-3 sweep, not by FR-RSR.9." |
| 3 | MINOR | Step PG.10 (L336–338) / Retry Monotonicity Protocol | The monotonicity halt condition is stated as "`\|failures_{n+1}\| >= \|failures_n\|`" with the byte-exact string `[HALT-MONOTONICITY] \|F\|=<n>`. This matches the rf-qa Retry Monotonicity Protocol spec (strict non-shrink → HALT). However the item conflates the two halt strings into one sentence without making explicit that the **regression check runs FIRST** and its halt string (`Regression detected on Item X.Y...`) takes precedence over the monotonicity string when both would fire in the same transition. The protocol ordering (regression → monotonicity → hard-cap → proceed) is named at L338 but the precedence-when-both-fire is not spelled out. **Fix:** add "(if both the regression and monotonicity conditions hold on the same cycle transition, emit the Regression halt string and do NOT emit the monotonicity string — regression takes precedence)." |
| 4 | MINOR | Step 5.2 (L232–234) / Step 6.1 (L244–246) | Two refs-edit items (`deviation-taxonomy.md` xref, `reviewer-spec.md` ledger entry) each cite specific source line anchors (e.g. taxonomy :115–138, reviewer-spec :47–49) that this structural lens did NOT independently re-verify against the live ref files (out of lens scope — anchor verification is delegated to the PG.4 evidence-citation-accuracy agent). NOT a structural defect; flagged so the reader knows these anchors are unverified by THIS report. **Fix:** none required structurally; PG.4 must verify. |
| 5 | MINOR | Whole-file granularity (item-10 atomicity) | Several execution items (Step 2.1 L186, Step 3.1 L198, Step 3.2 L202, Step 3.3 L206) are very large single paragraphs (~250–400 words, each embedding multiple Reads + one Edit + multiple acceptance assertions). They remain *self-contained* (B2-compliant) and each lands a single logical edit, so they do not breach the "single atomic change" rule, but they exceed the "executable without scrolling" heuristic. This is an accepted RF pattern for surgical-edit items with heavy anchor context, so flagged MINOR not IMPORTANT. **Fix:** optional — none mandatory; the heavy-context items are justified by the anchor-grounding requirement. |

## Corrections / Retractions (self-audit)

- **RETRACTED — my initial Items-Reviewed check #7 estimate of "30 items / low for scope":** A precise `grep -c '^- \[ \]'` returns **44** checklist items, which EXACTLY matches the TRACK GOAL's "~44" expectation. My earlier count was an estimate built while reading individual Steps and missed the 6 Post-Completion items. Item count is CORRECT and appropriate for scope. Check #7 is upgraded to clean PASS; the "MINOR low-count" sub-flag is withdrawn. (This is why grep-verification beats estimation — logging it per the self-audit principle.)
- **Phase-header-accuracy (task-integrity item 18):** No phase header in this file makes a numeric "(N items)" claim, so there is no header-count to falsify. Vacuously satisfied — no issue.

## Actions Taken

None — `fix_authorization: false`. All findings are report-only. No file was modified except this QA report.

## Confidence Gate

Step-1 categorization of the 9 structure/phase-ordering checks:
- VERIFIED [x]: #1 (Read L1–65), #2 (Read all sections), #3 (Read L94–99 + Step 3.2 + headers), #4 (grep TDD §23.2 + Step 3.3), #5 (Read L362–364), #6 (Read L362), #7 (grep count = 44), #8 (Read L296–338), #9 (traced item refs) — 9 VERIFIED.
- UNVERIFIABLE [?]: 0.
- UNCHECKED [ ]: 0.

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 3 | Glob: 0 | Bash: 3 (each mapped to a specific check: Read=task file pages + report; Grep/Bash=item count, phase headers, TDD §23.2, spec §10, FR placement)
- No web research performed (all claims local; no external/URL/standards-bound claim in scope).

Note: confidence is 100% on the STRUCTURE + PHASE-ORDERING lens only. Anchor-line accuracy (PG.4 lens), content/fail-loud correctness (PG.5 lens), and eval-falsifiability (PG.6 lens) are explicitly OUT of this lens's scope and are not asserted here.

## Recommendations

1. **Before execution:** Address Issue #1 — add the explicit TDD §23.2-vs-spec-§10 reconciliation note to the Phase 3 header (Option a). The placement is correct; the missing artifact is the *stated justification* for deviating from the TDD's authoritative P5 assignment. Without it, the POST reflect gate (or a reviewer) will flag the FR-RSR.7-in-Gather as an unexplained drift from the design of record.
2. Address Issue #2 — anchor FR-RSR.8 to a phase with a one-line note (it has no TDD §23.2 home).
3. Issue #3 (regression-vs-monotonicity precedence) is a low-cost clarity fix worth making since the gate is the last line of defense.
4. The strong structural elements — explicit blocker-ordering prose (Prerequisites L94–99), the gate restated inside the sweep item itself (Step 3.2), the correct FLAT POST reflect wrapper, the 6-agent M3 gate with serialized I20 fix + Retry Monotonicity Protocol, and the DAG-clean dependency graph — are all sound and require no change.

## Overall Verdict: FAIL

**Rationale:** One mandatory checklist item (#4, phase ordering vs the authoritative TDD §23.2) FAILS: the contract FR-RSR.7 is placed in Gather (Phase 3) where the TDD assigns it to Surface (P5), and the deviation is not reconciled in the task body (it is self-labeled "(P2, parallel)" — a placement the TDD table does not sanction). Under zero-tolerance task-integrity rules, an unreconciled deviation from the design-of-record phase mapping = FAIL, even though the placement is dependency-coherent and spec §10's sc:tasklist guidance supports parallelizing the contract. The fix is small (Option a: add the reconciliation note) and does NOT require re-architecting the phases. Issues #2/#3 should be folded into the same revision pass. Issues #4/#5 are informational.

This verdict is scoped to the STRUCTURE + PHASE-ORDERING lens. A clean overall task-integrity PASS additionally requires the anchor-accuracy, content-correctness, and eval-falsifiability lenses to pass.

## QA Complete
