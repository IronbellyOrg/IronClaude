# F-04: Systemic inversion -- all Write-emitting steps missing from `_STEP_ARTIFACT_FILES`

**Final severity (Stage 2 preliminary)**: CRITICAL
**Pattern tags**: P1, P3, P4, P5, P6
**Identified by**: E-1, E-4, E-5, E-6, E-14, D-1, A-12
**File:line**: `src/superclaude/cli/prd/executor.py:246-251` (table); `src/superclaude/cli/prd/prompts.py:381, 518, 590, 647, 716, 765, 812, 857, 919, 989, 1043` (Write instructions)

## Evidence

```python
# executor.py:246-251 -- the 4-entry table
_STEP_ARTIFACT_FILES: dict[str, str] = {
    "parse-request": "parsed-request.json",      # prompt: stdout only
    "scope-discovery": "scope-discovery-raw.md",  # prompt: stdout only
    "research-notes": "research-notes.md",        # prompt: stdout only
    "sufficiency-review": "sufficiency-review.md", # prompt: stdout only
}
# These 4 steps do NOT instruct the subprocess to Write to disk.
# All 13 steps that DO instruct Write are MISSING.

# prompts.py:381 (build-task-file)
Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}
# prompts.py:518 (investigation)
Research this aspect of the product and write findings to {output_path}
# prompts.py:590 (web-research)
Research this topic externally and write findings to {output_path}.
# prompts.py:765 (synthesis) + incremental write protocol
Output path: {output_path}
# prompts.py:919 (assembly) + incremental write protocol
Output path: {config.output_path}
# prompts.py:647, 716, 812, 857, 989, 1043 (QA steps)
Output path: {config.qa_dir / "<specific-filename>.md"}
```

## Trace

- **Writer**: 13 out of 19 prompt builders instruct the subprocess to Write to a file path. 0 out of those 13 are present in `_STEP_ARTIFACT_FILES`.
- **The 4 entries that exist** correspond to the steps where the prompt does NOT instruct a Write -- they rely on NDJSON stdout capture and `_persist_step_artifact` writes the captured text.
- **The dispatch table is inverted**: it lists exactly the steps where the subprocess does *not* write to disk, and is missing exactly the steps where it does.
- **Blast radius by step**:
  - `build-task-file`: min_lines=400, STRICT. **Halts the pipeline** (the reported failure).
  - `investigation-{N}`: min_lines=50. NDJSON commentary often exceeds 50 lines, so gate passes by accident.
  - `web-research-{N}`: min_lines=30. Same lucky pass.
  - `synthesis-{N}`: min_lines=80. Commentary may exceed 80 lines in long runs.
  - `assembly`: min_lines=800, STRICT. **Will halt** if reached -- 800-line NDJSON commentary is unlikely.
  - QA steps: min_lines=20, plus verdict check that may spuriously pass from instruction text.
- **Persistence**: `_persist_step_artifact` (executor.py:987-989) silently returns for missing artifact names, so downstream prompt builders that load by canonical filename find nothing.

## Reproduction sketch

Patch Bug 1 (F-01) to add `build-task-file` only. Run past step 7 to step 14a (assembly). The pipeline halts again with the same shape: gate reads NDJSON commentary, real PRD file is on disk at `config.output_path`. The fix must address the entire dispatch table, not just one entry.

## Confidence (aggregated)

0.97 -- Agent E verified by inspection that every Write-instructing prompt is absent from the table and every present key has no Write instruction. Agent D confirmed the subprocess plumbing always uses `stream-json` with no `tool_write_mode` override. Agent A confirmed the persistence guard also silently skips unmapped steps.

## Cross-agent corroboration

- **Agent E** produced the master table mapping all 19 steps to their Write behavior and quantified the inversion: 13 Write-instructing steps have zero dispatch entries. This transforms Bug 1 from a one-off omission into a systemic architectural defect.
- **Agent D** confirmed that `process.py` hard-codes `output_format="stream-json"` and never passes `tool_write_mode`, meaning every Write-tool artifact is invisible to the gate evaluation path.
- **Agent A** identified the persistence consequence: `_persist_step_artifact` silently returns for all unmapped steps, so canonical artifact files are never written to `task_dir`.
