# Phase 3 -- M3 Inherited Verdict + Self-Audit

**Phase Goal:** Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt under `## Inherited Structural Verdict` with directive; add `## Self-Audit` to rf-qa-qualitative output schema; preserve zero-trust QA invariant and anti-inflation rule at `rf-qa-qualitative.md:766-775` byte-stable; enforce INV-002 freshness, INV-010 dynamic enumeration, INV-019 Self-Audit obligation. Duration: 2 weeks (2026-06-12 → 2026-06-26). Exit: spawn prompt carries verdict table byte-for-byte; on fix-cycle re-run orchestrator re-injects NEW cycle-N verdict; rf-qa-qualitative output contains Self-Audit with ≥1 semantic check; anti-inflation bullet at :770 byte-identical.

### T03.01 -- Land FR-CONV.3 Inherited Verdict + Self-Audit wrapper

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt; add Self-Audit to output schema (CASE-B PR-04); preserve zero-trust QA invariant. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting, dependencies |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0026/spec.md`
- `TASKLIST_ROOT/artifacts/D-0026/evidence.md`

**Deliverables:**
- FR-CONV.3 wrapper landed across SKILL.md + rf-qa-qualitative.md.
- Verdict table byte-for-byte in spawn prompt.
- Self-Audit listed in output schema with ≥1 semantic check.

**Steps:**
1. **[PLANNING]** Confirm Phase 2 PASS; TB-Add catalogue stable (Phase 1).
2. **[PLANNING]** Read R-049 wrapper spec.
3. **[EXECUTION]** Author FR-CONV.3 wrapper in SKILL.md + rf-qa-qualitative.md.
4. **[EXECUTION]** Wire spawn-prompt injection of verdict table.
5. **[VERIFICATION]** Spawn quality-engineer sub-agent to validate wrapper preserves zero-trust QA.
6. **[COMPLETION]** Evidence + sub-agent report.

**Acceptance Criteria:**
- `grep -c "Inherited Structural Verdict" src/superclaude/skills/task-builder/SKILL.md` returns at least 1 match in the A.10.5 spawn prompt block.
- Self-Audit heading present in rf-qa-qualitative.md output schema.
- Sub-agent quality-engineer report confirms zero-trust QA preserved (no PASS without independent semantic check).
- Evidence at `TASKLIST_ROOT/artifacts/D-0026/evidence.md`.

**Validation:**
- Manual check: reviewer confirms wrapper landed without disturbing anti-inflation block.
- Evidence: sub-agent report.

**Dependencies:** Phase 2 (M2 PASS); TB-Add catalogue (M1)
**Rollback:** As stated in roadmap (disable passthrough flag; fall back to independent structural re-checking)
**Notes:** None.

### T03.02 -- Implement DM-002-M3 schema (3 sub-fields)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050, R-051, R-052, R-053 |
| Why | Implement DM-002 entity per M1 contract-freeze with all 3 fields populated (rf_qa_table_verbatim byte-exact, prompt_directive fixed-value, reinjection_rule fixed-value). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting, schema |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0027/spec.md`
- `TASKLIST_ROOT/artifacts/D-0027/evidence.md`

**Deliverables:**
- DM-002 entity implemented with all 3 fields.
- rf_qa_table_verbatim: byte-exact diff against qa-task-integrity Items Reviewed table.
- prompt_directive + reinjection_rule emitted verbatim per spec.

**Steps:**
1. **[PLANNING]** Confirm DM-002 contract-freeze (T01.13).
2. **[PLANNING]** Read R-050..R-053 field specs.
3. **[EXECUTION]** Implement rf_qa_table_verbatim: copy Items Reviewed table byte-exact at spawn time.
4. **[EXECUTION]** Emit prompt_directive: `"PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."` verbatim.
5. **[EXECUTION]** Emit reinjection_rule: `"On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."` verbatim.
6. **[VERIFICATION]** Diff DM-002 implementation against M1 contract-freeze; sub-agent confirms field-for-field match.

**Acceptance Criteria:**
- Diff of emitted rf_qa_table_verbatim vs qa-task-integrity Items Reviewed table is byte-identical (zero diff bytes).
- prompt_directive string appears verbatim in emitted DM-002 instance.
- reinjection_rule string appears verbatim in emitted DM-002 instance.
- Sub-agent report confirms 3-field contract-freeze match.

**Validation:**
- Manual check: reviewer confirms verbatim strings unaltered.
- Evidence: sub-agent report + diff output.

**Dependencies:** T03.01; T01.13
**Rollback:** As stated in roadmap
**Notes:** Critical-path override applied because DM-002 wire shape governs M3+M4 composition.

### T03.03 -- Implement API-002-M3 spawn-prompt injection at SKILL.md §A.10.5

| Field | Value |
|---|---|
| Roadmap Item IDs | R-054 |
| Why | Orchestrator-mediated spawn-prompt injection at SKILL.md §A.10.5; extracts Items Reviewed table contiguously; splices verbatim into spawn prompt. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0028/spec.md`
- `TASKLIST_ROOT/artifacts/D-0028/evidence.md`

**Deliverables:**
- API-002 implementation at SKILL.md §A.10.5.
- Contiguous Items Reviewed table extraction logic.
- Verbatim splice into spawn prompt (after TARGET FILES, before INSTRUCTIONS).

**Steps:**
1. **[PLANNING]** Confirm DM-005 published (T02.04).
2. **[PLANNING]** Read R-054 API spec.
3. **[EXECUTION]** Implement orchestrator extraction step in SKILL.md §A.10.5.
4. **[EXECUTION]** Splice verdict table at the prescribed location.
5. **[VERIFICATION]** Grep spawn-log for "Inherited Structural Verdict"; diff block vs qa-task-integrity.md.
6. **[COMPLETION]** Sub-agent report.

**Acceptance Criteria:**
- `grep -n "Inherited Structural Verdict" <spawn-log>` returns line N.
- Diff of injected block vs `qa-task-integrity.md` Items Reviewed table is byte-identical.
- Sub-agent quality-engineer report confirms splice position (after TARGET FILES, before INSTRUCTIONS).
- Evidence at `TASKLIST_ROOT/artifacts/D-0028/evidence.md`.

**Validation:**
- Manual check: reviewer confirms splice position in a real spawn-log.
- Evidence: sub-agent report.

**Dependencies:** T03.02; DM-005 (T02.04)
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.04 -- Add Self-Audit output schema + INV-019 obligation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-055, R-058 |
| Why | Add `## Self-Audit` section to rf-qa-qualitative output listing relied-on PASS items AND ≥1 semantic check; INV-019 consumer obligation enforced. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0029/spec.md`
- `TASKLIST_ROOT/artifacts/D-0029/evidence.md`

**Deliverables:**
- Self-Audit section in rf-qa-qualitative.md output schema.
- INV-019 enforcement: ≥1 semantic check per run.
- K-003 audit-target documented.

**Steps:**
1. **[PLANNING]** Read R-055, R-058 specs.
2. **[PLANNING]** Locate rf-qa-qualitative.md EOF (line 794).
3. **[EXECUTION]** Append Self-Audit output schema requirement.
4. **[EXECUTION]** Document INV-019 obligation: lists relied-on PASS items AND ≥1 semantic check.
5. **[VERIFICATION]** Run a sample rf-qa-qualitative cycle; grep for `## Self-Audit`; assert content.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "## Self-Audit" src/superclaude/agents/rf-qa-qualitative.md` returns a match at or after line 794.
- Self-Audit output includes both rf-qa PASS reliance list AND ≥1 documented semantic check.
- A run with 0 entries in the semantic-check category is flagged as INV-019 violation.
- Evidence at `TASKLIST_ROOT/artifacts/D-0029/evidence.md`.

**Validation:**
- Manual check: reviewer confirms Self-Audit content includes both categories.
- Evidence: sample output + grep log.

**Dependencies:** T03.03
**Rollback:** As stated in roadmap
**Notes:** Runtime sample verification deferred to T03.14 (TEST-009 self-audit fixture).

### T03.05 -- Wire INV-002 freshness rule (cycle-N+1 reinjection)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-056 |
| Why | Orchestrator MUST re-read current rf-qa task-integrity report and re-extract table on every fix-cycle spawn; stale verdicts forbidden. |
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
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0030/spec.md`
- `TASKLIST_ROOT/artifacts/D-0030/evidence.md`

**Deliverables:**
- Freshness rule enforced at every fix-cycle spawn.
- 2-cycle fixture asserting cycle-2 spawn carries cycle-2 verdict.
- Stale-verdict-rejection logic in orchestrator.

**Steps:**
1. **[PLANNING]** Read R-056 freshness rule.
2. **[PLANNING]** Identify spawn step in SKILL.md §A.10.5.
3. **[EXECUTION]** Add re-extract step at every fix-cycle entry.
4. **[VERIFICATION]** Run 2-cycle fixture; byte-diff cycle-1 vs cycle-2 spawn prompts at the table region; assert difference reflects cycle-2 verdict.
5. **[VERIFICATION]** Confirm stale verdict from cycle-1 is rejected if presented in cycle-2.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- 2-cycle fixture byte-diff at the verdict-table region shows cycle-2 content.
- Cycle-2 spawn prompt does NOT contain cycle-1's verdict.
- Orchestrator logs the re-extract step at every fix-cycle boundary.
- Evidence at `TASKLIST_ROOT/artifacts/D-0030/evidence.md`.

**Validation:**
- Manual check: reviewer confirms re-extract happens per cycle.
- Evidence: byte-diff output.

**Dependencies:** T03.03
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.06 -- Checkpoint: Phase 3 / Tasks T03.01-T03.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049, R-050, R-051, R-052, R-053, R-054, R-055, R-056 |
| Why | Gate: verify FR-CONV.3 wrapper, DM-002-M3 implementation, API-002-M3 injection, Self-Audit schema, and INV-002 freshness before proceeding to enumeration + anti-inflation tasks. |
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
| Deliverable IDs | D-CP03-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md`

**Purpose:** Mid-phase gate verifying FR-CONV.3 spawn-prompt injection, DM-002-M3 implementation, Self-Audit schema, and INV-002 freshness rule are operational.

**Verification:**
- FR-CONV.3 wrapper landed (D-0026 evidence).
- DM-002-M3 byte-exact verdict-table copy in spawn prompts (D-0027 + D-0028 evidence).
- INV-002 2-cycle fixture passes (D-0030 evidence).

**Exit Criteria:**
- All 5 regular tasks T03.01-T03.05 report PASS.
- Spawn-prompt grep returns `Inherited Structural Verdict` block.
- Cycle-2 spawn carries cycle-2 verdict (no stale cycle-1 content).

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T03.01-T03.05.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.01..T03.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T03.07 -- Wire INV-010 dynamic checklist enumeration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-057 |
| Why | Injected verdict table row count enumerates over TB-Add catalogue at runtime (auto-picks up FR-CONV.1 additions); structural diff before/after FR-CONV.1 landing shows enrichment. |
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
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0031/spec.md`
- `TASKLIST_ROOT/artifacts/D-0031/evidence.md`

**Deliverables:**
- Dynamic enumeration logic referencing TB-Add catalogue.
- Auto-richens checklist when catalogue grows.
- Structural diff demonstrating enrichment.

**Steps:**
1. **[PLANNING]** Read R-057 enumeration spec.
2. **[PLANNING]** Locate TB-Add catalogue source in rf-qa.md from Phase 1.
3. **[EXECUTION]** Implement enumeration loop pulling TB-Add IDs from catalogue.
4. **[VERIFICATION]** Add a synthetic TB-Add-9 stub; assert checklist auto-richens to include it.
5. **[VERIFICATION]** Diff checklist before/after catalogue growth; assert enrichment.
6. **[COMPLETION]** Evidence; remove synthetic stub after verification.

**Acceptance Criteria:**
- Structural diff of checklist before/after TB-Add catalogue growth shows new entries.
- Adding a synthetic TB-Add-9 stub causes the checklist to auto-richen without code changes.
- Evidence at `TASKLIST_ROOT/artifacts/D-0031/evidence.md`.
- TB-Add catalogue lookup is dynamic (no hard-coded list of TB-Add IDs in enumeration logic).

**Validation:**
- Manual check: reviewer confirms enumeration is dynamic.
- Evidence: before/after diff.

**Dependencies:** T03.03; TB-Add catalogue (M1)
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.08 -- Preserve anti-inflation block + wire failure-mode halt

| Field | Value |
|---|---|
| Roadmap Item IDs | R-059, R-060 |
| Why | rf-qa-qualitative.md:766-775 Prohibited Behaviors block (anti-inflation bullet at :770) MUST NOT be weakened/removed/rephrased; if rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at §A.10 before §A.10.5. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0032/spec.md`
- `TASKLIST_ROOT/artifacts/D-0032/evidence.md`

**Deliverables:**
- rf-qa-qualitative.md:766-775 Prohibited Behaviors block byte-identical pre/post.
- Failure-mode halt: missing verdict triggers gate halt at §A.10 before §A.10.5.
- Sub-agent verification confirms anti-inflation rule operational.

**Steps:**
1. **[PLANNING]** Capture byte hash of rf-qa-qualitative.md:766-775 pre-edit.
2. **[PLANNING]** Read R-059, R-060 specs.
3. **[EXECUTION]** Confirm no edits land within :766-775 range.
4. **[EXECUTION]** Wire failure-mode halt in SKILL.md §A.10.
5. **[VERIFICATION]** Byte-diff Prohibited Behaviors block pre/post; assert zero diff.
6. **[VERIFICATION]** Run missing-verdict fixture; assert rf-qa-qualitative does NOT spawn and gate halts.

**Acceptance Criteria:**
- Byte-diff of rf-qa-qualitative.md:766-775 pre/post MIG-003 is zero.
- Missing-verdict fixture produces gate halt at §A.10 before §A.10.5; rf-qa-qualitative is NOT spawned.
- Sub-agent quality-engineer report confirms K-003 audit operational compliance criteria still measurable.
- Evidence at `TASKLIST_ROOT/artifacts/D-0032/evidence.md`.

**Validation:**
- Manual check: reviewer confirms the block is verbatim unchanged.
- Evidence: sub-agent report + byte-diff log.

**Dependencies:** T03.04
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.09 -- Edit COMP-001-M3 SKILL.md A.10.5 spawn injection (923-1000)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-061 |
| Why | Inject `## Inherited Structural Verdict` block into SKILL.md A.10.5 spawn prompt at ~:966 (after TARGET FILES, before INSTRUCTIONS). |
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
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0033/spec.md`
- `TASKLIST_ROOT/artifacts/D-0033/evidence.md`

**Deliverables:**
- Inherited Structural Verdict block inserted at SKILL.md A.10.5 around line 966.
- Injection point verified.
- Grep evidence.

**Steps:**
1. **[PLANNING]** Read R-061 edit constraints (range 923-1000, target ~966).
2. **[EXECUTION]** Locate insertion site in SKILL.md A.10.5.
3. **[EXECUTION]** Insert the block.
4. **[VERIFICATION]** `grep -n "Inherited Structural Verdict" src/superclaude/skills/task-builder/SKILL.md`; assert line within 923-1000.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "Inherited Structural Verdict" src/superclaude/skills/task-builder/SKILL.md` returns at least 1 match with line N in [923, 1000].
- Injection sits after TARGET FILES and before INSTRUCTIONS in the spawn prompt.
- Evidence at `TASKLIST_ROOT/artifacts/D-0033/evidence.md`.
- No other content in SKILL.md:923-1000 outside the new block is modified.

**Validation:**
- Manual check: reviewer confirms position relative to TARGET FILES / INSTRUCTIONS.
- Evidence: grep output.

**Dependencies:** T03.03
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.10 -- Edit COMP-004-M3 rf-qa-qualitative EOF append (line 794)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-062 |
| Why | Append "Handling the Inherited Structural Verdict" section + add `## Self-Audit` to output schema at rf-qa-qualitative.md:794. |
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
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0034/spec.md`
- `TASKLIST_ROOT/artifacts/D-0034/evidence.md`

**Deliverables:**
- "Handling the Inherited Structural Verdict" section appended at rf-qa-qualitative.md:794.
- `## Self-Audit` added to output schema.
- Anti-inflation block at :766-775 byte-identical.

**Steps:**
1. **[PLANNING]** Confirm T03.08 anti-inflation preservation captured baseline.
2. **[PLANNING]** Read R-062 edit constraints.
3. **[EXECUTION]** Append the new section + Self-Audit at line 794.
4. **[VERIFICATION]** `grep -n "Self-Audit" src/superclaude/agents/rf-qa-qualitative.md`; assert match at EOF range.
5. **[VERIFICATION]** Byte-diff :766-775 region pre/post; assert zero diff.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "## Self-Audit" src/superclaude/agents/rf-qa-qualitative.md` returns match at or after line 794.
- Byte-diff of rf-qa-qualitative.md:766-775 region pre/post is zero.
- New section heading is "Handling the Inherited Structural Verdict".
- Evidence at `TASKLIST_ROOT/artifacts/D-0034/evidence.md`.

**Validation:**
- Manual check: reviewer confirms anti-inflation block untouched.
- Evidence: byte-diff + grep.

**Dependencies:** T03.08
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.11 -- Commit TEST-007 inherited verdict present fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-063 |
| Why | Fixture asserting `## Inherited Structural Verdict` block appears in rf-qa-qualitative spawn prompt. |
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
| Deliverable IDs | D-0035 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0035/evidence.md`

**Deliverables:**
- TEST-007 fixture committed.
- Grep-on-spawn-log assertion green.

**Steps:**
1. **[PLANNING]** Read R-063 fixture spec.
2. **[EXECUTION]** Author `tests/audit/test_inherited_verdict_present.py`.
3. **[EXECUTION]** Add assertion checking spawn-log for the block header.
4. **[VERIFICATION]** Run the fixture; assert green.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_inherited_verdict_present.py -v` exits 0.
- Fixture's assertion matches the block header verbatim.
- Evidence at `TASKLIST_ROOT/artifacts/D-0035/evidence.md`.
- TEST-007 listed in `TASKLIST_ROOT/artifacts/D-0035/evidence.md` with the pytest log path.

**Validation:**
- Manual check: reviewer confirms fixture exercises live spawn-log path.
- Evidence: pytest log.

**Dependencies:** T03.09
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.12 -- Checkpoint: Phase 3 / Tasks T03.07-T03.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-057, R-058, R-059, R-060, R-061, R-062, R-063 |
| Why | Gate: verify INV-010 enumeration, anti-inflation preservation, SKILL.md + rf-qa-qualitative.md edits, and TEST-007 fixture before remaining fixtures + migration. |
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
| Deliverable IDs | D-CP03-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-T07-T11.md`

**Purpose:** Mid-phase gate verifying enumeration + preservation + edit-site work lands cleanly before TEST fixtures + migration.

**Verification:**
- INV-010 enumeration auto-richens when catalogue grows (D-0031 evidence).
- Anti-inflation block byte-diff zero pre/post (D-0032 + D-0034 evidence).
- TEST-007 fixture green (D-0035 evidence).

**Exit Criteria:**
- All 5 regular tasks T03.07-T03.11 report PASS.
- SKILL.md A.10.5 contains the Inherited Structural Verdict block in range 923-1000.
- rf-qa-qualitative.md has Self-Audit at or after line 794.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T03.07-T03.11.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.07..T03.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T03.13 -- Commit TEST-008 freshness INV-002 2-cycle fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064 |
| Why | 2-cycle fixture asserting cycle-2 spawn carries cycle-2 verdict, not stale cycle-1; byte-diff cycle-1 vs cycle-2 spawn prompts. |
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
| Deliverable IDs | D-0036 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0036/evidence.md`

**Deliverables:**
- TEST-008 fixture committed.
- Cycle-2 spawn carries cycle-2 verdict; byte-diff at table region demonstrates difference.

**Steps:**
1. **[PLANNING]** Read R-064 fixture spec.
2. **[EXECUTION]** Author `tests/audit/test_inherited_verdict_freshness_inv_002.py` running 2 cycles.
3. **[EXECUTION]** Compare table region byte-diff.
4. **[VERIFICATION]** Assert cycle-2 prompt contains cycle-2 verdict.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_inherited_verdict_freshness_inv_002.py -v` exits 0.
- 2-cycle byte-diff shows cycle-2 verdict in cycle-2 spawn prompt.
- Stale cycle-1 verdict NOT present in cycle-2 spawn.
- Evidence at `TASKLIST_ROOT/artifacts/D-0036/evidence.md`.

**Validation:**
- Manual check: reviewer confirms 2-cycle fixture exercises real spawn boundary.
- Evidence: pytest log + byte-diff output.

**Dependencies:** T03.05; T03.12
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.14 -- Commit TEST-009 self-audit INV-019 fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-065 |
| Why | Fixture asserting rf-qa-qualitative output contains `## Self-Audit` with ≥1 documented semantic check beyond inherited verdict. |
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
| Deliverable IDs | D-0037 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0037/evidence.md`

**Deliverables:**
- TEST-009 fixture committed asserting Self-Audit + ≥1 semantic check.
- Content inspection finding ≥1 independent check.

**Steps:**
1. **[PLANNING]** Read R-065 fixture spec.
2. **[EXECUTION]** Author `tests/audit/test_self_audit_inv_019.py`.
3. **[EXECUTION]** Add content inspection asserting ≥1 semantic check.
4. **[VERIFICATION]** Run fixture; assert green.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_self_audit_inv_019.py -v` exits 0.
- Fixture verifies ≥1 documented semantic check is present.
- Evidence at `TASKLIST_ROOT/artifacts/D-0037/evidence.md`.
- A fixture variant with 0 semantic checks fails (verifies negative case).

**Validation:**
- Manual check: reviewer confirms negative-case variant fails.
- Evidence: pytest log.

**Dependencies:** T03.04; T03.10
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.15 -- Commit TEST-010 dynamic enumeration INV-010 fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-066 |
| Why | Fixture asserting checklist auto-richens when FR-CONV.1 catalogue grows; structural diff before/after catalogue growth shows enrichment. |
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
| Deliverable IDs | D-0038 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0038/evidence.md`

**Deliverables:**
- TEST-010 fixture committed.
- Structural diff demonstrating enrichment when catalogue grows.

**Steps:**
1. **[PLANNING]** Read R-066 fixture spec.
2. **[EXECUTION]** Author `tests/audit/test_dynamic_enumeration_inv_010.py`.
3. **[EXECUTION]** Add synthetic TB-Add stub then assert checklist auto-richens.
4. **[VERIFICATION]** Run fixture; assert green.
5. **[COMPLETION]** Evidence; remove synthetic stub.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_dynamic_enumeration_inv_010.py -v` exits 0.
- Structural diff before/after catalogue growth shows new entry.
- Synthetic stub removed after fixture run.
- Evidence at `TASKLIST_ROOT/artifacts/D-0038/evidence.md`.

**Validation:**
- Manual check: reviewer confirms enumeration is dynamic.
- Evidence: pytest log + diff output.

**Dependencies:** T03.07
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.16 -- Execute MIG-003 PR-04 landing migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-067, R-068 |
| Why | Strictly-additive passthrough single-commit landing FR-CONV.3; FF_INHERITED_STRUCTURAL_VERDICT governance; rollback disables passthrough flag with fallback to independent structural re-checking. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | migration, scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0039 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0039/spec.md`
- `TASKLIST_ROOT/artifacts/D-0039/evidence.md`

**Deliverables:**
- MIG-003 single commit landing FR-CONV.3.
- `make verify-sync` PASS.
- FF_INHERITED_STRUCTURAL_VERDICT governance entry cross-referenced to M7.

**Steps:**
1. **[PLANNING]** Confirm T03.13..T03.15 fixtures green.
2. **[PLANNING]** Run `make verify-sync` clean baseline.
3. **[EXECUTION]** Stage all SKILL.md (A.10.5 injection) + rf-qa-qualitative.md (Self-Audit append) edits.
4. **[EXECUTION]** Author commit message documenting per-line revert via passthrough-flag disable.
5. **[VERIFICATION]** Run `make verify-sync` post-commit; assert PASS.
6. **[COMPLETION]** Spawn quality-engineer sub-agent for diff spot-check.

**Acceptance Criteria:**
- `make verify-sync` exits 0 immediately after MIG-003 commit.
- Commit body documents passthrough-flag disable as rollback path.
- Sub-agent report confirms strictly-additive change with rf-qa-qualitative.md:766-775 byte-identical.
- FF_INHERITED_STRUCTURAL_VERDICT entry recorded at `TASKLIST_ROOT/artifacts/D-0039/spec.md`.

**Validation:**
- Manual check: reviewer confirms anti-inflation block byte-stable.
- Evidence: `make verify-sync` log + commit diff + sub-agent report.

**Dependencies:** T03.13, T03.14, T03.15
**Rollback:** As stated in roadmap (disable passthrough flag; fall back to current behavior)
**Notes:** Critical-path override applied because MIG-003 is the M3 landing gate.

### T03.17 -- Document K-007 sequencing-inversion contingency

| Field | Value |
|---|---|
| Roadmap Item IDs | R-069 |
| Why | Sequencing rule PR-06 → PR-04 enforced in release-spec §4.6; INV-010 dynamic-enumeration auto-richens when catalogue activates; re-merge in correct order on inversion detection. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0040/spec.md`
- `TASKLIST_ROOT/artifacts/D-0040/evidence.md`

**Deliverables:**
- Sequencing contingency note documented.
- INV-010 mitigation path cited.
- Inversion-detection re-merge procedure documented.

**Steps:**
1. **[PLANNING]** Read R-069 contingency spec.
2. **[EXECUTION]** Author K-007 mitigation note at `TASKLIST_ROOT/artifacts/D-0040/spec.md`.
3. **[EXECUTION]** Cite INV-010 dynamic-enumeration as auto-richening mitigation.
4. **[VERIFICATION]** Reviewer confirms procedure references release-spec §4.6.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0040/spec.md` exists and documents the K-007 contingency.
- Sequencing rule PR-06 → PR-04 explicitly named in the note.
- INV-010 mitigation cited.
- `grep -n "PR-06 → PR-04" <release-spec>` returns a match within §4.6, confirming sequencing rule is enforced (not merely documented in artifact note).
- Re-merge procedure described step-by-step.

**Validation:**
- Manual check: reviewer confirms release-spec §4.6 cross-reference.
- Evidence: linkable spec.

**Dependencies:** T03.16
**Rollback:** As stated in roadmap
**Notes:** None.

### T03.18 -- Checkpoint: End of Phase 3

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049, R-050, R-051, R-052, R-053, R-054, R-055, R-056, R-057, R-058, R-059, R-060, R-061, R-062, R-063, R-064, R-065, R-066, R-067, R-068, R-069 |
| Why | Gate: verify all M3 deliverables (Inherited Verdict + Self-Audit, INV-002 freshness, INV-010 enumeration, INV-019 obligation, anti-inflation preservation, MIG-003 landing, K-007 contingency) before unblocking M4. |
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

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`

**Purpose:** End-of-Phase-3 gate confirming Inherited Structural Verdict + Self-Audit live, all four INV-* invariants enforced, anti-inflation block byte-stable, MIG-003 merged.

**Verification:**
- Spawn prompt carries verdict table byte-for-byte (D-0027 + D-0028 + D-0035 evidence).
- Self-Audit + INV-019 obligation in rf-qa-qualitative output (D-0029 + D-0037 evidence).
- MIG-003 merged with `make verify-sync` PASS (D-0039 evidence).

**Exit Criteria:**
- All 15 regular tasks T03.01-T03.17 (skipping mid-checkpoints) report PASS.
- M3 Exit Conditions per roadmap (spawn prompt verbatim, fix-cycle re-injection, Self-Audit with ≥1 semantic check, anti-inflation byte-identical) all met.
- K-007 contingency documented.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Inspect M3 Exit Conditions checklist; assert every item is satisfied.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above with `Overall: Pass`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T03.01-T03.17 it covers.

**Validation:**
- Manual check: reviewer confirms the report declares M3 PASS and unblocks M4.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.01..T03.17
**Rollback:** N/A (checkpoints are read-only verifications)
