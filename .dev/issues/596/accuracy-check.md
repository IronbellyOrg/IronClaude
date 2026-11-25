## Accuracy check for #596

**Verdict:** current

Checked against `origin/master` at 3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda, and the pull requests merged since the issue was opened (1, list truncated: no). The scout's date-based search returned 12 PRs; only #592 merged after the exact creation time, 2026-11-17T13:45:23Z. All 12 listed PRs were checked for file-level relevance. No issue comments were present at verification.

| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
|---|---|---|---|
| 1 | "Disposable target for the #442 live observations (T4)." | still true | #442 is open and describes live launch-level observations on disposable targets. #596 remains an open, explicitly disposable T4 target; no comment changes that scope. This verifies its stated purpose, not whether a live observation has passed. |
| 2 | "create the file ob-442/T4.txt holding the single line ob-442 T4" | still true | The `ob-442` tree is absent from origin/master at commit 3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda; a checkout glob also found no files under that directory. None of the checked PRs changes that target. The requested addition remains outstanding. |
| 3 | "Touch nothing else. Close without merging anything." | still true | These are explicit scope and completion requirements in #596, not claims of existing behavior. There are no comments superseding them. No implementation, merge, or closure was performed by this check. |
| 4 | "The observation run's governed sessions (T4)" | still true | #596 identifies its intended audience; #442 supplies the launch-level observation context. The one-line fixture is not a request to alter the guard or its tests. Whether T4 has run successfully is Not known yet. |

### Merged pull requests that touch this issue

No listed PR changes the requested target. The table records the relevance check, including the eleven same-day PRs that predate this issue.

| PR | Title | Relevant files | Effect on the issue |
|---|---|---|---|
| #592 | feat(observe): question text, dispatch link and Decision Desk behind QUESTION-LINK (#409) | 47 files: observer collector, commands, export, parse, render and view; observer tests; #409 specifications and task artifacts | Only post-creation merge. Observer changes do not create `ob-442/T4.txt` or replace the disposable target request. |
| #589 | docs(dev): record the owner-run questions-read observation under Q30 (#339) | 1 alignment decision-record file | Predates creation; no target or implementation overlap. |
| #588 | docs(dev): fix three review findings on the alignment decision records (#339) | 2 alignment decision-record files | Predates creation; no target overlap. |
| #587 | docs(dev): record the orchestrator, observer and issue-watcher alignment decisions (#339) | 58 alignment decision-record files | Predates creation; no target overlap. |
| #586 | docs(observe): record the live questions test and the synthetic load test (#409) | 1 #409 specification file | Predates creation; observer test documentation does not fulfill T4. |
| #585 | docs(orchestration): narrow the D2 amendment wording to a Ruling | 14 worker-contract, architecture and task files | Predates creation; no target overlap or change to the requested contents. |
| #584 | feat(issue-pipeline): approval core for the issue-watcher claim handoff (Plan A) and the first live-test record | 32 approval-core, launch-level guard, worker-contract, design and test files | Related launch-governance background, already merged before creation; does not fulfill or supersede the target. This check does not certify launch safety. |
| #583 | fix(issue): remove the plain approved route from every worktree-level claim | 11 launch-level guard, claim-protocol, launch-prompt, observation-fixture, design and test files | Related governed-session background, already merged before creation; no `ob-442` target change. |
| #582 | feat(review): consequence-based review rule, fixcheck command and rf-qa rewrites (issue 552 stage 3) | 77 review rules, agents, CLI, tests and task files | Predates creation; no target overlap. |
| #581 | feat(review): safety-scan command and print-only follow-up paragraph (issue 552 stage 0 and 1) | 2740 review CLI, implement/reflect protocol, test, evaluation and task files | Predates creation; complete merge file list checked locally at fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d because GitHub's diff endpoint rejected the large diff. No `ob-442` target changes. |
| #579 | fix(sweep): restore the working class with the real Orca names | 31 sweep implementation, tests, design and task files | Predates creation; no target overlap. |
| #577 | feat(observe): enable the live questions read, apply the 11 cuts, record the owner's direction decision (#409) | 188 observer implementation, tests, #409 records and task files | Predates creation; complete file-name diff checked. Observer changes do not fulfill T4. |

The PR list itself was not truncated. GitHub's PR JSON file lists for #581 and #577 contained only 100 entries each; their complete file lists were checked separately as noted above. No application tests or live governed observations were run; this was a read-only accuracy check, not execution of the disposable task.

<!-- sc:issue:accuracy-check -->
