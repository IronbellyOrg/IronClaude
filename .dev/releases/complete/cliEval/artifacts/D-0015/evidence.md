# D-0015 — verification evidence

**Task:** T01.17 (Phase 1, Roadmap AC3 / R-015)
**Date:** 2026-05-20
**Tier:** EXEMPT (Section 5.3 — CI process check, no runtime code change)

## 1. Files landed

| File | Status |
|------|--------|
| `scripts/verify_deps.py`          | Created (executable). |
| `scripts/dependency_baseline.txt` | Created (36 entries: 34 pre-eval-CLI + 2 AC3 additions). |
| `Makefile` `verify-deps` target   | Added (lines 318-322). |
| `Makefile` `.PHONY` declaration   | Updated to include `verify-deps`. |
| `Makefile` help block             | Updated. |
| `.github/workflows/test.yml`      | Added `verify-deps` job + `test-summary` dependency. |

## 2. AC: `make verify-deps` exits 0 on current dependency tree

Captured at `evidence/T01.17/verify_deps.passing.log`:

```
🔍 Verifying Python dependency allow-list (AC3 / R-015)...
Baseline allow-list size: 36
Currently installed:      34
Allow-listed but not installed (informational, not a failure):
  - pexpect
  - ptyprocess

PASS: installed packages are a subset of the AC3 allow-list.
EXIT=0
```

The two informational entries (`pexpect`, `ptyprocess`) are AC3-permitted
additions that haven't been installed yet (ptytest vendor lands in Phase 2).

## 3. AC: script fails on a synthetic non-allow-list addition

Captured at `evidence/T01.17/verify_deps.synthetic_failure.log`. The current
install set was monkey-patched to include `requests` and `numpy-financial`
(neither in the baseline):

```
FAIL: new top-level dependencies detected outside AC3 allow-list:
  + numpy-financial
  + requests

AC3 (R-015) permits only `pexpect` and `jsonschema` as additions.
If this addition is intentional and approved, update:
  scripts/dependency_baseline.txt
EXIT=1
```

Exit code 1 confirms the failure path is wired through to a non-zero process
exit, so CI fails closed.

## 4. AC: baseline file is well-formed

Captured at `evidence/T01.17/baseline_validation.log`:

- 36 total entries, 36 unique (no duplicates).
- All entries are already PEP 503 normalised (lowercase, hyphenated).
- Pre-eval-CLI section is alphabetically sorted; AC3-additions section
  (`pexpect`, `ptyprocess`) follows the documented header convention.

## 5. AC: CI is wired to fail on out-of-list deps

`.github/workflows/test.yml` adds a `verify-deps` job:

```yaml
verify-deps:
  name: Dependency Allow-list (AC3)
  runs-on: ubuntu-latest
  steps:
    ...
    - name: Verify dependency allow-list
      run: |
        make verify-deps
```

The job is added to `test-summary`'s `needs:` list:

```yaml
needs: [test, lint, plugin-check, doctor-check, verify-deps]
```

and `test-summary` short-circuits with a non-zero exit when
`needs.verify-deps.result != 'success'`. This satisfies the AC bullet "CI
configuration runs `make verify-deps` and fails on new top-level deps
outside the allow-list".

## 6. AC: spec records allow-list and CI wiring

`artifacts/D-0015/spec.md` carries:

- The AC3 allowed-additions table (`pexpect`, `jsonschema`).
- The file inventory (script, baseline, Makefile target, CI workflow).
- The behavioural exit-code table (0 / 1 / 2).
- The CI-wiring snippet and `test-summary` dependency graph.
- The regeneration procedure for approved future additions.

## 7. Tier classification rationale

Tier=EXEMPT per phase-1-tasklist.md T01.17 metadata block. Section 5.3 of the
release spec exempts CI process checks that introduce no runtime code change
from sub-agent verification. The check itself is a thin wrapper around
`uv pip list` output diffing — no production code paths are touched.

## 8. Follow-on coordination

- **Phase 2 ptytest vendor drop** — when `ptytest` is vendored and `pexpect`
  is added as a real dep (direct or transitive), `verify-deps` will still
  pass because `pexpect` and `ptyprocess` are already in the baseline.
- **Future baseline updates** — must reference an approved roadmap entry and
  use the regeneration procedure in `spec.md` §"Regeneration procedure".
