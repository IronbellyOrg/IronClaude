# Research Notes: Sprint CLI per-task execution + handoff (Stages 0–3)

**Date:** 2026-06-03
**Scenario:** A (explicit — detailed BUILD_REQUEST + prior reflect audit)
**Depth Tier:** Deep
**Track Count:** 1
**Template:** 02 (complex — discovery + wire + test + verify phases)

> Build request: `.dev/tasks/BUILD-REQUEST-sprint-cli-wire-dead.md`
> Authoritative spec: `.dev/releases/backlog/sprint-cli-architecture-brainstorm/SYNTHESIS.md` (§3 skeleton; §6/§7 AUTHORITATIVE)
> Prior grounding: `.dev/reflect/pre-sprint-cli-arch-20260603002500/REPORT.md` + `artifacts/wave1a-grounding.md`

---

## EXISTING_FILES

Subsystem: `src/superclaude/cli/sprint/` (verified present). Load-bearing symbols (anchor on names, NOT lines — drift confirmed +4..+55):

- **executor.py** — `execute_sprint` (runtime fork ~L1264), `_parse_phase_tasks`, `execute_phase_tasks` (sequential per-task loop), `_run_task_subprocess` (thin prompt; returns `(exit_code, 0, output_bytes)` — turns hardcoded 0; no env_vars), `_subprocess_factory` (test injection seam — bypasses env_vars), `IsolationLayers` (dead dataclass; sets CLAUDE_SETTINGS_DIR), `setup_isolation` (dead; zero live callers), `_phase_env_vars` (Path A: CLAUDE_WORK_DIR=phase-copy dir), `aggregate_task_results`, `TurnLedger`. Comment "Turn counting wired separately in T02.06".
- **config.py** — `_TASK_HEADING_RE` (heading fork regex), `_DEPENDENCY_RE`, `SprintConfig` (add `task_parallelism`/`handoff_*` fields here), `task_output_file` → `phase-{N}-task-{task_id}` (collision evidence).
- **process.py** — `build_prompt` (monolithic phase-scoped, the prompt-composition surface for M3), `build_task_context` + `compress_context_summary` (dead context helpers to wire).
- **logging_.py** — `SprintLogger`, `_jsonl` (lock-free append), `write_task_rerun_complete` (EXISTING `task_rerun_complete` event — H3 reconciliation target).
- **checkpoints.py** — atomic temp+replace idiom (`tmp.write_text` → `tmp.replace`) to reuse for FileHandoffStore.
- **models.py** — `TaskResult` (+ `.to_dict`), `TaskEntry` (`.dependencies`), `resume_command` (emits dangling `--resume`).
- **rerun_tasks.py** — `walk_dependencies`/`_dependencies_of` (EXISTING `dependencies` consumer — reuse, don't re-derive).
- **commands.py** — `run()` click options (`--start`/`--end` phase-granular ints; add `--task-parallelism`/`--handoff`).

## PATTERNS_AND_CONVENTIONS

- Atomic write idiom: `checkpoints.py` temp+replace — the canonical pattern for one-file-per-task handoff.
- `SprintLogger` events via `_jsonl`; `write_task_rerun_complete` shows the existing per-task event shape (event/phase/task_id/status/turns/duration_sec).
- `TaskResult` is a dataclass with `.to_dict` — `HandoffRecord` extends it.
- Click options in `commands.py run()`; config fields on `SprintConfig` dataclass.
- UV-only (`uv run pytest`); src/ is source of truth, never edit `.claude/`.
- MDTM templates: **`src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`** (NOT `.claude/templates/` — that path is absent in this repo).

## GAPS_AND_QUESTIONS

- Exact existing test coverage of the dead code: `tests/cli/eval/test_isolation_layers_probe.py` pins `IsolationLayers`/`setup_isolation` API (COMP-012, T02.05); `tests/sprint/test_context_injection.py`, `test_state_dir_isolation.py` likely exercise context/isolation. Wiring must keep these green — researchers confirm what they assert.
- Existing task refs T02.05 (isolation API pin) + T02.06 (turn counting) — confirm scope so the tasklist reconciles, not duplicates.
- How `_subprocess_factory` is used by `test_executor.py` (the seam to extend for env capture).
- Whether `TurnLedger` already has any locking.

## RECOMMENDED_OUTPUTS

Research files under `research/`: 01-file-inventory, 02-patterns-conventions, 03-wiring-seams (integration points), 04-test-verification, 05-data-flow, 06-template-and-examples.

## SUGGESTED_PHASES

- **R1 File Inventory** — sprint CLI files: per-symbol export/signature/dead-or-live status. Scope: the 8 files above. Other researchers: R3 owns wiring seams, R5 owns data flow.
- **R2 Patterns & Conventions** — atomic-write, SprintLogger event shape, dataclass/`to_dict`, click/config patterns. Scope: checkpoints.py, logging_.py, models.py, commands.py, config.py.
- **R3 Integration Points / Wiring Seams** — the exact edit points: setup_isolation per-path merge (Path A `_phase_env_vars` vs Path B), build_task_context wiring, write_task_complete call site beside the wiring hook, `_subprocess_factory` env-capture seam, TurnLedger thread-safety surface. Scope: executor.py + process.py. Other researchers: R1 inventory only, R5 data flow.
- **R4 Test & Verification** — sprint test patterns + fixtures; how `_subprocess_factory`/`fake_claude` enable deterministic tests; what `test_isolation_layers_probe`/`test_context_injection`/`test_state_dir_isolation`/`test_wiring_integration` already assert; concurrency-test approach. Scope: `tests/sprint/`, `tests/cli/eval/`, `tests/integration/test_sprint_wiring.py`.
- **R5 Data Flow Tracer** — execute_sprint → fork → execute_phase_tasks → _run_task_subprocess; handoff write→read→resume flow; rerun_tasks dependency walk shape. Scope: executor.py, rerun_tasks.py.
- **R6 Template & Examples** — read `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (rules A3/A4/B2, L1-L6 handoff) + one recent `.dev/tasks/to-do/TASK-RF-*` example. Scope: templates + examples.

## TEMPLATE_NOTES

Template 02 (complex). Deep tier, 6 researchers, 0 web (Stage 4 agent-mail is out of scope and agent2 already did that web research). QA gates in generated tasklist: PER_PHASE. Testing: UNIT + INTEGRATION (the existing sprint test harness + fake_claude support both). Granularity: one item per wiring edit / per test / per flag.

## AUTHORITATIVE PATH A/B DEFINITION (gap-fill — rf-qa research gate, CRITICAL)

Per SYNTHESIS §H1 + verified source (`executor.py:1264-1330`). The builder MUST use this; research file 05 inverted the letters (corrected with a banner there):

- **Path A = per-phase single session** = the `else`/fallback branch (`executor.py:1309+`); the branch that **currently sets `CLAUDE_WORK_DIR=isolation_dir/phase-{N}`** (`executor.py:1327-1328`). H1: KEEP this `CLAUDE_WORK_DIR`, ADD only `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR`.
- **Path B = per-task** = the `if tasks:` branch (`executor.py:1265`) → `execute_phase_tasks` → `_run_task_subprocess`; **sets NO env today** (`executor.py:1101-1111`). H1: inject the full `setup_isolation` set.
- Anchor every item on **symbol + line** (`if tasks:` @1265, `_run_task_subprocess`, fallback `ClaudeProcess` @1309+), never the bare letter.

Builder must also add a one-line "Path A/B per SYNTHESIS §H1" definition to the tasklist's `## Execution Context`.

## AMBIGUITIES_FOR_USER

None blocking — scope (Stages 0–3) and authoritative source (§6/§7) are explicit. Stage 4 (agent-mail) and Stage C (coordinator) intentionally out of scope.
