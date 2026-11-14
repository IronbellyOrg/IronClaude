# Review 04: Orchestrator v2 (#423) alignment with v1 (#339 / PR #539) and the TUI observer (#409)

Reviewer: independent, read-only (no GitHub writes, no repo edits except this file). Date: 2026-11-13.
Status: COMPLETE.

## Scope read

Read live on 2026-11-13 (nothing relied on from the lead's brief without a re-read):

| Source | Version / state | What was read |
|---|---|---|
| #423 (IronbellyOrg/IronClaude) | OPEN, updated 2026-11-08T10:16:24Z | Full body; the one comment (2026-11-08T07:03:53Z, #331 built via PRs #447/#448, rollout #450) |
| #339 | OPEN, updated 2026-11-07T11:53:40Z | Body; all 5 comments (2026-11-05T13:43:07Z never-stop-polling and orchestrator-of-orchestrators; 13:45:07Z trustless-layer proposal; 2026-11-07T06:31:33Z owner answers; 07:30:05Z accuracy check, `out_of_date`; 07:30:07Z claim summary) |
| #444 | OPEN | Body and 2 comments (accuracy check 2026-11-08T17:59:08Z, claim summary) |
| #534 | OPEN | Body (Phase 1 follow-ups), no comments |
| #450 | OPEN | Body (watcher rollout) |
| PR #539 | OPEN, head `873599d59bc9563c459d39c1dcdf323aa3e8cb6a` (matches checkout HEAD) | Title and body |
| #409 | New body at `/tmp/pr339/i409-new-body.md` (read in full) | Alignment decisions 1-10, Plan, Related |
| Coder#477 (IronbellyOrg/Coder) | OPEN | Body and owner comment of 2026-11-13T16:20:07Z ("Ensure this aligns with Orchestrator and TUI Panel") |
| Design | `docs/designs/orchestrator-mode.md` in the checkout, HEAD 873599d59 | Sections 1, 6, 7.2 (data model), 7.3 (allowlist), 7.4 (JSON schema v1), 7.5 (report layout), 7.6, 8 (WC-16) |
| Code | `src/superclaude/cli/sweep/{report,models,probes,classify,commands}.py` | `to_json` (report.py:613-681), dataclass fields (models.py), allowlist (probes.py:62, :1276), `--run` option (commands.py:221) |
| Contract | `src/superclaude/core/WORKER-CONTRACT.md` at HEAD | WC-3, WC-9, WC-10, WC-11, WC-12 (:61), WC-13 (:62), WC-16 (:286-288), coordinator rules |
| Routing / docs | `src/superclaude/core/HOW-WE-WORK.md:335,406`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:972` | Sweep rows, section 7.7 |
| #423 components | `src/superclaude/commands/pm.md`, `skills/sc-pm-protocol/SKILL.md`, `commands/spawn.md`, `cli/issue_watch/`, `pm_agent/reflexion.py`, `docs/memory/` | Existence and role |
| Technical reference | `origin/master:docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`, section 14.3.1 (C1 to C19) | Read C8, C9 closely; scanned the rest |
| Research | `RESEARCH-REPORT-orchestrator-mode.md` "Later phases" table (about lines 1318-1334); `RESEARCH-REPORT-sub-orchestrator-mode.md` (grep for catalogue, cross-agent, trust, depth only; NOT read in full) | UNVERIFIED beyond the hits |
| Phase 2 input | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/PHASE2-preflight-input.md` | Full (owner reading list; no v2 content) |

Not done: no live Orca run, no read of #409's design branch `origin/docs/409-orca-dashboard-designs` (so "Collision Lens" and the other 19 designs are known by name only), #431 read by title only.

## Claim check of #423

Each claim in "Components Affected" and "Related Issues/PRs" against the repo and GitHub on 2026-11-13.

| # | Claim in #423 | Verdict | Evidence |
|---|---|---|---|
| C1 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` exists; its Orca section describes coordinator/worker separation | TRUE | File exists. Section 7.7 "Orca Orchestration: Commands as Workers" at line 972; its "How the pieces fit" says a coordinator is a session someone opened by hand and a worker runs one `/sc:` command |
| C2 | `src/superclaude/core/WORKER-CONTRACT.md` holds "coordinator, worker-report and cross-session follow-up rules" | TRUE, incomplete | Exists. Follow-ups are WC-12 (`:61`, pulled not pushed). Not named by #423 but decisive for v2: WC-13 (`:62`, a worker may not start workers or open sessions), WC-3 (a coordinator reply is not acceptance for a Ruling halt), WC-16 (`:286-288`, only on PR #539, not on master) |
| C3 | `src/superclaude/commands/pm.md` and `skills/sc-pm-protocol/SKILL.md` are the "memory/checkpoint protocol to review for integration or reuse" | TRUE, with a limit v2 must know | Both exist. Memory is `<project>/.superclaude/memory/`, "one store per worktree" (pm.md:23), self-gitignored with `*`; checkpoints are `checkpoint-<timestamp>.md` every 30 minutes (pm.md:46). It is per-worktree, so it is not a cross-workspace store. `/sc:pm` is on the never-as-worker list (WORKER-CONTRACT.md:23) |
| C4 | `src/superclaude/commands/spawn.md` is "task decomposition and delegation" | TRUE | Frontmatter: "Meta-system task orchestration with intelligent breakdown and delegation". On the never-as-worker list (WORKER-CONTRACT.md:23) |
| C5 | `~/.claude/skills/orchestration/SKILL.md` is an installed Orca discovery stub, external | TRUE | `~/.claude/skills/orchestration` is a symlink to `../../.agents/skills/orchestration` (confirmed with `ls -la`). #444's accuracy check row 1 says the same |
| C6 | "The scoped repository discovery did not locate a dedicated v1/v2 orchestrator command or skill implementation" | TRUE on master, STALE on PR #539 | On PR #539's branch there is now `superclaude sweep run` (`src/superclaude/cli/sweep/`), `commands/sweep.md`, `skills/sc-sweep-protocol/`, WC-16. None is listed in #423 |
| C7 | #331 is a "related intake service proposal that would notify a project's Orchestrator about tagged, human-approved backlog issues" | STALE and partly wrong | The comment says it is built (#447, #448, shipped disabled, rollout #450, #331 closed); the body was not updated. The built watcher "starts one ordinary top-level agent session through `orca agent launch` with the prompt `/sc:issue --claim <N>`" (`origin/master:docs/designs/issue-watcher.md:15`); `grep -i orchestrator\|coordinator src/superclaude/cli/issue_watch/*.py` returns nothing. It does not notify an Orchestrator |
| C8 | #409 is a "read-only human-observation dashboard ... distinct from v2's proactive knowledge sharing" | TRUE | Matches the new #409 body ("this observer shows the human what happened, v2 shares knowledge between agents", Alignment decision 8 and Related list) |
| C9 | #326 is "Git/GitHub communication ... not the catalogue itself" | UNVERIFIED | Not read; #409 lists #326 under "Searched earlier and not confirmed related" |
| C10 | #339 is a "v1 prerequisite covering session supervision, child reporting and session recovery/cleanup; v2 follows its completion" | CONTRADICTED by #339's own text | See F1. #339's comments call the trust layer and the orchestrator of orchestrators "version 2"; its remaining phases (close, resume, trust, orchestrator of orchestrators, management server) are not complete after PR #539 |
| C11 | Keep architecture "flexible for harnesses outside Claude Code, including one like Mastra" | UNVERIFIED | `grep -rli mastra docs src` returns nothing; Mastra is not referenced anywhere in the repo |

Components missing from #423's list that its own scope needs: `src/superclaude/cli/sweep/` and `docs/designs/orchestrator-mode.md` (the v1 data source), `src/superclaude/cli/issue_watch/` (intake), `src/superclaude/pm_agent/reflexion.py` with `docs/memory/solutions_learned.jsonl` (an existing "lessons learned" store: its header says primary storage `docs/memory/solutions_learned.jsonl`, secondary mindbase), and `docs/memory/reflect/`. All exist (`ls docs/memory` shows `solutions_learned.jsonl`, `patterns_learned.jsonl`, `reflect/`).

## Alignment findings

Verdicts: aligned | gap | contradiction | unknown.

### Results of the four proposals

| Proposal | Result |
|---|---|
| (a) v2's catalogue reuses the sweep's output, not a third scanner | HOLDS FOR CLASSIFICATION, FAILS AS STATED. The sweep is the right source for per-session class, proof and coverage. It cannot be the catalogue as it is: JSON v1 omits the fields v2 needs, covers one bound Run on one host, keeps no history, and is never shared (F2 to F6). Reuse the sweep's facts and vocabulary; add what v2 needs through one agreed schema change |
| (b) observer and v2 share one data source, different consumers | HOLDS, with one unresolved decision. #409 already states it (Alignment decision 8). The unresolved part is schema ownership: observer and v2 both need keys JSON v1 lacks (F13) |
| (c) one trust design covers listener (Coder#477), cross-session messages and orchestrator of orchestrators | PARTLY. One grant vocabulary (narrow, expiring, replay-proof, audited) can serve all three. One design cannot: the three have different threat models, and #339's own comment 2 says tokens do not stop poisoned content. v2's relay is a fourth consumer that needs the data-not-instruction rule, not grants (F8, F9) |
| (d) #423's related list and acceptance criteria should name #409, #450, Coder#477, #444, #534 | YES, with one correction: #409 is already named. The other four are missing, plus PR #539. Acceptance criteria currently say nothing about data source, scope, trust or the version gate (F12) |

### Findings table

| ID | Point | Verdict | Evidence | Proposed change |
|---|---|---|---|---|
| F1 | The label "v2" means two different things. #423 = catalogue, cross-agent reviews, proactive course correction. #339 comments = trust layer plus orchestrator of orchestrators. #423's gate "after v1 (#339) is complete" is therefore ambiguous: #339 is not complete after Phase 1, and its remaining phases are listed in the research as close, resume, trust, orchestrator of orchestrators, management-server relay | contradiction | #339 comment 1 (2026-11-05T13:43:07Z): "Version 2 should include an orchestrator of orchestrators"; comment 2 section 7 (13:45:07Z): "Build Steps 2 and 3 as part of version 2, before any orchestrator-of-orchestrators work". `RESEARCH-REPORT-orchestrator-mode.md` "Later phases" paragraph (about line 1324) records `[CONTRADICTION, sources disagree on phase grouping]`: summary says version 2 = signed grants plus orchestrator of orchestrators; the table lists Phases 2 to 6 (rows at about lines 1330-1333). #423 "Out of Scope": "v1 orchestrator work (#339)" | Rename #423's release to a name that cannot collide (for example "Orchestrator Knowledge Layer") or state both meanings; replace the gate with a concrete one (see Proposed edits) |
| F2 | Sweep JSON v1 cannot carry a catalogue. Row keys are `row_id`, `class`, `waiting_kind`, `rule`, `evidence`, `notes`, `policy`, `person_started`, `safe_to_close`. Missing: what the agent is doing (command, objective), branch, changed paths, issue or PR, last activity. The data model has some of them but does not emit them | gap | `report.py:642-661` (row keys), `:662-681` (worktree keys: no branch, no `changed_paths`); `models.py:121` (`ContractRecord.command`), `:157` (`SessionRow.last_activity`), `:200` (`WorktreeState.changed_paths`) exist but none is in `to_json`. Design 7.4 pins the key set with a golden test (`orchestrator-mode.md:599`). #409 Alignment decision 1 says the same for the observer | v2 AC: name the exact fields the catalogue needs and how they reach it. #339: decide additive v1 keys vs JSON v2 once, for observer and v2 together |
| F3 | Scope: sweep covers the coordinator's bound Run(s) on one host; v2 wants "all agents across all workspaces". `--include-remote` is the only forbidden token; the report always prints a `remote hosts: unknown` row and "lower bound: remote hosts not scanned" | gap | `probes.py:62` (`FORBIDDEN_TOKENS = {"--include-remote"}`), `:1276` (`SourceCoverage("remote hosts", "unknown", ...)`), `report.py:196`; design section 1 "Out of scope ... remote hosts"; `commands/sweep.md` description ("bound Orca Run"); Coder#477 is "the only planned channel" between workspaces and a monitor (#409 decision 5) and is not built | #423 must say whether "all workspaces" means one host's several Runs or several Coder workspaces; if the latter, depend on Coder#477 and the cross-host reads that v1 forbids |
| F4 | No durable catalogue storage and no history. The sweep never reads its own earlier reports; reports are local, git-ignored and "never posted". v2 needs a store that persists between refreshes and is readable by other orchestrators | gap | Design `:146` ("`collect` never reads `.dev/sweeps/`"); `.gitignore:255-256` ("dated, operator-local, never posted (WC-16). Never tracked."); WC-16 at `WORKER-CONTRACT.md:288` ("it is never posted"). PM memory is per worktree (`pm.md:23`) | v2 must name its store, owner and reader set. The v1 rule "never posted" and v2's "share between orchestrators" must be reconciled explicitly, not by drift |
| F5 | v2's relevance check ("agents with work in progress or unmerged PRs") needs GitHub reads. Phase 1 has none, and the Orca allowlist is closed (10 templates, 7 verbs) under owner sign-off | gap | Design `:35` ("Out of scope ... `gh` reads"); `:521-537` (`ALLOWED_ORCA`); `:555` (owner sign-off for INV-005 names exactly these verbs); `:66` (GQ-109). Same gap named in #409 decision 3 | v2 AC: say whether gh reads are a v2 collector or a new sweep template. If the latter, it needs a new owner note, as the design says for any allowlist change |
| F6 | v2 must know what each agent is "doing". The `working` class is inert in Phase 1 and the agent-wait rule cannot match on live data, so a sweep cannot say "working" | gap | #534 section 2 first bullet; design `:491` (Rule 5 inert; names UNVERIFIED); PR #539 body ("the 'working' rule is inert and the agent-wait rule is dark") | v2 prerequisite: the #534 live read-only capture (restores Rule 5 and Rule 4(a)). List #534 in #423 |
| F7 | v2 "child-session checkpoint reports" and "relay ... to affected agents" assume a channel that exists only for Orca workers. Person-started and watcher-launched sessions are ordinary sessions: they send no lifecycle messages and are "never messaged". A worker cannot message peers (WC-13). Coordinator follow-ups reach a worker only when it runs `check` (pull). A changed brief is a new Task, not a message | contradiction | WC-16 `:288` ("Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged"); `:62` (WC-13); `:61` (WC-12 pulled, not pushed); `:78` (a follow-up `send` is not used to carry a retry's new brief); #409 decision 9 ("A session the watcher launches is an ordinary session to the sweep"); #339 accuracy check row 1 | v2 AC: for each class of agent (Orca worker, watcher-launched session, person-started session), state how a checkpoint is obtained and how a course correction is delivered, using only WC-12 follow-ups for workers and "inform the person" for ordinary sessions, unless the owner rules otherwise |
| F8 | #423 has no trust or safety criterion, yet v2's core act (summarize one agent's work and relay it to another) is the "cross-session permission laundering" path described in #339 comment 2. Cheaper agents "searching sessions or diffing logs" read transcripts that may contain untrusted web or PR content, then their summary feeds other agents | gap | #339 comment 2 sections 3, 5 Step 1 and 2 (relay reports as data only; fixed message types; free text only in `detail`, never acted on); #339 comment 2 "Held message" incident; #423 body: no mention of trust | Add AC and out-of-scope (Proposed edits): relayed knowledge is data, never an instruction; fixed typed fields; summaries are marked LLM-derived |
| F9 | Proposal (c): "one trust design". The three consumers differ. Coder#477: network listener, authN/authZ of an external monitor, transport and audit. Cross-session messages: same-host, sender identity already verified, problem is content steering (comment 2 says encryption and signing do not solve it). Orchestrator of orchestrators: delegation that can only be narrowed. A shared grant vocabulary fits the first and third and the audit trail fits all; the content problem fits none of them | gap | #339 comment 2 section 3 ("Complete trust without risk is not reachable with cryptography alone") and Step 3; Coder#477 body ("Authentication and authorization restrict who can send requests ... audit trail"); #409 decision 6 ("Decide one design, not two"); #339 comment 3 (Q1 and Q2 go to `/tech-research`, macaroon vs Biscuit to a debate; neither has run: #339 accuracy-check row 20) | Do not promise one design in #423 or #409. Promise one grant vocabulary and one audit record format, decided after the #339 comment-3 research and debate. v2's relay uses the data-only rule (F8) |
| F10 | "Management server" in #339's body ("relay information on to the orchestrator management server") is unresolved: #409 lists Orca or the observer. v2's catalogue store is a third candidate, and the same store may be both | unknown | #339 body ("Part of the Orchestrator should be to relay information on to the orchestator amnagement server"); #339 accuracy-check row 12 ("Not known yet"); #409 decision 10; research Phase 6 (about line 1332, owner question GQ-66) | Add v2's store as a candidate in #339 and #409; ask the owner once (Questions) |
| F11 | #423 describes #331 as a proposal that "would notify a project's Orchestrator". The built watcher starts an ordinary session; no orchestrator is involved. Coder#477 describes the watcher as handing a command "to its project's orchestrator". The two descriptions of the same flow differ | contradiction | #423 Related list; `origin/master:docs/designs/issue-watcher.md:15`; grep of `issue_watch/*.py` empty; #450 body; Coder#477 Problem Statement. UNVERIFIED which description is intended | Fix the #331 line in #423. Ask the owner which flow Coder#477 targets (Questions) |
| F12 | Related list and acceptance criteria miss the items that bound v2 | gap | #423 Related list has #339, #409, #331, #326. Missing: #444 (names #423 as related, yet #423 does not name #444), #450, Coder#477, #534, PR #539, and possibly #431 (title only read: "Orchestrator waits on workers that went quiet because its alive check relies on weak signals"; relevance to catalogue freshness UNVERIFIED). #339's own text links only #409 (as inspiration) and none of #423, #444, #534, PR #539, Coder#477 (`grep` over the 5 comments and body) | Proposed edits below |
| F13 | Observer and v2 will both ask for schema additions. #409 wants the ten dimensions, PR and issue links, a step flow, a session-open link. v2 wants command or objective, branch, changed paths, lessons. Without one owner these become two diverging schema requests | gap | #409 decision 1; F2 | Decide once, in #339, who owns the sweep JSON contract and how consumers request keys |
| F14 | Determinism boundary is not stated in #423. The sweep and observer are deterministic and bounded with "no default LLM polling loop"; v2's relevance evaluation and "cheaper, faster agents summarizing" are LLM work. If LLM output flows into the same catalogue, the observer's rule "evidence is not admission; stale is not failed; overlap is not conflict" can be broken by v2 | gap | #409 body (AC "Keep collection deterministic and bounded, without a default LLM polling loop"; design rules "shared paths do not establish a conflict"); design `orchestrator-mode.md:515` (finished wording never says admitted) | v2 AC: LLM-derived entries are marked as inferred, are stored apart from sweep facts, and never change a sweep class. "Overlapping files" is reported as possible overlap, never as conflict |
| F15 | Harness-neutral architecture vs v1 collectors. Every v1 collector is Orca, ccsession and Claude Code transcript specific (Orca allowlist, tab map, `~/.claude/projects` transcripts). A harness-neutral catalogue must separate the fact schema from the collectors | gap | Design `:32` (ccsession tab map), `:449-468` (data model), `:521-537` (allowlist); no "Mastra" anywhere in repo | v2 AC: name the harness-neutral fact schema, and that the sweep is one collector implementation of it |
| F16 | Refresh cadence. #423 wants timer refreshes; WC-16 says the coordinator runs `/sc:sweep` on every wake or wait timeout at most every 5 minutes and "Phase 1 adds this duty, not a scheduler". A v2 timer would create a second scheduler beside WC-16, and PM checkpoints run on a third cadence (30 minutes, per worktree) | gap | `WORKER-CONTRACT.md:288`; `HOW-WE-WORK.md:406`; `pm.md:46` | v2 design must say whether the timer refresh is the WC-16 pass (preferred, no new scheduler) or a separate scheduler with its own owner decision |
| F17 | Who may read whose sessions. The sweep reads one operating-system user's transcripts, tab map and worktrees, and confines every path under the root, a scanned project-key folder or the tab-map folder; a path that escapes is not read. v2 across workspaces would read other workspaces' transcripts and worktrees, and may involve other users or hosts | gap | Design `:512` (path-escape rule); `probes.py:1347` (scanned project keys). How Coder workspaces map to users or hosts: UNVERIFIED | v2 AC and owner question: read permission model for cross-workspace data, and whether v2 reads transcripts at all or only a published summary |
| F18 | Duplicate-mechanism risk: collision and duplicate-work detection already exist in narrow form in v1 and in the #409 designs. v1: `worktrees[].shared_package_ids` (same plan package in several worktrees, `report.py:674`; `classify.py:433,459`). Intake: the watcher claims one issue per cycle through `/sc:issue --claim`. #409's gallery has "Collision Lens" (content UNVERIFIED, not read). v2's "multiple agents solving the same issue" and "overlapping files" reviews would be a third detector | gap | As cited | v2 brainstorm must start from these and say what each review adds. Put detection logic in one place |
| F19 | Boundary between observer and v2 | aligned | #423 Related (#409 "distinct from v2's proactive knowledge sharing and course corrections"); #409 Feature Summary and decision 8 ("this observer shows the human what happened, v2 shares knowledge between agents") | None. Keep. Add the one clarifying line in Proposed edits (what v2 may publish to the observer, if anything) |
| F20 | Sequencing statement "v2 starts after v1" | aligned in direction | #423 Proposed Solution and AC 14; #409 Plan items 1-5 and Related ("a separate later release") | Make the gate concrete (F1) |
| F21 | v1 leakage into v2 territory. Anything in PR #539 that belongs to v2? | aligned | Checked: design section 1 scope (one read-only command, one report); `/sc:sweep` "recommends nothing" (WC-16 `:288`); no catalogue, no relevance scoring, no cross-agent messaging, no lessons in `src/superclaude/cli/sweep/` (`ls` shows only classify, commands, models, probes, report). The Phase 2 input file (`PHASE2-preflight-input.md`) is a reading list for sub-orchestrator mode and holds no v2 item | None |
| F22 | What "Orchestrator" means. #423 says "each Orchestrator"; rules and contract say "coordinator" (person-opened, depth 1, D5); #444 evaluates a `/sc:orchestrator` command that does not exist; the technical reference asks whether to replace "orchestrator" with "coordinator" because "no orchestrator role is implemented" | unknown | Tech ref C9 (`origin/master:docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`, section 14.3.1); #444 accuracy-check rows 3, 5; #339 body (no `/sc:orchestrator`) | #423 should define "Orchestrator" as "coordinator session, WC-16 loop" for its own text, and name which role holds the catalogue (a coordinator per Run, or a new layer) |

## Proposed edits

All exact wording below is ready to paste. Nothing was posted.

### #423 (IronbellyOrg/IronClaude)

1. Feature Summary, add one sentence at the end:

   > In this issue "v2" means the knowledge layer described here. It is not the "version 2" of #339's comments (trust layer and orchestrator of orchestrators); those are tracked as later #339 phases.

2. Replace "This is a separate future release after the v1 orchestrator (#339) is complete." (Feature Summary, Proposed Solution, AC 14) with:

   > This starts only after #339 Phase 1 is merged (PR #539) and the #534 live capture that restores the `working` class is done. Which other #339 phases (close, resume, trust layer, orchestrator of orchestrators) must precede it is an owner decision, recorded here once made.

   (Owner decision needed: see Questions 1.)

3. Proposed Solution, add a subsection "Data source and boundaries":

   > The catalogue reads the facts that `superclaude sweep run` already produces (class, rule, evidence, coverage, per session and worktree; PR #539) and does not add a second scanner of Orca, git or transcripts. Any field the catalogue needs that JSON schema v1 lacks (command or objective, branch, changed paths, issue or PR, last activity; see #409 Alignment decision 1) is requested through the one schema decision in #339, not by a v2-only collector. The sweep covers one bound Run on one host; "all workspaces" therefore depends on the cross-workspace channel of IronbellyOrg/Coder#477 and on the cross-host reads that Phase 1 forbids. LLM-derived entries (relevance, summaries, lessons) are stored apart from sweep facts, are marked as inferred, and never change a sweep class. The observer (#409) shows the human what happened; this layer shares knowledge between agents; both read the same sweep facts.

4. Acceptance Criteria, add:

   > - [ ] The design names the exact catalogue fields, where each comes from in the sweep's JSON, and which fields need a schema change decided in #339.
   > - [ ] The design states the scope of "all agents across all workspaces": one Run, one host, or several Coder workspaces; for several workspaces it names the channel (IronbellyOrg/Coder#477) and the read permission model.
   > - [ ] The catalogue has a named store, an owner, and a reader set, and says how this differs from the v1 rule that sweep reports are local and never posted (WC-16).
   > - [ ] For each agent class (Orca worker, watcher-launched session, person-started session) the design states how a checkpoint is obtained and how a course correction is delivered, using only the existing coordinator follow-up rule (WC-12) for workers and a report to the person for ordinary sessions, or records the owner decision that changes this.
   > - [ ] Relayed knowledge is data, never an instruction: fixed typed fields, free text only in a detail field that is never acted on (#339 comment of 2026-11-05, Step 2), with the grant and audit format taken from the trust decision in #339/#409 item 6, or an explicit note that v2 ships before it and relays to the person only.
   > - [ ] The timer refresh is the WC-16 coordinator pass, or the design records the owner decision for a second scheduler.
   > - [ ] The design says what GitHub reads the relevance check needs (unmerged PRs) and where they are allowed, given that Phase 1 has none.
   > - [ ] The harness-neutral fact schema is named, with the sweep as one collector of it.
   > - [ ] The design lists what each review adds beyond `worktrees[].shared_package_ids`, the issue watcher's one-claim-per-issue rule and the #409 Collision Lens design.

5. Out of Scope, add:

   > - A second scanner of Orca, git or transcripts.
   > - Sending prompts or commands to person-started sessions (WC-16: they are never messaged).
   > - The trust layer, the orchestrator of orchestrators and the management-server relay (tracked in #339 and #409).
   > - Changing sweep classes or JSON v1 keys (decided in #339).

6. Components Affected, add (and mark WC-16 and the sweep as "on PR #539, not on master"):

   > - `src/superclaude/cli/sweep/`, `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, WC-16 in `src/superclaude/core/WORKER-CONTRACT.md`, `docs/designs/orchestrator-mode.md` (PR #539): the facts v2 is to read.
   > - `src/superclaude/cli/issue_watch/` (PRs #447, #448; rollout #450): intake; starts an ordinary session, notifies no orchestrator.
   > - `src/superclaude/pm_agent/reflexion.py`, `docs/memory/solutions_learned.jsonl`, `docs/memory/reflect/`: existing lessons-learned stores to reuse or deliberately not reuse.
   > - Correction to the PM line: `.superclaude/memory/` is per worktree and self-ignored, so it is not a cross-workspace store.

7. Related Issues/PRs: replace the #331 bullet and add the missing ones:

   > - #331: issue watcher, built (PRs #447, #448; rollout #450). It starts an ordinary `/sc:issue --claim <N>` session through `orca agent launch`; it does not notify an orchestrator.
   > - #450: watcher rollout (live test, shadow run, cron).
   > - #444: sub-orchestrator mode evaluation (Phase 2 input); decides who holds a catalogue when a coordinator sits under another.
   > - #534: Phase 1 follow-ups; the `working` class and agent-wait rule (item 2) gate what a catalogue can say.
   > - PR #539: Phase 1 of #339 (read-only sweep); the data source.
   > - IronbellyOrg/Coder#477: workspace listener and monitor registration; the only planned cross-workspace channel.

### #339

1. Add a "Related" section to the body (the body links only #409, as inspiration):

   > Related: #409 (read-only TUI observer), #423 (Orchestrator knowledge layer, a later release), #444 (sub-orchestrator evaluation), #450 (issue watcher rollout), #534 (Phase 1 follow-ups), PR #539 (Phase 1), IronbellyOrg/Coder#477 (workspace listener and monitor registration).

2. Add a line to the body or a pinned comment fixing the vocabulary:

   > Terminology: the comments of 2026-11-05 use "version 2" for the trust layer and the orchestrator of orchestrators. These are Phases 4 and 5 of the research report's later-phase list. "Orchestrator v2" in #423 is a different release (catalogue and cross-agent reviews).

3. Under "Part of the Orchestrator should be to relay information on to the orchestrator management server", add: "Candidates: Orca itself, the #409 observer, the #423 catalogue store. Not decided."

4. Add one comment recording the JSON contract decision needed (additive v1 keys or schema v2) and that both #409 and #423 request keys.

### #409

1. Alignment decision 6 ("One trust design"): change "Decide one design, not two." to "Decide one grant vocabulary and one audit record. The enforcement points differ (listener, cross-session messages, delegation), and signing does not stop poisoned content, so the data-not-instruction rule is separate (#339 comment of 2026-11-05)."
2. Alignment decision 8: append "v2 also needs keys JSON v1 lacks (command or objective, branch, changed paths); decide the schema once with decision 1. v2 must keep LLM-derived content apart from sweep facts."
3. Alignment decision 10 ("management server"): add the v2 catalogue store (#423) as a third candidate.
4. Related list: no change needed for #423, #444 and #534 (all already named). Add one sentence so both issues use the same wording for v2: "In #423, v2 means the knowledge layer; it is not the 'version 2' of #339's comments."

## Questions only the owner can answer

1. What exactly gates #423: Phase 1 merged only, or also close, resume, the trust layer and the orchestrator of orchestrators? And is "version 2" in #339's comments renamed?
2. Is "all agents across all workspaces" several Runs on one host, or several Coder workspaces? If several workspaces, does the catalogue travel through the Coder#477 registration, and is v2 allowed to read other workspaces' transcripts or only a published summary?
3. Where does the catalogue live, who may read it, and is it allowed to leave the "local, never posted" rule that WC-16 gives sweep reports?
4. May v2 deliver a course correction to any session other than an Orca worker through a WC-12 follow-up? (Today ordinary sessions are never messaged.)
5. Who owns the sweep's JSON contract (additive v1 keys or a schema v2), given that #409 and #423 both ask for new keys?
6. Does the "management server" in #339 mean the v2 catalogue store, Orca, or the observer?
7. Should GitHub reads (unmerged PRs) be a new sweep allowlist template (a new owner note) or a v2-only collector?
8. Is one trust design still the goal, or one grant vocabulary plus separate enforcement (the position in this report)?
9. Which flow does Coder#477 target: the built watcher (starts an ordinary session) or a handoff "to its project's orchestrator"? The two issues describe different flows.

## Verdict

NOT YET ALIGNED, fixable by edits to #423 (and small edits to #339 and #409). 22 findings: 3 contradictions (the "v2" label and gate F1, messaging F7, the #331 description F11), 14 gaps, 2 unknowns (F10, F22), 3 aligned (F19, F20, F21).
- Observer/v2 boundary: aligned. Both issues say the same thing. The open item is one shared schema owner (F13).
- Proposal (a): reuse the sweep's facts, but it cannot be the catalogue as it stands (JSON v1 omits needed keys, one Run and one host, no history, never posted).
- Proposal (c): share a grant vocabulary and audit record; do not promise one trust design (different threat models, poisoned content is not solved by signing).
- v1 leakage into v2 territory: none found. What v2 assumes that v1 does not provide: cross-host data, durable store, relevance inputs (GitHub reads), a delivery channel to ordinary sessions, a read permission model.
