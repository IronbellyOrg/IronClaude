# Research Notes: Observer, Sweep and Dashboard family (IronClaude)

**Date:** 2026-11-20
**Scenario:** A (explicit request: scope, paths, output location and purpose all given by team-lead)
**Depth Tier:** Standard (requested by team-lead; the scope is large, so the six investigation agents each take one deep slice; web research: none needed, all subjects are in-repo)
**Status:** Complete
**QA intensity:** standard
**Task dir:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/
**Final output (NOT under docs/):** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md

**Hard rules for EVERY agent (put in every brief):** read-only on all source code and design files; write only inside the task dir (research/, synthesis/, qa/, reviews/ and the files named in the brief) or the one final output file; `gh` only read-only and only with `--repo IronbellyOrg/IronClaude`; never touch SuperClaude-Org (no fetch/pull/push/PR/issue/comment/link flags); UV only for Python (never python -m, never pip); do not stage or commit. **Code snapshot (read-only export of origin/master 61ac2c2e6, same layout as repo root, omits `.dev/`):** `/home/coder/.cache/ic-snap-20261120/master`. Read ALL code from it (the checkout `/home/coder/workspaces/IronClaude` is stale for code). Design-package files (item d) are read from the checkout `/home/coder/workspaces/IronClaude` (docs branch `docs/409-orca-dashboard-designs`, commit 495eb96d1). Files that exist only on origin/master under `.dev/` (for example `.dev/issues/409/bmad/...`) are read with `git -C /home/coder/workspaces/IronClaude show origin/master:<path>` (read-only).

Four scope-discovery files (written by four parallel scope agents, each already evidence-cited, with UNVERIFIED marks) are the base for this plan and persist in `scope/`:
- scope/01-observe.md (113 lines)
- scope/02-sweep.md (162 lines)
- scope/03-agent-work-report.md (114 lines)
- scope/04-dashboard-design.md (163 lines)

---

## EXISTING_FILES

### (a) Observer: `src/superclaude/cli/observe/` (snapshot; 6,169 lines of Python+schema, 13 modules, 18 fixtures, 36 test files)
| Path | Lines | Purpose |
|---|---|---|
| commands.py | 524 | click group `observe` (no subcommands; flags only): `--once --width --ascii --fixture --run --snapshot --questions`; interactive loop; gates `QUESTION_GATE_PASSED=True` (67), `QUESTION_LINK_PASSED=True` (70) |
| adapter.py | 512 | the only Orca edge; 3 allowed argv shapes (`skills list --json` discovery, `orchestration worker-list --json --limit 100 [--run][--cursor]`, `orchestration check --all --types question --run <id> --json`); forbidden-token list; caps 10 s/call, 8 MiB |
| parse.py | 835 | strict-envelope / lenient-row parsing, merge, question parse, fixtures loader |
| collector.py | 361 | single-flight polling thread, interval 15 s, backoff to 60 s, 5 calls/cycle cap |
| questions.py | 142 | bounded (1,000) question retention; nothing ever "closed" |
| view.py / render.py / terminal.py / theme.py / keys.py / sanitize.py | 1300 / 1461 / 192 / 126 / 235 / 48 | pure view model, Rich renderables at 3 widths (160/116/80), colour roles, key reader, sanitizer |
| export.py + snapshot.schema.json | 274 + 158 | plain-text record + JSON snapshot v1 ("PROPOSED, not an Orca contract"); state dir `~/.local/state/superclaude/observe/`, 0600 atomic writes |
| main.py:590-592 | | registration |
| tests/observe/ | 36 files, ~13.6k lines | render 135 tests, view 61, parse 44, adapter 43, commands 36, collector 32 ... |
Docs: docs/user-guide/cli-groups.md:40-54 (flags), README.md:136, no CHANGELOG entry, docs/testing/v6.0.0/post-release-report.md notes "no technical doc for `superclaude observe`".

### (b) Sweep: `src/superclaude/cli/sweep/` + command + skill + contract (snapshot; 3,759 lines Python)
| Path | Lines | Purpose |
|---|---|---|
| sweep/commands.py | 288 | `superclaude sweep run [--run ...] [--window] [--root] [--output]`; only write = one report file |
| sweep/probes.py | 1477 | read side: allowlisted `orca-ide` calls (10 templates), 4 fixed git calls/worktree, disk reads (packages, contracts, transcript tails, ccsession tab map); budgets |
| sweep/classify.py | 1009 | pure classifier, 9 rules -> 8 classes; joins; safe-to-close; removable |
| sweep/report.py | 695 | Markdown report (12 sections) + JSON v1 |
| sweep/models.py | 278 | frozen dataclasses, class constants |
| commands/sweep.md (70), skills/sc-sweep-protocol/SKILL.md (66) | | `/sc:sweep` command and the skill that runs it once and prints counts + report path; the chat "exempt reply" rule |
| core/WORKER-CONTRACT.md | 339 | WC-16 "Coordinator loop" (287-289), "The sweep" (110, the coordinator's own liveness sweep), WC-10 stall proofs (46, 157), never-as-worker list (23) |
| core/HOW-WE-WORK.md | 361 | routing row 298 and coordinator bullet 359 |
| docs/designs/orchestrator-mode.md | 1058 | NOT a general orchestrator doc: it is the Phase 1 design of this sweep |
| tests/sweep/ (323 tests, 8 py + 21 fixtures, captured 2026-11-11 against Orca 1.4.245), tests/commands/test_sweep_command.py (28 drift guards) | | |

### (c) Living work report: `src/superclaude/skills/agent-work-report/` (PR 684, commit d7d645ddd, 28 files, +10,488)
SKILL.md 194; config.json 21; scripts: run.py 887, common.py 507, collect.py 317, clickup.py 642, sessions.py 444, orca_term.py 133, exclude.py 109, match.py 283, classify.py 147, compare.py 197, activity.py 279, render.py 626, check.py 350, page.py 387, prefs.py 64, waker.py 405; templates (item, needs-you, overview, summary, qa-report (unreferenced), report-template.html, report.js); tests/skills/test_agent_work_report.py 4005 lines / 142 tests; tests/skills/test_worker_contract.py +8; CHANGELOG +4. Related design (not in this skill): docs/designs/orchestrator.md (design only, "holds no implementation code"; PR C = this skill; PR B = package with `report-entry` verb), docs/designs/sc-closeout.md, sc-closeout-protocol settle.sh:1037-1042.

### (d) Orca dashboard / TUI design package (issue 409), read from the checkout
- `.dev/design/orca-observer-20261106/` (commit 495eb96d1: 440 files, +101,520): README, DESIGN-CONTRACT, PLAN, PREVIEWS, QA, concepts, data-dictionary, integration-gaps, sources.json, manifest.json, fixtures.py, canvas.py, render.py, layouts/{group_a,group_b,agent_focus}.py, tests/, 18 scenarios, 360 exports, 2 galleries, 2 PDFs. 20 designs (2 sets of 10).
- `.dev/issues/409/` (issue record, ZIP, bmad specs only on origin/master).
- `.dev/research/orca-dashboard-20261105/` (UNTRACKED, local-only: not on the docs branch, not on master): REPORT.md 264 L, MOCKUPS.txt, snapshot-brainstorm/merged-requirements.md 1134 L, interactive-brainstorm/adversarial/merged-visual-design.md 180 L, visual-v2/, dashboard-study.html.

---

## PATTERNS_AND_CONVENTIONS
- Read-only discipline, each with a mechanical guard: observer = argv allow-list + forbidden tokens + only `adapter.py` imports `subprocess` (test asserts); sweep = exact-template allowlist `check_orca_argv` (probes.py:226) and `check_git_args`, test_readonly.py; design package = "navigation only, no approve/dispatch/retry/merge even greyed" (DESIGN-CONTRACT.md:11); agent-work-report = reads only, but DOES write (ClickUp DM, Orca unread mark, Orca browser tab, git commit in the orchestrator repo).
- "Unknown is never zero / never all-clear" appears in all three read-only tools ("UNKNOWN" sentinel parse.py:43; "could not determine" class in sweep; design rules S1-S11 and R1-R11).
- Layering: observer adapter -> parse -> collector -> view (pure) -> render/export; sweep probes (impure) -> classify (pure) -> report (pure) -> commands._publish (only write).
- Untrusted text is sanitized by each tool separately (observe/sanitize.py, sweep/report.py `sanitize`, AWR activity.py quoted lines, design canvas.py `sanitize`): no shared module.
- Each tool has its own Orca binary choice: observer finds the real Orca CLI by `skills list --json` containing topic `orca-cli` (`install_user_setup._find_orca`); sweep uses `orca-ide` or `$ORCA_CLI_COMMAND` ("never bare orca"); agent-work-report calls bare `orca`.
- Status vocabulary differs: observer shows raw Orca fields (workerState, dispatchStatus, terminalState, liveness verdict, outcome); sweep has 8 classes by scripted rules; AWR has 6 model-judged statuses (working, progressed, waiting on you, stuck, stalled, done).

## FEATURE_ANALYSIS
Four subjects, two shipped read-only supervision tools, one shipped daily report skill (whose orchestrator writer is not built), one design package (built as a synthetic prototype, no live integration):

1. **Observer** (`superclaude observe`): LIVE. Full-screen Rich terminal viewer for a person, polling `orchestration worker-list` every 15 s (+ optional coordinator questions of ONE Run). Also `--once` text record and `snapshot.json` v1 (auto-written each cycle in live mode, overwritten, no history). R2 (questions) and R3 (question-to-worker link, Decision Desk) ship behind two Python constants both True; cited gate records `.dev/issues/409/...` are not in the snapshot (verify on origin/master). No in-repo consumer of the snapshot found; no agent/command calls the observer.
2. **Sweep** (`superclaude sweep run`, `/sc:sweep`, skill `sc-sweep-protocol`): LIVE, Phase 1. One-shot; reads Orca (worker-list, task-list, worker-show capped at 50, worktree ps), git (4 lock-free calls per worktree), contracts, transcript tails, ccsession tab map; writes exactly one `.dev/sweeps/<UTC>-sweep.md` (gitignored) and prints JSON v1. Consumers: the skill (counts + path), the coordinator via WC-16 (at most every 5 min, in the same pass as the coordinator's own liveness sweep, read before acting), a person. Phase 1 limits: stalled (proved) and fenced cannot fire (no producer of `worker_done_seen`/`fenced_evidence`); Safe to close and Removable never print yes; ready-Task creator not observable; remote hosts and Orca messages not read; `agentWait` non-null never captured.
3. **Living work report** (`agent-work-report`): BUILT as a daily, model-assisted report for one person (Clay): GitHub (2 orgs) + Projects + ClickUp + Orca terminals/transcripts -> `.dev/coordinator/runs/<id>/` artifacts + `report.html` served on 127.0.0.1:8765 and a ClickUp DM. The "living report" half (`orchestrated/` entry files, `exclude.py`, `run.py refresh`) reads/moves/prunes entry files, but NOTHING in the snapshot writes active entries (`superclaude orchestrator report-entry` and `/sc:orchestrator` are design-only). Triggers via Orca automations (live outside repo, UNVERIFIED), `waker.py`.
4. **Dashboard design package (#409)**: 20 synthetic designs, Python/Pillow prototype renderer, proposed fixture schema (not Orca API), QA verdict "FAIL for pre-correction snapshots" then corrections applied without a new independent verdict; no design chosen by the owner (provisional picks only). Relationship to the observer: the package is the observer's design/semantic source; the observer is a separate Python/Rich re-implementation sharing no code (stack decision 2026-11-08 supersedes the Bubble Tea preference); only 3 of 20 designs (Decision Desk, Signal Bridge, Attention Ledger) were cited as visual targets (sub-issue #606, PR #673). The same 406-file package reached origin/master through PR #503 although commit 495eb96d1/the docs branch is unmerged.

**Cross-cutting questions the reference must answer for the owner (the WHY):** (i) data sources of each, (ii) output formats and where written, (iii) what is live vs designed, (iv) who/what consumes each output, (v) overlaps in purpose (status classification; "waits on a person" defined 3 ways; terminal-to-transcript joins by 2 different keys; each has its own sanitizer and Orca wrapper), (vi) how WC-16 ties sweep to the coordinator and what Clay's orchestrator design (per-repo orchestrator woken by the issue watcher + living report) would meet.

**Known contradictions and stale items to record (with exact evidence by the agents):**
- [CODE-CONTRADICTED] docs/designs/orchestrator-mode.md:27 says `src/superclaude/cli/sweep/` does not exist yet; it exists (5 modules).
- Issue 409 body says both "no observer code exists" (live body lines 19, 36) and that the observer is on master (banner line 13); comment 2026-11-17 and sweep design say the package branch is unmerged while `git diff 495eb96d1 origin/master -- .dev/design` is empty (content merged via PR #503).
- Package README says Bubble Tea/Lip Gloss stack preferred; shipped observer is Python/Rich by owner decision 2 (2026-11-08, stack.md:3).
- Actions: research mockups proposed reply/ack/resolve; package bans all actions; sweep prints a "next inspection" line which the live issue body flags (alignment item 2).
- AWR SKILL.md:14 says state under `orchestrator_repo` of `issue-watch.json`, but no code in `cli/issue_watch/` reads or sets that key (UNVERIFIED who does).
- AWR `qa-report-template.md` unreferenced.
- C8 rule for this task: the sweep classes stalled (proved) and fenced are declared in the command/skill/WC-16 as part of `/sc:sweep` but cannot fire in Phase 1. The agents must look for the on-record cited scope decision (docs/designs/orchestrator-mode.md Phase 1 limits, SKILL.md "not observed in Phase 1") and quote it; if none is found, record it as DEFECT-CANDIDATE. The agents cannot create a remediation task folder (write boundary above); the reference records "remediation owner: none found; flagged for owner".

## RECOMMENDED_OUTPUTS
Research files (6 codebase agents; no web research), all in `${TASK_DIR}research/`:
- `01-observe-data-contract.md`, `02-observe-interaction-gates-docs.md`, `03-sweep-classifier-joins.md`, `04-sweep-readside-wc16.md`, `05-agent-work-report-living-report.md`, `06-dashboard-design-vs-observer-gaps.md`

Synthesis files (map to template sections), in `${TASK_DIR}synthesis/`:
- `synth-01-overview-architecture.md`: Sections 1, 2 (including the "family at a glance" comparison matrix: data sources x outputs x live/designed x consumers x overlaps; the relationship diagram with the coordinator and WC-16)
- `synth-02-directory-dataflow.md`: Sections 3, 4 (file trees of the four subjects; data-flow diagram per subject: Orca -> adapter ... -> screen/snapshot; Orca/git/disk -> probes -> classify -> report; GitHub/ClickUp/Orca -> pipeline -> report.html; fixture -> renderer -> exports)
- `synth-03-subsystem-observer.md`: Section 5.1 to 5.2 (observer data contract; observer interaction layer, exit codes, gates)
- `synth-04-subsystem-sweep.md`: Section 5.3 to 5.4 (classifier and joins; read side/safety/publish; WC-16 binding)
- `synth-05-subsystem-work-report-dashboard.md`: Section 5.5 to 5.6 (agent-work-report pipeline and living report; dashboard design package and its relationship to the observer)
- `synth-06-integration-config-perf.md`: Sections 6 (N/A with rationale unless a state model exists: observer session/view state, snapshot cycle state), 7 (N/A, no component inventory beyond subsystem tables), 8 (API and integration: Orca verb inventory per tool, bare `orca` vs `orca-ide`, file formats and schemas, who reads what), 9 (configuration: flags, env vars, config.json, paths), 10 (error handling), 11 (performance: caps, budgets, intervals)
- `synth-07-conventions-extension-debt.md`: Sections 12, 13 (extension guide: how to add a sweep class, a snapshot field, a probe/allowlist entry, an observer view; what a unifier would plug into), 14 (tech debt, contradictions, UNVERIFIED items, C8 candidates), 15, 16

Final: assembled by rf-assembler to the output path above.

## SUGGESTED_PHASES (per-agent detail for the builder; one checklist item per agent)

**Phase 2 research agents (all Code Tracer / Doc Analyst mix; all read-only; all given the hard rules and snapshot path above):**

| # | Output file | Type | Topic | Files |
|---|---|---|---|---|
| R1 | research/01-observe-data-contract.md | Code Tracer | What the observer reads from Orca and what it emits: argv templates, forbidden list, paging/backoff/STALE/merge rules, question retention, snapshot schema vs code (dropped fields), error-code table, `_find_orca` discovery, whether Orca `check --all --types question` is non-acknowledging (UNVERIFIED so far) | observe/adapter.py, parse.py, collector.py, questions.py, export.py, snapshot.schema.json, fixtures/golden-*.json; install_user_setup.py:247-270; tests/observe/test_adapter.py, test_parse.py, test_collector.py, test_snapshot_schema.py, test_golden_contract.py. Use scope/01-observe.md as a starting map; verify, do not copy. |
| R2 | research/02-observe-interaction-gates-docs.md | Code Tracer + Doc Analyst | How a person uses the observer and which release stage it is: full key map, 3 width layouts, Decision Desk, exit-code table, interactive vs `--once`, R2/R3 gate constants and where their gate records live (git show origin/master for `.dev/issues/409/...` records), doc gaps (cli-groups.md, README.md:136, no CHANGELOG entry, post-release-report.md), PRs #503/#514/#577/#592/#598/#673 (read-only `gh pr view --repo IronbellyOrg/IronClaude`) | commands.py, view.py, render.py, keys.py, terminal.py, theme.py, sanitize.py, tests/observe/test_commands.py, test_session.py, test_view.py, test_render.py, test_live_screen_pty.py; docs listed. |
| R3 | research/03-sweep-classifier-joins.md | Code Tracer | What each sweep row means: the 9 rules/8 classes with exact firing conditions, the person_started joins (path A/B, `_guard`), `_contract_for`, could-not-determine forcing, safe-to-close/removable, package states; which test/fixture proves each rule; any producer for `worker_done_seen`/`fenced_evidence` anywhere; C8 candidate analysis | sweep/classify.py, models.py, tests/sweep/test_classify.py, tests/sweep/fixtures/, docs/designs/orchestrator-mode.md sections 7.2, 12-14 |
| R4 | research/04-sweep-readside-wc16.md | Code Tracer + Doc Analyst | What the sweep touches in the world and who relies on it: Orca allowlist (10 templates, called vs pinned-not-called), git calls and filter holes, disk reads, budgets, failure-to-unscanned, publish atomicity and exit codes, JSON v1 schema and report sections; WC-16 text vs coordinator's own liveness sweep ("The sweep", heartbeats, `worktree ps --agent-wait`), WC-10, never-as-worker, HOW-WE-WORK rows, the pragmatic output-style exempt reply; open items in the design (section 17) still open; what consumes `.dev/sweeps` in code | sweep/probes.py, commands.py, report.py, tests/sweep/test_probes_allowlist.py, test_readonly.py, test_git_config_hole.py, test_cli_contract.py, WORKER-CONTRACT.md (20-30, 96-160, 287-289), HOW-WE-WORK.md:298,359, commands/sweep.md, SKILL.md, tests/commands/test_sweep_command.py, .gitignore:255-256 |
| R5 | research/05-agent-work-report-living-report.md | Code Tracer + Doc Analyst | The whole skill: 15-step pipeline, every run-folder artifact with fields, status judgement inputs (6 statuses), grouping/priority, run lock, delivery gate (sha256 chain), carry-forward invariants; the living report: entry-file JSON contract with who writes each field (today nobody), exclude.py, `run.py refresh` 7 stages, waker (find/start session, wake line, retries, DM), orca_term verbs, page.py server/tab; the orchestrator design (docs/designs/orchestrator.md, sc-closeout.md) relationship; built vs designed table; read-only `gh pr list --repo IronbellyOrg/IronClaude` for orchestrator PRs landing after 61ac2c2e6 | AWR scripts and SKILL.md, tests (142 test names), docs/designs/orchestrator.md (sections DQ12/DQ13, 5.4, 6.4, 8.1-8.2, O3/O4, U17/U38), docs/designs/sc-closeout.md, sc-closeout-protocol settle.sh:1037-1042 |
| R6 | research/06-dashboard-design-vs-observer-gaps.md | Doc Analyst + Code Tracer | The #409 design package and its status: inventory, proposed fixture schema, semantic rules S1-S11 / R1-R11 traced against the shipped observer (enforced at which line, or not enforced); which of the 20 designs the observer implements; fixture-name parity (diff package scenarios vs observe/fixtures); contradictions C1-C5 settled against the live issue 409 body (`gh issue view 409 --repo IronbellyOrg/IronClaude`) and the PR file lists; integration-gaps items 1-6 closed/partly/open now, which Orca fields are real vs assumed; whether any shipped component reads GitHub/ClickUp (the design reads neither); the unbuilt direction "observer reads the sweep JSON" | package files under /home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/, .dev/issues/409/, `git show origin/master:.dev/issues/409/bmad/spec-orca-observer/{SPEC,rendering-rules,release-gates,unverified-register}.md` and `.dev/issues/409/visual-parity/REDESIGN-SPEC.md`, snapshot observe/ files, `.dev/research/orca-dashboard-20261105/` (local-only) |

**Web research:** none planned (all subjects are internal; Orca CLI docs are not needed to describe what these tools call). If Phase 3 finds a gap that needs Orca documentation, add one web agent.

**Synthesis mapping:** see RECOMMENDED_OUTPUTS.

## TEMPLATE_NOTES
- Template: `/home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md` (27,858 B; identical copy under ~/.claude/templates/documents/).
- Tier: Standard (team-lead request). Target length 800-1,200 lines by the skill's table; this reference covers four subjects, so the assembler may run to the upper end; the cross-subject comparison matrix (Section 2) and the contradictions list (Section 14) are the decision-relevant parts and must not be cut. Keep subsystem sections within the 40-200 line budgets.
- Sections 6 (State Management) and 7 (Component Inventory): mostly N/A for this family; mark with rationale. Observer session/view state may be summarised in 5.2 or 6 if the agents find a clear state model.
- Section 8 must contain an Orca verb inventory across the tools (bare `orca` vs `orca-ide` vs discovered binary) and the schemas/formats each writes (snapshot v1 JSON, sweep report Markdown + JSON v1, run-folder JSON + report.html, design exports).
- Section 13 (Extension Guide) must be concrete (file paths, registration points): add a sweep class/probe, add a snapshot field (schema additive-only), add an observer panel, add an AWR source; plus a short "unification touch points" list stated as facts (not recommendations: the owner decides in a later brainstorm).
- Section 14 must carry: every `[CODE-CONTRADICTED]` / `[STALE DOC]` item above, every UNVERIFIED item, and the C8 DEFECT-CANDIDATE analysis (stalled (proved) and fenced).
- Document Provenance appendix: not a consolidation; provenance = scope files and research files list.
- Evidence rule: cite `file:line` of the snapshot (prefix the path with `snapshot:` or write paths relative to repo root and state once that they are from origin/master 61ac2c2e6), and cite design files with their checkout path. Mark `.dev/research/orca-dashboard-20261105/` as local-only (untracked).
- Domain/consumer note: the reader is the owner, who will decide how Clay's orchestrator design is unified with these tools in a later brainstorm: state facts and overlaps; do not recommend.

## AMBIGUITIES_FOR_USER
None. Intent is clear from the request (exact paths, output file, tier, constraints). Two items are flagged for the final document, not for the user now: (1) the C8 remediation-task rule conflicts with the "write nothing outside the task folder and output file" rule, so the reference records defect candidates and states that no remediation task was created; (2) several facts live outside the repo (Orca automations, `.dev/coordinator/` contents, `issue-watch.json` `orchestrator_repo`) and stay UNVERIFIED.
