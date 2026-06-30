---
executor_model_class: "implementation"
start_commit: "<PHASE_3_START_SHA>"
---
# Phase 3 -- Docs & Config Convergence

Phase 3 aligns human-facing documentation and removes or neutralizes dormant Tavily config artifacts that contradict the live installer. It ensures future contributors see one package and transport policy.

### T03.01 -- Update Tavily user-guide documentation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Docs must show the same `tavily-mcp@latest` local stdio policy as the live installer. |
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
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/evidence.md`

**Deliverables:**

- Updated Tavily block in `docs/user-guide/mcp-servers.md`.
- Documentation of `tavily-search`, `tavily-extract`, `tavily-map`, and `tavily-crawl` expected tools.
- Remote HTTP/OAuth note as optional/future, not default.

**Steps:**

1. **[PLANNING]** Load the Tavily section of `docs/user-guide/mcp-servers.md`.
2. **[PLANNING]** Check the installer package token and default transport from Phase 1.
3. **[EXECUTION]** Update the Tavily example to use `tavily-mcp@latest` and `TAVILY_API_KEY` env.
4. **[EXECUTION]** Add map/crawl expected-tool verification guidance and remote HTTP optional note.
5. **[VERIFICATION]** Confirm no current doc recommendation points to `tavily-mcp@0.1.x`.
6. **[COMPLETION]** Record doc changes in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/evidence.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/docs/user-guide/mcp-servers.md` documents local stdio `tavily-mcp@latest` for Tavily.
- The same file names `tavily-map` and `tavily-crawl` as expected Tavily capabilities.
- The same file describes remote HTTP/OAuth as optional or future, not the default installer path.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/evidence.md` records the final Tavily doc block.

**Validation:**

- Manual check: inspect the Tavily block in `docs/user-guide/mcp-servers.md`.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/evidence.md`.

**Dependencies:** T01.01
**Rollback:** Revert the Tavily documentation edits.

### T03.02 -- Retire dormant Tavily JSON config artifacts

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | Dormant Tavily JSON files must not advertise a remote bridge form that the live Python installer does not load. |
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
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/evidence.md`

**Deliverables:**

- Removed or neutralized `src/superclaude/mcp/configs/tavily.json`.
- Removed or neutralized `plugins/superclaude/mcp/configs/tavily.json`.
- Evidence that no active code treats these configs as the Tavily source of truth.

**Steps:**

1. **[PLANNING]** Confirm whether packaging references either Tavily JSON config artifact.
2. **[PLANNING]** Choose deletion unless a packaging dependency requires neutralized replacement.
3. **[EXECUTION]** Delete both dormant Tavily JSON config files or rewrite them to match the live installer policy.
4. **[EXECUTION]** Ensure no remaining dormant config advertises `mcp-remote` Tavily as the live installer path.
5. **[VERIFICATION]** Run the config cleanup regression test from Phase 4.
6. **[COMPLETION]** Record the chosen treatment in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/notes.md`.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/src/superclaude/mcp/configs/tavily.json` is absent or matches the live stdio policy.
- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/plugins/superclaude/mcp/configs/tavily.json` is absent or matches the live stdio policy.
- No dormant Tavily config advertises `mcp-remote https://mcp.tavily.com` as the active individual-server install path.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/evidence.md` records the cleanup result.

**Validation:**

- Manual check: inspect the two Tavily config artifact paths.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/evidence.md`.

**Dependencies:** T03.01
**Rollback:** Restore the deleted JSON files from git and rewrite them consistently.

### T03.03 -- Add docs/config parity regression guard

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006, R-007 |
| Why | Tests must fail if docs, installer, or config artifacts drift on Tavily package/transport policy. |
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
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**

- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0009/spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0009/notes.md`
- `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0009/evidence.md`

**Deliverables:**

- Test that extracts Tavily package token from installer and docs.
- Test that checks dormant config artifacts are absent or consistent.
- Test that no active doc recommends `tavily-mcp@0.1.x`.

**Steps:**

1. **[PLANNING]** Identify parser strategy for extracting the Tavily package token from installer and docs.
2. **[PLANNING]** Define active vs historical paths excluded from stale-pin checks.
3. **[EXECUTION]** Add docs-installer parity assertions to the Tavily test module.
4. **[EXECUTION]** Add config cleanup assertions for both Tavily JSON artifact locations.
5. **[VERIFICATION]** Run `uv run pytest` on the Tavily parity tests.
6. **[COMPLETION]** Record test names and outcomes in `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0009/evidence.md`.

**Acceptance Criteria:**

- Test file under `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/tests/` asserts docs and installer agree on `tavily-mcp@latest`.
- Test file under `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/tests/` fails if active docs recommend `tavily-mcp@0.1.x`.
- Test file under `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/tests/` fails if dormant Tavily configs contradict the installer policy.
- Artifact `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0009/evidence.md` records the parity test run.

**Validation:**

- Manual check: reviewer confirms the parity tests cover docs and config cleanup.
- Evidence: linkable artifact produced at `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0009/evidence.md`.

**Dependencies:** T03.01, T03.02
**Rollback:** Remove the parity regression test additions.

### T03.04 -- Checkpoint: End of Phase 3

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | Gate: verify outputs of tasks T03.01-T03.03 before continuing. |
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

**Checkpoint Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P03-END.md`

**Purpose:** Verify docs and config sources no longer contradict the installer.

**Verification:**

- Confirm D-0007 docs evidence exists.
- Confirm D-0008 config cleanup evidence exists.
- Confirm D-0009 parity test evidence exists.

**Exit Criteria:**

- User guide shows `tavily-mcp@latest`.
- Dormant Tavily configs are absent or consistent.
- Parity tests cover docs and config drift.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for T03.01-T03.03.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P03-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T03.01-T03.03.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.01..T03.03
**Rollback:** N/A (checkpoints are read-only verifications)

### T03.05 -- Post-Execution Reflection: superclaude reflect run (wrapper shell-out)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006, R-007 |
| Why | Independent post-execution deviation audit of every task in Phase 3, run by the reflect wrapper after all phase work completes. |
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
| Deliverable IDs | D-RF03 |

**Reflect Report Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-3/REPORT.md`

**Gate Command:** `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi; superclaude reflect run /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-3-tasklist.md --depth deep --fix --no-promote --base <PHASE_3_START_SHA> --output /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-3/`

**Steps:**

1. **[VERIFICATION]** Resolve `<PHASE_3_START_SHA>` at execution time as a single ref for the phase start.
2. **[VERIFICATION]** Run the Gate Command above and consume its exit code.
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface deviation counts.

**Acceptance Criteria:**

- File `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/reflect-post/phase-3/REPORT.md` exists with a deviation-taxonomy summary.
- The wrapper exited `0`; exit `10`/`11`/`2` fails the gate and is surfaced.
- Reflect ran with executor-disjoint reviewers.
- Report includes the per-task verdict matrix for Phase 3.

**Validation:**

- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** T03.01..T03.04
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately)
