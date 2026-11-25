# Section 03 analysis: Deliverables (Proposed Solution, section 3, body lines 48-59)
Counts: COVERED 18, CONFLICT 11, NOT-COVERED 7 (36 features)

Scope note: classified against the current plan = SPEC.md (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`, cited as SPEC:line), DECISIONS.md, the verdicts under `debates/<id>/VERDICT.md` (cited by id and line), FOLLOW-UPS.md and the tech references. "Coordinator" and "orchestrator" are treated as the same role when matching. Acceptance Criteria lines 215, 217, 220, 221, 228, 229 of the issue body touch this section and are folded into the rows below. Numbering warning for builders: 655 uses "FR-23", "FR-24", "T13" for items of Clay's IronFlow coordinator spec and test plan; the current plan uses the same labels for different things (SPEC FR-23 = watcher off by default; SPEC FR-24 = coordinator command; plan T13 = `tests/coordinator/test_merge_path.py`). Do not mix them.

## A. The orchestrator skill, command and verbs (body line 50)

### S03-F1 Skill and command exist in IronClaude with the section 2 workflow
- 655 says: IronClaude gets a skill and a command carrying the section 2 workflow, the templates, the playbook and the verbs (line 50; AC line 217: `SKILL.md` lists waves 0 to 9 with ref, commands, template and ending check, in the structure of `sc-issue-protocol`, `sc-pr-submit-protocol`, `sc-troubleshoot-protocol`).
- Status: COVERED
- Current plan: SPEC FR-24 (SPEC:226: role "coordinator", command `/sc:coordinator`, skill `sc-coordinator-protocol`, flags `--wake`, `--hourly`, `--resume`, `--take`, `--sub`); built in stage S14 (SPEC:498: "`/sc:coordinator` command and skill"); flag-less call is person-opened (FR-25, SPEC:227). The wave contents themselves are classified in 655 section 2 by another analyst.
- Depends on: S03-F2 (name), S03-F3 (verbs)
- Evidence from our documents: n/a (COVERED)
- Concerns: the plan builds the substrate (S13, SPEC:497) before the skill (S14), so the skill cannot land first.

### S03-F2 Names `orchestrator`, `/sc:orchestrator`, `sc-orchestrator-protocol`, `superclaude orchestrator`, `src/superclaude/cli/orchestrator/`
- 655 says: the skill is `orchestrator`, the command `/sc:orchestrator`, the protocol dir `sc-orchestrator-protocol`, the verb group `superclaude orchestrator` in `src/superclaude/cli/orchestrator/` (lines 3, 50, 62).
- Status: CONFLICT
- Current plan: D08 and FR-24 (SPEC:226: "no `commands/orchestrator.md`, no `sc-orchestrator-protocol`"); FR-62 (SPEC:319: "coordinator" for the session role, "orchestrator" only for Orca's layer and quoted titles); FR-63 (SPEC:320: renames `superclaude orchestrator ...` verbs). 655's names are REJECTED; the role is kept under the plan's names.
- Depends on: none
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/VERDICT.md:18` "Test: no `commands/orchestrator.md` and no `sc-orchestrator-protocol` exists after the unified work." Also D08 VERDICT:34 "'Orchestrator' already means the parent session of a skill in 63 installed files".
- Concerns: none beyond the numbering warning above; rename must happen before PR 686 merges (FR-63, SPEC:320).

### S03-F3 Eleven of the twelve verbs
- 655 says: twelve verbs `wake-check, wake-ack, state, lease, merge-gate, plan-check, repos, report-entry, escalate, answer-check, audit, handback`, with no `hold` verb (lines 50, 62).
- Status: COVERED
- Current plan: FR-26 (SPEC:228): one group `superclaude coordinator` with wake-check, wake-ack, state, plan-check, repos, merge, merge-gate, answer-check, audit, report-entry, escalate, handback, one JSON contract and one state lock. Eleven names match 655; the plan adds `merge` (a head-pinned merge verb, SEC-02, SPEC:291). No `hold` verb in either (the poll writes no label, FR-06, SPEC:196). Group name differs (see S03-F2). Built in S13 to S15 (SPEC:497-499).
- Depends on: S03-F2, S03-F4
- Evidence from our documents: n/a (COVERED)
- Concerns: 655's `lease` is dropped (S03-F4); 655's verb count of twelve stays twelve in the plan only because `merge` replaces `lease`.

### S03-F4 `lease` verb and the lease comment
- 655 says: `lease` is one of the twelve verbs (line 62); the "Claimed by" marker plus lease is part of the no-double-claim story (T4, line 200).
- Status: CONFLICT
- Current plan: FR-26 (SPEC:228: "no lease, no interrupt"); FR-40 (SPEC:242: lease comment reserved with a trigger); OD-8 (SPEC:104: "No lease comment now; reserved with a trigger."). 655's `lease` verb is REJECTED for the first build.
- Depends on: none
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/VERDICT.md:21` "The lease has a defect the design does not fix, and its trigger is absent on the settled single-host topology." and QG4:48 "drop `lease` from the verb list".
- Concerns: QG4:63 rates the reserve a bet that the one-host topology holds (design's own K13 medium/medium).

### S03-F5 `limits.py`: one `refuse(argv)` function behind every verb, a test per "may never" line
- 655 says: a module `limits.py` holds the refusal function that every `gh`, `git` and `orca` call of every verb passes through; each "may never" line has a test (line 62, 140; AC line 225).
- Status: COVERED
- Current plan: FR-26 (SPEC:228: "closed `refuse(argv)` list with a failing test per pattern", `tests/coordinator/test_refuse_argv.py`); D15 D8 adopted with change (SPEC:459: "N6 unconditional, no N7"); SEC-11 (SPEC:300: tag and publish refused, one test each); built in S13 (SPEC:497).
- Depends on: S03-F3
- Evidence from our documents: n/a (COVERED)
- Concerns: 655's "may never" list also carries "never stop a worker ... apart from that one interrupt" and an `escalate --interrupt` exemption (body line 140); the plan rejects the interrupt (OD-7, SPEC:103; D15 D9 REJECT, SPEC:458). That interrupt exemption is classified in 655 section 9 by another analyst; the list must be copied without it.

### S03-F6 `names.py`: no agent or model named in anything user-facing
- 655 says: a module that is not a verb enforces that no agent or model is named in user-facing text (line 62).
- Status: COVERED
- Current plan: FR-37 (SPEC:239: scan only `report-entry` and `escalate`, after U54; write anyway with a visible marker on a name-check failure, original in the action log); OD-3 (SPEC:99: scope B, "measure U54 first"); OD-4 (SPEC:100: fail open); QG2 action "Build `names_check` as fail open in the coordinator verb group" (QG2 VERDICT:53).
- Depends on: S03-F3
- Evidence from our documents: n/a (COVERED)
- Concerns: the plan's scope is narrower than "anything user-facing" (two writers only) and it fails open; U54 (false refusals over the last 50 titles) is UNVERIFIED (SPEC:669) and must be measured before the rule is enforced. QG2 VERDICT:63 notes the owner has not ruled on the naming rule; rulings 15, 27, 28, 39 are Clay's.

### S03-F7 Playbook file: how to unstick a worker (655's FR-23), typing into a worker terminal
- 655 says: `refs/playbook.md` and a worker check-in; the orchestrator unsticks workers by typing into their terminals under FR-23 (lines 50, 62, 92, 121).
- Status: COVERED
- Current plan: FR-40 (SPEC:242: type into worker terminals only under the four typing rules; never interrupt); D15 D14 adopted with change (SPEC:462, D15 VERDICT:98: "Typing rules 1, 2, 3, 5 add conditions at no cost"); FR-14 (SPEC:204: type only into an idle session, empty draft, 60 s quiet). Searched for the word "playbook" in SPEC.md, DECISIONS.md, all VERDICT.md, merged-requirements.md, inventory (no hit outside adversarial transcripts): the plan names the rules but no `playbook.md` file.
- Depends on: S03-F8 (approval part is rejected), S03-F21 (check-in template)
- Evidence from our documents: n/a (COVERED)
- Concerns: the unsticking content of 655's playbook is not itself reproduced in the plan documents (UNVERIFIED that the plan's four typing rules equal 655's FR-23 rules, since the IronFlow spec was never read, see S03-F28).

### S03-F8 Approving a worker's permission prompts (655's FR-24, "answer an approval once")
- 655 says: the orchestrator approves a permission prompt itself when the action is not in rows 1 to 7, typing and approvals included (lines 92, 121, 140; AC line 222).
- Status: CONFLICT
- Current plan: D15 D14 (D15 VERDICT:98: "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases"); FR-40 (SPEC:242: "never approve a permission prompt"); D15 VERDICT:238 summary "never answers a permission prompt". 655's approval handling is REJECTED. (Related: the "never a permanent always allow" line has nothing to guard once approvals are refused.)
- Depends on: S03-F7
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:98` "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases; S4 stays a report line".
- Concerns: none.

## B. The poll script (body line 51)

### S03-F9 A poll script exists, is read-only for the model, and starts no agent when nothing is new
- 655 says: "The poll script the Orca automation runs" finds new work with no model; when nothing is new no agent starts and no tokens are spent (lines 23-24, 51, 110; AC line 215).
- Status: COVERED
- Current plan: the poll is the existing `issue-watch once`, run per project by the dispatcher `issue-watch run-all` (FR-11, SPEC:201); a poll is read-only on GitHub (FR-06, SPEC:196; NG-2 kept, FR-82, SPEC:218); the shadow-run pass criterion is "no agent, no config generated, no GitHub write" (SPEC:705). Who is woken and how (wake files, ack) is FR-13 to FR-19 (SPEC:203-209), classified under 655 section 1.
- Depends on: S03-F10 (scheduler), S03-F11
- Evidence from our documents: n/a (COVERED)
- Concerns: in the plan the poll itself starts the claim session (`/sc:issue --claim <N> --pipeline none` via `orca agent launch`, SPEC:125, SPEC:174), whereas 655 has the orchestrator run the claim. That difference belongs to 655 sections 1 and 2.

### S03-F10 Scheduler: an Orca automation every 5 minutes, "no cron entry exists"
- 655 says: an Orca automation runs the poll script every 5 minutes as a precheck that exits non-zero; no cron entry exists (lines 23, 110; AC line 215; "Dropped on purpose: cron (FU-2)", line 161).
- Status: CONFLICT
- Current plan: D02 (SPEC:78: "Cron stays the scheduler; ... Clay's precheck automation is a tested-first fallback"); FR-10 (SPEC:200: one cron entry `*/5 * * * *` under `flock -n`, installed once per boot by the image, acceptance "one `crontab -l` line after two restarts"); section 7 row B2 REJECT (SPEC:449); B1 precheck pattern kept only as a conditional fallback (SPEC:449, 13.2 "Precheck test", SPEC:704). 655's automation-as-scheduler and the "no cron" criterion are REJECTED.
- Depends on: none
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/VERDICT.md:9` "Cron with one dispatcher stays the scheduler (the owner's line wins the tie)". The owner's reason was partly wrong and D02:17 corrects it ("a scheduled automation whose precheck exits non-zero starts no agent"), so Clay's technical claim is right but the choice still went to cron; D02:23 names the one test that would reverse it (a disabled-then-enabled automation firing 1 to 24 hours with only `skipped_precheck` rows).
- Concerns: D02:21 and SPEC:704 note cron is not in the image yet (Coder issue 515); the `orchestrator-poll` automation of 655 is UNVERIFIED to exist at all (OBSERVER techref `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:822`: "outside the repo: **[UNVERIFIED]**").

### S03-F11 Safety features carried over from the built poller (655 section 11)
- 655 says: the poll reuses the built `issue-watch` code with one claim and one worker start per issue, up to 3 delivery tries, a run lock, a call budget, an audit log, a dry-run mode, a validated integer in the launch prompt and an origin check (line 160, referenced at line 51).
- Status: COVERED
- Current plan: claim marker guard (FR-03, SPEC:193); three deliveries (FR-13, SPEC:203); lock and flock (FR-10, SPEC:200; D07 VERDICT:15 "its own lock, state directory, kill switch and day cap"); audit log (interface row 3, SPEC:173; FR-20, SPEC:210); dry-run (FR-11, SPEC:201; MC-12, SPEC:478); no GitHub text in prompts (SEC-16, SPEC:305); origin check test kept (13.1, `test_origin_parity.py`, SPEC:696); one writer per file (NFR-02, SPEC:215).
- Depends on: S03-F9
- Evidence from our documents: n/a (COVERED)
- Concerns: a "call budget" (as distinct from the day cap) is not named in SPEC.md (searched "budget", "call budget", "rate limit": no hit), so that one item is UNVERIFIED as kept; it lives in master's `github.py` per 655 line 160. The claim that "one worker start per issue" holds depends on FR-21 (SPEC:211) and the unproven worker binding (RK-1, SPEC:645).

### S03-F12 The hold of addition A: plan check and person-set `hold:backlog`, read-only
- 655 says: the poll checks `## Priority`, `## Fix approach`, `## Test plan` are each present once and filled; a failing issue is not sent on; a person's `hold:backlog` makes the system do nothing with the issue; assignment stays a precondition-only trigger (line 25; AC line 219).
- Status: COVERED
- Current plan: FR-05 (SPEC:195: read-only plan check, skip as `held_incomplete`, `hold:backlog` skipped as `held_backlog`, a `<...>`-only section counts as empty); FR-54 (SPEC:275: one plan check, `plan_body.py check` is the reference, copy in the package with a parity test); FR-08 (SPEC:198); D09 and Q03 (SPEC:85, 95); section 7 rows A1 to A3 ADOPT+CHANGE (SPEC:441).
- Depends on: S03-F18 (plan check lives in `plan_body.py`, PR 690)
- Evidence from our documents: n/a (COVERED)
- Concerns: in the plan "assignment" is not the only trigger: FR-01 (SPEC:191) still requires approval (field `Approved`), an allowed Project Status and an unedited-since check (see S03-F17).

### S03-F13 `hold:plan` label written by the poll, label removed when the check passes
- 655 says: a failing issue gets the label `hold:plan` (label only, never a comment) written by the poll; when the check passes the poll removes it; a hold removed by hand stays removed; there is no `hold` verb because the poll alone writes the label (lines 25, 62; AC line 219).
- Status: CONFLICT
- Current plan: FR-06 (SPEC:196: "Write nothing to GitHub in a poll cycle (NG-2): strip the label writer of PR 686"); FR-07 (SPEC:197: a leftover `hold:plan` is ignored, `issue.hold` grant dropped); FR-82 (SPEC:218); Q03 (SPEC:95); section 7 row A5 REJECT now (SPEC:443). 655's label write is REJECTED; it may return only as its own later PR with a shown reader, an NG-2 amendment, a 24-hour shadow run and a cron write test (SPEC:443; Q03 VERDICT:23).
- Depends on: S03-F12
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/VERDICT.md:21` "A `hold:plan` label on an issue is ignored. A person who wants a stop uses `hold:backlog`." and Q03:32 "NG-2 says 'no GitHub write'". Also `debates/D09/VERDICT.md:81` "Whether anyone reads `hold:plan` on GitHub" (UNVERIFIED benefit).
- Concerns: the "a hold removed by hand stays removed" state (`hand_removed`) goes with the label code (SPEC:196). The plan's local `holds` entry (FR-07) is the replacement for visibility.

### S03-F14 One plan request after one hour with no plan work
- 655 says: after one hour with no plan work the poll sends ONE plan request to the repo's orchestrator, which makes the plan through `/sc:issue --plan` (line 25; AC line 219).
- Status: NOT-COVERED
- Current plan: none found that builds it; searched: SPEC.md, DECISIONS.md, D09, D10, D15 VERDICT.md for "plan request", "one hour", "A4". The only hit is a DEFER: section 7 row A4 (SPEC:442: "Plan request after one hour with titles | DEFER | none").
- Component: WATCHER: it is a wake item written by the poll after a timer on the held issue.
- Feature statement: When an assigned issue has stayed in `held_incomplete` for one hour, the poll adds one id-only plan request to the repo coordinator's wake file so the coordinator can run `/sc:issue --plan`.
- Done when: a fixture issue held for 61 minutes yields exactly one plan request in the next wake and none in later cycles, and the request carries repo, number and url only.
- Depends on: S03-F12, S03-F18, 655 section 1 (wake format), 655 section 5 (plan mode)
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:44` "A wake-file item, not a GitHub write (D09 item 5); a title is free GitHub text (D10 item 5) ... Not built now; if built, ids only and after D07 settles who plans".
- Concerns: wake items must hold ids only (FR-13, SPEC:203; SEC-16, SPEC:305), so 655's plan request may not carry the issue title.

### S03-F15 A closed table of reason names in the audit log
- 655 says: the poll script ships a closed reason table (line 51; AC line 215).
- Status: COVERED
- Current plan: FR-20 (SPEC:210: reasons table equal to the code; restore the 14 approval reasons, add `coordinator_full`, `name_collision`, `no_checkout`, `coordinator_absent`, remove `registry_invalid`, `repo_not_listed` and four label-write reasons); MC-10 (SPEC:478); D15 E6 adopt with change (D15 VERDICT:114).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: see S03-F16 for the number.

### S03-F16 The reason table has "exactly 62 names"
- 655 says: "The closed reason table has exactly 62 names." (AC line 215; line 51).
- Status: CONFLICT
- Current plan: FR-20 (SPEC:210) and MC-10 (SPEC:478) require the table to equal the code after the plan removes six names and adds at least 14 + 4; the 62-name pin in PR 686's `test_audit.py:86-98` is the very test that forbids the 14 approval reasons the plan needs (D15 VERDICT:114: "recompute the pin"). 655's fixed count of 62 is REJECTED; the plan pins the recomputed set, not a number.
- Depends on: S03-F15
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:170` "the 62-reason table is pinned by a test that forbids the 14 approval reasons the approval gate needs". The final count is not stated in any plan file (my arithmetic 62 - 6 + 14 + 4 = 74 is UNVERIFIED and assumes no overlaps).
- Concerns: do not write a test that asserts 62.

### S03-F17 No trigger label, approval label, approver list, Project or Backlog read, and no plan-approval gate remain
- 655 says: the poll and the whole flow drop the trigger label, the approval label and approver list, the Project Backlog requirement and the plan-approval gate (WC-17, `issue_pipeline` approval rows, guard G2 rule 1); assignment is the only trigger (AC line 229; line 161; line 24).
- Status: CONFLICT
- Current plan: D01 (SPEC:77: "Approval, not assignment, starts work"); FR-01 (SPEC:191: approved by field `Approved`, allowed Project Status, no `hold:backlog`, plan check passing; "Assignment alone never starts work"); FR-02 (SPEC:192); D03 (SPEC:79: revert PR 682); FR-31 (SPEC:233: plan approval recorded, `check-approval` run); section 7 rows A12 and A13 REJECT (SPEC:447-448). PR 700 already put the plan-approval code back on master (Appendix B.1, SPEC:758). 655's removal list is REJECTED.
- Depends on: none
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/VERDICT.md:17` "Conditions to revisit. Assignment alone may be reconsidered only when all four hold: the launch guard refuses to start when it is not effective ...; the owner records the reversal of R19 in chat." The open owner answer OA-1 ("both gates stay" or "only the start gate") is still unrecorded (SPEC:789, Appendix B.3 item 4).
- Concerns: OA-1 decides whether the plan-approval gate stays; until the owner answers, builders must not remove it.

## C. The `/sc:issue --plan` mode (body line 52)

### S03-F18 `/sc:issue --plan` with `--remaining`, as its own small pull request built before the skill
- 655 says: a plan mode with `--remaining`, its own small PR built before the orchestrator skill (line 52; section 12 "PR P ... after D and before B", line 167).
- Status: COVERED
- Current plan: PR 690 is the carrier: KEEP-ADAPT, merge in lane 1 (SPEC:385); FR-53 (SPEC:274: fence-aware heading count, "passes" defined once, `plan.md` says who calls `--remaining`, rebase on master plus PR 693); stage S2 "adapt and merge PR 690" (SPEC:486), before the coordinator stages S13 to S15; L-04 (SPEC:357); D12 (SPEC:88; D12 VERDICT:11: adopt `--plan`, `plan_body.py`, `--remaining`); FR-60 (SPEC:281: merge PR 693 first).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: 655's header says the plan call runs on `plan_tier` (default `tier1b`, body line 9); the plan decided against it: OD-1 (SPEC:97: "`plan_depth` key, default `quick`; no `plan_tier`") and FR-59 (SPEC:280). That tier setting is outside this section but a builder of `--plan` must use `plan_depth`. The plan also treats PR 690's own `--remaining` consumer (`handback`) as unbuilt (D12 VERDICT:41).

## D. The four templates (body line 53)

### S03-F19 A handoff-prompt template that names the filed plan and carries the worker-binding marker
- 655 says: `templates/handoff-prompt.md` is one of four template files, used by wave 4 to start the worker (lines 41, 53, 62).
- Status: COVERED
- Current plan: FR-61 (SPEC:282: "Hand the `--pipeline none` worker a chain from the coordinator's own template that names the filed plan"); FR-30 (SPEC:232: marker `[sc-launch:v1:<nonce>]` in the first prompt); D05 action "Add the marker line to `templates/handoff-prompt.md`" (D05 VERDICT:58); D12 action (D12 VERDICT:66: handoff template "chooses the chain and must name the filed plan").
- Depends on: S03-F20
- Evidence from our documents: n/a (COVERED)
- Concerns: the marker line is a prompt-injection surface: SEC-17 (SPEC:306) bars marker-bearing text from a coordinator session.

### S03-F20 Handoff template has nine sections in order, and the `Fixes` or `Refs` link rule for the worker's PR
- 655 says: the handoff has nine sections in order; every worker PR links its issue with `Fixes <repo>#<N>` only when it fully addresses the issue and `Refs` otherwise (line 100; AC line 220).
- Status: NOT-COVERED
- Current plan: none found; searched: SPEC.md, DECISIONS.md, all `debates/*/VERDICT.md`, merged-requirements.md and both tech references for "nine sections", "handoff", "Refs" (word match), "Fixes". The plan states only the limit ("a `Fixes` line still closes at merge", SEC-12, SPEC:301) and never sets a rule for what the worker writes.
- Component: COORDINATOR: the template is filled by the coordinator at handoff.
- Feature statement: The coordinator's handoff template tells the worker to write `Fixes <repo>#<N>` in its PR only when the PR fully delivers the issue's own criteria and `Refs <repo>#<N>` otherwise, in a fixed section order that a test pins.
- Done when: a test renders the template for a part-done round and asserts `Refs`, renders it for a full-scope issue and asserts `Fixes`, and checks the section headings appear in the stated order.
- Depends on: S03-F19; 655 section 4 (nine section list); `/sc:closeout` (S03-F34)
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md:835` "RK-25 | Closeout or a `Fixes` line closes an issue whose work is unfinished | ... `Fixes` closing is GitHub behaviour outside the gate | Close only under the go (K12); keep `left_open`; state the limit".
- Concerns: 655 itself admits a wrongly written `Fixes` still closes the issue and no script checks it (K28, line 100); the plan's answer is a go before closing (SEC-12), which 655 does not have (see S03-F34).

### S03-F21 A worker check-in template
- 655 says: `templates/worker-checkin.md` is filled for each hourly check-in (lines 42, 53, 92).
- Status: NOT-COVERED
- Current plan: none found; searched: "check-in", "checkin", "worker-checkin", "hourly" in SPEC.md, DECISIONS.md, D04, D05, D15, merged-requirements.md. Only the flag `--hourly` (FR-24, SPEC:226) and the typing rules (FR-40, SPEC:242) exist; D04 VERDICT:35 and D15 VERDICT:96 mention "check-ins" as part of the supervised route but define no template.
- Component: COORDINATOR: it is the message the coordinator sends a running worker.
- Feature statement: The coordinator skill carries one check-in template used at each `--hourly` pass, id-only for GitHub data and written under the four typing rules.
- Done when: a test fills the template and the filled text contains no GitHub-sourced free text and is refused by `refuse(argv)` if the target terminal has unsent typing or output under 60 seconds old.
- Depends on: S03-F7, 655 section 2 wave 5
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:96` "D12 | One supervised `worker-start` route: mailbox, one message handled once per id, check-ins, restart ... | Adopt with change" (the check-in itself is adopted; the template is not specified).
- Concerns: the plan's rule against approving permission prompts (S03-F8) removes part of what 655's check-in does.

### S03-F22 Report-entry-update template
- 655 says: `templates/report-entry-update.md`, following the work report's `item-template.md`, is filled at every step that changes the entry (lines 40-45, 53).
- Status: COVERED
- Current plan: FR-48 (SPEC:259: `report-entry` the only writer of an entry file); D11 "Plain-English item template: Adopt with change: generic wording" (D11 VERDICT:38); section 7 row E5, E7 (SPEC:464); FR-80 (SPEC:263: entry fields shown only from a named allowlist).
- Depends on: S03-F31
- Evidence from our documents: n/a (COVERED)
- Concerns: the writer and the skill that holds `item-template.md` are blocked until the report skill is restored (S03-F32).

### S03-F23 Escalation template with the nine-row table
- 655 says: `templates/escalation.md` holds nine rows; `escalate` refuses an entry that names no row (line 137; AC lines 220, 224).
- Status: COVERED
- Current plan: FR-47 (SPEC:258: nine-row table in the notice step only, exactly nine rows); FR-37 (SPEC:239: write the escalation first, send nothing if refused); D15 D16 adopt with change (SPEC:463); D11 (D11 VERDICT:35).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: QG2 VERDICT:69 lists as UNVERIFIED "Whether the real escalation template fences paths, shas and numbers"; the 5-a-day cap stays a proposal with default 0 (FR-47, SPEC:258; D11 VERDICT:36), while 655 sets `reach_daily_max` to 5 per repo (line 137).

### S03-F24 Each of the four templates is a file with its own test
- 655 says: "The four templates, each a file with a test"; AC line 220: the four files exist, each with a test, used by every step that writes or sends.
- Status: NOT-COVERED
- Current plan: partly: QG2 keeps an "offline scan of every template, fixture and end-to-end body" (QG2 VERDICT:34) for the naming rule only, and S14 lists a "skill-text scan" (SPEC:498). No requirement says each template has its own test or that every writing step must use a template; searched "template" in SPEC.md section 4 and 8.
- Component: COORDINATOR: tests ship with the skill.
- Feature statement: Each coordinator template file has a test that renders it with fixture values, checks required sections and rejects unfilled placeholders, and a file table test checks every template is used by a step.
- Done when: `uv run pytest` shows one test module per template and a failing case for a deleted or unused template.
- Depends on: S03-F19, S03-F21, S03-F22, S03-F23
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/VERDICT.md:34` "Offline scan of every template, fixture and end-to-end body ... Merge: kept under scope B." (name check only).
- Concerns: none.

## E. The orchestrator repo (body line 54)

### S03-F25 A private repo `IronbellyOrg/IronOrchestrator` where the orchestrator sessions run
- 655 says: orchestrator sessions run in the private repo `IronbellyOrg/IronOrchestrator`; everything the orchestrator keeps while it runs lives there (lines 28, 54; section 11 of 655 aside).
- Status: CONFLICT
- Current plan: D07 item 1 and 2 (D07 VERDICT:15-16); FR-11 (SPEC:201: "no registry repository, no `repos.yaml`"); section 7 row C5 REJECT (SPEC:454); SPEC:46 lists "the registry repository" as a rejected design. The plan's coordinator runs in the project's own `Coordinator` worktree as `COORD-<RepoName>` (SPEC:125, 144; FR-64, SPEC:321; Coder issue 516), with shared records on branch `coordinators`.
- Depends on: none
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md:16` "No registry repo. The spec removes the separate `IronbellyOrg/IronOrchestrator` repo ... Test: a grep of the unified spec for `orchestrators.json` and `repos.yaml` finds only the 'rejected' table." Also D07:30: "On this host `/home/coder/workspaces/IronOrchestrator` does not exist and `orca repo list` does not show it, although the private repo exists on GitHub. REQ R17 says 'Nothing in the setup is manual.'"
- Concerns: D07:70 leaves one thing open (see S03-F30): the repo may still serve the report session.

### S03-F26 Repo list and the repo-to-checkout map kept in the orchestrator repo (`repos.yaml`)
- 655 says: the orchestrator reads the repo list and the repo-to-checkout map from the orchestrator repo, not from IronClaude configuration (lines 28, 54; also per-repo keys such as `max_in_flight`, `merge_method`, `merge_safety_files` in `repos.yaml`).
- Status: CONFLICT
- Current plan: FR-11 (SPEC:201: the dispatcher runs one poll per project of `orca repo list`; no `repos.yaml`); FR-12 (SPEC:202: per-repo JSON at `schema_version` 1 under `~/.config/superclaude/issue-watch.d/`, interface row 2, SPEC:172); D07 item 5 (D07 VERDICT:19: optional `merge` block with `merge_method`, `release_head`, `reviewers`, `merge_safety_files` in the per-repo config); resolved contradiction R-3 (SPEC:597: "per-repo JSON; PR 686's `repos.py` supplies key names only"). The coordinator verb `repos` exists (FR-26, SPEC:228) but reads and records config in that per-repo JSON. The location in 655 is REJECTED; the key names are adopted.
- Depends on: S03-F25
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/DECISIONS.md:1383` "R-3 | Settings home: `repos.yaml` keys (D04, D06) or per-repo JSON (D07) | Per-repo JSON in the project-local config".
- Concerns: SEC-10 (SPEC:299) makes the coordinator unable to edit `grants`, `merge_safety_files`, `reviewers` without a recorded owner answer; a shared repo file outside the project would need the same protection.

### S03-F27 A short overview of each repo, kept current as repos are added, removed or updated
- 655 says: the orchestrator repo holds "an overview of each repo" that changes as repos are added, removed or updated (line 54; comment 1 of the issue says it "also holds a short overview of what each repo is and does").
- Status: NOT-COVERED
- Current plan: none found; searched: "overview" and "IronOrchestrator" in SPEC.md, DECISIONS.md, all VERDICT.md, FOLLOW-UPS.md, merged-requirements.md. The only hit on a base "overview" is the report's `run.py refresh` reading a "base overview" (OBSERVER techref line 810); nothing in the plan creates or maintains one.
- Component: COORDINATOR: it is read by the per-project session (and the report) as repo context, next to its config.
- Feature statement: Each configured repo has a short plain-English overview file that the coordinator reads at intake and that is updated when a repo is added, removed or its purpose changes.
- Done when: `superclaude coordinator repos` lists each repo with its overview text, and a removed repo no longer appears.
- Depends on: S03-F26 (where the repo list lives)
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:810` "`run.py refresh` (7 stages: ... read base overview, drop held blocks, add entry blocks ...)" (the report's overview is a daily-report input, not a per-repo description).
- Concerns: free text from a repo overview that reaches a prompt would be GitHub-adjacent text; SEC-16 (SPEC:305) says no such text reaches a prompt, typed line or argv.

### S03-F28 Coordinator spec lives in the orchestrator repo; the IronFlow copy is kept in sync
- 655 says: the coordinator spec (`SPEC-AGENT-WORK-COORDINATOR-20261027.md`) moves to the orchestrator repo and the IronFlow copy is kept updated (FR-13, FR-1, FR-2, FR-19) (lines 54, 56, 92; AC line 228).
- Status: NOT-COVERED
- Current plan: none found; searched: "IronFlow", "coordinator spec", "SPEC-AGENT-WORK-COORDINATOR" in SPEC.md, DECISIONS.md, STATE.md, FOLLOW-UPS.md, all VERDICT.md, inventory, techrefs. Every hit says the IronFlow coordinator spec was NOT read by the debates.
- Component: OTHER: it is cross-repo documentation upkeep in the IronFlow repo, not a watcher, coordinator or dashboard behavior.
- Feature statement: After the plan's names and authority rules are final, the IronFlow coordinator spec is checked against them, its copy is updated for each changed rule, and one owner-named home for the spec is recorded.
- Done when: a diff list shows each requirement of the IronFlow spec that cites 655 (FR-1, FR-2, FR-13, FR-19, FR-23 to FR-25) marked kept, changed or dropped, with the owner's recorded choice of home.
- Depends on: S03-F29, S03-F25
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/VERDICT.md:87` "Clay's `RULINGS.md` (the full rulings file) and the IronFlow coordinator spec were not read." Same gap at D05 VERDICT:85, D10 VERDICT:90, D11 VERDICT:108, D15 VERDICT:264 and `inventory/clay-prs.md:200`.
- Concerns: UNVERIFIED claims all round: the spec's existence, its contents and whether "GeneralIronFlow" (D05 VERDICT:85) is an account with authority. Treat anything cited from it as unconfirmed.

### S03-F29 Edits to the coordinator spec: merges and issue closing leave the human-only list (FR-13); five places change for the interrupt (rows C25 to C29)
- 655 says: moves and spec sync include FR-13 and rows C25 to C29 of spec 6.3 (line 56); this issue "takes merges and closing issues off that list" (line 98); an interrupt exemption changes five places of the coordinator spec (line 140).
- Status: CONFLICT
- Current plan: SEC-01 (SPEC:290: merge only on a person's typed go bound to the head sha); SEC-06 (SPEC:295: no standing `pr.merge` or `issue.close`); SEC-12 (SPEC:301: one per-PR go covers merge and close); OD-7 (SPEC:103: "No interrupt of a running worker."); OD-10 (SPEC:106); section 7 rows D7, D9 REJECT (SPEC:458). The merge and close remain person-gated, and the interrupt is rejected, so these spec edits are REJECTED. Unverified: spec 6.3 rows C25 to C29 are in `docs/designs/orchestrator.md`, deleted from master by PR 700 (Appendix B.1, SPEC:758), so I could not read them.
- Depends on: S03-F28
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/DECISIONS.md:603` "The coordinator never merges alone, never tags or publishes, never answers a permission prompt, never interrupts a worker."
- Concerns: 655 line 98 also says that for THIS build no PR is merged by the orchestrator or a worker (each stops at green for the owner), which is consistent with the plan; the conflict is the later automatic merge.

## F. The work report (body line 55, 56)

### S03-F30 Work report state files, daily-run records and the report session live in the orchestrator repo
- 655 says: the work report and its state files and the daily run's records live in the orchestrator repo; the report state moves there (lines 54, 56, 167, 181).
- Status: NOT-COVERED
- Current plan: the plan decides the report layer (D11) but not where its state lives beyond "per-user configurable state path" (FR-46, SPEC:257; D11 VERDICT:34) and the report session names `coordinator`, `coordinator-`, `.dev/coordinator/` staying unchanged (FR-62, SPEC:319; D08 VERDICT:22). The one place the repo is discussed is an owner decision: D07 action "owner decides whether to keep it for the report session | DECISION | Not blocking" (D07 VERDICT:70). Searched: "IronOrchestrator", "report state", "state_dir", "report_state_dir" in SPEC.md, D07, D08, D11.
- Component: TUI-DASHBOARD: the report layer reads and writes these files and the observer reads the entry files (FR-44, SPEC:255).
- Feature statement: The owner records where the report session and its state and daily-run records live (a configured per-user path or a named repo), and the report reads and writes only that path.
- Done when: the report's `config.json` state path points to the chosen location on a fresh host with no hand edit, and a test shows no `"person"` or ClickUp ids in shipped config.
- Depends on: S03-F25, S03-F32
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:799` the daily run starts "a detached `python -m http.server 8765 --bind 127.0.0.1 --directory <.dev/coordinator>`, which serves the whole folder (`settings.json` with ClickUp user and DM channel ids, `action-log.jsonl`, run folders)".
- Concerns: SECURITY: that same line shows the report serves its whole state folder; moving state into a shared private repo would put it under a git commit by the model (Step 14, same line 799) and a local web server. FR-46 (SPEC:257) already requires removing person-specific config (`"person": "clayphi"`) from the shipped report.

### S03-F31 Work report integration: living report, `report-entry` the only writer, daily run no longer touches issue entries
- 655 says: the entry follows the item template, is added at claim, updated at milestones and removed at close; `superclaude orchestrator report-entry` writes it; the daily run no longer touches issue entries (lines 40, 94-96, 113; AC line 221 including a test).
- Status: COVERED
- Current plan: D11 (D11 VERDICT:34, 56: living report adopt with change, "no double reporting (`exclude.py`), no token cost"); FR-45 to FR-50 (SPEC:256-261); FR-48 (SPEC:259: `report-entry` only writer); FR-49 (SPEC:260: AU lines shown as waiting on a person); section 7 rows E1 to E7 (SPEC:464); S15c builds `report-entry` (SPEC:499); S16 observability glue (SPEC:500); existing test `skills/test_agent_work_report.py` (FR-50, SPEC:261). The exact milestone timing (added at claim, updated at milestones, removed at close) is classified under 655 section 7 by another analyst.
- Depends on: S03-F32, S03-F22
- Evidence from our documents: n/a (COVERED)
- Concerns: FR-45, FR-46, FR-48 are "blocked until the skill is restored" (SPEC:778). The report also sends a ClickUp DM and commits its state (D11 VERDICT:44), which the owner's rule keeps out of the sweep and observer. No recorded test says the daily run leaves entries alone beyond D11's `exclude.py` remark (UNVERIFIED as a test).

### S03-F32 `agent-work-report` skill moves into IronClaude (PR C)
- 655 says: the `agent-work-report` skill moves into IronClaude (lines 56, 167, 187).
- Status: COVERED
- Current plan: PR 684 already did the move; D11 adopts the skill with change (section 7 rows E1, E2, SPEC:464); PR 700 then removed it from master (Appendix B.1, SPEC:758); restoring it needs a later owner-approved PR (B.3 item 1, SPEC:786: "Decide whether to restore the PR 684 skill ... Yes: the D11 adoption of the living report proceeds from that PR. No: FR-45, FR-46 and FR-48 are dropped or rewritten").
- Depends on: none
- Evidence from our documents: n/a (COVERED in intent; the owner's yes or no is still open)
- Concerns: the effect on the plan is gated by that open owner answer. Fix text `agent-work-report/SKILL.md:12` still names `/sc:orchestrator` (D08 VERDICT:63).

### S03-F33 All skills live in IronClaude
- 655 says: all skills live in IronClaude (line 54; AC line 228).
- Status: COVERED
- Current plan: NFR-06 (SPEC:344: edit installed primitives under `src/superclaude/`, `make sync-dev`, `make verify-sync`); MC-9 (SPEC:478); FR-24 (SPEC:226); project `CLAUDE.md` rule on installed paths.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none.

## G. Closeout dependency, split and order, tests (body lines 57-58)

### S03-F34 Closeout is not part of this issue: `/sc:closeout` (issue 668) must merge before the live test
- 655 says: the closeout is its own issue #668, a dependency that must merge before the live test; wave 8 calls it after every merge; it closes only a done issue; the orchestrator runs no `gh issue close` (lines 57, 100; AC line 226).
- Status: COVERED
- Current plan: PR 683 (`/sc:closeout`) is already merged and KEEP (SPEC:392; D13 VERDICT:19, 38); FR-38 (SPEC:240: call `/sc:closeout <PR>` per merged PR; never as a worker); SEC-05 (SPEC:294); the live tests come after the skill stages (S17, SPEC:501), so the dependency is already met.
- Depends on: none
- Evidence from our documents: n/a (COVERED for the dependency itself)
- Concerns: the closing authority differs: the plan closes only under a person's per-PR go that names the close (SEC-12, SPEC:301; FR-38 "under a go naming the close"; OD-10, SPEC:106), while 655 lets `/sc:closeout` close by its own verdict. That is classified in 655 sections 2 and 7. Also `/sc:closeout`'s two `/sc:issue --plan` references only resolve when PR 690 merges (SPEC:392).

### S03-F35 Work split and order (PR D, A, P, B, C, E; PR B as ONE pull request after T1 to T13 pass)
- 655 says: build order is PR D (retire the plan-approval gate first), PR A (poll core with assignment-only discovery), PR P (plan mode), PR B (the whole skill as ONE PR: ten waves, refs, four templates, playbook, verbs, `limits.py`, `names.py`), PR C (move the report skill), PR E (fixtures, live-test record, runbook); the skill PR opens only after local end-to-end tests T1 to T13 pass, with their results in its description (lines 58, 167, 175-189; AC lines 217, 230).
- Status: CONFLICT
- Current plan: D14 and section 8 stages S0 to S17 (SPEC:482-501): S2 PR 690 first, S7 revert (done by PR 700), S9 planb, S11 PR 686 adapted, S13 substrate, S14 merge path plus `/sc:coordinator` command and skill, S15 split into four PRs (a to d), S16 observability, S17 live tests then enable; "one reviewable PR" per stage (SPEC:474). Conflicts: (1) PR D "retire the gate first" is rejected: PR 682 is reverted and PR 700 restored the code (SPEC:336, 758; D03 VERDICT:9); (2) PR A's assignment-only discovery is rejected (S03-F17); (3) PR B as one PR with all waves is rejected: the plan splits it into S13, S14 and four S15 PRs; (4) the rule that live end-to-end tests pass before the skill PR opens is reversed: the plan puts live tests at S17 after S14 to S16 and before enabling the poll. PR P before B and PR C are consistent (S03-F18, S03-F32). The live-test dependency on #668 is covered (S03-F34). Stage-by-stage coverage is classified under 655 sections 12 and 13.
- Depends on: S03-F17, S03-F18, S03-F32, S03-F34, S03-F36
- Evidence from our documents: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/VERDICT.md:11` "the owner's rules decide what lands and in what order (PR 682 reverted, PR 686 never merged as it stands)". Also SPEC:499 "S15 ... four PRs".
- Concerns: after PR 700 the order is partly moot (S6 and S7 done, S10 waits on the design-text decision, Appendix B.3 items 2 and 4); OA-1 and OA-2 (who adapts PRs 686 and 690) are still unanswered (SPEC:555).

### S03-F36 Tests: the local end-to-end plan T1 to T13 and what each proves
- 655 says: tests T1 to T13 run locally with throwaway issues and PRs in more than one repo across both orgs (IronbellyOrg and IronbellyGroup), results in the PR description (line 193-209; AC line 217).
- Status: COVERED
- Current plan: D15 G1 "Test plan T1 to T13 with U and K registers" adopt with change (D15 VERDICT:129; SPEC:467: T1, T3, T4, T8, T10, T11 logic rewritten, T12 for hand-back); plan's own T13 `tests/coordinator/test_merge_path.py` (SEC-01 to SEC-03, SPEC:290-292); the live firing tests of 13.2 (SPEC:698-713), including the merge-path rehearsal and worker binding probes.
- Depends on: S03-F35
- Evidence from our documents: n/a (COVERED)
- Concerns: (1) label clash: the plan's T13 is the merge path, 655's T13 is audit and merge-safety hold (body line 209); (2) six of the 655 T-rows must be rewritten because they assume assignment-only start, a registry repo, or the lease (D15 VERDICT:241); (3) no plan row tests across two GitHub orgs; the plan's live tests use "throwaway issue and repo" (SPEC:706) and org-wide search is off (FR-09, SPEC:199), so T1's cross-org claim is UNVERIFIED as covered; (4) all tests marked NEW are proposals not yet run (SPEC:692).

## Section summary
- The core deliverables of 655 section 3 map onto the plan with renames and removals: the skill, verbs, `refuse(argv)`, naming check, plan mode, report layer, closeout and tests are covered; the names, the `lease` verb, permission-prompt approval, the Orca-automation scheduler, the `hold:plan` label write, the fixed 62-name table, the removal of the approval gate and the IronOrchestrator repo with its `repos.yaml` are rejected by D01, D02, D03, D07, D08, D09/Q03, D15 and OD-7/OD-8.
- Remaining features to turn into issues: the one-hour plan request (WATCHER, deferred by A4), the handoff template's nine sections and `Fixes`/`Refs` rule (COORDINATOR), the worker check-in template (COORDINATOR), a test per template (COORDINATOR), the per-repo overview (COORDINATOR), the IronFlow spec upkeep (OTHER) and the home of the report state (TUI-DASHBOARD, an open owner decision at D07:70).
- Biggest unknowns: the IronFlow coordinator spec was never read by any debate (FR-13, FR-23 to FR-25 cited from it are UNVERIFIED), PR 700 removed the report skill and the design doc so FR-45, FR-46, FR-48 wait on the owner (Appendix B.3), and OA-1 (do both gates stay) is unanswered.
- Numbering trap for builders: 655's "FR-23/FR-24" and "T13" are not the plan's FR-23/FR-24/T13.
