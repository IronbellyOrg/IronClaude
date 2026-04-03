# TASKLIST INDEX -- PRD Skill Refactoring

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | PRD Skill Refactoring |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-04-03 |
| TASKLIST_ROOT | `.dev/releases/current/v3.8/` |
| Total Phases | 4 |
| Total Tasks | 18 |
| Total Deliverables | 22 |
| Complexity Class | MEDIUM |
| Primary Persona | refactorer |
| Consulting Personas | qa, architect |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/releases/current/v3.8/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/releases/current/v3.8/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/releases/current/v3.8/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/releases/current/v3.8/phase-3-tasklist.md` |
| Phase 4 Tasklist | `.dev/releases/current/v3.8/phase-4-tasklist.md` |
| Execution Log | `.dev/releases/current/v3.8/execution-log.md` |
| Checkpoint Reports | `.dev/releases/current/v3.8/checkpoints/` |
| Evidence Directory | `.dev/releases/current/v3.8/evidence/` |
| Artifacts Directory | `.dev/releases/current/v3.8/artifacts/` |
| Validation Reports | `.dev/releases/current/v3.8/validation/` |
| Feedback Log | `.dev/releases/current/v3.8/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Preparation and Validation | T01.01-T01.04 | EXEMPT: 4 |
| 2 | phase-2-tasklist.md | Content Extraction | T02.01-T02.04 | STANDARD: 4 |
| 3 | phase-3-tasklist.md | SKILL.md Restructuring | T03.01-T03.05 | STANDARD: 4, EXEMPT: 1 |
| 4 | phase-4-tasklist.md | Verification and Commit | T04.01-T04.05 | EXEMPT: 3, STANDARD: 2 |

## Source Snapshot

- Decompose monolithic PRD `SKILL.md` (1,373 lines, ~5,000+ tokens) into behavioral spine + 4 refs/ files
- Follow `sc-adversarial-protocol` refs/ lazy-loading pattern established in the codebase
- 4 refs/ files: agent-prompts.md (~415 lines), build-request-template.md (~165 lines), synthesis-mapping.md (~137 lines), validation-checklists.md (~127 lines)
- Word-for-word content preservation required; zero semantic drift permitted
- Refactored SKILL.md target: 430-500 lines (behavioral protocol only)
- Adversarial roadmap synthesis: Variant A (Opus, 82/100) base with 3 Variant B (Haiku) improvements

## Deterministic Rules Applied

- Phase numbering: 4 explicit phases preserved in roadmap appearance order (1-4, no gaps)
- Task IDs: `T<PP>.<TT>` zero-padded format, sequential within each phase
- Roadmap item IDs: `R-001` through `R-018` assigned in top-to-bottom appearance order
- Deliverable IDs: `D-0001` through `D-0022` assigned in task order then deliverable order
- Checkpoint cadence: end-of-phase checkpoint per phase (no phases exceed 5 tasks)
- Clarification tasks: none required (roadmap provides complete specifics for all tasks)
- Effort/Risk: computed via keyword-scoring algorithm (Section 5.2)
- Tier classification: keyword matching + context boosters (Section 5.3)
- Verification routing: tier-proportional (EXEMPT=skip, STANDARD=direct test, STRICT=sub-agent)
- MCP requirements: none required (no STRICT tasks; all STANDARD/EXEMPT)
- Traceability: every task traces to at least one R-### and at least one D-####
- Multi-file output: 1 index + 4 phase files

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | Verify fidelity index completeness. Confirm fidelity-index.md exists and covers all 32 content blocks (B01-B32). |
| R-002 | Phase 1 | Freeze SKILL.md baseline. Record current SKILL.md SHA: git hash-object. Confirm no pending changes on current branch. |
| R-003 | Phase 1 | Create feature branch and refs/ directory. Branch from current HEAD: git checkout -b refactor/prd-skill-decompose. |
| R-004 | Phase 1 | Verify reference implementation accessibility. Confirm sc-adversarial-protocol refs/ pattern is readable. Note cross-reference syntax used. |
| R-005 | Phase 2 | Create refs/agent-prompts.md (FR-PRD-R.2). Extract blocks B14-B21 (lines 553-967): all 8 agent prompt templates. |
| R-006 | Phase 2 | Create refs/synthesis-mapping.md (FR-PRD-R.4). Extract blocks B22-B23 (lines 969-1106): Output Structure + Synthesis Mapping. |
| R-007 | Phase 2 | Create refs/validation-checklists.md (FR-PRD-R.3). Extract blocks B24-B27 (lines 1108-1254): checklists + assembly + content rules. |
| R-008 | Phase 2 | Create refs/build-request-template.md (FR-PRD-R.5). Extract block B11 (lines 344-508): complete BUILD_REQUEST format. Update |
| R-009 | Phase 3 | Remove extracted content blocks from SKILL.md. Remove block B11 (lines 344-508), blocks B14-B21 (lines 553-967), blocks |
| R-010 | Phase 3 | Add per-phase loading declarations (FR-PRD-R.6). In Stage A.7 section, add loading declaration block for |
| R-011 | Phase 3 | Update internal cross-references. Replace all former prose section references with refs/ file paths. Grep verification. |
| R-012 | Phase 3 | Handle B05/B30 Artifact Locations table merge (GAP-01). Append B30 6 specific QA paths to B05 |
| R-013 | Phase 3 | Line count verification. Count SKILL.md lines: must be 430-500. Estimate token count: target <= 2,000. |
| R-014 | Phase 4 | Fidelity verification -- zero content loss (FR-PRD-R.7). Verify every content block from fidelity index appears |
| R-015 | Phase 4 | Success criteria validation sweep. Run all 12 success criteria checks from the Success Criteria table. |
| R-016 | Phase 4 | Component sync. Run make sync-dev to propagate .claude/skills/prd/ to src/superclaude/skills/prd/. Run make verify-sync. |
| R-017 | Phase 4 | Behavioral regression test (NFR-PRD-R.4). Invoke PRD skill on a test product. Verify Stage A completes, |
| R-018 | Phase 4 | Atomic commit. Single commit containing all changes. Commit message: refactor: decompose PRD SKILL.md into behavioral |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | Verified fidelity index (32 blocks confirmed) | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0001/evidence.md` | S | Low |
| D-0002 | T01.02 | R-002 | Baseline SHA record for SKILL.md | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0002/notes.md` | S | Low |
| D-0003 | T01.03 | R-003 | Feature branch + empty refs/ directory | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0003/notes.md` | S | Low |
| D-0004 | T01.04 | R-004 | Reference implementation pattern notes | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0004/notes.md` | XS | Low |
| D-0005 | T02.01 | R-005 | refs/agent-prompts.md (8 agent templates) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0005/spec.md` | S | Low |
| D-0006 | T02.01 | R-005 | Diff verification log (8 templates vs original) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0006/evidence.md` | S | Low |
| D-0007 | T02.02 | R-006 | refs/synthesis-mapping.md (output structure + mapping) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0007/spec.md` | S | Low |
| D-0008 | T02.02 | R-006 | Diff verification log (mapping table vs original) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0008/evidence.md` | S | Low |
| D-0009 | T02.03 | R-007 | refs/validation-checklists.md (checklists + rules) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0009/spec.md` | S | Low |
| D-0010 | T02.03 | R-007 | Diff verification log (checklists vs original) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0010/evidence.md` | S | Low |
| D-0011 | T02.04 | R-008 | refs/build-request-template.md (BUILD_REQUEST) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0011/spec.md` | M | Low |
| D-0012 | T02.04 | R-008 | Cross-reference update verification (6 path changes) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0012/evidence.md` | M | Low |
| D-0013 | T03.01 | R-009 | Reduced SKILL.md (content blocks B11, B14-B27 removed) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0013/evidence.md` | S | Low |
| D-0014 | T03.02 | R-010 | SKILL.md with A.7 loading declarations | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0014/evidence.md` | S | Low |
| D-0015 | T03.03 | R-011 | SKILL.md with updated cross-references (zero stale refs) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0015/evidence.md` | S | Low |
| D-0016 | T03.04 | R-012 | SKILL.md with merged B05/B30 Artifact Locations table | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0016/evidence.md` | S | Low |
| D-0017 | T03.05 | R-013 | Line count verification report (430-500 target) | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0017/evidence.md` | S | Low |
| D-0018 | T04.01 | R-014 | Fidelity verification report (all 32 blocks verified) | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0018/evidence.md` | S | Low |
| D-0019 | T04.02 | R-015 | Success criteria sweep report (12/12 checks) | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0019/evidence.md` | XS | Low |
| D-0020 | T04.03 | R-016 | Synced src/superclaude/skills/prd/ (matching .claude/) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0020/evidence.md` | S | Low |
| D-0021 | T04.04 | R-017 | E2E regression test transcript (PRD skill invocation) | STANDARD | Direct test execution | `.dev/releases/current/v3.8/artifacts/D-0021/evidence.md` | S | Low |
| D-0022 | T04.05 | R-018 | Atomic commit on feature branch | EXEMPT | Skip verification | `.dev/releases/current/v3.8/artifacts/D-0022/notes.md` | S | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | EXEMPT | 85% | `.dev/releases/current/v3.8/artifacts/D-0001/` |
| R-002 | T01.02 | D-0002 | EXEMPT | 90% | `.dev/releases/current/v3.8/artifacts/D-0002/` |
| R-003 | T01.03 | D-0003 | EXEMPT | 75% | `.dev/releases/current/v3.8/artifacts/D-0003/` |
| R-004 | T01.04 | D-0004 | EXEMPT | 90% | `.dev/releases/current/v3.8/artifacts/D-0004/` |
| R-005 | T02.01 | D-0005, D-0006 | STANDARD | 80% | `.dev/releases/current/v3.8/artifacts/D-0005/`, `.dev/releases/current/v3.8/artifacts/D-0006/` |
| R-006 | T02.02 | D-0007, D-0008 | STANDARD | 80% | `.dev/releases/current/v3.8/artifacts/D-0007/`, `.dev/releases/current/v3.8/artifacts/D-0008/` |
| R-007 | T02.03 | D-0009, D-0010 | STANDARD | 80% | `.dev/releases/current/v3.8/artifacts/D-0009/`, `.dev/releases/current/v3.8/artifacts/D-0010/` |
| R-008 | T02.04 | D-0011, D-0012 | STANDARD | 75% | `.dev/releases/current/v3.8/artifacts/D-0011/`, `.dev/releases/current/v3.8/artifacts/D-0012/` |
| R-009 | T03.01 | D-0013 | STANDARD | 75% | `.dev/releases/current/v3.8/artifacts/D-0013/` |
| R-010 | T03.02 | D-0014 | STANDARD | 80% | `.dev/releases/current/v3.8/artifacts/D-0014/` |
| R-011 | T03.03 | D-0015 | STANDARD | 80% | `.dev/releases/current/v3.8/artifacts/D-0015/` |
| R-012 | T03.04 | D-0016 | STANDARD | 75% | `.dev/releases/current/v3.8/artifacts/D-0016/` |
| R-013 | T03.05 | D-0017 | EXEMPT | 85% | `.dev/releases/current/v3.8/artifacts/D-0017/` |
| R-014 | T04.01 | D-0018 | EXEMPT | 85% | `.dev/releases/current/v3.8/artifacts/D-0018/` |
| R-015 | T04.02 | D-0019 | EXEMPT | 85% | `.dev/releases/current/v3.8/artifacts/D-0019/` |
| R-016 | T04.03 | D-0020 | STANDARD | 75% | `.dev/releases/current/v3.8/artifacts/D-0020/` |
| R-017 | T04.04 | D-0021 | STANDARD | 75% | `.dev/releases/current/v3.8/artifacts/D-0021/` |
| R-018 | T04.05 | D-0022 | EXEMPT | 90% | `.dev/releases/current/v3.8/artifacts/D-0022/` |

## Execution Log Template

**Intended Path:** `.dev/releases/current/v3.8/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| | T01.01 | EXEMPT | D-0001 | | Manual | TBD | `.dev/releases/current/v3.8/evidence/` |

## Checkpoint Report Template

For each checkpoint created, produce one report using this template:

- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** .dev/releases/current/v3.8/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status`
  - `Overall: Pass | Fail | TBD`
- `## Verification Results` (exactly 3 bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets)
- `## Issues & Follow-ups`
- `## Evidence`

## Feedback Collection Template

**Intended Path:** `.dev/releases/current/v3.8/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| T01.01 | EXEMPT | | | | | |
| T01.02 | EXEMPT | | | | | |
| T01.03 | EXEMPT | | | | | |
| T01.04 | EXEMPT | | | | | |
| T02.01 | STANDARD | | | | | |
| T02.02 | STANDARD | | | | | |
| T02.03 | STANDARD | | | | | |
| T02.04 | STANDARD | | | | | |
| T03.01 | STANDARD | | | | | |
| T03.02 | STANDARD | | | | | |
| T03.03 | STANDARD | | | | | |
| T03.04 | STANDARD | | | | | |
| T03.05 | EXEMPT | | | | | |
| T04.01 | EXEMPT | | | | | |
| T04.02 | EXEMPT | | | | | |
| T04.03 | STANDARD | | | | | |
| T04.04 | STANDARD | | | | | |
| T04.05 | EXEMPT | | | | | |

## Glossary

| Term | Definition |
|------|-----------|
| SKILL.md | The main manifest file for a SuperClaude skill, containing behavioral protocol (WHAT/WHEN) |
| refs/ | Directory within a skill containing reference material (HOW content) loaded on demand per phase |
| BUILD_REQUEST | The structured prompt format passed to the rf-task-builder subagent to create an MDTM task file |
| Fidelity index | A document mapping every content block from source to destination with verification markers |
| B-block | A sequentially numbered content block (B01-B32) in the fidelity index |

## Generation Notes

- Spec file provided as supplementary context (non-TDD format); used for enriching task descriptions and acceptance criteria
- No TDD-specific extraction triggered (spec lacks TDD §10 Component Inventory heading)
- All 18 roadmap tasks mapped 1:1 to generated tasks (no splitting required; roadmap already well-decomposed)
- No Clarification Tasks needed (roadmap provides complete specifics including line ranges, file paths, and verification commands)
- No STRICT tasks generated (no security/auth/database/migration keywords in task-level text)
- Parallelism note from roadmap preserved: Tasks 2.1-2.3 are parallelizable; Task 2.4 sequential after 2.1-2.3
