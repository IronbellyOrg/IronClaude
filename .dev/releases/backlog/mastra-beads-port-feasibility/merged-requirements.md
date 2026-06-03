---
topic: "Stack D (Mastra + Backlog.md + Beads) port feasibility for the SuperClaude CLI orchestration pipeline"
domain: architecture
strategy: enterprise
depth: deep
proposals: 4
convergence_score: 0.82
adversarial_status: pass
base_proposal: "Proposal D (reuse-maximizing) + Proposal C (strangler-fig) fusion"
created: 2026-06-02T21:51:00+00:00
source_seed: seed-brief.md
generated_by: /sc:brainstorm --depth deep --research deep --proposals 4
---

# Feasibility Study & High-Level Roadmap: Replatforming SuperClaude/IronClaude Orchestration onto Stack D (Mastra + Backlog.md + Beads)

**Decision document for engineering leadership — company-wide multi-tenant orchestration replatforming go/no-go**
**Status: convergence 0.82 across four independent proposals; recommendation HYBRID (conditional go)**
**Date: 2026-06-02**

---

## 1. Executive Summary & Recommendation

**Recommendation: HYBRID — a conditional, strangler-fig go, gated on a dual Phase-0 spike. Not an unconditional go; not a defer.**

The decisive, code-verified finding is that the SuperClaude/IronClaude codebase was **already built for runtime substitution**. The generic sequencer (`pipeline/executor.py`) runs against an injected `StepRunner` Protocol; `roadmap/executor.py` already wraps the runtime behind a `claude_process_factory` + `_ClaudeRunner` adapter (`roadmap/executor.py:1271-1279`); and only **~1.2K of ~73K LOC is genuinely Claude-Code-coupled** (`pipeline/process.py` ~245 + `sprint/process.py` ~385 + `sprint/monitor.py` ~570). The other **~62K LOC** — gate logic, the convergence engine, the FMEA suite, the audit suite, structural/semantic checkers, domain models, and the entire Markdown skill/agent harness — is runtime-agnostic Python/Markdown with **zero subprocess or Claude coupling** (verified: `roadmap/gates.py`, `roadmap/convergence.py`, `audit/wiring_gate.py` carry only `TYPE_CHECKING` imports). This is therefore a **seam swap of ~1.2K LOC, not a 65K-LOC rewrite** — which is what makes the project feasible at acceptable risk. We proceed by replacing only the `ClaudeProcess`/stream-json seam with an ACP driver, keeping the Python domain layer behind an MCP/HTTP boundary, running the new path **in parallel with the existing CLI under a 5%-tolerance acceptance gate**, and **deferring Mastra Server and the Enterprise-Edition (EE) licensing decision to the final phase** — because the strategic driver (multi-tenant RBAC) is EE-paid and sits *outside* the reuse story, meaning Phases 0–4 can fully succeed and still not deliver the company goal without a separate funded EE-buy-vs-DIY decision.

**Headline V/C/L/R** (0–40 scale; Likelihood higher = better, Complexity/Risk higher = worse):

| Value | Complexity | Likelihood | Risk |
|---|---|---|---|
| **33** | **30** | **29** | **26** |

The prize is real — ~62K LOC of differentiated IP unlocked for multi-tool, multi-user reuse — but capped because much of that value already works today; the *net new* value is multi-tenancy + multi-tool, which is significant but not existential. The seam analog (`@mastra/acp` `AcpAgent`) is near-exact, which is why Likelihood is high *for the seam swap*; it is materially lower for the full multi-tenant goal, which depends on unverified ACP parity, unverified per-tool support, EE cost, and Mastra API churn. **The entire recommendation is conditional on a Phase-0 spike that has not yet been run.**

---

## 2. Current-State Architecture

SuperClaude/IronClaude is a **~73K-LOC Python orchestration layer** driving the Claude Code CLI. It decomposes into three strata:

- **Stratum 1 — portable IP (~50–62K LOC):** pipeline base types and sequencer, the FMEA analysis suite (classifier/domains/invariants/dataflow/guards/conflicts/state), the static audit suite (`audit/*`, ~6.7K LOC), sprint/roadmap/tasklist domain models, the checkpoint system, the convergence engine (`DeviationRegistry` + 3-cycle convergence loop), semantic/structural checkers, the deterministic cosmetic remediator, all 24 `SKILL.md` files, and all 39 agent `.md` personas. Pure Python or Markdown, **zero Claude runtime coupling**.
- **Stratum 2 — adaptable orchestration (~12K LOC):** `sprint/executor.py` (~2150 LOC flagship loop) and `roadmap/executor.py` (~3700 LOC, the largest file). These contain `ClaudeProcess` coupling, but the orchestration *logic* (TurnLedger budget accounting, gate enforcement, convergence control, parallel dispatch with cancellation, stall watchdog) is pattern-portable.
- **Stratum 3 — Claude-Code-specific (~11K LOC):** `ClaudeProcess` + sprint subclass, the stream-json monitor, tmux/TUI, the `install_hooks/commands/agents/mcp` plumbing, and prompt files.

**The runtime seam (`pipeline/process.py::ClaudeProcess`)** is the single point of coupling. It builds and spawns:

```
['claude','--print','--verbose', <permission_flag>, '--no-session-persistence',
 '--tools','default','--max-turns',N,'--output-format','stream-json'|'text','--model',M]
```

via `subprocess.Popen` (`process.py:114-146`), delivering the prompt over **stdin** (to bypass Linux `MAX_ARG_STRLEN`), setting `os.setpgrp` for kill-tree teardown, and **stripping `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`** to defeat nested-session detection. `sprint/monitor.py` then tails the NDJSON `stream-json` output in a background thread, reconstructing **turns, tokens, tool calls, errors, and stall timing** — the signals that feed the `TurnLedger` economic model (`initial_budget = max_turns × active_phases`) and the stall watchdog.

**Critical correction to the architectural base (from codebase verification):** the sprint flagship is *not* substitution-clean. Its seam is a **private `_subprocess_factory` test-injection hook with a hardcoded `ClaudeProcess` default** (`sprint/executor.py:1324`), **not** a first-class `StepRunner` Protocol, and it is entangled with the monitor/TUI/tmux/`TurnLedger` machinery. The `delegate_runner` branch claimed in one proposal **does not exist**. Consequence: the `pipeline`/`roadmap` "built-for-substitution" thesis is solid, but **sprint Phase 2 carries real rewrite risk and must be sized very-high, not low-adapt.**

---

## 3. Target Stack D Assessment

Confidence per the supplied research: Mastra **medium**, Backlog.md **high**, Beads **high**.

### 3.1 Mastra (TypeScript agent/workflow runtime) — the runtime + multi-tenant front

**Verified:**
- **Maturity:** `@mastra/core` reached 1.0.0 on 2026-01-20; subsequent releases through 1.16.0 (2026-03-23). ACP support requires **`@mastra/core >= 1.34.0`**. ~22k stars, ~300k weekly npm downloads at 1.0. **UNVERIFIED:** the exact current-latest core version (floor `>=1.34.0` is confirmed; head is not).
- **License:** **Apache-2.0** for the main framework. Verified carve-out: anything under any `ee/` directory is governed by a custom **Mastra Enterprise Edition License** — production use requires a written commercial agreement; redistribution/sale forbidden.
- **Runtime-seam match (the decisive finding):** `@mastra/acp` provides **`AcpAgent`**, which spawns an ACP-compatible coding-agent CLI as a subprocess subagent (fields: `command`, `args`, `cwd`, `workspace`, runtime `model` selection; `persistSession` default true; `AcpAgent.stream()` emits normalized text-delta chunks). The documented example drives Claude Code via `npx -y @agentclientprotocol/claude-agent-acp`. **This is the exact structural replacement for `ClaudeProcess`.**
- **Durable workflows:** `createWorkflow`/`createStep` with `.then`/`.branch`/`.parallel`/`.foreach({concurrency})`/`.dountil`; Zod-typed step IO; **`suspend()`/`resume()` snapshots** persisted to Postgres/LibSQL — a direct functional analog of MDTM checkpoints + recoverable reruns.
- **Service + observability:** Mastra Server exposes agents/workflows/tools/MCP as HTTP endpoints; `@mastra/observability` is OpenTelemetry-native with per-run token/cost/turn attribution.
- **Multi-tenancy / RBAC (the strategic blocker):** `server.auth` SimpleAuth (API-key→role) is **license-free**. **SSO (WorkOS/Okta), `StaticRBACProvider`, default roles, permission-based Studio UI, and Agent Builder import from `@mastra/core/auth/ee` and require a paid EE license for production.** Tenant-fair concurrency/backpressure is not a core primitive — it comes from the Inngest engine integration.

**Gaps:** RBAC/multi-tenancy is EE-paid (the whole strategic driver); ~62K LOC of domain logic is *not* replaced by Mastra (it is a Python→TS migration or a permanent Python-behind-MCP boundary); Claude-Code hooks have no Mastra equivalent; verified API churn 1.0→1.16 (codemods, `getAgents→listAgents`, telemetry overhaul, Node 22.13 floor).
**UNVERIFIED:** whether `@mastra/acp` itself is Apache or sits under `ee/` (material to the Mastra-early-vs-late fork); ACP parity for `max_turns`/permission flags/`CLAUDE_WORK_DIR`; per-tool ACP parity for Cursor/Gemini/Copilot (Mastra docs name only Claude Code/Amp/Codex).

### 3.2 Backlog.md (markdown task-of-record) — MIT

**Verified:** v1.45.2 (2026-05-30); **MIT**; TypeScript/Bun; **built-in spec-aligned MCP server** (`backlog mcp start`; BACK-407 merged in v1.43.0; actively maintained through late May 2026), **stdio transport only**. Data model = git-committed `.md` files with YAML frontmatter (tasks/drafts/docs/decisions). Task fields map cleanly onto MDTM items: `--ac` (acceptance criteria, per-criterion check-off), `--plan`, `--dep` (with circular-dependency guard), `-p` parent/subtask, ordinal ordering; `backlog decision create` exists at the CLI. Concurrency-hardened (task-ID locking).
**Gaps:** **No multi-tenancy, RBAC, auth, or remote/HTTP transport** in the official server — single-user, single-repo, stdio-local by design (the RBAC variant seen in research is a third-party `waabox` fork, UNVERIFIED). No dependency-graph engine. Rich MDTM semantics (gates/convergence/certification) have no native schema and must live as labels/notes/docs conventions or stay in the Python layer.
**UNVERIFIED:** whether the *official* MCP server exposes a `decision.*`/`decision_create` tool (vs. CLI-only) and any milestone tool — must be probed live before depending on `decision.add`.

### 3.3 Beads (dependency-graph issue tracker) — MIT

**Verified:** `github.com/gastownhall/beads`, v1.0.4 (2026-05-09); **MIT**; **Dolt-only** storage as of 1.0 (the classic SQLite+JSONL backend was removed); embedded (single-writer) vs server (multi-writer) modes; agent-native `--json` CLI (`bd ready`, `bd update --claim`, `bd dep cycles`, `bd prime`/`remember`). **Maturity/ops risk is real and verified:** orphaned `dolt sql-server` daemons, embedded-mode nil-pointer panics in `bd ready`/`bd list`, migration-induced `bd dolt pull` failures, and a Rust fork (`beads_rust`) that deliberately freezes the classic architecture — signalling churn. No RBAC/tenancy. First-party MCP maturity UNVERIFIED (`beads-mcp` exists on PyPI; the `--json` CLI is the stable surface).

---

## 4. Component Port Matrix

Dispositions merge A's reuse-discipline on the heuristic mass with C's file-level granularity, corrected by codebase verification. **"reuse-as-is"** = keep as Python behind MCP/HTTP, no rewrite. **"adapt"** = mechanical port or thin wrapper. **"rewrite"** = the genuine new-runtime work. **"drop"** = retire (intent re-homed where it still matters).

| Component | Disposition | Rationale |
|---|---|---|
| **`pipeline/process.py` (`ClaudeProcess`) + `sprint/process.py`** (~630 LOC) — THE SEAM | **rewrite** | Replace with an ACP/stdio driver behind the **same** `build_command/start/wait/terminate` + `on_spawn/on_exit` interface so callers are unchanged. Cheapest path is a thin **Python ACP client** preserving the `StepRunner` contract (no TS, no Mastra needed for the seam). `max_turns`/permission/`CLAUDE_WORK_DIR` parity **UNVERIFIED** — Phase-0 gate. |
| **`sprint/monitor.py`** (~570 LOC stream-json parser) | **rewrite** | **The true risk concentration.** Turn accounting, token sums, stall timing, and error detection are bound to Claude Code's stream-json wire shape. ACP emits normalized `agent_message_chunk` events; a new event adapter must reconstruct the `TurnLedger`/stall/budget signals. |
| **`sprint/executor.py`** (~2150 LOC flagship) | **rewrite** | Phase sequencing, stall watchdog, `TurnLedger`, checkpoint enforcement, crash recovery. Seam is a private `_subprocess_factory` test hook (`:1324`), **not** a clean Protocol — **very-high** difficulty. Keep Python behind MCP during parallel-run; re-express the loop as a Mastra workflow only after the seam is proven. |
| **`roadmap/executor.py`** (~3700 LOC, 8-step pipeline) | **rewrite** | Largest file. Already wraps the runtime behind `claude_process_factory` + `_ClaudeRunner` (`:1271-1279`) → the **easier** of the two flagships to re-target. Keep Python behind MCP for early phases; port control flow to a Mastra workflow later. |
| **`pipeline/executor.py`** (StepRunner-injected sequencer) | **adapt** | Runtime-agnostic via the Protocol. Adaptation = swap the injected factory to the ACP driver; orchestration logic (retry, trailing-gate, cancellation) stays. Low-risk. |
| **`pipeline/models.py`, `sprint/models.py`, `roadmap/models.py`, `tasklist/models.py`** (`TurnLedger`, `GateCriteria`, `TaskEntry`, FSMs) | **reuse-as-is** (port to Zod only if/when a step crosses into TS) | Pure data, zero runtime imports. The contract types the whole port hangs on. |
| **`pipeline/gates.py` + `roadmap/gates.py` (14 gates, 30+ checks) + `tasklist/gates.py` + `validate_gates.py`** (~1.7K LOC) | **reuse-as-is** | Pure-Python validators (frontmatter, heading structure, cross-ref, table schema, routing consistency); no subprocess/LLM. **Highest-value reusable IP** — rewriting to TS is pure value-destruction. |
| **`roadmap/convergence.py`** (`DeviationRegistry` + 3-cycle loop + regression handling) | **reuse-as-is / adapt** | Verified runtime-agnostic (only `TYPE_CHECKING` import). Maps onto `.dountil` + suspend/resume; keep the algorithm in Python behind MCP. |
| **FMEA suite + `roadmap` structural/semantic/fidelity/obligation/cosmetic checkers + `spec_parser`** (~12.7K LOC) | **reuse-as-is** | Pure regex/AST/graph heuristics, zero coupling. Rewriting subtle heuristics to TS is high-risk/low-reward — **the anchor of the hybrid: don't rewrite what doesn't touch the seam.** |
| **`audit/*`** (~6.7K LOC static-analysis suite) | **reuse-as-is** | Highest-LOC reusable block; wrap as an MCP tool server any tool can call uniformly. |
| **`roadmap/prompts.py`, `prd/prompts.py`, certify/validate/remediate prompts** (~3.5K LOC) | **reuse-as-is** | Model-agnostic prompt text; carry verbatim. |
| **`sprint/checkpoints.py`, `config.py`, `kpi.py`, `retrospective.py`, `diagnostics.py`, `logging_.py`** (~1.9K LOC) | **adapt** | Pure Python + file I/O. Checkpoint extraction maps to suspend/resume snapshots; KPI/retro map to OTel spans + Backlog.md docs. |
| **`skills/*/SKILL.md` (24) + `agents/*.md` (39)** | **reuse-as-is** | Runtime-agnostic prompt IP; the crown jewels. `SKILL.md` is cross-agent portable (skills.sh; Mastra has skills.sh integration). Re-target the loader only. |
| **`/sc:*` command dispatch loader** | **drop** (re-home intent) | The `/sc:*` namespace exists only in Claude Code. Command *bodies* survive as skill content; the dispatch surface does not. |
| **`install_hooks/commands/agents/mcp.py` + `freshness-*.sh` + `settings.json` merge** (~1.4K LOC) | **drop** (re-home intent) | Irreducibly Claude-Code-specific (PreToolUse/UserPromptSubmit hook model, `~/.claude/` layout). Freshness/verify-sync re-expressed as Mastra processors/middleware where still needed. |
| **`sprint/tmux.py` + `sprint/tui.py` + `sprint/summarizer.py`** (~1.6K LOC terminal UX) | **drop** | Single-user-local concepts incompatible with the multi-tenant service goal; replaced by Mastra Server endpoints + OTel traces + optional Studio. |
| **`sprint/commands.py`, `roadmap/commands.py`, `tasklist/commands.py`** (Click CLIs) | **rewrite/adapt** | Replaced by Mastra Server HTTP endpoints + optional CLI wrapper. |
| **`eval/*`** (~8.5K LOC harness) | **adapt** | Re-point the PTY/isolation driver at the ACP driver instead of `ClaudeProcess`; keep the isolation model. |
| **`cli_portify/*`** (~6K LOC) | **adapt / drop** | Self-referential porting tool; retire after the port completes. |
| **Backlog.md** (external, MIT) | **adapt** | Sole task-of-record via its built-in MCP server, behind the existing `checkpoint`/`TaskEntry` models through a thin sync adapter. Rich MDTM gate/convergence semantics stay in the Python layer; mirror only task state. |
| **Beads** (external, MIT) | **drop / defer (v1)** | 3-of-4 proposals + research agree. `bd ready` is approximated by the MDTM phase model; Dolt ops instability + dual-source-of-truth drift with Backlog.md outweigh value. **Earn-its-place gate** only if DAG scheduling demonstrably beats the markdown phase graph. (Overrides one proposal's "adapt".) |
| **Mastra runtime (AcpAgent + Server + OTel)** | **adapt** | Adopt the **Apache** core as the ACP driver + HTTP front exposing the Python domain logic over MCP. **EE features (RBAC/SSO/Agent Builder) are a separate paid decision, not part of the reuse swap.** |
| **Existing SuperClaude CLI surfaces** (`sprint run`, `roadmap run`, `pipeline`, `tasklist`, `audit`, `prd`) | **reuse-as-is (benchmark/fallback)** | Keep fully operational as the live benchmark and rollback throughout the parallel run. |

---

## 5. The Runtime Seam

`@mastra/acp`'s `AcpAgent` is the structural twin of `ClaudeProcess`: both spawn a coding-agent CLI as a subprocess, stream its output, persist the session, and select a model at runtime. The swap re-implements `ClaudeProcess` as an **ACP/stdio driver behind the identical lifecycle interface** (`build_command/start/wait/terminate` + `on_spawn/on_signal/on_exit`), so the ~62K LOC of callers are unchanged.

**The hard part is not the seam — it is `monitor.py`.** Claude Code's `stream-json` is a *richer* wire format than ACP's normalized event stream. The current system derives **turn boundaries, per-turn token counts, tool-call inventory, error signatures, and stall timing** from that verbose shape, and those signals are load-bearing for the `TurnLedger` economic model (`initial_budget = max_turns × active_phases`) and recoverable-rerun logic. **Whether ACP events can reconstruct these signals is the single highest-uncertainty technical question, and it gates the entire recommendation.**

**Multi-tool / multi-model implications:** ACP is JSON-RPC 2.0 over stdio with adapters for Claude Code, Codex, Gemini CLI (native `--acp`), Cursor, Copilot, Amp, Goose, Auggie. This is precisely the multi-tool generalization Stack D promises — but ACP is a **lossy, lowest-common-denominator contract** over Claude-Code-specific knobs. Going multi-tool may mean accepting reduced fidelity on permission tiers and turn accounting, and **per-tool parity for Cursor/Gemini/Copilot is UNVERIFIED in Mastra's own docs** (only Claude Code/Amp/Codex are named) — each non-Claude tool needs its own integration spike.

**Sequencing choice (Mastra-late):** Phases 0–2 need **no Mastra at all** — a thin in-process Python ACP/stdio client preserving the `StepRunner` contract delivers multi-tool support with zero vendor surface. Mastra Server + AcpAgent enter only at the multi-user/multi-tenant front (Phase 4+), keeping the EE decision deferrable. *(See §11 for the named Mastra-early-vs-late fork — A's durable-workflow engine is a real benefit forgone by deferring.)*

---

## 6. Task-of-Record Decision

**Decision: Backlog.md is the sole task-of-record for v1. Beads is dropped/deferred.**

- **Backlog.md** (MIT, git-native, built-in spec-aligned MCP server) matches the existing Markdown-harness value with the lowest friction. Map MDTM phase items → backlog tasks: `AC → --ac`, `plan → --plan`, `deps → --dep`, phases → labels/parent tasks, checkpoints/retrospective/KPI → notes/docs, decisions → `backlog decision create`. It sits behind the existing `checkpoint`/`TaskEntry` models via a thin sync adapter; the Python layer retains the rich gate/convergence/certification semantics Backlog.md has no schema for (mirror task *state* only).
- **Beads** is the dependency-graph/ready-work/agent-memory layer Backlog.md lacks — but shipping both creates **dual-source-of-truth drift**, and Beads' **Dolt-only backend has verified ops instability and architectural churn**. 3-of-4 proposals plus the Beads research itself conclude DROP/DEFER for v1. (This overrides the one proposal that assigned Beads "adapt"; its own top-risks list — Dolt instability, dual-source drift — contradicts that choice.)

**Overlap resolution:** one authoritative store (Backlog.md, human-reviewable, diffable, the artifact the company audits); Beads, *if* ever adopted, is a derived/operational scheduling index reconciled via a sync adapter — and only after a benchmark shows `bd ready` + agent-memory beats the MDTM phase model.

**Gate before depending on it:** probe the **official** Backlog.md MCP server live (`backlog mcp start` + `/mcp`) to confirm `decision_create`/milestone tool exposure — the `obligation_scanner → decision.add` dependency in the roadmap pipeline requires it, and it is **UNVERIFIED**. Fall back to CLI invocation if absent.

---

## 7. Multi-Tenancy & Licensing

**This is the strategic crux, and it is commercially gated.** The whole reason for the port — company-wide multi-tenant RBAC — is **Mastra Enterprise Edition (paid)** and lives entirely *outside* the reuse story:

| Layer | OSS (Apache/MIT) capability | What multi-tenancy requires |
|---|---|---|
| Mastra runtime | SimpleAuth (API-key→role) + app-level storage scoping | **EE:** SSO (WorkOS/Okta), `StaticRBACProvider`, permission-based Studio UI, Agent Builder multi-tenant workflows |
| Tenant-fair concurrency | none in core | Inngest engine integration (3rd-party hosting/licensing) or DIY |
| Backlog.md | single-repo, stdio-local, no auth | tenancy = one repo/dir per tenant **behind an external authz gateway** |
| Beads (if used) | one un-permissioned graph per Dolt DB | per-tenant DBs/prefixes managed above Beads |

**Consequence:** a technically successful seam swap (Phases 0–4) can deliver **multi-user (SimpleAuth, $0 license)** and still **not deliver the multi-tenant company goal.** The EE-buy-vs-DIY decision is a **distinct, funded gate** (Phase 5): either license Mastra EE (recurring cost + vendor lock for the exact strategic feature) or build RBAC/tenant-isolation/fair-scheduling on the Apache server yourself (no license, but you build the hardest-to-get-right parts). **Cost/lock-in:** EE is a bespoke commercial agreement; Mastra ships breaking changes quarterly (version-pinning + an abstraction seam over Mastra itself are mandatory). **UNVERIFIED and material:** whether `@mastra/acp` is Apache or EE-gated — if the seam driver itself is EE, the "vendor-free seam swap" premise weakens.

---

## 8. What Is Lost Leaving Claude Code

| Lost capability | Severity | Mitigation |
|---|---|---|
| **Freshness hooks** (`freshness-pre-edit.sh`, session-context injection via UserPromptSubmit) | Dev-ergonomics, not the moat | Re-implement as Mastra processors/middleware where still needed; accept loss for non-Claude tools. |
| **`/sc:*` command dispatch** | Medium | Command *bodies* survive as portable skill content; only the dispatch surface is lost. Re-home via skills.sh. |
| **Permission modes** (`--dangerously-skip-permissions` / `--allow-hierarchical-permissions`) | **High — load-bearing** | ACP must expose equivalent permission semantics; **UNVERIFIED**, gated in Phase 0. If absent, sprint safety/permission model degrades. |
| **`max_turns` accounting + stream-json telemetry** | **High — load-bearing** | The `TurnLedger` budget model depends on it. Reconstruct from ACP events in the rewritten `monitor.py` adapter; **UNVERIFIED**, gated in Phase 0. |
| **`CLAUDE_WORK_DIR` isolation** | High | Map to AcpAgent `workspace` (LocalFilesystem basePath) / sandboxed execution; verify in Phase 0. |
| **`verify-sync` / source-of-truth enforcement** | Dev-ergonomics | Re-express as CI/middleware governance. |
| **tmux/TUI operational UX** | Low (single-user) | Replaced by Mastra Server endpoints + OTel traces + optional Studio — a net-positive for the multi-tenant direction. |

**Framing discipline (from the skeptic's critique):** the genuine competitive moat is the **runtime-agnostic gate/convergence/FMEA/audit IP — which the port preserves**. Hook loss and `/sc:*` loss are dev-ergonomics, not the moat; do not let them inflate the no-go case. The two load-bearing losses (permission semantics, turn/stall telemetry) are exactly what Phase 0 exists to de-risk.

---

## 9. Phased Roadmap

Strangler-fig: prove the seam, run new alongside old under a tolerance gate, defer Mastra and the EE decision to the latest justifiable point. **The existing Python CLI stays fully operational as the live benchmark and rollback throughout.**

### Phase 0 — Dual go/no-go gate: commercial + ACP parity spike
- **Goal:** (a) **Commercial stop/go** — obtain a Mastra EE quote + support terms and **verify the `@mastra/acp` license (Apache vs `ee/`)**. (b) **Parity spike** — drive Claude Code **and one second tool** (Codex or Gemini) through an ACP driver behind the *existing* `ClaudeProcess` interface; verify parity for `max_turns` budgeting, permission-flag semantics, runtime model selection, `CLAUDE_WORK_DIR` isolation, and **whether ACP events can reconstruct the turn/stall/token signals `monitor.py` needs**. Produce a report matching the current stream-json parse. **Both gates must pass before any commitment.**
- **Effort:** **S** (throwaway adapter against one existing interface)
- **Dependencies:** None. Resolves the highest-uncertainty unverified facts.
- **Rollback:** Trivial — throwaway spike; if either gate fails, recommendation flips to **defer/no-port** with <2 weeks sunk.

### Phase 1 — Domain logic behind MCP/HTTP (parallelizable with Phase 0)
- **Goal:** Wrap the ~62K LOC portable Python (gates, convergence, FMEA, audit, `spec_parser`, checkpoints, models) as an MCP tool server + HTTP service. **No logic change** — just expose existing functions. De-risks the "keep Python, don't rewrite" thesis early.
- **Effort:** **L**
- **Dependencies:** None (runs alongside Phase 0).
- **Rollback:** The Python functions remain callable in-process by the existing CLI; the MCP layer is additive.

### Phase 2 — Swap the seam on the sprint flagship + parallel-run gate
- **Goal:** Replace `ClaudeProcess` with the ACP driver for `sprint run`; **rewrite `monitor.py` as an ACP-event adapter** feeding the existing `TurnLedger`/stall-watchdog/checkpoint enforcement. Keep sprint orchestration, models, KPI, retrospective intact behind MCP. **Run the new path in PARALLEL with the Python CLI for 2–3 sprints with an explicit "identical outcomes within 5% tolerance" acceptance gate.**
- **Effort:** **L** (the sprint seam is a private `_subprocess_factory`, not a clean Protocol — highest rewrite concentration; `monitor.py` reconstruction is the real risk)
- **Dependencies:** Phase 0 parity confirmed + Phase 1 domain-over-MCP.
- **Rollback:** Existing CLI is the running benchmark; cutover only on passing the 5% gate. Reversible at any sprint.

### Phase 3 — Backlog.md as task-of-record
- **Goal:** Behind `sprint/checkpoints.py` + `TaskEntry`, add a sync adapter mapping MDTM phase items to Backlog.md tasks via its MCP server. Backlog.md becomes the durable git-native store; Python keeps the rich gate/convergence semantics. **Probe official MCP `decision`/`milestone` tool exposure live before committing `decision.add`.**
- **Effort:** **M**
- **Dependencies:** Phase 2 (one flagship working). Independent of Mastra EE.
- **Rollback:** MDTM `tasklist-index.md` remains the source of truth until the mirror is proven lossless; reject if it becomes a lossy round-trip.

### Phase 4 — Mastra Server multi-user (SimpleAuth, OSS) + second flagship
- **Goal:** Front the runtime with Mastra Server + OTel observability; **SimpleAuth (API-key→role) for multi-USER access on the free Apache tier**. Retire tmux/TUI for HTTP endpoints + run visualization. Port the **roadmap** flagship onto the runtime in parallel — its `claude_process_factory` injection makes it the easier of the two. **Delivers multi-user at $0 license cost.**
- **Effort:** **L**
- **Dependencies:** Phase 2. Mastra introduced here, not earlier (vendor-late).
- **Rollback:** Python CLI still operational; Mastra Server is an additive front, not yet load-bearing for tenancy.

### Phase 5 — Multi-tenant RBAC decision gate (paid build-or-buy)
- **Goal:** The explicit, **funded** strategic decision: **buy Mastra EE** (SSO/`StaticRBACProvider`/Agent Builder + Inngest for tenant-fair concurrency) **OR build RBAC + per-tenant isolation** on the Apache server + per-tenant Backlog.md repos behind an authz gateway. Pilot 2–3 internal tenants with isolation/noisy-neighbor verification. **This is where — and only where — the company-wide driver is met.**
- **Effort:** **XL**
- **Dependencies:** Phase 4 multi-user service running; **EE budget approval OR DIY-RBAC staffing approval**; `@mastra/acp` license clarified (Phase 0).
- **Rollback:** Deliberately last and separate — Phases 0–4 deliver real multi-tool + multi-user value independent of this gate, so "defer the tenancy build" stays a live option if EE pricing or per-tool parity disappoints.

*(Optional Phase 6 — opportunistic TS migration of leaf Python modules — is intentionally unscheduled; see §11, permanent-polyglot vs transitional-hybrid.)*

---

## 10. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **stream-json → ACP event impedance:** ACP cannot reconstruct `max_turns`/turn-boundary/stall/token signals `monitor.py` and `TurnLedger` depend on | Medium | **High** — budget model + recoverable-rerun logic degrade | Phase-0 parity spike is the gate; rewrite `monitor.py` as an ACP-event adapter; keep CLI benchmark for diff. **The single highest-uncertainty technical risk.** |
| **Strategic-driver / scope mismatch:** multi-tenant RBAC is EE-paid and outside the reuse swap | High | **High** — Phases 0–4 succeed yet miss the company goal | Name it explicitly (§7); make EE-buy-vs-DIY a distinct funded Phase-5 gate; deliver multi-user value first so the project is justifiable without it. |
| **`@mastra/acp` license UNVERIFIED** (Apache vs `ee/`) | Medium | Medium-High — undercuts vendor-free premise | Phase-0 commercial gate verifies via source/docs before commitment. |
| **ACP parity for permission flags / `CLAUDE_WORK_DIR`** UNVERIFIED | Medium | High — sprint safety/isolation semantics | Phase-0 spike; if absent, fall back to Claude-only fidelity or defer. |
| **Sprint flagship rewrite harder than framed:** seam is a private `_subprocess_factory`, not a clean Protocol, entangled with monitor/TUI/tmux | High (it is verified) | Medium-High | Size sprint Phase 2 very-high; keep Python behind MCP during parallel-run; 5%-tolerance gate prevents big-bang failure. |
| **Mastra API churn** (1.0→1.16 breaking; quarterly codemods; Node 22.13 floor) | High | Medium | Version-pin + codemod discipline + an abstraction seam over Mastra; Mastra-late sequencing limits exposure window. |
| **Per-tool ACP parity** (Cursor/Gemini/Copilot) UNVERIFIED | Medium | Medium — multi-tool half of the business case | One integration spike per tool; accept lowest-common-denominator contract; Claude+1 proven in Phase 0. |
| **Backlog.md MCP `decision`/`milestone` exposure** UNVERIFIED | Medium | Medium — `obligation_scanner → decision.add` dependency | Live `/mcp` probe in Phase 3; CLI fallback. |
| **Python↔TypeScript boundary tax** (62K LOC behind MCP = permanent two-runtime ops) | High (it is the design) | Medium | Treat the MCP boundary as **permanent architecture**, not a stopgap; budget polyglot ops; resist premature TS rewrite. |
| **Beads / Dolt instability + dual-source drift** | Medium | Medium | **Drop/defer Beads in v1**; Backlog.md is the single store; re-evaluate only on demonstrated `bd ready` value. |
| **Impedance: rich MDTM semantics (gates/convergence/certification) have no Backlog.md schema** | Medium | Medium | Keep them in the Python layer; mirror only task state; reject Backlog.md mapping if lossy. |
| **Multi-tenant pilot fails to beat current CLI + worktrees/subagents** throughput | Low-Medium | High (sunk cost) | Phase-5 pilot with measured side-by-side vs the benchmark before decommissioning anything. |

---

## 11. Open Questions / Decision Gates

These five conflicts are **named gates, not buried assumptions** (per the 0.82 convergence — ship the plan, preserve the conditionality):

1. **Mastra-early vs Mastra-late (genuine architectural fork; needs a Phase-1 decision owner).** Default to **Mastra-late** (vendor-free Python ACP client through Phases 0–2; introduce Mastra at Phase 4) to keep the EE decision deferrable and each phase independently justifiable. **Forgone benefit, documented:** Mastra-early would deliver the durable suspend/resume workflow engine + HTTP service sooner. Decide once `@mastra/acp` licensing (gate 4) is known.
2. **ACP parity for the load-bearing knobs** (`max_turns`, permission flags, `CLAUDE_WORK_DIR`, TurnLedger reconstruction from ACP events) — **UNVERIFIED across all four proposals.** The entire recommendation is conditional on this. **Resolved only by running the Phase-0 spike.**
3. **`@mastra/acp` license** (Apache vs `ee/`) — **UNVERIFIED.** If the seam driver is EE-gated, the vendor-free premise weakens and Mastra-early's cost rises. Phase-0 commercial gate.
4. **Per-tool ACP parity for Cursor/Gemini/Copilot** — **UNVERIFIED** in Mastra's own docs (only Claude Code/Amp/Codex named). The multi-tool half of the business case rests on per-tool spikes none of the proposals have run.
5. **Permanent polyglot vs transitional hybrid:** is Python-behind-MCP the **destination** or a **waystation** to a TS migration? Depends on org staffing and single-language pressure none of the proposals can know. **Flag as an explicit deferred decision** (optional Phase 6), not silently assumed.

**"What would have to be true" to continue past Phase 0** (the skeptic's decision-theoretic frame, adopted verbatim): (a) Mastra EE cost is acceptable *or* DIY-RBAC is staffed; (b) ACP matches `ClaudeProcess` behavior within defined tolerances on the load-bearing knobs; (c) at least Claude + one non-Claude tool execute real sprint/roadmap work; (d) the Python gate/convergence/FMEA/audit IP is reusable without TS rewrite; (e) Backlog.md represents MDTM tasks without lossy drift; (f) the multi-tenant pilot shows better company-wide throughput than the current CLI + worktrees/subagents model.

---

## 12. Recommendation Recap

**HYBRID — conditional go via strangler-fig, gated on a dual Phase-0 spike.** Proceed because the codebase was **verifiably built for runtime substitution** (`StepRunner` Protocol + `claude_process_factory`/`_ClaudeRunner`), making this a **~1.2K-LOC seam swap that unlocks ~62K LOC of differentiated, runtime-agnostic IP**, not a 65K-LOC rewrite. Swap only the seam; keep the Python domain layer behind a (permanent) MCP boundary; run the new path in parallel against the existing CLI under a **5%-tolerance acceptance gate**; adopt Backlog.md (MIT) as the sole task-of-record and **drop Beads for v1**; sequence **Mastra-late** to keep the EE decision deferrable.

The **load-bearing caveat**: the strategic driver — multi-tenant RBAC — is **Mastra-EE-paid and sits outside the reuse swap**, so the technical port can fully succeed and still not meet the company goal without a separate, funded EE-buy-vs-DIY decision at the final phase. The **highest technical risk** is `monitor.py`'s stream-json→ACP reconstruction, not the seam itself. The **entire recommendation is conditional on a Phase-0 spike that has not been run** — if `max_turns`/permission/turn-telemetry parity or the `@mastra/acp` license fails, the recommendation flips to **defer/no-port** with under two weeks sunk. Headline **V 33 / C 30 / L 29 / R 26** reflects a real but non-existential prize, a near-exact seam analog, and concentrated (not diffuse) risk localized to five named, gateable unknowns.
