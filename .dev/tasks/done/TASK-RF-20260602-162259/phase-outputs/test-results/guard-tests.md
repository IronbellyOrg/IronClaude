# Guard + Regression Tests & MD Acceptance (Step 5.7)

**Captured:** 2026-06-02 18:02
**Verdict: PASS**

## Guard + regression pytest

Command: `uv run pytest tests/roadmap/ -k "schema_id_pattern or matches_generate_id_pattern or accept_md_family" -q`

Result line: **`9 passed, 1 skipped, 1960 deselected in 0.52s`**

The 9 selected: 4 rebuilt guard tests (`test_{extract,extract_tdd,generate,merge}_schema_id_pattern_matches_contracts`, now keys-driven exact-arm), the merge≡generate pin (now also pinning the assembler output), and the 4 parametrized `test_all_schemas_accept_md_family[...]` cases. All green. (The `1 skipped` is the pre-existing unrelated skip.)

## Positive validate_tool_output(M1-D01) acceptance

A minimal `{'roadmap_ids': ['FR-1','M1-D01']}` object run through `validate_tool_output` against each on-disk schema returns only the expected *other* required-field errors (frontmatter / functional_requirements / milestones) and **zero `roadmap_ids` pattern errors**:

```
extract roadmap_ids pattern errors: [] -> PASS
extract_tdd roadmap_ids pattern errors: [] -> PASS
generate roadmap_ids pattern errors: [] -> PASS
merge roadmap_ids pattern errors: [] -> PASS
ALL_NO_ROADMAP_IDS_ERROR True
```

This proves the `roadmap_ids` pattern element is no longer the source of any validation error for `M1-D01` against any of the four schemas — the bug is closed at the runtime-validator level. (Full literal output incl. the unrelated required-field errors is in `md-acceptance.txt`.)
