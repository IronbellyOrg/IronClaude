---
id: "TASK-RF-20260518-cliEval-P2-loader-models-expect"
title: "cliEval Phase 2 — YAML loader + models + Expect.* DSL + eval list/describe"
description: "Build the declarative layer of the cliEval harness: YAML manifest loader, type-safe dataclass models, the Expect.* assertion DSL, JSON Schema for manifest validation, a minimal example suite, and the eval list/describe informational subcommands. This is Phase 2 of the cliEval release; Phase 1 (PTY + isolation + capability gates + eval_group skeleton) MUST be merged to master before execution begins."
status: "🟡 To Do"
type: "🛠️ Implementation"
priority: "🔼 High"
created_date: "2026-05-18"
updated_date: "2026-05-18"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: "cliEval-release"
depends_on:
- "TASK-RF-20260518-cliEval-P1-pty-isolation-gates"
related_docs:
- path: ".dev/releases/current/cliEval/design-spec.md"
  description: "Design spec — §3 directory layout, §5 manifest schema, §8 Expect.* DSL"
- path: ".dev/releases/current/cliEval/decisions.md"
  description: "Decisions log — D-2 (Expect.* port), D-4 (YAML registry + callback escape)"
- path: ".dev/releases/current/cliEval/build-requests/BUILD-REQUEST-cliEval-P2-loader-models-expect.md"
  description: "Originating build request with the 11 acceptance criteria (AC-P2.1 through AC-P2.11)"
- path: "src/superclaude/cli/prd/"
  description: "Reference sub-package layout — commands.py, config.py, executor.py, models.py shape to mirror"
tags:
- "cliEval"
- "Phase-2"
- "loader"
- "models"
- "expect-dsl"
- "yaml-schema"
- "click-subcommand"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "~350 LOC (models.py ~80, loader.py ~120, expect.py ~150, schema ~40, commands.py ext ~30, tests ~200)"
sprint: "cliEval-Phase-2"
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# cliEval Phase 2 — YAML loader + models + Expect.* DSL + eval list/describe

## Task Overview

This task implements Phase 2 of the cliEval release: the declarative layer that turns YAML manifests into executable, type-safe eval specifications and provides the assertion DSL that Phase 3's runner will invoke. It builds six new Python modules / schema files under `src/superclaude/cli/eval/`, extends `commands.py` with two informational subcommands (`eval list`, `eval describe`), and adds three test modules under `tests/cli/test_eval/`.

The 15 evals (E1-E15) defined in the design spec are authored declaratively as YAML per decision D-4 (YAML primary + Python callback escape hatch). This phase produces the parsing, validation, parameter-expansion, template-variable resolution, and assertion-DSL machinery that makes those manifests executable in Phase 3. Without this phase the orchestrator has nothing to schedule and the runner has nothing to assert against.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Type-safe data models:** `EvalSpec`, `EvalResult`, `RunSummary`, `ExpectFailure`, `ExpectResult`, and `EvalContext` dataclasses live in `src/superclaude/cli/eval/models.py` with round-trip-safe serialization and clear invariants.
2. **YAML manifest loader:** `src/superclaude/cli/eval/loader.py` parses suite YAML, validates against the JSON Schema, expands `parameterize:` blocks into separate `EvalSpec` instances (e.g., `E2.1`, `E2.2`, `E2.3`), and resolves the documented template variables (`{session_id}`, `{project_key}`, `{now - <duration>}`, `{home}`, `{eval_id}`). Invalid manifests raise `ManifestError` with file:line context.
3. **Expect.* assertion DSL:** `src/superclaude/cli/eval/expect.py` provides the `Expect` class with sub-builders (`FileExpect`, `JsonlExpect`, `SettingsExpect`, `ExitCodeExpect`, `StreamExpect`, `DurationExpect`) per design-spec §8; each builder returns an `ExpectCallable` of shape `(EvalContext) -> ExpectResult`.
4. **Manifest schema + example:** A draft 2020-12 JSON Schema at `src/superclaude/cli/eval/suites/suite.schema.json` plus an authoring guide `suites/README.md` and a 2-eval minimal-but-valid `suites/example.yaml` (NOT real.yaml — that is a downstream workstream).
5. **CLI surface — informational subcommands:** Extend `src/superclaude/cli/eval/commands.py` with `eval list` (enumerates `suites/*.yaml` with name/version/description/eval-count) and `eval describe --suite SUITE [--eval ID]` (prints parsed manifest content for the whole suite or a single eval).
6. **Test coverage:** Three test files — `test_models.py`, `test_loader.py`, `test_expect.py` — exercising dataclass invariants, valid/invalid manifest parsing, `parameterize:` expansion, template-variable substitution, and the PASS/FAIL paths for every Expect.* builder with observed-vs-expected failure messages.
7. **All eleven acceptance criteria green:** AC-P2.1 through AC-P2.11 from the BUILD_REQUEST must each be satisfied and traceable to a specific checklist item that produces or verifies their outputs.

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** cliEval-release (Phase 2 of 4 implementation phases per design-spec §17)
- **Blocking Dependencies:**
  - `TASK-RF-20260518-cliEval-P1-pty-isolation-gates`: provides `cli/eval/__init__.py` (exporting `eval_group`), `cli/eval/commands.py` (the `eval_group` Click group skeleton + `eval doctor` subcommand), `cli/eval/pty/` vendored driver, `cli/eval/isolation.py` (`HomeIsolation`), and `cli/eval/capability_gates.py`.

**CRITICAL — P1 must be MERGED to master before this task's execution begins.** This task extends `cli/eval/commands.py` (adds `eval list` and `eval describe` subcommands to the existing `eval_group` Click group) and presumes the `cli/eval/` sub-package layout exists. If P1 has not yet been merged, the executor MUST HALT at Step 1.3 (the merge verification gate) rather than scaffolding the package itself — that scaffolding is owned by P1 and recreating it here will create a merge conflict.

- **This task blocks:**
  - Phase 3 (`orchestrator.py` consumes `EvalSpec`/`EvalResult` models; `runner.py` invokes `Expect.*` callables on assertion lists; `reporter.py` consumes `RunSummary`).
  - The 15 real eval bodies (Wave 2 task files) — they author YAML against this loader and schema.

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

The actual checklist items for reading these files appear in Phase 1, Steps 1.4 and 1.5, and inline within Phase 2 build items per the self-contained pattern.

**Required Previous Stage Outputs:**

- **Design spec:** `.dev/releases/current/cliEval/design-spec.md` — §3 (directory layout, where each file lives), §5 (suite manifest schema, expected YAML fields and parameterize semantics), §8 (Expect.* DSL surface — class signatures and return shapes).
- **Decisions log:** `.dev/releases/current/cliEval/decisions.md` — D-2 (rationale for porting `mcp-eval`'s Expect.* idea without taking a dependency) and D-4 (YAML primary + Python callback escape).
- **Build request:** `.dev/releases/current/cliEval/build-requests/BUILD-REQUEST-cliEval-P2-loader-models-expect.md` — authoritative list of files to create, the 11 acceptance criteria, and the 3 open questions.
- **Reference sub-package:** `src/superclaude/cli/prd/` (notably `commands.py`, `config.py`, `executor.py`, `models.py`) — read for the conventional shape of a `cli/<subcommand>/` sub-package in this codebase.
- **Inspiration (no dependency):** `lastmile-ai/mcp-eval`'s `Expect.tools.*` API surface — mental model only; do NOT import or vendor anything from it.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-20260518-cliEval-P2-loader-models-expect/phase-outputs/`**

Subdirectories (pre-created by the build process):

- `discovery/` — manifest-schema field inventory, prd sub-package layout inventory, open-question resolutions
- `test-results/` — `uv run pytest` raw output and structured summaries; `make verify-sync` capture
- `reviews/` — QA gate verdicts (rf-qa structural reports)
- `plans/` — conditional fix plans when gates or tests fail
- `reports/` — final consolidated AC coverage report and run summary

These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:

- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Execution Context

<!-- Reader aid: source areas + key constraints for the executor; full evidence lives in per-item Context fields and research/* files. -->

- **References:** R-001 design-spec §3 / §5 / §8 (architectural authority for directory layout, manifest schema, and Expect.* DSL surface); R-002 decisions log D-2 / D-4 (architectural rationale for the DSL port and the YAML-primary registry); R-003 BUILD-REQUEST AC-P2.1 through AC-P2.11 (exhaustive acceptance criteria); R-004 prd sub-package (canonical shape for a Click-based subcommand sub-package in this codebase); R-005 P1 task file (dependency: sub-package skeleton owner — must be merged first).
- **Source areas:** the eval sub-package, the prd reference sub-package, the cliEval design and decisions docs, the cli main entry, the eval test directory, and the suites authoring area.
- **Key constraints:** P1 MUST be MERGED to master before execution; the executor HALTs at Step 1.3 otherwise. AC-P2.10 — all new pytest tests pass under `uv run pytest tests/cli/test_eval/...`. AC-P2.11 — `make verify-sync` MUST still EXIT=0 after the task completes. No new external Python deps beyond `jsonschema` (transitive) and `pyyaml` (already a dep). PER_PHASE QA gates (PG.1, PG.2, PG.3) are MANDATORY between Phase 2 → Phase 3, Phase 3 → Phase 4, and Phase 4 → Phase 5; fix cycles cap at 3 per gate per I16.

---

## Detailed Task Instructions

### Phase 1: Preparation, Dependency Verification, and Discovery

YOU MUST complete EVERY item in this phase IN ORDER before any code is written. Phase 1 establishes that P1 is merged, that the existing scaffold is what this task assumes, that the prd reference shape is internalized, and that the three open questions from the BUILD_REQUEST are resolved on the record.

**Step 1.1:** Update task status

- [ ] Update the frontmatter of this task file by setting `status` to "🟠 Doing", setting `start_date` to today's date in `YYYY-MM-DD` format, and setting `updated_date` to today's date, then add a timestamped entry to the ### Execution Log section of the ## Task Log / Notes at the bottom of this task file using the format `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.`, ensuring the frontmatter remains valid YAML and the execution log entry preserves any existing entries. Once done, mark this item as complete.

**Step 1.2:** Confirm handoff workspace exists

- [ ] Use Bash to run `ls -la /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260518-cliEval-P2-loader-models-expect/phase-outputs/` to verify the five subdirectories (`discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`) exist as pre-created by the build process, then if any subdirectory is missing create it with `mkdir -p`, ensuring all five directories are present and writable before any later item attempts to write into them. If the parent task directory itself is missing, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.3:** Verify Phase 1 (P1) is MERGED to master — MANDATORY HALT GATE

- [ ] Use Bash to run `cd /config/workspace/IronClaude && git log master --oneline --grep='cliEval' -n 20 && echo '---' && git ls-tree -r master --name-only | grep -E '^src/superclaude/cli/eval/(pty/|isolation\.py|capability_gates\.py|commands\.py|__init__\.py)' | sort` to confirm that P1's deliverables (`src/superclaude/cli/eval/pty/` vendored driver, `isolation.py` with `HomeIsolation`, `capability_gates.py`, `commands.py` exporting `eval_group`, and `__init__.py`) are present on `master`, then write a verification report to `phase-outputs/discovery/p1-merge-status.md` containing: the master HEAD SHA at check time, the list of P1 files found on master with their paths, the commit SHA(s) that landed P1, and a final verdict of either "VERIFIED — P1 is merged, P2 may proceed" or "BLOCKED — P1 not yet merged, P2 must halt", ensuring the verdict is derived strictly from the `git ls-tree` output (the listed P1 files must all be present on master) with no assumption that local working-tree state counts as "merged". IF the verdict is BLOCKED, update the frontmatter `status` to "⚪ Blocked" and populate `blocker_reason` with "P1 (cliEval Phase 1 — PTY + isolation + gates) is not yet merged to master; P2 cannot begin scaffolding work that P1 owns.", log the specific blocker using the templated format in the ### Phase 1 Findings section, and STOP all further work on this task. IF the verdict is VERIFIED, continue to Step 1.4. Once done, mark this item as complete.

**Step 1.4:** Inventory the prd reference sub-package shape

- [ ] Use Glob to list every Python file in `src/superclaude/cli/prd/` (pattern `src/superclaude/cli/prd/*.py`), then for each file use Read to extract: the module's top-level docstring (if any), the public classes/dataclasses defined (name + brief purpose), the public functions defined (name + signature), how Click commands/groups are declared (decorators used), and the typical import style (relative vs absolute), then write a structured inventory to `phase-outputs/discovery/prd-package-inventory.md` formatted as a markdown table with columns: File, Public Symbols, Click Pattern (if any), Import Style, and a free-form Notes column for conventions worth mirroring (e.g., dataclass usage, `pathlib.Path` for paths, `typing.Literal` for enums), ensuring every `.py` file in `cli/prd/` is included with accurate symbol names extracted directly from the source with no fabrication, and the Notes column captures concrete conventions (not vague summaries) that the cliEval P2 modules should follow. If unable to read files, log the specific blocker using the templated format in the ### Phase 1 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 1.5:** Extract the design-spec manifest-schema and Expect.* DSL contracts into a discovery doc

- [ ] Read `/config/workspace/IronClaude/.dev/releases/current/cliEval/design-spec.md` paying particular attention to §3 (directory layout — what files this task owns), §5 (the suite manifest schema YAML example, including `defaults:`, `required_binaries:`, `optional_capabilities:`, `evals:`, `parameterize:`, `requires:`, `expects:` with `type:` enum values like `file_exists`, `file_absent`, `jsonl_event`, `exit_code`, and `when:` ordering), and §8 (the Expect.* DSL Python interface — `FileExpect.exists/absent/has_mode/has_content_matching`, `JsonlExpect.contains_event/event_count/is_valid_jsonl`, `SettingsExpect.has_registration/hooks_count`, `ExitCodeExpect.equals/in_`, `StreamExpect.contains/does_not_contain/matches_line`, `DurationExpect.less_than/greater_than`), then read `.dev/releases/current/cliEval/decisions.md` D-2 and D-4 in full, then write a consolidated extraction to `phase-outputs/discovery/p2-contracts.md` containing: (a) the complete list of expect `type:` enum values that the YAML schema must accept, mapped to the Python `Expect.*` builder + method that implements each, (b) the complete list of template variables (`{session_id}`, `{project_key}`, `{now - <duration>}`, `{home}`, `{eval_id}`) with notes on which resolve at load time vs deferred to runtime, (c) the dataclass shapes the design implies for `EvalSpec`/`EvalResult`/`RunSummary`/`ExpectResult`/`ExpectFailure`/`EvalContext` with all fields and types, and (d) the `parameterize:` semantics (flat list of dicts → one EvalSpec per dict, IDs suffixed `.N`), ensuring every contract is quoted or paraphrased directly from the design spec with the specific section and line range cited, and any ambiguity surfaces explicitly with a flag like "AMBIGUOUS — see Open Question 3 below" rather than being silently resolved. If the design spec is unreadable, log the specific blocker using the templated format in the ### Phase 1 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 1.6:** Resolve the three Open Questions from the BUILD_REQUEST on the record

- [ ] Read the "Open questions for the executor" section of `/config/workspace/IronClaude/.dev/releases/current/cliEval/build-requests/BUILD-REQUEST-cliEval-P2-loader-models-expect.md` (Q1: `Expect.jsonl(...).contains_event(...)` matching semantics — strict vs fuzzy; Q2: `parameterize:` flat-only vs nested; Q3: template-variable resolution at load time vs deferred), then determine a defensible resolution for each by cross-referencing the design-spec §5 / §8 and decisions D-2 / D-4, then write a decision file `phase-outputs/discovery/open-questions-resolved.md` containing one section per question with: the question verbatim, the resolution chosen, the rationale citing the spec/decisions, and a short note on what the resolution implies for the loader/expect implementation (e.g., for Q1 strict matching means every supplied field is required to match exactly; for Q2 flat-only per the BUILD_REQUEST author's stated recommendation; for Q3 split — load-time for `{eval_id}` / `{project_key}` / `{home}` and deferred to runner for `{session_id}` / `{now - <duration>}`), ensuring each resolution is defensible against the spec and not invented, and any resolution that materially departs from the spec is escalated to an Open Questions entry rather than implemented unilaterally. If the BUILD_REQUEST is unreadable, log the specific blocker using the templated format in the ### Phase 1 Findings section, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Data Models, JSON Schema, and Example Manifest

Phase 2 lays the foundation that loader.py and expect.py depend on: the typed dataclasses, the schema the loader will validate against, and a minimal example manifest used by the loader and describe tests. Each item is a single deliverable file; no item in this phase touches loader.py or expect.py — those come in Phase 3.

**Step 2.1:** Create `cli/eval/models.py` — dataclasses (covers AC-P2.4 partial: model shape required by loader)

- [ ] Read the contracts discovery file `phase-outputs/discovery/p2-contracts.md` for the dataclass shapes the design spec implies (specifically the §3/§5/§8 extracts for `EvalSpec`, `EvalResult`, `RunSummary`, `ExpectFailure`, `ExpectResult`, and `EvalContext`), then read the prd inventory `phase-outputs/discovery/prd-package-inventory.md` for the conventions to mirror (dataclass style, `pathlib.Path` usage, `typing.Literal` for enums, `from __future__ import annotations` if present), then read `src/superclaude/cli/prd/models.py` (if it exists) as a concrete style reference, then create the file `src/superclaude/cli/eval/models.py` containing: a module docstring stating the purpose; `from __future__ import annotations`; the `EvalSpec` frozen dataclass with at minimum `id: str`, `title: str`, `category: str`, `requires: list[str]`, `timeout_sec: int`, `isolation: dict`, `inputs: list[dict]`, `expects: list[dict]` (raw expect specs from YAML; lowered into callables by loader), and `parameterize_params: dict | None` for parametric variants; the `ExpectResult` dataclass with `passed: bool`, `evidence: str`, `expect_type: str`; the `ExpectFailure` dataclass with `expect_type: str`, `expected: str`, `observed: str`, `location: str`; the `EvalContext` dataclass with `eval_id: str`, `session_id: str`, `home: pathlib.Path`, `run_id: str`, `tty_stdout: str = ""`, `tty_stderr: str = ""`, `exit_code: int | None = None`, `duration_sec: float = 0.0`; the `EvalResult` dataclass with `eval_id: str`, `status: Literal["PASS", "FAIL", "SKIP", "ERROR", "TIMEOUT", "XFAIL", "XPASS"]`, `duration_sec: float`, `expect_results: list[ExpectResult]`, `tty_log_path: pathlib.Path | None`, `home_path: pathlib.Path | None`, `error: str | None = None`; the `RunSummary` dataclass with `run_id: str`, `suite: str`, `started_at: str`, `duration_sec: float`, `parallel: int`, `totals: dict[str, int]`, `eval_results: list[EvalResult]`; an `ExpectCallable` type alias `= Callable[[EvalContext], ExpectResult]`; and a `ManifestError(Exception)` class with `file_line: str | None = None` for loader error reporting, ensuring all dataclasses are `@dataclass` (frozen where appropriate per immutability of specs vs mutability of results), all field types match the design spec §3 and §8, no fields are fabricated beyond what the spec calls for, and no placeholder TODOs remain. If the discovery files are missing, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** Create `cli/eval/suites/suite.schema.json` — JSON Schema draft 2020-12 for manifest validation

- [ ] Read the design-spec §5 YAML example at `.dev/releases/current/cliEval/design-spec.md` to identify every top-level and nested field name and type used in a suite manifest (`name`, `version`, `description`, `defaults` with `per_eval_timeout_sec`/`per_eval_memory_mb`/`capture_tty`/`keep_home_on_success`; `required_binaries` array of `{name, min_version?, failure_mode}`; `optional_capabilities` array of `{name, gate_flag?, failure_mode}`; `evals` array of objects with `id`, `title`, `category`, `requires`, `timeout_sec`, `isolation`, `inputs`, `expects`, optional `parameterize`, optional `callback`), then read the resolved expect-type enum from `phase-outputs/discovery/p2-contracts.md`, then create the file `src/superclaude/cli/eval/suites/suite.schema.json` containing a valid draft 2020-12 JSON Schema (`"$schema": "https://json-schema.org/draft/2020-12/schema"`) with: a top-level object requiring `name`, `version`, `description`, `evals`; `evals` as an array with `minItems: 1` and items conforming to an `EvalSpec` object schema; the `expects` field as an array of items whose `type` field is constrained to the enum `[file_exists, file_absent, file_mode, file_content_matches, jsonl_event, jsonl_event_count, jsonl_valid, settings_has_registration, settings_hooks_count, exit_code, exit_code_in, stderr_contains, stderr_does_not_contain, stdout_contains, duration_less_than, duration_greater_than]`; the `failure_mode` field constrained to `[hard, skip, xfail]`; the `parameterize` field if present constrained to an array of objects (flat per Q2 resolution); a `$defs` section factoring out the `EvalSpec` and `Expect` sub-schemas for clarity; and `"additionalProperties": false` on every object schema to catch typos in manifest authoring, ensuring every field type is sourced from the design spec §5 with no fabricated fields, the schema validates the §5 example as-written (mentally or by reference), and the expect-type enum exactly matches the resolved contracts in p2-contracts.md. If the design spec is unreadable, log the specific blocker using the templated format in the ### Phase 2 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** Create `cli/eval/suites/example.yaml` — 2-eval minimal-but-valid manifest

- [ ] Read the schema at `src/superclaude/cli/eval/suites/suite.schema.json` just authored, then read the design-spec §5 YAML example for the structural pattern, then create the file `src/superclaude/cli/eval/suites/example.yaml` containing a minimal-but-valid 2-eval suite with: `name: example`, `version: "1.0"`, `description: "Minimal example suite used by loader/describe tests; NOT real.yaml"`, a `defaults:` block with conservative values (e.g., `per_eval_timeout_sec: 30`, `capture_tty: false`), a `required_binaries:` array containing only `{name: claude, failure_mode: hard}` (kept minimal — the test loader does not actually invoke binaries), an empty or minimal `optional_capabilities: []`, and an `evals:` array with exactly two entries: (1) `E1` — a single eval with `title: "Example simple eval"`, `category: example`, `requires: []`, `timeout_sec: 10`, an `inputs:` array with one `{prompt: "hello"}` entry, and an `expects:` array with two entries `{type: file_exists, path: "{home}/.claude/marker.txt"}` and `{type: exit_code, value: 0}`; and (2) `E2` — a parameterized eval with `title: "Example parametric eval"`, `category: example`, `requires: []`, `timeout_sec: 10`, a `parameterize:` array with two entries `[{prefix: "a", value: 1}, {prefix: "b", value: 2}]`, an `inputs:` array with one `{prompt: "{prefix}"}` entry, and an `expects:` array with one `{type: file_exists, path: "{home}/.claude/marker-{eval_id}.txt"}` entry, ensuring the file YAML-parses cleanly, the manifest validates against `suite.schema.json` (the loader test will assert this), exactly two top-level evals are defined (loader will expand E2 into E2.1 and E2.2 — 3 EvalSpec instances total), and the file includes the standard `# yaml-language-server: $schema=./suite.schema.json` directive on line 1 for editor support. If unable to determine valid syntax, log the specific blocker using the templated format in the ### Phase 2 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 2.4:** Create `cli/eval/suites/README.md` — manifest authoring guide

- [ ] Read the schema at `src/superclaude/cli/eval/suites/suite.schema.json` and the example at `src/superclaude/cli/eval/suites/example.yaml`, then read the resolved Open Questions at `phase-outputs/discovery/open-questions-resolved.md` and the contracts at `phase-outputs/discovery/p2-contracts.md`, then create the file `src/superclaude/cli/eval/suites/README.md` containing a manifest authoring guide with sections: (1) Purpose — what a suite manifest is and how `eval run`/`eval describe`/`eval list` use it; (2) File Naming — `<suite-name>.yaml` under this directory, suite name matches `--suite` CLI flag; (3) Top-level Fields — `name`, `version`, `description`, `defaults`, `required_binaries`, `optional_capabilities`, `evals`, each with its purpose and a one-line example; (4) The `evals:` Entry Schema — every field (`id`, `title`, `category`, `requires`, `timeout_sec`, `isolation`, `inputs`, `expects`, `parameterize`, `callback`) documented with type and a usage example; (5) `parameterize:` Block — flat-list-only semantics per Q2 resolution, the substitution rules (every key in a parameter dict becomes a template variable inside that eval's strings), and the ID-suffix convention (`E2` with 3 params → `E2.1`/`E2.2`/`E2.3`); (6) `requires:` Capability Gates — list of capability names the eval needs; eval is SKIPped if any gate fails; (7) `expects:` Field Grammar — the full `type:` enum table from the schema with one row per type showing required fields and a usage example for each; (8) Template Variables — the resolution table per Q3 (load-time: `{eval_id}`, `{project_key}`, `{home}`; runtime: `{session_id}`, `{now - <duration>}`) with examples; (9) Validation — note that `eval run` and `eval describe` both invoke loader validation; errors include file:line, ensuring every documented field corresponds to a field actually present in the schema with no fabricated fields, and every example snippet is YAML-valid. If the schema or example file is missing, log the specific blocker using the templated format in the ### Phase 2 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 2.5:** Create `tests/cli/test_eval/test_models.py` — dataclass round-trip + invariants

- [ ] Read `src/superclaude/cli/eval/models.py` to know the actual dataclass shapes implemented in Step 2.1, then read the prd test directory (e.g., `tests/cli/test_prd/test_models.py` if it exists, otherwise `tests/cli/test_prd/` generally) for the conventional pytest style used in this project (assertion patterns, fixture style, imports), then create the file `tests/cli/test_eval/test_models.py` containing pytest test functions covering: (1) `test_eval_spec_construction` — construct an `EvalSpec` with all required fields and assert each field matches the input; (2) `test_eval_spec_is_frozen` — assert `EvalSpec` is a frozen dataclass (mutation raises `dataclasses.FrozenInstanceError`) if the design implies immutability; (3) `test_expect_result_pass` / `test_expect_result_fail` — construct PASS and FAIL `ExpectResult` instances and verify `passed` / `evidence` round-trip; (4) `test_eval_context_minimal` — construct `EvalContext` with minimum required fields and verify defaults populate correctly (e.g., `tty_stdout=""`, `exit_code=None`); (5) `test_eval_result_status_literal` — verify that `EvalResult.status` accepts each valid Literal value (`PASS`, `FAIL`, `SKIP`, `ERROR`, `TIMEOUT`, `XFAIL`, `XPASS`) by constructing one of each; (6) `test_run_summary_totals_shape` — construct a `RunSummary` with a `totals` dict containing `passed`, `failed`, `skipped`, `errored` and verify; (7) `test_manifest_error_carries_file_line` — construct a `ManifestError` with `file_line="example.yaml:42"` and verify the attribute round-trips, ensuring all tests use `pytest` directly (not unittest), no test is a placeholder or `pytest.skip`, every test references actual fields defined in models.py with no fabricated fields, and the test file's module docstring states "Tests for cli/eval/models.py dataclasses — round-trip + invariants (covers AC-P2.10 model portion)." If `models.py` is unreadable, log the specific blocker using the templated format in the ### Phase 2 Findings section, then mark this item complete. Once done, mark this item as complete.

### Phase Gate PG.1: QA Verification of Models + Schema + Example

This gate verifies that Phase 2's foundational artifacts (models.py, suite.schema.json, example.yaml, README.md, test_models.py) are internally consistent and faithful to the design spec BEFORE the loader and DSL build phases (which depend on them) begin. Fix cycles are capped at 3 per I16; on the third FAIL the executor MUST HALT and escalate to the user.

**Step PG.1.1:** Aggregate Phase 2 outputs for QA review

- [ ] Use Bash to run `ls -la /config/workspace/IronClaude/src/superclaude/cli/eval/models.py /config/workspace/IronClaude/src/superclaude/cli/eval/suites/suite.schema.json /config/workspace/IronClaude/src/superclaude/cli/eval/suites/example.yaml /config/workspace/IronClaude/src/superclaude/cli/eval/suites/README.md /config/workspace/IronClaude/tests/cli/test_eval/test_models.py 2>&1` to confirm all five Phase 2 artifacts exist on disk, then write an aggregation summary to `phase-outputs/reports/phase-2-artifacts.md` listing each artifact's absolute path, size in bytes, and a one-line claim of what it provides (e.g., "models.py — 6 dataclasses + ManifestError + ExpectCallable alias for the eval harness"), then list the source contracts each artifact must satisfy by referencing `phase-outputs/discovery/p2-contracts.md` and the design-spec §3 / §5 / §8, ensuring every artifact is listed with its actual on-disk size (not assumed), and any missing artifact is flagged as a Phase 2 incomplete blocker rather than aggregated. If any artifact is missing, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PG.1.2:** Spawn rf-qa for structural verification of Phase 2 outputs

- [ ] Spawn the `rf-qa` agent in `task-integrity` mode with the input file paths `src/superclaude/cli/eval/models.py`, `src/superclaude/cli/eval/suites/suite.schema.json`, `src/superclaude/cli/eval/suites/example.yaml`, `src/superclaude/cli/eval/suites/README.md`, `tests/cli/test_eval/test_models.py`, and the design-spec contract references `.dev/releases/current/cliEval/design-spec.md` (§3, §5, §8) and `phase-outputs/discovery/p2-contracts.md`, instructing rf-qa to verify: (a) every dataclass field in models.py matches the contract in p2-contracts.md with no extra or missing fields; (b) suite.schema.json validates the example.yaml manifest (have rf-qa run `jsonschema` mentally or via small script if available); (c) the schema's `expects[].type` enum exactly matches the enum in p2-contracts.md; (d) README.md documents every field present in the schema with no fabricated fields; (e) test_models.py exercises every dataclass with PASS and FAIL paths where applicable. The agent MUST write its full report to `phase-outputs/reviews/pg1-rf-qa-report.md` and return a binary verdict of PASS or FAIL (any issue of any severity is FAIL per I16). If unable to spawn rf-qa or the agent fails to produce a report, log the specific blocker using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PG.1.3:** Read the PG.1 verdict and proceed or fix

- [ ] Read the report at `phase-outputs/reviews/pg1-rf-qa-report.md` to determine the verdict: IF verdict is PASS, create `phase-outputs/plans/pg1-verdict.md` containing "PG.1 PASS — Phase 2 artifacts verified; Phase 3 may proceed" with the cycle count (1 if first pass), and continue to Phase 3; IF verdict is FAIL, read the report's findings list, then for each finding fix the relevant Phase 2 artifact in place (re-editing models.py, the schema, the example, the README, or test_models.py as the finding directs), then re-spawn rf-qa in fix-cycle mode by repeating Step PG.1.2 against the same input files (the agent must re-verify ALL previously failed items plus check for newly introduced issues), and re-read the new report; repeat up to a maximum of 3 fix cycles per I16; IF the third cycle still produces FAIL, update the frontmatter `status` to "⚪ Blocked" with `blocker_reason: "PG.1 QA gate FAIL after 3 fix cycles — escalating to user."`, append the unresolved issues to the ### Open Questions section of the ## Task Log / Notes, and HALT all further work, ensuring every fix cycle is recorded in `phase-outputs/reviews/pg1-rf-qa-report.md` (overwrite with the latest, but the verdict file accumulates cycle history), and the verdict file `phase-outputs/plans/pg1-verdict.md` clearly states the final outcome and cycle count. If unable to read the report, log the specific blocker using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

### Phase 3: Loader, Expect.* DSL, and CLI Subcommands

Phase 3 implements the active machinery: the YAML loader that turns manifests into `EvalSpec` lists, the Expect.* DSL whose callables the runner will invoke, and the two informational subcommands (`eval list`, `eval describe`) that prove the loader works end-to-end at the CLI surface.

**Step 3.1:** Create `cli/eval/loader.py` — YAML parsing + schema validation + parameterize expansion + template resolution (covers AC-P2.4, AC-P2.5, AC-P2.6 partial)

- [ ] Read the contracts at `phase-outputs/discovery/p2-contracts.md` for the loader's input/output shape, read the resolved Open Questions at `phase-outputs/discovery/open-questions-resolved.md` (specifically Q2 flat-only parameterize and Q3 split template resolution), read the schema at `src/superclaude/cli/eval/suites/suite.schema.json`, read the example manifest at `src/superclaude/cli/eval/suites/example.yaml`, read the models module at `src/superclaude/cli/eval/models.py` to import `EvalSpec` and `ManifestError`, and read `src/superclaude/cli/prd/config.py` or `cli/prd/inventory.py` for the conventional file-loading style, then create the file `src/superclaude/cli/eval/loader.py` containing: a module docstring stating the purpose; imports of `yaml`, `jsonschema`, `pathlib.Path`, `re`, `os` and the local `EvalSpec`/`ManifestError`; a constant `SUITES_DIR = Path(__file__).parent / "suites"`; a function `def load_schema() -> dict` that reads and json-parses `suite.schema.json`; a function `def list_suites() -> list[str]` that returns the stems of all `*.yaml` files in `SUITES_DIR` (sorted); a function `def load(suite_name: str) -> list[EvalSpec]` that reads `SUITES_DIR / f"{suite_name}.yaml"`, parses YAML (catching parse errors and re-raising as `ManifestError` with `file_line=f"{suite_name}.yaml:{mark.line+1}"` derived from the yaml Mark object), validates against the schema (catching `jsonschema.ValidationError` and re-raising as `ManifestError` with the JSON-path location string), expands every `parameterize:` block into N parametric `EvalSpec` instances with IDs suffixed `.1`, `.2`, … (the original eval id is the base; do NOT include the unparameterized form when `parameterize:` is present), resolves the load-time template variables (`{eval_id}`, `{project_key}`, `{home}` — where `{home}` resolves to the placeholder string `"{home}"` because the actual home is per-eval and chosen at runner time; document this in the docstring) by string-substituting inside every `inputs[*]`/`expects[*]`/`isolation.seed_state[*]` value, leaves runtime-only template variables (`{session_id}`, `{now - <duration>}`) un-substituted so the runner can resolve them, and returns the resulting `list[EvalSpec]`; a function `def load_raw(suite_name: str) -> dict` that returns the raw validated manifest dict (for `eval describe` to print without lowering to EvalSpec); and a helper `def _resolve_load_time_templates(value: Any, mapping: dict[str, str]) -> Any` that recursively walks dicts/lists/strings and substitutes `{key}` patterns from the mapping (leaving unknown `{key}` patterns intact), ensuring every error path raises `ManifestError` with a `file_line` attribute set whenever the source location is recoverable, every public function has a docstring describing inputs/outputs/raises, no field is read from the YAML that is not declared in the schema, and no fabricated template variables are resolved beyond the documented set. If any input file is missing, log the specific blocker using the templated format in the ### Phase 3 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 3.2:** Create `cli/eval/expect.py` — Expect.* assertion DSL (covers AC-P2.7, AC-P2.8, AC-P2.9)

- [ ] Read the design-spec §8 at `.dev/releases/current/cliEval/design-spec.md` for the complete Expect.* class signatures, read the resolved Open Question 1 at `phase-outputs/discovery/open-questions-resolved.md` (strict matching for `JsonlExpect.contains_event`), read the models module `src/superclaude/cli/eval/models.py` to import `EvalContext`, `ExpectResult`, `ExpectCallable`, then create the file `src/superclaude/cli/eval/expect.py` containing: a module docstring describing the DSL as a port of mcp-eval's `Expect.tools.*` API without any upstream dependency; imports of `json`, `re`, `pathlib.Path`, `dataclasses`, and the local `EvalContext`/`ExpectResult`; the `Expect` class with `@staticmethod` constructors `file(path)`, `jsonl(path)`, `settings_json(path)`, `exit_code()`, `stderr()`, `stdout()`, `duration()` each returning the appropriate sub-builder; the `FileExpect` class with methods `exists()`, `absent()`, `has_mode(mode: int)`, `has_content_matching(pattern: str | re.Pattern)` each returning an `ExpectCallable` `(EvalContext) -> ExpectResult` that resolves the file path against `ctx.home` if relative, performs the check, and returns `ExpectResult(passed=..., evidence="path X, size Y" or "<reason>", expect_type="file.exists"|"file.absent"|...)`; the `JsonlExpect` class with `contains_event(*, event: str, **fields)` returning a callable that opens the file, iterates lines, parses each as JSON, and returns PASS only when a line matches BOTH the `event` field AND every key/value in `**fields` exactly (strict per Q1), with FAIL evidence including the closest-matching line (most matching fields) for diagnostics, plus `event_count(*, event, op, n)` and `is_valid_jsonl()` per the spec; the `SettingsExpect` class with `has_registration(*, event: str, matcher: str)` returning a callable that parses settings.json and searches `hooks[event][*].matcher` for the matcher, plus `hooks_count(*, event, op, n)`; the `ExitCodeExpect` class with `equals(n: int)` and `in_(codes: list[int])` returning callables that read `ctx.exit_code`; the `StreamExpect` class with `contains(pattern)`, `does_not_contain(pattern)`, `matches_line(pattern)` parameterized by whether it inspects `ctx.tty_stdout` or `ctx.tty_stderr` (set at construction from `Expect.stdout()` vs `Expect.stderr()`); the `DurationExpect` class with `less_than(seconds)` / `greater_than(seconds)` reading `ctx.duration_sec`; and a private helper `_resolve_path(path, ctx)` that joins relative paths under `ctx.home` and leaves absolute paths alone, ensuring every PASS path returns `passed=True` with an `evidence` string containing concrete observed values (e.g., "path X, size Y"), every FAIL path returns `passed=False` with `evidence` describing the observed-vs-expected diff (e.g., for jsonl: "no line matched event=sticky_cleared; closest line: <line N JSON snippet>"), no observed values are fabricated, and every builder method returns a callable (not the result directly — callables are invoked by the runner with the live `ctx`). If models.py is unreadable, log the specific blocker using the templated format in the ### Phase 3 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 3.3:** Extend `cli/eval/commands.py` — add `eval list` subcommand (covers AC-P2.1)

- [ ] Read the existing `src/superclaude/cli/eval/commands.py` (provided by P1) to identify the `eval_group` Click group and existing subcommand decoration style, read `src/superclaude/cli/prd/commands.py` for the conventional Click subcommand style in this codebase, read the loader's `list_suites()` and `load_raw()` signatures in `src/superclaude/cli/eval/loader.py`, then extend `commands.py` by appending (do NOT modify existing P1 code) a new subcommand: `@eval_group.command("list")` named `eval_list` that takes no arguments, calls `loader.list_suites()` to enumerate suite stems, then for each suite stem calls `loader.load_raw(stem)` (wrapped in try/except for `ManifestError` so an invalid suite is listed with `<INVALID: reason>` rather than crashing the command) and extracts `name`, `version`, `description`, and the eval count (with `parameterize:` expanded — call `loader.load(stem)` for the count if cheap, or count `len(raw["evals"])` plus parameter-expansion math for efficiency), then prints a Rich-styled table (matching the prd commands' rich style; use `rich.console.Console` and `rich.table.Table`) with columns `Suite`, `Version`, `Description`, `Eval Count`, ensuring the output is human-readable, sorted by suite name, every `*.yaml` under `cli/eval/suites/` is listed (including `example.yaml`), invalid suites do not block listing of valid ones, and the command exits 0 on success. If the P1 commands.py is unreadable, log the specific blocker using the templated format in the ### Phase 3 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 3.4:** Extend `cli/eval/commands.py` — add `eval describe` subcommand (covers AC-P2.2, AC-P2.3)

- [ ] Read the just-extended `src/superclaude/cli/eval/commands.py` to confirm the `eval list` subcommand is in place and to see the loader-import style, then append a second subcommand: `@eval_group.command("describe")` named `eval_describe` with options `--suite SUITE` (required) and `--eval ID` (optional), that calls `loader.load(suite)` to get the expanded `list[EvalSpec]` (Suite-level validation errors should print a clean error to stderr with `click.echo(..., err=True)` plus the `file_line` from `ManifestError` and exit code 2; do NOT print a stack trace), then: IF `--eval` is not provided, print a human-readable rendering of the entire parsed suite — first a header section with `name`, `version`, `description` from `loader.load_raw(suite)`, then a per-eval section for every `EvalSpec` showing `ID` (e.g., `E2.1`), `Title`, `Category`, `Requires`, `Timeout`, an `Inputs` sub-section listing each input prompt, and an `Expects` sub-section listing each expect dict with its `type` and key fields; IF `--eval ID` is provided, filter to just the single matching EvalSpec (matching the `id` field exactly — `E2.1` matches `E2.1` only, not `E2`) and print that one in the same format, returning exit code 1 with an error message if the ID is not found, ensuring the output is sorted by eval `id`, uses Rich for formatting if the project conventions show that pattern, every field shown is sourced from the loaded EvalSpec / raw manifest with no fabrication, and the rendering is reproducibly deterministic (same input → same output). If unable to read commands.py, log the specific blocker using the templated format in the ### Phase 3 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 3.5:** Create `tests/cli/test_eval/test_loader.py` — valid/invalid parsing + parameterize + template resolution (covers AC-P2.4, AC-P2.5, AC-P2.6, AC-P2.10 loader portion)

- [ ] Read the loader at `src/superclaude/cli/eval/loader.py` to know the function signatures and error model, read the example manifest at `src/superclaude/cli/eval/suites/example.yaml` for the known-valid fixture, read the resolved Open Question 3 at `phase-outputs/discovery/open-questions-resolved.md` for the expected template-resolution behavior, then create the file `tests/cli/test_eval/test_loader.py` containing pytest test functions covering: (1) `test_load_example_succeeds` — call `loader.load("example")` and assert the return is a `list[EvalSpec]` with exactly 3 entries (E1, E2.1, E2.2 — the parameterized E2 expands into 2 variants); (2) `test_list_suites_includes_example` — call `loader.list_suites()` and assert `"example"` is in the returned list; (3) `test_parameterize_expansion` — assert that the E2 entries in the loaded list have IDs `E2.1` and `E2.2`, and that the `prefix` template variable is substituted in their inputs (`E2.1` has `prompt="a"`, `E2.2` has `prompt="b"`); (4) `test_template_eval_id_substitution` — assert that the `{eval_id}` template in E2's `expects[0].path` resolves to `{home}/.claude/marker-E2.1.txt` for E2.1 and `{home}/.claude/marker-E2.2.txt` for E2.2; (5) `test_template_home_left_unresolved` — assert that `{home}` is NOT substituted at load time (it remains literal `{home}` in the resulting EvalSpec) per Q3; (6) `test_template_session_id_left_unresolved` — same for `{session_id}` (it would only appear in an eval that references it; add a synthetic check via a temp fixture YAML if example.yaml does not naturally include it); (7) `test_invalid_yaml_raises_manifest_error_with_file_line` — write a malformed YAML to a temp file (e.g., `tmp_path / "bad.yaml"` with a tab-indentation error), monkeypatch `loader.SUITES_DIR` to point at `tmp_path`, call `loader.load("bad")`, assert it raises `ManifestError` whose `file_line` attribute is a non-empty string containing `bad.yaml:` and a line number; (8) `test_schema_violation_raises_manifest_error` — write a YAML missing the required `name` field to a temp file, assert `loader.load(...)` raises `ManifestError` with the JSON-path of the missing field in the error message, ensuring every test uses `pytest`/`tmp_path`/`monkeypatch` idiomatically, every assertion is grounded in actual loader behavior (not assumed), and no test is `pytest.skip`-stubbed. If loader.py is unreadable, log the specific blocker using the templated format in the ### Phase 3 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 3.6:** Create `tests/cli/test_eval/test_expect.py` — PASS/FAIL paths for every builder (covers AC-P2.7, AC-P2.8, AC-P2.9, AC-P2.10 expect portion)

- [ ] Read the DSL at `src/superclaude/cli/eval/expect.py` to know the exact API surface, read the models module at `src/superclaude/cli/eval/models.py` for `EvalContext`/`ExpectResult`, then create the file `tests/cli/test_eval/test_expect.py` containing pytest test functions using `tmp_path` for filesystem fixtures and constructing `EvalContext` instances with `home=tmp_path`: (1) `test_file_exists_pass` — write a file under `tmp_path`, build `Expect.file("relative/path").exists()`, invoke with ctx, assert `result.passed is True` and `result.evidence` contains the path and a size figure (covers AC-P2.7 PASS); (2) `test_file_exists_fail` — point Expect.file at a non-existent path, invoke, assert `result.passed is False` and `result.evidence` contains a reason like "file not found at <path>" (covers AC-P2.7 FAIL); (3) `test_file_absent_pass` and `test_file_absent_fail` — symmetric to (1)/(2) for `.absent()`; (4) `test_jsonl_contains_event_strict_match_pass` — write a JSONL file with 3 lines `{"event": "sticky_cleared", "session_id": "abc"}`, `{"event": "other", "session_id": "abc"}`, `{"event": "sticky_cleared", "session_id": "xyz"}`, build `Expect.jsonl(path).contains_event(event="sticky_cleared", session_id="abc")`, invoke, assert PASS with evidence pointing at line 1 (covers AC-P2.8 PASS); (5) `test_jsonl_contains_event_strict_match_fail` — same fixture, query for `event="sticky_cleared", session_id="missing"`, assert FAIL and evidence includes the closest matching line (line 1 with event match but wrong session_id, or line 3 with event match) (covers AC-P2.8 FAIL); (6) `test_settings_has_registration_pass` — write a synthetic `settings.json` with `{"hooks": {"PostToolUse": [{"matcher": "mcp__auggie__.*", "hooks": [...]}]}}`, build `Expect.settings_json(path).has_registration(event="PostToolUse", matcher="mcp__auggie__.*")`, assert PASS (covers AC-P2.9); (7) `test_settings_has_registration_fail` — same fixture, query for a non-matching matcher, assert FAIL; (8) `test_exit_code_equals_pass` and `test_exit_code_equals_fail` — set `ctx.exit_code` and assert; (9) `test_stream_contains_pass` and `test_stream_contains_fail` — set `ctx.tty_stdout` and use `Expect.stdout().contains("...")`; similarly for `stderr` and `does_not_contain`; (10) `test_duration_less_than_pass` and `test_duration_less_than_fail` — set `ctx.duration_sec` and assert, ensuring every test asserts BOTH `result.passed` AND the content of `result.evidence` (the evidence text is part of the contract — vague evidence is a test failure), no test fabricates the expected evidence text (instead assert it contains specific substrings derived from the actual implementation), and every Expect.* builder method from §8 of the design spec has at least one test. If expect.py is unreadable, log the specific blocker using the templated format in the ### Phase 3 Findings section, then mark this item complete. Once done, mark this item as complete.

### Phase Gate PG.2: QA Verification of Loader + DSL + CLI Subcommands

This gate verifies that the Phase 3 active machinery (loader.py, expect.py, the two new commands.py subcommands, test_loader.py, test_expect.py) is internally consistent and faithful to the design contracts before Phase 4's test-execution and sync-verification phase runs them for real. Fix cycles cap at 3 per I16.

**Step PG.2.1:** Aggregate Phase 3 outputs for QA review

- [ ] Use Bash to run `ls -la /config/workspace/IronClaude/src/superclaude/cli/eval/loader.py /config/workspace/IronClaude/src/superclaude/cli/eval/expect.py /config/workspace/IronClaude/src/superclaude/cli/eval/commands.py /config/workspace/IronClaude/tests/cli/test_eval/test_loader.py /config/workspace/IronClaude/tests/cli/test_eval/test_expect.py 2>&1` to confirm all five Phase 3 artifacts exist, then write an aggregation summary to `phase-outputs/reports/phase-3-artifacts.md` listing each artifact's absolute path and size, plus a one-line claim of contracts it satisfies (e.g., "loader.py — AC-P2.4 (load/raise), AC-P2.5 (parameterize expansion), AC-P2.6 (template resolution)"; "expect.py — AC-P2.7/8/9 PASS+FAIL paths"; "commands.py — AC-P2.1 (eval list), AC-P2.2/2.3 (eval describe)"), and a checklist mapping every AC from AC-P2.1 through AC-P2.9 to the artifact that satisfies it, ensuring the AC-to-artifact map is accurate per the actual code on disk with no AC marked satisfied if the implementing artifact is missing or empty. If any artifact is missing, log the specific blocker using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PG.2.2:** Spawn rf-qa for structural verification of Phase 3 outputs

- [ ] Spawn the `rf-qa` agent in `task-integrity` mode with input file paths `src/superclaude/cli/eval/loader.py`, `src/superclaude/cli/eval/expect.py`, `src/superclaude/cli/eval/commands.py`, `tests/cli/test_eval/test_loader.py`, `tests/cli/test_eval/test_expect.py`, and contract references `.dev/releases/current/cliEval/design-spec.md` (§5, §8), `phase-outputs/discovery/p2-contracts.md`, `phase-outputs/discovery/open-questions-resolved.md`, `phase-outputs/reports/phase-3-artifacts.md`, instructing rf-qa to verify: (a) loader.py raises `ManifestError` with `file_line` populated on schema violations and YAML parse errors; (b) loader.py expands `parameterize:` to the correct N variants with `.1`/`.2`/... IDs and the parameter values are substituted into all string fields of the eval; (c) loader.py performs load-time template substitution for `{eval_id}`/`{project_key}`/`{home}` per Q3 and leaves `{session_id}`/`{now - ...}` un-substituted; (d) expect.py implements every method in design-spec §8 with the documented signature, every PASS path returns `passed=True` with non-empty evidence, every FAIL path returns `passed=False` with observed-vs-expected diagnostic evidence; (e) commands.py adds `eval list` and `eval describe` to the existing `eval_group` without modifying P1 code; (f) test_loader.py and test_expect.py exercise both PASS and FAIL paths for every AC-listed behavior. The agent MUST write its full report to `phase-outputs/reviews/pg2-rf-qa-report.md` and return PASS or FAIL. If unable to spawn rf-qa, log the specific blocker using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PG.2.3:** Read the PG.2 verdict and proceed or fix

- [ ] Read `phase-outputs/reviews/pg2-rf-qa-report.md` to determine the verdict: IF PASS, create `phase-outputs/plans/pg2-verdict.md` containing "PG.2 PASS — Phase 3 artifacts verified; Phase 4 may proceed" with the cycle count, and continue to Phase 4; IF FAIL, fix each finding in the relevant Phase 3 artifact, re-spawn rf-qa (repeat Step PG.2.2) to re-verify ALL previously failed items plus new issues, repeat up to 3 cycles per I16; IF the third cycle still produces FAIL, update frontmatter `status` to "⚪ Blocked" with `blocker_reason: "PG.2 QA gate FAIL after 3 fix cycles — escalating to user."`, append unresolved issues to ### Open Questions, and HALT. Ensure every fix-cycle run is recorded and the final verdict file states the outcome and cycle count. If unable to read the report, log the specific blocker using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

### Phase 4: Test Execution and Sync Verification

Phase 4 runs the three new pytest modules and `make verify-sync` against the actual on-disk code to satisfy AC-P2.10 and AC-P2.11 with empirical evidence, not just structural promises. Per I18, code-modifying tasks MUST include test-execution items; this phase provides them.

**Step 4.1:** Run `uv run pytest tests/cli/test_eval/test_models.py tests/cli/test_eval/test_loader.py tests/cli/test_eval/test_expect.py -v` (covers AC-P2.10)

- [ ] Use the Bash tool to run the command `cd /config/workspace/IronClaude && uv run pytest tests/cli/test_eval/test_models.py tests/cli/test_eval/test_loader.py tests/cli/test_eval/test_expect.py -v 2>&1` and capture the complete output, then write the raw output to `phase-outputs/test-results/pytest-output.txt` preserving the exact pytest output with no modifications, then create a structured summary at `phase-outputs/test-results/pytest-summary.md` containing: overall result (PASSED or FAILED), the pytest summary line (e.g., `=== 27 passed in 1.42s ===`), total tests collected, total passed, total failed, total errored, total skipped, and a table of any failures with columns Test Name, Error Type (e.g., AssertionError, ImportError), Brief Error Message (one line), and AC-P2.10 verdict (PASS only if total failed == 0 AND total errored == 0), ensuring the summary numbers match the raw pytest output exactly with no fabricated counts, every failure is listed, and the AC verdict is derived strictly from the numbers (failed > 0 OR errored > 0 → FAIL). If pytest itself fails to execute (e.g., import error before collection), log the execution failure using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.2:** Conditionally fix or proceed based on Step 4.1 result

- [ ] Read the summary at `phase-outputs/test-results/pytest-summary.md` to determine the overall result: IF PASSED, create `phase-outputs/plans/test-verdict.md` containing "AC-P2.10 SATISFIED — pytest <count> passed, 0 failed, 0 errored" with the pass count, and proceed to Step 4.3; IF FAILED, read the raw output at `phase-outputs/test-results/pytest-output.txt` for full tracebacks, then for each failed test identify the root cause by reading the test, the implementation it exercises, and any helper modules, then create `phase-outputs/plans/test-fix-plan.md` listing each failed test with: the failing assertion, the most likely root cause (in the test, in the source, or in a contract mismatch), the proposed fix (which file to edit and what to change), and a priority order (compile/import errors first, then assertion failures), then apply the fixes to the relevant source/test files in place (do NOT introduce new files), then re-run Step 4.1's pytest command and update the summary file, repeating until PASSED or until 3 fix cycles have been spent; IF after 3 cycles tests still fail, append the residual failures to ### Open Questions in the ## Task Log / Notes and HALT with frontmatter `status="⚪ Blocked"` and a clear blocker reason, ensuring every fix decision is grounded in the actual failure output (not guessed), and no test is disabled or marked `pytest.skip` to make it pass. If the summary file is missing, log the blocker using the templated format in the ### Phase 4 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 4.3:** Run `make verify-sync` to confirm src/ and .claude/ remain in sync (covers AC-P2.11)

- [ ] Use the Bash tool to run the command `cd /config/workspace/IronClaude && make verify-sync 2>&1` and capture the complete output plus the shell exit code, then write the raw output to `phase-outputs/test-results/verify-sync-output.txt` preserving exact output, then create a structured summary at `phase-outputs/test-results/verify-sync-summary.md` containing: the captured exit code (EXIT=N), a PASS/FAIL verdict (PASS only if EXIT=0), any diff lines or sync warnings printed by the command, and a final AC-P2.11 verdict line, ensuring the exit code reflected in the summary matches the actual shell exit (verify by appending `; echo "EXIT=$?"` to the command), and that no fabricated lines are introduced into the diff section. NOTE: This task does NOT modify any files under `.claude/` directly — all source-of-truth files live under `src/superclaude/cli/eval/` — so `make verify-sync` should naturally pass without invoking `make sync-dev`. IF the verdict is FAIL because something under `.claude/` is out of sync with `src/superclaude/`, do NOT run `make sync-dev` automatically; instead log the failure as a Phase 4 blocker and HALT for user review, because an unexpected sync failure on this task means an unrelated drift exists in the repo. If unable to run make, log the specific blocker using the templated format in the ### Phase 4 Findings section, then mark this item complete. Once done, mark this item as complete.

**Step 4.4:** Run `uv run superclaude eval list` and `uv run superclaude eval describe --suite example` smoke-tests (covers AC-P2.1, AC-P2.2, AC-P2.3 end-to-end)

- [ ] Use the Bash tool to run three sequential commands and capture each output separately: (a) `cd /config/workspace/IronClaude && uv run superclaude eval list 2>&1; echo "EXIT=$?"` — capture to `phase-outputs/test-results/cli-eval-list.txt`; (b) `cd /config/workspace/IronClaude && uv run superclaude eval describe --suite example 2>&1; echo "EXIT=$?"` — capture to `phase-outputs/test-results/cli-eval-describe-all.txt`; (c) `cd /config/workspace/IronClaude && uv run superclaude eval describe --suite example --eval E1 2>&1; echo "EXIT=$?"` — capture to `phase-outputs/test-results/cli-eval-describe-E1.txt`, then create a structured summary at `phase-outputs/test-results/cli-smoke-summary.md` containing: a per-command section with the command, captured exit code, key output excerpt (first 30 lines + last 10 lines if longer), and a PASS/FAIL verdict per AC: AC-P2.1 PASS iff command (a) lists `example` with name/version/description/eval-count; AC-P2.2 PASS iff command (b) prints parsed structure for all evals (E1 and E2 expanded variants); AC-P2.3 PASS iff command (c) prints only E1's details and exits 0, ensuring each verdict is derived directly from the captured output (e.g., grep for the expected suite name or eval ID), and no verdict is awarded if the command exits non-zero or the expected output is absent. If a command fails to execute (e.g., import error), log the specific blocker using the templated format in the ### Phase 4 Findings section, then mark this item complete. Once done, mark this item as complete.

### Phase Gate PG.3: Final QA Validation Before Done

This final gate verifies that all 11 acceptance criteria are satisfied with on-disk evidence, that all output files exist, that no checklist items have been skipped, and that blockers are either resolved or surfaced as Open Questions. Per I17, this validation MUST run before the frontmatter is set to Done.

**Step PG.3.1:** Aggregate all AC evidence into a coverage report

- [ ] Use Glob to find every file in `phase-outputs/test-results/`, `phase-outputs/reviews/`, `phase-outputs/reports/`, and `phase-outputs/plans/` (pattern `phase-outputs/**/*`), then read each file, then create the final consolidated coverage report at `phase-outputs/reports/ac-coverage-report.md` containing: an executive summary stating "AC-P2.1 through AC-P2.11 — SATISFIED" or "PARTIAL — see findings"; a table with 11 rows (one per AC) with columns AC ID, AC Statement (quoted from BUILD_REQUEST), Evidence Path (the phase-outputs file proving satisfaction), Verdict (PASS/FAIL), Notes; a section listing every checklist item from Phase 1 through Phase 4 with its completion status (read this task file and count `[x]` vs `[ ]`); a section listing every blocker recorded in the Task Log with its resolution status; and a final verdict line "TASK READY FOR DONE" or "TASK NOT READY — N issues outstanding", ensuring every PASS verdict is backed by a real on-disk evidence file path (not assumed), every AC statement is quoted verbatim from the BUILD_REQUEST, and the final verdict is derived strictly from the row-level verdicts (any FAIL → not ready). If any required phase-outputs file is missing, log the gap using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PG.3.2:** Spawn rf-qa for the final task-integrity verdict

- [ ] Spawn the `rf-qa` agent in `task-integrity` mode with the input file paths `phase-outputs/reports/ac-coverage-report.md`, this task file (`TASK-RF-20260518-cliEval-P2-loader-models-expect.md`), `phase-outputs/test-results/pytest-summary.md`, `phase-outputs/test-results/verify-sync-summary.md`, `phase-outputs/test-results/cli-smoke-summary.md`, and the BUILD_REQUEST `.dev/releases/current/cliEval/build-requests/BUILD-REQUEST-cliEval-P2-loader-models-expect.md`, instructing rf-qa to verify: (a) every AC from AC-P2.1 through AC-P2.11 has a PASS verdict in the coverage report and a corresponding on-disk evidence file; (b) every `- [ ]` in this task file has been marked `- [x]` OR has an associated blocker entry in the Task Log with a stated resolution; (c) every output file specified in checklist items exists on disk (rf-qa MUST use Glob to verify); (d) the pytest summary shows 0 failed and 0 errored; (e) verify-sync exited 0; (f) every blocker entry in the Task Log has either a resolution note or is escalated to Open Questions. The agent MUST write its report to `phase-outputs/reviews/pg3-rf-qa-final-report.md` and return PASS or FAIL. If unable to spawn rf-qa, log the blocker using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PG.3.3:** Read PG.3 verdict and either finalize or fix

- [ ] Read `phase-outputs/reviews/pg3-rf-qa-final-report.md` to determine the final verdict: IF PASS, create `phase-outputs/plans/pg3-verdict.md` stating "PG.3 PASS — all 11 ACs satisfied; task ready for Post-Completion Actions" with the cycle count, and proceed to Post-Completion Actions; IF FAIL, fix each finding by editing the relevant artifact (Phase 2, Phase 3, or test outputs), then re-run the relevant phase-output regeneration (e.g., re-run Step 4.1 if a test was edited, re-run Step PG.3.1 to refresh the coverage report), then re-spawn rf-qa via Step PG.3.2, repeating up to 3 cycles per I16; IF the third cycle still produces FAIL, update frontmatter `status` to "⚪ Blocked" with `blocker_reason` summarizing the unresolved issues, append the issues to ### Open Questions, and HALT, ensuring every fix-cycle iteration is recorded and the final verdict file states the outcome and cycle count. If unable to read the report, log the blocker using the templated format in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [ ] Use Glob to find all output files specified in this task's checklist items — specifically `src/superclaude/cli/eval/models.py`, `src/superclaude/cli/eval/loader.py`, `src/superclaude/cli/eval/expect.py`, `src/superclaude/cli/eval/suites/suite.schema.json`, `src/superclaude/cli/eval/suites/example.yaml`, `src/superclaude/cli/eval/suites/README.md`, `tests/cli/test_eval/test_models.py`, `tests/cli/test_eval/test_loader.py`, `tests/cli/test_eval/test_expect.py`, and every file under `phase-outputs/` — and confirm each exists on disk, ensuring no expected deliverable is missing. The extended `src/superclaude/cli/eval/commands.py` must also exist (it was modified, not created — verify it contains the `eval_list` and `eval_describe` function definitions by reading it). If any file is missing without a documented blocker, log the gap in ### Follow-Up Items below, then mark this item complete. Once done, mark this item as complete.

- [ ] Confirm that the test suite from Step 4.1 was the last test execution and that no source files were modified after it. If any source modifications occurred between Step 4.1 and now (e.g., during PG.3 fix cycles), re-run `cd /config/workspace/IronClaude && uv run pytest tests/cli/test_eval/ -v 2>&1` and verify all tests still pass; capture the result to `phase-outputs/test-results/final-pytest-verification.txt`. If tests now fail, this is a regression — log it as a critical blocker in ### Phase Gate Findings, update frontmatter `status` to "⚪ Blocked", and HALT rather than marking the task Done. If no modifications occurred, note "Tests verified in Step 4.1; no subsequent modifications" in the ### Execution Log, then mark this item complete. Once done, mark this item as complete.

- [ ] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file by populating the templated format provided there. The summary MUST document: Completion Date (today); Work Completed listing each created file (the 6 implementation files + 3 test files + extensions to commands.py + 5 discovery files + the coverage report); Challenges Encountered (any items in Phase Findings sections with status Blocked or fix-cycle history); Deviations from Process (any time a step was modified or skipped); Blockers Logged with status Resolved or Unresolved; and Follow-Up Required (Yes if any Open Questions remain or any AC was marked PARTIAL, otherwise No), ensuring the summary is sourced entirely from the task log and phase-outputs with no fabricated content. Once the summary is complete, mark this item as complete.

- [ ] Update the frontmatter of this task file by setting `status` to "🟢 Done", setting `completion_date` to today's date in `YYYY-MM-DD` format, and setting `updated_date` to today's date, then add a timestamped entry to the ### Execution Log section using the format `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date. All 11 ACs satisfied per phase-outputs/reports/ac-coverage-report.md.`, ensuring the frontmatter is valid YAML, no other frontmatter fields are modified, and the execution log preserves all prior entries. Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary
<!-- Fill this section in Post-Completion Actions -->

**Completion Date:** [YYYY-MM-DD]

**Work Completed:**

- [Implementation files]: [List with paths]
- [Test files]: [List with paths]
- [Schema + example + README]: [List with paths]
- [Handoff files created]: [List phase-outputs/ files]

**Challenges Encountered:**

- [Challenge]: [How addressed] OR None

**Deviations from Process:**

- [Deviation]: [Rationale] OR None

**Blockers Logged:**

- [Step X.Y]: [Description] - **Status:** [Resolved/Unresolved] OR None

**Follow-Up Required:** [Yes/No] - [Description if yes]

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.

**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.

### Phase 1 — Preparation, Dependency Verification, and Discovery Findings

<!-- TEMPLATE FOR PHASE FINDINGS:
**[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

### Phase 2 — Data Models, Schema, and Example Findings

### Phase 3 — Loader, DSL, and CLI Subcommands Findings

### Phase 4 — Test Execution and Sync Verification Findings

### Phase Gate Findings

*QA gate verdicts, fix cycle counts, and unresolved issues from PG.1, PG.2, and PG.3 are recorded here.*

### Open Questions

<!-- For any issue that survives the 3-cycle fix cap on a QA gate, or for any Q1/Q2/Q3 resolution that materially departs from the design spec and requires user adjudication. Format:

**[YYYY-MM-DD HH:MM]** - [Origin: Step PG.N.M or Q-K]
- **Question:** [Verbatim]
- **Resolution attempted:** [What was tried]
- **Outstanding issue:** [What still needs human adjudication]
-->

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
