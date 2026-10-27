# D-0012 — `## Result File` Section Added to `build_prompt()`

## Task: T04.01

## Change Summary

Appended a `## Result File` section as the last `##`-level section in `build_prompt()` in
`src/superclaude/cli/sprint/process.py`, after `## Important`.

## Diff

**File:** `src/superclaude/cli/sprint/process.py`

**Before** (final lines of return statement):
```python
            f"## Important\n"
            f"- This is Phase {pn} of a multi-phase sprint\n"
            f"- Previous phases have already been executed in separate sessions\n"
            f"- Do not re-execute work from prior phases\n"
            f"- Focus only on the tasks defined in the phase file"
        )
```

**After:**
```python
            f"## Important\n"
            f"- This is Phase {pn} of a multi-phase sprint\n"
            f"- Previous phases have already been executed in separate sessions\n"
            f"- Do not re-execute work from prior phases\n"
            f"- Focus only on the tasks defined in the phase file\n"
            f"\n"
            f"## Result File\n"
            f"- When all tasks in this phase are complete, write the result file to:\n"
            f"  `{config.result_file(self.phase).as_posix()}`\n"
            f"- The file content must be exactly: `EXIT_RECOMMENDATION: CONTINUE`\n"
            f"- Write this file as the final action of this phase\n"
            f"- If a STRICT-tier task fails and you are halting, write instead:\n"
            f"  `EXIT_RECOMMENDATION: HALT`"
        )
```

## Acceptance Criteria Verification

| Criterion | Status |
|---|---|
| `## Result File` is last `##`-level section (after `## Important`) | PASS |
| Path uses `config.result_file(self.phase).as_posix()` | PASS |
| CONTINUE content instruction present | PASS |
| Conditional HALT instruction for STRICT-tier failures present | PASS |
| Existing prompt sections not repositioned | PASS |
| OQ-001: attribute name is `self.phase` (not `self._phase`) | CONFIRMED (D-0002) |

## Notes

- `config.result_file(phase)` is defined in `src/superclaude/cli/sprint/models.py:341`
- Path embedded at prompt build time — varies per phase/config as intended
- `as_posix()` used per FR-006 requirement
