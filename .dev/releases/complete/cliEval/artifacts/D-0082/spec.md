# D-0082 — OQ-2 Resolution: E3–E15 Eval Body Shapes (Frozen)

**Deliverable ID:** D-0082
**Task ID:** T05.01 (Phase 5)
**Roadmap items:** R-086 … R-098
**Resolution status:** 🟢 RESOLVED — RyanW — 2026-05-20 (sign-off landed at T06.09 / R12 in the SC5 single-sweep pass; see decisions.md §"OQ-2 Resolution" and §"SC5 OQ resolution ledger (T06.09)" → OQ-2 row)
**Date proposed:** 2026-05-20
**Date resolved:** 2026-05-20
**Stakeholder:** RyanW

---

## 1. Purpose

OQ-2 (roadmap.md:110) asks: *"Concrete content of E3–E15 manifest entries."*
The design-spec (§5) shows only E1 and E2 parameterize as exemplars; E3–E15 are deferred.

This spec freezes the **inputs, expects, and capability tags** for each of the 13 remaining bodies so that T05.07 … T05.21 may author them without further design churn.

## 2. Design constraints

1. **Coverage:** every hook event type in `src/superclaude/hooks/hooks.json` MUST be exercised by ≥1 eval among {E1, E2.1–3, E3 … E15}.
2. **Determinism:** every body MUST pass deterministically on a clean per-eval HOME (FR-ISO2) — no time-of-day, no network, no shared mutable state. (3-run determinism is the per-task AC.)
3. **No OQ-8 dependency:** E3–E15 MUST NOT require `CLAUDE_FAKE_TIME_OFFSET`. The original design-spec note tying E3 to "30-min freshness tests" is **superseded**; freshness-staleness via time offset is deferred until OQ-8 closes (separate follow-up).
4. **Expect.* primitive only:** every body's assertions MUST be expressible via the v1 DSL (`file.exists`, `file.absent`, `jsonl.contains_event`, `jsonl.event_count`, `settings_json.has_registration`, `exit_code.equals`, `stderr.contains`, `stdout.contains`, `duration.less_than`, `duration.greater_than`) plus the YAML `callback:` escape (D-4) for E14.
5. **Capability gating:** evals requiring a live MCP server soft-skip under `--no-mcp` with `skip_reason` populated (FR-CAP1).

## 3. Hook surface coverage map

| Hook event (hooks.json) | Matcher | Hook script | Covered by |
|---|---|---|---|
| `SessionStart` (1st) | (none) | `session-init.sh` | **E3** |
| `SessionStart` (2nd) | `*` | `freshness-session-start.sh` | **E4** |
| `UserPromptSubmit` | (none) | `freshness-user-prompt.sh` | **E5** |
| `PreToolUse` | `Edit\|Write\|mcp__serena__*` | `freshness-pre-edit.sh` | **E6** (Edit), **E7** (Write), **E8** (serena) |
| `PostToolUse` | `Read` (async) | `freshness-post-read.sh` | **E9** |
| `PostToolUse` | `mcp__auggie__\|mcp__auggie-mcp__\|mcp__airis-mcp-gateway__auggie_` | `auggie-flag-clear.sh` | **E1, E2.1, E2.2, E2.3** (existing) |
| `SubagentStart` | (none) | `freshness-subagent-start.sh` | **E10** |
| `SubagentStop` | (none) | `freshness-subagent-stop.sh` | **E11** |
| Cross-cutting: deploy idempotency | — | `install_hooks` adapter | **E12** |
| Cross-cutting: stderr fail-open | — | error path | **E13** |
| Cross-cutting: concurrency | — | N parallel sessions | **E14** (YAML callback per D-4) |
| Cross-cutting: timeout fail-open | — | `timeout:` field in hooks.json | **E15** (named in design-spec §11) |

Net: 100% v1 hook-event coverage; 100% v1 PreToolUse matcher coverage; 100% v1 PostToolUse matcher coverage; cross-cutting fail-mode + concurrency tests included.

## 4. Frozen body shapes

The body shape for each eval is `(inputs, expects, capability_tags)`. Capability tags map to FR-CAP1 gates; `[]` means no capability gate (always runs).

### E3 — SessionStart unmatched (session-init) hook fires

| Field | Value |
|---|---|
| **Inputs** | spawn a fresh claude session via `PtyDriver.spawn(home=isolated)`; wait for prompt-ready. |
| **Expects** | `file.exists(state/session-init.log)` (script writes its own log); `jsonl.contains_event(logs/session-events.jsonl, type=session_init)`; `exit_code.equals(0)` (session exits cleanly on `/quit`). |
| **Capability tags** | `[]` (no MCP; no network) |
| **Notes** | Verifies the matcher-less first-position SessionStart hook fires before the matcher=* hook. Determinism: every spawn writes a new session log. |

### E4 — SessionStart matcher=* freshness hook fires

| Field | Value |
|---|---|
| **Inputs** | spawn a fresh claude session; wait for prompt-ready; `/quit`. |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=session_start)`; `jsonl.event_count(logs/freshness.jsonl, type=session_start) == 1`. |
| **Capability tags** | `[]` |
| **Notes** | Verifies the SECOND SessionStart hook (matcher=*) also fires. E3 covers position 0; E4 covers position 1. |

### E5 — UserPromptSubmit freshness hook fires

| Field | Value |
|---|---|
| **Inputs** | spawn session; `inject_prompt("echo test")`; observe pre-prompt hook output. |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=user_prompt)`; `jsonl.event_count(logs/freshness.jsonl, type=user_prompt) >= 1` per injected prompt. |
| **Capability tags** | `[]` |
| **Notes** | Time-offset-free: simply asserts the hook fires once per prompt submission. OQ-8-dependent staleness test is a follow-up eval. |

### E6 — PreToolUse Edit matcher fires

| Field | Value |
|---|---|
| **Inputs** | spawn session; inject prompt that triggers a single `Edit` tool call on a scratch file. |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=pre_edit, matcher=Edit)`; `file.exists(<scratch>/edited.txt)`. |
| **Capability tags** | `[]` |
| **Notes** | Asserts the Edit branch of the `Edit\|Write\|mcp__serena__*` matcher resolves. |

### E7 — PreToolUse Write matcher fires

| Field | Value |
|---|---|
| **Inputs** | spawn session; inject prompt triggering a single `Write` tool call to a scratch file. |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=pre_edit, matcher=Write)`; `file.exists(<scratch>/written.txt)`. |
| **Capability tags** | `[]` |
| **Notes** | Asserts the Write branch of the PreToolUse matcher. |

### E8 — PreToolUse serena matcher fires

| Field | Value |
|---|---|
| **Inputs** | spawn session; inject prompt triggering `mcp__serena__replace_content` on a scratch file (or other `mcp__serena__*` variant in the matcher). |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=pre_edit, matcher=mcp__serena__*)`; `file.exists(<scratch>/modified.txt)`. |
| **Capability tags** | `[mcp_server.serena]` — soft-skip under `--no-mcp` or if serena unreachable. |
| **Notes** | Completes PreToolUse matcher coverage (Edit, Write, serena). |

### E9 — PostToolUse Read async hook fires

| Field | Value |
|---|---|
| **Inputs** | spawn session; inject prompt triggering a single `Read` of a fixture file; wait for async hook to flush. |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=post_read)`; `duration.less_than(post_read_event_ts - read_complete_ts, 2.0)` (async hook flushes within 2s). |
| **Capability tags** | `[]` |
| **Notes** | Exercises the `async: true` branch — distinct from synchronous matchers. |

### E10 — SubagentStart hook fires

| Field | Value |
|---|---|
| **Inputs** | spawn session; inject prompt that invokes a sub-agent (e.g., Explore or Plan). |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=subagent_start)`; `jsonl.event_count(logs/freshness.jsonl, type=subagent_start) >= 1`. |
| **Capability tags** | `[]` |
| **Notes** | Verifies SubagentStart event hook wiring. |

### E11 — SubagentStop hook fires

| Field | Value |
|---|---|
| **Inputs** | spawn session; invoke sub-agent (as in E10); allow it to complete; wait for stop hook flush. |
| **Expects** | `jsonl.contains_event(logs/freshness.jsonl, type=subagent_stop)`; `jsonl.event_count(logs/freshness.jsonl, type=subagent_start) == jsonl.event_count(logs/freshness.jsonl, type=subagent_stop)` (paired). |
| **Capability tags** | `[]` |
| **Notes** | Pairs with E10 to assert start↔stop event symmetry. |

### E12 — Hook deploy idempotency

| Field | Value |
|---|---|
| **Inputs** | call `install_hooks` adapter against the per-eval HOME twice in a row (back-to-back invocations). |
| **Expects** | `settings_json.has_registration(<all hook events>, <all matchers>)` after first deploy AND after second deploy; settings.json file digest unchanged between the two deploys (no duplicate entries); `exit_code.equals(0)` both times. |
| **Capability tags** | `[]` |
| **Notes** | Asserts the install_hooks adapter is idempotent — the regression class for PR #49-style "matcher exists but second deploy duplicates it" bugs. |

### E13 — Hook stderr error fails open

| Field | Value |
|---|---|
| **Inputs** | spawn session with a hooks.json variant where one PostToolUse hook script returns non-zero exit + stderr (simulated via a fixture script in `tests/fixtures/hooks/failing-post-read.sh`); inject prompt triggering a Read. |
| **Expects** | tool call completes successfully (`exit_code.equals(0)` for the Read tool); `stderr.contains(failing_hook_script_name)`; `jsonl.contains_event(logs/hook-errors.jsonl, type=hook_error, disposition=fail_open)`. |
| **Capability tags** | `[]` |
| **Notes** | Asserts the harness records hook errors without blocking the tool call. Regression class for "hook stderr causes apparent tool failure" bugs. |

### E14 — Concurrent SessionStart bursts

| Field | Value |
|---|---|
| **Inputs** | YAML `callback:` field invokes `superclaude.cli.eval.suites.real_callbacks:E14_concurrent_session_start` (per D-4 escape hatch). The callback spawns N=3 sessions in rapid succession (within ~200ms of each other) via threads. |
| **Expects** | each session writes its own `state/auggie-first-pending/<sid>.txt` (no cross-contamination); 3 distinct session_init events in 3 separate JSONL files (one per session HOME); `jsonl.event_count == 1` per session. |
| **Capability tags** | `[]` |
| **Notes** | Tests no-shared-mutable-state at SessionStart concurrency boundary. Uses the YAML callback escape hatch from D-4 (programmatic spawn ordering can't be expressed in declarative YAML). |

### E15 — Hook timeout fail-open

| Field | Value |
|---|---|
| **Inputs** | spawn session with a hooks.json variant where one PostToolUse hook is a fixture script (`tests/fixtures/hooks/slow-post-read.sh`) that sleeps longer than the configured `timeout:` field; inject prompt triggering a Read. |
| **Expects** | tool call completes successfully (`exit_code.equals(0)`); `duration.less_than(hook_timeout + 2.0)` (harness reaps the slow hook); `jsonl.contains_event(logs/hook-errors.jsonl, type=hook_timeout, disposition=fail_open)`. |
| **Capability tags** | `[]` |
| **Notes** | The named failing-case demo from design-spec §11 ("E15 hook timeout fail-open"). Asserts the harness's timeout-reaping behavior matches the documented fail-open contract. |

## 5. Schema impact

All 13 bodies above are expressible under the existing `suites/suite.schema.json` (D-4) without schema extensions. E14 uses the existing `callback:` field. No schema-version bump required.

## 6. Capability-tag rollup

| Eval | Capability tag(s) | Soft-skip under `--no-mcp`? |
|---|---|---|
| E1 (existing) | `mcp_server.auggie` | yes |
| E2.1 (existing) | `mcp_server.auggie` | yes |
| E2.2 (existing) | `mcp_server.auggie-mcp` | yes |
| E2.3 (existing) | `mcp_server.airis-mcp-gateway` | yes |
| E3 | — | no |
| E4 | — | no |
| E5 | — | no |
| E6 | — | no |
| E7 | — | no |
| E8 | `mcp_server.serena` | yes |
| E9 | — | no |
| E10 | — | no |
| E11 | — | no |
| E12 | — | no |
| E13 | — | no |
| E14 | — | no |
| E15 | — | no |

**Net under `--no-mcp`:** E1, E2.1, E2.2, E2.3, E8 SKIPPED (5 evals); E3, E4, E5, E6, E7, E9, E10, E11, E12, E13, E14, E15 RUN (12 evals). `counts.kept_plus_skipped_equals_n_prime` invariant preserved (17 + parameterize expansion).

## 7. Impacts list (downstream tasks unblocked)

This resolution unblocks the following 13 authoring tasks (phase-5-tasklist.md):

| Task | Eval | Roadmap |
|---|---|---|
| T05.07 | E3 | R-086 |
| T05.08 | E4 | R-087 |
| T05.09 | E5 | R-088 |
| T05.10 | E6 | R-089 |
| T05.11 | E7 | R-090 |
| T05.13 | E8 | R-091 |
| T05.14 | E9 | R-092 |
| T05.15 | E10 | R-093 |
| T05.16 | E11 | R-094 |
| T05.17 | E12 | R-095 |
| T05.19 | E13 | R-096 |
| T05.20 | E14 | R-097 |
| T05.21 | E15 | R-098 |

All 13 tasks remain BLOCKED on T05.01 sign-off until status flips from PROPOSED → RESOLVED below.

## 8. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟠 PROPOSED | — | 2026-05-20 |
| 🟢 RESOLVED | RyanW | 2026-05-20 |

**Sign-off line:** *RyanW — approved 2026-05-20 — OQ-2 resolved. E3..E15 body shapes frozen per D-0082/spec.md.* Approval landed in lockstep with the T06.09 SC5 single-sweep sign-off pass (decisions.md R12). T05.07..T05.21 (13 authoring tasks) unblocked.
