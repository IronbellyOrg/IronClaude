---
id: "OBSERVER-SWEEP-DASHBOARD-TECHREF"
title: "Observer, Sweep and Dashboard (IronClaude) - Technical Reference"
description: "Post-implementation technical reference documenting the architecture, subsystems, data flow, and operational details of the observer, the sweep, the living agent work report and the Orca dashboard design package of IronClaude as currently built (and, where stated, as designed only)"
version: "1.0"
status: "🟡 Draft"
type: "📖 Technical Reference"
priority: "🔼 High"
created_date: "2026-11-20"
updated_date: "2026-11-20"
assigned_to: "IronClaude maintainers"
autogen: false
autogen_method: ""
coordinator: "N/A"
parent_doc: "N/A (no single TDD; design package at /home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/ and docs/designs/orchestrator.md)"
parent_task: "/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/TASK-TECHREF-observer-sweep-dashboard-20261120-040203.md"
related_prd: "N/A"
related_tdd: "N/A"
depends_on:
- "origin/master 61ac2c2e6 (code snapshot)"
- "docs branch docs/409-orca-dashboard-designs, commit 495eb96d1 (design package)"
related_docs:
- "/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/README.md"
- "docs/designs/orchestrator.md (origin/master)"
- "docs/designs/orchestrator-mode.md (origin/master)"
tags:
- technical-reference
- observer
- sweep
- agent-work-report
- orca-dashboard
- post-implementation
- architecture
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# Observer, Sweep and Dashboard (IronClaude) - Technical Reference

> **WHAT:** Post-implementation technical reference documenting the architecture, subsystems, data flow, and operational details of the observer (`superclaude observe`), the sweep (`superclaude sweep run`), the living agent work report (`agent-work-report` skill) and the Orca dashboard design package (issue 409) of IronClaude as currently built; designed-only parts are tagged.
> **WHY:** Gives the owner one exact, cited picture of these four subjects for the later unification brainstorm, so nobody has to read every source file. Where code and documents disagree, this document records the disagreement and the evidence; it does not pick a winner and recommends no unification.
> **HOW TO USE:** Engineers and AI agents read Sections 1, 2 (especially 2.5 "Family at a glance") and 14 first; they consult Section 5 before touching a subsystem. Maintainers update it when any of the four subjects changes.

**Purpose:** An exact, cited picture of the observer, the sweep, the living work report and the Orca dashboard design package for the owner's later unification brainstorm; facts and overlaps only, no recommendation.

**Date:** 2026-11-20

**Tier:** Standard

**Research files:** 11 codebase research files (6 research files plus 5 gap-fill files GF-1 to GF-5), 0 web research files

**Scope:** Four subjects: the observer (`src/superclaude/cli/observe/`), the sweep (`src/superclaude/cli/sweep/`, with `src/superclaude/commands/sweep.md` and `src/superclaude/skills/sc-sweep-protocol/`), the living agent work report (`src/superclaude/skills/agent-work-report/`) and the Orca dashboard design package (`/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/`). Code citations are relative to the repo root at origin/master 61ac2c2e6; design-package files carry their checkout path (docs branch `docs/409-orca-dashboard-designs`, commit 495eb96d1); `.dev/research/orca-dashboard-20261105/` is local-only (untracked).

---

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| Requirements | Issue 409 body and owner decisions (no Product PRD) | Owner | See Section 14 for stale statements |
| Design | `docs/designs/orchestrator.md`, `docs/designs/orchestrator-mode.md`, the #409 design package | Engineering | Orchestrator design approved 2026-11-19, holds no implementation code |
| **Implementation** | **This Technical Reference** | **Engineering** | **Living document: updated with every significant change** |

---

## Document Information

| Field | Value |
|-------|-------|
| **Feature Name** | Observer, Sweep, living agent work report and Orca dashboard design package |
| **Feature Type** | Backend / CLI tooling around Orca (Python); one design-only prototype |
| **Tech Lead** | Not stated in the research |
| **Engineering Team** | IronClaude maintainers |
| **Maintained By** | IronClaude maintainers (owner: Clay, for the report skill) |
| **Source Location** | `src/superclaude/cli/observe/`, `src/superclaude/cli/sweep/`, `src/superclaude/skills/agent-work-report/`, `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/` |
| **Last Verified Against Code** | 2026-11-20 (origin/master 61ac2c2e6; docs-branch commit 495eb96d1 for the design package) |
| **Implementation Status** | Observer, sweep and report skill: Active Development / Stable by subject (see Section 1 and Section 14); orchestrator report-entry writer and dashboard package: designed only |

### Living Document Contract

This document MUST be updated when:
- A component is added, removed, or significantly refactored
- A subsystem's behavior, data flow, or interface changes
- New conventions or patterns are introduced to the feature
- State shape or management approach changes
- The feature is deprecated or replaced

---

## Completeness Status

**Completeness Checklist:**
- [x] Section 1: Overview — **Complete**
- [x] Section 2: Architecture — **Complete**
- [x] Section 3: Directory Structure — **Complete**
- [x] Section 4: Data Flow — **Complete**
- [x] Section 5: Subsystem Reference — **Complete (5.1 to 5.6)**
- [x] Section 6: State Management *(if applicable)* — **N/A: the observer, sweep and agent-work-report are CLI and file based tools and the design package is a static renderer, so there is no client-side store; the runtime state that does exist is tabulated in Section 6**
- [x] Section 7: Component Inventory *(if applicable)* — **N/A: these tools have no component tree; the subsystem tables in Section 5 are the inventory**
- [x] Section 8: API & Integration Points *(if applicable)* — **Complete**
- [x] Section 9: Configuration & Environment *(if applicable)* — **Complete**
- [x] Section 10: Error Handling & Edge Cases — **Complete**
- [x] Section 11: Performance Characteristics — **Complete (no performance was measured; counts only)**
- [x] Section 12: Conventions & Patterns — **Complete**
- [x] Section 13: Extension Guide — **Complete**
- [x] Section 14: Known Limitations & Technical Debt — **Complete (all code contradictions, stale documents, unverified items and the C8 defect-candidate analysis)**
- [x] Section 15: Verification & Accuracy — **Complete**
- [x] Section 16: Glossary *(if applicable)* — **Complete**
- [ ] All links verified — **Not done (assembly only; QA agents validate content)**
- [ ] Reviewed by the QA agents — **Pending QA review**

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | Code snapshot origin/master 61ac2c2e6; design package at docs-branch commit 495eb96d1; `docs/designs/orchestrator.md` |
| **Upstream** | Feeds from: source code, the #409 design package, the issue-409 body and owner decisions, `docs/designs/orchestrator.md` and `orchestrator-mode.md` |
| **Downstream** | Feeds to: the owner's later unification brainstorm; onboarding for the four subjects |
| **Change Impact** | Notify: the owner; maintainers of `superclaude observe`, `superclaude sweep`, the `agent-work-report` skill and the orchestrator design (PRs A #686, B, P #690) |
| **Review Cadence** | As-needed (re-verify after any PR that touches the four subjects) |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Directory Structure](#3-directory-structure)
4. [Data Flow](#4-data-flow)
5. [Subsystem Reference](#5-subsystem-reference)
6. [State Management](#6-state-management)
7. [Component Inventory](#7-component-inventory)
8. [API & Integration Points](#8-api--integration-points)
9. [Configuration & Environment](#9-configuration--environment)
10. [Error Handling & Edge Cases](#10-error-handling--edge-cases)
11. [Performance Characteristics](#11-performance-characteristics)
12. [Conventions & Patterns](#12-conventions--patterns)
13. [Extension Guide](#13-extension-guide)
14. [Known Limitations & Technical Debt](#14-known-limitations--technical-debt)
15. [Verification & Accuracy](#15-verification--accuracy)
16. [Glossary](#16-glossary)
- [Appendix A: Document Provenance](#appendix-a-document-provenance)
- [Document History](#document-history)

---

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
- The observer's question read reads the Run mailbox that the coordinator consumes; whether it is non-acknowledging is [UNVERIFIED] (5.1).

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
| Staged observer release behind gate constants | R0 fixtures, R1 live ledger, R2 questions (`QUESTION_GATE_PASSED = True`, owner pass record 2026-11-12), R3 link and Decision Desk (`QUESTION_LINK_PASSED = True`, status line recorded by the agent on the owner's chat "yes", 2026-11-17); R4 remote fleet, closure evidence, history, write-back "Not established" | Owner decision "Stage it" (`owner-decisions-20261108.md:5-9`); DIRECTION-SELECTED passed 2026-11-16 | Live issue-409 body still says "No direction chosen", "observer does not exist", PR #539 open (SD-21 to SD-23); `--fixture` with `--questions` is refused (14.5) |

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
| Observer | Orca only: `worker-list --json --limit 100` (up to 5 pages a cycle; 4 + 1 question call with `--questions`), `check --all --types question --run <id> --json` (one named Run, from the terminal that holds it), `skills list --json`. No GitHub, ClickUp, git or disk reads | Screen at 160/116/80 columns; `snapshot.json` (schemaVersion 1, closed schema, 20 of 31 row attributes, no question text, 0600, replaced each 15 s cycle, `$XDG_STATE_HOME/superclaude/observe`); `observe-<ts>.txt` records (include question subjects; accumulate) | Built; R0 to R3 enabled (`commands.py:67, 70` both True; PRs #503 to #673 merged). Not established: R4 remote fleet, closure evidence, history over 100 rows, write-back. R2/R3 live path wired; fixture replay of the question ledger and Decision Desk is refused (D-1, KNOWN LIMIT (cited), 14.5) | A person at a terminal; snapshot read only by tests (G-09) | Raw Orca fields shown, no classes; a question panel (one meaning of "waits on a person"); reads `worker-list` as the sweep does; palette and fixture names shared with the package |
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

C8 labels (KNOWN LIMIT and DEFECT-CANDIDATE, with their declaring lines and the on-record text) are tabulated once, in 14.5. PKG in Sections 3 to 5 = `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/`; SPEC and DESIGN are defined in 14.5. Tags: [CODE-VERIFIED] built, read in code; [DESIGNED] design text only, not built; [UNVERIFIED] stays open; [CODE-CONTRADICTED] a documentation statement contradicted by code.

---

## 3. Directory Structure

```
src/superclaude/cli/observe/               # `superclaude observe` (registered main.py:590-592)  [CODE-VERIFIED]
├── adapter.py     # the only Orca edge: 3 argv templates, forbidden-prefix list, caps (LiveSource)
├── collector.py   # one daemon poll thread, CycleResult, FixtureSource
├── parse.py       # strict envelope, lenient rows, UNKNOWN sentinel, merge
├── questions.py   # bounded question retention, nothing is ever closed
├── view.py        # build_view (STALE rule), apply_key, View dataclasses
├── render.py  terminal.py  theme.py  sanitize.py  keys.py   # layouts 160/116/80; policy; colour roles; escape stripping; key decoder (POSIX only)
├── export.py      # record_text, snapshot_json, write_atomic, state_dir
├── commands.py    # click group `observe`, gate constants, run_once / run_loop
├── snapshot.schema.json                    # Draft-07, closed, schemaVersion 1 (PROPOSED, not an Orca contract)
└── fixtures/      # worker-list-shaped JSON: base + 9 variants, golden-*, golden-question-*, question-cap-100
tests/observe/    # test_*.py, golden_*.json, record_golden*.py, release1_surface.py, live_child.py, conftest.py

src/superclaude/cli/sweep/                 # `superclaude sweep run` (registered main.py:581-583)  [CODE-VERIFIED]
├── commands.py    # click group `sweep`, command `run`; _publish = the only write
├── models.py      # frozen dataclasses, CLASSES (8), JSON_SCHEMA_VERSION = 1
├── probes.py      # only module that starts a subprocess: ALLOWED_ORCA, ALLOWED_GIT, Budget, collect
├── classify.py    # RULES (9), classify, classify_all, joins, safe_to_close, removable
└── report.py      # SECTIONS (12), render, to_json, sanitize
src/superclaude/commands/sweep.md          # /sc:sweep, allowed-tools: Skill; "Nothing starts it automatically" (:22)
src/superclaude/skills/sc-sweep-protocol/SKILL.md   # runs `superclaude sweep run`, Reads the report
src/superclaude/core/WORKER-CONTRACT.md    # WC-16 coordinator duty (:287-289), WC-10 (:46), never-as-worker list (:23)
tests/sweep/ (fixtures/captured-*.json + SOURCES.md)   tests/commands/test_sweep_command.py

src/superclaude/skills/agent-work-report/  # the report skill (PR #684)  [CODE-VERIFIED]
├── SKILL.md  config.json
├── scripts/       # run activity check classify clickup collect common compare exclude match orca_term page prefs render sessions waker (.py)
└── templates/     # item, needs-you, overview, summary, qa-report (unreferenced) .md; report-template.html; report.js
tests/skills/test_agent_work_report.py   tests/skills/test_worker_contract.py

PKG = .dev/design/orca-observer-20261106/  # #409 design package (synthetic only; checkout path)  [CODE-VERIFIED]
├── render.py  fixtures.py  canvas.py  requirements.txt (Pillow, wcwidth)      layouts/{group_a,group_b,agent_focus}.py
├── tests/{test_designs.py, test_gallery.cjs}
├── README DESIGN-CONTRACT PLAN PREVIEWS QA concepts data-dictionary integration-gaps (.md), sources.json, index.html   # no writer in render.py
└── generated by render.py: fixture.json, scenarios/, exports/<160|116|80>/, contact-sheet.png, portfolio.pdf, manifest.json, gallery.html,
    agent-focus/{exports/, contact-sheet.png, portfolio.pdf, manifest.json, gallery.html}   # batch 2

State and output locations written by the tools
~/.local/state/superclaude/observe/   ($XDG_STATE_HOME/superclaude/observe when absolute)  snapshot.json, observe-<ts>.txt     # observer
<root>/.dev/sweeps/                   one dated report per run; .gitignore:255-256 on master, absent from the stale checkout (SD-14)   # sweep
<orchestrator repo>/.dev/coordinator/ # path: $AWR_ROOT, else `orchestrator_repo` in ~/.config/superclaude/issue-watch.json (needs repos.yaml)
├── runs/<id>/         run folder (artifact list in 5.5)         ├── report.html (shared page)       ├── wakes/<time>-<mode>.json
├── orchestrated/      entry files; closed/ (written by run.py), info/                                  └── run.lock refresh.lock action-log.jsonl priorities.json settings.json
```

### 3.1 File Naming Conventions

| Pattern | Convention | Example |
|---------|-----------|---------|
| Observer snapshot | fixed name, replaced atomically (0600) each cycle, no history | `snapshot.json` |
| Observer record | `observe-<generatedAt, ":" to "-">.txt`, whole-second UTC; same-second exports share a file; no pruning | `observe-2026-11-08T12-00-00Z.txt` |
| Observer fixtures | `<variant>.json`, `golden-<kind>.json`, `golden-question-<kind>.json`, `question-cap-100.json` (19 JSON files; M-12) | `golden-success.json` |
| Sweep report | `YYYYMMDD-HHMMSS-sweep.md` from UTC now; collision gives `-2.md` to `-99.md` (`os.link`, never overwrites); temp file `.<stem>.<pid>.tmp` | `<stem>.md`, `<stem>-2.md` |
| Report run folder | `%Y%m%dT%H%M%SZ-<kind>` (daily, hourly, on-demand), `-n` suffix on collision | `runs/<%Y%m%dT%H%M%SZ>-daily` |
| Report entry file | `<owner>__<repo>__<number>.json`; information entries `info/<kind>__<key>.json` | `orchestrated/<owner>__<repo>__<number>.json` |
| Package exports | `exports/<width>/<slug>.<suffix>`, suffixes `.txt .ascii.txt .ansi .svg .png .mono.png`; batch 2 under `agent-focus/` | `exports/160/signal-bridge.png` |
| Package scenarios | `scenarios/<variant>.json`, `scenarios/scale-<owners>-<count>.json`; base is `fixture.json` | `scale-8-80.json` |

Extension edit points: see Section 13.

---

## 4. Data Flow

### 4.1 Primary Data Flow

**(a) Observer** [CODE-VERIFIED] (research 01 s12, 02 s1-4, GF-4 s3-5)
```
orca skills list --json (once, _find_orca)   orchestration worker-list --json --limit 100 [--run][--cursor]   check --all --types question --run <id> --json
        \__ adapter.LiveSource: 3 argv shapes, no shell, no Orca write; 10 s / 8 MiB per call    fixtures/*.json -> FixtureSource (--fixture)
              | SourceResult.pages  (<=5 calls per cycle; 4 + 1 message call with --questions)
              v
 parse.parse_page / parse_questions -> parse.merge / questions.merge_questions -> collector.Collector (daemon thread, 15 s, backoff to 60 s) -> CycleResult
              v
 keys.KeySource -> view.apply_key -> Session --+-> view.build_view -> View (STALE at 45 s, monotonic clock)
                                               |      |-> render.render (policy: terminal.py, theme.py) -> LiveScreen (screen)
                                               |      |-> export.record_text -> stdout (--once) | observe-<ts>.txt (key e)
                                               |      `-> export.snapshot_json -> snapshot.json (once per cycle; fixture runs only with --snapshot)
```
Live R2 and R3 are wired with both gate constants True (commands.py:67, 70); fixture replay of the question ledger is refused (KNOWN LIMIT (cited) D-1 / C8-9, cut R1 applied by PR #577); the non-acknowledging question read is [UNVERIFIED] (U-01); no in-repo reader of the snapshot except tests.

**(b) Sweep** [CODE-VERIFIED] (research 03, 04 s1-3, GF-4 s2)
```
Orca (orca-ide | $ORCA_CLI_COMMAND): run-current, worker-list --run, worker-show (<=50), task-list --ready, task-list, worktree ps --json
git (4 argv shapes, --no-optional-locks)   disk: .dev/tasks/{to-do,done}, contracts, ~/.claude/projects/<key>/*.jsonl tail, ccsession orca-tabs, Orca package.json
        v   probes.collect(ctx, runs, root, budget): the only I/O stage (50 shows / 90 s total / 10 s per call) -> SweepInput
        v   classify.classify_all (pure): merge dispatches -> join A, then B -> _guard -> 9 RULES -> _force_unknown -> safe_to_close / removable -> SweepResult
        v   report.render (pure, 12 sections) -> commands._publish (temp file + os.link, never overwrites) -> <root>/.dev/sweeps/<stem>.md
        v   report.to_json (v1, 12 top-level keys) -> stdout, printed AFTER publish; skill sc-sweep-protocol parses report_path + summary, Reads the report
 Hop 1 (coordinator wake -> /sc:sweep, WC-16) is prose only: no scheduler, no 5-minute throttle in code (research 04 s6.1).
```

**(c) Agent work report and living report** [CODE-VERIFIED for the daily pipeline and the reader side; writer DESIGNED, not built] (research 05 s23-29). The pipeline, run-folder artifacts and gate are in 5.5. The entry-file writer `superclaude orchestrator report-entry` is designed only (KNOWN LIMIT sequenced to PR B, C8-6; the present-tense skill text is [CODE-CONTRADICTED], CC-03); today only `run.py move_to_closed` writes into the entry tree, `exclude.py` excludes nothing and `refresh` renders no "Held by the orchestrator" block (G-37).

**(d) Design package** [CODE-VERIFIED by reading; nothing was run, U-24]. Synthetic only: no Orca, GitHub or ClickUp read. The render pipeline (`render.py` to exports, six files per design and width, contact sheet, PDF, manifest, gallery) is in 5.6.

**(e) Orchestrator design** [DESIGNED; docs/designs/orchestrator.md approved 2026-11-19, "holds no implementation code"] (GF-3 s6, s10)
```
Orca automation orchestrator-poll (*/5, outside repo, UNVERIFIED) -> issue-watch once (built; reshaped by PR A #686, open) -> wake file + Orca send to run:<id> + typed `/sc:orchestrator --wake <id>`
  -> orchestrator waves 0-9 (PR B, no PR): check --wait on the Run mailbox, hourly worker-list -> .orchestrator/{runs,issues,handoffs}/ state files -> report-entry -> .dev/coordinator/orchestrated/
```
The design never names `/sc:sweep`, WC-16, the observer or `.dev/sweeps`; the entry files are the one place the design and the report skill meet (GF-3 s2, s10; 8.2).

### 4.2 Data Sources

| Source | Type | Location | Description |
|--------|------|----------|-------------|
| Orca CLI reads (observer, sweep, report skill) | Orca CLI read | every verb, binary and call site per tool is in 8.1; GitHub, ClickUp, git, local page server and environment variables are in 8.3 and 9.2 | observer 3 argv shapes (31 row keys read, `parse.py:58-90`; `consumer_fenced` and `no_active_terminal` on the question read; non-owner non-consumption [UNVERIFIED], U-01; `_find_orca` discovery, odd `topics` shape [UNVERIFIED], U-03); sweep 10 templates, 6 called, `agentWait` read from `worker-show` (non-null meaning [UNVERIFIED], U-11); report skill terminal, worktree, automations and tab verbs (writes: terminal text and creation, unread mark, browser tab); the orchestrator design's about 30 verb forms are [DESIGNED] |
| Observer fixtures | static JSON | `src/superclaude/cli/observe/fixtures/*.json` via `--fixture <name>` (parse.py:750-835) | worker-list-shaped `cycles`; question fixtures reach tests through a fake runner, never the CLI (D-1, 14.5) |
| Sweep disk | files | `<worktree>/.dev/tasks/{to-do,done}` + `progress.md`; contracts named by task text; `~/.claude/projects/<key>/*.jsonl` (last 256 KiB); `<XDG_STATE_HOME>/ccsession/orca-tabs/*`; Orca `package.json` (fixed Linux path) | reads only, each checked with `_inside`; remote hosts never read |
| Report state | files | `config.json` (14 keys), `priorities.json`, `action-log.jsonl`, previous run's `snapshot.json` / `notes.json`, `orchestrated/*.json` | entry reader is hardened (symlinks refused, bad JSON skipped); no writer on master except `closed/` |
| **Package** fixture | synthetic | `fixtures.py::fixture()` (owners 5/8/10, count 50/80/100, 9 variants) | deterministic: no clock, environment or network (fixtures.py:1); fields proposed, not an Orca API; `sources.json` E01-E04 currency [UNVERIFIED] (U-25) |

### 4.3 Data Transformations

| Transformation | Input | Output | Location | Description |
|---------------|-------|--------|----------|-------------|
| Observer and sweep transformations | worker-list, question and sweep inputs | rows, views, snapshot, classes, report | see 5.1, 5.2, 5.3, 5.4 | argv gate, parse, merge, STALE derivation, Decision Desk join, snapshot export, sanitizers, contract and transcript joins, classify, Safe to close and Removable, publish: one description each in the named subsections (sanitizers compared in 2.5) |
| Report exclude / match | items, sessions, entries | `excluded.json`, `items.json` | exclude.py:59-103; match.py:119-247 | leaves out held issues, PR and `orca://session/<id>`; joins by `linked_pr`, branch PR, branch number, ClickUp id, prompt URL |
| Report classify / compare / gate / entry card | items, priorities, snapshot, `overview.md`, entry JSON | `classified.json`, `compare.json`, PASS / BLOCKED, item text | classify.py:67-128; compare.py:84-186; run.py:204-368; render.py:194-303 | groups and priority order; item closed only by evidence (`gh ... view`); sha256 chain, `close` enforces checks + sha only (CC-04); the entry card is the only transform of an entry file and is reachable today only through tests |
| Package canvas and exports | layout calls, `Canvas` | cells; 6 files per design x width | canvas.py:10-29, 38-55; render.py:41-74 | `sanitize` then `clip` by display width, ASCII fallback; 160-wide PNGs feed contact sheet and PDF (epoch dates); manifest holds `fixture_sha256` |

---

## 5. Subsystem Reference

> **This is the core of the Technical Reference.** Each subsystem gets its own subsection: purpose, key files, mechanism, interfaces, dependencies, consumers and conventions. Subsections 5.1 and 5.2 cover the observer, 5.3 and 5.4 the sweep, 5.5 the agent work report and living report, 5.6 the design package.
> Observer code lives in `src/superclaude/cli/observe/` (written `.../`). R01, R02, GF1, GF4 in 5.1 and 5.2 are the research files and gap-fill files of Appendix A; GF1 and GF4 supersede R01 and R02. Doc-sourced claims are marked "(doc)".

---

### 5.1 Observer data contract (what it reads from Orca, what it emits)

**Purpose:** `superclaude observe` reads Orca's worker list (and, for one named Run, its question messages) through one read-only edge and keeps a ledger in memory. It emits a plain-text record and a closed JSON snapshot (schema version 1, "PROPOSED, not an Orca contract"). This subsection covers what is read, how it is validated and merged, and what is written.

**Key Files:**

| File | Purpose |
|------|---------|
| `.../adapter.py` | Only observer module that imports `subprocess` (pinned, tests/observe/test_commands.py:585-601); three argv templates, forbidden prefixes, caps, `LiveSource` paging, kill and reap |
| `.../parse.py` | `UNKNOWN` sentinel (parse.py:43), the 31-key `_FIELDS`, `parse_page`, `parse_questions`, `merge`, fixture loader |
| `.../collector.py` | `Collector` (single-flight poll thread, backoff), `CycleResult`, `FixtureSource` |
| `.../questions.py` | `merge_questions` (retention bound 1,000), `window_is_full` (100) |
| `.../view.py` (data part) | `STALE_SECONDS = 45.0`, `source_state`, `_meta` -> `SnapshotMeta` (the bridge to export) |
| `.../export.py` | `snapshot_dict`, `snapshot_json`, `record_text`, `write_atomic`, `state_dir` |
| `.../snapshot.schema.json` | Draft-07 closed schema, `schemaVersion` const 1 |
| `.../fixtures/` | 19 JSON files: 10 synthetic variants, 8 golden (4 worker-list, 4 question), `question-cap-100` |
| `src/superclaude/cli/install_user_setup.py:247-270`; `tests/observe/test_{adapter,parse,collector,questions,export,snapshot_schema,golden_contract}.py` | `_find_orca`, the discovery probe the observer borrows; the tests that pin this contract |

**How It Works:** the flow from `_find_orca` to `build_view` and the three outputs is drawn in 4.1 (a).

*Allowed argv (after the binary).* Argv is a list, no shell; `assert_allowed` runs inside both builders and refuses anything else.

| # | Argv | Defined / checked | Notes |
|---|------|-------------------|-------|
| 1 | `skills list --json` | `DISCOVERY_TEMPLATE` adapter.py:30; exact match :148-149 | Run only by `_find_orca`; `LiveSource` never builds it |
| 2 | `orchestration worker-list --json --limit 100 [--run <id>] [--cursor <c>]` | `build_argv` adapter.py:173-183 | Pairs in that order, each at most once; `--limit 100` fixed |
| 3 | `orchestration check --all --types question --run <id> --json` (exactly 8 tokens) | `build_question_argv` :186-190; `_is_question_shape` :111-118 | Run id mandatory; only `read_questions` builds it |

Free values: run id must match `^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$` and a cursor must be a non-empty str with no leading `-`, no NUL, at most 2048 UTF-8 bytes; both limits are commented PROPOSED, not Orca formats (adapter.py:52-55, 92-108) [UNVERIFIED against Orca].

*Forbidden tokens.* `FORBIDDEN_PREFIXES` (adapter.py:34-50) holds 13 prefixes: `check`, `--ack`, `--wait`, `--retry-request`, `--peek`, `dispatch`, `inbox`, `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`. They match by `startswith` at every verb and flag position, never against run or cursor values. In the question shape token indexes 1, 4, 6 (`check`, `question`, run id) are exempt, so `check` is legal only there, and `--wait/--ack/--peek/--retry-request` fail even there. The set may grow but not shrink: test_adapter.py:178-192 asserts a superset of the 13 [CODE-VERIFIED].

*Limits.*

| Limit | Value | Where |
|-------|-------|-------|
| Per-call timeout | 10.0 s; comment "UNVERIFIED until the first permitted live read measures it" (possibly stale, SD-02) | adapter.py:60-62 |
| stdout / stderr / kill | 8 MiB, process group SIGKILLed on overflow; first 2 KiB of stderr kept; 2 s kill grace | adapter.py:58-63, 196-209 |
| Calls per cycle | 5 worker-list (a default argument of `read_pages`, so a caller can override it); 4 + 1 question call when questions are on. Derived, not in code (R01 s12): 500 / 400 rows per cycle; the live sample total was 428, so a questions-on cycle ends PARTIAL | adapter.py:57; collector.py:32-34, 273 |
| Interval, budget, backoff | 15 s wait between cycles, 15 s cycle budget; failed first page doubles the wait 15 -> 30 -> 60 s, any parsed page resets it; 5 s join on stop | collector.py:28-34, 306, 321 |
| Questions | 100-row read window (exactly 100 = "window full"); 1,000 retained, oldest by created time evicted | questions.py:21-22, 125-129 |
| STALE | 45 s on the monotonic clock, computed in `view.py`, never stored by the collector | view.py:33-35, 456-463 |

*Parsing and merging.*
- **Strict envelope:** `ShapeError` (cycle FAILED `shape`) unless `result` is an object, `result.workers` a list, `result.page` an object and `result.page.hasMore` a real bool (parse.py:365-407). **Lenient rows:** a non-object worker entry is counted (`malformed_rows`) and skipped; missing or odd fields become `UNKNOWN` and are listed in `absent_fields`.
- **31 keys read** (`_FIELDS` parse.py:58-90). Any other key is counted in `unrecognised_keys` and its name and value are dropped.
- **`UNKNOWN`** is one singleton, distinct from None/0/False/"" and surviving copy and pickle; JSON null and an absent key both give it. Only export.py turns it into the string "UNKNOWN".
- **Identity** is `(namespace, dispatchId)`; the namespace is `os.path.realpath` of the Orca binary (observer-derived, adapter.py:378-381); a blank `dispatchId` makes an anonymous row (flag `identity unknown`); there is no cross-namespace merge.
- **Merge** (pure, parse.py:654-744): same identity inside a cycle is deduplicated (newer timestamp wins on like fields, else first kept with flag `order unknown`); across cycles an older timestamp never overwrites a newer one (flag `conflict (time went back)`); a row with an identity missing from a cycle stays with `reobserved=False` and is never deleted for absence; an identity-unknown row missing from a complete cycle is dropped (kept only across a PARTIAL cycle, parse.py:726-727). The kept set of identified rows has no cap (derived: it only grows, untested, G-04).
- **STALE:** `source_state` passes `NOT_AVAILABLE`, `NOT_POLLED`, `FAILED` through; `OK` or `PARTIAL` becomes `STALE` at 45 s or with no success, else `OK`. So a `PARTIAL` cycle shows as `OK` and a `FAILED` one never shows STALE. Snapshot `source.status`: OK, STALE, FAILED -> ERROR, anything else -> UNKNOWN (view.py:667).
- **Collector:** `run_once` holds one cycle lock; one daemon thread `observe-collector`; it ends for good only when no Orca was validated. A failed first page keeps the last good rows; a question-read failure never touches backoff or rows.
- **Questions:** keyed `(Run, message.id)`, nothing is ever closed (no closure source). A question missing from a later good read stays, marked `no longer in source window`. Documented limit (questions.py:9-12): `check --all` rows carry no read/acknowledged marker, so a handled question is listed as open while Orca still returns it.

*Error and source codes.* The cycle codes (`not-found`, `timeout`, `overrun`, `output-cap`, `spawn-error`, `exit:<n>`, `json`, `shape`, `cursor-rejected`, `cursor-stalled`, `empty-page`, `consumer-fenced`, `no-active-terminal`) and their effect on the cycle are in 10.1. `overrun` on the question read gives FAILED; `no-question-fixture` (a `--fixture` source has no messages, collector.py:129) gives question source FAILED.

*Snapshot schema versus code.*
- **Match:** every key `snapshot_dict`, `_row_dict` and `_questions_dict` write is declared in the schema, which is closed (`additionalProperties: false`) on root, producer, source, page, collection, questions, items, row, stage, liveness, evidence; the code adds nothing [CODE-VERIFIED]. "Additive-only" is a stated policy in the schema description, not enforced by the file. `SCHEMA_VERSION = 1` (export.py:20).
- **Dropped (collected, absent from the JSON):** 11 of the 31 source attributes: all 7 `resource.*` (id, ownershipState, releaseState, worktreeId, ownerDispatchId, originDispatchId, recoveryAttemptCount), `workspace.id`/`.kind`, `stage.activity`/`.detail`. 20 are exported (19 text fields plus `evidence.durable` as given). Also dropped: row bookkeeping and every flag except `order unknown`, page `warnings`, the other coverage counters (`pages_read`, `empty_page`, `has_more_at_stop`, `stopped_by_*`, `identity_unknown_rows`, `malformed_rows`; the optional `collection` group exports `state`, `collected`, `changedDuringRead`, `duplicatesIgnored`, export.py:209-215), `mode`, `fixture_variant`, `diagnostic`; for questions `subject`, handles, `priority`, `thread_id`, `ask`, `dispatch_id`, `link`; `body`, `to_handle`, `payload` are never kept at all. Tests pin only some drops as privacy exclusions (stage detail and activity, worktreeId, ownershipState, releaseState, warnings, nextCursor); the reason for the other drops is not stated [UNVERIFIED, G-05].
- **Row shape:** flattened (`nextAction.kind` -> `nextAction`, `provider.id` -> `provider`, `host.kind/id` -> `hostKind/hostId`); numbers and booleans become strings via `json.dumps` except `evidence.durable`; optional `orderUnknown`, `notReobserved`, `absentFields`; rows newest first by `liveness.observedAt`, untimed last; every collected row is listed, historical included.
- **Questions group:** ids, `createdAt`, `ageSeconds`, `inWindow` and counts; `closureEvidence` is always "unavailable". The plain-text record differs: it also carries each question's subject (view.py:811; export.py:103-111), never the payload text.
- **Risk:** the schema limits `counts` values to scalars (schema line 50) but the parser keeps nested JSON to depth 6 (parse.py:277-290); no test feeds nested counts [UNVERIFIED].

*Where it writes.* State dir is `$XDG_STATE_HOME/superclaude/observe` when absolute, else `~/.local/state/superclaude/observe` (export.py:236-244). `snapshot.json` has a fixed name; `observe-<generatedAt, ':' -> '-'>.txt` records are written only by the `e` key. `write_atomic`: `mkdir` leaf mode 0700 (umask applies, unrun), `mkstemp` in the same dir (0600), write, fsync, `os.replace`, temp unlinked on failure [CODE-VERIFIED]. The snapshot is overwritten each cycle with no history: one write per published cycle, failed cycles included, when live or `--snapshot` is given; `--once` writes only with `--snapshot`; fixture runs write nothing without it. Records accumulate (no pruning; two exports in one second share a name).

*Is the question read non-acknowledging? [UNVERIFIED].* Code, tests and fixtures are consistent with it but cannot prove it: argv never carries `--ack/--wait/--peek/--retry-request`, only the `--all` form; every recorded reply has `result.acknowledged: null` and rows `delivered_at: null`, and the parser reads neither. Design records (doc, not re-run): RESEARCH-REPORT-phase2-gate.md 2.2 tested it as the owner of a probe Run only; release-gates.md says non-owner non-consumption is UNVERIFIED; the owner accepted that on 2026-11-12. A non-owner read is fenced today anyway. **Contradiction:** R02 section 6.2 says the gate record "resolves" the `check`-without-`--peek` question; R01 section 10 keeps UNVERIFIED because the evidence covers the owner-bound reader on a probe Run only. R01 has the stronger evidence, so UNVERIFIED stands. Orca's `check --all` source and `--help` were not read.

*Discovery.* `_find_orca` tries `orca-ide` then `orca` via `shutil.which`, runs `skills list --json` (timeout 10 s) and accepts exit 0 with a topic named `orca-cli` (install_user_setup.py:247-270) [CODE-VERIFIED]. The `any(...)` over `topics` sits outside the `try`, `LiveSource.discover` has no handler and `_loop` has none, so an odd `topics` shape would end the polling thread silently [UNVERIFIED: read, not run; no covering observer test found].

**Public Interface** (key signatures only):
- `LiveSource.read_pages(clock, budget_deadline, run_id=None, max_calls=MAX_CALLS_PER_CYCLE) -> SourceResult` (adapter.py:395); `read_questions(clock, budget_deadline, run_id) -> SourceResult` (:469); `SourceResult(state, pages, code, diagnostic, capped, calls)`.
- `build_argv(orca, run_id=None, cursor=None)`, `build_question_argv(orca, run_id)`, `assert_allowed(argv)` (raises `ArgvRejected`), `check_run_id`, `check_cursor`; `parse_page`, `parse_questions`, `merge(previous, pages, stopped_by_cap, stopped_by_error) -> Snapshot`, `merge_questions(...)`.
- `Collector(source, clock, interval=15.0, budget=15.0, max_backoff=60.0, run_id=None, questions=False, link=False)` with `run_once() -> CycleResult`, `latest()`, `start()`, `stop()` (collector.py:135-145); `CycleSource` protocol (`mode`, `variant`, `available`, `namespace`, `read_pages`, `read_questions`).
- `snapshot_dict(view)`, `snapshot_json(view)`, `record_text(view)`, `write_atomic(path, text)`, `state_dir()`.

**Dependencies:** Orca CLI (`orca-ide`, then `orca`) as a subprocess only through adapter.py (three argv shapes); `_find_orca` for discovery (import; the allow-list is not applied to this probe, which builds its own argv); `view.py` `source_state`, `_meta`, `SnapshotMeta` (import; export reads only `view.meta`, `view.all_rows`, `view.questions`).

**Consumers:** `.../commands.py` (`run_once`, `run_loop`) builds the `Collector` and writes the snapshot and record files; `tests/observe` validate snapshots against the schema (Draft7Validator in test_commands.py and test_snapshot_schema.py; `conftest.py:17, 32`). Anything else: none found. No module outside `observe/` imports it except the main.py registration, and no agent, command or skill names it; `snapshot.json` in `agent-work-report` is another producer, other schema, other directory.

**Conventions & Patterns:**
- Add an Orca call only by changing the template constants, `assert_allowed` and the pinned tests; add forbidden prefixes freely, never remove one (the test is a floor). Keep `subprocess` imports in adapter.py only.
- Missing values are `UNKNOWN`, never None, 0, False or "" (12.1); exporting a new row field is a four-place edit (13.1 C); treat questions as "seen, not resolved", never present `open` as unhandled.

---

### 5.2 Observer interaction layer, exit codes and release gates

**Purpose:** Describes how a person runs and drives the observer (one click group, seven flags, a key map, three width layouts, the Decision Desk), what it returns to the shell, which constants gate the live question features, and which release stage is built. It is read-only toward Orca: no key and no option writes to it.

**Key Files:**

| File | Purpose |
|------|---------|
| `.../commands.py` | Click group `observe`, `Options`, `Deps`, `execute`, `run_once`, `run_interactive`, `run_loop`, gate constants (:67, :70) |
| `.../view.py` | `build_view`, `apply_cycle`, `apply_key` (what each key means, :1246-1300), `Session`, `View` |
| `.../keys.py` | POSIX key decoder (termios, cbreak) and signal handlers; imported lazily |
| `.../terminal.py`, `.../render.py`, `.../theme.py`, `.../sanitize.py` | Width classes, colour and ASCII policy, the only Rich `Console`; layouts, questions panel, Decision Desk; seven exact state words coloured (not a health verdict); escape stripping |
| `.dev/issues/409/owner-pass-record-20261112.md`, `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` | Gate records; on origin/master only, not in the docs-branch checkout |

**How It Works:**

*Command surface.* `superclaude observe` is a click group with no subcommands; with no flag it starts the interactive loop (commands.py:449-521).

| Flag | Behavior |
|------|----------|
| `--once` | Read once, print, exit (`run_once`) |
| `--width {160,116,80}` | Binds the layout; with `--once` prints the rendered screen instead of the record |
| `--ascii` | Forces ASCII (also on when the stream encoding is not UTF-8) |
| `--fixture <name>` | Replays a synthetic fixture; unknown name is a click usage error |
| `--run <id>` | One Run; without `--questions` it filters the worker-list call (`--run`) |
| `--snapshot <file>` | JSON snapshot path; interactive default is the state dir |
| `--questions` | Lists coordinator questions of the one `--run` Run; needs a live source; guarded by `QUESTION_GATE_PASSED` |

`execute` first applies `_question_refusal` (before any Orca call, discovery included), then routes to `run_once` or `run_interactive`. Interactive polls every 15 s, repaints when dirty or every 0.5 s, and writes one snapshot per cycle (see 5.1). `--once` prints `record_text` by default (plain, no ESC bytes when piped); a colour screen only when `--width` is given and stdout is a TTY.

*Exit codes.*

| Code | Condition (commands.py unless noted) |
|------|--------------------------------------|
| 0 | `--once` read printed; loop ended by `q`, by Ctrl-C (decoded key) or by SIGINT (keys.py:115-117). A failed Orca read is a view state, not an exit code |
| 1 | `--once` snapshot not writable (:264-268); render failure in the loop ("observe: display failed", :364-369); `--questions` with the gate False (:195-196, unreachable today, constant is True) |
| 2 | `--questions` with `--fixture`, without `--run`, or with a rejected run id (:187-194); interactive on win32 (:377-379) or with no terminal on stdin (:385-387); click usage errors (bad `--width`, `--fixture`, `--run`; click's own code) |
| 143, 129 | SIGTERM, SIGHUP while the key source holds the terminal (keys.py:119-125) |

*Key map* (`apply_key`, view.py:1246-1300; keys change the Session only, "there is no refresh key and none reaches Orca"). The decoder emits up, down, enter, escape, backspace, ctrl_c and text; left, right, Home, End, PgUp, PgDn are swallowed.

| Key | Effect |
|-----|--------|
| Ctrl-C (any focus), `q` (not in filter) | Quit |
| any key in filter focus | Types into the filter; Backspace deletes; Enter or Esc returns to list |
| Up/`k`, Down/`j` (list or inspector); `d` / `u` (inspector) | Move selection; scroll the inspector 3 lines |
| Enter (row selected); Esc (inspector) | Open the inspector; back to list |
| `/`; `h` | Filter (substring over eight cells); toggle historical (`released` or `retained`) rows |
| `e`; `m` | Export plain record to the state dir and show `exported <path>`; set the "changed since" baseline |
| `n` / `p`; Esc | Next / previous question (oldest first) and clear selection; only with link on and a question line present |

*Width layouts* (terminal.py:21-24, 82-89; below 80 columns "terminal too narrow (min 80)", below 8 rows "terminal too small (min 8 rows)", each with counts and the gap notice).

| Class | Ledger columns | Questions panel | Decision Desk |
|-------|----------------|-----------------|---------------|
| full (>=160, `--width 160`) | marker, dispatchId (<=48), run, workerState, status, nextAction.kind, alive, evidence age | layouts A, B, C tried in order | question pane over list on the left, evidence pane 80 wide on the right |
| line (116-159) | marker, kind, dispatchId, alive, status, age | A, B, C tried in order | question pane spans the width; evidence left, list 46 wide right |
| short (80-115) | marker, kind, dispatchId, alive, status, age | C only | three panes stacked |

Layout A = count strip + list + RETAIN CONTEXT pane, B drops RETAIN, C drops the strip; the first that shows at least 3 question rows wins. Questions win over the ledger on a short terminal. When the list is cut the oldest questions stay and the newer are reachable only by export (owner decision 2026-11-12, as the docstring records).

*Decision Desk (R3).* Built only with `--questions` and the link on (`DeskView`, `_desk` view.py:888-948). It needs a selected question; the join is exact: the question's verified payload `dispatch_id` against a collected row's `dispatchId`. Linked fields: dispatch, state, status, outcome, next action, liveness, evidence age, `resource.worktreeId` shown as "this session only". Unlinked: "affected scope unknown" plus the reason. If it does not fit, `decision desk hidden: terminal too short` goes in the list frame. No desk key acts on a question. Question text from the payload is screen-only (cut at 400 characters, at most 4 desk lines); it is never in the JSON snapshot and not in the record's question lines (the record keeps ids, ages and subject).

*Gates.* `QUESTION_GATE_PASSED = True` (commands.py:67, cites `.dev/issues/409/owner-pass-record-20261112.md`) and `QUESTION_LINK_PASSED = True` (:70, cites release-gates.md `QUESTION-LINK`) [CODE-VERIFIED on 61ac2c2e6]. `_questions_on` = option and gate 1; `_link_on` = questions on and gate 2. Tests pin both as True only with a cited, existing record (tests/observe/test_commands.py:754-779); the snapshot export omits `.dev/`, so those two tests read origin/master-only files (G-07). The gate records live in `.dev/issues/409/` on origin/master only. Provenance differs (doc): QUESTION-OBSERVATION has an owner-written record (accepts Q-1 FAIL: reads only from the terminal that holds the Run; non-owner non-consumption unverified; burst loss over 100 rows accepted); QUESTION-LINK is an agent-written status line recording the owner's chat "yes" of 2026-11-17 (release-gates.md:58); the on-screen-only text decision is also a recorded chat decision (PR #598). The record names Run `run_93bfa00cae2b`; the code accepts any valid `--run` (G-08). Whether the "four sample kinds" data-gate rule (release-gates.md:5) was met for messages is [UNVERIFIED] (U-06).

*Release stage* (release-gates.md is doc; "State" is checked against code).

State at origin/master 61ac2c2e6: R0 (`--fixture` replay of 10 synthetic variants) built, `--questions` with `--fixture` refused (D-1 below); R1 (live worker ledger, `--once`, snapshot) built (PR #503), DIRECTION-SELECTED passed 2026-11-16; R2 (`--questions`, one named Run) built, live read enabled by PR #577; R3 (question text, link, Decision Desk) built 2026-11-17 behind QUESTION-LINK (PR #592); R4 and later (remote fleet `--include-remote`, closure evidence, history past 100 rows, admission, verification, cost, deep links, write-back) not built, "Not established" in the gate table, write-back "never R1".

Closure shows `unavailable (no source)`. What the docs lack: one section in `cli-groups.md` and two README lines; no CHANGELOG entry in [Unreleased], 6.1.0 or 6.0.0; no technical doc (the post-release report counts "13 source files"; Glob finds 14 `.py`, 13 without `fixtures/__init__.py`); no sysop guide (deferred, decision 6.6). Which tag first contained R2 and R3 is [UNVERIFIED] (U-08). `cli-groups.md:42` and the HELP say "no option maps to an Orca call"; `--run` and `--questions` do select which read argv is built (commands.py builds none) [CODE-CONTRADICTED, minor, CC-01].

*The six PRs* (all MERGED; state read with `gh pr view <n> --repo IronbellyOrg/IronClaude`; merge commits are ancestors of origin/master [CODE-VERIFIED via git]): #503 release 1 plus the design package (2026-11-11; `gh` file list truncated at 100, 545 files per G-10); #514 release 2, questions for one named Run, live read off (2026-11-12; `QUESTION_GATE_PASSED = False` at that merge, retention bounded at 1,000); #577 enable the live questions read, owner pass record (2026-11-17; 684 observe tests passed per body); #592 question text, dispatch link, Decision Desk behind QUESTION-LINK (2026-11-17; 762 observe tests per body); #598 record that question text stays on screen only (2026-11-17, docs only); #673 visual parity at 160, 116 and 80 columns, refs #606 (2026-11-19; 2,831 files per G-10; #606 was closed separately on 2026-11-20T00:20:54Z).

*C8 reachability.* Live R2 (`--questions`), R3 (link, Decision Desk), the snapshot and `--once` are wired from the click option through `Options` -> `_questions_on`/`_link_on` -> `Collector` -> `LiveSource.read_questions` (commands.py:173-180, 247-253, 388-395, 487-496; collector.py:205-245). The "no DEFECT-CANDIDATE" lines in R01 and R02 cover only these paths (GF1 section 4).
- **KNOWN LIMIT (cited) D-1 (C8-9):** `--questions --fixture` exits 2 (commands.py:77-78, 183-188, 414) and `FixtureSource.read_questions` always returns FAILED `no-question-fixture` (collector.py:125-129); cited decision: row R1 of the ponytail debate cut list (`.dev/issues/409/ponytail-review-20261116/cuts-debate/final-cut-list.md:24`, origin/master), applied by PR #577; a debate output, not an owner ruling; remediation task not created (read-only brief); flagged for the owner (14.5).

**Public Interface** (key signatures only):
- `observe_group(ctx, once, width, ascii_mode, fixture, run_id, snapshot, questions)`; `Options` (frozen, seven fields); `execute(options, deps=None) -> int`; `run_loop(collector, keys, screen, clock, *, make_policy, directory, snapshot_file, write_snapshots) -> int`.
- `build_view(result, session, clock) -> View` (the only `View` constructor); `apply_cycle(session, result, clock) -> Session`; `apply_key(session, key, view, clock) -> tuple[Session, Effect]` (`Effect` = NONE, EXPORT, QUIT); `render(view, policy, message=None) -> Group`; `screen_lines(view, policy, message=None) -> list[str]`; `KeySource(fd=None)`.

**Dependencies:** 5.1 `Collector` and `export` (data and files); `click` and `rich` (`Live`, `Console`; `Console` is built only in terminal.py); `termios` and `tty` (POSIX, imported lazily on the interactive path only; `--once` works with them blocked, test_commands.py:73-100).

**Consumers:** a person at a terminal (`superclaude observe [flags]`); `tests/observe` (pure view and render, click and loop with fakes, real pty in `test_live_screen_pty.py` and `test_keys_spike.py`); `main.py:590-592` registers it (test_registration.py:59-71).

**Conventions & Patterns:**
- A new panel: typed frozen dataclass, a builder returning None when off, a defaulted `View` field set by keyword in `build_view`, a literal in view.py (GF4 3.2). New data needs a new `CycleResult` field first.
- A new non-text key needs a name in `KEY_NAMES` (view.py:30), a `Key(...)` built in `keys.py` (`_take`, `_take_escape`) and a branch in `apply_key`; keys must only change the Session.
- Keep the question text out of the record and snapshot; a link-off screen must stay byte-identical to the reference capture (PR #592).
- R02's "41 entries" and "29 tests" are superseded by 36 entries, 26 `test_*.py` files, 27 tests in `test_session.py`; `test_keys_spike.py:3` ("only module with a real pty") predates `test_live_screen_pty.py` (SD-05).

---

### 5.3 Sweep Classifier and Joins

**Purpose:** Turn each Orca Dispatch row and each un-joined session transcript into one `SessionRow` with exactly one of 8 classes, using 9 ordered pure rules, then qualify it with join, transcript and source evidence. It never recommends an action; "could not determine" is the default for anything it cannot prove.

**Key Files:**

| File | Purpose |
|------|---------|
| `src/superclaude/cli/sweep/classify.py` (1009 lines) | `RULES` (345-355), `classify` (369), `classify_all` (880), joins (`_join_path_b` 609, `_guard` 728, `_person_origin` 760), `_contract_for` (570; docstring :575), `safe_to_close` (479), `removable` (455), `package_state` (423) |
| `src/superclaude/cli/sweep/models.py` (278) | `CLASSES` (50-59), `PACKAGE_STATES` (62-69), `SAFE_VALUES` (71), `OrcaObservation`, `SessionRow`, `Classification` (212) |
| `tests/sweep/test_classify.py` (1978) | In-memory builders `orca()`, `contract()`, `row()` (143-169); `RULE_NAMES` pin (378-379) |
| `tests/sweep/test_cli_contract.py`, `test_probes_allowlist.py` | The only readers of captured fixtures (rule 5 proof) |
| `tests/sweep/fixtures/` (21 entries) | 20 `captured-*.json` plus `SOURCES.md`; 5 exited workers captured 2026-11-11, `captured-worker-show-running.json` 2026-11-16 |

**How It Works:**

```
SweepInput -> classify_all: merge rows sharing a Dispatch id -> join each transcript (path A, else path B)
  -> _guard flags -> one SessionRow per Orca row + one per un-joined transcript (person_started via _person_origin)
  -> classify(row, ctx): RULES 1..9, first match wins -> note harvest -> unreadable transcript forces unknown
  -> classify_all: join/source flags force unknown -> lifecycle/health/result/freshness, counts, waiting_a/b
```

Terms: settled = `orca.outcome` in succeeded/partial/failed; STOP code = `E-...` token in contract `reason` plus `blocked_question`; Ruling halt = `E-HALT-QA` or `E-NO-RULING`; freeze code = any STOP code except `E-RESUME-NEEDED`.

| # | Rule | Class (kind) | Exact firing condition | Proving test | Fixture |
|---|------|--------------|------------------------|--------------|---------|
| 1 | `blocked_contract` | waiting on a person (a) | contract `blocked` and transcript not unreadable; then no Orca row needs a Ruling halt; Orca row settled, or `gate_policy == "report blocked"`, or Ruling halt matches; else declines (note "may be re-running" if live and policy is ask/None) | `test_classify.py:288-295, 728-760`; `test_cli_contract.py:1085-1115` | inline |
| 2 | `orca_exit_proof` | stalled (proved) | Orca row, `liveness_verdict == "exited"`, transcript not unreadable, `worker_done_seen is False`, `fenced_evidence == "absent"` | `:296-307, 581-624, 763-777` | inline only |
| 3 | `fenced` | fenced | Orca row and `fenced_evidence == "present"` | `:308`; `test_report.py:353` | inline only |
| 4 | `waiting_signal` | waiting (a) or (b) | (a) Orca `agent_wait` not None; (b) contract `failed` with a freeze code; (b) Orca `status == "ready"` Task row | `:309-319, 382-417, 476-485` | inline; `captured-task-list-ready.json` is an empty list |
| 5 | `working` | working | Orca row, `liveness_verdict == "live"`, `outcome == "in_progress"`, `agent_wait_present is True`, `agent_wait is None`; `dispatch.status` not tested | `:320, 444-485`; `test_cli_contract.py:1133-1169`; `test_probes_allowlist.py:1639-1651` | `captured-worker-show-running.json` (positive), `captured-worker-show-1.json` (exited, negative) |
| 6 | `finished` | finished | `orca.body_text` first line starts `guard refused:`, or Orca settled and a parsed contract with settled `worker_status`; note "partial: usable not yet judged" | `:321-328, 627-654, 785-806` | inline |
| 7 | `idle` | idle | `person_started True`, no Orca row, transcript readable, `last_activity <= now` and `< window_start` | `:329-337, 493-540, 957-968` | inline |
| 8 | `person_active` | person session (active) | `person_started True`, transcript readable, `last_activity >= window_start` (no check on Orca row or `<= now`) | `:338-346, 1734-1756` | inline |
| 9 | `fallback` | could not determine | always; evidence "no rule 1 to 8 matched (...)"; note "no contract read for this row" for a settled row without a contract | `:347, 581-654, 672-673` | inline |

Only rule 5 has a captured-fixture proof; the 5 captured tab-map files are read by no test (path-B tests use synthetic `entry()` objects). Rules 1 and 2 are called a second time by `classify` (378) only to harvest decline notes.

Which classes print on live data: `waiting on a person` (rules 1, 4) for contract and Task data, rule 4(a) needing a non-null `agentWait` that was never captured; `working` (rule 5) since the 2026-11-16 capture; `finished` (rule 6) only when a contract was found for the row; `idle` (rule 7) and `person session (active)` (rule 8) rarely, since both need `person_started True` (below), idle rows counted as `historical` (`visible = total - historical`); `could not determine` (rule 9 plus forcing) is the common outcome. `stalled (proved)` (rule 2) and `fenced` (rule 3) have no producer and never print.

**Could-not-determine forcing** (`_force_unknown`, 358-366; replaces the matched class, keeps its evidence): (B) `transcript_readable is False`, any rule; (C) a non-empty `forced` tuple from `classify_all`: path-A several-rows, path-B notes, duplicate Dispatch ids that disagree (`_merge_group` 512-525), or an `unscanned` source named `contract <dispatch>` or `transcript <path>` or containing "inconsistent"; (D) rule 9. The notes cell is the only place the three meanings (nothing proved, input unreadable, join ambiguous) differ. A transcript over 256 KiB joined by path B forces unknown ("session start not observable: transcript tail only", `test_classify.py:1405-1412`); a terminal Dispatch row without `completedAt` has no window (`:1385-1391`).

**Joins** (`classify_all` 880-1009):

| Step | Fact |
|------|------|
| Path A | `session_join == transcript session id`; one row joins, several rows give a forcing note. Tried first and independent of `JOIN_PATH`. Production `session_join` is `dispatch.assigneeHandle` (`term_<uuid>` captured); a production path-A join is UNVERIFIED |
| Path B (`JOIN_PATH = "B"`, 40) | tab-map keys (`file_name`, `terminal_handle`) of entries with the transcript's session id; needs a Dispatch window (`_window` 548-558), a transcript read from byte 0, and exactly one row whose window holds the first record (bounds inclusive) |
| `JOIN_PATH` | read in one place, `_guard` (745) |
| `_guard` | excludes `ready` Task rows; flags `origin` (5 list-incomplete notes), `unobservable`, `no_join`, `unmatched` and `earlier_pane` (path B: any considered row exists) |
| `person_started` (`_person_origin`) | True only if no origin note, no guard flag and no tab-map entry. Under path B, True needs a sweep with no non-ready Dispatch rows, a readable tab map and a complete worker list; with any Dispatch row present every un-joined transcript is None and prints could not determine. No live row of idle or person-active was found (UNVERIFIED) |
| `_contract_for` (570-591) | a contract attaches to an Orca row only if a report folder (`--report-dir/--output-dir/--output`) or a path named in the Task text identifies exactly one contract, or it is the only contract under the only row using that worktree; else None (so no rule 1, no finished, no frozen) |

**Safe to close, Removable, package states:**

| Item | Rule (all in `classify.py`) | Values it can print |
|------|-----------------------------|---------------------|
| `safe_to_close` (479-504) | terminal: no Orca row or unobserved gives could not determine; `retained` gives no; `reclaimable` + `release` gives could not determine ("result read not observable"); other gives no. Worktree part is `removable()` | no or could not determine; no branch returns `yes` |
| `removable` (455-476) | first of: uncommitted, unpushed or no upstream, `.dev/tasks` unsaved, frozen plan, a package in unfinished/archive-blocked/interrupted-archive/conflict, shared active package; then unreadable worktree; else could not determine ("report read, open PR and unmerged commits not observable") | no or could not determine; never `yes` |
| `package_state` (423-429) | `conflict` (id in to-do and done), `interrupted-archive` (marker), `archive-blocked` (to-do with `FINAL:` line), `unfinished` (to-do, no `FINAL:`), `archived` (done), `unknown`; first four block removal | proofs `test_classify.py:1770-1817`; shared packages `:1833-1871` |

**Phase 1 limits (KNOWN LIMIT (cited) per R-C8; declaring lines, cited text and residual owner facts for each are in 14.5, C8-1 to C8-5).** `stalled (proved)` and `fenced` cannot fire: `worker_done_seen` and `fenced_evidence` default to `None` and `"unreadable"` (`models.py:108-109`), are read in `classify.py`, are set by constructor arguments in tests only, and `parse_worker_show` (`probes.py:471-515`) never sets them (live exited rows get the note "Orca: exited; fenced evidence not readable"). `agent_wait_since` is never set (`models.py:111-112`, `probes.py:481`; pinned `is None`, `test_probes_allowlist.py:1651, 1687`), so a waiting row from `agentWait` alone has unknown age. `Safe to close` and `Removable` never print `yes` (no branch returns it); only the report footnote, CHANGELOG:171 and commands.md:621 say "never yes", while `commands/sweep.md:16` and `SKILL.md:66` do not. Remediation task not created (read-only brief); flagged for the owner.

**Public Interface:**

```python
classify(row: SessionRow, ctx: SweepContext) -> Classification          # classify.py:369
classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult          # classify.py:880
Rule(name: str, match: Callable[[SessionRow, SweepContext], Classification | None])   # RULES: 9 entries
_classification(class_name, rule, evidence, waiting_kind=None, notes=()) -> Classification  # :130 (private)
safe_to_close(row, worktree: WorktreeState | None) -> SafeToClose; removable(worktree) -> tuple[str, str]
```

**Dependencies:** `probes.collect` output (`SweepInput`: Orca rows, contracts, transcript tails, tab map, worktrees, source rows); `SweepContext` (`now`, `window`, `window_start`), the only time source, so rules do no file, process or clock access; `models.py` frozen dataclasses (`CLASSES`, `SessionRow`, `Classification`, `PackageRecord`).

**Consumers:** `commands.py:269-271` (`probes.collect` then `classify_all`); `report.py` (sections chosen by `waiting_kind`, `CLASSES[5]` idle and `CLASSES[7]` unknown; `NEXT_INSPECTION` keyed by rule name).

**Conventions & Patterns:**

- Rules are pure and first-match-wins (12.2); missing proof never becomes False or "absent" (SPEC:232): set `worker_done_seen` or `fenced_evidence` only from a named live source; a new class touches the places in 13.1 A.
- A `finished` row never says admitted or accepted (`test_classify.py:791-800`).
- Prove a rule with a captured fixture and a `SOURCES.md` entry; in-memory builders alone prove only the code path.

---

### 5.4 Sweep Read Side, Safety, Publish and the WC-16 Binding

**Purpose:** Collect read-only facts (Orca, git, disk), render one dated Markdown report plus a JSON v1 object, publish the report atomically under `.dev/sweeps/`, and bind a coordinator (by contract text only) to run it. Every failed read is reported as `unscanned`, never as clean.

**Key Files:**

| File | Purpose |
|------|---------|
| `src/superclaude/cli/sweep/probes.py` (1477 lines) | The only module that starts a subprocess: `ALLOWED_ORCA` (49-60), `ALLOWED_GIT` (68-81), `_orca` (266), `_git` (315), `Budget` (124), `collect` (1322) |
| `src/superclaude/cli/sweep/commands.py` (288) | `sweep run`, `_check_output` (99), `_publish` (153), exit codes |
| `src/superclaude/cli/sweep/report.py` (695) | `render` (608), `to_json` (613), `sanitize` (569), `SECTIONS` (545-558) |
| `src/superclaude/cli/main.py:581-583`, `cli/sweep/__init__.py` | Registration `sweep`; lazy import of `sweep_group` |
| `commands/sweep.md`, `skills/sc-sweep-protocol/SKILL.md`, `output-styles/pragmatic.md:22-25` | Command, skill (steps 1-4) and chat-summary exception |
| `core/WORKER-CONTRACT.md:20, 23, 46, 110, 287-289`, `core/HOW-WE-WORK.md:298, 359`, `.gitignore:255-256` | WC-16 and its routing and ignore rule |
| Tests | `test_probes_allowlist.py` (2397; 100 tests), `test_readonly.py` (536), `test_git_config_hole.py` (276; 10, real git), `test_cli_contract.py` (1534; 61), `test_cli_registration.py` (69; 3), `test_report.py` (1465; 43), `tests/commands/test_sweep_command.py` (637; 28 functions, prose pins only) |

**How It Works:** the flow (bind Run, collect, classify, render, publish, JSON on stdout) is drawn in 4.1 (b); the coordinator chain is in the WC-16 table below.

Orca allowlist (10 templates, 7 verbs; `check_orca_argv` needs a token-for-token match, `<run>` = `run_[0-9a-f]{12}`, `<dispatch>` = `ctx_[0-9a-f]{12}`, `--include-remote` rejected in any position, refusal before any process starts). Binary: `$ORCA_CLI_COMMAND` if set (not validated) else `orca-ide`, never bare `orca`; only the arguments are allowlisted.

The ten templates and their call sites (6 called, 4 pinned and not called) are listed in 8.1 (`probes.py:49-60`); the four uncalled ones are pinned by a zero-argv test (`test_probes_allowlist.py:624-638`). Result kinds: `ok`, `no_binding`, `unavailable` (timeout, binary missing, `runtime_unavailable`), `call_failed` (over 8 MiB, non-zero exit, invalid reply). After `unavailable` every later Orca read becomes an `unscanned` source row; the sweep still exits 0 (only a failed binding without `--run` exits 2).

Git: four exact argv shapes (`status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all`, `config --show-origin --list -z`, `ls-files -z`, `check-attr --stdin -z filter`). The seam always prepends `git --no-optional-locks -C <cwd> -c core.fsmonitor=false` and sets `GIT_OPTIONAL_LOCKS=0`. "4 fixed calls per worktree" is a maximum: `config` runs first; with no filter driver having a non-empty `clean` or `process` command, `status` runs after 2 calls. Filter holes (issue 547): when a tracked path selects such a driver, `status` is not run and the source row is `unscanned: git filter could run a program`. Real-git tests plant a marker-writing command and assert it never runs, with a positive control: routes 1 (shared `core.fsmonitor`), 4 (`include.path`), 5 (per-worktree config), 6 and 6b (`GIT_CONFIG_*` env), 2 and 3 (filter `clean`, `process`), 8 and 9 (submodule config). Route 7 was not found (UNVERIFIED); routes 8 and 9 pass because of `--ignore-submodules=all`, not the pre-check; a defined-but-unselected driver is still read.

Disk reads (sources in 4.2): packages (`.dev/tasks/{to-do,done}`, `progress.md` `FINAL:` line, `.archiving` marker) must stay inside the worktree and over 1 MiB only the last 512 KiB is searched; contracts (`yaml.safe_load`) are candidates named by Task text or report folders inside an observed worktree, 1 MiB; transcripts `~/.claude/projects/<key>/*.jsonl` (key = worktree path with non-alphanumerics replaced by `-`), last 256 KiB; a missing ccsession tab-map folder is readable and empty; the Orca version file is a fixed Linux path (elsewhere the lock line prints UNVERIFIED); remote hosts are never read (coverage fixed `unknown`).

Budgets: 50 shows (shared evenly across Runs), 90 s total, 10 s per call, 8 MiB output, 1 MiB contract and ledger, 256 KiB transcript tail, worker-list page 100. The sweep reads one `worker-list` page per Run and never pages (probes.py:1150, 1157-1161); a raw row count of 100 or more (`WORKER_LIST_PAGE`, probes.py:89) or `page.hasMore` true sets `truncated`, which prints the `PAGE_LINE` banner "[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]" (report.py:32, 209-210), adds a "could not determine" bullet (report.py:528-531) and the note `origin unknown: worker list truncated` (classify.py:72, 701-702), which keeps a transcript-only row's `person_started` unknown instead of True (classify.py:764-777). The four byte limits are marked "proposed (DESIGN 17 open item 19)"; a recorded decision for 50/90/10 is UNVERIFIED. Stable-read check re-reads once if (size, mtime) changed, then `conflict: inconsistent observation`.

Publish and exit codes: stem `YYYYMMDD-HHMMSS-sweep` (UTC); `_check_output` requires the folder inside `<root>/.dev/sweeps` (symlinked base fails) and not overlapping `.dev/tasks`, `~/.claude/projects` or the tab-map folder. Temp `.<stem>.<pid>.tmp` (`O_EXCL`, fsync), commit point `os.link` to `<stem>.md`, `-2` to `-99` (never overwrites), then unlink. JSON is printed after publication; a print failure leaves one complete report.

Exit codes: 0 report published and one JSON object on stdout; 1 publish error or any other exception (`[sweep <stage>] <sanitized message>`, an allowlist `ValueError` included); 2 usage or binding error (no Run bound, Orca unavailable while binding).

JSON v1 (12 top-level keys, all always present): `schema_version`, `observed_at`, `collected`, `scope`, `window`, `orca_available`, `sources`, `rows`, `worktrees`, `waiting`, `summary` (counts for every class, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`), `report_path` (the one unsanitized string). Shapes (report.py:619-695): `collected` {`start`, `end`}; `scope` {`runs`, `root`, `worktrees` (a count)}; `sources[]` {`name`, `coverage`, `age_seconds`, `unscanned` (null or text)}; `rows[]` {`row_id`, `class`, `waiting_kind`, `rule`, `evidence`, `notes[]`, `policy`, `person_started`, `safe_to_close` {`terminal`, `worktree`, `reason`}}; `worktrees[]` {`path`, `status_read`, `uncommitted`, `unpushed`, `dev_tasks_unsaved`, `frozen`, `packages[]` {`id`, `location`, `state`}, `shared_package_ids[]`, `removable`, `removable_reason`}; `waiting` {`a[]`, `b[]`} (text lines); text values sanitized but never cut. `orca_binary`, `orca_version`, the ten dimensions and Next inspection are Markdown only.

Report sections (`SECTIONS`, 12, joined by blank lines; header and footer have no `##`): header (READ ONLY line, scope, `Messages coverage: partial`, lock-risk line); Source coverage; Waiting on a person (a); Waiting on a person (b) with Ready Tasks "creator not observable in Phase 1"; Could not determine; Retained problems; Sessions (10 dimension columns, `SP24_LINE`, `SAFE_TO_CLOSE_LINE`); Worktrees; Historical sessions; Shift Brief; What I could not determine; footer ending "Report complete".

Sanitizer (`sanitize`, `report.py:569-599`): see the 2.5 sanitizer row; `cell` cuts to 200 characters and an empty cell prints `none`.

Command and skill: `commands/sweep.md` has `allowed-tools: Skill`, no worker mode and no `## Unattended mode`, and says "Nothing starts it automatically" (:22). The skill runs `superclaude sweep run` (PATH first; `uv run --frozen --no-sync` only on "command not found"; Bash timeout 120000), Reads the report in chunks of at most 150 lines to `Report complete`, then prints counts and the path; exit 1 or 2 prints stderr and ends. Chat exempt reply: the final successful reply may skip the DONE / NEXT table only if there is an explicit top-level coordinator assignment (system/developer or direct person instruction, in force), the loaded skill is executing a real `/sc:sweep`, exit 0, stdout parsed, report Read; workers, subagents, failures and quoted text stay ordinary. `SKILL.md:51` calls it "a rule the loaded text states, not a runtime detector"; 37 shared clauses plus 15 skill-only pins are tested as text.

**WC-16 binding:**

| Element | Text (location) | What code does |
|---------|-----------------|----------------|
| WC-16 | `WORKER-CONTRACT.md:287-289`: on every coordinator wake or wait timeout, at most once every 5 minutes, run "The sweep." unchanged and in the same pass `/sc:sweep`, read its report before acting; an added read, not a second pass, no heartbeat update, no `worktree ps --agent-wait`, not an L1 probe; "Phase 1 adds this duty, not a scheduler" | No caller exists: hop 1 is prose for an LLM session; hops 2-4 (command, skill, `main.py` registration) are intact |
| "The sweep." | `:110`: one `worker-list`, one `worktree ps --agent-wait`, one `stat` per contract path, heartbeat records updated | Sweep issues its own `worker-list`, never calls `worktree ps --agent-wait`, reads `agentWait` from `worker-show`, allowlists no message verb; heartbeats, deadlines and the L0-L5 ladder stay the coordinator's |
| WC-10 stall proofs | `:46, :157`; WC-16: "only Orca's stall proofs make a worker stalled" | Only rule 2, with no producer for two inputs; the transcript proof "final turn sent no `worker_done`" has no reader (transcript tail keeps timestamps and session id); fallback is could not determine |
| Never-as-worker | `:23` lists `/sc:sweep`; brief guard case 3 (`:20`); `commands/sweep.md:18, 42, 70` | Pinned in `tests/skills/test_worker_contract.py` and `test_sweep_command.py:155-159` |
| HOW-WE-WORK; cadence; never posted | rows 298 ("Coordinator or person only, never a worker") and 359 (every wake, at most once per 5 min); `commands/closeout.md:99`; WC-16, `.gitignore:255-256` | Row required by `tests/core/test_how_we_work_routing_table.py:33`; no throttle in `cli/sweep` (grep found none), only the sentence is pinned (`test_worker_contract.py:212-215`); no send or post verb, `NEXT_INSPECTION` names a read only (`test_report.py:1439-1459`) |

**Public Interface:**

```python
sweep run [--run RUN]... [--window 6h] [--root PATH] [--output PATH]          # commands.py:220-241; window <N>h|<N>d, max 720h
collect(ctx: SweepContext, runs: tuple[str, ...], root: Path, budget: Budget) -> SweepInput   # probes.py:1322
Budget(shows=50, total_s=90.0, per_call_s=10.0, clock=time.monotonic); bind_run(budget) -> str
check_orca_argv(args) / check_git_args(args) -> None   # raise ValueError
render(result: SweepResult, ctx: SweepContext) -> str; to_json(result, ctx, report_path: str) -> dict
_publish(text: str, output_dir: Path, now: datetime) -> Path                    # private, only writer
```

**Dependencies:** `orca-ide` or `$ORCA_CLI_COMMAND` (subprocess; 6 read templates; the `runtime_unavailable` shape was never induced, design item 9); `git` (subprocess; 4 exact argv shapes, lock-free); Claude project transcripts, the ccsession tab map and `.dev/tasks` (file reads, bounded as above); `yaml` (contract parsing) and `click` (CLI group).

**Consumers:** a coordinator or person via `/sc:sweep` (runs the skill and Reads the report; WC-16 asks for it, no code enforces it); tests in four pinning layers (allowlist shapes plus an `ast` scan of `probes.py` for write verbs, recorded-argv full sweeps, a before/after file-snapshot diff, real-git hole tests).

**Conventions & Patterns:**

- Add an Orca or git call only by extending `ALLOWED_ORCA` or `ALLOWED_GIT` and the pinned tests (13.1 B); map every failure to an `unscanned` source row or None, never to an empty or clean value; write only through `_publish`, inside `<root>/.dev/sweeps`.
- Pass every string into a report or JSON through `sanitize` (`cell` in tables); `report_path` is the one raw string, by design.
- A new report section is a function added to `SECTIONS`; a breaking JSON change bumps `JSON_SCHEMA_VERSION` (the bump policy is UNVERIFIED).
- Design section 17 (23 open items, no status column) is a historical list; item statuses stay UNVERIFIED unless code shows closure.
- Keep UNVERIFIED items marked: non-null `agentWait` meaning, source for stall and fence proofs, route 7, Budget decision, orchestrator binding.

---

### 5.5 Agent-work-report pipeline and the living report

**Purpose:** The `agent-work-report` skill builds one daily report of Clay's open work (both Ironbelly GitHub orgs, Projects boards, ClickUp, Orca agent sessions) with 16 scripts, a model-written judgement layer and a checked delivery gate. Since PR C (#684, merged 2026-11-20T02:01:07Z, d7d645ddd) it also keeps a "living report" page from per-issue entry files that an orchestrator is designed to write. The reader side is built; the writer is not (built-versus-designed table below).

**Key Files** (under `src/superclaude/skills/agent-work-report/`; scripts total 5,777 lines, 5,971 with SKILL.md; research 05's "6,321" is wrong, M-8):

| File | Purpose |
|---|---|
| `SKILL.md` (194 L) | the behavioural spec: 15 steps (76-95), statuses (140), gate (152), boundaries (192-194) |
| `scripts/run.py` (887) | run lock, gate, summary, close, abandon, log, refresh, status |
| `scripts/common.py` (507) | state paths, `repo_root()`, `run_cmd`, entry-file reader and contract comment (133-151), fixed vocabularies |
| `scripts/collect.py`, `clickup.py`, `sessions.py`; `exclude.py`, `match.py`, `classify.py`, `compare.py`; `activity.py`, `render.py`, `check.py` | GitHub, ClickUp, Orca-terminal-and-transcript collectors; steps 4b to 7 (leave out held issues, join, group, diff against the previous run); steps 8, 9, 11 (evidence file, writing sheet, seven script checks) |
| `scripts/page.py`, `waker.py`, `orca_term.py`, `prefs.py` | page, server and Orca tab; coordinator wake; Orca terminal verbs; priority and answer log |
| `config.json` (14 keys), `templates/` (7 files) | M-14 key list (`person`, `orgs`, `timezone`, `session_tag`, `automation_prefix`, ...); `qa-report-template.md` is unreferenced and stale |
| `tests/skills/test_agent_work_report.py` (4,005 L, 142 `def test_`) | fakes patch `gh_json`, `run_cmd` and the ClickUp `call`; no live call; results not run (UNVERIFIED) |

**How It Works:**

```
gh (2 orgs) ------> collect.py \
ClickUp GET ------> clickup.py  >-> exclude.py -> match -> classify -> compare -> activity -> render
Orca + transcripts > sessions.py/     ^ orchestrated/*.json (no writer in the snapshot)
model writes overview.md -> check.py --links -> page.py + summary -> run.py gate -> ClickUp DM / Orca tab -> run.py close
```

Pipeline and run-folder artifacts (state `<orchestrator repo>/.dev/coordinator/`, run folder `runs/<%Y%m%dT%H%M%SZ-kind>/`; step numbers and commands match the script usage lines, **[CODE-VERIFIED]**):

| Step | Script | Reads -> writes |
|---|---|---|
| 1 | `run.py open daily` or `on-demand` | lock, `wakes/` -> `run.json` (run, kind, started, previous_completed_run, stuck_run_replaced), `run-log.md`, `wake-records.json`, `automation-runs.json`, `incomplete-runs.json`, `run.lock` |
| 2 | `collect.py` | config orgs -> `github-items.json`, `coverage.json` (repos, boards, source_errors) |
| 3 | `clickup.py` | token, previous run -> `clickup-items/events/gone/status/replies.json`, `settings.json`; model logs DM answers with `prefs.py answer` |
| 4 | `sessions.py` | hook file, transcripts, /proc -> `sessions.json`, `sessions-status.json` |
| 4b | `exclude.py` | `orchestrated/*.json`, `coverage.json` -> `excluded.json`, rewritten items and sessions, two `*-before-exclude.json` copies |
| 5-7 | `match.py`, `classify.py`, `compare.py` | -> `items.json`, `merged-into.json`; `classified.json`; `snapshot.json`, `compare.json` (new, changed, closed, unchanged, carried) |
| 8-9 | `activity.py`, `render.py` | -> `activity.md` (others' text only as `> ` quoted lines); `overview.md` stub, `to-write.json` |
| 10 | model edits `overview.md` | never calls GitHub, ClickUp or Orca (SKILL.md:10) |
| 11 | `check.py --links` | -> `script-checks.md` (table plus `overview sha256: <hex>`); exit 1 on any FAIL |
| 12 | `page.py`; `run.py summary`, `gate`, `refresh --run` | -> `report.html`, `notes.json`, shared `.dev/coordinator/report.html`, `summary.md` |
| 13 | `page.py --open`; model posts `summary.md`; `clickup.py dm`; `run.py log ... delivered` | -> `clickup-dm.json` (sent, detail), `action-log.jsonl` |
| 14 | `run.py close`; model runs `git add .dev/coordinator && git commit` | -> `complete.json`; never push; no script runs `git commit` |
| 15 | `prefs.py priority` or `answer` | -> `priorities.json`, `action-log.jsonl`. Not in SKILL.md's table: `abandoned.json` (`run.py abandon`), state-folder `refresh.lock` |

Six statuses (SKILL.md:140; `common.SESSION_STATUSES`; Orca's own session state is never read, SKILL.md:38). Thresholds appear only in SKILL.md:140; no script computes them; `check.py` enforces only the form `status: <one of six>: <reason>` and the "Needs you" two-way match:

| Status | SKILL.md definition | Inputs the model sees (`activity.md`) |
|---|---|---|
| working | running, active in last 15 min | `Claude running`, N events since previous report, last activity |
| progressed | worked since previous report, now at rest | event count, last 3 prompts, last reply |
| waiting on you | last turn asks Clay, or a tool call waited over 15 min | quoted last reply, "stopped on a <tool> call with no result since <time>"; `ends_on_question` and `pending_tool_call` live in `sessions.json` |
| stuck | same error or step repeating | last 2 errors; `repeated_steps`, `error_count` are in `sessions.json` only, never printed |
| stalled | nothing since previous report, or Claude gone | event count 0; script rule `render.carried_status` for unchanged items |
| done | it reports the work finished | quoted last reply; session kept in `sessions.json` until a report called it done |

Who writes a status: the model for sessions on new or changed items; the script for unchanged items (`carried_status`); the entry file's `session_status` map for a held issue (nobody writes it today). Groups: assigned, owned, opened, inprogress, candidate, other (a session on no item is `inprogress`). Priority: `priorities.json`, then board priority, then `config.json` labels, then the person's own text, else Unset; order by level (Urgent, High, Medium, Low) then state.

**Lock, gate, carry-forward.** `run.lock` is `{run, kind, started}`; a lock younger than `time_budget_minutes` (daily 120, hourly 10) writes `wakes/*-skipped.json` and exits 3; an older one is kept as `stuck` and replaced. Delivery gate (`run.py:204-368`): seven checks PASS (placeholders, template, sessions, carry-forward, needs-you, candidates, links) plus the sha256 chain: `check.py` writes `overview sha256` into `script-checks.md`, `page.py` writes `<meta name="overview-sha256">` into `report.html`, `summary.md` must equal `build_summary` byte for byte, and `gate` recomputes all three. `clickup.py dm` enforces the whole gate and sends only `<run>/summary.md`; `run.py close` enforces only checks plus sha, so SKILL.md:183 is **[CODE-CONTRADICTED]** in part. Carry-forward invariants: every previous-snapshot item is listed, closed, counted quiet or in `excluded.json` (`check.py`); `compare.py` closes an item only on evidence (`gh ... view`; HTTP 404/410 means "no longer visible"; any other error carries it); items of a repo or org that failed to read, and sources not read, are carried unchanged.

**Data sources and exact commands** (all list-argument `run_cmd`, no shell, bare `orca` and `gh`; no `--repo IronbellyOrg/IronClaude` because both orgs are read; no SuperClaude-Org target):

- GitHub (read only): `gh repo list <org> --limit 1000`; `gh issue list` and `gh pr list --repo <o>/<r> --state open --limit 1000 --json ...`; `gh project list --owner <org>`; `gh project item-list <n> --owner <org>`; `gh search issues --owner <org> --involves <person> --state open [--include-prs]` (collect); `gh api --paginate --slurp repos/<o>/<r>/issues/<n>/timeline`, `gh pr view <url> --json mergeable,isDraft,reviewDecision,statusCheckRollup` (activity); `gh issue or pr view <url> --json state,closedAt` (compare); `--json number` (check); `gh issue view <n> --repo <r> --json state,stateReason,assignees` (run).
- ClickUp (read; one write): `urllib` GETs to `api.clickup.com` (`/v2/user`, `/v2/team`, tasks, comments, v3 chat); POST only in `send_dm` (`.../channels/direct_message`, `.../channels/{cid}/messages`); `CLICKUP_API_TOKEN` required, never the connector.
- Local (read): hook file `~/.config/orca/agent-hooks/last-status.json` (version 2), `~/.claude/projects/*/*.jsonl`, `/proc/<pid>/environ` (`ORCA_TERMINAL_HANDLE`, `CLAUDE_TOPIC`), `git -C <path> remote get-url origin`; terminal join fields `tabId`, `leafId`, `handle`, `worktreePath`, `connected`, `lastOutputAt` (sessions.py:323-330).

What it WRITES outside run and state folders (**[CODE-VERIFIED]**): (1) a ClickUp DM to the token owner's own DM channel (`clickup.py dm` after the gate; `waker.notify`); (2) an Orca unread mark and comment on the orchestrator repo workspace (`waker.notify` fallback); (3) text typed into the coordinator's Orca terminal (`/clear`, `Wake (daily report): run /agent-work-report for today's report.`, `ccsession coordinator`) and a new terminal; (4) an Orca browser tab at `http://127.0.0.1:8765/report.html`; (5) a detached `python -m http.server 8765 --bind 127.0.0.1 --directory <.dev/coordinator>`, which serves the whole folder (`settings.json` with ClickUp user and DM channel ids, `action-log.jsonl`, run folders); (6) a git commit in the orchestrator repo, by the model at Step 14. The page loads Google Fonts and makes no other outside request.

**Living report.** Entry-file contract (common.py:133-151), path `.dev/coordinator/orchestrated/<owner>__<repo>__<N>.json` (`closed/`, `info/<kind>__<key>.json`):

| Fields | Read by | Written today by |
|---|---|---|
| `url`, `title`, `priority`, `assignees`, `human_assignee`, `author`, `orchestrator{}`, `worker{}`, `pr_url`, `last_update`, `session_status`, written parts (`state`, `next`, `what`, `state_text`, `done`, `todo`, `happened`, `recommend`, `needs`, `how`), `suggested`, `priority_why` | `exclude.py`, `run.py refresh`, `render.entry(filed=)`, `common.entry_session_ids` | nobody in the snapshot; designed writer `superclaude orchestrator report-entry` (PR B); tests build entries by hand |
| `closed_at`, `close_reason` | `run.py` | this skill: `move_to_closed` (run.py:483), the only entry-file writer in the snapshot |
| `kind`, `group`, `follow_up_state` | no code | nobody (`follow_up_state` only in a test fixture and the design header) |

- `exclude.py`: a candidate is an issue assigned to the person in a repo read without error; it removes the issue url, the entry's `pr_url` and each `orca://session/<id>`; keeps unreduced copies so a rerun is identical; `closed/` and `info/` exclude nothing; no external command. With no entry files it excludes nothing.
- `run.py refresh` (7 stages: lock check, reconcile via `gh issue view`, prune by `info_ttl_days` 14, read base overview, drop held blocks, add entry blocks, build the page with `page.main`): exclusive flock on `refresh.lock`; without `--run` it does nothing while a daily run holds the lock; rewrites only the shared `report.html`; fake-tested, no live run recorded.
- `waker.py morning`, `hourly`, `check-missed`: finds the `coordinator` session by process environment, types `/clear` and the wake line, retries 15 x 120 s (morning only), counts SENT only when a run folder appears; failure becomes `DM_NEEDED` and `notify`; `hourly` is a recorded skip.
- `orca_term.py`: `send` is the only terminal-writing function (waker only); `typing_or_fresh` marks a terminal unsafe if it holds draft text or output under 60 s old.

**Built versus designed** (61ac2c2e6; sources research 05 s29, GF1 3.7, GF3 s7 and s8):

| Capability | Status |
|---|---|
| Skill, 15 steps, run lock, sha gate, carry-forward; `exclude.py`, `run.py refresh`, `render.entry(filed=)`, `waker.py` | built (PR #684), fake-tested |
| Design #681, plan-gate retirement #682, `/sc:closeout` #683 | merged |
| `superclaude orchestrator report-entry`, `src/superclaude/cli/orchestrator/`, `/sc:orchestrator`, `sc-orchestrator-protocol` | designed (PR B); absent; no PR. `cli/main.py` has no `orchestrat` match; closeout's `settle.sh:1037-1042` prints `ENTRY escalated key=<k> why=surface_absent` |
| Poll wakes the orchestrator and `orchestrator_repo` key (PR A #686); `/sc:issue --plan` (PR P #690) | open, unmerged; master `_TOP_KEYS` rejects `orchestrator_repo` (cycle.py:216-220) |
| Orca automations `coordinator-morning-wake`, `coordinator-missed-check`, `orchestrator-poll`; orchestrator repo `IronOrchestrator`; spec `SPEC-AGENT-WORK-COORDINATOR-20261027.md` | outside the repo: **[UNVERIFIED]** (triggers of `waker.py` included) |
| Daily report phased out for the living report (owner ruling 1) | designed; code still runs the daily pipeline |

**Public Interface:**

```
run.py open <daily|hourly|on-demand> | gate|summary|close <run> | abandon <run> <reason> | log <run> <action> <item|-> <reason> | refresh [--run <run>] | status   # exit 3 = run active
collect|clickup|sessions|exclude|match|classify|compare|activity|render.py <run>;  check.py <run> [--links];  page.py <run>;  page.py --open;  clickup.py dm <run> <message_file>
prefs.py priority <run> <item url> <Urgent|High|Medium|Low|clear>;  prefs.py answer <run> <url|-> <session|clickup-dm>;  waker.py morning|hourly|check-missed
common.repo_root() -> Path   # $AWR_ROOT, else orchestrator_repo in ~/.config/superclaude/issue-watch.json (dir must hold repos.yaml)
```

**Dependencies:** `gh`, bare `orca` and ClickUp REST (collection, terminals, tabs, DM); the Orca hook file, Claude transcripts and `/proc`, plus `ccsession` and system `python3` (session facts, wake typing, page server); `<orchestrator repo>/.dev/coordinator/` via `$AWR_ROOT` or `orchestrator_repo` (all run state; the repo is outside this checkout).

**Consumers:** Clay (page at 127.0.0.1:8765, ClickUp DM of `summary.md`, Orca unread mark); `sc-closeout-protocol` `settle.sh` `cmd_entry` (calls the absent `report-entry` verb; ends `surface_absent`); Orca automations outside the repo and the `coordinator` session (start `waker.py`, run `/agent-work-report`); the designed orchestrator (would write entry files and call `run.py refresh`; no code in the snapshot does either).

**Conventions & Patterns:**

- Run subprocesses only through `common.run_cmd` (12.1); the model writes only judgement parts and never calls GitHub, ClickUp or Orca; others' text enters as `> ` quoted lines. Deliver only after `run.py gate` PASS, send the ClickUp DM only from `<run>/summary.md`, commit `.dev/coordinator` in the orchestrator repo and never push.
- A new session status needs `SESSION_STATUSES` and `check.STATUS_OK` edits; links must be `http(s)://` or `orca://`; symlinked entry files and folders are refused.
- An entry writer must use the `WRITTEN` slot names plus `session_status`, `pr_url`, `orchestrator`, `priority_why`, `suggested`. Treat SKILL.md:14, 172, 183 as corrected above; design DQ13 "Watching" is **[CODE-CONTRADICTED]** (code: "Other work in progress").

---

### 5.6 Orca dashboard design package (issue 409) and its relationship to the observer

**Purpose:** The #409 package is "a design collaboration branch, not a production integration" (README.md:9): 20 synthetic terminal-dashboard designs (two sets of ten) with a Python/Pillow prototype renderer, drawn only from a synthetic fixture schema that is explicitly not an Orca API. The shipped observer (`superclaude observe`, Python and Rich) implements three of the designs in reduced form and shares no code or fixture data with the package. Provenance: package root (checkout) `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/` on docs branch `docs/409-orca-dashboard-designs`, commit 495eb96d1, which is not an ancestor of origin/master and has no PR; the same 406 files are on origin/master through PR #503 (merge 9e2608b03, 2026-11-11T19:54:57Z; REST list 545 files, `gh pr view` truncates at 100; #673 lists 2,831). `.dev/research/orca-dashboard-20261105/` is **LOCAL-ONLY, untracked** (0 files in HEAD and origin/master); it is the origin of the R-rules and is cited below only as local-only.

**Key Files** (package paths relative to the package root; counts re-made in research 06 s1: 406 files, 20 designs, 18 scenarios plus base, 360 exports, 2 galleries, 2 PDFs, fixture sha256 `1f17a907...bd42e4`):

| File | Purpose |
|---|---|
| `README.md`, `DESIGN-CONTRACT.md`, `concepts.md`, `data-dictionary.md`, `integration-gaps.md` (28 L), `sources.json`, `QA.md` | self-description, contract (navigation only), provisional picks, schema, six "not established" items, E01-E13 evidence, QA verdict |
| `render.py` (130), `fixtures.py` (122), `canvas.py` (122), `layouts/group_a.py`, `group_b.py`, `agent_focus.py`, `requirements.txt` (Pillow==13.0.0, wcwidth==0.9.4) | renderer, fixture builder, Canvas, layouts: set 1 (signal-bridge, fleet-quilt, time-loom, worktree-atlas, decision-desk, proof-gate, budget-engine, relay-map, delta-deck, watchkeeper), set 2 (leverage-board, attention-ledger, handoff-switchboard, loop-detector, collision-lens, outcome-ledger, revision-drift, mission-pulse, owner-load, shift-brief) |
| `tests/test_designs.py` (19 tests), `tests/test_gallery.cjs` | unittest on fixtures, sanitizing, layouts; Node DOM stub (no browser); count verified, pass result **[UNVERIFIED]** |
| `.dev/issues/409/` (origin/master; checkout copy) | `owner-decisions-20261108.md`, `owner-direction-record-20261116.md`, `bmad/spec-orca-observer/*` (`release-gates.md`, `unverified-register.md`, `rendering-rules.md`), `visual-parity/REDESIGN-SPEC.md` |

**How It Works:**

```
render.py [--batch 1|2] [--show SLUG] [--width N]     # --width only with --show; export mode renders 160, 116, 80
 -> exports(batch) -> write_fixtures(ROOT)            # fixture.json + scenarios/ (9 variants + 9 scale); both batches rewrite ROOT
 -> designs(batch) -> screen(spec, fixture, width) -> Canvas -> layout fn (c, f, metrics(f))
 -> six files per design and width (.txt .ascii.txt .ansi .svg .png .mono.png) -> contact-sheet.png, portfolio.pdf (160-wide PNGs)
 -> manifest.json (+ fixture sha256) -> gallery.html (19 scenarios x 10 designs x 3 widths, pre-rendered, no fetch)
```

- `--batch 2` swaps only the layout module (`layouts/agent_focus.py`) and the output folder (`agent-focus/`). README commands (README.md:24-28) are documented, not run; the DejaVu font path is read at import and not checked; README.md:44 is **[UNVERIFIED]**. No defect candidate in the pipeline; facts: `--width` is ignored in export mode; `test_export_manifest` skips `.mono.png`, contact sheet, gallery and hash.
- Fixture schema (proposed, not Orca; `data-dictionary.md:3`, `sources.json` E13): top-level keys `synthetic, as_of, variant, sources, orchestrators, sessions, worktrees, requests, edges, events, scope, previous`; five fake sources `demo:*`. A session has no PR, issue, url or session-open field (`fixtures.py:30-43`). Real Orca fields are the 31 worker-list keys the observer parses (`parse.py:58-90`) plus the question message row; `projection.attention`, `parent`, `resource`, `id` are present but redacted and unparsed (meaning **[UNVERIFIED]**); admission, revision, cost, timeline, edges and events have no verified Orca counterpart.
- Name parity: all 9 variant names plus base appear verbatim as observer fixtures (`parse.py:750-761`); content parity 0 of 10 (`cmp` differs; observer keys are `variant, description, cycles`). Package-only: 9 `scale-*`; observer-only: 8 `golden-*`, `question-cap-100` (19 files). Code reuse is banned on record (`ARCHITECTURE-SPINE.md:172`, `SPEC.md:76`, `sanitize.py:3-4`); `rendering-rules.md:3` ("the package's synthetic fixtures") is **[STALE DOC]**. Eight palette colors match exactly (`theme.py:59-69` and `canvas.py:7`).

In the observer: Signal Bridge partly (view A: worker ledger, counts and freshness strips; no owner or SIGNALS bars; `view.py:48`, `REDESIGN-SPEC.md:75-76`); Attention Ledger partly (view B: `COORDINATOR QUESTIONS` for one named Run; `view.py:54,69-84`, `REDESIGN-SPEC.md:78,82`); Decision Desk partly (view C, minimal: one question, one linked session; `view.py:97-112,888-948`); the other 17 not at all (0 name hits), PR #673 (refs #606; #606 was closed separately on 2026-11-20T00:20:54Z) targets exactly three (`REDESIGN-SPEC.md:9`).

Rules S1-S11 (package) and R1-R11 (local-only research) are a scope-discovery grouping, not numbers in any source file. Rule texts, one line each:

**S1-S11** (package paths relative to the package root): S1 a worker result is not admission; lifecycle settlement, report status, acceptance, current tests and human approval are independent, and admission comes only from an explicit record (README.md:39; data-dictionary.md:17-28; DESIGN-CONTRACT.md:11). S2 dirty is not dangerous, stale is not failed, overlap is not conflict, an inspectable evidence packet is not admitted, a partial cost subtotal is not total spend, tokens are not progress (README.md:40; DESIGN-CONTRACT.md:11; `fixtures.py:47` `"conflict": "not established"`). S3 unknown stays unknown: null cost is not zero, a timeline gap is a missing observation, not idle (data-dictionary.md:34, 40, 50). S4 evidence counts as current only when its `check_revision` equals the current revision (data-dictionary.md:28; DESIGN-CONTRACT.md:11). S5 affected counts are set unions, not sums; no one-to-one session and worktree assumption; historical sessions counted apart (data-dictionary.md:39, 46; README.md:37). S6 filtered and global counts are always labelled and the overview stays global (README.md:32; data-dictionary.md:46; integration-gaps.md:24). S7 source loss does not resolve questions, fail sessions, unlock a policy freeze or authorise retries (integration-gaps.md:24; data-dictionary.md:27). S8 navigation only: no approve, dispatch, retry or merge action, not even greyed; the header always prints scope and freshness; limited lists show omission counts (DESIGN-CONTRACT.md:11). S9 imported text is inert: ESC, CSI, OSC, C0/C1, CR and bidi controls removed before any renderer, width in display cells, NO_COLOR and strict-ASCII exports (PLAN.md:38, 66-67; README.md:31). S10 widths 160, 116 and 80 are composed separately, 80 as selected detail (PLAN.md:57); hold/pause freezes the display only, queues changes and discloses skipped observations on resume (README.md:32). S11 the data model is a proposed schema, never Orca API fields (DESIGN-CONTRACT.md:11; `sources.json` E13).

**R1-R11** (LOCAL-ONLY, untracked: `.dev/research/orca-dashboard-20261105/snapshot-brainstorm/merged-requirements.md` = MR, and `.../interactive-brainstorm/adversarial/merged-visual-design.md` = MV): R1 a decision stays listed until explicit resolution ("a reply, read flag, snooze or vanished message is not resolution"); enqueued, delivered, processed, answered and resolved are separate facts (MR DEC-6 :77, COM-2 :86). R2 while the message read is capped with no paging, counts print `>=N observed` and the frame says `OLDEST observed` (MR DEC-3, DEC-4 :74-75). R3 no fleet-wide all-clear; a partial or failed source gives `0 observed (partial)`, never `none`; unknown `?` is never summed or zero (MR COV-3 to COV-5 :105-107). R4 reads are non-consuming; a source that would consume is `unavailable (would consume)` (MR COM-5 :89; FG-8). R5 only an explicit routine form is a heartbeat; anything unmatched is `unclassified` and shown in the decision block (MR COM-4, COM-7 :88, 91). R6 deltas compare only to the last successful comparable observation; a failed or partial read never gives a zero baseline (MR CHG-1, CHG-2 :92-93). R7 completion, terminal existence, process liveness and independent verification are four separate fields (MR VER-1 to VER-4 :98-101). R8 run, task and attempt identities stay apart from host, workspace and session; superseded attempts never override the current one (MR BLK-6 :84). R9 source text is untrusted: quoted, truncated, controls escaped, secrets redacted and marked (MR COM-6 :90). R10 interactive rules: selection held by identity, pause freezes rendering only ("PAUSED, N queued"), urgency double-encoded (glyph and colour), reported-done shown as "self-reported", exact ids only in selected detail, oldest asks pinned with `+N more`, overlapping views labelled "overlap, not a sum" (MV :16-24). R11 feasibility gates FG-1 to FG-14 are the open source-contract checklist (MR :1104-1119).

Status in the shipped observer (research 06 s5; where 06's takeaways group S1, S2, S4 loosely as "by absence", its rule table is the stronger evidence):

| Status | Rules |
|---|---|
| ENFORCED | S3, S6, S7, S8 (`commands.py` builds no argv; allow-list in `adapter.py`), S9 (own sanitizer), S11 (labelling), R3 (other wording), R4 (non-consuming reads, `adapter.py:34-50`) |
| BY ABSENCE | S1 (`unavailable (no source)`, `view.py:134`), S2 (no git or overlap data) |
| PARTLY | S5, S10, R1, R2, R6, R7, R8, R9, R10 |
| NOT BUILT | S4 (scope on record: `release-gates.md:17`, `unverified-register.md:69-71`); hold/pause (S10, package-only); R5 (`--types question` instead); superseded attempts (R8); secret redaction (R9) |
| FG-1..14 (R11) | open: 1-7, 10, 12; FG-8 closed for the owner's own Run, **[UNVERIFIED]** for non-owners; 9 avoided; 11 n/a; 13, 14 partly |

`integration-gaps.md` items now: 1 enumeration beyond 100 rows partly closed (owner's own Run, still capped at 100); 2 joins across hosts partly closed for one Run on one host (QUESTION-LINK); 3 admission, revision and human owner, 4 cost telemetry, 5 durable replay (source-loss handling built, S7) and 6 deep links (no click-to-open) open.

Contradictions between the issue-409 body, the package and the code (stale body lines 19, 36, 27, 28, 204; "unmerged, no PR"; Bubble Tea versus Python and Rich; reply, ack and resolve versus navigation only; 405 versus 406 files; "No direction chosen") are settled in 14.4 A (SD-21 to SD-29) and 14.3.

**QA verdict and direction.** `QA.md:19`: "FAIL for the inspected pre-correction snapshots" (4 blocking findings); corrections were made with "No new independent post-correction verdict" (`QA.md:29`); Playwright check failed (Chrome absent). The package chose no design (`concepts.md:43-49` picks are "not user approval"). The live body says "No direction chosen" (stale); `owner-decisions-20261108.md:5-9` and `owner-direction-record-20261116.md:2-5` record a staged order (worker list, questions, third screen later), mapped by `release-gates.md:3,10` to Signal Bridge, Attention Ledger, Decision Desk (DIRECTION-SELECTED passed 2026-11-16); the owner's record names an order, not designs, and no package-ranked pick was adopted. Parity gate: PASS on the text and ANSI tier (PNG route failed).

**Overlaps (facts).** Reviewer asks of 2026-11-11 (issue links, PR links, plain-English summary, session-open link, step flow; issue comment, 14:47:52Z): live body line 98 says none is built; no observer or package row has a link. The report skill has counterparts, assembled here from 05 and 06 (neither states the mapping): GitHub urls and `linked_issue`/`linked_pr`, `orca://session/<id>` links, model-written "What it is" and "Current state"; no step-flow field (nearest: "Done with evidence", "Still to do"). Sweep layout and dimensions: `orchestrator-mode.md:609` "The layout is SPEC section 9 ... copied from #409 at `495eb96d`"; `sweep/models.py:162-164` "The #409 dimensions, nine fields ... dimension 9 'policy' ... report-only, never JSON keys" (06 cites fragments; wording re-read). "Observer reads the sweep JSON" is an undecided proposal only (body lines 82, 110-112, 204; alignment items 1-10 undecided; no code or design); JSON v1 lacks dimensions, links and step flow.

Orchestrator design overlap (mentions, about 30 Orca verb forms, the five status vocabularies): see 2.5, 8.1, 8.2 and 12.2. PR chain: merged #539, #503, #514, #577, #592, #598, #673, #681-#684; open #686, #690; PR B none.

**Public Interface:**

```
render.py [--batch {1,2}] [--show SLUG] [--width N]    # defaults 1, 116; NO_COLOR present disables ANSI
fixtures.fixture(owners=8, count=80, variant="base"); metrics(f, owner=None); write_fixtures(root)
render.designs(batch=1); render.screen(spec, f, width, ascii_mode=False) -> Canvas   # layout fn (c, f, m)
```

**Dependencies:** Pillow==13.0.0, wcwidth==0.9.4, DejaVu Sans Mono (hard-coded path), Node (gallery test), `uv` (README command).

**Consumers:** the observer spec (names, intent, palette, no code); `orchestrator-mode.md:609` (layout pin at `495eb96d`); reviewers (gallery, PDFs). Nothing imports the package.

**Conventions & Patterns:**

- Cite `.dev/research/orca-dashboard-20261105/` only as local-only and untracked; never as repo evidence. Cite package files by checkout path and code by origin/master path.
- Write "20 designs, 3 partly implemented"; never say the package fixture schema feeds the observer, or that the owner picked a package design.
- Keep UNVERIFIED: package test results, `sources.json` E01-E04 against the installed Orca, non-owner non-consumption, `projection.attention` meaning, FR-9 mapping.
- Apply R-C8 to any "required but unwired" capability: a cited decision gives KNOWN LIMIT, none gives DEFECT-CANDIDATE.

---

## 6. State Management

N/A as a client-side store: observer, sweep and agent-work-report (AWR) are CLI and file based tools and the #409 design package is a static renderer. The runtime state that does exist:

| Tool | State | Held where | Reset / lifetime |
|---|---|---|---|
| Observer | `Session` (focus, selected, filter_text, show_historical, baseline, marked, inspector_scroll, selected_question), changed only by `apply_cycle` / `apply_key` | in memory, frozen dataclass (view.py:151-168) | process life; no persisted "last look" (rendering-rules.md:97) |
| Observer | `CycleResult`: one immutable result per cycle, replaced under a lock (collector.py:155-184); states NOT_POLLED, NOT_AVAILABLE, OK, FAILED, PARTIAL | in memory | identified rows kept across cycles (`reobserved=False`), no cap on them; anonymous rows replaced on a complete cycle (parse.py:723-728; G-04); questions bounded at 1,000 (questions.py:21); both reset on restart |
| Sweep | none between runs; one report file is the only artifact (commands.py:153-208) | disk, `.dev/sweeps/` | by hand (SP-22: the person deletes old reports; design 1:35) |
| AWR | `<state>/run.lock` `{run, kind, started}`, run folder, previous run's `snapshot.json`, `action-log.jsonl`, `priorities.json` | `.dev/coordinator/` of the orchestrator repo | lock older than budget is kept as `stuck` and replaced (run.py:95-131) |

Observer state transitions ([CODE-VERIFIED] collector.py:252-321, view.py:456-463) are in 5.1 (Limits, Collector, STALE) and 10.1. Cross-store dependencies: none inside a tool; the only shared name is `snapshot.json` (observer state dir versus AWR run folder).

---

## 7. Component Inventory

N/A: these tools have no component tree. The subsystem tables in Section 5 are the inventory.

---

## 8. API & Integration Points

### 8.1 Orca verb inventory (every Orca call across the tools)

Binary per tool: observer = discovered binary (`_find_orca`: candidates `orca-ide` then `orca` via `shutil.which`, accepted only on exit 0 and a topic named `orca-cli` in `skills list --json`; install_user_setup.py:36, 247-270); sweep = `orca-ide` or unvalidated `$ORCA_CLI_COMMAND`, "never bare orca" (probes.py:43, 214-216); AWR = bare `orca` from PATH (run_cmd list args, research 05 section 27); design package = no Orca call (fixtures.py:1). Allowlists: observer 3 argv shapes plus 13 forbidden prefixes (adapter.py:29-50); sweep 10 templates, 7 verbs, `--include-remote` forbidden (probes.py:49-62); AWR has no allowlist.

| Tool | Binary | Verb and argv template (after binary) | Purpose | Status | Source |
|---|---|---|---|---|---|
| Observer | discovered | `skills list --json` | discovery, once per `LiveSource` | called (built by `_find_orca`, allowed by exact match) | adapter.py:30, 148-149; install_user_setup.py:258-264 |
| Observer | discovered | `orchestration worker-list --json --limit 100 [--run <id>] [--cursor <c>]` | worker ledger, up to 5 pages | called each cycle | adapter.py:29, 173-183 |
| Observer | discovered | `orchestration check --all --types question --run <id> --json` (8 tokens) | questions of one Run, `--questions` only | called (gate constants True) | adapter.py:32, 186-190, 469-512; commands.py:67, 70 |
| Sweep | orca-ide / env | `orchestration run-current` (plain text, no `--json`) | bind the Run when no `--run` | called | probes.py:50, 399 |
| Sweep | orca-ide / env | `orchestration worker-list --run <run> --json` | worker rows, once per Run | called | probes.py:51, 1150 |
| Sweep | orca-ide / env | `orchestration worker-show --dispatch <ctx_id> --json` | liveness, outcome, `agentWait`, `assigneeHandle` | called, max 50 per sweep | probes.py:52, 1281 |
| Sweep | orca-ide / env | `orchestration task-list --ready --run <run> --json` and `task-list --run <run> --json` | Task rows (ready Tasks, bodies) | called, once per Run each | probes.py:53-54, 1165, 1178 |
| Sweep | orca-ide / env | `worktree ps --json` | worktree paths | called once if Orca still available | probes.py:55, 1335 |
| Sweep | orca-ide / env | `worktree list --json`, `worktree current --json` | none yet | pinned, not called (zero-argv test) | probes.py:56-57; test_probes_allowlist.py:624-638 |
| Sweep | orca-ide / env | `worktree ps --agent-wait [--json]` | prompt-wait listing | pinned (R5, owner 2026-11-08), not called | probes.py:58-59 |
| AWR | bare `orca` | `terminal list [--worktree path:<p>] --json`; `terminal read --terminal <h> --screen --json`; `terminal wait --terminal <h> --for tui-idle --timeout-ms <ms> --json` | find and inspect the coordinator session, session join | called (read) | orca_term.py:24-31, 87-110; sessions.py:291 |
| AWR | bare `orca` | `terminal send --terminal <h> --text <t> [--enter --wait-submit <s>] --json`; `terminal create --worktree path:<ws>` | start and wake the coordinator session | called, WRITE (waker.py only) | orca_term.py:124-133; waker.py:186-189, 297-302 |
| AWR | bare `orca` | `worktree list --json`; `worktree set --worktree path:<repo> --unread --comment <text>` | issue/PR links of a worktree; unread mark as DM fallback | called; first read, second WRITE | sessions.py:309-312; waker.py:88-96 |
| AWR | bare `orca` | `automations list --json`; `automations runs --id <id> --json` | automation run records (names starting `coordinator-`) | called (read) | run.py:160-186 |
| AWR | bare `orca` | `tab list|close|switch|create ...`; `eval --page <id> --expression location.reload()` | open the report page in the Orca browser | called, WRITE (tab) | page.py:354-377 |

Orchestrator design set against these three [DESIGN-ONLY]: the design (`docs/designs/orchestrator.md`, merged by PR #681, "holds no implementation code", DESIGN:3) names about 30 distinct Orca verb forms (GF-3 rows 1-34). The `superclaude orchestrator` package and `sc-orchestrator-protocol` skill are absent from the snapshot. The binary the design would use is not stated in the research. "Match" = token-for-token with an existing allowlist.

| Verb family | Observer (3) | Sweep (10) | AWR | Orchestrator design (DESIGN line) |
|---|---|---|---|---|
| skills | `skills list --json` | none | none | `skills get orchestration [--reference f]` (9, 515, 534, 726) |
| run-current / run-create / run-use / run-show | forbidden (run-use, run-create) | `run-current` without `--json` | none | `run-current --json`, `run-create --objective`, `run-use --id`, `run-show --id` (98, 534, 661, 1262) |
| worker-list | `--json --limit 100 [--run][--cursor]` | `--run <run> --json` | none | `--json` (572), `--run <id> --json` (744), `--run <id> --terminal-state reclaimable --json` (628) |
| worker-show | none | `--dispatch <id> --json` (match) | none | same argv (565, 744, 1278) |
| worker-read / task-list | none | task-list `--run` (match), `--ready --run`; no worker-read | none | `worker-read --dispatch <id> --source transcript --limit <=200` (572, 745); `task-list --run <id> --json` (1304) |
| worker-start, request-show, release/retain, stop/abandon/reset, task-create, gates | none (`dispatch`, `reset` etc. forbidden) | none | none | worker-start (565, 726), `--retry-request` (1279), request-show (567), release/retain (628), task-create (565), gate-create/resolve (572); stop/abandon/reset listed as refused (759, 1117) |
| check / send / reply | `check --all --types question ...` only; `--ack --wait --peek` forbidden | none | none | `check --wait --types worker_done,escalation,question,status --timeout-ms 240000`, `--ack`, `--peek` (572, 748, 1263); `send` (112, 572, 1263); `reply` (572) |
| terminal | none | none | list, read, wait, send, create | list (744), read (573), send incl. `--interrupt` via `escalate` (573, 749), wait (748), close (710, 762) |
| worktree | none | `ps --json` called; `list`, `current`, `ps --agent-wait` pinned | list, set | `show --worktree issue:<N>` (474), `current --json` (565; match with pinned template), `set --unread --comment` (112, 666), `ps` without `--json` (1129), `rm` refused |
| other | none | none | automations, tab, eval | `project setup-clone` (114), `reference add|find` (474, 565), `automations list|show|runs` read-only (348, 762); `ccsession` is not an Orca verb |

Counts: 4 designed argv match a sweep template (worker-show, `worker-list --run`, `task-list --run`, pinned `worktree current --json`); none match an observer template; every write or consuming verb of the design is forbidden in the observer or outside the sweep allowlist (GF-3 section 3). Built today in the same area: `issue_watch` builds a 12-element `orca agent launch` argv (launch.py:95-131); PR A (#686, open) makes the poll wake instead of launch.

### 8.2 Internal Integration Points

| Integration | Direction | Mechanism | Description |
|---|---|---|---|
| WC-16 coordinator binding (sweep) | coordinator to sweep | prose duty, no code | WORKER-CONTRACT.md:287-289: on every wake or wait timeout, at most once per 5 minutes, run "The sweep." (WC:110) and `/sc:sweep`, read the report before acting. Chain: `commands/sweep.md:47` invokes skill `sc:sweep-protocol`, whose steps 1-2 run `superclaude sweep run`, registered at cli/main.py:581-583. No scheduler (sweep.md:22 "Nothing starts it automatically"), no throttle, no check that the report is read [CODE-VERIFIED absence]. The sweep issues its own `worker-list` and never runs `worktree ps --agent-wait`; it reads `agentWait` from `worker-show`, a different source from the coordinator's listing (research 04 s6.1) |
| `.dev/sweeps` consumers | sweep to disk | file | Writer only (commands.py:100-132, 240). No Python module, hook or script reads a published report back; readers are the skill's Read step (SKILL.md:25) and a person or coordinator. Ignored by `.gitignore:255-256` (absent from the stale checkout, SD-14) |
| Observer snapshot consumers | observer to disk | file | None found: nothing in `src/superclaude/{commands,skills,agents,core,hooks}` names the observer or its snapshot; only tests read it (research 02 s5.3; G-09) |
| Observer, sweep and orchestrator design to each other | none | none | no import or reference between observer and sweep (grep, research 06 s8.3; "observer reads the sweep JSON" is an undecided proposal in the live issue 409 body only); the design never mentions `/sc:sweep`, WC-16, observer or `.dev/sweeps` (GF-3 s2), and observer and sweep code never mention the orchestrator, poll or entry files. Whether WC-16 binds a script-started orchestrator is [UNVERIFIED] (U-35) |
| AWR to coordinator run folders | AWR to `.dev/coordinator/runs/<run>/` | files | 15 steps, 16 scripts; gate = 7 checks plus a sha256 chain (`overview.md`, `script-checks.md`, `report.html`, `summary.md`) (run.py:204-368) |
| Living-report entry files | designed writer to AWR | JSON files `.dev/coordinator/orchestrated/<owner>__<repo>__<n>.json` | Reader built: `exclude.py`, `run.py refresh`, `render.entry(filed=)` (merged PR #684). Writer `superclaude orchestrator report-entry` has no code (KNOWN LIMIT sequenced to PR B, no PR open; label flips if the owner says the PR split is not a scope decision, G-35). Only entry-file write in the snapshot: `move_to_closed` (run.py:483). `sc-closeout-protocol` `settle.sh:1037-1042` probes the verb and ends `ENTRY escalated why=surface_absent` |
| `orchestrator_repo` route | AWR reads poll config | `~/.config/superclaude/issue-watch.json` | KNOWN LIMIT sequenced to PR A (#686, open): master poll rejects the key (cycle.py:216-220), so only `$AWR_ROOT` works; CODE-CONTRADICTED tag on SKILL.md:14 stands until PR A merges (CC-02). Who sets the key: [UNVERIFIED] |
| Design package to observer | none in code | names and intent only | "no code, import or vendored file" (ARCHITECTURE-SPINE.md:172); all 10 same-named fixtures differ by `cmp`; palette: all 8 colours equal (theme.py:59-69 vs canvas.py:7); 3 of 20 designs partly implemented (research 06 s4) |

Who writes and reads each artifact, and the file formats written (observer snapshot v1, sweep Markdown and JSON v1, AWR run folder, design-package exports and manifest `{synthetic, as_of, batch, widths, concepts[], fixture_sha256}`), are in 3, 5.1, 5.4, 5.5 and 5.6. `page.py` serves the whole `.dev/coordinator/` folder on 127.0.0.1:8765 (G-22).

### 8.3 External Service Dependencies

| Service | Purpose | Failure Mode | Fallback |
|---|---|---|---|
| Orca CLI | all three tools | observer: no validated Orca gives `NOT_AVAILABLE` and the loop ends; call failures give FAILED or PARTIAL (section 10). Sweep: first-call failure becomes `unavailable`, later Orca reads are skipped as `unscanned`. AWR: `automations` failure writes `{"read": false, ...}`; terminal list truncated means "not read" | observer keeps last good rows; sweep still publishes (exit 0) unless binding fails with no `--run` (exit 2); AWR continues without that source |
| GitHub, orgs `IronbellyOrg` and `IronbellyGroup`, plus Projects | AWR only (`gh repo/issue/pr/project/search`, `gh api timeline`; read-only; no `--repo` flag because both orgs are swept) | per-repo errors go to `coverage.json` / `source_errors`, never fatal; `gh` close lookups: only "HTTP 404/410/Could not resolve" mean closed | items of unread repos are carried, not closed (compare.py:108-118, 166-169). Observer, sweep and design package read no GitHub or ClickUp (grep, research 06 s8.2) |
| ClickUp REST (`https://api.clickup.com/api`) | AWR reads tasks, comments, chat; only write is the self-DM | no `CLICKUP_API_TOKEN` raises `ClickUpError`; GET retried up to 3 times on 5xx; POST never retried; 429 waits up to 65 s; at most 6 attempts | `waker.notify` falls back to an Orca unread mark and comment, then records the failure (waker.py:81-99) |
| Local page server and browser | AWR `page.py`: detached `python -m http.server 8765 --bind 127.0.0.1 --directory .dev/coordinator` | server not answering after about 10 s | none recorded; report template loads Google Fonts when opened (G-23) |

---

## 9. Configuration & Environment

### 9.1 Configuration Files

| File | Purpose | Key Settings |
|---|---|---|
| `src/superclaude/skills/agent-work-report/config.json` | AWR behaviour | 14 keys: person, person_name, orgs, excluded_repos, timezone, daily_run_local, report_days, missed_run_dm_local, time_budget_minutes, session_tag, automation_prefix, clickup_user_id, clickup_email, priority_labels. Values recorded: person `clayphi`, orgs `IronbellyOrg` and `IronbellyGroup`, excluded_repos empty, timezone America/Chicago, daily_run_local 07, missed_run_dm_local 09, time_budget_minutes daily 120 / hourly 10, automation_prefix `coordinator-`; other values not recorded in research. `session_tag` read at waker.py:175, 273, 362; `person_name` at classify.py:35, 62; no read of `clickup_email` or `clickup_user_id` found (a fuller grep is needed before calling them unused; G-48). No `workspace` key (test at test_agent_work_report.py:3005) |
| `~/.config/superclaude/issue-watch.json` | poll config; AWR reads `orchestrator_repo` (absolute path to a repo holding `repos.yaml`) | master poll rejects any key outside `_TOP_KEYS` (cycle.py:58-69, 216-220); PR A branch accepts it. Who writes the file: [UNVERIFIED] |
| `.dev/coordinator/settings.json`, `priorities.json` | AWR state written by `clickup.py` and `prefs.py` | clickup_user_id, clickup_workspaces, clickup_dm_channel; per-item priority overrides (clickup.py:558-563, 610-612; prefs.py:35-47) |
| `.dev/design/orca-observer-20261106/requirements.txt` | package renderer dependencies | `Pillow==13.0.0`, `wcwidth==0.9.4`; font path `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` read at import (render.py:16-18; existence on this host [UNVERIFIED], U-27) |
| `.gitignore:255-256` | keeps sweep reports untracked | `.dev/sweeps/` |

Observer and sweep have no configuration file; they take flags and environment only.

### 9.2 Environment Variables

| Variable | Purpose | Default | Required |
|---|---|---|---|
| `ORCA_CLI_COMMAND` | sweep binary name; value unvalidated (probes.py:214-216) | `orca-ide` | No |
| `XDG_STATE_HOME` | observer state dir `<it>/superclaude/observe` when absolute (export.py:236-244); sweep ccsession tab map `<it or ~/.local/state>/ccsession/orca-tabs` (probes.py:871) | `~/.local/state` | No |
| `NO_COLOR`, `COLORTERM`, `TERM` | observer colour policy: `NO_COLOR` non-empty disables colour; truecolor/24bit, `*256color`, else standard; dumb gives none (terminal.py:92-116). Design `--show` tests only presence of `NO_COLOR` (render.py:129) | unset | No |
| `AWR_ROOT` | AWR orchestrator repo root, else `orchestrator_repo` of the poll config (common.py:28-51) | unset | Yes, unless the poll config key is usable (it is not on master) |
| `AWR_HOOK_FILE`, `AWR_PROJECTS` | AWR overrides for Orca's hook file and `~/.claude/projects` | `~/.config/orca/agent-hooks/last-status.json`, `~/.claude/projects` | No |
| `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` | ClickUp reads and the DM; `ORCA_TERMINAL_HANDLE` and `CLAUDE_TOPIC` are read from `/proc/<pid>/environ` of `claude` processes to map terminals to sessions (orca_term.py:34-58) | unset | token Yes for ClickUp; workspace id No (SKILL.md:37) |
| `GIT_OPTIONAL_LOCKS=0` | set by the sweep in every git child env, with `--no-optional-locks` and `-c core.fsmonitor=false` (probes.py:331-340) | set by code | n/a |

### 9.3 Feature Flags (CLI flags and gate constants)

| Flag | Description | Default | Impact When Toggled |
|---|---|---|---|
| observer `--once`, `--width {160,116,80}`, `--ascii`, `--fixture <name>`, `--snapshot <file>`, `--run <id>`, `--questions` | one click group, seven flags | defaults, exit codes and rules in 5.2 (command surface and exit codes) | `--questions` needs `--run` and a live source (exit 2 otherwise); fixture runs write no snapshot unless `--snapshot` is given |
| `QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED` (commands.py:67, 70) | gates for the question read and the Decision Desk link | both `True` on 61ac2c2e6; tests pin True only with a cited record (test_commands.py:754-779) | False: `--questions` exits 1 with no Orca call, not even discovery |
| sweep `run --run`, `--window`, `--root`, `--output` | Run ids (repeatable); look-back; checkout root; output folder | bound Run (`run-current`); `6h` (`[1-9][0-9]{0,3}[hd]`, max 720h or 30d); folder holding `.git`; `<root>/.dev/sweeps/` | output must stay under `.dev/sweeps` and not overlap input folders (exit 2) |
| sweep gate constants | `JOIN_PATH = "B"` (classify.py:40); `CHECKED_ORCA_VERSION = "1.4.245"` (report.py:23); `JSON_SCHEMA_VERSION = 1` (models.py:18) | as stated | JOIN_PATH only changes the guard cases; version mismatch prints lock risk UNVERIFIED; bump policy not stated in code (U-30) |
| AWR `run.py open daily\|hourly\|on-demand`, `waker.py morning\|hourly\|check-missed`, `check.py --links`, `page.py --open`, `refresh [--run]` | run kinds and modes | n/a | `check.py` without `--links` cannot pass the gate; `hourly` waker mode is a recorded skip (waker.py:216-220) |
| design `render.py --batch {1,2}`, `--show <slug>`, `--width N` | layout set and output folder; print one screen; its width | 1; none; 116 | `--width` ignored in export mode; batch 2 writes `agent-focus/` and rewrites ROOT `fixture.json` and `scenarios/` (render.py:42-43, 127-130) |

---

## 10. Error Handling & Edge Cases

### 10.1 Error Handling Patterns

| Error Category | Handling Pattern | User Experience | Recovery |
|---|---|---|---|
| Observer: `timeout`, `overrun`, `output-cap`, `spawn-error`, `exit:<n>`, `json`, `shape` (adapter.py:196-305, 409-444; parse.py:369-380) | cycle `FAILED` if on page 1, `PARTIAL` after; 10 s per call, 8 MiB (process group killed), 2 KiB stderr kept, stderr sanitized | header shows state and code; last good rows kept; `FAILED` outranks STALE | wait doubles 15, 30, 60 s; any cycle parsing a page resets to 15 s |
| Observer: `cursor-rejected`, `cursor-stalled`, `empty-page` (adapter.py:447-466) | `PARTIAL`, pages kept; `capped=True` at 5 calls | coverage shows PARTIAL or MISMATCH | next cycle |
| Observer: `not-found` (no Orca validated) | `NOT_AVAILABLE`, one result, polling thread ends (collector.py:252-270, 345-351) | "worker-list NOT AVAILABLE (no Orca CLI validated)" | restart observer |
| Observer: `consumer-fenced`, `no-active-terminal` (Orca error envelope, even at exit 0; code names [UNVERIFIED] against a live Orca) | question source `FAILED`; ledger, retained questions and backoff untouched (collector.py:290) | instruction line; read only works from the terminal holding the Run | run from that terminal; a good read recovers |
| Sweep Orca failures | `OrcaResult.kind` ok / no_binding / unavailable / call_failed; timeout, missing binary, `runtime_unavailable`, first-call failure give `unavailable`; over 8 MiB or non-zero exit gives `call_failed` (probes.py:254-312, 369-394) | `unscanned` source rows; "What I could not determine" section; class `could not determine` | exit 0 anyway |
| Sweep git, disk, join failures | every failure maps to `unscanned` or None, never to clean or empty; unreadable transcript, ambiguous join, duplicate Dispatch rows force `could not determine` (probes.py:1021-1048; classify.py:358-366, 908-914) | notes cell names the cause | none by the tool |
| Sweep exits and publish | 0 published and JSON printed; 2 `click.UsageError` or `BindingError`; 1 `_PublishError` or any other exception, `[sweep <stage>] <msg>` (commands.py:279-288); temp file `O_EXCL`, `os.link` never overwrites, own temp removed on failure | stderr only; stdout JSON only on exit 0 | rerun; names to `-99` |
| AWR run lock and gate | open run younger than budget: skip record and `sys.exit(3)`; gate needs 7 PASS rows plus matching sha256 chain, `BLOCKED: <why>` exit 1; `clickup.py dm` re-runs the whole gate and writes `clickup-dm.json {sent:false}` when blocked; `run.py close` re-checks only `passed()` (CC-04) | stderr; no DM | fix the checks; `abandon` releases the lock |
| AWR source failures | each source degrades to `read:false`, `errors` or carried items; waker outcomes SENT / HOLD / DM_NEEDED / SKIPPED, 15 retries for `morning` only | DM to Clay on DM_NEEDED | next automation run |

### 10.2 Known Edge Cases

| Scenario | Current Behavior | Notes |
|---|---|---|
| `check --all` re-lists a handled question | listed as open while Orca returns it; "seen is not resolved" | non-consumption verified for the owner-bound reader only; non-owner read [UNVERIFIED] (U-01); burst over 100 rows may lose questions |
| Transcript tail over 256 KiB joined by path B | row forced to `could not determine` (classify.py:619-628) | five exited workers (2026-11-12 record) all exceeded it; real frequency [UNVERIFIED] (U-12) |
| `os.link` fails (not `FileExistsError`; e.g. unsupported) / 99 names taken | `[sweep publish] cannot link report: <exc>` (commands.py:191-194) / `[sweep publish] report name space exhausted: <dir>` (commands.py:197-201; test_cli_contract.py:1414); both exit 1, no fallback | open item 14 |
| Entry-file reads | symlinked folder or file refused, bad JSON skipped with note, `javascript:` and `data:` URLs dropped | common.py:188-208 |
| Two exports in one second (observer) | same record file name | whole-second timestamp; records never pruned (export.py:247-250) |
| Design package `render.py --show <slug>` | a slug from the other batch raises `KeyError` (the lookup is in `designs(args.batch)`); `--width` is not limited to 160/116/80 (any int is accepted) | `render.py:128-130`; GF-5; code read, not run |

### 10.3 Graceful Degradation

| Failure | Impact | Degraded Experience |
|---|---|---|
| Orca call failing, observer | no new rows | last good rows stay on screen and the source shows FAILED (FAILED outranks STALE); STALE shows only when the last result was OK or PARTIAL and 45 s old; question panel has its own FAILED / STALE state |
| Orca unreachable, sweep | no Orca rows | report still published; counts and "could not determine" from disk and git reads |
| GitHub or ClickUp read fails, AWR | missing items | items carried from the previous run, run-log "Not checked" lines; DM only after the gate |

---

## 11. Performance Characteristics

### 11.1 Performance Profile

Only measured or code-stated values; the research ran no code and measured no tool latency itself.

| Metric | Value | Measurement Method | Notes |
|---|---|---|---|
| Live worker-list sample | 100 rows per page, `total` 428, `hasMore` true; `nextAction.kind` none 86 / release 14; liveness exited 63 / unverifiable 35 / live 2 | recorded golden sample (golden-success.json; test_golden_contract.py:43-58) | no worker-list latency found; `PER_CALL_TIMEOUT` comment still says UNVERIFIED (SD-02) |
| Message read latency and question traffic | about 0.2 s per call; 41 questions over about 66 h, at most 6 in one hour; synthetic steady load 181 sent and 181 retained; burst about 30 of about 415 lost | RESEARCH-REPORT probe; release-gates.md (QUESTION-LINK, QUESTION-OBSERVATION) | recorded results, not re-run or re-tested [UNVERIFIED] (U-05) |
| Sweep full-sweep fixture | 9 Orca argv: 1 worker-list, 2 task-list, 5 worker-show, 1 `worktree ps` | test_probes_allowlist.py:609-619 | argv count only, no timing; tests pin timeouts finishing under 120 s |
| Live sweep outcomes | 180 rows (5 Orca plus 175 transcript) all `could not determine` (2026-11-12 record); issue #590 run: 264 sessions, 263 `could not determine`, 1 waiting; causes named: show cap 50, no contract read | task-package record 2026-11-12; issue #590 | outcome, not duration; recorded, not re-run [UNVERIFIED] |
| AWR run budget | target "about 5 minutes and well under 1M new tokens"; time budget 120 min daily | SKILL.md:10, 97 | a target, not a measurement; no AWR timing recorded |
| Design package | `gallery.html` 15,653,280 B and `agent-focus/gallery.html` 13,952,741 B; 406 files, ZIP 14,438,526 B; 360 export files | `ls -l`, manifest | sizes read from disk; artifacts never regenerated (U-24, U-28) |

### 11.2 Performance-Critical Code (caps, budgets, intervals, timeouts)

| Area | Value | Why It Matters | Location |
|---|---|---|---|
| Observer | poll, call, question and STALE limits are in the 5.1 Limits table; also key read 0.1 s, redraw at least every 0.5 s, warnings 50; spacing is cycle time plus wait (observation) | per observer process; several observers multiply Orca load (HELP); one cycle is bounded at 500 rows (400 with questions) | collector.py:28-34, 345-351; adapter.py:55-63; commands.py:57-60; parse.py:403-405 |
| Sweep budget | 50 worker-shows, 90 s total, 10 s per call; show cap shared across Runs; 4 byte limits marked "proposed" (DESIGN 17 item 19); Budget defaults carry no decision record (U-14) | the #590 reporter names the 50 cap as one of two causes of `could not determine` rows (cause split not measured); issue #534 comments record an owner decision of 2026-11-17 to page past the cap (read to 400 characters per comment) | probes.py:85-89, 127-208 |
| Sweep size limits | output 8 MiB (checked after the child exits, buffered; "shortcut", owner ruling 2026-11-12 D-01); contract and ledger 1 MiB; ledger search last 512 KiB; transcript tail 256 KiB; worker-list page 100; window max 720 h; cell 200 chars; names up to `-99` | memory and read bounds | probes.py:85-89, 270-290; report.py:24; commands.py:29 |
| Sweep git | 2 to 4 calls per worktree; filter pre-check before status; status skipped when a filter driver could run | safety and cost | probes.py:995-1048 |
| AWR timeouts and waits | `run_cmd` 120 s; `orca_term` default 60 s; `gh view` 30 s; git 10 s; `FRESH_OUTPUT_SECONDS` 60; wake retries 15 x 120 s = 30 min; shell wait 30 s; start wait 120 s; run-opened wait 120 s; idle waits 90 s and 30 s; page server wait about 10 s | coordinator wake path | common.py:103-113; orca_term.py:14-21; waker.py:39-42, 203-210, 278-300 |
| AWR collection limits | `gh` lists 1000; 8 repo threads; 6 activity threads; 8 events per item; first session read 24 h and 30 MB; ClickUp 200 task pages, 400 comment calls, 30 active days, 10 min overlap; max 6 attempts | cost of a daily run | collect.py:267-270; activity.py:225; sessions.py:48-49; clickup.py:40-44 |
| Design package | `exports()` writes 10 x 3 x 6 = 180 files per batch; `build_gallery` renders 19 scenarios x 10 designs x 3 widths = 570 frame pairs (1,140 Canvas builds) (derived from code, not run) | gallery size | render.py:41-124 |

### 11.3 Asset Management

Observer fixtures: 19 JSON (10 variants, 8 golden, `question-cap-100`), loaded by name via `--fixture`, size not recorded. Sweep fixtures: 20 `captured-*.json` plus `SOURCES.md`, test only. AWR run folders: one per run under `.dev/coordinator/runs/`, kept; offsets let transcripts be read incrementally. Design package: counts and size in 11.1, offline self-contained gallery.

Extension and test tasks for these sections: see Section 13.

---

## 12. Conventions & Patterns

### 12.1 Code Conventions

| Convention | Description | Evidence |
|---|---|---|
| Read-only by construction, observer | Exactly three Orca argv shapes (`skills list --json`; `orchestration worker-list --json --limit 100 [--run][--cursor]`; one 8-token `orchestration check --all --types question --run <id> --json`). `assert_allowed` runs inside both argv builders. 13 forbidden prefixes (check, --ack, --wait, --retry-request, --peek, dispatch, inbox, run-use, run-create, send, ask, reply, reset); `check` is legal only inside the 8-token shape. No shell; own process group; kill on timeout or overflow. | `observe/adapter.py:29-50, 135-170`; guard tests: forbidden set may grow, not shrink (`tests/observe/test_adapter.py:178-192`); no module except `adapter.py` imports `subprocess` (`tests/observe/test_commands.py:585-601`) |
| Read-only by construction, sweep | `probes.py` is the only module that starts a process. Orca: 10 token-for-token templates (`ALLOWED_ORCA`), `--include-remote` rejected in any position, check runs before any process. Git: 4 fixed shapes, always `--no-optional-locks`, `-c core.fsmonitor=false`, `GIT_OPTIONAL_LOCKS=0`; filter pre-check refuses `git status` when a filter driver with a command applies. Only write: one report file via temp file + `os.link` (never overwrites). | `sweep/probes.py:49-62, 226-244, 331-340`; `commands.py:153-208`; four pin layers: allowlist tests, `ast` scan for write verbs (`test_probes_allowlist.py:475-498`), recorded-argv tests (:609-638), file-snapshot diff (`test_readonly.py:376`); real-git hole tests `test_git_config_hole.py` |
| Not read-only, agent-work-report | All subprocess calls go through `common.run_cmd` (list args, no shell) except the page server `Popen` (`page.py:318`) and `git remote get-url` (`sessions.py:119`). `gh` use is read only. The skill does write: a ClickUp DM, an Orca unread mark, text typed into the coordinator terminal, an Orca browser tab, a detached `http.server`, files under `.dev/coordinator/`; the model makes the Step 14 git commit. The guard is test fakes (`fake_gh` fails any command but `issue view`). | `common.py:103-113`; research 05 s27; `tests/skills/test_agent_work_report.py:2941-2959` |
| Unknown is never zero, never all-clear | Observer: dedicated `UNKNOWN` singleton, never None/0/False/"" (`parse.py:43`); only `export.py` turns it into the string "UNKNOWN"; `observedOpen` is "UNKNOWN", never 0; screen gap notice `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`. Sweep: every failure maps to `unscanned` or None, never to clean; `NO_RECORDS = "No matching records. This is not an all-clear."`; "Missing proof never becomes False" (SPEC:232); unknown-age group when no wait time. | `parse.py:25-43`; `view.py:45-48`; `probes.py:923-934`; `report.py:29`; `test_snapshot_schema.py:501-512` |
| Layering | Observer: adapter -> parse -> collector -> view (pure `build_view`) -> render / export. Collector never decides STALE; `export.py` imports none of render, parse, adapter, collector; `render(view, policy, message)` takes no other input. Sweep: probes (I/O) -> classify (pure; no file, process or clock; time only from `ctx.now` / `ctx.window_start`) -> report (pure; imports `re`, `unicodedata`, `models`) -> commands (publish). AWR: scripts write run-folder files; the model writes only judgement parts; a sha256 chain gates delivery. | `collector.py:1-6, 39`; `export.py:1-7`; `classify.py:3-5`; `report.py:1-7`; `run.py:204-368` |
| Single construction points | `View` is built only in `build_view`; `Classification` only through `_classification`; every observer display literal is a module constant (`view.py:44-134`, "every literal is defined here once"). | `view.py:968-1156`; `classify.py:130-143` |
| Closed, additive-only schemas; gates; recorded fixtures | Observer snapshot: Draft-07, `additionalProperties: false`, `schemaVersion` const 1, remove/rename/retype needs version 2; sweep JSON v1 has every key always present (`JSON_SCHEMA_VERSION = 1`). Gate constants are `True` only with a cited, existing record (5.2). Goldens are redacted recordings; sweep fixtures `captured-*.json` come from dated captures. | `snapshot.schema.json:3-9`; `report.py:613-616`; `models.py:18`; `test_commands.py:754-779`; `test_golden_contract.py:205-213` |

### 12.2 Architectural Patterns

| Pattern | Where Used | Description |
|---|---|---|
| First-match-wins rule table | Sweep `RULES` (9 `Rule(name, match)`) | `match(row, ctx)` returns `Classification` or None (decline). Rule 9 `fallback` always returns, so every row gets one class. Post-steps can force `could not determine` (unreadable transcript, ambiguous join, 256 KiB tail limit). `classify.py:345-386` |
| Strict envelope, lenient rows | Observer `parse_page` | Envelope shape error raises `ShapeError` (cycle FAILED); a bad row is counted and skipped; 31 keys read, other keys counted and dropped; missing value = UNKNOWN. `parse.py:365-407` |
| Panel as typed dataclass plus builder returning None | Observer `QuestionsPanel`, `DeskView` | Typed frozen dataclass, builder returns None when off, defaulted field on `View`, set by keyword in `build_view`. `view.py:253-298, 368-370, 1104-1156` |
| Atomic publish; budgeted reads; hardened local reads | Sweep `_publish`, observer `write_atomic`; sweep `Budget` and observer caps; sweep disk reads, AWR `entry_files` | Publish: sweep temp `O_EXCL`, fsync, `os.link`, unlink (`commands.py:153-208`); observer `mkstemp`, fsync, `os.replace`, 0600 (`export.py:257-274`). Budgets: 5.1 Limits and 5.4. Reads: every sweep read is checked with `_inside` (symlinks resolved); AWR refuses a symlinked entry folder or file, skips unparseable JSON, drops `javascript:`/`data:` urls (`common.py:183-209`). The AWR sha256 chain is in 5.5 (`run.py:204-368`) |

Status vocabularies in use (five over overlapping Orca data; `working` and `stalled` appear in more than one; the sets themselves are in the 2.5 overlaps table). Defined at: observer cycle NOT_POLLED, NOT_AVAILABLE, OK, FAILED, PARTIAL, view STALE (45 s monotonic), snapshot `source.status` OK, STALE, ERROR, UNKNOWN, coverage COMPLETE, PARTIAL, MISMATCH, panel PENDING, OK, STALE, FAILED (`collector.py:44`; `view.py:33-35, 456-463, 664-695`; `parse.py:214-218`); sweep classes plus `SAFE_VALUES` and `PACKAGE_STATES` (`models.py:50-71`); AWR 6 session statuses plus 9 `STATES` and 4 `LEVELS` (`common.py:240-247, 375-399`); FR-9, design only, field-to-state mapping in a spec not in the snapshot [UNVERIFIED] (`docs/designs/orchestrator.md:648, 572`); worker-contract S0-S11 with rungs L0-L5 (`core/WORKER-CONTRACT.md:116-155`).

### 12.3 Anti-Patterns (Things to Avoid)

| Anti-Pattern | Why It's Wrong | Do This Instead |
|---|---|---|
| Standing in None, 0, False or "" for a value the source did not give | Breaks "unknown is never zero"; the schema, tests and counts rely on UNKNOWN | Use UNKNOWN (observer), `unscanned`/None (sweep), unknown-age group; convert only in `export.py` |
| Adding an Orca argv outside the allowlist, or `--ack` / `--wait` / `--peek` to the observer | The observer's non-consuming read is the property the owner accepted on 2026-11-12 (UNVERIFIED for a non-owner reader) | Observer: follow the 5.1 Conventions (template constants, `assert_allowed`, pinned tests); sweep: 13.1 B; never shrink the forbidden set |
| Writing a new snapshot key on every row | Changes the questions-off bytes pinned by `golden_release1_records.json` ("never regenerated") | Conditional key (like `orderUnknown`, `questions`, `collection`) or a reviewed golden change |
| A ninth `CLASSES` entry without extending the unpack | `classify.py:42-51` unpacks eight names; a ninth entry fails at import (from Python semantics, not run) | Edit `CLASSES`, the unpack, `RULES`, `NEXT_INSPECTION` and the test tables together |
| Describing a capability in the present tense while its producer is absent | The documented route fails: `SKILL.md:14-16` (entry files), `CHANGELOG.md:170` (`working` never produced) | State the limit and the deciding line, as the sweep report does with `SP24_LINE` |
| Parsing worker text as markup, or showing it unsanitized | Terminal escape and markup injection | Build `rich.text.Text` from data; sanitize at the parse edge (observer) or `sanitize`/`cell` (sweep) |
| Using `dispatchId` as a question identity | Question identity is `(Run, message.id)`; a dispatch id is never one | Keep `merge_questions` keyed by Run and message id (`parse.py:416-418`) |
| Advice words in `NEXT_INSPECTION` | The report recommends nothing; `BANNED_WORD` forbids stop, retry, release, merge, remov* | Name only what to read (`report.py:54-68`; `test_report.py:1102-1130`) |
| Bare `orca` in the sweep | Sweep default binary is `orca-ide` or `$ORCA_CLI_COMMAND`, "never bare orca" (INV-017); AWR does use bare `orca` (fact, two code paths) | Go through `probes.orca_binary()` |

---

## 13. Extension Guide

Signatures below are from GF-4 (read, not run). Each scenario lists registration points; skeletons are minimal and use only verified signatures.

### 13.1 Common Extension Tasks

| Task | Steps | Files to Touch | Pitfalls |
|---|---|---|---|
| A. Add a sweep class or rule | 1 Add the class string to `CLASSES`; add a 9th name to the unpack. 2 Write the rule and register `Rule(name, fn)` in `RULES` at the precedence position. 3 Add `NEXT_INSPECTION[rule]`. 4 Edit report sections only if the class needs its own section (default: it shows only in the `Sessions` table and `summary.counts`). 5 Update the test tables. | `sweep/models.py:50-59`; `sweep/classify.py:42-51, 345-355`; `sweep/report.py:26-27, 54-68, 545-558`; tests `test_classify.py:277, 351-361, 371-379`, `test_report.py:1091-1127`, `test_cli_contract.py:956, 1032, 1077`; prose `docs/designs/orchestrator-mode.md:474`, `commands/sweep.md:14` | `report.py:26-27` index `CLASSES[5]`, `CLASSES[7]` (shifts if you insert before them). `class_name` not in `CLASSES` raises KeyError at `classify.py:976`. `classify_all` tests the rule names `idle` and `person_active` once, at `classify.py:958` (adds the `last_activity from <source>` suffix); a new rule whose evidence needs that suffix must be added to that tuple. `NEXT_INSPECTION` is keyed by rule name, not class name; a missing key falls back to `_NEXT_DEFAULT`. Rule 2 and rule 3 are the only producers of stalled and fenced; a new class that needs a new Orca field also needs scenario B. Whether a new JSON key needs `JSON_SCHEMA_VERSION` bumped is not stated in code (U-30) |
| B. Add a sweep probe or allowlist entry | 1 Add one token tuple to `ALLOWED_ORCA` (`<run>` and `<dispatch>` are the only placeholders; ids matched with `re.fullmatch`). 2 Add one call site shaped like the existing ones (worker-list at `probes.py:1150`). 3 Add the field to `OrcaObservation` (or `SweepInput`) and set it in `parse_worker_show`. 4 Add a `SourceCoverage` row for every read and failure. 5 Update the allowlist tests. For git: add a shape to `ALLOWED_GIT`. | `sweep/probes.py:49-62, 226-244, 266-312, 369-394, 458-515, 1143-1192, 1322-1396`; `sweep/models.py:83-112, 236-249`; tests `test_probes_allowlist.py:370, 375, 391, 405, 423-462, 475-498, 609-638`, `test_readonly.py:52-72, 448`, `test_git_config_hole.py` | `test_allowed_orca_is_exactly_the_ten_templates` and `..._names_seven_verbs` fail by design; the "10 templates, 7 verbs (NFR-014)" comment (:60) and the full-sweep recording (1 worker-list + 2 task-list + 5 worker-show + 1 `worktree ps` = 9 argv) change. Four pinned templates are tested as "zero argv"; the first call of one changes that test. `parse_worker_show` never raises. Failure maps to unscanned or None, never clean. A new git call must keep `--no-optional-locks`, `core.fsmonitor=false` and the filter pre-check (git config can start programs, issue 547) |
| C. Add a snapshot field | 1 Row field: add to `_FIELDS` and `Row`, populated by `parse_page`. 2 Export: add `("<jsonKey>", "<row_attr>")` to `_TEXT_FIELDS` (dotted key nests) or `_ANY_FIELDS`, or write a conditional key. 3 Top-level value: carry it on `SnapshotMeta`, set it in `_meta`, write it in `snapshot_dict`. 4 Edit `snapshot.schema.json`: add under `definitions.row.properties`; list in `required` only if emitted on every row. 5 Tests. | `observe/parse.py:58-90, 110-157, 365`; `observe/export.py:20, 25-47, 141-216`; `observe/view.py:203-223, 664`; `observe/snapshot.schema.json:106-155`; tests `test_snapshot_schema.py:25, 59-91, 296-326, 404-465`, `test_export.py`, `test_render.py:655-695` | Closed schema rejects an unlisted key. An unconditional row key changes the `snapshot_json` bytes of the five questions-off variants pinned by `golden_release1_records.json`; the conditional route leaves them unchanged. Privacy test lists keys that must never appear (`detail, activity, worktreeId, ownershipState, releaseState, warnings, nextCursor, body, token ...`); `WITHHELD_QUESTION_KEYS` forbids question text. 11 parsed attributes are not exported, with no stated reason for 6 of them (G-05). `counts` values are scalars in the schema but nested JSON to depth 6 in the parser (untested, G-03) |
| D. Add an observer view, panel or key | 1 New data? add a defaulted field to `CycleResult` and set it in `Collector.run_once` (collector.py:248), where the result is built; otherwise it stays at its default. 2 Typed frozen dataclass and a builder returning None when off. 3 Defaulted `View` field, set by keyword in `build_view`. 4 Literals as constants in `view.py`. 5 Place it in `_compose`'s height budget and in each width class. 6 New key: a branch in `apply_key`; a non-text key also needs its name in `KEY_NAMES` and a `Key("<name>")` returned from `KeySource._take` or `_take_escape` (keys.py:176, 217), the only places a `Key` is built (the escape decoder maps only the finals `A` and `B`); add it to the help-line constants `QUESTIONS_KEYS_LINE`, `QUESTIONS_LINK_KEYS_LINE`, `KEYS_LINE` (view.py:91-118) so it shows. 7 Fixture variant if needed. | `observe/collector.py:37-68`; `observe/view.py:30, 44-134, 253-298, 334-378, 968-1156, 1246-1299`; `observe/render.py:480-568, 915-942, 1058-1111, 1258-1446, 1328-1376`; `observe/keys.py`; `observe/theme.py`; fixtures `parse.py:750-761` | Three width classes: full >=160, line 116-159, short 80-115 (below 80 columns or 8 rows only a refusal line prints). Ledger columns differ per class (`_columns`); question panel layouts A/B/C at 160 and 116, C only at 80; Decision Desk side by side, split, stacked. Keys change `Session` only; "no key can reach the adapter or collector" is a test (`test_session.py:359-393`, which also pins `e` as the only export key and `q`/Ctrl-C as the only quit keys), and `test_session.py:339-353` pins `r`, `x`, `Z`, `1` and space as no-ops, so a new key can break both. A new colour role must exist in `theme.py` (registration rule UNVERIFIED, U-33). Help line chosen at `view.py:1139-1141`. A new always-on element changes the surface pinned by `golden_release1_surface.json` |
| E. Add an agent-work-report source | 1 New script `scripts/<name>.py` with `main(run)`: read the run folder, write `<run>/<name>.json`. 2 Subprocess only via `common.run_cmd`. 3 Add the step to the SKILL.md step list and artifact table. 4 Join it in `match.py` / `classify.py`; present it in `render.py` and templates. 5 A new gate check means `REQUIRED_CHECKS` and `check.main`. 6 A new `run.py` subcommand needs an exact-argv-length branch. | `skills/agent-work-report/scripts/{common,run,match,classify,render,check,exclude}.py`; `SKILL.md:56-72, 76-95`; `run.py:204-212, 868-887`; `common.py:103-113, 133-151` | `run.py` has no option parser: any argv shape not matched falls to `sys.exit(__doc__)` (exit 1). `SKILL.md:38`: Orca's own session state is never read. A run without `--links` cannot pass the gate. The artifact table already omits `abandoned.json` and `refresh.lock`. Entry-file readers refuse symlinks. Tests patch `gh_json`, `run_cmd` and the ClickUp `call`; no test runs a real `orca`, `gh` or ClickUp call |
| F. Add a design to the package | 1 Write `render(c, f, m)` in a layout module and add an entry (keys `name`, `question`, `omits`, `tradeoff`, `data`, `missing`, `render`) to that module's `DESIGNS` dict; `designs(batch)` merges the dicts (set 1 `group_a` + `group_b`, set 2 `agent_focus`). 2 Regenerate with `render.py` or `render.py --batch 2`. 3 Run `tests/test_designs.py`. | `.dev/design/orca-observer-20261106/layouts/{group_a,group_b,agent_focus}.py`; `render.py:21-23` (checkout path) | `test_all_scenarios_widths` asserts 20 designs, and `test_export_manifest` asserts 10 concepts per batch, so a new design breaks both by design; the counts in 11.2 change (derived, not run). Both batches must be generated before `test_export_manifest` can pass. Layouts must stay width-exact at 160/144/116/80 and show "SYNTHETIC" (GF-5) |

Skeletons for the two scenarios with a code contract (B, C, E and F follow existing shapes: one tuple in `ALLOWED_ORCA` at `probes.py:49-60`; one `("<jsonKey>", "<row_attr>")` pair in `export.py:25-45`; a `main(run)` script shaped like `exclude.py`; one `DESIGNS` entry):

```python
# A. classify.py (rule contract: Classification = rule applies; None = decline, next rule tried)
def _rule_example(row: SessionRow, ctx: SweepContext) -> Classification | None:
    if not (...):                                   # only row fields and ctx.now / ctx.window_start
        return None
    return _classification(C_EXAMPLE, "example", "evidence text")   # (class_name, rule, evidence, waiting_kind=None, notes=())
# Registration (`RULES` and `CLASSES` are tuples, so `+=` raises TypeError): insert Rule("example", _rule_example) into RULES before Rule("fallback", ...) (classify.py:345-355);
# add "example" inside CLASSES (models.py:50-59) and a ninth name C_EXAMPLE in the unpack (classify.py:42-51); add report.NEXT_INSPECTION["example"] = "read ..." (report.py:54-68)

# D. view.py: View gains `example: ExamplePanel | None = None`; build_view(...) passes example=_example_panel(result, clock)
def _example_panel(result: Any, clock: Any) -> ExamplePanel | None: ...   # None when the source is off
```

**Unification touch points (facts only; no recommendation).** The observer `--questions` read covers one named Run from the terminal that holds it (`consumer_fenced`, `no_active_terminal` otherwise), the same Run mailbox the design's wave 5 consumes with `check --wait`; the observer form carries no `--ack` or `--wait` (`adapter.py:34-50, 496-507`; GF-3 s10). Extension seams in code: observer `CycleSource` Protocol, `Runner` / `Discover` aliases (`adapter.py:24-27`), `Deps` (`commands.py:132-147`); sweep `RULES`, `ALLOWED_ORCA`, `SECTIONS`; AWR `run.py` dispatch. The rest (outputs, WC-16, `orchestrator_repo`, entry files, sanitizers, joins, wrappers) is in 2.5, 8.1 and 8.2.

### 13.2 Testing Requirements for Changes

| Change Type | Required Tests | Test Location |
|---|---|---|
| Sweep class or rule | one case per rule (`_rule_cases`), `reached == set(CLASSES)`, rule-order pin `RULE_NAMES`, `RULE_CLASS` and `NEXT_INSPECTION` coverage, counts keys equal `list(CLASSES)`, report determinism and sections | `tests/sweep/test_classify.py:277-379`; `test_report.py:549, 937, 1091-1130`; `test_cli_contract.py:956, 1032, 1070` |
| Sweep probe, allowlist, git | exact templates, 24 named negative argv, write-verb `ast` scan, recorded-argv full sweep, zero argv for not-called templates, budgets, byte limits, symlink escapes, stable-read, real-git hole routes with a positive control | `tests/sweep/test_probes_allowlist.py`, `test_readonly.py`, `test_git_config_hole.py` |
| Sweep CLI, publish, JSON | exit codes 0/1/2, publish failure modes, JSON key set and types, lazy registration | `tests/sweep/test_cli_contract.py:260-1505`, `test_cli_registration.py` |
| Sweep prose (command, skill, style) | 28 static drift guards on `commands/sweep.md`, `sc-sweep-protocol/SKILL.md`, `output-styles/pragmatic.md`; WC-16 heading and sentences; routing row | `tests/commands/test_sweep_command.py`; `tests/skills/test_worker_contract.py:167-170, 212-215`; `tests/core/test_how_we_work_routing_table.py:33` |
| Observer adapter or argv | exact argv per path, forbidden set (superset floor), 22 + 17 rejected shapes, cursor and run-id checks, paging, caps, real-process kill tests | `tests/observe/test_adapter.py` |
| Observer parse, merge, collector | strict envelope, UNKNOWN, identity, newer-wins merge, backoff `[30,60,60,60]`, STALE at exactly 45 s, single flight | `test_parse.py`, `test_collector.py`, `test_golden_contract.py` |
| Observer snapshot or export | schema validity after every cycle for every variant, closed nodes, privacy keys, 0600 atomic write, byte pin of questions-off records | `test_snapshot_schema.py`, `test_export.py`, `test_render.py:655-695` |
| Observer view, render, keys | session transitions, view build, 135 render tests, height budget over widths and heights, real pty tests (colour depth, `NO_COLOR`, alternate screen), key decoder | `test_session.py`, `test_view.py`, `test_render.py`, `test_height_budget.py`, `test_live_screen_pty.py`, `test_keys_spike.py` |
| Observer CLI and gates | options, exit codes, `--once`, gate constants cite an existing record, registration | `test_commands.py`, `test_registration.py` |
| Agent-work-report | run lock, gate, summary, page, exclude, refresh, symlink and url safety, entry-file reader | `tests/skills/test_agent_work_report.py` (142 definitions; living-report tests at 2979-3983) |
| Design package layout or fixture | `unittest` `Semantics` (10), `SafeText` (5), `Layouts` (4, including `test_export_manifest`, which needs both batches generated); Node DOM stub for the gallery (no browser); pass results not run [UNVERIFIED] | `.dev/design/orca-observer-20261106/tests/test_designs.py`, `test_gallery.cjs` (checkout path) |

Facts: tests were not run here; `test_commands.py:754-779` cannot pass on the snapshot because it omits `.dev/`; `tests/sweep/fixtures/captured-tab-map-*.json` are read by no test. All `tests/observe` paths above are under `tests/observe/`.

---

## 14. Known Limitations & Technical Debt

Labels follow rule R-C8 of GF-1 (14.5). Item ids (U-, CC-, SD-, DC-, G-, C8-) are the ids of `gaps-and-questions.md`. "None recorded" means no research file names a plan.

### 14.1 Current Limitations

| Limitation | Impact | Workaround | Planned Fix |
|---|---|---|---|
| Sweep `stalled (proved)` and `fenced` cannot fire on live data: `worker_done_seen` stays None and `fenced_evidence` stays `unreadable` because `parse_worker_show` never sets them (C8-1, C8-2, KNOWN LIMIT) | An exited worker prints `could not determine` with the note `Orca: exited; fenced evidence not readable`; a zero count means nothing | The report prints the limit (`SP24_LINE`); counts carry `(not observed in Phase 1)` | "until a source mapping exists" (SPEC:232); no work item owns the mapping (U-40); `fenced` has no "until" condition |
| Waiting (a) from `agentWait` alone has unknown age: `agent_wait_since` is never set (C8-3) | Row sits in the unknown-age group | A blocked contract gives an age from its mtime | None recorded; a non-null `agentWait` was never captured (U-11) |
| `Safe to close` and `Removable` never say `yes` (C8-4, C8-5) | Every cell reads `no` or `could not determine` with a reason | Read the reason text | Phase 2 `/sc:close` acts on these rows after the person confirms (SPEC:75, 208); no `yes` source is named |
| Sweep coverage gaps: remote hosts not scanned (lower bound), `Messages coverage: partial`, Ready-Task creator not observable, `worktree ps --agent-wait` never called | Totals are a lower bound; pending questions cannot be read | None | Out of Phase 1 on record (design s1 line 35) |
| Sweep show cap 50, no contract read, 256 KiB transcript tail, join path B | Live runs print mostly `could not determine` (issue #590: 264 sessions, 263 undetermined, causes not measured; recorded, not re-run [UNVERIFIED]) | Read the Evidence and Notes cells and the sources marked unscanned | Owner decision 2026-11-17 to page past the cap (issue #534 comment, wording UNVERIFIED) |
| Observer questions: one named Run, only from the terminal that holds it; 100-row window; nothing is ever closed ("seen is not resolved"); retention 1,000 | Bursts over 100 rows between reads may be lost; a handled question is listed again while Orca returns it | Run from the Run-holding terminal; export for newer questions | Recorded limit accepted in the owner pass record (2026-11-12) |
| Observer reads at most 500 worker rows per cycle (5 pages x 100; 400 with questions on); recorded live total was 428 | With questions on a full traversal never completes (always PARTIAL); oldest rows are the ones cut. Derived arithmetic, not stress-tested | Questions off | None recorded |
| Sweep reads one `worker-list` page of 100 rows per Run, no paging (probes.py:1150, 1157-1161) | `truncated`: page banner, a "could not determine" bullet, `origin unknown: worker list truncated` (5.4) | None | "paging not yet captured" (report.py:32); no owner recorded |
| Observer is POSIX only, needs a terminal of at least 80 columns and 8 rows, has no refresh key, and a polling thread ends if no Orca CLI is found | Windows prints POSIX-only text; narrow terminals print a refusal line | `--once` prints a plain record | None recorded |
| Observer snapshot v1 has no in-repo consumer; JSON drops 11 parsed attributes; the text record lists question subjects while the JSON does not | A second consumer would parse the file itself | None | None recorded |
| Question ledger and Decision Desk cannot be replayed from fixtures through `superclaude observe` (D-1, C8-9, KNOWN LIMIT (cited): cut R1, PR #577; 14.5) | `--questions --fixture` exits 2 | Fake-runner tests exercise views B and C | Remediation task not created (read-only brief); flagged for the owner |
| Living report: the entry writer `superclaude orchestrator report-entry` does not exist (C8-6) | `exclude.py` excludes nothing; `run.py refresh` renders no "Held by the orchestrator" block; closeout prints `ENTRY escalated why=surface_absent` | Entry files written by hand work (tests do this) | PR B (no PR); design states no interim behaviour (G-37) |
| `orchestrator_repo` key route to the state folder fails on master (C8-7) | Only `$AWR_ROOT` works | Set `$AWR_ROOT` | PR A (#686, open) |
| A "Needs you" entry for a session cannot be answered by `prefs.py answer ... <session url>` (C8-8, DEFECT-CANDIDATE) | The entry stays until answered | None found | Remediation task not created (read-only brief); flagged for the owner |
| Coordinator cadence ("at most once every 5 minutes") and "read before acting" are text duties; nothing schedules or enforces them | A sweep runs only when a session runs it | None | WC-16 says Phase 1 "adds this duty, not a scheduler" |

### 14.2 Technical Debt

No research file rates severity or effort, so those template columns read "not rated" and are not invented; the research label and the evidence are in the Description cell.

| Item | Severity | Description | Effort to Fix |
|---|---|---|---|
| `Window.more_text` | not rated | Dead code: field with no reader; spec says there is no "+N more" row. Evidence: `view.py:331, 402`; `test_render.py:99-118` | not rated |
| `counts` schema/parser mismatch | not rated | Untested risk: schema allows scalars; parser keeps nested JSON to depth 6. Evidence: `snapshot.schema.json:50`; `parse.py:277-290` | not rated |
| In-memory row set of identified rows only grows | not rated | Untested: `merge` keeps absent identified rows with `reobserved=False`, no cap or expiry (identity-unknown rows are dropped on a complete cycle, parse.py:726-727). Evidence: `parse.py:654-744` | not rated |
| `_find_orca` iterates `topics` outside its `try` | not rated | UNVERIFIED (U-03): a bad reply would end the observer's polling thread; not executed. Evidence: `install_user_setup.py:265-268`; `launch.py:148-152` | not rated |
| `PER_CALL_TIMEOUT` comment; constants labelled PROPOSED; `RowView.liveness` | not rated | Possibly stale comment "UNVERIFIED until the first permitted live read measures it" while live reads exist (SD-02, `adapter.py:60-62`); `RUN_ID_PATTERN`, `CURSOR_MAX_BYTES`, ms heuristic and schema are PROPOSED (U-02, `adapter.py:52-55`; `parse.py:247`); `RowView.liveness` is unread by ledger columns and read by `export._row_line` (U-32, `view.py:190`; `export.py:62`) | not rated |
| Sweep Budget defaults and four byte limits | not rated | No recorded decision (U-14); only the byte limits carry a "proposed" marker. Evidence: `probes.py:85-89, 127-133` | not rated |
| AWR entry fields `kind`, `group`, `follow_up_state` | not rated | Never read; in the contract comment or fixtures only. Evidence: research 05 s26 | not rated |
| AWR `waker.py` hourly mode, `templates/qa-report-template.md` | not rated | Leftover, unreferenced: no hourly automation exists; nothing reads a QA verdict. Evidence: `waker.py:8-9, 216-220`; SD-16 | not rated |

### 14.3 Future Considerations

| Item | Deferred Because | Revisit When |
|---|---|---|
| Sweep `stalled (proved)`, `fenced` live; Phase 2 `/sc:close` acting on Safe-to-close rows; report retention (SP-22, person deletes by hand) | no named live source for the absence of `worker_done` (SPEC:232); Phase 1 is read-only (SPEC:75, 208; design s1 line 35) | a source mapping exists (none is tracked); Phase 2; not stated |
| Observer write-back actions (reply, ack, resolve) | package contract is navigation only; recorded as a future stage that "never R1" and needs a boundary change on issue 409 | owner changes the boundary |
| Remote fleet rows (`--include-remote`); admission, revision-pinned verification, cost, deep links, persisted "last look", rotation set | R4 "Not established" (`release-gates.md:14`, backlog issue #604); not established or left out on record (`release-gates.md:17, 53`; `rendering-rules.md:97`) | not stated |
| A Go/TUI reader of the JSON snapshot; live issue 409 alignment items 1-10 (observer reads sweep JSON, recommendation text, PR/issue link sources) | Go reader deferred (`ARCHITECTURE-SPINE.md:287, 306, 318`); alignment items all "None is decided" (body lines 108-121) | not stated; owner decision |
| Orchestrator pieces: PR B (skill, verbs, "Orchestrated issue flow"), PR A (#686), PR P (#690) | sequencing D, A, P, B on record (DESIGN:1011-1046; ruling 37) | per the design order |
| Rasterised PNG visual-parity comparison | PNG route failed; gate scored on the text and ANSI tier | owner requirement (G-27) |

### 14.4 Contradictions, stale documentation and UNVERIFIED items

Where research files disagree, the stronger evidence wins: code and tests over docs; gap-fills over research files 01-06. Nine STALE DOC rows below are also [CODE-CONTRADICTED] in their source (SD-01, SD-06, SD-07, SD-21 to SD-24, SD-26, SD-27). Each row cites its research source in `gaps-and-questions.md`.

**A. Contradicted or stale documentation, grouped by subject** (document statement versus reality)

| Subject | ID and tag | Statement versus reality | Evidence |
|---|---|---|---|
| Sweep: design | SD-06 CODE-CONTRADICTED | `docs/designs/orchestrator-mode.md:27` says `src/superclaude/cli/sweep/` does not exist yet; the package exists (6 `.py` files). A dated fact (checked 2026-11-08) | Glob of `cli/sweep/` |
| Sweep: CHANGELOG | SD-07 CODE-CONTRADICTED | `CHANGELOG.md:170` (under `[6.0.0] - 2026-11-18`, "Known limits (sweep, Phase 1)") says `working` is never produced and healthy workers read `could not determine`; rule 5 is active since 2026-11-16 | `classify.py:251-269`; `test_cli_contract.py:1133-1140`; DESIGN:493, 841 |
| Sweep: CHANGELOG | SD-08 STALE DOC | Same line gives "the live `agentWait` names were never captured (design open item 6)" as the reason for stalled and fenced: the only public line that does. SPEC:232 gives a different reason; open item 6 is resolved 2026-11-16 (`orchestrator-mode.md:1003`) | CHANGELOG:170; SPEC:232 |
| Sweep: user guide | SD-09 STALE DOC | `docs/user-guide/commands.md:620` first clause (`working` never produced, healthy workers read `could not determine`) is stale; its clause "a waiting-on-a-person row from an agent wait cannot match on live data" is UNVERIFIED, not contradicted. `commands.md:619` is current and gives no reason | commands.md:619-621 |
| Sweep: issue and PR text | SD-10, SD-11 STALE DOC | Issue #534 body item 2 says rule 5 is inert (its own comment says PR #579 restored it; comment-level check only); PR #539 body lists "the working rule is inert and the agent-wait rule is dark" | `gh` read; `test_cli_contract.py:1133-1160` |
| Sweep: design status | SD-12 STALE DOC | Design section 17 still reads "Total: 23 open items" with no status column although item 6 is resolved and items 2, 3, 8 are implemented; treat as a historical list | `orchestrator-mode.md:992-1022` |
| Sweep: repo | SD-14 STALE DOC | The stale checkout `.gitignore` lacks the `.dev/sweeps/` rule that origin/master has at lines 255-256 | checkout vs master |
| Observer docs | SD-01 CODE-CONTRADICTED | `release-gates.md` R0 row says no recorded `worker-list` sample exists and `base` stands in; four golden samples exist and are tested | `fixtures/golden-*.json`; `test_golden_contract.py:22-199` |
| Observer docs | SD-02, SD-03 STALE DOC | `adapter.py:60-62` "UNVERIFIED until the first permitted live read" (live reads since 2026-11-17; possibly stale); RESEARCH-REPORT rotation set vs code (no contradiction found, tabled only) | `release-gates.md` lines 40-42 |
| Observer docs | SD-04, SD-05 STALE DOC | `post-release-report.md:56, 173` "No technical doc for `superclaude observe`" is still open at 61ac2c2e6 ("13 source files" vs 14 `.py` by Glob); `test_keys_spike.py:3` "only test module that uses a real pty" is older than `test_live_screen_pty.py:34` | docs/testing/v6.0.0 |
| Observer docs | CC-01 CODE-CONTRADICTED (minor) | "no key and no option maps to an Orca call" (`cli-groups.md:42`, HELP): true for keys and writes; `--run` and `--questions` select which read argv is built | `adapter.py:173-179, 469-512` |
| Report skill and entry files | CC-02 CODE-CONTRADICTED | `SKILL.md:14` and `common.py:25` name `orchestrator_repo` in `issue-watch.json`; the master poll rejects the key, so only `$AWR_ROOT` works. KNOWN LIMIT sequenced to PR A; the tag stands until PR A merges | `cycle.py:216-220`; ORCH:372, 374 |
| Report skill and entry files | CC-03 CODE-CONTRADICTED | `SKILL.md:14-16, 115-116` describe entry files and `exclude.py` in the present tense; the writer verb does not exist (design places it in PR B) | `refs/settle.md:99`; ORCH:510, 791 |
| Report skill and entry files | CC-04 CODE-CONTRADICTED (in part) | `SKILL.md:183` says the gate is enforced again by `clickup.py dm` and `run.py close`; `dm` enforces `deliverable`, `close` enforces only `passed()` | `clickup.py:619`; `run.py:376-379` |
| Report skill and entry files | CC-05 CODE-CONTRADICTED | Design DQ13 puts information entries under "Watching"; code uses "Other work in progress" and no "Watching" string exists | ORCH:123; `run.py:788-793` |
| Report skill and entry files | SD-16 to SD-20 STALE DOC | `qa-report-template.md` describes a verdict `run.py gate` reads (unreferenced; nothing reads it); `sc-closeout.md:361` says the skill is in IronFlow (moved by PR #684; the `report-entry` half is still true); `SKILL.md:56-72` omits `abandoned.json` and `refresh.lock`; design line cites into the IronFlow copy (render.py:194-303 etc., an expected shift); DQ12 "183 lines, 15 scripts" vs 194 and 16 | research 05 Stale |
| Issue 409 and design package | SD-21 to SD-24 CODE-CONTRADICTED | Live body says "No observer code exists yet" (lines 19, 36, 105), "No direction chosen" (25), PR #539 open (27, 28, 204: merged 2026-11-14), and the package is unmerged (`orchestrator-mode.md:609`: true only of commit 495eb96d1; the identical 406-file content is on master via PR #503). The body banner (line 13) says the observer is on master; the correction pass waits on an owner grant | `main.py:590-592`; PR #503, #539 |
| Issue 409 and design package | SD-25 to SD-29 STALE DOC | Package README and body prefer Bubble Tea / Lip Gloss; shipped observer is Python + Rich by owner decision 2026-11-08 (`stack.md:3`). `rendering-rules.md:3` says fixture mode uses the package's fixtures (different schema; only names shared). Local `issue-body.md:23` and `posted-body.md:23` say 405 files / 14,435,766 bytes (live: 406 / 14,438,526). `concepts.md:43-49` top three differ from the owner's staged three. Scope file `scope/04` cites wrong line numbers | research 06 s7 |
| Orchestrator design vs shipped | SD-30 to SD-35 STALE DOC | DESIGN:116, 135 cite WC-9 at :44-47 (now :41-45) and a `:300` line removed by PR #682; DESIGN:991, 1017 describe PR D as future work (merged 2026-11-20); guard comment at :500 is at `launch-level-guard.sh:496`; DESIGN:122 treats `refresh` and `exclude.py` as UNVERIFIED though the code exists; `closeout.md:97` names `/sc:issue --plan` (PR #690 open); ADD6 verb list omits `report-entry` and `plan-check` while the 5.1 row lists both | GF-3 Stale |

**B. UNVERIFIED items (all stay UNVERIFIED; M-17)**

| Subject | IDs | Statement | Evidence |
|---|---|---|---|
| Orca question read | U-01, U-04, U-05 | `orchestration check --all --types question` is not shown to be non-acknowledging: recorded probes show non-consumption for the owner-bound reader on probe Runs only; owner accepted the remainder 2026-11-12. Live message rate, `run-use` effect on a live coordinator, several concurrent observers, `message.id` on other Runs, fencing, the 100-row window, `--peek` order, latency and load figures are recorded probe results, re-verified only as encoded in code and fixtures | `adapter.py:34-50`; `release-gates.md:42, 48, 63`; `question-cap-100.json` |
| Observer constants, tests, versions | U-02, U-03, U-06, U-07, U-08, U-09 | `RUN_ID_PATTERN`, `CURSOR_MAX_BYTES`, ms heuristic (`> 1e11`) and the schema are PROPOSED; `_find_orca` robustness; four-kinds data-gate rule for messages (stale and contradictory samples); `tests/observe` golden and surface files not read; which tag first held R2 and R3 (no CHANGELOG entry); the two records cited by `commands.py:67, 70`; the Orca error-code names `consumer_fenced` and `no_active_terminal` (envelope `error.code`) are not shown to be verified against a live Orca (`adapter.py:65-69, 496-507`) | research 01 (line 52), 02 |
| Sweep inputs | U-10, U-11, U-12, U-13, U-15 | Whether Orca exposes a source for the absence of `worker_done` or fencing; the shape and meaning of a non-null `agentWait` (rule 4(a) unproven on live data; sweep reads `worker-show`, coordinator reads `worktree ps --agent-wait`); how often real transcripts exceed 256 KiB; whether path A ever matches in production; the definition of "route 7" in the git hole list | `models.py:98-112`; `probes.py:458-481`; `classify.py:40` |
| Sweep policy | U-14, U-16, U-30, U-31, U-39, U-40 | Budget defaults (50, 90 s, 10 s) have no recorded decision; design open items 17, 18, 21 not checked with `gh`; no stated rule for bumping `JSON_SCHEMA_VERSION`; a ninth `CLASSES` entry breaking the unpack (read from semantics, not run); how a live orchestrator or report session is classified (`could not determine` under path B per `classify.py:760-779`); no work item owns the "source mapping" (search, not scan) | `probes.py:127-133`; `models.py:18` |
| Observer internals | U-26, U-32, U-33 | `projection.attention` and `projection.parent` (present, redacted, not parsed) as attention or dependency signals; who reads `RowView.liveness`; `theme.py` role registration | `view.py:566-584`; `render.py:571, 1457` |
| Report skill and orchestrator environment | U-17 to U-23 | Who sets `orchestrator_repo` and writes `issue-watch.json`; Orca automations `coordinator-morning-wake`, `coordinator-missed-check` and their VERIFIED dates; the Orca automation `orchestrator-poll` (`*/5 * * * *`), the repo `IronbellyOrg/IronOrchestrator` and the `waker.py` triggers are outside the repo and not checked (research 05:571-572; GF-3:185-186; design O1, O3, O4); the spec path at `SKILL.md:12`; how the markdown entry-update template becomes the JSON entry file; design unknowns U17, U27, U38 (code answers partly, not run); ruling on two writers of the closed entry (`sc-closeout.md:374`); AWR test results ("142 tests" counts definitions) | research 05 |
| Orchestrator design | U-34 to U-38 | The eight FR-9 states and their mapping to `worker-list` fields (spec not in snapshot); whether WC-16 binds a script-started orchestrator (design says the orchestrator "is the coordinator", DESIGN:930; WC:70 says "a session the person opened"; open question of scope, flagged for the owner); the reach of PR B's "Orchestrated issue flow" section; typed approvals and the one interrupt against WC:122, 137, 188; `check --wait` types and cadence (design 4 types, 240000 ms; contract 9 types, 300000 ms) | GF-3 |
| Orca wrappers and recorded live result (no register id) | none | Why the observer, sweep and report skill have three separate Orca wrappers is not stated (Section 2.5; G-52); the issue #590 live result (264 sessions, 263 `could not determine`) is a recorded report, not re-run | issue #590; `adapter.py:224`; `probes.py:214`; `orca_term.py:17-21` |
| Design package | U-24, U-25, U-27, U-28, U-29 | `QA.md:9` "19 tests passed" and the gallery DOM test not run; `sources.json` E01-E04 against the installed Orca; the DejaVu font path; checked-in artifacts against the current `render.py`; README line 44 "previous prototype files are preserved unchanged" | `.dev/design/orca-observer-20261106/` |

**C.** The remaining open gaps (ids G-01 to G-52) and Gate 1 count corrections are in `gaps-and-questions.md`; their facts are stated where they apply (Sections 5, 9 to 11 and 14.1).

### 14.5 C8 DEFECT-CANDIDATE analysis

**The single rule (R-C8, GF-1 s2; it supersedes research 04's stricter test, which labelled stalled, fenced and `agent_wait_since` DEFECT-CANDIDATE).** A capability that a spec, design, skill, command or user doc names as shipped, enabled or required, and that has no producer, writer or reachable path at its runtime entrypoint, gets one label:

1. A cited spec-level or design-level text states, for that specific capability, that the shipped build does not deliver it (deferred, fixture-only, not observed, not observable, UNVERIFIED with a stated fallback outcome, or assigned to a named later piece of work): **KNOWN LIMIT (cited)**, citation printed. A report footnote, CHANGELOG line or user-guide line shows the limit is disclosed; by itself it is not the scope decision.
2. No such text: **DEFECT-CANDIDATE**. A text that only records an absence ("not built", "cannot run as written", "UNVERIFIED") does not meet step 1.
3. Either label carries the residual owner facts the citation does not settle; residual facts never change the label.
4. "Remediation task not created (read-only brief); flagged for the owner" is printed on every DEFECT-CANDIDATE and on every KNOWN LIMIT whose cited text names no tracked owner for its "until" condition.

Table of determinations (SPEC = `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` on origin/master; DESIGN = `docs/designs/orchestrator-mode.md`; ORCH = `docs/designs/orchestrator.md`):

| ID | Capability | Label | Declaring spec or design line | Code evidence | Cited decision or statement |
|---|---|---|---|---|---|
| C8-1 | Sweep `stalled (proved)` (rule 2 `orca_exit_proof`) | KNOWN LIMIT (cited) | SPEC:103 (FR-009), `commands/sweep.md:14`, WC:289 | `models.py:108-109`; `probes.py:471-515` never sets the inputs; `classify.py:196-200` | SPEC:231-232 ("stays fixture-only until a source mapping exists"); DESIGN:493, 636, 841, 877. Residual: no work item owns the mapping (U-40); review inputs, not a dated owner ruling (G-12). Impact in 14.1. Remediation task not created (read-only brief); flagged for the owner |
| C8-2 | Sweep `fenced` (rule 3) | KNOWN LIMIT (cited) | SPEC:251, `commands/sweep.md:14` | `models.py:109`; `classify.py:219-223` needs `present`; no producer | SPEC:251 "synthetic fixtures only in Phase 1", SPEC:231; DESIGN:493, 636, 841, 877. Residual: no "until" condition. Remediation task not created (read-only brief); flagged for the owner |
| C8-3 | Sweep `agent_wait_since` | KNOWN LIMIT (cited) | SPEC:238 | read at `classify.py:229-235`, `report.py:127-128`; set nowhere (`probes.py:481`) | SPEC:238; DESIGN:493, 494, 649, 1003. Residual: a non-null `agentWait` was never captured (U-11). Remediation task not created (read-only brief); flagged for the owner |
| C8-4 | `Safe to close` never `yes` | KNOWN LIMIT (cited) | SPEC:106 (FR-012) | `classify.py:479-504`: no branch returns `yes` | SPEC:106, 111, 167, 274; DESIGN:794. Only Phase 2 `/sc:close` (SPEC:75, 208) is named later; no `yes` source stated. Remediation task not created (read-only brief); flagged for the owner |
| C8-5 | `Removable` never `yes` | KNOWN LIMIT (cited) | SPEC:106 | `classify.py:455-476`; `REASON_NOT_OBSERVABLE` (:88-90) | SPEC:274, 338; DESIGN:795. No later work named. Remediation task not created (read-only brief); flagged for the owner |
| C8-6 | Living-report entry writer `superclaude orchestrator report-entry` | KNOWN LIMIT (cited), sequenced to PR B | `SKILL.md:14-16, 115-116`; `common.py:133-137` | no code outside tests writes `orchestrated/*.json`; `superclaude orchestrator` absent from `cli/` and `main.py`; `refs/settle.md:99` | ORCH:3 (owner ruling 37, 2026-11-19), 510, 791, 1020, 1021, 1041; closeout handles absence under D10 (`sc-closeout.md:66, 368`). Residual: skill text [CODE-CONTRADICTED] (CC-03); no interim behaviour stated (G-37); if the owner holds that a PR-sequencing line is not a scope decision the label becomes DEFECT-CANDIDATE with no fact changed (G-35). Remediation task not created (read-only brief); flagged for the owner |
| C8-7 | `orchestrator_repo` route to the state folder | KNOWN LIMIT (cited), sequenced to PR A | `SKILL.md:14`; `common.py:25` | master poll rejects the key (`cycle.py:216-220`) | ORCH:372, 374, 1018; PR A (#686) open. Residual: who sets the key is unverified (U-17); the [CODE-CONTRADICTED] tag stands (CC-02). Remediation task not created (read-only brief); flagged for the owner |
| C8-8 | Answering a "Needs you" session entry (`prefs.py answer <run> <session url> session`) | **DEFECT-CANDIDATE** | `SKILL.md:172`; `SKILL.md:22` ("An unanswered 'Needs you' entry stays until Clay answers it") | `prefs.check_url` accepts only GitHub and ClickUp urls (`prefs.py:20, 30-32`), so `orca://session/<id>` exits "not an item URL"; `render.still_waiting` drops an entry only when its url is in `answered_since` (`render.py:339, 347`); also [CODE-CONTRADICTED] | none found. Remediation task not created (read-only brief); flagged for the owner |
| C8-9 | D-1: fixture replay of the question ledger and Decision Desk through `superclaude observe --fixture` | **KNOWN LIMIT (cited)** (relabelled from DEFECT-CANDIDATE at Gate 4 review 1) | `SPEC.md:32` (CAP-1), `release-gates.md:9` (R0), `acceptance-tests.md:25` (AC-3, T7) under `.dev/issues/409/bmad/spec-orca-observer/` | `commands.py:77-78, 183-188, 414` refuse `--questions` with `--fixture` (exit 2); `FixtureSource.read_questions` always returns FAILED `no-question-fixture` (`collector.py:125-129`); only test hit `test_collector.py:675` | `.dev/issues/409/ponytail-review-20261116/cuts-debate/final-cut-list.md:24` (row R1, CUT-SMALLER, EXECUTE-NOW, 80 percent: cut the `question_fixture` argument, state and replay in `collector.py`, "keep `read_questions` as a 2-line stub returning FAILED `no-question-fixture`"; surviving guard "`--fixture` with `--questions` refused: commands.py:177-178") and `:62` (row D13: mark T7 "not built / no automated test"); `cuts-debate/execute-now-brief.md` Step 1; `ponytail-review-20261116/runtime-code.md:51` ("production can never reach it"); applied by PR #577 (merged 2026-11-17T00:40:16Z, "applies the 11 debated cuts"; issue comment of 2026-11-17: "applied the 11 agreed cuts"); `acceptance-tests.md:25` now carries the D13 wording, a text that alone would only record an absence. All on origin/master. This record meets R-C8 step 1: a design-package decision text, for this specific capability, that the build does not deliver it. Residual: it is a review-panel debate output, not a dated owner ruling, and names no "until" condition or owner; if the owner holds that a debated cut is not a scope decision the label becomes DEFECT-CANDIDATE with no fact changed (G-36 searched five owner records; they contain nothing on fixtures). Scope: observer `--fixture` path only; live `--questions` is wired. Question for the owner (fact, not a recommendation): is fixture replay through `superclaude observe --fixture` still wanted, or is the fake-runner test route the accepted substitute? Remediation task not created (read-only brief); flagged for the owner |

Checked and not raised as candidates (GF-1, GF-3, GF-4, GF-5): observer live R2 and R3, snapshot and `--once` are wired (both gate constants True, chain traced from the click option to the Orca read). The orchestrator design is a proposal ("It holds no implementation code", DESIGN:3), so its unbuilt `/sc:orchestrator`, verbs and contract section are not named as shipped. The missing `report-entry` verb is named in `check.py:77` (docstring) and `common.py:136` (comment) and called only by `settle.sh:1037-1042` (probe at :1037, call at :1042, ends `ENTRY escalated why=surface_absent`); that one caller is covered by decision D10. WC-16 versus the orchestrator design is an open question of scope, not a defect (U-35); no on-record decision says the orchestrator is exempt from WC-16 or covered; flagged for the owner; remediation task not created (read-only brief). The design package pipeline has a writing call for every documented output (no candidate); `--width` is ignored in export mode, `test_export_manifest` does not check `.mono.png`, the contact sheet, the gallery or the hash, and batch 2 rewrites the root `fixture.json` and `scenarios/` (facts, not defects). Declared Phase 1 limits with cited text (Ready-Task creator, remote hosts, Orca messages) and package-only designs not adopted by the observer (hold/pause, heartbeat classification, secret redaction, superseded attempts) are not named as shipped in the observer.

### 14.6 Process note (write boundary)

Research file 03 (line 10) records that one scratch copy of the SPEC was written to `/tmp` during reading and deleted again: a breach of the read-only write boundary with no residue (M-11, G-45). It is surfaced here for the owner. GF-1 states it wrote no scratch copy and read the SPEC with `git show ... | cat -n` only.

---

## 15. Verification & Accuracy

### 15.1 Verification Log

| Date | Verified By | Code Version / Commit | Sections Verified | Issues Found |
|---|---|---|---|---|
| 2026-11-20 | synthesis agent (Doc Analyst role) over research files 01-06, GF-1 to GF-5, `gaps-and-questions.md` | code: origin/master 61ac2c2e6 (read-only export); design package: docs-branch commit 495eb96d1 | 12, 13, 14, 16 and Appendix against the research files; code re-read this pass limited to `sweep/probes.py:40-63`, `sweep/report.py:50-71`, `observe/export.py:22-48` (skeleton literals) | 134 tracked items: 40 UNVERIFIED, 5 CODE-CONTRADICTED, 35 STALE DOC, 2 DEFECT-CANDIDATE as registered (Gate 4 relabelled D-1 / C8-9 to KNOWN LIMIT (cited), so one DEFECT-CANDIDATE, C8-8, stands in 14.5), 52 GAP (UNVERIFIED, CODE-CONTRADICTED, STALE DOC and DEFECT-CANDIDATE items in 14.4 and 14.5; GAP rows in `gaps-and-questions.md`). Gate 3 cycle 1 fixes (2026-11-20) re-read `keys.py:165-235`, `view.py:30, 91-118`, `collector.py:248-323`, `page.py:381-387`, `classify.py:42-51, 345-355` and `models.py:50-59` on the snapshot. Gate 4 cycle 1 fixes (2026-11-20, GF4-1 to GF4-8) re-read `observe/parse.py:712-745`, `observe/export.py:200-216`, `sweep/report.py:613-695`, `sweep/probes.py:1143-1161`, `sweep/classify.py:690-705, 760-778`, `sweep/commands.py:180-207`, `observe/collector.py:125-129`, `gh pr view 673`, `gh pr view 577`, `gh issue view 606`, the origin/master design-package cut-list record (`final-cut-list.md`, `runtime-code.md`, `execute-now-brief.md`) and the S and R rule sources. No tests, Orca, `gh` or renderer were run; test counts are counts of definitions |

Trust levels: [CODE-VERIFIED] statements come from research files that read the code; everything under UNVERIFIED in 14.4 stays UNVERIFIED. Research files 01-06 each carry their own date (2026-11-20).

### 15.2 Spot-Check Protocol

1. **File existence check:** every path in Sections 12-14 exists at origin/master 61ac2c2e6, for example `src/superclaude/cli/{observe,sweep}/`, `src/superclaude/skills/agent-work-report/scripts/`, `tests/{observe,sweep}/`, `docs/designs/orchestrator-mode.md`, `docs/designs/orchestrator.md`. Paths under `.dev/` exist only on origin/master (`git show origin/master:<path>`), the design package only at 495eb96d1 or via PR #503.
2. **Export verification:** check 3-5 signatures from the Public Interface blocks of Section 5 against the source: `classify` (`classify.py:369`), `collect` (`probes.py:1322`), `build_view` (`view.py:968`), observer `render` (`render.py:1449`), `Collector.__init__` (`collector.py:135`), and the `RULES` tuple of nine `Rule` entries (`classify.py:345-355`).
3. **State shape and component tree:** Sections 6 and 7 carry no client-state or component tree (N/A); if a later version adds one, compare it with `Session` (`view.py:151-168`), `CycleResult` (`collector.py:37-68`) and the width-class layouts of `render.py` (`LAYOUTS`, `_columns`, `_desk_widths`).
4. **Convention check:** verify 2-3 conventions from Section 12 in recent changes, for example: the forbidden-prefix set only grows (`test_adapter.py:178-192`); the rule order pin (`test_classify.py:378-379`); the closed snapshot schema (`snapshot.schema.json:6` and `test_snapshot_schema.py:59-73`).

---

## 16. Glossary

| Term | Definition |
|---|---|
| Observer | `superclaude observe` (`src/superclaude/cli/observe/`): read-only terminal view and record of Orca `worker-list` rows, on master since PR #503 (2026-11-11), registered at `main.py:590-592`. Python with Rich |
| Sweep | `superclaude sweep run` and `/sc:sweep` (`src/superclaude/cli/sweep/`): read-only snapshot of a Run, its worktrees and person-started sessions; writes one dated report under `.dev/sweeps/` and prints JSON v1; recommends nothing |
| WC-16 | Rule "Coordinator loop" at `core/WORKER-CONTRACT.md:287-289`: the coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, beside "The sweep." (WC:110) |
| WC-10 | Contract rule on stall proofs: restart only on Orca's positive proofs; a missing heartbeat is absence, not death (`WORKER-CONTRACT.md:46, 157`) |
| "The sweep." | The coordinator's own liveness pass (WC:110): one `worker-list`, one `worktree ps --agent-wait`, one `stat` per contract path; distinct from `/sc:sweep` |
| R0, R1, R2, R3 | Observer release stages: R0 synthetic fixture renders; R1 live worker-list ledger, `--once` and snapshot (it records the redacted golden samples); R2 question read (`--questions`); R3 link and Decision Desk. R4 (remote fleet) is "Not established" |
| Decision Desk | R3 observer pane for one selected question, built only with `--questions` and the link on; joins the question's verified `dispatch_id` to a collected row; screen only; no key acts on a question |
| Orchestrator | Designed, unbuilt: "a standing-grant coordinator and not a worker" (`docs/designs/orchestrator.md`; DESIGN:799); `/sc:orchestrator` and `superclaude orchestrator` do not exist |
| agent-work-report (AWR) | Skill in `src/superclaude/skills/agent-work-report/` (PR #684): 15-step report over GitHub, ClickUp and Orca sessions, plus the living report |
| PR A, B, C, D, P | A #686 poll wakes the orchestrator (open); B orchestrator skill and verbs (no PR); C #684 report skill and living report (merged); D #682 plan-approval retirement (merged); P #690 `/sc:issue --plan` (open) |
| SPEC | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` on origin/master (653 lines) |
| C8, KNOWN LIMIT, DEFECT-CANDIDATE | C8 is the brief's rule for capabilities named in scope but not reachable at the runtime entrypoint, applied as R-C8 (14.5): KNOWN LIMIT = cited text says the build does not deliver the capability; DEFECT-CANDIDATE = no such text |

---

## Appendices

### Appendix A: Document Provenance

This is not a consolidation of the research; it is the provenance of this document. All code claims trace to origin/master 61ac2c2e6 as read by the research agents; design-package claims trace to commit 495eb96d1. No unification between the tools is recommended or implied. All paths below are under `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/`.

| Source | Contribution to this document |
|---|---|
| Research 01 `research/01-observe-data-contract.md`, 02 `research/02-observe-interaction-gates-docs.md` | Observer: argv guard, parse and merge, collector, STALE, snapshot schema versus export, fixtures, error codes, non-acknowledging read verdict, key map, width classes, theme and sanitizer, R2/R3 wiring, tests, consumers, docs versus code (5.1, 5.2, 12, 13.1 C and D, 13.2, 14.1, 14.4) |
| Research 03 `research/03-sweep-classifier-joins.md`, 04 `research/04-sweep-readside-wc16.md` | Sweep: nine rules, eight classes, joins, producer search, allowlists, budgets, git guard, publish, report sections, JSON v1, sanitizer, WC-16 chain (5.3, 5.4, 12.1, 12.2, 13.1 A and B, 13.2, 14.1, 14.5); 03 records the scratch-copy note (14.6); 04's stalled, fenced and `agent_wait_since` labels are superseded by GF-1 |
| Research 05 `research/05-agent-work-report-living-report.md`, 06 `research/06-dashboard-design-vs-observer-gaps.md` | Report skill: scripts, gate, entry-file contract, built-versus-designed table, PR state (5.5, 12, 13.1 E, 14.1, 14.4); design package, contradictions C1-C8 settled against live sources, D-1 (5.6, 14.4 A, 14.5) |
| GF-1 `research/gapfill-c1-GF1-c8-reconciliation.md`, GF-2 `research/gapfill-c1-GF2-commands-md-claim.md`, GF-3 `research/gapfill-c1-GF3-orchestrator-design-overlap.md`, GF-4 `research/gapfill-c1-GF4-public-entry-points.md`, GF-5 `research/gapfill-c1-GF5-package-pipeline.md` | GF-1: rule R-C8 and every C8 label (authority for 14.5); GF-2: what `CHANGELOG.md:170`, `commands.md:619` and `:620` each say (14.4 A); GF-3: orchestrator design versus the tools, verbs, FR-9, contract edits, PR chain (8.1, 13.1, 14.4); GF-4: entry-point signatures and extension contracts (13.1); GF-5: design package render pipeline and tests (5.6, 14.4, 14.5) |
| `gaps-and-questions.md`; Gate 1 `qa/qa-research-consolidated-findings.md` | The 134-row register behind Section 14; blocking findings GF-1 to GF-5 (answered by the gap-fill files) and minor findings M-1 to M-17 (applied in the sections they concern) |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-11-20 | rf-assembler (from seven synthesis files) | Initial reference created from the synthesis files; assembly only, no new findings and no recommendation. After Gate 3 review 1 (fix cycle 1) the length was cut from 1,698 to under 1,400 lines (the Standard budget is 800-1,200; four subjects justify an upper-end overrun): repeated note blocks, the 2.5 C8 pointers, 14.4 C, the Appendix A assembly map and tables restated in other sections were removed. Gate 3 findings applied: 14.2 columns, C8 wording in five rows, the 12.3 cross-reference, 13.1 row D steps and a design-package scenario F, the 5.5 `page.py` usage, the skeleton A registration text, the run-folder cross-reference and package error, scenario and test rows. Gate 4 findings applied (GF4-1 to GF4-8): observer row retention, snapshot `collection` keys, sweep JSON shapes, sweep worker-list truncation, the report-name-exhausted message, D-1 / C8-9 relabelled KNOWN LIMIT (cited), PR #673 "refs #606", and the S1-S11 / R1-R11 rule texts. Research-file names appear as "research 0N" |

---
