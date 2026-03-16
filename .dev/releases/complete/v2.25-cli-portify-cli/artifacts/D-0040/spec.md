# D-0040: prompts-executor-design Prompt Builder and Step

## Status: COMPLETE

## Deliverable

- `prompts.py`: `build_prompts_executor_design_prompt(config_cli_name, step_graph_content, models_gates_content) -> str`
- `executor.py`: `execute_prompts_executor_design_step(config_cli_name, workdir, process_runner) -> PortifyStepResult`
- `gates.py`: `gate_prompts_executor_design()` (G-007, STRICT), `PROMPTS_EXECUTOR_DESIGN_GATE`
- `STEP_REGISTRY["prompts-executor-design"]` with `timeout_s=600`, `retry_limit=1`

## Acceptance Criteria

- [x] `uv run pytest tests/cli_portify/ -k "prompts_executor"` exits 0
- [x] Output written to `prompts-executor-spec.md` in workdir
- [x] G-007 (EXIT_RECOMMENDATION marker) applied and enforced
- [x] 600s timeout set

## Test Results

All prompts_executor tests passing. G-007 EXIT_RECOMMENDATION enforcement verified.
