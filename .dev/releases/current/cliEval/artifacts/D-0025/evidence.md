# D-0025 — Verification evidence

## Artifacts produced

| Path | Type | Purpose |
|------|------|---------|
| `src/superclaude/cli/eval/pty/PROVENANCE.md` | Created | SHA pin + cadence + review owner + review log table |
| `src/superclaude/cli/eval/pty/CHECKLIST.md` | Created | 5-step quarterly review procedure |
| `.dev/releases/current/cliEval/artifacts/D-0025/spec.md` | Created | Per-deliverable contract |
| `.dev/releases/current/cliEval/artifacts/D-0025/notes.md` | Created | Implementation notes + caveats |
| `.dev/releases/current/cliEval/artifacts/D-0025/evidence.md` | Created | This file |
| `.dev/releases/current/cliEval/evidence/T02.03/checks.txt` | Created | Mechanical check outputs |
| `.dev/releases/current/cliEval/evidence/T02.03/README.md` | Created | Evidence directory index |

## Acceptance criteria — evidence map

| Criterion (phase-2-tasklist.md §T02.03) | Evidence |
|-----------------------------------------|----------|
| File `src/superclaude/cli/eval/pty/PROVENANCE.md` records fork SHA, vendoring date, and "review cadence: quarterly". | `PROVENANCE.md` §2 SHA row (`61a46870…`) + vendoring-date row (`TBD` pending T02.01) + §3 *Review cadence: **Quarterly***. |
| File `src/superclaude/cli/eval/pty/CHECKLIST.md` exists with the review-procedure steps. | `CHECKLIST.md` Steps 1–5: Confirm current pin → Fetch upstream HEAD → Triage diff → Re-verify license + attribution → Record review outcome. |
| Review owner is named explicitly (RyanW). | `PROVENANCE.md` §3 *Review owner* row and `CHECKLIST.md` **Owner:** header both name *RyanW*. |
| `TASKLIST_ROOT/artifacts/D-0025/spec.md` records the drift policy. | `spec.md` §2 *Drift policy (canonical)* table. |

## Mechanical checks

Recorded in `evidence/T02.03/checks.txt`:

1. `grep -c "61a46870e38710c7cfc95f00cefbf0499111aa5f" src/superclaude/cli/eval/pty/PROVENANCE.md` → expected ≥ 1.
2. `grep -c "Quarterly" src/superclaude/cli/eval/pty/PROVENANCE.md` → expected ≥ 1.
3. `grep -c "RyanW" src/superclaude/cli/eval/pty/PROVENANCE.md` → expected ≥ 1.
4. `grep -c "RyanW" src/superclaude/cli/eval/pty/CHECKLIST.md` → expected ≥ 1.
5. `wc -l src/superclaude/cli/eval/pty/CHECKLIST.md` → expected non-zero; file present.

## Verification method (per task spec)

- Tier: EXEMPT — Verification Method = "Skip verification".
- Manual review by maintainer is the confirmation hook for the doc artifacts.
- Mechanical grep checks above are recorded as defense-in-depth so that an
  accidental future edit that removes the SHA, cadence, or owner is caught by
  a one-liner.

## Downstream

- T02.01 (NFR-MAINT1) will validate the SHA when it lands the vendored
  sources, and will update the `Vendoring date` / `Vendoring commit` rows in
  PROVENANCE.md §2 in the same commit.
- The first scheduled drift review is **2026-08-20**.
