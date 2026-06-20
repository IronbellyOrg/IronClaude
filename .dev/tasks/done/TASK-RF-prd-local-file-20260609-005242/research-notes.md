# Research Notes: Remove PRD pipeline `--file` local-path misuse (session-token crash fix)

**Date:** 2026-06-09
**Scenario:** A (explicit — design spec drives the change)
**Depth Tier:** Quick (<5 files, single concern)
**Track Count:** 1
**Driving spec:** `.dev/specs/prd-local-file-delivery-fix.md`
**Branch:** `fix/prd-local-file-no-session-token`

---

## EXISTING_FILES

- **`src/superclaude/cli/prd/process.py`** — `PrdClaudeProcess(ClaudeProcess)`. Holds the defect:
  - `_build_file_args(config, step_id)` static method (~:169-206) emits `--file` at TWO points:
    - `:198-199` refs >50KB branch: `file_args.extend(["--file", str(ref_path)])`
    - `:201-204` `--spec` branch (unconditional for steps in `_SPEC_FILE_STEPS`): `file_args.extend(["--file", spec_path])`
  - `:154-155` builds `file_args = self._build_file_args(...)`; `:166` passes `extra_args=file_args` to `super().__init__`.
  - Constants: `_PHASE_ALLOWED_REFS` (:95-113), `_FILE_SIZE_THRESHOLD = 50_000` (:115), `_SPEC_FILE_STEPS = frozenset({"scope-discovery","investigation"})` (:121).
  - Module docstring (:4,:11) and class docstring (:132-135) advertise "Phase-aware `--file` arg construction (GAP-003)".
- **`src/superclaude/cli/pipeline/process.py`** — base `ClaudeProcess`. `build_command()` (:73-95) appends `self.extra_args` to the claude argv (:94). `build_env()` (:97-112) = `os.environ.copy()` (so the child inherits the parent env — no token present headless).
- **`src/superclaude/cli/prd/prompts.py`** — delivery machinery to REUSE:
  - `_read_file(path, max_bytes=50_000)` (:42-47) + `_TRUNCATION_MARKER` (:34) — inline-with-cap.
  - `_authoritative_specs_block(spec_paths)` (:120-138) — Phase-1 paths-only block; called at `:247` (scope-discovery prompt) and `:919` (investigation prompt).
  - Refs are ALREADY inlined by name via `_read_file` (e.g. :514-518) — independent of `_build_file_args`.
- **Sibling pipelines (the correct pattern):** `roadmap/executor.py:8-9`, `tasklist/executor.py:10`, `roadmap/validate_executor.py:11` — "No `--file` … `--file` is a cloud download mechanism and does not inject local file content" (FR-003/FR-023).
- **Tests:** `tests/cli/prd/test_prompts.py`, `tests/cli/prd/test_cli_smoke.py`, `tests/cli/prd/test_integration.py`, `tests/roadmap/test_prd_prompts.py`, `tests/roadmap/test_prd_cli.py`. Need to locate any existing `PrdClaudeProcess`/`_build_file_args` test.

## PATTERNS_AND_CONVENTIONS

- Source of truth `src/superclaude/`; `make sync-dev` copies to `.claude/`; `make verify-sync` before commit. UV only (`uv run pytest`).
- `--file` semantics (per `claude --help`): "File resources to download at startup. Format: file_id:relative_path" — cloud download requiring `CLAUDE_CODE_SESSION_ACCESS_TOKEN`. Passing a local path is the misuse.
- Measured: all PRD refs <50KB (largest `agent-prompts.md` 22.8KB) → refs `--file` branch is dead in practice; prompt builder already inlines refs in full.
- Empty-input contract: `_authoritative_specs_block(None|[])` returns `""` → no-spec prompts must stay byte-identical.

## GAPS_AND_QUESTIONS

- Exact existing test coverage for `PrdClaudeProcess._build_file_args` / `build_command` extra_args — researcher must locate (likely `tests/cli/prd/`).
- Confirm no other references to `_PHASE_ALLOWED_REFS`, `_FILE_SIZE_THRESHOLD`, `_SPEC_FILE_STEPS` outside `_build_file_args` before deleting (grep).
- Confirm `_authoritative_specs_block` callers (:247, :919) only pass `spec_paths` and don't depend on paths-only formatting elsewhere (e.g., snapshot tests).

## RECOMMENDED_OUTPUTS

- `research/01-process-py-file-args.md` — File Inventory of process.py: the two `--file` branches, constants, usages, the extra_args wiring, and grep for external references to the constants. Plus existing test coverage for this method.
- `research/02-prompts-and-siblings.md` — Patterns: `_authoritative_specs_block` + `_read_file`/`_TRUNCATION_MARKER`; how callers (:247,:919) use the block; how refs get inlined (:514-518); the sibling-pipeline no-`--file` pattern; existing prompts test conventions.
- `research/03-template-and-tests.md` — Template 02 rules (A3 granularity, B2 self-containment) + test conventions in `tests/cli/prd/` (pytest layout, how PrdClaudeProcess/prompts are constructed in tests, fixtures).

## SUGGESTED_PHASES

- Researcher 1 (File Inventory): `src/superclaude/cli/prd/process.py` + `src/superclaude/cli/pipeline/process.py` build_command/extra_args + grep constants usages + existing process tests. Output `research/01-process-py-file-args.md`.
- Researcher 2 (Patterns & Conventions): `src/superclaude/cli/prd/prompts.py` (`_authoritative_specs_block`, `_read_file`, callers, refs inline) + sibling no-`--file` pattern + `tests/cli/prd/test_prompts.py` conventions. Output `research/02-prompts-and-siblings.md`.
- Researcher 3 (Template & Examples): Template 02 PART 1 rules + `tests/cli/prd/` test patterns/fixtures + a prior `.dev/tasks/to-do/` example. Output `research/03-template-and-tests.md`.
- Other researchers covered: each is told the others' scope to avoid overlap.

## TEMPLATE_NOTES

- Template **02** (complex): involves edit → sync → test → verify with a final QA/reflect gate. Tier **Quick** (3 researchers, 0 web). QA gates in the generated task file per M3/I19 floors.
- Testing: UNIT (pytest under `tests/cli/prd/`). Validation: `make verify-sync` + `uv run pytest` + grep-guard `"--file"` absent.

## AMBIGUITIES_FOR_USER

None — intent is fully specified by the design spec (Option B chosen). Scope is strictly: remove both `--file` emissions, inline spec content via existing machinery, add tests, verify. No pipeline redesign.
