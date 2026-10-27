---
spec_source: "TDD_TASK_BUILDER_CONVERGENCE.compressed.md"
complexity_score: 0.7
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "opus-architect"
variant_scores: "A:84 B:74"
convergence_score: 0.55
---

# Task-Builder Convergence v3.9 — Project Roadmap

## Executive Summary

This roadmap operationalises the six functional requirements (FR-CONV.1..6) of the Task-Builder Convergence v3.9 release as a strictly serial, per-FR-revertable delivery sequence (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03), plus a post-merge audit-and-measurement milestone. The release is intent-port-only: it adopts five proven sc-tasklist rigor mechanisms into the task-builder skill without copying any code, and preserves five load-bearing invariants (self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research) via dedicated synthetic fixtures (NFR-CONV.6..10). Milestone boundaries align with FR boundaries to make per-FR rollback a first-class roadmap citizen; an M1 architectural-surface map enumerates the six modification points (COMP-001..006) and a consolidated M7 governance table aggregates FLAG-*/MET-*/OPS-* for the GA-readiness audit.

**Business Impact:** Closes three structural-rigor gaps in task-builder's gate topology (no task-level executor-readability summary, no structural gate checks, implicit rubber-stamp passthrough between rf-qa and rf-qa-qualitative) and bounds an empirically-observed retry-oscillation pattern (FINAL-REPORT §6.2 F2: 21-retry / 18-batch loop) at a hard token-cost ceiling of ≤1.10 ratio per equivalent BUILD_REQUEST (NFR-CONV.4). All gate additions are local checks using only existing tools (Read, Grep, Glob, Bash); no new external dependencies, no synchronous network calls, no infrastructure scaling (NFR-CONV.5).

**Complexity:** HIGH (0.7) — driven by ~22 distinct edit points across 5 source files (SKILL.md 1709 lines + 4 rf-* agents totalling ~2067 lines), strict 6-step serial sequencing with no permitted parallelism, and three mutual-composition pairings (FR-CONV.5 ↔ FR-CONV.6 dedup-key, FR-CONV.3 ↔ FR-CONV.1 dynamic enumeration INV-010, FR-CONV.4 ↔ FR-CONV.3 inherited-PASS composition INV-013). Mitigating factors: strictly-additive A-002 governance (no rename / renumber / removal of existing items), per-FR rollback granularity with explicit co-revert matrix, and zero new external dependencies.

**Critical path:** Q-DM-1 schema-contradiction resolution (Engineering Lead) → M1 (TB-Add-1..8 + COMP-001..006 surface map + 3-surface mirror) → M2 (Execution Context header) → M3 (Inherited Structural Verdict + Self-Audit) → M4 (Five Adversarial Axes overlay) → M5 (monotonicity + regression halts) → M6 (synthetic-dnsp on partition exhaust) → M7 (K-003 audit window + NFR-CONV.4 token-cost measurement on 5 representative BUILD_REQUESTs). `make verify-sync` PASS is the per-FR landing gate; failure blocks the next milestone (K-009).

**Key architectural decisions:**

- Intent-port over implementation-port — adapt the *intent* of five sc-tasklist mechanisms re-expressed in task-builder's idiom; only one of the five is a literal source-line lift.
- Strictly-additive A-002 governance with per-FR rollback granularity, governed by a co-revert dependency matrix (FR-CONV.5 ↔ FR-CONV.6 jointly revertable; FR-CONV.1 ↔ FR-CONV.3 INV-010 enumeration dependency).
- Determinism scope split (NFR-CONV.1 byte-identical structural fields; NFR-CONV.2 LLM-driven prose nondeterminism acceptable) — gate verdicts driven by structured output, semantic prose intentionally excluded from determinism scope.
- Anti-inflation rule at `rf-qa-qualitative.md:766-775` treated as absolute — FR-CONV.3 inherited verdict is a deliberately-scoped RELIANCE channel for structural items only, gated by INV-019 Self-Audit obligation and the K-003 first-5-runs audit.
- M1 contract-freeze rows for DM-001..005, API-001..004, COMP-001..006 — provides a single milestone-boundary checkpoint for architectural-surface drift before per-FR work begins, complementing TDD-level contracts with roadmap-level commitment.

**Open risks requiring resolution before M1:**

- Q-DM-1 — PRD §25.4 declares per-item schema `{Description, Context, Acceptance, Confidence, Verification}` "preserved unchanged" at `SKILL.md:1452-1457`, but current source holds `{Context, Action, Output, Verification, Completion gate}`. Engineering Lead decision required before TB-Add-8 can be authored against a stable baseline (CRITICAL blocker).

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|FR-CONV.1 / PR-06 — Architectural Surface Map + Structural Gate Additions (TB-Add-1..8)|Foundation|P0|L|Q-DM-1 resolved|31|Medium|
|M2|FR-CONV.2 / PR-01 — Execution Context Header|Foundation|P0|S|M1|17|Low|
|M3|FR-CONV.3 / PR-04 — Inherited Structural Verdict + Self-Audit|Core Logic|P0|M|M2; TB-Add catalogue (INV-010)|21|Medium|
|M4|FR-CONV.4 / PR-07 — Five Adversarial Axes Overlay|Core Logic|P0|S|M3|20|Low|
|M5|FR-CONV.5 / PR-02 — Retry Monotonicity + Regression Halts|Integration|P0|M|M4; FR-CONV.6 dedup-key shape|21|Low|
|M6|FR-CONV.6 / PR-03 — Synthetic DNSP on Partition Exhaust|Integration|P0|L|M5|29|Low|
|M7|Production Readiness — K-003 Audit + NFR-CONV.4 Measurement + Consolidated Governance + GA|Hardening|P0|M|All FRs landed|26|Medium|

## Dependency Graph

```
M1 (FR-CONV.1, TB-Add-1..8 + COMP-001..006 surface map + DM/API contract-freeze)
  └─► M2 (FR-CONV.2, Execution Context header — depends on TB-Add-7/8 live)
        └─► M3 (FR-CONV.3, Inherited Verdict — depends on TB-Add catalogue INV-010 + TB-Add-7 cross-validation)
              └─► M4 (FR-CONV.4, Five Adversarial Axes — depends on FR-CONV.3 inherited-PASS composition INV-013)
                    └─► M5 (FR-CONV.5, Monotonicity halts — depends on FR-CONV.1 |F_n| count; mutual-shape coupling with M6)
                          └─► M6 (FR-CONV.6, Synthetic DNSP — emits the dedup-key shape M5 consumes)
                                └─► M7 (K-003 audit window + NFR-CONV.4 measurement + consolidated FLAG/MET/OPS → v3.9 GA)
```

**Cross-cutting coupling annotations:**
- **FR-CONV.5 ↔ FR-CONV.6 mutual-shape coupling** (M5/M6): M5 specifies the dedup-key shape it will consume; M6 emits that shape. Co-revertable per §19.4 §SP-10.
- **FR-CONV.3 ↔ FR-CONV.1 INV-010 enumeration dependency** (M3 on M1): The Inherited Verdict checklist auto-richens against the TB-Add catalogue at runtime.
- **FR-CONV.4 ↔ FR-CONV.3 INV-013 composition** (M4 on M3): Adversarial axes focus on the semantic surface that the inherited structural PASS does not cover.

## M1: FR-CONV.1 / PR-06 — Architectural Surface Map + Structural Gate Additions (TB-Add-1..8)

**Objective:** Establish the M1 architectural-surface checkpoint (COMP-001..006 modification points + contract-freeze for DM-001..005 / API-001..004 / NFR-CONV.5 no-new-deps); append 8 structural checks (TB-Add-1..8) to rf-qa task-integrity gate mirrored across all three definition surfaces (rf-qa.md 20-item checklist, SKILL.md A.10 9-item block, SKILL.md 15-item validation block); preserve zero-trust QA invariant; resolve INV-015 evidence-bound-item probe via TB-Add-8. | **Duration:** 2 weeks (2026-05-15 → 2026-05-29) | **Entry:** Q-DM-1 Engineering Lead decision landed; `make verify-sync` clean baseline; design approval. | **Exit:** COMP-001..006 surface map ratified; DM-001..005 + API-001..004 contract shapes frozen at milestone gate; TB-Add-1/3/4/5/6/7/8 fire distinct item-ID-naming errors and block gate on violation; TB-Add-2 emits `[ADVISORY]` and does not block; all 6 M1 fixtures PASS; `make verify-sync` PASS; no existing rf-qa check renamed/renumbered/removed.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-001|task-builder Orchestrator surface anchor|SKILL.md Stage A orchestrator; central integration surface for FR-CONV.1..6|task-builder/SKILL.md|A-001|type:Internal-Framework-Skill; location:src/superclaude/skills/task-builder/SKILL.md; modifies:FR-CONV.1-through-6; dependencies:rf-task-researcher,rf-task-builder,rf-qa,rf-analyst,rf-qa-qualitative; forbidden:direct-rf-team-lead-invocation|S|P0|
|2|COMP-002|rf-task-builder Agent surface anchor|BUILD_REQUEST consumer and MDTM emitter; modified by FR-CONV.5|rf-task-builder.md|API-001|type:Subagent; location:src/superclaude/agents/rf-task-builder.md; modifies:FR-CONV.5; returns:RESEARCH_NEEDED,MALFORMED,NEED_USER_INPUT; output:${TASK_DIR}${TASK_ID}.md; counters:separate-per-gate|S|P0|
|3|COMP-003|rf-qa Agent surface anchor|Structural QA agent — 4 phases; modified by FR-CONV.1, FR-CONV.5, FR-CONV.6|rf-qa.md|FR-CONV.1|type:Structural-QA-Agent; location:src/superclaude/agents/rf-qa.md; phases:research-gate,synthesis-gate,report-validation,task-integrity; modifies:FR-CONV.1,FR-CONV.5,FR-CONV.6; anchors:141-142,268-287,49-77,308-315|S|P0|
|4|COMP-004|rf-qa-qualitative Agent surface anchor|Content QA agent — consumes inherited verdict + axes overlay; modified by FR-CONV.3, FR-CONV.4, FR-CONV.6|rf-qa-qualitative.md|API-002|type:Content-QA-Agent; location:src/superclaude/agents/rf-qa-qualitative.md; phases:7-incl-task-qualitative; modifies:FR-CONV.3,FR-CONV.4,FR-CONV.6; anchors:527-583,675-714,766-775,786-795,794|S|P0|
|5|COMP-005|rf-analyst Agent surface anchor|Completeness verification and synthesis review; partition adversary at Gates 1+2; modified by FR-CONV.6|rf-analyst.md|API-003|type:Completeness-verification-and-synthesis-review; location:src/superclaude/agents/rf-analyst.md; modifies:FR-CONV.6; anchors:58-71; role:partition-adversary-at-gates-1-and-2|S|P0|
|6|COMP-006|rf-team-lead Preservation surface anchor|Existing all-agents-fail escalation guard — UNMODIFIED, line 417 NO-DRIFT verified 2026-05-14|rf-team-lead.md|API-003|type:Project-mode-orchestrator; location:src/superclaude/agents/rf-team-lead.md; modifies:none; preserved_anchor:line-417; behavior:max-3-cycles-per-phase-HALT-and-ask-user; verified:2026-05-14-NO-DRIFT|S|P0|
|7|FR-CONV.1|Append TB-Add-1..8 to rf-qa task-integrity gate|Add 8 strictly-additive structural checks to rf-qa A.10 mirrored across three definition surfaces; preserve zero-trust QA invariant (CASE-D PR-06)|rf-qa.md; SKILL.md|Q-DM-1|TB-Add-1/3/4/5/6/7/8:item-ID-naming-error-on-violation-and-block-gate; TB-Add-2:[ADVISORY]-prefix-does-NOT-block; existing-checks:not-renamed-renumbered-removed; bundle-specific-tasklist-checks:forbidden|M|P0|
|8|TB-Add-1|Placeholder scan check (Hard, blocking)|Detect "TBD"/"TODO"/title-only checklist items; emits item-ID-naming error on violation|rf-qa.md|FR-CONV.1|fixture-placeholder:TB-Add-1-fires; gate-verdict:FAIL; cites:source-check-ID|S|P0|
|9|TB-Add-2|Item-count bounds check (ADVISORY only)|Item-count bounds ≥3 / ≤40-track / ≤50-single-track; emits `[ADVISORY]` prefix and does NOT block gate (pending OPEN-INV-006 calibration)|rf-qa.md|FR-CONV.1|out-of-bounds-fixture:[ADVISORY]-emitted; gate-verdict:not-affected; status:advisory-until-Phase-2|S|P0|
|10|TB-Add-3|Clarification-adjacency check (Hard, blocking)|Detect items requiring clarification not adjacent to their resolving context; blocks gate on violation|rf-qa.md|FR-CONV.1|non-adjacent-clarification:FAIL; item-ID:named-in-error|S|P0|
|11|TB-Add-4|Circular-dependency DAG check (Hard, blocking)|Detect circular intra-/inter-phase dependencies; blocks gate on violation|rf-qa.md|FR-CONV.1|DAG-cycle-fixture:FAIL-with-TB-Add-4; detection:100%-on-synthetic|S|P0|
|12|TB-Add-5|Granularity / XL-has-subtasks check (Hard, blocking)|Detect XL-effort items lacking subtask decomposition; blocks gate on violation|rf-qa.md|FR-CONV.1|XL-without-subtasks:FAIL; item-ID:identified|S|P0|
|13|TB-Add-6|Confidence / Verification format consistency check (Hard, blocking)|Validate per-item Confidence field uses HIGH/MEDIUM/LOW enum + rationale; Verification field is command/inspection/test|rf-qa.md|FR-CONV.1; Q-DM-1|malformed-Confidence-or-Verification:FAIL; format-errors:named-per-item-ID|S|P0|
|14|TB-Add-7|Execution-Context source-areas cross-validation (Hard, blocking)|Validate each Source areas entry from Execution Context header reappears in ≥1 per-item Context field; blocks on drift|rf-qa.md|FR-CONV.1; FR-CONV.2|header-source-area-absent:FAIL; degraded-References-only:tolerated|S|P0|
|15|TB-Add-8|Per-item Context citation check (Hard, blocking; resolves INV-015)|Validate per-item Context field has ≥1 file:line citation OR justified-absence comment|rf-qa.md|FR-CONV.1; Q-DM-1|bare-src/foo:FAIL; src/foo:42:PASS; justified-absence:PASS|S|P0|
|16|DM-001|Execution Context Header schema (contract-freeze)|Freeze DM-001 entity contract at M1 gate; consumed by FR-CONV.2 in M2|SKILL.md|FR-CONV.1|References:list-string-R###; Source-areas:list-string-no-file-paths; Key-constraints:list-string-1-to-3-items; degradation:References-only-when-minimal|S|P0|
|17|DM-002|Inherited Structural Verdict Block schema (contract-freeze)|Freeze DM-002 entity contract at M1 gate; consumed by FR-CONV.3 in M3|SKILL.md|FR-CONV.1|rf_qa_table_verbatim:byte-exact-table; prompt_directive:fixed-string; reinjection_rule:cycle-N-fresh-INV-002|S|P0|
|18|DM-003|Synthetic DNSP Finding schema (contract-freeze)|Freeze DM-003 entity contract at M1 gate; consumed by FR-CONV.5 dedup-key composition (INV-012) and emitted by FR-CONV.6|rf-qa.md|FR-CONV.1; FR-CONV.5|severity:HIGH-fixed; source:synthetic-dnsp-fixed; affected_range:string; evidence:spawn-log-path-or-stub; recommendation:Manual-review-required-fixed; dedup_key:2-tuple-range-exhaust_point; found_n_times:int-default-1|S|P0|
|19|DM-004|Per-Item Checklist Schema (Q-DM-1 blocked; lands whichever schema resolves)|Per-item 5-field schema enforced by TB-Add-6 (format) and TB-Add-8 (Context citation). PRD-asserted: Description:one-line-action; Context:file-line-or-justified-absence; Acceptance:observable-success-condition; Confidence:HIGH-MEDIUM-LOW-enum-with-rationale; Verification:command-inspection-or-test. Current SKILL.md alternative: Context; Action; Output; Verification; Completion-gate. Invariant across resolutions: Context field present in both schemas; TB-Add-8 enforcement holds regardless|SKILL.md|FR-CONV.1; Q-DM-1|all-5-fields-per-Q-DM-1-resolution; TB-Add-6:enforces-Confidence-Verification-format; TB-Add-8:enforces-Context-file:line-or-justified-absence; applies-regardless-of-resolution|S|P0|
|20|DM-005|Phase Contract schema rf-qa → rf-qa-qualitative (contract-freeze)|Freeze DM-005 entity contract at M1 gate; 10-field producer/consumer agreement|SKILL.md|FR-CONV.1|producer:rf-qa; consumer:rf-qa-qualitative; artifact:Inherited-Structural-Verdict-block; schema_version:1.0.0; delivery_semantics:at-most-once-per-cycle; freshness_rule:INV-002-reinject-NEW; enumeration_rule:INV-010-auto-pick-TB-Add; consumer_obligation:INV-019-Self-Audit; anti_inflation:preserve-766-775; failure_mode:halt-A.10-before-A.10.5|S|P0|
|21|API-001|BUILD_REQUEST → MDTM contract (contract-freeze)|Freeze API-001 contract at M1 gate; preserve 15-field BUILD_REQUEST schema with optional EXECUTION_CONTEXT_REQUIREMENTS signal|SKILL.md|FR-CONV.1; DM-001|producer:task-builder; consumer:rf-task-builder; transport:Skill-prompt-plus-on-disk-MDTM; output:Execution-Context-block; error-mode:MALFORMED-max-2-retry|S|P0|
|22|API-002|Structural Verdict Handoff contract (contract-freeze)|Freeze API-002 contract at M1 gate; rf-qa task-integrity → rf-qa-qualitative task-qualitative spawn-prompt injection|SKILL.md|FR-CONV.1; DM-002,DM-005|producer:rf-qa; consumer:rf-qa-qualitative; transport:spawn-prompt-injection; extraction:contiguous-verdict-table; placement:after-TARGET-FILES-before-INSTRUCTIONS; missing-verdict:halt-before-A.10.5|S|P0|
|23|API-003|Partition Finding Stream contract (contract-freeze)|Freeze API-003 contract at M1 gate; partition-agent synthetic DNSP emission into orchestrator merge logic|rf-qa.md|FR-CONV.1; DM-003|producer:any-partition; consumer:task-builder-merge; transport:normal-output-stream; cardinality:per-partition; dedup:within-cycle-found_n_times; all_fail:zero-success-routes-to-rf-team-lead.md:417-NO-DNSP|S|P0|
|24|API-004|Fix-Loop Halt Signals contract (contract-freeze)|Freeze API-004 contract at M1 gate; monotonicity + regression halt-message strings consumed by retry loops|SKILL.md|FR-CONV.1; FR-CONV.5|monotonicity_message:[HALT-MONOTONICITY]-pipe-F-pipe-equals-n; regression_message:verbatim-PASS-at-N-to-FAIL-at-N+1; order:regression-then-monotonicity-then-hard-cap; F_n:dedup-key-set|S|P0|
|25|TEST-001|test_placeholder_tb_add_1|Synthetic fixture asserting TB-Add-1 fires on "TBD"/"TODO"/title-only items|tests|TB-Add-1|TB-Add-1:emits-item-ID-error; gate:FAILs; assertion:grep-on-gate-report|S|P0|
|26|TEST-002|test_dag_cycle_tb_add_4|Synthetic fixture asserting TB-Add-4 fires on circular dependency|tests|TB-Add-4|TB-Add-4:emits; gate:FAILs; detection:100%-on-cycle-fixture|S|P0|
|27|TEST-003|test_evidence_bound_tb_add_8|Three-fixture triple asserting TB-Add-8 behavior on (a) bare path FAIL, (b) file:line PASS, (c) justified-absence PASS|tests|TB-Add-8|three-sub-fixtures-per-spec; resolves:INV-015-probe|S|P0|
|28|MIG-001|M1.1 PR-06 landing migration|Strictly-additive append commits; per-line revertable; `make verify-sync` PASS gate|src/|FR-CONV.1|single-commit:lands-TB-Add-1..8-across-3-surfaces; revert-path:per-TB-Add-line-or-full-commit-documented|S|P0|
|29|NFR-CONV.1|Structural-field determinism instrumentation (M1 scope)|TB-Add-1..8 PASS/FAIL verdicts byte-identical across two runs on same BUILD_REQUEST + source tree|rf-qa.md|FR-CONV.1|two-runs-identical-input; diff-verdict-table; structural-fields:byte-equal|S|P0|
|30|NFR-CONV.5|No new external dependencies — diff inspection gate (contract-freeze at M1)|Constraint frozen at M1: all FR-CONV.X must use only Read/Grep/Glob/Bash; no new MCP servers, no synchronous network calls|src/|FR-CONV.1|diff-inspection:rejects-any-new-tool-beyond-four-tool-set; constraint:applies-to-all-M1-through-M6|S|P0|
|31|FF_TB_ADD_1_THROUGH_8|Feature-flag governance (logical, no runtime flag)|Per-TB-Add revertable-line discipline; TB-Add-2 advisory→hard pending OPEN-INV-006 calibration; consolidated cleanup tracking in M7|git|FR-CONV.1|each-TB-Add:own-line-or-commit; TB-Add-2:stays-ADVISORY-until-Phase-2; owner:rf-qa-maintainer; M7-consolidation:see-M7-governance-table|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|COMP-001..006 architectural-surface map|component registry|ratified-at-M1-gate|M1|All downstream FRs (M2..M7) — single page enumerating 6 modification points (TDD §6.2)|
|TB-Add catalogue (1..8)|registry|append-to-rf-qa-checklist|M1|FR-CONV.3 INV-010 dynamic enumeration (M3); FR-CONV.4 axis overlay (M4)|
|TB-Add-7 source-areas cross-validator|dispatch (regex check)|wired-to-Execution-Context-block|M1|FR-CONV.2 header (M2) — TB-Add-7 must tolerate degraded References-only form|
|TB-Add-8 evidence-bound check|dispatch (regex check)|wired-to-per-item-Context-field|M1|All downstream FRs preserving per-item Context schema (M2..M6)|
|DM-001..005 + API-001..004 contract-freeze|inter-agent contract baseline|frozen-at-M1-gate|M1|FR-CONV.2..6 implementations; change-detection at milestone boundary rather than commit time|
|rf-qa.md:141-142 PASS/FAIL definitions|invariant anchor|preservation-checkpoint|M1|All milestones (NFR-CONV.9 zero-trust QA preservation)|

### Milestone Dependencies — M1

- Q-DM-1 Engineering Lead decision landed (per-item schema authoritative source — see Open Questions below).
- Clean `make verify-sync` baseline before M1 commit (K-009 prevention).
- `rf-team-lead.md:417` NO-DRIFT verified (verified 2026-05-14; K-008 portfolio-wide preservation).
- A-001 source-of-truth workflow accepted (CLAUDE.md sync-discipline).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-DM-1|Per-Item Checklist Schema PRD-vs-source contradiction: PRD §25.4 declares the 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` "preserved unchanged" at `SKILL.md:1452-1457`, but current SKILL.md:1450-1460 holds `{Context, Action, Output, Verification, Completion gate}`. Resolution options: (a) FR-CONV.1/TB-Add-8 LANDS the PRD schema (would contradict A-002 unless treated as net-new); (b) correct the PRD §25.4 pointer to the real operational source; (c) §25.4 describes a separate schema living elsewhere. Source: TDD §22 / PRD §25.4.|CRITICAL — blocks TB-Add-6 / TB-Add-8 authoring; downstream TB-Add validation surfaces depend on which schema lands|Engineering Lead|Pre-FR-CONV.1 implementation (Pre-M1 entry gate)|
|2|OPEN-INV-018|If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration. Document layout-change contract. Source: TDD §22 / OPEN-INV-018.|HIGH (K-008 portfolio-wide) — layout change invalidates every FR-CONV path reference|Engineering Lead|Pre-M1 layout-stability commitment; re-check per release|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M1-1 — TB-Add false positives waste fix-cycles (K-001)|Low|Low|Low|Each TB-Add cites source-check-ID; TB-Add-2 ships as `[ADVISORY]`; individually revertable line|rf-qa maintainer|
|2|R-M1-2 — Q-DM-1 schema ambiguity leads to TB-Add-6/TB-Add-8 against wrong baseline|High|Medium|High|Resolve Q-DM-1 before any TB-Add work; record selected schema in DM-004; pre-M1 entry gate|Engineering Lead|
|3|R-M1-3 — INV-018 `.dev/tasks/` layout change invalidates all FR paths (K-008)|Low|Low|High|Portfolio-wide note; SP-33 stability commitment; re-integration commit contingency covering all 6 FRs|Engineering Lead|
|4|R-M1-4 — Sync-discipline (A-001) violated by direct `.claude/` edit (K-009)|Low|Low|Medium|All FR-CONV.1 paths reference `src/superclaude/` exclusively; CLAUDE.md mandates workflow; revert direct edit and re-run from `src/superclaude/` on failure|Per-commit author|

## M2: FR-CONV.2 / PR-01 — Execution Context Header

**Objective:** Insert task-level `## Execution Context` block (after frontmatter, before checklist) in generated MDTM task files with exactly three labeled lines (References / Source areas / Key constraints); preserve evidence-bound-item invariant; degrade gracefully to References-only on minimal BUILD_REQUEST. | **Duration:** 2 weeks (2026-05-29 → 2026-06-12) | **Entry:** M1 PASS; TB-Add-7/8 live and tolerant of degraded header; DM-001 contract frozen; `make verify-sync` clean. | **Exit:** Header renders three labeled lines for fully-populated BUILD_REQUEST; degrades to References-only for minimal BUILD_REQUEST (other lines explicitly omitted, not blank); `grep -E "src/|/.*:[0-9]+"` against header range returns zero; per-item Context fields retain file:line citations.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.2|Insert task-level Execution Context header|Insert `## Execution Context` block after frontmatter, before checklist; exactly 3 labeled lines (CASE-D PR-01); preserve evidence-bound-item invariant|SKILL.md; rf-task-builder.md|M1|fully-populated:3-labeled-lines; minimal:References-only-others-omitted; per-item-Context:unchanged|S|P0|
|2|DM-001.References|References field emitter|Emit BUILD_REQUEST refs (GOAL, WHY, related-doc IDs) as `R-###: <ref-line>` list entries|rf-task-builder.md|DM-001|References-list:populated-from-GOAL-WHY-related_docs; format:R-###-colon-ref-line; degradation:never-omitted|S|P0|
|3|DM-001.SourceAreas|Source areas field emitter (no file paths)|Emit named modules / packages — hidden-input determinism rule prohibits specific file paths or `file:line` citations|rf-task-builder.md|DM-001|grep-src/-or-file:N-returns-zero-hits; degradation:explicitly-omitted-not-blank-on-minimal|S|P0|
|4|DM-001.KeyConstraints|Key constraints field emitter (1-3 entries)|Emit top 1-3 invariants pulled verbatim from BUILD_REQUEST|rf-task-builder.md|DM-001|bounded:1-to-3-entries; degradation:explicitly-omitted-not-blank-on-minimal|S|P0|
|5|API-001|BUILD_REQUEST → MDTM contract update (M2 implementation)|Implement EXECUTION_CONTEXT_REQUIREMENTS optional signal; generated MDTM file MUST contain `## Execution Context` block at top after frontmatter, before Phase 1|SKILL.md|FR-CONV.2; DM-001|BUILD_REQUEST-15-field-schema:preserved; new-optional-signal:documented; emission-rules:per-fully-populated-vs-minimal; failure-mode:MALFORMED-retry-max-2|S|P0|
|6|DM-005|Phase Contract DM-005 (10 fields, explicit row)|10-field producer/consumer agreement enumerated as standalone row; published at M2 to enable M3 spawn-prompt injection|SKILL.md|FR-CONV.2; M1-contract-freeze|producer:rf-qa; consumer:rf-qa-qualitative; artifact:Inherited-Structural-Verdict-block; schema_version:1.0.0; delivery_semantics:at-most-once-per-cycle; freshness_rule:INV-002-reinject-NEW; enumeration_rule:INV-010-auto-pick-TB-Add; consumer_obligation:INV-019-Self-Audit; anti_inflation:preserve-766-775-byte-stable; failure_mode:halt-A.10-before-A.10.5|S|P0|
|7|Degradation rule|Minimal BUILD_REQUEST degradation behavior|Block degrades to References-only when GOAL is the only populated field; other 2 lines explicitly omitted, not blank-but-present|rf-task-builder.md|DM-001|minimal-fixture:References-only-header; degraded:no-Source-areas-or-Key-constraints-lines|S|P0|
|8|Hidden-input guard|No-file-paths invariant in header|Header MUST NOT contain specific file paths or file:line citations (NFR-CONV.3 hidden-input determinism)|rf-task-builder.md|DM-001|header-grep-src/-or-file:N:zero; TB-Add-7:cross-validates-Source-areas-vs-items|S|P0|
|9|COMP-001|SKILL.md primary template insertion (1407-1487)|Insert Execution Context block specification into MDTM template at SKILL.md:1407-1487|SKILL.md|FR-CONV.2|template-top:after-frontmatter-before-Phase-1; verifiable:grep-Execution-Context-in-SKILL.md|S|P0|
|10|COMP-001|SKILL.md BUILD_REQUEST guidance update (715-725)|Update BUILD_REQUEST prompt guidance near SKILL.md:715-725 with header generation rules|SKILL.md|FR-CONV.2|guidance:enumerates-3-line-vs-degraded; cites:NFR-CONV.3-hidden-input-rule|S|P0|
|11|COMP-002|rf-task-builder header emission logic|Modify rf-task-builder.md to emit `## Execution Context` block at task-file top|rf-task-builder.md|FR-CONV.2|generated-MDTM:contains-header-after-frontmatter-before-Phase-1; failure:MALFORMED-retry-max-2|S|P0|
|12|TEST-004|test_execution_context_full|Fixture asserting 3-labeled-line block in generated MDTM for fully-populated BUILD_REQUEST|tests|FR-CONV.2|grep-matches:all-3-labeled-lines-References-Source-areas-Key-constraints|S|P0|
|13|TEST-005|test_execution_context_minimal_buildrequest|Fixture asserting References-only degradation for minimal BUILD_REQUEST|tests|FR-CONV.2|grep-matches:degraded-References-only; other-2-lines:absent|S|P0|
|14|TEST-006|test_execution_context_no_file_paths|Fixture asserting `grep -E "src/|/.*:[0-9]+"` returns 0 in header range|tests|FR-CONV.2|header-range:0-file:line-hits; per-item-Context-fields-outside-header:still-carry-citations|S|P0|
|15|NFR-CONV.7|Evidence-bound-item invariant preservation|Per-item Context fields MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8 from M1)|rf-task-builder.md|FR-CONV.2; TB-Add-8|three-fixture-triple:bare-FAILS-file:line-PASSES-justified-absence-PASSES; integration-with-TB-Add-8:verified|S|P0|
|16|MIG-002|M1.2 PR-01 landing migration|Strictly-additive header emission; revertable by disabling header generation; per-item Context fields degrade gracefully|src/|FR-CONV.2|single-commit; make-verify-sync:PASS; rollback:disable-header-gen-per-item-Context-unchanged|S|P0|
|17|FF_EXECUTION_CONTEXT_HEADER|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days; owner task-builder maintainer; consolidated cleanup tracking in M7|git|FR-CONV.2|logical-flag; revert:disable-header-generation-block; degraded-form:natural-rollback-target; M7-consolidation:see-M7-governance-table|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`## Execution Context` block|template insertion|wired-to-MDTM-template-top|M2|TB-Add-7 cross-validator (M1, retroactive consumer); all downstream FRs (header is persistent)|
|EXECUTION_CONTEXT_REQUIREMENTS signal|optional BUILD_REQUEST field|wired-to-orchestrator-prompt|M2|task-builder skill orchestrator (SKILL.md:715-725)|
|DM-005 Phase Contract (explicit 10-field row)|inter-agent contract|published-at-M2-for-M3-consumption|M2|FR-CONV.3 spawn-prompt injection (M3)|

### Milestone Dependencies — M2

- M1 PASS (TB-Add-7/8 live and tolerant of degraded header form; DM-001 + DM-005 contract-freeze).
- `make verify-sync` PASS after M1 commit.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M2-1 — Execution Context header drift (header says X, items say Y) (K-002)|Low|Low|Low|TB-Add-7 cross-validates Source areas reappear in per-item Context fields; gate fails on drift; header degrades to References-only as fallback|task-builder maintainer|
|2|R-M2-2 — Per-item evidence migrates from items into the header|Low|Low|Medium|FR-CONV.2 Negative Criterion keeps file:line citations in item Context only; TB-Add-8 enforcement on per-item Context|Engineering|

## M3: FR-CONV.3 / PR-04 — Inherited Structural Verdict + Self-Audit

**Objective:** Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt under `## Inherited Structural Verdict` with directive; add `## Self-Audit` to rf-qa-qualitative output schema; preserve zero-trust QA invariant and the anti-inflation rule at `rf-qa-qualitative.md:766-775` byte-stable; enforce INV-002 freshness, INV-010 dynamic enumeration, INV-019 Self-Audit obligation. | **Duration:** 2 weeks (2026-06-12 → 2026-06-26) | **Entry:** M2 PASS; TB-Add catalogue stable (for INV-010 enumeration); DM-005 published in M2; `make verify-sync` clean. | **Exit:** Spawn prompt carries verdict table byte-for-byte; on fix-cycle re-run orchestrator re-injects NEW cycle-N verdict (INV-002); rf-qa-qualitative output contains Self-Audit listing relied-on PASS items AND ≥1 semantic check; anti-inflation bullet at :770 byte-identical pre/post.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.3|Inject Inherited Structural Verdict + Self-Audit|Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt; add Self-Audit to output schema (CASE-B PR-04); preserve zero-trust QA invariant|SKILL.md; rf-qa-qualitative.md|M2|spawn-prompt:byte-for-byte; re-injection-on-fix-cycle; Self-Audit:lists-relied-on-PASS-and-≥1-semantic-check; anti-inflation:unchanged|M|P0|
|2|DM-002|Inherited Structural Verdict Block schema (M3 implementation)|Implement DM-002 entity per M1 contract-freeze|SKILL.md|FR-CONV.3|all-3-fields-populated:rf_qa_table_verbatim-byte-exact; prompt_directive-fixed-string-verbatim; reinjection_rule-fixed-string-verbatim|S|P0|
|3|DM-002.rf_qa_table_verbatim|Verbatim table copy field|Byte-exact copy of rf-qa task-integrity Items Reviewed table at spawn time (no editing/summarisation/renaming)|SKILL.md|DM-002|diff-vs-qa-task-integrity.md-Items-Reviewed-table:byte-identical|S|P0|
|4|DM-002.prompt_directive|Fixed-value prompt directive|Fixed-value string: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."|SKILL.md|DM-002|string:emitted-verbatim; treated:frozen-wire-ABI-no-edits-permitted|S|P0|
|5|DM-002.reinjection_rule|Fixed-value reinjection rule|Fixed-value string: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."|SKILL.md|DM-002|rule:documented-in-DM-002; enforced-by-orchestrator:at-every-spawn-INV-002|S|P0|
|6|API-002|rf-qa → rf-qa-qualitative inter-agent API (M3 implementation)|Implement orchestrator-mediated spawn-prompt injection at SKILL.md §A.10.5; extracts Items Reviewed table contiguously; splices verbatim into spawn prompt|SKILL.md|DM-005|grep-Inherited-Structural-Verdict-in-spawn-log:returns-line-N; block-diff-vs-qa-task-integrity.md:byte-identical|S|P0|
|7|Self-Audit output schema|Add `## Self-Audit` section to rf-qa-qualitative output|Output schema addition listing relied-on PASS items AND ≥1 semantic check where PASS is insufficient|rf-qa-qualitative.md|FR-CONV.3|output:contains-Self-Audit-heading; section:lists-rf-qa-PASS-reliance-AND-≥1-documented-semantic-check|S|P0|
|8|INV-002|Freshness rule — cycle-N+1 reinjection|Orchestrator MUST re-read current rf-qa task-integrity report and re-extract table on every fix-cycle spawn|SKILL.md|FR-CONV.3|2-cycle-fixture:cycle-1-vs-cycle-2-spawn-prompts-byte-diff-at-table-region; cycle-2:carries-cycle-2-verdict|S|P0|
|9|INV-010|Dynamic checklist enumeration|Injected verdict table row count enumerates over TB-Add catalogue at runtime (auto-picks up FR-CONV.1 additions)|SKILL.md|FR-CONV.3; TB-Add catalogue|TB-Add-catalogue-growth:checklist-auto-richens; structural-diff:before-after-FR-CONV.1-landing|S|P0|
|10|INV-019|Self-Audit consumer obligation|rf-qa-qualitative output MUST list every rf-qa PASS item it relied on AND ≥1 semantic check where rf-qa PASS is insufficient|rf-qa-qualitative.md|FR-CONV.3|run-with-0-entries-in-category-b:violation; K-003:audits-first-5-runs|S|P0|
|11|Anti-inflation preservation|rf-qa-qualitative.md:766-775 byte-stable|Prohibited Behaviors block (anti-inflation bullet at :770) MUST NOT be weakened/removed/rephrased by FR-CONV.3|rf-qa-qualitative.md|FR-CONV.3|byte-diff-Prohibited-Behaviors-block-pre/post:0; K-003-audit:verifies-operational-compliance|S|P0|
|12|Failure-mode handling|rf-qa task-integrity verdict missing → halt|If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at §A.10 before §A.10.5|SKILL.md|API-002|missing-verdict-fixture:rf-qa-qualitative-does-not-spawn; gate:halts; error:surfaced-to-orchestrator|S|P0|
|13|COMP-001|SKILL.md A.10.5 spawn prompt injection (923-1000)|Inject `## Inherited Structural Verdict` block into SKILL.md A.10.5 spawn prompt at ~:966 (after TARGET FILES, before INSTRUCTIONS)|SKILL.md|FR-CONV.3|grep-Inherited-Structural-Verdict-in-SKILL.md:923-1000:returns-≥1-match; injection-point:verified-at-~966|S|P0|
|14|COMP-004|rf-qa-qualitative.md EOF append (line 794)|Append "Handling the Inherited Structural Verdict" section + add `## Self-Audit` to output schema at rf-qa-qualitative.md:794|rf-qa-qualitative.md|FR-CONV.3|grep-Self-Audit-in-rf-qa-qualitative.md:returns-≥1-match-at-EOF; anti-inflation-block-at-766-775:byte-identical|S|P0|
|15|TEST-007|test_inherited_verdict_present|Fixture asserting `## Inherited Structural Verdict` block in rf-qa-qualitative spawn prompt|tests|FR-CONV.3|grep-matches:block-header-in-spawn-log|S|P0|
|16|TEST-008|test_inherited_verdict_freshness_inv_002|2-cycle fixture asserting cycle-2 spawn carries cycle-2 verdict, not stale cycle-1|tests|INV-002|byte-diff-cycle-1-vs-cycle-2-spawn-prompts:shows-cycle-2-verdict|S|P0|
|17|TEST-009|test_self_audit_inv_019|Fixture asserting rf-qa-qualitative output contains `## Self-Audit` with ≥1 documented semantic check beyond inherited verdict|tests|INV-019|grep-Self-Audit-plus-content-inspection:finds-≥1-semantic-check|S|P0|
|18|TEST-010|test_dynamic_enumeration_inv_010|Fixture asserting checklist auto-richens when FR-CONV.1 catalogue grows|tests|INV-010|structural-diff-of-checklist:before-after-catalogue-growth-shows-enrichment|S|P0|
|19|MIG-003|M1.3 PR-04 landing migration|Strictly-additive passthrough; revertable by disabling passthrough block; rf-qa-qualitative falls back to independent structural re-checking|src/|FR-CONV.3|single-commit; make-verify-sync:PASS; rollback:disable-passthrough-flag-fallback-to-current-behavior|S|P0|
|20|FF_INHERITED_STRUCTURAL_VERDICT|Feature-flag governance (logical)|Enabled at merge; cleanup post-K-003 audit pass (release-spec §8.3 row 4); owner QA Lead; consolidated cleanup tracking in M7|git|FR-CONV.3|logical-flag; K-003-audit-target:governs-cleanup; revert-path:disables-passthrough-block; M7-consolidation:see-M7-governance-table|S|P0|
|21|K-007 mitigation|PR-04/PR-06 sequencing inversion contingency|Sequencing rule PR-06 → PR-04 enforced in release-spec §4.6; INV-010 dynamic-enumeration auto-richens when catalogue activates|SKILL.md|FR-CONV.3|sequencing-rule:enforced-in-release-spec; INV-010-mitigation:auto-richens; inversion-detection:re-merge-in-correct-order|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`## Inherited Structural Verdict` block|spawn-prompt injection|wired-to-SKILL.md-A.10.5|M3|rf-qa-qualitative spawn (FR-CONV.4 axis overlay consumes structural PASS via INV-013)|
|DM-005 Phase Contract|inter-agent contract|wired-to-orchestrator-spawn-step|M3|All future inter-agent contracts (versioning baseline 1.0.0)|
|`## Self-Audit` output section|output-schema addition|wired-to-rf-qa-qualitative.md-EOF|M3|K-003 audit-target (M7); ongoing per-release inspection|

### Milestone Dependencies — M3

- M2 PASS.
- TB-Add catalogue stable (FR-CONV.1 / M1 landed) — INV-010 dynamic enumeration depends on it.
- DM-005 explicit row published in M2.
- `make verify-sync` PASS after M2 commit.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-X-002|PR-04 anti-inflation operational test — "reliance ≠ verification" distinction is empirically observable, not structurally provable. Audit per release-spec.md §8.3 row 4 — first 5 rf-qa-qualitative runs after FR-CONV.3. Source: TDD §22 / OPEN-X-002.|HIGH (K-003 audit-target) — if audit shows inflation, FR-CONV.3 must be rolled back per §19.4|QA Lead|First 5 rf-qa-qualitative runs post-FR-CONV.3 land (audit window in M7)|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M3-1 — PR-04 passthrough causes inflation despite anti-inflation rule (K-003)|Medium|Low|Medium|INV-019 mandatory Self-Audit; X-002 audit-target (first 5 rf-qa-qualitative runs MUST be audited per release-spec §8.3 row 4); disable passthrough flag on audit FAIL|QA Lead|
|2|R-M3-2 — PR-04 + PR-06 sequencing inversion (K-007)|Medium|Low|Medium|Sequencing rule enforced in release-spec §4.6; INV-010 dynamic-enumeration mitigation (auto-richens when catalogue activates); re-merge in correct order on inversion detection|Engineering Lead|

## M4: FR-CONV.4 / PR-07 — Five Adversarial Axes Overlay

**Objective:** Insert `### Five Adversarial Axes` header subsection BEFORE rf-qa-qualitative's 15-item task-qualitative checklist; add `axis` column to Items Reviewed table; preserve zero-trust QA invariant and severity floor at `rf-qa-qualitative.md:786-795`; emit `drift-axis-inactive` annotation when no item restates BUILD_REQUEST.GOAL verbatim. | **Duration:** 2 weeks (2026-06-26 → 2026-07-10) | **Entry:** M3 PASS; Inherited Structural Verdict live (INV-013 composition). | **Exit:** Five Adversarial Axes header renders BEFORE 15-item checklist; Axis column populated with one canonical value per row from `{AX-1..AX-5, none}`; `drift-axis-inactive` annotation emitted in Summary block when GOAL-baseline absent; severity floor block byte-identical; 15-item checklist unchanged.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.4|Insert Five Adversarial Axes overlay|Insert axis-overlay header BEFORE rf-qa-qualitative 15-item checklist; add axis column to Items Reviewed table (CASE-D PR-07); overlay-only, no new conditional code path|rf-qa-qualitative.md; SKILL.md|M3|subsection-renders-before-15-item-checklist; Axis-column:populated-per-row; drift-axis-inactive-annotation:in-Summary-when-no-GOAL-baseline-item|S|P0|
|2|AX-1|Drift axis definition|A cited fact (file path, line number, signature, count, config value) no longer matches current source|rf-qa-qualitative.md|FR-CONV.4|AX-1:enumerated-in-canonical-axes-block-§8.5; finding-example:shows-stale-citation-pattern|S|P0|
|3|AX-2|Contradictions axis definition|Two artifacts (or two sections) assert mutually incompatible facts about same subject|rf-qa-qualitative.md|FR-CONV.4|AX-2:enumerated-in-canonical-axes-block; finding-example:shows-return-type-mismatch-pattern|S|P0|
|4|AX-3|Omissions axis definition|A required touchpoint, consumer, dependency, or step absent from plan|rf-qa-qualitative.md|FR-CONV.4|AX-3:enumerated; finding-example:shows-missing-signature-update-pattern|S|P0|
|5|AX-4|Weakened-criteria axis definition|Acceptance/verification condition softened to unobservable or trivially satisfiable|rf-qa-qualitative.md|FR-CONV.4|AX-4:enumerated; finding-example:shows-trivially-passing-test-pattern|S|P0|
|6|AX-5|Invented-content axis definition|Artifact introduces requirement/feature/capability not present in upstream source|rf-qa-qualitative.md|FR-CONV.4|AX-5:enumerated; finding-example:shows-scope-inflation-pattern|S|P0|
|7|`none` sentinel|none-axis sentinel value|Used when check passed and axis lens surfaced nothing (NOT an N/A escape)|rf-qa-qualitative.md|FR-CONV.4|passing-check:Axis-none; documented:canonical-annotation-rules|S|P0|
|8|`drift-axis-inactive` annotation|drift-axis-inactive Summary-block annotation|Single-line Summary-block annotation when artifact has no citations to drift against|rf-qa-qualitative.md|FR-CONV.4|GOAL-baseline-absent-fixture:emits-drift-axis-inactive; not-encoded-as-Axis-N/A|S|P0|
|9|Axis column on Items Reviewed table|Axis column addition (rf-qa-qualitative.md:675-714)|Insert `axis` column between `Check` and `Result` columns|rf-qa-qualitative.md|FR-CONV.4|every-row-task-qualitative:one-canonical-axis-or-none; column-omitted:for-non-task-qualitative-phases|S|P0|
|10|Five Adversarial Axes header subsection|Header insertion before 15-item checklist (rf-qa-qualitative.md:527)|`### Five Adversarial Axes` subsection inserted BEFORE `#### Checklist (15 items)` header at rf-qa-qualitative.md:527-583|rf-qa-qualitative.md|FR-CONV.4|grep-ordering:Five-Adversarial-Axes-before-Checklist; 15-item-checklist-body:unmodified|S|P0|
|11|15-item checklist preservation|Existing 15-item checklist body unchanged|Body at rf-qa-qualitative.md:527-583 MUST be unmodified; axes multiply lenses, not checks (TOTAL stays at 15 items)|rf-qa-qualitative.md|FR-CONV.4|byte-diff-15-item-checklist-body-pre/post:0; Tool-Engagement-Minimum:unchanged-at-tool-calls-≥15|S|P0|
|12|Severity-floor preservation (786-795)|rf-qa-qualitative severity floor unchanged|Contradictions always IMPORTANT/CRITICAL; severity floor at rf-qa-qualitative.md:786-795 MUST NOT be weakened|rf-qa-qualitative.md|FR-CONV.4|byte-diff-Critical-Rules-block-pre/post:0|S|P0|
|13|COMP-004|rf-qa-qualitative.md axis-column site (675-714)|Modify Items Reviewed table at rf-qa-qualitative.md:675-714 to add `axis` column between `Check` and `Result`|rf-qa-qualitative.md|FR-CONV.4|axis-column-header:present-in-table; parse:one-axis-value-per-row|S|P0|
|14|COMP-001|SKILL.md task-qualitative prompt axis directive (961)|Add axis-annotation directive at SKILL.md:961 in Task-Qualitative prompt|SKILL.md|FR-CONV.4|grep-Axis-in-SKILL.md:~961-returns-≥1-match; directive:instructs-annotation-per-row|S|P0|
|15|TEST-011|test_five_axes_overlay|Fixture asserting axes header appears BEFORE immutable 15-item checklist|tests|FR-CONV.4|grep-ordering-assertion:header-before-checklist|S|P0|
|16|TEST-012|test_axis_column_populated|Fixture asserting Items Reviewed table carries non-empty Axis value on every row|tests|FR-CONV.4|parse-table:assert-no-empty-Axis-cell|S|P0|
|17|TEST-013|test_drift_axis_inactive_when_no_goal_baseline|Fixture asserting `drift-axis-inactive` annotation emitted (not N/A) when no GOAL-baseline item|tests|FR-CONV.4|grep-matches:drift-axis-inactive-annotation-in-Summary-block|S|P0|
|18|TEST-014|test_severity_floor_unweakened|Fixture asserting severity-floor block at rf-qa-qualitative.md:786-795 unchanged|tests|FR-CONV.4|byte-diff-Critical-Rules-block:0|S|P0|
|19|MIG-004|M1.4 PR-07 landing migration|Strictly-additive overlay; revertable by removing axis column + drift-axis-inactive annotation; 15-item checklist untouched|src/|FR-CONV.4|single-commit; make-verify-sync:PASS; rollback:removes-overlay-checklist-intact|S|P0|
|20|FF_FIVE_ADVERSARIAL_AXES|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days post-axis-distribution audit (K-004); owner rf-qa-qualitative maintainer; consolidated cleanup tracking in M7|git|FR-CONV.4|logical-flag; revert-path:removes-overlay; cleanup-gated:K-004-axis-distribution-audit; M7-consolidation:see-M7-governance-table|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Five Adversarial Axes overlay|annotation-overlay|wired-to-rf-qa-qualitative-15-item-checklist|M4|All rf-qa-qualitative task-qualitative runs; INV-013 composition with inherited PASS items|
|Axis column registry (AX-1..AX-5 + none)|enumeration registry|wired-to-Items-Reviewed-table|M4|rf-qa-qualitative output schema; M7 audit reporting|

### Milestone Dependencies — M4

- M3 PASS (FR-CONV.3 Inherited Structural Verdict live; INV-013 composition forms the basis for axes to focus on semantic surface).
- `make verify-sync` PASS after M3 commit.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M4-1 — 5-axis annotation ambiguity over-flags items (K-004)|Low|Low|Low|Annotation-only overlay (no new code path); severity floor preserved; `drift-axis-inactive` annotation for missing GOAL-baseline|rf-qa-qualitative maintainer|

## M5: FR-CONV.5 / PR-02 — Retry Monotonicity + Regression Halts

**Objective:** Add two stop-conditions to EXISTING fix-cycle retry loops (no new loop or stage): monotonicity guard (HALT if `|F_{n+1}|>=|F_n|`) and regression detection (HALT if any item PASS at cycle N is FAIL at cycle N+1); regression precedence over monotonicity; preserve four independent retry counters (no collapsing); preserve existing 3-cycle hard cap at `rf-team-lead.md:417`. | **Duration:** 2 weeks (2026-07-10 → 2026-07-24) | **Entry:** M4 PASS; FR-CONV.6 dedup-key wire-shape spec finalised (mutual coupling — M5 specifies the shape it consumes; M6 lands the emitter). | **Exit:** Regression flip emits verbatim message and exits BEFORE monotonicity check; non-shrink emits `[HALT-MONOTONICITY] |F|=<n>`; identical dedup-key synthetic findings across cycles do NOT trigger halt; legitimate slow-cycle correction NOT halted; X-003 slow-convergence threshold remains REJECTED; all 4 fixtures PASS.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.5|Add monotonicity + regression halt guards|Add two stop-conditions to existing fix-cycle retry loops (CASE-D PR-02); regression > monotonicity precedence; preserve zero-trust QA invariant|SKILL.md; rf-task-builder.md; rf-qa.md|M4|two-halts:wired-to-existing-loops; regression:precedes-monotonicity; slow-shrink:continues; identical-dedup-key-synthetic:does-not-trip-regression-INV-012; 3-cycle-cap:preserved|M|P0|
|2|API-004|Fix-Loop Halt Signals contract (M5 implementation)|Implement halt-message strings as inter-loop wire ABI; ordering rule per cycle transition n→n+1 (regression first, monotonicity second, hard-cap third, proceed fourth)|SKILL.md|FR-CONV.5|all-4-ordering-rules-enforced; halt-strings:byte-exact-fixtures-depend-on-character-for-character-match; F-set-definition:dedup-key-identity|S|P0|
|3|Monotonicity halt message|`[HALT-MONOTONICITY]|F|=<n>` halt-string emitter|Emit verbatim halt string when `|F_{n+1}|>=|F_n|`; only consulted when `|F_n|> 0`|SKILL.md; rf-task-builder.md|API-004|halt-string:emitted-byte-exact-per-spec; emission:gated-on-prior-regression-check-passing; monotonicity-check:skipped-when-F_n-equals-0|S|P0|
|4|Regression halt message|Verbatim regression-detection halt-string emitter|Emit verbatim string `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` when item flips PASS@N→FAIL@N+1|SKILL.md; rf-task-builder.md|API-004|string:emitted-byte-exact; emitted-BEFORE-monotonicity-check; precedence-rule:honored|S|P0|
|5|F-set definition|`F_n` set with dedup-key identity|`F_n` = set of FAIL-verdict items at end of fix cycle n with item identity = dedup-key; cardinality after dedup-key deduplication|SKILL.md|API-004|identity-rule:documented; cardinality:computed-post-dedup; composition-with-synthetic-dnsp-findings-INV-012:wired|S|P0|
|6|Ordering precedence rule|Per-cycle precedence: regression > monotonicity > hard-cap > proceed|Strict ordering check per cycle transition n→n+1: (1) regression check first; (2) monotonicity check second; (3) existing 3-cycle hard cap third; (4) otherwise proceed to n+2|SKILL.md|API-004|each-cycle-transition:checks-4-conditions-in-order; regression:always-exits-BEFORE-monotonicity-check; existing-rf-team-lead.md:417-hard-cap:preserved-as-fallback|S|P0|
|7|INV-012|Cross-cycle synthetic-dnsp dedup composition|Synthetic-dnsp findings count as failures for `|F_n|` cardinality; identical dedup_key across consecutive cycles is dedup case (NOT regression — prior verdict was already FAIL)|SKILL.md|FR-CONV.5; FR-CONV.6|synthetic-same-dedup_key-cycles-N-N+1:contributes-1-not-2-to-F_n+1; persistence:trips-monotonicity-intended-not-regression|S|P0|
|8|3-cycle hard cap preservation|Existing rf-team-lead.md:417 preservation|Existing 3-cycle hard cap MUST NOT be replaced or short-circuited; verified NO DRIFT 2026-05-14|rf-team-lead.md|FR-CONV.5|byte-diff-rf-team-lead.md:417-line-pre/post:0; cap:remains-as-fourth-precedence-backstop|S|P0|
|9|Four-counter preservation|Four independent retry counters MUST NOT be collapsed|Per-gate fix-cycle counters (rf-task-builder.md I16 table) remain independent; FR-CONV.5 layers halts ON TOP without merging|rf-task-builder.md|FR-CONV.5|per-gate-counters-at-rf-task-builder.md:354-360:preserved; no-shared-monotonicity-state-across-counters|S|P0|
|10|X-003 rejection enforcement|No "shrinks too slowly" threshold|Rate-threshold halt design (X-003) REJECTED; `|F|= 5, 4` (shrink by 1) MUST continue|SKILL.md|FR-CONV.5|slow-shrink-fixture:continues-to-next-cycle; no-rate-of-shrink-parameter-introduced|S|P0|
|11|COMP-001|SKILL.md A.9 separate-counters invariant tail (867-873)|Modify SKILL.md A.9 separate-counters invariant tail to add halt-precedence note|SKILL.md|FR-CONV.5|grep-[HALT-MONOTONICITY]-in-SKILL.md:867-873:returns-≥1-match; precedence-rule:documented|S|P0|
|12|COMP-001|SKILL.md Behavioral Constraints hard-invariants (1547-1553)|Add halt-precedence rule to Behavioral Constraints hard-invariants list at SKILL.md:1547-1553|SKILL.md|FR-CONV.5|grep-Regression-detected-on-Item-in-SKILL.md:1547-1553:returns-≥1-match|S|P0|
|13|COMP-002|rf-task-builder.md I16 fix-cycle encoding (334-361)|Modify rf-task-builder.md QA-gate fix-cycle encoding table at :334-361 with halt rules|rf-task-builder.md|FR-CONV.5|halt-rules:documented-at-I16; per-gate-caps:unchanged|S|P0|
|14|COMP-003|rf-qa.md Fix Cycle Protocol Rules (308-315)|Modify rf-qa.md Fix Cycle Protocol Rules at ~:308-315 — promote existing SHOULD bullet to MUST-halt|rf-qa.md|FR-CONV.5|grep-MUST-related-to-halt-at-rf-qa.md:308-315:returns-≥1-match|S|P0|
|15|TEST-015|test_monotonicity_halt_F_5_5_5|3-cycle fixture: `|F|= 5, 5, 5` halts at cycle 2 with `[HALT-MONOTONICITY]|F|=5`; cycle 3 not attempted|tests|FR-CONV.5|grep-halt-message; assert-no-cycle-3-log-entry|S|P0|
|16|TEST-016|test_regression_halt_pass1_fail2|Item 3.2 PASS@1 / FAIL@2 fixture: halts with verbatim regression message BEFORE monotonicity check|tests|FR-CONV.5|grep-verbatim-message; ordering-assertion:confirms-regression-check-runs-first|S|P0|
|17|TEST-017|test_slow_shrink_continues|`|F|= 5, 4` fixture: continues — strict shrink holds; X-003 NOT triggered|tests|FR-CONV.5|execution-log:shows-cycle-continues-to-next-iteration|S|P0|
|18|TEST-022|test_synthetic_dnsp_dedup_not_regression|Synthetic with same dedup_key in cycles 1+2 (other findings shrinking) proceeds to cycle 3 — no regression halt (INV-012)|tests|INV-012|execution-log:shows-cycle-3-attempted; no-regression-halt-emitted-for-cross-cycle-dedup|S|P0|
|19|TEST-024|test_sequencing_PR06_before_PR04|Sequencing test: if PR-04 (FR-CONV.3) lands before PR-06 (FR-CONV.1), dynamic enumeration still richens once catalogue activates|tests|INV-010|structural-assertion-on-enriched-checklist; mitigation-against-K-007:verified|S|P0|
|20|MIG-005|M1.5 PR-02 landing migration|Strictly-additive halts on existing loops; revertable by disabling guards individually; per-gate caps continue to govern on rollback|src/|FR-CONV.5|single-commit; make-verify-sync:PASS; rollback:disable-guards-retain-existing-caps|S|P0|
|21|FF_RETRY_MONOTONICITY_GUARDS|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days post false-halt-rate audit (K-005); owner rf-task-builder maintainer; consolidated cleanup tracking in M7|git|FR-CONV.5|logical-flag; revert-path:disables-both-guards-individually; cleanup-gated:K-005-audit; M7-consolidation:see-M7-governance-table|S|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|API-004 halt-signal contract|inter-loop wire ABI|wired-to-fix-cycle-loop|M5|rf-task-builder fix-loop; downstream observability counters in M7 (HALT-MONOTONICITY counter, regression-halt counter)|
|F-set with dedup-key identity|composition contract|wired-to-FR-CONV.6-emission|M5/M6|FR-CONV.6 synthetic-dnsp emitter (mutual coupling — INV-012 composition)|

### Milestone Dependencies — M5

- M4 PASS.
- FR-CONV.6 dedup-key wire-shape spec finalised (M6 lands the emitter, but M5 specifies what shape it will consume — INV-012 composition).
- Existing 3-cycle hard cap at rf-team-lead.md:417 verified NO DRIFT.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-INV-006|Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track). TB-Add-2 stays `[ADVISORY]` until calibrated. Source: TDD §22 / OPEN-INV-006.|MEDIUM — affects when TB-Add-2 can promote from ADVISORY to Hard; informs rate at which `[HALT-MONOTONICITY]` fires on item-count-driven failures|Engineering|Phase-2 (with PR-05 re-evaluation)|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M5-1 — Retry monotonicity halts legitimate slow-cycle correction (K-005)|Low|Low|Low|Strict-shrink threshold (`|F|= 5, 4` continues); X-003 slow-convergence threshold REJECTED; disable guards individually on rollback|rf-task-builder maintainer|

## M6: FR-CONV.6 / PR-03 — Synthetic DNSP on Partition Exhaust

**Objective:** After a partition agent's escalation ladder exhausts (rf-analyst, rf-qa, or rf-qa-qualitative partition instance), emit synthetic HIGH-severity finding with `source: "synthetic-dnsp"` to agent's output stream rather than silently aborting; preserve all-agents-fail guard (zero partitions succeeded → no synthetic, existing rf-team-lead.md:417 escalation runs); preserve zero-trust QA + evidence-bound-item + parallel-research invariants. | **Duration:** 2 weeks (2026-07-24 → 2026-08-07) | **Entry:** M5 PASS; halt-signal contract live (API-004 consumes synthetic findings via dedup_key composition). | **Exit:** When ≥1 partition succeeded AND ≥1 exhausted, synthetic-dnsp HIGH finding emitted with all 5 fixed fields + dedup_key + found_n_times; identical dedup_keys collapse with `found N times`; zero-partitions-succeeded → NO synthetic emits and existing escalation runs; N-1 partitions complete concurrently (INV-021).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.6|Emit synthetic-dnsp on partition exhaust|After partition agent's escalation ladder exhausts, emit synthetic HIGH-severity finding (CASE-B PR-03 BASE); preserve all-agents-fail guard|SKILL.md; rf-analyst.md; rf-qa.md; rf-qa-qualitative.md|M5|all-5-fixed-fields-plus-2-dedup-control-fields:present; HIGH-severity:non-overridable; all-agents-fail-bypass:preserved; N-1-partitions-concurrent-INV-021|L|P0|
|2|DM-003|Synthetic DNSP Finding schema (M6 implementation)|Implement DM-003 entity per M1 contract-freeze with 7 fields|rf-qa.md|FR-CONV.6|all-7-fields-populated:severity-HIGH-fixed; source-synthetic-dnsp-fixed-sentinel; affected_range-verbatim-assigned-files-slice; evidence-never-blank-spawn-log-or-stub; recommendation-fixed-Manual-review-required; dedup_key-tuple-range-exhaust_point; found_n_times-int-default-1|S|P0|
|3|DM-003.severity|severity field — fixed HIGH non-overridable|HIGH severity literal; guarantees gate-level visibility; cannot be downgraded|rf-qa.md|DM-003|emission-with-severity-not-HIGH:invalid; gate-level-visibility:verified|S|P0|
|4|DM-003.source|source field — fixed `synthetic-dnsp` literal sentinel|Grep-able literal sentinel string for operator inspection|rf-qa.md|DM-003|grep-synthetic-dnsp-in-rf-analyst.md-rf-qa.md:returns-≥1-hit-per-file|S|P0|
|5|DM-003.affected_range|affected_range field — exhausted agent's assigned_files slice|Verbatim copy of partition's file list as received in spawn prompt|rf-qa.md|DM-003|exhausted-partition-fixture:affected_range-matches-spawn-prompt-assigned_files-byte-for-byte|S|P0|
|6|DM-003.evidence|evidence field — spawn-log path or stub citing log absence|Never blank — if log missing, stub explicitly cites absence (`no-spawn-log: <reason>`)|rf-qa.md|DM-003|evidence-field:never-empty; canonical-path-${TASK_DIR}qa/spawn-log-agent_role-partition_id.txt|S|P0|
|7|DM-003.recommendation|recommendation field — fixed string|Fixed value: `Manual review required — partition agent failed twice`|rf-qa.md|DM-003|emission:carries-fixed-recommendation-string-byte-exact|S|P0|
|8|DM-003.dedup_key|dedup_key field — 2-tuple identity|Composite `(assigned_files_range, escalation_ladder_exhaust_point)`; canonical wire format YAML list `["<range>", "<exhaust_point>"]`; exhaust_point from closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`|rf-qa.md|DM-003|dedup_key:emitted-as-YAML-list; exhaust_point:in-closed-vocabulary; deterministic-equality:enabled|S|P0|
|9|DM-003.found_n_times|found_n_times field — collision counter|Default 1; increments by 1 on each within-cycle dedup collapse|rf-qa.md|DM-003|two-identical-dedup_keys-within-cycle:collapse-to-one-record-with-found_n_times-2|S|P0|
|10|API-003|Partition agent → orchestrator API (M6 implementation)|Implement partition emission of structured block in normal output stream (no separate channel); consumed by SKILL.md §A.8 + §A.10 merge step|SKILL.md|DM-003|grep-source-synthetic-dnsp-in-partition-output-stream; orchestrator-merge-step:picks-up-block|S|P0|
|11|escalation_ladder_exhaust_point vocabulary|Closed vocabulary registry|`{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` — free-form descriptions forbidden|rf-qa.md|DM-003.dedup_key|vocabulary:documented; non-vocabulary-values:rejected; dedup-key-equality:deterministic|S|P0|
|12|All-agents-fail guard precedence|Zero-partitions-succeeded → NO synthetic emits|Mutually exclusive paths: ≥1 success AND ≥1 exhaust → emit; zero success → activate rf-team-lead.md:417|SKILL.md; rf-team-lead.md|FR-CONV.6|zero-partitions-fixture:no-synthetic-block-emitted; execution-log:shows-rf-team-lead.md:417-escalation-activates|S|P0|
|13|Within-cycle dedup collapse|Within-cycle identical-dedup_key collapse|Two synthetic findings with identical dedup_key collapse to one record with `found_n_times` incremented|SKILL.md|DM-003|fixture-two-identical-exhaust-events:collapse-to-one-finding-with-found_n_times-2; cardinality-1:verified|S|P0|
|14|Cross-cycle dedup non-regression|Cross-cycle identical-dedup_key NOT regression (INV-012)|Cross-cycle identical dedup_key is dedup case, NOT regression — prior verdict was already FAIL|SKILL.md|FR-CONV.5; FR-CONV.6|cross-cycle-synthetic-same-dedup_key:contributes-1-not-2-to-F_n+1; trips-monotonicity-intended-not-regression|S|P0|
|15|INV-021|Within-agent-instance emission (cohort does not serialize)|On one partition's escalation exhaust, N-1 sibling partitions continue concurrently to completion before exhausted one synthesises finding|rf-qa.md|FR-CONV.6|spawn-log-fixture:N-1-partitions-overlap-exhausted-partition's-synthesis; timestamp-evidence:proves-concurrency|S|P0|
|16|HIGH severity non-overridable|Severity HIGH guarantees gate visibility|Synthetic findings emit ALONGSIDE (not in place of) real findings from successful partitions|SKILL.md|DM-003.severity|emission-cardinality:real-findings-preserved; synthetic:adds-HIGH-visibility-finding-for-exhausted-partition|S|P0|
|17|COMP-001|SKILL.md A.8 Research Quality Gate (572-656)|Modify SKILL.md A.8 to wire synthetic-dnsp merge step|SKILL.md|FR-CONV.6|merge-step:wired-at-A.8; synthetic-block:picked-up-alongside-real-findings|S|P0|
|18|COMP-001|SKILL.md A.10 Task File Validation (870-918)|Modify SKILL.md A.10 to wire synthetic-dnsp merge step at task-integrity phase|SKILL.md|FR-CONV.6|merge-step:wired-at-A.10|S|P0|
|19|COMP-005|rf-analyst partition + DNSP edit site (58-71)|Modify rf-analyst.md:58-71 with DNSP emission logic|rf-analyst.md|FR-CONV.6|grep-synthetic-dnsp-src/superclaude/agents/rf-analyst.md:returns-≥1-hit|S|P0|
|20|COMP-003|rf-qa DNSP edit site (49-77, primary at 70-77)|Modify rf-qa.md:49-77 with DNSP emission logic at :70-77|rf-qa.md|FR-CONV.6|grep-synthetic-dnsp-src/superclaude/agents/rf-qa.md:returns-≥1-hit|S|P0|
|21|COMP-004|rf-qa-qualitative DNSP edit site (70-80)|Modify rf-qa-qualitative.md:70-80 with DNSP emission logic|rf-qa-qualitative.md|FR-CONV.6|grep-synthetic-dnsp-src/superclaude/agents/rf-qa-qualitative.md:returns-≥1-hit|S|P0|
|22|COMP-006|rf-team-lead.md preservation (line 417 NO DRIFT)|rf-team-lead.md line 417 MUST NOT be replaced/short-circuited; verified NO DRIFT 2026-05-14|rf-team-lead.md|FR-CONV.6|byte-diff-rf-team-lead.md:417-pre/post:0; activated-by-all-agents-fail-path|S|P0|
|23|TEST-018|test_dnsp_twice_exhaust|Partition fixture timing out twice emits synthetic-dnsp finding with all 5 fixed fields|tests|DM-003|parse-YAML-or-block; assert-all-5-fields-populated; severity-HIGH; source-synthetic-dnsp|S|P0|
|24|TEST-019|test_dnsp_dedup_collapse|Two identical-dedup_key synthetic findings collapse into one record with found_n_times=2|tests|DM-003.found_n_times|parse-merged-YAML; assert-cardinality-1-plus-found_n_times-2|S|P0|
|25|TEST-020|test_dnsp_all_agents_fail_bypass|Zero partitions succeeded → no synthetic emits; existing rf-team-lead.md:417 escalation activates|tests|FR-CONV.6|execution-log:shows-HALT-path; no-synthetic-block-emitted; rf-team-lead-activation:verified|S|P0|
|26|TEST-021|test_dnsp_does_not_serialize_cohort|On one partition's escalation exhaust, N-1 sibling partitions continue concurrently (INV-021)|tests|INV-021; NFR-CONV.10|spawn-log-timing:N-1-partitions-overlap-exhausted-partition's-synthesis|S|P0|
|27|MIG-006|M1.6 PR-03 landing migration|Strictly-additive emission logic; revertable by removing DNSP edit sites; existing rf-team-lead.md:417 already handles zero-partitions-succeeded|src/|FR-CONV.6|single-commit; make-verify-sync:PASS; rollback:revert-DNSP-sites-all-agents-fail-escalation-remains|S|P0|
|28|FF_SYNTHETIC_DNSP_EMISSION|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days post-emission-count audit (K-006); owner rf-analyst / rf-qa maintainers; consolidated cleanup tracking in M7|git|FR-CONV.6|logical-flag; revert-path:removes-DNSP-sites; cleanup-gated:K-006-audit; M7-consolidation:see-M7-governance-table|S|P0|
|29|NFR-CONV.10|Parallel-research invariant preservation|N partition agents spawn concurrently; on one's exhaust N-1 continue to completion before that one synthesises DNSP|rf-qa.md; rf-qa-qualitative.md|FR-CONV.6|spawn-log-timestamps:prove-concurrency; cohort-never-serialises; INV-021:wired|S|P0|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|DM-003 Synthetic DNSP Finding emission|structured-block emission|wired-to-partition-output-stream|M6|SKILL.md A.8 + A.10 merge step (orchestrator); M7 observability counter (synthetic-dnsp emission count)|
|All-agents-fail bypass guard|escalation-precedence dispatch|wired-to-orchestrator-pre-emission-check|M6|rf-team-lead.md:417 existing escalation path (unmodified)|
|escalation_ladder_exhaust_point vocabulary|closed-vocabulary registry|wired-to-dedup_key-composition|M6|FR-CONV.5 `|F_n|` cardinality composition (M5/M6 mutual coupling)|

### Milestone Dependencies — M6

- M5 PASS (halt-signal contract live; INV-012 composition rule documented).
- rf-team-lead.md:417 verified NO DRIFT (K-008 portfolio-wide).
- NFR-CONV.10 parallel-research invariant probe fixtures available for spawn-log timing assertion.

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M6-1 — Synthetic-dnsp findings mask real issues (K-006)|Low|Low|Low|HIGH severity guarantees gate visibility; dedup_key prevents over-emission; weekly inspection of emission-count metric|rf-qa maintainer|
|2|R-M6-2 — DNSP all-agents-fail branch short-circuits existing escalation|Low|Low|High|Zero-success branch emits no DNSP and uses rf-team-lead.md:417; FR-CONV.6 Negative Criterion enforces mutual-exclusivity|Engineering Lead|

## M7: Production Readiness — K-003 Audit + NFR-CONV.4 Measurement + Consolidated Governance + GA

**Objective:** Audit first 5 rf-qa-qualitative runs post-FR-CONV.3 (K-003 / X-002 audit-target); measure token-cost on 5 representative BUILD_REQUESTs against NFR-CONV.4 ≤1.10 ratio; consolidate FLAG-*/MET-*/OPS-* into a single GA-readiness governance table; instrument observability counters (synthetic-dnsp, HALT-MONOTONICITY, regression-halt, Self-Audit coverage, make verify-sync PASS rate); ship runbook for OPS-001..007 scenarios; remove fallback paths at GA + 30 days; commit v3.9 GA. | **Duration:** 2 weeks (2026-08-07 → 2026-08-21) | **Entry:** M6 PASS; all 6 FR-CONV.X merged; `make verify-sync` PASS. | **Exit:** K-003 audit PASS on first 5 rf-qa-qualitative runs (100% Self-Audit coverage with ≥1 independent semantic check each); NFR-CONV.4 ratio ≤1.10 across all 5 representative BUILD_REQUESTs; consolidated FLAG/MET/OPS governance table published; observability counters live; v3.9 GA tagged.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-007|Post-merge audit + NFR-CONV.4 measurement orchestration|Coordinate K-003 first-5-runs audit + NFR-CONV.4 token-cost measurement on 5 representative BUILD_REQUESTs|process|All FRs landed|audit-report:published; token-cost-ratio:computed; GA-tag:created-on-PASS|M|P0|
|2|NFR-CONV.4|Token-cost ratio empirical measurement (≤1.10)|Measure token-cost ratio post-merge / pre-merge per equivalent BUILD_REQUEST; ceiling 1.10|process|All FRs landed|5-BUILD_REQUESTs-covering-Quick-Standard-Deep-tiers; pre-merge-baseline-plus-post-merge-counts; ratio:≤1.10|S|P0|
|3|NFR-CONV.5|No-new-dependencies post-merge audit|Audit all 6 FR diffs to confirm only Read/Grep/Glob/Bash used; no new MCP servers; no synchronous network calls|process|All FRs landed|diff-inspection-across-6-FRs:returns-zero-new-external-dep-introductions|S|P0|
|4|NFR-CONV.6|self-contained-item invariant fixture PASS|Synthetic fixture with all 5 fields populated PASSES all 8 TB-Add checks; same fixture with one field stripped FAILS TB-Add-1|tests|FR-CONV.1; Q-DM-1|composite-fixture-per-NFR-CONV.6; binding:to-whichever-schema-resolves-Q-DM-1|S|P0|
|5|NFR-CONV.8|Persistent .dev/tasks/ artifact invariant verification|Diff `.dev/tasks/<task-id>/` directory layout pre-merge vs post-merge — zero structural changes (no new mandatory subdirectory, no rename of research/qa/synthesis/reviews/adversarial, no naming-pattern change)|process|All FRs landed|diff-output:empty; INV-018-preservation:verified|S|P0|
|6|NFR-CONV.9|Zero-trust QA invariant verification|Two-part fixture: (a) 1-LOW-finding fixture → gate FAILS; (b) FR-CONV.3 inherited-verdict applied → no item marked VERIFIED unless Self-Audit lists independent semantic-check engagement|tests|FR-CONV.1; FR-CONV.3|both-fixture-parts:PASS-per-spec; verbatim-PASS/FAIL-definitions-at-rf-qa.md:141-142:byte-identical|S|P0|
|7|NFR-CONV.2|Research-driven prose determinism exclusion documentation|Document NFR-CONV.2 scope split: structural fields byte-deterministic; research-prose nondeterminism acceptable; structural annotations within prose (axis labels, finding counts, dedup-keys) remain byte-equal|docs/|All FRs landed|documentation-page; structural-vs-prose-boundary:enumerated; M7-audit:verifies-structural-annotations-byte-equal-across-2-runs|S|P0|
|8|NFR-CONV-R1|Single-pass gate PASS rate baseline measurement|Run 5 representative BUILD_REQUESTs; count first-cycle PASS verdicts; target ≥80%|process|All FRs landed|≥4-of-5-BUILD_REQUESTs:PASS-task-integrity-gate-on-first-cycle-≥80%|S|P0|
|9|NFR-CONV.3|Hidden-input determinism guard verification|Fixture-populated `.dev/tasks/done/` vs empty: byte-identical structural output|tests|All FRs landed|byte-diff-structural-fields:0; PR-05-advisory-mechanism:remains-REJECTED-for-Phase-1|S|P0|
|10|TEST-023|test_hidden_input_guard fixture|Fixture-populated `.dev/tasks/done/` yields byte-identical structural output vs empty-done baseline|tests|NFR-CONV.3|byte-diff-structural-fields:0|S|P0|
|11|TEST-025|test_invariant_preservation_NFR_6_through_10 composite|All 5 invariants (self-contained-item, evidence-bound-item, persistent-artifact, zero-trust QA, parallel-research) preserved per Negative Criteria|tests|All FRs landed|composite-fixture:exercises-each-invariant-surface; all-5-invariants:PASS|S|P0|
|12|Consolidated FLAG-*/MET-*/OPS-* governance table|GA-readiness governance table — single-page audit artifact|Single consolidated governance table aggregating all 6 logical FF_* flags, 6 MET-* metrics with thresholds, and 7 OPS-* runbooks for the GA-tagging decision|docs/|All FRs landed|single-page-governance-table:published; all-6-FF_*-flags-enumerated-with-cleanup-windows; all-6-MET-*-metrics-with-thresholds; all-7-OPS-*-runbooks-cited|S|P0|
|13|OPS-001|K-003 audit-target runbook (first 5 rf-qa-qualitative runs)|Runbook: symptoms / diagnosis / resolution / escalation / prevention for Self-Audit missing or zero-independent-checks|docs/|FR-CONV.3|runbook:published; Self-Audit-coverage-gauge:target-100%-first-5-runs-documented; QA-Lead-4-business-hour-response-SLA|S|P0|
|14|OPS-002|DNSP triage runbook (synthetic-dnsp emission count >0)|Runbook: read affected partition's spawn-log; identify root cause of escalation-ladder exhaust; check dedup_key for prior similar events; escalate ≥3 distinct dedup-keys in a week|docs/|FR-CONV.6|runbook:published; 24-hour-response-SLA; weekly-inspection-cadence|S|P0|
|15|OPS-003|All-partitions-exhaust HALT runbook (no DNSP)|Runbook: confirm zero partition successes; verify line-417 escalation fired and NO synthetic-dnsp emitted (correct per FR-CONV.6 mutual-exclusivity)|docs/|FR-CONV.6|runbook:published; mutual-exclusivity-check:documented; resolution:user-resolves-unresolved-findings|S|P0|
|16|OPS-004|`[HALT-MONOTONICITY]` rate >50% runbook|Runbook: sample 3 halt events; inspect BUILD_REQUESTs for upstream defects; inspect MDTM for structural issues; resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)|docs/|FR-CONV.5|runbook:published; threshold-greater-than-50%-documented; upstream-quality-gate-referral-path|S|P0|
|17|OPS-005|Regression-halt rate >20% runbook|Runbook: sample 3 regression events; inspect what changed between cycles; resolution = tighten fix-cycle prompts (X-003 slow-convergence threshold REJECTED)|docs/|FR-CONV.5|runbook:published; threshold-greater-than-20%-documented; Engineering-Lead-escalation|S|P0|
|18|OPS-006|`make verify-sync` FAIL post-FR-merge runbook|Runbook: re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline (A-001); revert direct `.claude/` edit on persistent failure (K-009 contingency)|docs/|All FRs landed|runbook:published; pre-commit-hook-enforcement-documented; immediate-response-SLA|S|P0|
|19|OPS-007|INV-018 layout-change runbook (K-008)|Runbook: inspect all 6 FRs for path/naming references; re-integration commit covering all 6 FRs per §19.4 dependency matrix|docs/|All FRs landed|runbook:published; portfolio-wide-blast-radius-response-documented; SP-33-stability-commitment-cited|S|P0|
|20|MET-001|Single-Pass Gate PASS Rate measurement|Measure representative first-cycle task-integrity PASS rate (NFR-CONV-R1)|observability|NFR-CONV-R1|sample:5-BUILD_REQUESTs; metric:first-cycle-PASS-fraction; target:≥80%; validation:gate-reports|S|P0|
|21|MET-002|Detection Rate measurement|Measure unresolved-token and DAG-cycle detection on synthetic fixtures|observability|TEST-001,TEST-002|unresolved-token-detection:100%; DAG-cycle-detection:100%; method:synthetic-fixtures; validation:TB-Add-1/4-errors|S|P0|
|22|MET-003|Self-Audit Coverage measurement|Measure Self-Audit presence and semantic-check coverage after FR-CONV.3|observability|OPS-001|window:first-5-runs; target:100%; semantic-checks:≥1-each; failure:block-release|S|P0|
|23|MET-004|Halt Rate measurement (Synthetic-dnsp + HALT-MONOTONICITY + regression-halt)|Measure synthetic-dnsp emission count; HALT-MONOTONICITY rate; regression-halt rate across fix-cycle batches|observability|OPS-002,OPS-004,OPS-005|synthetic-dnsp:>0-triggers-OPS-002; monotonicity-alert:>50%-triggers-OPS-004; regression-alert:>20%-triggers-OPS-005; offline-grep-aggregate-per-release|S|P0|
|24|MET-005|DNSP Emission measurement|Measure DNSP emission on healthy and twice-exhaust fixtures|observability|FR-CONV.6|twice-exhaust:≥1; healthy-run:0; production-threshold:>0-triggers-review; fields:all-present|S|P0|
|25|MET-006|Token-Cost measurement (NFR-CONV.4)|Measure post/pre token cost ratio for equivalent BUILD_REQUESTs|observability|NFR-CONV.4|sample:5-BUILD_REQUESTs; tiers:Quick/Standard/Deep; target:≤1.10; contingency:summarise-inherited-verdict-table-if-exceeded|S|P0|

### Consolidated GA-Readiness Governance Table — M7

Single-page audit artifact aggregating all logical flags, metrics, and runbooks for the GA-tagging decision (Haiku improvement I3 — centralized governance for GA review).

|Flag / Metric / Runbook|Type|Default|Owner|Cleanup / Action Window|Source FR|
|---|---|---|---|---|---|
|FF_TB_ADD_1_THROUGH_8|Logical flag|Enabled at merge|rf-qa maintainer|GA+30d; TB-Add-2 stays ADVISORY until Phase-2 (OPEN-INV-006)|FR-CONV.1|
|FF_EXECUTION_CONTEXT_HEADER|Logical flag|Enabled at merge|task-builder maintainer|GA+30d; fallback References-only natural rollback|FR-CONV.2|
|FF_INHERITED_STRUCTURAL_VERDICT|Logical flag|Enabled at merge|QA Lead|Post-K-003 audit pass (release-spec §8.3 row 4); rollback disables passthrough|FR-CONV.3|
|FF_FIVE_ADVERSARIAL_AXES|Logical flag|Enabled at merge|rf-qa-qualitative maintainer|GA+30d post-axis-distribution audit (K-004); rollback removes overlay|FR-CONV.4|
|FF_RETRY_MONOTONICITY_GUARDS|Logical flag|Enabled at merge|rf-task-builder maintainer|GA+30d post false-halt-rate audit (K-005); rollback disables guards individually|FR-CONV.5|
|FF_SYNTHETIC_DNSP_EMISSION|Logical flag|Enabled at merge|rf-analyst / rf-qa maintainers|GA+30d post-emission-count audit (K-006); rollback removes DNSP sites|FR-CONV.6|
|MET-001|Single-Pass PASS Rate|N/A|Engineering|Target ≥80% on 5 BUILD_REQUESTs (NFR-CONV-R1)|All FRs|
|MET-002|Detection Rate|N/A|Engineering|100% TB-Add-1/4 on synthetic fixtures|FR-CONV.1|
|MET-003|Self-Audit Coverage|N/A|QA Lead|100% on first 5 runs; block release on failure|FR-CONV.3|
|MET-004|Halt Rate (combined)|N/A|rf-task-builder maintainer|HALT-MONOTONICITY>50% → OPS-004; regression>20% → OPS-005|FR-CONV.5|
|MET-005|DNSP Emission|N/A|rf-qa maintainer|>0 in production → OPS-002 review|FR-CONV.6|
|MET-006|Token-Cost Ratio|N/A|Engineering Lead|≤1.10 target; contingency K-010 summarise inherited verdict|All FRs|
|OPS-001|K-003 audit runbook|Operational|QA Lead|4 business hours response SLA|FR-CONV.3|
|OPS-002|DNSP triage runbook|Operational|rf-qa maintainer|24 hours response SLA; escalate ≥3 distinct/week|FR-CONV.6|
|OPS-003|All-partitions-exhaust runbook|Operational|rf-team-lead maintainer|Activates on zero-success path|FR-CONV.6|
|OPS-004|Monotonicity rate runbook|Operational|rf-task-builder maintainer|Threshold >50% of batches|FR-CONV.5|
|OPS-005|Regression rate runbook|Operational|Engineering Lead|Threshold >20% of batches|FR-CONV.5|
|OPS-006|Sync failure runbook|Operational|Per-commit author|Immediate response SLA (A-001 / K-009)|All FRs|
|OPS-007|Layout change runbook|Operational|Engineering Lead|Portfolio-wide blast-radius (K-008)|All FRs|

### Integration Points — M7

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Observability counters (synthetic-dnsp, HALT-MONOTONICITY, regression-halt, Self-Audit coverage, make verify-sync PASS rate)|metric emitter + alert rule registry|wired-to-offline-grep-pipeline|M7|Per-release audit + ongoing release-spec §8.3 audit-row inspection|
|OPS-001..007 runbooks|operational documentation|wired-to-on-call-knowledge-base|M7|task-builder maintainers (on-call rotation)|
|Feature-flag cleanup (6 logical flags)|governance lifecycle|wired-to-GA+30days-cleanup|M7|Post-GA fallback-path removal|
|Consolidated GA-Readiness Governance Table|single-page audit artifact|published-at-M7|M7|GA-tagging decision committee|

### Milestone Dependencies — M7

- All 6 FR-CONV.X landed (M1..M6 PASS).
- `make verify-sync` PASS after every prior commit.
- First 5 real rf-qa-qualitative runs available for K-003 audit.

### Open Questions — M7

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-TOKEN|NFR-CONV.4 token-ceiling empirical measurement: actual post-merge token-cost ratio against 1.10 ceiling on 5 representative BUILD_REQUESTs. Source: TDD §22 / OPEN-TOKEN.|MEDIUM — if ceiling exceeded, summarise FR-CONV.3 verdict table rather than emit verbatim (K-010 contingency)|Engineering Lead|Post-merge measurement (M7 audit window)|
|2|OPEN-PR05|When does `.dev/tasks/done/` reach ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05 (Tier-History Advisory)? Status: tracked, Phase-2 deferral; re-check each major release. Source: TDD §22 / OPEN-PR05.|LOW — PR-05 deferred to Phase-2 (NFR-CONV.3 hidden-input determinism enforces non-introduction in v3.9)|Engineering Lead|Re-check each major release|
|3|OPEN-INV-017|Historical-file staleness check for PR-05 advisory citations. Status: deferred until PR-05 returns. Source: TDD §22 / OPEN-INV-017.|LOW — no v3.9 deliverable impact; gated on PR-05 re-evaluation|Engineering|When PR-05 re-evaluated|

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-M7-1 — Audit FAIL on first 5 rf-qa-qualitative runs (K-003)|Medium|Low|Medium|If audit shows inflation → roll back FR-CONV.3 per §19.4; INV-019 Self-Audit mandate enforces structural visibility|QA Lead|
|2|R-M7-2 — Token ceiling NFR-CONV.4 exceeded by >10% (K-010)|Low|Low|Low|Empirical measurement on 5 BUILD_REQUESTs; contingency = summarise FR-CONV.3 verdict table rather than emit verbatim|Engineering Lead|
|3|R-M7-3 — Operational thresholds measured but not acted on|Medium|Low|Medium|Bind each threshold to OPS runbooks and release checklist gates via the Consolidated GA-Readiness Governance Table|task-builder maintainer|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|None — NFR-CONV.5 explicitly forbids new external dependencies, MCP servers, libraries, and synchronous network calls|All milestones|N/A|N/A — diff inspection rejects any new external dep|

### Internal Dependencies

- `release-spec.md` v1.0.0 — landing order (§4.6), SP-10 rollback matrix (§9), audit rows (§8.3): governance baseline for M1..M7.
- `conflict-register.md` (5 CASE-D rows): per-CASE-D conflicting mechanism + protected invariant for FR-CONV.1/.2/.4/.5; CASE-B for FR-CONV.3/.6 (no register row).
- `invariant-probe.md` (INV-002, INV-010, INV-012, INV-015, INV-019, INV-021): routed to FR Negative Criteria across M1..M6.
- `FINAL-REPORT.md` §6.2 F2 (21-retry / 18-batch oscillation evidence) + §6.3 (5 ADOPT-grade qualities inverse direction): empirical motivation for FR-CONV.5 + portfolio adoption rationale.
- `rf-team-lead.md:417` (3-fix-cycle escalation): NO-DRIFT preservation across M1..M7.
- `rf-qa.md:141-142` (zero-trust PASS/FAIL): preservation across M1..M6 (NFR-CONV.9).
- `task-builder/SKILL.md:~1452-1457` per-item schema: SC-1 drift flagged — Q-DM-1 critical blocker for M1.
- `.dev/tasks/` directory layout (INV-018): SP-33 stability commitment; K-008 portfolio-wide guard.
- `make sync-dev` / `make verify-sync` pipeline (A-001): per-FR landing gate across M1..M7.
- PRD v1.0 — Epics 1-3 (FR-CONV.1..6) source.

### Infrastructure Requirements

- N/A — no database, no message queue, no compute allocation, no deployment target. This release modifies markdown definition files (`src/superclaude/skills/task-builder/SKILL.md` + 4 rf-* agents) that propagate to `.claude/` via existing `make sync-dev` tooling. No infrastructure scaling required (NFR-CONV.5).
- Existing repository tooling required: `make sync-dev`, `make verify-sync`, `uv run pytest`.
- Persistent artifacts remain under `.dev/tasks/to-do/TASK-*/` with existing `research/`, `qa/`, `synthesis/`, `reviews/`, `adversarial/` subdirectory names unchanged (NFR-CONV.8 / INV-018).

## Risk Register

Global aggregation of all per-milestone risks. Each R-### row consolidates the risks listed in the per-milestone `### Risk Assessment and Mitigation — M{N}` subsections; `Affected Milestones` is the comma-separated list of M{N} IDs.

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-001|K-001 — TB-Add false positives waste fix-cycles|M1|Low|Low|Each TB-Add cites source-check-ID; TB-Add-2 ships as `[ADVISORY]`; individually revertable line|rf-qa maintainer|
|R-002|Q-DM-1 schema ambiguity leads to implementing TB-Add-6/8 against wrong baseline|M1, M2|Medium|High|Resolve Q-DM-1 before any TB-Add work; record selected schema in DM-004; pre-M1 entry gate|Engineering Lead|
|R-003|K-008 — INV-018 `.dev/tasks/` layout change invalidates all FR paths|M1, M2, M3, M4, M5, M6, M7|Low|High|Portfolio-wide note; SP-33 stability commitment; re-integration commit contingency covering all 6 FRs|Engineering Lead|
|R-004|K-009 — Sync-discipline (A-001) violated by direct `.claude/` edit|M1, M2, M3, M4, M5, M6, M7|Low|Medium|All FR-CONV.X paths reference `src/superclaude/` exclusively; CLAUDE.md mandates workflow; revert direct edit and re-run from `src/superclaude/` on failure|Per-commit author|
|R-005|K-002 — Execution Context header drift (header says X, items say Y)|M2|Low|Low|TB-Add-7 cross-validates header source-areas reappear in items; gate fails on drift; header degrades to References-only fallback|task-builder maintainer|
|R-006|Per-item evidence migrates from items into the header|M2|Low|Medium|FR-CONV.2 Negative Criterion keeps file:line citations in item Context only; TB-Add-8 enforcement on per-item Context|Engineering|
|R-007|K-003 — PR-04 passthrough causes inflation despite anti-inflation rule|M3, M7|Medium|Medium|INV-019 mandatory Self-Audit; X-002 audit-target — first 5 rf-qa-qualitative runs MUST be audited; contingency disable passthrough flag|QA Lead|
|R-008|K-007 — PR-04 + PR-06 sequencing inversion|M3|Medium|Medium|Sequencing rule enforced in release-spec §4.6; INV-010 dynamic-enumeration mitigation; re-merge in correct order on inversion|Engineering Lead|
|R-009|K-004 — 5-axis annotation ambiguity over-flags items|M4|Low|Low|Annotation-only overlay; severity floor preserved; `drift-axis-inactive` annotation when no GOAL-baseline; audit axis distribution post-GA|rf-qa-qualitative maintainer|
|R-010|K-005 — Retry monotonicity halts legitimate slow-cycle correction|M5|Low|Low|Strict-shrink threshold; X-003 slow-convergence threshold REJECTED; disable guards individually on rollback|rf-task-builder maintainer|
|R-011|K-006 — Synthetic-dnsp findings mask real issues|M6|Low|Low|HIGH severity guarantees gate visibility; dedup_key prevents over-emission; weekly emission-count inspection|rf-qa maintainer|
|R-012|DNSP all-agents-fail branch short-circuits existing escalation|M6|Low|High|Zero-success branch emits no DNSP and uses rf-team-lead.md:417; FR-CONV.6 Negative Criterion enforces mutual-exclusivity|Engineering Lead|
|R-013|K-010 — Token ceiling NFR-CONV.4 exceeded by >10%|M7|Low|Low|Empirical post-merge measurement on 5 BUILD_REQUESTs; contingency summarise FR-CONV.3 verdict table rather than emit verbatim|Engineering Lead|
|R-014|Operational thresholds measured but not acted on|M7|Medium|Medium|Bind each threshold to OPS runbooks and release-checklist gates via Consolidated GA-Readiness Governance Table|task-builder maintainer|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Single-pass gate PASS rate|Fraction of BUILD_REQUESTs passing task-integrity gate on first cycle|≥80% (currently baseline) ↑ post-merge|Run 5 representative BUILD_REQUESTs; count first-cycle PASS|M7|
|Placeholder-defect detection rate|TB-Add-1 fires on placeholder/title-only fixture items|100% on synthetic fixtures|TEST-001 synthetic-fixture assertion|M1|
|DAG-cycle detection rate|TB-Add-4 fires on circular-dependency fixtures|100% on synthetic fixtures|TEST-002 synthetic-fixture assertion|M1|
|Self-Audit coverage post-FR-CONV.3|Every rf-qa-qualitative run carries `## Self-Audit` entry with ≥1 independent semantic check|100% on first 5 runs (K-003 audit-target)|grep `## Self-Audit` + content inspection across first 5 runs (OPS-001 runbook)|M7|
|`[HALT-MONOTONICITY]` emission rate|Counter of halt emissions per fix-cycle batches|<10% target; >50% triggers upstream BUILD_REQUEST defect alert (OPS-004)|grep `[HALT-MONOTONICITY]` in fix-loop logs; offline aggregate per release|M7|
|Synthetic-dnsp emission count|Counter of synthetic-dnsp findings emitted|≥1 on twice-exhaust fixture; 0 on healthy runs|grep `"source: synthetic-dnsp"` across QA reports|M7|
|Generation-cost efficiency|Token-cost ratio post-merge / pre-merge|≤1.10 per equivalent BUILD_REQUEST (NFR-CONV.4)|5 representative BUILD_REQUESTs; pre/post token counts; compute ratio|M7|
|Gate convergence health|Fix-cycle convergence rate to gate PASS|≥75% baseline ↑ post-merge|Fraction of fix-cycle sequences converging to PASS rather than hitting cap or monotonicity halt|M7|
|Structural determinism|Structural field diff|Byte-identical across two identical runs|NFR-CONV.1 deterministic diff|M7|
|Hidden-input determinism|Structural output with populated `done/`|Byte-identical to empty `done/` baseline|TEST-023|M7|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Port direction|Intent-port (adapt intent, re-express in task-builder idiom) — 5 mechanisms ported|(1) Bulk-implementation-port all 17 sc-tasklist Stage-6 checks — REJECTED per CB-3 (only 8 of 17 are intent-portable; 11 are bundle-specific to phase-file naming, checkpoint emission, T-ID format); (2) Do nothing — REJECTED (persistent silent-acceptance defects, unbounded oscillation cost per FINAL-REPORT §6.2 F2)|FINAL-REPORT §6.3 asymmetric finding establishes the 5 mechanisms as worth adopting; per-check classification (CB-3) shows only 8 of 17 are intent-portable; bulk-port would force X-001 blanket "no specific file paths" rule onto per-item Context fields, gutting evidence-bound-item invariant|
|Governance model|Strictly-additive A-002 (no existing item renamed/renumbered/removed) with per-FR rollback granularity|Single-FR mega-merge — REJECTED (eliminates per-FR rollback granularity; co-revert matrix per §19 requires FRs expressible independently)|Per-FR rollback granularity is stated release goal; composition lives in algorithm not single monolithic structure; release-spec.md §9 SP-10 documents co-revert matrix|
|Milestone structure|7 per-FR milestones (M1..M7) aligned with FR boundaries; M1 augmented with COMP-001..006 architectural-surface map and contract-freeze rows|5-milestone layered (Foundation/Core/Integration/Hardening/Readiness) — partial — Haiku presentation|Per-FR isomorphism makes rollback first-class roadmap citizen; mutual-coupling (FR-CONV.5↔.6, FR-CONV.3↔.1) surfaces explicitly in dependency graph; M1 surface map and contract-freeze adopted from Haiku for change-detection at milestone boundary|
|Contract timing|Contract-freeze rows in M1 (COMP-001..006, DM-001..005 schemas, API-001..004 schemas, NFR-CONV.5 boundary) plus field-level implementation in consuming FR milestone|Pure just-in-time per-FR placement vs pure front-loaded M1 enumeration|Hybrid: M1 freeze catches drift at milestone-boundary while FR-milestone implementation rows track verification work; combines Opus field-level traceability with Haiku contract-freeze ceremony|
|Determinism scope|Structural fields byte-deterministic (NFR-CONV.1); research-prose nondeterminism acceptable (NFR-CONV.2)|(1) Full byte-determinism — REJECTED (impossible with LLM-driven builder); (2) Zero determinism — REJECTED (gate verdicts must be reliable enough to drive PASS/FAIL)|LLM determinism achievable on structured output but not on free prose; structural annotations within prose (axis labels, finding counts, dedup-keys) remain byte-equal to keep gate verdicts reliable|
|Anti-inflation handling|Absolute preservation of `rf-qa-qualitative.md:766-775`; FR-CONV.3 inherited verdict is deliberately-scoped RELIANCE channel for structural items only|(1) Strict mechanical re-check — REJECTED (wastes fix cycles); (2) Pure passthrough — REJECTED (rubber-stamp risk)|INV-019 Self-Audit mandate makes the rule auditable; K-003 designates first 5 runs as audit-target; failure path = disable passthrough flag (§19.4 rollback)|
|All-agents-fail guard precedence|FR-CONV.6 mutually exclusive: ≥1 success AND ≥1 exhaust → emit synthetic-dnsp; zero success → activate rf-team-lead.md:417 (NO synthetic)|(1) DNSP always emits on any exhaust — REJECTED (would mask total-failure condition); (2) No DNSP at all — REJECTED (leaves partial-failure case silent)|Preserves established 3-fix-cycle escalation; DNSP adds coverage for partial-failure case without short-circuiting "stop the line" HALT; rf-team-lead.md:417 verified NO DRIFT|
|FR-CONV.5 stop-condition design|Strict shrink + regression precedence (regression > monotonicity > hard-cap > proceed); F-set has dedup-key identity|(1) X-003 "shrinks too slowly" rate threshold — REJECTED (introduces tunable K with no principled value; legitimate slow-cycle is normal); (2) Pure cardinality, no regression — REJECTED (misses PASS@N→FAIL@N+1 swaps where cardinality stays constant)|Composition matters — F is set with identity, not just count; INV-012 dedup-key composition with FR-CONV.6 requires set-identity semantics; web-02 §4 prior art (ddmin failure-preservation invariant) supports regression precedence|
|GA governance presentation|Consolidated FLAG-*/MET-*/OPS-* governance table in M7 (single-page audit artifact) plus per-FR placement in originating milestone|Per-FR-only placement (Opus) vs consolidated-only (Haiku)|GA-tagging decision benefits from single-page enumeration; per-FR rollback envelope benefits from FR-local placement; both audiences served by dual presentation|

## Timeline Estimates

Dual scheduling presentation: calendar dates (stakeholder commitments) AND week-relative anchoring (honors Q-DM-1 resolution uncertainty per Haiku improvement I4). Week-1 is anchored to the date Q-DM-1 resolves AND design approval lands; absolute dates assume that happens on 2026-05-15.

|Milestone|Duration|Calendar Start|Calendar End|Week-Relative|Key Milestones|
|---|---|---|---|---|---|
|M1 (FR-CONV.1 / PR-06)|2 weeks|2026-05-15|2026-05-29|Weeks 1-2|Q-DM-1 resolved; COMP-001..006 surface map ratified; DM-001..005 + API-001..004 contract-freeze; TB-Add-1..8 land across 3 surfaces; TEST-001..003 PASS; `make verify-sync` PASS|
|M2 (FR-CONV.2 / PR-01)|2 weeks|2026-05-29|2026-06-12|Weeks 3-4|Execution Context header live; DM-001 fields wired; DM-005 published as explicit row; TEST-004..006 PASS|
|M3 (FR-CONV.3 / PR-04)|2 weeks|2026-06-12|2026-06-26|Weeks 5-6|Inherited Structural Verdict + Self-Audit live; DM-002/DM-005 wired; TEST-007..010 PASS; anti-inflation byte-stable|
|M4 (FR-CONV.4 / PR-07)|2 weeks|2026-06-26|2026-07-10|Weeks 7-8|Five Adversarial Axes overlay live; AX-1..5 + none + drift-axis-inactive; TEST-011..014 PASS; severity floor byte-stable|
|M5 (FR-CONV.5 / PR-02)|2 weeks|2026-07-10|2026-07-24|Weeks 9-10|Monotonicity + regression halts live; API-004 halt-signal contract wired; TEST-015..017, 022, 024 PASS|
|M6 (FR-CONV.6 / PR-03)|2 weeks|2026-07-24|2026-08-07|Weeks 11-12|Synthetic DNSP live; DM-003 5-field emission + dedup_key composition; TEST-018..021 PASS; rf-team-lead.md:417 byte-stable|
|M7 (Audit + Measurement + Consolidated Governance + GA)|2 weeks|2026-08-07|2026-08-21|Weeks 13-14|K-003 audit PASS on first 5 rf-qa-qualitative runs; NFR-CONV.4 ratio ≤1.10 on 5 BUILD_REQUESTs; Consolidated GA-Readiness Governance Table published; OPS-001..007 runbooks published; v3.9 GA tag|

**Total estimated duration:** 14 weeks (2026-05-15 → 2026-08-21 calendar / Weeks 1-14 relative), landing within the TDD §23.1 v3.9 GA = 2026-Q3 commitment with ~6 weeks of buffer before Q3 close (2026-09-30). Week-relative anchoring activates if Q-DM-1 resolution slips beyond 2026-05-15; absolute commitment dates shift by the same delta.
