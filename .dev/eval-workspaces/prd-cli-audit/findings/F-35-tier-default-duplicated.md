# F-35: Tier default duplicated between Click and `resolve_config`

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P7
**Identified by**: C-8
**File:line**: `src/superclaude/cli/prd/commands.py:55` (`default="standard"`); `src/superclaude/cli/prd/config.py:85` (`(tier or "standard").lower()`)

## Evidence

Click defaults to `"standard"`, so `tier` is never `None` when called from CLI. `config.py:85`'s `tier or "standard"` only fires when `resolve_config` is invoked programmatically (e.g. from tests). Two defaults that could drift independently.

## Trace

Both currently `"standard"`. If one is changed without the other, programmatic callers vs CLI callers get different defaults silently.

## Confidence (aggregated)

0.90 -- Agent C verified both default sites. Pattern is real but consequence is latent.

## Cross-agent corroboration

- **Agent C** identified the dual-default and noted the drift risk between CLI and programmatic invocation paths.
