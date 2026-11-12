# Research Notes: Sub-orchestrator / coordinator mode for the proposed /sc:orchestrator

**Date:** 2026-11-08
**Scenario:** A (explicit request: question, why, where and output type all given)
**Depth Tier:** Deep (multi-subsystem: worker contract, decision history, hooks and guards, Orca mechanics, issue backlog; architectural decision)
**QA intensity:** full (tier default; no user override)
**Status:** Complete
**Task folder:** .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/
**Scope-discovery inputs (already on disk, read by the orchestrator):** research/scope/scope-01-contract-and-rules.md, scope-02-decision-history-d5.md, scope-03-enforcement-surface.md, scope-04-issues-prs-and-prior-analysis.md

**Research question (GOAL):** Should the proposed `/sc:orchestrator` support a sub-orchestrator or coordinator mode (possibly `--sub`): a session that delegates work to its own sessions inside a worktree while taking orders from, and reporting to, an orchestrator above? Decision needed: value, implications, unlocks, rethinks, options, risks, recommendation.
**WHY:** GitHub issue #444 asks for this evaluation before anyone builds it. Issues #339 (v1) and #423 (v2) of `/sc:orchestrator` depend on the answer. PR #449 named "a coordinator under another orchestrator" in the installed rules without defining it, on purpose (INF-027 deferred WC-13 to this issue).
**OUTPUT_TYPE:** a decision report (options, risks, recommendation). The user said: do not plan or start an implementation. See TEMPLATE_NOTES for how Section 8 is handled.
**TOPIC_SLUG:** sub-orchestrator-mode

---

## EXISTING_FILES

Tags follow the Documentation Staleness Protocol: [CODE-VERIFIED] = a scope researcher read the file and the text is there; [UNVERIFIED] = not read or needs a live Orca run; [CODE-CONTRADICTED] = doc differs from current source. Line numbers come from the scope files and must be re-read by Phase 2 agents before they are cited in the report.

### A. Worker contract and installed rules (scope-01)

| Path | Purpose | Key facts (line refs from scope-01) |
|---|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md` (328 lines) | The only written rules for coordinator and worker roles; installs to `~/.claude/WORKER-CONTRACT.md` | WC-13 at :62 bans worker-start, dispatch, task-create, low-level dispatch, `worktree create --agent`, `agent launch`, "at any depth setting". WC-8 at :40 binds commands. Line 5: "Commands themselves contain no Orca calls". Worker run defined at :11 as a session with an Orca preamble (Task ID + Dispatch ID); any other session is "ordinary". Coordinator defined at :69 as "an Orca coordinator session the person opened". Word "orchestrator" appears nowhere. D5 revisit trigger evidence rule at :246. Authority rules: WC-9 :41-45, D4 commit grant :42/:233, outward actions :229-235, child worktrees :218-225, liveness :95-192. Never-as-worker list :23. |
| `src/superclaude/core/CLAUDE.md` lines 55-59 and repo-root `CLAUDE.md` :305-315 | PR #449 text: "The session that creates a worktree becomes its orchestrator, or a coordinator under another orchestrator, and owns its agent(s)" | Phrase is undefined in all four places it appears. Also `src/superclaude/skills/ccsession-tag/README.md:242` and the hook message at `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:354` (plugin mirror :354). |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` section 7.7 (:972-1013) | Developer summary of coordinator/worker | Two-tier flat model (:978). Silent on WC-12 to WC-15 and on any sub-role. :985 is stale ([CODE-CONTRADICTED]: says no command accepts `--unattended`; 31 do). |

### B. Decision history (scope-02)

| Path | Purpose | Key facts |
|---|---|---|
| `.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md` (94) plus `option-a.md` (19), `option-b.md` (22) | Nesting-depth decision | Option (a) keep depth 1 approved 2026-11-02. Option (b) "raise to exactly 2, scoped by `Sub-workers: allowed, max N`" rejected; its five stated costs at :48. Revisit trigger at :49 (composite brief type AND run-notes evidence of a material run-time split; before any raise AC-0.7 trace done AND depth-2 mailbox established). |
| `.dev/orca-command-refactor/decisions/APPROVED.md` (90) | Owner approvals D1-D5 | :12 D5 row ("coordinator is a person-opened session; WC-13; AC-0.7; AC-C6"). D2 person-only Rulings :9, D3 pr-submit never a worker :10, D4 :11, git ownership :13. |
| `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (468) | Applied spec | :405 D5 row, :386 non-goal 2, :81 WC-13, :98 run-notes duty, :276 AC-C6, :315 AC-0.7, :88 child-worktree placement. |
| `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md` (54) | Child worktrees | Worktree lineage under ONE coordinator; workers in children remain depth 1. Status line "not yet applied" is stale. |
| `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md` :18,:27 (and P0S `ac-0.7-depth-trace.md`) | Live evidence about depth checks | Orca checks depth on worker-start and dispatch; does NOT check `task-create`, `worktree create --agent`, `agent launch`. Only WC-13 plus transcript scans guard them. |
| `.dev/orca-command-refactor/review/issue-326-evaluation.md:80` (grep hit only) | "Orca's depth-1 limit only stops workers from starting workers" | [UNVERIFIED] not opened by any scope researcher. |

### C. Enforcement surface (scope-03)

| Path | Purpose | Key facts |
|---|---|---|
| `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` (357; byte-identical plugin mirror) | PreToolUse Bash gate: blocks `orca worktree create` without `--agent` | Reads only `tool_name` and `tool_input.command` (:345-347). Cannot tell any role from another. Ceilings declared at :39-61 (bash -c, eval, xargs, claude --bare, scripts). Registered in `src/superclaude/hooks/hooks.json:105-114` and `plugins/superclaude/hooks/hooks.json:80`. |
| `src/superclaude/hooks/scripts/launch-level-guard.sh` (747) and `launch-job-identity.sh` (566) | Governs only sessions that `/sc:issue --claim` launched, keyed by `session_id` | ESCAPE class (:455-478) blocks every state-changing `orca` verb in a governed session, so a sub-orchestrator cannot run in a claim-launched session unless the allowlist or launch-record kinds change. Design doc `docs/designs/sc-issue-launch-level-hook.md` lists "Orca preamble visible to hooks" as UNVERIFIED (:457). |
| `tests/skills/test_worker_contract.py` (3195) | Phrase-pins the contract | `RULE_PHRASES["WC-13"]` :155 pins only the title; WC-8 :123; coordinator liveness phrases :181-209; parametrized tests :907 and :1044; `NEVER_AS_WORKER` :382; "nested" in this file means nested commands, NOT nested workers. Grep was capped at 150 lines: re-grep before any change. |
| `tests/hooks/test_require_orca_worktree_agent.py` (:36-37 pins the #449 sentence), `tests/hooks/test_require_orca_worktree_agent_governed.py` (57), `tests/core/test_orca_session_launch_guidance.py` (:30,:32,:49), `tests/hooks/test_launch_level_guard.py` (:3047-3055 ESCAPE list, :3087-3091 read-only list) | Pins wording and guard lists | Changing "coordinator under another orchestrator" needs edits in 2 hook copies, 2 CLAUDE.md files, the README and 2 test files. |
| Orca app bundle (read-only): `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js`, `out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`; `orca skills get orchestration` (+ `references/worker-contract.md`, `references/coordinator-loop.md`); `~/.config/orca/profiles/*/orca-data.json` | Orca mechanics | `nestedWorkerMaxDepth` = 1, one profile-wide desktop setting, no CLI verb. Orca natively supports "helper workers" (`worker-start --from <handle> --spec ... --worktree current`) when the preamble has a SUB-DISPATCH section (depth below max); helpers report to the creating worker's own `check`. No sub-coordinator role exists in Orca's role table (Coordinator, Dispatched worker, Handoff owner, Compatibility operator, Ordinary terminal agent). |

### D. Issues, PRs and prior #444 work (scope-04)

| Item | Key facts |
|---|---|
| GitHub #444 (subject), #339 (v1 /sc:orchestrator), #423 (v2), #431 (coordinator liveness bug), #446 (edits WC-9 line of the contract), #409 (TUI dashboard, premise of several orchestrators; [UNVERIFIED] unread), PR #449, PR #434 (liveness rules), #422 merged | #339 comment 1 and 2 hold the only design sketch: orchestrator of orchestrators in "version 2", narrowing grant tokens (macaroon/Biscuit style), fixed message types, gated destructive actions; its own conclusion puts Steps 2-3 and a research spike before any build. #423 (titled v2) does NOT cover sub-orchestration. #431/#434 solve liveness only for one coordinator over depth-1 workers. INF-027 (`.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md:78`) deferred WC-13 on purpose to this issue. |
| `.dev/issues/444/issue-summary.md` (32), `analysis/analyze-orchestration.md` (71), `accuracy-check.md` (32) | Prior findings F1-F7 confirmed by scope-04, with corrections G1-G4 (contract changed 2026-11-08 via PR #434; #422 now merged; one line number moved; deferral was deliberate). Phase 2 agents must treat F1-F7 as starting hypotheses, not as evidence. |
| `docs/designs/sc-issue-claim-pipeline-flag.md`, `docs/designs/sc-issue-command.md` | Use "orchestrator" for the `/sc:issue` skill itself and "worker" for lookup subagents; no layered design. |
| `~/.claude/skills/orchestration/SKILL.md` (symlink to `~/.agents/skills/orchestration`) | Discovery stub only. |
| Not existing: any `/sc:orchestrator` command or skill file; any spec naming it in `docs/` | [CODE-VERIFIED] by two scope researchers. |

### E. Precedents for "a session that starts sessions" (not yet investigated, named by scope researchers)

`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (launches one governed agent per claim), `src/superclaude/cli/issue_watch/` (poller that launches agents; `launch.py`, `cycle.py`), `/sc:pr-submit` as an ordinary session per PR in a child worktree (D3), `/sc:pm`, `/sc:spawn`, `/sc:agent` (never-as-worker commands), the `superclaude sprint` and swarm CLIs (programmatic orchestration). Each is a candidate precedent or counter-example for a middle layer.

## PATTERNS_AND_CONVENTIONS

- **Rule-by-prose, phrase-pinned by tests.** The contract and #449 wording are enforced by text plus `RULE_PHRASES` pins, not by code. A role change is a multi-file prose edit (contract, two CLAUDE.md copies, README, hook and mirror, three or more tests, dev guide).
- **One-party authority.** Briefs, outward actions, commit grants, Rulings, child-worktree removal and merge-back are all written or decided by one coordinator, on the person's live instruction (WC-9, D2, D4, :229-235). Any middle layer must say which of these move down, in what quoted form, and which never do.
- **Quoted-grant precedent.** WC-9's local-commit grant quotes the person's words and covers one Task. It is the only existing pattern for delegated authority.
- **Preamble-defined roles.** Role comes from the Orca per-dispatch preamble (`:11`), not from env or hooks; no repo hook can see it. Session identity in hooks is `session_id` only (launch-level guard).
- **D1: no command detects Orca.** `--unattended` is the only command-side mode switch. A `--sub` flag would be a second, Orca-aware switch.
- **Fixed fences vs written rules.** Orca fences depth on `worker-start`/`dispatch` only. `worktree create --agent`, `agent launch` and (unverified) `task-create` are guarded only by WC-13 text and transcript scans.
- **Coordinator-only commands** live on the never-as-worker list (:23; test `NEVER_AS_WORKER`). A `/sc:orchestrator` command that calls Orca would join that list and still contradict line 5.
- **Conventions for the research itself:** tables over prose, file:line citations, no code reproduction, doc-sourced claims tagged, codebase over docs over web.

## SOLUTION_RESEARCH

Not a build. Candidate answers the report must evaluate against the evidence (names are working labels, not conclusions):

| Label | Shape | Mechanism | Where the evidence points so far |
|---|---|---|---|
| O1 Keep two tiers, no sub mode | Status quo; v1 `/sc:orchestrator` is a single-level coordinator | Nothing changes; fix #449 wording to match the contract | Cheapest; leaves #339's v2 sketch unanswered |
| O2 Peer coordinators opened by the person | Several person-opened coordinators, no hierarchy | Contract unchanged; `/sc:orchestrator` coordinates only its own worktree | Fits D5 and WC-69; no upward reporting needed |
| O3 Supervised sub-orchestrator (worker with helpers) | Sub-orchestrator is a dispatched worker that starts helpers | Raise depth to 2 (scoped brief `Sub-workers: allowed, max N`), relax WC-13 for that brief, Orca native helper path reports to the parent's `check` | This is D5 option (b); costs at D5/REC:48; revisit gate not met |
| O4 Handoff-owner sub-orchestrator | Sub-orchestrator started with `worktree create --agent` / `agent launch`, outside the contract | No depth raise (Orca does not fence these); needs a new upward channel and authority rule | Mechanically possible; no reporting channel; governed `/sc:issue --claim` sessions cannot do it |
| O5 In-session sub-orchestration | Sub-orchestrator is an Agent-tool subagent inside one session; no Orca nesting | No Orca change; Agent-tool fan-out is not depth-fenced | Dodges D5 and WC-13 but loses Orca records and liveness; WC-7 says commands run at top level |
| O6 Defer with explicit gates | Build v1 single-level; define gates (the D5 trigger, a defined role, an upward channel, a grant rule) that must be met before `--sub` | Documentation plus evidence collection (coordinator run notes) | Matches #339's own ordering |

External research targets (gap-driven, Phase 4): Claude Code cross-session message and permission-mode behaviour (#339 open questions 1 and 2, never researched); hierarchical or supervisor-tree orchestration patterns and their documented failure modes; capability-narrowing token designs (macaroons, Biscuit, CaMeL) as a feasibility check on #339's grant sketch; Orca's public documentation on nested worker depth and helper workers.

## RECOMMENDED_OUTPUTS

Task folder `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/`:

| Output | Path | Purpose |
|---|---|---|
| Research notes | `research/research-notes.md` | This file |
| Scope files (done) | `research/scope/scope-01..04-*.md` | Stage A.3 inputs |
| Codebase research files | `research/01-*.md` to `research/08-*.md` | Phase 2 (see SUGGESTED_PHASES) |
| Web research files | `research/web-01-*.md` to `research/web-04-*.md` | Phase 4 |
| Gaps log | `gaps-and-questions.md` | Compiled in Phase 3 |
| Synthesis files | `synthesis/synth-01..06-*.md` | Phase 5 |
| Final report | `RESEARCH-REPORT-sub-orchestrator-mode.md` | Phase 6 |
| QA files | `qa/*` | Per the skill's gate naming |
| BUILD-REQUEST and task file | `BUILD-REQUEST.md`, `TASK-RESEARCH-sub-orchestrator-mode-20261108-181115.md` | Stage A.7 |

## SUGGESTED_PHASES

Global constraints for every Phase 2 and Phase 4 agent: READ-ONLY. No edits to any source, doc, test, hook or config file outside the agent's own output file. No GitHub writes (read-only `gh` calls only, always `--repo IronbellyOrg/IronClaude`, never the upstream SuperClaude-Org repo). No Orca state changes: only `--help`, `skills get`, `list`, `show`, `read`-style commands and file reads; never `worker-start`, `dispatch`, `task-create`, `worktree create`, `agent launch`, `run-create` or any setting change. Phase 2 agents re-read every file:line they cite (scope-file line numbers are second-hand) and tag each doc-sourced claim [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED]. Scope researchers' prior findings F1-F7 and G1-G4 are hypotheses to confirm or refute.

### Phase 2: Deep investigation (8 parallel agents, one output file each)

| # | Type | Topic | Files and sources to investigate | Output file |
|---|---|---|---|---|
| 01 | Architecture Analyst | Authority and role model of the contract against a middle layer | `src/superclaude/core/WORKER-CONTRACT.md` (all), `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, `decisions/APPROVED.md`, `decisions/D5/*`; tests pins (Grep only) in `tests/skills/test_worker_contract.py`. Produce a matrix: every rule (WC-2 to WC-15 and every section-4 rule) x options O1-O6 = holds / breaks / undefined, with quotes and line numbers. State what a definition of "coordinator under another orchestrator" would have to say. | `research/01-contract-authority-model.md` |
| 02 | Code Tracer | Liveness and upward reporting for a two-level tree | `WORKER-CONTRACT.md:95-192` (S0-S11, L0-L5, C rules), `:99-106` (inbox, Delivery, quarantine), WC-10, WC-12, WC-14, WC-15, handoff files; GitHub #431 and PR #434 (read-only). Trace what each signal is, who consumes it, and what doubles, breaks or becomes ambiguous with a supervised-and-supervising middle session; list upward-channel candidates per option. | `research/02-liveness-and-reporting-stack.md` |
| 03 | Integration Mapper | Orca mechanics (read-only) | `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js`, the main chunk `out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` (grep snippets), `orca skills get orchestration` and its `--reference` files (`worker-contract.md`, `coordinator-loop.md`), `orca orchestration --help` family, `.dev/orca-command-refactor/inventory/orca-capabilities.md`, `~/.config/orca/profiles/*/orca-data.json`. Establish exactly which calls are depth-fenced, how the native helper-worker path routes mail, what parentage Orca records (`parentWorktreeId`, task parent), whether message types are extensible, what `agent launch` and `worktree create --agent` create (Run, Task, Dispatch or none), and which of D5's open Orca facts can be settled by reading. | `research/03-orca-mechanics.md` |
| 04 | Integration Mapper | Hooks, guards and role-identity signals | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `launch-level-guard.sh`, `launch-job-identity.sh`, both `hooks.json`, `src/superclaude/cli/install_hooks.py`, `docs/designs/sc-issue-launch-level-hook.md` (sections on U7, U28, ESCAPE), the hook tests. Establish what identity or role signals a hook can see today, what a role-aware guard would need, how governed `/sc:issue --claim` sessions would interact with a sub-orchestrator, and what a hook can and cannot enforce (declared ceilings). | `research/04-hooks-guards-identity.md` |
| 05 | Pattern Investigator | Precedents: sessions that start sessions | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, `src/superclaude/cli/issue_watch/` (`launch.py`, `cycle.py`), `/sc:pr-submit` ordinary-session-per-PR model (D3), `src/superclaude/commands/{pm,spawn,agent}.md`, sprint and swarm CLIs under `src/superclaude/cli/`. For each: how it launches, what it reports and to whom, what authority it holds, what limits its children, what could be reused or is a counter-example. | `research/05-precedents-session-launchers.md` |
| 06 | Doc Analyst | Decision history and the D5 revisit-trigger evidence | D1-D5 folders under `.dev/orca-command-refactor/decisions/`, `.dev/orca-command-refactor/review/issue-326-evaluation.md`, `.dev/orca-command-refactor/decisions/D5/debate/adversarial/refactor-plan.md`, `.dev/orca-command-refactor/decisions/D4/debate/adversarial/refactor-plan.md`, `.dev/orca-command-refactor/decisions/D3/debate/adversarial/refactor-plan.md`, `.dev/orca-command-refactor/decisions/D2/debate/adversarial/refactor-plan.md`, P1 and P2 phase reports and any coordinator run notes under `.dev/tasks/done/TASK-WF-*` (search for follow-up Tasks and recorded extra time). Decide whether D5's two-part trigger is met; list implications of D2, D3, D4 for a middle layer; cross-validate every doc claim against the shipped contract; list stale statements. | `research/06-decision-history-and-trigger-evidence.md` |
| 07 | Architecture Analyst | Blast radius per option (evidence only, no plan) | Grep the repo for every file that pins, mentions or mirrors: "coordinator under another orchestrator", WC-13, WC-8, "person opened", `NEVER_AS_WORKER`, the hook message; `src/` and `plugins/` mirrors, `.claude/` dev copies and `make sync-dev` / `verify-sync` ripple, `HOW-WE-WORK.md` copies, installed `~/.claude/` copies, dev guide, tests. For each of O1-O6 produce a table of files, tests and docs that would have to change and why. | `research/07-blast-radius-per-option.md` |
| 08 | Doc Analyst | What #339, #423, #431, #409 require and depend on | `gh issue view` (read-only, `--repo IronbellyOrg/IronClaude`) for #339 (all comments), #423, #431, #409, #326, #446; `.dev/issues/444/*`. Separate what v1 `/sc:orchestrator` needs regardless of `--sub` from what depends on a sub mode; list requirement-versus-contract conflicts; settle the "v2" naming collision; list hidden dependencies and ordering. | `research/08-orchestrator-issues-requirements.md` |

### Phase 3: Research completeness verification (full: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative, serialized fix, max 2 cycles)

Gaps compiled into `${TASK_DIR}gaps-and-questions.md`. Research files in Phase 3 scope: 8 (so 5 gate agents without partitioning; partition only if more than 6 files are present, then split in two).

### Phase 4: Web research (4 parallel agents, gap-driven; Tavily first)

| # | Topic | Gap it fills | Output file |
|---|---|---|---|
| web-01 | Claude Code cross-session messaging, "Held message" notice, permission-mode classes, hooks that can inspect or gate inbound messages (official Claude Code docs) | #339 open questions 1 and 2, never researched | `research/web-01-claude-code-cross-session-messaging.md` |
| web-02 | Hierarchical or supervisor multi-agent orchestration: documented benefits and failure modes (Anthropic multi-agent engineering write-ups, Erlang/OTP supervision trees, LangGraph hierarchical teams, AutoGen nested chats, CrewAI hierarchical process): cost, latency, error propagation, context loss versus flat designs | Evidence for "value" and "implications" beyond our own repo | `research/web-02-hierarchical-orchestration-patterns.md` |
| web-03 | Capability-narrowing grants: macaroons, Biscuit, CaMeL; offline verification; feasibility inside hook-based enforcement | #339 Step 3 sketch, open question 3 | `research/web-03-capability-narrowing-tokens.md` |
| web-04 | Orca public documentation and repository: nested worker depth rationale, helper workers, orchestration guide, any statement about sub-coordinators | D5 open Orca facts; roles in the version-matched guide | `research/web-04-orca-nested-depth-helpers.md` |

### Phase 5: Synthesis (6 parallel agents) and synthesis QA gate (full, serialized fix)

| Synth file | Report sections | Source research files |
|---|---|---|
| `synthesis/synth-01-problem-current-state.md` | 1 Problem Statement, 2 Current State Analysis | scope-01..04, research 01-08, gaps log |
| `synthesis/synth-02-target-gaps.md` | 3 Target State, 4 Gap Analysis | research 01-08, web-01..04, gaps log |
| `synthesis/synth-03-external-findings.md` | 5 External Research Findings | web-01..04 |
| `synthesis/synth-04-options-recommendation.md` | 6 Options Analysis (O1-O6), 7 Recommendation (with explicit gates) | all research and web files, gaps log |
| `synthesis/synth-05-change-surface.md` | 8 (see TEMPLATE_NOTES: decision-only, change surface per option) | research 07, 01, 04, 03 |
| `synthesis/synth-06-questions-evidence.md` | 9 Open Questions, 10 Evidence Trail | all gaps, all file paths |

### Phase 6: Assembly (single rf-assembler), lens QA (full), fidelity gate (2-4 agents), anti-omission gate (2-4 agents; mandatory), serialized fix, max 2 cycles each, HALT after max.

Report path: `RESEARCH-REPORT-sub-orchestrator-mode.md`.

## TEMPLATE_NOTES

- **Template 02** (discovery, parallel agents, multiple phases, review gates).
- **Section 8 handling (user instruction: "do not plan or start an implementation").** Section 8 of the Report Structure is an Implementation Plan. The report keeps all 10 sections, but Section 8 is marked N/A as an implementation plan with this rationale, and instead carries a "Change surface per option" table (files, tests, docs and installed copies each option would touch, from research 07). That table is evidence for the decision, not a plan: no phases, no step ordering, no effort schedule. The Phase 6 domain lens "implementation-plan-concreteness" is applied to that change-surface table (every row names real files); the other two domain lenses apply unchanged.
- The Recommendation (Section 7) must be a decision with explicit gates (what must be true before a `--sub` mode is built), because gates are the decision's actionable output.
- The report must separate: what the repo rules say today (code and contract), what Orca enforces, what is prose only, and what is UNVERIFIED and needs a live Orca run (a live run is out of scope: this investigation is read-only).
- Doc-sourced claims in Sections 2, 6, 7 and 8 need [CODE-VERIFIED] backing. Prior analysis F1-F7 is documentation, not evidence.
- C8 (docs may not close a defect) applies to the Gap Analysis: the contradiction between the installed #449 text and WC-13/line 69 is a rule conflict, not "future work"; record it with severity and a cited scope decision (INF-027 is that decision for deferral).

## AMBIGUITIES_FOR_USER

None. Intent is clear from the request and the codebase: a read-only decision report with options, risks and a recommendation, no implementation plan. (Interpretation applied and disclosed: Section 8 becomes a change-surface table, see TEMPLATE_NOTES.)
