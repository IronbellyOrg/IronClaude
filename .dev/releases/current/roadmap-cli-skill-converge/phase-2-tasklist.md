# Phase 2 -- Roadmap Skill References

Converge the roadmap skill and its references with the CLI where the release decision selected CLI-faithful updates. This phase covers B-3 through B-8 in roadmap order.

### T02.01 -- Add CLI step crosswalk to `sc-roadmap-protocol/SKILL.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Tier | STANDARD |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Deliverable IDs | D-0003 |

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` with CLI step crosswalk and Wave mapping.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` lists all 14 CLI roadmap step IDs named in the source documents.
- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` preserves Wave orchestration while mapping each Wave to CLI steps.
- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` marks threshold language as inference-only rather than CLI gate behavior.
- Evidence at `TASKLIST_ROOT/artifacts/D-0003/evidence.md` links B-3 to `D-0003` and names the cosmetic gate auto-remediation lane.

**Dependencies:** T01.03
**Rollback:** TBD (if not specified in roadmap)

### T02.02 -- Add PRD-first detection to `refs/scoring.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Tier | STANDARD |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Deliverable IDs | D-0004 |

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` with PRD-first detection reference content.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0004/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` states that PRD detection is checked before TDD detection.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` names the PRD signal categories and threshold behavior listed in the source documents.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` preserves the TDD detection reference after the PRD section and cites the CLI detection function.
- Evidence at `TASKLIST_ROOT/artifacts/D-0004/evidence.md` links B-4 to `D-0004` and records the source claim's PARTIAL status.

**Dependencies:** T02.01
**Rollback:** TBD (if not specified in roadmap)

### T02.03 -- Collapse `refs/templates.md` to single-template CLI behavior

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Tier | STANDARD |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Deliverable IDs | D-0005 |

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` with single-template resolver behavior.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` describes single-template resolution for roadmap templates.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` names `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"`.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` removes four-tier discovery from canonical behavior or moves it out of canonical scope.
- Evidence at `TASKLIST_ROOT/artifacts/D-0005/evidence.md` links B-5 to `D-0005` and records the source's VERIFIED status.

**Dependencies:** T02.02
**Rollback:** TBD (if not specified in roadmap)

### T02.04 -- Replace sub-agent validation reference with CLI gate criteria in `refs/validation.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Tier | STANDARD |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Deliverable IDs | D-0006 |

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` with CLI gate criteria.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` describes CLI gate criteria instead of sub-agent dispatch.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` names `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, frontmatter checks, semantic checks, and cosmetic gate auto-remediation.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` marks any retained quality-engineer, self-review, or REVISE-loop sub-agent language as non-canonical or removes it from canonical scope.
- Evidence at `TASKLIST_ROOT/artifacts/D-0006/evidence.md` links B-6 to `D-0006` and records the removed REVISE-loop behavior.

**Dependencies:** T02.03
**Rollback:** TBD (if not specified in roadmap)

### T02.05 -- Collapse `refs/extraction-pipeline.md` to single-pass extraction

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Tier | STANDARD |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Deliverable IDs | D-0007 |

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` with single-pass extraction behavior.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0007/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` describes one single-pass extraction step.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` preserves the eight-aspect coverage as rationale rather than required sequence.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` names `build_extract_prompt` and `build_extract_prompt_tdd` as the CLI extraction prompt-builder behavior described in the source documents.
- Evidence at `TASKLIST_ROOT/artifacts/D-0007/evidence.md` links B-7 to `D-0007` and records the source's VERIFIED status.

**Dependencies:** T02.04
**Rollback:** TBD (if not specified in roadmap)

### T02.06 -- Checkpoint: Phase 02 / Tasks T02.01-T02.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003, R-004, R-005, R-006, R-007 |
| Tier | LIGHT |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Deliverable IDs | D-CP02-MID |

**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md

**Verification:**

- `TASKLIST_ROOT/artifacts/D-0003/evidence.md` through `TASKLIST_ROOT/artifacts/D-0007/evidence.md` record source-change evidence for T02.01 through T02.05.
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` and `refs/scoring.md`, `refs/templates.md`, `refs/validation.md`, and `refs/extraction-pipeline.md` contain the covered B-3 through B-7 changes.
- Each covered evidence artifact keeps `TASKLIST_ROOT/artifacts/D-####/*` as supporting evidence rather than the primary source-change deliverable.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md` exists and contains `status: PASS`.
- Checkpoint report includes task IDs T02.01 through T02.05 and roadmap IDs R-003 through R-007.

**Dependencies:** T02.01..T02.05
**Rollback:** N/A (checkpoint reports can be regenerated if recorded incorrectly)

### T02.07 -- Replace `sc:adversarial-protocol` delegation with CLI debate flow in `refs/adversarial-integration.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Tier | STANDARD |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Deliverable IDs | D-0008 |

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` with CLI debate prompt flow.
- Updated `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` wording for the B-8/D-0001 reversal decision.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0008/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` describes the CLI debate prompt flow.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` removes direct `sc:adversarial-protocol` delegation from canonical roadmap protocol behavior and names `build_debate_prompt`.
- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` represents related D-0001 reversal wording consistently and names `_DEPTH_INSTRUCTIONS` where the source requires it.
- Evidence at `TASKLIST_ROOT/artifacts/D-0008/evidence.md` links B-8 to `D-0008` and records the source's VERIFIED status.

**Dependencies:** T02.06
**Rollback:** TBD (if not specified in roadmap)

### T02.08 -- Checkpoint: End of Phase 02

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003, R-004, R-005, R-006, R-007, R-008 |
| Tier | LIGHT |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Deliverable IDs | D-CP02 |

**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P02-END.md

**Verification:**

- `TASKLIST_ROOT/artifacts/D-0003/evidence.md` through `TASKLIST_ROOT/artifacts/D-0008/evidence.md` record source-change evidence for T02.01 through T02.07.
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` and all B-3 through B-8 reference files contain the covered source changes.
- The B-8 evidence records the Option 1 decision, `build_debate_prompt`, `_DEPTH_INSTRUCTIONS`, and the non-canonical status of direct `sc:adversarial-protocol` delegation.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- Checkpoint report includes task IDs T02.01 through T02.07 and roadmap IDs R-003 through R-008.

**Dependencies:** T02.01..T02.07
**Rollback:** N/A (checkpoint reports can be regenerated if recorded incorrectly)
