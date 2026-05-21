# Code Review: diff origin/master...HEAD (branch `fix/prd-path-resolution-and-templates`)

**Target**: local diff `origin/master...HEAD`
**Reviewer**: /sc:auggie-review (depth=quick, focus=quality,anti-patterns,architecture)
**Generated**: 2026-05-20 17:44 UTC
**Source PR**: (none — local diff)
**Base ↔ Head**: `2219545` ↔ `6a7a0dc`
**Stats**: 40 files, 9370 insertions / 130 deletions, **3 findings kept (2 dropped during grounding)**, **4 cross-cutting observations**

---

## Summary

The branch (1) anchors PRD CLI path resolution to `.claude/`, (2) migrates workflow and document templates into `src/superclaude/templates/` as a single source of truth synced to `.claude/templates/`, and (3) adds a new `install_templates.py` CLI module wired into `superclaude install`. The architectural moves are sound and consistent with existing patterns (CC3, CC4). The bulk of inserted lines are template `.md` content, not executable code.

Top concerns from the executable surface:
1. **CC1 / F1**: `install_templates.py` propagates the existing `except Exception` anti-pattern across all four installers — the diff adds a fourth instance rather than tightening the pattern.
2. **CC2**: Four near-identical `_get_*_source()` resolution helpers now exist; this PR adds a fourth without extracting the shared shape.

No Critical or High findings. **Recommendation: approve with comments** (Medium follow-ups worth a separate cleanup ticket; no merge blockers).

## Findings

### Critical (block merge)

_None._

### High (should fix before merge)

_None._

### Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. Broad exception handler in `install_templates.py` masks programming errors
- **File**: `src/superclaude/cli/install_templates.py:78`
- **Category**: error-handling / anti-pattern
- **Source**: auggie
- **Evidence**:
  ```python
  try:
      dest.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(src_file, dest)
      installed.append(str(rel))
  except Exception as exc:  # noqa: BLE001 — surface any IO failure
      failed.append(f"{rel}: {exc}")
  ```
- **Why this matters**: The `BLE001` noqa is justified as "surface any IO failure", but `Exception` catches programming bugs too (`AttributeError`, `TypeError`, `KeyError`). When the install path is partially configured (e.g. a refactor introduces a typo in the relative-path computation), this swallow-and-log loop hides the failure as "file failed to install" rather than crashing fast. The other three installers (`install_agents.py:58`, `install_core.py:58`, `install_commands.py:59`) already exhibit the same pattern, so this PR doesn't introduce the anti-pattern — but it does propagate it (see CC1).
- **Recommendation**: Narrow to expected IO failures: `except (PermissionError, OSError) as exc:` (FileNotFoundError and IOError are subclasses of OSError in Python 3). Remove the BLE001 noqa. If the install path needs to keep running through unrelated bugs, log them via a second `except Exception` branch that re-raises after collecting a count.

### Low (nice-to-have)

#### L1. Missing dedicated unit tests for `install_templates.py` core functionality
- **File**: `tests/cli/test_install_failures.py:1` (and absence of `tests/cli/test_install_templates.py`)
- **Category**: tests
- **Source**: auggie
- **Evidence**: New regression test `test_install_failures.py` covers only the shared "`not failed`" guard fix across four installers. No tests exist for `install_templates.py`-specific behaviour: source discovery (editable vs. wheel layout in `_get_templates_source()`), subdirectory preservation, `_PROTECTED_TARGET_SUBDIRS` rejection, or `list_available_templates()` / `list_installed_templates()` accuracy.
- **Why this matters**: The PR adds a complete new install pipeline (`install_templates`) that mirrors three existing ones. Without dedicated tests, future packaging changes (editable → wheel layout shifts, force-include path tweaks) can silently break only this module. Downgraded from Medium because the same coverage gap exists for the three sibling installers — this is a pre-existing pattern, not a regression introduced by this PR.
- **Recommendation**: Add `tests/cli/test_install_templates.py` covering: (a) `_get_templates_source()` resolution for both editable and wheel layouts, (b) subdirectory structure preservation (`workflow/`, `documents/`), (c) `_PROTECTED_TARGET_SUBDIRS` rejection guard, (d) listing accuracy. Follow the monkeypatch / `Path.home` isolation pattern already established in `tests/cli/prd/test_path_resolution.py`.

#### L2. Double `Path.relative_to()` computation in `list_available_templates` and `list_installed_templates`
- **File**: `src/superclaude/cli/install_templates.py:136-142` (and `:150-156`)
- **Category**: correctness / efficiency
- **Source**: auggie
- **Evidence**:
  ```python
  return sorted(
      str(f.relative_to(source))
      for f in source.rglob("*")
      if f.is_file()
      and "__pycache__" not in f.parts
      and not any(p in _PROTECTED_TARGET_SUBDIRS for p in f.relative_to(source).parts)
  )
  ```
- **Why this matters**: `f.relative_to(source)` is computed twice per file. In the (currently absent) presence of a symlink that escapes the source tree, `relative_to()` raises `ValueError`. The probability is low for `src/superclaude/templates/` (verified via `find -type l`: no symlinks today), so this is more about defensive coding and a small efficiency win than a real bug. Auggie self-marked confidence as "low" — confirmed.
- **Recommendation**: Bind the relative path once in a generator-`if` chain or extract a helper:
  ```python
  def _walk_templates(root: Path) -> Iterator[Path]:
      for f in root.rglob("*"):
          if not f.is_file():
              continue
          try:
              rel = f.relative_to(root)
          except ValueError:
              continue
          if "__pycache__" in rel.parts:
              continue
          if any(p in _PROTECTED_TARGET_SUBDIRS for p in rel.parts):
              continue
          yield rel
  ```
  Apply to both `list_available_templates` and `list_installed_templates`.

### Nits

_None worth surfacing; ruff is configured and will catch style issues._

## Architectural / Cross-Cutting Observations

### CC1. Broad-exception anti-pattern is now in all four installers (diff makes it worse)
- **Category**: anti-pattern
- **Severity**: Medium
- **Affected files**: `src/superclaude/cli/install_templates.py:78`, `src/superclaude/cli/install_agents.py:58`, `src/superclaude/cli/install_core.py:58`, `src/superclaude/cli/install_commands.py:59`
- **Why this matters**: All four installers wrap `shutil.copy2()` with `except Exception` (only `install_templates.py` has a noqa with a rationale). The PR adds the fourth instance rather than tightening the pattern across the board. Code-quality cost: programming bugs are surfaced as "file failed to install" messages, hiding the actual stack trace.
- **Recommendation**: Standardize to `except (PermissionError, OSError) as exc:` across all four installers in a follow-up. If a noqa is unavoidable, it should reference the specific IO concern, not justify catching everything. File as a refactor ticket rather than blocking this PR.

### CC2. Path-resolution helpers are duplicated four times (`_get_*_source()`)
- **Category**: architecture
- **Severity**: Medium
- **Affected files**: `src/superclaude/cli/install_templates.py:106-128`, `src/superclaude/cli/install_agents.py:89+`, `src/superclaude/cli/install_commands.py:92+`, `src/superclaude/cli/install_core.py:89+`
- **Why this matters**: Each installer module has its own `_get_<thing>_source()` function with near-identical resolution logic (editable vs. wheel layout). The PR adds a fourth instance. The subtle differences (e.g. `install_templates._get_templates_source()` checks `package_root / "_src" / "superclaude" / "templates"` for the wheel layout, while others may not) create a maintenance trap when packaging changes (e.g. switching from `[tool.hatch.build.force-include]` to a different layout strategy).
- **Recommendation**: Extract a shared helper into `src/superclaude/cli/_paths.py`:
  ```python
  def package_resource_dir(name: str) -> Path:
      """Resolve a package subdirectory for both editable and wheel layouts."""
      here = Path(__file__).resolve()
      package_root = here.parent.parent  # .../superclaude/
      editable = package_root / name
      if editable.is_dir():
          return editable
      wheel = package_root / "_src" / "superclaude" / name
      return wheel if wheel.is_dir() else editable
  ```
  Each installer becomes a one-liner: `source = package_resource_dir("templates")`. Defer to a follow-up to avoid expanding this PR's scope.

### CC3. Source-of-truth layering correctly enforced for templates (positive)
- **Category**: architecture (positive)
- **Severity**: informational
- **Affected files**: `src/superclaude/templates/workflow/05_prd_template.md`, `.claude/templates/workflow/05_prd_template.md`, `Makefile`
- **Why this matters**: The diff correctly implements the SoT rule documented in `CLAUDE.md`: `src/superclaude/templates/` is canonical, `.claude/templates/` is the dev copy synced via `make sync-dev`, and `make verify-sync` enforces drift detection. The Makefile additions follow the same pattern already used for `skills/` and `agents/`. This is the right way to add a new component family.
- **Recommendation**: No change required. Consider a brief Makefile comment explaining any intentional exclusion patterns (e.g. `*.legacy-rf-project.md`) so future maintainers don't accidentally remove them.

### CC4. PRD path resolution correctly migrated to `.claude/`-anchored lookups (positive)
- **Category**: architecture (positive)
- **Severity**: informational
- **Affected files**: `src/superclaude/cli/prd/models.py:38-83`, `src/superclaude/cli/prd/config.py`, `tests/cli/prd/test_path_resolution.py`
- **Why this matters**: `_default_skill_refs_dir()` (models.py:38) and `_default_template_path()` (models.py:66) implement a three-candidate fallback (cwd `.claude/`, home `.claude/`, dev-tree) and always return an absolute path even on total miss — which gives users an inspectable path in the eventual `FileNotFoundError` message. The 204-line `test_path_resolution.py` locks the behaviour in with parametrized coverage.
- **Recommendation**: No change required. The pattern is the cleanest helper in the diff and should be the model for any future resource-discovery code (see CC2).

## Audit

- **Auggie chunks**: 1 (succeeded: 1, retried: 0, skipped: 0)
- **Raw findings from Auggie**: 5 findings + 4 cross-cutting observations
- **Findings dropped during grounding**: 2
  - F2 ("Inconsistent 'failed' handling guard"): dropped — finding was factually inverted. The `test_install_failures.py` docstring at lines 7-10 explicitly states `install_skills.py` is the precedent the four other installers were aligned to; Auggie misread the direction of the consistency claim.
  - F5 ("install_templates not registered in pyproject.toml entry points"): dropped — incorrect premise. No installer module has its own entry point; all subcommands hang off `@main.command()` decorators in `main.py`. The recommendation for a standalone `superclaude templates` subcommand is speculative architecture, not a missing convention.
- **Findings kept**: 3 (1 Medium, 2 Low)
- **Cross-cutting kept**: 4 (CC1 Medium, CC2 Medium, CC3 + CC4 positive/informational)
- **Persona cross-check**: disabled (depth=quick)
- **Token cost**: Claude ≈ 6k orchestration; Auggie ≈ 8k retrieval
- **Audit log**: `/tmp/eval-diff-iter2/audit.log`

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: partial
critical: 0 high: 0 medium: 1 low: 2 nit: 0
dropped: 2
auggie_chunks: 1
duration_sec: 90
-->
