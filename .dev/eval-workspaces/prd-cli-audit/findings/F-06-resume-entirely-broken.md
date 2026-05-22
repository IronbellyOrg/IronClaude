# F-06: resume entirely broken -- executor ignores config, CLI drops flags

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P2, P5, P7, P8
**Identified by**: A-4, C-3
**File:line**: `src/superclaude/cli/prd/executor.py` (no resume_from references); `src/superclaude/cli/prd/commands.py:135-191`; `src/superclaude/cli/prd/models.py:196, 260-271`

## Evidence

```python
# commands.py:174-187 (resume subcommand) -- drops critical flags
config = resolve_config(request="", ..., resume_from=step_id)
# Missing: product, tier, output, where
executor = PrdExecutor(config)
result = executor.run()      # run() ignores config.resume_from

# executor.py -- grep for resume_from returns 0 matches

# models.py:260-271 -- resume_command EMITS flags the CLI won't accept
def resume_command(self) -> str:
    parts = ["superclaude", "prd", "resume", self.halt_step]
    if self.config.product_name:
        parts.extend(["--product", self.config.product_name])
    if self.config.tier != "standard":
        parts.extend(["--tier", self.config.tier])
    return " ".join(parts)
```

## Trace

- **Config defined**: `resume_from` is defined in models.py:196, validated in config.py:93-95, plumbed via commands.py:180.
- **Executor gap**: `PrdExecutor.run()` (executor.py:344-415) iterates `_STAGE_A_STEPS` from index 0 unconditionally; there is no skip logic conditioned on `resume_from`. `grep -rn "resume_from" src/superclaude/cli/prd/executor.py` returns 0 matches.
- **CLI gap**: `prd resume` only declares `--max-turns`, `--model`, `--debug`. Click rejects unknown options. `resume_command()` emits `--product` and `--tier` for the user to copy-paste, but Click will reject them with `Error: No such option: --product`.
- **Result**: Resume always reruns the full pipeline from step 1, overwriting partial artifacts, at standard tier, in a fresh `prd-task/` directory. Users are silently misled.

## Reproduction sketch

`superclaude prd run "x" --product foo --tier heavyweight` (Ctrl-C after step 3) then `superclaude prd resume parse-request`. Result: re-runs check-existing AND parse-request AND every subsequent step from scratch, at standard tier, in `prd-task/` instead of `prd-foo/`.

## Confidence (aggregated)

0.97 -- Agent A confirmed zero grep hits in executor. Agent C confirmed the Click surface exhaustively omits the flags and traced the path-resolution consequence.

## Cross-agent corroboration

- **Agent A** identified the executor side: `resume_from` has zero readers in the entire executor module, making the `resume` CLI subcommand a silent no-op that reruns from step 1.
- **Agent C** identified the CLI side: the resume subcommand drops `--tier`, `--product`, `--output`, `--where`, and `resume_command()` emits flags Click will reject, so even the documented resume invocation crashes.
