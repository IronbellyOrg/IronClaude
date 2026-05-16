---
spec_source: TDD_TASK_BUILDER_CONVERGENCE.compressed.md
generated: 2026-05-15T05:32:30Z
generator: requirements-design-extraction-agent
functional_requirements: 6
nonfunctional_requirements: 11
total_requirements: 17
complexity_score: 0.7
complexity_class: HIGH
domains_detected: [backend, testing, devops, documentation, agent-framework, qa]
risks_identified: 10
dependencies_identified: 10
success_criteria_count: 8
extraction_mode: standard
data_models_identified: 5
api_surfaces_identified: 5
components_identified: 6
test_artifacts_identified: 25
migration_items_identified: 7
operational_items_identified: 7
pipeline_diagnostics: {elapsed_seconds: 269.2, started_at: "2026-05-15T05:32:03.914014+00:00", finished_at: "2026-05-15T05:36:33.113215+00:00"}
---

## Functional Requirements

### FR-CONV.1 — Structural Gate Additions (TB-Add-1..8)
Append 8 structural checks (TB-Add-1..8) to rf-qa's task-integrity gate, mirrored across rf-qa.md 20-item checklist (`rf-qa.md:268-287`), SKILL.md A.10 9-item block (`SKILL.md:~898-906`), and SKILL.md 15-item validation block (`SKILL.md:~1491-1507`). **CASE D. Protected invariant: zero-trust QA.** Priority: Must Have (P0).

**TB-Add catalogue:**
- TB-Add-1: Placeholder scan (Hard)
- TB-Add-2: Item-count bounds ≥3/≤40-track/≤50-single-track ([ADVISORY] until calibration)
- TB-Add-3: Clarification adjacency (Hard)
- TB-Add-4: Circular-dependency DAG check (Hard)
- TB-Add-5: Granularity / XL-has-subtasks (Hard)
- TB-Add-6: Confidence/Verification format consistency (Hard)
- TB-Add-7: Execution-Context source-areas reappear in items (Hard)
- TB-Add-8: Per-item Context field ≥1 file:line citation OR justified-absence (Hard; resolves INV-015)

**Acceptance (Given/When/Then):** Given a generated MDTM file submitted to rf-qa A.10; When any of TB-Add-1/3/4/5/6/7/8 detects a violation; Then a distinct item-ID-naming error emits and gate verdict is FAIL. TB-Add-2 emits `[ADVISORY]` and does NOT block.

**Verification:** `grep -nE "TB-Add-[1-8]"` returns ≥3 hits per ID across three definition sites; synthetic fixture with placeholder-titled item fires TB-Add-1.

**Negative:** No existing rf-qa check renamed/renumbered/removed; bundle-specific `/sc:tasklist` checks (phase-file naming, checkpoint emission, R-### roadmap traceability) MUST NOT appear in any TB-Add.

### FR-CONV.2 — Execution Context Header
Insert task-level `## Execution Context` block in generated MDTM files (after frontmatter, before checklist) with exactly three labeled lines: References / Source areas / Key constraints. **CASE D. Protected invariant: evidence-bound-item.** Priority: Must Have (P0).

**Acceptance:** Given BUILD_REQUEST with GOAL+WHY+related_docs; When rf-task-builder generates the task file; Then `## Execution Context` emits with 3 labeled lines placed after `## Prerequisites & Dependencies` and before `## Phase 1`. Minimal BUILD_REQUEST → References-only degradation; other two lines explicitly omitted.

**Verification:** `grep -n "## Execution Context"` returns line N; next 10 lines contain ≥1 of `References:`/`Source areas:`/`Key constraints:`; `grep -E "src/|/.*:[0-9]+"` against header range returns ZERO hits.

**Insertion sites:** SKILL.md:1407-1487 (primary template), SKILL.md:715-725 (prompt guidance), SKILL.md:~139, SKILL.md:~86.

**Negative:** Per-item Context fields MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8); per-item self-contained 5-field schema MUST NOT be altered.

### FR-CONV.3 — Inherited Structural Verdict (Gate Results Passthrough)
Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt under `## Inherited Structural Verdict`, with directive "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality." Add `## Self-Audit` to rf-qa-qualitative output schema. **CASE B. Invariant alignment: zero-trust QA.** Priority: Must Have (P0).

**Acceptance:** Given rf-qa A.10 has emitted verdict; When orchestrator spawns rf-qa-qualitative at A.10.5; Then spawn prompt contains `## Inherited Structural Verdict` with rf-qa Items Reviewed table byte-for-byte plus directive. On fix-cycle re-run, orchestrator re-reads/re-injects NEW (cycle-N) verdict (INV-002). rf-qa-qualitative output contains `## Self-Audit` listing relied-on PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019).

**Verification:** `grep -n "## Inherited Structural Verdict"` returns line N; block below diffs identically against `${TASK_DIR}qa/qa-task-integrity.md`.

**Insertion sites:** SKILL.md:923-1000 (A.10.5 spawn prompt; ~:966), rf-qa-qualitative.md:794 (EOF append).

**Negative:** rf-qa-qualitative MUST NOT mark any item VERIFIED solely from inherited verdict; anti-inflation rule at rf-qa-qualitative.md:766-775 MUST NOT be weakened, removed, or rephrased.

### FR-CONV.4 — Five Adversarial Axes
Insert `### Five Adversarial Axes` header subsection BEFORE rf-qa-qualitative 15-item task-qualitative checklist, add `axis` column to Items Reviewed table. Five axes: drift / contradictions / omissions / weakened-criteria / invented-content (plus `none` sentinel). **CASE D. Protected invariant: zero-trust QA.** Priority: Must Have (P0).

**Acceptance:** Given rf-qa-qualitative runs task-qualitative phase; When it produces output; Then `### Five Adversarial Axes` subsection renders BEFORE the 15-item checklist, Items Reviewed table carries populated `axis` column with one value from {drift, contradictions, omissions, weakened-criteria, invented-content, none}. When no checklist item restates BUILD_REQUEST.GOAL verbatim, report emits `drift-axis-inactive` annotation in Summary block.

**Verification:** `grep -n "### Five Adversarial Axes" src/superclaude/agents/rf-qa-qualitative.md` returns ≥1 match.

**Insertion sites:** rf-qa-qualitative.md:527-583 (body unmodified; header before `#### Checklist (15 items)`); rf-qa-qualitative.md:675-714 (insert `axis` column between `Check` and `Result`); SKILL.md:961.

**Negative:** 15-item checklist MUST NOT be removed/reordered/renamed/replaced; severity floor at rf-qa-qualitative.md:786-795 MUST NOT be weakened; no axis introduces new conditional code path (overlay-only).

### FR-CONV.5 — Retry Monotonicity Guards
Add two stop-conditions to EXISTING fix-cycle retry loops (no new loop/stage): (1) Monotonicity guard — HALT if `|F_{n+1}|>=|F_n|`; (2) Regression detection — HALT if any item PASS@N is FAIL@N+1. **Precedence: Regression > monotonicity.** **CASE D. Protected invariant: zero-trust QA.** Priority: Must Have (P0).

**Acceptance:** Given fix-cycle transition N→N+1; When any item PASS at N flips to FAIL at N+1; Then loop emits verbatim `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` and exits BEFORE monotonicity check. When no regression but `|F_{n+1}|>=|F_n|`; Then loop emits `[HALT-MONOTONICITY]|F|=<n>` and exits. Synthetic-dnsp with identical dedup-key across cycles → no halt (dedup recognized, not regression — INV-012).

**Verification:** 3-cycle fixture with `|F|=5,5,5` halts at cycle 2 with `[HALT-MONOTONICITY]|F|=5`; 2-cycle fixture with Item 2.3 PASS@1/FAIL@2 halts with verbatim regression message regardless of `|F_2|<|F_1|`.

**Insertion sites:** SKILL.md:867-873 (A.9 separate-counters tail), SKILL.md:1547-1553 (Behavioral Constraints), rf-task-builder.md:334-361 (QA-gate fix-cycle encoding), rf-qa.md:~308-315 (Fix Cycle Protocol).

**Negative:** Legitimate slow-cycle correction MUST NOT halt (strict `|F|` shrink continues); four independent retry counters MUST NOT be collapsed; no halt-on-slow-convergence threshold (X-003 REJECTED). Existing 3-cycle hard cap at rf-team-lead.md:417 and per-gate fix-cycle table at rf-task-builder.md:354-360 preserved unchanged.

### FR-CONV.6 — DNSP Synthetic Finding
After a partition agent's entire escalation ladder exhausts (rf-analyst, rf-qa, or rf-qa-qualitative partition), emit synthetic HIGH-severity finding (`source: "synthetic-dnsp"`) into agent's output stream rather than silently aborting gate. Dedup key: `(assigned_files_range, escalation_ladder_exhaust_point)`. **CASE B. Invariant alignment: zero-trust QA + evidence-bound-item + parallel-research.** Priority: Must Have (P0).

**Acceptance:** Given ≥1 partition agent succeeded AND ≥1 partition agent's escalation ladder exhausted; When exhaust occurs; Then exhausted agent emits JSON-or-block finding with all 5 fixed fields (`severity: HIGH`, `source: "synthetic-dnsp"`, `affected_range`, `evidence`, `recommendation: "Manual review required — partition agent failed twice"`) plus `dedup_key` and `found_n_times`. Two synthetic findings with identical dedup-key collapse to one record with `found N times`. When zero partition agents succeeded; Then NO synthetic emits and existing all-agents-fail escalation runs (rf-team-lead.md:417).

**Verification:** Twice-timeout partition fixture produces synthetic-dnsp finding with all 5 fields; two identical-exhaust events collapse to one with `found N times`; `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns ≥1 hit per file.

**Insertion sites:** SKILL.md:572-656 (A.8 Research Quality Gate), SKILL.md:870-918 (A.10 Task File Validation), rf-analyst.md:58-71, rf-qa.md:49-77 + :70-77, rf-qa-qualitative.md:70-80.

**Negative:** synthetic-dnsp MUST NOT emit before escalation ladder exhausts; rf-team-lead.md:417 MUST NOT be replaced or short-circuited (NO DRIFT verified); HIGH severity ensures gate visibility (no masking); dedup-key collapse MUST NOT cross-cycle (INV-012).

**Cross-FR dependency chain:** FR-CONV.1 → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6 (strict serial; FR-CONV.5 ↔ FR-CONV.6 mutual reference resolved by landing order — 5 specifies dedup-key shape, 6 emits that shape).

## Non-Functional Requirements

### Performance
- **NFR-CONV.4** — Token-cost ratio (post-merge / pre-merge) ≤1.10 per equivalent BUILD_REQUEST. Measurement: 5 representative BUILD_REQUESTs across Quick/Standard/Deep tiers. Contingency K-010: summarise FR-CONV.3 verdict table if exceeded.
- **NFR-CONV.5** — Wall-clock: no new external dependencies, no synchronous network calls; gate additions are local checks using only Read, Grep, Glob, Bash.

### Reliability
- **NFR-CONV-R1** — Single-pass gate PASS rate ≥80% of representative BUILD_REQUESTs on first cycle.
- **NFR-CONV.3** — Hidden-input determinism: fixture-populated `.dev/tasks/done/` produces byte-identical structural output to empty `.dev/tasks/done/`. PR-05 advisory mechanism REJECTED for Phase-1.

### Determinism SLOs
- **NFR-CONV.1** — Structural fields (TB-Add-1..8 PASS/FAIL verdicts, synthetic-dnsp 5 fixed fields + dedup-key, axis column values, Items Reviewed table structure) byte-identical across two runs on same BUILD_REQUEST + source tree.
- **NFR-CONV.2** — Research-driven prose explicitly excluded from determinism scope; per-item Context prose and rf-qa-qualitative semantic-check prose remain LLM-driven. Structural annotations within prose (axis labels, finding counts, dedup-keys) MUST remain byte-equal.

### Security (Invariant Preservation)
- **NFR-CONV.6** — self-contained-item invariant. Source: SKILL.md:~1452-1457. Fixture: 5-field schema passes all 8 TB-Add; one field stripped → FAILS TB-Add-1 (fail-closed). **OPEN: SC-1/Q-DM-1 schema contradiction.**
- **NFR-CONV.7** — evidence-bound-item invariant. Source: SKILL.md:1530 rule #2. Fixture triple: bare `Context: src/foo` FAILS TB-Add-8; `src/foo:42` PASSES; justified-absence PASSES.
- **NFR-CONV.8** — persistent-`.dev/tasks/`-artifact invariant. Source: SKILL.md:1536 rule #5. Fixture: diff `.dev/tasks/<task-id>/` layout pre-merge vs post-merge → zero structural changes.
- **NFR-CONV.9** — zero-trust QA invariant. Source: rf-qa.md:141-142 (verbatim PASS/FAIL definitions). Fixture: (a) 1-LOW-finding fixture → gate FAILS; (b) FR-CONV.3 inherited-verdict → no item VERIFIED unless Self-Audit lists independent semantic-check engagement.
- **NFR-CONV.10** — parallel-research invariant. Source: rf-qa.md:49-77 + rf-qa-qualitative.md:50-82. INV-021: DNSP fires within-agent-instance. Fixture: N partition agents spawn concurrently; on one agent's escalation exhaust, N-1 partitions continue to completion before that one synthesises DNSP finding.

## Complexity Assessment

**complexity_score: 0.7**
**complexity_class: HIGH**

**Rationale:**
- 6 strictly-additive FRs landing in serial order across 5 source files (SKILL.md 1709 lines, rf-qa.md 432 lines, rf-qa-qualitative.md 794 lines, rf-analyst.md 349 lines, rf-task-builder.md 493 lines)
- Cross-FR dependency chain with mutual reference between FR-CONV.5 ↔ FR-CONV.6 requiring strict landing order
- Five load-bearing invariants must be provably preserved via NFR-CONV.6..10 synthetic fixtures
- G6 four-case conflict rule classification per FR (4 CASE-D, 2 CASE-B)
- One CRITICAL open contradiction (SC-1 / Q-DM-1) blocking FR-CONV.1 implementation
- Heavyweight TDD tier (all 28 sections completed)
- Three-paradigm rigor mechanism: structural gate (FR-CONV.1) + inter-agent verdict channel (FR-CONV.3/4) + retry/exhaust resilience (FR-CONV.5/6)
- Token-cost ceiling NFR-CONV.4 ≤10% adds optimization pressure
- 25 synthetic test fixtures required for AC coverage

## Architectural Constraints

1. **A-001 Sync Discipline** — `src/superclaude/` is source-of-truth; `make sync-dev` propagates to `.claude/`; `make verify-sync` MUST PASS before commit per K-009.
2. **A-002 Strictly-Additive Governance** — No existing rf-qa check, rf-qa-qualitative checklist item, gate stage, output field, or `.dev/tasks/` layout entry may be renamed, renumbered, or removed.
3. **G6 Four-Case Conflict Rule** — Authoritative tiebreaker for sc-tasklist ↔ task-builder mechanism conflicts (CASE A/B/C/D); conflict-register row required for CASE-A and CASE-D.
4. **Five Load-Bearing Invariants** — self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research; preserved or strengthened, never weakened.
5. **Per-FR Rollback Granularity** — Each FR a single revertable append line per K-001/K-005; co-revert matrix in §19.4 (FR-CONV.5↔FR-CONV.6 jointly revertable; FR-CONV.1→FR-CONV.3 co-revert; FR-CONV.2/FR-CONV.4 independent).
6. **Strict Serial Landing Order** — PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 enforced per release-spec.md §4.6 (K-007 mitigation).
7. **Intent-Port over Implementation-Port** — Adapt sc-tasklist *intent*, not implementation, per FINAL-REPORT §6.3 asymmetric finding.
8. **Per-Check Classification (CB-3)** — Import only 8 unique TB-Add checks, not bulk-port all 17/20 sc-tasklist Stage-6 checks.
9. **Tool Constraint** — Only existing tools permitted: Read, Grep, Glob, Bash (NFR-CONV.5).
10. **Hidden-Input Determinism Guard** — task-builder MUST NOT read any input outside BUILD_REQUEST + source-tree (NFR-CONV.3).
11. **Anti-Inflation Rule Absolute** — rf-qa-qualitative.md:766-775 Prohibited Behaviors block MUST be byte-stable.
12. **All-Agents-Fail Guard Precedence** — DNSP emits only when ≥1 succeeded AND ≥1 exhausted; zero-success falls through to rf-team-lead.md:417 (NO DRIFT preserved).
13. **`.dev/tasks/` Layout Stability** — SP-33 stability commitment; layout change forces re-integration of all 6 FRs (K-008).

**Persona-Driven Design Requirements (from PRD §7):** Three internal personas drive design — rf-task-builder (primary), rf-qa (secondary), rf-qa-qualitative (tertiary). All gate additions designed for prompt-driven deterministic execution; no human-UI personas exist; anti-personas: `/sc:tasklist` end users, downstream sprint executors, `.dev/tasks/` directory consumers expecting layout changes.

**Scope Boundaries (from PRD §12):** Out-of-scope explicit — bulk-port of 17 sc-tasklist checks (REJECTED CB-3), tier selection via historical pattern (REJECTED X-004), replacing 15-item rf-qa-qualitative checklist (REJECTED X-002), PR-05 Tier-History Advisory (Phase-2 deferred), roadmap regeneration, `.dev/tasks/` layout changes.

## Risk Inventory

1. **K-001 (Low/Low):** TB-Add false positives waste fix-cycles. Mitigation: each TB-Add cites source-check-ID; TB-Add-2 [ADVISORY]; individually revertable. Contingency: disable specific TB-Add line.
2. **K-002 (Low/Low):** Execution Context header drift (header vs items). Mitigation: TB-Add-7 cross-validates; gate fails on drift; header optional fallback to References-only.
3. **K-003 (Low/Medium):** PR-04 passthrough causes inflation despite anti-inflation rule. Mitigation: INV-019 Self-Audit listing; X-002 audit-target for first 5 rf-qa-qualitative runs. Contingency: disable passthrough.
4. **K-004 (Low/Low):** 5-axis annotation ambiguity over-flags items. Mitigation: axes annotation-only; 15-item checklist still runs; severity floor preserved; `drift-axis-inactive` annotation. Contingency: audit axis distribution; tune rules.
5. **K-005 (Low/Low):** Retry monotonicity halts legitimate slow-cycle correction. Mitigation: strict-shrink threshold; X-003 REJECTED. Contingency: disable guards individually.
6. **K-006 (Low/Low):** Synthetic-dnsp findings mask real issues. Mitigation: HIGH severity ensures visibility; all-agents-fail guard preserved; dedup-key prevents over-emission. Contingency: weekly emission-count metric inspection.
7. **K-007 (Low/Medium):** PR-04 + PR-06 sequencing inversion. Mitigation: serial enforcement in release-spec §4.6; INV-010 dynamic enumeration auto-richens. Contingency: re-merge in correct order.
8. **K-008 (Low/HIGH):** INV-018 `.dev/tasks/` directory layout changes invalidate all proposals. Mitigation: SP-33 stability commitment; portfolio-wide note. Contingency: re-integration commit covering all 6 FRs.
9. **K-009 (Low/Medium):** Sync-discipline (A-001) violated; `.claude/` edited directly without `make verify-sync`. Mitigation: CLAUDE.md mandates workflow; `make verify-sync` MUST pass pre-commit. Contingency: revert `.claude/` direct edit; re-run from `src/superclaude/`.
10. **K-010 (Low/Low):** Token ceiling NFR-CONV.4 exceeded by >10%. Mitigation: empirical post-merge measurement; per-FR profiling. Contingency: FR-CONV.3 verdict-table summarisation.

**Risk Profile:** 10 risks, all LOW probability. Impact: 6 LOW, 3 MEDIUM (K-003, K-007, K-009), 1 HIGH (K-008). Every risk has both mitigation and contingency.

## Dependency Inventory

**External:** NONE (NFR-CONV.5 forbids new external dependencies).

**Internal (10 dependencies):**
1. `release-spec.md` v1.0.0 — defines §4.6 landing order, §9 SP-10 rollback matrix, §8.3 audit rows
2. `conflict-register.md` — 5 CASE-D rows (PR-01, PR-02, PR-06, PR-07, PR-05-deferred)
3. `invariant-probe.md` — INV-002, INV-010, INV-012, INV-015, INV-019, INV-021 Round-2.5 findings
4. `FINAL-REPORT.md` §6.3 — asymmetric finding (5 ADOPT-grade qualities, inverse direction)
5. `FINAL-REPORT.md` §6.2 F2/F4 — 21-retry oscillation + hidden-input over-engineering empirical motivation
6. `rf-team-lead.md:417` — 3-fix-cycle escalation (VERIFIED NO-DRIFT 2026-05-14)
7. `rf-qa.md:141-142` — zero-trust verdict (verbatim PASS/FAIL)
8. `task-builder/SKILL.md:~1452-1457` — per-item schema (⚠ SC-1 CRITICAL DRIFT FLAGGED — Q-DM-1)
9. `.dev/tasks/` directory layout (INV-018, SP-33 stability commitment)
10. `make sync-dev` / `make verify-sync` pipeline (A-001 discipline tooling)

**Infrastructure:** NONE — no database, message queue, compute allocation, or deployment target.

## Success Criteria

**Technical (6):**
1. Single-pass gate PASS rate ↑ post-merge (baseline ≥80%)
2. Placeholder-defect detection rate 100% on synthetic fixtures (TB-Add-1)
3. DAG-cycle detection rate 100% on synthetic fixtures (TB-Add-4)
4. Self-Audit coverage post-FR-CONV.3 100% on first 5 runs (K-003 audit target)
5. `[HALT-MONOTONICITY]` emission rate <10% (>50% alerts upstream BUILD_REQUEST defect)
6. Synthetic-dnsp emission count ≥1 on twice-exhaust fixture; 0 on healthy run

**Business (2):**
7. Token-cost ratio post-merge / pre-merge ≤1.10 (NFR-CONV.4) on 5 representative BUILD_REQUESTs
8. Fix-cycle convergence rate ≥75% baseline, expected ↑ post-merge

**Additional from PRD §19 (cross-reference):**
- Phase-2 PR-05 re-evaluation trigger: `.dev/tasks/done/TASK-RF-*` ≥10 with ≥3 distinct task_types
- Regression-halt emission count <5% (>20% alerts fix-cycle introducing new defects)
- `make verify-sync` PASS rate 100% per A-001

## Open Questions

| ID | Question | Owner | Status |
|---|---|---|---|
| **Q-DM-1** | **SC-1 CRITICAL:** PRD §25.4 declares per-item 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` "preserved unchanged" at `SKILL.md:1452-1457`, but current SKILL.md:1450-1460 holds `{Context, Action, Output, Verification, Completion gate}`. Three resolution options listed in §7.1 Entity 4. Engineering Lead decision REQUIRED before FR-CONV.1 implementation. | Engineering Lead | 🔴 OPEN — synthesis-blocking |
| OPEN-PR05 | When does `.dev/tasks/done/` reach ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05? | Engineering Lead | 🟡 Tracked |
| OPEN-INV-006 | Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 / ≤50) | Engineering | 🔴 OPEN — TB-Add-2 stays [ADVISORY] until calibrated |
| OPEN-INV-017 | Historical-file staleness check for PR-05 advisory citations | Engineering | 🟡 Deferred (academic given PR-05 Phase-2 deferral) |
| OPEN-INV-018 | If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration | Engineering Lead | 🔴 OPEN — document layout-change contract |
| OPEN-X-002 | PR-04 anti-inflation operational test — "reliance ≠ verification" empirically observable, not structurally provable | QA Lead | 🔴 OPEN — K-003 audit-target |
| OPEN-TOKEN | NFR-CONV.4 token-ceiling empirical measurement | Engineering Lead | 🔴 OPEN — post-merge measurement |

**Resolved within TDD body:**
- Q-DM-2: Per-FR rollback dependency matrix inline (§19.4) — RESOLVED
- Q-DM-3: Five Adversarial Axes canonical definitions in §8.5 — RESOLVED
- Q-DM-4: Per-gate fix-cycle limits authority — rf-task-builder.md I16 authoritative; rf-qa.md max=3 layered — RESOLVED

**JTBD coverage (from PRD §6):** Three primary jobs (detect structural defects, pass verdict between agents, halt retry loops) — all mapped to corresponding FRs (FR-CONV.1/3/5+6). No JTBD lacks FR coverage.

## Data Models and Interfaces

### DM-001 — Execution Context Header
**Producer:** FR-CONV.2 (PR-01) via rf-task-builder. **Location:** MDTM file, after frontmatter / `## Prerequisites & Dependencies`, before first `## Phase N:`. **Source:** PRD §25.1.

| Field | Type | Required | Constraints |
|---|---|---|---|
| `References` | list[string] | Yes | Each `"R-###: <ref-line>"` |
| `Source areas` | list[string] | Yes (omitted under degradation) | **NEVER file paths or file:line citations** (hidden-input determinism) |
| `Key constraints` | list[string] | Yes, 1–3 items (omitted under degradation) | Top invariants verbatim from BUILD_REQUEST |

**Degradation:** Minimal BUILD_REQUEST → References-only; other two lines explicitly omitted (not blank-but-present). TB-Add-7 cross-validates each `Source areas` entry reappears in ≥1 per-item Context field.

### DM-002 — Inherited Structural Verdict Block
**Producer:** FR-CONV.3 (PR-04) via task-builder orchestrator at A.10.5. **Source:** PRD §25.2.

| Field | Type | Required | Constraints |
|---|---|---|---|
| `rf_qa_table_verbatim` | string / markdown | Yes | Byte-exact copy of rf-qa task-integrity Items Reviewed table + Overall Verdict + Summary counts |
| `prompt_directive` | string | Yes | Fixed: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality." |
| `reinjection_rule` | string | Yes | Fixed: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden." |

**Governing rules:** freshness_rule (INV-002 cycle-N+1 reinjection), enumeration_rule (INV-010 dynamic checklist), consumer_obligation (INV-019 Self-Audit), anti_inflation (rf-qa-qualitative.md:766-775 MUST NOT weaken).

### DM-003 — Synthetic DNSP Finding
**Producer:** FR-CONV.6 via any partition agent (rf-analyst / rf-qa / rf-qa-qualitative). **Source:** PRD §25.3.

| Field | Type | Required | Constraints |
|---|---|---|---|
| `severity` | enum | Yes | **Fixed = HIGH** — non-overridable |
| `source` | string | Yes | **Fixed = "synthetic-dnsp"** — literal grep-able sentinel |
| `affected_range` | string | Yes | Verbatim copy of partition's `assigned_files` slice |
| `evidence` | string | Yes | Spawn-log path OR explicit stub citing log absence; never blank |
| `recommendation` | string | Yes | Fixed: "Manual review required — partition agent failed twice" |
| `dedup_key` | tuple (2-tuple) | Yes | Composite: `(assigned_files_range, escalation_ladder_exhaust_point)`; canonical YAML list `["<range>", "<exhaust_point>"]`. `escalation_ladder_exhaust_point` closed vocabulary: `{"retry-1", "retry-2", "gap-fill-round-1", "gap-fill-round-2", "gap-fill-round-3"}` |
| `found_n_times` | int | Yes | Default 1; increments by 1 on each within-cycle dedup collapse |

**Composition (INV-012):** Synthetic-dnsp contributes `1` to `|F_n|` like real findings; identical dedup-key across consecutive cycles is dedup, NOT regression. All-agents-fail guard precedence: zero successes → no emit, rf-team-lead.md:417 escalation runs instead.

### DM-004 — Per-Item Checklist Schema ⚠ CRITICAL DRIFT (SC-1 / Q-DM-1)
**Source:** PRD §25.4 declared as NFR-CONV.6 operational source. **STATUS: PRD-vs-SKILL.md contradiction unresolved.**

**PRD-asserted schema (target / contract):**
| Field | Type | Required | Constraints |
|---|---|---|---|
| `Description` | string | Yes | Imperative voice, single line |
| `Context` | string | Yes | file:line citation OR justified-absence — TB-Add-8 enforced |
| `Acceptance` | string | Yes | Observable success condition |
| `Confidence` | enum {HIGH, MEDIUM, LOW} | Yes | With one-line rationale |
| `Verification` | string | Yes | Command, file inspection, or test |

**Current SKILL.md:1450-1460 (as-built):** `{Context, Action, Output, Verification, Completion gate}` — overlaps PRD-asserted on `Context`, `Verification` only.

**Resolution required before FR-CONV.1 lands.** Three options: (a) FR-CONV.1/TB-Add-8 LANDS the §25.4 schema (would contradict A-002 unless net-new schema); (b) PRD pointer corrected to current schema; (c) §25.4 schema lives elsewhere. **Invariant across all options:** TB-Add-8 applies to `Context` field (present in both).

### DM-005 — Phase Contract: rf-qa → rf-qa-qualitative
**Source:** PRD §25.5. Formalizes FR-CONV.3 handoff as versioned phase contract.

| Field | Type | Required | Constraints |
|---|---|---|---|
| `producer` | string | Yes | Fixed: `rf-qa` |
| `consumer` | string | Yes | Fixed: `rf-qa-qualitative` |
| `artifact` | string | Yes | Fixed: `"## Inherited Structural Verdict block in spawn prompt"` |
| `schema_version` | string | Yes | Fixed: `"1.0.0"` (semver) |
| `delivery_semantics` | string | Yes | Fixed: `"at-most-once-per-cycle"` |
| `freshness_rule` | string | Yes | INV-002 reinjection-on-retry |
| `enumeration_rule` | string | Yes | INV-010 dynamic TB-Add catalogue pickup |
| `consumer_obligation` | string | Yes | INV-019 Self-Audit listing |
| `anti_inflation` | string | Yes | rf-qa-qualitative.md:766-775 preservation |
| `failure_mode` | string | Yes | If rf-qa fails to emit verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5 |

### Data Storage
- MDTM task file → `.dev/tasks/to-do/TASK-*/TASK-*.md` (indefinite, Git VCS)
- Research artifacts → `.dev/tasks/to-do/TASK-*/research/` (indefinite, Git VCS)
- QA reports → `.dev/tasks/to-do/TASK-*/qa/` and `.../reviews/` (indefinite, Git VCS)
- No external datastore, no database, no network-delivered payload

## API Specifications

**No HTTP API.** Five inter-agent contract artifacts exchanged via spawn-prompt fragments and on-disk markdown artifacts under `.dev/tasks/to-do/TASK-*/`.

### API-001 — BUILD_REQUEST → MDTM Task File (FR-CONV.2 modifies output)
**Producer:** task-builder skill orchestrator. **Consumer:** rf-task-builder subagent. **Transport:** Skill-tool prompt; on-disk MDTM file. **Schema:** existing `BUILD_REQUEST` per SKILL.md:1407-1487 + optional `EXECUTION_CONTEXT_REQUIREMENTS`. MDTM file MUST contain `## Execution Context` block (DM-001) after frontmatter, before Phase 1.

**Auth:** N/A (internal subagent spawn). **Rate limits:** N/A. **Error behavior:** If orchestrator cannot derive `References`, MALFORMED return — rf-task-builder MALFORMED retry counter (max 2) governs.

### API-002 — rf-qa task-integrity → rf-qa-qualitative task-qualitative (FR-CONV.3)
**Producer:** rf-qa task-integrity phase (rf-qa.md:259-289). **Consumer:** rf-qa-qualitative task-qualitative phase (rf-qa-qualitative.md:508-603). **Transport:** orchestrator-mediated spawn-prompt injection at SKILL.md §A.10.5 (range 923-1000). **Schema:** DM-005 Phase Contract; injected block follows DM-002.

**Emission rules:**
- rf-qa emits verdict at `.dev/tasks/to-do/TASK-*/qa/qa-task-integrity*.md`
- Orchestrator extracts `## Items Reviewed` table contiguously, splices verbatim into rf-qa-qualitative spawn prompt
- INV-002 cycle-N+1 reinjection enforced
- INV-010 dynamic checklist enumeration (TB-Add catalogue)
- INV-019 Self-Audit mandate (≥1 semantic check)

**Anti-inflation:** rf-qa-qualitative.md:766-775 byte-stable. **Failure mode:** rf-qa no-verdict → rf-qa-qualitative MUST NOT spawn (gate halts at A.10).

### API-003 — Partition Agent → Orchestrator (FR-CONV.6 synthetic-dnsp emission)
**Producer:** any partition instance (rf-qa / rf-analyst / rf-qa-qualitative partition). **Consumer:** task-builder skill orchestrator gate-result merge step at SKILL.md §A.8 and §A.10. **Transport:** structured block in partition agent's normal output stream (no separate channel). **Schema:** DM-003.

**Emission rules:**
- One HIGH-severity synthetic finding (all 7 fields) per partition on escalation-ladder exhaust
- Cardinality per-partition-instance
- Within-cycle dedup collapse (identical dedup_key → `found_n_times` increment)
- INV-021 within-agent-instance emission (cohort does NOT serialize)
- HIGH severity non-overridable

**All-agents-fail precedence (SC-2):** Zero successes → NO synthetic emit; rf-team-lead.md:417 escalation runs.

| Condition | Action |
|---|---|
| ≥1 succeeded AND ≥1 exhausted | Emit synthetic-dnsp per exhausted partition |
| Zero succeeded (all exhausted) | NO synthetic; escalate per rf-team-lead.md:417 |
| All succeeded | No emission — normal gate flow |

### API-004 — Fix-Loop Halt Signals (FR-CONV.5)
**Producer:** rf-task-builder fix-loop + rf-qa fix-cycle protocol. **Consumer:** itself — next-cycle decision logic. **Transport:** halt-message strings in fix-loop verdict stream.

**Halt messages (verbatim — fixtures require character-for-character match):**
- Monotonicity halt: `[HALT-MONOTONICITY] |F|=<n>` (when `|F_{n+1}| >= |F_n|`)
- Regression halt: `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`

**Ordering precedence per cycle n→n+1:**
1. Regression check (R = items PASS@n ∧ FAIL@n+1); if R≠∅ → regression halt, exit
2. Monotonicity check; if `|F_{n+1}| >= |F_n|` → monotonicity halt, exit
3. Existing 3-cycle hard cap (rf-team-lead.md:417, rf-task-builder.md per-gate table)
4. Otherwise proceed to cycle n+2

**F-set definition:** `F_n` = FAIL-verdict items at end of cycle n; item identity is dedup-key; `|F_n|` cardinality after dedup. **INV-012 composition:** synthetic-dnsp counts as failures; identical dedup-key across cycles = dedup, NOT regression (prior verdict was FAIL).

### API-005 — All-Partition-Agents-Fail → rf-team-lead
**Producer:** orchestrator on zero partition success. **Consumer:** rf-team-lead (existing). **Transport:** existing escalation per rf-team-lead.md:417 (3 fix cycles per phase, HALT-and-ask-user). **Schema:** N/A — existing behavior preserved verbatim (FR-CONV.6 Negative Criterion).

### Governance
**Versioning:** schema_version "1.0.0" on Phase Contract (DM-005). **Compatibility:** A-002 strictly-additive landings. Allowed: add optional fields. Forbidden: remove field, rename field, change fixed-value text, change halt message format, change escalation_ladder_exhaust_point vocabulary (additions yes; removals/renames no). **Deprecation:** N/A for v3.9. Frozen surfaces: prompt_directive, halt messages, fixed-value fields.

### Five Adversarial Axes (FR-CONV.4 canonical definitions, §8.5)

| Axis ID | Name | Definition |
|---|---|---|
| AX-1 | Drift | Cited fact no longer matches current source |
| AX-2 | Contradictions | Mutually incompatible assertions in two artifacts/sections |
| AX-3 | Omissions | Required touchpoint/dependency/step absent |
| AX-4 | Weakened criteria | Acceptance softened to unobservable/trivially-satisfiable |
| AX-5 | Invented content | Requirement not present in upstream source |

**Annotation rules:** Every Items Reviewed row carries exactly one Axis from {AX-1..AX-5, none}; `Axis: none` = check passed via axis lens; `Axis: drift-axis-inactive` only when artifact has no citations. Axes multiply lenses, not checks (TOTAL stays at 15 items).

## Component Inventory

### COMP-001 — task-builder/SKILL.md
**Type:** Skill orchestrator (Stage A only, A.1–A.11). **Location:** `src/superclaude/skills/task-builder/SKILL.md` (1709 lines). **Modifying FRs:** FR-CONV.1, FR-CONV.2, FR-CONV.3, FR-CONV.4, FR-CONV.5, FR-CONV.6. **Dependencies:** spawns rf-task-researcher (optional), rf-task-builder, rf-qa, rf-analyst, rf-qa-qualitative.

### COMP-002 — rf-qa.md
**Type:** Structural QA agent (4 phases: research-gate, synthesis-gate, report-validation, task-integrity). **Location:** `src/superclaude/agents/rf-qa.md` (432 lines). **Modifying FRs:** FR-CONV.1 (TB-Add-1..8 append to 20-item checklist at :268-287), FR-CONV.5 (Fix Cycle Protocol Rules at :~308-315), FR-CONV.6 (DNSP edit site at :70-77). **Key anchors:** zero-trust verdict at :141-142.

### COMP-003 — rf-qa-qualitative.md
**Type:** Content QA agent (7 phases incl. task-qualitative). **Location:** `src/superclaude/agents/rf-qa-qualitative.md` (794 lines). **Modifying FRs:** FR-CONV.3 (Inherited Structural Verdict at :794 EOF), FR-CONV.4 (Five Adversarial Axes header before :527, axis column at :675-714), FR-CONV.6 (DNSP at :70-80). **Key anchors:** anti-inflation rule at :766-775; 15-item checklist at :527-583; severity floor at :786-795.

### COMP-004 — rf-analyst.md
**Type:** Completeness-verification + synthesis-review agent (parallel adversary at Gates 1 and 2). **Location:** `src/superclaude/agents/rf-analyst.md` (349 lines). **Modifying FRs:** FR-CONV.6 (DNSP partition protocol at :58-71). **Dependencies:** runs concurrently with rf-qa per NFR-CONV.10.

### COMP-005 — rf-task-builder.md
**Type:** BUILD_REQUEST → MDTM transformation subagent. **Location:** `src/superclaude/agents/rf-task-builder.md` (493 lines). **Modifying FRs:** FR-CONV.5 (QA-gate fix-cycle encoding I16 table at :334-361). **Key contract:** 15-field BUILD_REQUEST schema at :90-99.

### COMP-006 — rf-team-lead.md
**Type:** Project-mode escalation orchestrator. **Location:** `src/superclaude/agents/rf-team-lead.md` (431 lines). **Modifying FRs:** NONE (UNMODIFIED). **Key anchor:** line 417 = 3-fix-cycle HALT (VERIFIED NO-DRIFT 2026-05-14). **Preservation:** FR-CONV.6 Negative Criterion forbids replacement or short-circuit.

**Agent hierarchy (§6.2):** task-builder/SKILL.md (orchestrator) → spawns rf-task-researcher (A.7), rf-task-builder (A.9), rf-qa (A.8/A.10), rf-analyst (A.8/Stage-2), rf-qa-qualitative (A.10.5). rf-qa ↔ rf-analyst parallel adversarial pairing (NFR-CONV.10). rf-team-lead = escalation guard, not directly invoked.

**State management:** N/A — no persistent client state, no global state, no URL state, no form state. Closest analog is on-disk MDTM task file (DM-004) + persistent-`.dev/tasks/`-artifact invariant. Inter-cycle verdict carryover explicitly FORBIDDEN as durable state (INV-002).

## Testing Strategy

**Test pyramid (adapted to agent-instruction text changes):**
| Level | Coverage Target | Tools | Responsibility |
|---|---|---|---|
| Synthetic Fixtures (per-FR) | 100% AC coverage | `uv run pytest` | Engineering |
| Integration Tests | INV-010 + INV-012 + INV-019 composition | Custom multi-FR fixtures | Engineering |
| E2E Tests | Full A.1–A.11 pipeline on realistic BUILD_REQUEST | Custom fixture BUILD_REQUEST | Engineering |
| Manual Audit | K-003 first-5-runs of rf-qa-qualitative | Human review | QA Lead |

### TEST-001 — test_placeholder_tb_add_1 (FR-CONV.1)
Verifies TB-Add-1 fires on "TBD"/"TODO"/title-only checklist item. Input: synthetic MDTM with placeholder item. Expected: TB-Add-1 emits item-ID-naming error; gate FAILs. Mocks: none.

### TEST-002 — test_dag_cycle_tb_add_4 (FR-CONV.1)
Verifies TB-Add-4 fires on circular intra-/inter-phase dependency. Input: synthetic MDTM with circular deps. Expected: TB-Add-4 emits; gate FAILs.

### TEST-003 — test_evidence_bound_tb_add_8 (FR-CONV.1)
Verifies TB-Add-8 fires on bare `Context: src/foo` (INV-015). Inputs: (a) bare path → FAIL; (b) `src/foo:42` → PASS; (c) `<none — pure refactor> [justified-absence]` → PASS.

### TEST-004 — test_execution_context_full (FR-CONV.2)
Verifies 3-labeled-line Execution Context block in generated MDTM. Assertion: grep matches all 3 labeled lines.

### TEST-005 — test_execution_context_minimal_buildrequest (FR-CONV.2)
Verifies minimal BUILD_REQUEST degrades to References-only. Assertion: grep matches degraded References-only form.

### TEST-006 — test_execution_context_no_file_paths (FR-CONV.2)
Verifies `grep -E "src/|/.*:[0-9]+"` against header block returns zero (hidden-input determinism). Assertion: grep returns 0 hits.

### TEST-007 — test_inherited_verdict_present (FR-CONV.3)
Verifies `## Inherited Structural Verdict` block in rf-qa-qualitative spawn prompt. Assertion: grep matches block header.

### TEST-008 — test_inherited_verdict_freshness_inv_002 (FR-CONV.3)
2-cycle fixture verifies cycle-2 spawn shows cycle-2 structural verdict, not stale cycle-1. Assertion: byte-diff of cycle-1 vs cycle-2 spawn prompts.

### TEST-009 — test_self_audit_inv_019 (FR-CONV.3)
Verifies rf-qa-qualitative output contains `## Self-Audit` with ≥1 semantic check beyond inherited verdict. Assertion: grep + content inspection.

### TEST-010 — test_dynamic_enumeration_inv_010 (FR-CONV.3)
Verifies when FR-CONV.1 TB-Add catalogue grows, rf-qa-qualitative checklist auto-richens. Assertion: structural diff of checklist before/after catalogue growth.

### TEST-011 — test_five_axes_overlay (FR-CONV.4)
Verifies `### Five Adversarial Axes` header appears BEFORE immutable 15-item task-qualitative checklist (`rf-qa-qualitative.md:527`). Assertion: grep ordering.

### TEST-012 — test_axis_column_populated (FR-CONV.4)
Verifies Items Reviewed table (:675-714) carries non-empty `Axis` value on every row. Assertion: parse table, no empty `Axis` cell.

### TEST-013 — test_drift_axis_inactive_when_no_goal_baseline (FR-CONV.4)
Verifies no GOAL-baseline item → `drift-axis-inactive` annotation (not N/A). Assertion: grep matches annotation.

### TEST-014 — test_severity_floor_unweakened (FR-CONV.4)
Verifies rf-qa-qualitative severity floor (:786-795) unchanged. Assertion: byte-diff of Critical Rules block.

### TEST-015 — test_monotonicity_halt_F_5_5_5 (FR-CONV.5)
3-cycle `|F|=5,5,5` halts at cycle 2 with `[HALT-MONOTONICITY]|F|=5`. Assertion: grep halt message + no cycle-3 log.

### TEST-016 — test_regression_halt_pass1_fail2 (FR-CONV.5)
Item 3.2 PASS@1/FAIL@2 halts with verbatim regression message BEFORE monotonicity check. Assertion: grep message + ordering.

### TEST-017 — test_slow_shrink_continues (FR-CONV.5)
`|F|=5,4` continues — strict shrink holds; X-003 NOT triggered. Assertion: execution log shows cycle continues.

### TEST-018 — test_dnsp_twice_exhaust (FR-CONV.6)
Twice-timeout partition fixture emits synthetic-dnsp finding with all 5 fixed fields. Assertion: parse YAML, all 5 fields populated.

### TEST-019 — test_dnsp_dedup_collapse (FR-CONV.6)
Two identical-`dedup_key` synthetic findings collapse into one record with `found_n_times=2`. Assertion: parse merged YAML.

### TEST-020 — test_dnsp_all_agents_fail_bypass (FR-CONV.6)
Zero partitions succeeded → no synthetic emit; rf-team-lead.md:417 escalation activates. Assertion: execution log shows HALT path, no synthetic block.

### TEST-021 — test_dnsp_does_not_serialize_cohort (FR-CONV.6 + NFR-CONV.10)
On one partition's escalation exhaust, N-1 sibling partitions continue concurrently (INV-021). Assertion: spawn-log timing — N-1 partitions overlap.

### TEST-022 — test_synthetic_dnsp_dedup_not_regression (FR-CONV.5 + FR-CONV.6 + INV-012)
Synthetic finding same `dedup_key` cycles 1+2 (others shrinking) proceeds to cycle 3. Assertion: execution log shows cycle 3 attempted.

### TEST-023 — test_hidden_input_guard (NFR-CONV.3)
Fixture-populated `.dev/tasks/done/` yields byte-identical structural output vs empty-`done/`. Assertion: byte-diff structural fields.

### TEST-024 — test_sequencing_PR06_before_PR04 (INV-010)
If PR-04 lands before PR-06, dynamic enumeration still richens once catalogue activates. Assertion: structural assertion on enriched checklist.

### TEST-025 — test_invariant_preservation_NFR_6_through_10 (NFR-CONV.6..10)
All 5 invariants preserved per Negative Criteria. Composite fixture exercising each invariant surface.

**Test environments:** Local via UV (`uv run pytest`); CI (GitHub Actions / `make test`). No external services, no containers, no network. `make verify-sync` in CI confirms `src/superclaude/` and `.claude/` agree.

## Migration and Rollout Plan

**Migration strategy:** Strictly-additive, per-FR serially-sequenced (A-002 governance). No data migration, no schema backfill, no cutover. Each FR = own commit, independently revertable per §19.4 co-revert matrix.

**Authoritative landing order (single source of truth):** PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03.

### MIG-001 — M1.1: FR-CONV.1 (PR-06) lands 1st
Append TB-Add-1..8 structural checks to rf-qa task-integrity checklist + mirror in 15-item validation block. Strictly-additive per A-002. **Rollback:** revert specific TB-Add append lines individually OR full revert of PR-06 commit. **Dependencies:** Q-DM-1 decision; design approval. **Duration:** TBD.

### MIG-002 — M1.2: FR-CONV.2 (PR-01) lands 2nd
Insert task-level `## Execution Context` header. Header scope-confined: NO file paths in header; per-item Context fields keep file:line citations. **Rollback:** disable header generation; MDTM files degrade gracefully. **Dependencies:** M1.1 PASS.

### MIG-003 — M1.3: FR-CONV.3 (PR-04) lands 3rd
Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt. **Rollback:** disable passthrough block; rf-qa-qualitative falls back to current behavior. **Dependencies:** M1.2 PASS.

### MIG-004 — M1.4: FR-CONV.4 (PR-07) lands 4th
Insert "Five Adversarial Axes" header subsection + axis column on Items Reviewed table. Overlay-only. **Rollback:** remove axis column + drift-axis-inactive annotation; 15-item checklist untouched. **Dependencies:** M1.3 PASS.

### MIG-005 — M1.5: FR-CONV.5 (PR-02) lands 5th
Add monotonicity guard + regression detection to EXISTING retry loops. No new loop/stage. **Rollback:** disable two guards individually; existing retry loops + per-gate caps continue. **Dependencies:** M1.4 PASS.

### MIG-006 — M1.6: FR-CONV.6 (PR-03 BASE) lands 6th
Emit synthetic HIGH-severity synthetic-dnsp finding on partition escalation exhaust. All-agents-fail guard preserved. **Rollback:** revert DNSP edit sites; existing rf-team-lead.md:417 handles zero-partitions-succeeded path. **Dependencies:** M1.5 PASS.

### MIG-007 — M1.7: Post-merge audit + NFR-CONV.4 measurement (1–2 weeks)
Audit first 5 rf-qa-qualitative runs after FR-CONV.3 lands (K-003 / X-002 audit-target). Measure token-cost on 5 representative BUILD_REQUESTs (NFR-CONV.4 ≤10% ceiling). **Rollback triggers:** audit shows inflation → revert FR-CONV.3; ceiling exceeded → summarise FR-CONV.3 verdict table.

### Feature Flags (logical only — no runtime flag system)

| Logical Flag | Default | Cleanup Date | Owner |
|---|---|---|---|
| `TB_ADD_1_THROUGH_8` | Enabled at merge | Post-v3.9 GA + 30 days | rf-qa maintainer |
| `EXECUTION_CONTEXT_HEADER` | Enabled at merge | Post-v3.9 GA + 30 days | task-builder maintainer |
| `INHERITED_STRUCTURAL_VERDICT` | Enabled at merge | Post-K-003 audit pass | QA Lead |
| `FIVE_ADVERSARIAL_AXES` | Enabled at merge | Post-v3.9 GA + 30 days | rf-qa-qualitative maintainer |
| `RETRY_MONOTONICITY_GUARDS` | Enabled at merge | Post-v3.9 GA + 30 days | rf-task-builder maintainer |
| `SYNTHETIC_DNSP_EMISSION` | Enabled at merge | Post-v3.9 GA + 30 days | rf-analyst / rf-qa maintainers |

### Rollout Stages
- **Stage 0 — Pre-merge:** SC-1 / Q-DM-1 resolved by Engineering Lead before FR-CONV.1
- **Stages 1–6 — Serial FR landing:** PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03; `make verify-sync` PASS gate between each
- **Stage 7 — Post-merge audit window (1–2 weeks):** K-003 audit + NFR-CONV.4 measurement; §14.2 metric thresholds gate review
- **Stage 8 — GA + 30 days:** fallback paths removed; advisory rules promoted pending Phase-2 calibration

### Rollback Procedure (Co-Revert Matrix from §19.4)

| Reverted FR | Co-Revert Required | Reason |
|---|---|---|
| FR-CONV.5 | FR-CONV.6 dedup-key emission | INV-012 composition unneeded |
| FR-CONV.1 | FR-CONV.3 dynamic-enumeration consumer | INV-010 — TB-Add catalogue source |
| FR-CONV.2, FR-CONV.4 | Independently revertable | A-002 strictly-additive |
| FR-CONV.6 | FR-CONV.5 `\|F_n\|` definition adjustment | Inverse edge — pair jointly revertable |

**Rollback decision criteria:** K-003 inflation → revert FR-CONV.3; FR-CONV.5 false-halt rate >50% → disable guards; TB-Add false-positive class → revert specific append line; NFR-CONV.4 exceeded → summarise FR-CONV.3 table; INV-018 layout change → re-integration commit all 6 FRs; A-001 violated → revert direct `.claude/` edit.

## Operational Readiness

**Single-tenant internal framework — no multi-tenancy, no infrastructure scaling, no live alerting in v3.9.**

### OPS-001 — K-003 audit-target runbook (first 5 rf-qa-qualitative runs post-FR-CONV.3)
**Symptoms:** rf-qa-qualitative output missing `## Self-Audit` OR Self-Audit shows zero independent semantic checks. **Diagnosis:** Read `.dev/tasks/to-do/TASK-*/reviews/qa-qualitative-review.md`; grep for `## Self-Audit`; verify ≥1 semantic check beyond inherited PASS. **Resolution:** If missing → prompt FR-CONV.3 spawn-prompt; if zero independent checks → K-003 FAIL, disable passthrough flag. **Escalation:** QA Lead immediate; Engineering Lead if pattern across all 5 runs. **Prevention:** INV-019 mandate enforcement.

### OPS-002 — DNSP triage runbook (synthetic-dnsp emission count >0 in production)
**Symptoms:** rf-qa report contains `synthetic-dnsp` finding (HIGH severity). **Diagnosis:** Read affected partition spawn-log (`evidence` field); identify root cause of escalation-ladder exhaust; check `dedup_key` for prior similar events. **Resolution:** Manual investigation per `recommendation` field; consider whether root cause should land as new TB-Add. **Escalation:** rf-qa maintainer; escalate to Engineering if ≥3 distinct dedup-keys in a week. **Alert threshold:** >0 → human review (§14.2).

### OPS-003 — All-partitions-exhaust HALT runbook (no DNSP emitted)
**Symptoms:** rf-team-lead HALTs and asks user; zero partitions succeeded. **Diagnosis:** Confirm zero partition successes in spawn-log; verify line-417 escalation path fired and NO synthetic-dnsp emitted (correct per FR-CONV.6 mutual-exclusivity). **Resolution:** This is preserved all-agents-fail guard — user resolves unresolved findings before re-run. **Escalation:** rf-team-lead maintainer if HALT misfires when ≥1 partition succeeded.

### OPS-004 — Monotonicity halt rate alert (>50% of fix-cycle batches)
**Symptoms:** Many fix-loops halting with `[HALT-MONOTONICITY] |F|=<n>`. **Diagnosis:** Sample 3 halt events; inspect BUILD_REQUESTs for upstream defects; inspect generated MDTM for structural issues. **Resolution:** Improve upstream BUILD_REQUESTs; consider TB-Add-2 calibration (OPEN-INV-006). **Escalation:** rf-task-builder maintainer. **Alert threshold:** >50% (§14.2).

### OPS-005 — Regression-halt rate alert (>20% of fix-cycle batches)
**Symptoms:** Many fix-cycles emitting verbatim regression halt message. **Diagnosis:** Sample 3 regression events; inspect what changed between cycles; look for fix-cycle pattern introducing collateral damage. **Resolution:** Tighten fix-cycle prompts (X-003 slow-convergence threshold REJECTED). **Escalation:** Engineering Lead. **Alert threshold:** >20% (§14.2).

### OPS-006 — `make verify-sync` FAIL post-FR-merge
**Symptoms:** Sync verification fails between `src/superclaude/` and `.claude/`. **Diagnosis:** Re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline rule (A-001) followed. **Resolution:** Re-sync; commit only on PASS; if persistent, revert direct `.claude/` edit and re-run from `src/superclaude/` (K-009 contingency). **Escalation:** Per-commit author.

### OPS-007 — INV-018 layout change detected (K-008)
**Symptoms:** `.dev/tasks/` directory schema differs from pre-merge. **Diagnosis:** Inspect all 6 FRs for path/naming references; re-integrate at new layout. **Resolution:** Re-integration commit covering all 6 FRs per §19.4 dependency matrix. **Escalation:** Engineering Lead + orchestrator.

### Observability
**Logging:**
- rf-task-builder execution log → `### Execution Log` section in MDTM task file (indefinite, Git)
- rf-qa gate reports (4 phases) → `.dev/tasks/to-do/TASK-*/qa/qa-{phase}-{partition-N-of-M}.md`
- rf-qa-qualitative reports → `.dev/tasks/to-do/TASK-*/reviews/`
- Synthetic-dnsp findings → embedded structured block in partition agent's QA report
- Spawn logs → `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`

**Metrics (offline, post-merge):**
- `synthetic-dnsp emission count` (Counter): alert >0 in production
- `[HALT-MONOTONICITY] count` (Counter): alert >50% of fix-cycle batches
- `regression-halt count` (Counter): alert >20% of fix-cycle batches
- `Self-Audit coverage` (Gauge, fraction): alert <100% on first 5 runs (K-003 block-release)
- `make verify-sync PASS rate` (Counter): 100% threshold; any FAIL blocks commit

**Tracing:** N/A (single-process spawning model, no distributed coordination). Causality recovered offline from execution log + spawn-log + gate-report chain.

**Alerts/Dashboards:** N/A in v3.9 — offline review only. Live alerting deferred.

### On-Call
**Team:** task-builder maintainers (rotating). **Page volume:** <2/week at steady state. **Response time:** K-003 audit failure 4 business hours; DNSP triage 24 hours; `make verify-sync` FAIL immediate. **Knowledge prerequisites:** task-builder v3.9 architecture, rf-qa/rf-qa-qualitative gate semantics, rf-team-lead.md:417 escalation, A-001 sync workflow.

**Capacity Planning:** N/A — internal skill, no infrastructure scaling. NFR-CONV.5 forbids new external dependencies or synchronous network calls.
