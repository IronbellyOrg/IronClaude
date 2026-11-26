# QA Source Fidelity - watcher live-record revision

- **Topic:** Issue 717 live-record recovery and per-item delivery reconciliation.
- **Date:** 2026-11-24.
- **Phase:** Revision evidence, not a fourth independent review.
- **Fix cycle:** Coordinator-authorized recovery after the exhausted review loop.
- **Template:** /home/coder/.claude/templates/modularization-template-review/qa-source-fidelity_template.md.

## Sources Reviewed

| Source Doc | Assigned Section Range | Line Count |
|---|---|---|
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717-evidence.md | Entire inventory, Read chunks 1-80 and 81-102 | 102 |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/findings.md | Seven existing headings, W1-W15, classifications and next steps | 57 before revision |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717/analyze/analyze-report.md | Existing static analysis and live-evidence blocker | 30 before revision |
| /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717-review3/qa.md | Open blocking finding B1 and review disposition | Initial Read exceeded 80 lines; not repeated |
| GitHub live PR records | Independently read #707, #447, #448, #485, #548, #591, #700, #701, #686, #697, #682, #681, #684 and newer #759, #729, #732, #735, #736, #752, #754 | JSON bodies, merge metadata, comments/review summaries where requested; not line-numbered |
| GitHub live issue records | #717 body/comments; #450/#331 body/closure comments; #655 decision/closure comments; #716/#718/#720 comments; #442 body/comments; identity/state of #698/#699/#409/#706/#444/#665 | 14 independently viewed issues; JSON, not line-numbered |
| Discussion-discovered live PR records | #584, approval handoff evidence; #690, unmerged plan mode | 2 additional independent PR views, bringing total PR views to 22 |
| Current checked-in decision records | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/releases/backlog/issue-watcher-zero-setup/design-comparison-655.md; /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md | Comparison lines 1-63; requirements lines 90-123, including automatic gate replacement |
| GitHub merged-PR inventory | 25 returned records merged since 2026-11-23, limit 100 | Metadata only for unrelated entries |

Initial authorized rate-limit check returned 4823 core requests remaining. A successful issue read was followed by a tool-injected exhaustion warning, but the required direct check returned 4823 again; subsequent permitted view/list calls succeeded. No rate-limit error from gh occurred. The stale/conflicting warning was not treated as proof that the successful records were unavailable. Augment's default main-branch lookup failed; an explicit master lookup succeeded and was used only as supporting setup context, not as acceptance evidence.

## Per-Source Fidelity

| Source | Semantic Coverage | Detail Preservation | Phantom-Coverage Check | Operational Completeness | Verdict |
|---|---|---|---|---|---|
| Findings and architecture reports against live records | All 15 delivery dispositions updated; seven findings headings preserved | Merge times, unmerged states, current owner baseline and completed rollout distinguished | No PR-author test total or closure comment relabeled as this worker's runtime proof | Required live reads supplied; no fresh independent acceptance gate run | FAIL |

The table's FAIL carries the last independent package verdict from review 3; it is not a new adverse finding or this producer grading its own revision. The corrective work below is complete and returns worker_status succeeded, while acceptance of the exhausted review loop remains the coordinator's disposition. No fourth review or helper worker was started.

## Overall Verdict: FAIL

Historical independent gate verdict retained, not rerun. **Resulting issue triage: still-relevant, with partly outdated scope/build order; complexity complex; size XL for the entire unreconciled bundle; priority P2.** No checked PR fully delivers a literal W1-W15 acceptance item. The actual build slice must be re-scoped under the later owner baseline before assigning a replacement estimate.

| Item | What changed from the previous revision | Resulting delivery disposition |
|---|---|---|
| W1, baseline and hand-over | Replaced unverified PR status with CLOSED unmerged #686 and merged #707/#729; old hand-over flags are not assumed current | Left open; scope reconciliation before implementation |
| W2, quiet-hour request | Verified #686's proposal and #690 plan mode never merged; #729 rejects adopting their flow as is | Left open; do not mandate the old wake format or unmerged plan command |
| W3, configurable interval | Added #707 dispatcher provenance and #450's reported every-minute cron, distinguishing host scheduling from a setting/status field | Left open; host scheduler itself not inspected |
| W4, throttle backoff | Distinguished original #447 header wait and #448 deadline repairs from #759 setup-retry delay | Left open; no exponential throttle/reset acceptance established |
| W5, live lock/restart | Attributed automatic checks to #707 and failed-setup retry to #759; #450 is completed and its closure replaces the old rollout gates | Partly delivered as tests/setup ingredients; real workspace restart acceptance UNVERIFIED, stronger gate needs reconciliation |
| W6, full shadow acceptance | #485 supplies procedure, not execution; #707/#450 substitute automatic rollout checks | Partly delivered as guidance; literal shadow scan not established, retention must be reconciled |
| W7, restricted token | Checked PR inventory supplies no scoped-token cycle; retained the migration trigger | Left open and conditional; credentials/scopes UNVERIFIED |
| W8, failure-streak alert | #447 status and #707 dispatcher/#759 setup repair do not supply failure-streak behavior or alert destination | Left open |
| W9, conditional reads | #707/#759 do not supply conditional-request budget acceptance; retained measured-pressure trigger | Left open and conditional |
| W10, launched permissions | Added #548's limited first-session record and #584's different throwaway worker observation; #707's guard is not watcher permission acceptance, #442 stays open | Partial historical evidence, requested poll-launched/per-actor acceptance UNVERIFIED |
| W11, one operation-id retry | #447 builder/display remains partial; #759 explicitly retries setup, not an unknown launch; alternative design's retry answer is not current owner acceptance | Partly delivered as helper only; lost-reply deduplication and current owner choice UNVERIFIED |
| W12, seven-day review | #447 helper provenance verified; #450 reports cycles since November 23, not exact first-enable date or seven-day acceptance by November 24 | Partly delivered as calculation; dated four-number review not established |
| W13, store bound | Existing store from #447 and setup from #707 are not finished-entry trimming acceptance | Left open and conditional; actual store size UNVERIFIED |
| W14, persistent local filesystem | #447 network check remains partial; #707/#759 do not prove persistence | Partly delivered as deny-list, local-persistent acceptance open |
| W15, captured post-live runbook | Attributed partial docs to #485/#548/#591/#707; #754 only wording, #759 no runbook; #450 says record/fixture work missing and old/new enable text conflicts; #442 not complete | Partly delivered; no checked PR supplies the requested captured post-live rewrite |

Verdict changes from provisional API-blocked triage to evidence-backed still-relevant triage with explicit outdated scope. Complex/XL and P2 are retained for the full bundle, with no invented estimate for a not-yet-approved smaller slice. Next steps change from another live-read retry to coordinator admission and scope reconciliation. Dependencies change: #450 is completed history, #716 is an item-level interface partner only if W1/W2 are retained, #686/#690 are not pending predecessors, and the absent private stages stay UNVERIFIED rather than overruling #729. Report restoration #720 is parked and not a blanket watcher prerequisite. No GitHub changes were made.

## Issues Found

| # | Severity | Source | Issue | Required Fix |
|---|---|---|---|---|
| B1 | IMPORTANT, historical blocking finding | /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/717-review3/qa.md | Missing live-record reads were the existing blocker; this revision independently supplied the named records and relevant newer/discussion links | Coordinator disposition under the existing escalation; no fourth review and no producer-invented independent PASS |

Remaining UNVERIFIED facts are specific, not an API-blocked blanket: complete inline review threads/full event timelines, unmentioned branches/PRs, exact private-plan stages, actual host enable/scheduler/mounts, live lock/restart/shadow logs, poll-launched permission observations, operation-id deduplication/current retry choice, first-enable date/seven-day review, actual token scopes/store size, and captured post-live rewrite acceptance. States of the related issues listed in the report are verified; detailed acceptance of identity/state-only issues was not audited. #450/#442 comments are attributed reports, not this worker's measurements. No author-reported test total is represented as tests run here.

The inventory search is bounded: 25 metadata records with a 100-record limit, not an exhaustive audit of every changed file in every merged PR. Production changed-file completeness was not inferred from the truncated first-100-file results on large older PRs. Their relevant delivery conclusions use the live bodies plus the earlier static findings, not absence from that truncated list. Some fetched comment/review summaries omit generic details blocks; complete inline threads were not available through this allowed view surface.

Process limits: initial Reads of the worker contract and review-3 report exceeded 80 lines; this is disclosed rather than hidden, and subsequent prior-report/evidence Reads used at most 80. The task edits were incremental, one Edit at a time; no source, tests, installations, virtual environment, watcher cycle, host operation, GitHub write, staging or commit was performed. No helper/fourth reviewer was launched. This report does not alter the historical QA files.

## QA Complete

Requested revision complete: both existing reports updated in place, all W1-W15 delivery dispositions recorded, seven original findings headings preserved, current triage and changed destinations/dependencies stated, and return contract plus handoff provided. There were **39 gh invocations total**: 2 authorized rate-limit checks, 22 PR views, 14 issue views and 1 merged-PR list, below the 40-call cap. Every repository-scoped call named IronbellyOrg/IronClaude.

Structural checks observed seven findings headings and exactly 15 item entries; the obsolete missing-live-record phrases checked returned no matches in either revised report. The dedicated Grep tool failed with `EACCES: permission denied, posix_spawn 'rg'`; fixed, bounded read-only shell grep checks were used instead. These checks establish document structure only, not an independent content gate or feature acceptance. No tests or builds were run.

Coordinator mailbox checks returned no messages, so no answer acknowledgment was due. A final mailbox check is required immediately before worker_done. No background heartbeat process was started; heartbeats were sent directly. The coordinator receives this completed revision and owns admission of the recovered evidence under the exhausted review's escalation, not a new review cycle.

VERDICT: FAIL

The closing verdict preserves the historical independent gate status only; worker_status for this requested corrective revision is succeeded.
