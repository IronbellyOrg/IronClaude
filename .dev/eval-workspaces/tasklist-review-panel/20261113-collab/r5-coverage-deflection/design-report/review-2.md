verdict: FAIL

Second independent review of `r5-coverage-deflection/DESIGN.md` (597 lines, read in full) against `review-1.md`, `merged-requirements.md` (MR) Redesign 5 (803-893), section 4 conduct (925-976) and section 5 (1030-1100), and the harness files `run-reviewer.sh`, `judge-one.sh`, `anon-b11.sh`, `merge-b11.sh` and `combos/SPEC.md`. All 14 review-1 findings are fixed. The fixes added 2 blocking and 3 minor defects.

What I checked and found correct: the pinned sha256 values of `judge-one.sh` and `run-reviewer.sh` still match; the k formula with the 1e-9 term gives every T-12 k case as stated (computed with `uv run python`: 23.79 gives 2, 23.80 gives 1, 51.79 gives 1, 51.80 gives 0, and the (100, 6.4, 13.8) and (238, 23, 12.3) boundaries give 1); the per-package thresholds in 3.1 and 3.2, and the planned-end, finish-bound and hang-guard figures; `merge-b11.sh:11-12` already maps `t4-2`; `SPEC.md:4` ("~40k tokens") and `SPEC.md:99` (10 concurrent reviewer sessions) are quoted correctly; none of the three candidates contains a move id or one of the new redaction phrases, in either case (grep -ciE count 0 on each); the re-ask model check matches MR:933, MR:953 and R-28; D11 now reads MR:951/953 correctly and the judges run one after another (DESIGN.md:415, 454); the keys file sits outside the judge's `scoring/` tree (DESIGN.md:118, 405); the transcript audit lists `.claude/projects` and the live repository path, and T-18 has a case for the first; AC-4 now matches R-27 and REQ-S3; nothing in the fixes sends ground truth or peer conclusions to a reviewer.

## Review-1 findings: fixed or not fixed

| # | Review-1 finding | Status | DESIGN.md line |
|---|---|---|---|
| 1 | T-12 k cases contradict the k formula | Fixed (the k cases are now correct; the slowdown cases in the same row fail, see N1) | 246, 486 |
| 2 | Re-ask session model never checked | Fixed: `jq -s` through the RR:50-56 filters, `reask_model_ok`, the mismatch keeps the original report, audit row, T-10, F-9(c) | 280, 330, 484, 510 |
| 3 | Arm-identifying text reaches the judge | Fixed as proposed (the new move-id rewrite has a defect, see N2) | 406-407, 493 |
| 4 | Thresholds rounded up | Fixed: 18.65, 46.65, 22.15, 50.15 | 347 |
| 5 | "(adding `t4-2`)" is wrong | Fixed: "(which already include every id used here)" | 400 |
| 6 | `SPEC.md:4` misquoted | Fixed: "about 40k output tokens in total ... whole review" | 355 |
| 7 | Spike 5 declared not needed, but R-27 requires it | Fixed: AC-4 requires a recorded result or waiver; Q5 added | 531, 558, 592 |
| 8 | AC-4 requires a PASS for REQ-S3, which has no threshold | Fixed: measured rates plus the owner's decision | 558 |
| 9 | D11 misreads MR:953; judges not counted | Fixed: stated as a stricter self-imposed cap; judges run one after another | 65, 415, 454 |
| 10 | Transcript read routes to peer conclusions not flagged | Fixed: `.claude/projects` and the repository path are forbidden; T-18 case added | 328, 492 |
| 11 | Test command writes `.pytest_cache` outside R5 | Fixed in 6 and AC-1/AC-2 (line 69 still shows the old command, see N3) | 469, 555, 556 |
| 12 | Launch interface inconsistent (`SPIKE4`, `--pkgs`) | Fixed | 148, 384 |
| 13 | Meta read half-written; API-error attempt counted as usable | Fixed: temp file plus `mv`; `api_error: false` required (T-8 has no case for it, see N4) | 197, 268, 270 |
| 14 | Key file beside the judged folder | Fixed: `results/scoring-keys.jsonl` | 118, 405 |

## New findings

### N1. blocking. DESIGN.md:486 (T-12): the two slowdown-limit cases fail under the `pytest.approx` comparison the fix prescribes.

Evidence: the fix added "Floats are compared with `pytest.approx`". The default tolerance of `pytest.approx` is relative 1e-6. The formula at DESIGN.md:250, `s_max = (0.35 B - W) / B` with `W = 2 + 2k turn_p90`, gives (273.7, k = 2, 14) = 37.795 / 273.7 = 0.138089 and (116, k = 2, 6.4) = 13 / 116 = 0.112069. With `uv run python`, `s == pytest.approx(0.138)` and `s == pytest.approx(0.112)` both return `False`. The hang-offset and finish-offset cases pass. AC-1 (DESIGN.md:555) requires 0 failures, so an implementer who follows the stated text writes two failing assertions. This is the same class of defect as review-1 finding 1.

Fix: state the values as `pytest.approx(0.1381, abs=5e-5)` and `pytest.approx(0.1121, abs=5e-5)`, or keep 0.138 and 0.112 with `abs=1e-3`. Say the tolerance in the T-12 row.

### N2. blocking. DESIGN.md:406-407 (anonymiser): the move-id rewrite is case-sensitive but the post-check is case-insensitive, and reviewer finding ids collide with move ids. Ordinary packages in every arm, A1 included, become `anon_failed` and go unjudged.

Evidence: DESIGN.md:406 rewrites `\bM(10|[1-9])\b` to `<move>` and marks only the phrases as case-insensitive. DESIGN.md:407 then runs `grep -ciE '...|\bM(10|[1-9])\b|...'`, where `-i` also matches `m1`-`m10`. Reviewers use `M<n>` and `m<n>` as their own finding ids, and the merge prints them in ledger headings. For example, `r1-haiku-luna2/TASK-WF-makeTheAliasOnly-20261105-051649/R/merged-anon.md:53` has `#### L1.R2 (m1)`, and other reports have `#### L1.R2 (M4)`. Of the 310 historical `merged-anon.md` files under `EVAL/arms/scoring/combos`, 32 match the move-id pattern case-insensitively (none of these runs had the kit), and 6 contain lowercase forms. After the stated rewrite, those 6 still match the post-check, so they would be recorded `anon_failed` and not judged. The row then becomes `partial`, and this happens in A1 as well as F6. The case-insensitive reviewer-id part of the same post-check also rejects 3 more historical files (`Task-6`, `passes-after-Task-2`, `T1bModel01-03`), because the `anon-b11.sh:17` rewrite it copies is case-sensitive. That part may predate the fixes. In total, 9 of 310 (about 3%) of ordinary reports would be dropped, against arms of n = 12. A second problem is the note that "no candidate quote is changed". It is true, but the rewrite also renames reviewer finding ids, which are not moves, and `<move>` is a token found nowhere else in the reports. Its rate rises with the kit, so it is a weaker arm marker than the neutral `<redacted>` that already appears in every arm's reports (`report <redacted>`, `anon-b11.sh:25`).

Fix: run every rewrite with the same case-insensitivity as the post-check. Replace move ids with `<redacted>`, not `<move>`. Restrict the reviewer-id rewrite and post-check to the panel's real ids (`t1b-1|t2b-1|t3-1|t4-1|t4-2`, case-insensitive), not the generic `\bt[0-9a-z]+-[0-9]+\b`. Add T-19 cases: a `#### L1.R2 (m1)` heading and the prose `Task-6` come out with a zero post-check and the package is judged.

### N3. minor. DESIGN.md:69: the test command still lacks `-p no:cacheprovider`.

Evidence: line 69 says "tests as `uv run pytest R5/tests`". Lines 469 and 555 now add `-p no:cacheprovider` to keep `.pytest_cache/` out of the repository root. Anyone who runs the line-69 form writes outside R5, and the new AC-2 check `find REPO -maxdepth 1 -newer` then fails.

Fix: use the line-469 command at line 69.

### N4. minor. DESIGN.md:482 (T-8): no test covers the new `api_error: false` condition of the watcher.

Evidence: DESIGN.md:197 now requires `api_error: false` before a scout attempt counts. T-8 tests `model_ok: false` and a missing block only.

Fix: add the case "a meta with `model_ok` and `findings_block` true but `api_error: true` posts nothing and logs `scout_unusable`".

### N5. minor. DESIGN.md:469, 482, 496, 556: test temporary folders are written outside `R5/` and `SB/`.

Evidence: T-8 ("temp run dir") and T-22 ("a temporary git repo") use pytest's default base temp, `/tmp/pytest-of-<user>/`, which is outside both allowed roots. AC-2 says nothing outside `R5/` and `SB/` is written by the build. This did not come from the fixes and review 1 did not raise it, but it is a write outside the allowed folders.

Fix: add `--basetemp=/tmp/evalsb-collab-r5/pytest` to the commands at lines 69, 469 and 555. pytest clears that folder at each run, and it is inside `SB`.
