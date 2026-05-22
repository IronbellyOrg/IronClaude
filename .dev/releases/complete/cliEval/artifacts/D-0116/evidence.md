# D-0116 — Evidence index

| Item | Path | Notes |
|------|------|-------|
| Sync log (canonical deliverable) | `.dev/releases/current/cliEval/evidence/T06.14/sync.log` | Records `make sync-dev` exit 0 and `make verify-sync` exit 0 with git HEAD, host, and UTC timestamp provenance. |
| Per-task summary | `.dev/releases/current/cliEval/evidence/T06.14/summary.md` | One-page summary mirroring `artifacts/D-0116/spec.md`. |
| Spec | `.dev/releases/current/cliEval/artifacts/D-0116/spec.md` | Acceptance map and sign-off summary for MIG-001. |
| Notes | `.dev/releases/current/cliEval/artifacts/D-0116/notes.md` | Implementation notes, dirty-tree caveat, re-attestation cadence. |
| AC11 source-of-truth gate (dependency) | `.dev/releases/current/cliEval/evidence/T01.20/` | Pre-commit hook attestation. |
| OPS-003 retention (dependency) | `.dev/releases/current/cliEval/evidence/T04.21/` | Retention policy under which `sync.log` is preserved. |
| OPS-004 consumer | `docs/eval/validation-commands.md` (command 2) | `make verify-sync` row in the validation-commands contract. |
| OPS-005 consumer | `docs/eval/release-checklist.md` §5 row 5.2, §6 row 6.3 | Release-checklist sync attestation rows. |

## Provenance summary

- **Run timestamp (UTC):** 2026-05-21T00:12:34Z
- **Git HEAD:** `36df8608692f906c4154d0ddab5ea5c35d3f6af4`
- **Branch:** `feature/sc-auggie-review-protocol`
- **Host:** `Linux 6.8.0-111-generic x86_64`
- **sync-dev exit code:** 0
- **verify-sync exit code:** 0
- **Pre-sync `.claude/` deltas:** 0
- **Post-sync `.claude/` deltas:** 0
