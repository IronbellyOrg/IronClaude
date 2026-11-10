GATE3_DECISION: FAIL (cycle 1), second fix cycle required

Review count: review 1 (seven lens reports) and the cycle-1 verification (review 2) are done; the cycle-2 verification will be review 3. After cycle 2 any open blocking finding means HALT and ask the user.

SEVERITY_DOWNGRADES: 5

Source: `## Severity changes` of `qa/qa-consolidated-findings-phase6.md`. The consolidator downgraded 7 reporter IMPORTANT findings to MINOR; the orchestrator reversed the two on row 21 (TC#1, TC#2), so 5 stay downgraded. Findings downgraded from reporter IMPORTANT to MINOR:

- row 18: AC#7 IMPORTANT to MINOR (L1299 keeps the documented manual command and L1344 lists R-11 as an open labelled limit; no false claim; the observation gap for a built branch is blocking row 10).
- row 19: AC#8 IMPORTANT to MINOR (L1507-1508 state the hook script path is "a design choice not settled by the research" and install time is "UNVERIFIED (G-09)"; a conditional branch behind the row-8 gate with openly labelled choices).
- row 20: CR#5 IMPORTANT to MINOR (`install.sh:60` is `echo "[${SLUG}] install ok (marker: ${MARKER})"`, so L1318 and L1390 are true; missing anchor only).
- row 22: FR#1 IMPORTANT to MINOR and FR#6 IMPORTANT to MINOR (citations of `REPORT.md`, `04-bmad.md` and `.memlog.md:21` lack a directory; every cited line reproduces at the right file, so citation format only).
- Row 21 (TC#1, TC#2): downgraded by the consolidator, restored to IMPORTANT by the orchestrator (false statements about the report's own scope and method), so NOT counted.

Total downgraded findings: 5 (AC#7, AC#8, CR#5, FR#1, FR#6).

## Inputs read

| Report | Verdict | Counts |
|---|---|---|
| qa/qa-lens-template-conformance.md | FAIL | Critical 0, Important 2, Minor 12 |
| qa/qa-lens-internal-consistency.md | FAIL | Critical 0, Important 4, Minor 16 |
| qa/qa-lens-evidence-quality.md | FAIL | Critical 0, Important 1, Minor 7 |
| qa/qa-lens-actionability.md | FAIL | Critical 0, Important 8, Minor 5 |
| qa/qa-lens-domain-accuracy.md | FAIL | Critical 0, Important 1, Minor 10 |
| qa/qa-lens-crossref-chain.md | FAIL | Critical 0, Important 9, Minor 10 |
| qa/qa-lens-finding-reproducibility.md | FAIL | Critical 0, Important 2, Minor 8 |
| qa/qa-consolidated-findings-phase6.md | BLOCKING_COUNT: 18 | 69 rows |
| qa/qa-fix-log-phase6-cycle1.md | 18 fixed, 0 not fixed | |
| qa/qa-fix-verification-phase6-cycle1.md (structural) | FAIL | Critical 0, Important 1 (F-1), Minor 5; 17 of 18 rows fixed |
| qa/qa-fix-verification-qualitative-phase6-cycle1.md | FAIL | Critical 0, Important 4 (B-1 to B-4), Minor 3; 18 of 18 rows fixed in substance, 19 of 20 checks passed |

## Open blocking findings entering fix cycle 2

| ID | Report location | Finding |
|---|---|---|
| F-1 | report L1137 (Option D), L1227 (Table 1), L1299 (Section 7 Stage 1 "Why") | The row-4 fix re-rated Effort to M for B3, D3 and C but left D2 at "S (4 files)". Section 8 builds D2 for the (no, session) case (L1355, L1476, step 4D.6 L1520) and steps 5.3 and 5.4 add a new test file, a driver-table row and a second-file check in `test-73`; by the rubric at L1004-1005 that is M. Fix: re-rate D2 to M "as planned" in L1137 and L1227 and add D2 to the L1299 sentence. |
| B-1 | report L1477, L1463, Section 7 Stage 2 L1300, checklist L1669, step 4D.3 L1517 | Phase 4 gate cannot be run in the stated order: L1477 says "Gate before any branch" but the new procedure (L1482-1484) needs a candidate build of the chosen branch, and Section 7 Stage 2 and L1669 place the observation after building. Fix: reword L1477 to "Gate before relying on any branch: observed on the candidate build of the chosen branch (steps 4B.1-4B.2 or 4D.1-4D.3 drafted, not shipped)"; say in the Rule row that a failed fact 1 discards that draft; make Section 7 Stage 2, L1669 and L1463 use the same words. |
| B-2 | report L1452 (Phase 3 header), step 1.1 L1383 | Open owner defaults (git rule, guard, subfolder) are recorded as canonical `(constraint)` memlog bullets, but the memlog is append-only and these are open (step 3.4 L1459; Section 9 rows 5, 6, 10; Stage 0 (c) L1298). Fix: record the open items as `--type assumption` ("plan default pending owner, Section 9 rows 5, 6, 10") and `--type question` for owner inputs; keep `--type constraint` only for the fixed prohibitions of step 3.6; state in the CAP-8 success text that the command and predicate are defaults until rows 5, 6 and 10 are answered (`SKILL.md:61` lists assumption and question as valid types). |
| B-3 | report Rationale 4 L1311, Option B Pros L1091 vs Effort rows L1087, L1227 | Rationale 4 says "B3 is cheapest and least exposed" resting on the Effort row, and Option B Pros says "Cheapest", while the row-4 fix rates B3 M and B1 S and Stage 1 "Why" (L1299) says Effort does not separate them. Fix: replace "cheapest" with "lowest risk (no certain break, 0 layers)" in L1091 and L1311 and drop "Effort" from the rows Rationale 4 rests on (or state "S on the researched minimum, equal to B1"). |
| B-4 | report L1083, L1091, L1234, L1311, L1615 vs L1087, L1137, L1499, L1521, L1403, L1610, L1004 | "Template push only" for B3 and D3 contradicts the plan: steps 4B.6 (L1499) and 4D.7 (L1521) edit `image/catalogue/bmad/manifest.yaml`, and steps 2.5 (L1403) and 7.2 (L1610) say any edit under `image/catalogue/` changes `catalogue_sha256` (`main.tf:74`), retags the image and needs `coder update`; by the rubric (L1004) two delivery layers is L. Fix: say B3 and D3 as planned need a template push plus a catalogue-hash retag (the welcome-text sentence is mandatory in 4B.6 and 4D.7), or make the manifest edit optional in those steps; align L1083, L1234, L1311, L1615 and the Effort rating (L) with whichever is chosen; re-read `main.tf:74` before editing. |

Minor notes (not acted on): Dockerfile.coder:473-475 RUN also creates `/var/lib/aidev02` and `/etc/skel/.claude` (L1208, N-1); gate heading "Gate before any branch" does not fit (N-2, covered by B-1); leftover "This synthesis" wording at L684 and L689 (N-3); the fix log says the `/add-dir` v2.1.257 gate is absent but it appears at W01-4 (L791) (N-4); "`updated:` changed … no existing line changed" at L1383 reads as a contradiction (N-5); plus the other Minor rows of qa-consolidated-findings-phase6.md.

## Final (after fix cycle 2, review 3 of 3)

Cycle-2 verification reports read: qa/qa-fix-verification-phase6-cycle2.md (structural, PASS, Critical 0, Important 0, Minor 7; 5 of 5 rows fixed, 13 of 13 checks) and qa/qa-fix-verification-qualitative-phase6-cycle2.md (FAIL, Critical 0, Important 2, Minor 5; rows 1, 2, 4 resolved, rows 3 and 5 resolved only at the places the fix log named).

SEVERITY_DOWNGRADES (total across cycle-1 and cycle-2 consolidated files): 5 (cycle 1: AC#7, AC#8, CR#5, FR#1, FR#6; cycle 2: none). No extra downgrade lines.

Open blocking findings (qualitative agent; the executor read the report text qa-fix-verification-qualitative-phase6-cycle2.md lines 49-52):

- N-1 (IMPORTANT): the "B3 and D3 are modules.tf only" defect is left in three other places. (a) Section 6 Table 1 "Integration complexity" (report L1230) says B3 "1 file (`modules.tf`) + 1 pin" and D3 "1 file + 1 pin" while the Effort cells (L1227) say 6 files, 2 or 3 new tests and two delivery layers as planned (D2 "3 points + 1 test" against "8 files"; C "1 RUN group" against M). (b) Table 1 "Pinned tests that break" (L1236) omits `test-19:517-529`, `test-49:326` and `test-2-manifest-schema.sh` for B3 and D3, which the plan's own Table 5.1 (L1568, L1571, L1576) says the planned welcome-text edit (steps 4B.6, 4D.7) must keep green. (c) Section 2.4 (L367) still calls B2, B3, D2, D3 "the cheap variants". Fix: label the Integration-complexity cells "researched minimum" or add the as-planned count (B3 and D3: `modules.tf`, `manifest.yaml`, `README.md`, test pin, new test, driver row); add `test-19`, `test-49`, `test-2` BREAKS-IF to the B3, D3 (and D2, C) cells of L1236 or state that the Table 5.1 rows apply; replace "cheap variants" at L367 with "these variants".
- N-2 (IMPORTANT): Section 8 Phase 3 header (L1452) and Section 7 Stage 0 (c) (L1298) record "the fixed prohibitions of step 3.6" as `(constraint)` memlog bullets, but step 3.6 (L1461) also holds the rule that a stub "must not start with `bmad-`", which Limits row 1 (L1331) and Section 9 rows 2 and 3 call open and which rests only on doc-only W01-2; step 1.1 (L1383) also puts "assumption D-9, pending owner" inside the `(decision) Owner 2026-11-07` bullet although Section 9 row 8 (L1698) says D-9 awaits owner confirmation. Fix: split step 3.6: record the code-pinned prohibitions (seed-repo-path, `~/.claude` scope, test-3 reserved words, packaged and Orca names, `sc-` names) as `--type constraint` and the `bmad-` prefix rule as `--type assumption` ("plan default pending owner, Section 9 rows 2, 3"); make step 1.1 record D-9 as a separate `--type assumption` bullet instead of inside the decision bullet; say so in L1298 and L1452.

GATE3_FINAL: FAIL - HALT

## User exception applied (2026-11-07)

The user explicitly accepted this third exception to the 3-review limit, for Gate 3 only (it does not extend to Gates 4 and 5). The executor made the N-1 and N-2 edits itself in RESEARCH-REPORT-bmad-first-use.md (Table 1 "Integration complexity" and "Pinned tests that break" rows, Section 2.4 "cheap variants", Section 7 Stage 0 (c), Section 8 Phase 3 header and step 3.6, step 1.1 and the checklist line on constraint bullets), re-read the cited source (`test-19:515-529`, `test-49:324-326, 298, 310`) and Table 5.1 before editing, searched the report for leftover old phrasing afterward, and ran no fourth agent review.

GATE3_FINAL: PASS (user-accepted exception, 3 reviews plus manual edits; no fourth review)
