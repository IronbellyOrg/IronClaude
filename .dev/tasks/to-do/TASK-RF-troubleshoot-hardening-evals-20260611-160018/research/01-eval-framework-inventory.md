# Research: Eval Framework Inventory

**Topic type:** File Inventory — the cli/eval framework to MIRROR
**Scope:** `src/superclaude/cli/eval/` (runner, pty_driver, orchestrator, models, config, reporter, run_report, exit_codes, isolation, loader, expect) + `schemas/` + `suites/`
**Status:** Complete
**Date:** 2026-06-11

---

## REUSABILITY VERDICT (TL;DR for builder)

A new differential-backtest harness under `tests/troubleshoot/backtest/` should:
- **IMPORT-REUSE (runtime, lives under src/):** the report writer pattern (`run_report.py` renderers + `_write_artifact_set`), `exit_codes` constants, `resolve_scratch_root`/`EvalConfig` (AC12 scratch policy if writing under scratch roots), the `models.py` dataclass *idioms* (frozen + `to_dict()` + invariant guard).
- **MIRROR-SHAPE (re-implement, not import):** `EvalRunner` (eval-spec-coupled), `PtyDriver` (Claude-CLI-coupled), `Orchestrator` (suite-coupled), `EvalSpec`/`RunSummary` schema (different domain: scenarios/escapes vs evals). These are tightly coupled to the Claude-CLI eval domain; a backtest harness replaying git commits has a different scenario model.
- **KEY PATTERN TO COPY:** the `run_report.py` triad — pure string renderers (`render_*`) + a single `_write_artifact_set` + invariant-guard-before-write. This is the cleanest model for the backtest catch-rate report (`backtest_status` ∈ not_run|partial|complete mirrors the `RunSummary.counts` accounting fields).

---

## Purpose

Catalog the public API surface a NEW differential-backtest harness (`tests/troubleshoot/backtest/`)
would mirror to build: (a) a per-escape-scenario runner, (b) a machine-readable report writer,
(c) scenario declaration. For each symbol: is it **import-reusable** vs **must re-implement in tests-only code**
(spec §4.7: reusable runtime logic under `src/`, test-only validators may live under `tests/`).

---

## FILE: `models.py` (41KB) — dataclass shapes (DM-001..DM-012)

The cleanest template-set in the framework. All dataclasses are `@dataclass(frozen=True)` with
explicit `_*_FIELDS` ordering tuples and a `to_dict()` that walks that tuple. **This idiom is the
recommended template for backtest scenario/report dataclasses (mirror-shape, do not import — domain differs).**

| Symbol | Signature / fields | Purpose | Reuse for backtest |
|---|---|---|---|
| `EvalStatus` (Literal) | `PASS,FAIL,ERRORED,TIMEOUT,INTERRUPTED,SKIPPED,XFAIL,XPASS` | status enum | mirror → backtest needs `MISS`/`CATCH` enum (E1–E5 outcomes) |
| `EVAL_STATUSES` | `tuple = get_args(EvalStatus)` (models.py:62) | runtime membership set | pattern: keep authoritative tuple in module scope |
| `SKIPPED_STATUSES`/`PASSED_STATUSES`/`FAILED_STATUSES` | `frozenset` (models.py:69-71) | status partitions for tally rollup | mirror — backtest partitions catch/miss/not_run |
| `EvalSpec` | frozen dc; fields: `id,title,category,requires,timeout_sec,isolation,inputs,expects,parameterize,no_pty` (models.py:74-144) | parsed manifest row + `from_dict(data)` classmethod | **MIRROR** → backtest `ScenarioSpec` (escape_id, target_commit, old/new expectation) |
| `ExpectResult` | frozen dc; `name,passed,message,details,duration_sec,failure` + `to_dict()` (models.py:147-201) | per-assertion outcome | mirror — per-escape assertion result |
| `ExpectFailure` | frozen dc; `eval_id,expect_id,expect_name,expected,actual,message,artifact_ref,traceback` + `to_dict()` (models.py:218-274) | failure detail record, explicit-ordered to_dict | mirror — diff record for a MISS/unexpected-CATCH |
| `EvalOutcome` | frozen dc; `eval_id,title,status,duration_sec,expects,skip_reason,skip_flag_triggered,artifacts,error_class` + `__post_init__` status-validation + `to_dict()` (models.py:292-381) | runner emission, one per eval | **MIRROR** → `ScenarioOutcome` (escape_id, old_status, new_status, verdict) |
| `EvalResult` | frozen dc; `eval_id,outcome,start,end,duration_sec,stdout,stderr,artifacts,error` + duration-from-timestamps `__post_init__` + `to_dict()` (models.py:399-497) | reporter-facing wrapper around EvalOutcome | mirror if backtest captures stdout/stderr per replay |
| `_render_error(error)` | `(BaseException|None) -> {type,message}|None` (models.py:500) | JSON-safe exception render | **import-reusable helper pattern** (copy) |
| `EvalContext` | frozen dc, 15 fields incl `eval_spec,home,home_path,run_dir,env,exit_code,stdout,stderr,...` + `from_runner_state(**kw)` classmethod (models.py:539-726) | runtime view passed to assertions | MIRROR only the relevant subset; tightly Claude-CLI-coupled |
| `RunCounts` | frozen dc; `manifest_n,expanded_n_prime,kept_k,skipped_s,kept_plus_skipped_equals_n_prime` + `to_dict()` (models.py:741-780) | row accounting; invariant kept+skipped==n' | **MIRROR DIRECTLY** → backtest counts: total_escapes, replayed, catches, misses → drives `backtest_status` (not_run/partial/complete) |
| `RunTotals` | frozen dc; `passed,failed,skipped,errored,interrupted,timeout` + `to_dict()` (models.py:794-815) | per-status tally | mirror → catch/miss tally |
| `RunSummary` | frozen dc; 11 fields `run_id,started_at,finished_at,duration_sec,suite,manifest_version,parallel,counts,totals,evals,artifacts` + `__post_init__` count-invariant + `to_dict()` (models.py:835-946) | **the top-level report model** | **MIRROR DIRECTLY** → `BacktestSummary` is the analogue. `counts.kept_plus_skipped_equals_n_prime`-style derived invariant maps to `backtest_status` derivation per NFR-1 |

**Key takeaway:** `RunSummary` + `RunCounts` is the exact structural analogue of the backtest catch-rate
report. The `__post_init__` that re-derives `kept_plus_skipped_equals_n_prime` and raises on mismatch is
the model for deriving `backtest_status ∈ {not_run, partial, complete}` from counts (NFR-1).

---

## FILE: `exit_codes.py` (1.1KB) — canonical exit codes — **IMPORT-REUSABLE**

`SUCCESS=0, FAILURES=1, USAGE_ERROR=2, INTERRUPTED=3` (exit_codes.py:21-24). Exactly 4 canonical values
(design-spec §4). Note: INTERRUPTED=3, NOT 130. **Import directly** if the backtest harness needs a CLI exit
contract; otherwise mirror the 4-value discipline. `from superclaude.cli.eval import exit_codes`.

---

## FILE: `run_report.py` (16KB) — machine-readable report writer — **THE PATTERN TO COPY**

This is the user-named "run_report machine-readable pattern." Pure-function renderers + one consolidated
writer + invariant-guard-before-write. **Mirror-shape for the backtest report writer (domain differs: RunSummary→BacktestSummary).**

`__all__` (run_report.py:41-48): `REPORTER_CONTRACT_VIOLATION_EXIT_CODE, ReporterContractViolation, render_summary_markdown, render_summary_json, render_junit_xml, write_aggregated_report`.

| Symbol | Signature | Purpose | Reuse |
|---|---|---|---|
| `REPORTER_CONTRACT_VIOLATION_EXIT_CODE` | `int = exit_codes.USAGE_ERROR` (=2) (run_report.py:56) | exit code for report contract breach | import-reusable constant idiom |
| `ReporterContractViolation(RuntimeError)` | `__init__(*, expected, actual, run_id=None)` (run_report.py:67-93) | raised when len(evals)!=expanded_n_prime, BEFORE any write | **MIRROR** → raise when backtest counts disagree |
| `_check_invariant(summary)` | `(RunSummary) -> None` (run_report.py:96-108) | enforce N'-vs-K before write | **MIRROR** → guard backtest counts→status consistency |
| `render_summary_markdown(summary)` | `(RunSummary) -> str` (run_report.py:141) | human-readable summary.md body; calls `_check_invariant` first | **MIRROR** → backtest catch-rate .md |
| `render_summary_json(summary)` | `(RunSummary) -> str` (run_report.py:233) | wraps `summary.to_dict()` → JSON + trailing \n | **MIRROR** → machine-readable backtest report (the load-bearing artifact) |
| `render_junit_xml(summary)` | `(RunSummary) -> str` (run_report.py:259) | JUnit XML export | optional mirror (CI integration) |
| `render_summary_yaml(summary)` | `(RunSummary) -> str` (run_report.py:339) | YAML via `yaml.safe_dump(sort_keys=False)` | optional |
| `_write_artifact_set(out, *, summary, emit_junit, md_renderer=..., json_renderer=..., yaml_renderer=..., junit_renderer=...)` | `-> dict[str,Path]` (run_report.py:366) | **consolidated writer** — writes md/json/yaml always, junit if flag; injectable renderers | **MIRROR DIRECTLY** — single writer SoT |
| `write_aggregated_report(summary, output_dir, *, emit_junit=False)` | `-> Mapping[str,Path]` (run_report.py:413) | top-level entry: guard-then-write under output_dir | **MIRROR DIRECTLY** → `write_backtest_report(summary, output_dir)` |

**Pattern essence (copy this shape):**
1. Pure renderers `render_*(summary) -> str` (each calls `_check_invariant` first → no partial output past a broken invariant).
2. `to_dict()` on the frozen model is the single serialization SoT; JSON/YAML wrap it.
3. One `_write_artifact_set` does the filesystem I/O; renderers are injected as callables.
4. `write_aggregated_report` is the operator entry point.

---

## FILE: `reporter.py` (8KB) — class-shaped Reporter wrapper — mirror-optional

`__all__`: `AggregatedRunReport, REPORTER_CONTRACT_VIOLATION_EXIT_CODE, Reporter, ReporterContractViolation, render_summary_yaml`.

- `Reporter` (frozen `@dataclass`, reporter.py:93-196): fields `summary: RunSummary`, `emit_junit: bool=False`.
  Methods: `to_markdown()/to_yaml()/to_json()/to_junit() -> str` (each delegates to the matching `render_*`),
  and `write(output_dir) -> Mapping[str,Path]` (delegates to `_write_artifact_set` with instance-method renderers).
- `AggregatedRunReport = Reporter` alias (reporter.py:202).
- Pattern ref it mirrors: `src/superclaude/cli/sprint/executor.py:190-335` (`AggregatedPhaseReport`) — see R3/R7.
- **Verdict:** the class wrapper is optional sugar; the function-level `run_report.py` writer is the load-bearing piece. A backtest harness can skip the class and just call `write_*` functions.

---

## FILE: `config.py` (12KB) — EvalConfig + scratch-root allowlist — import-reusable IF writing under scratch roots

`__all__`: `DEFAULT_MIN_CLAUDE_VERSION, EvalConfig, SCRATCH_ROOT_POLICY, SCRATCH_ROOT_VIOLATION_EXIT_CODE, ScratchRootViolation, format_scratch_root_violation, resolve_scratch_root`.

| Symbol | Signature | Purpose | Reuse |
|---|---|---|---|
| `EvalConfig` | frozen dc; `paths: Mapping[str,Path]={}, defaults: Mapping[str,object]={}, allowed_scratch_roots: tuple[Path,...]=(/tmp/eval-runs, .dev/eval-runs), min_claude_version=(0,5,0)` (config.py:85-107) | harness config | import if reusing scratch policy; else mirror minimal |
| `resolve_scratch_root(path, *, config=None, output_dir=None)` | `-> Path` (config.py:165) | AC12 allowlist gate, single ingress for scratch writes; H4: rejects bare-prefix paths | **import-reusable** if backtest writes under `/tmp/eval-runs` or `.dev/eval-runs`. Worktrees (R3) live elsewhere → may not apply |
| `ScratchRootViolation(Exception)` | `__init__(path, resolved, allowed)` (config.py:121) | escape-of-allowlist error | import with resolve_scratch_root |
| `SCRATCH_ROOT_VIOLATION_EXIT_CODE` | `=USAGE_ERROR` (=2) (config.py:115) | exit code | import-reusable |
| `format_scratch_root_violation(exc)` | `-> str` (config.py:251) | render violation + policy text | import with above |
| `SCRATCH_ROOT_POLICY` | `str` const (config.py:42) | policy paragraph | reuse if reusing the gate |

**Verdict:** backtest harness uses git worktrees (per R3) which may be outside these scratch roots; treat `resolve_scratch_root` as import-reusable only if writing the report under `.dev/eval-runs`. Otherwise the `EvalConfig` shape is a mirror template.

---

## FILE: `runner.py` (48KB) — per-eval runner + lifecycle — **MIRROR-SHAPE (Claude-CLI-coupled)**

`__all__` (runner.py:64-71): `EvalRunner, ExecutorContext, ExpectCallable, LifecycleExecutor, ObservedRun, run_eval`.

| Symbol | Signature | Purpose | Reuse for backtest |
|---|---|---|---|
| `ExpectCallable` (type alias) | `Callable[[EvalContext], ExpectResult]` (runner.py:82) | assertion fn contract | mirror → `Callable[[ScenarioContext], AssertionResult]` |
| `ExecutorContext` | frozen dc; `eval_spec,home,home_path,run_dir,artifacts_dir,stdout_path,stderr_path,transcript_path,env` (runner.py:85-106) | post-isolation runtime state for executor | mirror subset |
| `ObservedRun` | frozen dc; `exit_code,stdout,stderr,duration_sec,jsonl_paths,artifacts` (runner.py:109-133) | result of spawn→inject→observe | **MIRROR** → `ReplayResult` (the captured output of replaying a commit) |
| `LifecycleExecutor` (Protocol) | `spawn(ctx)->None; inject(ctx)->None; observe(ctx)->ObservedRun` (runner.py:136-156) | strategy for the run steps; **tests substitute a stub returning canned ObservedRun** | **MIRROR THE PROTOCOL SEAM** → this is the exact injectable seam a backtest replaces with "checkout commit + run old/new protocol" |
| `run_eval(spec, *, home, config, run_dir, artifacts_dir, stdout_path, stderr_path, transcript_path, executor, expect_callables=(), deploy_hooks=..., on_teardown_error=None, keep_home_on_pass=False) -> EvalOutcome` | (runner.py:179-194) | 7-step FR-LC1 lifecycle skeleton; classifies non-KI/SE exceptions as ERRORED | **MIRROR** → `replay_scenario(...)` skeleton. Note KeyboardInterrupt/SystemExit re-raised; all else → ERRORED outcome |
| `EvalRunner` | class; ctor keyword-only: `home, config, executor, run_dir, artifacts_dir, stdout_path, stderr_path, transcript_path, expect_callables=(), deploy_hooks=..., keep_home_on_pass=False, default_timeout_sec=None, clock=time.monotonic, cancellation_token=None, retry_count=0, retry_policy=None, home_factory=None` (runner.py:712-827) | wraps `run_eval` + JSONL logging + timeout + retry-once | **MIRROR** → `BacktestRunner.run(scenario) -> ScenarioOutcome`. Single public method `run(spec)->EvalOutcome` (runner.py:833) |
| `EvalRunner.run(spec) -> EvalOutcome` | (runner.py:833) | the one public method; delegates to `_execute_once`, applies retry policy | **MIRROR** — clean single-entry API to copy |
| `EvalRunner.DEFAULT_RETRY_COUNT=0`, `EVENT_*` ClassVars | (runner.py:741-762) | JSONL event-name constants; NFR-REL2 retry guard rejects retry_count!=0 | mirror the event-name-constant idiom for the replay JSONL log if needed |

**Verdict:** `EvalRunner`/`run_eval` are the structural template for the backtest runner but are coupled to
`HomeIsolation`, `deploy_hooks`, Claude subprocess lifecycle. **Re-implement** the runner in tests-only code
(or under `src/` if spec §4.7 requires the replay logic to be reusable runtime). The single most valuable
import-pattern is the **`LifecycleExecutor` Protocol seam** — define a `ReplayExecutor` Protocol so the
backtest can stub "checkout pre-fix commit → run protocol → capture verdict" and unit-test the harness
without real git checkouts.

---

## FILE: `pty_driver.py` (16KB) — pexpect wrapper for Claude CLI — **MIRROR-SHAPE / likely NOT needed**

`__all__` (pty_driver.py:58-65): `DEFAULT_PROMPT_READY_PATTERN, PtyDriver, PtyDriverError, PtyDriverTimeout, PtyDriverNotStarted, PtyDriverEOF`.

| Symbol | Signature | Purpose |
|---|---|---|
| `PtyDriver(command, *, env=None, cwd=None, prompt_ready_pattern=DEFAULT_PROMPT_READY_PATTERN, default_timeout=30.0, encoding="utf-8", dimensions=(40,120))` | (pty_driver.py:130-160) | wraps `pexpect.spawn`; ctor does NOT spawn |
| `.spawn()` (pty_driver.py:167) | launch child via pexpect | idempotent after exit |
| `__enter__/__exit__` (pty_driver.py:191-195) | context manager | |
| `.is_alive()`, `.pid()`, `.exit_code()`, `.fileno()` | accessors (pty_driver.py:204-427) | |
| `.expect_prompt_ready(timeout=None) -> str` (pty_driver.py:224) | wait for Claude prompt frame | |
| `.inject_prompt(text) -> None` (pty_driver.py:270) | type a prompt | |
| `.write_stdin(data) -> int` (pty_driver.py:291), `.read_stdout(size=-1, timeout=None) -> str` (pty_driver.py:305) | raw IO | |
| `.wait_exit(timeout=None) -> int` (pty_driver.py:334), `.terminate(force=False)` (pty_driver.py:390), `.close()` (pty_driver.py:400) | lifecycle | |
| `DEFAULT_PROMPT_READY_PATTERN = r"[>$] *\r*\n"` (pty_driver.py:75) | prompt-ready regex | |
| Exception hierarchy: `PtyDriverError` < `PtyDriverTimeout`/`PtyDriverNotStarted`/`PtyDriverEOF` (pty_driver.py:78-90) | | |

**Verdict:** `PtyDriver` exists to drive an interactive Claude Code TUI session. A differential backtest that
replays git commits and asserts protocol MISS/CATCH almost certainly does **not** need a PTY at all — it runs
the H0–H5 gate logic against a checked-out tree, not an interactive `claude` session. **Mirror only if** a
scenario must literally drive `claude` interactively; otherwise SKIP `PtyDriver`. User asked to "mirror PtyDriver"
— interpret as *mirror the spawn→observe driver seam*, realised as the `LifecycleExecutor`/`ReplayExecutor`
Protocol, not necessarily a real pexpect PTY.

---

## FILE: `orchestrator.py` (17KB) — parallel scheduler — **MIRROR-SHAPE (clean, low-coupling)**

`__all__` (orchestrator.py:86): `RunOrchestrator, EvalWorker, allocate_session_id`.

| Symbol | Signature | Purpose | Reuse |
|---|---|---|---|
| `EvalWorker` (type alias) | `Callable[[EvalSpec], EvalOutcome]` (orchestrator.py:93) | worker contract | mirror → `Callable[[ScenarioSpec], ScenarioOutcome]` |
| `allocate_session_id(*, run_id, eval_id) -> str` | returns `f"sess-{run_id}-{eval_id}"` (orchestrator.py:96-110) | deterministic session id | mirror if backtest needs run-scoped ids |
| `RunOrchestrator(*, run_one: EvalWorker, cancellation_token=None, disk_budget_poller=None)` | (orchestrator.py:113-158) | **ThreadPoolExecutor scheduler**; folds worker exceptions → ERRORED; never re-raises | **MIRROR** → `BacktestOrchestrator` if E1–E5 replay in parallel. Note: the orchestrator does NOT build runners — caller passes a `run_one` closure (clean seam) |
| `RunOrchestrator.run(specs, *, parallel=8) -> list[EvalOutcome]` | (orchestrator.py:164-169) | run all specs in parallel, preserve input order; clamps parallel to [1,15] | **MIRROR** → returns one outcome per scenario in order |
| ClassVars `DEFAULT_PARALLEL=8, MIN_PARALLEL=1, MAX_PARALLEL=15` (orchestrator.py:143-145) | concurrency bounds | mirror or simplify (5 escapes → small N) |

**Verdict:** the cleanest mirror target. The `run_one` closure seam (orchestrator owns scheduling only; caller
owns resource allocation) is the pattern to copy. For only 5 escapes (E1–E5), the backtest may run sequentially
and skip the orchestrator entirely — but the `run_one: Callable[[Spec], Outcome]` indirection + "worker
exception → ERRORED outcome, never re-raise" discipline is worth mirroring for robustness.

---

## FILE: `loader.py` (25KB) — manifest validation + scenario declaration loader — **MIRROR-SHAPE**

`__all__` (loader.py:47-63): `CapabilityResolver, EVAL_ID_REGEX, INVALID_EVAL_ID_EXIT_CODE, InvalidEvalId, ParsedSuite, PermissiveCapabilityResolver, SCHEMA_ERROR_EXIT_CODE, SUITE_LOADER_ERROR_EXIT_CODE, SchemaError, SuiteLoader, SuiteLoaderError, UNRESOLVED_CAPABILITY_EXIT_CODE, UnresolvedCapability, validate_eval_id, validate_manifest`.

| Symbol | Signature | Purpose | Reuse |
|---|---|---|---|
| `validate_manifest(path) -> list[EvalSpec]` | (loader.py:298-321) | jsonschema-validate a `suites/*.yaml` then `EvalSpec.from_dict` per entry; raises `SchemaError` | **MIRROR** → `load_scenarios(path) -> list[ScenarioSpec]` for declaring E1–E5 in a YAML/JSON manifest |
| `validate_eval_id(eval_id) -> None` | (loader.py:135) | FR-SCH2 path-traversal guard on ids (regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`) | mirror if escape-ids become FS paths; `E1`..`E5` already match |
| `SuiteLoader` | `@dataclass`; field `capability_resolver=PermissiveCapabilityResolver()`; method `load(path) -> ParsedSuite` (loader.py:454-494). 5-stage gate: read+schema → id-regex → capability-resolve → parameterize-expand → re-check id-regex | **MIRROR** → backtest loader: read scenarios + validate target-commit refs exist |
| `ParsedSuite` | frozen dc; `name, version, description, defaults, required_binaries, optional_capabilities, evals: tuple[EvalSpec,...], source_path` (loader.py:431-451) | the `load()` return shape (expanded) | **MIRROR** → `ScenarioSuite` |
| `CapabilityResolver` (Protocol) | `resolve(...)` (loader.py:383-411) | gate on env capabilities (git/binaries) | mirror → resolve "target commit reachable" / "git available" |
| `PermissiveCapabilityResolver` | (loader.py:414) | no-op resolver (everything available) | reuse pattern for a default |
| Exceptions `SchemaError`, `InvalidEvalId`, `UnresolvedCapability`, `SuiteLoaderError` + `*_EXIT_CODE=USAGE_ERROR(2)` (loader.py:66-75, 329-346) | typed load failures, all → exit 2 | mirror the typed-error-per-gate + single-exit-code idiom |

**Verdict:** the loader is the model for **scenario declaration (c)**. A backtest scenario manifest mirrors
the `evalEntry` shape but with backtest-specific fields (see schema below). Re-implement `validate_manifest`/
`SuiteLoader` because the schema differs; the gate-ordering discipline (validate BEFORE side effects) is the
reusable principle.

---

## FILE: `schemas/` — JSON-schema for the machine-readable report

`schemas/__init__.py` (`__all__`: `SUMMARY_SCHEMA_FILENAME, load_summary_schema`):
- `SUMMARY_SCHEMA_FILENAME = "summary.schema.json"`; `load_summary_schema() -> Mapping` loads via `importlib.resources`
  (works from wheels + editable installs). (schemas/__init__.py:25-44)
- `summary.schema.json` (8.6KB, DM-012): the contract `RunSummary.to_dict()` must satisfy; `write_aggregated_report` is the producer.
- **Pattern to copy:** ship a `backtest-summary.schema.json` alongside the backtest report writer + an
  `importlib.resources` loader so the machine-readable catch-rate report is schema-validated. **R7 covers modeling
  the catch-rate report from this** — this inventory just notes the `importlib.resources`-loaded-schema idiom + the
  `to_dict()`-is-the-producer / schema-is-the-contract / fidelity-test-asserts-match triad (test ref TEST-007).

---

## FILE: `suites/` — manifest examples (scenario-declaration reference)

- `suite.schema.json` (5.8KB): the `evalEntry` shape (suite.schema.json:124-159) is the scenario-declaration template:
  required `id` (FR-SCH2 `evalIdString` pattern) + `title`; optional `category, requires, timeout_sec, isolation, inputs, expects, parameterize, no_pty`.
- `eval_smoke.yaml`: the SIMPLEST manifest — top-level `name/version/description/defaults/required_binaries/optional_capabilities/evals`;
  each eval has `inputs:[{prompt:...}]` + `expects:[{stdout:{contains:...}},{exit_code:{equals:0}}]`. This YAML shape is the
  direct model for declaring E1–E5: id, title, the replay-target, and the OLD-MISS vs NEW-CATCH expectation pair.
- Other suites (`real.yaml` 86KB, `freshness_blocks_unread_edit.yaml`, `audit_wiring_guard.yaml`, etc.) are richer examples;
  `freshness_blocks_unread_edit.yaml` and `agent_grounding_drift.yaml` are the closest existing analogues to "assert a
  protocol/gate fires" — worth the builder pointing the implementer at as concrete prior art.

**Scenario-declaration model for the backtest (mirror, do not import):** a YAML manifest with per-escape entries
carrying `id (E1..E5)`, `title`, `target_commit` (pre-fix SHA — R5 covers the 5 commits), and a paired expectation
`{ old_protocol: MISS, new_gate: CATCH }`. Validate it with a re-implemented `validate_manifest`-style function +
a dedicated `backtest-suite.schema.json`.

---

## FILE: `__init__.py` — package public surface (import map)

The package re-exports everything import-reusable from one namespace: `from superclaude.cli.eval import (...)`.
Confirmed top-level exports relevant to a backtest harness (init.py:123-213):
- **Report writers (import-reusable as a pattern/SoT):** `write_aggregated_report, render_summary_json, render_summary_markdown, render_junit_xml, render_summary_yaml, Reporter, AggregatedRunReport, ReporterContractViolation, REPORTER_CONTRACT_VIOLATION_EXIT_CODE`.
- **Models (mirror-template):** `RunSummary, RunCounts, RunTotals, EvalOutcome, EvalResult, ExpectResult, ExpectFailure, EvalStatus, EVAL_STATUSES, PASSED/FAILED/SKIPPED_STATUSES, EvalSpec, EvalContext`.
- **Runner/orchestrator (mirror-shape):** `EvalRunner, run_eval, ExecutorContext, ObservedRun, LifecycleExecutor, ExpectCallable`. (`RunOrchestrator`/`EvalWorker`/`allocate_session_id` are NOT in package `__all__` — import from `.orchestrator` directly.)
- **Config/exit (import-reusable):** `EvalConfig, resolve_scratch_root, ScratchRootViolation, SCRATCH_ROOT_*`. (`exit_codes` constants imported as `from superclaude.cli.eval import exit_codes`.)
- **PTY (likely skip):** `PtyDriver, PtyDriver{Error,Timeout,NotStarted,EOF}, DEFAULT_PROMPT_READY_PATTERN, PtyStream`.
- **Loader (mirror-shape):** `SuiteLoader, ParsedSuite, validate_manifest, validate_eval_id, CapabilityResolver, PermissiveCapabilityResolver`.

Note: `RunOrchestrator` is defined in `orchestrator.py` with its own `__all__` but is **not** lifted into the
package `__init__.__all__` — a backtest that wants it must `from superclaude.cli.eval.orchestrator import RunOrchestrator`.

---

## §4.7 PLACEMENT GUIDANCE (src/ vs tests/)

Per spec §4.7 (reusable runtime logic → `src/`; test-only validators → `tests/`):
- **If the replay/gate-execution logic is reusable runtime** (e.g. the H0–H5 gate runner is production code the
  troubleshoot protocol already ships under `src/`), the backtest **imports** it and the harness scaffolding
  (scenario loader, report writer, runner skeleton) is the *test* that drives it → may live under `tests/troubleshoot/backtest/`.
- **The machine-readable report writer** (`render_*` + `_write_artifact_set` + `write_backtest_report`) and the
  `BacktestSummary`/`BacktestCounts` dataclasses are the gray area: if any non-test code consumes the catch-rate
  report, they belong under `src/`; if only the test asserts on them, `tests/` is acceptable. **Recommendation:**
  put the report MODEL + writer under `src/` (mirrors how `run_report.py`/`models.py` live under `src/`) and keep
  the scenario specs + pytest harness under `tests/troubleshoot/backtest/`. This satisfies §4.7 and matches the
  framework's own split (eval models/reporter under src/, eval *tests* under tests/cli/eval — R2's scope).

---

## STATUS: Complete

### Summary for the builder

The user named "EvalRunner + PtyDriver + the eval framework + run_report machine-readable pattern." Mapping to the
three backtest needs:

1. **(a) per-escape-scenario runner** → MIRROR `EvalRunner.run(spec)->EvalOutcome` + the `run_eval` 7-step
   skeleton + the `LifecycleExecutor` Protocol seam (runner.py:136-156, 712-878). The Protocol seam is the single
   most valuable thing to copy: it lets the backtest stub "checkout pre-fix commit → run OLD protocol → capture
   verdict" and "run NEW H0–H5 gate → capture verdict" as a `ReplayExecutor`, unit-testable without real git ops.
   PtyDriver itself is almost certainly NOT needed (no interactive Claude TUI in a git-replay backtest) — mirror
   the *driver seam*, not pexpect.

2. **(b) machine-readable report writer** → MIRROR the `run_report.py` triad EXACTLY (run_report.py:96-439):
   pure `render_*(summary)->str` renderers (each calls `_check_invariant` first) + one injectable-renderer
   `_write_artifact_set` + `write_aggregated_report(summary, output_dir)`. Back it with a frozen `BacktestSummary`
   dataclass whose `to_dict()` is the single serialization SoT (mirror `RunSummary`, models.py:835-946) and a
   `BacktestCounts` whose `__post_init__` derives/validates `backtest_status ∈ {not_run, partial, complete}`
   exactly like `RunCounts.kept_plus_skipped_equals_n_prime` (models.py:741-780, 905-921) — this is the NFR-1 mechanism.

3. **(c) scenario declaration** → MIRROR the `suite.schema.json` `evalEntry` shape + `validate_manifest`/`SuiteLoader`
   (loader.py:298-494, suite.schema.json:124-159). Declare E1–E5 in a YAML manifest (id, title, target_commit,
   {old:MISS, new:CATCH}); validate with a re-implemented schema + loader; ship a `backtest-suite.schema.json`
   loaded via `importlib.resources` (schemas/__init__.py pattern).

**Import-reusable (no re-implementation):** `exit_codes` (4 constants), `EvalConfig`/`resolve_scratch_root` (only if
writing under `/tmp/eval-runs` or `.dev/eval-runs`).

**Mirror-shape (re-implement; domain differs — evals vs escapes, Claude-CLI vs git-replay):** `EvalRunner`,
`run_eval`, `RunOrchestrator`, `PtyDriver`, `EvalSpec`/`RunSummary`/`EvalOutcome` schema, `SuiteLoader`/`validate_manifest`,
the `run_report.py` writer (copy the shape, new model).

**Single best pattern to internalize:** frozen dataclass + explicit `_*_FIELDS` ordering tuple + `to_dict()` walking
that tuple + `__post_init__` invariant guard + pure renderers that check the invariant before any write. This appears
in models.py and run_report.py and is the entire mechanical basis for a deterministic, schema-validated,
tamper-evident catch-rate report.

### Evidence note
All citations verified by direct Read of the source files on 2026-06-11. `RunOrchestrator` non-export from package
`__all__` verified against `__init__.py:123-213`. No claims left Unverified.
