# Phase 3 -- Deep Validation Framing

Preserve the rich deep-validation protocol while making its relationship to the CLI explicit. This phase implements the recorded B-9 decision without collapsing the protocol.

### T03.01 -- Add Relationship to CLI header to `sc-validate-roadmap-protocol/SKILL.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | The source documents state that B-9 should preserve the deep-validation protocol with an explicit disclaimer and crosswalk rather than rewriting it to mirror the CLI. |
| Effort | L |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Manual source inspection plus release-level sync/regression later |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0009/spec.md`
- `TASKLIST_ROOT/artifacts/D-0009/notes.md`
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md`

**Deliverables:**

- Updated `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` with Relationship to CLI header and crosswalk.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0009/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`.
2. **[PLANNING]** Check dependencies and blockers from B-9 verification evidence.
3. **[EXECUTION]** Add a top-of-file Relationship to CLI section naming the deep-validation protocol as inference-only.
4. **[EXECUTION]** Add a crosswalk describing CLI validation as 7 baseline dimensions and 9 input-aware dimensions when source inputs resolve.
5. **[VERIFICATION]** Confirm the source `SKILL.md` preserves the deep protocol, states the simpler reflect plus adversarial-merge CLI flow, and distinguishes investigative validation from CI/CD gating.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0009/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` contains a top-of-file Relationship to CLI section stating this skill is an inference-only deep-validation protocol.
- File `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` states that `superclaude roadmap validate` runs a simpler reflect plus adversarial-merge flow against CLI validation dimensions.
- File `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` describes 7 baseline dimensions and 9 input-aware dimensions when original source inputs resolve, while preserving B-9's deep protocol.
- Evidence at `TASKLIST_ROOT/artifacts/D-0009/evidence.md` records the Option 2 decision and the usage distinction: skill for thorough investigative validation, CLI for automated CI/CD gating.

**Validation:**

- Manual check: inspect `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` for the Relationship to CLI header, crosswalk, CLI flow, dimensions, and usage distinction.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0009/evidence.md`.

**Dependencies:** T02.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** The source decision selects Option 2 for B-9.

### T03.02 -- Checkpoint: End of Phase 03

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Gate: verify outputs of tasks T03.01-T03.01 before continuing. |
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
| Deliverable IDs | D-CP03 |

**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P03-END.md

**Purpose:** Confirm B-9 source-file framing is represented before the packaging deferral decision.

**Verification:**

- `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` contains the Relationship to CLI header.
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md` records the Option 2 decision and usage distinction.
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md` records the 7 baseline and 9 input-aware CLI validation dimensions.

**Exit Criteria:**

- B-9 has a traceable source-file deliverable.
- B-9 output names the CLI validation dimensions and reflect/adversarial-merge flow required by the source.
- Phase 3 has no regular task after the end-of-phase checkpoint.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P03-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.01..T03.01
**Rollback:** N/A (checkpoint reports can be regenerated if recorded incorrectly)
