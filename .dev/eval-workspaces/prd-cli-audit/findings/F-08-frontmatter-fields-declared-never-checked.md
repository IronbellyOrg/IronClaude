# F-08: `required_frontmatter_fields` declared but never checked in PRD _evaluate_gate

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P1, P2, P7
**Identified by**: B-2
**File:line**: Consumer expected in `src/superclaude/cli/prd/executor.py:587-624`; declarations in `src/superclaude/cli/prd/gates.py:298, 304, 317, 323, 341, 354, 360-366, 388, 402, 408, 414, 426, 433, 439, 452-458, 475, 488, 502`

## Evidence

```python
# executor.py:_evaluate_gate -- only checks performed
if gate.min_lines > 0:
    line_count = len(content.splitlines())
    ...
if gate.semantic_checks:
    for check in gate.semantic_checks:
        ...

# gates.py:359-367 (build-task-file) -- frontmatter fields declared but never read
"build-task-file": GateCriteria(
    required_frontmatter_fields=[
        "id", "title", "status", "complexity", "created_date",
    ],
    min_lines=400, ...
)

# gates.py:451-458 (assembly)
"assembly": GateCriteria(
    required_frontmatter_fields=[
        "id", "title", "status", "created_date", "tags",
    ], ...
)
```

## Trace

- **Writer**: 17 gate entries declare `required_frontmatter_fields` (4 of them non-empty: `research-notes`, `build-task-file`, `assembly`, and `parse-request`).
- **Reader**: `grep -n "required_frontmatter_fields\|frontmatter" src/superclaude/cli/prd/executor.py` returns zero matches. The PRD pipeline's bespoke `_evaluate_gate` ignores that field entirely.
- **Generic pipeline**: `src/superclaude/cli/pipeline/gates.py` has a generic evaluator that does check frontmatter, but PRD does NOT use it.
- **Consequence**: The original heavyweight failure (30-line NDJSON commentary read as a task file) would also have failed the frontmatter check (`id`, `title`, `status` would all be missing) -- but the check never runs, so the only line that actually halted was the min_lines check.

## Reproduction sketch

Run a heavyweight PRD pipeline that produces a task file without `created_date` in its frontmatter. The gate still passes (line count + semantic checks satisfied). Downstream consumers that assume those frontmatter fields exist would crash with `KeyError`.

## Confidence (aggregated)

0.97 -- Agent B verified via grep that the field is unread in the PRD executor. The gap is mechanically verifiable.

## Cross-agent corroboration

- **Agent B** identified the dead-code field and noted that the original 30-line NDJSON artifact would have failed frontmatter validation had the check been wired, making this a defense-in-depth gap that would have caught the Bug 1 failure through a second mechanism.
