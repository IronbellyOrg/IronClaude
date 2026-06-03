# Synthesis 03 — Section 5 Subsystems 5.1–5.3 (Existing / Built Side)

**Target template sections:** §5.1 Existing pipeline-core seam · §5.2 Roadmap & tasklist workflows · §5.3 Sprint execution runtime
**Document:** Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration — Technical Reference
**Tag legend:** `[CODE-VERIFIED]` = existing Python at HEAD `9e864860` (real `path:line`); `[DESIGN — UNBUILT]` = target hybrid mapping (feasibility evidence, not code); `[EXTERNAL-VERIFIED]` = web source.
**Code root:** `src/superclaude/cli/` · **HEAD:** `9e864860` · **Spot-checks:** spot-01/02/03 (all CONFIRMED).

> **Important:** Subsections 5.1–5.3 document the **existing built subsystems being adapted**. Every architectural fact carries `[CODE-VERIFIED]` with a real `path:line`. Target-stack mappings (how a Mastra/Backlog.md/Beads port would represent these) are called out inline as `[DESIGN — UNBUILT]` and are NEVER presented as built. Demarcation per R2.

**Status: Complete**

---

### 5.1 Existing Pipeline-Core Seam `[CODE-VERIFIED]`

**Purpose:** The framework-neutral orchestration core (`src/superclaude/cli/pipeline/`) that all higher pipelines reuse: shared dataclass/enum contracts, a generic step sequencer with retry/gates/parallel dispatch, pure-Python gate validation, and the single replaceable subprocess boundary to the Claude CLI. This is the strongest port seam — orchestration, gating, and process execution are already separated behind injectable protocols `[CODE-VERIFIED]`.

**Key Files:**

| File | Purpose |
|------|---------|
| `pipeline/models.py:1-234` | Shared contracts; stdlib-only imports, zero sprint/roadmap imports (`models.py:1-6`, `:8-14`) `[CODE-VERIFIED]` |
| `pipeline/executor.py:1-469` | Generic `execute_pipeline()` sequencer; NFR-007 no sprint/roadmap imports (`executor.py:7`) `[CODE-VERIFIED]` |
| `pipeline/gates.py:1-142` | Pure-Python `gate_passed()` tier validation; no subprocess/LLM (`gates.py:1-10`) `[CODE-VERIFIED]` |
| `pipeline/process.py:1-244` | `ClaudeProcess` — THE runtime seam; sole `subprocess.Popen` (`process.py:134`) `[CODE-VERIFIED]` |
| `pipeline/trailing_gate.py:1-648` | Async gate eval, deferred-remediation log, scope-based mode resolution `[CODE-VERIFIED]` |
| `pipeline/deliverables.py:1-194` | Heuristic implement/verify decomposition `[CODE-VERIFIED]` |
| `pipeline/__init__.py:1-157` | 42-symbol public API surface (compatibility anchors) `[CODE-VERIFIED]` |

**How It Works:**

`execute_pipeline(steps, config, run_step, ...)` accepts `list[Step | list[Step]]`; a nested list is a parallel group (`executor.py:63-188`, sig `:63-72`) `[CODE-VERIFIED]`. The executor owns ordering, retry, gates, cancellation, and state callbacks; it never spawns a subprocess directly — all execution is delegated to the injected `StepRunner` callable (`executor.py:41-60`) `[CODE-VERIFIED]`. This injection point is the migration seam.

Per step, `_execute_single_step()` (`executor.py:191-399`) runs a retry loop and branches on gate mode `[CODE-VERIFIED]`:

```
run_step()  ──►  StepResult re-wrapped w/ attempt (executor.py:230-238)
   │
   ├─ no gate ............. trust runner status (:240-243)
   ├─ TIMEOUT/CANCELLED ... return without gate check (:245-248)
   ├─ TRAILING ........... submit to runner, return PASS immediately (:250-262)
   └─ BLOCKING ........... gate_passed(_gate_target(out), step.gate) (:264-278)
                              │ fail → cosmetic remediation (:280-364)
                              │      → retry if attempt<max (:375-376)
                              └      → terminal FAIL (:378-388)
```

`_gate_target()` (`executor.py:23-35`) prefers a sibling `.compressed.md` sidecar over the original output — gates validate what the downstream LLM actually consumes `[CODE-VERIFIED]`. Trailing-gate machinery (`trailing_gate.py`) is **advisory** in current code: at pipeline end, pending trailing results are collected with timeout `max(30.0, grace_period)` and failures are logged as warnings only, never converted to failed `StepResult`s (`executor.py:175-186`) `[CODE-VERIFIED]`.

`gate_passed()` (`gates.py:20-76`) enforces four tiers `[CODE-VERIFIED]`: EXEMPT always passes (`:28-30`); LIGHT requires existence + non-empty (`:41-43`); STANDARD adds min_lines + required frontmatter (`:45-60`); STRICT adds semantic checks short-circuiting on first non-`True` (`:65-74`). The frontmatter parser scans delimiter pairs anywhere (tolerates preamble) and matches top-level keys via regex rather than deep YAML (`gates.py:79-142`) `[CODE-VERIFIED]`.

**`ClaudeProcess` — THE replaceable runtime seam.** `ClaudeProcess` (`process.py:24-244`) is the sole concrete boundary to the `claude` CLI in the pipeline package: it is the only class that builds a `claude --print` argv (`build_command()`, `process.py:73-95`) and the only one that calls `subprocess.Popen` — at **`process.py:134`** `[CODE-VERIFIED]` (spot-01 confirmed). The prompt is delivered via stdin to dodge Linux `MAX_ARG_STRLEN` (`process.py:76-78`, `:136-139`); `wait()` returns exit code `124` on timeout to match bash semantics (`process.py:165`); `terminate()` escalates SIGTERM→10s→SIGKILL→5s on the process group (`process.py:173-214`) `[CODE-VERIFIED]`. Gates and trailing-gate code are pure-Python (no subprocess), so they are **not** a runtime seam. Replacing `ClaudeProcess` behind the `StepRunner` protocol is therefore the single substitution point to swap the Claude-CLI runtime.

**Public Interface (key signatures):**

```python
# models.py — portable contracts
class StepStatus(Enum): PENDING|PASS|FAIL|TIMEOUT|CANCELLED|SKIPPED   # is_failure ⇔ FAIL|TIMEOUT only (:64-66)
class GateMode(Enum): BLOCKING | TRAILING                              # (:69-78)
@dataclass GateCriteria(required_frontmatter_fields, min_lines, enforcement_tier, semantic_checks)  # (:90-105)
@dataclass Step(id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path)  # (:108-122)
@dataclass StepResult(step, status, attempt, gate_failure_reason, started_at, finished_at, remediated, remediations)  # (:125-148)
@dataclass PipelineConfig(work_dir, dry_run, max_turns, model, permission_flag='--dangerously-skip-permissions', debug, grace_period=0, ...)  # (:212-234)

# executor.py — orchestration seam
class StepRunner(Protocol): def __call__(step, config, cancel_check) -> StepResult   # (:41-60)
def execute_pipeline(steps: list[Step|list[Step]], config, run_step, on_step_start=None, on_step_complete=None, ...) -> list[StepResult]  # (:63-188)

# gates.py — deterministic validation
def gate_passed(output_file: Path, criteria: GateCriteria) -> tuple[bool, str|None]   # (:20-76)

# process.py — THE runtime seam
class ClaudeProcess:  # (:24-244)  sole subprocess.Popen at :134
    def build_command(self) -> list[str]            # (:73-95)  claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>
    def start(self) -> subprocess.Popen             # (:114-157)
    def wait(self) -> int                           # (:159-171)  124 on timeout
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| `claude` CLI binary | subprocess | Spawned by `ClaudeProcess` only (`process.py:134`) `[CODE-VERIFIED]` |
| Python stdlib | import | `models`/`gates`/`trailing_gate` import only stdlib + pipeline-local (`models.py:8-14`, `gates.py:12-17`) `[CODE-VERIFIED]` |
| Filesystem | I/O | Output artifacts, `.compressed.md` sidecars, `.log` sidecars (tool_write_mode) `[CODE-VERIFIED]` |

**Consumers:**

| Used By | How |
|---------|-----|
| Roadmap (§5.2) | Generic `execute_pipeline` + injected `roadmap_run_step` (`roadmap/executor.py:25-35`) `[CODE-VERIFIED]` |
| Tasklist validate (§5.2) | `execute_pipeline` + `tasklist_run_step` (`tasklist/executor.py:23-25`, `:259-263`) `[CODE-VERIFIED]` |
| Roadmap validate | `execute_pipeline` + `ClaudeProcess` runner (`validate_executor.py:105-180`) `[CODE-VERIFIED]` |
| Sprint (§5.3) | Reuses `Step`/`StepResult`/`DeferredRemediationLog`/`TrailingGateResult` but runs its **own** phase loop, not `execute_pipeline` (`sprint/executor.py:12-16`) `[CODE-VERIFIED]` |

**Conventions & Patterns:**

- Gate validation targets the `.compressed.md` sidecar when present, NOT the raw output (`executor.py:23-35`, `trailing_gate.py:146-155`) `[CODE-VERIFIED]`. A roadmap comment claiming "gates run on the ORIGINAL output file" (`roadmap/executor.py:1217-1219`) is STALE/CODE-CONTRADICTED — feeds §14.
- Trailing-gate failures are advisory (warning-only) and do not alter returned status (`executor.py:175-186`) `[CODE-VERIFIED]`.
- `grace_period == 0` coerces a declared TRAILING step to BLOCKING (`executor.py:212-214`) `[CODE-VERIFIED]` — see §5.2 wiring-gate note.
- **`[DESIGN — UNBUILT]`** Port mapping: `Step`/`GateCriteria`/`StepResult`/`PipelineConfig` → Mastra workflow schema + Backlog.md/Beads task metadata; replace only `StepRunner`/`ClaudeProcess` first, preserving executor + gate semantics. `DeferredRemediationLog` → Beads durable ledger. Claude-specific `permission_flag`/`--tools default` must stay in a runner-side adapter config, not the portable orchestration model. Feasibility per research file 01 §4/§8; not implemented.

---

### 5.2 Roadmap & Tasklist Workflows `[CODE-VERIFIED]`

**Purpose:** The two highest-level generative/validation pipelines that consume the §5.1 core. Roadmap turns a spec/TDD/PRD into roadmap artifacts via a 12-element step DAG with 15+ gates; tasklist exposes validation-only fidelity checking. Both prove the `StepRunner` seam by injecting their own runner into the generic `execute_pipeline` `[CODE-VERIFIED]`.

**Key Files:**

| File | Purpose |
|------|---------|
| `roadmap/executor.py:1947-2208` | `_build_steps()` — the wired 12-element roadmap DAG `[CODE-VERIFIED]` |
| `roadmap/executor.py:2985-3187` | `execute_roadmap()` — routing, resume, compression, shared-pipeline dispatch `[CODE-VERIFIED]` |
| `roadmap/gates.py:1020-1441` | All roadmap gate definitions (`ALL_GATES` reference list at `:1440`) `[CODE-VERIFIED]` |
| `roadmap/commands.py:32-298` | CLI `run` surface + flags `[CODE-VERIFIED]` |
| `tasklist/executor.py:92-218` | `tasklist_run_step()` pilot runner + single-step `_build_steps()` `[CODE-VERIFIED]` |
| `tasklist/gates.py:23-46` | `TASKLIST_FIDELITY_GATE` (sole gate of validation pipeline) `[CODE-VERIFIED]` |

**How It Works:**

`execute_roadmap()` routes 1–3 inputs (`detect_input_type()` scores PRD→TDD→spec; `roadmap/executor.py:74-335`), restores resume state from `.roadmap-state.json`, compresses, then calls `execute_pipeline(steps, config, roadmap_run_step, ...)` (`roadmap/executor.py:2985-3187`, dispatch `:3124-3131`) `[CODE-VERIFIED]`. The wired DAG from `_build_steps()` (`roadmap/executor.py:1947-2208`) is, in order `[CODE-VERIFIED]` (spot-02 CONFIRMED):

```
extract → [generate-A, generate-B] (parallel) → diff → debate → score →
merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification →
deviation-analysis → remediate
   (:2003)  (:2029-2066)  (:2068) (:2078) (:2088)
   (:2107)  (:2130)       (:2140) (:2158) (:2175)
   (:2186)  (:2196)
```

Step execution is **hybrid**: most steps launch `ClaudeProcess`, but anti-instinct / convergence-spec-fidelity / deviation-analysis / remediate / wiring-verification run deterministic Python (`roadmap/executor.py:955-1250`, `:977-1031`) `[CODE-VERIFIED]`. The adversarial workflow (diff→debate→score→merge) is wired inline in the executor — it does NOT call the `sc-adversarial-protocol` skill (`roadmap/executor.py:2068-2128`) `[CODE-VERIFIED]`. After a run, validation auto-invokes single-agent `reflect` (REFLECT_GATE) or multi-agent `reflect-{agent}` + `adversarial-merge` (`validate_executor.py:239-519`, `executor.py:3409-3447`) `[CODE-VERIFIED]`.

**Spot-check-confirmed gate facts (feed §14):**

- **CERTIFY_GATE UNWIRED.** `CERTIFY_GATE` is defined (STRICT tier, 5 frontmatter fields) at `roadmap/gates.py:1324-1351` and listed in the `ALL_GATES` reference list at `gates.py:1440`, but no `certify` Step is appended in `_build_steps()` (terminates at `remediate`, `:2196-2204`). The comment "Step 12 (certify) constructed dynamically by `roadmap_run_step` after remediate" (`executor.py:2205`) is **unbacked**: `build_certify_step`/`check_certify_resume` have zero production callsites `[CODE-VERIFIED]` (spot-02 CONFIRMED). Defined-only gap.
- **WIRING_GATE TRAILING coerced to BLOCKING.** The `wiring-verification` Step declares `gate_mode=GateMode.TRAILING` (`roadmap/executor.py:2183`, "shadow mode trailing gate") but `PipelineConfig.grace_period` defaults to `0` (`pipeline/models.py:232`) with no CLI override, and `_execute_single_step` coerces `grace_period == 0` → BLOCKING (`pipeline/executor.py:213-214`). So wiring-verification runs **synchronously/blocking** in production despite the trailing intent `[CODE-VERIFIED]` (spot-02 CONFIRMED).
- **Docstring staleness.** `_build_steps` docstring still says "9-step pipeline" (`executor.py:1948`) vs the 12 wired elements; two steps share a "Step 8" comment label (`:2140`, `:2157`). Cosmetic only; ordering unaffected `[CODE-VERIFIED]`.
- **Deviation classifier UNWIRED.** All deviation records render as UNCLASSIFIED; `DEVIATION_ANALYSIS_GATE` pins the `unclassified_count == total_analyzed` invariant (`executor.py:1603-1609`, `gates.py:1390-1422`) `[CODE-VERIFIED]`.

**Tasklist pilot.** The tasklist CLI exposes **only** a `validate` subcommand (no `generate`) (`tasklist/commands.py:31-82`) `[CODE-VERIFIED]`. `_build_steps()` builds exactly one `tasklist-fidelity` Step gated by `TASKLIST_FIDELITY_GATE` (STRICT, 6 frontmatter fields, min_lines 20, 2 semantic checks) over `[roadmap.md] + tasklist_files (+ optional TDD/PRD)` (`tasklist/executor.py:191-218`, gate `tasklist/gates.py:23-46`) `[CODE-VERIFIED]`. The pilot-port runner `tasklist_run_step()` (`tasklist/executor.py:92-188`) is a compact `ClaudeProcess` runner (inline input embedding, cancellation polling, timeout `124`→TIMEOUT, non-zero→FAIL, output sanitize) — the cleanest single-step seam to port first. CLI pass/fail is computed **independently** of the gate: `execute_tasklist_validate` runs the pipeline then parses `high_severity_count` from report frontmatter, returning failure on any HIGH severity or missing report (`tasklist/executor.py:221-276`) `[CODE-VERIFIED]`. Tasklist GENERATION is skill/protocol behavior (`build_tasklist_generate_prompt`, used by `/sc:tasklist`), NOT a CLI subcommand (`tasklist/prompts.py:151-234`) `[CODE-VERIFIED]`.

**Public Interface (key signatures):**

```python
# roadmap/executor.py
def _build_steps(config, ...) -> list[Step | list[Step]]                 # (:1947-2208) 12-element DAG
def execute_roadmap(config, ...) -> RoadmapResult                         # (:2985-3187)
def roadmap_run_step(step, config, cancel_check) -> StepResult            # ClaudeProcess + deterministic-Python hybrid

# tasklist/executor.py
def tasklist_run_step(step, config, cancel_check) -> StepResult           # (:92-188) pilot-port runner
def execute_tasklist_validate(config) -> bool                            # (:251-276) pass ⇔ no HIGH-severity
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| §5.1 pipeline-core | import | `execute_pipeline`, `Step`, `StepResult`, `StepStatus`, `ClaudeProcess` (`roadmap/executor.py:25-35`) `[CODE-VERIFIED]` |
| `.roadmap-state.json` | file | Resume state: spec hash, input type, step statuses, validation/fidelity/certify status (`roadmap/executor.py:2627-2682`) `[CODE-VERIFIED]` |
| `roadmap/convergence.py` | import | `DeviationRegistry`, fidelity-with-convergence cycles (`:90-207`, `:434-668`) `[CODE-VERIFIED]` |

**Consumers:**

| Used By | How |
|---------|-----|
| `/sc:roadmap`, `superclaude roadmap run` | CLI front door (`roadmap/commands.py:32-298`) `[CODE-VERIFIED]` |
| `/sc:tasklist` validate, `superclaude` tasklist validate | Validation-only pipeline `[CODE-VERIFIED]` |
| Sprint (§5.3) | Consumes tasklist-format output (index + phase files) `[CODE-VERIFIED]` |

**Conventions & Patterns:**

- `SPEC_FIDELITY_GATE` is wired only in `--no-convergence` mode; convergence mode replaces it with deterministic pass/fail from `_run_convergence_spec_fidelity` (`executor.py:2158-2173`, `:994-1001`) `[CODE-VERIFIED]`.
- Sprint-compatible tasklist output (N+1 files, literal phase filenames, `T<PP>.<TT>` IDs, checkpoints) is **protocol-specified, not CLI-enforced** (`sc-tasklist-protocol/SKILL.md:91-123`) `[DESIGN — UNBUILT]` (skill spec, no CLI generator).
- **`[DESIGN — UNBUILT]`** Mastra-workflow mapping: the linear+parallel DAG maps to Mastra fan-out/fan-in nodes; per-step gates → Mastra validation steps; `roadmap_run_step` hybrid (LLM vs deterministic) → mix of Mastra agent steps and pure workflow steps. The single-step `tasklist-fidelity` runner is the recommended **first** port candidate. Beads can own the deviation registry / remediation state. Feasibility per research file 02; not implemented.

---

### 5.3 Sprint Execution Runtime `[CODE-VERIFIED]`

**Purpose:** The supervised multi-phase execution engine (`src/superclaude/cli/sprint/`, 19 files / ~8,568 lines) that runs a tasklist bundle phase-by-phase, supervising Claude subprocesses with monitors, watchdogs, checkpoints, diagnostics, and tmux/TUI. It is the **hardest port surface** — a deliberate acceptance stress test, not the first rewrite candidate `[CODE-VERIFIED]`.

**Key Files:**

| File | Purpose |
|------|---------|
| `sprint/executor.py:1135-1757` | `execute_sprint()` core loop (file is 2,148 lines) `[CODE-VERIFIED]` |
| `sprint/commands.py:15-32`, `:189` | `sprint` Click group; `run()` orchestration entry `[CODE-VERIFIED]` |
| `sprint/config.py:275-492` | Phase discovery + `parse_tasklist()` `[CODE-VERIFIED]` |
| `sprint/models.py:347-510` | `SprintConfig(PipelineConfig)`, `PhaseStatus` (11 values), `TurnLedger` `[CODE-VERIFIED]` |
| `sprint/process.py:88-216` | Sprint `ClaudeProcess` subclass + Path B prompt builder `[CODE-VERIFIED]` |
| `sprint/checkpoints.py:22-408` | Checkpoint path/heading parsing, manifest, recovery `[CODE-VERIFIED]` |
| `sprint/monitor.py:253-571` | `OutputMonitor` stream-json reader + stall/exhaustion detectors `[CODE-VERIFIED]` |

**How It Works:**

`execute_sprint(config)` (`sprint/executor.py:1135-1757`) preflights the `claude` binary, installs signal handlers, builds TUI/monitor/`SprintResult`, starts a summary worker, constructs `TurnLedger` / `ShadowGateMetrics` / `DeferredRemediationLog` / `SprintGatePolicy` (`:1228-1234`), runs python-mode preflight phases, then iterates active phases `[CODE-VERIFIED]`. `SprintConfig` **extends** `PipelineConfig` (`models.py:347-510`), so it inherits the §5.1 contracts but runs its own phase loop rather than `execute_pipeline` `[CODE-VERIFIED]`.

**Two execution paths** (`sprint/executor.py:1259-1457`) `[CODE-VERIFIED]`:

```
phase ──► _parse_phase_tasks()
            │
            ├─ tasks present → PATH A (per-task)            (:1259-1301)
            │     execute_phase_tasks() → one subprocess per TaskEntry
            │     aggregate task statuses → continue  ◄── ends at :1301
            │
            └─ freeform (no headings) → PATH B               (:1303-1457)
                  isolation dir + OutputMonitor + ClaudeProcess
                  poll + stall watchdogs → _determine_phase_status() (:1502)
                  if PASS → _verify_checkpoints()  ◄── sole call site :1519
```

**Subprocess supervision.** Sprint's `ClaudeProcess` (`sprint/process.py:88-121`) subclasses the generic pipeline process and delegates lifecycle to `pipeline.process.ClaudeProcess` — it reuses the §5.1 seam, adding a sprint prompt. Path B builds a rich prompt invoking `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` plus sprint context, checkpoint-before-result ordering, and an `EXIT_RECOMMENDATION: CONTINUE|HALT` sentinel (`sprint/process.py:123-216`, `:187-195`, `:208-215`) `[CODE-VERIFIED]`. Path A builds only a minimal task prompt and writes **task-specific** output/error files (`config.task_output_file/task_error_file`, `executor.py:1098-1108`) `[CODE-VERIFIED]`. `OutputMonitor` reads stream-json NDJSON in a daemon thread; runtime watchdogs use CLI-configured `--stall-timeout`/`--startup-stall-timeout` thresholds, with `stall_action=kill` mapping the phase to exit `124` (`monitor.py:253-396`, `executor.py:1366-1445`) `[CODE-VERIFIED]`. `_determine_phase_status()` (`executor.py:2067-2148`) is the authoritative classifier combining exit code + result-file freshness + prompt-too-long detection + checkpoint inference `[CODE-VERIFIED]`.

**Spot-check-confirmed facts (feed §14):**

- **Path A skips checkpoint verification.** The Path A branch (`executor.py:1262-1301`) aggregates task results and `continue`s at `:1301` with no checkpoint call. The **sole** `_verify_checkpoints()` invocation is `executor.py:1519`, inside Path B after the `status == PASS` guard at `:1517` (definition at `:1811`). Checkpoint enforcement therefore does NOT run for parsed-task phases `[CODE-VERIFIED]` (spot-03 CONFIRMED).
- **Numbered-checkpoint contract.** `CHECKPOINT_HEADING_PATTERN` (`checkpoints.py:30-33`) accepts BOTH numbered `### T<PP>.<TT> -- Checkpoint:` and legacy `### Checkpoint:` via an optional regex group; `Checkpoint Report Path:` is matched by `CHECKPOINT_PATH_PATTERN` (`checkpoints.py:22-25`) `[CODE-VERIFIED]`. The runtime parser is dual-shape compatible. Stale legacy-only `### Checkpoint:` text remains in the Path B prompt (`process.py:188-195`) and the `verify-checkpoints` empty message (`commands.py:426`) — stale-but-harmless `[CODE-VERIFIED]`.
- **`sprint rerun-tasks` is ABSENT at HEAD.** A tree-wide grep for `rerun-tasks`/`rerun_tasks` returns zero matches; the `sprint` Click group registers exactly six subcommands — `run`, `attach`, `status`, `logs`, `kill`, `verify-checkpoints` (`commands.py:71/293/305/317/342/360`). The operator-memory note of a v4.3.0 `sprint rerun-tasks` does NOT correspond to anything at commit `9e864860` (package is v4.2.0). **Do not describe `rerun-tasks` as existing** `[CODE-VERIFIED]` (spot-03 RESOLVED). Closest extant recovery surface is `verify-checkpoints` (recovers checkpoint reports only, does not re-run tasks).
- **Partial/unused isolation.** Four-layer `IsolationLayers`/`setup_isolation` exists (`executor.py:106-182`) but is NOT called in the main loop; Path B sets only `CLAUDE_WORK_DIR`, Path A passes no isolation env (`executor.py:1303-1324`, `:1076-1115`) `[CODE-VERIFIED]`.
- **Path A turn-accounting gap.** `_run_task_subprocess` returns `turns_consumed=0` (turn counting wired separately), limiting `TurnLedger` accuracy for Path A (`executor.py:1111-1115`) `[CODE-VERIFIED]`.
- **Stubbed status/logs.** `SprintLogger` JSONL+Markdown writes are real, but `read_status_from_log`/`tail_log` are stubs ("not yet connected"), so the `status`/`logs` commands do not report live (`logging_.py:224-235`) `[CODE-VERIFIED]`.

**Public Interface (key signatures):**

```python
# sprint/executor.py
def execute_sprint(config: SprintConfig) -> SprintResult                  # (:1135-1757)
def execute_phase_tasks(phase, tasks, config, ledger, ...) -> list[TaskResult]  # (:927-1073) Path A
def _determine_phase_status(...) -> PhaseStatus                            # (:2067-2148)
def _verify_checkpoints(...) -> PhaseStatus                                # (:1811) Path-B only call at :1519

# sprint/models.py
class PhaseStatus(Enum): PASS|PASS_NO_SIGNAL|PASS_NO_REPORT|PASS_RECOVERED|PREFLIGHT_PASS|
                          PASS_MISSING_CHECKPOINT|INCOMPLETE|HALT|TIMEOUT|ERROR|SKIPPED  # (:211-270)
@dataclass SprintConfig(PipelineConfig): release_dir, state_dir, checkpoint_gate_mode, ...  # (:347-510)
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| §5.1 pipeline-core | import/inherit | `SprintConfig(PipelineConfig)`; reuses `Step`/`StepResult`/`DeferredRemediationLog`/`TrailingGateResult` (`sprint/executor.py:12-16`) `[CODE-VERIFIED]` |
| Tasklist bundle | file | Index + `phase-N-tasklist.md` files; `PHASE_FILE_PATTERN` (`config.py:15-26`) `[CODE-VERIFIED]` |
| `tmux`, Rich | external | Optional `sc-sprint-<sha1>` session + `SprintTUI` Live render (`tmux.py:81-210`, `tui.py:98-152`) `[CODE-VERIFIED]` |
| `claude` CLI | subprocess | Via sprint `ClaudeProcess` → base `subprocess.Popen` (`pipeline/process.py:134`) `[CODE-VERIFIED]` |

**Consumers:**

| Used By | How |
|---------|-----|
| `superclaude sprint run` | CLI orchestration entry (`commands.py:189`) `[CODE-VERIFIED]` |
| `manifest.json` / `execution-log.jsonl` | End-of-sprint artifacts (`executor.py:1702-1725`) `[CODE-VERIFIED]` |

**Conventions & Patterns:**

- Result-file sentinels (`EXIT_RECOMMENDATION: CONTINUE|HALT`, `status: PASS|FAIL|PARTIAL`) are authoritative control-plane evidence, not backlog metadata (`executor.py:1774-1808`) `[CODE-VERIFIED]`.
- Checkpoints are a filesystem protocol embedded in markdown tasklists (path declarations + manifest), not a database (`checkpoints.py:36-408`) `[CODE-VERIFIED]`.
- **`[DESIGN — UNBUILT]`** Port posture is **hybrid-first** (hardest port surface): keep the Python sprint runner as execution authority; evaluate Mastra as a supervisory/workflow layer and Backlog.md/Beads as task-state/dependency mirrors. Mastra agent-approval does not replace process-group lifecycle, file-tail watchdogs, tmux IPC, or stream-json telemetry; a faithful port must preserve deterministic phase/task discovery, result-file freshness, checkpoint manifest, process-group termination, and exit-code propagation. Per-task vs freeform Path A/B divergence should be normalized or consciously preserved before adding a framework. Feasibility per research file 03 §8; not implemented.

---

**Status: Complete**
