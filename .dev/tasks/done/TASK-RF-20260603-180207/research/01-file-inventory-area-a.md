# Research: File Inventory + Area A (stale test deletion)

- Topic type: File inventory across 5 follow-up areas + deep dive on Area A deletion safety
- Scope: Inventory file surface (paths, exports, line counts, intra-project imports) for Areas A-E; fully research Area A (`tests/integration/test_wiring_pipeline.py` deletion)
- Status: Complete
- Date: 2026-06-03

---

## Area A — Stale Test Deletion (`tests/integration/test_wiring_pipeline.py`)

### A.1 Collection error confirmed (evidence)

`uv run pytest tests/integration/test_wiring_pipeline.py --collect-only`:

```
collected 0 items / 1 error
ImportError while importing test module '.../tests/integration/test_wiring_pipeline.py'.
tests/integration/test_wiring_pipeline.py:28: in <module>
    from superclaude.cli.roadmap.gates import ALL_GATES, WIRING_GATE
E   ImportError: cannot import name 'WIRING_GATE' from 'superclaude.cli.roadmap.gates'
```

This is the ONLY collection error in the entire suite. Full-suite
`uv run pytest --collect-only -q` → `collected 7909 items / 1 error / 1 skipped`,
and the one error is `ERROR tests/integration/test_wiring_pipeline.py`. Because pytest
aborts collection on error (`Interrupted: 1 error during collection`), this single stale
file blocks whole-suite collection. Deleting it unblocks the suite.

### A.2 Why the import fails — `WIRING_GATE` was relocated AND the step removed

- `roadmap/gates.py` no longer defines `WIRING_GATE`. `grep WIRING_GATE src/superclaude/cli/roadmap/gates.py` → only comment references to `ALL_GATES` wiring; no symbol.
- `WIRING_GATE` now lives ONLY in `src/superclaude/cli/audit/wiring_gate.py:1024` (`WIRING_GATE = GateCriteria(...)`, 16 frontmatter fields + 5 semantic checks).
- Runtime confirmation: `dict(ALL_GATES)` keys are
  `['extract','generate-A','generate-B','diff','debate','score','merge','anti-instinct','test-strategy','spec-fidelity','deviation-analysis','remediate','certify','verify-implementation']`.
  `'wiring-verification' in ALL_GATES` → **False**.
- Per `tests/roadmap/test_eval_gate_rejection.py:10-12` and `tests/roadmap/test_eval_gate_ordering.py:58-132`:
  **R1.5 REMOVED the static `wiring-verification` step from `_build_steps` and REPLACED it
  (and its ALL_GATES slot) with dynamic `verify-implementation`.**

Consequence: even if line 28 were repaired to import `WIRING_GATE` from
`audit/wiring_gate`, the test would STILL fail at runtime because it asserts a deleted
architecture (see A.4). The file is testing a pipeline shape that no longer exists.

### A.3 Nothing else imports / references the test module

`grep -rn "test_wiring_pipeline"` across `*.py/*.toml/*.cfg/*.ini` (excluding the file
itself) → **no matches**. No conftest, no pytest config, no other module imports it. Safe
to remove with zero dangling references.

### A.4 Coverage analysis — what the 4 test classes assert, and where it is re-homed

| Class in deleted file | What it asserts | Status under R1.5 arch | Equivalent live coverage |
|---|---|---|---|
| `TestWiringVerificationEndToEnd` (3 tests) | pipeline runs a STATIC `wiring-verification` step; `len(results)==13`; step uses `GateMode.TRAILING`; positioned after `spec-fidelity`, before `remediate` | **Obsolete** — `wiring-verification` step removed from `_build_steps` (R1.5). `_get_all_step_ids` no longer contains it. | `tests/roadmap/test_eval_gate_ordering.py:58-138` (`test_step_count`, `test_wiring_verification_removed`, ordering tests) + `tests/roadmap/test_pipeline_integration.py` cover the CURRENT step set. The wiring-step E2E is intentionally gone. |
| `TestWiringGatePassed` (4 tests) | `gate_passed(report, WIRING_GATE)` accepts valid shadow / rejects missing / rejects incomplete frontmatter; `"wiring-verification" in ALL_GATES` and `ALL_GATES["wiring-verification"] is WIRING_GATE` | gate_passed behavior **still valid**; the `in ALL_GATES` assertion is **obsolete** (now False) | `tests/audit/test_wiring_gate.py:809-870` (`TestGatePassedIntegration`: shadow/soft/full mode pass+reject via `gate_passed(out, WIRING_GATE)`) and `tests/audit/test_wiring_gate.py:651-693` (WIRING_GATE definition: 16 fields, 5 semantic checks, STRICT tier). `tests/roadmap/test_eval_gate_rejection.py:597-617` adds WIRING_GATE rejection (`gate_passed(f, WIRING_GATE)`). The ALL_GATES-membership assertion is correctly DROPPED (it no longer holds). |
| `TestWiringVerificationResume` (2 tests) | `_apply_resume` skips a completed `wiring-verification` step / re-runs it when its gate fails | **Obsolete** — relies on the removed step | Generic resume logic covered by `tests/roadmap/test_resume.py`, `test_resume_restore.py`; wiring-specific resume is gone with the step. |
| `TestNFR007Compliance` (1 test) | `audit/wiring_gate.py` does not import from `pipeline/*` except `pipeline.models` | **Still meaningful** but NOT exactly duplicated | `tests/roadmap/test_nfr_compliance.py` (`TestNFR007*`) tests the REVERSE direction (`pipeline/*` does not import `roadmap/*` or `sprint/*`) — directionally different. The deleted test's "wiring_gate.py must not import pipeline (except models)" assertion is the ONLY place that exact NFR-007 direction is checked. See A.5 risk. |

### A.5 Risk: one assertion has no exact re-home (`TestNFR007Compliance.test_no_pipeline_imports_in_wiring_gate`)

This is the single piece of arguably-unique coverage. It guards that
`audit/wiring_gate.py` stays decoupled from `cli/pipeline/*` (architectural boundary).
The closest existing test, `tests/roadmap/test_nfr_compliance.py::TestNFR007*`, asserts the
opposite-direction invariant (`pipeline/*` files do not import `roadmap/`/`sprint/`), so it
does NOT cover `wiring_gate.py → pipeline` imports.

Severity: LOW.
- It is a static AST guard, not behavioral coverage.
- `audit/wiring_gate.py` currently imports `GateCriteria`/`SemanticCheck` etc. from
  `pipeline.models` only (verified: `grep "pipeline" src/superclaude/cli/audit/wiring_gate.py`
  shows model-only imports), so the invariant currently holds and is unlikely to silently
  regress.
- Recommendation: re-home this one AST check into `tests/audit/test_wiring_gate.py` (a small
  `TestNFR007Compliance` class, ~20 lines) BEFORE/ALONGSIDE deletion to preserve the boundary
  guard. This is cheap and keeps the architectural invariant enforced. (Owner: task item should
  call this out as the only re-homing requirement.)

### A.6 `WIRING_GATE` symbol + wrapper are NOT orphaned by the deletion

- The "run_all_semantic_checks" wrapper named in the brief is actually
  `check_wiring_report(content) -> tuple[bool, list[str]]` at
  `src/superclaude/cli/audit/wiring_gate.py:1102` (iterates `WIRING_GATE.semantic_checks`).
- Live (non-test) `src/` consumers of the `WIRING_GATE` CONSTANT or `check_wiring_report`:
  **none** (`grep -rn "WIRING_GATE\|check_wiring_report" src/ | grep -v wiring_gate.py` → empty).
  Both are used internally within `wiring_gate.py` and exercised by tests.
- BUT the `wiring_gate` MODULE is live: `src/superclaude/cli/sprint/kpi.py:21` imports
  `WiringReport`; `src/superclaude/cli/sprint/executor.py:502,728` import `run_wiring_analysis`.
  So the module is NOT dead — deleting the test does not orphan the module.
- Test consumers of `WIRING_GATE` that REMAIN after deletion (so the constant stays exercised):
  - `tests/audit/test_wiring_gate.py` (definition + gate_passed integration, ~10 refs)
  - `tests/roadmap/test_eval_gate_rejection.py:21,606,617` (direct gate_passed rejection)
  - `tests/v3.3/test_wiring_points_e2e.py:22,2691-2794` (delegation: `check_wiring_report` →
    5 `WIRING_GATE.semantic_checks`)
- Test consumers of `check_wiring_report`: `tests/v3.3/test_wiring_points_e2e.py` only.

Net: `WIRING_GATE` and `check_wiring_report` retain robust live test coverage after deletion;
the symbol must STAY in `audit/wiring_gate.py` (matches the brief's requirement).

---

## File Inventory — All 5 Areas

All `src/` paths are relative to `src/superclaude/cli/`. Line counts via `wc -l` (2026-06-03).
"Intra imports" = imports of other in-project modules only (stdlib/3rd-party omitted).

### Area A — stale test deletion

| Path | LOC | 1-line purpose | Key exports (sig) | Intra imports |
|---|---|---|---|---|
| `tests/integration/test_wiring_pipeline.py` | 379 | **TO DELETE** — E2E tests for removed `wiring-verification` pipeline step | 4 test classes (see A.4) | `pipeline.executor.execute_pipeline`, `pipeline.gates.gate_passed`, `pipeline.models.{GateMode,StepResult,StepStatus}`, `roadmap.executor._build_steps/_apply_resume/_get_all_step_ids`, `roadmap.gates.{ALL_GATES,WIRING_GATE}` (BROKEN: WIRING_GATE gone), `roadmap.models.{AgentSpec,RoadmapConfig}` |
| `audit/wiring_gate.py` | 1122 | Wiring-verification AST analyzers + `WIRING_GATE` GateCriteria + report emit/check | `class WiringFinding`, `class WiringReport`, `analyze_unwired_callables(...)`, `analyze_orphan_modules(...)`, `analyze_registries(...)`, `run_wiring_analysis(...)`, `emit_report(report, output_path)->Path`, `blocking_for_mode(report)->bool`, `check_wiring_report(content)->tuple[bool,list[str]]` (l.1102), `WIRING_GATE = GateCriteria(...)` (l.1024, 16 fields + 5 semantic checks) | `audit.wiring_config.*`, `pipeline.models.{GateCriteria,SemanticCheck}` (l.1022, **models-only** — NFR-007 holds) |
| `roadmap/gates.py` | 1585 | Roadmap pipeline gate criteria + semantic-check predicates + `ALL_GATES` registry | `ALL_GATES` (l.1566, 14 entries), `set_id_registry_sidecar_path(path)`, ~40 `_*` semantic-check predicates (e.g. `_roadmap_ids_within_spec`, `_no_undischarged_obligations`) | `pipeline.frontmatter.extract_frontmatter`, `pipeline.models.{CodeAssertion,GateCriteria,SemanticCheck}`, `roadmap.code_assertions.*`, `roadmap.verify_implementation.assert_all_frs_resolved`, `contracts.{GATE_FIELD_NAMES,THRESHOLDS}` |

### Area B — tool_writer phantom-ID (deep dive: R3)

| Path | LOC | 1-line purpose | Key exports (sig) | Intra imports |
|---|---|---|---|---|
| `roadmap/tool_writer.py` | 496 | Tool-call schema load/validate/render + ID-subset enforcement for tool-write steps | `class ToolDefinition` (l.42), `load_schema(name)->dict`, `validate_tool_output(out,schema)->list[str]`, `render_tool_output(out,template_path)->str`, `class ToolWriteSpec` (l.171), `validate_id_subset(...)` (l.344), `render_step_tool_write(...)` (l.421), `render_step_tool_write_with_id_check(...)` (l.455) | **none** (no in-project imports — leaf module; exposes `TEMPLATES_DIR`) |
| `roadmap/envelope.py` | 726 | Pipeline envelope dataclasses + (de)serialize + per-step post-extractors | `class ArtifactRef`, `class AcceptedDeviation`, `class PipelineEnvelope` (l.128), `envelope_to_dict`/`envelope_from_dict`, `save_envelope`/`load_envelope`, `get_post_extractor(step_id)->Optional[PostExtractor]` (l.713), 13 `extract_*_envelope_fields` funcs | `roadmap.convergence.ConvergenceResult`, `roadmap.id_registry.SpecIdRegistry`, `roadmap.models.Finding` |
| `roadmap/executor.py` | 4266 | Roadmap pipeline orchestration — step build, run, resume, state, sidecar persistence | `detect_input_type(spec_file)->str`, `roadmap_run_step(...)` (l.1464), `class _ClaudeRunner` (l.1496), `build_certify_step`, `execute_roadmap(...)` (l.3522), `write_state`/`read_state`, `apply_decomposition_pass`, `derive_pipeline_status`; **internal** `_build_steps`/`_apply_resume`/`_get_all_step_ids` (used by deleted test); writes `spec_id_registry.json` sidecar (l.650,666) | `pipeline.deliverables.decompose_deliverables`, `pipeline.executor.execute_pipeline`, `pipeline.models.*`, `pipeline.process.ClaudeProcess`, `compression.compress_file`, `.certify_prompts`, `.gates`, `.models`, `.prompts`, `.templates`, `.verify_implementation.build_verify_implementation_step` |
| `roadmap/id_registry.py` | 194 | Spec ID registry model + builder + roadmap-ID extractor | `class SpecIdRegistry` (l.44), `build_id_registry(...)` (l.135), `extract_roadmap_ids(roadmap_text)->frozenset[str]` (l.180) | `contracts.ID_PATTERNS` |

### Area C — opus-architect / spec-fidelity perf (deep dive: R4)

| Path | LOC | 1-line purpose | Key exports (sig) | Intra imports |
|---|---|---|---|---|
| `roadmap/models.py` | 155 | Core roadmap dataclasses/config | `class Finding` (l.22), `class AgentSpec` (l.64), `class RoadmapConfig(PipelineConfig)` (l.94), `class ValidateConfig(PipelineConfig)` (l.141) | `pipeline.models.PipelineConfig` |
| `roadmap/commands.py` | 513 | Click CLI surface for `roadmap` group (run/validate/accept-spec-change) | `roadmap_group()` (l.15), `run(...)` (l.256), `accept_spec_change(output_dir)` (l.406), `validate(...)` (l.463) | **none** at module top (lazy imports inside funcs) |
| `roadmap/prompts.py` | 2204 | All per-step LLM prompt builders + tool definitions | `roadmap_convergence_thresholds()->tuple[float,float]`, `build_extract_prompt(...)`, `build_generate_prompt(...)`, `build_spec_fidelity_prompt(...)` (l.1806), `build_wiring_verification_prompt(...)` (l.2002), `wrap_for_incremental_write(...)`, many `*_tool_definition()->ToolDefinition` | `cli.vocabulary.build_prompt_constraint_block`, `contracts.CONVERGENCE_THRESHOLDS`, `.models.AgentSpec`, `.tool_writer.{TEMPLATES_DIR,ToolDefinition,load_schema}` |
| `roadmap/fidelity_checker.py` | 426 | Programmatic spec-fidelity FR-mapping checker | `class FRMapping` (l.130), `class FidelityResult` (l.139), `class FidelityChecker` (l.150), `run_fidelity_check(...)` (l.410) | `contracts.ID_PATTERNS`, `.convergence.compute_stable_id`, `.models.Finding`, `.spec_parser.*` |
| `roadmap/convergence.py` | 778 | Convergence-aware fidelity loop + deviation registry + regression detection | `reimburse_for_progress(...)`, `compute_stable_id(...)` (l.63), `class RunMetadata`, `class DeviationRegistry` (l.91), `class ConvergenceResult` (l.321), `class RegressionResult`, `execute_fidelity_with_convergence(...)` (l.434), `handle_regression(...)` (l.671) | `.models.Finding` |
| `roadmap/semantic_layer.py` | 692 | LLM semantic-scoring layer (rubric, judge verdict, debate wiring) | `class RubricScores` (l.51), `class SemanticCheckRequest`, `build_semantic_prompt(request)->str` (l.182), `score_argument(...)`, `judge_verdict(...)`, `wire_debate_verdict(...)`, `class SemanticLayerResult`, `run_semantic_layer(...)` (l.413), `validate_semantic_high(...)` | `.models.Finding` |

### Area D/E — dual-write / spec_id_registry (deep dive: R5)

| Path | LOC | 1-line purpose | Key exports (sig) | Intra imports |
|---|---|---|---|---|
| `roadmap/models.py` | 155 | (see Area C) | (see Area C) | (see Area C) |
| `roadmap/remediate_parser.py` | 391 | Parse validation/individual reports into `Finding` objects | `parse_validation_report(text)->list[Finding]` (l.18), `parse_individual_reports(report_texts)->list[Finding]` (l.50); internal `_extract_finding_blocks`, `_deduplicate_findings`, `_merge_findings` | `.models.Finding` |
| `roadmap/remediate.py` | 433 | Remediation tasklist generation + finding filtering + deviation→finding | `class RemediationScope(enum.Enum)` (l.45), `format_validation_summary(...)`, `should_skip_prompt(...)`, `filter_findings(...)` (l.124), `generate_remediation_tasklist(...)` (l.177), `generate_stub_tasklist(...)`, `deviations_to_findings(...)` (l.361) | `.models.Finding` |
| `roadmap/id_registry.py` | 194 | (see Area B) | (see Area B) | (see Area B) |
| `spec_id_registry.json` | n/a (runtime artifact) | Per-run sidecar of accepted spec IDs (FR/NFR/SC/G/D/MD); NOT committed | written by `roadmap/executor.py` `_persist_spec_id_registry` path (sidecar = `output_dir/"spec_id_registry.json"`, l.650, log l.666; resume re-point l.3505-3515); consumed by `roadmap/gates.py` Contract #9 check (l.975-1047, `set_id_registry_sidecar_path`) and `roadmap/envelope.py` `spec_ids` absorption (l.146-166) | — only on-disk samples live under `.dev/tasks/.../acceptance-e2e/*/spec_id_registry.json` (test fixtures) |

Note (Area D/E for R5): the `spec_id_registry.json` SoT is `executor.py` (single writer). `envelope.py:25-28,146-166` documents R0.1→R1.x absorption of the sidecar into `PipelineEnvelope.spec_ids`, with a planned "R1.6 — delete `spec_id_registry.json` writes once [envelope is SoT]" (envelope.py:166). This is the likely dual-write surface for Area D/E — flagged for R5 deep dive, not resolved here.

---

## Summary

- **Area A collection error is real and is the sole suite-blocking collection error**
  (`7909 collected / 1 error`). Root cause: `tests/integration/test_wiring_pipeline.py:28`
  imports `WIRING_GATE` from `roadmap.gates`, where it no longer exists (relocated to
  `audit/wiring_gate.py:1024`; the whole `wiring-verification` step was REPLACED by
  `verify-implementation` in R1.5).
- The test file is **not referenced by anything else** (no conftest/config/import).
- 9 of its 10 tests assert a **removed architecture** (static `wiring-verification` step,
  `len(results)==13`, `"wiring-verification" in ALL_GATES`) and are correctly obsolete; their
  still-valid behavioral concerns (gate_passed on WIRING_GATE, step ordering, resume) are
  **already re-homed** in `tests/audit/test_wiring_gate.py`, `tests/roadmap/test_eval_gate_rejection.py`,
  `tests/roadmap/test_eval_gate_ordering.py`, and the resume test suite.
- **One** assertion (`TestNFR007Compliance.test_no_pipeline_imports_in_wiring_gate`, AST guard
  that `audit/wiring_gate.py` imports nothing from `pipeline/*` except `pipeline.models`) has
  **no exact equivalent** elsewhere. The invariant currently holds (wiring_gate.py:1022 imports
  only `pipeline.models`). Severity LOW.
- `WIRING_GATE` and `check_wiring_report` (the brief's "run_all_semantic_checks wrapper") have
  **no live `src/` consumers** but robust **test** coverage that survives the deletion; the
  `wiring_gate` MODULE remains live (consumed by `sprint/kpi.py`, `sprint/executor.py`). Symbol
  must STAY in `audit/wiring_gate.py`.
- Inventory of all 14 files across Areas A-E captured above (paths, LOC, exports, intra imports);
  `spec_id_registry.json` writer SoT = `roadmap/executor.py`, flagged dual-write absorption for R5.

## Area A deletion safety verdict

**SAFE TO DELETE with ONE small re-homing precondition.**

- Deleting `tests/integration/test_wiring_pipeline.py` is safe: no external references, the
  symbol it needs is gone by design, 9/10 tests are obsolete, and the still-valid behaviors are
  re-homed.
- **Precondition (LOW severity, recommended in the same task item):** before/alongside deletion,
  re-home the single unique assertion `test_no_pipeline_imports_in_wiring_gate` (the
  `audit/wiring_gate.py` ↛ `pipeline/*`-except-models AST guard) into
  `tests/audit/test_wiring_gate.py` (~20-line `TestNFR007Compliance` class). This preserves the
  architectural-boundary invariant that has no other home.
- If the team accepts losing that one AST guard, deletion is **unconditionally SAFE** (it only
  drops a static import-boundary check, not behavioral coverage). Recommended path: re-home it —
  it is cheap and the invariant is worth keeping.
