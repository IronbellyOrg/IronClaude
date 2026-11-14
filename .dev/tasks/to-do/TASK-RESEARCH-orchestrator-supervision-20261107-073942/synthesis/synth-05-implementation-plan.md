# Synthesis 05: Implementation Plan (Orchestrator mode, issue #339)

| Field | Value |
|---|---|
| Step | Phase 5, checklist item 222 (Section 8 of the final report) |
| Recommended option | **A1** (`synthesis/synth-04-options-recommendation.md` Section 7) |
| Gap source | `synthesis/synth-02-target-gaps.md` Section 4 (4.2 to 4.7) |
| Research inputs | `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md`, `gaps-and-questions.md` |
| NB-4 note | Fixed before synthesis: the scope-03 default Orca read allowlist (`scope-03:99`) now includes `task-list`, `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden (`qa/qa-nb4-fix-log.md`) |
| Research question | Phase 1 is a read-only, coordinator-only `/sc:sweep` that classifies sessions (waiting on a person, working, stalled (proved), finished, could not determine, idle: the research question's six; Section C adds fenced as a seventh, the working default, OQ-13), reports safe-to-close as a separate REVIEW dimension, bounds activity (not open items) by a default 6 h window, writes a dated static report on the #409 layout, and adds WC-14 |

Tag conventions: only [CODE-VERIFIED] facts are used as current architecture in steps. [UNVERIFIED] items are listed in Open Questions (section 8.2) and appear in a step only as "treated as could not determine", "forbidden", or, for the guide-only `exited` verdict (GQ-37), as a rule input built and tested only against labelled synthetic fixtures until a live capture exists. `(new)` marks a file or directory that does not exist yet; each `(new)` directory's parent exists (`src/superclaude/cli/`, `src/superclaude/commands/`, `src/superclaude/skills/`, `tests/`, `tests/commands/` were checked). "External context" marks a step detail drawn from web research, with its URL in section 8.3. No source code is reproduced; steps name files, functions and lines.

## 8. Implementation Plan

Plan for **A1**: a Python CLI `superclaude sweep` (Click group in a new package `src/superclaude/cli/sweep/`), called by a thin command `/sc:sweep` and its skill `sc:sweep-protocol`, plus the WC-14 coordinator-loop rule. A pure classifier, a probe module with single `_orca` / `_git` seams, and a report renderer are tested with mocks; read-only behaviour is proved with the `side_effect=AssertionError` pattern.

Option A4 (extend `sc-crash-recovery`) is **rejected** [CODE-CONTRADICTED]: its allowed-tools hold `Bash(git stash *)` (`sc-crash-recovery/SKILL.md:4`), so it is not "pure read-only" (`SKILL.md:13`, `:155`; C3); it hardcodes `~/workspace/...` while this host uses `~/workspaces/...` (`SKILL.md:4`, `:25-27`, `:53`; C4); its default window is 72 h, not 6 h; and `bootstrap_scan.sh` mis-encodes project paths (`:31`), reports every Orca worktree as not a repo because `.git` is a file there (`:73`, `:82`), and hand-builds JSON (`:136`) (scope-02 `:130-149`, `:241`).

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
                  _git(*args)         no subprocess        the ONLY write (--output)
                  file readers        Section C precedence
                  (allowlist,         + safe-to-close
                   timeout 10,        dimension
                   fail closed)
```

### Phase 1: read-only `/sc:sweep`, registries, static report, WC-14

**Goal.** Ship a coordinator-only, read-only sweep that lists every session and worktree the coordinator can see, classifies each with the Section C precedence, prints safe-to-close as a separate REVIEW dimension, writes one dated Markdown report on the #409 layout, and pins the WC-14 coordinator-loop rule in the worker contract (gaps G1 to G7, G-A, G-B, K1 to K4; success criteria SC-1 to SC-16 in synth-02 3.2).

**Dependencies.**

| Dependency | Status | Evidence |
|---|---|---|
| Click CLI with deferred subcommand registration | exists | `src/superclaude/cli/main.py:555-561` (init-lite, reflect), `__main__` guard `:564-565` [CODE-VERIFIED] |
| Pure-module and seam patterns to copy | exist | `src/superclaude/cli/reflect/contract.py:7`, `:397`; `src/superclaude/cli/reflect/config.py:64-78`, `:103-109`; `src/superclaude/cli/recommend/__init__.py:12-20` (scope-03) [CODE-VERIFIED] |
| Read-only test patterns | exist | `tests/cli/reflect/test_contract_status_cli.py:44-66` (docstring `:18-22`); `tests/cli/reflect/conftest.py:17`, `:58-80`; `tests/recommend/test_cli_registration.py:1-39`; `tests/commands/test_issue_command.py:1-60` [CODE-VERIFIED] |
| Contract constants | exist | `RETURN_CONTRACTS` in `src/superclaude/contracts/__init__.py:204-206`; lint Check 11 forbids redeclaring them (`Makefile:467-476`) [CODE-VERIFIED] |
| Worker contract and its pins | exist | `src/superclaude/core/WORKER-CONTRACT.md` (WC-1 to WC-13; no WC-14 today); `tests/skills/test_worker_contract.py` [CODE-VERIFIED] |
| Orca CLI 1.4.245 read verbs | exist on the host | help text and captures in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/` (`lc16-show-4.json`, `lc17-show-1.json`, `lc01-show-1.json`, `lc01-step7.txt`) [CODE-VERIFIED shapes; populated worker-list row UNVERIFIED] |
| #409 layout | unmerged, pinned | commit `495eb96d` (`canvas.py:73-81`, `layouts/agent_focus.py:44-53`, `:156-169`, `data-dictionary.md:12-28`, `DESIGN-CONTRACT.md:11`) [CODE-VERIFIED at that commit] |

#### 1A. Package, classifier, probes, report, CLI

| Step | Action | Files | Details |
|---|---|---|---|
| 1.1 | Create the package with a lazy export | `src/superclaude/cli/sweep/` (new), `src/superclaude/cli/sweep/__init__.py` (new) | Lazy `__getattr__` export of `sweep_group`, following `src/superclaude/cli/recommend/__init__.py:12-20` (scope-03 recommends lazy over the eager `reflect/__init__.py:17-30`; K4 / GQ-23). No Orca client is started at import. |
| 1.2 | Define the data model | `src/superclaude/cli/sweep/models.py` (new) | Dataclasses for: a session row (the ten #409 dimensions of `data-dictionary.md:19-28` as independent fields, plus derived `cls`, `evidence`, `notes`); the seven canonical class names of `research-notes.md` Section C (B-28); a two-part safe-to-close value (terminal releasable; worktree removable); a source-coverage record (name, coverage, age, `unscanned:` reason). Unknown prints "unknown", missing results "not observed" (`scope-04:295`). |
| 1.3 | Write the pure classifier | `src/superclaude/cli/sweep/classify.py` (new) | "No Click, no subprocess", as `reflect/contract.py:7`, `:397`. One function applies the Section C precedence (`research-notes.md:190-202`): (1) contract `worker_status: blocked` -> waiting on a person (a); (2) `liveness.verdict` exited, an observed exit, or a turn proved final, with no `worker_done` **and** no `consumer_fenced` evidence -> stalled (proved) (`exited` is guide text only and has never been captured, GQ-37 [UNVERIFIED]; this rule is built against synthetic `exited` fixtures, step 1.8, and the live-capture check stays in Open Questions, 8.2); (3) `consumer_fenced` -> fenced (WC-12, `WORKER-CONTRACT.md:60`); (4) non-null `observation.agentWait` -> (a), frozen `/sc:implement` plan or Ruling halt (`WORKER-CONTRACT.md:133-136`) or a foreign ready Task (`:129`) -> (b); (5) live, `in_progress`, `agentWait` null -> working; (6) settled outcome **and** contract read, or a "guard refused:" body -> finished; (7) all else -> could not determine. Idle only for person-started sessions with no activity in the window. Rules fixed by the gaps: exited + no `worker_done` + unreadable transcript -> could not determine (GQ-84); `agentWait` null = no wait observed (valid for working, never stall proof), absent on an unsettled row = could not determine (GQ-58, help `[H:worker-show]:16` followed); `unverifiable`, late heartbeat, stale `evidence.liveStatus` or a missing row -> could not determine, never stalled (WC-10 `WORKER-CONTRACT.md:45`; SC-5); a just-dispatched worker with no signal -> working or could not determine, never idle (external context, web-01 rec. 3); a non-null `parent` (`lc16-show-4.json:115`) -> note "WC-13 violation, review" (GQ-40). Never inputs: `projection.stage.activity` (C5; stays "working" after settlement, `lc17-show-1.json:132`) and `resource.terminalState` for the class (`lc16-show-4.json:145-151`). Safe-to-close is computed separately: terminal releasable = `terminalState` reclaimable + `nextAction` release (`lc17-show-1.json`); worktree removable = none of the five refusal conditions at `WORKER-CONTRACT.md:108` and not frozen (`:133-136`). Both print as REVIEW, never run. |
| 1.4 | Write the probe module with the read allowlist | `src/superclaude/cli/sweep/probes.py` (new) | Single seams `_orca(*args)` and `_git(*args)` with `timeout=10`, failing closed to a "could not determine" result, as `reflect/config.py:64-78`, `:103-109` (GQ-27: module location decided here). Every Orca argv is `orca-ide orchestration <verb>` (C13; GQ-85; SC-3). Module-level allowlist (default, `scope-03:99` after NB-4): `worker-list --run <id> --include-remote --json` paged on `page.nextCursor` (100 rows, newest first, `[H:worker-list]` 3, 21); `worker-show --dispatch <id> --json`, one call per row (G-A / B-08; worst case ceil(N/100) + N calls); `worker-read --source transcript` (restart without cursor on `source_changed`); `task-list --ready` / `--run <id>`; `run-list` (paged, `--cursor`); `run-current`; `gate-list`; `worktree ps --json` **without** `--agent-wait`. Any other verb raises before the subprocess call. Git: `git -C <worktree>` with `status`, `log`, `branch`, `rev-parse`, `stash list` only (GQ-21; C3). A per-sweep call bound (GQ-99) stops further `worker-show` calls and marks the remaining rows could not determine with an `unscanned:` reason. Orca unavailable (`runtime_unavailable`) -> banner "Orca unavailable", disk sources still read, never `orca open` (scope-02 `:115`). Disk readers (plain file reads, no subprocess): `<report-dir>/return-contract.yaml` (WC-4, `WORKER-CONTRACT.md:30-38`; `blocked_question`); `.dev/tasks/*/progress.md`, sprint `results/phase-N-result.json`, `.roadmap-state.json`, MDTM frontmatter `status:` (crash-recovery `refs/pipelines.md:19`, `:52-68`, `:102-116`, `:177-201`); the pane-to-transcript map `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/<tabId>+<leafId>` (3 lines; `ccsession:564-605`; K1 / GQ-18, CODE-VERIFIED for one worker); labelled sessions `~/.claude/projects/<key>/topics/*.txt` read directly, never `ccsession --list` (it writes via `ensure_names_migrated`, `ccsession:285-287`, `:1787-1788`; GQ-21); transcripts `*.jsonl` read by tail, not whole (the `parse_session_log.py:31-40` whole-file limit). Own scanner instead of `bootstrap_scan.sh` (K2 / GQ-19): project dir key replaces every non-alphanumeric character with `-` (`ccsession:1301-1302`), and a `.git` file counts as a repo. Contract constants are imported from `superclaude.contracts`, never redeclared (Check 11). Acceptance: one measured sweep run with `--include-remote` records its cost (GQ-22 stays open until measured; remote rows read `unverifiable` without the flag, `05:163`). |
| 1.5 | Write the report renderer (the only write) | `src/superclaude/cli/sweep/report.py` (new) | Renders the DERIVED skeleton of `scope-04:268-308`, pinned to `495eb96d` (GQ-35): title "# Orchestrator sweep: <worktree-tree root>"; "READ ONLY . observed <real UTC time>" (#409 hardcodes its clock, `canvas.py:73-77`; external context, web-02); "Scope:" with the root path (GQ-32); "Sources:" listing every source's coverage and age (GQ-31) and "Messages coverage: partial" (G-B; `scope-04:276`). Sections in order: Waiting on a person (a) explicit questions, sorted oldest first by the sweep itself (C6; `agent_focus.py:46` has no sort), tie-break by ID (GQ-29), unknown age in a labelled group, never age 0 (external context, web-02 Kanban); Waiting on a person (b) frozen or blocked by policy, no question text ever (B-11); Retained problems (failed / stale / policy frozen, plus stalled (proved) and could not determine split into "evidence absent" and "source not read", external context web-01 rec. 1); Sessions (<shown>/<total>) with the ten dimensions, derived Class and safe-to-close REVIEW; Worktrees (<shown>/<total>); Historical sessions. Every list prints `<shown>/<total>` (C7; GQ-33: list everything, so shown equals total); a source cut at 100 rows prints "at least 100 (truncated at 100), total could not determine" (GQ-48 / GQ-56; external context web-02 gh CLI). Fixed strings: "Seen is not resolved", "Answered: could not determine" (GQ-47 / GQ-49), "Inspection only." footer (`canvas.py:81`). Approval column prints "not observed" until the `gate-list` mapping is verified (GQ-34, OQ-9). Column sources per `scope-04:336-351`. Open Tasks, questions and unread reports are always listed; the 6 h window bounds only activity rows (GQ-61; SC-7); person-wait time is excluded from activity ages and the activity window, while the waiting list prints and sorts on time since the wait began (`scope-04:87` "original age"; external context, web-01 rec. 4). Optional one-line "what to check next" text per waiting item, text only (external context, web-02 I-PASS). Report text uses the Section C class names only (GQ-86 to GQ-95, GQ-97). |
| 1.6 | Write the Click group | `src/superclaude/cli/sweep/commands.py` (new) | `sweep_group` with one subcommand `run` taking `--window` (default 6h), `--run <id>` (repeatable; default every Run from `run-list` / `run-current`), `--root <dir>` and `--output <dir>`. Prints the result as JSON with `click.echo(json.dumps(...))`; with `--output` it also writes `<dir>/<YYYYMMDD-HHMMSS>-sweep.md` through `report.py` (G7: a dated local file under `.dev/`, never posted). Errors: `[sweep ...]` prefix on stderr and `sys.exit(1)` (reflect pattern, scope-03). Never calls `orca open`, `check`, `ask`, `reply`, `send`, `inbox`. |
| 1.7 | Register the CLI | `src/superclaude/cli/main.py` | Add the two-line deferred import and `main.add_command(sweep_group, name="sweep")` after `:561` and before the `__main__` guard at `:564-565`, with the same `# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` comment as `:559` (SC-10). |

#### 1B. Tests (read-only proofs, classification, report, registration)

| Step | Action | Files | Details |
|---|---|---|---|
| 1.8 | Add seam fixtures and Orca captures | `tests/sweep/` (new), `tests/sweep/conftest.py` (new), `tests/sweep/fixtures/` (new) | `patch_orca` and `patch_git` fixtures that `monkeypatch.setattr` the `probes` module's `_orca` / `_git`, as `tests/cli/reflect/conftest.py:58-80` (`FIXTURES_DIR` as `:17`). Fixtures copied from `lc16-show-4.json` (live, working), `lc17-show-1.json` (failed, reclaimable, `nextAction` release), `lc01-show-1.json` (succeeded), `lc01-step7.txt` (empty `workers`, `page`, `scope`), plus hand-made rows for `exited`, `unverifiable`, non-null and absent `agentWait`, and a 100-row page; hand-made rows are labelled synthetic because no capture exists (scope-02 `:209-217`). `tmp_path` contract and ledger files as `tests/recommend/conftest.py:1-24`. |
| 1.9 | Classification tests | `tests/sweep/test_classify.py` (new) | One case per precedence rule 1-7 plus idle (SC-4), including fenced with `exited` (NB-1), `agentWait` null versus absent (GQ-58), guard-refused body, exited + unreadable transcript -> could not determine (GQ-84), blocked contract with Orca outcome `failed` -> waiting on a person (WC-5 `WORKER-CONTRACT.md:58`), and no path to stalled without stop proof (SC-5). Safe-to-close cases for each of the five `:108` conditions and the `:133-136` freeze. |
| 1.10 | Allowlist tests | `tests/sweep/test_probes_allowlist.py` (new) | Record every `_orca` argv during a full sweep over fixtures and assert each is `orca-ide orchestration <verb>` (SC-3) and on the allowlist (SC-2). Negative cases that must fail: `check` in any form, `--ack`, `--wait`, `--unread`, `--format`, two or more of `--unread`/`--peek`/`--all`, `reply`, `ask`, `send`, `inbox`, `worktree ps --agent-wait`, any unknown verb. Git argv limited to the five read forms; `stash` only with `list`. |
| 1.11 | Read-only proof | `tests/sweep/test_readonly.py` (new) | Inside `CliRunner.isolated_filesystem()`, patch the write entry points (`subprocess.run` outside the seams, `pathlib.Path.write_text` outside the report path, `os.remove`, `shutil.rmtree`, `shutil.move`) with `side_effect=AssertionError(...)`, as `tests/cli/reflect/test_contract_status_cli.py:44-66`; assert the only created file is the dated report under `--output` (SC-1). |
| 1.12 | Report tests | `tests/sweep/test_report.py` (new) | Rendered headings in skeleton order; every class reachable in the Class column, stalled (proved) and could not determine also under Retained problems (SC-6); an open Task older than 6 h still listed (SC-7); `<shown>/<total>` on every list and the truncated-at-100 string (SC-8); real UTC time and "Messages coverage: partial" in the header (SC-9); oldest-first with the labelled unknown-age group. |
| 1.13 | CLI registration test | `tests/sweep/test_cli_registration.py` (new); optional `tests/cli/test_cli_registration.py` | `CliRunner` `superclaude sweep --help` and `sweep run --help`, as `tests/recommend/test_cli_registration.py:1-39` (SC-10). Optionally add `sweep` to `EXPECTED_TOP_LEVEL_COMMANDS` (`tests/cli/test_cli_registration.py:31-49`). |

#### 1C. Command and skill

| Step | Action | Files | Details |
|---|---|---|---|
| 1.14 | Write the thin command | `src/superclaude/commands/sweep.md` (new) | Frontmatter `name: sweep` and section layout copied from `src/superclaude/commands/issue.md` (newest template; scope-03 `:108`, `:111` CC). Activation block: "**MANDATORY**: Before executing any protocol steps, invoke: > Skill sc:sweep-protocol", naming the installed path `~/.claude/skills/sc-sweep-protocol/SKILL.md` and the project `.claude/skills/` copy (dual surface; no `src/superclaude/` path). States coordinator-only, read-only, never as a worker. No `## Unattended mode` section (`_check_no_unattended_sections`, `tests/skills/test_worker_contract.py:464-472`). |
| 1.15 | Write the skill | `src/superclaude/skills/sc-sweep-protocol/` (new), `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (new) | `name: sc:sweep-protocol` (lint: the directory ends in `-protocol`, SC-13). Calls `superclaude sweep run` from PATH first, then `uv run superclaude sweep run` inside a dev checkout, as `sc-reflect-protocol/SKILL.md:63-64` (K3 / GQ-25; B-19 / NB-3). `allowed-tools`: Read, Glob, Grep, `Bash(superclaude sweep *)`, `Bash(uv run superclaude sweep *)` (precedent `sc-swarm-wizard-protocol/SKILL.md:7`); no `git stash *`, no `ccsession`, no `orca-ide` outside the CLI. Steps: run the sweep with `--output` under `.dev/`, read the report, print its path and the (a)/(b) counts, recommend (never perform) the `WORKER-CONTRACT.md:74`, `:107` and WC-6 actions. Reuses the crash-recovery SAFE/REVIEW labels and the "What I could not determine" section with `unscanned:` markers (`sc-crash-recovery/SKILL.md:91`, `:139-150`; report-template `:127-129`). Contains no write verb that the AC-0.9 audit would flag (`AUDIT_ROOTS` `test_worker_contract.py:1090-1094`, `WRITE_VERB_RE` `:1098`, `WRITE_VERB_CLASSIFICATION` `:1166`). |
| 1.16 | Static command test | `tests/commands/test_sweep_command.py` (new) | As `tests/commands/test_issue_command.py:1-60`: frontmatter, Activation block, installed skill path, no `src/superclaude/` path, PATH form before `uv run` and both forms in `allowed-tools` (static half of SC-16), no `## Unattended mode` heading. |

#### 1D. WC-14 and contract pins

| Step | Action | Files | Details |
|---|---|---|---|
| 1.17 | Add the WC-14 rule | `src/superclaude/core/WORKER-CONTRACT.md` | New `### WC-14. Coordinator loop` after the fan-in rule ending at `:156` and before `### Worked example` at `:158` (alternative: after `:129`, before `:131`; GQ-11: WC-14 is the working default, not a WC-1 clause, pending the owner decision, OQ-11). Clauses: G1 keep polling (owner order 2026-11-05); G2 re-arm an expired wait; G3 run `/sc:sweep` on a cadence; G4 the classes, by reference to WC-10, WC-6 and `:108`; G5 one list of "tell the person" triggers (the cases at `:126`, `:127`, `:129`, `:134`, `:156`), each kept until answered; G6 person-started sessions (scope per the owner decision, OQ); G7 the report is a dated local file under `.dev/`, never posted. States the sweep performs none of the `:74` / `:107` / WC-6 actions and only recommends them; a replacement is a new Task, never `--retry-of` (GQ-98). No runnable code spans in WC-14 (`_check_repo_setup_gated`, `tests/skills/test_worker_contract.py:446`). |
| 1.18 | Add `/sc:sweep` to never-as-worker | `src/superclaude/core/WORKER-CONTRACT.md` | Append `/sc:sweep` to the never-as-worker list at `:23`. |
| 1.19 | Pin WC-14 and never-as-worker | `tests/skills/test_worker_contract.py` | Add a `"WC-14"` entry to `RULE_PHRASES` under the `# Coordinator rules` comment at `:163` (picked up by the parametrized tests at `:540-542`, `:587-594`); add `/sc:sweep` to `NEVER_AS_WORKER` (`:245-254`, 8 entries today, each in `/sc:` form; test name at `:545` says "all seven"; rename it in the same change); update the `RULE_PHRASES["never-as-worker"]` phrase at `:86-92`; `_check_never_as_worker` (`:398-404`, called at `:545-546`) then checks that the `**Never-as-worker list**` line of `WORKER-CONTRACT.md`, edited in step 1.18, names `/sc:sweep` (SC-12; GQ-12). Keep `sweep` out of `UNATTENDED_COMMANDS` (`:379`). |

#### 1E. Routing registries and docs

| Step | Action | Files | Details |
|---|---|---|---|
| 1.20 | Recommend refresh registry | `tests/recommend/test_routing_refresh.py` | Add `"sweep"` to `_POST_REFRESH_ADDITIONS` at `:33` (asserted at `:647-648`; Activation block parsed at `:38-40`, `:472`) (SC-11). |
| 1.21 | HOW-WE-WORK "Other commands" row | `src/superclaude/core/HOW-WE-WORK.md` | Add a `/sc:sweep` row inside `<!-- other-commands:v1 -->` (`:318`) ... `<!-- /other-commands -->` (`:337`), ASCII only (test `:342-347`). GQ-24 decided: "Other commands", not the excluded set (`tests/core/test_how_we_work_routing_table.py:299-309`). Optional "Orca coordination" bullet after `:403` or `:405`, pinned as in `tests/core/test_orca_session_launch_guidance.py:14-16`. The level table (`src/superclaude/core/CLAUDE.md:65-82`) is not touched. |
| 1.22 | Routing-table registry | `tests/core/test_how_we_work_routing_table.py` | Add `"sc:sweep"` to `_OTHER_COMMANDS` (`:27-40`, checked at `:291-311`) (SC-11). |
| 1.23 | Plugin byte copy | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Copy the edited guide byte for byte (`tests/commands/test_routing_plugin_parity.py:38`). |
| 1.24 | User guide row | `docs/user-guide/commands.md` | Add a `/sc:sweep` row to the UTILITIES table (`:105`; `/sc:issue` row `:115`, detail `:347`) and a short detail block. Whether a test pins this table is [UNVERIFIED] (GQ-28, OQ-6). |

#### 1F. Gates

| Step | Action | Files | Details |
|---|---|---|---|
| 1.25 | Sync and verify | `Makefile` targets | `make sync-dev`, then `make verify-sync` (SC-15). Never stage `.claude/` copies. |
| 1.26 | Lint | `Makefile:362-489`, `pyproject.toml:203-206` | `make lint` (lint-architecture Checks 1 `:368-383`, 2 `:385-396`, 3/4 `:398-411`, 6 `:413-427`, 8 `:429-439`, 9 `:441-451`, 11 `:467-476`), then `uv run ruff check .` (ruff 0.15.20; no `anthropic` import) and `uv run ruff format --check src/ tests/` (SC-13). |
| 1.27 | Tests | `tests/sweep/`, `tests/commands/`, `tests/core/`, `tests/skills/`, `tests/recommend/` | `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend` (run line pattern `docs/designs/sc-issue-command.md:402`), then `uv run pytest`. Suite scans that must pass: `tests/skills/test_model_alias_policy.py:81-100`, `tests/commands/test_graph_command.py:219-225`, the AC-0.9 write-verb audit (SC-14). |
| 1.28 | Primitive path check | `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md` | `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`; justify or remove every new hit (CLAUDE.md installed-primitive rule). |
| 1.29 | PATH form under pipx | none (manual) | Run `superclaude sweep --help` once from a directory that is not a uv project (dynamic half of SC-16; [UNVERIFIED] until run, OQ-1). |

Gated later addition inside the sweep (not built in Phase 1): `check --peek` and `check --all` as separate argv, added to the allowlist only after a probe settles 06 Gaps 1, 2 and 18 (`message-check-handler.js:17`, `:30`, `:58-71`); the handler rejects more than one read mode (`message-check-handler.js:18-19`). Until then G-B stays "could not determine" and the contract fallbacks are the only question sources.

### Later phases (recorded only, not designed)

| Phase | One line |
|---|---|
| Phase 2: `/sc:close` | A separate command that acts on the sweep's safe-to-close REVIEW rows (release terminals, remove worktrees) after the person confirms. |
| Phase 3: resume | Resume a stalled (proved) or frozen session from its contract and ledger as a new Task. |
| Phase 4: trust layer | Bounded automatic recovery gated on Orca stop proof (external context: OTP-style restart budget, web-01 rec. 5). |
| Phase 5: orchestrator of orchestrators | A coordinator that sweeps several coordinators' Runs. |
| Phase 6: management-server relay | Relay sweep results through a management server (meaning of "management server" is an owner question, GQ-66). |

### 8.1 Gap traceability (synth-02 Section 4)

| Gap ID | Step(s) | How |
|---|---|---|
| G-A (GQ-01) | 1.4, 1.8 | One `worker-show` per row; list row used only for envelope and Dispatch id; row shape stays OQ-3 |
| G-B (GQ-02) | 1.4, 1.5 | No `check`; questions from `blocked_question` and non-null `agentWait`; "Messages coverage: partial"; `check --peek/--all` gated later |
| G1 (GQ-04) | 1.17 | WC-14 keep-polling clause |
| G2 (GQ-05) | 1.17 | WC-14 re-arm clause |
| G3 (GQ-06) | 1.1-1.7, 1.17 | `superclaude sweep run` plus WC-14 cadence clause |
| G4 (GQ-07) | 1.2, 1.3, 1.17 | Section C classes in `models.py` / `classify.py`; WC-14 references WC-10, WC-6, `:108` |
| G5 (GQ-08) | 1.17 | One list of "tell the person" triggers, kept until answered |
| G6 (GQ-09) | 1.3, 1.4, 1.17 | Idle class and topics/orca-tabs readers; whether to report them is an owner decision (OQ-11) |
| G7 (GQ-10) | 1.6, 1.15, 1.17 | `--output` dated file, never posted; a directory under `.dev/` is the working default, the exact directory is an owner decision (OQ-11) |
| Static report writer | 1.5, 1.12 | `report.py` on the `495eb96d` skeleton |
| Read-only proof tests | 1.10, 1.11 | Allowlist and `side_effect=AssertionError` tests |
| Registries and suite gates | 1.20-1.28 | Registries, lint, scans, sync |
| K1 (GQ-18) | 1.4 | orca-tabs pane-key join |
| K2 (GQ-19) | 1.4 | Own scanner; `bootstrap_scan.sh` not reused |
| K3 (GQ-25) | 1.15, 1.16, 1.29 | PATH first, `uv run` second; pipx run stays OQ-1 |
| K4 (GQ-23) | 1.1 | Lazy `__getattr__` export |
| GQ-37 | 1.3, 1.8 | Synthetic `exited` / `unverifiable` rows; real capture -> Open Questions |
| GQ-58 | 1.3, 1.9 | Null = no wait observed; absent = could not determine |
| GQ-40 | 1.3 | Non-null `parent` -> WC-13 review note |
| GQ-43 | 1.4, 1.10 | Plain `check` forbidden; runtime marking -> Open Questions |
| GQ-44, GQ-57, GQ-59 | 1.4 (gated addition) | Contracts-only default; probe -> Open Questions |
| GQ-48, GQ-56 | 1.5, 1.12 | Truncated-at-100 string |
| GQ-60 | 8 intro | Settled as A1 |
| GQ-61 | 1.5, 1.6, 1.12 | 6 h default bounds activity only; owner decision -> Open Questions |
| GQ-63 | - | Sent to Open Questions |
| GQ-21 | 1.4, 1.15 | No `git stash *` beyond `list`; no `ccsession --list` |
| GQ-15, GQ-16, GQ-17, GQ-22, GQ-36, GQ-38, GQ-39, GQ-41 | 1.3, 1.4 | Each unknown -> could not determine; facts -> Open Questions |
| GQ-46, GQ-47, GQ-49 to GQ-54, GQ-64, GQ-65 | 1.4, 1.5 | `inbox`, `--agent-wait` forbidden; "Answered: could not determine"; facts -> Open Questions |
| GQ-11, GQ-12, GQ-14, GQ-24, GQ-26, GQ-27, GQ-28 | 1.4, 1.15, 1.17, 1.19, 1.21, 1.24 | GQ-11 WC-14 as working default (owner decision, OQ-11); GQ-12 pins; GQ-24 Other commands; GQ-27 `probes.py`; GQ-14, GQ-26, GQ-28 -> Open Questions |
| GQ-29 to GQ-35 | 1.5 | Tie-break by ID (GQ-29), all sources (GQ-31), root scope line (GQ-32), list everything (GQ-33), Approval "not observed" (GQ-34), pin `495eb96d` as working default (GQ-35, owner decision AMBIGUITY 9, OQ-11); GQ-30 closure evidence and the GQ-34 mapping -> Open Questions |
| GQ-62, GQ-66, GQ-67, GQ-100 | Later phases | Sent to Open Questions |
| GQ-84 | 1.3, 1.9 | Exited + unreadable transcript -> could not determine |
| GQ-85 | 1.4, 1.10 | Full verb form pinned |
| GQ-86 to GQ-95, GQ-97 | 1.5 | Canonical Section C terms in report text |
| GQ-98 | 1.17 | New Task, never `--retry-of` |
| GQ-99 | 1.4 | Per-sweep call bound |
| GQ-03 (resolved) | 1.4, 1.10 | NB-4 allowlist pinned by SC-2 |
| GQ-07, GQ-13, GQ-18, GQ-42 (resolved) | 1.3, 1.4, 1.15 | Vocabulary, `AUDIT_ROOTS`, pane-key join, plain read verbs |
| GQ-20, GQ-45, GQ-55 (resolved) | 1.3, 1.10 | `stage.activity`, `--unread`, `--format` excluded |
| GQ-68 to GQ-83 (resolved) | 1.3-1.16 | Built into the steps |
| GQ-96 (resolved) | 1.3 | Dimensions independent; blocked `/sc:implement` can be (a) and (b) |
| C1 | - | Sent to Open Questions |
| C2 | - | Sent to Open Questions (line-count note only: `test_how_we_work_routing_table.py` is 1202 lines, not about 360) |
| C3 | 1.4, 1.15, 8 intro | `git stash list` only; A4 rejected |
| C4 | 8 intro, 1.6 | Roots from Orca `terminal.worktreePath` and `--root`; 6 h, not 72 h |
| C5 | 1.3 | `stage.activity` never an input |
| C6 | 1.5 | Sweep sorts oldest first |
| C7 | 1.5 | Sweep prints `shown/total` |
| C9 | 1.6 | No `python -m` copied; UV forms only |
| C13 residual | 1.4, 1.10 | Full verb form |
| scope-02 `:146` | 1.4 | Claude Code path encoding in own scanner |
| scope-02 `:165` | 1.4 | `topics/*.txt` read directly |
| scope-01 `:100` | - | Sent to Open Questions |
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
| GQ-62, GQ-66, GQ-67, GQ-100 | Sequencing and owner clarifications outside Phase 1 |
| G6 (owner half) | Whether the sweep reports person-started sessions at all is an owner decision |
| C1, C2, scope-01 `:100`, scope-04 `:33` | Numbering, count and process notes in research files; no Phase 1 code or contract effect |
| S-01 to S-14 | Stale text in inventory, crash-recovery, #409 and research files; Phase 1 edits none of them (crash-recovery is not reused, #409 is pinned, not edited) |

### 8.2 Open Questions carried by the plan

| # | Question | Tag | Blocks |
|---|---|---|---|
| OQ-1 | Does the bare `superclaude sweep` PATH form work under pipx (GQ-25)? | [UNVERIFIED] | Step 1.29 |
| OQ-2 | Lazy versus eager package init (GQ-23); plan takes lazy | decision | Step 1.1 |
| OQ-3 | Populated worker-list row shape (G-A, 05 Gap 1) | [UNVERIFIED] | Cheaper list-only classification |
| OQ-4 | A non-consuming question read (G-B, 06 Gaps 1, 2, 17, 18) | [UNVERIFIED] | Gated `check --peek/--all` |
| OQ-5 | Side effects of the `agentWait` / `--agent-wait` probe (06 Gap 10) | [UNVERIFIED] | `worktree ps --agent-wait` stays forbidden |
| OQ-6 | Is the UTILITIES table pinned by a test (GQ-28) | [UNVERIFIED] | Step 1.24 test |
| OQ-7 | How `allowed-tools` patterns combine (GQ-26) | [UNVERIFIED] | Step 1.15 |
| OQ-8 | `inbox` read-marking (06 Gap 4) | [UNVERIFIED] | `inbox` stays forbidden |
| OQ-9 | `gate-list` status to Approval mapping (GQ-34) | [UNVERIFIED] | Approval prints "not observed" |
| OQ-10 | Fix `bootstrap_scan.sh` upstream or leave it (K2) | decision | none for Phase 1 |
| OQ-11 | Owner decisions: report person-started sessions (G6), 6 h window (GQ-61), DONE/NEXT exemption (GQ-63), report directory (GQ-10, G7), WC-14 versus amending WC-1 (GQ-11), pinning the layout to unmerged `495eb96d` (GQ-35). The plan uses working defaults for GQ-10 (under `.dev/`), GQ-11 (WC-14) and GQ-35 (`495eb96d`) until the owner decides | decision | WC-14 G6 wording and rule id, default window, report directory, layout pin |
| OQ-12 | `runtime_unavailable` exit code and shape (scope-02 OQ 3) | [UNVERIFIED] | Banner detection in step 1.4 |
| OQ-13 | Six versus seven classes: the research question lists six; Section C (`research-notes.md:188`, `:194`) keeps fenced as its own class (WC-12, `WORKER-CONTRACT.md:60`). Keep fenced, or fold it into could not determine (synth-02 4.8). The plan uses Section C's seven as the working default | decision | Steps 1.2, 1.3 (rule 3) and the SC-4 fenced tests |

### 8.3 External context used by the plan

All rows are external context from web research; none is a repository fact.

| Plan use | Source (web file) | URL |
|---|---|---|
| Separate "could not determine" from a negative state; absence never reads as death (steps 1.3, 1.5) | web-01 | https://kubernetes.io/docs/reference/node/node-status/ |
| Liveness versus readiness: "working" is not "healthy" (step 1.3) | web-01 | https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/ |
| Fenced as a mark, not an eviction (step 1.3) | web-01 | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ |
| UNKNOWN as a first-class health answer (step 1.3) | web-01 | https://github.com/grpc/grpc-proto/blob/master/grpc/health/v1/health.proto , https://grpc.io/docs/guides/health-checking/ |
| UNKNOWN distinct from CRITICAL; tool errors are UNKNOWN (steps 1.4, 1.6) | web-01, web-02 | https://nagios-plugins.org/doc/guidelines.html , https://support.nagios.com/kb/article.php?id=72 , https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html |
| Supervisor observes, does not repair in Phase 1; restart budget deferred to Phase 4 | web-01 | https://www.erlang.org/doc/system/sup_princ.html |
| A silence threshold alone does not prove a stall (step 1.3, rule "stalled (proved)") | web-01 | https://nightlies.apache.org/pekko/docs/pekko/1.1.3/docs/typed/failure-detector.html |
| Stuck detection needs a positive signal, not only a quiet heartbeat (step 1.3) | web-01 | https://github.com/pedapudi/harmonograf/blob/main/docs/adr/0018-heartbeat-stuck-detection.md |
| Off-rail agent detection as a human review, not an automatic action (steps 1.5, 1.17) | web-01 | https://docs.camunda.io/docs/next/components/agentic-orchestration/evaluate-agents/detect-off-rail-agents/ |
| Coordinator resilience and session troubleshooting patterns (WC-14 G1, G2) | web-01 | https://docs.agents-fleet.ai/advanced/coordinator-resilience , https://www.simple-agent-manager.org/docs/guides/session-troubleshooting/ |
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
| X-1 | Crash-recovery is described as read-only but runs `git stash` commands beyond `list` | scope-02, synth-02 C3 | The sweep does not reuse crash-recovery; only `git stash list` is allowed (steps 1.4, 1.10) |
| X-2 | `~/workspace` versus `~/workspaces` as the worktree root | scope-02, synth-02 C4 | Roots come from Orca `terminal.worktreePath` and `--root`; no hardcoded root (steps 1.4, 1.6) |
| X-3 | The `/sc:issue` design chose "No CLI" (`docs/designs/sc-issue-command.md:384`); A1 adds a CLI | scope-03, synth-04 | A1 needs deterministic, testable classification and an AssertionError read-only proof; a prose-only skill cannot be pinned the same way. Recorded, not a blocker |
| X-4 | Null `agentWait`: Orca help reads it as "no wait", the guide text is less clear | 06 `:144`, synth-02 | Follow the help reading: null = no wait observed; absent = could not determine (GQ-58, step 1.3) |
| X-5 | Bare `worker-list` in some research text versus the full `orca-ide orchestration worker-list` form | scope-03, synth-02 C13 | Full verb form only, pinned by SC-3 (steps 1.4, 1.10) |
| X-6 | Resolved, not a live contradiction: the gap count at `gaps-and-questions.md:125` reads "Open: 75. Resolved: 25" with GQ-03 resolved | `gaps-and-questions.md:125`; synth-02 4.5 GQ-03 row | None needed; counts agree with synth-02 Section 4 |
| X-7 | Number of session classes differs across research files | synth-02 4.8 | Section C list (rules 1-7 plus idle) is the working default (step 1.2); six versus seven stays an owner decision (OQ-13) |
| X-8 | 6 h versus 72 h window | synth-02 4.8, C4 | 6 h default bounds activity only; owner decision OQ-11 |
| X-9 | Nested workers: allowed in some text, a review item in WC-13 | synth-02 4.8 | Non-null `parent` is a WC-13 review note (GQ-40, step 1.3) |
| X-10 | Retry form: `--retry-of` versus a new Task | synth-02 4.8 | WC-6 wins: a replacement is a new Task (GQ-98, step 1.17) |
| X-11 | Missing data treatment (Grafana "OK/alerting" options versus UNKNOWN) | synth-02 4.8, web-02 | Grafana options rejected; could not determine (step 1.3) |
| X-12 | Stall heuristics (silence timeout) versus proof-only stall | synth-02 4.8, web-01 | Only "stalled (proved)" from positive evidence; silence alone is could not determine (step 1.3) |

### 8.5 Coverage of assigned files

| File | Key findings reflected | Where |
|---|---|---|
| `synthesis/synth-02-target-gaps.md` | Section 4 gaps G-A, G-B, G1-G7, K1-K4, GQ groups, C1-C13, S-01 to S-14; SC-1 to SC-16 | 8.1, Integration Checklist |
| `synthesis/synth-04-options-recommendation.md` | A1 chosen, A4 rejected; OQ-1 to OQ-10 | 8 intro, 8.2 |
| `research/scope-01-contract.md` | WORKER-CONTRACT rule layout, never-as-worker list at `:23`, WC-6 and WC-13 | 1.17-1.19 |
| `research/scope-02-orca-recovery.md` | Orca read verbs, path encoding (`:146`), topics files (`:165`), crash-recovery stash contradiction, `runtime_unavailable` | 1.4, X-1, X-2, OQ-12 |
| `research/scope-03-cli-patterns.md` | Click group and lazy init pattern, registration point in `main.py`, `[name ...]` stderr prefix and exit 1, NB-4 allowlist (`:99`), command template (`:108`, `:111`), suite scans (`:165`) | 1.1-1.7, 1.14, 1.27 |
| `research/scope-04-409-layout.md` | Report skeleton (`:268-308`) pinned to `495eb96d`, dated file name | 1.5, 1.12 |
| `research/05-orca-row-schema.md` | List row lacks the needed fields (G-A); `worker-show` per row; `nextCursor` paging | 1.4, OQ-3 |
| `research/06-orca-open-questions.md` | `check` consumes messages; `--peek/--all` single-mode rule; `--format`, `inbox`, `--agent-wait` forbidden; null `agentWait` | 1.4, 1.10, gated addition, OQ-4, OQ-5, OQ-8 |
| `research/web-01-agent-supervisor-session-health.md` | UNKNOWN as a state, proof-only stall, restart budget deferred | 8.3, Phase 4 |
| `research/web-02-static-status-report-conventions.md` | Oldest first, `shown/total`, separate dimensions, hand-off structure | 8.3, 1.5 |
| `gaps-and-questions.md` | GQ-01 to GQ-100 numbering; summary count at `:125` (Open 75 / Resolved 25) | 8.1, X-6 |

Excluded on purpose: phi-accrual (web-01 rec. 6, no sample history in a single sweep); OTP restart budgets (moved to Phase 4); `ccsession --list` (forbidden, GQ-21); reuse of `bootstrap_scan.sh` (K2, own scanner instead; OQ-10).

### Integration Checklist

- [ ] SC-1 No local write except the report: `tests/sweep/test_readonly.py` passes (step 1.11)
- [ ] SC-2 No Orca call outside the allowlist: `tests/sweep/test_probes_allowlist.py` passes (step 1.10)
- [ ] SC-3 Argv uses the full `orca-ide orchestration <verb>` form (step 1.10)
- [ ] SC-4 Classification is deterministic and follows the precedence (step 1.9)
- [ ] SC-5 Absence never reads as death: absent or unreadable data gives could not determine (step 1.9)
- [ ] SC-6 Every class has a report home (step 1.12)
- [ ] SC-7 Waiting-on-a-person items kept until answered (steps 1.12, 1.17)
- [ ] SC-8 Honest counts: `shown/total` and truncation string (step 1.12)
- [ ] SC-9 Real observation time in the header; "Messages coverage: partial" (step 1.12)
- [ ] SC-10 CLI registered: `superclaude sweep --help` works (steps 1.7, 1.13)
- [ ] SC-11 Routing registries updated (steps 1.20-1.24)
- [ ] SC-12 Contract tests pin WC-14 and never-as-worker (step 1.19)
- [ ] SC-13 `make lint` passes (step 1.26)
- [ ] SC-14 Suite-wide scans pass (step 1.27)
- [ ] SC-15 `make verify-sync` clean after `make sync-dev` (step 1.25)
- [ ] SC-16 PATH form works under pipx (step 1.29; [UNVERIFIED] until run, OQ-1)
- [ ] `uv run pytest tests/sweep/ tests/commands/ tests/core/ tests/skills/ tests/recommend/ -v` passes (step 1.27)
- [ ] `uv run ruff check` and `uv run ruff format --check` clean on `src/superclaude/cli/sweep/` and `tests/sweep/` (step 1.26)
- [ ] `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no new hit from `sweep.md` or `sc-sweep-protocol` (step 1.28)
- [ ] `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` is a byte copy of `src/superclaude/core/HOW-WE-WORK.md` (step 1.23)
- [ ] Only `src/` side staged; no `.claude/` path staged except `.claude/settings.json`
- [ ] `.dev/tasks/` staged with `git add .dev/tasks`
