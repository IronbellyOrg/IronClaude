# 02 -- Tasklist Generation Prompt Analysis

**Status**: Complete
**Investigator**: Code Tracer
**Date**: 2026-04-02
**File**: `src/superclaude/cli/tasklist/prompts.py` (237 lines)
**Research Question**: How does `build_tasklist_generate_prompt` handle TDD/PRD supplementary content, and does any language suppress task creation or encourage consolidation?

---

## 1. Function Signature and Parameters

**Lines 151-155**: `build_tasklist_generate_prompt(roadmap_file, tdd_file=None, prd_file=None)`

Three parameters, two optional. The function returns a string prompt. The `roadmap_file` parameter is typed `Path` but is not interpolated into the prompt text itself -- it is a positional marker for the caller to know which file to attach. The TDD and PRD paths control conditional block inclusion.

**Important docstring note (lines 158-163)**: The function is used by the `/sc:tasklist` skill protocol for inference-based generation workflows. It is NOT called by the CLI `tasklist validate` executor. There is no `tasklist generate` CLI subcommand.

## 2. Base Prompt (Lines 171-184) -- Roadmap-Only Mode

The base prompt (no TDD, no PRD) instructs:

```
"You are a tasklist generator.\n\n"
"Read the provided roadmap file and decompose it into a structured "
"tasklist with individual, actionable tasks. Each roadmap item should "
"produce one or more tasks with:\n"
"- A clear task title\n"
"- Deliverable IDs traced to the roadmap (R-NNN, D-NNNN)\n"
"- Acceptance criteria\n"
"- Effort estimate\n"
"- Dependencies on other tasks\n"
"- Verification method\n\n"
"Organize tasks by roadmap phase. Preserve all roadmap item IDs, "
"deliverable IDs, and dependency chains exactly as specified."
```

**Key language**: "Each roadmap item should produce **one or more** tasks" -- this is expansive, encouraging at least one task per roadmap item and allowing multiple.

No consolidation language exists in the base prompt.

## 3. TDD Enrichment Block (Lines 187-202) -- Conditional on `tdd_file is not None`

Appended when a TDD file is provided. Section header: `## Supplementary TDD Enrichment (for task generation)`

Instructions add five enrichment dimensions:
1. **Line 193**: Test cases from S15 -- "each test case should map to a validation task"
2. **Line 195**: API endpoint schemas from S8 -- "each endpoint should have implementation tasks"
3. **Line 197**: Component specs from S10 -- "each component should have tasks"
4. **Line 199**: Migration rollback from S19 -- "each rollback procedure should be a contingency task"
5. **Line 201**: Data model fields from S7 -- "each entity should have schema implementation tasks"

**Analysis**: The TDD block is purely **additive**. Every instruction says "each X should have/map to a task." This should INCREASE task count, not decrease it. The language is "enrich task decomposition" -- meaning more detail, more tasks.

**No suppression language found in the TDD block.**

## 4. PRD Enrichment Block (Lines 204-224) -- Conditional on `prd_file is not None`

Appended when a PRD file is provided. Section header: `## Supplementary PRD Enrichment (for task generation)`

Instructions add five enrichment dimensions:
1. **Line 210**: User persona context from S7 -- tasks "should reference which persona"
2. **Line 212**: Acceptance scenarios from S12/S22 -- "each user story acceptance criterion should map to a verification task"
3. **Line 214**: Success metrics from S19 -- "tasks should include metric instrumentation subtasks"
4. **Line 216**: Stakeholder priorities from S5 -- "task priority should reflect business value ordering"
5. **Lines 218-219**: Scope boundaries from S12 -- "tasks must not exceed defined scope; generate explicit 'out of scope' markers"

**CRITICAL FINDING -- Lines 221-223**:
```
"PRD context informs task descriptions and priorities but does NOT generate "
"standalone implementation tasks. Engineering tasks come from the roadmap; "
"PRD enriches them."
```

This is the **only suppression language** in the entire file. It explicitly tells the LLM:
- PRD does NOT generate standalone implementation tasks
- Engineering tasks come from the roadmap only
- PRD's role is enrichment, not creation

**This is a task-creation suppressor.** While the base prompt says "each roadmap item should produce one or more tasks" and the TDD block says "each X should map to a task," the PRD block says the opposite: do NOT create new tasks from PRD content, only annotate existing ones.

## 5. TDD + PRD Interaction Block (Lines 227-235) -- Conditional on BOTH being present

Appended only when both `tdd_file` and `prd_file` are provided:

```
"When both TDD and PRD are available, TDD provides structural engineering "
"detail and PRD provides product context. TDD-derived task enrichment "
"(test cases, schemas, components) takes precedence for implementation "
"specifics. PRD-derived enrichment (personas, metrics, priorities) shapes "
"task descriptions, acceptance criteria, and priority ordering."
```

**Analysis**: This block establishes a hierarchy:
- TDD = structural detail (tasks, schemas, components) -- implementation specifics
- PRD = context overlay (personas, metrics, priorities) -- descriptive enrichment

This reinforces the PRD suppression: PRD "shapes" existing tasks rather than creating new ones.

## 6. Consolidation Language Search

Searched the entire file for: `consolidat`, `merge`, `combine`, `group`, `high-level`, `standalone`, `does not generate`.

**Results**:
- **Line 221-222**: `"does NOT generate standalone implementation tasks"` -- FOUND in PRD block
- **Line 226**: `"Combined interaction note"` -- comment only, not prompt text
- No instances of: consolidate, merge, combine, group, high-level

**Conclusion**: There is no explicit "consolidate tasks" or "merge tasks" instruction. The suppression mechanism is more subtle -- it constrains the PRD's role to enrichment-only, preventing it from spawning new tasks.

## 7. Prompt Comparison: With vs Without TDD+PRD

### Roadmap-only prompt (no supplementary files)
- Base prompt (lines 171-184)
- `_OUTPUT_FORMAT_BLOCK` (YAML frontmatter formatting)
- Total instruction: ~170 words of generation guidance
- Task creation stance: "Each roadmap item should produce one or more tasks"

### Roadmap + TDD prompt
- Base prompt + TDD enrichment block (lines 187-202)
- Adds 5 enrichment dimensions, each saying "each X should map to a task"
- Task creation stance: **Expansive** -- more tasks expected from TDD detail

### Roadmap + PRD prompt
- Base prompt + PRD enrichment block (lines 204-224)
- Adds 5 enrichment dimensions, but final sentence **suppresses** new task creation
- Task creation stance: **Constrained** -- PRD enriches but does not create

### Roadmap + TDD + PRD prompt (the 49% fewer tasks case)
- Base prompt + TDD block + PRD block + Interaction block
- TDD says "create tasks for each X"
- PRD says "do NOT generate standalone tasks"
- Interaction block says TDD takes precedence for implementation, PRD shapes descriptions
- Task creation stance: **Conflicting signals** -- TDD is additive, PRD is suppressive

## 8. The _OUTPUT_FORMAT_BLOCK (imported from roadmap/prompts.py, line 62-79)

This is appended to all prompts. It is a formatting directive only:

```
CRITICAL: Your response MUST begin with YAML frontmatter (--- delimited block).
Do NOT include any text, preamble, or commentary before the opening ---.
```

No task-count-affecting language.

---

## Gaps and Questions

1. **Why does TDD+PRD produce FEWER tasks when TDD alone should be additive?** The PRD suppression line (221-223) is the most likely cause, but it only says "PRD does not generate standalone tasks." It does not say "reduce the total number of tasks." The LLM may be over-interpreting this as a consolidation instruction.

2. **The interaction block may amplify suppression.** When the LLM reads "PRD-derived enrichment shapes task descriptions, acceptance criteria, and priority ordering" (line 233-234), it may interpret this as: "fold PRD requirements into existing tasks rather than creating new ones." Combined with the PRD suppression line, the net effect could be that the LLM consolidates what would have been separate tasks into enriched versions of fewer tasks.

3. **Missing: No explicit task-count guidance.** Neither the base prompt nor any supplementary block says "aim for N tasks per roadmap item" or "do not reduce task count when supplementary documents are provided." This is a gap -- the LLM has no anchor for expected task granularity.

4. **Missing: No anti-consolidation guard.** There is no instruction like "supplementary documents should only ADD tasks or ADD detail to existing tasks, never reduce the number of tasks." This would be a direct fix.

5. **The scope boundary instruction (lines 218-219) may also suppress.** "Tasks must not exceed defined scope; generate explicit 'out of scope' markers where roadmap milestones approach scope edges." If the PRD scope is narrower than the roadmap, the LLM might drop roadmap tasks that fall outside PRD scope boundaries.

6. **Who calls this function?** The docstring says the `/sc:tasklist` skill protocol calls it. The CLI `tasklist validate` does NOT call it. The actual invocation path should be traced to understand how `tdd_file` and `prd_file` get populated.

7. **Is the 49% reduction measured on the same roadmap?** If the TDD+PRD pipeline also produces a different (merged) roadmap, the input roadmap to this prompt may itself be different, which would confound the analysis.

---

## Summary

**Root cause candidate identified**: Lines 221-223 of `src/superclaude/cli/tasklist/prompts.py` contain the only task-suppression language in the generation prompt:

> "PRD context informs task descriptions and priorities but does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them."

This instruction, combined with the TDD+PRD interaction block (lines 229-234) that frames PRD as a "shaping" influence rather than a generative one, likely causes the LLM to consolidate PRD-relevant requirements into enriched annotations on existing tasks rather than creating new tasks. The net effect: 4.1x more input produces fewer, more densely annotated tasks instead of more tasks.

**The TDD block is not the problem** -- it is purely additive ("each X should map to a task"). The PRD block's suppression language is the primary suspect, and the interaction block's hierarchy framing amplifies the effect.

**Recommended investigation**: Test the prompt with the PRD suppression line removed (lines 221-223) and compare task counts. If task count increases, the suppression language is confirmed as causal.
