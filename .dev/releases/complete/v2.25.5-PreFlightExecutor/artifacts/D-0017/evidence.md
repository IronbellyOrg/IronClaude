# Evidence: D-0017 — Evidence Artifact Writing

## Task
T03.02 — Implement Evidence Artifact Writing

## Function Signature

```python
def _write_evidence(
    task_id: str,
    command: str,
    exit_code: int,
    stdout: str,
    stderr: str,
    duration: float,
    classification: str,
    artifacts_dir: Path,
) -> None
```

## Location
`src/superclaude/cli/sprint/preflight.py`

## Output Path
`artifacts_dir / task_id / "evidence.md"`

## Directory Creation
`Path.mkdir(parents=True, exist_ok=True)` — no errors on pre-existing dirs

## Evidence File Format
```markdown
# Evidence: <task_id>

## Command

```
<command>
```

## Result

- **Exit code:** <exit_code>
- **Duration:** <duration>s
- **Classification:** <classification>

## stdout

```
<stdout_truncated>
```

## stderr

```
<stderr_truncated>
```
```

## Truncation Behavior

- stdout: truncated at 10240 bytes with `\n[truncated at 10240 bytes]` marker appended
- stderr: truncated at 2048 bytes with `\n[truncated at 2048 bytes]` marker appended
- Implemented in `_truncate(text, limit)` — encodes to UTF-8, slices bytes, decodes with errors="replace"

## Verification

Test command: `uv run pytest tests/sprint/test_preflight.py -v -k "evidence"` — 4 passed

- `test_evidence_structure`: verifies all 6 fields (command, exit_code, stdout, stderr, duration, classification) present
- `test_stdout_truncation_10kb`: 15KB input → 10KB with marker
- `test_stderr_truncation_2kb`: 5KB input → 2KB with marker
- `test_no_truncation_when_under_limit`: text under limit unchanged
- `test_truncation_exact_limit`: exact-limit text not truncated
