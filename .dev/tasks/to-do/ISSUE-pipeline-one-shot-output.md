# ISSUE: Pipeline Steps Use One-Shot Output — Will Fail at Scale

## Problem

All roadmap pipeline steps (`extract`, `generate`, `merge`, `score`, `debate`, `test-strategy`, `spec-fidelity`) run as `claude --print --output-format text` subprocesses. This means the LLM must produce its ENTIRE output in a single response, held in memory, written to stdout on process exit.

**Source:** `src/superclaude/cli/pipeline/process.py:75-83` — `ClaudeProcess.build_command()` uses `--print` and `--output-format text`.

**Source:** `src/superclaude/cli/roadmap/executor.py:749-758` — `roadmap_run_step()` creates `ClaudeProcess` with `output_format="text"`.

## Why This Will Fail

1. **Output token limits** — When prompts ask for large structured output (e.g., 14-section extraction with per-entity IDs, or a detailed roadmap with 80+ task rows), the LLM hits max output tokens and truncates. Already observed: TDD extraction produced 10/14 sections before truncating.

2. **Context pressure** — Large input (TDD 876 lines + PRD 406 lines + extraction prompt) leaves less room for output in the same context window. The LLM works entirely in memory with no ability to write partial results to disk.

3. **No incremental writing** — Unlike research/synthesis agents (which use Write + Edit to build files incrementally), pipeline agents have no filesystem access. They can't write section-by-section. If the response is interrupted or truncated, ALL work is lost.

4. **No continuation** — Although `--max-turns 100` is set, the agents don't use tools, so there's only 1 turn. The pipeline has no mechanism to detect truncation and re-prompt "continue from where you left off."

5. **Hallucination risk** — Generating large structured documents in one pass increases the chance of inconsistencies, fabricated content, and format drift compared to incremental generation with verification.

## Impact

- TDD+PRD extraction truncated at 10/14 sections (lost Component Inventory, Testing Strategy, Migration, Operational Readiness)
- Merge step frequently fails on `no_duplicate_headings` — possibly because one-shot generation of long roadmaps is more prone to heading duplication
- Will get worse as input documents get longer and output requirements get more granular

## Recommended Fix

Change pipeline agents from one-shot text output to incremental file writing:

1. Switch `output_format` from `"text"` to allowing tool use (Write/Edit)
2. Add instructions to each prompt telling the agent to write to the output file incrementally
3. The pipeline reads the output file after the subprocess exits (already does this for gate checks)
4. Add truncation detection — if the output file is missing expected sections, re-prompt with "continue from section N"

This aligns pipeline agents with how all other agents in the system work (research, synthesis, assembly — all use incremental writing).

## Priority

HIGH — This is a structural limitation that blocks the TDD/PRD entity ID fix from working correctly and will cause increasing failures as document complexity grows.

## Related

- TDD entity ID extraction fix (prompts.py changes) — blocked by this issue for large TDD documents
- Merge step duplicate heading failures — possibly caused by one-shot generation pressure
