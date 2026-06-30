# TASKLIST INDEX -- Tavily MCP Installer Upgrade

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Tavily MCP Installer Upgrade |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-06-22T23:31:36Z |
| TASKLIST_ROOT | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist` |
| Total Phases | 4 |
| Total Tasks | 20 |
| Total Deliverables | 12 |
| Complexity Class | MEDIUM |
| Reflect Pre Summary | `{pass: 0, partial: 0, fail: 0, skipped: 4}` |
| Primary Persona | backend |
| Consulting Personas | qa, refactorer, scribe |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/tasklist-index.md` |
| Phase 1 Tasklist | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-1-tasklist.md` |
| Phase 2 Tasklist | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-2-tasklist.md` |
| Phase 3 Tasklist | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-3-tasklist.md` |
| Phase 4 Tasklist | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-4-tasklist.md` |
| Execution Log | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/execution-log.md` |
| Checkpoint Reports | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/` |
| Evidence Directory | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/evidence/` |
| Artifacts Directory | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/` |
| Validation Reports | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/validation/` |
| Feedback Log | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution | Pre-Reflect Sign-off |
|---|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Installer Core | T01.01-T01.05 | STRICT: 1, STANDARD: 2, LIGHT: 1, EXEMPT: 1 | SKIPPED (artifact handoff only) |
| 2 | phase-2-tasklist.md | Migration & Redaction | T02.01-T02.05 | STRICT: 2, STANDARD: 1, LIGHT: 1, EXEMPT: 1 | SKIPPED (artifact handoff only) |
| 3 | phase-3-tasklist.md | Docs & Config Convergence | T03.01-T03.05 | STANDARD: 3, LIGHT: 1, EXEMPT: 1 | SKIPPED (artifact handoff only) |
| 4 | phase-4-tasklist.md | Tests & Verification | T04.01-T04.05 | STRICT: 1, STANDARD: 2, LIGHT: 1, EXEMPT: 1 | SKIPPED (artifact handoff only) |

## Source Snapshot

- Upgrade the live Tavily MCP installer from stale `tavily-mcp@0.1.2` to local stdio `tavily-mcp@latest`.
- Keep `TAVILY_API_KEY` env handling and `transport: stdio` as the default individual-server path.
- Do not switch default Tavily install to remote HTTP/OAuth in this change.
- Detect stale existing `tavily` installs instead of skipping them by name only.
- Reconcile docs and dormant config artifacts so they no longer contradict the live installer.
- Add unit/regression tests for package token, stale migration, docs parity, redaction, command grammar, and optional map/crawl verification.

## Deterministic Rules Applied

- Phases were derived from requirement clusters in the merged requirements.
- Task IDs use `T<PP>.<TT>` zero-padded phase/task numbering.
- Each regular task maps to at least one `R-###` roadmap item and one `D-####` deliverable.
- Checkpoints are emitted as numbered tasks and produce `D-CP<PP>` deliverables.
- Post-execution reflection tasks are terminal EXEMPT tasks with `D-RF<PP>` deliverables.
- Effort, risk, tier, confidence, verification method, and MCP requirements are included for every task.
- Validation commands use UV for Python test execution.
- The tasklist root is the explicit handoff output directory supplied by `/sc:brainstorm --handoff tasklist`.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Installer Core | Update live Tavily package spec from stale 0.1.2 to latest. |
| R-002 | Installer Core | Keep local stdio as default transport. |
| R-003 | Installer Core | Add testable MCP add command builder seam. |
| R-004 | Migration & Redaction | Add stale Tavily install reconciliation. |
| R-005 | Migration & Redaction | Redact API key values in displayed commands. |
| R-006 | Docs & Config | Reconcile docs with installer policy. |
| R-007 | Docs & Config | Retire dormant divergent Tavily config artifacts. |
| R-008 | Tests & Verification | Add map/crawl tool-surface verification. |
| R-009 | Tests & Verification | Add unit/regression tests covering version, migration, docs parity, redaction, config cleanup, command grammar. |
| R-010 | Migration & Redaction | Preserve back-compat for no install, stale install, current install, AIRIS gateway, and missing API key states. |
| R-011 | Installer Core | Remote HTTP remains future or optional work only. |
| R-012 | Tests & Verification | Unit tests must not require live Claude CLI, Node network install, or Tavily API key. |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001,R-002 | Centralized Tavily package token and registry update | STRICT | Sub-agent quality check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/spec.md` | M | Medium |
| D-0002 | T01.02 | R-003 | Testable MCP add command builder seam | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/spec.md` | M | Low |
| D-0003 | T01.03 | R-011 | Explicit remote HTTP non-goal note | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/spec.md` | S | Low |
| D-0004 | T02.01 | R-004,R-010 | Stale Tavily reconciliation flow | STRICT | Sub-agent quality check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/spec.md` | L | High |
| D-0005 | T02.02 | R-005 | Redacted command display helper | STRICT | Sub-agent quality check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/spec.md` | M | Medium |
| D-0006 | T02.03 | R-010 | Back-compat behavior matrix | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0006/spec.md` | S | Low |
| D-0007 | T03.01 | R-006 | User-guide Tavily docs update | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/spec.md` | S | Low |
| D-0008 | T03.02 | R-007 | Dormant Tavily config retirement | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/spec.md` | S | Low |
| D-0009 | T03.03 | R-006,R-007 | Docs/config parity regression guard | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0009/spec.md` | M | Low |
| D-0010 | T04.01 | R-009,R-012 | Tavily installer unit/regression suite | STRICT | Sub-agent quality check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/spec.md` | L | Medium |
| D-0011 | T04.02 | R-008 | Optional map/crawl integration smoke | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/spec.md` | M | Low |
| D-0012 | T04.03 | R-009 | Validation command and sync checklist | STANDARD | Direct test execution | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0012/spec.md` | S | Low |
| D-CP01 | T01.04 | R-003 | End-of-phase checkpoint report | LIGHT | Quick sanity check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P01-END.md` | XS | Low |
| D-CP02 | T02.04 | R-010 | End-of-phase checkpoint report | LIGHT | Quick sanity check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P02-END.md` | XS | Low |
| D-CP03 | T03.04 | R-007 | End-of-phase checkpoint report | LIGHT | Quick sanity check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P03-END.md` | XS | Low |
| D-CP04 | T04.04 | R-009 | End-of-phase checkpoint report | LIGHT | Quick sanity check | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/CP-P04-END.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | STRICT | [█████████-] 90% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/spec.md` |
| R-002 | T01.01 | D-0001 | STRICT | [█████████-] 90% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0001/spec.md` |
| R-003 | T01.02,T01.04 | D-0002,D-CP01 | STANDARD | [████████--] 85% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0002/spec.md` |
| R-004 | T02.01 | D-0004 | STRICT | [█████████-] 90% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/spec.md` |
| R-005 | T02.02 | D-0005 | STRICT | [█████████-] 90% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0005/spec.md` |
| R-006 | T03.01,T03.03 | D-0007,D-0009 | STANDARD | [████████--] 85% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0007/spec.md` |
| R-007 | T03.02,T03.04 | D-0008,D-CP03 | STANDARD | [████████--] 85% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0008/spec.md` |
| R-008 | T04.02 | D-0011 | STANDARD | [████████--] 85% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0011/spec.md` |
| R-009 | T04.01,T04.03,T04.04 | D-0010,D-0012,D-CP04 | STRICT | [█████████-] 90% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/spec.md` |
| R-010 | T02.01,T02.03,T02.04 | D-0004,D-0006,D-CP02 | STRICT | [█████████-] 90% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0004/spec.md` |
| R-011 | T01.03 | D-0003 | STANDARD | [████████--] 85% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0003/spec.md` |
| R-012 | T04.01 | D-0010 | STRICT | [█████████-] 90% | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/artifacts/D-0010/spec.md` |

## Execution Log Template

**Intended Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | Manual | TBD | `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/evidence/` |

## Checkpoint Report Template

**Template:**

- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status`
  - `Overall: Pass | Fail | TBD`
- `## Verification Results`
  - `<exact verification result 1>`
  - `<exact verification result 2>`
  - `<exact verification result 3>`
- `## Exit Criteria Assessment`
  - `<exact exit criterion 1>`
  - `<exact exit criterion 2>`
  - `<exact exit criterion 3>`
- `## Issues & Follow-ups`
  - `List blocking issues; reference T<PP>.<TT> and D-####`
- `## Evidence`
  - `Bullet list of intended evidence paths under /config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/evidence/`

## Feedback Collection Template

**Intended Path:** `/config/workspace/IronClaude/.dev/worktrees/TavilyUpgrade/.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| TBD | TBD |  |  | TBD | TBD | TBD |

## Generation Notes

- The explicit `--output` directory was used as `TASKLIST_ROOT` for this brainstorm handoff.
- Pre-reflect execution is recorded as skipped because this handoff produced planning artifacts only; phase files still include terminal post-execution reflection tasks for execution-time gating.
