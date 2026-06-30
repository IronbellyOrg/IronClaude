---
executor_model_class: "implementation"
start_commit: "<PHASE_2_START_SHA>"
---
# Phase 2 -- Migration & Redaction

Phase 2 handles users who already have Tavily installed and prevents command displays from exposing API key values. It keeps migration scoped to the exact `tavily` server entry and preserves existing behavior for current installs and gateway paths.

### T02.01 -- Add stale `tavily` install reconciliation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004, R-010 |
| Why | Existing `tavily` installs using 0.1.x must not be skipped by a name-only installed check. |
| Effort | L |
| Risk | High |
| Risk Drivers | credentials, migration |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/evidence.md`

**Deliverables:**

- Tavily-scoped stale install detector.
- Remove-then-add path for stale exact `tavily` installs.
- Dry-run description for stale migration.

**Steps:**

1. **[PLANNING]** Load the installed-server check and early-return path in `install_mcp_server()`.
2. **[PLANNING]** Check how the installer receives `scope` so removal and add use compatible scope behavior.
3. **[EXECUTION]** Add stale detection for exact server name `tavily` and commands containing `tavily-mcp@0.1.x` or a package mismatch.
4. **[EXECUTION]** Add a stale branch that removes exact `tavily` before re-adding the current package token.
5. **[VERIFICATION]** Confirm current `tavily-mcp@latest` installs still use the already-installed short-circuit.
6. **[COMPLETION]** Record migration cases in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/evidence.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/src/superclaude/cli/install_mcp.py` detects stale exact server name `tavily` installs.
- A mocked stale 0.1.x install triggers remove-before-add behavior.
- A mocked current `tavily-mcp@latest` install performs no remove/add mutation.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/evidence.md` records stale/current/no-install behavior.

**Validation:**

- Manual check: review mocked stale/current migration behavior in the new Tavily tests.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/evidence.md`.

**Dependencies:** T01.01, T01.02
**Rollback:** Remove the stale branch and restore name-only skip behavior.

### T02.02 -- Mask API key values in displayed installer commands

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Dry-run and command echo output must not show actual API key values in terminal logs or transcripts. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | credentials, secrets |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/evidence.md`

**Deliverables:**

- Display redaction helper for env values and Tavily API-key URL query forms.
- Dry-run output masking behavior.

**Steps:**

1. **[PLANNING]** Identify all installer command echo/dry-run output paths.
2. **[PLANNING]** Define redaction rules for `-e KEY=value` and `tavilyApiKey=` query values.
3. **[EXECUTION]** Add a display-only redaction helper that does not alter the subprocess argv.
4. **[EXECUTION]** Route dry-run and command echo output through the redaction helper.
5. **[VERIFICATION]** Confirm a sentinel `TAVILY_API_KEY` value is absent from captured output.
6. **[COMPLETION]** Record redaction examples in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/evidence.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/src/superclaude/cli/install_mcp.py` contains a display-only command redaction path.
- Dry-run output with `TAVILY_API_KEY=test-secret-value` does not contain `test-secret-value`.
- The real subprocess argv still receives the API key value when non-dry-run install proceeds.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/evidence.md` records masked output examples.

**Validation:**

- Manual check: inspect captured stdout/stderr from the redaction test.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/evidence.md`.

**Dependencies:** T01.02
**Rollback:** Revert output redaction helper and dry-run formatting changes.

### T02.03 -- Encode Tavily migration back-compat matrix

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | The installer must handle no install, stale install, current install, gateway install, and missing key states deterministically. |
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
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/evidence.md`

**Deliverables:**

- Back-compat matrix in code comments, tests, or docs.
- Test cases for each required user state.

**Steps:**

1. **[PLANNING]** List the five required user states from the merged requirements.
2. **[PLANNING]** Map each state to expected install behavior.
3. **[EXECUTION]** Add test fixtures or parameterized cases for each state.
4. **[EXECUTION]** Ensure AIRIS gateway or other server names remain untouched.
5. **[VERIFICATION]** Run the Tavily migration test subset.
6. **[COMPLETION]** Record the matrix in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/spec.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/spec.md` contains the five-state migration matrix.
- Tests cover no install, stale exact `tavily`, current exact `tavily`, AIRIS gateway, and missing key states.
- The missing `TAVILY_API_KEY` state preserves existing prompt/warning behavior rather than blocking solely on the key.
- Evidence file `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/evidence.md` records test outcomes.

**Validation:**

- Manual check: review the parameterized migration test cases.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/evidence.md`.

**Dependencies:** T02.01, T02.02
**Rollback:** Remove the migration matrix cases and related notes.

### T02.04 -- Checkpoint: End of Phase 2

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Gate: verify outputs of tasks T02.01-T02.03 before continuing. |
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

**Checkpoint Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P02-END.md`

**Purpose:** Verify migration and redaction behavior before docs/config updates.

**Verification:**

- Confirm D-0004 stale migration evidence exists.
- Confirm D-0005 redaction evidence exists.
- Confirm D-0006 back-compat matrix exists.

**Exit Criteria:**

- Stale exact `tavily` installs are reconciled.
- Current exact `tavily` installs are not mutated.
- Dry-run output masks API key values.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for T02.01-T02.03.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T02.01-T02.03.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.03
**Rollback:** N/A (checkpoints are read-only verifications)

### T02.05 -- Post-Execution Reflection: superclaude reflect run (wrapper shell-out)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004, R-005, R-010 |
| Why | Independent post-execution deviation audit of every task in Phase 2, run by the reflect wrapper after all phase work completes. |
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
| Deliverable IDs | D-RF02 |

**Reflect Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-2/REPORT.md`

**Gate Command:** `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-2-tasklist.md --depth deep --fix --no-promote --base <PHASE_2_START_SHA> --output /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-2/`

**Steps:**

1. **[VERIFICATION]** Resolve `<PHASE_2_START_SHA>` at execution time as a single ref for the phase start.
2. **[VERIFICATION]** Run the Gate Command above and consume its exit code.
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface deviation counts.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-2/REPORT.md` exists with a deviation-taxonomy summary.
- The wrapper exited `0`; exit `10`/`11`/`2` fails the gate and is surfaced.
- Reflect ran with executor-disjoint reviewers.
- Report includes the per-task verdict matrix for Phase 2.

**Validation:**

- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** T02.01..T02.04
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately)
