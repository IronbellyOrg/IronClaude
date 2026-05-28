---
spec_source: "TDD_TASK_BUILDER_CONVERGENCE.compressed.md"
complexity_score: 0.7
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# Task-Builder Convergence v3.9 — Project Roadmap

## Executive Summary

Task-Builder Convergence v3.9 is a strictly-additive refactoring release that imports five generation-time rigor mechanisms from `/sc:tasklist` plus one execution-resilience mechanism (DNSP synthetic finding) into the `task-builder` skill. Six functional requirements (FR-CONV.1..6) land in strict serial order PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03, with per-FR rollback granularity governed by the G6 four-case conflict rule and bounded by an ≤10% token-cost ceiling (NFR-CONV.4).

**Business Impact:** Closes three structural-rigor gaps (no task-level executor summary, no structural gate checks for placeholder/DAG/granularity, implicit inherited verdict between rf-qa and rf-qa-qualitative) and eliminates a documented 21-retry / 18-batch oscillation pattern (FINAL-REPORT §6.2 F2). Compounds across every downstream MDTM-driven workflow by reducing rework cost at sprint-execution time.

**Complexity:** HIGH (0.7) — 6 strictly-additive FRs across 5 source files (~3,800 lines total), cross-FR dependency chain with mutual reference (FR-CONV.5 ↔ FR-CONV.6), five load-bearing invariants requiring synthetic-fixture proof (NFR-CONV.6..10), G6 four-case conflict classification per FR, one CRITICAL open contradiction (SC-1 / Q-DM-1) blocking FR-CONV.1 implementation, and a three-paradigm rigor mechanism (structural gate + inter-agent verdict channel + retry/exhaust resilience).

**Critical path:** Q-DM-1 schema contradiction resolution (Engineering Lead decision) → FR-CONV.1 TB-Add-1..8 catalogue (PR-06) → FR-CONV.2 Execution Context header (PR-01) → FR-CONV.3 Inherited Structural Verdict (PR-04) → FR-CONV.4 Five Adversarial Axes (PR-07) → FR-CONV.5 Retry monotonicity guards (PR-02) → FR-CONV.6 Synthetic DNSP finding (PR-03) → Post-merge K-003 audit + NFR-CONV.4 token measurement → v3.9 GA.

**Key architectural decisions:**

- Intent-port over implementation-port — adapt `/sc:tasklist` *intent* (5 mechanisms), not implementation, per FINAL-REPORT §6.3 asymmetric finding cross-paradigm pattern.
- Additive-only governance (A-002) — no existing rf-qa check, rf-qa-qualitative checklist item, gate stage, output field, or `.dev/tasks/` layout entry is renamed, renumbered, or removed.
- Per-check classification (CB-3) — import only 8 unique TB-Add checks, not bulk-port all 17/20 `/sc:tasklist` Stage-6 checks; 11 are bundle-specific and inapplicable to single-MDTM output.
- Determinism scope split (NFR-CONV.1 vs NFR-CONV.2) — structural fields byte-deterministic; research-driven prose explicitly excluded from determinism scope.
- All-agents-fail guard precedence — DNSP synthetic-dnsp emits ONLY when ≥1 partition succeeded AND ≥1 exhausted; zero-success falls through to existing `rf-team-lead.md:417` 3-fix-cycle HALT (verified NO DRIFT 2026-05-14).
- Regression detection has STRICT PRECEDENCE over monotonicity guard — PASS@N→FAIL@N+1 flip emits verbatim regression message and exits BEFORE the monotonicity check.

**Open risks requiring resolution before M1:**

- SC-1 CRITICAL contradiction (Q-DM-1): PRD §25.4 declares the per-item 5-field schema is `{Description, Context, Acceptance, Confidence, Verification}` at `SKILL.md:1452-1457`, but current source content is `{Context, Action, Output, Verification, Completion gate}`. Engineering Lead decision required before FR-CONV.1 (TB-Add-8 enforcement target) implementation begins.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation — Q-DM-1 Resolution & Data-Model Definition|Foundation|P0|S|None|15|HIGH (Q-DM-1 blocker)|
|M2|FR-CONV.1 Structural Gate Catalogue (PR-06)|Core Logic|P0|M|M1|18|MED|
|M3|FR-CONV.2 Execution Context Header (PR-01)|Core Logic|P0|S|M2|11|LOW|
|M4|FR-CONV.3+FR-CONV.4 Inter-Agent Verdict Channel (PR-04, PR-07)|Integration|P0|L|M3|22|MED|
|M5|FR-CONV.5+FR-CONV.6 Retry Resilience & DNSP (PR-02, PR-03)|Integration|P0|L|M4|26|MED|
|M6|Hardening, Audit, NFR Measurement & GA|Production Readiness|P0|L|M5|14|MED|

## Dependency Graph

```
M1 (Foundation: Q-DM-1, DM-001..005, governance) ──▶ M2 (FR-CONV.1 / PR-06: TB-Add-1..8) ──▶ M3 (FR-CONV.2 / PR-01: Execution Context header)
                                                                                                            │
                                                                                                            ▼
M6 (Hardening + K-003 audit + NFR measurement + GA) ◀── M5 (FR-CONV.5/PR-02 → FR-CONV.6/PR-03) ◀── M4 (FR-CONV.3/PR-04 → FR-CONV.4/PR-07)

Cross-FR composition edges:
  FR-CONV.1 ──(INV-010 dynamic enumeration source)──▶ FR-CONV.3
  FR-CONV.2 ──(TB-Add-7 cross-validation; INV-013)──▶ FR-CONV.4
  FR-CONV.3 ──(items NOT in inherited PASS get 5-axis lens)──▶ FR-CONV.4
  FR-CONV.5 ◀──(INV-012 dedup-key composition with |F_n|)──▶ FR-CONV.6
  rf-team-lead.md:417 (UNMODIFIED) ◀──(all-agents-fail guard preserved)── FR-CONV.6
```

## M1: Foundation — Q-DM-1 Resolution & Data-Model Definition

**Objective:** Resolve the SC-1 CRITICAL schema contradiction blocking FR-CONV.1 and lock the five data-model entities and inter-agent contract surfaces before any FR implementation begins. | **Duration:** Week 1 (2026-05-15 → 2026-05-21) | **Entry:** TDD §22 Q-DM-1 documented; release-spec.md v1.0.0 stable; `make verify-sync` PASS on master | **Exit:** Q-DM-1 closed with Engineering Lead decision recorded; DM-001..DM-005 schemas frozen at schema_version 1.0.0; conflict-register.md 5 CASE-D rows validated; governance + sync-discipline checks operational

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|Q-DM-1|Resolve SC-1 schema contradiction|Engineering Lead decision selecting option (a) net-new schema migration, (b) PRD pointer correction, or (c) schema lives elsewhere; records resolution rationale in TDD §22 with cited authoritative source|SKILL.md|—|Decision recorded with chosen schema fields; TB-Add-8 enforcement target named (Context field invariant across options); A-002 governance impact assessed; PRD §25.4 and SKILL.md:1450-1460 reconciled|S|P0|
|2|DM-001|Define Execution Context Header schema|Lock 3-field schema (References, Source areas, Key constraints) with degradation rule (References-only on minimal BUILD_REQUEST); hidden-input determinism guard NO file paths in header|SKILL.md|Q-DM-1|References:list[string] R-### prefix; Source-areas:list[string] NEVER file paths; Key-constraints:list[string] 1-3 items; degradation explicit-omit not blank-but-present; grep "src/\|/.*:[0-9]+" against header returns 0|S|P0|
|3|DM-002|Define Inherited Structural Verdict Block schema|Lock 3-field schema (rf_qa_table_verbatim, prompt_directive fixed-text, reinjection_rule fixed-text); INV-002 freshness contract; INV-010 dynamic enumeration; INV-019 Self-Audit obligation|rf-qa-qualitative.md|Q-DM-1|rf_qa_table_verbatim:string byte-exact-copy; prompt_directive:string fixed "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."; reinjection_rule:string fixed cycle-N+1 reinjection|S|P0|
|4|DM-003|Define Synthetic DNSP Finding schema|Lock 7-field schema (severity HIGH fixed, source synthetic-dnsp fixed, affected_range, evidence, recommendation fixed, dedup_key 2-tuple, found_n_times int default 1); closed vocabulary for escalation_ladder_exhaust_point|rf-qa.md, rf-analyst.md|Q-DM-1|severity:enum=HIGH non-overridable; source:string="synthetic-dnsp" grep-able sentinel; affected_range:string verbatim from assigned_files; evidence:string never-blank; recommendation:string fixed text; dedup_key:tuple canonical YAML list; escalation_ladder_exhaust_point vocabulary={retry-1,retry-2,gap-fill-round-1,gap-fill-round-2,gap-fill-round-3}; found_n_times:int default 1 increments on dedup|S|P0|
|5|DM-004|Define Per-Item Checklist Schema target|Operational schema per Q-DM-1 resolution (PRD §25.4 target OR current-source schema OR new schema); TB-Add-8 enforcement target named|SKILL.md|Q-DM-1, DM-001|Schema fields:5; Context field present in all options invariant; TB-Add-8 file:line citation OR justified-absence applied to Context field; per-item self-contained 5-field structure preserved|S|P0|
|6|DM-005|Define rf-qa → rf-qa-qualitative Phase Contract|Lock 10-field phase contract (producer, consumer, artifact, schema_version 1.0.0, delivery_semantics at-most-once-per-cycle, freshness_rule, enumeration_rule, consumer_obligation, anti_inflation, failure_mode)|rf-qa.md, rf-qa-qualitative.md|DM-002|producer:string="rf-qa" fixed; consumer:string="rf-qa-qualitative" fixed; artifact:string="## Inherited Structural Verdict block in spawn prompt" byte-matches DM-002 header; schema_version:string="1.0.0" semver; delivery_semantics:string="at-most-once-per-cycle"; failure_mode if rf-qa no-verdict then rf-qa-qualitative MUST NOT spawn|S|P0|
|7|API-001|Document BUILD_REQUEST → MDTM Task File contract|Internal contract documentation; 15-field BUILD_REQUEST schema preserved; optional EXECUTION_CONTEXT_REQUIREMENTS signal added; MALFORMED return path documented (max 2 retries)|SKILL.md|DM-001|Contract documented at SKILL.md:1407-1487; producer task-builder; consumer rf-task-builder; transport Skill-tool prompt; error behavior orchestrator cannot derive References → MALFORMED return; rf-task-builder MALFORMED retry counter max=2|S|P0|
|8|API-002|Document rf-qa → rf-qa-qualitative phase-contract API|Spawn-prompt injection at SKILL.md §A.10.5; verbatim verdict-table extraction; INV-002 reinjection; INV-010 dynamic enumeration; INV-019 Self-Audit|SKILL.md, rf-qa.md, rf-qa-qualitative.md|DM-005|Insertion point SKILL.md:923-1000 range identified (~:966); verdict source `${TASK_DIR}qa/qa-task-integrity.md`; orchestrator-mediated injection; failure mode no-spawn|S|P0|
|9|API-003|Document Partition Agent → Orchestrator synthetic-dnsp emission API|Structured block in agent normal output stream (no separate channel); per-partition-instance cardinality; within-cycle dedup collapse; INV-021 within-agent-instance emission|rf-qa.md, rf-analyst.md, rf-qa-qualitative.md|DM-003|Transport structured block in normal output; cardinality one per exhausted partition; all-agents-fail precedence documented; HIGH severity non-overridable|S|P0|
|10|API-004|Document Fix-Loop Halt Signals API|Halt message strings (verbatim required for fixture parity); precedence order regression→monotonicity→hard-cap→proceed; F_n set definition (item identity = dedup-key)|rf-task-builder.md, rf-qa.md|DM-003|Monotonicity halt verbatim `[HALT-MONOTONICITY] |F|=<n>`; regression halt verbatim `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`; precedence regression FIRST; F-set cardinality after dedup|S|P0|
|11|API-005|Document All-Partition-Agents-Fail → rf-team-lead escalation API|Existing escalation preserved verbatim per rf-team-lead.md:417; FR-CONV.6 Negative Criterion enforced; NO DRIFT verification|rf-team-lead.md|Q-DM-1|Escalation path unchanged; 3 fix cycles per phase; HALT-and-ask-user; NO DNSP emission on zero-partitions-succeeded; line 417 anchor verified|S|P0|
|12|GOV-1|Lock Five Adversarial Axes canonical definitions|Define AX-1 Drift, AX-2 Contradictions, AX-3 Omissions, AX-4 Weakened criteria, AX-5 Invented content (plus `none` sentinel); annotation rules — axes multiply lenses not checks; TOTAL stays at 15 items|rf-qa-qualitative.md|—|AX-1..AX-5 canonical definitions recorded in TDD §8.5; closed vocabulary {AX-1, AX-2, AX-3, AX-4, AX-5, none, drift-axis-inactive}; Tool Engagement Minimum floor preserved tool-calls ≥ 15 NOT ≥ 15×5|S|P0|
|13|GOV-2|Validate conflict-register.md CASE-D rows|5 CASE-D rows present (PR-01, PR-02, PR-06, PR-07, PR-05-deferred); 2 CASE-B proposals (PR-03, PR-04) correctly absent; protected invariant named per row|—|—|conflict-register.md row count=5 CASE-D; PR-03 and PR-04 absent (CASE-B); each row names conflicting `/sc:tasklist` mechanism + protected invariant|S|P0|
|14|GOV-3|Establish sync-discipline pre-commit guard|`make verify-sync` PASS gate enforced before each FR commit; A-001 workflow documented in CLAUDE.md; K-009 mitigation tooling operational|—|—|`make verify-sync` runs in CI on PR; src/superclaude/ ↔ .claude/ byte-equal post-`make sync-dev`; pre-commit hook (or CI gate) blocks commit on FAIL|S|P0|
|15|GOV-4|Lock landing-order serialization rule|Authoritative landing order PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 recorded in release-spec.md §4.6 and TDD §19.1; K-007 mitigation; git-log inspection planned for release checklist|—|—|Landing order documented as single source of truth; cross-references in §5, §6, §23 do not redefine; git log visible serial chain enforced via CI ordering or PR review|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|DM-001..DM-005|Schema definitions|Define-only at M1|M1|All downstream FR implementations (M2-M5)|
|API-001..API-005|Contract documentation|Define-only at M1|M1|All downstream FR implementations + tests (M2-M5)|
|conflict-register.md|CASE-D ledger (registry)|Pre-existing|M1|FR-CONV.1 (PR-06), FR-CONV.2 (PR-01), FR-CONV.4 (PR-07), FR-CONV.5 (PR-02) traceability|
|make verify-sync CI hook|Sync-discipline gate (pre-commit / CI middleware)|Operational|M1|All FR commits in M2-M5|

### Milestone Dependencies — M1

- None — this is the foundation milestone.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-DM-1|SC-1 CRITICAL: PRD §25.4 declares per-item 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` "preserved unchanged" at SKILL.md:1452-1457, but current SKILL.md:1450-1460 holds `{Context, Action, Output, Verification, Completion gate}`. Three resolution options listed in TDD §7.1 Entity 4. Engineering Lead decision REQUIRED before FR-CONV.1 implementation.|Blocks FR-CONV.1 (TB-Add-8 enforcement target naming); affects A-002 governance compliance if option (a) chosen (net-new schema); cascades to DM-004, DM-001, FR-CONV.2 Negative Criterion|Engineering Lead|2026-05-21 (pre-M2)|
|2|OPEN-INV-018|If `.dev/tasks/` directory layout changes during release window, all 6 FRs require re-integration (K-008 portfolio-wide blast radius). Need layout-change contract documented.|Cross-milestone — invalidates M2-M6 deliverables if triggered; SP-33 stability commitment is the operational mitigation|Engineering Lead|Pre-M2|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Q-DM-1 unresolved at end of week 1|HIGH|MEDIUM|Blocks entire roadmap from progressing to M2; FR-CONV.1 cannot define TB-Add-8 enforcement target without authoritative schema|Engineering Lead time-boxed decision; document 3 options in TDD §22 for fast Lead review; escalate if not closed by 2026-05-19|Engineering Lead|
|2|K-009 sync-discipline violated during M1 governance setup|MED|LOW|`.claude/` edited directly; `make verify-sync` FAIL blocks first FR commit|CLAUDE.md mandates workflow; CI gate operational at end of M1|Per-commit author|
|3|K-008 INV-018 `.dev/tasks/` layout change detected|HIGH|LOW|Portfolio-wide re-integration; all 6 FRs must be re-anchored|Layout-change contract documented; SP-33 stability commitment reaffirmed|Engineering Lead|

## M2: FR-CONV.1 Structural Gate Catalogue (PR-06)

**Objective:** Land 8 strictly-additive structural checks (TB-Add-1..8) into rf-qa's task-integrity gate, mirrored across three definition sites (rf-qa.md 20-item checklist, SKILL.md A.10 9-item block, SKILL.md 15-item validation block). Activate INV-010 dynamic-enumeration source so downstream FR-CONV.3 can consume the catalogue. | **Duration:** Weeks 2-3 (2026-05-22 → 2026-06-04) | **Entry:** M1 exit criteria met; Q-DM-1 closed; DM-004 per-item schema target locked | **Exit:** TB-Add-1/3/4/5/6/7/8 hard checks operational; TB-Add-2 advisory operational; `make verify-sync` PASS; 9 unit fixtures (TEST-001..003 + 6 negative-criterion fixtures) PASS; rf-qa.md:268-287 + SKILL.md:~898-906 + SKILL.md:~1491-1507 grep returns ≥3 hits per TB-Add ID

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|16|FR-CONV.1|Append TB-Add-1..8 catalogue to rf-qa task-integrity gate (PR-06)|Master FR — appends 8 structural checks across 3 definition surfaces; CASE D protected invariant zero-trust QA; strictly-additive per A-002|rf-qa.md, SKILL.md|M1|TB-Add-1..8 appear at rf-qa.md:268-287 AND SKILL.md:~898-906 AND SKILL.md:~1491-1507; existing 9-item / 15-item / 20-item items preserved verbatim; no bundle-specific `/sc:tasklist` checks (phase-file naming, R-### roadmap traceability, checkpoint emission) appear in any TB-Add; `grep -nE "TB-Add-[1-8]"` returns ≥3 hits per ID|M|P0|
|17|TB-Add-1|Implement placeholder scan check|Hard check; fires on "TBD"/"TODO"/title-only checklist items; emits distinct item-ID-naming error; gate verdict FAIL|rf-qa.md|FR-CONV.1|Fires on placeholder item; emits item-ID-naming error; gate FAIL; no false-positive on legitimate description prose|S|P0|
|18|TB-Add-2|Implement item-count bounds advisory (≥3 / ≤40-track / ≤50-single-track)|`[ADVISORY]`-only until OPEN-INV-006 calibration; emits prefixed message; does NOT block gate|rf-qa.md|FR-CONV.1, OPEN-INV-006|Bounds out-of-range emits `[ADVISORY] item count <n> outside recommended bounds`; gate verdict NOT changed; PASS verdict still possible with advisory present|S|P0|
|19|TB-Add-3|Implement clarification-adjacency check|Hard check; fires when checklist items are adjacent to blocked/clarification-needed items; emits distinct error; gate FAIL|rf-qa.md|FR-CONV.1|Adjacency rule documented; fires on contiguous block-and-active items pattern; gate FAIL|S|P0|
|20|TB-Add-4|Implement circular-dependency DAG check|Hard check; cycle detection across intra-phase + inter-phase dependencies; emits item-ID-naming error; gate FAIL|rf-qa.md|FR-CONV.1|DAG cycle in dependency graph emits TB-Add-4 error; cycle items named; gate FAIL; non-cyclic graphs pass|M|P0|
|21|TB-Add-5|Implement granularity check (XL items have subtasks)|Hard check; fires when item flagged XL effort but has no decomposition into subtasks; emits error; gate FAIL|rf-qa.md|FR-CONV.1|XL effort item without subtasks fires TB-Add-5; S/M/L effort items unaffected; gate FAIL|S|P0|
|22|TB-Add-6|Implement Confidence/Verification format-consistency check|Hard check; validates Confidence enum {HIGH, MEDIUM, LOW} + rationale present; Verification field non-empty; emits error; gate FAIL|rf-qa.md|FR-CONV.1, DM-004|Confidence outside {HIGH, MEDIUM, LOW} or missing rationale → TB-Add-6 FAIL; empty Verification → TB-Add-6 FAIL|S|P0|
|23|TB-Add-7|Implement Execution-Context source-areas cross-validation|Hard check; validates each `Source areas:` entry from Execution Context header reappears in ≥1 per-item Context field; absorbs PR-01 failure-mode #4 cross-validation|rf-qa.md|FR-CONV.1, DM-001|Header `Source areas:` entries grep against item Context fields; missing area emits TB-Add-7 error; tolerates degraded header (References-only) without FAIL|M|P0|
|24|TB-Add-8|Implement per-item Context file:line citation OR justified-absence check|Hard check; resolves INV-015; validates per-item Context field has ≥1 file:line citation OR justified-absence comment; applied to schema-resolved Context field per Q-DM-1 outcome|rf-qa.md|FR-CONV.1, DM-004|Bare `Context: src/foo` (no `:N`) fires TB-Add-8 FAIL; `Context: src/foo:42` PASS; `Context: <none — pure refactor> [justified-absence]` PASS|M|P0|
|25|COMP-002|Update rf-qa.md task-integrity phase (4-phase QA agent)|Append TB-Add-1..8 catalogue at rf-qa.md:268-287 (20-item checklist sub-header at :266); existing 20 items preserved verbatim; key anchor zero-trust verdict at :141-142 unchanged|rf-qa.md|FR-CONV.1|rf-qa.md grows from 432 lines to ~432+~80 lines; existing items 1-20 byte-stable; new TB-Add-1..8 appear as items 21-28; rf-qa.md:141-142 byte-stable|M|P0|
|26|COMP-001 (M2 scope)|Update task-builder/SKILL.md A.10 mirror|Mirror TB-Add catalogue in SKILL.md:~898-906 (9-item A.10 block, append point after line 906); preserve existing 9 items verbatim|SKILL.md|FR-CONV.1, COMP-002|9-item A.10 block grows to 17 items (9 existing + 8 TB-Add); existing 9 items byte-stable; new TB-Add-1..8 appear as items 10-17 in mirror|S|P0|
|27|COMP-001 (M2 scope b)|Update task-builder/SKILL.md 15-item validation block|Mirror TB-Add catalogue in SKILL.md:~1491-1507 (15-item validation block); preserve existing 15 items verbatim|SKILL.md|FR-CONV.1, COMP-002|15-item validation block grows to 23 items; existing 15 items byte-stable; new TB-Add-1..8 appear as items 16-23|S|P0|
|28|NFR-CONV.1|Implement determinism guard for TB-Add structural verdicts|TB-Add-1..8 PASS/FAIL verdicts MUST be byte-identical across two runs on same BUILD_REQUEST + source tree (structural fields scope)|rf-qa.md|FR-CONV.1|Re-run task-builder on identical BUILD_REQUEST; diff TB-Add-1..8 emission lines; byte-identical|S|P0|
|29|NFR-CONV.5|Validate wall-clock guard for FR-CONV.1|No new external dependencies, no synchronous network calls added by TB-Add catalogue; only existing tools (Read, Grep, Glob, Bash) used|rf-qa.md|FR-CONV.1|Inspect rf-qa.md diff; no new tool invocation appears; CI lint reject on new dep|S|P0|
|30|NFR-CONV.6|Validate self-contained-item invariant under TB-Add-1..8|Synthetic fixture with all per-item schema fields populated PASSES all 8 TB-Add; same fixture with one field stripped FAILS TB-Add-1 (fail-closed)|rf-qa.md|FR-CONV.1, DM-004|Fixture pair: complete-5-field PASSES; field-stripped FAILS TB-Add-1; invariant preserved|S|P0|
|31|NFR-CONV.7|Validate evidence-bound-item invariant via TB-Add-8|Three-fixture triple per NFR-CONV.7 acceptance: bare Context FAILS, file:line PASSES, justified-absence PASSES|rf-qa.md|TB-Add-8|Fixture (a) `Context: src/foo` FAIL TB-Add-8; (b) `Context: src/foo:42` PASS; (c) `Context: <none — pure refactor> [justified-absence]` PASS|S|P0|
|32|TEST-001|test_placeholder_tb_add_1 fixture|Synthetic MDTM with "TBD"/"TODO"/title-only checklist item; expected TB-Add-1 emits item-ID-naming error and gate FAILs|rf-qa.md|TB-Add-1|`uv run pytest tests/task_builder/test_placeholder_tb_add_1.py -v` PASSES; grep for TB-Add-1 error line in gate log|S|P0|
|33|TEST-002|test_dag_cycle_tb_add_4 fixture|Synthetic MDTM with circular intra-/inter-phase dependency; expected TB-Add-4 emits; gate FAILs|rf-qa.md|TB-Add-4|`uv run pytest tests/task_builder/test_dag_cycle_tb_add_4.py -v` PASSES; cycle items named in error|S|P0|
|34|MIG-001|Land FR-CONV.1 (PR-06) commit — M1.1|Single revertable commit appending TB-Add-1..8 across 3 definition surfaces; serial landing position 1st; rollback per revert-specific-line OR full PR-06 revert; co-revert with FR-CONV.3 dynamic-enumeration consumer required if reverted (per §19.4 matrix)|rf-qa.md, SKILL.md|M1, all M2 items|Single commit; `make verify-sync` PASS post-commit; rf-qa.md, SKILL.md changes byte-equal between src/superclaude and .claude; co-revert dependency recorded|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|TB-Add-1..8 catalogue|rf-qa task-integrity checklist (dispatch table extension)|Activated M2 commit|M2|FR-CONV.3 (INV-010 dynamic enumeration); FR-CONV.5 (`|F_n|` count source)|
|TB-Add-7 cross-validation rule|Cross-FR validation (consumes Execution Context header)|Defined M2; activated M3 (header lands)|M2 (define) → M3 (activate)|FR-CONV.2 Negative Criterion enforcement|
|TB-Add-8 enforcement target|Schema-specific check (consumes Context field per DM-004)|Defined M2|M2|All per-item Context field generation; NFR-CONV.7 invariant probe|

### Milestone Dependencies — M2

- M1 (Q-DM-1 closed; DM-004 schema locked; conflict-register.md CASE-D row for PR-06 validated)

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-001 TB-Add false positives waste fix-cycles|LOW|LOW|Wasted retry tokens; developer frustration; possible roll-back of specific TB-Add line|Each TB-Add cites source-check-ID for traceability; TB-Add-2 ships `[ADVISORY]`; individually revertable per append line|rf-qa maintainer|
|2|K-009 sync-discipline violated during M2 commit|MED|LOW|`.claude/` direct-edit detected; `make verify-sync` FAIL post-commit|CLAUDE.md mandates workflow; pre-commit hook + CI gate operational; revert direct edit and re-run from src/superclaude (K-009 contingency)|Per-commit author|
|3|Bundle-specific check leak in TB-Add (FR-CONV.1 Negative Criterion violation)|MED|LOW|Phase-file naming, R-### roadmap traceability, checkpoint emission appears in TB-Add catalogue|Code review checklist gate enforces FR-CONV.1 Negative Criterion; CB-3 per-check classification documented|rf-qa maintainer|

## M3: FR-CONV.2 Execution Context Header (PR-01)

**Objective:** Insert task-level `## Execution Context` block (3 labeled lines: References / Source areas / Key constraints) into generated MDTM task files between frontmatter and Phase 1. Header is hidden-input-deterministic (NO file paths in header) while per-item Context fields retain file:line citations (TB-Add-8 enforces). | **Duration:** Week 4 (2026-06-05 → 2026-06-11) | **Entry:** M2 exit criteria met; FR-CONV.1 PR-06 commit landed; TB-Add-7 cross-validation rule live and waiting for header source | **Exit:** Generated MDTM files contain `## Execution Context` block; minimal-BUILD_REQUEST degrades to References-only (other lines explicitly omitted not blank-but-present); `grep -E "src/\|/.*:[0-9]+"` against header range returns 0 hits; TEST-004/005/006 PASS

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|35|FR-CONV.2|Insert Execution Context header into MDTM template (PR-01)|Master FR — task-level header at top of generated MDTM file; 3 labeled lines; CASE D protected invariant evidence-bound-item; scope-confined NO file paths in header|SKILL.md, rf-task-builder.md|M2|`## Execution Context` block emits after frontmatter / `## Prerequisites & Dependencies` and before `## Phase 1`; 3 labeled lines on full BUILD_REQUEST; degrades to References-only on minimal BUILD_REQUEST (other 2 lines OMITTED not blank); grep `src/\|/.*:[0-9]+` against header range returns 0|S|P0|
|36|COMP-001 (M3 scope a)|Update SKILL.md primary template (lines 1407-1487)|Insert `## Execution Context` block in primary template; preserve frontmatter and Phase-1 boundaries; preserve per-item self-contained 5-field schema|SKILL.md|FR-CONV.2|Primary template at SKILL.md:1407-1487 modified to emit header at top; existing template structure preserved|S|P0|
|37|COMP-001 (M3 scope b)|Update SKILL.md BUILD_REQUEST prompt guidance (lines 715-725)|Add EXECUTION_CONTEXT_REQUIREMENTS optional signal to BUILD_REQUEST handling; preserve existing 15-field schema|SKILL.md|FR-CONV.2, API-001|Prompt guidance at SKILL.md:715-725 updated; orchestrator can derive References from GOAL+WHY+related_docs; MALFORMED retry path documented|S|P0|
|38|COMP-001 (M3 scope c)|Update SKILL.md Execution Overview header anchor (~:139) and Tier Selection anchor (~:86)|Header policy anchor; tier-aware emission documented; consistent with degraded References-only behavior|SKILL.md|FR-CONV.2|Anchors updated; tier-aware policy expressed; consistent across Quick/Standard/Deep tiers|S|P0|
|39|COMP-005|Update rf-task-builder.md to emit header|rf-task-builder consumes optional EXECUTION_CONTEXT_REQUIREMENTS signal; emits header into MDTM at correct position|rf-task-builder.md|FR-CONV.2, COMP-001 (M3a)|rf-task-builder generation logic emits header per DM-001 schema; insertion position preserved across templates|S|P0|
|40|NFR-CONV.3|Validate hidden-input determinism guard for header|task-builder MUST NOT read .dev/tasks/done/ to populate header; fixture-populated done/ produces byte-identical header to empty done/|SKILL.md|FR-CONV.2|Run task-builder against identical BUILD_REQUEST with .dev/tasks/done/ (a) empty (b) populated 10+ historical tasks ≥3 task_types; diff structural fields; byte-identical|S|P0|
|41|NFR-CONV.7 (M3 reinforcement)|Reinforce evidence-bound-item invariant under header presence|Header introduction MUST NOT alter per-item Context field requirement; TB-Add-8 continues to enforce file:line OR justified-absence on per-item Context|SKILL.md, rf-qa.md|FR-CONV.2, TB-Add-8|Per-item Context field schema unchanged; TB-Add-8 verification suite re-PASSES post-header introduction|S|P0|
|42|TEST-004|test_execution_context_full fixture|Generated MDTM contains 3-labeled-line header on full BUILD_REQUEST|SKILL.md|FR-CONV.2|Assertion `grep -n "## Execution Context"` returns N; next 10 lines contain `References:` AND `Source areas:` AND `Key constraints:`|S|P0|
|43|TEST-005|test_execution_context_minimal_buildrequest fixture|Minimal BUILD_REQUEST (GOAL only) → header degrades to References-only; other lines OMITTED|SKILL.md|FR-CONV.2|Assertion grep matches degraded References-only form; `Source areas:` and `Key constraints:` lines absent (not blank)|S|P0|
|44|TEST-006|test_execution_context_no_file_paths fixture|Hidden-input determinism for header range — grep against header returns 0 file paths|SKILL.md|FR-CONV.2|`grep -E "src/\|/.*:[0-9]+"` against `## Execution Context` block range returns exactly 0 hits|S|P0|
|45|MIG-002|Land FR-CONV.2 (PR-01) commit — M1.2|Single revertable commit; serial landing position 2nd; rollback by disabling header generation; A-002 strictly-additive|SKILL.md, rf-task-builder.md|MIG-001|Single commit; `make verify-sync` PASS post-commit; degradation path verified empty/full BUILD_REQUEST|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`## Execution Context` header|MDTM template insertion (template-driven generation)|Activated M3 commit|M3|TB-Add-7 cross-validation (consumes header `Source areas:` lines); downstream executor agents reading MDTM|
|EXECUTION_CONTEXT_REQUIREMENTS signal|Optional BUILD_REQUEST field (callback parameter)|Defined M3|M3|rf-task-builder header-emission logic|

### Milestone Dependencies — M3

- M2 (FR-CONV.1 PR-06 landed; TB-Add-7 cross-validation rule live; TB-Add-8 enforcement target known per Q-DM-1)

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-002 Execution Context header drift (header source-areas != items)|LOW|LOW|TB-Add-7 fires on every gate; fix-cycle thrash|TB-Add-7 cross-validates; on drift gate fails; degraded References-only fallback|task-builder maintainer|
|2|Hidden-input contamination via header generation logic|MED|LOW|Determinism violated; NFR-CONV.3 fixture FAILS|NFR-CONV.3 test guards; orchestrator code reviewed against `.dev/tasks/done/` reads|task-builder maintainer|
|3|Per-item Context regression (header introduction strips per-item file:line)|HIGH|LOW|Evidence-bound-item invariant violated|FR-CONV.2 Negative Criterion + NFR-CONV.7 reinforcement test (M3 item 41); TB-Add-8 fires|task-builder maintainer + rf-qa maintainer|

## M4: FR-CONV.3 + FR-CONV.4 Inter-Agent Verdict Channel (PR-04, PR-07)

**Objective:** Establish explicit verdict passthrough from rf-qa task-integrity to rf-qa-qualitative task-qualitative (FR-CONV.3 / PR-04), then overlay the Five Adversarial Axes annotation on rf-qa-qualitative's existing 15-item checklist (FR-CONV.4 / PR-07). Both FRs preserve the anti-inflation rule at `rf-qa-qualitative.md:766-775` and mandate Self-Audit (INV-019). | **Duration:** Weeks 5-6 (2026-06-12 → 2026-06-25) | **Entry:** M3 exit criteria met; FR-CONV.1 + FR-CONV.2 commits landed; INV-010 dynamic-enumeration source active | **Exit:** `## Inherited Structural Verdict` block in rf-qa-qualitative spawn prompt; `### Five Adversarial Axes` header BEFORE 15-item checklist; axis column populated on every Items Reviewed row; Self-Audit mandatory; K-003 audit-target activated for first 5 real runs

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|46|FR-CONV.3|Inject Inherited Structural Verdict block (PR-04)|Master FR — orchestrator-mediated spawn-prompt injection at SKILL.md §A.10.5 (~:966); rf-qa task-integrity verdict-table verbatim into rf-qa-qualitative spawn; CASE B invariant alignment zero-trust QA|SKILL.md, rf-qa-qualitative.md|M3|`## Inherited Structural Verdict` block injected verbatim; INV-002 cycle-N+1 reinjection on every fix-cycle (no memoization); INV-010 dynamic enumeration over TB-Add catalogue; INV-019 Self-Audit mandate (≥1 semantic check beyond inherited PASS); anti-inflation rule at rf-qa-qualitative.md:766-775 byte-stable|M|P0|
|47|COMP-001 (M4 scope a)|Update SKILL.md §A.10.5 spawn-prompt injection logic|Orchestrator reads rf-qa task-integrity report; extracts `## Items Reviewed` table verbatim; splices into rf-qa-qualitative spawn prompt; emits `## Inherited Structural Verdict` header|SKILL.md|FR-CONV.3|Injection at SKILL.md:923-1000 range (~:966); insertion inside §A.10.5 spawn-prompt fenced block after `TARGET FILES` and before `INSTRUCTIONS:`; verbatim extraction|M|P0|
|48|COMP-003 (M4 scope a)|Append "Handling the Inherited Structural Verdict" section to rf-qa-qualitative.md|EOF append at rf-qa-qualitative.md:794; add `## Self-Audit` to output schema; documents INV-019 obligation; preserves anti-inflation rule|rf-qa-qualitative.md|FR-CONV.3|EOF append at :794; `## Self-Audit` output schema; anti-inflation rule at :766-775 byte-stable; severity floor at :786-795 byte-stable|M|P0|
|49|NFR-CONV.9 (M4 reinforcement)|Reinforce zero-trust QA invariant under FR-CONV.3|Inherited verdict is a RELIANCE channel for STRUCTURAL items only; semantic items continue to require independent tool calls; no item VERIFIED solely from inherited verdict|rf-qa-qualitative.md|FR-CONV.3|2-part fixture: (a) 1-LOW-finding fixture → gate FAILS; (b) FR-CONV.3 inherited-verdict applied → no item VERIFIED unless Self-Audit lists independent semantic-check engagement|M|P0|
|50|TEST-007|test_inherited_verdict_present fixture|`## Inherited Structural Verdict` block appears in rf-qa-qualitative spawn prompt|SKILL.md|FR-CONV.3|grep matches block header in spawn-prompt log; diff identically against `${TASK_DIR}qa/qa-task-integrity.md` Items Reviewed table|S|P0|
|51|TEST-008|test_inherited_verdict_freshness_inv_002 fixture|2-cycle fixture — cycle-2 spawn shows cycle-2 structural verdict not stale cycle-1|SKILL.md|FR-CONV.3|byte-diff of cycle-1 vs cycle-2 spawn prompts; cycle-2 contains current verdict not memoized prior|M|P0|
|52|TEST-009|test_self_audit_inv_019 fixture|rf-qa-qualitative output contains `## Self-Audit` with ≥1 semantic check beyond inherited verdict|rf-qa-qualitative.md|FR-CONV.3|grep `## Self-Audit` + content inspection; ≥1 entry documenting independent semantic-check engagement|S|P0|
|53|TEST-010|test_dynamic_enumeration_inv_010 fixture|When FR-CONV.1 TB-Add catalogue grows, rf-qa-qualitative checklist auto-richens to reference it|rf-qa-qualitative.md, rf-qa.md|FR-CONV.3, TB-Add-1..8|Structural diff of checklist before/after catalogue growth shows new TB-Add items referenced|M|P0|
|54|MIG-003|Land FR-CONV.3 (PR-04) commit — M1.3|Single revertable commit; serial landing position 3rd; rollback by disabling passthrough block; rf-qa-qualitative falls back to current behavior; co-revert with FR-CONV.1 INV-010 source if FR-CONV.1 reverted|SKILL.md, rf-qa-qualitative.md|MIG-002, all M4 FR-CONV.3 items|Single commit; `make verify-sync` PASS post-commit; K-003 audit-target activated for first 5 real runs|S|P0|
|55|FR-CONV.4|Insert Five Adversarial Axes overlay (PR-07)|Master FR — `### Five Adversarial Axes` header subsection BEFORE rf-qa-qualitative 15-item checklist; `axis` column on Items Reviewed table; CASE D protected invariant zero-trust QA; overlay-only (no new conditional code path)|rf-qa-qualitative.md, SKILL.md|MIG-003|`### Five Adversarial Axes` header inserted before `#### Checklist (15 items)` at rf-qa-qualitative.md:527; `axis` column inserted between `Check` and `Result` at :675-714; populated value from {AX-1, AX-2, AX-3, AX-4, AX-5, none}; `drift-axis-inactive` annotation when no checklist item restates BUILD_REQUEST.GOAL|M|P0|
|56|AX-1|Implement Drift axis definition|Canonical: "Cited fact (file path, line number, signature, count, config value) no longer matches current source"; consumes citations from per-item Context fields|rf-qa-qualitative.md|FR-CONV.4, GOV-1|Axis label `AX-1` documented at rf-qa-qualitative.md; example finding "Item 4.2 cites foo() at src/x.py:88; actual location :91"; annotation applied to Items Reviewed rows where citations drift|S|P0|
|57|AX-2|Implement Contradictions axis definition|Canonical: "Two artifacts (or two sections of one artifact) assert mutually incompatible facts about the same subject"|rf-qa-qualitative.md|FR-CONV.4, GOV-1|Axis label `AX-2`; example finding "Phase 3 says function returns dict; Phase 5 verification greps list return"; annotation applied across Items Reviewed rows|S|P0|
|58|AX-3|Implement Omissions axis definition|Canonical: "Required touchpoint, consumer, dependency, or step is absent from the plan"|rf-qa-qualitative.md|FR-CONV.4, GOV-1|Axis label `AX-3`; example "Item adds new kwarg but no item updates function signature to accept it"; annotation across Items Reviewed rows|S|P0|
|59|AX-4|Implement Weakened-criteria axis definition|Canonical: "Acceptance/verification condition softened to unobservable or trivially satisfiable"|rf-qa-qualitative.md|FR-CONV.4, GOV-1|Axis label `AX-4`; example "Verification reads `# Test` into file and asserts on 6-char placeholder"; annotation across Items Reviewed rows|S|P0|
|60|AX-5|Implement Invented-content axis definition|Canonical: "Artifact introduces a requirement, feature, or capability not present in its upstream source"|rf-qa-qualitative.md|FR-CONV.4, GOV-1|Axis label `AX-5`; example "TDD adds caching layer PRD never specified"; annotation across Items Reviewed rows|S|P0|
|61|COMP-003 (M4 scope b)|Insert Five Adversarial Axes header subsection|Header inserted BEFORE `#### Checklist (15 items)` at rf-qa-qualitative.md:527-583; body of 15-item checklist MUST be unmodified; axis column added to Items Reviewed table at :675-714|rf-qa-qualitative.md|FR-CONV.4, AX-1..AX-5|Header subsection emits before checklist body; 15-item checklist body byte-stable; `axis` column inserted between `Check` and `Result`; values from {AX-1..AX-5, none}|S|P0|
|62|COMP-001 (M4 scope b)|Update SKILL.md Task-Qualitative prompt at :961|Axis-annotation directive in spawn prompt; instruct rf-qa-qualitative to populate axis column per row from canonical vocabulary|SKILL.md|FR-CONV.4|Prompt directive at SKILL.md:961 emits axis-annotation instruction; closed vocabulary listed|S|P0|
|63|NFR-CONV.9 (M4 axes reinforcement)|Preserve severity floor under axis annotation|rf-qa-qualitative severity floor at :786-795 ("Contradictions are always IMPORTANT or CRITICAL") MUST NOT be weakened by axis annotation; axes annotate, do not substitute|rf-qa-qualitative.md|FR-CONV.4|byte-diff Critical Rules block at :786-795 before/after FR-CONV.4 commit; byte-identical|S|P0|
|64|TEST-011|test_five_axes_overlay fixture|`### Five Adversarial Axes` header appears BEFORE immutable 15-item task-qualitative checklist|rf-qa-qualitative.md|FR-CONV.4|grep ordering assertion: axes header line N; 15-item checklist header line M; N < M|S|P0|
|65|TEST-012|test_axis_column_populated fixture|Items Reviewed table at rf-qa-qualitative.md:675-714 carries non-empty axis value on every row|rf-qa-qualitative.md|FR-CONV.4|Parse table; assert no row has empty axis cell; all values from closed vocabulary {AX-1..AX-5, none, drift-axis-inactive}|S|P0|
|66|TEST-013|test_drift_axis_inactive_when_no_goal_baseline fixture|No GOAL-baseline item present → `drift-axis-inactive` annotation emitted (not N/A)|rf-qa-qualitative.md|FR-CONV.4, AX-1|grep matches `drift-axis-inactive` annotation in Summary block; AX-1 column shows annotation not blank|S|P0|
|67|TEST-014|test_severity_floor_unweakened fixture|rf-qa-qualitative severity floor at :786-795 unchanged after FR-CONV.4|rf-qa-qualitative.md|FR-CONV.4|byte-diff of Critical Rules block; PASS only on byte-equal|S|P0|
|68|MIG-004|Land FR-CONV.4 (PR-07) commit — M1.4|Single revertable commit; serial landing position 4th; rollback by removing axis column + drift-axis-inactive annotation; 15-item checklist untouched|rf-qa-qualitative.md, SKILL.md|MIG-003, all M4 FR-CONV.4 items|Single commit; `make verify-sync` PASS; INV-013 composition with FR-CONV.3 inherited PASS items verified|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`## Inherited Structural Verdict` block|Spawn-prompt injection (orchestrator middleware)|Activated M4 (MIG-003)|M4|rf-qa-qualitative task-qualitative phase|
|Phase Contract DM-005 schema_version 1.0.0|Versioned phase contract (registry)|Activated M4 (MIG-003)|M4|rf-qa producer + rf-qa-qualitative consumer|
|`### Five Adversarial Axes` header + axis column|Overlay annotation (template extension; no new code path)|Activated M4 (MIG-004)|M4|rf-qa-qualitative task-qualitative reports; downstream review|
|INV-019 Self-Audit obligation|Output-schema mandate (constraint)|Activated M4 (MIG-003)|M4|K-003 audit-target gate; QA Lead inspection|

### Milestone Dependencies — M4

- M3 (FR-CONV.2 PR-01 landed; Execution Context header live; TB-Add-7 cross-validation active)
- M2 (FR-CONV.1 PR-06 landed; INV-010 TB-Add catalogue source active for dynamic enumeration consumer)

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-X-002|PR-04 anti-inflation operational test — "reliance ≠ verification" distinction empirically observable, not structurally provable. K-003 audit-target activated; needs first 5 rf-qa-qualitative runs to validate.|If audit shows any item VERIFIED solely from inherited verdict without independent semantic check engagement, K-003 FAIL → disable passthrough (§19.4 rollback); FR-CONV.3 reverted|QA Lead|Post-MIG-003 + first 5 real runs (carries into M6 audit window)|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-003 PR-04 passthrough causes inflation despite anti-inflation rule|MED|LOW|rf-qa-qualitative marks items VERIFIED solely from inherited PASS; anti-inflation rule effectively weakened|INV-019 Self-Audit mandate; K-003 audit-target on first 5 real runs; rollback path documented; FR-CONV.3 reverted on FAIL|QA Lead|
|2|K-004 5-axis annotation ambiguity over-flags items|LOW|LOW|False-positive axis annotations create noise|Axes annotation-only; 15-item checklist still runs; severity floor preserved; `drift-axis-inactive` annotation; audit axis distribution post-merge|rf-qa-qualitative maintainer|
|3|K-007 PR-04 + PR-06 sequencing inversion|MED|LOW|If PR-04 lands before PR-06, dynamic enumeration cannot pick up TB-Add catalogue|Serial enforcement in release-spec §4.6 + GOV-4 commit ordering rule; INV-010 dynamic enumeration auto-richens once catalogue activates as ultimate fallback|Engineering Lead|
|4|Anti-inflation rule rephrased or weakened during M4 commits|HIGH|LOW|rf-qa-qualitative.md:766-775 byte-stability violated; semantic verification skip-eligibility expands beyond structural items|Code review gate enforces FR-CONV.3 Negative Criterion; byte-diff test of :766-775 block runs in CI; revert on FAIL|rf-qa-qualitative maintainer|

## M5: FR-CONV.5 + FR-CONV.6 Retry Resilience & DNSP (PR-02, PR-03)

**Objective:** Add monotonicity guard + regression detection halt-conditions to EXISTING fix-cycle retry loops (no new loop or stage) — FR-CONV.5 / PR-02 — then emit synthetic HIGH-severity DNSP findings on partition-agent escalation-ladder exhaust — FR-CONV.6 / PR-03 BASE. Together address the documented 21-retry / 18-batch oscillation and silent partition-exhaust failure modes. INV-012 dedup-key composition is the contract that links the two FRs. | **Duration:** Weeks 7-8 (2026-06-26 → 2026-07-09) | **Entry:** M4 exit criteria met; FR-CONV.3 + FR-CONV.4 commits landed; DM-003 dedup-key shape + halt-message verbatim strings locked | **Exit:** `[HALT-MONOTONICITY] |F|=<n>` halt fires on `|F_{n+1}| >= |F_n|`; verbatim regression message fires BEFORE monotonicity on PASS@N→FAIL@N+1; synthetic-dnsp 7-field finding emits on twice-exhaust with dedup collapse; all-agents-fail bypass preserved (rf-team-lead.md:417 NO DRIFT); 11 unit/integration fixtures (TEST-015..025) PASS

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|69|FR-CONV.5|Add monotonicity + regression halt to existing retry loops (PR-02)|Master FR — two stop-conditions on EXISTING fix-cycle retry loops; no new loop or stage; CASE D protected invariant zero-trust QA; precedence Regression > monotonicity|SKILL.md, rf-task-builder.md, rf-qa.md|MIG-004|`[HALT-MONOTONICITY] |F|=<n>` fires on `|F_{n+1}| >= |F_n|`; verbatim regression message fires BEFORE monotonicity check on PASS@N→FAIL@N+1; synthetic-dnsp identical dedup-key across consecutive cycles is dedup NOT regression (INV-012); legitimate slow-cycle correction (strict shrink even by 1) MUST NOT halt; 4 retry counters MUST NOT collapse|M|P0|
|70|COMP-001 (M5 scope a)|Update SKILL.md A.9 separate-counters tail (lines 867-873)|Document monotonicity guard + regression halt as additional stop-conditions on existing 4 retry counters; preserve separate-counter independence|SKILL.md|FR-CONV.5|Edit at SKILL.md:867-873 documents 2 new stop-conditions; 4 separate retry counters preserved unchanged in name and scope|S|P0|
|71|COMP-001 (M5 scope b)|Update SKILL.md Behavioral Constraints (lines 1547-1553)|Add hard-invariants list entries: regression-precedence-over-monotonicity; legitimate slow-shrink continues; no halt-on-slow-convergence threshold (X-003 REJECTED)|SKILL.md|FR-CONV.5|Edit at SKILL.md:1547-1553 lists hard invariants; X-003 REJECTED documented inline|S|P0|
|72|COMP-005 (M5 scope)|Update rf-task-builder.md QA-gate fix-cycle encoding (lines 334-361)|Encode monotonicity + regression halt-conditions in I16 per-gate fix-cycle table; preserve existing per-gate caps (research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, qualitative 3)|rf-task-builder.md|FR-CONV.5|Edit at rf-task-builder.md:334-361; per-gate caps unchanged; halt conditions layered on top trip earlier on pathological loops|M|P0|
|73|COMP-002 (M5 scope)|Update rf-qa.md Fix Cycle Protocol (lines ~308-315)|Promote existing SHOULD bullet to MUST-halt; document precedence rule|rf-qa.md|FR-CONV.5|Edit at rf-qa.md:~308-315 promotes SHOULD→MUST; rf-qa.md global max=3 preserved; per-gate caps in rf-task-builder.md remain authoritative|S|P0|
|74|TEST-015|test_monotonicity_halt_F_5_5_5 fixture|3-cycle `|F|=5,5,5` halts at cycle 2 with `[HALT-MONOTONICITY]|F|=5`; cycle 3 not attempted|rf-task-builder.md|FR-CONV.5|grep verbatim halt message; assert no cycle-3 log entry; execution log shows exit at cycle 2|S|P0|
|75|TEST-016|test_regression_halt_pass1_fail2 fixture|Item 3.2 PASS@1/FAIL@2 halts at cycle 2 with verbatim regression message BEFORE monotonicity check|rf-task-builder.md|FR-CONV.5|grep verbatim regression message; ordering assertion: regression check fires FIRST; monotonicity check skipped on regression|S|P0|
|76|TEST-017|test_slow_shrink_continues fixture|`|F|=5,4` continues — strict shrink holds; X-003 NOT triggered|rf-task-builder.md|FR-CONV.5|Execution log shows cycle continues to N+2; no halt message emitted; legitimate slow-cycle correction permitted|S|P0|
|77|MIG-005|Land FR-CONV.5 (PR-02) commit — M1.5|Single revertable commit; serial landing position 5th; rollback by disabling 2 guards individually; existing retry loops + per-gate caps continue; jointly revertable with FR-CONV.6 per §19.4|SKILL.md, rf-task-builder.md, rf-qa.md|all M5 FR-CONV.5 items|Single commit; `make verify-sync` PASS; halt-message verbatim strings locked; F_n composition with synthetic-dnsp documented|M|P0|
|78|FR-CONV.6|Emit synthetic-dnsp HIGH finding on partition exhaust (PR-03 BASE)|Master FR — synthetic finding into agent output stream on escalation-ladder exhaust; CASE B invariant alignment zero-trust QA + evidence-bound-item + parallel-research; preserves all-agents-fail guard at rf-team-lead.md:417|rf-qa.md, rf-analyst.md, rf-qa-qualitative.md, SKILL.md|MIG-005|7-field finding emits on twice-exhaust per partition; identical dedup-key collapse with `found N times`; zero-partitions-succeeded → NO synthetic emit + rf-team-lead.md:417 escalation runs; HIGH severity non-overridable; dedup-key MUST NOT cross-cycle (INV-012)|L|P0|
|79|COMP-001 (M5 scope c)|Update SKILL.md A.8 Research Quality Gate (lines 572-656)|Wire synthetic-dnsp finding emission into A.8 gate-result merge step; preserve existing escalation paths|SKILL.md|FR-CONV.6|Edit at SKILL.md:572-656; merge step accepts synthetic-dnsp findings as HIGH-severity entries; existing flow preserved|M|P0|
|80|COMP-001 (M5 scope d)|Update SKILL.md A.10 Task File Validation (lines 870-918)|Wire synthetic-dnsp finding emission into A.10 gate-result merge step; preserve existing escalation paths|SKILL.md|FR-CONV.6|Edit at SKILL.md:870-918; merge step accepts synthetic-dnsp findings; existing 9-item / TB-Add catalogue verdict preserved|M|P0|
|81|COMP-004|Update rf-analyst.md partition protocol (lines 58-71)|Add DNSP emission directive on escalation-ladder exhaust; preserve parallel partitioning protocol; INV-021 within-agent-instance emission|rf-analyst.md|FR-CONV.6, DM-003|Edit at rf-analyst.md:58-71 adds DNSP edit site; existing partition protocol byte-stable; emission only after twice-exhaust|M|P0|
|82|COMP-002 (M5 scope b)|Update rf-qa.md DNSP edit site (lines 49-77 + :70-77)|Add DNSP emission directive; preserve research-gate / synthesis-gate / report-validation / task-integrity 4-phase structure; INV-021|rf-qa.md|FR-CONV.6, DM-003|Edit at rf-qa.md:49-77 + specifically :70-77 adds DNSP partition protocol; 4-phase structure byte-stable|M|P0|
|83|COMP-003 (M5 scope c)|Update rf-qa-qualitative.md DNSP edit site (lines 70-80)|Add DNSP emission directive; preserve 7-phase structure; preserve anti-inflation rule at :766-775|rf-qa-qualitative.md|FR-CONV.6, DM-003|Edit at rf-qa-qualitative.md:70-80; DNSP edit appended; 7-phase structure byte-stable; anti-inflation rule unchanged|M|P0|
|84|COMP-006|Preserve rf-team-lead.md (UNMODIFIED — verification only)|Verify rf-team-lead.md:417 NO DRIFT; all-agents-fail escalation behavior preserved verbatim; FR-CONV.6 Negative Criterion enforcement|rf-team-lead.md|FR-CONV.6|`grep -n "max 3 cycles per phase" rf-team-lead.md` returns line 417; line content byte-equal to pre-merge baseline; CI gate prevents accidental modification|S|P0|
|85|NFR-CONV.10|Validate parallel-research invariant under DNSP emission|N partition agents spawn concurrently; on one agent escalation exhaust, N-1 partitions continue to completion; DNSP synthesised within-agent-instance NOT cross-cohort|rf-qa.md, rf-analyst.md|FR-CONV.6|Spawn-log inspection: timestamps overlap on N partitions; one-exhaust + N-1-continue verified; cross-cohort serialization → FAIL|M|P0|
|86|TEST-018|test_dnsp_twice_exhaust fixture|Twice-timeout partition fixture produces synthetic-dnsp finding with all 5 fixed fields (severity HIGH, source synthetic-dnsp, affected_range, evidence, recommendation)|rf-qa.md, rf-analyst.md|FR-CONV.6|Parse YAML; assert all 5 fixed fields populated; severity=HIGH; source="synthetic-dnsp"; recommendation verbatim|M|P0|
|87|TEST-019|test_dnsp_dedup_collapse fixture|Two identical-`dedup_key` synthetic findings collapse to one record with `found_n_times=2`|rf-qa.md|FR-CONV.6|Parse merged YAML; cardinality=1; `found_n_times=2`; identical dedup_key tuple|S|P0|
|88|TEST-020|test_dnsp_all_agents_fail_bypass fixture|Zero partitions succeeded → no synthetic emits; rf-team-lead.md:417 escalation activates|SKILL.md|FR-CONV.6|Execution log shows HALT path via rf-team-lead.md:417; no synthetic block in agent output; mutual-exclusivity verified|M|P0|
|89|TEST-021|test_dnsp_does_not_serialize_cohort fixture|On one partition's escalation exhaust, N-1 sibling partitions continue concurrently to completion (INV-021)|rf-qa.md, rf-analyst.md|FR-CONV.6, NFR-CONV.10|Spawn-log timing: N-1 partitions overlap exhausted partition's synthesis window; cohort does NOT serialize|M|P0|
|90|TEST-022|test_synthetic_dnsp_dedup_not_regression fixture|Synthetic finding same dedup_key cycles 1+2 (others shrinking) proceeds to cycle 3 — no regression halt|rf-task-builder.md|FR-CONV.5, FR-CONV.6|Execution log shows cycle 3 attempted; no regression halt fires; INV-012 composition verified|M|P0|
|91|TEST-023|test_hidden_input_guard fixture|Fixture-populated `.dev/tasks/done/` produces byte-identical structural output to empty `done/`|SKILL.md|NFR-CONV.3|Diff structural fields between (a) empty done/ and (b) populated done/ 10+ historical tasks ≥3 task_types runs; byte-identical|M|P0|
|92|TEST-024|test_sequencing_PR06_before_PR04 fixture|If PR-04 lands before PR-06 hypothetically, dynamic enumeration richens once catalogue activates|rf-qa.md, rf-qa-qualitative.md|FR-CONV.1, FR-CONV.3, INV-010|Structural assertion on enriched checklist; dynamic enumeration source detected|M|P0|
|93|TEST-025|test_invariant_preservation_NFR_6_through_10 composite fixture|All 5 invariants preserved per Negative Criteria; composite fixture exercising each invariant surface|All COMPs|all M2-M5 commits|All 5 invariants (self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research) PASS; NFR-CONV.6..10 fixtures all green|M|P0|
|94|MIG-006|Land FR-CONV.6 (PR-03 BASE) commit — M1.6|Single revertable commit; serial landing position 6th (final FR); rollback by reverting DNSP edit sites; existing rf-team-lead.md:417 handles zero-partitions-succeeded path; jointly revertable with FR-CONV.5 per §19.4|rf-qa.md, rf-analyst.md, rf-qa-qualitative.md, SKILL.md|MIG-005, all M5 FR-CONV.6 items|Single commit; `make verify-sync` PASS; all 6 FRs landed in serial order PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03|L|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`[HALT-MONOTONICITY]` halt-message string|Halt-signal sentinel (verbatim string, fixture-pinned)|Activated M5 (MIG-005)|M5|Fix-cycle next-cycle decision logic; CI fixture parsers|
|Regression halt-message string|Halt-signal sentinel (verbatim string, fixture-pinned)|Activated M5 (MIG-005)|M5|Fix-cycle next-cycle decision logic; CI fixture parsers|
|`source: "synthetic-dnsp"` literal sentinel|Grep-able tag in agent output stream (sentinel registry)|Activated M5 (MIG-006)|M5|Orchestrator gate-result merge; OPS-002 DNSP triage runbook|
|dedup_key composite tuple|Identity for within-cycle dedup-collapse + cross-cycle non-regression discrimination (registry key)|Activated M5 (MIG-006)|M5|FR-CONV.5 monotonicity check; INV-012 composition|
|all-agents-fail guard precedence|Mutually-exclusive escalation path (dispatch rule)|Preserved unchanged|M5|rf-team-lead.md:417 escalation; OPS-003 runbook|

### Milestone Dependencies — M5

- M4 (FR-CONV.3 + FR-CONV.4 landed; rf-qa-qualitative anti-inflation rule preserved)
- M2 (FR-CONV.1 landed; |F_n| count source from TB-Add catalogue verdicts)

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-005 Retry monotonicity halts legitimate slow-cycle correction|LOW|LOW|False halts on legitimate `|F|=5,4` shrink; legitimate fix work aborted|Strict-shrink threshold preserved (any forward motion continues); X-003 REJECTED documented; TEST-017 guards behavior|rf-task-builder maintainer|
|2|K-006 Synthetic-dnsp findings mask real issues|LOW|LOW|Real partition findings hidden by synthetic finding|HIGH severity ensures gate-level visibility; synthetic emits ALONGSIDE real findings (not in place of); dedup-key prevents over-emission; weekly emission-count metric inspection (OPS-002)|rf-qa maintainer|
|3|FR-CONV.6 short-circuits rf-team-lead.md:417 escalation|HIGH|LOW|All-agents-fail guard violated; existing 3-cycle escalation bypassed by synthetic emit on zero-success path|FR-CONV.6 Negative Criterion + COMP-006 verification + TEST-020 bypass fixture; mutual-exclusivity dispatch rule documented|rf-qa maintainer + rf-team-lead maintainer|
|4|Halt-message verbatim string drift|MED|LOW|Fixtures parse FAIL; CI suite breaks downstream of any string change|Verbatim strings locked at MIG-005; CI fixture parsers grep exact byte-equal; documented as wire-ABI in TDD §8.4 governance|rf-task-builder maintainer|
|5|INV-012 cross-cycle regression false-positive on synthetic-dnsp|MED|LOW|Identical dedup-key across cycles incorrectly flagged as regression; loop halts erroneously|TEST-022 fixture guards behavior; dedup-key composition rule documented in DM-003 + API-004; prior-cycle verdict was FAIL not PASS|rf-task-builder maintainer|

## M6: Hardening, Audit, NFR Measurement & GA

**Objective:** Validate all 6 FRs in composition; perform K-003 audit on first 5 real rf-qa-qualitative runs; measure NFR-CONV.4 token-cost ratio on 5 representative BUILD_REQUESTs; instrument offline metrics per §14.2; execute runbooks per §25.1; clean up degradation fallback paths post-GA + 30 days; reach v3.9 GA. | **Duration:** Weeks 9-20 (2026-07-10 → 2026-09-30) | **Entry:** M5 exit criteria met; all 6 FRs landed in serial order; `make verify-sync` PASS after each FR commit | **Exit:** Q-DM-1 closed; K-003 audit PASS on first 5 real runs; NFR-CONV.4 ratio ≤1.10 on 5 representative BUILD_REQUESTs; NFR-CONV.1 determinism spot-check PASS; v3.9 release tag created; all 6 logical feature flags promoted to default-enabled with fallback paths removed at GA+30 days

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|95|NFR-CONV.4|Measure token-cost ratio on 5 representative BUILD_REQUESTs|Post-merge measurement; sample Quick / Standard / Deep tier coverage; compute ratio post-merge / pre-merge per equivalent BUILD_REQUEST; instrument with counter histogram|All COMPs|MIG-006|Sample 5 representative BUILD_REQUESTs covering Quick/Standard/Deep tiers; pre-merge baseline + post-merge total token counts recorded; ratio ≤1.10 (NFR-CONV.4 ceiling) measured per-BUILD_REQUEST; histogram emitted to `docs/generated/nfr-conv-4-token-ratio.json`; if exceeded → K-010 contingency activate FR-CONV.3 verdict-table summarisation|M|P0|
|96|NFR-CONV-R1|Validate single-pass gate PASS rate baseline|≥80% of representative BUILD_REQUESTs PASS task-integrity gate on first cycle|All COMPs|MIG-006|Run 5 representative BUILD_REQUESTs; count first-cycle PASS verdicts; fraction ≥0.80; trend post-merge ↑ expected|S|P0|
|97|NFR-CONV.1 spot-check|Re-run determinism spot-check on identical BUILD_REQUEST|TB-Add-1..8 PASS/FAIL verdicts, synthetic-dnsp 5 fixed fields + dedup-key, axis column values, Items Reviewed table structure byte-identical across two runs|rf-qa.md, rf-qa-qualitative.md|MIG-006|Re-run task-builder on identical BUILD_REQUEST twice; diff rf-qa A.10 verdict table + rf-qa-qualitative Items Reviewed table; structural fields byte-equal|S|P0|
|98|OPS-001|Execute K-003 audit runbook on first 5 rf-qa-qualitative runs|First 5 real runs post-FR-CONV.3; verify each contains `## Self-Audit` with ≥1 independent semantic check beyond inherited PASS; alert at <100% coverage|rf-qa-qualitative.md|MIG-003 + 5 real runs|Read `.dev/tasks/to-do/TASK-*/reviews/qa-qualitative-review.md`; grep `## Self-Audit`; verify ≥1 semantic check; on FAIL → disable passthrough flag (§19.2); response time 4 business hours; alert threshold <100% on first 5 runs|M|P0|
|99|OPS-002|Operationalise DNSP triage runbook|Counter `synthetic-dnsp emission count` instrumented; alert threshold >0 in production → human review; ≥3 distinct dedup-keys in a week escalates to Engineering|rf-qa.md, rf-analyst.md|MIG-006|grep `"source: synthetic-dnsp"` across rf-analyst / rf-qa / rf-qa-qualitative outputs; counter emits to `docs/generated/metrics/synthetic-dnsp-count.json`; alert config records >0 threshold; escalation path documented|S|P0|
|100|OPS-003|Operationalise all-partitions-exhaust HALT runbook|No DNSP emitted; rf-team-lead.md:417 escalation activates; user resolves unresolved findings before re-run|rf-team-lead.md|MIG-006|Execution log inspection runbook documented; mutual-exclusivity verification; rf-team-lead maintainer escalation path on misfire|S|P0|
|101|OPS-004|Operationalise monotonicity-halt rate alert (counter + threshold)|Counter `[HALT-MONOTONICITY] count`; alert threshold >50% of fix-cycle batches; instrumented as offline metric|rf-task-builder.md|MIG-006|grep `[HALT-MONOTONICITY]` in fix-loop execution logs; counter emits to `docs/generated/metrics/halt-monotonicity-count.json`; alert config records >50% threshold per §14.2; OPEN-INV-006 calibration trigger documented|S|P0|
|102|OPS-005|Operationalise regression-halt rate alert (counter + threshold)|Counter `regression-halt count`; alert threshold >20% of fix-cycle batches; instrumented as offline metric|rf-task-builder.md|MIG-006|grep `Regression detected on Item` in fix-loop execution logs; counter emits to `docs/generated/metrics/regression-halt-count.json`; alert config records >20% threshold per §14.2|S|P0|
|103|OPS-006|Operationalise `make verify-sync` FAIL runbook|Per-commit gate; threshold any FAIL blocks commit (100% PASS rate required)|All COMPs|GOV-3|`make sync-dev && make verify-sync` runs in CI; on FAIL block commit; per-commit author re-syncs from src/superclaude; K-009 contingency documented|S|P0|
|104|OPS-007|Operationalise INV-018 layout-change detection runbook|Detect `.dev/tasks/` schema change pre-/post-merge; K-008 portfolio-wide re-integration path|All COMPs|GOV-2|`.dev/tasks/` directory schema diff captured; if change detected → re-integration commit covering all 6 FRs per §19.4 matrix|S|P0|
|105|MIG-007|Execute post-merge audit window M1.7 (1-2 weeks)|K-003 + NFR-CONV.4 measurement gating; advisory rules promoted pending Phase-2 calibration; fallback paths removed at GA+30 days|All COMPs|MIG-006 + 5 real runs|Audit window 1-2 weeks post-MIG-006; K-003 + NFR-CONV.4 PASS criteria evaluated; release criteria checklist §24.2 complete; rollback decision recorded per §19.4 if any FAIL|L|P0|
|106|NFR-CONV.8|Validate persistent-`.dev/tasks/`-artifact invariant preservation|`.dev/tasks/<task-id>/` layout diff pre-merge vs post-merge; zero structural changes (no new mandatory subdirectory, no rename, no naming-pattern change)|All COMPs|MIG-006|Diff `.dev/tasks/<task-id>/` layout pre-/post-merge; PASS only on zero structural changes; SP-33 stability commitment verified|S|P0|
|107|RR-K-001|Risk Register monitoring — K-001 TB-Add false positives|Track TB-Add false-positive rate per check; contingency disable specific TB-Add line|rf-qa.md|MIG-007|False-positive rate <5% per TB-Add; weekly inspection during audit window|S|P1|
|108|RR-K-010|Risk Register monitoring — K-010 NFR-CONV.4 token ceiling|Track token-cost ratio per release; contingency K-010 summarise FR-CONV.3 verdict table if exceeded|All COMPs|NFR-CONV.4 measurement|Ratio ≤1.10 sustained; on FAIL → activate K-010 contingency; FR-CONV.3 verdict-table summarisation documented as fallback|S|P1|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`synthetic-dnsp emission count` counter|Offline metric emitter (counter histogram)|Activated M6 (OPS-002)|M6|DNSP triage runbook; on-call alerting|
|`[HALT-MONOTONICITY] count` counter|Offline metric emitter (counter histogram)|Activated M6 (OPS-004)|M6|Monotonicity-halt rate runbook; upstream BUILD_REQUEST defect alerting|
|`regression-halt count` counter|Offline metric emitter (counter histogram)|Activated M6 (OPS-005)|M6|Regression-halt rate runbook; fix-cycle quality alerting|
|`Self-Audit coverage` gauge|Offline metric emitter (fraction gauge)|Activated M6 (OPS-001)|M6|K-003 audit-target gate; QA Lead inspection|
|`make verify-sync PASS rate` counter|CI step + commit hook output|Activated M1 (GOV-3); enforced through M6|M6|Per-commit author response; release checklist|
|`docs/generated/metrics/` artifact directory|Pipeline output directory (artifact sink)|Activated M6|M6|All counter/gauge metric files; post-merge audit consumption|

### Milestone Dependencies — M6

- M5 (all 6 FRs landed in serial order; DNSP emission + halt signals operational)
- M4 (K-003 audit-target activated at MIG-003; needs first 5 real runs to materialise)
- M2-M5 (cumulative invariant preservation across NFR-CONV.6..10)

### Open Questions — M6

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-TOKEN|NFR-CONV.4 token-ceiling empirical measurement — verify ≤1.10 ratio on 5 representative BUILD_REQUESTs|If exceeded → K-010 contingency (summarise FR-CONV.3 verdict table rather than emit verbatim); blocks GA until resolved|Engineering Lead|Post-MIG-006 + measurement window|
|2|OPEN-X-002|PR-04 anti-inflation operational test — verify first 5 rf-qa-qualitative runs show no inflation (audit carried from M4)|If inflation detected → §19.4 rollback path; FR-CONV.3 reverted; blocks GA|QA Lead|Post-MIG-003 + first 5 real runs|
|3|OPEN-PR05|`.dev/tasks/done/` count + task_type diversity threshold check for PR-05 Phase-2 re-evaluation eligibility|Determines Phase-2 release timing post-v3.9 GA; not a GA blocker; documented in KNOWLEDGE.md|Engineering Lead|Per-release inspection|
|4|OPEN-INV-006|Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track)|TB-Add-2 stays `[ADVISORY]` until calibrated; Phase-2 with PR-05|Engineering|Phase-2|
|5|OPEN-INV-017|Historical-file staleness check for PR-05 advisory citations — academic given PR-05 Phase-2 deferral|Out-of-band; resolve when PR-05 re-evaluated|Engineering|When PR-05 re-evaluated|

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-003 inflation detected in audit|MED|LOW|Audit shows item VERIFIED solely from inherited verdict; FR-CONV.3 rollback required; v3.9 GA delayed|INV-019 Self-Audit mandate; OPS-001 runbook + 4-hour response time; §19.4 rollback path documented|QA Lead|
|2|K-010 NFR-CONV.4 token ceiling exceeded by >10%|LOW|LOW|GA delayed pending K-010 contingency activation|Empirical measurement on 5 representative BUILD_REQUESTs; per-FR profiling identifies largest contributor; K-010 contingency (FR-CONV.3 verdict-table summarisation) documented|Engineering Lead|
|3|`[HALT-MONOTONICITY]` >50% rate post-merge|MED|LOW|Indicates upstream BUILD_REQUEST defect or systemic agent issue|OPS-004 runbook; sample 3 halt events; inspect BUILD_REQUESTs; TB-Add-2 calibration (OPEN-INV-006) considered|rf-task-builder maintainer|
|4|regression-halt >20% rate post-merge|MED|LOW|Fix-cycle introducing new defects|OPS-005 runbook; tighten fix-cycle prompts; X-003 slow-convergence threshold REJECTED documented|Engineering Lead|
|5|K-008 INV-018 layout change post-merge|HIGH|LOW|Portfolio-wide re-integration|OPS-007 runbook; SP-33 stability commitment; re-integration commit covering all 6 FRs per §19.4|Engineering Lead + orchestrator|
|6|K-009 `make verify-sync` FAIL post-FR-merge|MED|LOW|Sync verification fails between src/superclaude and .claude/|OPS-006 runbook; re-run `make sync-dev`; revert `.claude/` direct edit; re-run from src/superclaude (K-009 contingency)|Per-commit author|
|7|GA blocked by Q-DM-1 unresolved schema migration impact|HIGH|LOW|If option (a) net-new schema migration chosen and not fully discharged by GA, FR-CONV.1 enforcement incomplete|Engineering Lead decision recorded at M1 GOV-1; downstream impact propagated through DM-004; release-criteria checklist §24.2 verifies discharge|Engineering Lead|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|None — NFR-CONV.5 forbids new external dependencies, new MCP servers, new libraries|All|N/A|N/A|

### Infrastructure Requirements

- None — NFR-CONV.5 forbids new infrastructure. No database, no message queue, no compute allocation, no deployment target.
- Local development via UV (`uv run pytest`); CI via GitHub Actions invoking `make test`.
- `make verify-sync` enforced in CI as pre-commit gate (A-001 sync discipline).
- `docs/generated/metrics/` artifact directory (created at M6; sink for offline counter/gauge metric files).

### Internal Dependencies

- `release-spec.md v1.0.0` — defines §4.6 landing order, §9 SP-10 rollback matrix, §8.3 audit rows.
- `conflict-register.md` — 5 CASE-D rows (PR-01, PR-02, PR-06, PR-07, PR-05-deferred).
- `invariant-probe.md` — INV-002, INV-010, INV-012, INV-015, INV-019, INV-021 Round-2.5 findings.
- `FINAL-REPORT.md` §6.3 — asymmetric finding (5 ADOPT-grade qualities, inverse direction).
- `FINAL-REPORT.md` §6.2 F2/F4 — 21-retry oscillation + hidden-input over-engineering empirical motivation.
- `rf-team-lead.md:417` — 3-fix-cycle escalation (VERIFIED NO-DRIFT 2026-05-14).
- `rf-qa.md:141-142` — zero-trust verdict (verbatim PASS/FAIL definitions).
- `task-builder/SKILL.md:~1452-1457` — per-item schema (⚠ SC-1 CRITICAL DRIFT FLAGGED — Q-DM-1; resolution at M1).
- `.dev/tasks/` directory layout (INV-018, SP-33 stability commitment).
- `make sync-dev` / `make verify-sync` pipeline (A-001 discipline tooling).

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|K-001|TB-Add false positives waste fix-cycles|M2, M6|LOW|LOW|Each TB-Add cites source-check-ID; TB-Add-2 `[ADVISORY]`; individually revertable per append line|rf-qa maintainer|
|K-002|Execution Context header drift (header vs items)|M3|LOW|LOW|TB-Add-7 cross-validates each gate; on drift gate fails; degraded References-only fallback|task-builder maintainer|
|K-003|PR-04 passthrough causes inflation despite anti-inflation rule|M4, M6|LOW|MED|INV-019 Self-Audit mandate; K-003 audit-target on first 5 real runs; rollback path; FR-CONV.3 reverted on FAIL|QA Lead|
|K-004|5-axis annotation ambiguity over-flags items|M4|LOW|LOW|Axes annotation-only; 15-item checklist still runs; severity floor preserved; `drift-axis-inactive` annotation; audit axis distribution post-merge|rf-qa-qualitative maintainer|
|K-005|Retry monotonicity halts legitimate slow-cycle correction|M5|LOW|LOW|Strict-shrink threshold; X-003 REJECTED; TEST-017 guards behavior|rf-task-builder maintainer|
|K-006|Synthetic-dnsp findings mask real issues|M5, M6|LOW|LOW|HIGH severity ensures visibility; synthetic emits alongside real; dedup-key prevents over-emission|rf-qa maintainer|
|K-007|PR-04 + PR-06 sequencing inversion|M2, M3, M4|LOW|MED|Serial enforcement in release-spec §4.6 + GOV-4; INV-010 dynamic enumeration auto-richens as ultimate fallback|Engineering Lead|
|K-008|INV-018 `.dev/tasks/` directory layout changes invalidate proposals|M1, M2, M3, M4, M5, M6|LOW|HIGH|SP-33 stability commitment; OPS-007 runbook; re-integration commit covering all 6 FRs per §19.4|Engineering Lead + orchestrator|
|K-009|Sync-discipline violated; `.claude/` edited directly without `make verify-sync`|M1, M2, M3, M4, M5, M6|LOW|MED|CLAUDE.md mandates workflow; `make verify-sync` MUST pass pre-commit; OPS-006 runbook|Per-commit author|
|K-010|Token ceiling NFR-CONV.4 exceeded by >10%|M6|LOW|LOW|Empirical post-merge measurement on 5 representative BUILD_REQUESTs; per-FR profiling; FR-CONV.3 verdict-table summarisation contingency|Engineering Lead|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Single-pass gate PASS rate (baseline)|Fraction of representative BUILD_REQUESTs passing task-integrity gate on first cycle|≥80%|Run 5 representative BUILD_REQUESTs; count first-cycle PASS verdicts|M6|
|Placeholder-defect detection rate|TB-Add-1 firings on placeholder-injected fixtures|100%|`test_placeholder_tb_add_1` synthetic fixture suite|M2|
|DAG-cycle detection rate|TB-Add-4 firings on circular-dependency fixtures|100%|`test_dag_cycle_tb_add_4` synthetic fixture suite|M2|
|Self-Audit coverage post-FR-CONV.3|Fraction of rf-qa-qualitative runs with `## Self-Audit` containing ≥1 semantic check beyond inherited PASS|100% on first 5 real runs (K-003 audit)|Read `.dev/tasks/to-do/TASK-*/reviews/qa-qualitative-review.md`; grep + content inspection|M6 (OPS-001)|
|`[HALT-MONOTONICITY]` emission rate|Counter as fraction of fix-cycle batches emitting halt|<10% steady-state; >50% alerts upstream defect|grep `[HALT-MONOTONICITY]` in fix-loop logs; counter histogram|M6 (OPS-004)|
|Synthetic-dnsp emission count|Counter of HIGH-severity synthetic findings|≥1 on twice-exhaust fixture; 0 on healthy run; >0 in production triggers human review|grep `"source: synthetic-dnsp"` across agent outputs; counter histogram|M6 (OPS-002)|
|Token-cost ratio (post-merge / pre-merge)|NFR-CONV.4 empirical|≤1.10|Token count comparison on 5 representative BUILD_REQUESTs across Quick/Standard/Deep tiers|M6 (NFR-CONV.4)|
|Fix-cycle convergence rate|Fraction of fix-cycle sequences converging to gate PASS rather than hitting per-gate cap or monotonicity halt|≥75% baseline; trend ↑ post-merge|Per-fix-cycle log inspection across audit window|M6|
|Regression-halt emission rate|Counter as fraction of fix-cycle batches emitting regression halt|<5% steady-state; >20% alerts fix-cycle defect|grep `Regression detected on Item` in fix-loop logs; counter histogram|M6 (OPS-005)|
|`make verify-sync` PASS rate|Counter — fraction of commits passing sync verification|100% (any FAIL blocks commit)|CI step + commit hook output|M1-M6 (GOV-3, OPS-006)|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Port direction|Intent-port (adapt sc-tasklist intent, not implementation)|Bulk-implementation-port (REJECTED — would re-introduce v3.8 over-engineering pattern per FINAL-REPORT §6.3)|FINAL-REPORT §6.3 asymmetric finding: cross-paradigm merger between execution-context (rf) and generation-context (sc) requires intent-port; only one of 5 mechanisms is a literal source|
|Governance model|Strictly-additive (A-002)|Single-FR mega-merge (REJECTED — eliminates per-FR rollback granularity); selective replacement (REJECTED — breaks A-002)|Per-FR rollback granularity preserves operability under failure; low blast radius; each FR is single revertable commit|
|Check classification (FR-CONV.1)|Per-check (CB-3) — 8 unique TB-Adds|Bulk-port all 17/20 sc-tasklist Stage-6 checks (REJECTED per CB-3)|11 of 20 sc-tasklist checks are bundle-specific (phase-file naming, R-### roadmap traceability, checkpoint emission); 3 are not-relevant; only 8 intent-portable|
|Conflict-resolution rule|G6 four-case (CASE A/B/C/D per proposal)|Implicit precedence rules (REJECTED — opaque, non-auditable)|Makes conflict resolution auditable: PR-04 CASE-B (silent) vs PR-06 CASE-D (conflict-register row required); 5 CASE-D rows + 2 CASE-B (correctly absent)|
|Determinism scope|Structural fields byte-deterministic; research-prose excluded|Full byte-determinism (REJECTED — impossible with LLM); zero determinism (REJECTED — gate verdicts must be reliable)|LLM determinism achievable on structured output but not on free prose; gate verdicts reliable enough to drive PASS/FAIL while preserving research flexibility|
|Anti-inflation enforcement|`rf-qa-qualitative.md:766-775` byte-stable; FR-CONV.3 adds RELIANCE channel layered on top|Strict mechanical re-check (REJECTED — wastes fix cycles); pure passthrough (REJECTED — rubber-stamp risk)|INV-019 Self-Audit makes anti-inflation auditable; K-003 audit on first 5 runs is the operational guarantee|
|All-agents-fail guard|`rf-team-lead.md:417` NO DRIFT; DNSP only on partial-failure|DNSP always on any exhaust (REJECTED — would mask total-failure); no DNSP at all (REJECTED — leaves partial-failure silent)|Preserves established multi-fix-cycle escalation; DNSP adds coverage for partial-failure without short-circuiting the "stop the line" HALT|
|FR-CONV.5 ↔ FR-CONV.6 composition|Synthetic-dnsp counts as `|F_n|` failure; identical dedup-key across cycles is dedup NOT regression (INV-012)|Pure cardinality counting (REJECTED — produces false regressions); cross-cycle ignore of synthetic findings (REJECTED — would mask repeated defects)|Enables monotonicity guard to compose cleanly with DNSP emission without false-regression halts; set-with-identity semantics|
|Landing order|PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 strict serial|Parallel landing of independent FRs (REJECTED — dependency chain real)|FR-CONV.2 depends on FR-CONV.1; FR-CONV.3 depends on FR-CONV.1 + FR-CONV.2; FR-CONV.4 depends on FR-CONV.3; FR-CONV.5 + FR-CONV.6 share INV-012 contract; K-007 specifically mitigated by serial enforcement|
|PR-05 (Tier-History Advisory)|DEFERRED to Phase-2|Ship in Phase-1 with advisory framing (REJECTED — hidden-input determinism risk per FINAL-REPORT §6.2 F4)|Reads `.dev/tasks/done/` historical files — behavior-modifying hidden input violating NFR-CONV.3; Phase-2 trigger at `.dev/tasks/done/TASK-RF-*` ≥10 with ≥3 task_types|

## Timeline Estimates

|Milestone|Duration|Start|End|TDD Milestone Mapping|Key Milestones|
|---|---|---|---|---|---|
|M1 Foundation|1 week|2026-05-15 (Week 1)|2026-05-21 (Week 1)|TDD Stage 0 Pre-merge + Design Complete target|Q-DM-1 closed; DM-001..005 + API-001..005 locked; conflict-register validated|
|M2 FR-CONV.1 PR-06|2 weeks|2026-05-22 (Week 2)|2026-06-04 (Week 3)|TDD M1.1|TB-Add-1..8 catalogue lands rf-qa.md + SKILL.md; TEST-001..003 PASS; MIG-001 commit|
|M3 FR-CONV.2 PR-01|1 week|2026-06-05 (Week 4)|2026-06-11 (Week 4)|TDD M1.2|`## Execution Context` header in MDTM; TEST-004..006 PASS; MIG-002 commit|
|M4 FR-CONV.3+FR-CONV.4 PR-04+PR-07|2 weeks|2026-06-12 (Week 5)|2026-06-25 (Week 6)|TDD M1.3 + M1.4|Inherited Structural Verdict block + Five Adversarial Axes overlay; TEST-007..014 PASS; MIG-003 + MIG-004 commits|
|M5 FR-CONV.5+FR-CONV.6 PR-02+PR-03|2 weeks|2026-06-26 (Week 7)|2026-07-09 (Week 8)|TDD M1.5 + M1.6|Monotonicity + regression halt-conditions + synthetic-dnsp 7-field finding; TEST-015..025 PASS; MIG-005 + MIG-006 commits|
|M6 Hardening + Audit + NFR Measurement + GA|12 weeks|2026-07-10 (Week 9)|2026-09-30 (Week 20)|TDD M1.7 + Stage 7 Audit Window + Stage 8 GA+30d|K-003 audit PASS; NFR-CONV.4 ≤1.10; all OPS-001..007 runbooks operational; v3.9 GA at end Q3 2026|

**Total estimated duration:** 20 weeks (2026-05-15 → 2026-09-30). Aligns with TDD §23.1 v3.9 GA target of 2026-Q3 (end Q3 = 2026-09-30). Critical path runs through Q-DM-1 resolution (M1) → strict-serial FR landings (M2-M5) → post-merge audit window + NFR measurement (M6). If Q-DM-1 slips beyond 2026-05-21, M2 start date shifts day-for-day and GA target compresses M6 audit window; per Timeline Anchoring Rule, any overshoot beyond 2026-09-30 is flagged as a blocking Open Question (see OPEN-TOKEN / OPEN-X-002 in M6 if audit findings extend the window).
