# Mastra + Backlog.md + Beads Hybrid Orchestration Architecture — Technical Reference (§12-14)

> **Synthesis fragment:** Sections 12 (Conventions & Patterns), 13 (Extension Guide), and 14 (Known Limitations & Technical Debt) of the Technical Reference for the **PROPOSED** Mastra + Backlog.md + Beads hybrid, adapter-first orchestration architecture.

| Field | Value |
|-------|-------|
| **Status** | In Progress |
| **Date** | 2026-06-03 |
| **Code baseline (BUILT side)** | HEAD `9e864860` |
| **Sections in this fragment** | §12 Conventions & Patterns, §13 Extension Guide, §14 Known Limitations & Technical Debt |

### Evidence tag legend (R2 — exactly one tag per claim)

| Tag | Meaning |
|-----|---------|
| `[CODE-VERIFIED]` | Existing Python in `src/superclaude/` at HEAD `9e864860`; carries a real `path:line`. |
| `[DESIGN — UNBUILT]` | Target hybrid architecture; describes what the port would do. **No Mastra/Backlog.md/Beads integration exists in the repo today.** |
| `[EXTERNAL-VERIFIED]` | External substrate capability/constraint from web research (web-01 Mastra, web-02 Backlog.md, web-03 Beads, web-04 MCP/governance) with source URLs. |

> **Path-root convention:** bare `pipeline/…`, `sprint/…`, `roadmap/…`, `tasklist/…`, `cli_portify/…` paths are relative to `src/superclaude/cli/` (e.g. `process.py:76-78` resolves to `src/superclaude/cli/pipeline/process.py`), matching the evidence index. `core/…` and `commands/…`/`agents/…` README paths are relative to `src/superclaude/`.

> **CRITICAL:** Section 13 recipes describe the **proposed** architecture. Every step that touches Mastra/Backlog.md/Beads is `[DESIGN — UNBUILT]`. The existing-side files those recipes hook into are real and `[CODE-VERIFIED]`.

---

## 12. Conventions & Patterns

The proposed hybrid inherits its conventions from the **existing Python orchestration core**, which is already contract-first, artifact-centric, and runtime-agnostic. The port preserves these patterns rather than inventing new ones; the few genuinely new conventions (work-of-record split, file-first carried into Backlog/Beads) are `[DESIGN]` and clearly marked. A developer or AI agent extending this architecture MUST follow these rules of the road.

### 12.1 Code Conventions

| Convention | Description | Anchor | Tag |
|------------|-------------|--------|-----|
| Runtime-agnostic core (NFR-007) | `pipeline/models.py`, `executor.py`, `gates.py` import only stdlib + pipeline-local symbols — **zero** imports from `sprint`/`roadmap`. Any new shared contract goes in `pipeline/`, never reaches up into a consumer. | `models.py:1-14`, `executor.py:7`, `gates.py:1-17` | `[CODE-VERIFIED]` |
| Pure-Python gates (NFR-003) | Gate validation never spawns a subprocess or calls an LLM. `gates.py` imports only `re`/`Path`/`GateCriteria`. New gates are pure data + pure functions returning `tuple[bool, str\|None]`. | `gates.py:1-17`, `gates.py:20-76` | `[CODE-VERIFIED]` |
| Prompt via stdin, not argv | `ClaudeProcess` delivers the prompt on stdin to dodge Linux `MAX_ARG_STRLEN`; never pass a large prompt as a CLI arg. | `process.py:76-78`, `136-139` | `[CODE-VERIFIED]` |
| Env hygiene at the seam | `build_env()` strips `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` before spawning the child so nested Claude detection does not misfire. | `process.py:97-112` | `[CODE-VERIFIED]` |
| Timeout sentinel `124` | A timed-out step returns exit `124` (matches bash `timeout`); callers branch on `124 → TIMEOUT`, nonzero → `FAIL`. | `process.py:163-165` | `[CODE-VERIFIED]` |
| Runner-authored truth | `TaskResult`/`StepResult` are constructed by the runner from observed exit codes/artifacts — **never** self-reported by the agent. Preserve this when porting. | `sprint/models.py:158-209`, `pipeline/executor.py:230-238` | `[CODE-VERIFIED]` |
| Always `--json` to Beads | Every `bd` invocation in the adapter uses `--json` (stable schema v1; opt into `BD_JSON_ENVELOPE=1` for the uniform envelope). Parse the envelope, never scrape human text. | web-03 `docs/JSON_SCHEMA.md` | `[EXTERNAL-VERIFIED]` |
| Backlog.md supported-fields only | Backlog.md MCP task schemas set `additionalProperties:false`; SuperClaude custom metadata MUST map to supported fields/body sections/docs, never arbitrary MCP props. | web-02 `src/mcp/tools/tasks/schemas.ts` | `[EXTERNAL-VERIFIED]` |
| Edit `src/superclaude/` first | Source-of-truth is `src/superclaude/`; `.claude/` and `plugins/superclaude/` are synced/mirror copies. Never ingest mirrors as canonical (see §14, `plugins/` is a stale subset). | `core/CLAUDE.md:17-48` | `[CODE-VERIFIED]` |

### 12.2 Architectural Patterns

| Pattern | Where Used (BUILT) | Description | Tag |
|---------|--------------------|-------------|-----|
| **Single runtime seam** | `ClaudeProcess` behind the injected `StepRunner` protocol | The *only* `subprocess.Popen` / `claude --print` boundary in the pipeline package. The executor never touches a subprocess directly — it delegates through `run_step`. Swapping the Claude-CLI runtime for a Mastra-supervised one is a single substitution at this seam. | `process.py:24-244`, `executor.py:41-60` — `[CODE-VERIFIED]`; Mastra substitution — `[DESIGN — UNBUILT]` |
| **Generic step/gate pipeline core** | `execute_pipeline()` consumed by roadmap, tasklist, validate | One portable unit (`Step`) + one sequencer (`execute_pipeline`) with retry/gates/parallel dispatch; consumers inject a `run_step`. Nested `list[Step]` = parallel group. | `executor.py:63-188`, `models.py:108-123`; consumer proof `roadmap/executor.py:26`, `tasklist/executor.py:259-263` | `[CODE-VERIFIED]` |
| **Strangler-fig replatforming** | Roadmap (Phases 0-5, gates G0-G5) | Wrap one existing pipeline at a time behind a Mastra workflow that shells out to the current CLI; keep Python as the oracle; reimplement natively only after a step passes a parity gate. NOT a big-bang rewrite (Option B rejected). | ROADMAP Phase 1-3; cli-portify cautionary precedent `06-docs` §evolution | `[DESIGN — UNBUILT]` (target); precedent `[CODE-VERIFIED]` |
| **Python-as-oracle parity gating** | Phases 1-3 acceptance suites | At every phase the Mastra-wrapped verdict must equal the native CLI verdict (artifact/gate-mode/order/recovery parity) before native reimplementation is allowed. Gate G2 is the load-bearing exit: Mastra rerun/recovery must be demonstrated. | ROADMAP Gate G2/G3; FEASIBILITY §8 | `[DESIGN — UNBUILT]` |
| **Stable-ID contract** | sprint parser, tasklist protocol, deviation registry | `TASK-*`, `T<PP>.<TT>`, `D-####`, `D-CP...`, `R-###` are the cross-system sync keys. Adapters preserve IDs verbatim; idempotent imports are keyed on them. | `sprint/config.py:374-377`, `sc-tasklist-protocol/SKILL.md:161-164` — `[CODE-VERIFIED]`; cross-system reuse — `[DESIGN — UNBUILT]` |
| **Work-of-record split** | Proposed ownership matrix | Backlog.md owns prose/task/doc/decisions (primary human-readable work-of-record); Beads owns the dependency-graph mirror + agent memory + ready-queue + gates; Mastra owns run/trace/gate-execution state. Exactly one prose owner, one graph owner, one run owner. | ownership matrix (synthesis); web-02/web-03 | `[DESIGN — UNBUILT]` |
| **Fan-out → consolidate → verify** | prd, eval, audit | Tier-sized parallel fan-out (ThreadPoolExecutor), per-future exception → ERROR step (never dropped), then deterministic consolidation and a calibrated validation stage that asserts self-agreement (NOT ground-truth accuracy). | `prd/executor.py:862-958`, `eval/orchestrator.py:113-360`, `audit/validation.py:42-151` | `[CODE-VERIFIED]` |
| **File-first artifacts** | sprint, roadmap, MDTM tasks | Handoff state lives in the filesystem (release dir, task subdirs, `manifest.json`, `execution-log.jsonl`, checkpoint reports, `.compressed.md` sidecars). Gates validate the file the downstream LLM actually consumes (`.compressed.md` preferred over original). | `executor.py:23-35`, `02_mdtm_template_complex_task.md:718-731` — `[CODE-VERIFIED]`; carried into Backlog/Beads bodies — `[DESIGN — UNBUILT]` |
| **Numbered-checkpoint contract** | tasklist protocol + sprint checkpoint parser | Canonical form is numbered `### T<PP>.<NN> -- Checkpoint:` tasks with `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...`. The runtime parser accepts both numbered and legacy `### Checkpoint:`; new generators MUST emit the numbered form. | `sc-tasklist-protocol/SKILL.md:343-391`, `checkpoints.py:22-33` | `[CODE-VERIFIED]` |
| **Return-contract bridge** | cli-portify | Every path emits a `return-contract.yaml` (outcome / completed_steps / remaining_steps / suggested_resume_budget / resume_command) — the natural bridge to a Backlog/Beads reconciliation record. | `cli_portify/executor.py:283-372` — `[CODE-VERIFIED]`; Backlog/Beads bridge — `[DESIGN — UNBUILT]` |

### 12.3 Anti-Patterns (Things to Avoid)

| Anti-Pattern | Why It's Wrong | Do This Instead | Tag |
|--------------|----------------|-----------------|-----|
| Big-bang native rewrite (Option B) | XL effort + High risk; converts pure-Python reuse into rewrite-and-re-test; the in-house cli-portify code-gen-drift history is a direct warning. | Strangler-fig: wrap one pipeline, prove parity, then port. | `[DESIGN — UNBUILT]` / `[CODE-VERIFIED]` (precedent) |
| Second prose owner | Backlog.md + Beads both representing task status causes drift; their mutual integration is immature (Backlog FR #588). | Assign canonical owner per data class (one prose, one graph). | `[EXTERNAL-VERIFIED]` |
| Beads embedded mode for multi-agent | Embedded Dolt is single-writer ("database is locked"); concurrent agents corrupt/serialize. | Beads **server mode** + atomic `bd update --claim` + one-task-per-agent. | `[EXTERNAL-VERIFIED]` |
| Unpinned Beads/Dolt upgrades | v1.0.5 "do not upgrade" (migration 0043 breaks multi-machine sync, #4259); v1.0.4 server data-clobber. | Pin + gate versions; `bd doctor` + tested backup/restore in adoption gates. | `[EXTERNAL-VERIFIED]` |
| Treating MCP as governance | MCP is a tool-exchange protocol, explicitly NOT a governance platform; token passthrough is forbidden. | Add a dedicated control-plane (tenant registry, RBAC/ABAC, audit, cost) + MCP gateway with scoped tools. | `[EXTERNAL-VERIFIED]` |
| Telemetry into task bodies | High-volume `MonitorState` telemetry (bytes/tokens/turns/events) does not belong in the task-of-record. | Route telemetry → Mastra traces (with SuperClaude IDs as custom attributes); keep Backlog/Beads bodies lean. | `sprint/models.py:622-690` `[CODE-VERIFIED]` / `[DESIGN — UNBUILT]` |
| Scraping `plugins/` or `.claude/` as source | `plugins/superclaude/` is a stale, divergent subset (30 cmd / 20 agent / 1 skill vs 42/39/24); `.claude/` is sync output. | Ingest `src/superclaude/` only. | `core/CLAUDE.md:17-48` `[CODE-VERIFIED]` |
| Arbitrary MCP fields on Backlog tasks | Backlog.md MCP rejects unknown properties (`additionalProperties:false`). | Map metadata to supported fields/body sections/docs. | `[EXTERNAL-VERIFIED]` |

---

## 13. Extension Guide

> **CRITICAL:** These recipes are `[DESIGN — UNBUILT]` against the proposed hybrid. **No Mastra/Backlog.md/Beads integration exists at HEAD `9e864860`.** Each recipe is written as a strangler-fig increment: the *existing-side* files you hook into are real (`[CODE-VERIFIED]` paths); the Mastra/Backlog/Beads steps are the target design. Sequence them against the roadmap — read-only adapters (Phase 1) before wrapping a pipeline (Phase 2) before the parity port (Phase 3). Do not skip the parity gate.

### 13.1 Common Extension Tasks

#### Recipe A — Add a wrapped pipeline (strangler-fig increment)

**Goal:** Put an existing SuperClaude CLI pipeline behind a Mastra workflow without changing its behavior, proven at parity. **Start with the smallest:** `superclaude tasklist validate` — single LLM step, one strict gate, non-destructive (the Phase 2 pilot).

| # | Step | Existing-side file / registration point | Tag |
|---|------|------------------------------------------|-----|
| 1 | Pick the pipeline. Pilot = tasklist validate: one `tasklist-fidelity` Step gated by `TASKLIST_FIDELITY_GATE`, CLI pass/fail = `not _has_high_severity()`. | `tasklist/executor.py:191-218` (build_steps), `221-248` (`_has_high_severity`), `tasklist/gates.py:23-46` (gate) | `[CODE-VERIFIED]` |
| 2 | Identify the adapter contract = the `StepRunner` seam. The pipeline already routes execution through `execute_pipeline(..., run_step=...)`; the Mastra wrapper substitutes a workflow node that shells out to the existing CLI. | `pipeline/executor.py:41-60` (`StepRunner`), `63-188` (`execute_pipeline`); consumer `tasklist/executor.py:259-263` | seam `[CODE-VERIFIED]`; Mastra node `[DESIGN — UNBUILT]` |
| 3 | Build the Mastra workflow: `createWorkflow()` + one `createStep()` whose handler invokes `superclaude tasklist validate ...` via Workspace `executeCommand`. | Mastra `createWorkflow`/`createStep` (web-01); Workspace sandbox (web-01) | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| 4 | **Mirror the gate as the parity-gate step.** Re-express the CLI gate verdict as a Mastra scorer, then assert `Mastra verdict == native CLI verdict`. The native verdict comes from parsing `high_severity_count` from the report frontmatter. | `tasklist/executor.py:221-248`; gate semantics `pipeline/gates.py:20-76` | parity assertion `[DESIGN — UNBUILT]`; native verdict `[CODE-VERIFIED]` |
| 5 | Validate durability: suspend/resume + failed-step restart through Mastra `suspend()`/`resume()`/`resumeStream()`. **This is Gate G2 — the load-bearing exit.** | Mastra suspend/resume (web-01) | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| 6 | Run the subprocess-safety spike using the existing `eval/isolation.py` HOME-isolation model as the parity target (three-check containment guard). | `eval/isolation.py:224-260`, `456-747` | target `[CODE-VERIFIED]`; Mastra parity `[DESIGN — UNBUILT]` |
| 7 | Reconcile results back into Backlog.md + Beads via the return-contract bridge pattern. | `cli_portify/executor.py:283-372` (return-contract precedent) | bridge `[CODE-VERIFIED]`; Backlog/Beads write `[DESIGN — UNBUILT]` |

**Pitfalls:** Do NOT reimplement the gate logic in TypeScript on first pass — shell out and compare. Gate validates the `.compressed.md` sidecar if present (`executor.py:23-35`), so the Mastra scorer must target the same file. `grace_period=0` coerces declared `TRAILING` gates to BLOCKING (`executor.py:212-214`) — preserve that effective behavior, do not "fix" it silently.

#### Recipe B — Add a Beads gate (external-state barrier)

**Goal:** Encode a "done vs merged/validated/approved" barrier as a Beads gate so the graph blocks until an external condition clears. Maps the SuperClaude notion that a task can be code-complete but not merged/CI-green/approved.

| # | Step | Reference | Tag |
|---|------|-----------|-----|
| 1 | Choose the gate type. Beads supports: `gh:pr` (PR merged), `gh:run` (CI run), `timer` (elapsed time), `bead` (cross-rig dependency on another bead), `human` (manual approval). | web-03 `docs/DEPENDENCIES.md` | `[EXTERNAL-VERIFIED]` |
| 2 | Decide the SuperClaude barrier to map: roadmap validation pass → `bead`/`human`; PR-merge before phase-complete → `gh:pr`; CI green → `gh:run`; checkpoint soak → `timer`. | `roadmap/validate_executor.py:239-519`; sprint checkpoint model `sprint/checkpoints.py:36-112` | mapping `[DESIGN — UNBUILT]`; existing barriers `[CODE-VERIFIED]` |
| 3 | Create the gate via `bd gate` against the bead representing the task/phase; the bead stays out of `bd ready` until the gate clears. Discover/check with `bd gate check`/`bd gate discover`. | web-03 `docs/DEPENDENCIES.md` (`bd ready` = no open blocking deps) | `[EXTERNAL-VERIFIED]` |
| 4 | The Mastra workflow (or adapter poller) polls `bd ready --json`; only ready beads are dispatched. Claim atomically with `bd update --claim` (sets assignee + in_progress in one op). | web-03 CLI surface (`bd ready`, `bd update --claim`) | `[EXTERNAL-VERIFIED]` |
| 5 | Keep Beads gates orthogonal to the pure-Python `GateCriteria`/`gate_passed` artifact gates — Beads gates govern *graph readiness* (external state); Python gates govern *artifact correctness*. Do not conflate. | `pipeline/gates.py:20-76` | Python side `[CODE-VERIFIED]`; orthogonality `[DESIGN — UNBUILT]` |

**Pitfalls:** Cycles are rejected at write time — design dependency direction carefully. Multi-agent writers REQUIRE Beads server mode (embedded is single-writer). `gh:pr`/`gh:run` gates depend on GitHub state; rate-limit polling and handle transient failures. Pin the Beads version (avoid v1.0.5-class sync corruption).

#### Recipe C — Add a tenant (governance plane)

**Goal:** Onboard a new tenant to the multi-tenant control plane. **This is the heaviest recipe and depends on a layer that does NOT exist in any of the three components** — it is Phase 4 work, gated on decisions D1/D2/D3.

| # | Step | What the governance plane needs | Tag |
|---|------|----------------------------------|-----|
| 1 | Register the tenant in a **tenant registry** (the control-plane service — net-new; not Mastra/Backlog/Beads). | Separate control-plane service: tenant registry. None of the three components supplies this. | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` (gap) |
| 2 | Map the five distinct identities: **trigger / execution / authorization / tenant / attribution.** Access-control bugs surface silently when execution + tenant are conflated; RBAC must be config-driven, not inferred from user messages. | web-04 scalekit access-control guidance | `[EXTERNAL-VERIFIED]` |
| 3 | Add tenant/actor fields to the run models — **they are absent today** (`PipelineConfig`/`SprintConfig`/`TaskResult`/`MonitorState`/`TurnLedger` carry model/permission/budget but no tenant/actor/audit identity). | `pipeline/models.py:212-234`, `sprint/models.py:347-510`, `692-777` | absence `[CODE-VERIFIED]`; new fields `[DESIGN — UNBUILT]` |
| 4 | Wire RBAC/ABAC + scoped MCP tools through an MCP/AI gateway: OAuth 2.1, audience binding, single-issuer pinning, **no token passthrough** (forbidden), granular scopes (no `superclaude:*` wildcard). | web-04 MCP security best practices; CSA minimum maturity | `[EXTERNAL-VERIFIED]` |
| 5 | Promote `TurnLedger` to a **tenant cost model**: per-invocation cost attribution + budget/rate enforcement (model tokens + tool calls by tenant/team/user/agent/workflow/task). Cost attribution is NOT native to MCP. | `sprint/models.py:692-777` (sprint-local ledger); web-04 FinOps | ledger `[CODE-VERIFIED]`; tenant cost model `[DESIGN — UNBUILT]` |
| 6 | Promote Beads to **server/shared mode with per-tenant prefixes**; enforce tenant isolation so no tenant can read another's tasks/traces/costs (Gate G4 NO-GO condition). | web-03 server mode; ROADMAP Phase 4 G4 | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| 7 | Re-validate isolation + audit + cost on a two-tenant test per onboarding (Gate G5 recurring). | ROADMAP Phase 5 G5 | `[DESIGN — UNBUILT]` |

**Pitfalls:** Production RBAC/SSO/FGA/audit/on-prem are **Mastra Enterprise-licensed**, not Apache-2.0 core (R1) — "multi-tenant on Mastra OSS" is false for production RBAC. Without auth, Mastra Studio/API routes are public. Do NOT deploy company-wide on the three components alone — the control-plane service is mandatory and net-new.

### 13.2 Testing Requirements for Changes

| Change Type | Required Tests | Reference (existing harness to reuse) | Tag |
|-------------|----------------|----------------------------------------|-----|
| Wrap a pipeline (Recipe A) | Round-trip parser parity; Mastra verdict == native CLI verdict; suspend/resume + failed-step restart; subprocess-safety parity report. | `cli/eval` harness (`eval/orchestrator.py`, `eval/isolation.py`, `eval/runner.py`); round-trip vs `discover_phases()`/`parse_tasklist_file()` (`sprint/config.py`) | harness `[CODE-VERIFIED]`; parity suite `[DESIGN — UNBUILT]` |
| Add a Beads gate (Recipe B) | Cycle-rejection test; `bd ready` excludes gated beads until cleared; atomic `--claim` under concurrent writers (server mode); version-pinned `bd doctor` + backup/restore smoke. | web-03 CLI contracts; reuse eval forensic JSONL + retry-once for flaky steps (`eval/retry.py`) | `[EXTERNAL-VERIFIED]` / `[DESIGN — UNBUILT]` |
| Add a tenant (Recipe C) | Two-tenant isolation test (no cross-tenant read of tasks/traces/costs); per-invocation audit record assertion; cost-attribution join via trace IDs; token-passthrough negative test. | net-new; no existing test covers tenancy (absence is the finding) | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| Port a deterministic step natively | Artifact + gate-verdict + gate-mode + order + recovery/resume parity vs the Python oracle BEFORE replacing the shell-out. | `cli/eval` return-contract/artifact diffing; gate semantics `pipeline/gates.py` | parity `[DESIGN — UNBUILT]`; oracle `[CODE-VERIFIED]` |

---

## 14. Known Limitations & Technical Debt

> **CRITICAL — overall status:** The Mastra + Backlog.md + Beads hybrid architecture is **UNBUILT**. No source file at HEAD `9e864860` implements any Mastra/Backlog.md/Beads integration. The feasibility verdict is **Conditionally Recommended**, approach **Option D → Option A** (a time-boxed validation spike — Phases 0-2 / Gates G0-G2 — *then* hybrid adapter-first, only if the spike exit gates SG1-SG4 pass; NOT a native rewrite, NOT Backlog/Beads-only). Confidence ≈70% that hybrid is feasible; ≈55% that full company-wide multi-tenant is deliverable on the three components alone. Deferral is a legitimate outcome. `[DESIGN — UNBUILT]`

### 14.1 Current Limitations (BUILT-side gaps the port must carry, not silently fix)

These are real `[CODE-VERIFIED]` behaviors in the existing orchestrator at HEAD `9e864860`. The roadmap mandates **preserving and flagging** them (state effective-vs-intended separately), not normalizing them during the port.

| # | Limitation | Impact | Anchor | Tag |
|---|-----------|--------|--------|-----|
| L1 | **`CERTIFY_GATE` defined but NOT wired.** `CERTIFY_GATE`/`build_certify_step`/`check_certify_resume` exist; `_build_steps()` terminates at `remediate`; the "Step 12 (certify) constructed dynamically by roadmap_run_step" comment has **zero production callsites**. | Certification gate does not run in production roadmap; downstream "certified" frontmatter is never enforced. Port must preserve the gap (do not auto-wire). | def `roadmap/gates.py:1324-1351`; absent `executor.py:1947-2208`; comment `executor.py:2205`; `ALL_GATES` ref `gates.py:1440` | `[CODE-VERIFIED]` |
| L2 | **Wiring-verification grace=0 → effectively BLOCKING.** `wiring-verification` Step declares `gate_mode=TRAILING` ("shadow mode trailing") but `PipelineConfig.grace_period` defaults to 0 with no CLI override, and `_execute_single_step` coerces `grace_period==0 → BLOCKING`. | The gate runs synchronously/blocking in production despite shadow-trailing intent. Effective behavior ≠ declared behavior. | TRAILING `executor.py:2183`; default `pipeline/models.py:232`; coercion `pipeline/executor.py:211-214` | `[CODE-VERIFIED]` |
| L3 | **Path A skips `_verify_checkpoints()`.** The per-task (parsed) branch aggregates results and `continue`s at `executor.py:1301` with no checkpoint call. The sole `_verify_checkpoints()` call site is `executor.py:1519`, inside the Path B (freeform) branch only. | Checkpoint enforcement does not run for parsed-task phases — silent loss of checkpoint gating on the most common sprint path. Phase 3 must wire it into the per-task path. | Path A `executor.py:1262-1301`; sole call `executor.py:1519`; def `executor.py:1811` | `[CODE-VERIFIED]` |
| L4 | **Deviation classifier UNWIRED.** All deviation records render as `UNCLASSIFIED`; `DEVIATION_ANALYSIS_GATE` actually pins the invariant `unclassified_count == total_analyzed`. | The classifier is not producing classified output in production; the gate encodes the unwired state as the expected state. | `roadmap/executor.py:1603-1609`; gate `gates.py:1390-1422` | `[CODE-VERIFIED]` |
| L5 | **Partial / unused isolation in sprint.** Four-layer `IsolationLayers`/`setup_isolation` EXISTS but is not called in the main loop; Path B only sets `CLAUDE_WORK_DIR`, Path A passes no isolation env. Base process `Popen` has no `cwd` arg, so worker cwd is not guaranteed on Path A. | Sprint isolation guarantees are weaker than the code implies; the Mastra safety-parity target (eval HOME-isolation) is the stronger model to port toward. | `executor.py:106-182`, `1303-1324`, `1076-1115`; `process.py:125-134` | `[CODE-VERIFIED]` |
| L6 | **Stubbed sprint `status`/`logs`.** `SprintLogger` writes JSONL+Markdown (real), but `read_status_from_log`/`tail_log` are STUBS ("not yet connected") — the `status`/`logs` commands do not report live state. | Operator visibility into a running sprint is limited to the TUI/tmux; CLI status/logs are non-functional. | `sprint/logging_.py:13-213`, `224-235` | `[CODE-VERIFIED]` |
| L7 | **Path A turn-counting accuracy gap.** `_run_task_subprocess` returns `turns_consumed=0`; turn counting is wired separately, so per-task turn attribution is approximate. | Budget reconciliation on Path A is imprecise — relevant when promoting `TurnLedger` to a tenant cost model. | `executor.py:1086-1115`; `sprint/models.py:502-506` | `[CODE-VERIFIED]` |
| L8 | **`sprint rerun-tasks` is ABSENT at HEAD.** Tree-wide grep for `rerun-tasks`/`rerun_tasks` returns zero matches; the sprint Click group registers exactly `run/attach/status/logs/kill/verify-checkpoints`. The operator-memory note (v4.3.0) does not correspond to this commit (package is v4.2.0). | Any tech reference or recipe written against HEAD `9e864860` must state `rerun-tasks` ABSENT; the closest recovery surface is `verify-checkpoints` (checkpoint recovery only, not task re-run). | `sprint/commands.py` (6 subcommands, no `rerun`); resolved in spot-03 | `[CODE-VERIFIED]` (absence) |

### 14.2 Technical Debt — Stale / Contradiction Findings (confirmed at HEAD)

Documentation/comment/template drift confirmed against current source. Severity reflects risk that a port silently carries the *stale* statement instead of the *effective* behavior.

| # | Debt item | Severity | Description | Anchor | Tag |
|---|-----------|----------|-------------|--------|-----|
| D1 | Stale `### Checkpoint:` in sprint prompt | Medium | Path B freeform prompt tells the agent to scan for legacy `### Checkpoint:` sections and skip if none exist; does not mention the numbered task-form contract. Stale-but-harmless (Path A never uses this prompt) but misleads a port author. | `sprint/process.py:188-195` | `[CODE-VERIFIED]` |
| D2 | Stale `### Checkpoint:` in verify-checkpoints message | Low | `verify-checkpoints` empty-manifest message names only `` `### Checkpoint:` `` sections; omits `Checkpoint Report Path:` declarations the parser actually supports. | `sprint/commands.py:426` | `[CODE-VERIFIED]` |
| D3 | `src/` vs `plugins/` source-of-truth conflict | High | `core/CLAUDE.md` designates `src/superclaude/` canonical (42 cmd / 39 agent / 24 skill), but `commands/agents/hooks` READMEs say edit `plugins/superclaude/` first. `plugins/` is a materially out-of-sync subset (30/20/1). Ingesting the mirror as canonical would port a stale corpus. | `core/CLAUDE.md:17-48` vs `commands/README.md`, `agents/README.md`, `hooks/README.md`; counts in spot-04 | `[CODE-VERIFIED]` (contradicted) |
| D4 | `_build_steps` "9-step" docstring + duplicate "Step 8" labels | Low | `_build_steps` docstring still says "9-step pipeline" vs 12 wired list elements; inline comments label both spec-fidelity and test-strategy as "Step 8". Cosmetic — ordering is correct and matches research. | `roadmap/executor.py:1948`, `2140`, `2157` | `[CODE-VERIFIED]` |
| D5 | `TrailingGateResult` SPEC-DEVIATION shape | Low | Current shape `(step_id, passed, evaluation_ms, failure_reason)` (roadmap v3.0 authoritative); the older spec `(passed, evaluation_ms, gate_name)` is STALE. Docstring records the deviation. | `pipeline/trailing_gate.py:34-46` | `[CODE-VERIFIED]` (doc-contradicted) |
| D6 | Roadmap "ORIGINAL output file" comment | Low | Roadmap comment says "Gate checks run on the ORIGINAL output file" but `_gate_target()` prefers the `.compressed.md` sidecar. | `roadmap/executor.py:1217-1219` vs `pipeline/executor.py:23-35` | `[CODE-VERIFIED]` (contradicted) |
| D7 | cli-portify resume matrix drift | Medium | `cli_portify/resume.py` legacy matrix uses conceptual step names (analyze-workflow/design-pipeline/synthesize-spec) NOT the current `STEP_REGISTRY` IDs; resume validation contradicts the live registry. Retire duplicated resume matrices on port. | `cli_portify/resume.py:45-95`, `168-198` vs `executor.py:105-183` | `[CODE-VERIFIED]` (contradicted) |
| D8 | cleanup-audit parallel-batch docstring | Low | Docstring claims ThreadPoolExecutor parallel batch dispatch but code runs sequentially (no import); `--pass`/`--batch-size` flags accepted but not applied. | `cleanup_audit/executor.py:11-13`, `72-159`; `commands.py:24-40` | `[CODE-VERIFIED]` (contradicted) |
| D9 | Seed-brief substrate corrections | Medium | Seed-brief framing corrected by web research: Beads is **Dolt-first** (not SQLite+JSONL; `.beads/issues.jsonl` is export-only); `superclaude pipeline` is a shared package, NOT a root Click command; sprint prompt invokes `/sc:task` (not `/sc:task-unified`); ClaudeProcess uses stdin (not argv `-p`). | web-03 `SYNC_CONCEPTS.md`/`DOLT.md`; `cli/main.py:400-426`; `sprint/process.py:170`; `pipeline/process.py:114-147` | `[EXTERNAL-VERIFIED]` / `[CODE-VERIFIED]` |

### 14.3 Technical Debt — Risk Register (R1-R9) and the Four Critical Gaps

The port's debt is dominated by the validated risk register. **Severity** = Impact × Likelihood per RISK-REGISTER.md.

| # | Risk | Severity | Description | Critical-gap link | Tag |
|---|------|----------|-------------|-------------------|-----|
| R1 | License | **High** | Production multi-user RBAC/SSO/FGA/audit/on-prem are Mastra **Enterprise**-licensed (`ee/` dirs), not Apache-2.0 core. Strategic multi-tenant driver hits a budget/procurement gate. | G7 (auth/RBAC/governance/cost) | `[EXTERNAL-VERIFIED]` |
| R2 | Runtime migration | **High** | ~65K-LOC Python orchestration must replatform onto Mastra TS; the `ClaudeProcess` subprocess seam must be replaced; gate/convergence logic is pure Python (rewrite-and-re-test risk). | **G3** (subprocess/Claude-Code parity) | `[CODE-VERIFIED]` (risk) |
| R3 | Backlog/Beads overlap | **High** | Dual task/status owners cause drift; mutual integration immature (Backlog FR #588). Assign canonical owners (D1). | — | `[EXTERNAL-VERIFIED]` |
| R4 | Beads/Dolt version churn | **High** | v1.0.5 "do not upgrade" sync corruption (migration 0043, #4259); v1.0.4 server data-clobber. Pin + gate versions; tested backup/restore. | — | `[EXTERNAL-VERIFIED]` |
| R5 | Concurrency / multi-writer | **High** | Beads embedded mode is single-writer; multi-agent needs server mode; session attribution churning (#3400/#3583). Atomic `--claim` + one-task-per-agent. | — | `[EXTERNAL-VERIFIED]` |
| R6 | Subprocess / hook safety parity | **High** | Mastra Workspace `executeCommand` does NOT replicate Claude Code hooks/freshness/staging/permissions; UV-only, git-safety, `.claude/` SoT, fork-PR target must be rebuilt as middleware. | **G3** + **G4** (hook/safety parity) | `[EXTERNAL-VERIFIED]` |
| R7 | Checkpoint / wiring drift | **Medium-High** | Stale legacy `### Checkpoint:` refs (D1/D2 above), per-task skips `_verify_checkpoints()` (L3), certify maybe unwired (L1), trailing grace=0 forces blocking (L2). Adopt numbered contract; state effective-vs-intended. | — | `[CODE-VERIFIED]` (risk) |
| R8 | Governance / tenancy / cost gaps | **High** | None of the three components supplies tenant isolation, per-invocation audit, cost attribution, policy/approval/catalog. MCP is a protocol, not governance. Net-new control-plane required. | **G6** (tenant state) + **G7** (auth/RBAC/governance/cost) | `[EXTERNAL-VERIFIED]` |
| R9 | Fast-moving external tools | **Medium-High** | Mastra `@core` 1.1.0+ / Temporal experimental; Backlog v1.45.2 MVP + doc drift + bug #578; Beads 1.x frequent CLI/API changes. Pin versions; runtime-verify schemas. | — | `[EXTERNAL-VERIFIED]` |

**The four Critical gaps** cluster into two areas:

| Gap | Description | Maps to | Tag |
|-----|-------------|---------|-----|
| **G3** | Subprocess / Claude-Code execution parity cannot be assumed portable — the `ClaudeProcess` seam + Claude-Code-native runtime behavior. | R2 / R6 | `[CODE-VERIFIED]` (linkage) / `[EXTERNAL-VERIFIED]` |
| **G4** | Hook / safety parity (UV-only, freshness, staging, fork-PR, permissions) is not provided by Mastra defaults. | R6 | `[CODE-VERIFIED]` / `[EXTERNAL-VERIFIED]` |
| **G6** | Tenant state — current models carry no tenant/actor/audit identity (`PipelineConfig`/`SprintConfig`/`TaskResult`/`MonitorState`/`TurnLedger`). | R8 | `[CODE-VERIFIED]` (absence) |
| **G7** | Auth / RBAC / governance / cost control plane does not exist in any of the three components. | R1 / R8 | `[EXTERNAL-VERIFIED]` |

### 14.4 Future Considerations (deferred by design)

| Item | Deferred Because | Revisit When | Tag |
|------|------------------|--------------|-----|
| Native (non-shell-out) reimplementation of deterministic steps | Hybrid keeps Python as the oracle; native conversion concentrates parity risk. | Only per-step, after that step passes the Phase 3 parity suite. | `[DESIGN — UNBUILT]` |
| Full multi-tenant control plane | EE-licensing (D2) + governance-ownership (D3) decisions unresolved; ≈55% confidence on three components alone. | Phase 4, gated on D1+D2+D3 and a passing two-tenant isolation/audit/cost test (G4). | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| `roadmap run` + sprint wrap | Too much surface for a first slice; pilot is `tasklist validate`. | Phase 3, after Gate G2 (Mastra durability/rerun/recovery) passes. | `[DESIGN — UNBUILT]` |
| Backlog.md ↔ Beads native sync | Integration immature (FR #588); maintainer suggests a narrow import/export decision first. | After D1 (primary work-of-record) is recorded; start with one narrow sync workflow. | `[EXTERNAL-VERIFIED]` |
| Five gating decisions D1-D5 | Phase 0 outputs; all later mappings depend on them. | Phase 0 / Gate G0 (D1 + D4 mandatory before Phase 1). | `[DESIGN — UNBUILT]` |

---

**Status: Complete**
