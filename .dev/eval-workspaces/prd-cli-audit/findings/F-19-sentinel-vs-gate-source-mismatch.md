# F-19: Sentinel detection and gate evaluation read different sources -- can disagree

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P6
**Identified by**: A-17
**File:line**: `src/superclaude/cli/prd/executor.py:518-532`

## Evidence

```python
output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""
gate_content = _resolve_step_content(step_id, self._config.task_dir, output_text)
status = self._determine_status(exit_code, output_text, step_id)  # uses NDJSON text
...
gate_passed = self._evaluate_gate(step_id, gate, gate_content)    # uses disk file
```

## Trace

- For step_ids with a `_STEP_ARTIFACT_FILES` entry where the on-disk file exists, `gate_content` is the disk file (e.g. 400+ line research-notes.md) but `status` derivation reads the NDJSON commentary.
- The subprocess may emit `^EXIT_RECOMMENDATION: HALT` in its narration even though the disk artifact passes the gate, or vice versa.
- The two read different sources and reach independent verdicts. Specifically, sentinel detection on NDJSON commentary that is 30 lines long, and gate evaluation on a 400-line disk file, can produce "HALT sentinel + gate PASS" -- `_determine_status` returns HALT, and the gate code never runs because `status.is_success` is False at line 531.

## Reproduction sketch

Subprocess emits a hortative HALT sentinel in narration that does not reflect artifact quality. Pipeline halts despite a satisfactory artifact on disk.

## Confidence (aggregated)

0.80 -- Agent A verified the source mismatch is direct. Whether it surfaces in practice depends on subprocess prompt behavior.

## Cross-agent corroboration

- **Agent A** identified the dual-source evaluation: `_determine_status` reads NDJSON-extracted text while `_evaluate_gate` reads the resolved disk artifact, and a disagreement produces an irreversible halt.
