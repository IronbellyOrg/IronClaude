# Section 05 analysis: Claiming and starting workers (with the plan before the claim)
Counts: COVERED 18, CONFLICT 4, NOT-COVERED 8 (30 features; the NOT-COVERED rows are S05-F18 to F23, F25, F26)

Scope: 655 body lines 73-83 (section 5), plus the Acceptance Criteria items that touch it (body lines 218 and 219). Paths used below: SPEC = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md; DEC = .../20261120-pr686-unify/DECISIONS.md; VERD(x) = .../20261120-pr686-unify/debates/x/VERDICT.md.

### S05-F1 Reuse the existing claim workflow, no second one
- 655 says: the orchestrator runs the existing `/sc:issue --claim` workflow (`refs/claim.md`); that workflow assigns, checks accuracy, writes summary and next steps through `/sc:recommend`, and posts the accuracy-check and "Claimed by" comments (body line 75).
- Status: COVERED
- Current plan: D12 item 3 "Claim keeps its chain" (VERD(D12):19); FR-51 keeps `/sc:issue --claim` flag meanings (SPEC:272); SPEC section 3.1 says the claim is a session started by the poll as master already does (SPEC:125, row 4 at SPEC:174), then the coordinator adopts it (FR-29, SPEC:231). Same claim skill, different starter: 655 has the orchestrator run the claim, the plan has a poll-launched claim session. Same effect, so COVERED.
- Depends on: 655 section 1 (who is woken and when)
- Evidence from our documents: no conflict found
- Concerns: the actor differs (see above). A builder must follow the plan: the coordinator adopts a finished claim and does not run the claim itself on the normal path. `--take <owner/repo#N>` (FR-24, SPEC:226) is the hand-over route. UNVERIFIED whether the coordinator may also run the claim itself; D04 item 1 only says "Whatever starts a claim passes exactly `--pipeline none`" (DEC:238).

### S05-F2 Claim at `--pipeline none`, never through the claim's launch levels
- 655 says: "Decided by Clay": claim at `--pipeline none`; the worker is never started through the claim's `worktree` or `full` levels (body line 75; criteria line 218).
- Status: COVERED
- Current plan: FR-51 "Pass exactly `--pipeline none` for every watcher or coordinator claim" (SPEC:272); FR-52 Pipeline field not read while `GOVERNED_LEVELS_ALLOWED` is false (SPEC:273); D04 (SPEC:80).
- Depends on: none
- Evidence from our documents: no conflict found
- Concerns: none

### S05-F3 Coordinator starts the worker itself with `orca orchestration worker-start` (supervised, reports through the Run mailbox)
- 655 says: after the claim the orchestrator starts the worker with `worker-start`, so the worker is supervised and reports through the Run mailbox (body line 75).
- Status: COVERED
- Current plan: D04 item 2 "One supervised route: `worker-start` with mailbox" (VERD(D04):35, winner line 40); DEC:238 "After the claim, one supervised worker is started with `orca orchestration worker-start`"; FR-30 start every worker bound to the guard (SPEC:232); FR-29 adoption record before start (SPEC:231).
- Depends on: S05-F6 (guard)
- Evidence from our documents: no conflict found
- Concerns: the plan adds a guard binding step (FR-30) that 655 does not have; `WORKER_BINDING_PROVEN` is false, so a start outside the per-repo `probe_issues` is refused until a live probe passes (SPEC:232).

### S05-F4 Each issue claimed once and its worker started once
- 655 says: "each issue is claimed once and its worker started once" (criteria line 218).
- Status: COVERED
- Current plan: FR-03 keeps `marker_in_window` so a hand claim and a watcher start never run two workers (SPEC:193); FR-29 exclusive-create adoption record (SPEC:231); FR-21 one store save before publish, an unknown launch receipt never relaunches (SPEC:211).
- Depends on: none
- Evidence from our documents: no conflict found
- Concerns: none

### S05-F5 Worker starts in a worktree of the issue's own repo
- 655 says: `worker-start` in a worktree of the issue's own repo (criteria line 218).
- Status: COVERED
- Current plan: D07 "Project-local coordinators, one dispatcher, per-repo config" (SPEC:83); FR-29 reads `launch_cwd` and copies `.dev/issues/<N>/` into the worker worktree (SPEC:231).
- Depends on: 655 section 1 item 6 (repo list and checkout map)
- Evidence from our documents: no conflict found
- Concerns: the plan has no `IronOrchestrator` repo or repo-to-checkout map (D15 C5 rejected it, VERD(D15):77; no-checkout becomes a skip reason, C7 at :79). That is another section's feature, noted only.

### S05-F6 Does a `worker-start` worker fall under the #442 ship gate (open question in 655, "spec 2.1")
- 655 says: left open: whether a worker started this way falls under the #442 gate (body line 75).
- Status: COVERED
- Current plan: D05 "The guard is required for every worker the orchestrator starts, staged and not exempted" (VERD(D05):19); FR-30 (SPEC:232); FR-52 (SPEC:273). The plan answers the question: yes, bound, behind a live probe that closes issue 442's pending rows (VERD(D05):60).
- Depends on: none
- Evidence from our documents: VERD(D05):34 "Binding a `worker-start` worker has never been observed" (UNVERIFIED item).
- Concerns: binding of `worker-start` workers is unobserved (VERD(D05):82, "FU-1 precondition f, never tried"); the guard mitigates but does not close the unprotected-master risk (VERD(D05):22).

### S05-F7 Delivery to a launched agent by `orca orchestration send --to <terminal handle>` (2026-11-18 test, not re-run)
- 655 says: a test of 2026-11-18 showed `send --to <terminal handle>` reaching an agent launched with `orca worktree create --agent`, readable with `check --terminal` (body line 75); marked "not re-run here".
- Status: COVERED
- Current plan: FR-14 mailbox and typed line are id-only nudges, typing only into an idle or just-started session (SPEC:204); FR-40 typing rules for worker terminals (SPEC:242). The plan's live checks U5 and U25 still have to pass (SPEC:204).
- Depends on: none
- Evidence from our documents: VERD(D03):16 keeps the worker-contract bullet "ask and send carry no `--to`"; that bullet is about the bound worker's own messages, so UNVERIFIED whether it also limits a coordinator's `--to` send. SPEC:760 says that bullet is not on master after PR 700 (PR 701 re-adds it).
- Concerns: 655's own test is untested in our plan too (live check U5 pending).

### S05-F8 A plan must exist before an issue is claimed
- 655 says: "A plan must exist before an issue is claimed" (body line 77; criteria line 219).
- Status: COVERED
- Current plan: FR-01 start only with the plan check passing (SPEC:191); FR-04 "Require the plan before the approval" (SPEC:194); FR-05 skip as `held_incomplete` (SPEC:195); D01 (VERD(D01):16).
- Depends on: none
- Evidence from our documents: no conflict found
- Concerns: in the plan the gate order is plan, then person approval (field `Approved`), then claim (SPEC:125). 655 has no approval step. That is a section-1 conflict (trigger), not classified here.

### S05-F9 All plan creation goes through `/sc:issue` (rulings 23, 30, 31)
- 655 says: every plan is created through `/sc:issue --plan`, never by another path (body line 77).
- Status: COVERED
- Current plan: FR-53 adapt and merge PR 690 (`--plan`) (SPEC:274); FR-56 a manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>` (SPEC:277); VERD(D12):21 item 5; D09 item 5 names the plan body write as `/sc:issue --plan` under grant `issue.body.append_plan_sections` (VERD(D09):21).
- Depends on: S05-F27
- Evidence from our documents: no conflict found
- Concerns: a person may still fill the sections by hand; the plan does not forbid that.

### S05-F10 The check (`plan_check`): three headings once each, non-empty, not only "Not known yet"
- 655 says: a script checks `## Priority`, `## Fix approach`, `## Test plan`, each once, non-empty, not only "Not known yet" (body line 79; line 25).
- Status: COVERED
- Current plan: FR-54 one plan check, `plan_body.py check` is the reference: headings in fences or comments do not count; absent, repeated, empty or placeholder-only sections fail (incl. `<...>`, TBD, "Not known yet") (SPEC:275); FR-05 (SPEC:195); FR-53 fence-aware count (SPEC:274). The plan adds a package copy with a parity test.
- Depends on: none
- Evidence from our documents: no conflict found
- Concerns: the check proves presence, not quality (FR-54, SPEC:275).

### S05-F11 The poll applies the check to the search row's body, so a decision costs no call
- 655 says: the poll applies `plan_check` to the search row body; no extra call (body line 79).
- Status: COVERED
- Current plan: FR-05 "read-only plan check on the body (memory only) before the approval read" (SPEC:195); DEC:386 "on the body it already fetches" (D09 verdict item 1); body kept out of the audit log (DEC:391).
- Depends on: none
- Evidence from our documents: no conflict found
- Concerns: none

### S05-F12 Label `hold:plan` written by the poll, under the grant `issue.hold`
- 655 says: `hold:plan` is written only by the poll, under the grant `issue.hold`; a failing issue gets the label (body lines 25 and 79; criteria line 219).
- Status: CONFLICT
- Current plan: REJECTED by Q03, D09, D15 A5. FR-06 "Write nothing to GitHub in a poll cycle (NG-2): strip the label writer of PR 686" (SPEC:196); FR-07 "ignore a leftover `hold:plan`; drop the `issue.hold` and `pr.merge` grants from reference config and fixtures" (SPEC:197); FR-82 (SPEC:218); Q03 (SPEC:95; DEC:709-716). The plan replaces the label with a local `holds` entry and a read-only skip `held_incomplete`.
- Depends on: none
- Evidence from our documents: DEC:716 "A `hold:plan` label on an issue is ignored, with no warning." VERD(D15):45 "Reject now (replace by a read-only variant); label write deferred to its own later PR". DEC:401 "UNVERIFIED: whether anyone reads `hold:plan`".
- Concerns: the plan keeps one door open: the label write may return only with a shown reader, an NG-2 amendment, a 24-hour shadow run and a cron write test (SPEC:443; DEC:388). Until then 655's version is rejected. Owner rule NG-2 (poll writes nothing to GitHub) is the reason.

### S05-F13 The hold lifts when the plan passes the check; the issue stays unclaimed until then
- 655 says: the issue stays held and unclaimed; the poll lifts the hold (removes the label) once the plan passes the check (body lines 25 and 80).
- Status: COVERED (effect only; the label removal is the rejected part of S05-F12)
- Current plan: FR-05 runs the check every cycle on the fresh body (SPEC:195); FR-08 re-check at wake time (SPEC:198); a leftover `hold:plan` is ignored (FR-07, SPEC:197). A passing plan therefore releases the issue with no label write.
- Depends on: S05-F10, S05-F12
- Evidence from our documents: no conflict found
- Concerns: none

### S05-F14 A hold is a label only, never a comment
- 655 says: `hold:plan` is "a label only, never a comment" (body line 25).
- Status: COVERED
- Current plan: D09 item 2 "The poll never creates a label and never comments about a hold" (DEC:387); FR-06 (SPEC:196).
- Depends on: none
- Evidence from our documents: no conflict found
- Concerns: none

### S05-F15 `hold:backlog`: placed and removed only by a person; the system does nothing with the issue while it is on
- 655 says: `hold:backlog` is placed and removed only by a person; the system does nothing until it is removed (body lines 25 and 79).
- Status: COVERED
- Current plan: FR-01 "no `hold:backlog`" (SPEC:191); FR-05 skip `hold:backlog` as `held_backlog` (SPEC:195); FR-82 "`hold:backlog` stays by hand" (SPEC:218); D09 item 2 (DEC:387); D15 A3 (VERD(D15):43).
- Depends on: none
- Evidence from our documents: DEC:1410 (X-18): per-repo init does not create `hold:backlog`; it stays by hand until the owner asks.
- Concerns: 655 expects the label to exist; in the plan the repo init does not create it, so a repo may lack it until a person makes it (DEC:1138).

### S05-F16 A hold removed by hand stays removed (never put back)
- 655 says: "A hold removed by hand stays removed" (body lines 25 and 79; criteria line 219).
- Status: CONFLICT (the rule only exists to serve the label writer, which the plan strips)
- Current plan: FR-06 strips the label writer including the `hand_removed` state (SPEC:196); D15 A5 removes `hand_removed` and the reason `hold_removed_by_hand` (VERD(D15):45). With no `hold:plan` write there is nothing to put back; for `hold:backlog` the rule holds trivially because only a person writes it.
- Depends on: S05-F12
- Evidence from our documents: VERD(D15):45 "the `hand_removed` state ... Strip"
- Concerns: none; if the label write ever returns (SPEC:443), this rule must come back with it.

### S05-F17 An edit of the issue after the claim by someone other than the user's own login does not stop the work
- 655 says: "an edit after the claim by someone other than the user's own login is one line in the report entry and nothing else" (body line 79); this is Clay's ruling 23 (AD-A3).
- Status: CONFLICT (partly)
- Current plan: D01 item 5 "any body edit after the approval voids it" (VERD(D01):16); FR-04 "document that a body edit after approval voids it" (SPEC:194); FR-01 "approved ... and unedited since" (SPEC:191); FR-35 re-plan voids approval (SPEC:237). In the plan, an edit after approval stops the start; 655 lets edits through.
- Depends on: none
- Evidence from our documents: VERD(D01):29 "decides deliberately that edits before and after the claim are fine, with a wave-1 live re-check and a report line for a later edit by someone else. This narrowed the owner's content-binding argument (C-006 from 85 to 65 percent)."
- Concerns: the verdict lowered but kept the owner's rule, so confidence is moderate (D01 is "78% (p)" at SPEC:77). What happens to an edit AFTER the worker has started is not stated in the plan documents I read (UNVERIFIED). The report-line part is S05-F18.

### S05-F18 One report-entry line for a later edit by someone else
- 655 says: such an edit is "one line in the report entry and nothing else" (body line 79; section 7 owns the report format).
- Status: NOT-COVERED
- Current plan: none found; searched: "edited since", "edit after", "body edit", "voids" in SPEC (only the approval-void rule, SPEC:125, 191, 194, 237), `report-entry` and `escalate` rows (FR-26 SPEC:228, FR-37 SPEC:239), FOLLOW-UPS.md (grep "plan|hold|claim"), STATE.md.
- Component: COORDINATOR (the coordinator writes work-report entry lines through `report-entry`, FR-26)
- Feature statement: When the coordinator sees the issue body edited by a login other than the owner's after a claim, it adds one line to that issue's work-report entry and does nothing else.
- Done when: a test edits a claimed issue as another login and the entry gains exactly one new line, with no escalation and no state change.
- Depends on: S05-F17; 655 section 7 (report entry); the plan's `report-entry` verb (FR-26) which is NOT BUILT
- Evidence from our documents: VERD(D01):29 (Clay's design has the report line); no evidence found that the plan rejects it.
- Concerns: report skill state is unclear after PR 700 removed `agent-work-report` (SPEC:771; FR-45, FR-46, FR-48 blocked until restored, SPEC:778). Needs the S05-F17 decision first. FR-80 limits which entry fields the observer shows (SPEC:263).

### S05-F19 After one quiet hour the poll sends ONE plan request for an unplanned issue
- 655 says: after one hour in which nothing changed, the poll sends ONE `plan_requests[]` item to the repo's orchestrator (body lines 25 and 80; criteria line 219).
- Status: NOT-COVERED (explicitly DEFERRED by the plan, nothing built)
- Current plan: none found that delivers it; D15 A4 "Defer ... Not built now; if built, ids only and after D07 settles who plans" (VERD(D15):44; SPEC:442). D09 item 5 calls the request "a wake-file item, not a GitHub write" (VERD(D09):21). D10 removes `plan_requests[]` from the wake file (VERD(D10):18, :42, :61). Searched: "plan request", "plan_requests", "one hour", "plan_stuck", "quiet" in SPEC, DECISIONS, FOLLOW-UPS, STATE and all verdicts.
- Component: WATCHER (the poll decides and writes the wake item; the wake transport is the watcher's)
- Feature statement: The poll sends one id-only plan-request item to the project's coordinator for an issue that has stayed without a plan for one quiet hour, never twice for the same quiet period.
- Done when: a test with a clock shows exactly one plan-request item after 60 quiet minutes, none at 59, none a second time, and the wake file holds only `repo`, `number`, `url`.
- Depends on: S05-F20, S05-F21, S05-F23; 655 section 4 (wake format)
- Evidence from our documents: VERD(D10):18 "The plan-request payload (`plan_requests[]`, with a title) belongs to the plan-hold decision (D09), not to this transport." VERD(D01):16 "the plan request is an agent edit of the issue body, and any body edit after the approval voids it".
- Concerns: (1) NG-2 is respected only if the request stays a wake item, not a GitHub write. (2) The wake carries ids only; 655's version carries the issue title, which D10 item 5 rejected (titles are free GitHub text). (3) A plan edit after the person's approval voids that approval (FR-04), so a plan request only makes sense before approval; 655 has no approval step, so the ordering needs a ruling. (4) Who plans (poll side or coordinator) was left to D07 and is not stated again in the spec: UNVERIFIED.

### S05-F20 The quiet clock: it moves on any change (a linked branch, pull request or session)
- 655 says: "the quiet clock moves on any change, a linked branch, pull request or session" (body line 80).
- Status: NOT-COVERED
- Current plan: none found; searched: "quiet", "linked branch", "idle clock", "plan request" in SPEC, DECISIONS, techref and inventory folders; the poll's change signals in the plan are `status --json` fields (NFR-04, SPEC:217) which hold no per-issue quiet time.
- Component: WATCHER (per-issue timing in the poll's store)
- Feature statement: The poll keeps one quiet-since time per unplanned issue and resets it when the issue, a linked branch, a pull request or a session on it changes.
- Done when: a test shows the clock resets on each of the four change kinds and a plan request fires only after 60 quiet minutes.
- Depends on: S05-F19
- Evidence from our documents: no evidence found in our documents
- Concerns: extra reads. The plan's poll makes one read-only search per repo (D09 item 6, DEC:391) and keeps `gh` calls low; checking linked branches, pull requests and sessions per issue may need more calls. UNVERIFIED call cost.

### S05-F21 A plan request takes one of the repo's three in-flight places; routing to a coordinator with a free place
- 655 says: the plan request goes to an orchestrator of the repo that has a free place and takes one of the three places; a new orchestrator is started only when the repo has none (body line 80; criteria line 216).
- Status: NOT-COVERED
- Current plan: FR-33 caps work in flight per coordinator id, counting "pending, launched, claimed, woken, acked, unknown entries and open claim files"; a plan request is not in that list (SPEC:235). FR-27 and FR-34 decide when a missing coordinator is started (SPEC:229, 236), and D15 C5 rejected "poll starting extra orchestrators" (VERD(D15):77). Searched: "max_in_flight", "plan request" in SPEC, DECISIONS and verdicts.
- Component: WATCHER (counting and routing sit in the child cycle, FR-33)
- Feature statement: An open plan request counts as one in-flight place for its repo and is routed only to the repo's coordinator when a place is free.
- Done when: a test with three issues in flight shows the plan request waits, and with two it is sent and the count becomes three.
- Depends on: S05-F19; 655 section 1 item 5 (one orchestrator per repo, max 3)
- Evidence from our documents: VERD(D15):77 (C5) "Registry repo ... one orchestrator per repo with ids, 30-minute idle end, `wrong_target`, poll starting extra orchestrators | Reject".
- Concerns: the "start a new orchestrator when none exists" half of 655 is NOT adopted: in the plan the coordinator is person-opened, or a script starts it only with a recorded owner authorization after live check U3 (FR-27, SPEC:229); a missing coordinator is the skip `coordinator_absent`. The plan also holds the first build at `max_in_flight` 1 (FR-33, SPEC:235).

### S05-F22 Plan record written first, acknowledgment second (a crash cannot lose the request)
- 655 says: the orchestrator writes `.orchestrator/issues/plan-<key>.<requested_at>.json` first and the acknowledgment second (body line 80; criteria line 219).
- Status: NOT-COVERED
- Current plan: none found for plan requests; the same ordering rule exists for claims: FR-15 and D10 M1 "Accept an ack only if the per-issue state file exists and matches" (SPEC:205), and FR-29 "save `issues/<repo-key>__<N>.json` by exclusive create ..., then ack" (SPEC:231). The file name `.orchestrator/issues/plan-<key>...` is not in the plan (state root is `<state_dir>`, SPEC:176). Searched: "plan record", "plan-<key>", "requested_at" in all plan files.
- Component: COORDINATOR (it saves the record and acks)
- Feature statement: For each plan request the coordinator saves its own plan record, then acknowledges, so a restart can resume the request.
- Done when: a kill-and-restart test between the two steps shows the request is still handled once.
- Depends on: S05-F19; FR-15, FR-29 patterns
- Evidence from our documents: no evidence found in our documents against it; FR-15 shows the plan wants the same order for claim wakes.
- Concerns: file layout must follow the plan's `<state_dir>/issues/` and NFR-02 one writer per file (SPEC:215), not Clay's `.orchestrator/` path.

### S05-F23 The coordinator runs `/sc:issue --plan <N> --depth <d>` for the plan request
- 655 says: the orchestrator calls `Skill sc:issue-protocol --plan <N> --depth <d>`; the issue stays held and unclaimed (body line 80).
- Status: NOT-COVERED
- Current plan: the depth key is covered by FR-59 (see S05-F24). The plan names one automatic caller of `--plan`: the hand-back re-plan (FR-35, SPEC:237). No requirement has the coordinator call `--plan` for a new plan-less issue; FR-56 only warns a person (SPEC:277); VERD(D09):21 says the plan body write waits on D07. Searched: "--plan", "plan_depth", "append_plan_sections" in SPEC and DECISIONS.
- Component: COORDINATOR (calls the skill, needs the grant)
- Feature statement: On a plan-request wake the coordinator calls `/sc:issue --plan <N> --depth <plan_depth>` and leaves the issue unclaimed.
- Done when: a test with a stub skill shows one call per request with the configured depth, and no claim.
- Depends on: S05-F19, S05-F22, S05-F27, S05-F24
- Evidence from our documents: VERD(D12):41 "Document as called by a session that holds the issue"; SPEC:107 (OD-11) the owner grants at most four standing entries, the plan-body grant is not one of them.
- Concerns: the plan body write needs the grant `issue.body.append_plan_sections` (VERD(D09):21) and grants start empty (OD-11, SPEC:107; SEC-07). The edit voids any approval (FR-04). Treat the issue text as data; the skill must never take commands from it (FR-55 S5, SPEC:276).

### S05-F24 The plan depth comes from a `plan_tier` setting (default `tier1b`)
- 655 says: `<d>` comes from `plan_tier` (default `tier1b`); it sets the depth of `/sc:issue --plan` (body lines 9 and 80).
- Status: CONFLICT
- Current plan: OD-1 "`plan_depth` key, default `quick`; no `plan_tier`" (SPEC:97); FR-59 "Provide key `plan_depth` (quick, standard, deep; unset means `quick`, run by `issue-worker-t3`) passed to `/sc:issue --plan --depth`; no `plan_tier`" (SPEC:280); D15 C6 (VERD(D15):78).
- Depends on: none
- Evidence from our documents: VERD(D15):78 "`plan_tier` becomes a plain `plan_depth` passed to `--plan --depth`". OD-1 confidence is 66% (SPEC:97).
- Concerns: low confidence on OD-1 (66%); the default `quick` (cheapest worker) versus Clay's `tier1b` is a quality and cost choice the owner may revisit. The `worker_tier` and `orchestrator_tier` part of 655 line 9 belongs to the models section.

### S05-F25 Plan-call failure rules: a call that fails twice, or a repeated heading, is escalated
- 655 says: a `--plan` call that fails twice, or a repeated heading, is escalated (body line 80).
- Status: NOT-COVERED
- Current plan: the repeated-heading rule is in the check (FR-54, SPEC:275) and `--plan` stops on it (655 line 81 / S05-F28); the escalation path exists as a verb (`escalate`, FR-26, SPEC:228; FR-37, SPEC:239). No rule says "escalate after two failed plan calls". Searched: "fails twice", "escalat", "repeated" in SPEC and verdicts.
- Component: COORDINATOR (counts attempts and calls `escalate`)
- Feature statement: When `/sc:issue --plan` fails twice for one request, or stops on a repeated heading, the coordinator writes one escalation to the person.
- Done when: a test with a failing stub shows no escalation after one failure, one escalation after the second, and one on a repeated-heading stop.
- Depends on: S05-F23; FR-26, FR-37
- Evidence from our documents: no evidence found in our documents
- Concerns: the nine-row escalation table of 655 section 3 is another section; the plan's `escalate` must name a row (FR-37 fails open with a marker, OD-4, SPEC:100).

### S05-F26 Poll reason `plan_stuck` when a plan call is unfinished after 60 minutes
- 655 says: a call unfinished after 60 minutes raises the poll reason `plan_stuck` (body line 80); the closed reason table has exactly 62 names (criteria line 215).
- Status: NOT-COVERED
- Current plan: none found; searched: "plan_stuck" across all plan files (no match); the reasons table is FR-20 (SPEC:210) with `held_incomplete` and `held_backlog` only (SPEC:595, R-1).
- Component: WATCHER (skip and alarm reasons belong to the poll's table)
- Feature statement: The poll adds the reason `plan_stuck` to its closed reasons table and raises it when a plan request has had no finish for 60 minutes.
- Done when: the reasons-table test lists `plan_stuck`, and a clock test shows it at 60 minutes and not at 59.
- Depends on: S05-F19, S05-F22
- Evidence from our documents: SPEC:595 (R-1) names the two plan-related reasons the plan keeps: `held_incomplete`, `held_backlog`.
- Concerns: the 60-minute number is 655's own, not measured. The plan requires the reasons table to equal the code (FR-20, MC-10), so adding a name means recomputing the pin.

### S05-F27 PR P: the `/sc:issue --plan` mode is its own small pull request, built before PR B
- 655 says: PR P is its own small PR, built before PR B; it changes `commands/issue.md`, `SKILL.md`, new `refs/plan.md` and two issue test files (body line 81).
- Status: COVERED
- Current plan: PR 690 is Clay's PR P: "KEEP-ADAPT, merge in lane 1" (SPEC:385; FR-53, SPEC:274); stage S2 (SPEC:486); L-04 (SPEC:357); merge after PR 693 (FR-60, SPEC:281). The plan adapts it first (four fixes of D12) and builds the coordinator skill later.
- Depends on: none
- Evidence from our documents: no conflict found
- Concerns: the plan needs four fixes before merge: fence-aware heading count, one definition of "passes", `plan.md` names who calls `--remaining`, confirm the live head (FR-53). Inventory says PR 690 touches 13 to 15 files (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/inventory/clay-prs.md:110), more than the files 655 lists. PR 690 is a draft and stays a draft until the owner rules (SPEC:772).

### S05-F28 PR P behavior: append an absent section, fill an empty one in place, stop on a repeated heading, one marked body edit, no comment
- 655 says: `--plan` appends an absent section, fills an empty one in place, stops on a repeated heading, and makes one marked body edit and no comment (body line 81).
- Status: COVERED
- Current plan: adoption of `--plan` and `plan_body.py` (`check`, `splice`, `verify`; deterministic body write with race and read-back checks) (VERD(D12):35; D12 item 2 at VERD(D12):18; FR-53, SPEC:274). A repeated heading fails the check (FR-54, SPEC:275).
- Depends on: S05-F27
- Evidence from our documents: no conflict found
- Concerns: UNVERIFIED in our documents: the exact behaviours "no comment" and "fills an empty one in place" were not read from `plan.md`; the plan only describes `plan_body.py` in general terms.

### S05-F29 `--remaining <file>` rewrites `## Fix approach` and `## Test plan` to what is left (done items kept) for a hand-back round
- 655 says: `--remaining <file>` rewrites those two sections to the scope that is left, done items kept, for a hand-back round (body line 81).
- Status: COVERED
- Current plan: FR-53 and D15 A8 "Adopt with change" (VERD(D15):48); FR-35 round 2 re-plans with `/sc:issue --plan <N> --remaining <file> --depth <d>` and the whole start gate repeats (SPEC:237); OD-2 (SPEC:98).
- Depends on: S05-F27; 655 section on hand-back
- Evidence from our documents: VERD(D12):41 "its consumer (the `handback` verb of Clay's PR B) is unbuilt"; DEC:785 "UNVERIFIED: ... fidelity of `--remaining` in keeping done items; `HANDBACK_MAX` = 3 is 'not measured'".
- Concerns: the plan adds that re-plan voids approval, so a person must approve again (OD-2, R-6 at SPEC:600), which 655 does not have.

### S05-F30 At the start of wave 1 the orchestrator re-reads the issue live: no `hold:backlog` and the plan still passes, or nothing is claimed
- 655 says: at wave 1 the orchestrator re-reads the issue live; without `hold:backlog` and with a passing plan, or nothing is claimed (body line 82; criteria line 219).
- Status: COVERED
- Current plan: VERD(D12):21 item 5 "held by the orchestrator's own `plan-check` at its wave 1"; FR-26 verb `plan-check` (SPEC:228); FR-61 `plan-check` is the same function as `plan_body.py check` (SPEC:282); FR-02 repeat every start gate at the moment of start (SPEC:192); FR-08 wake-time re-check of plan check and `hold:backlog` (SPEC:198). D01 MR-1 widens it: the re-check must also repeat the approval, `unchanged_since` and Status allow-list (VERD(D01):14).
- Depends on: S05-F10, S05-F15
- Evidence from our documents: VERD(D01):14 "PR 686's wave-1 re-check covers only `hold:backlog` and `plan_check`" (the plan found this too narrow).
- Concerns: the live re-read also has to repeat the approval, unedited-since and Status gates, or the plan's MR-1 fails. UNVERIFIED which actor runs it in the plan: FR-02 is the poll's `_revalidate`; the coordinator's own live re-read is named only in D12 item 5 and FR-61.

## Section summary
- 30 features: the plan already delivers the claim half of section 5 (claim at `--pipeline none`, one supervised `worker-start` worker, guard, claim-once), the plan check, `hold:backlog`, PR P (PR 690) with `--remaining`, and the wave-1 re-check.
- Four 655 rules are rejected: the `hold:plan` label write and its grant (Q03, D09, FR-06, FR-07), the "hold removed by hand stays removed" rule that only serves that writer, `plan_tier` (OD-1, FR-59 use `plan_depth`), and "edits after the claim are fine" (D01 item 5: an edit voids approval).
- The whole automatic plan-request chain is NOT-COVERED because the plan deferred it (D15 A4): the quiet-hour request (WATCHER), its in-flight place (WATCHER), the `plan_stuck` reason (WATCHER), the plan record, the `--plan` call and the failure escalation (COORDINATOR), and the one report line for a later edit (COORDINATOR). These items form one group and share a prerequisite: a ruling on who plans and where the person's approval fits (an edit after approval voids it).
- Biggest open points: the plan's order is plan, approval, claim while 655 has no approval step (section 1 conflict, not classified here); binding of `worker-start` workers is unobserved; the plan-body write grant is not in the owner's four standing grants.

<!-- END -->
