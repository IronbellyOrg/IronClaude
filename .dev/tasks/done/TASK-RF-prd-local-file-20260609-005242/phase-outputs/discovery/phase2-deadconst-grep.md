# Phase 2.1 — Dead-Constant Grep

`grep -rn` across `src/` and `tests/` for the three constants:

| Constant | All matches | Verdict |
|----------|-------------|---------|
| `_PHASE_ALLOWED_REFS` | process.py:95 (def), :191 (inside `_build_file_args`) | **CONFIRMED-DEAD** — only def + method-internal use |
| `_FILE_SIZE_THRESHOLD` | process.py:115 (def), :198 (inside `_build_file_args`) | **CONFIRMED-DEAD** |
| `_SPEC_FILE_STEPS` | process.py:121 (def), :180 (docstring), :201 (inside `_build_file_args`) | **CONFIRMED-DEAD** |

Zero references outside the former `_build_file_args` method (`:169-206`); zero test references.

**prompts.py literal-name inlining confirmed** (`grep 'skill_refs_dir /'`): refs are inlined by literal filename at prompts.py:514-518 (`build-request-template.md`, `agent-prompts.md`, `synthesis-mapping.md`, `validation-checklists.md`, `operational-guidance.md`) — NOT via `_PHASE_ALLOWED_REFS`. Deleting the map drops no delivery path.

**All three constants safe to delete (Step 2.5).**
