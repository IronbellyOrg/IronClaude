---
topic: "Remediate 2 open Medium issues in PR #128 init_lite.py (head e55af621)"
domain: code
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-06-04T03:42:06Z
source_pr: https://github.com/IronbellyOrg/IronClaude/pull/128
head_commit: e55af6217129be1527a2e1f9da449cf0be5106be
file_under_change: src/superclaude/cli/init_lite.py
---

# Seed Brief: PR #128 Medium-Issue Remediation

## Problem Statement

`superclaude init-lite --context-optimized` has two valid, currently-open Medium
findings in `src/superclaude/cli/init_lite.py` at branch head `e55af621`. Both are
path-input handling defects that violate the principle of least surprise. Neither is
externally exploitable (single-user local dev CLI), but both make the "audit"
behavior silently wrong under operator error.

A third finding (M1, non-atomic `write_text` / TOCTOU) was already remediated in
commit `e55af621` via `_atomic_write` (tempfile + `os.replace`, used at `:264` and
`:278`) — **explicitly out of scope**.

## Known Context (verified against live code at e55af621)

- **Med-A** — `--project-root` (`:291-297`) uses `click.Path(file_okay=False, path_type=Path)`.
  `file_okay=False` rejects an *existing file*, but does **not** require existence
  (`exists` defaults False). `:335` `root = Path(project_root).resolve()` therefore
  accepts a nonexistent/typo'd directory. `discover_surfaces(root)` then finds nothing,
  `render_report` emits a "No surfaces found" report, and `_write_report` creates
  `<typo-root>/.dev/superclaude/context-audit.md` — directories materialized under the
  wrong root, with zero error signal. Audit silently lies.

- **Med-B** — `--output` (`:298-304`) uses `click.Path(dir_okay=False, path_type=Path)`
  with no `resolve_path`. `:339` `out_path = Path(output).resolve() if output else (root / REPORT_RELPATH)`.
  `Path.resolve()` on a *relative* value anchors to **CWD**, not `root`. So
  `--project-root /other/proj --output report.md` writes to `$CWD/report.md`, not
  `/other/proj/report.md`. Inconsistent with the `--project-root` framing; default
  (no `--output`) is correctly root-anchored, which makes the relative-override the
  sole surprising path.

## Repo Conventions (grounding for strategies)

- Idiomatic fail-fast for a must-exist directory input: `click.Path(exists=True, file_okay=False, path_type=Path)`
  — used verbatim at `src/superclaude/cli/sprint/commands.py:179` and `:390`.
- Output paths that need not pre-exist: `click.Path(exists=False, path_type=Path)`
  — `src/superclaude/cli/roadmap/commands.py:105`.
- `click.ClickException` is the established user-error surface in this module
  (`init_lite.py:248,258`).

## Constraints

- Read-only safety invariants on context inputs must be preserved untouched
  (`_is_protected_context_path`, `_is_init_lite_owned`, `--dry-run` writes nothing).
- Must not regress the 17 existing tests in `tests/cli/test_init_lite.py`.
- Fix must follow repo convention (SoT: edit `src/superclaude/`, then `make sync-dev` — though init_lite is CLI code, not a synced skill/agent/command, so no sync needed for the `.py`).
- Scope discipline: change only what the two findings require; no speculative additions.
- New behavior must be covered by tests (the review's L3 noted a test gap in this area).

## Success Criteria

- Med-A: a nonexistent/non-directory `--project-root` fails fast with a clear message
  and writes nothing.
- Med-B: a relative `--output` resolves predictably and consistently with `--project-root`
  (or its CWD-relative semantics are made explicit and visible) — no silent misplacement.
- Both behaviors are regression-tested.
- No change to protected-path / dry-run / force / scaffold invariants.

## Open Questions

- Med-B: change behavior (anchor relative output to root) vs. preserve behavior
  (keep CWD-relative, add transparency)? Backward-compat vs. least-surprise tension.
- Validate in the Click type layer (declarative, free `--help`/usage errors) vs. in
  the command body (custom messages, unit-testable without CliRunner)?
