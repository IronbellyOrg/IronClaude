# QA Report - Fidelity Fix Content Verification (report-qualitative, fix-cycle)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** report-qualitative (fix-cycle verification of content quality)
**Fix cycle:** 1
**Fix authorization:** false (report only)
**Status:** Complete

Inputs:
- Report: .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md
- Fix log: .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/qa/qa-fidelity-fix-log.md
- Consolidated findings: .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/qa/qa-fidelity-consolidated-findings.md

---

## Checks (appended incrementally)

### Check 1 - The previously blocking finding is fixed at line 1612 (Phase 4 filter table, row 4)

Result: PASS.
- Read report lines 1604-1614. The "documented for UI filtering only" clause is gone (Grep for `UI filtering` returned only line 1265, which is the corrected R4 cell, and the phrase "UI filtering only" appears nowhere).
- New wording says the gh manual for `gh project item-list` shows status filters with `--query` in its examples (`assignee:octocat -status:Done`, `label:bug -status:Done`), tagged [EXTERNAL-VERIFIED] and [CODE-VERIFIED by running `gh project item-list --help`, gh 2.103.3]; acceptance of exactly `status:Backlog` and the JSON schema stay [UNVERIFIED]: Q8.
- I re-ran `gh project item-list --help` (gh version 2.103.3, 2026-10-26): line 19 prints `--query ... e.g. "assignee:octocat -status:Done"`, line 36 prints `--query "label:bug -status:Done"`, and the header says "If supported by the API host". The report text matches.
- I fetched https://cli.github.com/manual/gh_project_item-list (WebFetch; the Tavily tools are not in this runtime tool list, so the fallback was used for this single lookup): the page gives the same `--query` description with `"assignee:octocat -status:Done"`. The [EXTERNAL-VERIFIED] tag holds.
- Proportionality: the examples only show a negated status filter (`-status:Done`), and the cell does not claim a positive `status:Backlog` is accepted; it keeps that as [UNVERIFIED]. The claim is no stronger than the evidence.

### Check 2 - The corrected R4 option-A cell at line 1265 (Requirement Scoring)

Result: PASS.
- Read lines 1256-1272. Cell now reads: `status:Backlog` is documented for UI filtering (matches line 788, which cites the docs.github.com filtering page and says it "does not establish API use"), and the gh manual shows status filters with `--query` in its examples; acceptance of exactly `status:Backlog` by `gh project item-list --query` or the REST `q` is [UNVERIFIED] (W01 §8, §13, gap 3).
- Consistent with the Requirement Scoring convention: the cell still carries an [UNVERIFIED] fact, so A stays Partly on R4. The rating did not need to change, and the Tally (A 2 Meets, B 1, C 0, D 2) and "Reading the scores" (R3/R4 closable by one owner-run live call, line 1287) are unchanged and still correct.
- B, C and D R4 cells say "same unverified filter" or equivalent; none repeats the old false claim.

### Check 3 - Consistency with Q8 and the rest of the report (requirement (a))

Result: PASS.
- Q8 (line 1861) asks whether `gh project item-list --query "status:Backlog ..."` or REST `q` accepts the UI filter syntax, and says the plan fails closed on unreadable status or repository. Same position as the fixed row.
- Q5 in the closing table (line 2048), 7.9 item 11 (line 1433), 7.6 checklist item 3 (line 1749), section 5.3 rows (lines 781, 787, 788) and the Phase 4 discovery row (line 1620: `[PROPOSAL; the key names are assumed and open: Q8]`) all keep the server-side filter acceptance as [UNVERIFIED] or open. No section now asserts or denies the filter outright.
- Line 1620's query `is:issue is:open status:Backlog label:<trigger> assignee:@me` says `is:issue is:open` is the form of the help example; confirmed by the local `--help` example `assignee:@me is:issue is:open` (help line 33).
- Section 2 (line 186), Section 6 (lines 1036-1037) and the 7.4 row (line 1747) say the claim leaves the issue in Backlog; row 4 of the table says the same and that the dispatch record, not the status, prevents repeats. No contradiction.

### Check 4 - The recommendation and plan still follow from the corrected facts (requirement (b))

Result: PASS.
- The fix changed the wording of evidence, not a fact the decision rests on: server-side `status:Backlog` acceptance was [UNVERIFIED] before and after. The plan already fails closed on an unreadable status/repository (row 4, Q8, Phase 4 step 4.2/line 1620) and schedules the owner-run call (7.6 item 3, line 1749; Tally "Reading the scores" line 1287).
- Rating impact: R4 stays Partly for A, B, C and D under the convention (an [UNVERIFIED] fact in the cell). No Meets/Partly/Does-not-meet cell and no Tally row should change; I recounted the Tally from lines 1260-1271: A Meets R1, R8 (2); B Meets R1 (1); C 0; D Meets R1, R8 (2). Matches lines 1277-1280.
- Section 7.1 (line 1335) and 7.2 (lines 1343-1350) do not depend on the "UI filtering only" claim; Options Comparison (lines 1294-1307) has no R4/filter cell. Implementation steps 3.x/4.x/6.x (lines 1591-1596, 1637-1641, 1731-1734) and acceptance criterion 4 (line 1734, 1822) are unchanged and still follow.
- No leftover `[CONTRADICTION` token (Grep count 0). Report headings unchanged, so the table of contents does not need regenerating.

### Check 5 - Owner-decision wording intact (requirement (c))

Result: PASS.
- Recommendation is option A labelled as decided by the owner: line 1335 "**Option A, the workspace-side poller, decided by the owner (ADDENDUM 2).**"; D1 row (line 135) "The Recommendation is option A, decided by the owner"; column headers "A: workspace poller (decided)" at lines 1260 and 1294.
- B and C stay scored (Requirement Scoring lines 1260-1271; Tally lines 1275-1280; Options Comparison lines 1294-1307) and carry revisit conditions: nine-row table at lines 1313-1323, closing line 1325, 7.8 (line 1417), follow-up table (lines 1787-1788).
- Coder#477 is stated with its repo boundary (lines 148, 528, 660, 1413, 1787-1789, 1845: "listener, registration and transport live in the Coder repo, not in IronClaude") and with the statement that option A makes it unnecessary unless B or C is revisited (lines 149, 660, 1325, 1413, 1789, 1845).
- Integer-only rule is stated: lines 291-295 (prompt contract), 1335 (7.1), 1361 (security model D3), 1592 (step 3.2, with the stricter `type(number) is int` plus regex form), 1596 (tests), 1734 item 2, 1821.
- None of these passages was touched by the two edits (fix log "Checked and left unchanged" agrees).

### Check 6 - Adversarial sweep for what the fix cycle missed (stance: assume at least 10 errors)

Result: no blocking defect found; four minor notes. Minor notes are not rechecked and do not fail the review.
- Note M1 (line 975, section 5.16 "Reading Projects v2"): the summary says "`gh project item-list --query` can filter by Status, label and assignee". The same row ends with "server-side filter acceptance is [UNVERIFIED] until one owner-run live call", and the manual's examples do show `assignee:`, `label:` and `-status:Done`, so the sentence is supported for the three field names, but it is slightly stronger than the Phase 4 row 4 wording about positive `status:Backlog`. Wording only.
- Note M2 (lines 294 and 1361): earlier sections still show `"/sc:issue --claim " + str(int(number))`, while step 3.2 (line 1592) says the implementation is stricter and explains why. Already recorded as consolidated finding 12; not a contradiction because 1592 states the difference.
- Note M3 (line 1413): "the only follow-up A needs in the Coder repo is the `coder_script` cron entry ... and a persisted path" is stronger than 7.9 items 7 and 9 and Q5/Q6 (Orca runtime reachable, `ccsession-orca` configured, `$HOME` persistence are per-host unknowns). Already recorded as consolidated finding 11.
- Note M4 (line 1612): the tag `[CODE-VERIFIED by running gh project item-list --help]` is accurate (confirmed above), but the evidence is a help/example line, not a call against the API host; the cell says so by keeping acceptance [UNVERIFIED]. No change needed.
- Checked and found sound: the two edited cells quote the examples exactly; gh version string 2.103.3 matches my run; `is:issue is:open` example matches `--help`; the "fails closed" client-side rule is stated in both row 4 and Q8.

## Report-qualitative checklist (12 items), applied to the changed content

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings | PASS | Lines 115-141 unchanged; fix does not touch the three questions |
| 2 | Current state is current | PASS | Line 186 and 570 still match the claim code finding; `gh` help re-run today |
| 3 | Options genuinely distinct | PASS | Lines 1260-1307 unchanged |
| 4 | Recommendation follows from analysis | PASS | Check 4; A decided by owner, scores reported honestly including where A is not ahead (line 1258, 1350) |
| 5 | Plan actionable | PASS | Check 4; live-call step 7.6 item 3 closes Q8 |
| 6 | Gaps honest | PASS | Q8 [UNVERIFIED]; fix removed a false negative claim and kept the unknown as unknown |
| 7 | External research relevant | PASS | gh manual page re-fetched; supports the corrected cell |
| 8 | Scale claims substantiated | PASS | Not touched by the fix; line 800 marks figures [DERIVED] |
| 9 | Risk assessment complete | PASS | Not touched; Q7/Q8 risk columns intact |
| 10 | Evidence trail complete | PASS | Row 4 cites manual, `--help`, Q8; fix log records the verification commands |
| 11 | No circular reasoning | PASS | Corrected claim rests on the external page and a local command, not on the report's own synthesis |
| 12 | Conclusion proportionate | PASS | "Partly" for R4 with explicit [UNVERIFIED]; no strengthened claim |

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` section was in my spawn prompt, so I ran standalone. I relied on the fix log only for the list of edits made (two cells), not for their correctness.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Corrected sentence versus source: ran `gh project item-list --help` (Bash) and WebFetch of https://cli.github.com/manual/gh_project_item-list; both show the `--query` examples quoted in the cells.
- Cross-section consistency of the filter claim: Grep for `Backlog|UI filtering|--query|item-list` over the report, then Read of lines 781-788, 968-977, 1256-1288, 1415-1438, 1585-1642, 1728-1750, 1855-1866, 2040-2051.
- Owner-decision wording: Grep for `Coder#477|decided by the owner|integer-only`, then Read of lines 143-150, 286-296, 1339-1366, 1409-1413, 1780-1794.
- Tally recount from the Requirement Scoring rows 1260-1271 against lines 1277-1280.

**Confidence:** Verified: 15/15 (12 checklist items plus the three requested checks a, b, c) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 18 | Grep: 5 | Glob: 0 | Bash: 1 (plus WebFetch: 1; Tavily unavailable in this runtime tool list, WebFetch used as the documented fallback for the one external lookup)

**Honesty note on the adversarial stance:** I did not find 10 errors. I found no blocking error after reading every changed line, every place the filter claim is repeated, and the owner-decision passages. The four items in Check 6 are minor wording notes, two of them already in the consolidated findings. I limited the sweep to the changed statements and their consistency with the rest of the report; I did not re-audit unrelated sections already covered by the two fidelity reports.

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Blocking issues: 0
- Minor notes: 4 (M1 to M4)
- Issues fixed in-place: 0 (report only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | report line 975 | "can filter by Status" is slightly stronger than the Phase 4 wording for positive `status:Backlog` (hedged in the same row) | Optional: say "shows status filters in examples" |
| 2 | MINOR | report lines 294, 1361 | Earlier sections show `str(int(number))`; step 3.2 is stricter and says so | None required (known finding 12) |
| 3 | MINOR | report line 1413 | "the only follow-up A needs in the Coder repo" stronger than the research | None required (known finding 11) |
| 4 | MINOR | report line 1612 | CODE-VERIFIED tag rests on help text, not an API call | None; cell already keeps acceptance [UNVERIFIED] |

## Recommendations

- Proceed. The one blocking fidelity finding is resolved and no new blocking finding was introduced.
- The owner-run live call (checklist item 3, step 7.6) remains the way to close Q8.

VERDICT: PASS

**Status:** Complete

## QA Complete

