# Technical Research Report: Orchestrator mode Phase 1 (read-only /sc:sweep and WC-14), issue #339

**Date:** 2026-11-07
**Depth:** Deep
**Research files:** 8 codebase + 2 web research
**Scope:** `src/superclaude/core/`, `src/superclaude/skills/sc-crash-recovery/`, `src/superclaude/skills/ccsession-tag/`, `src/superclaude/cli/`, `src/superclaude/commands/`, `tests/`, `.dev/orca-command-refactor/inventory/`, the #409 package at `495eb96d` (`.dev/design/orca-observer-20261106/` on the unmerged branch `docs/409-orca-dashboard-designs`)
**Task folder:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/` (all `research/`, `synthesis/`, `qa/` and `gaps-and-questions.md` paths below are relative to it)

**Research question:** Orchestrator mode Phase 1 for issue #339: a read-only, coordinator-only `/sc:sweep` that classifies sessions (waiting on a person, working, stalled (proved), could not determine, finished, idle: the research question's six; Section C of `research/research-notes.md` adds fenced as a seventh class, `research/research-notes.md:188`, and six versus seven is an open question, Section 9; safe-to-close is a separate dimension) over a default 6 h window that bounds activity only, writes a dated static report on the #409 layout, and adds a WC-14 coordinator-loop rule to `src/superclaude/core/WORKER-CONTRACT.md`. `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay are later phases, recorded only. Option A4 (extend sc-crash-recovery) is [CODE-CONTRADICTED] and appears only as a rejected option with its reason. (`synthesis/synth-01-problem-current-state.md:5`)

**Evidence labels:** [CODE-VERIFIED] checked against the named source (for a Markdown contract, the contract text and the tests that pin it, or a live CLI capture); [CODE-CONTRADICTED] (CC) the source says otherwise, corrected to what the source shows; [UNVERIFIED] (UV) not confirmed, sent to Open Questions; [STALE DOC] a document that no longer matches the source; [EXTERNAL] web sources, which never describe this repo's architecture. (`synthesis/synth-01-problem-current-state.md:9`; `synthesis/synth-06-questions-evidence.md:15`)

**NB-4 fix in effect:** GQ-03 (NB-4, the default argv allowlist) is resolved by the fix pass in `qa/qa-nb4-fix-log.md` (2026-11-07). It was a coordinator-approved exception at the Phase 3 research gate. The `scope-03:99` allowlist now includes `orchestration task-list` (`--ready`, `--run <id>`), `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden. (`synthesis/synth-06-questions-evidence.md:11`)

**Phase 6 anti-omission gate passed with exceptions, not clean:** the gate halted on its 2-fix-cycle limit (blocking findings 18 -> 1 -> 2, `[HALT-MONOTONICITY] |F|=2`) with two open blocking findings, and the owner chose (2026-11-08) to carry them as open Important gaps to be fixed at the /sc:design step, with no further fix pass. GQ-101 (NB-2): the step 1.3 one-package-in-two-worktrees pre-pass must count only packages actually running in a worktree, not committed folders every worktree shares (`src/superclaude/core/WORKER-CONTRACT.md:108`). GQ-102 (NB-4c): a package in both `to-do/` and `done/` is a fourth package state, conflict, that blocks removal (`~/.claude/skills/sc-crash-recovery/refs/pipelines.md:198`; `~/.claude/skills/sc-implement-protocol/SKILL.md:39`). Section 8 Phase 1 steps 1.2, 1.3, 1.8 and 1.9 are not yet corrected for either. A later /ponytail-review of the plan added three more blocking plan fixes, carried the same way as GQ-103 (`qa/ponytail-review-phase1-plan.md`). (`gaps-and-questions.md` GQ-101 to GQ-103)

---

## Table of Contents

| # | Section | Subsections | Source |
|---|---|---|---|
| 1 | [Problem Statement](#1-problem-statement) | none | `synthesis/synth-01-problem-current-state.md` |
| 2 | [Current State Analysis](#2-current-state-analysis) | 2.1 worker contract; 2.2 Orca session state; 2.3 crash recovery and ccsession; 2.4 CLI and command patterns; 2.5 #409 designs and the selected layout; 2.6 summary | `synthesis/synth-01-problem-current-state.md` |
| 3 | [Target State](#3-target-state) | 3.1 desired behavior; 3.2 success criteria; 3.3 constraints | `synthesis/synth-02-target-gaps.md` |
| 4 | [Gap Analysis](#4-gap-analysis) | 4.1 severity rules; 4.2 core gaps; 4.3 four known non-critical gaps; 4.4 other open gaps; 4.5 resolved; 4.6 [CODE-CONTRADICTED] corrections; 4.7 [STALE DOC]; 4.8 contradictions; 4.9 open questions; 4.10 coverage | `synthesis/synth-02-target-gaps.md` |
| 5 | [External Research Findings](#5-external-research-findings) | 5.1-5.8 findings; 5.9 contradictions and rejected patterns; 5.10 summary | `synthesis/synth-03-external-findings.md` |
| 6 | [Options Analysis](#6-options-analysis) | constraints; A1; A2; A3; A4 (rejected); comparison | `synthesis/synth-04-options-recommendation.md` |
| 7 | [Recommendation](#7-recommendation) | rationale; implementation steps; external context; 7.1 open questions for the option choice; 7.2 coverage | `synthesis/synth-04-options-recommendation.md` |
| 8 | [Implementation Plan](#8-implementation-plan) | Phase 1; later phases (recorded only); 8.1 gap traceability; 8.2 open questions; 8.3 external context; 8.4 contradictions; 8.5 coverage; integration checklist | `synthesis/synth-05-implementation-plan.md` |
| 9 | [Open Questions](#9-open-questions) | 9.1 GQ rows; 9.2 unverified and contradicted claims; 9.3 stale docs; 9.4 contradictions; 9.5 AMBIGUITIES 1-11; 9.6 resolved rows; 9.7 coverage | `synthesis/synth-06-questions-evidence.md` |
| 10 | [Evidence Trail](#10-evidence-trail) | codebase research; web research; synthesis files; gaps log; QA reports | `synthesis/synth-06-questions-evidence.md` |

---

## 1. Problem Statement

- **The question.** How should IronClaude build Phase 1 of orchestrator mode (issue #339, https://github.com/IronbellyOrg/IronClaude/issues/339): a read-only `/sc:sweep` that only the coordinator runs? It should sort every session into one of the question's six classes (waiting on a person, working, stalled (proved), could not determine, finished, and "idle" for person-started sessions only; Section C adds fenced as a seventh class, precedence rule 3 at `research/research-notes.md:194`, and six versus seven is an owner decision, S9 row 98a), report safe-to-close as a separate dimension, and look back over a default 6 h window that bounds activity only. It writes a dated static report on the #409 layout, and it needs a WC-14 coordinator-loop rule in `src/superclaude/core/WORKER-CONTRACT.md`. All of this must avoid breaking the Orca read rules (absence is never proof) and the repo's registries and tests. (`.dev/issues/339/issue-summary.md`; class names from `research/research-notes.md:188`, Section C.)
- **Why it matters.** #339 asks for one orchestrator session that every other session reports updates and questions through, so the person never has to open a child session. A static report of all agents, sessions and worktrees, modelled on #409, would replace the usual end-of-message table (`.dev/issues/339/issue-summary.md`). Today the contract has no rule that the coordinator keeps polling, re-arms its wait or sweeps on a schedule. No classification vocabulary is written down, and no command does any of this (`research/scope-01-contract.md` gaps G1-G7; `gaps-and-questions.md` GQ-04 to GQ-10). The issue estimates about 40 h of work, about 20 h of it for the sweep; the 40 h also includes about 14 h for `/sc:close` and about 6 h for the comment-3 research (`.dev/issues/339/issue-summary.md:6`), so it covers more than the sweep-only first PR this report plans (phase grouping conflict named under "Later phases" in Section 8). It says most of the base model already exists as the Orca contract (`.dev/issues/339/issue-summary.md`).
- **Trigger.** Issue #339 plus three comments: never stop polling and own cleanup (comment 1, matching the owner order of 2026-11-05 in the memory note `coordinator-never-stop-polling.md`, `gaps-and-questions.md` GQ-04); a trust layer (comment 2); and a request to send the open questions to /tech-research and an adversarial debate (comment 3) (`.dev/issues/339/issue-summary.md`). Out of scope for Phase 1 and recorded only: `/sc:close` (worktree removal after strict checks), resume, the trust layer, an orchestrator of orchestrators, and the management-server relay. The summary also notes two sequencing constraints. Contract edits for #339 should land after open PR #422. The #409 design is on the unmerged branch `docs/409-orca-dashboard-designs` at `495eb96d` (`.dev/issues/339/issue-summary.md`).

---

## 2. Current State Analysis

### 2.1 The worker contract (`src/superclaude/core/WORKER-CONTRACT.md`)

The contract is a 203-line Markdown file, installed to `~/.claude/` by `src/superclaude/cli/install_core.py:27` [CODE-VERIFIED]. Its sections are Terms (:9), Command-side rules (WC-2, 4, 8, 9, 10, 11; :26), Worker duties (WC-3, 5, 7, 12, 13; :48), Coordinator (:64, WC-6 at :68) and the template (:166-203). The Coordinator section covers the brief (:77-97), worktrees (:101-108), git ownership (:110-118), reading a result (:120-129), the stop after `/sc:implement` (:131-152), fan-in (:154-156) and a worked example (:158-164). Rules WC-2 to WC-13 exist and WC-1 is unused, so WC-14 is the next free ID. Whether to add WC-14 or reuse the unused WC-1 ID is an owner decision (`gaps-and-questions.md` GQ-11).

Contract rules a sweep must obey [CODE-VERIFIED against the contract text and `tests/skills/test_worker_contract.py`]:

| Rule | Line(s) | What it means for a sweep |
|---|---|---|
| Person-started sessions are ordinary sessions | :11 | Not workers; "idle" is used only for them (Section C) |
| Never-as-worker list | :20, :23 | `/sc:sweep` is coordinator-only; adding it to the list changes `NEVER_AS_WORKER` (8 entries, `test_worker_contract.py:245-254`; phrase pinned at :86-92) |
| WC-8 / WC-13: no fan-out | :39, :61 | A worker never calls `worker-start`; a non-null worker-show `parent` is reported as a WC-13 violation for review (GQ-40) |
| WC-9 | :40, :43, :117 | Git and worker ownership bounds |
| WC-10: a missing heartbeat is absence | :45 | Act only on Orca's stall proofs; a late heartbeat never means stalled |
| WC-3: no heartbeat while blocked in `ask` | :54-57 | A silent worker may be waiting, not dead |
| WC-3: `On a blocked gate: ask the coordinator` | :52, :54-55 | Under this brief policy (the default is `report blocked`, :53), at an eligible gate the worker asks the coordinator with `ask`, waits, then re-invokes the command in the same session; the second run's contract replaces the blocked one whole (:54). It asks at most once per Task; a second block is kept and reported `failed` (:55). So a `blocked` contract on disk can belong to a live worker that is waiting on the coordinator or re-running, not only to a settled one |
| WC-5: `blocked` maps to Orca outcome `failed` | :58 | Orca outcome alone cannot tell blocked from failed |
| WC-12: `consumer_fenced` | :60 | A fenced worker stops without `worker_done` by design |
| WC-6 | :70, :73, :74 | Coordinator duties when reading a stop |
| Child cleanup and the 5-condition refusal list | :107, :108 | Inputs to the later `/sc:close`, and to the safe-to-close dimension |
| Git ownership, placement map | :112, :114, :105 | Which session owns which tree |
| Reading a result (foreign ready Task) | :122-129 (:129) | A settled row is "finished" only after the return contract is read. For `partial` (:125), dependents do not start until the coordinator has read the contract's `report_path` and recorded whether the partial deliverable is usable; an unusable one is handled like `failed` (then :126: retry, answer, or report the failure to the person). A sweep cannot observe that judgment, so a `partial` row is finished but "partial: usable not yet judged" |
| Freeze after an implement stop | :133-136 | The "frozen or blocked by policy" kind of waiting on a person |
| Fan-in | :156 | Insertion point for WC-14 |

What the contract does not have (`research/scope-01-contract.md` G1-G7; `gaps-and-questions.md` GQ-04 to GQ-10). It has no rule that the coordinator keeps polling (G1), none to re-arm the wait after it expires (G2) and no periodic sweep (G3). It has no classification vocabulary (G4; now filled for the research by `research/research-notes.md` Section C, GQ-07 resolved). It has no rule for when to tell the person (G5), it does not say that person-started sessions are reported (G6, GQ-09; the sources settle that they are, Section 3.1 G6), and it does not say where the report goes (G7, an owner decision, GQ-10). A grep for poll, re-arm, cron, sweep and expire matches only :45. No sweep or close command exists. The candidate WC-14 insertion points are after :156 (before the worked example at :158) or after :129 (before :131).

How the tests pin the contract (`tests/skills/test_worker_contract.py`) [CODE-VERIFIED]:

- `RULE_PHRASES` runs from :25 to :237, with new coordinator rules going under `# Coordinator rules` at :163. The helper `_check_rule` is at :388-395, the positive test at :540-542 and the negative test at :587-594.
- `NEVER_AS_WORKER` is at :245-254. The test named "all_seven" checks 8 entries, so WC-14 work must not rely on that test name (GQ-12, N-34).
- The repo-setup gate is at :446, and `AUDIT_ROOTS` (:1090-1094) scans skills, commands and agents (GQ-13 resolved).
- The file holds 41 test functions.

Copies that move with an edit:

- The plugin HOW-WE-WORK is a byte copy (`test_routing_plugin_parity.py:38`).
- `src/superclaude/core/CLAUDE.md:65-82` copies only the HOW-WE-WORK level table (:11-28; `test_claude_md_routing_block.py:28-32`), so an edit to the Orca section does not touch it.
- `test_how_we_work_routing_table` requires ASCII-only text (:342-347) and uses `_OTHER_COMMANDS` (:27-40, :291-311).

Correction carried from scope-01. The first draft of the analysis cited claims the contract does not support. It was rewritten as F1-F14 plus S1-S5, leaving 12 [CODE-CONTRADICTED] citations corrected in place (tally 54 VERIFIED, 12 CONTRADICTED, 4 UNVERIFIED, `research/scope-01-contract.md`). Only the corrected readings are used above. Whether a test requires registering the command in help or HOW-WE-WORK is [UNVERIFIED] (GQ-14, see Open Questions).

**Evidence:** `src/superclaude/core/WORKER-CONTRACT.md:9`, `:11`, `:20`, `:23`, `:26`, `:39`, `:40`, `:45`, `:48`, `:54-57`, `:58`, `:60`, `:61`, `:64`, `:68`, `:105`, `:107`, `:108`, `:122-129`, `:133-136`, `:156`, `:158`; `src/superclaude/cli/install_core.py:27`; `tests/skills/test_worker_contract.py:25-237`, `:163`, `:245-254`, `:388-395`, `:446`, `:540-542`, `:587-594`, `:1090-1094`; `tests/commands/test_routing_plugin_parity.py:38`; `tests/core/test_claude_md_routing_block.py:28-32`; `tests/core/test_how_we_work_routing_table.py:27-40`, `:291-311`, `:342-347`; `src/superclaude/core/CLAUDE.md:65-82` (all via `research/scope-01-contract.md`).

### 2.2 Orca session state as the CLI exposes it

The installed CLI is `orca-ide` 1.4.245-aidev02, and verbs are spelled `orca-ide orchestration <verb>`. A bare top-level `worker-list` prints "Unknown command". The inventory `.dev/orca-command-refactor/inventory/orca-capabilities.md` was written against 1.4.237, so its guide line numbers are stale [STALE DOC] (`research/05-orca-row-schema.md:40`, `:61`, `:199`). All captures used here come from `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/`. They were taken on 2026-11-05 on a CLI version between those two, which the files do not record (GQ-41).

**worker-list** [CODE-VERIFIED from help and `lc01-step7.txt`]:

- It returns at most 100 rows per page, newest first, with `--limit 1-100`. The next page is fetched with `--cursor <page.nextCursor>`.
- The envelope is `workers[]`, `counts` (per terminal state), `page.{limit, total, hasMore, nextCursor}`, `scope.{run, source}` and `_meta.runtimeId`.
- With no `--run` it is scoped to the bound Run, or to every Run when there is no binding, and `scope.source` says which (`flag`, `bound` or `all`).

**worker-show** takes exactly one `--dispatch` [CODE-VERIFIED]. Its `result` carries `dispatch`, `worker`, `projection` (16 fields), `terminal`, `observation` and `terminalResource` (`lc16-show-4.json:5-207`).

| Field | Where | What it tells a sweep | Tag |
|---|---|---|---|
| `projection.liveness.verdict` | worker-show (`lc16-show-4.json:135-139`) | `live` / `unverifiable` / `exited`; only `live` (source `agent_status`) was ever captured | values beyond `live` [UNVERIFIED], guide text |
| `projection.outcome` | `lc16:134`, `lc17-show-1.json:134`, `lc01-show-1.json:134` | `in_progress`, `failed`, `succeeded`: the Orca half of "finished" | [CODE-VERIFIED] |
| `projection.nextAction`, `attention` | `lc16:152-159`; `lc17:152-166` | Literal argv (for example `worker-release`) and categories such as `failure`, `root_completion` | [CODE-VERIFIED] |
| `projection.resource.terminalState` | `lc16:145-151`; `lc17:150` | Process accounting only; a working worker shows `retained`. Feeds safe-to-close, not the class | [CODE-VERIFIED] |
| `observation.agentWait` (also `terminal.agentWait`) | `lc16:180`, `:185` | Object = waiting on a person; `null` = looked, no wait; absent = never looked. Not inside `projection`. Null in every capture | three states [CODE-VERIFIED as help text]; non-null shape [UNVERIFIED] (GQ-36) |
| `projection.stage.activity` | `lc17:132`, `lc01:132` | Stays "working" after settlement while the pane shows an idle prompt | [CODE-CONTRADICTED] as a work signal; not used (GQ-20) |
| `projection.parent` | `lc16:115` (null) | Non-null means a WC-13 violation for review | [CODE-VERIFIED] null case |

Corrections and contradictions:

- The guide says each worker-list row carries `projection.liveness`, `attention` and `nextAction` [UNVERIFIED, guide text]. No populated row was ever captured (`lc01-step7.txt:28` is `[]`), so the row's content is unknown, and so is whether it carries `agentWait` (GQ-01). The sweep therefore relies only on the envelope and the Dispatch id, and calls worker-show once per row. Worst case that is ceil(N/100) list calls plus N show calls (`research/05-orca-row-schema.md:157`, `:165`).
- The draft classifier in scope-02 (:105-109) is superseded by `research/research-notes.md` Section C (contradiction C14). Section C sets this precedence, first match wins:
  1. Contract read first (`worker_status: blocked` means waiting on a person). Fidelity-fix condition (WC-3, `WORKER-CONTRACT.md:54-55`): rule 1 applies only when the Orca row is settled, the brief's policy line is `On a blocked gate: report blocked` (the default), or the contract is an `/sc:implement` Ruling halt (`reason` `E-HALT-QA` or `E-NO-RULING`, which is never asked whatever the policy line says, WC-3 `WORKER-CONTRACT.md:56`). A live, unsettled row whose brief says `ask the coordinator` may be asking the coordinator or re-running with the answer (the second contract replaces the blocked one), so it is not labelled waiting on a person; it falls through to the later rules (working when rule 5 matches, else could not determine) with the note "blocked contract under ask the coordinator; may be re-running". The same condition gates the contract halves of rule 4: rule 4a's blocked-contract case and rule 4b-contract's blocked case apply only when rule 1 would have applied, so a skipped contract is neither (a) nor frozen; its policy prints "could not determine" with the same note, never "not frozen" (step 1.3). Source conflict: Section C (`research-notes.md:192`, `:196`) and GQ-96 state rule 1 and 4a without this condition; the report follows WC-3 (`WORKER-CONTRACT.md:54-56`).
  2. Stalled (proved), only with positive stop proof and no `consumer_fenced` evidence.
  3. Fenced.
  4. Waiting on a person: (a) explicit question, or (b) frozen or blocked by policy, including a foreign ready Task from `task-list --ready`. A blocked contract counts under 4a or 4b-contract only when rule 1's condition holds.
  5. Working (`live`, `in_progress`, `agentWait` null).
  6. Finished (outcome settled plus a read contract, or "finished: guard refused"). A `partial` contract is finished but marked "partial: usable not yet judged": per `WORKER-CONTRACT.md:125` dependents wait until the coordinator has read `report_path` and recorded whether the deliverable is usable, and an unusable one is handled like `failed`.
  7. Could not determine (`unverifiable`, `agentWait` absent on an unsettled row, a transcript-only stop sign with no Orca proof, the 100-row cap).
- Help and guide disagree on what a null `agentWait` means. The help says "looked and found no wait"; the guide says it is "that same absence seen again". The rule follows the help for classification (null is valid for working) and the guide for stop decisions (null is never stall proof). The conflict stays open (`research/06-orca-open-questions.md` Gap 19 `:176`).
- Guide text and the inventory disagree on whether a dispatched worker may start helpers. The contract (WC-8/WC-13) governs either way (GQ-40).

Messages and peers (`research/06-orca-open-questions.md` Summary `:185-189`):

- A worker's question reaches the coordinator as a durable `run:<id>` message from a blocking `ask`.
- Every `check` is a mutation call (`message-check-handler.js:30`). `--unread` consumes and is forbidden [CODE-VERIFIED]. `--peek` is ignored by older runtimes, and a `compatibilityAck` follow-up can acknowledge messages for the caller (`:17`, `:58-71`).
- The design consequence is that Orca question enumeration is "could not determine", answered state is "could not determine", and the report header states partial message coverage (GQ-02, GQ-43, GQ-44).
- Peer (person-started) sessions do not appear in worker-list. They appear only in `worktree ps` and `reference find`. `--agent-wait` is excluded because its probe side effects are unknown (06 Gap 10).

Recorded and not verified, sent to Open Questions:

- `liveness.reason` and the six `unverifiable` reasons (GQ-15, GQ-37).
- The shape of `runtime_unavailable` (GQ-16).
- Whether heartbeat age feeds liveness (GQ-17).
- `page.hasMore` past 100 rows (GQ-38).
- The `counts` keys (GQ-39).
- The cost of `--include-remote` (GQ-22).

**Evidence:** `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc16-show-4.json:5-207`, `:115`, `:128-159`, `:180`, `:185`; `lc17-show-1.json:132`, `:134`, `:150`, `:152-166`, `:182`; `lc01-show-1.json:132`, `:134`; `lc01-step7.txt:24-46` (`:28`, `:32-37`, `:38-41`); `orca-ide orchestration worker-list --help` lines 3, 19-22 and `worker-show --help` lines 3, 16 (as read in `research/05-orca-row-schema.md:14-29`); `message-check-handler.js:17`, `:30`, `:33-34`, `:58-71` (via `research/06-orca-open-questions.md:147-176`); `research/research-notes.md:188-200`.

### 2.3 Crash recovery and ccsession (`src/superclaude/skills/sc-crash-recovery/`, `src/superclaude/skills/ccsession-tag/`)

**sc-crash-recovery** (`SKILL.md`, 157 lines; `refs/investigators.md`, `refs/pipelines.md`, `refs/report-template.md`; `scripts/bootstrap_scan.sh`, 170 lines; `scripts/parse_session_log.py`, 128 lines) is a whole-project crash investigator. Pieces a sweep can copy as patterns [CODE-VERIFIED]:

- **SAFE / REVIEW labels:** `SKILL.md:91`. The skill proposes actions and never executes them (`:93-97`).
- **"What I could not determine":** a section listing the `unscanned:` markers (`SKILL.md:139-150`; template `report-template.md:127-129`). It maps onto the sweep's could-not-determine and Orca-unavailable cases.
- **Conflicts section:** the report shows both sides and does not pick one (`report-template.md:120-125`; `SKILL.md:134`).
- **On-disk progress signals:**
  - `TASK-WF-*` `progress.md` (`refs/pipelines.md:177-201`).
  - Sprint results (`:102-116`).
  - Further signals at `:52-68` and `:19`.

What does not hold [CODE-CONTRADICTED]:

| Claim or assumption | What the source shows |
|---|---|
| "Pure read-only, enforced by allowed-tools" (`SKILL.md:13`, `:155`) | `allowed-tools` at `SKILL.md:4` includes `Bash(git stash *)`, which allows `git stash push/pop/drop`. A sweep allows only `git stash list` (GQ-21) |
| Scans this host's projects | `SKILL.md:4` hardcodes `~/workspace/IronClaude/...`, and `--all` runs `find ~/workspace -maxdepth 1` (`:53`). Projects and Orca worktrees live under `~/workspaces/` and `~/workspaces/worktrees/...` (host observation: this worktree is `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`), so `--all` finds none of them. Single-project mode, the default, uses the cwd or a given path (`:27`, `:49-50`), so only `--all` (`:25`, `:36`, `:53`) and the dev-fallback allowlist entry (`:4`) are wrong here |
| `bootstrap_scan.sh` finds a project's session logs | `:31` replaces only `/`, while Claude Code replaces every non-alphanumeric character, so a path with `.` or `_` points at the wrong log dir |
| `bootstrap_scan.sh` reads git state for worktrees | `:73` tests `.git` as a directory; in a git worktree `.git` is a file, so every Orca worktree reports `is_repo` false |
| `bootstrap_scan.sh` emits valid JSON | `:136` escapes only partly, so a path with `"` or `\` gives malformed JSON |

`--since` defaults to 72 h (`SKILL.md:26`), which differs from #339's 6 h default. `parse_session_log.py` reads the whole transcript into memory (`:31-40`). It can show the latest assistant turn but cannot prove that turn is final, because it keeps no end-of-turn or process-exit signal (`:45-55`, `:85-102`). So a missing `worker_done` in that turn is never stall proof on its own: WC-10 accepts only Orca's stall proofs (`WORKER-CONTRACT.md:45`), so rule 2 needs Orca liveness `exited` or an Orca-observed exit, and a transcript-only stop sign gives could not determine with a note (Phase 6 QA narrowing of Section C rule 2). **This departs from analysis F3** (`.dev/issues/339/analysis/analyze-worker-contract.md:34`), which allows a stop recommendation on `exited` liveness "or a final turn without `worker_done`". The report keeps the `exited` half and narrows the second: a turn counts as final only when Orca observed the exit, because the transcript carries no end-of-turn or process-exit signal (`parse_session_log.py:45-55`, `:85-102`), so a transcript alone cannot show the turn is final, and WC-10 accepts only Orca's stall proofs (`WORKER-CONTRACT.md:45`), the same rule F3 cites.

**Rejected option A4 (extend or reuse sc-crash-recovery as the sweep).** A4 is rejected because it is [CODE-CONTRADICTED] by the rows above. The skill's tool allowance is not read-only (`SKILL.md:4`), its `--all` scan and one dev-fallback allowlist entry miss this host's projects (`SKILL.md:4`, `:53`; single-project mode uses the cwd, `:49-50`), and its scanner fails on Orca worktrees and some paths (`bootstrap_scan.sh:31`, `:73`, `:136`) (`research/research-notes.md:160`; `gaps-and-questions.md` GQ-19). Nothing in this synthesis builds on A4. Whether a later phase fixes `bootstrap_scan.sh` or writes a new scanner is an open plan decision (GQ-19).

**Tension between sources: reject A4, or reuse crash-recovery's signals.** `BUILD-REQUEST.md:21` says extending `sc-crash-recovery` as the sweep's home (A4) is CODE-CONTRADICTED and nothing may build on it. Analysis F11 (`.dev/issues/339/analysis/analyze-worker-contract.md:42`) and the issue summary (`.dev/issues/339/issue-summary.md:21`) ask the sweep to reuse crash-recovery's signals rather than re-implement them. Rejecting A4 rejects the skill as the sweep's home, not its signals, so the report reuses the **signals** and re-implements only the **code**: step 1.4 reads the same on-disk signals the skill names (`progress.md` ledgers, sprint results, `.roadmap-state.json`, MDTM `status:`, session transcripts; `refs/pipelines.md:19`, `:52-68`, `:102-116`, `:177-201`). Reusing the skill's code is not possible as it stands: `bootstrap_scan.sh` mis-encodes project paths (`:31`), skips every Orca worktree because it tests `.git` as a directory (`:73`) and emits malformed JSON for some paths (`:136`); `parse_session_log.py` reads the whole transcript (`:31-40`) and keeps no end-of-turn signal (`:45-55`), where the sweep needs a tail read; and the skill's tool allowance is not read-only (`SKILL.md:4`).

**ccsession** (`src/superclaude/skills/ccsession-tag/ccsession`, 1975 lines) [CODE-VERIFIED]:

- **Session store:** labelled sessions live at `~/.claude/projects/<name_key>/topics/<name>.txt`, each holding a session uuid (`:144`, `:175-222`).
- **Transcript lookup:** by uuid (`:1408-1411`).
- **`--list` output:** human-readable only, with no JSON form (`:1482-1580`).
- **`--list` is not read-only [CODE-CONTRADICTED]:** it first calls `ensure_names_migrated` (`:1787-1788`). That function moves and writes files when the marker `.ccsession-names-by-repo` (`:224`) is missing (`:285-287`). A read-only sweep reads `topics/*.txt` directly and never calls `ccsession --list` (GQ-21). **This overrides three sources:** the seed brief names `ccsession --list` as an existing pattern and says non-Orca sessions appear in the report "from ccsession and session logs" (`seed-brief.md:33`, `:75`), the issue summary names it as a sweep input (`.dev/issues/339/issue-summary.md:22`), and the analysis puts it in the Phase 1 sweep's inputs (`analyze-worker-contract.md:60`). The exclusion wins because the command writes (`ensure_names_migrated`, scope-02 `:165`) and Phase 1 is read-only (`seed-brief.md:53`). The sources' intent is kept: labelled sessions come from the `topics/*.txt` session store directly (`:144`, `:175-222`).
- **Orca join data:** `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/` (`:564`) holds one file per Orca pane key (`:` replaced by `+`). Each file has 3 lines: the Claude session id, the launch folder and the Orca terminal handle (`:558-605`). The pane-key to transcript join is verified for one worker, lc16 (GQ-18). Person-started sessions are in the Phase 1 report (`BUILD-REQUEST.md:12`; `seed-brief.md:66`, `:75`; analysis F2; Section 3.1 G6); they are read from `topics/*.txt` and transcripts, and the orca-tabs join is the route for Orca panes.

**Return contracts a sweep reads** [CODE-VERIFIED as contract text]:

- **Worker contract:** `<report-dir>/return-contract.yaml` (WC-4; shape at `WORKER-CONTRACT.md:32`). It holds `worker_status: succeeded | partial | failed | blocked`, plus `blocked_question` when blocked. WC-5 (`:58`) maps both `blocked` and `failed` to Orca outcome `failed`, so the sweep must read the YAML first.
- **Workflow package contract:** `.dev/tasks/to-do/<id>/return-contract.yaml` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3-19`). Under `--unattended` its worker variant has no `blocked` value (`:45-56`).

**Evidence:** `src/superclaude/skills/sc-crash-recovery/SKILL.md:4`, `:13`, `:25-27`, `:36`, `:49-50`, `:53`, `:91`, `:93-97`, `:134`, `:139-150`, `:155`; `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:120-125`, `:127-129`; `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:19`, `:52-68`, `:102-116`, `:177-201`; `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:31`, `:73`, `:136`; `src/superclaude/skills/sc-crash-recovery/scripts/parse_session_log.py:31-40`, `:45-55`, `:85-102`; `src/superclaude/skills/ccsession-tag/ccsession:144`, `:175-222`, `:224`, `:285-287`, `:558-605`, `:564`, `:1408-1411`, `:1482-1580`, `:1787-1788`; `src/superclaude/core/WORKER-CONTRACT.md:32`, `:58`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3-19`, `:45-56` (all via `research/scope-02-orca-recovery.md:18-26`, `:126-192`).

### 2.4 CLI and command patterns (`src/superclaude/cli/`, `src/superclaude/commands/`)

**CLI structure** [CODE-VERIFIED]:

- `src/superclaude/cli/main.py:18-26` defines the root Click group. Subcommand groups are registered by deferred import at `:519-561`, and the `__main__` guard is at `:564-565`.
- The registered groups are sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval, swarm, recommend, init-lite and reflect. No `sweep` group exists.
- Package `__init__` files follow two styles:
  - Lazy `__getattr__` in `src/superclaude/cli/recommend/__init__.py:12-20`, which scope-03 recommends.
  - Eager imports in `src/superclaude/cli/reflect/__init__.py:17-30`.
  - Which style the Orca client uses is an open plan decision (GQ-23).
- The house split is in `reflect`:
  - A pure module, `src/superclaude/cli/reflect/contract.py:7`, `:397`.
  - `config.py` routes all of its git calls through one `_git` seam, `src/superclaude/cli/reflect/config.py:64-78` (used at `:104`, `:127-137`, `:181-222`, `:312`). The package as a whole has no single seam: `commands.py:570-577` calls `subprocess.run` directly (tmux new/attach/kill-session), and `runner.py` starts its child through `ClaudeProcess` (`runner.py:31`), which the tests stub separately.
  - The Click layer, `src/superclaude/cli/reflect/commands.py`.
  - A sweep copies this split with one `_orca(*args)` seam (GQ-27).
- Click option conventions follow `src/superclaude/cli/recommend/commands.py:34-48`, `:73-75`.
- [CODE-CONTRADICTED] The recommend docstring says the command can run with `python -m`, but the package has no `__main__.py`.

**Test patterns** [CODE-VERIFIED]:

- CliRunner registration tests (`tests/recommend/test_cli_registration.py:1-39`).
- A `patch_git` fixture (`tests/cli/reflect/conftest.py:58-80`).
- A read-only proof test (`tests/cli/reflect/test_contract_status_cli.py:44-66`).
- For the sweep, a second test (B-13) patches the `_orca` seam and checks every argv against an allowlist.

**Orca argv allowlist for the sweep (after the NB-4 fix, `research/scope-03-cli-patterns.md:99`; `qa/qa-nb4-fix-log.md`):**

| Allowed by default | Gated (separate argv, off by default) | Forbidden |
|---|---|---|
| `orchestration worker-list`, `worker-show`, `worker-read` | `check --peek`, `check --all` | Plain `check` (no `check` call at all by default) |
| `worktree ps` without `--agent-wait` | | `inbox`. The CLI side is a plain read, but whether it marks messages read is [UNVERIFIED] (`07-gate-gap-fill.md:92`; `06` Gap 4 `:161`) |
| `orchestration task-list` (with `--ready`, `--run <id>`; `task-handlers.js:32-44`) | | `reply`, `ask`, `send` |
| `orchestration run-list` (`run-handlers.js:35-48`), `orchestration run-current` (`run-handlers.js:28-34`) | | `--ack`, `--wait`, `--unread` |
| `orchestration gate-list` (`gate-handlers.js:26-37`) | | `worktree ps --agent-wait`, and any verb not on the allowlist |

The four NB-4 verbs are plain reads on the CLI side (`research/07-gate-gap-fill.md` B `:41-44`). They supply:

- the "frozen or blocked by policy" kind of waiting on a person, via a foreign ready Task from `task-list --ready` (`research/research-notes.md:197`);
- the Run ids and the Owner column (`research/scope-04-409-layout.md:339`);
- the Approval candidate (`:345`). The gate-list to Approval mapping is still [UNVERIFIED] (GQ-34).

**Scope of "read-only".** The allowlist and the read-only tests prove read-only at the argv level and on the local filesystem only. A handler read proves what the CLI sends to the Orca runtime, not what the runtime does with it (`research/07-gate-gap-fill.md:8`). No capture shows that `worker-list`, `worker-show`, `worker-read --source transcript` or `worktree ps` leave runtime state unchanged (no read marker, no cursor advance) [UNVERIFIED]. Step 1.0a probes this once on a throwaway Run before the build (S9 row 79).

GQ-03 (NB-4) is resolved. The summary counts at `gaps-and-questions.md:125` read "Open: 75. Resolved: 25" after the NB-4 fix, and state "Open blocking QA finding: none". scope-03 still writes `worker-list`, `worker-show` and `worker-read` without the `orchestration` prefix that C13 requires. Callers must spell the full `orca-ide orchestration <verb>` (`qa/qa-nb4-fix-log.md:41`).

**Command and skill patterns** [CODE-VERIFIED]:

- Frontmatter follows `src/superclaude/commands/issue.md:1-9`.
- The activation block follows `src/superclaude/commands/reflect.md:146-151`. That block is parsed by `tests/recommend/test_routing_refresh.py:38-40` and `:472`.
- `allowed-tools` is set in 14 of 46 command files.
- Naming is `sweep.md` plus the skill `sc-sweep-protocol`.
- The skill calls `superclaude sweep` on PATH first, with `uv run superclaude sweep` as the dev-checkout fallback, and a static test pins the order (B-19). Whether this works under pipx is [UNVERIFIED] (GQ-25), and so is how `allowed-tools` patterns combine (GQ-26).
- The design-doc format follows `docs/designs/sc-issue-command.md` (20 headings).

**Registries and suite-wide checks a new command must pass:**

- `src/superclaude/cli/main.py` registration.
- `_POST_REFRESH_ADDITIONS` (`tests/recommend/test_routing_refresh.py:33`; asserted at `:647-648`).
- HOW-WE-WORK `:318-337`, `_OTHER_COMMANDS` and the plugin byte copy (2.1).
- `docs/user-guide/commands.md:105`, `:115`.
- `make lint` lint-architecture checks 1, 2, 3/4, 6, 8, 9 and 11 (`Makefile:362-489`).
- Suite scans: `tests/skills/test_model_alias_policy.py:81-100`, `tests/commands/test_graph_command.py:219-225`, the write-verb audit and `_check_no_unattended_sections` (`:464-472`).
- Ruff is pinned at 0.15.20 (`pyproject.toml:54`).
- Whether a test pins the UTILITIES table is [UNVERIFIED] (GQ-28).
- Whether "other commands" or the excluded set governs HOW-WE-WORK routing is open (GQ-24).

**Precedents the options in Section 6 rest on** [CODE-VERIFIED, re-read in the Phase 6 QA fix pass]:

| Precedent | Evidence | Used by |
|---|---|---|
| The sc-issue design chose no CLI: "No CLI (`src/superclaude/cli/`) code: the only program is the skill's own script." | `docs/designs/sc-issue-command.md:384` | A1's departure (Con, trade-off), A3's premise |
| sc-issue's scripts live in the skill (`scripts/clickup_claim.py`, `scripts/origin_repo.py`) and are tested directly by `tests/skills/test_clickup_claim.py` and `test_issue_repo_resolution.py` | `docs/designs/sc-issue-command.md:355-363`, `:395-396` | A3 (skill-local script layout and tests) |
| A skill that calls the package CLI lists it in `allowed-tools`: `Bash(uv run superclaude swarm *)` | `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md:7` | A1, A2 (allowed-tools form) |
| The reflect seam raises and its caller maps the failure: `_git(cwd: Path, *args: str) -> str` raises `subprocess.SubprocessError` or `OSError` (`check=True`, `timeout=10`); `_resolve_base` catches both and raises `ValueError("base-unresolved: ...")` | `src/superclaude/cli/reflect/config.py:64-78`, `:103-109` | A1 probe seam (step 1.4) |
| Crash recovery flags a pipeline that is still running (a process holding `.sprint-exitcode` open, or a recent execution-log entry) and asks the person to confirm before resuming | `src/superclaude/skills/sc-crash-recovery/SKILL.md:137` | A1 Reuse (the running-pipeline guard the sweep report keeps) |
| Option pros and cons as researched: A1 is deterministic and mock-testable (`seed-brief.md:62,68`); A2 breaks `:68`; a skill-local script cannot import package code and needs a path shim | `research/research-notes.md:157-159` | A1, A2, A3 |

Tally from scope-03: 58 VERIFIED, 3 CONTRADICTED, 3 UNVERIFIED.

**Evidence:** `src/superclaude/cli/main.py:18-26`, `:519-561`, `:564-565`; `src/superclaude/cli/recommend/__init__.py:12-20`; `src/superclaude/cli/reflect/__init__.py:17-30`; `src/superclaude/cli/reflect/contract.py:7`, `:397`; `src/superclaude/cli/reflect/config.py:64-78`, `:104`, `:127-137`; `src/superclaude/cli/reflect/commands.py:570-577`; `src/superclaude/cli/reflect/runner.py:31`; `src/superclaude/cli/recommend/commands.py:34-48`, `:73-75`; `tests/recommend/test_cli_registration.py:1-39`; `tests/cli/reflect/conftest.py:58-80`; `tests/cli/reflect/test_contract_status_cli.py:44-66`; `src/superclaude/commands/issue.md:1-9`; `src/superclaude/commands/reflect.md:146-151`; `tests/recommend/test_routing_refresh.py:33`, `:38-40`, `:472`, `:647-648`; `Makefile:362-489`; `pyproject.toml:54`; `research/scope-03-cli-patterns.md:99`; `qa/qa-nb4-fix-log.md:12-18`, `:39-41`; precedents block: `docs/designs/sc-issue-command.md:355-363`, `:384`, `:395-396`; `src/superclaude/cli/reflect/config.py:103-109`; `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md:7`; `src/superclaude/skills/sc-crash-recovery/SKILL.md:137`; `research/research-notes.md:157-159`.

### 2.5 The #409 observer designs and the layout this research selects (`495eb96d:.dev/design/orca-observer-20261106/`)

The #409 package (PKG below) lives only on the unmerged branch `docs/409-orca-dashboard-designs` at commit `495eb96d`, and it is read with `git show`. **#409 has no single layout.** It offers 20 alternative compositions in two sets (`PKG/README.md:13-15`; `PKG/concepts.md:3-15`, `:19-31`). Its ranking is labelled "Provisional design judgment, not user approval or measured comprehension" (`PKG/concepts.md:43`), and its plan says "User chooses the visual direction before any production integration" (`PKG/PLAN.md:62`; also `PKG/README.md:48`); no direction has been chosen. #409's own picks are Signal Bridge, Proof Gate and Fleet Quilt (first set) and Leverage Board, Collision Lens and Revision Drift for hands-on supervision (`PKG/concepts.md:45-49`). Attention Ledger and Shift Brief are not among them: they are a selection made by this research's upstream enrichment as "the closest matches to the #339 periodic report" (`.dev/brainstorms/20261107-073115-orchestrator-mode/enrichment/codebase-context.md:55`). Wherever this report says "the #409 layout", it means that research selection (header + Attention Ledger + Shift Brief), not a #409 decision; choosing it is an owner decision that #409 leaves to the user. Which version a sweep follows if it changes before merge is open (GQ-35). Everything in PKG about field names, IDs and sources is marked proposed only (`PKG/integration-gaps.md:20`, `:9-16`; `PKG/DESIGN-CONTRACT.md:11`). The facts below describe what the design draws [CODE-VERIFIED against the PKG files], not a running system.

| Element | What PKG shows | Source | Tag |
|---|---|---|---|
| Header | A title plus "SYNTHETIC · READ ONLY". The line "`<owners>` owners / `<sessions>` sessions / `<mapped>` mapped trees". A clock line with message coverage, worker age and check age | `PKG/canvas.py:73-77` | [CODE-VERIFIED]; the clock is hardcoded (`:77`) and the fixture `scope` object (`PKG/fixtures.py:21`) is never printed, although the contract says the header prints scope (GQ-32) |
| Footer | Disclaimer line | `PKG/canvas.py:81` | [CODE-VERIFIED] |
| Attention Ledger | Each question shows age, question, requester and owner (shown separately, "`<requester>` requests / `<owner>`", `:48`), and affected IDs. A "SEEN IS NOT RESOLVED" count panel follows, with seven retained-context facts that keep acting owner and requesting orchestrator apart (`:53`). The narrow view adds "Questions stay until explicit resolution." and "No reply observed is not delivery failure." (`:43`). The stated failure mode is "seen/delivered is not answered" (`PKG/concepts.md:23`) | `PKG/layouts/agent_focus.py:44-53` | [CODE-VERIFIED]. The docs call it "age-ranked" (`PKG/concepts.md:23`), but the code has no sort: [CODE-CONTRADICTED, partial] (`agent_focus.py:46`; tie-break GQ-29) |
| Shift Brief | A count with a "not an all-clear" coverage line, then per-request blocks (id / age / owner, question, affects or evidence), then failed / stale / frozen counts and an "Inspection only" line | `PKG/layouts/agent_focus.py:156-169` | [CODE-VERIFIED] |
| Data dictionary | Entities; ten independent state dimensions, each a closed value set (lifecycle, phase, health, approval, freshness, result, admission, evidence, policy, tests/review); a missing-evidence rule | `PKG/data-dictionary.md:7-15`, `:19-28`, `:50` | [CODE-VERIFIED] |
| Request definition | "Explicit synthetic human question, not inferred from any blocked status" | `PKG/data-dictionary.md:12` | [CODE-VERIFIED]; this is the basis for splitting waiting on a person into kinds (a) and (b) |
| Required semantics | Ten rules: (1) all fixture values synthetic; (2) worker result is not admission; (3) dirty != dangerous, stale != failed, overlap != conflict, partial cost subtotal != total spend, tokens != progress; (4) evidence flags use current revision equality; (5) "Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only."; (6) handle messages coverage unavailable vs partial; (7) header prints scope/freshness; (8) narrow views keep the first human decision, owner and affected scope/freshness; (9) "Show omission counts when limited"; (10) the data model is a proposed fixture schema, never the Orca API schema | `PKG/DESIGN-CONTRACT.md:11` | [CODE-VERIFIED]. Rule 5 conflicts with Phase 1 recommendations; see the [CONTRADICTION] note below the table |
| Omission rule | "`shown/total`" count when a list is limited | `listbox()` prints "`shown/total` lines shown" (`PKG/layouts/agent_focus.py:17`), and every listbox, wide or narrow, uses it; wide Outcome Ledger prints "`.../N` shown" (`:114`) and wide Revision Drift "`... mismatches shown`" (`:127`) | Only the wide Attention Ledger question loop and the Shift Brief request loop print no count (`:46-50`, `:164-167`), and neither truncates: they list every request. So the [CODE-CONTRADICTED] holds only in a weaker form: those two lists are unbounded, not limited without a count (GQ-33) |
| Message coverage | Complete non-consuming message enumeration is "not established" | `PKG/integration-gaps.md:11` | Still true for today's CLI (`research/06-orca-open-questions.md:183`) |

Neither of the two selected views lists every session and worktree. They render requests and counts only (`agent_focus.py:41-53`, `:156-169`). The #409 package as a whole does have inventory views: Outcome Ledger prints one row per reported session (SESSION / LIFECYCLE / REPORT / PACKET / ADMISSION, with "`shown/total`", `agent_focus.py:105-114`); Fleet Quilt shows every session (`PKG/concepts.md:7`); Worktree Atlas (`:9`) and Collision Lens (`:26`; branch / head / base / dirty / policy cards, `agent_focus.py:100-102`) are worktree views. So the sweep's inventory table, with Class as a derived column and one source field per column, is DERIVED in `research/scope-04-409-layout.md:268-351`; it is not inherited from the two selected views, and Outcome Ledger is its nearest in-package precedent.

[CONTRADICTION, sources disagree; owner decision] DESIGN-CONTRACT rule 5 says "Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only." (`PKG/DESIGN-CONTRACT.md:11`), but the seed brief asks for a report with "a recommended next action" for every session (`.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:66`) while also saying the report "follows the #409 layout" (`:67`). The Phase 1 skeleton in 3.1 follows the seed brief: it prints recommendations (safe-to-close REVIEW, the "new Task" resume recommendation, WC-14 item 8, the optional "what to check next"), which rule 5 would forbid. This report does not resolve the conflict; it is an owner decision (Section 9.4). It is a proposal for the plan, not current state. Its Approval column reads `gate-list` and its Owner column reads `run-list`, both allowed after NB-4 (2.4); the Approval value mapping stays [UNVERIFIED] (GQ-34). Open layout decisions: what counts as closure evidence (GQ-30), whether to print every source's coverage (GQ-31), the scope line (GQ-32) and the omission bound for a static file (GQ-33). Tally from scope-04: 3 CONTRADICTED, 0 UNVERIFIED.

**Evidence:** `495eb96d:.dev/design/orca-observer-20261106/canvas.py:73-77`, `:81`; `.../layouts/agent_focus.py:17`, `:41-53`, `:46-50`, `:100-102`, `:105-114`, `:127`, `:156-169`; `.../concepts.md:7`, `:9`, `:23`, `:26`, `:43-49`; `.../PLAN.md:62`; `.../README.md:13-15`, `:48` (these and the ten-rule list re-read with `git show` in the fidelity fix cycle); `.../data-dictionary.md:7-15`, `:12`, `:19-28`, `:50`; `.../DESIGN-CONTRACT.md:11`; `.../integration-gaps.md:9-16`, `:11`, `:20`; `.../fixtures.py:21` (all via `research/scope-04-409-layout.md:330-373`).

### 2.6 Current State Summary

The diagram shows only [CODE-VERIFIED] sources and the reads already allowed. [UNVERIFIED] and [CODE-CONTRADICTED] items appear only in the table below it.

```
  coordinator session (WORKER-CONTRACT.md:64; no poll / re-arm / sweep rule: G1-G3)
        |
        |  reads only (allowlist after NB-4, scope-03:99)
        v
  +---------------------------+     +------------------------------+     +---------------------------+
  | Orca CLI 1.4.245          |     | on-disk contracts            |     | ccsession store           |
  | orchestration run-list /  |     | <report-dir>/                |     | ~/.claude/projects/<key>/ |
  |   run-current  -> Run ids |     |   return-contract.yaml       |     |   topics/*.txt -> uuid    |
  | worker-list (100/page,    |     |   worker_status, blocked_q.  |     | orca-tabs/<pane key>      |
  |   envelope only)          |     |   (WC-4 :32, WC-5 :58)       |     |   -> session id, folder,  |
  | worker-show x N           |     | .dev/tasks/*/*/progress.md   |     |   terminal handle         |
  |   outcome, liveness,      |     |   (pipelines.md:177-201)     |     |   (ccsession:558-605)     |
  |   agentWait, nextAction   |     +------------------------------+     +---------------------------+
  | task-list --ready,        |                    |                                   |
  |   gate-list               |                    |                                   |
  +---------------------------+                    |                                   |
        |                                          |                                   |
        +--------------------+---------------------+-----------------------------------+
                             v
         research-notes.md Section C precedence (contract first; stall needs proof;
         absence -> could not determine)  -->  class + safe-to-close dimension
                             v
         static report: header / Attention Ledger / Shift Brief (research selection
         from #409's 20 designs, 495eb96d, unmerged; #409 direction not chosen)
```

| Area | Exists today | Missing or blocked | Tag of the key fact |
|---|---|---|---|
| Worker contract | WC-2..WC-13 and the coordinator section (`WORKER-CONTRACT.md:64-164`), pinned by `tests/skills/test_worker_contract.py` | No poll, re-arm, sweep or tell-the-person rule; WC-14 is free (G1-G5, GQ-04 to GQ-08, GQ-11) | [CODE-VERIFIED] |
| Orca reads | Paged worker-list envelope; worker-show fields; run-list, run-current, task-list and gate-list allowed (NB-4) | Populated row shape (GQ-01); `unverifiable` and `exited` never captured (GQ-37); non-null `agentWait` shape (GQ-36); no non-consuming question read (GQ-02); `inbox` forbidden (GQ-46) | envelope and fields [CODE-VERIFIED]; row content [UNVERIFIED] |
| Work signals | `outcome`, `liveness`, `agentWait`, contract `worker_status` | `stage.activity` unusable; `terminalState` is not a class input | `activity` [CODE-CONTRADICTED] |
| Crash recovery | SAFE/REVIEW labels, a "could not determine" section, pipeline signals | Not read-only (`git stash *`), wrong `~/workspace` path in `--all` mode and one allowlist entry, scanner bugs at `bootstrap_scan.sh:31`, `:73`, `:136`; option A4 rejected (GQ-19, GQ-21) | [CODE-CONTRADICTED] |
| ccsession | `topics/*.txt` store; orca-tabs pane-to-session join (verified for lc16) | `--list` writes through migration, so it is excluded; peer sessions are reported, observed and never messaged (GQ-09 settled by `BUILD-REQUEST.md:12`, `seed-brief.md:66`, `:75`, analysis F2; Section 3.1 G6) | [CODE-VERIFIED] |
| CLI and commands | Click root plus deferred groups; the reflect model / contract / seam / commands split; read-only test patterns; registry list | No `sweep` group, command or skill; lazy or eager start (GQ-23); behaviour under pipx (GQ-25) | [CODE-VERIFIED] |
| #409 layout | 20 alternative designs, no direction chosen (`PKG/PLAN.md:62`); this research selected header, Attention Ledger and Shift Brief (#409's own picks differ, `PKG/concepts.md:45-49`); ten dimensions, ten semantics rules; Outcome Ledger is the in-package per-session inventory precedent (`agent_focus.py:105-114`) | Unmerged; no sort; the selected views list no full inventory; their two request lists print no omission count but are unbounded; rule 5 (no actions, navigation only) conflicts with the Phase 1 recommendations (GQ-29 to GQ-35) | [CODE-VERIFIED] with 3 [CODE-CONTRADICTED] |

Excluded from Section 2 on purpose:

- Guide-only Orca statements, which are sent to Open Questions under the GQ IDs above:
  - the six `unverifiable` reason codes;
  - `liveness.reason`;
  - the worker-show verdict outranking the row;
  - remote rows reading `unverifiable` without `--include-remote`.
- The derived #409 inventory skeleton (a plan input, `research/scope-04-409-layout.md:268-351`).
- The `ccsession` and `bootstrap_scan.sh` reuse judgements, which are [UNVERIFIED] as judgements (`research/scope-02-orca-recovery.md:149`, `:157`).

**Evidence:** as cited in 2.1 to 2.5; `gaps-and-questions.md:22-70` (GQ-01 to GQ-47).


---

## 3. Target State

### 3.1 Desired behavior

- **One read-only, coordinator-only command.** "Read-only" means argv-level and local-filesystem read-only: no Orca call outside the allowlist and no local write except the report. Whether the allowlisted Orca read verbs mark state in the Orca runtime is [UNVERIFIED] (`07-gate-gap-fill.md:8`); step 1.0a probes it (S9 row 79). `/sc:sweep` is the command file `src/superclaude/commands/sweep.md` (`name: sweep`), backed by the skill `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (`name: sc:sweep-protocol`) and a Python CLI group `superclaude sweep` (option A1). Source: `research-notes.md:157`; naming per `scope-03:129`. Today neither `commands/sweep.md` nor any `sweep`/`close` command exists [CODE-VERIFIED] (`scope-01:74`, `scope-03:129`).
- **How the skill calls the CLI.** It calls the installed entry point `superclaude sweep ...` on PATH first. Inside a dev checkout, when that PATH call fails with "command not found", it falls back to `uv run superclaude sweep ...` (detection rule: the failure of the PATH call itself, so no separate `command -v` call and no extra `allowed-tools` entry is needed). `allowed-tools` lists both `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)` in the space form (B-19, NB-3; `scope-03:208-209`). Precedents: `sc-reflect-protocol/SKILL.md:63-64` shows only the bare `superclaude reflect ...` form [CODE-VERIFIED for the bare form]; `sc-swarm-wizard-protocol/SKILL.md:7` shows the space-form `Bash(uv run superclaude swarm *)` pattern [CODE-VERIFIED]. The PATH-first-then-`uv run` fallback itself has no precedent in either file: it is a new design (B-19).
- **Code split.** A pure classifier module with no subprocess calls, plus one subprocess-owning module whose Orca calls all go through a single `_orca(*args)` seam modelled on `reflect/config.py:64-78`. Precedent: `reflect/contract.py:7` and `scope-03:210` [CODE-VERIFIED for the precedent].
- **Data sources.** Only the sources below, all read-only (`research-notes.md` Section B; `scope-03:99` after NB-4):

| Source | Feeds | Read form |
|---|---|---|
| `orca-ide orchestration worker-list --json --run <id>`, paged on `page.nextCursor` (max 100 per page). `--include-remote` is off by default until its cost is measured (GQ-22); without it remote rows read `unverifiable` (`05:163`) and classify as could not determine | Dispatch ids and the envelope only (G-A) | plain read |
| `orca-ide orchestration worker-show --dispatch <id> --json` (one call per row) | `projection.{outcome, liveness, resource.terminalState, nextAction}`, `observation.agentWait`, `terminal.worktreePath`, `parent` | plain read; `lc16-show-4.json:127-185` [CODE-VERIFIED] |
| `orca-ide orchestration worker-read --source transcript` | latest turn; a note only, never stall proof (WC-10 accepts only Orca's proofs) | plain read |
| `orca-ide orchestration task-list --ready` / `--run <id>` | waiting on a person, kind (b): a foreign ready Task | plain read, `task-handlers.js:32-44` [CODE-VERIFIED] |
| `orca-ide orchestration run-list`, `run-current` | Run ids, Owner column | plain read, `run-handlers.js:28-48` [CODE-VERIFIED] |
| `orca-ide orchestration gate-list` | Approval candidate (the value mapping is [UNVERIFIED] -> Open Questions, GQ-34) | plain read, `gate-handlers.js:26-37` [CODE-VERIFIED] |
| `worktree ps` **without** `--agent-wait` | peer and person-started sessions | plain read |
| `<report-dir>/return-contract.yaml` (WC-4) | `worker_status`, `blocked_question`, `report_path` | file read |
| `.dev/tasks/{to-do,done}/*/progress.md`, sprint `results/`, `.roadmap-state.json`, MDTM frontmatter | unfinished ledgers (refusal condition 4) | file read |
| `git -C <worktree>` limited to status, log, branch and rev-parse | the five refusal conditions at `WORKER-CONTRACT.md:108`, plus unpushed commits and unsaved `.dev/tasks/` content (Section 3.1) | read-only git |
| `~/.local/state/ccsession/orca-tabs/<tabId>+<leafId>`, `~/.claude/projects/<key>/topics/*.txt`, transcript `*.jsonl` (read by tailing) | pane-key to transcript join; idle for person-started sessions | file read; join [CODE-VERIFIED] for lc16 only (C12) |

- **Ownership and coverage limits of these sources** (steps 1.3, 1.4):
  - **Co-location is not ownership.** "Workspace co-location alone is not ownership." (`PKG/integration-gaps.md:12`, `scope-04:222`) [CODE-VERIFIED]. The sweep maps a session to a worktree by path for the Worktree column only; sharing a worktree path never makes a session the owner of that worktree, its branch or its packages, and never credits it with another session's Task.
  - **Peer attribution.** `reference find` "`linked: true` requires recorded reference/session evidence; `linked: false` means ownership is unknown. ... never infer ownership merely from workspace membership." (`[CLI]:161`, `06-orca-open-questions.md:99`) [CODE-VERIFIED]. "Ownership of a peer row is unknown unless `linked: true`; the sweep must not attribute a peer session to a Task or worker by workspace membership." (`06:110`). A peer row without `linked: true` prints Owner "unknown".
  - **`worktree ps` coverage.** Usage is "orca worktree ps [--limit <n>] [--agent-wait] [--json]", and "A host named under `not covered` may still have workspaces; an empty answer for it is not evidence that it has none." (`[H:worktree-ps]:3`, `:16-17`, `06:97`) [CODE-VERIFIED]. "`worktree ps` is paged by a shared `--limit` cap and can list hosts as `not covered`; the sweep must report uncovered hosts as "could not determine", never as "no sessions"." (`06:109`). A page cut by the `--limit` cap under-reports, so the peer count prints as "at least <N>", like the 100-row rule under Report rules (plan decision, new design; step 1.4).

- **Classification.** Each session gets exactly one class, decided by the precedence in `research-notes.md` Section C (`:190-202`); the first rule that matches wins:

```
 per session
   |
   1 contract read first -- worker_status: blocked, and the row is
     settled, the brief says "report blocked", or it is a
     Ruling halt (WC-3 :56) -----------------------------------> waiting on a person (a)
     (live row + "ask the coordinator": may be re-running, WC-3
      :54; falls through to 5 or 7 with a note; policy could
      not determine)
   2 Orca liveness exited / Orca-observed exit, no worker_done,
     no consumer_fenced evidence ------------------------------> stalled (proved)
     (a transcript final turn without Orca proof is a note only;
      departs from analysis F3, analyze-worker-contract.md:34, see 2.3)
   3 consumer_fenced evidence (WC-12) -------------------------> fenced
   4 non-null agentWait | frozen plan | Ruling halt |
     foreign ready Task (task-list --ready) -------------------> waiting on a person (a)/(b)
     (a blocked contract counts here only when rule 1's
      condition holds)
   5 live + in_progress + agentWait null ----------------------> working
   6 settled + contract read (succeeded|partial|failed),
     or a "guard refused:" body --------------------------------> finished
     (partial: "usable not yet judged", WORKER-CONTRACT.md:125)
   7 everything else (unverifiable, agentWait absent, stale,
     Orca down, late heartbeat only, transcript-only stop sign,
     row truncated at 100) -------------------------------------> could not determine
   person-started session, no Task, no activity in window ----> idle
```

| Class | Rule | Maps the issue's term | Never derived from |
|---|---|---|---|
| waiting on a person | 1 or 4: (a) explicit question, or (b) frozen or blocked by policy | needs-person | a pending `ask` (no read path, G-B) |
| working | 5 | (healthy) | `stage.activity` [CODE-CONTRADICTED] |
| stalled (proved) | 2: positive stop proof only | stuck | a late heartbeat (WC-10), `unverifiable` |
| finished | 6: Orca settled **and** contract read | finished | Orca `outcome` alone (WC-5 shows blocked as `failed`) |
| could not determine | 7 | timed out (reported as absence, never death) | - |
| idle | person-started sessions only | idle | any Orca row |
| fenced | 3 | (none; ends without `worker_done` by design) | - |

- **Context-only Dispatches.** `worker-list --help` line 20: "Context-only Dispatches created by orchestration dispatch are included as unsupervised with terminal state retained." [CODE-VERIFIED] (`scope-02:95`; `05-orca-row-schema.md:20`); `worker-show --help` line 15: "A Dispatch created by orchestration dispatch is shown as unsupervised and reports the exact adopted terminal when its identity is still provable." [CODE-VERIFIED] (`05:28`). No such row was captured, so the JSON field that marks "unsupervised" is unknown. Such a row is never classed working or stalled (proved) from Orca liveness, since no worker is supervised; unless rule 1 or rule 6 matches on a return contract, it is could not determine with the note "context-only Dispatch (unsupervised, terminal retained)", and a `retained` terminal is never terminal releasable (plan decision, new design; read from the step 1.2 fields `OrcaObservation.unsupervised` and `terminal_state`; step 1.3, synthetic fixture in step 1.8).
- **Package states the ledger reader must recognise.** `TASK-WF-*` packages carry `progress.md` lines `T<id>: complete verdict=…`, `FINAL:` and `ARCHIVE:`; "in `to-do/` with all tasks complete = archive-blocked; `.archiving` marker = interrupted archive" (`scope-02:192`; `research-notes.md:177` lists "Unfinished ledgers, archive-blocked packages" as this source's yield). `sc-crash-recovery/refs/pipelines.md:190`: "in `to-do/` with every task complete = **archive-blocked**, not finished" [CODE-VERIFIED]; on any system other than Linux the move to `done/` is refused on purpose and the run reports archive-blocked (`src/superclaude/core/HOW-WE-WORK.md:17`). `pipelines.md:199`: "`<package>/.archiving` exists → a previous archive run was interrupted (maybe mid-move). Never delete it automatically and never infer the owner is dead from `FINAL:`/`ARCHIVE:` lines." [CODE-VERIFIED]. So an archive-blocked package is neither an unfinished ledger (refusal condition 4) nor reported as finished: it prints "archive-blocked" in the Worktrees section's Package state column. A package with an `.archiving` marker prints "interrupted archive" in that column and under Retained problems for review, is never deleted or cleared by the sweep, and makes its worktree "removable: no" (plan decision, new design; held in `WorktreeState.archive_states`, step 1.2; steps 1.3, 1.4, printed per step 1.5, tests in step 1.9).

- **Policy is a separate dimension, computed for every row.** The policy dimension ("policy: frozen / not frozen", `data-dictionary.md:27`; `research-notes.md:197`) is computed independently of the class (GQ-96: the dimensions are independent). A blocked implement contract that meets rule 1's condition (settled row, `report blocked` brief, or a Ruling halt) gets class waiting on a person (a) from rule 1 and policy frozen, and is listed under (b) too, so a frozen `/sc:implement` plan is never hidden (`WORKER-CONTRACT.md:133-136`). On a live, unsettled row under `ask the coordinator` the same contract gets no class from rules 1, 4a or 4b-contract and policy "could not determine" with the "may be re-running" note, never "not frozen": the freeze rule (`WORKER-CONTRACT.md:133`) reads the latest contract, and WC-3 (`:54`) says the re-run's contract replaces the blocked one. Rule 4b sets the class only for rows with no earlier match (the `failed` contract with a non-`E-RESUME-NEEDED` STOP code, the ledger and the ready-Task cases).
- **Contradiction: six classes or seven.** The research question lists six classes. Section C, the canonical vocabulary (C14, B-28; `research-notes.md:188`), defines seven: it adds **fenced** (rule 3). The stronger evidence is Section C, because it rests on WC-12 (`WORKER-CONTRACT.md:60`) [CODE-VERIFIED]: a fenced worker ends without `worker_done` by design, so it must be neither stalled nor finished. Target: keep fenced as its own row. If the owner holds to six classes, fenced must fold into "could not determine", never into stalled -> Open Questions.
- **Safe to close is a separate dimension, never a class.** It is a per-row REVIEW recommendation in two independent parts, printed and never executed (B-02, GQ-68; `research-notes.md:216-219`):
  - **Terminal releasable:** `resource.terminalState` is `reclaimable` and `nextAction` is `release`, and the session's result has already been read. No probe observes that the result has been read, so for a terminal Orca reports as reclaimable with next action release, Phase 1 prints "terminal releasable: could not determine (result read not observable); Orca: reclaimable, next action release", with no proxy for the read (step 1.3).
  - **Worktree removable:** all five refusal conditions at `WORKER-CONTRACT.md:108` are false (no unmerged commits, no open PR, no uncommitted changes, no unfinished `/sc:implement` ledger, no unread report), no freeze applies (`:133-136`), and two further refusal conditions the contract lacks are false:
    - **Unpushed commits:** the branch is ahead of its upstream, or has no upstream, so some commits may exist only locally. Read with `git status --branch --porcelain`, the same read-only `git status` step 1.3 already uses for uncommitted changes. The five contract conditions do not cover this (analysis F5: "a child can be merged locally into the feature branch while the feature branch is unpushed"); the seed brief tests classification on "unpushed commits" (`seed-brief.md:68`), the issue requires "nothing of value is uncommitted or unpushed" (`.dev/issues/339/issue-summary.md:10`), and analysis F5 names the gap (`.dev/issues/339/analysis/analyze-worker-contract.md:36`).
    - **`.dev/tasks/` content:** `.dev/tasks/` content is never classed as disposable (`seed-brief.md:60`; analysis F4, `analyze-worker-contract.md:35`). Any untracked or unstaged path under `.dev/tasks/` (`git status --porcelain -- .dev/tasks`) makes the worktree not removable.
    - **One package in two worktrees:** the same `:108` rule ends "It never runs one managed package in two worktrees at once." (`scope-01:64`, rule 9) [CODE-VERIFIED]; a safe-to-close check must cover at least all five conditions and is a recommendation only in Phase 1. When the ledger reader finds the same package id under two worktree roots, both worktrees print "removable: no" with this condition named, and the pair is listed under Retained problems for review (plan decision, new design; detected by a pre-pass over all worktree records before safe-to-close, `mark_shared_packages` in step 1.3, fields in step 1.2, printed per step 1.5, test in step 1.9).
  - A class is never derived from `resource.terminalState` (`research-notes.md:204`).
- **Window.** The default window is 6 h and bounds session-log and artifact **activity only**. An open Orca Task, a pending question or an unread report is listed whatever its age, so "kept until answered" holds (`research-notes.md:221`; N-41). The 72 h default belongs to crash-recovery (`sc-crash-recovery/SKILL.md:26`) and is not adopted. The owner decision is still open: GQ-61.
- **Report.** The sweep writes one dated static Markdown file on the #409 layout, pinned to commit `495eb96d` (#409 is unmerged; GQ-35). "The #409 layout" is this research's selection (header + Attention Ledger + Shift Brief, `codebase-context.md:55`) from #409's 20 alternative designs; #409 has chosen no direction ("User chooses the visual direction before any production integration", `PKG/PLAN.md:62`), and its own provisional picks are Signal Bridge / Proof Gate / Fleet Quilt and Leverage Board / Collision Lens / Revision Drift (`PKG/concepts.md:43-49`). See 2.5. The file is local only and never posted (git ownership, `WORKER-CONTRACT.md:112`, `:114`). `.dev/` is a working default, still open with the exact directory as an owner decision (GQ-10): no source fixes where a coordinator report goes. WC-11 (`:46`) is cited only for the naming rule (default output paths carry a timestamp or slug); its `.dev/` sentence is about worker report directories, not this report. The skeleton is DERIVED (`scope-04:268-308`):

```
# Orchestrator sweep: <worktree-tree root>
READ ONLY . observed <real UTC time>          <- #409 hardcodes its clock (canvas.py:73-77)
Scope: owners / sessions / mapped worktrees     <- names any filter (--run, window) and its denominator
Sources: <source> <coverage> <age> | ...      <- "Messages coverage: partial" (G-B)
## Waiting on a person: explicit questions (a)   oldest first; unknown age in a labelled group
Messages coverage: partial (Orca questions are not enumerated; sources are return contracts and worker-show agentWait). This is not an all-clear.
| ID | Age | Question | Requested by | Decision owner | Affected | Evidence |
Distinct affected sessions: <N> (set union, not a sum)
## Waiting on a person: frozen or blocked by policy (b)   no question text, ever
## Retained problems   failed / stale / policy frozen; plus stalled (proved), could not determine
## Sessions (<shown>/<total>)   10 #409 dimensions + derived Class + safe-to-close REVIEW
## Worktrees (<shown>/<total>)
## Historical sessions
Inspection only. ...                             <- footer (canvas.py:81)
```

- **Report rules** (`scope-04:316-351`; External context below):
  - Dimensions stay independent columns, and the class is one extra derived column that never overwrites a dimension.
  - Unknown values print "unknown"; missing results print "not observed".
  - The waiting list is sorted oldest first by the time since the wait began, the question's "original age" (`scope-04:87`) (#409 documents the sort but its code does not sort: C6). Rows with an unknown age go in a labelled group, never at age 0.
  - Every bounded list prints `<shown>/<total>`, as #409's listboxes, wide Outcome Ledger and wide Revision Drift already do (`agent_focus.py:17`, `:114`, `:127`); only the wide Attention Ledger and Shift Brief request lists print no count, and they are unbounded (C7, weaker form). A static file must bound them. A source truncated at 100 rows prints "at least 100 (truncated at 100), total could not determine".
  - "Answered: could not determine" and "Seen is not resolved".
  - **Explicit-questions table (a).** Columns `| ID | Age | Question | Requested by | Decision owner | Affected | Evidence |` (`scope-04:278`). Keeping ID and Evidence is a choice #409 does not dictate: its wide Attention Ledger omits them (`agent_focus.py:47-49`) and its Shift Brief carries both (`:165-167`) (`scope-04:311`, DERIVED). Cells come from the source that put the row there (B-12, `scope-04:322-330`): a `blocked` contract gives Question = the `blocked_question` text, Requested by = the worker's command and Task, Decision owner unknown, Evidence = the contract path; a non-null `agentWait` gives Question unknown (agentWait carries only its evidence type: hook, prompt-text or title, `worker-show --help` line 16), Requested by = the worker handle (`assigneeHandle`), Decision owner unknown, Evidence = the agentWait evidence type. A pending `ask` is not shown (G-B). (b) rows (Ruling halt or frozen plan: evidence = contract and ledger paths; foreign ready Task: evidence = Task id) carry no question text.
  - **Empty lists are not an all-clear.** An empty list prints "No matching records. This is not an all-clear." (`PKG/render.py:116`; empty-state test `PKG/tests/test_designs.py:58`; `scope-04:225`) [CODE-VERIFIED]. The (a) heading always carries "Messages coverage: partial (Orca questions are not enumerated; sources are return contracts and worker-show agentWait). This is not an all-clear." (`scope-04:276`), so an empty (a) list never reads as "nobody is waiting" (step 1.5, test in step 1.12).
  - **Affected counts are a set union.** "Derived affected counts use set unions." (`PKG/PLAN.md:36`, `scope-04:217`) [CODE-VERIFIED]; affected count is "Set union, not sum of overlapping requests" (`data-dictionary.md:39`, implemented `fixtures.py:102`, `:111`; `scope-04:194`); `research-notes.md:143` lists "set-union affected counts" in the #409 reuse pattern. A session reached by two sources (for example a `blocked` contract and a non-null `agentWait`) counts once. The (a) section prints "Distinct affected sessions: <N> (set union, not a sum)" (`scope-04:283`).
  - **Imported evidence is inert.** "Imported evidence is inert. Sanitize ESC/CSI/OSC, C0/C1 controls, carriage returns and bidi controls before any renderer" (`PKG/PLAN.md:38`); implemented in `sanitize()` (`PKG/canvas.py:10-17`), tested with the `injection` variant (`fixtures.py:85-86`) (`scope-04:219`) [CODE-VERIFIED]. Every untrusted string the sweep copies into the report (`blocked_question`, transcript-derived text, Orca body text, titles, paths) is sanitized before rendering, because a coordinator agent reads the file (step 1.5, test in step 1.12).
  - **Source loss changes nothing.** "Source loss does not resolve questions, fail sessions, unlock a policy freeze or authorize retries." (`PKG/integration-gaps.md:24`; `scope-04:101`, `:221`) [CODE-VERIFIED]. "Source read and the item is absent" differs from "source lost": only the first removes an item (SC-7). When a source fails or is unscanned, the items it last supported cannot be confirmed, so the affected rows print could not determine with the `unscanned:` reason; no row turns finished, failed, not frozen or retry-recommended because its source went away (plan decision, new design for how a lost source's rows print: the sweep keeps no state between runs, so it cannot list items it did not read this run; step 1.5, test in step 1.12).
  - **Counts name their scope and denominator.** "Global counts must name scope and collection completeness; a selected filter must state its denominator." (`PKG/integration-gaps.md:24`; `scope-04:67`) [CODE-VERIFIED]. The Scope line names any `--run` or window filter and the total it was taken from (for example "3 waiting of 12 sessions in run R1, window 6 h"; wording is a plan decision, new design), so a filtered count is never read as fleet-wide (step 1.5).
  - **Fan-in groups.** Fan-in (`WORKER-CONTRACT.md:156`): "wait until all N have settled. Admit an input only if its `worker_status` is `succeeded`, or `partial` judged usable as above." Max 10 inputs, merge only when "at least 2 inputs are admitted". "A sweep reporting a fan-in group should show settled/admitted counts against N." (`scope-01:68`, rule 13) [CODE-VERIFIED]. Where the sweep can tell that sessions form one fan-in group, it prints settled and admitted counts against N; "admitted" needs the coordinator's usability judgement for `partial`, which the sweep cannot see, so a `partial` input counts as "usable not yet judged" (step 1.5).
- **WC-14 coordinator-loop rule.** Add a new `### WC-14. Coordinator loop` to `src/superclaude/core/WORKER-CONTRACT.md`. Insert it after the fan-in rule ends at `:156` and before `### Worked example` at `:158`, or else after `:129` and before `:131` (`scope-01:78`) [CODE-VERIFIED insertion points]. It states:
  1. **G1:** the coordinator keeps polling until every Task it created is settled and read. Cite the owner order of 2026-11-05 (N-30). Candidate clause, [UNVERIFIED]: a coordinator turn guard, "do not end the coordinator turn while `worker-list --run <id> --terminal-state reclaimable --json` returns rows" (`orca-capabilities.md:113`, via `scope-02:94`, status UNVERIFIED). It is added to G1 only after the guard and the `--terminal-state` flag are confirmed (step 1.17); the sweep itself never passes `--terminal-state`, which is not on its allowlist (SC-2).
  2. **G2:** an expired wait is re-armed, never treated as done.
  3. **G3:** the periodic read-only sweep and its cadence.
  4. **G4:** the session classes, by reference to WC-10, WC-6 and `:108`.
  5. **G5:** one list of the "tell the person" triggers at `:125`-`:126` (including a `partial` result judged unusable, handled like `failed`), `:127`, `:129`, `:134` and `:156`, with each item kept in the report until answered. The `:156` fan-in item carries its bounds: at most 10 inputs, merge only when at least 2 are admitted, and settled/admitted counts shown against N (`scope-01:68`).
  6. **G6:** person-started sessions appear in the report, observed from transcripts and ccsession files and never messaged. The sources settle this for Phase 1: "supervise every Orca worker and ccsession" (`BUILD-REQUEST.md:12`), "lists every session and worktree" and "non-Orca sessions appear in the report from ccsession and session logs but cannot be messaged" (`seed-brief.md:66`, `:75`), and analysis F2 "Interactive peers must be observed ... not messaged" (`.dev/issues/339/analysis/analyze-worker-contract.md:33`). **Conflict named:** research-notes AMBIGUITY 8 (`research/research-notes.md:310`) offers limiting Phase 1 to Orca workers, which these sources do not allow; the report follows the sources, so GQ-09 is settled, not an open owner decision.
  7. **G7:** the report is a dated local file under `.dev/`, never posted.
  8. The sweep performs none of the actions at `:74` (stop/cancel), `:107` (merge/remove) or WC-6 (new Task); it only recommends them (`scope-01:86`).

  WC-14 should contain no runnable code spans (`_check_repo_setup_gated`, `test_worker_contract.py:446`). "WC-14" is a working name; adding WC-14 versus reusing the unused WC-1 ID is open (GQ-11).
- **Recommendations only.** These recommendations follow the seed brief's "recommended next action" (`seed-brief.md:66`) and conflict with #409 DESIGN-CONTRACT rule 5, "Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only." (`PKG/DESIGN-CONTRACT.md:11`); the conflict is an open owner decision (2.5, Section 9.4). A third source position sits against both: "The sweep must not propose stop/abandon/retry/release; those need positive proof and are coordinator decisions (`[G]:156-161`)." (`06-orca-open-questions.md:138`). Steps 1.15 and 1.17 keep the sweep recommending the `:74`, `:107` and WC-6 actions as printed text: the recommendation is a proposal only, and stopping, abandoning, retrying, releasing, merging or removing stays a coordinator decision that the coordinator makes and performs. Whether the sweep may print such proposals at all is part of the same open owner decision (Section 9.4 row 98b); if the owner adopts the `06:138` position or rule 5, the recommendation text is dropped from the rendered report and from steps 1.15 and 1.17. A resume recommendation for an Orca worker is phrased as "new Task" (WC-6, `WORKER-CONTRACT.md:70`, `:73`) and is never offered on `unverifiable`. A non-null worker-show `parent` is reported as a WC-13 violation for review (`:39`, `:61`).
- **Orca unavailable.** The sweep prints an "Orca unavailable" banner, falls back to the `--root` scan of `.dev/tasks/{to-do,done}/*/` for ledgers and contracts (every Orca source `unscanned: orca unavailable`; step 1.4), and never runs `orca open` (`scope-02` failure-mode table; `orca-capabilities.md:39`).
- **Worktree removed mid-sweep.** "Worktree removed mid-sweep must be reported, not crash the run" (`research-notes.md:178`); the seed brief lists "a worktree removed mid-sweep" among the failure modes (`.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:45`). When a worktree root vanishes between listing and reading (git or file read fails with a missing path), that worktree and its sessions print could not determine with `unscanned: worktree removed during sweep`, the run continues, the report is still written and the exit code stays 0 (plan decision, new design for the marker text; step 1.4, fixture in step 1.8, test in step 1.9).

### 3.2 Success criteria

| # | Criterion | How it is checked | Source |
|---|---|---|---|
| SC-1 | No local write except the report | Snapshot diff of the isolated root (path, size, `st_mtime_ns`, SHA-256) before and after `sweep run`, with `HOME` and `XDG_STATE_HOME` inside it; only the dated report (and a new `--output` directory) may differ; subprocess entry points patched with `side_effect=AssertionError` (step 1.11) | Subprocess half: `tests/cli/reflect/test_contract_status_cli.py:44-66` pattern (`scope-03:99`) [CODE-VERIFIED]. Snapshot diff: plan decision, no in-repo precedent |
| SC-2 | No Orca call outside the allowlist | Patch the `_orca(*args)` seam and assert every argv against the default allowlist, which names the allowed flags per verb: `worker-list` `--run <id>`, `--json`, `--cursor`; `worker-show` `--dispatch <id>`, `--json`; `worker-read` `--source transcript`; `task-list` `--ready`, `--run <id>`, `--json`; `run-list` `--cursor`; `run-current`; `gate-list`; `worktree ps` `--json` (step 1.4). The test fails on any other flag, including `--include-remote` while GQ-22 is unmeasured, and on `check` (while the probe is unsettled), `--ack`, `--wait`, `--unread`, `--format`, `reply`, `ask`, `send`, `inbox` or `worktree ps --agent-wait` | `scope-03:99` (NB-2, NB-4) |
| SC-3 | Argv uses the full verb form | Every pinned argv is `orca-ide orchestration <verb>`, except the one named top-level verb `orca-ide worktree ps --json`; the test asserts exact argv tuples | C13 [CODE-VERIFIED]; GQ-85 |
| SC-4 | Classification is deterministic and follows the precedence | Unit tests with mocked rows, one per rule 1-7 plus idle, including fenced-with-exited, `agentWait` null vs absent, and guard-refused. Step 1.9 also tests the worktree conditions with mocked git output: no upstream, ahead of upstream, untracked and unstaged `.dev/tasks/` paths, each "worktree removable: no" with the condition named, and a failed git call giving could not determine (`seed-brief.md:60`, `:68`). Rule 3 (fenced) is tested on synthetic fixtures only: no captured field or allowed probe carries `consumer_fenced`, so on live rows it is not buildable in Phase 1 and the row is could not determine (step 1.3; S9 row 81a) | `research-notes.md:190-202`; seed brief "mock-testable" (`research-notes.md:229`) |
| SC-5 | Absence never reads as death | A late heartbeat, `unverifiable` or a missing row gives could not determine; no test path yields stalled without stop proof | WC-10 `WORKER-CONTRACT.md:45` [CODE-VERIFIED] |
| SC-6 | Every class has a report home | The Sessions table Class column carries every class; stalled (proved) and could not determine also appear under Retained problems | `scope-04:332` |
| SC-7 | An item stays listed while its source still shows it, whatever its age (the sweep cannot see answers, G-B, so it prints "Answered: could not determine"; "until answered" is the WC-14 G5 coordinator duty, step 1.17) | Fixtures with an open Task, a non-null `agentWait` and a `blocked` contract, each older than the window, are still listed; the same items removed from a source that was read are no longer listed; when the source itself is lost or unscanned (Orca down, contract unreadable), the affected rows print could not determine with the `unscanned:` reason and none turns resolved, failed, not frozen or retry-recommended (step 1.12) | `research-notes.md:221`; N-41; "Source loss does not resolve questions, fail sessions, unlock a policy freeze or authorize retries." (`PKG/integration-gaps.md:24`, `scope-04:221`) |
| SC-8 | Honest counts | `<shown>/<total>` on every list; a 100-row result prints "truncated at 100" as could not determine | `scope-04:292`; GQ-48 |
| SC-9 | Real observation time in the header; "Messages coverage: partial" | Static check on the rendered report | `scope-04:270`, `:276`; web-02 recommendation 1 |
| SC-10 | CLI registered | `main.add_command(sweep_group, name="sweep")` after the pattern at `main.py:559-561`; a `CliRunner` `--help` test | `scope-03:135`, `:141` [CODE-VERIFIED] |
| SC-11 | Routing registries updated | `_POST_REFRESH_ADDITIONS` gains `"sweep"` (`test_routing_refresh.py:33`); HOW-WE-WORK "Other commands" row (`:318-337`, ASCII only); `_OTHER_COMMANDS` gains `"sc:sweep"` (`test_how_we_work_routing_table.py:27-40`); plugin byte copy (`test_routing_plugin_parity.py:38`), unless GQ-24 places sweep in the excluded set | `scope-03:136-139` [CODE-VERIFIED] |
| SC-12 | Contract tests pin WC-14 | `RULE_PHRASES` gains a WC-14 entry (`test_worker_contract.py`, under the comment at `:163`); `/sc:sweep` joins `NEVER_AS_WORKER` (`:245-254`, 8 entries; the test name says "all seven", N-34) and the phrase at `:86-92` | `scope-01` test-pinning section |
| SC-13 | `make lint` passes | lint-architecture Checks 1, 2, 3/4, 6, 8, 9 and 11 (`Makefile:362-489`); the SKILL.md `name:` ends in `-protocol`; no contract constants re-declared under `cli/` | `scope-03:143-150` [CODE-VERIFIED] |
| SC-14 | Suite-wide scans pass | `test_model_alias_policy.py:81-100`; `test_graph_command.py:219-225`; the AC-0.9 write-verb audit over `AUDIT_ROOTS` (`test_worker_contract.py:1090-1094`); no `## Unattended mode` section | `scope-03:152-157` [CODE-VERIFIED] |
| SC-15 | `make verify-sync` clean | `src/superclaude/` edited first, then `make sync-dev` | CLAUDE.md component sync; `scope-03:163` |
| SC-16 | PATH form works under pipx | Run `superclaude sweep --help` once from a project that is not a uv project; a static test pins bare form first and both forms in `allowed-tools` | `scope-03:208` (GQ-25; [UNVERIFIED] until run -> Open Questions) |

### 3.3 Constraints

| Constraint | Rule | Evidence |
|---|---|---|
| Read-only | No stop, cancel, merge, remove, Task creation, `orca open`, `check` (any mode, until the probe settles Gaps 1, 2 and 18), `inbox`, `--agent-wait`, `ccsession --list` (it writes: `ensure_names_migrated`, `ccsession:285-287`), or `git stash` beyond `list` | `scope-03:99`; `research-notes.md:178-182`; `06:158-175` |
| Coordinator-only | `/sc:sweep` is never run as a worker; it joins the never-as-worker list at `WORKER-CONTRACT.md:23` | `scope-01:80` (G3) |
| WC-10 | A missing heartbeat is absence, never death; the coordinator acts only on Orca's stall proofs | `WORKER-CONTRACT.md:45` [CODE-VERIFIED] |
| WC-6 | A retry is a new Task, never `--retry-of`, and never on `unverifiable`. `[G:recovery]` row 9 conflicts with this; WC-6 wins (GQ-98) | `WORKER-CONTRACT.md:70`, `:73`, `:74` [CODE-VERIFIED] |
| WC-12 | A fenced worker ends without `worker_done`; rule 2 excludes fenced evidence | `WORKER-CONTRACT.md:60` [CODE-VERIFIED] |
| WC-3 / WC-5 | A worker blocked in `ask` sends no heartbeat; Orca shows blocked and failed alike as `failed`, so the contract is read first | `WORKER-CONTRACT.md:54-58` [CODE-VERIFIED] |
| WC-13 | No fan-out; a non-null `parent` is a violation to report | `WORKER-CONTRACT.md:39`, `:61` |
| WC-11 and git ownership | The report is a local file with a timestamped name (WC-11 naming rule); a post is an outward action needing the person's instruction. `.dev/` is a working default only (GQ-10, open) | `WORKER-CONTRACT.md:46` (naming), `:112`, `:114` [CODE-VERIFIED] |
| Freeze and cleanup refusal | A frozen plan is "waiting on a person", never safe to close; the five refusal conditions, plus unpushed commits and unsaved `.dev/tasks/` content (below), gate "worktree removable" | `WORKER-CONTRACT.md:108`, `:133-136` [CODE-VERIFIED]; `seed-brief.md:68`; `issue-summary.md:10`; analysis F5 (`analyze-worker-contract.md:36`) |
| `.dev/tasks/` never disposable | `.dev/tasks/` content is never classed as disposable: an untracked or unstaged path under `.dev/tasks/` makes a worktree not removable, and the report never lists task packages, ledgers or their `artifacts/` as clutter | `seed-brief.md:60`; analysis F4 (`analyze-worker-contract.md:35`); repo `.dev/tasks/` always-staged rule (`WORKER-CONTRACT.md:117`) |
| No new store, extend the contract | No new protocol or database; the report is the only output | `research-notes.md:229` (seed brief `:53-59`) |
| Signals excluded | `stage.activity` (stays "working" after settlement, C5), `resource.terminalState` as a class input, heartbeat age as stall proof | `lc17-show-1.json:132`; `research-notes.md:204` |
| Later phases, recorded only | `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay (GQ-66) are out of Phase 1 | research question |
| Option A4 rejected | Extending `sc-crash-recovery` is [CODE-CONTRADICTED]: `Bash(git stash *)` in allowed-tools (`SKILL.md:4`), `--all` and one dev-fallback allowlist entry hardcode `~/workspace/` (`:4`, `:25`, `:36`, `:53`) where this host's worktrees are under `~/workspaces/` (host observation: this worktree's path; single-project mode uses the cwd, `:49-50`), 72 h default, and `bootstrap_scan.sh` bugs at `:31` (encoding), `:73` (`.git` is a file in a worktree) and `:136` (JSON escaping). Its SAFE/REVIEW vocabulary and report shape may be reused without its scripts | `research-notes.md:160-162`; `scope-02:131-146` |

**External context (supports the constraints; the codebase rules govern):**

| Finding | Effect on the target | URL |
|---|---|---|
| Kubernetes `Ready=Unknown` is distinct from `False`; OTP restarts on an exit signal; Pekko's phi detector says a suspect can come back. All independently support WC-10 (web-01 findings 1-2) | could not determine is a first-class class | https://kubernetes.io/docs/reference/node/node-status/ ; https://www.erlang.org/doc/system/sup_princ.html ; https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html |
| gRPC `UNKNOWN` vs `SERVICE_UNKNOWN`; Nagios UNKNOWN as a broken check (web-01 recommendation 1) | Split could-not-determine causes: evidence absent vs source unreadable | https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto ; https://nagios-plugins.org/doc/guidelines.html |
| Camunda excludes waiting for outside input from time budgets (web-01 finding 4) | Waiting on a person is healthy; exclude person-wait time from activity ages and the 6 h activity window (the waiting list still sorts on time since the wait began) | https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ |
| Harmonograf labels a progress-free run "stuck" (web-01 D3) | Heuristics are a note column only, never the stalled class | https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md |
| Kubernetes eviction after Unknown; liveness probe restarts (web-01 D1, D4) | Rejected for Phase 1 (WC-10; no action) | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ ; https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ |
| Icinga 2 UNKNOWN = "could not determine the service's state"; a probe timeout reports UNKNOWN (web-02) | A probe timeout maps to could not determine | https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/ |
| Statuspage keeps component state, incident lifecycle and impact as separate fields (web-02) | Safe to close stays a separate dimension | https://support.atlassian.com/statuspage/docs/top-level-status-and-incident-impact-calculations |
| Grafana lets missing data map to firing or OK, and an evicted series can look resolved (web-02) | **Contradicts WC-10; rejected.** A row that drops out of a listing is never "finished" | https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ |
| Kanban Work Item Age; `gh issue list` "Showing 30 of 624" (web-02) | Oldest first with an unknown-age group; `shown/total`, with an "at least N" form when the total is unknown (an extension of #409) | https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf ; https://github.com/cli/cli/issues/12196 |
| I-PASS action list with owner, "watcher" state and if-then contingency; PagerDuty "next update" (web-02) | Optional text-only "what to check next" line per waiting item; the header gives the observation time | https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html ; https://docs.pagerduty.com/ops-guides/incident-response-guide/incident-commander |

Excluded from the target, with reason: phi-accrual and progress-counter scores (web-01 recommendation 6: Orca exposes no heartbeat history, GQ-17); OTP-style restart budgets (web-01 recommendation 5: later phase only).

---

## 4. Gap Analysis

### 4.1 Severity rules

| Rule | Statement |
|---|---|
| R-1 Source severity | A row keeps the severity its source gives. G1-G7 follow N-32. B- and NB- findings are Important. Open questions that the sources call non-blocking are Minor (`gaps-and-questions.md:20`). |
| R-2 Unwired in-scope capability | **An in-scope Phase 1 capability that is designed but not wired into code, contract text, tests and registries is a defect rated Critical.** It is never retired as "future work" unless a scope decision is cited. The rule applies to the `/sc:sweep` command, skill and CLI (G3), the Section C classifier (G4), WC-14 and its clauses (G1, G2, G5), the static report writer, the read-only proof tests and the registries. For these rows R-2 wins over R-1: the row is rated Critical until wired, and the source severity is kept in the Severity cell for reference. G7 is not in this list: the report location is an owner decision (GQ-10), and the writer it governs is the separate Static report writer row. It does not apply to items the research question puts in later phases: `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay. Those are recorded only, and the research question is their cited scope decision. |
| R-3 Rows without a source severity | [CODE-CONTRADICTED] and [STALE DOC] rows have no source severity. They are rated **Important** when the wrong claim would change the Phase 1 design or a test (for example the read-only claims C3 and scope-02:165), and **Minor** when they are wording, line numbers or counts. Each row states its basis. |

### 4.2 Core gaps (G-A, G-B, G1-G7, and the Phase 1 build)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| G-A (GQ-01): `worker-list` row schema | No populated row has been captured (`lc01-step7.txt:28` is `[]`), so the row's fields are [UNVERIFIED] (C10). `agentWait` is not inside `projection` (`lc16-show-4.json:180,185`) [CODE-VERIFIED] | Use only the list envelope and the Dispatch id, then call `worker-show --dispatch <id> --json` once per row. Page on `page.nextCursor`. Worst case is ceil(N/100) list calls plus N show calls (05 `:165`, Gap 1 `:186`) | Critical | Open, partly answered. Closes only with a live `worker-list --run <id> --json` capture -> Open Questions. N-29 suggests downgrading once the fallback is accepted. The call count versus the batching policy is GQ-99. |
| G-B (GQ-02): no non-consuming read of pending questions | Every `check` mode goes through `callOrchestrationMutation` (`message-check-handler.js:30`). `inbox` read-marking is [UNVERIFIED] (06 Gap 4 `:161`). No read path exists (C11) | "Waiting on a person" (a) comes from the contract fallbacks only: WC-3 `blocked_question` (when rule 1's condition in step 1.3 holds) and a non-null `agentWait`. The frozen-plan test at `WORKER-CONTRACT.md:133-136` gives kind (b), never (a). The header prints "Messages coverage: partial", and every question shows "Answered: could not determine" (06 `:77`) | Critical | Open but answered for the design. Related Orca unknowns: GQ-43, GQ-44, GQ-47, GQ-48, GQ-56, GQ-57, GQ-59 (section 4.4). |
| G1 (GQ-04): no keep-polling rule | `WORKER-CONTRACT.md` has no rule that the coordinator keeps polling (`scope-01:78`) | WC-14 clause 1. It cites the owner order of 2026-11-05 in the memory note `coordinator-never-stop-polling.md` (N-30) | Critical | R-1 (N-32) and R-2. scope-01 marks the source [UNVERIFIED]; N-30 says the note is readable. |
| G2 (GQ-05): no re-arm rule | No current text (`scope-01:79`) | WC-14 clause 2: an expired wait is re-armed, never treated as done | Critical (R-2, unwired; source severity Important, N-32) | In scope as a WC-14 clause. |
| G3 (GQ-06): no periodic sweep | No `commands/sweep.md`, no `sc-sweep-protocol` skill and no `sweep` CLI group exist (`scope-01:74`, `scope-03:129`) [CODE-VERIFIED] | Option A1: `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, a `superclaude sweep` Click group registered after `main.py:559-561`, and the cadence stated in WC-14 clause 3 | Critical | This is the feature itself. A2 is not deterministic. A3 cannot import package code. A4 is rejected (section 3.3). |
| G4 (GQ-07): no classification vocabulary | Resolved on paper: `research-notes.md` Section C (`:188-204`) is the one canonical vocabulary (C14, B-01, B-28). No code implements it | A pure classifier module with no subprocess calls that applies rules 1-7 and idle in precedence order, with unit tests per rule (SC-4) | Critical (R-2, unwired) | The source gap is resolved, but the capability is not built. Six classes versus seven: section 4.8. |
| G5 (GQ-08): no rule for when to tell the person | The triggers are spread across `WORKER-CONTRACT.md:126`, `:127`, `:129`, `:134` and `:156` (`scope-01:82`) | WC-14 clause 5: one list, with each item kept in the report until answered | Critical (R-2, unwired; source severity Important, N-32) | Design decision for the plan. |
| G6 (GQ-09): person-started sessions | No rule. The evidence route (pane-key join) is [CODE-VERIFIED] for one worker, lc16 (C12) | Reported in Phase 1, observed and never messaged; `idle` applies only to these sessions | Important (N-32) | Settled by the sources, not an owner decision: `BUILD-REQUEST.md:12`, `seed-brief.md:66`, `:75`, analysis F2 (`analyze-worker-contract.md:33`). Conflicts with research-notes AMBIGUITY 8 (`research-notes.md:310`, "or limit Phase 1 to Orca workers"); the sources win (Section 3.1 G6). The remaining work is the rule text in WC-14 and the readers in steps 1.3-1.4. Overlaps GQ-18. |
| G7 (GQ-10): report location | No source fixes a location | A dated local file (timestamped name, WC-11 `:46`), never posted (`:112`, `:114`). `.dev/` is a working default, still open; the exact directory is an owner decision | Important (N-32; R-1, outside R-2's list) | The writer itself is Critical (next row); only the directory is a decision. |
| Static report writer | The #409 layout exists only at unmerged commit `495eb96d` (GQ-35), and it hardcodes its clock (`canvas.py:73-77`). No static writer exists | A writer for the skeleton in section 3.1: real observation time, waiting kinds (a) and (b), Retained problems, Sessions with 10 dimensions plus a derived Class column, Worktrees, Historical, the footer, and `shown/total` | Critical (R-2) | Column sources are at `scope-04:336-351`. Layout questions are GQ-29 to GQ-35. |
| Read-only proof tests | No sweep tests exist. Patterns exist: `test_contract_status_cli.py:44-66` and the `reflect/config.py:64-78` seam | SC-1 (no local write), SC-2 (`_orca(*args)` argv allowlist), SC-3 (full verb form) | Critical (R-2) | Designed in B-13/NB-2/NB-4 (`scope-03:99`). Without these tests the read-only claim is unproven. |
| Registries and suite gates | No sweep entry is registered (`scope-03:129`) | SC-10 to SC-15: `main.py`, `_POST_REFRESH_ADDITIONS`, HOW-WE-WORK "Other commands", `_OTHER_COMMANDS`, plugin byte copy, commands.md UTILITIES, `NEVER_AS_WORKER`, `RULE_PHRASES`, lint-architecture, `make verify-sync` | Critical (R-2) | Placement choices are GQ-12, GQ-24 and GQ-28. `NEVER_AS_WORKER` has 8 entries but its test is named for seven (N-34). |

### 4.3 The four known non-critical gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| K1 (GQ-18): pane-key to transcript join | [CODE-VERIFIED] for lc16. Replacing `:` with `+` in `assigneePaneKey` gives the orca-tabs file name, and that file's line 3 is the `assigneeHandle` (`lc16-show-4.json:11-12`) | Used for Orca pane rows; person-started sessions are in scope (G6, Section 3.1) | Important (resolved; `research-notes.md:273`) | Resolved: the pane-key join is the design (section 4.5; 8.1; 9.6). It is verified for one worker only, so a second-worker check is kept as a verification step (S9 row 93), not as an open gap. |
| K2 (GQ-19): fix `bootstrap_scan.sh` or write a new scanner | `sc-crash-recovery/scripts/bootstrap_scan.sh` has bugs at `:31` (encoding), `:73` (treats `.git` as a directory, which fails in a worktree) and `:136` (JSON escaping) | Write new read-only Python in the sweep CLI. Running `bootstrap_scan.sh` as it is stays excluded (`research-notes.md` Section B) | Important | A plan decision. A4 is [CODE-CONTRADICTED], so nothing builds on it (`BUILD-REQUEST.md:21`). Tension named: analysis F11 (`analyze-worker-contract.md:42`) and `issue-summary.md:21` ask to reuse crash-recovery's signals; the plan reuses the signals (the same on-disk files, step 1.4) and re-implements only the buggy scanner and the whole-file log parser (Section 2.3). |
| K3 (GQ-25): `uv run superclaude` outside a uv project | Decision B-19 is made: PATH form first, `uv run` fallback, both forms in `allowed-tools` | SC-16: a runtime check from a non-uv project plus a static test of the order | Important | Pipx PATH behaviour is [UNVERIFIED] -> Open Questions. |
| K4 (GQ-23): lazy or eager start of the Orca client | Both patterns exist: lazy `__getattr__` at `recommend/__init__.py:12-20` and eager imports at `reflect/__init__.py:17-30` | Lazy, as `scope-03` OQ1 recommends | Important | A plan decision. The seam location is GQ-27. |

### 4.4 Other open gaps (Orca behaviour, plan and owner decisions, #409 layout, wording)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| GQ-37: `unverifiable` and `exited` never captured | Their meanings and the six reason codes come from guide text only (`[G:recovery]` 34-38, 58-59) | Rules 2 and 7 are tested against a live stalled-row capture | Important | N-29. -> Open Questions. |
| GQ-58: null `agentWait`, help versus guide | `[H:worker-show]:16` reads "looked and found no wait"; `[G:recovery]:58-61` reads "same absence seen again" (06 `:144` is CC by help) | null = no wait observed, which is valid for working and never stall proof; absent = could not determine | Important | B-10. Contradiction in section 4.8. |
| GQ-40: nested workers (C15) | Guide `[G]` 130-131 says workers start helpers; `orca-capabilities.md:97-102` says depth 1 forbids it | The sweep reports a non-null `parent` (`lc16-show-4.json:115`) as a WC-13 violation for review | Important | Orca behaviour is [UNVERIFIED]; the sweep-side rule is settled. |
| GQ-43: does plain `check` mark rows read | Every check goes through `callOrchestrationMutation` (`message-check-handler.js:30`) | Plain `check` is forbidden | Important | [UNVERIFIED]. |
| GQ-44, GQ-57 and GQ-59: `check --peek` / `--all` side effects; `ackMessageIds`; runtime probe | Not side-effect-free by construction: older runtimes ignore `--peek` (`:17`), and both modes can trigger `compatibilityAck` (`:58-71`). No read-only version verb was found | Default is contracts only. `check --peek` / `--all` become a separate addition, gated on a probe | Important | `scope-03:99` (NB-2). |
| GQ-48 and GQ-56: enumeration past 100 rows; `check --all` `run:<id>` rows | `--all` and Run `--peek` cap at 100 with no cursor (`[H:check]:37`); older runtimes keep the newest 100 (`message-check-handler.js:82-83`) | A 100-row result reports "could not determine: message listing truncated at 100" | Important | B-18. |
| GQ-60: where the logic lives (AMBIGUITY 1) | Open, leaning A1 | A1 (section 3.1) | Important | A4 [CODE-CONTRADICTED] (`research-notes.md:160`). |
| GQ-61: window 6 h or 72 h (AMBIGUITY 2) | Open owner decision | 6 h default bounding activity only; open Tasks, questions and unread reports are always listed | Important | N-41. The research question fixes 6 h, but the owner decision is still recorded as open. |
| GQ-63: `pragmatic` DONE/NEXT "No exceptions" | `pragmatic.md:22`, `:53` give no exception mechanism; `launch-job-identity.sh` sets no environment variable | Owner decision on how a sweep report is exempted, if at all | Important | B-04 is resolved as evidence; the decision stays open. |
| GQ-21: exclude `git stash *` and `ccsession --list` | crash-recovery allows `Bash(git stash *)` (`SKILL.md:4`), and `ccsession --list` writes (`ensure_names_migrated`) | Both are excluded from the sweep's allowed-tools and code | Important | C3 and scope-02:165. Excluding `ccsession --list` overrides `seed-brief.md:33`, `:75`, `issue-summary.md:22` and `analyze-worker-contract.md:60`, which name it as a sweep input; read-only wins (Section 2.3). |
| GQ-15, GQ-16, GQ-17, GQ-22, GQ-36, GQ-38, GQ-39, GQ-41: Orca field and shape unknowns | `liveness.reason` values, `runtime_unavailable` shape, whether heartbeat age feeds liveness, the cost of `--include-remote`, the non-null `agentWait` shape, `page.hasMore` past 100 rows, `counts` keys and the capture CLI version are all [UNVERIFIED] | The classifier treats each unknown as could not determine, never as stalled | Minor | -> Open Questions. |
| GQ-46, GQ-47, GQ-49 to GQ-54, GQ-64, GQ-65: Orca read and identity unknowns | `inbox` read-marking, `reply` effect, `--dispatch-capability`, peer `ask --to run:<id>`, whether the `--agent-wait` probe writes, `agentWait` while blocked in `ask`, missing `caller`, cross-host joins, whether `identify` writes, `task-list` / `gate-list` caps: all [UNVERIFIED] | `inbox` and `--agent-wait` stay forbidden. "Answered: could not determine". Unknown caps print `shown/total` or "at least N" | Minor | N-35: a pending `ask` waits on the coordinator, not a person. |
| GQ-11, GQ-12, GQ-14, GQ-24, GQ-26, GQ-27, GQ-28: rule id and registry placement | add WC-14, or reuse the unused WC-1 ID; never-as-worker test changes; whether a test requires help or HOW-WE-WORK registration; "Other commands" versus the excluded set (also the routing-table option, N-37); how `allowed-tools` patterns combine; probe module location; whether a test pins UTILITIES | Decided in the plan, with each decision cited | Minor | GQ-14, GQ-26 and GQ-28 are [UNVERIFIED]. |
| GQ-29 to GQ-35: #409 layout | Sort tie-break, closure evidence, per-source coverage, scope line, omission bound, Approval label and its `gate-list` mapping ([UNVERIFIED]), pinning to unmerged `495eb96d` | Plan decisions inside the skeleton in section 3.1 | Minor | C6 and C7 apply. |
| GQ-62, GQ-66, GQ-67, GQ-100: sequencing and owner clarifications | PR #422 sequencing; meaning of "management server"; APPROVED.md texts unverified. GQ-67 (worktree-first versus trigger-based placement) is settled, not open: CR-01 is the approved child-worktree trigger rule (`seed-brief.md:42`; analysis F12, `analyze-worker-contract.md:43`; `decisions/APPROVED.md:25`). A child worktree is used only when a trigger applies (T1 the brief authorizes commits, T2 `/sc:implement` beside another writer outside `.dev/`, T3 `/sc:pr-submit`, T4 a parallel experiment), otherwise the shared feature worktree (`CR-01-feature-worktree-hierarchy.md:12-21`; WC-11, `WORKER-CONTRACT.md:46,87`). The issue's "new worktree is always first choice" is not adopted. [Sources disagree on CR-01's status: the CR-01 file header still reads "Status: PROPOSED" (`CR-01-feature-worktree-hierarchy.md:3`), while `APPROVED.md:25` and the seed brief record it as approved; the report follows `APPROVED.md:25`, the later decision record.] | Owner decisions (GQ-62, GQ-66, GQ-100). The management-server relay is a later phase, recorded only | Minor | GQ-62 is inside Phase 1: PR #422 gates steps 1.17-1.19 (Dependencies row, step 1.16a). GQ-66 is a later-phase decision; GQ-67 is settled by CR-01 and applies when a later phase places workers (Phase 1 is read-only and places none); GQ-100 is a pre-implementation read. |
| GQ-84: fenced exclusion with an unreadable transcript | Rule 2 fires before rule 7 | The plan states: exited, no `worker_done` and an unreadable transcript give could not determine | Minor | Not a WC-10 break. |
| GQ-85: mixed verb forms at `scope-03:99` | Bare `worker-list` next to full `orchestration <verb>` | Every pinned argv is `orca-ide orchestration <verb>` (C13) | Minor | `qa-nb4-fix-log.md:41`. |
| GQ-86 to GQ-95, GQ-97: wording and citation residuals | `--unread` versus `--unread --peek` wording; `scope-01:64` "class"; 06 `:57-58` tags; stale 06 `:187`; `filterLegacyPeekResult` runs on every peek; `scope-04:290` and `:320`; "needs a human" at `research-notes.md:225` and `scope-04:356`; G-A versus G-B at `research-notes.md:175`, `:196`; MISSING list at `:241-242`; a default stated as fact at `05:165` and `scope-01:142`; small citations | The canonical terms from Section C apply in the final report | Minor | No design effect. |
| GQ-98: `[G:recovery]` row 9 `--retry-of` | The guide says to start a replacement with `--retry-of` | A new Task, never `--retry-of` (WC-6) | Minor | Contradiction in section 4.8; WC-6 wins. |
| GQ-99: N `worker-show` calls versus the batching policy | Follows from G-A's worst case | Per-sweep bounds stated in step 1.4 (50 calls, 90 s), with a degraded but written report at the bound | Minor | N-40; S9 row 63. |

### 4.5 Resolved gaps (kept for traceability)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| GQ-03 (NB-4): allowlist omitted read verbs | Fixed: `scope-03:99` now allows `task-list`, `run-list`, `run-current` and `gate-list`, and `inbox` stays forbidden | Pinned by SC-2 | Important (resolved) | `qa/qa-nb4-fix-log.md` edits 1-3. The summary line `gaps-and-questions.md:125` now reads Open 75 / Resolved 25. |
| GQ-07, GQ-13, GQ-18, GQ-42 | Vocabulary (Section C); `AUDIT_ROOTS` scans `commands/` (`test_worker_contract.py:1090-1094`); pane-key join for lc16; other read surfaces are plain reads | Used as designed | Critical / Minor / Important / Important (resolved) | GQ-07 is still Critical as an unwired capability in 4.2 (R-2). |
| GQ-20, GQ-45, GQ-55 | `stage.activity` is never a signal (C5); `check --unread` is destructive and forbidden (`message-check-handler.js:33-34`); `--format` is a local text switch (`:38`, `:55`) | Excluded | Minor / Important / Minor (resolved) | [CODE-VERIFIED] or CC as tagged. |
| GQ-68 to GQ-83 (B-02, B-03, B-05/NB-1, B-11 to B-14/NB-2, B-20 to B-27, NB-3) | Safe to close is a dimension; full verb form; stall needs positive proof, with fenced excluded; waiting kinds (a) and (b); every class has a report home; read-only proof tests designed; missing columns added; tags fixed; suite scans listed; `--ack` claim corrected; lint gates listed; PATH-first call form | Built into sections 3.1 to 3.3 | Important (resolved) | Residuals are GQ-84 to GQ-95. |
| GQ-96: blocked `/sc:implement` fits kinds (a) and (b) | Accepted: the dimensions are independent. The policy dimension is computed for every row independently of the class, so a blocked implement contract on a settled row, under `report blocked` or for a Ruling halt gets class waiting on a person (a) from rule 1 and policy frozen, and is listed under (b) too; on a live, unsettled row under `ask the coordinator` it gets no class from rules 1, 4a or 4b-contract and policy could not determine (WC-3, `WORKER-CONTRACT.md:54-56`; the GQ-96 source states it without this condition, the report follows WC-3) | Built into section 3.1 and steps 1.3 and 1.8 | Minor (resolved) | `gaps-and-questions.md:119`; `research-notes.md:197` |

### 4.6 [CODE-CONTRADICTED] findings, corrected

| Gap | Current State (claim) | Target State (correction) | Severity | Notes |
|---|---|---|---|---|
| C1 (scope-01 `:111`, `:129-138`; research-notes `:40`) | The analysis findings are numbered F1-F12 | Use F1-F14 and S1-S5 (`analyze-worker-contract.md:30-55`) | Minor | R-3: numbering only. |
| C2 (research-notes `:31`) | `test_how_we_work_routing_table.py` is about 360 lines | 1202 lines | Minor | R-3: count only. |
| C3 (scope-02 `:131`) | sc-crash-recovery is "pure read-only" | `Bash(git stash *)` is allowed (`SKILL.md:4`) | Important | R-3: it decides A4 and GQ-21. |
| C4 (scope-02 `:132`, `:133`, `:241`; research-notes `:160`) | crash-recovery scans `~/workspace/` with a 72 h default | Only `--all` scans `~/workspace/` (`SKILL.md:25`, `:36`, `:53`), plus one dev-fallback allowlist entry (`:4`); single-project mode uses the cwd (`:49-50`). This host's worktrees are under `~/workspaces/` (host observation: this worktree's path, not a skill fact). The 72 h default (`:26`) is not adopted | Important | R-3: a reason A4 is rejected. |
| C5 (scope-02 `:74`; 05 `:132`, `:137`, Gap 7 `:192`; research-notes `:145`) | `stage.activity` signals work in progress | It stays "working" after settlement (`lc17-show-1.json:132`, `lc01-show-1.json:132`); use `projection.*` | Important | R-3: a classifier input. |
| C6 (scope-04 `:93`, `:368`; research-notes `:225`) | The #409 Attention Ledger is age-ranked | No sort at `agent_focus.py:46` at `495eb96d` (partial CC) | Important | R-3: the sweep must sort oldest first itself. |
| C7 (scope-04 `:247`, `:371`; research-notes `:225`) | #409 lists carry omission counts when limited | Weaker than first stated: listboxes (`agent_focus.py:17`), wide Outcome Ledger (`:114`) and wide Revision Drift (`:127`) do print `shown/total`; only the wide Attention Ledger and Shift Brief request loops (`:46-50`, `:164-167`) print none, and they do not truncate (unbounded, not limited without a count) | Important | R-3: the sweep must bound those two lists and add `shown/total`. |
| C9 (scope-03 `:76`; research-notes `:75`) | The recommend docstring's `python -m` usage | Against the UV rule; never copied | Minor | R-3: a docstring. |
| C13 residual (scope-02 `:16`, `:235`) | Bare `orca` command form | `orca-ide orchestration <verb>` [CODE-VERIFIED] | Important | B-03 is resolved; GQ-85 is the residual. |
| scope-02 `:146` | Bug 1: ENCODED_CWD replaces only `/` | An encoding bug in `bootstrap_scan.sh:31` | Minor | K2 (GQ-19). |
| scope-02 `:165` | `ccsession --list` is read-only | It migrates names (`ensure_names_migrated`, `ccsession:285-287`) | Important | R-3: excluded source (GQ-21). |
| scope-01 `:100` | The "41 tests" cross-reference | Tagged CC for the two cross-references only (`issue-summary.md:18` and `analyze-worker-contract.md:46` no longer contain "41 tests"). The count itself is right: `tests/skills/test_worker_contract.py` has 41 `def test_` functions [CODE-VERIFIED, re-counted in the Phase 6 QA fix pass]. Settled here; no open question | Minor | R-3: count only. |
| scope-03 `:108`, `:111` | recommend.md `name:` shape; Activation uses an "identical form" | Follow `issue.md` (newest template) for frontmatter and the Activation block | Minor | R-3: template detail. |
| scope-03 `:165` | No test globs every skill | Suite-wide scans exist (`scope-03:152-157`) | Important | R-3: these are SC-14 gates (B-21). |
| scope-04 `:33` | Generated files "Not read" | Tagged CC at `scope-04:33`; open, and the sweep does not depend on it | Minor | R-3: process note. |
| 06 `:63`, `:85` | `--format` help is self-contradictory | `--format` is a local text switch (GQ-55); forbidden | Minor | R-3: verb is not used. |
| 06 `:144` (CC by help) | A null `agentWait` means the same absence seen again | Help says looked and found no wait; see GQ-58 | Important | R-3: a classifier input. |
| Option A4 (research-notes `:160`; scope-02 `:241`) | Extend sc-crash-recovery | Rejected; see section 3.3 | Important | Shown only as a rejected option. |

### 4.7 [STALE DOC] findings

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| S-01: `orca-capabilities.md:8`, `:12` | Names CLI 1.4.237 and a 202-line guide | CLI 1.4.245 and a 215-line guide; `[G]` line numbers re-based | Minor | R-3: citations shift. Found at 05 `:199`. |
| S-02: `orca-capabilities.md:127` | Paging rule omits `page.hasMore` | Mention `page.hasMore`; the sweep pages on `page.nextCursor` | Minor | 05 `:200`. |
| S-03: `orca-capabilities.md` inventory | Missing `[H:worker-list]` line 22 (default scope) | Add it | Minor | 05 `:201`. |
| S-04: `orca-capabilities.md:97-102` | Candidate stale text against guide `[G]` 130-131 | Depends on C15 | Important | R-3: nested-worker rule (GQ-40). 05 `:202`. |
| S-05: `orca-capabilities.md:68`, `:177` | `ask` timeout | 600000 ms default, range 1 to 1800000 | Minor | 06 `:180`. |
| S-06: `orca-capabilities.md:8`, `:63` | Guide line numbers | Coordinator wait is `[G]:113`, not 108 | Minor | 06 `:181`. |
| S-07: `analyze-worker-contract.md` as cited by scope-01 | The old 55-line F1-F12 version | F1-F14 and S1-S5 | Minor | C1. |
| S-08: `sc-crash-recovery/SKILL.md:13`, `:155` | "Pure read-only, enforced by allowed-tools" | `Bash(git stash *)` is allowed | Important | C3. |
| S-09: `sc-crash-recovery/SKILL.md:4`, `:25`, `:36`, `:53` | `--all` and the dev-fallback allowlist entry hardcode `~/workspace/...`; single-project mode uses the cwd (`:49-50`) | `~/workspaces/...` on this host | Important | C4. |
| S-10: #409 `concepts.md:23` | Ledger is age-ranked | The code has no sort | Important | C6. |
| S-11: #409 `DESIGN-CONTRACT.md:11` | Requires omission counts when limited | Revised in the fidelity fix cycle: not stale. Docs and wide-view code agree (`agent_focus.py:17`, `:114`, `:127`); the two request lists without a count are unbounded, so nothing is limited without a count | Important | C7 (weaker form): the sweep bounds those lists itself. |
| S-12: recommend command docstring | `python -m` usage | UV form | Minor | C9. |
| S-13: `research/06-orca-open-questions.md:187` | Original summary stale | Superseded by `06:189` | Minor | GQ-89. |
| S-14: `research/research-notes.md:241-242` | Lists 05 and 06 as MISSING | Both exist | Minor | GQ-94. |

These were checked and are not stale: the WORKER-CONTRACT lines that 06 read (`06:182`) and `integration-gaps:11` (`06:183`).

### 4.8 Contradictions and the stronger evidence

| Contradiction | Side A | Side B | Stronger | Effect on Phase 1 |
|---|---|---|---|---|
| How many classes | The research question lists six | Section C lists seven, including fenced (`research-notes.md:194`) | Section C, which rests on WC-12 `:60` [CODE-VERIFIED] | Fenced stays its own class. If the owner keeps six, fenced folds into could not determine -> Open Questions. |
| Default window | The research question fixes 6 h | GQ-61 is open, and crash-recovery uses 72 h (`SKILL.md:26`) | Research question for Phase 1; the owner decision is still recorded | 6 h, activity only (N-41). |
| Null `agentWait` | `[H:worker-show]:16` | `[G:recovery]:58-61` | Neither is code. The sweep rule is conservative (GQ-58) | Never treated as stall proof. |
| Nested workers (C15) | `[G]` 130-131 | `orca-capabilities.md:97-102` | Unresolved; WC-13 governs the sweep | Report `parent` as a violation. |
| Retry form | `[G:recovery]` row 9 `--retry-of` | WC-6 `:70`, `:73` | WC-6 (repo contract) | Recommend "new Task". |
| Missing data | Grafana maps no-data to OK or firing (external, web-02) | WC-10 `:45` | WC-10 | A row that drops out is never finished. |
| Stall heuristics | Kubernetes taints and evicts after `Unknown` and restarts on liveness-probe failure; Harmonograf labels a progress-free run "stuck" with a UI alert only (external, web-01 D1, D3, D4). Of these three, only D1 contradicts WC-10; D3 is naming and D4 an action (synth-03 5.9; D5 and D6 are separate rejections, Section 5) | WC-10, and only Orca stall proofs count | Codebase | Heuristics are a note column only, with no action. |

### 4.9 Open Questions ([UNVERIFIED], not stated as fact)

Numbering: every row is keyed to its Section 9 row ("S9 row N"); Section 9 is the canonical open-question list, and Sections 7.1 and 8.2 use the same keys.

| S9 row(s) | Question | Blocks | Resolve by |
|---|---|---|---|
| S9 row 1 | What does a populated `worker-list` row contain (G-A, C10)? | Call-count bound (GQ-99) | A live `worker-list --run <id> --json` capture |
| S9 row 32 | What do live `unverifiable` and `exited` rows look like, and what is the end-of-turn marker (GQ-37, `research-notes.md:193`)? | Rules 2 and 7 | A captured stalled row and a transcript read |
| S9 rows 38, 47, 49 | Are `check --peek` / `--all` side-effect-free on the current runtime (GQ-44, GQ-57, GQ-59)? | Any use of `check` | Read the runtime handler, or test on a throwaway Run |
| S9 row 29 | How does `gate-list` map to the Approval column (GQ-34)? | The Approval column | Plan probe |
| S9 rows 20, 21 | Does the PATH form work under pipx (GQ-25), and how do `allowed-tools` patterns combine (GQ-26)? | SC-16 | Run `superclaude sweep --help` once outside a uv project |
| S9 row 93 | Does the pane-key join hold for a second worker (K1; C12, verified for one worker only)? | G6 (in scope) | Check one more worker |
| S9 rows 98a, 51, 8, 9 | Six classes or seven; is the window 6 h or 72 h; where does the report go; WC-14 or the unused WC-1 ID (GQ-61, GQ-10, GQ-11)? (Row 7, person-started sessions, GQ-09, is settled by the sources: they are reported; Section 3.1 G6.) | WC-14 text | Owner decisions |
| S9 rows 12, 13, 14, 39, 55 | `liveness.reason` values, `runtime_unavailable` shape, whether heartbeat feeds liveness, `inbox` read-marking, row caps (GQ-15 to GQ-17, GQ-46, GQ-65) | Could-not-determine wording | Captures |

### 4.10 Coverage of the assigned files

| File | Key findings reflected in | Excluded, with reason |
|---|---|---|
| `research/scope-01-contract.md` | Binding rules (3.3), G1-G7 and insertion points (3.1, 4.2), test pinning (3.2 SC-12) | - |
| `research/scope-02-orca-recovery.md` | Data sources and failure modes (3.1), A4 rejection and bugs (3.3, 4.3 K2), CC items (4.6) | `parse_session_log` reuse (`:157`) is UV and is a plan choice |
| `research/scope-03-cli-patterns.md` | Allowlist after NB-4, naming, call form, seam, registries, lint, scans (3.1, 3.2) | - |
| `research/scope-04-409-layout.md` | Skeleton, column sources, report rules, Q1-Q8 (3.1, 4.4) | - |
| `research/05-orca-row-schema.md` | G-A fallback, per-class signals, Gaps 1-10, stale docs (4.2, 4.4, 4.7) | - |
| `research/06-orca-open-questions.md` | G-B, check-mode constraints, Gaps 1-19, stale docs (4.2, 4.4, 4.7) | - |
| `gaps-and-questions.md` | Every row GQ-01 to GQ-100, K1-K4, AMBIGUITIES 1-11 (as GQ-09 to GQ-11, GQ-24, GQ-29, GQ-34, GQ-35, GQ-60 to GQ-63, GQ-66, GQ-67), C1-C15, sections (e) and (f) | - |
| `research/web-01-agent-supervisor-session-health.md` | Findings 1-7, D1-D4, recommendations 1-4 (3.3 External context, 4.8) | Recommendations 5 and 6 are excluded for Phase 1 (3.3) |
| `research/web-02-static-status-report-conventions.md` | Observation time, UNKNOWN on timeout, separate dimensions, oldest first, `shown/total`, optional if-then line (3.1, 3.3) | Grafana no-data mapping rejected (contradicts WC-10) |

---

## 5. External Research Findings

**Precedence:** codebase findings take precedence. Everything in this section is external context: patterns from other systems, each tied to its URL. None of it describes the current architecture of this repo. Where an external pattern conflicts with the codebase rule WC-10 (`src/superclaude/core/WORKER-CONTRACT.md:45`, the only codebase rule here) or with the Orca guide text the design follows (the stall-proof rule in `research-notes.md` Section C rule 2; `orca-capabilities.md:125` [UNVERIFIED — Orca guide]), WC-10 and the guide text win and the conflict is recorded in 5.9. Every `orca-capabilities.md:122-130` cite in this section is Orca guide or help text quoted in the inventory, not code; it is [UNVERIFIED — Orca guide] wherever it appears below.

**Inputs:** `research/web-01-agent-supervisor-session-health.md` (web-01) and `research/web-02-static-status-report-conventions.md` (web-02). Tavily was not available for either; both used WebSearch and WebFetch. web-02 was saved by the task executor from its agent's reply (provenance note in that file).

**Research question context:** Orchestrator mode Phase 1 for issue #339: a read-only, coordinator-only `/sc:sweep` that classifies sessions (waiting on a person, working, stalled (proved), could not determine, finished, idle: the research question's six; Section C adds fenced as a seventh class, `research/research-notes.md:188`, and six versus seven is an open question, Section 9; safe-to-close is a separate dimension) over a default 6 h window that bounds activity only, writes a dated static report on the #409 layout, and adds a WC-14 coordinator-loop rule to `src/superclaude/core/WORKER-CONTRACT.md`; `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay are later phases, recorded only.

**How to read each finding:** "Relationship" says whether the external pattern supports, extends or contradicts what the codebase already does. "WC-10 / read-only" says whether the pattern fits WC-10 (act only on Orca's stall proofs, never on a late heartbeat) and whether Phase 1 can use it without acting on a session. Anything that restarts, kills, evicts, retries or aborts is later-phase only.

### 5.1 Supervisors act on an observed exit, not on silence (Erlang/OTP)

- **[EXTERNAL] Finding:** every OTP restart strategy (`one_for_one`, `one_for_all`, `rest_for_one`) fires only when a child "terminates", learned through a link/exit signal, which is positive evidence. OTP has no "restart because the child was quiet".
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: HIGH
  - Relationship: supports the stall-proof rule (only `exited` liveness or an observed process exit counts).
  - WC-10 / read-only: WC-10 consistent. The restart itself is later-phase only; Phase 1 may only label the row "stalled (proved)".
- **[EXTERNAL] Finding:** restart types split normal finish from abnormal exit: `permanent` always restarts, `transient` only after an abnormal exit (`normal`, `shutdown` and `{shutdown, Term}` do not qualify), `temporary` never.
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: HIGH
  - Relationship: extends. It gives a vocabulary for finished (a `normal` exit: Orca `outcome` settled plus a read return contract) versus stalled (`exited` with no `worker_done`), and for why a `consumer_fenced` dispatch is an intended stop like `{shutdown, Term}`, never a failure (WC-12, `WORKER-CONTRACT.md:60`, as cited by web-01).
  - WC-10 / read-only: WC-10 consistent. Phase 1 uses only the classification half; restart policy is later-phase only.
- **[EXTERNAL] Finding:** restart intensity bounds automated recovery (`intensity` restarts per `period`, default 1 per 5 s); past it the supervisor stops its children, exits with `shutdown`, and "its parent then decides".
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: MEDIUM
  - Relationship: extends. The repo has no retry budget. For a later phase it argues that any automatic retry needs a bound and an escalation to the person (gap G5, GQ-08).
  - WC-10 / read-only: retry on absence is forbidden by WC-10 and is an action, so later-phase only. Phase 1 can at most report "repeated stalls" as a fact.
- **[EXTERNAL] Finding:** shutdown is graceful first: send `shutdown`, wait, then `kill` after the timeout; `brutal_kill` skips cleanup; supervisors default to `infinity`.
  - Source: https://www.erlang.org/doc/system/sup_princ.html
  - Relevance: LOW for Phase 1
  - Relationship: extends. Parallels the safe-to-close REVIEW dimension (terminal releasable only after the result is read; no probe observes that the result has been read, so for a terminal Orca reports as reclaimable with next action release Phase 1 prints "terminal releasable: could not determine (result read not observable); Orca: reclaimable, next action release", with no proxy for the read; worktree removable only when the five refusal conditions at `WORKER-CONTRACT.md:108` are false, as cited by web-01).
  - WC-10 / read-only: shutdown and kill are actions, later-phase only. Phase 1 prints the REVIEW line and never runs it.

### 5.2 Separate probes answer separate questions (Kubernetes liveness, readiness, startup)

- **[EXTERNAL] Finding:** liveness probes decide when to restart a container; readiness probes decide when it may take traffic, and a readiness failure "does not trigger a container restart"; startup probes hold off the other two until the app has started.
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ (WebFetch read the first 100000 of 118034 characters)
  - Relevance: HIGH
  - Relationship: supports the sweep's separate dimensions: liveness verdict (`live` / `unverifiable` / `exited`), waiting on a person (closest to readiness: alive but not taking new work), and terminal state, "reported separately from Task status" (`worker-list --help` line 19, as cited by web-01). Supports "waiting on a person is healthy, not failed".
  - WC-10 / read-only: the readiness idea (report, do not restart) fits Phase 1. The liveness restart is later-phase only. Kubernetes probes call into the container; the sweep must not probe the agent's terminal (GQ-51 excludes `--agent-wait`), so Phase 1 reads Orca's recorded state only.
- **[EXTERNAL] Finding:** "Incorrect implementation of liveness probes can lead to cascading failures"; liveness should catch unrecoverable failure, "not merely temporary overload or an unavailable dependency".
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
  - Relevance: HIGH
  - Relationship: supports WC-10 directly. A long tool call, a model wait or an unreachable remote host (`host_unavailable`, `orca-capabilities.md:124` [UNVERIFIED — Orca guide], as cited by web-01) is overload or an unavailable dependency, not death.
  - WC-10 / read-only: WC-10 consistent. External justification for reporting `unverifiable` as "could not determine".
- **[EXTERNAL] Finding:** liveness probes do not wait for readiness; slow starters need a startup probe or `initialDelaySeconds`.
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
  - Relevance: MEDIUM
  - Relationship: extends. A just-dispatched worker with no heartbeat yet is the startup case; nearest repo equivalents are Orca's `restored_unconfirmed` and a failed start reported `reclaimable` (`orca-capabilities.md:112`, UNVERIFIED, as cited by web-01). The sweep should not read "no activity yet" on a new dispatch as idle or stalled.
  - WC-10 / read-only: WC-10 consistent (no signal during startup is absence). A grace period changes only the label, never an action.
- **[EXTERNAL] Finding:** a process can pass a liveness probe while its work loop is hung, unless the probe exercises that loop ("running but cannot make progress").
  - Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
  - Relevance: MEDIUM
  - Relationship: supports. The repo already says PTY `observation.status` "is PTY liveness only. A live terminal can still hold a dead or stuck agent" (`orca-capabilities.md:123` [UNVERIFIED — Orca guide], as cited by web-01). The design is stricter: no PTY signal counts as stall proof either way.
  - WC-10 / read-only: WC-10 consistent. Phase 1 shows PTY status as context only.

### 5.3 Suspicion is a scale, and a suspected node can come back (phi-accrual failure detection)

- **[EXTERNAL] Finding:** accrual failure detectors "output a suspicion level on a continuous scale" instead of trust versus suspect, and keep monitoring separate from the application's decision of what to do.
  - Source: https://dspace.jaist.ac.jp/dspace/bitstream/10119/4784/1/IS-RR-2004-010.pdf (Hayashibara et al., abstract via search result; PDF not fetched in full)
  - Relevance: HIGH
  - Relationship: extends. The monitor-reports / application-decides split matches Phase 1 (sweep reports, person decides). Orca's verdict is categorical, not a scale; a heartbeat-age column could be shown as context.
  - WC-10 / read-only: a phi value measures absence only, so under WC-10 it can never make a row "stalled"; at most it ranks rows inside "could not determine". Computing it is a pure read, but Orca exposes no heartbeat history (GQ-17 open), so it is not buildable now.
- **[EXTERNAL] Finding:** `phi(t) = log10(1 / (1 - F(t)))` with F a normal CDF fitted to past heartbeat gaps; default threshold 8; a lower threshold detects sooner with more false alarms; `acceptable-heartbeat-pause` adds tolerance for GC stalls and network interruptions.
  - Source: https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html ; https://nightlies.apache.org/pekko/docs/pekko/1.1.3/japi/org/apache/pekko/remote/PhiAccrualFailureDetector.html (API page from search result only)
  - Relevance: MEDIUM
  - Relationship: supports WC-10. Agent heartbeat gaps are very irregular (long tool calls, model latency, a person reading a prompt), which is the regime where any fixed threshold mislabels healthy sessions.
  - WC-10 / read-only: a threshold crossing is a suspicion, which WC-10 forbids acting on. Any phi-triggered action is later-phase only and still needs Orca's stall proof.
- **[EXTERNAL] Finding:** phi is a timing estimate, not certainty of a crash; a node marked unreachable "may subsequently become reachable again" (paraphrase in web-01 of the fetched page).
  - Source: https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html
  - Relevance: HIGH
  - Relationship: supports, no discrepancy. Same as "contact loss is not process death" (`orca-capabilities.md:122`) and "Absence never authorizes stop, abandon, retry, or release" (`orca-capabilities.md:125`), both [UNVERIFIED — Orca guide], as cited by web-01.
  - WC-10 / read-only: a direct external statement of WC-10. Phase 1 reports "could not determine", never "stalled", for any suspicion-only row.

### 5.4 "Unknown" is a first-class health state (Kubernetes node status, gRPC, Icinga, Nagios, Prometheus / Grafana)

- **[EXTERNAL] Finding:** Kubernetes node `Ready` is `True` (healthy), `False` (not healthy) or `Unknown` ("the node controller has not heard from the node in the last `node-monitor-grace-period`", default 50 s). Heartbeats are Node `.status` updates and Lease renewals every 10 s. `Unknown` and `False` carry different taints (unreachable versus not-ready).
  - Source: https://kubernetes.io/docs/reference/node/node-status/ (both web-01 and web-02 cite it)
  - Relevance: HIGH
  - Relationship: supports "could not determine" as its own class. The split maps onto Orca's verdicts: `True` ~ `live`, `Unknown` ~ `unverifiable`, `False` ~ a positive failure report (`exited` / observed exit). Supports GQ-17 (a late heartbeat never proves stalled).
  - WC-10 / read-only: WC-10 consistent at the status layer. Kubernetes then acts on `Unknown` (taint, then eviction after a 300 s toleration, per https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/, search result only); that step is what WC-10 forbids and Phase 1 must not copy (5.9, D1). Data note: the same page also says "40 second default timeout for unreachable nodes", so it is internally inconsistent on the default.
- **[EXTERNAL] Finding:** gRPC health `ServingStatus` is `UNKNOWN = 0`, `SERVING = 1`, `NOT_SERVING = 2`, `SERVICE_UNKNOWN = 3` (Watch only). `Check` on an unregistered service fails with `NOT_FOUND`; `Watch` returns `SERVICE_UNKNOWN` and waits.
  - Source: https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto ; https://grpc.io/docs/guides/health-checking/ (guide from search result only)
  - Relevance: MEDIUM
  - Relationship: extends. Two kinds of unknown: "health not known yet" versus "no such subject". The sweep has the same pair: a row that exists with evidence absent (`unverifiable`, absent-versus-null `agentWait`, GQ-58) versus a source that could not be read at all (the `unscanned:` markers, `research/scope-02-orca-recovery.md:239`, as cited by web-01). Keep the two apart in the report.
  - WC-10 / read-only: WC-10 consistent (UNKNOWN is the default, never NOT_SERVING). `Check` and `Watch` are probes; only the vocabulary carries over.
- **[EXTERNAL] Finding:** Icinga 2 UNKNOWN means "The check could not determine the service's state" (exit code 3); a plugin that hits its own timeout reports UNKNOWN, not CRITICAL.
  - Source: https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/ ; https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/
  - Relevance: HIGH
  - Relationship: supports the "could not determine" class almost word for word.
  - WC-10 / read-only: the direct monitoring precedent for WC-10. A Phase 1 read timeout maps to "could not determine".
- **[EXTERNAL] Finding:** Nagios plugin return codes are 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN; UNKNOWN is for invalid arguments or an internal failure that stopped the check from running. The Nagios support KB says DNS lookup failures and socket timeouts "should generally NOT be reported as UNKNOWN states" (it does not say which code instead).
  - Source: https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html ; https://nagios-plugins.org/doc/guidelines.html ; https://support.nagios.com/kb/article.php?id=72
  - Relevance: MEDIUM
  - Relationship: the return-code scheme supports an explicit unknown; the KB timeout guidance partly contradicts the Orca guide text the design follows, which treats contact loss (`host_unavailable`, `orca-capabilities.md:124`) and absence (`stale_status`, `:125`) as `unverifiable` [UNVERIFIED — Orca guide], reported "could not determine". WC-10 wins (`WORKER-CONTRACT.md:45`). The domains differ: a Nagios timeout on a network service is a user-visible outage, a late agent heartbeat says nothing about useful work. It also conflicts with the Icinga timeout rule above (5.9, C1).
  - WC-10 / read-only: timeout-as-failure is not adopted. What carries over: when the sweep's own read fails (Orca not running, a page that will not load), report it as a sweep failure, separate from a row's "could not determine".
- **[EXTERNAL] Finding:** Prometheus alerts do not fire on missing data; absence must be tested explicitly (`absent()`, `absent_over_time()`), and `up==0` (scrape failed) differs from an absent series (target gone). Grafana: "Missing data isn't always a failure"; No Data handling can be set to NoData, Alerting, Normal or Keep Last State. An evicted series can look "resolved".
  - Source: https://prometheus.io/docs/prometheus/3.16/querying/functions/ ; https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ ; https://grafana.com/docs/grafana-cloud/observe-and-act/connect-externally-hosted/data-sources/prometheus/alerting/
  - Relevance: HIGH
  - Relationship: partly contradicts. Mapping missing data to Alerting or Normal is a guess WC-10 forbids; only Grafana's NoData (a distinct state) fits. The codebase rule governs: absence always gives "could not determine". The eviction warning extends the design: a session that drops out of a listing must not be reported as finished.
  - WC-10 / read-only: only the NoData option is WC-10 compatible. Read-only fit: yes (detection and labelling only).

### 5.5 Patterns from LLM agent session tools (Harmonograf, Camunda, unfetched product docs)

- **[EXTERNAL] Finding:** Harmonograf heartbeats carry a `progress_counter`; an unchanged nonzero counter across `STUCK_THRESHOLD` consecutive heartbeats on a running invocation is flagged, with a UI alert only and no restart. The ADR says "Stuck detection is a heuristic" and "Heartbeat can itself hang", and children's progress can mask a blocked parent.
  - Source: https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md
  - Relevance: HIGH
  - Relationship: supports that a liveness heartbeat says nothing about progress ("proves liveness, not completion", `orca-capabilities.md:130` [UNVERIFIED — Orca guide], as cited by web-01) and that even a progress flag is only a suspicion. Contradicts in naming: Harmonograf calls the flagged state "stuck", which the sweep must not equate with "stalled" (5.9, D3). The parent/child masking matches GQ-40 (nested workers).
  - WC-10 / read-only: WC-10 consistent only when labelled a suspicion (a note on a "working" or "could not determine" row). Alert-only fits Phase 1, but Orca exposes no progress counter today, so not buildable in Phase 1.
- **[EXTERNAL] Finding:** Camunda splits agent time into "Thinking", "Tool calling" and "Idle" (paused for outside input); execution duration excludes input-waiting time; "No single health indicator proves that an agent is stuck." At the limit an error is raised that an error boundary can route to a person.
  - Source: https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/
  - Relevance: HIGH
  - Relationship: supports "waiting on a person is healthy" (`worker-show --help` line 16; Section C rule 4, as cited by web-01) and QA finding N-41, recorded at GQ-61 (`gaps-and-questions.md:84`), that the window should bound activity only, not open Tasks or unread reports. N-41 is a QA finding, not an owner statement; the window length itself (6 h versus 72 h) is still an open owner decision (`seed-brief.md:79`; GQ-61, S9 row 51).
  - WC-10 / read-only: WC-10 consistent. The limit error and routing are actions, later-phase only. Phase 1 keeps person-wait time out of activity ages and the 6 h activity window; the waiting-on-a-person list prints the time since the wait began (R4).
- **[EXTERNAL] Finding (context only):** Simple Agent Manager separates "Needs input", provider-limit waits and stuck work; agents-fleet describes a coordinator watchdog with a stall notice and automatic abort.
  - Source: https://www.simple-agent-manager.org/docs/guides/session-troubleshooting/ ; https://docs.agents-fleet.ai/advanced/coordinator-resilience (search results only, not fetched)
  - Relevance: LOW
  - Relationship: the input-wait split supports the Camunda finding above; the automatic abort contradicts WC-10.
  - WC-10 / read-only: automatic abort is an action on suspicion, rejected for Phase 1 and not adopted later without Orca's stall proof. Not used as evidence for any design decision.

### 5.6 Status pages keep health, lifecycle and impact as separate fields (Atlassian Statuspage)

- **[EXTERNAL] Finding:** Statuspage component states are Operational, Under maintenance, Degraded performance, Partial outage and Major outage. There is no "unknown" component state, because a person sets every state.
  - Source: https://support.atlassian.com/statuspage/docs/what-is-a-component
  - Relevance: MEDIUM
  - Relationship: supports the #409 rule of keeping state dimensions independent; extends Statuspage, because an automated report needs the "could not determine" class that a person-set page lacks.
  - WC-10 / read-only: WC-10 consistent once "could not determine" is added. Read-only fit: yes.
- **[EXTERNAL] Finding:** incident lifecycle (Investigating, Identified, Monitoring, Resolved) is a field separate from component state, and impact is a third field.
  - Source: https://support.atlassian.com/statuspage/docs/what-is-statuspage/ ; https://support.atlassian.com/statuspage/docs/top-level-status-and-incident-impact-calculations
  - Relevance: HIGH
  - Relationship: supports keeping safe-to-close as its own dimension (GQ-68), not a class.
  - WC-10 / read-only: each dimension can be unknown on its own. A status page only reports, so it fits read-only.

### 5.7 Shift handover conventions (Google SRE, I-PASS, GitLab / PagerDuty)

- **[EXTERNAL] Finding:** the outgoing on-call engineer "sends a handoff email to the next engineer on-call"; incident response keeps a shared live incident document and hands over command explicitly. The workbook gives no field list for the email.
  - Source: https://sre.google/workbook/on-call/ ; https://sre.google/workbook/incident-response/
  - Relevance: MEDIUM
  - Relationship: supports the Shift Brief idea (`agent_focus.py:156-169`, as cited by web-02) but gives no layout.
  - WC-10 / read-only: a handover note is read-only by nature; fits Phase 1.
- **[EXTERNAL] Finding:** I-PASS clinical handover: Illness severity (stable / watcher / unstable), Patient summary, Action list (task, timeline, owner), Situation awareness and contingency ("if-then"), Synthesis by receiver.
  - Source: https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html (WebFetch returned 403; content from the search excerpt) ; https://www.jointcommissionjournal.com/article/S1553-7250%2817%2930176-9/abstract
  - Relevance: HIGH
  - Relationship: supports and extends. "Watcher" is a named in-between severity, the counterpart of reporting uncertainty instead of forcing stable or unstable. The owner-bearing action list matches the #409 owner and affected columns. "If-then" lets the report say what a person should check next. "Synthesis by receiver" has no static equivalent and points to a person confirming the report.
  - WC-10 / read-only: an if-then line is text only and starts no action, so it fits Phase 1.
- **[EXTERNAL] Finding:** GitLab and PagerDuty status updates carry a "Current Situation" and "Next status update expected by [time] UTC"; PagerDuty's status page has a "Time till Next Update" field.
  - Source: https://docs.pagerduty.com/ops-guides/incident-response-guide/incident-commander ; https://docs.pagerduty.com/incident-management/communicate/external-status-page ; https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/add-ai-tool-registry-design-doc/content/handbook/support/support-incident-response.md (handbook branch copy)
  - Relevance: MEDIUM
  - Relationship: extends. A dated report should state when its data was observed; #409 hardcodes its clock (`canvas.py:73-77`, as cited by web-02), so the sweep must print the real observation time. A static report has no next-update time unless the sweep is scheduled (GQ-10, GQ-61).
  - WC-10 / read-only: fits Phase 1; printing a time is presentation only.

### 5.8 Ordering and omission counts (Kanban Work Item Age, GitHub CLI)

- **[EXTERNAL] Finding:** Kanban Work Item Age (elapsed time from an item's start to now) is one of the four required flow metrics; daily review starts with the oldest in-flight item and asks what blocks it.
  - Source: https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf ; https://prokanban.org/blog/visualizing-flow-metrics---where-to-begin ; https://prokanban.org/kpg
  - Relevance: HIGH
  - Relationship: supports age-ranked ordering, which #409 documents but only partly codes (GQ-29). Extends it: a row with an unknown start time cannot be ranked honestly and goes in a labelled "age: could not determine" group, not at age 0.
  - WC-10 / read-only: ordering is presentation only; fits Phase 1.
- **[EXTERNAL] Finding:** `gh issue list` prints "Showing 30 of 624 open issues in cli/cli"; users asked for the total in `--json` because it was missing there.
  - Source: https://github.blog/developer-skills/github/how-to-level-up-your-git-game-with-github-cli/ ; https://github.com/cli/cli/issues/12196
  - Relevance: HIGH
  - Relationship: supports the #409 `shown/total` rule (`DESIGN-CONTRACT.md:11`, applied by `listbox()` and the wide Outcome Ledger and Revision Drift views, `agent_focus.py:17`, `:114`, `:127`; only the unbounded wide Attention Ledger and Shift Brief request lists print none; GQ-33) and shows machine-readable output needs the total too. Extends #409: when a source truncates without a total (the 100-row `check` cap, GQ-48), the honest form is "at least N, listing truncated: could not determine the total". No source found gives a form for an unknown total.
  - WC-10 / read-only: an unknown total is reported, not guessed; fits Phase 1.

### 5.9 Contradictions and rejected external patterns (codebase wins)

| # | External pattern | Source | Codebase rule | Outcome |
|---|---|---|---|---|
| D1 | Kubernetes taints and evicts after a node stays `Unknown` past its toleration (5.4) | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ | WC-10: absence never authorizes stop, retry or release (`WORKER-CONTRACT.md:45`, codebase rule; `orca-capabilities.md:125` [UNVERIFIED — Orca guide]) | Rejected for workers; recorded as a pattern the repo deliberately does not follow |
| D2 | Nagios KB: timeouts and DNS failures "should generally NOT be reported as UNKNOWN" (5.4) | https://support.nagios.com/kb/article.php?id=72 | Contact loss is `unverifiable`, reported "could not determine" | Codebase wins; domain differs (service outage versus agent progress) |
| D3 | Harmonograf labels a progress-free run "stuck" (5.5) | https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md | "stalled" needs positive stop proof (Section C rule 2) | Shown as a note, never as the stalled class |
| D4 | Kubernetes liveness probe restarts on probe failure (5.2) | https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ | Phase 1 never acts and never probes the agent's terminal (GQ-51) | Later phase only, and only with Orca's stall proof |
| D5 | Grafana No Data handling can map missing data to Alerting or Normal (5.4) | https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ | Absence always gives "could not determine" | Only the NoData option is compatible; Alerting / Normal / Keep Last State rejected |
| D6 | agents-fleet coordinator watchdog auto-aborts on stall (5.5) | https://docs.agents-fleet.ai/advanced/coordinator-resilience | WC-10; Phase 1 is read-only | Rejected; unfetched source, context only |

**Contradictions between external sources:**

| # | Conflict | Sources | Resolution for the sweep |
|---|---|---|---|
| C1 | Icinga reports a plugin's own timeout as UNKNOWN (web-02); the Nagios KB says socket timeouts should generally not be UNKNOWN (web-01) | https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/ ; https://support.nagios.com/kb/article.php?id=72 | Follow Icinga, because it matches WC-10: a read timeout is "could not determine" |
| C2 | The Kubernetes node-status page gives 50 s (`node-monitor-grace-period`) and also "40 second default timeout for unreachable nodes" | https://kubernetes.io/docs/reference/node/node-status/ | No effect: the sweep copies no timeout value from Kubernetes |

**Agreement across sources:** of the three stall heuristics (D1, D3, D4; row "Stall heuristics" in 4.8), only Kubernetes taint and eviction after `Unknown` (5.4, D1) contradicts WC-10; Harmonograf's "stuck" label (D3) is a naming note and the liveness-probe restart (D4) an action note, rejected as naming or action, not as contradictions of absence-is-not-death (synth-03 5.9). Outside the stall heuristics, Grafana's missing-data mapping (5.4, D5) and the agents-fleet auto-abort (5.5, D6, unfetched, context only) also contradict WC-10, and the Nagios KB timeout guidance (5.4, D2) differs in part because its domain differs (service outage versus agent progress). All are rejected (codebase wins). The remaining sources support WC-10's core claim: Kubernetes probe guidance (5.2), Pekko (5.3), Kubernetes node status at the status layer and Icinga (5.4) state it independently. No external source contradicts the verified #409 code (web-02).

**Rejected option A4 (extend sc-crash-recovery):** [CODE-CONTRADICTED] by codebase research. Neither web file evaluates it, and no external finding gives a reason to reopen it. It stays a rejected option.

### 5.10 External Research Summary

**Coverage of each file's Key External Findings:**

| File | Key External Finding | Reflected in |
|---|---|---|
| web-01 | 1. Supervisors act on positive exit evidence, not silence (OTP, Pekko, Kubernetes liveness warning) | 5.1, 5.2, 5.3 |
| web-01 | 2. "Unknown" is first-class in Kubernetes node status and gRPC health | 5.4 |
| web-01 | 3. Health has independent dimensions (liveness, readiness, startup) | 5.2 |
| web-01 | 4. Waiting for outside input is healthy and excluded from time budgets (Camunda) | 5.5 |
| web-01 | 5. Progress beats presence as a stuck signal, but is still a heuristic (Harmonograf, phi) | 5.3, 5.5 |
| web-01 | 6. Two kinds of unknown: health not known versus subject not known / check could not run | 5.4 |
| web-01 | 7. Every action-taking pattern is later-phase only; Phase 1 takes vocabulary and the report-not-act stance | 5.1-5.5, 5.9 |
| web-02 | 1. Icinga, Nagios, Kubernetes make "unknown" first-class, supporting WC-10 | 5.4 |
| web-02 | 2. Grafana's missing-data mapping contradicts WC-10; codebase wins | 5.4, 5.9 (D5) |
| web-02 | 3. Status pages keep health, lifecycle and impact separate, supporting safe-to-close as a dimension | 5.6 |
| web-02 | 4. Handover conventions (SRE, I-PASS): owner, action list, "watcher" state, if-then | 5.7 |
| web-02 | 5. Oldest-first ordering (Kanban Work Item Age); unknown ages need explicit placement | 5.8 |
| web-02 | 6. "Shown of total" is a CLI convention; no source gives a form for an unknown total | 5.8 |

No Key External Finding was excluded.

**Actionable statements for Phase 1 (all read-only, all WC-10 compliant):**

| # | Statement | Basis |
|---|---|---|
| R1 | Keep "could not determine" as an explicit class, and split its cause: (a) a row exists but evidence is absent (`unverifiable`, null-versus-absent `agentWait`); (b) the sweep could not read a source (Orca down, page failed, `unscanned:`), reported as a sweep failure | 5.4 (gRPC, Nagios, Icinga) |
| R2 | Tie "stalled" to Orca's positive proof only (Orca liveness `exited` or an Orca-observed exit, WC-10); a transcript final turn without `worker_done` is a note, never proof (departs from analysis F3, `analyze-worker-contract.md:34`, which allows it; reason in Section 2.3); show heartbeat age or any progress heuristic as a note column, never a class | 5.1, 5.3, 5.5 |
| R3 | Report a just-dispatched worker with no signal yet as "working" or "could not determine", never idle or stalled | 5.2 (startup probes) |
| R4 | Exclude person-wait time from activity ages and from the 6 h activity window. The waiting-on-a-person list is the exception: it prints and sorts on the question's original age, the time since the wait began (#409 keeps "original age" as a retained fact, `scope-04:87`) | 5.5 (Camunda); `scope-04:87` |
| R5 | Treat a read timeout or missing source as "could not determine"; never map absence to finished or stalled; a row that drops out of a listing is not evidence of finished | 5.4 (Icinga, Grafana) |
| R6 | Print the real observation time in the report header (#409 hardcodes its clock) | 5.7 (PagerDuty / GitLab) |
| R7 | Sort attention items oldest first by the time since the wait began (R4); rows with an unknown age go in a labelled group, not at age 0 | 5.8 (Kanban) |
| R8 | Every bounded list prints `shown/total`; a truncated source prints "at least N (truncated at 100), total could not determine" | 5.8 (GitHub CLI) |
| R9 | Optional: one if-then "what to check next" text line per waiting item, starting no action | 5.7 (I-PASS) |

**Not for Phase 1:**

| # | Statement | Basis |
|---|---|---|
| L1 | If automatic recovery is ever added, bound it OTP-style (restart budget per period, then escalate to the person) and gate every action on Orca's stall proof, never on `unverifiable` or a late heartbeat | 5.1, 5.2, 5.9 (D1) |
| L2 | Do not compute phi-accrual or progress-counter scores: Orca exposes no heartbeat history or progress counter (GQ-17 open), and the score could only rank suspicion | 5.3, 5.5 |

**Source reliability note:** most sources are official docs fetched with WebFetch. Fetched only partly or not at all: the Kubernetes probe page (first 100000 of 118034 characters), the phi-accrual paper (abstract only), the Pekko API page, the gRPC guide and the Kubernetes taint page (search results only), the AHRQ I-PASS page (403; search excerpt), and the two LOW product-doc sources in 5.5.

---

## 6. Options Analysis

### Constraints every option must meet

| # | Constraint | Source |
|---|---|---|
| K-1 | Read-only, and run by the coordinator only (the sweep goes on the never-as-worker list) | `seed-brief.md:53,57` via `research-notes.md:229` (owner constraints in `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md`, an input listed at `research-notes.md:44`; `:53` "First phase is read-only", `:57` "`/sc:sweep` is coordinator-only (never-as-worker list)", re-read in Phase 6 QA); `WORKER-CONTRACT.md:23`, `RULE_PHRASES["never-as-worker"]` / `NEVER_AS_WORKER` (`scope-01-contract.md`, `:245-254`) [CODE-VERIFIED]. The coordinator-only half is a contract rule, not a mechanical guard: `superclaude sweep run` has no caller check in this plan, and the K-4 tests prove read-only, not who calls it (steps 1.17-1.19) |
| K-2 | No new store; extend the contract instead | `seed-brief.md:54,56` via `research-notes.md:229` (`:54` "No new state store", `:56` "Extend the Orca coordinator/worker contract", re-read in Phase 6 QA) |
| K-3 | WC-10: a missing signal is never treated as death. Stalled requires positive proof only | `WORKER-CONTRACT.md:45` (`scope-01-contract.md`) [CODE-VERIFIED] |
| K-4 | Deterministic classification that can be tested with mocks | `seed-brief.md:62,68` via `research-notes.md:155-162` (`:62` "testable with mocks", `:68` "pure, deterministic and covered by mock-based tests", re-read in Phase 6 QA) |

The code and design precedents the options below cite (sc-issue "No CLI" and script layout, the swarm-wizard allowed-tools form, the reflect seam and its caller, the crash-recovery running-pipeline guard) are anchored in Section 2.4, "Precedents the options in Section 6 rest on".
| K-5 | Every Orca call stays inside the read allowlist. Forbidden: `check` in any form by default, `--ack`, `--wait`, `--unread`, reply, ask, send, `inbox`, `--agent-wait` | `scope-03-cli-patterns.md:99` (NB-2 plus NB-4); `message-check-handler.js:17,:30,:33-34,:58-71` [CODE-VERIFIED] (`06-orca-open-questions.md` Q2) |
| K-6 | Report on the #409 DERIVED skeleton. The sweep must add its own sort, because the #409 code has none, and must bound the request lists with a `shown/total` count: the two selected views' request lists are unbounded and print no count (`agent_focus.py:46-50`, `:164-167`), while other #409 views do print one (`:17`, `:114`, `:127`) | `scope-04-409-layout.md:268-304`; `agent_focus.py:46` [CODE-CONTRADICTED vs the #409 docs] |

### Option A1: Python CLI `superclaude sweep` plus a thin `/sc:sweep` command and `sc-sweep-protocol` skill

**Description:** All classification and probing lives in a new Python package under `src/superclaude/cli/`, which follows the `cli/reflect` split. The `/sc:sweep` command and the `sc-sweep-protocol` skill run `superclaude sweep run`; `report.py` renders and writes the dated report and the skill reads the result. The skill gathers no evidence itself (`research-notes.md:157`).

**How it works:**

```
/sc:sweep  (src/superclaude/commands/sweep.md, name: sweep)          [proposed]
   |  Skill call (blocking, per CLAUDE.md)
   v
sc-sweep-protocol  (src/superclaude/skills/sc-sweep-protocol/SKILL.md,
                    name: sc:sweep-protocol)                          [proposed]
   |  Bash: superclaude sweep ...          (PATH form first)
   |        uv run superclaude sweep ...   (dev checkout only; both in allowed-tools, B-19/NB-3)
   v
superclaude sweep  (Click group, two-line deferred import after main.py:561)
   |-- models.py          dataclasses
   |-- <pure classifier>  "No Click, no subprocess" (reflect/contract.py:7 pattern)
   |-- <probe module>     single _orca(*args) and _git(cwd, *args) seams,
   |                      timeout=10; seams raise, callers map to could not determine
   |                      (reflect/config.py:64-78 seam, :103-109 caller pattern)
   `-- commands.py        JSON echo; "[sweep ...]" stderr prefix + sys.exit(1) on error
   |
   v  read-only sources (allowlisted argv only)
   orca-ide orchestration worker-list --run --json (paged, page.nextCursor;
                                       no --include-remote until GQ-22 is measured)
   orca-ide orchestration worker-show / worker-read
   orca-ide orchestration task-list --ready --run / run-list / run-current / gate-list
   orca-ide worktree ps --json (no --agent-wait)
   <report-dir>/return-contract.yaml, progress.md ledger
   git status / log / branch / rev-parse / stash list
   ccsession topics/*.txt and orca-tabs read as files (never ccsession --list)
   |
   v
report.py renders and writes the dated static report (#409 DERIVED skeleton);
the skill only runs the CLI and reads the result (no Write in its allowed-tools)
```

Classification precedence, implemented in the pure module (`research-notes.md` Section C; `05-orca-row-schema.md:169-178`):

```
contract read (blocked -> waiting on a person, when the row is settled, the
               brief says "report blocked" or it is a Ruling halt; WC-3)
  -> stalled (proved)        positive proof only, and no consumer_fenced evidence
  -> fenced                  (WC-12)
  -> waiting on a person     (a) non-null agentWait  (b) frozen plan / policy / foreign ready Task
  -> working
  -> finished                Orca outcome settled AND contract read
  -> could not determine     everything else
idle: person-started sessions only.  safe-to-close: separate REVIEW dimension.
Never inputs: resource.terminalState, projection.stage.activity
```

| Aspect | Assessment |
|---|---|
| Effort | **L** ([UNVERIFIED] judgment; basis under "Effort basis" after the Options Comparison). New work: a package with four modules; a CliRunner test suite with the `_git` seam fixture (`tests/cli/reflect/conftest.py:58-80` pattern); a second `_orca` argv-allowlist test (B-13, `scope-03-cli-patterns.md:99`); a read-only proof test (`test_contract_status_cli.py:44-66` pattern); the registry entries listed under Files/systems affected; and the WC-14 text with its `RULE_PHRASES` pin |
| Risk | **Medium** ([UNVERIFIED] judgment from the open items below). Read-only is provable at the argv and local-filesystem level only: the argv allowlist is asserted at one seam; AssertionError side effects (`test_contract_status_cli.py:44-66` pattern) cover the subprocess and entry-point half only; the filesystem half is the new snapshot diff of step 1.11, with no in-repo precedent. Handler reads prove only what the CLI sends (`07-gate-gap-fill.md:8`), so runtime-side read-only needs the step 1.0a probe. Open runtime items: `exited` and `unverifiable` verdicts never captured (GQ-37, S9 row 32), which Section C rules 2 and 7 depend on; no populated `worker-list` row captured (G-A / GQ-01, S9 row 1); the `gate-list` to Approval mapping (GQ-34, S9 row 29); the cost of `--include-remote` (GQ-22, S9 row 17); whether the allowlisted Orca read verbs change runtime state (S9 row 79). Other open risks: (1) the bare PATH form under pipx is [UNVERIFIED] (GQ-25, `scope-03-cli-patterns.md:208`); (2) `make lint` must pass (lint-architecture checks, `Makefile:362-489`); check 11 compares `src/superclaude/cli/` with `superclaude.contracts` (`Makefile:467-470`), which holds no sweep vocabulary today (`ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`, `THRESHOLDS`, `RETURN_CONTRACTS` and roadmap ID families, `src/superclaude/contracts/__init__.py:64-254`), so it gives the sweep nothing to import and only forbids re-declaring those names; (3) it departs from the sc-issue "No CLI" decision (`docs/designs/sc-issue-command.md:384`; S2.4) |
| Reuse of existing code | `cli/reflect` module split (`reflect/contract.py:7,:397`; `reflect/config.py:64-78,103-109`) [CODE-VERIFIED]. Test fixtures and read-only proof (`tests/cli/reflect/conftest.py:58-80`; `test_contract_status_cli.py:44-66`) [CODE-VERIFIED]. `superclaude.contracts` has no sweep vocabulary to import (`contracts/__init__.py:64-254`); the class names and bounds are new constants in `sweep/models.py` (step 1.2). Skill-calls-CLI precedent: `sc-reflect-protocol/SKILL.md:63-64` calls `superclaude reflect contract-status`. Allowed-tools precedent: `sc-swarm-wizard-protocol/SKILL.md:7` (S2.4). From crash-recovery it reuses only the report shape and vocabulary, not its scripts: SAFE/REVIEW (`sc-crash-recovery/SKILL.md:91,93-97`), "What I could not determine" with `unscanned:` markers (`:139-150`; `report-template.md:127-129`), the conflicts section (`:120-125`) and the running-pipeline guard (`:137`). The transcript reader re-implements a tailing variant of `parse_session_log.py`, which today reads the whole file (`scope-02-orca-recovery.md`) |
| Files/systems affected | **New:** `src/superclaude/cli/sweep/` package; `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md`; tests under `tests/sweep/` (optional `tests/sweep/test_cli_registration.py`) and `tests/commands/test_sweep_command.py` (optional), per `scope-03-cli-patterns.md`. **Edited:** `src/superclaude/cli/main.py` (after `:561`, before the `__main__` guard at `:564-565`); `src/superclaude/core/WORKER-CONTRACT.md` (`:23` never-as-worker list; WC-14 after `:156` or `:129`); `tests/skills/test_worker_contract.py` `RULE_PHRASES` / `NEVER_AS_WORKER` (`:163`, `:245-254`); `_POST_REFRESH_ADDITIONS` (`tests/recommend/test_routing_refresh.py:33`, asserted `:647-648`); `src/superclaude/core/HOW-WE-WORK.md` "Other commands" (`:318-337`, the marker block) plus `_OTHER_COMMANDS` (`tests/core/test_how_we_work_routing_table.py:27-40,291-311`); plugin byte copy (`tests/commands/test_routing_plugin_parity.py:38`); `docs/user-guide/commands.md:105` UTILITIES table (whether a test pins it is [UNVERIFIED]). **Suite scans the new files must pass:** `test_model_alias_policy.py:81-100`, `test_graph_command.py:219-225`, the write-verb audit (`test_worker_contract.py:1090-1094`), `_check_no_unattended_sections` |
| Pros | Deterministic and mock-testable, as K-4 requires. Matches the house CLI pattern used by reflect and recommend. The single `_orca` seam is the natural home for the B-13 argv-allowlist test. Paging and one worker-show per row run in one process, not one model round trip per call (`research-notes.md:157`; batching policy). JSON output is reusable by later phases (`/sc:close`, resume) without re-parsing prose |
| Cons | Largest registry footprint: CLI registration plus routing and parity tests. The pipx PATH form is [UNVERIFIED]. It goes against the newest command precedent (sc-issue chose "No CLI", `docs/designs/sc-issue-command.md:384`; anchored in S2.4). The lazy-vs-eager package init is still undecided (GQ-23: `recommend/__init__.py:12-20` lazy vs `reflect/__init__.py:17-30` eager) |

### Option A2: Skill only (shell commands from the skill)

**Description:** `/sc:sweep` plus `sc-sweep-protocol` and no Python code. The skill calls each `orca-ide` verb, each git read and each file read through its own Bash or Read tool calls, and the model applies the Section C classification rules from the skill text. sc-crash-recovery is the precedent (`research-notes.md:158`).

**How it works:**

```
/sc:sweep -> sc-sweep-protocol/SKILL.md   (allowed-tools lists each read form)
   |
   |  model loop, one tool call per probe:
   |    Bash  orca-ide orchestration worker-list ... (repeat per page)
   |    Bash  orca-ide orchestration worker-show --dispatch <id>   (x N rows)
   |    Bash  git status / log ... per worktree
   |    Read  return-contract.yaml, progress.md per worktree
   v
model applies the Section C precedence in prose, then writes the report
```

| Aspect | Assessment |
|---|---|
| Effort | **M**. No package and no CLI registration. It still needs the command, the skill, the WORKER-CONTRACT never-as-worker and WC-14 edits with their `RULE_PHRASES` pin, the HOW-WE-WORK and plugin-parity registry entries, and the suite scans listed for A1 |
| Risk | **High.** (1) Classification is done by the model, is not deterministic and cannot be unit-tested with mocks, which breaks K-4 (`seed-brief.md:68`, `research-notes.md:158`). (2) Read-only rests only on the allowed-tools patterns. The direct precedent fails that test: `sc-crash-recovery/SKILL.md:4` allows `Bash(git stash *)` while `:13`/`:155` claim "pure read-only" (C3, S-08) [CODE-CONTRADICTED]. (3) The argv allowlist (K-5) can't be asserted at a seam; only glob patterns in allowed-tools constrain it. (4) Cost: worst case is ceil(N/100) worker-list calls plus N worker-show calls (`05-orca-row-schema.md:165`), and each one is a model round trip. Five or more serial known inspections fall under the batching policy, which moves them into a generated `/tmp` script. That script is an unreviewed classifier with no tests |
| Reuse of existing code | Skill shape, report template and SAFE/REVIEW vocabulary from `sc-crash-recovery` (`SKILL.md:91,93-97,:120-125,:139-150`; `report-template.md:127-129`). Allowed-tools precedent `sc-swarm-wizard-protocol/SKILL.md:7`. The class names and precedence rules live only as prose in the skill (`superclaude.contracts` has no sweep vocabulary for any option to import) |
| Files/systems affected | **New:** `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (plus `refs/`). **Edited:** `src/superclaude/core/WORKER-CONTRACT.md`; `tests/skills/test_worker_contract.py`; `src/superclaude/core/HOW-WE-WORK.md` with `tests/core/test_how_we_work_routing_table.py`; `tests/recommend/test_routing_refresh.py`; `tests/commands/test_routing_plugin_parity.py`; `docs/user-guide/commands.md:105` |
| Pros | Cheapest to write. No Python package, no CLI registry entry, no pipx PATH question. Matches crash-recovery, the skill closest in purpose |
| Cons | Fails K-4, the seed brief's mock-testable requirement. The read-only and allowlist guarantees are weaker. It scales poorly with session count. Repeated sweeps can classify the same evidence differently, which defeats a status report. Its only precedent is the skill whose read-only claim is [CODE-CONTRADICTED] |

### Option A3: Skill plus a skill-local standard-library script (sc-issue precedent)

**Description:** `/sc:sweep` plus `sc-sweep-protocol`, with the classifier and probes in a standard-library Python script under `src/superclaude/skills/sc-sweep-protocol/scripts/`. The script is installed to `~/.claude/skills/sc-sweep-protocol/scripts/` and run by the skill. The script layout follows `docs/designs/sc-issue-command.md:355-363`: SKILL.md under 500 lines, `refs/`, and `scripts/*.py` in the standard library only, tested directly (`:362-363,:395-396`; anchored in S2.4).

**How it works:**

```
/sc:sweep -> sc-sweep-protocol/SKILL.md
   |  Bash: python3 ~/.claude/skills/sc-sweep-protocol/scripts/<sweep script> --json
   |        (.claude/skills/... copy in a dev checkout; dual-surface rule)
   v
<sweep script>  (stdlib only; cannot import superclaude.*)
   |-- hand-rolled subprocess seam for orca-ide / git   (no _git helper to reuse)
   |-- classifier functions (Section C precedence)
   v
JSON -> skill writes the dated report
tests: import the script through a sys.path shim from the skill directory
```

| Aspect | Assessment |
|---|---|
| Effort | **M-L**. The classifier, paging, the argv-allowlist test and the read-only proof are the same work as in A1. It saves the CLI registration (`main.py:561`), but adds a test path shim and a hand-rolled subprocess seam. The registry edits are the same as A2 |
| Risk | **Medium.** Deterministic and testable, so it meets K-4. (1) The script cannot import package code (`research-notes.md:159`). Today that costs no shared constants: `superclaude.contracts` holds no sweep vocabulary (`contracts/__init__.py:64-254`) and check 11 scans only `src/superclaude/cli/` (`Makefile:467-470`), so neither A1 nor A3 has constants to import or copy. The cost is later: `/sc:close` and resume cannot import the classifier. (2) It runs from `~/.claude/skills/...`, which depends on the install copy and sync-dev being current. (3) The `_orca`/`_git` seam must be hand-rolled, with no `reflect/config.py` timeout and raise-then-map-to-fallback pattern (`:64-78`, `:103-109`) to inherit. (4) Interpreter choice: CLAUDE.md requires `uv run` for Python, and how a skill-local script is invoked outside a uv project is not settled by any research file [UNVERIFIED] |
| Reuse of existing code | sc-issue layout and testing approach (`docs/designs/sc-issue-command.md:355-363,:395-396`). Crash-recovery report shape and vocabulary, as in A1. It can't reuse the `cli/reflect` fixtures (`tests/cli/reflect/conftest.py:58-80`); `superclaude.contracts` has nothing sweep-related to reuse for either option |
| Files/systems affected | **New:** `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `refs/`, `scripts/<sweep script>.py`; tests with a path shim. **Edited:** the same registry and contract files as A2 (`src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`, `src/superclaude/core/HOW-WE-WORK.md`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`, `tests/commands/test_routing_plugin_parity.py`) |
| Pros | Testable and deterministic. No CLI registration. Matches the newest command precedent, sc-issue's "No CLI" (`docs/designs/sc-issue-command.md:384`). Ships inside the skill, so `superclaude` does not have to be on PATH, which avoids the pipx PATH question |
| Cons | No package imports, so later phases cannot import its classifier. A test path shim is needed. The seam is hand-rolled. The python3 vs `uv run` invocation is unsettled. Later phases (`/sc:close`, resume) would need their own scripts or would read this one's JSON. There is no shared module to extend |

### Option A4: Extend sc-crash-recovery (REJECTED, [CODE-CONTRADICTED])

**Description:** Add sweep behaviour to `src/superclaude/skills/sc-crash-recovery/`, reusing its investigators, `scripts/bootstrap_scan.sh` and its report template (`research-notes.md:160`).

**How it would work:** `/sc:crash-recovery --all`, or a new mode, would run `bootstrap_scan.sh` over the worktree root and fan out to investigators, then fill `report-template.md`.

**Why it is rejected.** Each reason below is a code fact that contradicts the claims the option relies on:

| # | Claim the option relies on | What the code shows | Evidence |
|---|---|---|---|
| R-1 | crash-recovery is read-only | allowed-tools includes `Bash(git stash *)`, and `:4` names a script under `~/workspace/IronClaude`. The "pure read-only, enforced by allowed-tools" claim at `:13`/`:155` is false | `sc-crash-recovery/SKILL.md:4,:13,:155` (C3, S-08, GQ-21) [CODE-CONTRADICTED] |
| R-2 | It scans where the worktrees are | Its `--all` mode hardcodes `~/workspace/...` (single-project mode uses the cwd, `:49-50`), with a 72 h default. This host's worktrees are under `~/workspaces/...` (host observation), and the sweep needs a 6 h activity window | `SKILL.md:25-26,:36,:53` (C4, S-09) [CODE-CONTRADICTED for `--all`] |
| R-3 | `bootstrap_scan.sh` finds Orca worktrees | It mis-encodes paths (`:31`), treats `.git` as a directory and so skips worktrees whose `.git` is a file (`:73`), and builds JSON by hand without escaping (`:136`) | `scope-02-orca-recovery.md` Q6 `:228`; K2/GQ-19 [CODE-VERIFIED bugs] |
| R-4 | Recovery and supervision fit one skill | Crash recovery is a post-crash, person-run tool. The sweep is coordinator-only (K-1) and goes on the never-as-worker list. Merging them mixes the two trigger models | `research-notes.md:160`; `WORKER-CONTRACT.md:23` |

| Aspect | Assessment |
|---|---|
| Effort | **M** to adapt, plus fixes to R-1 to R-3 that change crash-recovery for its existing users |
| Risk | **High.** Every read-only and path assumption is contradicted (R-1 to R-3) |
| Reuse of existing code | High on paper. In practice only the report shape and SAFE/REVIEW vocabulary are safe to reuse, and A1, A2 and A3 already take those without the scripts |
| Files/systems affected | `src/superclaude/skills/sc-crash-recovery/SKILL.md`, `scripts/bootstrap_scan.sh`, `report-template.md`, plus the contract and registry files |
| Pros | Investigators and report template already exist |
| Cons | Not read-only (R-1). Wrong root and window (R-2). Broken worktree scan (R-3). Mixes concerns (R-4) |

A4 is excluded from the comparison below. What it would have reused (the report shape, SAFE/REVIEW, "What I could not determine", the running-pipeline guard) is carried into every remaining option as text, not as scripts.

### Options Comparison

| Criterion | Option A1 (CLI + thin skill) | Option A2 (skill only) | Option A3 (skill + local script) |
|---|---|---|---|
| Effort | L: package, CLI registration, tests, registries | M: skill text and registries only | M-L: same classifier and tests as A1; no CLI registration; adds a path shim and a hand-rolled seam |
| Risk | Medium: argv-level and local-filesystem read-only provable at one seam. Open: GQ-37, G-A, GQ-34, GQ-22, Orca read-verb runtime side effects (S9 row 79, step 1.0a probe), pipx PATH form [UNVERIFIED] | High: not deterministic, fails K-4, allowlist enforced only by allowed-tools globs, one round trip per probe | Medium: testable, but depends on the installed skill copy, the seam is hand-rolled, and interpreter invocation is unsettled |
| Maintainability | High: pure classifier split from the single probe module (reflect pattern), importable by later phases | Low: rules live in prose and drift goes undetected by tests | Medium: tested, but the classifier cannot be imported by package code, so later phases copy it or read its JSON |
| Integration complexity | Highest registry count: `main.py`, routing tests, HOW-WE-WORK, plugin parity, contract pins. All are known, test-pinned paths | Lowest: command and skill plus the shared registries | Medium: shared registries plus install-path dependency (`~/.claude/skills/...` vs `.claude/skills/...` dual surface) |
| Reuse potential | High: JSON CLI and modules can be imported by later phases (`/sc:close`, resume) and by other CLI groups | Low: nothing callable is produced | Medium: script JSON is reusable; the code cannot be imported by package code |
| Meets K-1..K-6 | All, with K-4 and K-5 enforced by tests | Fails K-4; K-5 weak | All, with K-4 and K-5 by tests |

**Effort basis.** The Effort grades (A1 L, A2 M, A3 M-L, A4 M) are [UNVERIFIED] judgment: relative sizes from the steps and files each option touches, not hour estimates. A1's Phase 1 plan (Section 8) has 34 steps: 1.0 2 (the runtime read-only probe and the owner-decisions gate), 1A 7 (six new source files, one new test file, the `main.py` registration), 1B 6, 1C 3, 1D 4, 1E 7 (including the developer-guide copy and the CHANGELOG entry, steps 1.24a and 1.24b), 1F 5. A2 drops 1A and most of 1B; A3 keeps 1B's classifier, allowlist and read-only tests but drops step 1.7. No research file gives hours, so the grades cannot be compared with the issue's "about 20" hours for `/sc:sweep` with the static report (`.dev/issues/339/issue-summary.md:6`); the per-sub-block hour estimate and any scope cut are S9 row 81d. The recommendation does not rest on effort: A1 is chosen on K-4, K-5 and reuse (Section 7), and it accepts the highest effort as a trade-off.

---

## 7. Recommendation

**Recommended option: A1.** It is a Python CLI `superclaude sweep` with a pure classifier and one probe module, called by a thin `/sc:sweep` command and the `sc-sweep-protocol` skill. It reuses crash-recovery's report shape and SAFE/REVIEW vocabulary, but not its scripts. The plan uses working defaults for five open owner decisions (GQ-10, GQ-11, GQ-35, GQ-61, GQ-63; GQ-09, person-started sessions, is settled by the sources, Section 3.1 G6); Phase 1 step 1.0b asks for them, and reads APPROVED.md (GQ-100), before any code step, and names the steps each one blocks.

### Rationale (from the comparison)

| Deciding criterion | Why A1 wins on it | Runner-up and gap |
|---|---|---|
| K-4 mock-testable (hard requirement) | Reflect precedent for the mockable parts: CliRunner, and `config.py` routes all of its git calls through one `_git` seam (`config.py:64-78`, used at `:104`; fixture `tests/cli/reflect/conftest.py:58-80`), while `commands.py:570-577` (tmux) and `runner.py:31` (`ClaudeProcess`) start processes outside it; `side_effect=AssertionError` patches proving that entry points are not reached (`tests/cli/reflect/test_contract_status_cli.py:44-66`) [CODE-VERIFIED]. That pattern covers the subprocess and entry-point half only; filesystem read-only is the new snapshot diff of step 1.11, with no in-repo precedent | A3 also meets it, at the cost of a path shim. A2 fails it and is out |
| K-5 argv allowlist (read-only safety) | One `_orca(*args)` seam, so a single test can assert every argv against the NB-4 allowlist (`scope-03-cli-patterns.md:99`). This proves argv-level read-only only; runtime-side effects of the read verbs are probed once in step 1.0a (`07-gate-gap-fill.md:8`; S9 row 79) | A3 can do the same, but the seam is hand-rolled |
| Risk | Medium. Open runtime items: GQ-37 (`exited`/`unverifiable` never captured), G-A (no populated `worker-list` row), GQ-34 (`gate-list` mapping), GQ-22 (`--include-remote` cost), Orca read-verb side effects (S9 row 79), and the pipx PATH form (GQ-25, with a dev-checkout fallback already in allowed-tools). The Orca items bear on A3 equally; they do not separate the options | A3 is Medium: installed-copy dependency, hand-rolled seam, unsettled interpreter |
| Maintainability | The classifier is pure, separate from probes, and importable by later phases | A3's classifier cannot be imported by package code |
| Reuse potential | Later phases (`/sc:close`, resume) get an importable module and a JSON CLI | A3 offers only script JSON |

**Trade-offs accepted:**

| Trade-off | Accepted because | Mitigation |
|---|---|---|
| Highest effort (L, [UNVERIFIED] judgment, Effort basis in Section 6; hours are S9 row 81d) and registry count | Every registry is a known, test-pinned path. Effort over A3 is mostly registration, not logic | Follow the scope-03 checklist: `main.py:561`; `tests/recommend/test_routing_refresh.py:33`; `tests/core/test_how_we_work_routing_table.py:27-40`; `tests/commands/test_routing_plugin_parity.py:38` |
| Departs from sc-issue "No CLI" (`docs/designs/sc-issue-command.md:384`; S2.4) | sc-issue has no Orca probe surface needing an argv allowlist asserted at one tested seam. The sweep needs one (K-5), and later phases need an importable classifier | Record the departure and its reason in the plan |
| pipx PATH form [UNVERIFIED] | The decision is already made (B-19/NB-3: PATH first, `uv run` in a dev checkout, both in allowed-tools) | Run `superclaude sweep --help` once outside a uv project before release (GQ-25) |

**Contradictions this choice depends on, with the stronger evidence:**

| # | Conflict | Stronger evidence | Effect on A1 |
|---|---|---|---|
| X-1 | crash-recovery says "pure read-only" (`SKILL.md:13,:155`), but `Bash(git stash *)` is allowed (`:4`) | Code (`:4`) [CODE-CONTRADICTED claim] | A1 reuses no crash-recovery scripts or allowed-tools. Its git list allows `stash list` only |
| X-2 | `~/workspace` in crash-recovery vs `~/workspaces` on this host (C4) | Host layout | A1 takes worktree paths from Orca and `--root`, not from a hardcoded root; with Orca down only the `--root` scan of `.dev/tasks/{to-do,done}/*/` remains (step 1.4) |
| X-3 | sc-issue "No CLI" vs A1's CLI | Not a factual conflict. A design choice, decided by K-4/K-5 above | See trade-offs |
| X-4 | Help: null `agentWait` = "looked, found no wait". Guide: null = "absence seen again" (`06-orca-open-questions.md` Gap 19 `:144`) | Open. The help is code-verified text; the guide's reading is the safer one for stop decisions | The classifier uses the split rule: null is valid input for working but never stall proof, and absent means could not determine |
| X-5 | `scope-03-cli-patterns.md:99` writes bare `worker-list`; C13 requires `orca-ide orchestration <verb>` | C13 (`research-notes.md:331`) | The allowlist test asserts the full `orca-ide orchestration <verb>` argv |
| X-6 | Resolved, not a live conflict: `gaps-and-questions.md:125` reads "Open: 75. Resolved: 25" with GQ-03 counted as resolved | `gaps-and-questions.md:125` | None on the option choice |

### Recommended approach (steps are in Section 8, context in Section 5)

Build A1 as one Python package, `src/superclaude/cli/sweep/` (`models.py`, the pure classifier `classify.py`, the probe module `probes.py`, `report.py`, `commands.py`), registered in `src/superclaude/cli/main.py`. `report.py` renders and writes the dated report; the `/sc:sweep` command and the `sc-sweep-protocol` skill only run the CLI and read its result, so `Write` stays out of the skill's `allowed-tools`. Add the WC-14 coordinator-loop rule and the never-as-worker entry to `src/superclaude/core/WORKER-CONTRACT.md`, then the routing registries (including the HOW-WE-WORK "Other commands" table, `src/superclaude/core/HOW-WE-WORK.md:318-337`) and the gates.

- The ordered steps, files, tests and acceptance checks are Section 8, Phase 1 (steps 1.0a-1.29). This section does not repeat them.
- The runtime context the design depends on (Orca surfaces, contract rules, report conventions) is Section 5.

[CONTRADICTION: Component A (`synthesis/synth-04-options-recommendation.md`, Option A1 "Files affected" and Step 6) cites the HOW-WE-WORK "Other commands" table as `src/superclaude/core/HOW-WE-WORK.md:314-337`.
Component B (`synthesis/synth-01-problem-current-state.md` 2.4 and `synthesis/synth-02-target-gaps.md` SC-11) cites it as `:318-337`. `synthesis/synth-05-implementation-plan.md` names the file without a line range.
Both versions presented for QA resolution.]

Resolution (Phase 6 QA, P6-06): the report now cites `:318-337` (the `<!-- other-commands:v1 -->` marker block) in Option A1 "Files affected" and in the Recommended approach above. Both ranges cover the table: `:314` is the "## Other commands" heading, `:318` the opening marker and `:337` the closing marker (`src/superclaude/core/HOW-WE-WORK.md`, read in Phase 6). The marker block is the range a test or an edit touches, so it is used.

### External context (option-neutral)

These web findings shape the vocabulary and report rules that every option would implement. They do not separate A1 from A3.

| Finding | Source (external context) | Applies as |
|---|---|---|
| "Unknown" is a first-class state, separate from unhealthy | https://kubernetes.io/docs/reference/node/node-status/ ; https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto ; https://nagios-plugins.org/doc/guidelines.html | "could not determine" stays its own class. The cause is split between evidence absent and a source unreadable (web-01 rec. 1) |
| Act on positive exit proof, never on silence | https://www.erlang.org/doc/system/sup_princ.html ; https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ ; https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html | Supports WC-10. Heartbeat or progress age is a note column only, never a class (web-01 rec. 2) |
| Waiting for a person is healthy and is excluded from time budgets | https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ | Person-wait time is excluded from the 6 h activity window (web-01 rec. 4) |
| Oldest first; unknown age goes in a labelled group | https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf | The sweep's own sort (K-6) |
| `shown/total`; "at least N, truncated" when the total is unknown | https://github.com/cli/cli/issues/12196 | Extends #409, which has no unknown-total form |
| Grafana's no-data-as-OK mapping | (web-02 finding 2) | Rejected, because it conflicts with WC-10 |
| Restart, kill, evict and retry patterns | web-01 finding 7, rec. 5 | Later phases only, not Phase 1 |

### 7.1 Open Questions for the option choice (rows keyed to Section 9, the canonical list)

(UNVERIFIED items that affect the option or its build.)

| S9 row | Question | Source | Blocks |
|---|---|---|---|
| S9 row 20 | Does the bare `superclaude sweep` PATH form work under a pipx install? | GQ-25; `scope-03-cli-patterns.md:208` | Release check only |
| S9 row 18 | Lazy (`recommend/__init__.py:12-20`) or eager (`reflect/__init__.py:17-30`) package init? | GQ-23, K4 | Step 1 detail |
| S9 row 1 | What does a populated worker-list row carry? Until it is captured, plan for ceil(N/100) list calls plus N worker-show calls | `05-orca-row-schema.md:186`; G-A, C10 | Probe cost, not the option |
| S9 row 2 | Is there a non-consuming question read? Today: Orca question enumeration is "could not determine", and the header states partial message coverage | `06-orca-open-questions.md` Gaps 17-18; G-B, C11 | The sweep stays on the contracts-only fallback |
| S9 row 42 | Does the `--agent-wait` / `agentWait` probe send anything to the agent's terminal? | `06-orca-open-questions.md` Gap 10; GQ-51 | `--agent-wait` stays excluded |
| S9 row 23 | Is the `docs/user-guide/commands.md:105` UTILITIES table test-pinned? | `scope-03-cli-patterns.md`; GQ-28 | Step 6 |
| S9 row 21 | How do command-level and skill-level allowed-tools combine? | `scope-03-cli-patterns.md` OQ; GQ-26 | Step 4 |
| S9 row 39 | Does `inbox` mark rows read at runtime? | `06-orca-open-questions.md` Gap 4; GQ-46 | `inbox` stays forbidden |
| S9 row 29 | `gate-list` status to Approval mapping | GQ-34; `scope-04-409-layout.md:345` | Report column only |
| S9 row 15 | Fix `bootstrap_scan.sh` or write a new scanner? (A1 writes its own probes; this concerns crash-recovery only) | GQ-19, K2 | Not A1 |

### 7.2 Coverage and exclusions (synth-04)

| Input | Key findings reflected | Excluded here, and why |
|---|---|---|
| `scope-01-contract.md` | Never-as-worker list, WC-10, WC-14 placement and pinning, repo-setup gate | WC-3/6/8/9/12/13 rule text and G1-G7 gap detail belong to the contract synthesis section, not the option choice |
| `scope-02-orca-recovery.md` | Crash-recovery reuse limits, bootstrap bugs, the `parse_session_log.py` tail change | Orca failure-mode handling (`runtime_unavailable` banner, `source_changed` restart) applies to every option equally |
| `scope-03-cli-patterns.md` | Module split, registration, seams, allowlist, registries, lint, open questions | None |
| `scope-04-409-layout.md` | DERIVED skeleton, missing sort and omission count, partial message coverage | Field names and buckets are not fixed and do not separate the options |
| `05-orca-row-schema.md` | Worst-case cost, Section C Orca half, no `terminalState` or `stage.activity` | Liveness reason codes (guide-only, [UNVERIFIED]) |
| `06-orca-open-questions.md` | `check` is a mutation call, `--unread` forbidden, `inbox` unused, `--agent-wait` excluded, null vs absent `agentWait` | Peer-session `reference find` detail is option-neutral |
| `web-01`, `web-02` | External context table above | None |
| `gaps-and-questions.md` | GQ-03 (resolved), GQ-19, GQ-21, GQ-23, GQ-25, GQ-34, GQ-60, K2-K4, C3/C4, S-08/S-09 | Rows unrelated to where the logic lives |
| `research-notes.md` SOLUTION_RESEARCH | A1-A4 table, B/C/D data, provisional recommendation `:227`, constraint alignment `:229` | None |

---

## 8. Implementation Plan

Plan for **A1**: a Python CLI `superclaude sweep` (Click group in a new package `src/superclaude/cli/sweep/`), called by a thin command `/sc:sweep` and its skill `sc:sweep-protocol`, plus the WC-14 coordinator-loop rule. A pure classifier, a probe module with single `_orca` / `_git` seams, and a report renderer are tested with mocks; argv-level read-only behaviour is proved with the argv allowlist test, and the subprocess and entry-point half with the `side_effect=AssertionError` pattern (`test_contract_status_cli.py:44-66`, which patches entry points only); local-filesystem read-only is proved by the new snapshot diff of step 1.11, which has no in-repo precedent; runtime-side read-only of the Orca read verbs is probed once before the build (step 1.0a; `07-gate-gap-fill.md:8`).

Option A4 (extend `sc-crash-recovery`) is **rejected** [CODE-CONTRADICTED]: its allowed-tools hold `Bash(git stash *)` (`sc-crash-recovery/SKILL.md:4`), so it is not "pure read-only" (`SKILL.md:13`, `:155`; C3); its `--all` mode and one dev-fallback allowlist entry hardcode `~/workspace/...` while this host's worktrees are under `~/workspaces/...` (`SKILL.md:4`, `:25`, `:36`, `:53`; single-project mode uses the cwd, `:49-50`; C4); its default window is 72 h, not 6 h; and `bootstrap_scan.sh` mis-encodes project paths (`:31`), reports every Orca worktree as not a repo because `.git` is a file there (`:73`, `:82`), and hand-builds JSON (`:136`) (scope-02 `:130-149`, `:241`).

```
 coordinator session (never a worker: WORKER-CONTRACT.md:23)
        |
        v
 /sc:sweep  --->  Skill sc:sweep-protocol  --->  superclaude sweep run   (PATH first,
 (commands/sweep.md)   (skills/sc-sweep-protocol)      |                   then uv run)
                                                       v
                            cli/sweep/commands.py  (Click; JSON on stdout; [sweep ...] errors)
                              |            |                    |
                              v            v                    v
                       probes.py      classify.py          report.py
                  _orca(*args)        pure, no Click,      #409-layout Markdown,
                  _git(cwd, *args)    no subprocess        the ONLY write (--output)
                  file readers        Section C precedence
                  (allowlist,         + safe-to-close
                   timeout 10,        dimension
                   seams raise;
                   callers map to
                   could not determine)
```

### Phase 1: read-only `/sc:sweep`, registries, static report, WC-14

**Goal.** Ship a coordinator-only, read-only sweep that lists every session and worktree the coordinator can see, classifies each with the Section C precedence, prints safe-to-close as a separate REVIEW dimension, writes one dated Markdown report on the #409 layout, and pins the WC-14 coordinator-loop rule in the worker contract (gaps G1 to G7, G-A, G-B, K1 to K4; success criteria SC-1 to SC-16 in synth-02 3.2).

**Dependencies.**

| Dependency | Status | Evidence |
|---|---|---|
| Click CLI with deferred subcommand registration | exists | `src/superclaude/cli/main.py:555-561` (init-lite, reflect), `__main__` guard `:564-565` [CODE-VERIFIED] |
| Pure-module and seam patterns to copy | exist | `src/superclaude/cli/reflect/contract.py:7`, `:397`; `src/superclaude/cli/reflect/config.py:64-78`, `:103-109`; `src/superclaude/cli/recommend/__init__.py:12-20` (scope-03) [CODE-VERIFIED] |
| Read-only test patterns | exist | `tests/cli/reflect/test_contract_status_cli.py:44-66` (docstring `:18-22`); `tests/cli/reflect/conftest.py:17`, `:58-80`; `tests/recommend/test_cli_registration.py:1-39`; `tests/commands/test_issue_command.py:1-60` [CODE-VERIFIED] |
| Contract constants | exist | `RETURN_CONTRACTS` in `src/superclaude/contracts/__init__.py:204-206`; lint Check 11 forbids redeclaring them under `src/superclaude/cli/` (`Makefile:467-476`) [CODE-VERIFIED]. None of them is sweep vocabulary (`contracts/__init__.py:64-254`), so the sweep defines its own constants in `models.py` and must only avoid re-declaring these names |
| Worker contract and its pins | exist | `src/superclaude/core/WORKER-CONTRACT.md` (WC-2 to WC-13; WC-1 unused; no WC-14 today; `scope-01-contract.md:50`); `tests/skills/test_worker_contract.py` [CODE-VERIFIED] |
| Orca CLI 1.4.245 read verbs | exist on the host | help text and captures in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/` (`lc16-show-4.json`, `lc17-show-1.json`, `lc01-show-1.json`, `lc01-step7.txt`) [CODE-VERIFIED shapes; populated worker-list row UNVERIFIED] |
| #409 layout | unmerged, pinned | commit `495eb96d` (`canvas.py:73-81`, `layouts/agent_focus.py:44-53`, `:156-169`, `data-dictionary.md:12-28`, `DESIGN-CONTRACT.md:11`) [CODE-VERIFIED at that commit]. Gate: when #409 merges, re-diff those files against `495eb96d` and update the step 1.5 skeleton before the report tests (step 1.16a) |
| PR #422 | open; edits `WORKER-CONTRACT.md` (`.dev/issues/339/issue-summary.md:27`; analysis F8, `research-notes.md:307`) | Gates steps 1.17-1.19 (WC-14, never-as-worker line, contract pins): land them only after #422 is merged and this branch is rebased onto it, or keep the first PR to new files only and move 1.17-1.19 to a follow-up PR (GQ-62, S9 row 52). Whether #422 also touches the registry files of steps 1.21-1.23 is not checked; step 1.16a lists #422's files and gates any overlap the same way |

#### 1.0 Pre-build checks (before 1A)

| Step | Action | Files | Details |
|---|---|---|---|
| 1.0a | Probe runtime-side read-only of the Orca read verbs | none in the repo; result in the task package `artifacts/readonly-probe.md` | Why: the read-only tests (steps 1.10, 1.11) prove argv-level and local-filesystem read-only only; a handler read proves what the CLI sends, not what the runtime does (`research/07-gate-gap-fill.md:8`; S9 row 79). Probe (plan decision, new design): on a throwaway Run with one settled worker, record `worker-show --dispatch <id> --json` and `task-list --run <id> --json`; run `worker-list --run <id> --json`, `worker-show --dispatch <id> --json`, `worker-read --source transcript` twice in a row and `worktree ps --json`; record the same two reads again. Pass = the before and after records are identical apart from timestamps, and the second `worker-read` returns the same content as the first (no cursor advance). On a fail, the failing verb leaves the default allowlist (steps 1.4, 1.10) and the finding goes to Open Questions before 1A starts. |
| 1.0b | Owner decisions gate and APPROVED.md read | none in the repo; record in the task package `artifacts/owner-decisions.md` | Why: Phase 1 builds on open owner decisions as working defaults (`gaps-and-questions.md` GQ-10, GQ-11, GQ-35, GQ-61, GQ-63 all "open"; GQ-09 is also marked open there, but the sources settle it, Section 3.1 G6, so it is not asked). Before 1A, read `.dev/orca-command-refactor/decisions/APPROVED.md` (D1-D5; never read by any scope, `research-notes.md:42`; GQ-100, S9 row 64), then ask the owner for each decision and record the answer or "working default accepted". Each decision blocks only the steps named: GQ-10 report directory (S9 row 8) blocks the `--output` default of step 1.6; GQ-11 rule ID (S9 row 9), with the WC-14 wording, is a hard gate: steps 1.17-1.19 do not start until the owner's answer on GQ-11 is recorded; "working default accepted" counts only when the owner says it; GQ-35 layout pin (S9 row 30) blocks the step 1.5 skeleton; GQ-61 window (S9 row 51) blocks the `--window` default of step 1.6 and the step 1.5 / 1.12 window rules; GQ-63 DONE/NEXT exemption (S9 row 53) blocks the step 1.5 report format. A decision that differs from the working default changes the named steps before they start; other unanswered decisions (all except GQ-11) keep the working default and stay in S9. |

#### 1A. Package, classifier, probes, report, CLI

| Step | Action | Files | Details |
|---|---|---|---|
| 1.1 | Create the package with a lazy export | `src/superclaude/cli/sweep/` (new), `src/superclaude/cli/sweep/__init__.py` (new) | Lazy `__getattr__` export of `sweep_group`, following `src/superclaude/cli/recommend/__init__.py:12-20` (scope-03 recommends lazy over the eager `reflect/__init__.py:17-30`; K4 / GQ-23). No Orca client is started at import. |
| 1.2 | Define the data model | `src/superclaude/cli/sweep/models.py` (new) | Frozen dataclasses and constants (names, types and the string decision are plan decisions, new design). Class names are plain `str` constants, not an `Enum`, because the JSON and the report print them as they are: `WAITING_ON_PERSON = "waiting on a person"`, `WORKING = "working"`, `STALLED_PROVED = "stalled (proved)"`, `COULD_NOT_DETERMINE = "could not determine"`, `FINISHED = "finished"`, `IDLE = "idle"`, `FENCED = "fenced"`, collected in `CLASS_NAMES: tuple[str, ...]`; `UNKNOWN = "unknown"` and `NOT_OBSERVED = "not observed"`. `OrcaObservation`: `liveness_verdict: str | None`, `status: str | None`, `outcome: str | None`, `agent_wait: object | None`, `agent_wait_present: bool` (null versus absent, GQ-58), `parent: str | None`, `worktree_path: Path | None`, `body_text: str | None` (for "guard refused:"), and, read by step 1.3 rule (ii) and the terminal-releasable half of safe-to-close only, never to set the class (plan decision, new design): `unsupervised: bool | None` (context-only Dispatch, Section 3.1; None while the JSON field that marks it is not captured, so only synthetic fixtures set it in Phase 1), `terminal_state: str | None` (`resource.terminalState`, e.g. `reclaimable`, `retained`) and `next_action: str | None` (`nextAction`, e.g. `release`; `lc17-show-1.json`). `ContractRecord`: `path: Path`, `worker_status: str`, `blocked_question: str | None`, `reason: str | None`. `SessionRow`: `id: str`, `person_started: bool`, `orca: OrcaObservation | None`, `transcript_path: Path | None`, `last_activity: datetime | None`, then the ten #409 dimensions of `data-dictionary.md:19-28` (values per `scope-04-409-layout.md:181-190`) as `str` fields defaulting to `UNKNOWN`: `lifecycle` (running / settled / unknown), `phase` (work / review / queue / dependency), `health` (no issue observed / failed result / unknown), `approval` (none observed / human decision observed), `freshness` (fresh / stale) with `freshness_age_s: int | None`, `result` (succeeded / partial / failed / null), `admission` (admitted / not admitted), `evidence_packet` (complete packet / partial packet; named so it does not clash with the derived `evidence`), `policy` (frozen / not frozen), `tests_review: str | None` (null = unavailable); then the derived `classification: Classification | None` and `safe: SafeToClose | None`, set after step 1.3. `Classification`: `cls: str` (one of `CLASS_NAMES`), `waiting_kind: str | None` ("a" or "b"), `evidence: str`, `notes: tuple[str, ...]`. `WorktreeState`: `path: Path`, `uncommitted: bool | None`, `unmerged: bool | None`, `ledger_unfinished: bool | None`, `frozen: bool | None`, `unpushed: bool | None` (ahead of upstream or no upstream), `dev_tasks_unsaved: bool | None` (untracked or unstaged path under `.dev/tasks/`) (None = could not determine); and, for step 1.3 rules (i) and (iii) (plan decision, new design): `package_ids: tuple[str, ...]` (ids of the packages the step 1.4 disk reader finds under this root's `.dev/tasks/{to-do,done}/*/`), `archive_states: tuple[tuple[str, str], ...]` ((package id, "archive-blocked" or "interrupted archive") pairs from the step 1.4 ledger read and `.archiving` check; empty when none; a tuple rather than one `str | None` because one worktree can hold several packages in different states), and `shared_package_ids: tuple[str, ...]` (ids also found under another root; empty until the step 1.3 pre-pass sets it). `SafeToClose`: `terminal: str` and `worktree: str` (each "yes", "no" or `COULD_NOT_DETERMINE`), `reason: str`. `SourceCoverage`: `name: str`, `coverage: str`, `age_seconds: int | None`, `unscanned: str | None`. Step 1.6 flattens `classification` into the row keys `cls`, `evidence`, `notes` and `safe` into `safe_to_close`. The seven canonical class names of `research-notes.md` Section C (B-28): the question's six (including idle) plus fenced (rule 3, `research-notes.md:194`); precedence rules 1-7 assign the six Orca-row names (rules 1 and 4 both give waiting on a person) and idle is set only for person-started sessions (`:202`); a two-part safe-to-close value (terminal releasable; worktree removable); a source-coverage record (name, coverage, age, `unscanned:` reason). Unknown prints "unknown", missing results "not observed" (`scope-04:295`). |
| 1.3 | Write the pure classifier | `src/superclaude/cli/sweep/classify.py` (new) | "No Click, no subprocess", as `reflect/contract.py:7`, `:397`. Public functions (plan decision, new design): `classify(row: SessionRow, contract: ContractRecord | None, now: datetime) -> Classification` and `safe_to_close(row: SessionRow, worktree: WorktreeState | None) -> SafeToClose`, plus the pre-pass `mark_shared_packages(worktrees: list[WorktreeState]) -> list[WorktreeState]`, pure, which returns `dataclasses.replace` copies with `shared_package_ids` set to every id in `package_ids` that also appears under another root; `commands.py` calls it once over all worktree records after the step 1.4 probes and before any `safe_to_close` call, so `safe_to_close` keeps its one-worktree signature; every type named here is a dataclass in `models.py` (step 1.2), and `now` is injected so tests fix the clock. `classify` applies the Section C precedence (`research-notes.md:190-202`): (1) contract `worker_status: blocked` -> waiting on a person (a), only when the Orca row is settled, the brief's policy line is `On a blocked gate: report blocked` (the default), or the contract is an `/sc:implement` Ruling halt (`reason` `E-HALT-QA` or `E-NO-RULING`; WC-3 `WORKER-CONTRACT.md:56`: never asked, reported blocked whatever the policy line says) ("rule 1's condition"); under `ask the coordinator` a live, unsettled row may be asking the coordinator or re-running the command in the same session, and the second contract replaces the blocked one whole (WC-3, `WORKER-CONTRACT.md:54-55`), so such a row skips rule 1 and gets working (rule 5) or could not determine (rule 7) with the note "blocked contract under ask the coordinator; may be re-running" (the policy line is read from the Task spec; when it cannot be read, a live row with a blocked contract is could not determine with that note); (2) Orca `liveness.verdict` exited or an Orca-observed exit (WC-10 accepts only Orca's stall proofs, `WORKER-CONTRACT.md:45`; a transcript final turn without Orca proof gives (7) with a note, a deliberate departure from analysis F3, `analyze-worker-contract.md:34`, reason in Section 2.3), with no `worker_done` **and** no `consumer_fenced` evidence -> stalled (proved) (`exited` is guide text only and has never been captured, GQ-37 [UNVERIFIED]; this rule is built against synthetic `exited` fixtures, step 1.8, and the live-capture check stays in Open Questions, 8.2); (3) `consumer_fenced` -> fenced (WC-12, `WORKER-CONTRACT.md:60`). Rule 3 is not buildable from a named field in Phase 1: Section C names the worker's transcript or its `check` result as the evidence (`research-notes.md:193-194`), `check` is never called (SC-2), no transcript literal for fencing has been captured, and no step 1.4 probe returns a fencing field. Phase 1 builds rule 3 against synthetic fixtures only (step 1.8); on live rows the fenced check cannot be made, so an exited or settled row with no `worker_done` is could not determine with the note "fenced evidence not readable" (the GQ-84 rule), never stalled (S9 row 81a); (4) non-null `observation.agentWait` -> (a), frozen `/sc:implement` plan or Ruling halt (`WORKER-CONTRACT.md:133-136`) or a foreign ready Task (`:129`) -> (b). The policy dimension ("policy: frozen / not frozen", `data-dictionary.md:27`; `research-notes.md:197`) is computed for every row independently of the class (GQ-96: the dimensions are independent): a blocked implement contract that meets rule 1's condition gets class waiting on a person (a) from rule 1 and policy frozen, and is listed under (b) too. The `ask the coordinator` skip covers the contract halves of 4a and 4b-contract as well: rule 4's contract sub-cases apply only when rule 1 would have applied, so a skipped blocked contract gets no class from 4a or 4b-contract and its policy prints "could not determine" with the "may be re-running" note, never "not frozen" (the freeze rule `WORKER-CONTRACT.md:133` reads the latest contract, which WC-3 `:54` says the re-run replaces). Source conflict: Section C rule 1 and 4a (`research-notes.md:192`, `:196`) and GQ-96 (`gaps-and-questions.md:119`) carry no such condition; the plan follows WC-3. Rule 4b sets the class only for rows with no earlier match (the `failed` contract with a non-`E-RESUME-NEEDED` STOP code, the ledger and the ready-Task cases). Detection per sub-case: (4a) `worker-show --json` key `observation.agentWait` non-null, or `return-contract.yaml` `worker_status: blocked` with `blocked_question` when rule 1's condition holds (WC-2 `WORKER-CONTRACT.md:30` puts `blocked_question` in every blocked contract, so without the condition the rule 1 skip would have no effect); (4b-contract) frozen when the latest implement `return-contract.yaml` has `worker_status: blocked` and rule 1's condition holds (otherwise policy could not determine, as above), or `failed` with a `reason` STOP code other than `E-RESUME-NEEDED` (`WORKER-CONTRACT.md:133`; `06-orca-open-questions.md:136`); (4b-ledger) frozen or Ruling-halted when the package ledger `.dev/tasks/{to-do,done}/*/progress.md` shows the first non-complete task with `halt` or `blocked` as its last record and no eligible Ruling after it (`:133`). Only the `T<id>: complete verdict=…`, `FINAL:` and `ARCHIVE:` line forms are documented (`sc-crash-recovery/refs/pipelines.md:190`); the halt, blocked and Ruling record literals are not captured, so the ledger half is not buildable in Phase 1 and prints "policy: could not determine (ledger record format not known)" (S9 row 81b); (4b-Task) `task-list --ready --run <id> --json` returns `id`, `status`, `display_name`/`task_title`/`spec`, `assignee_handle`, `dispatch_id` and no creator field (`07-gate-gap-fill.md:43`), so a foreign Task cannot be told from the coordinator's own: Phase 1 lists every ready Task under (b) with "creator: could not determine" (S9 row 81c); (5) live, `in_progress`, `agentWait` null -> working; (6) settled outcome **and** contract read, or a "guard refused:" body -> finished ("contract read" means the sweep's own disk reader found and parsed `<report-dir>/return-contract.yaml` with `worker_status` succeeded, partial or failed, `research-notes.md:199`; it is a file the sweep reads, not a claim that the worker or coordinator read anything; a `partial` contract is finished with the note "partial: usable not yet judged", because `WORKER-CONTRACT.md:125` holds dependents until the coordinator has read `report_path` and recorded whether the partial deliverable is usable, and an unusable one is handled like `failed`, a judgment the sweep cannot observe); (7) all else -> could not determine. Idle only for person-started sessions with no activity in the window. Activity (plan decision, new design): the modification time (`os.stat`, a plain read by the step 1.4 disk reader) of the session's transcript `~/.claude/projects/<key>/*.jsonl`, compared with the `--window` start; for Orca rows, time with a non-null `agentWait` is excluded from activity age (step 1.5). A person-started session with activity inside the window matches no Orca rule and is routed explicitly by rule 7: could not determine, with the note "person session, active" (Section C defines working only from Orca fields, `research-notes.md:198`; person-started sessions are in scope, Section 3.1 G6). Rules fixed by the gaps: exited + no `worker_done` + unreadable transcript -> could not determine (GQ-84); `agentWait` null = no wait observed (valid for working, never stall proof), absent on an unsettled row = could not determine (GQ-58; the X-4 split rule, `06-orca-open-questions.md` Gap 19 `:144`); `unverifiable`, late heartbeat, stale `evidence.liveStatus` or a missing row -> could not determine, never stalled (WC-10 `WORKER-CONTRACT.md:45`; SC-5); a just-dispatched worker with no signal -> working or could not determine, never idle (external context, web-01 rec. 3); a non-null `parent` (`lc16-show-4.json:115`) -> note "WC-13 violation, review" (GQ-40). Never inputs: `projection.stage.activity` (C5; stays "working" after settlement, `lc17-show-1.json:132`) and `resource.terminalState` for the class (`lc16-show-4.json:145-151`). Safe-to-close is computed separately: terminal releasable needs `terminalState` reclaimable, `nextAction` release (`lc17-show-1.json`) and the session's result already read (`research-notes.md:218`); no probe observes that the result has been read, so for a terminal Orca reports as reclaimable with next action release Phase 1 prints "terminal releasable: could not determine (result read not observable); Orca: reclaimable, next action release", with no proxy for the read; worktree removable = none of the five refusal conditions at `WORKER-CONTRACT.md:108`, not frozen (`:133-136`), no unpushed commits (branch ahead of its upstream or with no upstream, from `git status --branch --porcelain`; `seed-brief.md:68`, `issue-summary.md:10`, analysis F5 `analyze-worker-contract.md:36`), and no untracked or unstaged path under `.dev/tasks/` (`git status --porcelain -- .dev/tasks`; `.dev/tasks/` content is never disposable, `seed-brief.md:60`, analysis F4 `:35`); either one present prints "no" with that condition. Of the five, uncommitted changes (`git status`), unmerged commits (`git log` / `branch`) and an unfinished ledger (`progress.md`) are observable through step 1.4; "a report it has not read" depends on the coordinator's own reading, and an open PR needs a `gh` call the allowlist does not contain, so neither is observable. Phase 1 therefore never prints "worktree removable: yes": it prints "no" with the observed condition, or "could not determine (report read and open PR not observable)". Both print as REVIEW, never run. Further rules recovered from the sources (Section 3.1): (i) one managed package in two worktrees (`WORKER-CONTRACT.md:108`, "It never runs one managed package in two worktrees at once."; `scope-01:64`): the same package id under two worktree roots makes both "removable: no" with that condition named and lists the pair under Retained problems (plan decision, new design; `safe_to_close` reads a non-empty `worktree.shared_package_ids`, set by the `mark_shared_packages` pre-pass above); (ii) a context-only Dispatch, listed as unsupervised with terminal state retained (`worker-list --help` line 20, `05:20`; `scope-02:95`) [CODE-VERIFIED], is never working or stalled (proved) from Orca liveness; unless rule 1 or 6 matches on a contract it is could not determine with the note "context-only Dispatch (unsupervised, terminal retained)", and `retained` is never terminal releasable (plan decision, new design; `classify` reads `row.orca.unsupervised`, `safe_to_close` reads `row.orca.terminal_state`, step 1.2; the JSON field that marks unsupervised is not captured, so the test uses a synthetic fixture, step 1.8); (iii) package states (`scope-02:192`; `pipelines.md:190`, `:199`): a package in `to-do/` whose ledger shows every task complete is "archive-blocked", neither an unfinished ledger (refusal condition 4) nor finished; a package with an `.archiving` marker is "interrupted archive", listed under Retained problems, never cleared, and its worktree is "removable: no" (plan decision, new design; both states are read from `worktree.archive_states`, step 1.2, and print where step 1.5 says); (iv) ownership: a session is mapped to a worktree by path for the Worktree column only, since "Workspace co-location alone is not ownership." (`PKG/integration-gaps.md:12`, `scope-04:222`); a peer row's Owner is "unknown" unless it carries `linked: true` (`06:99`, `:110`). Tests for (i)-(iii) in step 1.9. |
| 1.4 | Write the probe module with the read allowlist | `src/superclaude/cli/sweep/probes.py` (new) | Single seams `_orca(*args: str) -> str` (runs `["orca-ide", *args]`) and `_git(cwd: Path, *args: str) -> str` (runs `["git", "-C", str(cwd), *args]`), each `subprocess.run(..., capture_output=True, check=True, text=True, timeout=10)` returning stripped stdout. Like the precedent `reflect/config.py:64-78`, the seams raise rather than return a sentinel: `subprocess.SubprocessError` (including `TimeoutExpired` and `CalledProcessError` from `check=True`) or `OSError`. The probe functions in `probes.py` that call them catch `(OSError, subprocess.SubprocessError)`, as `reflect/config.py:103-109` does, and map the failure to a could-not-determine result for that row or source, with an `unscanned:` reason. An argv outside the allowlist raises `ValueError` before `subprocess.run` and is not caught, so the CLI exits 1 (plan decision, new design). GQ-27: module location decided here. Every Orca argv is `orca-ide orchestration <verb>` (C13; GQ-85; SC-3), with one named exception: `orca-ide worktree ps --json`, a top-level verb outside the `orchestration` group. Module-level allowlist (default, `scope-03:99` after NB-4): `worker-list --run <id> --json` (no `--include-remote` by default: its cost is unmeasured, GQ-22, S9 row 17; remote rows then read `unverifiable`, `05:163`, and classify as could not determine; the flag joins the allowlist only after the measurement below) paged on `page.nextCursor` (100 rows, newest first, `[H:worker-list]` 3, 21); `worker-show --dispatch <id> --json`, one call per row (G-A / B-08; worst case ceil(N/100) + N calls); `worker-read --source transcript` (restart without cursor on `source_changed`); `task-list --ready` / `--run <id>`; `run-list` (paged, `--cursor`); `run-current`; `gate-list`; `worktree ps --json` **without** `--agent-wait`. Any other verb raises before the subprocess call. Git: `git -C <worktree>` with `status`, `log`, `branch`, `rev-parse`, `stash list` only (GQ-21; C3). Per-sweep bounds (GQ-99; values proposed in this plan, new design): at most 50 `worker-show` calls and a total wall-clock budget of 90 s for all probe calls, below the Bash tool's 120 s default timeout (with `timeout=10` per call, about 12 hung calls would otherwise lose the whole report). The skill passes an explicit Bash timeout of 120000 ms. When either bound is reached, no further probe call starts; every remaining row is "could not determine (call bound reached)" with `unscanned: call bound reached`, the summary counts those rows, and `report.py` still writes the report. Orca unavailable (`runtime_unavailable`) -> banner "Orca unavailable", never `orca open` (scope-02 `:115`), and no further `_orca` call. Worktree roots and report dirs normally come from Orca (`terminal.worktreePath`, `worktree ps`), so with Orca down discovery is `--root` only (plan decision, new design): the fixed patterns `<root>/.dev/tasks/{to-do,done}/*/progress.md` and `<root>/.dev/tasks/{to-do,done}/*/return-contract.yaml`, plus the home-directory transcript sources below, which need no Orca. Each package found gives one row classified from its ledger and contract alone; a `return-contract.yaml` at a report dir outside those patterns is not found. Every Orca source prints `unscanned: orca unavailable`, and any row that needs an Orca field is could not determine with that note. Disk readers (plain file reads, no subprocess): `<report-dir>/return-contract.yaml` (WC-4, `WORKER-CONTRACT.md:30-38`; `blocked_question`); `<root>/.dev/tasks/{to-do,done}/*/progress.md` (packages sit one level below `to-do/` or `done/`, so a single-`*` pattern finds none; fixtures at that depth in steps 1.8 and 1.10), sprint `results/phase-N-result.json`, `.roadmap-state.json`, MDTM frontmatter `status:` (crash-recovery `refs/pipelines.md:19`, `:52-68`, `:102-116`, `:177-201`); the pane-to-transcript map `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/<tabId>+<leafId>` (3 lines; `ccsession:564-605`; K1 / GQ-18, CODE-VERIFIED for one worker); labelled sessions `~/.claude/projects/<key>/topics/*.txt` read directly, never `ccsession --list` (it writes via `ensure_names_migrated`, `ccsession:285-287`, `:1787-1788`; GQ-21); transcripts `*.jsonl` read by tail, not whole (the `parse_session_log.py:31-40` whole-file limit). Own scanner instead of `bootstrap_scan.sh` (K2 / GQ-19): project dir key replaces every non-alphanumeric character with `-` (`ccsession:1301-1302`), and a `.git` file counts as a repo. No name from `superclaude.contracts` is re-declared here (Check 11); none of them is needed, since that module holds no sweep vocabulary. Acceptance, live check (pass rules are plan decisions, new design): before the run, record each worker's state for one known Run from `orca-ide orchestration worker-list --run <id> --json`; then run `superclaude sweep run --run <id>` once through Bash with timeout 120000 ms. Pass = exit 0, the probe calls finish inside the 90 s budget, every row carries a class, each recorded worker gets the class its recorded state maps to under step 1.3 (could not determine where step 1.3 says so), and no row is could not determine because of a probe error or timeout. Save the stdout JSON to the task package `artifacts/sweep-live-check-1.4.json`. Separately, time one `worker-list --run <id> --include-remote --json` call and save its duration and row count to `artifacts/include-remote-cost.txt` (GQ-22 stays open until measured; remote rows read `unverifiable` without the flag, `05:163`). Recovered probe rules (Section 3.1): (a) worktree removed mid-sweep (`research-notes.md:178`; `seed-brief.md:45`): a `_git` call or disk read that fails because the worktree path no longer exists maps to could not determine with `unscanned: worktree removed during sweep` for that worktree and its sessions; the run continues and the report is written (fixture in step 1.8, test in step 1.9); (b) `worktree ps` coverage (`06:97`, `:109`): every host named under `not covered` prints "could not determine", never "no sessions", and, because the page is cut by a shared `--limit` cap and neither the default cap nor the JSON field that marks a cut page has been captured, the `worktree ps` peer count always prints as "at least <N>" until a capture shows how a complete page is recognised (plan decision, new design; test in step 1.10); (c) the disk reader also checks for `<package>/.archiving` with a plain `os.stat`, never deleting or clearing it (`pipelines.md:199`). |
| 1.5 | Write the report renderer (the only write) | `src/superclaude/cli/sweep/report.py` (new) | Public functions (plan decision, new design): `render(rows: list[SessionRow], worktrees: list[WorktreeState], sources: list[SourceCoverage], now: datetime) -> str`, pure, no I/O, with `now` injected for the header time and every age; and `write_report(text: str, output_dir: Path, now: datetime) -> Path`, the module's only I/O, which calls `output_dir.mkdir(parents=True, exist_ok=True)` and then `(output_dir / f"{now:%Y%m%d-%H%M%S}-sweep.md").write_text(text, encoding="utf-8")` and returns that path. These two calls (`Path.mkdir` and `Path.write_text`) are the only write primitives in the package; step 1.11 allows them under `--output` only. `report.py` does not build the JSON: `commands.py` builds and prints it (step 1.6). `render` lays out the DERIVED skeleton of `scope-04:268-308`, pinned to `495eb96d` (GQ-35): title "# Orchestrator sweep: <worktree-tree root>"; "READ ONLY . observed <real UTC time>" (#409 hardcodes its clock, `canvas.py:73-77`; external context, web-02); "Scope:" with the root path (GQ-32); "Sources:" listing every source's coverage and age (GQ-31) and "Messages coverage: partial" (G-B; `scope-04:276`). Sections in order: Waiting on a person (a) explicit questions, sorted oldest first by the sweep itself (C6; `agent_focus.py:46` has no sort), tie-break by ID (GQ-29), unknown age in a labelled group, never age 0 (external context, web-02 Kanban); Waiting on a person (b) frozen or blocked by policy, no question text ever (B-11); Retained problems (failed / stale / policy frozen, plus stalled (proved) and could not determine split into "evidence absent" and "source not read", external context web-01 rec. 1; plus, from the step 1.3 rules (i) and (iii) (plan decision, new design), one line per `archive_states` entry with state "interrupted archive", "interrupted archive: <package id> in <worktree path>; marker kept, review", and one line per package id in `shared_package_ids`, "one package in two worktrees: <package id> in <path 1> and <path 2>"); Sessions (<shown>/<total>) with the ten dimensions, derived Class and safe-to-close REVIEW; Worktrees (<shown>/<total>), each row with its safe-to-close worktree half and a Package state column (plan decision, new design) that prints every `archive_states` pair as "<package id>: archive-blocked" or "<package id>: interrupted archive" and "-" when there is none; Historical sessions. Every list prints `<shown>/<total>` (C7; GQ-33: list everything, so shown equals total); a source cut at 100 rows prints "at least 100 (truncated at 100), total could not determine" (GQ-48 / GQ-56; external context web-02 gh CLI). Fixed strings: "Seen is not resolved", "Answered: could not determine" (GQ-47 / GQ-49), "Inspection only." footer (`canvas.py:81`). Approval column prints "not observed" until the `gate-list` mapping is verified (GQ-34, S9 row 29). Column sources per `scope-04:336-351` (B-14), with the value printed when there is no source in brackets: Session = Orca Task / Dispatch id from `worker-list`, transcript uuid for a person-started session (-); Owner = Run id (`run-list` / `worker-list --run`), "person" for a person-started session (unknown); Worktree = Orca `terminal.worktreePath`, transcript cwd for a person-started session (unknown); Class = Section C precedence (could not determine); Lifecycle (`data-dictionary.md:19`) = `projection.outcome` and `stage.detail`, `settled` -> settled, else running (unknown); Phase (`:20`) = none among the sweep's inputs (not observed); Health (`:21`) = contract `worker_status: failed` -> failed result, liveness `unverifiable` -> unknown (unknown); Approval (`:22`) = candidate `gate-list` gate `status`, mapping [UNVERIFIED] (not observed); Freshness (`:23`) = `evidence.liveStatus` and `observedAt` (`lc16-show-4.json:140-144`), transcript mtime for a person-started session (unknown); Result (`:24`) = contract `worker_status` succeeded / partial / failed, `blocked` prints null because the class says waiting on a person (not observed); Admission (`:25`) = none, "never inferred", no admission record (`integration-gaps.md:13`) (not observed); Evidence (`:26`) = DERIVED: contract `report_path` and every `artifacts` path exist -> complete packet, else partial packet (not observed); Policy (`:27`) = frozen test at `WORKER-CONTRACT.md:133`, contract + ledger (not observed); Tests/review (`:28`) = none, no revision-pinned check feed (`integration-gaps.md:13`) (null (unavailable)). The (a) table has the columns `| ID | Age | Question | Requested by | Decision owner | Affected | Evidence |` (`scope-04:278`), with cells per source as in B-12 (`scope-04:322-330`; Section 3.1 Report rules). Further fixed strings and rules recovered from the sources (Section 3.1 Report rules): an empty list prints "No matching records. This is not an all-clear." (`PKG/render.py:116`); the (a) heading always prints "Messages coverage: partial (Orca questions are not enumerated; sources are return contracts and worker-show agentWait). This is not an all-clear." (`scope-04:276`); the (a) section prints "Distinct affected sessions: <N> (set union, not a sum)" computed as a set union over sessions (`PKG/PLAN.md:36`; `scope-04:283`); every untrusted string (`blocked_question`, transcript-derived text, Orca body text, titles, paths) passes a `sanitize()` that strips ESC/CSI/OSC sequences, C0/C1 controls, carriage returns and bidi controls before it reaches `render`'s output (`PKG/PLAN.md:38`, `PKG/canvas.py:10-17`); a lost or unscanned source never resolves a question, fails a session, lifts a freeze or yields a retry recommendation: its rows print could not determine with the `unscanned:` reason (`PKG/integration-gaps.md:24`); the Scope line names any `--run` or window filter and the denominator its counts are taken from (`PKG/integration-gaps.md:24`; `scope-04:67`); where sessions are known to form one fan-in group, the group prints settled and admitted counts against N, at most 10 inputs, merge only with at least 2 admitted, a `partial` input counted as "usable not yet judged" (`WORKER-CONTRACT.md:156`; `scope-01:68`). Tests for the empty state, sanitizing and source loss in step 1.12. Open Tasks, questions and unread reports are always listed; the 6 h window bounds only activity rows (GQ-61; SC-7); person-wait time is excluded from activity ages and the activity window, while the waiting list prints and sorts on time since the wait began (`scope-04:87` "original age"; external context, web-01 rec. 4). Optional one-line "what to check next" text per waiting item, text only (external context, web-02 I-PASS). Report text uses the Section C class names only (GQ-86 to GQ-95, GQ-97). |
| 1.6 | Write the Click group | `src/superclaude/cli/sweep/commands.py` (new), `tests/sweep/test_cli_contract.py` (new) | `sweep_group` with one subcommand `run`. Options (types and defaults are plan decisions, new design): `--window` string `<N>h` or `<N>d` with N a positive integer, parsed in `commands.py`, anything else a usage error, default `6h` (GQ-61); `--run <id>` string, repeatable, default the `run-current` binding when one exists, else every Run from `run-list` (paged), the same fallback `worker-list` uses (`07-gate-gap-fill.md:47`, `worker-list-run-scope.js:8-24`); `--root <dir>` path, default the current git top-level, the worktree-tree root printed as "Scope:" (GQ-32) and the base for disk readers: only fixed patterns under it and under each `worktree ps` root are read (`.dev/tasks/{to-do,done}/*/progress.md`, `<report-dir>/return-contract.yaml`), no recursive walk, and a path whose `resolve()` leaves the root (symlink out) is skipped with `unscanned: outside root`; `--output <dir>` path, default `.dev/sweeps/` under `--root` (working default, GQ-10, S9 row 8), and a resolved path outside `<root>/.dev/` is a usage error. Prints the result as JSON with `click.echo(json.dumps(...))`, schema version 1, every key always present (absent values `null`, never omitted): `schema_version` (int), `observed_at` (UTC ISO 8601 string), `scope` (string), `window` (string), `orca_available` (bool), `sources` (list of `name`, `coverage`, `age_seconds` int or null, `unscanned` string or null), `rows` (list of the ten dimension fields plus `cls`, `evidence`, `notes`, `safe_to_close` with `terminal` and `worktree`), `waiting` (`a` and `b` lists), `summary` (count per class name, `bound_reached` int, `total` int), `report_path` (string). It writes `<output>/<YYYYMMDD-HHMMSS>-sweep.md` through `report.py` (G7: a dated local file, never posted). Exit codes: 0 sweep completed, including rows that are could not determine and an Orca-unavailable sweep (`orca_available: false`, banner in the report); 1 internal error, `[sweep ...]` prefix on stderr (recommend pattern, `recommend/commands.py:73-74`; not reflect, which prints `Error: {exc}` and exits 2 on a config STOP); 2 usage error (Click's usage-error code: bad `--window`, `--output` outside `.dev/`). Never calls `orca open`, `check`, `ask`, `reply`, `send`, `inbox`. `test_cli_contract.py` asserts the top-level and row key sets and types on a fixture sweep, each exit code, the `--window` parser cases and the `--output` rejection. |
| 1.7 | Register the CLI | `src/superclaude/cli/main.py` | Add the two-line deferred import and `main.add_command(sweep_group, name="sweep")` after `:561` and before the `__main__` guard at `:564-565`, with the same `# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` comment as `:559` (SC-10). |

#### 1B. Tests (read-only proofs, classification, report, registration)

| Step | Action | Files | Details |
|---|---|---|---|
| 1.8 | Add seam fixtures and Orca captures | `tests/sweep/` (new), `tests/sweep/conftest.py` (new), `tests/sweep/fixtures/` (new) | `patch_orca` and `patch_git` fixtures that `monkeypatch.setattr` the `probes` module's `_orca` / `_git`, as `tests/cli/reflect/conftest.py:58-80` (`FIXTURES_DIR` as `:17`). Fixtures copied from `lc16-show-4.json` (live, working), `lc17-show-1.json` (failed, reclaimable, `nextAction` release), `lc01-show-1.json` (succeeded), `lc01-step7.txt` (empty `workers`, `page`, `scope`), plus hand-made rows for `exited`, `unverifiable`, non-null and absent `agentWait`, and a 100-row page; hand-made rows are labelled synthetic because no capture exists (scope-02 `:209-217`). One fixture per rule 4 sub-case: a non-null `agentWait` row and a `blocked` contract with `blocked_question` on a settled row (4a; the same contract on a live row under `ask the coordinator` is not (a), see the rule 1 fixtures); a `blocked` implement contract on a settled row or under `report blocked` (asserts both outputs: class waiting on a person (a) from rule 1 and policy frozen, so it is also listed under (b); GQ-96), the same contract on a live `in_progress` row under `ask the coordinator` (asserts no class from rules 1, 4a or 4b-contract and policy could not determine with the "may be re-running" note), a `blocked` implement contract with `reason` `E-HALT-QA` on a live row under `ask the coordinator` (Ruling halt, never asked, WC-3 `WORKER-CONTRACT.md:56`: class (a) and policy frozen), a `failed` contract with a non-`E-RESUME-NEEDED` STOP code and a `failed` contract with `E-RESUME-NEEDED` (not frozen) (4b-contract); a synthetic ledger at `.dev/tasks/to-do/<id>/progress.md` labelled synthetic until the record literals are known (4b-ledger, S9 row 81b); a `task-list --ready --json` row (4b-Task). Rule 1 fixtures (WC-3 `WORKER-CONTRACT.md:54-55`): a `blocked` contract on a settled row and on a live row whose brief says `report blocked` (both waiting on a person (a)), and a `blocked` contract on a live `in_progress` row whose brief says `ask the coordinator` (not waiting on a person: working or could not determine with the "may be re-running" note, and not (a) or frozen under rule 4). Rule 6 fixture: a `partial` contract (finished, note "partial: usable not yet judged", `:125`). `patch_git` fixtures for the two worktree conditions of step 1.3 (`unpushed`, `dev_tasks_unsaved`; mock-based tests for unpushed commits, `seed-brief.md:68`; `.dev/tasks/` content never disposable, `:60`): `git status --branch --porcelain` output for a branch with no upstream and for a branch ahead of its upstream, `git status --porcelain -- .dev/tasks` output with an untracked path and with an unstaged path under `.dev/tasks/`, and a `_git` that raises `subprocess.CalledProcessError` (could not determine). `tmp_path` contract and ledger files as `tests/recommend/conftest.py:1-24`. Fixtures for the rules recovered in Section 3.1, all labelled synthetic: a context-only Dispatch row (unsupervised, terminal state `retained`; no capture exists, `05:20`, `:28`); a `tmp_path` package in `to-do/` whose `progress.md` shows every task complete (archive-blocked) and one with an `.archiving` marker (`pipelines.md:190`, `:199`); the same package id under two worktree roots (`WORKER-CONTRACT.md:108`), giving two `WorktreeState` records whose `package_ids` share that id, passed through the step 1.3 `mark_shared_packages` pre-pass; a worktree root that exists when listed and is deleted before its `_git` call (a `_git` that raises because the path is gone; `seed-brief.md:45`); a `worktree ps --json` page naming a `not covered` host (`06:97`). |
| 1.9 | Classification tests | `tests/sweep/test_classify.py` (new) | One case per precedence rule 1-7 plus the idle rule (SC-4; together they reach all seven class names of step 1.2), including fenced with `exited` (NB-1), `agentWait` null versus absent (GQ-58), guard-refused body, exited + unreadable transcript -> could not determine (GQ-84), blocked contract with Orca outcome `failed` -> waiting on a person (WC-5 `WORKER-CONTRACT.md:58`), and no path to stalled without stop proof (SC-5). Safe-to-close cases for each of the five `:108` conditions and the `:133-136` freeze. One safe-to-close case per step 1.8 `patch_git` worktree fixture (branch with no upstream, branch ahead of upstream, untracked path under `.dev/tasks/`, unstaged path under `.dev/tasks/`), each built through the step 1.4 git probe and asserting "worktree removable: no" with the condition named (unpushed commits, or unsaved `.dev/tasks/` path); and one where the `_git` call fails, asserting `unpushed` / `dev_tasks_unsaved` is `None` and "worktree removable: could not determine" (`seed-brief.md:60`, `:68`). Cases for the recovered rules (step 1.3 (i)-(iii), step 1.4 (a)): the context-only Dispatch is never working or stalled (proved) and is could not determine with the "context-only Dispatch" note, and its `retained` terminal is never terminal releasable; the archive-blocked package is neither unfinished ledger nor finished and prints "archive-blocked" in the Worktrees Package state column (step 1.5); the `.archiving` package prints "interrupted archive" in that column and under Retained problems, the marker file still exists after the run, and its worktree is "removable: no"; `mark_shared_packages` sets `shared_package_ids` on both records of the two-root fixture and on neither record when the ids differ, and `safe_to_close` then makes both worktrees "removable: no" with the condition named, and the pair prints under Retained problems; the worktree removed mid-sweep gives could not determine with `unscanned: worktree removed during sweep`, exit 0, and the report file still written. |
| 1.10 | Allowlist tests | `tests/sweep/test_probes_allowlist.py` (new) | Record every `_orca` argv during a full sweep over fixtures and assert each recorded argv tuple equals one of the exact allowlisted argv tuples (SC-2), not only a prefix: `orca-ide orchestration <verb> ...` for every verb (SC-3), plus the one named exception `("orca-ide", "worktree", "ps", "--json")`. Negative cases that must fail: `check` in any form, `--ack`, `--wait`, `--unread`, `--format`, `worker-list --include-remote` (until GQ-22 is measured), two or more of `--unread`/`--peek`/`--all`, `reply`, `ask`, `send`, `inbox`, `worktree ps --agent-wait`, any unknown verb. Git argv limited to the five read forms; `stash` only with `list`. Bound case: a fixture with more rows than the `worker-show` bound, and one where `_orca` exceeds the wall-clock budget, both assert no further `_orca` call after the bound, the remaining rows read "could not determine (call bound reached)" with `unscanned: call bound reached`, the summary counts them, and the report file is still written. Orca-down case: the first `_orca` call raises with `runtime_unavailable`; assert no further `_orca` call, no `orca open`, exit 0 with `orca_available: false`, rows only for the packages of a `tmp_path` fixture laid out at `<root>/.dev/tasks/to-do/<id>/` and `<root>/.dev/tasks/done/<id>/`, every Orca source `unscanned: orca unavailable`, and the report still written. `worktree ps` coverage case (step 1.4 (b); `06:97`, `:109`): with the step 1.8 page naming a `not covered` host, that host prints "could not determine" and the string "no sessions" appears nowhere for it, and the peer count prints as "at least <N>". |
| 1.11 | Read-only proof | `tests/sweep/test_readonly.py` (new) | Proof by snapshot diff, not by patching write primitives (plan decision, new design). Inside `CliRunner.isolated_filesystem()`, lay out the step 1.8 fixtures under the isolated root, and `monkeypatch.setenv` `HOME` and `XDG_STATE_HOME` to directories inside it, so every disk source the sweep reads (packages, contracts, `~/.claude/projects/`, the ccsession tab map) is inside the snapshot. Before the run, record for every path under the isolated root its relative path, size, `st_mtime_ns` and a SHA-256 of its bytes; run `sweep run` with `patch_orca` / `patch_git` (step 1.8); record again. Assert the two snapshots are equal except for exactly one added file, `<output>/<YYYYMMDD-HHMMSS>-sweep.md`, plus the `--output` directory when it did not exist before (the `Path.mkdir` and `Path.write_text` of step 1.5); any other added, removed or changed path fails, whichever primitive made it (`open` in a write mode, `write_text`, `write_bytes`, `mkdir`, `touch`, `os.rename`, `os.replace`, `os.remove`, `shutil.*`). Subprocesses are proved separately: with the seams monkeypatched, no real subprocess call is needed, so `subprocess.run`, `subprocess.Popen` and `os.system` are patched with `side_effect=AssertionError(...)` for the whole run, in the style of `tests/cli/reflect/test_contract_status_cli.py:44-66`. That precedent patches entry points only; the snapshot diff has no cited in-repo precedent. Limit: the snapshot covers the isolated root only, which is why `HOME` and `XDG_STATE_HOME` are moved into it (SC-1). |
| 1.12 | Report tests | `tests/sweep/test_report.py` (new) | Rendered headings in skeleton order; every class reachable in the Class column, stalled (proved) and could not determine also under Retained problems (SC-6); an item stays listed while its source still shows it, whatever its age: an open Task, a non-null `agentWait` row and a `blocked` contract, each older than the window, are listed, and the same items absent from their source are not (SC-7); `<shown>/<total>` on every list and the truncated-at-100 string (SC-8); real UTC time and "Messages coverage: partial" in the header (SC-9); oldest-first with the labelled unknown-age group. Cases for the rules recovered in Section 3.1: empty state, an empty (a) list renders "No matching records. This is not an all-clear." and the (a) heading carries "This is not an all-clear." (`PKG/render.py:116`, `scope-04:276`); sanitizing, an injection fixture whose `blocked_question`, transcript text and Orca body carry ESC/CSI/OSC sequences, C0/C1 controls, a carriage return and bidi controls renders with none of them present (`PKG/PLAN.md:38`; #409's `injection` variant, `fixtures.py:85-86`); source loss, with a contract unreadable or Orca unavailable the affected rows print could not determine with the `unscanned:` reason, and none turns finished, failed, not frozen or retry-recommended (`PKG/integration-gaps.md:24`), kept apart from the SC-7 case where the source is read and the item is absent; set union, one session reached by both a `blocked` contract and a non-null `agentWait` counts once in "Distinct affected sessions"; denominator, a `--run` run prints the filter and its total on the Scope line. |
| 1.13 | CLI registration test | `tests/sweep/test_cli_registration.py` (new); optional `tests/cli/test_cli_registration.py` | `CliRunner` `superclaude sweep --help` and `sweep run --help`, as `tests/recommend/test_cli_registration.py:1-39` (SC-10). Optionally add `sweep` to `EXPECTED_TOP_LEVEL_COMMANDS` (`tests/cli/test_cli_registration.py:31-49`). |

#### 1C. Command and skill

| Step | Action | Files | Details |
|---|---|---|---|
| 1.14 | Write the thin command | `src/superclaude/commands/sweep.md` (new) | Frontmatter `name: sweep` and section layout copied from `src/superclaude/commands/issue.md` (newest template; scope-03 `:108`, `:111` CC). Activation block: "**MANDATORY**: Before executing any protocol steps, invoke: > Skill sc:sweep-protocol", naming the installed path `~/.claude/skills/sc-sweep-protocol/SKILL.md` and the project `.claude/skills/` copy (dual surface; no `src/superclaude/` path). States coordinator-only, read-only, never as a worker. No `## Unattended mode` section (`_check_no_unattended_sections`, `tests/skills/test_worker_contract.py:464-472`). |
| 1.15 | Write the skill | `src/superclaude/skills/sc-sweep-protocol/` (new), `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (new) | `name: sc:sweep-protocol` (lint: the directory ends in `-protocol`, SC-13). Calls `superclaude sweep run` from PATH first; when that call fails with "command not found", it runs `uv run superclaude sweep run` (dev checkout). The fallback is a new design (K3 / GQ-25; B-19 / NB-3): `sc-reflect-protocol/SKILL.md:63-64` is the precedent for the bare form only, and `sc-swarm-wizard-protocol/SKILL.md:7` for the `uv run` form. `allowed-tools`: Read, Glob, Grep, `Bash(superclaude sweep *)`, `Bash(uv run superclaude sweep *)` (space form, as `sc-swarm-wizard-protocol/SKILL.md:7` and `sc-crash-recovery/SKILL.md:4`); no `command -v` call, so no entry for it; no `Write` or `Edit` (`report.py` renders and writes the report, step 1.5; the skill only reads it); no `git stash *`, no `ccsession`, no `orca-ide` outside the CLI. Steps: run `superclaude sweep run` (default `--output .dev/sweeps/`, step 1.6) with an explicit Bash timeout of 120000 ms, treat exit 0 as a completed sweep, 2 as a usage error to report, 1 as a failure to report with its stderr, read the report at the JSON `report_path`, print its path and the (a)/(b) counts, recommend (never perform) the `WORKER-CONTRACT.md:74`, `:107` and WC-6 actions. These recommendations are proposals printed as text; stop, abandon, retry, release, merge and removal stay coordinator decisions that need positive proof (`06-orca-open-questions.md:138`: "The sweep must not propose stop/abandon/retry/release; those need positive proof and are coordinator decisions"). That source position, the seed brief's "recommended next action" and #409 rule 5 are one open owner decision (Section 3.1 "Recommendations only"; Section 9.4 row 98b); if the owner rules against proposals, this clause is dropped. Reuses the crash-recovery SAFE/REVIEW labels and the "What I could not determine" section with `unscanned:` markers (`sc-crash-recovery/SKILL.md:91`, `:139-150`; report-template `:127-129`). Contains no write verb that the AC-0.9 audit would flag (`AUDIT_ROOTS` `test_worker_contract.py:1090-1094`, `WRITE_VERB_RE` `:1098`, `WRITE_VERB_CLASSIFICATION` `:1166`). |
| 1.16 | Static command test | `tests/commands/test_sweep_command.py` (new) | As `tests/commands/test_issue_command.py:1-60`: frontmatter, Activation block, installed skill path, no `src/superclaude/` path, PATH form before `uv run`, and both space-form literals `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)` present exactly in `allowed-tools` (static half of SC-16), no `## Unattended mode` heading. |

#### 1D. WC-14 and contract pins

| Step | Action | Files | Details |
|---|---|---|---|
| 1.16a | Sequencing re-check (gate for 1D and the 1.5 skeleton) | none (read-only checks) | Run `gh pr view 422 --repo IronbellyOrg/IronClaude --json state,files`: if #422 is open, either stop before step 1.17 and wait for it, or keep this PR to new files and move steps 1.17-1.19 to a follow-up PR (GQ-62, S9 row 52); if it is merged, rebase onto `origin/master` first; any #422 file that steps 1.21-1.23 also edit is gated the same way. If #409 has merged, diff its layout files against `495eb96d` (Dependencies row) and update step 1.5 and its tests before step 1.12 runs. Record both results in the task package `artifacts/`. |
| 1.17 | Add the WC-14 rule | `src/superclaude/core/WORKER-CONTRACT.md` | New `### WC-14. Coordinator loop` after the fan-in rule ending at `:156` and before `### Worked example` at `:158` (alternative: after `:129`, before `:131`; GQ-11: WC-14 is the working default rather than reusing the unused WC-1 ID, pending the owner decision, S9 row 9). Draft clause text (plan wording, new design; final wording at implementation review), heading line `### WC-14. Coordinator loop`, then: G1 "The coordinator keeps watching its Run until every Task it created has settled and been admitted; it never stops watching on its own." (owner order 2026-11-05, GQ-04); G2 "When a wait on Orca expires, the coordinator re-arms it."; G3 "On every coordinator wake, the coordinator runs `/sc:sweep` and reads its report before it acts."; G4 "The sweep's classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine."; G5 "The coordinator tells the person about each of these and keeps it in its run notes until the person answers: a `failed` or `blocked` result it cannot retry, a `partial` result it has judged unusable (handled like `failed`), a third brief-guard refusal, a ready Task it did not create, a frozen plan, and a fan-in with fewer than 2 admitted inputs." (the cases at `:125`-`:126`, `:127`, `:129`, `:134`, `:156`); G6 "Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged." (settled by `BUILD-REQUEST.md:12`, `seed-brief.md:66`, `:75` and analysis F2, Section 3.1 G6); G7 "The sweep report is a dated local file; it is never posted." Closing sentence: "The sweep only recommends the stop-and-cancel step for a stalled attempt, worktree removal and a new Task under WC-6; the coordinator performs them under those rules, and a replacement is always a new Task." (`:74`, `:107`, WC-6; GQ-98). That sentence keeps the sweep's text a proposal and the act a coordinator decision; it stands against `06-orca-open-questions.md:138` ("The sweep must not propose stop/abandon/retry/release; those need positive proof and are coordinator decisions") and #409 rule 5, an open owner decision (Section 9.4 row 98b); if the owner rules against proposals, the closing sentence becomes "The sweep recommends none of these actions; the coordinator decides and performs them under those rules." G1 candidate clause, [UNVERIFIED]: "do not end the coordinator turn while `worker-list --run <id> --terminal-state reclaimable --json` returns rows" (`orca-capabilities.md:113`, via `scope-02:94`); add it to G1 only after `orca-ide orchestration worker-list --help` shows `--terminal-state` and the guard is confirmed, otherwise leave it out and record it in Open Questions. G5's fan-in item also names the bounds of `:156`: at most 10 inputs, merge only when at least 2 are admitted, settled/admitted counts against N (`scope-01:68`). No runnable code spans in WC-14 (`_check_repo_setup_gated`, `tests/skills/test_worker_contract.py:446`). |
| 1.18 | Add `/sc:sweep` to never-as-worker | `src/superclaude/core/WORKER-CONTRACT.md` | Replace the opening of the `:23` line with exactly: "**Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` and `/sc:sweep`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers." The rest of the line is unchanged. This line and WC-14 (step 1.17) make coordinator-only a contract rule, not a mechanical guard: the CLI has no caller check, and the step 1.19 pin proves only that the list names `/sc:sweep`, not that a worker cannot run it (K-1). |
| 1.19 | Pin WC-14 and never-as-worker | `tests/skills/test_worker_contract.py` | Add `"WC-14": ("WC-14", ["WC-14. Coordinator loop", "On every coordinator wake", "it is never posted"]),` to `RULE_PHRASES` under the `# Coordinator rules` comment at `:163` (the identifier and the first phrase share the heading line, as `_check_rule` requires at `:388-395` and as the WC-6 entry does; picked up by the parametrized tests at `:540-542`, `:587-594`); set `NEVER_AS_WORKER` (`:245-254`, 8 entries today) to the 9 entries `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard`, `/sc:sweep`, `/sc:pr-submit`; rename `test_never_as_worker_list_names_all_seven_commands` (`:545`) to `test_never_as_worker_list_names_every_listed_command`; set the `RULE_PHRASES["never-as-worker"]` phrase at `:86-92` to "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` and `/sc:sweep`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers" (the step 1.18 sentence); `_check_never_as_worker` (`:398-404`, called at `:545-546`) then checks that the `**Never-as-worker list**` line of `WORKER-CONTRACT.md`, edited in step 1.18, names `/sc:sweep` (SC-12; GQ-12). Keep `sweep` out of `UNATTENDED_COMMANDS` (`:379`). |

#### 1E. Routing registries and docs

| Step | Action | Files | Details |
|---|---|---|---|
| 1.20 | Recommend refresh registry | `tests/recommend/test_routing_refresh.py` | Add `"sweep"` to `_POST_REFRESH_ADDITIONS` at `:33` (asserted at `:647-648`; Activation block parsed at `:38-40`, `:472`) (SC-11). |
| 1.21 | HOW-WE-WORK "Other commands" row and "Orca coordination" section | `src/superclaude/core/HOW-WE-WORK.md` | (a) Add a `/sc:sweep` row inside `<!-- other-commands:v1 -->` (`:318`) ... `<!-- /other-commands -->` (`:337`), ASCII only (test `:342-347`). GQ-24 decided: "Other commands", not the excluded set (`tests/core/test_how_we_work_routing_table.py:299-309`). (b) Required, not optional: edit the "Orca coordination" section (`:396-405`) to match the contract change, as `seed-brief.md:35` and `issue-summary.md:18` require. Add a bullet that the coordinator runs `/sc:sweep` itself as a read-only report on its workers, sessions and worktrees (rules in `WORKER-CONTRACT.md`, WC-14 from step 1.17), and extend the "Some commands are never workers" bullet (`:403`) to name `/sc:sweep` beside `/sc:pr-submit`, matching step 1.18. No test pins this section today (grep of `tests/` for "Orca coordination": no match), so part (b) is checked by reading; a pin may follow the pattern of `tests/core/test_orca_session_launch_guidance.py:14-31`. Part (b) restates steps 1.17-1.18, so it follows their #422 gate (step 1.16a): if 1.17-1.19 move to a follow-up PR, part (b) moves with them. The level table (`src/superclaude/core/CLAUDE.md:65-82`) is not touched. Step 1.23 byte-copies the result, both parts, to the plugin copy. |
| 1.22 | Routing-table registry | `tests/core/test_how_we_work_routing_table.py` | Add `"sc:sweep"` to `_OTHER_COMMANDS` (`:27-40`, checked at `:291-311`) (SC-11). `_EXPECTED_IDS` (`:56-97`) pins the routing-row IDs; `scope-01:117` says a new routing row (for example `supervise-sessions`) "needs adding there; none may be removed". [CODE-CONTRADICTED as a requirement]: the test comment says "A row may be added; none of these may be renamed or removed." (`:54-55`) and `test_ids_unique_kebab_and_stable` (`:200`) asserts only a subset, `_EXPECTED_IDS <= set(ids)` (`:204`), so a new ID would pass without being registered. Step 1.21 adds only an "Other commands" row and no routing-table row, so `_EXPECTED_IDS` stays unchanged, and no ID in it may be renamed or removed. If a later step adds a routing row, adding its ID to `_EXPECTED_IDS` pins it but is not needed for the test to pass. |
| 1.23 | Plugin byte copy | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Copy the edited guide byte for byte, including the step 1.21 "Orca coordination" edit (`tests/commands/test_routing_plugin_parity.py:38`; `issue-summary.md:18`). If part (b) of step 1.21 lands in a follow-up PR, copy again there. |
| 1.24 | User guide row | `docs/user-guide/commands.md` | Add a `/sc:sweep` row to the UTILITIES table (`:105`; `/sc:issue` row `:115`, detail `:347`) and a short detail block. Whether a test pins this table is [UNVERIFIED] (GQ-28, S9 row 23). |
| 1.24a | Developer-guide never-as-worker copy | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | The guide repeats the never-as-worker list verbatim at `:991` (`/sc:agent` ... `/sc:swarm-wizard`, plus `/sc:pr-submit` while D3 keeps it off workers); add `/sc:sweep` there so it matches the step 1.18 line. Re-read the other references and change them only if their wording no longer holds: `:336` (`/sc:spawn` as a never-as-worker command), `:394` (the list changes only through the section 7.7 maintainer edit), `:799` (checklist item "Worker eligibility decided"), `:993` (the maintainer edit names `WORKER-CONTRACT.md` and `NEVER_AS_WORKER`), `:2203` (glossary entry). None of them counts the list, so they are expected to stay as they are. No file under `tests/` names this guide path (the only near match, `tests/docs/test_retired_docs_absent.py:26`, is the retired `docs/guides/` copy), so this step is checked by reading. |
| 1.24b | CHANGELOG entry | `CHANGELOG.md` | Add an entry under `## [Unreleased]` (`:5`) for `superclaude sweep run`, `/sc:sweep`, WC-14 and the never-as-worker addition, in the heading style of the #323 entries (`### Added: ... (#323)`, `:223`, `:230`). |

#### 1F. Gates

| Step | Action | Files | Details |
|---|---|---|---|
| 1.25 | Sync and verify | `Makefile` targets | `make sync-dev`, then `make verify-sync` (SC-15). Never stage `.claude/` copies. |
| 1.26 | Lint | `Makefile:362-489`, `pyproject.toml:203-206` | `make lint` (lint-architecture Checks 1 `:368-383`, 2 `:385-396`, 3/4 `:398-411`, 6 `:413-427`, 8 `:429-439`, 9 `:441-451`, 11 `:467-476`), then `uv run ruff check .` (ruff 0.15.20; no `anthropic` import) and `uv run ruff format --check src/ tests/` (SC-13). |
| 1.27 | Tests | `tests/sweep/`, `tests/commands/`, `tests/core/`, `tests/skills/`, `tests/recommend/` | `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend` (run line pattern `docs/designs/sc-issue-command.md:402`), then `uv run pytest`. Suite scans that must pass: `tests/skills/test_model_alias_policy.py:81-100`, `tests/commands/test_graph_command.py:219-225`, the AC-0.9 write-verb audit (SC-14). |
| 1.28 | Primitive path check | `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md` | `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`; justify or remove every new hit (CLAUDE.md installed-primitive rule). |
| 1.29 | PATH form under pipx | none (manual) | Run `superclaude sweep --help` once from a directory that is not a uv project, time limit 30 s (dynamic half of SC-16; [UNVERIFIED] until run, S9 row 20). Pass = exit 0 and the help text lists the `run` subcommand; save the output and exit code to the task package `artifacts/sweep-help-pipx.txt`. |

Gated later addition inside the sweep (not built in Phase 1): `check --peek` and `check --all` as separate argv, added to the allowlist only after a probe settles 06 Gaps 1, 2 and 18 (`message-check-handler.js:17`, `:30`, `:58-71`); the handler rejects more than one read mode (`message-check-handler.js:18-19`). Until then G-B stays "could not determine" and the contract fallbacks are the only question sources.

### Rollback (Phase 1)

Plan decisions, new design. Phase 1 changes a shared contract (WC-14 and the never-as-worker list) on working defaults, so it is reverted as one unit: WC-14 G3 tells the coordinator to run `/sc:sweep`, and a contract that names a removed command is wrong. The same holds for the HOW-WE-WORK "Orca coordination" bullets of step 1.21(b), which also name `/sc:sweep`.

| What to revert | Step | Files and registrations |
|---|---|---|
| Package and its tests | 1.2-1.6, 1.8-1.13 | `src/superclaude/cli/sweep/` (all six modules), `tests/sweep/` |
| CLI registration | 1.7 | The two deferred-import lines and `main.add_command(sweep_group, name="sweep")` added after `src/superclaude/cli/main.py:561` |
| Command, skill and static test | 1.14-1.16 | `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/`, `tests/commands/test_sweep_command.py` |
| Contract and pins | 1.17-1.19 | The `### WC-14. Coordinator loop` block and the `/sc:sweep` entry on the `**Never-as-worker list**` line of `src/superclaude/core/WORKER-CONTRACT.md`; the `"WC-14"` `RULE_PHRASES` entry, the 9-entry `NEVER_AS_WORKER`, the renamed test and the `never-as-worker` phrase in `tests/skills/test_worker_contract.py` |
| Four registries | 1.20-1.23 | `"sweep"` in `_POST_REFRESH_ADDITIONS` (`tests/recommend/test_routing_refresh.py:33`); the `/sc:sweep` row in `src/superclaude/core/HOW-WE-WORK.md` "Other commands"; the step 1.21(b) "Orca coordination" edits in the same guide: the bullet that the coordinator runs `/sc:sweep`, and `/sc:sweep` removed from the "Some commands are never workers" bullet (`:403`), so the guide no longer tells coordinators to run a removed command; `"sc:sweep"` in `_OTHER_COMMANDS` (`tests/core/test_how_we_work_routing_table.py:27-40`); the byte copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (`tests/commands/test_routing_plugin_parity.py:38`) re-copied from the reverted guide after both the "Other commands" and the "Orca coordination" reverts (if part (b) landed in a follow-up PR, revert and re-copy there too). `_EXPECTED_IDS` (`tests/core/test_how_we_work_routing_table.py:56-97`) is not touched by Phase 1 (step 1.22; the test asserts a subset, `:204`), so it needs no revert, and no ID in it may be removed |
| Docs | 1.24, 1.24a, 1.24b | The `/sc:sweep` row and detail block in `docs/user-guide/commands.md`; `/sc:sweep` in the developer guide list (`:991`); the `CHANGELOG.md` entry is kept and a revert entry is added under `## [Unreleased]` |
| Gates | 1.25-1.27 | Re-run `make sync-dev`, `make verify-sync`, `make lint`, `uv run pytest`. Whether `make sync-dev` deletes the removed `.claude/` copies, and whether `superclaude install` deletes them from `~/.claude/`, is not verified: check `commands/sc/sweep.md` and `skills/sc-sweep-protocol/` in both places by hand. `.claude/` is never staged either way |

Reports already written stay where they are: they are dated local files under `--output` (default `<root>/.dev/sweeps/`), never posted (G7), and nothing reads them once the command is gone. The revert does not delete them; a person may delete them by hand.

WC-14 does not land on the working default alone: GQ-11 (WC-14 as a new ID, S9 row 9), with the WC-14 wording, is a hard gate in step 1.0b: steps 1.17-1.19 do not start until the owner's answer on GQ-11 is recorded; "working default accepted" counts only when the owner says it. Step 1.0b records the other owner decisions before 1A starts. If the owner later rejects WC-14 or its wording, the table above is the revert plan, and the sweep CLI may stay only if WC-14's G3 and the never-as-worker entry are reworded in the same change.

### Later phases (recorded only, not designed)

**[CONTRADICTION, sources disagree on phase grouping]** The issue summary groups the work as version 1 = `/sc:sweep` (about 20 h) plus `/sc:close` (about 14 h) plus the comment-3 research (about 6 h), and version 2 = signed grants plus the orchestrator of orchestrators (`.dev/issues/339/issue-summary.md:6`). The analysis splits it into Phase 1 = read-only sweep, Phase 2 = `/sc:close`, Phase 3 = trust layer plus orchestrator of orchestrators (`.dev/issues/339/analysis/analyze-worker-contract.md:60-62`). **Resolution:** this report follows the analysis grouping for Phases 1 and 2, because the owner's recorded first-PR scope is the read-only sweep alone (`seed-brief.md:53`; `analyze-worker-contract.md:60`), so `/sc:close` is not in the first PR. It departs from both sources by giving resume, the trust layer, the orchestrator of orchestrators and the management-server relay their own numbers, because the seed brief lists them as separate later phases (`seed-brief.md:70`, `:78`). The numbering is this report's, not a source's. Per `seed-brief.md:70`, each later phase is recorded with its blockers.

| Phase | One line | Blockers |
|---|---|---|
| Phase 2: `/sc:close` | A separate command that acts on the sweep's safe-to-close REVIEW rows (release terminals, remove worktrees) after the person confirms. In the issue summary's grouping this is version-1 work (`issue-summary.md:6`). | Turn the section 4 refusals into executed checks and add "all commits pushed" and the `.dev/tasks/` rule (analysis F4, F5, `analyze-worker-contract.md:35-36`, `:61`); removal only through `orca worktree rm` (`:36`); keep the user's named instruction plus confirmation at the moment of action (S4, `:54`); contract edits land after open PR #422 (F8, `:39`). |
| Phase 3: resume | Resume a stalled (proved) or frozen session from its contract and ledger as a new Task. | WC-6 (a retry is a new Task) and WC-10 (a late heartbeat is absence, never death) (`seed-brief.md:42`, `:58`; analysis F3, `analyze-worker-contract.md:34`); needs positive stall proof, never `unverifiable`. |
| Phase 4: trust layer | Trust for messages between sessions, as the sources define it: one permission mode for every session, fixed message types, and signed narrow grants (`issue-summary.md:10`, comment 2; `seed-brief.md:70`; analysis S1-S5, `analyze-worker-contract.md:51-55`). | `CCSESSION_PERMISSIONS=default` recreates the mode mismatch, so a launch rule must state its mode and refuse mixing (S1); fixed types already hold for Orca workers, the gap is the Claude Code cross-session channel (S2); no design, library or code for Macaroon or Biscuit grants (S3); comment-3 research and the Macaroon-versus-Biscuit adversarial debate first (`analyze-worker-contract.md:62`; `seed-brief.md:80`); comment 3's open questions on bypass marking and hook inspection (S5). |
| Phase 5: orchestrator of orchestrators | A coordinator that sweeps several coordinators' Runs. | Version-2 work (`issue-summary.md:6`); after the comment-3 research and debate (`analyze-worker-contract.md:62`). |
| Phase 6: management-server relay | Relay sweep results through a management server (meaning of "management server" is an owner question, GQ-66). | The owner's definition of "orchestrator management server" (`seed-brief.md:78`; analysis F14, `analyze-worker-contract.md:45`); no standing service is built in this work (`seed-brief.md:55`). |
| Not a source phase: bounded automatic recovery | If automatic recovery is ever added, bound it with an OTP-style restart budget and gate every action on Orca stop proof (web-01 rec. 5; Section 5.1, L1). This is external context recorded by this report, not the trust layer and not a phase any source names. | Phase 3 (resume) first; Orca stop proof only, never `unverifiable` or a late heartbeat (WC-10); an owner decision to add automatic actions at all (`seed-brief.md:53`). |

### 8.1 Gap traceability (synth-02 Section 4)

| Gap ID | Step(s) | How |
|---|---|---|
| G-A (GQ-01) | 1.4, 1.8 | One `worker-show` per row; list row used only for envelope and Dispatch id; row shape stays open (S9 row 1) |
| G-B (GQ-02) | 1.4, 1.5 | No `check`; questions from `blocked_question` and non-null `agentWait`; "Messages coverage: partial"; `check --peek/--all` gated later |
| G1 (GQ-04) | 1.17 | WC-14 keep-polling clause |
| G2 (GQ-05) | 1.17 | WC-14 re-arm clause |
| G3 (GQ-06) | 1.1-1.7, 1.17 | `superclaude sweep run` plus WC-14 cadence clause |
| G4 (GQ-07) | 1.2, 1.3, 1.17 | Section C classes in `models.py` / `classify.py`; WC-14 references WC-10, WC-6, `:108` |
| G5 (GQ-08) | 1.17 | One list of "tell the person" triggers, kept until answered |
| G6 (GQ-09) | 1.3, 1.4, 1.17 | Idle class and topics/orca-tabs readers; person-started sessions are reported (settled by the sources, Section 3.1 G6) |
| G7 (GQ-10) | 1.6, 1.15, 1.17 | `--output` dated file, never posted; a directory under `.dev/` is the working default, the exact directory is an owner decision (S9 row 8) |
| Static report writer | 1.5, 1.12 | `report.py` on the `495eb96d` skeleton |
| Read-only proof tests | 1.10, 1.11 | Allowlist and `side_effect=AssertionError` tests |
| Registries and suite gates | 1.20-1.28 | Registries, lint, scans, sync |
| K1 (GQ-18) | 1.4 | orca-tabs pane-key join |
| K2 (GQ-19) | 1.4 | Own scanner; `bootstrap_scan.sh` not reused |
| K3 (GQ-25) | 1.15, 1.16, 1.29 | PATH first, `uv run` second; pipx run stays open (S9 row 20) |
| K4 (GQ-23) | 1.1 | Lazy `__getattr__` export |
| GQ-37 | 1.3, 1.8 | Synthetic `exited` / `unverifiable` rows; real capture -> Open Questions |
| GQ-58 | 1.3, 1.9 | Null = no wait observed; absent = could not determine |
| GQ-40 | 1.3 | Non-null `parent` -> WC-13 review note |
| GQ-43 | 1.4, 1.10 | Plain `check` forbidden; runtime marking -> Open Questions |
| GQ-44, GQ-57, GQ-59 | 1.4 (gated addition) | Contracts-only default; probe -> Open Questions |
| GQ-48, GQ-56 | 1.5, 1.12 | Truncated-at-100 string |
| GQ-60 | 8 intro | Settled as A1 |
| GQ-61 | 1.5, 1.6, 1.12 | 6 h default bounds activity only; owner decision -> Open Questions |
| GQ-63 | 1.0b, 1.5 | Owner decision asked in step 1.0b before the step 1.5 format is built; stays in Open Questions until answered |
| GQ-21 | 1.4, 1.15 | No `git stash *` beyond `list`; no `ccsession --list` |
| GQ-15, GQ-16, GQ-17, GQ-22, GQ-36, GQ-38, GQ-39, GQ-41 | 1.3, 1.4 | Each unknown -> could not determine; facts -> Open Questions |
| GQ-46, GQ-47, GQ-49 to GQ-54, GQ-64, GQ-65 | 1.4, 1.5 | `inbox`, `--agent-wait` forbidden; "Answered: could not determine"; facts -> Open Questions |
| GQ-11, GQ-12, GQ-14, GQ-24, GQ-26, GQ-27, GQ-28 | 1.4, 1.15, 1.17, 1.19, 1.21, 1.24 | GQ-11 WC-14 as working default (owner decision, S9 row 9); GQ-12 pins; GQ-24 Other commands; GQ-27 `probes.py`; GQ-14, GQ-26, GQ-28 -> Open Questions |
| GQ-29 to GQ-35 | 1.5 | Tie-break by ID (GQ-29), all sources (GQ-31), root scope line (GQ-32), list everything (GQ-33), Approval "not observed" (GQ-34), pin `495eb96d` as working default (GQ-35, owner decision AMBIGUITY 9, S9 row 30); GQ-30 closure evidence and the GQ-34 mapping -> Open Questions |
| GQ-62 | 1.16a, 1.17-1.19 | Gated on #422: steps 1.17-1.19 land after #422 merges, or move to a follow-up PR (Dependencies row; owner decision, S9 row 52) |
| GQ-66, GQ-67, GQ-100 | 1.0b (GQ-100); later phases (GQ-66, GQ-67) | APPROVED.md D1-D5 read in step 1.0b before implementation; GQ-66 sent to Open Questions; GQ-67 settled by CR-01, the approved trigger rule (`seed-brief.md:42`, `APPROVED.md:25`, `CR-01-feature-worktree-hierarchy.md:12-21`), for any later phase that places workers |
| GQ-84 | 1.3, 1.9 | Exited + unreadable transcript -> could not determine |
| GQ-85 | 1.4, 1.10 | Full verb form pinned |
| GQ-86 to GQ-95, GQ-97 | 1.5 | Canonical Section C terms in report text |
| GQ-98 | 1.17 | New Task, never `--retry-of` |
| GQ-99 | 1.4, 1.10 | Per-sweep bounds: 50 `worker-show` calls, 90 s wall-clock under the 120 s Bash timeout; remaining rows "could not determine (call bound reached)", report still written (S9 row 63) |
| GQ-03 (resolved) | 1.4, 1.10 | NB-4 allowlist pinned by SC-2 |
| GQ-07, GQ-13, GQ-18, GQ-42 (resolved) | 1.3, 1.4, 1.15 | Vocabulary, `AUDIT_ROOTS`, pane-key join, plain read verbs |
| GQ-20, GQ-45, GQ-55 (resolved) | 1.3, 1.10 | `stage.activity`, `--unread`, `--format` excluded |
| GQ-68 to GQ-83 (resolved) | 1.3-1.16 | Built into the steps |
| GQ-96 (resolved) | 1.3 | Dimensions independent; blocked `/sc:implement` can be (a) and (b) when rule 1's condition holds (settled row, `report blocked` or Ruling halt; WC-3 `WORKER-CONTRACT.md:54-56`) |
| C1 | - | Sent to Open Questions |
| C2 | - | Sent to Open Questions (line-count note only: `test_how_we_work_routing_table.py` is 1202 lines, not about 360) |
| C3 | 1.4, 1.15, 8 intro | `git stash list` only; A4 rejected |
| C4 | 8 intro, 1.4, 1.6, 1.10 | Roots from Orca `terminal.worktreePath` and `--root`; with Orca down, `--root` scan of `.dev/tasks/{to-do,done}/*/` only, Orca sources `unscanned: orca unavailable` (tested in 1.10); 6 h, not 72 h |
| C5 | 1.3 | `stage.activity` never an input |
| C6 | 1.5 | Sweep sorts oldest first |
| C7 | 1.5 | Sweep prints `shown/total` |
| C9 | 1.6 | No `python -m` copied; UV forms only |
| C13 residual | 1.4, 1.10 | Full verb form |
| scope-02 `:146` | 1.4 | Claude Code path encoding in own scanner |
| scope-02 `:165` | 1.4 | `topics/*.txt` read directly |
| scope-01 `:100` | - | Settled in 4.6 (41 `def test_` verified; only the cross-references are stale); no step and no open question |
| scope-03 `:108`, `:111` | 1.14 | `issue.md` template |
| scope-03 `:165` | 1.27 | Suite scans run |
| scope-04 `:33` | - | Sent to Open Questions |
| 06 `:63`, `:85` | 1.10 | `--format` forbidden |
| 06 `:144` | 1.3 | Help reading of null `agentWait` |
| Option A4 | 8 intro | Rejected with reasons |
| S-01 to S-14 | - | Sent to Open Questions |

Gaps sent to Open Questions:

| Gap ID | Reason |
|---|---|
| GQ-37 | `unverifiable` / `exited` never captured; rules 2 and 7 need a live stalled-row capture |
| GQ-43 | Runtime read-marking of plain `check` [UNVERIFIED] (`message-check-handler.js:30`) |
| GQ-44, GQ-57, GQ-59 | `--peek` / `--all` side effects and `compatibilityAck` need a runtime-handler read or throwaway-Run probe |
| GQ-61 | 6 h versus 72 h is an open owner decision (AMBIGUITY 2) |
| GQ-63 | How a sweep report is exempted from `pragmatic` DONE/NEXT is an owner decision |
| GQ-15, GQ-16, GQ-17, GQ-22, GQ-36, GQ-38, GQ-39, GQ-41 | Orca field and shape facts [UNVERIFIED]; the plan only treats them as could not determine |
| GQ-46, GQ-47, GQ-49 to GQ-54, GQ-64, GQ-65 | Orca read and identity facts [UNVERIFIED]; the plan only forbids or labels them |
| GQ-14, GQ-26, GQ-28 | Whether tests require help registration, how `allowed-tools` patterns combine, whether UTILITIES is pinned: [UNVERIFIED] |
| GQ-30, GQ-34 | Closure evidence for a real session (`agent_focus.py:53`) and the `gate-list` Approval mapping are [UNVERIFIED] |
| GQ-62 | PR #422 sequencing is an owner decision; it gates steps 1.17-1.19 inside Phase 1 (step 1.16a), so the open part is only which of the two orders the owner picks |
| GQ-66, GQ-100 | Owner clarifications outside Phase 1 (GQ-100 is read before implementation). GQ-67 is not sent: CR-01 is the approved trigger rule (`seed-brief.md:42`, `APPROVED.md:25`) |
| G6 | None left to the owner: the sources settle that person-started sessions are reported (Section 3.1 G6); the WC-14 sentence is drafted in step 1.17 |
| C1, C2, scope-04 `:33` | Numbering, count and process notes in research files; no Phase 1 code or contract effect |
| S-01 to S-14 | Stale text in inventory, crash-recovery, #409 and research files; Phase 1 edits none of them (crash-recovery is not reused, #409 is pinned, not edited) |

### 8.2 Open Questions carried by the plan

Numbering: every row is keyed to its Section 9 row ("S9 row N"), the canonical open-question list.

| S9 row(s) | Question | Tag | Blocks |
|---|---|---|---|
| S9 row 20 | Does the bare `superclaude sweep` PATH form work under pipx (GQ-25)? | [UNVERIFIED] | Step 1.29 |
| S9 row 18 | Lazy versus eager package init (GQ-23); plan takes lazy | decision | Step 1.1 |
| S9 row 1 | Populated worker-list row shape (G-A, 05 Gap 1) | [UNVERIFIED] | Cheaper list-only classification |
| S9 row 2 | A non-consuming question read (G-B, 06 Gaps 1, 2, 17, 18) | [UNVERIFIED] | Gated `check --peek/--all` |
| S9 row 42 | Side effects of the `agentWait` / `--agent-wait` probe (06 Gap 10; GQ-51) | [UNVERIFIED] | `worktree ps --agent-wait` stays forbidden |
| S9 row 23 | Is the UTILITIES table pinned by a test (GQ-28) | [UNVERIFIED] | Step 1.24 test |
| S9 row 21 | How `allowed-tools` patterns combine (GQ-26) | [UNVERIFIED] | Step 1.15 |
| S9 row 39 | `inbox` read-marking (06 Gap 4; GQ-46) | [UNVERIFIED] | `inbox` stays forbidden |
| S9 row 29 | `gate-list` status to Approval mapping (GQ-34) | [UNVERIFIED] | Approval prints "not observed" |
| S9 row 15 | Fix `bootstrap_scan.sh` upstream or leave it (K2) | decision | none for Phase 1 |
| S9 rows 8, 9, 30, 51, 53 | Owner decisions: 6 h window (GQ-61), DONE/NEXT exemption (GQ-63), report directory (GQ-10, G7), add WC-14 or reuse the unused WC-1 ID (GQ-11), pinning the layout to unmerged `495eb96d` (GQ-35). Person-started sessions (G6, GQ-09, S9 row 7) are not an owner decision: the sources settle that they are reported (Section 3.1 G6). The plan uses working defaults for GQ-10 (under `.dev/`), GQ-11 (WC-14) and GQ-35 (`495eb96d`) until the owner decides; step 1.0b asks for all five before 1A and names the steps each blocks | decision | WC-14 rule id, default window, report directory, layout pin, report format (GQ-63) |
| S9 row 13 | `runtime_unavailable` exit code and shape (scope-02 OQ 3; GQ-16) | [UNVERIFIED] | Banner detection in step 1.4 |
| S9 row 98a | Six versus seven classes: the research question lists six (waiting on a person, working, stalled (proved), could not determine, finished, idle); Section C (`research-notes.md:188`, `:194`) keeps fenced as its own class (WC-12, `WORKER-CONTRACT.md:60`). Keep fenced, or fold it into could not determine (synth-02 4.8). The plan uses Section C's seven as the working default | decision | Steps 1.2, 1.3 (rule 3) and the SC-4 fenced tests |

### 8.3 External context used by the plan

All rows are external context from web research; none is a repository fact.

| Plan use | Source (web file) | URL |
|---|---|---|
| Separate "could not determine" from a negative state; absence never reads as death (steps 1.3, 1.5) | web-01 | https://kubernetes.io/docs/reference/node/node-status/ |
| Liveness versus readiness: "working" is not "healthy" (step 1.3) | web-01 | https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ |
| Fenced as a mark, not an eviction (step 1.3) | web-01 | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ |
| UNKNOWN as a first-class health answer (step 1.3) | web-01 | https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto , https://grpc.io/docs/guides/health-checking/ |
| UNKNOWN distinct from CRITICAL; tool errors are UNKNOWN (steps 1.4, 1.6) | web-01, web-02 | https://nagios-plugins.org/doc/guidelines.html , https://support.nagios.com/kb/article.php?id=72 , https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html |
| Supervisor observes, does not repair in Phase 1; restart budget deferred to "bounded automatic recovery" (later phases, not a source phase) | web-01 | https://www.erlang.org/doc/system/sup_princ.html |
| A silence threshold alone does not prove a stall (step 1.3, rule "stalled (proved)") | web-01 | https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html |
| Stuck detection needs a positive signal, not only a quiet heartbeat (step 1.3) | web-01 | https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md |
| Off-rail agent detection as a human review, not an automatic action (steps 1.5, 1.17) | web-01 | https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ |
| Context only, unfetched (D6): coordinator watchdog and session-troubleshooting pages, search results only (5.5); not support for any WC-14 clause. WC-14 G1 and G2 trace to the owner order of 2026-11-05 (GQ-04, `gaps-and-questions.md:27`), not to these pages | web-01 | https://docs.agents-fleet.ai/advanced/coordinator-resilience , https://www.simple-agent-manager.org/docs/guides/session-troubleshooting/ |
| Oldest-first ordering and blocked-item aging (step 1.5) | web-02 | https://kanbanguides.org/the-kanban-guide/2025.5/pdf/kanban-guide.v2025.5.en.pdf , https://prokanban.org/kpg |
| Honest `shown/total` when a list is truncated (step 1.5) | web-02 | https://github.com/cli/cli/issues/12196 |
| Per-component state plus one top line (step 1.5 header) | web-02 | https://support.atlassian.com/statuspage/docs/what-is-a-component , https://support.atlassian.com/statuspage/docs/top-level-status-and-incident-impact-calculations |
| Host and service states kept separate (session versus worktree dimension, step 1.3) | web-02 | https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/ |
| Hand-off structure: situation, action list, owner (report "tell the person" section, step 1.5) | web-02 | https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html |
| One clear owner of the ask; status page separate from the work (step 1.5) | web-02 | https://docs.pagerduty.com/ops-guides/incident-response-guide/incident-commander , https://docs.pagerduty.com/incident-management/communicate/external-status-page |
| Rejected: treating missing data as OK or as alerting (contradicts "absence never reads as death") | web-02 | https://grafana.com/docs/grafana/latest/alerting/guides/missing-data/ |
| Excluded: phi-accrual suspicion levels (web-01 rec. 6; one sweep has no sample history) | web-01 | https://nightlies.apache.org/pekko/docs/pekko/1.1.3/japi/org/apache/pekko/remote/PhiAccrualFailureDetector.html , https://dspace.jaist.ac.jp/dspace/bitstream/10119/4784/1/IS-RR-2004-010.pdf |

### 8.4 Contradictions noted

| # | Contradiction | Sources | Plan resolution |
|---|---|---|---|
| X-1 | Crash-recovery is described as read-only, but its allowed-tools permit `git stash *` (`SKILL.md:4`) | scope-02, synth-02 C3 | The sweep does not reuse crash-recovery; only `git stash list` is allowed (steps 1.4, 1.10) |
| X-2 | `~/workspace` versus `~/workspaces` as the worktree root | scope-02, synth-02 C4 | Roots come from Orca `terminal.worktreePath` and `--root`; no hardcoded root (steps 1.4, 1.6). With Orca down only the `--root` scan of `.dev/tasks/{to-do,done}/*/` remains (step 1.4; test in step 1.10) |
| X-3 | The `/sc:issue` design chose "No CLI" (`docs/designs/sc-issue-command.md:384`); A1 adds a CLI | scope-03, synth-04 | A1 needs deterministic, testable classification and a read-only proof (AssertionError patches for subprocess entry points, plus the new step 1.11 snapshot diff for the filesystem, which has no in-repo precedent); a prose-only skill cannot be pinned the same way. Recorded, not a blocker |
| X-4 | Null `agentWait`: Orca help reads it as "no wait", the guide text is less clear | 06 `:144`, synth-02 | Apply the split rule (guide reading for stop decisions, `06-orca-open-questions.md` Gap 19 `:144`): null is valid input for working but never stall proof; absent = could not determine (GQ-58, step 1.3), as S7 X-4 |
| X-5 | Bare `worker-list` in some research text versus the full `orca-ide orchestration worker-list` form | scope-03, synth-02 C13 | Full verb form only, pinned by SC-3 (steps 1.4, 1.10) |
| X-6 | Resolved, not a live contradiction: the gap count at `gaps-and-questions.md:125` reads "Open: 75. Resolved: 25" with GQ-03 resolved | `gaps-and-questions.md:125`; synth-02 4.5 GQ-03 row | None needed; counts agree with synth-02 Section 4 |
| X-7 | Number of session classes differs across research files | synth-02 4.8 | Section C's seven class names (the question's six, including idle, plus fenced, rule 3 at `research-notes.md:194`), assigned by precedence rules 1-7 plus the idle rule, are the working default (step 1.2); six versus seven stays an owner decision (S9 row 98a) |
| X-8 | 6 h versus 72 h window | synth-02 4.8, C4 | 6 h default bounds activity only; owner decision (S9 row 51) |
| X-9 | Nested workers: allowed in some text, a review item in WC-13 | synth-02 4.8 | Non-null `parent` is a WC-13 review note (GQ-40, step 1.3) |
| X-10 | Retry form: `--retry-of` versus a new Task | synth-02 4.8 | WC-6 wins: a replacement is a new Task (GQ-98, step 1.17) |
| X-11 | Missing data treatment (Grafana "OK/alerting" options versus UNKNOWN) | synth-02 4.8, web-02 | Grafana options rejected; could not determine (step 1.3) |
| X-12 | Stall heuristics (silence timeout) versus proof-only stall | synth-02 4.8, web-01 | Only "stalled (proved)" from positive evidence; silence alone is could not determine (step 1.3) |

### 8.5 Coverage of assigned files

| File | Key findings reflected | Where |
|---|---|---|
| `synthesis/synth-02-target-gaps.md` | Section 4 gaps G-A, G-B, G1-G7, K1-K4, GQ groups, C1-C13, S-01 to S-14; SC-1 to SC-16 | 8.1, Integration Checklist |
| `synthesis/synth-04-options-recommendation.md` | A1 chosen, A4 rejected; its open questions (7.1, keyed to S9 rows) | 8 intro, 8.2 |
| `research/scope-01-contract.md` | WORKER-CONTRACT rule layout, never-as-worker list at `:23`, WC-6 and WC-13 | 1.17-1.19 |
| `research/scope-02-orca-recovery.md` | Orca read verbs, path encoding (`:146`), topics files (`:165`), crash-recovery stash contradiction, `runtime_unavailable` | 1.4, X-1, X-2, S9 row 13 |
| `research/scope-03-cli-patterns.md` | Click group and lazy init pattern, registration point in `main.py`, `[name ...]` stderr prefix and exit 1, NB-4 allowlist (`:99`), command template (`:108`, `:111`), suite scans (`:165`) | 1.1-1.7, 1.14, 1.27 |
| `research/scope-04-409-layout.md` | Report skeleton (`:268-308`) pinned to `495eb96d`, dated file name | 1.5, 1.12 |
| `research/05-orca-row-schema.md` | List row lacks the needed fields (G-A); `worker-show` per row; `nextCursor` paging | 1.4, S9 row 1 |
| `research/06-orca-open-questions.md` | `check` consumes messages; `--peek/--all` single-mode rule; `--format`, `inbox`, `--agent-wait` forbidden; null `agentWait` | 1.4, 1.10, gated addition, S9 rows 2, 42, 39 |
| `research/web-01-agent-supervisor-session-health.md` | UNKNOWN as a state, proof-only stall, restart budget deferred | 8.3, later phases (bounded automatic recovery) |
| `research/web-02-static-status-report-conventions.md` | Oldest first, `shown/total`, separate dimensions, hand-off structure | 8.3, 1.5 |
| `gaps-and-questions.md` | GQ-01 to GQ-100 numbering; summary count at `:125` (Open 75 / Resolved 25) | 8.1, X-6 |

Excluded on purpose: phi-accrual (web-01 rec. 6, no sample history in a single sweep); OTP restart budgets (moved to the "bounded automatic recovery" row of the later-phases table, not the trust layer); `ccsession --list` (forbidden, GQ-21; overrides `seed-brief.md:33`, `:75`, `issue-summary.md:22` and `analyze-worker-contract.md:60`, which name it as an input, because it writes; Section 2.3); reuse of `bootstrap_scan.sh` (K2, own scanner instead; S9 row 15; crash-recovery's signals are still reused, per analysis F11, Section 2.3).

### Integration Checklist

- [ ] SC-1 No local write except the report: `tests/sweep/test_readonly.py` passes (step 1.11)
- [ ] SC-2 No Orca call outside the allowlist: `tests/sweep/test_probes_allowlist.py` passes (step 1.10)
- [ ] SC-3 Argv uses the full `orca-ide orchestration <verb>` form, with `orca-ide worktree ps --json` as the one named exception; exact argv tuples asserted (step 1.10)
- [ ] SC-4 Classification is deterministic and follows the precedence (step 1.9)
- [ ] SC-5 Absence never reads as death: absent or unreadable data gives could not determine (step 1.9)
- [ ] SC-6 Every class has a report home (step 1.12)
- [ ] SC-7 A waiting or open item stays listed while its source still shows it, whatever its age: `tests/sweep/test_report.py` passes (step 1.12); keeping it until the person answers is the WC-14 G5 coordinator duty (step 1.17)
- [ ] SC-8 Honest counts: `shown/total` and truncation string (step 1.12)
- [ ] SC-9 Real observation time in the header; "Messages coverage: partial" (step 1.12)
- [ ] SC-10 CLI registered: `superclaude sweep --help` works (steps 1.7, 1.13)
- [ ] SC-11 Routing registries updated (steps 1.20-1.24)
- [ ] SC-12 Contract tests pin WC-14 and never-as-worker (step 1.19)
- [ ] SC-13 `make lint` passes (step 1.26)
- [ ] SC-14 Suite-wide scans pass (step 1.27)
- [ ] SC-15 `make verify-sync` clean after `make sync-dev` (step 1.25)
- [ ] SC-16 PATH form works under pipx (step 1.29; [UNVERIFIED] until run, S9 row 20)
- [ ] End to end, live: `/sc:sweep` run in a coordinator session against a known Run (the step 1.4 live check through the skill path of step 1.15) writes one dated report under `.dev/sweeps/` whose headings follow the step 1.5 order (header with "READ ONLY", Sources, Waiting on a person (a) and (b), Retained problems, Sessions, Worktrees, Historical sessions, "Inspection only." footer); `task-list --ready --run <id> --json` and `worker-list --run <id> --json` captured immediately before and after show no Task or Dispatch status change caused by the sweep; captures and report path saved to the task package `artifacts/sweep-e2e.md`
- [ ] WC-14 matches G1-G7: each of G1 to G7 (Section 4) is stated in the WC-14 text added by step 1.17, checked item by item against the step 1.17 draft, and the step 1.19 `WC-14` phrase pins pass
- [ ] `uv run pytest tests/sweep/ tests/commands/ tests/core/ tests/skills/ tests/recommend/ -v` passes (step 1.27)
- [ ] `uv run ruff check` and `uv run ruff format --check` clean on `src/superclaude/cli/sweep/` and `tests/sweep/` (step 1.26)
- [ ] `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no new hit from `sweep.md` or `sc-sweep-protocol` (step 1.28)
- [ ] `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` is a byte copy of `src/superclaude/core/HOW-WE-WORK.md` (step 1.23)
- [ ] The developer guide's never-as-worker list (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:991`) names `/sc:sweep` and matches the step 1.18 line; the references at `:336`, `:394`, `:799`, `:993`, `:2203` re-read (step 1.24a)
- [ ] `CHANGELOG.md` has an `## [Unreleased]` entry for the sweep, `/sc:sweep`, WC-14 and the never-as-worker addition (step 1.24b)
- [ ] Only `src/` side staged; no `.claude/` path staged except `.claude/settings.json`
- [ ] `.dev/tasks/` staged with `git add .dev/tasks`

---

## 9. Open Questions

Issues that need resolving before or during implementation.

### 9.1 Open gaps-file rows (GQ IDs)

Every open GQ row is cited. Rows that share one resolution are grouped.

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 1 | GQ-01 (G-A, C10): what is the full `worker-list --run <id> --json` row schema? | Critical. The classifier cannot rely on list fields it has never seen. | Use the fallback of one `worker-show` per row (worst case ceil(N/100) list calls plus N show calls). Close only with a live `worker-list --run <id> --json` capture. |
| 2 | GQ-02 (G-B, C11): there is no non-consuming read of pending questions. | Critical. "Waiting on a person" may be missed. | Use the contract fallbacks (`blocked_question`, non-null `agentWait`, frozen plan). The report header says "Messages coverage: partial". |
| 3 | GQ-04 (G1): how does WC-14 state "keep polling"? | Critical. This is the coordinator duty the rule must carry. | Cite the memory note `coordinator-never-stop-polling.md` (owner order 2026-11-05, N-30) in WC-14. |
| 4 | GQ-05 (G2): how is the wait re-armed after an expiry? | WC-14 wording. | State re-arm after every expiry in WC-14. |
| 5 | GQ-06 (G3): the periodic sweep itself. | Critical. It is the feature. | Build `/sc:sweep` in Phase 1 as scoped. |
| 6 | GQ-08 (G5): when does the coordinator tell the person? | WC-14 wording. | Define the trigger in WC-14. |
| 7 | GQ-09 (G6, AMB 8): are person-started sessions in scope? | Scope of the "idle" class. | Settled by the sources, not an owner decision: in scope, observed and never messaged (`BUILD-REQUEST.md:12`; `seed-brief.md:66`, `:75`; analysis F2). AMBIGUITY 8's "limit Phase 1 to Orca workers" conflicts with them and is not followed. Idle applies only to person-started sessions. |
| 8 | GQ-10 (G7, AMB 3): where does the report go? | Output path. | Owner decision. |
| 9 | GQ-11 (AMB 4): add WC-14, or reuse the unused WC-1 ID? (Rules are WC-2 to WC-13; WC-1 is unused, `scope-01-contract.md:50`.) | Rule numbering. | Owner decision (step 1.0b). WC-14 is the working default. |
| 10 | GQ-12: the never-as-worker list and its tests. N-34: the "all_seven" test checks 8 entries. | A test name and its count disagree; adding `/sc:sweep` touches this test. | Read the test before editing and update the list and the test together. |
| 11 | GQ-14 [UNVERIFIED]: is the `/sc:help` and HOW-WE-WORK registration test-enforced? | A missed registry fails CI. | Read `tests/commands/test_help_command.py` in full before implementation. |
| 12 | GQ-15: what values can `liveness.reason` take? | Classifier inputs. | Capture live rows; treat unknown values as "could not determine". |
| 13 | GQ-16: what shape does `runtime_unavailable` have? | Error handling. | Capture the error once; copy it verbatim into the report. |
| 14 | GQ-17: how do heartbeat age and liveness relate? | Stall proof. | Never classify a stale heartbeat alone as stalled. |
| 15 | GQ-19 (K2): fix `bootstrap_scan.sh` or write a new scanner? Bugs at `:31` (encoding), `:73` (`.git` file), `:136` (JSON escaping). | Reuse choice. | Write the scan in the new CLI module. A4 (extend sc-crash-recovery) is rejected as [CODE-CONTRADICTED]. |
| 16 | GQ-21 (C3): exclude `git stash *` and `ccsession --list`. | Read-only guarantee. | Keep both out of the sweep. Read `topics/*.txt` directly instead of `ccsession --list` (it migrates names, `scope-02:165`). |
| 17 | GQ-22: what does `--include-remote` cost? | Runtime bound. | Keep `--include-remote` out of the default `worker-list` argv until its cost is measured (step 1.4, step 1.10 negative case); without it remote rows read `unverifiable` (`05:163`) and classify as could not determine. Measure its cost once with one run using the flag (step 1.4, `artifacts/include-remote-cost.txt`), then decide whether to add it to the allowlist; GQ-22 stays open until then. |
| 18 | GQ-23 (K4): lazy or eager `__init__`? `recommend` `__init__.py:12-20` versus `reflect` `:17-30`. | Package layout. | Pick one precedent and follow it. |
| 19 | GQ-24: "Other commands" table versus the excluded set (`test_how_we_work_routing_table.py:299-309`, N-37). | Registry test. | Add `sc:sweep` to `_OTHER_COMMANDS` and the table together. |
| 20 | GQ-25 (K3): pipx PATH form. | The command may not be found. | Bare `superclaude sweep` first, `uv run` fallback. Run `superclaude sweep --help` once outside a uv project. |
| 21 | GQ-26: how do `allowed-tools` patterns combine? | Permission surface. | Pin both `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)` in the space form used by the precedents (`sc-swarm-wizard-protocol/SKILL.md:7`, `sc-crash-recovery/SKILL.md:4`); see the resolved [CONTRADICTION] below. Stays open only for how command-level and skill-level patterns combine; verify on first run. |
| 22 | GQ-27: where does the probe module live? | Testability. | Use an `_orca(*args)` seam, after `reflect/config.py:64-78`. |
| 23 | GQ-28: is the UTILITIES table in `docs/user-guide/commands.md` pinned by a test? | Docs drift. | Add the row; enforcement is [UNVERIFIED] (`scope-03:140`). |
| 24 | GQ-29 (C6): #409 sort tie-break. | Report order. | Choose a deterministic tie-break and state it in the report. |
| 25 | GQ-30: closure evidence in the report. | Safe-to-close dimension. | Record the evidence per row. |
| 26 | GQ-31: per-source coverage line. | Honest reporting. | Print coverage per source in the header. |
| 27 | GQ-32: scope line. | Report header. | Print the worktree-tree root path as the scope line (`scope-04:360`; synth-05 step 1.5). Plan decision, open (`gaps:55`). |
| 28 | GQ-33 (C7): omission bound. | Truncation honesty. | List everything, so `<shown>/<total>` has shown equal to total; a source cut at 100 rows prints "at least 100 (truncated at 100), total could not determine" (`scope-04:361`; synth-05 step 1.5). Plan decision, open (`gaps:56`). |
| 29 | GQ-34 [UNVERIFIED]: Approval label and the `gate-list` mapping. | Approval column. | `gate-list` is now allowed (NB-4); the mapping stays [UNVERIFIED] until a live gate is captured. |
| 30 | GQ-35: pin the layout to `495eb96d` (unmerged). | Layout drift. | Owner decision (AMB 9). |
| 31 | GQ-36: shape of a non-null `agentWait`. | Waiting-on-a-person proof. | Capture a live waiting row. |
| 32 | GQ-37: `unverifiable` and `exited` never captured. | Important. Two liveness states are unseen. | Capture a live stalled row. |
| 33 | GQ-38: worker-list `page.hasMore` past 100 rows (proven only for an empty page). | Paging. | Page on `page.nextCursor` and pass `--run` (synth-05 step 1.4; `05:163`). |
| 33a | GQ-48: non-consuming message enumeration past 100 rows (`--all` and Run `--peek` cap at 100 with no cursor). | Truncation. | Report "at least 100 (truncated at 100), total could not determine" (synth-05 step 1.5). |
| 34 | GQ-39: `counts` keys. | Header totals. | Capture once; do not depend on unknown keys. |
| 35 | GQ-40 (C15): nested workers. The sweep-side rule is settled. | WC-13. | Report a non-null `parent` as a WC-13 violation. Row stays open for the Orca side. |
| 36 | GQ-41: CLI version of the research captures not recorded (captures predate 1.4.245). | Evidence age. | Stays open [UNVERIFIED]. No report header field is promised, because no verified read-only version source exists (`gaps-and-questions.md:82`). |
| 37 | GQ-43: does plain `check` mark messages read? | Read-only guarantee. | Treat it as draining; forbidden. |
| 38 | GQ-44: `--peek` / `--all` side effects. | Read-only guarantee. | Not used until proved. |
| 39 | GQ-46: inbox read-marking. | Read-only guarantee. | `inbox` stays forbidden (NB-4 fix log). |
| 40 | GQ-47: `reply` effects. | Out of scope for a read-only sweep. | Forbidden. |
| 41 | GQ-49 / GQ-50: `ask --dispatch-capability` and peer `ask --to run:<id>`. | Later phases. | Record only; not used in Phase 1. |
| 42 | GQ-51: side effects of the `--agent-wait` probe. | Read-only guarantee. | Excluded. |
| 43 | GQ-52: `agentWait` during `ask`. | Waiting proof. | Capture live. |
| 44 | GQ-53: there is no `caller` in `status --json`. | Coordinator identity. | Do not rely on it. |
| 45 | GQ-54: cross-host joins. | Remote sessions. | Report as "could not determine". |
| 46 | GQ-56: `check --all` and `run:<id>` rows; which end the 100-row cap keeps. | Truncation. | Not used; capture if needed later. |
| 47 | GQ-57: `legacyCompatibility.ackMessageIds` / `compatibilityAck`. | Hidden acknowledgement. | Read the runtime handler under `out/main/chunks/` or run a throwaway-Run test. |
| 48 | GQ-58: null `agentWait`, help text versus guide. | Classifier rule. | Null = no wait observed; absent = could not determine. |
| 49 | GQ-59: runtime-version or `legacyCompatibility` probe before trusting `--peek`. | Read-only guarantee for any later `check`. | No version probe in Phase 1: no read-only verb that reports the runtime version was found (`gaps-and-questions.md:82`). The default stays contracts-only and `check --peek` stays gated (synth-05 8.1, gaps sent to Open Questions). GQ-59 stays open until a runtime-handler read or a throwaway-Run probe settles it. |
| 50 | GQ-60 (AMB 1): where does the logic live? | Architecture. | Leaning A1 (CLI `superclaude sweep` plus a thin skill). A4 rejected as [CODE-CONTRADICTED]: `git stash *` in allowed-tools and bootstrap bugs; also the `~/workspace` path in `--all` mode and one allowlist entry (single-project mode uses the cwd). |
| 51 | GQ-61 (AMB 2): 6 h or 72 h window? | Default scope. | Owner decision (AMBIGUITY 2). 6 h is the working default; the window bounds activity only (N-41). |
| 52 | GQ-62 (AMB 5): sequencing with PR #422. | Merge conflicts; gates Phase 1 steps 1.17-1.19 (#422 edits `WORKER-CONTRACT.md`, `research-notes.md:307`). | Owner decision between the two orders: land 1.17-1.19 after #422 merges and this branch is rebased, or ship new files first and move 1.17-1.19 to a follow-up PR. Step 1.16a checks #422's state and files before step 1.17. |
| 53 | GQ-63 (AMB 6): pragmatic DONE/NEXT "No exceptions" (`pragmatic.md:22`, `:53`). | Report format conflict. | Owner decision. |
| 54 | GQ-64: does `identify` write? | Read-only guarantee. | Not used until proved. |
| 55 | GQ-65: `task-list` / `gate-list` row caps. | Truncation. | Apply the omission rule. |
| 56 | GQ-66 (AMB 10): what is the "management server"? | Later phase. | Record only. |
| 57 | GQ-67 (AMB 11): settled, not an open question. CR-01 is the approved child-worktree trigger rule (`seed-brief.md:42`; analysis F12, `analyze-worker-contract.md:43`; `APPROVED.md:25`): child worktrees only on triggers T1-T4 (`CR-01-feature-worktree-hierarchy.md:12-21`). The only residue is the status conflict: the CR-01 file header still says "PROPOSED" (`:3`); the report follows `APPROVED.md:25`. | Placement rule for later phases. | None for the owner; update the CR-01 header when the spec revision applies it. |
| 58 | GQ-84: fenced exclusion when the transcript is unreadable. | Class precedence. | Rule 2 needs the transcript read: exited, no `worker_done` and an unreadable transcript give could not determine (as synth-05 step 1.3 and `gaps-and-questions.md:107`). Not a WC-10 break. |
| 59 | GQ-85: mixed verb forms at `scope-03:99`. | Wording. | Use the `orca-ide orchestration <verb>` form (C13). |
| 60 | GQ-86 to GQ-95: wording residuals (`--unread` versus `--unread --peek`; `scope-01:64` calls safe-to-close a "class"; `06:57-58` tags help text CODE-VERIFIED; `06:187` stale summary; `filterLegacyPeekResult` on every peek; `scope-04:290`, `:320`; "needs a human"; `research-notes:175`, `:196` say G-A for G-B; `research-notes:241-242` say "MISSING"; a conservative default phrased as fact). | Low. Wording only. | Correct the wording in the final report; do not carry it into the plan. |
| 61 | GQ-97: citation residuals. | Low. | Re-cite at the Phase 5 synthesis gate. |
| 62 | GQ-98: `--retry-of` versus WC-6. | Contract wording. | Check WC-6 before WC-14 cites `--retry-of`. |
| 63 | GQ-99: N `worker-show` calls versus the batching policy. | Runtime cost. | The batching policy governs agent Bash round trips, not a CLI's internal subprocess calls. The plan sets per-sweep bounds instead (step 1.4: 50 `worker-show` calls, 90 s wall-clock budget under the 120 s Bash timeout; remaining rows "could not determine (call bound reached)", report still written; tested in step 1.10). The bound values stay open until one measured sweep confirms them. |
| 64 | GQ-100: APPROVED.md D1-D5 and the ccsession-tag README not verified. | Unread decisions. | Read both before implementation: APPROVED.md in Phase 1 step 1.0b. |

[CONTRADICTION: Component A (`synthesis/synth-06-questions-evidence.md`, row 21 / GQ-26) pins the allowed-tools patterns as `Bash(superclaude sweep:*)` and `Bash(uv run superclaude sweep:*)` (colon form).
Component B (`synthesis/synth-02-target-gaps.md` 3.1 and `synthesis/synth-05-implementation-plan.md` step 1.15) lists them as `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)` (space form).
Both versions presented for QA resolution.]

Resolution (Phase 6 QA, P6-01): the space form wins. Evidence: the cited precedents use the space form, `sc-swarm-wizard-protocol/SKILL.md:7` (`Bash(uv run superclaude swarm *)`) and `sc-crash-recovery/SKILL.md:4` (`Bash(git status *)`, `Bash(git stash *)` and others). Row 21 above, 3.1 and steps 1.15 and 1.16 now use `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)`. Both versions are kept above for the record.

### 9.2 [UNVERIFIED] and [CODE-CONTRADICTED] claims with no GQ row (gaps-file section (e))

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 65 | `scope-01:118`: is `test_help_command.py` coverage wider than the marker asserts (`:32-33`, `:41`)? | Registry test. | Read the file in full (same as GQ-14). |
| 66 | `scope-01:128`: the memory claim about peer sessions (F2) is UNVERIFIED. | Person-started scope. | Scope does not depend on it: GQ-09 is settled by the sources (row 7). F2 also rests on `WORKER-CONTRACT.md:11` and `orca-capabilities.md:148-151` (`analyze-worker-contract.md:33`); the memory claim stays UNVERIFIED. |
| 67 | `scope-02:115-117`: error rows (`runtime_access_denied`); a bare `orca` may launch the GNOME screen reader. | Wrong binary. | Always call `orca-ide`. |
| 68 | `scope-02:122`: `stale_status`. | Stall proof. | Print the `observedAt` age; never classify stale as stalled. |
| 69 | `scope-02:124`: executable-failure handling. | Error reporting. | Copy the error verbatim. |
| 70 | `scope-02:157`: reuse of `parse_session_log` (a reuse judgement). It reads the whole file and cannot prove a turn is final. | Stall proof. | Closed for Phase 1: tail the file for a note only. A missing `worker_done` in the transcript is never stall proof; rule 2 needs Orca liveness `exited` or an Orca-observed exit (WC-10, `WORKER-CONTRACT.md:45`), otherwise "could not determine". |
| 71 | `scope-02:165` (CC): `ccsession --list` writes (it migrates names). | Read-only guarantee. | Read `topics/*.txt` directly. |
| 72 | `scope-03:108` (CC, low): `recommend.md:2` is `name: sc:recommend`, not bare. | Frontmatter template. | Use the `reflect.md` / `issue.md` bare-name form. |
| 73 | `scope-03:111` (CC, low): `recommend.md` Activation block is not an "identical form". | Activation template. | Copy from `reflect.md:146-151`. |
| 74 | `scope-03:140`: enforcement of the docs command surface is UNVERIFIED. | Docs drift. | Same as GQ-28. |
| 75 | `scope-04:33` (CC, partial): the "generated files" list is wrong; `layouts/group_a.py` and `group_b.py` are hand-written. | Layout reuse. | Read the layout sources before reuse. |
| 76 | `06:15-16`: live-only behaviour not captured. | Classifier inputs. | Live capture. |
| 77 | `06:127-132`: wait semantics. | Waiting proof. | Live capture (GQ-36, GQ-52). |
| 78 | `06:100`: caller identity. | Coordinator identity. | Same as GQ-53. |
| 79 | `07:8`: runtime behaviour not exercised; handler reads prove only what the CLI sends. | All allowlisted verbs; the read-only claim is argv-level and local-filesystem only until probed. | Confirm read-only behaviour once on a throwaway Run: Phase 1 step 1.0a (`artifacts/readonly-probe.md`). |
| 80 | `research-notes:193`: the end-of-turn marker was never captured. | Stall proof. | Capture one; until then "could not determine". |
| 81 | `research-notes:186`: "unverifiable is absence" rests on guide text. | Liveness rule. | Confirm with a live row (GQ-37). |
| 81a | Phase 6 QA (P6-15): which Orca field, or which `worker-read --source transcript` literal, marks `consumer_fenced`? Section C names the worker's transcript or its `check` result (`research-notes.md:193-194`); `check` is never called (SC-2) and no fencing literal or field has been captured. | Rules 2 and 3: until answered, rule 3 matches synthetic fixtures only and an exited or settled row with no `worker_done` is could not determine (step 1.3). | Capture the transcript tail and `worker-show` JSON of one fenced dispatch on a throwaway Run; add the literal or field to step 1.4 and a captured fixture to step 1.8. |
| 81b | Phase 6 QA (P6-16): what literal does an `/sc:implement` `progress.md` ledger write for a `halt`, a `blocked` and a Ruling record? Only `T<id>: complete verdict=…`, `FINAL:` and `ARCHIVE:` are documented (`sc-crash-recovery/refs/pipelines.md:190`). | Rule 4 (b) ledger half and worktree-removable: until answered, policy prints "could not determine (ledger record format not known)". | Read the `sc-implement-protocol` ledger writer (`~/.claude/skills/sc-implement-protocol/`) or one halted package's ledger; add the literals to step 1.3 and a captured ledger fixture to step 1.8. |
| 81c | Phase 6 QA (P6-16): which Orca field, if any, says who created a Task? `task-list` returns `id`, `status`, `display_name`/`task_title`/`spec`, `assignee_handle`, `dispatch_id` (`07-gate-gap-fill.md:43`) and no creator. | Rule 4 (b) foreign ready Task (`WORKER-CONTRACT.md:129`): until answered, every ready Task is listed with "creator: could not determine". | Capture `task-list --ready --json` for a Task created by another handle and look for a creator key; if none exists, the coordinator's run notes are the only source, a later-phase input. |
| 81d | Phase 6 QA (P6-26): how many hours does Phase 1 take per sub-block (1A-1F), and does it fit the issue's "about 20" hours for `/sc:sweep` with the static report (`.dev/issues/339/issue-summary.md:6`)? No research file gives an hour estimate; the option grades L, M, M-L, M are relative judgment. | Option choice (Effort row) and Phase 1 scope. | Owner estimate per sub-block before step 1.1; if it exceeds about 20 hours, the owner cuts scope (for example defers the registry and routing steps 1.20-1.24 to a follow-up PR) or accepts the overrun. |

`scope-03:165` (the no-glob claim) is already struck as CC and resolved by B-21 / GQ-76.

### 9.3 Stale docs (gaps-file section (f))

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 82 | S-01 to S-06 [STALE DOC] in `orca-capabilities.md`: CLI 1.4.237 versus 1.4.245; guide 202 versus 215 lines; `:127` hasMore; `[H:worker-list]` line 22 default scope; `:97-102`; `ask` timeout 600000 ms; shifted guide line numbers. | Plans may cite stale behaviour. | Cite the 1.4.245 captures; refresh the doc separately. |
| 83 | S-07 [STALE DOC]: the issue-339 analysis file was rewritten (F1-F14 at `:32-45`, S1-S5 at `:51-55`). | F1-F12 citations moved (C1). | Use F1-F14 / S1-S5. |
| 84 | S-08, S-09 [STALE DOC]: crash-recovery SKILL.md claims "pure read-only" and uses a `~/workspace` path for `--all` and one dev-fallback allowlist entry (`SKILL.md:4`, `:25`, `:36`, `:53`; single-project mode uses the cwd, `:49-50`). | Supports rejecting A4. | Do not reuse; record as rejection reasons. |
| 85 | S-10 [STALE DOC]: #409 docs on age-ranking (the code does not sort). S-11 (omission counts) is revised: not stale, since docs and wide-view code agree (`agent_focus.py:17`, `:114`, `:127`); the two unbounded request lists are the only views without a count. | Layout rules. | Sort: follow the layout source, not the docs (GQ-29). Omission counts: follow both; bound the request lists (GQ-33). |
| 86 | S-12 [STALE DOC]: the `recommend` docstring. | Template copying. | Do not copy the docstring. |
| 87 | S-13, S-14 [STALE DOC]: `06:187` and `research-notes:241-242`. | Wording. | Same as GQ-89, GQ-94. |

### 9.4 Contradictions (gaps-file section (d) and web discrepancies)

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 88 | C1 (CC): F1-F12 numbering is out of date. | Wrong citations. | Use F1-F14 / S1-S5. |
| 89 | C2 (CC): the test file length; it is 1202 lines. | Citation accuracy. | Use 1202. |
| 90 | C4 (CC): the `~/workspace` path in `--all` mode and one allowlist entry; single-project mode uses the cwd. | A4 rejection reason. | Recorded under GQ-60. |
| 91 | C8 (UV): guide statements not checked against code. | Behaviour claims. | Treat as UNVERIFIED until captured. |
| 92 | C9 (CC): a `python -m` docstring. | Breaks the UV rule if copied. | Do not copy; use `uv run`. |
| 93 | C12: verified for one worker only. | Sample size. | Capture more rows (GQ-01). |
| 94 | web-01 D1 [EXTERNAL]: Kubernetes eviction. | Pattern mismatch. | Codebase wins. |
| 95 | web-01 D2 [EXTERNAL]: the Nagios KB says timeouts are not UNKNOWN, but web-02 says Icinga reports a plugin timeout as UNKNOWN. The two external sources disagree with each other. | Mapping of a probe timeout. | Codebase wins: a timeout is "could not determine". |
| 96 | web-01 D3 [EXTERNAL]: Harmonograf's "stuck". | Class naming. | Codebase wins: "stalled" only when proved. |
| 97 | web-01 D4 [EXTERNAL]: liveness restart. | Read-only sweep. | Codebase wins: the sweep never restarts. |
| 98 | web-02 [EXTERNAL]: Grafana's configurable no-data mapping contradicts WC-10. | Missing data handling. | Rejected; no data stays "could not determine". |
| 98a | Six versus seven classes (synth-02 4.8): the research question lists six (waiting on a person, working, stalled (proved), could not determine, finished, idle); Section C (`research-notes:188`, `:194`) keeps fenced as its own class, resting on WC-12 (`WORKER-CONTRACT.md:60`). Owner choice: keep fenced as a seventh class, or fold it into could not determine. | Classifier, report Class column, SC-4 tests. | Owner decision; the plan uses Section C's seven classes as the working default (Section 8.2, this row). |
| 98b | #409 DESIGN-CONTRACT rule 5 ("Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only.", `495eb96d:.../DESIGN-CONTRACT.md:11`) versus the seed brief's "recommended next action" per session (`seed-brief.md:66`), which also says the report "follows the #409 layout" (`:67`). Phase 1 prints recommendations (safe-to-close REVIEW, "new Task" resume, WC-14 item 8, optional "what to check next"). Added in the fidelity fix cycle. A further source position, recorded in the anti-omission fix pass: "The sweep must not propose stop/abandon/retry/release; those need positive proof and are coordinator decisions (`[G]:156-161`)." (`06-orca-open-questions.md:138`). Steps 1.15 (the skill recommends, never performs, the `WORKER-CONTRACT.md:74`, `:107` and WC-6 actions) and 1.17 (WC-14 closing sentence "The sweep only recommends ...") make the sweep propose those actions as text; the act stays a coordinator decision. | Report content; WC-14 item 8; steps 1.5, 1.15, 1.17. | Owner decision. The plan follows the seed brief as the working default (recommendations printed as text, never executed; the coordinator decides and performs every stop, abandon, retry, release, merge or removal); if the owner holds to rule 5 or adopts the `06:138` position, drop the recommendation text (step 1.15's recommend clause and step 1.17's closing sentence change as stated there) and keep the classes and dimensions. |
| 98c | Which #409 design to follow: #409 offers 20 alternative designs, says "User chooses the visual direction before any production integration" (`495eb96d:.../PLAN.md:62`) and provisionally prefers Signal Bridge / Proof Gate / Fleet Quilt and Leverage Board / Collision Lens / Revision Drift (`concepts.md:43-49`); this research selected header + Attention Ledger + Shift Brief (`codebase-context.md:55`). Added in the fidelity fix cycle. | Report layout (step 1.5). | Owner decision; the plan uses the research selection as the working default (2.5). |

### 9.5 AMBIGUITIES 1-11 (`research-notes.md:303-313`)

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 99 | AMB 1: where the logic lives (A1-A4). | Architecture. | GQ-60. |
| 100 | AMB 2: default window 6 h or 72 h. | Default scope. | GQ-61. |
| 101 | AMB 3: report location. | Output path. | GQ-10. |
| 102 | AMB 4: add WC-14, or reuse the unused WC-1 ID. | Contract conflict. | GQ-11. |
| 103 | AMB 5: PR #422 sequencing. | Merge order. | GQ-62. |
| 104 | AMB 6: pragmatic DONE/NEXT exception. | Report format. | GQ-63. |
| 105 | AMB 7: routing placement, `_POST_REFRESH_ADDITIONS` (`test_routing_refresh.py:33`), never-as-worker list. | Registry tests. | Add `"sweep"` to `_POST_REFRESH_ADDITIONS`; GQ-12, GQ-24. |
| 106 | AMB 8: person-started sessions. | Idle class scope. | GQ-09, settled by the sources (in scope; row 7). AMB 8's option to limit Phase 1 to Orca workers conflicts with `BUILD-REQUEST.md:12`, `seed-brief.md:66`, `:75` and analysis F2. |
| 107 | AMB 9: #409 pinning, tie-break, approval label. | Layout. | GQ-29, GQ-34, GQ-35. |
| 108 | AMB 10: "management server". | Later phase. | GQ-66. |
| 109 | AMB 11: worktree-first versus trigger-based placement (CR-01 / WC-11): settled by CR-01, the approved trigger rule (`seed-brief.md:42`, `APPROVED.md:25`). | Placement rule. | See row 57; no owner decision. |

### 9.6 Resolved rows and where they were resolved

| GQ rows | Where resolved |
|---------|----------------|
| GQ-03 (NB-4) | NB-4 fix pass, `qa/qa-nb4-fix-log.md` (2026-11-07); coordinator-approved exception at the Phase 3 research gate; re-checked at the Phase 5 synthesis gate. |
| GQ-07, GQ-13, GQ-18 (K1), GQ-20 (C5), GQ-42, GQ-45, GQ-55, GQ-96 | Marked resolved in `gaps-and-questions.md` with their resolution text. GQ-42's allowlist follow-up pointed at GQ-03. |
| GQ-68 to GQ-83 | Research-gate fix cycle (B-items, for example B-21 / GQ-76); `research/07-gate-gap-fill.md` covers B-04, B-07, B-09 and B-24. |
| C14 | Resolved in `gaps-and-questions.md` section (d). |

### 9.7 Gaps-section coverage per research file

| File | Gaps entries | Covered by |
|------|--------------|------------|
| `research/scope-01-contract.md` | Q1-Q7 | GQ-01, 11, 12, 10, 13, 14, 09 (rows 1, 9, 10, 8, 9.6, 11, 7) |
| `research/scope-02-orca-recovery.md` | Q1-Q9 | GQ-01, 15-22 (rows 1, 12-17, 9.6) |
| `research/scope-03-cli-patterns.md` | OQ1-OQ6 | GQ-23 to GQ-28 (rows 18-23) |
| `research/scope-04-409-layout.md` | Q1-Q8 | GQ-29, 02, 30-35 (rows 24-30, 2) |
| `research/05-orca-row-schema.md` | Gaps 1-10 | GQ-01, 36, 15, 37, 38, 39, 20, 40, 41, 42 |
| `research/06-orca-open-questions.md` | Gaps 1-19 | GQ-43, 44, 45, 46, 02, 47, 48, 49, 50, 51, 52, 17, 53, 54, 55, 40, 56, 57, 58 |
| `research/07-gate-gap-fill.md` | B-04, B-07, B-09, B-24 | Resolved rows (9.6); `07:8` and `07:92` caveats in rows 79 and 39 |
| `research/research-notes.md` | AMBIGUITIES 1-11, C1-C15, K1-K4 | 9.4, 9.5, rows 15, 18, 20 |
| `research/web-01-agent-supervisor-session-health.md` | D1-D4 | Rows 94-97 |
| `research/web-02-static-status-report-conventions.md` | Grafana no-data, I-PASS 403 | Row 98; I-PASS taken from the search excerpt (10, below) |

A file without a Key Takeaways list is not a defect and is not listed as one.

---

## 10. Evidence Trail

All research files produced during this investigation.

### Codebase Research

| File | Topic | Agent Type |
|------|-------|------------|
| `research/research-notes.md` (335 lines) | Research-phase notes: existing files, patterns, solution options A-D, recommended outputs, phases, AMBIGUITIES 1-11, C1-C15 | rf-task-researcher |
| `research/scope-01-contract.md` (152 lines) | Worker contract and its tests | Phase 2 codebase research agent |
| `research/scope-02-orca-recovery.md` (242 lines) | Orca state, crash-recovery and ccsession | Phase 2 codebase research agent |
| `research/scope-03-cli-patterns.md` (215 lines) | CLI, command and skill patterns; default argv allowlist (edited by the NB-4 fix pass) | Phase 2 codebase research agent |
| `research/scope-04-409-layout.md` (374 lines) | #409 observer layout for a static report | Phase 2 codebase research agent |
| `research/05-orca-row-schema.md` (206 lines) | Orca worker-list row schema (G-A) | Phase 2b gap-fill codebase agent |
| `research/06-orca-open-questions.md` (190 lines) | Orca open questions (G-B) | Phase 2b gap-fill codebase agent |
| `research/07-gate-gap-fill.md` (94 lines) | Research-gate gap fill for B-04, B-07, B-09, B-24 (fix cycle 1). Read-only: Orca `--help` on CLI 1.4.245-aidev02.780594c521aa and handler sources under `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/` | Research-gate fix agent |

### Web Research

All entries are [EXTERNAL]. Phase 4 web research used WebSearch and WebFetch because Tavily was unavailable.

| File | Topic |
|------|-------|
| `research/web-01-agent-supervisor-session-health.md` (229 lines) [EXTERNAL] | Supervisor and health-check patterns: Erlang/OTP, Kubernetes probes, phi accrual, "unknown" as a state, LLM agent patterns. 14 sources, some from search results only. Fallback note `[WEB_RESEARCH_FALLBACK: tavily=tool not loaded ...; used=WebSearch+WebFetch]`. Discrepancies D1-D4 resolved as "codebase wins". |
| `research/web-02-static-status-report-conventions.md` (63 lines) [EXTERNAL] | Static status report conventions. Backend WebSearch / WebFetch only (`fallback_reason: tavily_missing`). The research agent had no file-writing tool; the task executor saved its reply unchanged (logged under Deviations in the task file). The I-PASS AHRQ WebFetch returned 403, so that content is from the search excerpt. Grafana's no-data mapping is rejected (contradicts WC-10). |

### Synthesis files

- `synthesis/synth-01-problem-current-state.md` (299 lines)
- `synthesis/synth-02-target-gaps.md` (317 lines)
- `synthesis/synth-03-external-findings.md` (230 lines)
- `synthesis/synth-04-options-recommendation.md` (275 lines)
- `synthesis/synth-05-implementation-plan.md` (310 lines)
- `synthesis/synth-06-questions-evidence.md` (233 lines)

Assembler note (2026-11-07, history): the synthesis list was first reproduced from `synthesis/synth-06-questions-evidence.md`, which was written before synth-05 existed; its "planned" and "this file" parentheticals were replaced with line counts at the Phase 6 QA pass. Sections map to sources as follows: 1-2 from synth-01; 3-4 from synth-02; 5 from synth-03; 6-7 from synth-04; 8 from synth-05; 9-10 from synth-06.

### Gaps Log

- `gaps-and-questions.md`: GQ-01 to GQ-103; 78 open, 25 resolved (`:125`). GQ-03 (NB-4) was resolved by the NB-4 fix pass and is re-checked at the Phase 5 synthesis gate. GQ-101 (NB-2) and GQ-102 (NB-4c) are the two open blocking findings of the Phase 6 anti-omission gate, carried by owner decision (2026-11-08) to /sc:design; GQ-103 carries the 3 blocking /ponytail-review findings.

### QA reports

Count as of report assembly (end of the Phase 5 synthesis gate): 43 files in `qa/`, listed in the three bullets below (24 + 18 + `qa-nb4-fix-log.md`). The Phase 6 report-lens files (`qa-lens-*`, `qa-consolidated-findings-phase6.md`, `qa-fix-log.md`) were written after assembly and are not counted.

- Phases 2-3 and task validation (24 files): analyst completeness reports 1-2, analyst cross-validation reports 1-2, Phase 3 consolidated findings (initial and cycle 1), research evidence / gaps / qualitative reports 1-2, research fix logs (initial and cycle 1), research verification and qualitative verification (initial and cycle 1), task-research alignment report, task validation reports (B2, consolidated, structure, fix cycle 1, verify cycle 1).
- Phase 5 synthesis gate (18 files): analyst synthesis-accuracy reports 1-2 (`analyst-synthesis-accuracy-1.md`, `-2.md`), analyst synthesis-tracing reports 1-2 (`analyst-synthesis-tracing-1.md`, `-2.md`), `qa-consolidated-findings-phase5.md` and `qa-consolidated-findings-phase5-cycle1.md`, and 12 `qa-synthesis-*` files (content 1-2, structure 1-2, qualitative reports 1-2, fix logs initial and cycle 1, verification initial and cycle 1, qualitative verification initial and cycle 1).
- `qa/qa-nb4-fix-log.md`: the NB-4 fix pass (2026-11-07). NB-4 was a coordinator-approved exception at the Phase 3 research gate. Three edits (two at `scope-03:99`, one at GQ-03); the eight dependent lines checked all agree.
