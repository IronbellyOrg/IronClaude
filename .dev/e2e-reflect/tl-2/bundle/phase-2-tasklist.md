# Phase 2 -- Content

Update the sandbox documentation files with the content requirements from the roadmap. This phase keeps all edits under `.dev/e2e-reflect/tl-2/work/`.

### T02.01 -- Add Usage section to `.dev/e2e-reflect/tl-2/work/index.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | The roadmap requires a Usage section in `index.md` that links to `glossary.md`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/tl-2/bundle/artifacts/D-0003/spec.md`
- `.dev/e2e-reflect/tl-2/bundle/artifacts/D-0003/notes.md`
- `.dev/e2e-reflect/tl-2/bundle/artifacts/D-0003/evidence.md`

**Deliverables:**

- Usage section in `.dev/e2e-reflect/tl-2/work/index.md` linking to `glossary.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for the `index.md` Usage section.
2. **[PLANNING]** Check dependencies and blockers from Phase 1.
3. **[EXECUTION]** Open `.dev/e2e-reflect/tl-2/work/index.md`.
4. **[EXECUTION]** Add a `## Usage` section containing a link to `glossary.md`.
5. **[VERIFICATION]** Confirm the Usage section and link are present.
6. **[COMPLETION]** Record evidence under the bundle evidence directory.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-2/work/index.md` contains `## Usage`.
- The Usage section links to `glossary.md`.
- The update remains confined to `.dev/e2e-reflect/tl-2/work/index.md`.
- Evidence references deliverable `D-0003`.

**Validation:**

- Manual check: `.dev/e2e-reflect/tl-2/work/index.md` contains a Usage section linking to `glossary.md`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc)

**Dependencies:** T01.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** None

### T02.02 -- Add summary table to `.dev/e2e-reflect/tl-2/work/glossary.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | The roadmap requires a one-row summary table in `glossary.md`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/tl-2/bundle/artifacts/D-0004/spec.md`
- `.dev/e2e-reflect/tl-2/bundle/artifacts/D-0004/notes.md`
- `.dev/e2e-reflect/tl-2/bundle/artifacts/D-0004/evidence.md`

**Deliverables:**

- One-row summary table in `.dev/e2e-reflect/tl-2/work/glossary.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for the `glossary.md` summary table.
2. **[PLANNING]** Check dependencies and blockers from Phase 1.
3. **[EXECUTION]** Open `.dev/e2e-reflect/tl-2/work/glossary.md`.
4. **[EXECUTION]** Add one markdown summary table with one data row.
5. **[VERIFICATION]** Confirm the summary table has one data row.
6. **[COMPLETION]** Record evidence under the bundle evidence directory.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-2/work/glossary.md` contains a markdown summary table.
- The summary table contains exactly one data row.
- The update remains confined to `.dev/e2e-reflect/tl-2/work/glossary.md`.
- Evidence references deliverable `D-0004`.

**Validation:**

- Manual check: `.dev/e2e-reflect/tl-2/work/glossary.md` contains one summary table with one data row.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc)

**Dependencies:** T01.02
**Rollback:** TBD (if not specified in roadmap)
**Notes:** None

### T02.03 -- Checkpoint: End of Phase 02

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004, R-005 |
| Why | Gate: verify outputs of tasks T02.01-T02.02 and the roadmap success criteria. |
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

**Checkpoint Report Path:** `.dev/e2e-reflect/tl-2/bundle/checkpoints/CP-P02-END.md`

**Purpose:** Confirm the Phase 2 content updates and final success criteria are present.

**Verification:**

- `.dev/e2e-reflect/tl-2/work/index.md` contains a Usage section linking to `glossary.md`.
- `.dev/e2e-reflect/tl-2/work/glossary.md` contains a one-row summary table.
- Both files exist under `.dev/e2e-reflect/tl-2/work/` with the required sections.

**Exit Criteria:**

- Phase 2 deliverable `D-0003` is present.
- Phase 2 deliverable `D-0004` is present.
- Checkpoint report is written to `.dev/e2e-reflect/tl-2/bundle/checkpoints/CP-P02-END.md`.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-2/bundle/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.02
**Rollback:** N/A (checkpoints are read-only verifications)
