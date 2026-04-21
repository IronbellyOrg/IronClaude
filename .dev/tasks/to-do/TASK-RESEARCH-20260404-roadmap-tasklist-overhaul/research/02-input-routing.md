# Research: Input Routing

**Investigation type:** Code Tracer
**Scope:** executor.py (detect_input_type, _route_input_files, _embed_inputs), commands.py, models.py
**Status:** Complete
**Date:** 2026-04-04

---

## 1. Entry Point: CLI Command (`commands.py`)

**File:** `src/superclaude/cli/roadmap/commands.py`

The `run` command accepts 1-3 positional `input_files` (line 33) plus two explicit flags:

- `--input-type` (line 107): Choice of `["auto", "tdd", "spec"]`. Default `"auto"`. Note: `"prd"` is NOT a valid CLI choice even though `detect_input_type()` can return it and `RoadmapConfig.input_type` allows it.
- `--tdd-file` (line 113): Explicit TDD file path for supplementary context.
- `--prd-file` (line 124): Explicit PRD file path for supplementary business context.

The command immediately calls `_route_input_files()` (line 171) to classify positional files and merge with explicit flags, then constructs `RoadmapConfig` (line 229) with the routing result.

**Key observation:** The command does NOT pass `input_type` through to the config directly. It passes `routing["input_type"]` (line 220), which is the resolved type from `_route_input_files()`.

---

## 2. Data Model: `RoadmapConfig` (`models.py`)

**File:** `src/superclaude/cli/roadmap/models.py`, lines 94-116

`RoadmapConfig` extends `PipelineConfig` and carries three input-routing fields:

```python
input_type: Literal["auto", "tdd", "spec", "prd"] = "auto"  # line 114
tdd_file: Path | None = None                                  # line 115
prd_file: Path | None = None                                  # line 116
```

`PipelineConfig` (in `src/superclaude/cli/pipeline/models.py`, line 170) has NO input-routing awareness. It only knows about `work_dir`, `dry_run`, `max_turns`, `model`, `permission_flag`, `debug`, `grace_period`.

**Key observation:** The `input_type` Literal includes `"prd"` even though the CLI `--input-type` choice does not. PRD is only reachable via auto-detection, never via explicit CLI override.

---

## 3. Auto-Detection: `detect_input_type()` (`executor.py`)

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 63-185

This function takes a single `Path` and returns `"prd"`, `"tdd"`, or `"spec"` using a weighted scoring system. Detection order is: PRD first, then TDD, with spec as fallback.

### 3a. PRD Detection (checked first, threshold >= 5)

| Signal | Weight | Description |
|--------|--------|-------------|
| Frontmatter contains "Product Requirements" (first 1000 chars) | +3 | Type field |
| 12 PRD-exclusive section headings (e.g., "User Personas", "Jobs To Be Done") | +1 each | Up to +12 |
| Regex `As .+, I want` matches | +2 | User story pattern |
| Regex `When I .+ I want to` matches | +2 | JTBD pattern |
| Regex `tags:.*\bprd\b` in first 2000 chars | +2 | Frontmatter tag |

Max possible: 21. Threshold: >= 5 returns `"prd"`. Borderline warning at 3-6.

### 3b. TDD Detection (checked second, threshold >= 5)

| Signal | Weight | Description |
|--------|--------|-------------|
| Numbered headings (`## N.` pattern): >=20 | +3 | Strong TDD signal |
| Numbered headings: >=15 | +2 | Moderate signal |
| Numbered headings: >=10 | +1 | Weak (specs can have 12) |
| TDD-exclusive frontmatter fields: `parent_doc`, `coordinator` | +2 each | Up to +4 |
| 8 TDD-specific section names (e.g., "Data Models", "API Specifications") | +1 each | Up to +8 |
| Frontmatter contains "Technical Design Document" (first 1000 chars) | +2 | Type field |

Max possible: 17. Threshold: >= 5 returns `"tdd"`. Borderline warning at 3-6.

### 3c. Fallback

Everything that scores below both thresholds returns `"spec"`.

**Key observation:** Detection is content-based, not filename-based. A file named `tdd.md` that lacks TDD structural markers will be classified as `"spec"`.

---

## 4. Routing: `_route_input_files()` (`executor.py`)

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 188-316

This function takes positional files + explicit flags and produces a dict with four keys: `spec_file`, `tdd_file`, `prd_file`, `input_type`.

### Algorithm (12 steps):

1. **Validate count** (lines 201-208): 0 files = error, >3 files = error.
2. *(step 2 missing in source -- numbering skips to 3)*
3. **Classify each file** (lines 211-213): Calls `detect_input_type()` on every positional file.
4. **Apply explicit override** (lines 216-222): `--input-type` only applies when there is exactly 1 input file. For multi-file mode, the flag is ignored with a warning.
5. **Validate no duplicates** (lines 225-234): If two files classify as the same type, raises `UsageError`.
6. **Validate primary input exists** (lines 237-246): At least one file must be `"spec"` or `"tdd"`. A PRD alone is rejected.
7. **Assign slots** (lines 249-262):
   - If spec exists: `spec_file = spec`, `tdd_file = tdd` (if detected).
   - If NO spec but TDD exists: **TDD becomes `spec_file`** (line 259). This is critical -- the TDD occupies the `spec_file` slot.
8. **Merge explicit flags** (lines 265-279): `--tdd-file` and `--prd-file` fill empty slots. Conflicts with positional files raise errors.
9. **Determine input_type** (lines 282-289): `"spec"` if spec detected, `"tdd"` otherwise. Single-file explicit override re-applied.
10. **Redundancy guard** (lines 292-296): If `input_type == "tdd"` and `tdd_file` is also set, the supplementary TDD is dropped (the primary already IS a TDD).
11. **Same-file guard** (lines 299-308): Prevents spec/tdd/prd from pointing to the same file.
12. **Return** (lines 311-316): Dict with all four fields.

### Critical Routing Behaviors:

**When input_type is "tdd":** The TDD file is assigned to the `spec_file` slot (step 7, line 259). This means ALL downstream code that reads `config.spec_file` is actually reading the TDD. The `tdd_file` slot is set to `None` (step 10, line 296).

**When input_type is "spec" with supplementary TDD:** The spec occupies `spec_file`, the TDD occupies `tdd_file`. Both are available to all steps.

**When input_type is "spec" with supplementary PRD:** The spec occupies `spec_file`, the PRD occupies `prd_file`.

**Three-file mode (spec + TDD + PRD):** All three slots populated. `input_type = "spec"`.

---

## 5. Input Embedding: `_embed_inputs()` (`executor.py`)

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 331-352

Pure function that reads files from `step.inputs` and returns concatenated fenced code blocks with semantic labels.

Labels are built in `roadmap_run_step()` (lines 723-731):
- `config.spec_file` -> `"[Primary input - {config.input_type}]"`
- `config.tdd_file` -> `"[TDD - supplementary technical context]"`
- `config.prd_file` -> `"[PRD - supplementary business context]"`

The composed prompt = `step.prompt + "\n\n" + embedded_content`. Size limit is 120 KB (`_EMBED_SIZE_LIMIT`, line 324); exceeding logs a warning but embeds anyway.

---

## 6. Propagation Through Pipeline Steps

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 1299-1490 (`_build_steps`)

### Step-by-step input_type influence:

| Step | input_type="spec" | input_type="tdd" | TDD/PRD as Supplementary |
|------|-------------------|-------------------|--------------------------|
| **extract** | `build_extract_prompt()` with EXTRACT_GATE | `build_extract_prompt_tdd()` with EXTRACT_TDD_GATE (1800s timeout vs 300s) | TDD/PRD appended as prompt sections |
| **generate-A/B** | extraction + optional TDD/PRD in inputs | extraction + optional TDD/PRD in inputs (same) | TDD adds "TDD as Primary Work Item Source" prompt block |
| **diff** | Two roadmap variants only | Same | No TDD/PRD access |
| **debate** | diff + two variants | Same | No TDD/PRD access |
| **score** | debate + two variants + optional TDD/PRD | Same | TDD/PRD in inputs |
| **merge** | score + two variants + debate + optional TDD/PRD | Same | TDD/PRD in inputs |
| **anti-instinct** | spec + roadmap.md (deterministic, no LLM) | Same | No TDD/PRD |
| **test-strategy** | roadmap + extraction + optional TDD/PRD | Same | TDD/PRD in inputs |
| **spec-fidelity** | spec + roadmap + optional TDD/PRD | Same | TDD/PRD in inputs |
| **wiring-verification** | roadmap + spec-fidelity (deterministic) | Same | No TDD/PRD |
| **deviation-analysis** | spec-fidelity + roadmap (deterministic) | Same | No TDD/PRD |
| **remediate** | deviation + spec-fidelity + roadmap (deterministic) | Same | No TDD/PRD |

### What changes between spec and TDD input_type:

1. **Extract step prompt:** Completely different prompt function. TDD extraction has 14 sections (8 standard + 6 TDD-specific: Data Models, API Specs, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness). Spec extraction has only 8 sections.
2. **Extract step gate:** `EXTRACT_TDD_GATE` requires 6 additional frontmatter fields (`data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`). Standard `EXTRACT_GATE` requires only 13 fields.
3. **Extract step timeout:** TDD extraction gets 1800s (30 min) vs 300s (5 min) for spec extraction.
4. **Structural audit warning:** Line 808 notes that structural audit uses spec heading patterns, not TDD patterns. TDD audit results are unreliable.
5. **Deviation analysis:** Line 239-248 in commands.py prints a CLI warning that the deviation-analysis step is "not yet TDD-compatible and may fail."

### What does NOT change between spec and TDD:

- Steps 2-12 use identical prompt builders and gates regardless of `input_type`.
- The `build_generate_prompt()` does NOT have a TDD-specific variant; it always receives the extraction document and optionally the TDD file (via `tdd_file` parameter).
- Diff and debate steps have NO access to TDD/PRD files at all.

---

## 7. Where Extraction Is Invoked vs Bypassed

Extraction is **always invoked** as step 1 of the pipeline regardless of input type. There is NO bypass path.

The extraction step is the single gateway through which all source content must pass before reaching downstream steps. Steps 2+ operate on `extraction.md`, not on the original source files.

**Exception:** When `tdd_file` or `prd_file` are set, steps 2 (generate), 5 (score), 6 (merge), 8 (test-strategy), and 9 (spec-fidelity) receive the original TDD/PRD file in their `inputs` list alongside extraction. This means the LLM has direct access to the supplementary file content at those steps. However, the PROMPT instructions for those steps still reference extraction as the primary structured input.

**Critical path for TDD inputs:** When `input_type == "tdd"`, the TDD is in the `spec_file` slot, so steps like anti-instinct, deviation-analysis, and spec-fidelity that reference `config.spec_file` are actually comparing against the original TDD. But the extraction output (which was produced by the TDD-specific prompt) intermediates the data for generation steps.

---

## 8. Double-Routing in `execute_roadmap()`

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 2296-2308

The `execute_roadmap()` function calls `_route_input_files()` a SECOND time (line 2296), even though `commands.py:run()` already called it and passed the result into `RoadmapConfig`. The second call routes `(config.spec_file,)` as a single-element tuple with `config.tdd_file` and `config.prd_file` as explicit flags.

This is redundant for the normal flow but serves the `--resume` path (line 2530), where state restoration may have loaded a config without the original multi-file routing. The same pattern appears in `_apply_resume_after_spec_patch()` (line 2530).

---

## Gaps and Questions

1. **PRD not selectable via `--input-type`:** The CLI restricts `--input-type` to `["auto", "tdd", "spec"]` (line 107 of commands.py), but `detect_input_type()` can return `"prd"` and `RoadmapConfig.input_type` accepts `"prd"`. If a user has a PRD that misdetects as spec, there is no CLI override to force PRD classification.

2. **TDD-as-spec_file semantic confusion:** When `input_type == "tdd"`, the TDD occupies `config.spec_file`. This means code that expects `spec_file` to be a specification is actually operating on a TDD. Steps like `_run_anti_instinct_audit()` and `_run_structural_audit()` assume spec heading patterns and will produce unreliable results on TDD content.

3. **Diff and debate steps lack TDD/PRD context:** Steps 3 (diff) and 4 (debate) operate only on the two roadmap variants with no access to TDD or PRD supplementary content. If the TDD contains granularity the roadmap should preserve, the diff/debate step cannot validate this.

4. **Extraction is never bypassed:** There is no way to skip extraction and feed a pre-existing extraction.md into the pipeline. This matters for iterative workflows where the extraction is correct but downstream steps need re-running.

5. **No `input_type` propagation into prompt builders beyond extract:** Only the extract step has a TDD-specific prompt. All other prompt builders (`build_generate_prompt`, `build_score_prompt`, `build_merge_prompt`, etc.) receive `tdd_file`/`prd_file` as optional parameters but do NOT receive `input_type`. They cannot differentiate between "primary input is TDD" vs "primary input is spec with supplementary TDD."

6. **Borderline detection scores:** Both PRD (3-6) and TDD (3-6) detection emit warnings for borderline scores, but the pipeline continues anyway. There is no interactive confirmation or alternative classification strategy.

7. **Step 2 comment numbering gap:** In `_route_input_files()`, step numbering jumps from 1 to 3 (there is no step 2 comment).

---

## Stale Documentation Found

- **commands.py docstring (line 152-160):** Claims `INPUT_FILES accepts 1-3 markdown files (spec, TDD, PRD) in any order` -- accurate.
- **commands.py line 109:** Says `PRD files are auto-detected when passed as positional arguments` -- accurate.
- **executor.py line 808-809:** Notes that structural audit is not TDD-compatible -- accurate, confirmed by code.
- **commands.py line 239-248:** TDD compatibility warning for deviation-analysis -- accurate.

No stale documentation was found. All documentation accurately reflects current behavior.

---

## Summary

**Input routing is a 3-layer system:**

1. **Detection layer** (`detect_input_type`): Content-based scoring classifies each file as prd/tdd/spec using weighted signals. PRD checked first (threshold 5), then TDD (threshold 5), fallback spec.

2. **Routing layer** (`_route_input_files`): Assigns files to slots (`spec_file`, `tdd_file`, `prd_file`) and resolves `input_type`. Critical behavior: when the primary input is a TDD, it occupies the `spec_file` slot and the supplementary `tdd_file` slot is cleared.

3. **Propagation layer** (`_build_steps` + prompt builders): `input_type` only diverges behavior at the extract step (different prompt, different gate, different timeout). All other steps receive TDD/PRD as supplementary inputs via the `tdd_file`/`prd_file` parameters on prompt builders, but use identical prompt structures regardless of `input_type`.

**Extraction is the universal bottleneck.** Every pipeline run passes through extraction as step 1. The extraction step is the ONLY step where `input_type` changes the prompt and gate. All downstream steps consume `extraction.md` as their primary structured input. This is the granularity loss mechanism: the TDD's 14-section extraction (with DM-xxx, API-xxx, COMP-xxx, TEST-xxx, MIG-xxx, OPS-xxx IDs) is an LLM summarization of the original TDD content, and the generation step then works from this summary rather than the original.

**Mitigation attempt:** Steps 2, 5, 6, 8, and 9 also receive the original TDD/PRD in their `inputs` list, giving the LLM direct access to source content. The `build_generate_prompt()` includes a "TDD as Primary Work Item Source" block when `tdd_file` is set, instructing the LLM to read the TDD directly for granular task rows. However, this creates a tension: the prompt references extraction as the structured input but also instructs reading the TDD directly, leaving the LLM to reconcile two potentially inconsistent sources.

