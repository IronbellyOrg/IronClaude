# 05 -- Roadmap Prompt Analysis: Phase Count and TDD/PRD Influence

**Investigation**: Do roadmap generation prompts influence phase count differently when TDD+PRD supplementary input is present? Could the roadmap prompt cause fewer phases for richer input?

**Status**: Complete
**Type**: Code Tracer  
**File**: `src/superclaude/cli/roadmap/prompts.py` (920 lines)  
**Secondary**: `src/superclaude/cli/roadmap/commands.py` (360 lines), `src/superclaude/cli/tasklist/prompts.py`  
**Date**: 2026-04-03

---

## 1. Functions in prompts.py That Build Roadmap Generation Prompts

| Function | Lines | Purpose | Accepts TDD/PRD? |
|---|---|---|---|
| `build_extract_prompt` | 82-205 | Extraction from spec input | Yes (tdd_file, prd_file) |
| `build_extract_prompt_tdd` | 208-377 | Extraction when input IS a TDD | Yes (tdd_file for cross-ref, prd_file) |
| `build_generate_prompt` | 380-483 | Roadmap generation from extraction | Yes (tdd_file, prd_file) |
| `build_diff_prompt` | 486-508 | Compare two roadmap variants | No |
| `build_debate_prompt` | 511-535 | Adversarial debate between variants | No |
| `build_score_prompt` | 538-593 | Score and select base variant | Yes (tdd_file, prd_file) |
| `build_merge_prompt` | 596-658 | Merge variants into final roadmap | Yes (tdd_file, prd_file) |
| `build_spec_fidelity_prompt` | 661-769 | Fidelity check roadmap vs. spec | Yes (tdd_file, prd_file) |
| `build_wiring_verification_prompt` | 772-827 | Static wiring analysis | No |
| `build_test_strategy_prompt` | 830-919 | Test strategy generation | Yes (tdd_file, prd_file) |

**Key finding**: 7 of 10 prompt functions accept `tdd_file` and/or `prd_file` parameters. The TDD/PRD content is conditionally appended as supplementary blocks.

---

## 2. How TDD and PRD Supplementary Content Is Injected

### Pattern: Conditional String Append

All prompt functions follow the same structural pattern (using `build_generate_prompt` as canonical example):

1. A `base` string is built with the core prompt instructions (lines 392-434)
2. If `tdd_file is not None`, a supplementary TDD block is appended (lines 436-463)
3. If `prd_file is not None`, a supplementary PRD block is appended (lines 465-481)
4. Return `base + _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK` (line 483)

The supplementary blocks are **additive** -- they add new instructions and dimensions but do NOT modify the base prompt's structural instructions. There is no conditional logic that changes the base roadmap structure when supplementary files are present.

### Input Routing in commands.py

The `run` command (line 134) accepts:
- `input_files` (positional, 1-3 files) -- auto-detected as spec, TDD, or PRD
- `--tdd-file` (explicit flag, line 113)
- `--prd-file` (explicit flag, line 122)
- `--input-type` (auto/tdd/spec, line 107)

Routing is handled by `_route_input_files()` in executor.py (line 188), which resolves positional files + explicit flags into `spec_file`, `tdd_file`, `prd_file` slots. These are passed through `RoadmapConfig` into every prompt builder.

---

## 3. Phase Count Instructions in Roadmap Generation

### build_generate_prompt (lines 380-483) -- THE critical function

The base prompt instructs (lines 421-427):

```
"After the frontmatter, provide a complete roadmap including:\n"
"1. Executive summary\n"
"2. Phased implementation plan with milestones\n"
"3. Risk assessment and mitigation strategies\n"
"4. Resource requirements and dependencies\n"
"5. Success criteria and validation approach\n"
"6. Timeline estimates per phase\n\n"
```

**CRITICAL FINDING**: There is NO instruction specifying:
- How many phases to create
- A minimum or maximum phase count
- How to decompose requirements into phases
- How to group or consolidate work into phases
- Whether more input detail should produce more or fewer phases

The prompt says "Phased implementation plan with milestones" and "Timeline estimates per phase" but provides ZERO guidance on phase granularity or count.

### What the TDD supplementary block adds (lines 436-463)

When TDD is present, the prompt adds instructions to "Address each in the roadmap with specific implementation phases, tasks, and milestones" for 6 categories:
- Data Models and Interfaces
- API Specifications
- Component Inventory
- Testing Strategy
- Migration and Rollout Plan
- Operational Readiness

**This instructs the LLM to create phases covering these categories but does NOT say "create separate phases for each" vs. "integrate into existing phases."** The language "Include schema implementation tasks" / "Include per-endpoint implementation tasks" could be interpreted either way.

### What the PRD supplementary block adds (lines 465-481)

PRD instructions focus on prioritization and phasing ORDER, not phase COUNT:
- "prioritize phases that deliver measurable business value earliest" (line 471)
- "ensure the roadmap addresses highest-impact user needs first" (line 473)
- "include compliance validation milestones at appropriate phases" (lines 475-476)
- "flag any roadmap items that fall outside stated product scope" (lines 478-479)

**The PRD block actively uses language about phasing prioritization but does NOT instruct on phase count.**

---

## 4. Language Search: Consolidation and Grouping Instructions

Searched for: `consolidat`, `group`, `organiz`, `fewer`, `reduce`, `combine`, `merge` (in context of phases).

**Result**: NONE of these terms appear in `build_generate_prompt` in relation to phase structure.

The word "phase" appears in `prompts.py` in these contexts:
- Line 45: `_INTEGRATION_ENUMERATION_BLOCK` -- "Owning Phase" / "Which phase(s) consume"
- Line 423: "Phased implementation plan with milestones"
- Line 427: "Timeline estimates per phase"
- Line 448: "specific implementation phases, tasks, and milestones" (TDD block)
- Line 471: "prioritize phases" (PRD block)
- Line 476: "milestones at appropriate phases" (PRD block)

No language instructs the LLM to "organize into logical phases", "consolidate related work", or "group by milestone". Phase structure is entirely left to LLM inference.

---

## 5. build_merge_prompt (lines 596-658) -- Could Merge Reduce Phases?

The merge prompt instructs (lines 617-627):

```
"After the frontmatter, provide the complete final roadmap with:\n"
"1. Executive summary (synthesized from both variants)\n"
"2. Phased implementation plan incorporating debate-resolved improvements\n"
"3. Risk assessment merging insights from both perspectives\n"
"4. Resource requirements\n"
"5. Success criteria and validation approach\n"
"6. Timeline estimates\n\n"
"Use proper heading hierarchy (H2, H3, H4) with no gaps. "
"Ensure all internal cross-references resolve. "
"Do not duplicate heading text at H2 or H3 level."
```

**The merge prompt does NOT instruct on phase count either.** The "Do not duplicate heading text at H2 or H3 level" instruction (line 626) could cause consolidation of identically-named phases from two variants, but this is about deduplication, not structural reduction.

When TDD is present in merge (lines 629-641), the supplementary block says "Ensure the merged roadmap retains all TDD-derived implementation tasks" -- this is additive, not consolidating.

---

## 6. Comparison: Roadmap Prompt vs. Tasklist Prompt

### Tasklist generation prompt (`tasklist/prompts.py`, lines 171-237)

The tasklist prompt says (line 182):

```
"Organize tasks by roadmap phase. Preserve all roadmap item IDs, "
"deliverable IDs, and dependency chains exactly as specified."
```

**Key difference**: The tasklist prompt explicitly says "Organize tasks by roadmap phase" -- it inherits the phase structure from the roadmap. It does NOT decompose or re-phase. The tasklist is downstream of the roadmap's phase decisions.

**Shared decomposition instructions**: NO. The roadmap and tasklist prompts do NOT share decomposition logic. The roadmap prompt asks for "Phased implementation plan" with no count guidance. The tasklist prompt asks for "decompose it into a structured tasklist" organized by the roadmap's existing phases.

Both prompts share:
- The `_OUTPUT_FORMAT_BLOCK` constant (YAML frontmatter enforcement)
- The conditional TDD/PRD supplementary block pattern
- Requirement ID preservation instructions

Neither shares phase decomposition rules.

---

## 7. Integration Enumeration Block (lines 38-49)

The `_INTEGRATION_ENUMERATION_BLOCK` constant is appended to `build_generate_prompt` (line 483) and contains:

```
"- **Owning Phase**: Which phase creates/populates the mechanism\n"
"- **Cross-Reference**: Which phase(s) consume the wired mechanism\n"
```

This block is appended regardless of whether TDD/PRD is present. It asks the LLM to assign phases to integration mechanisms but still does NOT prescribe phase count or structure. It is always present -- it is not conditional on supplementary input.

---

## 8. Could Richer Input Cause Fewer Phases?

### Direct prompt evidence: NO explicit mechanism

There is nothing in the prompts that says "when you have more detailed input, consolidate into fewer phases" or "richer specifications warrant broader phases." The prompts are additive -- more input adds more instructions, but never modifies the base structural guidance.

### Indirect/emergent possibility: YES, plausible via LLM behavior

The TDD supplementary block in `build_generate_prompt` (lines 436-463) adds 6 categories of work to "Address each in the roadmap with specific implementation phases, tasks, and milestones." When the LLM processes a rich TDD, it may:

1. **Group related TDD artifacts into fewer, broader phases** to keep the roadmap manageable (e.g., combining "Data Models", "API Specifications", and "Component Inventory" into a single "Core Implementation" phase)
2. **Treat TDD detail as implementation specificity within phases** rather than creating separate phases per TDD section
3. **Apply implicit coherence heuristics** -- an LLM given more structured input may produce a more consolidated output because the relationships between items are clearer

**However, this is emergent LLM behavior, not prompt-directed behavior.** The prompt neither encourages nor discourages consolidation.

### The PRD's phasing influence

The PRD block (lines 465-481) introduces value-based prioritization ("deliver measurable business value earliest") and persona-driven sequencing. This could cause the LLM to restructure phases around business value rather than technical decomposition, potentially producing a different (possibly smaller) phase count if business-value grouping is coarser than technical-feature grouping.

Again, this is emergent, not explicitly instructed.

---

## Gaps and Questions

1. **No phase count guidance**: The roadmap generation prompt provides ZERO guidance on how many phases to produce. This is the single largest under-specification in the prompt. Adding a heuristic (e.g., "target 4-8 phases for MEDIUM complexity, 6-12 for HIGH") would make phase count more deterministic.

2. **No consolidation instruction**: When TDD adds 6 new categories of work, the prompt does not say whether these should be new phases or folded into existing phases. This ambiguity could cause variance between runs.

3. **No phase count frontmatter**: The generate prompt's YAML frontmatter does NOT include `phase_count` or `milestone_count`. Adding this would make phase count trackable and gate-checkable.

4. **Asymmetric influence**: TDD adds structural work categories ("Include schema implementation tasks..."), while PRD adds prioritization constraints ("prioritize phases that deliver measurable business value earliest"). These pull in different directions -- TDD toward more phases (more categories), PRD toward fewer (value-grouped). Their interaction when both are present is undefined.

5. **No diff between TDD-present and TDD-absent generate prompts on structure**: The only structural difference is additive supplementary blocks. The base "Phased implementation plan with milestones" instruction is identical in both cases.

6. **Tasklist inherits phase structure uncritically**: The tasklist prompt says "Organize tasks by roadmap phase" with no mechanism to flag if the roadmap has too many or too few phases. It is a passive consumer of whatever phase structure the roadmap produces.

7. **Missing question**: Does the extraction step's `complexity_class` (LOW/MEDIUM/HIGH) influence phase count in the generate step? The generate prompt mentions `complexity_score` and `complexity_class` in the frontmatter it should "reference for context" (lines 400-401) but gives NO instruction on how complexity should influence phase count. The test-strategy prompt DOES map complexity to ratios (lines 853-856: LOW->1:3, MEDIUM->1:2, HIGH->1:1) but no equivalent mapping exists for phase count.

---

## Summary

**The roadmap generation prompts do NOT contain any mechanism that would cause fewer phases when TDD+PRD supplementary input is present.** The supplementary blocks are purely additive -- they append instructions for additional work categories and scoring dimensions but never modify the base prompt's structural guidance.

The base `build_generate_prompt` says "Phased implementation plan with milestones" with no count, no minimum, no maximum, no complexity-to-phase mapping, and no consolidation guidance. Phase count is entirely determined by LLM inference, which means it is non-deterministic and could vary between runs even with identical input.

If richer input (TDD+PRD) produces fewer phases in practice, this is an **emergent LLM behavior** -- not a prompt-directed outcome. The most likely mechanism would be: richer, more structured input lets the LLM see relationships between items more clearly, leading it to group related work into broader phases rather than splitting granularly. But this is speculation; the prompt neither encourages nor discourages it.

**Actionable finding**: Adding explicit phase-count guidance (e.g., a complexity-to-phase-count mapping like the test strategy's complexity-to-ratio mapping) to `build_generate_prompt` would be the most direct way to make phase count deterministic and prevent unintended consolidation when supplementary input is present.
