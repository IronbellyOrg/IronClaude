# F-37: `failure_area_slug` truncation can collide gap-fix filenames

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P3
**Identified by**: E-13
**File:line**: `src/superclaude/cli/prd/prompts.py:1145, 1172-1173`

## Evidence

```python
failure_area_slug = failure["area"][:20]
...
{config.qa_dir / f"gap-fix-{cycle:02d}-{failure_area_slug}.md"}
```

## Trace

- Two distinct failures with `area` strings sharing the first 20 chars (e.g. `"Authentication and authorization flow"` and `"Authentication and password reset"` both -> `"Authentication and a"`) produce the same `gap-fix-01-Authentication and a.md` path.
- The second fix-report overwrites the first with no collision detection.
- No slug-safety: spaces, slashes, or non-ASCII in `area` flow straight into the filename.

## Reproduction sketch

Produce two QA failures with area strings sharing the same first 20 characters. Second fix-report silently overwrites the first.

## Confidence (aggregated)

0.80 -- Agent E verified the truncation behavior.

## Cross-agent corroboration

- **Agent E** identified the collision risk from the 20-character truncation and the lack of slug-safety for special characters.
