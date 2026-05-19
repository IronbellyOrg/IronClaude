# Baseline snapshot — `src/superclaude/cli/prd/config.py`

**Captured:** 2026-05-19T02:03:26Z
**Purpose:** Pre-patch reference state for diff verification in Phase Gate PG-2.

## Defect summary

`L100: output_path = Path(output).resolve() if output else Path(".").resolve()` defaults to **CWD** when no `--output` flag is supplied. Combined with `task_dir_name = f"prd-{product_slug}"` (L107) and `task_dir = output_path / task_dir_name` (L108), invocations of `superclaude prd run` from the repo root create `<repo-root>/prd-<slug>/` directories — the source-of-truth defect surfaced by Phase 1 of TASK-RF-20260518-181333.

## Lines 95-115 of `src/superclaude/cli/prd/config.py` (verbatim)

```python
            f"Unrecognised resume step ID: {resume_from!r}. "
            f"Expected a known step pattern like 'parse-request', "
            f"'investigation-3', 'qa-synthesis-gate', etc."
        )

# -- Path resolution --
output_path = Path(output).resolve() if output else Path(".").resolve()

# Derive product slug from product name or request
product_name = product or ""
product_slug = _slugify(product_name) if product_name else ""

# Task directory: derived from output_path + product_slug (or 'prd-task')
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
task_dir = output_path / task_dir_name

# Skill refs directory: auto-discover from known locations
skill_refs_dir = _discover_skill_refs_dir()

return PrdConfig(
    user_message=request,
```

Note: lines as shown above are dedented for clarity in this markdown snapshot — the actual file indents the body of `resolve_config` by 4 spaces. The semantic content (the single-line ternary at L100, the comments at L99/L102/L106/L110, the assignment at L107-108) matches `src/superclaude/cli/prd/config.py` exactly.

## Patch target

- **Single line to replace:** L100 — `    output_path = Path(output).resolve() if output else Path(".").resolve()`
- **Lines that must remain unchanged:** L107 (`task_dir_name`), L108 (`task_dir`), and all surrounding comments.
- **Indentation level:** 4 spaces (body of `resolve_config`).
