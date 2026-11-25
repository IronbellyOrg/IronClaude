# Section 06 analysis: Orca's built-in orchestration
Counts: COVERED 8, CONFLICT 1, NOT-COVERED 7

Section 6 of 655 is body lines 84-89. Acceptance criterion touching it: body line 220 ("The skill loads Orca's own `orchestration` skill at run time; each wave names its Orca commands.").

Naming note: 655 says "orchestrator"; the current plan says "coordinator" (FR-62, SPEC.md:319). Where 655 writes "orchestration layer" for Orca's own layer, the plan accepts that sense (FR-62).

Paths used below. SPEC = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md. DEC = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/DECISIONS.md. WC = /home/coder/workspaces/IronClaude/src/superclaude/core/WORKER-CONTRACT.md (the contract the plan keeps and amends only at lines 57, 70, 245). TRO = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md. TRI = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md.

### S06-F1 One Orca Run per orchestrator, `run-create` and `run-use`, resumed after a restart
- 655 says: The orchestrator uses `run-create` and `run-use` so there is one Run per orchestrator and it is resumed after a restart (body line 86). Test T5 expects "The Run resumes (`run-use`) with no second claim and no second `worker-start`" (body line 202).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md and FOLLOW-UPS.md for `run-create`, `run-use`, `run-current`, "Orca Run", "one Run", "consumer_fenced" (no hit). Related but not the same: FR-34 restarts a dead coordinator with a resume wake (SPEC.md:236) and FR-29 has kill-and-restart tests (SPEC.md:231); neither says the Run is rebound. WC-16 already assumes the coordinator "never stops watching its Run" (TRI:1346, summary of contract lines 287-289).
- Component (NOT-COVERED only): COORDINATOR. The Run is bound by the coordinator session and its skill; the watcher only starts the session.
- Feature statement (NOT-COVERED only): The coordinator creates or reuses one Orca Run for its repo at start and, after any restart or resume, checks `run-current` and rebinds with `run-use` before it starts a worker.
- Done when (NOT-COVERED only): A restart test kills the coordinator mid-issue, resumes it, and shows `run-current` names the same Run and the next `worker-start` is not refused with `consumer_fenced` (no second claim, no second worker).
- Depends on: 655 section 2 waves (worker start), 655 section 5 restart handling, SPEC FR-34 (restart wake).
- Evidence from our documents: /home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/orca-coordinator-rebind-after-resume.md:11 "every orchestration mutation (worker-start etc.) fails with `consumer_fenced` until `orca orchestration run-use --id <run_id>` rebinds the Run". /home/coder/.claude/skills/sc-closeout-protocol/refs/settle.md:56 "No Orca Run is bound to this session, so the worker's task was not looked at" (closeout needs a bound Run). SPEC.md:668 lists "U5 mailbox from outside a Run" as an open live test.
- Concerns: Without this, FR-34's restart would leave a resumed coordinator unable to start or settle anything (known defect, memory dated 2026-11-04, 16 days old, UNVERIFIED against today's Orca). The observer and sweep must stay read-only and never call `run-use` or `run-create` (TRO:972, "forbidden (run-use, run-create)"); only the coordinator may.

### S06-F2 Tasks: `task-create` and `task-update`
- 655 says: The orchestrator uses `task-create` and `task-update` (body line 86).
- Status: COVERED
- Current plan: WORKER-CONTRACT (kept by the plan; SPEC.md:234, 304, 339 name it as a core file) already makes the coordinator create each Task with `task-create --spec` and retry as a new Task (WC:69; WC-6) and bans `task-create` by workers and commands (WC:38, WC:60). The Task is settled to completed by `/sc:closeout` through `orca orchestration task-update --status completed` (settle.md:58 under /home/coder/.claude/skills/sc-closeout-protocol/refs/), which the plan adopts as is (DEC:582 item F1) and runs per merged PR (FR-38, SPEC.md:240; DEC:502).
- Evidence from our documents: n/a (covered).
- Concerns: The plan has no FR that names `task-create` itself; it comes only through the contract. The skill author must follow WC:69 (new Task for every retry, never `--retry-of`). TRI:1360 notes that no Python in `src/` calls `task-create` today, so this stays prose in the skill.

### S06-F3 `worker-start` with the filled handoff as the Task spec, and `dispatch`
- 655 says: Workers start with `worker-start` using the filled handoff as the task spec, and `dispatch` is also listed (body line 86).
- Status: COVERED
- Current plan: FR-30 (SPEC.md:232) starts every worker with `pending --level worktree`, the marker `[sc-launch:v1:<nonce>]` in the first prompt and a check that `pending/<nonce>` is consumed; D12 "one supervised `worker-start` route: adopt with change" (DEC:582, SPEC.md:461); FR-61 hands the worker a chain from the coordinator's own template that names the filed plan (SPEC.md:282); DEC:238 "one supervised worker is started with `orca orchestration worker-start`".
- Evidence from our documents: n/a (covered).
- Concerns: The plan has ONE start route, `worker-start`; it never names `dispatch` as a second route, and the contract bans `dispatch` in commands and workers (WC:38). The skill must not add `dispatch` as a start path. Real risk from the debate: Orca may cut a long Task spec to sections 1, 2 and 9 plus a path, so the guard marker could be lost silently (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D05/adversarial/adversarial/invariant-probe.md:19, INV-013, UNVERIFIED; the plan leaves it to the S17 binding probe, SPEC.md:645, 666). No worker has ever been bound on this route (SPEC.md:57, RK-1 at 645).

### S06-F4 The mailbox: `send`, `check`, `ask`, `reply`, `inbox`
- 655 says: The orchestrator uses the Orca mailbox verbs `send`, `check`, `ask`, `reply` and `inbox` (body line 86).
- Status: COVERED
- Current plan: `check --wait` returns are where the coordinator pulls wakes (FR-28, SPEC.md:230); mailbox and typed line are id-only nudges (FR-14, SPEC.md:204; D10, SPEC.md:86); no GitHub text may reach a mailbox subject (SEC-16, SPEC.md:305); a bound worker may `send` and `ask` only as one plain call with no `--to` (DEC:271, D05 item 6; WC:66). Worker questions go to the coordinator (WC-3, WC:51).
- Evidence from our documents: n/a (covered).
- Concerns: `inbox` is not named anywhere in the plan (searched SPEC.md, FOLLOW-UPS.md and DECISIONS.md for "inbox": 0 hits); read it as covered by `check`. Mailbox delivery from outside a Run is unproven (U5, SPEC.md:668, 708); failure leaves the file pull as the only channel. The plan's mailbox is a nudge only; a 655 design that relies on the mailbox as the only wake would conflict with D10.

### S06-F5 `gate-create`: an Orca decision gate to record a pending question
- 655 says: The orchestrator uses `gate-create` (body line 86); the merge wave row uses `gate-create` when a failing check waits for the human's explicit OK (body line 44).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, FOLLOW-UPS.md for `gate-create`, `gate-resolve`, "decision gate", "Orca gate" (no hit). The plan's question channel is the `escalate` verb (FR-26, SPEC.md:228) with the nine-row table (D16, DEC:582) and a typed `answer-check` (D4/D20), not an Orca gate. The nearest sweep text says the observer's allowlist has no gate verb (TRO:976 "gate-create/resolve (572)" only in the 655 design column).
- Component (NOT-COVERED only): COORDINATOR. It is a verb the skill calls when it raises a question; the TUI-DASHBOARD would only display it.
- Feature statement (NOT-COVERED only): When the coordinator writes an escalation, it also opens an Orca gate for it so the pending question is visible to Orca and the sweep, and closes the gate when the recorded answer arrives.
- Done when (NOT-COVERED only): A test escalation produces one open gate that `orca orchestration` lists, the sweep report shows a pending question for it, and the gate is closed after the typed answer passes `answer-check`.
- Depends on: 655 section 8 (what reaches Clay, nine-row table), 655 section 7 merge wave, SPEC FR-26 and FR-37 (escalation written first).
- Evidence from our documents: TRO:1225 "Sweep coverage gaps: ... `Messages coverage: partial` ... pending questions cannot be read" (the sweep cannot see questions today). TRO:972-976 shows the sweep and observer allowlists contain no gate verb.
- Concerns: The gate must never be the approval itself (see S06-F6). Whether Orca gates show in the sweep is UNVERIFIED. The plan's FR-37 says write the escalation first and send nothing if refused; a gate would have to follow that order.

### S06-F6 `gate-resolve`: an Orca gate resolution as the human's OK
- 655 says: `gate-resolve` is one of the commands used (body line 86), paired with `gate-create` for the human's explicit OK to merge over a failing check (body line 44).
- Status: CONFLICT
- Current plan: SEC-01 (SPEC.md:290): a merge needs a person's go "typed in live chat after the gate output, recorded, one-shot"; SEC-03 (SPEC.md:292) lets only `checks_failing` and `merge_safety` be overridden, each with its own key; SEC-14 (SPEC.md:303): every approval, go and ruling is given in the owner's chat and an agent records it. An Orca gate resolved in the Orca UI or CLI is a different channel and no verdict accepts it as a go. 655's version, where `gate-resolve` carries the human's OK, is REJECTED. (`gate-create` as a notice only is S06-F5.)
- Evidence from our documents: DEC:293 "it is typed in live chat after the gate output, recorded, one-shot, expires ... and void on a head change"; DEC:242 "No file row written by the owner."; DEC:301 (D06 item 9) "`answer-check` ... cannot tell a person from a script" (a gate click would be even weaker).
- Concerns: `ironbelly` is a login shared by the owner and every session (DEC:251), so a recorded go proves little already; adding a click channel widens this. Do not let any Orca verb a worker or the coordinator can run stand in for the person's typed go.

### S06-F7 Watching workers: `worker-show` and `worker-read`
- 655 says: The orchestrator uses `worker-show` and `worker-read` (body line 86).
- Status: COVERED
- Current plan: The coordinator runs `/sc:sweep` each cycle (FR-38, SPEC.md:240) and reads its report before acting; the sweep already uses `worker-show --dispatch <id> --json` (up to 50 per sweep) and `task-list --run` (TRO:956, 974, 975). The coordinator's own liveness pass and the contract's loop are WC-16 (TRI:1346). Typing into worker terminals is allowed only under four rules (FR-40, SPEC.md:242).
- Evidence from our documents: n/a (covered).
- Concerns: The sweep allowlist has no `worker-read` ("no worker-read", TRO:975), so reading a worker transcript is a coordinator-only act not named in the plan; the skill may use it but the plan gives no rule. The sweep caps `worker-show` at 50 per sweep (TRO:1106).

### S06-F8 Releasing a worker: `worker-release`
- 655 says: The orchestrator uses `worker-release` (body line 86); wave 9 settles the worker by reuse, retain or release (body line 46).
- Status: COVERED
- Current plan: The contract says "After `worker_done`, the coordinator opens the contract, then releases or reuses the worker" (WC:88). FR-35 requires the old worker to be final before a hand-back re-plan (SPEC.md:237). `/sc:closeout` settles the worker's Orca task (DEC:502 item 1).
- Evidence from our documents: n/a (covered).
- Concerns: Only the contract names release; no FR or test pins it, and `worker-retain` is not named in the plan (searched SPEC.md and DECISIONS.md: 0 hits for `worker-release`, "retain"). The check "no reclaimable terminal for the Run" (`worker-list --terminal-state reclaimable`) belongs to 655 section 2 wave 9, not here.

### S06-F9 `orca reference add` and `find`
- 655 says: The orchestrator uses `orca reference add` and `find` (body line 86).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, FOLLOW-UPS.md, DECISIONS.md, STATE.md for `reference add`, `reference find`, "Orca reference" (no hit). TRO:980 lists it only under the 655 design column (design lines 474, 565).
- Component (NOT-COVERED only): COORDINATOR. The skill would call it when it hands over an issue or worktree.
- Feature statement (NOT-COVERED only): The coordinator records, with `orca reference add`, the link between an issue, its worktree and its worker, and finds it again with `orca reference find` after a restart.
- Done when (NOT-COVERED only): After a restart the coordinator finds the issue's worktree and worker through `orca reference find` and no second worktree or worker is created.
- Depends on: S06-F1 (Run rebind), 655 section 2 waves 1-3 (adoption and worktree), SPEC FR-29 (adoption record `issues/<repo-key>__<N>.json`).
- Evidence from our documents: SPEC.md:231 (FR-29) already keeps ONE adoption record per issue, an exclusive-create file; a second record in Orca would be a second store. /home/coder/workspaces/IronClaude/CLAUDE.md (project instructions, fork rule): Orca link flags (`--issue`, `--pr`) are never passed for this repo until the Orca project id is the fork's; whether `reference add` carries such a link is UNVERIFIED (not found in /home/coder/.claude/skills/orca-cli).
- Concerns: Possible overlap with FR-29's single adoption record (NFR-02 "one writer per file"). Must not create any link that resolves to SuperClaude-Org. The builder must read `orca reference --help` first (UNVERIFIED what it does).

### S06-F10 `orca worktree ps`
- 655 says: The orchestrator uses `orca worktree ps` (body line 86).
- Status: NOT-COVERED
- Current plan: partly. The cap is counted from the store and open claim files (FR-33, SPEC.md:235), and the claim-terminal and live-agent question is an open live check (FR-70 and X-001, SPEC.md:327, 667). The sweep calls `worktree ps --json` once per run (TRO:958). Nothing says the coordinator itself calls `worktree ps` to see whether a live agent already works in a worktree before it starts a worker. Searched SPEC.md, DECISIONS.md for "worktree ps": no hit.
- Component (NOT-COVERED only): COORDINATOR. It is the pre-start check inside the skill; the poll cap (FR-33) stays with the WATCHER.
- Feature statement (NOT-COVERED only): Before `worker-start`, the coordinator runs `orca worktree ps` and refuses to start a worker in a worktree where another agent is live.
- Done when (NOT-COVERED only): A test with a live agent in the target worktree makes the coordinator stop and escalate instead of starting a second worker.
- Depends on: SPEC FR-70 (X-001 live check), S06-F3 (worker start).
- Evidence from our documents: SPEC.md:667 "Claim terminal lifetime; complete live-agent list; worker worktree path | FR-70, FR-33 | S17 X-001 record". /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/adversarial/rounds/round2-advocate-2-sonnet-analyzer.md:38 "No code in planb's `issue_watch/` checks for live agents in the worktree: a grep for ... `worktree ps` ... finds nothing."
- Concerns: The sweep's own contract never calls `worktree ps --agent-wait` (TRO:705); use plain `ps --json`. The claim terminal may stay open as an idle second agent (same file, line 37, UNVERIFIED), which a `ps` check would also see and block on.

### S06-F11 Never run `worker-stop` or `worker-abandon`
- 655 says: The orchestrator never runs `worker-stop` or `worker-abandon` (body line 86, "section 9").
- Status: COVERED
- Current plan: FR-40 "never interrupt a worker" (SPEC.md:242); FR-26 gives a closed `refuse(argv)` list with a failing test per pattern, "no lease, no interrupt" (SPEC.md:228); verdict D15 rejects the interrupt exception N7 (D9, DEC:582) and states "The coordinator never merges alone, never tags or publishes, never answers a permission prompt, never interrupts a worker" (DEC:603); R-7 "no `lease`, no interrupt" (DEC:593). The OURS rebuttal states the wording "no `worker-stop`, no `worker-abandon`, no Escape or Ctrl+C by `terminal send --text`, no `terminal send --interrupt`" (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/adversarial/rounds/round2-rebuttal-1-ours.md:218).
- Evidence from our documents: n/a (covered).
- Concerns: SPEC.md itself does not name `worker-stop` or `worker-abandon` (0 hits in SPEC.md); the words appear only in the debate rebuttal. The build must put both verbs, and Escape or Ctrl+C typed text, into the `refuse(argv)` list with one test each (FR-26). 655's "section 9" is outside this section.

### S06-F12 Load Orca's own `orchestration` skill at run time (`orca skills get orchestration`) instead of copying it
- 655 says: Orca ships an `orchestration` skill; the orchestrator skill loads it at run time with `orca skills get orchestration` instead of copying it (body line 88; acceptance criterion body line 220).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, FOLLOW-UPS.md, DECISIONS.md and the debate verdicts for "orchestration skill", `skills get`, "loads it at run time" (hits only in D08 naming debate, where the skill is used as vocabulary evidence, e.g. /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/adversarial/diff-analysis.md:65). FR-24 (SPEC.md:226) defines the skill `sc-coordinator-protocol` without any load-at-run-time rule.
- Component (NOT-COVERED only): COORDINATOR. It is a step in the skill's start-up.
- Feature statement (NOT-COVERED only): The `sc-coordinator-protocol` skill runs `orca skills get orchestration` at start and follows its supervised loop and task-spec rules, without keeping a copy of that text in IronClaude.
- Done when (NOT-COVERED only): The skill text has a start step that runs the command, a test checks that no copy of Orca's skill text exists under `src/superclaude/skills/sc-coordinator-protocol/`, and the step fails closed with an escalation when the command returns nothing.
- Depends on: S06-F13 (what it cites), S06-F1 (Run).
- Evidence from our documents: D08 diff-analysis.md:8 and :65 say the skill was read through `orca skills get orchestration` and has "Coordinator" and "Handoff owner" roles; TRI:2005 (U-8) records "location of the Orca `orchestration` skill ... no `orchestration*` path under `src/`". WC:3 and WC:38-60 are IronClaude's own copy of the rules, so a run-time load adds a second source of rules.
- Concerns: If Orca's skill and WORKER-CONTRACT disagree (for example on stopping or interrupting a worker), the contract and the plan must win (FR-40, FR-26); the skill step must say so. Orca can change its skill text between versions, so a loaded text can silently widen the allowed verbs: the closed `refuse(argv)` list (FR-26) must not read from it. 655 says Orca's skill "cites" parts; whether those parts exist in today's Orca text is UNVERIFIED (only the role table was read, diff-analysis.md:148).

### S06-F13 Cite Orca's supervised loop, task-spec contract and completion accounting (a valid `worker_done` settles the Task; each settled worker is reused, retained or released)
- 655 says: The skill cites the orchestration skill's supervised loop, its task-spec contract and its completion accounting: a valid `worker_done` settles the Task, and each settled worker is reused, retained or released (body line 88).
- Status: COVERED
- Current plan: IronClaude already carries these in WORKER-CONTRACT: the coordinator loop that never stops watching its Run, re-arms waits and escalates a closed list of states (WC-16, summary at TRI:1346); the task-spec and brief template (WC section 5, WC:165-170; WC:69); `worker_done` once per worker, `failed` or `succeeded` (WC-5, TRI:1339); "After `worker_done`, the coordinator opens the contract, then releases or reuses the worker" (WC:88). The plan keeps this contract as the governing document (SPEC.md:234, 304, 339, 743-744) and has `/sc:closeout` settle the Task after merge (DEC:502).
- Evidence from our documents: n/a (covered).
- Concerns: The plan settles the Task at closeout (after merge), while 655 settles it when a valid `worker_done` arrives. Under a hand-back (FR-35, SPEC.md:237) the old worker must be final first. A builder must pick one point per Task and not settle twice (closeout's `task` item, settle.md:55-58, escalates `write_failed`).

### S06-F14 Name Clay's coordinator spec FR-8 and FR-9 for the same commands
- 655 says: "Clay's coordinator spec names FR-8 and FR-9 for the same commands" (body line 88); the spec is `.dev/specs/SPEC-AGENT-WORK-COORDINATOR-20261027.md` in the IronFlow repo (body line 92).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md and inventory for "SPEC-AGENT-WORK-COORDINATOR", "FR-8", "FR-9" as Clay's numbers (no hit; the plan's own FR-08, FR-09 are different requirements). The file itself was not read (it is in another repository), so its FR-8 and FR-9 text is UNVERIFIED.
- Component (NOT-COVERED only): OTHER. It is a documentation cross-reference, not behaviour; it belongs to the doc that describes the skill, once the owner decides how the IronFlow coordinator spec relates to the plan.
- Feature statement (NOT-COVERED only): The coordinator skill's reference page names which requirements of the IronFlow coordinator spec its Orca commands satisfy, using ids checked against that file.
- Done when (NOT-COVERED only): A table in the skill refs lists each Orca command with the IronFlow spec requirement id, and each id was checked against the real file.
- Depends on: 655 section 7 (one design with Clay's coordinator spec).
- Evidence from our documents: no evidence found in our documents.
- Concerns: The plan's numbering FR-nn is its own, so "FR-8 and FR-9" in a plan-based doc would be read as the wrong requirements; always write "IronFlow spec FR-8". The source file is outside this repository and may have moved (655 line 92 says it is "moving to the orchestrator repo").

### S06-F15 The handoff satisfies the brief layout of `WORKER-CONTRACT.md`
- 655 says: "The handoff also satisfies the brief layout of `src/superclaude/core/WORKER-CONTRACT.md`" (body line 88).
- Status: COVERED
- Current plan: The contract's coordinator brief template (WC section 5, WC:165-177, with its guard line copied word for word) stays the governing layout; FR-61 hands the worker a chain "from the coordinator's own template" (SPEC.md:282); FR-30 adds the launch marker line `[sc-launch:v1:<nonce>]` to the first prompt, in a restored `brief.py` / handoff template (SPEC.md:232; DEC:267 "a new line in `templates/handoff-prompt.md`"); the contract amendments are limited to lines 57, 70 and 245 (SPEC.md:360, L-07).
- Evidence from our documents: n/a (covered).
- Concerns: TRI:1360 records that the contract's brief template "has no launch-marker slot", so the marker line is a change to the brief layout the plan must make explicit and test. The brief guard (`Guard:` line, `--unattended` on each `Command:` line, WC:15-22, 95) applies to `/sc:` commands run as workers; a `--pipeline none` issue worker's chain must still pass it or be exempted in writing. 655's nine handoff sections are another section's feature.

### S06-F16 Each wave names its Orca commands (acceptance criterion)
- 655 says: The skill's `SKILL.md` lists waves 0 to 9 and "each wave names its Orca commands" (acceptance criterion, body line 220; also body line 217).
- Status: NOT-COVERED
- Current plan: none found as a requirement; searched SPEC.md for "names its", "per-wave", "wave" with "Orca command" (no hit). The plan's flow diagram does name some verbs per step (SPEC.md:145-157, for example `pending --level worktree`, `worker-start`, `check --wait`), and S14 lists a "skill-text scan" (SPEC.md:498), but there is no rule that every step lists its Orca verbs.
- Component (NOT-COVERED only): COORDINATOR. It is a content rule for the skill text.
- Feature statement (NOT-COVERED only): Each step of the `/sc:coordinator` skill states the exact Orca verbs it may call, and the closed `refuse(argv)` list is checked against that set.
- Done when (NOT-COVERED only): A test reads the skill text, extracts the Orca verbs per step, and fails if a step calls a verb that is not listed or one that `refuse(argv)` blocks.
- Depends on: S06-F1 to S06-F11, 655 section 2 (the waves), SPEC FR-26.
- Evidence from our documents: SPEC.md:498 (S14) "skill-text scan" is the closest existing check. TRO:971-980 shows how many verb forms the design uses (about 30) and that none beyond four match a sweep template, which is why a per-step list matters.
- Concerns: The plan has stages S0-S17, not waves 0-9; the mapping is for the section 2 analyst. Keep the per-step list short enough to review; the list is also the surface the `refuse(argv)` tests must cover.

## Section summary
- 16 features. 8 COVERED (Tasks, `worker-start`, mailbox, worker watching, release, never-stop, supervised-loop accounting, brief layout): the kept WORKER-CONTRACT plus FR-14, FR-26, FR-28, FR-30, FR-38, FR-40, FR-61 already deliver them. Only `dispatch` as a second start route is not carried (one route, D12).
- 1 CONFLICT: `gate-resolve` as the human's OK loses to SEC-01, SEC-03 and SEC-14 (go typed in chat, recorded by an agent).
- 7 NOT-COVERED, mostly coordinator work: Run create and rebind after restart (S06-F1, the most important: without it FR-34's restart cannot start workers), gate-create as a visible question, `orca reference`, `worktree ps` before worker start, loading Orca's `orchestration` skill at run time, the cross-reference to Clay's FR-8 and FR-9, and the "each wave names its Orca commands" rule.
- Builder warnings: the loaded Orca skill must never widen the allowed verbs; `worker-stop` and `worker-abandon` appear only in a debate rebuttal, so they need explicit `refuse(argv)` tests; `orca reference` must not create links that resolve to SuperClaude-Org (UNVERIFIED what it does).

