---
spec_source: "TDD_TASK_BUILDER_CONVERGENCE.compressed.md"
complexity_score: 0.7
complexity_class: HIGH
primary_persona: architect
---

# Task-Builder Convergence v3.9 — Project Roadmap

## Executive Summary

This roadmap operationalises the six functional requirements (FR-CONV.1..6) of the Task-Builder Convergence v3.9 release as a strictly serial, per-FR-revertable delivery sequence (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03), plus a post-merge audit-and-measurement milestone. The release is intent-port-only: it adopts five proven sc-tasklist rigor mechanisms into the task-builder skill without copying any code, and preserves five load-bearing invariants (self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research) via dedicated synthetic fixtures (NFR-CONV.6..10).

**Business Impact:** Closes three structural-rigor gaps in task-builder's gate topology (no task-level executor-readability summary, no structural gate checks, implicit rubber-stamp passthrough between rf-qa and rf-qa-qualitative) and bounds an empirically-observed retry-oscillation pattern (FINAL-REPORT §6.2 F2: 21-retry / 18-batch loop) at a hard token-cost ceiling of ≤1.10 ratio per equivalent BUILD_REQUEST (NFR-CONV.4). All gate additions are local checks using only existing tools (Read, Grep, Glob, Bash); no new external dependencies, no synchronous network calls, no infrastructure scaling (NFR-CONV.5).

**Complexity:** HIGH (0.7) — driven by ~22 distinct edit points across 5 source files (SKILL.md 1709 lines + 4 rf-* agents totalling ~2067 lines), strict 6-step serial sequencing with no permitted parallelism, and three mutual-composition pairings (FR-CONV.5 ↔ FR-CONV.6 dedup-key, FR-CONV.3 ↔ FR-CONV.1 dynamic enumeration INV-010, FR-CONV.4 ↔ FR-CONV.3 inherited-PASS composition INV-013). Mitigating factors: strictly-additive A-002 governance (no rename / renumber / removal of existing items), per-FR rollback granularity with explicit co-revert matrix, and zero new external dependencies.

**Critical path:** Q-DM-1 schema-contradiction resolution (Engineering Lead) → M1 (TB-Add-1..8 + 3-surface mirror) → M2 (Execution Context header) → M3 (Inherited Structural Verdict + Self-Audit) → M4 (Five Adversarial Axes overlay) → M5 (monotonicity + regression halts) → M6 (synthetic-dnsp on partition exhaust) → M7 (K-003 audit window + NFR-CONV.4 token-cost measurement on 5 representative BUILD_REQUESTs). `make verify-sync` PASS is the per-FR landing gate; failure blocks the next milestone (K-009).

**Key architectural decisions:**

- Intent-port over implementation-port — adapt the *intent* of five sc-tasklist mechanisms re-expressed in task-builder's idiom; only one of the five is a literal source-line lift.
- Strictly-additive A-002 governance with per-FR rollback granularity, governed by a co-revert dependency matrix (FR-CONV.5 ↔ FR-CONV.6 jointly revertable; FR-CONV.1 ↔ FR-CONV.3 INV-010 enumeration dependency).
- Determinism scope split (NFR-CONV.1 byte-identical structural fields; NFR-CONV.2 LLM-driven prose nondeterminism acceptable) — gate verdicts driven by structured output, semantic prose intentionally excluded from determinism scope.
- Anti-inflation rule at `rf-qa-qualitative.md:766-775` treated as absolute — FR-CONV.3 inherited verdict is a deliberately-scoped RELIANCE channel for structural items only, gated by INV-019 Self-Audit obligation and the K-003 first-5-runs audit.

**Open risks requiring resolution before M1:**

- Q-DM-1 — PRD §25.4 declares per-item schema `{Description, Context, Acceptance, Confidence, Verification}` "preserved unchanged" at `SKILL.md:1452-1457`, but current source holds `{Context, Action, Output, Verification, Completion gate}`. Engineering Lead decision required before TB-Add-8 can be authored against a stable baseline (CRITICAL blocker).

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|FR-CONV.1 / PR-06 — Structural Gate Additions (TB-Add-1..8)|Foundation|P0|M|Q-DM-1 resolved|23|Medium|
|M2|FR-CONV.2 / PR-01 — Execution Context Header|Foundation|P0|S|M1|17|Low|
|M3|FR-CONV.3 / PR-04 — Inherited Structural Verdict + Self-Audit|Core Logic|P0|M|M2; TB-Add catalogue (INV-010)|21|Medium|
|M4|FR-CONV.4 / PR-07 — Five Adversarial Axes Overlay|Core Logic|P0|S|M3|20|Low|
|M5|FR-CONV.5 / PR-02 — Retry Monotonicity + Regression Halts|Integration|P0|M|M4; FR-CONV.6 dedup-key shape|21|Low|
|M6|FR-CONV.6 / PR-03 — Synthetic DNSP on Partition Exhaust|Integration|P0|L|M5|29|Low|
|M7|Production Readiness — K-003 Audit + NFR-CONV.4 Measurement + GA|Hardening|P0|M|All FRs landed|20|Medium|

## Dependency Graph

```
M1 (FR-CONV.1, TB-Add-1..8)
  └─► M2 (FR-CONV.2, Execution Context header — depends on TB-Add-7/8 live)
        └─► M3 (FR-CONV.3, Inherited Verdict — depends on TB-Add catalogue INV-010 + TB-Add-7 cross-validation)
              └─► M4 (FR-CONV.4, Five Adversarial Axes — depends on FR-CONV.3 inherited-PASS composition INV-013)
                    └─► M5 (FR-CONV.5, Monotonicity halts — depends on FR-CONV.1 |F_n| count; mutual-shape coupling with M6)
                          └─► M6 (FR-CONV.6, Synthetic DNSP — emits the dedup-key shape M5 consumes)
                                └─► M7 (K-003 audit window + NFR-CONV.4 measurement → v3.9 GA)
```

## M1: FR-CONV.1 / PR-06 — Structural Gate Additions (TB-Add-1..8)

**Objective:** Append 8 structural checks (TB-Add-1..8) to rf-qa task-integrity gate, mirrored across all three definition surfaces (rf-qa.md 20-item checklist, SKILL.md A.10 9-item block, SKILL.md 15-item validation block); preserve zero-trust QA invariant; resolve INV-015 evidence-bound-item probe via TB-Add-8. | **Duration:** 2 weeks (2026-05-15 → 2026-05-29) | **Entry:** Q-DM-1 Engineering Lead decision landed; `make verify-sync` clean baseline; design approval. | **Exit:** TB-Add-1/3/4/5/6/7/8 fire distinct item-ID-naming errors and block gate on violation; TB-Add-2 emits `[ADVISORY]` and does not block; all 6 M1 fixtures PASS; `make verify-sync` PASS; no existing rf-qa check renamed/renumbered/removed.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.1|Append TB-Add-1..8 to rf-qa task-integrity gate|Add 8 strictly-additive structural checks to rf-qa A.10 mirrored across three definition surfaces; preserve zero-trust QA invariant (CASE-D PR-06)|rf-qa.md; SKILL.md|Q-DM-1|TB-Add-1/3/4/5/6/7/8 emit item-ID-naming error and block gate on violation; TB-Add-2 emits `[ADVISORY]` and does NOT block; no existing check renamed/renumbered/removed; no bundle-specific `/sc:tasklist` checks introduced|M|P0|
|2|TB-Add-1|Placeholder scan check (Hard, blocking)|Detect "TBD"/"TODO"/title-only checklist items; emits item-ID-naming error on violation|rf-qa.md|FR-CONV.1|Fixture with placeholder item triggers TB-Add-1 error; gate verdict FAIL; check cites source-check-ID|S|P0|
|3|TB-Add-2|Item-count bounds check (ADVISORY only)|Item-count bounds ≥3 / ≤40-track / ≤50-single-track; emits `[ADVISORY]` prefix and does NOT block gate (pending OPEN-INV-006 calibration)|rf-qa.md|FR-CONV.1|Out-of-bounds fixture emits `[ADVISORY]` message; gate verdict NOT affected; documented as advisory until Phase-2 calibration|S|P0|
|4|TB-Add-3|Clarification-adjacency check (Hard, blocking)|Detect items requiring clarification not adjacent to their resolving context; blocks gate on violation|rf-qa.md|FR-CONV.1|Non-adjacent clarification fixture FAILs gate; item-ID named in error message|S|P0|
|5|TB-Add-4|Circular-dependency DAG check (Hard, blocking)|Detect circular intra-/inter-phase dependencies; blocks gate on violation|rf-qa.md|FR-CONV.1|DAG-cycle fixture FAILs gate with TB-Add-4 emission; 100% detection rate on synthetic cycles|S|P0|
|6|TB-Add-5|Granularity / XL-has-subtasks check (Hard, blocking)|Detect XL-effort items lacking subtask decomposition; blocks gate on violation|rf-qa.md|FR-CONV.1|XL-without-subtasks fixture FAILs gate; item-ID identified|S|P0|
|7|TB-Add-6|Confidence / Verification format consistency check (Hard, blocking)|Validate per-item Confidence field uses HIGH/MEDIUM/LOW enum + rationale; Verification field is command/inspection/test|rf-qa.md|FR-CONV.1; Q-DM-1|Malformed Confidence or Verification fixture FAILs gate; format errors named|S|P0|
|8|TB-Add-7|Execution-Context source-areas cross-validation (Hard, blocking)|Validate each Source areas entry from Execution Context header reappears in ≥1 per-item Context field; blocks on drift|rf-qa.md|FR-CONV.1; FR-CONV.2|Header source-area absent from items FAILs gate; degraded References-only header tolerated|S|P0|
|9|TB-Add-8|Per-item Context citation check (Hard, blocking; resolves INV-015)|Validate per-item Context field has ≥1 file:line citation OR justified-absence comment|rf-qa.md|FR-CONV.1; Q-DM-1|Bare `Context: src/foo` (no `:N`) FAILs; `Context: src/foo:42` PASSES; `Context: <none — pure refactor> [justified-absence]` PASSES|S|P0|
|10|COMP-003|rf-qa agent modification (4-phase QA agent)|Modify rf-qa.md at task-integrity phase to host TB-Add-1..8 checklist additions; preserve PASS/FAIL definitions verbatim at rf-qa.md:141-142|rf-qa.md|FR-CONV.1|TB-Add-1..8 appear in rf-qa.md:268-287 region; zero-trust verdict definitions byte-identical pre/post; 4 QA phases unchanged|S|P0|
|11|COMP-001|task-builder SKILL.md A.10 mirror (9-item block)|Mirror TB-Add-1..8 into SKILL.md A.10 9-item block (~lines 898-906)|SKILL.md|FR-CONV.1|`grep -nE "TB-Add-[1-8]"` returns ≥1 hit per ID in SKILL.md:~898-906|S|P0|
|12|COMP-001|task-builder SKILL.md 15-item validation block mirror|Mirror TB-Add-1..8 into SKILL.md 15-item validation block (~lines 1491-1507)|SKILL.md|FR-CONV.1|`grep -nE "TB-Add-[1-8]"` returns ≥1 hit per ID in SKILL.md:~1491-1507|S|P0|
|13|TEST-001|test_placeholder_tb_add_1|Synthetic fixture asserting TB-Add-1 fires on "TBD"/"TODO"/title-only items|tests|TB-Add-1|TB-Add-1 emits item-ID-naming error; gate FAILs; assertion via grep on gate report|S|P0|
|14|TEST-002|test_dag_cycle_tb_add_4|Synthetic fixture asserting TB-Add-4 fires on circular dependency|tests|TB-Add-4|TB-Add-4 emits; gate FAILs; 100% detection rate on cycle fixture|S|P0|
|15|TEST-003|test_evidence_bound_tb_add_8|Three-fixture triple asserting TB-Add-8 behavior on (a) bare path (FAIL), (b) file:line (PASS), (c) justified-absence (PASS)|tests|TB-Add-8|All three sub-fixtures behave per spec; resolves INV-015 probe|S|P0|
|16|MIG-001|M1.1 PR-06 landing migration|Strictly-additive append commits; per-line revertable; `make verify-sync` PASS gate|src/|FR-CONV.1|Single commit lands TB-Add-1..8 across 3 surfaces; revert path (revert specific TB-Add line OR full commit) documented|S|P0|
|17|NFR-CONV.1|Structural-field determinism instrumentation (M1 scope)|TB-Add-1..8 PASS/FAIL verdicts byte-identical across two runs on same BUILD_REQUEST + source tree|rf-qa.md|FR-CONV.1|Re-run on identical input twice; diff verdict table; structural fields byte-equal|S|P0|
|18|NFR-CONV.5|No new external dependencies — diff inspection gate|All TB-Add-1..8 use only Read/Grep/Glob/Bash; no new MCP servers, no synchronous network calls|src/|FR-CONV.1|Diff inspection rejects any new tool invocation beyond the four-tool set|S|P0|
|19|TB-Add catalogue documentation|TB-Add catalogue reference page (8 IDs + Hard/Advisory classification)|Documentation page enumerating TB-Add-1..8 source-check-ID lineage|docs/|FR-CONV.1|Each TB-Add entry documents Hard vs Advisory; cites source-check origin (sc-tasklist intent-port); revertable per-line|S|P0|
|20|FF_TB_ADD_1_THROUGH_8|Feature-flag governance (logical, no runtime flag)|Per-TB-Add revertable-line discipline; TB-Add-2 advisory→hard pending OPEN-INV-006 calibration|git|FR-CONV.1|Each TB-Add appended on its own line/commit; TB-Add-2 stays `[ADVISORY]` until Phase-2 calibration; owner: rf-qa maintainer|S|P0|
|21|K-001 mitigation|TB-Add false-positive contingency wiring|Each TB-Add cites source-check-ID for traceability; individually revertable line; TB-Add-2 ships as ADVISORY|rf-qa.md|FR-CONV.1|Source-check-ID present in every TB-Add emission; revert procedure documented in §19.4 co-revert matrix|S|P0|
|22|K-009 mitigation|Sync-discipline pre-commit gate|All FR-CONV.1 edits target `src/superclaude/` exclusively; `make verify-sync` MUST PASS before commit|Makefile|FR-CONV.1|`make verify-sync` returns 0 after M1 commit; pre-commit hook checks `.claude/` not directly edited (A-001)|S|P0|
|23|DM-004|Per-Item Checklist Schema (Q-DM-1 blocked; lands whichever schema resolves)|Per-item 5-field schema enforced by TB-Add-6 (format) and TB-Add-8 (Context citation). PRD-asserted: Description:one-line-action; Context:file-line-or-justified-absence; Acceptance:observable-success-condition; Confidence:HIGH-MEDIUM-LOW-enum-with-rationale; Verification:command-inspection-or-test. Current SKILL.md alternative: Context; Action; Output; Verification; Completion-gate. Invariant across resolutions: Context field present in both schemas; TB-Add-8 enforcement holds regardless|SKILL.md|FR-CONV.1; Q-DM-1|All 5 fields per the schema chosen by Q-DM-1 resolution: each field has type and validation rule per spec; TB-Add-6 enforces Confidence/Verification format consistency; TB-Add-8 enforces Context field has file:line or justified-absence — applies regardless of resolution option|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|TB-Add catalogue (1..8)|registry|append-to-rf-qa-checklist|M1|FR-CONV.3 INV-010 dynamic enumeration (M3); FR-CONV.4 axis overlay (M4)|
|TB-Add-7 source-areas cross-validator|dispatch (regex check)|wired-to-Execution-Context-block|M1|FR-CONV.2 header (M2) — TB-Add-7 must tolerate degraded References-only form|
|TB-Add-8 evidence-bound check|dispatch (regex check)|wired-to-per-item-Context-field|M1|All downstream FRs preserving per-item Context schema (M2..M6)|
|rf-qa.md:141-142 PASS/FAIL definitions|invariant anchor|preservation-checkpoint|M1|All milestones (NFR-CONV.9 zero-trust QA preservation)|

### Milestone Dependencies — M1

- Q-DM-1 Engineering Lead decision landed (per-item schema authoritative source — see Open Questions below).
- Clean `make verify-sync` baseline before M1 commit (K-009 prevention).
- `rf-team-lead.md:417` NO-DRIFT verified (verified 2026-05-14; K-008 portfolio-wide preservation).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-DM-1|Per-Item Checklist Schema PRD-vs-source contradiction: PRD §25.4 declares the 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` "preserved unchanged" at `SKILL.md:1452-1457`, but current SKILL.md:1450-1460 holds `{Context, Action, Output, Verification, Completion gate}`. Resolution options: (a) FR-CONV.1/TB-Add-8 LANDS the PRD schema (would contradict A-002 unless treated as net-new); (b) correct the PRD §25.4 pointer to the real operational source; (c) §25.4 describes a separate schema living elsewhere. Source: TDD §22 / PRD §25.4.|CRITICAL — blocks TB-Add-6 / TB-Add-8 authoring; downstream TB-Add validation surfaces depend on which schema lands|Engineering Lead|Pre-FR-CONV.1 implementation (Pre-M1 entry gate)|
|2|OPEN-INV-018|If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration. Document layout-change contract. Source: TDD §22 / OPEN-INV-018.|HIGH (K-008 portfolio-wide) — layout change invalidates every FR-CONV path reference|Engineering Lead|Pre-M1 layout-stability commitment; re-check per release|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-001 — TB-Add false positives waste fix-cycles|Low|Low|Low|Each TB-Add cites source-check-ID; TB-Add-2 ships as `[ADVISORY]`; individually revertable line|rf-qa maintainer|
|2|K-008 — INV-018 `.dev/tasks/` layout change invalidates all FR paths|Low|Low|High|Portfolio-wide note; SP-33 stability commitment; re-integration commit contingency covering all 6 FRs|Engineering Lead|
|3|K-009 — Sync-discipline (A-001) violated by direct `.claude/` edit|Low|Low|Medium|All FR-CONV.1 paths reference `src/superclaude/` exclusively; CLAUDE.md mandates workflow; revert direct edit and re-run from `src/superclaude/` on failure|Per-commit author|

## M2: FR-CONV.2 / PR-01 — Execution Context Header

**Objective:** Insert task-level `## Execution Context` block (after frontmatter, before checklist) in generated MDTM task files with exactly three labeled lines (References / Source areas / Key constraints); preserve evidence-bound-item invariant; degrade gracefully to References-only on minimal BUILD_REQUEST. | **Duration:** 2 weeks (2026-05-29 → 2026-06-12) | **Entry:** M1 PASS; TB-Add-7/8 live and tolerant of degraded header; `make verify-sync` clean. | **Exit:** Header renders three labeled lines for fully-populated BUILD_REQUEST; degrades to References-only for minimal BUILD_REQUEST (other lines explicitly omitted, not blank); `grep -E "src/|/.*:[0-9]+"` against header range returns zero; per-item Context fields retain file:line citations.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.2|Insert task-level Execution Context header|Insert `## Execution Context` block after frontmatter, before checklist; exactly 3 labeled lines (CASE-D PR-01); preserve evidence-bound-item invariant|SKILL.md; rf-task-builder.md|M1|Fully-populated BUILD_REQUEST renders 3 labeled lines; minimal BUILD_REQUEST degrades to References-only with other lines explicitly omitted; per-item Context fields unchanged|S|P0|
|2|DM-001|Execution Context Header schema (data model)|Define DM-001 entity: References (list[string] `R-###: <ref-line>`); Source areas (list[string] named modules — NEVER file paths); Key constraints (list[string] 1-3 invariants from BUILD_REQUEST)|SKILL.md|FR-CONV.2|Schema enumerates all 3 fields: References:list-string-R###; Source areas:list-string-no-file-paths; Key constraints:list-string-1-3-items; degradation rule: References-only when BUILD_REQUEST minimal|S|P0|
|3|API-001|BUILD_REQUEST → MDTM contract update|Optional `EXECUTION_CONTEXT_REQUIREMENTS` signal added; generated MDTM file MUST contain `## Execution Context` block at top after frontmatter, before Phase 1|SKILL.md|FR-CONV.2; DM-001|BUILD_REQUEST 15-field schema preserved; new optional signal documented; emission rules per fully-populated vs minimal forms; failure mode = MALFORMED retry (max 2)|S|P0|
|4|DM-001.References|References field emitter|Emit BUILD_REQUEST refs (GOAL, WHY, related-doc IDs) as `R-###: <ref-line>` list entries|rf-task-builder.md|DM-001|References list populated from BUILD_REQUEST GOAL/WHY/related_docs; format `R-###: <ref-line>`; degradation: References never omitted|S|P0|
|5|DM-001.SourceAreas|Source areas field emitter (no file paths)|Emit named modules / packages — hidden-input determinism rule prohibits specific file paths or `file:line` citations|rf-task-builder.md|DM-001|`grep -E "src/|/.*:[0-9]+"` against Source areas line returns zero hits; degradation: explicitly omit (not blank) on minimal BUILD_REQUEST|S|P0|
|6|DM-001.KeyConstraints|Key constraints field emitter (1-3 entries)|Emit top 1-3 invariants pulled verbatim from BUILD_REQUEST|rf-task-builder.md|DM-001|Bounded 1-3 entries; degradation: explicitly omit (not blank) on minimal BUILD_REQUEST|S|P0|
|7|Degradation rule|Minimal BUILD_REQUEST degradation behavior|Block degrades to References-only when GOAL is the only populated field; other 2 lines explicitly omitted, not blank-but-present|rf-task-builder.md|DM-001|Minimal BUILD_REQUEST fixture produces References-only header; degraded form has no `Source areas:` or `Key constraints:` lines (omitted entirely)|S|P0|
|8|Hidden-input guard|No-file-paths invariant in header|Header MUST NOT contain specific file paths or file:line citations (NFR-CONV.3 hidden-input determinism)|rf-task-builder.md|DM-001|Header range grep for `src/` or `/.*:[0-9]+` returns 0; TB-Add-7 cross-validates Source areas against per-item Context fields|S|P0|
|9|COMP-001|SKILL.md primary template insertion (1407-1487)|Insert Execution Context block specification into MDTM template at SKILL.md:1407-1487|SKILL.md|FR-CONV.2|Block specification appears at template top after frontmatter; before `## Phase 1` checklist; verifiable via `grep -n "## Execution Context" src/superclaude/skills/task-builder/SKILL.md`|S|P0|
|10|COMP-001|SKILL.md BUILD_REQUEST guidance update (715-725)|Update BUILD_REQUEST prompt guidance near SKILL.md:715-725 with header generation rules|SKILL.md|FR-CONV.2|BUILD_REQUEST guidance enumerates 3-line vs degraded behavior; cites NFR-CONV.3 hidden-input rule|S|P0|
|11|COMP-002|rf-task-builder header emission logic|Modify rf-task-builder.md to emit `## Execution Context` block at task-file top|rf-task-builder.md|FR-CONV.2|Generated MDTM file contains header after frontmatter and before Phase 1; MALFORMED retry max=2 governs failure case|S|P0|
|12|TEST-004|test_execution_context_full|Fixture asserting 3-labeled-line block in generated MDTM for fully-populated BUILD_REQUEST|tests|FR-CONV.2|grep matches all 3 labeled lines (References / Source areas / Key constraints)|S|P0|
|13|TEST-005|test_execution_context_minimal_buildrequest|Fixture asserting References-only degradation for minimal BUILD_REQUEST|tests|FR-CONV.2|grep matches degraded References-only form; other 2 lines absent|S|P0|
|14|TEST-006|test_execution_context_no_file_paths|Fixture asserting `grep -E "src/|/.*:[0-9]+"` returns 0 in header range|tests|FR-CONV.2|Header range has 0 file:line hits; per-item Context fields outside header still carry citations|S|P0|
|15|NFR-CONV.7|Evidence-bound-item invariant preservation|Per-item Context fields MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8 from M1)|rf-task-builder.md|FR-CONV.2; TB-Add-8|Three-fixture triple: bare path FAILS; file:line PASSES; justified-absence PASSES; integration with TB-Add-8 verified|S|P0|
|16|MIG-002|M1.2 PR-01 landing migration|Strictly-additive header emission; revertable by disabling header generation; per-item Context fields degrade gracefully|src/|FR-CONV.2|Single commit; `make verify-sync` PASS; rollback path documented (disable header gen; per-item Context unchanged)|S|P0|
|17|FF_EXECUTION_CONTEXT_HEADER|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days; owner task-builder maintainer|git|FR-CONV.2|Logical flag; revert by disabling header generation block in rf-task-builder; degraded form is the natural rollback target|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`## Execution Context` block|template insertion|wired-to-MDTM-template-top|M2|TB-Add-7 cross-validator (M1, retroactive consumer); all downstream FRs (header is persistent)|
|EXECUTION_CONTEXT_REQUIREMENTS signal|optional BUILD_REQUEST field|wired-to-orchestrator-prompt|M2|task-builder skill orchestrator (SKILL.md:715-725)|

### Milestone Dependencies — M2

- M1 PASS (TB-Add-7/8 live and tolerant of degraded header form).
- `make verify-sync` PASS after M1 commit.

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-002 — Execution Context header drift (header says X, items say Y)|Low|Low|Low|TB-Add-7 cross-validates Source areas reappear in per-item Context fields; gate fails on drift; header degrades to References-only as fallback|task-builder maintainer|

## M3: FR-CONV.3 / PR-04 — Inherited Structural Verdict + Self-Audit

**Objective:** Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt under `## Inherited Structural Verdict` with directive; add `## Self-Audit` to rf-qa-qualitative output schema; preserve zero-trust QA invariant and the anti-inflation rule at `rf-qa-qualitative.md:766-775` byte-stable; enforce INV-002 freshness, INV-010 dynamic enumeration, INV-019 Self-Audit obligation. | **Duration:** 2 weeks (2026-06-12 → 2026-06-26) | **Entry:** M2 PASS; TB-Add catalogue stable (for INV-010 enumeration); `make verify-sync` clean. | **Exit:** Spawn prompt carries verdict table byte-for-byte; on fix-cycle re-run orchestrator re-injects NEW cycle-N verdict (INV-002); rf-qa-qualitative output contains Self-Audit listing relied-on PASS items AND ≥1 semantic check; anti-inflation bullet at :770 byte-identical pre/post.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.3|Inject Inherited Structural Verdict + Self-Audit|Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt; add Self-Audit to output schema (CASE-B PR-04); preserve zero-trust QA invariant|SKILL.md; rf-qa-qualitative.md|M2|Spawn prompt carries verdict table byte-for-byte; re-injection on fix-cycle; Self-Audit lists relied-on PASS + ≥1 semantic check; anti-inflation rule unchanged|M|P0|
|2|DM-002|Inherited Structural Verdict Block schema|Define DM-002 entity: rf_qa_table_verbatim (string/markdown — byte-exact); prompt_directive (fixed value string); reinjection_rule (fixed value string)|SKILL.md|FR-CONV.3|All 3 fields populated: rf_qa_table_verbatim:byte-exact-rf-qa-Items-Reviewed-table; prompt_directive:fixed-string-verbatim; reinjection_rule:fixed-string-verbatim|S|P0|
|3|DM-002.rf_qa_table_verbatim|Verbatim table copy field|Byte-exact copy of rf-qa task-integrity Items Reviewed table at spawn time (no editing/summarisation/renaming)|SKILL.md|DM-002|Diff vs `${TASK_DIR}qa/qa-task-integrity.md` Items Reviewed table = byte-identical|S|P0|
|4|DM-002.prompt_directive|Fixed-value prompt directive|Fixed-value string: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."|SKILL.md|DM-002|String emitted verbatim; treated as frozen wire ABI (no edits permitted)|S|P0|
|5|DM-002.reinjection_rule|Fixed-value reinjection rule|Fixed-value string: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."|SKILL.md|DM-002|Rule documented in DM-002; enforced by orchestrator at every spawn (INV-002)|S|P0|
|6|DM-005|Phase Contract schema (rf-qa → rf-qa-qualitative)|Define DM-005 entity with 10 fields: producer (fixed rf-qa); consumer (fixed rf-qa-qualitative); artifact; schema_version 1.0.0; delivery_semantics at-most-once-per-cycle; freshness_rule INV-002; enumeration_rule INV-010; consumer_obligation INV-019; anti_inflation; failure_mode|SKILL.md|FR-CONV.3|All 10 fields populated: producer:rf-qa; consumer:rf-qa-qualitative; artifact:Inherited-Structural-Verdict-block; schema_version:1.0.0; delivery_semantics:at-most-once-per-cycle; freshness_rule:reinject-NEW-verdict-INV-002; enumeration_rule:auto-pick-TB-Add-catalogue-INV-010; consumer_obligation:Self-Audit-INV-019; anti_inflation:preserve-766-775; failure_mode:halt-A.10-before-A.10.5|S|P0|
|7|API-002|rf-qa → rf-qa-qualitative inter-agent API|Orchestrator-mediated spawn-prompt injection at SKILL.md §A.10.5; extracts Items Reviewed table contiguously; splices verbatim into spawn prompt|SKILL.md|DM-005|grep `## Inherited Structural Verdict` in spawn-log returns line N; block diff vs `qa-task-integrity.md` byte-identical|S|P0|
|8|Self-Audit output schema|Add `## Self-Audit` section to rf-qa-qualitative output|Output schema addition listing relied-on PASS items AND ≥1 semantic check where PASS is insufficient|rf-qa-qualitative.md|FR-CONV.3|Output contains `## Self-Audit` heading; section lists rf-qa PASS reliance + ≥1 documented semantic check|S|P0|
|9|INV-002|Freshness rule — cycle-N+1 reinjection|Orchestrator MUST re-read current rf-qa task-integrity report and re-extract table on every fix-cycle spawn|SKILL.md|FR-CONV.3|2-cycle fixture: cycle-1 vs cycle-2 spawn prompts byte-diff at table region; cycle-2 carries cycle-2 verdict|S|P0|
|10|INV-010|Dynamic checklist enumeration|Injected verdict table row count enumerates over TB-Add catalogue at runtime (auto-picks up FR-CONV.1 additions)|SKILL.md|FR-CONV.3; TB-Add catalogue|TB-Add catalogue growth → checklist auto-richens; structural diff before/after FR-CONV.1 landing|S|P0|
|11|INV-019|Self-Audit consumer obligation|rf-qa-qualitative output MUST list every rf-qa PASS item it relied on AND ≥1 semantic check where rf-qa PASS is insufficient|rf-qa-qualitative.md|FR-CONV.3|Run with 0 entries in category (b) is a violation; K-003 audits first 5 runs|S|P0|
|12|Anti-inflation preservation|rf-qa-qualitative.md:766-775 byte-stable|Prohibited Behaviors block (anti-inflation bullet at :770) MUST NOT be weakened/removed/rephrased by FR-CONV.3|rf-qa-qualitative.md|FR-CONV.3|byte-diff of Prohibited Behaviors block pre/post = 0; K-003 audit verifies operational compliance|S|P0|
|13|Failure-mode handling|rf-qa task-integrity verdict missing → halt|If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at §A.10 before §A.10.5|SKILL.md|API-002|Missing-verdict fixture: rf-qa-qualitative does not spawn; gate halts; error surfaced to orchestrator|S|P0|
|14|COMP-001|SKILL.md A.10.5 spawn prompt injection (923-1000)|Inject `## Inherited Structural Verdict` block into SKILL.md A.10.5 spawn prompt at ~:966 (after TARGET FILES, before INSTRUCTIONS)|SKILL.md|FR-CONV.3|grep `## Inherited Structural Verdict` in SKILL.md:923-1000 returns ≥1 match; injection point verified at ~:966|S|P0|
|15|COMP-004|rf-qa-qualitative.md EOF append (line 794)|Append "Handling the Inherited Structural Verdict" section + add `## Self-Audit` to output schema at rf-qa-qualitative.md:794|rf-qa-qualitative.md|FR-CONV.3|grep `Self-Audit` in rf-qa-qualitative.md returns ≥1 match at EOF; anti-inflation block at :766-775 byte-identical|S|P0|
|16|TEST-007|test_inherited_verdict_present|Fixture asserting `## Inherited Structural Verdict` block in rf-qa-qualitative spawn prompt|tests|FR-CONV.3|grep matches block header in spawn-log|S|P0|
|17|TEST-008|test_inherited_verdict_freshness_inv_002|2-cycle fixture asserting cycle-2 spawn carries cycle-2 verdict, not stale cycle-1|tests|INV-002|byte-diff of cycle-1 vs cycle-2 spawn prompts shows cycle-2 verdict|S|P0|
|18|TEST-009|test_self_audit_inv_019|Fixture asserting rf-qa-qualitative output contains `## Self-Audit` with ≥1 documented semantic check beyond inherited verdict|tests|INV-019|grep `## Self-Audit` + content inspection finds ≥1 semantic check|S|P0|
|19|TEST-010|test_dynamic_enumeration_inv_010|Fixture asserting checklist auto-richens when FR-CONV.1 catalogue grows|tests|INV-010|Structural diff of checklist before/after catalogue growth shows enrichment|S|P0|
|20|MIG-003|M1.3 PR-04 landing migration|Strictly-additive passthrough; revertable by disabling passthrough block; rf-qa-qualitative falls back to independent structural re-checking|src/|FR-CONV.3|Single commit; `make verify-sync` PASS; rollback path: disable passthrough flag, fallback to current behavior|S|P0|
|21|FF_INHERITED_STRUCTURAL_VERDICT|Feature-flag governance (logical)|Enabled at merge; cleanup post-K-003 audit pass (release-spec §8.3 row 4); owner QA Lead|git|FR-CONV.3|Logical flag; K-003 audit-target governs cleanup; revert path disables passthrough block|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`## Inherited Structural Verdict` block|spawn-prompt injection|wired-to-SKILL.md-A.10.5|M3|rf-qa-qualitative spawn (FR-CONV.4 axis overlay consumes structural PASS via INV-013)|
|DM-005 Phase Contract|inter-agent contract|wired-to-orchestrator-spawn-step|M3|All future inter-agent contracts (versioning baseline 1.0.0)|
|`## Self-Audit` output section|output-schema addition|wired-to-rf-qa-qualitative.md-EOF|M3|K-003 audit-target (M7); ongoing per-release inspection|

### Milestone Dependencies — M3

- M2 PASS.
- TB-Add catalogue stable (FR-CONV.1 / M1 landed) — INV-010 dynamic enumeration depends on it.
- `make verify-sync` PASS after M2 commit.

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-X-002|PR-04 anti-inflation operational test — "reliance ≠ verification" distinction is empirically observable, not structurally provable. Audit per release-spec.md §8.3 row 4 — first 5 rf-qa-qualitative runs after FR-CONV.3. Source: TDD §22 / OPEN-X-002.|HIGH (K-003 audit-target) — if audit shows inflation, FR-CONV.3 must be rolled back per §19.4|QA Lead|First 5 rf-qa-qualitative runs post-FR-CONV.3 land (audit window in M7)|
|2|OPEN-PR05|When does `.dev/tasks/done/` reach ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05 (Tier-History Advisory)? Status: tracked, Phase-2 deferral; re-check each major release. Source: TDD §22 / OPEN-PR05.|LOW — PR-05 deferred to Phase-2 (NFR-CONV.3 hidden-input determinism enforces non-introduction in v3.9)|Engineering Lead|Re-check each major release|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-003 — PR-04 passthrough causes inflation despite anti-inflation rule|Medium|Low|Medium|INV-019 mandatory Self-Audit; X-002 audit-target (first 5 rf-qa-qualitative runs MUST be audited per release-spec §8.3 row 4); disable passthrough flag on audit FAIL|QA Lead|
|2|K-007 — PR-04 + PR-06 sequencing inversion (PR-04 lands before PR-06)|Medium|Low|Medium|Sequencing rule enforced in release-spec §4.6; INV-010 dynamic-enumeration mitigation (auto-richens when catalogue activates); re-merge in correct order on inversion detection|Engineering Lead|

## M4: FR-CONV.4 / PR-07 — Five Adversarial Axes Overlay

**Objective:** Insert `### Five Adversarial Axes` header subsection BEFORE rf-qa-qualitative's 15-item task-qualitative checklist; add `axis` column to Items Reviewed table; preserve zero-trust QA invariant and severity floor at `rf-qa-qualitative.md:786-795`; emit `drift-axis-inactive` annotation when no item restates BUILD_REQUEST.GOAL verbatim. | **Duration:** 2 weeks (2026-06-26 → 2026-07-10) | **Entry:** M3 PASS; Inherited Structural Verdict live (INV-013 composition). | **Exit:** Five Adversarial Axes header renders BEFORE 15-item checklist; Axis column populated with one canonical value per row from `{AX-1..AX-5, none}`; `drift-axis-inactive` annotation emitted in Summary block when GOAL-baseline absent; severity floor block byte-identical; 15-item checklist unchanged.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.4|Insert Five Adversarial Axes overlay|Insert axis-overlay header BEFORE rf-qa-qualitative 15-item checklist; add axis column to Items Reviewed table (CASE-D PR-07); overlay-only, no new conditional code path|rf-qa-qualitative.md; SKILL.md|M3|Subsection renders before 15-item checklist; Axis column populated per row; drift-axis-inactive annotation in Summary when no GOAL-baseline item|S|P0|
|2|AX-1|Drift axis definition|A cited fact (file path, line number, signature, count, config value) no longer matches current source|rf-qa-qualitative.md|FR-CONV.4|AX-1 enumerated in canonical axes block (§8.5); finding example shows stale citation pattern|S|P0|
|3|AX-2|Contradictions axis definition|Two artifacts (or two sections) assert mutually incompatible facts about same subject|rf-qa-qualitative.md|FR-CONV.4|AX-2 enumerated in canonical axes block; finding example shows return-type mismatch pattern|S|P0|
|4|AX-3|Omissions axis definition|A required touchpoint, consumer, dependency, or step absent from plan|rf-qa-qualitative.md|FR-CONV.4|AX-3 enumerated; finding example shows missing signature-update pattern|S|P0|
|5|AX-4|Weakened-criteria axis definition|Acceptance/verification condition softened to unobservable or trivially satisfiable|rf-qa-qualitative.md|FR-CONV.4|AX-4 enumerated; finding example shows trivially-passing test pattern|S|P0|
|6|AX-5|Invented-content axis definition|Artifact introduces requirement/feature/capability not present in upstream source|rf-qa-qualitative.md|FR-CONV.4|AX-5 enumerated; finding example shows scope-inflation pattern|S|P0|
|7|`none` sentinel|none-axis sentinel value|Used when check passed and axis lens surfaced nothing (NOT an N/A escape)|rf-qa-qualitative.md|FR-CONV.4|Items Reviewed row with passing check carries `Axis: none`; documented in canonical annotation rules|S|P0|
|8|`drift-axis-inactive` annotation|drift-axis-inactive Summary-block annotation|Single-line Summary-block annotation when artifact has no citations to drift against|rf-qa-qualitative.md|FR-CONV.4|GOAL-baseline absent fixture emits `drift-axis-inactive` annotation; not encoded as `Axis: N/A`|S|P0|
|9|Axis column on Items Reviewed table|Axis column addition (rf-qa-qualitative.md:675-714)|Insert `axis` column between `Check` and `Result` columns|rf-qa-qualitative.md|FR-CONV.4|Every row in task-qualitative Items Reviewed table carries one canonical axis value or `none`; column omitted entirely for non-task-qualitative phases|S|P0|
|10|Five Adversarial Axes header subsection|Header insertion before 15-item checklist (rf-qa-qualitative.md:527)|`### Five Adversarial Axes` subsection inserted BEFORE `#### Checklist (15 items)` header at rf-qa-qualitative.md:527-583|rf-qa-qualitative.md|FR-CONV.4|grep ordering assertion: `### Five Adversarial Axes` appears before `#### Checklist`; 15-item checklist body unmodified|S|P0|
|11|15-item checklist preservation|Existing 15-item checklist body unchanged|Body at rf-qa-qualitative.md:527-583 MUST be unmodified; axes multiply lenses, not checks (TOTAL stays at 15 items)|rf-qa-qualitative.md|FR-CONV.4|byte-diff of 15-item checklist body pre/post = 0; Tool Engagement Minimum unchanged at `tool calls ≥ 15`|S|P0|
|12|Severity-floor preservation (786-795)|rf-qa-qualitative severity floor unchanged|Contradictions always IMPORTANT/CRITICAL; severity floor at rf-qa-qualitative.md:786-795 MUST NOT be weakened|rf-qa-qualitative.md|FR-CONV.4|byte-diff of Critical Rules block pre/post = 0|S|P0|
|13|COMP-004|rf-qa-qualitative.md axis-column site (675-714)|Modify Items Reviewed table at rf-qa-qualitative.md:675-714 to add `axis` column between `Check` and `Result`|rf-qa-qualitative.md|FR-CONV.4|`axis` column header present in table; parse confirms one axis value per row|S|P0|
|14|COMP-001|SKILL.md task-qualitative prompt axis directive (961)|Add axis-annotation directive at SKILL.md:961 in Task-Qualitative prompt|SKILL.md|FR-CONV.4|grep `Axis` in SKILL.md:~961 returns ≥1 match; directive instructs annotation per row|S|P0|
|15|TEST-011|test_five_axes_overlay|Fixture asserting axes header appears BEFORE immutable 15-item checklist|tests|FR-CONV.4|grep ordering assertion confirms header-before-checklist|S|P0|
|16|TEST-012|test_axis_column_populated|Fixture asserting Items Reviewed table carries non-empty Axis value on every row|tests|FR-CONV.4|Parse table; assert no empty Axis cell|S|P0|
|17|TEST-013|test_drift_axis_inactive_when_no_goal_baseline|Fixture asserting `drift-axis-inactive` annotation emitted (not N/A) when no GOAL-baseline item|tests|FR-CONV.4|grep matches `drift-axis-inactive` annotation in Summary block|S|P0|
|18|TEST-014|test_severity_floor_unweakened|Fixture asserting severity-floor block at rf-qa-qualitative.md:786-795 unchanged|tests|FR-CONV.4|byte-diff of Critical Rules block = 0|S|P0|
|19|MIG-004|M1.4 PR-07 landing migration|Strictly-additive overlay; revertable by removing axis column + drift-axis-inactive annotation; 15-item checklist untouched|src/|FR-CONV.4|Single commit; `make verify-sync` PASS; rollback path removes overlay, checklist intact|S|P0|
|20|FF_FIVE_ADVERSARIAL_AXES|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days post-axis-distribution audit (K-004); owner rf-qa-qualitative maintainer|git|FR-CONV.4|Logical flag; revert path removes overlay; cleanup gated on K-004 axis-distribution audit|S|P0|

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
|1|K-004 — 5-axis annotation ambiguity over-flags items|Low|Low|Low|Annotation-only overlay (no new code path); severity floor preserved; `drift-axis-inactive` annotation for missing GOAL-baseline|rf-qa-qualitative maintainer|

## M5: FR-CONV.5 / PR-02 — Retry Monotonicity + Regression Halts

**Objective:** Add two stop-conditions to EXISTING fix-cycle retry loops (no new loop or stage): monotonicity guard (HALT if `|F_{n+1}|>=|F_n|`) and regression detection (HALT if any item PASS at cycle N is FAIL at cycle N+1); regression precedence over monotonicity; preserve four independent retry counters (no collapsing); preserve existing 3-cycle hard cap at `rf-team-lead.md:417`. | **Duration:** 2 weeks (2026-07-10 → 2026-07-24) | **Entry:** M4 PASS; FR-CONV.6 dedup-key wire-shape spec finalised (mutual coupling — M5 specifies the shape it consumes; M6 lands the emitter). | **Exit:** Regression flip emits verbatim message and exits BEFORE monotonicity check; non-shrink emits `[HALT-MONOTONICITY] |F|=<n>`; identical dedup-key synthetic findings across cycles do NOT trigger halt; legitimate slow-cycle correction NOT halted; X-003 slow-convergence threshold remains REJECTED; all 4 fixtures PASS.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.5|Add monotonicity + regression halt guards|Add two stop-conditions to existing fix-cycle retry loops (CASE-D PR-02); regression > monotonicity precedence; preserve zero-trust QA invariant|SKILL.md; rf-task-builder.md; rf-qa.md|M4|Two halts wired to existing loops; regression precedes monotonicity; slow-shrink continues; identical-dedup-key synthetic does not trip regression (INV-012); 3-cycle cap preserved|M|P0|
|2|API-004|Fix-Loop Halt Signals contract|Define halt-message strings as inter-loop wire ABI; ordering rule per cycle transition n→n+1 (regression first, monotonicity second, hard-cap third, proceed fourth)|SKILL.md|FR-CONV.5|All 4 ordering rules enforced; halt strings byte-exact (fixtures depend on character-for-character match); F-set definition uses dedup-key identity|S|P0|
|3|Monotonicity halt message|`[HALT-MONOTONICITY]|F|=<n>` halt-string emitter|Emit verbatim halt string when `|F_{n+1}|>=|F_n|`; only consulted when `|F_n|> 0`|SKILL.md; rf-task-builder.md|API-004|Halt string emitted byte-exact per spec; emission gated on prior regression-check passing; monotonicity check skipped when `F_n=0`|S|P0|
|4|Regression halt message|Verbatim regression-detection halt-string emitter|Emit verbatim string `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` when item flips PASS@N→FAIL@N+1|SKILL.md; rf-task-builder.md|API-004|String emitted byte-exact; emitted BEFORE monotonicity check; precedence rule honored|S|P0|
|5|F-set definition|`F_n` set with dedup-key identity|`F_n` = set of FAIL-verdict items at end of fix cycle n with item identity = dedup-key; cardinality after dedup-key deduplication|SKILL.md|API-004|Identity rule documented; cardinality computed post-dedup; composition with synthetic-dnsp findings (INV-012) wired|S|P0|
|6|Ordering precedence rule|Per-cycle precedence: regression > monotonicity > hard-cap > proceed|Strict ordering check per cycle transition n→n+1: (1) regression check first; (2) monotonicity check second; (3) existing 3-cycle hard cap third; (4) otherwise proceed to n+2|SKILL.md|API-004|Each cycle transition checks 4 conditions in order; regression always exits BEFORE monotonicity check; existing rf-team-lead.md:417 hard cap preserved as fallback|S|P0|
|7|INV-012|Cross-cycle synthetic-dnsp dedup composition|Synthetic-dnsp findings count as failures for `|F_n|` cardinality; identical dedup_key across consecutive cycles is dedup case (NOT regression — prior verdict was already FAIL)|SKILL.md|FR-CONV.5; FR-CONV.6|Synthetic with same dedup_key in cycles N, N+1 contributes 1 (not 2) to `|F_{n+1}|`; persistence trips monotonicity (intended), not regression|S|P0|
|8|3-cycle hard cap preservation|Existing rf-team-lead.md:417 preservation|Existing 3-cycle hard cap MUST NOT be replaced or short-circuited; verified NO DRIFT 2026-05-14|rf-team-lead.md|FR-CONV.5|byte-diff of rf-team-lead.md:417 line pre/post = 0; cap remains as fourth-precedence backstop|S|P0|
|9|Four-counter preservation|Four independent retry counters MUST NOT be collapsed|Per-gate fix-cycle counters (rf-task-builder.md I16 table) remain independent; FR-CONV.5 layers halts ON TOP without merging|rf-task-builder.md|FR-CONV.5|Per-gate counters at rf-task-builder.md:354-360 preserved; no shared monotonicity state across counters|S|P0|
|10|X-003 rejection enforcement|No "shrinks too slowly" threshold|Rate-threshold halt design (X-003) REJECTED; `|F|= 5, 4` (shrink by 1) MUST continue|SKILL.md|FR-CONV.5|Slow-shrink fixture continues to next cycle; no rate-of-shrink parameter introduced|S|P0|
|11|COMP-001|SKILL.md A.9 separate-counters invariant tail (867-873)|Modify SKILL.md A.9 separate-counters invariant tail to add halt-precedence note|SKILL.md|FR-CONV.5|grep `[HALT-MONOTONICITY]` in SKILL.md:867-873 returns ≥1 match; precedence rule documented|S|P0|
|12|COMP-001|SKILL.md Behavioral Constraints hard-invariants (1547-1553)|Add halt-precedence rule to Behavioral Constraints hard-invariants list at SKILL.md:1547-1553|SKILL.md|FR-CONV.5|grep `Regression detected on Item` in SKILL.md:1547-1553 returns ≥1 match|S|P0|
|13|COMP-002|rf-task-builder.md I16 fix-cycle encoding (334-361)|Modify rf-task-builder.md QA-gate fix-cycle encoding table at :334-361 with halt rules|rf-task-builder.md|FR-CONV.5|Halt rules documented at I16; per-gate caps unchanged|S|P0|
|14|COMP-003|rf-qa.md Fix Cycle Protocol Rules (308-315)|Modify rf-qa.md Fix Cycle Protocol Rules at ~:308-315 — promote existing SHOULD bullet to MUST-halt|rf-qa.md|FR-CONV.5|grep `MUST` related to halt at rf-qa.md:308-315 returns ≥1 match|S|P0|
|15|TEST-015|test_monotonicity_halt_F_5_5_5|3-cycle fixture: `|F|= 5, 5, 5` halts at cycle 2 with `[HALT-MONOTONICITY]|F|=5`; cycle 3 not attempted|tests|FR-CONV.5|grep halt message; assert no cycle-3 log entry|S|P0|
|16|TEST-016|test_regression_halt_pass1_fail2|Item 3.2 PASS@1 / FAIL@2 fixture: halts with verbatim regression message BEFORE monotonicity check|tests|FR-CONV.5|grep verbatim message; ordering assertion confirms regression check runs first|S|P0|
|17|TEST-017|test_slow_shrink_continues|`|F|= 5, 4` fixture: continues — strict shrink holds; X-003 NOT triggered|tests|FR-CONV.5|Execution log shows cycle continues to next iteration|S|P0|
|18|TEST-022|test_synthetic_dnsp_dedup_not_regression|Synthetic with same dedup_key in cycles 1+2 (other findings shrinking) proceeds to cycle 3 — no regression halt (INV-012)|tests|INV-012|Execution log shows cycle 3 attempted; no regression halt emitted for cross-cycle dedup|S|P0|
|19|TEST-024|test_sequencing_PR06_before_PR04|Sequencing test: if PR-04 (FR-CONV.3) lands before PR-06 (FR-CONV.1), dynamic enumeration still richens once catalogue activates|tests|INV-010|Structural assertion on enriched checklist; mitigation against K-007 verified|S|P0|
|20|MIG-005|M1.5 PR-02 landing migration|Strictly-additive halts on existing loops; revertable by disabling guards individually; per-gate caps continue to govern on rollback|src/|FR-CONV.5|Single commit; `make verify-sync` PASS; rollback path: disable guards, retain existing caps|S|P0|
|21|FF_RETRY_MONOTONICITY_GUARDS|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days post false-halt-rate audit (K-005); owner rf-task-builder maintainer|git|FR-CONV.5|Logical flag; revert path disables both guards individually; cleanup gated on K-005 audit|S|P0|

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
|1|K-005 — Retry monotonicity halts legitimate slow-cycle correction|Low|Low|Low|Strict-shrink threshold (`|F|= 5, 4` continues); X-003 slow-convergence threshold REJECTED; disable guards individually on rollback|rf-task-builder maintainer|

## M6: FR-CONV.6 / PR-03 — Synthetic DNSP on Partition Exhaust

**Objective:** After a partition agent's escalation ladder exhausts (rf-analyst, rf-qa, or rf-qa-qualitative partition instance), emit synthetic HIGH-severity finding with `source: "synthetic-dnsp"` to agent's output stream rather than silently aborting; preserve all-agents-fail guard (zero partitions succeeded → no synthetic, existing rf-team-lead.md:417 escalation runs); preserve zero-trust QA + evidence-bound-item + parallel-research invariants. | **Duration:** 2 weeks (2026-07-24 → 2026-08-07) | **Entry:** M5 PASS; halt-signal contract live (API-004 consumes synthetic findings via dedup_key composition). | **Exit:** When ≥1 partition succeeded AND ≥1 exhausted, synthetic-dnsp HIGH finding emitted with all 5 fixed fields + dedup_key + found_n_times; identical dedup_keys collapse with `found N times`; zero-partitions-succeeded → NO synthetic emits and existing escalation runs; N-1 partitions complete concurrently (INV-021).

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-CONV.6|Emit synthetic-dnsp on partition exhaust|After partition agent's escalation ladder exhausts, emit synthetic HIGH-severity finding (CASE-B PR-03 BASE); preserve all-agents-fail guard|SKILL.md; rf-analyst.md; rf-qa.md; rf-qa-qualitative.md|M5|All 5 fixed fields + 2 dedup-control fields present; HIGH severity non-overridable; all-agents-fail bypass preserved; N-1 partitions concurrent (INV-021)|L|P0|
|2|DM-003|Synthetic DNSP Finding schema|Define DM-003 entity with 7 fields: severity:HIGH-fixed; source:synthetic-dnsp-fixed; affected_range:string; evidence:spawn-log-path-or-stub; recommendation:fixed-string; dedup_key:2-tuple; found_n_times:int-default-1|rf-qa.md|FR-CONV.6|All 7 fields populated per spec: severity:HIGH-fixed-non-overridable; source:literal-synthetic-dnsp-sentinel; affected_range:verbatim-assigned-files-slice; evidence:never-blank-spawn-log-or-stub; recommendation:fixed-Manual-review-required-string; dedup_key:tuple-(assigned_files_range,escalation_ladder_exhaust_point); found_n_times:int-default-1|S|P0|
|3|DM-003.severity|severity field — fixed HIGH non-overridable|HIGH severity literal; guarantees gate-level visibility; cannot be downgraded|rf-qa.md|DM-003|Emission with severity != HIGH = invalid; gate-level visibility verified|S|P0|
|4|DM-003.source|source field — fixed `synthetic-dnsp` literal sentinel|Grep-able literal sentinel string for operator inspection|rf-qa.md|DM-003|`grep -n "synthetic-dnsp"` in rf-analyst.md / rf-qa.md returns ≥1 hit per file|S|P0|
|5|DM-003.affected_range|affected_range field — exhausted agent's assigned_files slice|Verbatim copy of partition's file list as received in spawn prompt|rf-qa.md|DM-003|Exhausted-partition fixture: affected_range matches spawn-prompt assigned_files byte-for-byte|S|P0|
|6|DM-003.evidence|evidence field — spawn-log path or stub citing log absence|Never blank — if log missing, stub explicitly cites absence (`no-spawn-log: <reason>`)|rf-qa.md|DM-003|Evidence field never empty; canonical path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`|S|P0|
|7|DM-003.recommendation|recommendation field — fixed string|Fixed value: `Manual review required — partition agent failed twice`|rf-qa.md|DM-003|Emission carries fixed recommendation string byte-exact|S|P0|
|8|DM-003.dedup_key|dedup_key field — 2-tuple identity|Composite `(assigned_files_range, escalation_ladder_exhaust_point)`; canonical wire format YAML list `["<range>", "<exhaust_point>"]`; exhaust_point from closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`|rf-qa.md|DM-003|dedup_key emitted as YAML list; exhaust_point in closed vocabulary; deterministic equality enabled|S|P0|
|9|DM-003.found_n_times|found_n_times field — collision counter|Default 1; increments by 1 on each within-cycle dedup collapse|rf-qa.md|DM-003|Two identical dedup_keys within cycle collapse to one record with found_n_times=2|S|P0|
|10|API-003|Partition agent → orchestrator API|Partition emits structured block in normal output stream (no separate channel); consumed by SKILL.md §A.8 + §A.10 merge step|SKILL.md|DM-003|grep `source: "synthetic-dnsp"` in partition output stream; orchestrator merge step picks up block|S|P0|
|11|escalation_ladder_exhaust_point vocabulary|Closed vocabulary registry|`{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` — free-form descriptions forbidden|rf-qa.md|DM-003.dedup_key|Vocabulary documented; non-vocabulary values rejected; dedup-key equality deterministic|S|P0|
|12|All-agents-fail guard precedence|Zero-partitions-succeeded → NO synthetic emits|Mutually exclusive paths: ≥1 success AND ≥1 exhaust → emit; zero success → activate rf-team-lead.md:417|SKILL.md; rf-team-lead.md|FR-CONV.6|Zero-partitions fixture: no synthetic block emitted; execution log shows rf-team-lead.md:417 escalation activates|S|P0|
|13|Within-cycle dedup collapse|Within-cycle identical-dedup_key collapse|Two synthetic findings with identical dedup_key collapse to one record with `found_n_times` incremented|SKILL.md|DM-003|Fixture: two identical-exhaust events collapse to one finding with `found_n_times=2`; cardinality 1 verified|S|P0|
|14|Cross-cycle dedup non-regression|Cross-cycle identical-dedup_key NOT regression (INV-012)|Cross-cycle identical dedup_key is dedup case, NOT regression — prior verdict was already FAIL|SKILL.md|FR-CONV.5; FR-CONV.6|Cross-cycle synthetic same dedup_key contributes 1 (not 2) to `|F_{n+1}|`; trips monotonicity (intended), not regression|S|P0|
|15|INV-021|Within-agent-instance emission (cohort does not serialize)|On one partition's escalation exhaust, N-1 sibling partitions continue concurrently to completion before exhausted one synthesises finding|rf-qa.md|FR-CONV.6|Spawn-log fixture: N-1 partitions overlap exhausted partition's synthesis; timestamp evidence proves concurrency|S|P0|
|16|HIGH severity non-overridable|Severity HIGH guarantees gate visibility|Synthetic findings emit ALONGSIDE (not in place of) real findings from successful partitions|SKILL.md|DM-003.severity|Emission cardinality: real findings preserved; synthetic adds HIGH visibility finding for exhausted partition|S|P0|
|17|COMP-001|SKILL.md A.8 Research Quality Gate (572-656)|Modify SKILL.md A.8 to wire synthetic-dnsp merge step|SKILL.md|FR-CONV.6|Merge step wired at A.8; synthetic block picked up alongside real findings|S|P0|
|18|COMP-001|SKILL.md A.10 Task File Validation (870-918)|Modify SKILL.md A.10 to wire synthetic-dnsp merge step at task-integrity phase|SKILL.md|FR-CONV.6|Merge step wired at A.10|S|P0|
|19|COMP-005|rf-analyst partition + DNSP edit site (58-71)|Modify rf-analyst.md:58-71 with DNSP emission logic|rf-analyst.md|FR-CONV.6|`grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md` returns ≥1 hit|S|P0|
|20|COMP-003|rf-qa DNSP edit site (49-77, primary at 70-77)|Modify rf-qa.md:49-77 with DNSP emission logic at :70-77|rf-qa.md|FR-CONV.6|`grep -n "synthetic-dnsp" src/superclaude/agents/rf-qa.md` returns ≥1 hit|S|P0|
|21|COMP-004|rf-qa-qualitative DNSP edit site (70-80)|Modify rf-qa-qualitative.md:70-80 with DNSP emission logic|rf-qa-qualitative.md|FR-CONV.6|`grep -n "synthetic-dnsp" src/superclaude/agents/rf-qa-qualitative.md` returns ≥1 hit|S|P0|
|22|COMP-006|rf-team-lead.md preservation (line 417 NO DRIFT)|rf-team-lead.md line 417 MUST NOT be replaced/short-circuited; verified NO DRIFT 2026-05-14|rf-team-lead.md|FR-CONV.6|byte-diff of rf-team-lead.md:417 pre/post = 0; activated by all-agents-fail path|S|P0|
|23|TEST-018|test_dnsp_twice_exhaust|Partition fixture timing out twice emits synthetic-dnsp finding with all 5 fixed fields|tests|DM-003|Parse YAML/block; assert all 5 fields populated; severity HIGH; source synthetic-dnsp|S|P0|
|24|TEST-019|test_dnsp_dedup_collapse|Two identical-dedup_key synthetic findings collapse into one record with found_n_times=2|tests|DM-003.found_n_times|Parse merged YAML; assert cardinality 1 + found_n_times=2|S|P0|
|25|TEST-020|test_dnsp_all_agents_fail_bypass|Zero partitions succeeded → no synthetic emits; existing rf-team-lead.md:417 escalation activates|tests|FR-CONV.6|Execution log shows HALT path; no synthetic block emitted; rf-team-lead activation verified|S|P0|
|26|TEST-021|test_dnsp_does_not_serialize_cohort|On one partition's escalation exhaust, N-1 sibling partitions continue concurrently (INV-021)|tests|INV-021; NFR-CONV.10|Spawn-log timing: N-1 partitions overlap exhausted partition's synthesis|S|P0|
|27|MIG-006|M1.6 PR-03 landing migration|Strictly-additive emission logic; revertable by removing DNSP edit sites; existing rf-team-lead.md:417 already handles zero-partitions-succeeded|src/|FR-CONV.6|Single commit; `make verify-sync` PASS; rollback path: revert DNSP sites, all-agents-fail escalation remains|S|P0|
|28|FF_SYNTHETIC_DNSP_EMISSION|Feature-flag governance (logical)|Enabled at merge; cleanup at GA + 30 days post-emission-count audit (K-006); owner rf-analyst / rf-qa maintainers|git|FR-CONV.6|Logical flag; revert path removes DNSP sites; cleanup gated on K-006 audit|S|P0|
|29|NFR-CONV.10|Parallel-research invariant preservation|N partition agents spawn concurrently; on one's exhaust N-1 continue to completion before that one synthesises DNSP|rf-qa.md; rf-qa-qualitative.md|FR-CONV.6|Spawn-log timestamps prove concurrency; cohort never serialises; INV-021 wired|S|P0|

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
|1|K-006 — Synthetic-dnsp findings mask real issues|Low|Low|Low|HIGH severity guarantees gate visibility; dedup_key prevents over-emission; weekly inspection of emission-count metric|rf-qa maintainer|

## M7: Production Readiness — K-003 Audit + NFR-CONV.4 Measurement + GA

**Objective:** Audit first 5 rf-qa-qualitative runs post-FR-CONV.3 (K-003 / X-002 audit-target); measure token-cost on 5 representative BUILD_REQUESTs against NFR-CONV.4 ≤1.10 ratio; instrument observability counters (synthetic-dnsp, HALT-MONOTONICITY, regression-halt, Self-Audit coverage, make verify-sync PASS rate); ship runbook for OPS-001..007 scenarios; remove fallback paths at GA + 30 days; commit v3.9 GA. | **Duration:** 2 weeks (2026-08-07 → 2026-08-21) | **Entry:** M6 PASS; all 6 FR-CONV.X merged; `make verify-sync` PASS. | **Exit:** K-003 audit PASS on first 5 rf-qa-qualitative runs (100% Self-Audit coverage with ≥1 independent semantic check each); NFR-CONV.4 ratio ≤1.10 across all 5 representative BUILD_REQUESTs; runbook published; observability counters live; v3.9 GA tagged.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|MIG-007|Post-merge audit + NFR-CONV.4 measurement orchestration|Coordinate K-003 first-5-runs audit + NFR-CONV.4 token-cost measurement on 5 representative BUILD_REQUESTs|process|All FRs landed|Audit report published; token-cost ratio computed; GA tag created on PASS|M|P0|
|2|NFR-CONV.4|Token-cost ratio empirical measurement (≤1.10)|Measure token-cost ratio post-merge / pre-merge per equivalent BUILD_REQUEST; ceiling 1.10|process|All FRs landed|5 BUILD_REQUESTs covering Quick/Standard/Deep tiers; pre-merge baseline + post-merge counts; ratio ≤1.10|S|P0|
|3|NFR-CONV.5|No-new-dependencies post-merge audit|Audit all 6 FR diffs to confirm only Read/Grep/Glob/Bash used; no new MCP servers; no synchronous network calls|process|All FRs landed|Diff inspection across 6 FRs returns zero new external dep introductions|S|P0|
|4|NFR-CONV.6|self-contained-item invariant fixture PASS|Synthetic fixture with all 5 fields populated PASSES all 8 TB-Add checks; same fixture with one field stripped FAILS TB-Add-1|tests|FR-CONV.1; Q-DM-1|Composite fixture per NFR-CONV.6; binding to whichever schema resolves Q-DM-1|S|P0|
|5|NFR-CONV.8|Persistent .dev/tasks/ artifact invariant verification|Diff `.dev/tasks/<task-id>/` directory layout pre-merge vs post-merge — zero structural changes (no new mandatory subdirectory, no rename of research/qa/synthesis/reviews/adversarial, no naming-pattern change)|process|All FRs landed|Diff output empty; INV-018 preservation verified|S|P0|
|6|NFR-CONV.9|Zero-trust QA invariant verification|Two-part fixture: (a) 1-LOW-finding fixture → gate FAILS; (b) FR-CONV.3 inherited-verdict applied → no item marked VERIFIED unless Self-Audit lists independent semantic-check engagement|tests|FR-CONV.1; FR-CONV.3|Both fixture parts PASS per spec; verbatim PASS/FAIL definitions at rf-qa.md:141-142 byte-identical|S|P0|
|7|NFR-CONV.2|Research-driven prose determinism exclusion documentation|Document NFR-CONV.2 scope split: structural fields byte-deterministic; research-prose nondeterminism acceptable; structural annotations within prose (axis labels, finding counts, dedup-keys) remain byte-equal|docs/|All FRs landed|Documentation page; structural-vs-prose boundary enumerated; M7 audit verifies structural annotations byte-equal across 2 runs|S|P0|
|8|NFR-CONV-R1|Single-pass gate PASS rate baseline measurement|Run 5 representative BUILD_REQUESTs; count first-cycle PASS verdicts; target ≥80%|process|All FRs landed|≥4 of 5 BUILD_REQUESTs PASS task-integrity gate on first cycle (≥80%)|S|P0|
|9|NFR-CONV.3|Hidden-input determinism guard verification|Fixture-populated `.dev/tasks/done/` vs empty: byte-identical structural output|tests|All FRs landed|byte-diff of structural fields = 0; PR-05 advisory mechanism remains REJECTED for Phase-1|S|P0|
|10|TEST-023|test_hidden_input_guard fixture|Fixture-populated `.dev/tasks/done/` yields byte-identical structural output vs empty-done baseline|tests|NFR-CONV.3|byte-diff of structural fields = 0|S|P0|
|11|TEST-025|test_invariant_preservation_NFR_6_through_10 composite|All 5 invariants (self-contained-item, evidence-bound-item, persistent-artifact, zero-trust QA, parallel-research) preserved per Negative Criteria|tests|All FRs landed|Composite fixture exercises each invariant surface; all 5 invariants PASS|S|P0|
|12|OPS-001|K-003 audit-target runbook (first 5 rf-qa-qualitative runs)|Runbook: symptoms / diagnosis / resolution / escalation / prevention for Self-Audit missing or zero-independent-checks|docs/|FR-CONV.3|Runbook published; Self-Audit coverage gauge target 100% on first 5 runs documented; QA Lead 4-business-hour response SLA|S|P0|
|13|OPS-002|DNSP triage runbook (synthetic-dnsp emission count >0)|Runbook: read affected partition's spawn-log; identify root cause of escalation-ladder exhaust; check dedup_key for prior similar events; escalate ≥3 distinct dedup-keys in a week|docs/|FR-CONV.6|Runbook published; 24-hour response SLA; weekly inspection cadence|S|P0|
|14|OPS-003|All-partitions-exhaust HALT runbook (no DNSP)|Runbook: confirm zero partition successes; verify line-417 escalation fired and NO synthetic-dnsp emitted (correct per FR-CONV.6 mutual-exclusivity)|docs/|FR-CONV.6|Runbook published; mutual-exclusivity check documented; resolution = user resolves unresolved findings|S|P0|
|15|OPS-004|`[HALT-MONOTONICITY]` rate >50% runbook|Runbook: sample 3 halt events; inspect BUILD_REQUESTs for upstream defects; inspect MDTM for structural issues; resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)|docs/|FR-CONV.5|Runbook published; threshold >50% documented; upstream quality-gate referral path|S|P0|
|16|OPS-005|Regression-halt rate >20% runbook|Runbook: sample 3 regression events; inspect what changed between cycles; resolution = tighten fix-cycle prompts (X-003 slow-convergence threshold REJECTED)|docs/|FR-CONV.5|Runbook published; threshold >20% documented; Engineering Lead escalation|S|P0|
|17|OPS-006|`make verify-sync` FAIL post-FR-merge runbook|Runbook: re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline (A-001); revert direct `.claude/` edit on persistent failure (K-009 contingency)|docs/|All FRs landed|Runbook published; pre-commit hook enforcement documented; immediate response SLA|S|P0|
|18|OPS-007|INV-018 layout-change runbook (K-008)|Runbook: inspect all 6 FRs for path/naming references; re-integration commit covering all 6 FRs per §19.4 dependency matrix|docs/|All FRs landed|Runbook published; portfolio-wide blast-radius response documented; SP-33 stability commitment cited|S|P0|
|19|Synthetic-dnsp emission counter|Counter metric — synthetic-dnsp emission count|Counter incrementing per emission; threshold >0 in production triggers human review per OPS-002|observability|FR-CONV.6|Counter wired via grep `"source: synthetic-dnsp"` across rf-analyst / rf-qa / rf-qa-qualitative outputs; offline review cadence weekly|S|P0|
|20|HALT-MONOTONICITY counter + alert rule|Counter metric — [HALT-MONOTONICITY] count; alert rule >50% of fix-cycle batches|Counter wired via grep `[HALT-MONOTONICITY]` in fix-loop execution logs; alert rule per OPS-004|observability|FR-CONV.5|Counter + alert rule wired; alert threshold >50% of batches documented as upstream BUILD_REQUEST defect signal|S|P0|

### Integration Points — M7

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Observability counters (synthetic-dnsp, HALT-MONOTONICITY, regression-halt, Self-Audit coverage, make verify-sync PASS rate)|metric emitter + alert rule registry|wired-to-offline-grep-pipeline|M7|Per-release audit + ongoing release-spec §8.3 audit-row inspection|
|OPS-001..007 runbooks|operational documentation|wired-to-on-call-knowledge-base|M7|task-builder maintainers (on-call rotation)|
|Feature-flag cleanup (6 logical flags)|governance lifecycle|wired-to-GA+30days-cleanup|M7|Post-GA fallback-path removal|

### Milestone Dependencies — M7

- All 6 FR-CONV.X landed (M1..M6 PASS).
- `make verify-sync` PASS after every prior commit.
- First 5 real rf-qa-qualitative runs available for K-003 audit.

### Open Questions — M7

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OPEN-TOKEN|NFR-CONV.4 token-ceiling empirical measurement: actual post-merge token-cost ratio against 1.10 ceiling on 5 representative BUILD_REQUESTs. Source: TDD §22 / OPEN-TOKEN.|MEDIUM — if ceiling exceeded, summarise FR-CONV.3 verdict table rather than emit verbatim (K-010 contingency)|Engineering Lead|Post-merge measurement (M7 audit window)|

### Risk Assessment and Mitigation — M7

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|K-003 — Audit FAIL on first 5 rf-qa-qualitative runs|Medium|Low|Medium|If audit shows inflation → roll back FR-CONV.3 per §19.4; INV-019 Self-Audit mandate enforces structural visibility|QA Lead|
|2|K-010 — Token ceiling NFR-CONV.4 exceeded by >10%|Low|Low|Low|Empirical measurement on 5 BUILD_REQUESTs; contingency = summarise FR-CONV.3 verdict table rather than emit verbatim|Engineering Lead|

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

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|K-001|TB-Add false positives waste fix-cycles|M1|Low|Low|Each TB-Add cites source-check-ID; TB-Add-2 ships as `[ADVISORY]`; individually revertable line|rf-qa maintainer|
|K-002|Execution Context header drift (header says X, items say Y)|M2|Low|Low|TB-Add-7 cross-validates header source-areas reappear in items; gate fails on drift; header degrades to References-only fallback|task-builder maintainer|
|K-003|PR-04 passthrough causes inflation despite anti-inflation rule|M3, M7|Low|Medium|INV-019 mandatory Self-Audit; X-002 audit-target — first 5 rf-qa-qualitative runs MUST be audited; contingency = disable passthrough flag|QA Lead|
|K-004|5-axis annotation ambiguity over-flags items|M4|Low|Low|Annotation-only overlay; severity floor preserved; `drift-axis-inactive` annotation when no GOAL-baseline; audit axis distribution post-GA|rf-qa-qualitative maintainer|
|K-005|Retry monotonicity halts legitimate slow-cycle correction|M5|Low|Low|Strict-shrink threshold; X-003 slow-convergence threshold REJECTED; disable guards individually on rollback|rf-task-builder maintainer|
|K-006|Synthetic-dnsp findings mask real issues|M6|Low|Low|HIGH severity guarantees gate visibility; dedup_key prevents over-emission; weekly emission-count inspection|rf-qa maintainer|
|K-007|PR-04 + PR-06 sequencing inversion|M3|Low|Medium|Sequencing rule enforced in release-spec §4.6; INV-010 dynamic-enumeration mitigation; re-merge in correct order on inversion|Engineering Lead|
|K-008|INV-018 `.dev/tasks/` directory layout change invalidates all FR paths|M1 (preventive), all milestones|Low|High|Portfolio-wide note; SP-33 stability commitment; re-integration commit contingency covering all 6 FRs|Engineering Lead|
|K-009|Sync-discipline (A-001) violated by direct `.claude/` edit|M1 (preventive), all milestones|Low|Medium|All FRs name `src/superclaude/` paths exclusively; CLAUDE.md mandates workflow; revert `.claude/` direct edit; re-run from `src/superclaude/`|Per-commit author|
|K-010|Token ceiling NFR-CONV.4 exceeded by >10%|M7|Low|Low|Empirical post-merge measurement on 5 BUILD_REQUESTs; contingency = summarise FR-CONV.3 verdict table rather than emit verbatim|Engineering Lead|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|Single-pass gate PASS rate|Fraction of BUILD_REQUESTs passing task-integrity gate on first cycle|≥80% (currently baseline) ↑ post-merge|Run 5 representative BUILD_REQUESTs; count first-cycle PASS|M7|
|Placeholder-defect detection rate|TB-Add-1 fires on placeholder/title-only fixture items|100% on synthetic fixtures|TEST-001 synthetic-fixture assertion|M1|
|DAG-cycle detection rate|TB-Add-4 fires on circular-dependency fixtures|100% on synthetic fixtures|TEST-002 synthetic-fixture assertion|M1|
|Self-Audit coverage post-FR-CONV.3|Every rf-qa-qualitative run carries `## Self-Audit` entry with ≥1 independent semantic check|100% on first 5 runs (K-003 audit-target)|grep `## Self-Audit` + content inspection across first 5 runs (OPS-001 runbook)|M7|
|`[HALT-MONOTONICITY]` emission rate|Counter of halt emissions per fix-cycle batches|<10% target; >50% triggers upstream BUILD_REQUEST defect alert|grep `[HALT-MONOTONICITY]` in fix-loop logs; offline aggregate per release|M7|
|Synthetic-dnsp emission count|Counter of synthetic-dnsp findings emitted|≥1 on twice-exhaust fixture; 0 on healthy runs|grep `"source: synthetic-dnsp"` across QA reports|M7|
|Generation-cost efficiency|Token-cost ratio post-merge / pre-merge|≤1.10 per equivalent BUILD_REQUEST (NFR-CONV.4)|5 representative BUILD_REQUESTs; pre/post token counts; compute ratio|M7|
|Gate convergence health|Fix-cycle convergence rate to gate PASS|≥75% baseline ↑ post-merge|Fraction of fix-cycle sequences converging to PASS rather than hitting cap or monotonicity halt|M7|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Port direction|Intent-port (adapt intent, re-express in task-builder idiom) — 5 mechanisms ported|(1) Bulk-implementation-port all 17 sc-tasklist Stage-6 checks — REJECTED per CB-3 (only 8 of 17 are intent-portable; 11 are bundle-specific to phase-file naming, checkpoint emission, T-ID format); (2) Do nothing — REJECTED (persistent silent-acceptance defects, unbounded oscillation cost per FINAL-REPORT §6.2 F2)|FINAL-REPORT §6.3 asymmetric finding establishes the 5 mechanisms as worth adopting; per-check classification (CB-3) shows only 8 of 17 are intent-portable; bulk-port would force X-001 blanket "no specific file paths" rule onto per-item Context fields, gutting evidence-bound-item invariant|
|Governance model|Strictly-additive A-002 (no existing item renamed/renumbered/removed) with per-FR rollback granularity|Single-FR mega-merge — REJECTED (eliminates per-FR rollback granularity; co-revert matrix per §19 requires FRs expressible independently)|Per-FR rollback granularity is stated release goal; composition lives in algorithm not single monolithic structure; release-spec.md §9 SP-10 documents co-revert matrix|
|Determinism scope|Structural fields byte-deterministic (NFR-CONV.1); research-prose nondeterminism acceptable (NFR-CONV.2)|(1) Full byte-determinism — REJECTED (impossible with LLM-driven builder); (2) Zero determinism — REJECTED (gate verdicts must be reliable enough to drive PASS/FAIL)|LLM determinism achievable on structured output but not on free prose; structural annotations within prose (axis labels, finding counts, dedup-keys) remain byte-equal to keep gate verdicts reliable|
|Anti-inflation handling|Absolute preservation of `rf-qa-qualitative.md:766-775`; FR-CONV.3 inherited verdict is deliberately-scoped RELIANCE channel for structural items only|(1) Strict mechanical re-check — REJECTED (wastes fix cycles); (2) Pure passthrough — REJECTED (rubber-stamp risk)|INV-019 Self-Audit mandate makes the rule auditable; K-003 designates first 5 runs as audit-target; failure path = disable passthrough flag (§19.4 rollback)|
|All-agents-fail guard precedence|FR-CONV.6 mutually exclusive: ≥1 success AND ≥1 exhaust → emit synthetic-dnsp; zero success → activate rf-team-lead.md:417 (NO synthetic)|(1) DNSP always emits on any exhaust — REJECTED (would mask total-failure condition); (2) No DNSP at all — REJECTED (leaves partial-failure case silent)|Preserves established 3-fix-cycle escalation; DNSP adds coverage for partial-failure case without short-circuiting "stop the line" HALT; rf-team-lead.md:417 verified NO DRIFT|
|FR-CONV.5 stop-condition design|Strict shrink + regression precedence (regression > monotonicity > hard-cap > proceed); F-set has dedup-key identity|(1) X-003 "shrinks too slowly" rate threshold — REJECTED (introduces tunable K with no principled value; legitimate slow-cycle is normal); (2) Pure cardinality, no regression — REJECTED (misses PASS@N→FAIL@N+1 swaps where cardinality stays constant)|Composition matters — F is set with identity, not just count; INV-012 dedup-key composition with FR-CONV.6 requires set-identity semantics; web-02 §4 prior art (ddmin failure-preservation invariant) supports regression precedence|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1 (FR-CONV.1 / PR-06)|2 weeks|2026-05-15|2026-05-29|Q-DM-1 resolved; TB-Add-1..8 land across 3 surfaces; TEST-001..003 PASS; `make verify-sync` PASS|
|M2 (FR-CONV.2 / PR-01)|2 weeks|2026-05-29|2026-06-12|Execution Context header live; DM-001 fields wired; TEST-004..006 PASS|
|M3 (FR-CONV.3 / PR-04)|2 weeks|2026-06-12|2026-06-26|Inherited Structural Verdict + Self-Audit live; DM-002/DM-005 wired; TEST-007..010 PASS; anti-inflation byte-stable|
|M4 (FR-CONV.4 / PR-07)|2 weeks|2026-06-26|2026-07-10|Five Adversarial Axes overlay live; AX-1..5 + none + drift-axis-inactive; TEST-011..014 PASS; severity floor byte-stable|
|M5 (FR-CONV.5 / PR-02)|2 weeks|2026-07-10|2026-07-24|Monotonicity + regression halts live; API-004 halt-signal contract wired; TEST-015..017, 022, 024 PASS|
|M6 (FR-CONV.6 / PR-03)|2 weeks|2026-07-24|2026-08-07|Synthetic DNSP live; DM-003 5-field emission + dedup_key composition; TEST-018..021 PASS; rf-team-lead.md:417 byte-stable|
|M7 (Audit + Measurement + GA)|2 weeks|2026-08-07|2026-08-21|K-003 audit PASS on first 5 rf-qa-qualitative runs; NFR-CONV.4 ratio ≤1.10 on 5 BUILD_REQUESTs; OPS-001..007 runbooks published; v3.9 GA tag|

**Total estimated duration:** 14 weeks (2026-05-15 → 2026-08-21), landing within the TDD §23.1 v3.9 GA = 2026-Q3 commitment with ~6 weeks of buffer before Q3 close (2026-09-30).
