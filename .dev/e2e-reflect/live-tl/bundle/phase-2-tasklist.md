# Phase 2 -- Content

Update the sandbox markdown files with linked usage content and a summary table. All work remains under `.dev/e2e-reflect/tl-1/work/`.

### T02.01 -- Add usage section to sandbox index

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | The roadmap requires a Usage section in `index.md` that links to `glossary.md`. |
| Effort | XS |
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

- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0003/spec.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0003/notes.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0003/evidence.md`

**Deliverables:**

- Usage section in `.dev/e2e-reflect/tl-1/work/index.md` linking to `glossary.md`.

**Steps:**

1. **[PLANNING]** Load roadmap item R-003 and identify the index file update.
2. **[PLANNING]** Check that `.dev/e2e-reflect/tl-1/work/index.md` exists from Phase 1.
3. **[EXECUTION]** Add a `## Usage` section to `.dev/e2e-reflect/tl-1/work/index.md`.
4. **[EXECUTION]** Add a markdown link from the Usage section to `glossary.md`.
5. **[VERIFICATION]** Confirm the Usage section and relative glossary link exist.
6. **[COMPLETION]** Record evidence under `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0003/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-1/work/index.md` contains a `## Usage` section.
- File `.dev/e2e-reflect/tl-1/work/index.md` contains a markdown link to `glossary.md`.
- The update is repeatable without duplicating the Usage section.
- Evidence path `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0003/evidence.md` records the verification.

**Validation:**

- Manual check: reviewer confirms `index.md` has a Usage section linking to `glossary.md`.
- Evidence: linkable artifact produced at `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0003/evidence.md`.

**Dependencies:** T01.01
**Rollback:** Remove the Usage section from `.dev/e2e-reflect/tl-1/work/index.md`.

---

### T02.02 -- Add glossary summary table

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | The roadmap requires a one-row summary table in `glossary.md`. |
| Effort | XS |
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

- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0004/spec.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0004/notes.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0004/evidence.md`

**Deliverables:**

- One-row summary table in `.dev/e2e-reflect/tl-1/work/glossary.md`.

**Steps:**

1. **[PLANNING]** Load roadmap item R-004 and identify the glossary table requirement.
2. **[PLANNING]** Check that `.dev/e2e-reflect/tl-1/work/glossary.md` exists from Phase 1.
3. **[EXECUTION]** Add a markdown summary table header to `glossary.md`.
4. **[EXECUTION]** Add exactly one summary data row to the table.
5. **[VERIFICATION]** Confirm the table contains one data row.
6. **[COMPLETION]** Record evidence under `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0004/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-1/work/glossary.md` contains a markdown summary table.
- The summary table contains exactly one data row.
- The update is repeatable without duplicating the summary table.
- Evidence path `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0004/evidence.md` records the verification.

**Validation:**

- Manual check: reviewer confirms `glossary.md` has a one-row summary table.
- Evidence: linkable artifact produced at `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0004/evidence.md`.

**Dependencies:** T01.02
**Rollback:** Remove the summary table from `.dev/e2e-reflect/tl-1/work/glossary.md`.

---

### T02.03 -- Checkpoint: End of Phase 02

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Gate: verify outputs of tasks T02.01-T02.02 before phase completion. |
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

**Checkpoint Report Path:** `.dev/e2e-reflect/live-tl/bundle/checkpoints/CP-P02-END.md`

**Purpose:** Verify Phase 2 content artifacts before post-execution reflection.

**Verification:**

- Confirm `.dev/e2e-reflect/tl-1/work/index.md` contains a Usage section.
- Confirm `.dev/e2e-reflect/tl-1/work/index.md` links to `glossary.md`.
- Confirm `.dev/e2e-reflect/tl-1/work/glossary.md` contains a one-row summary table.

**Exit Criteria:**

- T02.01 is complete.
- T02.02 is complete.
- Checkpoint report path is ready for execution evidence.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for T02.01-T02.02.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/live-tl/bundle/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T02.01 and T02.02.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.02
**Rollback:** N/A (checkpoints are read-only verifications)

---

### T02.04 -- Post-Execution Reflection: sc:reflect --mode post

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003, R-004 |
| Why | Independent post-execution deviation audit of every task in Phase 2, in a fresh session, after all phase work completes. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT  (* reflect is the auditor; it is not itself tier-verified *) |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification (reflect IS the verification) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | Required (fresh-session reflect ensemble) |
| Deliverable IDs | D-RF02 |

**Reflect Report Path:** `.dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-02/REPORT.md`

**Spawn Directive (fresh session):** Spawn a NEW agent/session and run:
`/sc:reflect --mode post --remediate --tasklist .dev/e2e-reflect/live-tl/bundle/phase-2-tasklist.md --diff <phase-commit-range> --depth quick --tier 1 --executor-model <EXECUTOR_CLASS> --output .dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-02/`
(The reflect agent uses the default subagent model; `--executor-model` is the reflect-native exclusion flag naming the class that ran the phase's work, so reflect removes it from the reviewer pool — it does not select a model. Never the `sc:task` execution command.)

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-02/REPORT.md`

**Deliverables:**

- Post-execution reflect report for Phase 2.

**Steps:**

1. **[VERIFICATION]** Resolve `<phase-commit-range>` = the git range covering all of Phase 2's task commits.
2. **[VERIFICATION]** Spawn a fresh session and invoke the Spawn Directive above (reflect audits the committed diff — cross-session-safe).
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface its deviation counts (authorized/necessary/drift/regression).

**Acceptance Criteria:**

- File `.dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-02/REPORT.md` exists with a deviation-taxonomy summary.
- Zero `regression`-class deviations, OR a `--remediate` Tier-3 task was authored for each.
- Reflect ran with executor-disjoint reviewers (the `<EXECUTOR_CLASS>` passed via `--executor-model` was excluded from the reviewer pool).
- Report includes the per-task verdict matrix for Phase 2.

**Validation:**

- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** all regular + checkpoint tasks in Phase 2.
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately).
