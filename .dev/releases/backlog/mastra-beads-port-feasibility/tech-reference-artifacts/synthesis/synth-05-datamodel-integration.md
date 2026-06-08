# Synthesis 05 — Sections 6, 7, 8 (State & Data Model · Contract & Workflow Inventory · API & Integration)

**Target document:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture — Technical Reference
**Template sections covered:** §6 (repurposed), §7 (repurposed), §8
**Status:** In Progress
**HEAD verified against:** `9e864860`
**Evidence index:** `.dev/tasks/to-do/TASK-TECHREF-20260603-021348/research/00-evidence-index.md`

> **Tag legend (R2 — built-vs-design demarcation):**
> `[CODE-VERIFIED]` — existing Python in `src/superclaude/` at HEAD `9e864860`, with real `path:line`.
> **Path-root convention:** bare `pipeline/…`, `sprint/…`, `roadmap/…`, `tasklist/…` paths are relative to `src/superclaude/cli/` (e.g. `pipeline/models.py` resolves to `src/superclaude/cli/pipeline/models.py`), matching the evidence index.
> `[DESIGN — UNBUILT]` — proposed hybrid architecture; **not implemented in the repo today.**
> `[EXTERNAL-VERIFIED]` — Mastra / Backlog.md / Beads / MCP capability confirmed via web research (web-01..04) with source URLs.
> No source file in the repo implements any Mastra / Backlog.md / Beads integration today (evidence `5.6-27`, `[DESIGN — UNBUILT]`).

---

## 6. State & Data Model

> **REPURPOSE NOTE (Section 6):** The template's Section 6 is "State Management (frontend / client-side state)." This is a backend orchestration architecture with no client-side state, so Section 6 is **repurposed to "State & Data Model."** It documents (a) the `[CODE-VERIFIED]` state and data contracts that exist today in the Python pipeline/sprint runtime, and (b) the `[DESIGN — UNBUILT]` ownership split across Mastra / Backlog.md / Beads that the proposed hybrid would impose on that same state. Subsections are remapped: 6.1 State Architecture & Ownership · 6.2 State Shape (current models) · 6.3 Key State Transitions & Status Enums · 6.4 Cross-Store Dependencies (proposed ownership boundaries).

### 6.1 State Architecture & Ownership

Today, all orchestration state lives in two physical tiers: **runtime Python dataclasses** (constructed by the runner, not self-reported by the agent) and **durable filesystem artifacts** (markdown task files, JSONL logs, result/checkpoint reports). The proposed hybrid does not collapse these into one store; it assigns each existing concept a single primary owner across three external substrates.

| State / data class | Current owner (today) | Tier | Proposed primary owner | Tag |
|--------------------|-----------------------|------|------------------------|-----|
| Human task body / AC / checklist / decisions | `.dev/tasks` + tasklist markdown (`templates/workflow/02_mdtm_template_complex_task.md:1-44`) | Durable file | Backlog.md | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-12`) |
| Machine dependency graph (`depends_on`, `T<PP>.<TT>` edges) | Markdown frontmatter + `**Dependencies:**` text (`sprint/config.py:379-384`) | Durable file | Beads (graph mirror) | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-12`) |
| Workflow run state, retries, step status, traces | Python dataclasses + process outputs (`pipeline/models.py`, `sprint/models.py`) | Runtime | Mastra (run/trace) | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-12`) |
| Execution logs, checkpoint reports, validation reports | Files under release/task dir (`sprint/models.py:473-510`) | Durable file | Backlog.md docs + Mastra trace refs | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-07`) |
| High-volume telemetry (`MonitorState`) | Sprint monitor runtime (`sprint/models.py:623-690`) | Runtime | Mastra observability (summaries only to Backlog/Beads) | `[CODE-VERIFIED]` (`5.5-08`) |
| Budget / cost ledger (`TurnLedger`) | Sprint runtime, sprint-local (`sprint/models.py:693-777`) | Runtime | Governance/control-plane service (insufficient in current model) | `[CODE-VERIFIED]` (`5.5-09`) |
| Stable IDs (`TASK-*`, `T<PP>.<TT>`, `D-####`, `D-CP...`, `R-###`) | Markdown / tasklist generator (`sc-tasklist-protocol/SKILL.md:161-164`) | Durable file | Cross-system sync key; Backlog.md assigns canonical | `[CODE-VERIFIED]` IDs (`5.5-04`); `[DESIGN — UNBUILT]` owner |
| Tenant / actor / audit identity | **Absent** from scoped models (`PipelineConfig`/`SprintConfig`/`TaskResult`/`MonitorState`/`TurnLedger` carry model/permission/budget but no tenant/actor) | — | Must be **added** (governance plane) | `[CODE-VERIFIED]` (absence) (`5.5-15`, `5.8-13`) |

> **Important:** Tenant/actor/audit identity is a verified *absence* in current scoped models, not a field to repoint. The proposed governance plane adds it; it is not assumed to already exist.

**Ownership rules the proposed design preserves** `[DESIGN — UNBUILT]` (`5.5-13`): one prose owner (Backlog.md), one graph owner (Beads), one run owner (Mastra), stable IDs preserved verbatim and never regenerated on import/export, and checkpoint reports remain linkable artifacts (the checkpoint *task node* and the checkpoint *report body* must not be conflated).

### 6.2 State Shape (Current Models — `[CODE-VERIFIED]`)

> Per template content rules: state shape is summarized as a table of key fields + notable behavior, not reproduced as full dataclass source. All rows `[CODE-VERIFIED]` at HEAD `9e864860`.

| Model | Key fields | Notable behavior | `path:line` |
|-------|-----------|------------------|-------------|
| `Step` | id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path | Core portable workflow-step unit; framework-neutral | `pipeline/models.py:108-123` (`5.1-07`, `5.5-05`) |
| `StepResult` | step pointer (optional), status, attempt, gate_failure_reason, timestamps, remediation metadata, computed duration | Runner-constructed; `step` is optional (state-build risk) | `pipeline/models.py:125-148` (`5.1-08`) |
| `TaskEntry` | task_id, title, description, dependencies, command, classifier | Stores deps but does **not** schedule by dependency order — preserves file order | `sprint/models.py:24-37` (`5.3-07`) |
| `TaskResult` | status, turns, exit_code, timing, output_bytes, gate outcome, reimbursement, output_path | Runner-constructed, **not** agent self-reported | `sprint/models.py:158-209` (`5.3-08`) |
| `CheckpointEntry` | phase, name, expected_path, exists, recovered, recovery_source | Backed by checkpoint report-path conventions on disk | `sprint/models.py:311-341` (`5.5-10`) |
| `MonitorState` | bytes, last event/growth times, activity log, turns, errors, assistant text, task progress, token counts | High-volume telemetry → belongs in tracing layer, not task-of-record | `sprint/models.py:622-690` (`5.5-08`) |
| `TurnLedger` | initial_budget, consumed, reimbursed, reimbursement_rate, minimum_allocation, remediation + wiring budgets | Sprint-local; insufficient for multi-tenant governance | `sprint/models.py:692-777` (`5.3-17`, `5.5-09`) |

### 6.3 Key State Transitions & Status Enums (Current — `[CODE-VERIFIED]`)

The status enums below are the authoritative lifecycle vocabulary the proposed Mastra run-status / Backlog status / Beads status mappings must round-trip without lossy normalization.

| Enum | Values | `path:line` |
|------|--------|-------------|
| `StepStatus` | PENDING, PASS, FAIL, TIMEOUT, CANCELLED, SKIPPED (`is_failure` true only for FAIL + TIMEOUT) | `pipeline/models.py:40-67` (`5.1-03`) |
| `TaskStatus` | PASS, FAIL, INCOMPLETE, SKIPPED | `sprint/models.py:39-54` (`5.5-06`) |
| `GateOutcome` | PASS, FAIL, DEFERRED, PENDING (+ display: CHECKING, FAIL_DEFERRED, REMEDIATING, REMEDIATED, HALT) | `sprint/models.py:56-124` (`5.5-06`) |
| `PhaseStatus` | 11 values: PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, PASS_MISSING_CHECKPOINT, INCOMPLETE, HALT, TIMEOUT, ERROR, SKIPPED | `sprint/models.py:211-270` (`5.3-09`) |
| `SprintOutcome` | SUCCESS, HALTED, INTERRUPTED, ERROR | `sprint/models.py:272-279` (`5.5-06`) |

**Proposed mapping of these transitions onto the hybrid** `[DESIGN — UNBUILT]` (`5.5-12`, Contract 4): a Mastra run emits step/run terminal states; an idempotent reconciliation adapter projects them to Backlog.md (human status + execution-log summary) and Beads (normalized graph status / blocker edges). The reconciliation must be idempotent — re-running the same Mastra result event must not duplicate Backlog log rows or Beads edges (`5.5-14`).

### 6.4 Cross-Store Dependencies (Proposed Ownership Boundaries — `[DESIGN — UNBUILT]`)

| Source store | Consumer store | Relationship | Boundary rule | Tag |
|--------------|----------------|--------------|---------------|-----|
| Backlog.md (prose + IDs) | Beads (graph) | Backlog/tasklist → Beads upsert by stable ID | Backlog wins for existence/title/body; Beads owns status only if explicitly configured | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Backlog.md + Beads | Mastra (run plan) | Read for deterministic dry-run workflow plan | Plan must be deterministic from Backlog + Beads before any side effect | `[DESIGN — UNBUILT]` (Contract 3) |
| Mastra (run results) | Backlog.md + Beads | Mastra → summaries/status updates | Idempotent; telemetry stays in Mastra traces, not Backlog/Beads bodies | `[DESIGN — UNBUILT]` (`5.5-14`, Contract 4) |
| Beads graph | Sprint execution order | Graph would drive scheduling | **Behavioral change:** today markdown tasklists are *ordered records*, sprint parses deps but executes in document order (`5.7-31`); making Beads `bd ready` authoritative changes execution semantics, not just storage | `[CODE-VERIFIED]` current behavior + `[DESIGN — UNBUILT]` change (`5.7-31`) |

> **CRITICAL:** Adopting Beads `bd ready` as the scheduler is a behavioral change, not a runtime swap. Current sprint execution is document-order (`sprint/config.py:379-384`, `executor.py:971-1010`, `5.7-31`); a dependency-graph scheduler can reorder execution. Round-trip parser-compatibility tests (`discover_phases()`, `parse_tasklist_file()`, task-count and dependency equality) are the proposed acceptance gate before any ownership transfer (`5.5-14`).

---

## 7. Contract & Workflow Inventory

> **REPURPOSE NOTE (Section 7):** The template's Section 7 is "Component Inventory (frontend component tree + component catalog)." This architecture has no React/UI component tree, so Section 7 is **repurposed to "Contract & Workflow Inventory."** In place of a component tree it inventories (a) the `[CODE-VERIFIED]` pipeline/runtime contracts that exist today and that any port must preserve, and (b) the four `[DESIGN — UNBUILT]` adapter contracts the proposed hybrid introduces. 7.1 replaces the component tree with a contract-dependency diagram; 7.2 replaces the component catalog with the existing-contract inventory; 7.3 replaces "shared/reusable components" with the proposed adapter-contract inventory.

### 7.1 Contract Dependency Map (replaces Component Tree)

```
[Existing — CODE-VERIFIED]                         [Proposed — DESIGN/UNBUILT]
                                                    
 pipeline/models.py  (framework-neutral contracts)
   ├── Step / StepResult / StepStatus / GateMode
   ├── GateCriteria / SemanticCheck
   ├── Deliverable / DeliverableKind
   └── PipelineConfig + CosmeticRemediator proto
            │
            ▼
 pipeline/executor.py  execute_pipeline()
   └── StepRunner protocol  ◄─── process boundary ───►  ClaudeProcess (pipeline/process.py)
            │                                                   │
   ┌────────┼──────────┬───────────┐                           │  Contract 3
   ▼        ▼          ▼            ▼                           ▼  Backlog+Beads → Mastra plan
 roadmap  tasklist   sprint     trailing_gate            ┌─────────────────────┐
 executor executor   executor   (deferred remediation)   │  Adapter Layer      │
   (shared execute_pipeline + injected run_step)          │  C1 tasklist→Backlog│
            │                                              │  C2 Backlog/TL→Beads│
            ▼                                              │  C3 →Mastra plan    │
 sprint/config.py  parse_tasklist  (strict parser)  ◄──── │  C4 Mastra→reconcile│
   T<PP>.<TT> headings · Dependencies · Command · CP       └─────────────────────┘
                                                            round-trip parser tests = acceptance gate
```

> **Note:** The single migration seam is `ClaudeProcess` + `StepRunner` / `execute_pipeline`; gate, model, deliverable and diagnostic logic is runtime-agnostic pure Python and therefore highly portable (`5.1-13`, `5.7-29`, `5.7-30`).

### 7.2 Existing Contract Inventory (`[CODE-VERIFIED]`)

These are the contracts a hybrid port must preserve. All rows `[CODE-VERIFIED]` at HEAD `9e864860`.

| Contract | Role | Key signature / shape | `path:line` | Evidence |
|----------|------|-----------------------|-------------|----------|
| `Step` dataclass | Portable workflow-step unit | id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path | `pipeline/models.py:108-123` | `5.1-07` |
| `StepResult` dataclass | Runner-authored outcome | status, attempt, gate_failure_reason, timestamps, remediation metadata, duration | `pipeline/models.py:125-148` | `5.1-08` |
| `StepRunner` protocol | Process-boundary seam | `__call__(step, config, cancel_check) -> StepResult` | `pipeline/executor.py:41-60` | `5.1-13` |
| `execute_pipeline()` | Generic sequencer | accepts `list[Step \| list[Step]]`; nested list = parallel group; start/complete/state callbacks, cancellation, optional trailing runner | `pipeline/executor.py:63-188` | `5.1-14` |
| `GateCriteria` + `gate_passed()` | Pure-Python validation | tiers EXEMPT/LIGHT/STANDARD/STRICT; frontmatter + min_lines + semantic checks | `pipeline/models.py:90-105`, `pipeline/gates.py:20-76` | `5.1-06`, `5.1-22` |
| `GateMode` + `resolve_gate_mode()` | Blocking vs trailing | BLOCKING/TRAILING; release always blocking, task trailing only if grace_period>0; `grace_period==0` forces BLOCKING | `pipeline/models.py:69-79`, `pipeline/executor.py:211-215`, `trailing_gate.py:604-647` | `5.1-04`, `5.1-17`, `5.1-36` |
| `ClaudeProcess` | Runtime subprocess seam | builds `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`; prompt via stdin; exit 124 = timeout | `pipeline/process.py:73-95`, `159-214` | `5.1-25`, `5.1-28`, `5.7-29` |
| `Deliverable` + `decompose_deliverables()` | Behavioral split | `.a` implement + `.b` verify; idempotent | `pipeline/models.py:151-209`, `pipeline/deliverables.py:146-194` | `5.1-09`, `5.1-39` |
| `DeferredRemediationLog` | Trailing-gate persistence | lock-guarded, disk-persistent JSON; PENDING/REMEDIATED/WAIVED | `pipeline/trailing_gate.py:471-596` | `5.1-35` |
| Sprint parser contract | Tasklist compatibility | `### T<PP>.<TT> -- Title`, `**Dependencies:**`, `**Command:**`, classifier row, Execution Mode (claude/python/skip), phase filename aliases | `sprint/config.py:15-26`, `374-492` | `5.3-04`, `5.3-06`, `5.5-11` |
| `TurnLedger` | Budget ledger | `can_launch()` / pre-debit / reconcile; sprint-local | `sprint/models.py:692-777` | `5.3-17` |
| `pipeline/__init__.py` API surface | Compatibility anchor | 42 exported symbols (models, executor, gates, process, deliverables, guard/FMEA/dataflow/conflict) | `pipeline/__init__.py:1-157` | `5.1-42` |

**Defined-but-unwired / drift contracts to preserve (not silently fix)** `[CODE-VERIFIED]`:

| Contract | State | `path:line` | Evidence |
|----------|-------|-------------|----------|
| `CERTIFY_GATE` / `build_certify_step` | Defined, **not wired** in production `_build_steps` | `roadmap/gates.py:1324-1351`, `roadmap/executor.py:2205` | `5.2-10` |
| Deviation classifier | **Unwired**; all records render UNCLASSIFIED | `roadmap/executor.py:1603-1609`, `gates.py:1390-1422` | `5.2-19` |
| `WIRING_GATE` trailing mode | Configured TRAILING but grace_period defaults 0 → effectively BLOCKING | `roadmap/executor.py:2175-2184` | `5.2-12` |
| Path-A `_verify_checkpoints()` | Per-task path does **not** call it (only Path B does) | `sprint/executor.py:1259-1301` vs `1512-1531` | `XC-06` |
| 4-layer `IsolationLayers` | Exists but **not called** in main loop; partial/unused | `sprint/executor.py:106-182`, `1303-1324` | `5.3-14` |
| `read_status_from_log` / `tail_log` | **Stubs** ("not yet connected"); status/logs commands don't report live | `sprint/logging_.py:224-235` | `5.3-28` |

> **CRITICAL:** A faithful port must preserve these states as-is and flag them, not normalize them. Silently wiring `CERTIFY_GATE` or the deviation classifier during migration would change gate semantics and mask known gaps (evidence index "key load-bearing facts" #2; `XC-16`).

### 7.3 Proposed Adapter-Contract Inventory (`[DESIGN — UNBUILT]`)

The hybrid introduces exactly four adapter contracts. **None is implemented in the repo today** (`5.6-27`). Each carries a round-trip / idempotency validation contract.

| # | Adapter contract | Direction | Mapping summary | Validation contract | Evidence |
|---|------------------|-----------|-----------------|---------------------|----------|
| C1 | Tasklist bundle → Backlog.md import | tasklist → Backlog | `TASKLIST_ROOT`→container, phase H1→milestone/doc, `T<PP>.<TT>`→task external ID, body→markdown, `**Dependencies:**`→dep metadata+text, numbered checkpoint tasks→verification task+linked doc | Export back to files such that `discover_phases()` + `parse_tasklist_file()` succeed and counts match `count_tasks_in_file()` | `5.5-14`, `07` Contract 1 |
| C2 | Backlog.md / tasklist → Beads graph sync | Backlog/tasklist → Beads | root issue, phase parent (epic), task issue (status/tier/risk/classifier/deliverable IDs), dependency edges `dep→dependent`, checkpoint node, artifact pointer (path only) | Graph export must produce dependency list identical to parser-extracted `TaskEntry.dependencies` unless a human-approved patch exists | `5.5-14`, `07` Contract 2 |
| C3 | Backlog.md / Beads → Mastra workflow plan | Backlog/Beads → Mastra | one workflow per bundle; one stage per phase; `T<PP>.<TT>` as step external ID; gate→blocking/trailing branch or scorer; trace metadata = R-*/T-*/D-*/phase/tier/model/permission/max_turns; provider = ClaudeProcess (hybrid) or new adapter | Plan generation must be **deterministic** from Backlog + Beads and produce a dry-run plan (task order, gates, expected artifacts, provider commands) before execution | `5.5-14`, `07` Contract 3 |
| C4 | Mastra run results → Backlog.md + Beads reconciliation | Mastra → Backlog/Beads | PASS→log entry + optional task done / issue close; FAIL/INCOMPLETE→failure note + remediation edge; DEFERRED→deferred gate report; HALT→halt report + resume command + blocked root; checkpoint→link doc + close node; telemetry→summarized budget line only | Reconciliation must be **idempotent**: replaying the same result event must not duplicate Backlog rows or Beads edges | `5.5-14`, `07` Contract 4 |

> **Tip:** The proposed pilot wraps `superclaude tasklist validate` first — the smallest surface (single strict gate, non-destructive, reuses the shared pipeline) — and the decisive early gate is proving Mastra rerun/recovery/durability before committing to broader port (`XC-13`).

---

## 8. API & Integration Points

This section documents the external integration surfaces of the three target substrates (`[EXTERNAL-VERIFIED]`, with source URLs) and the `[DESIGN — UNBUILT]` integration boundaries the hybrid would establish. The current system's only "API" is the `ClaudeProcess` subprocess seam (`[CODE-VERIFIED]`, §6.2 / §7.2); everything Mastra/Backlog/Beads is external capability, not current implementation.

### 8.1 External Integration Surfaces Used (`[EXTERNAL-VERIFIED]`)

| Surface | Substrate | Transport / contract | Key constraint | Source | Evidence |
|---------|-----------|----------------------|----------------|--------|----------|
| `MCPClient` | Mastra | Connects agents to external MCP servers over **stdio / HTTP / SSE** | — | mastra.ai/docs/mcp/overview | `5.7-07` |
| `MCPServer` | Mastra | Exposes agents/tools/workflows over **HTTP(S)**; `requireToolApproval` = human-in-the-loop; FGA enforcement for MCP tool exec | FGA tied to Enterprise Edition | mastra.ai/docs/mcp/overview | `5.7-07` |
| Mastra server (REST) | Mastra | Hono-based; Express/Hono/Fastify/Koa adapters; registered agents/workflows become REST endpoints with **OpenAPI/Swagger** | Studio/API public unless auth configured | mastra.ai/docs/server/mastra-server | `5.7-08`, `5.7-06` |
| `WorkspaceSandbox` | Mastra | `executeCommand`/start/stop/destroy, timeouts, stdout/stderr/wait, maxRetainedBytes (@mastra/core@1.1.0) | Candidate subprocess substrate but **NOT proven** parity with Claude Code hook/permission model | mastra.ai/reference/workspace/sandbox | `5.7-03`, `XC-22` |
| Backlog.md MCP (MVP) | Backlog.md | **stdio** MCP surface routing through Core APIs; tools `task_*`, `milestone_*`, `definition_of_done_defaults_*`, `document_*` | Decision tools are **CLI-only**, not MCP; contradicts older "75+ tools" claims | github.com/MrLesk/Backlog.md/src/mcp/README.md | `5.7-14` |
| Backlog.md MCP task schemas | Backlog.md | list/search/view/archive/complete use **`additionalProperties: false`** | SuperClaude custom metadata **cannot** be arbitrary MCP fields — must use supported fields / body sections / docs, or extend the schema | github.com/MrLesk/Backlog.md/src/mcp/tools/tasks/schemas.ts | `5.7-13` |
| Backlog.md CLI / filesystem | Backlog.md | `backlog/` dir; `backlog init --no-git` = filesystem-only; `autoCommit` default false; `proper-lockfile` | Local-file / git-centric, **not** a centralized multi-user transactional PM backend; one-task-per-agent discipline needed | github.com/MrLesk/Backlog.md; ADVANCED-CONFIG.md | `5.7-15`, `5.7-16` |
| Beads `bd` CLI (`--json`) | Beads | `--json` stable contract (schema v1); `BD_JSON_ENVELOPE=1` opts into uniform envelope (planned v2.0 default); legacy lists = raw arrays, objects = top-level `schema_version`, errors → stderr; `bd export --json` = JSONL | Integration must parse `--json` with **dual** legacy + envelope compatibility; **not** JSONL reads | github.com/gastownhall/beads/docs/JSON_SCHEMA.md | `5.7-25` |
| Beads core verbs | Beads | `bd ready` (unblocked), `bd create`, `bd update --claim` (atomic assignee + in_progress), `bd dep add`, `bd show`, `bd prime`, `bd remember` | `bd ready` = no open blocking deps; cycles rejected at write | github.com/gastownhall/beads; SETUP.md | `5.7-20`, `5.7-21` |
| Beads server mode | Beads | `dolt sql-server`, concurrent writers, `bd init --server` (`--server-host/port/socket/user` + `BEADS_DOLT_PASSWORD`) | **Server mode REQUIRED** for multi-agent; embedded (default) is single-writer ("database is locked" under contention) | github.com/gastownhall/beads/docs/DOLT.md | `5.7-24` |
| Beads gates | Beads | `gh:pr`, `gh:run`, `timer`, `bead` (cross-rig), `human` (approval); `bd gate check/discover` | Maps SuperClaude "done vs merged/validated" semantics | github.com/gastownhall/beads/docs/DEPENDENCIES.md | `5.7-22` |

> **CRITICAL:** Storage is **Dolt-first** for Beads (version-controlled SQL, cell-level merge, branching). `.beads/issues.jsonl` is export/interchange **only**, not the canonical sync layer — this corrects the seed-brief "SQLite + JSONL" framing (`5.7-23`). Version caution: Beads v1.0.5 is pre-release/gated ("do not upgrade", migration 0043 can break multi-machine sync, #4259); v1.0.4 had a server data-clobber regression — **pin and gate versions** (`5.7-27`).

### 8.2 Internal Integration Points (Current `[CODE-VERIFIED]` + Proposed `[DESIGN — UNBUILT]`)

| Integration | Direction | Mechanism | Description | Tag |
|-------------|-----------|-----------|-------------|-----|
| Executor ↔ runner | Bidirectional | `StepRunner` protocol | Process-boundary seam; runner owns subprocess + timeout, executor owns retry/gates/ordering | `[CODE-VERIFIED]` (`5.1-13`) |
| Runner → Claude CLI | Outbound | `ClaudeProcess` subprocess | `claude --print` over stdin; stdout = output file (or `.log` sidecar in tool-write mode) | `[CODE-VERIFIED]` (`5.1-24`..`5.1-28`) |
| roadmap / tasklist / sprint → shared pipeline | Inbound | `execute_pipeline` + injected `run_step` | All consumers reuse generic sequencer (sprint runs its own phase loop on shared models) | `[CODE-VERIFIED]` (`5.1-43`) |
| Tasklist → Backlog.md (C1) | Outbound | adapter import | Markdown task/doc import preserving stable IDs | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Backlog/tasklist → Beads (C2) | Outbound | `bd` CLI `--json` | Dependency-graph mirror by stable external ID | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Backlog/Beads → Mastra (C3) | Outbound | workflow plan generation | Deterministic dry-run plan before execution | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Mastra → Backlog/Beads (C4) | Inbound | idempotent reconciliation | Run results projected to status/log/graph | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Governance plane → all | Bidirectional | control-plane (proposed) | Tenant registry, identity mapping, RBAC/ABAC, tool catalog, MCP inventory, approval, audit, cost/budget attribution | `[DESIGN — UNBUILT]` (`5.8-11`) |

> **Important:** MCP is a narrow integration protocol (host/client/server tool-resource exchange), **explicitly not a governance platform** (`5.8-01`). Token passthrough is forbidden (`5.8-03`). A company-wide multi-tenant deployment needs an **additional** governance/control-plane layer beyond all three components (`5.8-11`); none of Mastra OSS, Backlog.md, or Beads supplies cross-tenant IAM, enterprise audit, rate limiting, or cost attribution (`5.8-09`, `5.8-10`).

### 8.3 External Service Dependencies & Failure Modes

| Service | Purpose in hybrid | Failure mode | Proposed fallback / mitigation | Tag |
|---------|-------------------|--------------|--------------------------------|-----|
| Mastra runtime | Run/trace/gate-execution owner (C3/C4) | Hook/permission parity NOT established vs Claude Code; Temporal runner experimental; rerun/replay/idempotency unvalidated | Hybrid: keep current Python+ClaudeProcess as execution oracle until spike gate SG1 proves durable subprocess supervision parity | `[EXTERNAL-VERIFIED]` risk (`5.7-10`, `XC-12`, `XC-22`) |
| Mastra EE (auth/RBAC/FGA/audit) | Production governance | RBAC/SSO/FGA/audit/on-prem are **Enterprise-licensed**, not Apache-2.0 core; `ee/` dirs under Mastra EE license | License decision is a go/no-go gate (D2); cost/identity decision at SG4 | `[EXTERNAL-VERIFIED]` key risk (`5.7-06`, `XC-17`) |
| Backlog.md | Prose / task / doc owner (C1) | `additionalProperties:false` rejects custom metadata; browser-UI state-loss bug #578; Backlog↔Beads integration immature (open FR #588) | Use supported fields/body/docs or extend schema; assign canonical owner per D1/D3; narrow import/export sync first | `[EXTERNAL-VERIFIED]` risk (`5.7-13`, `5.7-17`, `5.7-18`) |
| Beads (Dolt) | Dependency-graph owner (C2) | Embedded mode single-writer; multi-agent needs server mode; session attribution churning (#3400/#3583); version sync corruption (#4259) | Server mode + atomic `--claim` + one-task-per-agent; pin + gate versions; tested backup/restore (SG3) | `[EXTERNAL-VERIFIED]` risk (`5.7-24`, `5.7-27`, `5.7-28`, `XC-20`, `XC-21`) |
| Claude CLI (current) | Execution provider today | Subprocess timeout (exit 124), prompt-too-long, max-turns; `ClaudeProcess` handles SIGTERM→SIGKILL escalation | Current behavior preserved in hybrid; Mastra WorkspaceSandbox is candidate replacement only after parity proof | `[CODE-VERIFIED]` (`5.1-28`, `5.7-29`) |

---

**Status: Complete.**

> **Verification note:** Sections 6, 7, and 8 are grounded in evidence index `00-evidence-index.md` and research file `07-target-data-model-and-ownership.md`. CODE-VERIFIED `path:line` citations were spot-checked against HEAD `9e864860` (`StepResult` `pipeline/models.py:126`, `TaskEntry` `sprint/models.py:25`, `CheckpointEntry` `sprint/models.py:312`, `MonitorState` `sprint/models.py:623`, `TurnLedger` `sprint/models.py:693` — all consistent with cited dataclass-body ranges). EXTERNAL-VERIFIED rows carry web-01..04 source URLs. All `[DESIGN — UNBUILT]` rows are explicitly marked and reflect proposed, not implemented, architecture.
