---
title: "Task-Builder Convergence — Inverse-Direction Merge of /sc:tasklist Qualities"
version: "1.0.0"
status: draft
feature_id: TASK-BUILDER-CONVERGENCE
parent_feature: v3.8-RigorFlowMerger
spec_type: feature
complexity_score: 0.7
complexity_class: MEDIUM
target_release: v3.9
authors: [orchestrator-pipeline]
created: 2026-05-14
quality_scores:
  clarity: 9.3
  completeness: 9.3
  testability: 9.5
  consistency: 9.3
  overall: 9.3
---

<!-- Provenance: Phase 6 of /sc:adversarial Mode A pipeline; populated from
     merged-output.md (portfolio), refactor-plan.md (per-change detail),
     per-proposal-verdicts.md, invariant-probe.md, conflict-register.md,
     reflect-task.md, gate-report.md (Phase 5.2 PASS), and FINAL-REPORT §1+§6.3+§9.
     Spec is template-compliant per src/superclaude/examples/release-spec-template.md
     (12 sections + appendices, 16 frontmatter fields). Acceptance Criteria adapted
     to the orchestration-mandated three-field structure
     (Observable / Verification / Negative) inside the template's checkbox idiom. -->

## 1.0 Ubiquitous Language (Added per spec-panel SP-19)

The five load-bearing task-builder invariants are referenced throughout this spec. To prevent term overloading (DDD anti-pattern flagged by Evans), each invariant has exactly one canonical meaning below; all other appearances of these terms in the spec, conflict-register, and downstream artifacts MUST conform.

- **self-contained-item**: Every checklist item carries the five fields {Description, Context, Acceptance, Confidence, Verification} sufficient to execute it without reading other items. Operational source: SKILL.md:1452-1457.
- **evidence-bound-item**: Every per-item Context field referencing a code surface includes a `file:line` citation OR a justified-absence comment. Operational source: SKILL.md:1530 rule #2. (NOTE: distinct from the synthetic-dnsp `evidence:` *field*, which is a finding-level log-path, not an item-level binding; and distinct from "advisory-itself-as-evidence" in conflict-register PR-05 rationale.)
- **persistent-`.dev/tasks/`-artifact**: Research and QA outputs persist to `.dev/tasks/<task-id>/` with stable naming. Operational source: §11 OPEN-INV-018; layout is a stable contract for the scope of this release (see §9 stability commitment).
- **zero-trust QA**: "Any gap regardless of severity = FAIL" stance at the task-integrity gate. Operational source: rf-qa.md:140-142.
- **parallel-research**: rf-analyst and rf-qa partition cohorts run concurrently; per-partition failures do not serialize the cohort. Operational source: NFR-CONV.10; INV-021 (DNSP fires within-agent-instance).

## 1. Problem Statement

The v3.8 RigorFlow Merger analysis (`.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md` §1) imported four RF execution-resilience mechanisms into `/sc:tasklist`. The analysis was deliberately one-way (RF → SC). FINAL-REPORT §6.3 surfaced an asymmetric finding: 4 of 5 RF→SC proposals were over-engineered because RF mechanisms designed for *execution context* (long-running, stateful, non-deterministic agents) imported their *implementations* rather than their *intent* into SC's *generation context* (single-pass, stateless, determinism-first).

That asymmetry is paradigm-defining. It opens an inverse-direction question that the v3.8 work did not answer: which `/sc:tasklist` qualities — designed for generation-time rigor — strengthen `task-builder` (an execution-context skill that runs agent-team workflows on MDTM tasks) without re-introducing the SC→RF over-engineering risk in reverse?

`task-builder` lacks at least three classes of capability that `/sc:tasklist` documents: (a) a task-level executor-readability summary distinct from per-item Context fields; (b) structural gate checks for placeholder/title-only items, circular dependencies, granularity bounds, and confidence-format consistency; (c) an inherited-verdict passthrough between adjacent rf-qa and rf-qa-qualitative agents. Without them, task-builder's load-bearing invariants — self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research — are operationally enforced item-by-item but lack the cross-cutting structural and task-level reinforcement that `/sc:tasklist` ships.

This release imports only the `/sc:tasklist` qualities that strengthen at least one of those five invariants AND do not introduce hidden-input non-determinism (FINAL-REPORT §6.2 F4) into task-builder's existing pipeline. Five proposals (PR-02, PR-03, PR-04, PR-06, PR-07) are adopted; PR-01 is adopted with a revise-then-adopt acceptance criterion; PR-05 is deferred to Phase-2 pending data accumulation.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| FINAL-REPORT §6.3 — "4 of 5 RF→SC proposals over-engineered; conservative alternatives adapt *intent* not *implementation*" | `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md:196-198` | Motivates per-CB-3 per-check classification; bulk-port REJECTED across all 7 proposals |
| Five task-builder invariants enumerated and load-bearing | `merged-output.md:18-24` | Defines acceptance gates: any adopted change MUST NOT weaken any of the 5 invariants |
| Empirical oscillation pattern — 21 retry files / 18 batches | FINAL-REPORT §6.2 F2 (`:180-184`) | Justifies PR-02 monotonicity + regression-detection stop-conditions |
| Per-step Context references are unreliable (paths hallucinated/stale) | FINAL-REPORT §6.2 F1 (`:175-178`) | Justifies PR-01 scope-confinement of "no specific paths" rule to task-level header only |
| Hidden-input determinism risk for advisory-from-history mechanisms | FINAL-REPORT §6.2 F4 (`:191-194`) | Justifies PR-05 Phase-2 deferral and advisory-only framing in any future adoption |
| Convergence 0.88 over 7-proposal portfolio after Round 2 + invariant probe | `merged-output.md:13` | All 5 MEDIUM invariant concerns routed through explicit per-change acceptance criteria; HIGH-UNADDRESSED = 0 |
| Phase 5.2 G1–G5 citation/invariant gate verdict | `reflection/gate-report.md` (all 5 gates PASS) | Phase 6 cleared to proceed; no degradation required |

### 1.2 Scope Boundary

**In scope**: Six additive landings into `src/superclaude/skills/task-builder/SKILL.md` and `src/superclaude/agents/rf-{qa,qa-qualitative,analyst,task-builder}.md`. All landings adapt `/sc:tasklist` *intent* per FINAL-REPORT §6.3 — implementations stay native to task-builder's existing 4-stage gate topology and rf-* agent partitioning model. Acceptance criteria for INV-002, INV-010, INV-012, INV-015, INV-019 are spec-resident (not deferred to implementation discretion). All edits flow through the `make sync-dev` / `make verify-sync` pipeline (A-001).

**Out of scope**: (a) Bulk-port of all 17 `/sc:tasklist` quality-gate checks (REJECTED per CB-3 — see Appendix E). (b) Modifying tier selection on historical pattern (REJECTED per FR §6.2 F4 hidden-input risk — see Appendix E X-004). (c) Replacing rf-qa-qualitative's 15-item task-qualitative checklist (REJECTED — overlay-only per X-002 anti-inflation rule). (d) PR-05 tier-history advisory (DEFERRED to Phase-2 — see §11 Open Items). (e) Any roadmap regeneration or downstream tasklist generation (Phase 8+ work — see §10 Downstream Inputs). (f) Any structural change to `.dev/tasks/` directory layout (INV-018 portfolio-wide note).

## 2. Solution Overview

Six per-proposal landings into existing files, plus PR-05 Phase-2 deferral, plus eight cross-cutting acceptance criteria. No new skill, no new agent, no new gate stage. Every landing is additive (A-002 zero-trust governance). The portfolio's combined score is 0.88 convergence — above the 0.80 threshold.

The **base proposal** is PR-03 (DNSP Synthetic Finding, CASE-B, combined score 0.959), selected by combined hybrid scoring (quant 0.50 + qual 0.50) with Level-1 tiebreaker on debate performance. PR-03 was the only proposal across 5 RF→SC ports in v3.8 to win without revision (P3 39/50 in FINAL-REPORT §6.1) — paradigm-neutral by external evidence, CASE-B no-conflict by direct classification, and dual-invariant reinforcement (zero-trust QA + evidence-bound-item).

**Phase-1 ADOPT (5 proposals)**: PR-02 retry-monotonicity-guards, PR-03 DNSP-synthetic-finding (BASE), PR-04 gate-results-passthrough, PR-06 structural-gate-additions, PR-07 adversarial-category-naming.

**Phase-1 REVISE-then-adopt (1 proposal)**: PR-01 execution-context-header, with TB-Add-8 acceptance criterion (resolves INV-015 scope-confinement test).

**Phase-2 deferred (1 proposal)**: PR-05 tier-history-advisory, with explicit re-evaluation trigger (`.dev/tasks/done/` ≥10 completed tasks of ≥3 distinct task_types).

**Landing sequence**: PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03. This sequence resolves INV-010 (PR-06 lands first so PR-04's dynamic checklist enumeration auto-picks up the TB-Add catalogue) and INV-012 (PR-02's monotonicity logic specifies how PR-03 synthetic findings count toward `|F_n|`).

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Direction of port | task-builder ← /sc:tasklist (inverse of v3.8) | Continue v3.8 RF→SC direction only | FINAL-REPORT §6.3 asymmetry only documented one direction; portfolio-wide adversarial debate confirmed reverse direction has 5 ADOPT-grade qualities not yet imported |
| Base proposal selection | PR-03 (combined 0.959) | PR-02 (highest combined 0.965); PR-06 (0.963) | Level-1 tiebreaker (debate performance + paradigm-neutral external evidence: P3 39/50 unique in portfolio). PR-03 is CASE-B; PR-02/PR-06 are CASE-D. CASE-B = lowest integration friction |
| Bulk import of /sc:tasklist 17-point gate | REJECTED — per-check classification (CB-3) | Bulk-port of all 17 checks via PR-06 alternative | Bundle-specific checks (phase-file naming, index references) inapplicable to single-MDTM output; only 6-7 unique additive checks survive triage |
| PR-01 "no specific paths" rule scope | Header-only — per-item Context retains file:line | Extend rule to all task content (X-001 considered) | evidence-bound-item invariant is per-item and load-bearing (SKILL.md:1530 rule #2); scope-confinement preserves it; TB-Add-8 enforces the boundary structurally |
| PR-04 inherited-verdict reliance | Mechanical re-checking SKIPPED; semantic checks STILL required | Full verdict reliance (X-002 considered) | Anti-inflation rule rf-qa-qualitative.md:766-775 preserved; INV-019 acceptance criterion mandates Self-Audit listing |
| PR-02 halt-on-slow-convergence threshold | Strict non-shrink only (`F_{n+1} >= F_n` halts) | Halt on F_{n+1} = F_n - 1 (X-003 considered) | Preserves legitimate multi-cycle correction; forward motion permits continuation |
| PR-05 disposition | DEFER to Phase-2 | ADOPT in Phase-1 with advisory disclaimer; REJECT outright | Combined 0.862 (lowest); INV-003 MEDIUM unaddressable in agent-exploratory paradigm; author's own Phase-2 framing is strongest evidence |
| Landing sequencing | PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 | Parallel landing; reverse sequence | Resolves INV-010 (PR-06 establishes catalogue before PR-04 reads it); INV-011 (PR-06 absorbs PR-01 cross-validation as TB-Add-7); INV-012 (PR-02 spec'd dedup against PR-03) |

### 2.2 Workflow / Data Flow

```
BUILD_REQUEST.md
      │
      ▼
rf-task-builder ────► generates MDTM task file
      │                     │
      │                     ├── Execution Context block (PR-01, NEW)
      │                     │     references / source-areas (no specific paths) / constraints
      │                     │
      │                     └── checklist items (5-field schema, evidence-bound)
      │
      ▼
rf-analyst (partition protocol)
      │  N partitions in parallel
      │  ▼ on N=1: standard escalation only
      │  ▼ on escalation-ladder-exhaust: DNSP synthetic-dnsp finding emitted (PR-03, NEW)
      │     severity=HIGH, source=synthetic-dnsp, affected_range, evidence=spawn-log path,
      │     dedup-key=(assigned_files_range, escalation_ladder_exhaust_point)
      ▼
rf-qa  (A.10 task-integrity — 9 items → 9+8 items)
      │  TB-Add-1..7 (PR-06, NEW) — placeholder / count-bounds (advisory) / clarification-adjacency /
      │     DAG / granularity / format-consistency / Execution-Context-reappear
      │  TB-Add-8 (PR-01 acceptance criterion) — per-item Context field has file:line or justified absence
      │  Retry loops (PR-02, NEW) — monotonicity guard + regression detection
      │     Regression > monotonicity precedence; synthetic-dnsp counts as failure; dedup-key not regression
      │
      ▼
rf-qa-qualitative  (semantic check on items not covered by inherited PASS)
      │  ## Inherited Structural Verdict (PR-04, NEW) — rf-qa table verbatim
      │     "PASS items machine-verified — skip structural re-checking;
      │      FAIL items machine-verified defects — flag HIGH; focus on semantic quality"
      │  5 Adversarial Axes (PR-07, NEW) — drift / contradictions / omissions / weakened / invented
      │     drift-axis-inactive annotation when no GOAL-baseline item exists
      │
      ▼
MDTM task file (final, evidence-bound, structurally + semantically gated)
```

## 3. Functional Requirements

Each FR section corresponds to one accepted proposal. CASE classification (per the G6 four-case rule) is annotated; CASE-A/D rows reference `conflict-register.md`. Acceptance Criteria use the three-field structure (Observable behavior / Verification method / Negative criterion) inside the template's checkbox idiom.

### FR-CONV.1: Structural Gate Additions (PR-06, lands first)

**Description**: Append 8 structural checks (TB-Add-1 through TB-Add-8) to rf-qa's task-integrity checklist (currently 9 items at SKILL.md:898-906; rf-qa.md:264-287 has the 20-item form) and mirror in the 15-item validation block (SKILL.md:1491-1507). Each check is imported per CB-3 (per-check, not bulk) from `/sc:tasklist`'s 17-point gate (checks 11/13/14/15/16/17). TB-Add-7 (Execution-Context source-areas reappear in items) absorbs PR-01 failure-mode #4 cross-validation. TB-Add-8 (per-item Context field file:line citation OR justified absence) is the structural test that resolves INV-015 — see FR-CONV.2.

**TB-Add catalogue**:
- TB-Add-1: Placeholder scan ("TBD"/"TODO"/title-only) — Hard check
- TB-Add-2: Item count bounds (≥3 / ≤40 track / ≤50 single-track) — **ADVISORY-fail-until-calibrated** (INV-006 LOW)
- TB-Add-3: Clarification adjacency to blocked items — Hard check
- TB-Add-4: Circular dependency detection (DAG check) — Hard check
- TB-Add-5: Granularity check (XL items have subtasks) — Hard check
- TB-Add-6: Confidence/Verification format consistency — Hard check
- TB-Add-7: Execution Context source-areas reappear in items (cross-validates PR-01) — Hard check
- TB-Add-8: Every per-item Context field referencing a code surface includes ≥1 file:line citation OR justified-absence comment — Hard check

**CASE**: D — see `conflict-register.md` row PR-06. Conflicting `/sc:tasklist` mechanism: 17-point gate bulk import. Protected invariant: zero-trust QA.

**Acceptance Criteria for FR-CONV.1**:
- [ ] **Observable behavior**: Each of TB-Add-1..8 fires a distinct, item-ID-naming error message when its condition is violated; TB-Add-2 emits an `[ADVISORY]` prefix and does NOT block the gate; TB-Add-1..7 (excluding 2) block the gate on failure.
- [ ] **Verification method**: `grep -nE "TB-Add-[1-8]" src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md` must return ≥3 hits per ID (rf-qa.md:264-287 + SKILL.md:898-906 + SKILL.md:1491-1507); synthetic fixture with one placeholder-titled item runs rf-qa and TB-Add-1 emits in the gate log.
- [ ] **Negative criterion**: No existing rf-qa check is renamed, renumbered, or removed; the 9-item A.10 and 15-item validation existing-items are preserved verbatim; bundle-specific `/sc:tasklist` checks (phase-file naming, index references) MUST NOT appear in any TB-Add.

**Dependencies**: None (lands first).

### FR-CONV.2: Execution Context Header (PR-01, REVISE-then-adopt, lands second)

**Description**: Insert a task-level `## Execution Context` block in generated MDTM task files (after frontmatter, before checklist). Block contains: References (BUILD_REQUEST GOAL, WHY, related-doc IDs), Source areas (named modules/packages — **strictly NO specific file paths**), Key constraints (top 1-3 invariants from BUILD_REQUEST). Edits at SKILL.md:228-238 (template-selection note), SKILL.md:1409-1485 (output schema), SKILL.md:719 (rf-task-builder spawning instruction). The "no specific paths" rule is **scope-confined to the header**: per-item Context fields and research/*.md retain file:line citations to preserve the evidence-bound-item invariant. INV-015 (scope-confinement structural test) is resolved by TB-Add-8 in FR-CONV.1.

**CASE**: D — see `conflict-register.md` row PR-01. Conflicting `/sc:tasklist` mechanism: `## Execution Context` block per FINAL-REPORT §7-R2. Protected invariant: evidence-bound-item.

**Acceptance Criteria for FR-CONV.2**:
- [ ] **Observable behavior**: Generated MDTM task files contain a `## Execution Context` block with exactly three labeled lines (References / Source areas / Key constraints); when BUILD_REQUEST is minimal, the block degrades to References-only with WHY/source-area lines explicitly omitted (PR-01 failure-mode #2).
- [ ] **Verification method**: `grep -n "## Execution Context" <generated-task-file>` returns line N; the next 10 lines contain ≥1 of `References:` / `Source areas:` / `Key constraints:`; running `grep -E "src/|/.*:[0-9]+" <header-block-range>` returns zero hits (no file paths or file:line citations within the header).
- [ ] **Negative criterion**: Per-item Context fields elsewhere in the file MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8); the per-item self-contained 5-field schema MUST NOT be altered or supplemented by header content.

**Dependencies**: FR-CONV.1 (TB-Add-7 cross-validation + TB-Add-8 scope-confinement test must already be live).

### FR-CONV.3: Gate Results Passthrough (PR-04, lands third)

**Description**: Inject rf-qa's task-integrity verdict table verbatim into rf-qa-qualitative's spawn prompt under the heading `## Inherited Structural Verdict`, with prompt language: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality." Edits at SKILL.md:923-1000 (A.10.5 spawn description) and rf-qa-qualitative.md:794 (passthrough reference operationalisation). Operationalises an already-stated rule rather than introducing new behavior.

**CASE**: B — no conflict (CASE-B = no row in conflict-register). Invariant alignment: zero-trust QA (semantic verification still required).

**Acceptance Criteria for FR-CONV.3**:
- [ ] **Observable behavior**: rf-qa-qualitative's spawn prompt contains `## Inherited Structural Verdict` with the rf-qa table verbatim; on a fix-cycle re-run, the orchestrator re-injects the NEW verdict (INV-002); the spawn prompt's checklist enumeration is dynamic (auto-picks up TB-Add catalogue from FR-CONV.1, INV-010); rf-qa-qualitative's first run after FR-CONV.3 lands produces a `## Self-Audit` entry listing relied-on rf-qa PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019).
- [ ] **Verification method**: Capture rf-qa-qualitative spawn-prompt log; `grep -n "## Inherited Structural Verdict" <spawn-log>` returns line N; the block immediately below it matches rf-qa's emitted verdict table byte-for-byte; on a synthetic 2-cycle fixture, the second cycle's spawn log shows the NEW (cycle-2) verdict, not the stale (cycle-1) verdict; the same fixture's rf-qa-qualitative output contains a Self-Audit section with ≥1 entry per category above.
- [ ] **Negative criterion**: rf-qa-qualitative MUST NOT mark any item VERIFIED solely from the inherited verdict — every VERIFIED item must show an independent semantic-check engagement in the Self-Audit listing; anti-inflation rule rf-qa-qualitative.md:766-775 MUST NOT be weakened, removed, or rephrased; no stale verdict from a prior fix cycle is permitted to govern current-cycle decisions.

**Dependencies**: FR-CONV.1 (TB-Add catalogue is the verdict content); FR-CONV.2 (Execution Context cross-validation via TB-Add-7 occurs at A.10 BEFORE A.10.5 spawn, per INV-011).

### FR-CONV.4: Adversarial Category Naming (PR-07, lands fourth)

**Description**: Insert a "Five Adversarial Axes" header subsection BEFORE rf-qa-qualitative's existing 15-item task-qualitative checklist, with axis-annotation requirement on the Items Reviewed table. Five named axes: drift / contradictions / omissions / weakened criteria / invented content. Edits at rf-qa-qualitative.md:527-583 (axis subsection) + rf-qa-qualitative.md:675-714 (output template axis annotation) + SKILL.md:961 (reference). The 5 axes are an *overlay annotation*, not a replacement of the 15-item checklist topology. Drift-baseline operationalisation (PR-07 failure-mode #3): if the existing checklist does not contain an item that captures BUILD_REQUEST.GOAL verbatim, surface `drift-axis-inactive` annotation.

**CASE**: D — see `conflict-register.md` row PR-07. Conflicting `/sc:tasklist` mechanism: 5-category adversarial agent prompt. Protected invariant: zero-trust QA.

**Acceptance Criteria for FR-CONV.4**:
- [ ] **Observable behavior**: rf-qa-qualitative's task-qualitative output renders a "Five Adversarial Axes" subsection BEFORE the 15-item checklist; the Items Reviewed table contains an `axis` column populated with one of {drift, contradictions, omissions, weakened-criteria, invented-content, none} per row; when no item in the checklist captures BUILD_REQUEST.GOAL verbatim, output includes a single-line `drift-axis-inactive` annotation.
- [ ] **Verification method**: `grep -n "Five Adversarial Axes" <rf-qa-qualitative-output>` returns line N; the Items Reviewed table parses to N rows each with a non-empty `axis` value from the canonical set; synthetic fixture with no GOAL-baseline item produces `drift-axis-inactive` in the output.
- [ ] **Negative criterion**: The existing 15-item task-qualitative checklist MUST NOT be removed, reordered, or replaced — axes annotate, they do not substitute; the severity floor at rf-qa-qualitative.md:789 MUST NOT be weakened; no axis may rely on a code-path change (overlay-only, per CB-3).

**Dependencies**: FR-CONV.3 (5 axes apply to items NOT covered by inherited PASS — composition is clean per INV-013 ADDRESSED).

### FR-CONV.5: Retry Monotonicity Guards (PR-02, lands fifth)

**Description**: Add two stop-conditions to EXISTING retry loops (no new loop or stage): (1) Monotonicity guard — HALT if `|gate_failures|` does not strictly shrink between cycles (`F_{n+1} >= F_n` halts); (2) Regression detection — HALT if any item that PASSed at cycle N FAILs at cycle N+1. Precedence rule: **Regression > monotonicity**. Halt message format: `"Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check."` Edits at SKILL.md:870 + SKILL.md:1550 (new "Retry Monotonicity Protocol" subsection) + rf-task-builder.md:336-359 (per-gate fix-cycle integration) + rf-qa.md:310-313 (3-fix-cycle integration). Independent retry counters (RESEARCH_NEEDED, MALFORMED, research-gate, per-gate) each retain their own monotonicity history — NOT collapsed (INV-001).

**INV-012 composition criterion (PR-02 + PR-03 stacking)**: Synthetic findings emitted by FR-CONV.6 (PR-03 DNSP) COUNT as failures for `|F_n|` monotonicity. BUT a synthetic finding with identical dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles is a dedup case (PR-03 failure-mode #4), NOT a regression. This composition rule is encoded verbatim in the Retry Monotonicity Protocol subsection.

**CASE**: D — see `conflict-register.md` row PR-02. Conflicting `/sc:tasklist` mechanism: Stages 9-10 monotonicity guard + regression detection + full-set re-validation. Protected invariant: zero-trust QA.

**Acceptance Criteria for FR-CONV.5**:
- [ ] **Observable behavior**: On a fix-cycle where `F_{n+1} >= F_n`, the loop emits `[HALT-MONOTONICITY] |F|=<n>` and exits; on a cycle where Item X.Y was PASS at cycle N and is FAIL at cycle N+1, the loop emits the verbatim regression halt message and exits BEFORE the monotonicity check; on a cycle where a synthetic-dnsp finding with identical dedup-key appears in both N and N+1, no halt fires (dedup recognized).
- [ ] **Verification method**: Synthetic 3-cycle fixture with `F_1=5, F_2=5, F_3=5` halts at cycle 2 with `[HALT-MONOTONICITY]`; synthetic 2-cycle fixture with Item 3.2 PASS@1/FAIL@2 halts at cycle 2 with the regression message; synthetic 2-cycle fixture with one synthetic-dnsp finding (same `assigned_files_range`+`escalation_ladder_exhaust_point` in both cycles) proceeds to cycle 3 without halting; `grep -n "Retry Monotonicity Protocol" src/superclaude/skills/task-builder/SKILL.md` returns ≥2 lines (SKILL.md:870 + SKILL.md:1550).
- [ ] **Negative criterion**: Legitimate slow-cycle correction MUST NOT be halted — any cycle where `|F|` strictly shrinks (even by 1) continues; the four independent retry counters MUST NOT be collapsed into a shared monotonicity state; no halt-on-slow-convergence threshold (e.g., `F_{n+1} = F_n - 1`) is permitted (X-003 REJECTED).

**Dependencies**: FR-CONV.1 (gate produces `F_n` count); FR-CONV.6 (synthetic-dnsp findings consumed by monotonicity per INV-012).

### FR-CONV.6: DNSP Synthetic Finding (PR-03, BASE, lands sixth)

**Description**: After the entire escalation ladder exhausts on a partition agent (rf-analyst or rf-qa partition), emit a synthetic HIGH-severity finding rather than silently aborting the gate. **Emission contract**: `severity: HIGH; source: "synthetic-dnsp"; affected_range: <agent's assigned_files slice>; evidence: <spawn-log path, OR stub citing log absence per failure-mode #3>; recommendation: "Manual review required — partition agent failed twice"`. **Dedup key**: `(assigned_files_range, escalation_ladder_exhaust_point)` — two synthetic findings with identical key collapse into one with a `found N times` note. **All-agents-fail guard preserved**: if zero partition agents succeeded, escalate normally (existing behavior at rf-team-lead.md:417 — 3 fix cycles per phase) and DO NOT emit synthetic. Edits at SKILL.md:574-654 (A.8 research gate) + SKILL.md:872-916 (A.10 task integrity) + rf-analyst.md:60-69 + rf-qa.md:70-77 + rf-qa-qualitative.md:72-78.

**CASE**: B — no conflict (CASE-B = no row in conflict-register; PR-03 is paradigm-neutral). Invariant alignment: zero-trust QA (visible gap > silent abort) + evidence-bound-item (synthetic cites range + log) + parallel-research (N-1 partitions complete).

**Acceptance Criteria for FR-CONV.6**:
- [ ] **Observable behavior**: When a partition agent's escalation ladder exhausts (twice-failed retry), the agent's output stream emits a JSON-or-block finding with `severity: HIGH`, `source: "synthetic-dnsp"`, `affected_range: <range-of-assigned_files>`, `evidence: <log-path-OR-stub>`, `recommendation: "Manual review required — partition agent failed twice"`; two synthetic findings with identical `(assigned_files_range, escalation_ladder_exhaust_point)` collapse with a `found 2 times` note; when zero partitions succeeded, no synthetic emits (existing all-agents-fail escalation runs).
- [ ] **Verification method**: Inject a partition-agent fixture that times out twice; verify synthetic-dnsp finding appears in the gate output with all 5 required fields; inject two identical exhaust events; verify only one finding emits with `found N times`; inject all-agents-fail fixture; verify zero synthetic emits and existing escalation path activates; `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns ≥1 hit per file at the partition-protocol section.
- [ ] **Negative criterion**: Synthetic-dnsp MUST NOT emit before the escalation ladder exhausts (no premature emission) — proposal line 35 all-agents-fail guard runs first; the existing escalation behavior at rf-team-lead.md:417 (3 fix cycles per phase) MUST NOT be replaced or short-circuited; synthetic findings MUST NOT mask real findings — HIGH severity ensures gate-level visibility; the dedup-key collapse MUST NOT cross-cycle (PR-02 monotonicity treats dedup as not-regression per INV-012).

**Dependencies**: FR-CONV.5 (PR-02 monotonicity consumes synthetic-dnsp per INV-012 dedup-key rule).

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| None | All six landings are edits to existing files | n/a |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/agents/rf-qa.md:264-287` | APPEND TB-Add-1..8 to 20-item task-integrity checklist | FR-CONV.1, FR-CONV.2 (TB-Add-7+8); single owner per CB-3 per-check classification |
| `src/superclaude/agents/rf-qa.md:70-77` | INSERT DNSP synthetic-finding emission contract in partition protocol | FR-CONV.6; mirror across all partitioned agents |
| `src/superclaude/agents/rf-qa.md:310-313` | INTEGRATE Retry Monotonicity Protocol with 3-fix-cycle | FR-CONV.5; existing loop, additive stop-conditions |
| `src/superclaude/agents/rf-qa-qualitative.md:527-583` | INSERT "Five Adversarial Axes" subsection BEFORE 15-item checklist | FR-CONV.4; overlay-only |
| `src/superclaude/agents/rf-qa-qualitative.md:675-714` | EXTEND output template with `axis` column on Items Reviewed table | FR-CONV.4; annotation requirement |
| `src/superclaude/agents/rf-qa-qualitative.md:72-78` | INSERT DNSP synthetic-finding emission contract in partition protocol (if applicable) | FR-CONV.6; mirror |
| `src/superclaude/agents/rf-qa-qualitative.md:794` | OPERATIONALISE Inherited Structural Verdict passthrough reference | FR-CONV.3; existing rule activation |
| `src/superclaude/agents/rf-analyst.md:60-69` | INSERT DNSP synthetic-finding emission contract in partition protocol | FR-CONV.6; partition-agent host |
| `src/superclaude/agents/rf-task-builder.md:336-359` | INTEGRATE Retry Monotonicity Protocol with per-gate fix-cycle | FR-CONV.5; existing loop |
| `src/superclaude/skills/task-builder/SKILL.md:228-238` | ADD template-selection note: Execution Context header optional | FR-CONV.2 |
| `src/superclaude/skills/task-builder/SKILL.md:574-654` | INSERT DNSP synthetic-finding paragraph in A.8 research gate | FR-CONV.6 |
| `src/superclaude/skills/task-builder/SKILL.md:719` | ADD rf-task-builder spawning instruction for Execution Context block | FR-CONV.2 |
| `src/superclaude/skills/task-builder/SKILL.md:870` | INSERT Retry Monotonicity Protocol subsection | FR-CONV.5 |
| `src/superclaude/skills/task-builder/SKILL.md:872-916` | EXTEND A.10 task-integrity with TB-Add catalogue + DNSP integration | FR-CONV.1, FR-CONV.6 |
| `src/superclaude/skills/task-builder/SKILL.md:898-906` | EXTEND 9-item A.10 checklist to 17 items (9 existing + TB-Add-1..8) | FR-CONV.1 |
| `src/superclaude/skills/task-builder/SKILL.md:923-1000` | EXTEND A.10.5 spawn description with `## Inherited Structural Verdict` block | FR-CONV.3 |
| `src/superclaude/skills/task-builder/SKILL.md:961` | ADD reference to "Five Adversarial Axes" for rf-qa-qualitative | FR-CONV.4 |
| `src/superclaude/skills/task-builder/SKILL.md:1409-1485` | EXTEND output schema with Execution Context block | FR-CONV.2 |
| `src/superclaude/skills/task-builder/SKILL.md:1491-1507` | EXTEND 15-item validation block to mirror TB-Add catalogue | FR-CONV.1 |
| `src/superclaude/skills/task-builder/SKILL.md:1550` | MIRROR Retry Monotonicity Protocol in lower section | FR-CONV.5 |

### 4.3 Removed Files

None. No file, section, or check is removed. Portfolio is strictly additive per A-002 zero-trust governance.

### 4.4 Module Dependency Graph

```
                            ┌──────────────────────────┐
                            │ task-builder/SKILL.md    │
                            │   A.8 research gate      │◄────────FR-CONV.6
                            │   A.10 task-integrity    │◄────────FR-CONV.1, FR-CONV.6
                            │   A.10.5 qualitative     │◄────────FR-CONV.3
                            │   Retry Monotonicity     │◄────────FR-CONV.5
                            │   Output schema (header) │◄────────FR-CONV.2
                            └──────────┬───────────────┘
                                       │ spawn
                                       ▼
                      ┌──────────────────────────────────┐
                      │ rf-task-builder.md               │◄────FR-CONV.2, FR-CONV.5
                      │   generates MDTM + retry loops   │
                      └──────────┬───────────────────────┘
                                 │ spawn-pool
              ┌──────────────────┼──────────────────────┐
              ▼                  ▼                      ▼
        ┌──────────┐      ┌───────────────┐      ┌───────────────────────┐
        │rf-analyst│      │   rf-qa       │─────►│  rf-qa-qualitative    │
        │ partition│      │ partition +   │ pass │  partition (if appl.) │
        │ + DNSP   │      │ A.10 + DNSP   │ thru │  + 5 axes + verdict   │
        │ FR-CONV.6│      │ FR-CONV.1,6   │ FR-3 │  FR-CONV.3, FR-CONV.4 │
        │          │      │ + retry FR-5  │      │  + DNSP FR-CONV.6     │
        └──────────┘      └───────────────┘      └───────────────────────┘

(One-way arrows = read/spawn dependency. Retry loops are within-agent, not cross-agent.
Sequencing: FR-CONV.1 first → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6.)
```

### 4.5 Data Models

The portfolio introduces three persisted/passed structures (text-format inside .md files; no JSON files added):

```yaml
# Execution Context block (FR-CONV.2) — inside generated MDTM task file
"## Execution Context":
  References:        # list of BUILD_REQUEST refs (GOAL, WHY, related-doc IDs)
    - "R-###: <ref-line>"
  Source areas:      # list of named modules/packages — NEVER specific file paths
    - "<package-or-module-name>"
  Key constraints:   # top 1-3 invariants from BUILD_REQUEST
    - "<invariant statement>"

# Inherited Structural Verdict block (FR-CONV.3) — inside rf-qa-qualitative spawn prompt
"## Inherited Structural Verdict":
  rf_qa_table_verbatim: <copy of rf-qa task-integrity table at spawn time>
  prompt_directive: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."
  reinjection_rule: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."

# Synthetic DNSP Finding (FR-CONV.6) — inside agent partition output
synthetic_dnsp_finding:
  severity: HIGH                                # fixed
  source: "synthetic-dnsp"                      # fixed
  affected_range: "<agent's assigned_files slice>"
  evidence: "<spawn-log path, OR stub citing log absence>"
  recommendation: "Manual review required — partition agent failed twice"
  dedup_key: "(assigned_files_range, escalation_ladder_exhaust_point)"
  found_n_times: <int, default 1>               # increments on dedup collapse

# Per-item checklist schema (SP-05 addition) — referenced by NFR-CONV.6
# Operational source: SKILL.md:1452-1457
per_item_schema:
  Description: "<one-line task-item action statement>"
  Context: "<file:line citation OR justified-absence comment>"     # TB-Add-8 enforced
  Acceptance: "<observable success condition>"
  Confidence: "<HIGH|MEDIUM|LOW> — with one-line rationale"
  Verification: "<command, file inspection, or test to confirm Acceptance>"
```

### 4.6 Implementation Order

```
1. FR-CONV.1 (PR-06 Structural Gate Additions)  -- establishes TB-Add catalogue;
                                                    TB-Add-7+8 also satisfy FR-CONV.2 prereq
2. FR-CONV.2 (PR-01 Execution Context Header)   -- validated by TB-Add-7+8 from FR-CONV.1
3. FR-CONV.3 (PR-04 Gate Results Passthrough)   -- inherits TB-Add catalogue dynamically
                                                    (INV-010 sequencing)
4. FR-CONV.4 (PR-07 Adversarial Category Naming)-- composes cleanly with inherited verdict
                                                    (INV-013 ADDRESSED)
5. FR-CONV.5 (PR-02 Retry Monotonicity Guards)  -- specifies how synthetic-dnsp counts
                                                    (INV-012 dedup criterion)
6. FR-CONV.6 (PR-03 DNSP Synthetic Finding)     -- BASE; independent of gate-pipeline edits
                                                    could parallel-land with 5; conventionally last
                                                    (sync-discipline applies portfolio-wide)
```

After all six land: run `make sync-dev` → `make verify-sync` → commit only on PASS (A-001).

## 5. Interface Contracts

### 5.1 CLI Surface

No CLI surface changes. Task-builder is invoked via the Skill tool; BUILD_REQUEST.md remains the sole input contract.

### 5.2 Gate Criteria

Task-builder retains its existing 4-stage gate topology (research / task-integrity / qualitative / end-to-end). FR-CONV.1 extends the rf-qa task-integrity checklist count; FR-CONV.3 establishes a verdict-passthrough channel between A.10 (task-integrity) and A.10.5 (qualitative).

| Step | Gate Tier | Frontmatter / Output Schema | Min Lines | Semantic Checks |
|------|-----------|------------------------------|-----------|-----------------|
| A.8 research gate | rf-analyst partition | DNSP synthetic-dnsp finding (HIGH severity, 5 fields, dedup-key) | n/a (per-partition) | Evidence binding; partition completeness |
| A.10 task-integrity | rf-qa | 9 existing + 8 TB-Add items (17 total); TB-Add-2 is `[ADVISORY]` | 17 items total | Placeholder scan; count bounds; clarification adjacency; DAG; granularity; format consistency; Execution Context reappear; per-item file:line |
| A.10.5 qualitative | rf-qa-qualitative | Inherited Structural Verdict block; 5-axis overlay; Self-Audit | 15 existing items + axes overlay | Drift; contradictions; omissions; weakened criteria; invented content (5 axes annotate the 15) |
| End-to-end | full pipeline | All 5 invariants exercised on synthetic BUILD_REQUEST | n/a | All FR-CONV.* AC negative criteria honored |

### 5.3 Phase Contracts

Inter-phase contract between rf-qa and rf-qa-qualitative (FR-CONV.3 makes this contract explicit; previously implicit):

```yaml
phase_contract:
  producer: rf-qa
  consumer: rf-qa-qualitative
  artifact: "## Inherited Structural Verdict block in spawn prompt"
  schema:
    structural_verdict_table: <markdown table from rf-qa A.10 output>
    directive_text: "PASS items machine-verified — skip structural re-checking;
                     FAIL items machine-verified defects — flag HIGH.
                     Focus on semantic quality."
  freshness_rule: "On fix-cycle re-run, orchestrator re-injects NEW verdict;
                   stale verdicts from prior cycles are FORBIDDEN (INV-002)."
  enumeration_rule: "Checklist enumeration is dynamic — auto-picks up TB-Add catalogue
                     from FR-CONV.1; no manual template edit required (INV-010)."
  consumer_obligation: "MUST produce Self-Audit listing relied-on PASS items AND
                        ≥1 semantic check where rf-qa PASS is insufficient (INV-019)."
  anti_inflation: "Mechanical re-checking SKIPPED for PASS items; semantic verification
                   STILL REQUIRED per rf-qa-qualitative.md:766-775."
  # Added per spec-panel SP-15 (delivery guarantees) and SP-16 (versioning):
  schema_version: "1.0.0"
  delivery_semantics: "at-most-once-per-cycle — exactly one verdict re-injected per fix-cycle re-run"
  failure_mode: "If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5."
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-CONV.1 | Determinism scope — gate outputs deterministic | Gate-results structure (TB-Add-* PASS/FAIL emissions, synthetic-dnsp finding 5 fields, dedup-key) MUST be deterministic for fixed BUILD_REQUEST + fixed source tree | Re-run task-builder on identical BUILD_REQUEST twice; diff the rf-qa A.10 verdict table; structural fields must be byte-identical (semantic prose may differ — that's research-driven) |
| NFR-CONV.2 | Determinism scope — what remains research-driven | Per-item Context field prose (citations and rationale text) and rf-qa-qualitative semantic-check prose remain LLM-research-driven and are NOT required to be byte-deterministic | Diff the prose between two runs; non-byte-equality acceptable; structural fields (axis annotations, finding-counts) must remain byte-equal |
| NFR-CONV.3 | Hidden-input guard (per FR §6.2 F4) | Task-builder MUST NOT read any input outside BUILD_REQUEST + source-tree that could modify behavior; PR-05 advisory mechanism (would have read `.dev/tasks/done/`) is the canonical hidden-input case and is REJECTED for Phase-1 | Behavioral guard: synthetic test where `.dev/tasks/done/` contains 10 fixture tasks with varied tier values MUST produce byte-identical structural output to a run with empty `.dev/tasks/done/` (advisory mechanism not active in Phase-1) |
| NFR-CONV.4 | Token ceiling | ≤10% token-cost increase over pre-merge task-builder baseline per equivalent BUILD_REQUEST | Sample 5 representative BUILD_REQUESTs; record pre-merge and post-merge token counts; ratio must be ≤1.10 |
| NFR-CONV.5 | Wall-clock | No new external dependencies; gate additions are local checks; no synchronous network calls added | Inspect rf-qa.md and SKILL.md diffs for new tool invocations: only existing tools (Read, Grep, Glob, Bash) permitted |
| NFR-CONV.6 | Invariant preservation — self-contained-item | 5-field per-item schema MUST remain operational across all 8 TB-Add checks and the Execution Context header | Synthetic fixture with all 5 fields populated passes all TB-Add checks; same fixture with one field stripped fails TB-Add-1 (placeholder scan) — fails closed |
| NFR-CONV.7 | Invariant preservation — evidence-bound-item | Every per-item Context referencing code surface MUST retain file:line citation OR justified-absence (TB-Add-8 enforces) | Synthetic fixture with bare `Context: src/foo` (no `:N`) fails TB-Add-8; same with `Context: src/foo:42` passes; same with `Context: <none — pure refactor> [justified-absence]` passes |
| NFR-CONV.8 | Invariant preservation — persistent-`.dev/tasks/`-artifact | Research/qa persistence in `.dev/tasks/<task-id>/` MUST remain unchanged | Diff `.dev/tasks/` directory layout pre- and post-merge; no path, no naming pattern altered |
| NFR-CONV.9 | Invariant preservation — zero-trust QA | "Any gap regardless of severity = FAIL" stance (rf-qa.md:140-142) MUST remain operative; no TB-Add or PR-04 mechanism weakens it | Synthetic fixture with 1 LOW finding fails the gate (per rf-qa.md:140-142); FR-CONV.3 inherited verdict does NOT mark items VERIFIED in absence of independent semantic check |
| NFR-CONV.10 | Invariant preservation — parallel-research | rf-analyst / rf-qa partition cohort MUST remain parallel; DNSP fires within-agent-instance, not across the cohort (INV-021) | Spawn-log inspection: N partition agents run concurrently; on one agent's escalation exhaust, N-1 continue to completion before DNSP synthesises a finding |

## 7. Risk Assessment

Risk IDs follow the FINAL-REPORT §9 convention (K-prefix). Severity buckets: low / med / high. All MEDIUM invariant-probe findings (INV-002, INV-003, INV-010, INV-012, INV-015) are addressed via per-FR Acceptance Criteria above and are NOT re-listed as risks. LOW unaddressed invariants (INV-006, INV-017, INV-018) are tracked in §11 Open Items.

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| K-001 — TB-Add false positives waste fix-cycles | low | low | Each TB-Add cites its source-check-ID for traceability; TB-Add-2 is `[ADVISORY]` already; FR-CONV.1 negative criterion forbids removing items, but each TB-Add can be individually disabled by reverting its append line |
| K-002 — Execution Context header drift (header says X, items say Y) | low | low | TB-Add-7 cross-validates header source-areas reappear in items; on drift, gate fails and rf-task-builder retries; header is optional (degrades to References-only) |
| K-003 — PR-04 passthrough causes inflation despite anti-inflation rule | low | med | INV-019 acceptance criterion mandates Self-Audit listing on first run; X-002 unresolved tension flagged as audit target — first 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited; if any run shows inflation, disable passthrough and fall back to current behavior |
| K-004 — 5-axis annotation ambiguity over-flags items | low | low | Axes are annotation-only; the existing 15-item checklist still runs; severity floor preserved; `drift-axis-inactive` annotation surfaces when GOAL-baseline missing rather than silently mis-classifying |
| K-005 — Retry monotonicity halts legitimate slow-cycle correction | low | low | Strict-shrink threshold (`F_{n+1} >= F_n`); any forward motion permits continuation; X-003 "halt on slow convergence" explicitly REJECTED; rollback by disabling guards individually |
| K-006 — Synthetic-dnsp findings mask real issues (FINAL-REPORT §9 K3 analogue) | low | low | HIGH severity ensures gate-level visibility; all-agents-fail guard preserves existing escalation path; dedup-key prevents over-emission while preserving the failure signal |
| K-007 — PR-04 + PR-06 sequencing inversion (PR-04 lands before PR-06) | low | med | Sequencing rule PR-06 → PR-04 enforced (FR-CONV.1 lists before FR-CONV.3 in §4.6); PR-04 prompt uses dynamic checklist enumeration so it richens automatically when TB-Add items go live (INV-010 mitigation) |
| K-008 — INV-018 `.dev/tasks/` directory structure changes invalidate all 7 proposals | low | high | Portfolio-wide note; if directory structure changes, re-integrate all 7 proposals at the new layout; tracked in §11 Open Items |
| K-009 — sync-discipline (A-001) violated: `.claude/` edited directly without `make verify-sync` | low | med | All FRs name `src/superclaude/` paths exclusively; CLAUDE.md mandates the sync workflow; `make verify-sync` MUST pass before commit (cross-cutting AC) |
| K-010 — Token ceiling NFR-CONV.4 exceeded by >10% | low | low | Empirical measurement post-merge per NFR-CONV.4; if exceeded, profile per-FR contribution and revise FR-CONV.3 Inherited Structural Verdict block content (verdict table can be summarised rather than verbatim) |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_tb_add_1_placeholder_scan_fires` | `tests/task_builder/test_structural_gate.py` | FR-CONV.1 TB-Add-1: synthetic fixture with `Item 1.1: TODO` fails the gate with item-ID-naming error |
| `test_tb_add_2_advisory_does_not_block` | `tests/task_builder/test_structural_gate.py` | FR-CONV.1 TB-Add-2: 60-item track emits `[ADVISORY]` but gate passes |
| `test_tb_add_4_dag_circular_detection` | `tests/task_builder/test_structural_gate.py` | FR-CONV.1 TB-Add-4: Item 1.1 depends on 1.2, 1.2 depends on 1.1 → gate fails |
| `test_tb_add_7_execution_context_reappear` | `tests/task_builder/test_structural_gate.py` | FR-CONV.1 + FR-CONV.2 TB-Add-7 cross-validation: header source-area `auth` must appear in ≥1 item |
| `test_tb_add_8_per_item_file_line_or_justified_absence` | `tests/task_builder/test_structural_gate.py` | FR-CONV.2 + FR-CONV.1 TB-Add-8: bare `src/foo` Context fails; `src/foo:42` passes; `[justified-absence]` passes |
| `test_execution_context_header_no_paths` | `tests/task_builder/test_header_block.py` | FR-CONV.2: header block contains References / Source areas / Key constraints; grep for `src/.*:[0-9]+` inside header range returns 0 |
| `test_execution_context_minimal_buildrequest` | `tests/task_builder/test_header_block.py` | FR-CONV.2 PR-01 failure-mode #2: minimal BUILD_REQUEST yields References-only header |
| `test_inherited_structural_verdict_present` | `tests/task_builder/test_passthrough.py` | FR-CONV.3: rf-qa-qualitative spawn prompt contains `## Inherited Structural Verdict` + directive text |
| `test_inherited_verdict_reinjection_on_fix_cycle` | `tests/task_builder/test_passthrough.py` | FR-CONV.3 INV-002: cycle 2 spawn prompt contains cycle-2 verdict, NOT cycle-1 verdict |
| `test_self_audit_required_on_first_run` | `tests/task_builder/test_passthrough.py` | FR-CONV.3 INV-019: rf-qa-qualitative output contains `## Self-Audit` with ≥1 semantic-engagement entry |
| `test_five_axes_overlay_present` | `tests/task_builder/test_adversarial_axes.py` | FR-CONV.4: output contains "Five Adversarial Axes" subsection AND Items Reviewed table has `axis` column |
| `test_drift_axis_inactive_when_no_goal_baseline` | `tests/task_builder/test_adversarial_axes.py` | FR-CONV.4 PR-07 failure-mode #3: absence of GOAL-baseline item surfaces `drift-axis-inactive` |
| `test_monotonicity_halt_on_non_shrink` | `tests/task_builder/test_retry_guards.py` | FR-CONV.5: F_1=5, F_2=5, F_3=5 → halt at cycle 2 with `[HALT-MONOTONICITY]` |
| `test_regression_halt_overrides_monotonicity` | `tests/task_builder/test_retry_guards.py` | FR-CONV.5: Item 3.2 PASS@1/FAIL@2 → regression halt before monotonicity check |
| `test_synthetic_dnsp_dedup_not_regression` | `tests/task_builder/test_retry_guards.py` | FR-CONV.5 + FR-CONV.6 INV-012: same `(range, exhaust_point)` across cycles does NOT trigger regression halt |
| `test_independent_counters_not_collapsed` | `tests/task_builder/test_retry_guards.py` | FR-CONV.5 INV-001: 4 retry counters maintain separate monotonicity history |
| `test_dnsp_emits_5_fields_with_dedup_key` | `tests/task_builder/test_synthetic_dnsp.py` | FR-CONV.6: synthetic finding has severity=HIGH, source=synthetic-dnsp, affected_range, evidence, recommendation; dedup-key recorded |
| `test_dnsp_dedup_collapse_found_n_times` | `tests/task_builder/test_synthetic_dnsp.py` | FR-CONV.6: two identical synthetic findings collapse to one with `found 2 times` |
| `test_dnsp_all_agents_fail_guard` | `tests/task_builder/test_synthetic_dnsp.py` | FR-CONV.6: zero partitions succeeded → no synthetic emits; existing escalation path runs |
| `test_dnsp_does_not_serialize_cohort` | `tests/task_builder/test_synthetic_dnsp.py` | FR-CONV.6 INV-021: on one agent's exhaust, N-1 partitions continue to completion |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `test_end_to_end_all_5_invariants` | Full pipeline against synthetic BUILD_REQUEST exercising all 5 invariants (self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research) — see §8.3 below |
| `test_sequencing_PR06_before_PR04` | FR-CONV.1 lands before FR-CONV.3 (INV-010); FR-CONV.3 dynamic enumeration picks up TB-Add items from FR-CONV.1 |
| `test_sequencing_PR06_before_PR01` | FR-CONV.1 TB-Add-7+8 live before FR-CONV.2 header generation; cross-validation runs in A.10 before A.10.5 spawn (INV-011) |
| `test_PR02_PR03_composition` | FR-CONV.5 + FR-CONV.6: synthetic-dnsp counts as failure for `|F_n|` BUT dedup-key not regression (INV-012) |
| `test_PR04_PR07_composition` | FR-CONV.3 + FR-CONV.4: 5 axes apply only to items NOT covered by inherited PASS (INV-013) |
| `test_hidden_input_guard` | NFR-CONV.3: fixture-populated `.dev/tasks/done/` produces byte-identical structural output to empty `.dev/tasks/done/` (PR-05 deferred; hidden-input guard holds) |
| `test_sync_discipline_post_merge` | A-001: `make sync-dev && make verify-sync` PASS after all 6 FRs land |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| End-to-end synthetic BUILD_REQUEST | (1) Construct BUILD_REQUEST with GOAL, WHY, 3 source-areas, 5 invariants; (2) Run task-builder skill; (3) Inspect generated MDTM task; (4) Inspect rf-qa A.10 verdict; (5) Inspect rf-qa-qualitative output | (1) MDTM contains Execution Context header with References/Source-areas/Key-constraints; (2) Per-item Context fields retain file:line citations (TB-Add-8); (3) Inherited Structural Verdict re-injected in rf-qa-qualitative spawn (INV-002); (4) Five Adversarial Axes overlay rendered; (5) Self-Audit lists relied-on PASS items + ≥1 semantic check (INV-019) |
| Fix-cycle regression scenario | (1) Inject synthetic 2-cycle fixture where Item 3.2 PASS@1/FAIL@2; (2) Run task-builder fix loop | Halt at cycle 2 with verbatim regression message; halt precedes monotonicity check |
| Partition-agent escalation exhaust | (1) Inject rf-analyst partition fixture that times out twice; (2) Allow remaining N-1 partitions to complete | Synthetic-dnsp finding with all 5 fields emits; N-1 partitions reach completion (no serialization); dedup-key recorded |
| Audit-after-FR-CONV.3-lands | (1) Run task-builder on first 5 real BUILD_REQUESTs after FR-CONV.3 lands; (2) Inspect each rf-qa-qualitative Self-Audit | All 5 Self-Audits show ≥1 semantic check beyond inherited PASS; no inflation detected; if any audit shows inflation, fail K-003 gate and disable FR-CONV.3 |

## 9. Migration & Rollout

- **Breaking changes**: None. Every FR is strictly additive (A-002 zero-trust governance). No existing rf-qa check, rf-qa-qualitative checklist item, gate stage, output field, or directory layout is removed or renamed.
- **Backwards compatibility**: Generated MDTM task files from pre-merge task-builder remain valid post-merge — the Execution Context header is OPTIONAL (FR-CONV.2 degrades to References-only on minimal BUILD_REQUEST); the TB-Add catalogue items can each be individually disabled via revert of their append line if false-positive volume becomes unacceptable.
- **Rollout sequencing**: Strict per §4.6 order — FR-CONV.1 → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6. Each FR ships independently per its own acceptance criteria (no batched merge required). Each FR's PR passes `make verify-sync` before merge.
- **Rollback plan**: Each FR is revertable via single-PR reversion of its specific edit lines (see §4.2). Default rollback granularity: per-FR. Rollback impact: low — none of the FRs has downstream-consumer schema dependencies outside task-builder's own files.

  **Rollback dependency matrix (SP-10)** — per-FR rollback is not actually independent in two cases:
  | Reverted FR | Required co-revert | Reason |
  |-------------|-------------------|--------|
  | FR-CONV.5 (PR-02 monotonicity) | FR-CONV.6's dedup-key emission | INV-012 composition: monotonicity logic consumes dedup-key |
  | FR-CONV.1 (TB-Add catalogue) | FR-CONV.3 dynamic-enumeration consumer | FR-CONV.3 reads TB-Add catalogue at spawn time; absence yields empty checklist |
  All other FR pairs are mutually rollbackable.

- **`.dev/tasks/` stability commitment (SP-33)**: The `.dev/tasks/` directory layout is treated as a stable contract for the scope of this release. Future structural changes require either (a) a coordinated re-integration commit covering all six FRs that read or write the layout, or (b) introduction of a versioning mechanism for the layout (deferred — see §11 OPEN-INV-018). Without this commitment, K-008 mitigation degrades from "portfolio-wide note" to "portfolio-wide invalidation".

- **Sequencing reconciliation (SP-26)**: §4.6 lists six FRs in strict serial order. The narrative in §4.5 Implementation Order describing "could parallel-land with 5" for FR-CONV.6 is **non-binding advisory text**. The binding sequence is §4.6's serial order (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03). No parallel-land tolerance is permitted for SKILL.md:872-916 since FR-CONV.1 and FR-CONV.6 both edit overlapping ranges in that band (see §4.2).

- **PR-05 Phase-2 trigger**: When `.dev/tasks/done/TASK-RF-*` count ≥10 with frontmatter `tier` + `task_type` populated across ≥3 distinct task_types, re-run adversarial scoring on PR-05 with new data context. If verdict flips to ADOPT, draft Phase-2 release-spec as a follow-on; if verdict remains REVISE, document and close.

## 10. Downstream Inputs

### For sc:roadmap

Not in this release's scope. Task-builder convergence does not require a new roadmap — the v3.8 roadmap covered the original RF→SC direction; this release is the inverse-direction merge of the same paradigm.

### For sc:tasklist

Not in this release's scope. PRD generation (Phase 8 of the orchestration) precedes any tasklist generation for implementation. The PRD will translate the 6 FRs above into product-level requirements for the `prd` skill; tasklist generation occurs post-PRD.

### For prd skill (Phase 8 of this orchestration)

Each FR section is structured to feed directly into the `prd` skill:
- **FR title + Description** → PRD feature title + description
- **Three-field Acceptance Criteria** → PRD acceptance criteria (Observable/Verification/Negative map to PRD's `✅ [Criterion]` style with verification + counterfactual sub-bullets)
- **CASE classification + invariant-protected** → PRD risk/constraint section
- **NFR-CONV.* table** → PRD non-functional requirements
- **Risk table** → PRD risk analysis (§20 in `prd_template.md`)
- **Test plan** → PRD success metrics + measurement section (§19 in `prd_template.md`)

### For implementation (post-PRD)

- Six edit-batches per §4.2; sequenced per §4.6
- All edits flow through `src/superclaude/` → `make sync-dev` → `.claude/` (per CLAUDE.md sync workflow)
- Acceptance gates per FR are the unit-test fixtures listed in §8.1

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OPEN-PR05 | When does `.dev/tasks/done/` reach the ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05? | Determines Phase-2 release timing | Re-check at each major release; document in `KNOWLEDGE.md` |
| OPEN-INV-006 | Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track) | TB-Add-2 stays `[ADVISORY]` until calibrated | Phase-2 with PR-05 (same data dependency) |
| OPEN-INV-017 | Historical-file staleness check for PR-05 advisory citations | Academic given PR-05 Phase-2 deferral | Resolve when PR-05 re-evaluated |
| OPEN-INV-018 | If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration | Portfolio-wide blast radius | Document layout-change contract; re-integrate on demand |
| OPEN-X-002 | PR-04 anti-inflation operational test — "reliance ≠ verification" distinction is empirically observable, not structurally provable | First 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited (K-003 mitigation) | Post-merge audit per §8.3 row 4 |
| OPEN-TOKEN | NFR-CONV.4 token-ceiling empirical measurement | Confirms ≤10% increase target | Post-merge measurement on 5 representative BUILD_REQUESTs |

## 12. Brainstorm Gap Analysis

Phase 3 of the orchestration produced 7 proposals (PR-01..PR-07) from 10 importable matrix-sc-only rows + 5 FR mechanisms (FINAL-REPORT R1..R5). The 7 proposals collectively cover the inverse-direction port surface. Below: rows / mechanisms that were NOT promoted to proposals, and the rationale.

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|------------------|---------|
| GAP-M-SC-01 | Blanket-determinism import — make ALL task-builder outputs byte-deterministic | high | §6 NFR (NFR-CONV.1/2 scope-limits this deliberately) | analyzer |
| GAP-M-SC-13 | No-loop import — adopt `/sc:tasklist`'s "no loop after spot-check" rule | high | §3 FR-CONV.5 (PR-02 establishes guarded loops INSTEAD of no-loop) | analyzer |
| GAP-M-SC-14 | Write-atomicity import — adopt full bundle-validation-before-write | med | §3 FR-CONV.6 (PR-03 emits in-stream; no bundle-write semantics applicable) | analyzer |
| GAP-FR-R3 | Gate-results-passthrough as JSON FILE (`validation/gate-results.txt`) | low | §5.3 Phase Contracts (FR-CONV.3 uses in-prompt block, not file) | backend |
| GAP-FR-R5 | Tier calibration advisory rendered in tasklist-index.md | (deferred) | §11 Open Items OPEN-PR05 | analyzer |

**Gap analysis summary**: The three M-SC-* gaps (blanket determinism, no-loop, write-atomicity) were REJECTED per CB-5 invariant conflict. Rationale: task-builder operates in an execution context where (a) full determinism would break the LLM-research-driven semantic-check prose that rf-qa-qualitative produces (NFR-CONV.2 explicitly preserves this); (b) no-loop would forfeit the retry-and-converge benefit that task-builder's existing 3-fix-cycle architecture provides (rf-team-lead.md:417); (c) write-atomicity assumes a multi-file bundle output, but task-builder emits a single MDTM task file in-place — atomicity is the file system's `mv`, not a pre-write gate. The two FR gaps (R3 file-form, R5 deferred) are tracked: R3 was a deliberate design choice for in-prompt passthrough (lower latency, no extra IO); R5 is the PR-05 Phase-2 deferral. Total proposals: 7, total accepted-in-Phase-1: 5 ADOPT + 1 REVISE-then-adopt (6 FRs); 1 deferred (PR-05); zero rejected outright.

---

## 13. Release Lifecycle Procedures

> **Added post-tag (2026-05-19) to resolve doc drift.** The v3.9 tag message and `CP-P07-END.md` cite `release-spec §19.4` (rollback) and `release-spec §8.3` (GA-tagging-committee approval). §19.4 was never authored; §8.3 in this spec is the "Manual / E2E Tests" table (which correctly contains the K-003 audit at row 4, but does not contain an approval clause). The canonical content now lives in §13.1 and §13.2 below. Pre-tag artifact citations to §19.4 and §8.3-as-approval-clause should be read as §13.1 and §13.2 respectively. The inscribed v3.9 tag message preserves its original section numbers as a historical record.

### 13.1 Rollback Procedure

**Authority**: This section is the canonical rollback procedure. The detailed step-by-step is maintained in `artifacts/D-0099/spec.md §4` (verbatim) — this subsection summarizes it.

**Trigger conditions** (any one is sufficient):

- K-003 FINAL-PASS reports `tier_drift_count > 0` or `compliance_breakage_observed = true` within the OPS-001 4-business-hour SLA window.
- A post-tag invariant probe (NFR-CONV-* family) returns FAIL on a contract that passed at TRACKING-PASS.
- Committee disposition flips from APPROVE to REVOKE (see §13.2).

**Step sequence** (full detail in `D-0099/spec.md §4`):

1. **Tag deletion** — delete the local and remote `v3.9` tag. Local: `git tag -d v3.9`. Remote: `git push origin :refs/tags/v3.9`. The branch SHA remains; only the tag is removed.
2. **Per-FR revert sequence** — revert the FR-CONV.1..6 land sequence in reverse order:

    ```bash
    for sha in 87c8254 db6166e 487e76b ad083b6 2648be8 9d1e51b; do
      git revert --no-edit "$sha"
    done
    ```

3. **Sync + verify** — run `make sync-dev` and `make verify-sync`, then `make test`. All 53/53 checkpoint tests + the NFR-CONV invariant suite must pass on the reverted tree.
4. **Partial rollback** — if only a subset of FRs is implicated, revert only those SHAs (newest-first within the subset). Document the partial-revert SHA list in `D-0099/spec.md §4.2` addendum.
5. **Post-rollback obligations** — file the rollback ADR under `decisions.md` with disposition `REVOKE` and a pointer to the K-003 or invariant-probe artifact that triggered it. Notify the committee within 1 business hour.
6. **Re-tag-on-recovery** — once the root cause is fixed and the invariant suite is green for two consecutive runs, the committee may re-issue an APPROVE disposition (§13.2). Re-tag as `v3.9.1` (do not reuse `v3.9`).

### 13.2 GA-Tagging-Committee Approval Gate

**Input artifacts** (all must be present and current as of the disposition timestamp):

- `results/gate-kpi-report.md` — gate pass/fail KPI summary, 21/21 gates required.
- `results/release-retrospective.md` — phase-by-phase narrative and token accounting.
- `manifest.json` — checkpoint manifest with `total`, `found`, `missing` counts; missing checkpoints must be ADR-justified.
- `artifacts/D-0099/spec.md` — rollback spec (§13.1 above).
- K-003 TRACKING-PASS report (FINAL-PASS may be deferred to the SLA window post-tag per OPS-001).

**Approval criteria** (all four must hold for APPROVE):

1. **Gate completeness** — gate-kpi-report shows ≥21/21 gates passed OR any missing gate has an ADR with disposition `WAIVE` or `DEFER`.
2. **Invariant coverage** — the NFR-CONV invariant suite reports green (no new FAILs vs. the pre-FR-CONV.1 baseline).
3. **Compliance-tier integrity** — no STRICT-tier task in the release shows `tier_drift_count > 0` between TRACKING-PASS and the disposition timestamp.
4. **Rollback readiness** — §13.1 procedure has been dry-run-validated against the candidate tag SHA (revert sequence applies cleanly on a throwaway branch).

**Dispositions**:

- **APPROVE** — local tag may be pushed to origin. Tag message footer must cite §13.1 / §13.2. Remote push is the committee-authorized action; no further approval is required for branch push of the same SHA.
- **HOLD** — local tag remains; remote push gated until the named blocker is resolved. Blocker is recorded in `decisions.md` with target-resolution-date.
- **REJECT** — the candidate SHA is not tag-eligible. Re-cut from a new SHA after the named defect is fixed. The rejected SHA may still be branch-merged if it carries non-tagged value.
- **REVOKE** (post-tag) — triggers §13.1 rollback. Recorded in `decisions.md` with the triggering K-003 / invariant-probe artifact.

**Out of scope**: This gate governs the **tag** push only. Branch pushes (master, integration, feature branches) follow the standard Git workflow in `CLAUDE.md` and do not require committee disposition.

---

## Appendix A: Conflict Register Summary

(Copied verbatim from `conflict-register.md` — append-only ledger of CASE-A/CASE-D decisions per G6 four-case conflict rule.)

| proposal-id | case | sc-mechanism | tb-behavior-or-silence | disposition | invariant-protected | rationale |
|-------------|------|--------------|------------------------|-------------|---------------------|-----------|
| PR-01 | D | sc:tasklist `## Execution Context` block (FINAL-REPORT §7-R2): roadmap-refs + source-areas, no specific paths at task header | task-builder has per-item self-contained 5-field schema (SKILL.md:900, 1452-1457) but no task-LEVEL executor-view summary | ADOPT-ADAPTED: import task-level header block; confine "source areas only" rule to header; per-item Context fields and research/*.md retain file:line citations | evidence-bound-item | task-builder's per-item evidence binding to file:line (SKILL.md:1530 rule #2) must remain — partial scope-of-rule keeps the invariant intact while gaining executor-readability |
| PR-02 | D | sc:tasklist Stages 9-10 monotonicity guard + regression detection + full-set re-validation (FINAL-REPORT §7-R4, §6.2 F2 oscillation) | task-builder has independent retry counters (SKILL.md:651/859/865/870, rf-task-builder.md:336-359) but no monotonicity or regression stop-conditions | ADOPT-ADAPTED: add the two stop conditions to existing retry loops; no new loop stage; full-set re-validation already implicit (gate runs full checklist each cycle) | zero-trust QA | existing 4-stage gate pipeline + multi-cycle retries are the host; the SC mechanism plugs in as stricter halt-conditions (preserving Bucket D rf-qa.md:140-142 "any gap = FAIL"), rather than replacing fix cycles |
| PR-05 | D | sc:tasklist feedback-log advisory (FINAL-REPORT §7-R5; §6.2 F4 advisory-only resolves hidden-input) | task-builder tier selection is rule-based (Quick/Standard/Deep, SKILL.md:88-101) with no feedback infrastructure | ADOPT-ADAPTED: read frontmatter (`tier`, `task_type`) of `.dev/tasks/done/TASK-RF-*/TASK-RF-*.md` for pattern surfacing; explicit "advisory only" disclaimer; tier remains rule-based selection | evidence-bound-item | advisory must cite specific historical task file paths (advisory itself = evidence); reading frontmatter only (not body) avoids privacy leakage; protects existing rule-based selection from being short-circuited by historical pattern-matching |
| PR-06 | D | sc:tasklist 17-point gate structural checks 11/13/14/15/16/17 (Bucket A SKILL.md:1000, 1025-1029) | task-builder's 9-item task-integrity (SKILL.md:898-906) and 15-item validation (SKILL.md:1491-1507) overlap on basics but lack: placeholder/TBD scan, item-count bounds, clarification-adjacency, circular-dep detection, granularity-split enforcement, format consistency | ADOPT-ADAPTED per CB-3: import only the 4-6 unique checks; cite each by source-check-ID; bundle-specific checks (phase-file naming, index references) excluded as inapplicable to single-MDTM output | zero-trust QA | additive checks strengthen existing gate without redundancy; preserves the 4-stage gate topology (Bucket C: 4 vs sc:tasklist's 1); each import is per-check per CB-3 advisory |
| PR-07 | D | sc:tasklist 5-category adversarial agent prompt (Bucket A SKILL.md:1112-1117): drift / contradictions / omissions / weakened-criteria / invented-content | task-builder's rf-qa-qualitative has generic adversarial stance (8× repetition of "find what was missed") but no named 5-axis taxonomy | ADOPT-ADAPTED per CB-3: add 5 named axes as an overlay header on the existing 15-item checklist; axes annotate finding-source, do not replace items | zero-trust QA | lightest-touch import — naming-only annotation; existing 15 checks still run; axes sharpen adversarial stance without replacing rf-qa-qualitative's own checklist topology (Bucket D rf-qa-qualitative.md:527-583) |

PR-03 and PR-04 are CASE-B (no conflict) — correctly absent from the ledger per G6 four-case rule.

## Appendix B: Per-Proposal Verdict Summary

(Copied from `adversarial/per-proposal-verdicts.md`.)

| Proposal | Verdict | CASE | Combined Score | Lands |
|----------|---------|------|----------------|-------|
| PR-01 execution-context-header | REVISE-then-adopt | D | 0.912 | FR-CONV.2 (2nd) |
| PR-02 retry-monotonicity-guards | ADOPT | D | 0.965 | FR-CONV.5 (5th) |
| PR-03 dnsp-synthetic-finding (BASE) | ADOPT (BASE) | B | 0.959 | FR-CONV.6 (6th) |
| PR-04 gate-results-passthrough | ADOPT | B | 0.934 | FR-CONV.3 (3rd) |
| PR-05 tier-history-advisory | REVISE (Phase-2 deferral) | D | 0.862 | DEFERRED |
| PR-06 structural-gate-additions | ADOPT | D | 0.963 | FR-CONV.1 (1st) |
| PR-07 adversarial-category-naming | ADOPT | D | 0.913 | FR-CONV.4 (4th) |

**Counts**: ADOPT 5 (PR-02, PR-03, PR-04, PR-06, PR-07) + REVISE-then-adopt 1 (PR-01) + DEFER 1 (PR-05) + REJECT 0.

## Appendix C: Invariant-Probe Summary

(Copied from `adversarial/invariant-probe.md` — Round 2.5 fault-finder analysis.)

- **Total findings**: 21
- **ADDRESSED**: 13
- **UNADDRESSED**: 8 — **HIGH = 0** (convergence NOT blocked); MEDIUM = 5 (all routed through per-FR acceptance criteria); LOW = 3 (in §11 Open Items)

**MEDIUM warnings — all addressed via per-FR Acceptance Criteria**:
- INV-002 PR-04 verdict re-injection on subsequent fix cycles → FR-CONV.3 AC
- INV-003 PR-05 advisory operational obedience → PR-05 Phase-2 deferral
- INV-010 PR-04 + PR-06 sequencing → FR-CONV.3 dynamic enumeration + §4.6 sequencing
- INV-012 PR-02 + PR-03 composition → FR-CONV.5 dedup-key criterion
- INV-015 PR-01 scope-confinement test → FR-CONV.1 TB-Add-8

**LOW notes** (in §11 Open Items):
- INV-006: PR-06 TB-Add-2 bounds Phase-2 calibration deferral (already `[ADVISORY]`)
- INV-017: PR-05 historical file staleness check (academic given Phase-2 deferral)
- INV-018: directory-structure assumption (portfolio-wide note)

## Appendix D: Constraints — G6 Four-Case Conflict Rule

The portfolio's CASE-A/B/C/D classification follows the G6 four-case conflict rule (per orchestration spec):

- **CASE-A**: `/sc:tasklist` has a mechanism; task-builder has a conflicting mechanism. Disposition: explicit decision; one of {ADOPT-ADAPTED, REJECT}. Required: conflict-register row naming the conflicting mechanism and the protected invariant.
- **CASE-B**: `/sc:tasklist` has a mechanism; task-builder is silent (no conflict). Disposition: ADOPT (or ADOPT-ADAPTED). No conflict-register row required.
- **CASE-C**: `/sc:tasklist` is silent; task-builder has a mechanism. Disposition: keep task-builder behavior; nothing to import.
- **CASE-D**: `/sc:tasklist` has a mechanism; task-builder has a *related but non-conflicting* mechanism (e.g., overlapping scope without contradiction). Disposition: ADOPT-ADAPTED with scope-confinement or per-check classification (CB-3). Required: conflict-register row naming the `/sc:tasklist` mechanism and the protected invariant.

**Portfolio distribution**: PR-01 D, PR-02 D, PR-03 B, PR-04 B, PR-05 D, PR-06 D, PR-07 D. Conflict-register has exactly 5 rows (one per CASE-D proposal); CASE-B proposals (PR-03, PR-04) correctly omitted.

## Appendix E: Excluded Mechanisms

Documented per orchestration spec — REJECT rows from `matrix-sc-only.md` and explicitly-rejected per-proposal extensions (X-001..X-004 from `refactor-plan.md`).

| Excluded mechanism | Source | Rationale |
|--------------------|--------|-----------|
| Bulk-port of all 17 `/sc:tasklist` gate checks | PR-06 alternative | Per CB-3 per-check classification; bundle-specific checks (phase-file naming, index references) inapplicable to single-MDTM output |
| PR-01 "no specific file paths" rule extended to per-item Context fields (X-001) | refactor-plan.md "Rejected" §1 | Would break evidence-bound-item invariant; scope-confinement to header preserved |
| PR-04 verdict reliance without re-running semantic checks (X-002) | refactor-plan.md "Rejected" §2 | Would break anti-inflation rule at rf-qa-qualitative.md:766-775; FR-CONV.3 keeps mechanical-skip + semantic-required |
| PR-02 halt on slow convergence (e.g., F_{n+1} = F_n - 1) (X-003) | refactor-plan.md "Rejected" §3 | Would penalise legitimate multi-cycle correction; FR-CONV.5 uses strict non-shrink only |
| PR-05 tier modification based on historical pattern (X-004) | refactor-plan.md "Rejected" §4 | Hidden-input determinism risk per FINAL-REPORT §6.2 F4; PR-05 deferred entirely |
| M-SC-01 blanket-determinism import | matrix-sc-only.md (Phase 3) | Would break LLM-research-driven semantic prose (NFR-CONV.2 preserves this) |
| M-SC-13 no-loop import | matrix-sc-only.md (Phase 3) | Would forfeit retry-and-converge benefit (rf-team-lead.md:417 3-fix-cycle architecture) |
| M-SC-14 write-atomicity import | matrix-sc-only.md (Phase 3) | Task-builder emits single MDTM file in-place; atomicity is filesystem `mv`, not pre-write gate |
