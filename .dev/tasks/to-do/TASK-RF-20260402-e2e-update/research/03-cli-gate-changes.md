# Research: CLI & Gate Changes

| Field       | Value                          |
|-------------|--------------------------------|
| Topic Type  | Integration Points + Patterns  |
| Status      | Complete                       |
| Date        | 2026-04-02                     |
| Researcher  | researcher-03                  |
| Scope       | gates.py, commands.py, models.py, executor.py |

---

## 1. EXTRACT_TDD_GATE

**Location:** `src/superclaude/cli/roadmap/gates.py`, lines 797-835

### Full Field List (19 fields)

**13 standard fields (shared with EXTRACT_GATE):**
1. `spec_source`
2. `generated`
3. `generator`
4. `functional_requirements`
5. `nonfunctional_requirements`
6. `total_requirements`
7. `complexity_score`
8. `complexity_class`
9. `domains_detected`
10. `risks_identified`
11. `dependencies_identified`
12. `success_criteria_count`
13. `extraction_mode`

**6 TDD-specific fields:**
14. `data_models_identified`
15. `api_surfaces_identified`
16. `components_identified`
17. `test_artifacts_identified`
18. `migration_items_identified`
19. `operational_items_identified`

### Semantic Checks (2)
- `complexity_class_valid` -- complexity_class must be one of LOW, MEDIUM, HIGH
- `extraction_mode_valid` -- extraction_mode must be 'standard' or start with 'chunked'

These are identical to EXTRACT_GATE's semantic checks.

### Other Gate Properties
- `min_lines=50` (same as EXTRACT_GATE)
- `enforcement_tier="STRICT"` (same as EXTRACT_GATE)

### When Used vs EXTRACT_GATE

**File:** `src/superclaude/cli/roadmap/executor.py`, line 1356:
```python
gate=EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE,
```

The conditional is in `_build_steps()` (line 1299). The same conditional also selects between `build_extract_prompt_tdd()` and `build_extract_prompt()` at lines 1341-1353.

### E2E Impact

Any E2E item that checks extraction frontmatter fields after a TDD pipeline run must account for 19 fields (not 13). Specifically:
- Phase 4 items checking extraction.md frontmatter must verify all 6 TDD-specific fields are present
- Phase 4 items checking for specific field names should reference `data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`

**Note:** EXTRACT_TDD_GATE is NOT in the `ALL_GATES` list (line 1124-1139). Only `EXTRACT_GATE` appears there. This means any E2E check that iterates ALL_GATES will not encounter the TDD variant -- it is only applied dynamically in `_build_steps()`.

---

## 2. Other New/Changed Gates

### DEVIATION_ANALYSIS_GATE

**Location:** `src/superclaude/cli/roadmap/gates.py`, lines 1070-1121

**Status:** This gate EXISTS in the current codebase. It appears in:
- `ALL_GATES` list at line 1136: `("deviation-analysis", DEVIATION_ANALYSIS_GATE)`
- Executor import at line 32
- Used in `_build_steps()` at line 1472: `gate=DEVIATION_ANALYSIS_GATE`

**Required frontmatter fields (9):**
1. `schema_version`
2. `total_analyzed`
3. `slip_count`
4. `intentional_count`
5. `pre_approved_count`
6. `ambiguous_count`
7. `routing_fix_roadmap`
8. `routing_no_action`
9. `analysis_complete`

**Semantic checks (7):**
- `no_ambiguous_deviations` -- ambiguous_deviations must be 0
- `validation_complete_true` -- analysis_complete must be true
- `routing_ids_valid` -- All routing IDs must match DEV-\d+ pattern
- `slip_count_matches_routing` -- slip_count must equal number of IDs in routing_fix_roadmap
- `pre_approved_not_in_fix_roadmap` -- Pre-approved IDs must not appear in routing_fix_roadmap
- `total_analyzed_consistent` -- total_analyzed must equal sum of counts
- `deviation_counts_reconciled` -- total_analyzed must equal count of unique routed IDs (SC-008)

**TDD Compatibility:** The file header comment at lines 15-16 explicitly states: "DEVIATION_ANALYSIS_GATE: NOT TDD-compatible -- deferred to separate work." The CLI commands.py also warns about this at lines 239-248 when `resolved_type == "tdd"`.

### REMEDIATE_GATE

**Location:** `src/superclaude/cli/roadmap/gates.py`, lines 989-1012

**Status:** EXISTS in codebase. In `ALL_GATES` at line 1137, imported in executor at line 39, used at line 1482.

**Required frontmatter fields (6):**
1. `type`
2. `source_report`
3. `source_report_hash`
4. `total_findings`
5. `actionable`
6. `skipped`

**Semantic checks (2):**
- `frontmatter_values_non_empty`
- `all_actionable_have_status` -- Not all actionable findings have FIXED or FAILED status

### CERTIFY_GATE

**Location:** lines 1014-1041. Also exists, used in executor. Required fields: `findings_verified`, `findings_passed`, `findings_failed`, `certified`, `certification_date`.

### ANTI_INSTINCT_GATE

**Location:** lines 1043-1068. Exists, uses fields: `undischarged_obligations`, `uncovered_contracts`, `fingerprint_coverage`. Header comment notes: "format-agnostic (pure Python). TDD performance hypothesis unverified (I-5)."

### Changes to Existing Gates

No structural changes to any pre-existing gate definitions were observed. EXTRACT_TDD_GATE is the only NEW gate. All others (DEVIATION_ANALYSIS_GATE, REMEDIATE_GATE, CERTIFY_GATE, ANTI_INSTINCT_GATE) are pre-existing.

---

## 3. CLI Option Changes

### --input-type Choice List

**File:** `src/superclaude/cli/roadmap/commands.py`, lines 106-109

```python
@click.option(
    "--input-type",
    type=click.Choice(["auto", "tdd", "spec"], case_sensitive=False),
    default="auto",
    help="Input file type. auto=detect from content (PRD, TDD, or spec), tdd/spec=force type. PRD files are auto-detected when passed as positional arguments. Default: auto.",
)
```

**IMPORTANT FINDING:** The `--input-type` Choice list is `["auto", "tdd", "spec"]` -- it does NOT include `"prd"`. However, the help text mentions PRD: "auto=detect from content (PRD, TDD, or spec)" and "PRD files are auto-detected when passed as positional arguments."

This is a deliberate design: PRD files are auto-detected via `_route_input_files()` when passed as positional arguments. There is no `--input-type prd` override. The models.py Literal includes "prd" (see section 4), but the CLI Choice does not expose it.

### Positional Argument Change: nargs=-1

**File:** `src/superclaude/cli/roadmap/commands.py`, line 33

```python
@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
```

Previously this was `@click.argument("spec_file", ...)` (single file). Now accepts 1-3 files with validation at line 162-166:
```python
if len(input_files) > 3:
    raise click.UsageError(
        f"Expected 1-3 input files, got {len(input_files)}. "
        "Provide at most one spec, one TDD, and one PRD."
    )
```

### Help Text for --tdd-file

**File:** lines 111-121

```
"Path to a TDD file for supplementary technical context enrichment. "
"When the primary input is a spec, the TDD provides data models, "
"API endpoints, component inventory, and test strategy detail. "
"Ignored if the primary input is itself a TDD (use --input-type spec to force)."
```

### Help Text for --prd-file

**File:** lines 122-132

```
"Path to a PRD file for supplementary business context enrichment. "
"The PRD provides personas, success metrics, compliance requirements, "
"and scope boundaries. Works with both spec and TDD primary inputs. "
"Auto-wired from .roadmap-state.json on --resume if not specified."
```

### Run Subcommand Docstring

**File:** lines 152-161

```
"""Run the roadmap generation pipeline on INPUT_FILES.

INPUT_FILES accepts 1-3 markdown files (spec, TDD, PRD) in any order.
Content type is auto-detected. Use --input-type to override for single files.

Examples:
    superclaude roadmap run spec.md
    superclaude roadmap run spec.md tdd.md
    superclaude roadmap run spec.md tdd.md prd.md
"""
```

### TDD Warning Message

**File:** lines 239-248. When `resolved_type == "tdd"`, the CLI emits a yellow warning:
```
NOTE: TDD input detected. The pipeline's deviation-analysis step
(DEVIATION_ANALYSIS_GATE) is not yet TDD-compatible and may fail.
All other steps (extract through spec-fidelity) will work correctly.
```

### Routing Feedback Message

**File:** lines 232-237. Emitted to stderr:
```
[roadmap] Input type: {resolved_type} (spec={routing['spec_file']}, tdd={routing['tdd_file']}, prd={routing['prd_file']})
```

### New Options Added

No entirely new options beyond what was previously documented. The changes are:
- `spec_file` argument renamed to `input_files` with `nargs=-1`
- `--input-type` help text updated to mention PRD
- Function signature updated: `input_files: tuple[Path, ...]` instead of `spec_file: Path`
- Routing logic via `_route_input_files()` call at lines 171-176

---

## 4. Models Changes

### input_type Literal Change

**File:** `src/superclaude/cli/roadmap/models.py`, line 114

```python
input_type: Literal["auto", "tdd", "spec", "prd"] = "auto"  # auto=detect from content, tdd/spec/prd=force
```

The Literal now includes `"prd"` as a valid value. This is wider than the CLI Choice (which only has `["auto", "tdd", "spec"]`). The `"prd"` value can be set internally by `_route_input_files()` when auto-detection identifies a PRD document, but it cannot be forced from the CLI via `--input-type prd`.

### Other Model Changes

- `tdd_file: Path | None = None` (line 115) -- documented as "TDD integration: optional TDD file path for downstream enrichment"
- `prd_file: Path | None = None` (line 116) -- documented as "PRD integration: optional PRD file path for business context enrichment"

These fields were added in prior work (PRD pipeline task). No changes in this iteration beyond the `input_type` Literal widening.

---

## 5. E2E Impact Assessment

### Phase 1 Item 1.3 (Help Output Check)

**Current item text:** "Verify that the pipeline CLI supports the new flags by running `uv run superclaude roadmap run --help 2>&1` and confirming the output contains both `--prd-file` and `--tdd-file` options."

**Impact:** The help output will now show:
- `INPUT_FILES` (plural) instead of `SPEC_FILE` in the usage line
- The examples section will show multi-file usage (`spec.md tdd.md prd.md`)
- `--input-type` will show choices `[auto|tdd|spec]` (NOT including prd)
- `--prd-file` and `--tdd-file` are still present as options

**Recommendation:** Item 1.3 should also verify:
- The positional argument is `INPUT_FILES` (not `SPEC_FILE`)
- The help text mentions "1-3 markdown files"
- `--input-type` choices are `[auto|tdd|spec]`

### Phase 3 Items (Dry-Run Checks)

**Current items check for:** Step plan output, flag acceptance, auto-detection messages.

**Impact from routing feedback:** The stderr now emits `[roadmap] Input type: {type} (spec=..., tdd=..., prd=...)` at lines 233-237. Dry-run items can check for this message to verify routing.

**Impact from TDD warning:** When running TDD primary input (Phase 3 item 3.1), stderr will contain the yellow DEVIATION_ANALYSIS_GATE warning. Items should account for this.

**Impact from multi-file support:** The dry-run can now be invoked with positional files instead of `--tdd-file`/`--prd-file` flags:
```
superclaude roadmap run spec.md tdd.md prd.md --dry-run
```
New E2E items could test positional file routing via dry-run.

### Phase 4 Items (Extraction Frontmatter)

**Impact:** When `input_type == "tdd"`, the extraction step uses EXTRACT_TDD_GATE which requires 19 frontmatter fields (13 standard + 6 TDD-specific). E2E items that verify extraction.md frontmatter must check for all 6 additional fields:
- `data_models_identified`
- `api_surfaces_identified`
- `components_identified`
- `test_artifacts_identified`
- `migration_items_identified`
- `operational_items_identified`

For spec-path runs, EXTRACT_GATE applies with only 13 fields. No change needed.

### Gate Name References

No E2E items directly reference gate names like `EXTRACT_TDD_GATE` by string. The gates are enforced internally. However, the TDD warning message at line 243 references `DEVIATION_ANALYSIS_GATE` by name -- any E2E item checking for this warning should match that exact string.

### Multi-File Routing E2E Items (New)

The existing E2E task does not have items that test:
1. Passing multiple positional files (`spec.md tdd.md prd.md`) instead of using `--tdd-file`/`--prd-file`
2. Verifying `_route_input_files()` correctly classifies each file
3. Verifying the error when >3 files are passed
4. Verifying conflict detection (e.g., two TDD files passed positionally)

These would be new E2E items if the task is being updated.

---

## Summary

| Change | File | Lines | E2E Impact |
|--------|------|-------|------------|
| EXTRACT_TDD_GATE (19 fields) | gates.py | 797-835 | Phase 4 TDD extraction checks need 6 extra fields |
| DEVIATION_ANALYSIS_GATE TDD incompatibility warning | commands.py | 239-248 | Phase 3 TDD dry-run sees yellow warning |
| `--input-type` Choice is `[auto, tdd, spec]` (NO prd) | commands.py | 106-109 | Phase 1 help check: verify no "prd" in choices |
| `input_type` Literal includes "prd" | models.py | 114 | Internal only -- "prd" set by routing, not CLI |
| Positional `input_files` nargs=-1 | commands.py | 33 | Phase 1 help: verify `INPUT_FILES` in usage |
| Routing feedback `[roadmap] Input type: ...` | commands.py | 233-237 | Phase 3 dry-run can verify routing output |
| REMEDIATE_GATE, CERTIFY_GATE pre-existing | gates.py | 989-1041 | No change to E2E items |
| ANTI_INSTINCT_GATE pre-existing | gates.py | 1043-1068 | Known blocker, no change |
