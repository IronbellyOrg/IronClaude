# auggie-first — closeout

**Status:** complete (shipped on master via commit `184edf7`).
**Closeout commit:** see PR for `feat/freshness-auggie-closeout` branch.

## What shipped

- `src/superclaude/hooks/scripts/auggie-flag-clear.sh` — synchronous PostToolUse sticky-clear (v2.1 §6).
- `src/superclaude/hooks/hooks.json` — `PostToolUse` matcher `mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*` (v2.1 §6 + §14 deferred gateway-alias widening).
- `src/superclaude/hooks/scripts/freshness-user-prompt.sh` (§6.5) and `freshness-session-start.sh` (GC + sticky logic) — auggie-first envelope injection.
- `src/superclaude/hooks/auggie-projects.txt.example` — seed file deployed by `_deploy_seed_files()` in `install_hooks.py`.
- `tests/hooks/test_auggie_first.py` — five-case Python harness covering both `mcp__auggie__*` and `mcp__airis-mcp-gateway__auggie_*` matchers, sentinel guard, sticky preservation, and fail-open paths. Resolves v2.1 §14 deferred test item.

## Spec revisions (archived in this directory)

- `auggie-first-hook-proposal.md` — v1 (locked design from 2026-05-14 /sc:brainstorm). Superseded.
- `auggie-first-hook-proposal-v2.md` — spec-panel-revised draft (sentinel collision + async-race fixes). Superseded.
- `auggie-first-hook-proposal-v2.1.md` — canonical/final; retargets paths from `~/.claude/` to `src/superclaude/` per source-of-truth rule.

## Deferred (out of scope for this closeout)

None — all v2.1 §14 deferred items addressed (gateway-alias matcher widening + test harness landed in this closeout).
