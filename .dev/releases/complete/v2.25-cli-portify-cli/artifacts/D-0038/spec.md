# D-0038: step-graph-design Prompt Builder and Step

## Status: COMPLETE

## Deliverable

- `prompts.py`: `build_step_graph_design_prompt(config_cli_name, analysis_report_content) -> str`
- `executor.py`: `execute_step_graph_design_step(config_cli_name, workdir, process_runner) -> PortifyStepResult`
- `gates.py`: `gate_step_graph_design()` (G-005, STRICT), `STEP_GRAPH_DESIGN_GATE`
- `STEP_REGISTRY["step-graph-design"]` with `timeout_s=600`, `retry_limit=1`

## Acceptance Criteria

- [x] `uv run pytest tests/cli_portify/ -k "step_graph"` exits 0
- [x] `build_step_graph_design_prompt()` references analysis report content
- [x] Mock execution writes `step-graph-spec.md` with EXIT_RECOMMENDATION marker in workdir
- [x] G-005 gate passes on output with marker; fails on output without marker

## Test Results

All step_graph tests passing. G-005 enforcement verified.
