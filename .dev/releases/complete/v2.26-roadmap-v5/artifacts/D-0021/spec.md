# D-0021: annotate-deviations Step Wiring

## Location
`src/superclaude/cli/roadmap/executor.py` — `_build_steps()`

## Position
Between merge (Step 6) and test-strategy (Step 8). Is Step 7.

## Step Definition
```python
Step(
    id="annotate-deviations",
    prompt=build_annotate_deviations_prompt(
        config.spec_file,
        merge_file,
        debate_file,
        diff_file,
    ),
    output_file=spec_deviations_file,  # spec-deviations.md
    gate=ANNOTATE_DEVIATIONS_GATE,
    timeout_seconds=300,
    inputs=[config.spec_file, merge_file, debate_file, diff_file],
    retry_limit=0,
)
```

## FR-018: spec-deviations.md passed to spec-fidelity
The spec-fidelity step receives `spec_deviations_file` as an additional input:
```python
Step(
    id="spec-fidelity",
    prompt=build_spec_fidelity_prompt(
        config.spec_file, merge_file, spec_deviations_path=spec_deviations_file
    ),
    inputs=[config.spec_file, merge_file, spec_deviations_file],
    ...
)
```
