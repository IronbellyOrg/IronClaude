# D-0015 — implementation notes

## Decisions made during build

1. **Why `uv pip list` instead of parsing `pyproject.toml`.** AC3 names
   `pexpect` explicitly even though it is purely transitive (via vendored
   `ptytest`). Parsing `[project.dependencies]` would never see `pexpect`
   because it is not a direct dep, so the check would silently pass even if
   ptytest brought in pexpect ≥ N versions. `uv pip list` captures the
   actual installed surface, which is what AC3 is constraining.

2. **Allow-list as a committed file (`scripts/dependency_baseline.txt`)
   rather than a Python constant.** The list moves through PR review when a
   real dep change happens. Putting it in a Python constant would conflate
   "policy data" with "policy logic" — the spec wants the data to be the
   diffable artefact.

3. **Name-only comparison (versions ignored).** Pinning versions in the
   baseline would mean every minor `pytest` bump fails CI, which is noise.
   AC3 is a *boundary* check, not a *lockfile*; the dependency-lock concern
   is a separate, future-roadmap item.

4. **PEP 503 normalisation.** Both `uv pip list` and source-of-truth lists
   can drift on `_` vs `-` and casing. Normalising (`lower()` +
   `replace('_','-')`) makes the check stable across upstream metadata
   renames.

5. **Removals do not fail.** Allow-list is treated as an upper bound, not an
   equality check. A dev tool can be dropped without ceremony; only
   additions are the AC3 concern.

6. **`ptyprocess` pre-added to allow-list.** `pexpect` requires `ptyprocess`
   at runtime, so AC3's explicit `pexpect` allowance implicitly carries
   `ptyprocess`. Pre-adding it avoids a CI surprise when the ptytest vendor
   drop lands in Phase 2.

7. **`superclaude` itself in the baseline.** The editable install registers
   `superclaude` as a top-level package, so it appears in `uv pip list`. It
   stays in the baseline so the check passes today.

8. **`jsonschema` not separately re-listed in the AC3-additions block.** It
   is already a direct dep in `pyproject.toml` and thus in the pre-eval-CLI
   baseline snapshot. AC3's mention of `jsonschema` is to clarify that its
   retention is approved, not that it is a new addition.

9. **Separate CI job rather than a step in `test`.** Keeps the green/red
   signal isolated so a dep-boundary breach reads as such in the run page,
   not as "tests failed". The job is added to `test-summary`'s `needs:`
   list so the umbrella status reflects it.

10. **No matrix for the CI job.** The Python-version axis is not relevant
    to the allow-list comparison — the installed set is determined by
    `pyproject.toml`, not the interpreter version. Running once on 3.10
    matches the `lint` job's pattern.

11. **Exit code 2 reserved for tooling errors.** `uv` missing or baseline
    file missing returns 2 (matches the FR-SCH2 convention used by the
    eval CLI loader). Exit 1 is the actual AC3 violation. Exit 0 is the
    happy path.

## Things deliberately NOT in scope of T01.17

- A `uv.lock` / pinned lockfile gate — AC3 is name-only.
- Detecting removed dev tools — not an AC3 concern.
- Auto-updating the baseline — that would defeat the PR-review purpose.
- Wiring `pexpect` into `pyproject.toml` — Phase 2 (ptytest vendor) owns it.
- Enforcing the allow-list at `uv pip install` time (pre-install hook) — CI
  gate is sufficient per the EXEMPT tier classification (Section 5.3).

## Risks observed during build

- **Baseline drift after upstream wheels rename a package.** PEP 503
  normalisation handles the common case (`_` ↔ `-`, casing), but a wholesale
  rename (e.g., `pyyaml` → `yaml`) would fail until the baseline is updated.
  This is a feature: such renames should be reviewed, not silently absorbed.

- **`uv` not on PATH in some dev environments.** Exit 2 with a clear error
  message means the dev sees the cause; CI installs `uv` explicitly via the
  existing UV install step.

- **Editable installs of sibling projects** (e.g., a contributor running
  `uv pip install -e ../neighbour` into the venv) would inject packages
  that fail the check. This is the intended behaviour — `make verify-deps`
  represents the *committed* dependency surface, not a contributor's local
  experimentation.

## CI behaviour summary

```
test-summary
├── test          (matrix: 3.10, 3.11, 3.12)
├── lint
├── plugin-check
├── doctor-check
└── verify-deps   ← new (single Python 3.10 run)
```

All five must pass for `test-summary` to be green.
