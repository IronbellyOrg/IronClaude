# Research Notes: Orchestrator mode (#339)
**Date:** 2026-11-07
**Scenario:** A
**Depth Tier:** Deep
**Status:** Complete

Research question: a coordinator session supervises every Orca / Claude Code session in one worktree tree. Phase 1 (owner decision, 2026-11-07, `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:17,53`) is a read-only, coordinator-only `/sc:sweep` that classifies sessions (idle, stuck, timed out, finished, needs-person) over a default 6-hour window and writes one dated static report on the #409 layout, plus coordinator-loop rules in `src/superclaude/core/WORKER-CONTRACT.md`. Later phases are recorded only: `/sc:close` with safety checks, resume, cross-session trust layer, orchestrator of orchestrators, management-server relay. Purpose: enrichment for `/sc:brainstorm --research deep`, then a design doc and implementation.

Inputs: `research/scope-01-contract.md` (147 lines), `research/scope-02-orca-recovery.md` (220), `research/scope-03-cli-patterns.md` (197), `research/scope-04-409-layout.md` (331), all `Status: Complete`; seed brief (80 lines). Paths below were re-checked on 2026-11-07 with `test -e` and `wc -l` from the worktree root; line numbers cited from the scopes were spot-checked where noted.

Tags: [CODE-VERIFIED] confirmed in the file named; [CODE-CONTRADICTED] the file shows otherwise; [UNVERIFIED] doc-only or not checked.

---

## EXISTING_FILES

Line counts are `wc -l` on 2026-11-07. "Cited by" names the scope file (S1-S4) or seed brief (SB). Status: OK = exists; MISSING = does not exist (all MISSING rows are planned Phase 1 outputs, not broken citations).

### Worker contract, routing guide and their tests (S1)

| Path | Lines | Purpose | Key exports / anchors | Cited by | Status |
|---|---|---|---|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md` | 203 | Orca coordinator/worker contract, installed to `~/.claude/` | Terms `:9`; never-as-worker list `:23`; WC-2..WC-13 (`:30-62`); section 4 coordinator rules `:64-164`; WC-10 liveness `:45`; WC-6 retry `:70-75`; cleanup refusal list `:108`; reading a result `:122-129`; fan-in `:156`; brief template `:166-203` | S1, S2, SB | OK |
| `src/superclaude/core/HOW-WE-WORK.md` | 405 | Routing guide | level table `:11-28`; "Other commands" `:314-337` (markers `:318`, `:337`); "Orca coordination" `:396-405` (re-read this session: never-workers bullet `:403`, end of file `:405`) | S1, S3 | OK |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | 405 | Byte copy of the guide | identical to core today (S1 `cmp`) | S1, S3 | OK |
| `src/superclaude/core/CLAUDE.md` | 136 | Installed framework CLAUDE.md | `### Orca session launches` `:45`; level-table copy `:65-82` | S1, S3 | OK |
| `src/superclaude/cli/install_core.py` | 177 | Core-file installer | `"WORKER-CONTRACT.md"` at `:27` | S1 | OK |
| `tests/skills/test_worker_contract.py` | 2265 | Pins contract text | `CONTRACT_PATH` `:19`; `RULE_PHRASES` `:25-237`; `NEVER_AS_WORKER` `:245-254`; `_check_rule` `:388-395`; `AUDIT_ROOTS` `:1090-1094` (re-read: skills, commands, agents); `WRITE_VERB_RE` `:1098-1101`; 41 `def test_` | S1 | OK |
| `tests/core/test_claude_md_routing_block.py` | 100 | Level-table byte copy check | `:28-32` | S1 | OK |
| `tests/commands/test_routing_plugin_parity.py` | 47 | Guide plugin byte copy; plugin command mirrors | `:38` `filecmp.cmp`; `:41-47` mirrors for help/recommend/workflow/implement | S1, S3 | OK |
| `tests/core/test_how_we_work_routing_table.py` | 1202 | Routing table and "Other commands" membership | `_OTHER_COMMANDS` `:27-40`; `_EXPECTED_IDS` `:56-97`; command resolution `:213-217`; set equality `:291-311`; ASCII rule `:342-347`. S1 called the file "~360 lines": [CODE-CONTRADICTED] it is 1202; the cited line ranges were not re-read | S1, S3 | OK |
| `tests/core/test_orca_session_launch_guidance.py` | 31 | Pins `core/CLAUDE.md` Orca launch section | section-slice pattern `:14-16` | S1 | OK |
| `tests/commands/test_help_command.py` | 62 | `/sc:help` level-table markers | `:32-41` | S1 | OK |

### Issue, decisions and Orca inventory (S1, S2, SB)

| Path | Lines | Purpose | Key anchors | Cited by | Status |
|---|---|---|---|---|---|
| `.dev/issues/339/issue-summary.md` | 33 | Issue #339 summary and cheatsheet | effort `:6`; open PR #422 `:27`; local research package `:28` | S1, SB | OK |
| `.dev/issues/339/analysis/analyze-worker-contract.md` | 72 | `/sc:analyze` findings F1-F14, S1-S5, 3-phase recommendation | findings table `:30-45`; security `:49-55`; recommend `:59-65`. S1 read a 55-line version with F1-F12: [CODE-CONTRADICTED] the file has since grown and its F-numbers moved (see AMBIGUITIES) | S1, SB | OK |
| `.dev/orca-command-refactor/inventory/orca-capabilities.md` | 188 | Orca 1.4.237 capability inventory (guide text cited as `[G]`, `[H:...]`) | ask/reply `:56-68`; question delivery via `check --wait --types ...question` `:63`; liveness and stall proof `:122-130`; peer sessions `:148-151`; open items `:177-186` | S2, SB | OK |
| `.dev/orca-command-refactor/decisions/APPROVED.md` | 90 | Decisions D1-D5 | not read by any scope | S1 | OK |
| `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md` | 54 | Child-worktree trigger rule | cited by analysis F12 `:43` | analysis | OK |
| `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md` | 80 | Owner constraints | constraints `:51-62`; success criteria `:64-71`; open questions `:73-80` | input | OK |
| `/home/coder/.claude/skills/orchestration/SKILL.md` | 68 | Orca discovery stub (outside repo) | `runtime_access_denied` `:64-66`; screen-reader warning `:37-39` | S2 | OK |
| `/opt/Orca/resources/bin/orca-ide` | 37 | Installed Orca CLI launcher (1.4.245 per S2) | help text read live by S2 | S2 | OK |

### Data sources a sweep reads (S2)

| Path | Lines | Purpose | Key anchors | Status |
|---|---|---|---|---|
| `src/superclaude/skills/sc-crash-recovery/SKILL.md` | 157 | Read-only crash sweep | `allowed-tools` `:4` (re-read: includes `Bash(git stash *)` and `~/workspace/IronClaude/...`); args `--all`/`--since 72h` `:25-27` (re-read: `~/workspace/`, 72 h); SAFE/REVIEW `:91`; "What I could not determine" `:139-150` | OK |
| `src/superclaude/skills/sc-crash-recovery/refs/investigators.md` | 171 | Investigator briefs | git-state `:101-126`; waves of 3 `:171` | OK |
| `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md` | 222 | Pipeline progress signals | roadmap `:52-68`; sprint `:102-116`; TASK-WF `progress.md` `:177-201` | OK |
| `src/superclaude/skills/sc-crash-recovery/refs/report-template.md` | 169 | Report shape | SAFE/REVIEW examples `:71-118`; conflicts `:120-125`; could-not-determine `:127-129` | OK |
| `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` | 170 | Per-project JSON scan | encoding bug `:31`; `.git`-is-dir bug `:73`; output keys `:143-169` | OK |
| `src/superclaude/skills/sc-crash-recovery/scripts/parse_session_log.py` | 128 | Transcript tail parser | reads whole file; output `{session_file, turns:[...]}` | OK |
| `src/superclaude/skills/ccsession-tag/ccsession` | 1975 | Labelled-session store and Orca tab map | `PROJECTS_DIR` `:144`; `list_sessions` `:1482-1580`; migration writes on `--list` `:285-287`, `:1787-1788`; `ORCA_TABS_DIR` `:564`; tab files `:558-605`; `CCSESSION_PERMISSIONS` `:135-139` | OK |
| `src/superclaude/skills/ccsession-tag/README.md` | 766 | ccsession docs | Orca launch text (S1) | OK |
| `/home/coder/.local/state/ccsession/orca-tabs/` | dir | Runtime pane-key to transcript map | 3-line files per pane key | OK |
| `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md` | 56 | Workflow package contract 1.1 and `--unattended` worker variant | `:3-19`, `:45-56` | OK |
| `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc16-show-4.json` | 212 | worker-show capture, working | `projection.*` `:127-159`; `terminal.*` `:165-181`; `agentWait` null `:180,185` | OK |
| `.../artifacts/lc17-show-1.json` | 219 | worker-show capture, failed | `nextAction` release `:153`; attention `failure` `:162-165` | OK |
| `.../artifacts/lc01-show-1.json` | 219 | worker-show capture, succeeded | attention `root_completion` | OK |
| `.../artifacts/lc01-step7.txt` | 47 | worker-list (empty `workers[]`) + worker-release receipt | envelope `ok/result.workers/counts/page/scope` | OK |
| `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` | 461 | worker-contract mapping table `:385` | grep hit only | OK |
| `src/superclaude/skills/sc-graph-protocol/SKILL.md`, `sc-impact-protocol/SKILL.md` | 165 / 193 | mapping tables `:112` / `:100` | grep hits only | OK |

### CLI, command and skill patterns (S3)

| Path | Lines | Purpose | Key exports / anchors | Status |
|---|---|---|---|---|
| `src/superclaude/cli/main.py` | 565 | Root Click group | `main()` `:18-26`; deferred registrations `:519-561`; `__main__` `:564-565` | OK |
| `src/superclaude/cli/recommend/__init__.py` | 20 | Lazy `__getattr__` package init | `recommend_group` `:12-20` | OK |
| `src/superclaude/cli/recommend/commands.py` | 461 | Click surface | `@click.group("recommend")` `:34-48`; JSON echo `:75`; `[group sub]` stderr + `sys.exit(1)` `:73-74`; `python -m` docstring claim `:40-41` [CODE-CONTRADICTED, no `__main__.py`] | OK |
| `src/superclaude/cli/reflect/__init__.py` | 30 | Eager package init | `:17-30` | OK |
| `src/superclaude/cli/reflect/config.py` | 394 | Owns every subprocess call | `_git()` `:64-78`; fail-closed callers `:103-109` | OK |
| `src/superclaude/cli/reflect/contract.py` | 420 | Pure module ("No Click, no subprocess") | `:7`, `:397` | OK |
| `src/superclaude/cli/reflect/models.py` | 182 | Dataclasses + `Verdict` enum | | OK |
| `src/superclaude/cli/reflect/commands.py`, `runner.py` | 585 / 834 | Click surface / runner | `shutil.which` preflight `commands.py:494`, `runner.py:387` | OK |
| `tests/cli/test_cli_registration.py` | 128 | Top-level command subset check | `EXPECTED_TOP_LEVEL_COMMANDS` `:31-49` | OK |
| `tests/recommend/test_cli_registration.py`, `conftest.py` | 39 / 24 | CliRunner registration test; `tmp_path` fixtures | | OK |
| `tests/cli/reflect/conftest.py` | 188 | `_git` monkeypatch fixture | `patch_git` `:58-80`; `which` patch `:95`; `FIXTURES_DIR` `:17` | OK |
| `tests/cli/reflect/test_contract_status_cli.py` | 292 | Read-only proof: forbidden entry points raise `AssertionError`, `isolated_filesystem()` | `:18-22`, `:44-66` | OK |
| `tests/cli/reflect/test_isolate_reviewers_cli.py`, `test_cli_smoke.py`, `test_preflight_phase_complete.py` | 168 / 326 / 182 | Other `_git`/`which` mocking examples | | OK |
| `tests/recommend/test_routing_refresh.py` | 690 | Command registry | `_POST_REFRESH_ADDITIONS` `:33`; assertion `:647-648`; Activation parse `:38-40`, `:472` | OK |
| `tests/commands/test_issue_command.py` | 129 | Static command-file test precedent | `:1-60` | OK |
| `tests/unit/test_cli_install.py` | 1106 | Install presence check (4 named commands only) | `:638-647` | OK |
| `src/superclaude/commands/issue.md`, `reflect.md`, `recommend.md`, `help.md`, `graph.md`, `README.md` | 100 / 305 / 138 / 135 / 81 / 12 | Command-file templates | issue section order `:22-95`; Activation `reflect.md:146-151`; scoped Bash `graph.md:9`; help reads tree live `help.md:30-34` | OK |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `sc-reflect-protocol/SKILL.md`, `sc-recommend/SKILL.md`, `sc-swarm-wizard-protocol/SKILL.md` | 155 / 1954 / 414 / 212 | Skill frontmatter; `uv run superclaude <group>` calls; scoped `allowed-tools` (`sc-swarm-wizard-protocol/SKILL.md:7`) | | OK |
| `Makefile`, `pyproject.toml`, `.pre-commit-config.yaml`, `.github/workflows/test.yml` | 560 / 216 / 145 / 200 | Build/lint/sync; `ruff==0.15.20` (`pyproject.toml:54`); banned `anthropic` import (`:203-206`) | | OK |
| `docs/designs/sc-issue-command.md` | 477 | Design-doc house format | 20 headings `:11-467` | OK |
| `docs/user-guide/commands.md` | 1516 | User guide; UTILITIES table `:105` | | OK |
| `src/superclaude/output-styles/pragmatic.md` | 234 | Mandatory DONE / NEXT table (analysis F10) | `:22`, `:53` (re-read in fix cycle 1; "No exceptions", no exception mechanism; `07-gate-gap-fill.md` A.1) | OK |
| `src/superclaude/hooks/scripts/launch-job-identity.sh` | 566 | PR #414 same-user job identity (analysis S3) | `:2-19`, `:21`, `:431-435` (sets no environment variables; identity is the file `~/.claude/state/launch-level/sessions/<id>`; `07-gate-gap-fill.md` A.2) | OK |

### #409 observer package (S4), committed only on unmerged commit `495eb96d`

Not on disk in this worktree. `git cat-file -t 495eb96d` = `commit`; `git ls-tree 495eb96d .dev/design/orca-observer-20261106/` lists `README.md`, `DESIGN-CONTRACT.md`, `PLAN.md`, `QA.md`, `concepts.md`, `data-dictionary.md`, `integration-gaps.md`, `canvas.py`, `fixtures.py`, `render.py`, `layouts/`, `agent-focus/`, `tests/`, `manifest.json`, `fixture.json` and others [CODE-VERIFIED]. Read with `git show 495eb96d:<path>`. Anchors: header `canvas.py:73-77`; footer `canvas.py:78-81`; Attention Ledger `layouts/agent_focus.py:41-53`; Shift Brief `:156-169`; `listbox()` omission count `:13-24`; state dimensions `data-dictionary.md:17-28`; required semantics `DESIGN-CONTRACT.md:10-11`; proposed-only boundary `integration-gaps.md:9-24`.

### Planned outputs that do not exist yet

| Path | Status |
|---|---|
| `src/superclaude/commands/sweep.md` | MISSING (planned) |
| `src/superclaude/commands/close.md` | MISSING (later phase) |
| `src/superclaude/cli/sweep/` | MISSING (planned if the CLI approach is chosen) |
| `src/superclaude/skills/sc-sweep-protocol/` | not created; S3 proposes this name |

## PATTERNS_AND_CONVENTIONS

### Contract and its pinning tests

- New coordinator rules go in section 4 of `WORKER-CONTRACT.md`. Proposed slot: a `### WC-14. Coordinator loop` after fan-in (ends `:156`) and before `### Worked example` (`:158`), or after `### Reading a result` (ends `:129`). WC-1 is unused; WC-14 is the next free ID (S1 "Contract structure"). [CODE-VERIFIED by S1 grep]
- Each pinned rule is one `RULE_PHRASES` entry `rule -> (identifier, [verbatim phrases])` under `# Coordinator rules` (`tests/skills/test_worker_contract.py:163`); the positive test (`:540-542`) and the negative removal test (`:587-594`) parametrize over it, so no new test function is needed. [CODE-VERIFIED by S1]
- Adding `/sc:sweep` to the never-as-worker list means editing `WORKER-CONTRACT.md:23`, the `"never-as-worker"` phrase (`test_worker_contract.py:86-92`) and `NEVER_AS_WORKER` (`:245-254`) together. [CODE-VERIFIED by S1]
- The write-verb audit scans `src/superclaude/skills`, `commands` and `agents` (`test_worker_contract.py:1090-1094`, re-read this session) for `git add|commit|push|merge|stash|update-ref|worktree add/remove` and `gh pr|api` (`:1098-1101`). A new `sweep.md` or `sc-sweep-protocol/SKILL.md` that names any of those verbs (even to forbid them, or as `git stash list`) needs a `WRITE_VERB_CLASSIFICATION` entry (`:1166-~2198`) with category `read-only` or `never-worker` (`:1103-1104`). This answers S1 open question 5. [CODE-VERIFIED]
- New contract lines must not put runnable code spans (`make ...`, `uv ...`, `bash ...`) without the setup-gate wording (`_check_repo_setup_gated`, `:446`). [CODE-VERIFIED by S1]

### Routing guide copies

- `HOW-WE-WORK.md` is byte-copied to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (`tests/commands/test_routing_plugin_parity.py:38`). Only the level table (`:11-28`) is also copied into `core/CLAUDE.md:65-82`; an edit to "Orca coordination" (`:396-405`) or "Other commands" (`:314-337`) does not touch `core/CLAUDE.md`. [CODE-VERIFIED by S1, S3]
- Guide text must be ASCII except `Ruling:` lines (`tests/core/test_how_we_work_routing_table.py:342-347`); a `/sc:sweep` row in "Other commands" requires `_OTHER_COMMANDS` (`:27-40`) to gain `sc:sweep` and the command file to exist (`:291-311`). [CODE-VERIFIED by S1, S3; line ranges not re-read this session]
- `tests/recommend/test_routing_refresh.py:33` `_POST_REFRESH_ADDITIONS` must gain `"sweep"` or `:647-648` fails. [CODE-VERIFIED by S3]

### CLI package shape (if a Python subcommand is used)

- Registration: two lines appended after `src/superclaude/cli/main.py:561`, with the `# noqa: E402,I001  # intentional: deferred subcommand registration ...` comment, then `main.add_command(<group>, name="sweep")`. [CODE-VERIFIED by S3]
- Package split copied from `cli/reflect/`: `models.py` (types), a pure module documented "No Click, no subprocess" (`reflect/contract.py:7`, `:397`), one module that owns every subprocess call through a `_git(cwd, *args)`-style helper with `timeout=10` and fail-closed callers (`reflect/config.py:64-78`, `:103-109`), and `commands.py` for Click. Lazy `__getattr__` init keeps `superclaude --help` fast (`recommend/__init__.py:12-20`). [CODE-VERIFIED by S3]
- Click output: `click.echo(json.dumps(..., ensure_ascii=False))`; errors to stderr with a `[group sub]` prefix and `sys.exit(1)` (`recommend/commands.py:73-75`). [CODE-VERIFIED by S3]
- Tests: `CliRunner` against the live `main` (`tests/recommend/test_cli_registration.py`); patch the single subprocess seam, not `subprocess.run` (`tests/cli/reflect/conftest.py:58-80`); prove read-only by patching forbidden entry points with `side_effect=AssertionError` inside `isolated_filesystem()` (`tests/cli/reflect/test_contract_status_cli.py:18-22`, `:44-66`); fixtures under `tests/<suite>/fixtures/` via `FIXTURES_DIR` (`conftest.py:17`). [CODE-VERIFIED by S3]
- Lint: `ruff==0.15.20` (`pyproject.toml:54`), CI runs `ruff check` and `ruff format --check` on `src/` `tests/` (`.github/workflows/test.yml:100-106`); no `anthropic` SDK import (`pyproject.toml:203-206`). [CODE-VERIFIED by S3]

### Command and skill files

- Command frontmatter: bare `name`, quoted one-line `description`, `category`, `complexity`, `mcp-servers`, `personas`, `argument-hint` (`src/superclaude/commands/issue.md:1-9`). Section order from `issue.md`: Triggers, Usage, Options, STOP rules, Examples, Outputs, Boundaries, Activation, Related Commands (`:22-95`). [CODE-VERIFIED by S3]
- Activation block: `## Activation` / `**MANDATORY**` / `> Skill sc:<name>-protocol` / installed path `~/.claude/skills/sc-<name>-protocol/SKILL.md` (`reflect.md:146-151`); parsed by `tests/recommend/test_routing_refresh.py:38-40`, `:472`. Never a `src/superclaude/...` path in an installed primitive (root `CLAUDE.md` rule). [CODE-VERIFIED by S3]
- Skills call the CLI as `uv run superclaude <group> ...` (`sc-recommend/SKILL.md:77`; `sc-swarm-wizard-protocol/SKILL.md:35`) and scope Bash in `allowed-tools`, e.g. `Bash(uv run superclaude swarm *)` (`sc-swarm-wizard-protocol/SKILL.md:7`). [CODE-VERIFIED by S3]

### Report conventions to reuse

- From sc-crash-recovery: label each proposed action `SAFE` or `REVIEW` and never execute it (`SKILL.md:91-97`); every failed probe becomes an `unscanned:` marker listed under "What I could not determine" (`SKILL.md:139-150`; `refs/report-template.md:127-129`); a conflicts section that does not pick a side (`report-template.md:120-125`). [CODE-VERIFIED by S2]
- From #409 (`495eb96d`): header names scope and source freshness (`DESIGN-CONTRACT.md:11`; `canvas.py:73-77`); questions stay until explicit closure, "seen is not resolved" (`agent_focus.py:43,51`); independent state dimensions, unknown stays unknown (`data-dictionary.md:17-28,50`); set-union affected counts (`PLAN.md:36`); `shown/total` omission counts (`agent_focus.py:17`); no action buttons (`DESIGN-CONTRACT.md:11`); footer "Inspection only..." and "source coverage is not fleet-wide assurance" (`agent_focus.py:169`; `canvas.py:81`). Field names and IDs are proposed only, never Orca API (`integration-gaps.md:20`). [CODE-VERIFIED by S4 via `git show`]
- Classification rules from the contract: a late heartbeat is absence, never death (`WORKER-CONTRACT.md:45`); "stalled" needs Orca's positive stall proof (`:74`; `orca-capabilities.md:126`); a `consumer_fenced` worker ends with no `worker_done` (`:60`); a worker blocked in `ask` sends no heartbeat (`:57`); "finished" means the return contract is read and admitted, not only settled (`:122-129`); a frozen `/sc:implement` worktree is waiting on a person, never safe to close (`:133-136`); "safe to close" must clear all five refusal conditions (`:108`). [CODE-VERIFIED by S1]
- Orca field cautions: `projection.stage.activity` reads `working` on settled workers, so it is not a work signal (`lc17-show-1.json:132`) [CODE-CONTRADICTED as a work signal, S2]; Orca reports `blocked` and `failed` both as outcome `failed`, so the sweep must read `return-contract.yaml` `worker_status` (`WORKER-CONTRACT.md:58`). [CODE-VERIFIED by S2]

## SOLUTION_RESEARCH

**PROBLEM DOMAIN:** read-only supervisor sweep and static status report over a fleet of agent sessions (Orca workers plus person-started Claude Code sessions) in one worktree tree.

**WEB SEARCH PROVENANCE:** no web search was run for these notes. External patterns are planned for `research/web-01-*.md` and `research/web-02-*.md` (see RECOMMENDED_OUTPUTS). Everything below comes from the four scope files and the files they cite.

### A. Where the sweep logic lives

| Option | Description | Pros | Cons | Evidence |
|---|---|---|---|---|
| A1. Python CLI subcommand (`superclaude sweep`) + thin `/sc:sweep` command and `sc-sweep-protocol` skill | Pure classifier module, one subprocess-owning module (orca, git), Click surface emitting JSON; the skill calls the installed entry point `superclaude sweep ...` on PATH first, with `uv run superclaude sweep ...` as the fallback only inside a dev checkout (when `command -v superclaude` finds nothing), and `allowed-tools` lists both forms (S3 open question 3, gate fix B-19; NB-3), then renders or writes the report | Deterministic and mock-testable, which the seed brief requires (`seed-brief.md:62,68`); follows the `cli/reflect` split (`reflect/contract.py:7`; `reflect/config.py:64-78`); read-only proof pattern ready (`test_contract_status_cli.py:44-66`); scales better than one shell call per session (`seed-brief.md:41`) | Adds a CLI registry entry (`main.py:561`) and a test suite; the bare PATH form from a project that is not a uv project is UNVERIFIED until the implementation plan runs `superclaude sweep --help` there once (S3 open question 3); departs from the sc-issue design, which chose "No CLI" (`docs/designs/sc-issue-command.md:384`) | S3 |
| A2. Skill only, shell commands | Skill runs `orca-ide orchestration worker-list`, `git status` etc. through Bash and classifies in the prompt | Cheapest; no Python package; crash-recovery precedent | Classification is not deterministic and cannot be unit-tested with mocks (breaks `seed-brief.md:68`); every Bash call is a model round trip (batching policy); crash-recovery's own "read-only" claim fails because `Bash(git stash *)` is allowed (`sc-crash-recovery/SKILL.md:4`) | S2, S3 |
| A3. Skill + skill-local standard-library script | Like sc-issue: `SKILL.md` + `scripts/*.py`, tested directly | Testable; no CLI registration; matches newest command precedent (`docs/designs/sc-issue-command.md:355-363`) | Script cannot import package code; runs from `~/.claude/skills/...`, so its tests need a path shim; the shell-out seam must be hand-rolled | S3 |
| A4. Extend `sc-crash-recovery` with an Orca mode | Add flags to the existing sweep | Reuses investigators and report template | 72 h default and `~/workspace/` path conflict with the 6 h window and `~/workspaces/` layout (`SKILL.md:25-27` re-read) [CODE-CONTRADICTED for this host]; `bootstrap_scan.sh` mis-encodes paths (`:31`) and skips worktrees whose `.git` is a file (`:73`); allowed-tools is not read-only; mixes crash recovery with supervision | S2 |

Leaning from the scopes: A1, keeping the report shape and SAFE/REVIEW vocabulary from crash-recovery (A4) without its scripts. The decision is still open (seed brief open question `:77`).

### B. Data sources

| Source | What it gives | Read-only? | Caveats | Evidence |
|---|---|---|---|---|
| `orca-ide orchestration worker-list --include-remote --json [--run <id>]`, paged on `page.nextCursor` | Rows per Dispatch; counts; scope | Yes (help-documented list) | No capture with a non-empty `workers[]`, so the row shape is UNVERIFIED (B-08): the sweep must not rely on any row field beyond the envelope and falls back to one `worker-show` per row; worst-case cost is ceil(N/100) list calls plus N show calls. Max 100 per page; remote rows read `unverifiable` without `--include-remote` | S2 "Orca worker-list fields"; `05-orca-row-schema.md` Answer (5) |
| `orca-ide orchestration worker-show --dispatch <id> --json` | `projection.{outcome, liveness, resource.terminalState, nextAction, attention}`, `observation.agentWait`, `terminal.worktreePath` | Yes | One call per worker (cost at 50-500 sessions) | `lc16-show-4.json:127-185` [CODE-VERIFIED] |
| `orca-ide orchestration worker-read --source transcript` | Latest agent turn; counts as stall proof only when the turn is proved final (Section C rule 2) | Yes | Cursor restarts on `source_changed` | `worker-read --help` line 20 (S2) |
| `orca-ide orchestration run-list` / `run-current` | Run IDs for `--run <id>` (run-list pages at 100 with `--cursor`); the caller's bound Run | Yes on the CLI side (plain `client.call`) | Feeds scope only, no class | `07-gate-gap-fill.md` B [CODE-VERIFIED: run-handlers.js:28-48] |
| `orca-ide orchestration task-list [--ready] [--run <id>]` | Tasks with status, spec, assignee, dispatch id | Yes on the CLI side | Feeds "waiting on a person" kind (b): a ready Task this coordinator did not create; no cursor, row cap UNVERIFIED | `07-gate-gap-fill.md` B [CODE-VERIFIED: task-handlers.js:32-44] |
| `orca-ide orchestration gate-list [--run <id>]` | Gates with status and question | Yes on the CLI side | Candidate pending-decision source; no cursor | `07-gate-gap-fill.md` B [CODE-VERIFIED: gate-handlers.js:26-37] |
| `orca-ide orchestration inbox` | Messages across recipients | NOT PROVEN: CLI side is a plain read, runtime read-marking UNVERIFIED | Not used until settled | `07-gate-gap-fill.md` B [CODE-VERIFIED: message-inbox-handlers.js:20-25] |
| Open questions (`ask`) | Needs-person evidence | UNKNOWN (no read path, G-B) | Questions reach the coordinator through `check --wait --types "worker_done,escalation,question"` (`orca-capabilities.md:63`); whether any read path lists pending questions without consuming them is not established (`495eb96d:integration-gaps.md:11`). `agentWait` is the only non-consuming wait signal found, and no capture shows it non-null | S2, S4; Critical gap G-A below |
| `<report-dir>/return-contract.yaml` (WC-4) | `worker_status` succeeded/partial/failed/blocked, `blocked_question`, `report_path` | Yes (file read) | Only path known to the coordinator before dispatch (`WORKER-CONTRACT.md:31`) | S2 |
| `.dev/tasks/*/progress.md`, sprint `results/`, `.roadmap-state.json`, MDTM frontmatter | Unfinished ledgers, archive-blocked packages | Yes | Signal formats in `sc-crash-recovery/refs/pipelines.md:19-201` | S2 |
| `git -C <worktree>` status / branch / log against upstream | Uncommitted, unpushed, unmerged state for the five refusal conditions (`WORKER-CONTRACT.md:108`) | Yes, if limited to status/log/branch/rev-parse (no `stash` beyond `list`) | Worktree removed mid-sweep must be reported, not crash the run (`seed-brief.md:45`) | S1, S3 |
| `~/.claude/projects/<key>/topics/*.txt` + `~/.local/state/ccsession/orca-tabs/*` | Person-started session names; pane key to Claude transcript uuid | Yes (direct file reads) | `ccsession --list` itself can write (`ccsession:285-287`, `:1787-1788`) so it is excluded; the pane-key join to `dispatch.assigneePaneKey` is verified for one worker: `assigneePaneKey` with `:` replaced by `+` is the orca-tabs file name and its line 3 equals `assigneeHandle` (`07-gate-gap-fill.md` D) [CODE-VERIFIED: lc16-show-4.json:11-12; orca-tabs file lines 1-3]. Whether the sweep reports person-started sessions at all is an open owner decision (WC-14) | S2 |
| Claude transcripts `*.jsonl` (via a tailing variant of `parse_session_log.py`) | Last activity time and last turn for person-started sessions | Yes | Current script reads whole files (can be GB) | S2 |

Excluded on purpose: `orca open` (changes state, `orca-capabilities.md:39`), `check --wait` (consumes messages, assumed; UNVERIFIED), `ccsession --list`, `bootstrap_scan.sh` as-is.

### C. Classification inputs and vocabulary

The issue's classes (idle, stuck, timed out, finished, needs-person) cannot be used literally: WC-10 forbids treating a late heartbeat as death (`WORKER-CONTRACT.md:45`), and `unverifiable` is absence (`orca-capabilities.md:125`, UNVERIFIED guide text). The scopes derive this mapping (DERIVED, S2 "Classifier mapping"; S1 gap G4).

**This is the one canonical class vocabulary and mapping for the research (fix cycle 1, B-01, B-28).** `05-orca-row-schema.md` (classification table), `scope-02-orca-recovery.md` (classifier), `06-orca-open-questions.md` (Q4) and `scope-04-409-layout.md` (skeleton) cite this section; where they differ, this section wins (contradiction C14). The class names are: **waiting on a person, working, stalled (proved), fenced, finished, could not determine, idle**.

**Precedence.** Evaluate per session in this order; the first rule that matches sets the class:

1. **Contract read first.** If `<report-dir>/return-contract.yaml` exists, read it before anything else. `worker_status: blocked` means **waiting on a person**, never finished (WC-5 maps blocked to Orca outcome `failed`, `WORKER-CONTRACT.md:58`, so Orca's outcome alone cannot tell).
2. **Stalled (proved).** Only positive stop proof: `exited` liveness with no `worker_done`, the worker's own observation of process exit, or a transcript turn **proved final** with no `worker_done` (`orca-capabilities.md:126`; `WORKER-CONTRACT.md:74`). "Proved final" needs independent evidence that the turn is the last one: `exited` liveness, a process-exit observation, an observable end-of-turn marker in a `worker-read --source transcript` capture (no such marker has been captured yet, UNVERIFIED), or Orca reporting the proof itself; reading the latest turn without that evidence gives **could not determine**, never stalled (B-05). **Fenced exclusion (second fix pass, NB-1):** rule 2 matches only when there is **no `consumer_fenced` evidence** in the worker's transcript or `check` result. A fenced worker stops without `worker_done` (WC-12, `WORKER-CONTRACT.md:60`), so once its process exits it shows `exited` with no `worker_done`; with fenced evidence present, rule 2 does not match and rule 3 sets the class.
3. **Fenced.** A dispatch that stopped because `check` returned `consumer_fenced` ends without `worker_done` by design (WC-12, `WORKER-CONTRACT.md:60`). It is its own class, never stalled and never finished (B-05). Evidence source: the worker's transcript or its `check` result; with no such evidence a settled-without-`worker_done` row is could not determine.
4. **Waiting on a person.** Split into two kinds (B-11, following #409's rule that a Request is an "Explicit synthetic human question, not inferred from any blocked status", `495eb96d:.dev/design/orca-observer-20261106/data-dictionary.md:12`):
   - (a) *explicit question*: non-null `observation.agentWait` (worker-show only), `worker_status: blocked` with `blocked_question` (rule 1), or a pending `ask` (no read path found, see G-A);
   - (b) *frozen or blocked by policy (derived)*: a Ruling halt or a frozen `/sc:implement` plan (`WORKER-CONTRACT.md:133-136`), or a ready Task this coordinator did not create (`:129`, read from `task-list --ready`, see `07-gate-gap-fill.md` B). These are reported under the policy dimension, not as Requests (`data-dictionary.md:27` "policy: frozen / not frozen").
5. **Working.** liveness `live`, outcome `in_progress`, and `agentWait` **null** (Orca looked and found no wait). `agentWait` null is valid evidence for working but is never stall proof (B-10).
6. **Finished.** Outcome settled **and** a read contract with `worker_status` succeeded, partial or failed. Partial still needs its `report_path` read before a dependent may start (`WORKER-CONTRACT.md:122-129`). The only settled row without a contract that is finished is a brief-guard refusal: no contract and a `worker_done --outcome failed` body starting `guard refused:` (nothing ran, `WORKER-CONTRACT.md:127`), reported as "finished: guard refused". Any other missing contract (a non-guard failure) gives **could not determine**.
7. **Could not determine.** Everything else: `unverifiable` liveness, `agentWait` **absent** on an unsettled row (Orca never looked), stale evidence, Orca unavailable, late heartbeat only, unreadable log, a latest transcript turn not proved final, a list row truncated by the 100-row cap. Reported as absence, never as death (maps the issue's "timed out").

**Idle** applies only to person-started sessions (no Orca Task and no transcript activity inside the window); Orca rows never get it.

**Rules that hold across all classes:** never derive a class from `resource.terminalState` (it is the terminal's lifecycle, not the work's); `agentWait` absence matters only for unsettled rows; `projection.stage.activity` is never an input (`lc17-show-1.json:132`).

| Report class | Inputs | Maps the issue's |
|---|---|---|
| waiting on a person | rule 1 or 4 above, kind (a) explicit question or (b) frozen/blocked by policy | needs-person |
| working | rule 5 | (healthy) |
| stalled (proved) | rule 2 | stuck |
| fenced | rule 3 | (none; by design) |
| finished | rule 6 | finished |
| could not determine | rule 7 | timed out (reported as absence, never as death) |
| idle | person-started session only | idle |

**Safe to close is a separate per-row dimension, not a class** (the #409 rule that dimensions are independent, `495eb96d:README.md:39`) (B-02). It has two independent parts, both printed as REVIEW recommendations only, never executed:

- *terminal releasable*: Orca `resource.terminalState` `reclaimable` and `nextAction` `release`, and only after the session's result has been read (rule 1/6).
- *worktree removable*: all five refusal conditions at `WORKER-CONTRACT.md:108` are false (no unmerged commits, open PR, uncommitted changes, unfinished `/sc:implement` ledger, or unread report) and no freeze applies (`:133-136`).

Window: the issue asks 6 h, crash-recovery uses 72 h (`sc-crash-recovery/SKILL.md:26`). DERIVED point for the design: the window should bound session-log and artifact activity only; an Orca Task that is still open, a pending question or an unread report must be listed whatever its age, or the "kept until answered" criterion (`seed-brief.md:66`) breaks.

### D. Report surface

Static Markdown file following S4's DERIVED skeleton (`scope-04-409-layout.md:268-304`): header with scope and per-source coverage, "Needs a human" first sorted oldest first, retained problems, session and worktree tables, historical sessions, footer disclaimers. #409's own code does not sort (`agent_focus.py:46`) and has no omission count in wide views (`:46-50`, `:164-167`) [CODE-CONTRADICTED against its own contract], so the sweep must implement both explicitly.

**RECOMMENDED APPROACH (provisional, pending web research and owner decisions):** A1 with the data sources in B minus the excluded set, the class vocabulary in C, and the report in D, written to a dated file under `.dev/`.

**PROJECT CONSTRAINT ALIGNMENT:** read-only and coordinator-only (`seed-brief.md:53,57`); no new store (`:54`); extends the contract instead of a new protocol (`:56`); WC-10/WC-6 respected through the class vocabulary (`:58`); #409 layout reused (`:59`); mock-testable (`:62`).

## RECOMMENDED_OUTPUTS

All paths are relative to `${TASK_DIR}` = `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`.

| Output | Status | Producer | Content |
|---|---|---|---|
| `research/scope-01-contract.md` | EXISTS, Complete | done (Phase 2) | Contract, never-as-worker list, registries |
| `research/scope-02-orca-recovery.md` | EXISTS, Complete | done (Phase 2) | Orca fields, crash-recovery signals, ccsession, classifier mapping |
| `research/scope-03-cli-patterns.md` | EXISTS, Complete | done (Phase 2) | CLI package shape, tests, registration |
| `research/scope-04-409-layout.md` | EXISTS, Complete | done (Phase 2) | #409 Attention Ledger, Shift Brief, report skeleton |
| `research/05-orca-row-schema.md` | MISSING, planned | gap-fill codebase agent (Critical gap G-A) | Whether a `worker-list` row carries the worker-show `projection`; values of liveness (`live`/`unverifiable`/`exited`) and a non-null `agentWait` shape; paging; cost per call. Sources: `orca-ide worker-list --help`, `worker-show --help`, `orca-capabilities.md:110-130`, the installed Orca guide text (read only, no state change) |
| `research/06-orca-open-questions.md` | MISSING, planned | gap-fill codebase agent (Critical gap G-B) | A read-only, non-consuming way to list pending `ask` questions for the needs-person class, or a stated fallback (`agentWait`, `blocked_question`, Ruling halt, frozen plan). Sources: `orca-capabilities.md:56-68,148-151`, `WORKER-CONTRACT.md` WC-3 and `:133-136`, `495eb96d:integration-gaps.md:11` |
| `research/web-01-agent-supervisor-session-health.md` | MISSING, planned | web research agent | Supervisor and health-classification patterns: Erlang/OTP supervisors, Kubernetes liveness vs readiness probes, heartbeat / phi-accrual failure detectors, "unknown" as a first-class state |
| `research/web-02-static-status-report-conventions.md` | MISSING, planned | web research agent | Static status and handover report conventions: SRE status pages, shift-handover reports, alert triage ordering (oldest first), omission counts |
| `synthesis/synth-01-problem-current-state.md` | MISSING | synthesis agent | Report sections 1-2 |
| `synthesis/synth-02-target-gaps.md` | MISSING | synthesis agent | Sections 3-4 |
| `synthesis/synth-03-external-findings.md` | MISSING | synthesis agent | Section 5 |
| `synthesis/synth-04-options-recommendation.md` | MISSING | synthesis agent | Sections 6-7 |
| `synthesis/synth-05-implementation-plan.md` | MISSING | synthesis agent | Section 8 |
| `synthesis/synth-06-questions-evidence.md` | MISSING | synthesis agent | Sections 9-10 |
| `RESEARCH-REPORT-orchestrator-mode.md` | MISSING | assembler | Final report |

Synth file names and section ranges follow `src/superclaude/skills/tech-research/SKILL.md:1497-1502`.

## SUGGESTED_PHASES

**Phase 2 (codebase research): verify only, no re-investigation.** One item per existing scope file. Each item checks that the file has `**Status:** Complete`, a findings body with file:line citations, and a gaps / open-questions section, and copies its gaps into the gaps log.

| Item | File | Expected headings (observed) |
|---|---|---|
| 2.1 | `research/scope-01-contract.md` | Status Complete; "Open questions" present; no "Summary" heading (accept, or add a one-paragraph summary in the gaps log, not in the file) |
| 2.2 | `research/scope-02-orca-recovery.md` | Status Complete; "Summary" and gaps present |
| 2.3 | `research/scope-03-cli-patterns.md` | Status Complete; "Open questions" present; no "Summary" heading (same handling as 2.1) |
| 2.4 | `research/scope-04-409-layout.md` | Status Complete; "Summary" and gaps present |

**Phase 2b (gap fill): at most 2 codebase agents, in parallel.**

| Item | Output | Gap | Severity |
|---|---|---|---|
| 2b.1 | `research/05-orca-row-schema.md` | G-A: worker-list row schema and liveness / agentWait values never captured | Critical |
| 2b.2 | `research/06-orca-open-questions.md` | G-B: no established non-consuming read of pending questions | Critical |

Important but not Critical (record in the gaps log; synthesis handles them as open questions, no agent): pane-key to transcript join (`orca-tabs` vs `dispatch.assigneePaneKey`); fix `bootstrap_scan.sh` (`:31`, `:73`) vs a new scanner; `uv run superclaude` outside a uv project (pipx installs); lazy vs eager init of the Orca client in the CLI.

**Phase 3 (web research): 2 agents, in parallel.** `research/web-01-agent-supervisor-session-health.md` and `research/web-02-static-status-report-conventions.md` (topics above). Each must state how a pattern maps to WC-10 (absence is never death) and to the read-only constraint.

**Phase 4 (synthesis): 6 agents, inputs per file.**

| Synth file | Inputs |
|---|---|
| synth-01-problem-current-state.md | scope-01..04, 05, 06, gaps log |
| synth-02-target-gaps.md | scope-01..04, 05, 06, gaps log, web-01, web-02 |
| synth-03-external-findings.md | web-01, web-02 |
| synth-04-options-recommendation.md | scope-01..04, 05, 06, web-01, web-02, gaps log, and SOLUTION_RESEARCH A-D in these notes |
| synth-05-implementation-plan.md | scope-01 (contract rule placement, never-as-worker), scope-03 (CLI shape, registries, tests), scope-04 (report skeleton), web-01/web-02 (patterns) |
| synth-06-questions-evidence.md | gaps log, every research file, AMBIGUITIES_FOR_USER below |

synth-05 must keep the phase split: Phase 1 = read-only `/sc:sweep` + static report + coordinator-loop rule; `/sc:close`, resume, trust layer, orchestrator of orchestrators and the management-server relay are recorded as later phases only.

**Phase 5 onward:** QA gates, assembly into `RESEARCH-REPORT-orchestrator-mode.md`, and final QA as the tech-research skill defines them.

## TEMPLATE_NOTES

- Template: **02 (complex task)**, at `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` and the installed copy `~/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1519 lines). The project dev copy `.claude/templates/workflow/` is MISSING in this worktree, so the builder must read the installed or `src/` copy.
- Why 02: Deep tier, multi-phase (verify, gap fill, web, synthesis, QA, assembly), parallel agents per phase, and per-file synthesis inputs.
- Phase 2 items must be verify-only (the four scope files are finished; do not rerun them).
- Every checklist item that writes a file names its exact output path from RECOMMENDED_OUTPUTS.

## AMBIGUITIES_FOR_USER

Owner decisions (the plan should decide these, not implementation; analysis recommendation 4):

1. **Where the logic lives:** CLI subcommand + thin skill (A1), skill-only (A2), skill-local script (A3) or extend crash-recovery (A4). The issue design leaned "no CLI" for sc-issue (`docs/designs/sc-issue-command.md:384`); the testability requirement (`seed-brief.md:62,68`) favours A1.
2. **Default window:** 6 h (issue) vs 72 h (`sc-crash-recovery/SKILL.md:26`) (analysis F11). Also whether the window applies only to activity evidence, so open Tasks, pending questions and unread reports are listed whatever their age (DERIVED, see SOLUTION_RESEARCH C).
3. **Report location:** under `.dev/tasks/` (always staged by rule) or another `.dev/` folder; dated file name format.
4. **Rule ID:** new coordinator-loop rule as WC-14 (next free) or reuse the unused WC-1.
5. **Sequencing with open PR #422**, which edits `WORKER-CONTRACT.md` (analysis F8): land the contract rule after #422, or keep the first PR to new files only.
6. **Pragmatic output style:** whether to add an orchestrator exception to the mandatory DONE / NEXT table (`pragmatic.md:22,53`, "No exceptions") (analysis F10).
7. **Routing placement:** `/sc:sweep` as a row in the HOW-WE-WORK "Other commands" table (`:314-337`) or in the excluded set; also the `_POST_REFRESH_ADDITIONS` entry (`test_routing_refresh.py:33`) and the never-as-worker list (analysis F6, F7).
8. **Person-started sessions:** include them (observed through transcripts and ccsession files only, analysis F2) or limit Phase 1 to Orca workers.
9. **#409 pinning:** copy the layout into this repo or cite commit 495eb96d (unmerged); which sort tie-break to use; what approval label the reused design carries.
10. **"Management server"** (analysis F14): no counterpart in the repo; Orca or the #409 observer is not known.
11. **Worktree-first placement** in the issue vs trigger-based placement in CR-01 / WC-11 (analysis F12).

Contradictions and unverified claims found (each must reach the gaps log):

| # | Claim | Tag | Evidence |
|---|---|---|---|
| C1 | scope-01's F1-F12 numbering of the analysis findings | CODE-CONTRADICTED | The analysis file now has F1-F14 and S1-S5 (`.dev/issues/339/analysis/analyze-worker-contract.md:30-55`, 72 lines); scope-01 read an older 55-line version. Use the current numbers. |
| C2 | `tests/core/test_how_we_work_routing_table.py` is about 360 lines | CODE-CONTRADICTED | `wc -l` gives 1202 |
| C3 | sc-crash-recovery is read-only | CODE-CONTRADICTED | allowed-tools includes `Bash(git stash *)` (`sc-crash-recovery/SKILL.md:4`) |
| C4 | crash-recovery `--all` scans `~/workspace/` | CODE-CONTRADICTED on this host | Worktrees live under `~/workspaces/` (`SKILL.md:25-27`) |
| C5 | `stage.activity` signals work in progress | CODE-CONTRADICTED | Scope-02 shows it is not a work signal; use `projection.*` |
| C6 | #409 Attention Ledger is age-ranked | CODE-CONTRADICTED (partial) | No sort in `agent_focus.py:46` at 495eb96d |
| C7 | #409 wide views carry omission counts | CODE-CONTRADICTED | Absent at `agent_focus.py:46-50,164-167` |
| C8 | Orca guide-sourced statements in `orca-capabilities.md` (liveness meanings `:125-126`, `check --wait` consumption) | UNVERIFIED | Guide text, not repo code; see gap-fill 05 and 06 |
| C9 | The recommend docstring's `python -m` usage claim | CODE-CONTRADICTED | Recorded in scope-03; low impact, decide whether it matters |
| C10 | `worker-list` row carries the worker-show projection | UNVERIFIED | No capture with non-empty `workers[]` (Critical gap G-A). Until a capture exists the sweep uses only the list envelope and calls `worker-show` per row; worst case ceil(N/100) + N calls (`05-orca-row-schema.md` Answer (5)) |
| C11 | A non-consuming read of pending questions exists | UNVERIFIED | `495eb96d:integration-gaps.md:11` (Critical gap G-B) |
| C12 | Pane key in `orca-tabs` joins to `dispatch.assigneePaneKey` | CODE-VERIFIED for one worker | `lc16-show-4.json:11-12` against `~/.local/state/ccsession/orca-tabs/ec61f494-...+2844c731-...` lines 1-3 (`07-gate-gap-fill.md` D). Reporting person-started sessions stays an owner decision (WC-14) |
| C13 | Orca verb form | CODE-VERIFIED | On CLI 1.4.245 every orchestration verb is `orca-ide orchestration <verb>` (`worker-list`, `worker-show`, `worker-read`, `run-list`, `task-list`, `gate-list`, `inbox`, `check`); a top-level `orca-ide worker-list` prints "Unknown command". Earlier short forms in these notes and in scope-02 were corrected in fix cycle 1 |
| C14 | Classifier mappings disagree | RESOLVED by Section C | `05-orca-row-schema.md` classification table (old :169-176, including its "idle = settled and terminal retained/released" row) and `scope-02-orca-recovery.md` classifier (old :97-103, including "safe to close" as a class) disagreed with each other and with Section C (blocked contract both finished and waiting; idle meaning two things; finished from outcome alone). Section C's precedence mapping supersedes both; the two files now cite it |
| C15 | Nested workers | CONTRADICTION, open | Current guide `[G]` 130-131 says a dispatched worker starts helpers with `worker-start --spec`; `orca-capabilities.md:97-102` says depth 1 forbids it; WC-8 and WC-13 forbid it for this project's workers at any depth. The contract governs: the sweep reports a non-null `parent` (worker-show `projection.parent`, `lc16-show-4.json:115`) as a WC-13 violation for review |

**Critical gaps: 2** (G-A worker-list row schema; G-B non-consuming open-question read).
