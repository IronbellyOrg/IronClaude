# TASKLIST INDEX -- Roadmap CLI Skill Convergence

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Roadmap CLI Skill Convergence |
| TASKLIST_ROOT | `.dev/releases/current/roadmap-cli-skill-converge/` |
| Total Phases | 5 |
| Total Tasks | 17 |
| Total Deliverables | 17 |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Command Surface Alignment | T01.01-T01.03 | STANDARD: 2, LIGHT: 1 |
| 2 | phase-2-tasklist.md | Roadmap Skill References | T02.01-T02.08 | STANDARD: 6, LIGHT: 2 |
| 3 | phase-3-tasklist.md | Deep Validation Framing | T03.01-T03.02 | STANDARD: 1, LIGHT: 1 |
| 4 | phase-4-tasklist.md | Packaging Deferral | T04.01-T04.02 | EXEMPT: 1, LIGHT: 1 |
| 5 | phase-5-tasklist.md | Sync and Verification | T05.01-T05.02 | STANDARD: 1, LIGHT: 1 |

## Source Snapshot

- The release converges `/sc:roadmap`, `/sc:validate-roadmap`, and backing skills with the shipped `superclaude roadmap` CLI where drift was verified.
- B-1 and B-2 are command-surface changes.
- B-3 through B-8 are roadmap skill/reference convergence.
- B-9 preserves deep validation with a Relationship to CLI header.
- B-10 defers packaging changes.
- B-12 performs sync, global refresh, parity, and release verification.
- B-11 is excluded because the source verification refuted it.

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths |
|---:|---:|---:|---|---|---|---|
| D-0001 | T01.01 | R-001 | Update `src/superclaude/commands/roadmap.md` for CLI-faithful `/sc:roadmap` command surface | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0001/evidence.md` |
| D-0002 | T01.02 | R-002 | Update `src/superclaude/commands/validate-roadmap.md` for CLI-faithful `/sc:validate-roadmap` command surface | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0002/evidence.md` |
| D-CP01 | T01.03 | R-001, R-002 | Phase 1 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P01-END.md` |
| D-0003 | T02.01 | R-003 | Update `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` with CLI step crosswalk | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0003/evidence.md` |
| D-0004 | T02.02 | R-004 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` with PRD-first detection | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0004/evidence.md` |
| D-0005 | T02.03 | R-005 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` with single-template CLI behavior | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0005/evidence.md` |
| D-0006 | T02.04 | R-006 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` with CLI gate criteria | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0006/evidence.md` |
| D-0007 | T02.05 | R-007 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` with single-pass extraction | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0007/evidence.md` |
| D-CP02-MID | T02.06 | R-003, R-004, R-005, R-006, R-007 | Phase 2 mid checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-T01-T05.md` |
| D-0008 | T02.07 | R-008 | Update `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` and `SKILL.md` for CLI debate flow | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0008/evidence.md` |
| D-CP02 | T02.08 | R-003, R-004, R-005, R-006, R-007, R-008 | Phase 2 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P02-END.md` |
| D-0009 | T03.01 | R-009 | Update `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` with Relationship to CLI header and crosswalk | STANDARD | Manual source inspection plus release-level sync/regression later | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0009/evidence.md` |
| D-CP03 | T03.02 | R-009 | Phase 3 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P03-END.md` |
| D-0010 | T04.01 | R-010 | Record B-10 packaging deferral decision | EXEMPT | Skip verification | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0010/evidence.md` |
| D-CP04 | T04.02 | R-010 | Phase 4 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P04-END.md` |
| D-0011 | T05.01 | R-011 | Record source-to-dev sync, global refresh, three-way parity, and verification evidence | STANDARD | Direct test execution | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/evidence.md` |
| D-CP05 | T05.02 | R-011 | Phase 5 checkpoint report | LIGHT | Quick sanity check | `.dev/releases/current/roadmap-cli-skill-converge/checkpoints/CP-P05-END.md` |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Primary Source / Evidence Paths |
|---:|---:|---:|---|
| R-001 | T01.01, T01.03 | D-0001, D-CP01 | `src/superclaude/commands/roadmap.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0001/evidence.md` |
| R-002 | T01.02, T01.03 | D-0002, D-CP01 | `src/superclaude/commands/validate-roadmap.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0002/evidence.md` |
| R-003 | T02.01, T02.06, T02.08 | D-0003, D-CP02-MID, D-CP02 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0003/evidence.md` |
| R-004 | T02.02, T02.06, T02.08 | D-0004, D-CP02-MID, D-CP02 | `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0004/evidence.md` |
| R-005 | T02.03, T02.06, T02.08 | D-0005, D-CP02-MID, D-CP02 | `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0005/evidence.md` |
| R-006 | T02.04, T02.06, T02.08 | D-0006, D-CP02-MID, D-CP02 | `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0006/evidence.md` |
| R-007 | T02.05, T02.06, T02.08 | D-0007, D-CP02-MID, D-CP02 | `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0007/evidence.md` |
| R-008 | T02.07, T02.08 | D-0008, D-CP02 | `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`; `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0008/evidence.md` |
| R-009 | T03.01, T03.02 | D-0009, D-CP03 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`; `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0009/evidence.md` |
| R-010 | T04.01, T04.02 | D-0010, D-CP04 | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0010/evidence.md` |
| R-011 | T05.01, T05.02 | D-0011, D-CP05 | `.dev/releases/current/roadmap-cli-skill-converge/artifacts/D-0011/evidence.md` |

## Generation Notes

- `TASKLIST_ROOT/artifacts/D-####/*` paths are supporting evidence locations; source-of-truth edits belong under `src/superclaude/`.
- No `.claude/` path is a stageable source-of-truth edit.
