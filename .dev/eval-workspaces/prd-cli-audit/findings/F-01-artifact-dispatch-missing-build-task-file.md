# F-01: `_STEP_ARTIFACT_FILES` missing `build-task-file` -- proximate halt cause

**Final severity (Stage 2 preliminary)**: CRITICAL
**Pattern tags**: P1, P3, P4, P6
**Identified by**: A-1, B-11, E-1 (partial), F-1, F-2, F-3, F-10
**File:line**: `src/superclaude/cli/prd/executor.py:246-269`

## Evidence

```python
# executor.py:246-251 -- the dispatch table
_STEP_ARTIFACT_FILES: dict[str, str] = {
    "parse-request": "parsed-request.json",
    "scope-discovery": "scope-discovery-raw.md",
    "research-notes": "research-notes.md",
    "sufficiency-review": "sufficiency-review.md",
}

# executor.py:267-269 -- the consumer that falls through
artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
if not artifact_name:
    return ndjson_text          # silent fallback to subprocess stream
```

## Trace

- **Writer**: Maintainer added `build-task-file` to `_STAGE_A_STEPS` (executor.py:301-316) but never added a corresponding entry to `_STEP_ARTIFACT_FILES`.
- **Reader chain**: `_resolve_step_content` (executor.py:254-293) is called by `_run_subprocess_step` (executor.py:522) which feeds `_evaluate_gate` (executor.py:587). For `build-task-file`, the dict lookup returns `None`, so `gate_content = ndjson_text` -- the extracted assistant commentary from the NDJSON stream (~30 lines).
- **Gate**: `GATE_CRITERIA["build-task-file"]` has `min_lines=400` and `enforcement_tier="STRICT"`. Gate fails with "Min lines: 30/400".
- **Persistence**: `_persist_step_artifact` (executor.py:976-1004) also short-circuits at 988-989 for missing artifact_name, so the canonical `TASK-PRD-{slug}.md` is never copied to `task_dir`.

## Reproduction sketch

`superclaude prd run "Build a user auth system" --product test-auth --tier standard` -- pipeline reaches step 7, `_resolve_step_content("build-task-file", ...)` returns NDJSON commentary, STRICT gate fails with "Min lines: 30/400", pipeline halts. This is the exact reported failure mode.

## Confidence (aggregated)

0.99 -- The dict membership is mechanically verifiable. Agent A confirmed the code path end-to-end. Agent B confirmed the gate reads the wrong source. Agent E confirmed the prompt instructs Write to disk. Agent F confirmed no test catches this.

## Cross-agent corroboration

- **Agent A** traced the full executor chain from dispatch miss to gate halt and identified this as the proximate cause.
- **Agent B** cross-referenced the symptom: `_resolve_step_content` falls through to NDJSON, confirming the "30 lines of NDJSON commentary" read as task file.
- **Agent E** confirmed the prompt at prompts.py:381 explicitly instructs the subprocess to Write to `TASK-PRD-{slug}.md` on disk, making the dispatch miss load-bearing.
- **Agent F** verified that zero tests exercise `_resolve_step_content` for this step ID and the mock harness defeats the real chain by writing passing content into the stream file.
