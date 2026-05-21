# F-34: Static dispatch tables for step IDs -- `_PHASE_ALLOWED_REFS` and `_STEP_ID_PATTERN`

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P1, P3
**Identified by**: D-11, C-10
**File:line**: `src/superclaude/cli/prd/process.py:95-113`; `src/superclaude/cli/prd/config.py:26-33`

## Evidence

```python
# process.py:95-113 -- file args per step, static keys
_PHASE_ALLOWED_REFS: dict[str, list[str]] = {
    "parse-request": [],
    "scope-discovery": [],
    ...
}
# process.py:175 -- lookup, no error on miss
allowed = _PHASE_ALLOWED_REFS.get(base_step, [])

# config.py:26-33 -- step ID validation regex
_STEP_ID_PATTERN = re.compile(
    r"^(check-existing|parse-request|scope-discovery|research-notes"
    r"|sufficiency-review|template-triage|build-task-file|verify-task-file"
    r"|preparation|investigation-\d+|web-research-\d+"
    r"|analyst-completeness|qa-research-gate"
    r"|synthesis-\d+|analyst-synthesis|qa-synthesis-gate"
    r"|assembly|structural-qa|qualitative-qa|completion)$"
)
```

## Trace

Both tables must be maintained in sync with `_STAGE_A_STEPS`, `_build_*_steps` generators, and `GATE_CRITERIA`. Adding a new step requires editing all of them independently.

- `_PHASE_ALLOWED_REFS`: missing step IDs get `[]` (zero --file args). Subprocess runs without refs and produces degraded output.
- `_STEP_ID_PATTERN`: `superclaude prd resume <new-step>` fails with "Unrecognised resume step ID" until someone edits the regex.

Three independent source-of-truth lists for step IDs with nothing enforcing synchrony.

## Reproduction sketch

Add a new step `taxonomy-review` to `_STAGE_A_STEPS` and ship it. `superclaude prd resume taxonomy-review` fails until someone remembers to edit the regex. The subprocess runs without `--file` args.

## Confidence (aggregated)

0.90 -- Both agents independently identified the static-dispatch-table pattern. Mechanically verifiable.

## Cross-agent corroboration

- **Agent D** identified `_PHASE_ALLOWED_REFS` silent-empty-on-miss behavior.
- **Agent C** identified `_STEP_ID_PATTERN` hand-maintained regex and the three independent source-of-truth problem.
