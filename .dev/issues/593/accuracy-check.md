## Accuracy check for #593

**Verdict:** current

Checked against `origin/master` at `3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda` after `git fetch origin`, and the pull requests merged since the issue was opened (1, list truncated: no).

The date-based scout search returned 12 pull requests, but 11 merged before the issue's creation at 2026-11-17T13:45:20Z. Only #592 merged afterward. All 12 scout entries and their returned changed-file lists were checked for relevance. The issue is open and has no comments; `gh issue view 593 --repo IronbellyOrg/IronClaude --comments` returned no comments, and the structured issue response confirmed `comments: []`.

| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
|---|---|---|---|
| 1 | "Disposable target for the #442 live observations (T1)." | still true | #442 asks for real-session observations of the launch-level guard using disposable work. This describes the intended purpose of #593, not a claim that any observation has already passed. |
| 2 | "create the file ob-442/T1.txt" | still true | At commit `3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda`, `git ls-tree -r origin/master -- ob-442` and `git ls-tree -d origin/master -- ob-442` both returned no entries: neither the target file nor the directory exists in the default-branch tree. A local Glob also found no matching target files. |
| 3 | "holding the single line ob-442 T1" | still true | The requested content remains unfulfilled because the target file is absent at the checked commit. No returned changed-file list includes `ob-442/T1.txt` or another path under `ob-442/`. |
| 4 | "Touch nothing else." | still true | This remains the issue's explicit scope restriction. No comments amend it; the requested change is only the one-line disposable file, not the launch guard, observation tests, or observer implementation. |
| 5 | "Close without merging anything." | still true | This remains an explicit completion instruction, not a report of an existing merge. The issue is still open and has no comments changing that instruction. #592 changes unrelated observer code and does not satisfy this request. |
| 6 | "The observation run's governed sessions (T1)" | still true | This is the stated audience for the disposable target. No comment changes it. Whether a particular governed session has run is Not known yet; the issue makes no claim that one has. |

### Merged pull requests that touch this issue

No reviewed pull request changes the target artifact. Two earlier pull requests concern the surrounding launch workflow; neither changes the requested file or its content. The table includes every scout entry so that exclusions are explicit.

| PR | Title | Relevant files | Effect on the issue |
|---|---|---|---|
| #592 | feat(observe): question text, dispatch link and Decision Desk behind QUESTION-LINK (#409) | None for this target; returned files are observer specifications, task artifacts, `src/superclaude/cli/observe/` modules and `tests/observe/` files. | Only post-creation merge; does not create or alter the disposable target. |
| #589 | docs(dev): record the owner-run questions-read observation under Q30 (#339) | Alignment decision records under `.dev/brainstorms/20261113-orchestrator-tui-alignment/`. | Pre-creation documentation; no target change. |
| #588 | docs(dev): fix three review findings on the alignment decision records (#339) | Alignment decision records under `.dev/brainstorms/20261113-orchestrator-tui-alignment/`. | Pre-creation documentation; no target change. |
| #587 | docs(dev): record the orchestrator, observer and issue-watcher alignment decisions (#339) | Alignment decision records under `.dev/brainstorms/20261113-orchestrator-tui-alignment/`. | Pre-creation documentation; no target change. |
| #586 | docs(observe): record the live questions test and the synthetic load test (#409) | Observer issue documentation under `.dev/issues/409/`. | Pre-creation documentation; no target change. |
| #585 | docs(orchestration): narrow the D2 amendment wording to a Ruling | Orchestration reference, core documentation and completed-task artifacts. | Pre-creation orchestration documentation; no target change. |
| #584 | feat(issue-pipeline): approval core for the issue-watcher claim handoff (Plan A) and the first live-test record | `docs/designs/sc-issue-launch-level-hook.md`, launch-level guard source/plugin mirror, issue-pipeline CLI and tests. | Contextually related to governed launches, but predates #593 and does not create the target or amend this issue's instructions. |
| #583 | fix(issue): remove the plain approved route from every worktree-level claim | Launch-level guard source/plugin mirror, `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, launch-prompt template and related tests/docs. | Contextually related to launch approval, but predates #593 and does not change the requested artifact. No guard or approval change is requested here. |
| #582 | feat(review): consequence-based review rule, fixcheck command and rf-qa rewrites (issue 552 stage 3) | Review primitives, CLI, tests and task artifacts. | Pre-creation review work; no target change. |
| #581 | feat(review): safety-scan command and print-only follow-up paragraph (issue 552 stage 0 and 1) | Returned files are evaluation artifacts under `.dev/eval-workspaces/shadow-model-combos/`. | Pre-creation review work; no target file in the returned list. |
| #579 | fix(sweep): restore the working class with the real Orca names | Sweep CLI/tests, orchestration design and task/review artifacts. | Pre-creation sweep work; no target change. |
| #577 | feat(observe): enable the live questions read, apply the 11 cuts, record the owner's direction decision (#409) | Returned files are observer issue and completed-task artifacts. | Pre-creation observer work; no target file in the returned list. |

The PR-list result did not reach the 200-PR limit. The returned file arrays for #581 and #577 contain 100 entries each and are not treated as proof of complete historical file enumeration. Both merges precede this issue; the fetched default-branch tree independently establishes that the target remains absent. No runtime observation or guard validation was performed, and none is needed to establish that this one-file request is still current.

<!-- sc:issue:accuracy-check -->
