# D-0015 — AC3 CI dependency-boundary assertion spec

**Task:** T01.17 (Phase 1, Roadmap AC3 / R-015)
**CI gate:** `make verify-deps`
**Status:** Implemented 2026-05-20

## AC3 contract

Roadmap AC3 (R-015) forbids any new external Python dep landing with the eval
CLI **beyond** the two transitive packages already in scope:

| Allowed addition | Provenance |
|------------------|------------|
| `pexpect`        | Transitive via vendored `ptytest` (lands in Phase 2 T02.x when ptytest is vendored). |
| `jsonschema`     | Already a transitive dep (used as `[project.dependencies]` entry today). |

Any other addition to `uv pip list` (direct or transitive) is a CI failure
that must be explicitly approved via a baseline update + PR review.

## Files

| Path                                  | Purpose |
|---------------------------------------|---------|
| `scripts/verify_deps.py`              | Compares `uv pip list --format=json` against the baseline; exits 0/1. |
| `scripts/dependency_baseline.txt`     | The committed allow-list (current pre-eval-CLI install + AC3 additions). |
| `Makefile` `verify-deps` target       | Invokes the script via `uv run python scripts/verify_deps.py`. |
| `.github/workflows/test.yml`          | New `verify-deps` job and `test-summary` dependency. |

## Allow-list contents

The baseline file (`scripts/dependency_baseline.txt`) carries:

1. **Pre-eval-CLI snapshot** — 34 packages captured 2026-05-20 from
   `uv pip list --format=json` after `uv pip install -e ".[dev]"`. This is the
   "before" half of the AC3 snapshot diff.
2. **AC3 additions** — `pexpect` (and its required runtime dep `ptyprocess`).
   `jsonschema` is already in the baseline (already a direct dep in
   pyproject.toml), so no separate allow-list entry is needed for it; AC3
   simply codifies that its retention or version churn does not constitute a
   new addition.

PEP 503 normalisation is applied (lowercase, hyphenated) so casing or
underscore drift in upstream package metadata does not produce spurious
diffs.

## Behaviour

| Situation                                                             | Exit | Output                                                 |
|-----------------------------------------------------------------------|------|--------------------------------------------------------|
| Installed packages are a subset of the baseline                       | 0    | "PASS: installed packages are a subset of the AC3 allow-list." |
| A package outside the baseline is installed                           | 1    | "FAIL: new top-level dependencies detected outside AC3 allow-list:" + sorted diff |
| Allow-listed package is missing from install (pexpect not yet pulled in) | 0    | Informational note, no failure                       |
| Baseline file missing/empty                                           | 2    | "ERROR: baseline file ..."                             |
| `uv` not on PATH                                                      | 2    | "ERROR: `uv` is not on PATH..."                        |

Removals from the install are intentionally not a failure — a dev tool can be
dropped without ceremony, and the allow-list is upper-bound, not exact.

## CI wiring

`.github/workflows/test.yml` adds a `verify-deps` job that:

- Runs on `ubuntu-latest` (no matrix — package set is the same across Python
  versions for this gate).
- Installs the project with `uv pip install --system -e ".[dev]"`.
- Invokes `make verify-deps`.
- Is added to the `test-summary` job's `needs:` list so any failure blocks
  the green-summary status.

## Acceptance criteria → implementation map

| AC bullet (T01.17)                                                                                | Implementation site |
|---------------------------------------------------------------------------------------------------|---------------------|
| File `Makefile` contains a `verify-deps` target running the `uv pip list` snapshot comparison.    | `Makefile` — `verify-deps` target invokes `scripts/verify_deps.py`. |
| CI configuration runs `make verify-deps` and fails on new top-level deps outside `{pexpect,jsonschema}`. | `.github/workflows/test.yml` — `verify-deps` job + `test-summary` needs entry. |
| `make verify-deps` exits 0 on the current dependency tree (pre-eval-CLI).                          | Verified by `evidence/T01.17/verify_deps.passing.log`. |
| `TASKLIST_ROOT/artifacts/D-0015/spec.md` records the allow-list and CI wiring.                     | This file. |

## Validation evidence

| Check                                              | Evidence path                                              |
|----------------------------------------------------|------------------------------------------------------------|
| `make verify-deps` exits 0 on a clean tree         | `evidence/T01.17/verify_deps.passing.log`                  |
| Script fails on a synthetic added dep              | `evidence/T01.17/verify_deps.synthetic_failure.log`        |
| Baseline file is sorted, deduped, PEP 503 cleaned  | `evidence/T01.17/baseline_validation.log`                  |

## Out of scope for T01.17

- Pinning versions or running a lock-file diff (`uv lock`) — AC3 is name-only.
- Enforcing the allow-list at install time (e.g., via a `uv pip install`
  pre-hook) — CI gate is sufficient per the EXEMPT tier classification.
- Detecting *removed* packages — removals are not an AC3 concern.
- Wiring `pexpect` into `pyproject.toml` — that lands with the ptytest vendor
  drop in Phase 2.

## Regeneration procedure

When a deliberate dep addition has been approved (post-review), regenerate the
baseline:

```bash
uv pip install -e ".[dev]"
uv pip list --format=json \
  | python -c "import json,sys; \
      names=sorted({p['name'].lower().replace('_','-') for p in json.load(sys.stdin)}); \
      print('\n'.join(names))" \
  > /tmp/new_baseline.txt
# Merge changes into scripts/dependency_baseline.txt, preserving header comments
# and the AC3 allow-list section.
```

Approval must reference the roadmap entry that lifts AC3's constraint (or
amend AC3 explicitly).
