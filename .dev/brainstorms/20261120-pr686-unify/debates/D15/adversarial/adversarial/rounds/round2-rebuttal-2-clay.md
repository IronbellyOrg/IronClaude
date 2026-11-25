# D15 Round 2: Rebuttal for Variant 2 (CLAY)

Topic: Clay strengths bundle, what to adopt and how. Variant 2 = CLAY. "They" means Clay (account `clayphi`); the repository owner is `ironbelly`. Weighting rule: OURS wins unless CLAY shows a clear, evidenced benefit; a tie goes to OURS; a clear separable CLAY benefit is a HYBRID.

Notation: "D:nnn" is a line of `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master`. "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` in the same export. "Dnn" is `debates/Dnn/VERDICT.md` under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`. "pr-a" and "pr-p" are the PR 686 and PR 690 exports in `/home/coder/.cache/ic-snap-20261120`. "R2-OURS" is `round2-rebuttal-1-ours.md`.

## Facts I read myself in this round

- Design: D:56-141 (goals, DQ1 to DQ13, ADD1 to ADD6), D:540-548 (wave 1), D:563-629 (waves 4 to 9, the hand-back), D:664-700 (5.6), D:720-734 (5.8), D:740-771 (5.9), D:796-849 (5.10 end, 5.11, 5.12), D:902-930 (the C-amendments), D:1083, D:1121-1143 (T1 to T13), and the `interrupt` lines found by grep.
- Contract: WC:36-75, WC:100-205, WC:232-248.
- Verdicts: D01 in full, D06 lines 9-38, and greps of D01 to D13 for hand-back, ADD1, permission prompt, FR-24, notice and lease.
- Code: master `predicates.py` (`unchanged_since`), master `agent-work-report/scripts/collect.py:199-218`, master `sc-closeout-protocol/refs/settle.md:62-68` and `refs/result.md:40-47`, master `sc-issue-protocol/refs/tiers.md`, master `ccsession:1001-1010`, master `launch.py` (zero `ccsession` or `--tier` hits), pr-a `repos.py:30-60`, pr-a `github.py:165-176`, pr-p `commands/issue.md:9-46`, pr-p `refs/plan.md:54-62`.
- Counts I ran read-only: `gh pr list --repo IronbellyOrg/IronClaude --state merged --limit 30` gives 25 of 30 bodies with "Generated with" (same as OURS); a grep of master `src`, `tests`, `docs` for a bare seven-equals line gives one hit, `src/superclaude/cli/swarm/tmux.py:9`, which is a reStructuredText underline; the same grep for `<<<<<<< ` or `>>>>>>> ` at line start gives none.

Not read by me, so UNVERIFIED: the coordinator spec (IronFlow) rows FR-8, FR-10, FR-23, FR-24, Q12 and the source lines of C25 to C29; `refs/claim.md` Wave 2 (I know it only as quoted at D:113 and D:544); the Orca behaviour of `--agent claude` workers with respect to permission prompts; the owner's unpushed plan rows (R9, R17, R23, R25, R33); D:300-420 (the poll code table), so my completeness check of the amendment list covers only the rows listed above.

---

# TASK A: Response to the OURS Round 2 rebuttal on C-001 to C-009, X-001, X-002

## A1. Which OURS concessions I accept

OURS moved to my position on nearly every point. I accept these:

| OURS concession (R2-OURS) | My answer |
|---|---|
| W4/C-005: hand-back, cap and restart, acknowledged wake are capability gaps and are adopted | Accept. |
| W5/C-004: wake is HYBRID (CLAY transport, OURS conditions M1 and M2) | Accept. |
| W6/C-003: relabel from OURS to HYBRID; closed, pinned reasons table kept; 14 approval reasons come back for D01; rewrite the pin at `test_audit.py:86-98` | Accept. |
| W7/X-001: withdraws "unbuilt counts against a piece"; X-001 is SPLIT | Accept. |
| W8/A-001: every row says "depends on owner decision" where the verdict says so | Accept. |
| C-006 OURS, C-007 tie to OURS, C-009 OURS on home with CLAY key names, X-002 tie to OURS | Accept (I already conceded all four). |
| A2.1 and A2.2: OURS decides every rule row; control verbs built once against one contract (D:140) for the nine verbs that have verdicts | Accept, with the substrate point in A3.1. |
| A2.3: T1 to T13, the U-register and the K-register are the skeleton of the test plan | Accept as the skeleton. The count of rewritten rows is in A3.2. |
| W1: two of my five interlocks (the `refuse` release pass at D:767 and the `--interrupt` pass) disappear if G-9 and G-6 go OURS' way | Accept. I agree with G-9 (N6) and G-6 below, so those two edges are gone. This is a real saving of OURS' approach and I do not dispute it. |
| A1 W2: nine of the 12 verbs already have a verdict; three (`lease`, `escalate`, `handback`) had none | Accept as a count. One nuance: `escalate` is partly covered by D11 (the nine-row table lives in the notice step only, the cap is a proposal). The part with no verdict is the `--interrupt` option, which is G-6. |

## A2. The four things I asked the judges to take: where OURS stands

1. "OURS decides every rule row": accepted by OURS.
2. "Control verbs built as one group against one contract": accepted for the nine verbs and for what Task B decides. OURS narrows the "tested together" part to the merge path. I add one thing (A3.1).
3. "T1 to T13 and the registers as the single plan": accepted as a skeleton. OURS says six rows need a logic rewrite. I accept those six and add a smaller setup edit for most other rows (A3.2).
4. "A named amendment list": OURS says it is finite only after Task B. I accept that (A3.3).

## A3. Points still in dispute

### A3.1 C-001: the unit that must be built and tested together

OURS: only the merge path is one unit (merge gate, go entry, `answer-check`, `E-NO-GRANT`, `repos` guard, T13); the other adopted verbs are independent.

Contest, with evidence. There is a wider shared base that OURS' list leaves out, and it is in the design text, not in a verdict:

- `refuse(argv, answer_ref, caller)` is one function that "every `gh`, `git` and `orca` call that a `superclaude orchestrator` verb makes passes through" (D:767), and "every verb's runner refuses a listed argv, exits 2 and logs the reason" (D:1117). Every verb, not only the merge ones, runs on it.
- The state lock `.orchestrator/state.lock` is used by `escalate` (the `asks.json` file, in the "daily cap" paragraph of 5.6), by `handback` (D:613 "under the state lock"), by routing (D:318) and by `state`.
- All verbs print one JSON contract (D:140).

So the true closure is: a small substrate (runner, `refuse`, JSON contract, state lock) that every verb uses, plus the merge path on top of it. OURS is right that the other verbs do not need to be tested together with the merge path. I am right that they all need the substrate first. The practical effect: build the substrate once and early, then the verbs in any order, with the merge path tested as one unit.

Final: HYBRID (as OURS now says), with the unit defined as "substrate first, merge path as one tested unit, other verbs separable".

### A3.2 Single test plan: size of the rewrite

I read D:1123-1139. OURS lists six rows with a logic rewrite: T1, T3, T4, T8, T10, T11. I accept that list. Reasons I checked: T1 and T3 use `repos.yaml` and `clone_parent` (D07, G-8); T4 is the lease (G-1); T8 expects an autonomous merge of a clean PR (D06 item 1 needs a person's go); T10 has the poll start orchestrator 2 (D07); T11 has the poll write `hold:plan` labels (D09).

What OURS understates: D01 puts the approval back, so "assigned to the user" no longer starts work. Every row that starts a worker (T1, T2, T5, T6, T7, T9, T10, T11, T12) needs a setup step that approves the throwaway issue after its plan exists (D01 item 5 ordering). D05 (launch guard marker and preflight) and D06 item 5 (Full Submit route for the PR) also change how a worker is started. This is a setup edit, not a logic rewrite, and I have not counted it exactly (UNVERIFIED count). It supports OURS' word "skeleton". It does not change my view that the plan, the U-register and the K-register are the right base, since OURS has no coordinator-layer plan of its own that I can find.

Final: HYBRID. Base plan = T1 to T13 and the registers; six logic rewrites; one setup edit on most other rows; T12 gets the re-approval step (G-3); T13 gets a conflict-marker banner case (G-9).

### A3.3 Amendment list completeness

Accepted: the list of amendments in the verdicts is finite only after the nine gaps are decided. I did not list them in Round 1 and OURS found them. In the design rows I read (see the facts list) I found no further undecided row, but I did not read D:300-420, so I cannot certify completeness.

One related fact the gaps depend on: D06 item 5 says Clay's "Orchestrated issue flow" (ADD1, D:135) is not adopted, and D06 item 7 proposes a WC:70 amendment that lets a coordinator started at depth 0 by the owner's watcher count as a coordinator. So section 4 of the contract (S4, the input veto, the ladder) binds a script-started coordinator too. This matters for G-5 and G-6.

### A3.4 X-001 residual

Agreed as SPLIT. No further dispute.

## A4. Final position on each point

| Point | Final | One-line reason |
|---|---|---|
| C-001 unit of adoption | HYBRID | Rule rows decided per element by OURS; substrate built first; merge path is the one unit tested together (A3.1). |
| C-002 status of unbuilt verbs | HYBRID | Design text only, so adoption means building; one group, one contract (D:140). Nine have verdicts, three decided in Task B. |
| C-003 62-reason table | HYBRID | Closed, pinned table with kinds and exit codes is adopted; the 14 approval reasons D01 needs come back; the pin is rewritten. |
| C-004 wake transport | HYBRID | CLAY file plus acknowledgment (D10); M1 and M2 are mandatory OURS conditions. |
| C-005 tiers and hand-back | HYBRID | Hand-back adopted with change (G-3). `coordinator_tier` and `worker_tier` adopted as requests. `plan_tier` is replaced by a plain `plan_depth` (G-2), not dropped. |
| C-006 contested rules | OURS | Both papers agree. |
| C-007 who pays the rewrite | OURS (tie) | Same renames and re-homes either way. |
| C-008 readiness evidence | HYBRID | Merged and reviewed pieces count; unbuilt verbs carry no proof. |
| C-009 settings home | OURS on home, CLAY key names | `issue-watch.d/<repo>.json` with a `merge` block (D07 item 5). |
| X-001 | SPLIT | Tie on "never ran live"; "unbuilt" proves nothing either way; the benefit rests on capability gaps. |
| X-002 | Tie, so OURS | Same rewrite either way. |

---

# TASK B: The nine gaps no verdict decided

Method: for each gap I read the design lines OURS cites and the contract lines it cites, checked the reading, and applied the weighting rule. Where I agree I say so and add anything OURS missed. Where I disagree I say what the evidence is.

## Summary

| Gap | OURS outcome | My view | Final recommended outcome |
|---|---|---|---|
| G-1 lease comment | defer | Agree | Defer; reserved design with a trigger; add a stale-lease rule if ever built. |
| G-2 tier settings | adopt with change, drop `plan_tier` | Disagree in part (a factual error) | Keep `coordinator_tier` and `worker_tier`; replace `plan_tier` with `plan_depth`; efforts wait for U30. Default depth is a small owner decision. |
| G-3 hand-back | adopt with change, recorded go per later round | Agree on the need, disagree on the mechanism | Adopt; round 2 must pass the D01 start gate. Owner picks: re-approval after re-plan (default) or no body edit. |
| G-4 naming rule | adopt with change, owner sets scope | Agree | Open owner decision; default B. |
| G-5 DQ9 | typing yes, approving prompts no | Agree | Reject approving prompts now. |
| G-6 N7 interrupt | reject, defer | Agree on outcome, correct one reasoning step | Not built; closed unless the owner asks. |
| G-7 info streams | adopt, off by default | Agree | Off; enable only after U8 live capture. |
| G-8 `setup-clone` | reject | Agree | Reject; `no_checkout` skip reason. |
| G-9 audit rows and N6 | adopt with change | Agree on AU5 and N6; disagree on "report line only" | AU5 narrowed; N6 unconditional; audit escalation uses the notice step D11 adopts. |

## G-1. Lease comment (DQ3 layer 4; D:113, D:543-547)

**OURS' reading checks out.** D:113 says layers 1 and 2 keep two orchestrators of one host apart, and that layer 4 exists for "two hosts that each run a poll, two users' orchestrators, a hand-run `--take`, a store restored from a backup". The claim's own stop does not cover the same login (quoted at D:113 from `refs/claim.md:36-43`; I read it only as quoted, UNVERIFIED in the file). D07 names a second host polling as something that would change its verdict (D07 line 83). No double claim has been observed.

**Strongest case for CLAY.** The gap in OURS is real and cited from the owner's own claim text: re-claim by the same login is allowed and idempotent. Layer 2 (`O_EXCL` state file) is host-local and git-ignored (D:115; D07 point 3). The lease is one comment and needs no new GitHub feature. That is a capability OURS lacks.

**Why it does not win.** (a) The trigger is not present: one dispatcher, one host (D07). Under the weighting rule an unobserved risk with no present trigger is a tie, so OURS. (b) A defect in the design as written: a lease whose owner crashed before editing it to `released` keeps the lowest comment id. I found no stale-lease rule or time limit in the lines that mention `lease` (grep of the design; UNVERIFIED that none exists elsewhere). A later orchestrator for the same issue would lose, record `claimed_elsewhere` and take nothing. Building it unchanged would add a way to wedge an issue.

**A small correction to R2-OURS.** It lists as a cost "an ordering rule: the D01 start re-check must run before the lease". The design already says this: D:543 "First step, the live re-check ... before the lease and the claim", with the step order `plan_rechecked` then `lease_posted` (D:547). The D01 amendment is to widen that re-check to cover approval, `unchanged_since` and Status (MR-1), not to move it.

**Final: agree, defer.** Record it as reserved design with the trigger "a second host or a second user runs a poll". If it is ever built: add a stale-lease rule, rename the marker (D08), and rewrite T4. Not an open owner decision unless the owner wants it earlier.

## G-2. Tier settings (5.8; D:720-734; D:1083)

**What agrees.** `orchestrator_tier` (renamed `coordinator_tier`): the `--tier` option exists in master (`ccsession:1001-1010`, I read it) and master `launch.py` has zero `ccsession` or `--tier` text. That is a real gap with a real mechanism. `worker_tier` as a request until U28 passes: D:726 itself says "a request, not a fact". Efforts wait for U30: agreed.

**Where OURS is wrong, with evidence.** R2-OURS drops `plan_tier` because "the owner's `/sc:issue` already routes work by complexity to pinned worker tiers (`refs/tiers.md`)". That is true for the claim and create flows (accuracy check and summary by complexity; `tiers.md` table). It is not true for `--plan`:

- `--plan` takes `--depth quick|standard|deep` with the default `quick` (pr-p `commands/issue.md:18` and `:46`).
- The depth chooses the worker: quick is `issue-worker-t3` (tier2b), standard is `issue-worker-t2`, deep is `issue-worker-t1` (pr-p `refs/plan.md:56-60`).
- Nothing in either line picks the depth from the issue's complexity for `--plan`.
- D12's deferral ("a higher tier floor at create for medium and complex, no cost baseline") is about create, not plan.

So without any key, the orchestrator's plan call has no depth and falls to the cheapest worker, which is the opposite of the stated goal G6 (D:60: stronger models plan, cheaper models build). That is a gap in OURS' outcome, not a second router.

**What OURS is right about.** `plan_tier` as designed is awkward: a tier name that the orchestrator must translate into a depth by a table in `refs/intake.md` (D:1083), and that depth then re-pins a tier through `refs/plan.md`. The table does not exist yet. That is duplication, and it is a fair complaint.

**Final recommended outcome.** Replace `plan_tier` with one plain key, `plan_depth`, whose value is a `/sc:issue` depth and is passed straight to `--depth`. No tier-name table, no second routing. `coordinator_tier` and `worker_tier` as proposals; efforts not adopted until U30. Open owner decision (small): the default value of `plan_depth`. Clay's G6 implies `deep` (his default `plan_tier` is tier1b, which is the T1 worker); `--plan`'s own default is `quick`. I do not pick one.

## G-3. Hand-back loop (wave 8; D:603-620)

**Is the extra step required by D01?** Yes, on the rule's own text, and it is stronger than OURS says:

- D01 item 1: a worker is started for an issue only when the approval is "present and unedited since" (`unchanged_since`), plus Status, `hold:backlog` and `plan_check`. D01 Implications: "Whatever starts the worker must repeat the start gates (MR-1)".
- `unchanged_since` counts the issue body's `issue_last_edited_at` at or after the approval time as a change whoever made it; only comments by the watcher's own login are skipped (master `predicates.py`, `unchanged_since`, which I read).
- The hand-back round re-plans by editing the body (`/sc:issue --plan --remaining`, D:618, grant `issue.body.append_plan_sections`). So a round-2 start would fail `edited_after_approval` by construction.
- The design never re-runs the start gate at round 2: it re-enters at wave 2 and says wave 1 "is not run again" (D:615).
- D06 item 7's proposed WC:245 amendment makes the approval label the person's go for the issue's push and pull request. With the label voided, the round-2 push has no go either.

So OURS is right that a hand-back needs the start gate again. A hand-back does not escape D01 just because the issue is already in flight.

**Where I disagree: the mechanism.** R2-OURS adds "a recorded go in chat per later round, bound to issue, round and the hash of the remaining file, checked by `answer-check`, with a new waiting step `handback_awaiting_go`". D01's mechanism is not a chat go. It is the approval itself (label or `Approved` field) set by an allowed approver, and D01 item 5 already says the order is plan first, approval after. So round 2 needs the person to re-apply the approval after the re-plan. That is the same gate used for round 1. A second mechanism (a chat go checked by `answer-check`) for one worker start, beside the label for another, is a new rule with no source. It also reuses `answer-check`, which D06 item 9 says cannot tell a person from a script. The waiting state is simpler: the start gate fails with `edited_after_approval` and the issue shows that skip reason.

**A separable alternative with evidence.** The edit that voids the approval is a choice of the design, not a need of the loop:

- The handoff already carries the remaining items: D:619 adds a block "Round <n> of at most <1 + HANDBACK_MAX>" with the earlier pull requests, what they delivered and the remaining items.
- The remaining list is also in the state file and the remaining file (D:611, D:613).
- `unchanged_since` ignores comments by the watcher's own login, so a progress comment does not void the approval.
- If the round-2 plan is not written into the body, the approved content is unchanged, D01's gate and D06's WC:245 go still hold, and each round still needs the person's go at merge (D06 item 1).

What this loses: the body does not show "Done so far / Remaining" (cosmetic), and it leaves PR 690's `--remaining` without its first caller (D12 already says its consumer is unbuilt). What it keeps: the loop's capability (compute the remaining criteria, the cap, the no-progress stop, the new branch, the new worker) with no extra person step at round start.

**Weighting.** Both OURS' outcome and mine pass D01. OURS' version is the safe default and wins a tie. Mine keeps a CLAY capability (no person step at each round start) at no loss under the owner's own rules, so it is a separable benefit. I do not claim it wins; I claim it is a real second option the owner should see.

**Final recommended outcome.** Adopt the hand-back verb, `HANDBACK_MAX` = 3 labelled "this design's value, not measured" (D:612), and the old-worker-must-be-final wait (D:614, consistent with WC:157). Round 2 must pass the D01 start gate. Genuine open owner decision: (a) the body is re-planned and the person re-applies the approval before round 2 (default, OURS), or (b) the body is left alone and the remaining list travels in the handoff round block and a comment. No new `answer-check` go for round starts either way.

## G-4. Naming rule (5.12; D:830-847)

**OURS' facts check out.** I re-ran the count: 25 of the last 30 merged PR bodies in `IronbellyOrg/IronClaude` contain "Generated with". D:832 forbids a "generated with" line in a PR body and keeps only the commit trailer (ruling 39). The design calls it owner ruling 15 but defines "the user" and "the owner" as Clay (D:3, D:11, D:830).

**What OURS missed.** The enforcement part of the design is already option B. `names_check` is run by the writer verbs `report-entry` and `escalate` and by tests over fixtures (D:847 items 1 to 3). A worker's PR body "cannot be scanned before it is written; the handoff line above is its rule" (D:847, last sentence). So the real choice is not "scan or not". It is one sentence: the handoff-prompt line at D:841 that tells workers to leave out attribution lines in commits, PR bodies and comments. That line is the one that collides with the repo's practice. Whether the owner wants those lines gone from PR bodies is an owner call; no owner file I read forbids them.

**CLAY's benefit.** A mechanical `names_check` with data-driven deny and allow lists and a measurement on real titles (U54) is a pattern OURS lacks. It is a benefit only if the owner wants a rule at all.

**Final: genuine open owner decision.** Options: (A) as written; (B) scan only the coordinator's own writers, leave the handoff line about PR bodies out, workers keep current practice; (C) no naming rule. My recommended default is B, because it matches what the design can enforce. Measure U54 before enabling the scan. I agree with OURS.

## G-5. DQ9: typing into worker terminals, approving permission prompts (D:119, D:573, D:752)

**Do WC:122, WC:137 and WC:188 forbid approving a worker's permission prompt?** Mostly yes, with one correction to how OURS reads them.

- WC:122, row S4 "blocked on a person prompt": response "capture the screen; L5 at 5 minutes ...; never answer the prompt". This is a rule in section 4, which binds the coordinator (WC:70).
- WC:137, input veto: "never interrupt; never type into a busy, S11 or S4 session; never answer a person prompt".
- WC:188 is narrower than OURS says. It is the "Never on silence" list: on silence, a passed deadline, `unverifiable` liveness or screen text alone, the coordinator never "answers a permission or person-only prompt". Read alone it forbids acting on silence, not approving after a person says so. So the load-bearing lines are WC:122 and WC:137, not WC:188.

**Does a coordinator-only exception apply?** No. There is no such exception in the text.

- ADD1 (D:135) was the design's route to a "standing-grant coordinator", and it says "everything else in the contract is unchanged". D06 item 5 does not adopt ADD1.
- D06 item 7 proposes the WC:70 amendment "or one started at depth 0 by the owner's installed watcher", which puts a script-started coordinator under the same section 4. So WC:122 and WC:137 apply to it.
- The design's own table (D:573 rule 6) approves everything except escalation rows 1 to 7, and D:752 lists "Answer one approval once" as covered. That conflicts with WC:122 and WC:137 and the design does not say so. The C-amendments (D:902-930) amend the coordinator spec in IronFlow, not the contract.

**Strongest case for CLAY.** Unattended throughput: a worker parked on a prompt is stalled until a person acts, and the FR-24 rules (single-use yes, never "always allow", re-read the screen, never rows 1 to 7, never rely on issue text) are narrow and test-pinned. That is a capability OURS lacks.

**Why it does not win.** There is no measured count of prompts that would be approved. The delay Orca adds before `agentWait` shows a prompt is unmeasured, and what Claude Code does with text typed during a tool call is UNVERIFIED (WC:198-199). ccsession sessions run with the permission bypass unless `CCSESSION_PERMISSIONS=default` is set (commit 843df6ac4, #390, in this checkout's recent log), so prompts are expected to be rare; for Orca `--agent claude` workers this is UNVERIFIED. No clear benefit, so a tie, so OURS.

**Final: agree, reject approving prompts now.** Keep: FR-24 rules (1), (2), (3), (5) as conditions on typed nudges; N1 (never type "always allow", never write permission rules; it is a restriction, so it stays). One addition: when S4 is reported (L5, every 15 minutes, WC:122 and WC:155), the report line may say which escalation row the prompt's action would fall under (rules (6) and (7) as classification text, no key sent). Later optional owner decision: a closed list of prompt classes the coordinator may approve, recorded in chat. Not open now.

## G-6. N7 `escalate --interrupt` (D:749, D:764, D:767)

**Does N7 reverse a contract rule?** Not as OURS puts it, though the outcome stands.

- OURS cites WC:137 ("Input veto: never interrupt"). That bullet sits under "Answers and acks" and governs the typed ack copy. The S6 row (WC:124) interrupts a worker with the WC-14 exception (WC:63), so "never interrupt" cannot be a general rule or S6 would break it. N7 therefore does not reverse a general rule. It adds a second interrupt case with no contract text behind it, and ADD1's "everything else unchanged" (D:135) means none is planned. C25 to C29 amend the IronFlow spec only.
- WC:188 and the ladder do not forbid an interrupt either (WC:188 says "stops a worker", and N7 says it stops only the turn).

**Reasons that do carry weight, and that OURS did not give.**

1. After an interrupt the worker sits idle at its prompt. The next sweep sees S3, and the L2 nudge text (WC:164) says "If your turn ended before worker_done, continue with your next Command: line now". That would undo the interrupt. D:749, D:764 and D:1117 describe the ordering and the hold exemption but I found no rule that suppresses the nudge after an N7 interrupt.
2. Orca gives no receipt that tells "steered" from "queued" (U40), so landing cannot be confirmed.
3. No incident is cited. Ruling 25 is Clay's (D:1197, AD-C1).
4. The escalation is written first anyway, so the person is told; the interrupt adds only the stop.

**Strongest case for CLAY.** A worker about to take an irreversible action in escalation rows 1 to 7 could be stopped before the person reads the report. That is a capability OURS lacks, with a narrow guard (escalation first, one caller, one verb). But with points 1 to 3 the capability is not shown to work, so no clear benefit.

**Final: agree, not built in the first build.** Keep the "write the escalation first, send nothing if it is refused" rule as a rule of `escalate` with no interrupt. If the owner ever asks for the interrupt: it needs a contract exception written like S6's, a rule that suppresses the L2 nudge after it, and the U40 receipt check. Closed unless the owner asks.

## G-7. DQ13 information entries and the three info streams (D:123, D:137, D:254)

**OURS' reading checks out.** The report's collector already gathers items the person is involved in: master `collect.py:199-218`, `involves(org, person)`, one `gh search issues --owner <org> --involves <person>` per pass (plus `--include-prs`). D:254 defines S4 as `involves:<login> ... -assignee:<login>` and S2 as `mentions:`, so both are subsets of "involves". `could_assign` (S3, new unassigned issues) is the only new kind. pr-a has the code (`github.py:165-176`).

**Strongest case for CLAY.** `could_assign` is awareness the owner's report does not have, the code is written, and the cost is about 8 calls a cycle against a budget of 35 (D:137).

**Why it does not win now.** The replies of S2 to S4 are UNVERIFIED (U8; D:137 says "the replies of S2 to S4 are UNVERIFIED and the live test captures them"). The fixtures are assumed-shape. An off switch is therefore also the evidence-based default, not only a taste.

**Final: agree, off by default.** Keep the read-only code behind one switch, off and fail-open, and the same off switch as D07 item 6. Enable only after the U8 live capture. `mention` and `affects` are not written as entries (the daily run already lists them and D:123 merges by URL). Owner decision (later): "list newly assignable issues in the report?" Default no.

## G-8. DQ4 `orca project setup-clone` (D:114, D:544, D:762)

**OURS' reading checks out.** D:114 rests on `repos.yaml` and `clone_parent`, which D07 removes, and on "since approvals are broad" from the coordinator spec (FR-8, Q12; UNVERIFIED, not read). Under D01 approvals are per issue, so that basis does not carry over. D:762 itself puts `setup-clone` in N5 ("machine or VM lifecycle") as the one allowed `orca project` verb. pr-a has no `setup-clone` call; my grep of pr-a `issue_watch` found none, so it is coordinator text only.

**Strongest case for CLAY.** Automatic onboarding of a repo that has an assigned issue and no checkout. A repo not in Orca has no coordinator under D07, so someone must add it.

**Why it does not win.** No owner authorization for a clone is recorded; the action changes the machine; the benefit has no measured demand. The origin check (`check_origin`, D:114) is a control both lines want and it stays.

**Final: agree, reject.** The skip reason is `no_checkout`; a person adds the project to Orca; T3's first case is dropped; the `setup-clone` exception is struck from N5. Later: if the repo count grows, a recorded authorization per repo.

## G-9. Audit escalation rows (D:825) and N6 (D:763)

### Part 1: audit escalation

**AU5.** OURS' point is verified. D:815 flags "lines the merge commit added that are conflict markers (`<<<<<<< `, `>>>>>>> `, a bare `=======`)". The one seven-equals line in master `src`, `tests` and `docs` is `src/superclaude/cli/swarm/tmux.py:9`, a reStructuredText underline under "Surface". An added heading like that would be a violation and an escalation. Narrow the rule: `<<<<<<< ` or `>>>>>>> ` at line start always counts; a bare `=======` counts only with an opener or closer among the added lines of the same file. Agreed, and add the banner case to T13 case (e).

**AU4a, AU4c fire only for out-of-gate merges.** OURS is right: the gate refuses `changes_requested` and `threads_open` (D:582-583, D06 item 3), so the audit is the only detector for a merge made outside the gate (D:812, D:814).

**Where I disagree: "report line only".** R2-OURS says the escalation goes only into the report entry and not a ClickUp DM or gate "until the owner rules on the nine-row list and the notice cap". That is stricter than the verdicts. D11 adopts the nine-row table in the notice step only, and the cap of 5 as a proposal with the key default at 0 (no cap). D06 item 11 adopts the list as an inventory for non-outward decisions, and "revert or accept" is exactly that. D:666 says an escalation reaches the person by an entry, a gate or a notice. The DM channel already exists in the report skill (D11, report Steps 13 and 14). OURS' own argument says the volume is low, and D:825 says one escalation per pull request. The benefit is timing: AU4a, AU4c and AU5 mean a merged result that is possibly broken or unreviewed, and a line in a living report waits until someone opens it.

**Final (part 1).** AU5 narrowed. Audit escalation = the entry lines (D:825 item 2) plus the notice step as D11 adopts it, with the cap key at its default of 0 until the owner rules. No gate. Warnings never reach the person. This does not build a new channel.

### Part 2: N6, release and tag only with a recorded OK

**What D:763 says.** Tagging or publishing passes `refuse` only with an `answer_ref` that `answer-check` accepted. D:763 itself says words typed into the issue cannot be told from the orchestrator's text (U57), and D:769 says `refuse` sees only commands that verbs run.

**Is N6 contrary to D06?** Not by itself. D06 item 1 requires a person's typed go before an outward action; N6's recorded OK is a typed go. The real grounds for refusing are different: tags and package uploads are not recoverable the way a merge is (the squash merge of release 6.1.0 was reverted by #662, D:118), and the check is the one D06 item 9 says cannot tell a person from a script.

**Strongest case for CLAY.** Letting a person say "cut it" in chat is a capability. But I found no evidence of demand, release flows exist outside the coordinator, and the guard is the weakest one in the design (D:769). No clear benefit; lower risk and lower cost for the refusal, so OURS.

**Final (part 2): agree.** N6 becomes an unconditional refusal with no `answer_ref` branch in `limits.py`. A test scans the skill and refs for `git tag`, `git push origin <tag>`, `gh release create` and package uploads outside "Will Not Do" and the denylist file (D:769's own remedy). Merging a release PR stays an ordinary merge with a go (D06 item 1). Owner decision: confirm that the coordinator never tags or publishes; default yes.

---

# Final list for the unified spec

Genuine open owner decisions from this round (the rest are decided by the weighting rule and need only a note):

1. G-2: default value of `plan_depth` (`quick`, `standard` or `deep`).
2. G-3: re-plan the body and re-apply the approval before round 2 (default), or leave the body alone.
3. G-4: naming rule scope A, B (default) or C.
4. G-9: confirm the coordinator never tags or publishes; confirm the notice step for audit escalations.
5. G-6: closed unless the owner asks for the interrupt.

Decided here, no owner decision needed now: G-1 defer, G-5 reject approving prompts, G-7 off, G-8 reject.

## What I could not verify

- The coordinator spec rows FR-8, FR-10, FR-23, FR-24, Q12, C25 to C29 (IronFlow).
- `refs/claim.md` Wave 2 text itself (only as quoted in the design).
- Whether Orca `--agent claude` workers run with the permission bypass.
- Whether the design has a stale-lease or interrupt-suppression rule outside the lines I read.
- The exact number of test rows that need the D01 approval setup step.
- D:300-420 (so the completeness of the amendment list is not certified).
- Whether round-2 closeout done-checks behave well when the body keeps the original full criteria (option (b) in G-3).
