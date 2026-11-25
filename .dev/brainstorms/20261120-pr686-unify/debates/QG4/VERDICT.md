# Verdict QG4: Build now or reserve (OD-7 interrupt a running worker, OD-8 lease comment, OD-9 newly assignable issues)

## Question
QG4 Build now or reserve: OD-7 (interrupt a running worker), OD-8 (build the lease comment now), OD-9 (list newly assignable issues; keep info streams off)

Terms. PR 686 is Clay's open rewrite of the issue watcher (snapshot `pr-a`, head `8e5ae29ad`). "D:nnn" is a line of Clay's design `docs/designs/orchestrator.md` on master (merged by PR 681, the design-text PR). "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` on master. N7 is the design's one exception that lets the coordinator interrupt a worker (`escalate --interrupt`, D:749, D:764). The lease comment is the design's fourth layer against a double claim (a comment `<!-- sc:orchestrator:lease ... -->`, lowest comment id wins, D:113). `could_assign` is one of three extra GitHub searches (info streams) that find newly assignable issues (D:123, D:137). U40 and U8 are rows of the design's register of unproven assumptions (U40: Orca gives no receipt that tells a steered send from a queued one, D:1298; U8: the replies of the three info searches were never captured, D:137). D15 is the earlier verdict on Clay's strengths bundle that asked these three questions as OD-7, OD-8 and OD-9.

## Winner
OURS: all three answers follow the owner's line (do not build now), and the reserve text takes six small separable improvements from Clay's side.

## Winning recommendation
The adversarial skill ran in full at depth quick (one round; advocates for both papers, orchestrator scoring, merge-executor). Convergence 88.2 percent (15 of 17 points, threshold 80). Both advocates ended on the same three answers. Merged text: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/merged-qg4-position.md`.

1. **OD-7, interrupt a running worker besides context exhaustion: No. `escalate --interrupt` (N7) is not built.** Reason: no incident is cited; Orca gives no receipt that the interrupt landed (U40, D:1298); and the next liveness nudge says "If your turn ended before worker_done, continue with your next Command: line now" (WC:164), which would undo the stop, with no rule in the design that suppresses it (D:749, D:764). CLAY's own paper concedes it is not shown to work. Source: D:749, D:764, D:1170 and D:1197 (ruling 25 is one of Clay's rulings 23 to 35), D:1298, WC:164, WC:63 and WC:124 (the one existing interrupt, S6, context exhaustion). Keep one part: the verb `escalate` writes the escalation first and sends nothing if the escalation is refused (D:749, D:764). Do not cite WC:137 as a general ban on interrupts: it is the last bullet of the "Answers and acks" block (WC:131-138) and governs typing the copy of an answer.
2. **OD-8, build the lease comment now: No. Reserved design with a recorded trigger.** Reason: the lease arbitrates only "two hosts that each run a poll, two users' orchestrators, a hand-run `--take`, a store restored from a backup" (D:113); the settled topology is one cron entry and one dispatcher on one host (D07 verdict), and no double claim is cited. A second reason: the lease as designed wedges an issue when its owner crashes before editing it to `released`, and the design has no stale-lease rule (grep of D found none; D:113, D:510, D:543-547). The risk is real, not small: the design rates it medium likelihood, medium impact and names the lease as the mitigation (K13, D:1235), and master's claim allows a re-claim by the same login (`claim.md:43`). So the reserve rests on the absent trigger. Source: D:113, D:543-547, D:1235, `claim.md:43`. Reopen when a second host or a second user runs a poll; before building add a stale-lease rule, rename the marker `sc:coordinator:lease` (naming decision D08), rewrite test T4, and reserve the state step names `plan_rechecked`, `lease_posted`, `claim_started`, `claim_done` (D:547).
3. **OD-9, list newly assignable issues (`could_assign`); keep the info streams off: Yes, keep them off. The report does not list newly assignable issues now.** Reason: the replies of the three searches are unverified (U8, D:137), and two of the three streams (`mentions`, `affects`) are subsets of what the report skill already collects with one `involves` search per org (`src/superclaude/skills/agent-work-report/scripts/collect.py:200-210`). Only `could_assign` is new, and it is awareness, never a claim (D:123). Source: D:123, D:137, `collect.py:200-210`. New fact from this debate (see Implications OD-9): in PR 686 the streams are not behind any switch today and a failed search stops the whole cycle, so "keep off" needs a code change. If the owner ever turns them on, enable `could_assign` alone, after the U8 capture.

## Strongest points
**OURS**
1. The N7 interrupt would be undone by the contract's own nudge and cannot be confirmed to land, and no incident is cited. WC:164 (nudge text), D:749 and D:764 (no suppression rule), D:1298 (U40). CLAY's advocate agreed (C-001 and C-003, both advocates OURS).
2. The lease has a defect the design does not fix, and its trigger is absent on the settled single-host topology. D:113 (scope), D:543-547 (steps, no stale rule), D07 verdict. Both advocates agreed (C-004, C-005).
3. Two of three info streams duplicate the report's `involves` search and the replies are unverified. `collect.py:200-210`, D:137 (U8). Both advocates agreed (C-006, C-007).

**CLAY**
1. The OURS paper misread WC:137 (scope is answer typing). `WORKER-CONTRACT.md:131-138`. Both advocates agreed (X-001); the correction is adopted.
2. The double-claim gap is real: master's claim treats an issue already assigned to the current login as "continue, re-claim is allowed and idempotent" (`claim.md:43`), the claim marker carries no host or session id (D:113, citing `claim.md:30`), and the design rates it M/M (K13, D:1235). OURS's "not possible" was too strong (X-002).
3. Clay's design states what N7 would cost (the five coordinator-spec changes C25 to C29, D:925-928; the caller-scoped refusal pattern, D:767), and the escalation-first ordering rule is sound. These become build conditions and a kept rule.

## Clay strengths to adopt
- **Escalation-first ordering rule (U-006).** What: `escalate` writes the escalation first and sends nothing if the escalation is refused (D:749, D:764). Why: both advocates adopt it; it is separable from the interrupt. How: spec text of the `escalate` verb with no interrupt option.
- **Build conditions for a later N7 (U-004).** What: contract exception written like S6's, the C25 to C29 changes (D:925-928), a nudge-suppression rule, a check whether `--interrupt` has its own receipt (U40 covers text sends). Why: turns "closed unless the owner asks" into a testable reopen list. How: a reserved-design list in the unified spec.
- **Reserve the persisted names and the trigger (U-005, K13).** What: keep `plan_rechecked`, `lease_posted`, `claim_started`, `claim_done` (D:547) and the renamed marker free; write the trigger "a second host or user runs a poll"; state K13's M/M rating. Why: a later build needs no migration; the reserve is honest about a real risk. How: reserved-design list and runbook line; override only the marker name (D08).
- **`could_assign` alone (C-007).** What: if streams are ever enabled, fetch only `could_assign`. Why: the other two duplicate `involves`. How: switch (see Actions).
- **Correction of the WC:137 reading (X-001).** What: do not cite line 137 as a ban. Why: verified at `WORKER-CONTRACT.md:131-138`. How: spec wording "no contract text authorizes a second interrupt".
- **Cheap checks before a later decision (A-001).** What: U8 is three GitHub searches (D:137); U40 starts with `orca terminal send --help` and then one local send into a busy worker (D:1298), and that send is a write into a session, so it is not read-only. Why: turns two unknowns into facts. How: run in the live-test phase (Actions).

## Our strengths that must be kept
- The owner's weighting rule result: no new write path, no new interrupt, no new GitHub comment without a shown benefit (D06, D09, D15 verdicts).
- The reserved-design form with an explicit trigger per question, and "closed unless the owner asks" for OD-7.
- The poll's rule of reading little and writing nothing (NG-2, D09 verdict).
- The sweep and the report skill as the one reader of "involves" items (`collect.py:200-210`, D11 verdict).
- The launch guard and the person's typed go as the real brakes for irreversible actions (D05, D06 verdicts).

## Actions
| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Delete the "Interrupt a worker, in one case" row, the N7 text, the `--interrupt` option from the verb lists, the N7 test rows, and do not apply C25 to C29; keep the escalation-first rule in the `escalate` text | DOC | `docs/designs/orchestrator.md` lines 140, 510, 749, 764, 925-928, 1106, 1117 (same action as D15 row D9) | O1 |
| Move the lease to a reserved-design list: trigger, stale-lease rule needed first, marker `sc:coordinator:lease`, reserved step names, T4 rewritten, K13 note; drop `lease` from the verb list | DOC | `docs/designs/orchestrator.md` lines 113, 510, 543-547, 1235; test table T4 (same action as D15 row C8) | O1 |
| Add a runbook line that names the trigger for the lease ("a second host or a second user runs a poll") | DOC | issue watcher runbook / unified spec | O1 |
| State in the unified spec that no contract text authorizes a second interrupt, and that `WORKER-CONTRACT.md:137` governs answer typing only | DOC | unified spec (`.dev/brainstorms/20261120-pr686-unify/`) | O1 |
| Adapt PR 686 so the info streams are off: add an explicit off switch (default off) around the loop at `cycle.py:922-935`, make a failed or rate-limited info search a warning and not a stop of the cycle before any enabling, and fetch only `could_assign` when enabled | PR KEEP-ADAPT | PR 686: `cycle.py:922-935`, `github.py:100`, `:171-176`, `wake.py:149` | O3, in the adapted 686a |
| Run the live checks: U8 (three read-only searches) and U40 (`orca terminal send --help`, then one local send into a busy worker: needs the owner's go because it types into a session) | DECISION | owner or live-test session; issue 442, PR 685 (live evidence) | O7, before the poll is enabled |
| Owner confirms in chat the three answers OD-7 No, OD-8 No, OD-9 No (the agent records it; the owner writes no file) | DECISION | owner `ironbelly` | O0 |

## Implications
**OD-7 (no interrupt verb).**
- Coordinator: the verb list loses the interrupt option (D15 R-7 already lists the 12 verbs it builds with no interrupt option; this confirms it). A coordinator that sees a worker about to take an irreversible action has the escalation and the person's go only; it never presses interrupt (WC:137 scope aside, no text allows it).
- Breaks: nothing built. Two design places need text edits (D:749, D:764) and the coordinator-spec lines C25 to C29 are not applied.
- Owner must know: the brake for an irreversible worker action is the launch guard and the person's go, not a coordinator interrupt; a worker already past its check is not stopped by a coordinator.
**OD-8 (no lease now).**
- Watcher and claim pipeline: no new comment per issue, no new grant-bound write (`issue.comment`), no change to the claim chain. One host, one dispatcher stays the rule.
- Breaks: nothing today. If a second host or user polls, two coordinators of one login can both start; no detector notices a second poller (UNVERIFIED that none exists elsewhere), so the trigger is a written rule, not an alarm.
- Owner must know: the design itself rates this risk medium/medium (K13); the reserve is a bet on the one-host topology holding. A time-based stale-lease rule would give up the "no clock agreement between hosts" property D:113 names (orchestrator inference).
**OD-9 (streams off).**
- Dashboard and report: the report keeps the `involves` list; no "newly assignable" line.
- Poll: new finding, verified in the `pr-a` snapshot: the loop at `cycle.py:922-935` runs all three searches for every org in every cycle with no off switch, and `_val` (`cycle.py:894-900`) turns any failed or rate-limited shared read into `_Stop(read.reason)`. So a bad or changed reply of an unverified stream stops the whole discovery cycle, the opposite of the "fail-open" the D15 verdict and the papers assume. The poll is globally `enabled: false` today, so nothing runs; but "keep off" is not true in the code until the switch is added. Also `could_assign` rows are kept only for repos in the list `self.rdoc.get(item.repo)` (`cycle.py:931`), and D15 removes the registry file that list comes from (D07, R-3), so the filter needs a new source. These two points are not in the merged file; they were found after the merge by reading `pr-a`.
- Cost: about 8 calls of the 35 per cycle if enabled (D:137).

## Confidence
OD-7 85 percent; OD-8 75 percent; OD-9 85 percent for "off" (the answer), 70 percent that the code change in Actions row 5 is the smallest fix. Overall 80 percent. It would rise with a U40 receipt that shows an interrupt lands and stays, or with a shown stale-lease rule; it would fall if a second host or user is already polling (OD-8), if the owner wants awareness of newly assignable issues now (OD-9), or if an incident shows a worker doing an irreversible action that only an interrupt would have stopped (OD-7).

## Unverified
- Whether `--interrupt` has its own receipt (U40 covers text sends only; D:1298).
- The reply shapes of the three info searches (U8, D:137); the PR 686 tests use assumed-shape fixtures (`github.py:778-783`).
- That no stale-lease rule exists anywhere in the design (the orchestrator's grep covered lines containing `lease`; some very long design lines were cut in earlier greps).
- That no detector of a second poller exists anywhere.
- The D07 topology verdict was not re-read by the advocates; the orchestrator relied on D15 and the verdict text.
- Whether a failed info search on a malformed (not failed) reply also stops the cycle (only the failed-read path was read).
- The cost of a later lease migration (asserted by CLAY, not measured).
- The scoring layer was applied by one evaluator in two orders (no independent second judge); the margin was large and the quantitative layer was a tie.

## Debate artifacts
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/merged-qg4-position.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/variant-1-original.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/variant-2-original.md`
