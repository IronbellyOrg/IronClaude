<!-- Provenance: produced by /sc:brainstorm → /sc:adversarial (compare mode) -->
<!-- Base: Med-A=A-S1, Med-B=B-S1; graft: B-S2 doc clarification (U-004) -->
<!-- Convergence: 0.86 | 2026-06-04T03:42:06Z -->

# Merged Remediation Spec — PR #128 Medium Issues

**Target file:** `src/superclaude/cli/init_lite.py` (branch `feat/init-lite`, head `e55af621`)
**Scope:** Med-A + Med-B only. **M1 (atomic write) is already fixed — do not touch `_atomic_write`.**
**Safety contract (must remain intact):** `_is_protected_context_path`, `_is_init_lite_owned`, `--dry-run` writes nothing, `--force` scope-limited to `.dev/superclaude/`.

---

## Fix 1 — Med-A: fail fast on a nonexistent/non-directory `--project-root`

**Winning strategy: A-S1 (declarative Click validation).** Matches repo convention `sprint/commands.py:179,390`.

**Edit** — `init_lite.py` `--project-root` option (currently `:295`):

```python
# BEFORE
@click.option(
    "--project-root",
    "project_root",
    default=".",
    type=click.Path(file_okay=False, path_type=Path),
    help="Project directory to audit (default: current directory).",
)

# AFTER
@click.option(
    "--project-root",
    "project_root",
    default=".",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Project directory to audit (must be an existing directory; default: current directory).",
)
```

**Effect:** A nonexistent or file (non-dir) `--project-root` is rejected at parse time (exit code 2) before any body code runs — no audit, no `.dev/superclaude/` dirs created under a typo'd root. `default="."` always exists, so default behavior is unchanged.
**Invariant preserved (A-001):** an existing-but-empty project still succeeds with an empty audit — only nonexistent/non-dir roots are rejected.

---

## Fix 2 — Med-B: anchor relative `--output` to `--project-root`

**Winning strategy: B-S1 (anchor to root)** + **graft B-S2's doc clarification**.

**Edit 2a** — `out_path` computation (currently `:339`):

```python
# BEFORE
out_path = Path(output).resolve() if output else (root / REPORT_RELPATH)

# AFTER
if output is None:
    out_path = root / REPORT_RELPATH
else:
    out_path = (output if output.is_absolute() else (root / output)).resolve()
```

**Edit 2b** (graft U-004) — `--output` help text (currently `:303`):

```python
# BEFORE
    help="Report output path (default: <project-root>/.dev/superclaude/context-audit.md).",
# AFTER
    help="Report output path. Relative values resolve against --project-root "
         "(default: <project-root>/.dev/superclaude/context-audit.md).",
```

**Edit 2c** (graft U-004) — SKILL.md §4 (`src/superclaude/skills/sc-init-lite-protocol/SKILL.md`): add one line noting relative `--output` resolves against `--project-root`, not CWD. (Then `make sync-dev`, `make verify-sync` — SKILL.md is synced; the `.py` is not.)

**Effect:**
- Relative `--output` now lands under the audited project, not CWD.
- **Byte-identical** behavior when `--project-root` is default `.` (then `root == cwd.resolve()`).
- Absolute `--output` unaffected (`is_absolute()` branch).
- **Bonus (INV-004):** closes a latent divergence — with the old CWD-relative path, `_is_init_lite_owned(root, out_path)` (root-relative) could disagree with a CWD-relative `out_path`, misclassifying `--force` ownership when `root != cwd`. Anchoring couples them.

---

## Required tests (`tests/cli/test_init_lite.py`)

Also discharges review finding **L3** (`--output` / `--project-root` coverage gap).

1. **Med-A reject:** `--project-root <nonexistent>` → `result.exit_code != 0`; assert no `.dev/superclaude/` created. (CliRunner.)
2. **Med-A no over-reject (A-001 guard):** existing dir with zero SuperClaude surfaces → exit 0, report written, "No … surfaces found".
3. **Med-A non-dir reject:** `--project-root <path-to-a-file>` → nonzero exit.
4. **Med-B anchoring:** cwd = `tmp_b`, `--project-root tmp_a --output report.md` → file at `tmp_a/report.md`, **not** `tmp_b/report.md`.
5. **Med-B absolute unaffected:** absolute `--output` writes exactly there.
6. **Med-B default parity:** `--project-root .` default output path unchanged (regression guard).

## Acceptance criteria
- [ ] Both edits applied to `src/superclaude/cli/init_lite.py`; SKILL.md doc line added + synced.
- [ ] 6 new/updated tests pass.
- [ ] Full suite green: `uv run pytest tests/cli/test_init_lite.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py`.
- [ ] `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` clean.
- [ ] No change to protected-path / dry-run / force / scaffold invariants (existing tests still green).
- [ ] M1/`_atomic_write` untouched.

## Explicitly out of scope
- M1 atomic write (already fixed in `e55af621`).
- L1/L2/L4 + nit (symlink `is_symlink` guard, trust-boundary docstring, command-doc `--force` row) — separate follow-up; not part of this remediation.
- "Typo that resolves to a *different existing* directory" — semantically valid input; no existence check can catch it.
