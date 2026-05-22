# Code Review: diff origin/master...HEAD (fix/prd-path-resolution-and-templates)

**Target**: local diff (origin/master...HEAD)
**Reviewer**: /sc:auggie-review (depth=quick, focus=quality,anti-patterns,architecture)
**Generated**: 2026-05-20 (local eval)
**Source PR**: n/a (local branch eval)
**Base ↔ Head**: origin/master ↔ HEAD (1150b41)
**Stats**: 36 files, 9269 insertions / 128 deletions, 5 file-level findings + 2 cross-cutting (0 dropped during grounding)

---

## Summary

Branch `fix/prd-path-resolution-and-templates` does two things: (1) anchors the PRD CLI's path resolution to `.claude/` and (2) migrates the canonical template tree from `.claude/templates/` into `src/superclaude/templates/` (Source-of-Truth), with a new `install_templates` CLI command and 200+ lines of new tests. The bulk of the diff (~9000 lines) is static markdown template content, not executable code. The code surface is small (`install_templates.py`, a registration in `main.py`, small edits to `prd/config.py` and `prd/models.py`) and is generally consistent with the existing install-* module conventions. One real correctness gap stands out: the `update` command was not updated to install templates alongside core/commands/agents/skills — operators running `superclaude update` will silently fall behind. Recommendation: **approve with comments** — fix the `update`-command omission, add a smoke test for `install_templates`, and merge.

## Findings

### 🔴 Critical (block merge)

_None._

### 🟠 High (should fix before merge)

_None._

### 🟡 Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. `update` command does not install templates
- **File**: `src/superclaude/cli/main.py:309`
- **Category**: correctness (api-contract drift)
- **Source**: auggie
- **In diff**: false (the un-updated lines are pre-existing in main.py; the diff added the templates step to `install` at line 201 but not to `update`)
- **Evidence**:
  ```python
  # main.py:309 (inside the `update` command)
  if not core_success or not cmd_success or not agent_success or not skill_success:
      sys.exit(1)
  ```
- **Why this matters**: The full `install` flow (main.py line 201) now does `install_templates(force=force)` as a peer of core/commands/agents/skills. The sibling `update` command (lines 268–310) imports `install_core`, `install_commands`, `install_agents`, `install_all_skills` — but not `install_templates` — and its success-check on line 309 does not include `templates_success`. Operators running `superclaude update` after this release will have stale (or absent) templates while every other distributable is current, which silently breaks PRD/MDTM pipelines that depend on the templates being present and current.
- **Recommendation**: Add `from .install_templates import install_templates`, call it after the skills step with `force=True`, capture `templates_success`, and include it in the line-309 disjunction. Add a smoke test in `tests/cli/test_install_failures.py` (or a new `test_install_templates.py`) that asserts `update` actually installs the template tree.

#### M2. No unit test for the new `install_templates` module
- **File**: `src/superclaude/cli/install_templates.py:1` (whole-file scope)
- **Category**: tests
- **Source**: auggie
- **In diff**: true (new file)
- **Evidence**: `tests/cli/` contains `test_install_failures.py` and `test_install_hooks.py` but no `test_install_templates.py`. `tests/cli/prd/test_path_resolution.py` (also added by this branch) covers PRD path resolution, not the new installer.
- **Why this matters**: The new installer does non-trivial work — two-layout source discovery (editable vs. wheel `_src` layout), `_PROTECTED_TARGET_SUBDIRS` filtering, force-vs-skip semantics, success/skip/fail aggregation. The wheel-layout branch in `_get_templates_source` (lines 122–124) in particular is hard to exercise without a test because most contributors only run editable installs. A regression that hides templates from pipx users would surface only in production.
- **Recommendation**: Add `tests/cli/test_install_templates.py` covering: (a) editable-layout discovery, (b) wheel-layout discovery via a tmp-path fixture that mocks `_src/superclaude/templates`, (c) `force=False` skipping existing files, (d) `force=True` overwriting, (e) `agent-memory/` in the source tree being filtered out, (f) empty-source-directory returning `(False, "...")`.

### 🟢 Low (nice-to-have)

#### L1. Broad `except Exception` in copy loop
- **File**: `src/superclaude/cli/install_templates.py:78`
- **Category**: error-handling
- **Source**: auggie
- **In diff**: true
- **Evidence**:
  ```python
  try:
      dest.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(src_file, dest)
      installed.append(str(rel))
  except Exception as exc:  # noqa: BLE001 — surface any IO failure
      failed.append(f"{rel}: {exc}")
  ```
- **Why this matters**: Catching `Exception` here is intentional — the comment and the `noqa` make that explicit, and the `failed` list surfaces the per-file failure to the user. However, swallowing `KeyboardInterrupt`/`SystemExit` is avoided (those don't inherit `Exception`) and the failure mode is bounded, so the risk is small. Worth noting only because a future maintainer might tighten this to `OSError` for clearer intent.
- **Recommendation**: Optional — narrow to `(OSError, shutil.Error)` if you want to surface unknown errors as crashes instead of accumulating them. Either choice is defensible; current behavior is documented.

### 💬 Nits

- `_PROTECTED_TARGET_SUBDIRS` membership check (`any(p in _PROTECTED_TARGET_SUBDIRS for p in rel.parts)`) appears verbatim at install_templates.py:67, :141, and :155. Consider extracting `_is_protected(rel: Path) -> bool` for a single source of truth. Cost: ~3 lines, low value.

## Architectural / Cross-Cutting Observations

### X1. Two source-resolution patterns coexist across install-* modules
- **Category**: architecture (consistency)
- **Affected files**: `src/superclaude/cli/install_templates.py:106-128`, `src/superclaude/cli/install_agents.py:89-108`, `src/superclaude/cli/install_commands.py:92-115`, `src/superclaude/cli/install_core.py:89-110`, `src/superclaude/cli/install_skill.py:58-90`, `src/superclaude/cli/install_hooks.py:462-525`
- **Source**: auggie + claude (validated against repo)
- **Why this matters**: `install_templates._get_templates_source` is the **only** install module that explicitly handles both the editable layout AND the pipx/wheel `_src/superclaude/<sub>` layout. `install_agents._get_agents_source` checks only `package_root/agents` and returns the same path on miss; `install_core`, `install_commands`, and `install_skill` follow the same single-layout pattern. The wheel force-include at `pyproject.toml:79-80` (`"src" = "superclaude/_src"`) means the OTHER install modules likely **also** need the `_src` fallback for pipx users — install_templates may be the first to surface a latent issue that affects the whole module family. (Note: this is a cross-cutting observation, not a finding against this diff. The diff is consistent with itself; the wider inconsistency pre-exists.)
- **Recommendation**: Either (a) backport the two-layout discovery from `install_templates._get_templates_source` into a shared helper (`_resolve_package_subdir(name: str) -> Path`) used by every install_* module, or (b) confirm via a pipx install smoke test that the single-layout install modules actually work for wheel installs and document the assumption. Track as a separate task; do not block this PR.

### X2. Install module family follows consistent (success, message) tuple return shape
- **Category**: architecture (positive consistency)
- **Affected files**: every `install_*.py` in `src/superclaude/cli/`
- **Source**: auggie + claude (validated)
- **Why this matters**: `install_templates` correctly mirrors the `Tuple[bool, str]` return contract, emoji-decorated message blocks, and `installed/skipped/failed` accounting used by `install_agents`, `install_commands`, `install_core`, etc. This is consistency worth preserving — any new install module added in the future should use this same shape, and the four `_success / _message` assignments in main.py's `install` command pivot on it.
- **Recommendation**: No action required. Capture this convention in a brief docstring on the `cli/` package or a `CONTRIBUTING.md` snippet so future contributors do not invent a third shape.

## Audit

- Auggie chunks: 1 (succeeded: 1, retried: 0, skipped: 0)
- Auggie wall-clock: ~107s
- Findings raw from Auggie: 5 file-level + 2 cross-cutting
- Findings dropped during grounding: 0
- Findings severity-remapped:
  - F1 (`severity_hint=medium`, category=correctness, in_diff=false on the un-updated `update` lines but logically required by the diff's other half) → kept at **Medium** (correctness ceiling applies; not default-path crash, but pipelines silently degrade)
  - F2 (`severity_hint=low`, category=architecture, "plugins fallback missing") → **dropped as misframed** — the claim is that `install_templates` is missing a fallback that other install_* modules have; in fact the opposite is true (install_templates has MORE robust two-layout discovery than `install_agents`/`install_commands`/`install_core`). The underlying observation that the install_* family is inconsistent IS real and is captured as cross-cutting X1 instead.
  - F3 (`severity_hint=medium`, category=tests, confidence=high) → kept at **Medium** (test-floor for new install module)
  - F4 (`severity_hint=low`, category=error-handling, confidence=medium) → kept at **Low** (intentional broad except with `noqa` justification)
  - F5 (`severity_hint=nit`, category=naming) → kept at **Nit** (the underlying observation is real but low-value; constant name itself is fine, the duplicated membership check is the nit)
- Cross-source agreement bonus: n/a (depth=quick, single Auggie pass)
- Token cost: Claude ≈ 4k orchestration, Auggie ≈ ~10k (single pass)

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 0 medium: 2 low: 1 nit: 1
dropped: 1
auggie_chunks: 1
duration_sec: 107
-->
