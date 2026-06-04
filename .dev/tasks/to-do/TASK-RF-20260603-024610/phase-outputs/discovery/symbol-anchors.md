# Symbol Anchors — Drift-Proof Discovery (Step 1.3)

Generated at task start (2026-06-03) by grepping the live source vs the research-cited lines in
`research/01-file-inventory.md` and `research/03-wiring-seams.md`.

**Method note (tooling deviation):** the standalone `Grep`/`Glob` tools are unavailable in this
runtime; `bash grep -n` was used as the fallback for line-anchoring. Logged in Deviations from Process.

**Headline:** drift is 0..+1 lines across all symbols — the research citations are accurate. Later
wiring items should still re-confirm each edit point by symbol name, not the bare line.

| File | Symbol | Current Line | Research-Cited Line | Drift |
|------|--------|--------------|---------------------|-------|
| executor.py | `class IsolationLayers` | 108 | 107 | +1 |
| executor.py | `def setup_isolation` | 151 | 151 | 0 |
| executor.py | `class AggregatedPhaseReport` | 192 | 191 | +1 |
| executor.py | `def aggregate_task_results` | 297 | 297 | 0 |
| executor.py | `def execute_phase_tasks` | 928 | 928 | 0 |
| executor.py | `results.append(result)` (per-task append) | 1066 | 1066 | 0 |
| executor.py | `def _run_task_subprocess` | 1079 | 1079 | 0 |
| executor.py | `# Turn counting ... T02.06` comment | 1117 | 1117 | 0 |
| executor.py | `def _parse_phase_tasks` | 1121 | 1121 | 0 |
| executor.py | `def execute_sprint` | 1138 | 1138 | 0 |
| executor.py | `_phase_env_vars = {` (Path A fallback) | 1327 | 1327 | 0 |
| executor.py | `_stall_acted` watchdog block | 1344 | 1344 | 0 |
| executor.py | `startup_stall_timeout` watchdog | 1374 | ~1344-1444 | in-range |
| executor.py | `def _write_preliminary_result` | 1987 | 1987 | 0 |
| process.py | `class ClaudeProcess` | 88 | 88 | 0 |
| process.py | `def build_prompt` | 123 | 123 | 0 |
| process.py | `def build_task_context` | 257 | 257 | 0 |
| logging_.py | `def write_task_rerun_complete` | 205 | 205 | 0 |
| logging_.py | `def write_summary` | 245 | 245 | 0 |
| logging_.py | `def _jsonl` | 265 | 265 | 0 |
| models.py | `class TaskEntry` | 31 | 30 | +1 |
| models.py | `class TaskStatus(Enum)` | 45 | 45 | 0 |
| models.py | `class GateOutcome(Enum)` | 63 | 63 | 0 |
| models.py | `class TaskResult` | 166 | 165 | +1 |
| models.py | `TaskResult.to_dict` | 184 | 184 | 0 |
| models.py | `TaskResult.from_dict` | 213 | 212 | +1 |
| models.py | `class SprintConfig` | 407 | 406 | +1 |
| models.py | `SprintConfig.task_output_file` | 561 | 561 | 0 |
| models.py | `SprintResult.resume_command` | 677 | 677 | 0 |
| models.py | `class TurnLedger` | 758 | 757 | +1 |
| models.py | `def build_resume_output` | 844 | 844 | 0 |
| config.py | `_TASK_HEADING_RE` | 380 | 380 | 0 |
| config.py | `def parse_tasklist` | 405 | 405 | 0 |
| config.py | `def load_sprint_config` | 281 | (call @commands.py:230) | n/a |
| checkpoints.py | `def write_manifest` (atomic idiom) | 173 | 173 | 0 |
| rerun_tasks.py | `def walk_dependencies` | 368 | 368 | 0 |
| rerun_tasks.py | `def _dependencies_of` (nested) | 438 | 438 | 0 |
| rerun_tasks.py | `def _is_satisfied` (nested) | 453 | 453 | 0 |
| commands.py | `def run(` (sprint run command) | 190 | 72 (first decorator) | decorators span 73-189 |

**NOT FOUND:** none. `def build_env` is NOT defined in `process.py` (it is inherited from the pipeline
base `_PipelineClaudeProcess`); research 03 §1 references its merge behavior but it lives upstream — no
edit needed there per the seams analysis.
