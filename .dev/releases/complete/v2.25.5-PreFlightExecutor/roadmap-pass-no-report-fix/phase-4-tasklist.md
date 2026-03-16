# Phase 4 -- Prompt Contract Reinforcement

Strengthen the agent prompt contract by adding a `## Result File` section to `build_prompt()` in `process.py`, and validate with a prompt assertion test. This phase is defense-in-depth; the executor's preliminary result writer is the primary fix.

### T04.01 -- Add `## Result File` section to `build_prompt()` in `process.py`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Instructing the agent to write the result file reduces reliance on the executor fallback, but the architecture does not depend on agent compliance (FR-006). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [██████----] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/artifacts/D-0012/spec.md

**Deliverables:**
- `## Result File` section appended as the LAST `##`-level section in `build_prompt()` output, after `## Important`

**Steps:**
1. **[PLANNING]** Load `src/superclaude/cli/sprint/process.py` and locate `build_prompt()` method
2. **[PLANNING]** Confirm the phase attribute name from T01.02 OQ-001 (`self.phase` vs `self._phase`)
3. **[EXECUTION]** Append `## Result File` section as the last `##`-level section, after `## Important`
4. **[EXECUTION]** Include exact path via `config.result_file(self.phase).as_posix()` (FR-006: `as_posix()` required)
5. **[EXECUTION]** Include content instruction: content must be exactly `EXIT_RECOMMENDATION: CONTINUE`
6. **[EXECUTION]** Include conditional HALT instruction only for STRICT-tier failure scenarios
7. **[VERIFICATION]** Verify existing prompt section order is preserved -- only the final append changes
8. **[COMPLETION]** Record the prompt diff

**Acceptance Criteria:**
- `## Result File` section appears as the last `##`-level section in the built prompt (SC-013)
- Path in prompt matches `config.result_file(phase).as_posix()` exactly (FR-006)
- Existing prompt sections are not repositioned or modified
- `uv run pytest tests/sprint/ -v` shows 0 regressions

**Validation:**
- `uv run pytest tests/sprint/ -v`
- Evidence: diff of `process.py` showing only the appended section

**Dependencies:** T01.02 (OQ-001 answer needed for attribute name)
**Rollback:** Remove the `## Result File` section from `build_prompt()`

---

### T04.02 -- Write prompt assertion test for section order and path format

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | The test encodes the prompt contract: `## Result File` must be last, and the path must use `as_posix()` format. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None | Preferred: None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/artifacts/D-0013/evidence.md

**Deliverables:**
- Prompt assertion test verifying `## Result File` is after `## Important` and path uses `as_posix()` format

**Steps:**
1. **[PLANNING]** Identify test file for prompt tests (likely in `tests/sprint/`)
2. **[PLANNING]** Design assertions: `prompt.rindex("## Result File") > prompt.rindex("## Important")` and path format check
3. **[EXECUTION]** Write test asserting `## Result File` appears after `## Important` (SC-013)
4. **[EXECUTION]** Write assertion that the path string in the prompt exactly matches `config.result_file(phase).as_posix()`
5. **[EXECUTION]** Write assertion that no existing sections were repositioned
6. **[VERIFICATION]** Run `uv run pytest tests/sprint/ -v` -- new test passes, 0 regressions
7. **[COMPLETION]** Record test output to evidence artifact

**Acceptance Criteria:**
- Test asserts `prompt.rindex("## Result File") > prompt.rindex("## Important")` (SC-013)
- Test asserts path in prompt matches `config.result_file(phase).as_posix()` exactly
- `uv run pytest tests/sprint/ -v` exits 0 with 0 regressions
- Attribute name used in `build_prompt()` for phase access confirmed to match `ClaudeProcess.__init__` (OQ-001 verification from M0)
- Test recorded in `.dev/releases/current/v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/artifacts/D-0013/evidence.md`

**Validation:**
- `uv run pytest tests/sprint/ -v`
- Evidence: test execution output at intended artifact path

**Dependencies:** T04.01 (`## Result File` section must be added first)
**Rollback:** Remove the prompt assertion test

---

### Checkpoint: End of Phase 4

**Purpose:** Confirm prompt contract is strengthened and tested before final validation.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/checkpoints/CP-P04-END.md
**Verification:**
- `## Result File` section present and correctly positioned in prompt output
- Prompt assertion test passing
- Full sprint test suite green with 0 regressions
**Exit Criteria:**
- Prompt contract reinforcement complete
- No existing prompt sections displaced
- Ready for full validation sweep in Phase 5
