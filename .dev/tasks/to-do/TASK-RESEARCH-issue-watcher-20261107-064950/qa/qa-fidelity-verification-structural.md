# QA Report - Fidelity Fix Cycle Verification (structural)

**Topic:** GitHub issue watcher research report (issue 331)
**Date:** 2026-11-07
**Phase:** fix-cycle (fidelity verification, cycle 1 re-review)
**Fix cycle:** 1
**Fix authorization:** false (report only; the research report was not modified)
**Report under review:** `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md`
**Inputs:** `qa/qa-fidelity-consolidated-findings.md`, `qa/qa-fidelity-fix-log.md`
**Status:** Complete

---

## Checks (appended incrementally)

### Check 1: Blocking finding #1 (Phase 4 filter table row 4, report line 1612) is resolved

Source truth read by me, not taken from the fix log:
- `gh project item-list --help` (gh 2.103.3, 2026-10-26), run in Bash. `--query` flag text: `Filter items using the Projects filter syntax, e.g. "assignee:octocat -status:Done"`. EXAMPLES section: `gh project item-list 1 --owner "@me" --query "label:bug -status:Done"`. Description paragraph: "If supported by the API host, the --query option can be used to perform advanced search."
- Manual page `https://cli.github.com/manual/gh_project_item-list` (WebFetch): same sentence "If supported by the API host, the --query option can be used to perform advanced search."; three `--query` examples, one of them bug-labeled work excluding Done; no required scope and no JSON schema stated.

Report now (Read of line 1612, last cell): "The gh manual page for `gh project item-list` shows status filters with `--query` in its examples (`assignee:octocat -status:Done`, `label:bug -status:Done`; [EXTERNAL-VERIFIED] and [CODE-VERIFIED by running `gh project item-list --help`, gh 2.103.3]); whether the API host accepts exactly `status:Backlog`, and the JSON schema, remain [UNVERIFIED]: Q8. The claim leaves the item in Backlog (R01 §3), so the dispatch record, not the status, prevents repeats."
- This matches the source: status filters appear with `--query`, and acceptance of exactly `status:Backlog` plus the JSON schema are not established by the source. RESOLVED.
- Grep of the report for `UI filtering only`: 0 matches (count mode). The false phrase is gone.
- Line 1265 (R4, option A cell, Read): "`status:Backlog` is documented for UI filtering, and the `gh project item-list` manual shows status filters with `--query` in its examples (`assignee:octocat -status:Done`); acceptance of exactly `status:Backlog` by `gh project item-list --query` or the REST `q` parameter is [UNVERIFIED] ...". Consistent with line 1612 and with the source. "Documented for UI filtering" is true of the docs.github.com filtering page (line 788 says the page "documents view filtering; it does not establish API use"). PASS.
- Related lines left unchanged and still consistent: 781 (manual flags row), 788 (UI syntax row), 1749 (owner-run checklist item 3), 1861 (Q8), 2048 (Q5). All keep acceptance of `status:Backlog` as [UNVERIFIED] / owner-run check. No contradiction.

Result: finding #1 RESOLVED.

### Check 2: No new blocking distortion, phantom claim or broken structure introduced

- Table shape: row 4 of the five-filter table (line 1612) still has 6 cells (same as rows 1 to 5 at lines 1609-1613); the new text contains no `|` character. The R4 row (line 1265) still has 5 cells (R4 plus options A to D), same as R3 at line 1264. No broken table.
- Phantom claims: every new fact in the edits is checked against the source above (status filters with `--query`; the two literal query strings; gh 2.103.3 output). The `[CODE-VERIFIED by running gh project item-list --help, gh 2.103.3]` tag is true: I ran the same command and got gh 2.103.3. No new unverifiable claim. The [UNVERIFIED] scope (exact `status:Backlog` acceptance, JSON schema) was kept, not upgraded, so the fix did not overclaim.
- Conclusion unchanged: dispatch record (not Status) prevents repeats; fail-closed client-side status check at line 1612 is intact.
- Binding addenda untouched: Grep of the report for `CONTRADICTION` returns 0 hits (no stray contradiction token written).
- Diff scope: the report file is untracked, so no git diff is available; I checked each occurrence of `status:Backlog` (lines 788, 1265, 1612, 1620, 1749, 1861, 2048) and each is consistent with the others.

Result: no new blocking issue.

### Check 3: 10-section structure and Table of Contents intact

- Headings (Grep `^## |^# `): `## 1. Problem Statement` (102), 2 (153), 3 (575), 4 (675), 5 (752), 6 (990), 7 (1331), 8 (1441), 9 (1833), 10 (1909), plus `## Appendix A` (1996). Ten numbered sections present, in order.
- ToC (Read lines 10-98) lists sections 1 to 10 and Appendix A with subsections; the Phase 4 and Requirement Scoring entries it names still exist. The fix log states no headings were changed, and the headings I read match the ToC entries at section level.
- File is 2176 lines.

Result: structure and ToC intact.

## Notes (minor, not blocking, not rechecked)

- Line 781 puts the phrase "provided the API host supports it" inside quotation marks; the manual says "If supported by the API host, the --query option can be used...". The meaning is the same; the quotation is a paraphrase. Minor.
- Line 1612 says the two example strings appear "in its examples". In `gh project item-list --help`, `assignee:octocat -status:Done` is in the `--query` flag description and `label:bug -status:Done` is in the EXAMPLES section. Imprecise labelling only; the claim that status filters are shown with `--query` is true. Minor.
- Minor findings 2 to 12 from the consolidated findings remain open as notes, as agreed.

## Summary

- Previously blocking findings: 1. Resolved: 1. Still open: 0.
- New blocking findings introduced by the fix: 0.
- Checks passed: 3 / 3.
- Confidence: Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 7 | Grep: 4 | Glob: 0 | Bash: 2 (plus WebFetch: 1; no Tavily needed because the cited page is a single known URL fetched with WebFetch, tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 1, reason: Tavily tools are not in this session's tool list)
- Report file Read back after the final edit: yes (see completion step).

VERDICT: PASS

Status: Complete
