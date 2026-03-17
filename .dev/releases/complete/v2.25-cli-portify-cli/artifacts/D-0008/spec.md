# D-0008: Workflow Path Resolution — Implementation Spec

**Task:** T02.01 | **Roadmap Item:** R-008 | **Status:** COMPLETE

## Implementation

`resolve_workflow_path(name_or_path, skills_root=None)` in `src/superclaude/cli/cli_portify/config.py:183`

### Rules Implemented
1. Direct path to directory with SKILL.md → return it
2. Direct path to SKILL.md file → return parent
3. With skills_root: partial-name search → exact or AMBIGUOUS_PATH/INVALID_PATH
4. No match → raise InvalidPathError (INVALID_PATH)

### Error Codes
- `AMBIGUOUS_PATH` — AmbiguousPathError with candidates list
- `INVALID_PATH` — InvalidPathError when no SKILL.md found

## Verification
`uv run pytest tests/cli_portify/test_config.py -v` → 30 passed
