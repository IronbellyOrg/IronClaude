# Synthesis 01: Sections 1 and 2 (Overview, Architecture) - Observer, Sweep, Agent-Work-Report, Dashboard Design Package

> Path convention (stated once): code paths are relative to the repo root at origin/master 61ac2c2e6; design-package files carry their checkout path (`/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/`, docs branch `docs/409-orca-dashboard-designs`, commit 495eb96d1; the same 406-file content is on origin/master through PR #503). `.dev/research/orca-dashboard-20261105/` is local-only and untracked. Tags: [CODE-VERIFIED], [UNVERIFIED], [DESIGNED]. Gap-fill file GF-1 is the authority for every C8 label. Facts and overlaps only; no unification is recommended.

## 1. Overview

Four subjects sit in one family around Orca, the agent-session manager. Three are live code on origin/master: `superclaude observe` (a terminal dashboard and JSON snapshot of Orca workers, plus coordinator questions for one named Run), `superclaude sweep run` / `/sc:sweep` (a read-only classifier that writes one dated report), and the `agent-work-report` skill (the daily report that gathers GitHub, ClickUp and Orca sessions, with a built reader side for a "living report"). Two are designed only: the orchestrator's writer of living-report entries (`superclaude orchestrator report-entry`, PR B, no PR open, inside `docs/designs/orchestrator.md`, which "holds no implementation code"), and the issue-409 dashboard design package, a synthetic prototype (20 designs rendered from fake fixtures) that says it is "not a production integration".

**What it does:** the observer shows Orca worker rows and coordinator questions; the sweep labels each session with one of 8 classes; the report skill writes the daily work report; the package shows 20 mock layouts.
**Who uses it:** the observer, a person in a terminal (no in-repo consumer reads its snapshot except tests); the sweep, the coordinator or a person, never a worker (WC-16 is a prose duty, no code calls it); the report skill, the owner (Clay) through a page and a ClickUp DM; the package, human reviewers.
**Where it lives:** `src/superclaude/cli/observe/`, `src/superclaude/cli/sweep/`, `src/superclaude/skills/agent-work-report/`, and the design package folder above.
**Key numbers** (grep/wc counts of definitions and lines; no test was run; "tests" are top-level `def test_`, not pytest-collected cases):

| Subject | Files | Lines | Tests | Merge record |
|---|---|---|---|---|
| Observer | 13 `.py` + `snapshot.schema.json`; `fixtures/` 20 entries (19 JSON) | 6,011 + 158 | `tests/observe`: 26 test files, 565 defs | PRs #503, #514, #577, #592, #598, #673 |
| Sweep | 6 `.py` (5 modules + `__init__`) | 3,759 | `tests/sweep`: 7 files, 323 defs; 28 drift guards in `tests/commands/test_sweep_command.py` | PR #539 (2026-11-14) |
| Agent-work-report | 16 scripts, 7 templates, `config.json`, `SKILL.md` | 5,777 + 194 | `tests/skills/test_agent_work_report.py`: 4,005 lines, 142 defs | PR #684 (2026-11-20) |
| Design package (checkout path) | 406 files (412 with 6 `.pyc`): 20 designs, 19 scenario JSON incl. base, 360 exports, 2 galleries, 2 PDFs; 6 renderer files | 1,011 (renderer) | 19 `unittest` + 1 Node DOM test | on master via #503 (545 files) |
| Orchestrator design | 1 file `docs/designs/orchestrator.md` | 1,412 | none (no code) | PR #681; PR D #682 and C #684 merged; A #686, P #690 open; B none |

---

## 2. Architecture

### 2.1 High-Level Architecture

```
 SOURCES                        SUBJECT                          OUTPUT -> CONSUMER
 ------------------------------ -------------------------------- ------------------------------------------
 Orca CLI: worker-list,     --> OBSERVER [live]                  screen; snapshot.json v1 (0600, replaced
   check --all (questions)      adapter -> parse -> collector        each cycle); observe-<ts>.txt
                                -> view -> render / export       -> a person; in-repo reader: tests only
 Orca CLI: worker-list,     --> SWEEP [live]                     .dev/sweeps/<UTC>-sweep.md + JSON v1 (stdout)
   worker-show, task-list,      probes -> classify -> report     -> coordinator or person; WC-16 "read before
   worktree ps                  (only write: one report file)       acting, <= 1 per 5 min" is a prose duty;
 git: 4 exact argv shapes                                           no code reads a published report
 disk: .dev/tasks, transcripts,
   ccsession orca-tabs
 GitHub (gh, 2 orgs), ClickUp --> AGENT-WORK-REPORT [live]       run folder; report.html (127.0.0.1:8765);
   REST, Orca terminals, hook       16 scripts, 15 steps; the       ClickUp DM, Orca unread mark and tab;
   file, transcripts, /proc         model writes judgement parts    git commit by the model -> Clay
                                        ^ entry files .dev/coordinator/orchestrated/ (reader built)
                                        | no writer on master
 (no live source)               --> ORCHESTRATOR [DESIGNED]      writer `superclaude orchestrator report-entry`
                                    wake, waves, check --wait       (PR B, no PR); bound by WC-16? [UNVERIFIED]
 fake fixture.json + scenarios/ --> DESIGN PACKAGE [prototype]   360 exports, 2 galleries, 2 PDFs -> reviewers
```

- [CODE-VERIFIED] No code links the observer, the sweep and the report skill: a grep finds no reference between the three packages, and nothing under `commands/`, `skills/`, `agents/`, `core/`, `hooks/` names `superclaude observe`. "The observer reads the sweep JSON" exists only as an undecided proposal in the live issue-409 body (research 06 section 8.3).
- The observer's question read (`orchestration check --all --types question --run <id> --json`) reads the Run mailbox that the coordinator consumes. Whether it is non-acknowledging is [UNVERIFIED]: recorded probes show non-consumption only for the owner-bound reader, and the owner accepted the remainder on 2026-11-12.

### 2.2 Subsystem Map

| Subsystem (Section 5) | Purpose | Primary Directory | Key Files (lines) |
|---|---|---|---|
| 5.1 Observer data contract | Read Orca through 3 argv templates, parse strictly, retain rows and questions, export a closed JSON schema | `src/superclaude/cli/observe/` | `adapter.py` (512), `parse.py` (835), `collector.py` (361), `questions.py` (142), `export.py` (274), `snapshot.schema.json` (158), `fixtures/`; `_find_orca` at `src/superclaude/cli/install_user_setup.py:247-270` |
| 5.2 Observer interaction layer | CLI group, 7 flags, key map, 160/116/80-column layouts, Decision Desk, gate constants | `src/superclaude/cli/observe/` | `commands.py` (524), `view.py` (1,300), `render.py` (1,461), `keys.py` (235), `terminal.py` (192), `theme.py` (126), `sanitize.py` (48); registered at `src/superclaude/cli/main.py:590-592` |
| 5.3 Sweep classifier and joins | 9 ordered rules, 8 classes, transcript-to-Dispatch joins, Safe to close and Removable values | `src/superclaude/cli/sweep/` | `classify.py` (1,009), `models.py` (278) |
| 5.4 Sweep read side and WC-16 | Allow-listed Orca and git reads, disk reads, 12-section report, JSON v1, atomic publish, coordinator duty | `src/superclaude/cli/sweep/`; `src/superclaude/commands/sweep.md` (70); `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (66) | `probes.py` (1,477), `report.py` (695), `commands.py` (288); `src/superclaude/core/WORKER-CONTRACT.md:287-289` |
| 5.5 Agent-work-report and living report | 15-step daily pipeline, delivery gate, ClickUp DM, reader side of the entry files | `src/superclaude/skills/agent-work-report/` | `scripts/run.py` (887), `common.py` (507), `sessions.py` (444), `waker.py` (405), `exclude.py` (109); `SKILL.md` (194) |
| 5.6 Design package and its relation to the observer | 20 synthetic layouts, fixtures, exports, gallery; palette and fixture names shared with the observer | `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/` | `render.py` (130), `fixtures.py` (122), `canvas.py` (122), `layouts/` (637), `tests/test_designs.py` (117) |

### 2.3 Key Design Decisions (As Built)

| Decision | What Was Built | Rationale | TDD Divergence (design or docs) |
|---|---|---|---|
| Python + Rich stack | Observer is Python + Rich (`rich.live.Live`); package prototype is Python + Pillow 13.0.0 + wcwidth 0.9.4, "not a production-stack commitment"; the 8 palette values match; no shared code or data (`ARCHITECTURE-SPINE.md:172`) | Owner decision CONFIRMED 2026-11-08 (`.dev/issues/409/bmad/spec-orca-observer/stack.md:3`, origin/master) | Package `README.md:46-48`, `description.md` and live issue body line 127 still name Bubble Tea / Lip Gloss / Bubbles the leading candidate (SD-25); a Go reader is deferred |
| Observer, sweep and agent-work-report are separate Orca wrappers | Observer: `_find_orca` tries `orca-ide` then `orca`, accepts one whose `skills list --json` shows a topic named `orca-cli`. Sweep: `orca_binary()` = `$ORCA_CLI_COMMAND` else `orca-ide`. Agent-work-report: bare `orca` and `gh` from PATH through `common.run_cmd`. No shared module | Reason for three wrappers not stated [UNVERIFIED]; `_find_orca` docstring: a bare `orca` on Linux is usually the GNOME screen reader | Sweep comment "never bare orca (SPEC section 8, INV-017)"; `$ORCA_CLI_COMMAND` value is unvalidated |
| Staged observer release behind gate constants | R0 fixtures, R1 live ledger, R2 questions (`QUESTION_GATE_PASSED = True`, owner pass record 2026-11-12), R3 link and Decision Desk (`QUESTION_LINK_PASSED = True`, status line recorded by the agent on the owner's chat "yes", 2026-11-17); R4 remote fleet, closure evidence, history, write-back "Not established" | Owner decision "Stage it" (`owner-decisions-20261108.md:5-9`); DIRECTION-SELECTED passed 2026-11-16 | Live issue-409 body still says "No direction chosen", "observer does not exist", PR #539 open (SD-21 to SD-23); `--fixture` with `--questions` is refused (pointer in 2.5) |

### 2.4 Technology Stack (Feature-Specific)

| Technology | Version | Purpose in This Feature |
|---|---|---|
| Rich (`rich.live.Live`, `screen=True`) | not stated in research | Observer screen and styled `--once` text; replaced "Go + Bubble Tea" by owner decision |
| `termios` / `tty` / `fcntl`, one daemon thread `observe-collector` | stdlib | Observer key reader (POSIX only; win32 exits 2) and 15 s polling; `--once` never imports `keys.py` |
| `jsonschema` Draft7, `pexpect` | not stated in research | Observer tests validate `snapshot.json` against `snapshot.schema.json`; pty tests skip without pexpect |
| PyYAML `yaml.safe_load` | not stated in research | Sweep reads worker contract files (1 MiB cap) |
| Orca CLI (`orca-ide`, `orca`, `$ORCA_CLI_COMMAND`) | sweep pins `CHECKED_ORCA_VERSION = "1.4.245"` (`report.py:23`) | Only Orca data source of the observer and the sweep; the report skill also writes tabs, terminals, unread marks |
| Pillow, wcwidth, DejaVu Sans Mono TTF | `Pillow==13.0.0`, `wcwidth==0.9.4`; font path fixed in `render.py:16-17` (existence on this host not checked) | Design package renderer (PNG, PDF, SVG, ANSI) |

### 2.5 Family at a glance

| Subject | Data sources read | Outputs, format, where written | Live vs designed (evidence) | Consumers | Overlaps in purpose |
|---|---|---|---|---|---|
| Observer | Orca only: `worker-list --json --limit 100` (up to 5 pages a cycle; 4 + 1 question call with `--questions`), `check --all --types question --run <id> --json` (one named Run, from the terminal that holds it), `skills list --json`. No GitHub, ClickUp, git or disk reads | Screen at 160/116/80 columns; `snapshot.json` (schemaVersion 1, closed schema, 20 of 31 row attributes, no question text, 0600, replaced each 15 s cycle, `$XDG_STATE_HOME/superclaude/observe`); `observe-<ts>.txt` records (include question subjects; accumulate) | Built; R0 to R3 enabled (`commands.py:67, 70` both True; PRs #503 to #673 merged). Not established: R4 remote fleet, closure evidence, history over 100 rows, write-back. R2/R3 live path wired; fixture replay of the question ledger and Decision Desk is refused (D-1, DEFECT-CANDIDATE) | A person at a terminal; snapshot read only by tests (G-09) | Raw Orca fields shown, no classes; a question panel (one meaning of "waits on a person"); reads `worker-list` as the sweep does; palette and fixture names shared with the package |
| Sweep | Orca (`run-current`, `worker-list --run`, up to 50 `worker-show`, `task-list --ready`, `task-list`, `worktree ps --json`); git (status, config, ls-files, check-attr); disk (`.dev/tasks/{to-do,done}`, contract files, last 256 KiB of transcripts, ccsession tab map, Orca version file). No messages, no GitHub | `<root>/.dev/sweeps/<UTC>-sweep.md` (12 sections, dated, never tracked, `.gitignore:255-256`) plus JSON v1 (12 top-level keys) on stdout; exit 0, 1 or 2 | Built (PR #539); 6 of 8 classes can print on live data. `stalled (proved)`, `fenced`, `agent_wait_since`, `Safe to close = yes`, `Removable = yes` cannot (KNOWN LIMIT, cited). Recorded live runs (not re-run): 180 of 180 rows (2026-11-12) and 263 of 264 rows (issue #590, [UNVERIFIED]) read `could not determine` | Coordinator (WC-16, prose duty) or a person; the sweep skill Reads its own report; no code reads published reports (G-17) | 8-class vocabulary; "waiting on a person" (a)/(b); tab-map join; own sanitizer; `orca-ide` wrapper |
| Agent-work-report | GitHub (`gh`, two orgs, Projects, `involves` search), ClickUp REST GETs, Orca terminals, worktrees, automations, the agent hook file, transcripts, `/proc`, `git remote get-url`; entry files under `.dev/coordinator/orchestrated/` | Run folder `.dev/coordinator/runs/<run id>/` (`overview.md`, `snapshot.json`, `script-checks.md`, `summary.md`, `report.html`, ...); shared `.dev/coordinator/report.html` on 127.0.0.1:8765; ClickUp DM; Orca unread mark and tab; typed wake line; git commit by the model | Daily pipeline built (PR #684; 142 test defs, not run) with the living-report reader side. Entry-file writer designed only (KNOWN LIMIT sequenced to PR B, C8-6); `orchestrator_repo` route fails on master (CC-02, PR A #686 open); Orca automations [UNVERIFIED] | Clay (page and DM); the coordinator session `waker.py` starts; the sweep and observer read none of it | 6 model-judged statuses; `waiting on you`; hook-file join; two sanitizer functions; bare `orca` |
| Dashboard design package | None live: deterministic synthetic `fixture.json` and 18 scenario files from `fixtures.py` (no Orca adapter, environment or network read); proposed schema "NOT an Orca API" | Per batch: 180 export files (10 designs x 3 widths x 6 suffixes), `contact-sheet.png`, `portfolio.pdf`, `manifest.json` (with fixture sha256), `gallery.html` (19 scenarios x 10 designs x 3 widths); batch 2 under `agent-focus/` | Designed only as a product: README "not a production integration"; QA.md verdict FAIL for pre-correction snapshots, no later independent verdict; 19 tests not run [UNVERIFIED]. Observer shows 3 of 20 designs in reduced form | Human reviewers; the observer inherits 9 of 9 fixture names and 8 palette values, 0 of 10 fixture contents | Three designs map to observer views A, B, C; own sanitizer; "navigation only" contract against the sweep's `Next inspection` text (undecided, issue-409 alignment item 2) |

Overlaps in purpose (facts only; the research states no decision about any of them):

| Overlap | Observer | Sweep | Agent-work-report | Designed or contract |
|---|---|---|---|---|
| Status vocabularies | No classes; `worker_state`, `dispatch_status`, `terminal_state`, `outcome`, `next_action`, `liveness` shown as separate raw fields (`view.py:566-584`); `projection.attention` present, not parsed | 8 classes (`models.CLASSES`): waiting on a person, stalled (proved), fenced, working, finished, idle, person session (active), could not determine | 6 statuses judged by the model: working, progressed, waiting on you, stuck, stalled, done; Orca state never read | Orchestrator FR-9: 8 states (working, question, gated, delivered, claimed-missing, stalled, failed, not-started), mapping to `worker-list` fields not stated, spec not in the repo [UNVERIFIED]; worker contract ladder S0 to S11. `working` and `stalled` occur in more than one set |
| "Waits on a person" | Coordinator-question panel for one named Run; "seen, not resolved"; ledger labelled "worker-reported, not questions" when questions are off | Class `waiting on a person`: (a) blocked contract or non-null `agentWait` (rule 4(a) unproven on live data [UNVERIFIED]); (b) frozen plan or ready Task; "Requested by" and "Decision owner" fixed to `unknown` | `waiting on you`: last turn asks a question or a tool call waited over 15 minutes; the thresholds are model instruction, no script computes them; plus "Needs you" entries | FR-9 `question` and `gated`; worker contract S4 and S5 |
| Terminal-to-transcript join | None (no transcripts read) | `dispatch.assigneeHandle` (`term_<uuid>`) against ccsession `orca-tabs` file names and handles; `JOIN_PATH = "B"` (Dispatch time window); path A unseen on live data [UNVERIFIED] | Orca hook file entries keyed `<tabId>:<leafId>` give `providerSession.id` and `transcriptPath`; `ORCA_TERMINAL_HANDLE` from `/proc` marks a running Claude | None |
| Sanitizers | `observe/sanitize.py` (48 lines): drops Cc/Cf/Cs and all escape forms | `sweep/report.py:569-599`: strips escapes, drops Cc/Cf/Cs/Co, escapes `\ \| < > [ ]`, cells cut at 200; `report_path` left unsanitized | `activity.clean` and `common.safe_title` (two functions; control characters removed, titles capped at 200) | Package `canvas.py:10-17`, never imported by the observer (`sanitize.py:3-4`) |

C8 pointers (details in Section 14; GF-1 is the authority; remediation task not created (read-only brief); flagged for the owner):

- KNOWN LIMIT (cited): `stalled (proved)` (SPEC:231-232), `fenced` (SPEC:251), `agent_wait_since` (SPEC:238), `Safe to close` and `Removable` never `yes` (SPEC:106, 274, 338), carried in `docs/designs/orchestrator-mode.md` as: stalled and fenced 493, 636, 841, 877; `agent_wait_since` 493, 494, 649, 1003; `Safe to close` 794; `Removable` 795; SPEC = origin/master `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`. Living-report entry writer: sequenced to PR B (`docs/designs/orchestrator.md:3, 510, 791, 1020, 1041`). `orchestrator_repo`: sequenced to PR A. No work item owns the "source mapping" of SPEC:232 (U-40).
- DEFECT-CANDIDATE: `superclaude observe --fixture ... --questions` is refused, so the question ledger and Decision Desk cannot be replayed from fixtures (D-1; no cited scope decision); `prefs.py answer <run> <session url> session` cannot answer a "Needs you" session entry (`prefs.py:20, 30-32`).
