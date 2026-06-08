# Phase 1 -- Scaffold

Create the sandbox markdown files required by the roadmap. All work remains under `.dev/e2e-reflect/tl-1/work/`.

### T01.01 -- Create sandbox index markdown

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The roadmap requires `.dev/e2e-reflect/tl-1/work/index.md` with a title and intro paragraph. |
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
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0001/spec.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0001/notes.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0001/evidence.md`

**Deliverables:**

- File `.dev/e2e-reflect/tl-1/work/index.md` containing one title and one intro paragraph.

**Steps:**

1. **[PLANNING]** Load the roadmap item R-001 and identify the required sandbox path.
2. **[PLANNING]** Check that `.dev/e2e-reflect/tl-1/work/` is the only execution target.
3. **[EXECUTION]** Create `.dev/e2e-reflect/tl-1/work/index.md` with a markdown title.
4. **[EXECUTION]** Add one intro paragraph describing the sandbox docs bundle.
5. **[VERIFICATION]** Confirm the file exists and contains the title and intro paragraph.
6. **[COMPLETION]** Record evidence under `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0001/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-1/work/index.md` exists.
- File `.dev/e2e-reflect/tl-1/work/index.md` contains a markdown H1 title.
- File `.dev/e2e-reflect/tl-1/work/index.md` contains an intro paragraph below the title.
- Evidence path `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0001/evidence.md` records the verification.

**Validation:**

- Manual check: reviewer confirms `.dev/e2e-reflect/tl-1/work/index.md` has a title and intro paragraph.
- Evidence: linkable artifact produced at `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0001/evidence.md`.

**Dependencies:** None
**Rollback:** Remove `.dev/e2e-reflect/tl-1/work/index.md`.

---

### T01.02 -- Create sandbox glossary markdown

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | The roadmap requires `.dev/e2e-reflect/tl-1/work/glossary.md` with three placeholder terms. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0002/spec.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0002/notes.md`
- `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0002/evidence.md`

**Deliverables:**

- File `.dev/e2e-reflect/tl-1/work/glossary.md` containing three placeholder terms.

**Steps:**

1. **[PLANNING]** Load roadmap item R-002 and identify the glossary path.
2. **[PLANNING]** Check that no path outside `.dev/e2e-reflect/tl-1/work/` is needed.
3. **[EXECUTION]** Create `.dev/e2e-reflect/tl-1/work/glossary.md` with a markdown title.
4. **[EXECUTION]** Add three placeholder glossary terms.
5. **[VERIFICATION]** Confirm the glossary contains exactly three placeholder terms.
6. **[COMPLETION]** Record evidence under `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0002/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-1/work/glossary.md` exists.
- File `.dev/e2e-reflect/tl-1/work/glossary.md` contains three placeholder glossary terms.
- The glossary content is deterministic across repeated runs.
- Evidence path `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0002/evidence.md` records the verification.

**Validation:**

- Manual check: reviewer confirms `.dev/e2e-reflect/tl-1/work/glossary.md` has three placeholder terms.
- Evidence: linkable artifact produced at `.dev/e2e-reflect/live-tl/bundle/artifacts/D-0002/evidence.md`.

**Dependencies:** None
**Rollback:** Remove `.dev/e2e-reflect/tl-1/work/glossary.md`.

---

### T01.03 -- Checkpoint: End of Phase 01

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Gate: verify outputs of tasks T01.01-T01.02 before phase completion. |
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
| Deliverable IDs | D-CP01 |

**Checkpoint Report Path:** `.dev/e2e-reflect/live-tl/bundle/checkpoints/CP-P01-END.md`

**Purpose:** Verify Phase 1 scaffold artifacts before post-execution reflection.

**Verification:**

- Confirm `.dev/e2e-reflect/tl-1/work/index.md` exists.
- Confirm `.dev/e2e-reflect/tl-1/work/glossary.md` exists.
- Confirm evidence files for D-0001 and D-0002 are recorded.

**Exit Criteria:**

- T01.01 is complete.
- T01.02 is complete.
- Checkpoint report path is ready for execution evidence.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for T01.01-T01.02.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/live-tl/bundle/checkpoints/CP-P01-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T01.01 and T01.02.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.02
**Rollback:** N/A (checkpoints are read-only verifications)

---

### T01.04 -- Post-Execution Reflection: sc:reflect --mode post

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002 |
| Why | Independent post-execution deviation audit of every task in Phase 1, in a fresh session, after all phase work completes. |
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
| Deliverable IDs | D-RF01 |

**Reflect Report Path:** `.dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-01/REPORT.md`

**Spawn Directive (fresh session):** Spawn a NEW agent/session and run:
`/sc:reflect --mode post --remediate --tasklist .dev/e2e-reflect/live-tl/bundle/phase-1-tasklist.md --diff <phase-commit-range> --depth quick --tier 1 --executor-model <EXECUTOR_CLASS> --output .dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-01/`
(The reflect agent uses the default subagent model; `--executor-model` is the reflect-native exclusion flag naming the class that ran the phase's work, so reflect removes it from the reviewer pool — it does not select a model. Never the `sc:task` execution command.)

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-01/REPORT.md`

**Deliverables:**

- Post-execution reflect report for Phase 1.

**Steps:**

1. **[VERIFICATION]** Resolve `<phase-commit-range>` = the git range covering all of Phase 1's task commits.
2. **[VERIFICATION]** Spawn a fresh session and invoke the Spawn Directive above (reflect audits the committed diff — cross-session-safe).
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface its deviation counts (authorized/necessary/drift/regression).

**Acceptance Criteria:**

- File `.dev/e2e-reflect/live-tl/bundle/validation/reflect-post/phase-01/REPORT.md` exists with a deviation-taxonomy summary.
- Zero `regression`-class deviations, OR a `--remediate` Tier-3 task was authored for each.
- Reflect ran with executor-disjoint reviewers (the `<EXECUTOR_CLASS>` passed via `--executor-model` was excluded from the reviewer pool).
- Report includes the per-task verdict matrix for Phase 1.

**Validation:**

- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** all regular + checkpoint tasks in Phase 1.
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately).
