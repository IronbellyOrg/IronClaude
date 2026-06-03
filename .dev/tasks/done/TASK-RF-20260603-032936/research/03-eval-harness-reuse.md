# Research: Eval Harness Reuse

Status: Complete
Date: 2026-06-03

---

## 1. The two distinct eval systems (critical framing)

There are TWO unrelated eval mechanisms in this repo, and the sc-recommend
`--eval` flag wants the *lightweight* one, not the heavyweight CLI harness.

### System A — `src/superclaude/cli/eval/` (the "cliEval" real-eval harness)

A heavyweight, PTY-driven, **real subprocess** eval harness. It spawns actual
`claude` CLI processes inside isolated `$HOME` sandboxes via a PTY, drives them
with an expect-style DSL, captures artifacts, and aggregates a `RunSummary`.
This is roadmap COMP-001..009 (deliverables D-0004..D-0060). Evidence:

- `orchestrator.py:1-13` — "parallel eval scheduler" using
  `ThreadPoolExecutor + as_completed`, mirrors `cli/prd/executor.py:774-802`.
- `isolation.py` (34 KB) `HomeIsolation` / `containment_guard` — per-eval
  `$HOME` sandbox.
- `pty_driver.py` / `pty_stream.py` / `claude_process.py` (`ClaudeProcessAdapter`)
  — spawn + drive a real `claude` binary over a PTY.
- `expect.py` (31 KB) `Expect`, `PRIMITIVE_NAMES` — the assertion DSL run
  against captured terminal output.
- `loader.py` — `SuiteLoader.load()` parses `suites/*.yaml` → `ParsedSuite`
  (jsonschema Draft 2020-12 against `suites/suite.schema.json`).
- `models.py` (41 KB) — `EvalSpec`, `EvalOutcome`, `RunSummary`, `RunCounts`,
  `RunTotals`, `ExpectResult`.
- `run_report.py` — `write_aggregated_report()` → `summary.md` / `summary.json`
  / `summary.yaml` / `junit.xml`.
- `commands.py` (75 KB) — the Click `eval_group` (`eval run`, `eval list`,
  `eval doctor`).
- `capabilities.py` / `config.py` / `coverage.py` / `retry.py` / `disk_budget.py`
  / `signal_handler.py` / `reporter.py` — supporting subsystems.

**This harness drives the local `claude` CLI; it does NOT have a notion of
"test opus vs sonnet vs haiku and pick a best_model".** Its `EvalSpec` has no
per-model fan-out axis. Reusing it for sc-recommend's `--eval` would require
threading a `--model` axis through `EvalSpec`, the runner, and the report — net
new code on a large, contract-heavy surface.

### System B — `.dev/eval-workspaces/sc-recommend/` (the skill-creator workspace)

The lightweight, file-based grading scaffold produced by the `skill-creator`
plugin's eval workflow. No subprocess spawning in the grader itself — subagents
are fanned out *by the orchestrating agent* (one Claude subagent per eval×config),
each writes `outputs/recommendation.md` + `timing.json`, then a plain Python
`grader.py` scores the markdown against JSON assertions and `build_benchmark.py`
aggregates. Evidence: `grader.py:32-48`, `build_benchmark.py:10-36`.

**This is the model the `--eval` flag should reuse.** It already has the exact
shape sc-recommend wants: per-case assertions (`must_appear` / `must_not_appear`
/ typed assertions), per-run `grading.json`, aggregate `benchmark.json` with
pass-rate/tokens/time means + stddev, and a with/without-skill delta.

### CONFLICT in the spec sources (must be resolved by the builder)

The two requirement docs disagree on which harness to reuse:

- `merged-requirements.md:259-269` ("CLI eval integration") says reuse
  **the `.dev` scripts** (`grader.py` / `build_benchmark.py`) and generate an
  iteration dir under `.claude/cache/eval-runs/iteration-<N>/`.
- `round-4-synthetic-eval-cases.md:16,24,54` says plugin evals run **via the
  cliEval harness** (`src/superclaude/cli/eval/`), adding suite YAMLs there.

Reading both closely: the **per-row `--eval` pipeline** (R3, `merged-requirements`)
should reuse the **`.dev` lightweight model** (Python grader + agent-spawned
subagents). The **plugin synthetic-eval pipeline** (R4) *aspires* to the cliEval
harness but, on inspection (§3 below), the cliEval harness cannot actually do
per-model panels or token aggregation, so the practical answer is the same:
extend the `.dev`-style Python grader, borrow only schema/precondition concepts
from cliEval. This conflict should be surfaced as a task decision point.

## 2. `.dev/eval-workspaces/sc-recommend/` scaffolding — verified shapes

### `evals.json` eval-case schema (`evals.json:5-92`)

Top-level: `{skill_name, schema_version:"1.0", notes, evals:[...]}`. Each eval:

```
id: int                       # 1..6
name: str                     # kebab-case slug
prompt: str                   # the user request fed to the subagent
expected_output: str          # prose intent (human-readable, not graded)
must_appear: [str]            # OPTIONAL — informational; NOT auto-graded
must_not_appear: [str]        # OPTIONAL — informational; NOT auto-graded
must_appear_one_of: [str]     # OPTIONAL — informational
assertions: [ {text, type, value} ]   # THE graded contract
files: []                     # seed files (unused in iter-1)
```

KEY FINDING: `must_appear` / `must_not_appear` / `must_appear_one_of` are
**documentation only** — `grader.py` never reads them. The *graded* contract is
the `assertions[]` array. Each assertion is `{text, type, value}`.

### `grader.py` assertion mechanism (`grader.py:11-29`)

`check(assertion, text)` dispatches on `assertion["type"]` against the raw
`recommendation.md` text. Supported types (the entire vocabulary):

| type | semantics (grader.py line) |
|---|---|
| `string_contains` | `value in text` (`:14-16`) |
| `string_not_contains` | `value not in text` (`:17-19`) |
| `regex_match` | `re.search(value, text, DOTALL|MULTILINE)` (`:20-22`) |
| `regex_match_not` | inverse of regex_match (`:23-25`) |
| `max_length_check` | `len(text) <= value` (`:26-28`) |

All five are **pure text assertions over a single markdown file**. No tool-use /
transcript inspection (that is the round-4 NEW work — see §5).

### `grade_run` + `grading.json` output schema (`grader.py:32-48`)

Reads `<run_dir>/eval_metadata.json` (the per-run assertion copy) and
`<run_dir>/outputs/recommendation.md`. Emits `grading.json`:

```
{ eval_id, eval_name, configuration, output_chars, output_exists,
  expectations: [ {text, passed: bool, evidence: str} ],
  pass_rate: float }          # passed / len(expectations)
```

`main()` (`:51-64`) globs `iteration-1/eval-*/{with_skill,without_skill}/`,
grades any dir containing `eval_metadata.json`, writes `grading.json` per run.

### Per-run input artifacts (verified on disk)

- `eval_metadata.json` — `{eval_id, eval_name, prompt, configuration,
  assertions:[...]}` (subset of the evals.json row; the canonical per-run copy
  the grader reads).
- `timing.json` — `{total_tokens, duration_ms, total_duration_seconds,
  tool_uses, summary}`. **This is the only source of token/tool-call data.** It
  is produced by the orchestrating agent that ran the subagent, NOT by any
  harness code. (verified: `eval-1/with_skill/timing.json`.)
- `outputs/recommendation.md` — the subagent's deliverable, the grading target.

### `build_benchmark.py` aggregation (`build_benchmark.py:10-95`)

Walks `eval-*/{with_skill,without_skill}/`, joins `grading.json` + `timing.json`
into per-run records (`:19-36`) with `result:{pass_rate, passed, failed, total,
time_seconds, tokens, tool_calls, errors}`. `stats()` (`:39-47`) computes
`{mean, stddev, min, max}`. `summarize(cfg, key)` (`:50-52`) groups by
configuration. Final `benchmark.json` (`:79-92`):

```
{ metadata:{skill_name, skill_path, executor_model, ..., runs_per_configuration},
  runs:[ per-run records ],
  run_summary:{ with_skill:{pass_rate,time_seconds,tokens (each {mean,stddev,min,max})},
                without_skill:{...},
                delta:{pass_rate, time_seconds, tokens} } }   # with − without
```

This is precisely the per-model aggregation `--eval` needs — except the grouping
axis is `with_skill|without_skill`, NOT `opus|sonnet|haiku`. Re-grouping by model
is a small change to `summarize()`'s key (`configuration` → `model`).

### `.dev/eval-workspaces/sc-reflect/grader.py` — richer assertion precedent

Cited by round-4 as the tool-use-log inspection precedent. Verified it has
`check_checkpoint_logged(assertion, base_dir)` (`:212-229`) which parses a JSONL
`audit_log` for a `checkpoint_name` — i.e. grades by reading a post-run log, not
just final text. Also `check_citation_resolves`, `check_regex_present/absent`,
`check_yaml_list_contains`, `check_matrix_covers_items`. This is the template
for round-4's `tool_use_present` / `tool_use_absent` assertion types.

## 3. cliEval harness (`src/superclaude/cli/eval/`) — per-file reuse verdict

For each key file: purpose, key exports, reusability for a per-row sc-recommend
`--eval` that spawns N parallel subagents per model and aggregates
pass-rate/tokens/duration.

| File | Purpose / key exports | Reusable for sc-recommend `--eval`? |
|---|---|---|
| `orchestrator.py` | `RunOrchestrator.run(specs, parallel)` — `ThreadPoolExecutor + as_completed` parallel scheduler; `EvalWorker = Callable[[EvalSpec], EvalOutcome]`; clamps `parallel∈[1,15]` (`:143-201`); `allocate_session_id` (`:96-110`). | **PARTIAL (pattern, not code).** The parallelism axis is *threads running local subprocesses*, not *Agent-tool subagents on different models*. sc-recommend's fan-out is done by the orchestrating Claude agent spawning N Agent calls in one message — there is no Python thread pool. Borrow the *shape* (pre-allocate slots, preserve order, one outcome per input) but do not call `RunOrchestrator` directly. |
| `runner.py` (48 KB) | `EvalRunner`, `run_eval`, `ExecutorContext`, `LifecycleExecutor`, `ObservedRun`, `ExpectCallable`. Drives a real `claude` over PTY inside an isolated HOME, runs expects, emits `EvalOutcome`. | **NO.** Hard-wired to PTY + `ClaudeProcessAdapter` + `HomeIsolation`. sc-recommend grades markdown the agent already produced; it never spawns `claude` subprocesses. |
| `loader.py` | `validate_manifest(path) -> list[EvalSpec]`; `SuiteLoader.load() -> ParsedSuite`; jsonschema Draft2020-12 against `suites/suite.schema.json`; `validate_eval_id` FR-SCH2 regex; capability resolution + parameterize expansion. | **CONCEPT-ONLY for per-row eval** (per-row evals are not YAML suites). **YES (reusable) for the round-4 PLUGIN synthetic-suite path** — plugin evals ARE suite YAMLs and want `SuiteLoader.load()` + schema validation. |
| `run_report.py` | `write_aggregated_report(summary, output_dir, emit_junit)` → `summary.md/json/yaml` (+ `junit.xml`); `render_summary_{markdown,json,yaml}`, `render_junit_xml`; `ReporterContractViolation` (N'-vs-K invariant). | **NO (as-is).** Consumes a `RunSummary` whose `EvalOutcome` has **no token field and no model field** (verified `models.py:337-345`). It cannot render the per-model pass-rate/tokens/duration table `--eval` needs. `build_benchmark.py`'s JSON shape is a better fit. Reuse only as a *stylistic reference* for markdown rendering. |
| `commands.py` (75 KB) | Click `eval_group` with `run` (`:1553`), `list` (`:924`), `doctor` (`:767`), `describe` (`:1205`). `--parallel` option, RAM precheck, run-dir = `.dev/eval-runs/<date>/<run-id>/` (`:1335`). `discover_suite_manifests`, `summarize_suites`, `build_doctor_report`. | **NO.** This is the `superclaude eval` CLI surface for the PTY harness. sc-recommend's `--eval` is a *flag on the `/sc:recommend` skill invocation* driven by an agent, not a `superclaude eval run` subcommand. Different entry point entirely. |
| `models.py` (41 KB) | `EvalSpec` (`:74`, fields: id/title/category/requires/timeout_sec/isolation/inputs/expects/parameterize/no_pty — **no model, no tokens**); `EvalOutcome` (`:292`, 9 fields, `duration_sec` but **no tokens/model**); `RunSummary`/`RunCounts`/`RunTotals`/`ExpectResult`. | **NO for the data model.** Neither `EvalSpec` nor `EvalOutcome` carries the model-panel axis or token counts sc-recommend's `best_model` selection requires. A fresh lightweight result model (mirroring `build_benchmark.py`'s per-run dict) is cleaner than retrofitting these frozen DM-001 contracts. |
| `config.py` | `EvalConfig` frozen dataclass; `resolve_scratch_root`; `SCRATCH_ROOT_POLICY`; `allowed_scratch_roots` defaults to `/tmp/eval-runs` + `.dev/eval-runs` (AC12). | **NO / FRICTION.** The allowlist does NOT include `.claude/cache/eval-runs/` (the spec's required output dir, `merged-requirements.md:263`). If any cliEval write-path were reused it would *reject* the spec's target dir. Confirms `--eval` should write directly, not through `resolve_scratch_root`. |
| `coverage.py` | `coverage_gate` — FR-G5 hook-matcher coverage gate (unrelated: checks every settings.json hook matcher has a covering eval). | **NO.** Out of scope — nothing to do with model panels or recommendation grading. |
| `retry.py` | `RetryOncePolicy` — NFR-REL2 retry-once for MCP-flaky-tagged evals. | **NO** (not needed; could *inspire* a re-run-on-flake for plugin evals, but not MVP). |
| `suites/` | 13 suite YAMLs + `suite.schema.json` + `README.md`. `model_capability_matrix.yaml`, `adversarial_merge_consistency.yaml` cited by round-4 as multi-model templates. | **CONCEPT.** See §4 — these do NOT spawn per-model harness runs; they delegate `--agents opus,sonnet,haiku` to `/sc:adversarial` inside ONE eval. `suite.schema.json` IS the schema the round-4 plugin suites extend. |
| `schemas/` | `summary.schema.json` (the `RunSummary` JSON contract) + `__init__.py`. | **NO.** Tied to `RunSummary`; not the per-row/per-model shape. |

### Entry point a new `--eval` pipeline would call

There is **no single reusable Python entry point** in `cli/eval/` that does
"spawn N subagents per model, grade, aggregate per-model, pick best_model." The
closest *callable* primitives worth importing:

- `loader.validate_manifest` / `SuiteLoader.load` — **only** for the round-4
  plugin synthetic-suite YAML path (schema-validate the generated suite).
- The `grader.check()` + `build_benchmark.summarize()/stats()` functions from the
  `.dev` scaffold — copy/adapt into a new `cli/sc_recommend/` module (the spec's
  `synthetic_cases.py` / a new `eval_pipeline.py`). NOTE: these `.dev` scripts
  live under `.dev/eval-workspaces/` which is dev-only scaffolding, NOT importable
  package code — they must be *ported* into `src/superclaude/cli/sc_recommend/`.

The new pipeline is fundamentally **agent-orchestrated** (the skill's cold-path
spawns Agent-tool subagents), with Python only for grading + aggregation +
best_model selection. The cliEval harness is Python-orchestrated subprocess
spawning — architecturally incompatible with the hot-path Haiku-subagent design.

`src/superclaude/cli/sc_recommend/` does NOT exist yet (verified) — it is net-new
per round-4's "Files Touched" table.

## 4. `--eval` modes + best_model selection: existing vs NEW

### Mode matrix (`merged-requirements.md:230-235`)

| Mode | Models tested | Runs/model | Total runs | ~Tokens | ~Wall time |
|---|---|---|---|---|---|
| `none` (default) | — | 0 | 0 | 0 | 0 |
| `quick` | opus | 1 | 1 | ~90K | ~70s |
| `normal` | opus + sonnet | 2 | 4 | ~360K | ~3 min |
| `deep` | opus + sonnet + haiku | 3 | 9 | ~810K | ~10 min |

Pipeline shape (`:237-246`): for each model in the panel → spawn N parallel
subagents on that model → each gets the same eval prompt (the triggering user
request) + the just-inserted row's `prompt_envelope_template` → produces the real
deliverable → grade against assertions → aggregate per-model pass-rate/mean
tokens/mean duration. For plugins: each model runs TWICE (with/without resource)
for the delta.

### best_model tier selection (`merged-requirements.md:248-257`) — deterministic

- `quality`: highest pass_rate; tie-break lower mean tokens.
- `speed`: lowest mean duration among models with pass_rate > 0.70 (quality floor).
- `cost`: lowest mean tokens among models with pass_rate > 0.70.
- `balanced` (default): normalize `(1−pass_rate)`, tokens, duration each to [0,1]
  across the panel; weighted sum 0.5/0.25/0.25; lowest score wins.
- `best_model.tier` records which tier was selected; default tier when `--eval`
  has no tier preference is `balanced`. (Future `--eval-tier` flag noted, NOT MVP.)
- `best_model.confidence` (risk #8, `:382`): eval delta vs runner-up; if < 0.5
  the hot-path hint is suppressed (row treated as model-agnostic).

### REUSABLE vs NEW for `--eval`

| Capability | Reusable from | NEW code required |
|---|---|---|
| Mode→model-panel→runs mapping table | — | NEW: a `MODE_MATRIX` dict (`none/quick/normal/deep`). ~10 LoC. |
| Spawn N parallel subagents per model | Pattern only (orchestrator.py shape; the sc-task Haiku-subagent precedent) | NEW: emitted as Agent-tool calls by the skill, one message per model panel. Behavioral (in SKILL.md), not Python. |
| Grade output vs assertions | **`.dev grader.py check()`** (5 assertion types) | Port into `cli/sc_recommend/`. |
| Per-run record {pass_rate, tokens, duration, tool_calls} | **`.dev build_benchmark.py:19-36`** | Re-group by `model` instead of `configuration`. |
| Mean/stddev/min/max stats | **`.dev build_benchmark.py:39-52` `stats()`/`summarize()`** | Reuse verbatim; change grouping key. |
| Per-model aggregation table | — | NEW: aggregate by model (the `.dev` script aggregates by with/without only). |
| best_model tier selection (4 deterministic rules + confidence + 70% floor) | — | **NEW (the core of R3).** ~40-60 LoC pure function. No precedent in repo. |
| Write `row-<key>-results.json` + patch lookup row `best_model`/`eval_history` | — | NEW: depends on the cache YAML reader/writer (researcher-01/04 surface). |
| `timing.json` token/duration capture | `.dev` convention (agent-written) | NEW: skill must instruct each subagent to emit `timing.json` (tokens not auto-captured by any harness). |
| Output dir `.claude/cache/eval-runs/iteration-<N>/` | — | NEW dir convention; cliEval `config.py` allowlist does NOT cover it (FRICTION noted §3). |

**Net:** `--eval` reuses the `.dev` *grading + stats* layer (ported), reuses the
parallel-fan-out *pattern* (not code), and writes NEW: the mode matrix, per-model
aggregation, the entire best_model tier-selection function, the results-JSON +
row-patch writer, and the timing-capture instruction in the subagent prompt.

## 5. Plugin synthetic-eval pipeline (round-4) — reuse map

Pipeline (`round-4:36-58`): Discovery → Stage 1 capability extraction (Haiku,
~3K) → Stage 2 synthetic case generation (Haiku/Sonnet, ~20-35K, emits cliEval
suite YAML) → Stage 3 mandatory user-review gate (eval-viewer HTML, no LLM cost)
→ commit approved suite to
`.claude/cache/eval-runs/synthetic-cases/<plugin-key>.yaml` → Stage 4 run via
`--eval` panels + adoption gate.

### Preconditions self-check schema (`round-4:124-135, 274-284`)

```yaml
preconditions:
  - kind: mcp_server_installed | binary_available | file_present
    server: <plugin-key>          # for mcp_server_installed
    binary: <name>                # for binary_available
    path:   <path>                # for file_present
    failure_mode: hard | warn | skip
    failure_message: <multiline help>
```

Checked BEFORE any eval runs. `mcp_server_installed` resolves via
`src/superclaude/cli/install_mcp.py:check_mcp_server_installed(server_name)`
(round-4 auggie finding #1 — verified-claimed; researcher-04 owns dispatch).

### Suite schema additions (`round-4:254-302`) — backward-compatible

Per-eval: `configuration: {with_resource|without_resource|both}` (default
`both`), `pair_id` (links without→with for delta), `capability` (grouping label).
Suite-level: `preconditions[]`, `adoption_gate{threshold_pass_rate_delta:0.10,
threshold_token_delta:-0.20, must_not_regress:[pass_rate], on_negative_verdict}`.
New assertion types: `tool_use_present` / `tool_use_absent` (with
`tool_name_pattern` regex).

### REUSABLE vs NEW for plugin eval

| Capability | Reusable from | NEW code required |
|---|---|---|
| Suite YAML format + load + schema-validate | **`cli/eval/loader.SuiteLoader` + `suites/suite.schema.json`** | NEW: schema delta (`configuration`, `pair_id`, `capability`, `preconditions`, `adoption_gate`, 2 assertion types) — ~50 LoC per round-4 table. |
| Seed fixture files into eval workspace | `cli/eval` `isolation: {home_strategy: seeded, seed_state}` **concept** | sc-recommend doesn't use PTY HOMEs; seed_state becomes agent-prompt context. Concept reuse only. |
| `mcp_server_installed` precondition | **`install_mcp.check_mcp_server_installed()`** (+ `check_binary_available`, `check_docker_available`, `check_prerequisites`) | NEW: a precondition runner that dispatches on `kind` and applies `failure_mode`. ~30 LoC. |
| Text assertions | **`.dev grader.py`** | reuse. |
| `tool_use_present/absent` (transcript JSONL grep) | **`.dev/eval-workspaces/sc-reflect/grader.py:check_checkpoint_logged`** (JSONL log parse precedent) | NEW: ~80 LoC transcript parser per round-4 table; requires persisting subagent tool-use transcript to a deterministic path. |
| with/without delta | **`.dev build_benchmark.py` delta block (`:66-76`)** | reuse — already computes with/without delta means. |
| adoption gate (delta thresholds, must_not_regress, verdict→row) | — | **NEW.** round-3 threshold logic; ~40 LoC. |
| User-review gate (eval-viewer HTML) | iteration-1 `eval-viewer.html` exists (119 KB at `iteration-1/`); round-4 wants a `generate_review.py --mode synthetic-case-review` | **`generate_review.py` does NOT exist** (verified: not found under `.dev/eval-workspaces`). The 119 KB `eval-viewer.html` is a static artifact, not a generator. NEW: `cli/sc_recommend/review_workflow.py` (~100 LoC per round-4) + a review-HTML generator. |
| Stage 1/2 generators (capability extraction, case gen) | — | **NEW: `cli/sc_recommend/synthetic_cases.py` (~150 LoC).** Agent-orchestrated Haiku/Sonnet calls. |

## Summary

Status: Complete

### One-paragraph answer

The repo has TWO eval systems. The heavyweight `src/superclaude/cli/eval/`
("cliEval") harness drives real `claude` CLI subprocesses over a PTY in isolated
HOMEs; its data model (`EvalOutcome`) carries **no token count and no model axis**,
its orchestrator parallelizes *threads/subprocesses* (not multi-model Agent
fan-out), and its report writer can't render a per-model best_model table. It is
therefore **not directly reusable** for sc-recommend's per-row `--eval`. The
lightweight `.dev/eval-workspaces/sc-recommend/` scaffold (`grader.py` +
`build_benchmark.py` + `evals.json`) is the right reuse target — it already grades
markdown against typed assertions and aggregates pass-rate/tokens/duration with
mean/stddev and a with/without delta. The builder should **port** that grading +
stats layer into a NEW `src/superclaude/cli/sc_recommend/` package (does not yet
exist), re-grouping the aggregation axis from `with_skill|without_skill` to
`opus|sonnet|haiku`, and write fresh: the mode matrix, the deterministic
best_model tier selection (the core R3 logic, no precedent), the results-JSON +
lookup-row patch writer, and the subagent timing-capture instruction. For the
round-4 PLUGIN synthetic-eval path, `cli/eval/loader.SuiteLoader` +
`suites/suite.schema.json` ARE reusable (plus a backward-compatible schema delta),
`install_mcp.check_mcp_server_installed()` satisfies the precondition self-check,
and `sc-reflect/grader.py:check_checkpoint_logged` is the template for the NEW
`tool_use_present/absent` transcript assertions.

### Master REUSABLE-vs-NEW table

| Concern | REUSE (path) | NEW (write fresh) |
|---|---|---|
| Markdown grading (5 assertion types) | **`.dev/.../grader.py:check()`** (PORT into package) | — |
| Per-run record + mean/stddev/min/max | **`.dev/.../build_benchmark.py:19-52`** (PORT) | re-group key `configuration`→`model` |
| with/without delta | **`.dev/.../build_benchmark.py:66-76`** | — |
| Parallel fan-out | `orchestrator.py` *pattern* + sc-task Haiku-subagent precedent | Agent-tool calls in skill (behavioral) |
| Mode matrix none/quick/normal/deep | — | `MODE_MATRIX` dict |
| Per-model aggregation | — | NEW (axis is model, not config) |
| best_model tier selection (quality/speed/cost/balanced + confidence + 70% floor) | — | **NEW — core R3, ~40-60 LoC** |
| Results JSON + row `best_model`/`eval_history` patch | — | NEW (uses cache YAML writer) |
| Token/duration capture | `.dev timing.json` convention (agent-emitted) | subagent prompt instruction |
| Output dir `.claude/cache/eval-runs/` | — | NEW (cliEval allowlist excludes it) |
| Plugin suite YAML load + schema-validate | **`cli/eval/loader.SuiteLoader`, `suites/suite.schema.json`** | schema delta ~50 LoC |
| Precondition self-check (`mcp_server_installed`) | **`install_mcp.check_mcp_server_installed()`** | precondition runner ~30 LoC |
| `tool_use_present/absent` assertions | **`sc-reflect/grader.py:check_checkpoint_logged`** (JSONL parse precedent) | transcript parser ~80 LoC |
| Adoption gate (delta thresholds → row) | round-3 thresholds (spec) | ~40 LoC |
| Stage 1/2 generators | — | `cli/sc_recommend/synthetic_cases.py` ~150 LoC |
| User-review gate | iteration-1 `eval-viewer.html` (static only) | `review_workflow.py` ~100 LoC + HTML generator (`generate_review.py` does NOT exist) |

### Load-bearing flags / decision points for the builder

1. **Spec conflict** (`merged-requirements.md:259-269` vs `round-4:16,24,54`):
   per-row `--eval` → `.dev` lightweight model; plugin eval → aspires to cliEval
   but practically also `.dev`-style. Resolve before building.
2. **cliEval `EvalOutcome` has no tokens/model field** (`models.py:337-345`) —
   the single most important reason the cliEval harness can't be reused as-is.
3. **`model_capability_matrix.yaml` does NOT do harness-level per-model fan-out** —
   it delegates `--agents opus,sonnet,haiku` to `/sc:adversarial` inside one eval
   (`:81`). Round-4 cites it as a template but it does not implement the panel.
4. **`config.py` scratch-root allowlist excludes `.claude/cache/eval-runs/`** —
   the spec's required output dir. Don't route `--eval` writes through
   `resolve_scratch_root`.
5. **`.dev/eval-workspaces/` scripts are dev scaffolding, not importable package
   code** — they must be ported into `src/superclaude/cli/sc_recommend/`.
6. **`generate_review.py` referenced by round-4 does not exist** — the user-review
   gate generator is fully NEW.
