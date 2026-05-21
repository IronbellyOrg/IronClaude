# F-21: Dual slug sources (CLI `--product` vs LLM-emitted PRODUCT_SLUG) with no reconciliation

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P2, P7
**Identified by**: C-6
**File:line**: `src/superclaude/cli/prd/config.py:120-125`; `src/superclaude/cli/prd/prompts.py:65-101`

## Evidence

```python
# prompts.py:73 (parse-request prompt asks the LLM to emit its own slug)
{
  "PRODUCT_NAME": "...",
  "PRODUCT_SLUG": "<kebab-case identifier>",
  ...
}

# config.py:121-123 (CLI-derived slug already used for task_dir)
product_slug = _slugify(product_name) if product_name else ""
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
task_dir = output_path / task_dir_name
```

## Trace

- **Writer A**: CLI `--product` -> `_slugify` -> `config.product_slug` -> `task_dir` name -> build-task-file Write target.
- **Writer B**: parse-request LLM step writes `parsed-request.json` containing `PRODUCT_SLUG`. Read by scope-discovery and other downstream steps.
- **No reconciler**: If they diverge (user passes `--product "User Auth"` -> slug `user-auth`; LLM emits `auth` or `userauth`), some prompts cite the CLI slug, others cite the parsed slug. Downstream gates/inventory rely on whichever the consumer happens to read.

## Reproduction sketch

`superclaude prd run "Build auth for v2" --product "User Auth Module"`. Inspect `parsed-request.json` after step 2 -- observe `PRODUCT_SLUG` value vs `config.product_slug = "user-auth-module"`.

## Confidence (aggregated)

0.80 -- Agent C confirmed the divergence path is real. Impact depends on downstream readers not exhaustively traced.

## Cross-agent corroboration

- **Agent C** traced the two independent slug writers and identified the absence of any reconciliation mechanism, noting that the CLI slug drives `task_dir` while the LLM slug drives `parsed-request.json` with no cross-validation.
