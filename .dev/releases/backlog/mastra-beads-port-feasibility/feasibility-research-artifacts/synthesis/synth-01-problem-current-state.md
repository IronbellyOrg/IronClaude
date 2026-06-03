# Synthesis 01: Problem Statement and Current State (Report Sections 1-2)

**Task:** TASK-RESEARCH-20260602-211124
**Date:** 2026-06-02
**Status:** Complete
**Scope:** Report Sections 1 (Problem Statement) and 2 (Current State Analysis)
**Sourcing rule:** Every fact below is traced to a research file under
`.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/` or the seed brief at
`.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md`. Current-state facts are
restricted to `[CODE-VERIFIED]` findings per the synthesis guardrails in research file `11`.
Doc-only, `[UNVERIFIED]`, and `[CODE-CONTRADICTED]` claims are excluded from current-state facts
and surfaced only as risks/caveats where the research files require it.

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
| `execute_pipeline(steps, config, run_step, ...)` sequences `Step | list[Step]` entries; nested lists = parallel groups. | `executor.py:63-78` |
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

## Current-State Summary

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

**Status:** Complete
