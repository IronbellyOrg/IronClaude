# Gate 3 consolidated findings (cycle 2)

**Date:** 2026-11-20
**F_2 = 1** (BLOCKING N-1; 0 synthetic). Source: qa/qa-verification-content-c1.md (FAIL, 1 BLOCKING) and qa/qa-verification-structural-c1.md (PASS). G3-1..G3-9 are FIXED-OK.

| ID | Origin | Location (document lines at review time) | Finding (full text: qa/qa-verification-content-c1.md row N-1) | Required fix |
|---|---|---|---|---|
| N-1 | content verification c1 (carried-over sentence, also newly written into the G3-8 row) | L354 (2.4 row 6), L1258 (5.3 G2 rule 2 paragraph), L1448 (8.1 new guard-stack row) | "every other orca call is ESCAPE" / "every other orca verb off the allow-list is blocked" is false: launch-level-guard.sh:487-490 lets a short call end in `--help` or `-h` through (at most four words from `orca`, no glob character; comment "help only on a short call"); pinned by tests/hooks/test_launch_level_guard_worker.py:226-230 (`test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker`, `orca list --help`, `orca agent launch -h`) | In each of the three places say the allow-list is exhaustive except for a short help call (`<verb words> --help` or `-h`, at most four words from `orca`, no glob character), citing launch-level-guard.sh:487-490 and test_launch_level_guard_worker.py:226-230; also check any other place that repeats the universal claim (grep "every other") |
