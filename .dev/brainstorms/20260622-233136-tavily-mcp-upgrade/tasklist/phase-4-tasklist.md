---
executor_model_class: "implementation"
start_commit: "<PHASE_4_START_SHA>"
---
# Phase 4 -- Tests & Verification

Phase 4 creates the Tavily-focused regression suite and optional live verification path. It validates installer behavior with mocks and reserves live map/crawl enumeration for explicitly enabled integration runs.

### T04.01 -- Implement Tavily installer unit and regression tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009, R-012 |
| Why | The upgrade must be guarded by tests that do not require live Claude CLI, Node network install, or a Tavily API key. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | key, pipeline |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/evidence.md`

**Deliverables:**

- Tavily installer test module under `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/tests/`.
- Mocked tests for package token, fresh install, stale migration, current skip, dry-run, API-key env behavior, redaction, docs parity, config cleanup, transport shape, command ordering, and installed-check robustness.

**Steps:**

1. **[PLANNING]** Choose the test file path based on existing CLI/MCP test organization.
2. **[PLANNING]** Define mocks for `_run_command`, `prompt_for_api_key`, and installed-state probes.
3. **[EXECUTION]** Add the Tavily test module with unit and regression cases from the merged requirements.
4. **[EXECUTION]** Ensure tests never call live `claude`, live `npx`, or Tavily APIs by default.
5. **[VERIFICATION]** Run `uv run pytest` on the Tavily test module.
6. **[COMPLETION]** Record test command output in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/evidence.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/tests/cli/test_install_mcp_tavily.py` or `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/tests/mcp/test_tavily_upgrade.py` exists.
- The Tavily test module mocks Claude CLI and network-dependent subprocesses by default.
- `uv run pytest <tavily-test-module> -v` exits 0 after implementation.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/evidence.md` records the passing test command.

**Validation:**

- Manual check: reviewer confirms the Tavily test module includes all required regression cases.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/evidence.md`.

**Dependencies:** T01.01, T02.01, T02.02, T03.03
**Rollback:** Remove the Tavily-specific test module.

### T04.02 -- Add optional map/crawl integration smoke

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | The upgraded package should expose map/crawl capabilities, but live enumeration requires external prerequisites and must be optional. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/evidence.md`

**Deliverables:**

- Optional integration test or documented smoke procedure for `tavily-map` and `tavily-crawl`.
- Skip condition for missing live prerequisites.

**Steps:**

1. **[PLANNING]** Define live prerequisites for map/crawl tool enumeration.
2. **[PLANNING]** Select exact skip marker or manual verification path.
3. **[EXECUTION]** Add optional integration test or documentation that enumerates Tavily tools.
4. **[EXECUTION]** Require map/crawl presence only when the integration test is explicitly enabled.
5. **[VERIFICATION]** Confirm default unit test runs skip the live smoke without failure.
6. **[COMPLETION]** Record smoke procedure in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/spec.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/docs/user-guide/mcp-servers.md` or the Tavily test module describes map/crawl verification.
- Live tool enumeration is skipped by default unless prerequisites are present.
- When enabled, the smoke checks for `tavily-map` and `tavily-crawl` or their actual exposed tool names.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/spec.md` records the skip and enablement rules.

**Validation:**

- Manual check: reviewer confirms the live smoke is optional and map/crawl-specific.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/evidence.md`.

**Dependencies:** T03.01, T04.01
**Rollback:** Remove the optional integration smoke.

### T04.03 -- Run final Tavily validation commands

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | The completed change must be validated with targeted tests and sync checks before implementation is considered complete. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0012/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0012/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0012/evidence.md`

**Deliverables:**

- Validation command checklist.
- Captured targeted test output.
- Sync verification note if component sync applies.

**Steps:**

1. **[PLANNING]** Identify final validation commands from the merged requirements and project rules.
2. **[PLANNING]** Confirm all Python commands use `uv run`.
3. **[EXECUTION]** Run `uv run pytest <tavily-test-module> -v`.
4. **[EXECUTION]** Run relevant formatting/lint checks scoped to changed files if implementation touches Python.
5. **[VERIFICATION]** Confirm test output shows success or record exact failures.
6. **[COMPLETION]** Save validation output to `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0012/evidence.md`.

**Acceptance Criteria:**

- Command `uv run pytest <tavily-test-module> -v` exits 0 after implementation.
- Any formatting/lint command used is scoped to changed files and its result is recorded.
- Validation output is saved under `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0012/evidence.md`.
- The validation note states whether live map/crawl smoke was skipped or run.

**Validation:**

- Manual check: reviewer confirms the validation evidence file records the final commands.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0012/evidence.md`.

**Dependencies:** T04.01, T04.02
**Rollback:** N/A (validation produces evidence only)

### T04.04 -- Checkpoint: End of Phase 4

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Gate: verify outputs of tasks T04.01-T04.03 before closing the tasklist. |
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

**Checkpoint Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P04-END.md`

**Purpose:** Verify all Tavily upgrade tests and validation artifacts are ready.

**Verification:**

- Confirm D-0010 test-suite evidence exists.
- Confirm D-0011 optional map/crawl smoke procedure exists.
- Confirm D-0012 final validation evidence exists.

**Exit Criteria:**

- Tavily test module exists.
- Targeted `uv run pytest` command is documented.
- Optional map/crawl smoke has skip and enablement rules.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for T04.01-T04.03.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P04-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T04.01-T04.03.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.01..T04.03
**Rollback:** N/A (checkpoints are read-only verifications)

### T04.05 -- Post-Execution Reflection: superclaude reflect run (wrapper shell-out)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008, R-009, R-012 |
| Why | Independent post-execution deviation audit of every task in Phase 4, run by the reflect wrapper after all phase work completes. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification (reflect IS the verification) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | No |
| Deliverable IDs | D-RF04 |

**Reflect Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-4/REPORT.md`

**Gate Command:** `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-4-tasklist.md --depth deep --fix --no-promote --base <PHASE_4_START_SHA> --output /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-4/`

**Steps:**

1. **[VERIFICATION]** Resolve `<PHASE_4_START_SHA>` at execution time as a single ref for the phase start.
2. **[VERIFICATION]** Run the Gate Command above and consume its exit code.
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface deviation counts.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-4/REPORT.md` exists with a deviation-taxonomy summary.
- The wrapper exited `0`; exit `10`/`11`/`2` fails the gate and is surfaced.
- Reflect ran with executor-disjoint reviewers.
- Report includes the per-task verdict matrix for Phase 4.

**Validation:**

- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** T04.01..T04.04
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately)
