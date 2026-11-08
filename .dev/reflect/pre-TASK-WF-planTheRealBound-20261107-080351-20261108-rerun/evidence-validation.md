# Evidence Validation Report

(Returned by the evidence-validator agent; persisted by the parent on receipt at 2026-11-08T02:21Z. The draft frontmatter and two wording points were corrected afterwards by the parent, see Notes.)

**Report under validation**: REPORT.md.draft (now REPORT.md)
**Timestamp**: 2026-11-08T02:18:55Z
**Total citations**: 48 (16 non-plan file:line, 22 plan, 10 `source.md:1` quotes)
**Verified**: 48   **Dropped**: 0   **Passed through (command, no reexec)**: 0
**Suggested report status**: success for citation validation; the report keeps `partial` for its degraded components (no rebuttal round, position-bias pass and invariant probe not run, strict convergence 40.0%).

## Verified citations

Requested checks, all verified against the current working-tree plan: plan:22 contains "the preflight one, Task 2 four, Task 3 four and Task 4 three" (1+4+4+3 = 12); plan:31 contains "appends one JSON line per run" and "per-case cleanup never signals a surviving job or its supervisor"; plan:66 contains "inside the same governed command before it exits"; plan:117 contains "no unavailable row lacks a named interface"; plan:119 contains the real-Claude run count rule (real_claude true, refused launches included, at most twelve); plan:79 and plan:120 (release, PID reuse and boot identity labelled controlled; FAIL expected); plan:90 "no real Claude run is spent on this task"; plan:29 heading "Build the observation runner with a preflight and an exit-status ledger".

Source, design and archive citations, all verified: helper:338 (`if status is not None and not live:`, the return at 339 is inside it), helper:234 (compares start ticks and boot identity), helper:253 (comment "No bounded ancestry walk ..."), helper:292-295 (os.setsid, subreaper prctl(36)), helper:435-437 (no record means not rewritten), helper:219-223, helper:238-241 (released), helper:83 (owner-only mode), helper:149 (st_nlink != 1), design:504, design:555, design:526, design:557, live_probe:253 (--disable-slash-commands), help:131-132 ("only works with --print"), actor-context-probe.sh:11 (LIMIT = 64; real path .dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh).

Other plan citations verified: plan:23, :25, :35, :44, :49, :55-60, :66, :69, :95, :101, :114 (wrapper, Git and hook trees and auto-mode terms occur only at plan:114 and :117), :118-120, :121. All ten Inferred requirement quotes occur verbatim at source.md:1 (source.md has exactly one line).

## Dropped citations

None.

## Notes

1. The draft's own counts were inconsistent with the validator's: it said "five LOW items" (four LOW rows and one INFO row exist) and frontmatter citations_total 24 / citations_inferred 6. The parent corrected them to four LOW items, citations_total 48, citations_revalidated 48, citations_inferred 3 (three lines carry the [INFERRED] tag).
2. M2-06 wording was loose ("the ledger has no run id"); corrected to "the ledger field list at plan:31 names no run id and plan:119 counts ledger entries with real_claude true".
3. "The plan has no ledger yet (plan:25)": plan:25 supports only the freeze rule; the absence of a ledger rests on a directory listing (the package holds only source.md, the plan and return-contract.yaml). The report text now says so.
4. M2-13 bundled six sub-items under a loose line list; the parent mapped each item to its line (plan:31, :44, :55, :95, :101, :121).
5. The [INFERRED] runtime claims (M2-01, M2-02, M2-07 and the Grounding gaps) are untested; M2-xx analyses reason about the cited text, whose existence was confirmed, not about tested outcomes.
6. No pattern of upstream error: all 48 citations matched at the cited location. Structural assertions were not emitted (no assertions_path).
