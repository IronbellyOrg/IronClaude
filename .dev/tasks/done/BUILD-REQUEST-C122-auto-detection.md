# BUILD REQUEST: C-122 — Multi-File Auto-Detection and Routing

## What This Is

Upgrade the `superclaude roadmap run` CLI to accept multiple input files as positional arguments and auto-detect which is a TDD, PRD, or spec. Currently users must explicitly use `--tdd-file` and `--prd-file` flags — this change makes the CLI smart enough to route files automatically.

## Why It Matters

Users should be able to do:
```
superclaude roadmap run tdd.md prd.md        # auto-detects, routes correctly
superclaude roadmap run prd.md tdd.md        # same result, order irrelevant
superclaude roadmap run tdd.md               # just TDD, no PRD
superclaude roadmap run spec.md prd.md       # spec + PRD, no TDD
```

Currently they MUST do:
```
superclaude roadmap run spec.md --tdd-file tdd.md --prd-file prd.md
```

If a user passes a PRD as the positional arg today, it silently misclassifies as "spec" — there's no PRD detection at all. This absorbs findings C-19 (content validation), C-53 (input-type vs content), and C-55 (PRD misclassification).

## Current State

### Detection (`src/superclaude/cli/roadmap/executor.py:63-133`)

`detect_input_type(spec_file: Path) -> str` uses 4 weighted signals to return `"tdd"` or `"spec"`:
1. Numbered section headings `## N.` — TDDs have ~28, specs ~12 (+1/+2/+3 by count)
2. TDD-exclusive frontmatter fields: `parent_doc`, `coordinator` (+2 each)
3. TDD-specific section names: 8 keywords like "Data Models", "API Specifications" (+1 each)
4. Frontmatter type containing "Technical Design Document" (+2)

Threshold: score >= 5 = TDD, else spec. Max possible = 17.

**No PRD detection exists.** PRDs would score 0-2 on TDD signals and be classified as "spec."

### CLI Args (`src/superclaude/cli/roadmap/commands.py:32-132`)

```python
@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))  # single positional
@click.option("--tdd-file", ...)   # supplementary TDD
@click.option("--prd-file", ...)   # supplementary PRD
@click.option("--input-type", type=click.Choice(["auto", "tdd", "spec"]), default="auto")
```

Only ONE positional arg. `--tdd-file` and `--prd-file` are named flags.

### Routing (`src/superclaude/cli/roadmap/executor.py:execute_roadmap`)

After detection resolves input_type:
- `config.spec_file` = primary input (positional arg)
- `config.tdd_file` = supplementary TDD (`--tdd-file`)
- `config.prd_file` = supplementary PRD (`--prd-file`)
- Redundancy guard: if `input_type == "tdd"` and `tdd_file` is not None → null tdd_file
- Same-file guard: tdd_file and prd_file can't be the same file

### Pipeline Consumption

All prompt builders accept `tdd_file` and `prd_file` as optional params:
- `build_extract_prompt()` / `build_extract_prompt_tdd()` — extraction
- `build_generate_prompt()` — roadmap generation
- `build_score_prompt()` — variant scoring
- `build_merge_prompt()` — final merge
- `build_test_strategy_prompt()` — test strategy
- `build_spec_fidelity_prompt()` — fidelity validation

The `_embed_inputs()` function labels files with semantic roles based on `RoadmapConfig`.

### Gate Routing

- `EXTRACT_GATE` (13 fields) for spec input
- `EXTRACT_TDD_GATE` (19 fields) for TDD input
- No PRD-specific gate (PRD enriches body sections, not frontmatter)

## What Needs to Change

### 1. PRD Detection — New Function or Extend `detect_input_type`

PRD detection signals (from analyzing `test-prd-user-auth.md` and the PRD skill template):

**PRD-exclusive frontmatter fields:**
- `type: "Product Requirements"` or containing "PRD" (+3)

**PRD-specific section names (not found in TDD or spec):**
- "User Personas" (+2)
- "Jobs To Be Done" / "JTBD" (+2)
- "Customer Journey Map" (+1)
- "Value Proposition Canvas" (+1)
- "Competitive Analysis" (+1)
- "Success Metrics and Measurement" (+1)
- "Business Context" (+1)

**PRD-exclusive frontmatter tags:**
- `tags` containing "prd" (+2)

**Negative signals (rules out PRD):**
- TDD score >= 5 → it's a TDD, not a PRD
- Numbered section headings (## N.) >= 10 → likely TDD or spec, not PRD

**Approach:** Change `detect_input_type` to return `"tdd"`, `"prd"`, or `"spec"` (three-way classification). Run TDD detection first (existing). If TDD score < 5, run PRD detection. If PRD score >= threshold, return "prd". Else return "spec".

### 2. Multi-Positional Args — CLI Change

Change from:
```python
@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))
```
To:
```python
@click.argument("input_files", nargs=-1, type=click.Path(exists=True, path_type=Path), required=True)
```

Must accept 1-3 files. Error if 0 or >3.

### 3. Routing Logic — New Function

After detecting each file's type, assign to slots:
```python
def _route_input_files(input_files: tuple[Path, ...]) -> dict:
    """Detect each file's type and assign to spec_file, tdd_file, prd_file slots.

    Returns dict with keys: spec_file, tdd_file, prd_file, input_type.
    Raises SystemExit with clear error if:
    - Two files detect as the same type (e.g., two TDDs)
    - No file detects as spec or TDD (need at least one primary input)
    - More than 3 files provided
    """
```

Routing rules:
- If 1 file: detect type → assign as primary (`spec_file`), set `input_type`
- If 2 files: detect both → assign primary (TDD or spec) to `spec_file`, supplementary to `tdd_file` or `prd_file`
- If 3 files: detect all → must have exactly one of each type (or one spec + one TDD, and one PRD)
- If two files detect as the same type → error with clear message
- PRD can never be the primary input for the pipeline — it must always be supplementary

### 4. Backward Compatibility

- `--tdd-file` and `--prd-file` flags remain as explicit overrides
- `--input-type` flag remains as explicit override
- If explicit flags are provided alongside positional args, explicit wins
- Single positional arg still works exactly as before
- `--input-type` choices expand from `["auto", "tdd", "spec"]` to `["auto", "tdd", "spec", "prd"]`

### 5. State File

The state file already stores `input_type`, `tdd_file`, `prd_file`. No schema change needed. Just ensure the resolved routing is saved, not "auto".

### 6. Update `--input-type` Choice

Add "prd" to the valid choices. When `--input-type prd` is forced, the file is treated as supplementary PRD context — the user must also provide a spec or TDD as the primary input.

## Key Files to Modify

| File | Changes |
|------|---------|
| `src/superclaude/cli/roadmap/executor.py` | Extend `detect_input_type` with PRD signals. Add `_route_input_files()`. |
| `src/superclaude/cli/roadmap/commands.py` | Change positional arg to `nargs=-1`. Add routing call before `RoadmapConfig` construction. Update `--input-type` choices. |
| `src/superclaude/cli/roadmap/models.py` | Update `input_type` type hint to include `"prd"`. |
| `tests/cli/test_tdd_extract_prompt.py` | Add PRD detection tests, multi-file routing tests, boundary tests. |

## Key Files to Read (context for task builder)

| File | Why |
|------|-----|
| `src/superclaude/cli/roadmap/executor.py` | Current detection logic, routing, redundancy guard |
| `src/superclaude/cli/roadmap/commands.py` | Current CLI arg structure |
| `src/superclaude/cli/roadmap/models.py` | RoadmapConfig dataclass |
| `.dev/test-fixtures/test-prd-user-auth.md` | Real PRD for detection signal analysis |
| `.dev/test-fixtures/test-tdd-user-auth.md` | Real TDD for comparison |
| `.dev/test-fixtures/test-spec-user-auth.md` | Real spec for comparison |
| `src/superclaude/skills/prd/SKILL.md` | PRD template structure |
| `src/superclaude/examples/tdd_template.md` | TDD template for signal comparison |
| `src/superclaude/examples/release-spec-template.md` | Spec template for signal comparison |
| `tests/cli/test_tdd_extract_prompt.py` | Existing detection tests to extend |

## Testing Requirements

1. **PRD detection tests:** Real PRD fixture detected as "prd", not "tdd" or "spec"
2. **Three-way boundary tests:** PRD doesn't trigger TDD detection, TDD doesn't trigger PRD detection, spec triggers neither
3. **Multi-file routing tests:**
   - 1 file (TDD) → spec_file=TDD, input_type=tdd
   - 1 file (PRD) → error (PRD can't be primary)
   - 2 files (TDD + PRD) → spec_file=TDD, prd_file=PRD, input_type=tdd
   - 2 files (spec + PRD) → spec_file=spec, prd_file=PRD, input_type=spec
   - 2 files (spec + TDD) → spec_file=spec, tdd_file=TDD, input_type=spec
   - 3 files (spec + TDD + PRD) → all assigned correctly
   - 2 files same type → error
4. **Backward compatibility tests:** Single positional + explicit flags still work
5. **Override tests:** `--input-type` overrides detection, `--tdd-file`/`--prd-file` override routing

## Constraints

- `uv run superclaude` for all pipeline runs (not bare `superclaude`)
- `make sync-dev` after editing any skill/command files in `src/superclaude/`
- Run `uv run pytest tests/cli/test_tdd_extract_prompt.py tests/roadmap/ tests/tasklist/ -v --tb=short` after code changes
- Do NOT modify the prompt builders — they already accept tdd_file/prd_file correctly
- Do NOT change the gate system — EXTRACT_GATE and EXTRACT_TDD_GATE already route by input_type
