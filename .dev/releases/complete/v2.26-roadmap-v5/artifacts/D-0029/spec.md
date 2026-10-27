# D-0029: _check_annotate_deviations_freshness() Implementation

## Summary

Implemented `_check_annotate_deviations_freshness()` in `src/superclaude/cli/roadmap/executor.py`.

## Function Signature

```python
def _check_annotate_deviations_freshness(
    output_dir: Path,
    roadmap_file: Path,
    gate_pass_state: dict[str, bool] | None = None,
) -> bool:
```

## Behavior

- Reads `spec-deviations.md` frontmatter, extracts `roadmap_hash`
- Compares against `hashlib.sha256(roadmap_content).hexdigest()`
- **Fail-closed**: returns False for missing file, missing field, read error, empty file, corrupt frontmatter, missing roadmap.md, or empty/None hash
- On mismatch: logs specific reason, resets `spec-fidelity` and `deviation-analysis` from gate_pass_state (FR-084)
- Integrated into `_apply_resume()` before skipping `annotate-deviations` (FR-071)

## Failure Reasons Logged

Each failure case logs a specific reason:
1. spec-deviations.md not found
2. Read error (OSError)
3. Empty file
4. Corrupt/missing frontmatter
5. roadmap_hash field missing or empty
6. roadmap.md not found
7. roadmap.md read error
8. Hash mismatch (saved vs current)

## Test Results

`uv run pytest tests/sprint/test_executor.py -v -k "freshness"` — **11 passed** (9 SC-8 cases + 2 gate-state tests)

All 9 SC-8 test cases:
- [PASS] matching hash → True
- [PASS] mismatched hash → False
- [PASS] missing file → False
- [PASS] missing field → False
- [PASS] read error → False
- [PASS] empty file → False
- [PASS] corrupt frontmatter → False
- [PASS] missing roadmap.md → False
- [PASS] empty/None hash field → False
