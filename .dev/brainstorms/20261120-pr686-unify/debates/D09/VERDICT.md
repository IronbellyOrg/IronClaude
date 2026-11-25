# Verdict D09: Watcher writes to GitHub

## Question

CLAY's poll writes labels `hold:plan` and `hold:backlog`, a plan check, a plan request after one hour and a lease comment (D:410, D:436-495, DQ3). OURS: `docs/designs/issue-watcher.md` NG-2 and owner decision D2 say the poller never assigns, comments or moves Project items. Is the plan hold a clear benefit worth adopting, and if so under which rule change (which writes are allowed, by whom)?

## Winner

HYBRID: take Clay's read-only plan check, the `held_incomplete` skip and the person-set `hold:backlog` stop now; keep the owner's rule that the poll writes nothing to GitHub, because the one write Clay adds (the `hold:plan` label) has no evidenced benefit yet.

## Winning recommendation

Terms: "poll" is the unattended cron job that watches for newly assigned issues (PR 686, Clay's rewrite of the watcher, changes it). "Plan check" is `plan_check(body)` in PR 686's `hold.py`: a text-only test that the issue body has the three sections Priority, Fix approach and Test plan filled in.

The spec must say, in this order:

1. **Adopt now, read-only.** The poll runs `plan_check` on the issue body it already fetches and skips a failing issue with the reason `held_incomplete`. Nothing is written to GitHub. Test: a failing issue is never woken or launched and the argv scan finds no write call.
2. **Only three parties ever write the hold.** A person places `hold:backlog` (the poll only reads it and does nothing with that issue). The per-repo init creates both labels once (`hold:plan` and `hold:backlog`). The poll never creates a label and never comments about a hold.
3. **The label write is deferred, not rejected.** If the owner later wants a GitHub-visible mark, the only poll write allowed is add or remove of the existing label `hold:plan`, only in a repo that holds the `issue.hold` grant, and NG-2 is amended to name exactly those two calls at that time. D2 is unchanged: it names assign, comment and Project moves, and a label add is none of them (`/home/coder/.cache/ic-snap-20261120/master/docs/designs/issue-watcher.md:41-43`, `:48`). Until the amendment lands, NG-2 stays as written (`issue-watcher.md:76`).
4. **Switch-on gate for item 3.** A 24-hour `--dry-run` shadow run has shown the holds, and a test has shown that `gh` can add and remove a label under cron's minimal environment (write scope; only the login was tested, `requirements.md:97`).
5. **Every other write stays with the coordinator or orchestrator under a grant row** (R24: the owner's rule that a coordinator write needs that issue's own grant row). The plan body write (`/sc:issue --plan`, grant `issue.body.append_plan_sections`) and the lease comment are not poll writes. The one-hour plan request is a wake-file item, not a GitHub write. All three wait for the topology decision D07.
6. **Fixes the debate found, as spec lines:** `plan_check` runs before the approval read; a `<...>` placeholder-only section counts as empty (moderator verified: today only HTML comments are stripped, `pr-a/.../hold.py:69-70`, `:140`, so the unfilled issue template passes); with no grant a failing issue is skipped as `held_incomplete` with no warning and a leftover label is ignored (today it warns every cycle, `cycle.py:1021-1027`, `test_hold.py:416-426`); the poll may read an issue body for `plan_check` only, held in memory and never put in the audit log, the store, argv or a typed line; one poll per repo is a stated rule; a failed write is remembered for the cycle.
7. **Name the tree.** The spec says which commit it describes. Master's poll still calls `approval_of` (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/issue_watch/cycle.py:883`, `:998`); PR 686's head has no such call (0 matches). So "no human approval gate" describes the PR 686 head and design PR 681, not master.

## Strongest points

OURS:
1. The write boundary is an owner decision with tests behind it: NG-2 (`issue-watcher.md:76`), D2 (`:41-43`), master tests (`tests/issue_watch/test_security_invariants.py:10`, `:245-251`, `:693-698`), and the chain in which workers never write and every other write needs a grant row (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:9`, R24 in `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:50`).
2. The label's only unique effect is visibility, and nobody could show it is used. Both advocates conceded this in Round 2 (debate-transcript.md, Round 2). By the owner's bar (a clear, evidenced benefit) it is a tie, and a tie goes to OURS.
3. The label write is the costly part of Clay's hold and its dormant form is unclean: the hold still works without the label (`orchestrator.md:455`, `:494`), yet the label drags in rows 3 to 6, a `hand_removed` state and a live read, and with no grant PR 686 warns every cycle (`cycle.py:1021-1027`, `test_hold.py:416-426`).

CLAY:
1. The gap is real and the check is cheap and separable: nothing holds a plan-less issue today (`H-design681-map.md:53`), and `plan_check` is a pure text function with no GitHub call (`orchestrator.md:440`). OURS conceded it fills a gap OURS lacks.
2. The write form is narrow and already tested: add or remove one label, no comment (`orchestrator.md:444`, `:463`), a grant switch, `--dry-run` that writes nothing (`:461`), a baseline that never touches the 17 already-assigned issues (`:492`), and a rewritten NG-2 test that pins exactly the label calls (`pr-a/tests/issue_watch/test_security_invariants.py:12`, `:288`, `:634`).
3. OURS' "the poll never writes" was too absolute: the owner's own local branch already creates a label from the watcher package (`claim-handoff-planb/src/superclaude/cli/issue_watch/repo_init.py:72`, `:116`, `first_run.py:192`, requirements R11 and R30). That is a once-per-repo first-run write, not a per-issue write each cycle (`dispatch.py:72`, `:353`).

## Clay strengths to adopt

- **Read-only `plan_check` and the `held_incomplete` skip.** Why: OURS has no early check, and its accuracy check runs after a launch is spent. How to merge: adopt it into the poll; fix the placeholder gap (rule 6), run it before the approval read, and amend the owner's no-body rule (NFR-002, `issue-watcher.md:226`) so the body may be read for this check only.
- **`hold:backlog`, a person-set stop label that the poll only reads.** Why: a stop switch on GitHub with no config file and no poll write (`orchestrator.md:445`, row 1 `:452`). How to merge: init creates the label (R11); the poll skips the issue with no other action.
- **`--dry-run` that shows the holds before any write, plus the switch-on baseline.** Why: it makes any later label write testable at no risk. How to merge: they become the gate in recommendation item 4.
- **The narrow label-write form as the pre-agreed fallback.** Why: if the owner wants a GitHub-visible mark, the form is already designed and tested (add and remove only, grant gated, no comment). How to merge: keep PR 686's code only if the owner chooses to ship it dormant (see Actions A6); creation moves to init; the NG-2 test changes from three calls to two.

## Our strengths that must be kept

- NG-2 as written, and D2, until the day the label write is enabled; the poll never comments, assigns, moves a Project item or creates a label.
- Coordinator-only writes with a per-issue grant row (R24); workers never write (WC-9).
- The edit-voids-approval rule (R19, R36 `edited_after_approval`): a held issue that is filled in after an approval needs a fresh approval. It fails closed.
- GitHub text never reaches a typed line, the audit log or the store (NFR-002); the body read for `plan_check` stays in memory.
- The per-issue grant row, and the coordinator as the one place a person's go is recorded.

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Write recommendation items 1 to 7 into the unified design as the D09 rules | DOC | unified design spec (D14 output) | First |
| Keep `plan_check` and the `held_incomplete` skip; add the `<...>` placeholder rule; evaluate before the approval read | PR KEEP-ADAPT | PR 686 `hold.py`, `cycle.py` (Clay's watcher rewrite) | After the DOC row |
| Amend the no-body rule so the body may be read for `plan_check` only, in memory | LOCAL CHANGE | `docs/designs/issue-watcher.md:226` and the NFR-002 tests in the owner's local branch | With the `plan_check` row |
| Keep the label code only if shipped dormant: remove label creation from the poll, fix the no-grant state, change the NG-2 test from three calls to two | PR KEEP-ADAPT | PR 686 `github.py` (`LabelWriter`), `cycle.py:1021-1044`, `test_hold.py:416-426`, `test_security_invariants.py:12` | Only if the owner picks "ship dormant" |
| Decide whether the dormant label-write code ships in PR 686 now or is removed until later (the one point the debate left open; Clay does not object to removal but did not size the rework of design 4.11 rows 3 to 6) | DECISION | owner | Before PR 686 merges |
| Create both labels in the per-repo init | LOCAL CHANGE | `claim-handoff-planb/src/superclaude/cli/issue_watch/repo_init.py` | Before the label write is ever enabled |
| Label-write-under-cron test and a 24-hour dry-run shadow run | LOCAL CHANGE | tests and the watcher runbook | Gate for enabling the label write |
| Amend NG-2 to name exactly add and remove of `hold:plan` | DOC | `docs/designs/issue-watcher.md:76` | Only at the moment the label write is enabled |
| Defer the one-hour plan request and the lease comment | DECISION | topic D07 (topology) | D07 result |
| Name the commit or design each rule describes; replace "master has no human gate" | DOC | unified design spec | With the first DOC row |

## Implications

- **Watcher.** The poll stays read-only on GitHub (adopting the check adds a body read, no write). It skips failing issues and records `held_incomplete` in its audit log. PR 686's design 4.11 rows 3 to 6, the `holds` map and `hand_removed` only matter if the label write is switched on.
- **Visibility.** With no label, a held issue shows only in `issue-watch status` and the audit log. The sweep (`/sc:sweep`, PR 539, read-only) and the observer behind the issue 409 dashboard design should read that output or the audit log, or a plan-less issue is invisible to everyone but the owner (a point for D11).
- **Coordinator and claim pipeline.** A held issue is never sent to a coordinator (`orchestrator.md:459`), so plans are created by a person or by `/sc:issue --plan` (PR 690, open) and the poll never starts that. Where the owner's approval gate stays (local branch), an issue approved while empty and then filled in is refused as edited after approval and needs a fresh approval.
- **What breaks.** PR 686's NG-2 test pins three label calls and will change; the unfilled issue template passes `plan_check` until the placeholder rule lands; two workspaces polling one repo would re-add a hand-removed label unless one poll per repo is enforced.
- **The owner must know.** (a) The poll in PR 686 removes the claim-time approval that master's poll still has, so on that tree the plan check is the only gate; (b) the three writes in the question are not all poll writes: the plan request is a wake-file item and the lease comment and plan body are the orchestrator's; (c) the owner's own local branch already writes a label once per repo at first run.

## Confidence

78 percent. It would rise with evidence that someone reads `hold:plan` or with a passing label-write test under cron. It would fall if the owner decides GitHub visibility of a hold is required now (the label write then ships, in its narrow form), or if D07 keeps several orchestrators per repo so the lease comment and plan request must be written by the poll side.

## Unverified

- Whether anyone reads `hold:plan` on GitHub; ruling 33's owner authority and its "as Jay does" comparison.
- Label write scope under cron (only the login was tested, `requirements.md:97`, `:110`).
- Whether the owner's per-repo init runs unattended (R18 says automatic, `requirements.md:44`).
- The edit-voids-approval claim at `predicates.py:275-297` and the ordering of `plan_check` against the approval read: the local branch has no hold code (agent-reported, not re-read).
- That PR 682 deleted the post-claim plan approval and that issue 655 chose "assignment is the only trigger" (Clay's paper; the full report records it, not re-read in this debate).
- The probe items INV-003, INV-005 to INV-008 and INV-010 (agent-reported, not re-read), including whether two workspaces share a poll store and the 4.7 second regex timing.
- The "about 22 of 58 tests" figure is a rough count by test name.
- The scoring was done by two agent evaluators; the six disagreements were settled by the moderator.

## Debate artifacts

- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/position-OURS.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/position-CLAY.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/merged-output.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/return-contract.yaml
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/diff-analysis.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/debate-transcript.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/invariant-probe.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/base-selection.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/refactor-plan.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/merge-log.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/return-contract.yaml
- Adversarial status: partial (convergence 0.93, one unresolved point, two HIGH probe items cleared by moderator resolution; see the return contract).
