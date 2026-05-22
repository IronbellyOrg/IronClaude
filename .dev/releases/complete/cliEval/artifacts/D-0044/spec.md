# D-0044 — Quarterly ptytest drift review checklist (R5-mit)

**Task:** T02.26 (Phase 2)
**Roadmap row:** R-044 (R5-mit — ptytest fork drift mitigation)
**Tier:** EXEMPT
**Date:** 2026-05-20
**Depends on:** T02.03 (AC10 — fork SHA pin + drift policy). The 5-step review
procedure and the cadence anchor were authored by T02.03; T02.26 layers the
explicit target-date schedule on top so the cadence is durable across
maintainer rotation.

---

## 1. Why this deliverable exists

R5 (ptytest fork drift) is mitigated by AC10 (the SHA pin and quarterly
review). AC10 by itself names a *cadence*; R5-mit additionally requires that
the maintainer can open the checklist and see *the next concrete review
dates* without recomputing the 90-day offset from the anchor. The gap T02.26
fills is therefore a small one — a pre-scheduled target-date table inside
`CHECKLIST.md` — but it is the difference between a procedure that survives
maintainer rotation and one that decays the moment someone forgets to update
the anchor.

## 2. Files changed by this task

| Path | Change | Purpose |
|------|--------|---------|
| `src/superclaude/cli/eval/pty/CHECKLIST.md` | UPDATED | Added a "Target review dates (R5-mit)" section listing the next four reviews; added explicit AC10 + R5-mit / T02.03 + T02.26 cross-reference in the header. |
| `.dev/releases/current/cliEval/artifacts/D-0044/spec.md` | CREATED | This file. |
| `.dev/releases/current/cliEval/artifacts/D-0044/notes.md` | CREATED | Implementation notes + scheduling rationale. |
| `.dev/releases/current/cliEval/artifacts/D-0044/evidence.md` | CREATED | Verification evidence pointers. |
| `.dev/releases/current/cliEval/evidence/T02.26/` | POPULATED | Evidence directory for the task. |

Files NOT touched in this task:

- `src/superclaude/cli/eval/pty/PROVENANCE.md` — already records the cadence
  anchor (`Next review due: 2026-08-20`) and review owner. The new target-date
  table in `CHECKLIST.md` is anchored *against* PROVENANCE.md §3, not a
  duplicate of it; the cadence still has one source of truth.
- The 5-step review procedure in `CHECKLIST.md` Steps 1–5 — unchanged; T02.26
  is purely an additive scheduling layer.

## 3. Target review dates (canonical)

The schedule below is reproduced in `CHECKLIST.md` so a maintainer reading the
checklist does not need to bounce to this artifact to know the next date.

| # | Target date | Quarter | Owner | Status |
|---|-------------|---------|-------|--------|
| 1 | 2026-08-20 | 2026 Q3 | RyanW | Scheduled (initial cadence anchor) |
| 2 | 2026-11-18 | 2026 Q4 | RyanW | Scheduled |
| 3 | 2027-02-16 | 2027 Q1 | RyanW | Scheduled |
| 4 | 2027-05-17 | 2027 Q2 | RyanW | Scheduled |

Offsets are 90-day rolls from the prior row, matching the cadence definition
in `PROVENANCE.md` §3.

## 4. Acceptance criteria (per phase-2-tasklist.md §T02.26)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| File `src/superclaude/cli/eval/pty/CHECKLIST.md` lists the 5-step review procedure with owner = RyanW. | ✅ MET (carried from T02.03; re-verified) | `CHECKLIST.md` Steps 1–5 + **Owner:** header. |
| File records quarterly cadence with at least the next 2 target review dates. | ✅ MET | `CHECKLIST.md` *Target review dates (R5-mit)* table — 4 dates listed (2026-08-20, 2026-11-18, 2027-02-16, 2027-05-17). |
| AC10 cross-reference is recorded in CHECKLIST.md. | ✅ MET | `CHECKLIST.md` header **Satisfies:** row names *AC10 (fork SHA pin + drift policy)* and *R5-mit*. |
| `TASKLIST_ROOT/artifacts/D-0044/spec.md` records the checklist content. | ✅ MET | This file — §3 reproduces the target-date table, §2 enumerates the file-level changes. |

## 5. Verification (per phase-2-tasklist.md §T02.26 Validation)

- Manual read of `src/superclaude/cli/eval/pty/CHECKLIST.md` confirms:
  - The *Target review dates (R5-mit)* section is present with 4 rows.
  - The **Satisfies:** header names both AC10 and R5-mit.
  - The 5-step procedure (Steps 1–5) is unchanged.
- Tier is EXEMPT (Verification Method = "Skip verification"); the manual read
  above is the maintainer's confirmation hook, recorded in `evidence.md`.

## 6. Dependencies and downstream

- **Depends on:** T02.03 (CHECKLIST.md + PROVENANCE.md created; SHA pin set;
  initial cadence anchor at 2026-08-20).
- **Unblocks:** Nothing on the critical path — R5-mit is a maintenance-policy
  artifact, not a runtime gate. The downstream consumer is the quarterly
  review cycle, first due 2026-08-20.

## 7. Out of scope for T02.26

- Automating the quarterly trigger (calendar reminder, CI issue opener) —
  noted as deferred in `CHECKLIST.md` Acceptance section; lives outside this
  release's scope.
- Updating `PROVENANCE.md` cadence anchor — anchor is owned by §3 of that file
  and rolls forward only when an actual review row is appended to §4.
- Re-pinning the SHA — that is a resync action triggered by a review outcome,
  not by the scheduling layer.
