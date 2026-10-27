# Phase 4 -- M4 Five Adversarial Axes Overlay

**Phase Goal:** Insert `### Five Adversarial Axes` header subsection BEFORE rf-qa-qualitative's 15-item task-qualitative checklist; add `axis` column to Items Reviewed table; preserve zero-trust QA invariant and severity floor at `rf-qa-qualitative.md:786-795`; emit `drift-axis-inactive` annotation when no item restates BUILD_REQUEST.GOAL verbatim. Duration: 2 weeks (2026-06-26 → 2026-07-10). Exit: header renders BEFORE 15-item checklist; Axis column populated with `{AX-1..AX-5, none}`; drift-axis-inactive annotation when GOAL-baseline absent; severity floor byte-identical; 15-item checklist body unchanged.

### T04.01 -- Land FR-CONV.4 axis overlay wrapper

| Field | Value |
|---|---|
| Roadmap Item IDs | R-070 |
| Why | Insert axis-overlay header BEFORE rf-qa-qualitative 15-item checklist (CASE-D PR-07); overlay-only, no new conditional code path. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0041 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0041/spec.md`
- `TASKLIST_ROOT/artifacts/D-0041/evidence.md`

**Deliverables:**
- FR-CONV.4 wrapper inserted in rf-qa-qualitative.md + SKILL.md.
- Axis-overlay header subsection renders before 15-item checklist.
- INV-013 composition with inherited structural PASS preserved.

**Steps:**
1. **[PLANNING]** Confirm M3 PASS; FR-CONV.3 Inherited Structural Verdict live.
2. **[PLANNING]** Read R-070 wrapper spec.
3. **[EXECUTION]** Insert FR-CONV.4 wrapper before 15-item checklist.
4. **[VERIFICATION]** Grep ordering: assert axis header before checklist.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "Five Adversarial Axes" src/superclaude/agents/rf-qa-qualitative.md` returns line N preceding `Checklist (15 items)` header line.
- Wrapper does not introduce a new conditional code path (overlay-only).
- 15-item checklist body unchanged.
- Evidence at `TASKLIST_ROOT/artifacts/D-0041/evidence.md`.

**Validation:**
- Manual check: reviewer confirms overlay-only (no new code paths).
- Evidence: grep output.

**Dependencies:** Phase 3 (M3 PASS)
**Rollback:** As stated in roadmap (revertable by removing axis column + annotation; 15-item checklist untouched)
**Notes:** None.

### T04.02 -- Define AX-1 + AX-2 axis canonical entries

| Field | Value |
|---|---|
| Roadmap Item IDs | R-071, R-072 |
| Why | AX-1 Drift: cited fact no longer matches current source. AX-2 Contradictions: two artifacts assert mutually incompatible facts about same subject. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0042/spec.md`
- `TASKLIST_ROOT/artifacts/D-0042/evidence.md`

**Deliverables:**
- AX-1 Drift axis definition + finding example showing stale citation pattern.
- AX-2 Contradictions axis definition + finding example showing return-type mismatch pattern.

**Steps:**
1. **[PLANNING]** Read R-071, R-072 axis specs.
2. **[EXECUTION]** Author AX-1 entry in canonical-axes block §8.5.
3. **[EXECUTION]** Author AX-2 entry in canonical-axes block.
4. **[VERIFICATION]** Grep canonical-axes block for AX-1 and AX-2 enumeration.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -c "AX-1\|AX-2" src/superclaude/agents/rf-qa-qualitative.md` returns at least 2 distinct matches in the canonical-axes block.
- AX-1 definition cites stale citation pattern; AX-2 cites return-type mismatch pattern.
- Both finding examples present.
- Evidence at `TASKLIST_ROOT/artifacts/D-0042/evidence.md`.

**Validation:**
- Manual check: reviewer confirms axis definitions verbatim match roadmap text.
- Evidence: linkable canonical-axes block excerpt.

**Dependencies:** T04.01
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.03 -- Define AX-3 + AX-4 axis canonical entries

| Field | Value |
|---|---|
| Roadmap Item IDs | R-073, R-074 |
| Why | AX-3 Omissions: required touchpoint, consumer, dependency, or step absent from plan. AX-4 Weakened-criteria: acceptance/verification condition softened to unobservable or trivially satisfiable. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0043/spec.md`
- `TASKLIST_ROOT/artifacts/D-0043/evidence.md`

**Deliverables:**
- AX-3 Omissions axis definition + missing signature update pattern.
- AX-4 Weakened-criteria axis definition + trivially passing test pattern.

**Steps:**
1. **[PLANNING]** Read R-073, R-074 axis specs.
2. **[EXECUTION]** Author AX-3 entry.
3. **[EXECUTION]** Author AX-4 entry.
4. **[VERIFICATION]** Grep canonical-axes block for AX-3 and AX-4.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -c "AX-3\|AX-4" src/superclaude/agents/rf-qa-qualitative.md` returns at least 2 distinct matches in the canonical-axes block.
- AX-3 definition cites missing-signature-update pattern; AX-4 cites trivially-passing-test pattern.
- Evidence at `TASKLIST_ROOT/artifacts/D-0043/evidence.md`.
- Both finding examples present.

**Validation:**
- Manual check: reviewer confirms axis definitions verbatim.
- Evidence: linkable excerpt.

**Dependencies:** T04.02
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.04 -- Define AX-5 axis canonical entry

| Field | Value |
|---|---|
| Roadmap Item IDs | R-075 |
| Why | AX-5 Invented-content: artifact introduces requirement/feature/capability not present in upstream source; finding example shows scope inflation pattern. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0044 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0044/spec.md`
- `TASKLIST_ROOT/artifacts/D-0044/evidence.md`

**Deliverables:**
- AX-5 Invented-content axis definition + scope inflation finding example.

**Steps:**
1. **[PLANNING]** Read R-075 axis spec.
2. **[EXECUTION]** Author AX-5 entry.
3. **[VERIFICATION]** Grep canonical-axes block for AX-5.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "AX-5" src/superclaude/agents/rf-qa-qualitative.md` returns at least 1 match in the canonical-axes block.
- AX-5 definition cites scope inflation pattern.
- Evidence at `TASKLIST_ROOT/artifacts/D-0044/evidence.md`.
- Finding example present and aligned with FR-CONV.4 spec.

**Validation:**
- Manual check: reviewer confirms axis definition verbatim.
- Evidence: linkable excerpt.

**Dependencies:** T04.03
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.05 -- Wire `none` sentinel + `drift-axis-inactive` annotation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-076, R-077 |
| Why | `none` sentinel: passing check with axis lens surfacing nothing (NOT N/A escape). `drift-axis-inactive`: Summary-block annotation when artifact has no citations to drift against. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0045 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0045/spec.md`
- `TASKLIST_ROOT/artifacts/D-0045/evidence.md`

**Deliverables:**
- `none` sentinel documented; not an N/A escape.
- `drift-axis-inactive` annotation emitted in Summary block.
- Canonical annotation rules in rf-qa-qualitative.md.

**Steps:**
1. **[PLANNING]** Read R-076, R-077 specs.
2. **[EXECUTION]** Document `none` sentinel value usage.
3. **[EXECUTION]** Implement `drift-axis-inactive` annotation emitter.
4. **[VERIFICATION]** GOAL-baseline-absent fixture emits `drift-axis-inactive`.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "drift-axis-inactive" src/superclaude/agents/rf-qa-qualitative.md` returns annotation rule.
- GOAL-baseline-absent fixture's Summary block contains the literal `drift-axis-inactive` annotation.
- Passing check uses `none` sentinel, NOT `N/A`.
- Evidence at `TASKLIST_ROOT/artifacts/D-0045/evidence.md`.

**Validation:**
- Manual check: reviewer confirms `none` ≠ `N/A`.
- Evidence: fixture run + annotation log.

**Dependencies:** T04.04
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.06 -- Checkpoint: Phase 4 / Tasks T04.01-T04.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-070, R-071, R-072, R-073, R-074, R-075, R-076, R-077 |
| Why | Gate: verify FR-CONV.4 wrapper + AX-1..AX-5 + `none` sentinel + `drift-axis-inactive` annotation before axis-column + edit-site work. |
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
| Deliverable IDs | D-CP04-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md`

**Purpose:** Mid-phase gate confirming all five axis definitions + `none` sentinel + `drift-axis-inactive` annotation are operational before column-insertion edits.

**Verification:**
- Canonical axes block contains AX-1..AX-5 entries (D-0041..D-0044 evidence).
- `none` sentinel + `drift-axis-inactive` annotation rules in place (D-0045 evidence).
- FR-CONV.4 wrapper precedes 15-item checklist (D-0041 evidence).

**Exit Criteria:**
- All 5 regular tasks T04.01-T04.05 report PASS.
- GOAL-baseline-absent fixture emits `drift-axis-inactive` annotation.
- Passing checks use `none` sentinel, not N/A.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T04.01-T04.05.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.01..T04.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T04.07 -- Add Axis column to Items Reviewed table

| Field | Value |
|---|---|
| Roadmap Item IDs | R-078 |
| Why | Insert `axis` column between `Check` and `Result` columns at rf-qa-qualitative.md:675-714; every task-qualitative row carries one canonical axis or `none`; column omitted for non-task-qualitative phases. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0046/spec.md`
- `TASKLIST_ROOT/artifacts/D-0046/evidence.md`

**Deliverables:**
- Axis column inserted in Items Reviewed table at :675-714.
- Every task-qualitative row carries one canonical axis or `none`.
- Column omitted for non-task-qualitative phases.

**Steps:**
1. **[PLANNING]** Read R-078 column-insertion spec.
2. **[EXECUTION]** Modify Items Reviewed table at lines 675-714.
3. **[EXECUTION]** Insert axis column between Check and Result.
4. **[VERIFICATION]** Parse table; assert no empty Axis cells in task-qualitative phase.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "| Check | axis | Result |" src/superclaude/agents/rf-qa-qualitative.md` or equivalent header line returns the new table header.
- Every task-qualitative row in the Items Reviewed table has a non-empty Axis value.
- Non-task-qualitative phase tables do not include the Axis column.
- Evidence at `TASKLIST_ROOT/artifacts/D-0046/evidence.md`.

**Validation:**
- Manual check: reviewer confirms column position.
- Evidence: parsed-table excerpt.

**Dependencies:** T04.06
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.08 -- Insert Five Adversarial Axes header subsection

| Field | Value |
|---|---|
| Roadmap Item IDs | R-079 |
| Why | `### Five Adversarial Axes` subsection inserted BEFORE `#### Checklist (15 items)` header at rf-qa-qualitative.md:527-583. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0047 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0047/spec.md`
- `TASKLIST_ROOT/artifacts/D-0047/evidence.md`

**Deliverables:**
- `### Five Adversarial Axes` subsection inserted at 527-583 range, before the 15-item Checklist header.
- 15-item checklist body unmodified.
- Ordering grep evidence.

**Steps:**
1. **[PLANNING]** Capture byte hash of 15-item checklist body :527-583 pre-edit.
2. **[PLANNING]** Read R-079 insertion spec.
3. **[EXECUTION]** Insert axes subsection above the 15-item Checklist header.
4. **[VERIFICATION]** Grep ordering: axes header line N precedes Checklist header line M.
5. **[VERIFICATION]** Byte-diff 15-item checklist body pre/post; assert zero diff.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "Five Adversarial Axes\|Checklist (15 items)" src/superclaude/agents/rf-qa-qualitative.md | sort -t: -k2n` shows Axes header line precedes Checklist header line.
- Byte-diff of the 15-item checklist body (lines :527-583) pre/post insertion is zero.
- Evidence at `TASKLIST_ROOT/artifacts/D-0047/evidence.md`.
- Tool-Engagement-Minimum still ≥15 tool calls.

**Validation:**
- Manual check: reviewer confirms ordering.
- Evidence: byte-diff + grep.

**Dependencies:** T04.07
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.09 -- Verify 15-item checklist body preservation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-080 |
| Why | Body at rf-qa-qualitative.md:527-583 MUST be unmodified; axes multiply lenses, not checks (TOTAL stays at 15 items). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0048 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0048/evidence.md`

**Deliverables:**
- Byte-diff report of 15-item checklist body pre/post phase changes.
- Confirmation that count stays at 15 items.
- Tool-Engagement-Minimum unchanged.

**Steps:**
1. **[PLANNING]** Reference the pre-edit byte hash from T04.08.
2. **[EXECUTION]** Re-diff the body after all axis-overlay edits.
3. **[VERIFICATION]** Assert byte-diff is empty.
4. **[VERIFICATION]** Count items in the body; assert exactly 15.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Byte-diff of rf-qa-qualitative.md:527-583 body pre/post all M4 changes is zero.
- Item count in the body is exactly 15.
- Tool-Engagement-Minimum statement unchanged (search for "tool calls ≥15" in surrounding text).
- Evidence at `TASKLIST_ROOT/artifacts/D-0048/evidence.md`.

**Validation:**
- Manual check: reviewer confirms 15 items unchanged.
- Evidence: byte-diff + count log.

**Dependencies:** T04.08
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.10 -- Verify severity-floor preservation (786-795)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-081 |
| Why | Contradictions always IMPORTANT/CRITICAL; severity floor at rf-qa-qualitative.md:786-795 MUST NOT be weakened. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0049 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0049/evidence.md`

**Deliverables:**
- Byte-diff report of severity floor at :786-795 pre/post.
- Critical Rules block byte-identical.

**Steps:**
1. **[PLANNING]** Capture byte hash of rf-qa-qualitative.md:786-795 pre-edit.
2. **[EXECUTION]** No edits should land in this range during M4.
3. **[VERIFICATION]** Re-hash post-edit; assert match.
4. **[VERIFICATION]** Byte-diff Critical Rules block pre/post; assert zero diff.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Byte-diff of rf-qa-qualitative.md:786-795 pre/post all M4 changes is zero.
- Contradictions severity floor (IMPORTANT/CRITICAL) verbatim in the block.
- Evidence at `TASKLIST_ROOT/artifacts/D-0049/evidence.md`.
- Critical Rules block hash matches the baseline captured pre-edit.

**Validation:**
- Manual check: reviewer confirms block unchanged.
- Evidence: byte-diff log.

**Dependencies:** T04.09
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.11 -- Edit COMP-004-M4 axis-column site (675-714)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-082 |
| Why | Modify Items Reviewed table at rf-qa-qualitative.md:675-714 to add `axis` column between `Check` and `Result`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0050 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0050/spec.md`
- `TASKLIST_ROOT/artifacts/D-0050/evidence.md`

**Deliverables:**
- COMP-004-M4 edit applied at lines 675-714.
- Axis-column header inserted.
- Parse confirms one axis value per row.

**Steps:**
1. **[PLANNING]** Read R-082 edit constraints.
2. **[EXECUTION]** Edit Items Reviewed table at lines 675-714.
3. **[VERIFICATION]** Parse table; assert axis header and one axis value per row.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "| .* | axis | .* |" src/superclaude/agents/rf-qa-qualitative.md` returns header line in [675, 714].
- Every task-qualitative row has a non-empty axis value drawn from `{AX-1..AX-5, none}`.
- Evidence at `TASKLIST_ROOT/artifacts/D-0050/evidence.md`.
- Edit confined to lines 675-714.

**Validation:**
- Manual check: reviewer confirms column position.
- Evidence: parsed-table excerpt.

**Dependencies:** T04.07
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.12 -- Checkpoint: Phase 4 / Tasks T04.07-T04.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-078, R-079, R-080, R-081, R-082 |
| Why | Gate: verify axis-column insertion, header subsection, and preservation diffs before SKILL.md edits + test fixtures. |
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
| Deliverable IDs | D-CP04-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T07-T11.md`

**Purpose:** Mid-phase gate confirming axis column inserted, header subsection precedes checklist, 15-item body unchanged, severity floor preserved.

**Verification:**
- Axis column on Items Reviewed table at 675-714 (D-0046 + D-0050 evidence).
- Five Adversarial Axes header subsection before 15-item Checklist (D-0047 evidence).
- 15-item body + severity floor byte-diff zero (D-0048 + D-0049 evidence).

**Exit Criteria:**
- All 5 regular tasks T04.07-T04.11 report PASS.
- 15-item checklist body and severity floor byte-identical.
- Every task-qualitative row has one canonical axis value.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T04.07-T04.11.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.07..T04.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T04.13 -- Edit COMP-001-M4 SKILL.md task-qualitative prompt axis directive (961)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-083 |
| Why | Add axis-annotation directive at SKILL.md:961 in Task-Qualitative prompt; instructs annotation per row. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0051 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0051/spec.md`
- `TASKLIST_ROOT/artifacts/D-0051/evidence.md`

**Deliverables:**
- Axis-annotation directive inserted at SKILL.md:~961.
- Directive instructs per-row annotation in canonical axes vocabulary.

**Steps:**
1. **[PLANNING]** Read R-083 edit constraints.
2. **[EXECUTION]** Edit SKILL.md at line ~961 with axis-annotation directive.
3. **[VERIFICATION]** `grep -n "Axis" src/superclaude/skills/task-builder/SKILL.md`; assert at least 1 match around line 961.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "Axis" src/superclaude/skills/task-builder/SKILL.md` returns at least 1 match with line N within [958, 964] (small tolerance for whitespace shifts).
- Directive references the `{AX-1..AX-5, none}` vocabulary.
- Evidence at `TASKLIST_ROOT/artifacts/D-0051/evidence.md`.
- Edit confined to the named line range.

**Validation:**
- Manual check: reviewer confirms directive ties to canonical vocabulary.
- Evidence: linkable grep output.

**Dependencies:** T04.12
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.14 -- Commit TEST-011..014 axis overlay fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-084, R-085, R-086, R-087 |
| Why | TEST-011 axes header before checklist; TEST-012 axis column non-empty on every row; TEST-013 drift-axis-inactive when no GOAL-baseline; TEST-014 severity-floor block unchanged. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0052 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0052/evidence.md`

**Deliverables:**
- TEST-011 ordering fixture.
- TEST-012 axis-column populated fixture.
- TEST-013 drift-axis-inactive annotation fixture.
- TEST-014 severity-floor preservation fixture.

**Steps:**
1. **[PLANNING]** Read R-084..R-087 fixture specs.
2. **[EXECUTION]** Author the four fixtures under `tests/audit/`.
3. **[VERIFICATION]** Run all four via pytest; assert all green.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_five_axes_overlay.py tests/audit/test_axis_column_populated.py tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py tests/audit/test_severity_floor_unweakened.py -v` exits 0.
- TEST-013 asserts `drift-axis-inactive` literal annotation in Summary block.
- TEST-014 asserts byte-diff of Critical Rules block is zero.
- Evidence at `TASKLIST_ROOT/artifacts/D-0052/evidence.md`.

**Validation:**
- Manual check: reviewer confirms each fixture's assertion matches roadmap spec.
- Evidence: pytest log.

**Dependencies:** T04.08, T04.09, T04.10, T04.11, T04.13
**Rollback:** As stated in roadmap
**Notes:** None.

### T04.15 -- Execute MIG-004 PR-07 landing migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-088, R-089 |
| Why | Strictly-additive overlay single commit; revertable by removing axis column + drift-axis-inactive annotation; 15-item checklist untouched; FF_FIVE_ADVERSARIAL_AXES governance. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0053 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0053/spec.md`
- `TASKLIST_ROOT/artifacts/D-0053/evidence.md`

**Deliverables:**
- MIG-004 single commit landing FR-CONV.4.
- `make verify-sync` PASS.
- FF_FIVE_ADVERSARIAL_AXES governance entry referenced for M7.

**Steps:**
1. **[PLANNING]** Confirm T04.14 fixtures green.
2. **[PLANNING]** Run `make verify-sync` clean baseline.
3. **[EXECUTION]** Stage all rf-qa-qualitative.md + SKILL.md edits.
4. **[EXECUTION]** Commit with revert path documented (remove overlay; checklist intact).
5. **[VERIFICATION]** Run `make verify-sync` post-commit; assert PASS.
6. **[COMPLETION]** Spawn quality-engineer sub-agent for diff spot-check.

**Acceptance Criteria:**
- `make verify-sync` exits 0 immediately after MIG-004 commit.
- Commit body documents axis-overlay removal as rollback path.
- Sub-agent report confirms 15-item checklist + severity floor byte-identical.
- FF_FIVE_ADVERSARIAL_AXES `TASKLIST_ROOT/artifacts/D-0053/spec.md` records (a) logical-flag designation, (b) revert path = remove overlay, (c) cleanup gate = K-004 axis-distribution audit, (d) M7 consolidation reference.

**Validation:**
- Manual check: reviewer confirms strictly-additive overlay.
- Evidence: `make verify-sync` log + commit diff + sub-agent report.

**Dependencies:** T04.14
**Rollback:** As stated in roadmap (remove overlay; checklist intact)
**Notes:** Critical-path override applied because MIG-004 is the M4 landing gate.

### T04.16 -- Checkpoint: End of Phase 4

| Field | Value |
|---|---|
| Roadmap Item IDs | R-070, R-071, R-072, R-073, R-074, R-075, R-076, R-077, R-078, R-079, R-080, R-081, R-082, R-083, R-084, R-085, R-086, R-087, R-088, R-089 |
| Why | Gate: verify all M4 deliverables (axis overlay, AX-1..AX-5, axis column, header subsection, 15-item + severity-floor preservation, fixtures, MIG-004) before unblocking M5. |
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
| Deliverable IDs | D-CP04 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`

**Purpose:** End-of-Phase-4 gate confirming Five Adversarial Axes overlay live without disturbing 15-item checklist or severity floor; MIG-004 merged; axis-distribution audit-prep complete.

**Verification:**
- Five Adversarial Axes header subsection precedes 15-item Checklist (D-0047 evidence).
- Axis column populated on every task-qualitative row with canonical vocabulary (D-0046 + D-0050 evidence).
- MIG-004 merged with `make verify-sync` PASS (D-0053 evidence).

**Exit Criteria:**
- All 13 regular tasks T04.01-T04.05, T04.07-T04.11, T04.13-T04.15 (skipping mid-checkpoints) report PASS.
- M4 Exit Conditions per roadmap (axes header before checklist, axis column populated, drift-axis-inactive annotation when GOAL absent, severity floor byte-stable, checklist unchanged) all met.
- K-004 audit-prep note recorded.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Inspect M4 Exit Conditions checklist; assert every item is satisfied.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above with `Overall: Pass`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T04.01-T04.15 it covers.

**Validation:**
- Manual check: reviewer confirms the report declares M4 PASS and unblocks M5.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.01..T04.05, T04.07..T04.11, T04.13..T04.15
**Rollback:** N/A (checkpoints are read-only verifications)
