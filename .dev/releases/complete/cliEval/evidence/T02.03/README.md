# T02.03 — Evidence index

**Task:** T02.03 — AC10 ptytest fork SHA pin + drift policy
**Deliverable:** D-0025
**Tier:** EXEMPT
**Date:** 2026-05-20

## Files in this directory

| File | Purpose |
|------|---------|
| `README.md` | This index. |
| `checks.txt` | Output of the 5 mechanical grep / wc checks documented in `artifacts/D-0025/evidence.md` §*Mechanical checks*. |

## Acceptance criteria verification

| Criterion | Result | Source |
|-----------|--------|--------|
| `src/superclaude/cli/eval/pty/PROVENANCE.md` records fork SHA. | ✅ PASS — SHA `61a46870…` appears 2× in PROVENANCE.md. | `checks.txt` check 1 |
| `PROVENANCE.md` records "review cadence: quarterly". | ✅ PASS — "Quarterly" appears in §3 cadence row. | `checks.txt` check 2 |
| `PROVENANCE.md` records vendoring date. | ✅ PASS — row present in §2 (`TBD` pending T02.01 landing — documented). | Read `PROVENANCE.md` §2 |
| `src/superclaude/cli/eval/pty/CHECKLIST.md` exists with review procedure. | ✅ PASS — 97 lines, 5 steps. | `checks.txt` check 5 |
| Review owner named explicitly (RyanW). | ✅ PASS — RyanW named in both PROVENANCE.md (×2) and CHECKLIST.md (×1). | `checks.txt` checks 3, 4 |
| `artifacts/D-0025/spec.md` records drift policy. | ✅ PASS — see `spec.md` §2 *Drift policy (canonical)*. | `artifacts/D-0025/spec.md` |

## Notes

- T02.03 ran before T02.01 (vendoring) landed. The `src/superclaude/cli/eval/pty/`
  directory was created here to host `PROVENANCE.md` and `CHECKLIST.md`. T02.01
  will populate `LICENSE`, `__init__.py`, and the vendored module sources, and
  will confirm or update the SHA row in `PROVENANCE.md` §2 in the same commit.
- The SHA pin was captured live from the GitHub API
  (`brandon-fryslie/ptytest@master`) on the authoring date so that the AC10
  acceptance criterion ("records fork SHA") is unambiguously met independent
  of T02.01 timing.
- First scheduled drift review: **2026-08-20** (90 days from authoring).
