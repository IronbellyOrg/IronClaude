# R7 — Test & Verification Research

**Status:** Complete
**Date:** 2026-06-03
**Topic:** Test & Verification — how each of the 5 follow-up changes is tested deterministically, plus existing test landscape and CI gates.
**Scope:** `tests/roadmap/`, `tests/integration/`, `tests/contracts/`, `tests/roadmap/fixtures/`, `pyproject.toml`/`Makefile` test config, CI.

The 5 areas:
- **(A)** delete `tests/integration/test_wiring_pipeline.py`
- **(B)** generation-time phantom-ID prevention in `tool_writer.py`/`executor.py`
- **(C)** opus-architect/spec-fidelity perf (mostly non-unit-testable)
- **(D)** markdown-path deletion (precondition-gated)
- **(E)** spec_id_registry dual-write removal + remediate_parser.py + MD-family reconciliation

---

## 0. Baseline state (run 2026-06-03, evidence)

| Check | Command | Result |
|---|---|---|
| Full-suite collection | `uv run pytest --collect-only -q` | **7909 tests collected, 1 error** — `Interrupted: 1 error during collection` |
| Integration collection | `uv run pytest --collect-only tests/integration/ -q` | **26 collected, 1 error** |
| The single error | — | `ERROR tests/integration/test_wiring_pipeline.py` → `ImportError: cannot import name 'WIRING_GATE' from 'superclaude.cli.roadmap.gates'` (`test_wiring_pipeline.py:28`) |

**Why it errors:** `WIRING_GATE` was removed from `src/superclaude/cli/roadmap/gates.py` when the wiring-verification step was REPLACED by the terminal `verify-implementation` step (R1.5; see `gates.py:1474` "REPLACES wiring-verification" and `gates.py:1582`). `test_wiring_pipeline.py` is a stale relic still importing the deleted symbol. Because pytest collection imports every test module, this single ImportError **interrupts the whole collection** (exit non-zero) — it is a hard CI failure, not an isolated test failure.

**Disambiguation (do NOT over-delete):** `WIRING_GATE` still legitimately exists in a *different* module, `src/superclaude/cli/audit/wiring_gate.py:1024`. Two other test files import it FROM THERE and are fine:
- `tests/roadmap/test_eval_gate_rejection.py:21` → `from superclaude.cli.audit.wiring_gate import WIRING_GATE` (its docstring at lines 10-12 explicitly notes the symbol is preserved in the audit module).
- `tests/audit/test_wiring_gate.py` (audit suite).
Only `tests/integration/test_wiring_pipeline.py` imports the now-deleted `cli.roadmap.gates.WIRING_GATE`. Deleting just that one file is the surgical fix.

---

## 1. Test inventory (relevant to the 5 areas)

### tool_writer / phantom-ID (Areas B, D)
- `tests/roadmap/test_tool_write_step_generate.py` (17.4K, 12 tests) — schema load, id-pattern parity vs Contract #3 `ID_PATTERNS`, render parity, and the **generation-time phantom-ID tests**: `test_id_check_skips_when_spec_ids_empty` (374), `test_render_step_tool_write_with_id_check_rejects_invalid` (390), plus a clean-pass id-check case (~355-371). `build_generate_prompt` asserts the word "phantom" is in the prompt (418).
- `tests/roadmap/test_tool_write_step_merge.py` (24K) — merge is the **SECOND** primary phantom-ID source. `test_merge_rejects_phantom_id` (488) asserts `validate_id_subset(["FR-1","FR-99"], spec_ids=...)` returns an error mentioning FR-99 and neither `.md` nor `.json` is written; `test_all_schemas_accept_md_family` (363) is the **MD-family reconciliation** regression (guards against the schema arm omitting `MD-` ids).
- The other 10 `test_tool_write_step_*.py` (extract, extract_tdd, diff, debate, score, spec_fidelity, test_strategy, certify, validate_reflect, remediation) — each verifies its registry entry (`config_flag`, `schema_name`, `template_name`), schema validation, and render parity. **161 passed** for the whole `test_tool_write_step_*` glob.
- `tests/roadmap/test_spec_roadmap_id_containment.py` (12.6K, 12 tests) — Contract #9 / MERGE_GATE containment. `test_phantom_id_rejected` (75), `test_spec_ids_contained_when_roadmap_matches_spec` (128), `test_accepted_deviation_allows_otherwise_phantom_id` (152), and registry-shape asserts on `fr_ids/nfr_ids/d_ids`. This is the **merge-gate-side** check (`_gates._roadmap_ids_within_spec`), complementary to the generate-side check in B.
- `tests/roadmap/test_pipeline_envelope.py` (13K, ~12 tests) — PipelineEnvelope round-trip, dispatch-map canonical step ids, `test_dual_write_preservation` (per docstring §6: the dual-write helper never mutates the step's existing markdown). Relevant to Area E envelope absorption.
- `tests/roadmap/test_parser_consistency.py` (10.6K, ~30 tests) — canonical-parser determinism, golden-corpus parametrize, CRLF==LF, "legacy parser removed" asserts, "both gate layers route through canonical parser" (183). Relevant to Area E (must still pass after dual-write removal).

### wiring (Area A)
- `tests/integration/test_wiring_pipeline.py` (13.5K) — **the file to delete.** Tests an end-to-end wiring-verification step + `WIRING_GATE` from `cli.roadmap.gates` (both removed). Stale.
- Survivors in `tests/integration/`: `test_pytest_plugin.py`, `test_sprint_wiring.py` (sprint-mode wiring, unrelated), `test_wiring_e2e_shadow.py` (shadow-mode pipeline — collects fine).

### id_registry / threshold (Area E)
- `tests/roadmap/test_threshold_registry.py` (14.5K, ~24 tests) — arch-lint over `id_registry.py` (single-definition of constants, consumers import from `superclaude.contracts`, no orphan literals). Does **not** test the `spec_id_registry.json` write directly, but `id_registry.py` is in its scanned consumer set (line 41).
- `tests/contracts/test_arch_lint.py` (10.4K, 19 tests) — architecture lint gate; **19 passed**.

---

## 2. Test patterns

**Fixtures.** `tests/roadmap/conftest.py` provides: session-scoped `audit_trail`, `results_dir`, `recurrence_corpus_dir` (→ `tests/roadmap/fixtures/recurrence/`), and `recurrence_case` (parametrized loader, used as `@pytest.mark.parametrize("recurrence_case", [("id_containment","spec_roadmap_drift_case")], indirect=True)`). Crucially it also defines `_merge_gate_id_registry_sidecar` (conftest.py:52) — a fixture that writes a **permissive `spec_id_registry.json`** into `tmp_path` and registers it via `set_id_registry_sidecar_path` so MERGE_GATE integration fixtures (which use mock pipelines, no real executor) can resolve the sidecar. **This fixture is a load-bearing reader of `spec_id_registry.json` for tests** — relevant to Area E (see §5).

**Tool-writer test idiom** (mocking style = none; pure functions over JSON + tmp_path). Real example, the generate-side phantom-ID check (`tests/roadmap/test_tool_write_step_generate.py:390-397`):

```python
def test_render_step_tool_write_with_id_check_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "roadmap.md"
    errors = render_step_tool_write_with_id_check(
        "generate", "{not valid json", out, spec_ids={"FR-1"}
    )
    assert errors
    assert not out.exists()
    assert not (tmp_path / "roadmap.json").exists()
```

And the phantom-skip-on-empty case (lines 374-387) confirms that empty `spec_ids` → check skipped (identity). Parametrize is used heavily in `test_parser_consistency.py` (golden corpus) and `test_spec_roadmap_id_containment.py` (`recurrence_case`).

**The underlying functions** (`src/superclaude/cli/roadmap/tool_writer.py`):
- `validate_id_subset(roadmap_ids, spec_ids, accepted_deviations)` (344) — returns one error string per id NOT in `spec_ids ∪ accepted_deviations`; **empty list = PASS**; empty `spec_ids` is the identity (skip).
- `render_step_tool_write_with_id_check(step_id, json_text, output_path, spec_ids, accepted_deviations)` (455) — parse → schema-validate → **subset gate** → persist+render. On any failure it writes NEITHER the `.md` NOR the `.json` sidecar (485-496).
- `render_step_tool_write(...)` (421) — same WITHOUT the id gate (used by non-phantom steps).

---

## 3. Area A verification (delete `test_wiring_pipeline.py`)

**Proof the collection error is gone** after `git rm tests/integration/test_wiring_pipeline.py`:

```bash
uv run pytest --collect-only tests/integration/ -q   # expect: "N collected" with 0 errors
uv run pytest --collect-only -q                        # full suite: "7908 collected" (was 7909+1err), 0 errors
```

Baseline (current, before fix): `26 tests collected, 1 error` (integration) / `7909 tests collected, 1 error` (full) — confirmed by run in §0. After deleting the file the integration count drops by however many tests that module defined and the **error count must be 0** (no "Interrupted: ... error during collection" line). The decisive assertion is the absence of any `ERROR tests/...` line and a zero exit code from `--collect-only`.

**No new test needed for Area A** — the verification is a collection check, not a test. Optionally, a one-line guard test could assert the stale module is gone (mirroring the `test_legacy_*_parser_removed` idiom at `test_parser_consistency.py:170/177`), e.g. assert the import path no longer resolves. This is optional, not required.

---

## 4. Area B test design (generation-time phantom-ID PREVENTION)

**KEY FINDING — the capability already exists and is wired.** Generation-time phantom-ID rejection is implemented in `render_step_tool_write_with_id_check` (tool_writer.py:455) and **already called by the executor** for both `generate` and `merge` steps:

`src/superclaude/cli/roadmap/executor.py:1269-1296`:
```python
if _tw_key in ("generate", "merge"):
    # ... derive _spec_ids from <output_dir>/extraction.json ...
    _tw_errors = render_step_tool_write_with_id_check(
        _tw_key, _json_text, step.output_file,
        spec_ids=_spec_ids, accepted_deviations=None,
    )
else:
    _tw_errors = render_step_tool_write(_tw_key, _json_text, step.output_file)
```

So the function-level + render-level regression tests **already exist**: `test_tool_write_step_generate.py:390` and `test_tool_write_step_merge.py:488`. What is NOT yet covered is an **executor-integration** test proving the wiring (`_tw_key in ("generate","merge")` → id-check is invoked with spec_ids derived from `extraction.json`, and a phantom id makes the STEP fail with status FAIL rather than writing a polluted artifact).

**Recommended deterministic regression test** (the missing executor-level proof):
- **Target file:** new `tests/roadmap/test_generation_phantom_id_prevention.py` (focused, name matches the area) — OR extend `tests/roadmap/test_executor.py` (already exercises the tool-write render branch).
- **Fixture:** a `tmp_path` `output_dir` containing `extraction.json` with `{"roadmap_ids": ["FR-1","FR-2"]}` (the spec_ids universe), and a `generate`/`merge` step whose `output_file` holds schema-valid JSON whose `roadmap_ids` includes a phantom `FR-99`. Set `config.tool_write_generate = True` (or `tool_write_merge`).
- **Assertion:** the executor's per-step render branch returns a `StepResult` with `status == StepStatus.FAIL` and `gate_failure_reason` containing `"FR-99"`/`"not in spec_ids"`; AND the `.md` output artifact + `.json` sidecar were NOT written (`not step.output_file.exists()`).
- **Determinism:** pure file I/O over `tmp_path`, no LLM, no network — fully deterministic.

A second, lighter assertion (function level, mirroring existing tests) belongs in the same file for the "no `extraction.json` ⇒ empty spec_ids ⇒ skip" path, to lock the documented identity behaviour.

---

## 5. Area E test design (dual-write removal + remediate_parser + MD-family)

**The dual-write:** `_save_id_registry` (executor.py:611-675) writes `<output_dir>/spec_id_registry.json`; the same `SpecIdRegistry` is ALSO absorbed into `PipelineEnvelope.spec_ids` (envelope.py:146-168). The R1.6 cutover (envelope.py:165-168 `.. todo:: R1.6 — delete spec_id_registry.json writes once gate logic reads envelope.spec_ids directly`) is exactly this area.

**The stranded-reader risk — what breaks if `spec_id_registry.json` stops being written:**
1. **MERGE_GATE** — `gates.py:996 _roadmap_ids_within_spec` reads the sidecar via `set_id_registry_sidecar_path`; if the file is gone and the gate isn't repointed at `envelope.spec_ids`, the gate returns `"Contract #9: could not read spec_id_registry sidecar..."` (gates.py:1024) → **every merge step fails**. This is the primary risk; removal MUST be paired with repointing the gate's reader.
2. **Test fixture** — `tests/roadmap/conftest.py:52 _merge_gate_id_registry_sidecar` writes and registers the sidecar; if production stops reading the sidecar, this fixture (and any MERGE_GATE integration test relying on it) needs to be migrated to feed `envelope.spec_ids` instead, or it silently no longer exercises the real path.
3. **Containment tests** — `test_spec_roadmap_id_containment.py` exercises `_roadmap_ids_within_spec` directly with a registered sidecar (`extract_roadmap_ids`, registry-shape asserts). These MUST still pass after the reader is repointed.

**Tests that MUST still pass after dual-write removal** (regression set):
- `tests/roadmap/test_spec_roadmap_id_containment.py` (Contract #9 containment — the gate's behaviour must be byte-identical whether it reads sidecar or envelope).
- `tests/roadmap/test_parser_consistency.py` (canonical-parser determinism + "both gate layers route through canonical parser", 183).
- `tests/roadmap/test_pipeline_envelope.py` (envelope round-trip + dual-write-preservation).
- `tests/roadmap/test_remediate_parser.py` — relevant because the remediate parser extracts finding records (10-field `Finding`) and MD-family ids must round-trip through it (the parse-extraction step is part of the MD-family lineage).

**MD-family reconciliation regression:** `tests/roadmap/test_tool_write_step_merge.py:363 test_all_schemas_accept_md_family` already guards that every tool-write schema's `roadmap_ids` pattern accepts an `MD-` id and rejects a non-family token. `id_registry.py:89,128,173 md_ids` is the SoT for the MD family. If dual-write removal touches `SpecIdRegistry.to_dict()` / `from_dict()`, add a round-trip assertion that `md_ids` survives `to_dict → envelope.spec_ids → gate read` unchanged. Recommended: extend `test_pipeline_envelope.py` (envelope is now the SoT) with `test_envelope_spec_ids_preserve_md_family`.

---

## 6. CI / make gates

| Gate | File / target | Command | Collects ALL tests? |
|---|---|---|---|
| Full test (CI) | `.github/workflows/test.yml:56` | `pytest -v --tb=short --color=yes` (no path filter) | **YES** — currently **broken** by the Area A collection error (exit non-zero) |
| Coverage (CI) | `.github/workflows/test.yml:61` | `pytest --cov=superclaude ...` | YES — also broken |
| Quick check (CI) | `.github/workflows/quick-check.yml:33` | `pytest tests/unit/ -x` | NO — only `tests/unit/`, unaffected by Area A |
| Lint (CI) | `test.yml:96` / `quick-check.yml:37` | `ruff check src/ tests/` | n/a |
| Contract #3 lint (CI) | `.github/workflows/contract3-generator-constraint-lint.yml` | PR-body grep gate — fires only when `gates.py`/`structural_checkers.py`/`*_validator.py` is touched; requires a `## Generator-Constraint Considered` PR-body section | n/a |
| `make test` | `Makefile:13-15` | `uv run pytest` | YES — broken (same root cause) |
| `make lint` | `Makefile:48-50` | `lint-architecture` + `ruff check .` | n/a |
| `make verify-sync` | `Makefile:166` | src/ ↔ .claude/ parity | n/a |

**pytest config** (`pyproject.toml:103-137`): `testpaths=["tests"]`, `addopts=["-v","--strict-markers","--tb=short"]`, `--strict-markers` is ON (any unknown marker is an error). 22 custom markers registered; none specifically gate the 5 areas. Coverage source = `src/superclaude` (139).

**Bottom line for CI:** Area A's collection error currently fails `test.yml` and `make test` for the whole repo. Fixing Area A is a **prerequisite to a green CI** for any of the other areas.

---

## 7. Recommended phase-gate verification commands

| Area | Verification command(s) | New / changed test |
|---|---|---|
| **A** delete `test_wiring_pipeline.py` | `uv run pytest --collect-only -q 2>&1 \| tail -3` → assert "0 errors", no `Interrupted`; then `uv run pytest tests/integration/ -q` | None required (collection check). Optional: a `test_legacy_wiring_pipeline_module_removed` guard. |
| **B** gen-time phantom-ID prevention | `uv run pytest tests/roadmap/test_tool_write_step_generate.py tests/roadmap/test_tool_write_step_merge.py tests/roadmap/test_spec_roadmap_id_containment.py -q` (currently **179+ pass**) + new executor-integration test | NEW `tests/roadmap/test_generation_phantom_id_prevention.py` (executor-level: phantom `FR-99` in generate/merge JSON + `extraction.json` spec_ids ⇒ StepResult FAIL, no artifact written). |
| **C** opus-architect/spec-fidelity perf | `uv run pytest tests/roadmap/test_spec_fidelity.py tests/roadmap/test_tool_write_step_spec_fidelity.py -q` (regression-only; perf is largely non-unit-testable — gate on no behavioural change) | None (no deterministic perf unit test); rely on existing spec-fidelity regression. |
| **D** markdown-path deletion (precondition-gated) | `uv run pytest tests/roadmap/test_tool_write_step_*.py tests/roadmap/test_executor.py -q` (tool-write glob = **161 pass**) | Changed: any test asserting the markdown path is still reachable when its `tool_write_*` flag is False (precondition); add executor test that with flag True the markdown is rendered from JSON, with flag False the legacy path runs. |
| **E** dual-write removal + remediate + MD-family | `uv run pytest tests/roadmap/test_spec_roadmap_id_containment.py tests/roadmap/test_parser_consistency.py tests/roadmap/test_pipeline_envelope.py tests/roadmap/test_remediate_parser.py tests/roadmap/test_threshold_registry.py -q` (currently green) | Changed: repoint MERGE_GATE reader to `envelope.spec_ids` and migrate `conftest.py:_merge_gate_id_registry_sidecar`. NEW `test_envelope_spec_ids_preserve_md_family` in `test_pipeline_envelope.py`. |
| **Whole-suite green** | `uv run pytest -q` (mirrors `test.yml:56` / `make test`) | — |

**Suggested single baseline-green command** (the 5-area regression set, fast, deterministic, no network):
```bash
uv run pytest tests/roadmap/test_tool_write_step_generate.py tests/roadmap/test_tool_write_step_merge.py tests/roadmap/test_spec_roadmap_id_containment.py tests/roadmap/test_parser_consistency.py tests/roadmap/test_pipeline_envelope.py tests/roadmap/test_remediate_parser.py tests/roadmap/test_threshold_registry.py tests/contracts/test_arch_lint.py -q
```
Confirmed today: the first 6 of these = **179 passed, 1 skipped**; the full `test_tool_write_step_*` glob = **161 passed**; `test_arch_lint.py` = **19 passed**.

---

## Status: Complete

### Summary

- **Area A baseline confirmed:** the full pytest suite currently fails collection — `7909 tests collected, 1 error` (`Interrupted`), root cause `tests/integration/test_wiring_pipeline.py:28` importing the deleted `WIRING_GATE` from `cli.roadmap.gates`. This breaks `test.yml` CI (`pytest` with no path filter, line 56) and `make test`. Deleting that single stale file is the surgical fix; `WIRING_GATE` legitimately survives in `cli/audit/wiring_gate.py` (imported by `test_eval_gate_rejection.py:21` and `tests/audit/`), so do not over-delete. Verification = `uv run pytest --collect-only -q` returns 0 errors.
- **Area B is largely already built:** `render_step_tool_write_with_id_check` + `validate_id_subset` (tool_writer.py:455/344) implement generation-time phantom-ID rejection and the executor already routes `generate`+`merge` through it (executor.py:1269-1296), deriving spec_ids from `extraction.json`. Function/render tests exist (`test_tool_write_step_generate.py:390`, `test_tool_write_step_merge.py:488`). The gap is an **executor-integration** regression proving the wiring + FAIL-on-phantom-no-artifact; recommend new `tests/roadmap/test_generation_phantom_id_prevention.py`.
- **Area E hinges on a single stranded reader:** removing the `spec_id_registry.json` dual-write strands MERGE_GATE's `_roadmap_ids_within_spec` (gates.py:996/1024) and the test fixture `conftest.py:_merge_gate_id_registry_sidecar` — both must be repointed to `envelope.spec_ids` (the R1.6 cutover already TODO'd at envelope.py:165). MD-family reconciliation is already guarded by `test_all_schemas_accept_md_family` (merge test:363); add an envelope round-trip MD-family assertion.
- **CI:** `test.yml` and `make test` collect ALL tests (broken by Area A now); `quick-check.yml` only runs `tests/unit/` (unaffected). Contract #3 lint is a PR-body grep gate triggered by gates/validator edits.
- **All 5-area regression files are green today** (179 + 1 skip; 161 tool-write; 19 arch-lint) — a clean pre-change baseline.
