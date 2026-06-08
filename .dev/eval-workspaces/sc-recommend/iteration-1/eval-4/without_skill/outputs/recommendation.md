# Recommendation

For a ~40-line utility refactor, use **`/sc:improve src/utils/timefmt.py`**.

## Why

- `/sc:improve` is purpose-built for systematic code-quality refactoring (readability, maintainability, small structural cleanups) at the file scope — exactly the size/intent here.
- File is small enough that a single-pass improvement is appropriate; no need for `/sc:task` (multi-step orchestration), `/sc:workflow` (PRD-driven), or `/sc:analyze` (diagnostic only, no edits).
- If you want a safety net first, prepend `/sc:analyze src/utils/timefmt.py` to surface issues before `/sc:improve` applies changes. Otherwise, `/sc:improve` alone is the natural fit.
