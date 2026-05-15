# Research Notes: Task-Builder Convergence v3.9 TDD

**Date:** 2026-05-14
**Status:** Complete
**Scenario:** A (Explicit request — PRD provided + output location specified + scope bounded by 6 FRs)
**Tier:** Heavyweight
**Tier rationale:** Scope spans 6 functional requirements across 2 skills and 4 rf-* agents — 6 source files (`src/superclaude/skills/task-builder/SKILL.md` at 1709 lines, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` at 1390 lines, plus four rf-* agent files totaling 2,068 lines). Total source = ~6,103 lines. Architectural layers touched: skill orchestration, agent partition protocols, retry-loop control, inter-agent contract (rf-qa → rf-qa-qualitative spawn prompt), gate-checklist topology (4-stage), and `.dev/tasks/` artifact persistence. The PRD itself is 1,057 lines with 6 FRs + 10 NFRs + 5 load-bearing invariants + a G6 four-case conflict rule. This is platform-scale design (>20 relevant interaction points across multiple subsystems), which mandates the Heavyweight tier per SKILL.md tier selection rules.

**Output target:** `.dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.md` (per user-supplied `--output` argument).

---

## EXISTING_FILES

### Source-of-truth files in scope (per PRD §27 "Source code targets")

| File | Lines | Purpose | Key sections referenced by PRD |
|---|---|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` | 1709 | Generation orchestration; 4-stage gate topology; A.1–A.11 pipeline; agent prompt templates; output structure; task file content rules | **228-238** (Tier Selection), **719** (Execution Overview), **870** (Retry monotonicity insertion), **898-906** (9-item A.10 task-integrity checklist), **923-1000** (A.10.5 Task File Qualitative Validation + spawn prompt), **961** (5-axis overlay insertion), **1409-1485** (Builder Agent Prompt + BUILD_REQUEST template), **1452-1457** (5-field per-item schema example), **1491-1507** (15-item Task File Validation Checklist), **1530** (rule #2 file:line citation), **1550** (Retry monotonicity insertion #2), **574-654** + **872-916** (DNSP emission edits) |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 1390 | Source of the 5 imported mechanisms (intent-port reference, NOT modified by this release) | 17-point gate (994-1037 Quality Gates), 5-category adversarial prompt (Bucket A line refs), Stages 9-10 monotonicity + regression (Post-Generation Roadmap Validation, lines 1083+) |
| `src/superclaude/agents/rf-qa.md` | 432 | Partitioned QA agent; 20-item task-integrity checklist (264-287); research-gate (96-141); synthesis-gate (146-211); report-validation (215-256); task-integrity (259-289); fix-cycle (291-313); partition protocol (49-77); zero-trust verdict (140-142) | **70-77** (DNSP emission edit), **140-142** (zero-trust verdict; "Any gap … = FAIL"), **264-287** (20-item checklist landing site for TB-Add-1..8), **310-313** (retry monotonicity tie-in to fix cycle) |
| `src/superclaude/agents/rf-qa-qualitative.md` | 794 | Adversarial QA agent; 7 specialised QA phases (PRD, report, TDD, tech-ref, ops-guide, README, **task-qualitative at 508-583**); Adaptation Guidance (NO N/A rule, 564); Self-Audit requirement (per phase); Severity Ratings; anti-inflation rule (766-775); Prohibited Behaviors | **72-78** (DNSP emission edit), **527-583** (Task-Qualitative 15-item checklist + 5 Adversarial Axes overlay insertion site), **675-714** (Items Reviewed table — axis column), **766-775** (anti-inflation rule — MUST NOT weaken), **789** (severity floor — MUST NOT weaken), **794** (Inherited Structural Verdict block insertion site) |
| `src/superclaude/agents/rf-analyst.md` | 349 | Partitioned analyst agent; cross-validates research; completeness verification | **60-69** (DNSP emission edit site) |
| `src/superclaude/agents/rf-task-builder.md` | 493 | Subagent that emits MDTM file; QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS / TESTING_REQUIREMENTS encoding (336-359 region) | **336-359** (retry monotonicity integration site within QA-gate encoding region) |
| `src/superclaude/agents/rf-team-lead.md` | 431 | Project-mode orchestrator; **417** "3 fix cycles per phase" escalation rule | **417** (all-agents-fail guard preserved; DO NOT short-circuit) — actually located ~line 414 in current source, see "Verified line-number drift" below |

### Release-spec artifacts inspected (read-only context, not edited)

| File | Purpose |
|---|---|
| `.dev/releases/current/task-builder-merge/release-spec.md` (71,481 bytes) | Authoritative source spec — PRD claims compliance with v1.0.0 |
| `.dev/releases/current/task-builder-merge/conflict-register.md` | 5 CASE-D rows (PR-01, PR-02, PR-05, PR-06, PR-07); CASE-B rows correctly omitted (PR-03 BASE, PR-04 passthrough) |
| `.dev/releases/current/task-builder-merge/adversarial/refactor-plan.md` (15,983 bytes) | Per-FR landing-sequence and rollback granularity |
| `.dev/releases/current/task-builder-merge/adversarial/merge-log.md` (6,585 bytes) | Per-change merge events |
| `.dev/releases/current/task-builder-merge/adversarial/per-proposal-verdicts.md` (11,533 bytes) | Per-proposal verdict scores |
| `.dev/releases/current/task-builder-merge/adversarial/invariant-probe.md` (11,210 bytes) | INV-002, INV-006, INV-010, INV-012, INV-015, INV-018, INV-019, INV-021 |
| `.dev/releases/current/task-builder-merge/reflection/reflect-task.md` (10,149 bytes) | G1–G5 reflection findings |
| `.dev/releases/current/task-builder-merge/reflection/gate-report.md` (5,672 bytes) | Phase 5.2 PASS verdict on all 5 gates |
| `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md` | §6.3 asymmetric finding (motivating upstream evidence); §6.2 F2 (21 retry / 18 batches) + F4 (hidden-input determinism) |

### Verified line-number drift (must be re-confirmed by deep investigation)

- PRD cites `rf-qa.md:140-142` for the zero-trust verdict. Grep confirms "PASS — All checks pass" and "FAIL — Any gaps exist (CRITICAL, IMPORTANT, or MINOR)" appear at **rf-qa.md:144-146** in the current source (close, but offset by ~2 lines).
- PRD cites `rf-qa.md:264-287` for the 20-item task-integrity checklist. Grep confirms checklist actually spans **rf-qa.md:266-287** in current source.
- PRD cites `rf-team-lead.md:417` for "3 fix cycles per phase." Grep confirms the phrase appears at **rf-team-lead.md:414** in current source.
- All other PRD-cited line numbers (SKILL.md:898-906, SKILL.md:1452-1457, SKILL.md:1491-1507, rf-qa-qualitative.md:766-775) match current source byte-for-byte.
- TDD synthesis MUST cite current line numbers, not PRD-asserted line numbers. Each cited `file:line` MUST be re-verified with `sed -n` or Read before TDD assembly.

---

## PATTERNS_AND_CONVENTIONS

### 1. Five Task-Builder Invariants (load-bearing, per release-spec.md §1.0)

| Invariant | Operational source | Mechanism |
|---|---|---|
| **self-contained-item** | `task-builder/SKILL.md:1452-1457` | Every checklist item carries 5 fields: Description, Context, Acceptance, Confidence, Verification — sufficient to execute without reading other items |
| **evidence-bound-item** | `task-builder/SKILL.md:1530` (rule #2) | Per-item Context referencing code surface has `file:line` citation OR justified-absence comment |
| **persistent-`.dev/tasks/`-artifact** | OPEN-INV-018 (PRD §13) | Research and QA outputs persist to `.dev/tasks/<task-id>/` with stable naming |
| **zero-trust QA** | `rf-qa.md:144-146` | "Any gap regardless of severity = FAIL" stance at task-integrity gate |
| **parallel-research** | `rf-qa.md:49-77`, `rf-qa-qualitative.md:50-82`, NFR-CONV.10 | rf-analyst and rf-qa partition cohorts run concurrently; per-partition failures don't serialize the cohort |

### 2. G6 Four-Case Conflict Rule (authoritative tiebreaker, per release-spec.md Appendix D)

| Case | Definition | Disposition rule | Conflict-register row? |
|---|---|---|---|
| **A** | sc has mechanism; task-builder has conflicting mechanism | Explicit {ADOPT-ADAPTED, REJECT}; protected invariant required | YES |
| **B** | sc has mechanism; task-builder silent (no conflict) | ADOPT or ADOPT-ADAPTED | NO |
| **C** | sc silent; task-builder has mechanism | Keep task-builder; nothing to import | NO |
| **D** | sc has mechanism; task-builder has *related but non-conflicting* mechanism | ADOPT-ADAPTED with scope-confinement or per-check classification (CB-3) | YES |

Portfolio distribution per PRD §14.3: PR-01 D, PR-02 D, PR-03 B, PR-04 B, PR-05 D (deferred), PR-06 D, PR-07 D. Conflict-register has exactly 5 D-rows (one per CASE-D proposal). PR-03 (DNSP synthetic finding) and PR-04 (Gate Results Passthrough) are CASE-B and correctly omitted from the register.

### 3. 4-Stage Gate Topology (preserved by all 6 FRs)

Stage 1: Research Gate (rf-qa research-gate phase, lines 96-141 of rf-qa.md)
Stage 2: Synthesis Gate (rf-qa synthesis-gate phase, lines 146-211)
Stage 3: Report Validation Gate (rf-qa report-validation phase, lines 215-256)
Stage 4: Task Integrity Gate (rf-qa task-integrity phase, lines 259-289; A.10 in SKILL.md) → followed by A.10.5 Task Qualitative gate (rf-qa-qualitative.md:508-583)

No FR adds, removes, or renames a stage. All landings are insertions WITHIN existing stages. The PR-04 passthrough mechanism establishes a contract BETWEEN stage 4 (rf-qa task-integrity) and the rf-qa-qualitative task-qualitative phase that immediately follows it.

### 4. Strictly-Additive Edit Discipline (A-002 governance)

Every FR is a strictly-additive change. No existing rf-qa check, rf-qa-qualitative checklist item, gate stage, output field, or `.dev/tasks/` layout entry is removed or renamed. Each FR's Negative Criterion explicitly lists what MUST NOT be modified. Per-FR rollback granularity = revert specific append lines.

### 5. Partition + Escalation + DNSP-emit Pattern

rf-qa and rf-analyst spawn N parallel partition agents (typically when file count >6). Each partition runs an escalation ladder (initial → retry-1 → retry-2). On full ladder exhaust for one partition (rf-team-lead.md "3 fix cycles per phase" rule at ~line 414), the partition emits a synthetic-dnsp HIGH-severity finding rather than silently aborting. The all-agents-fail guard reserves: if **zero** partitions succeeded, the existing escalation path activates instead of DNSP emission.

### 6. Anti-Inflation Rule (rf-qa-qualitative.md:766-775)

"NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION." This rule constrains the PR-04 Inherited Structural Verdict mechanism: rf-qa-qualitative MUST treat inherited PASS as a signal to skip mechanical re-checking, NOT as a license to mark items VERIFIED without independent semantic engagement. INV-019 mandates that the first 5 real runs after FR-CONV.3 lands produce a `## Self-Audit` entry showing ≥1 semantic check beyond inherited PASS.

### 7. Hidden-Input Determinism Guard (NFR-CONV.3)

Task-builder MUST NOT read any input outside `BUILD_REQUEST + source-tree` that could modify behavior. This is the explicit deferral lever for PR-05 (Tier-History Advisory): reading `.dev/tasks/done/TASK-RF-*` frontmatter to adjust tier selection would introduce hidden input. The fixture-test contract: "Fixture-populated `.dev/tasks/done/` MUST produce byte-identical structural output to empty `.dev/tasks/done/`."

### 8. Determinism Scope Split (NFR-CONV.1 vs NFR-CONV.2)

- **Structural fields** (TB-Add-* PASS/FAIL, synthetic-dnsp 5 fixed fields, dedup-key, axis column) MUST be byte-deterministic.
- **Research-driven prose** (per-item Context prose, rf-qa-qualitative semantic-check prose) MAY vary across runs — LLM nondeterminism acceptable. Diff-on-rerun must be limited to prose; structural fields must remain byte-equal.

---

## PRD_CONTEXT

### Epics (4 total; PRD §21.1.1)

1. **Epic 1 — Structural Gate Reinforcement** (FR-CONV.1 + FR-CONV.2) — P0
2. **Epic 2 — Inter-Agent Verdict Channel** (FR-CONV.3 + FR-CONV.4) — P0
3. **Epic 3 — Retry & Exhaust Resilience** (FR-CONV.5 + FR-CONV.6) — P0
4. **Epic 4 — Tier-History Advisory (DEFERRED)** (PR-05) — P2, Phase-2

### Functional Requirements (6 FRs, strictly serial sequencing per release-spec.md §4.6)

| FR | Proposal | CASE | Lands | Description | Insertion points |
|---|---|---|---|---|---|
| **FR-CONV.1** | PR-06 | D | 1st | Append 8 TB-Add checks (TB-Add-1..8) to rf-qa task-integrity | `rf-qa.md:264-287` + `SKILL.md:898-906` + `SKILL.md:1491-1507` |
| **FR-CONV.2** | PR-01 | D | 2nd | Insert `## Execution Context` block in generated MDTM file (3 labeled lines: References / Source areas / Key constraints; **strictly NO file paths in header**) | `SKILL.md:228-238` + `SKILL.md:1409-1485` + `SKILL.md:719` |
| **FR-CONV.3** | PR-04 | B | 3rd | Inject rf-qa verdict verbatim under `## Inherited Structural Verdict` in rf-qa-qualitative spawn; cycle-N+1 reinjection (INV-002); dynamic checklist enumeration (INV-010); Self-Audit mandate (INV-019) | `SKILL.md:923-1000` + `rf-qa-qualitative.md:794` |
| **FR-CONV.4** | PR-07 | D | 4th | Insert "Five Adversarial Axes" header BEFORE 15-item checklist; axis column on Items Reviewed table; `drift-axis-inactive` annotation when no GOAL-baseline item exists | `rf-qa-qualitative.md:527-583` + `rf-qa-qualitative.md:675-714` + `SKILL.md:961` |
| **FR-CONV.5** | PR-02 | D | 5th | Add 2 stop-conditions: monotonicity (`F_{n+1} >= F_n` HALT) + regression (PASS@N → FAIL@N+1 HALT, takes precedence over monotonicity); INV-012 dedup-key composition rule | `SKILL.md:870` + `SKILL.md:1550` + `rf-task-builder.md:336-359` + `rf-qa.md:310-313` |
| **FR-CONV.6** | PR-03 (BASE) | B | 6th | Emit HIGH-severity synthetic-dnsp finding with 5 fixed fields + dedup-key on partition exhaust; preserve all-agents-fail guard (rf-team-lead.md:417) | `SKILL.md:574-654` + `SKILL.md:872-916` + `rf-analyst.md:60-69` + `rf-qa.md:70-77` + `rf-qa-qualitative.md:72-78` |

### Non-Functional Requirements (10 NFRs)

- **NFR-CONV.1**: Determinism — structural fields byte-deterministic
- **NFR-CONV.2**: Determinism scope — research-prose excluded (LLM nondeterminism acceptable)
- **NFR-CONV.3**: Hidden-input guard — fixture-populated `.dev/tasks/done/` produces byte-identical output to empty
- **NFR-CONV.4**: Token ceiling — ≤10% increase on 5 representative BUILD_REQUESTs
- **NFR-CONV.5**: Wall-clock — no new external deps; existing tools only (Read, Grep, Glob, Bash)
- **NFR-CONV.6–10**: One per invariant — self-contained-item / evidence-bound-item / persistent-artifact / zero-trust-QA / parallel-research preservation

### Acceptance Criteria Pattern (per FR, three-field)

Every FR carries:
- **Observable behavior** (visible/emitted output condition)
- **Verification method** (grep/fixture test commanding exact match)
- **Negative criterion** (Out of scope / Must not break — names protected invariants and rejected alternatives)

### Critical PRD Invariant: Per-FR Rollback Granularity

The 6 FRs land in strict serial order, but each is independently revertable. Rollback dependency matrix in release-spec.md §9 SP-10:
- Reverted FR-CONV.5 (monotonicity) → co-revert FR-CONV.6 dedup-key emission
- Reverted FR-CONV.1 (TB-Add catalogue) → co-revert FR-CONV.3 dynamic-enumeration consumer
- All other FRs independently revertable

### K-Risks (10 entries; PRD §20)

K-001 TB-Add false positives, K-002 header drift, **K-003 PR-04 inflation risk (audit-target — first 5 runs)**, K-004 axis ambiguity, K-005 monotonicity over-halt, K-006 DNSP masking, K-007 PR-04/PR-06 sequencing, **K-008 `.dev/tasks/` layout change (portfolio-wide blast)**, K-009 sync-discipline (A-001), K-010 token ceiling exceeded.

### Open Questions (6 entries; PRD §13)

OPEN-PR05 (threshold), OPEN-INV-006 (calibration), OPEN-INV-017 (staleness), OPEN-INV-018 (layout contract), **OPEN-X-002 (anti-inflation operational test)**, **OPEN-TOKEN (NFR-CONV.4 measurement)**.

---

## SOLUTION_RESEARCH

This release **documents an already-agreed engineering decision** (the inverse-direction merge per FINAL-REPORT §6.3). The PRD presents the decision; the TDD's job is to translate it into actionable engineering specifications. However, the TDD MUST cover the design decisions implicit in the spec:

### Design alternatives the TDD MUST surface in §21

1. **Alternative 0: Do Nothing** (mandatory per template) — Why not leave task-builder as-is? Cost: silent acceptance of placeholder items, undetected DAG cycles, rubber-stamped rf-qa-qualitative passes, 21-retry/18-batch oscillation from FINAL-REPORT §6.2 F2.
2. **Alternative 1: Bulk-port all 17 `/sc:tasklist` checks** (REJECTED per CB-3) — Bundle-specific checks (phase-file naming, index references) inapplicable to single-MDTM output; blanket "no specific file paths" rule (X-001) would break evidence-bound-item invariant.
3. **Alternative 2: Continue v3.8 RF→SC direction only** (REJECTED) — FINAL-REPORT §6.3 documented asymmetry one-way; portfolio-wide adversarial debate identified 5 ADOPT-grade qualities in inverse direction.
4. **Alternative 3: Ship PR-05 (Tier-History Advisory) in Phase-1 with advisory framing** (REJECTED — DEFERRED) — Hidden-input determinism risk (NFR-CONV.3) inverts the over-engineering pattern from FINAL-REPORT §6.2 F4.
5. **Alternative 4: Single-FR mega-merge** (REJECTED) — Per-FR rollback granularity is a release goal; mega-merge eliminates rollback granularity.

### Design decisions the TDD MUST capture in §6.4

- **Intent-port over implementation-port** (Strategic Bet 1) — Adapt intent, not implementation, when crossing paradigms (generation vs execution).
- **Additive-only governance (A-002)** — Strictly additive landings keep blast radius low.
- **Per-check classification (CB-3) over bulk-port** — Importing 8 unique TB-Add checks (not all 17), each cited by source-check-ID.
- **G6 four-case rule as authoritative tiebreaker** — Conflict-register row required for CASE-A and CASE-D; CASE-B and CASE-C correctly silent.
- **Determinism scope split** — Structural fields deterministic; research-prose nondeterminism acceptable.
- **Anti-inflation rule absolute** — PR-04 passthrough MUST NOT weaken or rephrase rf-qa-qualitative.md:766-775; Self-Audit listing makes this auditable.
- **All-agents-fail guard precedence** — DNSP emission MUST NOT short-circuit existing rf-team-lead.md:417 escalation when zero partitions succeeded.
- **Dedup-key composition with monotonicity** (INV-012) — Synthetic-dnsp findings count as failures for `|F_n|`, but identical dedup-key across consecutive cycles is dedup, not regression.

---

## RECOMMENDED_OUTPUTS

### Task folder structure

```
.dev/tasks/to-do/TASK-TDD-20260514-121250/
├── TASK-TDD-20260514-121250.md     (MDTM task file — created by rf-task-builder in A.7)
├── research-notes.md                (this file)
├── research/                        (16 codebase files + 2 web files)
├── synthesis/                       (10 synthesis files mapped to TDD sections)
├── qa/                              (3 analyst reports + 4 QA reports)
└── reviews/                         (final qualitative review)
```

### Final TDD output (per user `--output` argument)

`.dev/releases/current/task-builder-merge/TDD_TASK_BUILDER_CONVERGENCE.md`

### Codebase research files (Phase 2; 16 files, zero-padded numbering)

| # | Topic | Agent type | Files to investigate | Output path |
|---|---|---|---|---|
| **00** | PRD requirements extraction | rf-task-researcher | `.dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md` | `research/00-prd-extraction.md` |
| **01** | task-builder SKILL.md architecture (A.1–A.11 pipeline + 4-stage gate topology) | Architecture Analyst | `src/superclaude/skills/task-builder/SKILL.md` lines 1-1709 | `research/01-task-builder-skill-architecture.md` |
| **02** | sc-tasklist-protocol SKILL.md — source of imported mechanisms | Doc Analyst | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` lines 1-1390 | `research/02-sc-tasklist-source-mechanisms.md` |
| **03** | rf-qa partition + verdict topology (research / synthesis / report-val / task-integrity) | Code Tracer | `src/superclaude/agents/rf-qa.md` lines 1-432 | `research/03-rf-qa-topology.md` |
| **04** | rf-qa-qualitative 7-phase structure + anti-inflation rule + Self-Audit | Code Tracer | `src/superclaude/agents/rf-qa-qualitative.md` lines 1-794 | `research/04-rf-qa-qualitative-topology.md` |
| **05** | rf-analyst partition protocol + completeness verification | Code Tracer | `src/superclaude/agents/rf-analyst.md` lines 1-349 | `research/05-rf-analyst-topology.md` |
| **06** | rf-task-builder QA-gate / validation / testing encoding | Code Tracer | `src/superclaude/agents/rf-task-builder.md` lines 1-493 | `research/06-rf-task-builder-encoding.md` |
| **07** | rf-team-lead escalation + 3-fix-cycle behavior | Code Tracer | `src/superclaude/agents/rf-team-lead.md` lines 1-431 | `research/07-rf-team-lead-escalation.md` |
| **08** | Per-FR insertion-point verification (FR-CONV.1 — TB-Add 1..8 landing sites) | Code Tracer | `src/superclaude/agents/rf-qa.md:264-287` + `src/superclaude/skills/task-builder/SKILL.md:898-906` + `:1491-1507` | `research/08-fr1-tb-add-landings.md` |
| **09** | Per-FR insertion-point verification (FR-CONV.2 — Execution Context header) | Code Tracer | `src/superclaude/skills/task-builder/SKILL.md:228-238` + `:719` + `:1409-1485` | `research/09-fr2-execution-context.md` |
| **10** | Per-FR insertion-point verification (FR-CONV.3 — Inherited Structural Verdict + Self-Audit) | Code Tracer | `src/superclaude/skills/task-builder/SKILL.md:923-1000` + `src/superclaude/agents/rf-qa-qualitative.md:794` + `:766-775` | `research/10-fr3-inherited-verdict.md` |
| **11** | Per-FR insertion-point verification (FR-CONV.4 — Five Adversarial Axes overlay) | Code Tracer | `src/superclaude/agents/rf-qa-qualitative.md:527-583` + `:675-714` + `src/superclaude/skills/task-builder/SKILL.md:961` | `research/11-fr4-adversarial-axes.md` |
| **12** | Per-FR insertion-point verification (FR-CONV.5 — Monotonicity + regression guards) | Code Tracer | `src/superclaude/skills/task-builder/SKILL.md:870` + `:1550` + `src/superclaude/agents/rf-task-builder.md:336-359` + `src/superclaude/agents/rf-qa.md:310-313` | `research/12-fr5-retry-monotonicity.md` |
| **13** | Per-FR insertion-point verification (FR-CONV.6 — DNSP synthetic-dnsp finding) | Code Tracer | `src/superclaude/skills/task-builder/SKILL.md:574-654` + `:872-916` + `src/superclaude/agents/rf-analyst.md:60-69` + `src/superclaude/agents/rf-qa.md:70-77` + `src/superclaude/agents/rf-qa-qualitative.md:72-78` | `research/13-fr6-dnsp-synthetic.md` |
| **14** | Invariant probe — preservation conditions for 5 load-bearing invariants (NFR-CONV.6..10) | Architecture Analyst | All 6 source files at invariant-anchor lines | `research/14-invariant-preservation.md` |
| **15** | Data models — `## Execution Context`, `## Inherited Structural Verdict`, synthetic-dnsp finding, per-item 5-field schema (PRD §25 schemas) | Data Model Analyst | PRD §25 + current SKILL.md schema at 1452-1457 | `research/15-data-models.md` |

### Web research files (Phase 4; 2 files)

| # | Topic | Rationale |
|---|---|---|
| **web-01** | Multi-stage QA gate design patterns + adversarial-axis taxonomies (drift / contradictions / omissions / weakened-criteria / invented-content) | PR-07's 5-axis naming is borrowed from a recognized adversarial-review pattern; TDD §21 must show prior art |
| **web-02** | Monotonicity guards in retry/fix-loop control + dedup-key strategies | PR-02's `F_{n+1} >= F_n` guard and INV-012 dedup-key composition are standard control-loop patterns; TDD §6.4 must cite prior art |

### Synthesis files (Phase 5; 10 files mapped to TDD template sections)

| # | Synthesis topic | Target TDD sections | Source research files |
|---|---|---|---|
| **synth-01** | Executive Summary + Problem Statement + Goals/Non-Goals + Success Metrics | §1, §2, §3, §4 | 00, 14, 15 |
| **synth-02** | Technical Requirements (functional + non-functional) | §5 | 00, 08, 09, 10, 11, 12, 13, 14 |
| **synth-03** | Architecture (4-stage gate topology + 6-FR landing topology + design decisions) | §6 | 01, 02, 03, 04, 05, 06, 07, 14 |
| **synth-04** | Data Models (5 schemas: Execution Context, Inherited Verdict, Synthetic DNSP, Per-Item 5-field, Phase Contract) | §7 | 15, 08, 09, 10, 11, 12, 13 |
| **synth-05** | API Specifications (rf-qa → rf-qa-qualitative phase contract + per-FR emit contracts) | §8 | 03, 04, 10, 12, 13, 15 |
| **synth-06** | Error Handling, Security, Observability, Testing Strategy | §12, §13, §14, §15 | 03, 04, 05, 07, 12, 13 |
| **synth-07** | Dependencies + Migration & Rollout Plan + Risks (K-001..K-010) + Alternatives | §18, §19, §20, §21 | 00, 02, 14 + web-01, web-02 |
| **synth-08** | Open Questions, Timeline, Release Criteria, Operational Readiness, Cost | §22, §23, §24, §25, §26 | 00, 06, 07, 12 |
| **synth-09** | References & Glossary | §27, §28 | 00, 01, 02 + web-01, web-02 |
| **synth-10** | TDD-specific conditional sections: §9 State Management (N/A), §10 Component Inventory (N/A — internal framework, no UI), §11 User Flows (agent-operator only — see PRD §16.1), §16 Accessibility (N/A), §17 Performance Budgets (token-cost only) | §9, §10, §11, §16, §17 | 00, 14 |

### Analyst + QA gate reports

- `qa/analyst-report-research.md` (Phase 3 — rf-analyst research completeness)
- `qa/qa-report-research.md` (Phase 3 — rf-qa research gate)
- `qa/analyst-report-synthesis.md` (Phase 5 — rf-analyst synthesis review)
- `qa/qa-report-synthesis.md` (Phase 5 — rf-qa synthesis gate)
- `qa/qa-report-assembly.md` (Phase 6 — rf-qa structural validation)
- `reviews/qa-qualitative-final.md` (Phase 6 — rf-qa-qualitative TDD-qualitative phase)

---

## SUGGESTED_PHASES

### Phase 1: Preparation (3 items)
- 1.1: Read TDD template at `src/superclaude/examples/tdd_template.md` and confirm 28-section schema
- 1.2: Read PRD at `.dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md` and confirm 6-FR + 10-NFR + 5-invariant + G6-rule scope
- 1.3: Confirm Heavyweight tier (target 1,400-2,200 lines) and conditional-section selections

### Phase 2: Deep Investigation (16 parallel codebase agents)
- Spawn 16 agents in parallel per "Recommended Outputs" table above. Each agent receives a single research topic + assigned files + output path + zero-trust adversarial stance + line-citation requirement.

### Phase 3: Completeness Verification (2 parallel agents, partitioned)
- 3.1: rf-analyst completeness verification (8 files per partition recommended given 16 research files) → `qa/analyst-report-research.md`
- 3.2: rf-qa research gate (parallel with 3.1; same partition strategy) → `qa/qa-report-research.md`
- Both must PASS before Phase 4. On FAIL, gap-fill cycle (max 2 rounds).

### Phase 4: Web Research (2 parallel agents)
- 4.1: Adversarial-axis taxonomies + multi-stage QA gate design patterns → `research/web-01-adversarial-taxonomies.md`
- 4.2: Monotonicity-guard patterns + dedup-key strategies in retry control → `research/web-02-monotonicity-patterns.md`

### Phase 5: Synthesis + QA Synthesis Gate (10 synthesis agents + 2 verification agents)
- 5.1–5.10: Spawn 10 synthesis agents in parallel per "Synthesis files" table above
- 5.11 (parallel with itself): rf-analyst synthesis review → `qa/analyst-report-synthesis.md`
- 5.12 (parallel with 5.11): rf-qa synthesis gate → `qa/qa-report-synthesis.md`

### Phase 6: Assembly (3 sequential items)
- 6.1: rf-assembler reads all 10 synthesis files + TDD template + writes `TDD_TASK_BUILDER_CONVERGENCE.md` to `.dev/releases/current/task-builder-merge/`
- 6.2: rf-qa structural validation against TDD template (28-section completeness + frontmatter + line-citation accuracy) → `qa/qa-report-assembly.md`
- 6.3: rf-qa-qualitative TDD-qualitative content review (14-item checklist per rf-qa-qualitative.md:255-292) → `reviews/qa-qualitative-final.md`

### Phase 7: Present to User & Complete Task (2 items)
- 7.1: Present final TDD path + summary of artifacts + offer PRD-to-TDD traceability matrix
- 7.2: Move task folder from `.dev/tasks/to-do/` to `.dev/tasks/done/`; update task-frontmatter status to `completed`

---

## TEMPLATE_NOTES

**Template: 02 (Complex Task)** — TDD creation inherently requires discovery before building, parallel subagent spawning, multiple phases (research → synthesis → assembly → review), and conditional flows based on findings. The skill's own decision rule ("for TDD creation, the answer is almost always Template 02") applies unambiguously here.

**Conditional template sections to mark N/A in the assembled TDD (with brief rationale per template guidance):**

| Section | Disposition | Rationale |
|---|---|---|
| §9 State Management | N/A | Internal framework component; no client-side state |
| §10 Component Inventory | N/A | No frontend UI; agent-operator interaction only (PRD §16.1) |
| §16 Accessibility Requirements | N/A | Plain-text logs only; no UI surface (PRD §16.2) |
| §6.5 Multi-Tenancy Architecture | N/A | Single-tenant internal framework |
| §13.4 Data Governance & Compliance | N/A | No PII; no new data collected/stored/transmitted (PRD §17) |
| §14.6 Business Metric Instrumentation | N/A | Internal framework — no user-facing business metrics |
| §17 Performance Budgets | Reduced | Token-cost budget only (NFR-CONV.4 ≤10%); no frontend/backend RPS metrics |
| §25 Operational Readiness — Capacity Planning | N/A | No infrastructure scaling concerns |
| §26 Cost & Resource Estimation | Reduced | LLM token-cost only (per NFR-CONV.4); no infrastructure $$$ |

**Sections requiring deep population:** §1 Exec Summary, §2 Problem & Context, §3 Goals/Non-Goals, §4 Success Metrics, §5 Technical Requirements (heaviest — 6 FRs × 3-field AC + 10 NFRs), §6 Architecture (heaviest — 4-stage gate topology + 6-FR landing topology), §7 Data Models (5 schemas), §8 API Specifications (phase contracts), §12 Error Handling, §13 Security (minimal — anti-inflation rule treatment), §14 Observability (telemetry per PRD §19.3), §15 Testing Strategy (synthetic-fixture catalogue), §18 Dependencies, §19 Migration & Rollout (per-FR landing order + rollback dependency matrix), §20 Risks (K-001..K-010), §21 Alternatives (5 alternatives including Do Nothing), §22 Open Questions (6 entries), §23 Timeline, §24 Release Criteria, §25 Operational Readiness (runbook for K-003 audit + DNSP triage), §27 References, §28 Glossary.

---

## AMBIGUITIES_FOR_USER

None of the user's intent is ambiguous. The PRD is comprehensive, the output location is specified, and the tier is unambiguously Heavyweight. However, two design questions remain that are **TDD-internal**, not user-intent ambiguities — these will be captured in the TDD's §22 Open Questions and surfaced to the user at Phase 7:

1. **TDD-internal Q1**: Should the TDD's §25 Operational Readiness include a runbook entry for the K-003 first-5-runs audit (Self-Audit listings on rf-qa-qualitative output post-FR-CONV.3)? Recommendation: **yes** — operational readiness is exactly where audit-on-merge protocols belong.
2. **TDD-internal Q2**: Should the TDD's §19 Migration & Rollout enumerate the per-FR rollback dependency matrix (release-spec.md §9 SP-10) inline, or reference it externally? Recommendation: **enumerate inline** — TDD is an engineering specification; external references that govern rollback decisions belong in the spec body.

No `[CODE-CONTRADICTED]` or `[UNVERIFIED]` findings from scope discovery. All PRD line-number citations either match current source exactly OR have a ≤3-line offset that the deep-investigation phase will normalize.
