# POST reflect gate (item 14.48): owner rulings on the escalated deviations (2026-11-12)

Status: RULED by the owner.

## Context

The independent `/sc:reflect --mode post --depth deep` run (`reflect-post-20261112T192600Z-TASK-RF-sweep-phase1`, report `reflect/post/audit/REPORT.md`) returned PASS-with-deviations, no blocking finding, and escalated 12 unresolved deviations (1 Regression D-01, 11 Drift D-02 to D-12) under the rule of item 14.48.

## Owner's words and rulings

- D-01 (SPEC section 8 asks for `Popen`, chunked reads and a kill at 8 MiB; the seams use `subprocess.run` with an after-the-fact size check): "Leave it as is, there is no observable benefit worth the effort being Popen." Ruling: ACCEPTED as is; D-01 is Authorized. Facts recorded for the record: the plan's reason (the test guard only catches `subprocess.run`) was false (`tests/sweep/conftest.py:41` patches `Popen` too); the real ceiling is one call's output held in memory until the child exits or the 10 s per-call timeout kills it (real Orca replies are at most 14 KB; 8 MiB is about 100,000 `git status` paths at about 82 bytes each); the limit is still enforced for output that finishes in time. No DESIGN section 13 row was added.
- D-02 to D-04: "Update or remove stale text." Done: D-02 (two tests renamed to `..._still_render` and `..._collects_and_renders`, DESIGN line 760 and the result maps reworded; publication is credited to `test_cli_contract.py`); D-03 (DESIGN header lines 5 to 7 updated, task Open Questions OQ-2 to OQ-8 and OQ-17 marked RESOLVED with their records, OQ-18 NOT TRIGGERED); D-04 (a known-gap comment in `probes.py` and `classify.py`, no behaviour change; whether real Orca emits rows without a Dispatch id stays unverified).
- D-05 to D-12: "Leave the rest." Ruling: accepted as is; they go into the backlog issue.
