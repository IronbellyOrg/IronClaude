# Phase 5 -- Sync and Verification

Complete the mechanical source-to-dev sync and release verification after all source edits land. This phase covers B-12 and the release acceptance checks that depend on the generated work.

### T05.01 -- Run source sync and release verification for B-12

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | The source documents state that synced copies need refresh after source updates and that `make verify-sync`, three-way command parity, and slash-command regression checks are release acceptance criteria. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0011/spec.md`
- `TASKLIST_ROOT/artifacts/D-0011/notes.md`
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Deliverables:**

- Source-to-dev sync, global command refresh, three-way parity, and verification evidence artifact for B-12.

**Steps:**

1. **[PLANNING]** Load context and identify scope for B-12 sync and release verification.
2. **[PLANNING]** Check dependencies and blockers from all prior phase outputs.
3. **[EXECUTION]** Run `make sync-dev` after source edits land.
4. **[EXECUTION]** Refresh global command copies according to the release practice stated in the source documents.
5. **[VERIFICATION]** Run `make verify-sync`, record three-way parity for both command files across `src/`, repo-local `.claude/`, and `/config/.claude/`, and run the slash-command regression check described by the release acceptance criteria.
6. **[COMPLETION]** Record evidence in `TASKLIST_ROOT/artifacts/D-0011/evidence.md`.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0011/evidence.md` records `make verify-sync` passing.
- The evidence artifact records that source-to-dev sync ran and both repo-local and global synced command copies were refreshed after source edits.
- The evidence artifact records md5sum or equivalent content comparison proving three-way parity for `roadmap.md` and `validate-roadmap.md` across `src/superclaude/commands/`, `.claude/commands/sc/`, and `/config/.claude/commands/sc/`.
- The evidence artifact records regression coverage for `/sc:roadmap` and `/sc:validate-roadmap` end-to-end against a sample spec.

**Validation:**

- Manual check: confirm B-12 evidence includes sync, global refresh, three-way parity, verify-sync, and slash-command regression outcomes.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0011/evidence.md`.

**Dependencies:** T04.02
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Do not stage `.claude/` sync output unless explicitly authorized; source-of-truth edits belong under `src/superclaude/`.

### T05.02 -- Checkpoint: End of Phase 05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Gate: verify outputs of tasks T05.01-T05.01 before completion. |
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
| Deliverable IDs | D-CP05 |

**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P05-END.md

**Purpose:** Confirm sync, global refresh, parity, and release verification evidence is ready for release review.

**Verification:**

- `TASKLIST_ROOT/artifacts/D-0011/evidence.md` records source-to-dev sync and both repo-local and global synced command-copy refresh.
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md` records three-way parity for both command files across `src/`, repo-local `.claude/`, and `/config/.claude/`.
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md` records `make verify-sync` and slash-command regression coverage.

**Exit Criteria:**

- B-12 has a traceable evidence artifact.
- Release acceptance criteria that depend on sync, global refresh, and parity are represented.
- Phase 5 has no regular task after the end-of-phase checkpoint.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P05-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers and the B-12 sync/global-refresh/parity evidence summary.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.01..T05.01
**Rollback:** Delete or regenerate `TASKLIST_ROOT/checkpoints/CP-P05-END.md` if checkpoint verification was recorded incorrectly.
