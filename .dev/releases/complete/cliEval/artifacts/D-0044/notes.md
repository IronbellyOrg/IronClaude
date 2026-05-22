# D-0044 — Implementation notes

## Scheduling rationale

The target-date table in `CHECKLIST.md` lists *four* upcoming reviews rather
than the bare minimum of two required by the acceptance criterion. The reason
is that two-row visibility is fragile under maintainer rotation: if the owner
completes review #1 and forgets to append row #3 at the bottom, the table
quietly degrades to one-row visibility and the next handoff inherits a
checklist that effectively *names no future date*. Pre-scheduling four rows
keeps two reviews visible even after a clean completion+append cycle has been
skipped once.

The "slip up to one calendar week without bumping the cadence" rule is a
soft fence: it absorbs a maintainer being on vacation when the target date
lands, without forcing a paperwork entry for what is effectively a
no-behavior-change late review. Slips beyond a week are recorded explicitly
in `PROVENANCE.md` §4 so the cadence does not silently drift quarter over
quarter.

## Why this is additive, not a rewrite

The 5-step procedure that T02.03 authored (Confirm pin → Fetch HEAD →
Triage diff → License re-verify → Record outcome) is the *content* of a
review. R5-mit asked for the *scheduling layer* — when reviews happen, by
whom, against which calendar. Mixing the two into a single rewrite would
have lost the boundary between T02.03 (procedure) and T02.26 (schedule),
making the next regression hard to localize. The header **Satisfies:** row
that names both AC10 and R5-mit makes the layering explicit so a reader can
see which obligations the file is closing without bouncing through the
release directory.

## Cadence anchor source of truth

`PROVENANCE.md` §3 *Next review due* remains the single source of truth for
"when is the next review". The target-date table in `CHECKLIST.md` is a
*projection* of that anchor 90, 180, 270, 360 days forward. If the anchor in
PROVENANCE.md changes (e.g. a resync lands and the anchor rolls forward from
the resync date), the maintainer recomputes the table from the new anchor on
the next review completion.

This split is intentional: anchor in PROVENANCE.md, projection in
CHECKLIST.md. Storing the anchor in two places would invite drift between
them.

## Out-of-band review triggers (carried from T02.03)

The list in `CHECKLIST.md` (CVE, upstream commit touching prompt-detection
or ANSI-stripping, failing `tests/cli/eval/test_pty_vendor.py`) is unchanged
by T02.26. R5-mit does not introduce new triggers; it formalizes when the
*scheduled* reviews happen so the maintainer is not silently waiting on a
trigger that may never fire.

## Files left unchanged

- `PROVENANCE.md` — anchor still `2026-08-20`; review log §4 still records
  only the T02.03 authoring row. Both fields update on the *first actual
  completed review* (2026-08-20 target), not at T02.26 authoring time.
- `decisions.md` — D-10 (NOTICE/LICENSE attribution) and D-1 (fork-vs-build)
  cover ptytest decisions; R5-mit is a mitigation of a tracked risk, not a
  new ADR-worthy decision.

## Open caveats

- No automation. R5-mit deliberately stays as a procedure document. A future
  task may add a calendar reminder or a CI job that opens an issue 90 days
  after the last review row in `PROVENANCE.md` §4 — that work is out of
  scope here per the task notes in `phase-2-tasklist.md` §T02.26.
- The four pre-scheduled rows project against the *initial* anchor. A resync
  inside the window will reset the anchor and invalidate the later rows.
  This is expected — the maintainer recomputes from the new anchor at the
  next completion.
