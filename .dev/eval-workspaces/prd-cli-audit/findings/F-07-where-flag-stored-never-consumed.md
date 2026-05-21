# F-07: `--where` flag stored on config, never read by any consumer

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P2
**Identified by**: C-2
**File:line**: `src/superclaude/cli/prd/commands.py:41-45, 82, 107`; `src/superclaude/cli/prd/config.py:50, 64, 134`; `src/superclaude/cli/prd/models.py:182`; `src/superclaude/cli/prd/prompts.py:54-101`

## Evidence

```python
# commands.py:41
@click.option("--where", "-w", multiple=True, help="Source directories to focus on (repeatable).")
# config.py:134
where=list(where) if where else [],
# models.py:182
where: list[str] = field(default_factory=list)

# grep -rn "config\.where|cfg\.where|self\._config\.where" src/ returns no hits
```

## Trace

- **Writer**: argparse -> `resolve_config(where=...)` -> `PrdConfig.where` list.
- **Reader**: none. The parse-request prompt (prompts.py:54-101) asks the LLM to extract `WHERE` from the natural-language `user_message` itself. Scope-discovery then reads `parsed-request.json["WHERE"]`. The CLI-provided `--where` list is never injected into any prompt or written into `parsed-request.json` as a seed.
- **Consequence**: `--help` text and the docstring example at commands.py:25 actively misrepresent the behavior. Users pass `--where src/api --where src/search` and those paths are silently dropped.

## Reproduction sketch

`superclaude prd run "Add search" --where src/api --where src/search`. The two paths are silently dropped. If the user's natural-language string does not also name them, scope discovery roams the whole repo.

## Confidence (aggregated)

0.95 -- Single agent, but mechanically verified via negative grep result across `src/`. Could only be wrong if a consumer accesses `where` via getattr/string lookup, which was not found.

## Cross-agent corroboration

- **Agent C** discovered and fully traced this: the flag reaches `PrdConfig.where` correctly but zero consumers read it, while the parse-request prompt independently re-derives `WHERE` from the user's natural language, making the CLI flag a dead surface.
