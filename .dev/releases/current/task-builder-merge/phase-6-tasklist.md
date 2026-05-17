# Phase 6 -- M6 Synthetic DNSP on Partition Exhaust

**Phase Goal:** After a partition agent's escalation ladder exhausts (rf-analyst, rf-qa, or rf-qa-qualitative partition instance), emit synthetic HIGH-severity finding with `source: "synthetic-dnsp"` to agent's output stream rather than silently aborting; preserve all-agents-fail guard (zero partitions succeeded → no synthetic, existing rf-team-lead.md:417 escalation runs); preserve zero-trust QA + evidence-bound-item + parallel-research invariants. Duration: 2 weeks (2026-07-24 → 2026-08-07). Exit: when ≥1 partition succeeded AND ≥1 exhausted, synthetic-dnsp HIGH finding emitted with all 5 fixed fields + dedup_key + found_n_times; identical dedup_keys collapse with `found N times`; zero-partitions-succeeded → NO synthetic emits and existing escalation runs; N-1 partitions complete concurrently (INV-021).

### T06.01 -- Land FR-CONV.6 synthetic-dnsp wrapper

| Field | Value |
|---|---|
| Roadmap Item IDs | R-111 |
| Why | After partition agent's escalation ladder exhausts, emit synthetic HIGH-severity finding (CASE-B PR-03 BASE); preserve all-agents-fail guard. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0068 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0068/spec.md`
- `TASKLIST_ROOT/artifacts/D-0068/evidence.md`

**Deliverables:**
- FR-CONV.6 wrapper landed in SKILL.md + rf-analyst.md + rf-qa.md + rf-qa-qualitative.md.
- All-agents-fail guard preserved (zero-partitions-succeeded → no synthetic).
- INV-021 N-1 partitions concurrent invariant wired.

**Steps:**
1. **[PLANNING]** Confirm M5 PASS; API-004 halt-signal contract live for dedup_key composition.
2. **[PLANNING]** Read R-111 wrapper spec.
3. **[EXECUTION]** Insert FR-CONV.6 wrapper at the 4 modified files.
4. **[VERIFICATION]** Spawn quality-engineer sub-agent to validate all-agents-fail guard preserved.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -c "synthetic-dnsp" src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa-qualitative.md` returns at least 3 (≥1 per file).
- `grep -c "synthetic-dnsp" src/superclaude/skills/task-builder/SKILL.md` returns at least 1 (detailed merge-step verification deferred to T06.11).
- Sub-agent confirms zero-partitions-succeeded path activates rf-team-lead.md:417 (no synthetic).
- INV-021 N-1 concurrency wired.
- Evidence at `TASKLIST_ROOT/artifacts/D-0068/evidence.md`.

**Validation:**
- Manual check: reviewer confirms wrapper preserves all-agents-fail guard.
- Evidence: sub-agent report.

**Dependencies:** Phase 5 (M5 PASS); API-004
**Rollback:** As stated in roadmap (remove DNSP edit sites; all-agents-fail escalation remains)
**Notes:** None.

### T06.02 -- Implement DM-003-M6 7-field schema

| Field | Value |
|---|---|
| Roadmap Item IDs | R-112 |
| Why | Implement DM-003 entity per M1 contract-freeze with 7 fields (severity HIGH-fixed; source synthetic-dnsp-fixed sentinel; affected_range verbatim assigned_files slice; evidence never blank spawn-log or stub; recommendation fixed Manual review required; dedup_key tuple; found_n_times int default 1). |
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
| Deliverable IDs | D-0069 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0069/spec.md`
- `TASKLIST_ROOT/artifacts/D-0069/evidence.md`

**Deliverables:**
- DM-003 entity implementation with all 7 fields populated.
- Diff vs M1 contract-freeze byte-for-byte.

**Steps:**
1. **[PLANNING]** Confirm DM-003 contract-freeze (T01.13).
2. **[PLANNING]** Read R-112 field specs.
3. **[EXECUTION]** Implement all 7 fields per the frozen contract.
4. **[VERIFICATION]** Sub-agent confirms 7-field match against DM-003 baseline.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- DM-003 emission has all 7 fields: severity (HIGH), source (synthetic-dnsp), affected_range, evidence, recommendation, dedup_key, found_n_times.
- Sub-agent quality-engineer report confirms field-for-field match against M1 contract-freeze.
- Diff vs DM-003 spec is byte-identical on fixed-value fields.
- Evidence at `TASKLIST_ROOT/artifacts/D-0069/evidence.md`.

**Validation:**
- Manual check: reviewer confirms 7 fields present.
- Evidence: sub-agent report.

**Dependencies:** T06.01; T01.13
**Rollback:** As stated in roadmap
**Notes:** Critical-path override applied because DM-003 wire shape governs INV-012 composition with FR-CONV.5.

### T06.03 -- Implement DM-003.severity + DM-003.source fixed-field emitters

| Field | Value |
|---|---|
| Roadmap Item IDs | R-113, R-114 |
| Why | severity field — fixed HIGH non-overridable; source field — fixed `synthetic-dnsp` literal sentinel for operator inspection. |
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
| Deliverable IDs | D-0070 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0070/spec.md`
- `TASKLIST_ROOT/artifacts/D-0070/evidence.md`

**Deliverables:**
- severity emitter producing HIGH non-overridable.
- source emitter producing `synthetic-dnsp` literal sentinel.

**Steps:**
1. **[PLANNING]** Read R-113, R-114 specs.
2. **[EXECUTION]** Implement severity HIGH emitter.
3. **[EXECUTION]** Implement source `synthetic-dnsp` sentinel emitter.
4. **[VERIFICATION]** Emission with severity != HIGH is rejected as invalid.
5. **[VERIFICATION]** Grep `synthetic-dnsp` returns ≥1 hit per file.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -c "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns at least 1 hit per file.
- Synthetic emission with severity != HIGH is rejected by the emitter.
- source field is the literal string `synthetic-dnsp`.
- Evidence at `TASKLIST_ROOT/artifacts/D-0070/evidence.md`.

**Validation:**
- Manual check: reviewer confirms HIGH non-overridable.
- Evidence: emitter rejection log + grep.

**Dependencies:** T06.02
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.04 -- Implement DM-003.affected_range + DM-003.evidence emitters

| Field | Value |
|---|---|
| Roadmap Item IDs | R-115, R-116 |
| Why | affected_range — verbatim copy of partition's assigned_files slice as received in spawn prompt; evidence — spawn-log path or stub citing log absence (never blank). |
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
| Deliverable IDs | D-0071 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0071/spec.md`
- `TASKLIST_ROOT/artifacts/D-0071/evidence.md`

**Deliverables:**
- affected_range emitter copying assigned_files byte-for-byte.
- evidence emitter producing spawn-log path or stub.

**Steps:**
1. **[PLANNING]** Read R-115, R-116 specs.
2. **[EXECUTION]** Implement affected_range emitter.
3. **[EXECUTION]** Implement evidence emitter with canonical path `${TASK_DIR}qa/spawn-log-agent_role-partition_id.txt` or stub.
4. **[VERIFICATION]** Run exhausted-partition fixture; assert affected_range = spawn-prompt assigned_files byte-for-byte.
5. **[VERIFICATION]** evidence field NEVER blank in emissions.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Exhausted-partition fixture's affected_range field byte-matches the spawn-prompt assigned_files slice.
- evidence field is never empty across the test corpus.
- Canonical evidence path format used: `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`.
- Evidence at `TASKLIST_ROOT/artifacts/D-0071/evidence.md`.

**Validation:**
- Manual check: reviewer confirms evidence stub explicitly cites log absence when missing.
- Evidence: emitter log.

**Dependencies:** T06.03
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.05 -- Implement recommendation + dedup_key + found_n_times emitters

| Field | Value |
|---|---|
| Roadmap Item IDs | R-117, R-118, R-119 |
| Why | recommendation field — fixed string `Manual review required — partition agent failed twice`. dedup_key — 2-tuple `(assigned_files_range, escalation_ladder_exhaust_point)` emitted as YAML list. found_n_times — collision counter default 1, increments by 1 on each within-cycle dedup collapse. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0072 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0072/spec.md`
- `TASKLIST_ROOT/artifacts/D-0072/evidence.md`

**Deliverables:**
- recommendation emitter producing byte-exact fixed string.
- dedup_key emitter producing YAML list `["<range>", "<exhaust_point>"]`.
- found_n_times counter with default 1 and increment-on-collapse logic.

**Steps:**
1. **[PLANNING]** Read R-117, R-118, R-119 specs.
2. **[EXECUTION]** Implement recommendation emitter.
3. **[EXECUTION]** Implement dedup_key as 2-tuple YAML list.
4. **[EXECUTION]** Implement found_n_times counter with default 1.
5. **[VERIFICATION]** Two-identical-dedup_key fixture: collapse to one record with found_n_times=2.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- recommendation field is the literal string `Manual review required — partition agent failed twice` byte-exact.
- dedup_key emitted as YAML list `["<range>", "<exhaust_point>"]`.
- Emitter rejects synthesis with exhaust_point outside `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`.
- Two-identical-dedup_key fixture collapses to cardinality 1 with found_n_times=2.
- Evidence at `TASKLIST_ROOT/artifacts/D-0072/evidence.md`.

**Validation:**
- Manual check: reviewer confirms YAML list format.
- Evidence: fixture log.

**Dependencies:** T06.04
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.06 -- Checkpoint: Phase 6 / Tasks T06.01-T06.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-111, R-112, R-113, R-114, R-115, R-116, R-117, R-118, R-119 |
| Why | Gate: verify FR-CONV.6 wrapper, DM-003-M6 7-field schema, and the 7 sub-field emitters before partition-API + vocabulary work. |
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
| Deliverable IDs | D-CP06-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-T01-T05.md`

**Purpose:** Mid-phase gate after wrapper + 7-field schema + sub-field emitters land.

**Verification:**
- 7-field DM-003 schema implemented (D-0069 evidence).
- All 7 fixed/dynamic emitters operational (D-0070..D-0072 evidence).
- All-agents-fail guard preserved (D-0068 evidence).

**Exit Criteria:**
- All 5 regular tasks T06.01-T06.05 report PASS.
- severity HIGH non-overridable.
- found_n_times collapse fixture passes with cardinality=1 + found_n_times=2.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P06-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T06.01-T06.05.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T06.01..T06.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T06.07 -- Implement API-003-M6 + exhaust-point vocabulary

| Field | Value |
|---|---|
| Roadmap Item IDs | R-120, R-121 |
| Why | Implement partition emission of structured block in normal output stream (no separate channel); consumed by SKILL.md §A.8 + §A.10 merge step. Closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` — free-form descriptions forbidden. |
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
| Deliverable IDs | D-0073 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0073/spec.md`
- `TASKLIST_ROOT/artifacts/D-0073/evidence.md`

**Deliverables:**
- API-003 implementation with structured-block emission in normal output stream.
- Closed vocabulary for escalation_ladder_exhaust_point.
- Non-vocabulary values rejected.

**Steps:**
1. **[PLANNING]** Read R-120, R-121 specs.
2. **[EXECUTION]** Implement structured-block emission in partition output stream.
3. **[EXECUTION]** Document closed vocabulary and reject non-vocabulary values.
4. **[VERIFICATION]** Sub-agent confirms merge step at SKILL.md A.8 + A.10 picks up the block.
5. **[VERIFICATION]** Non-vocabulary exhaust_point value is rejected.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -E "retry-1|retry-2|gap-fill-round" src/superclaude/agents/rf-qa.md` returns vocabulary entries.
- Non-vocabulary exhaust_point value triggers an error in the emitter.
- Sub-agent report confirms merge step wired at SKILL.md A.8 + A.10.
- Evidence at `TASKLIST_ROOT/artifacts/D-0073/evidence.md`.

**Validation:**
- Manual check: reviewer confirms vocabulary is closed.
- Evidence: sub-agent report.

**Dependencies:** T06.06
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.08 -- Wire all-agents-fail guard precedence

| Field | Value |
|---|---|
| Roadmap Item IDs | R-122 |
| Why | Zero-partitions-succeeded → NO synthetic emits; mutually exclusive paths: ≥1 success AND ≥1 exhaust → emit; zero success → activate rf-team-lead.md:417. |
| Effort | S |
| Risk | High |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0074 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0074/spec.md`
- `TASKLIST_ROOT/artifacts/D-0074/evidence.md`

**Deliverables:**
- Zero-partitions-succeeded path activates rf-team-lead.md:417 (no synthetic).
- ≥1 success path emits synthetic-dnsp.
- Mutually-exclusive paths documented.

**Steps:**
1. **[PLANNING]** Read R-122 mutual-exclusivity spec.
2. **[EXECUTION]** Wire pre-emission guard in orchestrator.
3. **[EXECUTION]** Confirm rf-team-lead.md:417 path activates on zero-success.
4. **[VERIFICATION]** Zero-partitions fixture: no synthetic block, escalation path activates.
5. **[VERIFICATION]** Mixed-success fixture: synthetic emitted alongside real findings.
6. **[COMPLETION]** Sub-agent report.

**Acceptance Criteria:**
- Zero-partitions-succeeded fixture's execution log shows rf-team-lead.md:417 activation and no synthetic block.
- Mixed-success fixture's output stream contains synthetic-dnsp emission.
- Sub-agent quality-engineer report confirms mutually-exclusive paths preserved.
- Evidence at `TASKLIST_ROOT/artifacts/D-0074/evidence.md`.

**Validation:**
- Manual check: reviewer confirms mutual exclusivity.
- Evidence: sub-agent report + fixture logs.

**Dependencies:** T06.07
**Rollback:** As stated in roadmap
**Notes:** Critical-path override applied because the all-agents-fail guard governs escalation safety.

### T06.09 -- Wire within-cycle + cross-cycle dedup behavior (INV-012)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-123, R-124 |
| Why | Within-cycle identical-dedup_key collapse to one record with found_n_times incremented. Cross-cycle identical dedup_key is dedup case, NOT regression — prior verdict was already FAIL. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STANDARD |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None; Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0075 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0075/spec.md`
- `TASKLIST_ROOT/artifacts/D-0075/evidence.md`

**Deliverables:**
- Within-cycle collapse logic wired.
- Cross-cycle non-regression composition wired (INV-012).
- Contributes 1 (not 2) to F_n+1 on cross-cycle same dedup_key.

**Steps:**
1. **[PLANNING]** Read R-123, R-124 specs.
2. **[EXECUTION]** Implement within-cycle collapse incrementing found_n_times.
3. **[EXECUTION]** Implement cross-cycle dedup composition referencing INV-012 (T05.07).
4. **[VERIFICATION]** Within-cycle fixture: 2 identical dedup_keys collapse to 1 + found_n_times=2.
5. **[VERIFICATION]** Cross-cycle fixture: same dedup_key in cycles N + N+1 contributes 1, not 2.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Within-cycle fixture cardinality is 1 with found_n_times=2.
- Cross-cycle same-dedup_key contributes 1 to `F_n+1`, not 2.
- No regression halt emitted for cross-cycle case (trips monotonicity, intended).
- Evidence at `TASKLIST_ROOT/artifacts/D-0075/evidence.md`.

**Validation:**
- Manual check: reviewer confirms INV-012 composition is consistent across M5+M6.
- Evidence: fixture log.

**Dependencies:** T06.08; INV-012 (T05.07)
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.10 -- Wire INV-021 N-1 concurrency + HIGH severity non-overridable

| Field | Value |
|---|---|
| Roadmap Item IDs | R-125, R-126 |
| Why | INV-021: on one partition's escalation exhaust, N-1 sibling partitions continue concurrently to completion before exhausted one synthesises finding. HIGH severity: synthetic findings emit ALONGSIDE (not in place of) real findings from successful partitions. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0076 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0076/spec.md`
- `TASKLIST_ROOT/artifacts/D-0076/evidence.md`

**Deliverables:**
- INV-021 N-1 concurrency invariant wired.
- HIGH severity non-overridable.
- Real findings preserved alongside synthetic.

**Steps:**
1. **[PLANNING]** Read R-125, R-126 specs.
2. **[EXECUTION]** Confirm N-1 partitions continue concurrently when one exhausts.
3. **[EXECUTION]** Confirm synthetic emits ALONGSIDE real findings.
4. **[VERIFICATION]** Spawn-log fixture: N-1 partitions overlap exhausted one's synthesis.
5. **[VERIFICATION]** Real findings preserved in output stream.
6. **[COMPLETION]** Sub-agent report.

**Acceptance Criteria:**
- Spawn-log timestamps prove N-1 partitions completed concurrently with exhausted one's synthesis.
- Real findings count unchanged when synthetic is added (synthetic adds to, doesn't replace).
- Sub-agent report confirms emission cardinality and parallel-research preservation.
- Evidence at `TASKLIST_ROOT/artifacts/D-0076/evidence.md`.

**Validation:**
- Manual check: reviewer confirms cohort never serialises.
- Evidence: spawn-log timestamps + sub-agent report.

**Dependencies:** T06.09
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.11 -- Edit COMP-001-M6 SKILL.md A.8 + A.10 merge step

| Field | Value |
|---|---|
| Roadmap Item IDs | R-127, R-128 |
| Why | Modify SKILL.md A.8 Research Quality Gate (572-656) and A.10 Task File Validation (870-918) to wire synthetic-dnsp merge step. |
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
| Deliverable IDs | D-0077 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0077/spec.md`
- `TASKLIST_ROOT/artifacts/D-0077/evidence.md`

**Deliverables:**
- COMP-001-M6 edit at SKILL.md A.8 (:572-656).
- COMP-001-M6-r18 edit at SKILL.md A.10 (:870-918).
- Merge step wired alongside real findings.

**Steps:**
1. **[PLANNING]** Read R-127, R-128 edit constraints.
2. **[EXECUTION]** Edit SKILL.md A.8 at :572-656 to wire merge step.
3. **[EXECUTION]** Edit SKILL.md A.10 at :870-918 similarly.
4. **[VERIFICATION]** Grep `synthetic-dnsp` in both ranges; assert merge step present.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "synthetic-dnsp" src/superclaude/skills/task-builder/SKILL.md` returns matches in both [572, 656] and [870, 918].
- Merge step picks up synthetic block alongside real findings.
- Evidence at `TASKLIST_ROOT/artifacts/D-0077/evidence.md`.
- Edits confined to named line ranges.

**Validation:**
- Manual check: reviewer confirms merge step wiring.
- Evidence: grep output.

**Dependencies:** T06.06
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.12 -- Checkpoint: Phase 6 / Tasks T06.07-T06.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-120, R-121, R-122, R-123, R-124, R-125, R-126, R-127, R-128 |
| Why | Gate: verify API-003 + vocabulary + all-agents-fail guard + dedup composition + INV-021 concurrency + SKILL.md merge step. |
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
| Deliverable IDs | D-CP06-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-T07-T11.md`

**Purpose:** Mid-phase gate after API-003 emission, vocabulary, guard logic, dedup composition, INV-021 concurrency, and SKILL.md merge step.

**Verification:**
- API-003 emission + closed vocabulary live (D-0073 evidence).
- All-agents-fail guard preserved (D-0074 evidence).
- INV-021 concurrency + INV-012 composition wired (D-0075 + D-0076 evidence).

**Exit Criteria:**
- All 5 regular tasks T06.07-T06.11 report PASS.
- Mixed-success fixture emits synthetic alongside real findings.
- N-1 partitions concurrent on spawn-log timestamps.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P06-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T06.07-T06.11.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T06.07..T06.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T06.13 -- Edit COMP-005-M6 + COMP-003-M6 rf-analyst + rf-qa DNSP edit sites

| Field | Value |
|---|---|
| Roadmap Item IDs | R-129, R-130 |
| Why | Modify rf-analyst.md:58-71 with DNSP emission logic; modify rf-qa.md:49-77 (primary at 70-77) with DNSP emission logic. |
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
| Deliverable IDs | D-0078 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0078/spec.md`
- `TASKLIST_ROOT/artifacts/D-0078/evidence.md`

**Deliverables:**
- COMP-005-M6 edit at rf-analyst.md:58-71.
- COMP-003-M6 edit at rf-qa.md:49-77 (primary :70-77).
- DNSP emission logic landed.

**Steps:**
1. **[PLANNING]** Read R-129, R-130 edit constraints.
2. **[EXECUTION]** Edit rf-analyst.md:58-71 with DNSP emission logic.
3. **[EXECUTION]** Edit rf-qa.md:70-77 with DNSP emission logic.
4. **[VERIFICATION]** Grep `synthetic-dnsp` in both files; assert hits.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md` returns at least 1 match in [58, 71].
- `grep -n "synthetic-dnsp" src/superclaude/agents/rf-qa.md` returns at least 1 match in [70, 77].
- Edits confined to named ranges.
- Evidence at `TASKLIST_ROOT/artifacts/D-0078/evidence.md`.

**Validation:**
- Manual check: reviewer confirms line ranges.
- Evidence: grep output.

**Dependencies:** T06.12
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.14 -- Edit COMP-004-M6 + verify COMP-006-M6 preservation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-131, R-132 |
| Why | COMP-004-M6: modify rf-qa-qualitative.md:70-80 with DNSP emission logic. COMP-006-M6: rf-team-lead.md line 417 MUST NOT be replaced/short-circuited; verified NO DRIFT 2026-05-14. |
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
| Deliverable IDs | D-0079 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0079/spec.md`
- `TASKLIST_ROOT/artifacts/D-0079/evidence.md`

**Deliverables:**
- COMP-004-M6 edit at rf-qa-qualitative.md:70-80.
- COMP-006-M6 byte-diff zero at rf-team-lead.md:417.
- All-agents-fail path activates on zero-success.

**Steps:**
1. **[PLANNING]** Capture byte hash of rf-team-lead.md:417.
2. **[PLANNING]** Read R-131, R-132 constraints.
3. **[EXECUTION]** Edit rf-qa-qualitative.md:70-80.
4. **[VERIFICATION]** Byte-diff rf-team-lead.md:417 pre/post; assert zero diff.
5. **[VERIFICATION]** Grep `synthetic-dnsp` in rf-qa-qualitative.md; assert hit.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "synthetic-dnsp" src/superclaude/agents/rf-qa-qualitative.md` returns at least 1 match in [70, 80].
- Byte-diff of rf-team-lead.md:417 pre/post is zero.
- All-agents-fail path activates rf-team-lead.md:417 on zero-success fixture.
- Evidence at `TASKLIST_ROOT/artifacts/D-0079/evidence.md`.

**Validation:**
- Manual check: reviewer confirms rf-team-lead.md:417 byte-stable.
- Evidence: byte-diff + grep.

**Dependencies:** T06.13
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.15 -- Commit TEST-018 + TEST-019 dnsp twice-exhaust + dedup-collapse fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-133, R-134 |
| Why | TEST-018: partition timing out twice emits synthetic-dnsp finding with all 5 fixed fields. TEST-019: two identical-dedup_key synthetic findings collapse into one record with found_n_times=2. |
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
| Deliverable IDs | D-0080 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0080/evidence.md`

**Deliverables:**
- TEST-018 twice-exhaust fixture.
- TEST-019 dedup-collapse fixture.

**Steps:**
1. **[PLANNING]** Read R-133, R-134 fixture specs.
2. **[EXECUTION]** Author both fixtures under `tests/audit/`.
3. **[VERIFICATION]** Run pytest; assert both green.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py -v` exits 0.
- TEST-018 asserts all 5 fixed fields populated; severity HIGH; source synthetic-dnsp.
- TEST-019 asserts cardinality=1 with found_n_times=2.
- Evidence at `TASKLIST_ROOT/artifacts/D-0080/evidence.md`.

**Validation:**
- Manual check: reviewer confirms fixture assertions.
- Evidence: pytest log.

**Dependencies:** T06.05, T06.09, T06.13, T06.14
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.16 -- Commit TEST-020 + TEST-021 all-agents-fail + cohort-concurrency fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-135, R-136 |
| Why | TEST-020: zero partitions succeeded → no synthetic emits; existing rf-team-lead.md:417 escalation activates. TEST-021: on one partition's escalation exhaust, N-1 sibling partitions continue concurrently (INV-021). |
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
| Deliverable IDs | D-0081 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0081/evidence.md`

**Deliverables:**
- TEST-020 all-agents-fail bypass fixture.
- TEST-021 cohort-concurrency fixture.

**Steps:**
1. **[PLANNING]** Read R-135, R-136 fixture specs.
2. **[EXECUTION]** Author both fixtures.
3. **[VERIFICATION]** Run pytest; assert both green.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py tests/audit/test_dnsp_does_not_serialize_cohort.py -v` exits 0.
- TEST-020 asserts no synthetic block emitted and rf-team-lead activation.
- TEST-021 asserts spawn-log timing shows N-1 partitions overlap with synthesis.
- Evidence at `TASKLIST_ROOT/artifacts/D-0081/evidence.md`.

**Validation:**
- Manual check: reviewer confirms TEST-020 verifies mutual exclusivity.
- Evidence: pytest log + spawn-log timestamps.

**Dependencies:** T06.08, T06.10, T06.15
**Rollback:** As stated in roadmap
**Notes:** None.

### T06.17 -- Execute MIG-006 + FF_SYNTHETIC governance + NFR-CONV.10

| Field | Value |
|---|---|
| Roadmap Item IDs | R-137, R-138, R-139 |
| Why | Strictly-additive emission logic single commit; revertable by removing DNSP edit sites; existing rf-team-lead.md:417 already handles zero-partitions-succeeded; FF_SYNTHETIC_DNSP_EMISSION governance; NFR-CONV.10 parallel-research invariant preserved. |
| Effort | M |
| Risk | High |
| Risk Drivers | migration |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0082 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0082/spec.md`
- `TASKLIST_ROOT/artifacts/D-0082/evidence.md`

**Deliverables:**
- MIG-006 single commit landing FR-CONV.6.
- `make verify-sync` PASS.
- FF_SYNTHETIC_DNSP_EMISSION + NFR-CONV.10 governance entries referenced for M7.

**Steps:**
1. **[PLANNING]** Confirm T06.15 + T06.16 fixtures green.
2. **[PLANNING]** Run `make verify-sync` clean baseline.
3. **[EXECUTION]** Stage all rf-analyst.md, rf-qa.md, rf-qa-qualitative.md, SKILL.md edits.
4. **[EXECUTION]** Commit with revert path documented (remove DNSP sites).
5. **[VERIFICATION]** Run `make verify-sync` post-commit; assert PASS.
6. **[COMPLETION]** Spawn quality-engineer sub-agent for diff spot-check.

**Acceptance Criteria:**
- `make verify-sync` exits 0 immediately after MIG-006 commit.
- Commit body documents revert path via DNSP-site removal.
- Sub-agent report confirms rf-team-lead.md:417 byte-identical and NFR-CONV.10 N-1 concurrency operational.
- FF_SYNTHETIC_DNSP_EMISSION + NFR-CONV.10 entries recorded at `TASKLIST_ROOT/artifacts/D-0082/spec.md`.

**Validation:**
- Manual check: reviewer confirms preservation invariants in commit body.
- Evidence: `make verify-sync` log + commit diff + sub-agent report.

**Dependencies:** T06.15, T06.16
**Rollback:** As stated in roadmap (revert DNSP sites; all-agents-fail escalation remains)
**Notes:** Critical-path override applied because MIG-006 is the M6 landing gate.

### T06.18 -- Checkpoint: End of Phase 6

| Field | Value |
|---|---|
| Roadmap Item IDs | R-111, R-112, R-113, R-114, R-115, R-116, R-117, R-118, R-119, R-120, R-121, R-122, R-123, R-124, R-125, R-126, R-127, R-128, R-129, R-130, R-131, R-132, R-133, R-134, R-135, R-136, R-137, R-138, R-139 |
| Why | Gate: verify all M6 deliverables (FR-CONV.6 emission, DM-003 schema + 7 fields, API-003 + vocabulary, all-agents-fail guard, dedup composition, INV-021 concurrency, edit sites, fixtures, MIG-006) before unblocking M7. |
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
| Deliverable IDs | D-CP06 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-END.md`

**Purpose:** End-of-Phase-6 gate confirming synthetic DNSP emission live with full 7-field schema, all-agents-fail guard preserved, INV-021 + NFR-CONV.10 concurrency intact, MIG-006 merged.

**Verification:**
- DM-003 7-field synthetic emission on twice-exhaust fixture (D-0069..D-0072 + D-0080 evidence).
- All-agents-fail guard activates rf-team-lead.md:417 with no synthetic (D-0074 + D-0081 evidence).
- N-1 partition concurrency proven by spawn-log timestamps (D-0076 + D-0081 evidence).

**Exit Criteria:**
- All 15 regular tasks T06.01-T06.17 (skipping mid-checkpoints) report PASS.
- M6 Exit Conditions per roadmap (all 5 fixed fields + dedup_key + found_n_times, HIGH non-overridable, all-agents-fail bypass preserved, N-1 concurrent, rf-team-lead.md:417 byte-stable) all met.
- MIG-006 `make verify-sync` PASS.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Inspect M6 Exit Conditions checklist; assert every item is satisfied.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above with `Overall: Pass`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P06-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T06.01-T06.17 it covers.

**Validation:**
- Manual check: reviewer confirms the report declares M6 PASS and unblocks M7.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T06.01..T06.17
**Rollback:** N/A (checkpoints are read-only verifications)
