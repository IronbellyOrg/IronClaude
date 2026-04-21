# Research: Auto-Detection & Multi-File Routing Changes

| Field | Value |
|-------|-------|
| Topic type | Data Flow Tracer + Integration Points |
| Status | Complete |
| Date | 2026-04-02 |
| Researcher | researcher-02 |
| Track Goal | Update E2E rerun task file to reflect auto-detection changes |

---

## 1. PRD Detection in detect_input_type()

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 63-186

### 5 PRD Signals with Weights

| # | Signal | Weight | Implementation Detail |
|---|--------|--------|----------------------|
| 1 | Frontmatter `type` contains "Product Requirements" | +3 | Checks `content[:1000]` only (line 94) |
| 2 | 12 PRD-exclusive section headings | +1 each (max +12) | Exact strings: "User Personas", "Jobs To Be Done", "Product Vision", "Customer Journey", "Value Proposition", "Competitive Analysis", "User Stories", "User Experience Requirements", "Legal and Compliance", "Success Metrics and Measurement", "Maintenance and Ownership", "Background and Strategic Fit" (lines 98-107) |
| 3 | User story regex `As .+, I want` | +2 | `re.search()` across full content (line 110) |
| 4 | JTBD regex `When I .+ I want to` | +2 | `re.search()` across full content (line 114) |
| 5 | `prd` tag in frontmatter | +2 | `re.search(r"tags:.*\bprd\b", content[:2000])` (line 118) |

**Max possible PRD score:** 3 + 12 + 2 + 2 + 2 = **21**

### Threshold and Ordering

- **Threshold:** `prd_score >= 5` triggers return "prd" (line 121)
- **Order:** PRD scoring runs FIRST, before TDD scoring (lines 90-129 vs 131-185). If PRD threshold met, function returns immediately -- TDD scoring never runs.
- This means a document with both PRD and TDD signals will always be classified as PRD if PRD score >= 5.

### Borderline Warning Behavior

- If `3 <= prd_score <= 6`, a `_log.warning()` is emitted (lines 123-128):
  `"Borderline PRD detection score (%d) for %s -- result=prd. Use --input-type to override if incorrect."`
- Note: warning is only emitted when score is already >= 5 (i.e., scores 5 and 6 trigger both return "prd" AND the warning).
- Scores 3 and 4 do NOT trigger the warning because the `if prd_score >= 5` check (line 121) comes first, and scores below 5 fall through to TDD scoring without warning.

### Behavioral Differences from Original

The original `detect_input_type()` only had TDD scoring (numbered headings, exclusive frontmatter fields, section names, type field) with threshold >= 5 and spec as fallback. The new version adds:
1. A complete PRD scoring block that runs first
2. Three-way return values: "prd", "tdd", or "spec" (previously only "tdd" or "spec")
3. `_log.info()` messages now distinguish prd vs tdd scoring paths

---

## 2. _route_input_files() Routing Function

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 188-316

### Input Parameters

```python
def _route_input_files(
    input_files: tuple[Path, ...],     # Positional files from CLI (nargs=-1)
    explicit_tdd: Path | None,         # --tdd-file flag value
    explicit_prd: Path | None,         # --prd-file flag value
    explicit_input_type: str,          # --input-type flag value ("auto", "tdd", "spec")
) -> dict:
```

### Return Value Format

```python
{
    "spec_file": Path,           # Always set (spec or TDD-as-primary)
    "tdd_file": Path | None,     # Set if supplementary TDD detected/provided
    "prd_file": Path | None,     # Set if PRD detected/provided
    "input_type": str,           # "spec" or "tdd" (resolved primary type)
}
```

### Step-by-Step Routing Logic (12 steps, not 14)

| Step | Lines | Description |
|------|-------|-------------|
| 1 | 201-208 | **Validate count:** 0 files -> UsageError; >3 files -> UsageError |
| 2 | (skipped) | Step numbering in code skips from 1 to 3 |
| 3 | 211-213 | **Classify each file:** Call `detect_input_type(f)` for every positional file |
| 4 | 216-222 | **Apply explicit override (single-file only):** If `--input-type != auto` AND exactly 1 file, override that file's classification. If multi-file + `--input-type != auto`, emit `_log.warning` that it's ignored |
| 5 | 224-234 | **Validate no duplicates:** Count files per type; if any type has >1 file, raise UsageError: `"Multiple files detected as {t}: {names}. Use --input-type to disambiguate."` |
| 6 | 236-246 | **Validate primary input exists:** Must have spec or tdd. If only PRD -> UsageError: `"PRD cannot be the sole primary input; provide a spec or TDD file."`. If nothing detected -> UsageError: `"No primary input (spec or TDD) detected."` |
| 7 | 248-262 | **Assign slots:** If has_spec: spec_file = spec, tdd_file = tdd (if present). If no spec: TDD becomes spec_file (TDD-as-primary). PRD assigned to prd_file if present |
| 8 | 264-279 | **Merge explicit flags:** If `--tdd-file` provided but tdd_file already set from positional -> UsageError: `"--tdd-file conflicts with positional file detected as TDD; remove one."`. Same for `--prd-file` |
| 9 | 281-289 | **Determine input_type:** "spec" if has_spec, else "tdd". Single-file explicit override already applied via classifications in step 4 |
| 10 | 291-296 | **Redundancy guard:** If `input_type == "tdd"` and `tdd_file` is set, log warning and set `tdd_file = None` (TDD is already the primary, supplementary TDD is redundant) |
| 11 | 298-308 | **Same-file guard:** Check all 3 pairs (spec/tdd, spec/prd, tdd/prd). If any pair resolves to same file -> UsageError: `"{name_a} and {name_b} point to the same file: {a}"` |
| 12 | 310-316 | **Return** dict with spec_file, tdd_file, prd_file, input_type |

### Error Conditions (6 distinct UsageError messages)

1. `"At least one input file required."` (step 1, line 203)
2. `"Expected 1-3 input files, got {N}..."` (step 1, line 205-208)
3. `"Multiple files detected as {t}: {names}..."` (step 5, lines 231-234)
4. `"PRD cannot be the sole primary input..."` (step 6, line 242-244)
5. `"No primary input (spec or TDD) detected."` (step 6, line 246)
6. `"--tdd-file conflicts with positional file detected as TDD..."` (step 8, line 267-269)
7. `"--prd-file conflicts with positional file detected as PRD..."` (step 8, line 275-277)
8. `"{name_a} and {name_b} point to the same file: {a}"` (step 11, lines 306-308)

---

## 3. CLI Changes (commands.py)

**File:** `src/superclaude/cli/roadmap/commands.py`

### nargs=-1 Argument Change

- **Old:** `@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))`
- **New (line 33):** `@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))`
- Parameter type changed from `spec_file: Path` to `input_files: tuple[Path, ...]` (line 139)

### File Count Validation

- Lines 162-166: `if len(input_files) > 3` raises `click.UsageError`
- Note: This is in the `run()` function body, separate from `_route_input_files()` which also validates count. **Duplicate validation** exists (commands.py line 162 AND executor.py line 204-208).

### Routing Integration

- Lines 167-176: Imports `_route_input_files` from executor, calls it with positional files + explicit flags
- The `routing` dict is used to populate `RoadmapConfig` kwargs (lines 210-222)

### New stderr Output Format

- **Old format:** `"[roadmap] Auto-detected input type: X"` (removed from commands.py)
- **New format (line 233-236):**
  ```
  [roadmap] Input type: {resolved_type} (spec={routing['spec_file']}, tdd={routing['tdd_file']}, prd={routing['prd_file']})
  ```
- Written to `err=True` (stderr)

### --input-type Choice: DISCREPANCY FOUND

- **commands.py line 107:** `click.Choice(["auto", "tdd", "spec"], case_sensitive=False)` -- does NOT include "prd"
- **models.py line 114:** `Literal["auto", "tdd", "spec", "prd"]` -- DOES include "prd"
- **help text (line 109):** Mentions PRD detection but the Choice list won't accept "prd" as a value
- **Impact:** Users cannot force `--input-type prd` from the CLI even though the model supports it. PRD detection is auto-only.

### --prd-file Flag

- Lines 124-132: New `--prd-file` option added with `type=click.Path(exists=True, path_type=Path)`
- Help text describes PRD enrichment and auto-wiring from `.roadmap-state.json` on `--resume`

---

## 4. New Test Coverage

**File:** `tests/cli/test_tdd_extract_prompt.py`

### 5 New Test Classes Added

| Class | Lines | Tests | What It Covers |
|-------|-------|-------|----------------|
| `TestPrdDetection` | 507-558 | 4 tests | PRD detection from real fixture, synthetic PRD signals, not confused with TDD, not confused with spec |
| `TestThreeWayBoundary` | 561-607 | 4 tests | PRD score below threshold -> spec, PRD score at threshold -> prd, TDD-only signals -> tdd, both PRD+TDD signals -> PRD wins (order priority) |
| `TestMultiFileRouting` | 610-732 | 10 tests | Single-file routing (spec, tdd, prd-raises), multi-file routing (spec+tdd, spec+prd, tdd+prd, all three), error cases (duplicate type, too many files, conflict positional+explicit) |
| `TestBackwardCompat` | 735-772 | 3 tests | Single positional routes like before, explicit --input-type overrides detection, explicit --tdd-file works with positional |
| `TestOverridePriority` | 775-822 | 2 tests | --input-type ignored for multifile, explicit --prd-file supplements positional spec+tdd |

**Total new tests: 23** (4 + 4 + 10 + 3 + 2)

### Pre-existing Related Test Classes (not new, but relevant)

| Class | Tests | Covers |
|-------|-------|--------|
| `TestAutoDetection` | 8 | Original TDD vs spec detection |
| `TestDetectionThresholdBoundary` | 4 | TDD score boundary (4->spec, 5->tdd, 6->tdd, 0->spec) |
| `TestSameFileGuard` | 2 | Same-file raises SystemExit / different files ok |
| `TestPrdFileOverrideOnResume` | 1 | Explicit --prd-file not overwritten by state |
| `TestRedundancyGuardStatePersistence` | 2 | TDD-primary nullifies tdd_file, no warning when no tdd_file |

---

## 5. E2E Test Items Needed

The following E2E test items should be added to verify auto-detection and routing behaviors end-to-end (i.e., through the actual CLI invocation, not just unit tests of the functions).

### 5.1 Multi-File Invocation

| # | E2E Test Item | What to Verify | Priority |
|---|---------------|----------------|----------|
| E2E-AD-01 | `superclaude roadmap run spec.md tdd.md --dry-run` | Two positional files accepted, routing assigns spec_file=spec.md and tdd_file=tdd.md, input_type=spec. stderr shows new format `[roadmap] Input type: spec (spec=spec.md, tdd=tdd.md, prd=None)` | High |
| E2E-AD-02 | `superclaude roadmap run tdd.md prd.md --dry-run` | TDD becomes primary (spec_file=tdd.md), prd_file=prd.md, tdd_file=None (redundancy guard), input_type=tdd | High |
| E2E-AD-03 | `superclaude roadmap run spec.md tdd.md prd.md --dry-run` | Three files routed correctly to all three slots, input_type=spec | High |
| E2E-AD-04 | `superclaude roadmap run f1.md f2.md f3.md f4.md` | >3 files raises UsageError with message containing "1-3" | Medium |
| E2E-AD-05 | `superclaude roadmap run tdd.md prd.md` (reversed order) | Order of positional arguments does not affect routing (content detection, not position) | High |

### 5.2 PRD Auto-Detection Verification

| # | E2E Test Item | What to Verify | Priority |
|---|---------------|----------------|----------|
| E2E-AD-06 | `superclaude roadmap run prd.md --dry-run` | Single PRD file raises UsageError: "PRD cannot be the sole primary input" | High |
| E2E-AD-07 | `superclaude roadmap run spec.md --prd-file prd.md --dry-run` | Explicit --prd-file supplements positional spec, stderr shows prd=prd.md | Medium |
| E2E-AD-08 | Real fixture detection: run detect_input_type on `.dev/test-fixtures/test-prd-user-auth.md` | Returns "prd" (not "spec" or "tdd") | High |

### 5.3 Three-Way Detection Boundary

| # | E2E Test Item | What to Verify | Priority |
|---|---------------|----------------|----------|
| E2E-AD-09 | File with both PRD and TDD signals | PRD wins due to scoring order (PRD checked first) | Medium |
| E2E-AD-10 | File with PRD score = 4 (below threshold) | Falls through to TDD scoring or defaults to spec | Medium |

### 5.4 Routing Conflict Handling

| # | E2E Test Item | What to Verify | Priority |
|---|---------------|----------------|----------|
| E2E-AD-11 | `superclaude roadmap run spec.md tdd.md --tdd-file other-tdd.md` | Raises UsageError about --tdd-file conflict with positional TDD | High |
| E2E-AD-12 | `superclaude roadmap run spec.md prd.md --prd-file other-prd.md` | Raises UsageError about --prd-file conflict with positional PRD | High |
| E2E-AD-13 | `superclaude roadmap run spec1.md spec2.md` (two specs) | Raises UsageError: "Multiple files detected as spec" | Medium |

### 5.5 Backward Compatibility

| # | E2E Test Item | What to Verify | Priority |
|---|---------------|----------------|----------|
| E2E-AD-14 | `superclaude roadmap run spec.md --dry-run` | Single-file invocation works identically to pre-change behavior | Critical |
| E2E-AD-15 | `superclaude roadmap run spec.md --tdd-file tdd.md --dry-run` | Explicit --tdd-file flag still works with single positional file | High |
| E2E-AD-16 | `superclaude roadmap run spec.md --input-type tdd --dry-run` | --input-type override works for single file | Medium |

### 5.6 New stderr Output Format Verification

| # | E2E Test Item | What to Verify | Priority |
|---|---------------|----------------|----------|
| E2E-AD-17 | Capture stderr from any `roadmap run` invocation | Format is `[roadmap] Input type: {type} (spec=..., tdd=..., prd=...)` NOT old format `[roadmap] Auto-detected input type: X` | High |
| E2E-AD-18 | TDD primary input stderr | Shows yellow NOTE about DEVIATION_ANALYSIS_GATE not being TDD-compatible (lines 239-248 of commands.py) | Low |

### 5.7 Discrepancy to Address

| # | Item | Detail | Priority |
|---|------|--------|----------|
| E2E-AD-19 | `--input-type prd` not accepted by CLI | commands.py Choice is `["auto", "tdd", "spec"]` but models.py Literal includes "prd". Users cannot force PRD type. Either add "prd" to Choice or document this as intentional. | Medium |

---

## Summary

**Key findings:**

1. `detect_input_type()` now performs three-way classification (prd/tdd/spec) with PRD scored first. 5 weighted PRD signals with threshold >= 5.
2. `_route_input_files()` is a new 12-step routing function that classifies N positional files, merges explicit flags, validates conflicts, and returns slot assignments.
3. CLI changed from single `spec_file` to `nargs=-1` `input_files` accepting 1-3 files. New stderr output format shows all three slots.
4. 23 new unit tests across 5 test classes cover detection, boundary, routing, backward compat, and override priority.
5. **Discrepancy found:** `--input-type` Click.Choice lacks "prd" while `models.py` Literal includes it (commands.py line 107 vs models.py line 114).
6. **19 E2E test items** identified across 7 categories to verify these behaviors end-to-end.
