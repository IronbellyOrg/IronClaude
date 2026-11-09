# QA Report - Qualitative Fix Verification, Phase 6, Fix Cycle 2 (Gate 3 agent 2 of 2)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Phase:** fix-cycle (report-qualitative), fix_authorization: false
**Report line numbers** are those of `RESEARCH-REPORT-bmad-first-use.md` as read in this session (1795 lines).

---

## Check (a): the five Blocking = yes rows, resolved by substance?

| Row | Finding | Result | Evidence |
|---|---|---|---|
| 1 | F-1 D2 left at S | RESOLVED | L1137 (D2 cell: "L as planned", S kept as researched minimum, 8 files named), L1227 (Table 1 D2: "L as planned (8 files; S on the researched minimum, 4 files...)"), L1299 (Stage 1 "Why" names D2 (8 files)). Recount by the rubric at L1004: new `20-*.json`, `Dockerfile.coder`, `main.tf`, `test-73`, `manifest.yaml`, `README.md`, new first-use test (step 5.3), `coder-ci-aidev02-contract.yml` driver row = 8, so L. Deviation from the proposed M is correct (M would break the 8-file rule). |
| 2 | B-1 gate order | RESOLVED (one nuance, N-3) | One order now at L1300 (Stage 2), L1463 (Phase 4 heading), L1478 (gate heading "before relying on any branch ... candidate build ... drafted and not shipped"), L1488 (Rule: failed Fact 1 discards the draft), L1669 (checklist), L1694 (Section 9 row 4), L1705 (row 15). Grep for "Gate before any branch" and "observed before B or D" found no survivor. |
| 3 | B-2 open defaults as constraints | PARTLY RESOLVED (residual N-2) | Phase 3 header L1452, step 1.1 L1383, Stage 0 (c) L1298 and checklist L1656 now say `--type assumption` / `--type question`, with `--type constraint` only for step 3.6. Source check: `.claude/skills/bmad-spec/SKILL.md:54` (memlog canonical, append-only, never edited), `:61` (types include assumption and question), `_bmad/scripts/memlog.py:164-177` (`cmd_append` only appends; `--type` is free text, `:209`) all confirm. Residual: step 3.6 itself contains an item that the report calls open (see N-2). |
| 4 | B-3 "cheapest" | RESOLVED at the two named places, residual wording elsewhere (N-1c) | L1091 now "Lowest risk of the three (no certain break, 0 layers)"; L1311 Rationale 4 rests on Risk, Image layers, HOME persistence and names Effort (L against S for B1) and Image rebuild as the price; L1299 and L1311 agree. The fix log's grep for `cheapest` could not find L367 "the cheap variants" (B2, B3, D2, D3), which now conflicts with ratings M, L, L, L. |
| 5 | B-4 "template push only" | PARTLY RESOLVED (residual N-1a, N-1b) | Consistent at L1083, L1087, L1091, L1141, L1234, L1311, L1494, L1515, L1615 (step 7.7), L625 (K-05), L1691. Source check: `main.tf:74` (`catalogue_sha256` hashes `catalogue/**`), `main.tf:104-107` (folded into `image_inputs_sha256`), `main.tf:111` (image tag), `Dockerfile.coder:593` (`COPY --chown=0:0 catalogue /catalogue`, existing COPY, 0 layers) all confirmed. Two rows of Table 1 still describe B3 and D3 as `modules.tf` only. |

## Check (b): claims no stronger than evidence; recommendation, plan and tables consistent?

Focus asked for: does re-rating B3 and D3 to L and removing "cheapest" leave Section 7's recommendation, Rationale and Section 8's plan consistent?

| Point | Result | Evidence |
|---|---|---|
| Section 7 Stage 1 "Why" vs Rationale 4 | CONSISTENT | L1299 says Effort is L as planned for B3, D3 (template push plus retag) and D2 (8 files), M for C, and therefore does not favour B3 or D3 over B1 and D1 (S); Risk and Pinned-tests rows separate them. L1311 grounds B3 on Risk (Medium, R2 only), Image layers, HOME persistence and names L Effort as the price. The B3 recommendation no longer rests on Effort. |
| Rationale 4 "highest Effort of the skill deliveries as planned (L, against S for B1)" | TRUE | Options B cells L1087: B1 S, B2 M, B3 L. |
| Section 8 plan vs rating | CONSISTENT | 4B.1 (L1494) and 4D.1 (L1515) say the resource alone is a template push and 4B.6 / 4D.7 add the retag; 4B.6 (L1499) and 4D.7 (L1521) do edit `manifest.yaml`; step 7.7 (L1615) and step 2.5 (L1403) say the same; Section 9 row 1 (L1691) agrees. B3 file count 6 (`modules.tf`, `manifest.yaml`, `README.md`, `test-52`, new test, driver workflow) and 2 new tests: M by files and tests, L by two delivery layers, as the cell states. |
| Gate order across Section 7 / 8 / 9 | CONSISTENT | See check (a) row 2. |
| Q1 / Q2 handling after fixes | UNCHANGED | The fixes added no claim that a stub is allowed or what "first use" means; step 1.1 still forbids it (L1383). |
| Table 1 rows other than Effort and Image rebuild | NOT CONSISTENT | See N-1a, N-1b: "Integration complexity" and "Pinned tests that break" still describe B3 and D3 as `modules.tf` only. |
| Section 2.4 wording | NOT CONSISTENT | N-1c: "the cheap variants" at L367. |
| Open-record handling | NOT FULLY CONSISTENT | N-2. |

## Check (c): Feasibility statement and both owner questions

| Item | Result | Evidence |
|---|---|---|
| Feasibility statement | PRESENT AND CORRECT | L1319-1325: both questions answered "Yes" with the 01, 03 evidence and "Stop condition: not triggered"; Section 9 row 4 (L1694) restates it; Section 8 intro (L1355) repeats it. Wording "not supported by code-traced evidence; owner decides" still used for (no, named skill) and (no, session). |
| Q1 unanswered | PRESENT | L1339 ("copied unanswered") and Section 9 row 1 (L1691, "Owner Q1 (unanswered)", resolution "Ask the owner"). |
| Q2 unanswered, with sub-questions | PRESENT | L1339, Section 9 row 2 (L1692, "Owner Q2 (unanswered)", sub-questions under (a) and (b)). |
| No answer written by the fixes | CONFIRMED | Fix log L46 says none; the reading of L1283-1294 and L1341-1347 shows only branches, not choices. |

## Issues found

Blocking (unresolved or new):

| # | Severity | Blocking | Report location | Issue | Required fix |
|---|---|---|---|---|---|
| N-1 | IMPORTANT | yes | Section 6 Table 1, rows "Integration complexity" (L1230) and "Pinned tests that break" (L1236); Section 2.4 (L367) | Same defect as row 5 (B3 and D3 described as `modules.tf` only), left in three other places. (a) L1230 gives B3 "1 file (`modules.tf`) + 1 pin" and D3 "1 file + 1 pin", while the Effort cells of the same table (L1227) say 6 files, 2 or 3 new tests and two delivery layers as planned; D2 "3 points + 1 test" against "8 files", and C "1 RUN group" against M with a helper, new test and driver row, are unlabelled researched minima. (b) L1236: the B3 and D3 cells list only `modules.tf` conditional breaks (`test-52`, `test-51`, `test-startup-boot`) and omit `test-19:517-529`, `test-49:326` and `test-2-manifest-schema.sh`, which the plan's own Table 5.1 (L1568, L1571, L1576) says the planned welcome-text edit (steps 4B.6, 4D.7) must keep green and which the Option A cell of the same row lists. (c) L367 still calls B2, B3, D2 and D3 "the cheap variants" (the fix log's grep for `cheapest` could not find it) while Table 1 rates them M, L, L, L. A reader comparing B3 sees "1 file" next to "L". | Label the "Integration complexity" row cells "researched minimum" or add the as-planned count (B3 and D3: `modules.tf`, `manifest.yaml`, `README.md`, test pin, new test, driver row); add `test-19`, `test-49`, `test-2` BREAKS-IF to the B3, D3 (and D2, C) cells of L1236 or state that the Table 5.1 rows apply; replace "cheap variants" at L367 with "these variants". |
| N-2 | IMPORTANT | yes | Section 8 Phase 3 header (L1452), Section 7 Stage 0 (c) (L1298), step 3.6 (L1461), step 1.1 (L1383) | Row 3 is resolved for steps 3.2 to 3.4 but not completely. L1452 and L1298 record "the fixed prohibitions of step 3.6" as `(constraint)` bullets in the append-only memlog, but step 3.6 (L1461) also holds the rule that a stub "must not start with `bmad-`", which the same step, Limits row 1 (L1331) and Section 9 rows 2 and 3 call open ("whether the owner wants a literal `/bmad-*` name despite the shadowing risk is open") and which rests only on doc-only W01-2. An implementer following L1452 would write that open, doc-only rule into the owner's record as a constraint that only a superseding bullet can reverse (`SKILL.md:54`). Related: step 1.1 (L1383) puts "assumption D-9, pending owner" inside the `(decision) Owner 2026-11-07` bullet, although Section 9 row 8 (L1698) says D-9 awaits owner confirmation. | Split step 3.6: record the code-pinned prohibitions (seed-repo-path, `~/.claude` scope, test-3 reserved words, packaged and Orca names, `sc-` names) as `--type constraint` and the `bmad-` prefix rule as `--type assumption` ("plan default pending owner, Section 9 rows 2, 3"); make step 1.1 record D-9 as a separate `--type assumption` bullet instead of inside the decision bullet; say so in L1298 and L1452. |

Notes (MINOR, not blocking, counted separately):

| # | Report location | Note |
|---|---|---|
| N-3 | L1463, L1478 | Heading and Phase 4 title say no branch is relied on before the gate, but Facts 1 to 3 and the candidate-build steps are defined only for B (4B.1, 4B.2) and D (4D.1 to 4D.3, 4D.6); branch 4C has no gate steps, so the sentence cannot be satisfied literally for 4C. Say "B and D branches". |
| N-4 | L1112, L1227 | Option C "M as planned": no file count is shown. Count from steps 4C.1, 4C.3, 4C.5, 5.3, 5.4: `Dockerfile.coder`, helper, `main.tf`, `manifest.yaml`, `README.md`, new test, driver row = 7 (M); 8 (L) if the `test-60` extraction check of step 5.4 is added. The fix log (L40) flagged this and did not recount; UNVERIFIED which side of the 8-file line it falls on. |
| N-5 | L1056, L1403 | Option A says the `manifest.yaml` welcome text is "an optional second file", but Stage 0 (b) and step 2.5 edit it under every reading, so the image retag arrives with Stage 0 for every option; the "price" statements for B3 and D3 (L1311, L1615) are true as planned but partly shared with Stage 0. Not wrong, but worth one sentence. |
| N-6 | L1372 | The gap-to-step map says F-10 and F-11 are "recorded as constraints", while L1452 now limits `--type constraint` to the step 3.6 prohibitions; the fix log's grep (`constraint` forms) did not catch "recorded as constraints". Clarify that it means the report's K-list, not memlog bullets. |
| N-7 | L1208 | The earlier N-1 of the cycle-2 findings (the `Dockerfile.coder:473-475` RUN also creates `/var/lib/aidev02` and `/etc/skel/.claude`) is confirmed by my Grep of `Dockerfile.coder:474-475`. Still open, MINOR. |

## Self-Audit

What I actively checked:

- Read the embedded prompt (task file line 409), the consolidated findings (29 lines) and the fix log (47 lines) in full.
- Read the report in full for L1-60, L316, L367, L625 and L990-1795 (Sections 6, 7, 8, 9 and 10: all option tables, Table 1 and 2, Stage table, Rationale, Feasibility, Limits, owner-reading table, all eight phases, integration checklist, Section 9 and the register). I did NOT read L61-989 in full (Sections 1 to 5); there I ran Grep for `B3|D3|D2`, `cheap|template push|push only|no rebuild|smallest|lowest effort`, the gate wording, and `constraint` forms, and read the hits (L204, L362-369, L524-525, L611, L625, L629, L741). A hidden contradiction elsewhere in L61-989 is UNVERIFIED.
- Reproduced against source: `templates/VSCode-AIDev02/main.tf:73-111` (catalogue hash, `image_input_files`, `image_inputs_sha256`, image tag), `Dockerfile.coder` Grep (L474-475 `install -d`, L500-501 drop-in COPY, L593 `COPY ... catalogue /catalogue`), `_bmad/scripts/memlog.py:116-119, 164-177, 209`, `.claude/skills/bmad-spec/SKILL.md:44-69`, `modules.tf:82` (`orca_retirement`), `test-52...sh:1374`, `catalogue/bmad/manifest.yaml:8, 14`, `coder-ci-aidev02-contract.yml:1234-1241` (driver rows). All cited lines matched.
- Recounted D2 (8 files) and B3 (6 files, 2 tests, two layers) and D3 by the rubric at L1004-1005; they agree with the new ratings.
- Searched for survivors of each fix: "Gate before any branch", "observed before B or D", `cheapest`, "template push only", `S (4 files)`: none. That search is what exposed L367 "cheap variants" (N-1c) and the Table 1 rows (N-1a, N-1b), which the fix log's own greps did not cover.

Why the count is credible: five prior blocking rows were each traced to every location named in the fix log and then to the neighbouring rows of the same table; three rows are resolved by substance (1, 2, 4 at the named places), two are resolved only at the named places (3, 5). I found 2 blocking and 5 minor items; a zero would not have been credible given that the same table still carried the old B3 and D3 description in two rows. I did not run any test, workflow or script, and I did not observe any CI result, so every statement about what a test would do is a reading of the report and of the cited source lines only.

## Confidence

- **Confidence:** Verified: 17 of 19 | Unverifiable: 0 | Unchecked: 2 | Confidence: 89.5% (checks: 5 rows + 3 consistency points + Q1/Q2/Feasibility = 9 items on the prompt, plus 10 residual-scan items; the 2 unchecked are the unread Sections 1 to 5 beyond Grep, and the Sysbox/CI facts the report itself marks UNVERIFIED). Below the 95% bar, so no PASS is eligible; the FAIL does not depend on it.
- **Tool engagement:** Read: 19 | Grep: 11 | Glob: 0 | Bash: 0

## Summary

- Prior blocking rows resolved in full: 3 of 5 (rows 1, 2, 4 at their named places); resolved in part: 2 of 5 (rows 3, 5).
- New or residual blocking issues: 2 (N-1, N-2), both IMPORTANT. CRITICAL: 0.
- MINOR notes: 5 (N-3 to N-7), not blocking.
- Feasibility statement and both owner questions: present, unanswered, correct.
- Counts check: 2 blocking + 5 minor = 7 items listed above.
- Fixes applied by me: 0 (fix_authorization false). No file other than this report was created or edited.

## Verdict

**FAIL**

Unresolved or new blocking issues: N-1 (Section 6 Table 1 rows "Integration complexity" and "Pinned tests that break", Section 2.4 L367) and N-2 (Section 8 Phase 3 header and step 3.6, Section 7 Stage 0 (c), step 1.1). The B3 and D3 re-rating and the removal of "cheapest" are otherwise consistent across Section 7 (Stage 1, Rationale 4), Section 8 (4B.1, 4B.6, 4D.1, 4D.7, 7.7) and Section 9 row 1.

## QA Complete
