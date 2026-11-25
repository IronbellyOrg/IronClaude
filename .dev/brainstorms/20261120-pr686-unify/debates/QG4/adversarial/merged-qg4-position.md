<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS) -->
<!-- Merge date: 2026-11-20 -->

# QG4 merged position: build now or reserve (OD-7, OD-8, OD-9)

<!-- Source: Base (original, modified) - retitled per the merge instruction; stub status line replaced by a merged status line -->
Status: merged position. Base: Variant 1 (OURS); eight planned changes applied from the refactoring plan.

Topic: build now or reserve. OD-7 (interrupt a running worker), OD-8 (build the lease comment now), OD-9 (list newly assignable issues, keep the info streams off).
Terms: PR 686 = Clay's open rewrite of the issue watcher. "D:nnn" = a line of `docs/designs/orchestrator.md` on master (Clay's design, merged by PR 681, snapshot `/home/coder/.cache/ic-snap-20261120/master`). "U40", "U8" = rows of the design's register of unproven assumptions (U40: Orca gives no receipt that tells a steered send from a queued one; U8: the replies of the three info searches were never captured). D15 = the earlier verdict on Clay's strengths bundle.

## Claim
<!-- Source: Base (original) -->
Answer No to all three: OD-7 no interrupt verb, OD-8 no lease comment now (reserved design with a trigger), OD-9 the info streams stay off. Each is a capability whose trigger is absent or whose working is unproven. Under the weighting rule an unobserved risk or an unproven benefit is a tie, and a tie goes to the owner's line.

## OD-7: May the coordinator ever interrupt a running worker besides context exhaustion? No.
<!-- Source: Base (original, modified) - Fact 1 corrected per Change #1; hybrid line inserted after Fact 7 per Change #2 -->
Mechanism: `escalate --interrupt` (N7) would write an escalation, then send `orca terminal send --interrupt` to stop a worker's current turn (D:749, D:764). It is exempt from the 60-second typing hold.
Facts:
<!-- Source: Base (original, modified) - Change #1: the WC:137 claim corrected (X-001) -->
1. The contract already has exactly one interrupt, the context-exhausted nudge S6 (WC-14 exception, `src/superclaude/core/WORKER-CONTRACT.md:63`; nudge table `:152`). Line 137 (input veto) belongs to the "Answers and acks" block (`:131-138`) and governs the typed copy of an answer, so it is not a general ban; the point that stands is that no contract text authorizes a second interrupt: D:749 and D:764 add the exception themselves and D:764 says it conflicts with the coordinator spec in five places. N7 would be a second interrupt case with no contract text behind it (Clay's own advocate concedes this, D15 round2-rebuttal-2-clay.md G-6).
2. Orca gives no receipt telling "steered" from "queued" (U40, D:1298), so the interrupt cannot be confirmed to have landed.
3. After an interrupt the worker sits idle; the next L2 nudge says "continue with your next Command: line now" (WC:164) and would undo it. The design has no rule that suppresses the nudge after N7 (D:749, D:764, D:1117).
4. No incident is cited. Ruling 25 that added N7 is one of Clay's rulings 23 to 35 (D:1170, D:1197), not the owner's.
5. The escalation is written first anyway, so the person is told; the interrupt adds only the stop. An interrupt does not undo what is already done.
6. The real brakes for the escalation rows are the launch guard and the person's typed go (D05, D06 verdicts).
7. Both advocates in D15 already agreed on "not built" (D15 debate transcript row G-6, 85 percent).
<!-- Source: Variant 2 (CLAY), Section OD-7 "What it gets right" - merged per Change #2 -->
Hybrid kept: the verb `escalate` writes the escalation first and sends nothing if the escalation is refused (D:749, D:764), with no interrupt option.
<!-- Source: Base (original) -->
Cost of No: a worker about to do an irreversible thing is not stopped by the coordinator before the person reads the report.
Risk of No: low; the launch guard and the person's go remain.
What it gets right: keep the ordering rule "write the escalation first, send nothing if it is refused" as a rule of `escalate`.

## OD-8: Build the lease comment before a second host or user runs a poll? No (reserved design).
<!-- Source: Base (original, modified) - Fact 4 narrowed per Change #5; Risk of No replaced per Change #4; detector gap inserted per Change #8 -->
Mechanism: before wave 1 the coordinator posts a comment `<!-- sc:orchestrator:lease host=<host> run=<run id> -->`, lists its own login's lease comments, keeps the claim only if its lease has the lowest comment id (D:113, D:543-547).
Facts:
1. The design itself says the lease arbitrates only "two hosts that each run a poll, two users' orchestrators, a hand-run `--take`, a store restored from a backup" (D:113, D:708 layer 4). Layers 1 to 3 (single router under one lock, `wrong_target`, exclusive-create state file) keep two coordinators of one host apart.
2. The topology verdict D07 gives one cron entry and one dispatcher on one host, and says a second host polling would change its verdict (D07 VERDICT).
3. No double claim is cited anywhere.
<!-- Source: Variant 2 (CLAY), Section OD-8 Fact 4 and orchestrator check of predicates.py:279-293 - merged per Change #5 -->
4. The owner's line has the create-once claim files on a shared branch (Q26) and the claim-marker check `marker_in_window` (`src/superclaude/cli/issue_watch/predicates.py:279-293`, D01 item 4). The marker check counts an own-login claim marker only after the claim exists, so it does not close the window before the marker is posted.
<!-- Source: Base (original) -->
5. A defect as designed: a lease whose owner crashed before editing it to `released` keeps the lowest comment id, so a later coordinator loses and takes nothing. No stale-lease rule was found in the design (Clay's advocate concedes, round2-rebuttal-2-clay.md G-1; UNVERIFIED that none exists elsewhere).
6. Cost if built now: one extra visible comment per claimed issue, one more write needing the `issue.comment` grant and `E-NO-GRANT`, a marker renamed for the coordinator naming (D08), test T4 rewritten.
<!-- Source: Base (original, modified) - Change #4: "not possible" softened to "trigger not present", K13 added (X-002) -->
Risk of No: a double claim by two logins, two users or two hosts. The trigger is not present on the settled one-host topology (D07) and none has been observed. The design itself rates the risk medium likelihood, medium impact and names the lease as its mitigation (K13, D:1235), so the reserve rests on the absent trigger, not on a small risk.
<!-- Source: Base (original) -->
What it gets right: the race is real (re-claim by the same login is allowed, `claim.md:43`), so record the design with its trigger.
<!-- Source: Variant 2 (CLAY), Section OD-8 weakness 4 (detector gap) - merged per Change #8 -->
Known gap: no rule notices that a second host or user has started a poll, so the trigger depends on someone remembering (no detector found; UNVERIFIED that none exists elsewhere). Writing the trigger into the spec and the runbook is the minimum.

## OD-9: List newly assignable issues (`could_assign`)? No; the info streams stay off.
<!-- Source: Base (original, modified) - closing paragraph appended per Change #7 -->
Mechanism: three extra search streams per org (about 8 calls a cycle against a budget of 35, D:137) and an information entry per kind under "Watching", kept 14 days (D:123).
Facts:
1. `mention` and `affects` are subsets of what the report already collects: `involves(org, person)` runs one `gh search issues --owner <org> --involves <person>` per org (`src/superclaude/skills/agent-work-report/scripts/collect.py:200-209`).
2. Only `could_assign` (new unassigned issues) is new, and it is awareness, never a claim (D:123).
3. The replies of the three searches are UNVERIFIED (U8; D:137 says the live test captures them), and the fixtures are assumed-shape, so off is also the evidence-based default.
4. The poll's rule is to read little and write nothing (NG-2, D09 verdict); three more reads widen the poll beyond discovery.
5. The code already exists in PR 686 (`github.py:100`, `:171-176`, `cycle.py:931`, `:1644`, `wake.py:149`), so it stays behind one off switch with the org-wide search switch (D07 item 6); deleting it costs more than switching it off.
Cost of No: no report line for newly assignable issues until the owner asks.
Risk of No: none to safety; a missed-assignment awareness gap only.
What it gets right: the code is written and fail-open; keep it behind the switch.
<!-- Source: Variant 2 (CLAY), Section OD-9 (C-007 hybrid, A-001 cheap checks) - merged per Change #7 -->
If the owner ever turns the streams on, enable `could_assign` alone: `mention` and `affects` are subsets of `involves`. The two unproven assumptions behind OD-7 and OD-9 are cheap, read-only checks: U8 is three searches (D:137) and U40 is `orca terminal send --help` plus one local send (D:1298). Run them before the owner decides on a later build.

## Summary of what is kept
<!-- Source: Base (original, modified) - OD-7 clause replaced per Change #3; OD-8 clause replaced per Change #6; OD-9 clause extended per Change #7 -->
Keep the three as reserved design.

<!-- Source: Variant 2 (CLAY), Section OD-7 Fact 3 (D:925-928) - merged per Change #3 -->
OD-7 closed unless the owner asks. To reopen it: (a) a contract exception written like S6's (WC:63, WC:124); (b) the five coordinator-spec changes C25 to C29 (D:925-928); (c) a rule that suppresses the L2 nudge after an interrupt (WC:164); (d) a check whether `--interrupt` has its own receipt, because U40 (D:1298) covers text sends only.

<!-- Source: Variant 2 (CLAY), Section OD-8 Fact 4 (D:547) and D:113 - merged per Change #6 -->
OD-8 reserved. Trigger: a second host or a second user runs a poll. Before building: a stale-lease rule (a time-based rule would give up the "no clock agreement between hosts" property D:113 names, so this is a design task; orchestrator inference); the marker renamed `sc:coordinator:lease` (D08); the state step names `plan_rechecked`, `lease_posted`, `claim_started`, `claim_done` (D:547) reserved so a later build needs no migration; test T4 rewritten.

<!-- Source: Base (original, modified) - OD-9 clause kept; Change #7 text appended -->
OD-9 off until the U8 live capture, then an owner decision. If the owner ever turns the streams on, enable `could_assign` alone: `mention` and `affects` are subsets of `involves`. The two unproven assumptions behind OD-7 and OD-9 are cheap, read-only checks: U8 is three searches (D:137) and U40 is `orca terminal send --help` plus one local send (D:1298). Run them before the owner decides on a later build.
