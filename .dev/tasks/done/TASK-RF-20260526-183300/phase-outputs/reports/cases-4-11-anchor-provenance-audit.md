---
phase: 6
step: 6.4
title: Cases 4-11 Anchor / Provenance Audit
status: BLOCKED (rerun pending) with pre-rerun baseline notes
created_date: 2026-05-26
task_id: TASK-RF-20260526-183300
---

# Cases 4-11 Anchor / Provenance Audit

This audit inspects each of cases 4-11 for dedicated `## Provenance` sections and critical seed-anchor disposition. Because cases have NOT been re-run against the Phase 2-3 protocol changes (see `cases-4-11-rerun-instructions.md`), the existing `live-runs/eval-*/` artifacts reflect the PRE-remediation regression baseline. Audit verdicts are accordingly BLOCKED until rerun, with pre-rerun observations recorded as evidence of the regression that Phase 2-3 is designed to fix.

Case 12 (`architecture-graphql-public-api`) is excluded from this audit — registry compatibility is out of scope.

**Verdict legend:** PASS = post-remediation criterion met; FAIL = post-remediation criterion not met; BLOCKED = cannot evaluate post-remediation criterion because rerun has not occurred.

## Pre-Rerun Section Inventory (Evidence of Baseline Regression)

Grep of `live-runs/eval-<case>/merged-requirements.md` for Phase-2-mandated section headings:

| Case | `## Provenance` present? | Other Phase-2 sections detected |
|------|-------------------------|--------------------------------|
| 4 `code-migrate-pytest-vitest` | NO | `## Out of Scope` (seed-brief level) |
| 5 `architecture-worker-pool-errors` | YES | — |
| 6 `process-contributor-onboarding` | YES | — |
| 7 `research-bun-vs-node` | NO | — |
| 8 `code-api-caching-tasklist` | NO | — |
| 9 `code-feature-flag-task` | NO | — |
| 10 `incident-payment-webhook-q1` | NO | `## Out of Scope` (seed-brief level) |
| 11 `code-duplicate-auth-blind` | NO | — |

Pre-rerun result: 6 of 8 cases (75%) missing dedicated `## Provenance`. Acceptance criterion 6 (Phase 6.3 row 6) target is 0 missing. Phase 2 protocol contract now mandates this section for every case; rerun is expected to produce 0 missing.

## Per-Case Verdict

### Case 4 — `code-migrate-pytest-vitest`

- **Provenance section status:** Pre-rerun: missing. Phase 2 contract mandates dedicated `## Provenance` in merged-requirements.
- **Preserved anchors:** Cannot determine post-remediation state. Pre-Phase-2 seed brief lacks `Context Anchors`, `Must Preserve`, and structured anchor extraction; pre-rerun artifact has no deterministic anchor record to audit against.
- **Dropped anchors with rationale:** Cannot determine post-remediation state for the same reason.
- **Critical unresolved loss:** Pre-rerun comparison shows -38.46% structural delta (16/26 vs 26/26) — proposal_count and merged frontmatter assertions failed (per `comparison-against-iteration-2.json:92-204`).
- **Verdict:** **BLOCKED**. Resume after rerun produces post-remediation seed-brief with `## Intent Summary` + `## Context Anchors` + `## Must Preserve` + `## Out of Scope` and merged-requirements with dedicated `## Provenance`.

### Case 5 — `architecture-worker-pool-errors`

- **Provenance section status:** Pre-rerun: PRESENT (`## Provenance` detected). This case did not regress structurally (27/27 baseline vs 27/27 live in pre-rerun comparison).
- **Preserved anchors:** Cannot determine post-remediation state systematically — pre-rerun seed-brief lacks structured Context Anchors.
- **Dropped anchors with rationale:** Cannot determine.
- **Critical unresolved loss:** None observed structurally pre-rerun; qualitative regression status unknown until quality grading covers this case.
- **Verdict:** **BLOCKED**. The presence of `## Provenance` pre-rerun is a positive signal that the case 5 prior run already met part of the Phase 2 contract; rerun will confirm whether the full Phase 2 schema is satisfied (Context Anchors / Must Preserve / Intent Summary / Out of Scope / canonical six sections / return-contract Phase 2 fields).

### Case 6 — `process-contributor-onboarding`

- **Provenance section status:** Pre-rerun: PRESENT.
- **Preserved anchors:** Cannot determine post-remediation state.
- **Dropped anchors with rationale:** Cannot determine.
- **Critical unresolved loss:** Pre-rerun -16.00% structural delta (21/25 vs 25/25); proposal_count and agent_spec assertions failed.
- **Verdict:** **BLOCKED**. Provenance present in baseline is encouraging but the structural regression indicates other Phase 2 schema fields are missing.

### Case 7 — `research-bun-vs-node`

- **Provenance section status:** Pre-rerun: missing.
- **Preserved anchors:** Cannot determine post-remediation state.
- **Dropped anchors with rationale:** Cannot determine. Pre-rerun Risks-section parsing failed (table-shaped Risks not counted) — Phase 4 grader now supports `section_items_or_table_rows` so rerun assertions should resolve this.
- **Critical unresolved loss:** Pre-rerun -13.04% structural delta.
- **Verdict:** **BLOCKED**.

### Case 8 — `code-api-caching-tasklist`

- **Provenance section status:** Pre-rerun: missing.
- **Preserved anchors:** Cannot determine.
- **Dropped anchors with rationale:** Cannot determine. Pre-rerun architect/refactorer + model alias assertions failed (per `comparison-against-iteration-2.json:1116-1126`).
- **Critical unresolved loss:** Pre-rerun -16.00% structural delta; handoff-tasklist case specifically.
- **Verdict:** **BLOCKED**.

### Case 9 — `code-feature-flag-task`

- **Provenance section status:** Pre-rerun: missing.
- **Preserved anchors:** Cannot determine.
- **Dropped anchors with rationale:** Cannot determine. Pre-rerun -8.33% structural delta (11/12 vs 12/12); handoff-task case.
- **Critical unresolved loss:** Smaller regression than other cases but still missing Provenance.
- **Verdict:** **BLOCKED**.

### Case 10 — `incident-payment-webhook-q1`

- **Provenance section status:** Pre-rerun: missing.
- **Preserved anchors:** Cannot determine.
- **Dropped anchors with rationale:** Cannot determine. Pre-rerun interactive tagging failed (per `comparison-against-iteration-2.json:1420-1424`).
- **Critical unresolved loss:** Pre-rerun -25.00% structural delta (21/28 vs 28/28). This is one of the larger regressions; interactive + enterprise + deep depth case.
- **Verdict:** **BLOCKED**. Phase 2 added `expected_interactive_mode` per-case key plus `seed_brief_frontmatter_has_interactive_mode_when_expected` assertion; rerun is expected to address this.

### Case 11 — `code-duplicate-auth-blind`

- **Provenance section status:** Pre-rerun: missing.
- **Preserved anchors:** Cannot determine.
- **Dropped anchors with rationale:** Cannot determine. Pre-rerun blind-mode assertions failed for both seed and merged frontmatter, plus Agent A-E label assertions (per `comparison-against-iteration-2.json:1676-1782`); also `adversarial_status='success'` where assertion expected `pass`.
- **Critical unresolved loss:** Pre-rerun -29.63% structural delta (19/27 vs 27/27). Blind mode specifically — Phase 2 added `expected_blind_mode` per-case key and Phase 4 added `blind_mode_anonymized_agent_spec_labels` + `blind_mode_anonymized_debate_labels` text assertions to grader.
- **Verdict:** **BLOCKED**.

## Aggregate Status

| Status | Count | Cases |
|--------|-------|-------|
| PASS | 0 | (none — measurable only after rerun) |
| FAIL | 0 | (none — measurable only after rerun) |
| BLOCKED | 8 | 4, 5, 6, 7, 8, 9, 10, 11 |

All 8 cases are BLOCKED pending operator-driven rerun. Pre-rerun observations confirm the regression Phase 2-3 is designed to fix is currently present (6 of 8 cases missing Provenance, multiple cases with structural-delta -16% to -38%). The remediation machinery is in place (PG-2/3/4/5 PASS verdicts); only the empirical re-measurement is outstanding.

## Discipline

- Missing rerun artifacts are treated as BLOCKED, NOT silently as PASS or FAIL.
- Pre-rerun observations are recorded as evidence of baseline regression, not as remediated state.
- Rerun must follow `cases-4-11-rerun-instructions.md` exactly (fresh session per case, verbatim prompts, no case 12).

## Resolution Path

1. Operator executes rerun per `cases-4-11-rerun-instructions.md`.
2. Operator re-runs `uv run python .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py` and qualitative grading.
3. Re-resume this task; re-audit each case section above with PASS/FAIL based on the regenerated artifacts.
4. Update `remediation-acceptance-matrix.md` rows 1-7 with post-rerun PASS/FAIL verdicts.
5. PG-6 qualitative review then has evidence to evaluate against.
