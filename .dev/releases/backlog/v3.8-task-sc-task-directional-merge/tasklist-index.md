# TASKLIST INDEX -- `/task` ← `/sc:task` Directional Feature-Transfer Merge

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | `/task` ← `/sc:task` Directional Feature-Transfer Merge |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-05-14 |
| TASKLIST_ROOT | `.dev/releases/current/task-sc-task-directional-merge/` |
| Total Phases | 8 |
| Total Tasks | 38 (30 regular + 8 checkpoint) |
| Total Deliverables | 38 (30 D-#### + 8 D-CP##) |
| Complexity Class | COMPLEX |
| Primary Persona | architect |
| Consulting Personas | analyzer, refactorer, qa, scribe |
| Sprint Type | Directional feature-transfer with adversarial gating (NOT neutral comparison) |
| Recipient Surface | `/task` (MDTM Task File Executor) -- base, retained |
| Donor Surface | `/sc:task` (Unified Task Command) -- absorbed-then-deprecated |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/phase-5-tasklist.md` |
| Phase 6 Tasklist | `TASKLIST_ROOT/phase-6-tasklist.md` |
| Phase 7 Tasklist | `TASKLIST_ROOT/phase-7-tasklist.md` |
| Phase 8 Tasklist | `TASKLIST_ROOT/phase-8-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/artifacts/` |
| Validation Reports | `TASKLIST_ROOT/validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Recipient & Donor Inventory | T01.01-T01.04 | EXEMPT: 3, LIGHT: 1 |
| 2 | phase-2-tasklist.md | Donor Feature Characterization | T02.01-T02.05 | EXEMPT: 4, LIGHT: 1 |
| 3 | phase-3-tasklist.md | Recipient Integration Surface & Invariant Bound | T03.01-T03.04 | EXEMPT: 3, LIGHT: 1 |
| 4 | phase-4-tasklist.md | Adversarial Debate & Stack Rank (`/sc:adversarial`) | T04.01-T04.06 | STANDARD: 5, LIGHT: 1 |
| 5 | phase-5-tasklist.md | Synthesis -- Ranked Feature Transfer Manifest | T05.01-T05.04 | STANDARD: 3, LIGHT: 1 |
| 6 | phase-6-tasklist.md | Directional Merge Plan | T06.01-T06.06 | STRICT: 5, LIGHT: 1 |
| 7 | phase-7-tasklist.md | Validation & Adversarial Re-Review | T07.01-T07.05 | STRICT: 4, LIGHT: 1 |
| 8 | phase-8-tasklist.md | Sprint Checkpoint & Artifact Assembly | T08.01-T08.04 | LIGHT: 4 |

## Source Snapshot

- **Recipient `/task`**: skill package `.claude/skills/task/SKILL.md` (dev copy) / `src/superclaude/skills/task/` (source of truth). F1 execution loop: READ -> IDENTIFY -> EXECUTE -> UPDATE -> REPEAT. Companion builder `.claude/skills/task-builder/SKILL.md`. Phase-gate `rf-qa` invariant inside `task/SKILL.md`. Subagent vocabulary: `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler`, `rf-task-builder`, `rf-task-researcher`, `Explore`, `general-purpose`. Real MDTM consumers under `.dev/tasks/to-do/TASK-*/`.
- **Donor `/sc:task`**: command file `.claude/commands/sc/task.md` / `src/superclaude/commands/task.md`. Execution protocol `.claude/skills/sc-task-protocol/SKILL.md` / `src/superclaude/skills/sc-task-protocol/`. Candidate features: STRICT/STANDARD/LIGHT/EXEMPT tier classification table, TFEP (Test Failure Escalation Protocol), classification header emission, per-tier flow branching, MCP server declarations, persona auto-activation, declared allowed-tools, compliance gating.
- **Direction**: `/sc:task` is the donor; every valuable unique feature is evaluated for absorption into `/task`; the remainder is deprecated. This is a feature-transfer sprint, not a comparison sprint.
- **Load-bearing invariants** (MAY NOT be broken by any absorbed feature): INV-01 F1 loop semantics; INV-02 prohibited-actions catalog; INV-03 phase-gate `rf-qa` + post-completion `rf-qa`/`rf-qa-qualitative`; INV-04 resumability from disk; INV-05 refusal-of-definition (the MDTM file decides *what*, the F1 loop only *executes*).
- **Adversarial gating**: Phase 4 runs a `/sc:adversarial` debate per donor feature; verdict by binding rubric Net = (V x C) / K; thresholds ADOPT >=5, ADAPT 3-5, DEFER 1.5-3, REJECT <1.5 or any invariant violation.

## Deterministic Rules Applied

- **R-RULE-01**: Every code-reading task uses `mcp__auggie-mcp__codebase-retrieval` as the primary search tool with `directory_path: /config/workspace/IronClaude`.
- **R-RULE-02**: Strict phase sequencing -- no phase begins until the prior phase checkpoint passes.
- **R-RULE-03**: All behavioral claims about either surface cite specific `file:line` evidence; no unsupported claims.
- **R-RULE-04**: Anti-sycophancy gate -- every donor-feature value claim states the conditions under which it does NOT deliver value; every complementarity claim states integration cost. Position A lacking a trade-off acknowledgment is sent back for re-debate.
- **R-RULE-05**: Invariant gate -- any donor feature requiring violation of INV-01..INV-05 is auto-REJECTed in Phase 4 regardless of value score; the debate surfaces the violation.
- **R-RULE-06**: "Absorb patterns, not implementation mass" -- Phase 6 extracts the control pattern, not the donor's surrounding ceremony; ceremony without behavioral teeth is REJECTed in Phase 4.
- **R-RULE-07**: Scoring rubric is binding -- Net = V x C / K; verdict thresholds fixed; subjective overrides require an explicit "manifest exception" entry in `transfer-manifest.md` with named justification.
- **R-RULE-08**: Artifacts are written to `TASKLIST_ROOT/artifacts/`.
- **R-RULE-09**: Each phase ends with a checkpoint task carrying a checkpoint table verifying all phase acceptance criteria.
- **R-RULE-10**: `src/superclaude/` is source of truth; `.claude/` is the dev copy. Every file claim specifies which side it cites. Drift between sides is a finding and must appear in Phase 6.
- **R-RULE-11**: The rejected-features ledger is terminal -- DEFER/REJECT features may not be silently re-proposed in Phase 6/7; re-litigation requires explicit re-debate.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | Enumerate `/task` recipient extension points (hooks, frontmatter slots, prohibited-actions negative space, subagent dispatcher). |
| R-002 | Phase 1 | Enumerate `/sc:task` donor features at concrete granularity with file:line evidence and first-pass transferability tags. |
| R-003 | Phase 1 | Cross-flag donor features `/task` already has as DUPLICATE-OF-EXISTING for Phase 4 special handling. |
| R-004 | Phase 2 | Characterize tier classification model and classification header emission (mechanism, outputs, value/coupling claims). |
| R-005 | Phase 2 | Characterize TFEP and per-tier flow branching (entry/exit conditions, escalation artifacts, dependencies). |
| R-006 | Phase 2 | Characterize MCP declarations, persona auto-activation, allowed-tools, compliance gating, triggering surface. |
| R-007 | Phase 2 | Apply anti-sycophancy pass: every value claim records the conditions under which it does NOT deliver value. |
| R-008 | Phase 3 | Define INV-01..INV-05 invariant bounds: behavioral rule, file:line enforcement, failure mode, violating typology. |
| R-009 | Phase 3 | Document extension-point contracts: admit/reject criteria per `/task` extension point. |
| R-010 | Phase 3 | Analyze `task-builder` adjacent surface to route work-definition transfers correctly. |
| R-011 | Phase 4 | Run `/sc:adversarial` debates for tier classification and classification header emission features. |
| R-012 | Phase 4 | Run `/sc:adversarial` debates for TFEP and per-tier flow branching features. |
| R-013 | Phase 4 | Run `/sc:adversarial` debates for MCP, persona, allowed-tools, compliance, triggering-surface features. |
| R-014 | Phase 4 | Apply anti-sycophancy gate and invariant gate; send failing debates back for re-debate. |
| R-015 | Phase 4 | Stack-rank all features by Net = V x C / K with verdict column and integration sketches. |
| R-016 | Phase 5 | Merge per-feature verdicts; resolve inter-feature dependencies and ADOPT/REJECT conflicts. |
| R-017 | Phase 5 | Lock integration sketches for ADOPT; define explicit modifications for ADAPT; preconditions for DEFER. |
| R-018 | Phase 5 | Produce `transfer-manifest.md` (binding) and `rejected-features-ledger.md` (terminal). |
| R-019 | Phase 6 | Convert manifest to implementation roadmap with dependency graph (`/sc:roadmap` patterns). |
| R-020 | Phase 6 | Produce refactor plans for `/task` skill edits and MDTM frontmatter extensions. |
| R-021 | Phase 6 | Produce `/sc:task` deprecation plan and references refactor (backlog, skills, command files). |
| R-022 | Phase 6 | Produce distribution surface refactor (`superclaude install`, `make sync-dev`, README) and documentation. |
| R-023 | Phase 6 | Produce `merge-master.md` unified plan with dependency graph and execution order. |
| R-024 | Phase 7 | Run `/sc:adversarial` on the merge plan: Invariant Defender vs Manifest Auditor. |
| R-025 | Phase 7 | Re-verify every file reference via auggie; check compat hazards against in-flight MDTM and current sprints. |
| R-026 | Phase 7 | Check traceability gaps; produce invariant-survival walkthrough with worked example. |
| R-027 | Phase 7 | Re-score drifted features; produce `validation-report.md` and `final-merge-plan.md`. |
| R-028 | Phase 8 | Build `artifact-index.md` linking every artifact in Phases 1-7. |
| R-029 | Phase 8 | Verify the end-to-end traceability chain; confirm no orphaned artifacts or dead references. |
| R-030 | Phase 8 | Produce `sprint-summary.md` and pass the final structural quality gate. |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---|---|---|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | `recipient-extension-points.md` (one row per extension point) | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/recipient-extension-points.md` | M | Low |
| D-0002 | T01.02 | R-002 | `donor-feature-catalog.md` (one row per donor feature + transferability tag) | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/donor-feature-catalog.md` | L | Med |
| D-0003 | T01.03 | R-003 | DUPLICATE-OF-EXISTING flags merged into donor catalog | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/donor-feature-catalog.md` | S | Low |
| D-CP01 | T01.04 | R-001, R-002, R-003 | Phase 1 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P01-END.md` | XS | Low |
| D-0004 | T02.01 | R-004 | `feature-tier-classification.md`, `feature-classification-header.md` | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/feature-*.md` | M | Low |
| D-0005 | T02.02 | R-005 | `feature-tfep.md`, `feature-per-tier-branching.md` | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/feature-*.md` | M | Med |
| D-0006 | T02.03 | R-006 | `feature-mcp-declarations.md`, `feature-persona-activation.md`, `feature-allowed-tools.md`, `feature-compliance-gating.md`, `feature-triggering-surface.md` | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/feature-*.md` | L | Med |
| D-0007 | T02.04 | R-007 | Anti-sycophancy completeness pass over all `feature-*.md` | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/feature-*.md` | S | Low |
| D-CP02 | T02.05 | R-004, R-005, R-006, R-007 | Phase 2 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P02-END.md` | XS | Low |
| D-0008 | T03.01 | R-008 | `invariant-bounds.md` (one section per INV-NN) | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/invariant-bounds.md` | M | Low |
| D-0009 | T03.02 | R-009 | `extension-point-contracts.md` (one row per extension point) | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/extension-point-contracts.md` | M | Low |
| D-0010 | T03.03 | R-010 | `task-builder-adjacency.md` (work-definition transfer routing) | EXEMPT | Skip (read-only) | `TASKLIST_ROOT/artifacts/task-builder-adjacency.md` | S | Low |
| D-CP03 | T03.04 | R-008, R-009, R-010 | Phase 3 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P03-END.md` | XS | Low |
| D-0011 | T04.01 | R-011 | `debate-tier-classification.md`, `debate-classification-header.md` | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/debate-*.md` | L | Med |
| D-0012 | T04.02 | R-012 | `debate-tfep.md`, `debate-per-tier-branching.md` | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/debate-*.md` | L | Med |
| D-0013 | T04.03 | R-013 | `debate-mcp-declarations.md`, `debate-persona-activation.md`, `debate-allowed-tools.md`, `debate-compliance-gating.md`, `debate-triggering-surface.md` | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/debate-*.md` | XL | Med |
| D-0014 | T04.04 | R-014 | Anti-sycophancy + invariant gate pass; re-debate ledger | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/gate-pass-report.md` | M | Med |
| D-0015 | T04.05 | R-015 | `stack-rank.md` (all features by Net score + verdict + integration sketch) | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/stack-rank.md` | M | Med |
| D-CP04 | T04.06 | R-011..R-015 | Phase 4 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P04-END.md` | XS | Low |
| D-0016 | T05.01 | R-016 | Inter-feature dependency reconciliation matrix | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/feature-dependency-matrix.md` | M | Med |
| D-0017 | T05.02 | R-017 | Locked integration sketches (ADOPT) + modifications (ADAPT) + preconditions (DEFER) | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/integration-sketches.md` | L | Med |
| D-0018 | T05.03 | R-018 | `transfer-manifest.md` (binding) + `rejected-features-ledger.md` (terminal) | STANDARD | Direct review | `TASKLIST_ROOT/artifacts/transfer-manifest.md`, `rejected-features-ledger.md` | L | High |
| D-CP05 | T05.04 | R-016, R-017, R-018 | Phase 5 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P05-END.md` | XS | Low |
| D-0019 | T06.01 | R-019 | Implementation roadmap with dependency graph | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/merge-roadmap.md` | L | High |
| D-0020 | T06.02 | R-020 | `refactor-task-skill.md`, `refactor-mdtm-frontmatter.md` | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/refactor-*.md` | L | High |
| D-0021 | T06.03 | R-021 | `refactor-sctask-deprecation.md`, `refactor-references.md` | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/refactor-*.md` | L | High |
| D-0022 | T06.04 | R-022 | `refactor-distribution.md`, `refactor-documentation.md` | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/refactor-*.md` | M | Med |
| D-0023 | T06.05 | R-023 | `merge-master.md` (unified plan + dependency graph + execution order) | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/merge-master.md` | L | High |
| D-CP06 | T06.06 | R-019..R-023 | Phase 6 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P06-END.md` | XS | Low |
| D-0024 | T07.01 | R-024 | `plan-adversarial-review.md` (Invariant Defender vs Manifest Auditor) | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/plan-adversarial-review.md` | L | High |
| D-0025 | T07.02 | R-025 | `file-reference-reverification.md` + `compat-hazard-report.md` | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/file-reference-reverification.md`, `compat-hazard-report.md` | M | High |
| D-0026 | T07.03 | R-026 | `traceability-gap-report.md` + `invariant-survival-walkthrough.md` | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/invariant-survival-walkthrough.md` | M | Med |
| D-0027 | T07.04 | R-027 | `validation-report.md` + `final-merge-plan.md` | STRICT | Sub-agent verification | `TASKLIST_ROOT/artifacts/validation-report.md`, `final-merge-plan.md` | L | High |
| D-CP07 | T07.05 | R-024..R-027 | Phase 7 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P07-END.md` | XS | Low |
| D-0028 | T08.01 | R-028 | `artifact-index.md` linking all Phase 1-7 artifacts | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/artifact-index.md` | S | Low |
| D-0029 | T08.02 | R-029 | Traceability-chain verification result | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/traceability-chain-check.md` | S | Low |
| D-0030 | T08.03 | R-030 | `sprint-summary.md` + final structural quality gate result | LIGHT | Quick sanity check | `TASKLIST_ROOT/artifacts/sprint-summary.md` | M | Low |
| D-CP08 | T08.04 | R-028, R-029, R-030 | Phase 8 end-of-phase checkpoint report (SPRINT EXIT GATE) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P08-END.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---|---|---|---|---|---|
| R-001 | T01.01 | D-0001 | EXEMPT | 85% | `TASKLIST_ROOT/artifacts/recipient-extension-points.md` |
| R-002 | T01.02 | D-0002 | EXEMPT | 80% | `TASKLIST_ROOT/artifacts/donor-feature-catalog.md` |
| R-003 | T01.03 | D-0003 | EXEMPT | 80% | `TASKLIST_ROOT/artifacts/donor-feature-catalog.md` |
| R-004 | T02.01 | D-0004 | EXEMPT | 80% | `TASKLIST_ROOT/artifacts/feature-tier-classification.md` |
| R-005 | T02.02 | D-0005 | EXEMPT | 80% | `TASKLIST_ROOT/artifacts/feature-tfep.md` |
| R-006 | T02.03 | D-0006 | EXEMPT | 75% | `TASKLIST_ROOT/artifacts/feature-mcp-declarations.md` |
| R-007 | T02.04 | D-0007 | EXEMPT | 85% | `TASKLIST_ROOT/artifacts/feature-*.md` |
| R-008 | T03.01 | D-0008 | EXEMPT | 85% | `TASKLIST_ROOT/artifacts/invariant-bounds.md` |
| R-009 | T03.02 | D-0009 | EXEMPT | 80% | `TASKLIST_ROOT/artifacts/extension-point-contracts.md` |
| R-010 | T03.03 | D-0010 | EXEMPT | 80% | `TASKLIST_ROOT/artifacts/task-builder-adjacency.md` |
| R-011 | T04.01 | D-0011 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/debate-tier-classification.md` |
| R-012 | T04.02 | D-0012 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/debate-tfep.md` |
| R-013 | T04.03 | D-0013 | STANDARD | 70% | `TASKLIST_ROOT/artifacts/debate-mcp-declarations.md` |
| R-014 | T04.04 | D-0014 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/gate-pass-report.md` |
| R-015 | T04.05 | D-0015 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/stack-rank.md` |
| R-016 | T05.01 | D-0016 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/feature-dependency-matrix.md` |
| R-017 | T05.02 | D-0017 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/integration-sketches.md` |
| R-018 | T05.03 | D-0018 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/transfer-manifest.md` |
| R-019 | T06.01 | D-0019 | STRICT | 75% | `TASKLIST_ROOT/artifacts/merge-roadmap.md` |
| R-020 | T06.02 | D-0020 | STRICT | 75% | `TASKLIST_ROOT/artifacts/refactor-task-skill.md` |
| R-021 | T06.03 | D-0021 | STRICT | 75% | `TASKLIST_ROOT/artifacts/refactor-sctask-deprecation.md` |
| R-022 | T06.04 | D-0022 | STRICT | 80% | `TASKLIST_ROOT/artifacts/refactor-distribution.md` |
| R-023 | T06.05 | D-0023 | STRICT | 75% | `TASKLIST_ROOT/artifacts/merge-master.md` |
| R-024 | T07.01 | D-0024 | STRICT | 75% | `TASKLIST_ROOT/artifacts/plan-adversarial-review.md` |
| R-025 | T07.02 | D-0025 | STRICT | 80% | `TASKLIST_ROOT/artifacts/compat-hazard-report.md` |
| R-026 | T07.03 | D-0026 | STRICT | 80% | `TASKLIST_ROOT/artifacts/invariant-survival-walkthrough.md` |
| R-027 | T07.04 | D-0027 | STRICT | 75% | `TASKLIST_ROOT/artifacts/final-merge-plan.md` |
| R-028 | T08.01 | D-0028 | LIGHT | 90% | `TASKLIST_ROOT/artifacts/artifact-index.md` |
| R-029 | T08.02 | D-0029 | LIGHT | 90% | `TASKLIST_ROOT/artifacts/traceability-chain-check.md` |
| R-030 | T08.03 | D-0030 | LIGHT | 85% | `TASKLIST_ROOT/artifacts/sprint-summary.md` |
| R-001, R-002, R-003 | T01.04 | D-CP01 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P01-END.md` |
| R-004..R-007 | T02.05 | D-CP02 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P02-END.md` |
| R-008, R-009, R-010 | T03.04 | D-CP03 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P03-END.md` |
| R-011..R-015 | T04.06 | D-CP04 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P04-END.md` |
| R-016, R-017, R-018 | T05.04 | D-CP05 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P05-END.md` |
| R-019..R-023 | T06.06 | D-CP06 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P06-END.md` |
| R-024..R-027 | T07.05 | D-CP07 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P07-END.md` |
| R-028, R-029, R-030 | T08.04 | D-CP08 | LIGHT | 100% | `TASKLIST_ROOT/checkpoints/CP-P08-END.md` |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---|---|---|---|---|---|---|

## Checkpoint Report Template

```
# Checkpoint Report -- <Checkpoint Title>
**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md
**Scope:** <tasks covered>

## Status
Overall: Pass | Fail | TBD

## Verification Results
- <bullet aligned to checkpoint Verification>

## Exit Criteria Assessment
- <bullet aligned to checkpoint Exit Criteria>

## Issues & Follow-ups
- <blocking issues; reference T<PP>.<TT> and D-####>

## Evidence
- <bullet list of intended evidence paths under TASKLIST_ROOT/evidence/>
```

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---|---|---|---|---|---|---|

## Generation Notes

- **Sprint type:** Directional feature-transfer with adversarial gating. `/sc:task` is the donor; `/task` is the recipient and the only surface retained post-sprint. Phase 4 `/sc:adversarial` is the core mechanism, not a side activity.
- **Tier assignment:** Phases 1-3 are EXEMPT (read-only inventory / characterization / invariant extraction) with the per-phase checkpoint at LIGHT. Phases 4-5 are STANDARD (adversarial debate and synthesis produce binding, auditable artifacts). Phases 6-7 are STRICT (plan that will drive code changes; all file references must be verified). Phase 8 is LIGHT (assembly and verification).
- **Checkpoint cadence:** No phase exceeds 5 regular tasks; mid-phase checkpoints not required. Each phase ends with a mandatory end-of-phase checkpoint per R-RULE-09.
- **auggie-first:** Per R-RULE-01, every code-reading task names `mcp__auggie-mcp__codebase-retrieval` with `directory_path: /config/workspace/IronClaude` as the primary search tool. Serena is listed optional where symbol-level call-site resolution is likely (Phases 6-7 rename/deprecation scope).
- **Binding artifacts:** `transfer-manifest.md` (Phase 5) and `final-merge-plan.md` (Phase 7) are the binding outputs. `rejected-features-ledger.md` is terminal per R-RULE-11.
- **TASKLIST_ROOT derivation:** `.dev/releases/current/task-sc-task-directional-merge/` per the sprint specification. Artifacts sit under `TASKLIST_ROOT/artifacts/` per R-RULE-08.
- **Source-of-truth discipline:** Per R-RULE-10 every file claim in Phases 1-7 must specify `src/superclaude/` vs `.claude/`. Drift between the two sides is itself a Phase 6 finding.
