# MIG-002 — Eval-Batch Rollout Plan

| Field | Value |
|---|---|
| Roadmap item | R-103 / MIG-002 |
| Risk it mitigates | R9 — PR scope creep as evals are added |
| Owner task | T05.27 (phase-5-tasklist) |
| Status | Locked once Phase 5 closes (M5 exit gate). |
| Authoritative coverage gate | `src/superclaude/cli/eval/coverage.py` (`default_matcher_filter`, v1 prefixes `mcp__auggie__`, `mcp__auggie-mcp__`, `mcp__airis-mcp-gateway__`). |
| Suite manifest | `src/superclaude/cli/eval/suites/real.yaml` (17 enumerated entries: E1, E2.1, E2.2, E2.3, E3..E15 — published as "15 evals" per design-spec §5). |

## 1. PR ordering policy (R9 mitigation)

| PR | Scope | Lands |
|---|---|---|
| **PR 1 — Harness** | M1..M4 contract: schema + loader + models, isolation + PTY, runner + reporter, CLI surface + coverage-gate entry. **No eval bodies.** | First. Reviewers can validate the contract without paging in any eval. |
| **PR 2 — Batch A** | E1, E2.1, E2.2, E2.3 (MCP matcher coverage + sticky lifecycle). | After PR 1 merges. Unlocks FR-G5 green for v1 matcher families. |
| **PR 3 — Batch B** | E3, E4, E5 (Session/Prompt lifecycle hooks). | After PR 2 merges. |
| **PR 4 — Batch C** | E6, E7, E8 (PreToolUse tool-gate hooks). | After PR 2 merges (independent of Batch B). |
| **PR 5 — Batch D** | E9, E10, E11 (PostToolUse async + Subagent lifecycle). | After PR 2 merges (independent of B/C). |
| **PR 6 — Batch E** | E12, E13, E14, E15 (Hook resilience: deploy idempotency, fail-open, concurrency, timeout). | After PR 2 merges (independent of B/C/D). |

PRs 2-6 are independent once PR 1 lands; the order above is the recommended landing order, not a hard dependency chain. Each eval PR description **MUST** cite its batch's `coverage-map:` field verbatim from this file so reviewers can resolve the matcher / hook-event provenance without leaving the PR body.

## 2. Per-batch definition of done (DoD)

Every batch PR is mergeable iff **all** the following pass:

1. `uv run superclaude eval list --json` enumerates each new eval id in this batch.
2. `uv run superclaude eval run --suite real --eval <id>` exits 0 on a clean HOME for every eval in the batch.
3. Three consecutive runs of any one eval in the batch produce identical `EvalOutcome.status` (determinism check; FR-ISO2 + DM-008 serializable).
4. `uv run superclaude eval doctor --check-coverage` exits 0 against `~/.claude/settings.json` (no matcher family regressed).
5. Per-eval evidence saved under `TASKLIST_ROOT/evidence/T05.<NN>/` for each authoring task this PR closes.
6. PR description cites the batch's `coverage-map:` field **verbatim** from this file.

Batch-specific DoD additions are listed below each batch's coverage map.

---

## 3. Batch definitions

### Batch A — MCP matcher coverage + sticky lifecycle (PR 2)

| Eval | Title | Tool call exercised | Matcher family it clears |
|---|---|---|---|
| E1   | auggie-first sticky lifecycle — set then clear | `mcp__auggie__codebase-retrieval` | `mcp__auggie__*` |
| E2.1 | auggie matcher coverage — `mcp__auggie__*` | `mcp__auggie__codebase-retrieval` | `mcp__auggie__*` |
| E2.2 | auggie matcher coverage — `mcp__auggie-mcp__*` | `mcp__auggie-mcp__ask_question` | `mcp__auggie-mcp__*` |
| E2.3 | auggie matcher coverage — `mcp__airis-mcp-gateway__auggie_*` | `mcp__airis-mcp-gateway__auggie_search` | `mcp__airis-mcp-gateway__*` |

#### <a id="batch-a-coverage-map"></a>Batch A coverage map

- **coverage-map:** `docs/eval/mig-002-batch-plan.md#batch-a-coverage-map`
- **FR-G5 matcher families cleared by this batch:** `mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*` (all three v1 prefixes from `coverage.py::_DEFAULT_MCP_TOOL_PREFIXES`).
- **Suite source rows:** `src/superclaude/cli/eval/suites/real.yaml` E1 (line 43), E2.1 (line 79), E2.2 (line 111), E2.3 (line 142).
- **Hook telemetry asserted:** `state/auggie-first-pending/<sid>.txt` lifecycle + `logs/auggie-first.jsonl::sticky_cleared` (E1); per-matcher hook telemetry in per-eval JSONL (E2.1-3).
- **Capability gating:** all four soft-skip under `--no-mcp` with `skip_reason="capability_gate:<cap>"` (TEST-014 contract).

**Batch A DoD additions:**
- `uv run superclaude eval doctor --check-coverage` reports **3/3** v1 matcher families covered after this batch lands (before this batch: 0/3).
- `uv run superclaude eval run --suite real --no-mcp` classifies E1/E2.1/E2.2/E2.3 as `SKIPPED` with populated `skip_reason`.

---

### Batch B — Session / Prompt lifecycle hooks (PR 3)

| Eval | Title | Hook event |
|---|---|---|
| E3 | SessionStart unmatched (session-init) hook fires | `SessionStart` (no matcher) |
| E4 | SessionStart matcher=`*` freshness hook fires | `SessionStart` (`matcher: *`) |
| E5 | UserPromptSubmit freshness hook fires | `UserPromptSubmit` |

#### <a id="batch-b-coverage-map"></a>Batch B coverage map

- **coverage-map:** `docs/eval/mig-002-batch-plan.md#batch-b-coverage-map`
- **FR-G5 matcher families cleared:** none (these hooks have no `matcher:` field or the `*` wildcard, which `extract_hook_matchers` either skips or `default_matcher_filter` excludes — see `coverage.py` lines 188-198, 201-224).
- **Suite source rows:** `real.yaml` E3 (line 179), E4 (line 228), E5 (line 292).
- **Hook telemetry asserted:** SessionStart/UserPromptSubmit log lines in per-eval JSONL; freshness signal markers under per-eval HOME.
- **Capability gating:** no MCP requirement; `requires: []` — runs under `--no-mcp`.

**Batch B DoD additions:**
- E3/E4/E5 all run green with **and without** `--no-mcp` (no skip expected).

---

### Batch C — PreToolUse tool-gate hooks (PR 4)

| Eval | Title | Hook event / matcher |
|---|---|---|
| E6 | PreToolUse Edit matcher fires | `PreToolUse` matcher=`Edit` |
| E7 | PreToolUse Write matcher fires | `PreToolUse` matcher=`Write` |
| E8 | PreToolUse serena matcher fires | `PreToolUse` matcher=`mcp__serena__replace_content` (tool call `mcp__serena__replace_content`) |

#### <a id="batch-c-coverage-map"></a>Batch C coverage map

- **coverage-map:** `docs/eval/mig-002-batch-plan.md#batch-c-coverage-map`
- **FR-G5 matcher families cleared:** none in v1. E8's matcher targets `mcp__serena__*` which is **out of scope** for the v1 `default_matcher_filter` (only auggie/airis prefixes). E6/E7 target built-in tools (`Edit`, `Write`) which the gate explicitly excludes per `coverage.py` lines 188-198 ("matchers like `Edit|Write|...` are bookkeeping hooks").
- **Suite source rows:** `real.yaml` E6 (line 370), E7 (line 465), E8 (line 565).
- **Hook telemetry asserted:** PreToolUse JSONL events per matcher; for E8 the `mcp__serena__replace_content` invocation under a per-eval HOME with serena gated as `mcp_server.serena`.
- **Capability gating:** E6/E7 `requires: []`; E8 `requires: [mcp_server.serena]` — E8 soft-skips under `--no-mcp`.

**Batch C DoD additions:**
- `uv run superclaude eval run --suite real --no-mcp` shows E8 `SKIPPED` with `skip_reason=capability_gate:mcp_server.serena`; E6/E7 PASS.
- When MIG-002 follow-up extends `default_matcher_filter` to cover `mcp__serena__*`, E8 transitions from "informational" to "FR-G5-clearing" without a body change.

---

### Batch D — PostToolUse async + Subagent lifecycle (PR 5)

| Eval | Title | Hook event |
|---|---|---|
| E9  | PostToolUse Read async hook fires | `PostToolUse` matcher=`Read` (async) |
| E10 | SubagentStart hook fires | `SubagentStart` |
| E11 | SubagentStop hook fires | `SubagentStop` |

#### <a id="batch-d-coverage-map"></a>Batch D coverage map

- **coverage-map:** `docs/eval/mig-002-batch-plan.md#batch-d-coverage-map`
- **FR-G5 matcher families cleared:** none (Read is a built-in tool; Subagent* events don't carry MCP matchers).
- **Suite source rows:** `real.yaml` E9 (line 690), E10 (line 785), E11 (line 884).
- **Hook telemetry asserted:** async PostToolUse completion in per-eval JSONL (E9); Subagent lifecycle markers under per-eval HOME (E10/E11). E10/E11 verify the `Task` tool path triggers the matched hook.
- **Capability gating:** `requires: []` for all three; not gated by `--no-mcp`.

**Batch D DoD additions:**
- E9 asserts the **async** code path (hook returns before tool result is consumed); not just synchronous hook execution.
- E10/E11 assert telemetry correlates by sub-agent invocation id (no cross-contamination across parallel workers under `--parallel 8`).

---

### Batch E — Hook resilience (PR 6)

| Eval | Title | Resilience property |
|---|---|---|
| E12 | Hook deploy idempotency | Re-running `sync-dev` is a no-op when hooks are already installed (idempotent installer) |
| E13 | Hook stderr error fails open | Hook writing to stderr does not block the tool call |
| E14 | Concurrent SessionStart bursts | Parallel sessions don't corrupt per-session state files |
| E15 | Hook timeout fails open with telemetry | Slow hook is killed; tool call succeeds; telemetry records the timeout |

#### <a id="batch-e-coverage-map"></a>Batch E coverage map

- **coverage-map:** `docs/eval/mig-002-batch-plan.md#batch-e-coverage-map`
- **FR-G5 matcher families cleared:** none (these test hook *runtime* behavior, not matcher coverage).
- **Suite source rows:** `real.yaml` E12 (line 1014), E13 (line 1132), E14 (line 1292), E15 (line 1435).
- **Hook telemetry asserted:** deploy idempotency artifact diff (E12); fail-open exit + stderr captured in JSONL (E13/E15); concurrent session state file integrity (E14).
- **Capability gating:** `requires: []` for all four; not gated by `--no-mcp`.

**Batch E DoD additions:**
- E14 runs under `--parallel 8` and asserts no state-file collision across concurrent SessionStart bursts (NFR-REL1).
- E15 asserts hook timeout writes a `hook_timeout` artifact and the tool call exits 0 (fail-open invariant).

---

## 4. Coverage map index (reverse lookup)

For any eval id, look up its batch + coverage-map anchor:

| Eval | Batch | coverage-map field (paste verbatim into PR) |
|---|---|---|
| E1, E2.1, E2.2, E2.3 | A | `docs/eval/mig-002-batch-plan.md#batch-a-coverage-map` |
| E3, E4, E5 | B | `docs/eval/mig-002-batch-plan.md#batch-b-coverage-map` |
| E6, E7, E8 | C | `docs/eval/mig-002-batch-plan.md#batch-c-coverage-map` |
| E9, E10, E11 | D | `docs/eval/mig-002-batch-plan.md#batch-d-coverage-map` |
| E12, E13, E14, E15 | E | `docs/eval/mig-002-batch-plan.md#batch-e-coverage-map` |

## 5. Why these batches

- **Batch A is the v1-coverage-gate-clearing batch.** All three matcher families in `default_matcher_filter` are closed by E1 + E2.1-3, so PR 2 is the gate that unlocks "FR-G5 green" and lets every subsequent batch land against a non-empty coverage baseline. Sizing it at 4 evals keeps reviewer load proportional to its load-bearing role.
- **Batches B-E are partitioned by hook-event domain, not by author or by date**, so a reviewer can read each PR end-to-end without context from siblings: B is session/prompt entrypoints, C is the tool-call gate, D is the post-tool / sub-agent fanout, E is runtime robustness. Each batch lives in 3-4 evals (well inside the MIG-002 "3-5" envelope) and 1-3 hook events.
- **B/C/D/E are independent of each other.** Once Batch A merges, B/C/D/E can land in any order or in parallel reviewer streams without coverage-map collisions.
- **The 5-batch ceiling is held.** AC requires 3-5 batches; the plan uses exactly 5, leaving one slot of headroom for a "Batch F — coverage gate extension" follow-up (e.g., when `default_matcher_filter` grows beyond auggie/airis prefixes) without re-partitioning the existing roster.

## 6. References

- Roadmap: `.dev/releases/current/cliEval/roadmap.md` (R-103 MIG-002; R9 risk row).
- Design-spec: §1.5 (matcher coverage), §5 (eval roster).
- Coverage gate source: `src/superclaude/cli/eval/coverage.py`.
- Suite manifest: `src/superclaude/cli/eval/suites/real.yaml`.
- Capability-gate skip semantics (R9 cross-link): `.dev/releases/current/cliEval/artifacts/D-0103/spec.md` (TEST-014).
