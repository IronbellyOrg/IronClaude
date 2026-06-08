# Technical Research Report: Mastra + Backlog.md + Beads Port Feasibility

**Date:** 2026-06-03
**Depth:** Deep
**Research files:** 11 codebase (incl. 4 gap-fill) + 4 web research + research-notes inventory
**Scope:** SuperClaude CLI orchestration (pipeline core, roadmap, tasklist, sprint, cli-portify, prd, cleanup-audit, eval, audit, skills/agents/harness)

**Research question:** Can SuperClaude's CLI orchestration pipeline — the Python layer under `src/superclaude/cli/` that drives Claude Code as a worker — be ported or recreated onto **Stack D = Mastra (agent/workflow runtime) + Backlog.md (markdown task-of-record + MCP) + Beads (issue/dependency graph)** to become a **multi-tenant, multi-user, multi-tool company orchestration layer**?

**Authority order:** Codebase is source of truth (Sections 1–4, code-verified). Fresh web research (web-01..04, 2026-06-02, `provider=tavily`) supersedes the older enrichment seed wherever they differ (Section 5). External Stack-D capability/version/license claims are tagged `[UNVERIFIED external]` and are inputs to Options/Risk sections, never promoted to current-state facts.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Current State Analysis](#2-current-state-analysis)
3. [Target State](#3-target-state)
4. [Gap Analysis](#4-gap-analysis)
5. [External Research Findings](#5-external-research-findings)
6. [Options Analysis](#6-options-analysis)
7. [Recommendation](#7-recommendation)
8. [Implementation Plan](#8-implementation-plan)
9. [Open Questions](#9-open-questions) (incl. 9.C Risk Register)
10. [Evidence Trail](#10-evidence-trail)

---

## 1. Problem Statement

### 1.1 The Question

Can SuperClaude's CLI orchestration pipeline — the Python layer under `src/superclaude/cli/`
that drives Claude Code as a worker (`sprint run`, `roadmap run`/`validate`, `tasklist validate`,
`cli-portify`, `prd`, `cleanup-audit`, `eval`, `audit`, plus the reusable skills/agents/harness) —
be **ported or recreated** onto **Stack D = Mastra (agent/workflow runtime) + Backlog.md
(markdown task-of-record + MCP) + Beads (issue/dependency graph)** to become a **multi-tenant,
multi-user, multi-tool company orchestration layer**?

The seed brief frames this explicitly as a feasibility study plus high-level roadmap — *not* an
implementation, and *not* assumed to be worthwhile in advance (seed-brief.md:37-38, 44-50). "Do
not port" must remain a live outcome (seed-brief.md:38).

### 1.2 Why It Matters (the Trigger)

The strategic driver is an upgrade to a **multi-tenant company orchestration layer**, with
capabilities the current system structurally lacks:

| Driver | Why the current system cannot satisfy it (evidence) |
|---|---|
| Multi-tenant / multi-user / RBAC | The scoped current models read carry model/permission/budget/runtime fields but **no tenant/actor/audit identity fields** (research 11, Evidence Table; `PipelineConfig` `models.py:212-235`, `SprintConfig` `sprint/models.py:347-510`). Multi-tenancy is therefore a *new* target-design requirement, not an existing capability (research 11, RG-M3). |
| Drive multiple agent CLIs/models (Claude Code, Cursor, Codex, Gemini, Copilot) | The single execution substrate is a subprocess driver hard-bound to the `claude` binary: `ClaudeProcess.build_command()` composes `claude --print --verbose ...` (`pipeline/process.py:73-95`; research 01, 06). The current driver cannot drive non-Claude models (seed-brief.md:33, 41). |
| Company-wide, durable, inspectable work-of-record | State today is file-based: `.roadmap-state.json`, `deviation-registry.json`, JSONL/Markdown logs, result/checkpoint files, and JSON remediation logs (research 02, 03). There is no shared issue/dependency database. |

The seed brief also notes the local model aliases are now **heterogeneous** (opus=`claude-opus-4-8`,
sonnet=`gpt-5.5`, haiku=`qwen3.6-plus`), which is relevant precisely because a multi-tool layer
must drive non-Claude models that the current `claude`-CLI driver cannot (seed-brief.md:33).

### 1.3 The Core Technical Framing

The investigations converge on one framing: the SuperClaude orchestration layer is a
**Python-controlled, Claude-Code-subprocess, Markdown-artifact orchestration system**, and the
single coupling seam between portable orchestration and Claude-specific runtime is the
`ClaudeProcess` subprocess boundary (research 01 Summary; research 06 Summary; seed-brief.md:28).
A Stack D effort is therefore a **replatforming**, not a like-for-like rewrite: it must preserve
the portable harness IP (skills/agents/commands/gates/MDTM format) where possible while replacing
the runtime seam and adding multi-tenancy (seed-brief.md:24, 29-31, 39).

### 1.4 What a Defensible Answer Must Contain

Per the seed brief's success criteria (seed-brief.md:44-51), the report must deliver: a
go/no-go/hybrid recommendation with risk register; a component-by-component port matrix
(reuse-as-is / adapt / rewrite / drop); a phased strangler-fig roadmap; explicit treatment of the
runtime seam and the Backlog.md-vs-Beads task-of-record decision; and a risk register covering
Mastra EE license drift, Backlog/Beads overlap, loss of Claude-Code-native features, and
multi-tenant security.

> **Scope note for Section 1.** All Stack D capability/version/license/schema statements
> (Mastra, Backlog.md, Beads) are external claims tagged `[UNVERIFIED external]` and were not
> code-verifiable from this repository (research 11 Guardrail 1; research 06 Gaps #1; research 05
> Section 6). They are inputs to the Options/Risk sections, not to the current-state baseline below.

---

## 2. Current State Analysis

This section describes how SuperClaude orchestration works **now**. Per the synthesis guardrails
(research 11), only `[CODE-VERIFIED]` findings appear as current-state facts; every claim cites a
file path and line range carried from the research files. Source-of-truth for all citations is
`src/superclaude/` (research 11 Guardrail 2; `core/CLAUDE.md:17-29`, `:45-48`).

### 2.0 System-Level Architecture

The orchestration layer is a set of Click CLI command groups registered on a single root group,
each driving Claude Code through a shared subprocess seam, with deterministic Python owning
sequencing/gates/state and Claude subprocesses filling structured artifacts.

```
                       superclaude (root Click group)  [main.py:18-26, 400-426]
                                       |
   +---------+-----------+-------------+-------------+-----------+---------+
   |         |           |             |             |           |         |
 sprint   roadmap   cleanup-audit   tasklist     cli-portify    prd      eval
   |         |           |             |             |           |         |
   |    execute_pipeline (shared) <----+-------------+           |    own orchestrator
   |    [pipeline/executor.py:63-188]                            |    [eval/orchestrator.py]
   |         |                                                   |
 own phase   +--- run_step (consumer-specific) ---> ClaudeProcess (THE SEAM)
 loop                                                [pipeline/process.py:24-244]
 (executor.py:1135-1757)                              builds: claude --print --verbose
                                                      --no-session-persistence --tools default
                                                      --max-turns N --output-format <fmt>
                                                      [process.py:73-95]
```

Verified system facts:

| Fact | Evidence |
|---|---|
| Root Click group `main`; registers `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, `eval`. | `main.py:18-26`, `main.py:400-426` (research 06, 08) |
| There is **no** root `superclaude pipeline` command; `pipeline/` is a shared library package. | `pipeline/__init__.py:1-21`; root registration `main.py:400-426` (research 06 Gap #2; research 08) — corrects seed-brief.md:19 wording. |
| `ClaudeProcess` is the single Claude-Code runtime seam reused by sprint, roadmap, tasklist, cli-portify, cleanup-audit. | `pipeline/process.py:73-95`, `:114-157` (research 01, 06 Summary) |
| Output format is per-consumer: sprint=`stream-json`, roadmap/tasklist=`text`. | `sprint/process.py:108-121`; `tasklist/executor.py:130-140`; `roadmap/executor.py:1107-1118` (research 06) |

### 2.1 Shared Pipeline Core (`src/superclaude/cli/pipeline/`)

The shared core is **already framework-neutral**: `models.py` has zero imports from sprint or
roadmap and is stdlib-only (`models.py:1-5`, `:8-15`); the executor declares NFR-007 (no
sprint/roadmap imports) (`executor.py:7`); gates are pure Python with no subprocess/LLM calls
(`gates.py:1-9`). This is identified as the strongest migration seam (research 01 Summary).

#### Core data contracts (`pipeline/models.py`)

| Contract | Purpose | Evidence |
|---|---|---|
| `Step` | Core unit: id, prompt, output_file, gate, timeout, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path. | `models.py:108-123` |
| `StepResult` | step ptr, status, attempt, gate failure reason, start/finish ts, remediation metadata, computed duration. | `models.py:125-148` |
| `GateCriteria` | required frontmatter fields (OR-group tuples), `min_lines`, `enforcement_tier` (STRICT/STANDARD/LIGHT/EXEMPT), semantic checks. | `models.py:90-105` |
| `StepStatus` enum | PENDING, PASS, FAIL, TIMEOUT, CANCELLED, SKIPPED; `is_failure` true only for FAIL+TIMEOUT (not CANCELLED/SKIPPED). | `models.py:40-67` |
| `GateMode` enum | BLOCKING, TRAILING (trailing non-blocking until grace-period eval). | `models.py:69-79` |
| `SemanticCheck` | pure-Python content check (`name`, `check_fn`, `failure_message`). | `models.py:81-87` |
| `Deliverable`/`DeliverableKind` | portable deliverable classification + JSON round-trip; missing `kind` defaults to `implement`. | `models.py:151-209` |
| `PipelineConfig` | work_dir, dry_run, max_turns, model, permission_flag (default `--dangerously-skip-permissions`), debug, grace_period, cosmetic-remediation fields. | `models.py:212-235` |

#### Generic executor (`pipeline/executor.py`)

| Behavior | Evidence |
|---|---|
| `execute_pipeline(steps, config, run_step, ...)` sequences `Step \| list[Step]` entries; nested lists = parallel groups. | `executor.py:63-78` |
| `StepRunner` protocol is injected — it owns subprocess execution + timeout; executor owns retry/gates/ordering. **This is the process-boundary seam.** | `executor.py:41-60` |
| `_gate_target()` prefers a sibling `.compressed.md` sidecar when present — gates validate what downstream LLM steps consume. | `executor.py:23-35` |
| Parallel groups run in daemon threads; any non-PASS sets a shared cancellation event for siblings; group halts if any result is not PASS. | `executor.py:402-452`, `:108-123`, `:416-423` |
| `grace_period == 0` forces `GateMode.BLOCKING` even when a step declares TRAILING. | `executor.py:211-215` |
| Trailing gate failures at pipeline end are **logged as warnings, not converted to failed StepResults** (advisory/shadow in current code). | `executor.py:175-187` (research 01 Section 6) |

#### Gate validation (`pipeline/gates.py`) — deterministic, portable

| Tier | Behavior | Evidence |
|---|---|---|
| EXEMPT | always passes | `gates.py:28-30` |
| LIGHT | file exists + non-empty | `gates.py:32-43` |
| STANDARD | + min_lines + required frontmatter | `gates.py:45-63` |
| STRICT | + semantic checks, short-circuit on first non-`True` | `gates.py:65-76` |

Frontmatter parsing is regex-based and **permissive**: it scans delimiter pairs anywhere (tolerates
preamble), checks only top-level keys, and supports OR-group aliases (`gates.py:79-142`). A stricter
YAML parser in another stack could change pass/fail behavior (research 01 Section 6 risk).

#### Trailing gates / remediation (`pipeline/trailing_gate.py`)

Provides async gate evaluation (`TrailingGateRunner`, `trailing_gate.py:93-228`), typed
`TrailingGateResult` (`step_id, passed, evaluation_ms, failure_reason`; `:34-47`), a persistent
`DeferredRemediationLog` (`:508-596`), deterministic `build_remediation_prompt()` (`:282-346`), and a
retry-once `attempt_remediation()` state machine with turn budgeting (`:373-468`). Same
`.compressed.md` sidecar preference as the executor (`:146-156`).

#### Other core modules

| Module | Current behavior | Evidence |
|---|---|---|
| `deliverables.py` | Heuristic `is_behavioral()` + `decompose_deliverables()` expand behavioral deliverables into `.a` implement / `.b` verify pairs; idempotent. | `deliverables.py:100-194` |
| `diagnostic_chain.py` | Four-stage report (troubleshoot/root-causes/solutions/summary) that is **deterministic static Markdown assembly, not LLM/adversarial calls** despite naming. | `diagnostic_chain.py:71-158` (research 01 Section 6; research 11 01-G6) |
| `process.py` (`ClaudeProcess`) | Builds the `claude` command; delivers prompt via **stdin** (avoids `MAX_ARG_STRLEN`); strips `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT`; process-group-aware terminate (SIGTERM→10s→SIGKILL); timeout returns code `124`. | `process.py:73-95`, `:114-157`, `:173-214`, `:163-165` |

**Core-layer port note (from research):** the cleanest seam is to replace only
`StepRunner`/`ClaudeProcess` first while preserving executor + gate semantics; `Step`,
`GateCriteria`, `StepResult`, `PipelineConfig` translate to Mastra schemas / Beads metadata with
minimal dependency drag (research 01 Section 4/8). The main hazard is accidentally baking Claude-CLI
permission flags into the portable orchestration model (`models.py:226-235`; research 01).

---

### 2.2 Roadmap and Tasklist Pipelines (`cli/roadmap/`, `cli/tasklist/`)

Both consumers reuse the shared `execute_pipeline()` plus an injected `run_step`; roadmap is the
largest and richest subsystem, tasklist is validation-only (research 02).

#### Roadmap run — hybrid deterministic/LLM DAG

`execute_roadmap()` (`roadmap/executor.py:2985-3187`) routes inputs, compresses inputs, builds
steps, applies resume, installs a roadmap-owned cosmetic remediator, then delegates to
`execute_pipeline(steps, config, roadmap_run_step, ...)` (`:3124-3131`). Most steps launch
`ClaudeProcess` (`output_format="text"`), but several step IDs run **deterministic Python** rather
than LLM calls (`roadmap/executor.py:955-1250`, `:977-1031`).

Wired step order in `_build_steps()` (`roadmap/executor.py:1947-2208`):

```
extract -> [generate-A | generate-B] -> diff -> debate -> score -> merge
  -> anti-instinct -> test-strategy -> spec-fidelity -> wiring-verification
  -> deviation-analysis -> remediate
  (parallel group)         (deterministic Python steps interleaved)
```

| Step | Gate | Nature | Evidence |
|---|---|---|---|
| extract | EXTRACT_GATE / EXTRACT_TDD_GATE | LLM | `executor.py:2003-2027` |
| generate-A / generate-B | GENERATE_A_GATE (=B) | LLM, parallel | `executor.py:2029-2066` |
| diff / debate / score / merge | DIFF/DEBATE/SCORE/MERGE gates | LLM (inline adversarial) | `executor.py:2068-2128` |
| anti-instinct | ANTI_INSTINCT_GATE | deterministic `_run_anti_instinct_audit` | `executor.py:2130-2138`, `:977-992` |
| test-strategy | TEST_STRATEGY_GATE | LLM | `executor.py:2140-2156` |
| spec-fidelity | SPEC_FIDELITY_GATE or None | split: convergence mode → deterministic pass/fail; `--no-convergence` → gate | `executor.py:2158-2173`, `:994-1001` |
| wiring-verification | WIRING_GATE (`gate_mode=TRAILING`) | deterministic `run_wiring_analysis` | `executor.py:2175-2184`, `:1011-1031` |
| deviation-analysis | DEVIATION_ANALYSIS_GATE | deterministic `_run_deviation_analysis` | `executor.py:2186-2194`, `:1003-1005` |
| remediate | REMEDIATE_GATE | deterministic `_run_remediate_step` | `executor.py:2196-2204`, `:1007-1009` |

Key current-state subtleties (all `[CODE-VERIFIED]`):

- **Adversarial is inline, not delegated.** The CLI wires `diff → debate → score → merge`
  directly; it does **not** call `sc:adversarial-protocol` (research 02; research 06 row E).
- **Convergence engine is stateful and file-backed.** `_run_convergence_spec_fidelity`
  (`executor.py:1290-1478`) uses a `DeviationRegistry` (`convergence.py:90-207`), a `TurnLedger`
  budget, up to three checker/remediation cycles (`convergence.py:434-557`), structural-regression
  handling, and pass when active HIGH count reaches zero. Porting requires more than an LLM compare
  step (research 02).
- **Remediation artifacts.** `remediation-tasklist.md` + JSON sidecar from
  `_run_remediate_step` (`executor.py:1804-1897`); parallel per-file remediation with snapshots /
  rollback / diff-size guard in `execute_remediation` (`remediate_executor.py:735-755`).
- **Cosmetic remediation lane.** Roadmap injects a remediator into shared `PipelineConfig`
  (`executor.py:3092-3122`); the generic executor invokes it after gate failure
  (`pipeline/executor.py:286-365`).
- **Validation subsystem.** Auto-invoked after a successful run (`executor.py:3409-3447`);
  single-agent `reflect` (REFLECT_GATE) or multi-agent parallel `reflect-{agent}` +
  `adversarial-merge` (ADVERSARIAL_MERGE_GATE) (`validate_executor.py:239-339`, `:442-519`).
- **State files:** `.roadmap-state.json`, `deviation-registry.json`, `spec-deviations.*`,
  `remediation-tasklist.*` (research 02).

#### Tasklist — validation-only (generation lives in the skill)

| Fact | Evidence |
|---|---|
| CLI exposes only `tasklist validate`; **no `tasklist generate` subcommand**. | `tasklist/commands.py:31-82`; `prompts.py:156-162` (research 02, 06) |
| Single `tasklist-fidelity` step (TASKLIST_FIDELITY_GATE, STRICT, 20-line min) over `[roadmap.md] + tasklist files + optional TDD/PRD`. | `tasklist/executor.py:191-218`; `tasklist/gates.py:23-46` |
| CLI pass/fail = `high_severity_count == 0` parsed from the generated report. | `tasklist/executor.py:221-276` |
| `.roadmap-state.json` auto-wires TDD/PRD paths. | `tasklist/commands.py:113-160` |
| Tasklist **generation** is a skill/protocol behavior (`sc-tasklist-protocol`), not Python CLI; it emits `tasklist-index.md` + literal `phase-N-tasklist.md`, sprint-compatible. | `sc-tasklist-protocol/SKILL.md:31-44`, `:91-123`, `:1062-1117` (research 02) |

> **Current-state caveats carried as risks (not facts):** `CERTIFY_GATE`/`build_certify_step` are
> **defined but not wired** into production `_build_steps` (`gates.py:1324-1351`, `executor.py:1899-1944`
> vs `:1947-2208`; research 02 Gap #1, research 11 02-G1). `wiring-verification` declares TRAILING but
> default `grace_period=0` forces blocking (research 02 Gap #2, research 11 02-G2). The deviation
> classifier renders all records `UNCLASSIFIED` (research 02 Gap #4, research 11 02-G4). Per guardrail
> 8, these are not normalized away.

---

### 2.3 Sprint Execution Runtime (`cli/sprint/`)

Sprint is the heaviest and hardest-to-port surface: 19 Python files, ~8,568 lines, concentrated in
`executor.py` (2,148), `models.py` (883), `tui.py` (629), `monitor.py` (571), `config.py` (509),
`commands.py` (463), `checkpoints.py` (408), `process.py` (385), `tmux.py` (323) (research 03 Source
Inventory). Unlike roadmap/tasklist, sprint does **not** use the generic `execute_pipeline()` for its
main loop; it runs a custom phase loop (`executor.py:1135-1757`) and only shares pipeline
models/remediation contracts (research 01 Gap #5; research 11 01-G5).

#### Two execution paths

```
execute_sprint(config)  [executor.py:1135-1757]
  |
  |-- preflight `claude` binary, signal handlers, TUI, monitor, TurnLedger,
  |   ShadowGateMetrics, DeferredRemediationLog, SprintGatePolicy, SummaryWorker
  |
  +-- per phase:
        python-mode  -> handled in preflight  [executor.py:1228-1234]
        skip-mode    -> PhaseResult(SKIPPED)   [executor.py:1245-1257]
        |
        +-- PATH A (parsed tasks present):  _parse_phase_tasks -> execute_phase_tasks
        |     one ClaudeProcess subprocess per TaskEntry, post-task gates/hooks,
        |     `continue` BEFORE phase-level monitor block   [executor.py:1259-1301]
        |
        +-- PATH B (freeform phase file):  isolation dir + OutputMonitor + ClaudeProcess
              poll process, stall watchdogs, checkpoint verify   [executor.py:1303-1457]
```

| Subsystem | Current behavior | Evidence |
|---|---|---|
| Phase discovery | filename patterns `phase-N-tasklist.md`, `pN-tasklist.md`, `phase_N_tasklist.md`, `tasklist-pN.md`; index table parse + dir fallback; `Execution Mode` ∈ {claude, python, skip}. | `config.py:15-26`, `:52-140` |
| Task parsing | `### T<PP>.<TT>` headings → `TaskEntry` (id, title, description, dependencies, command, classifier). | `config.py:399-492`, `models.py:24-37` |
| Dependency scheduling | dependencies are **parsed but not used for ordering**; tasks execute in file order. | `config.py:379-384`, `executor.py:971-1010` (research 06 row C) |
| Process seam | sprint `ClaudeProcess` subclasses base, `output_format="stream-json"`, prompt = `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic`. | `sprint/process.py:88-121`, `:123-216` (corrects stale `/sc:task-unified`) |
| Path A subprocess | minimal prompt (task id/title/phase file/description); per-task output/error files; **returns `turns_consumed=0`** (TurnLedger inaccurate for Path A). | `executor.py:1086-1115`, `:1098-1108`, `models.py:502-506` |
| Monitoring | `OutputMonitor` parses incremental stream-json/NDJSON in a daemon thread; tracks bytes, events, stall seconds, tokens, files-changed. | `monitor.py:253-396`, `models.py:623-666` |
| Stall watchdogs | startup-stall (`events==0` & `stall>startup_timeout`) and mid-stall fire from CLI thresholds; `kill` → exit 124, `warn` → continue. | `executor.py:1366-1445` |
| Result classification | `_determine_phase_status` blends exit code + result-file freshness + prompt-too-long + checkpoint inference + checkpoint gate mode → PASS/HALT/TIMEOUT/PASS_RECOVERED/PASS_NO_REPORT/INCOMPLETE/ERROR. | `executor.py:2067-2148`, `:1774-1808` |
| Checkpoints | `extract_checkpoint_paths` parses `Checkpoint Report Path:` declarations; `_verify_checkpoints` respects mode off/shadow(default)/soft/full; manifest written to `<release_dir>/manifest.json`; recovery can synthesize `UNKNOWN` reports. | `checkpoints.py:36-94`, `executor.py:1811-1891`, `:1702-1725`, `checkpoints.py:209-408` |
| Diagnostics | on failure: `DiagnosticCollector` + `FailureClassifier` + `ReportGenerator` → markdown report, sprint `HALTED`. | `executor.py:1609-1639`, `diagnostics.py:72-232` |
| Retrospective | `RetrospectiveGenerator(config).generate(...)` runs at sprint wrap-up; **failures are non-aborting**. | `executor.py:1661-1688`, `retrospective.py` (research 11 Evidence Table — `[CODE-VERIFIED]`) |
| tmux/TUI | deterministic `sc-sprint-<sha1>` session, 3-pane layout, exit-code sentinel propagation; Rich `Live` TUI. | `tmux.py:81-173`, `:213-252`, `tui.py:98-197` |

#### Checkpoint contract (RG-C2, from gap-fill 09)

The **canonical** `/sc:tasklist` generation contract is **numbered checkpoint task entries**
(`### T<PP>.<NN> -- Checkpoint: ...` with a `Checkpoint Report Path:` line), per
`SKILL.md:343-391`, `:947-1027`, `:1062-1117` `[CODE-VERIFIED]`. The runtime parser
(`checkpoints.py:18-33`) accepts **both** the numbered form and legacy sibling `### Checkpoint:`
headings, and `config.py` parses numbered checkpoint tasks as ordinary `TaskEntry` objects
(`config.py:420-492`). The contradiction is real but confined to stale prompt/template/doc surfaces
(`phase-template.md:101-125`, `process.py:187-195`), **not** the runtime parser (research 09
Findings 1-2). The adapter-safe contract: emit numbered checkpoint tasks with `Checkpoint Report
Path:` lines using `TASKLIST_ROOT/checkpoints/...` paths (research 09 Canonical Contract).

> **Current-state caveats carried as risks (not facts):** the documented "4-layer isolation"
> (`setup_isolation`) is **not called** in the main loop — Path B sets only `CLAUDE_WORK_DIR`, Path A
> sets no isolation env (`executor.py:106-182`, `:1303-1324`, `:1098-1108`; research 03; research 11).
> `status`/`logs` CLI commands are **stubs** (`logging_.py:224-235`). Path A does **not** submit
> SummaryWorker summaries before continuing, while Path B does (`executor.py:1259-1301` vs `:1578-1592`).
> Per-task `_verify_checkpoints()` is **not** called in the Path A branch (research 09 Finding 3).
> A sprint **`rerun-tasks`** CLI verb is **not present** in current source (`commands.py` has run,
> attach, status, logs, kill, verify-checkpoints) — excluded from current-state per research 11
> guardrail 4. Sprint is the recommended last/hardest migration surface, not the first (research 03
> Section 8; research 11 RG-I7).

---

### 2.4 Adjacent Orchestration Tools (`cli_portify/`, `prd/`, `cleanup_audit/`, `eval/`, `audit/`)

Five additional CLI-adjacent orchestration systems, each contributing a distinct reusable pattern
(research 04). File counts: `cli_portify/` 87, `prd/` 44, `cleanup_audit/` 37, `eval/` 65,
`audit/` 127 (research 04 Inventory).

| Tool | Pattern / shape | Key current-state facts | Evidence |
|---|---|---|---|
| `cli_portify` | Deterministic graph-first migration pipeline. | `STEP_REGISTRY` (12 ordered steps with phase types, timeouts, retries); two-layer `PortifyGatePolicy` (SHADOW/SOFT/FULL, blocking only in FULL); `return-contract.yaml` on all outcomes; standalone `ConvergenceEngine`. | `executor.py:105-183`, `:380-440`, `:283-372`, `convergence.py:144-255` |
| `prd` | Dynamic multi-agent fan-out + QA/fix convergence. | Sequential Stage A (9 steps) → dynamic Stage B; tier-sized investigation (3/5/8) and web (1/2/3) agents; `ThreadPoolExecutor` (max 10) with per-future ERROR capture; QA→fix→re-QA loop with budget halt; 15-step `GATE_CRITERIA`. | `executor.py:372-388`, `:721-860`, `:862-905`, `:923-958`, `:963-1047`, `gates.py:303-514` |
| `cleanup_audit` | Read-only audit, monitored subprocesses, blocking gates. | Six sequential steps `G-001`..`G-006`; sprint-style supervised loop (preflight, poll, stall watchdog, gate, diagnostics); strict gates → HALT. | `executor.py:52-184`, `:187-287`, `gates.py:59-154` |
| `eval` | Safe parallel execution + isolation + forensic accounting. | Capability/version preflight (`claude --version`); scratch-root allowlist; per-eval HOME isolation w/ containment guard; `RunOrchestrator` `ThreadPoolExecutor` (1-15) preserving order; never drops an outcome; policy-tag `RetryOncePolicy` (MCP-flaky); JSONL forensic logs; disk-budget skips. | `commands.py:119-192`, `:1713-1830`, `orchestrator.py:164-299`, `runner.py:833-1005`, `isolation.py:456-642`, `retry.py:92-165` |
| `audit` | Shared scoring primitive library (not one end-to-end command). | content-hash `ResultCache`; deterministic `(tier, action)→category` classification; consolidation by file path w/ highest-confidence conflict resolution; stratified-sample consistency validation (self-agreement, **not** accuracy); atomic checkpoint; batch retry (max 2); ordered budget degradation. | `tool_orchestrator.py:146-224`, `classification.py:108-166`, `consolidation.py:93-180`, `validation.py:89-151`, `validation_output.py:14-27`, `checkpoint.py:58-110`, `batch_retry.py:60-187`, `budget.py:159-320` |

Cross-tool shared patterns (the verified "migration methodology" inputs, research 04 Section 4):
single authoritative step graph; explicit per-node artifact/gate contracts; preflight before side
effects; observable supervision (monitor/deadline/stall/signal); gate after every artifact step with
persisted diagnostics; QA/fix or convergence loops instead of assuming first-pass success.

> **Current-state caveats carried as risks (not facts):** `cli_portify` `resume.py:45-95` /
> `review.py:32-38` use **legacy step names** that drift from the live `STEP_REGISTRY`
> (`[CODE-CONTRADICTED]`, research 04 Gaps). `cleanup_audit` accepts `--pass`/`--batch-size` but
> `_build_steps` shows no pass filtering/batching, and the docstring claims `ThreadPoolExecutor`
> parallelism while the code runs **sequentially** (`[CODE-CONTRADICTED]`, research 04). No source
> file implements Mastra/Backlog/Beads integration today (`[UNVERIFIED]`, research 04 Gaps; research
> 11 04). `/sc:forensic` referenced by TFEP has **no** matching command/skill in `src/superclaude`
> (`[CODE-CONTRADICTED]`, research 11 Evidence Table) — excluded per guardrail 4.

---

### 2.5 Skills, Agents, and Harness (`skills/`, `agents/`, `commands/`, `core/`, `templates/`, `hooks/`, `mcp/`)

This is the portable "intelligence" layer: Markdown/YAML knowledge artifacts plus event-driven
policy, distinct from the Python orchestration runtime (research 05). All citations resolve to
`src/superclaude/` as source-of-truth (`core/CLAUDE.md:17-29`, `:45-48`, `[CODE-VERIFIED]`).

#### Scoped inventory (counts are scoped/sampled, not exhaustive semantic parity — research 11 RG-M2)

| Asset group | Count / size | Evidence |
|---|---|---|
| Command markdown front doors | 42 files under `commands/` | research 05 Section 8 |
| Agent definitions | 39 files under `agents/` | research 05 Section 8 |
| Skill packages (`SKILL.md` + refs/rules/templates/scripts) | 24 packages, ~31,820 lines incl. refs | research 05 Section 8 |
| Core instruction files | 12 files under `core/` | research 05 Section 8 |
| Workflow templates (incl. MDTM 01/02) | 8 files under `templates/workflow/` | research 05 Section 8 |
| Document templates | 7 files, 3,308 lines under `templates/documents/` | research 05 Section 8 |
| Hook assets | `hooks.json` + 9 scripts + README/example | research 05 Section 8 |
| MCP assets | 11 docs + 11 JSON configs | research 05 Section 8 |

#### Layer roles and runtime coupling

| Layer | Current role | Claude-Code coupling | Evidence |
|---|---|---|---|
| Commands (`commands/*.md`) | Thin front doors: parse flags, validate inputs, then mandatorily invoke a backing skill (e.g. `task.md:156-162`, `tasklist.md:70-84`, `roadmap.md:82-92`). | `Skill` invocation, `/sc:*` dispatch. | research 05 Section 2 |
| Skills (`skills/*/SKILL.md`) | Main reusable instruction body / protocol policy. | references Claude Code `Skill`/`Task`. | research 05 Section 3 |
| Agents (`agents/*.md`) | Role prompts; Rigorflow team = team-lead, researcher, builder, qa, qa-qualitative with `RESEARCH_READY`/`TASK_READY`/`BLOCKED` message vocabulary. | `Task`/`TeamCreate`/`SendMessage`. | `rf-team-lead.md:36-103`, `rf-task-researcher.md:30-57`, research 05 Section 3 |
| MDTM templates (`templates/workflow/01/02`) | Task frontmatter + granular-breakdown / self-contained-item rules. | none observed beyond skill access. | `01_..._generic_task.md:1-44`, `:87-159` |
| Core (`core/*.md`) | Policy corpus: CLAUDE.md, COMMANDS, ORCHESTRATOR (scoring matrices), MCP (server selection/circuit breakers), RULES (conflict hierarchy, verification-before-recommendation). | references Claude Code commands/tools. | `core/CLAUDE.md`, `ORCHESTRATOR.md:5-130`, `MCP.md:5-15`, `:269-304`, `RULES.md:5-82` |
| Hooks (`hooks/`) | Event policy: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SubagentStart`, `SubagentStop`; freshness-user-prompt context injection; freshness-pre-edit guard; reject-workspace-writes. | **Claude Code-specific hook events + shell scripts.** | `hooks.json:1-95`, `freshness-pre-edit.sh:63-138`, `reject-workspace-writes.sh:25-62` |
| MCP (`mcp/configs/*.json`) | Server launch configs (Tavily, Auggie, Serena, Sequential, ...); secret/env injection; circuit-breaker/fallback policy. | MCP server lifecycle. | `mcp/configs/tavily.json:1-12`, `core/MCP.md:269-304` |

#### Reuse boundary (the in-repo portification precedent)

The strongest internal precedent for the port itself is `sc-cli-portify-protocol` — it already
decomposes inference workflows into component inventory → step graph → gates →
executor/workflow model → reviewed spec (`SKILL.md:12-28`; `refs/pipeline-spec.md:15-128`; research
05 Section 6). Its evolution also carries a cautionary lesson: early code-generation/spec drift
caused failures; the successful direction was contract-first, gated, resumable, source-verified
(research 06 row B Summary).

> **Current-state caveats carried as risks (not facts):** **Source-of-truth conflict** —
> `core/CLAUDE.md:45-48` says edit `src/superclaude/` first, but `commands/README.md:13-23`,
> `agents/README.md:11-21`, `hooks/README.md:9-19` say plugin mirrors are edit-first; `diff -qr`
> showed mirrors materially differ (`[CODE-CONTRADICTED]`, research 11 RG-I4). For this branch
> `src/superclaude/` is canonical; a port must add a source-of-truth resolver + sync gate before
> ingesting any corpus (guardrail 2). **Hook portability** — hook contracts/behavior are reusable but
> the shell implementation is Claude-Code-specific and must be rebuilt as middleware/guards
> (`[CODE-VERIFIED behavior; UNVERIFIED portability]`, guardrail 3). Some agent refs point at
> `.claude/templates/...` dev copies; a canonical `src/superclaude/templates/...` resolver is required
> (research 05 Gaps #5). All Mastra/Backlog.md/Beads fit claims remain `[UNVERIFIED external]`
> (research 05 Section 6; guardrail 1).

---

### 2.6 Current-State Summary

| Subsystem | Orchestration ownership | Runtime seam | Portability posture (from research) |
|---|---|---|---|
| Shared pipeline core | Python (framework-neutral) | injected `StepRunner` / `ClaudeProcess` | Strongest seam; translate contracts + gates directly. |
| Roadmap/tasklist | shared `execute_pipeline` + hybrid deterministic/LLM steps | `ClaudeProcess` (text) | Feasible as workflow DAG + gate/state machine; tasklist generation must be rebuilt from skill protocol. |
| Sprint | custom phase loop (not generic executor) | sprint `ClaudeProcess` (stream-json) + tmux/monitor | Hardest; recommended last; preserve file-based result/checkpoint/sentinel contracts. |
| Adjacent tools | per-tool graphs / orchestrators | `ClaudeProcess` (cli_portify/cleanup) or own runner (eval) | Reusable methodology: graph-first, gated, preflighted, isolated, QA/fix loops. |
| Skills/agents/harness | Markdown/YAML + hook policy | Claude Code `Skill`/`Task`/hooks/MCP | Instruction reuse high; runtime control (loops, deps, hooks, tools) must move into deterministic workflow code. |

**Bottom line for the current state:** SuperClaude orchestration today is a Python-controlled,
Claude-Code-subprocess, Markdown-artifact system. Deterministic Python owns sequencing, retry/halt,
state emission, gates, and file outputs; Claude subprocesses fill structured content; the single
runtime coupling point is `ClaudeProcess`. Multi-tenancy, multi-model drive, and a shared
issue/dependency database are **absent** from the scoped current models — they are new target-design
requirements, not existing capabilities (research 11 RG-M3; research 06 Summary).

---

## 3. Target State

Target-stack capability cells cite web research URLs (provenance `tavily` unless noted), surfaced
by `web-01`–`web-04`. Doc-only or externally-asserted claims are marked `[UNVERIFIED external]` and
are never stated as current fact.

### 3.1 Desired Behavior

The target is a deliberate replatforming (not a like-for-like rewrite) of the SuperClaude/IronClaude Python orchestration layer onto Stack D = Mastra (agent/workflow runtime) + Backlog.md (markdown task-of-record + MCP) + Beads (issue/dependency graph), operating as a multi-tenant, multi-user, multi-tool company orchestration layer (`seed-brief.md:2,24`). The desired end behavior, decomposed by capability area:

| # | Desired behavior | What "good" looks like in the target stack | Source of requirement |
|---|---|---|---|
| TB-1 | **Sprint parity** — execute MDTM task phases (`tasklist-index.md` + `phase-N-tasklist.md`) with per-task/per-phase execution, checkpoints, stall/recovery, retrospective. | A durable workflow models phase→task execution; checkpoint reports remain first-class artifacts; result classification preserves exit-code + result-file + checkpoint semantics. | `seed-brief.md:17`; current sprint runtime `R03 §sprint/executor.py:1135-1757` |
| TB-2 | **Roadmap parity** — spec/TDD/PRD → extract → parallel generate → diff/debate/score/merge → anti-instinct → test-strategy → spec-fidelity → wiring → deviation → remediate, with convergence and cosmetic remediation. | Workflow DAG with first-class gate validators; deterministic steps stay deterministic; convergence keeps a durable deviation registry with stable IDs and budget accounting. | `seed-brief.md:18`; `R02 §roadmap/executor.py:1947-2208`, `R02 §convergence.py:90-668` |
| TB-3 | **Tasklist generate + validate** — generate sprint-compatible tasklist bundles from roadmaps, and validate roadmap↔tasklist fidelity. | Generation (currently skill-only) is implemented as a deterministic workflow or strictly-validated LLM node; validation (currently a single fidelity gate) is preserved. | `R02 §tasklist/executor.py:191-276`, `R02 §sc-tasklist-protocol/SKILL.md:91-123` (generation is skill, not CLI) |
| TB-4 | **Reusable skills/agents/harness** — preserve SuperClaude IP (skills, agents, commands, MDTM templates, gate logic) as instruction/policy packs. | Commands become front-door route manifests; skills become workflow/prompt packs; agents become role prompts; MDTM templates become task/issue schemas; gates become structured state transitions. | `seed-brief.md:24,29`; `R05 §src/superclaude/{commands,skills,agents,templates}` |
| TB-5 | **Multi-tool runtime** — drive multiple agent CLIs/models (Claude Code, Cursor, Codex, Gemini, Copilot), not just `claude`. | The runtime seam (`ClaudeProcess`) is replaced by a provider/runner adapter that can target heterogeneous models; current single-CLI driver is a hard limit. | `seed-brief.md:33,41`; current seam `R01 §pipeline/process.py:24-244` |
| TB-6 | **Multi-tenant governance** — tenant isolation, RBAC, cost attribution, audit, approvals as first-class. | A governance/control-plane layer (separate from Mastra+Backlog+Beads) owns tenant/actor/audit identity, scoped tool permissions, per-invocation audit, and cost metering. | `seed-brief.md:40`; `web-04 §finops.org`, `web-04 §scalekit.com/access-control` |
| TB-7 | **Task-of-record + dependency graph** — one canonical prose owner and one canonical dependency-graph owner, no drift. | Backlog.md likely owns human-readable task/doc/decision prose; Beads likely owns the queryable dependency DAG/ready-queue/memory; Mastra owns run state/traces. | `R07 §Ownership Matrix`; `web-02 §github.com/MrLesk/Backlog.md`, `web-03 §gastownhall/beads` |
| TB-8 | **Observability + diagnosability** — traces, run inspection, diagnostics that join task/phase/Backlog/Beads IDs. | Mastra observability/Studio with custom trace attributes; diagnostics remain attached artifacts. | `web-01 §mastra.ai/docs/observability/tracing/overview`; current diagnostics `R03 §diagnostics.py:72-232` |

### 3.2 Success Criteria

Carried from `seed-brief.md:44-51` (the study's own acceptance bar), framed as target-state checks. These are the criteria the *feasibility study* must satisfy; they are not yet met and are not recommendations (Sections 6–7 own go/no-go):

| ID | Success criterion | Evidence anchor |
|---|---|---|
| SC-1 | A defensible **go / no-go / hybrid** recommendation with V/C/L/R-style scoring and an explicit risk register. | `seed-brief.md:46` |
| SC-2 | A **component-by-component port matrix** (reuse-as-is / adapt / rewrite / drop) for each orchestration subsystem and harness class. | `seed-brief.md:47`; reuse seams in `R01`–`R05` |
| SC-3 | A **phased strangler-fig roadmap** with milestones, sequencing, dependencies, and rough complexity bands (not story points). | `seed-brief.md:48` |
| SC-4 | Explicit treatment of the **runtime seam** (`ClaudeProcess`/stream-json → Mastra workflows/agents) and the **task-of-record** decision (Backlog.md vs Beads vs both). | `seed-brief.md:49`; seam `R01 §pipeline/process.py:73-95` |
| SC-5 | A **risk register** covering Mastra EE license drift, Backlog/Beads overlap, loss of Claude-Code-native features (hooks, slash commands, permission modes), and multi-tenant security. | `seed-brief.md:50-51` |
| SC-6 | **Parity preservation criterion:** any port must preserve verified current contracts (gate tiers, sidecar gate target, trailing-gate advisory semantics, result-file freshness, checkpoint manifest, stable IDs) or consciously change them with tests. | `R01 §Section 8`, `R03 §Section 8`, `R07 §Ownership Rules` |
| SC-7 | **Round-trip compatibility criterion:** adapters must export task state back to `tasklist-index.md` + `phase-N-tasklist.md` such that `discover_phases()` and `parse_tasklist_file()` succeed and task counts match. | `R07 §Adapter Contract Sketches`, validation contracts |

### 3.3 Constraints

| ID | Constraint | Detail and evidence |
|---|---|---|
| CON-1 | **TypeScript vs Python boundary.** | Current orchestration is ~65K-LOC Python (`seed-brief.md:15`); Mastra is a TypeScript agent framework (`web-01 §mastra.ai/blog/announcing-mastra-1`). Pure-Python gate logic, parsers, and convergence engine (`R01 §gates.py:20-142`, `R03 §config.py:374-492`, `R02 §convergence.py:90-668`) must either be reimplemented in TS, wrapped as a Python subprocess/service, or kept hybrid. No mechanical translation exists. |
| CON-2 | **Mastra Enterprise licensing for production RBAC.** | Mastra core is Apache-2.0, but RBAC/FGA/Studio-auth/Agent-Builder are tied to the Enterprise Edition (`@mastra/core/auth/ee`, `StaticRBACProvider`, WorkOS FGA) and require a valid EE license in production (`web-01 §mastra.ai/docs/studio/auth`, `web-01 §mastra.ai/pricing`). Without auth, Studio and API routes are public (`web-01 §mastra.ai/docs/server/auth`). Team/multi-user deployment likely forces EE for production SSO/RBAC/audit/on-prem. |
| CON-3 | **Backlog.md vs Beads ownership overlap.** | Both can represent tasks/status/dependencies; one must be primary work-of-record, the other memory/graph (`seed-brief.md:34`). Backlog.md is local-file/git-centric markdown task store, not a multi-user transactional backend (`web-02 §github.com/MrLesk/Backlog.md`); Beads is a Dolt-backed dependency graph with ready-queue/gates (`web-03 §gastownhall/beads`). Backlog.md↔Beads integration is **not mature** — maintainer asks for a narrow import/export decision first (`web-02 §github.com/MrLesk/Backlog.md/issues/588`). |
| CON-4 | **Stable CLI/MCP/JSON integration boundaries.** | Backlog.md MCP task schemas reject unknown properties (`additionalProperties: false`) so arbitrary SuperClaude metadata cannot be added as MCP fields (`web-02 §src/mcp/tools/tasks/schemas.ts`); current Backlog MCP is an MVP stdio surface lacking decision tools (`web-02 §src/mcp/README.md`). Beads' stable contract is `bd --json` (schema v1, migrating to `BD_JSON_ENVELOPE`), and `.beads/issues.jsonl` is export-only, not canonical (`web-03 §docs/JSON_SCHEMA.md`, `web-03 §SYNC_CONCEPTS.md`). Adapters must target supported fields/CLI/MCP, not hand-edit files. |
| CON-5 | **SuperClaude safety/hook discipline must be preserved.** | Current safety lives in Claude Code hooks (freshness-pre-edit, workspace-write guards, source-context enrichment, subagent lifecycle) plus project rules (UV-only Python, `.claude/` source-of-truth/staging discipline, fork-only PR target) (`R05 §hooks/hooks.json:1-95`, `R05 §hooks/scripts/*`). These are Claude-Code-specific and **must be rebuilt as target middleware/guards**, not copied (`R11 §Synthesis Guardrails`). Mastra Workspace command execution does **not** replicate Claude Code hook/permission parity (`web-01 §Limitations`). |
| CON-6 | **Feasibility-study scope, not implementation.** | Output is requirements/analysis only; "do not port" must remain a live option; major-replatforming framing, not incremental upgrade (`seed-brief.md:37-38`). |
| CON-7 | **External maturity/version risk is real.** | Beads v1.0.5 carries explicit sync/migration upgrade warnings (`web-03 §github.com/gastownhall/beads/releases`); Backlog.md browser UI has an open state-loss bug under concurrent file changes (`web-02 §issues/578`); Mastra `@mastra/temporal` durable-execution integration is marked experimental (`web-01 §mastra.ai/docs/deployment/workflow-runners`). Version pinning and adoption gates are constraints, not optional. |

### 3.4 Target Ownership Split (hypothesis, pending product decision)

Derived from `R07 §Ownership Matrix` and tempered by web research. This is a target-state *hypothesis*, not a verified fact; every cross-system capability remains an assumption until validated:

| Data / artifact class | Proposed target owner | Mirror / secondary | Evidence + caveat |
|---|---|---|---|
| Human-readable task body, AC, checklist, decisions | Backlog.md | Mastra trace links, Beads metadata | Backlog.md is the markdown work-of-record (`web-02 §github.com/MrLesk/Backlog.md`); but custom orchestration metadata needs body-section/doc conventions or schema extension (`web-02 §src/types/index.ts`, `§schemas.ts`). `[UNVERIFIED external]` for exact extension points. |
| Machine dependency graph, ready-queue, blockers, project memory | Beads | Backlog.md retains visible dependency text | Beads offers typed deps, `bd ready`, gates, `bd remember` (`web-03 §docs/DEPENDENCIES.md`, `§github.com/gastownhall/beads`). Server mode required for multi-agent writers (`web-03 §DOLT.md`). |
| Workflow run state, retries, step status, traces | Mastra | Backlog/Beads summaries | Durable workflows + suspend/resume + snapshots + observability (`web-01 §workflows/suspend-and-resume`, `§observability/tracing/overview`); production durability depends on runner + storage choice (`web-01 §deployment/workflow-runners`). |
| Tenant/actor/audit identity, RBAC, cost attribution | **Separate governance/control-plane (new build)** | feeds from Mastra observability | Not provided by MCP, Mastra OSS, Backlog.md, or Beads (`web-04 §Synthesis`, `§finops.org`, `§scalekit.com`). Current scoped models carry no tenant/actor fields (`R07 §Gaps`, `R11 §RG-M3`). |
| Stable IDs / traceability (`TASK-*`, `R-*`, `T<PP>.<TT>`, `D-*`) | Shared cross-system keys, Backlog.md canonical | Mastra + Beads store as metadata | IDs already exist in current parsers (`R07 §Model Group A`, `R03 §config.py:374-492`). `[CODE-VERIFIED current IDs; target uncertain]`. |

---

## 4. Gap Analysis

Each row traces current state to research evidence (codebase `file:lines`) and target-stack capability to web research URLs. Severity scale: **Critical** = could be a go/no-go blocker or silent-failure risk; **High** = significant rework/risk requiring an explicit decision; **Medium** = real work but bounded; **Low** = minor/mechanical. Severity is an input to Sections 6–7, not a recommendation.

### 4.1 Runtime and Execution Gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| **G1. Language/runtime boundary** | ~65K-LOC Python orchestration; pure-Python gates (`R01 §gates.py:20-142`), markdown parsers (`R03 §config.py:374-492`), convergence engine (`R02 §convergence.py:90-668`), all stdlib-light. `[CODE-VERIFIED]` | Mastra is TypeScript; typed workflows via `createWorkflow()`/`createStep()` (`web-01 §mastra.ai/docs/workflows/overview`). Python logic must be reimplemented in TS, wrapped as a subprocess/service, or kept hybrid. | High | No mechanical Python→TS path. Hybrid (keep Python gate/parser logic behind a service) reduces rework but adds an IPC seam. Decision feeds Sections 6–7. |
| **G2. Durable workflow runtime** | Sequencing/retry/halt/parallel-group/cancellation/trailing-gate semantics live in `execute_pipeline()` + `_execute_single_step()` + `_run_parallel_steps()` (`R01 §executor.py:63-188,191-452`); sprint has a separate custom phase loop (`R03 §executor.py:1135-1757`). State is Python dataclasses + files. `[CODE-VERIFIED]` | Mastra workflows support suspend/resume, snapshots persisted to storage, resume-from-step, retries, scheduled/cron, multi-instance claiming (`web-01 §workflows/suspend-and-resume`, `§deployment/workflow-runners`). Production durability depends on runner (built-in/Inngest/Temporal) and storage choice. | High | Mastra plausibly expresses the wave→checkpoint→wave + gate/convergence loops, but rerun/replay/partial-rerun/idempotency must be hands-on validated (`web-01 §Limitations 1`). Temporal runner is experimental (`web-01 §Findings 1`). |
| **G3. Subprocess / Claude Code execution parity** | `ClaudeProcess` builds `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`, prompt via stdin, stdout/stderr to files, process-group SIGTERM→SIGKILL, timeout=124, `tool_write_mode` (`R01 §process.py:24-244`); sprint subclass uses `stream-json` + NDJSON monitor (`R03 §process.py:88-216`, `§monitor.py:253-571`). This is the single runtime seam. `[CODE-VERIFIED]` | Mastra Workspace `WorkspaceSandbox.executeCommand()` with start/stop/destroy, timeouts, stdout/stderr, `wait()`, bounded retention (`web-01 §workspace/sandbox`, `@mastra/core@1.1.0`). | Critical | Workspace can run CLI-like ops but does **NOT** prove parity with Claude Code hooks/permission model, stream-json monitoring, tmux IPC, or stall watchdogs (`web-01 §Findings 3`, `§Limitations 3`). Multi-tool requirement (TB-5) means a new provider adapter, not a 1:1 swap. |
| **G4. Hook / safety parity** | Safety is Claude Code hooks: freshness-pre-edit (blocks stale edits), reject-workspace-writes, source-context enrichment, subagent lifecycle (`R05 §hooks/hooks.json:1-95`, `§hooks/scripts/*`), plus UV-only/`.claude/` SoT/fork-PR project rules. `[CODE-VERIFIED behavior exists; UNVERIFIED portability]` | Mastra has guardrails, `requireToolApproval` HITL for MCP, runtime context/auth (`web-01 §mcp/overview`); MCP best practices add auth, scope minimization, no token passthrough (`web-04 §Findings 4,6`). | Critical | Hooks are not portable artifacts — must be rebuilt as middleware/guards (`R11 §Guardrail 3`). Mastra Workspace does not replicate freshness checks, staging restrictions, or permission prompts (`web-01 §Limitations 3`). Loss of Claude-Code-native enforcement is an irreducible-loss risk (`seed-brief.md:58`). |
| **G5. Subprocess safety controls (isolation)** | `eval` has strong per-execution HOME isolation + scratch-root allowlists + containment guards (`R04 §isolation.py:224-642`); but sprint's documented 4-layer isolation is **not active** — only Path B sets `CLAUDE_WORK_DIR`, Path A passes no isolation env (`R03 §executor.py:106-182,1303-1324,1076-1115`). `[CODE-VERIFIED]` | Mastra Workspace process management + timeouts + bounded retention (`web-01 §workspace/sandbox`); subprocess safety (allowlists, env isolation, secret redaction, approval) must be designed (`web-01 §Limitations 6`). | High | Do **not** claim active 4-layer isolation as current behavior. Target can implement stronger isolation, but that is a behavior change, not parity (`R11 §03 setup_isolation`). `eval` isolation is the strongest reusable pattern. |

### 4.2 State, Tenancy, and Governance Gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| **G6. Tenant-aware state model** | Scoped models (`PipelineConfig`, `SprintConfig`, `TaskResult`, `MonitorState`, `TurnLedger`) carry model/permission/budget/runtime fields but **no tenant/actor identity fields** in read ranges (`R07 §Gaps`, `R11 §RG-M3`). `[UNVERIFIED repo-wide; scoped absence only]` | Mastra Platform Organizations are multi-tenant containers; Projects span deployments (`web-01 §mastra-platform/overview`). Multi-tenant agents need separate trigger/execution/authorization/tenant/attribution identities (`web-04 §Findings 9, scalekit.com/access-control`). | Critical | Tenancy is the strategic driver (`seed-brief.md:40`) but absent from current models. Conflating execution and tenant identity causes silent access-control bugs (`web-04 §Findings 9`). Must be a new target design dimension, not assumed-existing. |
| **G7. Auth / RBAC / governance / cost attribution** | No auth/RBAC layer in scoped code; only sprint-local `TurnLedger` budget accounting (`R07 §Model Group B`, `sprint/models.py:692-777`). `[CODE-VERIFIED absence in scope]` | Mastra RBAC/FGA/SSO/audit are **Enterprise-licensed** (`web-01 §Findings 6, mastra.ai/docs/studio/auth, /pricing`). MCP is not a governance platform; needs control-plane (identity, policy, audit, cost) (`web-04 §Synthesis`). Backlog.md/Beads provide no cross-tenant IAM/audit/cost (`web-04 §Findings 14,15`). | Critical | Company-wide multi-tenant deployment needs (a) Mastra EE for production RBAC/SSO/audit OR a separate auth layer, AND (b) a **new governance/control-plane** for cost attribution/metering/budgets/tool catalog (`web-04 §Recommendations 2,7`). License + build cost is a go/no-go input. |
| **G8. Backlog.md / Beads ownership overlap + immature integration** | Current task-of-record is markdown MDTM/tasklist files; dependencies are parsed but **not scheduling drivers** — sprint executes file order (`R06 §Section 9`, `R03 §executor.py:971-1010`). `[CODE-VERIFIED]` | Backlog.md = markdown task/doc/decision store (`web-02 §github.com/MrLesk/Backlog.md`); Beads = dependency DAG + ready-queue + gates + memory (`web-03 §docs/DEPENDENCIES.md`). **Both can hold tasks/status/deps → overlap.** Backlog.md↔Beads integration is immature; maintainer wants a narrow import/export decision first (`web-02 §issues/588`). | High | One must be primary work-of-record, other memory (`seed-brief.md:34`). Adopting Beads' dependency-driven scheduling is a **behavior change** vs current file-order execution, not a runtime swap (`R06 §Section 9`). Dual status owners create drift unless one is canonical (`R07 §Ownership Rules 1-2`). |
| **G9. Beads storage reality (Dolt, not SQLite/JSONL)** | N/A in current repo (no Beads integration). Seed brief asserts "SQLite or Dolt server-mode" and "`.beads/` Dolt or SQLite + JSONL" (`seed-brief.md:31`). `[UNVERIFIED external in seed]` | Current Beads is **Dolt-first**; the local Dolt DB is source of truth; `.beads/issues.jsonl` is **export/interchange only**, not canonical sync (`web-03 §Findings 7, SYNC_CONCEPTS.md`). Embedded mode = single-writer; **server/shared-server mode required for multi-agent concurrent writers** (`web-03 §Findings 8,9, DOLT.md`). | High | **Corrects the seed brief**: do not design around SQLite/JSONL canonical storage. Multi-tenant/parallel orchestration mandates Beads server mode + version pinning; v1.0.5 has sync/migration upgrade hazards (`web-03 §Findings 2`). Tools reading old JSONL directly are incompatible (`web-03 §Findings 7`). |

### 4.3 Pipeline-Internal Parity Gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| **G10. Checkpoint contract nuance** | Canonical `/sc:tasklist` checkpoints are numbered task entries `### T<PP>.<NN> -- Checkpoint:` with `Checkpoint Report Path:` (`R09 §SKILL.md:343-391,947-1027`); runtime parser `checkpoints.py` accepts both numbered + legacy `### Checkpoint:` (`R09 §checkpoints.py:18-33`). But `phase-template.md`, `sprint/process.py` prompt, and several comments still reference legacy sibling sections `[CODE-CONTRADICTED]`; and per-task (Path A) branch does **not** call `_verify_checkpoints()` (`R09 §executor.py:1259-1301` vs `:1512-1531`). | Backlog.md checkpoints map to verification tasks + linked docs; Beads can map checkpoint nodes/gates (`web-03 §Findings 6, gates`); Mastra verifies/generates reports in-workflow. | High | Adapters must emit **numbered checkpoint task entries with `Checkpoint Report Path:`** (the strongest compatibility anchor) and not sibling sections (`R09 §Adapter Implications`). Per-task checkpoint verification gap is a current runtime hole to preserve-or-fix consciously, not silently inherit. |
| **G11. Roadmap defined-only `certify` + sprint Path A/B risks** | `CERTIFY_GATE`, `build_certify_step`, `check_certify_resume` exist and docs/tests list `certify` as a step, but production `_build_steps` does **not** wire it; no production call to `build_certify_step` found (`R02 §executor.py:1899-1944,1947-2208`, `§Gaps 1`). Sprint has real Path A (per-task, weaker monitor/isolation) vs Path B (freeform, richer monitor/checkpoint) divergence (`R03 §Section 4,8`). `[CODE-VERIFIED defined-only / Path split]` | Workflow DAG would make every gate an explicit node; a port must decide whether `certify` is wired, deferred, or dropped, and whether to normalize Path A/B. | High | Do **not** list certification as a currently-wired production step (`R11 §02-G1`). Path A/B divergence means "phases and tasks" modeling under-captures real complexity; sprint is the hardest port surface and should not be first (`R03 §Section 8`). |
| **G12. Roadmap wiring gate trailing-vs-blocking + compressed-sidecar nuance** | `wiring-verification` declares `GateMode.TRAILING`, but default `grace_period=0` forces `BLOCKING`, and no roadmap CLI grace-period flag exists → effectively blocking (`R02 §executor.py:2175-2184`, `R01 §executor.py:211-215`). Gates validate `.compressed.md` sidecars when present, contradicting a roadmap code comment (`R01 §executor.py:23-35`, `§roadmap/executor.py:1217-1219` `[CODE-CONTRADICTED]`). Trailing-gate failures are **advisory** (warn-only, do not change `StepResult`) (`R01 §executor.py:175-187`). | Mastra scorers/validators per node; trailing/advisory checks become non-blocking annotations or Beads non-blocking relations (`web-03 §DEPENDENCIES.md` non-blocking types). | Medium | Preserve current effective behavior (sidecar gate target; advisory trailing) unless the port consciously strengthens it (`R01 §Section 8 items 6-8`). State effective vs intended behavior separately. Migration hazard if a stricter target silently makes trailing failures blocking. |
| **G13. Tasklist generation vs validation split** | CLI exposes only `tasklist validate` (single `tasklist-fidelity` strict-gate step) (`R02 §tasklist/executor.py:191-276`); **generation is skill/protocol only** (`sc-tasklist-protocol`), no `superclaude tasklist generate` (`R02 §prompts.py:156-162`, `§SKILL.md:91-123`). `[CODE-VERIFIED]` | Mastra could implement generation as a deterministic workflow or strictly-validated LLM node; Backlog.md/Beads store the generated bundle (`web-02 §github.com/MrLesk/Backlog.md`, `web-03 §github.com/gastownhall/beads`). | High | Any claim of "tasklist CLI parity" must separate **validate (Python, exists)** from **generate (skill protocol, no Python generator)**. A port must implement the `sc-tasklist-protocol` algorithm as real workflow logic with strict output validation, with mandatory sprint-parser round-trip tests (SC-7). |

### 4.4 Cross-Cutting and Reuse Gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| **G14. Stable integration boundaries (MCP/JSON schema)** | Current CLI uses `claude` subprocess; no MCP in investigated pipeline paths (repo-wide no-MCP claim is `[UNVERIFIED]`, `R01 §Gaps 2`). Markdown artifacts + file paths are the integration contract (`R07 §Model Group A,B`). | Backlog.md MCP rejects unknown props (`additionalProperties:false`) and current MCP is an MVP without decision tools (`web-02 §schemas.ts, §src/mcp/README.md`); Beads stable surface is `bd --json` migrating to envelope mode, JSONL export-only (`web-03 §JSON_SCHEMA.md`). MCP itself is not governance (`web-04 §Findings 1`). | High | Adapters must target supported fields/CLI/MCP, not arbitrary metadata or file edits (`web-02 §Recommendations 3,4`; `web-03 §Recommendations 2`). SuperClaude-specific metadata needs body-sections/docs or schema extension. Dual JSON parsers needed for Beads legacy+envelope. |
| **G15. Source-of-truth / instruction-corpus ingestion** | `src/superclaude/` is canonical per core instructions; `.claude/` are synced dev copies (`R05 §core/CLAUDE.md:45-48` `[CODE-VERIFIED]`); but plugin-mirror READMEs say edit `plugins/superclaude/` first and mirrors are materially out of sync (`R11 §RG-I4` `[CODE-CONTRADICTED]`). | A port consumes the instruction corpus (skills/agents/commands/templates) as policy packs (`R05 §Section 8`). | Medium | Port must include a source-of-truth resolver + mirror-sync verification before ingesting corpus (`R11 §Guardrail 2`). Use `src/superclaude/` meanwhile. Inventories are scoped/sampled, not exhaustive semantic parity (`R11 §RG-M2`). |
| **G16. Unsupported / unverified implementation inputs** | `/sc:forensic` (referenced by TFEP) has **no** command/skill file in `src/superclaude` (`R11 §RG-I5` `[CODE-CONTRADICTED]`); no sprint `rerun-tasks` CLI verb in current `sprint/commands.py` (`R11 §evidence table` `[CODE-CONTRADICTED]`) — contradicts seed brief "recoverable per-task reruns" (`seed-brief.md:17`). Retrospective generator **does** exist and runs at sprint end (`R11 §RG-I5` `[CODE-VERIFIED]`). | N/A target-stack capability; these are current-state correction items. | Medium | Exclude `/sc:forensic` and sprint `rerun-tasks` from current-state/implementation inputs unless separately located/built; the project memory `reference_sprint_rerun_tasks` mentions a v4.3.0 `sprint rerun-tasks` verb — **this scoped research did not find it in current source**, so treat as unverified pending a broader/branch search. Diagnostic chain is static Markdown, not agentic (`R01 §diagnostic_chain.py:71-158`); do not overstate. |
| **G17. Observability / diagnosability mapping** | Diagnostics are deterministic collectors/classifiers + JSONL/Markdown logs; `status`/`logs` sprint subcommands are **stubs** (`R03 §logging_.py:224-235`, `§diagnostics.py:72-232` `[CODE-VERIFIED]`). | Mastra AI-tracing auto-instruments agent/LLM/tool/workflow steps; Studio inspects runs/traces; 1.0 unified schema (`web-01 §observability/tracing/overview, §studio/overview`). | Low | Strong target capability; needs custom trace attributes to join task/phase/Backlog/Beads IDs + git branch/commit (`web-01 §Recommendations 6`). Do not claim live `status`/`logs` as current capability. |

### 4.5 Required-Coverage Cross-Check

Mapping of the task's minimum-required gaps to the rows above (ensures none are dropped):

| Required gap (from task brief) | Covered by |
|---|---|
| language/runtime boundary | G1 |
| durable workflow runtime | G2 |
| subprocess/Claude Code execution parity | G3 |
| hook/safety parity | G4 (+ G5 isolation) |
| tenant-aware state model | G6 |
| auth/RBAC/governance/cost-attribution | G7 |
| Backlog.md/Beads ownership + overlap + immature Beads integration | G8 |
| Beads Dolt storage reality (not SQLite/JSONL) | G9 |
| checkpoint contract nuance | G10 |
| roadmap defined-only/certify and sprint Path A/B internal risks | G11 (+ G12 wiring/sidecar) |
| tasklist generation vs validation split | G13 |

### 4.6 Severity Roll-Up

- **Critical (4):** G3 (subprocess/Claude-Code parity), G4 (hook/safety parity), G6 (tenant state), G7 (auth/RBAC/governance/cost).
- **High (9):** G1, G2, G5, G8, G9, G10, G11, G13, G14.
- **Medium (3):** G12, G15, G16.
- **Low (1):** G17.

The Critical cluster concentrates in two areas: (1) the runtime seam + Claude-Code-native safety that cannot be assumed-portable (G3/G4), and (2) the multi-tenant governance layer that **does not exist** in current code and is **not supplied** by Mastra OSS / Backlog.md / Beads (G6/G7). These four drive the go/no-go calculus that Sections 6–7 resolve.

---

## 5. External Research Findings

This section synthesizes EXTERNAL research only. It does not override the codebase findings elsewhere in this report.

**Authority order (per task rules):**

1. **Codebase is source of truth.** External research adds context and options; where external claims touch the actual SuperClaude/IronClaude code, the verified-code findings in Sections 1-4 govern. Discrepancies are noted explicitly here.
2. **Fresh web research (web-01..04, dated 2026-06-02) supersedes the older enrichment seed (`research-deep.md`)** wherever the two differ. The seed encoded several Stack D assumptions that the fresh research corrects or qualifies; those corrections are called out in dedicated "Seed Correction" callouts below.

**Reliability ratings** are the per-finding ratings carried from the source web agents (HIGH / MEDIUM-HIGH / MEDIUM), reflecting source authority (official docs/repo > vendor blog > third-party writeup) and corroboration.

**Relationship-to-codebase** is one of: **Supports** (external evidence reinforces a codebase need/seam), **Extends** (adds capability/option beyond current code), **Contradicts** (external reality conflicts with a codebase assumption or a prior seed claim), or **Neutral/Context**.

**Provenance:** All fresh findings used Tavily search/extract first (plus Context7 for Mastra docs); no WebSearch/WebFetch fallback fired. `provider=tavily`.

### 5.1 Mastra (Runtime / Workflow / ACP Seam)

Mastra is the candidate TypeScript runtime and workflow engine, and — critically — the candidate replacement for the SuperClaude `ClaudeProcess`/stream-json subprocess seam (via `@mastra/acp` `AcpAgent`).

#### 5.1.1 Capability Findings

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| M1 | Durable workflows: `suspend()`/`resume()`/`resumeStream()` serialize a full snapshot (runId, per-step status, payloads, output) to configured storage; snapshots persist across deployments and restarts. Direct analog to MDTM checkpoints and the desired recoverable per-task rerun concept; this report separately notes that a current sprint `rerun-tasks` CLI verb was not found in scoped source. | HIGH | Supports | [suspend-and-resume](https://mastra.ai/docs/workflows/suspend-and-resume) ; Context7 `/mastra-ai/mastra` |
| M2 | Code-defined workflow graph: `createWorkflow()`/`createStep()` with `.then()`, `.branch()`, `.parallel()`, `.map()`, loops (`.dountil()`/`.dowhile()`/`.foreach()`), Zod-typed step IO, nested workflows. Covers sprint/roadmap/pipeline phase-graph control flow. | HIGH | Supports | [workflows/overview](https://mastra.ai/docs/workflows/overview) |
| M3 | `@mastra/acp` `AcpAgent` spawns an ACP coding-agent CLI as a subprocess subagent (streaming, runtime model selection, persistent sessions, sandboxed workspace). Example drives Claude Code via `npx -y @agentclientprotocol/claude-agent-acp`. **The decisive structural replacement for `ClaudeProcess` spawning `claude --print --verbose` with stream-json.** Requires `@mastra/core@1.34.0+`. | HIGH | Extends | [Mastra releases](https://github.com/mastra-ai/mastra/releases); enrichment `research-deep.md` (ACP intro blog / PR #16423 cited there) |
| M4 | Mastra Workspace / `WorkspaceSandbox`: persistent filesystem + `executeCommand(command, args?, options?)`, `start()/stop()/destroy()`, timeouts, status/resource reporting, bounded retention (`maxRetainedBytes`). Added `@mastra/core@1.1.0`. Candidate subprocess/command-execution layer. | HIGH | Extends | [workspace/overview](https://mastra.ai/docs/workspace/overview) ; [workspace/sandbox](https://mastra.ai/reference/workspace/sandbox) |
| M5 | Storage: libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare; `MastraCompositeStore` routes memory/workflows/scores/observability to different backends. ClickHouse for prod observability, libSQL for local dev. | HIGH | Supports | [memory/storage](https://mastra.ai/docs/memory/storage) ; [storage/composite](https://mastra.ai/reference/storage/composite) |
| M6 | Observability: OpenTelemetry-native, auto-instruments agent runs/LLM gen/tool calls/workflow steps with token/cost attribution; exporters (Datadog, Langfuse, Arize, Braintrust, SigNoz, Mastra platform). Studio visualizes workflow graphs/traces, runs tools in isolation. 1.0 unified schema (`entityId`/`entityType`/`entityName`). | HIGH | Supports | [observability/tracing/overview](https://mastra.ai/docs/observability/tracing/overview) ; [studio/overview](https://mastra.ai/docs/studio/overview) |
| M7 | MCP: `MCPClient` (stdio/HTTP/SSE outbound) and `MCPServer` (expose agents/tools/workflows over HTTP). `requireToolApproval` for HITL approval of MCP tool execution; recent FGA enforcement for MCP tool execution. | HIGH | Supports | [mcp/overview](https://mastra.ai/docs/mcp/overview) |
| M8 | Deployment: `mastra dev`/`build`/`start`, `mastra server deploy` (Docker image + URL). Hono-based generated server; adapters for Express/Hono/Fastify/Koa; agents/workflows become REST endpoints with OpenAPI. Self-host Node/Bun, Vercel, Cloudflare, Render, K8s/EKS. Node ≥22.13.0. | HIGH | Extends | [server/mastra-server](https://mastra.ai/docs/server/mastra-server) ; [research-deep.md] |
| M9 | Durability extras: `DurableAgent` + resumable streams survive client disconnect and server crash via cached events + `observe(runId,{offset})`. Inngest integration adds durable step memoization, retries, and **per-tenant concurrency/backpressure** (3rd-party engine). | HIGH | Extends | [Mastra releases](https://github.com/mastra-ai/mastra/releases); [workflow runners](https://mastra.ai/docs/deployment/workflow-runners); enrichment `research-deep.md` (release note cited there) |

#### 5.1.2 Licensing and Multi-Tenancy (Key Risk)

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| M10 | **Dual license.** Apache-2.0 governs the main framework (agents, workflows, storage adapters, Server, observability core). A separate **Mastra Enterprise Edition (EE) License** (`ee/LICENSE`, a bespoke commercial license — NOT Elastic 2.0 / BSL) governs everything under any `ee/` directory. EE "production" = any use beyond dev+testing on your own systems; requires a written commercial agreement; redistribution/sublicense/sell forbidden. | HIGH | Contradicts (seed framing) | [research-deep.md] (ee/LICENSE verified); Context7 `/mastra-ai/mastra` |
| M11 | **Production RBAC/SSO/FGA is EE-gated.** `server.auth` (who) is separate from `server.rbac` (what). SimpleAuth (API-key→{id,name,role}) works license-free. But `StaticRBACProvider`, `DEFAULT_ROLES` (owner/admin/member/viewer), WorkOS/Okta SSO, permission-based Studio UI, and Agent Builder multi-tenant workflows import from `@mastra/core/auth/ee` and **require a paid EE license in production**. | HIGH | Contradicts (Stack-D "feasible OSS multi-tenant" assumption) | [server/auth](https://mastra.ai/docs/server/auth) ; [studio/auth](https://mastra.ai/docs/studio/auth) ; [pricing](https://mastra.ai/pricing) |
| M12 | Without auth, Studio and API routes are public. Agent Builder without RBAC grants every authenticated user full access. Real per-tenant concurrency isolation / noisy-neighbor protection is NOT in Apache core — it comes from the Inngest engine integration. | HIGH | Contradicts (governance gap) | [server/auth](https://mastra.ai/docs/server/auth) ; [research-deep.md] |

> **SEED CORRECTION / CONFIRMATION (Mastra licensing).** Task rule 3 calls out: *"Mastra production RBAC/auth is Enterprise-licensed."* Both the fresh web research (web-01 finding 6) and the enrichment seed AGREE on this — it is the single biggest strategic gate for any company-wide multi-tenant SuperClaude port. The fresh research SHARPENS the seed by confirming via official docs that EE is a bespoke commercial license (not Elastic/BSL) and that production use of `ee/` requires a written agreement. **Net: a multi-tenant RBAC platform on Mastra is feasible but commercially gated; the OSS Apache path yields only SimpleAuth (flat API-key→role) + application-level storage scoping, with the RBAC/tenant layer DIY.**

#### 5.1.3 Maturity Claims and Open Questions

| # | Finding | Rating | Note |
|---|---------|--------|------|
| M13 | 1.0.0 reached 2026-01-20; verified later core releases through 1.16.0 (2026-03-23); ACP floor `@mastra/core@1.34.0+`. ~300k weekly npm downloads, 22-24k GitHub stars, 300+ contributors. Production claims (Replit, PayPal, Sanity). | MEDIUM | Vendor claims; PRECISE current-latest core version UNVERIFIED beyond the `>=1.34.0` floor. |
| M14 | `@mastra/temporal` marked experimental/not-production-ready in at least one current deployment page; treat Temporal cautiously vs. Inngest. | MEDIUM | Runner choice affects production retry/durability semantics. |

**UNVERIFIED / needs hands-on validation (carried forward to Gaps):**

- Workflow restart/replay/partial-rerun/idempotency semantics (claimed analog to MDTM, not empirically proven against SuperClaude reruns).
- Whether `@mastra/acp` itself sits under Apache or an `ee/` path is UNVERIFIED.
- `max_turns` / permission-flag / model parity between `AcpAgent` (ACP contract) and the current `ClaudeProcess` stream-json knobs is UNVERIFIED.
- Cursor / Gemini CLI / Copilot driving via Mastra `AcpAgent` is plausible (they speak ACP) but NOT explicitly validated in Mastra's own docs.
- **Claude Code hook parity is NOT established.** Mastra Workspace command execution does NOT replicate SuperClaude/Claude Code hooks (UserPromptSubmit session-context injection, freshness-pre-edit, verify-sync), UV-only Python rule, git-safety, `.claude/` source-of-truth/staging discipline, or fork-PR-target enforcement. These would need re-implementation as Mastra processors/middleware or be dropped.

### 5.2 Backlog.md (Markdown Task-of-Record)

Backlog.md is the candidate human-readable, repo-local task/docs/decision work-of-record, mapped onto the MDTM tasklist-index format.

#### 5.2.1 Capability Findings

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| B1 | Markdown-native tasks in a project-local `backlog/` folder (committed `.md` files w/ YAML frontmatter, `task-10 - Add core search.md`); CLI + TUI Kanban (`backlog board`) + web UI (`backlog browser`) + fuzzy search + docs + decisions + MCP, all over one source of truth. MIT license. v1.45.2 (released 2026-05-30), TypeScript/Bun, active (~5.7k stars, 185 releases). | HIGH | Supports | [github.com/MrLesk/Backlog.md](https://github.com/MrLesk/Backlog.md) |
| B2 | Rich first-class task schema maps onto MDTM phase items: `status`, `assignee`, `labels`, `priority`, acceptance criteria (per-criterion `--check-ac N`), `--plan`, `--notes`, `--final-summary`, `dependencies` (`--dep`, with circular-dependency guard), parent/subtasks, `ordinal`, `modifiedFiles`. Concurrency-hardened (BACK-404 task-ID locking). | HIGH | Supports | [src/types/index.ts](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/types/index.ts) ; [CLI-INSTRUCTIONS.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md) |
| B3 | Docs (`backlog doc create -p guides`) and decisions/ADR (`backlog decision create -s proposed`) are first-class at the CLI/data layer — candidate host for roadmap/adversarial `decision.add` obligations. Absolute paths / `..` traversal rejected. | HIGH | Supports | [CLI-INSTRUCTIONS.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md) |
| B4 | Git is optional: `backlog init --no-git` creates a filesystem-only project; config `remoteOperations`, `autoCommit` (default false), `filesystemOnly`. Supports both repo-native and no-git orchestration. | HIGH | Extends | [ADVANCED-CONFIG.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/ADVANCED-CONFIG.md) |
| B5 | Built-in MCP server (`backlog mcp start`, stdio); `backlog init` can auto-configure it. Agent workflow guidance (decompose → AC → one-task-per-session/PR → research/plan → implement/verify → rerun fresh) aligns with SuperClaude tasklist discipline. | HIGH | Supports | [github.com/MrLesk/Backlog.md](https://github.com/MrLesk/Backlog.md) ; [src/mcp/README.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md) |

#### 5.2.2 Limitations and Contradictions

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| B6 | **MCP is an MVP stdio surface**, smaller than older "75+ tools" claims. README: "minimal stdio MCP surface" routing through Core APIs. Current MCP task tools: `task_create/list/search/edit/view/archive/complete`; plus `milestone_*`, `definition_of_done_defaults_*`, `document_*`. | HIGH | Contradicts (older claims) | [src/mcp/README.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md) ; [src/mcp/tools/tasks/index.ts](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/index.ts) |
| B7 | **MCP task schemas reject unknown properties (`additionalProperties: false`).** SuperClaude-specific orchestration metadata CANNOT simply be added as arbitrary MCP fields — must use supported fields, body sections, docs, references, or extend Backlog.md. | HIGH | Contradicts (arbitrary-frontmatter assumption) | [src/mcp/tools/tasks/schemas.ts](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/schemas.ts) |
| B8 | **CLI > MCP coverage.** Decisions are first-class in CLI but NOT clearly exposed in the current MCP MVP README — a CLI-vs-MCP coverage gap. Use CLI for decisions until MCP decision support is verified at runtime. | HIGH | Contradicts (seed "decisions via MCP" assumption) | [CLI-INSTRUCTIONS.md](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md) |
| B9 | No built-in sprint/roadmap pipeline equivalent; no dependency-GRAPH engine (intra-project `--dep` edges only, not a queryable graph DB); no execution/orchestration runtime. Backlog.md replaces the MDTM tasklist-index FORMAT, NOT the ~65K-LOC pipeline logic or the `ClaudeProcess` seam. | HIGH | Neutral/Context | [CLI instructions](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/CLI-INSTRUCTIONS.md); [Backlog.md repo](https://github.com/MrLesk/Backlog.md); enrichment `research-deep.md` |
| B10 | Browser UI open state-loss bug #578: "UI state resets if files change while browser UI is running" — unsaved draft text cleared when an agent updates files concurrently (BACK-429 open). | HIGH | Neutral/Context | [issue #578](https://github.com/MrLesk/Backlog.md/issues/578) |
| B11 | Local-file/git-centric, NOT a centralized multi-user transactional PM backend. `proper-lockfile` dependency; single-writer-per-repo git model can contend under true concurrent multi-user write load. **NO native multi-tenancy / RBAC / auth / remote-HTTP transport in the official server — stdio + single-repo + single-trust-domain by design.** | MEDIUM-HIGH | Contradicts (multi-tenant expectation) | [Backlog.md repo](https://github.com/MrLesk/Backlog.md); [package.json](https://raw.githubusercontent.com/MrLesk/Backlog.md/main/package.json); enrichment `research-deep.md` |
| B12 | Beads ↔ Backlog.md integration is NOT mature. Open feature request #588; maintainer: *"This needs a narrower integration decision before tasking... start by choosing one workflow, such as import/export sync with Beads, rather than committing to a broad integration surface."* | HIGH | Contradicts (seed "shared repo metadata references" claim) | [issue #588](https://github.com/MrLesk/Backlog.md/issues/588) |

#### 5.2.3 The BACK-407 Conflict (Seed vs. Fresh Research)

> **SEED CORRECTION (BACK-407 specifically UNVERIFIED).** Task rule 3 calls out: *"Backlog.md MCP is an MVP surface and BACK-407 specifically unverified (BACK-408 found)."* The two external sources DISAGREE:
>
> | Source | Claim about BACK-407 | Strength |
> |--------|----------------------|----------|
> | Enrichment seed (`research-deep.md`) | BACK-407 ("Align MCP server with latest spec") is **MERGED in v1.43.0 (2026-03-21)**, plus a companion chain BACK-406/403/408/434/436/465. Cites release notes + newreleases.io. | Asserted as verified. |
> | Fresh web-02 (2026-06-02) | BACK-407 **could NOT be confirmed**; search surfaced **BACK-408** (consolidate MCP workflow guide tools) instead. The MCP README presents only an **MVP** surface. Doc drift observed (`agent-nudge.md` resource selectors vs. README `backlog://docs/task-workflow`). | Marked `[UNVERIFIED]`. |
>
> **Resolution for this report:** Per task rule 2, the fresh research governs. Treat BACK-407's specific scope/merge status as **UNVERIFIED** and the Backlog.md MCP as an **MVP surface with active churn and doc drift**. Do NOT build the integration decision on an assumed "spec-aligned, BACK-407-complete" MCP. **Action:** verify the live MCP tool catalog with `backlog mcp start` + an `/mcp` probe (and check decision/milestone tool exposure) before committing any `decision.add` / metadata-mapping dependency. BACK-408 (workflow-guide consolidation) IS the corroborated item across both sources.

### 5.3 Beads (Dependency Graph / Agent Memory)

Beads is the candidate machine-facing dependency graph, ready-work scheduler, and cross-session agent memory.

#### 5.3.1 Capability Findings

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| BD1 | Current repo `gastownhall/beads` (Steve Yegge's org). "Distributed graph issue tracker for AI agents, powered by Dolt." High activity (24.3k stars, 91 releases). Packages: npm `@beads/bd`, PyPI `beads-mcp`. | HIGH | Neutral/Context | [github.com/gastownhall/beads](https://github.com/gastownhall/beads) |
| BD2 | Agent-native CLI: `bd ready` (unblocked + priority-sorted work), `bd create -p 0`, `bd update <id> --claim` (atomic claim: assignee + in_progress), `bd dep add <child> <parent>`, `bd show <id>` (details + audit trail), `bd prime` (agent context + memories), `bd remember` (persistent project memory). Maps directly to SuperClaude orchestration primitives. | HIGH | Supports | [github.com/gastownhall/beads](https://github.com/gastownhall/beads) ; SETUP.md |
| BD3 | Dependency graph richer than simple blockers. Blocking (affect `bd ready`): `blocks`, `parent-child`, `conditional-blocks`, `waits-for`. Non-blocking: `related`, `tracks`, `discovered-from`, `caused-by`, `validates`, `supersedes`. `bd dep add` rejects cycles at write time. Maps to SuperClaude wave/planning dependencies. | HIGH | Supports | [DEPENDENCIES.md](https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md) |
| BD4 | **Gates bridge Beads state to external code/CI state**: `gh:pr` (PR merged), `gh:run` (CI success), `timer`, `bead` (cross-rig issue closed), `human` (manual approval). `bd gate check`/`discover`. Directly maps to SuperClaude's "work done" vs "merged/validated" distinction — validation/PR-merge phases could be encoded as gates. | HIGH | Extends | [DEPENDENCIES.md](https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md) |
| BD5 | `bd --json` is the stable integration contract (use `--json`, not `--format json`). Schema version `1`; `BD_JSON_ENVELOPE=1` opts into a uniform envelope (planned default v2.0). Legacy list commands emit raw arrays; `bd export --json` emits JSONL (not envelope-wrapped). Integrations need a dual parser (legacy + envelope). | HIGH | Supports | [JSON_SCHEMA.md](https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md) |
| BD6 | Hash-based collision-resistant IDs (`bd-a1b2`, dotted epics `bd-a3f8.1.1`) purpose-built for concurrent multi-agent/multi-branch writes. 5 priority levels P0-P4. Higher-level primitives: Formulas (workflow templates), Molecules (work graphs), Gates, GitHub Issues sync. | HIGH | Extends | [Beads repo](https://github.com/gastownhall/beads); enrichment `research-deep.md` (pkg.go.dev + README cited there) |

#### 5.3.2 Storage Backend — Seed Correction

> **SEED CORRECTION (Beads is Dolt-first, NOT SQLite/JSONL).** Task rule 3 calls out: *"Beads is Dolt-first (not SQLite/JSONL)."* This is the most consequential correction in this section.
>
> | Claim | Status |
> |-------|--------|
> | Seed-brief / Stack-D framing: "embedded SQLite or Dolt server-mode", "`.beads/` Dolt or SQLite + JSONL" | **CONTRADICTED** by current official docs. |
> | Current reality (web-03 + research-deep.md verified facts): **Beads uses Dolt ONLY** as of the 1.0 line. The classic SQLite+JSONL+git backend was REMOVED (early Feb 2026). "The local Dolt database is the source of truth for `bd list/show/ready` and every write command." | **VERIFIED** (official README, DOLT.md, SYNC_CONCEPTS.md). |
> | `.beads/issues.jsonl` role | **Export/interop/migration/backup ONLY** — NOT canonical cross-machine sync; does not capture Dolt branches/history/working-set. Tools reading old JSONL directly are **incompatible** with current versions. Use `bd backup` for restorable backups. |
> | Why the seed was wrong | Third-party writeups (Peter Warnock, Better Stack) still describe the older SQLite+JSONL architecture and are **stale**. A Rust fork (`beads_rust`) deliberately freezes the classic SQLite+JSONL architecture — confirming the divergence. |
>
> **Implication for the port:** Any integration must (1) drive `bd ... --json` rather than read `.beads/issues.jsonl`, (2) treat Dolt (embedded or server) as the store of record, and (3) use Dolt-native sync/backup (`bd dolt push/pull`, `bd bootstrap`, `bd backup`). Exclude JSONL-direct community tools unless updated for Dolt.

#### 5.3.3 Concurrency, Modes, and Risk

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| BD7 | Two Dolt modes: **Embedded** (default, in-process, `.beads/embeddeddolt/`, **single-writer** with file lock — "database is locked" under contention, solo only) vs **Server** (external `dolt sql-server`, `.beads/dolt/`, multiple concurrent writers, `bd init --server`). History: v0.56.1 removed embedded → v0.63.0 reintroduced as default → v1.0.0 stable. | HIGH | Neutral/Context | [DOLT.md](https://github.com/gastownhall/beads/blob/main/docs/DOLT.md) |
| BD8 | **Server mode is REQUIRED for SuperClaude parallel/multi-agent orchestration**; embedded is insufficient for concurrent writers. Atomic claim `bd update <id> --claim --assignee <agent>`; sync via Dolt remotes under `refs/dolt/data`. Shared-server mode (`~/.beads/shared-server/`, port 3308) hosts multiple projects by prefix. | HIGH | Supports | [DOLT.md](https://github.com/gastownhall/beads/blob/main/docs/DOLT.md) ; SYNC_CONCEPTS.md |
| BD9 | Session attribution is actively changing (issues #3400/#3583: `--claim` could lose session info; acceptance criteria added `--session`/`CLAUDE_SESSION_ID`/`BEADS_SESSION_ID`). Multi-agent observability is in flux. | HIGH | Neutral/Context | [issues #3400/#3583](https://github.com/gastownhall/beads/issues/3400) |
| BD10 | **Version/release caution.** v1.0.5 shown as pre-release/gated with "do not upgrade" warning — migration `0043` can silently/unrecoverably break multi-machine `bd dolt` sync (issue #4259); v1.0.4 had a server-mode data-clobber regression (#3870). Operational instability on the Dolt-only line: orphaned `dolt sql-server` daemons, nil-pointer panics in `bd ready`/`bd list`, migration PK forks blocking `bd dolt pull` (#2573 "made beads unusable for me"). | MEDIUM-HIGH | Contradicts (production-ready assumption) | [releases](https://github.com/gastownhall/beads/releases) ; [issue #3870](https://github.com/gastownhall/beads/issues/3870) ; DoltHub blog 2026-05-29 |
| BD11 | **Production readiness:** usable but fast-moving with sharp edges. FAQ: core stable, dogfooded, safe for dev/internal WITH backup/sync hygiene; NOT recommended as sole record for mission-critical without tested backup/restore. **Mandatory: version-pin + an abstraction seam + `bd doctor`/backup/push-pull smoke tests in adoption gates.** | HIGH | Contradicts (drop-in assumption) | [FAQ.md](https://github.com/gastownhall/beads/blob/main/docs/FAQ.md) ; [issue #2938](https://github.com/gastownhall/beads/issues/2938) |
| BD12 | NO multi-tenancy / RBAC at the Beads layer. "Multi-writer" (Dolt server mode) is concurrency, not tenancy — one shared un-permissioned graph per Dolt DB. Tenant isolation must be imposed ABOVE Beads (separate Dolt DBs / issue-prefixes per tenant + gating in the orchestration layer). First-party MCP server maturity UNVERIFIED — the `--json` CLI is the most stable agent interface. | HIGH | Contradicts (governance) | [Beads repo](https://github.com/gastownhall/beads); [DOLT.md](https://github.com/gastownhall/beads/blob/main/docs/DOLT.md); [JSON_SCHEMA.md](https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md); enrichment `research-deep.md` |

> **Version discrepancy note (for runtime verification):** web-03 reports the current line at **v1.0.5** (with the "do not upgrade" gating); the older enrichment seed (fetched same day) recorded **v1.0.4** as latest (2026-05-09). The seed also flags a separate "Beads v0.60.0" Gas Town product-line version track. **Confirm the exact current release and its safety gating against the live releases page at use time before pinning.**

### 5.4 MCP and Multi-Tenant Governance

This area answers a structural question: can a Mastra + Backlog.md + Beads stack serve as a company-wide, multi-tenant SuperClaude replacement on its own?

#### 5.4.1 MCP Is a Protocol, Not a Governance Platform

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| GV1 | MCP is a deliberately narrow host/client/server context-exchange protocol. It explicitly does NOT dictate how AI apps use LLMs, manage context, or govern access. | HIGH | Contradicts (seed "MCP as governance" assumption) | [modelcontextprotocol.io/architecture](https://modelcontextprotocol.io/docs/concepts/architecture) |
| GV2 | MCP authorization is OPTIONAL but strongly recommended for enterprise / audit / consent / rate-limiting / per-user tracking. Remote-server auth is OAuth 2.1-based (Protected Resource Metadata, resource indicators, audience binding, token validation). | HIGH | Extends (requirement) | [authorization tutorial](https://modelcontextprotocol.io/docs/tutorials/security/authorization) ; [spec/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) |
| GV3 | **Token passthrough explicitly forbidden** — breaks accountability/audit, bypasses rate limits, enables exfiltration. Servers must validate tokens were issued for them. Downstream services need separate tokens + attribution metadata, not forwarded credentials. | HIGH | Extends (requirement) | [security best practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) |
| GV4 | Official MCP guidance flags multi-tenant/realm mix-ups, generic audience/resource indicators, session-ID-as-auth misuse, broad wildcard scopes. Guidance: pin to single issuer/tenant unless explicitly multi-tenant; minimize scopes (no `files:*`/`db:*`/`admin:*`); incremental elevation via `WWW-Authenticate`. | HIGH | Extends (requirement) | [authorization tutorial](https://modelcontextprotocol.io/docs/tutorials/security/authorization) ; [security best practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) |

#### 5.4.2 The Missing Governance Layer

| # | Finding | Rating | Relationship | Source |
|---|---------|--------|--------------|--------|
| GV5 | Enterprise governance is MCP's missing layer: identity, policy, visibility, audit, tool catalog, change control. Analogous to early REST needing API-management. Record caller identity/session, tool name/version/schema, inputs, target, outcome, policy decision, approvals. | MEDIUM | Extends | [tray.ai](https://tray.ai/blog/mcp-security-governance-enterprise) ; [scalekit](https://www.scalekit.com/blog/enterprise-mcp-how-identity-sso-and-scoped-auth-actually-work) |
| GV6 | **Multi-tenant agents need FIVE separate identities: trigger, execution, authorization, tenant, attribution.** Access-control bugs surface silently when execution and tenant identities are conflated. Config-driven RBAC; no inference from user messages. | MEDIUM (very high relevance) | Supports (SuperClaude ownership/attribution semantics) | [scalekit multi-tenant](https://www.scalekit.com/blog/access-control-multi-tenant-ai-agents) |
| GV7 | An AI control plane is broader than an LLM gateway (model routing/rate limits) or an MCP gateway (tool-calling paths) — it unifies connection, identity, policy, observability across all agents/systems. | MEDIUM | Extends | [speakeasy](https://www.speakeasy.com/resources/ai-control-plane) |
| GV8 | Cost attribution / FinOps is NOT native to MCP — requires host/gateway/control-plane metering (model tokens + tool calls + retries + workflow runs by tenant/team/user/agent/task). | MEDIUM-HIGH | Extends | [finops.org](https://www.finops.org/wg/model-context-protocol-mcp-ai-for-finops-use-case) |
| GV9 | CSA/minimum maturity: all MCP connections authenticated; remote uses OAuth 2.1 + PKCE; maintain server inventory (name/version/location/owner); least-privilege service accounts; basic audit logging of all tool invocations. Curated approved tool catalog with versioned/reviewed contracts. | MEDIUM-HIGH | Extends | [CSA agentic MCP](https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1) ; [tray.ai](https://tray.ai/blog/mcp-security-governance-enterprise) |

> **SEED CORRECTION / KEY CONCLUSION (MCP is not a governance platform).** Task rule 3 calls out: *"MCP is not a governance platform."* Confirmed strongly by official MCP docs (GV1) and enterprise guidance (GV5-GV9). **Net structural finding:** Mastra (runtime/workflow/observability/MCP primitives, EE-gated RBAC), Backlog.md (single-tenant markdown store), and Beads (un-permissioned shared graph per Dolt DB) together provide an orchestration/task SUBSTRATE — **none of them, alone or combined, is a complete multi-tenant governance control plane.** A company-wide deployment requires an ADDITIONAL governance layer for: tenant isolation; the five-identity attribution model (GV6); per-invocation audit; cost attribution; rate/budget limits; tool catalog + change control; approval gates; cross-app authorization (downstream tokens, no passthrough). This directly supports preserving SuperClaude's existing target-ownership/attribution semantics rather than compressing them into a single "agent identity."

#### 5.4.3 Component-Level Governance Reality

| Component | Governance role | What it does NOT provide |
|-----------|-----------------|--------------------------|
| **Mastra** | Runtime, workflow, HITL suspend/resume, MCP client+server, OTel observability, EE RBAC/SSO/FGA (paid) | Complete tenant governance, policy/budget/approval/catalog, cost attribution; Apache core = SimpleAuth only |
| **Backlog.md** | Repo-local markdown task/spec/decision records | Cross-tenant auth, enterprise audit, rate limiting, cost attribution, remote/HTTP transport |
| **Beads** | Dolt-backed dependency graph, ready-work scheduler, agent memory, gates, audit trail | Cross-tenant IAM, policy enforcement, MCP server inventory, cost attribution; one shared graph per DB |
| **MCP (protocol)** | Context/tool/resource exchange; optional OAuth 2.1 auth | Identity, policy, visibility, catalog, audit, rate limits, cost — all left to implementers |

### 5.5 External Research Summary

**Capability verdict.** The fresh external research supports the *technical feasibility* of a Mastra + Backlog.md + Beads orchestration substrate: Mastra supplies durable workflows (a direct MDTM-checkpoint analog) plus the `AcpAgent` subprocess seam that structurally replaces `ClaudeProcess`/stream-json; Backlog.md supplies a MIT-licensed markdown task-of-record whose schema maps onto MDTM phase items; Beads supplies a dependency-aware ready-work graph with gates and agent memory. **The blockers are not capability gaps but governance, licensing, parity, and maturity gaps.**

**Four seed corrections the fresh research forces (per task rule 3):**

| Corrected claim | Stack-D seed framing | Verified current reality |
|-----------------|----------------------|--------------------------|
| Beads storage | "embedded SQLite or Dolt server-mode"; "`.beads/` SQLite + JSONL" | **Dolt-first ONLY**; classic SQLite+JSONL removed; JSONL is export/interop only; drive `bd --json`, never read JSONL. |
| Mastra RBAC/auth | feasible OSS multi-tenant platform | **Production RBAC/SSO/FGA is Enterprise-licensed** (paid `ee/` commercial agreement); OSS path = SimpleAuth + DIY tenant scoping. |
| Backlog.md MCP / BACK-407 | "BACK-407-aligned, spec-complete" MCP server | **MVP stdio surface**; BACK-407 specifically **UNVERIFIED** (BACK-408 found); decisions CLI-only in MVP; `additionalProperties: false` rejects arbitrary metadata. Probe live before relying on it. |
| Backlog.md ↔ Beads | "shared repo metadata references" integration | **Immature** — open request #588; maintainer recommends narrow import/export sync first, not a broad integration surface. |

**Fifth structural correction:** **MCP is not a governance platform.** A company-wide multi-tenant SuperClaude port needs an additional governance/control-plane layer (tenant isolation, five-identity attribution, audit, cost attribution, rate/budget, tool catalog, approvals) above all three components.

**Authority reminder (task rule 4).** Everything above is EXTERNAL context. Where these findings touch the actual SuperClaude/IronClaude code (the `ClaudeProcess` seam, MDTM tasklist/rerun semantics, hook/freshness/verify-sync/`.claude`-source-of-truth discipline, fork-PR-target enforcement, the ~65K-LOC roadmap/pipeline domain logic), the verified-code findings in Sections 1-4 are authoritative. The external research adds options and risk framing; it does NOT establish parity, and notably does NOT prove Claude Code hook/permission parity, workflow-rerun/idempotency parity, or production stability of Beads/Mastra-EE for this use case. Those remain hands-on-validation items.

**Net recommendation posture (external view, not a decision):** treat the stack as a *substrate*, scope a focused Mastra ACP + durable-workflow spike, version-pin Beads behind an abstraction seam, drive Backlog.md/Beads via CLI/`--json` (not file reads), and budget for either Mastra EE or a DIY governance/control-plane layer before any multi-tenant rollout. "Do not port / keep the Python harness" remains a live, defensible option for the heavy domain logic.

---

## 6. Options Analysis

**Evidence convention:** Codebase claims cite `file:line` within the research directory (abbreviated as `RES/<file>:<line>`). External claims cite `web-0N` agent files (which themselves carry Tavily/Context7 source URLs) or the source URL directly. Claims that remain `[UNVERIFIED]` are flagged inline and are NOT presented as fact.

**Effort/Risk legend.** Effort bands (complexity, not story points): XS = days; S = 1-2 weeks; M = ~1 month; L = 1-3 months; XL = 3+ months / multi-quarter. Risk = likelihood × impact of the option failing to reach parity or producing drift/security exposure. Deferral ("do not port now") is a genuine, live option — a port is NOT assumed worthwhile.

### 6.0 Scoping facts that constrain every option

These verified facts shape all four options and are referenced repeatedly below:

| # | Fact | Evidence |
|---|---|---|
| F1 | The orchestration↔runtime coupling is a single seam: `ClaudeProcess` builds `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`. | `RES/01-pipeline-core-contracts.md:80-91`; `RES/08-gap-fill-feasibility-enrichment.md:39,114` [CODE-VERIFIED] |
| F2 | Roadmap, tasklist-validate, and cli-portify/prd/cleanup-audit already share a generic `execute_pipeline()` + injected `StepRunner` protocol; the runner is the swap point. | `RES/01:36-53`; `RES/02-roadmap-tasklist-pipelines.md:38-39,54-60`; `RES/04-cli-portify-prd-cleanup-audit-eval.md:67,74` [CODE-VERIFIED] |
| F3 | Gate logic (`gate_passed`, tiers EXEMPT/LIGHT/STANDARD/STRICT), `Step`/`GateCriteria`/`StepResult` models, deliverable decomposition, and diagnostic chain are pure Python with no Claude imports — runtime-agnostic. | `RES/01:55-72,119-152,196-209` [CODE-VERIFIED] |
| F4 | Sprint does NOT use the generic executor for its main loop; it runs a custom phase/task loop with two divergent paths (A: per-task subprocess; B: freeform + `OutputMonitor`/tmux/watchdogs), file-based result sentinels, checkpoints, `TurnLedger`, summarizer/retrospective. ~8,568 LOC across 19 files; `executor.py` alone is 2,148 lines. | `RES/03-sprint-execution-runtime.md:10,67-71,90-95,139-153` [CODE-VERIFIED] |
| F5 | Roadmap is the largest single subsystem: `executor.py` 3,702 lines + `gates.py` 1,441 lines; 12-step wired pipeline (extract→generate×2→diff→debate→score→merge→anti-instinct→test-strategy→spec-fidelity→wiring→deviation→remediate). | `RES/02:12,14,88-90` [CODE-VERIFIED] |
| F6 | Reusable knowledge corpus: 42 commands, 39 agents, 24 skill packages (~31,820 lines incl. refs), 12 core files, MDTM templates, hooks, MCP configs. Markdown/YAML, runtime-agnostic content but Claude-Code-coupled tool vocabulary (`Skill`, `Task`, `TeamCreate`). | `RES/05-skills-agents-harness-reuse.md:159-172` [CODE-VERIFIED] |
| F7 | An in-repo portification pattern already exists (`/sc:cli-portify` + `sc-cli-portify-protocol`): inventory→step graph→gates→executor spec. Its own history is a cautionary precedent — early code-gen/spec drift caused failures; contract-first planning became the safer pattern. | `RES/05:136-141`; `RES/06-docs-and-existing-feasibility-artifacts.md:217` [CODE-VERIFIED] |
| F8 | Multi-tenant auth/RBAC/FGA/audit/SSO/on-prem are Enterprise-licensed in Mastra (`@mastra/core/auth/ee`, Studio Auth, Agent Builder); without auth, Studio and API routes are public. | `web-01:51-56,78-82` [tavily/context7] |
| F9 | Backlog.md and Beads overlap as task stores AND their mutual integration is immature (Backlog.md issue #588: maintainer says "narrower integration decision before tasking"). Beads is Dolt-first (not SQLite/JSONL as seed-brief assumed); embedded mode is single-writer; server mode needed for multi-agent. Beads v1.0.5 carried a "do not upgrade" sync-corruption warning. | `web-02:93-98`; `web-03:54-70,107-128` [tavily] |
| F10 | None of Mastra+Backlog.md+Beads provides a tenant-aware governance/control plane (identity, policy, tool catalog, audit, cost attribution); MCP itself is explicitly NOT a governance layer. A separate control-plane service is required for company-wide multi-tenant use. | `web-04:93-128,144-153` [tavily] |
| F11 | Current scoped models (`PipelineConfig`, `SprintConfig`, `TaskResult`, `MonitorState`, `TurnLedger`) carry model/permission/budget fields but NO tenant/actor/audit identity fields. | `RES/07-target-data-model-and-ownership.md:102,197`; `RES/11-gap-fill-unverified-inputs-classification.md:115` [CODE-VERIFIED scoped; repo-wide UNVERIFIED] |

### 6.1 Option A — Hybrid adapter-first

**Description.** Mastra orchestrates workflows + traces and owns the durable run state; existing Python CLIs continue to execute via adapters (MCP/subprocess wrappers behind the `StepRunner` seam, F2); Backlog.md owns markdown tasks/specs/decisions; Beads owns the dependency graph + agent memory. The `ClaudeProcess` seam (F1) is wrapped, not replaced, in phase 1.

| Dimension | Assessment |
|---|---|
| **Effort** | **M-L.** Adapter layer + Mastra workflow shells + Backlog/Beads importers; reuses Python execution wholesale. Roadmap/tasklist/cli-portify wrap cleanly via F2; sprint needs a supervisory wrapper only (F4), not a rewrite. |
| **Risk** | **Low-Med.** Python remains the execution oracle (`RES/07:182`), so behavior parity is preserved by construction. Main risks: ownership drift between Backlog.md/Beads (F9), and adapter-state persistence outside transient Python objects (`RES/04:67`). |
| **Reuse of existing code** | **Highest.** All gate logic, models, executor semantics, sprint runtime, roadmap pipeline reused as-is (F2, F3, F4, F5). Knowledge corpus (F6) consumed as instruction packs. |
| **Files/systems affected** | New: Mastra workflow defs, `StepRunner`→Mastra adapter, Backlog.md importer, Beads graph sync, control-plane stub. Unchanged: `cli/pipeline/*`, `cli/sprint/*`, `cli/roadmap/*` (wrapped, not edited). |
| **Pros** | Preserves verified contracts; lowest parity risk; incremental/strangler-fig; lets the Backlog-vs-Beads and native-rewrite decisions be deferred until adapters prove the mapping (`RES/06:220`); can drive non-Claude models later via Mastra agents without touching the Python core. |
| **Cons** | Two runtimes to operate (Python + TypeScript/Mastra); does NOT by itself deliver multi-tenancy (still needs F8 EE + F10 control plane); Backlog/Beads overlap unresolved if both adopted at once; the `claude` CLI single-model limit persists for wrapped paths until the seam is actually replaced. |

### 6.2 Option B — Native Mastra reimplementation

**Description.** Translate pipeline core / roadmap / tasklist / sprint / PRD / audit into TypeScript Mastra workflows + agents. Replace `ClaudeProcess` (F1) with Mastra agent/Workspace execution; reimplement gates, models, monitors, checkpoints natively.

| Dimension | Assessment |
|---|---|
| **Effort** | **XL.** Must re-home: roadmap (5.1K LOC, 12-step pipeline, F5), sprint (8.5K LOC, dual paths, monitors, tmux, watchdogs, checkpoints, F4), pipeline core, plus port ~31.8K lines of knowledge corpus tool vocabulary (F6). cli-portify history (F7) shows code-gen ports drift and fail without contract-first discipline. |
| **Risk** | **High.** Sprint is the hardest stress test — "Any Mastra port that only models phases and tasks will miss the real complexity: process lifecycle, output files, result sentinels, monitors, watchdogs, and tmux IPC" (`RES/03:133`). Mastra long-running subprocess-supervision parity is `[UNVERIFIED]` (`RES/03:240`; `web-01:86-88`). `@mastra/temporal` durable runner is experimental (`web-01:18,87`). Many subtle behaviors (compressed-sidecar gate target, warning-only trailing gates, permissive frontmatter regex) must be re-tested (`RES/01:213-220`). |
| **Reuse of existing code** | **Low for runtime** (rewritten in TS), **Medium for knowledge** (markdown corpus translatable as instructions, F6). Pure-Python gate logic (F3) becomes a TS re-implementation, not a reuse. |
| **Files/systems affected** | Effectively the entire `src/superclaude/cli/` tree re-authored in TypeScript + every skill/agent re-homed to Mastra agent format. |
| **Pros** | Single runtime; native Mastra durability/observability/Studio; clean multi-model support; removes the `claude`-CLI single-model limit (seed-brief line 33); best long-term maintainability IF parity is achieved. |
| **Cons** | Largest effort and highest parity risk; Python→TS boundary means losing pure-Python reuse (F3); loses Claude-Code-native hooks/`/sc:*` dispatch/permission modes/freshness enforcement, all of which must be rebuilt as Mastra middleware (`RES/05:88-91`, `web-01:88`); cli-portify drift precedent (F7) warns against big-bang code-gen; still needs F8 EE + F10 control plane on top. |

### 6.3 Option C — Preserve Python CLI, add Backlog/Beads only (no Mastra runtime initially)

**Description.** Keep the Python CLI as the orchestration runtime. Add Backlog.md as the markdown work-of-record and Beads as the dependency graph + memory, via importers/sync adapters. No Mastra workflow runtime in phase 1.

| Dimension | Assessment |
|---|---|
| **Effort** | **S-M.** Two importer/sync adapters + round-trip parser-compatibility tests (`RES/07:125,138`). No runtime rewrite. Smallest of the build options. |
| **Risk** | **Med.** Backlog/Beads overlap and immature mutual integration (F9) is the central risk; Beads Dolt churn / v1.0.5 sync warning (F9) requires version pinning + backup gates (`web-03:135`). Ownership drift if both own status (`RES/07:107,193`). |
| **Reuse of existing code** | **Highest** (Python untouched, like Option A) but with **no new orchestration capability** — only task/graph state externalized. |
| **Files/systems affected** | New: Backlog.md importer, Beads graph sync, stable-ID preservation layer (`RES/07:100,109`). Unchanged: all of `cli/`. |
| **Pros** | Lowest-cost way to test the Backlog/Beads mapping and the task-of-record decision before committing to Mastra; preserves all current behavior; directly answerable by round-trip tests against `discover_phases()`/`parse_tasklist_file()` (`RES/07:125`). |
| **Cons** | Delivers neither multi-tenancy (F8/F10) nor multi-model orchestration (the strategic drivers, seed-brief lines 40-41); Mastra still required later for workflow/trace/governance-telemetry; risks investing in a Backlog/Beads schema that a later Mastra layer reshapes; does not address the `claude`-CLI single-runtime limit at all. |

### 6.4 Option D — Defer / not recommended now

**Description.** Do not port now. Keep the Python+Claude-Code stack. Optionally fund a narrow, time-boxed validation spike (Mastra durable-workflow + Workspace-subprocess safety; Backlog↔Beads single-workflow sync) to retire the `[UNVERIFIED]` external assumptions before any build decision.

| Dimension | Assessment |
|---|---|
| **Effort** | **XS-S.** Zero for pure defer; S for a time-boxed spike (`web-01:100-104,110`). |
| **Risk** | **Low (execution) / strategic.** No parity/migration risk. Risk is opportunity cost: multi-tenant/multi-model goals remain unmet, and target-stack churn (Beads v1.x sharp edges, F9; Mastra EE licensing, F8) keeps shifting. |
| **Reuse of existing code** | **Full** — nothing changes. |
| **Files/systems affected** | None (defer) or a throwaway spike workspace. |
| **Pros** | Honest response to the large `[UNVERIFIED]` external surface (`gaps-and-questions.md` RG-I1/RG-I2; F-facts above); avoids committing to immature Backlog↔Beads integration (F9) and EE licensing (F8) prematurely; a spike retires the highest-uncertainty assumptions cheaply (Mastra subprocess-supervision parity `RES/03:240`; Beads multi-writer/Dolt behavior `web-03:135`). |
| **Cons** | Strategic drivers (company-wide multi-tenant, multi-tool orchestration) stay unaddressed; `claude`-CLI single-model limit persists; defers rather than answers the go/no-go; if the company need is urgent, deferral is a cost. |

### 6.5 Options Comparison

| Criterion | A — Hybrid adapter-first | B — Native Mastra rewrite | C — Backlog/Beads only | D — Defer |
|---|---|---|---|---|
| **Effort** | M-L | XL | S-M | XS-S |
| **Risk** | Low-Med | High | Med | Low (strategic only) |
| **Maintainability** | Med (two runtimes) | High long-term *if* parity reached; High-risk to reach | Med (Python + 2 stores) | High (status quo, known) |
| **Integration complexity** | High (Mastra + Backlog + Beads + adapters) | Very High (full re-home + control plane) | Med (2 stores, no Mastra) | None / Low (spike only) |
| **Reuse potential** | Highest (F2-F6 as-is) | Low runtime / Med knowledge | Highest (Python untouched) | Full |
| **Multi-tenant readiness** | Partial — needs F8 EE + F10 control plane added | Partial — same F8/F10 still required | None in phase 1 | None |

**Cross-cutting note for all build options (A/B/C):** multi-tenancy is NOT delivered by the three named components. It requires (a) Mastra Enterprise licensing for production RBAC/SSO/audit/FGA/on-prem (F8, `web-01:51-56`) and (b) a separate governance/control-plane layer for tenant isolation, identity separation, tool catalog, audit, and cost attribution (F10, `web-04:125-128`). Current models also lack tenant/actor identity fields (F11). This is an additive requirement on top of whichever build option is chosen.

---

## 7. Recommendation

### 7.1 Feasibility verdict

| Field | Value |
|---|---|
| **Verdict** | **Conditionally Recommended** |
| **Recommended approach** | **Option D → Option A** — fund a time-boxed validation spike first (D), then proceed with **Hybrid adapter-first (A)** if and only if the spike clears its exit gates. Do NOT start with Option B. |
| **Confidence band** | **Medium (≈70%)** that Hybrid adapter-first is technically feasible and the right first build posture; **Low-Medium (≈55%)** that a *full company-wide multi-tenant* layer is deliverable on Mastra+Backlog+Beads alone without significant added Enterprise + control-plane investment. |

**Why "Conditionally" and not "Recommended":** the core orchestration port is technically feasible (the seam is clean — F1, F2, F3; the existing `sc-cli-portify-protocol` proves the method — F7). But the *strategic* goal (multi-tenant company orchestration) depends on conditions that are currently `[UNVERIFIED]` or licensing/maturity-gated: Mastra long-running subprocess-supervision parity (`RES/03:240`, `web-01:86-88`), Mastra EE licensing for production RBAC/SSO/audit (F8), immature Backlog↔Beads integration (F9), and the absence of any control-plane/tenant-identity layer in the three components (F10, F11). The verdict is therefore gated on a spike, not an unconditional go.

**Why "Recommended" rather than "Not Recommended":** the no-go case is not supported — the runtime coupling is a single, already-abstracted seam (F1/F2), the gate/model/diagnostic logic is runtime-agnostic Python (F3), and the knowledge corpus is portable markdown (F6). Nothing in the research shows a structural blocker that makes a port impossible; the blockers are cost, parity-proof, and governance scope, which a phased hybrid path manages.

### 7.2 Rationale against the comparison

| Why A over B | Why A over C | Why A over D-as-endpoint |
|---|---|---|
| B is XL effort + High risk; sprint subprocess/monitor/tmux/checkpoint complexity (F4) plus `[UNVERIFIED]` Mastra supervision parity (`RES/03:240`) makes a big-bang rewrite the worst risk/reward. The cli-portify drift precedent (F7) is a direct in-house warning. | C delivers neither strategic driver (multi-tenant, multi-model). It is a useful *sub-step inside* A (externalize task-of-record), not a competing endpoint. A subsumes C's work and adds the workflow/trace layer the governance plane needs. | D alone leaves the strategic drivers unmet. D is the right *first* move (retire `[UNVERIFIED]` risk cheaply), but as a permanent endpoint it forfeits the company-wide goal. The recommendation is D-then-A, not D forever. |

A also aligns with the independently-reached framing in prior research: keep Python as execution oracle, replace the seam in a narrow runner first, decide task-of-record after a dependency-graph behavior test (`RES/03:216`, `RES/06:220`, `RES/07:182`).

### 7.3 Spike exit gates (the conditions on "Conditionally")

Proceed from D to A only when ALL of these pass (each retires a named risk):

| Gate | Retires | Evidence target |
|---|---|---|
| SG1 — Mastra durably supervises a long-running subprocess (suspend/resume, restart, partial rerun, timeout, kill-escalation) at parity with `ClaudeProcess`/watchdogs. | `[UNVERIFIED]` Mastra supervision (`RES/03:240`, `web-01:86-88`) | Working spike, not docs. Workspace `executeCommand` safety validated (`web-01:101`). |
| SG2 — One round-trip: import a real `tasklist-index.md`+`phase-N` bundle into Backlog.md+Beads and export back so `discover_phases()`/`parse_tasklist_file()` succeed with matching task counts and dependencies. | Backlog/Beads schema fit `[UNVERIFIED]` (`RES/07:191-192`) | Round-trip test (`RES/07:125,138`). |
| SG3 — Beads server-mode multi-writer + Dolt sync survives a pinned version with backup/restore smoke tests; no v1.0.5-class corruption. | Beads churn/Dolt risk (F9, `web-03:135`) | Version-pinned spike with `bd doctor` + push/pull tests. |
| SG4 — A documented multi-tenant cost/identity decision: which Mastra license tier, and what the separate control-plane scope is. | F8 licensing + F10 control plane | Written decision, not code. |

> Note: the spike exit gates SG1–SG4 above are *spike-level* gates and are distinct from the roadmap's phase go/no-go gates G0–G5 in Section 8. The cross-cutting Critical gaps from Section 4 map here as follows: G3-gap (subprocess/Claude-Code parity) → spike gate SG1; G4-gap (hook/safety parity) → spike gate SG1 plus the "Python/TS boundary" and "Governance" honesty statements (7.4) and Section 8 step 3.9; G6-gap (tenant state) and G7-gap (auth/RBAC/governance/cost) → spike gate SG4 plus the "Governance/control-plane" honesty statement (7.4) and Section 8 Phase 4.

### 7.4 Mandatory honesty statements

**Enterprise licensing.** Production multi-tenant RBAC, SSO, audit logs, FGA, and on-prem/VPC are Mastra **Enterprise-licensed**, not in the Apache-2.0 core (`web-01:51-56,89` [tavily/context7]). Without auth, Mastra Studio and API routes are public (`web-01:80`). A local/single-team port may avoid EE; a company-wide multi-tenant deployment most likely **requires Enterprise conversations and cost/lock-in acceptance**. This is a budget and procurement gate, not just an engineering one. Treat any "multi-tenant on Mastra OSS" assumption as false for production RBAC.

**Python/TS boundary.** The runtime-agnostic value (gates, models, deliverable decomposition, diagnostics — F3) is **pure Python**. Option A keeps it; Option B forces a TypeScript re-implementation, converting reuse into rewrite-and-re-test (`RES/01:213-220`). The boundary is the single biggest reason to prefer adapter-first: it lets the Python IP keep executing while only the *orchestration shell* moves to Mastra. Crossing the boundary wholesale (B) is where parity risk concentrates.

**Beads Dolt / version churn.** Current Beads is **Dolt-first**, contradicting the seed-brief's "SQLite or Dolt" framing (`web-03:54-59` [tavily]); `.beads/issues.jsonl` is export-only, not canonical sync. Embedded mode is single-writer; multi-agent **requires server mode** (`web-03:61-70`). v1.0.5 was gated "do not upgrade" over a sync-corruption migration (`web-03:20-25`). Beads is "fast-moving with sharp edges… safe for dev/internal with backup/sync hygiene" but risky as a sole record for mission-critical use (`web-03:105-107`). **Mandate version pinning, server mode for any multi-writer use, and tested backup/restore before adoption.**

**Backlog/Beads overlap — pick a primary work-of-record.** Both can represent tasks; their mutual integration is **immature** (Backlog.md maintainer asks for a "narrower integration decision before tasking," issue #588, `web-02:93-98` [tavily]). Dual status owners create silent drift (`RES/07:107,193`). **Recommended split:** **Backlog.md = primary human-readable work-of-record** (task/spec/decision prose, stable IDs); **Beads = dependency graph + agent memory + ready-queue + gates**, NOT a second prose owner. Status canonicality must be assigned to exactly one (recommend Backlog.md for human status, Beads mirrors normalized status for graph queries only) — `RES/07:95-110,106-109`.

**Governance/control-plane layer beyond the three components.** Mastra+Backlog.md+Beads is an orchestration/task substrate, **not** a complete enterprise platform. MCP is explicitly not a governance layer (`web-04:12-13,119` [tavily]). Company-wide multi-tenant use requires an **additional control-plane service**: tenant registry, separated trigger/execution/authorization/tenant/attribution identities (`web-04:66-71`), RBAC/ABAC policy, tool/skill catalog + change control, per-invocation audit log, and cost attribution/budget metering (`web-04:125-128,144-153`). Current SuperClaude models carry no tenant/actor identity (F11). **This layer is not optional for the strategic goal and is not provided by any of the three components.**

### 7.5 One-line bottom line

A port is **feasible and worth a gated start**, but only as **hybrid adapter-first after a validation spike** — not as a native rewrite, not as a Backlog/Beads-only half-measure, and not as a "multi-tenant on the three components alone" assumption. If the company need is not yet urgent or the spike gates cannot be funded, **deferral (D) is a legitimate and honest choice**, not a failure.

---

## 8. Implementation Plan

**Recommended approach:** **Option D → Option A**. Phases 0–2 are the time-boxed validation spike that must retire the SG1–SG4 uncertainties from Section 7.3 before the work is treated as a committed Hybrid adapter-first program. If those spike gates fail, stop at Option D (defer / do not port now). If they pass, continue into Option A, corroborated by the data-model evidence in `07-target-data-model-and-ownership.md:173-184` ("Hybrid adapter-first is favored by data-model risk… native Mastra rewrite is higher-risk because it must replace subprocess, parser, telemetry, gates, and artifact ownership at once").

### 8.0 Reading Guide and Ground Rules

This section is a **phased validation-spike and strangler roadmap**, not a code-ready implementation spec. Several prerequisite decisions remain open (primary work-of-record, Mastra Enterprise licensing, governance/control-plane ownership); steps that depend on those decisions are explicitly marked **[DECISION-GATED]** and must not be treated as buildable until the gating decision is made.

**Authority order:**

1. **Codebase is source of truth.** Current SuperClaude CLI contracts (parser shapes, gate semantics, step registries, IDs) are verified in research files 01–11 and govern. They are preserved verbatim across adapters.
2. **External capabilities** (Mastra/Backlog.md/Beads/MCP governance) come from `web-01`..`web-04` (dated 2026-06-02, `provider=tavily`). Every external capability the roadmap depends on is cited to its web source; capabilities flagged HIGH-risk in web research (e.g. Mastra workflow rerun/replay semantics, EE licensing) are surfaced as go/no-go criteria, never assumed.

**Evidence binding:** Steps cite `file:line` for codebase contracts and source URLs for external claims. Claims that remain `[UNVERIFIED]` in upstream research stay `[UNVERIFIED]` here.

**Phase overview:**

| # | Phase | One-line goal | Primary go/no-go |
|---|---|---|---|
| 0 | Spike discovery & decisions | Pin contracts, choose work-of-record, scope licensing | Decisions D1–D5 recorded |
| 1 | Spike adapter MVP (read-only) | Import current artifacts into Backlog.md + Beads, round-trip-safe | Parser round-trip parity passes (SG2/SG3 evidence) |
| 2 | Spike hybrid pilot | Wrap ONE real pipeline (`tasklist validate`) behind a Mastra workflow step | Pilot parity vs native CLI passes (SG1 evidence) |
| 3 | Committed parity port | Wrap `roadmap run` + sprint execution; reproduce gates/checkpoints/hooks | Artifact + gate parity suite passes |
| 4 | Multi-tenant hardening | Add governance/control-plane, tenant identity/audit/cost | EE + governance decisions resolved |
| 5 | Rollout | Progressive production rollout behind the control plane | Operational + recovery gates pass |

### 8.1 Phase 0 — Discovery and Foundational Decisions

**Goal:** Lock the contracts that must survive the port, and make the five decisions that gate every later phase, before any adapter or workflow code is written. No execution code in this phase; output is an inventory + a decision record.

**Dependencies:** None (entry phase). Consumes research files 01–11, `web-01`..`web-04`, `07-target-data-model-and-ownership.md`, `09-gap-fill-checkpoint-contract.md`.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 0.1 | Freeze the **stable-ID contract** as the cross-system reconciliation key | `sprint/config.py:374-377`; `07-...ownership.md:41,100` | IDs `TASK-*`, `R-###`, `T<PP>.<TT>`, `D-####`, `D-CP*` already appear in current files and parsers. Catalog every ID producer/consumer. Rule: adapters preserve IDs verbatim, never regenerate on import/export (`07-...:109`). |
| 0.2 | Inventory the **sprint parser compatibility contract** that any tasklist adapter must satisfy | `sprint/config.py:15-26,28-49,374-492`; `09-...:131-141` | Phase discovery names (`phase-N-tasklist.md` etc.), `### T<PP>.<TT> -- Title` heading regex, `**Dependencies:**`, `**Command:**`, `\| Classifier \|` table, `**Deliverables:**` description, `count_tasks_in_file` count. This is the round-trip acceptance surface for Phase 1. |
| 0.3 | Adopt the **canonical checkpoint contract** as the emit shape | `09-gap-fill-checkpoint-contract.md:127-154` | Numbered checkpoint task entries `### T<PP>.<NN> -- Checkpoint: ...`, one mid-phase per 5 tasks + one end-of-phase last task, each with a `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...` line. Do NOT emit legacy sibling `### Checkpoint:` headings. Record the known per-task `_verify_checkpoints()` gap (`executor.py:1259-1301`) as a Phase 3 risk. |
| 0.4 | **[DECISION D1 — work-of-record]** Choose primary owner: Backlog.md vs Beads | `web-02:115-118`; `web-03:140`; `07-...:181,193` | Recommended split (hypothesis, `[UNVERIFIED target]`): Backlog.md owns human prose/tasks/docs/decisions (`web-02:115`); Beads owns dependency DAG + ready-queue + claims + memory + gates (`web-03:140`). One canonical status owner — dual owners cause drift (`07-...:107,193`). Backlog.md↔Beads integration is **not mature** (`web-02:93-98`, request #588); pick a narrow import/export sync, not broad integration. |
| 0.5 | **[DECISION D2 — Mastra licensing track]** Decide OSS vs Enterprise track now | `web-01:51-57,78-83,89` | Apache-2.0 core covers workflows/steps/storage/observability/MCP; production RBAC/SSO/FGA/audit/on-prem are EE-gated (`@mastra/core/auth/ee`, `web-01:53`). Local/single-tenant pilot can run OSS; company-wide multi-tenant likely requires an EE conversation. This decision gates Phase 4, not Phases 1–3. |
| 0.6 | **[DECISION D3 — governance/control-plane]** Acknowledge that Mastra+Backlog+Beads is NOT a governance plane | `web-04:93-99,125-127,140` | None of the three provides tenant isolation, per-invocation audit, cost attribution, tool catalog, or policy enforcement. A separate control-plane layer is required before company-wide multi-tenant deployment. Scope it as a Phase 4 deliverable, not a Phase 1–3 dependency. |
| 0.7 | **[DECISION D4 — runtime substrate]** Pick the subprocess/exec seam for the hybrid wrapper | `web-01:30-35,88,91`; `pipeline/process.py:24-35` | Current seam is `claude --print --verbose --output-format ... ` over stdin (`07-...:36`). Candidate target is Mastra Workspace `WorkspaceSandbox.executeCommand()` (`@mastra/core@1.1.0`, `web-01:32`). **Does NOT prove Claude Code hook/permission parity** (`web-01:35,88`) — schedule a safety spike (Phase 2). Hybrid track keeps calling the existing Python CLI first. |
| 0.8 | **[DECISION D5 — Beads deployment mode + version pin]** | `web-03:61-67,68-74,19-25,135` | Embedded mode is single-writer ("database is locked"); multi-agent orchestration requires **server / shared-server mode** (`web-03:66,122`). Pin version and gate upgrades — v1.0.5 carries a sync/migration warning (issue #4259, `web-03:21`). Integrate via `bd ... --json` with envelope compatibility (`web-03:38,133`), never JSONL reads. |
| 0.9 | Produce a **Decision Record + Contract Inventory** artifact and an architecture diagram of the proposed ownership split | output: `discovery/decision-record.md`, `discovery/contract-inventory.md` | Ownership matrix from `07-...:93-102`. This artifact is the input gate to Phase 1. |

**Go/No-Go Gate G0 → Phase 1:** PROCEED only if D1 (work-of-record) and D4 (runtime seam for hybrid) are recorded, and the parser/checkpoint contracts (0.2, 0.3) are inventoried with citations. D2/D3/D5 may remain provisional (they gate Phase 4) but must be logged. NO-GO if work-of-record is unresolved — every adapter mapping depends on it (`07-...:181`).

### 8.2 Phase 1 — Adapter MVP (Read-Only, No Ownership Transfer)

**Goal:** Build **read-only importers** that ingest existing `.dev/tasks` and tasklist bundles into Backlog.md (prose) and Beads (dependency graph) **without mutating current files**, and prove the import is round-trip-safe against the sprint parser. This de-risks ID/graph/artifact mapping before any execution or ownership change (`07-...:179-180`).

**Dependencies:** G0 passed. D1 (work-of-record), D5 (Beads mode/version) recorded. Beads server-mode instance provisioned (`web-03:122`); Backlog.md initialized (`backlog init`, `--no-git` if required, `web-02:54`).

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 1.1 | Build a **tasklist-bundle → Backlog.md importer** | reads `tasklist-index.md` + `phase-N-tasklist.md`; writes via `backlog` CLI/MCP | Map per Contract 1 (`07-...:114-125`): phase H1 → milestone/list; `### T<PP>.<TT>` → task with ID as **external ID** (not display text); body sections → `description`/`implementationPlan`/`implementationNotes`; AC → acceptance criteria; `**Dependencies:**` → `dependencies` + retained body text. Mutate only through `task_create`/`task_edit` (`web-02:117`), never hand-edit markdown. |
| 1.2 | Respect Backlog.md schema limits; map non-native metadata explicitly | `web-02:27-38` | MCP task schemas use `additionalProperties:false` (`web-02:33-34`) — SuperClaude-specific fields (tier, classifier, risk, `R-*`/`D-*` IDs) cannot be arbitrary frontmatter. Map to supported fields (`labels`, `milestone`, `references`, `documentation`, `modifiedFiles`) or body sections (`web-02:118`). Use CLI for `decision create` — decisions are not in the current MCP MVP (`web-02:47-49`). |
| 1.3 | Build a **tasklist/Backlog → Beads graph mirror** | `bd create`, `bd dep add`, `bd update --json`; `web-03:27-31,133` | Per Contract 2 (`07-...:127-138`): root issue per tasklist bundle, phase parent issue/epic, one issue per `T<PP>.<TT>`, directed edges from `TaskEntry.dependencies`. Use typed deps (`blocks`, `parent-child`, `web-03:41`). Beads rejects cycles at write (`web-03:42`). Mirror checkpoint tasks as verification nodes, not implementation blockers unless they block the next phase (`07-...:135`). |
| 1.4 | Encode "work-done vs merged/validated" barriers as **Beads gates** | `bd gate`; `web-03:48-52` | Map SuperClaude validation/PR-merge phases to gate issues: `gh:pr` (PR merged), `gh:run` (CI), `human` (manual approval), `timer` (`web-03:49`). This is a direct fit for the certify/wiring/validation distinction in the current pipeline. |
| 1.5 | Make every importer **idempotent and additive** | importer code; `07-...:165` | Re-running an import must not duplicate Backlog rows or Beads edges (`07-...:165`). Key all upserts on stable IDs (0.1). Never silently rewrite human markdown if the Beads graph diverges — emit a **proposed graph-patch report** instead (`07-...:96,134`). |
| 1.6 | Build the **round-trip parity exporter + test** (acceptance gate) | exporter; `sprint/config.py` `discover_phases()`, `parse_tasklist_file()`, `count_tasks_in_file()` | Export Backlog/Beads state back to `tasklist-index.md` + `phase-N-tasklist.md` and assert: (a) `discover_phases()` finds every phase, (b) `parse_tasklist_file()` reads every task, (c) task counts equal `count_tasks_in_file()`, (d) exported dependency lists are identical to parser-extracted `TaskEntry.dependencies` unless a human-approved graph patch exists (`07-...:125,138,180`). |
| 1.7 | Seed a representative corpus mixing both checkpoint shapes | `.dev/releases/complete/cliEval/phase-1-tasklist.md:251` (numbered); `.dev/test-sprints/smoke-test/phase-1-tasklist.md:172` (legacy) | Import must normalize legacy sibling `### Checkpoint:` into numbered checkpoint tasks before re-export (`09-...:152`), proving the importer handles the real mixed corpus. |

**Go/No-Go Gate G1 → Phase 2:** PROCEED only if the round-trip parity test (1.6) passes on the mixed corpus (1.7) AND importers are proven idempotent (1.5). NO-GO if any task is dropped, any dependency edge diverges without an approved patch, or checkpoint normalization is lossy. This phase changes **no execution behavior** — current Python orchestration remains the oracle (`07-...:182`).

### 8.3 Phase 2 — Hybrid Pilot (Wrap ONE Real Pipeline)

**Goal:** Prove a Mastra workflow can drive a real SuperClaude pipeline end-to-end by **wrapping the existing CLI as a subprocess step** (hybrid, not native reimplementation), with one pipeline only. Validate durability, gate handling, and trace capture against the native CLI as oracle.

#### Pilot recommendation (smallest safe first slice)

**Wrap `superclaude tasklist validate` as the first Mastra-wrapped pipeline.** Rationale, evidence-bound:

- It is the **single smallest pipeline**: one LLM fidelity step with one strict gate, not a generator — `tasklist/executor.py:191-218` wires a single `tasklist-fidelity` step; `tasklist/executor.py:251-276` returns pass only when there are zero HIGH-severity deviations (`02-...:153-154,204-206`).
- It has a **clean, parseable pass/fail contract**: `high_severity_count` parsed from report frontmatter; missing/unparseable report = fail (`tasklist/executor.py:221-248`). That is a trivial Mastra scorer/gate to mirror.
- It is **read-only / non-destructive** — it validates roadmap→tasklist alignment and writes a report; it mutates no source (`tasklist/prompts.py:17-148`). Lowest blast radius for a first wrapped run.
- It reuses the **shared pipeline layer** (`tasklist/executor.py:23-25,259-263` → `execute_pipeline`), so lessons transfer directly to `roadmap run` in Phase 3.

Defer `roadmap run` to Phase 3: it carries parallel generate steps, convergence mode, compression sidecars, deviation registry, trailing gates, and post-run validation (`02-...:40,89-96`) — too much surface for a first slice.

**Dependencies:** G1 passed. D4 (runtime seam) recorded. Mastra OSS instance with composite storage (PostgreSQL/libSQL for snapshots; avoid in-memory, `web-01:103`). A Backlog.md/Beads-derived input or a native roadmap+tasklist input pair.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 2.1 | Define a Mastra workflow with **one step that shells out** to `superclaude tasklist validate` | `createWorkflow()`/`createStep()` (`web-01:23-28`); `WorkspaceSandbox.executeCommand()` (`web-01:30-35`) | Hybrid wrapper: the Mastra step invokes the existing CLI; SuperClaude stays the execution oracle (`07-...:150,182`). Capture stdout/stderr, exit code, and the written report path. |
| 2.2 | Mirror the CLI's gate as a **Mastra scorer/validator** | mirror of `tasklist/executor.py:221-248`; `web-01:46` (eval/scorer) | Parse `high_severity_count` from the report; map zero-HIGH → workflow PASS, else FAIL. Assert the Mastra verdict equals the native CLI exit code (`tasklist/commands.py:181-185`). |
| 2.3 | Run the **subprocess-safety spike** (gates D4 for later phases) | `web-01:88,91,101-102`; `eval/isolation.py:456-642` | Mastra Workspace exec does NOT replicate Claude Code hooks/permission/freshness/staging discipline (`web-01:35,88`). Reuse the eval harness isolation model — per-run HOME, scratch-root allowlist, containment guard (`eval/isolation.py:224-260,456-642`) — as the parity target for safe command execution. Record gaps; do not claim CLI parity (`web-01:101`). |
| 2.4 | Validate **durability: suspend/resume + failed-step restart** | `web-01:16-22,86` | Test Mastra `suspend()`/`resume()`, snapshot persistence across restart, and partial rerun. Rerun/replay/idempotency semantics are flagged HIGH-risk-unverified (`web-01:86`) — this step exists to verify them empirically, not assume them. Treat `@mastra/temporal` as experimental (`web-01:18,87`). |
| 2.5 | Capture **traces with SuperClaude IDs** as custom attributes | `web-01:44-49`; `07-...:149` | Attach `R-*`, `T<PP>.<TT>`, `D-*`, phase, tier, model, git branch/commit to every span (`07-...:149`; `web-01:105`). This is the join key between Mastra traces and Backlog.md/Beads records and the seed for cost attribution in Phase 4. |
| 2.6 | Reconcile the run result back into Backlog.md + Beads | Contract 4 (`07-...:154-165`) | On PASS: summarize execution-log entry in Backlog, close/check the Beads verification node. On FAIL: failure note + gate report + edge to a remediation issue. Reconciliation must be idempotent (`07-...:165`). |

**Validation/eval strategy for the pilot:** Run the SAME input through (a) native `superclaude tasklist validate` and (b) the Mastra-wrapped workflow; assert identical verdict, identical `high_severity_count`, and equivalent report content. Use the `eval/` harness pattern as the test substrate — capability preflight (`eval/commands.py:119-192`), ordered per-spec outcomes (`eval/orchestrator.py:164-299`), JSONL forensic logs and preserved-on-failure artifacts (`eval/runner.py:537-588,425-473`).

**Go/No-Go Gate G2 → Phase 3:** PROCEED only if (a) Mastra-wrapped verdict == native CLI verdict across the corpus, (b) suspend/resume + failed-step restart behave correctly (2.4), and (c) the subprocess-safety spike (2.3) produced an explicit parity/gap report. **NO-GO if Mastra rerun/recovery semantics cannot be demonstrated** — that is the load-bearing assumption for porting the stateful `roadmap`/`sprint` pipelines (`07-...:189`; `web-01:86`).

### 8.4 Phase 3 — Parity Port (Roadmap Run, Sprint Execution, Gates, Checkpoints, Hooks)

**Goal:** Extend the hybrid pattern to the **full orchestration surface**: wrap `superclaude roadmap run` and sprint execution behind Mastra workflows, reproduce the multi-step graph, gates, checkpoints, and Claude Code hooks as Mastra middleware/guards — while keeping the Python CLI as the execution oracle until parity is proven. Native reimplementation of any step happens **only after** that step passes a parity gate (`07-...:175,182`).

**Dependencies:** G2 passed. Mastra durable workflows validated (Phase 2). Beads server mode + gates live (Phase 1). This is the highest-risk phase — sprint Path A/B, isolation, and process supervision are flagged as the hardest port surface (`gaps-and-questions.md` RG-I7).

#### 3a. Roadmap run (rich, mostly stateless-per-step pipeline)

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 3.1 | Map the roadmap **step graph** to a Mastra workflow, one node per registry step | `roadmap/executor.py:2003-2204` (`02-...:89`) | Wired order: `extract` → parallel `generate-{a}`/`generate-{b}` → `diff` → `debate` → `score` → `merge` → `anti-instinct` → `test-strategy` → `spec-fidelity` → `wiring-verification` → `deviation-analysis` → `remediate`. Mastra parallel steps for the two generate agents (`web-01:23-26`). Generate the graph from the authoritative step list — do NOT maintain a parallel matrix (avoid the `cli_portify` resume-drift anti-pattern, `04-...:69,75`). |
| 3.2 | Reproduce **gates** as Mastra guards/scorers, preserving gate modes | `roadmap/gates.py`; `pipeline/models.py:69-79` (`07-...:35`) | Preserve `GateMode` blocking vs `TRAILING` semantics. `wiring-verification` uses `WIRING_GATE` + `GateMode.TRAILING` + deterministic `run_wiring_analysis` (`roadmap/executor.py:2175-2184,1011-1031`). **Preserve, do not normalize:** `CERTIFY_GATE` is **defined but not wired in production** (`gates.py:1324-1351`; `executor.py:1947-2208`; `02-...:146`) — the port must not silently "fix" this; flag it as an open parity question. |
| 3.3 | Port **convergence + remediation** state machine | `roadmap/executor.py:1804-1897`; `roadmap/remediate.py:177-288`; `convergence.py:144-255` (`02-...:111,174-175`) | Stateful via `deviation-registry.json`, `spec-deviations.*`, `remediation-tasklist.*`, `.roadmap-state.json` (`02-...:111`). Mastra owns run state only after durability proven (`07-...:108`); until then, these JSON/markdown sidecars remain source of truth. Preserve compression-sidecar behavior (`gaps-and-questions.md` RG-I6). |
| 3.4 | Wrap **post-run auto-validation** | `roadmap/executor.py:3409-3447`; `validate_executor.py:183-236` (`02-...:102,106`) | `roadmap run` auto-invokes validation, resolving inputs from `.roadmap-state.json` (`02-...:106`). Preserve release-dir resolution semantics (`sprint/config.py:236-272`, `07-...:82`). |

#### 3b. Sprint execution (hardest surface)

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 3.5 | Reproduce **Path A (per-task) vs Path B (freeform)** execution routing | `sprint/executor.py:1118-1133,1259-1301`; `process.py:170,187-195` (`09-...:30-32,56-58`) | Phases with numbered `### T<PP>.<TT>` headings route per-task (`executor.py:1259-1301`); freeform phases use the full-phase prompt (`process.py:170`). Adapter must emit numbered tasks so execution is deterministic per-task (`09-...:153`). |
| 3.6 | Wire **checkpoint verification** into the per-task path (closes the known gap) | `sprint/executor.py:1259-1301` vs `1512-1531`; `checkpoints.py:18-94` (`09-...:106-110`) | Per-task branch does NOT call `_verify_checkpoints()` (`09-...:121`). The port should verify checkpoints after task aggregation (or run `verify-checkpoints` after, `09-...:154`). `checkpoints.py` already accepts numbered + legacy headings (`09-...:48`). Mirror checkpoint reports as Backlog docs + Beads verification-node closure. |
| 3.7 | Map **sprint phases/tasks/checkpoints** to Beads graph + ready-queue scheduler | `bd ready --json`, `bd update --claim`; `web-03:28,133`; Contract 3 (`07-...:140-152`) | Use `bd ready --json` as scheduler input and `bd update <id> --claim --assignee <agent>` for atomic acquisition (`web-03:28,132`). Honor session attribution caveat — `--claim` session-loss bug is actively changing (`web-03:70`). One Mastra stage per phase; phase `Execution Mode` (`claude`/`python`/`skip`, `sprint/config.py:67-119`) selects the Mastra runner type. |
| 3.8 | Preserve **status/result/telemetry/budget models** as Mastra run metadata + summaries | `sprint/models.py` enums (`07-...:50-60`); `web-01:44-49` | Map `StepStatus`/`TaskStatus`/`GateOutcome`/`PhaseStatus`/`SprintOutcome` to Mastra run states; route high-volume telemetry (`MonitorState`, stdout/stderr) to Mastra traces/observability, NOT into Backlog/Beads bodies — only summaries there (`07-...:65,97,163`). |

#### 3c. Hooks → Mastra middleware/guards

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 3.9 | Reproduce **Claude Code hooks** as Mastra middleware/guards + governance pre-checks | `web-01:35,104`; `web-01:106` (MCP `requireToolApproval`) | Recreate UV-only Python rule, `.claude/` source-of-truth/staging discipline, fork-PR target, freshness pre-edit checks, safe command execution as explicit Mastra guards or pre-step validators (`web-01:104`). Hook portability is flagged `[UNVERIFIED]` (`gaps-and-questions.md` RG-I5) — verify each hook's trigger surface before claiming parity. Use `requireToolApproval` for human-in-the-loop tool gates (`web-01:60`). |
| 3.10 | Begin **selective native reimplementation** of deterministic steps only | per-step parity gate (3.x) | Deterministic Python steps (`run_wiring_analysis`, remediation generation, classification, audit primitives `04-...:255-258`) can be reimplemented natively in Mastra/TS once their step passes parity. LLM steps stay hybrid (call existing CLI) until explicitly re-validated. Never replace subprocess+parser+telemetry+gates+artifacts in one move (`07-...:173`). |

**Validation/eval strategy (parity suite):** This is the core acceptance machinery for Phase 3.

| Parity dimension | Method | Evidence anchor |
|---|---|---|
| Artifact parity | Diff Mastra-produced artifacts vs native CLI artifacts for the same input (roadmap outputs, tasklist bundle, checkpoint reports, return contracts). | `cli_portify/executor.py:283-372` return-contract; `09-...` checkpoint paths |
| Gate parity | Assert each gate's verdict + mode (blocking/trailing/deferred) matches native. | `roadmap/gates.py`; `pipeline/models.py:69-79` |
| Graph/order parity | Assert executed step order + dependency order equals native + Beads `bd ready` order. | `roadmap/executor.py:2003-2204`; `sprint/config.py` |
| Safe-execution parity | Reuse eval HOME isolation, scratch-root allowlist, JSONL forensics, retry-once, ordered outcome accounting. | `eval/isolation.py:456-642`; `eval/orchestrator.py:164-299`; `eval/runner.py:833-878`; `eval/retry.py:92-165` |
| Recovery parity | Test crash recovery / resume against native sprint recovery + manifest. | `sprint/executor.py:1702-1721`; `09-...:64-66` |

**Go/No-Go Gate G3 → Phase 4:** PROCEED only if the parity suite passes for `roadmap run` AND a representative sprint (artifact + gate + order + safe-execution + recovery parity), AND every hook is reproduced as a verified guard (3.9). NO-GO if any gate verdict, checkpoint enforcement, or recovery path diverges from native behavior, or if hook parity is unproven. Native step reimplementation (3.10) is allowed only for steps that individually passed parity.

### 8.5 Phase 4 — Multi-Tenant Hardening

**Goal:** Convert the single-tenant parity port into a company-wide multi-tenant orchestration layer. **This phase is gated on four explicit decisions/builds that Mastra + Backlog.md + Beads do NOT provide on their own.**

> **CRITICAL FLAGS (per task rule 4) — none of these can be skipped:**
>
> 1. **Mastra Enterprise licensing decision (D2).** Production RBAC, SSO, FGA, audit logs, on-prem/VPC, and Studio Auth/Agent Builder are EE-licensed (`@mastra/core/auth/ee`, `web-01:51-57,80-82,89`). OSS Mastra leaves Studio/API public without auth (`web-01:52`). Company-wide multi-tenant deployment **requires an Enterprise conversation** — this is a go/no-go business decision, not an engineering toggle.
> 2. **A separate governance/control-plane layer is required (per `web-04`).** Mastra+Backlog+Beads is an orchestration/task substrate, NOT a governance plane (`web-04:93-99,125-127,140`). The missing layer = tenant isolation, policy enforcement, tool catalog/change control, audit, cost attribution, approvals (`web-04:125,145`).
> 3. **Tenant-aware identity, audit, and cost attribution are net-new.** Current scoped models have NO tenant/actor fields — only a sprint-local `TurnLedger` budget (`07-...:102,197`; `web-04:127`). Multi-tenant agents need **separate trigger / execution / authorization / tenant / attribution identities** (`web-04:66-71`); conflating execution and tenant identity causes silent access-control bugs (`web-04:68`).
> 4. **A primary work-of-record decision between Backlog.md and Beads must be final (D1 from Phase 0).** Dual status owners create drift (`07-...:107,193`); confirm and freeze the canonical owner before scaling to many tenants/teams.

**Dependencies:** G3 passed. D2 (EE track) and D1 (work-of-record) **resolved, not provisional**. D3 (control-plane) scoped.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 4.1 | **[DECISION-GATED on D2]** Stand up Mastra auth + RBAC/FGA on the EE track (or document OSS limits) | `web-01:53,56,80-82` | If EE: configure `StaticRBACProvider`/`DEFAULT_ROLES`/`MastraFGAPermissions`, Studio Auth SSO, WorkOS FGA. If OSS-only: explicitly bound deployment to non-public/single-tenant and record the gap. Without auth, Agent Builder/Studio are open to anyone reachable (`web-01:80`). |
| 4.2 | **[DECISION-GATED on D3]** Build the governance/control-plane service | `web-04:145` | Tenant registry; user/team/agent identity mapping; RBAC/ABAC policy store; tool/skill catalog + ownership registry; MCP server inventory; approval policy engine; audit/event log; cost + rate/budget attribution; environment separation + rollout controls. This is a **separate service**, not a Mastra config. |
| 4.3 | Add an **MCP/AI gateway** for any remote/shared MCP surface | `web-04:27-35,42,49,146` | Enforce OAuth 2.1 for remote MCP (PRM, resource indicators, audience binding, token validation, `web-04:27`). **Forbid token passthrough** (`web-04:34`). Pin to single issuer/tenant; reject other-realm tokens; never tie auth to session ID (`web-04:42`). Tool-level allowlists, no wildcard scopes (`web-04:49`). |
| 4.4 | Map SuperClaude command/skill privileges to **granular scopes** | `web-04:52,147` | Avoid one broad `superclaude:*` permission. Map commands/skills/tools to read-only / code-edit / git-write / external-search / infra-change / destructive / admin; require progressive elevation + approval for higher-risk actions (`web-04:147`). Aligns with the existing per-skill ownership concept (`web-04:148`). |
| 4.5 | Implement **per-invocation audit records** | `web-04:149` | Every orchestration action: timestamp, tenant, user, agent/client, workflow/task ID, tool/skill name+version+schema, input classification, target system, result, policy decision, approval ID, cost, correlation ID. Feed Mastra observability into the governance plane; join traces with Backlog.md/Beads IDs (`web-04:151`; uses the 2.5 trace-attribute join key). |
| 4.6 | Implement **cost attribution + budget/rate enforcement** | `web-04:150`; `07-...:58,183` | Promote the sprint-local `TurnLedger` (`sprint/models.py:692-777`) to a first-class tenant/team/project/task/agent cost model (model tokens, tool calls, retries, evaluations, workflow runs) with budget alerts/limits (`web-04:150`; `07-...:183`). MCP/FinOps is outside MCP itself (`web-04:80-85`). |
| 4.7 | Promote **Beads to server/shared-server mode** for multi-tenant writers, with per-tenant prefixes | `web-03:66,82-85,122` | Server mode for concurrent writers (`web-03:66`); shared-server with unique per-project/tenant prefix + database name (`web-03:83`). Enforce backup/restore + push/pull smoke tests as adoption gates (`web-03:135`). Keep version pinned (D5). |
| 4.8 | Enforce **one canonical work-of-record** at scale and curate the tool catalog | `web-04:111-115,153`; `07-...:107` | Freeze D1. Do not expose raw MCP server/tool catalogs broadly — publish curated, versioned, reviewed workflow-tools aligned to SuperClaude commands/skills (`web-04:153,111-115`). Backlog.md and Beads each stay scoped; neither owns runtime authorization or tenant isolation (`web-04:152`). |

**Go/No-Go Gate G4 → Phase 5:** PROCEED only if (a) D1 + D2 are final, (b) the governance/control-plane (4.2) and MCP gateway (4.3) enforce tenant isolation + per-invocation audit + cost attribution on a two-tenant test, and (c) granular scopes + approval gates (4.4) are live. NO-GO if any tenant can read another tenant's tasks/traces/costs, if token passthrough is possible, or if EE-gated features are assumed without a licensing decision. **Do not deploy company-wide on Mastra+Backlog+Beads alone** (`web-04:140`).

### 8.6 Phase 5 — Rollout

**Goal:** Progressive production rollout of the multi-tenant orchestration layer behind the control plane, starting with the lowest-risk pipeline and tenant, with operational + recovery gates at each expansion.

**Dependencies:** G4 passed. Governance plane, MCP gateway, audit, and cost attribution live. Beads server mode + backup/restore validated. EE licensing (if chosen) procured.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 5.1 | Roll out the **pilot pipeline (`tasklist validate`) to a single internal tenant** first | Phase 2 workflow + Phase 4 governance | Lowest blast radius, read-only, proven in Phase 2. Validate audit/cost/scope enforcement end-to-end on a real tenant before adding stateful pipelines. |
| 5.2 | Expand to `roadmap run`, then sprint execution, **one pipeline at a time** | Phase 3 workflows | Gate each expansion on its own parity suite (G3 dimensions) re-run in the production-config environment. Honor merge-freeze / release-cut operational constraints. |
| 5.3 | Add tenants progressively with **isolation re-validation per onboarding** | governance plane (4.2); Beads prefixes (4.7) | Re-run the two-tenant isolation test (G4) at each new tenant. Verify per-tenant cost attribution and budget limits actually fire. |
| 5.4 | Operationalize **recovery + backup hygiene** | `web-03:135`; `sprint/executor.py:1702-1721` | Scheduled `bd backup`/`bd dolt push`, tested restore, sprint manifest + crash-recovery drills. Beads is safe for internal use only with tested backup/restore (`web-03:126`). |
| 5.5 | Keep a **native-vs-hybrid fallback** for any step not yet natively reimplemented | Phase 3.10 | Steps still in hybrid mode call the existing CLI; retain the ability to fall back to native Python orchestration if a Mastra path regresses. Decommission the Python oracle per-step only after sustained production parity. |
| 5.6 | Establish **drift detection** between Backlog.md, Beads, and Mastra run state | round-trip test (1.6); reconciliation (2.6) | Run the round-trip parity + idempotent reconciliation continuously in production to catch ownership drift early (`07-...:107,193`). |

**Go/No-Go Gate G5 (production-readiness, recurring):** Each rollout increment PROCEEDS only if parity suite + isolation test + recovery drill pass in the production-config environment. NO-GO / rollback if drift detection (5.6) flags divergence, a recovery drill fails, or cost/audit attribution is incomplete.

### 8.7 Consolidated Decision Gates (cross-phase)

| ID | Decision | Owner phase | Gates | Default if unresolved |
|---|---|---|---|---|
| D1 | Primary work-of-record: Backlog.md vs Beads | Phase 0 (final by Phase 4) | G0, G4 | NO-GO to Phase 1 — all mappings depend on it |
| D2 | Mastra OSS vs Enterprise licensing track | Phase 0 (final by Phase 4) | G4 | OSS pilot allowed; multi-tenant NO-GO until resolved |
| D3 | Separate governance/control-plane ownership | Phase 0 (built Phase 4) | G4 | Multi-tenant NO-GO without it |
| D4 | Runtime subprocess/exec seam (hybrid wrapper) | Phase 0 | G0, G2 | Hybrid = keep calling existing CLI |
| D5 | Beads deployment mode + version pin | Phase 0 (server mode by Phase 4) | G1, G4 | Embedded = solo eval only |

### 8.8 Validation and Eval Strategy (cross-phase summary)

The roadmap reuses the existing `cli/eval` harness patterns as the test substrate at every phase, and adds artifact/gate parity tests:

| Capability | Reuse from | Used in |
|---|---|---|
| Round-trip parser parity (import → export → `discover_phases`/`parse_tasklist_file`/`count_tasks_in_file`) | `sprint/config.py`; `07-...:125,180` | Phase 1 (G1), Phase 5 drift |
| Capability preflight (`claude --version`, `~/.claude/` checks) | `eval/commands.py:119-205` | Phases 2–3 |
| Safe parallel execution (per-run HOME, scratch-root allowlist, containment guard) | `eval/isolation.py:224-260,456-642` | Phases 2–3 (G2, G3) |
| Ordered outcome accounting (never drop an outcome, preserve spec order) | `eval/orchestrator.py:164-299` | Phase 3 parity suite |
| Forensic JSONL logs + preserve-failed-HOME | `eval/runner.py:537-588,425-473` | Phases 2–5 |
| Retry-once policy for flaky (MCP) steps | `eval/retry.py:92-165` | Phases 2–3 |
| Return-contract / artifact diffing | `cli_portify/executor.py:283-372` | Phase 3 artifact parity (G3) |
| Gate verdict + mode parity | `roadmap/gates.py`; `pipeline/models.py:69-79` | Phase 3 gate parity (G3) |
| Checkpoint enforcement parity | `09-...:106-110`; `checkpoints.py:18-94` | Phase 3 (G3) |
| Recovery/resume parity | `sprint/executor.py:1702-1721`; `09-...:64-66` | Phases 3, 5 |
| Tenant isolation + audit + cost two-tenant test | net-new (`web-04:125,149-150`) | Phase 4–5 (G4, G5) |

### 8.9 Summary

The recommended path is **hybrid adapter-first** (Option A), corroborated by data-model risk evidence (`07-...:173`): preserve the verified current contracts — stable IDs, sprint parser shapes, numbered-checkpoint contract, shared pipeline/gate models, and the Claude CLI subprocess seam — while adding read-only adapters, then a single wrapped pipeline, then full parity, then multi-tenant governance.

The smallest safe first slice is wrapping **`superclaude tasklist validate`** (a single-step, strict-gate, non-destructive pipeline; `tasklist/executor.py:191-218,221-248`) behind a Mastra workflow. Each phase has an explicit go/no-go gate; the load-bearing early gate is **G2 — proving Mastra rerun/recovery/durability semantics** (`web-01:86`), without which the stateful `roadmap`/`sprint` ports are infeasible.

Multi-tenant hardening is NOT a thin add-on: it requires a **Mastra Enterprise licensing decision**, a **separate governance/control-plane layer** (`web-04:140,145`), **tenant-aware identity/audit/cost attribution** with separated trigger/execution/authorization/tenant/attribution identities (`web-04:66-71`), and a **final primary work-of-record decision between Backlog.md and Beads** (`07-...:193`). Mastra + Backlog.md + Beads alone are an orchestration/task substrate, not an enterprise governance plane.

This roadmap is **phase-gated and decision-gated**, not code-ready: `[DECISION-GATED]` and `[UNVERIFIED]` markers indicate where prerequisite decisions or hands-on validation must precede implementation.

---

## 9. Open Questions

Open questions are grouped into (9.A) strategic/architectural decisions the project owner must make and (9.B) verification/parity gaps that survived the research gate. None of these are answered here; each carries an honest impact and a suggested resolution path. Questions whose evidence is genuinely unresolved are flagged as such in the Suggested Resolution column.

### 9.A Strategic / Architectural Open Questions (owner decisions)

| # | Question | Impact | Suggested Resolution |
|---|---|---|---|
| Q1 | Primary work-of-record: Backlog.md vs Beads vs Mastra storage? Backlog.md (markdown task tree) and Beads (Dolt issue/dependency graph) functionally overlap; one must be primary work-of-record, the other memory/graph. | Core architecture decision; wrong split causes status drift between two task owners (research file `07` flags dual task/status owners as a drift risk; `web-02 §13`/`web-04 §14-15` confirm neither tool owns cross-system authority). | Decide canonical owners per data class: human-readable task/spec/decision body (Backlog.md), dependency DAG + ready-queue + claim/memory (Beads), durable workflow snapshots/state (Mastra storage). Pilot a single workflow (e.g., Backlog↔Beads import/export) before broad integration, per Backlog.md maintainer guidance (`web-02 §13`). Unresolved until owner picks canonical status/body/graph owners (`research/11:100`). |
| Q2 | Multi-tenancy model: what tenant/actor/audit identity model does the company orchestration layer require? | Strategic driver of the whole replatforming; current scoped SuperClaude models carry no tenant/actor identity fields (`research/07`, `research/11:115`), and MCP/Mastra/Backlog/Beads do not supply a tenant-aware governance plane (`web-04 §13-15`). | Run a repo-wide identity audit (current claim is scoped to read dataclasses only), then design a tenant/actor/audit identity model separating trigger/execution/authorization/tenant/attribution identities (`web-04 §9`). Treat as new target-design requirement, not an existing capability. Genuinely open pending identity-model design. |
| Q3 | Pilot deployment scope: which tenant count and local-vs-hosted track should the first slice use? | Determines effort band and whether EE licensing is triggered on day one; external research recommends separate local/OSS vs team/EE tracks (`web-01 §6`, rec 3). | **Surface recommendation is resolved by Section 8:** start with single-tenant `superclaude tasklist validate` as the smallest non-destructive wrapped pipeline. The remaining owner decision is deployment scope: local OSS-only spike vs hosted/team pilot, tenant count, and whether that triggers EE licensing. |
| Q4 | Parity bar for sprint and roadmap: like-for-like behavior, or accept behavior changes? | Sets the migration acceptance criteria; several current behaviors are advisory/stubbed (status/logs stubs, trailing-gate grace=0 forcing blocking, certify gate not wired in production) and "parity" may mean preserving or fixing them (`research/02`, `research/03`, `research/11:66-67`). | Owner must declare, per surface, whether the target preserves current effective behavior or adopts the documented-intended behavior. Unresolved design decision; carried as risk R7 below. |
| Q5 | Subprocess / sandbox mapping: does Mastra Workspace `WorkspaceSandbox.executeCommand` safely replace the `ClaudeProcess` subprocess seam with parity on hooks/permissions/freshness? | The runtime seam is the single coupling point a port must replace (`seed-brief`, `research/08:82`); external research explicitly states Workspace does NOT prove Claude Code hook/permission parity (`web-01 §3`, limitation 3). | Run a safety spike: validate `executeCommand` allowlists, env isolation, secret redaction, timeout, retention, approval against Claude Code hook/permission/freshness behavior before assuming parity. Genuinely unverified; hands-on validation required (`web-01` rec 2). |
| Q6 | Mastra Enterprise licensing: does multi-user/hosted RBAC/SSO/audit force the Mastra EE license, and at what cost/lock-in? | License-cost and lock-in driver; production RBAC/FGA/SSO/Studio-auth/Agent-Builder/audit/on-prem are Enterprise-linked (`web-01 §6, §10`; dual license Apache-2.0 core + EE for `ee/`). | Confirm EE pricing/terms with vendor for the intended deployment model; scope which features actually require EE vs OSS. Pricing/terms not fully resolved in research (vendor pricing page cited but exact figures not captured). Open pending vendor confirmation. |

### 9.B Verification / Parity Open Questions (from research gate + gap-fill)

| # | Question | Impact | Suggested Resolution |
|---|---|---|---|
| Q7 | Source-of-truth conflict: `src/superclaude/` (core/project policy) vs plugin-mirror READMEs ("edit plugins first"); mirrors are materially out of sync. | A port could ingest the wrong instruction corpus (skills/agents/hooks/commands) (`gaps RG-I4`, `research/11:51,84,110`). | Owner picks a canonical resolver; implementation must add a sync verifier/gate before ingesting any corpus. Use `src/superclaude/` meanwhile. Open pending resolver decision + sync audit. |
| Q8 | Checkpoint contract: should `executor.py` per-task branch call `_verify_checkpoints()`, and should the freeform `process.py` prompt and `phase-template.md` be aligned to the numbered-task checkpoint contract? | Sprint-compatible adapter correctness; canonical contract is numbered checkpoint tasks, but prompt/template/docs still reference legacy `### Checkpoint:` sections, and the per-task branch skips verification (`research/09:107,158-163`, `RG-C2`). | Adopt the canonical contract in `research/09:127-154`; emit numbered checkpoint tasks with `Checkpoint Report Path:` lines. The executor-branch wiring and prompt/template sync are open remediation decisions (`research/09:158-163`). |
| Q9 | `/sc:forensic` and sprint `rerun-tasks`: are these supported current surfaces, or must they be excluded/built? | TFEP/implementation scope could include unsupported features (`gaps RG-I5`, `research/11:88,93,113-114`). | Targeted source search found neither in current `src/superclaude` (no forensic command/skill; `sprint/commands.py` has no `rerun-tasks`). Exclude from current-state and implementation features unless a separate task locates or builds them. Open if retained. |
| Q10 | Backlog.md / Beads / Mastra schemas and API semantics for SuperClaude orchestration metadata (checkpoints, telemetry, retrospective, gates). | Field/state mappings are hypotheses; Backlog.md MCP schemas reject unknown properties (`additionalProperties:false`, `web-02 §4`), Beads is Dolt-first with envelope-mode JSON migration (`web-03 §4,7`). | Validate against current docs/APIs and prototype mappings; keep field mappings as hypotheses until validated (`research/11:60,71,86`). Open pending integration prototype. |
| Q11 | Skill-vs-CLI parity scope: does the port target CLI parity, skill/protocol parity, or a merged future state? | Determines port scope and effort before estimation; tasklist generation lives in the skill protocol while the CLI only validates (`research/02`, `research/11:70`). | Owner must pick one parity scope before estimating (targeted-research blocker for broad port scope, `research/11:70`). Open. |
| Q12 | Roadmap production wiring: is the certification gate (`CERTIFY_GATE`) actually appended in production `_build_steps`, and is `wiring-verification` trailing or blocking given `grace_period=0`? | Roadmap parity risk; declared-vs-effective behavior diverges (`research/02`, `research/11:66-67`). | State effective current behavior separately from intended behavior in the parity matrix; verify wiring before claiming certification is a live production step. Open / carry as risk R7. |
| Q13 | Exhaustive command/skill/agent semantic parity: have all assets been semantically reviewed, or only sampled? | Overclaim risk if a parity matrix is described as exhaustive (`gaps RG-M2`, `research/11:53,116`). | Label inventories as scoped/sampled; run an exhaustive semantic inventory only if the parity matrix requires every asset. Open if exhaustive parity is in scope. |

### 9.C Risk Register

Severity = combined Impact × Likelihood judgment (High / Medium / Low). Likelihood reflects current evidence strength, not a forecast. "Owner / Decision Gate" names where the risk must be resolved before it is allowed to propagate into implementation. Every row is evidence-cited; no risk is asserted without a source.

| # | Risk | Source Evidence | Impact | Likelihood | Severity | Mitigation | Owner / Decision Gate |
|---|---|---|---|---|---|---|---|
| R1 | License risk: production multi-user RBAC/SSO/FGA/audit/on-prem are Mastra Enterprise-licensed (`ee/` directories), not Apache-2.0 core. | `web-01 §6, §10` (dual license, EE-gated Studio auth/RBAC/FGA/Agent-Builder); `seed-brief` Known Context (EE license for `ee/`). | High (cost + lock-in for the strategic multi-tenant driver) | High (RBAC/SSO/audit are explicitly EE-linked) | High | Separate local/OSS and team/EE architecture tracks (`web-01` rec 3); confirm EE pricing/terms (Q6); design so OSS-only features remain usable single-tenant. | Owner + vendor before any hosted multi-tenant build (Q6 gate). |
| R2 | Language/runtime migration: ~65K-LOC Python orchestration must be replatformed onto Mastra's TypeScript step/workflow model; the `ClaudeProcess` subprocess seam must be replaced. | `seed-brief` Problem Statement (~65K LOC Python; subprocess driver); `research/08:38-70` (CODE-VERIFIED subprocess seam + sprint/roadmap/tasklist surfaces); `web-01 §2-3` (Mastra TS workflows + Workspace). | High (large rewrite; gate/convergence logic is pure Python today) | Medium-High (feasible per `web-01`, but unproven for these specific control loops) | High | Strangler-fig phased roadmap; port portable Markdown/YAML harness first; rebuild gate/wave/checkpoint loops as Mastra control flow; prototype before committing (`web-01` rec 1, bottom line). | Architecture owner; runtime-seam spike gate (Q5). |
| R3 | Backlog.md / Beads functional overlap: both can act as task store; dual task/status owners cause drift. | `seed-brief` Known Context (overlap risk); `research/07` + `research/11:100` (dual task/status owner drift); `web-02 §13` (Beads↔Backlog integration not mature, maintainer says narrow scope first). | High (data integrity / single-source-of-truth) | Medium (avoidable with a clear ownership split) | High | Assign canonical owners per data class (Q1); start with one narrow Backlog↔Beads sync workflow; do not assume native integration. | Owner (Q1 decision gate). |
| R4 | Beads / Dolt version churn: v1.0.5 carries "do not upgrade" sync warnings; migration `0043` can silently break multi-machine `bd dolt` sync; v1.0.4 had a server-mode data-clobber regression. | `web-03 §2` (v1.0.5 pre-release/gated, issue #4259, #3870); `web-03 §15` (fast-moving with sharp edges); seed-brief Beads version note (now corrected by `web-03 §7`). | High (data loss / corruption in multi-writer sync) | Medium (only if upgrades are unpinned/ungated) | High | Pin and gate Beads versions; avoid gated/pre-release builds; require `bd doctor` + backup/restore + push/pull smoke tests in adoption gates (`web-03` rec 4). | Platform/ops owner; version-pin gate before any Beads adoption. |
| R5 | Concurrency / multi-writer: Beads embedded mode is single-writer ("database is locked"); multi-agent needs Dolt server/shared-server mode, and session attribution is actively changing. | `web-03 §8-9` (embedded single-writer; server mode for concurrent writers; issues #3400/#3583 on session attribution); `web-02 §12` (Backlog.md is file/lock-based, not a transactional multi-user backend). | High (parallel/multi-agent orchestration correctness) | Medium-High (default embedded mode is insufficient for the company use case) | High | Require Beads server/shared-server mode for any multi-agent writer scenario; enforce atomic `bd update --claim`; one-task-per-agent/session discipline; track session-attribution fixes. | Architecture owner; concurrency-model gate before multi-agent rollout. |
| R6 | Subprocess / hook safety parity: Mastra Workspace `executeCommand` does NOT replicate Claude Code hooks, freshness checks, staging restrictions, or permission prompts; SuperClaude safety rules (UV-only, git safety, `.claude/` SoT, fork-PR target) must be rebuilt. | `web-01 §3` + limitation 3, rec 5; `research/11:111,123` (hooks are Claude Code-specific; portable unit is the policy, not the shell scripts); `gaps RG-I5`. | High (safety regression: unsafe command execution, lost guardrails) | High (parity is explicitly not provided by Mastra defaults) | High | Safety spike before assuming CLI parity (Q5); reimplement hook policies as Mastra middleware/guards; preserve SuperClaude governance outside Mastra defaults (`web-01` rec 5). | Security/architecture owner; safety-spike gate (Q5). |
| R7 | Checkpoint contract drift + roadmap wiring drift: stale prompt/template/docs reference legacy `### Checkpoint:` sections; per-task executor branch skips `_verify_checkpoints()`; certify gate may not be wired in production; trailing gate grace=0 forces blocking. | `research/09:98-109,158-172` (checkpoint contradiction; per-task branch skips verification; stale docs); `research/02` + `research/11:66-67` (certify wiring + trailing/blocking mismatch). | Medium-High (silent loss of checkpoint/gate enforcement on port) | Medium (real in docs/prompt surfaces; runtime parser already handles both shapes) | Medium-High | Adopt canonical numbered-checkpoint contract (`research/09:127-154`); emit `Checkpoint Report Path:` lines; align stale prompt/template/docs; state effective-vs-intended behavior separately (Q8, Q12). | Implementation owner; checkpoint/parity decision gate (Q8/Q12). |
| R8 | Governance / tenancy / cost gaps: Mastra + Backlog.md + Beads provide no tenant isolation, no per-invocation audit, no cost attribution, no policy/approval/catalog control plane; MCP is a protocol, not governance. | `web-04 §1-15` (MCP not governance; token passthrough forbidden; tenant/realm mix-up pitfalls; Mastra/Backlog/Beads each not a governance plane); `research/07` + `research/11:99` (tenant/actor/audit identity is a new target requirement). | High (blocks safe company-wide multi-tenant deployment) | High (none of the three tools supplies this layer) | High | Add a dedicated governance/control-plane service (tenant registry, identity mapping, RBAC/ABAC, tool catalog, audit log, cost/budget metering) + MCP/AI gateway enforcing OAuth 2.1, audience validation, scoped tools (`web-04` rec 2-3). | Owner + security; governance-plane gate before multi-tenant deployment (Q2). |
| R9 | Reliance on fast-moving external tools: Mastra (`@mastra/core` 1.1.0+, Temporal integration experimental), Backlog.md (v1.45.2, MCP MVP + doc drift + open browser state-loss bug), Beads (1.x, frequent CLI/API changes) are all rapidly evolving. | `web-01 §1` (Temporal experimental), §9 (vendor maturity claims need validation); `web-02 §5,9,10,11` (MCP MVP, doc drift, issue #578, v1.45.2); `web-03 §15` (active 1.x, sharp edges). | Medium-High (breaking changes, doc drift, schema instability mid-build) | High (all three are pre-mature or fast-moving) | Medium-High | Pin versions; runtime-verify MCP instruction/schema surfaces (`web-02` rec 6); avoid experimental runners (Temporal); prefer stable contracts (`bd --json`, Backlog CLI/MCP); budget for churn; do not migrate without hands-on validation (`web-01` bottom line). | Platform owner; version-pin + validation gates per tool. |

**Cross-reference:** R1↔Q6, R2↔Q5/Q11, R3↔Q1, R6↔Q5, R7↔Q8/Q12, R8↔Q2, R9↔Q10. The seed brief's required risk-register coverage (license drift, Backlog/Beads overlap, loss of Claude-Code-native features, multi-tenant security) is satisfied by R1, R3, R6, and R8 respectively (`seed-brief` Success Criteria).

---

## 10. Evidence Trail

All paths are relative to the repository root `/config/workspace/IronClaude/`. The task directory prefix `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/` is abbreviated as `<TASK>/` below.

### 10.1 Codebase Research Files (Phase 1-3, files 01-07)

| File | Path | Topic / Scope |
|---|---|---|
| 01 | `<TASK>/research/01-pipeline-core-contracts.md` | Shared pipeline core contracts: `pipeline/` models, executor, gates, process (`ClaudeProcess` seam), trailing_gate, deliverables, diagnostic_chain — for Stack D port feasibility. |
| 02 | `<TASK>/research/02-roadmap-tasklist-pipelines.md` | Roadmap and tasklist CLI + skill protocols + commands; certification/wiring/convergence gates; generation-vs-validation split. |
| 03 | `<TASK>/research/03-sprint-execution-runtime.md` | Sprint execution runtime: Path A/B execution, tmux/session driver, stream-json monitor, isolation, status/log stubs, retrospective, checkpoints. |
| 04 | `<TASK>/research/04-cli-portify-prd-cleanup-audit-eval.md` | Adjacent orchestration surfaces: cli_portify, prd, cleanup_audit, eval, audit; retry/forensic/eval drift. |
| 05 | `<TASK>/research/05-skills-agents-harness-reuse.md` | Portable harness reuse: skills, agents, commands, core, templates, hooks, mcp; reuse/adapt/rewrite mapping (patched for external tags + MCP citation). |
| 06 | `<TASK>/research/06-docs-and-existing-feasibility-artifacts.md` | Existing docs + feasibility artifacts inventory and cross-validation (inventory line superseded by file 08). |
| 07 | `<TASK>/research/07-target-data-model-and-ownership.md` | Target data model and ownership: MDTM task/checkpoint shape, tenant/actor/audit identity absence (scoped), Backlog/Beads/Mastra ownership split. |

### 10.2 Web Research Files (Phase 4 external, dated 2026-06-02)

| File | Path | Topic |
|---|---|---|
| web-01 | `<TASK>/research/web-01-mastra-current-capabilities.md` | Mastra 1.0+ workflows, Workspace/subprocess, storage, observability/Studio, MCP, deployment, auth/RBAC/FGA, Enterprise licensing. Provenance: tavily + context7. |
| web-02 | `<TASK>/research/web-02-backlog-md-current-capabilities.md` | Backlog.md v1.45.2 CLI/MCP/schema, MCP MVP + `additionalProperties:false`, no-git mode, agent workflow, Beads integration immaturity, browser state-loss bug. Provenance: tavily. |
| web-03 | `<TASK>/research/web-03-beads-current-capabilities.md` | Beads (`gastownhall/beads`) CLI/JSON contract, Dolt-first storage, embedded vs server mode, multi-writer, gates, v1.0.5 sync warnings. Provenance: tavily. |
| web-04 | `<TASK>/research/web-04-mcp-multitenancy-governance.md` | MCP enterprise governance limits, tenancy/audit/cost gaps, OAuth 2.1, token-passthrough ban, control-plane patterns; Mastra/Backlog/Beads governance insufficiency. Provenance: tavily. |

### 10.3 Gap-Fill Research Files (fix cycle 1, files 08-11)

| File | Path | Topic / Remediated Gate Finding |
|---|---|---|
| 08 | `<TASK>/research/08-gap-fill-feasibility-enrichment.md` | RG-C1: reconciles existing feasibility enrichment files (`enrichment/codebase-context.md`, `research-deep.md`) that exist in repo; supersedes stale file-06 inventory. |
| 09 | `<TASK>/research/09-gap-fill-checkpoint-contract.md` | RG-C2: checkpoint-contract contradiction (numbered-task vs legacy `### Checkpoint:`); defines canonical sprint-compatible checkpoint shape + adapter implications. |
| 10 | `<TASK>/research/10-gap-fill-harness-claim-patch.md` | RG-I2/RG-I3: tags external Mastra/Backlog/Beads claims `[UNVERIFIED external]` in file 05; corrects invalid `MCP.md:269-305` → `269-304`. |
| 11 | `<TASK>/research/11-gap-fill-unverified-inputs-classification.md` | RG-I1/RG-I4/RG-I5/RG-M2/RG-M3: classifies every unresolved gap as resolved / synthesis-safe / carry-as-risk / targeted-blocker / out-of-scope; defines synthesis guardrails. |
| Notes | `<TASK>/research/research-notes.md` | Phase inventory / scope notes used to seed codebase research coverage and track research inputs. |

### 10.4 Synthesis Files

| File | Path | Report Sections |
|---|---|---|
| synth-01 | `<TASK>/synthesis/synth-01-problem-current-state.md` | Sections 1-2: Problem Statement and Current State Analysis (code-verified facts only). |
| synth-02 | `<TASK>/synthesis/synth-02-target-gaps.md` | Sections 3-4: Target State and Gap Analysis. |
| synth-03 | `<TASK>/synthesis/synth-03-external-findings.md` | Section 5: External Research Findings (web-01..04 reconciled against `research-deep.md` seed). |
| synth-04 | `<TASK>/synthesis/synth-04-options-recommendation.md` | Sections 6-7: Options analysis (four options A-D with Effort/Risk/Reuse/Files/Pros/Cons tables + an Options Comparison table) and the conditional go/no-go/hybrid (D→A) recommendation with spike exit gates and rationale-against-comparison. |
| synth-05 | `<TASK>/synthesis/synth-05-implementation-roadmap.md` | Section 8: Phased implementation roadmap / strangler-fig sequencing. |
| synth-06 | `<TASK>/synthesis/synth-06-risk-questions-evidence.md` | Sections 9-10: Open Questions, Risk Register support block, Evidence Trail. |

### 10.5 Gaps Log and QA Reports

| File | Path | Role |
|---|---|---|
| Gaps log | `<TASK>/gaps-and-questions.md` | Merged, classified gap/question register (RG-C1..RG-M3) feeding Sections 9-10 and the risk register. |
| QA — analyst 1 | `<TASK>/qa/analyst-completeness-report-1.md` | Completeness verdict for research files 01-04 (PASS; 8 important gaps carried). |
| QA — analyst 2 | `<TASK>/qa/analyst-completeness-report-2.md` | Completeness verdict for research files 05-07 (FAIL; enrichment contradiction + checkpoint/SoT/external gaps). |
| QA — gate 1 | `<TASK>/qa/qa-research-gate-report-1.md` | Research-gate verdict for files 01-04 (FAIL; unresolved gaps). |
| QA — gate 2 | `<TASK>/qa/qa-research-gate-report-2.md` | Research-gate verdict for files 05-07 (FAIL; checkpoint contradiction, untagged external claims, invalid MCP citation). |
| QA — merged | `<TASK>/qa/research-gate-merged-report.md` | Merged research-gate verdict (FAIL) + deduplicated findings + required gap-fill plan. |
| QA — fix cycle 1 | `<TASK>/qa/qa-research-fix-cycle-1.md` | Fix-cycle verdict (PASS, 15/15; \|F1\|=0); gate cleared for Phase 4 with guardrails. |

### 10.6 Feasibility Seed and Enrichment Inputs (pre-existing)

| File | Path | Role |
|---|---|---|
| Seed brief | `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` | Original problem statement, known context, constraints, success criteria, strategic open questions (source for Section 9.A). |
| Enrichment — codebase | `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md` | Prior codebase-context seed (architecture broadly code-verified; line/LOC refs approximate per file 08). |
| Enrichment — deep | `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/research-deep.md` | Prior external/Stack-D deep-research seed (superseded by fresh web-01..04 where they differ; per Section 5 ground rules). |

---

## Report Provenance

This report consolidates six synthesis files (synth-01..06) into the ten required sections. Per the synthesis guardrails (research 11) and the user's honesty rule, unresolved target-stack, source-of-truth, hook-portability, recovery, checkpoint, identity, and licensing-cost matters remain Open Questions (Section 9) or Risks (Section 9.C) rather than being resolved into facts. External Stack D claims trace to fresh web research (`provider=tavily`, dated 2026-06-02); codebase claims trace to `[CODE-VERIFIED]` source reads under `src/superclaude/`.
