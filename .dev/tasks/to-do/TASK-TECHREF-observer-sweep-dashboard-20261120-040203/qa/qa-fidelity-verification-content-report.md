# QA Report - Gate 4 Fidelity Verification (content), cycle 1

**Status:** Complete
**Phase:** fix-cycle (tech-ref-qualitative, content)
**Date:** 2026-11-20
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
**Inputs:** qa-fidelity-consolidated-findings.md, qa-fidelity-fix-log-c1.md (same directory)
**Fix authorization:** false (document not modified)

## Per-finding results

Doc = the final document (1,399 lines by `wc -l`, within the 1,400 limit). SNAP = /home/coder/.cache/ic-snap-20261120/master. OM = `git -C /home/coder/workspaces/IronClaude show origin/master:<path>`.

| ID | Status | Evidence read in the current document and in the source |
|---|---|---|
| GF4-1 observer merge: "never deleted" | RESOLVED | Doc:446 now says identified rows are never deleted for absence, an identity-unknown row missing from a complete cycle is dropped, kept only across a PARTIAL cycle (parse.py:726-727). SNAP `observe/parse.py:723-727`: `if row.identity_unknown and not coverage.partial: continue` precedes `merged.append(replace(row, reobserved=False))`. Same narrowing at Doc:1246 (limitations row). The remaining "only grows" hit at Doc:1354 is the forbidden-prefix convention, unrelated. |
| GF4-2 snapshot "Dropped" bullet | RESOLVED | Doc:455 lists six dropped counters (`pages_read`, `empty_page`, `has_more_at_stop`, `stopped_by_*`, `identity_unknown_rows`, `malformed_rows`) and the four exported `collection` keys `state`, `collected`, `changedDuringRead`, `duplicatesIgnored` (export.py:209-215). SNAP `export.py:207-215` has exactly those four keys; SNAP `parse.py:180-193` `Coverage` fields match the six dropped names; SNAP `view.py:220-223, 687-692` maps the four exported ones. It no longer says "coverage counters" are dropped wholesale. |
| GF4-3 sweep JSON v1 shapes | RESOLVED | Doc:692 lists the 12 top-level keys and the shapes of `collected`, `scope`, `sources[]`, `rows[]` (with `safe_to_close`), `worktrees[]` (with `packages[]`), `waiting`. Compared field by field with SNAP `sweep/report.py:613-695` (`to_json`): all keys, nesting and the "report_path is the one unsanitized string" remark match; `scope.worktrees` is a count in code and in the Doc. |
| GF4-4 worker-list truncation | RESOLVED | Doc:686 and Doc:1229. SNAP `sweep/probes.py:89` `WORKER_LIST_PAGE = 100`; `probes.py:1150-1161` one `worker-list` call per Run, no paging, `raw_count >= WORKER_LIST_PAGE or hasMore` sets `truncated`; `report.py:32, 209-210` banner text identical to the Doc quote; `report.py:526-531` bullet; `classify.py:72, 701-702` note text identical; `classify.py:764-777` `_person_origin` returns `None` (unknown) when `g.origin` is non-empty, so the Doc wording "keeps a transcript-only row's person_started unknown instead of True" is accurate (it does not copy the finding's looser word "blocked"). |
| GF4-5 report-name error text | RESOLVED | Doc:1071 now gives `cannot link report: <exc>` (commands.py:191-194) and `report name space exhausted: <dir>` (commands.py:197-201; test_cli_contract.py:1414). SNAP `sweep/commands.py:180-207` and `tests/sweep/test_cli_contract.py:1414` carry both strings exactly; both raise `_PublishError`. |
| GF4-6 D-1 / C8-9 relabel | RESOLVED (see the C8 judgement below) | Present and consistent in every place: Doc:246, 346, 375, 549, 556, 1232, 1329, 1345, 1397. No place still labels D-1 a DEFECT-CANDIDATE; C8-8 keeps its label and full wording (Doc:1235, 1328). Doc:1345 states "2 DEFECT-CANDIDATE as registered" and that Gate 4 relabelled D-1, so one stands. |
| GF4-7 PR #673 and #606 | RESOLVED | Doc:553 and Doc:873 read "refs #606 ... #606 was closed separately on 2026-11-20T00:20:54Z". `gh pr view 673 --repo IronbellyOrg/IronClaude`: body "refs #606", `closingIssuesReferences` empty, merged 2026-11-19T19:16:52Z. `gh issue view 606`: closedAt 2026-11-20T00:20:54Z, `closedByPullRequestsReferences` empty. |
| GF4-8 S1-S11 / R1-R11 rule texts | RESOLVED | Doc:875-879 give one-line texts with file:line. Spot-checked against the package (README.md:33-41, DESIGN-CONTRACT.md:11, PLAN.md:38/57/66-67, integration-gaps.md:24, data-dictionary.md:17-50, fixtures.py:47) and research (`merged-requirements.md` :74-77, 84-93, 98-107, 1104-1119; `merged-visual-design.md` :16-24): every rule text is supported. The research files are marked LOCAL-ONLY, untracked. Two citation slips are minor notes (below). |

## Extra check: is the D-1 / C8-9 relabel (DEFECT-CANDIDATE to KNOWN LIMIT (cited)) honest under the C8 rule?

**Judgement: yes, honest. No blocking finding.**

Facts re-verified (not taken from the fix log):
- OM `.dev/issues/409/ponytail-review-20261116/cuts-debate/final-cut-list.md:24` is row R1, CUT-SMALLER, EXECUTE-NOW, confidence 80; it removes the collector `question_fixture` argument, state and replay and keeps `read_questions` as a 2-line stub returning FAILED `no-question-fixture`; its surviving guard is "`--fixture` with `--questions` refused: commands.py:177-178". `:62` is row D13 (mark T7 "not built / no automated test", "strike nothing"). R1 is one of the 11 EXECUTE-NOW rows.
- OM `execute-now-brief.md` Step 1 repeats R1; OM `runtime-code.md:51` says "production can never reach it ... Move to a test double"; OM `acceptance-tests.md:25` carries the T7 "not built / no automated test" wording.
- `gh pr view 577 --repo IronbellyOrg/IronClaude`: merged 2026-11-17T00:40:16Z, body "applies the 11 debated cuts"; the issue 409 comment of 2026-11-17 says "applied the 11 agreed cuts".
- Code: SNAP `observe/collector.py:125-129` is the stub; SNAP `observe/commands.py:77-79, 183-188, 414` refuse `--questions` with `--fixture` (exit 2).

Why it holds under R-C8 (Doc:1310-1315): step 1 asks for a cited design-level text that states, for the specific capability, that the shipped build does not deliver it. R1 (decision, applied in a merged PR) plus the code stub is that text for fixture replay of the question ledger. Step 2 says a bare "not built" line does not qualify, and the row says so itself about `acceptance-tests.md:25` ("a text that alone would only record an absence"). The row does not claim an owner ruling: it says "a review-panel debate output, not a dated owner ruling", names no "until" condition or owner, states the reversal ("if the owner holds that a debated cut is not a scope decision the label becomes DEFECT-CANDIDATE with no fact changed"), cites G-36 (five owner records searched, nothing on fixtures), keeps the owner question, and prints the exact words "remediation task not created (read-only brief); flagged for the owner" (Doc:556, 1232, 1329). This is the same treatment the document gives C8-1 ("review inputs, not a dated owner ruling") and C8-6 (reversal clause), so the relabel is consistent with the other rows. C8-8 (Needs-you session entry) stays DEFECT-CANDIDATE with full wording. The relabel is disclosed in three places (the C8-9 label cell, Doc:1345, the Document History row), so a reader cannot miss that it differs from the register.

**Neutrality (no unification recommendation): confirmed.** Doc:53, 56, 159 and 1381 state "no recommendation / no unification recommended"; Doc:1192 is headed "Unification touch points (facts only; no recommendation)". Grep for `recommend|prefer|consolidat|should|ought|would be better|best option|advis` found only: negations, the field name `recommend` (Doc:805), the sweep "recommends nothing" statements (Doc:576, 1157, 1363), a design-package "prefer Bubble Tea" fact (Doc:1289), and a file-name use of "consolidated" (Doc:1389). The owner question in C8-9 ("is fixture replay ... still wanted, or is the fake-runner test route the accepted substitute?") is a fact question, not a recommendation.

**Designed-versus-built check.** No fix turned a designed-only item into a built one. GF4-6 moves a built-but-limited path to a labelled limit, not the reverse; GF4-8 adds rule texts to a status table whose rows still carry their designed/built status; the other six fixes correct statements about code that is built.

## New blocking defects introduced by the fixes

None found. Re-read every changed passage against the source (table above). Length 1,399 lines (limit 1,400). The protected parts (2.5 matrix, 8.1 verb inventory, 14.4 contradictions list, the five 13.1 scenarios, every DEFECT-CANDIDATE row with full wording) were not cut: the fix log records net +7 lines and no deletions, and C8-8 is intact.

## Minor notes (not rechecked, no fix cycle triggered)

1. Doc:877 cites `README.md:32` for S6 and S10; line 32 of the package README is blank and the text (overview stays global; Space holds/resumes; fixture changes queue) is at `README.md:33`. The claims are true; the line is off by one.
2. Doc:159 says "Gap-fill file GF-1 is the authority for every C8 label"; C8-9 now differs from GF-1 by the Gate 4 relabel (disclosed in the C8-9 row, Doc:1345 and the history row). A clause "except C8-9, relabelled at Gate 4" would remove the apparent conflict.
3. Doc:556 and Doc:1329 say the cut is a decision "for this specific capability"; R1's own stated reason is removing production-unreachable replay code, and D13 says "strike nothing", so SPEC CAP-1 and the R0 gate wording still name the capability. The row prints the DESIGN-package lines and the residual, so a reader can see this; adding "D13: strike nothing" to the row would make it complete.
4. Doc:455 lists six dropped coverage counters but not `Coverage.page_totals` (parse.py:178), which is also not exported as such (it feeds `page.total` through `reported_total`). Not a counter in the sense used; low impact.

## Self-Audit

**(a) Reliance list:** relied on the fix log and the consolidated findings only for the list of locations to inspect; every verdict above comes from a fresh read of the document and the source.

**(b) Independent semantic checks:** re-read SNAP `parse.py:712-745`, `export.py:198-218`, `sweep/commands.py:178-207`, `sweep/probes.py:85-92, 1140-1165`, `sweep/report.py:28-36, 205-213, 524-535, 605-700`, `sweep/classify.py:68-76, 686-706, 758-780`, `observe/collector.py:118-132`, `observe/commands.py:75-79, 181-189, 412-415`, `tests/sweep/test_cli_contract.py:1410-1418`; read OM cut list, execute-now brief, runtime-code and acceptance-tests; ran read-only `gh pr view 577/673` and `gh issue view 606/409` with `--repo IronbellyOrg/IronClaude`; read package README, DESIGN-CONTRACT, PLAN, integration-gaps, data-dictionary and research `merged-requirements.md` / `merged-visual-design.md` lines cited by the rule texts; grepped the document for the labels, counts, advice words and unification language.

## Result

- Blocking findings checked: 8 (GF4-1 to GF4-8): 8 RESOLVED, 0 STILL OPEN.
- New blocking findings: 0.
- **Open blocking count: 0.**
- Confidence: Verified: 8/8 findings plus 3 extra checks (C8, neutrality, designed-vs-built) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%.
- Tool engagement: Read: 8 | Grep: 8 | Glob: 1 | Bash: 14 (read-only: sed, grep, git show, gh view). Tavily/web: not used.

## Verdict: PASS (4 minor notes)

**Status:** Complete
