GATE1_DECISION: FAIL (cycle 1), second fix cycle required

Review count: 3 of 3 reviews are NOT yet used. Review 1 (three reports) and the cycle-1 verification (review 2) are done; the cycle-2 verification will be review 3. After cycle 2 any open blocking finding means HALT and escalate to the user.

SEVERITY_DOWNGRADES: 0

(The `## Severity changes` section of `qa/qa-consolidated-findings-phase3.md` says `none`.)

## Inputs read

| Report | Verdict | Counts |
|---|---|---|
| qa/analyst-completeness-report.md | FAIL | Critical 0, Important 2, Minor 8 |
| qa/qa-research-evidence-report.md | FAIL | Critical 0, Important 5, Minor 4 |
| qa/qa-research-qualitative-report.md | FAIL | Critical 0, Important 5, Minor 2 |
| qa/qa-consolidated-findings-phase3.md | BLOCKING_COUNT: 9 | 18 findings after de-duplication |
| qa/qa-fix-log-phase3-cycle1.md | 9 fixed, 0 not fixed | |
| qa/qa-verification-phase3-cycle1-structural.md (Transcribed by orchestrator from the agent's .json) | FAIL | Critical 0, Important 2 (N1, N2), Minor 3; all 9 original findings verified fixed |
| qa/qa-verification-phase3-cycle1-content.md | FAIL | Critical 0, Important 4 (F1-a, F1-b, F4-a, X-1), Minor 8; findings 3, 5, 6, 7, 8, 9 pass, finding 2 passes but introduced X-1 |

## Open blocking findings entering fix cycle 2

| ID | Target | Finding |
|---|---|---|
| F1-a | research/05-startup-boot-test-docs-and-decision-trail.md line 57 | Still says "C, E, F at boot"; the file's own addendum (C-F1-2) says B1, D1, E, F. |
| F1-b | research/05 reconciled matrix (addendum) | Built from the 04 addendum while it was In Progress; omits the test-73 pin for D2, the test-52:1374-1377 and test-51 `modules.tf` pins for B3 and D3, and the test-1-catalogue-shape pin for B1 and D1 that the finished 04 addendum lists. |
| F4-a | research/03-startup-flow-home-and-user-level-claude.md addendum (U8 closed verdict and Summary) | Says the 41 `python3` skill steps "are blocked there" and tags it [CODE-VERIFIED], while the same addendum lists as UNVERIFIED that Claude emits the bare form and that a fresh workspace has the hook registered. Split into verified (hook blocks a `python3` command word) and UNVERIFIED (emission and registration). |
| X-1 | research/02, research/04 (A.3(a), A.9, A.10), research/05 (row S13) | Conflicting guidance on adding a B2 skill to the `Dockerfile.coder:547-548` COPY: 02 treats it as a zero-layer fold; 04 and 05 say it breaks test-60, but test-60:84-88 only requires the same three sources and the same destination; 04 A.9 says keep it on its own COPY (costs one of the two free layers). Reconcile into one statement with the test-60 assertion text. |
| N1 | research/05 line 318 and matrix row S7 (line 341) | Says the image wrapper (option C) is invisible to test-57. False: `install.sh:42` runs `bmad install`, and test-57 runs it with the image PATH (test-57:27,75-79), so the baked wrapper is exercised. The same addendum's X2 row says so; row S7 gives C "none" for assertions X2 marks "breaks if". |
| N2 | research/03 line 286 | Calls `official-modules.js:770-797` the installer's existing-install check. That function only loads existing config; the real check is `installer.js:1549-1552` (always `P/_bmad`), which the 01 addendum cites correctly at `01:463`. The two addenda contradict each other. |

Minor items (notes only, not acted on): stale UNVERIFIED and CODE-CONTRADICTED counts in the 05 Summary; the 04 pointer says A.1-A.8 but the addendum runs A.1-A.11; 01 line 491 says the 03 addendum was In Progress but it is Complete; plus the Minor items already in the consolidated findings (10 to 18) and the verification reports' other Minor findings.

## Final (after fix cycle 2, review 3 of 3)

Cycle-2 verification reports read: qa/qa-verification-phase3-cycle2-structural.md (PASS, Critical 0, Important 0, Minor 3) and qa/qa-verification-phase3-cycle2-content.md (FAIL, Critical 0, Important 1, Minor 7).

SEVERITY_DOWNGRADES (total across cycle-1 and cycle-2 consolidated files): 0 (both `## Severity changes` sections say `none`; no extra downgrade lines).

Open blocking finding (New-1, IMPORTANT, content agent; executor re-read both lines in research/05-startup-boot-test-docs-and-decision-trail.md and confirmed it): line 376 still lists X2 as a "none" row with the old reasoning that test-57 never exercises a wrapper (grep finds no literal `bmad install`), although the X2 row (line 369) and line 318 now say option C BREAKS-IF because `install.sh:42` runs `bmad install` through the baked wrapper in every seeded test-57 run; line 408 (C-F1-2) still says option C has "no certain break (S1 none, S10 BREAKS-IF only)" although C is BREAKS-IF in S3, S7, S10, S11, S13 to S15, X2 and X3. The content agent's required fix: split the line-376 bullet ("X1, and X2 for every column except C ... for C see line 318 and the X2 row") and replace "S10 BREAKS-IF only" with "BREAKS-IF in S3, S7, S10, S11, S13 to S15, X2 and X3". Evidence to cite is already in the file (install.sh:42; test-57:27, 75-79, 173-178).

GATE1_FINAL: FAIL - HALT

## User exception applied (2026-11-07)

The user explicitly accepted ONE exception to the 3-review limit for Gate 1 (reply to ask msg_acc5015c9601). The executor edited only line 376 and line 408 of research/05-startup-boot-test-docs-and-decision-trail.md with the fix text above, re-read both lines and the cited source lines (test-57:27, 75-79, 173-178; catalogue/bmad/install.sh:42; rows S3, S7, S10, S14, S15, X2, X3 of file 05), and ran no fourth agent review.

GATE1_FINAL: PASS (user-accepted exception, 3 reviews plus two-line manual fix; no fourth review)

## User exception applied (2026-11-07)

The user explicitly accepted ONE exception to the 3-review limit for Gate 1 (reply to ask msg_acc5015c9601). The executor edited only line 376 and line 408 of research/05-startup-boot-test-docs-and-decision-trail.md with the fix text above, re-read both lines and the cited source lines (test-57:27, 75-79, 173-178; catalogue/bmad/install.sh:42; rows S3, S7, S10, S14, S15, X2, X3 of file 05), and ran no fourth agent review.

GATE1_FINAL: PASS (user-accepted exception, 3 reviews plus two-line manual fix; no fourth review)
