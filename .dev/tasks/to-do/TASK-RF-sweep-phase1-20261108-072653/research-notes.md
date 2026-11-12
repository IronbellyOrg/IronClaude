# Research Notes: issue #339 Phase 1, read-only `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-14

**Date:** 2026-11-08
**Status:** Complete
**Scenario:** A (explicit: the design names every file, step and test)
**Depth Tier:** Deep (more than 20 files across CLI package, tests, command, skill, core contract, docs, registries)
**Track Count:** 1 (every part depends on the design fixes and on the shared models; not independent)
**SPEC_PATH:** docs/designs/orchestrator-mode.md (design, 1013 lines). Requirements: .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md (653 lines).
**CLI_MODE:** false (reflect_post_mode: skill)

---

## EXISTING_FILES

Design inputs (read in chunks of at most 150 lines):
- `docs/designs/orchestrator-mode.md`: section 2 GQ resolutions; 3 report publication (G-1); 4 components; 5 sequence; 6 data flow; 7 interfaces (7.1 modules, 7.2 models and observation rules, 7.3 allowlists, 7.4 JSON, 7.5 report, 7.6 command and skill); 8 WC-14; 9 routing rows R1 to R8 (line 688); 10 .gitignore; 11 test plan; 12 traceability; 13 deviations D1 to D9; 15 step map (line 864; table at line 900, steps 1.0a to 1.29); 16 rollback; 17 open items; 18 revision log.
- `docs/designs/orchestrator-mode-review-3.md`: the three open blocking findings R3-B1, R3-B2, R3-B3 (owner-approved to carry as first tasks).
- `.dev/issues/339/analysis/inv-005-orca-index-lock.md`: allowlist safety evidence.

Existing code to modify (design section 9 and 15): `src/superclaude/cli/main.py` (deferred registration, after line 561 per design), `src/superclaude/core/WORKER-CONTRACT.md` (WC-14, line 23 never-as-worker list), `tests/skills/test_worker_contract.py`, `src/superclaude/core/HOW-WE-WORK.md` and `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`, `docs/user-guide/commands.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, `CHANGELOG.md`, `.gitignore`.

New files (design 7.1, 11, 15): `src/superclaude/cli/sweep/{__init__,models,classify,probes,report,commands}.py`; `src/superclaude/commands/sweep.md`; `src/superclaude/skills/sc-sweep-protocol/SKILL.md`; `tests/sweep/{conftest,test_classify,test_probes_allowlist,test_readonly,test_report,test_cli_registration,test_cli_contract}.py`; `tests/commands/test_sweep_command.py`.

Templates: `~/.claude/templates/workflow/02_mdtm_template_complex_task.md` (project `.claude/templates/workflow/` does not exist in this worktree; `src/superclaude/templates/workflow/` holds the source copy).

## PATTERNS_AND_CONVENTIONS

- Click groups under `src/superclaude/cli/<name>/` with deferred import in `cli/main.py` (to verify: researcher 2).
- Thin command plus protocol skill pair; command names the skill in `## Activation`.
- Installed primitives reference `~/.claude/...` only (CLAUDE.md rule; check with `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`).
- `make sync-dev`, `make verify-sync`, `make lint`; UV only; never stage `.claude/` except settings.json; `.dev/tasks/` always staged.

## GAPS_AND_QUESTIONS

- R3-B1: which Orca `worker-show` / `worker-list` fields carry Dispatch start and end times (UNVERIFIED until the step 1.0a capture; design open item 23).
- R3-B2: the tie-break rule when two Dispatch rows share one pane.
- R3-B3: where SPEC FR-010's three fixtures (outage, full page, call_failed) belong in `test_classify.py`.
- Whether each line anchor the design cites (main.py:561, HOW-WE-WORK.md lines 318-337 and 396-403, test files' line numbers, WORKER-CONTRACT.md:23) still holds on this branch.
- Step 1.0a live capture and 1.0b owner decisions are human-gated items: how the task file encodes them without a live Orca call in tests.
- Test infrastructure: `integration` marker, subprocess mocking pattern, AST test for `report.py`, snapshot-diff helper.

## RECOMMENDED_OUTPUTS

- research/01-file-inventory.md
- research/02-patterns-conventions.md
- research/03-integration-points.md
- research/04-design-fixes-r3.md
- research/05-test-verification.md
- research/06-template-examples.md

## SUGGESTED_PHASES

- Researcher 1, File Inventory: design sections 7, 9, 10, 15 versus the repo. For every NEW file: purpose, the interfaces it must hold (signatures from 7), its step and dependency. For every EXISTING file to modify: verify the cited line anchors. Covers the CLI package and tests only as an inventory, not conventions.
- Researcher 2, Patterns and Conventions: read `src/superclaude/cli/main.py` registration, one existing CLI package (`src/superclaude/cli/reflect/` or `recommend/`) and its tests, one thin command plus protocol skill pair (frontmatter, `allowed-tools`, `## Activation`). Not WC or routing files.
- Researcher 3, Integration Points: WORKER-CONTRACT.md (WC list, line 23, free rule ID), test_worker_contract.py pins, the eight routing rows R1 to R8 and their tests, the HOW-WE-WORK byte-copy and core CLAUDE.md level-table tests, `.gitignore`. Not the CLI package.
- Researcher 4, Design fixes R3: read review-3 blocking findings, design 7.2, 11 and 12, SPEC FR-010; the Orca read-verb outputs available without a live call (`orca orchestration worker-show --help`, `worker-list --help`, the inv-005 report, Orca bundle field names); the ccsession tab map source. Produce, for each of R3-B1, R3-B2, R3-B3, the exact design edit and test fixture text. Not other design sections.
- Researcher 5, Test and Verification: pytest config, markers, conftest patterns, subprocess and filesystem mocking, Makefile targets, how existing tests pin command and skill text, CI. Not the contract tests (researcher 3).
- Researcher 6, Template and Examples: template 02 PART 1 rules (A3, B2, L-patterns, M3, M4, I19 to I22), one recent TASK-RF example in `.dev/tasks/`, how human-gated items (owner decisions, live capture) and design-doc edit items are encoded; the POST reflect item form for skill mode.

## TEMPLATE_NOTES

Template 02 (discovery of design fixes, build, test, review phases, QA gates). QA_INTENSITY full. PER_PHASE QA gates. Testing UNIT plus one real-git integration test (design section 11). Phase order: setup, design fixes R3-B1 to R3-B3 (each its own QA gate), pre-implementation gates 1.0a, 1.0b, 1.16a, then steps 1.1 to 1.28 grouped by design section 15, then final validation, POST reflect, done.

## AMBIGUITIES_FOR_USER

None that block building. Owner decisions are carried as step 1.0b items (GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, D9 sign-off). Coordinator order: stop after the task file; do not run /task or write code.
