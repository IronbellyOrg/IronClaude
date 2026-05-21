# Evidence Validation Report — evidence-validator agent

**Report draft**: REPORT.md
**Evidence section locator**: "## Evidence"
**allow_command_reexec**: false
**Method**: For each cited `file:line` in the report's Evidence section, I Read the on-disk fixture at that exact line range and verified the cited snippet matches the file content.

## Citations checked

| # | Citation | File on disk | Status |
|---|----------|--------------|--------|
| 1 | `commands.py:1472-1477` — `eval_run` resolve_scratch_root call with `output_dir=output_dir` kwarg | verified (lines 1472-1477 show exactly: `try: / resolved_output = resolve_scratch_root( / requested_output, / config=base_config, / output_dir=output_dir, / )`) | **VERIFIED** |
| 2 | `commands.py:1476` — the smoking-gun `output_dir=output_dir` self-reference | verified (line 1476 reads `            output_dir=output_dir,`) | **VERIFIED** |
| 3 | `commands.py:815-823` — doctor's positional-only call to `resolve_scratch_root(output_dir)` | verified (line 817 reads `            resolve_scratch_root(output_dir)`, no `output_dir=` kwarg) | **VERIFIED** |
| 4 | `config.py:219-220` — kwarg appends to allowlist | verified (line 219: `if output_dir is not None:` / line 220: `allowed.append(_resolve_prefix(Path(output_dir)))`) | **VERIFIED** |
| 5 | `config.py:225-229` — tautological match in the comparison loop | verified (line 225-229 show `for prefix in allowed:` / `if resolved == prefix or resolved.is_relative_to(prefix): return resolved`) | **VERIFIED** |
| 6 | `commands.py:1490-1499` — correct downstream `runtime_allowed` extension | verified (lines 1490-1499 show `runtime_allowed = tuple(base_config.allowed_scratch_roots) + (resolved_output, home_root,)` and the `runtime_config = EvalConfig(...)` construction) | **VERIFIED** |
| 7 | `scratch-roots.md:19-20` — policy doc on `--output-dir <path>` allowlist extension | verified (table rows describe extension "for the current invocation only") | **VERIFIED** |
| 8 | `scratch-roots.md:82-88` — OPS-002 cross-module consistency commitment for `eval run` | verified (paragraph explicitly states future eval run "MUST funnel through that helper") | **VERIFIED** |

## Dropped citations
None.

## Suggested report status
**success** — all citations verified against on-disk fixtures, no drops, no inferred line numbers.
