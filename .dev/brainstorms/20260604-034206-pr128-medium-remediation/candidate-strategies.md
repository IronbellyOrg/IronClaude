# Candidate Remediation Strategies — PR #128 Medium Issues

Two strategies per open Medium issue. Each is a concrete, code-level option grounded
in `init_lite.py@e55af621` and existing repo conventions. These feed the adversarial
adjudication that selects the best per issue.

---

## Med-A — `--project-root` accepts nonexistent/typo'd paths (fail-fast needed)

### A-S1 — Declarative Click-layer validation (`exists=True, file_okay=False`)

**Mechanism**: Change the option type at `init_lite.py:295` from
`click.Path(file_okay=False, path_type=Path)` to
`click.Path(exists=True, file_okay=False, path_type=Path)`.

**Diff sketch**:
```python
@click.option(
    "--project-root", "project_root", default=".",
    type=click.Path(exists=True, file_okay=False, path_type=Path),  # was: file_okay=False
    help="Project directory to audit (default: current directory).",
)
```

**Pros**:
- Exactly matches the repo's established pattern (`sprint/commands.py:179,390`).
- Zero command-body code; Click emits a standard usage error + nonzero exit for free.
- `default="."` always exists, so default behavior is unaffected.
- One-line change; minimal review surface.

**Cons**:
- Click's error message is generic (`Directory '<x>' does not exist.`) — not branded.
- Validation is harder to unit-test in isolation (requires `CliRunner` invocation,
  which the suite already uses, so low cost in practice).
- Couples the "must exist" semantic to the CLI boundary only; a future programmatic
  caller of an extracted helper wouldn't get the guard.

### A-S2 — Imperative body check with branded `ClickException`

**Mechanism**: Keep the option type, add an explicit guard right after `:335`.

**Diff sketch**:
```python
root = Path(project_root).resolve()
if not root.is_dir():
    raise click.ClickException(
        f"--project-root {project_root} is not an existing directory; "
        f"refusing to audit a nonexistent path."
    )
```

**Pros**:
- Custom, on-brand error message consistent with the module's other
  `ClickException`s (`:248,258`).
- Guard lives in code → unit-testable directly; can also protect a future
  extracted `run_audit(root)` helper.
- Catches the post-`resolve()` reality (symlink-to-file, race) rather than the
  pre-resolution string.

**Cons**:
- More lines than A-S1; duplicates a guard Click can express declaratively.
- Diverges from the declarative `exists=True` convention used elsewhere.
- Slightly later failure (after `resolve()`), though still before any write.

---

## Med-B — relative `--output` resolved against CWD, not `--project-root`

### B-S1 — Anchor relative `--output` to `root` (least-surprise, behavior change)

**Mechanism**: Interpret a relative `--output` relative to the resolved project root
at `init_lite.py:339`.

**Diff sketch**:
```python
if output is None:
    out_path = root / REPORT_RELPATH
else:
    out_path = output if output.is_absolute() else (root / output)
    out_path = out_path.resolve()
```

**Pros**:
- Makes `--project-root` and `--output` consistent — directly resolves the finding.
- Matches the mental model: "everything is relative to the project I'm auditing."
- Absolute `--output` is unaffected; default path unaffected.

**Cons**:
- **Behavior change**: any existing caller relying on CWD-relative `--output`
  (e.g. a script run from repo root auditing the same repo) would see the file move
  — though when `--project-root` is default `.`, `root == CWD` so the resolved path
  is identical, making real-world breakage unlikely.
- Must be regression-tested for both the `--project-root == cwd` and `!= cwd` cases.

### B-S2 — Preserve CWD semantics, add transparency + docs (no behavior change)

**Mechanism**: Keep `Path(output).resolve()` (CWD-relative) but always echo the
fully-resolved absolute destination, and document the CWD-relative semantics in the
`--output` help + SKILL.md.

**Diff sketch**:
```python
out_path = Path(output).resolve() if output else (root / REPORT_RELPATH)
...
# already prints: click.echo(f"Context audit written to {out_path}")  # now always absolute
```
Plus help text: `"Report output path. Relative values resolve against the current
working directory, not --project-root."`

**Pros**:
- Zero behavioral risk — no existing invocation changes where it writes.
- The existing `click.echo(f"Context audit written to {out_path}")` (`:349`) already
  surfaces the absolute path; the fix is mostly making the contract explicit.
- Smallest blast radius.

**Cons**:
- Doesn't actually remove the inconsistency the finding flags — it documents it.
  A reviewer could argue the surprise remains for anyone who doesn't read the echo.
- Two surfaces to keep in sync (help text + SKILL.md) vs. one code path.

---

## Decision axes for adversarial adjudication

1. **Least-surprise vs. backward-compat** (sharpest on Med-B: S1 changes behavior, S2 documents it).
2. **Declarative-at-boundary vs. imperative-in-body** (Med-A: S1 convention-match vs. S2 testability/branding).
3. **Test cost** — both issues need new coverage regardless (ties into review finding L3).
4. **Blast radius / review surface** — A-S1 and B-S2 are the smallest; A-S2 and B-S1 are more thorough.
