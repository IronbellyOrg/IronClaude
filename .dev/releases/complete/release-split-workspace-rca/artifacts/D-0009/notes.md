# D-0009 — Implementation Notes

## Insertion site

Placed the target between `lint-architecture` and `help` so it sits in the developer-convenience block. This keeps it lexically near `sync-dev` / `verify-sync` (the other quality-of-life targets) and lets the `help` section list it adjacent to the architecture lint output.

## Recipe shape

```makefile
eval-skill:
	@if [ -z "$(SKILL)" ]; then \
		echo "❌ Error: SKILL is unset. Usage: make eval-skill SKILL=<name>" >&2; \
		exit 1; \
	fi
	@mkdir -p .dev/eval-workspaces/$(SKILL)
	@realpath .dev/eval-workspaces/$(SKILL)
```

- `@` prefixes suppress recipe echoing so stdout is exactly the `realpath` line — important for downstream callers that consume it.
- The unset guard uses `[ -z "$(SKILL)" ]`. Make expands `$(SKILL)` to the empty string when undefined; the shell test catches that. `>&2` keeps the error message off stdout (so a pipeline reading stdout for the path doesn't see the error).
- `mkdir -p` is the idempotence mechanism — POSIX guarantees no error when the directory already exists.

## Why this is operationally hardened beyond literal D3.3

The phase file's "Notes" call out that the unset-SKILL error is hardening beyond R-009's literal scope: a silent no-op would create a confusing failure mode where `mkdir -p .dev/eval-workspaces/` (the parent) succeeds and `realpath` of the parent prints, hiding the bug. The guard is cheap insurance.

## What I deliberately did NOT add

- No `SKILL` regex validation (e.g. rejecting `../foo`). The PreToolUse hook (T03.01) and `.gitignore` (T01.x) are the authoritative defences; adding regex here would duplicate enforcement and could disagree with the hook over time.
- No success-message decoration. `realpath` alone is the contract.
- No removal of the probe directory inside the target — that's the verification step's responsibility, not the target's.

## Cross-task interactions

- **T03.01 (PreToolUse hook):** The target lands writes in the *permitted* destination, so the hook never fires for this codepath. Verified indirectly — `make eval-skill SKILL=__probe__` succeeded under `bypassPermissions` mode and no hook rejection occurred.
- **T03.02 (CLAUDE.md addendum):** The addendum (already present per Phase 3 progress) references `.dev/eval-workspaces/<skill-name>/` as the destination; this target makes that destination trivially reachable via a single command.
- **T01.01 (`.dev/README.md`):** No coupling at the Makefile level. The README documents the convention; the target enforces it operationally.

## Verification approach

Ran three invocations in sequence: positive (creates + prints absolute path), idempotent re-run (re-prints same path, exit 0), unset-SKILL (stderr message, non-zero exit). All captured in `evidence.md`.
