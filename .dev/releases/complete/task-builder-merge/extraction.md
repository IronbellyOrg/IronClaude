---
spec_source: TDD_TASK_BUILDER_CONVERGENCE.compressed.md
generated: 2026-05-15T15:11:00+00:00
generator: requirements-design-extraction-agent
functional_requirements: 6
nonfunctional_requirements: 11
total_requirements: 17
complexity_score: 0.7
complexity_class: HIGH
domains_detected: [backend, testing, devops, security, qa-framework]
risks_identified: 10
dependencies_identified: 10
success_criteria_count: 8
extraction_mode: standard
data_models_identified: 5
api_surfaces_identified: 4
components_identified: 6
test_artifacts_identified: 25
migration_items_identified: 7
operational_items_identified: 7
pipeline_diagnostics: {elapsed_seconds: 494.2, started_at: "2026-05-15T15:10:30.040586+00:00", finished_at: "2026-05-15T15:18:44.269768+00:00"}
---

## Functional Requirements

### FR-CONV.1
**Title:** Append 8 structural checks (TB-Add-1..8) to rf-qa task-integrity gate
**Priority:** Must Have (P0)
**Classification:** CASE-D adopt-adapted port (PR-06)
**Protected invariant:** zero-trust QA
**Behavior:** Append 8 structural checks (TB-Add-1..8) to rf-qa A.10 mirrored across all three definition surfaces (rf-qa.md 20-item checklist, SKILL.md A.10 9-item block, SKILL.md 15-item validation block).
**Acceptance:** Each TB-Add-1..8 fires a distinct, item-ID-naming error on violation; TB-Add-1/3/4/5/6/7/8 block the gate; TB-Add-2 emits `[ADVISORY]` and does not block.
**TB-Add catalogue:**
- TB-Add-1: placeholder scan (Hard)
- TB-Add-2: item-count bounds ≥3/≤40-track/≤50-single-track (`[ADVISORY]` until OPEN-INV-006 calibration)
- TB-Add-3: clarification adjacency (Hard)
- TB-Add-4: circular-dependency DAG check (Hard)
- TB-Add-5: granularity / XL-has-subtasks (Hard)
- TB-Add-6: Confidence/Verification format consistency (Hard)
- TB-Add-7: Execution-Context source-areas reappear in items (Hard)
- TB-Add-8: per-item Context field has ≥1 file:line citation OR justified-absence comment (Hard) — resolves INV-015
**Insertion sites:** rf-qa.md:268-287; SKILL.md:~898-906; SKILL.md:~1491-1507
**Negative criteria:** No existing rf-qa check renamed/renumbered/removed; no bundle-specific `/sc:tasklist` checks may appear.

### FR-CONV.2
**Title:** Insert task-level Execution Context header in generated MDTM files
**Priority:** Must Have (P0)
**Classification:** CASE-D adopt-adapted port (PR-01)
**Protected invariant:** evidence-bound-item
**Behavior:** Insert `## Execution Context` block (after frontmatter, before checklist) with exactly three labeled lines: References / Source areas / Key constraints.
**Acceptance:** Block renders three labeled lines for fully-populated BUILD_REQUEST; degrades to References-only for minimal BUILD_REQUEST (other lines explicitly omitted, not blank).
**Verification:** `grep -n "## Execution Context"` returns line N; next 10 lines contain ≥1 of References/Source areas/Key constraints; `grep -E "src/|/.*:[0-9]+"` returns zero hits in header range.
**Insertion sites:** SKILL.md:1407-1487 (primary template); SKILL.md:715-725 (BUILD_REQUEST guidance); SKILL.md:~139, ~86
**Negative criteria:** Per-item Context fields MUST retain file:line citations or justified-absence comments; per-item 5-field schema MUST NOT be altered.

### FR-CONV.3
**Title:** Inject Inherited Structural Verdict block + Self-Audit obligation into rf-qa-qualitative spawn
**Priority:** Must Have (P0)
**Classification:** CASE-B silent-adopt port (PR-04)
**Invariant alignment:** zero-trust QA
**Behavior:** Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt under `## Inherited Structural Verdict` with directive: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality." Add `## Self-Audit` to output schema.
**Acceptance:** Spawn prompt carries verdict table byte-for-byte; on fix-cycle re-run, orchestrator re-injects NEW (cycle-N) verdict (INV-002); rf-qa-qualitative output contains Self-Audit listing relied-on PASS items AND ≥1 semantic check (INV-019).
**Insertion sites:** SKILL.md:923-1000 (A.10.5 spawn prompt; injection at ~:966); rf-qa-qualitative.md:794 (EOF append).
**Negative criteria:** rf-qa-qualitative MUST NOT mark any item VERIFIED solely from inherited verdict; anti-inflation rule at rf-qa-qualitative.md:766-775 MUST NOT be weakened.

### FR-CONV.4
**Title:** Insert Five Adversarial Axes overlay before rf-qa-qualitative 15-item checklist
**Priority:** Must Have (P0)
**Classification:** CASE-D adopt-adapted port (PR-07)
**Protected invariant:** zero-trust QA
**Behavior:** Insert `### Five Adversarial Axes` header subsection BEFORE existing 15-item task-qualitative checklist; add `axis` column to Items Reviewed table. Five axes: drift / contradictions / omissions / weakened-criteria / invented-content (plus `none` sentinel).
**Acceptance:** Subsection renders before 15-item checklist; Items Reviewed table `axis` column populated with one canonical value per row; `drift-axis-inactive` annotation emitted in Summary block when no item restates BUILD_REQUEST.GOAL verbatim.
**Insertion sites:** rf-qa-qualitative.md:527-583 (body unmodified; header inserts before `#### Checklist (15 items)`); rf-qa-qualitative.md:675-714 (axis column site); SKILL.md:961.
**Negative criteria:** 15-item checklist MUST NOT be removed/reordered/renamed; severity floor at rf-qa-qualitative.md:786-795 MUST NOT be weakened; no axis introduces new conditional code path.

### FR-CONV.5
**Title:** Add monotonicity + regression halt guards to retry loops
**Priority:** Must Have (P0)
**Classification:** CASE-D adopt-adapted port (PR-02)
**Protected invariant:** zero-trust QA
**Behavior:** Add two stop-conditions to EXISTING fix-cycle retry loops (no new loop or stage): (1) Monotonicity guard — HALT if `|F_{n+1}|>=|F_n|`; (2) Regression detection — HALT if any item PASS at cycle N is FAIL at cycle N+1. Precedence: Regression > monotonicity.
**Acceptance:** Regression flip emits verbatim message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` and exits BEFORE monotonicity check; non-shrink emits `[HALT-MONOTONICITY]|F|=<n>`; identical dedup-key synthetic findings across cycles do NOT trigger halt.
**Insertion sites:** SKILL.md:867-873; SKILL.md:1547-1553; rf-task-builder.md:334-361; rf-qa.md:~308-315.
**Negative criteria:** Legitimate slow-cycle correction MUST NOT be halted; four independent retry counters MUST NOT be collapsed; X-003 slow-convergence threshold REJECTED; existing 3-cycle hard cap at rf-team-lead.md:417 preserved.

### FR-CONV.6
**Title:** Emit synthetic-dnsp HIGH finding on partition escalation-ladder exhaust
**Priority:** Must Have (P0)
**Classification:** CASE-B silent-adopt port (PR-03 BASE)
**Invariant alignment:** zero-trust QA + evidence-bound-item + parallel-research
**Behavior:** After partition agent's escalation ladder exhausts (rf-analyst, rf-qa, or rf-qa-qualitative partition), emit synthetic HIGH-severity finding with `source: "synthetic-dnsp"` to agent's output stream. Dedup key: `(assigned_files_range, escalation_ladder_exhaust_point)`.
**Acceptance:** When ≥1 partition succeeded AND ≥1 partition exhausted: emit JSON-or-block finding with all 5 fixed fields (severity HIGH, source synthetic-dnsp, affected_range, evidence, recommendation) plus dedup_key and found_n_times; identical dedup_keys collapse with `found N times`; zero partitions succeeded → NO synthetic emits, existing all-agents-fail escalation runs.
**Insertion sites:** SKILL.md:572-656 (A.8); SKILL.md:870-918 (A.10); rf-analyst.md:58-71; rf-qa.md:49-77 (DNSP edit at :70-77); rf-qa-qualitative.md:70-80.
**Negative criteria:** synthetic-dnsp MUST NOT emit before ladder exhausts; existing rf-team-lead.md:417 escalation MUST NOT be replaced or short-circuited; synthetic findings MUST NOT mask real findings; dedup-key collapse MUST NOT cross-cycle (INV-012).

**Cross-FR dependency chain:** FR-CONV.1 → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6.

## Non-Functional Requirements

### NFR-CONV.1 — Structural Field Determinism
TB-Add-1..8 PASS/FAIL verdicts, synthetic-dnsp 5 fixed fields + dedup-key, axis column values, Items Reviewed table structure are byte-identical across two runs on the same BUILD_REQUEST + source tree. Measurement: re-run task-builder twice; diff structural fields; must be byte-equal.

### NFR-CONV.2 — Research-Driven Prose Determinism Exclusion
Per-item Context prose and rf-qa-qualitative semantic-check prose remain LLM-research-driven; byte-equality not required. Structural annotations within prose (axis labels, finding counts, dedup-keys) MUST remain byte-equal.

### NFR-CONV.3 — Hidden-Input Determinism
Fixture-populated `.dev/tasks/done/` produces byte-identical structural output to empty `.dev/tasks/done/`. Measurement: identical BUILD_REQUEST run with (a) empty and (b) populated done/; structural fields must be byte-identical. PR-05 advisory mechanism REJECTED for Phase-1.

### NFR-CONV.4 — Token-Cost Ceiling
Token-cost ratio (post-merge / pre-merge) per equivalent BUILD_REQUEST ≤1.10. Measurement: 5 representative BUILD_REQUESTs covering Quick/Standard/Deep tiers; record total token counts; compute ratio. Contingency K-010: summarise FR-CONV.3 verdict table if exceeded.

### NFR-CONV.5 — No New Dependencies / Local Checks Only
Wall-clock impact: no new external dependencies, no synchronous network calls; gate additions use only Read, Grep, Glob, Bash. Measurement: diff inspection rejects any new external dep or synchronous network call.

### NFR-CONV-R1 — Single-Pass Gate PASS Rate
≥80% of representative BUILD_REQUESTs PASS the task-integrity gate on first cycle. Measurement: run 5 representative BUILD_REQUESTs; count first-cycle PASS verdicts.

### NFR-CONV.6 — Self-Contained-Item Invariant
Operational source: SKILL.md:~1452-1457 (5-field per-item schema). **SC-1 OPEN (Q-DM-1):** PRD §25.4 vs SKILL.md current content schema contradiction — fixture targets whichever schema lands. Pass/fail: synthetic fixture with all 5 fields PASSES all 8 TB-Add checks; same fixture with one field stripped FAILS TB-Add-1.

### NFR-CONV.7 — Evidence-Bound-Item Invariant
Operational source: SKILL.md:1530 rule #2. Three-fixture triple: (a) `Context: src/foo` (no `:N`) → FAILS TB-Add-8; (b) `Context: src/foo:42` → PASSES; (c) `Context: <none — pure refactor> [justified-absence]` → PASSES.

### NFR-CONV.8 — Persistent .dev/tasks/ Artifact Invariant
Operational source: OPEN-INV-018 / SKILL.md:1536 rule #5. Diff `.dev/tasks/<task-id>/` directory layout pre-merge vs post-merge. PASS when zero structural changes occur: no new mandatory subdirectory, no rename of research/qa/synthesis/reviews/adversarial, no naming-pattern change.

### NFR-CONV.9 — Zero-Trust QA Invariant
Operational source: rf-qa.md:141-142. Verbatim PASS/FAIL definitions: any gap of any severity = FAIL. Two-part fixture: (a) 1-LOW-finding fixture → gate FAILS; (b) FR-CONV.3 inherited-verdict applied → no item marked VERIFIED unless Self-Audit lists independent semantic-check engagement.

### NFR-CONV.10 — Parallel-Research Invariant
Operational source: rf-qa.md:49-77 + rf-qa-qualitative.md:50-82. INV-021: DNSP fires within-agent-instance. Spawn-log fixture: N partition agents spawn concurrently (timestamp overlap proves concurrency); on one agent's exhaust, N-1 partitions continue to completion before that one synthesises a DNSP finding. FAIL if cohort serialises or DNSP fires cross-cohort.

## Complexity Assessment

**complexity_score:** 0.7
**complexity_class:** HIGH

**Scoring rationale:**
- **Surface area:** 6 FRs × 3-4 file insertion sites each = ~22 distinct edit points across 5 source files (SKILL.md 1709 lines, rf-qa.md 432 lines, rf-qa-qualitative.md 794 lines, rf-analyst.md 349 lines, rf-task-builder.md 493 lines).
- **Dependency chain depth:** 6-step strict serial sequencing (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03) with no parallelism permitted.
- **Cross-FR composition complexity:** FR-CONV.5 ↔ FR-CONV.6 mutual dedup-key composition; FR-CONV.3 ↔ FR-CONV.1 dynamic enumeration (INV-010); FR-CONV.4 ↔ FR-CONV.3 inherited-PASS composition (INV-013).
- **Invariant preservation risk:** 5 load-bearing invariants must remain provable via NFR-CONV.6..10 fixtures; 4 of 6 FRs have direct invariant alignment requirements.
- **Open critical-path blocker:** Q-DM-1 (SC-1) — PRD vs source schema contradiction must be resolved by Engineering Lead before FR-CONV.1 can land.
- **Risk profile:** 10 risks (K-001..K-010); 1 HIGH-impact (K-008 portfolio-wide layout dependency), 3 MEDIUM-impact (K-003, K-007, K-009).
- **Mitigating factors:** strictly-additive A-002 governance; per-FR rollback granularity; no new external dependencies (NFR-CONV.5); local checks only.

## Architectural Constraints

1. **A-001 sync-discipline:** Source of truth is `src/superclaude/`; `make sync-dev` propagates to `.claude/`; `make verify-sync` MUST PASS before each commit.
2. **A-002 strictly-additive governance:** No existing pipeline stage, agent, checklist item, or rule may be renamed, renumbered, or removed by any FR.
3. **G6 four-case conflict rule:** Every proposal classified as CASE A/B/C/D; CASE-A and CASE-D require conflict-register row; CASE-B and CASE-C are correctly silent.
4. **CB-3 per-check classification:** Bulk-import of mechanisms from sc-tasklist forbidden; per-check classification only.
5. **Strict serial FR landing order:** PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03; no parallel landings permitted.
6. **NFR-CONV.5 dependency boundary:** No new external dependencies, no new MCP servers, no new libraries, no synchronous network calls; only existing tools (Read, Grep, Glob, Bash).
7. **rf-team-lead.md:417 preservation:** Existing 3-fix-cycle escalation guard MUST NOT be replaced or short-circuited; verified NO DRIFT 2026-05-14.
8. **Anti-inflation rule absolute:** rf-qa-qualitative.md:766-775 (Prohibited Behaviors block, anti-inflation bullet at :770) MUST NOT be weakened, removed, or rephrased.
9. **Zero-trust verdict definitions absolute:** rf-qa.md:141-142 PASS/FAIL definitions ("any gap of any severity = FAIL") MUST be preserved verbatim.
10. **Determinism scope split:** Structural fields byte-deterministic (NFR-CONV.1); research-prose nondeterminism acceptable (NFR-CONV.2).
11. **Single-tenant internal framework:** No multi-user surface, no per-tenant data, no isolation boundary beyond `.dev/tasks/<task-id>/` persistence.
12. **Skill-level Critical Rule #13:** task-builder skill does not invoke rf-team-lead directly (forbidden by SKILL.md:~1552).
13. **Persistent artifact convention (INV-018):** `.dev/tasks/` layout stability — research/qa/synthesis/reviews/adversarial subdirectory naming MUST NOT change.

## Risk Inventory

1. **K-001** (LOW probability / LOW impact) — TB-Add false positives waste fix-cycles. **Mitigation:** Each TB-Add cites source-check-ID; TB-Add-2 ships as `[ADVISORY]`; individually revertable. **Contingency:** Disable specific TB-Add line.
2. **K-002** (LOW / LOW) — Execution Context header drift. **Mitigation:** TB-Add-7 cross-validates header source-areas reappear in items; gate fails on drift. **Contingency:** Header optional fallback to References-only.
3. **K-003** (LOW / MEDIUM) — PR-04 passthrough causes inflation despite anti-inflation rule. **Mitigation:** INV-019 mandatory Self-Audit; X-002 audit-target — first 5 rf-qa-qualitative runs MUST be audited. **Contingency:** Disable passthrough flag.
4. **K-004** (LOW / LOW) — 5-axis annotation ambiguity over-flags items. **Mitigation:** Annotation-only overlay; severity floor preserved; `drift-axis-inactive` annotation. **Contingency:** Audit axis distribution; tune annotation rules.
5. **K-005** (LOW / LOW) — Retry monotonicity halts legitimate slow-cycle correction. **Mitigation:** Strict-shrink threshold; X-003 REJECTED. **Contingency:** Disable guards individually.
6. **K-006** (LOW / LOW) — Synthetic-dnsp findings mask real issues. **Mitigation:** HIGH severity guarantees gate visibility; dedup-key prevents over-emission. **Contingency:** Inspect emission-count weekly.
7. **K-007** (LOW / MEDIUM) — PR-04 + PR-06 sequencing inversion. **Mitigation:** Sequencing rule enforced in release-spec.md §4.6; INV-010 dynamic enumeration mitigation. **Contingency:** Re-merge in correct order.
8. **K-008** (LOW / HIGH) — INV-018 `.dev/tasks/` directory layout changes invalidate all proposals. **Mitigation:** Portfolio-wide note; SP-33 stability commitment. **Contingency:** Re-integration commit covering all 6 FRs.
9. **K-009** (LOW / MEDIUM) — sync-discipline (A-001) violated. **Mitigation:** All FRs name `src/superclaude/` paths exclusively; CLAUDE.md mandates workflow. **Contingency:** Revert `.claude/` direct edit; re-run from `src/superclaude/`.
10. **K-010** (LOW / LOW) — Token ceiling NFR-CONV.4 exceeded by >10%. **Mitigation:** Empirical post-merge measurement on 5 BUILD_REQUESTs. **Contingency:** Summarise FR-CONV.3 verdict table rather than emit verbatim.

## Dependency Inventory

**External dependencies:** NONE — NFR-CONV.5 explicitly forbids new external dependencies, network calls, MCP servers, or libraries.

**Internal dependencies (10):**
1. `release-spec.md` v1.0.0 — landing order (§4.6), SP-10 rollback matrix (§9), audit rows (§8.3)
2. `conflict-register.md` — 5 CASE-D rows for PR-01/PR-02/PR-06/PR-07/PR-05-deferred
3. `invariant-probe.md` — INV-002, INV-010, INV-012, INV-015, INV-019, INV-021 routed to FR Negative Criteria
4. `FINAL-REPORT.md` §6.3 (5 ADOPT-grade qualities, inverse direction); §6.2 F2/F4 (oscillation + over-engineering evidence)
5. `rf-team-lead.md:417` — 3-fix-cycle escalation; verified NO DRIFT 2026-05-14
6. `rf-qa.md:141-142` — zero-trust PASS/FAIL definitions
7. `task-builder/SKILL.md:~1452-1457` — per-item schema; **drift flagged (SC-1)** — Q-DM-1 blocker
8. `.dev/tasks/` directory layout (INV-018) — stable per SP-33
9. `make sync-dev` / `make verify-sync` pipeline (A-001) — operational tooling
10. PRD v1.0 — Epics 1-3 (FR-CONV.1..6) source

**Infrastructure dependencies:** N/A — no database, message queue, compute allocation, or deployment target.

## Success Criteria

### Technical Metrics (§4.1)
1. **Single-pass gate PASS rate:** Currently ≥80%; target ↑ post-merge. Method: Fraction of BUILD_REQUESTs passing task-integrity gate on first cycle.
2. **Placeholder-defect detection rate:** Currently n/a; target 100% on synthetic fixtures. Method: TB-Add-1 fires on every placeholder/title-only fixture item.
3. **DAG-cycle detection rate:** Currently n/a; target 100% on synthetic fixtures. Method: TB-Add-4 fires on every circular-dependency fixture.
4. **Self-Audit coverage post-FR-CONV.3:** Target 100% on first 5 runs (K-003 audit-target). Method: Every rf-qa-qualitative run carries `## Self-Audit` entry.
5. **`[HALT-MONOTONICITY]` emission rate:** Target <10%. >50% emission rate alerts upstream BUILD_REQUEST defect.
6. **Synthetic-dnsp emission count:** Target ≥1 on twice-exhaust fixture; 0 on healthy run.

### Business Metrics (§4.2)
7. **Generation-cost efficiency:** Token-cost ratio ≤1.10 (NFR-CONV.4). Method: 5 representative BUILD_REQUESTs.
8. **Gate convergence health:** Fix-cycle convergence rate ≥75% baseline, expected ↑ post-merge.

## Open Questions

### Q-DM-1 — CRITICAL Blocker (SC-1) — OPEN
**Per-Item Checklist Schema PRD-vs-source contradiction.** PRD §25.4 declares per-item 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` "preserved unchanged" at `SKILL.md:1452-1457`, BUT current SKILL.md:1450-1460 holds `{Context, Action, Output, Verification, Completion gate}`. Schemas overlap on only 2 fields (Context, Verification). **Owner:** Engineering Lead. **Target:** Pre-FR-CONV.1 implementation. **Resolution options:** (a) FR-CONV.1/TB-Add-8 LANDS PRD schema (would contradict A-002 unless treated as net-new); (b) correct PRD §25.4 pointer; (c) §25.4 describes a separate schema living elsewhere.

### OPEN-PR05 — Tracked
When does `.dev/tasks/done/` reach ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05 Tier-History Advisory? Owner: Engineering Lead. Re-check each major release.

### OPEN-INV-006 — OPEN
Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track). Owner: Engineering. Phase-2 with PR-05. TB-Add-2 stays `[ADVISORY]` until calibrated.

### OPEN-INV-017 — Deferred
Historical-file staleness check for PR-05 advisory citations. Academic given PR-05 Phase-2 deferral.

### OPEN-INV-018 — OPEN
If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration. Owner: Engineering Lead. Document layout-change contract.

### OPEN-X-002 — OPEN (K-003 audit-target)
PR-04 anti-inflation operational test — "reliance ≠ verification" distinction empirically observable, not structurally provable. Owner: QA Lead. Audit per release-spec.md §8.3 row 4 — first 5 rf-qa-qualitative runs after FR-CONV.3.

### OPEN-TOKEN — OPEN
NFR-CONV.4 token-ceiling empirical measurement. Owner: Engineering Lead. Post-merge on 5 representative BUILD_REQUESTs.

### Q-DM-2 — RESOLVED (§19.4)
Per-FR rollback dependency matrix enumerated inline (§19.4).

### Q-DM-3 — RESOLVED (§8.5)
Five Adversarial Axes canonical definitions defined in §8.5.

### Q-DM-4 — RESOLVED (§6.1, §12.4)
Per-gate fix-cycle limits authority: rf-task-builder.md I16 (`:334-361`) is authoritative; rf-qa.md max=3 is per-cycle global ceiling layered on top.

## Data Models and Interfaces

### DM-001 — Execution Context Header
**Producer:** FR-CONV.2 (rf-task-builder). **Source:** PRD §25.1 / SKILL.md placement after frontmatter.
**Schema:**
```yaml
"## Execution Context":
  References:        # list[string], "R-###: <ref-line>"
  Source areas:      # list[string], named modules — NEVER file paths
  Key constraints:   # list[string], 1-3 invariants from BUILD_REQUEST
```
**Constraints:** `Source areas` MUST NOT contain file:line citations (hidden-input determinism). Block degrades to References-only when BUILD_REQUEST minimal — other lines explicitly omitted, not blank. TB-Add-7 cross-validates `Source areas` reappear in ≥1 per-item Context field.

### DM-002 — Inherited Structural Verdict Block
**Producer:** task-builder orchestrator (executing A.10.5). **Source:** PRD §25.2.
**Schema:**
```yaml
"## Inherited Structural Verdict":
  rf_qa_table_verbatim: <verbatim copy of rf-qa task-integrity Items Reviewed table at spawn time>
  prompt_directive: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."
  reinjection_rule: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."
```
**Governing rules:** freshness_rule (INV-002 cycle-N+1 reinjection); enumeration_rule (INV-010 dynamic checklist); consumer_obligation (INV-019 Self-Audit); anti_inflation (rf-qa-qualitative.md:766-775 unchanged).

### DM-003 — Synthetic DNSP Finding
**Producer:** Partition agent (rf-analyst, rf-qa, rf-qa-qualitative partition). **Consumer:** task-builder orchestrator merge step. **Source:** PRD §25.3.
**Schema:**
```yaml
synthetic_dnsp_finding:
  severity: HIGH                                # fixed
  source: "synthetic-dnsp"                      # fixed
  affected_range: "<agent's assigned_files slice>"
  evidence: "<spawn-log path, OR stub citing log absence>"
  recommendation: "Manual review required — partition agent failed twice"
  dedup_key: "(assigned_files_range, escalation_ladder_exhaust_point)"
  found_n_times: <int, default 1>
```
**Constraints:** severity HIGH non-overridable; source fixed literal; canonical wire format YAML list `["<range>", "<exhaust_point>"]`; `escalation_ladder_exhaust_point` from closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`. Within-cycle dedup collapses; cross-cycle dedup-key NOT a regression (INV-012). All-agents-fail guard precedence: zero successes → no synthetic emits.

### DM-004 — Per-Item Checklist Schema ⚠ CRITICAL DRIFT (Q-DM-1)
**Source:** PRD §25.4 — declared `NFR-CONV.6` operational source. **Status:** SC-1 unresolved.
**PRD-asserted schema (target):**
```yaml
per_item_schema:
  Description: "<one-line task-item action statement>"
  Context: "<file:line citation OR justified-absence comment>"     # TB-Add-8 enforced
  Acceptance: "<observable success condition>"
  Confidence: "<HIGH|MEDIUM|LOW> — with one-line rationale"
  Verification: "<command, file inspection, or test to confirm Acceptance>"
```
**Current SKILL.md:1450-1460 (as-built):**
```yaml
phase_item_schema_AS_BUILT:
  Context: "<what the executor needs to know>"
  Action: "<exactly what to do>"
  Output: "<what gets created/modified>"
  Verification: "<how to confirm it worked>"
  Completion gate: "<when this item is done>"
```
**Invariant across all resolution options:** TB-Add-8 enforcement applies to Context field regardless of schema selection (both schemas contain Context field).

### DM-005 — Phase Contract: rf-qa → rf-qa-qualitative
**Producer:** rf-qa (task-integrity). **Consumer:** rf-qa-qualitative (task-qualitative). **Source:** PRD §25.5.
**Schema:**
```yaml
phase_contract:
  producer: rf-qa
  consumer: rf-qa-qualitative
  artifact: "## Inherited Structural Verdict block in spawn prompt"
  schema_version: "1.0.0"
  delivery_semantics: "at-most-once-per-cycle"
  freshness_rule: "On fix-cycle re-run, orchestrator re-injects NEW verdict; stale verdicts forbidden (INV-002)"
  enumeration_rule: "Checklist enumeration is dynamic — auto-picks up TB-Add catalogue from FR-CONV.1 (INV-010)"
  consumer_obligation: "Self-Audit listing relied-on PASS items AND ≥1 semantic check (INV-019)"
  anti_inflation: "Mechanical re-checking SKIPPED for PASS items; semantic verification STILL REQUIRED (rf-qa-qualitative.md:766-775)"
  failure_mode: "If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5"
```

**Data flow:** BUILD_REQUEST → rf-task-builder → MDTM file (contains DM-001 Execution Context Header + DM-004 per-item checklist) → rf-qa task-integrity (applies TB-Add-1..8 from FR-CONV.1) → emits DM-002 Inherited Structural Verdict (governed by DM-005 Phase Contract) → rf-qa-qualitative (applies Five Adversarial Axes overlay). Partition exhaust at any rf-* agent → emits DM-003 Synthetic DNSP Finding → dedup_key composes into FR-CONV.5 `F_n` set.

**Storage:** All entities are in-band Markdown/YAML artifacts under `.dev/tasks/to-do/TASK-*/`. DM-001 and DM-004 live inside MDTM task file; DM-002 and DM-005 are transient spawn-prompt content (logged to `qa/` spawn logs); DM-003 emitted into agent output stream and merged into `qa/` report. Persistence and version history provided by Git.

## API Specifications

### API-001 — BUILD_REQUEST → MDTM Task File Contract (FR-CONV.2 modifies output)
**Producer:** task-builder skill (orchestrator). **Consumer:** rf-task-builder subagent. **Transport:** Skill-tool prompt; on-disk MDTM task file artifact.
**Schema:** Existing 15-field BUILD_REQUEST per SKILL.md:1407-1487 + optional new `EXECUTION_CONTEXT_REQUIREMENTS` signal that FR-CONV.2 may add. Generated MDTM file MUST contain `## Execution Context` block (DM-001) at top after frontmatter, before Phase 1.
**Auth:** N/A (internal framework). **Rate limits:** N/A (single-process spawning).
**Emission rules:** Fully-populated BUILD_REQUEST → exactly three labeled lines; minimal BUILD_REQUEST → degrades to References-only (other two lines omitted, not blank); header MUST NOT contain specific file paths (NFR-CONV.3 hidden-input determinism).
**Error behavior:** If orchestrator cannot derive even References (no GOAL), task-file generation is MALFORMED return; rf-task-builder's MALFORMED retry counter (max 2) governs.

### API-002 — rf-qa task-integrity → rf-qa-qualitative task-qualitative (FR-CONV.3)
**Producer:** rf-qa running task-integrity QA phase (rf-qa.md:259-289). **Consumer:** rf-qa-qualitative running task-qualitative QA phase (rf-qa-qualitative.md:508-603). **Transport:** orchestrator-mediated spawn-prompt injection at SKILL.md §A.10.5 (verified range SKILL.md:923-1000).
**Schema:** PRD §25.5 Phase Contract (DM-005); injected block follows PRD §25.2 (DM-002).
**Emission rules:** rf-qa emits verdict table verbatim at `.dev/tasks/to-do/TASK-*/qa/qa-task-integrity*.md`; orchestrator extracts table contiguously; splices verbatim into spawn prompt under `## Inherited Structural Verdict` after `TARGET FILES` and before `INSTRUCTIONS:`.
**Constraints:** INV-002 cycle-N+1 reinjection; INV-010 dynamic checklist enumeration; INV-019 Self-Audit mandate.
**Anti-inflation invariant:** Prohibited Behaviors block at rf-qa-qualitative.md:766-775 MUST NOT be weakened.
**Failure mode:** If rf-qa fails to emit task-integrity verdict, rf-qa-qualitative MUST NOT spawn — gate halts at §A.10.

### API-003 — Partition Agent → Orchestrator (FR-CONV.6 synthetic-dnsp emission)
**Producer:** Any partition instance — rf-qa, rf-analyst, or rf-qa-qualitative partition (identical contract). **Consumer:** task-builder skill orchestrator gate-result merge step at SKILL.md §A.8 and §A.10. **Transport:** Synthetic finding emitted as structured block in partition agent's normal output stream.
**Schema:** PRD §25.3 (DM-003).
**Emission rules:** One HIGH-severity synthetic finding with all 7 fields when escalation ladder exhausts; cardinality per-partition-instance; within-cycle dedup collapse increments `found_n_times`; INV-021 within-agent-instance emission (cohort does not serialize); HIGH severity non-overridable.
**All-agents-fail precedence:** Zero partitions succeeded → MUST NOT emit synthetic; activate rf-team-lead.md:417 escalation. Mutually exclusive paths.

### API-004 — Fix-Loop Halt Signals (FR-CONV.5)
**Producer:** rf-task-builder fix-loop (and rf-qa fix-cycle protocol feeding verdict counts). **Consumer:** Itself — next-cycle decision logic. **Transport:** Halt-message strings in fix-loop verdict stream.
**Halt messages (verbatim — fixtures depend on character-for-character match):**
- Monotonicity halt: `[HALT-MONOTONICITY] |F|=<n>` (emitted when `|F_{n+1}| >= |F_n|`)
- Regression halt: `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (emitted when item flips PASS@N → FAIL@N+1)

**Ordering / precedence per cycle transition n → n+1:** (1) regression check first; (2) monotonicity check second; (3) existing 3-cycle hard cap third; (4) otherwise proceed.
**F-set definition:** `F_n` = set of FAIL-verdict items at end of fix cycle n with item identity = dedup-key.
**Negative criteria:** No "shrinks too slowly" threshold (X-003 REJECTED); 4+ retry counters never collapsed; INV-012 — synthetic-dnsp findings count as failures but cross-cycle identical dedup_key is dedup not regression.

**Versioning strategy:** schema_version `1.0.0` (semver) on Phase Contract; other artifacts implicitly versioned under same umbrella. **Compatibility (A-002):** Additive field changes allowed without bump; field renames/removals/halt-message changes are breaking and forbidden. **Deprecation policy:** N/A for v3.9 — strictly-additive landings only; halt-message strings + fixed-value fields are frozen wire ABI.

### Five Adversarial Axes — Canonical Definitions (FR-CONV.4)
- **AX-1 Drift:** Cited fact (file path, line number, signature, count, config value) no longer matches current source.
- **AX-2 Contradictions:** Two artifacts (or two sections) assert mutually incompatible facts about same subject.
- **AX-3 Omissions:** Required touchpoint, consumer, dependency, or step absent from plan.
- **AX-4 Weakened criteria:** Acceptance/verification condition softened to unobservable or trivially satisfiable.
- **AX-5 Invented content:** Artifact introduces requirement/feature/capability not present in upstream source.

**Annotation rules:** Every Items Reviewed row in task-qualitative phase carries exactly one Axis value from `{AX-1..AX-5}` OR literal `none`; `Axis: drift-axis-inactive` permitted only when artifact has no citations to drift against; axes multiply lenses not checks (TOTAL stays at 15 items); Axis column task-qualitative-only.

## Component Inventory

### COMP-001 — task-builder/SKILL.md (Orchestrator)
**Type:** Internal Framework Skill (Stage A only — A.1-A.11 pipeline).
**Location:** `src/superclaude/skills/task-builder/SKILL.md` (1709 lines).
**Modifying FRs:** FR-CONV.1, FR-CONV.2, FR-CONV.3, FR-CONV.4, FR-CONV.5, FR-CONV.6.
**Dependencies:** Spawns rf-task-researcher, rf-task-builder, rf-qa, rf-analyst, rf-qa-qualitative; does NOT invoke rf-team-lead directly (Critical Rule #13).

### COMP-002 — rf-task-builder Agent
**Type:** Subagent (BUILD_REQUEST consumer).
**Location:** `src/superclaude/agents/rf-task-builder.md` (493 lines).
**Modifying FRs:** FR-CONV.5.
**Function:** Consumes BUILD_REQUEST; emits MDTM file at `${TASK_DIR}${TASK_ID}.md` (incremental write — header first, phases per Edit, Task Log last); 3 return flows: RESEARCH_NEEDED (max 2), MALFORMED (max 2 separate counter), NEED_USER_INPUT.

### COMP-003 — rf-qa Agent
**Type:** Structural QA Agent (4 phases: research-gate, synthesis-gate, report-validation, task-integrity).
**Location:** `src/superclaude/agents/rf-qa.md` (432 lines).
**Modifying FRs:** FR-CONV.1, FR-CONV.5, FR-CONV.6.
**Key anchors:** rf-qa.md:141-142 (zero-trust PASS/FAIL); rf-qa.md:268-287 (20-item checklist); rf-qa.md:49-77 (Parallel Partitioning); rf-qa.md:70-77 (DNSP edit site); rf-qa.md:~308-315 (Fix Cycle Protocol Rules).

### COMP-004 — rf-qa-qualitative Agent
**Type:** Content QA Agent (7 phases including task-qualitative; 15-item checklist + Self-Audit).
**Location:** `src/superclaude/agents/rf-qa-qualitative.md` (794 lines).
**Modifying FRs:** FR-CONV.3, FR-CONV.4, FR-CONV.6.
**Key anchors:** rf-qa-qualitative.md:527-583 (15-item checklist body); rf-qa-qualitative.md:675-714 (Items Reviewed table — axis column site); rf-qa-qualitative.md:766-775 (anti-inflation rule); rf-qa-qualitative.md:786-795 (severity floor); rf-qa-qualitative.md:794 (EOF — FR-CONV.3 append site).

### COMP-005 — rf-analyst Agent
**Type:** Completeness-verification + synthesis-review agent; partition adversary at Gates 1 and 2.
**Location:** `src/superclaude/agents/rf-analyst.md` (349 lines).
**Modifying FRs:** FR-CONV.6.
**Key anchors:** rf-analyst.md:58-71 (partition protocol + DNSP edit site).

### COMP-006 — rf-team-lead Agent (UNMODIFIED — preservation only)
**Type:** Project-mode orchestrator; escalation guard.
**Location:** `src/superclaude/agents/rf-team-lead.md` (431 lines).
**Modifying FRs:** None (line 417 NO-DRIFT preservation; verified 2026-05-14).
**Function:** rf-team-lead.md:417 — "max 3 cycles per phase ... HALT and ask user — do NOT proceed with unresolved findings." Activated by all-partitions-exhaust path (mutually exclusive with synthetic-dnsp).

**Component-to-FR matrix:**
| Component | FRs |
|---|---|
| task-builder/SKILL.md | 1, 2, 3, 4, 5, 6 |
| rf-qa.md | 1, 5, 6 |
| rf-qa-qualitative.md | 3, 4, 6 |
| rf-analyst.md | 6 |
| rf-task-builder.md | 5 |
| rf-team-lead.md | None (preservation) |

## Testing Strategy

**Test pyramid (adapted — agent-instruction text not executable code):** Synthetic Fixtures per-FR (100% AC coverage); Integration Tests (cross-FR composition); E2E Tests (full A.1-A.11 pipeline); Manual Audit (K-003 first-5-runs after FR-CONV.3). **Tooling:** Custom fixtures under test directory; `uv run pytest`. **Ownership:** Engineering for fixtures + integration; QA Lead for K-003 manual audit.

### TEST-001 — test_placeholder_tb_add_1 (FR-CONV.1)
TB-Add-1 fires on "TBD"/"TODO"/title-only checklist item. Assertion: TB-Add-1 emits item-ID-naming error; gate FAILs.

### TEST-002 — test_dag_cycle_tb_add_4 (FR-CONV.1)
TB-Add-4 fires on circular intra-/inter-phase dependency. Assertion: TB-Add-4 emits; gate FAILs.

### TEST-003 — test_evidence_bound_tb_add_8 (FR-CONV.1)
TB-Add-8 fires on bare `Context: src/foo` with no `:N` anchor (INV-015). Assertion: FAIL without anchor; PASS with `Context: src/foo:42`.

### TEST-004 — test_execution_context_full (FR-CONV.2)
3-labeled-line Execution Context block present in generated MDTM. Assertion: grep matches all 3 labeled lines.

### TEST-005 — test_execution_context_minimal_buildrequest (FR-CONV.2)
Minimal/sparse BUILD_REQUEST degrades header to References-only. Assertion: grep matches degraded form.

### TEST-006 — test_execution_context_no_file_paths (FR-CONV.2)
Header contains no specific file paths. Assertion: `grep -E "src/|/.*:[0-9]+"` against header block returns 0.

### TEST-007 — test_inherited_verdict_present (FR-CONV.3)
`## Inherited Structural Verdict` block appears in rf-qa-qualitative spawn prompt. Assertion: grep matches block header.

### TEST-008 — test_inherited_verdict_freshness_inv_002 (FR-CONV.3)
2-cycle fixture — cycle-2 spawn shows cycle-2 verdict, not stale cycle-1. Assertion: byte-diff of cycle-1 vs cycle-2 spawn prompts.

### TEST-009 — test_self_audit_inv_019 (FR-CONV.3)
rf-qa-qualitative output contains `## Self-Audit` with ≥1 documented semantic check beyond inherited verdict. Assertion: grep + content inspection.

### TEST-010 — test_dynamic_enumeration_inv_010 (FR-CONV.3)
When FR-CONV.1 TB-Add catalogue grows, rf-qa-qualitative checklist auto-richens. Assertion: structural diff of checklist before/after catalogue growth.

### TEST-011 — test_five_axes_overlay (FR-CONV.4)
`### Five Adversarial Axes` header appears BEFORE immutable 15-item checklist (rf-qa-qualitative.md:527). Assertion: grep ordering assertion.

### TEST-012 — test_axis_column_populated (FR-CONV.4)
Items Reviewed table (rf-qa-qualitative.md:675-714) carries non-empty Axis value on every row. Assertion: parse table; assert no empty Axis cell.

### TEST-013 — test_drift_axis_inactive_when_no_goal_baseline (FR-CONV.4)
No GOAL-baseline item present → `drift-axis-inactive` annotation emitted (not N/A). Assertion: grep matches annotation.

### TEST-014 — test_severity_floor_unweakened (FR-CONV.4)
rf-qa-qualitative severity floor (rf-qa-qualitative.md:786-795 — contradictions always IMPORTANT/CRITICAL) unchanged. Assertion: byte-diff of Critical Rules block.

### TEST-015 — test_monotonicity_halt_F_5_5_5 (FR-CONV.5)
3-cycle `|F|= 5, 5, 5` halts at cycle 2 with `[HALT-MONOTONICITY]|F|=5`; cycle 3 not attempted. Assertion: grep halt message + assert no cycle-3 log.

### TEST-016 — test_regression_halt_pass1_fail2 (FR-CONV.5)
Item 3.2 PASS@1 / FAIL@2 halts with verbatim regression message BEFORE monotonicity check. Assertion: grep message + ordering assertion.

### TEST-017 — test_slow_shrink_continues (FR-CONV.5)
`|F|= 5, 4` continues — strict shrink holds; X-003 slow-convergence threshold NOT triggered. Assertion: execution log shows cycle continues.

### TEST-018 — test_dnsp_twice_exhaust (FR-CONV.6)
Partition fixture timing out twice emits synthetic-dnsp finding with all 5 fixed fields. Assertion: parse YAML/block; assert all 5 fields populated.

### TEST-019 — test_dnsp_dedup_collapse (FR-CONV.6)
Two identical-`dedup_key` synthetic findings collapse into one record with `found_n_times=2`. Assertion: parse merged YAML; assert cardinality 1 + `found_n_times`.

### TEST-020 — test_dnsp_all_agents_fail_bypass (FR-CONV.6)
Zero partitions succeeded → no synthetic emits; existing rf-team-lead.md:417 escalation activates. Assertion: execution log shows HALT path; no synthetic block.

### TEST-021 — test_dnsp_does_not_serialize_cohort (FR-CONV.6 + NFR-CONV.10)
On one partition's escalation exhaust, N-1 sibling partitions continue concurrently to completion (INV-021). Assertion: spawn-log timing — N-1 partitions overlap exhausted partition's synthesis.

### TEST-022 — test_synthetic_dnsp_dedup_not_regression (FR-CONV.5 + FR-CONV.6 + INV-012)
Synthetic finding with same `dedup_key` in cycles 1+2 (other findings shrinking) proceeds to cycle 3 — no regression halt. Assertion: execution log shows cycle 3 attempted.

### TEST-023 — test_hidden_input_guard (NFR-CONV.3)
Fixture-populated `.dev/tasks/done/` yields byte-identical structural output vs empty-`done/` baseline. Assertion: byte-diff of structural fields.

### TEST-024 — test_sequencing_PR06_before_PR04 (INV-010)
If PR-04 (FR-CONV.3) lands before PR-06 (FR-CONV.1), dynamic enumeration still richens once catalogue activates. Assertion: structural assertion on enriched checklist.

### TEST-025 — test_invariant_preservation_NFR_6_through_10 (NFR-CONV.6..10)
All 5 invariants (self-contained-item, evidence-bound-item, persistent-artifact, zero-trust QA, parallel-research) preserved per Negative Criteria. Assertion: composite fixture exercising each invariant surface.

**Test environments:** Local development via UV (`uv run pytest`, `uv run pytest tests/path/ -v`) plus CI (GitHub Actions invoking `make test`). No external services, no containers, no network. `make verify-sync` runs in CI to confirm `src/superclaude/` and `.claude/` agree before suite executes.

## Migration and Rollout Plan

**Strategy:** Strictly-additive, per-FR serially-sequenced migration (governance assumption A-002). No data migration, no schema backfill, no cutover event. Each FR is its own commit; each commit independently revertable subject to co-revert matrix.

### MIG-001 — M1.1 FR-CONV.1 (PR-06) — lands 1st
**Description:** Append TB-Add-1..8 structural checks to rf-qa task-integrity checklist + mirror in 15-item validation block. Strictly-additive per A-002. **Duration:** TBD. **Dependencies:** Q-DM-1 Engineering Lead decision. **Rollback:** Revert specific TB-Add append lines individually OR full revert of PR-06 commit.

### MIG-002 — M1.2 FR-CONV.2 (PR-01) — lands 2nd
**Description:** Insert task-level `## Execution Context` header in generated MDTM files. Header scope-confined: NO file paths in header; per-item Context fields keep file:line citations. **Duration:** TBD. **Dependencies:** M1.1 PASS. **Rollback:** Disable header generation; per-item Context fields unchanged so MDTM files degrade gracefully.

### MIG-003 — M1.3 FR-CONV.3 (PR-04) — lands 3rd
**Description:** Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt under `## Inherited Structural Verdict`. **Duration:** TBD. **Dependencies:** M1.2 PASS. **Rollback:** Disable passthrough block; rf-qa-qualitative falls back to current behavior (independent structural re-checking).

### MIG-004 — M1.4 FR-CONV.4 (PR-07) — lands 4th
**Description:** Insert "Five Adversarial Axes" header subsection BEFORE rf-qa-qualitative's 15-item checklist + axis-annotation column on Items Reviewed table. Overlay-only. **Duration:** TBD. **Dependencies:** M1.3 PASS. **Rollback:** Remove axis column + `drift-axis-inactive` annotation; 15-item checklist untouched.

### MIG-005 — M1.5 FR-CONV.5 (PR-02) — lands 5th
**Description:** Add two stop-conditions (monotonicity guard + regression detection) to EXISTING retry loops. No new loop/stage. **Duration:** TBD. **Dependencies:** M1.4 PASS. **Rollback:** Disable two guards individually; existing retry loops + per-gate caps continue to govern.

### MIG-006 — M1.6 FR-CONV.6 (PR-03 BASE) — lands 6th
**Description:** Emit synthetic HIGH-severity `synthetic-dnsp` finding when partition agent's escalation ladder exhausts. All-agents-fail guard preserved. **Duration:** TBD. **Dependencies:** M1.5 PASS. **Rollback:** Revert DNSP edit sites; existing rf-team-lead.md:417 all-agents-fail escalation already handles zero-partitions-succeeded path.

### MIG-007 — M1.7 Post-merge audit + NFR-CONV.4 measurement
**Description:** Audit first 5 rf-qa-qualitative runs after FR-CONV.3 lands (K-003 / X-002 audit-target); measure token-cost on 5 representative BUILD_REQUESTs (NFR-CONV.4 ≤10% ceiling). **Duration:** 1-2 weeks. **Dependencies:** All 6 FRs landed. **Rollback:** If audit shows inflation → roll back FR-CONV.3. If token ceiling exceeded → summarise FR-CONV.3 verdict table rather than emit verbatim (K-010 contingency).

**Feature flags (logical, no runtime flag system):**
| Flag | Default | Cleanup | Owner |
|---|---|---|---|
| TB_ADD_1_THROUGH_8 | Enabled at merge | GA + 30 days; TB-Add-2 advisory→hard pending Phase-2 | rf-qa maintainer |
| EXECUTION_CONTEXT_HEADER | Enabled at merge | GA + 30 days | task-builder maintainer |
| INHERITED_STRUCTURAL_VERDICT | Enabled at merge | Post-K-003 audit pass | QA Lead |
| FIVE_ADVERSARIAL_AXES | Enabled at merge | GA + 30 days | rf-qa-qualitative maintainer |
| RETRY_MONOTONICITY_GUARDS | Enabled at merge | GA + 30 days | rf-task-builder maintainer |
| SYNTHETIC_DNSP_EMISSION | Enabled at merge | GA + 30 days | rf-analyst / rf-qa maintainers |

**Rollout stages:** Stage 0 (Pre-merge — Q-DM-1 resolution); Stages 1-6 (serial FR landing with `make verify-sync` PASS gate per FR); Stage 7 (post-merge audit window 1-2 weeks); Stage 8 (GA + 30 days — fallback paths removed).

**Rollback co-revert matrix:**
| Reverted FR | Co-Revert Required | Reason |
|---|---|---|
| FR-CONV.5 | FR-CONV.6 dedup-key emission | INV-012 composition no longer needed |
| FR-CONV.1 | FR-CONV.3 dynamic-enumeration consumer | INV-010 — TB-Add catalogue is enumeration source |
| FR-CONV.2, FR-CONV.4 | Independently revertable | A-002 strictly-additive |
| FR-CONV.6 | FR-CONV.5 `\|F_n\|` definition adjustment | Inverse edge — treat FR-CONV.5/6 pair as jointly revertable |

## Operational Readiness

### OPS-001 — K-003 audit-target (first 5 rf-qa-qualitative runs post-FR-CONV.3)
**Symptoms:** rf-qa-qualitative output missing `## Self-Audit` section OR Self-Audit shows zero independent semantic checks. **Diagnosis:** Read `.dev/tasks/to-do/TASK-*/reviews/qa-qualitative-review.md`; grep for `## Self-Audit`; verify ≥1 semantic check beyond inherited PASS. **Resolution:** If missing — prompt FR-CONV.3 spawn-prompt; if zero independent checks — K-003 FAIL → disable passthrough flag (§19.2). **Escalation:** QA Lead immediate; Engineering Lead if pattern across all 5 runs. **Prevention:** INV-019 mandatory Self-Audit listing.

### OPS-002 — DNSP triage (synthetic-dnsp emission count >0 in production)
**Symptoms:** rf-qa report contains `synthetic-dnsp` finding (HIGH severity). **Diagnosis:** Read affected partition's spawn-log (cited in `evidence` field); identify root cause of escalation-ladder exhaust; check `dedup_key` for prior similar events. **Resolution:** Manual investigation per `recommendation` field; consider whether root cause should land as new TB-Add. **Escalation:** rf-qa maintainer; escalate to Engineering if ≥3 distinct dedup-keys in a week. **Prevention:** Inspect synthetic-dnsp emission-count metric weekly.

### OPS-003 — All-partitions-exhaust HALT (no DNSP emitted)
**Symptoms:** rf-team-lead HALTs and asks user; zero partitions succeeded. **Diagnosis:** Confirm zero partition successes in spawn-log; verify line-417 escalation path fired and NO synthetic-dnsp emitted (correct per FR-CONV.6 mutual-exclusivity). **Resolution:** This is preserved all-agents-fail guard, not a defect — user resolves unresolved findings before re-run. **Escalation:** rf-team-lead maintainer if HALT misfires when ≥1 partition succeeded. **Prevention:** Mutual-exclusivity check in FR-CONV.6 emission logic.

### OPS-004 — `[HALT-MONOTONICITY]` rate >50% of fix-cycle batches
**Symptoms:** Many fix-loops halting before convergence with `[HALT-MONOTONICITY] |F|=<n>`. **Diagnosis:** Sample 3 halt events; inspect BUILD_REQUESTs for upstream defects; inspect generated MDTM for structural issues. **Resolution:** Improve upstream BUILD_REQUESTs; consider TB-Add-2 calibration (OPEN-INV-006). **Escalation:** rf-task-builder maintainer. **Prevention:** Upstream BUILD_REQUEST quality gates.

### OPS-005 — Regression-halt rate >20% of fix-cycle batches
**Symptoms:** Many fix-cycles emitting verbatim regression halt message. **Diagnosis:** Sample 3 regression events; inspect what changed between cycles; look for fix-cycle pattern introducing collateral damage. **Resolution:** Tighten fix-cycle prompts (note: X-003 slow-convergence threshold REJECTED). **Escalation:** Engineering Lead. **Prevention:** Regression-detection precedence rule.

### OPS-006 — `make verify-sync` FAIL post-FR-merge
**Symptoms:** Sync verification fails between `src/superclaude/` and `.claude/`. **Diagnosis:** Re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline rule (A-001) followed. **Resolution:** Re-sync; commit only on PASS; if persistent, revert `.claude/` direct edit and re-run from `src/superclaude/` (K-009 contingency). **Escalation:** Per-commit author. **Prevention:** Pre-commit hook enforcement of `make verify-sync`.

### OPS-007 — INV-018 layout change detected (K-008)
**Symptoms:** `.dev/tasks/` directory schema differs from pre-merge. **Diagnosis:** Inspect all 6 FRs for path/naming references; re-integrate at new layout. **Resolution:** Re-integration commit covering all 6 FRs per §19.4 dependency matrix. **Escalation:** Engineering Lead + orchestrator. **Prevention:** SP-33 stability commitment + portfolio-wide layout-change contract.

**On-call expectations:** task-builder maintainers (rotating); page volume <2/week at steady state; required response — K-003 audit failure 4 business hours, DNSP triage 24 hours, `make verify-sync` FAIL immediate; knowledge prerequisites — task-builder skill v3.9 architecture, rf-qa.md / rf-qa-qualitative.md gate semantics, rf-team-lead.md:417 escalation ladder, sync workflow per CLAUDE.md (A-001).

**Capacity planning:** N/A — internal skill with no infrastructure scaling. NFR-CONV.5 forbids new external dependencies or synchronous network calls. No database, storage, or compute resources to project.

**Observability:** Logs — rf-task-builder execution log, rf-qa gate reports (4 phases), rf-qa-qualitative reports (8 phases) with new Axis column, synthetic-dnsp findings, spawn logs (FR-CONV.6 evidence field at canonical path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`). Metrics — synthetic-dnsp emission count (counter; threshold >0 in production triggers human review), `[HALT-MONOTONICITY]` count (threshold >50% of batches), regression-halt count (threshold >20% of batches), Self-Audit coverage (gauge — 100% on first 5 runs after FR-CONV.3 — K-003 audit-fail blocks release if <100%), `make verify-sync` PASS rate (threshold 100%). Tracing — N/A (single-process spawning model). Alerts — N/A in v3.9 (offline measurement on 5 representative BUILD_REQUESTs per NFR-CONV.4). Dashboards — N/A.
