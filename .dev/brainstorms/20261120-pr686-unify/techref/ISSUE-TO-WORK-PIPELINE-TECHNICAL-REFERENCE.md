---
id: "ISSUE-PIPELINE-TECHREF"
title: "Issue-to-Work Pipeline - Technical Reference"
description: "Post-implementation technical reference documenting the architecture, subsystems, data flow, and operational details of the issue-to-work pipeline (issue watcher, issue claim flow, launch-level guard stack, coordinator contract text, and the removed issue-pipeline package) as currently built on origin/master 61ac2c2e6"
version: "1.0"
status: "🟡 Draft"
type: "📖 Technical Reference"
priority: "🔼 High"
created_date: "2026-11-20"
updated_date: "2026-11-20"
assigned_to: "IronClaude maintainers"
autogen: false
autogen_method: ""
coordinator: "Not recorded in the sources"
parent_doc: "docs/designs/issue-watcher.md (design of the watcher), read in the snapshot"
parent_task: "TASK-TECHREF-issue-pipeline-20261120-040158"
related_prd: "None found in the snapshot"
related_tdd: "docs/designs/issue-watcher.md"
depends_on:
- "docs/designs/issue-watcher.md"
- "docs/designs/issue-watcher-setup.md"
- "docs/designs/sc-issue-launch-level-hook.md"
- "docs/designs/sc-issue-claim-pipeline-flag.md"
related_docs:
- "docs/designs/issue-pipeline-fu1.md"
- "docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md"
- "src/superclaude/core/WORKER-CONTRACT.md"
tags:
- technical-reference
- issue-pipeline
- issue-watch
- sc-issue
- launch-level-guard
- post-implementation
- architecture
source_references:
- "Snapshot root: /home/coder/.cache/ic-snap-20261120/master (read-only export of origin/master, commit 61ac2c2e6)"
- "Removed-code commit: 01e7a9e23 (issue-pipeline package, read at 01e7a9e23^)"
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

# Issue-to-Work Pipeline - Technical Reference

> **WHAT:** Post-implementation technical reference documenting the architecture, subsystems, data flow, and operational details of the issue-to-work pipeline as currently built.
> **WHY:** Serves as the source of truth for AI coding agents and human developers who need to understand, modify, or extend the pipeline without reading every source file. Where implementation diverges from a design document, this reference follows the code.
> **HOW TO USE:** Engineering teams maintain this as a living document; developers and AI agents consult it before modifying or extending the pipeline.

**Purpose:** Describe, as built, how a GitHub issue on `IronbellyOrg/IronClaude` moves from "approved by a person" to a claimed issue and, when asked, to a launched agent session, and which parts of that path are on, switched off, not built or removed.
**Date:** 2026-11-20
**Tier:** Standard
**Research files:** 6 codebase + 0 web research (web research skipped: repo-internal subject)
**Scope:** the watcher (`superclaude issue-watch`), the claim flow (`/sc:issue --claim`), the guard stack (L1 hook guard, job-identity wrapper, L2 pre-push hook, launch levels), the coordinator contract text, and the removed `issue-pipeline` package.
**Snapshot identity:** origin/master 61ac2c2e6 (removed code read at 01e7a9e23^).

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| Requirements | Product PRD | Product | None found in the snapshot |
| Design | `docs/designs/issue-watcher.md` and the other design files listed in the frontmatter | Engineering | Read in the snapshot |
| **Implementation** | **This Technical Reference** | **Engineering** | **Living document, updated with every significant change** |

---

## Document Information

| Field | Value |
|-------|-------|
| **Feature Name** | Issue-to-Work Pipeline |
| **Feature Type** | Backend / Infrastructure (Click CLI group, Claude Code hooks, git hook, instruction text) |
| **Tech Lead** | Not recorded in the sources |
| **Engineering Team** | IronClaude maintainers |
| **Maintained By** | IronClaude maintainers |
| **Source Location** | `src/superclaude/cli/issue_watch/`, `src/superclaude/skills/sc-issue-protocol/`, `src/superclaude/commands/issue.md`, `src/superclaude/hooks/`, `src/superclaude/core/WORKER-CONTRACT.md` |
| **Last Verified Against Code** | 2026-11-20, against origin/master 61ac2c2e6 |
| **Implementation Status** | Mixed: watcher BUILT-OFF (enabled:false), claim and guard stack BUILT-ON, coordinator duties NOT BUILT, `issue-pipeline` package REMOVED (ledger in Section 2.3) |

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
- [x] Section 1: Overview - Populated
- [x] Section 2: Architecture - Populated
- [x] Section 3: Directory Structure - Populated
- [x] Section 4: Data Flow - Populated
- [x] Section 5: Subsystem Reference - Populated (5.1 watcher, 5.2 claim flow, 5.3 guard stack and launch levels, 5.4 coordinator contract text)
- [x] Section 6: State Management - Populated (local file stores; no client-side state)
- [x] Section 7: Component Inventory - N/A (backend feature, no UI components), with rationale in the section
- [x] Section 8: API & Integration Points - Populated
- [x] Section 9: Configuration & Environment - Populated
- [x] Section 10: Error Handling & Edge Cases - Populated
- [x] Section 11: Performance Characteristics - Populated
- [x] Section 12: Conventions & Patterns - Populated
- [x] Section 13: Extension Guide - Populated
- [x] Section 14: Known Limitations & Technical Debt - Populated
- [x] Section 15: Verification & Accuracy - Populated
- [x] Section 16: Glossary - Populated
- [x] Appendix A: Test-Pin Matrix - Present
- [x] Appendix B: Removed on 2026-11-20 - Present
- [ ] All links verified - Not performed; the document cites repository paths, not hyperlinks
- [ ] Reviewed by a person - Pending

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | The design and architecture documents listed in the frontmatter; the snapshot source tree |
| **Upstream** | Feeds from: the source code at origin/master 61ac2c2e6 and the removed code at 01e7a9e23^ |
| **Downstream** | Feeds to: operators of `issue-watch` and `/sc:issue`, maintainers of the guard stack, authors of coordinator contract text |
| **Change Impact** | Notify: owners of the watcher, the claim skill, the hook scripts and `WORKER-CONTRACT.md` |
| **Review Cadence** | As-needed, and after any change to the files named in Section 3 |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
   - 2.1 Whole-pipeline diagram
   - 2.2 Component relationship table
   - 2.3 Live-versus-switched-off ledger
   - 2.4 Integration map
3. [Directory Structure](#3-directory-structure)
   - 3.1 Key file inventory
4. [Data Flow](#4-data-flow)
   - 4.1 Watcher cycle; 4.2 Claim flow by wave and actor; 4.3 Launch-level binding flow
   - 4.4 Trigger table; 4.5 Writes to GitHub, per piece; 4.6 Approval and gate points
5. [Subsystem Reference](#5-subsystem-reference)
   - 5.1 Issue watcher (5.1.1 poll cycle, 5.1.2 GitHub I/O, 5.1.3 launch and dispatch record, 5.1.4 operator surface, 5.1.5 gates and approvals, 5.1.6 reason vocabulary, 5.1.7 dead and not-built items, 5.1.8 contradictions, 5.1.9 extension points)
   - 5.2 `/sc:issue --claim` flow and `orca_worktree.py`
   - 5.3 Guard stack and launch levels
   - 5.4 Coordinator contract text
6. [State Management](#6-state-management)
7. [Component Inventory](#7-component-inventory) (N/A, not a UI feature)
8. [API & Integration Points](#8-api--integration-points)
   - 8.1 External commands; 8.2 CLI surface; 8.3 Hand-off contracts; 8.4 Hook registrations; 8.5 External service dependencies
9. [Configuration & Environment](#9-configuration--environment)
   - 9.1 Watcher configuration file; 9.2 Claim, guard and install settings; 9.3 Environment variables, paths and kill switch; 9.4 What is not configurable
10. [Error Handling & Edge Cases](#10-error-handling--edge-cases)
    - 10.1 Exit-code tables; 10.2 Closed vocabularies; 10.3 Recovery and fail-safe behaviour; 10.4 Guard exit codes
11. [Performance Characteristics](#11-performance-characteristics)
    - 11.1 Budgets, deadlines and caps; 11.2 Performance-critical code
12. [Conventions & Patterns](#12-conventions--patterns)
    - 12.1 Code conventions; 12.2 Architectural patterns; 12.3 Anti-patterns
13. [Extension Guide](#13-extension-guide)
    - 13.1 Common extension tasks (13.1.1 to 13.1.8); 13.2 Testing requirements for changes
14. [Known Limitations & Technical Debt](#14-known-limitations--technical-debt)
    - 14.1 Current limitations (14.1.1 limitations table, 14.1.2 doc-versus-code contradiction table)
    - 14.2 Technical debt (14.2.1 DEFECT CANDIDATE, NOT BUILT, BUILT-OFF and REMOVED capability rows)
    - 14.3 Future considerations (14.3.1 evidence limits and open questions, 14.3.2 architectural risks)
15. [Verification & Accuracy](#15-verification--accuracy)
    - 15.1 Verification log; 15.2 Spot-check protocol; 15.3 Evidence limits; 15.4 Evidence trail; 15.5 Remediation and web research; 15.6 Assembly cross-check
16. [Glossary](#16-glossary)
- [Appendix A: Test-Pin Matrix](#appendix-a-test-pin-matrix) (A.1 watcher, A.2 guard stack, A.3 claim, A.4 other directories)
- [Appendix B: Removed on 2026-11-20](#appendix-b-removed-on-2026-11-20) (B.1 to B.9)
- [Document History](#document-history)

---

## 1. Overview

The issue-to-work pipeline takes a GitHub issue on `IronbellyOrg/IronClaude` from "approved by a person" to "claimed, with an accuracy check, a summary and next steps posted", and, when asked, on to a Claude agent session launched in an Orca worktree whose launch level is enforced by hooks. It is four cooperating pieces plus a fifth, the `issue-pipeline` package, that was removed in commit 01e7a9e23 (PR #682). As built, the watcher ships switched off and nothing in the snapshot schedules it, so only a person typing a command starts any part of the pipeline. The built-versus-not-built ledger is in Section 2.3.

**What it does:** a watcher polls GitHub read-only for approved issues and starts one Orca claim session per cycle; the claim session assigns the issue and posts two marked comments; optionally the claim creates a worktree and launches an agent bound to a launch level by guard hooks.

**Who uses it:** the repository owner (runs the five `issue-watch` verbs and types `/sc:issue --claim`), Claude Code sessions (claim orchestrator, tier workers, launched agents) and Orca (`agent launch`, `worktree create`). The repository literal is hard-coded in the watcher (`src/superclaude/cli/issue_watch/github.py:37`, `src/superclaude/cli/issue_watch/launch.py:50`).

**Where it lives:**

| # | Piece | What it is | Location |
|---|-------|------------|----------|
| 1 | Watcher | `superclaude issue-watch` Click group: poll cycle, read-only `gh` calls, local state, one fixed Orca launch | `src/superclaude/cli/issue_watch/` (registered at `src/superclaude/cli/main.py:577-579`) |
| 2 | Claim | `/sc:issue --claim`: command front, orchestrator skill, tier workers, helper scripts, templates | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/`, `src/superclaude/agents/issue-worker-t{1,2,3}.md` |
| 3 | Guard | L1 hook guard, job-identity command wrapper, L2 git pre-push hook, G2 rule 2, hook registration and install | `src/superclaude/hooks/scripts/launch-*.sh`, `src/superclaude/hooks/hooks.json`, `src/superclaude/cli/install_hooks.py` |
| 4 | Coordinator text | worker and coordinator contract; it holds no issue-pipeline duties | `src/superclaude/core/WORKER-CONTRACT.md` |
| 5 | Removed | `issue-pipeline` command group, rule WC-17, "Issue pipeline duties", guard rule 1 | absent in the snapshot; read at `01e7a9e23^` under `src/superclaude/cli/issue_pipeline/` |

**Two kinds of "level".** "L1" and "L2" name guard LAYERS, not pipeline levels: L1 is the Claude Code hook `src/superclaude/hooks/scripts/launch-level-guard.sh` (header :4-6) and L2 is the git `pre-push` hook `src/superclaude/hooks/scripts/launch-level-pre-push.sh` (header :4-5). The `--pipeline` levels (`src/superclaude/commands/issue.md:43-44`) are `worktree`, `full`, `full --submit` and `none`. The guard stores one level per bound session as W (worktree), WA (worktree, approved), F (full) or FS (full --submit) (`src/superclaude/hooks/scripts/launch-level-guard.sh:264-272`). `none` has no guard level because the claim ends before any launch (`src/superclaude/skills/sc-issue-protocol/SKILL.md:90`).

**Key statistics** (stated here once; later sections do not repeat them):

| Area | Figures | Counted at |
|------|---------|------------|
| Watcher package | 8 modules, 4,795 lines (cycle 1,406; github 960; record 865; audit 404; launch 370; cli 348; predicates 312; runner 130), plus an empty `__init__.py` | `src/superclaude/cli/issue_watch/` |
| Watcher surface | 5 verbs; 7 read-only `gh` calls (G1-G7); per-issue call cap 35 (32 ordinary plus 3 reserved) plus the two shared calls G1 and G2, so at most 37 `gh` calls per cycle (2 when idle); 59 reason words; exit codes 0, 1, 2, 3, 4, 5, 6, 7, 75; launch argv of 12 elements | `src/superclaude/cli/issue_watch/cli.py:111-348`, `.../github.py:175-262`, `.../audit.py:26-102`, `.../launch.py:95-116` |
| Watcher store | `dispatch.json` with 7 top-level keys, 17-field entries, 6 entry states, transitions T-1..T-13 | `src/superclaude/cli/issue_watch/record.py:120-130, 69-88, 34-36` |
| Watcher tests | 20 files in `tests/issue_watch/` (19 test modules plus `conftest.py`), 19,801 lines, 867 test functions (parametrisation not expanded), 19 `_assumed_shape` fixtures | `tests/issue_watch/` |
| Claim | `issue.md` 117 lines; `SKILL.md` 197 lines plus 5 refs; `orca_worktree.py` 1,906 lines; `origin_repo.py` 195; `clickup_claim.py` 270; 15 templates; 3 worker agents of 35 lines each; 4 `--pipeline` levels | `src/superclaude/commands/`, `skills/sc-issue-protocol/`, `agents/` |
| Claim tests | 10 test files (the 8 named for the claim path plus `tests/skills/test_clickup_claim.py` and `tests/skills/test_model_alias_policy.py`) | `tests/skills/`, `tests/commands/`, `tests/cli/` |
| Guard | `launch-level-guard.sh` 808 lines; `launch-job-identity.sh` 582; `launch-level-pre-push.sh` 208; `hooks.json` 192; 18 block words; 4 guard levels | `src/superclaude/hooks/` |
| Guard tests | 17 files, 24,388 lines, 921 test functions by plain `def test_` grep (920 strict): 14 table files plus 3 claim-side pin files (two of the three are also claim-side tests); the main file has 4,631 lines and 162 tests | `tests/hooks/`, `tests/cli/`, `tests/unit/`, `tests/core/`, `tests/skills/` |
| Coordinator text | `WORKER-CONTRACT.md` 339 lines; rules WC-2..WC-16 (15 rules; no WC-1, no WC-17); `tests/skills/test_worker_contract.py` 3,220 lines, 59 tests | `src/superclaude/core/`, `tests/skills/` |
| Removed package | 10 files, 1,597 lines, 10 verbs; 116 tests in 10 test files plus 1 registration test | `01e7a9e23^` |

PR 686 and the rewrite design are out of scope for this reference.

**Evidence limits.** The source is a snapshot of `origin/master` at 61ac2c2e6: it has no runtime state, no git history and no PR data. Therefore these statements stay [UNVERIFIED]: "never run live" and the PR numbers #447 and #448 (`docs/designs/issue-watcher.md:3`), the real reply shapes of `gh` and Orca (all `_assumed_shape` fixtures; no live-test record exists), the live observations OB-H1..3 and OB-CTX, the recorded FU-1 lines (`docs/designs/issue-pipeline-fu1.md:108-119`), the `enabled` value on any real machine, and whether anything runs `issue-watch once` on a schedule. Tests were read, not run. Of all components, only the L1 guard script was executed (44 sample payloads, sandbox HOME, observation run in the guard research). Removed code is labelled `@01e7a9e23^`. A pointer: Section 2.3 holds the ledger; Section 14 lists unwired, switched-off, retired and caller-less capabilities.

---

## 2. Architecture

Status words are only BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT and REMOVED. Every statement below is [CODE-VERIFIED] against the 61ac2c2e6 snapshot unless it carries another tag. Paths are repository-relative; removed code is labelled `@01e7a9e23^`.

### 2.1 Whole-pipeline diagram

```
 TRIGGERS   (a scheduler, dispatcher or zero-setup install is "not found in snapshot")
  [A] a person or external scheduler runs   superclaude issue-watch once [--dry-run]
  [B] a person types                        /sc:issue --claim <N> [--pipeline worktree|full|none]
        |                                                         |
        v                                                         |
 +--------------------------------------------+                   |       GITHUB  IronbellyOrg/IronClaude
 | 1 WATCHER  cli/issue_watch/                |                   |       reads : gh calls G1-G7 (watcher only)
 |   BUILT-OFF (enabled:false)                |-- reads G1..G7 ---|--->   writes: none from the watcher
 |   enabled gate -> setup check -> lock      |                   |
 |   -> DISABLED -> store -> login (G1)       |   LOCAL STATE     |
 |   -> origin -> sweep -> discovery (G2)     |-> <state_dir>/dispatch.json, lock, DISABLED,
 |   -> candidates, reads G3-G7 -> `pending`  |                   audit.jsonl, dry-run.json
 |   -> ONE launch per cycle -> commit        |                   |
 +---------------------|----------------------+                   |
                       |  <orca> agent launch --agent claude --worktree path:<abs worktree>
                       |     --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json
                       |  (this prompt has no [sc-launch:v1:<nonce>] marker: the guard never binds it)
                       v                                          v
 +-------------------------------------------------------------------------------------+
 | 2 CLAIM  /sc:issue --claim   BUILT-ON   waves 0-8 are prose run by the model       |
 |   W0 orca preflight | W1 scout (worker t3) | W3 assign + ClickUp | W4 check (t2/t1) |
 |   W6 post accuracy-check and claim comments (hidden markers)                       |
 |   --pipeline none : ends after W6; no worktree, no agent, no launch record        |
 |   worktree | full | full --submit : W7 worktree, W8 launch                         |
 +-----------|----------------------------------------|----------------------------------+
             | levels worktree/full/full --submit     | GITHUB WRITES (orchestrator only):
             v                                        |   gh issue edit --add-assignee @me
 +-----------------------------------------------+    |   gh issue comment | gh api -X PATCH
 | 3 orca_worktree.py (only code that calls orca)|    |   ClickUp assignee add (if env set)
 |  worktree: orca worktree create --no-parent   |    |   <-- the watcher re-reads the claim
 |            copy .dev/issues/<N>/ into it      |    |       marker comment through G4
 |  launch  : IR-4 preflight -> install_l2       |    +--------------------------------
 |            -> pending/<nonce> (level word)    |
 |            -> orca agent launch --prompt      |
 |               "[sc-launch:v1:<nonce>] Read     |
 |               .dev/issues/<N>/launch-prompt.md |
 |               and follow it." --json          |
 |            -> detect ccsession shim (warning) |
 +-------|-------------------------|-------------+
         |                         +--> <git-common-dir>/hooks/pre-push (+ data file)   = L2
         v
 +-------------------------------------------------------------------------------------+
 | 4 LAUNCHED AGENT (Orca terminal, ccsession-orca) reads launch-prompt.md level blocks |
 |   its first prompt carries the marker -> L1 guard binds pending/<nonce> -> sessions/<sid> |
 +--------------------------------------------|----------------------------------------+
                                              v
 5 GUARD HOOKS on every prompt and tool call of a bound session (Claude Code hooks.json):
     launch-level-guard.sh   UserPromptSubmit + PreToolUse: blocks implement / commit / push / submit by level;
                             G2 rule 2: `orchestration send|ask` allowed only with no --to
                               (matches the command word `orca` only; `orca-ide` is not constrained, Section 5.3, D-25);
                             a typed first line /sc:implement or /task at level worktree writes sessions/<sid>.ok
     launch-job-identity.sh  PreToolUse(Bash): wraps each Bash call so a git hook can name the actor
     pre-push (git, L2)      asks identity; refuses main/master pushes by governed or unknown actors

 NOT BUILT / REMOVED (see Section 14): hand-off from a `--pipeline none` claim to a started worker;
 coordinator release of a bound worker (REMOVED); a caller of `orca_worktree.py pending`; a scheduler.
```

### 2.2 Component relationship table

Watcher import rules are pinned by `tests/issue_watch/test_module_boundaries.py:241`.

| Component | Path | Role | Depends on | Depended on by |
|-----------|------|------|------------|----------------|
| cycle | `src/superclaude/cli/issue_watch/cycle.py` | config loader and validators (:34-483), one poll cycle `_Cycle` (:485-1222), status report and SLO reducer (:1225-1406) | runner, github, predicates, record, launch, audit | `src/superclaude/cli/issue_watch/cli.py` |
| github | `src/superclaude/cli/issue_watch/github.py` | the seven read-only `gh` calls, call budget, rate-limit handling | runner, predicates | `src/superclaude/cli/issue_watch/cycle.py` |
| record | `src/superclaude/cli/issue_watch/record.py` | `FileStore` for `dispatch.json`, flock, atomic write, DISABLED check, dry-run shadow, entry transitions | predicates; `swarm.atomic` inside functions only | `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/cli.py` |
| launch | `src/superclaude/cli/issue_watch/launch.py` | the one fixed `orca agent launch`, Orca discovery, origin check, reply mapping | runner; `_ORCA_CLIS` at `src/superclaude/cli/install_user_setup.py:36` | `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/cli.py` |
| predicates | `src/superclaude/cli/issue_watch/predicates.py` | pure eligibility checks (approval replay, owner, edits, project, marker window) | nothing from `superclaude` | cycle, record, github |
| audit | `src/superclaude/cli/issue_watch/audit.py` | `audit.jsonl` writer, reason table (:26-102), rotation | import table pinned at `tests/issue_watch/test_module_boundaries.py:241` | cycle, cli |
| cli | `src/superclaude/cli/issue_watch/cli.py` | Click group `issue-watch`, five verbs, exit-code mapping | cycle, record, audit, launch, runner, click | `src/superclaude/cli/main.py:577-579` |
| runner | `src/superclaude/cli/issue_watch/runner.py` | the only module that imports `subprocess` (`shell=False`) | none | github, launch, cli |
| command front | `src/superclaude/commands/issue.md` | flags, STOP rules, Activation (:104-110) | skill `sc-issue-protocol` | a person; the watcher prompt |
| orchestrator skill | `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/{claim,create,chains,tiers,labels}.md` | waves 0-8 run by the model; level rule at `src/superclaude/skills/sc-issue-protocol/refs/claim.md:81` | workers, three scripts, templates, `Skill sc-recommend` | `issue.md` |
| tier workers | `src/superclaude/agents/issue-worker-t{1,2,3}.md` | read-only lookups and drafts, write only under `.dev/issues/`; `model:` on line 6 (tier1b, tier2, tier2b) | `gh` reads, `git fetch` | SKILL.md waves 1 and 4 |
| origin script | `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` | resolves the repo from `origin` only | `git` | wave 0 |
| ClickUp script | `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py` | at most one ClickUp assignee add, only when env is set | ClickUp API | wave 3 |
| worktree script | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | preflight, worktree, prompt, launch, pending; the only code that calls `orca` for the claim | `orca`, `git`, `~/.claude/hooks/*`, launch-prompt template | waves 0, 5, 7, 8 |
| templates | `src/superclaude/skills/sc-issue-protocol/templates/` | posted comment bodies, summaries, level blocks (`src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:11,20,25,28`) | none | SKILL.md; marker pinned by `tests/issue_watch/test_marker_contract.py:28-48` |
| L1 guard | `src/superclaude/hooks/scripts/launch-level-guard.sh` | binds a session to a level, blocks action classes, G2 rule 2 | `jq`; reads only `HOME`; store `~/.claude/state/launch-level/` | Claude Code events (`src/superclaude/hooks/hooks.json:63-71,115-124`); claim IR-4 preflight |
| job identity | `src/superclaude/hooks/scripts/launch-job-identity.sh` | wraps governed Bash calls; `identify` names the actor of a process | `uv`, Linux `/proc` | `src/superclaude/hooks/hooks.json:125-134`; L2 hook |
| L2 hook | `src/superclaude/hooks/scripts/launch-level-pre-push.sh` | git `pre-push` refusal for main/master | identity `identify` (:65) | git; installed by `orca_worktree.py` `install_l2` |
| registration | `src/superclaude/hooks/hooks.json`, `src/superclaude/cli/install_hooks.py` | merge registrations into `~/.claude/settings.json`; copy scripts (skip if present unless `force`) | `superclaude install` and `update` | `src/superclaude/cli/main.py:219, 412` |
| ccsession | `src/superclaude/skills/ccsession-tag/ccsession-orca`, `src/superclaude/cli/install_ccsession.py` | Orca's Claude command; carries NO launch level | none | detected, never required, by the claim (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1802-1811`) |
| coordinator text | `src/superclaude/core/WORKER-CONTRACT.md` | general coordinator and worker rules; no issue-pipeline duties | none | coordinator sessions (instruction text only) |

### 2.3 Live-versus-switched-off ledger

"BUILT-ON" means the code exists and is wired into a path that runs in a normal install; it does not say any machine has run it. Rows 1 to 8 are the eight pieces; rows 1b, 7b and 9 to 18 are additional rows. In row 12 the words "enabled:false" label a switched-off constant, not the `enabled` config key.

| Piece | Status word | Evidence (path:line) | Trigger | Writes to GitHub | Note |
|-------|-------------|----------------------|---------|------------------|------|
| 1 Watcher, real cycle (`issue-watch once`) | BUILT-OFF (enabled:false) | `src/superclaude/cli/issue_watch/cycle.py:228` (default `False`); `src/superclaude/cli/issue_watch/cycle.py:685-686` (`not_enabled`, exit 0); `src/superclaude/cli/main.py:577-579` | only a person or an external scheduler running `once`; none exists in the snapshot | none; seven read-only `gh` calls (`src/superclaude/cli/issue_watch/github.py:175-262`); its one outward effect is one `orca agent launch` | no config file ships; a real machine's `enabled` value is [UNVERIFIED]; the `DISABLED` file is a second kill switch and `once --dry-run` ignores `enabled` |
| 1b Watcher verbs and `once --dry-run` | BUILT-ON | `src/superclaude/cli/issue_watch/cli.py:111-137` (`once`), `:164-182` (`status`), `:185-198` (`check-config`), `:201-214` (`init-state`), `:282-348` (`reset`); `src/superclaude/cli/issue_watch/cycle.py:685` (dry-run skips the gate), `:1029-1035` (dry-run stops before any probe or launch); `src/superclaude/cli/issue_watch/cycle.py:712, 1063` (`DISABLED` file) | an operator by hand | none | the audit writer is not behind the gate (`src/superclaude/cli/issue_watch/cycle.py:691-693`) |
| 2 Claim (`/sc:issue --claim`) | BUILT-ON | `src/superclaude/commands/issue.md:104-110`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:74`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:48, 91-92` | a person typing it; the watcher prompt (`src/superclaude/cli/issue_watch/launch.py:84-92`) | `gh issue edit <N> --repo <R> --add-assignee @me`; `gh issue comment` or `gh api -X PATCH` on two marked comments; ClickUp assignee add (`src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:232-237`) | waves are prose run by the model, no program orders them; ClickUp runs only when its env is set (`src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:164-169`); workers are read-only; labels, type and fields are never written |
| 3 L1 guard | BUILT-ON | `src/superclaude/hooks/hooks.json:63-71, 115-124`; `src/superclaude/hooks/scripts/launch-level-guard.sh:4-6, 257, 391` | Claude Code `UserPromptSubmit` and `PreToolUse` events | none | governs only a session a claim launch bound; every other session exits 0 (fail-open), a bound one fails closed; its orca checks (G2 rule 2) recognise the command word `orca` only, not `orca-ide` (row 6) |
| 4 L2 pre-push hook | BUILT-ON | `src/superclaude/hooks/scripts/launch-level-pre-push.sh:4-5, 187-208`; `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1386-1442, 1754`; `src/superclaude/cli/install_hooks.py:96` | git `pre-push` in a clone where `install_l2` placed it | none | installed by the claim at launch, not registered in `hooks.json`; refuses only `refs/heads/main` and `refs/heads/master` (`src/superclaude/hooks/scripts/launch-level-pre-push.sh:17`); only a claim at `worktree` or `full` installs it |
| 5 Job identity | BUILT-ON | `src/superclaude/hooks/hooks.json:125-134`; `src/superclaude/hooks/scripts/launch-job-identity.sh:430-505, 541-572` | Claude Code `PreToolUse` for `Bash`; `identify` called by the L2 hook | none | needs Linux and `uv`; fails closed for a bound session; not a sandbox (`src/superclaude/hooks/scripts/launch-job-identity.sh:2`) |
| 6 G2 rule 2 | BUILT-ON | `src/superclaude/hooks/scripts/launch-level-guard.sh:485, 496-537`; `src/superclaude/core/WORKER-CONTRACT.md:66`; `tests/hooks/test_launch_level_guard_worker.py:74, 187` | a bound session's Bash call `orca orchestration send` or `ask` | none | applies only to sessions bound by a claim marker; nothing binds a coordinator-started worker (rows 10 and 18); recognises the command word `orca` only: `orca-ide` is not constrained (observed exit 0), see Section 5.3 and Section 14 D-25 |
| 7 Coordinator text, issue-pipeline duties | NOT BUILT | `src/superclaude/core/WORKER-CONTRACT.md` (full read: no "Issue pipeline duties", no "WC-17", no "watcher", no "COORD-"); issue-related lines only at `:23, 57, 66, 242-243`; `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268` | none found in snapshot | none | who starts a worker after a claim is not defined in any file read; the hand-off prose at `src/superclaude/commands/issue.md:85` has no code behind it |
| 7b Coordinator text, general rules | BUILT-ON | `src/superclaude/core/WORKER-CONTRACT.md:31-64, 72, 287`; `tests/skills/test_worker_contract.py:876-878` | read by a person-opened coordinator session; no code loads it (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:186`, [UNVERIFIED]) | none from the text; contract `:243` names issue comments as coordinator actions | rules WC-2..WC-16 are instruction text pinned only as text |
| 8 Removed package `issue_pipeline` | REMOVED | `src/superclaude/cli/issue_pipeline/` absent; present at `01e7a9e23^`; `CHANGELOG.md:17` (records the removal); old `src/superclaude/cli/main.py:581, 583` @01e7a9e23^ | none in code; ran only if a coordinator or worker session followed the removed contract text | none from its code: GitHub reads only, local rows and one local `.ok` file; the plan reply and label mirror were contract text, no command line | commit 01e7a9e23, PR #682, dated 2026-11-19 18:02 -0600 (2026-11-20 00:02 UTC); its message says nothing ran this code [CODE-VERIFIED as text, runtime [UNVERIFIED]] |
| 9 G2 rule 1 / route A (`release-worker`) | REMOVED | `src/superclaude/hooks/scripts/launch-level-guard.sh:496-497` (comment: retired); old TAMPER case at `src/superclaude/hooks/scripts/launch-level-guard.sh:441-444` @01e7a9e23^; zero hits for `release-worker` in `src`, `tests`, `plugins` | none | none | the only `.ok` writer left is the guard's typed-prompt branch (`src/superclaude/hooks/scripts/launch-level-guard.sh:347-359`); route B (signed file) is NOT BUILT (zero hits for signature terms) |
| 10 Caller of `orca_worktree.py pending` | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON | verb at `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523, 1886-1893`; only test callers `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498` | no trigger found in snapshot | none | the verb is BUILT-ON, the caller is absent; the launch-level guard design says it does not govern a coordinator-started worker (`docs/designs/sc-issue-launch-level-hook.md:23`) |
| 11 IR-3 `pipeline.json` | NOT BUILT | zero hits for `pipeline.json` in `src` and `plugins`; `docs/designs/sc-issue-claim-pipeline-flag.md:58` (documentation only) | none | none | the level travels by files under `~/.claude/state/launch-level/` only |
| 12 IR-7 refusal (L2 not owned) | BUILT-OFF (enabled:false) | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:822` (`IR7_REFUSE = False`), `:1757-1758`; `tests/skills/test_issue_l2_install.py:639` | a claim launch at `worktree` or `full` | none | the switch is a constant, not the `enabled` key; a missing L2 hook only adds `W-L2-ABSENT` |
| 12b IR-4 enforcement preflight | BUILT-ON | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:955-1045, 1730-1747` | a claim launch | none | refuses the launch with `W-ENFORCEMENT-ABSENT`; verifies the claim process only |
| 13 OB-H1..3 and OB-CTX live observations; ship gate | NOT BUILT | `tests/hooks/test_launch_level_observations.py:79-84` (every parametrised case skips); `src/superclaude/commands/issue.md:16`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:136` | none | none | the gate is prose; no code reads it; whether the observations passed is [UNVERIFIED] |
| 14 Scheduler for `issue-watch once` | NOT BUILT | `src/superclaude/cli/issue_watch/cli.py:98` ("Run `once` from a timer"); no timer, cron, systemd, launchd, GitHub Action or Orca automation artefact in the snapshot; `docs/designs/issue-watcher-setup.md:288` says this work installs none | none | none | deferred behind the live test by the design (`docs/designs/issue-watcher.md:33, 861`) |
| 15 Dispatcher, `COORD-<RepoName>` coordinator worktree, zero-setup install | NOT BUILT | not found in snapshot: `COORD-` has 0 hits outside `.git` and `.dev`; `dispatcher` hits are unrelated (swarm, Orca shim) | none | none | "grant row" exists only as prose (`src/superclaude/core/WORKER-CONTRACT.md:57`, `docs/designs/issue-pipeline-fu1.md:24, 26`); no store, verb or schema |
| 16 Live-test record | NOT BUILT | `docs/designs/issue-watcher-live-test.md` is absent; `docs/designs/issue-watcher.md:33` (the owner writes it); `tests/issue_watch/test_github.py:575-583` (fixtures still assumed) | none | none | gates enabling the watcher by design; no code checks the gate |
| 17 Hand-off from a `--pipeline none` claim to a worker | NOT BUILT | `src/superclaude/commands/issue.md:85`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:140`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:96` (prose); no Python in `src` calls `worker-start` | none found in snapshot | none | the removed duties are row 8; see Section 14 |
| 18 Binding of coordinator-started workers | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON | the only marker generator was `brief.build` @01e7a9e23^ (old `src/superclaude/cli/issue_pipeline/brief.py:71-73`); the contract brief template has no marker slot | none | none | G2 rule 2 (row 6) therefore runs only for claim-launched sessions |

### 2.4 Integration map

| # | Hand-off | Mechanism | Evidence (path:line) | Status word |
|---|----------|-----------|----------------------|-------------|
| 1 | watcher -> claim | `orca agent launch ... --prompt "/sc:issue --claim <N> --pipeline none" --json` in the operator's existing worktree; the level `none` is hard-coded; the claim ends after wave 6 | `src/superclaude/cli/issue_watch/launch.py:33, 84-92, 95-116`; `src/superclaude/commands/issue.md:48`; `src/superclaude/skills/sc-issue-protocol/SKILL.md:90`; pinned at `tests/issue_watch/test_launch.py:75` and `tests/issue_watch/test_security_invariants.py:936` | BUILT-OFF (enabled:false) |
| 2 | claim -> watcher (return path) | the claim comment ends with a hidden marker; the watcher reads it through G4 and moves the entry to `claimed` | `src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md:23`; `src/superclaude/cli/issue_watch/github.py:223-225`; `src/superclaude/cli/issue_watch/cycle.py:848-865, 896-899`; `tests/issue_watch/test_marker_contract.py:28-48` | BUILT-OFF (enabled:false) |
| 3 | claim -> guard | files only: `pending/<nonce>` holds one level word; the launch prompt carries `[sc-launch:v1:<nonce>]`; the guard renames it to `sessions/<sid>` on the first prompt; only levels `worktree`, `full`, `full --submit` | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1488-1512, 1759-1761, 1776-1779`; `src/superclaude/hooks/scripts/launch-level-guard.sh:318, 372-375` | BUILT-ON |
| 4 | claim -> L2 hook | `install_l2` hard-links the hook into `<git-common-dir>/hooks/pre-push` with a data file, after the IR-4 preflight; an existing hook is never replaced | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1386-1442, 1754`; template copied by `src/superclaude/cli/install_hooks.py:96` | BUILT-ON |
| 5 | install -> guard registration | `superclaude install` and `update` merge `hooks.json` into `~/.claude/settings.json`; the claim refuses to launch if the guard is absent, stale or not registered | `src/superclaude/cli/main.py:219, 412`; `src/superclaude/hooks/hooks.json:63-71, 115-134`; `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:955-1045, 1730-1747` | BUILT-ON |
| 6 | guard -> orchestration commands (G2 rule 2) | a bound session may run `orca orchestration send` or `ask` only as one plain call with no `--to`; every other `orca` verb off the allow-list is blocked, except a short help call (`<verb words> --help` or `-h`, at most four words counting from `orca`, no glob character; `orca list --help` and `orca agent launch -h` pass), and only for the command word `orca`: `orca-ide` is not constrained (observed exit 0), see Section 5.3 and Section 14 D-25 | `src/superclaude/hooks/scripts/launch-level-guard.sh:457, 480-491, 496-537`; help call `launch-level-guard.sh:487-490`, pinned by `tests/hooks/test_launch_level_guard_worker.py:226-230`; `src/superclaude/core/WORKER-CONTRACT.md:66` | BUILT-ON |
| 7 | L2 hook -> job identity | the pre-push hook runs `identify $$` under a pinned `HOME` and `uv` directory to learn whether the pusher is governed | `src/superclaude/hooks/scripts/launch-level-pre-push.sh:52-101`; `src/superclaude/hooks/scripts/launch-job-identity.sh:215-260` | BUILT-ON |
| 8 | claim -> ccsession shim | detection only, by screen text or tab title; the shim carries no level; absence is a warning, not a refusal | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1802-1811`; zero hits for `launch-level` under `src/superclaude/skills/ccsession-tag` | BUILT-ON |
| 9 | `--pipeline none` claim -> coordinator-started worker | prose only (run `orca_worktree.py worktree`, then `worker-start`); no code and no contract text | `src/superclaude/commands/issue.md:85`; `src/superclaude/core/WORKER-CONTRACT.md` (no such rule) | NOT BUILT |
| 10 | coordinator -> release of a bound worker | `release-worker` wrote `sessions/<sid>.ok`; the verb and guard rule 1 are gone | `src/superclaude/hooks/scripts/launch-level-guard.sh:496-497`; old `src/superclaude/cli/issue_pipeline/release.py:57-62` @01e7a9e23^ | REMOVED |

**Reading the map.** A watcher-launched session (hand-off 1) carries no marker, so the guard hand-offs do not apply to it: the guard exits 0 for a session with no marker and no bound record (`src/superclaude/hooks/scripts/launch-level-guard.sh:363-365`), and the watcher prompt must fully match a pattern with no marker (`src/superclaude/cli/issue_watch/launch.py:33`). Hand-offs 3, 4, 6 and 7 apply only to a session bound through a claim a person typed at `worktree`, `full` or `full --submit`; hand-off 5 is the install step they all rely on.

---

## 3. Directory Structure

Paths are repository-relative against snapshot 61ac2c2e6. Shorthand used in Sections 3, 4 and 6: `P/` = `src/superclaude/cli/issue_watch/`, `SK/` = `src/superclaude/skills/sc-issue-protocol/`, `H/` = `src/superclaude/hooks/scripts/`. Removed code is cited as `@01e7a9e23^` (removal commit 01e7a9e23, 2026-11-19 18:02 -0600 = 2026-11-20 00:02 UTC, PR #682).

```
src/superclaude/
├── cli/
│   ├── issue_watch/                  # the poller package: nine modules, no sub-package (BUILT-OFF (enabled:false) for real cycles)
│   │   ├── __init__.py               # empty
│   │   ├── runner.py                 # SubprocessRunner: the only module that imports subprocess
│   │   ├── predicates.py             # pure rules: approval, owner, edits, project, claim-marker window, order
│   │   ├── audit.py                  # REASON_TABLE, audit-line builders, AuditLog writer, stderr fallback
│   │   ├── github.py                 # G1-G7 gh argv builders, classify, CallBudget, paged reads
│   │   ├── record.py                 # FileStore, dispatch.json schema, transitions, flock, init_state, dry-run shadow
│   │   ├── launch.py                 # launch_argv, find_orca, check_origin, OrcaLauncher, outcome_of
│   │   ├── cycle.py                  # config loader, validate_approvers, run_cycle, status_report, slo_numbers
│   │   └── cli.py                    # click group issue-watch: once, status, check-config, init-state, reset
│   ├── main.py                       # registers issue-watch at lines 577-579
│   ├── install_hooks.py              # copies hook scripts to ~/.claude/hooks, merges hooks.json into settings.json
│   ├── install_ccsession.py          # wires ccsession and ccsession-orca into ~/.local/bin
│   └── issue_pipeline/               # REMOVED @01e7a9e23^ (10 files; see Appendix B)
├── commands/issue.md                 # /sc:issue front: --claim, --create (117 lines)
├── skills/
│   ├── sc-issue-protocol/            # the claim and create protocol, run by the model
│   │   ├── SKILL.md
│   │   ├── refs/                     # claim.md, create.md, labels.md, tiers.md, chains.md
│   │   ├── scripts/                  # origin_repo.py, clickup_claim.py, orca_worktree.py
│   │   └── templates/                # 15 files (claim-comment.md, launch-prompt.md, issue-summary.md ...)
│   └── ccsession-tag/                # ccsession, ccsession-orca, ccsession-models.json, hooks/session-start.sh, session-name.sh
├── agents/issue-worker-t1.md, -t2.md, -t3.md   # tier-pinned read-only claim and create workers
├── hooks/
│   ├── hooks.json                    # registrations (launch-level guard twice, job identity once)
│   └── scripts/                      # launch-level-guard.sh, launch-job-identity.sh, launch-level-pre-push.sh, require-orca-worktree-agent.sh
└── core/WORKER-CONTRACT.md           # worker and coordinator rules (WC-2 to WC-16)
plugins/superclaude/hooks/            # mirror: hooks.json (differs) and the three launch-level scripts (byte-identical)
docs/designs/                         # issue-watcher.md (942), issue-watcher-setup.md (706), sc-issue-command.md (509),
                                      # sc-issue-claim-pipeline-flag.md (470), sc-issue-launch-level-hook.md (627),
                                      # issue-pipeline-guard-g2.md (51), issue-pipeline-guard-g2-no-to.md (57), issue-pipeline-fu1.md (119)
tests/
├── issue_watch/                      # 19 test files, conftest.py, fixtures/_assumed_shape/ (19 JSON files)
├── hooks/                            # test_launch_level_guard*.py (5), test_launch_job_identity.py, test_launch_level_pre_push*.py (2),
│                                     # test_launch_level_observations.py, test_require_orca_worktree_agent*.py (2)
├── skills/                           # test_issue_protocol, _orca_worktree, _repo_resolution, _worker_agents, _t1_fallback, _l2_install,
│                                     # test_clickup_claim, test_model_alias_policy, test_worker_contract
├── commands/ and cli/                # commands/test_issue_command.py, cli/test_issue_body_templates.py, cli/test_install_hooks.py
└── unit/ and core/                   # unit/test_install_ccsession.py, unit/test_ccsession_tag.py, unit/test_ccsession_tiers.py,
                                      # core/test_orca_session_launch_guidance.py
```

### 3.1 Key file inventory

| Path | Lines | Purpose |
|------|-------|---------|
| `P/cycle.py` | 1406 | Config loader, approvers-file check, one poll cycle, `status_report`, `slo_numbers` |
| `P/github.py` | 960 | The seven read-only `gh` calls, reply classification, call budget |
| `P/record.py` | 865 | `dispatch.json` store, state machine, flock, `init_state`, dry-run shadow file |
| `P/audit.py` | 404 | Closed reason vocabulary, audit lines, rotation, stderr fallback |
| `P/launch.py` | 370 | Orca discovery, origin check, the one `orca agent launch` argv |
| `P/cli.py` | 348 | Five operator verbs, exit-code mapping |
| `P/predicates.py` | 312 | Pure eligibility predicates (no I/O, no clock) |
| `P/runner.py` | 130 | Subprocess wrapper (`shell=False`, timeout, stderr cap) |
| `src/superclaude/commands/issue.md` | 117 | `/sc:issue` flags, STOP rules, activation of the skill |
| `SK/SKILL.md` | 197 | Orchestrator protocol: waves, worker spawn rules, return contract, error table |
| `SK/refs/claim.md` | 150 | Claim waves 0 to 8, level rule, remedy lines |
| `SK/refs/create.md` / `labels.md` / `tiers.md` / `chains.md` | 99 / 67 / 58 / 40 | Create path, label and field rules, tier pins and fallback, next-step chains |
| `SK/scripts/orca_worktree.py` | 1906 | Only caller of `orca` for the claim: preflight, worktree, prompt, launch, pending, IR-4, L2 install |
| `SK/scripts/clickup_claim.py` | 270 | ClickUp lookup and at most one assignee add |
| `SK/scripts/origin_repo.py` | 195 | Resolves repo and issue number from `origin` only |
| `SK/templates/launch-prompt.md` / `claim-comment.md` | 34 / 23 | Launch prompt blocks; the posted claim comment ending `<!-- sc:issue:claim -->` |
| `src/superclaude/agents/issue-worker-t1.md` / `t2` / `t3` | 35 each | Workers pinned to `claude-gw-tier1b` / `tier2` / `tier2b` (frontmatter line 6) |
| `H/launch-level-guard.sh` | 808 | L1 guard: binds sessions, enforces the level grid, exit 0 or 2 only |
| `H/launch-job-identity.sh` | 582 | Rewrites governed Bash calls under a supervisor; `identify` answers governed, ordinary or unknown |
| `H/launch-level-pre-push.sh` | 208 | L2 git pre-push hook for pushes to main or master |
| `src/superclaude/hooks/hooks.json` | 192 | Hook registrations (plugin copy: 154 lines) |
| `src/superclaude/cli/install_hooks.py` / `install_ccsession.py` | 614 / 161 | Hook installer and ccsession wiring |
| `src/superclaude/skills/ccsession-tag/ccsession-orca` | 263 | Orca's Claude command wrapper; carries no launch level |
| `src/superclaude/core/WORKER-CONTRACT.md` | 339 | Coordinator and worker rules; no issue-pipeline duties in this snapshot |

---

## 4. Data Flow

Shorthand as in Section 3. Status words: BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. The pipeline has three code-backed parts that touch each other only through GitHub comments and files: the watcher (reads GitHub, starts one Orca session), the claim (`/sc:issue --claim`, writes the GitHub comments) and the guard stack (reads files under `~/.claude/state/launch-level/`).

```
 [no trigger found in snapshot]                      person types /sc:issue --claim N [--pipeline L]
            |  (a person or an outside scheduler)                       |
            v                                                           |
  superclaude issue-watch once                                          |
  BUILT-OFF (enabled:false)                                             |
   G1..G7 gh reads (no GitHub write)                                    |
            | one orca agent launch --prompt "/sc:issue --claim N --pipeline none"
            +---------------------------------------------------------->+
                                                                        v
                       claim session: assign + accuracy-check comment + claim comment (marker)
                                   |                                    |
        watcher reads marker (G4)  |            level worktree|full: worktree + launch
        next cycle -> entry claimed|                                    v
                                                      pending/<nonce> -> L1 guard binds sessions/<sid>
```

### 4.1 Watcher cycle (`superclaude issue-watch once`)

Numbered steps of `_Cycle.run` in `P/cycle.py`; "G" ids are the read-only `gh` calls of Section 4.5. Counters: shared = G1 and G2 only; per-issue non-reserved reads stop at 32 calls; the reserved re-read may use calls up to 35.

| # | Step (`P/cycle.py` lines) | GitHub read and budget | State write | On failure (word, exit) |
|---|---|---|---|---|
| 0 | `enabled` gate (685-686) | none | one cycle line | `not_enabled`, 0; dry-run ignores the gate |
| 1 | `validate_setup`: worktree is a directory, approvers file valid (687-693; 371-377) | none | one cycle line on failure | `worktree_invalid`, `approvers_invalid`, 2 |
| 2 | Lock: non-blocking flock on `state_dir/lock` (694-702; `P/record.py:380-419`) | none | none (no rotation on failure) | `lock_held`, 75; `lock_missing`, `lock_invalid`, 6 |
| 3 | `DISABLED` kill switch (712-713) | none | none, no health stamp | `disabled`, 0 |
| 4 | Load `dispatch.json` (739-750) | none | migrated store saved at once, real cycle only (746-747) | `store_missing`, `store_invalid`, 6; `rate_limited`, 5 while `now < next_permitted_at` |
| 5 | Login step (752-775) | G1, shared call 1 | `clock_skew_s` on the cycle line; warning `clock_skew` above 60 s (`SKEW_WARN_S`, 44, 774) | `gh_*`, `login_invalid`, 3; `account_id_mismatch`, 2; `rate_limited` / `rate_limit_clamped`, 5 |
| 6 | Origin check, git only (716-722) | none (not budgeted) | none | `origin_mismatch`, 2 |
| 7 | Sweep (777-792; `P/record.py:627-651`) | none | `pending` becomes `abandoned` (`pending_orphan`); `launched` past its lease becomes `abandoned` (`claim_not_observed`) | none |
| 8 | Discovery (794-808) | G2, shared call 2 | warning `discovery_count` at 80 or more | `truncated`, `discovery_duplicate`, 4; rate limit, 5 |
| 9 | Order: never-examined issues first, then oldest `considered`; first 10 (725-737; `P/predicates.py:299-312`) | none | dry-run shadow load only | none |
| 10 | Candidate loop, gates E1 to E14 in `_examine` (812-834, 915-961; detail in Section 5.1) | per-issue reads in order G4 comments, G3 events, G5 edits, G6 project items (cap 32); local gates cost no call | one decision line per examined candidate; `considered` stamp except `budget_exhausted` | skip words, 0; missing scope, `project_read_failed`, 3; rate limit, `rate_limit_clamped`, 5 |
| 11 | Launch step `_launch` (1026-1112), in order: dry-run return (1029-1035), probe (`find_orca`), prompt, re-read `_revalidate` (979-1016), day cap, DISABLED, cut-off, origin, `pending` save, `orca agent launch` | the re-read: G7, G3', G6' on the reserved calls | `pending` saved and fsynced before the launch call (1091-1092); outcome `launched` / `unknown` / `abandoned` held for the commit | `orca_not_found`, `origin_mismatch`, 2; `revalidation_failed`, `disabled_mid_cycle`, 0; `revalidation_transient`, `launch_unknown`, `spawn_error`, 7 |
| 12 | Commit (1116-1144) | none | one save of `dispatch.json` (real) or `dry-run.json` (dry-run); health stamp only with no stop reason and exit 0 | `state_dir_unwritable`, 6 |
| 13 | Conclude (1176-1211) | none | decision lines, then one cycle line, to `audit.jsonl`; rotation only with the lock held | write failure: stderr fallback line only |

```
enabled? -> setup -> lock -> DISABLED? -> load -> G1 -> origin -> sweep -> G2 -> order
                                                                              |
audit.jsonl <- conclude <- commit <- launch step <- re-read G7,G3',G6' <- candidates G4,G3,G5,G6
```

- One launch per cycle: the candidate that enters the launch step sets `launching`, then `halt` ends the loop after any launch-step outcome (`P/cycle.py:1028, 833-834`); later candidates get no read and no decision line.
- A dry-run runs steps 1 to 10 and returns at the top of step 11 (`P/cycle.py:1029-1035`): no probe, re-read, `pending` write or Orca call, so it cannot show a launch-step problem.
- [CODE-CONTRADICTED] `docs/designs/issue-watcher.md:331, 362, 621` say `find_orca` is cached per cycle (code caches nothing, `P/launch.py:6, 177`) and `:360` says entry-state candidates cost 0 calls (they read G4 first, `P/cycle.py:922-935`). Code is stronger evidence.

### 4.2 Claim flow (`/sc:issue --claim`) by wave and actor

"Orchestrator" is the Claude session that invoked the skill, not a program; only the three helper scripts are code (`SK/SKILL.md:35`). Workers are read-only and write only under `.dev/issues/` (agent files line 28 and 30). Every GitHub, ClickUp and Orca write is the orchestrator's.

| Wave | What happens | Actor | Writes outside `.dev/issues/` | Evidence |
|------|--------------|-------|-------------------------------|----------|
| 0 | `origin_repo.py --claim`, `gh auth status`, `orca_worktree.py preflight` (runs even for `--pipeline none`), default branch lookup, create `.dev/issues/<N>/` | orchestrator | none | `SK/refs/claim.md:11-21` |
| 1 | Lookup, writes `scout.md` | worker t3 | none | `SK/refs/claim.md:23-34` |
| 2 | Edge cases from `scout.md` (closed issue, assigned to another login: STOP, no writes) | orchestrator | none | `SK/refs/claim.md:36-44` |
| 3 | Assign on GitHub, then ClickUp script | orchestrator | GitHub assignee; one ClickUp assignee add | `SK/refs/claim.md:46-51` |
| 4 | Accuracy check and summary (analysis if out of date) | worker t2, or t1 when scout sizes `complex` (t1 falls back to t2 once) | none | `SK/refs/claim.md:53-63`; `SK/refs/tiers.md:34-42` |
| 5 | `Skill sc-recommend`, `next-steps.md`, resolve level, render `launch-prompt.md` | orchestrator | none | `SK/refs/claim.md:75-84` |
| 6 | Post or edit the accuracy-check comment and the claim comment | orchestrator | two comments (marked, edited on re-run) | `SK/refs/claim.md:86-96` |
| 7 | Create or reuse the worktree `issue-<N>` (no agent), copy `.dev/issues/<N>/`, close the first plain tab | orchestrator runs `orca_worktree.py worktree` | none on GitHub | `SK/refs/claim.md:98-115`; `SK/scripts/orca_worktree.py:625-738` |
| 8 | Launch an agent in the worktree (flow in 4.3) | orchestrator runs `orca_worktree.py launch` | none on GitHub | `SK/refs/claim.md:117-136`; `SK/scripts/orca_worktree.py:1696-1834` |

- `--pipeline none` (the only level the watcher sends) ends after Wave 6: no worktree, no agent, no `launch-prompt.md`, no `worktree.json` (`SK/refs/claim.md:94`; `src/superclaude/commands/issue.md:80`). The level is a code-fixed word in `P/launch.py:92`.
- The default level when `--pipeline` is omitted is a prose rule applied by the model (`SK/refs/claim.md:81`); no code computes it (NOT BUILT as code, prose rule only, D-20).

**Claim-to-watcher link: how a claim comment moves a watcher entry to `claimed`**

1. The watcher's launch step saves entry `pending`, runs `orca agent launch` with `/sc:issue --claim <N> --pipeline none` and records `launched` with a 60 minute lease (`P/cycle.py:1091-1105`; `P/record.py:580-596`).
2. The claim session assigns the issue (C1) and posts the claim comment whose last line is `<!-- sc:issue:claim -->` (`SK/templates/claim-comment.md:23`; `SK/refs/claim.md:92`), then ends.
3. Next cycle, for a `launched`, `unknown` or `abandoned`-with-`pending_at` entry, the watcher reads comments with G4; the comment body becomes a boolean through `MARKER_JQ` (`P/cycle.py:922-931`; `P/github.py:61-64`).
4. `_hit` accepts a marker only when its author is the watcher's own login and its time (the later of created and updated) is at or after `pending_at` minus 300 s (`SKEW_TOLERANCE_S`), or strictly after the current approval when there is no `pending_at` (`P/cycle.py:848-865`; `P/predicates.py:17, 274-296`).
5. `_claim` then calls `record.mark_claimed` (T-10 from `launched`/`unknown`/`abandoned`; T-11 with no entry; T-12 from `failed`); `claimed` is terminal (`P/cycle.py:896-899`; `P/record.py:654-686`). A decision line `claimed` is written.
6. With no marker by lease expiry, the sweep marks `abandoned` (`claim_not_observed`, T-9); `unknown` entries never leave on the lease and cost at least one G4 read per cycle (`P/record.py:638-643`; open question Q-02 in U-10, Section 14.3.1).
7. After the claim, nothing in the snapshot code starts a worker: no trigger found in snapshot. The hand-off text (`issue.md:85`, `SK/SKILL.md:140`, `SK/refs/claim.md:96`) is [UNVERIFIED - doc-only, no code confirmation]; the contract section that defined it is REMOVED (`CHANGELOG.md:17`; `src/superclaude/core/WORKER-CONTRACT.md` has no such section).

### 4.3 Launch-level binding flow (claim writes the pending file, the session binds it, hooks consult the session file)

Applies to claims at level `worktree` or `full` (with `--submit` the word is `full-submit`). The level travels only by files; the ccsession shim carries none (grep of `src/superclaude/skills/ccsession-tag` for launch-level terms: zero hits).

```
claim Wave 8: SK/scripts/orca_worktree.py launch                                   (cmd_launch :1696-1834)
  1 worktree record, already-launched check, stale-prompt check                    :1700-1724
  2 IR-4 enforcement preflight; fail -> W-ENFORCEMENT-ABSENT, no record, no agent  :1730-1747
  3 install_l2 then l2_status; not owned -> W-L2-ABSENT note, launch proceeds      :1754-1758
  4 publish_pending: ~/.claude/state/launch-level/pending/<32 hex nonce> = one word :1759-1761, :1488-1512
  5 orca agent launch --agent claude --worktree path:<wt> --surface terminal
        --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json   :1776-1779
  6 behind_ccsession: 5 tries x 2 s; absent -> W-LAUNCH-NOT-CCSESSION (warning only) :1802-1811
  7 record_launch -> worktree.json + <git dir>/sc-issue-launch-<N>.json              :1814
             |
             v   first UserPromptSubmit of the launched session
L1 guard (H/launch-level-guard.sh)
  match [sc-launch:v1:<32 hex>] (:318); mv pending/<nonce> -> sessions/.take-<sid> (:372-375);
  ln -> sessions/<sid> (hard link, first binding wins) (:299-313); bad word -> "degraded" = level W + note (:306)
             |
             v   every later UserPromptSubmit and PreToolUse
  sessions/<sid> exists (:257-273) -> governed: W | WA | F | FS; no record -> ordinary, exit 0 (:391)
  typed first line /sc:implement or /task at W -> sessions/<sid>.ok -> WA (:347-360)
  PreToolUse Bash: job-identity rewrites governed calls; writes requests/<token>, jobs/<kernel-sid>.json
  git push in a clone with hooks/pre-push: L2 asks `launch-job-identity.sh identify $$` -> governed | ordinary | unknown
```

- The pending record and the session record are one inode (hard link). A person releases a session by deleting `sessions/<sid>` and `sessions/<sid>.ok` (`H/launch-level-guard.sh:97`); nothing prunes `pending/` or `sessions/` (`docs/designs/sc-issue-launch-level-hook.md:627`).
- The watcher path binds nothing: `P/launch.py:33` fixes the prompt to `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` (no marker), and a `none` claim runs only `preflight` of the script. Coordinator-started workers get no marker either: `orca_worktree.py pending` has no production caller in the snapshot (only the test callers `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498`); the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`).
- [CODE-CONTRADICTED] `SK/refs/claim.md:125` says the L2 hook is installed "as the worktree's pre-push hook" and that IR-4 runs "before anything else"; code installs into the shared `<git-common-dir>/hooks/pre-push` (`SK/scripts/orca_worktree.py:1365, 1402`) and runs the record, already-launched and stale-prompt checks first (`:1700-1724`).
- [CODE-CONTRADICTED] `SK/templates/launch-prompt.md:23` names `/sc:task` as a releasing first line; the guard regex at `H/launch-level-guard.sh:347` accepts only `/sc:implement` and `/task`.
- The IR-7 refusal (turn a missing L2 hook into a refused launch) is BUILT-OFF (enabled:false): the switch is the constant `IR7_REFUSE = False`, not an `enabled` key (`SK/scripts/orca_worktree.py:822, 1757-1758`).

### 4.4 Trigger table: what starts each piece

| Piece | What starts it | Who or what runs it | Frequency | Evidence (path:line) | Live? |
|-------|----------------|---------------------|-----------|----------------------|-------|
| Watcher real cycle, `issue-watch once` | A run of `superclaude issue-watch once` | no trigger found in snapshot (docstring: "Run `once` from a timer"; intended every 5 minutes by a cron entry, follow-up FU-2, not installed) | none in code | `P/cli.py:98, 111-137`; `src/superclaude/cli/main.py:577-579`; `docs/designs/issue-watcher.md:15, 30, 861`; `docs/designs/issue-watcher-setup.md:288` | BUILT-OFF (enabled:false): `enabled` defaults false and a real cycle stops `not_enabled` (`P/cycle.py:228, 685-686`); no config file and no scheduler artefact ship |
| Watcher dry-run, `once --dry-run` | A person | the operator at a terminal | on demand | `P/cli.py:111-137`; `P/cycle.py:685` | BUILT-ON |
| `status`, `check-config`, `init-state`, `reset` | A person | the operator | on demand; `status` is meant for an outside alert check that does not exist (`docs/designs/issue-watcher-setup.md:557`) | `P/cli.py:164-348` | BUILT-ON |
| Watcher launch step (its only outward action) | First candidate to pass every gate in a real cycle | `OrcaLauncher.launch` inside `once` | at most once per cycle | `P/cycle.py:1099`; `P/launch.py:358-370` | BUILT-OFF (enabled:false) |
| Scheduler, dispatcher, `COORD-` coordinator worktree, zero-setup install for the issue pipeline | not found in snapshot (no cron, timer, workflow, Orca automation or such artefact; `COORD-` has zero hits) | not found in snapshot | none | negative searches in research files 01 to 03 and 06 | NOT BUILT |
| `/sc:issue --claim` typed by a person | The person types it | the orchestrating Claude session | on demand | `src/superclaude/commands/issue.md:25, 104-110` | BUILT-ON |
| `/sc:issue --claim <N> --pipeline none` launched by the watcher | The watcher launch step | an Orca terminal session in the configured worktree | at most one per cycle | `P/launch.py:33, 84-92` | BUILT-OFF (enabled:false) |
| Claim helpers `origin_repo.py`, `clickup_claim.py` | Wave 0 and Wave 3 of a claim | the orchestrator | per claim; ClickUp step skips without `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` | `SK/refs/claim.md:14, 50`; `SK/scripts/clickup_claim.py:164-169` | BUILT-ON |
| `orca_worktree.py preflight` | every claim, including `none` | the orchestrator | per claim | `SK/refs/claim.md:17`; `SK/scripts/orca_worktree.py:210-223` | BUILT-ON |
| `orca_worktree.py worktree`, `prompt`, `launch` | Waves 7, 5 and 8 at level `worktree` or `full` | the orchestrator | per claim | `SK/refs/claim.md:98-136` | BUILT-ON |
| `orca_worktree.py pending` | no trigger found in snapshot (verb exists; only callers are two tests) | none | none | `SK/scripts/orca_worktree.py:1515-1523, 1886-1893`; `tests/hooks/test_launch_level_guard_worker.py:287`; `tests/skills/test_issue_orca_worktree.py:2472-2498` | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON |
| Claim workers t1, t2, t3 | Waves 1 and 4 | Agent tool called by the orchestrator, `subagent_type` only | per claim | `SK/SKILL.md:54-64` | BUILT-ON |
| Coordinator hand-off after a `--pipeline none` claim | no trigger found in snapshot | none | none | `src/superclaude/commands/issue.md:85` (prose); no code or contract text (`src/superclaude/core/WORKER-CONTRACT.md`: zero hits for adopt, watcher, claim) | NOT BUILT |
| Coordinator loop rule WC-16 | A person-opened coordinator session reading the contract | no code runs it; "Phase 1 adds this duty, not a scheduler" | n/a | `src/superclaude/core/WORKER-CONTRACT.md:287-289` | BUILT-ON as instruction text only; not issue-specific |
| L1 guard | Claude Code events UserPromptSubmit and PreToolUse | the hook runner, if `superclaude install` merged hooks.json | every prompt and matched tool call | `src/superclaude/hooks/hooks.json:63-71, 115-124` | BUILT-ON |
| Job identity hook | PreToolUse with matcher `Bash`; its `identify` mode also from L2 | the hook runner; the L2 hook | every Bash call in a bound session | `src/superclaude/hooks/hooks.json:125-134`; `H/launch-level-pre-push.sh:65` | BUILT-ON |
| L2 pre-push hook | `git push` in a clone where `install_l2` placed `hooks/pre-push` | git; `install_l2` is called by `cmd_launch` | per push | `SK/scripts/orca_worktree.py:1754`; `H/launch-level-pre-push.sh:187-208` | BUILT-ON, placed only by a claim launch |
| `install_hooks`, `wire_ccsession` | A person runs `superclaude install` or `update` | the installer | on demand | `src/superclaude/cli/main.py:219, 412, 211, 406`; `src/superclaude/cli/eval/hook_adapter.py:230` | BUILT-ON |
| `ccsession-orca` | Orca runs it as the Claude command; the claim reaches it through `orca agent launch --agent claude` | Orca | per launched session | `src/superclaude/skills/ccsession-tag/ccsession-orca` header lines 2-12; `SK/scripts/orca_worktree.py:1777` | BUILT-ON (the claim only detects it) |
| IR-7 refusal of a launch | `cmd_launch` when L2 is not owned | the claim script | per launch | `SK/scripts/orca_worktree.py:822, 1757-1758` | BUILT-OFF (enabled:false), constant `IR7_REFUSE = False` |
| SLO reducer `slo_numbers` | no trigger found in snapshot (only an owner-run snippet) | none | none | `P/cycle.py:1359`; `docs/designs/issue-watcher-setup.md:457-476` | NOT BUILT as an operator surface (function exists, tested only) |
| Removed `issue-pipeline` verbs, WC-17, guard rule G2.1 | a coordinator following the old contract text | none (code deleted) | none | `CHANGELOG.md:17` (records the removal); commit 01e7a9e23 (PR #682) | REMOVED |

### 4.5 Writes to GitHub, per piece (exact commands)

`<R>` is the repo parsed from `origin` by `origin_repo.py` (the fork when `origin` is the fork); `<D>` is `.dev/issues/<N>/`. Every `gh` write of the claim passes `--repo <R>` (`SK/SKILL.md:72-74`).

**Watcher: every `gh` call is a read and the watcher writes no GitHub state.** Evidence: the only `"gh"` argv literals are five lines in `P/github.py` (177, 183, 204, 231, 255); `P/cycle.py` has no `gh`, `git`, `orca` or `subprocess` literal; the REST argv carry `--method GET` (`P/github.py:206-207, 257-258`); the GraphQL calls travel as HTTP POST but their constants hold queries only (`P/github.py:107-108`; pinned by `tests/issue_watch/test_security_invariants.py:894, 912`).

| Piece | Command (exact) | Actor | read / write | File:line | When |
|-------|-----------------|-------|--------------|-----------|------|
| Watcher G1 | `gh api user --include` | watcher | read | `P/github.py:175-177`; `P/cycle.py:755` | step 5 of every cycle |
| Watcher G2 | `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | watcher | read | `P/github.py:180-198`; `P/cycle.py:796` | step 8 |
| Watcher G3 (and G3' reserved) | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>` | watcher | read | `P/github.py:201-220`; `P/cycle.py:907, 944, 996` | per candidate; re-read |
| Watcher G4 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <MARKER_JQ>` | watcher | read | `P/github.py:223-225`; `P/cycle.py:905, 926, 942` | per candidate (marker booleans only) |
| Watcher G5 | `gh api graphql -f query=<EDITS_QUERY> -F number=<N> [-f after=<cursor>]` | watcher | read (query only) | `P/github.py:228-244`; `P/cycle.py:948` | per candidate |
| Watcher G6 (and G6' reserved) | `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=<N> [-f after=<cursor>]` | watcher | read (query only) | `P/github.py:228-249`; `P/cycle.py:957, 1013` | per candidate; re-read |
| Watcher G7 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>` | watcher | read | `P/github.py:252-262`; `P/cycle.py:983` | re-read before launch |
| Watcher non-GitHub commands | `git -C <worktree> remote get-url origin`; `<orca> skills list --json`; `<orca> agent launch --agent claude --worktree path:<worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json` (12 elements) | watcher | local read; the launch starts the claim session | `P/launch.py:244, 200, 95-116`; `P/cycle.py:721, 1048, 1099` | start of cycle and before launch; probe and launch in the launch step |
| Claim C1 assign | `gh issue edit <N> --repo <R> --add-assignee @me` | orchestrator | write | `SK/refs/claim.md:48`; `SK/SKILL.md:74, 87` | Wave 3; failure stops with `E-ASSIGN-FAILED` |
| Claim C2 ClickUp (not GitHub) | `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"`, which sends `PUT https://api.clickup.com/api/v2/task/{task_id}` with body `{"assignees": {"add": [<user id>]}}` | orchestrator runs the script | write (ClickUp), only if one task matches | `SK/refs/claim.md:50`; `SK/scripts/clickup_claim.py:232-237` | Wave 3; non-fatal |
| Claim C3 accuracy-check comment | `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`; on re-run `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | orchestrator | write | `SK/refs/claim.md:89-91` | Wave 6; never shown for approval first |
| Claim C4 claim comment (carries the marker) | `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md`; on re-run `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/claim-comment.md` | orchestrator | write | `SK/refs/claim.md:92`; `SK/templates/claim-comment.md:23` | Wave 6; failure `E-POST-FAILED` |
| Claim C5 PR path (only `--pipeline full --submit`) | In the launched session: `gh pr list --repo <R> --head <branch> --state all` (read), a conventional commit staging `.dev/tasks` and changed files (never `.claude/`, never `.dev/issues/`), `git push origin <branch>`, `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`; never merge | the launched agent, not the claim | write | `SK/templates/launch-prompt.md:28-34` | after Wave 8, inside the session; the guard at `full-submit` allows `gh pr comment/edit/ready/create --repo`, `gh issue create/edit/comment` and canonical pushes, and still blocks merge, push to master or main, free-form `gh api` writes and `gh pr create` without `--repo` (`H/launch-level-guard.sh:554-663, 716-722, 791-800`) |
| Claim reads (no write) | `gh auth status`; `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name`; `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author`; `gh api user -q .login`; `gh pr list --repo <R> --state merged --search "merged:>=<date>" --limit 200 --json number,title,mergedAt,files,url` | orchestrator; worker t3 | read | `SK/refs/claim.md:16-29`; `src/superclaude/agents/issue-worker-t3.md:22` | Wave 0 and Wave 1 |
| Claim create path X1 (the `--create` mode, not the claim) | `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md`, `--label "<mode label>"` and `--type "<name>"` only when they exist | orchestrator | write | `SK/refs/create.md:92`; `SK/SKILL.md:103` | create Wave 5 |
| Claim create path X2, X3 | `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`; optional `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md` | orchestrator | write | `SK/refs/create.md:95-96`; `SK/refs/labels.md:43` | create Wave 5 |
| Claim workers t1, t2, t3 | only read `gh` calls with `--repo <R>`; the one git write is `git fetch origin` | workers | read | `src/superclaude/agents/issue-worker-t1.md:28-29` (same lines in t2 and t3) | Waves 1 and 4 |
| `orca_worktree.py`, `origin_repo.py` | no GitHub write: first command words are `git` and `orca` only (`git remote get-url origin` for the script `origin_repo.py`) | orchestrator | none | `SK/scripts/orca_worktree.py` (`run([...])` first words); `SK/scripts/origin_repo.py:159-164` | per claim |
| L1 guard, job identity, L2 pre-push | no GitHub write; the guard only classifies and blocks the agent's own `gh` and `git` commands | hooks | none | `H/launch-level-guard.sh`; `H/launch-job-identity.sh`; `H/launch-level-pre-push.sh` | n/a |
| `install_hooks.py`, `install_ccsession.py`, `ccsession-orca` | no GitHub write (no network or `gh` use) | installer; Orca | none | `src/superclaude/cli/install_hooks.py`; `src/superclaude/cli/install_ccsession.py`; `src/superclaude/skills/ccsession-tag/ccsession-orca` | n/a |
| Coordinator contract text | progress posts such as issue comments are coordinator actions; no command line is given | a person-opened coordinator | write, no exact command in the text | `src/superclaude/core/WORKER-CONTRACT.md:242-243` | n/a |
| Removed `issue-pipeline` package | none: its `gh` calls were reads (`gh api user --include`, `gh api --method GET .../issues/<N>`, `.../events`, `.../comments`, `gh api graphql`); plan reply, label and Status mirror were contract text for the coordinator, no command line | n/a | none | Appendix B; `@01e7a9e23^` | REMOVED |
| Operator (a person, not code) | `gh label create ... --repo IronbellyOrg/IronClaude` (form [UNVERIFIED], not run); `gh issue edit <N> --repo IronbellyOrg/IronClaude --add-assignee @me`, `--add-label`, `--remove-label` | the person | write | `docs/designs/issue-watcher-setup.md:136-137, 161-163, 179-182` | before the watcher can see an issue |

### 4.6 Approval and gate points

The only human approval in the code is the approval label on the issue (judged against the approvers file); there is no second approval step in the watcher. The claim has no approval prompt for its posts. The one in-session approval is a typed prompt at level `worktree`.

| Gate | Piece | Condition | Closed word or exit code | Evidence |
|------|-------|-----------|--------------------------|----------|
| Enable switch | watcher | `not config.enabled and not dry_run` | `not_enabled`, 0 | `P/cycle.py:685-686` |
| Setup | watcher | worktree not a directory; approvers file not regular, symlink, wrong owner, group or other writable, over 1 MiB, bad line, or no ids | `worktree_invalid`, `approvers_invalid`, 2 | `P/cycle.py:298-361, 371-377` |
| Single instance | watcher | flock busy or lock inode replaced; lock missing or invalid | `lock_held`, 75; `lock_missing`, `lock_invalid`, 6 | `P/record.py:380-419` |
| Kill switch | watcher | `state_dir/DISABLED` exists (any type), checked at start and again before launch | `disabled`, `disabled_mid_cycle`, 0 | `P/cycle.py:712-713, 1063-1064`; `P/record.py:421-423` |
| Approval label | watcher | seven ordered rules: approval label applied by a `User` actor whose numeric id is in the approvers file, after the last trigger event and after store creation, not voided, no same-second tie | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete`, 0 | `P/predicates.py:185-234` |
| Intended owner | watcher | assignee set is not exactly the watcher's login | `unassigned`, `assigned_other`, 0 | `P/predicates.py:162-174` |
| Unchanged since approval | watcher | any issue, comment or rename time at or after approval | `edited_after_approval`, 0 | `P/predicates.py:237-259` |
| Project | watcher | not exactly one live item in the project with Status `Backlog` | `project_mismatch`, 0 | `P/predicates.py:262-271` |
| Caps and budget | watcher | day cap (`DAY_CAP`), candidates (`MAX_CANDIDATES`), call budget 32 plus 3 reserved, deadline floor, launch cut-off | `day_cap`, `budget_exhausted`, 0; `gh_timeout`, 3 | `P/cycle.py:34-47, 736, 867-876, 1069-1079`; `P/github.py:46-49, 448-454` |
| Re-read before launch | watcher | issue not open, label gone, assignee changed, approval voided or replaced, project moved | `revalidation_failed`, 0; transient, `revalidation_transient`, 7 | `P/cycle.py:979-1016` |
| Write-ahead | watcher | `pending` saved before `orca agent launch`; save failure | `state_dir_unwritable`, 6 | `P/cycle.py:1082-1092` |
| At-most-once and halt | watcher | entry `pending`/`claimed` (or launched/unknown/abandoned without a fresh marker); one launch-step outcome ends the cycle | `already_dispatched`, 0; no word | `P/cycle.py:919-933, 833-834` |
| Origin and Orca | watcher | `git remote get-url origin` is not `ironbellyorg/ironclaude` (lower-cased); no absolute `orca-ide` or `orca` listing the `orca-cli` topic | `origin_mismatch`, `orca_not_found`, 2 | `P/launch.py:163-251`; `P/cycle.py:721-722, 1048-1052, 1074-1075` |
| Operator forfeit | watcher | `reset N --forfeit-guarantee` on a state other than `abandoned` or `unknown` | `reset_refused`, 2 | `P/cli.py:232-252` |
| Orca down | claim | `orca status --json` not ok or not reachable; before any write | STOP `E-ORCA-REQUIRED` | `SK/scripts/orca_worktree.py:210-223`; `SK/refs/claim.md:17, 21` |
| Fork safety | claim | claim URL names another repo or host | STOP `E-FOREIGN-REPO`, 3 | `SK/scripts/origin_repo.py:135-140` |
| Assign and post | claim | assign fails; comment post fails | STOP `E-ASSIGN-FAILED`, `E-POST-FAILED`; no approval prompt | `SK/refs/claim.md:48, 93`; `SK/SKILL.md:76` |
| `--submit` | claim | `--submit` without explicit `--pipeline full` | STOP `E-SUBMIT-NEEDS-FULL`; script exit 2 | `src/superclaude/commands/issue.md:59`; `SK/scripts/orca_worktree.py:1900-1901` |
| Already launched, stale prompt | claim | `launch` entry in `worktree.json` or mirror; worktree prompt differs from the rendered one | `already_launched`; `W-LAUNCH-FAILED` | `SK/scripts/orca_worktree.py:1704-1724` |
| IR-4 preflight | claim | missing jq, uv or guard commands, guard not executable or old, registrations not firing, `disableAllHooks`, config dir mismatch | `W-ENFORCEMENT-ABSENT`, launch refused, no record | `SK/scripts/orca_worktree.py:955-1045, 1730-1747` |
| IR-7 refusal | claim | L2 not owned | BUILT-OFF (enabled:false); `W-L2-ABSENT` warning only | `SK/scripts/orca_worktree.py:822, 1757-1758` |
| Ship gate OB-H1 item 1, OB-H2, OB-H3 | claim | prose only: no governed claim on a real issue until they pass | NOT BUILT as a mechanism; the 12 observation tests skip | `src/superclaude/commands/issue.md:16`; `tests/hooks/test_launch_level_observations.py:79-84` |
| Typed approval | L1 guard | level `worktree`, bound session, no `agent_id`, first prompt line `/sc:implement` or `/task` | writes `sessions/<sid>.ok`, level becomes `worktree (approved)` | `H/launch-level-guard.sh:347-360` |
| Level grid | L1 guard | block IMPL and TURN at W; COMMIT, PUSH, SUBMIT, SKILL below `full-submit`; REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG at every level; the orca-verb part of ESCAPE (G2 rule 2 and the orca allow-list) recognises the command word `orca` only, so `orca-ide` is not constrained (observed exit 0), see Section 5.3 and Section 14 D-25 | `LL-*` words, exit 2 | `H/launch-level-guard.sh:783-803` |
| Fail closed for bound sessions | L1 guard | unparseable tool payload with a bound id, input error, unknown event, binding failure | `LL-BROKEN`, `LL-NOBIND`, exit 2; ordinary sessions and lost identity exit 0 | `H/launch-level-guard.sh:218-238, 367-392, 807-808` |
| Wrap failure | job identity | a governed Bash call cannot be wrapped | stderr text, exit 2 | `H/launch-job-identity.sh:500-502` |
| Protected push | L2 pre-push | governed or unknown actor pushes `refs/heads/main` or `master`; malformed record | `L2-PROTECTED`, `L2-UNKNOWN`, 1; `L2-MALFORMED`, 2 | `H/launch-level-pre-push.sh:187-208` |
| Session release | L1 guard | a person deletes `sessions/<sid>` and `sessions/<sid>.ok` | none; `identify` then reports `ordinary`, reason `released` | `H/launch-level-guard.sh:97`; `H/launch-job-identity.sh:252-255` |
| Plan-approval gate (plan hash, approval row, adoption row, `release-worker`, WC-17) | removed package | removed by decision; no replacement in code or contract | REMOVED | `CHANGELOG.md:17`; `@01e7a9e23^`; Appendix B |

---

## 5. Subsystem Reference

### 5.1 Issue watcher

Paths are relative to the 61ac2c2e6 snapshot. `P` = `src/superclaude/cli/issue_watch/`. `DES` = `docs/designs/issue-watcher.md`, `SET` = `docs/designs/issue-watcher-setup.md`.

**Purpose:** `superclaude issue-watch once` is a one-shot poll cycle. It reads GitHub (read-only `gh`), decides which approved issue is eligible, records that decision in a local store, and starts at most one Orca session that runs `/sc:issue --claim <N> --pipeline none`. It never writes to GitHub; the launched session does (P/launch.py:84-92).

**Status: BUILT-OFF (enabled:false).**

| Fact | Evidence | Tag |
|---|---|---|
| `enabled` defaults to false and must be a JSON boolean; the real cycle stops `not_enabled` (exit 0) before validation, lock and any external call | P/cycle.py:228-230, 685-686 | [CODE-VERIFIED] |
| `once --dry-run` ignores `enabled` and is BUILT-ON; it stops before the launch step (P/cycle.py:1029-1035) | P/cycle.py:685 | [CODE-VERIFIED] |
| No shipped config file; with none, `load_config` raises `config_invalid` | no `**/issue-watch*.json` in snapshot; P/cycle.py:206-213 | [CODE-VERIFIED] |
| Scheduler artefact (cron, systemd, launchd, GitHub Action, Orca automation) | not found in snapshot (greps over P, `.github`, `.claude`, `plugins`, `scripts`, Makefile, `pyproject.toml`, `package.json` return nothing; research 03 F.2). DES:30 and SET:288 record the cron entry (FU-2) as out of scope: "This work does not install or enable the entry" | [CODE-VERIFIED] by absence; status NOT BUILT, see Section 14 |
| Dispatcher, `COORD-<RepoName>` worktree, zero-setup install | not found in snapshot (`COORD-` returns 0 hits; no dispatcher for the issue pipeline) | not found in snapshot |
| Live-test record `docs/designs/issue-watcher-live-test.md` | not found in snapshot; only `issue-watcher.md` and `issue-watcher-setup.md` exist; DES:33 says the owner writes it. All 19 `_assumed_shape` fixtures are still assumptions | NOT BUILT, see Section 14 |
| "Implemented and merged in PRs #447 and #448; never run live" (DES:3) | no history or runtime state in a snapshot; the 19 assumed fixtures are consistent with it | [UNVERIFIED - doc-only, no code confirmation] |
| Whether `enabled` is true in the owner's real config, and whether anything outside the snapshot runs `once` | not visible in a snapshot | [UNVERIFIED] |

**Key files** (all under `P`; no module outside `P` touches `dispatch.json`, `audit.jsonl` or `dry-run.json`):

| Module | Lines | Role |
|---|---|---|
| `cycle.py` | 1406 | config loader, setup validation, `_Cycle` (the poll cycle), exit resolution, `status_report`, `slo_numbers` |
| `github.py` | 960 | the seven read-only `gh` argv builders, reply classifier, paged reads, `CallBudget`, rate-limit time |
| `record.py` | 865 | `FileStore`, `dispatch.json` schema, pure state transitions T-1..T-13, flock, atomic save, `init_state`, dry-run shadow |
| `launch.py` | 370 | Orca discovery, origin check, the one fixed `orca agent launch` argv, reply mapping |
| `predicates.py` | 312 | pure rules: approval replay, owner, edits, project Backlog, marker window, candidate order |
| `audit.py` | 404 | closed 59-word `REASON_TABLE`, audit line builders and schema, rotation, stderr fallback |
| `cli.py` | 348 | Click group `issue-watch`, five verbs, exit-code mapping (registered at `src/superclaude/cli/main.py:577-579`) |
| `runner.py` | 130 | the only module importing `subprocess` (`shell=False`, closed stdin, mandatory timeout, stderr cap 500 bytes) |

Pinned by `tests/issue_watch/test_module_boundaries.py` (nine modules, import allow-list) and `test_no_shell.py`.

**Dependencies and consumers.** Depends on `gh`, `git`, an Orca CLI (`orca-ide` then `orca`, `_ORCA_CLIS` at `src/superclaude/cli/install_user_setup.py:36`) and `swarm/atomic.py` (function-level import, record.py:372). Consumers: the operator and, by design only, an external timer (not found in snapshot). The launched claim session is the only downstream effect (Section 5.2).

---

#### 5.1.1 Poll cycle (decision engine)

Entry: `run_cycle(deps, dry_run)` (P/cycle.py:1214) builds `_Cycle` and calls `_Cycle.run` (682). Three private exceptions steer it: `_Skip(reason)` ends one issue, `_Stop(reason, stamp)` ends the cycle, `_Transient` marks a re-read timeout or 5xx.

```
once -> [0 enabled?]-no->  cycle line not_enabled (exit 0, no lock, no call)
          |yes/dry-run
        [1 validate_setup: worktree dir, approvers file]-bad-> exit 2
        [2 flock state_dir/lock]-held-> exit 75 | missing/invalid-> exit 6
        [3 DISABLED file?]-yes-> exit 0 `disabled`
        [4 load dispatch.json; now < next_permitted_at?]-> exit 6 | exit 5
        [5 G1 gh api user: login, account pin, clock skew]
        [6 git origin check] -> exit 2 origin_mismatch
        [7 sweep: pending->abandoned, expired launched->abandoned]
        [8 G2 discovery (trigger label + own login)]
        [9 order: never-examined first, max 10]
        [10 per candidate: E1..E14 gates, reads G4,G3,G5,G6]
              first launch-step outcome -> halt (no later candidate read)
        [11 _launch: re-read G7,G3',G6', DISABLED, origin, pending save, orca launch]
        [12 one commit: dispatch.json (real) or dry-run.json (dry)]
        [13 decision lines, then ONE cycle line -> audit.jsonl; rotate if locked]
```

Cycle steps (P/cycle.py; all [CODE-VERIFIED] against DES 6.2 except where marked in 5.1.8):

| # | Step (lines) | Stop or skip reason, exit |
|---|---|---|
| 0 | `enabled` gate (685-686) | `not_enabled`, 0 |
| 1 | `validate_setup` (688, 371-377) | `worktree_invalid`, `approvers_invalid`, 2 |
| 2 | `store.lock()` (695, record.py:380-419) | `lock_held` 75; `lock_missing`, `lock_invalid` 6 |
| 3 | DISABLED kill switch (712-713) | `disabled`, 0 (no health stamp) |
| 4 | store load, migrated store saved (real only, 746-747), `next_permitted_at` (748-750) | `store_missing`, `store_invalid` 6; `rate_limited` 5 |
| 5 | login G1 (752-775) | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` 3; `account_id_mismatch` 2; rate limit 5; warning `clock_skew` |
| 6 | origin check (716-722) | `origin_mismatch` 2; no time left `gh_timeout` 3 |
| 7 | sweep (777-792, record.py:627-651) | decision lines `pending_orphan`, `claim_not_observed` (state `abandoned`), exit 0 |
| 8 | discovery G2 (794-808) | `truncated`, `discovery_duplicate` 4; rate limit 5; warning `discovery_count` at >= 80 |
| 9 | order, `[:MAX_CANDIDATES]` = 10 (725-737, predicates.py:299-312) | none; dry-run uses the `dry-run.json` shadow map |
| 10 | candidates (812-834, `_examine` 915-961) | skip words in 5.1.1.1 |
| 11 | `_launch` (1026-1112) | table in 5.1.1.2 |
| 12 | `_commit` (1116-1126) | `state_dir_unwritable` 6 |
| 13 | `_conclude` (1176-1211) | decision lines first, then exactly one cycle line |

Exit resolution (cycle.py:462-482): precedence 2, 6, 7, 5, 3, 4; 75 only when it is the sole non-zero condition; else 0. The cycle never produces exit 1 (only `once` writes `cycle_crashed`, cli.py:123-129). The cycle-line reason is a stop reason, else the first condition reason matching the exit code, else `cycle_complete` (1164-1174). Health stamp (`last_completed_cycle_at`) is written only when no stop reason is set and the exit is 0, real cycle only (1138-1139).

##### 5.1.1.1 Per-candidate gate order (`_examine`, cycle.py:915-961)

Any `_Skip` writes one decision line (exit 0) and every skip except `budget_exhausted` stamps the issue in `considered` (831-832), which sorts it behind never-examined issues next cycle.

| Gate | Condition | Word (state) | GitHub reads |
|---|---|---|---|
| E1 (919-921) | entry `claimed` or `pending` | `already_dispatched` | 0 |
| E2 (922-931) | entry `launched`, `unknown`, or `abandoned` with `pending_at`; own marker found | `claimed` (T-10) else `already_dispatched` | G4 |
| E3 (932-933, 901-913) | `abandoned` tombstone (`attempts_exhausted`) | `claimed` or `already_dispatched` | G4, G3 |
| E4 (934-935) | `failed` entry still in backoff | `claimed` or `in_backoff` | G4, G3 |
| E5 (936-937, 867-876) | day cap reached (6 per 24 h, plus dry-run shadow launches) | `day_cap` | 0 |
| E6 (938-940) | assignee set != {own login} | `unassigned`, `assigned_other` | 0 |
| E7 (941-943) | marker read | `marker_unreadable` | G4 |
| E8 (944) | events read | `events_unreadable`, `events_incomplete` | G3 |
| E9 (945, 878-894) | approval replay (7 rules) | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete` | 0 |
| E10 (946-947) | own marker after current approval | `claimed` (T-11 / T-12); no launch | 0 |
| E11-E12 (948-956) | edits read; any edit, comment or rename at or after approval time | `edits_unreadable`; `edited_after_approval` | G5 |
| E13-E14 (957-960) | project items; exactly one live item in the configured project with status `Backlog` | `project_unreadable`; `project_mismatch` | G6 |
| E15 (961) | `_launch` | see 5.1.1.2 | - |

Note word `re-approved`: `_issue_line` (cycle.py:646-661) builds the per-issue decision line and sets `note = "re-approved"` (660) when both a current approval and a stored entry exist and the entry's approval event id is set and differs from the current approval's (654-659); it is a note on the line, not a skip or stop reason (`P/audit.py:280-284`).

Read failures: `rate_limited` raises `_rate_stop` (+3600 s, `rate_limit_clamped` 5, 663-668); `scope_missing` raises `project_read_failed` 3 (842-843); an unavailable call is `budget_exhausted` (skip, not stamped, loop continues).

##### 5.1.1.2 Launch step (`_launch`, cycle.py:1026-1112)

`c.launching = True` is the first line (1028); after the step returns or raises `_Skip`, the loop sets `halt` (833-834).

| Order | Check or action (lines) | Failure word, exit |
|---|---|---|
| dry-run | `would_launch = n`, shadow launch time appended, return `launched` with no state; no probe, re-read, Orca or write (1029-1035) | - |
| probe | `find_orca` (1048-1052) | `orca_not_found` 2 (stamped); out of time `budget_exhausted` |
| prompt | `build_claim_prompt` (1054-1056) | `prompt_invalid` 7 (unreachable for discovered issues; only test_cycle.py:3348) |
| re-read | `_revalidate` (979-1016): G7 state open and both labels present, owner again, G3' same approval event id, G6' project | `revalidation_failed`, `unassigned`, `assigned_other` (0); timeout or 5xx `revalidation_transient` 7. Edits are not re-read (1006) |
| guards | day cap again (1061), DISABLED again (1063-1064), launch cut-off 120 s (1069, 1078, 1095), origin again (1074-1075) | `day_cap`; `disabled_mid_cycle` 0; `budget_exhausted`; `origin_mismatch` 2 |
| write-ahead | `mark_pending` T-4 then `_save()` (1082-1092); if the save crossed the cut-off, restore and save again (1095-1098) | save failure `state_dir_unwritable` 6 |
| launch | `launcher.launch(orca, worktree, prompt, 120.0)` (1099) | outcome words below |

Outcomes: `launched` (T-5), `launch_unknown` exit 7 (T-6), `spawn_error` exit 7 (T-7).

**Dry-run versus real** (cycle.py): a dry-run runs steps 1-10, honours DISABLED and a persisted `next_permitted_at`, never saves a migrated store, never persists a rate limit, replaces a corrupt `dry-run.json` with a shadow (warning `dry_run_shadow_reset`), writes `dry-run.json` only when something was examined or would launch, writes audit lines with `dry_run: true` and no `state`, never writes `dispatch.json` or the health stamp (639, 685, 727-735, 746-747, 1029-1035, 1146-1162). It cannot reveal a probe, re-read or launch-step problem.

---

#### 5.1.2 GitHub I/O (`P/github.py`)

**The watcher never writes to GitHub.** Evidence: the five `"gh"` list literals in `P` are all in github.py (177, 183, 204, 231, 255) and all are reads; `cycle.py` holds no `gh`, `git`, `orca` or `subprocess` literal; no `POST|PATCH|PUT|DELETE|mutation` string exists in github.py except the comment at 107-108 and the two `--method GET` lines (206, 257); the GraphQL constants hold queries only (pinned by `test_security_invariants.py`, `test_github.py`). The repository is the literal `IronbellyOrg/IronClaude` (github.py:37). [CODE-VERIFIED]

| Id | Exact argv (`<>` = validated value) | Budget class | Called at |
|---|---|---|---|
| G1 | `gh api user --include` | shared | cycle.py:755 |
| G2 | `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | shared | 796 |
| G3 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>` | per-issue (G3' reserved) | 907, 944, 996 |
| G4 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <MARKER_JQ>` | per-issue | 905, 926, 942 |
| G5 | `gh api graphql -f query=<EDITS_QUERY> -F number=<N> [-f after=<cursor>]` | per-issue | 948 |
| G6 | `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=<N> [-f after=<cursor>]` | per-issue (G6' reserved) | 957, 1013 |
| G7 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>` | always reserved | 983 |

Builders: github.py:175-262. The comment projection `MARKER_JQ` turns the comment body into a boolean (no title, body or comment text is requested).

| Mechanism | Fact |
|---|---|
| `CallBudget` (github.py:437-463) | `CALL_CAP` 35 (46), `RESERVED_CALLS` 3 (49): non-reserved per-issue reads refuse at 32, reserved reads (G7, G3', G6') up to 35; G1 and G2 are shared and never refused, so at most 37 calls per cycle, 2 on an idle cycle |
| Paging | `PAGE_SIZE` 100, `PAGE_CAP` 5; repeated id, page cap or malformed item gives an incomplete or unreadable read |
| Deadline | `DEADLINE_TOTAL_S` 240, call floor `GH_FLOOR_S` 5, per-call `GH_TIMEOUT_S` 20 (cycle.py:37, 41-42, 418-427); a refused call is a skip `budget_exhausted` (per-issue) or `gh_timeout` (G1, G2) |
| `classify` (345-371) | timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed; the stderr and GraphQL error strings (`GH_ERROR_SIGNS`, 267-277) are marked `[UNVERIFIED]` in source |
| Rate limit | headers readable only for G1 (`--include`); `rate_limit_wait` (418-431): `Retry-After` or `x-ratelimit-reset` within 1..3600 s gives `rate_limited`, else now + 3600 s `rate_limit_clamped`; every G2 or per-issue limit clamps (cycle.py:663-668); stored in `next_permitted_at`; both exit 5 |

The GraphQL reply shapes, the cursor alphabet and the `--include` header layout are [UNVERIFIED]: all 19 `tests/issue_watch/fixtures/_assumed_shape/*.json` fixtures are assumptions (pinned by `test_github.py:575-597`); a wrong shape fails closed (read skipped, issue skipped).

---

#### 5.1.3 Launch and dispatch record

**Launch** (`P/launch.py:95-116`): exactly 12 argv elements, `ORCA_AGENT` fixed to `claude`, no permission flag, no model flag, run with `cwd=<worktree>` and a 120 s timeout:

`<orca> agent launch --agent claude --worktree path:<abs worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json`

`<orca>` is the absolute path chosen by `find_orca`: `orca-ide`, then `orca`, accepted only when `skills list --json` lists topic `orca-cli` (163-203, not cached). The prompt matches `PROMPT_PATTERN` (33) and the level `none` is hard-coded (3 occurrences of `--pipeline`, all in launch.py). The watcher creates no worktree: `--worktree` is the operator-set `worktree` config value. Origin check: `git -C <worktree> remote get-url origin` must equal `ironbellyorg/ironclaude` lower-cased (233-251).

**Reply handling** (`outcome_of`, 326-349), in order: spawn failure `spawn_error`; timeout, `agent_session_operation_unknown` text, non-zero exit, non-JSON, missing id at `receipt.operation_id` / `error.operation_id`, or an id outside `^[A-Za-z0-9._:-]{1,128}$` all give `unknown`; else `launched` with the id. The reply shapes (`OPERATION_ID_PATHS` 42-45, `OP_UNKNOWN_TEXT` 47) are [UNVERIFIED] (`[PROPOSAL, UNVERIFIED]` in source). `LaunchOutcome.detail` is set but never read (see 5.1.7). The watcher learns the result only when a later G4 read sees the session's own claim marker (`_hit` cycle.py:848-865, then `_claim` T-10).

**`dispatch.json`** (`<state_dir>/dispatch.json`, mode 0600, `P/record.py`): 7 top-level keys (`schema_version` 1, `created_at`, `next_permitted_at`, `last_completed_cycle_at`, `considered`, `consumed_log`, `entries`); each entry has 17 fields (record.py:69-88: `issue`, `state`, `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `approved_at`, `launch_cwd`, `launch_login`, `launch_account_id`, `consumed_at`, `pending_at`, `created_at`, `updated_at`, `lease_expires_at`, `last_reason`); six states `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed` (34-36). Any extra or missing key makes the store `store_invalid` (exit 6).

| T | Transition (record.py function) | Trigger |
|---|---|---|
| T-1, T-3 | none or `failed` -> `failed`; third failure -> `abandoned` `attempts_exhausted` (`fail` 503-525) | `prompt_invalid`, `revalidation_transient` (MAX_ATTEMPTS 3) |
| T-2 | `failed` eligible again (`backoff_elapsed` 528-535) | 10 min backoff |
| T-4 | none or `failed` -> `pending`, `launches=1` (`mark_pending`) | all checks passed, saved before the launch |
| T-5, T-6, T-7 | `pending` -> `launched` (lease 60 min), `unknown`, `abandoned` `spawn_error` | launch outcome |
| T-8, T-9 | `pending` -> `abandoned` `pending_orphan`; `launched` past lease -> `abandoned` `claim_not_observed` (`sweep` 627-651) | start of next cycle |
| T-10, T-11, T-12 | `launched`/`unknown`/`abandoned`, none, `failed` -> `claimed` (`mark_claimed` 654-686) | own claim marker seen (window: at or after `pending_at` minus 300 s, else strictly after the approval) |
| T-13 | `abandoned`/`unknown` -> entry removed (`reset_entry` 706-720) | `reset N --forfeit-guarantee` |

`claimed` is terminal; `unknown` leaves only through a marker or `reset`. Any other (state, trigger) pair raises `TransitionError`.

**Write path.** Save = `json.dumps` sorted, indent 2, ASCII; `write_prepared_bytes` (mkstemp in the same directory, fsync, `os.replace`), `chmod 0600`, directory fsync (record.py:370-378). Lock = non-blocking `flock(LOCK_EX|LOCK_NB)` on `state_dir/lock` (pre-created by `init-state`, `O_NOFOLLOW`, regular file owned by the euid, inode re-checked after locking; held means exit 75) (380-419). Dry-run uses `dry-run.json` (`considered`, `shadow_launches`) and never touches `dispatch.json` (831-865).

**Crash points** (pinned by `test_crash_injection.py`: one crash per point, then five more cycles, launcher called at most once in all six runs): C1 before the pending save (store untouched), C2 during the atomic replace (old file kept; orphan `*.tmp` ignored), C3 after the pending save (swept to `pending_orphan`, never launched), C4 after the spawn (swept, never relaunched), C5 after the outcome save (only audit lines lost).

**DISABLED kill switch.** `os.path.lexists(state_dir/DISABLED)` (record.py:421-423; a dangling symlink counts), checked at step 3 and again before the pending write (`disabled_mid_cycle`). Nothing in `P` creates or removes the file.

---

#### 5.1.4 Operator surface (`P/cli.py`)

Five verbs, each with `--config` (default `~/.config/superclaude/issue-watch.json`, `~` expanded for the option only; cli.py:31, 49-59). `test_cli.py` pins "exactly five commands".

| Verb | Options | Effect | Platform check |
|---|---|---|---|
| `once` | `--dry-run` | the cycle of 5.1.1; prints `cycle: <reason>`, `exit: <code>`, dry-run adds `probe:` and `would_launch:` (cli.py:111-137) | yes |
| `status` | `--json` | local read of `dispatch.json` and `DISABLED` mtime; no lock, no `gh`, never reads `audit.jsonl` (cycle.py:1270-1335); `healthy` = a real stop-free exit-0 cycle within `HEALTH_AGE_S` 900; stale = `unknown` or `pending_orphan` older than 86400 s; prints (never runs) a `--retry-launch` argv for `unknown` entries | no |
| `check-config` | - | static check: config, worktree directory, approvers file; no `gh`, no Orca, no origin check (cli.py:185-198) | yes |
| `init-state` | - | creates `state_dir` 0700, `lock` 0600, `dispatch.json` 0600; refuses an existing store (exit 6) (record.py:753-802) | yes |
| `reset` | `ISSUE --forfeit-guarantee` or `--rate-limit` | removes an `abandoned` or `unknown` entry (T-13), or clears `next_permitted_at`; writes one audit line under the lock (cli.py:282-348) | yes |

Exit codes of `once` (reasons from `audit.REASON_TABLE`; `status` also returns 1 for unhealthy, 6 store error, 2 config error):

| Exit | Meaning | Words |
|---|---|---|
| 0 | finished or deliberate no-op | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled`, all skip and entry-success words |
| 1 | crash (stderr line only) | `cycle_crashed` (cli.py:123-129) |
| 2 | config or environment | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch`; `reset_refused` |
| 3 | GitHub read failure | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` |
| 4 | incomplete discovery | `truncated`, `discovery_duplicate` |
| 5 | rate limit | `rate_limited`, `rate_limit_clamped` |
| 6 | state store | `store_missing`, `store_invalid`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` |
| 7 | launch-path entry failure | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` |
| 75 | lock held (only as sole condition) | `lock_held` |

**Config** (`load_config`, cycle.py:195-283; JSON, strict, unknown keys rejected, no `~` expansion, network filesystem `state_dir` refused; full table in Section 9):

| Key | Default | Rule |
|---|---|---|
| `schema_version` | required | integer 1 |
| `enabled` | `false` | JSON boolean |
| `labels.trigger`, `labels.approval` | `issue-watch:trigger`, `issue-watch:approved` | 1-50 chars, no comma, quote, control char or leading `-`; must differ |
| `project_id` | required | `PVT_[A-Za-z0-9_-]{1,64}` |
| `owner_account_id` | none | optional pin; mismatch is `account_id_mismatch` |
| `worktree`, `approvers_file` | required | absolute paths |
| `state_dir` | `$XDG_STATE_HOME` or `~/.local/state`, plus `superclaude/issue-watch` | absolute |

The timeouts, `DAY_CAP`, 10 candidates and 60 min lease are code constants, not config keys (cycle.py:33-47).

**Approvers file** (`validate_approvers`, cycle.py:298-361): regular file (symlink refused), opened `O_NOFOLLOW` with an inode re-check, owner = euid, not group- or other-writable (read bits unchecked), at most 1 MiB, UTF-8, every non-blank line not starting with `#` must match `[1-9][0-9]{0,19}` (no whitespace, no CR), at least one id. Checked on every enabled or dry-run cycle.

**SLO.** `slo_numbers` (cycle.py:1359-1406) computes p95 approval-to-launch, exit-0 share over 7 days, claimed-within-lease share and stale count; it has no production caller (only `test_slo_helper.py` and an owner-run snippet at SET:457-476). DES:752 records "a library function ... not a verb". Status NOT BUILT as an operator surface, see Section 14.

**Audit log** (`P/audit.py`): `audit.jsonl` (0600, one sorted-key ASCII JSON line per `os.write`), three kinds (cycle, decision, warning), every key type- and shape-checked, rotation at 5 MiB keeping `.1`-`.4`, only with the lock held; one cycle line per exit that reaches `_conclude`, decision lines first. Config or platform failure, `cycle_crashed`, `state_dir_unwritable` and reset usage errors write only a stderr JSON line (cli.py:79, 127, 219; cycle.py:1195-1196). Nothing in `src/` reads the file back.

---

#### 5.1.5 Gates and approvals

Approval is one human label event judged by `approval_of` (predicates.py:185-234): the approval label must be present and last applied by an `actor_type == "User"` (not `[bot]`) whose numeric id is in the approvers file; it must be strictly after the last trigger-label event and the store `created_at`; a later unlabel voids it; a same-second label collision is `events_incomplete`. There is no second approval step in the cycle.

| Gate | Condition | Word / exit | Evidence | Pinned by |
|---|---|---|---|---|
| Enable switch | `not enabled and not dry_run` | `not_enabled` / 0 | cycle.py:685-686 | test_cycle.py (`...enabled_false...fr027`) |
| Kill switch | `DISABLED` exists, at start and before the pending write | `disabled`, `disabled_mid_cycle` / 0 | cycle.py:712, 1063; record.py:421 | test_cycle.py, test_record.py |
| Single instance | flock busy or lock inode replaced | `lock_held` / 75 | record.py:403-414 | test_concurrency.py |
| Trigger label | discovery filters on `labels.trigger` and own login; `>= 100` results | `truncated` / 4 | github.py:180-198, 823-824 | test_github.py |
| Approver label + allow-list | rules of `approval_of` | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete` / 0 | predicates.py:185-234 | test_predicates.py |
| Owner | assignee set equals {own login}; optional `owner_account_id` | `unassigned`, `assigned_other` / 0; `account_id_mismatch` / 2 | predicates.py:162-174; cycle.py:768 | test_predicates.py, test_cycle.py |
| Unchanged since approval | any edit, comment (not own) or rename time >= approval | `edited_after_approval` / 0 | predicates.py:237-259 | test_predicates.py |
| Project | one live item in `project_id`, status `Backlog` | `project_mismatch` / 0 | predicates.py:262-271 | test_predicates.py |
| Day cap | 6 launches in a rolling 24 h (checked twice) | `day_cap` / 0 | cycle.py:36, 867-876, 1061 | test_cycle.py, test_record.py |
| Call budget | 32 ordinary + 3 reserved; 240 s deadline; 120 s launch cut-off | `budget_exhausted` / 0 | github.py:46-49, 448-454; cycle.py:41-43 | test_github.py, test_cycle.py |
| Rate limit | `next_permitted_at` in the future | `rate_limited`, `rate_limit_clamped` / 5 | cycle.py:748-750, 663-668 | test_cycle.py, test_github.py |
| Origin and Orca | origin not `ironbellyorg/ironclaude`; no `orca-cli` binary | `origin_mismatch`, `orca_not_found` / 2 | launch.py:163-251 | test_launch.py, test_origin_parity.py |
| At-most-once | entry `pending`, `claimed`, or launched/unknown/abandoned without a marker; `pending` saved before launch | `already_dispatched` / 0 | cycle.py:919-933; record.py:538 | test_cycle.py, test_crash_injection.py |
| One launch per cycle | `launching` then `halt` | no word | cycle.py:833-834 | test_cycle.py (`...s1_case_b...`) |
| Re-validation | state, labels, owner, approval id, project re-read | `revalidation_failed` / 0; `revalidation_transient` / 7 | cycle.py:979-1016 | test_cycle.py, test_github.py |
| Launch argv | 12 literal elements, prompt pattern | `prompt_invalid` / 7 | launch.py:84-116 | test_launch.py, test_security_invariants.py |
| Operator reset | only `abandoned` or `unknown`, with `--forfeit-guarantee` | `reset_refused` / 2 | cli.py:232-252, 309-313 | test_cli.py |

Prose-only gates (no code check): the live-test record, shadow run, grants, acceptances and a running coordinator (SET:226-290, 584-635); "grant row" appears only as prose (SET:274, `docs/designs/issue-pipeline-fu1.md:24, 26`), not found as code in snapshot.

---

#### 5.1.6 Closed reason vocabulary (`audit.REASON_TABLE`, audit.py:26-102, 59 words)

Pinned literally, in order, with every (kind, exit) pair by `test_audit.py` (`test_reasons_pin_59_names...`). Raise sites: the per-candidate skip and entry words are in 5.1.1.1, the launch-step words in 5.1.1.2, the cycle-level stop words in the 5.1.1 step table, and the exit and evidence column of every word in 10.1 and 10.2. The note word `re-approved` is set in `_issue_line` (5.1.1.1).

| Group (count) | Words |
|---|---|
| Cycle, exit 0 (4) | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled` |
| Cycle, exit 2 (7) | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` |
| Cycle, exit 3 (5) / 4 (2) / 5 (2) | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed`; `truncated`, `discovery_duplicate`; `rate_limited`, `rate_limit_clamped` |
| Cycle, exit 6 (5) / 75 (1) / 1 (1) | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable`; `lock_held`; `cycle_crashed` |
| Skip, exit 0 (17) | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete`, `events_unreadable`, `edited_after_approval`, `project_mismatch`, `project_unreadable`, `unassigned`, `assigned_other`, `already_dispatched`, `in_backoff`, `day_cap`, `budget_exhausted`, `revalidation_failed`, `marker_unreadable`, `edits_unreadable` |
| Entry (9) | `launched`, `claimed`, `pending_orphan`, `claim_not_observed`, `attempts_exhausted` (exit 0); `prompt_invalid`, `revalidation_transient`, `spawn_error`, `launch_unknown` (exit 7) |
| Note (1), warning (4), operator (1) | `re-approved`; `discovery_count`, `clock_skew`, `dry_run_shadow_reset`, `reset_refused` (exit 2); `operator_reset` |

Five words never come out of `run_cycle`: `config_invalid`, `platform_unsupported`, `cycle_crashed`, `reset_refused`, `operator_reset` (CLI-owned). Adding a skip word: add it to `REASON_TABLE`, raise `_Skip`, update the literal pin in `test_audit.py`; `audit.line` raises `ValueError` for an unknown word.

---

#### 5.1.7 Dead, unwired and not-built items (see Section 14)

| Item | Status | Evidence |
|---|---|---|
| `MAX_LAUNCHES_PER_CYCLE = 1` (cycle.py:35): 14 constants at cycle.py:34-47, 13 read, this one defined and never read (no hit in `src/` or `tests/`). The one-launch limit is enforced by `_Cand.launching` (1028) and `self.halt` (833-834, loop break 816-817), which also halts after any launch-step skip, not only after a launch. DES:380, 819 name the constant as a default | NOT BUILT (dead constant) | [CODE-VERIFIED]; Section 14 |
| Scheduler that runs `once` (FU-2) | NOT BUILT | not found in snapshot; DES:30, SET:288 |
| Live-test record and captured fixtures (FU-1) | NOT BUILT | absent file; 19 `_assumed_shape` fixtures |
| `slo_numbers` as a verb or alert; alerting FU-4, auto `--retry-launch` FU-8 (`retry_argv` launch.py:119-132 only prints), role check FU-9, pruning FU-11, ETag FU-5, FS allow-list FU-12 | NOT BUILT | deferred by DES:856-871, SET:669-686 |
| `status` reads `audit.jsonl` (DES:406) | NOT BUILT | cycle.py:1279-1281 "not read" |
| `LaunchOutcome.detail` (8 words), `launch_login`, `launch_account_id`, `record.disabled_present` | dead or write-only | no reader in `src` (launch.py:58-70; record.py:548-568, 748-750) |
| `prompt_invalid` for discovered issues | practically unreachable | github.py:827-828 rejects bad numbers first; only test_cycle.py:3348 |
| Dispatcher, `COORD-`, zero-setup install, coordinator that starts the worker after the claim | not found in snapshot | research 03 F.2, F.3; the "Issue pipeline duties" contract text is REMOVED (CHANGELOG.md:17) |

---

#### 5.1.8 Contradictions found and open questions

| # | Doc claim | Code | Tag |
|---|---|---|---|
| 1 | Skew: DES:827 "skew tolerance 300 s" and the 60 s warning (DES:510, SET:384) | two constants: `SKEW_TOLERANCE_S` = 300 is the claim-marker window (predicates.py:17, 295); `SKEW_WARN_S` = 60 is the clock-skew warning threshold (cycle.py:44, 774). The row label is ambiguous, the number is right | [CODE-VERIFIED] (not a code contradiction; earlier contradiction tag withdrawn by erratum) |
| 2 | `find_orca` "cached per cycle" (DES:331, 362, 621) | caches nothing (launch.py:6, 177) | [CODE-CONTRADICTED] |
| 3 | Step 10 "Calls 0" (DES:360) | entry-state candidates read G4 (and G3) first (cycle.py:922-935) | [CODE-CONTRADICTED] |
| 4 | Exit 7 combines with 5 or 3 (DES:173) | unreachable through `_Cycle` (S1 halt); only 7 with 6 | [CODE-CONTRADICTED] |
| 5 | `audit.jsonl` written by every exit, read by `status` and the SLO reducer (DES:406) | stderr-only exits exist; no reader in `src` | [CODE-CONTRADICTED] |
| 6 | Prompt `/sc:issue --claim <N>` (DES:15; SET:616-619) | `... --pipeline none` (launch.py:92) | [CODE-CONTRADICTED] |
| 7 | `clock_skew_s` always on the cycle line (DES:722) | optional (audit.py:165) | [CODE-CONTRADICTED] |
| 8 | `agent-work-report` reads `orchestrator_repo` from the same config file (`src/superclaude/skills/agent-work-report/scripts/common.py:22-40`) | `load_config` rejects keys outside the 8 allowed (cycle.py:58-69, 216-220): such a config makes `once` exit 2 `config_invalid` | [CODE-CONTRADICTED] (cross-consumer) |
| 9 | SET:170, DES:43 name `WORKER-CONTRACT.md` "Issue pipeline duties" and `stage-status` | no such section or verb (CHANGELOG.md:17) | [CODE-CONTRADICTED] |

Open questions: PRs #447/#448 and "never run live" (DES:3) [UNVERIFIED]; real `gh` and Orca reply shapes [UNVERIFIED]; what runs `once` and the real `enabled` value [UNVERIFIED]; whether the per-cycle G4 cost for stuck `unknown` and `claim_not_observed` entries is acceptable; the unseen edit window between the G5 read and the launch (edits are not re-read, cycle.py:1006); `status` prints `disabled since: no` for a dangling `DISABLED` symlink while the cycle treats it as present (record.py:421-431); `reset --rate-limit --forfeit-guarantee` silently ignores the second flag (cli.py:309-313).

---

#### 5.1.9 Extension points

| File | Function | What to change | Pinned by |
|---|---|---|---|
| `P/github.py` | `argv_*` builders, `_call`, `classify` | new read: validate every caller value, `--method GET`, reuse a word already in `REASON_TABLE` | `test_github.py` (argv written out literally), `test_security_invariants.py` |
| `P/audit.py` | `REASON_TABLE`, `_KEYS`, `_TYPES`, `_RULES` | new reason word or audit key | `test_audit.py`, `test_predicates.py` (every predicate reason is in the table) |
| `P/predicates.py` + `P/cycle.py` | `_examine` | new gate: pure predicate, call it in the gate order of 5.1.1.1 | `test_predicates.py`, `test_cycle.py` |
| `P/record.py` | `ENTRY_STATES`, `MIGRATIONS` (ships empty), transition functions | new state or entry field needs a migration step and a pair-table update | `test_record.py` |
| `P/launch.py` | `launch_argv`, `PROMPT_PATTERN`, `build_claim_prompt` | change together; update the literal 12-element test | `test_launch.py`, `test_security_invariants.py` |
| `P/runner.py` | `Runner.run` | no other module may import `subprocess` | `test_no_shell.py`, `test_module_boundaries.py` |

---

All line numbers in Sections 5.2 to 5.4 are for snapshot 61ac2c2e6.

**Path key (used by every citation in 5.2 to 5.4; every short form expands to a repository-relative path):**
`SK/` = `src/superclaude/skills/sc-issue-protocol/`; `OW` = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; `GD` = `src/superclaude/hooks/scripts/launch-level-guard.sh`; `ID` = `src/superclaude/hooks/scripts/launch-job-identity.sh`; `PP` = `src/superclaude/hooks/scripts/launch-level-pre-push.sh`; `HJ` = `src/superclaude/hooks/hooks.json`; `WC` = `src/superclaude/core/WORKER-CONTRACT.md`; `T/` = `tests/`; `CMD` = `src/superclaude/commands/issue.md`; `AG` = `src/superclaude/agents/`. A bare file name followed by `:line` (for example `claim.md:81`) means the file under `SK/refs/` or `CMD` as named in the same row.

**Status words used here:** BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. Verification tags: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED], [STALE DOC]. Remediation is not created here; capabilities that are unwired, switched off, retired or caller-less carry a "see Section 14" pointer.

---

### 5.2 `/sc:issue --claim` flow and `orca_worktree.py`

**Purpose:** `/sc:issue --claim <N>` takes a GitHub issue on the repository that `origin` points at, assigns it, checks its accuracy, writes a summary and a next-step prompt, and (unless `--pipeline none`) creates an Orca worktree and launches a Claude agent in it at a chosen level. It is a prose protocol run by the orchestrating model, backed by three helper scripts; the only code that calls `orca` is `orca_worktree.py` (SKILL.md:35).

**Status lines**

| Piece | Status | Evidence |
|---|---|---|
| `/sc:issue` command (version 1.1.0) and skill protocol | BUILT-ON | `issue.md:2-3`, Activation `issue.md:104-110`; run by the model, no switch |
| `origin_repo.py`, `clickup_claim.py` | BUILT-ON (ClickUp conditional: `skipped` without `CLICKUP_API_TOKEN` or `CLICKUP_WORKSPACE_ID`) | `clickup_claim.py:164-169` |
| `orca_worktree.py` preflight, worktree, prompt, launch, IR-4 preflight, L2 install, shim detection | BUILT-ON | no gating flag; `build_parser` `OW:1857-1894` |
| IR-7 refusal of a launch when the L2 hook is not owned | BUILT-OFF (a constant, not an `enabled` key) | `IR7_REFUSE = False` `OW:822`; refusal branch `OW:1757-1758` and text `OW:829-831` unreachable; pinned off by `T/skills/test_issue_l2_install.py:639` (see Section 14) |
| IR-3 `pipeline.json` level file | NOT BUILT | grep `pipeline\.json` over `src` and plugins: no match; stated as not built at `docs/designs/sc-issue-claim-pipeline-flag.md:58` (see Section 14) |
| Any caller of `orca_worktree.py pending` | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON (`OW:1515-1523`, `OW:1886-1893`) | grep of `src` and plugins: no caller; only tests run it, `T/hooks/test_launch_level_guard_worker.py:287` and `T/skills/test_issue_orca_worktree.py:2472-2498` (see Section 14) |
| Default `--pipeline` pick from type, complexity, hours | NOT BUILT as code (prose rule only) | `claim.md:81`; no `.py`, `.sh`, `.json` holds the reason strings (see Section 14) |
| Ship gate "no governed claim until OB-H1 item 1, OB-H2, OB-H3 pass" | NOT BUILT as a mechanism (prose) | `issue.md:16`, `claim.md:136`; no code reads it (see Section 14) |
| Coordinator hand-off after a `--pipeline none` claim | NOT BUILT (prose at `issue.md:85`, `SKILL.md:140`, `claim.md:96`) | no caller of the `worktree` subcommand besides the claim prose (see Section 14) |
| Automatic close of an agent that is not behind the shim | NOT BUILT (warning only) | `OW:1803-1811` (see Section 14) |

**Key Files**

| File | Purpose |
|---|---|
| `CMD` (117 lines) | Command front: seven flags (`issue.md:36-44`), STOP rules before Activation (`issue.md:50-59`), outputs table (`issue.md:74-81`), Will / Will Not (`issue.md:89-102`) |
| `SK/SKILL.md` (197 lines) | Orchestrator protocol: files table `SKILL.md:24-50`, worker spawn rule `:54-64`, GitHub call rules `:70-78`, claim waves `:80-92`, return contract `:105-150`, error table `:152-177` |
| `SK/refs/claim.md`, `refs/tiers.md`, `refs/chains.md` (40 lines) | Wave text; tier pins and T1-to-T2 fallback (`tiers.md:34-42`); default next-step rows (`chains.md:9-16`) |
| `SK/scripts/origin_repo.py` (195 lines) | Resolves `<R>` and `<N>` from `origin` only (`:156-174`, `:102-153`) |
| `SK/scripts/clickup_claim.py` (270 lines) | Read-then-assign ClickUp lookup; the single write is `:232-237` |
| `SK/scripts/orca_worktree.py` (1906 lines) | Preflight, worktree create/reuse, prompt render, IR-4 preflight, L2 install, launch, `pending` |
| `SK/templates/` (15 files, not 17) | Posted comments (`claim-comment.md` 23 lines, `accuracy-check-comment.md` 20), `issue-summary.md`, `next-steps.md`, `launch-prompt.md` (34 lines, four blocks `:11,:20,:25,:28`) |
| `AG/issue-worker-t1.md`, `-t2.md`, `-t3.md` (35 lines each; erratum applied) | Tier workers; `tools` line 5, `model:` line 6 |

**How It Works**

The "orchestrator" is the Claude session that invoked the skill, not a program: no Python runs the waves in order (SKILL.md:80-92). Workers run in waves 1 and 4 only; every write to GitHub, ClickUp or Orca is the orchestrator's. Worker rules: read-only GitHub, write only under `.dev/issues/`, return only file paths (`t*.md:28-35`); an empty or missing worker file is retried once, then STOP `E-WORKER-NO-OUTPUT` (SKILL.md:66).

```
 /sc:issue --claim N [--pipeline L] [--submit]
   W0 orch   origin_repo.py, gh auth, orca_worktree.py preflight, default branch   (claim.md:11-21)
   W1 T3     scout.md  (lookup)                                                    (claim.md:23-34)
   W2 orch   edge cases: closed / assigned-to-other => STOP, no writes             (claim.md:36-44)
   W3 orch   gh issue edit --add-assignee @me ; clickup_claim.py                   (claim.md:46-51)
   W4 T2|T1  accuracy-check.md, issue-summary.md (+ analysis if out of date)       (claim.md:53-63)
   W5 orch   Skill sc-recommend -> next-steps.md ; resolve level L ; prompt render (claim.md:75-84)
   W6 orch   post/edit accuracy-check + claim comments        <- --pipeline none ends here (claim.md:86-96)
   W7 orch   orca_worktree.py worktree  (create/reuse issue-<N>, copy .dev/issues/<N>/)  (claim.md:98-115)
   W8 orch   orca_worktree.py launch  -> pending/<nonce> + agent with [sc-launch:v1:<nonce>]  (claim.md:117-136)
```

**Waves and owners**

| Wave | Actor | Action | Output |
|---|---|---|---|
| 0 | orchestrator | origin, `gh auth status`, `orca_worktree.py preflight` (runs for `none` too), default branch via `gh repo view`, mkdir `<D>` | `<D>` = `.dev/issues/<N>/` (`claim.md:11-21`) |
| 1 | worker T3 | issue, comments, merged PRs, git log lookup | `scout.md` |
| 2 | orchestrator | edge cases from `scout.md` | STOP or continue |
| 3 | orchestrator | assign on GitHub, then ClickUp script | `clickup.json` |
| 4 | worker T2 (T1 when scout sizes `complex`) | accuracy check, summary, optional `/sc:analyze` | `accuracy-check.md`, `issue-summary.md`, `analysis/analyze-<scope>.md` |
| 5 | orchestrator | `Skill sc-recommend`, level pick, plan boundary, `orca_worktree.py prompt` | `recommend.md`, `next-steps.md`, `launch-prompt.md` |
| 6 | orchestrator | post or edit two marked comments | `claim-comment.md`, comments on the issue |
| 7 | orchestrator (script) | create or reuse the worktree | `worktree.json` |
| 8 | orchestrator (script) | launch the agent | `launch` entry in `worktree.json` |

**GitHub and ClickUp writes (all by the orchestrator; no write before Wave 3; none before the Orca preflight passes, `claim.md:21`)**

| # | Path | Exact command | Wave | Evidence |
|---|---|---|---|---|
| C1 | claim | `gh issue edit <N> --repo <R> --add-assignee @me` | 3 | `claim.md:48`, `SKILL.md:74,87` |
| C2 | claim | ClickUp `PUT https://api.clickup.com/api/v2/task/{task_id}` body `{"assignees": {"add": [<user id>]}}` via `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R>` (only when exactly one task matches) | 3 | `clickup_claim.py:232-237`, `claim.md:50` |
| C3 / C3' | claim | `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`; or edit `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | 6 | `claim.md:89,91` |
| C4 / C4' | claim | same two forms with `claim-comment.md` | 6 | `claim.md:92` |
| C5 | launched agent, not the claim | at `full --submit` only: commit, `git push origin <branch>`, `/sc:pr-submit --monitor 3 --head <branch> ...` | after W8 | `templates/launch-prompt.md:28-34` |
| X1 | create | `gh issue create --repo <R> --title "[FEATURE|BUG] <title>" --body-file <D>/issue-body.md [--label ...] [--type ...]` | create W5 | `create.md:92`, `SKILL.md:103` |
| X2 | create | `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json` | create W5 | `create.md:95`, `labels.md:43` |
| X3 | create | `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md` (marker `<!-- sc:issue:create-review -->`) | create W5 | `create.md:96` |

The claim writes no label, issue type, issue field, status change or PR (`issue.md:93-102`, `labels.md:7`). Posts go up directly, never shown for approval (`SKILL.md:76`); markers `<!-- sc:issue:claim -->` (`claim-comment.md:23`) and `<!-- sc:issue:accuracy-check -->` (`accuracy-check-comment.md:20`) make a re-run edit instead of duplicate. Workers never write to GitHub or ClickUp. `create` makes no ClickUp call and no self-assignment (`create.md:9`). Every `gh` write passes `--repo <R>` with `<R>` from `origin_repo.py` only (`SKILL.md:72-73`); `origin_repo.py` resolves the fork only when the clone's `origin` URL is the fork (`origin_repo.py:14-15`; the guarantee is a property of the clone, not of the script).

**STOP codes (prose, executed by the model) and exit codes**

| Code | Condition | Source |
|---|---|---|
| `E-CREATE-ONLY-FLAG` / `E-CLAIM-ONLY-FLAG` | `--depth/--mode/--type` with `--claim` / `--pipeline/--submit` with `--create` | `issue.md:53,57` |
| `E-SUBMIT-NEEDS-FULL` | `--submit` with a value, without `--pipeline full`, or with no `--pipeline`; the script re-checks (exit 2) | `issue.md:59`, `OW:1900-1901` |
| `E-NO-ORIGIN` (exit 1), `E-FOREIGN-REPO` (3), `E-NOT-AN-ISSUE` (4) | origin missing or not GitHub; claim URL on another repo; `/pull/<N>` or non-issue argument | `origin_repo.py:47-50,114-153` |
| `E-GH-AUTH`, `E-ORCA-REQUIRED` | `gh auth status` fails; preflight `ok:false` (before any write, even for `none`) | `claim.md:16,17` |
| `E-WORKER-NO-OUTPUT`, `E-TIER-UNAVAILABLE` | worker file missing after one retry; tier not served (no alias fallback) | `SKILL.md:66,167`, `tiers.md:44-52` |
| `E-ASSIGN-FAILED`, `E-POST-FAILED`, `E-CREATE-FAILED` | assignee failure (before ClickUp and comments); comment post failure; `gh issue create` failure | `claim.md:48,93`, `create.md:92` |
| (no code) | usage errors, closed issue, assigned to another login: "not claimed", no writes | `issue.md:52,54-56,58`, `claim.md:41-42` |

Exit codes: `origin_repo.py` 0/1/3/4 and 2 (argparse); `clickup_claim.py` 2 only for bad arguments (the GitHub assignment stays, `claim.md:51`); every other `orca_worktree.py` outcome prints one JSON object and exits 0, exit 2 only for argparse (`OW:11-12`). Warning codes (never STOP; claim `status` stays `success`): 8 worktree codes in rank order `W-ORCA-LIST-FAILED`, `W-ORIGIN-BASE-MISSING`, `W-WORKTREE-CREATE-FAILED`, `W-WORKTREE-AMBIGUOUS`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED`, `W-ORIGIN-BASE-STALE`, `W-FIRST-TAB-LEFT` (`OW:230-239`); 4 launch codes `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `W-L2-ABSENT` (`REMEDY` `OW:802-817`); ccsession note stays first, `also W-L2-ABSENT` goes to `detail` (`claim.md:134`, `OW:1825`).

**`--pipeline` levels**

| Level | What the launched agent does | In code (`orca_worktree.py`) | Source |
|---|---|---|---|
| `worktree` | Orca worktree plus agent; runs `next-steps.md` up to `Plan boundary`, prints the plan path and `Waiting for approval`; a person approves by running a prompt whose first line starts `/sc:implement` or `/task` (the template at `launch-prompt.md:23` also names `/sc:task`; [CODE-CONTRADICTED], the guard regex at `GD:347` does not accept it, see 5.3 and Section 14 D-23); still no commit, push, `/sc:pr-submit` | `--level worktree` (`OW:1873,:1883`); pending word `worktree` | `launch-prompt.md:20-23`, `issue.md:43` |
| `full` | every step; no commit, push or PR; stages nothing; prints `git status --short` | `--level full`; word `full` | `launch-prompt.md:25-26` |
| `full --submit` | adds: no open or merged PR for the branch, conventional commit (stage `.dev/tasks` and changed files, never `.claude/`, never `.dev/issues/`), `git push origin <branch>`, `/sc:pr-submit --monitor 3 ...`, never merge | `--submit` with `--level full`; word `full-submit` (`OW:1759-1761`); `prompt` adds the `submit` block | `launch-prompt.md:28-34`, `issue.md:44` |
| `none` | no worktree, no agent; the claim ends after Wave 6 | not a `--level` value; only `preflight` runs | `issue.md:43,83`, `claim.md:94` |

Default-level rule (prose only, `claim.md:81`; no code): an explicit `--pipeline` wins; if Type, Complexity or Effort estimate cannot be read from `issue-summary.md` the level is `worktree`; else `full` for every bug, `full` for a simple or medium feature of 16 hours or less, `worktree` for a complex feature or one over 16 hours; the printed line is `Level: <L> (explicit)` or `Level: <L> (default: <reason>)`. The watcher always passes `--pipeline none` (`issue.md:48`; `src/superclaude/cli/issue_watch/launch.py:84-92`). **Contradiction [CODE-CONTRADICTED]:** `docs/designs/sc-issue-claim-pipeline-flag.md:21,43,66` still lead with "default `worktree`" before later amendments; `claim.md:81` and `issue.md:43` are the stronger evidence (they are what the model executes). Pinned only as text: `T/skills/test_issue_protocol.py:774`, `:791`; `T/commands/test_issue_command.py:182`.

**orca_worktree.py subcommands** (stdlib only, no shell; timeouts `DEFAULT_TIMEOUT=120`, `PREFLIGHT_TIMEOUT=30`, `TERMINAL_READ_TIMEOUT=15`, env `SC_ORCA_TIMEOUT`, `OW:88-91`; `run()` never raises, `OW:132-166`)

| Subcommand | Behaviour | Evidence |
|---|---|---|
| `preflight` | argv `orca status --json`; prints `{"ok": true}` only when the runtime is reachable, else `{"ok": false, "detail": ...}` | `cmd_preflight` `OW:210-223` |
| `worktree` | find main checkout via `git rev-parse --path-format=absolute --git-common-dir`; `orca worktree list --repo path:<main> --limit 500 --json`; reuse lookup keys in order `marker` (`sc:issue <R>#<N>` in the row comment), `record`, `basename` (`^issue-<N>(-\|$)`), `branch`; none: `git fetch origin`, verify base, create with `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json` (no `--agent`, `--issue`, `--pr`); relist; `finish()` copies `<D>` into `<wt>/.dev/issues/<N>/` (skips `worktree.json`, refuses symlinks, never overwrites a tracked file, a differing untracked file becomes `<name>.prev`); writes `<D>/worktree.json`; closes the first plain tab only for a new worktree | `cmd_worktree` `OW:625-738`, `lookup` `:373-411`, `finish` `:527-563`, `copy_issue_dir` `:439-504`, `close_first_tab` `:568-622` |
| `prompt` | keeps blocks `common` + level (+ `submit`), replaces `<N>`, `<R>`; `kept` (writes nothing) when a launch entry exists and the file exists | `cmd_prompt` `OW:764-784` |
| `launch` | see order below | `cmd_launch` `OW:1696-1834` |
| `pending --level worktree\|full\|full-submit` | writes one pending record, prints `{"ok": true, "nonce": ...}`; meant for a coordinator that starts a worker itself | `OW:1515-1523`; no production caller |

**Launch order ("refuse early, write the record last")**

| Step | Check or action | Failure result | Evidence |
|---|---|---|---|
| 1 | usable worktree record | `failed`, `W-LAUNCH-FAILED` | `OW:1700-1702` |
| 2 | `launch` entry in `<D>/worktree.json` or mirror `<wt git dir>/sc-issue-launch-<N>.json` | `already_launched`, no Orca call | `OW:1704-1721`, `:1586-1616` |
| 3 | worktree `launch-prompt.md` byte-identical to `<D>/launch-prompt.md` | `failed`, `W-LAUNCH-FAILED`, no agent | `stale_prompt` `OW:1666-1693`, `:1722-1724` |
| 4 | IR-4 `enforcement_preflight(wt)` (read-only: `jq`, `uv`, guard commands `cat sed tr mkdir mv ln rm`, Linux process interfaces, `~/.claude/hooks/launch-level-guard.sh` executable with line `# launch-level-guard-version: 1`, `CLAUDE_CONFIG_DIR`, `disableAllHooks`, guard registered on `UserPromptSubmit` and on `PreToolUse` for all 23 `GOVERNED_TOOLS`, identity hook registered for `Bash`) | `failed`, `W-ENFORCEMENT-ABSENT`, no pending record, no agent | `OW:955-1045`, `:1730-1747`, `GOVERNED_TOOLS` `:841-867` |
| 5 | `install_l2(wt)` then `l2_status(wt)`; not `owned` adds a `W-L2-ABSENT` note; `if IR7_REFUSE and l2_notes:` would refuse | with `IR7_REFUSE = False` never refuses | `OW:1754-1758`, `:822` |
| 6 | `publish_pending(word)` writes `~/.claude/state/launch-level/pending/<32-hex nonce>` (dirs 0700, file 0600, `.tmp-<nonce>` then `os.replace`) | `failed`, `W-LAUNCH-FAILED` | `OW:1488-1512`, `:1759-1775` |
| 7 | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` (no `--model`, `--effort`, link flag) | not-ok reply: pending record removed, `failed` with a `hand_command` | `OW:1776-1793` |
| 8 | shim detection `behind_ccsession(handle)`: up to 5 tries, 2.0 s apart (`SC_ORCA_SHIM_INTERVAL`), `orca terminal read --terminal <h> --screen --json` for `[ccsession]` or `Session name (Enter or Ctrl+C`, else `orca terminal show` title regex `sc-launch-v1-<hex>-<MMDD>-<HHMMSS>-<hex4>` | `W-LAUNCH-NOT-CCSESSION` note; launch still counts as `launched`; the agent is not closed | `OW:792-800`, `:1564-1583`, `:1802-1811` |
| 9 | `record_launch` writes `{level, submit, at}`; `session_report` returns `release` text and `layers` | write failure adds text, does not fail | `OW:1619-1643`, `:1445-1485`, `:1814-1833` |

L2 install (`install_l2` `OW:1386-1442`, read-only `l2_status` `:1048-1067`): puts `pre-push` and data file `pre-push.launch-level` into `<git-common-dir>/hooks/`, shared by every worktree of the clone; an existing entry is never replaced; the staged copy is self-tested (`_l2_selftest` `:1278-1332`) before `os.link` (`:1428`); `core.hooksPath` set, hooks dir not the common one, or an unsafe dir gives `unsupported`. [STALE DOC] `claim.md:125` and `sc-issue-claim-pipeline-flag.md:59` say "the worktree's `pre-push` hook" (code: shared hooks dir, `OW:1365,1402`); `claim.md:125` says IR-4 runs "before anything else" (code: record, already-launched and stale-prompt checks run first, `OW:1700-1724`) and names `git rev-parse --git-path hooks/pre-push` (code asks `--git-path hooks`, `OW:1357`); `pending` is not named in `SKILL.md:35`.

**Worker tiers and models**

| Agent file (35 lines each; erratum applied) | `model:` (line 6) | Other frontmatter | Jobs |
|---|---|---|---|
| `AG/issue-worker-t3.md` | `claude-gw-tier2b` | `effort: low` (line 7) | claim lookup (`scout.md`), create lookup, quick body |
| `AG/issue-worker-t2.md` | `claude-gw-tier2` | tools `Read, Grep, Glob, Write, Bash` (line 5; no Edit) | claim Wave 4 simple or medium; quick flag choice; standard flag validation and body |
| `AG/issue-worker-t1.md` | `claude-gw-tier1b` | same tools | claim Wave 4 when scout sizes `complex`; standard and deep flag choice; deep body |

The skill passes only `subagent_type: issue-worker-t<N>`, never `model` (`SKILL.md:54-64`, picker table `:58-62`). The only fallback is T1 to T2, once, on a not-served spawn (`tiers.md:34-42`); T2 and T3 have none. **Contradiction [CODE-CONTRADICTED]:** `docs/designs/sc-issue-command.md:58,107,129,391,423,449` pin T3 to `claude-gw-tier3`; the agent file (`issue-worker-t3.md:6`), `tiers.md:17` (issue 488 decision) and `T/skills/test_issue_worker_agents.py:22-23` say `tier2b`, the stronger evidence; no test scans `docs/designs/`. Proxy behaviour and the model order behind the pins are [UNVERIFIED] (`tiers.md:23-26,36`).

**Local artefacts** (`<D>` = `.dev/issues/<N>/`, never staged, `issue.md:100`): `scout.md`, `clickup.json`, `accuracy-check.md`, `issue-summary.md`, `analysis/analyze-<scope>.md`, `recommend.md`, `next-steps.md`, `launch-prompt.md` (not for `none`), `claim-comment.md`, `worktree.json` (origin checkout only, `{"path","status","launch":{...}}`, atomic 0644; not written for `none`) (`issue.md:80`). Outside `<D>`: the `<wt>/.dev/issues/<N>/*` copy, mirror `<wt git dir>/sc-issue-launch-<N>.json`, `pending/<nonce>` (written by the claim), `<git-common-dir>/hooks/pre-push[.launch-level]`. `sessions/`, `requests/`, `jobs/` are never written by the claim (grep of `OW`).

**Test pins per behaviour** (files under `T/`; read by name, not run)

| Behaviour | Pinning file and key tests |
|---|---|
| Protocol text, waves, file inventory, codes, return contract, default-level text, fork safety | `skills/test_issue_protocol.py` (1055 lines, 62 tests): `test_every_named_path_exists_and_every_file_is_named` :147, `test_st6_preflight_is_in_wave_0_and_worktree_is_wave_7_after_the_posts` :251, `test_every_worktree_warning_code_is_listed_with_a_remedy_line` :350, `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` :560, `test_default_level_rule_is_bug_full_complex_feature_worktree` :791, `test_every_gh_issue_pr_label_mention_carries_repo` :833 |
| Command front: seven flags, STOP rules, version `1.1.0` | `commands/test_issue_command.py` (212 lines, 15 tests): `test_st1_options_table_lists_exactly_the_seven_flags` :84, `test_submit_rule_stops_a_bare_submit_and_keeps_its_message` :191 |
| `orca_worktree.py` against a fake `orca` (create argv, lookup keys, copy rules, launch argv, IR-4, IR-7 warns, shim detection, `pending`) | `skills/test_issue_orca_worktree.py` (2501 lines, 109 tests): `test_la1_launch_argument_list_is_exact`, `test_fo18_exact_commands_and_no_forbidden_flag` :837, `test_ir4_each_failing_condition_refuses_the_launch`, `test_ir7_l2_absent_warns_and_the_launch_proceeds` :1838, `test_la5_launch_shim_check_failure_keeps_the_launch_and_warns`, `test_pending_writes_one_private_record_and_prints_its_nonce` (:2472-2496) |
| L2 install and the IR-7 switch | `skills/test_issue_l2_install.py` (716 lines, 26 tests): `test_ir7_shipped_switch_is_off` :639, `test_hookspath_is_unsupported` :312, `test_l2_status_never_writes` :575 |
| Repo resolution, exit codes 1/3/4 | `skills/test_issue_repo_resolution.py` (291 lines, 18 tests): `test_claim_url_on_another_repo_is_e_foreign_repo`, `test_pull_url_on_origin_is_rejected_not_parsed` |
| ClickUp: the one PUT, no-PUT outcomes, caps, token never printed | `skills/test_clickup_claim.py` (569 lines, 29 tests, 41 collected cases): `test_assign_sends_assignees_add_body` :311, `test_ambiguous_returns_candidates_and_makes_no_put` :277, `test_token_never_printed_on_any_outcome` :548 (its fake server rejects any other request type, :145-146) |
| Worker pins, tools, read-only rules | `skills/test_issue_worker_agents.py` (559 lines, 24 tests): `test_worker_file_exists_with_pinned_picker_id` :77, `test_t3_effort_is_low` :85, `test_tools_exclude_edit` :102; `skills/test_model_alias_policy.py` (249 lines, 11 tests; 4 touch this pipeline, the other seven are repository-wide alias policy): `test_frontmatter_model_is_an_alias_when_present` :83 |
| T1 to T2 fallback | `skills/test_issue_t1_fallback.py` (69 lines, 8 tests) |

**Extension points**

| File | Function or case | What to change | Pinning test file |
|---|---|---|---|
| `CMD`, `claim.md:81`, `templates/launch-prompt.md`, `OW` choices `:1873,:1883,:1891` | add a pipeline level | option rows and STOP rules (`issue.md:43,58`), the level rule, a new block (`BLOCK_MARKER` regex `[a-z]+`, `OW:743`), the three `choices`, then the guard word table `GD:264-269` | `test_issue_protocol.py` (4-block check :295), `test_issue_command.py` :84, `test_issue_orca_worktree.py` |
| `OW` `REMEDY` `:802-817` or `WARNING_ORDER` `:230-239` | add a warning code | the code, its remedy line in `claim.md` (`:106-115`, `:127-132`) and the `SKILL.md` error table (`:161-162`) | `test_every_worktree_warning_code_is_listed_with_a_remedy_line` |
| `AG/issue-worker-tN.md`, `SKILL.md:58-62`, `tiers.md:11-15` | add a worker tier | new agent file with `model:` picker id, tier key in `ccsession-models.json` | `T/skills/test_issue_worker_agents.py:21-26` (`WORKERS`) |
| `SK/templates/`, `SKILL.md:36-50` | add a template | the file plus a files-table row | `test_every_named_path_exists_and_every_file_is_named` |

---

### 5.3 Guard stack and launch levels

**Purpose:** A claim launched at `worktree`, `full` or `full --submit` starts an agent whose permitted actions are limited by a level. The level travels only as files under `~/.claude/state/launch-level/`; a Claude Code hook (L1 guard) reads it on every prompt and tool call, a second hook rewrites governed Bash calls so a git hook (L2) can tell the agent from a person. The prompt text itself (`launch-prompt.md`) is advisory; only L1 and L2 enforce.

**Status lines**

| Piece | Status | Evidence |
|---|---|---|
| L1 guard `launch-level-guard.sh` (808 lines, version line `GD:10`) | BUILT-ON | registered on `UserPromptSubmit` (`HJ:63-71`) and `PreToolUse` (`HJ:115-124`); copied by `install_hooks.py:93`; required by the claim's IR-4 preflight (`OW:975-988`) |
| Job identity `launch-job-identity.sh` (582 lines) | BUILT-ON | `PreToolUse` matcher `Bash`, after the guard (`HJ:125-134`); `install_hooks.py:90`; IR-4 requires it (`OW:1037-1044`); Linux and `uv` needed |
| L2 pre-push hook `launch-level-pre-push.sh` (208 lines) | BUILT-ON, claim-installed only; not in `hooks.json` | template copied to `~/.claude/hooks/` (`install_hooks.py:96`); written into a clone by `install_l2`, called only from `cmd_launch` (`OW:1754`) |
| G2 rule 2 (a bound worker may run `orchestration send` or `ask` only with no `--to`) | BUILT-ON | `GD:485`, `GD:496-537`; plugin copy identical; stated at `WC:66`; pinned by `T/hooks/test_launch_level_guard_worker.py` |
| G1 (a worker started by a coordinator runs with no marker, so no guard) | NOT BUILT as a guard; it is the live condition for such workers | no caller of `orca_worktree.py pending`; the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`; see Section 14) |
| G2 rule 1 / route A (coordinator writes the worker's `.ok`) | REMOVED | zero hits for `release-worker`; guard comment `GD:496-497` says the rule 1 text is retired; the only `.ok` writer left is the guard's typed-prompt branch `GD:358`; see Appendix B |
| G2 route B (signed approval file) | NOT BUILT | no `signature`/`hmac`/`openssl` in `GD` or `ID` |

**Key Files**

| File | Purpose |
|---|---|
| `GD` | L1: binds a pending launch, classifies each tool call, exits 0 or 2 |
| `ID` (bash prologue `:1-54`, embedded Python `:55-581`, `exec uv run --no-project python -I` `:582`) | PreToolUse(Bash) rewriter; `identify`, `prepare`, `run`, `execute` subcommands |
| `PP` (`#!/bin/bash -p`) | git `pre-push` hook: refuses pushes to `refs/heads/main` and `refs/heads/master` from a governed or unknown actor |
| `HJ` (192 lines), `plugins/superclaude/hooks/hooks.json` (154 lines) | registrations |
| `src/superclaude/cli/install_hooks.py` (614 lines) | copies scripts, merges registrations into `~/.claude/settings.json` |
| `src/superclaude/cli/install_ccsession.py` (161 lines), `src/superclaude/skills/ccsession-tag/ccsession-orca` (263 lines) | ccsession wiring and Orca's Claude command; no launch level |

**Which launch paths each layer governs**

| Launch path | Pending record and marker | L1 and L2 | Evidence |
|---|---|---|---|
| `/sc:issue --claim` at `worktree`, `full`, `full --submit` | yes, `launch` writes `pending/<nonce>` and the prompt carries `[sc-launch:v1:<nonce>]` | L1 binds on the agent's first prompt; L2 installed in the clone and consulted on `git push` | `OW:1754-1779` |
| Watcher session (`/sc:issue --claim <N> --pipeline none`) | no: for `none` only `preflight` runs, so no launch step, no `pending` record, no `install_l2`; the watcher prompt pattern has no marker | no L1/L2 binding: the session is ordinary (guard exit 0) | `launch.py:33,84-92` (prompt pattern), `OW` `none` handling (`claim.md:94`), `GD:391` |
| Worker started by a coordinator (`worker-start`) | no: nothing calls `orca_worktree.py pending` and the brief template (`WC:303-311`) has no marker slot (0 hits for `sc-launch`) | no L1/L2 binding; by the code reading a process with no job record is `ordinary` (`ID:228-229`) and `PP` exits 0 at once (`PP:188`) | `docs/designs/sc-issue-launch-level-hook.md:23` says the guard does not govern such a worker (see Section 14) |
| Any other session | no | L1 exits 0 for every event (`GD:391`) | observed S01, S03 |

**Binding state machine** (first prompt binds a pending launch to a session; `GD:314-385`)

```
 claim launch                                   L1 guard, agent's FIRST UserPromptSubmit
 publish_pending --> pending/<nonce> ----------> prompt matches \[sc-launch:v1:([0-9a-f]{32})\]  (GD:318)
   (word: worktree | full | full-submit)           subagent prompt (agent_id set) => exit 0, never binds (GD:315)
                                                   mv pending/<nonce> sessions/.take-<sid>   (one rename wins, GD:372-375)
                                                   ln .take-<sid> sessions/<sid>             (hard link; first binding wins, GD:299-313)
 level word -> W (worktree) | F (full) | FS (full-submit) | other word => "degraded" read as W + LL-STATE note (GD:264-269,306)
 W + typed first line  ^[[:space:]]*/(sc:implement|task)([[:space:]]|$)  => sessions/<sid>.ok  => WA   (GD:347-360)
 release (kill switch): a person deletes sessions/<sid> and sessions/<sid>.ok; approval lasts until then (GD:361)
```

A marker that cannot be bound is `LL-NOBIND` (exit 2): empty session id, unowned or symlinked `sessions/`, no regular session file afterwards (`GD:366-384`). Empty-store fast exit: no `sessions/` directory and no `[sc-launch:` in the input gives exit 0 (`GD:168-173`).

**State stores** (root `$HOME/.claude/state/launch-level/`, three literals `GD:20-23`; the guard reads only `HOME`)

| Path | Writer | Reader | Format |
|---|---|---|---|
| `pending/<32 hex>` | `publish_pending` (`OW:1488-1512`) | guard (`GD:334-337`, `mv` `:374`); claim deletes it on launch failure (`OW:1783`) | one level word, no newline; file 0600, dir 0700 |
| `sessions/<sid>`, `.take-<sid>`, `.tmp-<sid>-<pid>` | guard (`GD:289-313`) | guard, identity `governed()` (`ID:177-186`), `identify` | level word (read as 13 bytes); `degraded` read as W |
| `sessions/<sid>.ok` | guard approval branch, noclobber (`GD:356-359`) | guard (`GD:270`) | empty file; observed mode 600 |
| `requests/<32 hex>` | identity `publish()` (`ID:164-174`) | identity `run`, consumed once under flock | JSON `{session_id, tool_use_id, command}`, 0400 |
| `jobs/<kernel sid>.json` | identity supervisor (`ID:307-375`) | `identify` (`ID:215-260`), `PP` via `identify` | keys `pid, start, boot, kernel_sid, session_id`, 0400 |

No pruning of `pending/` or `sessions/` (design `docs/designs/sc-issue-launch-level-hook.md:627`, owner decision O-15). The installer never creates the store (`install_hooks.py`; the claim and the two hooks do).

**LEVEL MATRIX** (W = `worktree`, WA = `worktree` approved, F = `full`, FS = `full --submit`). Source of decisions: `GD:783-803`; oracle `EXPECTED` `T/hooks/test_launch_level_guard.py:806-854`. Every pin below is a case of `T/hooks/test_launch_level_guard.py::test_grid_policy[<id>]` (:3394); all 16 cells were OBSERVED to match in the run below.

| Level | IMPL (Skill `sc:implement`) | COMMIT (`git commit -m x`) | PUSH (`git push -u origin feature`) | SUBMIT (Skill `sc:pr-submit`, `gh pr comment/create`) |
|---|---|---|---|---|
| W | block `LL-IMPL`; `GRID-IMPL-skill-implement-W` | block `LL-COMMIT`; `GRID-COMMIT-git-commit-W` | block `LL-PUSH`; `GRID-PUSH-git-push-canonical-W` | block `LL-SUBMIT`; `GRID-SUBMIT-skill-pr-submit-W` |
| WA | allow; `GRID-IMPL-skill-implement-WA` | block; `GRID-COMMIT-git-commit-WA` | block; `GRID-PUSH-git-push-canonical-WA` | block; `GRID-SUBMIT-skill-pr-submit-WA` |
| F | allow; `GRID-IMPL-skill-implement-F` | block; `GRID-COMMIT-git-commit-F` | block; `GRID-PUSH-git-push-canonical-F` | block; `GRID-SUBMIT-skill-pr-submit-F` |
| FS | allow; `GRID-IMPL-skill-implement-FS` | allow; `GRID-COMMIT-git-commit-FS` | allow; `GRID-PUSH-git-push-canonical-FS` | allow; `GRID-SUBMIT-skill-pr-submit-FS` |

Other classes (all rows pinned by the same `test_grid_policy` with ids `GRID-<CLASS>-<case>-<level>`; the research gives the class rows, not each id): TURN (Cron*/Schedule* tools) blocks at W only, like IMPL (`GD:786,788`); SKILL (a skill name that cannot be read) blocks at W, WA, F and allows at FS (`GD:787,790`); REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG block at every level including FS (`GD:791-800`). A cell with no match, or an empty level, is `LL-BROKEN` (`GD:801`). So F cannot commit, push or open a PR; only FS can; nothing at any level can merge, push main or master, or make a free-form `gh api` write. Second pins: `test_grid_level_steps` (:3457, ids such as `GRID-step-W-skill-implement`, `GRID-step-F-git-commit`, `GRID-step-FS-git-push`; no WA step); WA is also held by `test_skill_grid_matches_oracle` (:905) and `test_apr_approval_never_unlocks_commit_push_submit` (:3852). Block precedence (first class wins, `GD:783`): BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL.

**Classifiers** (`GD:398-754`)

| Tool | Rule | Evidence |
|---|---|---|
| Skill | name normalised (first word, lower case, strip one `/`, text after last `:`, strip one `sc-` and one `-protocol`); `implement`, `task`, `cleanup` give IMPL; `pr-submit` SUBMIT; `issue` ESCAPE; unreadable SKILL | `GD:398-413`, IMPL line `:409` |
| Bash, Monitor | over 65536 bytes BIG; normalisation NM1a-NM7; TAMPER tokens; ESCAPE words (`ccsession*`, tmux, screen, xdotool, ydotool, `claude` plus a launch flag); orca allow-list; G2 rule 2; git; gh; canonical push | `GD:414-726` |
| git | `merge`, `pull` MERGE; `push` family PUSH; `commit`, `cherry-pick`, `am`, `commit-tree`, `revert` COMMIT; `update-ref` on HEAD, `--stdin`, `refs/heads/*` COMMIT; unknown subcommand or alias/config forms UNKNOWN; only `git push [-u\|--set-upstream] origin <branch>[:<dst>]` is canonical, dst `master`/`main` PROTECTED, `HEAD` or other forms PUSHFORM | `GD:580-725`, regex `:716` |
| gh | `gh api` allowed only as one plain GET else GHWRITE; `merge`, `update-branch`, `sync` MERGE; `pr create/edit/comment/ready`, `issue create/edit/comment` SUBMIT; `pr create` without `-R/--repo <value>` REPO | `GD:550-663` |
| Edit, Write, NotebookEdit | path only (after `/+` squeeze); a `..` segment is TAMPER; contents never read | `GD:727-735` |
| Agent, Task, others | `isolation == remote` ESCAPE; Cron*/Schedule* TURN; RemoteTrigger, Workflow, SendMessage ESCAPE; `mcp__*` write-like suffix MCP (MERGE if it contains merge) unless `list_/get_/search_/read_` | `GD:736-754` |
| TAMPER tokens | `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git`, `.git/hooks`, `hooks/pre-push`, `pre-push.launch-level`, `--no-verify`, `hookspath`, `hook.pre-push`, `install_hooks`, `superclaude ... install` | `GD:440,451,760-775` |

IMPL list: code has three skills (`implement`, `task`, `cleanup`, `GD:409`); the design lists six (`implement`, `task`, `improve`, `cleanup`, `spawn`, `build`, `docs/designs/sc-issue-launch-level-hook.md:106,179,236,391`). [CODE-CONTRADICTED] by the guard, by `ls src/superclaude/commands` (`improve`, `spawn`, `build` absent) and by `test_lookalike_skill_names_stay_none` (`T/hooks/test_launch_level_guard.py:934-936`); the code is the stronger evidence. Pins: `test_impl_name_spellings` :927, `test_skill_grid_matches_oracle` :905.

**Typed approval versus the `/sc:task` mismatch.** The approval regex (`GD:347`) accepts a first line `/sc:implement` or `/task`, not `/sc:task`. `templates/launch-prompt.md:23` tells the agent that a first line starting `/sc:task` also approves. [CODE-CONTRADICTED]: grep of the guard for `sc:task` finds nothing, so a typed `/sc:task ...` does not create `<sid>.ok`; the code is the stronger evidence, and no file says which side is intended (Q-14, see Section 14). Note the Skill-tool classifier still treats a Skill call named `sc:task` as IMPL (blocked at W), so only the typed-prompt release differs. The design row that typed `approved` writes `.ok` (`sc-issue-launch-level-hook.md:123`) is [CODE-CONTRADICTED] by the design's own `:189`, by `GD:347` and by `test_apr_plain_approved_releases_nothing` (:3800).

**Fail-closed versus fail-open; exit codes; block words**

| Rule | Behaviour | Evidence |
|---|---|---|
| Exit codes | L1 and identity use only 0 (allow) and 2 (block); never 1, no `onFailure`; `ll_on_exit` trap turns any other rc into exit 0 (ordinary) or LL-NOBIND / LL-BROKEN exit 2 (governed) | `GD:4-6,135-163`; `ID:435-502,580` |
| Governed means only | valid session id AND `sessions/<id>` exists; a tool call with no governed record exits 0 | `GD:257,391` |
| Fail-open (ordinary session) | missing or invalid session id on a tool event ("identity loss"), no jq or unparseable JSON with no bound id, unrelated event | `GD:208-238,386-391` |
| Fail-closed (governed session) | jq failure on a payload containing a bound id, non-string tool field or NUL, unknown event, internal error, default deny | `GD:218-232,392,807-808` |
| Block words (18) | `LL-IMPL LL-COMMIT LL-PUSH LL-PUSH-FORM LL-PROTECTED LL-MERGE LL-GH-WRITE LL-SUBMIT LL-REPO LL-UNKNOWN LL-MCP LL-ESCAPE LL-TURN LL-TAMPER LL-SKILL LL-BIG LL-NOBIND LL-BROKEN`; LL-TAMPER prints the release `rm` command; notes `LL-STATE`, `LL-TEXT` | `GD:36-133`; pinned by `test_design_table_holds_all_eighteen_ids` (:1712) |
| Hook time limit | `timeout: 5` on both guard registrations and the identity hook; a killed hook allows the call (design V8/R2, not testable here) | `HJ:68,121,131` |

**G2 rule 2.** A bound worker may run `orca orchestration send` or `ask` only as one raw command of plain words and quoted strings, no expansion, no newline, at most 8192 bytes and 64 arguments; any option starting `--to`, `--run`, `--environment` or `--pairing-code`, a name that is a prefix of `--to` or `--run`, a bare word or a lone `--` is ESCAPE (`GD:496-537`, `LL_SA` set at `:485`). Allowed at every level, so a bound worker at W may send. The orca allow-list is `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`; any glob character turns the read verbs into ESCAPE; every other orca call is ESCAPE (`GD:480-491`), except a short help call: a call whose last word is `--help` or `-h`, with no glob character and at most four words counting from `orca` (`orca, two verb words, help`), is allowed (`GD:487-490`; pinned by `test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker`, `orca list --help` and `orca agent launch -h`, `T/hooks/test_launch_level_guard_worker.py:226-230`). Pins: `test_a_bound_worker_may_send_and_ask_its_coordinator` (:74), `test_a_bound_worker_cannot_address_another_worker_or_a_group` (:187), `test_every_other_orca_word_stays_blocked_for_a_bound_worker` (:213), `test_a_forged_release_from_the_workers_own_session_is_blocked_as_tampering` (:262), all in `T/hooks/test_launch_level_guard_worker.py`; doc pin `messages-carry-no-to` (`T/skills/test_worker_contract.py:423-431`).

**orca-ide command-word gap.** The guard matches the basename `orca` only (`GD:457`); grep for `orca-ide` in the guard finds nothing. OBSERVED: a bound session at W ran `orca-ide terminal send --text hi` and `orca-ide orchestration send --to run:run_1 --body hi` with exit 0 (cases EXTRA-2, EXTRA-3), while `orca terminal send` and `/usr/local/bin/orca terminal send` were blocked. `orca-ide` is the default binary of `src/superclaude/cli/sweep/probes.py:43` and first in `src/superclaude/cli/install_user_setup.py:36`. `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:83` already records this as a DEFECT with a draft plan; no decision to fix was found (D-25, Section 14.2.1). Consequence: G2 rule 2 and the ESCAPE class do not constrain the `orca-ide` spelling.

**Job identity** (`ID`; not a sandbox, `ID:2`)

| Item | Behaviour | Evidence |
|---|---|---|
| Rewrite | PreToolUse(Bash) only; once `sessions/<sid>` exists, replaces the command with `shlex.join(['/bin/bash', script, 'execute', sid, tool_use_id, original])` through `hookSpecificOutput.updatedInput`; sets no `permissionDecision` | `ID:430-505`, output `:491-497` |
| Silent (exit 0) | input over 1 MiB, unparseable JSON, tool other than `Bash` (Monitor has no adapter), invalid session id, no session record, no `HOME` or store | `ID:20-24,433-453` |
| Closed (exit 2) | governed Bash call that cannot be wrapped: stderr `launch job: governed Bash call cannot be wrapped safely`; no `uv`: `launch job: UV is required for this invocation`; other: `launch job: invalid invocation or unavailable private state` | `ID:25-54,500-502,572-580` |
| `identify [PID]` | one JSON line: `ordinary`, `ordinary`+`released`, `governed`+`session_id`, `unknown` (with reason `stale\|orphaned\|foreign\|unreadable`) | `ID:215-260,546-553` |
| Declared limits | `setsid` or daemonising escapes selection; Monitor and pipelines unsupported; `cd` does not persist across governed Bash calls; ordering with other hooks unspecified | `ID:7-18` |

Writes to GitHub: none in the identity hook. Pins: `T/hooks/test_launch_job_identity.py` (1530 lines, 56 tests), `T/hooks/test_launch_level_guard_with_identity.py` (212 lines, 5 tests; Linux only; the guard must see the original command, :135; a `degraded` record blocks all Bash through the identity hook, :187).

**L2 pre-push hook** (`PP`): installed by the claim (`install_l2`, `OW:1754`) as `<git-common-dir>/hooks/pre-push` next to data file `pre-push.launch-level` (line 1 pinned `HOME`, line 2 `uv` directory); it is a git hook, not a Claude Code hook, so it is not in `hooks.json`, and a plain `superclaude install` only copies the template (`install_hooks.py:96`). Actor from `ID identify $$` under `env -i`, `timeout 10`; ordinary exits 0 at once (`PP:188`); protected refs `refs/heads/main` and `refs/heads/master` only (`PP:17`); governed plus protected `L2-PROTECTED` exit 1; unknown actor plus protected `L2-UNKNOWN` exit 1; malformed record from a non-ordinary actor `L2-MALFORMED` exit 2; pushes to other refs allowed for every actor (`PP:187-208`). It is the only hook here that exits 1 (`PP:9-10`). The feature-branch push control (commit, push, submit) lives in L1 only. Pins: `T/hooks/test_launch_level_pre_push.py` (1194 lines, 34 tests), `test_launch_level_pre_push_records.py` (230 lines, 8 tests).

**Registrations and installer** (`HJ`)

| Event | Matcher | Command | Timeout | Lines |
|---|---|---|---|---|
| UserPromptSubmit | none | `~/.claude/hooks/launch-level-guard.sh` | 5 | `HJ:63-71` |
| PreToolUse | `^(Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Monitor\|Workflow\|RemoteTrigger\|SendMessage\|Cron[A-Za-z]*\|Schedule[A-Za-z]*)$\|^mcp__.*(merge\|push\|commit\|pull_request\|create_or_update_file\|delete_file\|update_ref\|create_ref\|create_branch)` | same guard | 5 | `HJ:115-124` |
| PreToolUse | `Bash` | `~/.claude/hooks/launch-job-identity.sh` (after the guard in file order) | 5 | `HJ:125-134` |

`install_hooks(target_path=None, force=False)` copies scripts to `~/.claude/hooks/` skip-if-exists unless `force` (`install_hooks.py:282-289`), merges registrations additively by command-path ownership, keeps the identity hook last (`:460-473`), writes `settings.json.bak.<UTC stamp>` first and refuses a malformed target (`:336-367`). Callers: `main.py:219` (install, `force` flag), `main.py:412` (update, `force=True`), `cli/eval/hook_adapter.py:230` (`force=False`). So a plain install keeps an older guard on disk; update or `install --force` refreshes it, and IR-4 refuses a guard without the version line (`OW:986-988`). A governed agent cannot re-run the installer (TAMPER, `GD:440,451`). Plugin copies: the three scripts are byte-identical (`cmp -s`; pinned by `T/hooks/test_launch_level_guard_l2_tokens.py:149`, `T/cli/test_install_hooks.py:1086-1109`); the plugin `hooks.json` has the same three launch-level registrations but also lacks the ccsession-tag entries, the `pragmatic-subagent.js` SubagentStart entry, and carries `"async": true` on `freshness-subagent-start.sh` (the scope hint saying "only ccsession-tag entries" is [CODE-CONTRADICTED], verified by `diff`). Registration pins: `T/hooks/test_launch_level_guard_registration.py` (127 lines, 7 tests).

**ccsession coupling.** The ccsession shim carries NO launch level: grep for `launch-level|sc-launch|LAUNCH_LEVEL|launch_level` over `src/superclaude/skills/ccsession-tag` returns zero lines; `ccsession-orca` sets `CCSESSION_ORIGIN` and unsets `CCSESSION_NAME`/`CCSESSION_ASK_TIMEOUT` (`ccsession-orca:198-256,249`) and never touches the store; `install_ccsession.py` registers no hooks and has no launch-level text (`install_ccsession.py:11-142`). The level travels only by files: `pending/<nonce>` then marker `[sc-launch:v1:<nonce>]` then `sessions/<sid>`. The claim only DETECTS the shim after launch (`behind_ccsession`, `OW:1564-1583`) and warns `W-LAUNCH-NOT-CCSESSION` (a warning, not a refusal); without the shim the guard still binds through the prompt marker. The shim passes the prompt through, which is how the marker reaches Claude and why the tab title starts `sc-launch-v1-<nonce12>-...` (`OW:793-797`). The word "shim" also names ccsession's `--shim` model-alias proxy; the claim does not check that proxy (Q-20). No test pins "the shim carries no level" (grep over `T/` finds none in ccsession test files).

**Ledger of guard items**

| Item | Status | Evidence |
|---|---|---|
| G1 (coordinator-started worker has no marker, so no guard) | NOT BUILT (as a guard) | see launch-path table; `docs/designs/sc-issue-launch-level-hook.md:23` says the guard does not govern such a worker |
| G2 rule 1 / route A | REMOVED | `GD:496-497`; `CHANGELOG.md:17` records the removal; see Appendix B |
| G2 rule 2 | BUILT-ON | `GD:485,496-537` |
| FU-1 (first live-test runbook for the claim hand-off) | REMOVED (its run steps name commands that no longer exist); the file's RECORDED lines a-k dated 2026-11-17 remain as text, [UNVERIFIED] | `docs/designs/issue-pipeline-fu1.md:64,108-119`; no `issue_pipeline` in `cli/main.py` |
| IR-3 `pipeline.json` | NOT BUILT | `sc-issue-launch-level-hook.md:34,615`; grep empty |
| IR-4 enforcement preflight | BUILT-ON | `OW:955-1045`, refusal `:1730-1747` |
| IR-7 refusal when L2 is not owned | BUILT-OFF | `IR7_REFUSE = False` `OW:822` (comment "owner decision 2026-11-08", turn on only after the #442 observations pass); `T/skills/test_issue_l2_install.py:639-641` |
| OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX (live observations) | NOT BUILT (never run) | `T/hooks/test_launch_level_observations.py:79-84`: one test parametrized over 12 entries, body `pytest.skip(...: needs a real governed session and has not been run)`; design `sc-issue-launch-level-hook.md:6,625` "Pending, none run"; no code reads an observation record (see Section 14) |

**Observation run (OBSERVED versus READ-ONLY-READING).** OBSERVED: the unmodified guard script from the snapshot was run against 44 sample payloads with `env -i HOME=<sandbox> PATH=/usr/bin:/bin` (bash 5.2.37, jq 1.7; sandbox `research/05-guard-run-sandbox/` inside the task folder; `find -newer` found no change under the snapshot). All 44 matched the code reading: the 16 matrix cells; binding for W, F, FS and a `badword` record (became `degraded`); typed approval `/sc:implement x` creating `gov-w.ok` (mode 600) and moving W to WA; PROTECTED, MERGE and REPO blocked at FS; G2-A and G2-B allowed, G2-C (`--to`) and G2-D (`orca terminal send`) blocked; TAMPER on `rm -rf ~/.claude/state/launch-level`; fail-open for an ordinary id, identity loss, non-JSON with an ordinary id, event `Stop` for an ordinary session; fail-closed for non-JSON with a bound id (LL-BROKEN), marker in non-JSON (LL-NOBIND), event `Stop` for a bound session; the `orca-ide` gap. READ-ONLY-READING (not run): the identity hook, the L2 hook (they need `uv`, a live supervisor and git state outside the sandbox), the claim, both installers, the live observations OB-H1..3 and OB-CTX; no pytest was run.

**Test pins** (files under `T/`; 14 files in the research table plus 3 claim-side files, 17 in all; counts by `grep` of `def test_`)

| File | Pins |
|---|---|
| `hooks/test_launch_level_guard.py` (4631 lines, 162 tests) | binding B1-B13, classifiers, `test_grid_policy` :3394, `test_grid_complete` :3401, `test_precedence_order` :4520, 18 message texts, typed approval `test_apr_matching_prompt_writes_ok_at_w` :3737 |
| `hooks/test_launch_level_guard_l2_tokens.py` (160, 7) | hook-file and `--no-verify`/`hookspath` TAMPER tokens; mirror byte-identical :149 |
| `hooks/test_launch_level_guard_registration.py` (127, 7), `test_launch_level_guard_with_identity.py` (212, 5), `test_launch_level_guard_worker.py` (300, 11) | registrations; guard with identity; G2 rule 2 |
| `hooks/test_launch_job_identity.py` (1530, 56), `test_launch_level_pre_push.py` (1194, 34), `test_launch_level_pre_push_records.py` (230, 8) | identity; L2 matrix T-01..T-24 |
| `hooks/test_launch_level_observations.py` (84, 6) | nine fixtures, log-only probe; 12 skipped live cases |
| `cli/test_install_hooks.py` (1246, 37), `unit/test_install_ccsession.py` (417, 22), `core/test_orca_session_launch_guidance.py` (62, 3), `unit/test_ccsession_tag.py` (7101, 277), `unit/test_ccsession_tiers.py` (3821, 149) | installer; ccsession wiring and wrapper (no launch-level content) |
| claim-side: `skills/test_issue_l2_install.py`, `skills/test_issue_orca_worktree.py`, `hooks/test_require_orca_worktree_agent_governed.py` (56, 1) | L2 install, launch; governed-session block of bare `worktree create` |

**Extension points**

| File | Function or case | What to change | Pinning test file |
|---|---|---|---|
| `GD:783-803`, `ll_say` `:36-133` | add or change a block class or word | decision table, message, then the oracle `EXPECTED` | `hooks/test_launch_level_guard.py` (:806-854, :1712, :4520) |
| `GD:409` | add an IMPL skill | the `implement\|task\|cleanup` case | `test_impl_name_spellings` :927, `test_skill_grid_matches_oracle` :905 |
| `GD:480-491`, `GD:496-537` | add an allowed orca verb or change G2 rule 2 | allow-list or rule | `hooks/test_launch_level_guard_worker.py` :213, :187 |
| `GD:760-775` | add a TAMPER token | token list | `hooks/test_launch_level_guard_l2_tokens.py` |
| `HJ:115-124`, `OW:841-867` | guard a new tool name | matcher and `GOVERNED_TOOLS` (IR-4 checks every one) | `hooks/test_launch_level_guard_registration.py:68` |
| `GD:10`, `PP:2`, `install_hooks.py:90-96`, plugin copies | change a hook script | bump the version line, keep plugin copies byte-identical | `cli/test_install_hooks.py:1086-1118` |

---

### 5.4 Coordinator contract text (`WORKER-CONTRACT.md`)

**Purpose:** `WC` (339 lines) is the text a supervised coordinator and its workers follow. Sections: `## 1. Terms` :9, `## 2. Command-side rules` :27, `## 3. Worker-session duties` :49, `## 4. Coordinator rules` :68, `## 5. Coordinator brief template` :299. This subsection records what it says about the issue pipeline today: nothing issue-specific. The contract is documentation text; the technical reference states that no code runs the coordinator loop or distinguishes a coordinator from a worker (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:186`, doc claim, [UNVERIFIED] by the research).

**Rules present (WC-2 to WC-16: 15 rules; there is no WC-1)**

| Rule | Line | Content |
|---|---|---|
| WC-2 | 31 | no person-blocking step under `--unattended`; each gate resolves to a documented default, caller flag, or blocked |
| WC-3 | 53-58 | questions go to the coordinator; ask at most once per Task; a Ruling halt (`E-HALT-QA`, `E-NO-RULING`) is never asked; the person gives a Ruling in chat |
| WC-4 | 32-39 | one `return-contract.yaml` per outcome in the one report directory the brief names |
| WC-5 | 59 | worker sends `worker_done` once; `failed` for `failed`/`blocked`/no contract, `succeeded` for `succeeded`/`partial` |
| WC-6 | 72-80 | every retry is a new Task (never `worker-start --retry-of`); three-failed-starts cap |
| WC-7 | 60 | run at top level, never inside a subagent |
| WC-8, WC-13 | 40, 62 | a command or worker never calls `worker-start`, `dispatch`, `task-create` (WC-13 adds `worktree create --agent`, `agent launch`) |
| WC-9 | 41-45 | no outward action from a worker; only git write a brief may authorize is an end-of-Task local commit; coordinator stages `.dev/tasks` |
| WC-10, WC-11 | 46, 47 | liveness heartbeats, waits of at most 4 minutes; parallel-safe writes |
| WC-12, WC-14, WC-15 | 61, 63, 64 | follow-ups pulled and acked; no turn ends between chain steps; context-safe reading and handoff files |
| WC-16 | 287-289 | coordinator loop: never stops watching its Run, re-arms waits, runs the sweep and read-only `/sc:sweep` on each wake, escalates a closed list of states to the person; "Phase 1 adds this duty, not a scheduler" |

**Explicit finding.** `WC` has no WC-17 and no heading or sentence "Issue pipeline duties" (0 grep hits each), and no "issue pipeline", "watcher", "adopt", "claim" or "COORD-" text; "dispatcher" and "zero-setup watcher" are likewise not found in snapshot. The removal is recorded at `CHANGELOG.md:17` (see Appendix B). Several documents still name the missing section as live: `docs/designs/issue-watcher-setup.md:170` and `docs/designs/issue-watcher.md:43` [CODE-CONTRADICTED / STALE DOC], and `docs/designs/issue-pipeline-guard-g2-no-to.md:48` tells an editor to edit a rule that does not exist.

**Issue-related lines in the contract** (grep of `issue`, `grant row`)

| Line | Text | Relevance |
|---|---|---|
| 23 | `/sc:issue` is on the never-as-worker list (with `/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:sweep`, `/sc:swarm-wizard`): never dispatched as a worker, no `--unattended` | the claim command may not run as a worker |
| 57 | WC-3 sub-bullet: "other owner records, such as a grant row or a pass record, are still written by the owner" | the phrase "grant row" occurs exactly once; the contract defines no store, writer verb or schema for it (a grep finds it also at `docs/designs/issue-pipeline-fu1.md:24,26`); no decision found in the files this reference cites about retiring it |
| 66 | "Messages carry no `--to`": a worker's `ask` and `send` carry no `--to`; the launch-level guard blocks any `--to` from a bound worker | the contract side of G2 rule 2 (see 5.3) |
| 242-243 | Git and GitHub ownership: actions target `IronbellyOrg/IronClaude`, never upstream, never through Orca issue or PR linking; "Progress posts (issue comments, project fields)" are coordinator actions; workers report only by heartbeats and `worker_done` | the only text on coordinator issue comments; names no issue-number source and no watcher |
| 258, 289 | "The coordinator starts only Tasks it created itself"; a ready Task it did not create is reported to the person (WC-16 lists it as an escalation) | bounds what a coordinator may start |

**Who starts a worker after a claim: not defined.** No contract rule says that a coordinator adopts a claimed issue, reads `.dev/issues/<N>/issue-summary.md` or `next-steps.md`, creates the issue worktree or starts a worker. The technical reference says so directly at `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`: the section "Issue pipeline duties" "was removed in issue 655 ... and until [its replacement] lands no contract rule says who starts that worker" [CODE-VERIFIED by reading the line]. The command side of the hand-off is prose only (`issue.md:85`, `SKILL.md:140`, `claim.md:96`: run `orca_worktree.py worktree`, then `worker-start --worktree path:<printed path>`); no Python in `src/` calls `worker-start` or `task-create`. Status: NOT BUILT (see Section 14). The binding of such a worker to the guard is the G1 row in 5.3; the brief template (`WC:299-312`) has no launch-marker slot. [STALE DOC] the same reference states "WC-2 to WC-15 ... 327-line contract" (`:196`) and ranges `:67-282`, `:283-327` (`:285`); the snapshot has WC-2 to WC-16, 339 lines, coordinator rules `:68-297`, template `:299-339`; its "739 tests" for the contract test (`:208`) is [UNVERIFIED] (the file has 59 `def test_`).

**Test pin.** `tests/skills/test_worker_contract.py` (3220 lines, 59 tests) pins the contract as text: `RULE_PHRASES` (:25-436, about 80 entries incl. WC-2 to WC-16, `messages-carry-no-to` :423-431), consumed by `test_contract_states_rule` (:876-878); the never-as-worker list including `/sc:issue` (:444-454); a write-verb audit of `src/superclaude/{skills,commands,agents}` (:1840-3141) that classifies the issue flow as read-only or never-worker (`agents/issue-worker-t*.md` :2890-2913, `sc-issue-protocol` :2914-2960, orchestrator-writes-only statement :3021); and `test_the_no_to_rule_sits_in_the_worker_session_duties` (:3216-3220). It contains no WC-17, "Issue pipeline duties", `issue-pipeline` or `watcher` text (0 grep hits) and has no test of absence.

**Open items for this subsection (all listed in Section 14 and in the gap log):** whether OB-H1 item 1, OB-H2, OB-H3 have passed (U-4, D-21); who runs `orca_worktree.py pending` (U-6, D-18); which side of the `/sc:task` mismatch is intended (D-23); whether coordinator-started workers should be bound (D-18); whether the guard should recognise `orca-ide` (D-25); live behaviour of the Orca flags, tier models and FU-1 RECORDED lines remains [UNVERIFIED] (U-5, U-7).

---

## 6. State Management

The pipeline has no client-side state. Its state is three on-disk stores, each with its own writer. Shorthand as in Section 3. Mode is the file mode set by the writer.

| Store | Path pattern | Writer | Readers | Format and key fields | Notable behaviour and mode |
|-------|--------------|--------|---------|-----------------------|----------------------------|
| 1. Watcher state directory | `<state_dir>/`, default `${XDG_STATE_HOME:-~/.local/state}/superclaude/issue-watch/` (`P/cycle.py:187-192`) | `init-state` creates it (`P/record.py:753-802`) | all verbs | directory | mode 0700; a network filesystem is refused at config load (`P/cycle.py:270-272`); a lost directory loses the at-most-once memory |
| 1a. `dispatch.json` | `<state_dir>/dispatch.json` | `FileStore.save`: init-state, real cycles (`P/cycle.py:603, 747, 1092, 1097, 1143`), `reset` (`P/cli.py:224-229`) | `FileStore.load` (`P/cycle.py:742`; `P/cli.py:241`); `status` reads it without the lock (`P/cycle.py:1231-1248`); no other reader found in snapshot | JSON, sorted keys, indent 2, ASCII. Seven top-level keys: `schema_version` (1), `created_at`, `next_permitted_at`, `last_completed_cycle_at`, `considered`, `consumed_log`, `entries`. Each entry has 17 fields: `issue`, `state`, `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `approved_at`, `launch_cwd`, `launch_login`, `launch_account_id`, `consumed_at`, `pending_at`, `created_at`, `updated_at`, `lease_expires_at`, `last_reason`. Six states: `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed` | mode 0600; atomic write (temp file, fsync, `os.replace`, directory fsync); `pending` is saved before the launch call; any extra or missing key makes the store `store_invalid` (exit 6); `claimed` is terminal; `launch_login` and `launch_account_id` have no reader (`P/record.py:69-131, 168-244, 370-378`) |
| 1b. `lock` | `<state_dir>/lock` | nobody writes bytes; `init-state` creates it | `FileStore.lock` (`P/cycle.py:695`) | empty file used for `flock` | mode 0600; must be a regular file owned by the euid, opened `O_NOFOLLOW`; held by another run gives exit 75 (`P/record.py:380-419`) |
| 1c. `DISABLED` | `<state_dir>/DISABLED` | the operator (`touch`) | `store.disabled()` (`P/cycle.py:712, 1063`); `status` uses its mtime | existence only | any type counts for the cycle (`os.path.lexists`); `status` shows `disabled since: no` for a dangling symlink (`P/record.py:421-431`, open question Q-08 in U-10, Section 14.3.1) |
| 1d. `audit.jsonl`, `.1` to `.4` | `<state_dir>/audit.jsonl*` | `AuditLog.append` from `_conclude` (`P/cycle.py:1200`) and `cli._write_reset` | none in code: `status` does not read it, `slo_numbers` has no production caller (`P/cycle.py:1279-1284, 1359`) | one sorted-key ASCII JSON object per line; kinds `cycle`, `decision`, `warning`; closed reason table | mode 0600; rotated at 5 MiB keeping four files, only with the lock held (`P/audit.py:106-156`); [CODE-CONTRADICTED] `docs/designs/issue-watcher.md:406` (written by every exit, read by `status`) |
| 1e. `dry-run.json` | `<state_dir>/dry-run.json` | `save_dry_run`, dry-run only (`P/cycle.py:1146-1162`) | `load_dry_run`, dry-run only (`P/cycle.py:727`) | JSON `{schema_version, considered, shadow_launches}` | mode 0600; an invalid file is replaced and warns `dry_run_shadow_reset` (`P/record.py:831-865`) |
| 1f. temp file | `<state_dir>/dispatch.json.<random>.tmp` | `write_prepared_bytes` | none | transient | an orphan after a hard crash is never removed (open question Q-06 in U-10, Section 14.3.1; D-13) |
| 2. Launch-level store | `~/.claude/state/launch-level/` | created by the claim (`publish_pending`) and the guard; the installer never creates it | see rows 2a to 2e | directories | dirs 0700; no pruning of `pending/` or `sessions/` (`docs/designs/sc-issue-launch-level-hook.md:627`) |
| 2a. `pending/<32 hex nonce>` | `pending/<nonce>` | `publish_pending` via `launch` or `pending` (`SK/scripts/orca_worktree.py:1488-1512`) | L1 guard renames it (`H/launch-level-guard.sh:334-337, 374`); the claim deletes it if the launch fails (`:1783`) | one word: `worktree`, `full` or `full-submit`, no newline | file 0600, written as `.tmp-<nonce>` then `os.replace`d; consumed once |
| 2b. `sessions/<session_id>` | `sessions/<sid>` | L1 guard: hard link of the taken pending record (`:299-313`) or the word `degraded` (`:289-297`) | guard (`:257-273`); job identity `governed()` (`H/launch-job-identity.sh:177-186`); L2 through `identify` | one level word, read as 13 bytes; `degraded` reads as level W with a note | same inode as the pending record; first binding wins; removed only by a person |
| 2c. `sessions/<sid>.ok`, `.take-<sid>`, `.tmp-<sid>-<pid>` | `sessions/` | L1 guard (`:356-359, 372-376, 289-297`) | guard (`:270`) | `.ok` is empty, existence means approved; the dot files are temporary | `.ok` only at level W; dot names are never valid session ids |
| 2d. `requests/<32 hex token>` | `requests/` | job identity `publish()` (`H/launch-job-identity.sh:164-174`) | `run` consumes it under flock (`:378-385`) | JSON `{session_id, tool_use_id, command}` | mode 0400; single use |
| 2e. `jobs/<kernel-sid>.json` | `jobs/` | job identity supervisor (`:307-375`) | `identify` (`:215-260`), so L2 too | JSON keys `pid`, `start`, `boot`, `kernel_sid`, `session_id` | mode 0400; removed when no member process remains |
| 3. Claim artefacts | `.dev/issues/<N>/` in the checkout that ran the claim | see rows below | the orchestrator, the launched agent | markdown and JSON | never staged or committed (`src/superclaude/commands/issue.md:89-102`) |
| 3a. Worker output | `scout.md`, `accuracy-check.md`, `issue-summary.md`, `analysis/analyze-<scope>.md` | workers t3 (scout), t2 or t1 (the rest) | orchestrator; the level rule reads `issue-summary.md` | markdown from templates | written with the Write tool; "only under `.dev/issues/`" is a prose rule (`src/superclaude/agents/issue-worker-t*.md:30`) |
| 3b. Orchestrator output | `clickup.json`, `recommend.md`, `next-steps.md`, `claim-comment.md` | orchestrator (`clickup.json` is the script's stdout) | orchestrator; launched agent | one JSON object; markdown | `claim-comment.md` and `accuracy-check.md` are the posted bodies |
| 3c. Script output | `launch-prompt.md`, `worktree.json` | `orca_worktree.py prompt`; `write_record`, `record_launch` (`SK/scripts/orca_worktree.py:507-524, 1619-1643`) | `cmd_worktree`, `cmd_launch`, `cmd_prompt`; `stale_prompt` compares copies | `worktree.json` is `{"path","status","launch":{"level","submit","at"}}` | atomic write, mode 0644; `worktree.json` is never copied into the worktree and is not written for `--pipeline none` |
| 3d. Worktree copy and mirror | `<wt>/.dev/issues/<N>/*`; `<wt git dir>/sc-issue-launch-<N>.json` | `copy_issue_dir` (`:439-504`); `record_launch` (`:1634-1642`) | launched agent; `read_mirror` (`:1600`) | copy of 3a to 3c except `worktree.json`; mirror `{"path","launch"}` | copy refuses symlinks, never overwrites a tracked file, keeps a differing untracked file as `<name>.prev` |

Outside the three stores: the config file (`~/.config/superclaude/issue-watch.json`) and the approvers file are written only by the operator and read-only to the code; the claim also writes the L2 hook `<git-common-dir>/hooks/pre-push` and `pre-push.launch-level` (`SK/scripts/orca_worktree.py:1386-1442`).

---

## 7. Component Inventory

N/A - not a UI feature. The issue-to-work pipeline is a command-line poller, a prose protocol run by the model, three helper scripts and shell hooks; it has no rendered screens, components or client-side stores. The file inventory is in Section 3 and the on-disk state in Section 6.

---

## 8. API & Integration Points

Conventions for Sections 8 to 11. Paths are repository-relative against the 61ac2c2e6 snapshot. `P` = `src/superclaude/cli/issue_watch/`; `SK` = `src/superclaude/skills/sc-issue-protocol/`; `HK` = `src/superclaude/hooks/scripts/`. Status words are only BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. Tags: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED].

The pipeline has no HTTP endpoint of its own. Its integration surface is a set of subprocess commands (`gh`, `git`, `orca`, `uv`, `jq`), one ClickUp REST call, files under `~/.claude/state/launch-level/`, and Claude Code hook registrations. The watcher part writes nothing to GitHub: all seven `gh` argv are reads (`P/github.py:107-108`, `:206`, `:257`; greps in research 01 section 13 and research 02 section 7(c)).

### 8.1 External Commands (every `gh`, `orca`, ClickUp and git command)

**Watcher (BUILT-OFF (enabled:false) for real cycles; `once --dry-run` runs the same reads and BUILT-ON).** Every argv runs through `SubprocessRunner.run` with `shell=False`, stdin `DEVNULL`, a mandatory timeout (`P/runner.py:91-101`). Repository literal: `REPO = "IronbellyOrg/IronClaude"` (`P/github.py:37`).

| Piece | Command (exact argv or command line) | R/W | Actor | File:line |
|---|---|---|---|---|
| G1 login | `["gh","api","user","--include"]` | Read | watcher | `P/github.py:175-177`; call `P/cycle.py:755` |
| G2 discovery | `["gh","issue","list","--repo","IronbellyOrg/IronClaude","--state","open","--label",<trigger>,"--assignee",<login>,"--json","number,labels,assignees,state","-L","100"]` | Read | watcher | `P/github.py:180-198`; `P/cycle.py:796` |
| G3 events (G3' = reserved) | `["gh","api","--method","GET","repos/IronbellyOrg/IronClaude/issues/<N>/events","-F","per_page=100","-F","page=<P>","--jq",EVENTS_JQ]` | Read | watcher | `P/github.py:201-220`; `P/cycle.py:907, 944, 996` |
| G4 claim-marker comments | same shape on `.../issues/<N>/comments` with `--jq MARKER_JQ` (body reduced to a boolean) | Read | watcher | `P/github.py:223-225`; `P/cycle.py:905, 926, 942` |
| G5 edits | `["gh","api","graphql","-f","query=<EDITS_QUERY>","-F","number=<N>"]` plus `["-f","after=<cursor>"]` from page 2 | Read (GraphQL query; POST by design) | watcher | `P/github.py:228-244`; `P/cycle.py:948` |
| G6 project items (G6' = reserved) | `["gh","api","graphql","-f","query=<PROJECT_ITEMS_QUERY>","-F","number=<N>"]` plus optional cursor | Read | watcher | `P/github.py:228-249`; `P/cycle.py:957, 1013` |
| G7 re-read | `["gh","api","--method","GET","repos/IronbellyOrg/IronClaude/issues/<N>","--jq",REREAD_JQ]` | Read | watcher | `P/github.py:252-262`; `P/cycle.py:983` |
| Origin check | `["git","-C",<worktree>,"remote","get-url","origin"]` | Read | watcher | `P/launch.py:244`; `P/cycle.py:721, 1074` |
| Orca discovery | `[<abs path of orca-ide, then orca>,"skills","list","--json"]`; accepted only if topic `orca-cli` is listed | Read (local; the doc's "no runtime contact" claim is [UNVERIFIED]) | watcher | `P/launch.py:163-203`; `P/cycle.py:1048` |
| The one Orca launch (12 elements) | `<orca> agent launch --agent claude --worktree path:<abs worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json`, run with `cwd=<worktree>` | Write (starts a Claude session) | watcher | `P/launch.py:95-116, 358-370`; `P/cycle.py:1099` |
| Retry argv (printed only) | the launch argv with `--retry-launch <op-id>` before `--json` (14 elements) | none (printed by `status`; nothing runs it; automatic retry NOT BUILT) | `status` | `P/launch.py:119-132`; `P/cycle.py:1308-1312` |

**Claim (`/sc:issue --claim`; every write is made by the orchestrating model, workers are read-only).** `<R>` comes from `origin_repo.py` only (`SK/SKILL.md:72-73`).

| Piece | Command | R/W | Actor | File:line |
|---|---|---|---|---|
| C1 assign | `gh issue edit <N> --repo <R> --add-assignee @me` | Write | orchestrator, Wave 3 | `SK/refs/claim.md:48`; `SK/SKILL.md:74` |
| C2 ClickUp assign | `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"`; the one non-GET request is `PUT https://api.clickup.com/api/v2/task/{task_id}` body `{"assignees": {"add": [<user id>]}}` | Write (only if one task matches) | orchestrator runs script | `SK/scripts/clickup_claim.py:232-237`; `SK/refs/claim.md:50` |
| C3 / C3' accuracy comment | `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`, or `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | Write | orchestrator, Wave 6 | `SK/refs/claim.md:89, 91` |
| C4 / C4' claim comment (ends with the marker) | `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md`, or the same `gh api -X PATCH` form | Write | orchestrator, Wave 6 | `SK/refs/claim.md:92` |
| Claim reads | `git remote get-url origin`; `gh auth status`; `orca status --json`; `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name`; `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author`; `gh api user -q .login`; `gh pr list --repo <R> --state merged --search "merged:>=<date>" --limit 200 --json number,title,mergedAt,files,url`; `git fetch origin` (the only worker git write); `git log --since=<createdAt> --name-only origin/<B>`; ClickUp `GET /user`, `GET /team/{ws}/task?page&subtasks=true&include_markdown_description=true[&list_ids[]]` | Read | origin_repo.py, orchestrator, T3 worker, clickup_claim.py | `SK/scripts/origin_repo.py:159-164`; `SK/refs/claim.md:16-29`; `clickup_claim.py:176, 185-191` |
| Create path X1-X3 (not the claim) | `gh issue create --repo <R> --title "[FEATURE\|BUG] <title>" --body-file ... [--label ...] [--type ...]`; `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`; `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md` | Write | orchestrator, Wave 5 | `SK/refs/create.md:92-96`; `SK/SKILL.md:103` |
| Worktree step | `git rev-parse --path-format=absolute --git-common-dir`; `orca worktree list --repo path:<main> --limit 500 --json`; `git fetch origin`; `git rev-parse --verify <base>`; `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json` (no `--agent`, no `--issue`, no `--pr`); `git -C <wt> ls-files .dev/issues/<N>`; `orca terminal list --worktree path:<wt> --json`; `orca terminal close --terminal <handle> --tab --json` | Write (create, close first tab) | `orca_worktree.py worktree` | `SK/scripts/orca_worktree.py:287-291, 314-350, 684-700, 568-622` |
| Preflight | `orca status --json` (30 s); passes only with `ok` true and `runtime.reachable` true | Read | `orca_worktree.py preflight` | `orca_worktree.py:210-223` |
| Governed launch | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` (no `--model`, `--effort` or link flag) | Write | `orca_worktree.py launch` | `orca_worktree.py:1776-1779` |
| Shim check | `orca terminal read --terminal <h> --screen --json` then `orca terminal show --terminal <h> --json`, up to 5 tries, 2.0 s apart | Read | `orca_worktree.py launch` | `orca_worktree.py:1564-1583, 1551-1561` |
| L2 install probes | `git -C <wt> config --get core.hooksPath`; `git rev-parse --path-format=absolute --git-path hooks`; `git -C <wt> rev-parse --absolute-git-dir` (mirror file) | Read | `install_l2`, `record_launch` | `orca_worktree.py:1348-1350, 1356-1367, 1593` |

**Guard stack and installers.**

| Piece | Command / invocation | R/W | Actor | File:line |
|---|---|---|---|---|
| L1 guard | Claude Code hook `~/.claude/hooks/launch-level-guard.sh` (stdin JSON; tools used: `jq`, `sed`, `tr`, `cat`, `mkdir`, `mv`, `ln`, `rm`); exit 0 or 2 only | Write (session files under `sessions/`) | Claude Code | `HK/launch-level-guard.sh:4-6, 291-313` |
| Worker `orca` commands the L1 guard lets a bound worker run (G2 rule 2) | `orca orchestration send` or `orca orchestration ask` as one raw command of plain words and quoted strings (no expansion, no newline, at most 8192 bytes and 64 arguments) with no `--to`, `--run`, `--environment` or `--pairing-code` option and no name that is a prefix of `--to` or `--run`; the allow-list `orca status`, `help`, `--version`, `worktree current`, `worktree list`, `worktree show`, `terminal list`, `terminal show`, `terminal read`, `orchestration check`, `orchestration inbox`, `orchestration run-current`, `orchestration task-list`, `orchestration worker-show` (a glob character makes these ESCAPE); every other `orca` call is ESCAPE, except a short help call (`<verb words> --help` or `-h`, at most four words counting from `orca`, no glob character) | none (the guard only decides; the worker makes the call) | the L1 guard for a bound worker; the rule is BUILT-ON, but no code binds a coordinator-started worker (D-18) | `HK/launch-level-guard.sh:480-491` (allow-list), `:487-490` (short help call, pinned by `tests/hooks/test_launch_level_guard_worker.py:226-230`), `:485` and `:496-537` (send, ask); pins `tests/hooks/test_launch_level_guard_worker.py:74`, `:187`, `:213`, `:262` (Section 5.3) |
| Job identity | `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"`; modes `hook`, `execute SESSION TOOL_ID COMMAND`, `identify [PID]`, `prepare SESSION COMMAND [TOOL_USE_ID]`, `run TOKEN`; a governed Bash command is rewritten to `/bin/bash <script> execute <sid> <tool_use_id> <command>` | Write (`requests/`, `jobs/`) | Claude Code hook; L2 | `HK/launch-job-identity.sh:541-582, 491-497` |
| L2 pre-push | git `pre-push` hook; asks `$L2_HOME/.claude/hooks/launch-job-identity.sh identify $$` under `cd /` and `env -i HOME=<pinned> PATH=<uvdir>:/usr/bin:/bin UV_NO_CONFIG=1 timeout 10`; exit 0, 1 or 2 | none (writes no file, calls no git) | git | `HK/launch-level-pre-push.sh:52-101, 187-208` |
| Hook installer | `superclaude install` / `update`: `install_hooks()` copies scripts to `~/.claude/hooks/` (0755) and merges `hooks.json` into `~/.claude/settings.json` (backup `settings.json.bak.<UTC stamp>`) | Write | person | `src/superclaude/cli/install_hooks.py:156-246`; callers `main.py:219, 412` |
| ccsession installer | `wire_ccsession()` symlinks `ccsession`, `ccsession-orca` into `~/.local/bin`; runs `unseed-env.py`, `retention.py ensure`, `ccsession --migrate-names` (30 or 60 s timeouts) | Write | person | `src/superclaude/cli/install_ccsession.py:11-142`; callers `main.py:211, 406` |

### 8.2 CLI Surface

| Verb | Options | Exit codes | Evidence |
|---|---|---|---|
| `superclaude issue-watch once` | `--dry-run`, `--config PATH` (default `~/.config/superclaude/issue-watch.json`) | 0, 1, 2, 3, 4, 5, 6, 7, 75 (Section 10.1) | `P/cli.py:111-137`; registered `src/superclaude/cli/main.py:577-579` |
| `issue-watch status` | `--json`, `--config`; no platform check | 0 healthy; 1 unhealthy; 2 config; 6 store | `P/cli.py:164-182` |
| `issue-watch check-config` | `--config`; static check only (no `gh`, no Orca, no origin, no store) | 0 valid; 2 invalid | `P/cli.py:185-198` |
| `issue-watch init-state` | `--config` | 0 created; 2 config; 6 exists or unwritable | `P/cli.py:201-214` |
| `issue-watch reset` | optional `ISSUE` (1..999999999), `--forfeit-guarantee`, `--rate-limit`, `--config`; needs `ISSUE --forfeit-guarantee` or `--rate-limit`, not both | 0; 2 usage or refused; 6; 75 | `P/cli.py:282-348` |
| `/sc:issue` | `--claim <N\|#N\|url>`, `--create`, `--depth`, `--mode`, `--type` (create only), `--pipeline worktree\|full\|none`, `--submit` (only with explicit `--pipeline full`); no repo, dry-run or preview option | STOP codes (Section 10.2) | `src/superclaude/commands/issue.md:36-59` |
| `--pipeline` levels | `none` ends after Wave 6 (no worktree, no agent); `worktree` stops at the plan boundary until a typed `/sc:implement` or `/task` line; `full` runs every step with no commit, push or PR; `full --submit` adds commit, push, `/sc:pr-submit --monitor 3` | n/a | `SK/refs/claim.md:81-96`; `SK/templates/launch-prompt.md:20-34` |
| `orca_worktree.py` | `preflight`; `worktree --repo --number --base --source`; `prompt --template --level worktree\|full [--submit] ... --out`; `launch --number --source --level worktree\|full [--submit]`; `pending --level worktree\|full\|full-submit` | 0 for every runtime outcome (one JSON object); 2 for argparse errors incl. `--submit needs --level full` | `orca_worktree.py:11-12, 1857-1902` |
| `origin_repo.py` | `--claim <arg>` prints `{"repo","number"}` | 0; 1 `E-NO-ORIGIN`; 2 argparse; 3 `E-FOREIGN-REPO`; 4 `E-NOT-AN-ISSUE` | `SK/scripts/origin_repo.py:45-50, 177-191` |
| `clickup_claim.py` | `--issue-url`, `--issue-number`, `--repo` | 0 with one JSON object; 2 bad arguments only | `SK/scripts/clickup_claim.py:245-259` |

### 8.3 Hand-off Contracts Between Pieces

| Contract | Producer | Consumer | Format | Evidence |
|---|---|---|---|---|
| Launch prompt | watcher `build_claim_prompt(n)` | the launched Claude session running `/sc:issue` | exactly `/sc:issue --claim <N> --pipeline none`; `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`; level `none` and agent `claude` hard-coded | `P/launch.py:33, 84-92`; `issue.md:48`; pinned `tests/issue_watch/test_security_invariants.py:936-1009` |
| Claim marker | claim session (comment ending `<!-- sc:issue:claim -->`) | watcher G4 `marker_in_window` (window: marker time at or after `pending_at` minus 300 s, else after `approved_at`) | hidden comment line; G4 reduces the body to a boolean | `P/predicates.py:14, 17, 274-296`; `SK/templates/claim-comment.md:23`; `tests/issue_watch/test_marker_contract.py` |
| Governed launch prompt | `orca_worktree.py launch` | L1 guard on the agent's first `UserPromptSubmit` | `[sc-launch:v1:<32 hex nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it.`; regex `\[sc-launch:v1:([0-9a-f]{32})\]` | `orca_worktree.py:1779`; `HK/launch-level-guard.sh:318` |
| Launch-level files | `publish_pending` (`launch` or `pending`) then the guard | guard, identity hook, L2 hook | `~/.claude/state/launch-level/pending/<nonce>` holds one word `worktree`, `full` or `full-submit` (file 0600, dirs 0700); guard renames it to `sessions/.take-<sid>` and hard-links `sessions/<sid>`; `sessions/<sid>.ok` (empty) = approval at level `worktree` | `orca_worktree.py:791, 1488-1512, 1759-1761`; guard `:299-313, 347-360, 372-376` |
| Identity records | identity hook (`execute`/`prepare`, supervisor) | identity `run`; L2 via `identify` | `requests/<32 hex>` JSON (0400, single use); `jobs/<kernel-sid>.json` with keys `pid, start, boot, kernel_sid, session_id`; `identify` prints one of five JSON shapes | `HK/launch-job-identity.sh:140-174, 215-260, 307-375`; `HK/launch-level-pre-push.sh:82-88` |
| L2 install | `install_l2` in `cmd_launch` | git, `l2_status` | `<git-common-dir>/hooks/pre-push` (0755, hard link) plus data file `pre-push.launch-level` (0644; line 1 `HOME`, line 2 `uv` directory); never replaces an existing entry | `orca_worktree.py:1386-1442, 1754` |
| Launch record | `record_launch` | `cmd_worktree`, `cmd_launch`, `cmd_prompt` | `<D>/worktree.json` `{"path","status","launch":{"level","submit","at"}}` plus mirror `<wt git dir>/sc-issue-launch-<N>.json` | `orca_worktree.py:507-524, 1586-1643` |
| Worker output | `issue-worker-t1/t2/t3` | orchestrator | worker returns only the paths it wrote under `.dev/issues/<N>/`; one retry on empty | `SK/SKILL.md:66`; `src/superclaude/agents/issue-worker-t*.md:35` |
| Config cross-consumer | operator file `~/.config/superclaude/issue-watch.json` | `agent-work-report` skill expects key `orchestrator_repo` | the watcher loader rejects that key (`config_invalid`, exit 2): the two consumers contradict each other [CODE-CONTRADICTED]; see Section 14 | `P/cycle.py:58-69, 216-220`; `skills/agent-work-report/scripts/common.py:22-40` |
| Coordinator hand-off after a `--pipeline none` claim | nothing in the snapshot | a person-opened coordinator (prose only) | NOT BUILT; contract text was removed; no code calls `orca_worktree.py worktree` or `worker-start` for a claimed issue; see Section 14 | `issue.md:85`; `SK/refs/claim.md:96`; `src/superclaude/core/WORKER-CONTRACT.md` (no "Issue pipeline duties") |
| Binding a coordinator-started worker (`orca_worktree.py pending`) | the verb exists; no production caller | L1 guard G2 rule 2 | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON; no production caller found; see Section 14 | `orca_worktree.py:1515-1523, 1886-1893`; test callers `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498` |

### 8.4 Hook Registrations (`src/superclaude/hooks/hooks.json`, 192 lines)

| Event | Matcher | Command | Timeout (s) | Lines |
|---|---|---|---|---|
| SessionStart | none / `*` / `startup` / `startup\|resume` | `session-init.sh` (10); `freshness-session-start.sh` (5); `codegraph-session-start.sh` (5); ccsession-tag `session-start.sh` (5) | 10, 5, 5, 5 | `:3-42` |
| UserPromptSubmit | none | `freshness-user-prompt.sh` (3); ccsession-tag `session-name.sh` (5); `~/.claude/hooks/launch-level-guard.sh` (5) | 3, 5, 5 | `:45-71` |
| SessionEnd | none | ccsession-tag `session-name.sh` | 5 | `:73-83` |
| PreToolUse | `Edit\|Write` | `freshness-pre-edit.sh` | 1 | `:85-94` |
| PreToolUse | `Bash` | `block-bare-python.sh`; `require-orca-worktree-agent.sh` | 3, 3 | `:95-114` |
| PreToolUse | `^(Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Monitor\|Workflow\|RemoteTrigger\|SendMessage\|Cron[A-Za-z]*\|Schedule[A-Za-z]*)$\|^mcp__.*(merge\|push\|commit\|pull_request\|create_or_update_file\|delete_file\|update_ref\|create_ref\|create_branch)` | `~/.claude/hooks/launch-level-guard.sh` | 5 | `:115-124` |
| PreToolUse | `Bash` | `~/.claude/hooks/launch-job-identity.sh` (after the guard in file order) | 5 | `:125-134` |
| PostToolUse | `Read`; auggie/augment matcher | `freshness-post-read.sh` (async); `auggie-flag-clear.sh` | 1 | `:136-157` |
| SubagentStart / SubagentStop | none | `freshness-subagent-start.sh`, `pragmatic-subagent.js`; `freshness-subagent-stop.sh` (async) | 1, 5, 1 | `:159-190` |

No registration has an `onFailure` key (pinned by `tests/hooks/test_launch_level_guard_registration.py:64`). `launch-level-pre-push.sh` is not in `hooks.json`; the claim installs it as a git hook (Section 8.3). The plugin copy `plugins/superclaude/hooks/hooks.json` (154 lines) carries the same three launch-level registrations; it also lacks the ccsession-tag entries and the `pragmatic-subagent.js` entry, and has `async: true` on `freshness-subagent-start.sh` [CODE-VERIFIED by diff; research 05 section 4.1]. The three launch-level scripts are byte-identical in both trees.

### 8.5 External Service Dependencies

| Service | Purpose | Failure mode | Fallback |
|---|---|---|---|
| GitHub via `gh` (login, `read:project` scope) | discovery, approval replay, re-read | unauthenticated, missing scope, rate limit, 5xx, non-JSON map to `gh_auth_failed`, `project_read_failed`, `rate_limited`, `gh_timeout`, `gh_non_json` (exit 3 or 5) | fail closed: skip or stop; no write happens. All 19 reply fixtures are assumed shapes [UNVERIFIED] |
| Orca CLI (`orca-ide`, then `orca`) | the only way to start a session | not found: `orca_not_found` (exit 2); unusable launch reply: `launch_unknown` (exit 7) | never auto-retried; `status` prints a retry command |
| ClickUp API | optional assignment mirror | any error becomes a non-fatal JSON `error` reason | claim continues; exit 2 (bad arguments) stops but keeps the GitHub assignment (`SK/refs/claim.md:51`) |
| `uv`, `jq`, `/proc`, `pidfd_open` | guard and identity hooks | governed session: fail closed (exit 2); ordinary session: fail open (exit 0) | claim IR-4 preflight refuses a launch when they are absent (`W-ENFORCEMENT-ABSENT`) |

---

## 9. Configuration & Environment

### 9.1 Watcher Configuration File (`~/.config/superclaude/issue-watch.json`, or `--config PATH`)

The loader is strict: any key outside `_TOP_KEYS` is `config_invalid` (exit 2), error details never echo file values, and no sample file ships in the snapshot (Glob `**/issue-watch*.json` is empty). Only the eight top-level keys below exist (`P/cycle.py:58-69`).

| Key or setting | Where defined | Default | Valid values | Purpose | Evidence |
|---|---|---|---|---|---|
| `schema_version` | `Config` loader | none (required) | integer `1` (`true` and `1.0` fail) | file format version | `P/cycle.py:222-226` |
| `enabled` | `Config.enabled` | `false` (`raw.get("enabled", False)`) | JSON boolean | gate for real cycles; `once --dry-run` ignores it | `P/cycle.py:228-230, 685-686` |
| `labels.trigger` | `Config.trigger_label` | `issue-watch:trigger` (`DEFAULT_TRIGGER_LABEL`) | 1..50 chars, no control character, no comma, no double quote, no leading `-` | label that selects issues in G2 | `P/cycle.py:55, 71, 127-139, 240-241` |
| `labels.approval` | `Config.approval_label` | `issue-watch:approved` (`DEFAULT_APPROVAL_LABEL`) | same rules; must differ from `labels.trigger` | label whose add-event is the human approval | `P/cycle.py:56, 242-243` |
| `project_id` | `Config.project_id` | none (required) | `PVT_[A-Za-z0-9_-]{1,64}` | the one GitHub Project the issue must sit in (Status `Backlog`) | `P/cycle.py:72, 245-249` |
| `owner_account_id` | `Config.owner_account_id` | absent = no pin | integer 1..10**20-1 | pins the G1 account id; mismatch is `account_id_mismatch` | `P/cycle.py:74, 251-255, 768-769` |
| `worktree` | `Config.worktree` | none (required) | absolute path (no `~` expansion) to an existing directory whose `origin` is `IronbellyOrg/IronClaude` | `--worktree path:` and `cwd` of the Orca launch | `P/cycle.py:118-124, 257-259, 371-377` |
| `approvers_file` | `Config.approvers_file` | none in code (runbook example `~/.config/superclaude/issue-watch-approvers.txt`) | absolute path; regular file, euid-owned, no group/other write bit, at most 1 MiB, UTF-8, one decimal id per line (`[1-9][0-9]{0,19}`), `#` comments only at line start, at least one id | allow-list of approver account ids | `P/cycle.py:75, 298-361` |
| `state_dir` | `Config.state_dir` | `$XDG_STATE_HOME/superclaude/issue-watch`, else `~/.local/state/superclaude/issue-watch` | absolute path; a network filesystem (`nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p`) is refused; unreadable `/proc/self/mountinfo` skips the check | holds `dispatch.json`, `lock`, `DISABLED`, `audit.jsonl*`, `dry-run.json` | `P/cycle.py:50-52, 187-192, 261-272` |

`check-config` is a static check only and succeeds without `gh`, Orca, a correct origin or an initialised store (`P/cycle.py:371-377`).

### 9.2 Claim, Guard and Install Settings

| Key or setting | Where defined | Default | Valid values | Purpose | Evidence |
|---|---|---|---|---|---|
| `--pipeline` default-level rule | model-applied prose, not code | explicit value wins; unreadable type, complexity or hours gives `worktree`; bug gives `full`; simple or medium feature of 16 h or less gives `full`; complex feature or over 16 h gives `worktree` | `worktree`, `full`, `none` | picks how far the launched agent runs; prints `Level: <L> (explicit)` or `(default: <reason>)` | `SK/refs/claim.md:81`; `issue.md:43`; pinned as text only by `tests/skills/test_issue_protocol.py:774, 791` |
| `--pipeline` for the watcher | `P/launch.py:33, 92` | always `none` | not configurable | watcher launches stop after the claim comments | `issue.md:48` |
| `--submit` | `issue.md:44` | off | only with explicit `--pipeline full`; otherwise `E-SUBMIT-NEEDS-FULL` (script exit 2) | adds commit, push and `/sc:pr-submit --monitor 3` | `orca_worktree.py:1900-1901` |
| `superclaude install` hooks | `install_hooks(force=False)` | existing scripts in `~/.claude/hooks/` are skipped | `--force` refreshes; `update` uses `force=True` | a plain install keeps an older guard on disk; IR-4 refuses a guard lacking `# launch-level-guard-version: 1` | `install_hooks.py:282-289`; `main.py:219, 412`; `orca_worktree.py:986-988` |
| Settings merge | `_merge_settings` | additive, ownership by command path, backup before write, malformed target refused | n/a | registers the three launch-level hooks | `install_hooks.py:301-494` |
| IR-7 refusal | `IR7_REFUSE` | `False` (BUILT-OFF: refusal branch never runs) | boolean constant | would refuse a launch when the L2 hook is not owned | `orca_worktree.py:822, 1757-1758`; pinned `tests/skills/test_issue_l2_install.py:639` |
| L2 protected refs | `L2_PROTECTED` | `refs/heads/main`, `refs/heads/master` | fixed | refused for governed and unknown actors (exit 1) | `HK/launch-level-pre-push.sh:17` |

### 9.3 Environment Variables, Paths and Kill Switch

| Variable or path | Where read | Default | Valid values | Purpose | Evidence |
|---|---|---|---|---|---|
| `HOME` | watcher default `state_dir`; guard (the only env var it reads); identity; claim | none (no `HOME`: "state_dir has no default") | absolute path | locates `~/.claude/state/launch-level/` and `~/.config/` | `P/cycle.py:187-192`; `HK/launch-level-guard.sh:23` |
| `XDG_STATE_HOME` | `_default_state_dir` | unset, then `~/.local/state` | absolute (a relative value is `config_invalid`) | state directory root | `P/cycle.py:187-192, 261-268` |
| `CLAUDE_CONFIG_DIR` | IR-4 preflight | unset | unset or resolving to `$HOME/.claude` | claim refuses a launch otherwise (`W-ENFORCEMENT-ABSENT`) | `orca_worktree.py:989-997` |
| `SC_ORCA_TIMEOUT` | `_timeout` | `DEFAULT_TIMEOUT=120` s (preflight 30, terminal read 15) | number of seconds | per-command Orca timeout override | `orca_worktree.py:88-91, 120` |
| `SC_ORCA_SHIM_INTERVAL` | shim check | 2.0 s (`SHIM_TRIES = 5`) | number of seconds | wait between shim reads | `orca_worktree.py:798-800` |
| `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` | `clickup_claim.py` | none; missing gives `skipped` (`no_token`, `no_workspace`) | strings | ClickUp auth (token only in the `Authorization` header) | `clickup_claim.py:109, 166, 169` |
| `CLICKUP_LIST_IDS`, `CLICKUP_MAX_PAGES` | `clickup_claim.py` | none; `20` (`DEFAULT_MAX_PAGES`); invalid values fall back to 20 | list ids; positive integer | narrows search; page cap | `clickup_claim.py:74, 88-94` |
| `CCSESSION_PERMISSIONS=default` | ccsession wrapper | unset (permission bypass applies) | `default` drops the bypass | launch-line permission mode (issue 390) | `tests/unit/test_ccsession_tag.py:1519-1684` |
| `CCSESSION_ORIGIN`, `CCSESSION_NAME`, `CCSESSION_ASK_TIMEOUT` | `ccsession-orca` | set or unset by the shim, not by the operator | `human`, `agent` | shim naming; carries no launch level | `skills/ccsession-tag/ccsession-orca:198-256, 249` |
| `AWR_ROOT` | `agent-work-report` | unset | path | only a workaround when `orchestrator_repo` is absent from the shared config | `skills/agent-work-report/scripts/common.py:22-40` |
| `<state_dir>/DISABLED` | cycle start and again before the launch | absent | any file, symlink or dangling symlink (`os.path.lexists`) | kill switch (`disabled`, `disabled_mid_cycle`, exit 0) | `P/record.py:421-423`; `P/cycle.py:712-713, 1063-1064` |
| `~/.claude/state/launch-level/{pending,sessions,requests,jobs}` | claim, guard, identity | absent until first launch; never pruned (owner decision O-15) | modes 0700 dirs, 0600/0400 files | launch-level stores (Section 8.3) | `orca_worktree.py:791`; guard `:20-23`; identity `:102-130`; `docs/designs/sc-issue-launch-level-hook.md:627` |
| `<git-common-dir>/hooks/pre-push`, `pre-push.launch-level` | `install_l2` | absent | see Section 8.3 | L2 hook and its pinned `HOME` and `uv` directory | `orca_worktree.py:1079, 1386-1442` |
| `.dev/issues/<N>/` | claim | absent | markdown and JSON artefacts; never staged or committed | claim output folder | `issue.md:80, 100` |
| Scheduler for `once` | not found in snapshot | none | n/a | runbook text names `0 */5 * * * *`; no timer, cron, systemd or workflow file exists (NOT BUILT) | `docs/designs/issue-watcher-setup.md:288`; research 03 section F.2 |

### 9.4 What Is NOT Configurable

| Fixed behaviour | Evidence |
|---|---|
| Every numeric limit of the cycle (candidates, day cap, timeouts, deadline, warn and health ages) is a module constant: "module constants, not operator knobs" | `P/cycle.py:33-47` |
| Repository is the literal `IronbellyOrg/IronClaude`; origin must equal `ironbellyorg/ironclaude` (lower-cased) | `P/github.py:37`; `P/launch.py:50` |
| Orca agent `claude`; surface `terminal`; no permission flag, no model flag; 12-element argv | `P/launch.py:26-28, 95-116` |
| Launch prompt and pipeline level `none` | `P/launch.py:33, 84-92` |
| Retry counts: `MAX_ATTEMPTS = 3`, backoff 10 min, lease 60 min, 24 h day-cap window | `P/record.py:434-443` |
| Launch-level words (`worktree`, `full`, `full-submit`), the 23 governed tool names and the L1 level grid | `orca_worktree.py:841-867`; guard `:781-803` |
| Worker tier pins live in agent frontmatter line 6; the skill never passes `model` | `SK/SKILL.md:54-64`; `src/superclaude/agents/issue-worker-t*.md:6` |
| `--retry-launch` is never run by code; a cron entry is never installed by code | `P/cycle.py:1308-1312`; `docs/designs/issue-watcher-setup.md:288` |

---

## 10. Error Handling & Edge Cases

### 10.1 Exit-Code Tables

**`issue-watch once` (resolved by `resolve_exit`).** The code of a reason is `audit.REASON_TABLE[reason][1]` (`P/cycle.py:480-482`). Precedence when several conditions exist: 2, 6, 7, 5, 3, 4 (`_PRECEDENCE`, `P/cycle.py:462`); 75 only when it is the sole non-zero condition; otherwise 0 (`P/cycle.py:466-477`). Exit-code constants in the CLI: `_EXIT_UNHEALTHY = 1`, `_EXIT_CRASH = 1`, `_EXIT_CONFIG = 2`, `_EXIT_STORE = 6`, `_EXIT_LOCK_HELD = 75` (`P/cli.py:34-38`); codes 3, 4, 5, 7 come only from the cycle.

| Exit | Condition | Reasons | Evidence |
|---|---|---|---|
| 0 | cycle finished or deliberate no-op | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled`, every skip reason, `attempts_exhausted`, `launched`, `claimed`, `pending_orphan`, `claim_not_observed` | `P/audit.py:26-102` |
| 1 | `once`: an unexpected `Exception` out of the cycle (stderr line carries the class name only); `status`: unhealthy | `cycle_crashed` (written to stderr only) | `P/cli.py:123-129, 164-182`; `P/audit.py:57` |
| 2 | config or environment | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch`; also `reset_refused` | `P/cycle.py:195-377, 722, 769, 1052` |
| 3 | GitHub read failure | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` | `P/github.py:489-496`; `P/cycle.py:764-765, 842-843` |
| 4 | incomplete discovery | `truncated` (100 or more results), `discovery_duplicate` | `P/github.py:823-830` |
| 5 | rate limit | `rate_limited` (header wait 1..3600 s), `rate_limit_clamped` (3600 s) | `P/github.py:418-431`; `P/cycle.py:663-668, 748-750` |
| 6 | state store | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` | `P/record.py:347-401`; `P/cycle.py:605, 1125-1126` |
| 7 | launch-step failure | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` | `P/cycle.py:1021, 1108, 1111` |
| 75 | another run holds the lock, or the lock path was replaced after `flock` | `lock_held` | `P/record.py:403-414`; `P/cycle.py:698-699` |

The doc claim that exit 7 can combine with 5 or 3 is not reachable through the cycle because a launch-step outcome halts the loop (`P/cycle.py:833-834`); only 7 with 6 is reachable [CODE-CONTRADICTED, `docs/designs/issue-watcher.md:173`]. Other verbs: `check-config` 0 or 2; `init-state` 0, 2 or 6; `reset` 0, 2, 6 or 75; `status` 0, 1, 2 or 6 (`P/cli.py:185-348`).

### 10.2 Closed Vocabularies

| Vocabulary | Members | Evidence |
|---|---|---|
| `REASON_TABLE` cycle-kind (27) | exit 2: `config_invalid, approvers_invalid, platform_unsupported, worktree_invalid, origin_mismatch, orca_not_found, account_id_mismatch`; exit 6: `store_invalid, store_missing, lock_missing, lock_invalid, state_dir_unwritable`; exit 3: `login_invalid, gh_auth_failed, gh_timeout, gh_non_json, project_read_failed`; exit 4: `truncated, discovery_duplicate`; exit 5: `rate_limited, rate_limit_clamped`; exit 75: `lock_held`; exit 1: `cycle_crashed`; exit 0: `disabled, disabled_mid_cycle, not_enabled, cycle_complete` | `P/audit.py:26-102`; pinned literally `tests/issue_watch/test_audit.py:214, 223` |
| skip-kind (17, exit 0) | `not_approved, approval_before_trigger, approval_before_init, events_incomplete, events_unreadable, edited_after_approval, project_mismatch, project_unreadable, unassigned, assigned_other, already_dispatched, in_backoff, day_cap, budget_exhausted` (never stamped in `considered`), `revalidation_failed, marker_unreadable, edits_unreadable` | `P/audit.py:26-102`; raise sites in 5.1.1.1 |
| entry-kind (9) | `prompt_invalid`(7), `revalidation_transient`(7), `spawn_error`(7), `launch_unknown`(7), `attempts_exhausted`(0), `pending_orphan`(0), `claim_not_observed`(0), `launched`(0), `claimed`(0) | `P/audit.py:84-91` |
| note, warning, operator | note `re-approved`; warnings `discovery_count` (80 or more), `clock_skew` (over 60 s), `dry_run_shadow_reset`, `reset_refused`(2); `operator_reset` | `P/cycle.py:660, 731, 775, 807`; `P/cli.py:244-250` |
| Total | 27 + 17 + 9 + 1 + 4 + 1 = 59; five words never leave `run_cycle`: `config_invalid`, `platform_unsupported`, `cycle_crashed`, `reset_refused`, `operator_reset` | `P/audit.py:26-102`; `P/cli.py:244-250` |
| `gh` reply kinds | `Reply.kind`: `timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed`; `Read.kind` adds `incomplete, budget_exhausted, truncated, discovery_duplicate`; stderr and GraphQL strings in `GH_ERROR_SIGNS` are [UNVERIFIED] | `P/github.py:267-277, 345-371, 481-496` |
| Launch outcomes | kinds `launched, unknown, spawn_error`; details `ok, spawn_error, timeout, exit_nonzero, non_json, no_operation_id, operation_id_invalid, op_unknown` (set but read nowhere); id pattern `^[A-Za-z0-9._:-]{1,128}$` | `P/launch.py:36, 56-70, 326-349` |
| Entry states | `pending, launched, unknown, failed, abandoned, claimed`; `claimed` is terminal | `P/record.py:34-36, 654-686` |
| Claim STOP codes | `E-CREATE-ONLY-FLAG, E-CLAIM-ONLY-FLAG, E-SUBMIT-NEEDS-FULL, E-NO-ORIGIN(exit 1), E-FOREIGN-REPO(3), E-NOT-AN-ISSUE(4), E-GH-AUTH, E-ORCA-REQUIRED, E-WORKER-NO-OUTPUT, E-TIER-UNAVAILABLE, E-ASSIGN-FAILED, E-POST-FAILED, E-CREATE-FAILED`; closed or assigned issue prints a no-write message | `issue.md:50-59`; `SK/SKILL.md:152-177`; `origin_repo.py:45-50` |
| Claim worktree warnings (8) | `W-ORCA-LIST-FAILED, W-ORIGIN-BASE-MISSING, W-WORKTREE-CREATE-FAILED, W-WORKTREE-AMBIGUOUS, W-WORKTREE-STALE, W-WORKTREE-COPY-FAILED, W-ORIGIN-BASE-STALE, W-FIRST-TAB-LEFT` (never STOP; status stays `success`) | `orca_worktree.py:230-239` |
| Claim launch warnings (4) and statuses | `W-LAUNCH-FAILED, W-LAUNCH-NOT-CCSESSION, W-ENFORCEMENT-ABSENT, W-L2-ABSENT`; statuses `launched, already_launched, failed`; `W-LAUNCH-NOT-CCSESSION` leaves the agent running | `orca_worktree.py:802-817, 1823-1831` |
| ClickUp results | `skipped` (`no_token`, `no_workspace`), `not_found`, `ambiguous`, `already_assigned`, `assigned`, `error` (`auth`, `rate_limited`, `page_cap`, `http_<code>`, `network`, `bad_response`, `unexpected`) | `clickup_claim.py:117-242` |
| L1 guard words (18) | `LL-IMPL, LL-COMMIT, LL-PUSH, LL-PUSH-FORM, LL-PROTECTED, LL-MERGE, LL-GH-WRITE, LL-SUBMIT, LL-REPO, LL-UNKNOWN, LL-MCP, LL-ESCAPE, LL-TURN, LL-TAMPER, LL-SKILL, LL-BIG, LL-NOBIND, LL-BROKEN`; block order BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL; ten classes block at every level including `full --submit` | `HK/launch-level-guard.sh:36-133, 783-803`; `tests/hooks/test_launch_level_guard.py:1712` |
| L2 and identity words | `L2-PROTECTED`, `L2-UNKNOWN`, `L2-MALFORMED`; identity stderr `launch job: governed Bash call cannot be wrapped safely`, `launch job: UV is required for this invocation`, `launch job: invalid invocation or unavailable private state`; `identify` statuses `ordinary` (with optional `released`), `governed`, `unknown` (reasons `stale, orphaned, foreign, unreadable`) | `HK/launch-level-pre-push.sh:187-208`; `HK/launch-job-identity.sh:215-260, 500-580` |

Level grid (`worktree` W, W approved, `full` F, `full --submit` FS): IMPL and TURN blocked at W only; COMMIT, PUSH, SUBMIT, SKILL blocked at W, WA and F and allowed at FS (`HK/launch-level-guard.sh:785-803`). Approval at W is a typed first prompt line matching `^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)`; a first line `/sc:task` is not accepted although `templates/launch-prompt.md:23` names it [CODE-CONTRADICTED].

### 10.3 Recovery and Fail-Safe Behaviour

| Mechanism | Behaviour | Evidence |
|---|---|---|
| Write-ahead `pending` | `mark_pending` then `_save()` (atomic temp file, fsync, `os.replace`, chmod 0600, directory fsync) before `orca agent launch`; if the save crosses the 120 s cut-off the previous document is restored | `P/cycle.py:1091-1098`; `P/record.py:370-378` |
| Crash points C1-C5 | C1 before the pending save: store untouched. C2 during the atomic replace: old file kept. C3 after the pending save: swept as `pending_orphan`, never launched. C4 after the spawn: swept, never launched again. C5 after the outcome save: only audit lines are lost. Across 6 runs the launcher is called at most once | `tests/issue_watch/test_crash_injection.py:1-11` |
| Sweep | `pending` found at cycle start gives `abandoned` / `pending_orphan`; `launched` past its 60 min lease gives `abandoned` / `claim_not_observed`; a later marker hit moves an entry with `pending_at` to `claimed` | `P/record.py:627-651`; `P/cycle.py:922-931` |
| At-most-once | `pending`, `launched`, `unknown`, `abandoned`, `claimed` are never relaunched; only `reset N --forfeit-guarantee` removes `abandoned` or `unknown` (the day-cap count is kept) | `P/record.py:706-720` |
| Stuck entries | `unknown` and `abandoned` with `pending_at` cost at least one G4 call per cycle while the issue stays discovered; whether that is acceptable is an open question (see Section 14) | `P/cycle.py:922-931` |
| Lock and `flock` | non-blocking `LOCK_EX\|LOCK_NB` on a pre-created 0600 `lock` file (`O_NOFOLLOW`, euid-owned, regular); inode re-checked after locking; held or replaced gives exit 75 with no rotation; missing or unsafe gives exit 6 | `P/record.py:380-419`; `tests/issue_watch/test_concurrency.py` |
| Kill switches | `enabled` false (exit 0, no lock, no call); `DISABLED` file checked inside the lock and again before the launch; neither stamps the health marker, so `status` reports unhealthy while disabled | `P/cycle.py:685-686, 712-713, 1063-1064, 1138-1139` |
| Rate limit | G1 with a usable header: wait 1..3600 s stored in `next_permitted_at`; no header (G2 and every per-issue read): clamp `now + 3600 s`; next cycles stop `rate_limited` while `now < next_permitted_at`; a dry-run never persists it | `P/github.py:418-431`; `P/cycle.py:663-668, 748-750` |
| Budget and deadline | a refused call is `budget_exhausted` (skip, not stamped, no exit); G1 or G2 starved by the deadline is `gh_timeout` (exit 3) | `P/github.py:557-589`; `P/cycle.py:418-431` |
| Dry-run isolation | all reads run; no `dispatch.json` write; no probe, re-read or launch; shadow file `dry-run.json`; a bad shadow is reset with a warning | `P/cycle.py:1029-1035, 1146-1162`; `P/record.py:831-865` |
| Audit output | decision lines then one cycle line, atomic one-`os.write` append; on `OSError` or `state_dir_unwritable` only a five-key stderr JSON line; config or platform failures before the cycle are stderr only | `P/audit.py:130-139, 381-404`; `P/cycle.py:1176-1211`; `P/cli.py:77-91` |
| Malformed or hostile replies | every typed read returns a `Read` and never raises; a wrong assumed shape reads as `non_json`, `failed` or `no_operation_id`, which fail closed (skip, or `unknown`); an unreadable launch reply is never retried | `P/github.py:467-477`; `P/launch.py:326-349` |
| Guard fail-closed versus fail-open | governed session: `LL-BROKEN`/`LL-NOBIND` (exit 2) on jq failure with a bound id, input error, unknown event, trap on non-zero exit, wrap failure; ordinary session, missing or invalid session id on a tool event, empty store, subagent prompts: exit 0 | `HK/launch-level-guard.sh:147-163, 168-173, 208-238, 386-392` |
| Claim refusals | `already_launched` without an Orca call; stale launch prompt, IR-4 failure or unwritable record: `failed` with no agent; failed launch removes the pending record; recorded-write failure adds "do not re-run the claim" text | `orca_worktree.py:1704-1775, 1815-1821` |
| Re-run idempotence | marked comments (`<!-- sc:issue:claim -->`, `<!-- sc:issue:accuracy-check -->`) are edited, not duplicated; a failed post stops with `E-POST-FAILED` and files stay | `SK/refs/claim.md:88-93` |

### 10.4 Guard Exit Codes

| Hook | Exit codes | Rule | Evidence |
|---|---|---|---|
| L1 guard (`launch-level-guard.sh`) | 0 allow, 2 block with message on stderr; never 1 and no `onFailure`; the EXIT trap maps any other status to 0 (ordinary) or 2 (governed) | Claude Code blocks only on exit 2 | `HK/launch-level-guard.sh:4-6, 135-163` |
| Job identity (`launch-job-identity.sh`) | 0 or 2 only | exit 2 for any wrap failure on a bound session, missing `uv` with a verified binding, or invalid invocation | `HK/launch-job-identity.sh:435-502, 575-580` |
| L2 pre-push (`launch-level-pre-push.sh`) | 0 allow; 1 refuse (`L2-PROTECTED`, `L2-UNKNOWN`); 2 refuse malformed stream (`L2-MALFORMED`) | the only hook in the stack that exits 1 (git's refuse code); pushes to non-protected refs are allowed for every actor | `HK/launch-level-pre-push.sh:9-10, 187-208` |
| Claim scripts | `orca_worktree.py` 0 (one JSON object) or 2 (argparse); `origin_repo.py` 0, 1, 2, 3, 4; `clickup_claim.py` 0 or 2 | runtime outcomes ride in JSON, not exit codes | `orca_worktree.py:11-12`; `origin_repo.py:45-50`; `clickup_claim.py:245-259` |

---

## 11. Performance Characteristics

No measured latency exists in the snapshot (no benchmark, no recorded timing); the section lists the budgets, deadlines and caps the code enforces. The one timing statement in the docs, "L2 costs about 100 ms per push" (`docs/designs/sc-issue-launch-level-hook.md:617-623`), was not re-run and no test asserts a time [UNVERIFIED].

### 11.1 Budgets, Deadlines and Caps

| Name | Value | Where | Effect |
|---|---|---|---|
| `gh` calls per cycle | 35 per-issue calls (`CALL_CAP`), the last 3 (`RESERVED_CALLS`) usable only by G7, G3', G6'; G1 and G2 counted apart; ceiling 37, idle cycle 2 (plus one `git` origin call) | `P/github.py:46, 49, 448-463`; `P/cycle.py:580-585` | non-reserved reads stop at 32; a refused call is a `budget_exhausted` skip |
| `PAGE_SIZE`, `PAGE_CAP` | 100 per page, 5 pages per paged read | `P/github.py:40, 43` | a fifth full page returns `incomplete` |
| `MAX_CANDIDATES` | 10 | `P/cycle.py:34, 736` | at most 10 issues examined per cycle; with one page per read about 8 can run the whole chain (design `k = min(10, 8)`) |
| `MAX_LAUNCHES_PER_CYCLE` | 1; defined but never read (dead constant); the limit works through `_Cand.launching` and `halt` | `P/cycle.py:35, 833-834` | see Section 14 |
| `DAY_CAP` | 6 launches in a rolling 24 h (`DAY_CAP_WINDOW`) | `P/cycle.py:36, 867-876`; `P/record.py:443` | `day_cap` skip, tested twice (examine and launch step) |
| `DISCOVERY_BOUND`, `DISCOVERY_WARN` | 100, 80 | `P/github.py:486`; `P/cycle.py:47, 806` | 100 or more results: `truncated`, exit 4; 80 or more: warning `discovery_count` |
| `GH_TIMEOUT_S` | 20.0 s per `gh` call | `P/cycle.py:37, 578, 582` | timeout reply kind `timeout` |
| `PROBE_TIMEOUT_S` | 10.0 s per Orca probe | `P/cycle.py:38, 1036, 1044` | no time: `budget_exhausted` skip |
| `GIT_TIMEOUT_S` | 10.0 s | `P/cycle.py:39, 716, 1071` | no time at start: `gh_timeout`, exit 3 |
| `LAUNCH_TIMEOUT_S` | 120.0 s | `P/cycle.py:40, 1099` | timeout gives `unknown` / `timeout` |
| `DEADLINE_TOTAL_S` | 240.0 s per cycle | `P/cycle.py:41, 405` | cycle budget (sized for a 5 minute cadence) |
| `GH_FLOOR_S` | 5.0 s | `P/cycle.py:42, 425` | fewer than 5 s left: no call starts |
| `LAUNCH_CUTOFF_S` | 120.0 s elapsed | `P/cycle.py:43, 431, 1069-1079, 1095-1098` | checked before and after the git call and after the pending save; past it: `budget_exhausted`, no launch |
| `SKEW_WARN_S` | 60 s | `P/cycle.py:44, 774` | warning line `clock_skew`; `clock_skew_s` is written on every cycle line whose `Date` header parsed |
| `SKEW_TOLERANCE_S` | 300 s (claim-marker window, not the warning) | `P/predicates.py:17, 295` | marker counts if at or after `pending_at` minus 300 s. The design row "skew tolerance 300 s" (`docs/designs/issue-watcher.md:827`) names this value [CODE-VERIFIED; the label is ambiguous, the number is right] |
| `HEALTH_AGE_S` | 900 s | `P/cycle.py:45, 1327` | `status` healthy only if the last stop-free exit-0 cycle is at most 900 s old (status report only) |
| `STALE_AGE_S` | 86400 s | `P/cycle.py:46, 1259` | `unknown`, or `abandoned`/`pending_orphan`, older than 24 h is listed as stale (status report only) |
| `RATE_LIMIT_MAX_WAIT_S` | 3600 s | `P/github.py:376`; `P/cycle.py:488` | longest header wait and the clamp |
| `MAX_ATTEMPTS`, `BACKOFF`, `LEASE` | 3, 10 min, 60 min | `P/record.py:434-440` | third pre-launch failure abandons; failed entries wait 10 min; a launched entry needs a marker within 60 min |
| Audit rotation | 5 MiB (`ROTATE_BYTES`), 4 rotated files (`_ROTATIONS`) | `P/audit.py:106-107, 141-156` | rotation only with the lock held; the previous `.4` is overwritten |
| stderr cap | 500 bytes (`STDERR_CAP_BYTES`), cut on a character boundary; stdout not capped | `P/runner.py:15, 57-64` | bounded memory and no text leakage |
| Approvers file size cap | 1 MiB (`_APPROVERS_MAX_BYTES`) | `P/cycle.py:75, 341-349` | larger file: `approvers_invalid` |
| Claim command timeouts | `DEFAULT_TIMEOUT` 120 s, `PREFLIGHT_TIMEOUT` 30 s, `TERMINAL_READ_TIMEOUT` 15 s (override `SC_ORCA_TIMEOUT`); shim check 5 tries x 2.0 s; L2 self-test 30 s | `orca_worktree.py:88-91, 798-800, 1078, 1178` | `run()` never raises; a timeout is a failed result |
| ClickUp caps | `CLICKUP_MAX_PAGES` 20; one retry of a 429 after `Retry-After` | `clickup_claim.py:74, 88-94, 119-123` | page cap gives `page_cap` and never assigns |
| Worker caps | one retry of an empty worker file; one T1 to T2 fallback; T2 and T3 none | `SK/SKILL.md:64-66` | `E-WORKER-NO-OUTPUT`, `E-TIER-UNAVAILABLE` |
| Hook limits | guard and identity hook timeout 5 s; L2 identity lookup `timeout 10`; guard `LL-BIG` above 65536 bytes; G2 rule 2 at most 8192 bytes and 64 arguments; identity stdin at most 1 MiB, command at most 32768 bytes | `hooks.json:68, 121, 131`; `HK/launch-level-guard.sh:419-420, 506-512`; `HK/launch-job-identity.sh:197, 433-435`; `HK/launch-level-pre-push.sh:65` | a killed hook allows the call (design V8/R2, not testable here) |

### 11.2 Performance-Critical Code

| Area | Optimization | Why it matters | Location |
|---|---|---|---|
| GitHub reads | projections (`--jq`) keep bodies out; a marker body is reduced to a boolean | bounded output and no text leakage | `P/github.py:54-67` |
| Idle cycle | exits after G1 and G2 when no trigger issue exists | 2 calls per idle cycle (`tests/issue_watch/test_cli_e2e.py:299`) | `P/cycle.py:794-808` |
| Guard empty-store fast exit | no `sessions/` directory and no `[sc-launch:` in the input: exit 0 before any parse | ordinary sessions pay almost nothing per hook event | `HK/launch-level-guard.sh:168-173` |
| Identity prologue | hook mode with no `~/.claude/state/launch-level` exits 0 before starting `uv` | ordinary sessions never need `uv` | `HK/launch-job-identity.sh:20-24` |
| L2 hook | ordinary actor exits 0 without reading stdin | most pushes cost one identity lookup only | `HK/launch-level-pre-push.sh:188` |

---

## 12. Conventions & Patterns

Snapshot: origin/master 61ac2c2e6 (read-only export). Removed code is labelled `@01e7a9e23^` (the parent of the removal commit). Path shorthand used in Sections 12 to 14 and Appendix B (this differs from Section 5.2 to 5.4, where `T/` means `tests/`): `P` = `src/superclaude/cli/issue_watch/`; `T` = `tests/issue_watch/`; `GUARD` = `src/superclaude/hooks/scripts/launch-level-guard.sh`; `WCT` = `src/superclaude/core/WORKER-CONTRACT.md`; `OW` = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; `DES` = `docs/designs/issue-watcher.md`; `SET` = `docs/designs/issue-watcher-setup.md`. Status words are only BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. Tags are [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED] (plus [STALE DOC] for a doc statement that is out of date).

### 12.1 Code Conventions

| Convention | Rule | Where enforced | Pinned by test |
|---|---|---|---|
| Closed watcher vocabulary | Every reason is one of 59 names in `REASON_TABLE`, each mapped to `(kind, exit)`; `audit.line()` raises `ValueError` for an unknown kind, reason or key | `P/audit.py:26-104`; `exit_for` `P/cycle.py:480-482` | `T/test_audit.py:214` (names literal, in order), `:223` (every pair) |
| Closed guard words | 18 `LL-*` block words (16 classes plus `LL-NOBIND` and the default `LL-BROKEN`), printed as `Blocked:` / `Why:` / `You can:` | `GUARD:36-133` (`ll_say`), grid `:785-803` | `tests/hooks/test_launch_level_guard.py:1712` (`test_design_table_holds_all_eighteen_ids`; message texts read from the design doc at run time, `:72-85`) |
| Closed L2 and claim words | L2 words `L2-PROTECTED`, `L2-UNKNOWN`, `L2-MALFORMED`; claim STOP codes (13, prose) and warning codes (12) | `src/superclaude/hooks/scripts/launch-level-pre-push.sh:187-208`; `OW:230-239` (`WARNING_ORDER`), `:802-817` (`REMEDY`) | `tests/hooks/test_launch_level_pre_push.py` (T-01..T-24); `tests/skills/test_issue_protocol.py:350` (every warning code has a remedy line) |
| Write-ahead before launch | `pending` (launches = 1) is saved and fsynced before `orca agent launch`; a crash leaves `pending_orphan`, never a relaunch | `P/cycle.py:1082-1099` | `T/test_cycle.py:4737` (`test_a_failed_outcome_save_after_the_launch_never_relaunches__fr010_nfr005_c6`) |
| One subprocess module, `shell=False` | Only `runner.py` imports `subprocess`; argv lists only, closed stdin, mandatory timeout | `P/runner.py:10`, `:91-101` | `T/test_no_shell.py:150`, `:156` (AST scan); `T/test_module_boundaries.py:219-276` (exactly nine modules, import allow-list, four Protocol classes) |
| Hook exit codes | Claude Code hooks exit 0 (allow) or 2 (block), never 1; the L2 git pre-push hook is the only script in the area that exits 1 (`L2-PROTECTED`) | `GUARD:4`, `:138`; `launch-job-identity.sh:572-580`; pre-push `:9-10`, `:197-200` | guard grid tests `tests/hooks/test_launch_level_guard.py:3394`, `:3401`, `:3457`; `tests/hooks/test_launch_level_pre_push.py` |
| Level and identity travel by files | The level is read only from `~/.claude/state/launch-level/sessions/<session_id>`; the guard reads HOME only; the ccsession shim carries no level (zero grep hits in `skills/ccsession-tag`) | `GUARD:257-273`, `:23`; `launch-job-identity.sh:103` | no test pins "the shim carries no launch level" (research 05, Gap-fill c1 B-3 D; a negative search, not proof) |
| Plugin copies byte-identical | The three launch scripts under `plugins/superclaude/hooks/scripts/` equal the `src` copies; the two `hooks.json` files carry the same three launch registrations but are not identical as files | `cmp -s` identical (research 05 section 4.1) | `tests/hooks/test_launch_level_guard_l2_tokens.py:149`; `tests/cli/test_install_hooks.py:1086-1109`; `tests/hooks/test_launch_level_guard_registration.py:121` |
| GitHub text never reaches state, argv or prompt | Audit keys are a closed set; the prompt must match `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`; no argv builder asks `gh` for title, body or comments | `P/audit.py` `line()`; `P/launch.py:33`, `:84-92`; `P/github.py:175-262` | `T/test_no_text.py:530`, `:551`, `:599`, `:818`, `:939`; `T/test_security_invariants.py:462`, `:535`, `:652` |
| Read-only `gh`, fork fixed | Every REST call carries `--method GET`; GraphQL constants contain no `mutation`; repo is the literal `IronbellyOrg/IronClaude`; origin must match | `P/github.py:37`, `:206`, `:257`; `P/launch.py:233-251` | `T/test_security_invariants.py:652`, `:894`, `:912` |
| Governed sessions fail closed, ordinary sessions fail open | Governed = a `sessions/<id>` entry; anything unparseable for a bound id is `LL-BROKEN`; missing id or no record exits 0 | `GUARD:386-392`, `:218-237`, `:807-808` | `tests/hooks/test_launch_level_guard.py` ("ordinary sessions never blocked", "fail-closed resolution"); observed on 44 sandbox payloads (research 05) |
| Strict store shape | Exactly 7 top-level keys and 17-field entries; a field change needs a `MIGRATIONS` step | `P/record.py:120-131`, `:170-171`, `:247` | `T/test_record.py` (`the_pair_table_covers_every_state_and_trigger_once`) |
| Contract rules pinned as text | Each `WC-n` rule is a set of required phrases | `WCT`; `RULE_PHRASES` `tests/skills/test_worker_contract.py:25-436` | `tests/skills/test_worker_contract.py:876-878` (`test_contract_states_rule`) |
| Claim workers are read-only; the orchestrator alone writes | Workers write only under `.dev/issues/`; every git/gh write verb in skills, commands and agents is classified | `src/superclaude/agents/issue-worker-t1.md`..`t3.md`; write-verb audit | `tests/skills/test_issue_worker_agents.py`; `tests/skills/test_worker_contract.py:1840-3141` (`WRITE_VERB_RE` `:1863-1866`) |
| Tier pins are aliases | `claude-gw-tier*` text may appear only in allow-listed paths; the three worker pins are fixed | `tests/skills/test_model_alias_policy.py:29-33`, `:38-44` | `tests/skills/test_model_alias_policy.py:83-101`, `:104-119` |
| Claim marker has one literal | `predicates.CLAIM_MARKER` appears in both required copies; the template's last non-blank line is the marker | `P/predicates.py`; `refs/claim.md`; `templates/claim-comment.md` | `T/test_marker_contract.py:28-51` |

### 12.2 Architectural Patterns

| Pattern | Where Used | Description |
|---|---|---|
| Strict pipeline of closed decisions | Watcher cycle (`P/cycle.py`) | One `once` cycle is an ordered pipeline; every decision is a `REASON_TABLE` word; exit codes resolve by the fixed precedence 2, 6, 7, 5, 3, 4 (75 only alone), `P/cycle.py:466-477` |
| Single-writer store with write-ahead | `dispatch.json` (`P/record.py`) | Non-blocking `flock`, atomic replace, state saved before the outward effect (at-most-once launch) |
| Injected Protocols | Watcher modules | Exactly four Protocols (Runner, Store, Launcher, Clock); import allow-list per module (`T/test_module_boundaries.py:276`) |
| Nonce handoff to a bound session | Claim, then guard | `pending/<nonce>` is taken by one rename, hard-linked to `sessions/<sid>`; first binding wins (`GUARD:372-384`) |
| Prose protocol plus helper scripts | `/sc:issue --claim` | The orchestrating model follows `refs/claim.md`; three scripts do the mechanical parts; text is pinned by tests, not enforced by code |
| Two independent layers | L1 guard (Claude hooks) and L2 pre-push (git hook) | L2 covers pushes to `main`/`master` only; the commit/push/submit classes live only in L1 |

### 12.3 Anti-Patterns (Things to Avoid)

| Anti-Pattern | Why It's Wrong | Do This Instead |
|---|---|---|
| Importing `subprocess` outside `P/runner.py` | Fails the AST test and bypasses timeout and `shell=False` | Go through `Runner.run` |
| Reading a launch level from an env var or the shim | The level exists only as files; no code or test supports another channel | Read `sessions/<id>` as the guard does |
| Storing or printing GitHub text | Breaks the no-text tests and the closed audit keys | Keep only validated ids, closed words and times |
| Adding a Bash PreToolUse hook casually | `tests/hooks/test_freshness_subagent_start_policy.py:105-115` pins the exact set of three; the identity hook must stay last (`tests/hooks/test_launch_level_guard_registration.py:99`) | Update both tests in the same change |
| Treating `MAX_LAUNCHES_PER_CYCLE` as the cap | The constant is never read (`P/cycle.py:35`); the cap is the S1 halt (`:833-834`) | Cite the halt |
| Following design docs for `issue-pipeline`, `release-worker`, `stage-status` | Those commands are removed (see Appendix B) | Use the Section 14.1.2 table before trusting a design doc |

---

## 13. Extension Guide

All eight scenarios below name files, functions and tests that exist at 61ac2c2e6 (research 01 to 06). Skeletons are illustrative and use only names the research quotes. A scenario whose registration point the research does not give says so.

### 13.1 Common Extension Tasks

**13.1.1 Add a watcher skip or stop reason**

- Files: `P/audit.py` (`REASON_TABLE` `:26-102`, `REASONS` `:104`); the raise site in `P/cycle.py` (`_cond` `:587-588`, `_stopped` `:590-592`, `raise _Stop(...)` as at `:685-686`); exit comes from `exit_for` (`:480-482`) and `resolve_exit` (`:466-477`).
- Steps: add the name with its `(kind, exit)` pair; raise it where the decision is made; update the two literal pins in `T/test_audit.py`; add a cycle test in `T/test_cycle.py`.
```
# P/audit.py, inside REASON_TABLE (kinds: cycle, skip, entry, note; research 01 section 8)
"new_reason": ("<kind>", <exit>),
# P/cycle.py, where the decision is made
raise _Stop("new_reason")        # or self._cond("new_reason")
```
- Pinned by: `T/test_audit.py:214` (59 names, literal order), `:223` (pairs); the `test_df42_...` tests in `T/test_record.py:1518`, `:1522` for `last_reason` words (not in `T/test_audit.py`). Pitfall: the count 59 and the order are pinned; `DES` section 4.3 and its "59 reason names" line (`DES:716`) become stale; a `note` word must have kind `note` (`P/audit.py:229-243`).

**13.1.2 Add a watcher config key**

- Files: `P/cycle.py` (`_TOP_KEYS` `:58-69`, `Config` dataclass `:96-107`, `load_config` `:195-283`, unknown-key check `:216-220`); `P/cli.py:185-198` only if `check-config` should print it.
```
_TOP_KEYS = frozenset({..., "new_key"})      # cycle.py:58-69
# Config(..., new_key: <type>)               # cycle.py:96-107 (frozen)
# load_config: raw.get("new_key", <default>), validate, on failure raise _invalid("<fixed detail>")
```
- Pinned by: config and approvers rule tests in `T/test_cycle.py` (names not listed in research 03); `T/test_cli.py:351-452` (check-config). Pitfall: failures must use a fixed detail (details never echo file values); a key read by another consumer must be added here or `once` exits 2 `config_invalid` (the `orchestrator_repo` mismatch, row D-08); defaults such as `MAX_CANDIDATES` are module constants, not operator knobs (`P/cycle.py:33`).

**13.1.3 Add a read-only `gh` call**

- Files: `P/github.py` (argv builders `:175-262`; value checks `_issue_arg`, `_page_arg`, `_cursor_args`, `_trigger_arg`, `_login_arg`; `_call` `:557-577`; `classify`).
- Steps: one `argv_*` builder, REST path with `--method GET`; call through `_call` so the 5 s floor and `CallBudget` apply; return a typed `Read`; map failures to an existing `REASON_TABLE` word.
```
def argv_new(number, page):   # validate every caller value through the _*_arg helpers
    return ["gh", "api", "--method", "GET", "repos/IronbellyOrg/IronClaude/issues/<N>/<path>", "-F", "per_page=100", "-F", "page=<P>", "--jq", <JQ>]
```
- Pinned by: `T/test_github.py` (literal argv per builder; `CALL_CAP`, `RESERVED_CALLS`, `PAGE_CAP`); `T/test_security_invariants.py:712`, `:652`; `T/test_no_text.py:818`. Pitfalls: the per-issue budget is 32 plus 3 reserved (37 per cycle); a new fixture changes the count of 19 `_assumed_shape` files pinned at `T/test_github.py:575-583`; reply shapes stay assumed until a live test exists.

**13.1.4 Add a `--pipeline` level**

- Files: `src/superclaude/commands/issue.md` (option rows `:43`, STOP rule `:58`); `src/superclaude/skills/sc-issue-protocol/refs/claim.md:81` (level rule); `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md` (a new block; names matched by `BLOCK_MARKER` `[a-z]+`, `OW:743`); `OW:1873`, `:1883`, `:1891` (`choices` of `prompt`, `launch`, `pending`); level word table `GUARD:264-269`; grid `GUARD:785-803`.
```
<!-- block:<name> -->                              # templates/launch-prompt.md; name is [a-z]+ and equals the level word (render_prompt keeps "common" + the level block, OW:756)
choices=["worktree", "full", "<name>"]            # OW:1873 (prompt), OW:1883 (launch); pending also lists "full-submit" at OW:1891
<name> | <name>$'\n') LL_LEVEL=<X> ;;              # GUARD:264-269 (read from the pending record)
<CLASS>:<X>) ll_deny "LL-<CLASS>" ;;               # one cell per class for the new level in the case at GUARD:785-803; a missing cell becomes LL-BROKEN
```
- Pinned by: `tests/skills/test_issue_protocol.py:295` (four-block assertion); `tests/commands/test_issue_command.py:84` (options table); the PR and LA tests in `tests/skills/test_issue_orca_worktree.py`. Pitfall: the level pick is prose run by the model (D-20); `pipeline.json` is not built (D-22).

**13.1.5 Add a guard level or classifier word and its matrix test**

- Files: `GUARD` (Skill classifier `:398-413`, IMPL pattern `implement | task | cleanup` at `:409`; Bash classifiers `:414-726`; precedence list `:783`; grid `:785-803`; words `:36-133`) and its byte-identical copy `plugins/superclaude/hooks/scripts/launch-level-guard.sh`; the design table of message texts in `docs/designs/sc-issue-launch-level-hook.md` (read by a test at run time).
```
# GUARD :783  precedence: BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL <NEWCLASS>
# GUARD :785-803  one cell per level W WA F FS; a class with no cell becomes LL-BROKEN (:801)
#   <NEWCLASS>:W | <NEWCLASS>:WA | <NEWCLASS>:F | <NEWCLASS>:FS) ll_deny "LL-<NEWCLASS>" ;;     # or a `;;` with no action where the level allows it
# the classifier that sets the class in $LL_CLASSES (Skill :398-413, Bash :414-726): not determinable from research for a new class beyond these ranges
```
- Pinned by: `tests/hooks/test_launch_level_guard.py` `test_grid_policy` `:3394`, `test_grid_complete` `:3401`, `test_grid_level_steps` `:3457` (hand-written oracle), `test_skill_grid_matches_oracle` `:905`, `test_impl_name_spellings` `:927`, `test_lookalike_skill_names_stay_none` `:936`, `test_design_table_holds_all_eighteen_ids` `:1712`, `test_precedence_order` `:4520`; copy check `tests/hooks/test_launch_level_guard_l2_tokens.py:149`. Pitfalls: the design lists six IMPL skills but code has three (row KW-6 in 14.1.2); the guard matches the basename `orca` only (D-25).

**13.1.6 Register a new hook script**

- Files: `src/superclaude/hooks/scripts/<name>.sh`; `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py:42-97` (launch scripts at `:90`, `:93`, `:96`); `src/superclaude/hooks/hooks.json` (PreToolUse groups `:85-134`; identity hook must stay last, `:125-134`); `plugins/superclaude/hooks/hooks.json` (hand-kept; it already differs from `src` in three documented ways); byte-identical `plugins/superclaude/hooks/scripts/<name>.sh`.
```
# src/superclaude/hooks/hooks.json, inside the "PreToolUse" array (the identity group stays last, :125-134)
{ "matcher": "<tool regex>", "hooks": [ { "type": "command", "command": "~/.claude/hooks/<name>.sh", "timeout": 5 } ] }
# src/superclaude/cli/install_hooks.py, inside _FRESHNESS_SCRIPTS (:42-97), after the launch scripts at :90, :93, :96
"<name>.sh",
```
- Registration row: event, matcher, command `~/.claude/hooks/<name>.sh`, timeout (the guard and identity use 5), no `onFailure` key (pinned). A git hook (like the L2 pre-push) is not registered in `hooks.json`; it is installed by the claim.
- Pinned by: `tests/cli/test_install_hooks.py:1086`, `:1104` ("packaged, listed, executable, mirrored" pattern), `:897`; `tests/hooks/test_launch_level_guard_registration.py:45-121`; `tests/hooks/test_freshness_subagent_start_policy.py:91-115` (exact set of Bash PreToolUse commands). Pitfalls: a plain `superclaude install` skips an existing script (only `update` and `--force` refresh, `install_hooks.py:282-284`, `main.py:219`, `:412`); a registration collision is decided by command path (`:405-418`).

**13.1.7 Add a claim worker tier or template**

- Worker: `src/superclaude/agents/issue-worker-tN.md` (line 5 `tools: Read, Grep, Glob, Write, Bash`; line 6 `model: claude-gw-tier...`); `WORKERS` dict `tests/skills/test_issue_worker_agents.py:21-26`; `ISSUE_WORKER_PINS` `tests/skills/test_model_alias_policy.py:29-33` and `TIER_TEXT_ALLOWED` `:38-44`; `SKILL.md:58-62`; `refs/tiers.md:11-15`; the tier key in `src/superclaude/skills/ccsession-tag/ccsession-models.json` (tier keys at lines 85, 93, 104, 113).
```
# src/superclaude/agents/issue-worker-tN.md, frontmatter (as in issue-worker-t3.md:1-8)
name: issue-worker-tN
tools: Read, Grep, Glob, Write, Bash
model: claude-gw-<tier>
# tests/skills/test_issue_worker_agents.py:21-26, WORKERS
"issue-worker-tN": ("claude-gw-<tier>", "<tier>"),
```
Which tier a new worker takes and how the orchestrator picks it (`SKILL.md:58-62`, `refs/tiers.md:11-15`) are prose rules: the selection logic is not determinable from research.
- Template: a file under `src/superclaude/skills/sc-issue-protocol/templates/` plus a row in the `SKILL.md` files table (`:36-50`); pinned by `tests/skills/test_issue_protocol.py:147` (two-way inventory). Posted templates must end with their marker.
- Pitfalls: `test_tier_ids_appear_only_in_allowed_paths` (`:104`) fails unless the new path is allowed; the scan does not cover `docs/designs/`, so a stale tier text there is not caught (KW-7).

**13.1.8 Add a coordinator contract rule**

- Files: `WCT` (rules are `**WC-n.` bullets in sections 2 to 4; section 4 starts `:68`); `tests/skills/test_worker_contract.py` `RULE_PHRASES` (`:25-436`, rule name to required phrases; consumed by the parametrized `test_contract_states_rule` `:876-878`). If the rule names a command that must never run as a worker, also the list at `:444-454` (`_check_never_as_worker` `:734`); if it names a git or gh write verb, classify it in the write-verb audit (`:1840-3141`).
```
RULE_PHRASES["<rule-name>"] = (None, ["<required phrase 1>", "<required phrase 2>"])   # tests/skills/test_worker_contract.py:25-32
```
- Value shape: a 2-tuple `(identifier-or-None, [phrases])` (`tests/skills/test_worker_contract.py:24`; unpacked as `ident, phrases = RULE_PHRASES[rule]` at `:725`). Every phrase must occur in the contract text; when the first element is not `None`, that identifier must also share one line with the first phrase (`:728-731`). A plain list here breaks the unpacking.
- Pitfalls: no test pins the absence of a removed rule (WC-17 has 0 hits anywhere in tests); `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:196`, `:285` quote rule counts and line ranges that drift (X-28); whether a plugin copy of the contract exists: not determinable from research.

**Symbols used in 13.1.** The helper and test names that the scenarios above name but Section 5 and Appendix A do not list by name. Paths are repository-relative (`P/`, `T/`, `OW`, `GUARD` as in Section 12); lines are for the 61ac2c2e6 snapshot.

| Symbol | File:line | What it is | Where it is pinned |
|---|---|---|---|
| `_cond(reason)` | `P/cycle.py:587-588` | appends `(reason, exit_for(reason))` to the cycle's condition list (13.1.1) | `T/test_cycle.py` (Appendix A.1); the word itself by `T/test_audit.py:214`, `:223` |
| `_stopped(reason)` | `P/cycle.py:590-592` | sets `stop_reason`, then calls `_cond` (13.1.1) | `T/test_cycle.py` (Appendix A.1) |
| `test_df42_every_reason_these_tests_write_is_in_the_audit_table` | `T/test_record.py:1518` | every `last_reason` word the record tests write is in `REASONS` (13.1.1) | itself (Appendix A.1, `test_record.py` row) |
| `test_df42_every_reason_the_transitions_write_is_in_the_audit_table` | `T/test_record.py:1522` | the same check for the words the transitions write (13.1.1) | itself (Appendix A.1, `test_record.py` row) |
| `_issue_arg`, `_page_arg` | `P/github.py:111`, `:118` | reject an invalid issue number or a page outside 1 to `PAGE_CAP` with `ValueError` (13.1.3) | no test names them; exercised through the argv builders in `T/test_github.py` (Appendix A.1) |
| `_cursor_args`, `_trigger_arg`, `_login_arg` | `P/github.py:141`, `:150`, `:168` | validate a GraphQL cursor, a trigger label and a login before they reach an argv (13.1.3) | `T/test_github.py:2132` (`invalid cursor`), `:2077` (`invalid trigger label`), `:2107` (`invalid login`); no test names the helpers |
| `render_prompt` | `OW:746-761` | keeps the `common` block, the level block and (with submit) the `submit` block of `launch-prompt.md`; raises `ValueError` for a missing block (13.1.4) | `tests/skills/test_issue_protocol.py:295` (13.1.4) |
| `ll_deny` | `GUARD:135-139` | sets the denied flag, prints the block message for the word and exits 2 (13.1.4, 13.1.5) | the grid tests of 13.1.5 (`test_grid_policy` `tests/hooks/test_launch_level_guard.py:3394`) |
| `_FRESHNESS_SCRIPTS` | `src/superclaude/cli/install_hooks.py:42-97` | the installer's list of hook script file names (13.1.6) | `tests/cli/test_install_hooks.py:1086`, `:1104`, `:897` (13.1.6) |
| `test_tier_ids_appear_only_in_allowed_paths` | `tests/skills/test_model_alias_policy.py:104` | the test behind "`claude-gw-tier` text only in allowed paths" (13.1.7; Appendix A.3) | itself |
| `_check_never_as_worker` | `tests/skills/test_worker_contract.py:734` | requires exactly one never-as-worker term line and every command of `NEVER_AS_WORKER` on it (13.1.8) | `test_never_as_worker_list_names_every_listed_command` (`:881-882`) |

### 13.2 Testing Requirements for Changes

| Change Type | Required Tests | Test Location |
|---|---|---|
| New or renamed reason word | literal name list and `(kind, exit)` pairs; one cycle path | `T/test_audit.py:214`, `:223`; `T/test_cycle.py` |
| New `gh` or Orca argv | literal argv, no-text, allowed-form scan | `T/test_github.py`, `T/test_launch.py:75`, `T/test_no_text.py:818`, `T/test_security_invariants.py:712` |
| Store field or state change | pair table, `MIGRATIONS`, key-set check | `T/test_record.py` |
| New module or import | module list and import allow-list; AST rule | `T/test_module_boundaries.py:219-276`, `T/test_no_shell.py:150-156` |
| Guard class, level, word | oracle grid, precedence, 18-id table, byte-identical copy | `tests/hooks/test_launch_level_guard.py`, `tests/hooks/test_launch_level_guard_l2_tokens.py:149` |
| Hook registration or install | registration pins, install pins, exact Bash hook set | `tests/hooks/test_launch_level_guard_registration.py`, `tests/cli/test_install_hooks.py`, `tests/hooks/test_freshness_subagent_start_policy.py:91-115` |
| Claim script, template or worker tier | inventory, warning-code remedies, tier pins, marker | `tests/skills/test_issue_protocol.py`, `tests/skills/test_issue_orca_worktree.py`, `tests/skills/test_issue_worker_agents.py`, `tests/skills/test_model_alias_policy.py`, `T/test_marker_contract.py` |
| Contract rule | required phrases; never-as-worker list; write-verb audit | `tests/skills/test_worker_contract.py` |

Evidence limit: these tests were read by name and selected bodies, not run (Q-22 in 14.3).

---

## 14. Known Limitations & Technical Debt

Scope note: every row below comes from the six research files, including their Gap-fill errata (which supersede earlier wording). The row about `DES:827` is not a contradiction: it is [CODE-VERIFIED] (see KW-1). Path shorthand is as in Section 12.

### 14.1 Current Limitations

#### 14.1.1 Limitations table

| Limitation | Impact | Workaround | Planned Fix |
|---|---|---|---|
| The real watcher cycle is BUILT-OFF: `enabled` defaults to false (`P/cycle.py:228`, stop `not_enabled` `:685-686`) and no scheduler artefact exists in the snapshot | No issue is claimed automatically | `once --dry-run` bypasses `enabled` and stops before the launch step | FU-2 cron entry, gated behind the live test (`DES:861`; `SET:676`); `SET:288`: "This work does not install or enable the entry" |
| All 19 `gh` and Orca reply fixtures are `_assumed_shape: true`; no live-test record exists | The reason a live failure produces (`gh_auth_failed`, `rate_limited`, `gh_non_json`, `launch_unknown`) is unverified | Owner-run live test (FU-1) | FU-1 (`DES:33`; `SET:272`): "You write that file; the implementation does not" |
| One launch step per cycle; `claimed` is terminal and `reset` refuses it (`P/record.py:448`) | A claimed issue is never dispatched again by the watcher | none documented | none (`DES:478`) |
| Stuck entries (`unknown`, `claim_not_observed`, `spawn_error`) cost at least one G4 call every cycle while the issue is discovered (`P/cycle.py:922-931`) | Budget use grows with stuck issues | `reset N --forfeit-guarantee` | none recorded (open question Q-02) |
| The edit check runs once before the re-read (`P/cycle.py:1006`) | A body edit between the G5 read and the launch is not seen | none | none recorded (Q-03) |
| Linux only for `once`, `check-config`, `init-state`, `reset` (`P/cli.py:88`, `:314`); `status` is not checked (`:169`); identity hook needs Linux and `uv` | Other platforms exit 2 | none | none |
| The guard governs only a session bound by a claim launch at `worktree` or `full`; a `--pipeline none` claim (the watcher launch) creates no pending record | The watcher's claim session and coordinator-started workers are outside the guard | none | none recorded (D-18) |
| L1, L2 and identity cover only the tested local Bash surface (limits LIM-1..LIM-20; identity returns 0 for any non-Bash tool, `launch-job-identity.sh:442-444`) | Monitor, `setsid`, a killed supervisor and some `git --no-verify` spellings are outside | none | declared limits, owner decision OD-1 (`docs/designs/sc-issue-launch-level-hook.md:534`) |
| After a `--pipeline none` claim no code or contract rule starts a worker (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`) | The claimed issue waits for a person | a person-opened coordinator by hand | none (D-16) |

#### 14.1.2 Doc-vs-code contradiction table

Part A: the eight known staleness warnings (BUILD-REQUEST), each confirmed or refuted by code.

| ID | Doc path:line | Doc claim | Code reality (path:line) | Tag | Research file |
|---|---|---|---|---|---|
| KW-1 | `DES:827` | "skew tolerance 300 s, equals the cadence" is a stale clock-skew value | NOT contradicted. 300 s is the claim-marker window `SKEW_TOLERANCE_S` (`P/predicates.py:17`, used `:295`); the clock-skew warning is 60 s, `SKEW_WARN_S` (`P/cycle.py:44`, used `:774`); `DES:510` says 60. The label "skew tolerance" is ambiguous, the number is right | [CODE-VERIFIED] (label ambiguous) | R01 row 22; R03 Gap-fill c1 F-1 |
| KW-2 | `DES:380`, `DES:819` | `max_launches_per_cycle` = 1 is a default | Behaviour exists (S1 halt `P/cycle.py:833-834`); the constant `MAX_LAUNCHES_PER_CYCLE` (`:35`) is never read (row D-01) | [STALE DOC] | R01 Gap-fill c1 B-1 |
| KW-3 | `SET:170`; `SET:616-619`; `SET:5`, `SET:270-274` | Cites `WCT` section 4 "Issue pipeline duties"; launch capture command is `--prompt '/sc:issue --claim <test issue>'`; a live-test file is a deliverable; no dispatcher or zero-setup step | `WCT` has 0 hits for "Issue pipeline duties" (section 4 is "Coordinator rules", `:68`); code prompt ends `--pipeline none` (`P/launch.py:33`, `:92`; `SET:170` and `:575` do mention it); `docs/designs/issue-watcher-live-test.md` absent; "dispatcher", `COORD-`, "zero-setup watcher": not found in snapshot | [CODE-CONTRADICTED] | R03; R02; R06 |
| KW-4 | `docs/designs/issue-pipeline-fu1.md:64-66` | Runbook runs `superclaude issue-pipeline plan-hash` / `check-approval`, cites `src/superclaude/cli/issue_pipeline/plan_hash.py` | Command group and directory absent (`src/superclaude/cli/main.py` has no registration; `CHANGELOG.md:17` records the removal). `:36` is accurate as history | [CODE-CONTRADICTED] | R03; R05; R06 |
| KW-5 | `docs/designs/issue-pipeline-guard-g2.md:13`, `:22`, `:9`, `:18`, `:45-51` | Allow-list lines `:471-474` and TAMPER `:703`; rule 1 / route A `release-worker` is live design; a coordinator calls `orca_worktree.py pending` | Lines now `GUARD:480-491`, `:760-762`; rule 1 retired (`GUARD:496`); zero hits for `release-worker`; `pending` exists (`OW:1515`, `:1886-1893`) but has no production caller (D-18) | [CODE-CONTRADICTED] (lines, route A); [UNVERIFIED] (caller) | R05 rows 5, 8, 9; R04 |
| KW-6 | `docs/designs/sc-issue-launch-level-hook.md:106`, `:179`, `:236`, `:391`; `:123` | IMPL skills are implement, task, improve, cleanup, spawn, build; row 34: a typed `approved` writes `.ok` | `GUARD:409` matches `implement \| task \| cleanup`; `improve`, `spawn`, `build` are absent from `src/superclaude/commands`; the design contradicts itself (`:189` says plain `approved` was removed); code accepts only a first line `/sc:implement` or `/task` (`GUARD:347`) | [CODE-CONTRADICTED] | R05 rows 1, 2 |
| KW-7 | `docs/designs/sc-issue-command.md:3`, `:58`, `:107`, `:129`, `:391`, `:423`, `:449`; `docs/designs/sc-issue-claim-pipeline-flag.md:21`, `:43`, `:66` | Status "Design only (nothing implemented)"; T3 pinned to `claude-gw-tier3`; default level is `worktree` | Command, skill, scripts, agents and tests exist; `src/superclaude/agents/issue-worker-t3.md:6` pins `claude-gw-tier2b`; the default is a prose pick at `refs/claim.md:81` (`full` for a person-typed bug or small feature, else `worktree`; the watcher passes `none`); no test scans `docs/designs/` | [CODE-CONTRADICTED] / [STALE DOC] | R04 |
| KW-8 | scope hint (no doc line) | The ccsession shim carries the launch level | Zero grep hits for launch-level text in `src/superclaude/skills/ccsession-tag`; the level travels by files only; the claim only detects the shim (`OW:1564-1583`, warning `W-LAUNCH-NOT-CCSESSION` `:1802-1811`) | [CODE-CONTRADICTED] | R05 section 5.2 |

Part B: every other contradicted or stale row in the research files.

| ID | Doc path:line | Doc claim | Code reality (path:line) | Tag | Research file |
|---|---|---|---|---|---|
| X-1 | `DES:331`, `:362`, `:621` | `find_orca` result cached per cycle | "caches nothing" (`P/launch.py:6`, `:177`); `OrcaLauncher` holds only the runner (`:352-356`) | [CODE-CONTRADICTED] | R01; R02 |
| X-2 | `DES:360` | Step 10 local checks "Calls 0" | Entries in `launched`/`unknown`/`abandoned` read G4; tombstones and backoff entries read G4 and G3 (`P/cycle.py:922-935`) | [CODE-CONTRADICTED] | R01 |
| X-3 | `DES:173` | Exit 7 combines with 5 or 3 | Unreachable through `_Cycle` (halt `P/cycle.py:833-834`); only 7 with 6 occurs; `resolve_exit` accepts any set (`:466-477`) | [CODE-CONTRADICTED] | R01 |
| X-4 | `DES:406` | `audit.jsonl` written by every exit and read by `status` and the SLO reducer | Several exits write only stderr (`P/cli.py:79-81`, `:127`, `:219`; `P/cycle.py:1195-1196`); nothing reads the file (`:1279-1284`); `slo_numbers` has no caller | [CODE-CONTRADICTED] | R01; R03 |
| X-5 | `DES:722` | `clock_skew_s` always present on the cycle line | Optional (`P/audit.py:165`); absent without a parseable `Date` header (`P/cycle.py:770-773`) | [CODE-CONTRADICTED] | R01 |
| X-6 | `DES:15`, `:41` | Watcher prompt is `/sc:issue --claim <N>` | `/sc:issue --claim <N> --pipeline none` (`P/launch.py:33`, `:84-92`); `DES:43`, `:49` already say none | [CODE-CONTRADICTED] | R01; R03 |
| X-7 | `SET:616-619` | Capture-sheet launch lacks `--pipeline none` | The watcher always sends it (`P/launch.py:92`; `tests/issue_watch/test_security_invariants.py:936-1009`); a fixture captured this way records a launch the watcher cannot make | [CODE-CONTRADICTED] | R02; R03 |
| X-8 | `CHANGELOG.md:9`; `src/superclaude/skills/agent-work-report/scripts/common.py:22-40`; `tests/skills/test_agent_work_report.py:2979-3000` | The poll config carries `orchestrator_repo` for `agent-work-report` | `_TOP_KEYS` lacks it (`P/cycle.py:58-69`); unknown keys exit 2 `config_invalid` (`:216-220`) | [CODE-CONTRADICTED] (cross-consumer) | R01; R03 |
| X-9 | `DES:43`; `SET:170` | Two inputs approve the plan, "read by the coordinator through `stage-status`" | `stage-status` is removed (`CHANGELOG.md:17`; Appendix B) | [CODE-CONTRADICTED] | R03; R06 |
| X-10 | `DES:75` | Platform check omits `reset` | `P/cli.py:314` checks it for `reset` | [CODE-CONTRADICTED] | R03 |
| X-11 | `DES` section 4.1 (no line in research) | `once` exit list omits 1; `reset --rate-limit` list omits 2 | Per research 03 Gaps 6 | [CODE-CONTRADICTED] | R03 |
| X-12 | `DES:137`; `DES:154-155` | Label and approvers-file rules complete | Label bans on comma, quote, leading dash (`P/cycle.py:127-139`); 1 MiB and UTF-8 rules (`:75`, `:341-349`) | [CODE-CONTRADICTED] (incomplete) | R03 |
| X-13 | `DES` (no line) | `_ORCA_CLIS` at `install_user_setup.py:35` | Line 36 | [CODE-CONTRADICTED] (minor) | R03 |
| X-14 | `DES:103` | `--retry-launch` appears nowhere | `launch.retry_argv` contains it (`P/launch.py:119-132`) | [STALE DOC] | R03 |
| X-15 | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1059` | `issue-watch` registered at `cli/main.py:563-565` | Lines `:577-579` | [STALE DOC] | R03 |
| X-16 | `docs/user-guide/cli-groups.md` | Verbs and examples complete | No exit codes, no `enabled` default, no note that no timer is installed | [STALE DOC] (incomplete) | R03 |
| X-17 | `SET` section 8.5 | Relies on a "grant" and a coordinator handoff | No dispatcher, no zero-setup step; no code implements a grant or handoff | [STALE DOC] | R03 |
| X-18 | `DES:485` | T-1 only from "(none)" | `record.fail` also runs from `failed` (`P/record.py:511`) | [STALE DOC] (minor) | R02 |
| X-19 | `DES:640` | Operation id is a non-empty `str` | `^[A-Za-z0-9._:-]{1,128}$` (`P/launch.py:36`, `:287-289`, `:347-348`) | [STALE DOC] (code stricter) | R02 |
| X-20 | `tests/issue_watch/test_find_orca_parity.py:13-18` | Original `_find_orca` at `install_user_setup.py:216-219` | Now `:247-270`; behaviour unchanged | [STALE DOC] (lines) | R02 |
| X-21 | `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:23` | `/sc:task` is a releasing first line | `GUARD:347` accepts only `/sc:implement` and `/task`; no `sc:task` in the guard (row D-23) | [CODE-CONTRADICTED] | R04 |
| X-22 | `docs/designs/sc-issue-command.md:154-158` | Wave 0 has no Orca check and no `--limit 200` | `refs/claim.md:17`, `:28` | [STALE DOC] | R04 |
| X-23 | `refs/claim.md:125`; `SKILL.md:35`, `:92`; `refs/tiers.md:32`, `:44`; `docs/designs/sc-issue-claim-pipeline-flag.md:59` | L2 hook "in the new worktree"; IR-4 runs "before anything else"; `--git-path hooks/pre-push`; four subcommands; heading once | Shared `<git-common-dir>/hooks/pre-push` (`OW:1365`, `:1402`); record, already-launched and stale-prompt checks run first (`:1700-1724`); `--git-path hooks` (`:1357`); `pending` (`:1886`) unnamed in docs; heading appears twice | [STALE DOC] | R04 |
| X-24 | `docs/reference/model-aliases.md:12`, `:18` | Test lines "46-47 and 100-115", "36-40"; three allowed locations | `TIER_TEXT_DIRS` `:50`, `TIER_TEXT_ALLOWED` `:38-44`, test `:104-119`; a fourth location `src/superclaude/cli/review/data/` (`:43`) | [CODE-CONTRADICTED] (lines, omission) | R04 Gap-fill c1 F-2 |
| X-25 | `docs/designs/issue-pipeline-guard-g2-no-to.md:7`, `:48`, `:57` | Block at lines 500-549; rule WC-17 holds the no-`--to` sentence; `release-worker` | Block now `GUARD:496-537`; WC-17 removed, the sentence is the bullet "Messages carry no `--to`" (`WCT:66`); the guard change itself is built | [CODE-CONTRADICTED] | R05; R06 |
| X-26 | `docs/designs/sc-issue-launch-level-hook.md:23` vs `docs/designs/issue-pipeline-guard-g2.md:9` | "Not governed" versus "must be bound before any other issue runs" | Code binds only claim launches; the two docs disagree | [CODE-CONTRADICTED] between docs | R05 row 10 |
| X-27 | scope hint (no doc line) | Plugin `hooks.json` differs only by lacking ccsession-tag entries | Also lacks the `pragmatic-subagent.js` entry; `freshness-subagent-start.sh` has `async: true` in the plugin only | [CODE-CONTRADICTED] (hint) | R05 row 21 |
| X-28 | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:196`, `:285`, `:1058`, `:1133` | "WC-2 to WC-15 in a 327-line contract"; ranges `:67-282`, `:283-327`; `orca_worktree.py` line counts | `WCT` is 339 lines with WC-2..WC-16 (ranges `:68-297`, `:299-339`); counts are for an older checkout; `:268` is accurate | [STALE DOC] | R06 |

### 14.2 Technical Debt

No remediation tasks were created because this run may write nowhere outside its task folder and the output file; the rows below are listed for the owner to decide. Where a decision for a removal is recorded in a file this reference cites, the row cites it (`CHANGELOG.md:17` for the removed items; `docs/designs/sc-issue-launch-level-hook.md:23` for the guard not governing a coordinator-started worker). A row with no cited decision has none in the files read; none is relabelled a "known gap".

#### 14.2.1 DEFECT CANDIDATE, NOT BUILT, BUILT-OFF and REMOVED capability rows

| ID | Capability | Declaring doc path:line | Code evidence | Class | Status word | Note |
|---|---|---|---|---|---|---|
| D-01 | `max_launches_per_cycle` = 1 as a named default | `DES:380`, `:819`; `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1740` | `MAX_LAUNCHES_PER_CYCLE = 1` at `P/cycle.py:35`, no other hit in `src/` or `tests/`; the cap is `_Cand.launching` plus `halt` (`:1028`, `:833-834`) | DEFECT CANDIDATE (dead constant) | NOT BUILT (constant unread; the cap itself works) | No decision found; low severity |
| D-02 | `status` reads `audit.jsonl` | `DES:406` | `status_report` takes `audit` "accepted for the fixed signature and not read" (`P/cycle.py:1279-1281`); only writers elsewhere | DEFECT CANDIDATE | NOT BUILT (reader) | No decision found |
| D-03 | SLO numbers (p95 approval-to-launch, exit-0 share, claimed share, stale count) as a report | `DES:750-752`, `:869`; `SET:455-478`, `:684` | `slo_numbers` (`P/cycle.py:1359`) and `SloNumbers` (`:1339`) have no caller; only `T/test_slo_helper.py` and an owner-run snippet (`SET:467-475`) | NOT BUILT | NOT BUILT | `DES:752`: "a library function with a fixture test, not a verb" records "no verb", not "no caller"; FU-10 |
| D-04 | Scheduled trigger for `issue-watch once` (cron every 5 min, FU-2) | `DES:15`, `:30`, `:861`; `SET:198`, `:286-290`, `:676`; `P/cli.py:98` | No timer, installer or action in `P`, `.github`, `.claude`, `plugins`, `scripts`, Makefile, pyproject, package.json | NOT BUILT | NOT BUILT | Decision: `DES:28`, `:30` out of scope; `SET:288`; ordering behind FU-1 (`DES:33`, `:861`) means "later", not "out of scope" |
| D-05 | Owner-run live-test record and replacement of every `_assumed_shape` fixture (FU-1) | `DES:33`, `:775`, `:860`; `SET:5`, `:270-274`, `:586-625`, `:675` | `docs/designs/issue-watcher-live-test.md` absent; 19 fixtures assumed (`T/test_github.py:575-583`); no code checks the gate | NOT BUILT | NOT BUILT | Decision: `DES:33` ("neither this design nor its implementation writes it"); `SET:272`, `:625` |
| D-06 | The whole real watcher cycle | `DES:3`, `:33` | `P/cycle.py:228`, `:685-686`; no shipped config file | BUILT-OFF by design | BUILT-OFF (enabled:false) | Decision: `DES:33` deployment gate |
| D-07 | `prompt_invalid` entry for a bad issue number | `DES:362`, `:170` | Only reachable for a non-int or out-of-range number (`P/launch.py:90-91`), which `github.discover` rejects first (`P/github.py:827-828`); reached only by `T/test_cycle.py:3348` | DEFECT CANDIDATE (unreachable path) | BUILT-ON (unreachable in practice) | No decision found; low |
| D-08 | One config file read by two consumers | `src/superclaude/skills/agent-work-report/scripts/common.py:22-25`, `:40`; `CHANGELOG.md:9`; `tests/skills/test_agent_work_report.py:2979-3000` | `_TOP_KEYS` lacks `orchestrator_repo` (`P/cycle.py:58-69`); unknown keys exit 2 (`:216-220`); without the key the skill exits "the orchestrator repo is unknown" unless `AWR_ROOT` is set | DEFECT CANDIDATE (cross-consumer) | BUILT-ON (consumers contradict) | No decision found |
| D-09 | `record.disabled_present(state_dir)` | `DES:228` | Defined `P/record.py:748-750`; only `T/test_record.py:861`, `:870` call it; the cycle uses `FileStore.disabled()` (`P/cycle.py:712`, `:1063`) | DEFECT CANDIDATE (dead code) | BUILT-ON (no production caller) | No decision found; low |
| D-10 | `LaunchOutcome.detail` (8 words, `LAUNCH_DETAILS`) | `DES:634-641` (details are code-only, `P/launch.py:58-70`) | No read of `.detail`; `_launch` uses `kind` and `operation_id` only (`P/cycle.py:1101-1112`); the reason an `unknown` happened is lost | DEFECT CANDIDATE (dead field) | BUILT-ON (set, never read) | No decision found; low |
| D-11 | `launch_login`, `launch_account_id` | `DES:437-438` | Written (`P/record.py:548-568`) and validated (`:180`, `:185`); no reader in `src` | DEFECT CANDIDATE (write-only) | BUILT-ON (write-only) | Informational |
| D-12 | Automatic retry of an `unknown` launch (FU-8) | `DES:867`; `SET:682` | `retry_argv` (`P/launch.py:119-132`) is only printed by `status_report` (`P/cycle.py:1308-1312`) | NOT BUILT | NOT BUILT | Deferred "after FU-1 confirms the C20 argv" |
| D-13 | Cleanup of orphan `dispatch.json.*.tmp` | `DES` C2 row (about `:535`) | No unlink beyond the in-exception one (`swarm/atomic.py:33-38`) | NOT BUILT | NOT BUILT | Decision: the orphan "is ignored" (`DES` about `:535`) |
| D-14 | Bound or pruning rule for finished entries (FU-11) | `SET:685`; `DES:870` | Only `reset_entry` removes `abandoned`/`unknown` (`P/record.py:706-720`) | NOT BUILT | NOT BUILT | Deferred "when the store is above 1 MiB" |
| D-15 | Alerting FU-4, ETag FU-5, per-actor checks FU-6, approver role check FU-9, local-FS allow-list FU-12 | `DES:862-871`; `SET:673-686` | No code (`status` only prints a retry command) | NOT BUILT | NOT BUILT | Listed as follow-ups: "None of these is built by this work" |
| D-16 | Coordinator hand-off after a claim (adopt, create the issue worktree, `worker-start`); dispatcher, `COORD-<RepoName>` worktree, zero-setup install | `DES:43`; `SET:170`; `docs/designs/issue-pipeline-fu1.md:9-12`; `src/superclaude/commands/issue.md:85`; `refs/claim.md:96` | `WCT` has no "Issue pipeline duties", `adopt`, `watcher` or `claim` (0 hits); `COORD-` 0 hits; no Python in `src/` calls Orca `worker-start` or `task-create`; `/sc:issue` is never-as-worker (`WCT:23`); "dispatcher", `COORD-`, "zero-setup watcher": not found in snapshot | NOT BUILT | NOT BUILT | No file records this as out of scope or a replacement as built; `CHANGELOG.md:17` records removal of the old duties; who starts a worker after a claim is undefined (Q-10) |
| D-17 | `issue-pipeline` CLI, WC-17, "Issue pipeline duties" (plan-hash binding, approval record, edit detection, revocation, adoption row, `release-worker`, fixed brief) | `CHANGELOG.md:17`; `docs/user-guide/cli-groups.md:25`; named as live by `DES:43`, `SET:170`, `:274` | `src/superclaude/cli/issue_pipeline/`, `tests/issue_pipeline/`, `tests/cli/test_issue_pipeline_registered.py` absent; only trace: comment `GUARD:496` | REMOVED (deliberate) | REMOVED | Decision: `CHANGELOG.md:17`; commit 01e7a9e23 (PR 682) |
| D-18 | Binding of coordinator-started workers: `orca_worktree.py pending` plus a marker line `[sc-launch:v1:<nonce>]` in the brief | `OW:7-9`, `:1516`; `docs/designs/issue-pipeline-guard-g2.md:9`, `:18`; `WCT:66` | `pending` defined (`OW:1488-1523`, `:1886-1893`) and tested (`tests/skills/test_issue_orca_worktree.py:2472-2498`; `tests/hooks/test_launch_level_guard_worker.py:287`), no production caller; the only marker generator `brief.build` was removed; the contract template (`WCT:303-311`) has no marker slot | DEFECT CANDIDATE | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON | No decision found in the files this reference cites; the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`); the "bound worker" sentences describe a path no code starts |
| D-19 | IR-7 refusal when L2 is not owned | `src/superclaude/commands/issue.md:16`; `SKILL.md:92`; `refs/claim.md:134`; `docs/designs/sc-issue-launch-level-hook.md:34`, `:355`, `:516`, `:615` | `IR7_REFUSE = False` (`OW:822`); branch `:1757-1758`, `:829-831` unreachable; `tests/skills/test_issue_l2_install.py:639` | BUILT-OFF (a constant) | BUILT-OFF (`IR7_REFUSE = False`; not `enabled:false`) | Decision: `OW:818-822` ("owner decision OD-3", "2026-11-08": on only after the #442 observations pass); listed for visibility |
| D-20 | Default `--pipeline` pick from type, complexity, hours | `issue.md:43`; `refs/claim.md:81`; `sc-issue-claim-pipeline-flag.md:21`, `:43` | Prose only; no function computes it; tests pin text (`tests/skills/test_issue_protocol.py:774`, `:791`; `tests/commands/test_issue_command.py:182`) | DEFECT CANDIDATE | NOT BUILT (as code) | No decision found that prose-only is deliberate |
| D-21 | Ship gate "no governed claim until OB-H1 item 1, OB-H2, OB-H3 pass" and the live observations OB-H1..3 and OB-CTX | `issue.md:16`; `SKILL.md:92`; `refs/claim.md:136`; `sc-issue-launch-level-hook.md:6`, `:625` | 0 hits for `OB-H1..3` in `src/superclaude` code; `cmd_launch` (`OW:1696-1834`) never reads a record; 12 tests skip unconditionally (`tests/hooks/test_launch_level_observations.py:79-84`); `--pipeline worktree` or `full` can run today | NOT BUILT | NOT BUILT (mechanism; prose gate) | Design `:625` says "Pending, none run"; no decision lets the gate stay unenforced in code |
| D-22 | IR-3 `pipeline.json` level file | `sc-issue-claim-pipeline-flag.md:58`; `sc-issue-launch-level-hook.md:34`, `:351`, `:615` | 0 hits in `src/` and plugins | NOT BUILT | NOT BUILT | Decision: `pipeline-flag.md:58`, `:4` (documentation only); hook design `:34` |
| D-23 | Approval by a first line `/sc:task` | `templates/launch-prompt.md:23` | `GUARD:347` accepts only `/sc:implement` and `/task` | DEFECT CANDIDATE | NOT BUILT | No decision found (which side is intended: Q-14) |
| D-24 | Automatic action on `W-LAUNCH-NOT-CCSESSION` | `refs/claim.md:130` | `OW:1803-1811` adds a note and continues; no close call | NOT BUILT | NOT BUILT (warning only) | Remedy asks a person to close it |
| D-25 | L1 recognition of the Orca CLI under its real name `orca-ide` | `sc-issue-launch-level-hook.md:119`, `:175` | Guard matches basename `orca` only (`GUARD:457`); observed exit 0 for `orca-ide terminal send` and `orca-ide orchestration send --to run:run_1`; `orca-ide` is the default in `src/superclaude/cli/sweep/probes.py:43` | DEFECT CANDIDATE (observed) | NOT BUILT (recognition of `orca-ide`) | No decision found; the architecture reference `:83` records it as a DEFECT with a draft plan that "is not a fix" |
| D-26 | G2 route B (signed approval file) | `issue-pipeline-guard-g2.md:24` | 0 hits for signature, hmac or openssl in guard and identity | NOT BUILT | NOT BUILT | `guard-g2.md:26` recommends route A, itself REMOVED (D-27) |
| D-27 | G2 rule 1 / route A: coordinator releases a bound worker (`release-worker`) | `issue-pipeline-guard-g2.md:22`, `:45-51` | 0 hits; package deleted; guard comment `:496-497` says retired; only a person's typed `/sc:implement` or `/task` line releases (`GUARD:347-359`) | REMOVED | REMOVED | Decision: `CHANGELOG.md:17` records the removal; guard comment `GUARD:496-497` |
| D-28 | FU-1 runbook commands | `issue-pipeline-fu1.md:64` | Command group absent | DEFECT CANDIDATE (doc names removed commands) | REMOVED (the commands) | Runbook text not updated |
| D-29 | L2 and identity cover more than the tested local Bash surface | `sc-issue-launch-level-hook.md:536-557` | Identity `hook()` returns 0 for non-Bash tools (`launch-job-identity.sh:442-444`) | DEFECT CANDIDATE (declared limits) | BUILT-ON (with limits) | Decision: design `:534` "Limits (OD-1)" |
| D-30 | Capture sheet records the real watcher launch | `SET:616-619` | Lacks `--pipeline none`; watcher sends it (`P/launch.py:92`) | DEFECT CANDIDATE (doc, low) | BUILT-ON | No decision found |
| D-31 | "Grant row": per-issue owner record gating each issue write and live test | `WCT:57` (one mention, undefined); `issue-pipeline-fu1.md:24`, `:26` | No file, verb, path or schema in the snapshot; the removed contract text also used the phrase twice (old `WCT` l.57 and l.300 @01e7a9e23^) | RETIRED | REMOVED (the flow); phrase still in live text | No decision found in the files this reference cites |

### 14.3 Future Considerations

| Item | Deferred Because | Revisit When |
|---|---|---|
| FU-1 live test, then enable the watcher | Gate before `enabled: true` (`DES:33`) | Owner runs the live test and writes the record |
| FU-2 cron entry | Gated behind FU-1 and the shadow run (`DES:861`; `SET:588`, `:676`) | After FU-1 |
| FU-8 auto-retry, FU-10 SLO review, FU-11 pruning, FU-4/5/6/9/12 | "None of these is built by this work" (`DES:856-871`; `SET:669-686`) | FU-8 after FU-1 confirms the argv; FU-10 "after 7 days live"; FU-11 "when the store is above 1 MiB" |
| Binding coordinator-started workers (D-18) | No decision found in the files this reference cites (D-18); the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`) | No revisit trigger found in the files read (Q-11) |
| The OB-H gate as code (D-21) | No decision found that leaves the gate prose-only (D-21); the one related owner decision (OD-3) keeps the IR-7 refusal off (`IR7_REFUSE = False`, `OW:818-822`) until the #442 observations pass | After the #442 observations pass, for the IR-7 refusal (`OW:822`); none recorded for the OB-H gate as code |

#### 14.3.1 Evidence limits and open questions [UNVERIFIED]

| ID | Question or limit | Why it cannot be resolved from files |
|---|---|---|
| U-1 | PRs #447, #448 ("merged, never run live", `DES:3`) and #425, #394, #441, #442 | A snapshot has no history, PR data or runtime state; `enabled` ships false and no schedule is installed ARE [CODE-VERIFIED] |
| U-2 | Real `gh` replies and error strings (`GH_ERROR_SIGNS` `P/github.py:267-278`, `EDITS_QUERY`/`PROJECT_ITEMS_QUERY` `:71-72`) and the Orca launch reply (`OPERATION_ID_PATHS` `P/launch.py:39-45`, `OP_UNKNOWN_TEXT` `:47`) | All 19 fixtures are `_assumed_shape`; the shapes are `_assumed_shape` in tests and `[UNVERIFIED]`/`[PROPOSAL, UNVERIFIED]` in source; no live-test record |
| U-3 | Whether `enabled` is true in the owner's real config; whether any Coder cron, dispatcher, coordinator, external scheduler or person runs `issue-watch once` | No config or scheduler artefact in the snapshot; "dispatcher", `COORD-`, "zero-setup watcher": not found in snapshot (the `grep COORD-` over the snapshot excluding `.git` and `.dev` has 0 matches) |
| U-4 | OB-H1 item 1, OB-H2, OB-H3, OB-CTX (12 skipped tests) | Never run; design `:625` "Pending, none run" |
| U-5 | Orca CLI flags valid in the installed Orca; tier model order; Claude Code model resolution and the proxy's HTTP 400 text; `skills list --json` side-effect free; interactive mode of the launched session; six-field cron; runbook shell commands | External behaviour; no real `orca` run; tests use a fake `orca` (`tests/skills/test_issue_orca_worktree.py:1-6`) |
| U-6 | Who calls `orca_worktree.py pending`; how a coordinator learns a worker's session id; whether `brief.build` had any caller besides tests | No production caller found; only `git show` of named paths was allowed for the removed tree |
| U-7 | FU-1 recorded lines a to k (`docs/designs/issue-pipeline-fu1.md:108-119`); L2 cost "about 100 ms" (`sc-issue-launch-level-hook.md:617-623`); shim screen text visible "1-2 s" (`OW:793-794`) | Live or timing results written in text; nothing can re-run them |
| U-8 | "739 tests" for `tests/skills/test_worker_contract.py` (architecture reference `:208`); contract installed by `install_core.py:27` and not `@`-imported; location of the Orca `orchestration` skill; formats of `dispatch.json` and the approvers file as read by the removed `stage-status` | The file has 59 `def test_`; other items are outside the files read; no `orchestration*` path under `src/` |
| U-9 | Issue #384, #315 and review-panel PN1 decisions cited by `tests/skills/test_model_alias_policy.py:1`, `:35-37`, `:42`; whether two other docs pin T3 to tier3 | Issues and docs not read |
| U-10 | Owner-policy questions: stuck-entry cost (Q-02); unseen edit window (Q-03); `LaunchOutcome.detail` (Q-04); `launch_login` (Q-05); orphan tmp (Q-06); retry argv uses bare `orca-ide` (Q-07, `P/cycle.py:1262-1267`); `status` shows `disabled since: no` for a dangling `DISABLED` (Q-08); `reset --rate-limit --forfeit-guarantee` silently ignored (Q-09, `P/cli.py:309-313`); `degraded` session blocks every Bash call via identity (Q-18); claim does not refuse without `ccsession-orca` (Q-19); two meanings of "shim" (Q-20); `session-start.sh` uses bare `python3 -c` (Q-21, `:20-21`) | No file states the intent |
| U-11 | Evidence limits: tests were read by name and selected bodies, not run; counts are `grep` counts that do not expand parametrisation; large parts of some files were not read; a negative grep means only "no hit for these terms". The guard was run once in a sandbox HOME on 44 payloads (all matched the code reading); identity, L2, install and claim paths were not executed | Read-only research (Q-22 to Q-24) |

**Identifier map.** The `Q-` identifiers in this reference come from the gap log (Section 15.4). Where one has no row of its own in this section, it maps as follows: Q-10 is D-16; Q-11 is D-18 (and the "Binding coordinator-started workers" row of 14.3); Q-12 is U-4 and D-21; Q-13 is U-6 and D-18; Q-14 is D-23; Q-17 is D-25; Q-02, Q-03, Q-04, Q-05, Q-06, Q-07, Q-08, Q-09, Q-18, Q-19, Q-20 and Q-21 are listed in U-10; Q-22 to Q-24 are in U-11.

#### 14.3.2 Architectural risks (evidenced by the research only)

| Risk | Evidence |
|---|---|
| Enforcement is bound only by claim launches; the watcher launch and coordinator-started workers are ungoverned | `GUARD:391`; D-18; research 05 "Not defects but worth stating" |
| Several controls are prose run by the model (default level, ship gate, STOP rules, hand-off) | D-16, D-20, D-21; `refs/claim.md:81` |
| Guard misses the real Orca binary name | D-25 (observed exit 0) |
| Every outward reply shape is assumed; failure reasons are unverified | U-2; 19 fixtures |
| Unbounded or unread state: no `audit.jsonl` reader, no store pruning, orphan temp files, write-only fields | D-02, D-11, D-13, D-14 |
| Design docs still instruct removed commands and no test scans `docs/designs/` | 14.1.2 (KW-3, KW-4, X-9); `tests/skills/test_model_alias_policy.py:50` |

---

## 15. Verification & Accuracy

> This section lets a reader re-check the document. Every fact here was taken from a snapshot of origin/master 61ac2c2e6 (removed code from 01e7a9e23^). Line numbers are for that snapshot and must be re-read from the live file before they are cited again.

### 15.1 Verification Log

| Date | Verified By | Code Version / Commit | Sections Verified | Issues Found |
|------|------------|----------------------|-------------------|-------------|
| 2026-11-20 | Six codebase research agents (research files 01 to 06, read-only against the snapshot), six synthesis agents (synthesis files 01 to 06, each already verified at the synthesis gate before assembly), then one assembler (assembly and cross-check only; it re-verified no source line) | origin/master 61ac2c2e6; removed code at 01e7a9e23^ | Sections 1 to 14, Appendix A, Appendix B | Doc-versus-code contradictions and stale docs are listed in Section 14.1.2; open and unverifiable items are listed in Section 14.3.1; the assembler's cross-section check found no contradiction between sections (see 15.6) |

### 15.2 Spot-Check Protocol

Set the snapshot root once: `S=/home/coder/.cache/ic-snap-20261120/master`. Every command in the code block under the table only reads the snapshot or runs read-only `git`; none writes. The expected result of each numbered check is in the table; the `# n` comments in the block match the `#` column. The commands are outside the table so that a pipe or a regex can be copied as written.

| # | Claim in this document | Expected result |
|---|------------------------|-----------------|
| 1 | The watcher package has eight modules and an empty `__init__.py` (Sections 1, 3) | `__init__.py audit.py cli.py cycle.py github.py launch.py predicates.py record.py runner.py` |
| 2 | `enabled` defaults to false (Sections 2.3, 5.1, 9.1) | one hit near line 228 |
| 3 | The watcher's `gh` argv are five list literals, all reads (Sections 4.5, 5.1.2) | five hits (lines 177, 183, 204, 231, 255) |
| 4 | The launch argv has 12 elements and the prompt ends `--pipeline none` (Sections 4.4, 5.1.3, 8.1) | the prompt builder and the 12-element argv list |
| 5 | `MAX_LAUNCHES_PER_CYCLE` is defined and never read (Sections 5.1.7, 14.2.1 D-01) | one hit, `cycle.py:35` |
| 6 | The IR-7 refusal is a constant set to False (Sections 2.3, 5.2, 14.2.1 D-19) | `IR7_REFUSE = False` near line 822 and the guarded branch near line 1757 |
| 7 | The contract has no WC-17 and no "Issue pipeline duties" (Sections 2.3, 5.4) | `0` from `grep -c`; `339` from `wc -l` |
| 8 | No dispatcher or `COORD-` worktree exists for the issue pipeline (Sections 2.3, 4.4) | no output |
| 9 | The guard matches the command word `orca` only, not `orca-ide` (Sections 5.3, 14.2.1 D-25) | the case arm `orca)`; count `0` |
| 10 | Typed approval accepts `/sc:implement` and `/task`, not `/sc:task` (Sections 5.3, 14.2.1 D-23) | the regex `^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)`; the template line naming `/sc:implement`, `/sc:task` or `/task` |
| 11 | The guard hook is registered twice (once per event) and the identity hook once (Sections 5.3, 8.4) | the `UserPromptSubmit` guard entry, the `PreToolUse` guard entry and the `Bash` identity entry, each with `timeout: 5` |
| 12 | The plugin copies of the launch scripts are byte-identical (Sections 5.3, 12.1) | no output (identical) |
| 13 | The removal is recorded in the changelog and the package is absent (Sections 2.3, Appendix B) | the changelog line naming the removal; `No such file or directory` |
| 14 | The removed package had 10 files (Appendix B.1) | ten paths |
| 15 | `release-worker` created the `.ok` file with `O_EXCL` (Appendix B.4) | the `os.open` call with `O_WRONLY \| O_CREAT \| O_EXCL \| O_NOFOLLOW` |
| 16 | There are 19 assumed-shape fixtures (Sections 1, 5.1.2, Appendix A.1) | `19` |
| 17 | `test_audit.py` has 46 test functions and pins the 59 reason words (Section 5.1.6, Appendix A.1) | `46`; the `REASON_TABLE` block |
| 18 | The claim marker is the last line of the claim comment template (Sections 2.4, 4.2) | the last non-blank line is `<!-- sc:issue:claim -->` |

```bash
S=/home/coder/.cache/ic-snap-20261120/master
# 1
ls "$S/src/superclaude/cli/issue_watch/"
# 2
grep -n 'raw.get("enabled", False)' "$S/src/superclaude/cli/issue_watch/cycle.py"
# 3
grep -n '"gh"' "$S/src/superclaude/cli/issue_watch/github.py"
# 4
sed -n '84,116p' "$S/src/superclaude/cli/issue_watch/launch.py"
# 5
grep -rn 'MAX_LAUNCHES_PER_CYCLE' "$S/src" "$S/tests"
# 6
grep -n 'IR7_REFUSE' "$S/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py"
# 7
grep -c -e 'WC-17' -e 'Issue pipeline duties' "$S/src/superclaude/core/WORKER-CONTRACT.md"
wc -l "$S/src/superclaude/core/WORKER-CONTRACT.md"
# 8
grep -rIn 'COORD-' "$S" --exclude-dir=.git --exclude-dir=.dev
# 9
sed -n '457p' "$S/src/superclaude/hooks/scripts/launch-level-guard.sh"
grep -c 'orca-ide' "$S/src/superclaude/hooks/scripts/launch-level-guard.sh"
# 10
sed -n '347p' "$S/src/superclaude/hooks/scripts/launch-level-guard.sh"
sed -n '23p' "$S/src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md"
# 11
sed -n '63,71p;115,134p' "$S/src/superclaude/hooks/hooks.json"
# 12
cmp "$S/src/superclaude/hooks/scripts/launch-level-guard.sh" "$S/plugins/superclaude/hooks/scripts/launch-level-guard.sh"
# 13
sed -n '17p' "$S/CHANGELOG.md"
ls "$S/src/superclaude/cli/issue_pipeline"
# 14
git -C /home/coder/workspaces/IronClaude ls-tree -r --name-only 01e7a9e23^ -- src/superclaude/cli/issue_pipeline/
# 15
git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:src/superclaude/cli/issue_pipeline/release.py | sed -n '57,62p'
# 16
ls "$S/tests/issue_watch/fixtures/_assumed_shape" | wc -l
# 17
grep -c 'def test_' "$S/tests/issue_watch/test_audit.py"
sed -n '26,102p' "$S/src/superclaude/cli/issue_watch/audit.py"
# 18
tail -n 3 "$S/src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md"
```

### 15.3 Evidence Limits

A snapshot has no runtime state, no git history and no PR data. The tests were read, not run. Only the L1 guard script was executed, once, against 44 sample payloads in a sandbox HOME (Section 5.3 observation run); the identity hook, the L2 hook, the installers and the claim scripts were read only. A negative search (for example zero hits for `COORD-`) proves only that the searched terms are absent from the snapshot. Items that need a live system stay [UNVERIFIED] and are listed in Section 14.3.1. Counts are `grep` counts that do not expand parametrised tests.

### 15.4 Evidence Trail

| Kind | File (absolute path) |
|------|----------------------|
| Research 01 | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/01-watcher-decision-engine.md` |
| Research 02 | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/02-watcher-io-github-launch-record.md` |
| Research 03 | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/03-watcher-operator-surface-and-setup.md` |
| Research 04 | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/04-claim-flow-and-orca-worktree.md` |
| Research 05 | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/05-guard-stack-and-ccsession.md` |
| Research 05 observation run (sandbox and outputs) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/05-guard-run-sandbox/` |
| Research 06 | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/06-coordinator-text-and-removed-code.md` |
| Synthesis 01 (Sections 1, 2) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/synth-01-overview-architecture.md` |
| Synthesis 02 (Sections 3, 4, 6, 7) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/synth-02-directory-dataflow.md` |
| Synthesis 03 (Section 5.1) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/synth-03-subsystem-watcher.md` |
| Synthesis 04 (Sections 5.2 to 5.4) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/synth-04-subsystem-claim-guard-coordinator.md` |
| Synthesis 05 (Sections 8 to 11, Appendix A) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/synth-05-integration-config-tests.md` |
| Synthesis 06 (Sections 12 to 14, Appendix B) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/synth-06-conventions-extension-debt-appendix.md` |
| Gap and question log (cited by synthesis 04 and 06) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/gaps-and-questions.md` |
| Build request (goal, required content) | `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/BUILD-REQUEST.md` |

### 15.5 Remediation and Web Research

- **No remediation tasks were created.** The run that produced this reference may write nowhere outside its task folder and this output file, so the rows in Section 14.2.1 are listed for the owner to decide; none is relabelled a "known gap" unless a cited file records that decision.
- **Web research was skipped.** The subject is repository-internal (code, tests and design documents in one repository), so no external source could add evidence, and no repository or owner detail was sent to an outside service.

### 15.6 Assembly Cross-Check

| Check | Result |
|-------|--------|
| Section 8 integration points against the subsystem descriptions in Section 5 | Match: the same commands, hand-off files and registrations appear in 8.1 to 8.4 and in 5.1 to 5.3, including the worker `orca orchestration send` / `ask` command and the `orca` allow-list of G2 rule 2 (guard-stack table of 8.1) |
| Section 6 state stores against Sections 4 and 5 | Match: stores 1a to 1f, 2a to 2e and 3a to 3d appear in the data flow (4.1 to 4.3) and in 5.1.3 and 5.3 |
| Section 12 conventions against the patterns in Section 5 | Match: each convention names a mechanism described in 5.1 to 5.3 |
| Section 14 against every [CODE-CONTRADICTED], [STALE DOC], NOT BUILT and DEFECT CANDIDATE finding | Every such finding in Sections 4, 5 and 8 has a row in 14.1.2 or 14.2.1 |
| Live-versus-switched-off ledger (2.3) against the status lines in Section 5 and the rows of 14.2.1 | Match on every row (watcher BUILT-OFF = D-06; IR-7 BUILT-OFF = D-19; scheduler = D-04; live-test record = D-05; observations = D-21; coordinator duties and hand-off = D-16, D-17; binding = D-18; G2 rule 1 = D-27; `pipeline.json` = D-22) |
| Facts stated twice | Identical in wording and numbers where checked (59 reason words, 19 fixtures, 12-element argv, 37 calls per cycle, 339-line contract, 10-file removed package) |
| Tables carried by two synthesis files | The overlapping tables (watcher `gh` reads, exit codes, reason words, hook registrations, dispatch.json fields) differ in columns and grouping between files, so each is kept where its file placed it; no table is identical in both |

---

## 16. Glossary

Every definition below is taken from the synthesis files of this reference.

| Term | Definition |
|------|------------|
| Snapshot | The read-only export of origin/master at 61ac2c2e6 that this reference describes; it has no runtime state, history or PR data |
| BUILT-ON | The code exists and is wired into a path that runs in a normal install; it does not say any machine has run it |
| BUILT-OFF (enabled:false) | The code exists but a switch keeps it from running; for the watcher this is the `enabled` config key defaulting to false, for IR-7 it is the constant `IR7_REFUSE = False` |
| NOT BUILT | No code implements the capability in the snapshot |
| REMOVED | The code existed and was deleted (commit 01e7a9e23, PR 682) |
| Guard layer L1 | The Claude Code hook `launch-level-guard.sh`; it binds a session to a level and blocks action classes on every prompt and tool call |
| Guard layer L2 | The git `pre-push` hook `launch-level-pre-push.sh`; it refuses pushes to `refs/heads/main` and `refs/heads/master` by a governed or unknown actor |
| Pipeline level | A `--pipeline` value of `/sc:issue --claim`: `worktree`, `full`, `full --submit` or `none` |
| Launch level | The level the guard stores for one bound session: W, WA, F or FS; `none` has no launch level because the claim ends before any launch |
| W | Launch level `worktree`: no implement, commit, push or submit until a typed approval |
| WA | Launch level `worktree` approved: W after the session file `sessions/<sid>.ok` exists; implement is allowed, commit, push and submit are not |
| F | Launch level `full`: implement allowed; no commit, push or PR |
| FS | Launch level `full --submit`: commit, push and submit allowed; merge, push to main or master and free-form `gh api` writes stay blocked |
| Pending file | `~/.claude/state/launch-level/pending/<32 hex nonce>`: holds one level word (`worktree`, `full` or `full-submit`), written by the claim and consumed once by the guard |
| Session file | `~/.claude/state/launch-level/sessions/<session_id>`: the hard link that binds a session to its level; first binding wins; only a person removes it |
| Nonce | The 32-hex token in the launch marker `[sc-launch:v1:<nonce>]` that names the pending file |
| Governed session | A session with a valid id and an existing `sessions/<id>` file; anything else is ordinary and exits 0 |
| `dispatch.json` | The watcher's local store in `<state_dir>`: 7 top-level keys, 17-field entries, 6 entry states; written before the launch call |
| Entry states | `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed`; `claimed` is terminal |
| T-1 to T-13 | The numbered state transitions of a `dispatch.json` entry (Section 5.1.3) |
| `REASON_TABLE` | The closed vocabulary of 59 reason words in `audit.py`, each mapped to a kind and an exit code |
| Trigger label | The label named by `labels.trigger` (default `issue-watch:trigger`); discovery G2 selects open issues that carry it and are assigned to the watcher's login |
| Approval label | The label named by `labels.approval` (default `issue-watch:approved`); the add-event of this label by an allow-listed human is the approval |
| `DISABLED` file | `<state_dir>/DISABLED`; if it exists (any type, even a dangling symlink) the watcher stops with `disabled` or `disabled_mid_cycle`, exit 0 |
| G1 to G7 | The seven read-only `gh` calls of the watcher: login, discovery, events, comments, edits, project items, re-read |
| S1 halt | The rule that ends the candidate loop after the first launch-step outcome, so at most one launch step runs per cycle |
| Dry-run | `once --dry-run`: runs the cycle up to the launch step, ignores `enabled`, writes only `dry-run.json` |
| `_assumed_shape` | Marker on the 19 test fixtures whose `gh` and Orca reply shapes are assumptions, not captured from a live system |
| Claim marker | The hidden last line `<!-- sc:issue:claim -->` of the claim comment; the watcher reads it through G4 to move an entry to `claimed` |
| Wave | A numbered step (0 to 8) of the claim protocol; waves are prose run by the model, not a program |
| Orchestrator | The Claude session that invoked the `/sc:issue` skill; it makes every GitHub, ClickUp and Orca write; the workers t1, t2, t3 are read-only |
| G2 rule 1 | The removed guard rule that treated coordinator-side pipeline verbs (including `release-worker`) as tampering by a bound worker |
| G2 rule 2 | The guard rule that lets a bound worker run `orca orchestration send` or `ask` only with no `--to` |
| IR-3 | The `pipeline.json` level file; NOT BUILT |
| IR-4 | The claim's enforcement preflight before a governed launch; BUILT-ON; refuses with `W-ENFORCEMENT-ABSENT` |
| IR-7 | The refusal of a launch when the L2 hook is not owned; BUILT-OFF through `IR7_REFUSE = False` |
| OB-H1 to OB-H3, OB-CTX | The live observations the launch-level design requires before a governed claim; never run (12 tests skip) |
| WC-n | A numbered rule of `WORKER-CONTRACT.md`; the snapshot has WC-2 to WC-16 and no WC-17 |
| WC-17 | The removed contract rule "Plan approval is the reply to the worker's own ask" |
| `LL-*` words | The 18 block words of the L1 guard (for example `LL-IMPL`, `LL-TAMPER`, `LL-BROKEN`) |
| Class (guard) | The kind of action the guard detects: IMPL, COMMIT, PUSH, SUBMIT, TURN, SKILL and ten classes blocked at every level (REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG) |
| Job identity | The hook `launch-job-identity.sh`; it wraps governed Bash calls so the L2 hook can ask `identify` whether the pusher is governed, ordinary or unknown; it is not a sandbox |
| ccsession shim | `ccsession-orca`, Orca's Claude command; it carries no launch level; the claim only detects it and warns |
| Grant row | A phrase in `WORKER-CONTRACT.md:57` for an owner record; no store, verb or schema defines it |
| FU-1, FU-2 | Follow-ups of the watcher design: FU-1 is the owner-run live test, FU-2 is the cron entry that would run `once` |
| Plan hash | In the removed package: one SHA-256 over a named list of plan files, bound into the approval text |

---

## Appendix A: Test-Pin Matrix

Counts: Lines = `wc -l`; Tests = count of `def test_` (the strict count is given where the plain `grep -c` differs); a parametrized function counts once, so collected cases are higher. No test was executed in this research: "pins" means what the test asserts when read, not a pass result. All tests below use fakes, stubs or temporary homes; none calls the real GitHub (`gh`) or Orca, and the pre-push and L2-install tests run real `git` against temporary local repositories and a local bare remote, so they prove self-consistency with assumed reply shapes, not agreement with the live tools.

### A.1 `tests/issue_watch/` (watcher)

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/issue_watch/conftest.py` | 1155 | 0 (fixtures) | test support | `FakeClock`, `FakeRunner`, `CrashingStore` (`CRASH_POINTS = (None,"C1","C3","C4","C5")`), `FailingStore`, `FakeLauncher`, `GhWorld`; `make_config` builds an ENABLED config (`:352`) so the `enabled:false` path is pinned only by `test_cycle.py:1607, 1623` |
| `tests/issue_watch/test_cycle.py` | 4982 | 237 | decision engine | `load_config` rules and defaults, `validate_approvers`, `resolve_exit` over every pair and subset, `Deadline` constants 240/5/120, idle cycle = 2 `gh` calls, `not_enabled` and `DISABLED` = 0 calls, S1 halt (one launch step per cycle), durable `pending`, 32+3 budget, 50-cycle at-most-once, dry-run isolation; no test references `MAX_LAUNCHES_PER_CYCLE` |
| `tests/issue_watch/test_github.py` | 2161 | 141 | watcher I/O | the seven argv written out literally, `--method GET` on REST and none on GraphQL, no mutation or upstream repo in any argv, `classify` rows, rate-limit wait and clamp, `CallBudget` 32/35, paging 99/100/101 and page cap 5, discovery bound 100, hostile values never reach an argv; pins the 19 fixtures are labelled and each is read (`:575-597`) |
| `tests/issue_watch/test_record.py` | 2377 | 147 | dispatch record | store schema (7 keys, 17-field entries), `store_invalid` cases, save is sorted/ASCII/0600/fsync, lock cases, DISABLED, T-1..T-13 one case each and every other pair raises `TransitionError`, half-open windows, day cap, `init_state` modes, dry-run shadow; key lists are literal, not read from the module |
| `tests/issue_watch/test_cli.py` | 1672 | 60 | operator surface | exactly five verbs, shared `--config`, `check-config`, `once` exit code = cycle code, crash gives exit 1 with class name only, `status` JSON fields and exit follows age, `init-state`, every `reset` rule (usage errors before config, refusals, day-cap kept, exit 75 and 6) |
| `tests/issue_watch/test_security_invariants.py` | 1013 | 16 | prompt and argv safety | only `/sc:issue --claim <n> --pipeline none` reaches `--prompt` (2000 seeded draws, 31 attack strings); every argv is an allowed form; GraphQL constants read-only; launch argv is exactly 12 elements |
| `tests/issue_watch/test_no_text.py` | 971 | 22 | no GitHub text stored | a canary title/label/login never reaches state files, argv, prompt or output; audit keys are a closed set; 500-byte stderr cap; crash line names the class only |
| `tests/issue_watch/test_launch.py` | 952 | 66 | launch and origin | `build_claim_prompt` int 1..999999999; `launch_argv` literal 12 elements; agent `claude`; `retry_argv`; Orca probe order and relative-path skip; origin parse tables and `check_origin`; outcome table (op-unknown wins over a valid reply); only the launch passes `cwd` |
| `tests/issue_watch/test_audit.py` | 849 | 46 | audit log | the 59 reason names and every `(kind, exit)` pair pinned literally; `line()` rejections; one-`os.write` append, 0600; rotation at 5 MiB keeping four files; exit-75 path never rotates; stderr fallback has five keys |
| `tests/issue_watch/test_predicates.py` | 732 | 44 | pure predicates | `approval_of` rows, `unchanged_since`, `is_intended_owner`, `project_check`, `marker_in_window` (skew floor, `pending_at` wins), `eligibility_order`, `parse_utc`, `valid_operation_id`; every predicate reason is in the audit table |
| `tests/issue_watch/test_cli_e2e.py` | 443 | 4 | end to end (PATH stubs) | real process: idle cycle = exactly 2 `gh` calls and stdout `cycle: cycle_complete`/`exit: 0`; one launch through `orca-ide` with the literal argv; `pending` already on disk at launch time; a second `once` launches nothing |
| `tests/issue_watch/test_slo_helper.py` | 421 | 14 | SLO reducer | `slo_numbers`: nearest-rank p95, 7-day exit-0 share excluding `disabled`, `not_enabled` and dry-run, claimed-within-lease share, stale count; the reducer has no production caller |
| `tests/issue_watch/test_module_boundaries.py` | 413 | 13 | architecture | exactly nine modules, per-module import allow-list, `fcntl` and `swarm.atomic` imported inside functions, exactly four Protocol classes |
| `tests/issue_watch/test_crash_injection.py` | 373 | 6 | crash safety | crash at C1-C5 then five more cycles: launcher called at most once, a recorded call leaves `launches` 1 |
| `tests/issue_watch/test_find_orca_parity.py` | 288 | 10 | Orca discovery | `launch.find_orca` equals `install_user_setup._find_orca` on the same probe replies; rejects where the original raises |
| `tests/issue_watch/test_concurrency.py` | 275 | 6 | locking | two real processes on one store give one launch and one `lock_held`; symlinked, directory or missing lock gives exit 6; replaced-after-`flock` gives exit 75 |
| `tests/issue_watch/test_no_shell.py` | 266 | 9 | no shell | AST scan: no `shell=` other than False, no `os.system`/`os.popen`, `import subprocess` only in `runner.py` |
| `tests/issue_watch/test_runner.py` | 226 | 16 | subprocess runner | `TypeError` for non-list argv, `shell=False`, `cwd` only when given, stderr cut to 500 bytes on a character boundary, timeout and spawn error shapes |
| `tests/issue_watch/test_origin_parity.py` | 179 | 7 | origin parsing | `launch.parse_origin` equals `origin_repo.parse_origin_url`; only `check_origin` compares lower-cased with `ironbellyorg/ironclaude` |
| `tests/issue_watch/test_marker_contract.py` | 53 | 3 | claim marker | `CLAIM_MARKER` literal present in both `src/` copies (`refs/claim.md`, `templates/claim-comment.md`), the template's last non-blank line is the marker, `MARKER_JQ` embeds it |
| `tests/issue_watch/fixtures/_assumed_shape/` | 19 files, 12,059 bytes | n/a | reply fixtures | all 19 carry `_assumed_shape: true`; all reply shapes are still assumed and no live-test record exists; count and "every file is read by a test" pinned by `test_github.py:575-597` |

### A.2 `tests/hooks/` (guard stack)

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/hooks/test_launch_level_guard.py` | 4631 | 162 (163 by plain grep: the extra hit is a string literal at `:4615`) | L1 guard | real script run with JSON on stdin; binding B1-B13 and single-use nonce; the hand-written level grid (`test_grid_policy`); IMPL spellings and look-alikes stay NONE; the 18 words (`:1712`); typed approval writes `.ok` only at `worktree` and plain `approved` releases nothing; precedence; `LL-BIG` above 65536 bytes |
| `tests/hooks/test_launch_level_guard_l2_tokens.py` | 160 | 7 | L1 tamper tokens | hook-file edits and `.git/hooks`, `--no-verify`, `hookspath`, `hook.pre-push` are TAMPER; guard and plugin copy byte-identical |
| `tests/hooks/test_launch_level_guard_registration.py` | 127 | 7 | hook registration | guard registered once per event with timeout 5, no `onFailure`, matcher equals the design string, identity hook stays last, both `hooks.json` trees agree |
| `tests/hooks/test_launch_level_guard_with_identity.py` | 212 | 5 | guard plus identity | `full --submit` allowed and identity replaces only the command; guard sees the original command; a `degraded` record blocks all Bash through identity |
| `tests/hooks/test_launch_level_guard_worker.py` | 300 | 11 | G2 rule 2 | a marker prompt binds a worker; `orchestration send`/`ask` allowed only without `--to`; other workers, groups and orca verbs off the allow-list blocked (a short `--help` or `-h` call stays allowed, `:226-230`); forged release is TAMPER; a test caller of `orca_worktree.py pending` (`:287`; the other is `tests/skills/test_issue_orca_worktree.py:2472-2498`) |
| `tests/hooks/test_launch_job_identity.py` | 1530 | 56 | job identity | prepare/run/identify on real Linux sessions, refusals, stale/orphaned/foreign records, hook command replacement, missing `uv`/`jq` fallbacks, `setsid` escape unselected |
| `tests/hooks/test_launch_level_pre_push.py` | 1194 | 34 | L2 pre-push | matrix T-01..T-24 with real git and a bare remote (create/update/delete/force/mixed/linked worktree), invalid data file, hook sha256 pin, `install_l2` placement, bypass FR-101 |
| `tests/hooks/test_launch_level_pre_push_records.py` | 230 | 8 | L2 record parsing | actor mapping, malformed record, ordinary never reads stdin, no file written |
| `tests/hooks/test_launch_level_observations.py` | 84 | 6 (5 run) | live observations | nine synthetic fixtures and log-only probe; `test_pending_live_observation` (12 cases OB-H1..3, OB-CTX) skips unconditionally: the live observations were never run |
| `tests/hooks/test_require_orca_worktree_agent_governed.py` (added: claim-side pin of the governed branch) | 56 | 1 | worktree-agent hook | a bare worktree create is blocked in a governed session |
| `tests/hooks/test_freshness_subagent_start_policy.py` (added: second registration pin) | 115 | 5 | hook registration | the `Bash` PreToolUse set is exactly `block-bare-python.sh`, `require-orca-worktree-agent.sh`, `launch-job-identity.sh` |

### A.3 `tests/skills/` (claim)

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/skills/test_issue_protocol.py` | 1055 | 62 | claim protocol text | two-way file inventory, Wave ordering (preflight Wave 0, worktree after posts), four launch-prompt blocks, every worktree warning code has a remedy, `none` creates no worktree, ten return fields, default-level text (`:774, :791`), fork safety (`--repo` on every `gh` mention), one allowed `orgs/` read, coordinator paragraph identical in three files |
| `tests/skills/test_issue_orca_worktree.py` | 2501 | 109 | `orca_worktree.py` | fake `orca` on PATH: preflight, lookup keys, exact create argv and no forbidden flag, copy rules, first-tab close, prompt rendering, exact launch argv (LA1), record privacy, shim detection, IR-4 refusal, IR-7 warns and launches, `pending` verb (`:2472-2498`) |
| `tests/skills/test_issue_l2_install.py` | 716 | 26 | L2 install | `install_l2`/`l2_status` on real git: fresh and repeat install, forged entry never owned, `core.hooksPath` unsupported, self-test failure links nothing, `IR7_REFUSE is False` (`:639`) |
| `tests/skills/test_issue_repo_resolution.py` | 291 | 18 | `origin_repo.py` | origin forms, `E-NO-ORIGIN` exit 1, foreign URL exit 3, `/pull/` URL exit 4, only `origin` read, stdlib only |
| `tests/skills/test_issue_worker_agents.py` | 559 | 24 | worker agents | `model:` pins `claude-gw-tier2b` (t3), `claude-gw-tier2` (t2), `claude-gw-tier1b` (t1), t3 `effort: low`, tools exactly `Read, Grep, Glob, Write, Bash`, read-only GitHub rule |
| `tests/skills/test_issue_t1_fallback.py` | 69 | 8 | tier fallback | T1 to T2 fallback text, STOP when not served, no alias fallback, none for T3 or T2 |
| `tests/skills/test_worker_contract.py` | 3220 | 59 | coordinator text | WC-2..WC-16 required text, never-as-worker list (includes `/sc:issue`), write-verb audit that classifies the issue skill and agents, the surviving no-`--to` bullet (`:3216-3220`); no WC-17 or issue-pipeline pin; the doc figure "739 tests" is [UNVERIFIED] |
| `tests/skills/test_clickup_claim.py` (added: pins the only ClickUp write) | 569 | 29 (41 collected cases) | `clickup_claim.py` | fake server accepts only `GET /user`, `GET /team/<ws>/task`, `PUT /task/<id>`; one PUT with `{"assignees":{"add":[4242]}}`; ambiguous, already-assigned and page-capped searches never write; 429 retried once; invalid `CLICKUP_MAX_PAGES` falls back to 20; token never printed |
| `tests/skills/test_model_alias_policy.py` (added: pins worker tier ids) | 249 | 11 (13 collected cases) | model alias policy | `ISSUE_WORKER_PINS` (`:29-33`) must equal each worker `model:`; `claude-gw-tier` text only in allowed paths; issue chains pass no `--models`; the other seven tests are repository-wide alias policy |

### A.4 Other Directories

| Path | Lines | Tests | Piece | What it pins (behaviours, constants, invariants) |
|---|---|---|---|---|
| `tests/commands/test_issue_command.py` | 212 | 15 | `/sc:issue` front | version `1.1.0`, exactly seven flags, no repo/dry-run/preview option, STOP rules, `E-SUBMIT-NEEDS-FULL`, default-level text with the watcher explicit (`:182`) |
| `tests/cli/test_issue_body_templates.py` | 97 | 5 | create-mode bodies | handoff and backlog body files ship flat with four headings; `/sc:issue` is the only issue primitive (not a claim test) |
| `tests/cli/test_install_hooks.py` | 1246 | 37 | hook installer | merge cases 1-8, force refresh, backup, launch scripts packaged, executable and mirrored, guard registers both events idempotently, upgrade lands before identity, pre-push sha256 pin |
| `tests/unit/test_install_ccsession.py` | 417 | 22 | ccsession install | symlink and env seeding, refuses an unmanaged binary or symlinked skill, older skill without `ccsession-orca` still succeeds |
| `tests/unit/test_ccsession_tag.py` | 7101 | 277 | ccsession wrapper | `CCSESSION_PERMISSIONS=default` drops the bypass (`:1519-1684`), status lines on stderr, prompt passes through unchanged; no test pins "the shim carries no launch level" |
| `tests/unit/test_ccsession_tiers.py` | 3821 | 149 | tier slots | tier model slots and defaults (incl. `tier2b`); no launch-level content |
| `tests/core/test_orca_session_launch_guidance.py` | 62 | 3 | session guidance | the "Orca session launches" paragraph names Claude (CLI), `ccsession-orca`, `worktree create --agent`, `--surface terminal`; identical in both copies |

Total: 48 rows (A.1 21, A.2 11, A.3 9, A.4 7): 44 are the files named for this appendix (the 20 watcher files plus the fixture directory, 9 hooks, 7 skills, 1 command, 2 cli, 3 unit, 1 core) and 4 are added because research shows they pin pipeline behaviour (`test_require_orca_worktree_agent_governed.py`, `test_freshness_subagent_start_policy.py`, `test_clickup_claim.py`, `test_model_alias_policy.py`). Tests that pinned the removed `issue_pipeline` package are listed in Appendix B.

---

## Appendix B: Removed on 2026-11-20

Everything in this appendix is read from commit 01e7a9e23^ (the parent of the removal commit) with read-only `git show`. These files do not exist at 61ac2c2e6. Every line citation is labelled @01e7a9e23^. The removal commit is 01e7a9e23 (PR 682), committed 2026-11-19 18:02 -0600, which is 2026-11-20 00:02 UTC. Its message says: "Nothing ran this code: the issue watcher has enabled: false and never ran live. issue_watch is unchanged." Status word for every piece below: REMOVED.

### B.1 What was removed

Directory `src/superclaude/cli/issue_pipeline/` @01e7a9e23^ (10 files, 1,597 lines):

| File | Lines @01e7a9e23^ | Purpose |
|---|---|---|
| `__init__.py` | 5 | Docstring only: the approval core for a coordinator-started plan-writing worker; imports from `issue_watch`, never the reverse (boundary pinned by `tests/issue_watch/test_module_boundaries.py`) |
| `approval_line.py` | 62 | The only two accepted approval texts and the check against a recomputed plan hash |
| `approval_record.py` | 416 | Approval record and adoption record store (local JSON rows, flock) |
| `brief.py` | 74 | Builds the fixed worker brief from a template and a validated issue number |
| `cli.py` | 395 | Click group `issue-pipeline` with 10 verbs |
| `plan_hash.py` | 90 | One SHA-256 over a named list of plan files |
| `reads.py` | 161 | Read-only `gh` projections of comments, events, edits |
| `release.py` | 66 | Writes the `.ok` file that releases a guard-bound worker |
| `stage_predicates.py` | 301 | Pure functions that decide plan-reply, label and comment approval state |
| `templates/worker-brief.txt` | 27 | Brief template with head, marker and three complexity rows |

The same commit also changed: `CHANGELOG.md` (+4); `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (one line, `:268`); `docs/user-guide/cli-groups.md` (10 lines); `src/superclaude/cli/main.py` (-4: the import at old `:581` and `main.add_command(issue_pipeline_group, name="issue-pipeline")` at old `:583`); `WORKER-CONTRACT.md` (+1/-12, 350 to 339 lines); `launch-level-guard.sh` and its plugin copy (5 lines removed, 2 added each); the removed tests (B.8).

### B.2 The CLI verbs

Group `issue_pipeline_group` (`click.group(name="issue-pipeline")`, `cli.py:56-58` @01e7a9e23^). Exit codes: `_EXIT_REFUSED = 1`, `_EXIT_CONFIG = 2`, `_EXIT_LOCK_HELD = 75` (`cli.py:29-32`). No verb printed file or GitHub text.

| # | Verb (line) | Arguments and options | Output and exit | Read or wrote |
|---|---|---|---|---|
| 1 | `plan-hash` (`:61`) | `REPORT_DIR`, `NAMES...` | `file: <name>` per sorted name, then `plan-sha256: <hex>`; `refused:<reason>` exit 1 | read plan files |
| 2 | `check-approval` (`:76`) | `REPORT_DIR`, `NAMES...`, `--line` (required), `--issue N` | `ok` exit 0, or the refusal word, exit 1 | read plan files |
| 3 | `init` (`:96`) | `APPROVALS_DIR` | `ok`; `refused:<reason>` exit 1 | wrote dir 0700 and `lock` 0600 |
| 4 | `adopt-create` (`:108`) | + `--issue`, `--stage` (default `plan`) | JSON `created`; `refused:already-started` or `refused:uncertain-launch` exit 1; `lock-held, retry` exit 75 | wrote adoption row |
| 5 | `adopt-mark` (`:117`) | + `--state started\|uncertain`, `--dispatch-id` | JSON `marked` | wrote adoption row |
| 6 | `record-create` (`:134`) | + `--plan-hash`, `--channel label\|comment\|reply`, `--evidence-id`, `--actor` | JSON `created` or `exists` | wrote approval row |
| 7 | `record-show` (`:161`) | + `--plan-hash` | JSON row | read |
| 8 | `record-mark` (`:179`) | + `--plan-hash`, `--state instructed\|acked\|revoked` | JSON `marked` | wrote approval row |
| 9 | `release-worker` (`:200`) | `SESSION_ID`, `--store` (default `~/.claude/state/launch-level`) | `released` or `already-released`; `refused:<reason>` exit 1 | wrote `<store>/sessions/<session_id>.ok` |
| 10 | `stage-status` (`:335`) | `ISSUE`, `--json`, `--config` (default `~/.config/superclaude/issue-watch.json`), `--approvals-dir`, `--plan-dir`, `--plan-file` | one sorted JSON object; config error exit 2; read failure exit 1 | read `gh`, rows, plan files |

### B.3 Approval record format and plan hash

| Item | Rule @01e7a9e23^ |
|---|---|
| Accepted texts | `approved` (comment channel only) or `approved ap-<issue>-plan-<12 hex> plan-sha256=<64 hex>`; whole-text match, no trimming (`approval_line.py:18-21`, `:33-40`) |
| Check results | `ok`, `refused:bare`, `refused:mismatch`, `refused:malformed`, or `refused:<plan-hash reason>` (`:43-62`) |
| Plan hash | SHA-256 over sorted names; per name: `len(name)` 8 bytes big-endian, name, `len(data)` 8 bytes big-endian, bytes; 11 refusal words `no-names`, `bad-dir`, `absolute-name`, `dotdot-name`, `bad-name`, `duplicate-name`, `symlink`, `missing`, `outside-dir`, `not-a-file`, `unreadable` (`plan_hash.py:24-36`, `:77-90`) |
| Store | Caller-named directory (no default in code), mode 0700, `lock` 0600, symlink refused (`approval_record.py:81-98`) |
| Adoption row | `adoption-<issue>-<stage>.json`; keys `kind`, `issue`, `stage`, `state`, `dispatch_id`, `created_at`, `updated_at`; states `reserved`, `started`, `uncertain` (`:126-139`, `:44`) |
| Approval row | `approval-<issue>-<stage>-<64 hex>.json`; keys `kind`, `record_id`, `issue`, `stage`, `plan_hash`, `state`, `evidence`, `created_at`, `updated_at`; states `recorded`, `instructed`, `acked`, `revoked`; evidence keys `channel`, `id`, `actor`, `time` (`:132-153`) |
| Writes | JSON via `swarm.atomic.write_prepared_bytes`, chmod 0600, directory fsync; every mutation holds the `FileStore` flock; a second caller gets `lock-held` (exit 75) (`:108-123`, `:225-229`) |
| Plan reply marker | `<!-- sc:stage:plan id=<record id> plan=<64 hex> -->` (`reads.py:42`) |

### B.4 The release-worker action and GitHub writes

- `release.release(session_id, store=None)` created the zero-length file `<store>/sessions/<session_id>.ok` with `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0600 (`release.py:57-62`). Refusals: `bad-session-id`, `no-store`, `not-bound`, `not-worktree-level`; a second call gave `already-released`. The guard already read that file: a worktree-level session with it became level `WA`, whose IMPL and TURN classes are allowed (snapshot `GUARD:270-272`, `:786`).
- Who could run it: the coordinator (docstring `release.py:3-4`: "The coordinator calls this after it has recorded a plan approval"); a bound worker could not (guard rule 1, B.6). The old contract text never named the verb or `.ok`.
- GitHub writes: none by the package. Its only `gh` lines were reads: `gh api user --include`; `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>`; `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>`; `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <COMMENTS_JQ>`; `gh api graphql -f query=<EDITS_QUERY> -F number=<N>` (a POST whose query only reads) (argv builders in `P/github.py:175-262`, used by `reads.py`). `test_the_command_only_reads_and_never_calls_orca` (`tests/issue_pipeline/test_stage_status.py:451` @01e7a9e23^) pinned that `stage-status` calls no `orca`.
- The contract text told the coordinator model to write to GitHub without a command line: "Post the plan reply with the hash and file list and mention the assignee" and "mirror the label and Status" (old `WCT:298`); "post an issue write without that issue's grant row" was forbidden (old `WCT:300`).

### B.5 WC-17 and "Issue pipeline duties"

Old `WORKER-CONTRACT.md` (350 lines) @01e7a9e23^.

**WC-17**, "Plan approval is the reply to the worker's own ask" (old `:59`, section 3). Trigger: a brief carrying the `Plan approval:` line. Steps: (1) `superclaude issue-pipeline plan-hash <report-dir> <names>`; (2) `ask` once with path, file list and hash; (3) wait (resume the same message on timeout); (4) `superclaude issue-pipeline check-approval <report-dir> <names> --line <reply>`; (5) `ack <message_id> applied|refused`; (6) continue only on `applied`. A bare `approved`, or any text that is not the reply to its own ask, is never approval; a mismatch is refused and reported in `worker_done`. The sentence "`ask` and `send` carry no `--to`" was kept in the snapshot as `WCT:66`.

**"### Issue pipeline duties"** (old `:291-300`, section 4). Scope: an issue the watcher claimed with `/sc:issue --claim <N> --pipeline none` that this coordinator now owns.

| # | Duty (old line) | Content |
|---|---|---|
| 1 | Adopt (`:295`) | Read only the watcher's `claimed` entry in `dispatch.json` and `.dev/issues/<N>/issue-summary.md`, `next-steps.md` |
| 2 | Reserve before starting (`:296`) | `adopt-create` before `worker-start`; mark `started` with the Dispatch id or `uncertain`; never start again for an `uncertain` row |
| 3 | Worktree, then worker (`:297`) | `orca_worktree.py worktree ...` then `worker-start --worktree path:<path> --agent claude --spec <brief>` |
| 4 | Plan approval (`:298`) | Post the plan reply; read GitHub through `stage-status`; `record-create` only when the worker's `ask` carries the hash; reply `approved <record-id> plan-sha256=<hash>`; mirror label and Status; mark `instructed`, then `acked` |
| 5 | No exception (`:299`) | Route B adds no exception to "never answer a person prompt"; nothing is typed into a worker terminal |
| 6 | Never (`:300`) | Tell a worker to pass its plan boundary without an approval row; act on a Status move alone; relaunch a dead worker alone; "post an issue write without that issue's grant row" |

Facts about names: the duties named `adopt-create`, `adopt-mark`, `stage-status`, `record-create`, `record-mark` (and WC-17 named `plan-hash`, `check-approval`), never `release-worker` or `brief`. "COORD-" was absent from the old contract (0 hits). "grant row" appeared twice (old `:57` and `:300`) and was defined nowhere. In the snapshot `WCT:57` contains "grant row" once, undefined; "dispatcher", `COORD-` and "zero-setup watcher": not found in snapshot.

### B.6 The guard's G2 rule 1 TAMPER case

Old `launch-level-guard.sh` (811 lines) @01e7a9e23^, comment at `:441-444` and the case at `:444`: any Bash text (normalised, `:428`) containing `release-worker`, `release_worker`, `issue-pipeline` followed later by `adopt-` or `record-`, `issue_pipeline` followed later by `release`, or `issue_pipeline` followed later by `approval_record` added the class TAMPER. The decision table (snapshot `GUARD:799`, unchanged) denies TAMPER at levels W, WA, F and FS with `LL-TAMPER` (exit 2). `plan-hash` and `check-approval` stayed allowed. After the removal: G2 rule 2 (`orchestration send`/`ask` with no `--to`, `GUARD:496-537`) and the generic store TAMPER (`GUARD:761`, a forged `.ok` is still `LL-TAMPER`, `tests/hooks/test_launch_level_guard_worker.py:262-270`) remain; the only way to create `.ok` is a person's typed first prompt line `/sc:implement` or `/task` at level W (`GUARD:347-359`). One comment is left at `GUARD:496`.

### B.7 Data flow and safety properties

```
issue-watch once (enabled:false) -> claim: /sc:issue --claim N --pipeline none  [comments, issue-summary.md, next-steps.md, no agent]
        |
        v  (LLM text, coordinator, old WCT:295)  read dispatch.json (read-only) + .dev/issues/N/*
 init APPROVALS_DIR -> adopt-create (row `reserved`, flock) -> orca_worktree.py worktree -> worker-start --spec <brief>
        |                                                           (brief.build: not called by any verb)
        v                         adopt-mark started|uncertain
 worker writes plan -> plan-hash -> ask(path, files, hash)
        |
        v  coordinator posts plan reply with marker <!-- sc:stage:plan id=.. plan=.. --> (GitHub write, LLM text, no command line)
 approver: label or `approved` comment  -> stage-status N (read-only gh) says approved
        |
        v  record-create (row `recorded`) -> reply "approved <id> plan-sha256=<hash>" -> record-mark instructed
 worker: check-approval ok -> ack applied -> record-mark acked
        |
        v  release-worker <sid> -> sessions/<sid>.ok  (level WA)   [which text told a coordinator to call it: UNVERIFIED]
```

Safety properties the package enforced (old code places): exact-text approval (`approval_line.py:18-21`, `:33-40`); plan binding by content, refusing links, `..`, absolute and duplicate names (`plan_hash.py:39-90`; the approval key includes the hash, `approval_record.py:132-134`); no self-approval by a bare word (`approval_line.py:50-51`); approver identity, order and edit detection with fail-closed reads (`stage_predicates.py:145-244`, `reads.py:138-139`); revocation (`stage_predicates.py:171-177`, `approval_record.py:389-416`); at-most-once worker start by write-ahead row (`approval_record.py:235-265`); no GitHub text stored or printed (`reads.py:1-11`; every stored value pattern-checked); a worker could not forge release or rows (guard rule 1); a fixed brief with no issue text (`brief.py:5-8`).

### B.8 Removed tests and test edits

116 tests in 10 files under `tests/issue_pipeline/` (2,391 lines; counts are `def test_` definitions) plus `tests/cli/test_issue_pipeline_registered.py` (15 lines, 1 test):

| File @01e7a9e23^ | Lines | Tests | What it pinned |
|---|---|---|---|
| `test_approval_concurrency.py` | 78 | 2 | one winner for concurrent `record_create` and `adopt_create` |
| `test_approval_crash.py` | 88 | 3 | killed `record_create` leaves `recorded`; kill between `worker-start` and `adopt-mark` blocks a second start; duplicate approval plus crash gives at most one instruction |
| `test_approval_line.py` | 135 | 9 | two accepted texts; variants rejected; mismatch; bare refused; CLI exit codes |
| `test_approval_record.py` | 424 | 21 | store creation, forward-only moves, revoke and reopen, adoption paths, fixed patterns, corrupt rows, exit 75 on a held lock |
| `test_brief.py` | 224 | 12 | golden briefs; only template characters; bug type refused; no row runs implement, commit, push or submit; one marker line |
| `test_plan_hash.py` | 116 | 10 | ordered list and hash; one byte, rename or added file changes it; refusals; symlink refused |
| `test_reads.py` | 295 | 10 | typed projection; approval forms; hostile body never reaches output; page and call caps; failure gives a closed reason |
| `test_release.py` | 89 | 7 | `.ok` is one empty private file; second release no-op; refusals |
| `test_stage_predicates.py` | 466 | 29 | label and comment channels, ordering, edits, revocation, `status_seen` never approves alone |
| `test_stage_status.py` | 476 | 13 | closed keys through an injected runner; reads only, never calls `orca` |
| `__init__.py` and `fixtures/recorded/` (issue 452 responses) | 0 and fixtures | n/a | the recorded issue had no label event, plan reply or approval comment, so every approval case ran on hand-built evidence |
| `tests/cli/test_issue_pipeline_registered.py` | 15 | 1 | `issue-pipeline` and `issue-watch` in `main.commands`; `--help` prints `plan-hash` |

Edits to surviving test files:

| File | Before @01e7a9e23^ | After the commit | Change |
|---|---|---|---|
| `tests/skills/test_worker_contract.py` | 3,181 lines, 61 tests | 3,135 lines (+8/-54); 59 tests | 3 tests dropped (`test_adoption_names_only_sources_that_exist_after_pipeline_none`, `test_adoption_check_fails_when_worktree_json_is_named`, `test_issue_pipeline_duties_allow_no_typing_into_a_worker_prompt`) and `RULE_PHRASES` entries `issue-pipeline-duties` and `wc17-plan-approval` removed; 1 added (`test_the_no_to_rule_sits_in_the_worker_session_duties`); at 61ac2c2e6 the file has 3,220 lines |
| `tests/hooks/test_launch_level_guard_worker.py` | 330 lines, 13 tests | 300 lines (-30 net); 11 tests | `test_a_bound_worker_cannot_run_the_coordinator_side_pipeline_verbs` (old `:270-287`, 6 commands expecting `LL-TAMPER`) and `test_a_bound_worker_may_still_run_plan_hash_and_check_approval` (old `:290-299`) dropped; the chain test now types `/sc:implement plan.md` (current `:255-257`) instead of calling `release.release(SID, store)` (old `:254`); the nonce test no longer imports `brief` |

Research 06 B13 states "-56 net" for the guard worker test; the file lengths (330 to 300) and the commit figures give -30, which is the stronger evidence. The record of research 06 is used for all other figures.

### B.9 What replaced each removed duty

| Removed duty | Replacement at 61ac2c2e6 | 14.2 row |
|---|---|---|
| Approval record, plan-hash binding, approver identity, edit detection, revocation, WC-17 worker wait | no replacement found in snapshot | D-17 |
| Write-ahead adoption row (at-most-once worker start) | no replacement found in snapshot; the watcher's own `dispatch.json` covers the claim launch only | D-16, D-17 |
| Coordinator release of a bound worker (`release-worker`) | a person's typed first line `/sc:implement` or `/task` (`GUARD:347-359`); no coordinator verb | D-27 |
| Fixed worker brief with launch marker (`brief.build`) | no replacement found in snapshot; `pending` exists with no production caller | D-18 |
| Adopt, worktree and `worker-start` sequence ("Issue pipeline duties") | no replacement found in snapshot; `WCT` has general rules WC-2..WC-16 only | D-16 |
| Guard rule 1 (TAMPER on coordinator-side verbs) | generic store TAMPER (`GUARD:761`) and G2 rule 2 remain | D-27 |
| "Grant row" gating each issue write | no replacement found in snapshot; the phrase survives at `WCT:57` | D-31 |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-11-20 | rf-assembler (from research and synthesis files) | Initial creation from code research against origin/master 61ac2c2e6 |

---

> **Template Version:** 1.0.2 (technical_reference_template.md, structure followed)


