# Research: Roadmap CLI Integration Points

**Investigation type:** Code Tracer
**Scope:** src/superclaude/cli/roadmap/commands.py, models.py, executor.py
**Status:** Complete
**Date:** 2026-03-27

---

## 1. Models Layer: `src/superclaude/cli/roadmap/models.py`

### RoadmapConfig dataclass (line 95-115)

`RoadmapConfig` extends `PipelineConfig` (from `src/superclaude/cli/pipeline/models.py`).

Existing supplementary fields relevant to PRD integration:

| Field | Type | Line | Purpose |
|---|---|---|---|
| `spec_file` | `Path` | 102 | Primary input file (spec or TDD) |
| `retrospective_file` | `Path \| None` | 111 | Optional retro from prior cycle |
| `input_type` | `Literal["auto","tdd","spec"]` | 114 | Controls auto-detection routing |
| `tdd_file` | `Path \| None` | 115 | Optional TDD for downstream enrichment |

**Key finding: `tdd_file` exists on `RoadmapConfig` at line 115 but is NEVER REFERENCED in the executor or commands.** [CODE-VERIFIED] It is dead code in the roadmap pipeline. The `tdd_file` field is only actively wired in the *tasklist* pipeline (`src/superclaude/cli/tasklist/`).

**Action for PRD:** Add `prd_file: Path | None = None` after `tdd_file` at line 115. Follow the same pattern.

### ValidateConfig dataclass (line 119-133)

Does NOT have `tdd_file` or any supplementary input fields. Only has `output_dir` and `agents`. If PRD needs to flow into the validation subcommand as well, a field would need to be added here too.

### Key Takeaways -- Models

1. Adding `prd_file: Path | None = None` to `RoadmapConfig` is trivial -- append after line 115.
2. `tdd_file` on `RoadmapConfig` is dead code (no CLI flag, no executor reference). The PRD integration should learn from this: wire it end-to-end or don't add the field.
3. `ValidateConfig` may also need `prd_file` if the validate subcommand should accept it.

---

## 2. Commands Layer: `src/superclaude/cli/roadmap/commands.py`

### `run` command (lines 32-218)

The `run` command is a Click command under `roadmap_group`. It accepts the primary input as a positional argument `spec_file` (line 33).

Existing CLI flags for supplementary inputs:

| Flag | Parameter | Type | Line | Notes |
|---|---|---|---|---|
| `--retrospective` | `retrospective` | `click.Path(exists=False, path_type=Path)` | 96-104 | Uses `exists=False` (missing file is not an error) |
| `--input-type` | `input_type` | `click.Choice(["auto","tdd","spec"])` | 106-110 | Controls detection routing |

**Key finding: There is NO `--tdd-file` flag on the `run` command.** [CODE-VERIFIED] The `tdd_file` field on `RoadmapConfig` is never populated by the CLI. This confirms `tdd_file` is dead code in the roadmap pipeline.

The `config_kwargs` dict (lines 170-181) assembles all config fields. Adding `prd_file` here follows the `retrospective_file` pattern.

**Pattern for `--prd-file`:**

```python
# After the --input-type option (around line 110), add:
@click.option(
    "--prd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to a PRD file for supplementary context enrichment.",
)
```

Then in the `run` function signature (line 112-127), add `prd_file: Path | None` parameter.

In `config_kwargs` (line 170-181), add:
```python
"prd_file": prd_file.resolve() if prd_file is not None else None,
```

### `validate` command (lines 247-322)

Does NOT currently accept any supplementary input files. If PRD should also feed into validation, add `--prd-file` here too, following the tasklist validate pattern (which does have `--tdd-file` at line 62-66 of tasklist/commands.py).

### Key Takeaways -- Commands

1. Add `--prd-file` Click option with `type=click.Path(exists=True, path_type=Path)` to the `run` command.
2. Use `exists=True` (unlike `--retrospective` which uses `exists=False`). PRD should exist if specified.
3. Wire into `config_kwargs` with `.resolve()`.
4. No changes to `--input-type` choices needed -- PRD is supplementary, not a mode.
5. Consider adding to `validate` command as well.

---

## 3. Executor Layer: `src/superclaude/cli/roadmap/executor.py`

### `detect_input_type()` (lines 59-117)

Auto-detects whether input is TDD or spec using weighted scoring (numbered headings, exclusive frontmatter fields, section names). Returns `"tdd"` or `"spec"`.

**PRD does NOT affect this function.** [CODE-VERIFIED] PRD is supplementary input, not a primary input mode. `detect_input_type()` should remain unchanged.

### `_build_steps()` (lines 843-1012)

This is the critical function. It constructs the 9-step pipeline as a list of `Step` objects. Each `Step` has:
- `prompt`: built by a prompt builder function
- `inputs`: list of `Path` objects the subprocess can read
- `output_file`: where the step writes its output

**Current supplementary input handling (retrospective):**

Lines 872-880: Retrospective content is loaded as a string and passed into `build_extract_prompt()` / `build_extract_prompt_tdd()` as `retrospective_content` parameter. It is NOT added to the `inputs` list -- it's embedded directly into the prompt text.

**TDD handling in `_build_steps()`:**

Lines 884-903: `effective_input_type` controls which extract prompt builder is called (`build_extract_prompt` vs `build_extract_prompt_tdd`). The `config.tdd_file` field is NEVER read in `_build_steps()`. [CODE-VERIFIED]

**Steps and their inputs -- where PRD could be injected:**

| Step | ID | Prompt Builder | `inputs` list | PRD relevance |
|---|---|---|---|---|
| 1 | `extract` | `build_extract_prompt` / `build_extract_prompt_tdd` | `[config.spec_file]` | **HIGH** -- PRD context enriches extraction |
| 2a/2b | `generate-{agent}` | `build_generate_prompt` | `[extraction]` | LOW -- uses extraction output, not raw inputs |
| 3 | `diff` | `build_diff_prompt` | `[roadmap_a, roadmap_b]` | NONE |
| 4 | `debate` | `build_debate_prompt` | `[diff_file, roadmap_a, roadmap_b]` | NONE |
| 5 | `score` | `build_score_prompt` | `[debate_file, roadmap_a, roadmap_b]` | NONE |
| 6 | `merge` | `build_merge_prompt` | `[score_file, roadmap_a, roadmap_b, debate_file]` | NONE |
| 7 | `anti-instinct` | (non-LLM) | `[config.spec_file, merge_file]` | POSSIBLE -- could cross-reference PRD |
| 8 | `test-strategy` | `build_test_strategy_prompt` | `[merge_file, extraction]` | LOW |
| 8b | `spec-fidelity` | `build_spec_fidelity_prompt` | `[config.spec_file, merge_file]` | **MEDIUM** -- PRD could augment fidelity checks |
| 9 | `wiring-verification` | `build_wiring_verification_prompt` | `[merge_file, spec_fidelity_file]` | NONE |

**Recommended injection points for `prd_file`:**

1. **Step 1 (extract)** -- Add `prd_file` to both `inputs` list and prompt builder parameter. This is the primary injection point.
2. **Step 8b (spec-fidelity)** -- Optionally add PRD as supplementary context for fidelity checks.

For the extract step (lines 885-903), the change would be:
```python
Step(
    id="extract",
    prompt=(
        build_extract_prompt_tdd(
            config.spec_file,
            retrospective_content=retrospective_content,
            prd_file=config.prd_file,  # NEW
        )
        if effective_input_type == "tdd"
        else build_extract_prompt(
            config.spec_file,
            retrospective_content=retrospective_content,
            prd_file=config.prd_file,  # NEW
        )
    ),
    output_file=extraction,
    gate=EXTRACT_GATE,
    timeout_seconds=300,
    inputs=[config.spec_file] + ([config.prd_file] if config.prd_file else []),  # NEW
    retry_limit=1,
),
```

### `execute_roadmap()` (lines 1728-1807+)

Top-level orchestrator. Calls `_build_steps(config)` at line 1778. No changes needed here -- it passes the full config through.

### Key Takeaways -- Executor

1. `detect_input_type()` needs NO changes. PRD is supplementary.
2. `_build_steps()` is the primary wiring point. PRD should be added to extract step's `inputs` and prompt builder.
3. The retrospective pattern (load content, pass as string to prompt builder) is a viable pattern for PRD.
4. Alternatively, PRD can be added to `inputs` (file path list) so the subprocess can read it directly -- this is how TDD works in the tasklist pipeline.
5. `config.tdd_file` is dead code in the roadmap executor. `config.prd_file` should NOT replicate this mistake.

---

## 4. Prompts Layer: `src/superclaude/cli/roadmap/prompts.py`

### Prompt builder signatures

| Function | Line | Current supplementary params |
|---|---|---|
| `build_extract_prompt` | 82 | `retrospective_content: str \| None = None` |
| `build_extract_prompt_tdd` | 161 | `retrospective_content: str \| None = None` |
| `build_generate_prompt` | 288 | None |
| `build_diff_prompt` | 338 | None |
| `build_debate_prompt` | 363 | None |
| `build_score_prompt` | 390 | None |
| `build_merge_prompt` | 416 | None |
| `build_spec_fidelity_prompt` | 448 | None |
| `build_wiring_verification_prompt` | 528 | None |
| `build_test_strategy_prompt` | 586 | None |

**PRD integration requires adding `prd_file: Path | None = None` to:**
1. `build_extract_prompt()` (line 82) -- mandatory
2. `build_extract_prompt_tdd()` (line 161) -- mandatory
3. `build_spec_fidelity_prompt()` (line 448) -- optional, for enriched fidelity

The implementation follows the `retrospective_content` pattern: conditionally append a PRD context section to the prompt string when `prd_file is not None`.

### Reference: Tasklist TDD prompt integration pattern

In `src/superclaude/cli/tasklist/prompts.py` (lines 111-123), the TDD integration appends a supplementary section:

```python
if tdd_file is not None:
    base += (
        "\n\n## Supplementary TDD Validation (when TDD file is provided)\n\n"
        "A Technical Design Document (TDD) is included in the inputs alongside ..."
    )
```

PRD should follow this exact pattern.

### Key Takeaways -- Prompts

1. Add `prd_file` parameter to `build_extract_prompt` and `build_extract_prompt_tdd`.
2. Conditionally append a `## Supplementary PRD Context` section to the prompt.
3. The prompt should instruct the LLM to use PRD content for requirement enrichment, user story context, and acceptance criteria verification.
4. Optionally extend `build_spec_fidelity_prompt` for PRD-aware fidelity checks.

---

## 5. TDD Integration as Reference Pattern (Tasklist Pipeline)

The tasklist pipeline has a complete, working `tdd_file` integration. Here is the full flow:

### Flow: CLI flag -> model -> executor -> prompt builder

1. **CLI** (`tasklist/commands.py:62-66`): `--tdd-file` option with `type=click.Path(exists=True, path_type=Path)` [CODE-VERIFIED]
2. **Config** (`tasklist/commands.py:114`): `tdd_file=tdd_file.resolve() if tdd_file is not None else None` [CODE-VERIFIED]
3. **Model** (`tasklist/models.py:25`): `tdd_file: Path | None = None` [CODE-VERIFIED]
4. **Executor** (`tasklist/executor.py:193-194`): `if config.tdd_file is not None: all_inputs.append(config.tdd_file)` [CODE-VERIFIED]
5. **Executor** (`tasklist/executor.py:202`): `tdd_file=config.tdd_file` passed to prompt builder [CODE-VERIFIED]
6. **Prompts** (`tasklist/prompts.py:20`): `tdd_file: Path | None = None` parameter on `build_tasklist_fidelity_prompt` [CODE-VERIFIED]
7. **Prompts** (`tasklist/prompts.py:111-123`): Conditional append of supplementary TDD validation section [CODE-VERIFIED]

This is the exact pattern to replicate for `prd_file` in the roadmap pipeline.

---

## Gaps and Questions

1. **Dead `tdd_file` on `RoadmapConfig`**: Should this be wired up as part of the PRD work, or cleaned up separately? It exists at line 115 of models.py but has no CLI flag and no executor reference. This is tech debt.

2. **PRD scope in downstream steps**: Should PRD context flow only into extraction (step 1), or also into spec-fidelity (step 8b)? Decision needed.

3. **Content embedding vs file reference**: The retrospective pattern embeds content as a string into the prompt. The tasklist TDD pattern adds the file path to `inputs` so the subprocess reads it. Which pattern should PRD use? Recommendation: use `inputs` (file path) since PRDs can be large.

4. **`validate` subcommand**: Should `--prd-file` also be added to `superclaude roadmap validate`? The validate command currently has no supplementary input mechanism.

5. **State persistence**: `_save_state()` and `_restore_from_state()` handle `--resume`. If `prd_file` needs to persist across resume cycles, the state serialization would need updating. (Low priority -- retrospective_file is also not persisted in state.)

6. **Anti-instinct step**: The non-LLM anti-instinct audit (step 7) takes `[config.spec_file, merge_file]` as inputs. If PRD cross-referencing is desired, it would need to be added here too.

---

## Stale Documentation Found

1. **`RoadmapConfig` docstring** (models.py line 98-99): States "Extends PipelineConfig with roadmap-specific fields: spec_file, agents, depth, output_dir, retrospective_file" but does NOT mention `convergence_enabled`, `allow_regeneration`, `input_type`, or `tdd_file` which were added later. [CODE-CONTRADICTED]

2. **Step numbering in `_build_steps()`** (executor.py): Comment on line 987 says "Step 8" for spec-fidelity but it's actually the 9th step entry (after anti-instinct at step 7, test-strategy at step 8). The wiring-verification comment says "Step 9" at line 997 making it the 10th entry. The function docstring says "9-step pipeline" but there are actually 10 step entries. [CODE-CONTRADICTED]

---

## Summary

### Files that need changes for `--prd-file` integration:

| File | Change | Complexity |
|---|---|---|
| `src/superclaude/cli/roadmap/models.py` | Add `prd_file: Path \| None = None` to `RoadmapConfig` | Trivial |
| `src/superclaude/cli/roadmap/commands.py` | Add `--prd-file` Click option + wire into `config_kwargs` | Low |
| `src/superclaude/cli/roadmap/executor.py` | Add `config.prd_file` to extract step `inputs` + pass to prompt builder | Low |
| `src/superclaude/cli/roadmap/prompts.py` | Add `prd_file` param to `build_extract_prompt` + `build_extract_prompt_tdd`; append conditional PRD section | Medium |

### What does NOT change:

- `detect_input_type()` -- PRD is supplementary, not a mode
- `--input-type` choices -- no new mode needed
- Steps 2-6 (generate, diff, debate, score, merge) -- PRD context is absorbed at extraction
- Gate definitions in `gates.py` -- no new gates needed

### Recommended implementation order:

1. `models.py` -- add field
2. `commands.py` -- add CLI flag and wiring
3. `prompts.py` -- add parameter and conditional prompt section
4. `executor.py` -- wire `config.prd_file` into extract step inputs and prompt builder call
5. Tests -- add test cases for PRD flag parsing and prompt inclusion

