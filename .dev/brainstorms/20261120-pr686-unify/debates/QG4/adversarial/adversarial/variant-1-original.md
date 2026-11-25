# QG4 position paper: OURS (the owner's line)

Status: header stub. Sections are appended below.

Topic: build now or reserve. OD-7 (interrupt a running worker), OD-8 (build the lease comment now), OD-9 (list newly assignable issues, keep the info streams off).
Terms: PR 686 = Clay's open rewrite of the issue watcher. "D:nnn" = a line of `docs/designs/orchestrator.md` on master (Clay's design, merged by PR 681, snapshot `/home/coder/.cache/ic-snap-20261120/master`). "U40", "U8" = rows of the design's register of unproven assumptions (U40: Orca gives no receipt that tells a steered send from a queued one; U8: the replies of the three info searches were never captured). D15 = the earlier verdict on Clay's strengths bundle.

## Claim
Answer No to all three: OD-7 no interrupt verb, OD-8 no lease comment now (reserved design with a trigger), OD-9 the info streams stay off. Each is a capability whose trigger is absent or whose working is unproven. Under the weighting rule an unobserved risk or an unproven benefit is a tie, and a tie goes to the owner's line.

## OD-7: May the coordinator ever interrupt a running worker besides context exhaustion? No.
Mechanism: `escalate --interrupt` (N7) would write an escalation, then send `orca terminal send --interrupt` to stop a worker's current turn (D:749, D:764). It is exempt from the 60-second typing hold.
Facts:
1. The contract already has exactly one interrupt, the context-exhausted nudge S6 (WC-14 exception, `src/superclaude/core/WORKER-CONTRACT.md:63`; nudge table `:152`). The input-veto line says "never interrupt" (`:137`). N7 would be a second interrupt case with no contract text behind it (Clay's own advocate concedes this, D15 round2-rebuttal-2-clay.md G-6).
2. Orca gives no receipt telling "steered" from "queued" (U40, D:1298), so the interrupt cannot be confirmed to have landed.
3. After an interrupt the worker sits idle; the next L2 nudge says "continue with your next Command: line now" (WC:164) and would undo it. The design has no rule that suppresses the nudge after N7 (D:749, D:764, D:1117).
4. No incident is cited. Ruling 25 that added N7 is one of Clay's rulings 23 to 35 (D:1170, D:1197), not the owner's.
5. The escalation is written first anyway, so the person is told; the interrupt adds only the stop. An interrupt does not undo what is already done.
6. The real brakes for the escalation rows are the launch guard and the person's typed go (D05, D06 verdicts).
7. Both advocates in D15 already agreed on "not built" (D15 debate transcript row G-6, 85 percent).
Cost of No: a worker about to do an irreversible thing is not stopped by the coordinator before the person reads the report.
Risk of No: low; the launch guard and the person's go remain.
What it gets right: keep the ordering rule "write the escalation first, send nothing if it is refused" as a rule of `escalate`.

## OD-8: Build the lease comment before a second host or user runs a poll? No (reserved design).
Mechanism: before wave 1 the coordinator posts a comment `<!-- sc:orchestrator:lease host=<host> run=<run id> -->`, lists its own login's lease comments, keeps the claim only if its lease has the lowest comment id (D:113, D:543-547).
Facts:
1. The design itself says the lease arbitrates only "two hosts that each run a poll, two users' orchestrators, a hand-run `--take`, a store restored from a backup" (D:113, D:708 layer 4). Layers 1 to 3 (single router under one lock, `wrong_target`, exclusive-create state file) keep two coordinators of one host apart.
2. The topology verdict D07 gives one cron entry and one dispatcher on one host, and says a second host polling would change its verdict (D07 VERDICT).
3. No double claim is cited anywhere.
4. The owner's line has its own defences: create-once claim files on a shared branch (Q26) and the claim-marker guard `marker_in_window` (D01 item 4).
5. A defect as designed: a lease whose owner crashed before editing it to `released` keeps the lowest comment id, so a later coordinator loses and takes nothing. No stale-lease rule was found in the design (Clay's advocate concedes, round2-rebuttal-2-clay.md G-1; UNVERIFIED that none exists elsewhere).
6. Cost if built now: one extra visible comment per claimed issue, one more write needing the `issue.comment` grant and `E-NO-GRANT`, a marker renamed for the coordinator naming (D08), test T4 rewritten.
Risk of No: a double claim by two logins or hosts, not observed and not possible on the present single-host topology.
What it gets right: the race is real (re-claim by the same login is allowed, `claim.md:43`), so record the design with its trigger.

## OD-9: List newly assignable issues (`could_assign`)? No; the info streams stay off.
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

## Summary of what is kept
Keep the three as reserved design: OD-7 closed unless the owner asks (needs a contract exception written like S6's, a rule that suppresses the L2 nudge afterwards, and the U40 receipt check); OD-8 reserved with the trigger "a second host or a second user runs a poll" plus a stale-lease rule and marker `sc:coordinator:lease`; OD-9 off until the U8 live capture, then an owner decision.
