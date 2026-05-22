# D-0113 — verification evidence

**Task:** T06.10 (Phase 6, Roadmap SC3 / R-112)
**Date:** 2026-05-20
**Tier:** EXEMPT (Section 5.3 — verification artifact; consumes T01.17 infrastructure unchanged).

## 1. Files landed

| File | Status |
|------|--------|
| `Makefile` `verify-deps` target | Added (closes T01.17 documentation/implementation gap; see `notes.md`). |
| `Makefile` `.PHONY` declaration | Updated to include `verify-deps`. |
| `Makefile` help block | Updated with the new target line. |
| `.dev/releases/current/cliEval/evidence/T06.10/dep-diff.log` | Created — human-readable diff summary. |
| `.dev/releases/current/cliEval/evidence/T06.10/make-verify-deps.log` | Created — verbatim `make verify-deps` output, exit 0. |
| `.dev/releases/current/cliEval/evidence/T06.10/uv-pip-list-post.json` | Created — raw `uv pip list --format=json` snapshot. |
| `.dev/releases/current/cliEval/evidence/T06.10/installed-post.txt` | Created — PEP 503 normalised install set (36 entries). |
| `.dev/releases/current/cliEval/evidence/T06.10/baseline-allowlist.txt` | Created — combined AC3 baseline allow-list (36 entries). |
| `.dev/releases/current/cliEval/evidence/T06.10/baseline-pre-eval-cli.txt` | Created — pre-eval-CLI snapshot (34 entries). |
| `.dev/releases/current/cliEval/evidence/T06.10/additions.txt` | Created — empty (0 lines). |
| `.dev/releases/current/cliEval/evidence/T06.10/removals.txt` | Created — empty (0 lines). |
| `.dev/releases/current/cliEval/artifacts/D-0113/spec.md` | Created — verification outcome record. |
| `.dev/releases/current/cliEval/artifacts/D-0113/notes.md` | Created — implementation notes (T01.17 gap, axis rationale). |
| `.dev/releases/current/cliEval/artifacts/D-0113/evidence.md` | This file. |
| `decisions.md` §"SC3 Closure — Zero-new-deps verification (T06.10)" | Appended — sign-off record. |

## 2. AC: `dep-diff.log` shows zero new top-level deps post-implementation

Captured at `evidence/T06.10/dep-diff.log`. Two diff axes are recorded:

- **Combined allow-list axis** (`scripts/dependency_baseline.txt`, 36 entries):
  0 additions, 0 removals. The install set is exactly the allow-list.
- **Pre-eval-CLI axis** (the 34-package pre-eval-CLI snapshot):
  2 additions — `pexpect`, `ptyprocess`. Both are AC3-permitted
  transitive runtimes (pexpect = runtime of the vendored ptytest fork;
  ptyprocess = pexpect's transitive runtime).

Zero unauthorised additions on either axis.

## 3. AC: `make verify-deps` exits 0 on the final tree

Captured at `evidence/T06.10/make-verify-deps.log`:

```
🔍 Verifying Python dependency allow-list (AC3 / R-015)...
Baseline allow-list size: 36
Currently installed:      36

PASS: installed packages are a subset of the AC3 allow-list.
EXIT=0
```

Shell exit code: 0.

## 4. AC: `decisions.md` SC3 entry status is `resolved`

`decisions.md` §"SC3 Closure — Zero-new-deps verification (T06.10)"
records:

- `Resolution: <verbatim outcome>` — both diff axes summarised + the
  `make verify-deps` exit code.
- `Resolution status: RESOLVED — 2026-05-20`.
- `Resolution artifact: <this file>` + `artifacts/D-0113/spec.md` + the
  per-file evidence list above.
- Cross-references to SC2 / SC4 / SC5 / T06.16 already note SC3 is
  unaffected by adjacent success criteria.

## 5. AC: spec records verification outcome

`artifacts/D-0113/spec.md` carries:
- The SC3 contract (allow-list table).
- The verification outcome table (combined axis + pre-eval-CLI axis +
  make-target exit code).
- The gate-wiring section (Makefile target, CI job, baseline file).
- The acceptance criteria → evidence map.
- The failure-mode analysis.
- The regeneration procedure.

## 6. Tier classification rationale

Tier=EXEMPT per phase-6-tasklist.md T06.10 metadata block ("Verification
Method: Skip verification"). The task is a release-attestation artifact
that consumes T01.17's existing gate infrastructure unchanged; no
runtime code path is altered. The one structural change — adding the
`verify-deps` Makefile target — closes a documentation/implementation
gap in T01.17 and does not introduce new production behaviour beyond
what `scripts/verify_deps.py` already provides.

## 7. Reproducibility

To re-verify on a clean checkout:

```bash
# 1. Install dependencies (matches CI).
uv pip install -e ".[dev]"

# 2. Run the gate.
make verify-deps        # expected: exit 0, "PASS" message.

# 3. Regenerate the post-impl snapshot (optional, for refreshed evidence).
uv pip list --format=json \
  > .dev/releases/current/cliEval/evidence/T06.10/uv-pip-list-post.json
```

If `make verify-deps` exits non-zero on a fresh tree, `scripts/verify_deps.py`
will print the offending additions and the operator can either:
- Roll back the unauthorised dep, or
- Update `scripts/dependency_baseline.txt` after PR approval (see the
  regeneration procedure in `artifacts/D-0015/spec.md`).

## 8. Follow-on coordination

- **T06.12 (Checkpoint P06-T07-T11):** consumes this artifact as the SC3
  pass evidence for the mid-phase checkpoint.
- **T06.16 (Phase 6 end-of-phase checkpoint):** consumes this artifact as
  one of the five SC1-SC5 attestations gating M6 exit.
- **OPS-005 release checklist (T06.13):** links this artifact under the
  "Dependency gate" checklist item.
- **Post-v1 dep additions:** any future approved addition must follow the
  regeneration procedure documented in `artifacts/D-0113/spec.md` §"Regeneration / future updates".
