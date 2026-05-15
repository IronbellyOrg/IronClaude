# Bucket B — sc-tasklist CLI and command digest

## Files read

| Path | Lines | Status |
|------|-------|--------|
| src/superclaude/commands/tasklist.md | 114 | complete |
| src/superclaude/cli/tasklist/commands.py | 185 | complete |
| src/superclaude/cli/tasklist/executor.py | 276 | complete |
| src/superclaude/cli/tasklist/gates.py | 43 | complete |
| src/superclaude/cli/tasklist/models.py | 26 | complete |
| src/superclaude/cli/tasklist/prompts.py | 234 | complete |
| src/superclaude/cli/tasklist/__init__.py | 17 | complete |

## Command wrapper (`commands/tasklist.md`)

- **Arg parsing**: `<roadmap-path> [--spec <spec-path>] [--output <output-dir>]` (commands/tasklist.md:22-27); supports `@file` syntax and explicit paths (commands/tasklist.md:26).
- **Input validation**: four checks (commands/tasklist.md:58-67) — roadmap exists/readable/non-empty (lines 60-61, `EMPTY_INPUT`/`MISSING_FILE`); spec exists if provided (62-63); `--output` parent exists+writable (64-65); TASKLIST_ROOT derivation succeeds (66-67, `DERIVATION_FAILED`). Error format is two fields `error_code`/`message` (commands/tasklist.md:52-56). No partial output on failure (commands/tasklist.md:50).
- **TASKLIST_ROOT derivation**: 3-step priority algorithm (commands/tasklist.md:40-46): (1) first `.dev/releases/current/<segment>/` match in roadmap; (2) first `v<digits>(.<digits>)+` version token → `.dev/releases/current/<token>/`; (3) fallback `.dev/releases/current/v0.0-unknown/`.
- **Mode flags**: none — command file does not surface generate/validate/patch modes; only `--spec` and `--output` (commands/tasklist.md:34-38). Activation is `STRICT` (commands/tasklist.md:71).
- **Skill invocation**: MANDATORY `Skill sc:tasklist-protocol` before any protocol steps (commands/tasklist.md:73-82). Context passed: roadmap text, spec text (optional), resolved TASKLIST_ROOT (commands/tasklist.md:77-79). Explicit instruction: "Do NOT attempt to generate the tasklist using only this command file. The full generation algorithm is in the protocol skill." (commands/tasklist.md:81-82).
- **Validation artifact references**: "Validate generated tasklist against source roadmap (via skill stages 7-10)" and "Produce validation artifacts in TASKLIST_ROOT/validation/" (commands/tasklist.md:107-108). Command does NOT itself call the CLI `tasklist validate` subcommand — that wiring is implicit via the skill.

## CLI module structure

### `__init__.py`

- Lazy `__getattr__` exposing `tasklist_group` from `.commands` (__init__.py:9-14); `__all__ = ["tasklist_group"]` (__init__.py:17). Module docstring: "tasklist validation against upstream roadmaps using the shared pipeline/ foundation" (__init__.py:3-6).

### commands.py

- **Click group**: `@click.group("tasklist")` `tasklist_group` (commands.py:15-28). Docstring scopes to validation only — "Validate generated tasklists against their upstream roadmap" (commands.py:18-19). No `generate` subcommand exists.
- **Sole subcommand**: `@tasklist_group.command()` `validate` (commands.py:31, 73-95). Per FR-016/FR-017 comment (commands.py:3-4).
- **Args/options/defaults**:
  - Positional `OUTPUT_DIR` (Path, commands.py:32) — where validation report is written.
  - `--roadmap-file` default `{output_dir}/roadmap.md` (commands.py:33-38, resolved at 103-107).
  - `--tasklist-dir` default `{output_dir}/` (commands.py:39-44, resolved at 109-111).
  - `--model` default `""` (commands.py:45-49).
  - `--max-turns` default `100` (commands.py:50-55).
  - `--debug` flag (commands.py:56-60).
  - `--tdd-file` optional Path (commands.py:61-66) — TDD validation input.
  - `--prd-file` optional Path (commands.py:67-72) — PRD validation input.
- **Output paths**: `resolved_output.mkdir(parents=True, exist_ok=True)` (commands.py:101); report at `resolved_output / "tasklist-fidelity.md"` (commands.py:175). Echoes report path on existence (commands.py:176-177) or "No report generated" stderr otherwise (commands.py:178-179). Exits 1 with red "FAIL: HIGH-severity deviations found" if `passed` is False (commands.py:181-183); green "PASS" otherwise (commands.py:184-185).
- **Auto-wiring of TDD/PRD from roadmap state** (commands.py:113-159): reads `.roadmap-state.json` via `..roadmap.executor.read_state` at `resolved_output / ".roadmap-state.json"` (commands.py:114-116). If `--tdd-file` not passed, prefers `state["tdd_file"]` (commands.py:117-131); falls back to `state["spec_file"]` when `state["input_type"] == "tdd"` (commands.py:132-144). Same pattern for `--prd-file` reading `state["prd_file"]` (commands.py:145-159). Warns to stderr when state references a missing path (commands.py:128-131, 155-159). All wired paths echoed via `click.echo(..., err=True)` with `[tasklist validate] Auto-wired …` prefix.
- **Config + dispatch**: builds `TasklistValidateConfig` (commands.py:161-171) and calls `execute_tasklist_validate(config)` (commands.py:173).

### executor.py

- **Execution flow**: `execute_tasklist_validate(config)` (executor.py:251-276) is the top-level entry. It calls `_build_steps(config)` (executor.py:257) and dispatches via `execute_pipeline(steps=steps, config=config, run_step=tasklist_run_step)` (executor.py:259-263). After pipeline returns, checks for `FAIL`/`TIMEOUT` results (executor.py:268-274) and returns `not _has_high_severity(report_path)` (executor.py:276).
- **Validation orchestration**: `_build_steps` (executor.py:191-218) builds a single `Step` with id `"tasklist-fidelity"` (executor.py:204), prompt from `build_tasklist_fidelity_prompt(...)` (executor.py:205-210), output `output_dir / "tasklist-fidelity.md"` (executor.py:211), gate `TASKLIST_FIDELITY_GATE` (executor.py:212), `timeout_seconds=600` (executor.py:213), `retry_limit=1` (executor.py:215), inputs = `[roadmap_file] + tasklist_files (+ tdd_file?) (+ prd_file?)` (executor.py:194-200). Tasklist files collected via `_collect_tasklist_files` — sorted `*.md` glob with FileNotFoundError on missing dir or empty result (executor.py:40-52).
- **Claude subprocess invocation**: `tasklist_run_step` (executor.py:92-188) — mirrors `validate_run_step` from roadmap/validate_executor (executor.py:99). Embeds inputs inline via `_embed_inputs` fenced blocks (executor.py:55-63, 114-116); composes `step.prompt + "\n\n" + embedded` (executor.py:116); warns at 500KB (executor.py:37, 117-123). Instantiates `ClaudeProcess` (executor.py:130-140) with `output_format="text"`, `permission_flag=config.permission_flag`. Polls `proc._process.poll()` with `cancel_check()` and 1s sleep (executor.py:144-155). Handles exit 124 → `TIMEOUT` (executor.py:160-168), non-zero → `FAIL` (executor.py:170-178). On success calls `_sanitize_output` to strip conversational preamble before YAML frontmatter (executor.py:66-89, 180).
- **Severity gate evaluation**: `_has_high_severity` parses YAML frontmatter for `high_severity_count:` line; returns True (treated as failure) when report missing, frontmatter malformed, or field absent (executor.py:221-248).
- **Patch invocation — absences explicit**: No call to `/sc:adversarial`, no Sprint executor invocation, no `sc:task-unified` call, no `tasklist generate` subcommand, no `patch` step, no re-run loop. The executor runs exactly one fidelity step and exits. The "patch any drift, and verifies corrections" behavior described in the skill command file (commands/tasklist.md:14) is NOT implemented in this CLI module — confirmed absent across executor.py:1-276. There is no `subprocess` or `os.system` invocation of any other `superclaude` CLI command or `claude` slash command within the validate executor.

### gates.py

- **`TASKLIST_FIDELITY_GATE`** (gates.py:20-43) — module-level `GateCriteria` constant (pure data per NFR-005, gates.py:3-6).
- **Required frontmatter fields**: `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready` (gates.py:21-28).
- **min_lines**: 20 (gates.py:29). **enforcement_tier**: `"STRICT"` (gates.py:30).
- **Semantic checks** (gates.py:31-42):
  - `high_severity_count_zero` — uses `_high_severity_count_zero` from `roadmap/gates.py` (gates.py:18, 33-36); failure message "high_severity_count must be 0 for tasklist-fidelity gate to pass" (gates.py:35).
  - `tasklist_ready_consistent` — uses `_tasklist_ready_consistent` from `roadmap/gates.py` (gates.py:18, 37-41); failure message "tasklist_ready is inconsistent with severity counts or validation_complete" (gates.py:40).
- Unidirectional dep on `roadmap/validate_gates.py` pattern noted (gates.py:11-13).

### models.py

- **`TasklistValidateConfig`** dataclass (models.py:14-26) extends `PipelineConfig` (models.py:11, 15).
- Fields: `output_dir: Path` default `Path(".")` (models.py:22), `roadmap_file: Path` default `Path(".")` (models.py:23), `tasklist_dir: Path` default `Path(".")` (models.py:24), `tdd_file: Path | None = None` (models.py:25), `prd_file: Path | None = None` (models.py:26).
- No additional types/schemas — gate criteria live in `gates.py`, pipeline primitives (`Step`, `StepResult`, `StepStatus`, `PipelineConfig`) imported from `..pipeline.models`.

### prompts.py

- **Fidelity-prompt template**: `build_tasklist_fidelity_prompt(roadmap_file, tasklist_dir, tdd_file=None, prd_file=None) -> str` (prompts.py:17-148). Pure function per NFR-004 (prompts.py:3-5).
  - Base prompt (prompts.py:37-109) covers: validation layering guard restricting to roadmap→tasklist (42-47); severity definitions HIGH/MEDIUM/LOW with examples (48-68); 5 comparison dimensions — Deliverable Coverage, Signature Preservation, Traceability ID Validity, Dependency Chain Correctness, Acceptance Criteria Completeness (69-81); YAML frontmatter contract listing all gate-required fields plus `source_pair`, `upstream_file`, `downstream_file` (82-93); Deviation Report fields `DEV-NNN` with ID/Severity/Deviation/Upstream Quote/Downstream Quote/Impact/Recommended Correction (94-103); Summary section (104-108).
  - TDD supplementary block (prompts.py:112-128) — 5 checks: Testing Strategy §15, Migration & Rollout §19, Component Inventory §10, Data Models §7, API Specifications §8. Missing coverage = MEDIUM.
  - PRD supplementary block (prompts.py:131-146) — 4 checks: User Personas S7, Success Metrics S19, Scope/Journey Map S12/S22, Business Context S5 (priority mismatch = LOW). Missing coverage = MEDIUM.
  - Appends `_OUTPUT_FORMAT_BLOCK` imported from `superclaude.cli.roadmap.prompts` (prompts.py:14, 148).
- **Generation-prompt template**: `build_tasklist_generate_prompt(roadmap_file, tdd_file=None, prd_file=None) -> str` (prompts.py:151-234). Baseline decomposition instructions (171-184); TDD enrichment block referencing S15/S8/S10/S19/S7 (187-202); PRD enrichment referencing S7/S12/S22/S19/S5/S12 (205-221); combined TDD+PRD precedence note (224-232); appends `_OUTPUT_FORMAT_BLOCK` (234).
- **Variables consumed**: only file paths; no run-time templating variables — file contents are embedded by the executor's `_embed_inputs`, not by the prompt builder.
- **Whether generation is CLI-driven or skill-only** — explicit docstring quote (prompts.py:160-163):
  > "This function is used by the `/sc:tasklist` skill protocol for inference-based generation workflows. It is NOT currently called by the CLI `tasklist validate` executor (which only runs fidelity validation). There is no `tasklist generate` CLI subcommand — generation is handled by the skill protocol reading this prompt builder directly."

## Validation artifacts produced

- `tasklist-fidelity.md` — written at `config.output_dir / "tasklist-fidelity.md"` (executor.py:211, 265; commands.py:175). Sole artifact produced by the CLI `validate` path.
- `.err` sibling — `step.output_file.with_suffix(".err")` for stderr capture during Claude subprocess (executor.py:133).
- `.tmp` sibling — used transiently by `_sanitize_output` before `os.replace` (executor.py:84-86).
- No `validation/` subdirectory and no `tasklist-patch.md`/`tasklist-verify.md` are produced by the CLI — despite `commands/tasklist.md:108` mentioning "validation artifacts in TASKLIST_ROOT/validation/", the Python CLI writes the single report at the top level of `output_dir`.

## Integration points

- **Skill invocation**: only in `commands/tasklist.md:73-82` (`Skill sc:tasklist-protocol`). The Python CLI does NOT invoke the skill; the skill is invoked by the slash-command layer. Conversely, the skill calls back into the CLI for validation per `commands/tasklist.md:107-108` (skill stages 7-10).
- **`/sc:adversarial` invocation**: no call found. `grep`-grade absence confirmed across all 7 files; no `subprocess`, `Popen`, or shell-out to any sibling slash command in executor.py.
- **Sprint executor invocation**: no call found. `commands/tasklist.md:113` explicitly states "Run `superclaude sprint run` … invocation is separate". CLI does not import from `..sprint`.
- **Roadmap module integration**: `commands.py:114` imports `read_state` from `..roadmap.executor` for `.roadmap-state.json` auto-wiring; `gates.py:18` imports `_high_severity_count_zero` and `_tasklist_ready_consistent` from `..roadmap.gates`; `prompts.py:14` imports `_OUTPUT_FORMAT_BLOCK` from `..roadmap.prompts`. Unidirectional dependency tasklist→roadmap.
- **Pipeline integration**: `executor.py:24-26` imports `execute_pipeline`, `PipelineConfig`, `Step`, `StepResult`, `StepStatus`, `ClaudeProcess` from `..pipeline.*`. All subprocess management is delegated to the shared pipeline foundation.

## evidence_status: complete
