# Research: Orchestrator design overlap with observer, sweep and work-report tools (GF-3)
**Investigation type:** Doc Analyst
**Scope:** /home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator.md; /home/coder/.cache/ic-snap-20261120/master/docs/designs/sc-closeout.md (sweep/coordinator touch points only); /home/coder/.cache/ic-snap-20261120/master/src/superclaude/core/WORKER-CONTRACT.md (lines 20-30, 96-160, 280-295); research files 04 and 05; read-only `gh pr list/view --repo IronbellyOrg/IronClaude`
**Status:** Complete
**Date:** 2026-11-20
---

Path key: DESIGN = /home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator.md (1412 lines; origin/master 61ac2c2e6; merged by PR #681 on 2026-11-20T00:02:33Z). WC = /home/coder/.cache/ic-snap-20261120/master/src/superclaude/core/WORKER-CONTRACT.md (339 lines). All line numbers are snapshot line numbers read in this pass. The design is a proposal ("It holds no implementation code", DESIGN:3), so a design statement about what the orchestrator WILL do is tagged [DESIGN-ONLY] (nothing to verify in code) unless a built file is named.

## 1. Document status and what it is (DESIGN:1-11, 29-50)

- DESIGN:1 title "Design: the issue-polling orchestrator (`/sc:orchestrator`)"; DESIGN:3 "Status: approved by the owner (Clay) on 2026-11-19 ... It holds no implementation code. The build starts from this text". [CODE-VERIFIED] the file exists on origin/master (snapshot).
- Pipeline (DESIGN:35-47): Orca automation every 5 min (precheck only, no agent) -> poll script `superclaude issue-watch once` -> orchestrator session (one per repo, at most 3 issues in flight, tag `orchestrator-<short>-<n>`, command `/sc:orchestrator`) with waves 0 to 9 -> workers started by `orca orchestration worker-start`.
- DESIGN:49: "The orchestrator keeps the work report current as a living document all day ... There is no session-manager skill ... the orchestrator does every check-in itself, including typing into a worker's terminal and approving its permission prompts (owner ruling 2, DQ9)".
- Contents (DESIGN:13-27): scope, decisions DQ1-DQ13 (DESIGN:109-123), OQ1-OQ6 and ADD1-ADD6 (DESIGN:129-140), wake message (from 143), poll script, skill (waves in 5.3 at DESIGN:528-631), coordinator-spec changes C1-C29 (DESIGN:897-926), PR split (section 8), tests (section 9), owner decisions (10), risks (11), UNVERIFIED items (12), coverage matrix (13).

Key Takeaways
- The orchestrator is a designed successor to the built `superclaude issue-watch` poller and the coordinator spec's session-manager idea; it is one session per repo that owns issues from claim to merge. The design itself says it is "the coordinator" of the coordinator spec (DESIGN:930).

## 2. Grep evidence: does the design mention the sweep, WC-16, the observer or `.dev/sweeps`? (question c)

Searches run read-only on DESIGN:
- Pattern (case-insensitive) `/sc:sweep|superclaude sweep|superclaude observe|WC-16|WC-10|observer|\.dev/sweeps|never-as-worker|sc:sweep`: hits only at DESIGN:135, 480, 580, 748, 799, 1249 and 1313, all of them `never-as-worker` or `WC-10` text. ZERO hits for `/sc:sweep`, `superclaude sweep`, `superclaude observe`, `WC-16`, `observer` and `.dev/sweeps`.
- Pattern `WC-10|WC-16|WC-17|never-as-worker`: DESIGN:135, 480, 580 (WC-10), 748 (WC-10), 799, 991 (WC-17), 1017, 1095, 1249, 1313, 1381 (WC-17). No WC-16 hit.
- Pattern `sweep` (case-insensitive) gives 9 line hits (DESIGN:122, 298, 313, 387, 422, 657, 803, 913), none about `/sc:sweep` or `superclaude sweep`:
  - DESIGN:122 (DQ12) and DESIGN:913 (C15): "a missed-update sweep" = one of the things the daily work-report run still covers.
  - DESIGN:298: `import yaml` with `safe_load` "is already used in `src/superclaude/cli/sweep/probes.py`, `cli/eval/loader.py` and others, so no dependency is added" = the ONLY reference to the sweep package, as a dependency precedent; no behavioural relation.
  - DESIGN:313 (4.5 step 6) "Sweep: an entry still `pending` at the start of a cycle was left by a cycle that died between steps 10 and 11": the issue poll's own store sweep. DESIGN:387 `cycle.py` `_sweep` (777), DESIGN:422 `record.py` `sweep` (627), DESIGN:657 "the poll's sweep (4.5 step 6) raises `plan_stuck`": same poll-internal sweep (functions of the BUILT `issue_watch` package, reshaped).
  - DESIGN:803: "it is not run over all pull requests (the sweep is not adopted)": a pull-request sweep considered for the closeout wave and not adopted.
- Pattern `observer` case-insensitive: no hit in DESIGN.

Key Takeaways
- Fact for the owner: the approved orchestrator design does not reference `/sc:sweep`, WC-16, the observer (`superclaude observe`) or `.dev/sweeps`. The word "sweep" there means the issue poll's own store sweep, a missed-update sweep of the daily report, a pull-request sweep it does not adopt, and the `cli/sweep/probes.py` yaml precedent (DESIGN:298).
- The design does cite WC-10 (DESIGN:580, 748) and the never-as-worker list (DESIGN:135, 480, 799, 1249). WC-16 itself (WC:289) says the `/sc:sweep` classes "follow WC-10", so WC-10 is the one worker-contract rule both the design and the sweep text name.

## 3. Orca verbs the orchestrator is designed to call, set against the observer's 3 and the sweep's 10 argv templates (question a)

Allowlists read in this pass: observer `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/observe/adapter.py:29-50` (WORKER_LIST_TEMPLATE `("orchestration","worker-list","--json","--limit","100")`, DISCOVERY_TEMPLATE `("skills","list","--json")`, QUESTION_TEMPLATE `("orchestration","check","--all","--types","question")` then `--run <runId>` then `--json`; FORBIDDEN_PREFIXES `check, --ack, --wait, --retry-request, --peek, dispatch, inbox, run-use, run-create, send, ask, reply, reset`) **[CODE-VERIFIED]**. Sweep `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/sweep/probes.py:49-60` (ALLOWED_ORCA, 10 templates, 7 verbs; FORBIDDEN_TOKENS `--include-remote`) **[CODE-VERIFIED]**; call status of each template is in research 04 section 1.1 (6 called, 4 pinned and never called).

The design's verbs, with every design line that names them (DESIGN = orchestrator.md). "Obs" = argv accepted by the observer allowlist; "Swp" = argv accepted by the sweep allowlist (token-for-token match, ids as `<run>`/`<dispatch>`). [DESIGN-ONLY] means the call exists only as designed text; nothing in the snapshot makes it (the `superclaude orchestrator` package and `sc-orchestrator-protocol` skill are absent, section 7).

| # | Designed call (DESIGN line) | Who calls it in the design | Obs | Swp |
|---|---|---|---|---|
| 1 | `orca skills get orchestration` (+ `--reference <file>`) (DESIGN:9, 515, 534, 726) | orchestrator wave 0 | no (observer allows only `skills list --json`) | no |
| 2 | `orca orchestration --help`, each verb `--help` (DESIGN:530, 534, 1102) | design authoring and a pinned-fixture test | no | no |
| 3 | `orca orchestration run-current --json` (DESIGN:534) | wave 0 | no | no: the sweep's template 1 is `orchestration run-current` without `--json` (probes.py:50) |
| 4 | `orca orchestration run-create --objective "<text>" --json` (DESIGN:98, 534) | wave 0, once per orchestrator | no (`run-create` forbidden, adapter.py:44) | no |
| 5 | `orca orchestration run-use --id <run id>` (DESIGN:534, 661) | wave 0 and restart | no (`run-use` forbidden, adapter.py:43) | no |
| 6 | `orca orchestration run-show --id <run>` (DESIGN:1262, U4 live check) | owner window | no | no |
| 7 | `orca orchestration task-create --spec <file> --task-title "<R>#<N>" --json` (DESIGN:565) | wave 4 | no | no |
| 8 | `orca orchestration task-list --run <id> --json` (DESIGN:1304, T12 live check); sc-closeout.md:379 runs `task-list --json` | live test; the closeout skill | no | sweep template 5 `task-list --run <run> --json` matches the first form (probes.py:54); `task-list --ready --run` (probes.py:53) is not in the design |
| 9 | `orca orchestration worker-start --task <task id> --worktree path:<path> --agent claude --model claude-gw-<worker_tier> [--effort <e>] --json` (DESIGN:565, 726) | wave 4 | no | no |
| 10 | `orca orchestration worker-start --help`, `worker-start --retry-request <uuid>` (DESIGN:565, 1279) | wave 4 retry; live check | no (`--retry-request` forbidden, adapter.py:39) | no |
| 11 | `orca orchestration request-show --request <id> --json` (DESIGN:567, 1279) | wave 4 outcome_unknown | no | no |
| 12 | `orca orchestration worker-show --dispatch <dispatch id> --json` (DESIGN:565, 744, 1278) | waves 4, 5 | no | YES: sweep template 3 `worker-show --dispatch <dispatch> --json` (probes.py:52), called, capped at 50 per sweep |
| 13 | `orca orchestration worker-list --json` (DESIGN:572) and `worker-list --run <id> --json` (DESIGN:744) | wave 5 hourly check, "list sessions" line | no (the observer needs `--limit 100` fixed: adapter.py:29) | `--run <run> --json` YES (probes.py:51, called once per Run); the bare `worker-list --json` no |
| 14 | `orca orchestration worker-list --run <run id> --terminal-state reclaimable --json` (DESIGN:628) | wave 9 | no | no (extra option; not token-for-token the sweep template) |
| 15 | `orca orchestration worker-read --dispatch <id> --source transcript --limit <n<=200> [--cursor <c>]` (DESIGN:572, 745, 1299) | wave 5 / "read bounded transcripts" | no | no (`worker-read` is not among the sweep's 10 templates, probes.py:49-60) |
| 16 | `orca orchestration check --wait --types "worker_done,escalation,question,status" --timeout-ms 240000 --json`, then `--ack <delivery id>` (DESIGN:572, 748) and `check --run <id> --peek --json` (DESIGN:1263) | wave 5 loop | no (`check` outside the question shape, `--wait`, `--ack`, `--peek` forbidden, adapter.py:36-40) | no |
| 17 | `orca orchestration reply --id <message id> --body <text>` (DESIGN:572) | wave 5 | no (`reply` forbidden) | no |
| 18 | `orca orchestration send --to dispatch:<id>|run:<id> --type status --subject <t> --body <b>` (DESIGN:112, 163, 572, 580, 1263) | the poll (wake to `run:<id>`) and wave 5 check-ins | no (`send` forbidden) | no |
| 19 | `orca orchestration gate-create --task <id> --question <t> --options <json>`, `gate-resolve` (DESIGN:572) | wave 5 / escalation | no | no |
| 20 | `orca orchestration worker-release --dispatch <id> --json`, `worker-retain` (DESIGN:628) | wave 9 | no | no |
| 21 | `orca orchestration worker-stop`, `worker-abandon`, `reset` (DESIGN:759, 1117) | listed as REFUSED in the argv denylist test | n/a | n/a |
| 22 | `orca terminal list --worktree path:<repo> --json` (DESIGN:744, 1261) | the poll (find a session by tag) and the orchestrator ("find its own sessions") | no | no (the sweep allowlist has no `terminal` verb) |
| 23 | `orca terminal read --terminal <handle> --screen` (DESIGN:573, 752) | wave 5 typing rules | no | no |
| 24 | `orca terminal send --terminal <handle> --text <t> --enter [--wait-submit <s>] [--retry-request <id>]` and `--interrupt` (DESIGN:159, 573, 746, 752) | the poll (one typed wake line) and wave 5 (typing, approvals); `--interrupt` only through `superclaude orchestrator escalate --interrupt` (DESIGN:749) | no | no |
| 25 | `orca terminal wait --for tui-idle` (DESIGN:748) | wave 5 | no | no |
| 26 | `orca terminal close --terminal <handle>` (DESIGN:710, 762, 1284) | orchestrator's own terminal at idle end | no | no |
| 27 | `orca worktree show --worktree issue:<N> --json` (DESIGN:474, 1290) | poll evidence E4 | no | no |
| 28 | `orca worktree current --json` (DESIGN:565, 1267) | wave 4, project check before `reference add` | no | argv is the sweep's PINNED template 8 (probes.py:57), never called by the sweep |
| 29 | `orca worktree ps` (DESIGN:1129, live test T-case only) | a verification step, not a wave | no | `worktree ps --json` is template 6 (called once per sweep, probes.py:55); the design's form has no `--json`; no match |
| 30 | `orca worktree set --worktree path:<orchestrator repo> --unread --comment <note>` (DESIGN:112, 666) | the poll and escalation notice | no | no |
| 31 | `orca worktree rm` (DESIGN:759, 1117) | listed as REFUSED | n/a | n/a |
| 32 | `orca project setup-clone --project github:<o>/<r> --host local --url <url> --destination <clone_parent>` (DESIGN:114, 544) | wave 1 (DQ4) | no | no |
| 33 | `orca reference add <url> --worktree path:<p>`, `orca reference find <url> --json` (DESIGN:474, 565) | wave 4; poll evidence | no | no |
| 34 | `orca automations list|show|runs` read-only; `create|edit|remove|run` refused (DESIGN:348, 354, 762, 965, 1025, 1117, 1265) | owner-run setup O3/O4; the orchestrator never calls them | no | no |
| 35 | `ccsession --list` (read only) (DESIGN:744), `ccsession orchestrator-<short>-<n> --tier <tier>` (DESIGN:112, 710), `ccsession --rm` refused (DESIGN:759) | the poll starts a session; the orchestrator lists | not an Orca verb | not an Orca verb |

Built-today Orca callers in the same area, for comparison (snapshot code):
- AWR scripts call `orca terminal list [--worktree path:<p>]` (orca_term.py:26; sessions.py:291), `terminal read --terminal <h> --screen` (orca_term.py:89), `terminal send --terminal <h> --text <t>` (orca_term.py:125), `worktree list` (sessions.py:311) and `terminal create --worktree path:<w>` (waker.py:187) **[CODE-VERIFIED]** (files under /home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/agent-work-report/scripts/). The design's DQ2 says the poll reuses this pattern (DESIGN:112 cites `orca_term.py:31-58`, `waker.py:144-169`).
- The built `issue_watch` launcher builds a 12-element `orca agent launch` argv (launch.py:95-131) **[CODE-VERIFIED]**; DESIGN:112 and PR A (open) make the poll stop launching work and only wake.

Counts: observer 3 templates; sweep 10 templates (6 called); the design names about 30 distinct Orca verb forms (rows 1-34 above). Token-for-token matches with an existing allowlist: row 12 `worker-show --dispatch <id> --json` (sweep), row 13 second form `worker-list --run <id> --json` (sweep), row 8 first form `task-list --run <id> --json` (sweep) and row 28 `worktree current --json` (sweep, pinned and never called). No designed argv matches one of the observer's three templates. Every write or consuming verb of the design (rows 4, 5, 7, 9, 10, 16-20, 24-26, 30, 32-34) is on the observer's forbidden list or outside the sweep's read-only allowlist by construction.

Key Takeaways
- Read side overlap in Orca verbs is limited to `worker-list`, `worker-show`, `task-list` and (pinned only) `worktree current`; the design reads them with different option sets (`--terminal-state reclaimable`, no `--limit 100`, `run-current --json`).
- The orchestrator is the only one of the three families designed to send messages, type into terminals, start workers and release Dispatches; the observer and sweep allowlists forbid all of those.
- Neither the observer nor the sweep reads `terminal list/read`, `worker-read` or the Run mailbox (`check`), all of which the design uses for its watch loop.

## 4. The FR-9 follow-up state set and its mapping to `worker-list` fields (question b)

Facts from DESIGN:
- Set (DESIGN:648; also DESIGN:560, 666, 712, 744, 1105, 1134): `working, question, gated, delivered, claimed-missing, stalled, failed, not-started` (8 values). Named "the FR-9 set" and defined in the coordinator spec `SPEC-AGENT-WORK-COORDINATOR-20261027.md`, FR-9. That spec is NOT in the snapshot or the checkout (Glob `**/SPEC-AGENT-WORK-COORDINATOR*` under /home/coder returned no file); DESIGN:1024 says it lives in IronFlow `.dev/specs/` and O2 copies it to the orchestrator repo. So the per-state definition of FR-9 is **[UNVERIFIED]** here.
- Source data (DESIGN:572): "`orca orchestration worker-list --json` (FR-9: `projection.liveness`, `attention`, `nextAction`)". DESIGN:744: "sorts each worker it started into an FR-9 state ... `worker-list --run <id> --json`, `worker-show --dispatch <id>`; `orca terminal list ...`; `ccsession --list`". DESIGN:1134 (T6): "`worker-list` states map to the FR-9 states" for three scripted workers (exits at once, stays silent, sends one `ask`).
- The design contains NO table or rule that maps a given `projection.liveness`, `attention` or `nextAction` value to an FR-9 state. Grep for `projection|liveness|claimed-missing` on DESIGN: `projection` and `liveness` only at line 572; `claimed-missing` only at line 648. **[UNVERIFIED]** how the mapping is made; it is deferred to the coordinator spec (FR-9) and to test T6.
- The same eight words are the "follow-up state" header line of the report entry template (DESIGN:648) and a check: "a follow-up state outside the FR-9 set fails" (DESIGN:1105). Derived rule in DESIGN:712: an issue whose orchestrator is down is `stalled` with reason "orchestrator <id> is down, restart in progress" (a state set by the poll's registry, not by `worker-list`).
- Session-status words in the same entry (DESIGN:558): `session_status` map, status one of `working, progressed, waiting on you, stuck, stalled, done`: the six AWR statuses (research 05 section 24; common.py `SESSION_STATUSES`). Two different words appear in both sets: `working` and `stalled`.

Built vocabularies in the snapshot, set against it (all different source, same Orca data where noted):
1. Observer: no class vocabulary of its own. `RowView` keeps `worker_state`, `dispatch_status`, `terminal_state`, `outcome`, `next_action`, `liveness` as separate text fields from the `worker-list` row (observe/view.py:566-584) **[CODE-VERIFIED]**; the live sample carries `projection.attention` which the observer does not parse (research 06 line 183, [UNVERIFIED] meaning).
2. Sweep: 8 classes `models.CLASSES` (models.py:50-59): `waiting on a person, stalled (proved), fenced, working, finished, idle, person session (active), could not determine` (research 03 section 2); plus `PACKAGE_STATES` (models.py:62). Reads `worker-list`, `worker-show`, `task-list`, `worktree ps --json`.
3. AWR report: six session statuses (above) + group/priority classes, judged by the model from transcript facts; "Orca's own state is never read" (SKILL.md:38, per research 05 section 24).
4. Orchestrator design: FR-9 set (eight words) over `worker-list` fields. The design also uses per-issue state-file statuses and return-contract outcomes: `in_progress` (DESIGN:536), `done` (DESIGN:631), `escalated` (DESIGN:523, 799) and the contract outcomes `merged_closed, escalated, skipped, failed, in_progress` (DESIGN:525).
5. WORKER-CONTRACT.md: a liveness ladder S0 to S11 (`starting, progressing, long step, idle at prompt, blocked on a person prompt, blocked in ask, context exhausted, unreachable, exited, finished but unreported, settled, unknown`) with rungs L0-L5 (WC:116-129, 148-155) **[CODE-VERIFIED]**. The design never cites it: a search of DESIGN for `Liveness supervision`, `stall proof`, `agentWait`, `agent-wait` and `WC-6` returned no hit.
So there are at least five status vocabularies over overlapping Orca and transcript data: observer fields, sweep 8 classes, AWR 6 statuses, FR-9 8 states and WC S0-S11 (plus the design's own state-file statuses and contract outcomes).

Key Takeaways
- The design adds an FR-9 state set derived from `worker-list`, but does not state the field-to-state mapping; the mapping lives in the coordinator spec (not available here) and is tested only by T6 (DESIGN:1134).
- `projection.attention` is named by the design as an FR-9 input (DESIGN:572) and is the same field the observer receives but does not parse (research 06).

## 5. What the design changes in WORKER-CONTRACT.md, and whether WC-16 is among it (questions c, d)

Method: the design's own statements (DESIGN:116-119, 135, 480, 637, 991, 1017, 1020), then the snapshot file (`WC`, 339 lines) and the PR D diff (`git show 01e7a9e23519fd54bc438bb1a1a0e03dcdae5baf -- src/superclaude/core/WORKER-CONTRACT.md`, read-only; PR #682 merged 2026-11-20T00:02:36Z).

| # | Design statement (line) | Snapshot state | Tag |
|---|---|---|---|
| a | Drops WC-17 "Plan approval is the reply to the worker's own ask" (DESIGN:991, 1017, 1381) | PR D diff hunk `@@ -59 +58,0 @@` removes the WC-17 bullet; grep of WC for `WC-17|Plan approval|issue-pipeline` returns no match | **[CODE-VERIFIED]** done by PR #682 |
| b | Drops the "### Issue pipeline duties" section "line 291 to the end of its bullets, 300" (DESIGN:991) | PR D diff hunk `@@ -291,11 +290,0 @@` removes the heading and six bullets (Adopt, Reserve, Worktree then worker, Plan approval, Route B, Never); WC:291 is now "### Worked example: gate hit, answer, new Task" | **[CODE-VERIFIED]** done by PR #682 |
| c | Cites "`WORKER-CONTRACT.md:300` (issue write needs a grant row, retires with the duties)" (DESIGN:116) | line was inside the removed section; WC:300 is now inside the brief template | retired; design line number is now **[STALE DOC]** (design read base 89dc403d4) |
| d | Adds one section "Orchestrated issue flow" in PR B, with the brief line `Flow: orchestrated-issue` and a test change in `tests/skills/test_worker_contract.py` (DESIGN:135, 637, 1020) | grep of WC for `Orchestrated issue flow` and `orchestrated-issue`: no match; PR B has no pull request (research 05 section 18) | **[DESIGN-ONLY]**; not built |
| e | "Everything else in the contract is unchanged" (DESIGN:135, last sentence) | n/a | design statement; so WC-16 (WC:287-289), WC-10 (WC:46), the never-as-worker list (WC:23), "Liveness supervision" (WC:95-200), "The sweep." (WC:110) and "Git and GitHub ownership" (WC:239-246) are NOT slated to change by the design |
| f | Cites the never-as-worker list at "`WORKER-CONTRACT.md:23`" and the coordinator rule "PRs go only through `/sc:pr-submit` ... never as a worker" at ":244" (DESIGN:135, 480) | WC:23 holds the list (`/sc:agent, /sc:closeout, /sc:git, /sc:help, /sc:issue, /sc:pm, /sc:sweep, /sc:swarm-wizard`, plus `/sc:pr-submit` while D3 keeps it off workers); WC:244 holds the PR rule | **[CODE-VERIFIED]** |
| g | Cites WC-9 at ":44-47" (DESIGN:135) and WC-12 (DESIGN:119) | WC-9 is now at WC:41-45 and WC-12 at WC:61 | **[CODE-VERIFIED]** the rules exist; the design's line numbers for WC-9 are **[STALE DOC]** by 3 lines |
| h | Says the contract "lists `/sc:pr-submit` as never-as-worker" and "WC-9 switches every push, PR and GitHub post off for a worker and no brief can turn them on" (DESIGN:135) | WC:23 and WC:41 | **[CODE-VERIFIED]** |

WC-16 position: WC-16 "Coordinator loop" is WC:287 (heading) and WC:289 (text) **[CODE-VERIFIED]**. It was NOT touched by PR D (diff hunks are only at old lines 59, 66 and 291-300). The design does not mention WC-16 anywhere (section 2). By the design's own sentence "Everything else in the contract is unchanged" (DESIGN:135) WC-16 is not among the lines the design changes or removes. The design edits listed under 6.3 (C1 to C29, DESIGN:897-926) are all to the coordinator spec `SPEC-AGENT-WORK-COORDINATOR-20261027.md`, none to WORKER-CONTRACT.md. DESIGN:1020 also puts `src/superclaude/core/HOW-WE-WORK.md` and its plugin copy into PR B (to name `/sc:orchestrator`); HOW-WE-WORK.md already carries the WC-16 sentence (HOW-WE-WORK.md:359) and the `/sc:sweep` routing row (HOW-WE-WORK.md:298) in the snapshot **[CODE-VERIFIED]**.

Who the contract's coordinator rules bind: WC:70 "These bind the coordinator: an Orca coordinator session the person opened." DESIGN:135 says "the coordinator is 'a session the person opened'" and that the new section defines the orchestrator as "a standing-grant coordinator that may be started by a script, whose outward actions are exactly the `grants` list (DQ6)". DESIGN:799 says "The orchestrator is a standing-grant coordinator and not a worker (ADD1)". DESIGN:930 says "the orchestrator is the coordinator" that FR-5, FR-6, FR-8, FR-9, FR-21, FR-22 and FR-26 to FR-28 describe. Whether WC-16's `/sc:sweep` duty (and the rest of section 4) binds a script-started orchestrator is therefore not stated in the design, and the new section that would say so does not exist yet. **[UNVERIFIED]**

Contract rules a reader may set against the design's wave 5 (facts, no conclusion):
- Wait call. WC:101: `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000`, and WC:196 "The coordinator always lists every type"; WC:105 "An unknown type puts its sender in S11". DESIGN:572: `check --wait --types "worker_done,escalation,question,status" --timeout-ms 240000`. The type lists differ (4 versus 9) and the timeouts differ (240000 versus 300000). The 4-minute figure matches WC-10's cap on a single blocking wait (WC:46; DESIGN:580 "Each blocking wait is at most 4 minutes (WC-10)").
- Typing and approvals. WC:122 (S4: "never answer the prompt"), WC:137 ("Input veto: never interrupt; never type into a busy, S11 or S4 session; never answer a person prompt"), WC:188 ("On silence, a passed deadline, `unverifiable` liveness or screen text alone, the coordinator never ... answers a permission or person-only prompt"). DESIGN:573 (seven rules; a single-use yes is typed for an approval), DESIGN:119 (DQ9) and DESIGN:749 (N7: one interrupt of a worker's turn, after the escalation is written). The design changes the coordinator spec (C25-C29, DESIGN:922-926) for these, not the contract; DESIGN:1020 does not list the contract's Liveness supervision section as edited.
- Restart. WC-6 (WC:72-80): every retry is a new Task, never `--retry-of`. DESIGN:567/1104: a lost `worker-start` is checked once with `worker-list`/`request-show` and started once more only if none exists (ruling R5), and DESIGN:1279 plans `worker-start --retry-request <uuid>` (an Orca idempotency token, U-row). The design does not cite WC-6.
- Merge and close. WC:239-246, WC:244 (coordinator merges only on the person's instruction; `merge_ready` merges only on the person's instruction, WC:108) against DESIGN:586-602 (wave 7: `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>` by the orchestrator when every condition holds). DESIGN:135 states this contradiction itself and resolves it by the new section (d).

Key Takeaways
- PR D (merged) already did the contract deletions the design lists; PR B's addition ("Orchestrated issue flow") is not built; WC-16, WC-10 and the never-as-worker list are not among the lines the design changes.
- The design nowhere cites WC-16, WC-6 or the liveness ladder; it cites WC-9, WC-10, WC-12, the never-as-worker list and "Git and GitHub ownership".

## 6. What the orchestrator does at a wake, against the coordinator "The sweep." and WC-16 (question e)

Orchestrator side (design text):
- Delivery (DQ2, DESIGN:112; section 3): the poll writes a wake file, sends an Orca mailbox message to `run:<run id>` and, only when the session is idle at its prompt with no unsent typing and no output in 60 seconds, types one line `/sc:orchestrator --wake <wake_id>`. No acknowledgment in 10 minutes means the same issues are sent again (attempts 2 and 3), then `abandoned` and exit 7.
- Wave 0 on a wake (DESIGN:532-539): `orca skills get orchestration`; `run-current`; `run-create` or `run-use`; `superclaude orchestrator wake-check <wake_id>`; `repos check`; `git -C <checkout> remote get-url origin`; `gh issue view <N> --repo <R> --json state,assignees,comments`; writes an acknowledgment file; creates one state file per new issue with `O_EXCL`; handles `plan_requests[]`.
- Wave 5 loop while workers run (DESIGN:570-573, DQ10 at DESIGN:120): `check --wait` blocks on the Run mailbox (at most 240000 ms), `--ack` after handling; once an hour per running worker, Monday to Friday, 24 hours a day, the loop runs a status check that reads `worker-list` and `gh issue view <N> --json state,assignees`; `/sc:orchestrator --hourly` runs the same check once on request. The check for a worker stops at its `worker_done` or at wave 9 (DESIGN:120, 630).
- Poll cadence (DQ10): a separate Orca automation `orchestrator-poll`, `*/5 * * * *`, 24x7, that reads GitHub; "the worker status check has no automation of its own" (DESIGN:120).

Coordinator side (contract text):
- "The sweep." (WC:110): after every wake or timeout, at most once every 5 minutes: one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path (WC-11), updating each worker's heartbeat record; costly probes (transcript tail, screen read) only for triggered workers.
- WC-16 (WC:289): on every coordinator wake or wait timeout, at most once every 5 minutes, run "The sweep." unchanged and, in the same pass, run `/sc:sweep` and read its report before acting; `/sc:sweep` "does not update heartbeat records or run the `worktree ps --agent-wait` listing"; the report is a dated local file, never posted; it recommends nothing; the coordinator keeps the pass scheduled while work remains.

Side-by-side facts:
| Item | Orchestrator design | WORKER-CONTRACT.md |
|---|---|---|
| Trigger | poll wake (typed line or mailbox); mailbox messages in the wave 5 loop; hourly status check per worker | every coordinator wake or wait timeout, at most once per 5 minutes |
| `worker-list` | hourly check (DESIGN:572, 744) and wave 9 (`--terminal-state reclaimable`) | one per sweep (WC:110) |
| `worktree ps --agent-wait` | not in the design | one per sweep (WC:110) |
| `stat` of the worker's contract path | not in the design (the design reads `worker_done` from the mailbox and evidence under `{{report_dir}}`, DESIGN:645) | one per worker per sweep (WC:110) |
| Heartbeat record | mailbox heartbeat "handled once by its id" (DESIGN:1104); no record or deadline W | heartbeat record per worker; deadline W = max(10 min, 2 x median interval) capped at 45 min (WC:112) |
| `/sc:sweep` | never named | run in the same pass (WC:289) |
| Output | per-issue state files, report entry files, return contract (DESIGN:525) | run notes; dated local `/sc:sweep` report under `.dev/sweeps/` (research 04) |
| Who acts | the orchestrator acts (check-ins, typed keys, approvals, interrupt in one case, merge, close) | the coordinator decides; `/sc:sweep` recommends nothing (WC:289) |

Cross-references in the other direction (snapshot code): grep of `src/superclaude/cli/sweep`, `src/superclaude/cli/observe` and `src/superclaude/skills/sc-sweep-protocol` for `sc:orchestrator|orchestrator-<short>|issue-watch|issue_watch|orchestrated/|\.orchestrator/|report-entry|agent-work-report` returns no match in any of the three folders **[CODE-VERIFIED]**. A grep of `src/superclaude/skills/agent-work-report` for `/sc:sweep|superclaude sweep|observe` returns only the unrelated ClickUp `sweep` function (clickup.py:13, 150, 418, 425). The only snapshot files naming `.dev/sweeps`, `/sc:sweep` or `superclaude sweep|observe` are the sweep and observer packages, `commands/sweep.md`, `commands/closeout.md`, `core/HOW-WE-WORK.md`, `core/WORKER-CONTRACT.md`, `output-styles/pragmatic.md` and `skills/sc-sweep-protocol/SKILL.md` (grep, 15 files). `commands/closeout.md:99` lists `/sc:sweep` in its Related Commands table ("A read-only snapshot of a Run and its worktrees; it changes nothing"). Same table, `commands/closeout.md:97`: "`/sc:issue --plan <N>` is how the orchestrator updates a plan after a not-done result"; the snapshot's `commands/issue.md` has no `--plan` text (grep count 0, PR P #690 is open), so that sentence is a forward reference **[STALE DOC]** until PR P merges.

Key Takeaways
- The two descriptions share one fact source (`worker-list`) and one blocking-wait cap (4 minutes) and differ in cadence (event driven plus hourly versus per wake at most every 5 minutes), in extra reads (`worktree ps --agent-wait` and contract `stat` are in the contract's sweep only), and in whether `/sc:sweep` is called (the contract's WC-16 yes; the design never).
- Nothing in the sweep or observer code or skill refers to the orchestrator, the poll or the report entry files.

## 7. Built versus designed, as of the snapshot (origin/master 61ac2c2e6)

Existence checks run read-only in /home/coder/.cache/ic-snap-20261120/master:

| Item | Where the design puts it | Snapshot | Tag |
|---|---|---|---|
| `/sc:orchestrator` command | `src/superclaude/commands/orchestrator.md` (PR B, DESIGN:1020) | absent | **[DESIGN-ONLY]** |
| orchestrator skill | `src/superclaude/skills/sc-orchestrator-protocol/` (PR B) | absent | **[DESIGN-ONLY]** |
| `superclaude orchestrator` verbs (`wake-check, wake-ack, state, lease, merge-gate, plan-check, repos, report-entry, escalate, answer-check, audit, handback`, DESIGN:510) | `src/superclaude/cli/orchestrator/` (PR B) | directory absent; the only mentions of `report-entry` are in `agent-work-report` (check.py:77, common.py:136, run.py:688) and `sc-closeout-protocol` (SKILL.md:21, refs/settle.md:99, scripts/settle.sh:1037-1042), all of which expect the verb | **[DESIGN-ONLY]**; callers exist, the command does not |
| poll that wakes an orchestrator (`wake.py`, `repos.py`, `route.py`, `hold.py`) | PR A (#686) | `src/superclaude/cli/issue_watch/` holds `audit.py cli.py cycle.py github.py launch.py predicates.py record.py runner.py`; `repos.py` and `hold.py` absent | PR A open, unmerged |
| `/sc:issue --plan` and `--remaining` | PR P (#690) | not in snapshot (PR open) | open, unmerged |
| retire the plan-approval gate | PR D (#682) | `src/superclaude/cli/issue_pipeline/` absent; WC-17 and "Issue pipeline duties" gone; `launch-level-guard.sh` still mentions `issue-pipeline` in a comment at line 496 ("the rule 1 text of that design is retired") | **[CODE-VERIFIED]** merged |
| report skill in IronClaude with the living report (`exclude.py`, `run.py refresh`) | PR C (#684) | `src/superclaude/skills/agent-work-report/` present with `exclude.py`, `run.py` `refresh` (run.py:629), 16 script files in `scripts/` | **[CODE-VERIFIED]** merged |
| closeout skill | issue 668 (#683) | `skills/sc-closeout-protocol/` and `commands/closeout.md` present | **[CODE-VERIFIED]** merged |
| orchestrator repo `IronbellyOrg/IronOrchestrator` | O1 (DESIGN:1023, OD8 DESIGN:1159) | outside IronClaude; not checked here | **[UNVERIFIED]** |
| orchestrator-poll automation (`*/5 * * * *`) | O3/O4 owner-run (DESIGN:1025) | not checkable from the snapshot | **[UNVERIFIED]** |

Key Takeaways
- Three of the design's five IronClaude pull requests are merged (design #681, D #682, C #684) plus issue 668's closeout (#683); A (#686) and P (#690) are open; B (the orchestrator skill and verb group) has no pull request.
- The sweep and the observer are built and merged (PR #539 for the sweep, merged 2026-11-14T17:41:26Z); the orchestrator is not.

## 8. The pull request chain (read-only `gh pr list` and `gh pr view`, `--repo IronbellyOrg/IronClaude`, 2026-11-20)

| PR | Title (short) | State | Merged (UTC) | Size | Relation |
|---|---|---|---|---|---|
| #539 | feat(sweep): read-only `superclaude sweep` and `/sc:sweep` (Phase 1 of orchestrator mode, #339) | MERGED | 2026-11-14T17:41:26Z | 2290 files, +306957 | its body says it adds "the WC-16 coordinator-loop rule" and lists known limits tracked in issue #534 ("the 'working' rule is inert and the agent-wait rule is dark"); research 03 records `working` is produced since 2026-11-16, so that body sentence is **[STALE DOC]** for `working` |
| #587, #588 | docs(dev): record the orchestrator, observer and issue-watcher alignment decisions (#339) and fix three review findings | MERGED | 2026-11-17T06:04:21Z and 06:32:09Z | 58 files in #587, under `.dev/brainstorms/20261113-orchestrator-tui-alignment/` | decision records under `.dev/`; contents not read in this pass (outside the scope list) |
| #434 | docs(orca): add the v1 worker-liveness rules to the worker contract | MERGED | 2026-11-08T01:53:33Z | n/a | by its title, adds the v1 liveness rules; the section is "Liveness supervision" (WC:95-200) |
| #681 | docs(design): approved orchestrator design for issue 655 (docs only) | MERGED | 2026-11-20T00:02:33Z | 1 file, +1412 | the design under study (`docs/designs/orchestrator.md`) |
| #682 | refactor: retire the old plan-approval gate (PR D) | MERGED | 2026-11-20T00:02:36Z | 36 files, +35/-4599 | WORKER-CONTRACT.md: 13 lines changed |
| #683 | feat(closeout): `/sc:closeout` and `sc-closeout-protocol` (issue 668) | MERGED | 2026-11-20T01:16:58Z | 27 files, +6889 | called by orchestrator wave 8 (DESIGN:799) |
| #684 | feat(agent-work-report): move the report skill into IronClaude and add the living report (PR C) | MERGED | 2026-11-20T02:01:07Z | 28 files, +10488 | reader side of the living report |
| #686 | feat(issue-watch): the poll wakes the repo's orchestrator (PR A) | OPEN, not draft | not merged | 59 files, +14306/-16637 | reshapes `issue_watch/` |
| #690 | feat(issue): `/sc:issue --plan` and `--remaining` (PR P) | OPEN | not merged | 13 files, +2811/-39 | plan mode used by orchestrator wave 0 |
| none | PR B (orchestrator skill and verb group) | no pull request found (`--search "orchestrator"`, `--search "issue 655"`) | n/a | n/a | |
Other open PRs at the time (`gh pr list --state open`): #693 (issue 691, save the claim launch result as `launch-result.json`) and #685 (issue #442 runbook); neither is in the orchestrator or sweep scope.

sc-closeout design touch points (`/home/coder/.cache/ic-snap-20261120/master/docs/designs/sc-closeout.md`, 753 lines): it does not mention `/sc:sweep`, WC-16 or the observer (grep `sweep|observer` returns only line 47, "anything else in Jay's repository, such as its pull request sweep", scope exclusion). It names the coordinator and orchestrator at: D10 (line 66) the work report entry is settled only through `superclaude orchestrator report-entry --key <key> --closed`, absent means the entry item is `escalated` (`why=surface_absent`, lines 368, 374); D12 (line 68) `/sc:closeout` goes on the never-as-worker list (present at WC:23 **[CODE-VERIFIED]**); line 379 the task lookup uses `orca orchestration task-list --json` and the task titled `<owner>/<repo>#<N>`; D22 (line 78) a `not_done` verdict hands back to the orchestrator. Line 361 ("`agent-work-report` is in the IronFlow repo ... `report-entry` and `orchestrator_repo` appear nowhere under `src/`") was true on 2026-11-19 and is now **[STALE DOC]** for the first half (PR C moved the skill); the `report-entry` half is still true in the snapshot (section 7).

Key Takeaways
- The chain the owner will see: merged #539 (sweep, WC-16) and #434 (liveness rules) on the one side; #681, #682, #683, #684 merged and #686, #690 open and PR B unopened on the orchestrator side.
- The closeout skill is the only artifact outside the orchestrator package whose code already calls a future `superclaude orchestrator` verb.

## 9. C8 determination for this gap (defect candidates)

C8 asks for a DEFECT or DEFECT-CANDIDATE when a spec or design names a capability as shipped or enabled that is not wired at its runtime entrypoint, unless a cited on-record scope decision exists.
- The orchestrator design describes unbuilt capabilities (status line DESIGN:3: "It holds no implementation code. The build starts from this text"; PR split DESIGN:1015-1026, order DESIGN:1028-1046), so its unbuilt `/sc:orchestrator`, `superclaude orchestrator` verbs and "Orchestrated issue flow" section are not "named as shipped or enabled". No DEFECT-CANDIDATE is raised for them by this file. On-record decision for the sequencing: DESIGN:1011-1046 (order D, A, P, B; B opens after A merges) and owner ruling 37 (DESIGN:3).
- Wiring gap that touches the sweep family: callers of a verb that does not exist yet. `agent-work-report` (check.py:77, common.py:136), `sc-closeout-protocol` (settle.sh:1037-1042) already name `superclaude orchestrator report-entry`; the closeout handles the absence with `ENTRY escalated why=surface_absent` under the on-record decision D10 (sc-closeout.md:66, 368, U1 at refs/settle.md:99). That is a cited decision, so it is a documented limit, not a new candidate. The AWR writer side is for GF-1 (reconciliation) to carry.
- WC-16 and the design: WC-16 (shipped, merged in #539) says the coordinator runs `/sc:sweep` on every wake; the design (unbuilt) describes an orchestrator that is "the coordinator" (DESIGN:930) and has no step that runs `/sc:sweep`. No on-record decision was found that says the orchestrator is exempt from WC-16 or that it is covered. I record this as an OPEN QUESTION OF SCOPE, not as a defect: the orchestrator does not exist, so no shipped capability is unwired today. If the owner reads WC-16 as binding the future orchestrator, the design has a gap against a shipped rule. Remediation task not created (read-only brief); flagged for the owner.

## 10. Other overlaps in data and files (facts)

- Run scoping. The orchestrator makes one Orca Run per orchestrator (`run-create`, `.orchestrator/runs/<id>.json`, DESIGN:94, 115) and `run-use`s it after a restart. The sweep binds a Run with `orchestration run-current` or `--run` (research 04 table row 1; commands.py:264-266) and the observer takes `--run` for `worker-list` and requires a named Run for `--questions` (research 01). So with N orchestrators there can be N Runs; both read-side tools take one or more named Runs and neither lists Runs by orchestrator tag. The observer's `--questions` template (`check --all --types question --run <runId>`) reads the same Run mailbox the orchestrator's wave 5 consumes with `check --wait`; the observer form never carries `--ack` or `--wait` (adapter.py:34-50), so it does not consume messages. DESIGN:112 makes the orchestrator's Run mailbox the durable wake channel (`orchestration send --to run:<id>`).
- Sessions with no worker Dispatch. Orchestrator sessions (tag `orchestrator-<short>-<n>`) and the report session (tag `coordinator`) run in the orchestrator repo's Orca workspace (DESIGN:93, 714) and are not workers. Under the shipped `JOIN_PATH = "B"` the sweep prints `could not determine` for any un-joined transcript while any non-ready Dispatch row exists in the scoped Runs, and a transcript with a tab-map entry gets the note "Orca pane session, not in scoped Runs" and no person class (research 03 section 4.5, classify.py:760-779). No test or text in the snapshot names an orchestrator session; **[UNVERIFIED]** how a live orchestrator session would be classified.
- Files written. Sweep: one `.dev/sweeps/<UTC>-sweep.md` per run (research 04). Observer: state dir `snapshot.json` v1 and `observe-<ts>.txt` (research 01 section 6). Orchestrator: `<orchestrator-repo>/.orchestrator/{runs,issues,handoffs}/...`, `.dev/coordinator/orchestrated/<owner>__<repo>__<N>.json` entry files and `report.html` (DESIGN:115, 122, 558). No path is shared between the three; the entry files are the one place the design and the AWR skill meet (research 05 sections 15, 26).
- Per-issue entry fields set against the sweep row fields: the entry carries the worker's session link `orca://session/<id>` and the Orca session ids (DESIGN:558, 648); the sweep row is keyed by Orca Dispatch and transcript (research 03); the observer by Run, Dispatch and worker identity (view.py:566-584). No code joins them today.
- Claim layer. The design's claim is `/sc:issue --claim <N> --pipeline none` (DESIGN:544) and the poll today launches through `orca agent launch` (launch.py:95-131). Neither the sweep nor the observer reads issue state, GitHub or `issue-watch` files (grep, section 6).
- Audit versus sweep. The design's post-merge `superclaude orchestrator audit` is computed from GitHub only (DESIGN:803) and says "the sweep is not adopted" for pull requests; it is a different "sweep" from `/sc:sweep` (section 2).

## Gaps and Questions

1. **[UNVERIFIED]** FR-9 definitions and the mapping of `worker-list` fields to the eight FR-9 states: the coordinator spec `SPEC-AGENT-WORK-COORDINATOR-20261027.md` is not in the snapshot or checkout (Glob under /home/coder found none); DESIGN names only the set (DESIGN:648) and the source fields (DESIGN:572). Needs the spec (IronFlow `.dev/specs/` or the orchestrator repo copy per O2).
2. **[UNVERIFIED]** Whether WC-16 (and the rest of WC section 4) binds a script-started orchestrator. DESIGN:135 defines the orchestrator in a PR B section that does not exist yet; WC:70 says the coordinator is "a session the person opened".
3. **[UNVERIFIED]** Whether PR B's "Orchestrated issue flow" section will touch WC-16, WC-10, the never-as-worker list or the Liveness supervision section. The design says "Everything else in the contract is unchanged" (DESIGN:135); its C-list edits the coordinator spec, not the contract.
4. **[UNVERIFIED]** How the design's typed approvals (DESIGN:573) and the one interrupt (DESIGN:749) relate to WC:122, 137 and 188 ("never answer the prompt", "never interrupt", "never ... answers a permission or person-only prompt" on silence); the design reconciles only in the coordinator spec (C25-C29).
5. **[UNVERIFIED]** The type list and cadence of the orchestrator's `check --wait` (4 types, 240000 ms) against WC:101 and WC:196 (9 types, 300000 ms, "always lists every type").
6. **[UNVERIFIED]** How the sweep classifies a live orchestrator or report session (no test or doc names one; section 10).
7. Not read in this pass (out of the scope list, noted so synthesis does not claim coverage): design sections 3.x wake file schema in full (DESIGN:143-250), 4.x poll internals beyond the lines cited, 5.7 registry detail beyond DESIGN:706-716, 5.8, 5.12, 6.1/6.2, 6.4 reader table (DESIGN:932+), 7.x, 9.x tests beyond rows quoted, 11 risks, 12 UNVERIFIED rows U1-U57 beyond rows quoted, 13 coverage matrix; the alignment decision records of PR #587/#588 (`.dev/brainstorms/20261113-orchestrator-tui-alignment/`, 58 files); the unmerged branches of PR #686 and #690 beyond research 05 section 19.
8. Open fact (not a defect): `projection.attention` is an FR-9 input in the design and an unparsed key in the observer; its meaning is unverified in both (research 06 line 183).
9. DEFECT-CANDIDATE: none raised by this file (section 9); remediation task not created (read-only brief); flagged for the owner: the WC-16 versus design question (Gap 2).

## Stale Documentation Found

- DESIGN:116 and DESIGN:135 cite `WORKER-CONTRACT.md:44-47` for WC-9 and `:300` for "issue write needs a grant row"; the snapshot has WC-9 at WC:41-45 and the `:300` text was removed by PR #682 **[STALE DOC]** (design written against base 89dc403d4).
- DESIGN:991 and 1017 describe the PR D deletions as future work; they are done (PR #682 merged 2026-11-20T00:02:36Z) **[STALE DOC]** as a status, accurate as a description.
- DESIGN:1017 says the guard comment sits at `launch-level-guard.sh:500`; the snapshot has it at line 496 (minor drift).
- DESIGN:122 treats `run.py refresh`, `exclude.py` and the ClickUp re-homing as UNVERIFIED; the code exists on master (research 05 section 17) while no live run is recorded.
- `docs/designs/sc-closeout.md:361` ("`agent-work-report` is in the IronFlow repo") is stale for the skill location (PR #684 moved it); the `report-entry` half remains true.
- `src/superclaude/commands/closeout.md:97` names `/sc:issue --plan <N>` which is not yet in `commands/issue.md` (PR #690 open).
- PR #539 body says the `working` rule is inert; research 03 records `working` is produced since 2026-11-16 (`test_cli_contract.py:1133-1160`).
- The design names ADD6's verb list without `report-entry` and `plan-check` while its 5.1 package row lists both (research 05 section 17): an internal inconsistency of DESIGN:140 versus DESIGN:510.

## Summary

- The approved orchestrator design (DESIGN, 1412 lines, merged by PR #681) never mentions `/sc:sweep`, `superclaude sweep`, WC-16, WC-10 as a sweep rule, the observer or `.dev/sweeps`; it cites WC-10 only for the 4-minute wait cap, and the never-as-worker list for `/sc:issue` and `/sc:closeout`. It says the orchestrator "is the coordinator" the coordinator spec describes (DESIGN:930), and WC-16 (WC:287-289) tells the coordinator to run `/sc:sweep` on every wake.
- The design adds a fourth status vocabulary (FR-9: 8 states over `worker-list` `projection.liveness`/`attention`/`nextAction`, mapping not stated) next to the observer's raw fields, the sweep's 8 classes and the report's 6 statuses, and WORKER-CONTRACT.md has a fifth (liveness S0-S11). Of about 30 Orca verb forms the design names, 4 match a sweep template token for token, none match the observer's 3; every write or consuming verb is outside both read-only allowlists.
- Built versus designed: design (#681), plan-gate retirement (#682), closeout (#683) and the report skill with the living report (#684) are merged; the poll rework (#686) and `/sc:issue --plan` (#690) are open; the orchestrator skill, its `superclaude orchestrator` verbs (including `report-entry`, already called by closeout and the report skill) and the contract's "Orchestrated issue flow" section have no pull request. PR D already removed WC-17 and "Issue pipeline duties"; it did not touch WC-16. No unification is recommended here.
