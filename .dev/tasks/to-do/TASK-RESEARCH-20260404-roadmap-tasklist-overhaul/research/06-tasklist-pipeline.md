# 06 — Tasklist Generation Pipeline: End-to-End Trace

**Status**: Complete
**Date**: 2026-04-04
**Investigator**: Claude Opus 4.6 (Code Tracer)
**Scope**: CLI invocation through tasklist executor, prompt building, output generation, validation, and skill relationship

---

## 1. Architecture Split: CLI vs Skill

The tasklist pipeline is split across two entirely separate execution paths. This is the single most important structural fact about the system.

### CLI Path (programmatic, subprocess-based)
- **Entry**: `superclaude tasklist validate <output_dir>` (Click command in `commands.py`)
- **Scope**: Validation ONLY. There is **no `tasklist generate` CLI subcommand**.
- **Executor**: `execute_tasklist_validate()` in `executor.py`
- **Prompt**: `build_tasklist_fidelity_prompt()` in `prompts.py`
- **Output**: A single fidelity report (`tasklist-fidelity.md`) with YAML frontmatter

### Skill Path (inference-based, in-session)
- **Entry**: `/sc:tasklist` skill invocation
- **Scope**: Full generation (roadmap parsing, task decomposition, multi-file output) PLUS post-generation validation
- **Protocol**: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (v4.0, ~800 lines)
- **Prompt reference**: The skill's scope note (Section 3.x) explicitly says it uses `build_tasklist_generate_prompt` from `tasklist/prompts.py`
- **Output**: Multi-file bundle (`tasklist-index.md` + N `phase-N-tasklist.md` files)

**Critical finding**: `build_tasklist_generate_prompt()` exists in `prompts.py` but is **never called by any CLI code**. Its docstring confirms: "There is no `tasklist generate` CLI subcommand -- generation is handled by the skill protocol." The function exists solely as a reference prompt builder for the inference-based skill.

---

## 2. CLI Validate Pipeline: Full Trace

### 2.1 Entry Point: `commands.py` validate command

```
superclaude tasklist validate <output_dir> [--roadmap-file] [--tasklist-dir] [--tdd-file] [--prd-file] [--model] [--max-turns] [--debug]
```

**Default resolution logic**:
- `roadmap_file` defaults to `{output_dir}/roadmap.md`
- `tasklist_dir` defaults to `{output_dir}/` (i.e., the output dir itself)

**Auto-wiring from `.roadmap-state.json`** (lines 113-159):
- Reads state file from `{output_dir}/.roadmap-state.json`
- Auto-wires `tdd_file` from state if not passed via CLI flag
- Special case: when `input_type == "tdd"` in state, the `spec_file` field IS the TDD (since `--tdd-file` is supplementary, not primary)
- Auto-wires `prd_file` from state if not passed via CLI flag
- Emits stderr warnings if auto-wired paths no longer exist on disk

### 2.2 Config Construction: `models.py`

`TasklistValidateConfig` extends `PipelineConfig` with:
- `output_dir: Path`
- `roadmap_file: Path`
- `tasklist_dir: Path`
- `tdd_file: Path | None`
- `prd_file: Path | None`

### 2.3 Executor: `executor.py`

`execute_tasklist_validate(config)` orchestrates:

1. **`_build_steps(config)`** -- Creates a single-step pipeline:
   - Step ID: `"tasklist-fidelity"`
   - Inputs: `[roadmap_file] + sorted(tasklist_dir/*.md) + [tdd_file?] + [prd_file?]`
   - Prompt: `build_tasklist_fidelity_prompt(...)` 
   - Gate: `TASKLIST_FIDELITY_GATE`
   - Timeout: 600 seconds
   - Retry limit: 1
   - Output file: `{output_dir}/tasklist-fidelity.md`

2. **`execute_pipeline(steps, config, run_step=tasklist_run_step)`** -- Delegates to the shared pipeline executor

3. **`_has_high_severity(report_path)`** -- Post-pipeline check: parses YAML frontmatter for `high_severity_count` field, returns True if > 0

4. **Exit code**: 0 if no HIGH severity deviations, 1 otherwise

### 2.4 Step Runner: `tasklist_run_step()`

Mirrors the roadmap's `validate_run_step`:

1. **Input embedding**: Always inline (comment: "--file is broken, cloud download mechanism"). Reads all input files and concatenates as fenced code blocks via `_embed_inputs()`.
2. **Prompt composition**: `step.prompt + "\n\n" + embedded_inputs`
3. **Size warning**: Logs warning if composed prompt exceeds 100KB (`_EMBED_SIZE_LIMIT`), but embeds anyway since there's no fallback.
4. **Subprocess launch**: `ClaudeProcess(prompt=..., output_file=..., output_format="text", ...)`
5. **Polling loop**: 1-second polls with cancel check
6. **Post-processing**: `_sanitize_output()` strips conversational preamble before YAML frontmatter (regex search for `^---` on its own line)

### 2.5 Gate: `gates.py`

`TASKLIST_FIDELITY_GATE` = `GateCriteria` with:
- **Required frontmatter fields**: `high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready`
- **min_lines**: 20
- **enforcement_tier**: `"STRICT"`
- **Semantic checks** (reused from `roadmap/gates.py`):
  1. `_high_severity_count_zero` -- `high_severity_count` must be 0
  2. `_tasklist_ready_consistent` -- `tasklist_ready` must be consistent with severity counts and `validation_complete`

### 2.6 Prompt: `build_tasklist_fidelity_prompt()`

A long string prompt (~4KB) that instructs Claude to:
- Compare roadmap vs tasklist across 5 dimensions: deliverable coverage, signature preservation, traceability ID validity, dependency chain correctness, acceptance criteria completeness
- Apply severity classifications (HIGH/MEDIUM/LOW) with explicit definitions and examples
- Output YAML frontmatter with structured counts
- Produce a numbered deviation report (DEV-NNN format)
- **Validation layering guard**: Explicitly scoped to roadmap-to-tasklist only; does NOT check spec-to-tasklist

Optional TDD supplementary validation (5 additional checks when `tdd_file` is provided):
- Test cases (S15), rollback procedures (S19), component inventory (S10), data models (S7), API endpoints (S8)

Optional PRD supplementary validation (4 additional checks when `prd_file` is provided):
- User persona coverage (S7), success metrics (S19), acceptance scenarios (S12/S22), priority ordering (S5)

Appends `_OUTPUT_FORMAT_BLOCK` (shared from `roadmap/prompts.py`) which enforces YAML-frontmatter-first output.

---

## 3. Skill Protocol: Generation Algorithm

The `/sc:tasklist` skill (SKILL.md v4.0) defines a 10-stage deterministic generation algorithm. This is purely inference-based -- the skill protocol is a prompt that Claude follows during an interactive session. There is no programmatic executor backing it.

### 3.1 R-Item Parsing (Section 4.1)

R-items are parsed from the roadmap by the LLM following these rules:

1. **Split** the roadmap into items by scanning top-to-bottom
2. **New item triggers**: Any markdown heading (`#`, `##`, `###`), bullet point (`-`, `*`, `+`), or numbered list item
3. **Paragraph splitting**: Multi-requirement paragraphs split at semicolons/sentences only when each clause is independently actionable
4. **ID assignment**: Sequential appearance order: `R-001`, `R-002`, `R-003`, ...

**This is entirely LLM-driven.** There is no programmatic parser for R-items. The skill protocol describes the algorithm, and the LLM executes it during inference. This means:
- Non-deterministic in practice (different model runs may parse differently)
- No validation that R-IDs are consistent across generation and validation runs
- The fidelity validator checks R-NNN references in the tasklist against the roadmap, but doesn't re-parse R-items itself

### 3.2 Phase Bucketing (Section 4.2)

1. If roadmap has explicit phases/versions/milestones: use those as buckets
2. Otherwise: use `##` level headings
3. Fallback: create 3 default phases (Foundations, Build, Stabilize)

Phase numbers are always renumbered sequentially (no gaps).

### 3.3 Task Decomposition (Section 4.4)

- Default: 1 task per roadmap item
- Split into multiple tasks ONLY when the item contains 2+ independently deliverable outputs (specific combinations listed)

### 3.4 Task Count Determination

Task count is a function of:
1. Number of R-items parsed (1:1 default)
2. Split rules (2+ tasks for items with multiple deliverable types)
3. Supplementary TDD tasks (appended from component inventory, migration, testing, observability, release criteria)
4. Supplementary PRD tasks (user stories, success metrics, acceptance scenarios)
5. Clarification tasks (inserted when info is missing or confidence < 0.70)

**No programmatic bounds on task count** beyond the structural quality gate: "every phase has >= 1 and <= 25 tasks" (check #13).

### 3.5 Multi-File Output

The skill produces N+1 files:
- `tasklist-index.md` -- All cross-phase metadata, registries, traceability matrix, templates
- `phase-1-tasklist.md` through `phase-N-tasklist.md` -- Self-contained phase execution units

**Sprint CLI compatibility**: Phase files must start with `# Phase N -- <Name>` (level 1 heading, em-dash separator). Index must contain literal filenames in the Phase Files table.

### 3.6 Post-Generation Validation (Stages 7-10)

The skill protocol defines mandatory post-generation validation:
- Stage 7: Validate generated output against source roadmap
- Stage 8: Produce validation report
- Stage 9: Patch drift (fix any deviations found)
- Stage 10: Spot-check verification

This is inference-only validation -- not the CLI `tasklist validate` command.

---

## 4. Prompt Builders: Generation vs Validation

### `build_tasklist_generate_prompt()` (unused by CLI)

- Role: "You are a tasklist generator"
- Input: roadmap file (+ optional TDD/PRD)
- Instruction: Decompose roadmap into structured tasks with IDs, acceptance criteria, effort, dependencies, verification
- **Missing**: The entire deterministic algorithm from the SKILL.md (R-item parsing, phase bucketing, tier classification, deliverable registry, traceability matrix). The prompt is a lightweight stub compared to the 800-line skill protocol.

### `build_tasklist_fidelity_prompt()` (used by CLI validate)

- Role: "You are a tasklist fidelity analyst"
- Input: roadmap + tasklist files (+ optional TDD/PRD)
- Instruction: Compare roadmap vs tasklist, report deviations with severity
- Explicit layering guard: roadmap-to-tasklist ONLY
- Output format: YAML frontmatter + deviation report

---

## 5. Granularity Loss Points

### 5.1 Input Embedding Bottleneck

`_embed_inputs()` reads ALL tasklist files and the roadmap, concatenating them as fenced code blocks. For a large roadmap + multi-phase tasklist, this can easily exceed 100KB. The system logs a warning but has no mitigation:

```python
if len(composed.encode("utf-8")) > _EMBED_SIZE_LIMIT:  # 100KB
    _log.warning("tasklist executor: composed prompt exceeds %d bytes; embedding inline anyway")
```

This is the same structural failure as the roadmap pipeline -- one-shot prompting with all inputs inline.

### 5.2 No Extraction Step

Unlike the roadmap pipeline (which has an extraction step to distill the spec into structured data before generation), the tasklist pipeline has **no intermediate extraction**. Both generation and validation work directly from raw input files.

For validation this means:
- The LLM must simultaneously parse the roadmap structure, parse the tasklist structure, and compare them
- No structured intermediate representation enables systematic comparison
- Comparison quality depends entirely on the LLM's ability to track R-IDs and D-IDs across documents

### 5.3 R-Item Identity Gap

R-items (`R-001`, `R-002`, etc.) are assigned by the generation-time LLM. The validation-time LLM independently reads the roadmap and checks that R-IDs in the tasklist reference real roadmap items. But:
- The validator doesn't have the original R-item registry from generation
- If the roadmap doesn't contain explicit R-IDs (and most don't -- the generator assigns them), the validator must re-derive them
- No guarantee that the validator's R-item parsing matches the generator's

### 5.4 One-Shot Output Limits

The generation skill produces N+1 files in a single session. For large roadmaps (10+ phases, 100+ tasks), this pushes against context window limits. The protocol has no chunking strategy -- it relies on the LLM's ability to generate all files atomically.

---

## 6. Relationship: CLI Pipeline vs Skill Protocol

| Dimension | CLI (`superclaude tasklist validate`) | Skill (`/sc:tasklist`) |
|-----------|---------------------------------------|------------------------|
| **Execution model** | Subprocess (`claude -p`) | Interactive session |
| **Function** | Validation only | Generation + validation |
| **R-item parsing** | None (expects existing tasklist) | LLM-driven per algorithm |
| **Task decomposition** | None | LLM-driven per algorithm |
| **Prompt source** | `build_tasklist_fidelity_prompt()` | SKILL.md (800 lines) + `build_tasklist_generate_prompt()` reference |
| **Output** | Single fidelity report | Multi-file tasklist bundle |
| **Gate enforcement** | Programmatic (YAML frontmatter + semantic checks) | Inference-only (self-check) |
| **TDD/PRD support** | Supplementary validation checks | Full enrichment + task generation |
| **Sprint compatibility** | N/A (produces a report, not a tasklist) | Phase files compatible with `superclaude sprint run` |

**Key disconnect**: The CLI can validate a tasklist but cannot generate one. Generation requires the skill protocol, which runs in an interactive Claude session. There is no programmatic path from "I have a roadmap" to "I have a tasklist" without invoking the inference-based skill.

---

## 7. Gaps and Questions

1. **No CLI generate subcommand**: Why does `build_tasklist_generate_prompt()` exist if it's never called by any CLI code? Is there a planned `tasklist generate` subcommand?

2. **R-item identity problem**: The generation skill assigns R-IDs, but the CLI validator has no access to the generation-time R-item registry. How does validation reliably check traceability if R-IDs are derived independently?

3. **No extraction step for validation**: The roadmap pipeline has extraction (spec -> structured data) before generation. The tasklist pipeline has no analog. Should a roadmap-to-structured-items extraction precede both generation and validation?

4. **Prompt asymmetry**: `build_tasklist_generate_prompt()` is a ~40 line lightweight stub. The actual generation algorithm is 800+ lines in SKILL.md. If a CLI generate subcommand were added, the prompt builder would need to encode the entire algorithm -- or a fundamentally different approach would be needed.

5. **One-shot output limits**: Large roadmaps with 10+ phases and 100+ tasks will produce outputs that exceed typical context windows. The skill protocol has no chunking or phase-by-phase generation strategy.

6. **Validation layering ambiguity**: The fidelity prompt says "Do NOT compare the tasklist against the original specification." But with `--tdd-file` and `--prd-file`, it adds supplementary checks against those documents. Is this a contradiction of the layering guard?

7. **100KB embedding limit**: The warning is logged but embedding proceeds. What actually happens when the composed prompt exceeds the model's context limit?

---

## 8. Stale Documentation Found

- `build_tasklist_generate_prompt()` docstring says "used by the `/sc:tasklist` skill protocol for inference-based generation workflows." However, the skill protocol is a self-contained 800-line prompt -- it doesn't literally import or call this Python function. The relationship is conceptual, not programmatic.

- The SKILL.md Section 3.x scope note says the CLI `validate` uses `build_tasklist_fidelity_prompt` and the skill protocol uses `build_tasklist_generate_prompt`. This is directionally correct but creates a false impression that the prompt builder is actively consumed by the skill. In reality, the skill protocol IS the prompt -- the Python function is a much simpler reference version.

- `commands.py` docstring references "FR-016/FR-017" requirement IDs that don't appear anywhere in the codebase as formal requirements documents.

---

## 9. Summary

The tasklist pipeline has a fundamental architectural split: **validation is programmatic** (CLI subprocess with gates) but **generation is inference-only** (800-line skill protocol). There is no CLI path to generate a tasklist from a roadmap.

The core structural problems mirror the roadmap pipeline:
1. **One-shot embedding**: All inputs are concatenated and sent in a single prompt, hitting size limits
2. **No extraction intermediary**: No structured representation between raw inputs and the final comparison/generation
3. **R-item identity gap**: Generator and validator independently parse roadmap items with no shared registry
4. **Output size limits**: Large tasklist bundles push against context window constraints

The `build_tasklist_generate_prompt()` function is effectively dead code from the CLI's perspective -- it exists as a lightweight reference but is never invoked. The actual generation algorithm lives entirely in the skill protocol SKILL.md, which is executed by the LLM during an interactive session, not by any programmatic executor.
