# 06 — Context Window Saturation Analysis

**Status**: Complete
**Investigator:** Architecture Analyst
**Date:** 2026-04-03
**Question:** Does the combined size of TDD+PRD roadmap, supplementary files, and skill protocol approach context window limits, leaving less room for task generation output?

---

## 1. Generation Pathway Identification

Before estimating token budgets, we must identify **how** the tasklist is generated. Two pathways exist:

| Pathway | Mechanism | Context Window |
|---------|-----------|----------------|
| **CLI Pipeline** (`superclaude roadmap run`) | `claude -p` subprocess; prompt passed as CLI argument | Model's full context window (200K for Sonnet, 200K for Opus). CLI arg limit is 120KB for the prompt string, but the model sees the full context. |
| **Skill Protocol** (`/sc:tasklist`) | Interactive Claude Code session; SKILL.md loaded into session context alongside CLAUDE.md, user files, and conversation history | Model's full context window minus session overhead (CLAUDE.md, skills index, conversation history). |

**Evidence from test fixtures:**
- `test3-spec-baseline/` has `tasklist-fidelity.err` -- the tasklist was generated via CLI pipeline (which includes a tasklist step).
- `test1-tdd-prd-v2/` has **no** `tasklist*.err` file -- the tasklist was likely generated via the skill protocol (`/sc:tasklist`), not the CLI pipeline's integrated tasklist step.

This distinction is critical: the skill protocol pathway loads significantly more ambient context.

---

## 2. Component Size Inventory

### Raw byte counts (measured)

| Component | Bytes | Est. Tokens (~4 chars/token) | Role |
|-----------|-------|------------------------------|------|
| SKILL.md (sc-tasklist-protocol) | 63,273 | ~15,818 | Generation protocol instructions |
| TDD+PRD Roadmap (746 lines) | 44,004 | ~11,001 | Primary input (TDD+PRD scenario) |
| Baseline Roadmap (380 lines) | 25,773 | ~6,443 | Primary input (baseline scenario) |
| TDD source document | 44,148 | ~11,037 | Supplementary input (TDD+PRD scenario) |
| PRD source document | 19,619 | ~4,905 | Supplementary input (TDD+PRD scenario) |
| prompts.py (generate prompt text) | ~3,500* | ~875 | Prompt template (generate function only) |
| Project CLAUDE.md | 11,894 | ~2,974 | Session system prompt |
| User CLAUDE.md | 5,282 | ~1,321 | Session system prompt |
| Skills index (session startup) | ~5,000** | ~1,250 | Skill listings loaded at session start |

*Only the `build_tasklist_generate_prompt` function body (~3,500 bytes when TDD+PRD blocks included).
**Estimated from the skills listing in the session context.

### Derived prompt content from `build_tasklist_generate_prompt`

The `prompts.py` file assembles the generation prompt as follows:

1. **Base prompt** (~740 bytes): "You are a tasklist generator..." with basic instructions
2. **TDD enrichment block** (conditional, ~640 bytes): 5 enrichment rules for TDD cross-referencing
3. **PRD enrichment block** (conditional, ~770 bytes): 5 enrichment rules plus scope guard
4. **TDD+PRD interaction block** (conditional, ~280 bytes): Precedence note
5. **`_OUTPUT_FORMAT_BLOCK`** (~330 bytes): YAML frontmatter format instructions

Total prompt template when both TDD+PRD: ~2,760 bytes (~690 tokens)

---

## 3. Context Window Budget Calculations

### Scenario A: Baseline (Roadmap Only, Skill Protocol)

| Category | Est. Tokens |
|----------|-------------|
| Session overhead (CLAUDE.md x2, skills index) | ~5,545 |
| SKILL.md protocol | ~15,818 |
| Roadmap (380 lines) | ~6,443 |
| Prompt template (base only) | ~268 |
| **Total input estimate** | **~28,074** |

### Scenario B: TDD+PRD (Skill Protocol)

| Category | Est. Tokens |
|----------|-------------|
| Session overhead (CLAUDE.md x2, skills index) | ~5,545 |
| SKILL.md protocol | ~15,818 |
| Roadmap (746 lines) | ~11,001 |
| TDD source document | ~11,037 |
| PRD source document | ~4,905 |
| Prompt template (TDD+PRD enrichment) | ~690 |
| **Total input estimate** | **~48,996** |

### Scenario C: CLI Pipeline (for reference)

The CLI pipeline uses `claude -p` subprocess with the prompt as a CLI arg. The 120KB (`_EMBED_SIZE_LIMIT`) constraint applies to the CLI argument string, not the model context window. When the prompt plus embedded file content exceeds 120KB, a warning is logged but execution proceeds.

For the TDD+PRD scenario via CLI:
- Prompt template: ~2,760 bytes
- Roadmap (embedded): ~44,004 bytes
- TDD (embedded): ~44,148 bytes
- PRD (embedded): ~19,619 bytes
- **Total: ~110,531 bytes** -- 90% of the 120KB CLI arg limit

This is tight but within bounds. However, the CLI `tasklist` step does NOT embed the TDD/PRD source documents in the prompt -- the `_embed_inputs` function only embeds the roadmap file. The TDD and PRD files are referenced in the prompt template instructions but are not inlined as file content in the CLI pathway.

---

## 4. Context Window Utilization

### Model context windows (Claude Code, April 2026)

| Model | Context Window | Max Output Tokens |
|-------|---------------|-------------------|
| Claude 3.5 Sonnet | 200,000 tokens | ~8,192 |
| Claude 3.5 Haiku | 200,000 tokens | ~8,192 |
| Claude Opus 4 | 200,000 tokens | ~32,000 |

### Utilization percentages

| Scenario | Input Tokens | % of 200K Window | Remaining for Output |
|----------|-------------|-------------------|---------------------|
| A: Baseline | ~28,074 | **14.0%** | ~171,926 tokens |
| B: TDD+PRD | ~48,996 | **24.5%** | ~151,004 tokens |
| Delta (B - A) | +20,922 | +10.5% | -20,922 tokens |

### Output token comparison

| Scenario | Output Lines | Output Bytes | Est. Output Tokens |
|----------|-------------|-------------|-------------------|
| Baseline (test3) | 3,380 | 108,867 | ~27,217 |
| TDD+PRD (test1-v2) | 2,407 | 114,339 | ~28,585 |

**Key observation:** The TDD+PRD output has **fewer lines** (2,407 vs 3,380, a 29% reduction) but **more bytes** (114,339 vs 108,867, a 5% increase). This means TDD+PRD tasks are individually longer/denser but there are fewer of them.

---

## 5. Saturation Assessment

### Is context saturation a plausible explanation?

**No. Context window saturation is NOT a plausible explanation for fewer tasks.**

The evidence against saturation:

1. **Utilization is low:** Even in the TDD+PRD scenario, input consumes only ~24.5% of the 200K context window. Over 150K tokens remain available for output -- far more than the ~28K tokens actually generated.

2. **Output bytes actually increased:** The TDD+PRD scenario produced 114,339 bytes vs 108,867 bytes for baseline. If the model were truncating due to context pressure, we would expect fewer output bytes, not more.

3. **The delta is small relative to headroom:** The additional ~21K input tokens from TDD+PRD supplementary content represents only a 10.5% increase in context utilization. The model has ~151K tokens of headroom vs ~172K in baseline -- both vastly exceed the actual output size.

4. **Max output tokens is the binding constraint, not context:** Claude models have explicit max output token limits (8K-32K depending on model). At ~28K output tokens, both scenarios are near the max output limit regardless of input size. The fewer-but-denser tasks in TDD+PRD suggest the model is hitting the same output ceiling but allocating tokens differently (more detail per task, fewer tasks).

5. **The 120KB CLI arg limit is irrelevant for skill protocol:** The skill protocol runs inside the Claude Code session, not via `claude -p` subprocess. The CLI arg size limit does not apply.

### What IS the binding constraint?

The **max output token limit** (not context window) is the more likely binding constraint:

- Baseline: ~27,217 output tokens across 3,380 lines (5 phases, many tasks)
- TDD+PRD: ~28,585 output tokens across 2,407 lines (3 phases, fewer but denser tasks)

Both outputs are in the same ~27K-29K output token range. The model appears to hit a consistent output budget and distributes it differently:
- **Without enrichment:** More tasks, less detail per task
- **With enrichment:** Fewer tasks, more detail per task (TDD/PRD cross-references, persona annotations, metric subtasks)

This is an **output budget allocation** effect, not a context window saturation effect.

---

## 6. Alternative Explanations for Task Count Reduction

Given that context saturation is ruled out, the 29% task count reduction (3,380 -> 2,407 lines) is more likely explained by:

1. **Task consolidation via enrichment:** TDD+PRD enrichment rules (sections 4.4a/4.4b of SKILL.md) explicitly instruct "Merge rather than duplicate if a generated task duplicates an existing task for the same component." This consolidation naturally produces fewer, richer tasks.

2. **Phase count difference:** test3-baseline has 5 phases; test1-tdd-prd-v2 has 3 phases. The roadmap structure itself (not context pressure) determines phase count.

3. **Roadmap content difference:** The 746-line TDD+PRD roadmap is a merged adversarial roadmap with different structural decisions than the 380-line baseline roadmap. Different input -> different output.

4. **Output token ceiling behavior:** Both scenarios produce ~28K output tokens. The model appears to have a consistent generation budget regardless of input size.

---

## Gaps and Questions

1. **Output token limit verification:** What specific model was used for each test run? The max output tokens differ between Sonnet (8K) and Opus (32K). If Sonnet was used, the ~28K output tokens would exceed the 8K limit -- suggesting either Opus was used or the Claude Code session enables multi-turn generation that bypasses single-response limits.

2. **Multi-turn generation:** Does the skill protocol generate the tasklist in a single response or across multiple turns? If multi-turn, context window pressure accumulates differently (earlier turn outputs become input context for later turns).

3. **Actual token counts:** The ~4 chars/token approximation is rough. Actual tokenization of structured markdown with code fences, tables, and YAML may differ significantly. Precise counts from the API usage logs would be more reliable.

4. **Conversation history:** In the skill protocol pathway, prior conversation turns consume context. If the user had a long conversation before invoking `/sc:tasklist`, the effective available context could be much smaller than the raw 200K window. This analysis assumes a fresh session.

5. **CLI vs Skill divergence:** The test fixtures may not both use the same generation pathway. If test3 used the CLI pipeline and test1-v2 used the skill protocol, the comparison is confounded by pathway differences, not just input differences.

---

## Summary

**Context window saturation does not explain the reduction in task count.** The TDD+PRD scenario uses approximately 49K input tokens (24.5% of the 200K context window), leaving over 150K tokens available -- far more than the ~28K tokens actually generated. Both scenarios produce roughly the same total output bytes (~110-114KB), suggesting a consistent output token budget.

The fewer tasks in TDD+PRD are more likely caused by: (a) explicit merge/consolidation rules in the SKILL.md protocol that reduce duplication when enrichment sources are available, (b) structural differences in the roadmap itself (3 phases vs 5 phases), and (c) the model redistributing a fixed output budget toward fewer, denser tasks with TDD/PRD cross-references.

The **max output token limit** (not context window) is the more plausible binding constraint. Both scenarios generate approximately the same total output volume, but the TDD+PRD scenario produces fewer tasks with more detail per task. This is an output budget allocation effect, not a context saturation effect.

**Verdict:** Context window saturation is **not a contributing factor** to the task count reduction. Investigate output token limits and task consolidation rules instead.
