<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (option-b, SessionStart hook) -->
<!-- Merge date: 2026-10-29 -->
# P2 indexing and sync: final recommendation

<!-- Source: Base original (Variant 2 position, condensed to a verdict) -->
**Verdict:** IronClaude ships a fail-open SessionStart hook that initializes codegraph once per checkout, plus core CLAUDE.md guidance. It writes no global git config.

<!-- Source: Base original (registration bullet) -->
## What ships
- Script `src/superclaude/hooks/scripts/codegraph-session-start.sh`, registered in `src/superclaude/hooks/hooks.json` SessionStart with matcher `startup` and `timeout: 5`.
- Listed in `_FRESHNESS_SCRIPTS` (`src/superclaude/cli/install_hooks.py`), mirrored in `plugins/superclaude/hooks/hooks.json`; the packaged-script pin in `tests/unit/test_cli_install.py` is updated.

<!-- Source: Base modified — portable detach (Change 1), completion marker (Change 2), no lock (Change 3) -->
## Hook behaviour
1. Always exit 0 and print nothing on stdout, so the hook adds no context.
2. Exit if `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`, or if `command -v codegraph` fails.
3. `top=$(git -C "$CLAUDE_PROJECT_DIR" rev-parse --show-toplevel)` or exit (non-git dirs are never indexed); exit if `top` is `$HOME` or `/`.
4. Fast path: exit if `$top/.codegraph/.superclaude-init-ok` exists.
5. Otherwise, with `log=${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/codegraph-init.log`, run `mkdir -p "${log%/*}" || exit 0`, then
   `nohup sh -c 'codegraph init --yes "$1" && touch "$1/.codegraph/.superclaude-init-ok"' _ "$top" </dev/null >>"$log" 2>&1 &`.
   Every descriptor is redirected so Claude Code does not wait; no `setsid` (macOS lacks it). A failed or killed init writes no marker, so the next session retries; on an index Coder already built, init is a ~125 ms no-op and the marker is written. `codegraph uninit` removes the marker with the index.
6. No IronClaude lock: codegraph's own writer lock makes a losing concurrent init fail and retry next session, and a `mkdir` lock goes stale after a kill. No `rm` on failure: it could delete a concurrent Coder init.
- Each worktree, nested or sibling, gets its own index on the first session opened in it.

<!-- Source: Base modified — exact fallback text (Change 4, from Variant 1) -->
## Core CLAUDE.md guidance (`src/superclaude/core/CLAUDE.md`)
> If any codegraph tool returns an error, says the project is not initialized, or says the index belongs to a different working tree, run `codegraph init --yes` at the directory printed by `git rev-parse --show-toplevel`, then retry; it is safe to repeat. If results look incomplete after an interrupted init, run `codegraph index --force`. Never run `codegraph sync` while a session is open: the MCP daemon owns the index.

<!-- Source: Variant 1, Change 5; Variant 3, Change 7; Variant 1, Change 6 -->
## Docs page and dependency
- Docs page: `codegraph init --yes`, `codegraph uninit`, `codegraph index --force`, `codegraph.json` excludes, the cost (~70 KB per file on disk, ~1 GB peak RSS during init) and the opt-out `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`.
- Opt-in recipe (docs only): a user-installed `post-checkout` hook that runs `codegraph init --yes` backgrounded with `|| true`, never `sync`. The installer never writes global git config.
- Dependency (A-004): freshness relies on the upstream watcher, which runs only while codegraph is registered and connected as an MCP server, a separate decision.

<!-- Source: Base modified — UNVERIFIED items from Changes 2, 3 and debate A-006 -->
## Pre-ship probes (UNVERIFIED)
1. Does `init --yes` repair a partial index? If not, run `codegraph index --force` when the DB exists without the marker.
2. Do two concurrent inits on one checkout fail cleanly with an intact index? If not, re-add a lock (PID file with a `kill -0` check).
3. Capture the exact MCP "not initialized" reply text.

<!-- Source: base-selection.md Combined Scoring; debate-transcript.md Convergence Assessment -->
## Evidence
- Scores: V1 0.756, V2 0.886, V3 0.736; margin 0.130, no tiebreaker. Convergence 100% (18/18, threshold 80%), depth quick, 1 round.
- Taken from losing options: V1 the no-sync rule, the docs page and cost disclosure, the A-003 completeness concern, and smallest code (no lock); V3 the opt-in `post-checkout` recipe, docs only.
- Rejected: V3 global `init.templateDir` and `sync` in git hooks; V1 no hook by default.
