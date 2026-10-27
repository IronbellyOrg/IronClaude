# Phase 3 — M3 Document-QA Consolidated Findings

**Topic:** RFMerger Refresh — M3 structural + content document-QA consolidation (report-only)
**Date:** 2026-06-18
**Consolidation scope:** M3 only (structural template-conformance, structural internal-consistency, structural evidence-quality, content actionability, content domain-accuracy, content cross-reference chain). **M4 source-fidelity reports are explicitly OUT OF SCOPE for this consolidation.**
**Fix authorization:** false — NO fixes applied. Report-only consolidation.
**Consolidation item:** Step 3.3 (M3 structural/content)

---

## CONSOLIDATED VERDICT: FAIL

The consolidated verdict is **FAIL** because 4 of the 6 M3 reports returned FAIL (zero-tolerance gate: any FAIL → consolidated FAIL).

### Source-report verdict roll-up

| # | M3 report | Verdict | Lens |
|---|-----------|---------|------|
| 1 | `phase-3-structural-template-conformance.md` | **PASS** | Structural / template conformance |
| 2 | `phase-3-structural-internal-consistency.md` | **FAIL** | Structural / cross-document internal consistency |
| 3 | `phase-3-structural-evidence-quality.md` | **PASS** | Structural / evidence quality |
| 4 | `phase-3-content-actionability.md` | **FAIL** | Content / actionability |
| 5 | `phase-3-content-domain-accuracy.md` | **FAIL** | Content / domain accuracy |
| 6 | `phase-3-content-crossref-chain.md` | **FAIL** | Content / cross-reference chain |

**FAIL count: 4 / 6.** Consolidated verdict is therefore FAIL.

Per-output verdict is preserved (not collapsed into a single package-level verdict). The two PASS reports (template-conformance, evidence-quality) are recorded as PASS and contributed only MINOR observations; they are not the basis of the FAIL. The FAIL is driven by cross-document internal-consistency defects, retained-requirement actionability gaps, domain-accuracy/source-ownership mismatches, and broken P2/P5 + `--no-reflect` traceability chains.

> Scope note on PENDING decisions: P2 and P5 are PENDING human decisions with `default_chosen: false`. PENDING status alone is **NOT** a document-QA failure and is not counted here as a finding. The P2/P5-related findings below are about (a) cross-document label divergence, (b) the P2 decision-record's own cap-semantics off-by-one and missing-`prd.md` update target, (c) undefined retained-option algorithms, and (d) missing artifact links to the decision records — none of which is "the decision is still PENDING," and none of which is a document that auto-defaulted a PENDING decision. No document auto-defaulted P2 or P5.

---

## Deduplicated Findings (keyed by affected document + requirement)

Findings are deduplicated across the six M3 reports by **affected document + requirement/topic**. Where multiple agents flagged the same underlying defect, the originating agents are merged into one row and the highest severity is taken. Originating-agent abbreviations:

- **IC** = `phase-3-structural-internal-consistency` (FAIL)
- **ACT** = `phase-3-content-actionability` (FAIL)
- **DOM** = `phase-3-content-domain-accuracy` (FAIL)
- **XREF** = `phase-3-content-crossref-chain` (FAIL)
- **TC** = `phase-3-structural-template-conformance` (PASS — observations only)
- **EQ** = `phase-3-structural-evidence-quality` (PASS — MINOR observations only)

Adversarial axes: AX-1 drift · AX-2 contradictions · AX-3 omissions · AX-4 weakened criteria · AX-5 invented content.

"Blocks downstream?" = does this finding block downstream implementation-tasklist (`/task-builder`) generation? (Note: P2/P5 PENDING already independently BLOCK `/task-builder` per the decision records; the column here records whether the *document-QA finding itself* adds a blocking condition.)

### CRITICAL findings

None. No M3 report raised a CRITICAL-severity finding.

### IMPORTANT findings

| ID | Originating agent(s) | Sev | Axis | Affected doc(s) | One-line description | Required fix | P2/P5 decision impact | Blocks downstream? |
|----|----------------------|-----|------|-----------------|----------------------|--------------|-----------------------|--------------------|
| C-01 | IC (F-1) + XREF (#3) | IMPORTANT | AX-3, AX-2 | `p2-human-decision-record.md` (+ `prd.md` consumer) | P2 decision-record's update-target list omits `prd.md`, though the PRD records P2 disposition in ≥4 places (PR-2 AC, OQ-3, Approval row, MoSCoW); P5 record correctly lists prd.md → the two records are mutually asymmetric. A reviewer who records P2 would leave PRD's P2 fields stale. | Add `prd.md` to the P2 record's update-target list (`spec.md, prd.md, tdd.md, refresh-requirements-ledger.md`). | Affects how a recorded P2 decision propagates; does not change PENDING status. | Yes — would propagate a stale PRD into tasklist generation if P2 is later decided. |
| C-02 | IC (F-2) | IMPORTANT | AX-2 | `p2-human-decision-record.md` (vs `spec.md`, `tdd.md`, `refresh-requirements-ledger.md`) | P2 patch-cap off-by-one: decision record says "Two-pass cap (at most two patch passes)" (= 2 total), but spec/tdd/ledger/historical define "2 extra cycles (3 total passes)". Same guard, two different caps. | Reword the P2 record to "the original pass + at most 2 re-patch passes = 3 total" to match spec/tdd/ledger. | Changes the actual cap a reviewer would adopt for the P2 retained option. | Yes — wrong cap would ship into any P2-retain implementation. |
| C-03 | IC (F-3) | IMPORTANT | AX-2 | `spec.md`, `prd.md`, `tdd.md` | The two PENDING decisions (P2, P5) carry three label schemes: unnumbered in spec, `OQ-3`/`OQ-4` in prd, `Q-P2`/`Q-P5` in tdd. A cross-reference to "OQ-3" resolves only in the PRD. Cross-document referential-integrity defect. | Pick one label scheme (e.g. `Q-P2`/`Q-P5`) and use it in all three docs. | Labeling only; PENDING status unchanged. | Yes — broken cross-refs would mislead task-builder when resolving the decision entities. |
| C-04 | ACT (#1) + DOM (#5) | IMPORTANT | AX-4, AX-3 | `spec.md` (FR-RFMERGE.1), `prd.md` (PR-1), `tdd.md` (FR-001), `refresh-requirements-ledger.md` (P1) | P1 `## Execution Context` block is "optional/may" with no defined emission trigger, granularity, or exact shape; AND it ignores that `## Execution Context` is already mandatory in the task-builder MDTM surface (`task-builder/SKILL.md:1066-1072,1231-1235`), risking two incompatible "Execution Context" meanings. | Define a deterministic emission rule + exact markdown shape; add a boundary stating whether P1 reuses the task-builder schema or deliberately uses a distinct contract; add no-semantic-collision tests. | None. | Yes — task-builder must guess the trigger and risks schema collision. |
| C-05 | ACT (#2) + DOM (#8) | IMPORTANT | AX-3, AX-2 | `spec.md` (§4.2 / P1 Architecture), `tdd.md` (§10.1 component inventory) | P1 names both inline `SKILL.md` and `templates/phase-template.md` as edit targets and labels the template a "read-only mirror reflected via `make sync-dev`", but the template lives under `src/` (not a `.claude/` generated mirror). Authoritative edit path is ambiguous; "generated mirror" terminology is misapplied. | State one authoritative edit path (edit `src/.../sc-tasklist-protocol/SKILL.md`); relabel the template "source-side read-only reference extracted from SKILL.md"; reserve "generated mirror" for `.claude/` copies. | None. | Yes — implementer could edit the wrong/canonical-vs-mirror file. |
| C-06 | ACT (#3) + DOM (#1, #2, #9) | IMPORTANT | AX-5, AX-3, AX-2 | `spec.md` (FR-RFMERGE.3 / §§2-5), `prd.md` (PR-3), `tdd.md` (§§6-8 / data entity), `refresh-requirements-ledger.md` (P3), `refresh-validation-matrix.md` (P3 gates) | P3 DNSP is framed as a *new* `sc:tasklist` Stage-7 mechanism, but synthetic-dnsp already exists and is owned by `task-builder/SKILL.md:873-911` (richer: fixed/dynamic fields, 2-element dedup key, found-count, all-agents-fail path, merge semantics, N-1 concurrency). Refreshed P3 reduces it to `source:"synthetic-dnsp"` + zero-success guard, mis-places ownership, and omits compatibility/regression tests vs the existing contract. | Decide P3 = extend/reuse existing task-builder DNSP **or** a deliberately separate, narrower tasklist-local DNSP with a stated compatibility boundary; import or scope-out the full current contract; add compatibility tests vs `tests/audit/test_dnsp_*` / `test_task_builder_merge.py`. | None. | Yes — highest-priority repair; mixed-ownership P3 cannot be safely generated into tasks. |
| C-07 | ACT (#4, #7) + DOM (#3) | IMPORTANT | AX-4, AX-2 | `spec.md` (FR-RFMERGE.4 + NFR), `prd.md` (PR-4), `tdd.md` (data entity / performance) | P4 requires a `gate-results.txt` with no serialization contract (content set, format, pass/fail record, empty/success behavior, Stage-7 insertion point), and repeatedly calls the gate "17-point" while current source (`sc-tasklist-protocol/SKILL.md:1132-1187`) defines **20** pre-write checks and no existing `gate-results.txt`. Performance NFRs ("no material regression", "bounded growth") have no threshold/fixture/predicate. | Define the exact `gate-results.txt` format + source-check set + Stage-7 injection point; correct "17-point" → actual 20-check gate (or explain the mapping); replace vague perf NFRs with bounded, fixtured criteria. | None. | Yes — task-builder cannot generate a P4 artifact or perf test without the contract. |
| C-08 | ACT (#5) | IMPORTANT | AX-4 | `spec.md` (FR-RFMERGE.2), `prd.md` (PR-2), `tdd.md` (FR-002) | P2 retained option names `full-set re-validation`, `monotonicity guard`, `regression detection`, `2-pass cap`, `no overlap` but defines no compared data, halt predicates, state model, or Stage-10.5 non-overlap proof. | If P2 stays in the decision space, define the algorithm + state model (failure set, prev/current comparison, regression predicate, cap counting, Stage-10.5 exclusion). | Defines the P2 *retained-option* contract; PENDING status unchanged. | Yes (conditionally) — if P2 is retained, the option is non-generatable as written. |
| C-09 | ACT (#6) | IMPORTANT | AX-4 | `spec.md` (FR-RFMERGE.5), `prd.md` (PR-5), `tdd.md` (FR-005) | P5 retained option says "min 2 matching overrides" but defines no feedback input schema, match key, override priority, warning text, or omission behavior (only one edge-case sentence). | Define the advisory input contract, matching algorithm, exact markdown output, strict-downgrade warning semantics, deterministic ordering/omission. | Defines the P5 *retained-option* contract; PENDING status unchanged. | Yes (conditionally) — if P5 is retained, the option is non-generatable as written. |
| C-10 | ACT (#8) | IMPORTANT | AX-4 | `spec.md` (test plan), `tdd.md` (test strategy) | Retained-requirement tests point to `tests/tasklist/ (new)` / "new Stage-7/orchestrator unit" with no concrete module/function under test, fixtures, or assertions. | Name target files or require discovery items that locate exact functions/classes; specify fixtures + assertions per retained requirement. | None. | Yes — test obligations are not executable for tasklist generation. |
| C-11 | XREF (#1, #4) | IMPORTANT | AX-3, AX-4 | `prd.md` (PR-6) | PR-6 describes `--no-reflect` in prose but omits it from PR-6 acceptance criteria, while spec (FR-RFMERGE.6, `spec.md:251-265`) and tdd (`tdd.md:293-294`) keep it. Weakened criterion / phantom coverage: a PRD-only acceptance review could pass without the escape-hatch requirement. | Add explicit PR-6 AC: `--no-reflect` skips Stage 10.5 + templated post-reflect, auto-set by `--dry-run`, slash-only. | None. | Yes — breaks the PRD acceptance chain for the `--no-reflect` requirement. |
| C-12 | XREF (#2) | IMPORTANT | AX-3 | `spec.md`, `prd.md`, `tdd.md`, `refresh-requirements-ledger.md`, `refresh-validation-matrix.md` | No refreshed output names `p2-human-decision-record.md` or `p5-human-decision-record.md` (`rg` → 0 matches); the P2/P5 chain is semantic text only, not a traceable artifact link. | Add explicit references to the decision-record files in the P2/P5 sections / human-decision gates (especially ledger + matrix). | Improves traceability of the PENDING decisions; status unchanged. | Yes — broken artifact traceability for the two gating decisions. |
| C-13 | DOM (#4) | IMPORTANT | AX-2 | `spec.md` (§§1.1, 5.1), `prd.md` (§§10.1, 25), `tdd.md` (§§2, 8, 10, 15) | PRD/TDD autowire conflated across two surfaces: `/sc:tasklist` slash command exposes only `--spec`; `superclaude tasklist validate` exposes `--tdd-file`/`--prd-file` + `.roadmap-state.json` autowire. The skill body also contradicts itself ("exactly one input"/roadmap-only at `SKILL.md:49-57` vs later source enrichment). | Split the claims by surface (slash-gen `--spec`; validate-CLI `--tdd-file`/`--prd-file` autowire); add an explicit open-risk for the skill's roadmap-only-vs-enrichment contradiction rather than treating autowire as settled. | None. | Yes — task-builder would inherit a conflated/contradictory input contract. |
| C-14 | DOM (#6, #7) + ACT (#11) | IMPORTANT | AX-4 | `refresh-validation-matrix.md` (gate rows + fix-cycle spec) | Matrix weakens current QA contracts: it specifies one fix agent/cycle then halt vs current task-builder max-3 fix-verify + monotonicity/regression behavior (`task-builder/SKILL.md:1263-1303,1396-1410`); and per-output QA agent counts fall below current I19/I21 final-document floors (8 final-doc agents for 500-1500 line docs vs matrix's 3+2+2 / 2+1+2). Also lacks QA-artifact paths/report schema/consolidator definition. | Recompute gate counts from output line counts per current I19/I21; align fix-cycle semantics with current retry/monotonicity rules (or label as a deliberate stricter override with safety rationale); add concrete QA-artifact paths + report schema. | None. | Yes — undercounted/weakened gates would let downstream generation proceed on weaker validation. |
| C-15 | ACT (#9) + DOM (#10) | IMPORTANT | AX-3 | `spec.md` (OQ-1/OQ-2), `prd.md` (OQ), `tdd.md` (OQ) | OQ-1 (`tests/cli/reflect/` path) / OQ-2 handling: docs treat OQ-1 as a blocker to "pinning" the matrix command, but the matrix already pins `uv run pytest tests/cli/reflect/ -v`; the open question is stale relative to the refreshed outputs. Separately, no explicit downstream precondition that source OQs be fixed/waived before `/task-builder` handoff. | Rephrase OQ-1 as an upstream-source cleanup only (matrix is already pinned); add an explicit precondition that no `/task-builder` handoff occurs until OQ-1/OQ-2 are fixed-at-source or formally waived with rationale. | None. | Yes — a builder could hit stale upstream facts if OQ source files are not fixed first. |
| C-16 | ACT (#10) | IMPORTANT | AX-3 | `tdd.md` (frontmatter, lines 21-26) | TDD `quality_scores` keys are present but blank, weakening the claimed self-check/frontmatter-completeness rigor and leaving quality metadata non-actionable. (Note: TC reported frontmatter PASS structurally; ACT flags the blank *values* as a content/actionability gap — recorded as the ACT finding.) | Populate the quality scores, or remove them from the actionable-metadata contract with a stated reason for intentional blankness. | None. | No (metadata completeness; does not block generation by itself). |

### MINOR findings

| ID | Originating agent(s) | Sev | Axis | Affected doc(s) | One-line description | Required fix | P2/P5 decision impact | Blocks downstream? |
|----|----------------------|-----|------|-----------------|----------------------|--------------|-----------------------|--------------------|
| C-17 | IC (F-4) | MINOR | AX-2 | `refresh-validation-matrix.md` (spec structural-gate column) | Matrix's spec-row required frontmatter field is `complexity` (singular), but spec carries `complexity_score` + `complexity_class` (no field named `complexity`); tdd row says "complexity fields" (plural) → matrix internally inconsistent and mis-gates the spec it gates. | Change the matrix spec-row required field to `complexity_score, complexity_class` (or "complexity fields"). | None. | No. |
| C-18 | IC (F-5) | MINOR | AX-1 | `spec.md` (frontmatter `status`) vs `prd.md`, `tdd.md` | Spec frontmatter `status: draft` (bare) vs sibling "🟡 Draft (reviewed-planning)" framing; a consumer keying on frontmatter sees a plainer state than the prose asserts. | Align spec frontmatter `status` with the reviewed-planning framing, or note in the matrix that the spec template intentionally uses a bare enum. | None. | No. |
| C-19 | EQ (M-1) | MINOR | AX-1 (borderline) | `spec.md` (§8.2 test plan, line 531) | Audit tests `test_inherited_verdict_freshness_inv_002.py` / `test_five_axes_overlay.py` given as bare filenames adjacent to a `tests/skills/...` path; they actually live at `tests/audit/`. Files exist; no wrong path literally asserted → imprecision, not fabrication. | Prefix both with `tests/audit/` for unambiguity. | None. | No. |
| C-20 | EQ (M-2) + TC (O-1) | MINOR | AX-1 (borderline) | `refresh-validation-matrix.md` (line 42) | A literal `{{SC_PLACEHOLDER:` token appears inside the structural-gate description (a self-describing check target, not a leaked placeholder); a blunt `grep` false-positives. Both PASS reports flagged this as a non-defect observation. | Optional: escape/rephrase the token so a blunt grep does not false-positive. | None. | No. |

---

## Finding Counts (deduplicated)

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| IMPORTANT | 16 (C-01 … C-16) |
| MINOR | 4 (C-17 … C-20) |
| **Total deduplicated** | **20** |

### Dedup accounting (raw → consolidated)

Raw findings across the 4 FAIL reports + MINOR observations from the 2 PASS reports totaled 5 (IC F-1..F-5) + 11 (ACT 1..11) + 10 (DOM 1..10) + 4 (XREF 1..4) + 2 (EQ M-1, M-2) = 32 raw rows. Merges applied: C-01 (IC F-1 + XREF #3), C-04 (ACT #1 + DOM #5), C-05 (ACT #2 + DOM #8), C-06 (ACT #3 + DOM #1/#2/#9), C-07 (ACT #4/#7 + DOM #3), C-11 (XREF #1 + #4), C-14 (DOM #6/#7 + ACT #11), C-15 (ACT #9 + DOM #10), C-20 (EQ M-2 + TC O-1). After deduplication by affected document + requirement: **20 distinct findings**.

### Downstream-generation gate

Of the 20 deduplicated findings, 13 IMPORTANT findings (C-01 through C-13, plus C-14/C-15) carry a "blocks downstream" condition; combined with the independently-blocking P2/P5 PENDING decisions, **downstream implementation-tasklist (`/task-builder`) generation must NOT proceed** until the consolidated FAIL is remediated and the gate re-run. No CRITICAL findings exist; no document auto-defaulted a PENDING decision.

## QA Consolidation Complete
