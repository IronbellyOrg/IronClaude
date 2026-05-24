# TASKLIST INDEX -- Roadmap CLI Skill Convergence

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Roadmap CLI Skill Convergence |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-05-25T20:06:00+00:00 |
| TASKLIST_ROOT | `.dev/releases/current/roadmap-cli-skill-converge/` |
| Total Phases | 5 |
| Total Tasks | 17 |
| Total Deliverables | 17 |
| Complexity Class | HIGH |
| Primary Persona | scribe |
| Consulting Personas | architect, qa |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/releases/current/roadmap-cli-skill-converge/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/releases/current/roadmap-cli-skill-converge/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/releases/current/roadmap-cli-skill-converge/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/releases/current/roadmap-cli-skill-converge/phase-3-tasklist.md` |
| Phase 4 Tasklist | `.dev/releases/current/roadmap-cli-skill-converge/phase-4-tasklist.md` |
| Phase 5 Tasklist | `.dev/releases/current/roadmap-cli-skill-converge/phase-5-tasklist.md` |
| Execution Log | `.dev/releases/current/roadmap-cli-skill-converge/execution-log.md` |
| Checkpoint Reports | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/` |
| Evidence Directory | `.dev/releases/current/roadmap-cli-skill-converge/evidence/` |
| Artifacts Directory | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/` |
| Validation Reports | `.dev/releases/current/roadmap-cli-skill-converge/validation/` |
| Feedback Log | `.dev/releases/current/roadmap-cli-skill-converge/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Command Surface Alignment | T01.01-T01.03 | STANDARD: 2, LIGHT: 1 |
| 2 | phase-2-tasklist.md | Roadmap Skill References | T02.01-T02.08 | STANDARD: 6, LIGHT: 2 |
| 3 | phase-3-tasklist.md | Deep Validation Framing | T03.01-T03.02 | STANDARD: 1, LIGHT: 1 |
| 4 | phase-4-tasklist.md | Packaging Deferral | T04.01-T04.02 | EXEMPT: 1, LIGHT: 1 |
| 5 | phase-5-tasklist.md | Sync and Verification | T05.01-T05.02 | STANDARD: 1, LIGHT: 1 |

## Source Snapshot

- The release converges `/sc:roadmap`, `/sc:validate-roadmap`, and their backing skills with the shipped `superclaude roadmap` CLI where concrete drift was verified.
- The recorded design decision uses a mixed posture: CLI-faithful command/reference surfaces, inference-only preservation for deep validation, and deferred structure-only refactors.
- B-1 and B-2 are sequenced first as command-surface changes.
- B-3 through B-8 are sequenced as the roadmap skill/reference convergence batch.
- B-9 preserves the deep-validation protocol with an explicit Relationship to CLI header and crosswalk.
- B-12 is the mechanical sync and verification step after source edits land.

## Deterministic Rules Applied

- TASKLIST_ROOT was derived from the first `.dev/releases/current/<segment>/` path in the source documents.
- Phase buckets were derived from the recorded sequencing decision and renumbered contiguously from Phase 1 through Phase 5.
- Task IDs use zero-padded `T<PP>.<TT>` identifiers scoped by phase.
- Checkpoints are emitted as numbered task entries after every five tasks and at each phase end.
- Deliverable IDs use `D-0001` through `D-0011` for regular tasks and `D-CP` IDs for checkpoints.
- Effort and risk labels were assigned using the keyword mappings in the generator protocol.
- Tier classification uses the STRICT, EXEMPT, LIGHT, STANDARD priority model and maps each task to deterministic verification routing.
- MCP requirements and fallback settings were derived from the computed tier for each task.
- Sub-agent delegation is not required because no task is both STRICT and High risk.
- Traceability links every roadmap item to at least one task, deliverable, source/evidence path, tier, and confidence value.
- B-11 was not converted into an implementation task because the source verification document marks the global-install gap as refuted.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Command Surface Alignment | B-1 — `commands/roadmap.md` flag-set drift |
| R-002 | Command Surface Alignment | B-2 — `commands/validate-roadmap.md` frontmatter + flag drift |
| R-003 | Roadmap Skill References | B-3 — `sc-roadmap-protocol/SKILL.md` taxonomy mismatch |
| R-004 | Roadmap Skill References | B-4 — `refs/scoring.md` stale CLI cross-reference |
| R-005 | Roadmap Skill References | B-5 — `refs/templates.md` 4-tier discovery vs single-template CLI |
| R-006 | Roadmap Skill References | B-6 — `refs/validation.md` sub-agent pattern absent from CLI |
| R-007 | Roadmap Skill References | B-7 — `refs/extraction-pipeline.md` 8-step extraction vs single CLI prompt |
| R-008 | Roadmap Skill References | B-8 — `refs/adversarial-integration.md` protocol delegation |
| R-009 | Deep Validation Framing | B-9 — `sc-validate-roadmap-protocol/SKILL.md` deep validation pipeline |
| R-010 | Packaging Deferral | B-10 — `sc-validate-roadmap-protocol` packaging shape |
| R-011 | Sync and Verification | B-12 — synced copies refresh |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | Update `src/superclaude/commands/roadmap.md` for CLI-faithful `/sc:roadmap` command surface | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0001/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0001/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0001/evidence.md` | M | Low |
| D-0002 | T01.02 | R-002 | Update `src/superclaude/commands/validate-roadmap.md` for CLI-faithful `/sc:validate-roadmap` command surface | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0002/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0002/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0002/evidence.md` | M | Low |
| D-CP01 | T01.03 | R-001, R-002 | Phase 1 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P01-END.md` | XS | Low |
| D-0003 | T02.01 | R-003 | Update `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` with CLI step crosswalk | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0003/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0003/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0003/evidence.md` | L | Low |
| D-0004 | T02.02 | R-004 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` with PRD-first detection | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0004/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0004/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0004/evidence.md` | M | Low |
| D-0005 | T02.03 | R-005 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` with single-template CLI behavior | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0005/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0005/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0005/evidence.md` | M | Low |
| D-0006 | T02.04 | R-006 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` with CLI gate criteria | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0006/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0006/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0006/evidence.md` | M | Low |
| D-0007 | T02.05 | R-007 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` with single-pass extraction | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0007/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0007/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0007/evidence.md` | M | Low |
| D-CP02-MID | T02.06 | R-003, R-004, R-005, R-006, R-007 | Phase 2 mid checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-T01-T05.md` | XS | Low |
| D-0008 | T02.07 | R-008 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` and `SKILL.md` for CLI debate flow | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0008/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0008/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0008/evidence.md` | M | Low |
| D-CP02 | T02.08 | R-003, R-004, R-005, R-006, R-007, R-008 | Phase 2 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` | XS | Low |
| D-0009 | T03.01 | R-009 | Update `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` with Relationship to CLI header and crosswalk | STANDARD | Manual source inspection plus release-level sync/regression later | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0009/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0009/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0009/evidence.md` | L | Low |
| D-CP03 | T03.02 | R-009 | Phase 3 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P03-END.md` | XS | Low |
| D-0010 | T04.01 | R-010 | Record B-10 packaging deferral decision | EXEMPT | Skip verification | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0010/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0010/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0010/evidence.md` | S | Low |
| D-CP04 | T04.02 | R-010 | Phase 4 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P04-END.md` | XS | Low |
| D-0011 | T05.01 | R-011 | Record source-to-dev sync, global refresh, three-way parity, and verification evidence | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/notes.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/evidence.md` | M | Low |
| D-CP05 | T05.02 | R-011 | Phase 5 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P05-END.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Primary Source / Evidence Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01, T01.03 | D-0001, D-CP01 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/commands/roadmap.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0001/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P01-END.md` |
| R-002 | T01.02, T01.03 | D-0002, D-CP01 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/commands/validate-roadmap.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0002/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P01-END.md` |
| R-003 | T02.01, T02.06, T02.08 | D-0003, D-CP02-MID, D-CP02 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0003/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-T01-T05.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` |
| R-004 | T02.02, T02.06, T02.08 | D-0004, D-CP02-MID, D-CP02 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0004/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-T01-T05.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` |
| R-005 | T02.03, T02.06, T02.08 | D-0005, D-CP02-MID, D-CP02 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0005/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-T01-T05.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` |
| R-006 | T02.04, T02.06, T02.08 | D-0006, D-CP02-MID, D-CP02 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0006/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-T01-T05.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` |
| R-007 | T02.05, T02.06, T02.08 | D-0007, D-CP02-MID, D-CP02 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0007/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-T01-T05.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` |
| R-008 | T02.07, T02.08 | D-0008, D-CP02 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`; `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0008/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` |
| R-009 | T03.01, T03.02 | D-0009, D-CP03 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0009/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P03-END.md` |
| R-010 | T04.01, T04.02 | D-0010, D-CP04 | EXEMPT, LIGHT | [███████---] 70%; [██████████] 100% | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0010/spec.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0010/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P04-END.md` |
| R-011 | T05.01, T05.02 | D-0011, D-CP05 | STANDARD, LIGHT | [████████--] 80%; [██████████] 100% | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/evidence.md`; `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P05-END.md` |

## Execution Log Template

This is a template to be filled during execution.

**Intended Path:** `.dev/releases/current/roadmap-cli-skill-converge/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
|  |  |  |  |  | Manual | TBD | `.dev/releases/current/roadmap-cli-skill-converge/evidence/` |

## Checkpoint Report Template

For each checkpoint created under Section 4.8, execution must produce one report using this template.

**Template:**

- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status`
  - `Overall: Pass | Fail | TBD`
- `## Verification Results`
  - `<verification result 1>`
  - `<verification result 2>`
  - `<verification result 3>`
- `## Exit Criteria Assessment`
  - `<exit criterion 1>`
  - `<exit criterion 2>`
  - `<exit criterion 3>`
- `## Issues & Follow-ups`
  - `List blocking issues; reference T<PP>.<TT> and D-####`
- `## Evidence`
  - `TASKLIST_ROOT/evidence/<evidence-file>`

## Feedback Collection Template

Track tier classification accuracy and execution quality for calibration learning.

**Intended Path:** `.dev/releases/current/roadmap-cli-skill-converge/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
|  |  |  |  | clean | pass | on-target |

**Field definitions:**

- `Override Tier`: Leave blank if no override; else the user-selected tier
- `Override Reason`: Brief justification, such as "Involved auth paths" or "Actually trivial"
- `Completion Status`: `clean | minor-issues | major-issues | failed`
- `Quality Signal`: `pass | partial | rework-needed`
- `Time Variance`: `under-estimate | on-target | over-estimate`

## Glossary

- CLI: Command-line interface, specifically `superclaude roadmap` in the source documents.
- Inference surface: The slash command and skill protocol behavior described as distinct from deterministic CLI behavior.

## Generation Notes

- The tasklist treats `design-decision.md` as the governing roadmap and uses the included scope, solutions, and verification documents as source context.
- B-11 is represented only in the source snapshot and generation notes because the verification source refuted it.
- `TASKLIST_ROOT/artifacts/D-####/*` paths are supporting evidence locations; source-of-truth edits belong under `src/superclaude/`.
