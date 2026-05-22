# D-0076 — Working notes (T04.15)

## Why this task is EXEMPT-tier

Phase-4 tasklist row T04.15 sets `Tier: EXEMPT` and `Verification Method: Skip verification`.
The task is a decision-recording / documentation closure, not a code change. The decision
itself (option A vs B) requires no test run because the implementation has already converged
on option A under T03.13 (Reporter) and T04.10 (CLI). T04.15 is the paperwork that closes the
loop between `roadmap.md` row 253, the spec, and the code that already exists.

## Investigation steps

1. Read `phase-4-tasklist.md` rows T04.10 (FR-CLI1) and T04.15 (DOC-OQ7) to identify the
   contract (12 flags, `--junit` named).
2. Searched `decisions.md` for OQ-7 references — found in §B "Open Question resolution status"
   marked `OPEN` per OPS-001 closure date, with two outcomes named.
3. Searched `design-spec.md` for `junit` occurrences:
   - `:140` — directory tree shows `junit.xml` as optional artifact.
   - `:591-593` — §9 says `Generated only when --junit is passed`.
   - `:621` — §10 says `Add to_json() and to_junit() (new methods, ~50 LOC each)`.
   - §4 flag table (`:185-199`) did **not** list `--junit` — this is the drift OQ-7 was
     opened to close.
4. Searched `roadmap.md` for OQ-7 / `--junit`:
   - `:111-112` — OQ-7 owner is `RyanW`, target `before M1 exit`.
   - `:249` — FR-CLI1 row R-072 lists 12 flags including `--junit`.
   - `:253` — DOC-OQ7 row R-076 names the two outcomes.
5. Inspected `src/superclaude/cli/eval/commands.py` and `reporter.py` — `--junit` flag and
   `to_junit()` / `emit_junit` gate are already implemented. Code matches option A.

## Decision logic

- The implementation is already option A. Choosing option B would require deleting working
  code AND amending three documents (roadmap R-072, T04.10 AC, spec §9 + §10).
- The marginal cost of option A is one row in the spec §4 flag table.
- Option A is consistent with the dominant CI ingestion pattern (JUnit XML).
- Therefore option A wins on consistency, sunk cost, and forward-utility grounds.

## What this commit does

1. Append `DOC-OQ7 Closure` section to `decisions.md` (the deliverable named by T04.15).
2. Add `--junit BOOL` row to spec §4 flag table to close the §4-vs-FR-CLI1 drift.
3. Create `artifacts/D-0076/{spec,notes,evidence}.md` per the Phase-4 tasklist intended-paths.
4. Create `evidence/T04.15/` with verification artifacts.

## What this commit deliberately does NOT do

- Does not edit `roadmap.md` or `.roadmap-state.json` — out of scope; the roadmap row R-072
  already lists `--junit` and needs no change.
- Does not modify `commands.py` or `reporter.py` — both already implement option A.
- Does not re-render the OPS-001 OQ-7 row from `OPEN` to `RESOLVED` in place — the
  `DOC-OQ7 Closure` section is canonical and supersedes by date precedence (the same pattern
  is used by D-9 / D-10 in this file).
- Does not add a new TEST row for JUnit-XML schema conformance — left as a future refinement
  if TEST-007 needs strengthening.
