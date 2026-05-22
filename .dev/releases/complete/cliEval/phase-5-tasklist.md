# Phase 5 -- Eval Bodies Coverage Gate Rollout

**Phase Goal:** Author the 15 eval bodies (E1-E15), validate the coverage gate against a real `~/.claude/settings.json`, prove the suite runs end-to-end at `--parallel 8`, and define the eval-batch rollout plan. All 15 evals enumerate in `eval list`; coverage gate green for all three v1 matcher families; full suite completes <10 min; MIG-002 batch plan recorded.

### T05.01 -- Clarify: E3-E15 eval body content per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-086,R-087,R-088,R-089,R-090,R-091,R-092,R-093,R-094,R-095,R-096,R-097,R-098 |
| Why | Roadmap entries E3..E15 state "content frozen post-OQ-2" -- exact eval body content is unresolved. Per Section 4.6 a Clarification Task must precede the blocked tasks; this captures the OQ-2 decision before T05.07..T05.21 begin authoring. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0082 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0082/spec.md`
- `TASKLIST_ROOT/artifacts/D-0082/notes.md`
- `TASKLIST_ROOT/artifacts/D-0082/evidence.md`

**Deliverables:**
- OQ-2 resolution document recorded in `.dev/releases/current/cliEval/decisions.md` naming each E3..E15 body shape (inputs, expects, capability tags) frozen before authoring begins.

**Steps:**
1. **[PLANNING]** Load OQ-2 entry from `.dev/releases/current/cliEval/decisions.md`.
2. **[PLANNING]** Identify the 13 missing eval body shapes (E3..E15) and the stakeholder owner (RyanW).
3. **[EXECUTION]** Capture the proposed body for each of E3..E15 in decisions.md with status=resolved and signed-off by RyanW.
4. **[EXECUTION]** Update Impacts list with the 13 downstream tasks (T05.07..T05.21).
5. **[VERIFICATION]** Manual review by stakeholder.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.01/`.

**Acceptance Criteria:**
- File `.dev/releases/current/cliEval/decisions.md` records OQ-2 status=resolved with a signed-off entry naming the body of each of E3..E15.
- Decision artifact lists impacts (T05.07..T05.21) and confirms blockers cleared.
- Stakeholder sign-off (RyanW) is captured next to the OQ-2 entry.
- `TASKLIST_ROOT/artifacts/D-0082/spec.md` records the resolved body summary.

**Validation:**
- Manual check: reviewed with stakeholder(s).
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None (this task unblocks T05.07..T05.21)
**Rollback:** N/A (decision artifact)
**Notes:** Confidence-triggered clarification: confidence on E3..E15 tier classification < 0.85; this task records the decision before authoring.

### T05.02 -- Author E1 auggie-first sticky lifecycle eval

| Field | Value |
|---|---|
| Roadmap Item IDs | R-082 |
| Why | E1 is the sticky-lifecycle eval per design-spec section 5: set -> real MCP call -> `auggie-flag-clear` hook clears sticky; asserts `state/auggie-first-pending/<sid>.txt` removed and `logs/auggie-first.jsonl` gains `sticky_cleared` event. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: auggie (mcp__auggie__codebase-retrieval); Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0083 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0083/spec.md`
- `TASKLIST_ROOT/artifacts/D-0083/notes.md`
- `TASKLIST_ROOT/artifacts/D-0083/evidence.md`

**Deliverables:**
- E1 eval YAML entry in `suites/real.yaml` + body assertions invoking real `mcp__auggie__codebase-retrieval`; tagged `hook-lifecycle`; skip under `--no-mcp`.

**Steps:**
1. **[PLANNING]** Confirm Expect.file (T04.02), Expect.jsonl (T04.03) and `--no-mcp` flag (T04.10).
2. **[PLANNING]** Identify auggie-flag-clear hook output paths.
3. **[EXECUTION]** Author E1 entry in `suites/real.yaml` invoking `mcp__auggie__codebase-retrieval` once.
4. **[EXECUTION]** Wire Expect.file (sticky present pre, absent post) + Expect.jsonl (sticky_cleared event) assertions.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E1`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.02/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains an entry `id: E1` with inputs invoking `mcp__auggie__codebase-retrieval`.
- E1 assertions verify `state/auggie-first-pending/<sid>.txt` exists pre-call and is removed post-call.
- E1 assertions confirm `logs/auggie-first.jsonl` gains a `sticky_cleared` event after the call.
- `TASKLIST_ROOT/artifacts/D-0083/spec.md` documents the E1 contract and `--no-mcp` skip behavior.

**Validation:**
- Manual check: run E1 and inspect transcript + per-eval JSONL.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.03, T04.04, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Soft-skip under `--no-mcp` per OQ-5 resolution.

### T05.03 -- Author E2.1 mcp__auggie__ matcher coverage eval

| Field | Value |
|---|---|
| Roadmap Item IDs | R-083 |
| Why | E2.1 covers the `mcp__auggie__*` matcher via a real `codebase-retrieval` invocation; parameterize-expanded id matches the eval_id regex; hook telemetry asserted in per-eval JSONL. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: auggie (mcp__auggie__codebase-retrieval); Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0084 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0084/spec.md`
- `TASKLIST_ROOT/artifacts/D-0084/notes.md`
- `TASKLIST_ROOT/artifacts/D-0084/evidence.md`

**Deliverables:**
- E2.1 parameterize entry in `suites/real.yaml` invoking real `mcp__auggie__codebase-retrieval`; tagged `hook-coverage`.

**Steps:**
1. **[PLANNING]** Confirm FR-SCH2 (T01.05) accepts parameterize-expanded id `E2.1`.
2. **[PLANNING]** Identify expected hook telemetry events for `mcp__auggie__*`.
3. **[EXECUTION]** Author E2.1 parameterize entry invoking `mcp__auggie__codebase-retrieval`.
4. **[EXECUTION]** Wire Expect.jsonl assertion that the matcher-coverage hook fires.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E2.1`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.03/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains an entry `id: E2.1` (or parameterize template producing E2.1).
- E2.1 invokes `mcp__auggie__codebase-retrieval` and asserts the `mcp__auggie__*` matcher hook telemetry in per-eval JSONL.
- Parameterize-expanded id `E2.1` passes `validate_eval_id` (FR-SCH2).
- `TASKLIST_ROOT/artifacts/D-0084/spec.md` documents the matcher contract.

**Validation:**
- Manual check: run E2.1 and inspect per-eval JSONL for hook telemetry.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.05, T04.03, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Soft-skip under `--no-mcp` per OQ-5; status `SKIPPED` with `skip_reason` populated.

### T05.04 -- Author E2.2 mcp__auggie-mcp__ matcher coverage eval

| Field | Value |
|---|---|
| Roadmap Item IDs | R-084 |
| Why | E2.2 covers the `mcp__auggie-mcp__*` matcher via a real `ask_question` invocation; hook telemetry asserted; soft-skip under `--no-mcp`. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: auggie-mcp (mcp__auggie-mcp__ask_question); Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0085 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0085/spec.md`
- `TASKLIST_ROOT/artifacts/D-0085/notes.md`
- `TASKLIST_ROOT/artifacts/D-0085/evidence.md`

**Deliverables:**
- E2.2 parameterize entry in `suites/real.yaml` invoking real `mcp__auggie-mcp__ask_question`; tagged `hook-coverage`.

**Steps:**
1. **[PLANNING]** Confirm parameterize-expanded id `E2.2` passes FR-SCH2.
2. **[PLANNING]** Identify expected matcher telemetry for `mcp__auggie-mcp__*`.
3. **[EXECUTION]** Author E2.2 entry invoking `mcp__auggie-mcp__ask_question`.
4. **[EXECUTION]** Wire Expect.jsonl asserting the matcher hook telemetry.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E2.2`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.04/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains an entry `id: E2.2` invoking `mcp__auggie-mcp__ask_question`.
- E2.2 asserts the `mcp__auggie-mcp__*` matcher hook telemetry in per-eval JSONL.
- Parameterize-expanded id `E2.2` passes `validate_eval_id` (FR-SCH2).
- `TASKLIST_ROOT/artifacts/D-0085/spec.md` documents the matcher contract.

**Validation:**
- Manual check: run E2.2 and inspect per-eval JSONL.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.05, T04.03, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Soft-skip under `--no-mcp` per OQ-5; status `SKIPPED` with `skip_reason` populated.

### T05.05 -- Author E2.3 mcp__airis-mcp-gateway__ matcher coverage eval

| Field | Value |
|---|---|
| Roadmap Item IDs | R-085 |
| Why | E2.3 covers the `mcp__airis-mcp-gateway__*` matcher via a real `auggie_search` invocation; soft-skip under `--no-mcp` with `skip_reason` recorded. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: airis-mcp-gateway (mcp__airis-mcp-gateway__auggie_search); Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0086 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0086/spec.md`
- `TASKLIST_ROOT/artifacts/D-0086/notes.md`
- `TASKLIST_ROOT/artifacts/D-0086/evidence.md`

**Deliverables:**
- E2.3 parameterize entry in `suites/real.yaml` invoking real `mcp__airis-mcp-gateway__auggie_search`; soft-skip under `--no-mcp`.

**Steps:**
1. **[PLANNING]** Confirm parameterize-expanded id `E2.3` passes FR-SCH2 (T01.05).
2. **[PLANNING]** Identify gateway matcher telemetry shape.
3. **[EXECUTION]** Author E2.3 entry invoking `mcp__airis-mcp-gateway__auggie_search`.
4. **[EXECUTION]** Wire Expect.jsonl asserting the matcher hook telemetry; soft-skip flag honored.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E2.3`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.05/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E2.3` invoking `mcp__airis-mcp-gateway__auggie_search`.
- Under `--no-mcp`, E2.3 emits status `SKIPPED` with `skip_reason` populated.
- E2.3 asserts the gateway matcher hook telemetry in per-eval JSONL.
- `TASKLIST_ROOT/artifacts/D-0086/spec.md` documents the matcher contract.

**Validation:**
- Manual check: run E2.3 with and without `--no-mcp`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.05, T04.03, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Completes the v1 matcher coverage roster.

### T05.06 -- Checkpoint: Phase 5 / Tasks T05.01-T05.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-082,R-083,R-084,R-085 |
| Why | Gate: verify OQ-2 clarification, E1 sticky-lifecycle, and 3 matcher-coverage evals before E3..E15 authoring begins. |
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

**Purpose:** Confirm OQ-2 clarification + E1 + E2.{1,2,3} before E3..E15 authoring.

**Verification:**
- OQ-2 resolution recorded in `.dev/releases/current/cliEval/decisions.md` with stakeholder sign-off.
- E1, E2.1, E2.2, E2.3 entries present in `suites/real.yaml` and run green individually.
- Matcher coverage gate (T04.14) recognises all 3 v1 matchers (`auggie`, `auggie-mcp`, `airis-mcp-gateway`).

**Exit Criteria:**
- `uv run superclaude eval run --suite real --eval E1` exits 0; same for E2.1, E2.2, E2.3.
- `uv run superclaude eval doctor --check-coverage` exits 0 against current `~/.claude/settings.json`.
- Checkpoint report `CP-P05-T01-T05.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T05.01-T05.05).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.01..T05.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T05.07 -- Author E3 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-086 |
| Why | E3 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: passes deterministically on a clean HOME. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0087 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0087/spec.md`
- `TASKLIST_ROOT/artifacts/D-0087/notes.md`
- `TASKLIST_ROOT/artifacts/D-0087/evidence.md`

**Deliverables:**
- E3 eval YAML entry in `suites/real.yaml` plus body assertions per OQ-2 resolution captured in T05.01.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution from T05.01 decision artifact.
2. **[PLANNING]** Confirm Expect.* primitives (T04.01-T04.08) cover the assertions named.
3. **[EXECUTION]** Author E3 entry in `suites/real.yaml` matching the resolved body shape.
4. **[EXECUTION]** Wire assertions per OQ-2 resolution.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E3`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.07/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E3` whose body matches the OQ-2 resolution recorded in T05.01.
- `uv run superclaude eval run --suite real --eval E3` exits 0 on a clean HOME.
- E3 is deterministic: 3 consecutive runs produce identical EvalOutcome statuses.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0087/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E3 thrice on a clean HOME and confirm identical PASS outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.08 -- Author E4 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-087 |
| Why | E4 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0088 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0088/spec.md`
- `TASKLIST_ROOT/artifacts/D-0088/notes.md`
- `TASKLIST_ROOT/artifacts/D-0088/evidence.md`

**Deliverables:**
- E4 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution from T05.01.
2. **[PLANNING]** Confirm Expect.* primitives are available.
3. **[EXECUTION]** Author E4 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E4`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.08/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E4` whose body matches the OQ-2 resolution from T05.01.
- `uv run superclaude eval run --suite real --eval E4` exits 0 deterministically across 3 consecutive runs.
- Test asserts deterministic AC behavior; eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0088/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E4 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.09 -- Author E5 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-088 |
| Why | E5 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0089 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0089/spec.md`
- `TASKLIST_ROOT/artifacts/D-0089/notes.md`
- `TASKLIST_ROOT/artifacts/D-0089/evidence.md`

**Deliverables:**
- E5 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E5 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E5`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.09/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E5` whose body matches the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E5` exits 0 deterministically.
- E5 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0089/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E5 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.10 -- Author E6 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-089 |
| Why | E6 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0090 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0090/spec.md`
- `TASKLIST_ROOT/artifacts/D-0090/notes.md`
- `TASKLIST_ROOT/artifacts/D-0090/evidence.md`

**Deliverables:**
- E6 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E6 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E6`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.10/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E6` whose body matches the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E6` exits 0 deterministically.
- E6 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0090/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E6 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.11 -- Author E7 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-090 |
| Why | E7 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0091 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0091/spec.md`
- `TASKLIST_ROOT/artifacts/D-0091/notes.md`
- `TASKLIST_ROOT/artifacts/D-0091/evidence.md`

**Deliverables:**
- E7 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E7 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E7`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.11/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E7` whose body matches the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E7` exits 0 deterministically.
- E7 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0091/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E7 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.12 -- Checkpoint: Phase 5 / Tasks T05.07-T05.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-086,R-087,R-088,R-089,R-090 |
| Why | Gate: verify E3-E7 author and run green deterministically before E8-E12 authoring begins. |
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

**Purpose:** Confirm E3-E7 author and run deterministically before E8-E12 authoring.

**Verification:**
- Entries E3..E7 present in `suites/real.yaml` and pass FR-SCH2 eval_id regex.
- Each of E3..E7 runs green individually under `uv run superclaude eval run --eval <id>`.
- 3 consecutive runs of any single E3..E7 produce identical EvalOutcome status.

**Exit Criteria:**
- `uv run superclaude eval run --suite real --eval E3` ... `E7` each exit 0.
- `uv run superclaude eval list --json` enumerates all 7 authored entries (E1, E2.{1,2,3}, E3..E7).
- Checkpoint report `CP-P05-T07-T11.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T05.07-T05.11).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.07..T05.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T05.13 -- Author E8 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-091 |
| Why | E8 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0092 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0092/spec.md`
- `TASKLIST_ROOT/artifacts/D-0092/notes.md`
- `TASKLIST_ROOT/artifacts/D-0092/evidence.md`

**Deliverables:**
- E8 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E8 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E8`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.13/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E8` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E8` exits 0 deterministically across 3 runs.
- E8 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0092/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E8 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.14 -- Author E9 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-092 |
| Why | E9 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0093 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0093/spec.md`
- `TASKLIST_ROOT/artifacts/D-0093/notes.md`
- `TASKLIST_ROOT/artifacts/D-0093/evidence.md`

**Deliverables:**
- E9 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E9 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E9`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.14/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E9` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E9` exits 0 deterministically across 3 runs.
- E9 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0093/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E9 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.15 -- Author E10 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-093 |
| Why | E10 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0094 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0094/spec.md`
- `TASKLIST_ROOT/artifacts/D-0094/notes.md`
- `TASKLIST_ROOT/artifacts/D-0094/evidence.md`

**Deliverables:**
- E10 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E10 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E10`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.15/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E10` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E10` exits 0 deterministically across 3 runs.
- E10 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0094/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E10 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.16 -- Author E11 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-094 |
| Why | E11 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0095 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0095/spec.md`
- `TASKLIST_ROOT/artifacts/D-0095/notes.md`
- `TASKLIST_ROOT/artifacts/D-0095/evidence.md`

**Deliverables:**
- E11 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E11 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E11`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.16/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E11` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E11` exits 0 deterministically across 3 runs.
- E11 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0095/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E11 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.17 -- Author E12 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-095 |
| Why | E12 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0096 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0096/spec.md`
- `TASKLIST_ROOT/artifacts/D-0096/notes.md`
- `TASKLIST_ROOT/artifacts/D-0096/evidence.md`

**Deliverables:**
- E12 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E12 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E12`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.17/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E12` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E12` exits 0 deterministically across 3 runs.
- E12 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0096/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E12 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.18 -- Checkpoint: Phase 5 / Tasks T05.13-T05.17

| Field | Value |
|---|---|
| Roadmap Item IDs | R-091,R-092,R-093,R-094,R-095 |
| Why | Gate: verify E8-E12 author and run green deterministically before E13-E15 authoring + SC2 + R3-mit. |
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
| Deliverable IDs | D-CP05-MID-T13-T17 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-T13-T17.md`

**Purpose:** Confirm E8-E12 author and run deterministically before E13-E15 + SC2 + R3-mit.

**Verification:**
- Entries E8..E12 present in `suites/real.yaml` and pass FR-SCH2.
- Each of E8..E12 runs green individually.
- 3 consecutive runs of any single E8..E12 produce identical EvalOutcome status.

**Exit Criteria:**
- `uv run superclaude eval run --suite real --eval E8`..`E12` each exit 0.
- `uv run superclaude eval list --json` enumerates 12+ authored entries.
- Checkpoint report `CP-P05-T13-T17.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-T13-T17.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T05.13-T05.17).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.13..T05.17
**Rollback:** N/A (checkpoints are read-only verifications)

### T05.19 -- Author E13 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-096 |
| Why | E13 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0097 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0097/spec.md`
- `TASKLIST_ROOT/artifacts/D-0097/notes.md`
- `TASKLIST_ROOT/artifacts/D-0097/evidence.md`

**Deliverables:**
- E13 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E13 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E13`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.19/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E13` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E13` exits 0 deterministically across 3 runs.
- E13 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0097/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E13 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.20 -- Author E14 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-097 |
| Why | E14 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0098 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0098/spec.md`
- `TASKLIST_ROOT/artifacts/D-0098/notes.md`
- `TASKLIST_ROOT/artifacts/D-0098/evidence.md`

**Deliverables:**
- E14 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E14 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E14`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.20/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E14` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E14` exits 0 deterministically across 3 runs.
- E14 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0098/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E14 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Confidence 75% reflects OQ-2 dependency at task generation time. Determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit. Eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.21 -- Author E15 eval body per OQ-2 resolution

| Field | Value |
|---|---|
| Roadmap Item IDs | R-098 |
| Why | E15 body content is frozen post-OQ-2 (resolved in T05.01). Minimum AC: deterministic AC. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0099 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0099/spec.md`
- `TASKLIST_ROOT/artifacts/D-0099/notes.md`
- `TASKLIST_ROOT/artifacts/D-0099/evidence.md`

**Deliverables:**
- E15 eval YAML entry + body assertions per OQ-2 resolution.

**Steps:**
1. **[PLANNING]** Load OQ-2 resolution.
2. **[PLANNING]** Confirm Expect.* primitives.
3. **[EXECUTION]** Author E15 entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire assertions per resolved body shape.
5. **[VERIFICATION]** Run `uv run superclaude eval run --suite real --eval E15`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.21/`.

**Acceptance Criteria:**
- File `suites/real.yaml` contains entry `id: E15` matching the OQ-2 resolution.
- `uv run superclaude eval run --suite real --eval E15` exits 0 deterministically across 3 runs.
- E15 outcome is reproducible across 3 consecutive runs.
- Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`.
- `TASKLIST_ROOT/artifacts/D-0099/spec.md` records the eval body summary.

**Validation:**
- Manual check: run E15 thrice and confirm identical outcomes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.01, T04.01..T04.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Final eval body in the v1 suite. Confidence 75% reflects OQ-2 dependency at task generation time; determinism assertion assumes M3 EvalRunner + Reporter availability transitively via M4 exit; eval body assumes per-eval HOME isolation enforced by FR-ISO2 (T02.08).

### T05.22 -- Verify SC2: manifest schema covers all 15 evals

| Field | Value |
|---|---|
| Roadmap Item IDs | R-099 |
| Why | SC2 confirms all E1-E15 IDs match the FR-SCH2 regex and load via the schema; `eval doctor` reports zero violations on `real.yaml`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0100 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0100/spec.md`
- `TASKLIST_ROOT/artifacts/D-0100/notes.md`
- `TASKLIST_ROOT/artifacts/D-0100/evidence.md`

**Deliverables:**
- Verification artifact `TASKLIST_ROOT/evidence/T05.22/sc2.log` recording `eval doctor --suite real` with zero violations on all 15 evals.

**Steps:**
1. **[PLANNING]** Confirm all 15 evals (T05.02..T05.21) are authored.
2. **[PLANNING]** Confirm FR-SCH1 (T01.04) and FR-SCH2 (T01.05) are wired into doctor.
3. **[EXECUTION]** Run `superclaude eval doctor --suite real` and capture output to `sc2.log`.
4. **[EXECUTION]** Confirm zero violations and all 15 ids enumerated.
5. **[VERIFICATION]** Inspect `sc2.log` for "0 violations" line.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.22/`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/evidence/T05.22/sc2.log` records `superclaude eval doctor --suite real` with zero schema or regex violations.
- All 15 evals (E1, E2.1-3, E3..E15) appear in the doctor output.
- Parameterize-expanded ids E2.1, E2.2, E2.3 are individually validated.
- `TASKLIST_ROOT/artifacts/D-0100/spec.md` documents the verification outcome.

**Validation:**
- Manual check: run doctor and grep for `0 violations`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.04, T01.05, T05.02..T05.21
**Rollback:** TBD (if not specified in roadmap)
**Notes:** SC2 success criterion landed here; cross-referenced from M6 SC5 (T06.09).

### T05.23 -- Implement R3-mit MCP retry-once policy

| Field | Value |
|---|---|
| Roadmap Item IDs | R-100 |
| Why | R3-mit performs per-eval retry-once on MCP-specific failure modes; honors `MCP_FLAKY_TAG`; tagged failures recorded in `outcome.artifacts` with `mcp_server_flaky`. |
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
| Deliverable IDs | D-0101 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0101/spec.md`
- `TASKLIST_ROOT/artifacts/D-0101/notes.md`
- `TASKLIST_ROOT/artifacts/D-0101/evidence.md`

**Deliverables:**
- Retry-once policy module in `src/superclaude/cli/eval/retry.py` honored by EvalRunner when an eval is tagged `MCP_FLAKY_TAG`; failure path records `mcp_server_flaky` artifact.

**Steps:**
1. **[PLANNING]** Confirm NFR-REL2 (T03.08) `MCP_FLAKY_TAG` constant + EvalRunner integration.
2. **[PLANNING]** Read OQ-10 resolution status (may resolve empirically).
3. **[EXECUTION]** Add retry-once policy invoked on MCP-tagged failures in EvalRunner.
4. **[EXECUTION]** Record `mcp_server_flaky` in `outcome.artifacts` on retry-triggering failure.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_mcp_retry_once.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.23/`.

**Acceptance Criteria:**
- Eval carrying the `MCP_FLAKY_TAG` constant (and only that tag) triggers retry-once on stubbed MCP failure; on persistent failure, status is `FAIL` with `mcp_server_flaky` artifact in `outcome.artifacts`.
- Non-tagged evals do not retry (NFR-REL2 default honored).
- `TASKLIST_ROOT/artifacts/D-0101/spec.md` documents the retry policy.
- Decision recorded if OQ-10 keeps R3-mit at P1 vs promotes to P0.

**Validation:**
- Manual check: stub MCP failure on a tagged eval and observe retry behavior.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.05, T03.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** OQ-10 resolution may downgrade or remove this policy.

### T05.24 -- Checkpoint: Phase 5 / Tasks T05.19-T05.23

| Field | Value |
|---|---|
| Roadmap Item IDs | R-096,R-097,R-098,R-099,R-100 |
| Why | Gate: verify E13-E15 author, SC2 schema coverage, and R3-mit retry policy before coverage gate + no-MCP tests close M5. |
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
| Deliverable IDs | D-CP05-MID-T19-T23 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-T19-T23.md`

**Purpose:** Confirm E13-E15 + SC2 + R3-mit before coverage gate tests and MIG-002 close M5.

**Verification:**
- Entries E13, E14, E15 present in `suites/real.yaml` and run green individually.
- SC2 doctor invocation records zero violations on all 15 evals.
- R3-mit retry-once policy retries exactly once on a stubbed MCP failure.

**Exit Criteria:**
- `uv run superclaude eval run --suite real --eval E13`..`E15` each exit 0.
- `TASKLIST_ROOT/evidence/T05.22/sc2.log` exists and shows 0 violations.
- Checkpoint report `CP-P05-T19-T23.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-T19-T23.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T05.19-T05.23).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.19..T05.23
**Rollback:** N/A (checkpoints are read-only verifications)

### T05.25 -- TEST-013 coverage gate integration tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-101 |
| Why | TEST-013 covers doctor + top-of-run coverage gate against missing and complete matcher sets; missing matcher fails; complete matcher passes; doctor names uncovered patterns. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0102 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0102/spec.md`
- `TASKLIST_ROOT/artifacts/D-0102/notes.md`
- `TASKLIST_ROOT/artifacts/D-0102/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_coverage_gate_integration.py` covering full-coverage and missing-matcher scenarios.

**Steps:**
1. **[PLANNING]** Confirm FR-G5 coverage gate (T04.14) is wired into doctor + run.
2. **[PLANNING]** Build a fixture settings.json with 4 matchers (3 covered + 1 uncovered).
3. **[EXECUTION]** Author tests exercising doctor and top-of-run gate against the fixture.
4. **[EXECUTION]** Assert doctor names the uncovered pattern in stderr.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_coverage_gate_integration.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.25/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_coverage_gate_integration.py` exits 0 with tests for: complete coverage passes; missing matcher fails with exit 2; doctor stderr names the uncovered pattern.
- Test fixtures live under `tests/cli/eval/fixtures/coverage_gate/` for the 4-matcher case.
- Test asserts a `coverage_missing:<pattern>` artifact file is produced.
- `TASKLIST_ROOT/artifacts/D-0102/spec.md` records the test matrix.

**Validation:**
- Manual check: run the targeted pytest module.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.14, T05.02..T05.21
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Cross-links FR-G5 + the authored eval suite.

### T05.26 -- TEST-014 no-MCP skip behavior tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-102 |
| Why | TEST-014 verifies MCP-dependent evals are classified as SKIPPED with `skip_reason` set when `--no-mcp` is used; counts.kept_plus_skipped_equals_n_prime is true. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0103 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0103/spec.md`
- `TASKLIST_ROOT/artifacts/D-0103/notes.md`
- `TASKLIST_ROOT/artifacts/D-0103/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_no_mcp_skip.py` asserting `--no-mcp` skips MCP evals with `skip_reason` populated.

**Steps:**
1. **[PLANNING]** Confirm CapabilityGates (T01.11) + FR-RPT1 (T03.11) wire `--no-mcp` skipping.
2. **[PLANNING]** Identify MCP-dependent evals (E1, E2.1, E2.2, E2.3).
3. **[EXECUTION]** Author tests running the suite with `--no-mcp` and asserting each MCP eval status=SKIPPED.
4. **[EXECUTION]** Assert RunSummary `counts.kept_plus_skipped_equals_n_prime` is True.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_no_mcp_skip.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.26/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_no_mcp_skip.py` exits 0 asserting MCP evals classify SKIPPED with non-empty `skip_reason` under `--no-mcp`.
- RunSummary `counts.kept_plus_skipped_equals_n_prime` is True under the skip scenario.
- Each SKIPPED eval entry includes a populated `skip_reason` value.
- `TASKLIST_ROOT/artifacts/D-0103/spec.md` records the skip semantics.

**Validation:**
- Manual check: run the targeted pytest module.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.11, T03.11, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Provides confidence that R9 PR scope creep mitigation works under reduced capability. The DM-001 `skip_flag_triggered` field is informational only; TEST-014 does not require asserting its value beyond `skip_reason` being populated.

### T05.27 -- Define MIG-002 eval-batch rollout plan

| Field | Value |
|---|---|
| Roadmap Item IDs | R-103 |
| Why | MIG-002 splits broad eval bodies into reviewable batches after harness contract lands (R9 mitigation): 15 eval IDs tracked, batches of 3-5 defined, harness PR separable, eval PRs reference coverage map. |
| Effort | S |
| Risk | Low |
| Risk Drivers | data (migration keyword), planning |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0104 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0104/spec.md`
- `TASKLIST_ROOT/artifacts/D-0104/notes.md`
- `TASKLIST_ROOT/artifacts/D-0104/evidence.md`

**Deliverables:**
- `docs/eval/mig-002-batch-plan.md` defining 3-5 eval batches for PR rollout post-harness with coverage map links.

**Steps:**
1. **[PLANNING]** Confirm all 15 evals authored (T05.02..T05.21) and the coverage gate (T05.25) green.
2. **[PLANNING]** Group E1, E2.1-3, E3..E15 into batches of 3-5 by domain.
3. **[EXECUTION]** Author `docs/eval/mig-002-batch-plan.md` listing batches and per-batch DoD.
4. **[EXECUTION]** Add coverage-map reference per batch.
5. **[VERIFICATION]** Sub-agent quality-engineer review for batching coherence.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T05.27/`.

**Acceptance Criteria:**
- File `docs/eval/mig-002-batch-plan.md` exists and partitions all 15 evals into 3-5 batches.
- Each batch entry lists DoD and the matchers it covers.
- Harness PR is named explicitly as PR 1 with eval PRs as PR 2+; each batch entry in `docs/eval/mig-002-batch-plan.md` includes a `coverage-map: <link>` field that the corresponding eval PR description cites verbatim (per roadmap MIG-002 AC "eval PRs reference coverage map").
- `TASKLIST_ROOT/artifacts/D-0104/spec.md` records the batch plan summary.

**Validation:**
- Manual check: reviewer reads the batch plan and confirms partition.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T05.02..T05.21, T05.25
**Rollback:** TBD (if not specified in roadmap)
**Notes:** STRICT tier per Section 5.3.2 (migration keyword + critical path override).

### T05.28 -- Checkpoint: End of Phase 5

| Field | Value |
|---|---|
| Roadmap Item IDs | R-082..R-103 |
| Why | M5 exit gate: all 15 evals enumerate in `eval list`, coverage gate green for the 3 v1 matcher families, full suite completes <10 min on dev host, MIG-002 batch plan recorded. |
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

**Purpose:** M5 exit gate: 15 evals + coverage gate + sub-10-min suite + MIG-002 batch plan.

**Verification:**
- `uv run superclaude eval list` enumerates 15 evals (E1, E2.1-3, E3..E15).
- `uv run superclaude eval doctor --check-coverage` exits 0 against `~/.claude/settings.json` covering all 3 v1 matcher families.
- Full suite at `--parallel 8` completes in <600 seconds (per NFR-PERF3 budget).

**Exit Criteria:**
- `uv run superclaude eval run --suite real --parallel 8` exits 0 (or 1 only if expected XFAIL evals).
- `docs/eval/mig-002-batch-plan.md` exists and lists all 15 evals.
- Checkpoint report `CP-P05-END.md` records pass/fail per task in Phase 5.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T05.01-T05.27).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.01..T05.27
**Rollback:** N/A (checkpoints are read-only verifications)
