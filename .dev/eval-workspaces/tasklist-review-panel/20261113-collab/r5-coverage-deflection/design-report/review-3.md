verdict: FAIL

Third independent review of `r5-coverage-deflection/DESIGN.md` (596 lines, read in full) against `review-2.md` N1-N5, `merged-requirements.md` (MR:951-955, MR:1057-1060), `EVAL/tools/tmp-scripts/anon-b11.sh:15-26`, the 310 historical `merged-anon.md` files under `EVAL/arms/scoring/combos`, and the installed pytest 9.2.0 source (`_pytest/tmpdir.py:194-199`). N1-N5 are all fixed. The N5 fix adds one blocking defect (B1). There is also one new minor finding (M1).

## Review-2 findings: fixed or not fixed

| # | Review-2 finding | Status | DESIGN.md line |
|---|---|---|---|
| N1 | T-12 slowdown cases fail under `pytest.approx` | Fixed. T-12 now states 0.1381 and 0.1121 with `pytest.approx(value, abs=5e-5)`. Computed with `uv run python`: 37.795/273.7 = 0.1380891 (difference 1.09e-5) and 13/116 = 0.1120690 (difference 3.10e-5). Both are within 5e-5, and `x == pytest.approx(v, abs=5e-5)` returns True for both. All 10 k cases, finish offset 143.8 and hang offset 410.55 still pass. The k = 1 limits at lines 356 and 365 (14.8%, 22.2%) also check out (0.14832, 0.22241). | 486 |
| N2 | Anonymiser case mismatch; generic reviewer-id pattern | Fixed. Line 406 now says "every one case-insensitive (`sed -E 's/.../.../gI'`)", and the post-check at line 407 is `grep -ciE`. Every pattern in the post-check has a matching case-insensitive rewrite: reviewer ids, `\bM(10\|[1-9])\b`, `panel request`, `catalogue move(s)`, `peer coverage` and `requested Task(s)`. The `origin`, board and path patterns are unchanged from the earlier design. The rewrite and the post-check both use `t1b-1\|t2b-1\|t3-1\|t4-1\|t4-2`. Section 3 uses sl2 = t1b-1, t4-1, t3-1; hl2 = t4-1, t4-2, t3-1; el2 = t4-1, t3-1, t2b-1 (lines 338-340). The union is exactly those five ids, so the list covers every panel. Move ids now become `<redacted>`, which 299 of 310 historical reports already carry (`report <redacted>`, `anon-b11.sh:25`). The stated 32 of 310 move-id matches is correct (6 of them lowercase), and the three candidates give 0 case-insensitive matches. T-19 now covers `#### L1.R2 (m1)`, `Task-6` and `T1bModel01-03`. | 406, 407, 493 |
| N3 | Line 69 test command lacks `-p no:cacheprovider` | Fixed. Line 69 now says "tests with the command of section 6". | 69 |
| N4 | T-8 has no `api_error: true` case | Fixed. T-8 now has "a meta with `model_ok` and `findings_block` true but `api_error: true` posts nothing and logs `scout_unusable`". | 482 |
| N5 | pytest temporary folders written outside `R5/` and `SB/` | Fixed as to location: `--basetemp=/tmp/evalsb-collab-r5/pytest` is now in the line-469 and AC-1 commands, and line 69 points to them. The new option breaks the test run (see B1). | 469, 555 |

## New findings

### B1. blocking. DESIGN.md:469 and 555: the `--basetemp` path fails when `/tmp/evalsb-collab-r5` does not exist yet, so AC-1 cannot pass on a fresh host.

Evidence: pytest 9.2.0 (`_pytest/tmpdir.py:194-199`) handles a given basetemp with `if basetemp.exists(): rm_rf(basetemp)`, then `basetemp.mkdir(mode=0o700)`. It does not pass `parents=True`. `/tmp/evalsb-collab-r5` does not exist on this host now (`ls` fails). Only `sandbox-build.sh` creates it, and the design runs AC-1 at build time with no ordering after S-H3. Reproduced with a one-test file that uses `tmp_path`: `--basetemp=<tmp>/missing-parent/pytest` gives `ERROR test_x.py::test_a - FileNotFoundError`. Every test that uses `tmp_path` would error the same way, including T-8, T-22 and the F-* fault tests that use temporary run folders. AC-1 requires 0 failures. The sentence "pytest clears that folder at each run" is true, but it does not create the parent folder.

Fix: create the parent folder in both commands: `mkdir -p /tmp/evalsb-collab-r5 && cd REPO && PYTHONPATH=R5/lib uv run pytest -p no:cacheprovider --basetemp=/tmp/evalsb-collab-r5/pytest R5/tests ...` (lines 469 and 555). Putting `mkdir -p` in the command itself does not depend on when pytest first builds its base temporary folder.

### M1. minor. DESIGN.md:406: "the panel's own reviewer ids (`t1b-1|t2b-1|t3-1|t4-1|t4-2`)" can be read two ways.

Evidence: "the panel's own" suggests the three ids of the running panel. The parenthesis lists all five, and the post-check at line 407 checks all five. If an implementer rewrites only the panel's three ids, a report on a different panel that mentions another panel's id would be recorded `anon_failed`. Reports do not normally contain another panel's ids, so the effect is small.

Fix: say "every id from `t1b-1|t2b-1|t3-1|t4-1|t4-2` that occurs in the report, mapped to `R1..Rn` in sorted order".

## What else I checked (no defect)

- Line 406 cites `MR:953` correctly: it says the judge "cannot tell which arm a report came from".
- No new ground-truth path or text reaches a reviewer or the judge. The redaction count goes only to `results/scoring-keys.jsonl`, which is outside the judge's `scoring/` tree.
- The case-insensitive move-id rewrite cannot alter a candidate quote, because all three candidates give 0 matches.
- The only new write location the edits add is `/tmp/evalsb-collab-r5/pytest`, which is inside `SB`.
- T-19 (line 493) agrees with lines 406-407, and line 69 agrees with section 6.
