# F-15: Empty product_slug produces malformed artifact paths and frontmatter IDs

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P5, P7
**Identified by**: C-5
**File:line**: `src/superclaude/cli/prd/config.py:120-125`; `src/superclaude/cli/prd/prompts.py:381, 384, 405, 464`

## Evidence

```python
# config.py:120-123
product_name = product or ""
product_slug = _slugify(product_name) if product_name else ""
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"

# prompts.py:381 -- concatenation with empty slug
Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}
# Produces: TASK-PRD-.md

# prompts.py:384
- id: TASK-PRD-{config.product_slug}
# Produces: id: TASK-PRD-  (invalid MDTM identifier)
```

## Trace

- **Writer**: `_slugify` is gated on `product_name` truthiness; no fallback derives a slug from `request`, repo name, or timestamp.
- **Reader**: prompts.py:381 interpolates `product_slug` into the literal Write path. When the slug is empty, the LLM is told to write to `TASK-PRD-.md` with id `TASK-PRD-`.
- **Chain break with F-02**: A static `_STEP_ARTIFACT_FILES["build-task-file"] = "TASK-PRD-{slug}.md"` cannot be expressed because the dict carries plain strings, not patterns. Adding the entry needs slug interpolation at lookup time.
- **Downstream**: `prompts.py:405, 464` glob `config.task_dir.glob("TASK-PRD-*.md")` and pick `task_files[0]` -- works by accident even with empty slug, but the canonical filename is malformed.

## Reproduction sketch

`superclaude prd run "Build auth" --tier lightweight` (no `--product`). Generated path: `.../prd-task/TASK-PRD-.md`. Frontmatter id `TASK-PRD-`.

## Confidence (aggregated)

0.93 -- Agent C confirmed all four interpolation sites in prompts.py.

## Cross-agent corroboration

- **Agent C** traced the slug derivation from config through all interpolation sites and identified the chain break with F-02: even if the dispatch table entry is added, the empty-slug case produces an invalid filename pattern.
