# D-0045: 4-Substep Release Spec Synthesis 3a–3d (T07.02)

## Status: COMPLETE

## Implementation

### Substep 3a: Working copy confirmation
- `execute_release_spec_synthesis_step()` calls `load_release_spec_template()` + `create_working_copy()`

### Substep 3b: Section population
- `build_section_population_prompt(working_copy, portify_spec, analysis_report)` in `prompts.py`
- Writes `workdir/release-spec-draft.md`

### Substep 3c: 3-persona brainstorm
- `build_brainstorm_prompt(draft_content, persona)` for architect, analyzer, backend
- Parses newline-delimited JSON findings from stdout into `BrainstormFinding` objects

### Substep 3d: Finding incorporation
- `incorporate_findings(draft, findings)` in `prompts.py`
- CRITICAL/MAJOR with `affected_section` → body comments
- Unresolvable (no section) or INFO → Section 12 table

### BrainstormFinding dataclass
- Located in `src/superclaude/cli/cli_portify/models.py`
- Fields: `gap_id`, `description`, `severity`, `affected_section`, `persona`

## Verification

```
uv run pytest tests/cli_portify/test_phase7_release_spec.py -k "brainstorm or finding_incorporation or synthesis" -v
```

Result: **All PASSED**

## Acceptance Criteria

- [x] 3 persona Claude calls produce distinct findings with required structure
- [x] CRITICAL findings incorporated into body
- [x] Unresolvable findings routed to Section 12
- [x] `BrainstormFinding` dataclass importable from `superclaude.cli.cli_portify.models`
