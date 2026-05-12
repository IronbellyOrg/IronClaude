# Phase 4 -- Tier 3 Deferred / Conditional

**Phase Goal:** Phase 5 designates Tier 3 (A2, B5, B2, A3) as "Defer or merge" pending preconditions. This phase carries the four refactors plus two prerequisite-clarification tasks (B5 needs a Jenkins-Script-Console fetcher; B2 is conditional on user intent for the unanchored `.gitignore` line). Tasks should not ship unless their precondition clarifies in favor of execution; otherwise mark as Deferred in feedback-log.

### T04.01 -- Spec->file application audit (parse `+`/`-` hunks; grep target)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | A2 detects when a spec's `+`/`-` hunks are not present in the named target file by parsing the spec hunks and re-grepping; Phase 5 says A2 should be reconsidered once C2 ships -- the reconsideration may favor retirement (`A2 ⊂ A5` redundancy, line 77) rather than shipping. Confirm ship-vs-retire decision in `feedback-log.md` before executing. Rank 11 of 14 (Priority 0.666). |
| Effort | S |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0012/spec.md`
- `TASKLIST_ROOT/artifacts/D-0012/notes.md`
- `TASKLIST_ROOT/artifacts/D-0012/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `spec_to_file_application_audit(spec_path)` subroutine that parses `+` and `-` hunks from the spec, identifies the named target file(s), and emits `DISCREPANCY: spec-hunk-not-applied` when the `+` hunk content is absent from the target (or the `-` hunk content is still present).

**Steps:**
1. **[PLANNING]** Decide ship-vs-retire for A2 against the A5 (T02.01) shipped state per Phase 5 line 77 redundancy; record decision in `feedback-log.md`. Abort task if decision is Retire.
2. **[PLANNING]** Load `/sc:reflect`; pick a hunk parser (parse-only, no patch application).
3. **[PLANNING]** Define target-resolution: parse `<file>:<lines>` anchors in spec heading or front-matter; fall back to nearest preceding code-fence path comment.
4. **[EXECUTION]** Implement the parser + grep runner; emit `DISCREPANCY: spec-hunk-not-applied` per missing `+` line or surviving `-` line.
5. **[EXECUTION]** Add fixture: `phase4.2-move-artifacts-to-opt-docker.md:141-160` against `pipeline-script-phase3.1.groovy:289-297`; confirm DISCREPANCY emits with the unsatisfied hunk lines.
6. **[VERIFICATION]** Run on the §4.2 fixture; cross-reference with T03.07 to ensure the false-positive class Phase 5 warned about is gone.
7. **[COMPLETION]** Document parser, fixture, run log in `TASKLIST_ROOT/artifacts/D-0012/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `spec_to_file_application_audit` subroutine emitting `DISCREPANCY: spec-hunk-not-applied` on the documented schema.
- Running the patched protocol on the §4.2 spec against the bug fixture emits a DISCREPANCY row quoting the unsatisfied hunk line(s).
- Two consecutive runs produce byte-identical DISCREPANCY output (deterministic).
- Parser, target-resolution rule, fixture, run log recorded in `TASKLIST_ROOT/artifacts/D-0012/spec.md` and `evidence.md`.

**Validation:**
- Manual check: applying the missing hunk to the mirror file removes the DISCREPANCY on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0012/`.

**Dependencies:** T03.07 (Phase 5 explicitly says A2 has a false-positive class without C2)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 4 redundancy note: A2 ⊂ A5; if T02.01 alone is judged sufficient by feedback-log, consider retiring A2 instead of shipping it.

### T04.02 -- Clarify: B5 prerequisite (Jenkins-Script-Console fetcher availability)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Phase 5 explicitly says "B5 requires a Jenkins-Script-Console fetcher that doesn't exist in the project today". Cannot ship B5 (T04.03) until this prerequisite is confirmed available, scoped, or formally deferred. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | dependency (Jenkins fetcher) |
| Tier | LIGHT |
| Confidence | [██████----] 60% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0013/spec.md`
- `TASKLIST_ROOT/artifacts/D-0013/notes.md`
- `TASKLIST_ROOT/artifacts/D-0013/evidence.md`

**Deliverables:**
- A written decision artifact recording one of: (a) Jenkins-Script-Console fetcher is now available at `<path>` and B5 may ship; (b) fetcher will be built as part of B5 with scope `<scope>`; (c) B5 is deferred until fetcher lands as a separate work item.

**Steps:**
1. **[PLANNING]** Read Phase 5 §"Tier 3 -- Defer or merge" and the matrix row for B5 to confirm the prerequisite statement.
2. **[PLANNING]** Survey the project for any existing Jenkins-Script-Console fetcher (grep for `script.console`, `crumbIssuer`, `groovy=` POSTs).
3. **[EXECUTION]** Decide which of the three paths applies; record the decision and rationale in `TASKLIST_ROOT/artifacts/D-0013/spec.md`.
4. **[VERIFICATION]** If decision is (a) or (b), update T04.03 metadata (Dependencies, Effort) accordingly. If (c), set T04.03 status to Deferred in feedback-log.
5. **[COMPLETION]** Note the decision and impacts in `feedback-log.md` Override Reason column for T04.03.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0013/spec.md` exists and records exactly one decision (a/b/c) with a written rationale and any pointer to an existing fetcher path.
- T04.03's Dependencies field or Deferred status is updated to reflect the decision.
- Decision recorded; impacts on T04.03 effort and shipping path identified in the rationale.
- Reviewed with stakeholder(s).

**Validation:**
- Manual check: T04.03 metadata in `phase-4-tasklist.md` matches the decision recorded in `D-0013/spec.md`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0013/`.

**Dependencies:** None (blocks T04.03)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Per Section 4.6 main rule: cannot make T04.03 executable without this missing detail.

### T04.03 -- Tri-source reconciliation (live <-> mirror <-> handoff) -- needs Jenkins fetcher

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | B5 reconciles three sources of truth (Jenkins live job XML, repo mirror file, handoff doc claims); cannot ship without a fetcher to read live job state. Rank 12 of 14 (Priority 0.515). |
| Effort | M |
| Risk | Low |
| Risk Drivers | dependency (Jenkins fetcher) |
| Tier | STANDARD |
| Confidence | [██████----] 65% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`
- `TASKLIST_ROOT/artifacts/D-0014/notes.md`
- `TASKLIST_ROOT/artifacts/D-0014/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `tri_source_reconciliation(live_fetcher, mirror_path, handoff_path)` subroutine that diffs the three sources at named anchors and emits `DISCREPANCY: tri-source-mismatch` per anchor where any pair disagrees.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect`; load the fetcher decision from T04.02 (`D-0013/spec.md`); abort if T04.02 selected option (c) Deferred. If A5 (T02.01) shipped and is judged sufficient by `feedback-log.md`, prefer retiring B5 -- record rationale in `D-0014/spec.md` and abort. Proceed only if reconciliation against live Jenkins XML provides value beyond A5's spec/mirror/live sweep.
2. **[PLANNING]** Define the input contract: the fetcher is a callable returning live job XML/source for a given job name; mirror_path and handoff_path are local files.
3. **[EXECUTION]** Implement the reconciler: call fetcher, read mirror, read handoff anchors; produce a 3-way diff at each anchor; emit `DISCREPANCY: tri-source-mismatch`.
4. **[EXECUTION]** Add fixture (only if option (a) or (b) was chosen in T04.02): a known-divergent job + mirror + handoff; confirm DISCREPANCY emits.
5. **[VERIFICATION]** Run on the project; if option (b), include the new fetcher implementation in this deliverable; if option (a), depend on the existing fetcher.
6. **[COMPLETION]** Document the reconciler, fixture, fetcher integration, run log in `TASKLIST_ROOT/artifacts/D-0014/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `tri_source_reconciliation` subroutine emitting `DISCREPANCY: tri-source-mismatch` on the documented schema (only if T04.02 decision was option (a) or (b)).
- Running the patched protocol on the chosen fixture emits a DISCREPANCY row quoting the three regions and naming the anchor.
- Two consecutive runs produce byte-identical DISCREPANCY output (deterministic).
- Reconciler, fetcher integration approach, fixture, run log recorded in `TASKLIST_ROOT/artifacts/D-0014/spec.md` and `evidence.md`.

**Validation:**
- Manual check: bringing the three sources into agreement removes the DISCREPANCY on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0014/`.

**Dependencies:** T04.02 (must select option (a) or (b)); if (c), this task is Deferred.
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 4 redundancy note: B5 ≈ A5 on this bug. Phase 5 lists B5 at Priority 0.515 (Tier 3 lowest viable); ship only if the fetcher prerequisite resolves favorably.

### T04.04 -- Clarify: B2 .gitignore line intent (design vs accident)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | Phase 5 explicitly says "B2 is conditional on user intent for the unanchored `.gitignore` line (could be design or accident)". Cannot ship B2 (T04.05) until intent is confirmed. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | none |
| Tier | LIGHT |
| Confidence | [██████----] 60% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0015/spec.md`
- `TASKLIST_ROOT/artifacts/D-0015/notes.md`
- `TASKLIST_ROOT/artifacts/D-0015/evidence.md`

**Deliverables:**
- A written decision artifact recording one of: (a) the unanchored `.gitignore` line is intentional design and B2 should ship as an awareness check (warn-only); (b) the line is an accident and B2 should ship as an enforcer that anchors the line and tracks the previously-swept files; (c) defer B2 until further investigation.

**Steps:**
1. **[PLANNING]** Read Phase 5 §"Tier 3" notes and Cluster B context for B2 to confirm the conditional statement.
2. **[PLANNING]** Inspect the project's `.gitignore` for the line in question; identify which paths it currently sweeps.
3. **[EXECUTION]** Decide which of the three options applies; record the decision and any anchored-line rewrite in `TASKLIST_ROOT/artifacts/D-0015/spec.md`.
4. **[VERIFICATION]** Update T04.05 metadata (Tier, scope, behavior) to match.
5. **[COMPLETION]** Note the decision in `feedback-log.md` Override Reason column for T04.05.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0015/spec.md` exists and records exactly one decision (a/b/c) with rationale and (if (b)) the proposed anchored line replacement.
- T04.05's metadata in `phase-4-tasklist.md` is updated to reflect the decision.
- Decision recorded; impacts on T04.05 scope (warn-only vs enforcer vs deferred) identified in the rationale.
- Reviewed with stakeholder(s).

**Validation:**
- Manual check: T04.05 scope description matches the decision recorded in `D-0015/spec.md`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0015/`.

**Dependencies:** None (blocks T04.05)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Per Section 4.6 main rule: cannot make T04.05 executable without this user-intent decision.

### T04.05 -- `.gitignore` anchor-and-coverage check

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | The mirror file may have been swept by an unanchored `.gitignore` `artifacts/*` line (Agent 3's Hypothesis A3.H1, confidence 0.55). B2 detects unanchored sweeps and reports their coverage. Rank 13 of 14 (Priority 0.468). |
| Effort | XS |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [██████----] 65% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0016/spec.md`
- `TASKLIST_ROOT/artifacts/D-0016/notes.md`
- `TASKLIST_ROOT/artifacts/D-0016/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `.gitignore_anchor_coverage_check()` subroutine that detects unanchored ignore patterns and emits `WARN: gitignore-unanchored-sweep` (or `HAZARD:` per T04.04 decision) listing the files each unanchored line currently sweeps. If T04.04 chose option (b), this task additionally rewrites the offending `.gitignore` line to its anchored form.

**Steps:**
1. **[PLANNING]** Load the T04.04 decision from `D-0015/spec.md`; abort if option (c) Deferred was chosen.
2. **[PLANNING]** Define the unanchored-pattern regex (e.g., a line not starting with `/` and not containing `**/` that matches more than one directory tree).
3. **[EXECUTION]** Implement the detector; emit the agreed-on finding category (WARN or HAZARD per T04.04 decision) listing each file currently swept.
4. **[EXECUTION]** If T04.04 chose option (b): apply the anchored rewrite recorded in `D-0015/spec.md` and add the previously-swept files to git tracking in a follow-up commit (do not bundle that commit with the protocol patch).
5. **[VERIFICATION]** Run on the project; confirm only the `.gitignore` line(s) flagged in T04.04 are reported.
6. **[COMPLETION]** Document the detector, decision integration, fixture, run log in `TASKLIST_ROOT/artifacts/D-0016/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `.gitignore_anchor_coverage_check` subroutine emitting the agreed-on finding category on the documented schema.
- Running the patched protocol against the project emits exactly the lines flagged by the T04.04 decision (no false positives).
- Two consecutive runs produce byte-identical output (deterministic).
- Detector, T04.04 integration, fixture, run log recorded in `TASKLIST_ROOT/artifacts/D-0016/spec.md` and `evidence.md`.

**Validation:**
- Manual check: a synthetic anchored-line `.gitignore` produces zero WARN/HAZARD rows on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0016/`.

**Dependencies:** T04.04 (decision must select option (a) or (b))
**Rollback:** TBD (if not specified in roadmap) -- if (b) was chosen, `.gitignore` rewrite is reversible by reverting the commit.
**Notes:** Phase 4 redundancy note: B2 ⊂ B1; if T01.01 (B1) is judged sufficient by feedback-log, B2 may be retired instead of shipping.

### Checkpoint: Phase 4 / Tasks T04.01-T04.05

**Purpose:** Mid-phase checkpoint after the first 5 Phase 4 tasks (3 ships + 2 clarifications), to confirm preconditions for T04.03 and T04.05 are settled and to decide whether the heaviest task (T04.06 A3) is worth the implementation cost.

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md`

**Verification:**
- T04.02 and T04.04 each produced written decisions recorded under `D-0013/` and `D-0015/`.
- T04.01, T04.03 (if not Deferred), T04.05 each report Acceptance Criteria 1 satisfied with named subroutines.
- A combined `/sc:reflect` run on the project surfaces Phase 4 findings (where applicable) without regressing Phase 1-3 outputs.

**Exit Criteria:**
- T04.01 merged; T04.03 status known (merged or Deferred); T04.05 status known (merged or Deferred).
- Decision on T04.06: ship only if an independent ledger initiative exists for other reasons (per Phase 5 line 64-65); otherwise Defer.
- Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md` records Pass.

### T04.06 -- Tool-call no-op detector (SHA pre/post + `edit_ledger.jsonl`)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | A3 detects when an Edit/Write tool call reports success but produced no file change; SHA-pre vs SHA-post comparison plus an `edit_ledger.jsonl` append makes silent no-ops detectable. Rank 14 of 14 (Priority 0.323) -- lowest-likelihood cause AND heaviest implementation footprint per Phase 5; defer unless an independent ledger is built for other reasons. |
| Effort | L |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0017/spec.md`
- `TASKLIST_ROOT/artifacts/D-0017/notes.md`
- `TASKLIST_ROOT/artifacts/D-0017/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `tool_call_noop_detector` subroutine plus a per-session `edit_ledger.jsonl` schema; the subroutine compares SHA-256 of each touched file before and after every Edit/Write tool call, appends a ledger row, and emits `DISCREPANCY: tool-call-no-op` when SHAs match despite a "success" report.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect`; survey existing tool-invocation hooks; design the ledger schema (`{ts, tool, file, sha_pre, sha_post, claimed_outcome, ledger_id}`).
2. **[PLANNING]** Decide ledger location: `TASKLIST_ROOT/evidence/edit_ledger.jsonl` (per-task) or session-level path; record the choice in `D-0017/spec.md`.
3. **[EXECUTION]** Implement SHA capture before and after each Edit/Write call (or the protocol's wrapper); append ledger rows.
4. **[EXECUTION]** Implement the no-op detector that scans the ledger and emits `DISCREPANCY: tool-call-no-op` per row where `sha_pre == sha_post AND claimed_outcome == success`.
5. **[VERIFICATION]** Add fixture: a deliberately-noop Edit (e.g., editing whitespace to itself); confirm DISCREPANCY emits.
6. **[VERIFICATION]** Run on a real edit batch; confirm zero false positives.
7. **[COMPLETION]** Document schema, detector, fixture, run log in `TASKLIST_ROOT/artifacts/D-0017/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `tool_call_noop_detector` subroutine plus the documented `edit_ledger.jsonl` schema; subroutine emits `DISCREPANCY: tool-call-no-op` per the documented rule.
- Running the patched protocol against the no-op fixture emits a DISCREPANCY row whose `ledger_id` matches the fixture entry.
- Two consecutive runs on the same fixture produce byte-identical DISCREPANCY output (deterministic).
- Schema, detector, fixture, run log recorded in `TASKLIST_ROOT/artifacts/D-0017/spec.md` and `evidence.md`.

**Validation:**
- Manual check: a real edit that does change file content does NOT trigger a DISCREPANCY (no false positive).
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0017/`.

**Dependencies:** None hard; ship only if an independent ledger initiative exists for other reasons (per Phase 5 line 64-65); otherwise Defer.
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 5 ranks A3 last (Priority 0.323) and flags it as the heaviest implementation footprint; cost-justify against the ledger's secondary uses before merging.

### Checkpoint: End of Phase 4

**Purpose:** Close the RCA refactor program. Confirm the four Tier 3 outcomes (each Merged or Deferred-with-reason) are recorded and the full `/sc:reflect` rerun against the bug fixture produces a clean, deterministic finding set across all merged subroutines.

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`

**Verification:**
- Each of T04.01, T04.03, T04.05, T04.06 has a recorded outcome (Merged or Deferred-with-reason) in `feedback-log.md`.
- A final `/sc:reflect` run against the §4.2 bug fixture produces findings consistent with all merged Phase 1-4 subroutines and zero contradictions.
- Validation artifacts at `TASKLIST_ROOT/validation/` are present (ValidationReport.md and either PatchChecklist.md + Verification Results, or a clean report).

**Exit Criteria:**
- All four Phase 4 outcomes recorded; deferred items flagged with rationale.
- Final fixture run log archived at `TASKLIST_ROOT/evidence/final-fixture-run.md`.
- Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P04-END.md` records Pass; the RCA refactor program closes here.
