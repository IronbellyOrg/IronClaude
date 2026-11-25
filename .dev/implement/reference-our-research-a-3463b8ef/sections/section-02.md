# Section 02 analysis: The orchestrator's runtime workflow (waves 0 to 9)
Counts: COVERED 25, CONFLICT 13, NOT-COVERED 17 (55 feature rows, S02-F1 to S02-F55)

Source: issue 655 body lines 31-47 (the wave table) plus acceptance criteria at lines 215-229 that touch it. Current plan = SPEC.md, DECISIONS.md, verdict files and FOLLOW-UPS.md under /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/. In this file "SPEC" means spec/SPEC.md and "D15" etc. mean debates/D15/VERDICT.md. The plan says "coordinator"; 655 says "orchestrator"; they are matched as one role. Verified locally (read-only help output): `orca orchestration` has run-create, run-use, task-create, worker-start (--task, --spec, --worktree path:..., --agent), worker-show, worker-read, worker-release, worker-retain, worker-list --terminal-state reclaimable, gate-create, gate-resolve, request-show; `orca reference` has add and find; `orca skills get` exists.

## Skill structure (body lines 33-34, acceptance line 217)

### S02-F1 Ten numbered waves, each with its own ref file loaded only at that wave
- 655 says: `SKILL.md` carries the workflow as waves 0 to 9; each wave has a ref (`refs/<name>.md`, loaded only at that wave), its commands, its template and the check that ends it (body lines 33-35; acceptance line 217).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, all debates/*/VERDICT.md, FOLLOW-UPS.md, STATE.md for "refs/", "wave", "waves" and "SKILL.md". The plan fixes only the skill name, command and flags (FR-24, SPEC.md:226) and a 10-step flow diagram (SPEC.md:144-158) that is not a wave/ref layout. Interface row 8 says the skill is "NOT BUILT" (SPEC.md:178).
- Component (NOT-COVERED only): COORDINATOR (the skill `sc-coordinator-protocol` is the coordinator's own instruction set)
- Feature statement (NOT-COVERED only): Lay out `sc-coordinator-protocol/SKILL.md` as numbered waves, each with a `refs/<name>.md` loaded only at that wave, naming its commands, template and ending check.
- Done when (NOT-COVERED only): `SKILL.md` lists every wave with ref, commands, template and ending check, and a test fails if a ref named in the table is missing.
- Depends on: S02-F2 (names); 655 section 3 deliverables and section 4 templates; the other S02 wave rows supply the content.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:134 `| G6 | The design text (PR 681) | Adopt with change | Source of verb and wave detail; not shown to be owner-approved on GitHub |`. The wave detail lives in Clay's design text, which PR 700 removed from master (SPEC.md:758, Appendix B).
- Concerns: the plan treats the 681 design text as unapproved source material, so each wave row must be re-checked against the verdicts below before it is built. The design doc is on the archive branch only (SPEC.md:759).

### S02-F2 Names: skill `orchestrator`, command `/sc:orchestrator`, verbs `superclaude orchestrator ...`
- 655 says: every wave names `Skill sc:issue-protocol`, `superclaude orchestrator report-entry|merge-gate|audit|handback` and an "orchestrator" role (body lines 37-45).
- Status: CONFLICT
- Current plan: FR-24 (SPEC.md:226) "no `commands/orchestrator.md`, no `sc-orchestrator-protocol`"; FR-26 (SPEC.md:228) one verb group `superclaude coordinator`; FR-62 (SPEC.md:319); FR-63 (SPEC.md:320) renames `superclaude orchestrator ...` verbs before PR 686 merges; decision D08 (SPEC.md:84). 655's names are REJECTED; the behaviors are judged row by row below.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/VERDICT.md:33 `WORKER-CONTRACT has 80 lines with "coordinator" and 0 with "orchestrator"; Orca's orchestration skill has Coordinator and Handoff owner roles and no Orchestrator role`.
- Concerns: the verb list differs: FR-26 lists wake-check, wake-ack, state, plan-check, repos, merge, merge-gate, answer-check, audit, report-entry, escalate, handback (12 verbs, no interrupt); 655 wave rows use only report-entry, merge-gate, audit, handback of those.

### S02-F3 Escalation can end any wave
- 655 says: at any wave the orchestrator fills the escalation template and waits (body line 33); hand-back stops and failed starts are "row 9" (lines 41, 45).
- Status: COVERED
- Current plan: FR-26 verb `escalate` (SPEC.md:228); FR-37 write first, send nothing if refused (SPEC.md:239); FR-47 nine-row table in the notice step only (SPEC.md:258); decisions D15 D16 and OD-4 (SPEC.md:100). The template file itself is section 4 of 655 (not classified here).
- Concerns: the plan has no push notice in the first build (OA-25a, SPEC.md:113; SEC-21, SPEC.md:310); "waits" means an entry line marked "waiting on a person", not a message.

## Wave 0, Intake (body line 37)

### S02-F4 Load Orca's own `orchestration` skill at run time
- 655 says: wave 0 runs `orca skills get orchestration` and the skill cites it instead of copying it (body line 37; line 88; acceptance line 220).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, verdict files, merged-requirements.md and STATE.md for "skills get orchestration", "orchestration skill", "loads Orca". Only D08 mentions that Orca's skill exists (roles Coordinator and Handoff owner).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): At wave 0 the coordinator skill loads the version-matched Orca `orchestration` guide with `orca skills get orchestration` and follows its supervised loop and completion accounting.
- Done when (NOT-COVERED only): the coordinator's wave 0 ref names that command and a test or run shows the guide loaded before the first `worker-start`.
- Depends on: S02-F1.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/VERDICT.md:33 (Orca's `orchestration` skill has Coordinator and Handoff owner roles and no Orchestrator role). Local check: `orca skills get` exists (help output).
- Concerns: none beyond keeping the skill name "coordinator" (FR-62).

### S02-F5 Bind a Run: `run-create` once, `run-use --id <run>` after a restart
- 655 says: one Run per orchestrator; `run-create` once, `run-use` after a restart (body lines 37, 86).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, all VERDICT.md, merged-requirements.md, techref for "run-create", "run-use", "orchestration run". FR-34 restarts a dead coordinator with a resume wake (SPEC.md:236) but never says how it re-binds the Run. D04 assumes `worker_done` arrives "on the Run mailbox".
- Component (NOT-COVERED only): COORDINATOR (the per-project session owns its Run)
- Feature statement (NOT-COVERED only): The coordinator creates an Orca Run on first start, stores its id in its per-issue/state records, and on `--resume` runs `run-current` and `run-use --id <run>` before any mutation.
- Done when (NOT-COVERED only): a kill-and-restart test of the coordinator ends with `orca orchestration run-current` showing the same Run and a following `worker-start` not failing with `consumer_fenced`.
- Depends on: S02-F4; FR-34 restart (plan).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:668 `U5 mailbox from outside a Run` listed UNVERIFIED; /home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/orca-coordinator-rebind-after-resume.md:10 `every orchestration mutation (worker-start etc.) fails with consumer_fenced until orca orchestration run-use --id <run_id> rebinds the Run`.
- Concerns: UNVERIFIED in the plan whether a mailbox send reaches a worker from outside a Run (U5).

### S02-F6 Read the wake; take only wakes addressed to itself; refuse any other
- 655 says: wave 0 reads the wake and takes every issue of its own wake; a wake for another orchestrator is refused (body line 37; acceptance line 216).
- Status: COVERED
- Current plan: FR-28 "take only wakes addressed to itself", pulled at every `check --wait` return (SPEC.md:230); wake format and files FR-13 (SPEC.md:203) and interface row 5 (SPEC.md:175); D10 (SPEC.md:86).
- Concerns: the plan has one coordinator per project, so "addressed to itself" means the project folder, not 655's `target` field of the registry (D07 VERDICT.md:78 says the `target` field assumes the registry and changes).

### S02-F7 Check each issue's repo against the orchestrator repo's list
- 655 says: wave 0 checks each issue's repo against the list kept in the orchestrator repo (body line 37; also line 28).
- Status: CONFLICT
- Current plan: D07 (SPEC.md:83) "no registry repository"; FR-11 (SPEC.md:201) cron calls `run-all` over `orca repo list`, no registry repository, no `repos.yaml`; FR-20 (SPEC.md:210) removes `registry_invalid` and `repo_not_listed`; FR-67 (SPEC.md:324) `owner/name` keys, a duplicate short name is a `name_collision` skip; a missing checkout is a `no_checkout` skip. 655's check is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md:16 `No registry repo. The spec removes the separate IronbellyOrg/IronOrchestrator repo, ... the hand-kept repos.yaml allow list ... and the wrong_target refusal`.
- Concerns: the same decision removes `repos.yaml` as the place for merge method, reviewers and merge-safety files; those values survive as the `merge` block of per-repo JSON (see S02-F47).

### S02-F8 Every wake issue gets a repo, a checkout and a state (new, already claimed, or skipped with a reason); state saved before the ack
- 655 says: wave 0 ends when every issue in the wake has a repo, a checkout and a state; for a plan request the plan record is written first and the acknowledgment second (body line 37).
- Status: COVERED
- Current plan: FR-29 adopt a claim by exclusive create of `issues/<repo-key>__<N>.json`, then ack (SPEC.md:231); FR-15 ack only if the state file matches (M1, SPEC.md:205); ack buckets accepted, skipped, rejected (interface row 5, SPEC.md:175; FR-19, SPEC.md:209); skip reasons `no_checkout`, `name_collision`, `coordinator_full` (FR-20, SPEC.md:210); FR-03 no wake for a claim the poll did not launch (SPEC.md:193).
- Concerns: none.

### S02-F9 Plan request: read the issue live, write the plan record, then ack, then call `/sc:issue --plan`
- 655 says: on a plan request wave 0 reads the issue live, writes the plan record first and the acknowledgment second, calls `Skill sc:issue-protocol --plan <N> --depth <d>`; the wave ends with the body passing the plan check or an escalated failure (body lines 25, 37; acceptance line 219).
- Status: NOT-COVERED
- Current plan: the plan request itself is DEFERRED, not decided against. D15 row A4 "Defer ... Not built now; if built, ids only and after D07 settles who plans" (SPEC.md:442, D15 VERDICT.md:44). The plan does adopt the `--plan` command (FR-53, SPEC.md:274), the `plan_depth` key (FR-59, SPEC.md:280) and the grant `issue.body.append_plan_sections` (SEC-07, SPEC.md:296), and the same plan call in hand-back (FR-35).
- Component (NOT-COVERED only): COORDINATOR (consumes the request); the one-hour trigger that produces it is WATCHER and belongs to 655 section 1
- Feature statement (NOT-COVERED only): When a wake carries a plan request (ids only), the coordinator reads the issue live, saves the request state, acknowledges, runs `/sc:issue --plan <N> --depth <plan_depth>` and ends only when `plan-check` passes or the failure is escalated.
- Done when (NOT-COVERED only): a wake with a plan request for a plan-less fixture issue ends with a passing `plan-check` on the body, or an escalation entry, and the state file written before the ack.
- Depends on: 655 section 1 hold and one-hour plan request (watcher side); FR-53 and FR-59 (plan); S02-F8.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/VERDICT.md:21 `The one-hour plan request is a wake-file item, not a GitHub write. All three wait for the topology decision D07.`; D01 VERDICT.md:16 `any body edit after the approval voids it`.
- Concerns: a plan edit after the person's approval voids the approval (D01 item 5); the request must carry ids only, because titles are free GitHub text (D15 A4, D10 item 5).

## Wave 1, Claim (body line 38)

### S02-F10 The orchestrator itself runs the claim workflow (assign, accuracy check, summary, next steps, comments)
- 655 says: wave 1 runs `/sc:issue --claim <N> --pipeline none` from the orchestrator session (body line 38; acceptance line 218).
- Status: CONFLICT
- Current plan: in the plan the poll starts a separate claim session (`/sc:issue --claim <N> --pipeline none`, as master already does); the coordinator only adopts the finished claim: SPEC.md section 3.1 (SPEC.md:125), diagram steps (SPEC.md:140-147), interface row 4 (SPEC.md:174), FR-29 (SPEC.md:231), FR-21 (SPEC.md:211). The coordinator's `--take <owner/repo#N>` flag (FR-24) takes over by hand. 655's "coordinator claims" is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D04/VERDICT.md:60 `Keep the watcher launch prompt pinned to --pipeline none and its pattern test ... Clay's orchestrator wave 1 (D:544)`; SPEC.md:667 UNVERIFIED `Claim terminal lifetime; complete live-agent list; worker worktree path` (FR-70, FR-33, RK-7 SPEC.md:651: claim agent and standing coordinator share the `Coordinator` worktree).
- Concerns: moving the claim into the coordinator would remove the claim-agent worktree-sharing risk RK-7 but would also reopen decisions D01, D07 and the claim-evidence/delivery-intent save of FR-21. Not a builder choice; the owner would have to rule.

### S02-F11 Claim passes `--pipeline none`; never the claim's launch levels
- 655 says: the claim runs at `--pipeline none`; workers start only through `worker-start`, never through the claim's launch levels (body line 38; acceptance line 218).
- Status: COVERED
- Current plan: FR-51 exactly `--pipeline none` for every watcher or coordinator claim (SPEC.md:272); D04 (SPEC.md:80); FR-52 Pipeline field not read while `GOVERNED_LEVELS_ALLOWED` is false (SPEC.md:273).
- Concerns: none.

### S02-F12 Re-read the issue live before the claim: a plan must exist and no `hold:backlog`
- 655 says: wave 1 first re-reads the issue live (plan exists, no `hold:backlog`) (body line 38; acceptance line 219).
- Status: COVERED
- Current plan: FR-02 repeat every start gate at the moment of start (SPEC.md:192); FR-05 plan check and `hold:backlog` as read-only skips (SPEC.md:195); FR-08 at wake time re-check plan check and `hold:backlog` (SPEC.md:198); FR-54 one plan check function (SPEC.md:275).
- Concerns: the plan does this in the poll's start check and again at wake time, not in the coordinator's claim step (see S02-F10).

### S02-F13 Claim needs only the assignment (re-read omits approval, "unedited since" and the Status allow-list)
- 655 says: the claim path starts from assignment; the wave 1 live re-read lists only "plan exists, no `hold:backlog`" (body lines 24, 38; "Assignment stays the only trigger").
- Status: CONFLICT
- Current plan: FR-01 start only if open, assigned only to the watcher login, approved (field `Approved`=Yes) and unedited since, Status in Research/Spec/Plan/Debug, no `hold:backlog`, plan check passing; "Assignment alone never starts work" (SPEC.md:191); FR-02 (SPEC.md:192); decision D01 (SPEC.md:77); element A12 "assignment alone as trigger" REJECT (SPEC.md:447). 655's trigger rule is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/VERDICT.md:17 `Assignment alone may be reconsidered only when all four hold: the launch guard refuses to start when it is not effective ...; workers cannot push or merge ...; the watcher skips an issue that already has a claim record or worktree (MR-2); the owner records the reversal of R19 in chat.`
- Concerns: 655's own "conditions to revisit" are not met today (workers are unguarded, RK-1 and RK-2, SPEC.md:645-646).

### S02-F14 Wave ends when the "Claimed by" comment (marker `<!-- sc:issue:claim -->`) exists; a closed, held, otherwise-assigned issue or a PR stops with no write
- 655 says: end check is the claim marker comment plus a success report; stops with no write for a closed, held or otherwise-assigned issue, or a pull request (body line 38).
- Status: COVERED
- Current plan: FR-03 keep `marker_in_window` so a hand claim and a watcher start never run two workers (SPEC.md:193); interface row 4 marker (SPEC.md:174); FR-01 open, assigned only to the watcher login (SPEC.md:191).
- Concerns: the "a pull request is not an issue" stop is not named in FR-01 to FR-03 (not found in the lines read); UNVERIFIED whether the built poll already refuses a PR number.

### S02-F15 Each issue claimed once and its worker started once
- 655 says: each issue is claimed once and its worker started once (acceptance line 218).
- Status: COVERED
- Current plan: FR-03 (SPEC.md:193); FR-21 claim evidence and delivery intent in one store save, replay keeps the wake id, an unknown launch receipt never relaunches (SPEC.md:211); FR-29 exclusive-create adoption record (SPEC.md:231); FR-33 cap counts an issue once (SPEC.md:235).
- Concerns: none.

## Wave 2, Plan record (body line 39)

### S02-F16 Record `body_sha`, the sha256 of the issue body handed to the worker
- 655 says: wave 2 records the sha256 of the body it hands the worker, starts no agent; the wave ends when `body_sha` is recorded (body line 39).
- Status: NOT-COVERED
- Current plan: none found as a stored field of the per-issue state; searched SPEC.md, DECISIONS.md, VERDICT.md files, techref for "body_sha", "sha256", "body hash". Nearest: FR-04 "a body edit after approval voids it" and the `unchanged_since` check (SPEC.md:194; QG1 VERDICT.md:26). QG1 uses `body_sha` only as a recommended, UNVERIFIED carrier name in the waiting-hand-back step.
- Component (NOT-COVERED only): COORDINATOR (a field in the per-issue state file the coordinator owns)
- Feature statement (NOT-COVERED only): At worker handoff the coordinator stores the sha256 of the exact issue body given to the worker in `issues/<repo-key>__<N>.json`, so a later body change is detected.
- Done when (NOT-COVERED only): the state file of a started issue holds `body_sha` equal to sha256 of the body that was read at handoff, and a test shows a changed body gives a different value.
- Depends on: S02-F8 (state file); S02-F17.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/VERDICT.md:31 `Carrier (recommended, side effects UNVERIFIED): the state file takes status escalated with step handback_awaiting_approval(body_sha)`.
- Concerns: the plan's approval check already reads whether the body changed since approval (`unchanged_since`, `predicates.py:249-259`, QG1 VERDICT.md:26); a builder must not create a second, competing "unchanged" test.

### S02-F17 In a hand-back round, update the plan first with `/sc:issue --plan <N> --remaining <file>`
- 655 says: in a hand-back round wave 2 first updates the plan through `--remaining` before a new worker starts (body line 39; acceptance line 219, 226).
- Status: COVERED
- Current plan: FR-35 round 2 re-plans with `/sc:issue --plan <N> --remaining <file> --depth <d>` (SPEC.md:237); FR-53 (SPEC.md:274); QG1 item 2 (QG1 VERDICT.md:24-25); D15 row D18 (D15 VERDICT.md:102).
- Concerns: the plan inserts a person's re-approval after the re-plan; see S02-F52.

## Wave 3, Report entry added (body line 40)

### S02-F18 `report-entry` writes the issue's entry into the living work report at claim time
- 655 says: wave 3 adds the issue's entry to the living report with `superclaude orchestrator report-entry` (body line 40; acceptance line 221).
- Status: COVERED
- Current plan: FR-26 verb `report-entry` (SPEC.md:228); FR-48 `report-entry` is the only writer of an entry file (SPEC.md:259); D11 living report adopted with change (D11 VERDICT.md:34); element E7 (D15 VERDICT.md:115); interface row 10 (SPEC.md:180).
- Concerns: blocked today: PR 700 removed the `agent-work-report` skill from master and the owner has not decided whether to restore it (SPEC.md:771, 778, 786); FR-45, FR-46 and FR-48 "stay requirements" but are blocked. D11 VERDICT.md:89 says "entry creation at claim depends on D01 to D08".

### S02-F19 Entry content and lifecycle: human assignee, orchestrator and worker as links, last-update time; added at claim, updated at milestones only, removed at close
- 655 says: the entry shows the human assignee, the orchestrator, a follow-up state and a last-update time; updated only at milestones (plan done, blocked, PR opened, review summary, PR ready, merged) and removed at close (`report-entry --closed`); the daily run no longer touches issue entries (body lines 40, 45, 94-96; acceptance line 221).
- Status: NOT-COVERED
- Current plan: none found for the lifecycle rules (added at claim, milestone-only updates, removal at close, daily run stops touching issue entries); searched SPEC.md FR-41 to FR-50, FR-79 to FR-81, D11 and OAG2 verdicts, merged-requirements.md for "milestone", "entry removed", "--closed", "assignee". The plan fixes only who writes entries (FR-48), what the observer may show (FR-80) and the nine-row table (FR-47).
- Component (NOT-COVERED only): COORDINATOR (the coordinator calls `report-entry`; the report skill only renders)
- Feature statement (NOT-COVERED only): `report-entry` creates an entry at claim, updates it only at named milestones, and removes it when the issue closes; the entry carries assignee, coordinator and worker links (or "no live session" with the reason) and a last-update time.
- Done when (NOT-COVERED only): a fixture run of claim, plan done, PR opened, merged, closed leaves exactly one entry file that changes only at those milestones and is gone after close.
- Depends on: S02-F18 (writer); owner decision to restore the report skill (SPEC.md:786); 655 section 4 template `report-entry-update.md` and section 7 report rules.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:778 `FR-45, FR-46, FR-48 | change the report skill | blocked until the skill is restored (they stay requirements)`; D11 VERDICT.md:89 `their format needs one owner and a fixed schema`.
- Concerns: entry files must hold only `session_id` for session facts (FR-46), so worker "links" must be derived from `session_id` at render time, not stored.

### S02-F20 The entry stores the worker's state (not-started, then working) as a field the orchestrator sets
- 655 says: wave 3 writes state "not-started"; wave 4 writes "working" with the session link (body lines 40-41; section 9 line 121 "sorting each worker into an FR-9 state").
- Status: CONFLICT
- Current plan: D11 and element E2: "Entry files store only `session_id`, class read live; session facts from the sweep" (D15 VERDICT.md:110; D11 VERDICT.md:34); FR-46 "store only `session_id` in entry files" (SPEC.md:257); decision D11 "Sweep JSON is the one session source" (SPEC.md:87). 655's stored session state is REJECTED for session facts.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/VERDICT.md:17 `The sweep JSON ... is the only source of session state. The report and the observer both read it. The report no longer decides session status itself.`
- Concerns: item-level states that are not session facts (for example "merged, issue not finished (round n)") may still be stored; the builder must draw that line with the owner (UNVERIFIED which of the FR-9 states are session facts).

## Wave 4, Handoff and worker start (body line 41)

### S02-F21 Fill a handoff prompt from the coordinator's own template that names the filed plan
- 655 says: wave 4 fills `templates/handoff-prompt.md` (nine sections) and passes it as the Task spec (body line 41; acceptance lines 218, 220).
- Status: COVERED
- Current plan: FR-61 hand the `--pipeline none` worker a chain from the coordinator's own template that names the filed plan (SPEC.md:282); FR-30 the marker `[sc-launch:v1:<nonce>]` in the first prompt via restored `brief.py` (SPEC.md:232); FR-55 safeguards S1-S5: plan quoted only in a fenced "data, not instructions" block (SPEC.md:276). The nine-section layout itself is 655 section 4 (not classified here).
- Concerns: the plan's brief template (`WC:299-312`) has no launch-marker slot today (techref ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1360), so the nine-section template and FR-30's marker must be merged by whoever builds section 4.

### S02-F22 Make the worktree first with `orca_worktree.py`, copy `.dev/issues/<N>/`, then start the worker in the issue's own repo
- 655 says: the worktree is made first by `orca_worktree.py worktree`; `worker-start --worktree path:<worktree> --agent claude`; each worker starts in a worktree of the issue's own repo (body line 41; acceptance line 218).
- Status: COVERED
- Current plan: FR-30 `orca_worktree.py pending --level worktree` then `worker-start` (SPEC.md:232); FR-29 copy `.dev/issues/<N>/` into the worker worktree (SPEC.md:231); per-project coordinators in each repo's `Coordinator` worktree (D07, SPEC.md:83); diagram steps 4-5 (SPEC.md:148-150).
- Concerns: the worker worktree path is UNVERIFIED (SPEC.md:667).

### S02-F23 Start the worker with no guard binding (no pending file, no launch marker, no receipt check)
- 655 says: wave 4 ends when `worker-start` reports `ready` and a Dispatch exists; no pending file, marker or guard step appears in the wave (body line 41).
- Status: CONFLICT
- Current plan: FR-30 start every worker bound to the guard: `pending --level worktree`, marker in the first prompt, preflight, `pending/<nonce>` gone within a stated timeout (60 s proposed, UNVERIFIED) else stop and escalate; `WORKER_BINDING_PROVEN` (false) refuses a start outside `probe_issues` (SPEC.md:232); SEC-13 (SPEC.md:302); D05 (SPEC.md:81); D15 row D13 REJECT "workers run unbound, decided" (SPEC.md:458). 655's unguarded start is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:97 `D13 | DQ7 and K12 "workers run unbound, decided" | Reject the "decided"; adopt the K12 risk row and live-test record`; SPEC.md:645 `RK-1 | A worker-start worker cannot be bound; never observed | High`.
- Concerns: UNVERIFIED that `worker-start` delivers the task as a first prompt that fires the guard's hook with the marker intact (SPEC.md:666, S17 binding probe). Until proven, FR-30 refuses real issues.

### S02-F24 Create the Task, start the worker from it, link the issue and show the worker
- 655 says: `orca orchestration task-create --spec <filled handoff>`; `worker-start --task <id> ...`; `orca reference add` to link the issue to the worktree; `worker-show`; the session link goes into the entry (body line 41).
- Status: NOT-COVERED
- Current plan: none found for the Task/Dispatch/reference mechanics; searched SPEC.md, DECISIONS.md, VERDICT.md files, merged-requirements.md, techref for "task-create", "worker-show", "orca reference add", "Dispatch". The plan names only `worker-start` (FR-30, SPEC.md:232, diagram line 148).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): After the guard binding, the coordinator creates the Orca Task from the filled handoff, starts the worker with `worker-start --task`, attaches the issue with `orca reference add`, checks `worker-show`, and stores the Dispatch id in its state file.
- Done when (NOT-COVERED only): a fixture start shows a Task, a Dispatch in `ready`, the issue attached to the worktree (`orca reference list`) and the Dispatch id in `issues/<repo-key>__<N>.json`.
- Depends on: S02-F5 (Run), S02-F21, S02-F23.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1360 `no Python in src/ calls worker-start or task-create. Status: NOT BUILT`; same file line 1342 (WC-8, WC-13: a command or worker never calls `worker-start`, `dispatch`, `task-create`).
- Concerns: the worker contract bars commands and workers from `worker-start`, `dispatch` and `task-create` (WC-8, WC-13); FR-27 repeats "never `worker-start`" for a script-started coordinator. Only a person-opened or authorized coordinator session may run these.

### S02-F25 Unknown start outcome: check once, retry once, second failure is row 9
- 655 says: an unknown outcome of `worker-start` is checked once and retried once; a second failure is escalated (body line 41).
- Status: NOT-COVERED
- Current plan: none found for a worker-start retry; searched SPEC.md, verdicts for "retry", "unknown outcome". The plan's nearby rules point the other way: "an unknown launch receipt never relaunches" (FR-21, SPEC.md:211, claim launch only) and "stop and escalate" when the guard receipt is missing (FR-30).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): When `worker-start` returns an unknown outcome, the coordinator asks Orca whether that request took effect (`request-show`) once, retries only with the same request id, and escalates on the second failure.
- Done when (NOT-COVERED only): a fault-injected unknown `worker-start` never produces two Dispatches for one issue and the second failure writes an escalation entry.
- Depends on: S02-F24; S02-F3.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:211 `an unknown launch receipt never relaunches` (FR-21); local check: `orca orchestration request-show` and `worker-start --retry-request` exist (help output).
- Concerns: a blind retry could start two workers in one worktree; keep the plan's no-double-start principle (FR-21, FR-29).

### S02-F26 The worker runs `/sc:workflow` if needed, then `/sc:implement`
- 655 says: after start the worker runs `/sc:workflow` if needed and `/sc:implement` (body line 41).
- Status: COVERED
- Current plan: FR-55 claim rule C1: short chain `/sc:workflow` then `/sc:implement` when the plan passes (SPEC.md:276); FR-61 (SPEC.md:282).
- Concerns: none.

### S02-F27 The worker runs the regression gate before it reports done
- 655 says: the worker's chain includes "the regression gate" (body line 41).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, VERDICT.md files, merged-requirements.md and the techref for "regression gate" and "regression-gate" (no hits).
- Component (NOT-COVERED only): COORDINATOR (a line of the handoff template the coordinator fills)
- Feature statement (NOT-COVERED only): The handoff prompt names the repo's regression gate command and the worker must run it and report its result in `worker_done`.
- Done when (NOT-COVERED only): the handoff template contains the gate step and a fixture `worker_done` without a gate result is rejected by the coordinator.
- Depends on: S02-F21; S02-F38 (what a valid `worker_done` holds); 655 section 4 handoff template.
- Evidence from our documents: no evidence found in our documents.
- Concerns: "the regression gate" is not defined in the files read (UNVERIFIED what command or file it is).

### S02-F28 The worker pushes its own branch and runs `/sc:pr-submit --monitor 3`
- 655 says: the worker runs `/sc:pr-submit --monitor 3`; "the worker pushes its own branch and opens its pull request, never merges, never force-pushes" (body lines 41, 98; acceptance line 223).
- Status: CONFLICT
- Current plan: SEC-05 never run `/sc:pr-submit` or `/sc:closeout` as a `worker-start` worker (SPEC.md:294); FR-32 the coordinator commits after `worker_done`, a push needs a person's typed go in a person-opened session (SPEC.md:234); SEC-22 (SPEC.md:311); diagram step 6 "worker_done (no commit, push or PR command)" and step 8 (SPEC.md:151-156); decisions D06 (SPEC.md:82), Q04 (SPEC.md:96). 655's worker push and PR route is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:95 `ADD1's worker runs /sc:pr-submit | ... worker route: reject | a worker never runs /sc:pr-submit`; SPEC.md:646 RK-2 `A bound worker's own script pushes a feature branch, opens a PR ... carried, not solved`.
- Concerns: 655 body line 98 says that "for THIS build no pull request is merged by the orchestrator session or any worker" (the owner merges); that is consistent with the plan for merging but not for the worker's push and PR.

### S02-F29 No person approves the worker's plan between worker start and implementation
- 655 says: planning is done once at the issue; the worker then plans if needed and implements with no approval step in waves 4 and 5 (body lines 3, 41; Problem Statement line 13 "a plan-approval gate after the claim" is removed).
- Status: CONFLICT
- Current plan: FR-31 when both gates stay, record the plan approval, check it (`check-approval`) and write the worker's `.ok` file (W to WA) (SPEC.md:233); diagram step 5 (SPEC.md:149-150); D03 (SPEC.md:79); decision D14 (SPEC.md:90). 655's removal of the plan-approval gate is REJECTED by default. The owner question OA-1 "Do BOTH gates stay?" is still open in chat (SPEC.md:554; Appendix B.3 item 4, SPEC.md:789).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/VERDICT.md:29 `Dependency (UNVERIFIED): whether the restored plan-approval flow (WC-17, deleted by PR 682) can serve as this gate; it exists only if the owner decides both gates stay (D14).`
- Concerns: if the owner answers OA-1 "only the start gate stays", this row flips to COVERED for waves 4 to 5 (SPEC.md:163, 505 section 8.3). PR 700 already restored the plan-approval code on master (SPEC.md:758, 776).

## Wave 5, Watching (body line 42)

### S02-F30 Handle worker messages from the Run mailbox: `check --wait`, `reply`, `send`, `ask`
- 655 says: wave 5 handles worker messages with `orca orchestration check --wait --types "worker_done,escalation,question"`, `reply`, `send`, `ask`, `worker-show`, `worker-read` (body line 42; section 8 line 111).
- Status: COVERED
- Current plan: D04 one supervised `worker-start` route with mailbox, one message handled once per id, check-ins, restart (D04 VERDICT.md:35, 40); D15 row D12 (D15 VERDICT.md:96); FR-28 pulls the wake folder at every `check --wait` return (SPEC.md:230); SEC-20 a bound worker's `send` and `ask` are one plain call, no `--to` (SPEC.md:309).
- Concerns: UNVERIFIED mailbox behavior from outside a Run (U5, SPEC.md:668).

### S02-F31 Check-ins by the coordinator itself on each running worker (the `--hourly` mode)
- 655 says: the orchestrator does every check-in itself for each running worker (body lines 42, 92; acceptance line 222).
- Status: COVERED
- Current plan: flag `--hourly` kept on `/sc:coordinator` (FR-24, SPEC.md:226; D08, SPEC.md:84; D08 VERDICT.md:43 "lift unchanged onto /sc:coordinator"); check-ins are part of the adopted supervised route (D15 VERDICT.md:96); FR-40 typing under four rules (SPEC.md:242).
- Concerns: what `--hourly` does is defined only in Clay's design text (D:133), which this analysis did not read and which PR 700 removed from master; UNVERIFIED that it means the worker status check. See S02-F32 for the rules the plan does not state.

### S02-F32 Worker status check rules: hourly by default, per running worker, Monday to Friday 24 hours a day, stops at `worker_done`, also reads the issue
- 655 says: the status check runs hourly by default (interval configurable), for each running worker Monday to Friday 24 hours, stops at its `worker_done`; it reads Orca state, checks in where needed, and reads the issue (closed, assigned elsewhere, edited by someone else); the entry changes only at milestones (body line 42; section 8 line 112; acceptance line 222).
- Status: NOT-COVERED
- Current plan: none found for the schedule, the weekday rule, the stop condition or the issue re-read; searched SPEC.md, DECISIONS.md, VERDICT.md files, merged-requirements.md and techref for "hourly", "Monday", "weekday", "every hour", "check-in", "milestone". Only the flag name `--hourly` is carried (S02-F31).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): `/sc:coordinator --hourly` runs a status check per running worker (Orca state, optional check-in, issue re-read) at a configurable interval, default hourly, Monday to Friday, and stops for a worker once its `worker_done` arrives.
- Done when (NOT-COVERED only): a fake clock test shows one check per running worker per interval on weekdays, none on Saturday or Sunday, and no check after `worker_done`.
- Depends on: S02-F31; S02-F38; S02-F19 (milestone-only entry updates); 655 section 8 (checks table).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:229-242 (FR-27 to FR-40 name no worker check cadence); WC-16 allows one coordinator sweep per 5 minutes (D11 VERDICT.md:43).
- Concerns: the status check must stay under the 5-minute sweep limit WC-16 and the typing rules of FR-40; the weekday-only rule leaves weekends unwatched (a design choice of 655, not of the plan).

### S02-F33 Type into a worker terminal for a check-in under safety rules
- 655 says: the orchestrator types check-ins into the worker terminal itself (body lines 42, 92; acceptance line 222 "refused on unsent typing or fresh output").
- Status: COVERED
- Current plan: FR-40 "Type into worker terminals only under the four typing rules (never approve a permission prompt)" (SPEC.md:242); D15 row D14 "Typing rules 1, 2, 3, 5 add conditions at no cost" (D15 VERDICT.md:98); FR-14 typing only into an idle session with empty draft and 60 s quiet (SPEC.md:204, UNVERIFIED live U5, U25).
- Concerns: none.

### S02-F34 Approve a worker's permission prompts under Clay's FR-24 rules ("always allow" never sent)
- 655 says: the orchestrator approves a permission prompt when the action is not in rows 1 to 7, typing and approvals included (body lines 42, 92, 121; acceptance line 222).
- Status: CONFLICT
- Current plan: FR-40 "never approve a permission prompt" (SPEC.md:242); D15 row D14 "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases" (D15 VERDICT.md:98); coordinator summary "never answers a permission prompt" (D15 VERDICT.md:238; DECISIONS.md:603). 655's approvals are REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:238 `It never merges alone, never tags or publishes, never answers a permission prompt, never interrupts a worker.`
- Concerns: QG4 corrected the reading of WC:137 (it scopes answer typing, not a ban; QG4 VERDICT.md:25, 34) but kept the rejection on other grounds, so do not cite line 137 as the reason.

### S02-F35 The playbook (a file in the skill) for unsticking a worker
- 655 says: the orchestrator applies the FR-23 playbook (a file in the skill) to unstick workers, together with the permission rules (body lines 42, 50, 92, 121).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, VERDICT.md files, merged-requirements.md, techref for "playbook" and "unstick" (no hits). The plan's only text on this is D15 row D14 which removes the approval rules and tests.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): Provide a coordinator playbook file that maps each stuck-worker state (stalled, asking, errored, idle) to one allowed response, with no permission-prompt approvals.
- Done when (NOT-COVERED only): the file exists in the skill's refs, each stuck state maps to an action that is on the "may do" list, and a test fails if the file contains a permission-approval step.
- Depends on: S02-F34 (approvals removed); S02-F33; the "may do / may never do" lists of 655 section 9.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/VERDICT.md:63 `Fix agent-work-report/SKILL.md:12 ("The orchestrator (/sc:orchestrator) does every check-in itself") | PR KEEP-ADAPT`; D15 VERDICT.md:98 (approval rules dropped).
- Concerns: the playbook's text is not in the files read (it is in Clay's IronFlow spec FR-23); UNVERIFIED which of its entries approve prompts and must be cut.

### S02-F36 Orca decision gates (`gate-create`, `gate-resolve`) to hold a task for a human answer
- 655 says: wave 5 (and wave 7) use `gate-create` and `gate-resolve` for waits on a person (body lines 42, 44, 86).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, VERDICT.md files, merged-requirements.md, techref for "gate-create", "gate-resolve" (no hits). The plan carries every approval and go in the owner's chat, recorded by an agent: SEC-08 (SPEC.md:297), SEC-14 (SPEC.md:303), memory rule "Approvals through chat, never files".
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator may open an Orca decision gate to park a task while it waits for a person, but a gate can never itself carry an approval.
- Done when (NOT-COVERED only): a test shows `gate-resolve` alone does not satisfy `answer-check` or a merge go; only a recorded chat go does.
- Depends on: S02-F44; SEC-08 and SEC-09 (plan).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:297 `Accept a recorded go only with the owner's quoted words ... typed by a person in their own session, never relayed`; RK-3 `answer-check cannot tell a person from a script` (SPEC.md:647).
- Concerns: owner rule: every approval is given in chat and never in a file or another channel (SPEC.md:303). Resolving a gate in Orca could be script-typed and would not meet SEC-08 as a go.

### S02-F37 The one interrupt exception (acceptance "except the one interrupt")
- 655 says: check-in typing is refused on unsent typing or fresh output "except the one interrupt" (acceptance line 222; also line 225).
- Status: CONFLICT
- Current plan: OD-7 "No interrupt of a running worker" (SPEC.md:103); FR-40 "never interrupt a worker" (SPEC.md:242); FR-26 "no lease, no interrupt" (SPEC.md:228); D15 row D9 REJECT (D15 VERDICT.md:93). 655's interrupt is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:93 `No incident cited; Orca gives no receipt (U40); a nudge would undo it (G-6)`.
- Concerns: none.

### S02-F38 A valid `worker_done` (and every milestone in the entry) ends the wave
- 655 says: the wave ends when the worker sent a valid `worker_done`, or it was escalated and the human answered; every milestone reached is in the entry (body line 42; Orca "a valid worker_done settles the Task", line 88).
- Status: NOT-COVERED
- Current plan: the plan relies on `worker_done` (diagram step 6, SPEC.md:151; FR-83, SPEC.md:243 reads a "succeeded worker_done"; merge-gate reason `worker_not_done`, D06 VERDICT.md:16) but none found that defines what makes a `worker_done` valid; searched SPEC.md, D04 and D06 verdicts, techref for "worker_done" fields.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): Define and check the fields of a valid `worker_done` (outcome word, paths, PR number or branch, regression-gate result) before wave 5 ends and before any merge-gate or closeout step relies on it.
- Done when (NOT-COVERED only): a table-driven test accepts a well-formed fixture `worker_done` and rejects a missing outcome, a missing result or a message sent twice.
- Depends on: S02-F30; S02-F27; FR-83 (plan).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:243 FR-83 `after it reads a succeeded worker_done or a launched agent's result.md`; SPEC.md:677 UNVERIFIED `PR 693's result file path and shape`.
- Concerns: UNVERIFIED shape of both `worker_done` and the launched agent's `result.md`.

## Wave 6, Pull request watch (body line 43)

### S02-F39 Readiness test on the final head: checks green, review agents finished, no open thread, no `changes_requested`, no merge-safety hold, `worker_done` received (the `merge-gate` verb)
- 655 says: wave 6 decides readiness with `superclaude orchestrator merge-gate` (13 closed reasons); it ends when all of those hold on the final head (body line 43; acceptance line 223).
- Status: COVERED
- Current plan: FR-26 verb `merge-gate` (SPEC.md:228); SEC-02 read-only `merge-gate` (13 closed reasons plus "no recorded merge go") run before the go and again before the merge (SPEC.md:291); D06 item 3 lists the reasons including `checks_pending`, `review_pending`, `threads_open`, `changes_requested`, `worker_not_done`, `merge_safety`, `head_moved` (D06 VERDICT.md:16); decision D06 (SPEC.md:82).
- Concerns: the gate is design only; "`merge-gate`, `answer-check`, `E-NO-GRANT` exist nowhere" (SPEC.md:674 UNVERIFIED, to be re-checked before S14).

### S02-F40 A review agent that does not run or finish holds the pull request
- 655 says: every review agent the repo lists (Augment, Codex) must have finished on the final head; one that does not run or finish holds the PR and escalates; `reviewers: none` means no hold (body lines 43, 98; acceptance line 223).
- Status: COVERED
- Current plan: SEC-04 merge-time hold: owner-set `reviewers` list (`none` an explicit exception), re-request on the final head, wait 60 minutes (UNVERIFIED, owner-settable), then escalate; `review_stalled`, `review_none_present` not overridable (SPEC.md:293); OA-13b (SPEC.md:111); D15 row D3 (D15 VERDICT.md:87).
- Concerns: the 60-minute value is UNVERIFIED (SPEC.md:676).

### S02-F41 Reuse the `superclaude.pr_submit` core and the poll scripts to read CI and review state
- 655 says: readiness reuses the `superclaude.pr_submit` core, `scripts/poll-ci-checks.sh` and `scripts/poll-augment-review.sh` (body lines 43, 98).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, VERDICT.md files and techref for "poll-ci-checks", "poll-augment-review", "pr_submit core". The plan fixes what `merge-gate` refuses (SEC-02) but not what data source it reads. The plan keeps `/sc:pr-submit` itself with a person (FR-32, SEC-05, SEC-22).
- Component (NOT-COVERED only): COORDINATOR (a read-only helper behind the `merge-gate` verb)
- Feature statement (NOT-COVERED only): `merge-gate` gets its check, review and thread state from the existing `superclaude.pr_submit` helpers and poll scripts, read-only, without running `/sc:pr-submit` itself.
- Done when (NOT-COVERED only): a fixture PR state produces the same reason list from `merge-gate` as from the pr_submit helpers, and a test shows the gate never calls a push, comment or fix command.
- Depends on: S02-F39.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:674 `merge-gate, answer-check, E-NO-GRANT exist nowhere (searched src/ of three exports)`. Local check: `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`, `poll-augment-review.sh` and `src/superclaude/pr_submit/ci.py`, `reviewers.py` exist in this checkout.
- Concerns: SEC-04 says keep `/sc:pr-submit`'s silent-reviewer skip in its loop and add the merge-time hold separately; reusing the skip rule inside the gate would defeat the hold (D15 row D3: the skip rule loses a late reviewer).

### S02-F42 An already merged pull request goes straight to wave 8
- 655 says: if the PR is already merged (by anyone), wave 6 jumps to wave 8 (body line 43; line 100 "including a merge made by a person").
- Status: COVERED
- Current plan: FR-38 each cycle call `/sc:closeout <PR>` per merged PR (SPEC.md:240); D13 (SPEC.md:89); D15 row D15 "Keep after a go as well" for the audit (D15 VERDICT.md:99); row F1 closeout is a coordinator step after a merge (D15 VERDICT.md:120).
- Concerns: none.

## Wave 7, Merge (body line 44)

### S02-F43 The orchestrator merges on its own when wave 6 ended clean
- 655 says: wave 7 merges when wave 6 ended clean; "only the orchestrator merges" (body lines 44, 121 "merging when every merge condition holds"; acceptance line 223).
- Status: CONFLICT
- Current plan: SEC-01 merge only on a person's typed go naming repo, PR, full 40-character head sha, method, the word "merge" and the gate output; "A passing gate never triggers a merge" (SPEC.md:290); SEC-06 no standing `pr.merge` (SPEC.md:295); decision D06 (SPEC.md:82); D15 row D7 "Standing pr.merge and issue.close; autonomous merge (DQ8, R10, wave 7) | Reject" (D15 VERDICT.md:91). 655's autonomous merge is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/VERDICT.md:76 `What breaks. Clay's wave 7 autonomous merge, ADD1's worker flow, K7's "merge when every condition holds"`; D06 VERDICT.md:65 `its wave 7 asks for a go instead of merging`; SPEC.md:646 `master unprotected` (RK-2).
- Concerns: 655's own body line 98 says that for THIS build no PR is merged by the orchestrator or any worker and the owner merges; that matches the plan for the first build. The go has no clock expiry in the first build (OA-13a, SPEC.md:110).

### S02-F44 A failing check, or a merge-safety file change, waits for an explicit human OK; an unreadable file list is a hold
- 655 says: a failing check waits for the human's explicit OK; a merge-safety file change waits for Clay's OK for that head; the OK is tied to a question key (body lines 44, 98; acceptance line 223, 227).
- Status: COVERED
- Current plan: SEC-03 a go never overrides the eleven refusal reasons; only `checks_failing` and `merge_safety` may be overridden, each with its own key (SPEC.md:292); SEC-08 question key `merge_safety:<PR>:<head sha>` (SPEC.md:297); D06 item 2 fail-closed file list (D06 VERDICT.md:15); `merge_safety_files` per-repo with SEC-10 (SPEC.md:299).
- Concerns: 655 waits through an Orca gate (`gate-create`, body line 44); the plan requires a typed chat go recorded by an agent (SEC-08, SEC-14); see S02-F36.

### S02-F45 `changes_requested` is never merged
- 655 says: a pull request at "changes requested" is never merged, no recorded OK overrides it (body lines 43-44, 98; acceptance lines 223, 227).
- Status: COVERED
- Current plan: OA-13c "`changes_requested` stays a hard refusal" 95% (SPEC.md:112); SEC-03 (SPEC.md:292); D15 row D2 adopt as is (D15 VERDICT.md:86).
- Concerns: none.

### S02-F46 Merge command: `gh pr merge --match-head-commit`, pinned to the issue's own repo, never `--auto`, `--admin`, `--delete-branch`; confirm merged afterwards
- 655 says: `gh pr merge --match-head-commit` pinned to the issue's repo; the wave ends when `gh` shows the PR merged (body line 44; line 98 "Every gh call is pinned to the issue's own repo").
- Status: COVERED
- Current plan: SEC-02 `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>`, never `--auto`, `--admin`, `--delete-branch` (SPEC.md:291); RK-12 head-pinned argv and "reconcile the exact head" after an uncertain result (SPEC.md:656); D06 item 2 "After a restart the PR state is read first" (D06 VERDICT.md:15); project rule: `--repo IronbellyOrg/IronClaude` on every gh call.
- Concerns: none.

### S02-F47 Merge method comes from the repo's own settings (`merge_method`, `release_merge_method`)
- 655 says: the repo's own merge method from `repos.yaml` (body line 44; line 98: IronClaude squashes ordinary PRs and merges a release PR with a merge commit).
- Status: COVERED
- Current plan: the values are adopted, the place is not: an optional `merge` block in the per-repo JSON with `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`, read at merge time (D07 VERDICT.md:19; FR-12, SPEC.md:202); SEC-01 the go names the method (SPEC.md:290). `repos.yaml` itself is rejected (see S02-F7).
- Concerns: `can_merge` and the safety list are overridden by the live GitHub role at merge time, because the config directory is not tamper-protected (D07 VERDICT.md:19); SEC-10 protects these keys from the coordinator's own writes (SPEC.md:299).

## Wave 8, Close, closeout, audit, drop the entry (body line 45)

### S02-F48 Run `/sc:closeout <PR>` after a merge; it decides "done" from the issue's own criteria
- 655 says: wave 8 runs `Skill sc:closeout-protocol <PR>`, which decides whether the issue is done by its own criteria, not by `Fixes`/`Closes` words (body lines 45, 100; acceptance line 226).
- Status: COVERED
- Current plan: FR-38 `/sc:closeout <PR>` per merged PR, never as a worker (SPEC.md:240); element F1 `/sc:closeout` adopt as is (D15 VERDICT.md:120); D13 (SPEC.md:89); SEC-05 (SPEC.md:294).
- Concerns: none.

### S02-F49 Closeout closes the issue when done, with no per-PR go naming the close
- 655 says: `/sc:closeout` "closes it only then" (when done); the orchestrator runs no `gh issue close` (body lines 45, 100; acceptance line 226).
- Status: CONFLICT
- Current plan: SEC-12 one per-PR go ("merge PR N at sha X, then close issue M if closeout's verdict is done") covers merge and close; no standing close; a restart reads the recorded go (SPEC.md:301); SEC-06 refuses `issue.close` as a grant (SPEC.md:295); FR-38 closeout "under a go naming the close" (SPEC.md:240); OD-10 (SPEC.md:106). 655's close without that go is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:143 `C-INV-4 (INV-004). The post-merge close has a stated authority (go entry covers it, or an explicit closeout grant recorded in chat); the Fixes line bypass is stated as a limit.`; SPEC.md:654 RK-10 `Closeout or a Fixes line closes unfinished work`.
- Concerns: a `Fixes` line still closes an issue at merge; the plan states that as a limit (SEC-12), and 655 admits the same (K28, body line 100).

### S02-F50 Audit after a pull request lands: eight checks, no model, no GitHub write, result into the entry
- 655 says: `superclaude orchestrator audit` runs AU1 to AU8 on the landed PR, whoever merged it; the result goes into the entry; AU4a, AU4c, AU5 reach the person (body lines 45, 104; acceptance line 227).
- Status: COVERED
- Current plan: FR-36 audit AU1 to AU8 with AU5 narrowed to conflict-marker lines, and a statement that it cannot see a push with no PR (SPEC.md:238); FR-26 verb `audit` (SPEC.md:228); FR-49 AU4a, AU4c, AU5 shown as entry lines marked "waiting on a person", push notice reserved (SPEC.md:260); D15 row D15 (D15 VERDICT.md:99); OD-5 (SPEC.md:101).
- Concerns: 655 says these three "reach Clay (row 8)"; the plan shows them as entry lines first and sends no push notice in the first build (OA-25a, SPEC.md:113). AU5 as written in 655 is wider than the plan's narrowed form.

### S02-F51 Hand-back loop: `handback` verb, at most 3 hand-backs, stop when nothing progressed, old worker final first, each stop escalated
- 655 says: a not-done issue goes back through waves 4 to 9; `handback` bounds it at 3 hand-backs and stops when a round leaves the same unmet criteria; the old worker must be final (`worker_done` received) and released first; a stop or failed re-plan is row 9 (body lines 45, 102; acceptance line 226).
- Status: COVERED
- Current plan: FR-35 hand-back loop: stop on empty list, `HANDBACK_MAX` 3 "not measured", `no_progress`; old worker final first; idempotent re-plan marker (SPEC.md:237); FR-26 verb `handback` (SPEC.md:228); D15 row D18 (D15 VERDICT.md:102); QG1 "Clay strengths to adopt" (QG1 VERDICT.md:52).
- Concerns: `HANDBACK_MAX` 3 is UNVERIFIED (SPEC.md:676); D15 C-INV-1 and C-INV-2 conditions apply (D15 VERDICT.md:140-141).

### S02-F52 The hand-back starts the new worker without a person's re-approval and keeps the issue "in flight"
- 655 says: after the re-plan the orchestrator starts a new worker; "the issue stays in flight" (body lines 45, 102).
- Status: CONFLICT
- Current plan: FR-35 round 2 re-plans, then enters `waiting_reapproval` (outside the cap, a visible reason), the poll gives a NEW wake id and "the whole start gate repeats" (SPEC.md:237); OD-2 re-plan, person re-approves, whole start gate repeats (SPEC.md:98); OD-13 a waiting hand-back does not count toward `max_in_flight` (SPEC.md:109); D15 R-6. 655's automatic restart is REJECTED.
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/VERDICT.md:26 `a body edit after approval voids the approval ... so a re-plan without re-approval starts a worker on a body nobody approved. Clay's text has no round-2 gate ..., and Clay's advocate conceded this.`
- Concerns: the option (b) (leave the body alone, carry the remaining list in the handoff) is the owner's cheaper alternative; with it nothing waits (QG1 VERDICT.md:36). QG1 notes the `escalated` carrier is UNVERIFIED (QG1 VERDICT.md:35).

### S02-F53 New branch `issue-<N>-r<n>` in the reused worktree for each hand-back round
- 655 says: the new worker starts on a new branch `issue-<N>-r<n>` in the reused worktree; "the guard looks at tracked changes only" (body line 102).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, VERDICT.md files, merged-requirements.md and techref for "issue-<N>-r", "-r<n>", "reused worktree". The plan has commit rules that check "branch and base" (FR-32, SPEC.md:234) and worktree-sharing risks (RK-7, SPEC.md:651).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): For hand-back round n the coordinator starts the new worker on a fresh branch named `issue-<N>-r<n>` in the same worktree, only after the old worker is final and its terminal released.
- Done when (NOT-COVERED only): a fixture second round shows a new branch with that name, the old branch untouched, and no second live worker in the worktree.
- Depends on: S02-F51; S02-F54; S02-F23 (guard binding repeats for the new worker).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md:77 `The worktree-sharing defect (INV-004) affects the claim procedure of Q26 ("no other unpushed commit")`.
- Concerns: UNVERIFIED that the guard looks only at tracked changes (655 claim; not found in the plan files read); FR-32 requires a branch and base check before a commit.

## Wave 9, Completion accounting (body line 46)

### S02-F54 Settle each worker: reuse, retain or release its terminal; end when no reclaimable terminal is left
- 655 says: `orca orchestration worker-release` (or `worker-retain`); the wave ends when `worker-list --run <id> --terminal-state reclaimable` shows nothing for the Run (body line 46; line 88).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, VERDICT.md files, merged-requirements.md and techref for "worker-release", "worker-retain", "reclaimable", "terminal state". Related only: the plan's own verb `release-worker` writes the guard's `.ok` file (SPEC.md:177) and is a different thing; FR-39 and a spec UNVERIFIED row cover `orca worktree rm` (SPEC.md:672).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): After a worker's `worker_done` is handled, the coordinator releases (or deliberately retains) that worker's terminal and checks that `worker-list --run <id> --terminal-state reclaimable` is empty.
- Done when (NOT-COVERED only): a finished fixture run ends with no terminal in state `reclaimable` for the Run, or with a recorded reason for each retained one.
- Depends on: S02-F5 (Run id); S02-F38; S02-F51 (release before a hand-back round).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:762 `Issues 698 (release-worker guard bypass and approver rule)`; memory note orca-coordinator-rebind-after-resume.md:10 (a closed terminal returns its Task to `ready`). Local check: `worker-release`, `worker-retain` and `worker-list --terminal-state reclaimable` exist (help output).
- Concerns: name clash: Orca's `worker-release` (terminal accounting) and the plan's `release-worker` verb (guard approval file) must not be confused; the coordinator never runs `worker-stop` or `worker-abandon` (655 section 9, consistent with "never interrupt" FR-40).

### S02-F55 Print the skill's return contract at the end of the run
- 655 says: wave 9 ends when the return contract is printed (body line 46).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, VERDICT.md files for "return contract" for the coordinator skill (hits are only about debate runs and the existing claim skill).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator skill prints a fixed return contract (issue, PR, outcome, round, escalations, Run id) when an issue's workflow ends.
- Done when (NOT-COVERED only): a fixture run ends with a return contract that a test parses with every required field present.
- Depends on: S02-F54; 655 section 4 templates (the contract format).
- Evidence from our documents: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1016 (the claim skill `SKILL.md` carries a return contract at `:105-150`, the pattern 655 follows).
- Concerns: none.

## Section summary

- 55 features: 25 COVERED, 13 CONFLICT, 17 NOT-COVERED. The current plan covers the merge gate and its refusals, the closeout and audit steps, the hand-back bounds, the wake and state handling of wave 0, the typing rules and the per-repo merge settings.
- The 13 CONFLICT rows are rejected parts of 655: the orchestrator names (F2), the registry repo list (F7), the coordinator running the claim itself (F10), assignment-only start (F13), entry-stored session state (F20), unguarded workers (F23), worker push and `/sc:pr-submit` (F28), no plan approval (F29, flips if the owner answers OA-1 "only the start gate"), permission-prompt approvals (F34), the interrupt (F37), autonomous merge (F43), closing without a per-PR go (F49) and hand-back without re-approval (F52).
- The 17 NOT-COVERED rows are all COORDINATOR work and none belongs to the watcher or dashboard: the wave/ref layout of the skill (F1), Orca skill load and Run binding (F4, F5), plan-request handling (F9, deferred by D15 A4), `body_sha` (F16), entry lifecycle (F19), Task/Dispatch mechanics and start retry (F24, F25), regression gate (F27), hourly check cadence and playbook (F32, F35), decision gates (F36), valid `worker_done` (F38), pr_submit helper reuse in `merge-gate` (F41), hand-back branch naming (F53) and wave 9 accounting and return contract (F54, F55).
- Builder cautions: the wave detail comes from Clay's design text, which is not owner-approved and is off master (SPEC.md:758, D15 VERDICT.md:134); the guard binding, `merge-gate`, `answer-check` and the report skill are unbuilt or removed (SPEC.md:674, 778); F25 and F36 must not weaken the no-double-start and chat-only-approval rules.