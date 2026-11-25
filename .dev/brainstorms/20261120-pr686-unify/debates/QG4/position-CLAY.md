# QG4 position paper: CLAY (Clay's line)

Status: header stub. Sections are appended below.

Topic: build now or reserve. OD-7 (interrupt a running worker), OD-8 (build the lease comment now), OD-9 (list newly assignable issues, keep the info streams off).
Terms: PR 686 = Clay's open rewrite of the issue watcher. "D:nnn" = a line of `docs/designs/orchestrator.md` on master (Clay's design, merged by PR 681, snapshot `/home/coder/.cache/ic-snap-20261120/master`). U40, U8 = rows of the design's register of unproven assumptions.

## Claim
Build all three now, each as designed. Each closes a hole that the owner's line leaves open, the code or text for two of the three already exists, and a later build costs a migration. A narrow, guarded capability beats a reserved one.

## OD-7: Build `escalate --interrupt` (N7). Yes, narrowly.
Mechanism: the verb writes the escalation first and sends nothing if the escalation is refused. Only then it sends `orca terminal send --interrupt` to stop one worker's current turn, only for a case that fits a row of the nine-row table (identity, secret, money, legal, irreversible, other people's access, breaking change), one caller, one verb (D:749, D:764, D:767).
Facts:
1. A worker about to take an irreversible action in rows 1 to 7 could be stopped before the person reads the report. The owner's line has no way to stop it (the S6 interrupt covers context exhaustion only, `WORKER-CONTRACT.md:63`, `:124`).
2. The guard is narrow: escalation first, one caller, no `answer_ref` pass path after D15's N6 change; the `refuse(argv)` pattern for N7 is the only caller-scoped branch (D:767).
3. The design states the exemption openly and lists the five coordinator-spec changes C25 to C29 (D:925-928), so nothing is hidden.
4. The "never interrupt" rule (`WORKER-CONTRACT.md:137`) sits under "Answers and acks" and governs the typed ack copy; the S6 row proves it is not a general rule (Clay's advocate, round2-rebuttal-2-clay.md G-6).
5. Cost: one verb option, one contract exception, one row in the table.
Risks: Orca gives no receipt, so landing is unconfirmed (U40); the L2 nudge text "continue with your next Command: line now" (WC:164) would undo the interrupt unless a suppression rule is added; no incident is cited.
What it gets right: the escalation-first ordering rule.
Honest limit: with those risks the capability is not shown to work (Clay's own advocate concedes, "no clear benefit").

## OD-8: Build the lease comment now. Yes.
Mechanism: `lease post` then `lease check` before `/sc:issue --claim`; lowest comment id wins; the loser edits its lease to `released` (D:113, D:543-547).
Facts:
1. The gap in the owner's line is real: master's claim treats an issue already assigned to the current login as "continue, re-claim is allowed and idempotent" (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:43`), so two coordinators on one login are not stopped by the claim.
2. The exclusive-create state file is host-local and git-ignored (D:115, D07 point 3), so it cannot arbitrate across hosts or users.
3. The lease needs one comment and no new GitHub feature.
4. Later adds cost a migration of persisted names and state steps (`lease_posted`, `claim_started`, D:547).
5. The poll can be started by a second user or host with no code change; nothing prevents it today.
Risks: a lease whose owner crashed before `released` keeps the lowest id and wedges the issue, and the design has no stale-lease rule; one more visible comment per issue and one more grant-bound write; the trigger (a second host or user polling) is not present and no double claim has been observed (D07).
What it gets right: the design says plainly what the lease is for.

## OD-9: List newly assignable issues (`could_assign`) and turn the info streams on. Yes.
Mechanism: three info searches per org (mentions, could_assign, affects), about 8 calls a cycle against a budget of 35 (D:137); the wake carries `info.mentions[]`, `info.could_assign[]`, `info.affects[]` (D:184); entries live 14 days under "Watching" (D:123, D:873).
Facts:
1. `could_assign` is awareness the owner's report does not have (`collect.py:200-209` collects "involves" only).
2. The code is written and tested with fixtures: `github.py:171-176` (`argv_search_info`), `cycle.py:931`, `:1644`, `:1770`, `wake.py:149`, `:239`.
3. The cost fits the call budget.
4. It is read-only; nothing is claimed or written.
Risks: the replies of the three searches are UNVERIFIED (U8, D:137), the fixtures are assumed-shape; `mention` and `affects` duplicate "involves"; it widens what the poll reads beyond discovery.
What it gets right: awareness of unassigned work with no write.

## Summary
CLAY's best honest position: OD-7 loses on evidence (U40, nudge undo, no incident), OD-8 is a real gap with no present trigger and an unsolved stale-lease defect, OD-9 is unproven (U8) but harmless if off; CLAY's separable benefits are the escalation-first ordering rule (OD-7), the recorded trigger and marker design (OD-8) and keeping the written code behind a switch (OD-9).
