---
executor_model_class: "implementation"
start_commit: "<PHASE_1_START_SHA>"
---
# Phase 1 -- Installer Core

Phase 1 updates the live Tavily installer registry and isolates command construction so the package policy and stdio grammar are testable. It preserves the local stdio default and records remote HTTP as out of scope for this upgrade.

### T01.01 -- Update `MCP_SERVERS["tavily"]` package token

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002 |
| Why | The live installer must stop hard-pinning `tavily-mcp@0.1.2` and use the requested `tavily-mcp@latest` stdio path. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | key, change |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/evidence.md`

**Deliverables:**

- Centralized Tavily package token such as `TAVILY_MCP_PACKAGE = "tavily-mcp@latest"`.
- Updated `MCP_SERVERS["tavily"]["command"]` deriving from that token.
- Preserved `transport: "stdio"` and `api_key_env: "TAVILY_API_KEY"`.

**Steps:**

1. **[PLANNING]** Load `src/superclaude/cli/install_mcp.py` and identify the `MCP_SERVERS["tavily"]` entry.
2. **[PLANNING]** Check that no remote HTTP default change is required in this task.
3. **[EXECUTION]** Add the centralized Tavily package token near the MCP registry constants.
4. **[EXECUTION]** Replace the stale Tavily command with a command that uses `tavily-mcp@latest`.
5. **[VERIFICATION]** Confirm the registry entry still uses `transport: "stdio"` and `api_key_env: "TAVILY_API_KEY"`.
6. **[COMPLETION]** Record the changed registry token and command in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/evidence.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/src/superclaude/cli/install_mcp.py` contains a centralized `tavily-mcp@latest` package token.
- `MCP_SERVERS["tavily"]["command"]` no longer contains `tavily-mcp@0.1.2`.
- `MCP_SERVERS["tavily"]["transport"]` remains `stdio`.
- Evidence file `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/evidence.md` records the final registry values.

**Validation:**

- Manual check: inspect the Tavily registry entry in `src/superclaude/cli/install_mcp.py`.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/evidence.md`.

**Dependencies:** None
**Rollback:** Revert the package token and Tavily registry command changes.

### T01.02 -- Extract testable MCP add command builder

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | The stdio command grammar must be testable without invoking a live Claude CLI. |
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
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/evidence.md`

**Deliverables:**

- A pure helper or equivalent seam that builds `claude mcp add` argv.
- Tests or notes proving server-name/env/`--` command ordering.

**Steps:**

1. **[PLANNING]** Locate the inline command-building block in `install_mcp_server()`.
2. **[PLANNING]** Identify the current grammar invariant: server name before env flags, env flags before `--`, command after `--`.
3. **[EXECUTION]** Extract the argv-building logic into a helper that accepts `server_info`, `scope`, and env args.
4. **[EXECUTION]** Keep existing stdio behavior unchanged for all current servers.
5. **[VERIFICATION]** Add or prepare direct unit tests asserting the Tavily stdio argv ordering.
6. **[COMPLETION]** Document the helper contract in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/spec.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/src/superclaude/cli/install_mcp.py` exposes a testable command-builder seam for MCP add commands.
- The Tavily stdio argv places `tavily` before `-e`, `-e` before `--`, and `npx` after `--`.
- Existing non-Tavily stdio server command behavior is unchanged by the seam.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/spec.md` records the command grammar contract.

**Validation:**

- Manual check: inspect the helper output for a Tavily server-info fixture.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/evidence.md`.

**Dependencies:** T01.01
**Rollback:** Inline the helper logic back into `install_mcp_server()`.

### T01.03 -- Document remote HTTP as out of scope in installer comments

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | The merged requirements explicitly defer default remote HTTP/OAuth because it needs different CLI grammar and auth behavior. |
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
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/evidence.md`

**Deliverables:**

- Installer note or helper comment explaining that HTTP transport is not the default for Tavily in this upgrade.
- Future-work note covering positional URL grammar without implementing it.

**Steps:**

1. **[PLANNING]** Locate the command-builder helper or nearby install command comments.
2. **[PLANNING]** Confirm the note does not imply remote HTTP support is implemented.
3. **[EXECUTION]** Add concise documentation for the stdio default and remote HTTP deferral.
4. **[EXECUTION]** Ensure the note avoids recommending API-key query URLs as the default path.
5. **[VERIFICATION]** Confirm Tavily registry still uses local stdio after the note.
6. **[COMPLETION]** Record the out-of-scope statement in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/notes.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/src/superclaude/cli/install_mcp.py` contains an out-of-scope note for default remote HTTP Tavily behavior.
- The note states that remote HTTP needs separate command grammar or auth handling before becoming a default.
- The Tavily registry remains local stdio after the note is added.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/notes.md` records the future-work boundary.

**Validation:**

- Manual check: inspect the installer comments and Tavily registry entry.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/evidence.md`.

**Dependencies:** T01.02
**Rollback:** Remove the out-of-scope note.

### T01.04 -- Checkpoint: End of Phase 1

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Gate: verify outputs of tasks T01.01-T01.03 before continuing. |
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

**Checkpoint Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P01-END.md`

**Purpose:** Verify installer core changes are ready before migration and docs work.

**Verification:**

- Confirm D-0001 registry evidence exists.
- Confirm D-0002 command-builder contract exists.
- Confirm D-0003 remote HTTP boundary note exists.

**Exit Criteria:**

- Tavily package token is `tavily-mcp@latest`.
- Default Tavily transport remains `stdio`.
- Command-builder ordering invariant is documented.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for T01.01-T01.03.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P01-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T01.01-T01.03.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.03
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.05 -- Post-Execution Reflection: superclaude reflect run (wrapper shell-out)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003, R-011 |
| Why | Independent post-execution deviation audit of every task in Phase 1, run by the reflect wrapper after all phase work completes. |
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
| Deliverable IDs | D-RF01 |

**Reflect Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-1/REPORT.md`

**Gate Command:** `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-1-tasklist.md --depth deep --fix --no-promote --base <PHASE_1_START_SHA> --output /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-1/`

**Steps:**

1. **[VERIFICATION]** Resolve `<PHASE_1_START_SHA>` at execution time as a single ref for the phase start.
2. **[VERIFICATION]** Run the Gate Command above and consume its exit code.
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface deviation counts.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-1/REPORT.md` exists with a deviation-taxonomy summary.
- The wrapper exited `0`; exit `10`/`11`/`2` fails the gate and is surfaced.
- Reflect ran with executor-disjoint reviewers.
- Report includes the per-task verdict matrix for Phase 1.

**Validation:**

- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** T01.01..T01.04
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately)
