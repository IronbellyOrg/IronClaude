# Task 3 spec-compliance review

T3.AC1 met — docs/designs/issue-watcher-setup.md:587 introduces the required subsection; its 19 data rows at docs/designs/issue-watcher-setup.md:593–611 match the 19 fixture filenames. The per-file single-occurrence checks are recorded at .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t3-sheet-check.log:1–39.

T3.AC2 met — Each row's builder is recorded at .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t3-sheet-check.log:1–38. Independently compared the documented commands against github.argv_user and github.argv_discover at src/superclaude/cli/issue_watch/github.py:175–198, the REST page builders at src/superclaude/cli/issue_watch/github.py:201–225, the GraphQL builders at src/superclaude/cli/issue_watch/github.py:228–249, github.argv_reread at src/superclaude/cli/issue_watch/github.py:252–262, and the claim prompt and launch builder at src/superclaude/cli/issue_watch/launch.py:84–116. Query/projection substitution and pagination are explicitly explained at docs/designs/issue-watcher-setup.md:589; the Project id is not invented as an argv argument.

T3.AC3 met — docs/designs/issue-watcher-setup.md:593–611 uses angle-bracket placeholders for variable logins, issue numbers, node ids and launch paths, without a real token. The fixed repository and numeric command constants are builder literals, not captured personal values or real issue numbers.

T3.AC4 met — docs/designs/issue-watcher-setup.md:613 requires exact channel output and fixture-based filenames; docs/designs/issue-watcher-setup.md:614 requires same-type redaction of logins, numeric ids, node ids, titles, bodies and tokens; docs/designs/issue-watcher-setup.md:615 requires recording every uncaptured fixture as still assumed.

T3.AC5 met — The independently inspected git diff against the start snapshot contains only the new subsection insertion. The four bullets remain at docs/designs/issue-watcher-setup.md:582–585 and the original paragraph remains at docs/designs/issue-watcher-setup.md:617. The saved section diff at .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t3-sheet-check.log:41–82 likewise contains no removal or replacement of either.

Findings: none.

Self-audit: Checked all 19 fixture source/note descriptions, missing/duplicate rows, builder argument order and quoting, projected versus raw replies, output channels, placeholder leakage, and preservation of the deployment gate. Challenged whether exceptional errors were advertised as reproducible: rate-limit, HTTP 502 and lost/missing-id Orca replies are explicitly capture-if-seen, and the sheet prohibits repeating launches or manufacturing replies. Read the offline checker rather than trusting its PASS labels; independently inspected the current document and start-snapshot diff. No external services were contacted, no runtime reply shapes were claimed verified, and no product files were changed by this review.
