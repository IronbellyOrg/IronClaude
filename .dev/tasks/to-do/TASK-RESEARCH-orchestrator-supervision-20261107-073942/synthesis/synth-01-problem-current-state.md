# Synthesis 01: Problem Statement and Current State Analysis

**Task:** TASK-RESEARCH-orchestrator-supervision-20261107-073942, Phase 5, Step 5.1
**Date:** 2026-11-07
**Research question context:** Orchestrator mode Phase 1 for issue #339: a read-only, coordinator-only `/sc:sweep` that classifies sessions (waiting on a person, working, stalled (proved), could not determine, finished, idle: the research question's six; Section C adds fenced as a seventh class, `research/research-notes.md:188`, and six versus seven is an open question, Section 9; safe-to-close is a separate dimension) over a default 6 h window that bounds activity only, writes a dated static report on the #409 layout, and adds a WC-14 coordinator-loop rule to `src/superclaude/core/WORKER-CONTRACT.md`; `/sc:close`, resume, the trust layer, an orchestrator of orchestrators and the management-server relay are later phases, recorded only. Option A4 (extend sc-crash-recovery) is [CODE-CONTRADICTED] and may appear only as a rejected option with its reason.

**Inputs:** `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `gaps-and-questions.md` (all paths relative to the task folder). NB-4 fix applied before synthesis (`qa/qa-nb4-fix-log.md`): the scope-03 default Orca read allowlist now includes `orchestration task-list`, `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden.

**Tag key:** [CODE-VERIFIED] checked against the named source (for a Markdown contract, the contract text and the tests that pin it, or a live CLI capture); [CODE-CONTRADICTED] the source says otherwise (corrected below to what the source shows); [UNVERIFIED] not confirmed, sent to Open Questions.

---

## 1. Problem Statement

- **The question.** How should IronClaude build Phase 1 of orchestrator mode (issue #339, https://github.com/IronbellyOrg/IronClaude/issues/339): a read-only `/sc:sweep` that only the coordinator runs? It should sort every Orca worker into a class (waiting on a person, working, stalled (proved), fenced, finished, could not determine; "idle" for person-started sessions only), report safe-to-close as a separate dimension, and look back over a default 6 h window that bounds activity only. It writes a dated static report on the #409 layout, and it needs a WC-14 coordinator-loop rule in `src/superclaude/core/WORKER-CONTRACT.md`. All of this must avoid breaking the Orca read rules (absence is never proof) and the repo's registries and tests. (`.dev/issues/339/issue-summary.md`; class names from `research/research-notes.md:188`, Section C.)
- **Why it matters.** #339 asks for one orchestrator session that every other session reports updates and questions through, so the person never has to open a child session. A static report of all agents, sessions and worktrees, modelled on #409, would replace the usual end-of-message table (`.dev/issues/339/issue-summary.md`). Today the contract has no rule that the coordinator keeps polling, re-arms its wait or sweeps on a schedule. No classification vocabulary is written down, and no command does any of this (`research/scope-01-contract.md` gaps G1-G7; `gaps-and-questions.md` GQ-04 to GQ-10). The issue estimates about 40 h of work, about 20 h of it for the sweep. It says most of the base model already exists as the Orca contract (`.dev/issues/339/issue-summary.md`).
- **Trigger.** Issue #339 plus three comments: never stop polling and own cleanup (comment 1, matching the owner order of 2026-11-05 in the memory note `coordinator-never-stop-polling.md`, `gaps-and-questions.md` GQ-04); a trust layer (comment 2); and a request to send the open questions to /tech-research and an adversarial debate (comment 3) (`.dev/issues/339/issue-summary.md`). Out of scope for Phase 1 and recorded only: `/sc:close` (worktree removal after strict checks), resume, the trust layer, an orchestrator of orchestrators, and the management-server relay. The summary also notes two sequencing constraints. Contract edits for #339 should land after open PR #422. The #409 design is on the unmerged branch `docs/409-orca-dashboard-designs` at `495eb96d` (`.dev/issues/339/issue-summary.md`).

---

## 2. Current State Analysis

### 2.1 The worker contract (`src/superclaude/core/WORKER-CONTRACT.md`)

The contract is a 203-line Markdown file, installed to `~/.claude/` by `src/superclaude/cli/install_core.py:27` [CODE-VERIFIED]. Its sections are Terms (:9), Command-side rules (WC-2, 4, 8, 9, 10, 11; :26), Worker duties (WC-3, 5, 7, 12, 13; :48), Coordinator (:64, WC-6 at :68) and the template (:166-203). The Coordinator section covers the brief (:77-97), worktrees (:101-108), git ownership (:110-118), reading a result (:120-129), the stop after `/sc:implement` (:131-152), fan-in (:154-156) and a worked example (:158-164). Rules WC-2 to WC-13 exist and WC-1 is unused, so WC-14 is the next free ID. Whether to add WC-14 or amend WC-1 is an owner decision (`gaps-and-questions.md` GQ-11).

Contract rules a sweep must obey [CODE-VERIFIED against the contract text and `tests/skills/test_worker_contract.py`]:

| Rule | Line(s) | What it means for a sweep |
|---|---|---|
| Person-started sessions are ordinary sessions | :11 | Not workers; "idle" is used only for them (Section C) |
| Never-as-worker list | :20, :23 | `/sc:sweep` is coordinator-only; adding it to the list changes `NEVER_AS_WORKER` (8 entries, `test_worker_contract.py:245-254`; phrase pinned at :86-92) |
| WC-8 / WC-13: no fan-out | :39, :61 | A worker never calls `worker-start`; a non-null worker-show `parent` is reported as a WC-13 violation for review (GQ-40) |
| WC-9 | :40, :43, :117 | Git and worker ownership bounds |
| WC-10: a missing heartbeat is absence | :45 | Act only on stall proofs; a late heartbeat never means stalled |
| WC-3: no heartbeat while blocked in `ask` | :54-57 | A silent worker may be waiting, not dead |
| WC-5: `blocked` maps to Orca outcome `failed` | :58 | Orca outcome alone cannot tell blocked from failed |
| WC-12: `consumer_fenced` | :60 | A fenced worker stops without `worker_done` by design |
| WC-6 | :70, :73, :74 | Coordinator duties when reading a stop |
| Child cleanup and the 5-condition refusal list | :107, :108 | Inputs to the later `/sc:close`, and to the safe-to-close dimension |
| Git ownership, placement map | :112, :114, :105 | Which session owns which tree |
| Reading a result (foreign ready Task) | :122-129 (:129) | A settled row is "finished" only after the return contract is read |
| Freeze after an implement stop | :133-136 | The "frozen or blocked by policy" kind of waiting on a person |
| Fan-in | :156 | Insertion point for WC-14 |

What the contract does not have (`research/scope-01-contract.md` G1-G7; `gaps-and-questions.md` GQ-04 to GQ-10). It has no rule that the coordinator keeps polling (G1), none to re-arm the wait after it expires (G2) and no periodic sweep (G3). It has no classification vocabulary (G4; now filled for the research by `research/research-notes.md` Section C, GQ-07 resolved). It has no rule for when to tell the person (G5), it does not say whether person-started sessions are reported (G6, an owner decision, GQ-09), and it does not say where the report goes (G7, an owner decision, GQ-10). A grep for poll, re-arm, cron, sweep and expire matches only :45. No sweep or close command exists. The candidate WC-14 insertion points are after :156 (before the worked example at :158) or after :129 (before :131).

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
  1. Contract read first (`worker_status: blocked` means waiting on a person).
  2. Stalled (proved), only with positive stop proof and no `consumer_fenced` evidence.
  3. Fenced.
  4. Waiting on a person: (a) explicit question, or (b) frozen or blocked by policy, including a foreign ready Task from `task-list --ready`.
  5. Working (`live`, `in_progress`, `agentWait` null).
  6. Finished (outcome settled plus a read contract, or "finished: guard refused").
  7. Could not determine (`unverifiable`, `agentWait` absent on an unsettled row, a latest turn not proved final, the 100-row cap).
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
| Scans this host's projects | `SKILL.md:4` hardcodes `~/workspace/IronClaude/...`, and `--all` runs `find ~/workspace -maxdepth 1` (`:53`). Projects and Orca worktrees live under `~/workspaces/` and `~/workspaces/worktrees/...`, so it finds none of them |
| `bootstrap_scan.sh` finds a project's session logs | `:31` replaces only `/`, while Claude Code replaces every non-alphanumeric character, so a path with `.` or `_` points at the wrong log dir |
| `bootstrap_scan.sh` reads git state for worktrees | `:73` tests `.git` as a directory; in a git worktree `.git` is a file, so every Orca worktree reports `is_repo` false |
| `bootstrap_scan.sh` emits valid JSON | `:136` escapes only partly, so a path with `"` or `\` gives malformed JSON |

`--since` defaults to 72 h (`SKILL.md:25-27`), which differs from #339's 6 h default. `parse_session_log.py` reads the whole transcript into memory (`:31-40`). It can show the latest assistant turn but cannot prove that turn is final, because it keeps no end-of-turn or process-exit signal (`:45-55`, `:85-102`). So a missing `worker_done` in that turn is stall proof only with separate final-turn proof; otherwise the row is could not determine (Section C rule 2).

**Rejected option A4 (extend or reuse sc-crash-recovery as the sweep).** A4 is rejected because it is [CODE-CONTRADICTED] by the rows above. The skill's tool allowance is not read-only (`SKILL.md:4`), its paths miss this host's projects (`SKILL.md:4`, `:53`), and its scanner fails on Orca worktrees and some paths (`bootstrap_scan.sh:31`, `:73`, `:136`) (`research/research-notes.md:160`; `gaps-and-questions.md` GQ-19). Nothing in this synthesis builds on A4. Whether a later phase fixes `bootstrap_scan.sh` or writes a new scanner is an open plan decision (GQ-19).

**ccsession** (`src/superclaude/skills/ccsession-tag/ccsession`, 1975 lines) [CODE-VERIFIED]:

- **Session store:** labelled sessions live at `~/.claude/projects/<name_key>/topics/<name>.txt`, each holding a session uuid (`:144`, `:175-222`).
- **Transcript lookup:** by uuid (`:1408-1411`).
- **`--list` output:** human-readable only, with no JSON form (`:1482-1580`).
- **`--list` is not read-only [CODE-CONTRADICTED]:** it first calls `ensure_names_migrated` (`:1787-1788`). That function moves and writes files when the marker `.ccsession-names-by-repo` (`:224`) is missing (`:285-287`). A read-only sweep reads `topics/*.txt` directly and never calls `ccsession --list` (GQ-21).
- **Orca join data:** `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/` (`:564`) holds one file per Orca pane key (`:` replaced by `+`). Each file has 3 lines: the Claude session id, the launch folder and the Orca terminal handle (`:558-605`). The pane-key to transcript join is verified for one worker, lc16 (GQ-18). Whether the sweep uses it for person-started sessions is GQ-09, an owner decision.

**Return contracts a sweep reads** [CODE-VERIFIED as contract text]:

- **Worker contract:** `<report-dir>/return-contract.yaml` (WC-4; shape at `WORKER-CONTRACT.md:32`). It holds `worker_status: succeeded | partial | failed | blocked`, plus `blocked_question` when blocked. WC-5 (`:58`) maps both `blocked` and `failed` to Orca outcome `failed`, so the sweep must read the YAML first.
- **Workflow package contract:** `.dev/tasks/to-do/<id>/return-contract.yaml` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3-19`). Under `--unattended` its worker variant has no `blocked` value (`:45-56`).

**Evidence:** `src/superclaude/skills/sc-crash-recovery/SKILL.md:4`, `:13`, `:25-27`, `:53`, `:91`, `:93-97`, `:134`, `:139-150`, `:155`; `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:120-125`, `:127-129`; `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:19`, `:52-68`, `:102-116`, `:177-201`; `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:31`, `:73`, `:136`; `src/superclaude/skills/sc-crash-recovery/scripts/parse_session_log.py:31-40`, `:45-55`, `:85-102`; `src/superclaude/skills/ccsession-tag/ccsession:144`, `:175-222`, `:224`, `:285-287`, `:558-605`, `:564`, `:1408-1411`, `:1482-1580`, `:1787-1788`; `src/superclaude/core/WORKER-CONTRACT.md:32`, `:58`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3-19`, `:45-56` (all via `research/scope-02-orca-recovery.md:18-26`, `:126-192`).

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
  - One subprocess seam, `_git` in `src/superclaude/cli/reflect/config.py:64-78` (used at `:158-159`).
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

Tally from scope-03: 58 VERIFIED, 3 CONTRADICTED, 3 UNVERIFIED.

**Evidence:** `src/superclaude/cli/main.py:18-26`, `:519-561`, `:564-565`; `src/superclaude/cli/recommend/__init__.py:12-20`; `src/superclaude/cli/reflect/__init__.py:17-30`; `src/superclaude/cli/reflect/contract.py:7`, `:397`; `src/superclaude/cli/reflect/config.py:64-78`, `:158-159`; `src/superclaude/cli/recommend/commands.py:34-48`, `:73-75`; `tests/recommend/test_cli_registration.py:1-39`; `tests/cli/reflect/conftest.py:58-80`; `tests/cli/reflect/test_contract_status_cli.py:44-66`; `src/superclaude/commands/issue.md:1-9`; `src/superclaude/commands/reflect.md:146-151`; `tests/recommend/test_routing_refresh.py:33`, `:38-40`, `:472`, `:647-648`; `Makefile:362-489`; `pyproject.toml:54`; `research/scope-03-cli-patterns.md:99`; `qa/qa-nb4-fix-log.md:12-18`, `:39-41`.

### 2.5 The #409 layout (observer design, `495eb96d:.dev/design/orca-observer-20261106/`)

The #409 package (PKG below) lives only on the unmerged branch `docs/409-orca-dashboard-designs` at commit `495eb96d`, and it is read with `git show`. Which version a sweep follows if it changes before merge is open (GQ-35). Everything in PKG about field names, IDs and sources is marked proposed only (`PKG/integration-gaps.md:20`, `:9-16`; `PKG/DESIGN-CONTRACT.md:11`). The facts below describe what the design draws [CODE-VERIFIED against the PKG files], not a running system.

| Element | What PKG shows | Source | Tag |
|---|---|---|---|
| Header | A title plus "SYNTHETIC · READ ONLY". The line "`<owners>` owners / `<sessions>` sessions / `<mapped>` mapped trees". A clock line with message coverage, worker age and check age | `PKG/canvas.py:73-77` | [CODE-VERIFIED]; the clock is hardcoded (`:77`) and the fixture `scope` object (`PKG/fixtures.py:21`) is never printed, although the contract says the header prints scope (GQ-32) |
| Footer | Disclaimer line | `PKG/canvas.py:81` | [CODE-VERIFIED] |
| Attention Ledger | Each question shows age, question, requester or owner, and affected IDs. A "SEEN IS NOT RESOLVED" count panel follows, with seven retained-context facts | `PKG/layouts/agent_focus.py:44-53` | [CODE-VERIFIED]. The docs call it "age-ranked" (`PKG/concepts.md:23`), but the code has no sort: [CODE-CONTRADICTED, partial] (`agent_focus.py:46`; tie-break GQ-29) |
| Shift Brief | A count with a "not an all-clear" coverage line, then per-request blocks (id / age / owner, question, affects or evidence), then failed / stale / frozen counts and an "Inspection only" line | `PKG/layouts/agent_focus.py:156-169` | [CODE-VERIFIED] |
| Data dictionary | Entities; ten independent state dimensions, each a closed value set (lifecycle, phase, health, approval, freshness, result, admission, evidence, policy, tests/review); a missing-evidence rule | `PKG/data-dictionary.md:7-15`, `:19-28`, `:50` | [CODE-VERIFIED] |
| Request definition | "Explicit synthetic human question, not inferred from any blocked status" | `PKG/data-dictionary.md:12` | [CODE-VERIFIED]; this is the basis for splitting waiting on a person into kinds (a) and (b) |
| Required semantics | Ten rules | `PKG/DESIGN-CONTRACT.md:11` | [CODE-VERIFIED] |
| Omission rule | "`shown/total` lines shown" | only in `listbox()`, `PKG/layouts/agent_focus.py:17` | The wide ledger and Shift Brief do not apply it: [CODE-CONTRADICTED] (`:46-50`, `:164-167`; GQ-33) |
| Message coverage | Complete non-consuming message enumeration is "not established" | `PKG/integration-gaps.md:11` | Still true for today's CLI (`research/06-orca-open-questions.md:183`) |

Neither #409 view lists every session and worktree. They render requests and counts only (`agent_focus.py:41-53`, `:156-169`). So the sweep's inventory table, with Class as a derived column and one source field per column, is DERIVED in `research/scope-04-409-layout.md:268-351` and not inherited from #409. It is a proposal for the plan, not current state. Its Approval column reads `gate-list` and its Owner column reads `run-list`, both allowed after NB-4 (2.4); the Approval value mapping stays [UNVERIFIED] (GQ-34). Open layout decisions: what counts as closure evidence (GQ-30), whether to print every source's coverage (GQ-31), the scope line (GQ-32) and the omission bound for a static file (GQ-33). Tally from scope-04: 3 CONTRADICTED, 0 UNVERIFIED.

**Evidence:** `495eb96d:.dev/design/orca-observer-20261106/canvas.py:73-77`, `:81`; `.../layouts/agent_focus.py:17`, `:41-53`, `:46-50`, `:156-169`; `.../concepts.md:23`; `.../data-dictionary.md:7-15`, `:12`, `:19-28`, `:50`; `.../DESIGN-CONTRACT.md:11`; `.../integration-gaps.md:9-16`, `:11`, `:20`; `.../fixtures.py:21` (all via `research/scope-04-409-layout.md:330-373`).

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
  | worker-show x N           |     | .dev/tasks/*/progress.md     |     |   terminal handle         |
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
         static report: header / Attention Ledger / Shift Brief (#409, 495eb96d, unmerged)
```

| Area | Exists today | Missing or blocked | Tag of the key fact |
|---|---|---|---|
| Worker contract | WC-2..WC-13 and the coordinator section (`WORKER-CONTRACT.md:64-164`), pinned by `tests/skills/test_worker_contract.py` | No poll, re-arm, sweep or tell-the-person rule; WC-14 is free (G1-G5, GQ-04 to GQ-08, GQ-11) | [CODE-VERIFIED] |
| Orca reads | Paged worker-list envelope; worker-show fields; run-list, run-current, task-list and gate-list allowed (NB-4) | Populated row shape (GQ-01); `unverifiable` and `exited` never captured (GQ-37); non-null `agentWait` shape (GQ-36); no non-consuming question read (GQ-02); `inbox` forbidden (GQ-46) | envelope and fields [CODE-VERIFIED]; row content [UNVERIFIED] |
| Work signals | `outcome`, `liveness`, `agentWait`, contract `worker_status` | `stage.activity` unusable; `terminalState` is not a class input | `activity` [CODE-CONTRADICTED] |
| Crash recovery | SAFE/REVIEW labels, a "could not determine" section, pipeline signals | Not read-only (`git stash *`), wrong `~/workspace` paths, scanner bugs at `bootstrap_scan.sh:31`, `:73`, `:136`; option A4 rejected (GQ-19, GQ-21) | [CODE-CONTRADICTED] |
| ccsession | `topics/*.txt` store; orca-tabs pane-to-session join (verified for lc16) | `--list` writes through migration, so it is excluded; peer-session reporting is an owner decision (GQ-09) | [CODE-VERIFIED] |
| CLI and commands | Click root plus deferred groups; the reflect model / contract / seam / commands split; read-only test patterns; registry list | No `sweep` group, command or skill; lazy or eager start (GQ-23); behaviour under pipx (GQ-25) | [CODE-VERIFIED] |
| #409 layout | Header, Attention Ledger, Shift Brief, ten dimensions, ten semantics rules | Unmerged; no sort; omission count only in `listbox`; no session or worktree inventory view (GQ-29 to GQ-35) | [CODE-VERIFIED] with 3 [CODE-CONTRADICTED] |

Excluded from Section 2 on purpose:

- Guide-only Orca statements, which are sent to Open Questions under the GQ IDs above:
  - the six `unverifiable` reason codes;
  - `liveness.reason`;
  - the worker-show verdict outranking the row;
  - remote rows reading `unverifiable` without `--include-remote`.
- The derived #409 inventory skeleton (a plan input, `research/scope-04-409-layout.md:268-351`).
- The `ccsession` and `bootstrap_scan.sh` reuse judgements, which are [UNVERIFIED] as judgements (`research/scope-02-orca-recovery.md:149`, `:157`).

**Evidence:** as cited in 2.1 to 2.5; `gaps-and-questions.md:22-70` (GQ-01 to GQ-47).

