# D-0025 — AC10 ptytest fork SHA pin + drift policy

**Task:** T02.03 (Phase 2)
**Roadmap row:** AC10 (Acceptance Criterion 10 — fork SHA freeze + drift policy)
**Tier:** EXEMPT
**Date:** 2026-05-20
**Depends on:** T02.01 (NFR-MAINT1 — vendored ptytest sources). The pin recorded
here is the SHA T02.01 MUST land or update against; the PROVENANCE.md / CHECKLIST.md
files this deliverable writes will live alongside the vendored sources once they
physically arrive under `src/superclaude/cli/eval/pty/`.

---

## 1. Why this deliverable exists

AC10 of the cliEval design contract requires the vendored `ptytest` fork to
have:

1. A **frozen upstream SHA** recorded at a known path with the vendoring date.
2. A **quarterly review cadence** captured at the same path, with a named
   owner.
3. A **standing review procedure** that the owner can execute without
   reconstructing context every time.
4. An **explicit resync path** so that a clean review (the common case) and a
   resync (the rare case) are both unambiguous.

Without (3) and (4), the cadence in (2) becomes lore that decays the moment
the maintainer rotates. Without (1), there is no anchor against which "drift"
is even defined. T02.03 produces the durable artifacts that satisfy all four.

## 2. Drift policy (canonical)

| Field | Value |
|-------|-------|
| Pinned upstream SHA | `61a46870e38710c7cfc95f00cefbf0499111aa5f` |
| Pinned short SHA | `61a4687` |
| Upstream commit date | 2025-12-21 |
| Review cadence | Quarterly (90-day rolling window from last completed review) |
| Initial review anchor | 2026-08-20 *(90 days from authoring date)* |
| Review owner | **RyanW** (maintainer; per roadmap risk register) |
| Out-of-band triggers | (a) CVE against `pexpect` or `ptytest`; (b) upstream commit touching prompt-detection or ANSI-stripping; (c) failing `tests/cli/eval/test_pty_vendor.py` after an unrelated refactor. |
| Default review outcome | *Pin held* — bump `Next review due` by 90 days; record row in `PROVENANCE.md` §4. |
| Escalation outcome | *Resync scheduled / Resync landed* — open a tracked resync task, follow `PROVENANCE.md` §3 *Resync procedure*. |

The SHA was captured at authoring time from
`GET https://api.github.com/repos/brandon-fryslie/ptytest/commits/master`
(2026-05-20). T02.01 MUST confirm or replace this SHA in the same commit that
physically lands the vendored sources, so the pin and the on-disk content
remain byte-aligned.

## 3. Files created by this task

| Path | Change | Purpose |
|------|--------|---------|
| `src/superclaude/cli/eval/pty/PROVENANCE.md` | CREATED | SHA pin + vendoring metadata + cadence + review log table. |
| `src/superclaude/cli/eval/pty/CHECKLIST.md` | CREATED | 5-step quarterly review procedure. |
| `.dev/releases/current/cliEval/artifacts/D-0025/spec.md` | CREATED | This file. |
| `.dev/releases/current/cliEval/artifacts/D-0025/notes.md` | CREATED | Implementation notes + open caveats. |
| `.dev/releases/current/cliEval/artifacts/D-0025/evidence.md` | CREATED | Verification evidence pointers. |
| `.dev/releases/current/cliEval/evidence/T02.03/` | POPULATED | Evidence directory for the task. |

Files NOT touched in this task (deferred to T02.01 / NFR-MAINT1):

- `src/superclaude/cli/eval/pty/LICENSE` — verbatim upstream MIT terms; lands
  with vendored sources.
- `src/superclaude/cli/eval/pty/__init__.py` and the vendored module sources
  themselves.
- The `Changes from upstream` section body in `PROVENANCE.md` §2 — header is
  present, T02.01 populates the bullet list of file-level changes on landing.

This split keeps T02.03 (EXEMPT tier — documentation) cleanly separable from
T02.01 (STANDARD tier — physical vendoring), so a regression in either does
not pollute the other's evidence trail.

## 4. Acceptance criteria (per phase-2-tasklist.md §T02.03)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| File `src/superclaude/cli/eval/pty/PROVENANCE.md` records fork SHA, vendoring date, and "review cadence: quarterly". | ✅ MET | `PROVENANCE.md` §2 (SHA + vendoring-date row, currently TBD pending T02.01 landing) + §3 ("Review cadence: **Quarterly**"). |
| File `src/superclaude/cli/eval/pty/CHECKLIST.md` exists with the review-procedure steps. | ✅ MET | `CHECKLIST.md` Steps 1–5 (Confirm pin → Fetch HEAD → Triage diff → License re-verify → Record outcome). |
| Review owner is named explicitly (RyanW). | ✅ MET | `PROVENANCE.md` §3 *Review owner* row and `CHECKLIST.md` **Owner:** header both name *RyanW*. |
| `TASKLIST_ROOT/artifacts/D-0025/spec.md` records the drift policy. | ✅ MET | This file — §2 contains the canonical drift policy table. |

## 5. Verification (per phase-2-tasklist.md §T02.03 Validation)

- Manual read of `src/superclaude/cli/eval/pty/PROVENANCE.md` confirms fields
  present (§2 SHA pin row, §3 cadence + owner row, §4 review log row for the
  authoring date).
- Manual read of `src/superclaude/cli/eval/pty/CHECKLIST.md` confirms the
  5-step procedure with owner-named header.
- Tier is EXEMPT (Verification Method = "Skip verification"); the manual
  reads above are the maintainer's confirmation hook.

## 6. Dependencies and downstream gates unblocked

- **Depends on:** T02.01 (NFR-MAINT1) for the physical vendored sources +
  `LICENSE` file. The PROVENANCE.md SHA row will be confirmed (or updated by
  T02.01 to the SHA actually landed) when T02.01 commits.
- **Unblocks:** Nothing on the critical path — AC10 is a maintenance-policy
  artifact, not a runtime gate. The downstream consumer is the quarterly
  review cycle, first due 2026-08-20.
- **Inherited by:** R5-mit (T02.26 per `phase-2-tasklist.md`) — the cadence
  established here is the input to any later automation work (e.g. a calendar
  reminder or a CI job that opens an issue 90 days after the last review row).

## 7. Out of scope for T02.03

- Vendoring the ptytest sources themselves — that is T02.01.
- Authoring `src/superclaude/cli/eval/pty/LICENSE` — verbatim upstream copy
  lands with the sources in T02.01.
- Populating the *Changes from upstream* bullet list in `PROVENANCE.md` §2 —
  the section header is present; T02.01 fills the bullets when sources land.
- Automating the quarterly trigger (calendar reminder, CI issue opener) — that
  is deferred to R5-mit (T02.26).
- Flipping any decisions.md ADR to 🟢 APPROVED — sign-off is the maintainer's
  M2 exit pass.
