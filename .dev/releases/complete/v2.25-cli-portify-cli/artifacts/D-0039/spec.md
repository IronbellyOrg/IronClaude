# D-0039: models-gates-design Prompt Builder and Step

## Status: COMPLETE

## Deliverable

- `prompts.py`: `build_models_gates_design_prompt(config_cli_name, step_graph_content) -> str`
- `executor.py`: `execute_models_gates_design_step(config_cli_name, workdir, process_runner) -> PortifyStepResult`
- `gates.py`: `gate_models_gates_design()` (G-006, STANDARD), `MODELS_GATES_DESIGN_GATE`
- `STEP_REGISTRY["models-gates-design"]` with `timeout_s=600`, `retry_limit=1`

## Acceptance Criteria

- [x] `uv run pytest tests/cli_portify/ -k "models_gates"` exits 0
- [x] `build_models_gates_design_prompt()` references step graph content
- [x] G-006 (return type pattern check) applied on output
- [x] 600s timeout set in STEP_REGISTRY for this step

## Test Results

All models_gates tests passing. G-006 return type pattern enforcement verified.
