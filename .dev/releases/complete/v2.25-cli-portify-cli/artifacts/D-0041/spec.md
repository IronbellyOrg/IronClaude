# D-0041: pipeline-spec-assembly Step

## Status: COMPLETE

## Deliverable

- `executor.py`: `assemble_specs_programmatic(step_graph, models_gates, prompts_executor) -> str`
- `executor.py`: `execute_pipeline_spec_assembly_step(config_cli_name, workdir, process_runner) -> PortifyStepResult`
- `prompts.py`: `build_spec_assembly_prompt(assembled_content) -> str`
- `gates.py`: `gate_pipeline_spec_assembly()` (G-008, STRICT), `PIPELINE_SPEC_ASSEMBLY_GATE`
- `STEP_REGISTRY["pipeline-spec-assembly"]` with `timeout_s=600`, `retry_limit=1`

## Acceptance Criteria

- [x] `uv run pytest tests/cli_portify/ -k "spec_assembly"` exits 0
- [x] Programmatic pre-assembly produces deduplicated content before Claude call
- [x] G-008 gate passes on `portify-spec.md` with consistent step_mapping count (SC-005)
- [x] G-008 gate fails when step_mapping count mismatches declared steps

## Test Results

All spec_assembly tests passing. G-008 step-count consistency and EXIT_RECOMMENDATION enforcement verified.
`assemble_specs_programmatic()` correctly deduplicates frontmatter blocks from the 3 input specs.
