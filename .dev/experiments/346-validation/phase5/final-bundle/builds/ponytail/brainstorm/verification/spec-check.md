# Spec check: 346-ponytail SPEC.md (independent adversarial verification)

Target: `.dev/brainstorms/346-ponytail/SPEC.md` (328 lines). Read-only check, 2026-11-08. `E` = `exp346-p1-logs/.dev/experiments/346-validation`, `F2` = `exp346-ab-flg-r2/.dev/orca-command-refactor`.

verdict: FAIL

## Blocking problems

| # | Location in SPEC | Problem | Evidence | Smallest fix |
|---|---|---|---|---|
| B1 | 2.3 step 1 (id match, `foreign-id` class), 2.4 brief ("one row per finding id in fix-list.md"), 3.3 K3 | The id rules contradict each other and do not fit S1. (a) Ids are matched only from "ids that the R2 report itself defines", so a hunk citing only other ids is found as no-id (`unattributed`); `foreign-id` can never be detected. (b) The spec gives "cycle-1 ids" as the foreign example, but the S1 Arm B review-2 reports restate every cycle-1 id with a blocking yes/no column. (c) If cycle-1 ids are foreign and listed in fix-list.md, the brief requires a row for them and K3 ("every id exists in R") fails the whole audit. If they count as defined, their grade form (`\| F16 \| no \| open`) is not among the four parsed formats. In that case they are read as unknown, so blocking, and many minor-only hunks become blocking-involved. Then the 27% revert share (measured with N/C ids only) does not carry over to growth 27% in 2.8 and 5. | `F2/review/spec-panel-round2.md:42,50,224` (all 22 prior ids graded); cycle-2 diff v2 to v3 adds lines citing F10 (5x), F2 (4x), F22, F1 (3x), F14, F21 and others; `enrichment/minor-byte-share.md:5` (id sets N/C only) | Define "ids R2 defines" as ids R2 grades in its new-findings list or citation notes. Every other id-shaped token is foreign. A foreign-id hunk gets one `-` row and counts as blocking-involved (protected). K3 accepts `-` rows for it. State that 2.8's 2.5-point growth term assumes this rule, or re-measure with it. |
| B2 | 3.1 row 1 and 3.2 (variant command text) | The variant keeps Review Loop bullets 1-7 byte-identical. Bullet 4 says every run is one review and that with `--re-review` the command "writes no revised specification". The design note's D4 says `--re-review` "is critique-only and never revises". The Fix Audit line passes `--re-review` and `--baseline` (without `--mode critique`) and edits the spec through the script. No sentence says that Fix Audit overrides those bullets or the Behavioral Flow. The variant file therefore contains two opposite rules for the same invocation, and only prose obedience decides between them (3.6 admits step 6 is prose). | `src/superclaude/commands/spec-panel.md:258,261`; `docs/designs/spec-panel-review-loop.md:176`; SPEC.md:193-195 | Add to Fix Audit item 1: "With `--fix-audit` the run is not a review. The Behavioral Flow and Review Loop bullets 1, 4, 5 and 6 do not apply, it does not count toward the cap, and the scripted edit is the one exception to bullet 4." Pin that sentence in `test_spec_panel_ponytail.py`. |
| B3 | 5, predicted numbers table vs 2.8 | The point predictions disagree with each other. The mean of 3.2 implies an effect of -0.3. "About 5 and about 1" per replicate implies a mean of 3.0 and an effect of -0.5. The paired effect is given as -0.4. 2.8's own derivation (-0.35 to -0.5 plus 0.15 to 0.25) nets to -0.1 to -0.35, so -0.4 lies outside it. "About 5 and 1" (mean 3.0) also conflicts with the "about 40% chance of 3 or lower". | SPEC.md:141,147,154,279-281,289 | Paired effect: -0.3 (0 to -0.8). Per replicate: about 5.3 and about 1.2. |
| B4 | 5 table row "On the 427-only base", 2.8 derivation P | Growth "about 26%" on the 427-only base (29.7%) takes the flg revert channel. The cited debate file measures the trt runs' minor-only share at 10% of cycle-2 characters (not 27-33%). By 2.8's own method that is about 1 point plus about 0.5 for shrinks, so about 28%, not 26%. | `nested/.../round2-B.md:28-29,35`; SPEC.md:147,287 | Change to "growth about 28%" (or drop the row). |

## Minor notes

- 2.7 step 5 "never turns a FAIL into a PASS" holds only in `427` mode. In `any-severity` mode (the S1 mode) the stricter-of-two cross-check is skipped. If review 3 lists a reverted minor id as open blocking (the upward label drift that 1.2 itself names), the script removes it and the result rests on a printed line only. Suggest printing `consistency: DISAGREE` and FAIL whenever a closed id appears in review 3 as open, regressed or blocking.
- 2.3 step 4 and 3.3: `apply` "re-checks" before applying, but after a first apply the spec sha no longer matches `state.json` (K1). A rerun therefore gives CHECK_FAIL, not "already applied", unless the idempotency test runs first. Say that it does.
- 4, T08a brief: `worker_done --report-path .../fix-audit/apply-log.md`, but only `apply` writes that file. On not-triggered, skip or CHECK_FAIL it does not exist. Report `state.json`, or have every path write `apply-log.md`.
- 2.2 trigger "R2 header is `review: 2 of 3`": in flg-r2 that line is line 19 and carries trailing text (`review: 2 of 3 (prior report ...`). In flg-r1 it is line 1, bare. Specify "a line starting with `review: 2 of 3`" so S1 does not silently not-trigger.
- 2.3 says `--dispositions` defaults to the file beside R2, but 3.2 says "without it no hunk is reverted whole". Pick one.
- 3.3 heads K1-K10 "each fails the whole audit", but K6 only logs DOWNGRADE/UPGRADE and K9's "strongest verdict wins" resolves a tie (REVERT_SHARED, 2.6). Separate the failing checks from the resolution rules.
- The disposition "Where" column is `SPEC':N` single lines (`F2/review/disposition-round2.md:19-33`). The parse rule for "line range listed under a blocking id" is not stated.
- 1.1 "open critical+major" is the recorders' proxy count of new review-3 findings (`E/phase4/AB-REPORT.md:13,19`), not an open count. 5 says so; 1.1 and 2.8 do not.
- 1.2 89%/100% come from the treatment-A reports (`AB-REPORT.md:30`), not Arm B. 1.4 and 2.8 say "bytes" for measured characters (`minor-byte-share.md:7`).
- The growth bar is 44.4% in D11 (`E/DECISIONS.md:64`) and 44.5% in D12 and ARMB (`DECISIONS.md:68`, `ARMB-REPORT.md:24`). The spec's 44.4% matches D11. A one-line note would help.
- 4 calls the 486-line master "427 text". The S1 arm's original is the 472-line exact 427 file (`ARMB-REPORT.md:6`). The drift test therefore guards a different base than the one the experiment runs. This is harmless for T08a but worth one sentence.

## Self-Audit (what I checked)

- Section 1 numbers: 6.0/5.5/3.5, runs 6 and 1, 63.5/29.7/30.0% (AB-REPORT.md:19, ARMB-REPORT.md:13,20); 89/100% (AB-REPORT.md:30); flg-r1 6 vs 4 (ARMB-REPORT.md:13-14); flg-r2 15 of 15 rows, 9 minor (evidence-attribution.md:124; disposition-round2.md:35); A/B/C/D = 1/7/12/8 of 28 and the 0.2 per run (evidence-attribution.md:138-161, recounted); 6%/27% and 33/27/10/10% (minor-byte-share.md:9-10; round2-B.md:26-29); T09 quote (T09 template line 1). All correct.
- 2.5: ponytail 5.3.3 pin (installation.md:346,363-368); the SKILL.md output format, "changes no code" and the default target (SKILL.md:18-19,74-101); the worker Skill load observed (F2/review/spec-panel-round3.md:31). All correct.
- 2.8: Arm B base and class means over critical+major (A 0.5, B 1.0, C 1.0, D 1.0), with R2-7 graded `MAJOR (FR-8 GAP) | minor` (flg-r1 spec-panel-round2.md:151); 22 of 25 and the 6% cycle-1 share (round2-B.md:39,53); arithmetic re-derived (see B3, B4).
- 3.x and 4: spec-panel.md is 486 lines, Review Loop at 256-264, Usage at 22-23; qa.md:91 quote; README.md:30; D9 (DECISIONS.md:46); test_routing_plugin_parity.py:41-47; test T3 seven bullets (test_spec_panel_review_loop.py:83-90); managed-workspace.md:54 pattern; apply_rows.py "STOP, nothing written"; C6 in the design note; coordinator-log.md:48 (07:47Z readiness failures).
- Item 4: every T08a path exists in F2 (spec 76,328 B; review/spec-panel-round2.md 251 lines, last line `verdict: FAIL`; specs/history/spec-v2-after-round1.md 70,255 B; review/disposition-round2.md), plus spec-v3-after-round2.md for the paired fork.
- Item 2: the revert/restore/delete rules agree across 2.3, 2.4, 2.6 and K6-K9 except B1 and the minor notes; the 2.2 and 3.2 triggers agree except the readable-files clause (2.2 only) and the dispositions default.
- Item 3: all seven sections are present; the variant name and the predicted review-3 (3.2) and growth (27%) numbers are given.
- Not checked: the T05-T08 templates, the ctl/trt run folders beyond the cited lines, metrics.json files, and any script run.

## Re-check after revision

I re-read the revised SPEC.md (332 lines: 2.3-2.4, 2.6-2.8, 3.2-3.5, 4, 5) and the "Re-measure after verification" section of `enrichment/minor-byte-share.md:17-23`. I also re-ran a read-only count of flg-r2 cycle 2 (v2 to v3, 21 hunks, 6,301 added characters) with a scratch script in `/tmp`.

verdict: FAIL

| Item | Status | Evidence | Smallest fix |
|---|---|---|---|
| B1 id rule (2.3), brief (2.4), K3 | Fixed. "Ids R2 defines" excludes ids that only appear in the prior-status table. Foreign-id hunks are protected and get a `-` row. K3 matches the brief. | SPEC.md:36-39,72-73,97,104-105,215 | none |
| B1 numbers: 23%, growth 28% | 28% holds. 23% is one reading of an under-specified rule (minor note M1). | my re-count; SPEC.md:150 | none blocking |
| B2 override sentence and pin | Fixed. The sentence is present and pinned; one literal mismatch remains (minor note M2). | SPEC.md:196,238 | none blocking |
| B3 2.8 vs 5 | Fixed. Per replicate 6-(0.7 to 1.0)+(0.15 to 0.25) gives about 5.4, and 1+(0.15 to 0.25) gives about 1.2. Their mean is 3.3 and the paired effects are -0.6 and +0.2, mean -0.2. The 35% chance appears in both 2.8 and 5. | SPEC.md:144,150,157,283-285,293 | none |
| B4 427-only base | Fixed. Review 3 is 5.5-(0.35 to 0.5)+(0.15 to 0.25), about 5.3. Growth of about 29% is close: 10% of the trt cycle-2 characters (about 7,450) times 70% is about 0.9 points, not 0.5, which gives about 28.3%. That is within rounding. | SPEC.md:150,291; round2-B.md:28-29 | optional: "about 28 to 29%" |
| R1 (new) 2.7 step 3 vs S1 review 3, 2.6 reason (1), 3.5 | **Blocking.** Step 3 now forces FAIL whenever a closed (reverted minor) id appears among the open rows. On S1, review 3 lists every round-2 finding, minor ones included, in its status table: T09 says "for each round-2 finding {{R2_FIRST_ID}}-{{R2_LAST_ID}}", and flg-r2 review 3 has rows N7-N11 and C9-C14 with blocking `no`. A reverted minor fix will be reported `open`, so every audit that reverts anything forces FAIL. 2.6 reason (1) ("never in review 3's prior-blocking table") is false for S1. The 3.5 test "a closed-minor id listed open is removed and printed" contradicts the new step 3. | SPEC.md:121,128-132,235; T09 template line 1; `F2/review/spec-panel-round3.md:37-45` | In 2.7 step 2, count a prior row only when its blocking column says yes, or when R2 graded that id blocking. Raise DISAGREE/FAIL only when review 3 grades a closed id blocking. Reword 2.6 (1) to "review 3 may list it, as a non-blocking row the script ignores". Change the 3.5 verdict test to match. |

Minor notes (re-check):
- M1. The 23% figure (1,468 of 6,301) depends on two choices that 2.3 does not pin down: what counts as an "id-shaped token", and how "ids already in the baseline text" is tested.
  - A literal positional word diff with finding-id shapes only (N, C, F, R2-n) gives 789 characters (12.5%). Moved cycle-1 ids (F21 at v3:11, F14 at v3:69, F3 at v3:112, all present in the v2 lines) then land in "added words" and make three hunks foreign.
  - A per-line "present in the baseline line" test with the same id shapes gives 1,726 characters (27%).
  - 23% matches the per-line test only if non-finding tokens such as `WC-5` (new at v3:228, beside N8) count as foreign ids.
  - Growth stays 27.4% to 28.5% across all three readings, so 28% (26 to 29) holds.
  - Fix: state the id pattern (finding-id families from R2 only) and "context = the token occurs in the hunk's baseline lines".
- M2. The 3.5 static pin quotes `With --fix-audit the run is not a review`, but the 3.2 text has backticks around `--fix-audit`, so an exact-substring test fails. Pin "the run is not a review", or pin the backticked form.
- M3. The brief's parenthetical "every hunk that cites no such id (class unattributed or foreign-id)" is looser than 2.3: a foreign-id hunk may also cite an R2-defined id. K3 still works, because such a hunk is covered by that id's row.
- Confirmed fixed from the first minor notes: the apply idempotency order (2.3 step 4), the T08a report path (`state.json`, written on every path), the header match (a line starting with `review: 2 of 3`), the dispositions default, the K-list header, "new review-3 findings" in 1.1 and 5, and the 44.4/44.5 note.

## Final re-check

I re-read SPEC.md 2.3 (lines 35-41), 2.6 (120-126), 2.7 (128-135) and 3.5 (227-240). I also re-counted flg-r2 cycle 2 under the rule exactly as now written: the regex from 2.3, a per-hunk multiset difference, R2-defined ids N1-N11 and C9, C12-C14, listed-only ids F1-F22, other tokens ignored. I used a scratch script in `/tmp`, since removed.

verdict: FAIL

| Item | Status | Evidence | Smallest fix |
|---|---|---|---|
| Open-row problem (R1) | Fixed. 2.7 step 2 counts a resolution row only if R2 graded its id blocking. A reverted minor id that review 3 lists as open is printed, not counted. DISAGREE/FAIL fires only when review 3 grades a closed id blocking. This fits T09's "for each round-2 finding" and flg-r2 review 3's rows N7-N11 and C9-C14. | SPEC.md:131-132; T09 template line 1; `F2/review/spec-panel-round3.md:37-45` | none |
| 2.6 (1), 2.7, 3.5 agreement | Agree. 2.6 (1) now defers to 2.7's R2-blocking filter. The 3.5 verdict test matches steps 2-3 and limits the stricter-line rule to `427` mode, as the 2.7 header does. The pin `the run is not a review` is a substring of the 3.2 sentence. | SPEC.md:125,129-135,196,235,238 | none |
| F1 (new) measured share vs the rule as written | **Blocking (wrong number).** 2.3:40 says "Measured on flg-r2 cycle 2 with this rule: 1,468 of 6,301 (23%)". 23% needed `WC-5` (new on v3:228, beside N8) to count as a foreign id, and the revised rule now ignores such labels. With the rule as written, that hunk is minor-only: 1,726 characters (27%). With the regex taken literally, the range `N1-N11` on v3:5 is one token, R2 neither defines nor lists it, so it is ignored, and the revision-note hunk is also minor-only: 2,067 characters (33%). 2.8:150 ("23% ... about 2.5 points") and the 5 table reference "flg-r2 minor-only 0.23" (SPEC.md:288) carry the stale figure. Growth stays inside the stated band: 30.0 - 0.7 x (3.0 to 3.6) - 0.5 = 27.0 to 27.4%, so the central 28% becomes about 27%. | SPEC.md:37,39,40,150,288; flg-r2 `specs/history/spec-v2-after-round1.md` vs `spec-v3-after-round2.md` lines 5, 228 | Replace 23%/1,468 with 27% (1,726; 33% if ranges are not expanded). In 2.8 use about 3.0 points, giving growth about 27% (26 to 29). Change the 5 reference cell to 0.27. |

Minor note (final): the regex reads a range such as `N1-N11` as one token and ignores it. A hunk that cites a blocking range plus one minor id would be classed minor-only and could be reverted whole. Review 3 would then see the blocking finding unresolved and the verdict would count it, so this is not a silent PASS, but it wastes the revert. Fix: expand `X<a>-X<b>` ranges before matching, and add a unit test.
