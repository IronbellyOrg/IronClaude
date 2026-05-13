# D-0009 — `make eval-skill` Target Spec

**Task:** T03.03
**Roadmap Item:** R-009 (sourced from FR-L1.3)
**Deliverable:** A new `eval-skill` target in `/config/workspace/IronClaude/Makefile`.

## Interface

```
make eval-skill SKILL=<name>
```

## Behaviour

1. **Idempotent creation:** `mkdir -p .dev/eval-workspaces/<name>/` — no-op if the directory already exists, no error on re-run.
2. **Absolute path on stdout:** `realpath .dev/eval-workspaces/<name>` is printed as the sole stdout line so callers (humans, shell pipelines, plugin wrappers) can consume it as the workspace root.
3. **Unset-SKILL guard:** if `SKILL` is empty, the target prints `❌ Error: SKILL is unset. Usage: make eval-skill SKILL=<name>` to stderr and exits non-zero (`exit 1`, surfaced by `make` as exit 2).

## Acceptance Criteria (mirrored from phase-3-tasklist T03.03)

- `make eval-skill SKILL=__probe__` creates `.dev/eval-workspaces/__probe__/` and prints the absolute path on stdout; exit status 0.
- `make eval-skill` (without `SKILL`) exits non-zero with a clear error.
- Target is idempotent: running `make eval-skill SKILL=__probe__` twice does not error.
- Both outputs captured in `D-0009/evidence.md`.

## Files Touched

- `Makefile` — added `eval-skill` to `.PHONY`, added the target body, added a help-text line.

## Out of Scope

- Auto-generating `SKILL.md` stubs inside the workspace (skill-creator's job, not this target's).
- Removing existing workspaces (no-destructive-action principle).
- Cross-repo or absolute-`SKILL` paths (`SKILL` must be a plain skill name; path-traversal hardening is left to the hook in T03.01).
