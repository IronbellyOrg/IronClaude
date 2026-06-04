# R2 — Patterns & Conventions of the Roadmap Pipeline Code

**Status:** Complete
**Date:** 2026-06-03
**Researcher:** R2 (task-builder)
**Scope:** `src/superclaude/cli/roadmap/{models.py,executor.py,gates.py,tool_writer.py,prompts.py}` + `tests/` layout
**Goal:** Extract reusable PATTERNS so the task builder can write items in house style.

---

## 0. KEY TAKEAWAY — Sync model (resolves a common task-builder mistake)

`make sync-dev` syncs ONLY `src/superclaude/{skills,agents}` → `.claude/` (Makefile `sync-dev:` target loops over `src/superclaude/skills/*/` and `src/superclaude/agents/*.md` only — confirmed Makefile lines under `sync-dev:`). **Nothing under `src/superclaude/cli/roadmap/` is mirrored to `.claude/`.** Edits to `models.py / executor.py / gates.py / tool_writer.py / prompts.py` are plain Python-package edits: NO `make sync-dev`, NO `make verify-sync` needed. The task should NOT include sync-dev/verify-sync steps for cli/ edits. (Only skill/agent edits would need that — and these 5 follow-ups are all cli/ + tests/.)

Test invocation is UV-only: `uv run pytest tests/roadmap/ -v`. Full suite = `uv run pytest`. 2098 tests collect from `tests/roadmap/`.

---

## 1. Config-flag pattern (`models.py`)

All `tool_write_*` flags live on the `@dataclass class RoadmapConfig(PipelineConfig)` (models.py:93-137) and `ValidateConfig` (models.py:140-155). House shape — a `bool = False` with a long **inline trailing comment** that always states: the R-number + Step number, what it gates, which render path (PLAIN `render_step_tool_write` vs id-check `render_step_tool_write_with_id_check`), the phantom-ID constraint status, and the closing sentence "Default False (markdown path is production) until cutover per Vector A >=3 release cycles." Examples:

- `tool_write_extract: bool = False  # R1.4 dual-write opt-in: ... Default False (markdown path is production) until cutover per Vector A >=3 release cycles.` (models.py:127)
- `tool_write_generate: bool = False  # R1.4 Step 9.4 ... generation-time phantom-ID rejection ...` (models.py:129)
- `tool_write_merge: bool = False  # ... render_step_tool_write_with_id_check ...` (models.py:133)
- `tool_write_validate_reflect: bool = False  # ... Wired in validate_run_step ...` lives on `ValidateConfig` not `RoadmapConfig` (models.py:155).

Frozenset enum-validation pattern (for new validated string fields) — `VALID_FINDING_STATUSES = frozenset({...})` at module top (models.py:15-18) + `__post_init__` raising `ValueError(f"Invalid ... {self.x!r}. Must be one of: {', '.join(sorted(...))}")` (models.py:50-60).

**What REMOVING a flag entails** (relevant to follow-up #5 spec_id_registry dual-write removal, and any flag-retirement):
1. Delete the flag declaration + its inline comment in `models.py`.
2. Delete the `getattr(config, _tw_spec.config_flag, False)` branch / `if config.tool_write_X:` consumer in `executor.py` (the executor reads flags via `getattr(config, spec.config_flag, False)` — tool_writer.py:181-184, executor.py:1257).
3. Delete the matching `TOOL_WRITE_REGISTRY` entry in `tool_writer.py` (lines 199-341) if it's a tool-write flag.
4. Remove/adjust the per-step test file `tests/roadmap/test_tool_write_step_<name>.py`.
5. Remove the `tool_write=config.tool_write_X` kwarg threaded into the `build_X_prompt(...)` call in `executor.py:_build_steps` (e.g. executor.py:2522).

---

## 2. Step construction pattern (`executor.py`)

Steps are built in `_build_steps` into `steps: list[Step | list[Step]]` (executor.py:2499) — a flat step is a `Step(...)`, parallel steps are a nested `[Step(...), Step(...)]` list. Canonical shape (executor.py:2502-2625):

Single LLM step (Diff, executor.py:2555-2565):
```python
Step(
    id="diff",
    prompt=build_diff_prompt(roadmap_a, roadmap_b, tool_write=config.tool_write_diff),
    output_file=diff_file,
    gate=DIFF_GATE,
    timeout_seconds=300,
    inputs=_llm_inputs_for(config, roadmap_a, roadmap_b),
    retry_limit=1,
),
```

Generate step (tool_write_mode + template_path + model + gate ternary; executor.py:2515-2533):
```python
Step(
    id=f"generate-{agent_a.id}",
    prompt=build_generate_prompt(agent_a, extraction, tdd_file=..., prd_file=..., tool_write=config.tool_write_generate),
    output_file=roadmap_a,
    gate=GENERATE_A_GATE,
    timeout_seconds=900,
    inputs=[extraction] + _llm_inputs_for(config, effective_tdd_file, config.prd_file),
    retry_limit=1,
    model=agent_a.model,
    tool_write_mode=_roadmap_template is not None,
    template_path=_roadmap_template,
),
```

Conventions worth matching:
- `gate=` is a module-level `*_GATE` constant from `gates.py` (or a ternary, e.g. `EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE`, executor.py:2506).
- `timeout_seconds`: extract 300 (1800 for TDD), generate/merge/debate 600-900, diff/score/test-strategy 300, non-LLM deterministic (anti-instinct) 30.
- `retry_limit=1` for LLM steps; `retry_limit=0` for the non-LLM deterministic anti-instinct step (executor.py:2634).
- `inputs=` built via the `_llm_inputs_for(config, *files)` helper; concatenated with `[extraction]`/`[debate_file]` lists.
- Step-numbering comments precede each Step: `# Step 1: Extract`, `# Steps 2a+2b: Generate (parallel)`, etc.
- `prompt=""` with comment `# non-LLM step; prompt unused` for deterministic steps (executor.py:2629).

The `build_X_prompt(..., tool_write: bool = False)` convention (prompts.py): every builder takes a defaulted `tool_write: bool = False` (prompts.py:563, 749, 1001); the docstring documents `tool_write:` (prompts.py:579,765,1011) and an `if tool_write:` branch appends the structured-output contract (prompts.py:715,959,1055). The default-False prompt MUST stay byte-identical to the pre-R1.4 prompt (load-bearing guarantee, see models.py:137 remediate note).

---

## 3. Gate pattern (`gates.py` + dispatch in `executor.py`)

GateCriteria instances are module-level constants under the `# --- GateCriteria instances ---` banner (gates.py:1062). Shape (gates.py:1064-1094):
```python
EXTRACT_GATE = GateCriteria(
    required_frontmatter_fields=[("spec_source", "spec_sources"), "generated", ...],  # tuples = "any-of" alias groups
    min_lines=50,
    enforcement_tier="STRICT",           # EXEMPT | LIGHT | STANDARD | STRICT
    semantic_checks=[
        SemanticCheck(name="...", check_fn=_some_pred, failure_message="..."),
    ],
)
```
- Aliasing: identical gates share one instance, `GENERATE_B_GATE = GENERATE_A_GATE` (gates.py:1191) — comment explains "share one criteria instance so adding/tuning a check happens in exactly one place."
- `SemanticCheck(name, check_fn, failure_message)` — check_fn is a module-level `_foo(...)` predicate; failure_message is the exact human string surfaced on failure.
- `CodeAssertion(name, check_fn, failure_message, ci_only=...)` for AST/dispatch-reachability assertions (gates.py:1451-1466 CERTIFY_GATE; gates.py:1481-1490 VERIFY_IMPLEMENTATION_GATE). `ci_only=True` means "source-tree AST walk; skipped in live gate path, enforced by tests/roadmap/test_dispatch_reachability.py" (gates.py:1460-1464).
- A CodeAssertion-only gate sets `required_frontmatter_fields=[]`, `min_lines=0`, `semantic_checks=None` so `gate_passed` runs zero content checks and dispatches only the assertion (gates.py:1476-1491).

`gate_passed` lives in `cli/pipeline/gates.py:20` (NOT cli/roadmap/) — signature:
```python
def gate_passed(output_file: Path, criteria: GateCriteria, *, envelope: object | None = None, repo_root: Path | None = None) -> tuple[bool, str | None]:
    # (True, None) on pass; (False, reason) on failure
```
NFR-007: `cli/pipeline/*` must NOT import from `cli/roadmap/*`, so `envelope` is typed `object` and `repo_root` is `Path | None` rather than the precise types (gates.py docstring lines 32-44). CI-only assertions are skipped even when envelope is plumbed.

**Render-dispatch in executor (executor.py:1233-1310):** the R1.4 tool-write render block. Resolves a `_tw_key` (extract→extract_tdd by input_type; `generate-*`→`generate`; else `step.id`), looks up `TOOL_WRITE_REGISTRY`, checks `getattr(config, _tw_spec.config_flag, False)`. Then:
- `if _tw_key in ("generate", "merge"):` → `render_step_tool_write_with_id_check(...)` deriving `spec_ids` from `extraction.json` sidecar (executor.py:1269-1296).
- `else:` → PLAIN `render_step_tool_write(...)` (executor.py:1297-1300).
- On non-empty error list → returns `StepResult(status=StepStatus.FAIL, gate_failure_reason="Step '{id}' tool-write schema/render failure: " + "; ".join(errors[:5]))` (executor.py:1301-1310).

---

## 4. Phantom-ID invariant style (`tool_writer.py`)

`validate_id_subset(roadmap_ids, spec_ids, accepted_deviations=None) -> list[str]` (tool_writer.py:344-370). Return-a-list-of-error-strings; **empty list == PASS**. The invariant is stated in the docstring exactly as:
```
roadmap_ids ⊆ set(spec_ids) ∪ set(accepted_deviations)
```
Error message format (one per offending id): `f"roadmap_id '{rid}' not in spec_ids ∪ accepted_deviations"` (tool_writer.py:367). Uses the `⊆` and `∪` unicode glyphs in docstrings/messages.

Generator-side gate `render_step_tool_write_with_id_check` (tool_writer.py:455-496) inserts the subset check BETWEEN schema validation and render; if `spec_ids` empty/falsy the check is SKIPPED (vacuous identity, tool_writer.py:487). On any id error → return errors, write NO artifact ("REJECTED AT GENERATION TIME", tool_writer.py:491-493).

Parallel Contract #9 primitive in `id_registry.py`: `SpecIdRegistry.contains(roadmap_id) -> bool` (id_registry.py:106-113) and `union_of_known() -> frozenset[str]` (id_registry.py:94-104). Invariant restated as `roadmap_id_set ⊆ spec_id_set ∪ accepted_deviation_id_set` (id_registry.py:11). Both `build_id_registry` and `extract_roadmap_ids` REUSE `spec_parser.extract_requirement_ids` (Contract #8 anti-duplication — "no duplicate regex literals", id_registry.py:19-25,141,183).

---

## 5. Error-handling convention (raise vs return)

- **Return list[str] of errors** (empty == PASS) for validation/gate logic: `validate_tool_output` (tool_writer.py:94-117), `validate_id_subset` (tool_writer.py:344-370), `render_step_tool_write` (tool_writer.py:421-452), the remediate_parser pure functions return `list[Finding]`.
- **Return `(bool, str | None)`** for gate-level pass/fail: `gate_passed` (pipeline/gates.py:20).
- **Raise** only for programmer/config errors that should abort: `FileNotFoundError` for a missing schema (tool_writer.py:87-90, with an "Available: [...]" hint listing siblings); `ValueError` in `__post_init__` for invalid enum values (models.py:52-59). `render_tool_output` uses Jinja2 `StrictUndefined` so a missing template field RAISES rather than silently emitting empty (tool_writer.py:143-155).
- **Permissive try/except for non-fatal I/O** that must not crash a step: `_save_id_registry` wraps `scan_accepted_deviation_records` in `try/except Exception` with `_log.warning` + `# pragma: no cover - defensive` (executor.py:643-647). The dual-write envelope path swallows failures with `[R1.2 dual-write] envelope update failed ...` log (executor.py:1419-1458). Fail-shut (NOT fail-open) is the doctrine for ID-registry resolution: a missing sidecar makes the MERGE check return a failure string, never silently pass (executor.py:3503-3519; conftest note "master:§Flaw 4 -- no fail-open defaults").

---

## 6. Module docstring / comment conventions (R-numbers, Contract #N, Vector A, dual-write)

- Module docstrings open with a one-line summary + a `(R1.4 / BUILD-REQUEST §MVR §3)` style provenance tag (tool_writer.py:1; id_registry.py:1-3 "Contract #9 enforcement primitive").
- References use stable shorthand: `master:§Flaw N`, `master:§Top-3 #N`, `master:§Recurrence #N`, `Contract #N`, `BUILD-REQUEST §R0 item 1`, `§MVR §3`, `Vector A`, `R0.1 / R1.2 / R1.4 / R5 (PR #111 port)`, `D-0003`, `FR-3 / NFR-007`, `AC-005`.
- "dual-write" = the side-by-side legacy-markdown + structured-JSON phase; always paired with the "Default False ... until cutover per Vector A >=3 release cycles" closing (models.py:127-136). R1.2 dual-write (envelope) vs R1.4 dual-write (tool-write per-step) are distinct — tag the R-number.
- PRESERVE markers: when code must stay byte-untouched it's flagged inline, e.g. "semantic_layer.py stays byte-untouched", "convergence.py / semantic_layer.py stay PRESERVE", "the LOAD-BEARING guarantee is that the default (False) prompt stays byte-identical".
- Status-lifecycle / enum docs cite the design clause: "Status lifecycle defined in D-0003: PENDING/ACTIVE -> FIXED|FAILED|SKIPPED (all terminal)" (models.py:25-29).

---

## 7. Test conventions (`tests/roadmap/`)

- Naming: `tests/roadmap/test_<area>.py`; tool-write per-step tests are `test_tool_write_step_<stepname>.py` (extract, generate, merge, diff, debate, score, spec_fidelity, test_strategy, certify, validate_reflect, remediation). A new tool-write step → mirror `test_tool_write_step_extract.py` (the generate test explicitly says "These tests mirror test_tool_write_step_extract.py", test_tool_write_step_generate.py:9-13).
- Test-file docstrings carry the same provenance tags as the code ("R1.4 generate-step ... master:§Top-3 #3 ... Contract #3", test_tool_write_step_generate.py:1-14).
- Imports come from `superclaude.cli.roadmap.{gates,models,prompts,tool_writer}` and `superclaude.contracts` (test_tool_write_step_generate.py:25-36).
- Fixtures dir: `tests/roadmap/fixtures/` (currently holds `recurrence/`). `tests/roadmap/conftest.py` re-exports the session-scoped `audit_trail` fixture from `tests/v3.3/conftest.py` and registers a permissive Contract #9 sidecar (`set_id_registry_sidecar_path`) for mock-subprocess MERGE_GATE tests (conftest.py:1-40+).
- Markers (pyproject.toml:113-137): `unit`, `integration`, `performance`, `slow`, `property_based`, `backward_compat`, `nfr_benchmark`, `gate_performance`, `agent_regression`, etc. `--strict-markers` is set (pyproject.toml:110) — any new marker MUST be registered in pyproject. `testpaths = ["tests"]` (pyproject.toml:104).
- Invocation: `uv run pytest tests/roadmap/ -v` (specific), `uv run pytest tests/roadmap/test_tool_write_step_generate.py -v` (one file). NEVER `python -m pytest`.
- Stale-test deletion (follow-up #1): there are dedicated regression files `test_no_fragility_stubs.py`, `test_recurrence_regression.py`, `test_anti_instinct_recurrence.py`, `test_dispatch_reachability.py`, `test_backward_compat.py` — these are the "invariant guard" tests; deleting/replacing a test should preserve any such guard.

---

## 8. MD-family reconciliation (follow-up #5 context)

`md_ids` is a first-class field on `SpecIdRegistry` (id_registry.py:67-72,89,102,128,173) — family `M{n}-D{nn}`, canonical `M{n}-D{m}`, added per R5 (PR #111 port) "so milestone-scoped deliverables are recognized as valid by the Contract #9 containment check instead of being collapsed under the bare-D family." The MD-vs-bare-D reconciliation lives in `spec_parser.py:347-371`: a dedup step "remove bare-D tokens that are the trailing portion of an MD-family token" to "preserve the family boundary (M{n}-D{nn} is a roadmap-internal deliverable)" (spec_parser.py:359-371). `extract_requirement_ids` is the SINGLE SoT for ID regex literals; `id_registry` + `contracts.ID_PATTERNS` (R0.3 hoist) source families from it, never re-defining the regex (Contract #8).

---

## Summary

All 8 patterns extracted with file:line evidence from actual code.

**Most load-bearing facts for the task builder:**
1. **No sync needed for cli/ edits** — `make sync-dev` covers only skills/agents; the 5 follow-ups touch `cli/roadmap/*` + `tests/` only. Do not include sync-dev/verify-sync steps.
2. **Config-flag removal is a 5-touchpoint operation** (models flag + inline comment, executor consumer/getattr branch, TOOL_WRITE_REGISTRY entry, per-step test file, prompt kwarg). Document all five in any flag-retirement item.
3. **Validation returns `list[str]` (empty==PASS)**; gates return `(bool, str|None)`; raise only for FileNotFoundError (missing schema) / ValueError (bad enum) / Jinja StrictUndefined. Fail-shut, never fail-open, for ID-registry.
4. **Phantom-ID invariant** is `roadmap_ids ⊆ spec_ids ∪ accepted_deviations`, enforced generation-time in `render_step_tool_write_with_id_check` + `validate_id_subset` (tool_writer.py) and via `SpecIdRegistry.contains` (id_registry.py); both reuse `spec_parser.extract_requirement_ids` (Contract #8, no duplicate regex).
5. **Tests** mirror `test_tool_write_step_extract.py`; `--strict-markers` means new markers must be registered in pyproject; run with `uv run pytest tests/roadmap/ -v`.

**Status:** Complete
