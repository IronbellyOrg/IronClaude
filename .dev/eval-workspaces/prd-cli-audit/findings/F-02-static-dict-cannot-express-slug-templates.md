# F-02: Static dict cannot express slug-templated artifact names

**Final severity (Stage 2 preliminary)**: CRITICAL
**Pattern tags**: P3, P5
**Identified by**: A-2, E-2, C-5 (partial), F-4
**File:line**: `src/superclaude/cli/prd/executor.py:246-293`, `src/superclaude/cli/prd/prompts.py:381`, `src/superclaude/cli/prd/config.py:121-125`

## Evidence

```python
# executor.py:267-281 -- static-key lookup, no interpolation
artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
...
base_name = Path(artifact_name).name
...
for match in root.rglob(base_name):

# prompts.py:381 -- the Write target varies per run
Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}

# config.py:121-125 -- slug varies per invocation
product_slug = _slugify(product_name) if product_name else ""
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
```

## Trace

- **Writer**: The Claude subprocess writes to `TASK-PRD-{slug}.md` where `{slug}` is derived per-run from `product_slug` (which itself may come from the LLM at parse-request, not just CLI `--product`).
- **Reader**: `_STEP_ARTIFACT_FILES` is `dict[str, str]` -- keys are step IDs, values are literal filenames. There is no mechanism to (a) interpolate slug variables, (b) accept a glob pattern, or (c) accept a callable.
- **Chain break**: Adding `"build-task-file": "TASK-PRD-{slug}.md"` would search for a literal file with curly braces in the name. `Path(artifact_name).name` and `root.rglob(base_name)` both treat the value as an exact filename, not a pattern.
- **Workaround exists**: prompts.py:405 and :464 already use `config.task_dir.glob("TASK-PRD-*.md")` for the verify and preparation steps. The same pattern needs to be available to `_resolve_step_content`.

## Reproduction sketch

Even a hypothetical fix that adds `"build-task-file": "TASK-PRD.md"` to the dict would miss `TASK-PRD-20260520-userauth.md`. The dict value type must change (to support glob patterns or callables) or `_resolve_step_content` must gain pattern/glob support.

## Confidence (aggregated)

0.97 -- Agent A verified the resolve function end-to-end with no pattern/glob/interpolation hooks. Agent E confirmed the prompt emits a slug-templated path and that prompts.py itself uses glob as a workaround elsewhere. Agent C confirmed slug derivation and the empty-slug edge case.

## Cross-agent corroboration

- **Agent A** identified the static dict type constraint and showed that `rglob` treats values as exact filenames.
- **Agent E** confirmed from the prompt side that the Write target is slug-templated and noted that prompts.py already uses glob at lines 405/464 as the correct pattern.
- **Agent C** traced `product_slug` derivation and noted that the slug can be empty (compounding the issue with `TASK-PRD-.md`).
- **Agent F** confirmed no test exists for slug-templated artifact resolution.
