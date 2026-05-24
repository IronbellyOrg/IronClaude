# Phase 2 -- Roadmap Skill References

Converge the roadmap skill and its references with the CLI where the release decision selected CLI-faithful updates. This phase covers B-3 through B-8 in roadmap order.

### T02.01 -- Add CLI step crosswalk to `sc-roadmap-protocol/SKILL.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | The source documents say the skill uses Wave taxonomy while the CLI uses named steps including anti-instinct, spec-fidelity, wiring-verification, deviation-analysis, remediate, and certify. |
| Effort | L |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0003/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/notes.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` with CLI step crosswalk and Wave mapping.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`.
2. **[PLANNING]** Check dependencies and blockers from B-3 verification evidence.
3. **[EXECUTION]** Preserve Wave orchestration while adding all 14 CLI step IDs as first-class crosswalk entries.
4. **[EXECUTION]** Reframe non-CLI thresholds as inference heuristics only and include the cosmetic gate auto-remediation lane.
5. **[VERIFICATION]** Validate the source `SKILL.md` for CLI step IDs, Wave mapping, inference-only thresholds, and cosmetic gate auto-remediation.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` lists all 14 CLI roadmap step IDs named in the source documents.
- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` preserves Wave orchestration while mapping each Wave to CLI steps.
- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` marks threshold language as inference-only rather than CLI gate behavior.
- Evidence at `TASKLIST_ROOT/artifacts/D-0003/evidence.md` links B-3 to `D-0003` and names the cosmetic gate auto-remediation lane.

**Validation:**

- Manual check: confirm `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` includes anti-instinct, spec-fidelity, wiring-verification, deviation-analysis, remediate, certify, the full 14-step crosswalk, and cosmetic gate auto-remediation.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Dependencies:** T01.03
**Rollback:** TBD (if not specified in roadmap)
**Notes:** The source decision uses a hybrid based on Option 1 for B-3.

### T02.02 -- Add PRD-first detection to `refs/scoring.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | The source documents state that `refs/scoring.md` omits the PRD scoring algorithm even though CLI detection checks PRD signals first. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0004/spec.md`
- `TASKLIST_ROOT/artifacts/D-0004/notes.md`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` with PRD-first detection reference content.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0004/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`.
2. **[PLANNING]** Check dependencies and blockers from B-4 verification evidence.
3. **[EXECUTION]** Add PRD detection before TDD detection in the scoring reference.
4. **[EXECUTION]** Cite the current CLI detection function by name and include PRD signal categories and threshold behavior.
5. **[VERIFICATION]** Validate the source `scoring.md` for PRD-first ordering, signal categories, threshold behavior, and preserved TDD reference.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0004/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` states that PRD detection is checked before TDD detection.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` names the PRD signal categories and threshold behavior listed in the source documents.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` preserves the TDD detection reference after the PRD section and cites the CLI detection function.
- Evidence at `TASKLIST_ROOT/artifacts/D-0004/evidence.md` links B-4 to `D-0004` and records the source claim's PARTIAL status.

**Validation:**

- Manual check: compare `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` against the PRD-first detection evidence in the verification source.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0004/evidence.md`.

**Dependencies:** T02.01
**Rollback:** TBD (if not specified in roadmap)

### T02.03 -- Collapse `refs/templates.md` to single-template CLI behavior

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | The source documents state that the skill reference describes four discovery tiers while the CLI uses a single named template resolver. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0005/notes.md`
- `TASKLIST_ROOT/artifacts/D-0005/evidence.md`

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` with single-template resolver behavior.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`.
2. **[PLANNING]** Check dependencies and blockers from B-5 verification evidence.
3. **[EXECUTION]** Replace four-tier discovery language with single-template resolver behavior.
4. **[EXECUTION]** Include the `ROADMAP_TEMPLATE` constant named in the source documents.
5. **[VERIFICATION]** Validate the source `templates.md` for single-template CLI behavior and absence of active four-tier discovery requirements.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` describes single-template resolution for roadmap templates.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` names `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"`.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` removes four-tier discovery from canonical behavior or moves it out of canonical scope.
- Evidence at `TASKLIST_ROOT/artifacts/D-0005/evidence.md` links B-5 to `D-0005` and records the source's VERIFIED status.

**Validation:**

- Manual check: confirm `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` represents single-template CLI behavior only.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Dependencies:** T02.02
**Rollback:** TBD (if not specified in roadmap)

### T02.04 -- Replace sub-agent validation reference with CLI gate criteria in `refs/validation.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | The source documents state that `refs/validation.md` describes quality-engineer and self-review sub-agents, while the CLI uses gate criteria rather than sub-agent dispatch. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/notes.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` with CLI gate criteria.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md`.
2. **[PLANNING]** Check dependencies and blockers from B-6 verification evidence.
3. **[EXECUTION]** Replace sub-agent dispatch language with CLI gate criteria, including `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE`.
4. **[EXECUTION]** Include frontmatter checks, semantic checks, cosmetic gate auto-remediation, and non-canonical sub-agent handling.
5. **[VERIFICATION]** Validate the source `validation.md` for CLI gate criteria and removal or demotion of REVISE-loop sub-agent behavior.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` describes CLI gate criteria instead of sub-agent dispatch.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` names `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`, frontmatter checks, semantic checks, and cosmetic gate auto-remediation.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` marks any retained quality-engineer, self-review, or REVISE-loop sub-agent language as non-canonical or removes it from canonical scope.
- Evidence at `TASKLIST_ROOT/artifacts/D-0006/evidence.md` links B-6 to `D-0006` and records the removed REVISE-loop behavior.

**Validation:**

- Manual check: confirm `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` does not require quality-engineer or self-review sub-agents for CLI parity.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Dependencies:** T02.03
**Rollback:** TBD (if not specified in roadmap)

### T02.05 -- Collapse `refs/extraction-pipeline.md` to single-pass extraction

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | The source documents state that the skill reference describes eight sequential extraction steps while the CLI executes one extraction prompt builder step. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0007/notes.md`
- `TASKLIST_ROOT/artifacts/D-0007/evidence.md`

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` with single-pass extraction behavior.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0007/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`.
2. **[PLANNING]** Check dependencies and blockers from B-7 verification evidence.
3. **[EXECUTION]** Replace sequential extraction pipeline wording with single-pass extraction behavior.
4. **[EXECUTION]** Preserve the eight original aspects as coverage notes and name `build_extract_prompt` plus `build_extract_prompt_tdd`.
5. **[VERIFICATION]** Validate the source `extraction-pipeline.md` for one extraction step, prompt-builder names, and non-sequential eight-aspect coverage.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0007/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` describes one single-pass extraction step.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` preserves the eight-aspect coverage as rationale rather than required sequence.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` names `build_extract_prompt` and `build_extract_prompt_tdd` as the CLI extraction prompt-builder behavior described in the source documents.
- Evidence at `TASKLIST_ROOT/artifacts/D-0007/evidence.md` links B-7 to `D-0007` and records the source's VERIFIED status.

**Validation:**

- Manual check: confirm `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` does not instruct execution of eight chained extraction steps.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0007/evidence.md`.

**Dependencies:** T02.04
**Rollback:** TBD (if not specified in roadmap)

### T02.06 -- Checkpoint: Phase 02 / Tasks T02.01-T02.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003, R-004, R-005, R-006, R-007 |
| Why | Gate: verify outputs of tasks T02.01-T02.05 before continuing. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP02-MID |

**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md

**Purpose:** Confirm the first five roadmap skill reference source edits and evidence artifacts are present before B-8 work begins.

**Verification:**

- `TASKLIST_ROOT/artifacts/D-0003/evidence.md` through `TASKLIST_ROOT/artifacts/D-0007/evidence.md` record source-change evidence for T02.01 through T02.05.
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` and `refs/scoring.md`, `refs/templates.md`, `refs/validation.md`, and `refs/extraction-pipeline.md` contain the covered B-3 through B-7 changes.
- Each covered evidence artifact keeps `TASKLIST_ROOT/artifacts/D-####/*` as supporting evidence rather than the primary source-change deliverable.

**Exit Criteria:**

- B-3 through B-7 each have traceable source-file deliverables and evidence artifacts.
- The mid-phase checkpoint report covers tasks T02.01 through T02.05.
- No artifact path in the covered range is missing from the Deliverable Registry.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T02.01 through T02.05 and roadmap IDs R-003 through R-007.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.05
**Rollback:** N/A (checkpoint reports can be regenerated if recorded incorrectly)

### T02.07 -- Replace `sc:adversarial-protocol` delegation with CLI debate flow in `refs/adversarial-integration.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | The source documents state that the skill reference delegates to `sc:adversarial-protocol`, while the CLI debate phase is a single LLM prompt flow. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/notes.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**

- Updated `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` with CLI debate prompt flow.
- Updated `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` wording for the B-8/D-0001 reversal decision.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0008/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` and `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`.
2. **[PLANNING]** Check dependencies and blockers from B-8 verification evidence.
3. **[EXECUTION]** Replace direct `sc:adversarial-protocol` delegation with CLI debate prompt flow.
4. **[EXECUTION]** Align related `SKILL.md` wording about D-0001 reversal with the selected B-8 decision and name `build_debate_prompt` plus `_DEPTH_INSTRUCTIONS`.
5. **[VERIFICATION]** Validate source files for single-shot debate behavior and removal of canonical `sc:adversarial-protocol` delegation.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0008/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` describes the CLI debate prompt flow.
- File `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` removes direct `sc:adversarial-protocol` delegation from canonical roadmap protocol behavior and names `build_debate_prompt`.
- File `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` represents related D-0001 reversal wording consistently and names `_DEPTH_INSTRUCTIONS` where the source requires it.
- Evidence at `TASKLIST_ROOT/artifacts/D-0008/evidence.md` links B-8 to `D-0008` and records the source's VERIFIED status.

**Validation:**

- Manual check: confirm `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` does not require `sc:adversarial-protocol` invocation for CLI parity.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0008/evidence.md`.

**Dependencies:** T02.06
**Rollback:** TBD (if not specified in roadmap)
**Notes:** The source decision selects Option 1 for B-8.

### T02.08 -- Checkpoint: End of Phase 02

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003, R-004, R-005, R-006, R-007, R-008 |
| Why | Gate: verify outputs of tasks T02.01-T02.07 before continuing. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP02 |

**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P02-END.md

**Purpose:** Confirm all roadmap skill/reference convergence source edits and evidence artifacts are ready before deep-validation framing.

**Verification:**

- `TASKLIST_ROOT/artifacts/D-0003/evidence.md` through `TASKLIST_ROOT/artifacts/D-0008/evidence.md` record source-change evidence for T02.01 through T02.07.
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` and all B-3 through B-8 reference files contain the covered source changes.
- The B-8 evidence records the Option 1 decision, `build_debate_prompt`, `_DEPTH_INSTRUCTIONS`, and the non-canonical status of direct `sc:adversarial-protocol` delegation.

**Exit Criteria:**

- B-3 through B-8 each have traceable source-file deliverables and evidence artifacts.
- The B-8 source-file updates follow the recorded Option 1 decision.
- Phase 2 has no regular task after the end-of-phase checkpoint.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T02.01 through T02.07 and roadmap IDs R-003 through R-008.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.07
**Rollback:** N/A (checkpoint reports can be regenerated if recorded incorrectly)
