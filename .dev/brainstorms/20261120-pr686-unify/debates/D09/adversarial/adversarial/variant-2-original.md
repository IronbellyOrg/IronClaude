# Position CLAY: D09 watcher writes to GitHub

Advocate for Clay's line (design 681, PR 686). Line references D:nnn are to `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master/`.

## Claim

An issue with no plan is not ready, and the system must not spend a launch on it. The cheapest, most visible and most reversible mark is one GitHub label, `hold:plan`, written by the poll and nothing else. The write is narrow (add or remove one label), has no comment, is tested, and gives the owner and every other person a mark on the issue they already look at. The plan request after one hour turns a stuck hold into a plan with no person in the loop.

## Mechanism

1. `plan_check(body)` is one pure text function: three headings (`## Priority`, `## Fix approach`, `## Test plan`) each present once and not empty or "Not known yet" (D:440). It uses no model and no GitHub call.
2. The poll reads body and labels from the search row it already fetches, so the decision costs no extra call (D:448). It adds `hold:plan` to a failing issue and removes it when the check passes (D:444, table rows 3 to 6 at D:450-457). `hold:backlog` is placed only by a person and the poll only reads it (D:445).
3. After one quiet hour with no sign of plan work elsewhere (E1 to E4, D:467-476) the poll writes one `plan_requests[]` item into the wake file. The coordinator runs `/sc:issue --plan <N>`, which fills the three sections; the poll lifts the hold on its next cycle (D:478-484).
4. The lease comment (DQ3, D:113) is written by the orchestrator, not the poll, and exists to arbitrate two claimers.

## Cited facts

1. The gap is real: nothing in master holds a plan-less issue. PR 651 (plan sections in the issue templates) only adds the sections; it does not stop an empty issue from being claimed. Source: `H-design681-map.md:53` ("Nothing held plan-less issues (#651 only adds template sections)").
2. The writes are the narrowest possible. Design: "The grant covers two writes: add the label, remove it. The poll posts no comment about the hold" (D:444, D:463, ruling 33). PR 686 code matches: `github.py:14-18` of the PR head says the only writes are create-label, add, remove; the only DELETE is `repos/<R>/issues/<N>/labels/hold:plan`; an injected `guard` can refuse any argv.
3. The write boundary is still tested. PR 686 rewrote the NG-2 test from "nothing writes" to "the only writes to GitHub are the three calls on the `hold:plan` label" (`pr-a/tests/issue_watch/test_security_invariants.py:12`, `:288`, `:634`). The security property changed shape, it was not dropped.
4. The hold is a precondition and not a trigger or approval: "Assignment stays the only trigger (R1): the hold is a precondition on the issue, not a trigger and not an approval that anybody gives" (D:438). A person can still remove the label by hand and the poll never puts it back (D:446, AD-A9), so a person always wins.
5. It protects the stop switch: `hold:backlog` makes the system "do nothing at all with this issue" and the poll never writes it (D:445, row 1 at D:452). That is a human stop that works on every repo with no config file.
6. Cost of the read side is small: E1 costs no call; E2 to E4 are read once an hour and count against the call budget (D:476). `--dry-run` runs the whole hold step and writes nothing, so a 24-hour shadow run shows the holds before any write (D:461).
7. The failure mode of the write is bounded: a refused write is `hold_write_failed`, a warning with exit 0, the issue is skipped and the write is retried next cycle (D:454, D:340). It never launches an issue on a failed write.
8. Switch-on is safe: "the baseline records every issue already assigned and step 7a never touches a recorded issue, so no label or comment is written on the 17 issues already assigned" (D:492).
9. The human approval that OURS leans on is not on master: PR 682 deleted the approval code (FULL-REPORT section 3), and issue 655 chose "assignment is the only trigger". With no human gate on master, the plan check is the only thing between an empty issue and a launched worker (D:73, R1).

## What it costs

- The poll gains write rights on one label per repo, and the `hold:plan` label must be created once per repo (D:444). `test_hold.py` and about 60 lines of design rules.
- The poll's store gets a `holds` map (D:486).

## What it risks

- A wrong write repeats each cycle until noticed (bounded by the retry-next-cycle rule and the call budget).
- The search index can show a label one cycle late; the design adds a live read (D:456, D:494).
- A label written by the shared `ironbelly` login does not show who acted (FULL-REPORT section 1, item 7). This is true of every GitHub action on this host, including the claim comments.

## What it gets right

- Early, cheap, visible: the issue says "plan missing" where people look.
- Reduces a launch spent on an empty issue, a cost OURS does not guard (the accuracy check runs after the launch).
- Keeps humans in control: hand-removed hold stays removed; `hold:backlog` is the owner's stop.
- Stateless-ish and idempotent: the one-per-hold rule means one plan request per hold, even across restarts (D:478).

## Weak point conceded

The lease comment and the one-hour plan request depend on the orchestrator topology (several orchestrators per repo, three in flight) that is another debate topic (D07). They are not needed by the plan hold itself.
