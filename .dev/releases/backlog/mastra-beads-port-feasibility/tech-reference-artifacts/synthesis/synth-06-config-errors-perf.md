# Synthesis 06 — Sections 9-11 (Configuration & Environment, Error Handling & Recovery, Performance Characteristics)

**Target document:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture — Technical Reference
**Template:** `.claude/templates/documents/technical_reference_template.md`
**Covers template sections:** §9 Configuration & Environment, §10 Error Handling & Edge Cases, §11 Performance Characteristics
**Status:** Complete
**HEAD (for `[CODE-VERIFIED]` claims):** `9e864860`
**Evidence index:** `.dev/tasks/to-do/TASK-TECHREF-20260603-021348/research/00-evidence-index.md`

> **CRITICAL — Built-vs-Design demarcation.** This is a DESIGN REFERENCE for a PROPOSED, not-yet-built hybrid. Every claim below carries exactly one tag:
> - `[CODE-VERIFIED]` — existing Python in `src/superclaude/` at HEAD `9e864860`, with real `path:line`.
> - `[DESIGN — UNBUILT]` — target hybrid architecture; not implemented anywhere in the repo today.
> - `[DESIGN — UNVERIFIED]` — target behavior whose performance/semantics cannot be measured because no integrated system exists.
> - `[EXTERNAL-VERIFIED]` — Mastra / Backlog.md / Beads / MCP-governance facts from web research (web-01..04), each with a source URL.
>
> **No source file in the repo implements any Mastra / Backlog.md / Beads integration today** (evidence index row 5.6-27). All hybrid configuration, recovery, and performance claims are forward-looking.
>
> **Path-root convention:** bare `pipeline/…`, `sprint/…`, `roadmap/…`, `tasklist/…` paths are relative to `src/superclaude/cli/` (e.g. `pipeline/models.py` resolves to `src/superclaude/cli/pipeline/models.py`), matching the evidence index.

---

## 9. Configuration & Environment

> **Conditional Section status:** INCLUDED. The proposed hybrid is configuration-heavy: it composes three independently versioned external substrates (Mastra, Backlog.md, Beads), each with its own licensing, deployment-mode, and version-pinning constraints, on top of the existing Python pipeline's configuration surface.

### 9.1 Configuration Files

This table separates configuration that exists today (the Python pipeline the hybrid wraps) from configuration the hybrid would need to introduce.

| File / Surface | Purpose | Key Settings | Tag |
|----------------|---------|--------------|-----|
| `pipeline/models.py` `PipelineConfig` | Base run config for the generic executor | `work_dir`, `dry_run`, `max_turns`, `model`, `permission_flag` (default `--dangerously-skip-permissions`), `debug`, `grace_period`, cosmetic-remediation settings | `[CODE-VERIFIED]` `pipeline/models.py:212-235` |
| `sprint/models.py` `SprintConfig` | Sprint run config; extends `PipelineConfig` | `__post_init__` sets `work_dir=release_dir`, maps wiring fields, derives `wiring_gate_mode`, defaults `state_dir` to `.dev/sprint-state/<id>` | `[CODE-VERIFIED]` `sprint/models.py:347-510`, `415-471` |
| `.roadmap-state.json` | Roadmap resume/state file | spec path/hash, input type, TDD/PRD paths, agents, depth, per-step statuses, validation/fidelity/remediate/certify status | `[CODE-VERIFIED]` `roadmap/executor.py:2627-2682` |
| `cli_portify` `config YAML` + `STEP_REGISTRY` | Deterministic step config (precedent for hybrid step config) | 12 ordered step IDs, phase types, per-step timeouts, retry limits, named artifacts | `[CODE-VERIFIED]` `cli_portify/executor.py:105-183`, `767-840` |
| `backlog.config.yml` (Backlog.md) | Project-local task-store config | `statuses`, `labels`, `defaultStatus`, git settings, `filesystemOnly`, zero-padded IDs, `backlogDirectory`, prefixes, MCP HTTP config; `autoCommit` default `false`, `remoteOperations`, `bypassGitHooks` | `[EXTERNAL-VERIFIED]` https://raw.githubusercontent.com/MrLesk/Backlog.md/main/ADVANCED-CONFIG.md ; src/types/index.ts |
| Beads Dolt mode config | Embedded vs server mode selection | embedded (default): `.beads/embeddeddolt/`, single-writer file lock; server: `bd init --server`, `--server-host/port/socket/user` + `BEADS_DOLT_PASSWORD`, `.beads/dolt/`; shared-server: `bd dolt set shared-server true`, port 3308 | `[EXTERNAL-VERIFIED]` https://github.com/gastownhall/beads/blob/main/docs/DOLT.md |
| Mastra `Mastra` instance + `MastraCompositeStore` | Runtime/workflow/storage config | storage provider selection (libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare); composite routing of memory/workflows/scores/observability domains; runner choice (built-in / Inngest / Temporal-experimental) | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/memory/storage ; https://mastra.ai/reference/storage/composite ; https://mastra.ai/docs/deployment/workflow-runners |
| Hybrid adapter config (e.g. `hybrid.config.yml`) | **DESIGN** — single typed graph as source-of-truth + adapter routing | ownership map (Backlog.md=prose/task/doc/decisions, Beads=dependency graph, Mastra=run/trace/gate state); stable-ID strategy; round-trip parser validation; per-adapter version pins | `[DESIGN — UNBUILT]` (evidence index 5.5-12, 5.5-14, 5.6-25) |

### 9.2 Licensing as Configuration (External Substrates)

> **Important:** For this hybrid, licensing is not a footnote — it is a hard configuration gate that determines which features are even available. This is the single biggest strategic constraint (RISK R1, evidence index XC-17).

| Component | License | What is free | What is gated | Tag |
|-----------|---------|-------------|--------------|-----|
| Mastra core | Apache-2.0 | Agents, workflows, storage adapters, Server, observability core; `SimpleAuth` (API-key → `{id,name,role}`) | Everything under any `ee/` directory: `StaticRBACProvider`, `DEFAULT_ROLES` (owner/admin/member/viewer), WorkOS/Okta SSO, permission-based Studio UI, Agent Builder multi-tenant workflows — all import from `@mastra/core/auth/ee` and require a paid EE license in production | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/server/auth ; https://mastra.ai/pricing ; Context7 `/mastra-ai/mastra` |
| Mastra EE | Mastra Enterprise License (bespoke commercial — NOT Elastic 2.0 / BSL) | dev + testing on your own systems | Any "production" use beyond dev/testing requires a written commercial agreement; redistribution/sublicense/sell forbidden; RBAC, audit logs, SLAs, VPC/on-prem data locality | `[EXTERNAL-VERIFIED]` web-01 finding 6; FEASIBILITY-STUDY M10/M11 |
| Backlog.md | MIT | Entire product (CLI, TUI board, browser UI, search, docs, decisions, MCP MVP) | (none) — but no native multi-tenancy/RBAC/auth/remote-HTTP transport exists; stdio + single-repo + single-trust-domain by design | `[EXTERNAL-VERIFIED]` https://github.com/MrLesk/Backlog.md ; package.json |
| Beads | open-source (`gastownhall/beads`) | Full CLI / Dolt store / dependency graph / gates / memory | (none) — but NO multi-tenancy/RBAC at the Beads layer; "multi-writer" (server mode) is concurrency, not tenancy | `[EXTERNAL-VERIFIED]` https://github.com/gastownhall/beads ; DOLT.md |

> **CRITICAL:** The OSS Apache path on Mastra yields only `SimpleAuth` (flat API-key→role) plus application-level storage scoping; the RBAC/tenant layer must be built DIY. A multi-tenant RBAC platform on Mastra is feasible but commercially gated. `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY §5.1.2)

### 9.3 Version Pins and Deployment-Mode Settings

> **Important:** All three external components are fast-moving with sharp edges (RISK R9, evidence index XC-25). Every adapter MUST pin versions and runtime-verify schemas rather than assume a stable contract.

| Component | Version (verified) | Pin / mode guidance | Tag |
|-----------|--------------------|--------------------|----|
| Beads | `v1.0.5` | **`v1.0.5` is pre-release / gated with a "do not upgrade" warning** — migration `0043` can silently and unrecoverably break multi-machine `bd dolt` sync (issue #4259). `v1.0.4` had a server-mode data-clobber regression (#3870). Pin + gate versions; include `bd doctor` + backup/restore + push/pull smoke tests in adoption gates. Confirm exact current release against the live releases page before pinning. | `[EXTERNAL-VERIFIED]` https://github.com/gastownhall/beads/releases ; issue #3870, #4259 |
| Beads deployment mode | embedded (default) vs server | Embedded = in-process Dolt, single-writer with file lock ("database is locked" under contention), solo only. **Server mode (`bd init --server`) is REQUIRED for any multi-agent / parallel writer scenario.** Sync via Dolt remotes under `refs/dolt/data`. `.beads/issues.jsonl` is export/interchange ONLY — drive `bd ... --json`, never read JSONL as canonical. | `[EXTERNAL-VERIFIED]` https://github.com/gastownhall/beads/blob/main/docs/DOLT.md ; SYNC_CONCEPTS.md |
| Beads JSON contract | schema version `1` | `--json` (not `--format json`) is the stable contract. `BD_JSON_ENVELOPE=1` opts into a uniform envelope (planned default v2.0). Legacy list commands emit raw arrays; `bd export --json` emits JSONL. Integrations need a dual parser (legacy + envelope). | `[EXTERNAL-VERIFIED]` https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md |
| Backlog.md | `v1.45.2` | TypeScript/Bun; MVP stdio MCP surface with active churn and doc drift. Git is optional: `backlog init --no-git` creates a filesystem-only project (`autoCommit` default `false`). MCP task schemas use `additionalProperties: false` — custom orchestration metadata CANNOT be added as arbitrary MCP fields; must map to supported fields, body sections, docs, or extend the schema. | `[EXTERNAL-VERIFIED]` package.json ; src/mcp/tools/tasks/schemas.ts ; ADVANCED-CONFIG.md |
| Mastra core | `@mastra/core 1.1.0+` (1.x line, fast-moving); precise current-latest is `[DESIGN — UNVERIFIED]` and MUST be verified/pinned at adoption time | `WorkspaceSandbox` was ADDED in `@mastra/core@1.1.0`, so `>= 1.1.0` is the hard floor `[EXTERNAL-VERIFIED]` (web-01; https://mastra.ai/reference/workspace/sandbox). Pin `@mastra/core` at a known-good `1.x` version at adoption time — the package is 1.x and fast-moving, so verify the exact current-latest before pinning rather than assuming a stable contract `[DESIGN — UNBUILT]`. Use composite storage in any serious deployment (PostgreSQL/libSQL for snapshots, ClickHouse for observability; avoid in-memory except tests — in-memory resets on process change). `@mastra/temporal` is experimental/not-production-ready; prefer built-in or Inngest runner. | `[EXTERNAL-VERIFIED]` web-01 ; https://mastra.ai/reference/workspace/sandbox ; https://mastra.ai/docs/deployment/workflow-runners |

### 9.3.1 Hybrid configuration the design would need to add `[DESIGN — UNBUILT]`

| Config need | Why | Tag |
|-------------|-----|-----|
| Ownership map (one prose owner, one graph owner, one run owner) | Dual task/status owners (Backlog.md + Beads) cause drift; integration is immature (Backlog.md FR #588). Canonical owners must be assigned in config. | `[DESIGN — UNBUILT]` (5.5-13; RISK R3 / XC-19) |
| Stable-ID mapping config (`TASK-*`, `T<PP>.<TT>`, `D-####`, `R-###` ↔ Backlog.md IDs ↔ Beads hash IDs) | Stable IDs are the cross-system sync keys and are non-negotiable. | `[DESIGN — UNBUILT]` (5.5-04, 5.5-13) |
| Beads ↔ Backlog.md sync scope (start narrow: import/export only) | Maintainer guidance on FR #588: choose one workflow (e.g. import/export sync) before a broad integration surface. | `[DESIGN — UNBUILT]` (5.7-17) |
| Governance/control-plane config (tenant registry, identity mapping, RBAC/ABAC, tool catalog, MCP inventory, approval engine, audit log, cost/rate/budget) | None of the three components supplies tenant isolation, per-invocation audit, or cost attribution; MCP is not a governance platform. Required before company-wide multi-tenant deployment. | `[DESIGN — UNBUILT]` (5.8-11; RISK R8 / XC-24) |

### 9.4 Environment Variables

| Variable | Purpose | Default | Required | Tag |
|----------|---------|---------|----------|-----|
| `CLAUDE_WORK_DIR` | Sprint Path B sets this on the spawned subprocess (the only isolation env reliably passed today) | (unset) | No | `[CODE-VERIFIED]` `sprint/executor.py:1303-1324`, `1320-1324` |
| `CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT` | Stripped by `build_env()` before launching the child `claude --print` process | (stripped) | n/a | `[CODE-VERIFIED]` `pipeline/process.py:97-112`, `136-139` |
| `BEADS_DOLT_PASSWORD` | Beads server-mode auth | (unset) | Yes (server mode) | `[EXTERNAL-VERIFIED]` DOLT.md |
| `BEADS_DOLT_SHARED_SERVER` / `BEADS_DIR` | Enable shared-server mode / relocate `.beads/` | (unset) | No | `[EXTERNAL-VERIFIED]` DOLT.md |
| `BD_JSON_ENVELOPE` | Opt into uniform Beads JSON envelope (planned v2.0 default) | `0` | No | `[EXTERNAL-VERIFIED]` JSON_SCHEMA.md |
| `CLAUDE_SESSION_ID` / `BEADS_SESSION_ID` | Beads multi-agent session attribution (actively changing — issues #3400/#3583) | (unset) | No (in flux) | `[EXTERNAL-VERIFIED]` issues #3400/#3583 |
| Mastra storage / auth provider env (e.g. PostgreSQL/ClickHouse DSNs, WorkOS/Auth0/Clerk keys) | Configure composite storage + auth provider | varies | varies | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/memory/storage ; https://mastra.ai/docs/server/auth |

> **Note:** The four-layer `IsolationLayers` (`CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`) is DEFINED but NOT called in the sprint main loop today; only Path B sets `CLAUDE_WORK_DIR` and Path A passes no isolation env. A faithful Mastra port must either implement these for real or explicitly scope to the weaker active model — they are not a current runtime guarantee. `[CODE-VERIFIED]` `sprint/executor.py:106-182`, `1303-1324`, `1076-1115`

### 9.5 Feature Flags

These exist in the current pipeline and would carry forward conceptually as hybrid run modes; the hybrid-specific flags are DESIGN.

| Flag / Surface | Description | Default | Impact When Toggled | Tag |
|----------------|-------------|---------|---------------------|-----|
| `--dry-run` | Roadmap/pipeline preview without side effects; skips sub-skill invocations | off | Structured preview only; no LLM calls | `[CODE-VERIFIED]` `roadmap/commands.py:32-298` |
| `--no-validate` / `--no-convergence` / `--no-compress` | Roadmap stage toggles | on (enabled) | Disables auto-validation / convergence loop / compression | `[CODE-VERIFIED]` `roadmap/commands.py:32-298` |
| `--allow-cosmetic-remediation` / `--strict-no-remediation` | Cosmetic-remediation lane | off | Injects roadmap remediator into `PipelineConfig` | `[CODE-VERIFIED]` `roadmap/commands.py:153-172` |
| sprint `--shadow-gates`, `--stall-timeout`, `--stall-action`, `checkpoint_gate_mode` (off/shadow/soft/full) | Sprint watchdog + checkpoint enforcement | shadow (checkpoints) | Controls stall handling and checkpoint blocking severity | `[CODE-VERIFIED]` `sprint/commands.py:71-188`, `executor.py:1811-1891` |
| Mastra `requireToolApproval` | Human-in-the-loop approval for MCP tool execution | off | Gates tool calls behind manual approval | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/mcp/overview |
| Hybrid `ownership.mode` (DESIGN) | Which substrate owns a given record class | n/a | Routes writes to canonical owner; prevents dual-owner drift | `[DESIGN — UNBUILT]` (5.5-12/13) |

---

## 10. Error Handling & Recovery

> **Note:** Section title aligns to the template's §10 "Error Handling & Edge Cases" and extends it to recovery, since durability/recovery is the decisive engineering concern for this hybrid (the early-spike gate G2 is "prove Mastra rerun/recovery/durability" — evidence index XC-13). The hybrid would inherit two recovery models that must be reconciled: the existing Python pipeline's filesystem-artifact recovery (`[CODE-VERIFIED]`) and Mastra's snapshot-based durable workflow recovery (`[EXTERNAL-VERIFIED]`).

### 10.1 Error Handling Patterns

| Error Category | Handling Pattern | Recovery | Tag |
|----------------|------------------|----------|-----|
| Step failure (generic pipeline) | `StepStatus` FAIL/TIMEOUT are failures; CANCELLED/SKIPPED are not. Retry loop in `_execute_single_step()`; blocking vs trailing branching; cosmetic remediation; final fail | Retry up to `retry_limit`; trailing-mode failures logged as advisory warnings only | `[CODE-VERIFIED]` `pipeline/models.py:40-67`, `executor.py:191-399` |
| Subprocess timeout | `wait()` returns `124` (matches bash `timeout`); `terminate()` does SIGTERM → 10s → SIGKILL → 5s on the process group | Timeout maps to `124`/INCOMPLETE/TIMEOUT downstream | `[CODE-VERIFIED]` `pipeline/process.py:159-214` |
| Parallel-group failure | `_run_parallel_steps()` sets a shared cancellation event when any step fails; no group-level retry | Group cancelled; daemon threads observe cancellation | `[CODE-VERIFIED]` `pipeline/executor.py:402-452` |
| Sprint phase classification | `_determine_phase_status()` authoritative classifier: exit `124`→TIMEOUT; prompt-too-long→INCOMPLETE; end-checkpoint PASS + no contamination→PASS_RECOVERED; result-file HALT/CONTINUE markers; no result+output→PASS_NO_REPORT; no output→ERROR (11 `PhaseStatus` values) | Runner-authored classification, not agent-self-reported | `[CODE-VERIFIED]` `sprint/executor.py:2067-2148`, `models.py:211-270` |
| Sprint diagnostic capture on failure | `DiagnosticCollector` snapshots monitor + tails logs; `FailureClassifier` prioritizes stall/timeout/context-exhaustion/crash/error/unknown; `ReportGenerator` writes diagnostic markdown; outcome HALTED | Diagnostic artifact + halt | `[CODE-VERIFIED]` `sprint/executor.py:1609-1639`, `diagnostics.py:72-127`, `157-232` |
| eval per-eval error | Per-eval JSONL forensic event buffer logs setup/teardown/spawn/inject/observe/errors; classify ERRORED/PASS/FAIL; timeout emits timeout events, best-effort cancel, preserves HOME, returns TIMEOUT, flushes JSONL | Failed/errored HOMEs preserved for forensics; optional retry-once | `[CODE-VERIFIED]` `eval/runner.py:537-588`, `591-673`, `1026-1101` |
| Beads cycle rejection | `bd dep add` rejects dependency cycles at write time; `bd ready` = no open blocking deps | Write rejected before graph corruption | `[EXTERNAL-VERIFIED]` https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md |
| Mastra durable suspend/resume | Workflows `suspend()` / `resume()` / `resumeStream()`; on suspend Mastra stores a snapshot in the configured storage provider; snapshots persist across deployments and restarts; resume from a specific step ID | Resume from snapshot at a specific step ID | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/workflows/suspend-and-resume |
| Mastra runner retries | Inngest runner provides step memoization + automatic retries + suspend/resume; Temporal provides durable execution + retries (experimental) | Runner-dependent; production retry/durability depends on runner + storage choice | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/deployment/workflow-runners |

### 10.2 Existing Code-Verified Recovery Surfaces (Reusable by the Hybrid)

These are the recovery primitives the hybrid would wrap or port — they already work today.

| Surface | Behavior | Tag |
|---------|----------|-----|
| Roadmap resume state | `.roadmap-state.json` carries spec path/hash, per-step statuses, validation/fidelity/remediate/certify status; `execute_roadmap()` restores resume state, supports spec-patch resume | `[CODE-VERIFIED]` `roadmap/executor.py:2627-2682`, `2985-3187` |
| Sprint checkpoint verification | `_verify_checkpoints()` runs only after PASS-like status; respects `checkpoint_gate_mode` (off / shadow=default / soft / full); full mode downgrades to `PASS_MISSING_CHECKPOINT` when files are missing. `verify_checkpoint_files()` returns existence status per declared checkpoint | `[CODE-VERIFIED]` `sprint/executor.py:1811-1891`, `checkpoints.py:97-112` |
| Sprint `verify-checkpoints` CLI | Builds a manifest, optionally recovers missing reports, writes `manifest.json`, prints table or JSON | `[CODE-VERIFIED]` `sprint/commands.py:360-415` |
| Sprint manifest + checkpoint recovery | End-of-sprint `build_manifest()` + `write_manifest()` write `<release_dir>/manifest.json` + a `checkpoint_manifest` JSONL event; `recover_missing_checkpoints()` synthesizes reports marked status UNKNOWN | `[CODE-VERIFIED]` `sprint/executor.py:1702-1725`, `checkpoints.py:209-408` |
| eval HOME isolation + forensic JSONL | Three-check `containment_guard` (eval-ID regex, scratch-root allowlist, post-mkdtemp containment); per-eval HOME under `home_root`; failed/errored HOMEs preserved; thread-safe JSONL forensic event buffer | `[CODE-VERIFIED]` `eval/isolation.py:224-260`, `456-642`; `eval/runner.py:537-588` |
| eval RetryOncePolicy | Immutable, policy-tag driven (`MCP-flaky` tag, flaky statuses FAIL/ERRORED/TIMEOUT); one retry on a fresh HOME; idempotent annotation | `[CODE-VERIFIED]` `eval/retry.py:41-165` |
| audit checkpoint/retry/budget | Atomic checkpoint writes (temp + rename); `batch_retry` (max 2, cascading-failure detection); budget degradation (warn/degrade/halt with ordered protected-capability overrides) | `[CODE-VERIFIED]` `audit/checkpoint.py:58-110`, `batch_retry.py:60-187`, `budget.py:26-320` |
| DeferredRemediationLog | Lock-guarded, disk-persistent, JSON serde; PENDING/REMEDIATED/WAIVED; pending entries survive across runs | `[CODE-VERIFIED]` `pipeline/trailing_gate.py:471-596` |

### 10.3 Checkpoint-Recovery Strategy (Hybrid) `[DESIGN — UNBUILT]`

The hybrid must reconcile two recovery substrates without losing the runner-authored-truth property of the current system.

| Design element | Strategy | Tag |
|----------------|----------|-----|
| Run/trace/gate state ownership | Mastra owns run/trace/gate-execution state via durable workflow snapshots; checkpoint stages map to workflow steps. Mastra workflow state could REPRESENT checkpoint stages, but the current implementation relies on filesystem manifests + JSONL events — a faithful port needs explicit filesystem-artifact handling or a migration plan for those artifacts | `[DESIGN — UNBUILT]` (5.5-12; research 03 §line 175) |
| Checkpoint contract preservation | Preserve the canonical numbered `### T<PP>.<NN> -- Checkpoint:` task contract with `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...`; the runtime parser accepts BOTH legacy `### Checkpoint:` and numbered forms, but **Path A (per-task executor) does NOT call `_verify_checkpoints()`** today — a known runtime gap the port must wire in, not inherit | `[CODE-VERIFIED]` gap → `[DESIGN — UNBUILT]` fix (XC-05, XC-06; RISK R7 / XC-23) |
| Resume reconciliation | Map sprint phases/tasks to Beads `bd ready` + atomic `bd update <id> --claim`; reconcile Mastra run results back to Backlog.md + Beads idempotently (results→Backlog/Beads reconciliation adapter). Each adapter contract needs round-trip parser validation | `[DESIGN — UNBUILT]` (5.5-14; XC-16) |
| External gates as recovery boundaries | Encode SuperClaude "work done" vs "merged/validated" as Beads gates: `gh:pr` (PR merged), `gh:run` (CI), `timer`, `human` (approval); `bd gate check`/`discover`. These become durable recovery checkpoints external to the workflow runner | `[EXTERNAL-VERIFIED]` DEPENDENCIES.md → `[DESIGN — UNBUILT]` wiring |

### 10.4 Drift-Detection Strategy (Hybrid) `[DESIGN — UNBUILT]`

Dual ownership across three stores is the central new failure mode the hybrid introduces (RISK R3 / XC-19). Drift detection is therefore first-class, not optional.

| Drift surface | Detection strategy | Tag |
|---------------|--------------------|-----|
| Backlog.md ↔ Beads task/status drift | One canonical owner per record class (one prose owner, one graph owner, one run owner); periodic reconciliation diff keyed on stable IDs; start with narrow import/export sync (FR #588 maturity caveat) | `[DESIGN — UNBUILT]` (5.5-13, 5.7-17; RISK R3) |
| Stable-ID drift | Stable IDs (`TASK-*`, `T<PP>.<TT>`, `D-####`, `R-###`) are non-negotiable sync keys; round-trip parser validation on every adapter boundary detects ID divergence | `[DESIGN — UNBUILT]` (5.5-04, 5.5-14) |
| Beads sync corruption | Migration `0043` (v1.0.5) can silently break multi-machine `bd dolt` sync; detection = version-pin gate + `bd doctor` + backup/restore + push/pull smoke tests in adoption gates | `[EXTERNAL-VERIFIED]` (RISK R4 / XC-20; issue #4259) |
| Convergence/deviation drift (existing) | `DeviationRegistry.load_or_create` resets on spec-hash mismatch; merges structural + semantic findings with stable IDs, ACTIVE status, first/last_seen_run — an existing drift-tracking pattern the hybrid can reuse | `[CODE-VERIFIED]` `roadmap/convergence.py:90-207` |
| Schema/version drift (external tools) | Runtime-verify schemas rather than assume stable contracts: probe live Backlog.md MCP catalog (`additionalProperties:false` rejects unknown fields), use Beads dual JSON parser (legacy + envelope), pin `@mastra/core` at a known-good `1.x` version (`WorkspaceSandbox` requires `>= 1.1.0`; verify exact current-latest at adoption time) | `[EXTERNAL-VERIFIED]` (RISK R9 / XC-25) |

### 10.5 Graceful Degradation

| Failure | Impact | Degraded Experience | Tag |
|---------|--------|---------------------|-----|
| Beads server unavailable (multi-agent) | No concurrent claim/ready queue | Embedded single-writer fallback for solo work only ("database is locked" under contention) — multi-agent halts | `[EXTERNAL-VERIFIED]` DOLT.md |
| Backlog.md browser UI concurrent-edit | Unsaved draft text lost when files change underneath (open bug #578) | Avoid long unsaved browser drafts during agent mutation; CLI/MCP mutation unaffected | `[EXTERNAL-VERIFIED]` issue #578 |
| Mastra storage = in-memory | Snapshots reset on process change | Durability lost; use composite storage (PostgreSQL/libSQL + ClickHouse) in any non-test deployment | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/memory/storage |
| Mastra EE license absent | No production RBAC/SSO/FGA/audit | OSS path: `SimpleAuth` (flat API-key→role) + DIY application-level storage scoping only | `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY M11) |
| Sprint summary/retrospective failure | No phase summary or retrospective | End-of-sprint waits up to 90s for summaries; failures logged but do NOT abort wrap-up | `[CODE-VERIFIED]` `sprint/executor.py:1661-1688` |
| sprint `status`/`logs` commands | Live status/log views unavailable | `read_status_from_log`/`tail_log` are STUBS ("not yet connected"); JSONL/Markdown logs still written | `[CODE-VERIFIED]` `sprint/logging_.py:13-213`, `224-235` |

---

## 11. Performance Characteristics

> **CRITICAL — PERFORMANCE IS LARGELY `[DESIGN — UNVERIFIED]`.** There is **no integrated Mastra + Backlog.md + Beads system to measure**. No source file in the repo implements any of the three integrations (evidence index 5.6-27). Therefore this section documents **characteristics-by-design only** — architectural properties whose *direction* is known from external substrate docs (`[EXTERNAL-VERIFIED]`) or current-code structure (`[CODE-VERIFIED]`), and explicitly marks every concrete throughput/latency expectation as `[DESIGN — UNVERIFIED]`. **No metrics are fabricated. No "measured value" is asserted for the hybrid, because none has been measured.**

### 11.1 Performance Profile

> **Note:** The template's "Measured Value" column is intentionally filled with **"NOT MEASURED — no integrated system exists"** for all hybrid rows. The only genuinely measurable rows describe the *current* Python pipeline's structural performance levers, not the proposed hybrid.

| Metric | Measured Value | Measurement Method | Tag |
|--------|----------------|--------------------|-----|
| Hybrid end-to-end pipeline latency | NOT MEASURED — no integrated system exists | n/a (would require a built spike per XC-13) | `[DESIGN — UNVERIFIED]` |
| Mastra durable suspend/resume overhead | NOT MEASURED for SuperClaude workloads; snapshot cost depends on storage provider + runner choice | Vendor docs describe capability, not benchmarked latency | `[DESIGN — UNVERIFIED]` (capability `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/workflows/suspend-and-resume) |
| Beads `bd ready` scheduling latency | NOT MEASURED for SuperClaude graph sizes | n/a | `[DESIGN — UNVERIFIED]` |
| Backlog.md mutation throughput under concurrent agents | NOT MEASURED; `proper-lockfile` + single-repo git model can contend under true concurrent write load | n/a | `[DESIGN — UNVERIFIED]` (contention risk `[EXTERNAL-VERIFIED]` package.json) |
| Current pipeline parallel step speedup | Documented design property (Wave→Checkpoint→Wave); not re-benchmarked here | Existing executor parallel dispatch | `[CODE-VERIFIED]` `pipeline/executor.py:63-188`, `402-452` |

### 11.2 Characteristics-by-Design (Concurrency, Durability, Single-Writer)

This is the substance of what *can* be said about hybrid performance: directional architectural properties, each tagged by provenance. No numbers are invented.

| Characteristic | By-design behavior | Tag |
|----------------|--------------------|-----|
| Mastra durability vs latency trade | Durable workflows persist a snapshot to storage on suspend; this adds storage I/O per suspend/resume boundary. Production durability/retry semantics depend on runner (built-in / Inngest / Temporal-experimental) and storage backend (ClickHouse recommended for prod observability; libSQL for dev; in-memory resets) | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/workflows/suspend-and-resume ; https://mastra.ai/docs/memory/storage ; https://mastra.ai/docs/deployment/workflow-runners |
| Mastra concurrency / noisy-neighbor | Real per-tenant concurrency isolation / noisy-neighbor protection is NOT in the Apache core — it comes from the Inngest engine integration. OSS-only deployments therefore have weaker concurrency-isolation guarantees | `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY M12) |
| Mastra observability auto-instrumentation | Tracing auto-instruments agent runs, LLM generations, tool calls, workflow steps (token usage, model params) — this is an observability cost AND the primary source for any future hybrid performance measurement | `[EXTERNAL-VERIFIED]` https://mastra.ai/docs/observability/tracing/overview |
| Beads embedded = single-writer | Embedded mode (default) is in-process Dolt, single-writer with file locking; throughput-bound to one writer and yields "database is locked" under contention — solo only | `[EXTERNAL-VERIFIED]` https://github.com/gastownhall/beads/blob/main/docs/DOLT.md |
| Beads server = multi-writer | Server mode (`dolt sql-server`) supports multiple concurrent writers; REQUIRED for any parallel/multi-agent throughput. Atomic claim via `bd update <id> --claim` serializes acquisition | `[EXTERNAL-VERIFIED]` DOLT.md ; FAQ.md |
| Beads operational stability cost | Dolt-only line has documented instability (orphaned `dolt sql-server` daemons, nil-pointer panics in `bd ready`/`bd list`, migration PK forks blocking `bd dolt pull`) — a reliability-affecting performance consideration, not a throughput number | `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY BD10; issue #2938) |
| Backlog.md single-trust-domain | Local-file/git-centric; single-writer-per-repo git model contends under true concurrent multi-user write load; one-task-per-agent/session discipline needed | `[EXTERNAL-VERIFIED]` https://github.com/MrLesk/Backlog.md ; package.json |
| Current pipeline gate evaluation | `gates.py` is pure-Python validation (no subprocess/LLM) — cheap, deterministic, runtime-agnostic; the most portable and lowest-overhead layer | `[CODE-VERIFIED]` `pipeline/gates.py:1-17`, `20-76` |
| Current parallel dispatch | `_run_parallel_steps()` runs a group in daemon threads with shared cancellation; `prd`/`eval` use `ThreadPoolExecutor` (eval default 8 workers, 1-15; prd `max_workers=min(steps,10)`) — the existing concurrency model the hybrid must preserve or improve | `[CODE-VERIFIED]` `pipeline/executor.py:402-452`; `eval/orchestrator.py:113-360`; `prd/executor.py:862-958` |

### 11.3 Performance-Critical Code (Current System — Levers to Preserve)

The hybrid's performance ceiling is set by how faithfully it preserves these existing levers. These are `[CODE-VERIFIED]`; their post-port performance is `[DESIGN — UNVERIFIED]`.

| Area | Optimization | Why It Matters | Location | Tag |
|------|-------------|----------------|----------|-----|
| Subprocess prompt delivery | Prompt delivered via stdin (not argv) to avoid Linux `MAX_ARG_STRLEN` | Large prompts would fail on argv; stdin is the safe path the Mastra Workspace substitute must replicate | `pipeline/process.py:73-78`, `97-112` | `[CODE-VERIFIED]` |
| Gate target selection | `_gate_target()` prefers sibling `.compressed.md` over original output | Gates validate what the downstream LLM actually consumes; cheaper + correct | `pipeline/executor.py:23-35` | `[CODE-VERIFIED]` |
| Turn budgeting | `TurnLedger` pre-debits min allocation, reconciles after; budget-gated launches | Bounds cost/turn consumption per phase; the cost-control lever | `sprint/executor.py:927-1073`, `models.py:693-776` | `[CODE-VERIFIED]` |
| Trailing (non-blocking) gates | Trailing-mode steps return PASS immediately; pending results collected at pipeline end | Avoids blocking the critical path on advisory checks — but `grace_period` defaults to 0, forcing BLOCKING in practice (must be preserved/flagged, not silently fixed) | `pipeline/executor.py:250-262`, `211-215` | `[CODE-VERIFIED]` |
| Result caching (audit) | Content-hash `ResultCache` (SHA-256) avoids re-running identical classifications | Skips redundant work; a reuse pattern the hybrid could extend | `audit/tool_orchestrator.py:61-224` | `[CODE-VERIFIED]` |

### 11.4 Measurement Plan (Required Before Any Performance Claim) `[DESIGN — UNVERIFIED]`

Because nothing is measurable today, the only honest "performance" content is *how* the hybrid would be measured. The decisive early gate is G2 / SG1: prove Mastra durable subprocess supervision parity and rerun/recovery/durability (evidence index XC-12, XC-13).

| To be measured | Via | Gate | Tag |
|----------------|-----|------|-----|
| Mastra suspend/resume + partial-rerun overhead on a real SuperClaude tasklist | Time-boxed validation spike wrapping `superclaude tasklist validate` (smallest single strict-gate, non-destructive) | SG1 / Pilot G2 | `[DESIGN — UNVERIFIED]` (XC-12/XC-13) |
| Tasklist round-trip latency into Backlog.md + Beads | Round-trip parser validation spike | SG2 | `[DESIGN — UNVERIFIED]` (XC-12) |
| Beads server-mode + Dolt sync throughput on pinned version | `bd doctor` + backup/restore + push/pull smoke under load | SG3 | `[DESIGN — UNVERIFIED]` (XC-12) |
| Multi-tenant cost/identity overhead | Governance-plane prototype with per-invocation metering (model tokens + tool calls by tenant/team/task) | SG4 | `[DESIGN — UNVERIFIED]` (XC-12; cost attribution is non-native — RISK R8) |

> **Bottom line for Section 11:** Any reader seeking throughput, latency, or speedup numbers for the hybrid will find none here, by design — they do not exist and will not until the Phase 0-2 validation spike runs. The substrate-level concurrency and durability *directions* above are the most that current evidence supports.

---

## Cross-Section Tag Summary

| Section | Dominant tags | Notes |
|---------|---------------|-------|
| §9 Configuration | `[EXTERNAL-VERIFIED]` (licensing, version pins, modes) + `[CODE-VERIFIED]` (current config surfaces) + `[DESIGN — UNBUILT]` (hybrid config) | Licensing (Mastra OSS/EE), Beads v1.0.5 pin + embedded/server, Backlog.md `--no-git`/v1.45.2 all cite URLs |
| §10 Error Handling & Recovery | `[EXTERNAL-VERIFIED]` (suspend/resume, cycle rejection) + `[CODE-VERIFIED]` (verify-checkpoints, eval HOME/forensic JSONL) + `[DESIGN — UNBUILT]` (checkpoint-recovery, drift-detection) | Recovery surfaces carry real `path:line` |
| §11 Performance | `[DESIGN — UNVERIFIED]` (all hybrid metrics) + `[EXTERNAL-VERIFIED]` (substrate concurrency/durability direction) + `[CODE-VERIFIED]` (current levers) | NO fabricated metrics; explicit "NOT MEASURED" |

**Status: Complete.**
