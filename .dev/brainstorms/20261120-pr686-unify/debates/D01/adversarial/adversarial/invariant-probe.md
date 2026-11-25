# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis (agent a8f916068f69d205f; orchestrator verified INV-001 and INV-002 against source)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | The poll's gates still hold when the worker actually starts (live re-check "still passes", `orchestrator.md:317`) | UNADDRESSED | HIGH | PR 686 wave-1 re-check covers `hold:backlog` and `plan_check` only (`orchestrator.md:488`, `:543`); `pr-a/.../cycle.py:1279-1305` has no approval, edit or Status read; master `_revalidate` (`cycle.py:979`, called `:1058`) re-reads approval and Status. A gap exists between wake and claim; `hold:backlog` applied after wake is honoured only at wave 1 (`pr-a/.../cycle.py:992-1005`) |
| INV-002 | interaction_effects | A manual `/sc:issue --claim` of an approved issue cannot cause a double start | UNADDRESSED | HIGH | Master: a `CLAIM_MARKER` comment after approval makes `_examine` mark the issue claimed without launching (`cycle.py:858,946-947`, `marker_in_window`); `/sc:issue --claim` posts that marker (`refs/claim.md:30,92`). PR 686 keeps only the constant (`pr-a/.../predicates.py:18`); its layers (DQ3) cover poll store, `O_EXCL` state file and a lease comment, and layer 4 says a claim by the current login is idempotent |
| INV-003 | state_variables | `plan_check` can be a skip reason ahead of approval without changing the approval's lifetime | UNADDRESSED | MEDIUM (HIGH if the plan-request flow is kept) | `unchanged_since` voids on any body edit at or after approval, whoever made it (`predicates.py:249-259`); the plan request is done by an agent under the same login and edits the body (`orchestrator.md:484`), so the approval must come after the plan exists; PR 686 writes `hold:plan` labels (`pr-a/.../cycle.py:1067,1080`) |
| INV-004 | sufficiency_challenge | Assignment plus an allowed approver's unedited approval stops an unwanted start | UNADDRESSED | MEDIUM | Falsifier: an agent on the watcher's own login assigns and approves; self-approval is warn-only (R33 item 3); orchestrator and Clay share the login (`orchestrator.md:111`); L-1 shared by both positions |
| INV-005 | sufficiency_challenge | The consensus start rule is a tested combination of existing gates | UNADDRESSED | MEDIUM | The gates exist in different trees: approval and `unchanged_since` on master and the planb branch; Status allow-list and R35 field events only on branch `ironbelly/issue-watcher-zero-setup-plan`; `plan_check` and `hold:backlog` only in PR 686; no file shows them together; PR 686 deletes what the planb branch extends |
| INV-006 | guard_conditions | The trigger label is redundant or harmless to keep | UNADDRESSED | MEDIUM | `approval_of` makes it load-bearing: approval must follow the last trigger event (`approval_before_trigger`), no trigger event gives `events_incomplete`, same-second events give `events_incomplete` (`predicates.py:204-231`); field events take an id equal to epoch seconds on the planb branch (`github.py:866-890`) |
| INV-007 | guard_conditions | `unchanged_since` is neutral to the approver's own follow-up | UNADDRESSED | MEDIUM | Only comments by the own login are exempt (`predicates.py:253-255`); the body is never exempt; refusal reason `edited_after_approval` does not say who edited |
| INV-008 | state_variables | Assignment can stand in for a person's decision because the assigner is trusted | UNADDRESSED | LOW | Neither check reads `assigned`/`unassigned` events; approval is not bound to who the assignee was; two assignees is skipped (`predicates.py:169-174`) |
| INV-009 | state_variables | Store-init floor and baseline behave the same for an approval-gated start | UNADDRESSED | MEDIUM | Master refuses approvals at or before store creation (`approval_before_init`, `predicates.py:230-231`); PR 686 baseline marks issues assigned at switch-on as seen and never woken (`orchestrator.md:264`, `:492`; `pr-a/.../cycle.py:992-994`) so such an issue needs `--take` |
| INV-010 | count_divergence | "Status allow-list (R22)" names one list | ADDRESSED (code) | LOW | Planb `ALLOWED_STATUSES` has four values (Research, Spec, Plan, Debug), `Ready` excluded; master requires Backlog (inverted polarity, `predicates.py:262-271`); `hold:backlog` and Backlog status are two overlapping stop mechanisms |
| INV-011 | count_divergence | "Assigned only to the own login" is one rule | UNADDRESSED | LOW | DQ1 (`orchestrator.md:111`): no other assignee; file-map row (`:399`): all assignees in the user set, at least one; equal with one login |
| INV-012 | collection_boundaries | Event and comment evidence is complete; empty or multiple approvers behave sanely | ADDRESSED | LOW | Reads capped at 5 pages of 100 and fail closed (`incomplete`, `truncated`, `github.py:40-44,599-628,809-824`); empty approver set approves nobody; last `labeled` event decides |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 2 (INV-010, INV-012)
- **UNADDRESSED**: 10
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 6 (INV-003, INV-004, INV-005, INV-006, INV-007, INV-009)
  - LOW: 2 (INV-008, INV-011)
