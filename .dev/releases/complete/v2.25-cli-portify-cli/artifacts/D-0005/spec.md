# D-0005 — Prompt Splitting Threshold Decision

**Produced by**: T01.05
**Sprint**: v2.25-cli-portify-cli
**Date**: 2026-03-16

---

## Decision

**Location**: `prompts.py` prompt builder

**Threshold**: 300 lines (aggregate prompt, all sections combined)

**Split output path**: `portify-prompts.md` (in the run's work directory)

---

## Rationale

**Why `prompts.py`**: The prompt builder is the single point that constructs the complete prompt string by assembling all sections (preamble, spec content, step instructions, context). Splitting here ensures:
1. The executor remains clean — it only receives a final prompt string; it does not know or care about splitting.
2. No duplication risk: there is exactly one code path where the aggregate length is knowable.
3. The split file is a builder-level concern, not an executor-level concern.

**Why aggregate, not per-section**: The 300-line threshold from roadmap Phase 9 FR-050/AC-010 applies to the aggregate prompt (all sections combined). Per-section limits would not prevent the model from receiving a prompt too long to process effectively.

---

## Algorithm (for implementation in Phase 9)

```python
def build_prompt(config, step_context) -> str | Path:
    """
    Returns:
        str: the prompt inline (aggregate <= 300 lines)
        Path: path to portify-prompts.md written to work_dir (aggregate > 300 lines)
    """
    sections = _build_sections(config, step_context)
    aggregate = "\n".join(sections)
    if aggregate.count("\n") + 1 > 300:
        prompt_file = config.work_dir / "portify-prompts.md"
        prompt_file.write_text(aggregate)
        return prompt_file  # executor embeds via read + inline
    return aggregate
```

Note: since `--file` is prohibited (OQ-008/FIX-001), the executor reads the split file and embeds its content inline in the `-p` argument — it does NOT pass `--file`.

---

## Scope

This decision affects Phase 9 (T09.xx) `prompts.py` implementation only. Phases 2–8 build the non-splitting prompt builder; Phase 9 adds the split path.

**Confirmed**: 300-line aggregate threshold, `prompts.py` location, `portify-prompts.md` output path.
