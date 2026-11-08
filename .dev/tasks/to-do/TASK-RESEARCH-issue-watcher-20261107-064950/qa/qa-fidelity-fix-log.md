# Fidelity fix log (Gate 4, fix cycle 1)

**Agent:** rf-qa fidelity fix agent (`fix_authorization: true`)
**Date:** 2026-11-07
**Report edited:** `RESEARCH-REPORT-issue-watcher.md`
**Findings source:** `qa/qa-fidelity-consolidated-findings.md` (1 blocking, 11 minor)

## Verification before editing

- Ran `gh project item-list --help` (gh 2.103.3, 2026-10-26): `--query` flag text is `Filter items using the Projects filter syntax, e.g. "assignee:octocat -status:Done"`; EXAMPLES include `gh project item-list 1 --owner "@me" --query "label:bug -status:Done"`.
- Fetched `https://cli.github.com/manual/gh_project_item-list`: shows the same two illustrations (`assignee:octocat -status:Done`; `label:bug -status:Done`).
- Conclusion: the report's "documented for UI filtering only" wording is false against the cited page. Whether the API host accepts exactly `status:Backlog` and the item-list JSON schema stay [UNVERIFIED] (Q8).

## Blocking findings and resolutions

| # | Finding | Resolution | Status |
|---|---|---|---|
| 1 | Phase 4 five-filter table row 4 (report line 1612) said `status:Backlog` "is documented for UI filtering only"; the cited gh manual and local `--help` show status filters with `--query` | Edit 1, row 4 last cell: replaced the "UI filtering only" clause with "The gh manual page for `gh project item-list` shows status filters with `--query` in its examples (`assignee:octocat -status:Done`, `label:bug -status:Done`; [EXTERNAL-VERIFIED] and [CODE-VERIFIED by running `gh project item-list --help`, gh 2.103.3]); whether the API host accepts exactly `status:Backlog`, and the JSON schema, remain [UNVERIFIED]: Q8." The "claim leaves the item in Backlog" sentence is unchanged. Edit 2, Requirement Scoring table, R4 option-A cell (line 1265): added that the manual shows status filters with `--query` in its examples, and narrowed the unverified part to "acceptance of exactly `status:Backlog`". Verified by re-reading line 1612 and grepping the report for "UI filtering only" (0 matches). | FIXED |

## Checked and left unchanged

- Line 788 (external-findings row) says the filtering page "documents view filtering; it does not establish API use": true of that docs.github.com page, so no change. Line 781 already records the manual's `--query` text.
- Lines 1861 and 2048 (Q8, Q5) already call acceptance of the filter [UNVERIFIED]; consistent with the fix.
- No headings changed, so the Table of Contents was not regenerated. No `[CONTRADICTION` token written. Binding addenda (option A decided by the owner, B and C scored, Coder#477 boundary, integer-only rule) were not touched.
- Minor findings 2 to 12 remain notes; none were fixed.
