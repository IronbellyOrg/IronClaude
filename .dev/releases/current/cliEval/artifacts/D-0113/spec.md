# D-0113 — SC3 zero-new-deps verification

**Task:** T06.10 (Phase 6, Roadmap SC3 / R-112)
**Success criterion:** SC3 — "no new external Python deps land beyond `pexpect` (vendored via ptytest) and `jsonschema` (already transitive)."
**Verifier:** `make verify-deps` → `scripts/verify_deps.py` (T01.17 / R-015 / D-0015)
**Status:** RESOLVED — 2026-05-20

## Purpose

SC3 (roadmap row 446 / R-112) requires the v1 implementation to land **zero new external Python dependencies** beyond two explicitly allow-listed transitive additions:

| Allowed addition | Provenance |
|------------------|------------|
| `pexpect`        | Runtime dependency of the vendored `ptytest` fork (D-1 / `cli/eval/pty/`). |
| `ptyprocess`     | Required transitive runtime of `pexpect`. |

`jsonschema` was already a direct dependency of `superclaude` pre-eval-CLI; AC3 treats it as in-scope and not a net addition.

T06.10 captures the post-implementation evidence demonstrating SC3 holds:

1. A `uv pip list --format=json` snapshot of the post-implementation install tree.
2. A diff against `scripts/dependency_baseline.txt` (the AC3 allow-list landed by T01.17).
3. `make verify-deps` exit 0 on the final tree.
4. Confirmation that the CI assertion (`.github/workflows/test.yml :: verify-deps`) fails closed on any future out-of-list addition.

## Verification outcome

| Comparison | Result |
|------------|--------|
| Post-impl install vs combined AC3 baseline allow-list (36 packages) | **0 additions, 0 removals** — perfect subset/equal. |
| Post-impl install vs pre-eval-CLI snapshot (34 packages) | **2 additions:** `pexpect`, `ptyprocess`. Both AC3-permitted. **0 unauthorized additions.** |
| `make verify-deps` exit code | **0** (PASS). |

Full evidence:

- `TASKLIST_ROOT/evidence/T06.10/dep-diff.log` — human-readable diff summary.
- `TASKLIST_ROOT/evidence/T06.10/make-verify-deps.log` — verbatim `make verify-deps` stdout/stderr.
- `TASKLIST_ROOT/evidence/T06.10/uv-pip-list-post.json` — raw `uv pip list --format=json` snapshot.
- `TASKLIST_ROOT/evidence/T06.10/installed-post.txt` — PEP 503 normalised post-impl name set (36 entries).
- `TASKLIST_ROOT/evidence/T06.10/baseline-allowlist.txt` — combined AC3 allow-list (36 entries).
- `TASKLIST_ROOT/evidence/T06.10/baseline-pre-eval-cli.txt` — pre-eval-CLI snapshot (34 entries).
- `TASKLIST_ROOT/evidence/T06.10/additions.txt` — empty (0 additions vs combined allow-list).
- `TASKLIST_ROOT/evidence/T06.10/removals.txt` — empty (0 removals vs combined allow-list).

## Gate wiring

### `Makefile :: verify-deps` (landed by T06.10)

T01.17 / D-0015 declared this target as part of its file inventory but the
target body was never committed to `Makefile`. T06.10 closes the gap by
adding the canonical four-line target plus a `.PHONY` entry and a help
line — see `Makefile :: verify-deps`.

```makefile
verify-deps:
	@echo "🔍 Verifying Python dependency allow-list (AC3 / R-015)..."
	@uv run python scripts/verify_deps.py
	@echo "EXIT=$$?"
```

### `.github/workflows/test.yml :: verify-deps` (already wired by T01.17)

```yaml
verify-deps:
  name: Dependency Allow-list (AC3)
  runs-on: ubuntu-latest
  steps:
    ...
    - name: Verify dependency allow-list
      run: make verify-deps
```

`test-summary.needs` includes `verify-deps`, so a failed allow-list check short-circuits the CI summary with non-zero exit.

### `scripts/verify_deps.py` + `scripts/dependency_baseline.txt`

Both landed by T01.17 (D-0015); T06.10 consumes them unchanged. PEP 503 normalisation (lowercase, hyphenated) is applied to both sides of the comparison.

## Acceptance criteria → evidence map

| AC (T06.10) | Evidence |
|-------------|----------|
| File `TASKLIST_ROOT/evidence/T06.10/dep-diff.log` shows zero new top-level deps post-implementation. | `evidence/T06.10/dep-diff.log` §2 (combined allow-list diff: 0 additions, 0 removals) + §3 (pre-eval-CLI diff: only `pexpect`, `ptyprocess`, both AC3-permitted). |
| `make verify-deps` exits 0 on the final tree. | `evidence/T06.10/make-verify-deps.log` (final `FINAL_EXIT=0`). |
| `decisions.md` SC3 entry status is `resolved`. | `decisions.md` §"SC3 Closure — Zero-new-deps verification (T06.10)". |
| `TASKLIST_ROOT/artifacts/D-0113/spec.md` records the verification outcome. | This file. |

## Failure-mode analysis

| Drift pattern | Caught by | Notes |
|---|---|---|
| New direct dep added to `pyproject.toml :: dependencies` | `scripts/verify_deps.py` compares `uv pip list` (which reflects installed deps after `uv pip install -e ".[dev]"`); the new package appears as an addition → exit 1. | CI `verify-deps` job fails. |
| New transitive dep pulled in by an existing dep's version bump | Same — `uv pip list` reflects the full install set, transitive included. | CI `verify-deps` job fails. |
| Allow-listed package version churn (no name change) | Comparison is **name-only** (PEP 503 normalised). Version drift does not trigger a failure. | By design — versions are governed by `pyproject.toml`, not this gate. |
| Allow-listed package not yet installed (e.g. dev tool dropped) | Reported as informational "Allow-listed but not installed" — does not fail. | By design — removals do not fail; only out-of-list additions do. |
| Baseline file missing or empty | `scripts/verify_deps.py` exits 2 with a clear error. | Catches accidental deletion. |

## Cross-references

- **T01.17 / R-015 / D-0015:** wired the `verify_deps.py` script, the baseline file, and the CI job. T06.10 consumes this infrastructure.
- **D-1 (R5 ADR, decisions.md §"D-1"):** vendored ptytest decision; `pexpect` is its runtime dep. The vendor lives at `cli/eval/pty/` and is not counted in the dependency tree — only its transitive runtime requirements are.
- **SC2 (roadmap row 451):** 15-eval coverage in `real.yaml`. Independent of SC3.
- **SC4 (T06.08 / R-110):** LOC estimate ack. SC4 §"Cross-references" already notes SC3 is unaffected by the harness LOC overrun (no new top-level deps; the LOC is in already-imported stdlib + jsonschema + the vendored fork).
- **SC5 (T06.09 / R-111):** OQ ledger. SC3 is independent of OQ resolution status.
- **T06.16 (M6 exit checkpoint):** consumes this section as the v1 SC3 attestation.
- **`pyproject.toml`:** the authoritative source for the direct-deps surface; `verify_deps.py` operates on the installed result of `uv pip install -e ".[dev]"` rather than parsing pyproject directly, so the gate covers both direct adds and transitive surprises.

## Regeneration / future updates

To regenerate this evidence (e.g. after a future approved dep addition):

```bash
# 1. Refresh the installed snapshot.
uv pip install -e ".[dev]"

# 2. Re-run the verification.
make verify-deps

# 3. Re-capture the diff evidence.
uv pip list --format=json > .dev/releases/current/cliEval/evidence/T06.10/uv-pip-list-post.json
uv run python -c "
import json
data = json.load(open('.dev/releases/current/cliEval/evidence/T06.10/uv-pip-list-post.json'))
names = sorted({p['name'].lower().replace('_','-') for p in data})
print('\n'.join(names))
" > .dev/releases/current/cliEval/evidence/T06.10/installed-post.txt

# 4. Refresh the dep-diff.log narrative if the post-impl install set changes.
```

If a future addition is **approved**, update `scripts/dependency_baseline.txt` (the allow-list) **and** add an `Outcome:` line to the SC3 Closure section in `decisions.md` so the audit trail is preserved.
