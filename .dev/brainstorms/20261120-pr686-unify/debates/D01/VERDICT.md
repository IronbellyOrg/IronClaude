# Verdict D01: Trigger and approval gate

## Question
Should a newly assigned issue alone start the work (CLAY R1: assignment is the only trigger, no trigger label, no approver list, no plan-approval gate, D:73), or must a human approval stay as the gate (OURS R19, R22, R35, R36: approval label plus the issue Status or `Approved` field)? Which code in `src/superclaude/cli/issue_watch/` (predicates.py, github.py, cycle.py) survives?

## Winner
HYBRID: the owner's rule decides the trigger (assignment alone never starts work; an approval stays the gate), and Clay's plan check and `hold:backlog` veto are adopted as extra read-only skip reasons.

## Winning recommendation
The spec must say:

1. **Start rule.** A worker is started for an issue only when all of these hold: (a) the issue is open and assigned only to the watcher's own login; (b) an allowed approver's approval (the organisation issue field `Approved` = `Yes` per R35; the `issue-watch:approved` label until R35 is live) is present and unedited since (`unchanged_since`, `src/superclaude/cli/issue_watch/predicates.py:237-259`); (c) the Project Status is in the allow-list Research, Spec, Plan, Debug (R22); (d) the label `hold:backlog` is absent; (e) `plan_check(body).ok` is true. Assignment alone never starts work.
2. **New skip reasons, read-only.** `plan_check` (from `hold.py:122-143` in PR 686, Clay's rewrite of the watcher) and `hold:backlog` are evaluated before the approval counts. The watcher writes no label for them (NG-2, `docs/designs/issue-watcher.md:76`); whether any label write is ever allowed is topic D09.
3. **MR-1 (found by the invariant probe, HIGH).** The check made at the moment of start must repeat the approval, `unchanged_since` and the Status allow-list, not only `plan_check` and `hold:backlog`. Master has this in `_revalidate` (`cycle.py:979`, called at `:1058`); PR 686's wave-1 re-check covers only `hold:backlog` and `plan_check` (`docs/designs/orchestrator.md:488`).
4. **MR-2 (found by the invariant probe, HIGH).** Keep the claim-marker guard `marker_in_window` (`cycle.py:858,946-947`). `/sc:issue --claim` itself assigns the issue and posts the claim marker (`SKILL.md:87`, `refs/claim.md:30,92`), so without the guard a hand claim plus a watcher start can run two workers.
5. **Ordering.** The plan must exist before the approval: the plan request is an agent edit of the issue body, and any body edit after the approval voids it (`predicates.py:249-259`). Document this in the runbook and test it.
6. **Conditions to revisit.** Assignment alone may be reconsidered only when all four hold: the launch guard refuses to start when it is not effective (topic D05); workers cannot push or merge (topic D06); the watcher skips an issue that already has a claim record or worktree (MR-2); the owner records the reversal of R19 in chat.
7. **Trigger label.** The separate `issue-watch:trigger` label is redundant once assignment does its discovery job, but R35 (line 61) says it stays and `approval_of` makes it load-bearing (`predicates.py:204-231`). Keep it for now; dropping it is the owner's decision (see Actions).

## Strongest points
**OURS**
1. Assignment is an effect of claiming, not a go signal: `/sc:issue --claim` runs `--add-assignee @me` (`src/superclaude/skills/sc-issue-protocol/SKILL.md:87`, `refs/claim.md:48`). Clay's advocate conceded it.
2. The owner has recorded the gate more than once: REQ R19 (requirements line 45), "Gates that stay manual" (lines 102-104), R35 keeps the trigger label, and R36 (line 62) withdraws only R31, keeping the edit rule. Clay's advocate called this "decisive".
3. The consequence of removing the gate is large in Clay's design: the same assignment ends in a worker with no launch guard, pushes and an orchestrator merge (`orchestrator.md:117,118,1234`) on an unprotected `master` (`gh api repos/IronbellyOrg/IronClaude/branches/master` printed `protected: false`, 0 rulesets, 2026-11-20).

**CLAY**
1. `plan_check` is a real readiness signal that the approval never gave (`hold.py:122-143`); both advocates want it as a skip reason (C-005 won by Clay at 75%).
2. A login-based approval is weak against an agent on the same login (accepted risk L-1, `.dev/analyze/pr686-20261120/E-pr682.md:75`; orchestrator and Clay share the login, `orchestrator.md:111`). Owner's advocate conceded it.
3. Their design is not silent about edits: AD-A3 / ruling 23 (`orchestrator.md:488`) decides deliberately that edits before and after the claim are fine, with a wave-1 live re-check and a report line for a later edit by someone else. This narrowed the owner's content-binding argument (C-006 from 85 to 65 percent).

## Clay strengths to adopt
- **`plan_check(body)`** (`hold.py:122-143`, pure, no I/O, plus its pure helpers and tests in `tests/issue_watch/test_hold.py`). Why: no check in the owner's line verifies the issue has a plan, and the approval can be placed on an empty issue (`H-design681-map.md:53`). Merge: import as a function; skip reason `plan_incomplete` evaluated before the approval; keep the three headings of issue 651 (Clay's plan-sections change for `/sc:issue`); leave out `table_row`, `new_hold`, `with_evidence`, `plan_request_due` and the label writer (topic D09).
- **`hold:backlog` as a person's veto.** Why: a cheap opt-out beside the opt-in approval; labels are already in the discovery row (`pr-a/.../predicates.py:139-160`). Merge: read-only skip reason `held_backlog`; it overlaps with Status Backlog being outside the R22 allow-list (INV-010), so state both in the runbook.
- **The reopening principle.** Clay's advocate stated when assignment alone would be safe; adopted as the "Conditions to revisit" in the recommendation.

## Our strengths that must be kept
- Assignment is necessary, never sufficient (`argv_discover` already filters on assignee and trigger label, `github.py:180-198`).
- `approval_of`, `unchanged_since`, `project_check` turned into the R22 allow-list, `marker_in_window`, `is_intended_owner`, `eligibility_order` and the evidence dataclasses (`LabelEvent`, `EditEvidence`, `MarkerEvidence`, `ProjectItem`, `ApprovalResult`) in `predicates.py`.
- In `github.py`: discovery, `events`, `edits`, `marker_comments`, `project_items`, and the R23/R35 additions on the planb branch (Pipeline field, field events).
- In `cycle.py`: `_approve`, `_claim`, `_revalidate`, `_hit`, `validate_approvers`.
- Closed ship gate (`GOVERNED_LEVELS_ALLOWED = False`, R33), Status allow-list (R22), and the approvals-in-chat rule.
- The symbol diff of master against PR 686 shows what the contested rule would delete: 14 symbols in `predicates.py` and about 30 in `github.py`.

## Actions
| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Write the hybrid start rule and MR-1, MR-2, ordering and revisit conditions into the unified spec | DOC | `.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/merged-output.md` (section "Merged recommendation") | First; other verdicts D03, D05, D06, D09 feed the revisit conditions |
| Do not merge PR 686 (Clay's rewrite of the watcher) as it removes the approval, trigger, Project and approver code; keep and reuse `hold.py` `plan_check` and its tests | PR KEEP-ADAPT | PR 686 (final disposition is topic D14) | After D01 and D09 |
| Add `plan_incomplete` and `held_backlog` read-only skip reasons before the approval check, reusing `plan_check` | LOCAL CHANGE | `issue_watch/predicates.py`, `cycle.py` on branch `ironbelly/issue-watcher-zero-setup-plan` (worktree `claim-handoff-planb`) | After the running `/sc:implement` plan finishes, to avoid editing the same files |
| Make the start-time re-check cover approval, `unchanged_since`, Status allow-list, `plan_check`, `hold:backlog` (MR-1), with a test that removing the approval between wake and start refuses | LOCAL CHANGE | `issue_watch/cycle.py` (`_revalidate`) | Same pass as the row above |
| Keep `marker_in_window` and add a test: an approved issue with a manual `/sc:issue --claim` marker is not launched (MR-2) | LOCAL CHANGE | `issue_watch/cycle.py`, `tests/issue_watch/test_cycle.py` | Same pass |
| Document and test the plan-before-approval ordering | LOCAL CHANGE | `docs/designs/issue-watcher.md`, `docs/designs/issue-watcher-setup.md` | After the skip reasons exist |
| Confirm in chat that R19 stands (approval stays the gate) and decide whether the trigger label stays; agent records the answer; answer Clay on issue 450 (owner's roll-out issue for the watcher) | DECISION | Owner, issues 450 and 655 | Needed before PR 686 is judged (D14) |
| Mark the trigger sentence of R1 (D:73), DQ1 and 4.11 ("no person has to set or approve anything") as superseded by the owner's rule | DOC | `docs/designs/orchestrator.md` lines 73, 111, 488 | After the owner confirms R19 |
| Correct FULL-REPORT section 7: R36 withdraws R31 only, it does not withdraw the Status gate | DOC | `.dev/analyze/pr686-20261120/FULL-REPORT.md` line 96 | Any time |
| PR 682 (Clay's deletion of the issue-pipeline plan-approval code): this verdict does not decide it; the start approval and the plan approval after the claim are different gates | DECISION | Topic D03 | D03 |

## Implications
- **Watcher.** The owner's watcher keeps its trigger code, so PR 686 must be rebased onto it or split; PR 686 and the planb branch edit the same files (`predicates.py`, `github.py`, `cycle.py`, `launch.py`) and the probe found no tree that contains both rule sets (INV-005). Issues assigned before switch-on are baselined as "seen" in PR 686 and never woken, so an approved one needs `--take` (INV-009).
- **Coordinator or orchestrator.** Whatever starts the worker must repeat the start gates (MR-1); a wake alone is not a start. The plan-request agent edits the body and voids an earlier approval, so approval comes after the plan (INV-003).
- **Dashboard.** Two new skip reasons (`plan_incomplete`, `held_backlog`) must appear in the audit reasons the observer and dashboard read.
- **Claim pipeline.** A hand claim must not double start (MR-2). Because the claim assigns the issue, "assigned" cannot be shown to the user as "approved".
- **What breaks.** Dropping the approval would remove the only code that ties a person's yes to the content (14 predicate symbols, about 30 github.py symbols). Keeping it keeps the burden Clay names: one manual set of `Approved` per issue.
- **For the owner.** Clay's comment on issue 450 is still without a recorded answer; this verdict is a recommendation, not the owner's ruling. The weighting rule decided it, and Clay's side conceded R19 as decisive.

## Confidence
78 percent. It would drop below 60 if the owner reverses R19 in chat, if D05 and D06 show workers claim-only with an effective guard, or if live GitHub shows the `Approved` field events cannot be read reliably. It would rise if a test shows MR-1 and MR-2 hold on the merged tree.

## Unverified
- Whether a read-only user can self-assign an issue, and the exact set of apps and bots with issue-write permission (`orchestrator.md:134` OQ6).
- The shape of `Approved` field timeline events on live GitHub (the planb branch used assumed-shape fixtures); field event ids equal epoch seconds there (INV-006).
- Whether the trigger label can be dropped without changing `approval_of` (the ordering rule at `predicates.py:226-229`).
- Whether any of the owner's chat approvals of R19 on 2026-11-18 came before or after Clay's comment on issue 450 (17:00:32); the hour is unrecorded.
- Scores in `base-selection.md` are single-evaluator estimates; the position-bias check was not independent.
- `docs/designs/orchestrator.md:1234` (K12) was verified by the orchestrator, not by the owner's advocate.
- The first Round 2 request to advocate A did not return; Round 2 was re-run with fresh agents. Return contract status is `partial` because two HIGH invariants (INV-001, INV-002) were unaddressed in the advocates' consensus and were turned into requirements instead of another round.

## Debate artifacts
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/position-OURS.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/position-CLAY.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/merged-output.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/return-contract.yaml
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/diff-analysis.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/debate-transcript.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/invariant-probe.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/base-selection.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/refactor-plan.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/merge-log.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/return-contract.yaml
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/adversarial/adversarial/variant-1-original.md and variant-2-original.md
