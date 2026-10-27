# Refactoring Plan — task-builder-merge Portfolio

## Overview

- **Base proposal**: PR-03 (DNSP Synthetic Finding) — combined score 0.959, tiebreaker by debate performance.
- **Incorporated proposals**: PR-02, PR-06, PR-04, PR-07 (ADOPT) + PR-01 (REVISE-then-adopt) + PR-05 (REVISE-defer-to-Phase-2)
- **Change count**: 6 portfolio entries + 1 deferral + 8 cross-cutting acceptance criteria
- **Risk profile**: Low-to-Medium (no HIGH-severity invariant violations; 5 MEDIUM invariant concerns addressed via acceptance criteria)
- **Merged output type**: consolidated portfolio document (not a single proposal replacement)

## Adoption Sequencing (recommended landing order)

The merge plan adopts a specific landing sequence that resolves INV-010 (PR-04/PR-06 sequencing) and INV-012 (PR-02/PR-03 stacking):

1. **PR-06 lands first** — establishes the TB-Add-1 through TB-Add-7 structural catalogue. TB-Add-7 = "Execution Context source-areas re-appear in items" (absorbed from PR-01 failure-mode #4).
2. **PR-01 lands second** — introduces the task-level Execution Context block; validated by PR-06's TB-Add-7. Add structural-test acceptance criterion for INV-015 (scope-confinement).
3. **PR-04 lands third** — inherited structural verdict propagation; richens automatically as PR-06's catalogue is in place. Acceptance criterion for INV-002 (verdict re-injection on subsequent fix cycles).
4. **PR-07 lands fourth** — 5-axis overlay on rf-qa-qualitative; clean composition with PR-04's inherited verdict.
5. **PR-02 lands fifth** — monotonicity + regression detection stop conditions; acceptance criterion for INV-012 (PR-03 synthetic findings as failure-count input).
6. **PR-03 lands sixth** — DNSP synthetic-finding emission at partition boundary; independent of the gate-pipeline edits. Could land in parallel with PR-02 but conventionally last because base.
7. **PR-05 DEFERRED to Phase-2** with explicit trigger: re-evaluate when `.dev/tasks/done/` has ≥10 completed tasks of ≥3 distinct task_types.

## Planned Changes

### Change #1 — Adopt PR-06 (Structural Gate Additions)

- **Source variant**: PR-06 (CASE-D, combined score 0.963, ADOPT verdict)
- **Target location**: `src/superclaude/agents/rf-qa.md:264-287` (20-item task-integrity checklist) + `src/superclaude/skills/task-builder/SKILL.md:898-906` (9-item A.10) + `src/superclaude/skills/task-builder/SKILL.md:1491-1507` (15-item validation)
- **Integration approach**: APPEND — add 7 new items (TB-Add-1 through TB-Add-7) to existing checklists. Each item cites source check ID from sc:tasklist (11/13/14/15/16/17) for traceability.
- **TB-Add list**:
  - TB-Add-1: Placeholder scan ("TBD"/"TODO"/title-only)
  - TB-Add-2: Item count bounds (≥3 / ≤40 track / ≤50 single-track) **ADVISORY-fail until calibrated** (INV-006)
  - TB-Add-3: Clarification adjacency to blocked items
  - TB-Add-4: Circular dependency detection (DAG check)
  - TB-Add-5: Granularity check (XL items have subtasks)
  - TB-Add-6: Confidence/Verification format consistency
  - TB-Add-7: Execution Context source-areas reappear in items (absorbed from PR-01 failure-mode #4)
- **Rationale**: CB-3 per-check classification (no bulk import). Debate per-point matrix: PR-06 wins C-002 (75%), C-003 (70%), invariant subtotal 5/5. zero-trust QA strengthened.
- **Risk level**: Low (additive; TB-Add-2 ADVISORY-fail mitigates calibration uncertainty)
- **Acceptance criterion**: Each TB-Add check produces a clear error message naming the offending item ID. TB-Add-2 emits warning, not block, until empirical calibration completes.

### Change #2 — Adopt PR-01 (Execution Context Header) with REVISE acceptance criterion

- **Source variant**: PR-01 (CASE-D, combined score 0.912, REVISE verdict)
- **Target location**: `src/superclaude/skills/task-builder/SKILL.md:228-238` (template-selection) + SKILL.md:1409-1485 (output schema) + new instruction at SKILL.md:719 (rf-task-builder spawning)
- **Integration approach**: INSERT — task-level `## Execution Context` block after frontmatter, before checklist.
- **Block contents**: References (BUILD_REQUEST GOAL, WHY, related-doc IDs), Source areas (named modules, NEVER paths), Key constraints (top 1-3 invariants from BUILD_REQUEST).
- **Rationale**: Closes U-001 (no other proposal addresses task-level executor readability). Scope-confinement preserves evidence-bound-item invariant (cite proposal line 34).
- **REVISE acceptance criterion (resolves INV-015)**: Add an rf-qa A.10 structural check: "Every per-item Context field that references a code surface includes at least one file:line citation OR a justified absence comment." This is a new check separate from TB-Add-7. Mark as TB-Add-8.
- **Risk level**: Low — header is optional; failure modes documented in proposal.

### Change #3 — Adopt PR-04 (Gate Results Passthrough)

- **Source variant**: PR-04 (CASE-B, combined score 0.934, ADOPT verdict)
- **Target location**: `src/superclaude/skills/task-builder/SKILL.md:923-1000` (A.10.5 spawn) + `src/superclaude/agents/rf-qa-qualitative.md:794` (passthrough reference)
- **Integration approach**: INSERT — rf-qa-qualitative spawn prompt includes `## Inherited Structural Verdict` section with rf-qa's table verbatim + instruction "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH."
- **Rationale**: Operationalises rf-qa-qualitative.md:794 stated rule. Per-point matrix: PR-04 wins X-002 (65%), U-004 (78%). Lowest implementation risk in portfolio.
- **Acceptance criterion (INV-002)**: When rf-qa re-runs after a fix cycle, orchestrator MUST re-inject the new verdict; rf-qa-qualitative MUST NOT use a stale verdict from a prior cycle. Add unit-test-equivalent in rf-task-builder.md spawning logic.
- **Acceptance criterion (INV-010 sequencing)**: PR-04 prompt template uses dynamic checklist enumeration that auto-picks up PR-06's TB-Add items. No manual template edit required when TB-Adds go live.
- **Acceptance criterion (INV-019 anti-inflation)**: rf-qa-qualitative's first run after PR-04 lands must produce a Self-Audit entry listing relied-on rf-qa PASS items AND include at least one semantic check where rf-qa PASS is insufficient (e.g., section-content-quality vs. section-numbering).
- **Risk level**: Low — anti-inflation rule strengthened, not weakened.

### Change #4 — Adopt PR-07 (Adversarial Category Naming)

- **Source variant**: PR-07 (CASE-D, combined score 0.913, ADOPT verdict)
- **Target location**: `src/superclaude/agents/rf-qa-qualitative.md:527-583` (task-qualitative phase) + output template ~675-714 + SKILL.md:961 reference
- **Integration approach**: INSERT — "Five Adversarial Axes" header subsection BEFORE existing 15-item checklist + axis annotation requirement on Items Reviewed table.
- **Axes**: drift, contradictions, omissions, weakened criteria, invented content.
- **Rationale**: Lowest over-engineering risk (per author line 13). Per-point matrix: PR-07 wins C-004 (72%). Pure intent-port.
- **Acceptance criterion (PR-07 failure-mode #3 drift baseline)**: rf-qa-qualitative's task-qualitative checklist MUST contain an item that captures BUILD_REQUEST.GOAL verbatim BEFORE the drift check is applied. If no such item exists, drift axis is INACTIVE for this task; surface as `drift-axis-inactive` annotation.
- **Risk level**: Low — naming-only overlay; no code-path changes.

### Change #5 — Adopt PR-02 (Retry Monotonicity Guards)

- **Source variant**: PR-02 (CASE-D, combined score 0.965, ADOPT verdict)
- **Target location**: `src/superclaude/skills/task-builder/SKILL.md:870, 1550` (new "Retry Monotonicity Protocol" subsection) + `src/superclaude/agents/rf-task-builder.md:336-359` + `src/superclaude/agents/rf-qa.md:310-313`
- **Integration approach**: INSERT — two stop conditions (monotonicity guard + regression detection) plug into existing retry loops; no new loop or stage.
- **Rationale**: Per-point matrix: PR-02 wins X-003 (85%), C-005 (80%), U-002 (90%). Highest quant score (0.965). Addresses documented oscillation defect.
- **Precedence rule (PR-02 Round-2 spec)**: Regression > monotonicity. Halt message format: "Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check."
- **Acceptance criterion (INV-012)**: Synthetic findings from PR-03 DNSP COUNT as failures for |F_n| monotonicity, BUT a synthetic for the same `(assigned_files_range, escalation_ladder_exhaust_point)` key across consecutive cycles is a dedup case (PR-03 failure-mode #4), not a regression. Explicit specification in the Retry Monotonicity Protocol subsection.
- **Risk level**: Low — stop-conditions strengthen, never loosen.

### Change #6 — Adopt PR-03 (DNSP Synthetic Finding) — BASE

- **Source variant**: PR-03 (CASE-B, combined score 0.959, ADOPT verdict, BASE)
- **Target location**: `src/superclaude/skills/task-builder/SKILL.md:574-654` (A.8 research gate) + `src/superclaude/skills/task-builder/SKILL.md:872-916` (A.10 task integrity) + `src/superclaude/agents/rf-analyst.md:60-69` + `src/superclaude/agents/rf-qa.md:70-77` + optionally `src/superclaude/agents/rf-qa-qualitative.md:72-78`
- **Integration approach**: INSERT — "DNSP Synthetic Finding Protocol" paragraph + 3-bullet emission contract in each agent's partition-protocol section.
- **Emission contract**:
  - severity: HIGH
  - source: "synthetic-dnsp"
  - affected_range: agent's assigned_files slice
  - evidence: spawn-log path (or stub citing log absence)
  - recommendation: "Manual review required — partition agent failed twice"
- **Dedup key (Round-2 spec)**: `(assigned_files_range, escalation_ladder_exhaust_point)`. Two synthetic findings with identical key collapse into one with a "found N times" note.
- **Rationale**: PR-03 wins C-001 (88% — only invariant-double-reinforcement), C-007 (92% — most ready), U-003 (92% — paradigm-neutral). External evidence P3 39/50 unique in portfolio.
- **Risk level**: Low — DNSP fires only after escalation ladder exhausts; existing all-agents-fail guard preserved.

### Change #7 — Defer PR-05 (Tier History Advisory) to Phase-2

- **Source variant**: PR-05 (CASE-D, combined score 0.862, REVISE verdict — Phase-2 deferral)
- **Disposition**: NOT adopted in Phase-1. Explicitly entered into the portfolio as a Phase-2 candidate.
- **Re-evaluation trigger**: `.dev/tasks/done/` accumulates ≥10 completed tasks of ≥3 distinct task_types.
- **Rationale**: Author-acknowledged Phase-2 framing (proposal line 12, 61). INV-003 MEDIUM invariant concern (advisory operational obedience cannot be structurally enforced). Lowest combined score among 7 proposals.
- **Action**: Document Phase-2 candidacy in merged-output portfolio document. No SKILL.md or agent edits at this time.

## Changes NOT Being Made

Document transparency — proposals/aspects considered and rejected:

### Rejected: PR-01 "no specific file paths in task-level header" rule applied to per-item Context fields (X-001)

- **PR-01 proposed scope**: Header-only. Other variants implicitly considered whether the rule should extend to all task content.
- **Decision**: REJECT extension. PR-01's scope-confinement (line 34) is correct: per-item Context and research/*.md MUST retain file:line citations per evidence-bound-item invariant.
- **Rationale**: cite invariant evidence-bound-item; cite Round-1 PR-01 advocate statement strength #2.

### Rejected: PR-04 "rely on rf-qa verdict for verification" without re-running semantic checks (X-002)

- **Decision**: REJECT. PR-04 line 50 + Round-2 rebuttal commit to: "rf-qa PASS items skip structural re-checking but each semantic check requires your own tool engagement." Mechanical re-checking is skipped; semantic verification is not.
- **Rationale**: anti-inflation rule rf-qa-qualitative.md:766-775 preserved.

### Rejected: PR-02 "halt on slow convergence" (e.g., F_{n+1} = F_n - 1) (X-003)

- **Decision**: REJECT. PR-02 monotonicity fires only on strict NON-shrink. Any forward motion permits continuation.
- **Rationale**: preserves legitimate multi-cycle correction tolerance.

### Rejected: PR-05 "modify tier selection based on historical pattern" (X-004)

- **Decision**: REJECT. Advisory-only framing preserved. Rule-based selection (SKILL.md:96-101) is the binding mechanism.
- **Rationale**: hidden-input regression risk; LLM agent obedience to disclaimer is operationally unproven.

### Rejected: Bulk-port of all 17 sc:tasklist gate checks (PR-06 alternative)

- **Decision**: REJECT bulk import per CB-3. Only the 6-7 specific checks NOT already in task-builder's existing checklists are imported.
- **Rationale**: avoids gate redundancy and bundle-specific machinery that doesn't apply to single-task output.

## Risk Summary

| Change | Risk Level | Impact if Wrong | Rollback Path |
|--------|------------|-----------------|---------------|
| #1 PR-06 structural checks | Low | False positives waste fix-cycles | Remove TB-Add items individually; TB-Add-2 already ADVISORY |
| #2 PR-01 Execution Context | Low | Header drift, executor confusion | Make header generation conditional; remove block |
| #3 PR-04 passthrough | Low | Inflation risk if anti-inflation prompt fails | Disable passthrough; rf-qa-qualitative falls back to current behavior (failure-mode #1) |
| #4 PR-07 5-axis overlay | Low | Axis ambiguity over-flagging | Remove axis annotation requirement; checklist runs unchanged |
| #5 PR-02 monotonicity | Low | Premature halt of legitimate slow-cycle correction | Strict-shrink threshold prevents this; rollback by disabling guards individually |
| #6 PR-03 DNSP | Low | Synthetic findings mask real issues (proposal failure-mode #3) | HIGH severity ensures visibility; all-agents-fail guard preserves existing behavior |
| #7 PR-05 deferral | None | (no change) | n/a |

**Overall portfolio risk**: Low. No HIGH-severity invariant violations. 5 MEDIUM concerns all addressed via acceptance criteria above.

## Cross-Cutting Acceptance Criteria

These criteria apply to the portfolio as a whole:

1. **Sync-discipline (A-001)**: All 6 adopted changes edit `src/superclaude/skills/task-builder/SKILL.md` and/or `src/superclaude/agents/rf-*.md`. After integration, `make sync-dev` MUST run, and `make verify-sync` MUST pass before commit.
2. **Zero-trust governance (A-002)**: Every adopted gate-touching change (PR-02, PR-03, PR-04, PR-06, PR-07) MUST be additive — no existing check removed or weakened.
3. **CASE-label adaptability (A-003)**: The portfolio explicitly documents PR-05's Phase-2 deferral as a CASE-label adaptability case. If similar future evidence emerges, CASE classifications may be re-evaluated.
4. **Invariant probe MEDIUMs**: 5 MEDIUM invariant concerns (INV-002, INV-003, INV-010, INV-012, INV-015) — all addressed in per-change acceptance criteria above.
5. **Test/validation gate**: After all 6 changes land, run a fresh task-builder pipeline end-to-end against a synthetic BUILD_REQUEST with all 5 invariants exercised. Verify:
   - Per-item Context fields retain file:line citations (INV-015)
   - Inherited verdict re-injected on fix-cycle re-runs (INV-002)
   - PR-06 TB-Add-7 cross-validates PR-01 header (INV-011)
   - PR-02 monotonicity correctly classifies PR-03 synthetics (INV-012)
   - PR-07 drift axis becomes INACTIVE when no GOAL-baseline item exists
6. **PR-05 Phase-2 trigger**: After 10+ completed tasks accumulate, re-run adversarial scoring on PR-05 with the new data context.
7. **Sequencing enforcement**: Land in the order: PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03. Land PR-05 separately when triggered.
8. **Provenance annotations**: Merged output document MUST include per-section attribution to source proposal.

## Review Status

- Default: Auto-approved (non-interactive mode).
- Approval timestamp: 2026-05-14.
- All decisions documented with debate-evidence citations and per-point matrix references.
