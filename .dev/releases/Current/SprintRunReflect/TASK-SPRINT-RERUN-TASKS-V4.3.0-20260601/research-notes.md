# Research Notes: superclaude sprint rerun-tasks v4.3.0

**Date:** 2026-06-01
**Scenario:** A (explicit — TDD specifies file paths, function signatures, error layers, 8 ACs)
**Depth Tier:** Standard (single subsystem, ~1260 LOC, 6 files touched, 5-12 new test files)
**Track Count:** 1
**Template:** 02 (Complex — discovery → build → test → review per the 6 phases the user enumerated)

---

## EXISTING_FILES

**Sprint package (`src/superclaude/cli/sprint/`):**
| File | LOC | Role |
|---|---|---|
| `checkpoints.py` | 408 | **CANONICAL PATTERN** — `extract_checkpoint_paths`, `verify_checkpoint_files`, `build_manifest`, `recover_missing_checkpoints` + helpers `_nearest_heading`, `_extract_verification_block`, `_discover_phase_artifacts`, `_render_recovered_checkpoint` |
| `models.py` | 32KB / ~900 LOC | Dataclasses: `TaskEntry` (25), `TaskStatus` Enum (39), `TaskResult` (159), `PhaseStatus` Enum (211), `Phase` (282), `CheckpointEntry` (312), `PhaseResult` (523), `SprintResult` (559), `MonitorState` (623), `TurnLedger` (693), `ShadowGateMetrics` (837) |
| `commands.py` | 13.6KB | 6 existing Click subcommands at lines 71, 293, 305, 317, 342, 360 (`verify-checkpoints` at 360 — the natural sibling) |
| `executor.py` | 84.6KB | Main phase loop; `run_post_phase_wiring_hook` (748), `run_post_task_anti_instinct_hook` (803), phase_complete event emission at ~1605 |
| `config.py` | 18.6KB | `SprintConfig` + env-var defaults |
| `logging_.py` | 8.9KB | JSONL execution-log emission |

**New files to create:**
- `src/superclaude/cli/sprint/recovery.py` (~250 LOC; `RecoveryBundle` dataclass + state machine + SHA256 + lock file)
- `src/superclaude/cli/sprint/rerun_tasks.py` (~250 LOC; `extract_phase_subset` + dep walking + checkbox uncheck/restore)

**Test directory (`tests/sprint/`):** 14+ existing test files including `test_checkpoints.py`, `test_executor.py`, `test_cli_contract.py`, `test_config.py`, `test_e2e_halt.py`, `test_e2e_success.py`, `test_execute_sprint_integration.py`.

## PATTERNS_AND_CONVENTIONS

**Mirror target (canonical) — `checkpoints.py`:**
- snake_case module-level functions for public API (`extract_checkpoint_paths`, `verify_checkpoint_files`, `build_manifest`, `recover_missing_checkpoints`)
- Leading-underscore helpers (`_nearest_heading`, `_extract_verification_block`, `_discover_phase_artifacts`, `_render_recovered_checkpoint`)
- Returns structured intermediate dataclasses (CheckpointEntry, etc.)
- "Parse tasklist → manipulate structure → reconstruct" pipeline shape
- File-on-disk I/O via `pathlib.Path` not raw strings

**Dataclass conventions (`models.py`):**
- `@dataclass` with `field(default_factory=lambda: ...)` for mutable defaults
- Enum classes use `class XStatus(Enum)`; member values are lowercase strings
- `PhaseResult(StepResult)` inheritance pattern — `RecoveryBundle` should likely inherit StepResult too for shared timing fields
- TaskResult at line 159; add `task_results: list[TaskResult] = field(default_factory=list)` to PhaseResult (line 523)
- TaskStatus at line 39 — add `FAIL_RECOVERABLE = "fail_recoverable"` (keep enum-value style consistent)

**Click subcommand pattern (`commands.py`):**
- All subcommands attached to `@sprint_group.command()` decorator
- `verify-checkpoints` at line 360 is the natural sibling — read it as the structural model for `rerun-tasks`
- Use `--name UPPERCASE_TYPE` flag pattern; default values via `@click.option(default=...)`

## GAPS_AND_QUESTIONS

1. **`PhaseResult` persistence to `results/phase-N-result.json`** — does executor.py already write any per-phase JSON artifact? Need to check. The TDD specifies persisting `task_results` to this path; researchers should verify whether the path is greenfield or replaces an existing file.
2. **Lock file convention** — checkpoints.py uses no lock file pattern visible from the function list; researchers should check if there's a precedent elsewhere in the sprint package (e.g., process.py for sprint-level locks).
3. **SHA256 helper** — is there a sprint utility for SHA256 computation, or does each module use `hashlib` directly?
4. **MDTM template 02** — researcher should verify the template's L1-L6 handoff sections to ensure the generated task file uses them correctly.
5. **Lint/verify-sync commands** — `make lint` and `make verify-sync` are referenced; researchers should confirm these exist and what they validate.

## RECOMMENDED_OUTPUTS

5 parallel researchers:
| # | Topic | Scope | Output |
|---|---|---|---|
| 1 | File Inventory | `src/superclaude/cli/sprint/*.py` (19 files) | `research/01-file-inventory.md` |
| 2 | Patterns & Conventions | Deep read of `checkpoints.py` + samples from `commands.py` (verify-checkpoints), `models.py` (Phase/PhaseResult/TaskResult/Status enums), `executor.py` (phase loop signature) | `research/02-patterns-conventions.md` |
| 3 | Integration Points | `commands.py` Click subcommand wiring + `executor.py` phase-loop hook insertion points + `models.py` additive field placement + `logging_.py` event emission + `__init__.py` exports | `research/03-integration-points.md` |
| 4 | Test & Verification | `tests/sprint/test_checkpoints.py` (mirror pattern), `test_cli_contract.py` (CLI flag tests), `test_e2e_success.py` (integration test pattern), `conftest.py` (fixtures); identify how to structure 8 AC pytest tests + unit tests for each new module function | `research/04-test-patterns.md` |
| 5 | Template & Examples | `.claude/templates/workflow/02_mdtm_template_complex_task.md` (MDTM rules); `.dev/tasks/done/` recent task files for executable-implementation examples | `research/05-template-examples.md` |

No web research needed (Standard tier; codebase is fully self-contained).
No Doc Cross-Validator needed (TDD is the only doc and is fresh).
No Solution Research needed (TDD specifies the architecture).
No Data Flow Tracer needed (the data flow IS the TDD's RecoveryBundle state machine, already documented).

## SUGGESTED_PHASES

Per user prompt — 6 phases:
- **Phase 1:** Setup & data-model foundation (FAIL_RECOVERABLE enum, `PhaseResult.task_results` field, executor persistence to `results/phase-N-result.json`)
- **Phase 2:** Recovery abstraction (`recovery.py` + `RecoveryBundle` dataclass + state transitions + SHA256 + lock file)
- **Phase 3:** Task extraction & rerun engine (`rerun_tasks.py` + `extract_phase_subset` + dep walking + checkbox uncheck/restore)
- **Phase 4:** CLI integration (`commands.py` `rerun-tasks` subcommand + 9 flags + dry-run + verify-checkpoints auto-invoke)
- **Phase 5:** Test suite (AC1-AC8 + unit tests)
- **Phase 6:** Documentation + `make lint` + `make verify-sync` + final QA gate

PER_PHASE QA gates required (per BUILD_REQUEST). Post-completion 2-step at end.

## TEMPLATE_NOTES

- Template 02 (Complex) selected — multi-phase build with discovery → implementation → testing → review structure
- Item count: ~30-45 items expected (5-8 per phase × 6 phases)
- Use Execution Context block REQUIRED (per BUILD_REQUEST EXECUTION_CONTEXT_REQUIREMENTS); cite file:line evidence in per-item Context fields
- TB-Add-2 item-count bounds (≥3 ≤40 per track) — projected count is within bounds
- TB-Add-8 per-item Context evidence binding — every item touching code surface MUST cite file:line

## AMBIGUITIES_FOR_USER

None — user explicitly resolved the 4 prior open questions; TDD specifies file paths, function signatures, error layers, and 8 ACs. Builder has frozen inputs.
