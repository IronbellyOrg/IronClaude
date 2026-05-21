# F-24: `check_existing_work` returns ALREADY_COMPLETE for any `.md` under `results/`

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P7
**Identified by**: E-10
**File:line**: `src/superclaude/cli/prd/inventory.py:55-59`

## Evidence

```python
results_dir = task_dir / "results"
if results_dir.is_dir():
    prd_files = list(results_dir.glob("*.md"))
    if prd_files:
        return ExistingWorkState.ALREADY_COMPLETE
```

## Trace

- Any `.md` file under `task_dir/results/` is treated as proof the PRD pipeline is complete -- including a half-written assembly artifact from a crashed run, an unrelated note file, or a previous-tier output.
- The assembly prompt (prompts.py:919) writes to `config.output_path` incrementally with `status: "Draft"` from the very first edit. If the pipeline crashes mid-assembly, the next run sees a Draft-status file and reports ALREADY_COMPLETE.
- No content check (no frontmatter parse, no `status: Final` requirement, no line count vs tier min).

## Reproduction sketch

Run a pipeline, kill at step 14a after the first Edit. Re-run -- `check_existing_work` returns ALREADY_COMPLETE. User gets "Already complete" with a draft PRD.

## Confidence (aggregated)

0.85 -- Agent E verified the code path.

## Cross-agent corroboration

- **Agent E** identified the content-free check and traced the interaction with the assembly prompt's incremental write behavior, noting that any `.md` file triggers completion detection regardless of actual content or status.
