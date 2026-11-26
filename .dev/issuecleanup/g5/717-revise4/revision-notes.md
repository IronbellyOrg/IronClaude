# QA Source Fidelity - watcher recovery precondition

- **Topic:** Issue 717 live-record revision attempt.
- **Date:** 2026-11-24.
- **Phase:** precondition report, not a fourth independent review.
- **Fix cycle:** No new review cycle; coordinator-authorized recovery attempt.
- **Template:** /home/coder/.claude/templates/modularization-template-review/qa-source-fidelity_template.md.

## Sources Reviewed

| Source Doc | Assigned Section Range | Line Count |
|---|---|---|
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717-evidence.md | Entire inventory, chunks 1-80 and 81-102 | 102 |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/findings.md | Existing seven headings and acceptance items | 57 |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/analyze/analyze-report.md | Existing analysis and blocked live-evidence declaration | 30 |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717-review3/qa.md | Existing blocking finding and disposition | Initial Read exceeded the 80-line worker limit; not repeated |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717-revise3/revision-notes.md | Prior recovery result | 66 |
| /home/coder/.claude/WORKER-CONTRACT.md | Worker duties and blocked-gate policy | Initial Read exceeded the 80-line worker limit; not repeated |

The dispatch's first condition is exactly: `Before any gh call run 4962; if it is under 300, stop and report blocked with that number`. Its GitHub allow-list permits only issue/pr view/list. No current executable check or output field is identified by `4962`; no GitHub command was run in this attempt. The coordinator's earlier reported budget is not an independently observed remaining budget.

## Per-Source Fidelity

| Source | Semantic Coverage | Detail Preservation | Phantom-Coverage Check | Operational Completeness | Verdict |
|---|---|---|---|---|---|
| Coordinator evidence inventory | Read in full, but no live claims adopted | Merge dates and states remain inventory claims, not independent observations | No claimed new PR delivery or live acceptance | Required independent reads not started because their precondition is malformed | FAIL |
| Existing findings and analysis | Read, unchanged | Provisional classification and all existing uncertainty retained | No previous-worker read relabeled as this worker's read | Requested revision not performed | FAIL |

## Overall Verdict: FAIL

**worker_status: blocked.** The dispatch requires reporting blocked at a blocked gate. The success-shaped contract requested for completed work cannot truthfully be written because the independent live-record reads and required report updates have not been performed. This is a precondition report, not a fourth review and not a new acceptance verdict.

The existing result remains **still-relevant (provisional), complexity complex, size XL, priority P2**. These are retained classifications from the unchanged reports, not newly verified project triage. No per-item delivery claim has been promoted from UNVERIFIED.

| Acceptance item | Change in this attempt | Result |
|---|---|---|
| W1, first-enable baseline and hand-over | None | Delivery by inventory PRs not independently rechecked |
| W2, quiet-hour plan request | None | Delivery by inventory PRs not independently rechecked |
| W3, configurable polling interval | None | Delivery by inventory PRs not independently rechecked |
| W4, exponential throttle delay | None | Delivery by inventory PRs not independently rechecked |
| W5, live lock and workspace restart | None | Existing partial ingredients retained; live acceptance not rechecked |
| W6, full shadow-run acceptance | None | Live result remains UNVERIFIED |
| W7, restricted token | None | Actual scopes and migration trigger remain UNVERIFIED |
| W8, failure-streak alert | None | Delivery by inventory PRs not independently rechecked |
| W9, conditional reads | None | Delivery and budget trigger not rechecked |
| W10, launched-session permissions | None | Effective mode remains UNVERIFIED |
| W11, operation-id retry | None | Live deduplication and owner choice remain UNVERIFIED |
| W12, seven-day service review | None | Enable date and dated review remain UNVERIFIED |
| W13, finished-entry store bound | None | Delivery and size trigger not rechecked |
| W14, persistent local filesystem | None | Existing partial ingredients retained; persistence not verified |
| W15, post-live runbook | None | Existing partial text retained; live rewrite not verified |

Verdict, complexity, size, priority, dependencies and related-PR contents in the two existing reports are unchanged. The next action for this attempt is coordinator correction of the budget precondition within the read-only GitHub boundary, not an unauthorized rate-limit endpoint call.

## Issues Found

| # | Severity | Source | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT, blocking prerequisite | Dispatch condition (0) and its GitHub command allow-list | `run 4962` does not specify an executable live-budget check. Treating the number as a fresh result or substituting an unapproved endpoint would silently change the dispatch. | Coordinator supplies a usable precondition consistent with the allowed read-only commands; remaining work then needs permitted independent reads. |

The previous missing-live-record finding remains open. This attempt neither proves API exhaustion nor verifies the coordinator's claimed reset; it stopped before a GitHub call. Escalation `msg_b8db6650eea3` durably reported the malformed precondition.

## QA Complete

Attempt ended at the malformed precondition; the requested revision is not complete. Only this attempt's notes, handoff and worker contract were written. No GitHub calls, source edits, changes to either existing report, tests, installs, virtual-environment creation, staging, commits or outward writes were performed. No independent review was spawned because the worker contract prohibits worker-session fan-out, and the earlier review loop is exhausted.

Recovery of a local tool failure: the freshness hook rejected the first Edit of this newly created notes file because it required a tracked Read; the file was Read and the same Edit retried successfully. No bypass was used. The coordinator mailbox returned no answers or directives at the checkpoints already completed; therefore no acknowledgment line was due. The mandatory final mailbox check still occurs before worker_done.

VERDICT: FAIL
