# Phase 5 -- M5 Retry Monotonicity + Regression Halts

**Phase Goal:** Add two stop-conditions to EXISTING fix-cycle retry loops (no new loop or stage): monotonicity guard (HALT if `|F_{n+1}|>=|F_n|`) and regression detection (HALT if any item PASS at cycle N is FAIL at cycle N+1); regression precedence over monotonicity; preserve four independent retry counters; preserve existing 3-cycle hard cap at `rf-team-lead.md:417`. Duration: 2 weeks (2026-07-10 → 2026-07-24). Exit: regression flip emits verbatim message and exits BEFORE monotonicity check; non-shrink emits `[HALT-MONOTONICITY] |F|=<n>`; identical dedup-key synthetic findings across cycles do NOT trigger halt; legitimate slow-cycle correction NOT halted; X-003 slow-convergence threshold REJECTED; all 4 fixtures PASS.

### T05.01 -- Land FR-CONV.5 halt-guards wrapper

| Field | Value |
|---|---|
| Roadmap Item IDs | R-090 |
| Why | Add two stop-conditions to existing fix-cycle retry loops (CASE-D PR-02); regression > monotonicity precedence; preserve zero-trust QA invariant and four independent counters. |
| Effort | M |
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
| Deliverable IDs | D-0054 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0054/spec.md`
- `TASKLIST_ROOT/artifacts/D-0054/evidence.md`

**Deliverables:**
- FR-CONV.5 wrapper landed in SKILL.md + rf-task-builder.md + rf-qa.md.
- Two halt guards wired to existing fix-cycle loops.
- Regression > monotonicity precedence documented.

**Steps:**
1. **[PLANNING]** Confirm M4 PASS; FR-CONV.6 dedup-key wire-shape spec available (M6 mutual coupling).
2. **[PLANNING]** Read R-090 wrapper spec.
3. **[EXECUTION]** Wire monotonicity guard to existing loops.
4. **[EXECUTION]** Wire regression guard with precedence over monotonicity.
5. **[VERIFICATION]** Spawn quality-engineer sub-agent to confirm no new loops or stages introduced.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -c "HALT-MONOTONICITY\|Regression detected on Item" src/superclaude/skills/task-builder/SKILL.md` returns at least 2 distinct halt-message references.
- Sub-agent quality-engineer report confirms no new retry loops introduced.
- Four independent retry counters preserved.
- Evidence at `TASKLIST_ROOT/artifacts/D-0054/evidence.md`.

**Validation:**
- Manual check: reviewer confirms wrappers are additive on existing loops.
- Evidence: sub-agent report.

**Dependencies:** Phase 4 (M4 PASS); FR-CONV.6 dedup-key shape spec
**Rollback:** As stated in roadmap (disable guards individually; per-gate caps continue)
**Notes:** None.

### T05.02 -- Implement API-004-M5 fix-loop halt-signals contract

| Field | Value |
|---|---|
| Roadmap Item IDs | R-091 |
| Why | Implement halt-message strings as inter-loop wire ABI; ordering rule per cycle transition n→n+1 (regression first, monotonicity second, hard-cap third, proceed fourth). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0055 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0055/spec.md`
- `TASKLIST_ROOT/artifacts/D-0055/evidence.md`

**Deliverables:**
- API-004 implementation with byte-exact halt-message strings.
- 4-step ordering rule documented.
- F-set definition with dedup-key identity.

**Steps:**
1. **[PLANNING]** Confirm API-004 contract-freeze (T01.14).
2. **[PLANNING]** Read R-091 implementation spec.
3. **[EXECUTION]** Implement halt-message emitters with byte-exact strings.
4. **[EXECUTION]** Document the 4-step ordering rule.
5. **[VERIFICATION]** Sub-agent confirms wire-ABI matches API-004 frozen contract.
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep "HALT-MONOTONICITY" src/superclaude/skills/task-builder/SKILL.md` returns the byte-exact halt-message string.
- 4-step ordering rule documented: regression → monotonicity → hard-cap → proceed.
- F-set defined with dedup-key identity (cardinality post-dedup).
- Sub-agent report confirms wire-ABI byte-for-byte.

**Validation:**
- Manual check: reviewer confirms ordering rule in implementation.
- Evidence: sub-agent report.

**Dependencies:** T05.01; T01.14
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.03 -- Implement monotonicity halt-message emitter

| Field | Value |
|---|---|
| Roadmap Item IDs | R-092 |
| Why | Emit verbatim halt string `[HALT-MONOTONICITY] |F|=<n>` when `|F_{n+1}|>=|F_n|`; only consulted when `|F_n|> 0`. |
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
| Deliverable IDs | D-0056 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0056/spec.md`
- `TASKLIST_ROOT/artifacts/D-0056/evidence.md`

**Deliverables:**
- Monotonicity halt-message emitter wired.
- Emission gated on prior regression-check passing.
- Monotonicity check skipped when `|F_n|=0`.

**Steps:**
1. **[PLANNING]** Read R-092 emission spec.
2. **[EXECUTION]** Implement emitter producing `[HALT-MONOTONICITY] |F|=<n>` literal.
3. **[EXECUTION]** Add gating on prior regression-check and `|F_n|>0`.
4. **[VERIFICATION]** Run `|F|=5,5,5` fixture; assert halt at cycle 2 with byte-exact message.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `[HALT-MONOTONICITY] |F|=5` literal appears in halt log on `|F|=5,5,5` fixture.
- Cycle 3 NOT attempted.
- Monotonicity check skipped when `|F_n|=0`.
- Monotonicity emission verified gated on prior regression-check passing (test with regression flip on the same cycle confirms monotonicity NOT emitted).
- Evidence at `TASKLIST_ROOT/artifacts/D-0056/evidence.md`.

**Validation:**
- Manual check: reviewer confirms byte-exact halt string.
- Evidence: fixture log.

**Dependencies:** T05.02
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.04 -- Implement regression halt-message emitter

| Field | Value |
|---|---|
| Roadmap Item IDs | R-093 |
| Why | Emit verbatim string `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` when item flips PASS@N→FAIL@N+1. |
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
| Deliverable IDs | D-0057 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0057/spec.md`
- `TASKLIST_ROOT/artifacts/D-0057/evidence.md`

**Deliverables:**
- Regression-halt emitter producing byte-exact message.
- Emitted BEFORE monotonicity check (precedence rule honored).

**Steps:**
1. **[PLANNING]** Read R-093 emission spec.
2. **[EXECUTION]** Implement regression detector comparing per-item PASS@N vs FAIL@N+1.
3. **[EXECUTION]** Emit byte-exact message; exit BEFORE monotonicity.
4. **[VERIFICATION]** Run PASS@1 / FAIL@2 fixture; assert regression message emitted ahead of monotonicity.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `Regression detected on Item 3.2` literal appears in halt log on PASS@1/FAIL@2 fixture.
- Ordering assertion confirms regression check runs first.
- Monotonicity check NOT consulted on the regressed item.
- Evidence at `TASKLIST_ROOT/artifacts/D-0057/evidence.md`.

**Validation:**
- Manual check: reviewer confirms byte-exact regression message.
- Evidence: fixture log.

**Dependencies:** T05.02
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.05 -- Define F-set + ordering precedence rule

| Field | Value |
|---|---|
| Roadmap Item IDs | R-094, R-095 |
| Why | `F_n` = set of FAIL-verdict items at end of fix cycle n with item identity = dedup-key; cardinality after dedup-key deduplication. Strict ordering check per cycle transition n→n+1: regression > monotonicity > hard-cap > proceed. |
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
| Deliverable IDs | D-0058 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0058/spec.md`
- `TASKLIST_ROOT/artifacts/D-0058/evidence.md`

**Deliverables:**
- F-set identity definition documented.
- 4-step ordering rule with hard-cap fallback.
- INV-012 composition wired with synthetic-dnsp findings.

**Steps:**
1. **[PLANNING]** Read R-094, R-095 specs.
2. **[EXECUTION]** Document F-set with dedup-key identity in SKILL.md.
3. **[EXECUTION]** Document the 4-step precedence: regression > monotonicity > hard-cap > proceed.
4. **[VERIFICATION]** Sub-agent confirms ordering verbatim and composition wired.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Documented precedence text explicitly states the 4-step order `regression → monotonicity → hard-cap → proceed` (regex match on the ordered string in SKILL.md) and sub-agent report confirms "regression always exits BEFORE monotonicity".
- F-set identity (dedup-key) explicitly stated in SKILL.md.
- Existing rf-team-lead.md:417 hard-cap referenced as fallback.
- Sub-agent quality-engineer report confirms 4-step ordering verbatim.

**Validation:**
- Manual check: reviewer confirms F-set identity rule.
- Evidence: sub-agent report.

**Dependencies:** T05.03, T05.04
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.06 -- Checkpoint: Phase 5 / Tasks T05.01-T05.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-090, R-091, R-092, R-093, R-094, R-095 |
| Why | Gate: verify FR-CONV.5 wrapper, API-004-M5 contract, halt emitters, and F-set/ordering rule before cross-cycle composition + counter preservation tasks. |
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
| Deliverable IDs | D-CP05-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-T01-T05.md`

**Purpose:** Mid-phase gate after the wrapper + halt-string emitters land.

**Verification:**
- Both halt-message strings emit byte-exact (D-0056 + D-0057 evidence).
- 4-step ordering rule documented (D-0058 evidence).
- F-set identity = dedup-key (D-0058 evidence).

**Exit Criteria:**
- All 5 regular tasks T05.01-T05.05 report PASS.
- Regression precedes monotonicity on the PASS@1/FAIL@2 fixture.
- `|F|=5,5,5` fixture halts at cycle 2.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T05.01-T05.05.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.01..T05.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T05.07 -- Wire INV-012 cross-cycle dedup composition

| Field | Value |
|---|---|
| Roadmap Item IDs | R-096 |
| Why | Synthetic-dnsp findings count as failures for `|F_n|`; identical dedup_key across consecutive cycles is dedup case (NOT regression — prior verdict was already FAIL). |
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
| Deliverable IDs | D-0059 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0059/spec.md`
- `TASKLIST_ROOT/artifacts/D-0059/evidence.md`

**Deliverables:**
- INV-012 cross-cycle dedup composition rule documented.
- Cross-cycle identical dedup_key contributes 1 (not 2) to F_n+1.
- Persistence trips monotonicity (intended), not regression.

**Steps:**
1. **[PLANNING]** Read R-096 composition spec.
2. **[EXECUTION]** Document INV-012 in SKILL.md.
3. **[EXECUTION]** Wire dedup-key tracking across cycles.
4. **[VERIFICATION]** Run cross-cycle same-dedup_key fixture; assert no regression halt.
5. **[COMPLETION]** Sub-agent report + evidence.

**Acceptance Criteria:**
- Cross-cycle synthetic same-dedup_key fixture contributes 1 to `F_n+1`, not 2.
- No regression halt emitted for the cross-cycle dedup case.
- Monotonicity halt fires if cardinality is non-shrinking.
- Sub-agent quality-engineer report confirms composition rule documented in SKILL.md.

**Validation:**
- Manual check: reviewer confirms dedup-key logic.
- Evidence: sub-agent report + fixture log.

**Dependencies:** T05.05; FR-CONV.6 dedup-key shape (M6 mutual)
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.08 -- Preserve 3-cycle hard cap + four counters + X-003 rejection

| Field | Value |
|---|---|
| Roadmap Item IDs | R-097, R-098, R-099 |
| Why | Existing rf-team-lead.md:417 3-cycle hard cap MUST NOT be replaced or short-circuited; four independent retry counters MUST NOT be collapsed; X-003 "shrinks too slowly" threshold REJECTED — `|F|= 5, 4` (shrink by 1) MUST continue. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope:cross-cutting |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0060 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0060/spec.md`
- `TASKLIST_ROOT/artifacts/D-0060/evidence.md`

**Deliverables:**
- Byte-diff zero on rf-team-lead.md:417.
- Four-counter independence verified at rf-task-builder.md:354-360.
- X-003 rejection enforced: slow-shrink fixture continues.

**Steps:**
1. **[PLANNING]** Capture byte hash of rf-team-lead.md:417 pre-edit.
2. **[PLANNING]** Read R-097, R-098, R-099 specs.
3. **[EXECUTION]** No edits in rf-team-lead.md:417 range; verify after T05.16 commit.
4. **[VERIFICATION]** Sub-agent confirms per-gate counters at rf-task-builder.md:354-360 preserved.
5. **[VERIFICATION]** Run `|F|=5,4` fixture; assert continues to next cycle (no rate-of-shrink parameter introduced).
6. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- Byte-diff of rf-team-lead.md:417 pre/post M5 changes is zero.
- Per-gate counters at rf-task-builder.md:354-360 are independent (no shared monotonicity state).
- `|F|=5,4` slow-shrink fixture continues to cycle 3 (X-003 NOT triggered).
- Sub-agent report confirms three preservation invariants.

**Validation:**
- Manual check: reviewer confirms preservation diffs are clean.
- Evidence: byte-diff log + sub-agent report.

**Dependencies:** T05.07
**Rollback:** As stated in roadmap
**Notes:** Critical-path override applied because the preservation invariants govern fix-cycle escalation safety.

### T05.09 -- Edit COMP-001-M5 SKILL.md A.9 invariant tail + behavioral constraints

| Field | Value |
|---|---|
| Roadmap Item IDs | R-100, R-101 |
| Why | Modify SKILL.md A.9 separate-counters invariant tail at :867-873 to add halt-precedence note; add halt-precedence rule to Behavioral Constraints hard-invariants list at :1547-1553. |
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
| Deliverable IDs | D-0061 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0061/spec.md`
- `TASKLIST_ROOT/artifacts/D-0061/evidence.md`

**Deliverables:**
- COMP-001-M5 edit at SKILL.md A.9 (867-873).
- COMP-001-M5-r12 edit at SKILL.md Behavioral Constraints (1547-1553).
- Grep evidence for halt-precedence rule in both ranges.

**Steps:**
1. **[PLANNING]** Read R-100, R-101 edit constraints.
2. **[EXECUTION]** Edit SKILL.md A.9 invariant tail at :867-873.
3. **[EXECUTION]** Edit SKILL.md Behavioral Constraints at :1547-1553.
4. **[VERIFICATION]** Grep `[HALT-MONOTONICITY]` at :867-873 and `Regression detected on Item` at :1547-1553.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -n "HALT-MONOTONICITY" src/superclaude/skills/task-builder/SKILL.md` returns line N in [867, 873].
- `grep -n "Regression detected on Item" src/superclaude/skills/task-builder/SKILL.md` returns line M in [1547, 1553].
- Both edits confined to named ranges.
- Evidence at `TASKLIST_ROOT/artifacts/D-0061/evidence.md`.

**Validation:**
- Manual check: reviewer confirms line ranges.
- Evidence: linkable grep output.

**Dependencies:** T05.06
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.10 -- Edit COMP-002-M5 rf-task-builder.md I16 fix-cycle encoding (334-361)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-102 |
| Why | Modify rf-task-builder.md QA-gate fix-cycle encoding table at :334-361 with halt rules; per-gate caps unchanged. |
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
| Deliverable IDs | D-0062 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0062/spec.md`
- `TASKLIST_ROOT/artifacts/D-0062/evidence.md`

**Deliverables:**
- I16 fix-cycle encoding table updated with halt rules.
- Per-gate caps preserved.

**Steps:**
1. **[PLANNING]** Read R-102 edit constraints.
2. **[EXECUTION]** Edit rf-task-builder.md:334-361 with halt rules.
3. **[VERIFICATION]** Grep "halt" in :334-361 range; confirm rules documented.
4. **[VERIFICATION]** Confirm per-gate cap entries unchanged.
5. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -nE "halt|HALT" src/superclaude/agents/rf-task-builder.md` returns line in [334, 361].
- Per-gate cap entries byte-identical pre/post.
- Edit confined to :334-361.
- Evidence at `TASKLIST_ROOT/artifacts/D-0062/evidence.md`.

**Validation:**
- Manual check: reviewer confirms per-gate caps unchanged.
- Evidence: linkable grep + diff.

**Dependencies:** T05.06
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.11 -- Edit COMP-003-M5 rf-qa.md Fix Cycle Protocol Rules (308-315)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-103 |
| Why | Modify rf-qa.md Fix Cycle Protocol Rules at ~:308-315 — promote existing SHOULD bullet to MUST-halt. |
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
| Deliverable IDs | D-0063 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0063/spec.md`
- `TASKLIST_ROOT/artifacts/D-0063/evidence.md`

**Deliverables:**
- Fix Cycle Protocol Rules at rf-qa.md:308-315 updated.
- Existing SHOULD bullet promoted to MUST-halt.

**Steps:**
1. **[PLANNING]** Read R-103 edit constraints.
2. **[EXECUTION]** Edit rf-qa.md:308-315 to promote the bullet.
3. **[VERIFICATION]** Grep "MUST" in :308-315 confirming promotion.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `grep -nE "MUST" src/superclaude/agents/rf-qa.md` returns line in [308, 315] for the halt rule.
- Original SHOULD bullet replaced by MUST-halt phrasing.
- Edit confined to :308-315.
- Evidence at `TASKLIST_ROOT/artifacts/D-0063/evidence.md`.

**Validation:**
- Manual check: reviewer confirms MUST-halt phrasing.
- Evidence: linkable grep output.

**Dependencies:** T05.06
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.12 -- Checkpoint: Phase 5 / Tasks T05.07-T05.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-096, R-097, R-098, R-099, R-100, R-101, R-102, R-103 |
| Why | Gate: verify INV-012 composition, 3-cycle cap + four-counter preservation + X-003 rejection, and SKILL/rf-task-builder/rf-qa edits before fixtures + migration. |
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
| Deliverable IDs | D-CP05-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-T07-T11.md`

**Purpose:** Mid-phase gate verifying INV-012 + preservation invariants + edit sites are landed.

**Verification:**
- INV-012 cross-cycle dedup composition rule documented (D-0059 evidence).
- Preservation invariants (3-cycle cap, four counters, X-003 rejection) verified (D-0060 evidence).
- SKILL/rf-task-builder/rf-qa edits at named ranges (D-0061, D-0062, D-0063 evidence).

**Exit Criteria:**
- All 5 regular tasks T05.07-T05.11 report PASS.
- rf-team-lead.md:417 byte-identical.
- Slow-shrink `|F|=5,4` fixture continues (X-003 NOT triggered).

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T05.07-T05.11.

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.07..T05.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T05.13 -- Commit TEST-015 + TEST-016 monotonicity + regression fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-104, R-105 |
| Why | TEST-015 `|F|=5,5,5` halts at cycle 2 with `[HALT-MONOTONICITY] |F|=5`; TEST-016 Item 3.2 PASS@1/FAIL@2 halts with verbatim regression message BEFORE monotonicity check. |
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
| Deliverable IDs | D-0064 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0064/evidence.md`

**Deliverables:**
- TEST-015 monotonicity halt fixture.
- TEST-016 regression precedence fixture.

**Steps:**
1. **[PLANNING]** Read R-104, R-105 fixture specs.
2. **[EXECUTION]** Author both fixtures under `tests/audit/`.
3. **[VERIFICATION]** Run pytest; assert both green.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_regression_halt_pass1_fail2.py -v` exits 0.
- TEST-015 assertion: `[HALT-MONOTONICITY] |F|=5` appears in cycle-2 log; cycle-3 not attempted.
- TEST-016 assertion: regression message emitted BEFORE monotonicity check.
- Evidence at `TASKLIST_ROOT/artifacts/D-0064/evidence.md`.

**Validation:**
- Manual check: reviewer confirms ordering assertions.
- Evidence: pytest log.

**Dependencies:** T05.03, T05.04, T05.12
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.14 -- Commit TEST-017 + TEST-022 slow-shrink + dedup fixtures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-106, R-107 |
| Why | TEST-017 `|F|=5,4` continues — strict shrink holds; X-003 NOT triggered. TEST-022 synthetic with same dedup_key in cycles 1+2 proceeds to cycle 3 (INV-012). |
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
| Deliverable IDs | D-0065 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0065/evidence.md`

**Deliverables:**
- TEST-017 slow-shrink fixture.
- TEST-022 cross-cycle dedup fixture.

**Steps:**
1. **[PLANNING]** Read R-106, R-107 specs.
2. **[EXECUTION]** Author both fixtures.
3. **[VERIFICATION]** Run pytest; assert both green.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_slow_shrink_continues.py tests/audit/test_synthetic_dnsp_dedup_not_regression.py -v` exits 0.
- TEST-017 assertion: execution log shows cycle continues.
- TEST-022 assertion: no regression halt emitted for cross-cycle dedup.
- Evidence at `TASKLIST_ROOT/artifacts/D-0065/evidence.md`.

**Validation:**
- Manual check: reviewer confirms X-003 stays REJECTED.
- Evidence: pytest log.

**Dependencies:** T05.07, T05.08, T05.13
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.15 -- Commit TEST-024 sequencing inversion fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-108 |
| Why | Sequencing test: if PR-04 (FR-CONV.3) lands before PR-06 (FR-CONV.1), dynamic enumeration still richens once catalogue activates; mitigation against K-007. |
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
| Deliverable IDs | D-0066 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0066/evidence.md`

**Deliverables:**
- TEST-024 sequencing fixture asserting INV-010 enrichment activates once catalogue is present.

**Steps:**
1. **[PLANNING]** Read R-108 fixture spec.
2. **[EXECUTION]** Author fixture under `tests/audit/`.
3. **[VERIFICATION]** Run pytest; assert green.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- `uv run pytest tests/audit/test_sequencing_PR06_before_PR04.py -v` exits 0.
- Structural assertion confirms enriched checklist when catalogue activates.
- K-007 mitigation verified.
- Evidence at `TASKLIST_ROOT/artifacts/D-0066/evidence.md`.

**Validation:**
- Manual check: reviewer confirms K-007 mitigation.
- Evidence: pytest log.

**Dependencies:** INV-010 (T03.07); T05.14
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.16 -- Execute MIG-005 PR-02 landing migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-109, R-110 |
| Why | Strictly-additive halts on existing loops; revertable by disabling guards individually; per-gate caps continue to govern on rollback; FF_RETRY_MONOTONICITY_GUARDS governance. |
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
| Deliverable IDs | D-0067 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0067/spec.md`
- `TASKLIST_ROOT/artifacts/D-0067/evidence.md`

**Deliverables:**
- MIG-005 single commit landing FR-CONV.5.
- `make verify-sync` PASS.
- FF_RETRY_MONOTONICITY_GUARDS governance entry referenced for M7.

**Steps:**
1. **[PLANNING]** Confirm T05.13..T05.15 fixtures green.
2. **[PLANNING]** Run `make verify-sync` clean baseline.
3. **[EXECUTION]** Stage all SKILL.md + rf-task-builder.md + rf-qa.md edits.
4. **[EXECUTION]** Author commit message documenting per-guard disable as rollback.
5. **[VERIFICATION]** Run `make verify-sync` post-commit; assert PASS.
6. **[COMPLETION]** Spawn quality-engineer sub-agent for diff spot-check.

**Acceptance Criteria:**
- `make verify-sync` exits 0 immediately after MIG-005 commit.
- Commit body documents per-guard disable as rollback path.
- Sub-agent report confirms rf-team-lead.md:417 byte-identical and four counters preserved.
- FF_RETRY_MONOTONICITY_GUARDS entry recorded at `TASKLIST_ROOT/artifacts/D-0067/spec.md`.

**Validation:**
- Manual check: reviewer confirms preservation invariants in commit body.
- Evidence: `make verify-sync` log + commit diff + sub-agent report.

**Dependencies:** T05.13, T05.14, T05.15
**Rollback:** As stated in roadmap (disable guards individually; per-gate caps continue)
**Notes:** Critical-path override applied because MIG-005 is the M5 landing gate.

### T05.17 -- Verify slow-cycle correction halt-safety regression sweep

| Field | Value |
|---|---|
| Roadmap Item IDs | R-099 |
| Why | Final K-005 mitigation check: confirm `|F|=5,4` and other legitimate slow-cycle fixtures continue to halt only on the documented regression+monotonicity conditions; no false-halt regressions. |
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
| Deliverable IDs | D-0100 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0100/notes.md`

**Deliverables:**
- False-halt-rate sweep results captured for M7 K-005 audit prep.

**Steps:**
1. **[PLANNING]** Read R-099 X-003 rejection enforcement.
2. **[EXECUTION]** Re-run `|F|=5,4`, `|F|=5,3`, `|F|=5,2` fixtures.
3. **[VERIFICATION]** Confirm no false halts; document false-halt-rate metric baseline.
4. **[COMPLETION]** Evidence.

**Acceptance Criteria:**
- All slow-shrink fixtures continue without halts.
- False-halt-rate metric documented at `TASKLIST_ROOT/artifacts/D-0100/notes.md` for M7 K-005 audit input.
- Cross-reference to MIG-005 commit recorded.
- Reviewer confirms baseline metric captured.

**Validation:**
- Manual check: reviewer confirms baseline metric captured.
- Evidence: pytest log + notes.

**Dependencies:** T05.16
**Rollback:** As stated in roadmap
**Notes:** None.

### T05.18 -- Checkpoint: End of Phase 5

| Field | Value |
|---|---|
| Roadmap Item IDs | R-090, R-091, R-092, R-093, R-094, R-095, R-096, R-097, R-098, R-099, R-100, R-101, R-102, R-103, R-104, R-105, R-106, R-107, R-108, R-109, R-110 |
| Why | Gate: verify all M5 deliverables (FR-CONV.5 halt guards, API-004-M5 contract, halt emitters, F-set + ordering, INV-012, preservation invariants, edit sites, fixtures, MIG-005) before unblocking M6. |
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

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-END.md`

**Purpose:** End-of-Phase-5 gate confirming retry monotonicity + regression halts live with precedence ordering, all preservation invariants intact, MIG-005 merged.

**Verification:**
- Regression precedes monotonicity on PASS@N→FAIL@N+1 fixture (D-0057 + D-0064 evidence).
- `|F|=5,5,5` halts at cycle 2; `|F|=5,4` continues (D-0056 + D-0064 + D-0065 evidence).
- rf-team-lead.md:417 byte-identical; four counters preserved (D-0060 evidence).

**Exit Criteria:**
- All 15 regular tasks T05.01-T05.17 (skipping mid-checkpoints) report PASS.
- M5 Exit Conditions per roadmap (regression flip exits first, monotonicity halt verbatim, cross-cycle dedup not regression, slow-shrink continues, X-003 REJECTED, 4 fixtures PASS) all met.
- K-005 false-halt-rate baseline captured.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Inspect M5 Exit Conditions checklist; assert every item is satisfied.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above with `Overall: Pass`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report lists task IDs T05.01-T05.17 it covers.

**Validation:**
- Manual check: reviewer confirms the report declares M5 PASS and unblocks M6.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.01..T05.17
**Rollback:** N/A (checkpoints are read-only verifications)
