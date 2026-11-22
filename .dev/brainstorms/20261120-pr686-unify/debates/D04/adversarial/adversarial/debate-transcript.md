# Adversarial Debate Transcript (D04 claim level and grants)

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 (invariant probe, see invariant-probe.md); Round 3 not run (depth standard)
- Convergence achieved: 78.9% (15 of 19 points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant A = OURS, Variant B = CLAY)
- Taxonomy coverage (AD-5): L1 = S-001, S-002 debated; L2 = 12 points debated; L3 = C-003, C-008, X-002, X-004 debated; no forced round needed
- Note: Round 2 of A was run by a fresh advocate agent; an earlier SendMessage resume of the Round 1 A agent was not awaited (its output, if any, was not used)

## Round 1: Advocate Statements

### Variant A Advocate (OURS)
**Position**: The Pipeline field should pick the launch level, with one grant row per issue. R23 and R25 (requirements.md lines 47 and 51, 2026-11-18 and 2026-11-19) set that per-issue choice, and merge and close should never be granted in bulk. CLAY shows no evidenced benefit for forcing none-only that cannot be adopted separately (chat-recorded approvals, the closed command list).

**Steelman of Variant B**: The claim is one fixed, tested command (`PROMPT_PATTERN = ^/sc:issue --claim N --pipeline none$`, launch.py:33), approved by the owner in Q35 (owner-answers line 184). Every issue runs through one supervised `worker-start` worker with mailbox, heartbeat and audit trail (D:1104). The standing `grants` list removes a person from low-stakes steps (D:116) and is enforced by code: `E-NO-GRANT`, a closed `refuse(argv)` list, and `answer-check`, which refuses relayed, stale or unknown-source answers (D:688, D:1117). That last piece fits the owner's chat-only approval rule better than a hand-written grant row (owner-answers line 130 against memory `approvals-through-chat-never-files`).

**Key strengths claimed**:
1. The levels come from the owner's later decisions: R23 and R25 (requirements.md lines 47, 51); R25: "the cron watcher instructs the coordinator to launch the Pipeline levels Worktree, Full and Full Submit, not only None."
2. The brake is built and merged: the guard keeps the level outside the worktree and fails closed (`W-ENFORCEMENT-ABSENT`); B's own DQ7 (D:117) says its workers run "with no L1 guard and no L2 pre-push hook."
3. Grant rows are narrow and per issue: Decision 8 (owner-answers line 130); old contract line 300 lists posting an issue write without that issue's grant row as a "Never".
4. The safe state is the current state: `GOVERNED_LEVELS_ALLOWED = False` (R33, line 59), so only None launches today and OURS gives up nothing at the claim step now.
5. R24 already puts level-None work on the mailbox through `worker_done`, so OURS already has B's supervised route at None.

**Weaknesses identified in Variant B**:
1. C-001, X-001 (L2): Q35 is dated 2026-11-14; R23 and R25 are later and call the fixed none prompt "today", to be changed. B cites the superseded answer as current, and Q35 itself says the prompt change "waits on the first live test."
2. C-006, C-007 (L2): the standing list holds `pr.merge` and `issue.close` for every routed issue (D:116); the old contract allows outward action only when the person names it and pushes only on the person's go (lines 239-246). B's own ADD1 (D:135) admits the contradiction and says PR B must rewrite the contract.
3. C-008 (L3): the list that bounds the grants sits in a file the orchestrator edits: D:688 "ours are inside it and are guarded by the verb and by a test." A rule, not a permission boundary. `answer-check` is valuable but separable.
4. C-003, C-005 (L3): no per-issue stop between assignment and merge except `hold:backlog` (D:445). UNVERIFIED that no other brake exists in D: only "Pipeline field" was searched.
5. C-010, A-003 (L2): the "recorded word" is Clay's (D:688); B names no login for "the owner".
6. X-004 (L3): D:117 says "accepted for the first test issue only", yet the standing list has no such scope.

**Positions on X-001..X-004**: X-001: A holds, R23/R25 supersede Q35; B's code match is only because the gate is closed. X-002: conceded wording; "the control that exists today" overstates it, the accurate claim is "the only control that is built". X-003: qualified; Q36 (line 185) is approval latency, not the grant row (Decision 8, line 130); A's cost bullet blended the two. X-004: B's side holds.

**Shared assumptions**: A-001 QUALIFY (assignment is consent for the claim's own writes, not for a level above None; R25 needs Pipeline plus `Approved` for a Full Submit push; the signal is D01's question). A-002 QUALIFY (a person-opened coordinator can be trusted for low-stakes writes unattended, not for merge or close without a named go). A-003 QUALIFY ("the owner" must be one pinned identity under both designs; a per-issue row limits the damage of a wrong identity to one issue, a standing list limits nothing).

**Concessions**: A1: S-001 and S-002 are cosmetic; adopts "launch level" and "grant row" as B uses them. A2: the Status x Pipeline matrix (R32 P-8, R33, R34) is real design surface and removing Project reads is a real simplification (U-006); the cost only lands when the gate opens. A3: the per-issue row is slow and sits badly with chat-only approvals; B's `answer-check` (U-003) and `refuse(argv)` (U-004) are clear, separable benefits; proposes a hybrid: record each grant row from the owner's chat through an `answer-check`-style verb and keep a closed command list. A4: low-stakes standing grants (assign, comment, plan sections, hold) have an evidenced benefit (D:116) and are separable from `pr.merge` and `issue.close`, which stay per issue. A5: until issue 442 closes, OURS behaves like CLAY at the claim step (X-002).

### Variant B Advocate (CLAY)
**Position**: Variant B holds on claim level. The owner's own Q35 and the code on master both say the watcher claims at `--pipeline none`; the Pipeline-level route is gated closed and delivers nothing live. B also brings separable controls OURS lacks: `answer-check`, `refuse(argv)` and mailbox supervision. B's weakest point (X-004) is verified and conceded.

**Steelman of Variant A**: A gives the person who knows the issue a per-issue throttle on the board where the owner already works. R25 widened the levels on 2026-11-19, later than Q35 (2026-11-14). The level is enforced by a guard the agent cannot edit and fails closed (`W-ENFORCEMENT-ABSENT`). Grants are narrow and listed; merge and close are never bulk-granted, and `WORKER-CONTRACT.md:239-246` (read at `01e7a9e23^`) says the coordinator acts outward only on a named instruction. The gate is closed, so the safe state is also the current state. B's no-guard cost (DQ7, D:117) is real.

**Key strengths claimed**:
1. Q35 "B1b" (owner-answers.md:184): "the watcher claims with `--pipeline none`; the coordinator runs the existing worktree step and starts the worker". D:81 (R9) matches it.
2. The levels deliver nothing live: R33 closes the gate (requirements.md:59); A's own cost list concedes "OURS behaves exactly like CLAY at the claim step" today; governed levels need 12 skipped observations and issue 442 to clear; the guard does not see a `worker-start` worker (D:117).
3. One supervised route: R24 (requirements.md:50) puts a launched agent at Worktree, Full or Full Submit on `result.md` only; the `worker-start` route has a mailbox with one handling per message id, check-ins and restart (D:1104).
4. A grant mechanism OURS lacks (L3, C-008): `answer-check` refuses relayed, wrong-entry, stale or unknown-source answers (D:688); `E-NO-GRANT` refuses and logs every write outside the list (D:696); a closed list and `refuse(argv)` carry one test per pattern (D:1117).
5. A per-issue row fits an unattended watcher badly (L2): R1 says no person sets or approves anything for work to start (D:73); Decision 8 says the row is "written by the owner, not by an agent" (owner-answers.md:130); D:116 says the old row "came from the approval flow that this issue retires"; under the chat-only rule an agent records approvals, so the row has the same self-edit gap OURS attributes to B.
6. Smaller surface: no Status x Pipeline matrix (R23, R32 P-8, R33, R34) and no Project read (D:256).

**Weaknesses identified in Variant A**:
1. C-008 (L3): the claim that a per-issue row has no gap: the row is a record an agent writes from chat, and Decision 8 forbids that; OURS has neither a refusing verb nor `answer-check`. D:688 is a guard A treats as weak, yet stronger than A's.
2. X-002 (L3): internal contradiction: fact 3 calls the guarded level choice "the control that exists today", while A's own first cost bullet says no governed level can run today.
3. X-001 (L2): A cites R23 and R25 but never mentions Q35. R25 is later, but R33 gated it closed on the same day.
4. C-005 (L2): the gate is closed, so the Pipeline throttle is not operative; A lists "dead weight" among its own risks.
5. X-003 (L2): A's cost bullet misreads Q36; line 185 is plan-approval latency, not the grant row (line 130). B's fact 5 does the same; that fact is withdrawn.

**Positions on X-001..X-004**: X-001: B (Q35 plus launch.py:33 and issue.md:48; R25 postdates Q35 but is gated closed). X-002: B (verified defect in A). X-003: neither side is right; B's fact 5 is withdrawn; Decision 8 is a separate owner decision that D:116 retires. X-004: A is right (see concessions).

**Shared assumptions**: A-001 ACCEPT (assignment is the consent for the claim writes, R1, D:73; the level choice needs no further per-issue input if the claim is none-only). A-002 QUALIFY (the orchestrator is script-startable only after PR B rewrites the contract, ADD1, D:135; R25 also needs a trusted unattended actor, because the cron watcher instructs the coordinator). A-003 REJECT as stated ("the owner" is not one known login; owner-answers.md:162: `ironbelly` is "the one login shared by the owner and every session on this host, so who merged is NOT established"; `answer-check` verifies the source of an answer rather than a login).

**Concessions**: X-004 is a verified defect in B: Q38 (owner-answers.md:187) "G2 is not built; only the one G1 test issue can run... any further issue waits for G2"; Q34 (line 147): the G1 acceptance "does not extend to any later issue"; D:117 adopts the no-guard route for all issues. C-007 is a real reversal of `WORKER-CONTRACT.md:239-246` (ADD1 says PR B rewrites it). C-003 is a verified cost: no L1 guard or L2 hook, `master` unprotected (D:117, K12). C-010: "Clay's recorded word" is a naming gap (D:688). Hybrid proposed: adopt B's none-only claim and standing-list machinery (`answer-check`, `refuse(argv)`, mailbox); keep the Pipeline field as a later per-issue brake that reads "stop after claim", and keep the guard; do not ship `pr.merge` or `issue.close` as standing grants until the owner rules on the contract rewrite and the G2 acceptance.

(Orchestrator check: Q34 line 147, owner-answers line 162 and Q38 line 187 were re-read and match the quoted text.)

## Round 2: Rebuttals

### Variant A Rebuttal (OURS)
**Responses to B**:
1. C-008: concedes the narrow point. A per-issue row an agent writes from chat, with no refusing verb, is weaker than `E-NO-GRANT` + `answer-check` (D:688, D:696). But those controls do not depend on the list being standing: a list entry scoped by issue number gets the same `--answer-ref` check and refusal. C-008 supports adopting the controls, not choosing standing over per-issue. D:696 also says assignment and claim comments are written by `/sc:issue` itself, "which these verbs do not see", so `E-NO-GRANT` does not cover two of the six entries.
2. X-002: conceded. The accurate wording is "the only control that is built".
3. X-001: accepts none-only is the correct live rule today; does not accept R25 is dead. R9 (D:81) is dated 2026-11-18, one day before R25 (2026-11-19). R33 (requirements.md:59) closes the gate "until a reviewed commit flips it": sequencing, not revocation. Q35 (owner-answers:184) is conditional: "waits on the first live test".
4. C-005: conceded for now; whether the spec should say so is open question (a).
5. X-003: both misread Q36 (owner-answers:185 is approval latency, not Decision 8 at :130). Settled.

**Still disagree**:
- R9 and D:1102 are written as permanent, so they conflict with R25. B's hybrid keeps Pipeline only as a later "stop after claim" brake; that can only narrow, while R25 (requirements.md:51) widens: "launch the Pipeline levels Worktree, Full and Full Submit, not only None."
- B's "no Project read" (D:256) also drops Status. D:256: "no board column and no Project is read anywhere". R23 (requirements.md:47) says Status picks the command: a lost owner decision, not just a smaller surface (may belong to topic D01).
- Standing `pr.merge` and `issue.close`: see (c).

**Answers to open questions**:
(a) The spec should say "not used while `GOVERNED_LEVELS_ALLOWED` is False". D:81 says the claim's launch levels "are never used"; D:1102 says "a test fails if the skill launches through `orca_worktree.py launch` or passes `--pipeline worktree` or `full`"; D:117 repeats the launch test. When the owner opens the gate under R25 all three fail by design, so R25 would need a spec amendment, a test rewrite and an owner re-ruling. A test keyed to the gate constant gives the same protection today and does not undo R25 later.
(b) Concedes part: reading Pipeline now delivers nothing (R33) and R36 shows value reads have a cost. Read it only when the gate opens; the spec should name the gate-open design (Pipeline picks the level) so it is not lost.
(c) Safe as standing: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold` (bounded, reversible, about the issue's own text; R24 already makes the result comment a coordinator write). Not safe by default: `pr.merge`, `issue.close`: contract line 241 (outward action needs an instruction naming the action), line 245 (pushes need the person's go; "no earlier pre-authorization waives this"), line 300 (issue write without that issue's grant row is a "Never"); D:135 (ADD1) admits R10 contradicts lines 239-246. B's fair counter: R10 is a ruling that the orchestrator merges and closes; A cannot verify R10 supersedes Q38 (owner-answers:187, "any further issue waits for G2"). D:117 (master unprotected, no L1/L2) argues for per-issue conditions on merge and close until the owner confirms.
(d) A chat-recorded go is enough; a file-form row written by the owner is not needed. Decision 8's "written by the owner" (owner-answers:130, 2026-11-14) is superseded in form by the 2026-11-17 rule. Trust then comes from a verb that refuses writes without an accepted `--answer-ref` (B's `answer-check`). For governed levels the per-issue consent is the board itself: Pipeline plus `Approved` (R25, R35); the script can derive the row from those fields so nobody writes a file.

**Final position**: live rule with the gate closed: claim at `--pipeline none` only. Spec text and tests keyed to the gate so opening it reactivates R25 without a rewrite; Pipeline picks the level when the gate opens. Adopt B's `answer-check`, `refuse(argv)`, `E-NO-GRANT` and mailbox supervision. Four standing grants. `pr.merge` and `issue.close` stay per issue, or standing only after the owner confirms R10 against ADD1 and G2.

**Resolved**: S-001, S-002, X-002, X-003, X-004 (B's side), C-004 (live behaviour none-only), C-010 (naming gap), U-003 to U-005 adopted.
**Unresolved**: C-001 and C-005 (gate-keyed wording plus Status dropped from reads), C-007 (R10 vs contract lines 239-246), C-008 (resolved in direction, needs wording), C-009 (whether reads are deferred), X-001 (live rule agreed, R9 permanence open), A-001 and A-002 (to D01 and D06), A-003 (shared and open).

### Variant B Rebuttal (CLAY)
**Responses to A**:
- Accepts: Pipeline read only when the gate opens (R33; the spec should name the gate-open design); four low-stakes standing grants (caveat in (iii)); a chat-recorded go plus `answer-check` is enough, no per-issue file row; Q35 is conditional (line 184 "waits on the first live test and a running coordinator"); withdraws R9 as owner authority (it matches Q35 in content, but R9 is Clay's ruling).
- Concedes `pr.merge` and `issue.close` should not ship as standing grants until `ironbelly` rules on the contract rewrite and G2.

**Still contests**:
1. "Keyed to the gate constant": the orchestrator test has a reason independent of #442. K4 (D:1226): "The claim's launch levels and `worker-start` could be mixed ... `worker-start` only; a test fails if the skill launches through `orca_worktree.py launch`". A gate-keyed test would repeat what `/sc:issue` already enforces and say nothing about the orchestrator's own route.
2. A per-issue grant row for merge and close: existing machinery gives the per-issue condition without a row. A merge question key `merge_safety:<PR>:<head sha>` (D:598) is accepted by `answer-check` and tied to one PR and head; the go stays in chat.
3. "Pipeline picks the level" as the gate-open design: waves 5 to 8 end on `worker_done` for the active Task and Dispatch (D:575); a launched agent reports only through `result.md` (R24). Level-picking would need a second watch path, a new decision rather than a flag flip.

**Answers to (i)-(iv)**:
(i) R9 and R10 are Clay's rulings, not `ironbelly`'s: D:71 heads the table "Ruling (Clay, 2026-11-18)", D:688 says "Clay's recorded word", FULL-REPORT section 4 says the design is "approved by the owner (Clay)" and every ruling read was posted under `clayphi`; section 1 point 6: "the owner" means Clay in #655 and the design and `ironbelly` in the decision records. C-007 gains weight for A: standing merge and close rest on a maintainer's ruling that contradicts the owner-recorded contract (D:135, lines 239-246) and Q38. B's X-001 loses weight for the same reason.
(ii) Partly yes: K4 (D:1226) is a one-route reason, not the #442 gate; DQ9 and wave 5 (D:572-576) make mailbox ids, check-ins and restart replay load-bearing. Concedes that DQ7 (D:117) puts the test next to the gate argument and that the mailbox link is an inference.
(iii) A is right. D:696 says `E-NO-GRANT` covers writes "through its own verbs"; assignment and claim comments come from `/sc:issue`, "which these verbs do not see". `issue.close` is written by `/sc:closeout` (D:605); the only claim it falls under the grant is D:799, stated without a mechanism. Enforcement is evidenced for `issue.hold` and `issue.body.append_plan_sections` (D:300, D:1100); none found for `pr.merge`, which D:588 runs as a raw `gh pr merge`. So `E-NO-GRANT` backs at most 2 of the 6 entries. Related defect: `answer-check` hardwires its source to Clay's own terminal input or Clay's ClickUp id (D:694), so it needs a parameter for the owner identity.
(iv) More brakes than `hold:backlog` exist, none a per-issue stop after claim. Per repo: `enabled` (D:278, D:302), `max_in_flight` (D:289). Per PR: `changes_requested`, `merge_safety` (needs an OK), failing-check OK, `review_stalled`, escalation rows 1 to 7. `hold:plan` is poll-written and reflects only a missing plan. A's "Pipeline is the only brake" is wrong, and B's "any assigned issue to merge and close" is overstated.

**Final position**: claim at `--pipeline none` now, no Project read. Adopt `answer-check` (owner identity parameterised), `refuse(argv)` and mailbox supervision. Four standing grants. `pr.merge` and `issue.close` not standing: each released by an `answer-check`-accepted go keyed to the PR until `ironbelly` confirms R10 and G2. Spec wording: "the orchestrator launches only through `worker-start`; level-picking by Pipeline is a future decision gated on #442" (drops "never used", drops "keyed to the gate").

**Resolved**: S-001, S-002, X-002, X-003, X-004, C-004, C-005 (brakes mapped), C-010, C-008 (adopt the controls, scope the weak entries), C-009 (Pipeline read deferred), U-003 to U-005, A-003 (R9, R10, DQ7 are Clay's).
**Unresolved**: C-001/X-001 (whether R9's "never" yields to R23/R25; owner call, probably D01), C-007 (whether `ironbelly` ratifies R10 and G2), C-002 (whether a second launch route is ever wanted), A-001 and A-002 (consent signal and trusted unattended actor; D01, D06).

(Orchestrator check: D:575, D:588, D:598, D:694, D:696, D:1226 and D:71 re-read in the master snapshot and match.)

## Round 2.5: Invariant Probe (summary)

Full table in `invariant-probe.md`. 12 findings: 9 UNADDRESSED (5 HIGH: INV-001 gate constant not on master, INV-002 grants file editable by the orchestrator, INV-003 worker-start worker unbound by any guard, INV-004 merge go not tied to a gate reason, INV-012 sufficiency challenge: shared `ironbelly` login, unprotected master, contract not rewritten; 4 MEDIUM). The probe changes spec conditions, not the winner.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Neither (cosmetic) | 90% | Both advocates: presentation only |
| S-002 | Neither (cosmetic) | 90% | A adopts B's terms; no substance |
| C-001 | Hybrid: B live rule, A gate-open design | 65% | Both: none-only now (R33, launch.py:33); A: R25 must not be erased by "never used" (D:81, D:1102); B: level-picking is a new decision gated on #442 (D:575, R24) |
| C-002 | B for the live route | 75% | worker-start + mailbox is the only route that runs (D:1104, K4 D:1226); whether a second route is ever wanted is open |
| C-003 | A | 85% | B concedes no L1/L2, unprotected master (D:117, K12); owner accepted the no-guard route for one test issue only (Q34, Q38) |
| C-004 | B | 90% | Both: live behaviour is none-only (A cost 1, R33) |
| C-005 | A (partly) | 65% | No per-issue stop after claim exists in B; B corrected A: other brakes exist (`enabled`, `max_in_flight`, gate reasons, D:278, D:289, D:582) |
| C-006 | Hybrid | 85% | Four standing grants, two per action; both advocates converge (D:116, contract lines 241, 245, 300) |
| C-007 | A | 85% | Standing merge and close rest on Clay's ruling R10 against contract lines 239-246 and Q38; B concedes |
| C-008 | B (controls), A (scope) | 75% | `answer-check`, `E-NO-GRANT`, `refuse(argv)` adopted; `E-NO-GRANT` covers at most 2 of 6 entries (D:696); owner identity must be a parameter (D:694) |
| C-009 | B | 80% | Pipeline read deferred until the gate opens; Status/Project reads are a D01 question |
| C-010 | A | 75% | "Clay's recorded word" (D:688) is a naming and authority gap; B concedes |
| X-001 | Split | 55% | Q35 supports none live; R25 later; R9/R10 are Clay's rulings (D:71), not the repository owner's |
| X-002 | B | 95% | A conceded: "the only control that is built" |
| X-003 | Neither | 95% | Both misread Q36 (owner-answers 185 is approval latency; Decision 8 is line 130) |
| X-004 | A | 90% | B conceded: Q34 and Q38 limit the no-guard acceptance to one test issue |
| A-001 | Unresolved | 50% | A: QUALIFY; B: ACCEPT; to topic D01 |
| A-002 | Tie (both QUALIFY) | 80% | Low-stakes unattended yes; merge and close need a named go |
| A-003 | Open for both | 85% | `ironbelly` is a shared login (owner-answers 162); `answer-check` needs an owner-identity parameter |

## Convergence Assessment
- Points resolved: 15 of 19
- Alignment: 78.9%
- Threshold: 80%
- Status: NOT_CONVERGED (also BLOCKED_BY_INVARIANTS: 5 HIGH UNADDRESSED, see invariant-probe.md)
- Unresolved points: C-001, C-002, X-001, A-001
- Handling: depth standard has no Round 3. Per the error-handling matrix: force-select by score, document non-convergence, flag for review, status partial. The four unresolved points depend on the repository owner (R9/R25 permanence, consent signal) or on other debate topics (D01, D06).
