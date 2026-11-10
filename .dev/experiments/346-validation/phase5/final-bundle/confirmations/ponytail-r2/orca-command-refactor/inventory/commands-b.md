# Inventory B: Orca-worker readiness of 22 SC commands

Task: task_8b3cfb525d84 (Inventory B). Scope: `src/superclaude/commands/{load,pm,post-release,pr-submit,recommend,reflect,release-split,research,review-translation,roadmap,save,spawn,spec-panel,swarm-wizard,task,tasklist,tdd,test,troubleshoot,validate-roadmap,validate-tests,workflow}.md` and every skill each activates.
Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. All paths are repo-relative. Planning only.

## Method
1. Read all 22 command files in full under `src/superclaude/commands/`.
2. Resolved each command's activated skill from its `## Activation` (or `## Skill Invocation`) line. Six commands name no skill (`load`, `research`, `save`, `spawn`, `spec-panel`, `test`); for them the command file is the whole protocol.
3. Read the activated `SKILL.md` files (in full for the short ones; the decision-relevant sections for the long ones: `sc-reflect-protocol`, `sc-tasklist-protocol`, `sc-validate-roadmap-protocol`, `sc-roadmap-protocol`, `sc-troubleshoot-protocol`, `sc-release-split-protocol`, `sc-post-release-protocol`, `tdd`, `sc-recommend`), plus the refs that decide fields (a)-(f): interaction gates, fan-out counts, output contracts, resume and outward actions. Located them with `Grep` over `src/superclaude/skills/<skill>/**` for prompt, fan-out, contract, resume and git/gh patterns, then read the hit lines.
4. Cited `path:line` only for lines read in this run. Where a fact could not be confirmed from a file, it is marked UNVERIFIED.
5. Orca facts used for the verdict come from two sources: `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39` (a supervised Claude worker that sits at an unanswered question fails Orca's 60-second readiness limit) and this run's Orca dispatch preamble (a local `AskUserQuestion` prompt is invisible to the coordinator; questions must go through `orca orchestration ask`; results go through `worker_done --report-path`). Task 3 (`inventory/orca-capabilities.md`) owns the full Orca facts; nothing here re-derives them.

## Field legend
| Field | Meaning | What counts as evidence |
|---|---|---|
| (a) Waits on a person | The run stops until a human answers: `AskUserQuestion`, a `[yes / no]` or `y/n` offer, a "STOP AND WAIT" gate, an `--interactive` checkpoint, or a "confidence < 0.70, ask the user" rule | The line that names the prompt or gate, and whether it is default-on or behind a flag |
| (b) Needs a top-level session | The file says it must run in the main session, or it relies on something a nested Agent-tool subagent may not have (spawning its own agents, `Monitor`, an attended poll loop) | An explicit statement, else the dependency line. A generic "Agent-tool subagents cannot spawn agents" claim is not stated in any file read here and is marked UNVERIFIED wherever it is the only reason |
| (c) Fan-out | Uses the `Task`/Agent tool or another sub-process to run more agents, and how many | Count or range as written; "transitive" when it comes only through a nested skill |
| (d) Report / contract file | A single durable file whose path could be passed as `worker_done --report-path` | Path pattern as written; "machine contract" when it is a YAML return contract |
| (e) Resumes from disk | A documented way to continue from files left by an earlier run | Flag or rule that reads the earlier state |
| (f) Outward actions | Anything that leaves the working tree: git commit/push, PR, GitHub comments, installs, real-model network runs | The line that performs or forbids it |
| (g) Verdict | `ready-as-Orca-worker` (runs unattended, writes a report path, no person needed by default), `needs-change` (works as a worker only after a named change), `coordinator-only` (its job is orchestration or an attended loop that belongs in the coordinator or a human-facing session) | One line, with the change or the reason |

Note on (b): an Orca worker is itself a top-level Claude session in its own terminal (dispatch preamble), so "needs a top-level session" does not block running as an Orca worker. It only blocks running the command inside an Agent-tool subagent of a worker or coordinator.

## Inventory table
Short form; the full evidence for every cell is in the per-command note below. `cmd/` = `src/superclaude/commands/`, `sk/` = `src/superclaude/skills/`, `ag/` = `src/superclaude/agents/`. A bare `SKILL.md:N` or `refs/<file>:N` in a row means the skill named in that row's first column.

| Command (skill) | (a) Waits on a person | (b) Needs top-level | (c) Fan-out | (d) Report / contract file | (e) Resumes from disk | (f) Outward actions | (g) Verdict |
|---|---|---|---|---|---|---|---|
| `/sc:load` (none) | No (`cmd/load.md:25-38`) | No | None | None; context in chat (`cmd/load.md:52`) | Yes, it is the loader: `.superclaude/memory/` (`cmd/load.md:42-43`) | None | needs-change: writes no file; use as a brief step, not a task |
| `/sc:pm` (`sc-pm-protocol`) | Yes: reports to user, Socratic mode (`sk/sc-pm-protocol/SKILL.md:34-41`, `:60`) | Implied: "runs automatically at every session start" (`cmd/pm.md:12-17`) | Unbounded specialist delegation (`sk/sc-pm-protocol/SKILL.md:56-84`) | None single; memory + `docs/pdca/` (`:45-54`, `:143-148`) | Yes: memory keys (`:27-32`) | Edits CLAUDE.md (`:48`, `:158`) | coordinator-only: competing orchestrator |
| `/sc:post-release` (`sc-post-release-protocol`) | Conditional: pre-tag, output dir, VM/install/commit/PR confirm (`sk/sc-post-release-protocol/SKILL.md:71-75`, `:340`, `:351`) | No | 2-3 to 5-8 scanners per workstream + consolidator + writers (`refs/fan-out-pattern.md:9-13`) | `post-release-report.md` + manifest + `audit.log` (`SKILL.md:221-235`) | Additive mode from prior manifest, not interrupt resume (`SKILL.md:95-99`) | Real installs/VM, offers commit/PR (`SKILL.md:129-131`, `:324`) | needs-change: confirmations → pre-authorization inputs or `ask` |
| `/sc:pr-submit` (`sc-pr-submit-protocol`) | At `--monitor 1`: "fix these? y/n" (`sk/sc-pr-submit-protocol/SKILL.md:194`) | Yes, explicit (`SKILL.md:37-39`, `:66-68`) | `evidence-validator`, troubleshoot per finding, 1 auggie fallback (`SKILL.md:193-197`) | `monitor-run-<PR>.jsonl` (`cmd/pr-submit.md:39`, `:55`; `SKILL.md:170`) | Yes: `--resume <jsonl>` (`SKILL.md:141`, `:246`) | PR, commit, push, replies, resolves, re-trigger comments (`SKILL.md:189`, `:196`) | needs-change: heartbeats in poll loop, y/n + HALTs via `ask`/`escalation`, summary file; never as subagent |
| `/sc:recommend` (`sc-recommend`) | Conditional: one clarifying question (`cmd/recommend.md:44`; `sk/sc-recommend/SKILL.md:160`) | Implied: skill owns Agent spawns (`SKILL.md:71`) | 1 classifier + 1 cold-path; `--eval` 1/4/9 (`SKILL.md:73`, `:320`, `:332`) | None; chat prompt (`SKILL.md:30-33`); cache under `.claude/cache/` (`:313`, `:336`) | Cache hints only (`SKILL.md:65-67`) | Web search; never runs the prompt (`cmd/recommend.md:130`) | needs-change: write envelope to a file, question via `ask` |
| `/sc:reflect` (`sc-reflect-protocol`) | Only with `--remediate`: "[yes / no]" (`sk/sc-reflect-protocol/refs/remediation-handoff.md:228`) | No | Tier 1: 2 + reuse-auditor; Tier 2: 2-3 reviewers + calibrators + adversarial + validator (`cmd/reflect.md:142-143`; `SKILL.md:460`) | `<output>/return-contract.yaml` + REPORT.md (`SKILL.md:659`; `cmd/reflect.md:101`) | `--promote-resume` for promotion only (`SKILL.md:1508`) | No git (`SKILL.md:1556`); default UC-2 folder move (`cmd/reflect.md:110`) | ready (no `--remediate`; `--no-promote` if coordinator owns moves) |
| `/sc:release-split` (`sc-release-split-protocol`) | With `--interactive` (`sk/sc-release-split-protocol/SKILL.md:182`, `:256`, `:368`); also a tasklist-shaped input "confirm with user" (`:88`) and `--r1-scope custom` "prompt user" (`:175`) | No | brainstorm + adversarial 2-10 agents (`SKILL.md:93`, `:161`, `:190-208`) | `release-split-report.md` (`SKILL.md:402`) | `--resume-from` (`SKILL.md:120`) | None (`SKILL.md:460`) | ready (no `--interactive`, spec-shaped input, default `--r1-scope`) |
| `/sc:research` (none; persona agent) | Strategy-dependent: intent/unified ask (`ag/deep-research-agent.md:46-56`) | No | None (batched searches, `cmd/research.md:74-78`) | `claudedocs/research_[topic]_[timestamp].md` (`cmd/research.md:103`) | None | Web search only (`cmd/research.md:95-99`) | needs-change (small): pin `--strategy planning` or `ask` |
| `/sc:review-translation` (`sc-review-translation-protocol`) | Yes, mandatory: Phase 1 STOP AND WAIT, Phase 7 menu (`sk/sc-review-translation-protocol/SKILL.md:44`, `:76`, `:174-183`) | No | 1 agent per language + research agent (`SKILL.md:114-120`, `:134`) | `reports/localization/*_review_*.md`, `PROJECT_SUMMARY_*.md` (`cmd/review-translation.md:106-111`) | No mechanism (`SKILL.md:217`) | Web search; applies fixes on choice (`SKILL.md:178`) | needs-change: Phase 1/7 gates via input or `ask` |
| `/sc:roadmap` (`sc-roadmap-protocol`) | Yes: resume "[Y/n]" (`sk/sc-roadmap-protocol/SKILL.md:435`); `--interactive` prompts (`:231`, `:243`) | No | Wave 4: 2 validators; adversarial 2-10 (`SKILL.md:307-309`, `:84`) | `roadmap.md`, `extraction.md`, `test-strategy.md` (`SKILL.md:46-50`) | Yes, two conflicting mechanisms (`cmd/roadmap.md:29`; `SKILL.md:433-438`) | None | needs-change: reconcile flags, resume prompt → flag, add contract |
| `/sc:save` (none) | No | No | None | Memory files `.superclaude/memory/<key>.md` (`cmd/save.md:42`) | Writes the resume state (`cmd/save.md:27-31`) | None | needs-change: single-owner keys clobber in parallel (`cmd/save.md:44`) |
| `/sc:spawn` (none) | No | Not stated | Uncapped delegation; troubleshoot agents + debate (`cmd/spawn.md:28-36`, `:74-122`) | "Task breakdown document", no path (`cmd/spawn.md:203`) | None | None stated; contradicts own Edit/Write list (`cmd/spawn.md:30`, `:140`, `:192-201`) | coordinator-only: decomposition is the coordinator's job |
| `/sc:spec-panel` (none) | Conditional: asks for `target_release` (`cmd/spec-panel.md:35`) | No | None (simulated experts, `cmd/spec-panel.md:91`) | Review document, no path (`cmd/spec-panel.md:222`, `:455`) | None | None | needs-change: output path; `target_release` as input |
| `/sc:swarm-wizard` (`sc-swarm-wizard-protocol`) | Yes, by design: `AskUserQuestion` interview + go-ahead (`sk/sc-swarm-wizard-protocol/SKILL.md:84`, `:143`) | Implied: arms `Monitor` (`SKILL.md:148`) | Swarm 2-4 reviewers (`SKILL.md:106`) | swarm `return-contract.yaml` (`SKILL.md:159`, `:178`) | Offers swarm `--resume` (`SKILL.md:196`) | Real-model proxy runs (`SKILL.md:141-144`) | coordinator-only: human interview; workers call `superclaude swarm run` |
| `/sc:task` (`sc-task-protocol`) | Conditional: confidence < 0.70 prompt; TFEP "present to user" (`cmd/task.md:93`; `sk/sc-task-protocol/SKILL.md:225-226`) | No | STRICT: 1 quality-engineer; TFEP → troubleshoot (`SKILL.md:95`, `:216`) | Only on TFEP: `tfep-incident-report.md` (`SKILL.md:250`) | None | TFEP report "committed to git" (`SKILL.md:264`); EXEMPT commit/push (`cmd/task.md:80`) | needs-change: no prompt, no commit, fixed report |
| `/sc:tasklist` (`sc-tasklist-protocol`) | Indirect: Stage 10.5 passes `--remediate` to reflect (`sk/sc-tasklist-protocol/SKILL.md:1622-1631`) | Implied: reflect inside subagents (`SKILL.md:1618`); UNVERIFIED | 2N validators, Stage 9 `sc:task`, N reflects (`SKILL.md:1368`, `:1614`, `:1618`) | `tasklist-index.md`, `validation/ValidationReport.md` (`SKILL.md:92`, `:1452`) | None | None at generation (`SKILL.md:1162` runs later in Sprint) | needs-change: drop `--remediate` in 10.5; ready with `--no-reflect` |
| `/sc:tdd` (`tdd` → `task`) | Yes for a topic-only prompt: "do NOT proceed immediately. Ask the user to clarify" (`sk/tdd/SKILL.md:52-61`); otherwise rare (`:190`); `/task` asks on ambiguity (`sk/task/SKILL.md:49`, `:114`) | Expects to be top spawner (`sk/tdd/SKILL.md:238`) | 2-10+ code, 0-4 web agents + builder + QA (`cmd/tdd.md:57-61`; `sk/tdd/SKILL.md:353`, `:414`) | TDD file at `--output` (`sk/tdd/SKILL.md:48`) | Yes: `--resume <task-file>` (`cmd/tdd.md:29`; `sk/tdd/SKILL.md:22`) | None (`cmd/tdd.md:176`) | ready (precise component prompt + `--output`; rare questions via `ask`) |
| `/sc:test` (none) | No | No | None | None, no path (`cmd/test.md:52`) | None | Runs tests; `--fix` edits (`cmd/test.md:49`, `:89`) | needs-change: forbid `--watch`, add report path |
| `/sc:troubleshoot` (`sc-troubleshoot-protocol`) | Only with `--fix`: "[yes / no]" (`sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`); diagnosis "never AskUserQuestion" (`SKILL.md:209`) | No | Tier 1: 2; Tier 2: 2-4 + adversarial + validator (`cmd/troubleshoot.md:75-76`, `:171`) | `report_path` REPORT.md, `audit.log` (`SKILL.md:63-68`) | None | None: "No auto-commit" (`cmd/troubleshoot.md:203`) | ready (no `--fix`) |
| `/sc:validate-roadmap` (`sc-validate-roadmap-protocol`) | None found | No | Conflict: command `--agents` N (`cmd/validate-roadmap.md:98`) vs skill up to 20 (`SKILL.md:97`, `:491`) | Conflict: `validate/validation-report.md` (`cmd/validate-roadmap.md:62-69`) vs `02-consolidated-report.md` (`SKILL.md:1149`) | No; `--prior-taxonomy` seed (`SKILL.md:101`) | None | needs-change: command and skill interfaces disagree |
| `/sc:validate-tests` (`sc-validate-tests-protocol`) | No | No | None (`SKILL.md:4`) | `--report [path]`; skill lists no Write or Bash, command lists Bash but not Write (`cmd/validate-tests.md:6`, `:33`; `SKILL.md:4`) | None | None | needs-change: default target missing; report-writing path unclear |
| `/sc:workflow` (`sc-workflow-protocol`) | No (`sk/sc-workflow-protocol/SKILL.md:58`) | No | Transitive via reflect Wave 4 (`SKILL.md:58`; `cmd/reflect.md:142`) | `.dev/tasks/to-do/<id>/return-contract.yaml` (`refs/return-contract.md:3-19`) | None; never reuses a package (`SKILL.md:72`) | None at `--handoff none` (`SKILL.md:66`) | ready (with `--handoff none`) |

## Per-command evidence notes
Each note gives the evidence behind the table row. `cmd/` = `src/superclaude/commands/`, `sk/` = `src/superclaude/skills/`, `ag/` = `src/superclaude/agents/`.

### /sc:load
Skill: none (command file is the protocol).
- (a) None found. The file has no prompt or gate (`cmd/load.md:25-38`).
- (b) None stated. Uses only Glob/Read/Grep/Write (`cmd/load.md:47-52`).
- (c) None.
- (d) None. Output is session context in chat; Write is listed for "checkpoint creation" with no path (`cmd/load.md:52`).
- (e) Yes, this is the resume tool: reads `<project>/.superclaude/memory/<key>.md`, one store per worktree, with a read-only `.serena/memories/` fallback (`cmd/load.md:42-43`); `--type checkpoint --checkpoint <id>` restores a checkpoint (`cmd/load.md:82`), but `--checkpoint` is missing from the Usage line (`cmd/load.md:22`).
- (f) None.
- (g) needs-change: it only loads context into the current session and writes no file, so a worker has nothing to report. Better used as a step inside a worker brief than as a dispatched task; if dispatched, it needs a written context-summary file.

### /sc:pm
Skill: `sc:pm-protocol` (`cmd/pm.md:52`).
- (a) Yes, by design. Session start ends with "Report to User" and "User can immediately continue" (`sk/sc-pm-protocol/SKILL.md:34-41`); vague requests enter "Brainstorming Mode → Socratic questioning" (`sk/sc-pm-protocol/SKILL.md:60`, `cmd/pm.md:86-89`); "User Feedback: Incorporate throughout execution" (`sk/sc-pm-protocol/SKILL.md:192`). No `AskUserQuestion` call is named.
- (b) Not stated, but the command claims to be the "Always-Active Foundation Layer" that "runs automatically at every session start" and is the "Default entry point for all interactions" (`cmd/pm.md:12-17`), so it assumes it owns the session.
- (c) Yes, unbounded: delegates to requirements-analyst, system-architect, security-engineer, backend-architect, quality-engineer, technical-writer in sequence or parallel phases (`sk/sc-pm-protocol/SKILL.md:56-84`); no count cap.
- (d) None as a single report. Writes many files: `.superclaude/memory/*` (`sk/sc-pm-protocol/SKILL.md:45-54`), `docs/pdca/<feature>/{plan,do,check,act}.md` (`:143-148`), `docs/patterns/`, `docs/mistakes/` (`:48`, `:156-168`).
- (e) Yes: reads `pm_context`, `current_plan`, `last_session`, `next_actions` at start (`sk/sc-pm-protocol/SKILL.md:27-32`); 30-minute checkpoints (`:46`).
- (f) Edits shared instruction files: "update CLAUDE.md if global" and "Update CLAUDE.md with new best practices" (`sk/sc-pm-protocol/SKILL.md:48`, `:158`). No git/PR action named.
- (g) coordinator-only: it is a competing orchestrator (delegates to every specialist and claims every session), which is the role Orca's coordinator now holds; as a worker it would also overwrite single-owner memory keys and edit CLAUDE.md.

### /sc:post-release
Skill: `sc:post-release-protocol` (`cmd/post-release.md:63`). Refs read: `refs/fan-out-pattern.md`.
- (a) Yes, conditional gates: an untagged `<version>` must be confirmed before a pre-tag run (`sk/sc-post-release-protocol/SKILL.md:71-73`); an ambiguous output directory is confirmed (`:75`, `:225`); VM provisioning, installs against a real target, commit and PR are "confirmed first unless the user pre-authorized them this session" (`:340`, `:351`).
- (b) None stated.
- (c) Yes: per workstream (A-E) a read-only scanner team of "2-3 scanners" for a small surface up to "5-8" for a large one, spawned in one message, plus a consolidator and parallel writers (`sk/sc-post-release-protocol/refs/fan-out-pattern.md:9-13`, `:17`, `:26`); may also route writers through the project's task tooling (`sk/sc-post-release-protocol/SKILL.md:150-157`).
- (d) Yes: `post-release-report.md` and `post-release-manifest.json` in `--output` (default `docs/testing/<version>/`, `cmd/post-release.md:36`), plus `<output-dir>/audit.log`; the RESULT header carries `report_path` (`sk/sc-post-release-protocol/SKILL.md:221-235`, `:266-276`).
- (e) Partly: additive mode reads a prior release's `post-release-manifest.json` (`sk/sc-post-release-protocol/SKILL.md:95-99`). This is cross-release delta, not resuming an interrupted run; no resume flag exists.
- (f) Yes: runs the real install path (throwaway venv, container, `pipx install .`, VM per runbook) (`sk/sc-post-release-protocol/SKILL.md:129-131`, `:187`); offers commit/PR at the end (`:324`), with PRs only against `origin` (`:348`).
- (g) needs-change: the pre-tag, output-dir and outward-action confirmations must become explicit pre-authorization inputs in the worker brief (or go through `orca orchestration ask`); the report path is already suitable for `--report-path`.

### /sc:pr-submit
Skill: `sc:pr-submit-protocol` (`cmd/pr-submit.md:71`).
- (a) Yes at `--monitor 1`: "PROPOSE 'fix these? y/n' and apply NO edits" (`sk/sc-pr-submit-protocol/SKILL.md:194`; `refs/state-machine.md:44`, `:66`). Halts hand recovery to "the operator" (`SKILL.md:190`, `:196`, `:237-246`). Default `--monitor 3` has no y/n gate (`cmd/pr-submit.md:25`).
- (b) Yes, explicit: "Top-level activation required. This skill MUST run in the main orchestrating session ... Do NOT run it inside an Agent-tool subagent that itself spawns skills" (`sk/sc-pr-submit-protocol/SKILL.md:37-39`); every side effect stays in the main session, "Never hand a side effect to a background shell, detached loop, or subagent" (`:66-68`); "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`).
- (c) Yes: one read-only `evidence-validator` agent per wave-3 pass (`SKILL.md:193`); `Skill sc:troubleshoot-protocol` per verified finding (`:194`), which itself fans out 2-4 Tier 2 agents (see `/sc:troubleshoot`); at most one `/sc:auggie-review` fallback (`:197`).
- (d) Yes: the write-ahead run-log `monitor-run-<PR>.jsonl` under `--output-dir` (default `.dev/pr-monitor/pr-<N>-<ts>/`) is the authoritative record (output dir `cmd/pr-submit.md:55`; file name `cmd/pr-submit.md:39`, `SKILL.md:170`). It is JSONL, not a human summary; no summary report file is named. UNVERIFIED whether a markdown summary is written.
- (e) Yes: `--resume <run-log.jsonl>` rebuilds state, with crash-window recovery so there is "no double push, no re-fix" (`cmd/pr-submit.md:56`; `SKILL.md:141`, `:190`, `:246`).
- (f) Yes, all of them: `gh pr create --repo`, commits one fix commit per cycle, `git push origin <sha>:<branch>`, replies to and resolves review threads, posts `augment review` re-trigger comments (`SKILL.md:189`, `:196`); never force-push (`:227`).
- (g) needs-change: an Orca worker is a top-level session, so the top-level rule is met, but the attended poll loop waits up to `--timeout` 600 s per wait over several rounds (`cmd/pr-submit.md:49`) and must send Orca heartbeats; the L1 y/n and the operator HALT messages must go through `orca orchestration ask` / `escalation`; it must never be run as an Agent-tool subagent; `worker_done --report-path` needs a summary file (the JSONL log is the only artifact).

### /sc:recommend
Skill: `sc-recommend` (`cmd/recommend.md:56`).
- (a) Conditional: "If the objective stays ambiguous, it asks one question and stops" (`cmd/recommend.md:44`); "User request is too vague ... Ask one clarifying question" (`sk/sc-recommend/SKILL.md:160`).
- (b) Not stated. The skill "owns only the Agent spawns" because the CLI cannot spawn agents (`SKILL.md:71`), so it needs the Agent tool in its own session.
- (c) Yes: one Haiku classifier subagent (`SKILL.md:73`), one cold-path Haiku subagent on a cache miss (`SKILL.md:320`), and with `--eval` 1 / 4 / 9 parallel Agent calls for `quick` / `normal` / `deep` (`SKILL.md:330-334`).
- (d) None as a report: the output is a paste-ready prompt in chat (`SKILL.md:30-33`). Side files: cache rows via `uv run superclaude recommend cache put` (`SKILL.md:324`), eval outputs under `.claude/cache/eval-runs/iteration-<N>/...` (`SKILL.md:336-337`), plugin cache `.claude/cache/sc-recommend-plugin.yaml` (`SKILL.md:313`).
- (e) A lookup cache gives hints only, never state to resume (`SKILL.md:65-67`).
- (f) `--plugin` does web/marketplace search and prints install commands; it never runs the recommended prompt ("the user pastes it manually", `cmd/recommend.md:130`).
- (g) needs-change: its deliverable is chat-only text addressed to a person who pastes it; as a worker it must write the handoff envelope to a file for `--report-path` and send its one clarifying question through `orca orchestration ask`. It is more naturally a coordinator-side routing helper.

### /sc:reflect
Skill: `sc:reflect-protocol` (`cmd/reflect.md:149`). Refs read: `refs/remediation-handoff.md`, `refs/reviewer-spec.md` (grep hits).
- (a) Only with `--remediate`: after REPORT.md it asks "Proceed with <sc:workflow | task-builder>? [yes / no]" (`sk/sc-reflect-protocol/refs/remediation-handoff.md:228`; `cmd/reflect.md:205`, `:220`). Under headless `claude --print` it auto-accepts for auto-fixable registers and skips the gates (`remediation-handoff.md:239-247`). An Orca worker is an interactive terminal session, not `--print`, so the prompt would fire (derived from the dispatch preamble; not tested). Without `--remediate` there is no prompt (`cmd/reflect.md:288`).
- (b) None stated.
- (c) Yes: Tier 1 always runs `root-cause-analyst` + `confidence-calibrator` (`cmd/reflect.md:142`) and a `reuse-auditor` in UC-2 (`SKILL.md:460`); Tier 2 adds 2-3 heterogeneous reviewers, each calibrated, merged by `sc:adversarial-protocol`, then `evidence-validator` (`cmd/reflect.md:143`; `refs/reviewer-spec.md:94-96`).
- (d) Yes, machine contract plus report: `<output>/return-contract.yaml` "AND returned inline" (`SKILL.md:659`), with REPORT.md in the same dir; default output `.dev/reflect/<mode>-<slug>-<ts>/` (`cmd/reflect.md:101`).
- (e) Yes for promotion only: `--promote-resume <promotion-checkpoint.yaml>` finishes an interrupted cross-filesystem move (`cmd/reflect.md:114`; `SKILL.md:1508`, `:1514`). The audit itself is not resumable.
- (f) No git: "Reflect does NOT `git add` moved files" (`SKILL.md:1556`, `:1807`). Default-on Wave 7 in UC-2 moves the validated work-unit folder to its `done` destination (`cmd/reflect.md:110`, `:264`); UC-2 runs scoped non-mutating tests/linters (`cmd/reflect.md:106`); writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (`cmd/reflect.md:165`).
- (g) ready-as-Orca-worker without `--remediate`: the contract path is a direct `--report-path`; pass `--no-promote` when the coordinator should own folder moves.

### /sc:release-split
Skill: `sc:release-split-protocol` (`cmd/release-split.md:103`). Refs read: `refs/adversarial-integration.md` (grep hits); nested `sc-brainstorm-protocol/SKILL.md` (grep hits).
- (a) Mostly behind `--interactive` (default `false`, `cmd/release-split.md:55`): checkpoints after Part 1, Part 2 and on NOT VERIFIED (`sk/sc-release-split-protocol/SKILL.md:182`, `:256`, `:368`). Two prompts do not depend on it: a tasklist-shaped input is a WARN that says "confirm with user" (`SKILL.md:88`), and `--r1-scope custom` says "prompt user for Release 1 scope guidance" (`SKILL.md:175`). Without it, low convergence (0.5-0.59) aborts instead of asking (`SKILL.md:224`, `:436`). The nested `sc:brainstorm` waits for a reply only "if `--interactive`; otherwise auto-proceed" (`sk/sc-brainstorm-protocol/SKILL.md:134`).
- (b) None stated.
- (c) Yes: Part 1 `Skill sc:brainstorm` (`SKILL.md:149`, `:161`), Part 2 `Skill sc:adversarial-protocol` Mode B with 2-10 agents generating variants in parallel, default `opus:architect,sonnet:analyzer` (`SKILL.md:93`, `:190-208`).
- (d) Yes: `<output>/release-split-report.md` (`SKILL.md:402`) plus 4-6 named artifacts (`SKILL.md:39-55`); default `<spec-dir>/release-split/` (`cmd/release-split.md:53`).
- (e) Yes: `--resume-from <split-proposal-final.md>` skips Parts 1-2 (`SKILL.md:120`; `cmd/release-split.md:56`).
- (f) None: "Manage git operations or version control" is Will Not (`SKILL.md:460`; `cmd/release-split.md:124`).
- (g) ready-as-Orca-worker without `--interactive`, with a spec-shaped input and the default `--r1-scope`: `release-split-report.md` is the report path, and low convergence fails closed instead of prompting.

### /sc:research
Skill: none. Persona `deep-research-agent` in frontmatter (`cmd/research.md:7`); whether the frontmatter persona loads `ag/deep-research-agent.md` at run time is UNVERIFIED.
- (a) Strategy-dependent: `--strategy planning|intent|unified` (`cmd/research.md:25`). In the persona file, "Intent-Planning" generates "clarifying questions first" and "Unified Planning" says "Seek user confirmation" (`ag/deep-research-agent.md:46-56`); "Planning-Only" runs "without clarification" (`:40-44`). No default strategy is stated in the command.
- (b) None stated.
- (c) No Agent fan-out; "parallel-first searches" are batched tool calls (`cmd/research.md:53`, `:74-78`).
- (d) Yes: `claudedocs/research_[topic]_[timestamp].md` (`cmd/research.md:103`, `:134`). The exact name is generated at run time, so the worker must report the path it wrote.
- (e) None.
- (f) Web search/extraction via Tavily and Playwright (`cmd/research.md:95-99`); no git or install. "STOP AFTER RESEARCH REPORT" (`cmd/research.md:123-132`).
- (g) needs-change (small): pin `--strategy planning` in the worker brief, or route the intent/unified clarifying questions through `orca orchestration ask`; otherwise ready.

### /sc:review-translation
Skill: `sc:review-translation-protocol` (`cmd/review-translation.md:48`).
- (a) Yes, mandatory and default-on: "Phase 1 context analysis MUST receive user confirmation before any review work begins" (`cmd/review-translation.md:104`); "Output: Context Summary for User Confirmation → STOP AND WAIT for user" (`sk/sc-review-translation-protocol/SKILL.md:44`, `:76`). Phase 7 presents six options and waits for a choice (`SKILL.md:174-183`).
- (b) None stated.
- (c) Yes: one review agent per translation file (`SKILL.md:114-120`) plus a research sub-agent for evidence on Critical/High findings (`:134-147`).
- (d) Yes: `reports/localization/[lang]_review_*.md` and `reports/localization/PROJECT_SUMMARY_*.md` (`cmd/review-translation.md:106-111`). Names carry a run-time suffix.
- (e) Not really: "Partial completion: Document progress, save for resume" (`SKILL.md:217`), but no resume input or state file is defined.
- (f) Web evidence search (Tavily, `cmd/review-translation.md:6`); Phase 7 option 1 applies fixes to the translation files (`SKILL.md:178`). No git.
- (g) needs-change: the Phase 1 STOP-AND-WAIT gate and the Phase 7 menu block an unattended worker; they need a pre-confirmed context input or routing through `orca orchestration ask`, and the default Phase 7 choice for a worker should be "skip implementation".

### /sc:roadmap
Skill: `sc:roadmap-protocol` (`cmd/roadmap.md:85`).
- (a) Yes, default-on when an earlier session exists: "Prompt user: Found incomplete roadmap session (last completed: Wave X). Resume? [Y/n]" (`sk/sc-roadmap-protocol/SKILL.md:433-438`). With `--interactive` it also prompts on persona, template and low convergence (`SKILL.md:76`, `:209`, `:231`, `:243`).
- (b) None stated.
- (c) Yes: Wave 4 dispatches `quality-engineer` + `self-review` in parallel, with up to 2 REVISE loops (`SKILL.md:307-313`); `--specs` / `--multi-roadmap` / `--agents` call `sc:adversarial-protocol` with 2-10 agents (`SKILL.md:70-75`, `:84`). The CLI counterpart runs Claude subprocesses (`--max-turns` "per Claude subprocess", `cmd/roadmap.md:32`).
- (d) Partly: `roadmap.md`, `extraction.md`, `test-strategy.md` in the output dir (`SKILL.md:46-50`); no single report or return contract for the roadmap run itself. `roadmap.md` is the closest `--report-path`.
- (e) Yes, two mechanisms that disagree: the command's `--resume` skips steps whose outputs pass their gates and reads `.roadmap-state.json` (`cmd/roadmap.md:29`, `:40`); the skill resumes from `<output_dir>/.session-memory.md` after the [Y/n] prompt and has `--resume-from` for adversarial output (`SKILL.md:81`, `:420-438`).
- (f) None outward; writes memory through `sc:save` at every wave (`SKILL.md:316`, `:420`).
- (g) needs-change: the command and skill flag surfaces conflict (the command says `--specs`, `--template`, `--multi-roadmap`, `--interactive`, `--compliance`, `--persona` are unsupported, `cmd/roadmap.md:46-48`, `:98`, while the skill still defines them, `SKILL.md:69-82`); the resume [Y/n] prompt must become a flag; a single report or contract file is needed.

### /sc:save
Skill: none (command file is the protocol).
- (a) None found (`cmd/save.md:25-38`).
- (b) None stated.
- (c) None.
- (d) Yes, memory files: `<project>/.superclaude/memory/<key>.md` (`cmd/save.md:42`). No single report file.
- (e) It writes the state that `/sc:load` and `/sc:pm` resume from (`cmd/save.md:27-31`).
- (f) None outside the worktree; first write creates `<project>/.superclaude/.gitignore` with `*` (`cmd/save.md:43`).
- (g) needs-change: the store is one per worktree (`cmd/save.md:42`) and the single-owner keys `pm_context`, `last_session`, `next_actions` are "overwritten whole on each save" (`cmd/save.md:44`), so parallel workers in one worktree clobber each other. A worker must write only the per-session keys (`<key>-<session-or-timestamp>.md`, `cmd/save.md:45`) and report that file's path.

### /sc:spawn
Skill: none (command file is the protocol).
- (a) None found.
- (b) Not stated; it spawns "synchronous agents" (`cmd/spawn.md:47`).
- (c) Yes, uncapped: decomposes into Epic → Story → Task → Subtask and delegates (`cmd/spawn.md:28-36`); Rule 2.5 runs several parallel "troubleshoot agents" then an "adversarial-debate stage" (`cmd/spawn.md:74-122`). No count limit is stated.
- (d) A "Task breakdown document" (`cmd/spawn.md:203-208`) with no path.
- (e) None.
- (f) None by the CRITICAL BOUNDARIES block ("Execute implementation tasks directly", "Write or modify code" are Will NOT, `cmd/spawn.md:192-201`). This contradicts the flow step "Orchestrate: Execute tasks using optimal coordination strategy" and the Edit/Write/Bash tool list (`cmd/spawn.md:30`, `:140-141`).
- (g) coordinator-only: decomposing work and delegating it to other `/sc:*` commands is the Orca coordinator's job; as a worker it would also need an output path and a fix for the execute-vs-stop contradiction.

### /sc:spec-panel
Skill: none (command file is the protocol).
- (a) Conditional: for a TDD input with empty `target_release`, "ask the user to specify the target release before proceeding" (`cmd/spec-panel.md:35`). "Will Not: Modify specifications without explicit user consent" (`cmd/spec-panel.md:451`) gates the improved-spec step (`:34`).
- (b) None stated.
- (c) None: the 11 experts are simulated by "Native reasoning" (`cmd/spec-panel.md:91`, `:457`).
- (d) An "Expert review document" (`cmd/spec-panel.md:455-460`); Write is listed for "report creation" (`:222`) but no path or `--output` flag exists (`:22`).
- (e) None.
- (f) None.
- (g) needs-change: add an output path (or `--output`) so the worker can report it, and require `target_release` as an input instead of asking. This run's own Task 5 uses spec-panel as a worker, so the gap is live.

### /sc:swarm-wizard
Skill: `sc:swarm-wizard-protocol` (`cmd/swarm-wizard.md:68`). Ref read: `refs/interview.md` (grep hits).
- (a) Yes, by design: a Socratic interview with `AskUserQuestion` (`sk/sc-swarm-wizard-protocol/SKILL.md:7`, `:81-86`; `refs/interview.md:3`, `:12`, `:35`); STOP and ask on an ambiguous goal or missing target (`cmd/swarm-wizard.md:31-33`); an explicit go-ahead before any real run (`SKILL.md:143-144`). `--yes` reduces this to goal + target only (`SKILL.md:85-86`).
- (b) Not stated, but it arms the `Monitor` tool on `execution-log.jsonl` for its own run (`SKILL.md:7`, `:148-150`). UNVERIFIED whether `Monitor` is available inside an Agent-tool subagent.
- (c) The swarm CLI fans out 2-4 reviewers (`--reviewers` in [2,4], `SKILL.md:106`); the skill also lists `Task` (`:7`).
- (d) Yes: the swarm run's `return-contract.yaml` in `--output` (default `.dev/swarm-runs/<lens>-<ts>/`) (`cmd/swarm-wizard.md:51`; `SKILL.md:131`, `:159`, `:178`).
- (e) Offers swarm `--resume` (skips succeeded workers) after a partial run (`SKILL.md:196`).
- (f) Real-model network runs against the T2 proxy (`SKILL.md:59`, `:141-144`); no git.
- (g) coordinator-only: it exists to interview a non-expert and get a go-ahead; an Orca worker should run `uv run superclaude swarm run ...` with explicit flags instead, which needs no wizard.

### /sc:task
Skill: `sc:task-protocol` for STANDARD/STRICT only (`cmd/task.md:99-102`, `:159`).
- (a) Yes, conditional: confidence < 0.70 → "prompt user: Override with `--compliance [tier]`" (`cmd/task.md:93`) and "Will Not: Proceed with <70% confidence without user confirmation" (`cmd/task.md:183`; `sk/sc-task-protocol/SKILL.md:387`). TFEP: `test_is_wrong` or docs remediation → "Present to user for review" (`SKILL.md:225-226`); 3rd trigger → "**FULL STOP** (report to user, no further fixes)" (`:214`).
- (b) None stated.
- (c) STRICT spawns one `quality-engineer` verification agent (`SKILL.md:95`, `:312`); TFEP calls `/sc:troubleshoot` up to twice (`SKILL.md:216`, `:268-271`), which fans out 2-4 agents at Tier 2.
- (d) Partly: `tfep-incident-report.md` and `{output_dir}/context.yaml` only when TFEP fires (`SKILL.md:206`, `:250`); a session note `.superclaude/memory/task/session-<timestamp>.md` (`:317`). No report on the normal path.
- (e) None across sessions. TFEP "Resume" is in-session (`SKILL.md:242-246`).
- (f) Yes: the TFEP incident report "is committed to git alongside other diagnostic artifacts" (`SKILL.md:264`); EXEMPT keywords include `commit` and `push`, which run immediately with no skill (`cmd/task.md:80`, `:99`).
- (g) needs-change: the < 0.70 confidence prompt must default to the higher tier (or use `orca orchestration ask`), the TFEP "committed to git" step must be removed or made coordinator-owned, and a fixed report file is needed for every tier.

### /sc:tasklist
Skill: `sc:tasklist-protocol` (`cmd/tasklist.md:76`).
- (a) None in the generator. But Stage 10.5 runs `/sc:reflect --mode pre --remediate` per phase (`sk/sc-tasklist-protocol/SKILL.md:1614`, `:1622-1629`), and reflect with `--remediate` asks "Proceed with ...? [yes / no]" in an interactive run (`sk/sc-reflect-protocol/refs/remediation-handoff.md:228`, `:239-243`). Stage 10.5 says reflect "offers" remediation and `needs_human_decision` items HALT (`SKILL.md:1631`). Who answers that offer inside a subagent is not stated: UNVERIFIED.
- (b) Implied: Stage 10.5 dispatches N Agent-tool subagents that each run `/sc:reflect`, which itself spawns `root-cause-analyst` + `confidence-calibrator` (`SKILL.md:1618`; `cmd/reflect.md:142`). That is subagent→agent nesting, which `sk/tdd/SKILL.md:238` explicitly avoids. UNVERIFIED whether nested spawning works.
- (c) Yes: Stage 7 spawns 2N parallel validation agents for N phases (`SKILL.md:1347-1368`); Stage 9 patches via `sc:task --compliance strict` (`SKILL.md:1614`), which spawns a `quality-engineer`; Stage 10.5 spawns N parallel reflect agents (`SKILL.md:1618`, `:1775`).
- (d) Yes: `TASKLIST_ROOT/tasklist-index.md` and `TASKLIST_ROOT/validation/ValidationReport.md` (`SKILL.md:92`, `:99`, `:1452`); `TASKLIST_ROOT` defaults to `.dev/releases/current/<segment>/` (`cmd/tasklist.md:41-47`).
- (e) None for generation.
- (f) None directly; each phase file ends with a templated task that later runs `superclaude reflect run ... --fix` when Sprint executes it (`SKILL.md:1136`, `:1162`); generation itself does not run it.
- (g) needs-change: Stage 10.5 should call reflect without `--remediate` (or headless) so no yes/no offer can fire, and the per-phase reflect fan-out must run at the worker's top level, not inside subagents; with `--no-reflect` (`cmd/tasklist.md:39`) it is ready today, reporting `tasklist-index.md`.

### /sc:tdd
Skill: `tdd` (`cmd/tdd.md:151`). Nested: `task` skill (grep hits).
- (a) Default-on for a topic-only prompt: "If the user provides only a topic name or a vague request, do NOT proceed immediately. Ask the user to clarify", proceeding once "#1 answered clearly" (`sk/tdd/SKILL.md:52-61`). With a clear component it is rare: "Do NOT interrogate the user ... Only ask the user if there's a genuine ambiguity about intent" (`sk/tdd/SKILL.md:190`). The nested `/task` executor asks the user when several task files match (`sk/task/SKILL.md:49`) or an item looks wrong (`sk/task/SKILL.md:114`, `:592`); downstream offers are non-blocking (`sk/task/SKILL.md:97`).
- (b) Partly addressed: the reuse scout runs at orchestrator level "avoids subagent→agent nesting" (`sk/tdd/SKILL.md:238`), so the skill expects to be the top-level spawner.
- (c) Yes, heavy: 2-3 to 6-10+ codebase agents and 0-4 web agents by tier (`cmd/tdd.md:57-61`); an `rf-task-builder` subagent (`sk/tdd/SKILL.md:353`, `:386`), optional `rf-task-researcher` (`:244`), then `/task` runs parallel agents plus rf-analyst / rf-qa / rf-qa-qualitative gates (`:407-414`).
- (d) Yes: the final TDD at `--output` or `docs/[domain]/TDD_[COMPONENT-NAME].md` (`sk/tdd/SKILL.md:48`; `cmd/tdd.md:49`), with research under `.dev/tasks/to-do/TASK-TDD-<ts>/` (`sk/tdd/SKILL.md:86-92`).
- (e) Yes: `--resume <task-file>` continues from the first unchecked `- [ ]` item (`cmd/tdd.md:29`, `:48`; `sk/tdd/SKILL.md:22`, `:149`).
- (f) None ("Modify existing source code" is Will Not, `cmd/tdd.md:176`).
- (g) ready-as-Orca-worker only with a precise component prompt (required, because of `sk/tdd/SKILL.md:52-61`) and `--output` set: the TDD file is the report path and the task file gives resume; the rare intent question and `/task`'s "ask the user" lines should go through `orca orchestration ask`.

### /sc:test
Skill: none (command file is the protocol).
- (a) None found.
- (b) None stated.
- (c) None.
- (d) "Coverage reports and test summaries" via Write (`cmd/test.md:52`) with no path.
- (e) None.
- (f) Runs the project's test runner (`cmd/test.md:49`); Playwright browser tests for `--type e2e` (`:43`); `--fix` applies "automatic simple failure fixes" (`:90`).
- (g) needs-change: `--watch` is "continuous testing" (`cmd/test.md:22`, `:59`, `:89`) and never ends, so a worker brief must forbid it; a fixed report path is needed.

### /sc:troubleshoot
Skill: `sc:troubleshoot-protocol` (`cmd/troubleshoot.md:82`). Ref read: `refs/remediation-handoff.md` (grep hits).
- (a) Only with `--fix`: "Proceed with <sc:workflow | task-builder>? [yes / no]" (`sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`) and "refactor the task before running, or proceed as-is?" (`:198`; `SKILL.md:590`); Tier 3 needs "user explicitly accepts the remediation offer" (`SKILL.md:576`). Diagnosis itself never asks: "never AskUserQuestion" (`SKILL.md:209`, `:646`). STOP on `--depth deep` with < 10 words "ask the user to add detail first" (`SKILL.md:57`).
- (b) None stated.
- (c) Yes: Tier 1 `root-cause-analyst` + `confidence-calibrator`; Tier 2 2-4 specialist agents, capped at 4, plus `sc:adversarial-protocol`, `self-review`, `evidence-validator` (`cmd/troubleshoot.md:75-76`, `:171`, `:174-176`, `:186`); Wave 1.5 auggie documentation fan-out (`cmd/troubleshoot.md:88`).
- (d) Yes: `report_path` (REPORT.md) and `audit_log_path` in the output contract (`SKILL.md:63-68`), default `.dev/troubleshoot/<slug>-<timestamp>/` (`cmd/troubleshoot.md:56`); `return-contract.yaml` only when `--caller task-unified` (`SKILL.md:104`, `:175`, `:570`).
- (e) None.
- (f) Read-only probes and diagnostic commands under an execution gate (`cmd/troubleshoot.md:101`); `gh api` only as a doc-fetch fallback (`SKILL.md:397`); never applies code or commits ("No silent code changes. No auto-execution. No auto-commit.", `cmd/troubleshoot.md:203`).
- (g) ready-as-Orca-worker without `--fix`: diagnosis never prompts and REPORT.md is the report path; `--fix` needs its yes/no offer routed through `orca orchestration ask`.

### /sc:validate-roadmap
Skill: `sc-validate-roadmap-protocol` (`cmd/validate-roadmap.md:74`).
- (a) None found in the skill (grep for prompt patterns in `sk/sc-validate-roadmap-protocol/SKILL.md` returned no prompt).
- (b) None stated.
- (c) Command and skill disagree. Command: N agents from `--agents` (default 1), and "Will Not: Spawn additional sub-agents beyond the `--agents` list" (`cmd/validate-roadmap.md:31`, `:38-39`, `:98`). Skill: one `sonnet` agent per domain plus four mandatory cross-cutting agents, `--max-agents` default 20 (range 4-20), all in one parallel `Task` message (`SKILL.md:97`, `:308`, `:360`, `:374`, `:491`).
- (d) Command and skill disagree. Command: `<OUTPUT_DIR>/validate/validation-report.md` (`cmd/validate-roadmap.md:62-69`). Skill: `{roadmap-dir}/validation/` with return contract `report_path: {OUTPUT_DIR}/02-consolidated-report.md`, `summary_path: .../05-validation-summary.md` (`SKILL.md:94`, `:1137-1151`).
- (e) No resume; `--prior-taxonomy` seeds domain clustering from a prior run (`SKILL.md:101`); fail-open memory under `.superclaude/memory/validate-roadmap/` (`SKILL.md:135`, `:975`).
- (f) None.
- (g) needs-change: the command's interface (`<OUTPUT_DIR>`, `--agents`, `--model`, `--max-turns`) is passed "verbatim" (`cmd/validate-roadmap.md:76`) to a skill that requires `<roadmap-path> --specs` (`SKILL.md:85`, `:92-93`) and says it is "NOT a behavioural mirror" of the CLI (`SKILL.md:20`); the coordinator cannot know the report path or agent count until they agree. The CLI `superclaude roadmap validate` is the deterministic worker option today.

### /sc:validate-tests
Skill: `sc:validate-tests-protocol` (`cmd/validate-tests.md:112`).
- (a) None. `requires_confirmation` is a field being tested, not a prompt (`sk/sc-validate-tests-protocol/SKILL.md:102`, `:269`).
- (b) None stated.
- (c) None (skill tools: Read, Glob, Grep, TodoWrite, `SKILL.md:4`).
- (d) `--report [path]` "Save detailed report to file" (`cmd/validate-tests.md:33`; `SKILL.md:52`). The skill lists neither Write nor Bash (`SKILL.md:4`); the command lists Bash but not Write (`cmd/validate-tests.md:6`). UNVERIFIED which one saves the report.
- (e) None.
- (f) None.
- (g) needs-change: the default target `tests/sc-task/` (`cmd/validate-tests.md:22`) does not exist in this checkout (`ls tests/sc-task` → "No such file or directory", run 2026-11-02), and the skill that runs the protocol cannot write the `--report` file (no Write or Bash in `SKILL.md:4`); fix both before dispatching it.

### /sc:workflow
Skill: `sc:workflow-protocol` (`cmd/workflow.md:51`). Ref read: `refs/return-contract.md`.
- (a) None in the workflow skill. The nested Wave 4 reflect runs with "defaults for every other flag, no `--remediate`" (`sk/sc-workflow-protocol/SKILL.md:58`), so reflect's remediation offer does not fire.
- (b) None stated.
- (c) The skill says "Will Not: ... Task fan-out" (`SKILL.md:74`), but Wave 4 invokes `sc:reflect-protocol` via Skill (`SKILL.md:18`, `:58`), whose Tier 1 always spawns `root-cause-analyst` + `confidence-calibrator` and may escalate to 2-3 reviewers (`cmd/reflect.md:142-143`). Transitive fan-out.
- (d) Yes, machine contract: `.dev/tasks/to-do/<id>/return-contract.yaml` (contract 1.1) with `status`, `plan_path`, `reflect_report_path` (`sk/sc-workflow-protocol/refs/return-contract.md:3-19`); written on every post-creation outcome, including `failed` (`:41`). Not written for pre-creation STOPs (`:39`).
- (e) None: "Never overwrites or reuses an existing package" (`SKILL.md:72`).
- (f) None at `--handoff none`. `--handoff implement` invokes `sc:implement-protocol` (`SKILL.md:18`, `:66`), which changes code. `.dev/tasks/` "is always staged" (`SKILL.md:28`); UNVERIFIED whether the skill itself runs `git add`.
- (g) ready-as-Orca-worker with `--handoff none`: no prompts, one new package, and `return-contract.yaml` is a direct `--report-path`.

## Summary: needs-change and coordinator-only
Totals: 5 ready-as-Orca-worker, 14 needs-change, 3 coordinator-only (22 rows).

**Ready as an Orca worker (with the stated inputs):** `/sc:reflect` (no `--remediate`), `/sc:release-split` (no `--interactive`, spec-shaped input, default `--r1-scope`), `/sc:tdd` (precise component prompt, not a bare topic, plus `--output`), `/sc:troubleshoot` (no `--fix`), `/sc:workflow` (`--handoff none`). Under those inputs each runs with no person and writes a file whose path fits `worker_done --report-path`.

**Coordinator-only (3):**
| Command | Why |
|---|---|
| `/sc:pm` | A competing always-on orchestrator that delegates to every specialist and claims the session (`cmd/pm.md:12-17`; `sk/sc-pm-protocol/SKILL.md:56-84`); also edits CLAUDE.md and overwrites single-owner memory keys. |
| `/sc:spawn` | Task decomposition and delegation to other `/sc:*` commands is the coordinator's job (`cmd/spawn.md:192-210`); it also has no output path and contradicts itself on executing. |
| `/sc:swarm-wizard` | A human interview with `AskUserQuestion` and an explicit go-ahead (`sk/sc-swarm-wizard-protocol/SKILL.md:84`, `:143`); a worker should run `uv run superclaude swarm run` with explicit flags instead. |

**Needs-change (14), grouped by the change:**
| Change | Commands | Evidence |
|---|---|---|
| Route a default-on human gate through `orca orchestration ask` or turn it into an input/flag | `/sc:review-translation` (Phase 1 STOP AND WAIT, Phase 7 menu), `/sc:roadmap` (resume [Y/n]), `/sc:post-release` (pre-tag, output dir, outward confirmations), `/sc:pr-submit` (L1 y/n, operator HALTs), `/sc:task` (confidence < 0.70), `/sc:spec-panel` (`target_release`), `/sc:research` (intent/unified strategies), `/sc:recommend` (one clarifying question) | `sk/sc-review-translation-protocol/SKILL.md:76`, `:174`; `sk/sc-roadmap-protocol/SKILL.md:435`; `sk/sc-post-release-protocol/SKILL.md:71-75`, `:351`; `sk/sc-pr-submit-protocol/SKILL.md:194`; `cmd/task.md:93`; `cmd/spec-panel.md:35`; `ag/deep-research-agent.md:46-56`; `cmd/recommend.md:44` |
| Write a single report file the worker can name in `--report-path` | `/sc:load`, `/sc:spec-panel`, `/sc:test`, `/sc:recommend`, `/sc:task` (normal path), `/sc:pr-submit` (JSONL log only), `/sc:roadmap` (three artifacts, no contract) | `cmd/load.md:52`; `cmd/spec-panel.md:222`; `cmd/test.md:52`; `sk/sc-recommend/SKILL.md:30-33`; `sk/sc-task-protocol/SKILL.md:250`; `cmd/pr-submit.md:55`; `sk/sc-roadmap-protocol/SKILL.md:46-50` |
| Reconcile a command with its own skill (interface drift) | `/sc:roadmap` (flag surface), `/sc:validate-roadmap` (inputs, agent count, report path), `/sc:validate-tests` (missing default target, skill cannot write the `--report` file) | `cmd/roadmap.md:46-48` vs `sk/sc-roadmap-protocol/SKILL.md:69-82`; `cmd/validate-roadmap.md:21`, `:98` vs `sk/sc-validate-roadmap-protocol/SKILL.md:92-97`, `:1149`; `cmd/validate-tests.md:6`, `:22` |
| Remove a nested fan-out or remediation offer that runs inside subagents | `/sc:tasklist` (Stage 10.5 runs `/sc:reflect --remediate` in N subagents) | `sk/sc-tasklist-protocol/SKILL.md:1614-1631` |
| Make shared state safe for parallel workers | `/sc:save` (single-owner keys overwritten whole) | `cmd/save.md:42-45` |
| Keep outward actions with the coordinator or a pre-authorization | `/sc:task` (TFEP report "committed to git"), `/sc:pr-submit` (push, replies, resolves), `/sc:post-release` (installs, commit/PR) | `sk/sc-task-protocol/SKILL.md:264`; `sk/sc-pr-submit-protocol/SKILL.md:196`; `sk/sc-post-release-protocol/SKILL.md:340` |
| Never-ending mode must be forbidden in a worker brief | `/sc:test` (`--watch`) | `cmd/test.md:22`, `:59` |
| Heartbeats during long attended waits | `/sc:pr-submit` (poll loop, 600 s per wait, several rounds) | `cmd/pr-submit.md:49`; `sk/sc-pr-submit-protocol/SKILL.md:41-64` |

Flag-gated prompts that are safe by default (no change needed if the brief omits the flag): `/sc:reflect --remediate`, `/sc:troubleshoot --fix`, `/sc:release-split --interactive`, `/sc:roadmap --interactive`.

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Field (b) does not block running as an Orca worker | (1) treat "needs top-level" as disqualifying; (2) treat it as "must not run as an Agent-tool subagent" only | The dispatch preamble starts each worker as its own Claude session in its own terminal, so a worker is top-level. Option 2 matches that; `/sc:pr-submit` therefore gets needs-change, not coordinator-only. |
| A prompt behind an opt-in flag still allows "ready" | (1) any prompt anywhere → needs-change; (2) only default-on prompts count | The coordinator controls the flags in the brief. Option 2, with the flag named in the verdict. |
| Long skills read by targeted search plus the deciding sections | (1) read every line of ~20k skill lines; (2) grep for field patterns and read hit regions | Option 2 keeps each claim tied to a read line. Lines not read are not cited. Any field with no hit says "None found" or "None stated" rather than "none". |
| Command-vs-skill conflicts recorded on both sides | (1) pick the more recent file; (2) record both with citations | No file in scope says which side wins (`sk/sc-validate-roadmap-protocol/SKILL.md:20` only says the skill is not a CLI mirror), so both are recorded and the row is needs-change. |
| `/sc:reflect` remediation prompt counted as firing in an Orca worker | (1) assume headless auto-accept applies; (2) assume the interactive prompt fires | The headless rule keys on `claude --print` with no TTY (`sk/sc-reflect-protocol/refs/remediation-handoff.md:239-242`); an Orca worker is a terminal session. Option 2; not tested in this run. |
| Verdict wording for `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` | needs-change vs coordinator-only | Their stated purpose (orchestrate, decompose, interview a person) is the coordinator's or a human's role under "Orca on top" (`.dev/orca-command-refactor/README.md:6`), so changing them into workers would remove their purpose. |

## UNVERIFIED items
1. Whether an Agent-tool subagent can itself spawn agents, use `Monitor`, or answer a remediation offer. No file read here states it; `sk/tdd/SKILL.md:238` only says the skill avoids subagent→agent nesting, and `sk/sc-pr-submit-protocol/SKILL.md:37-39` forbids it for pr-submit. Affects `/sc:tasklist` (b), `/sc:swarm-wizard` (b), and anyone running workflow/reflect inside a subagent.
2. Whether an Orca worker session is treated as `--print` (headless) by `/sc:reflect`; assumed not (see Decisions).
3. Whether the frontmatter `personas: [deep-research-agent]` in `cmd/research.md:7` loads `ag/deep-research-agent.md` behaviour at run time.
4. Whether `/sc:workflow` itself runs `git add .dev/tasks` or only states the rule (`sk/sc-workflow-protocol/SKILL.md:28`).
5. Whether `/sc:pr-submit` writes any human-readable summary file besides `monitor-run-<PR>.jsonl`; only the JSONL is named (`sk/sc-pr-submit-protocol/SKILL.md:170`).
6. How `/sc:validate-tests --report` writes its file: the skill has no Write or Bash, the command has Bash only (`cmd/validate-tests.md:6`; `sk/sc-validate-tests-protocol/SKILL.md:4`).
10. Independent check: a fresh `evidence-validator` agent re-read about 270 citations in the notes and summary and found 3 substantive defects and 3 small ones, all fixed above (release-split and tdd prompts, the validate-tests tool wording, three line or quote corrections). It did not re-check the Method, Decisions or UNVERIFIED sections.
7. Whether the `/sc:roadmap` skill shells out to `superclaude roadmap run` or performs the waves itself; the command calls the CLI its "deterministic counterpart" (`cmd/roadmap.md:92`) and the skill describes waves plus a CLI crosswalk (`sk/sc-roadmap-protocol/SKILL.md:107-130`).
8. Who answers the reflect remediation offer that `/sc:tasklist` Stage 10.5 triggers inside subagents (`sk/sc-tasklist-protocol/SKILL.md:1631`).
9. No command was run end to end as an Orca worker in this task; every verdict is from reading files.
