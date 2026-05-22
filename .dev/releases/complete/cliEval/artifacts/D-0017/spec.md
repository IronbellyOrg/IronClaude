# D-0017 — AC11 source-of-truth discipline gate

**Task:** T01.20 (Phase 1, Roadmap AC11 / R-017)
**Surfaces:** `Makefile :: verify-sync`, `.pre-commit-config.yaml :: verify-sync`
**Status:** Wired 2026-05-20

## Purpose

AC11 codifies the project's source-of-truth rule for distributable
components: `src/superclaude/` is canonical, `.claude/` is a dev-time
mirror. Drift between the two — typically a `.claude/` edit that never
gets copied back to `src/`, or a `src/` edit committed without
`make sync-dev` — silently regresses the installer's view of the
framework. The gate must catch the drift at the commit boundary, before
it ships.

T01.20 wires two layers:

1. **`make verify-sync`** — the canonical diff command, already
   exhaustively detailed (see `Makefile:155-315`). It compares
   `src/superclaude/{skills,agents,commands,hooks}` against
   `.claude/{skills,agents,commands/sc,hooks}`, flags every
   `MISSING` / `DIFFERS` case, and exits 1 on any drift.
2. **A `verify-sync` pre-commit hook** that re-runs the same target
   whenever a commit touches a file in the synced scope. The hook
   rejects the commit if `make verify-sync` exits non-zero — i.e. it
   makes the AC11 rule structurally unforgeable on the commit path,
   not just a doc convention.

## Gate wiring

### `Makefile :: verify-sync`

Pre-existing in this branch; this task extended **no** behaviour — the
target already mirrors the four scopes T01.20 requires
(`skills`, `agents`, `commands`, `hooks`) plus the installer-registration
and hooks-cross-consistency cross-checks. The dependency from
T01.20 is "ensure the target exists, is correct, and exits 0 on a
synced tree." Verified by `evidence/T01.20/verify-sync-positive.log`.

### `.pre-commit-config.yaml :: verify-sync` (added by T01.20)

```yaml
- repo: local
  hooks:
    - id: verify-sync
      name: Verify src/superclaude/ ↔ .claude/ sync (AC11)
      entry: make verify-sync
      language: system
      pass_filenames: false
      files: '^(src/superclaude/(skills|agents|commands|hooks)|\.claude/(skills|agents|commands|hooks))/'
```

Design decisions:

| Choice | Why |
|---|---|
| `repo: local` (no upstream repo) | The check is project-specific and must call the project's own `Makefile`; no upstream provides this. |
| `language: system` | Reuses the host shell + `make` toolchain rather than a managed Python env, so the hook does not regress when project deps churn. |
| `pass_filenames: false` | `make verify-sync` operates on the whole tree, not a file list — passing filenames would force per-file invocations that miss cross-cut drift (e.g. a `.claude/foo` that has no `src/` counterpart at all). |
| `files: ^(src/superclaude/(...)\|\.claude/(...))/` | Triggers only when a file in the synced scope changes, so unrelated commits do not pay the verify-sync cost. The scope covers the same four kinds the Makefile checks. |

## Acceptance criteria → implementation map

| AC (T01.20) | Implementation site |
|---|---|
| Target `make verify-sync` exists in `Makefile` and exits 0 on a synced tree. | `Makefile:155-315`. Confirmed by `evidence/T01.20/verify-sync-positive.log` (exit 0 after `make sync-dev`). |
| Pre-commit hook rejects a synthetic commit that edits a `.claude/` file without touching the matching `src/superclaude/` source. | `.pre-commit-config.yaml` local hook above; `evidence/T01.20/pre-commit-negative.log` shows exit 1 with `DIFFERS: refactoring-expert.md` after a synthetic `.claude/` edit. |
| Pre-commit hook test fixture confirms a benign synced edit is allowed (positive case). | `evidence/T01.20/pre-commit-positive.log` shows the hook passing for a same-tree run after `make sync-dev`. |
| `TASKLIST_ROOT/artifacts/D-0017/spec.md` records the gate wiring. | This file. |

## Failure mode analysis

| Drift pattern | Caught by | Notes |
|---|---|---|
| Edit `.claude/skills/foo/SKILL.md`, no matching `src/` edit | `make verify-sync` → `DIFFERS: foo` | hook rejects commit |
| Add `.claude/agents/new.md`, no `src/` counterpart | `make verify-sync` → `MISSING in src/superclaude/agents/: new.md` | hook rejects commit |
| Add `src/superclaude/skills/bar/`, forget `make sync-dev` | `make verify-sync` → `MISSING in .claude/skills/: bar` | hook rejects commit |
| Edit `.claude/hooks/foo.sh`, no `src/` edit | `make verify-sync` → `DIFFERS: foo.sh` | hook rejects commit |
| Edit outside scope (e.g. `tests/…`, `docs/…`) | hook does not trigger | by design — `files:` filter |

## Caller contract / downstream consumers

* **Local dev loop.** `git commit` against a path inside the synced
  scope runs the hook automatically (once `pre-commit install` is in
  place). Operators with stale checkouts see the same rejection that CI
  would emit, before the bad state escapes.
* **CI.** Existing CI configuration (when AC11 is wired to GitHub
  Actions in a follow-up) reuses `make verify-sync` directly; the
  pre-commit hook is a local mirror of the CI check, not a replacement.
* **MIG-001 / T06.14.** The migration scaffolding lands the same
  source-of-truth contract for the new `cli/eval/` tree; this hook
  already covers the four scopes (`skills/agents/commands/hooks`) and
  needs no extension for `cli/eval/` because that path lives entirely
  under `src/` and has no `.claude/` mirror.

## Risk / scope notes

* The hook only triggers when files inside the four synced scopes
  change. A pure-test commit (`tests/…`) intentionally does not invoke
  verify-sync — Makefile-level CI invocations remain the authoritative
  enforcement for non-commit pathways.
* `make verify-sync` requires `uv` (it calls `uv run python` to read
  `_FRESHNESS_SCRIPTS`). Contributors without `uv` would see the hook
  fail with a different error; the project README already establishes
  `uv` as a prerequisite (see CLAUDE.md "Python Environment Rules").
* The hook does not implement automatic remediation. By design — a
  silent `make sync-dev` inside the hook would mask which side the
  contributor intended to be the source of the edit. The failure
  message in `make verify-sync` already tells the operator both
  remediation paths (`make sync-dev` to push src→.claude, or copy
  `.claude/` edits back to `src/`).

## Cross-references

* `Makefile:155-315` — `verify-sync` target (full diff/cross-check
  logic).
* `Makefile:109-152` — `sync-dev` target (the inverse direction).
* `.pre-commit-config.yaml` — hook registration.
* `CLAUDE.md` "Component Sync" — the project convention this gate
  enforces.
* Roadmap entries: AC11 (R-017 / row 17) and MIG-001 (carried into
  T06.14).
