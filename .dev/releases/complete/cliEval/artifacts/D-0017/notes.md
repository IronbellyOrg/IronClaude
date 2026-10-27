# D-0017 — Implementation notes

## Decisions

1. **Reuse `make verify-sync`; do not re-implement the diff in Python.**
   The Makefile target already covers the four scopes T01.20 cares
   about (`skills`, `agents`, `commands`, `hooks`), plus two derived
   cross-checks (`_FRESHNESS_SCRIPTS` installer registration, hooks.json
   ↔ auggie-flag-clear.sh prefix consistency). A parallel Python
   implementation would create a second source of "what counts as
   drift" — the kind of duplication AC11 itself argues against.

2. **`repo: local` over a forked upstream.** No public pre-commit hook
   reproduces this project's sync semantics, and the hook is one line
   of shell. A local definition is structurally simpler than packaging
   a hook repo just to host a single `make` call.

3. **`pass_filenames: false`.** Verify-sync's value is *whole-tree*
   diff; passing only the staged files would let an unstaged orphan
   `.claude/skills/foo/` survive each commit. The hook deliberately
   ignores `pre-commit`'s per-file pagination and runs the same target
   CI would.

4. **`files:` scope, not `always_run: true`.** A commit that only
   touches `tests/`, `docs/`, or the eval CLI tree should not pay the
   verify-sync cost. Constraining the trigger to the four synced
   directory roots keeps the hook unintrusive on the common case while
   still catching every cross-tree edit.

5. **No `language: python` runtime.** `language: system` reuses the
   host shell and `make`. The hook stays unaffected when the Python
   environment changes (e.g. when a contributor bumps Python or
   reinstalls `uv`); the same target runs identically in CI.

6. **No autofix.** A silent `make sync-dev` inside the hook would
   erase the contributor's intent — sometimes the edit belongs in
   `src/`, sometimes the `.claude/` change is the canonical fix being
   ported back. Surfacing the drift and letting the human pick the
   direction is the safer policy.

## Open follow-ups

* **CI wiring.** AC11 names `make verify-sync` as the canonical check;
  the GitHub Actions workflow (currently in flux on this branch) should
  invoke the same target in its lint stage. Tracked under OPS-001
  (R-021) and the AC11 closeout.
* **Pre-commit framework migration warning.** `pre-commit` emits a
  deprecation notice about `default_stages: [commit]` → `[pre-commit]`.
  Not a T01.20 concern, but worth migrating in a separate
  housekeeping pass; the local `verify-sync` hook is unaffected
  because it does not pin a stage.

## What was deliberately left out

* No new Python module under `scripts/`. The hook is a single
  `make verify-sync` invocation; adding a wrapper script would obscure
  the call site without adding behaviour.
* No automatic install of the pre-commit hooks on `make dev`. The
  framework already documents `pre-commit install` as an operator step;
  forcing it in `make dev` would surprise contributors who use a
  different workflow.
* No retroactive recheck of older commits. The hook gates *new*
  commits; historical drift, if any, surfaces the next time those
  files are touched and is repaired in that commit.
