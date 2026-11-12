# Reviewer 2 brief (persona: qa, model class: haiku)

## T1 card excerpt

```yaml
grounding:
  verification_run:
    ruff_check_touched_files: {exit: 0, result: "All checks passed!"}
    pytest_scoped: {exit: 0, result: "1788 passed in 6.39s", scope: "tests/sweep, tests/commands/test_sweep_command.py, tests/skills/test_worker_contract.py, tests/core/test_how_we_work_routing_table.py, tests/recommend/test_routing_refresh.py"}
    real_entrypoint: {cmd: "uv run superclaude sweep --help and sweep run --help", exit: 0, result: "subcommand `run` listed with options --run --window --root --output"}
    recheck_of_logged_env_failures: "tests/cli/eval/test_claude_process_adapter.py two ruff tests fail with '.venv/bin/python: No module named ruff' (not in the diff); tests/hooks/test_launch_level_guard.py speed tests pass on isolated re-run (6 passed)"
  runtime_surface: "click group `sweep_group` (src/superclaude/cli/sweep/commands.py:214-216), command `run` (commands.py:219-245), deferred import (src/superclaude/cli/main.py:567) and registration `main.add_command(sweep_group, name=\"sweep\")` (src/superclaude/cli/main.py:569), console script superclaude -> cli.main:main: all hit the decorator/registry/packaging degrade oracle -> runtime_surface_degraded=true, unreached=0"
  reuse_sweep: "12 candidates, 0 confident duplicates; 3 maybe-related advisory (_git mirrors reflect/config.py:64, _publish idiom has copies at sprint/recovery.py:433 and install_ccsession.py:83, parse_time mirrors swarm/tui.py:125); neighbour search degraded (auggie unavailable)"
  tasklist_state: "355 checklist items; 353 ticked; unticked are 14.48 (this audit) and 14.49 (set status Done)"
  coverage: "all 50 diff files map to tasklist items (36 by literal path, 14 captured fixtures by the glob in item 7.16, tasklist line 1280): effective unmapped hunks 0, S_dev_density 0.0"
  S_scope: 50
  S_domains: 4          # code, tests, docs, config

  - id: DC-6
    claim: "Stale status text: DESIGN header still says owner approval of WC-16 'is still required' and 'Review status: NOT a clean pass' (docs/designs/orchestrator-mode.md:5, :7); the task file's Open Questions OQ-2 to OQ-8 still read OWNER DECISION PENDING / PERSON INPUT PENDING (task file lines 3037-3043) although decision records exist under phase-outputs/plans/ (OQ-2..OQ-8 files)."
    proposed_class: drift          # documentation/record drift, non-gating
    confidence: 0.75

  - id: DC-8
    claim: "Final QA gate ended 'PASS by owner ruling, open: FIN-F7' (qa/final/gate-decision.md): the exempt /sc:sweep chat reply does not relay an Orca outage on an exit 0 run; ruled a documented limitation 2026-11-12. The owner's recorded 'words' are the executor's own recommended reply pasted back (phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md). FIN-F5 was fixed in cycle 2."
    proposed_class: authorized_expansion
    confidence: 0.75

  - id: DC-10
    claim: "Task objective 6 says the full `uv run pytest` passes; the recorded full run had 3 failures (25252 passed): two ruff tests fail because `ruff` is not importable in .venv (re-confirmed by the auditor) and one timing test failed under machine load (passes alone, re-confirmed). None reads a file the diff changed. `uv run ruff format --check src/ tests/` also lists 12 Markdown files unchanged at base."
    proposed_class: necessary_deviation   # pre-existing / environmental
    confidence: 0.80

  - id: DC-11
    claim: ".dev/tasks staging: at audit time the work-unit holds 54 untracked and 2 staged-then-modified files (project rule: .dev/tasks/ is always staged); item 14.49 stages it."
    proposed_class: authorized_expansion   # pending its own tasklist item
    confidence: 0.70
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T19:25:01Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3034-3043

```markdown
### Open Questions

- **OQ-1 (R5, `--agent-wait`), RESOLVED by the owner on 2026-11-08.** "Allow it, no conditions needed." The sweep may run `worktree ps --agent-wait`, with and without `--json`; option (b) does not apply. The INV-005 allowlist pin and the version-scoped claim (Orca 1.4.245) are kept. Evidence: coordinator live probe, 24 calls on one idle worktree, 0 `index.lock` sightings at 5 ms polling, 0 failed calls. Record: `phase-outputs/plans/OQ-1-agent-wait-decision.md` (written at build time); applied by items 6.1 to 6.4.
- **OQ-2 (GQ-10, report location), OWNER DECISION PENDING.** Recommendation `<root>/.dev/sweeps/`, gitignored; does NOT authorize adoption. Items 7.1 and 7.2.
- **OQ-3 (GQ-11, rule id), OWNER DECISION PENDING.** (a) new rule WC-16 or (b) amend WC-1. Recommendation (a); does NOT authorize adoption. Items 7.3 and 7.4.
- **OQ-4 (GQ-35, #409 pin `495eb96d`), OWNER DECISION PENDING.** Recommendation: pin and cite it; does NOT authorize adoption. Items 7.5 and 7.6.
- **OQ-5 (GQ-61, default window 6 h or 72 h), OWNER DECISION PENDING.** Recommendation 6 h, activity only; does NOT authorize adoption. Items 7.7 and 7.8.
- **OQ-6 (GQ-63, DONE / NEXT exception), OWNER DECISION PENDING, no recommendation.** No source recommends an option. Items 7.9 and 7.10.
- **OQ-7 (D9 sign-off), OWNER DECISION PENDING; blocks the classify step.** Record: `phase-outputs/plans/OQ-7-D9-signoff-decision.md`.
- **OQ-8 (the Run id for step 1.0a), PERSON INPUT PENDING.** Blocks step 1.0a and the step 1.4 live check (item 9.3). Record: `phase-outputs/plans/OQ-8-run-id-decision.md`.
```

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:3055-3061

```markdown
### Follow-Up Items Identified

- [High] WC-9 lock retry for the coordinator, out of scope for this task, tracked in IronbellyOrg/IronClaude#446 - Identified in the Execution Context Key Constraints (build time)
- [Closed] OQ-1 was resolved as allow by the owner on 2026-11-08, so no follow-up PR to master's contract text at `src/superclaude/core/WORKER-CONTRACT.md:110` is needed - Identified in Step 6.3
- [Medium] Open the Phase 1 PR after the user asks, only via `/sc:pr-submit --monitor 3` (every gh command carries `--repo IronbellyOrg/IronClaude`); this task never commits, pushes or merges - Identified in Step 14.46
- [Medium] DESIGN section 17 open item 19 stays open after this task: the rationale for the proposed byte limits (1 MiB, 256 KiB, 8 MiB; SP-28) must be recorded in the task package before release. Until then the limits apply as proposed and are marked proposed in `src/superclaude/cli/sweep/probes.py` (items 8.5 and 8.10). This follow-up does not close the open item, so DESIGN keeps `Total: 23 open items.` - Identified in Steps 8.5 and 8.10 (reflect run 2, R-05)
- [Medium] FIN-F7: the exempt `/sc:sweep` chat reply (counts and report path alone) does not relay an Orca outage on an exit 0 run; fixing it needs the sweep exception in `pragmatic.md` (7 sites), the revision addendum (lines 29 and 37), DESIGN 7.6 step 3 (now `:663`, take `orca_available`) and the skill steps 3 and 4 with their pins; ruled a documented limitation by the owner - Identified in Step 14.32
```

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/final/gate-decision.md:1-12

```markdown
# Final gate decision (item 14.32)

Final gate: PASS by owner ruling, open: FIN-F7

## How this outcome was reached

- Cycle 2 (`cycle2-decision.md`): F_2 = {FIN-F7}, |F_2| = 1, below |F_1| = 2; no check of the cycle-1 PASS set regressed; all 238 checks pass in both cycle-2 verifier reports; FIN-F5 is resolved.
- `|F_2|` is not 0, so the hard cap of two fix cycles applied. The plan's rule gave a HALT with the open finding FIN-F7 (recorded in the plan's Execution Log as the item 14.32 HALT row, and in `cycle-ledger.md` row 2). The HALT rule was applied (plan status Blocked, `blocker_reason` set, item not ticked) and the open MAJOR finding was escalated to the owner.
- The owner ruled FIN-F7 a documented limitation on 2026-11-12 (`phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md`). The HALT is resolved by that ruling (HALT RESOLVED row in the Execution Log); the plan status is back to Doing.

## The open finding

```

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md:1-16

```markdown
# Final gate, item 14.32 halt: owner ruling on FIN-F7 (2026-11-12)

Status: RULED by the owner. Chosen: documented limitation (the recommended action).

## Context

The final QA gate reached its two-fix-cycle cap with one open MAJOR finding: FIN-F7. The chat reply of the exempt `/sc:sweep` run prints the summary counts and the report path alone, so an exit 0 run during an Orca outage reads like a normal run in that reply. The report at the printed path states the outage, the skill requires the session to Read that report to its last line first, and the lower-bound note still prints with the counts. Fixing it needs edits of `src/superclaude/output-styles/pragmatic.md` (the sweep exception, 7 sites), the revision addendum, DESIGN 7.6 and the tests.

## Owner's words

The owner pasted back the recommended action as their answer ("I record the ruling in the gate decision and write Final gate: PASS by owner ruling, open: FIN-F7. I set the plan back to Doing and tick 14.32. FIN-F7 goes into the follow-up issue, with the fix list above as its starting point. The run continues to the fidelity gate (14.33 to 14.45)").

## Ruling

- FIN-F7 is a documented limitation of Phase 1. It is not fixed in this run.
- Gate decision: `Final gate: PASS by owner ruling, open: FIN-F7`.
```

### docs/designs/orchestrator-mode.md:1-13

```markdown
# Orchestrator mode, Phase 1: `/sc:sweep` architecture design

## 1. Status, scope and inputs

Status: design for review, issue #339 Phase 1, written 2026-11-08 by `/sc:design --type architecture --format spec`. It holds no implementation code. Owner approval of the WC-16 text (section 8) is still required.

Review status: NOT a clean pass. Three blocking findings were still open after the review cap (2 fix cycles, 3 reviews: `orchestrator-mode-review-1.md` to `-3.md`). With coordinator approval (the reply to `msg_ee6f54c3b8a4`, delivery `delivery_17bd071084c5`, 2026-11-08), they are carried as the first required design-fix tasks of the `/task-builder` task file. Each one is closed by its own review gate before any code task starts:

- R3-B1: the session-to-Dispatch time-window rule reads three time fields (Dispatch start, Dispatch end, and the earliest transcript timestamp) that the data model (`OrcaObservation`, `TranscriptTail`) lacks.
- R3-B2: two Dispatch rows on one pane give conflicting results (False and None, or a join to both rows), and no rule decides between them.
- R3-B3: three SPEC FR-010 fixtures (outage, full page, `call_failed`) were dropped from `test_classify.py`.

Phase 1 adds one read-only command, `superclaude sweep run`, a thin `/sc:sweep` command and `sc-sweep-protocol` skill that call it, the WC-16 "Coordinator loop" contract text, and the routing and doc rows that name it. A successful run leaves one filesystem change: one dated report under `<root>/.dev/sweeps/`, plus that directory when it is new. A dot-prefixed temp file exists only during publication (section 3).
```

### docs/designs/orchestrator-mode.md:746-770

```markdown
## 11. Test plan mapped to files

Seven new files under `tests/sweep/` (the REPORT names, steps 1.8 to 1.13), one new command test, and edits to three existing test files (`tests/commands/test_routing_plugin_parity.py` must also still pass, unchanged). Every test runs with the seams patched; none starts Orca, ccsession or Claude (NFR-013).

Shared setup in `tests/sweep/conftest.py` (step 1.8):

- `patch_orca` and `patch_git` replace `probes._orca` and `probes._git` with fakes that record every argv and return fixture data, as `tests/cli/reflect/conftest.py` does for its seams.
- An autouse fixture patches `subprocess.run`, `subprocess.Popen` and `os.system` to raise `AssertionError`. It steps aside only for a test carrying the existing `integration` marker, which is used by exactly one test, the real-git test below. `pyproject.toml` runs pytest with `--strict-markers`, and `integration` is already registered there, so no new marker and no `pyproject.toml` edit is needed.
- A fixed `now` and a `tmp_path` layout with `HOME` and `XDG_STATE_HOME` moved inside it, holding packages, contracts, transcripts and a ccsession `orca-tabs/` folder.
- Fixtures copied from captured Orca output keep their source name; hand-made ones carry `synthetic` in the file name until step 1.0a replaces them.

| File | Covers | Main cases |
|---|---|---|
| `tests/sweep/test_readonly.py` (created at step 1.4a, extended at 1.11) | NFR-002, FR-025, GQ-103(1), GQ-110, NFR-001, NFR-013 | Step 1.4a part: every recorded `_git` argv has `--no-optional-locks` at index 1 and `-C <path>` after it; the child env holds `GIT_OPTIONAL_LOCKS=0`; one git argv per discovered worktree; the one `integration`-marked real-git test in a `tmp_path` repository with the four SPEC assertions (control, `check-ignore` of `.dev/sweeps/x.md` succeeds, of `.dev/tasks/to-do/x.md` fails, a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged). Step 1.11 part: the snapshot diff (path, size, `st_mtime_ns`, SHA-256) over the root, `HOME` and the XDG dirs: exactly one added report file plus the output directory when new; no temp file and no second name for the report remain after exit 0 |
| `tests/sweep/test_probes_allowlist.py` | NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ-109, M7, SPEC section 11 failure modes, FR-010 | Full-sweep recording: each argv equals one template token for token, argv[0] is `$ORCA_CLI_COMMAND` when set, else `orca-ide`; zero argv for all four templates marked "not called in Phase 1" (`worktree list`, `worktree current` and both `worktree ps --agent-wait` forms, with and without `--json`); exact-set pin of the ten templates; negatives that raise `ValueError` before a subprocess (`check`, `inbox`, `worker-read`, `gate-list`, an extra flag, `--include-remote`, `run-list`); a positive case that both `worktree ps --agent-wait` templates (with and without `--json`) are accepted; the FR-021 forbidden list held in the test; git negatives (`rev-parse`, `log`, `branch`, `--version`, any `stash` form). Result classes: each unavailable cause on call one, the quoted-marker negative fixture, a middle `worker-show` exit 1, a malformed zero-exit body, the empty `run-current` body, and the captured no-binding fixture (gated on 1.0a). The `collect` source rows and `truncated` that the FR-010 list-incomplete rule reads (`test_collect_worker_list_source_rows_and_truncated`, over a fake `_orca`): R1 `worker-list` ok and R2 `worker-list` `call_failed` (not call one) give the `sources` rows whose name starts with `orca worker-list` exactly `orca worker-list R1` and `orca worker-list R2` (the prefix is the literal word `orca`, not `$ORCA_CLI_COMMAND`), R2 `unscanned` non-null and R1 `unscanned` None; a failed `task-list --run R2` sets `unscanned` on `orca task-list R2` and not on `orca worker-list R2`; with the budget spent before R2's `worker-list`, no argv is recorded for it and the row `orca worker-list R2` has `unscanned: time budget rea [line cut for the brief; re-Read the file]
| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-015, NFR-010, NFR-004, GQ-101, GQ-102, GQ-105, GQ-108, SP-07, SP-16, SP-24, SP-26, SP-29, D9, WC-13, M6, M9, SPEC section 11 unreadable inputs | One parametrized case per rule 1 to 9 (the `working` case expects rule `fallback` while Rule 5 is inert, open item 6), reaching every name in `CLASSES` except `working` until Rule 5 is restored; rule-name order pin `[r.name for r in RULES]`; window cases (5 h old row, windows under and at 6 h; record timestamp older than mtime); the four FR-008 inputs; a late-heartbeat live row is never `stalled (proved)` (SPEC line 444); the two FR-009 cases with the exact note; rule 1 decline notes (M6); the rule 5 case (it never matches while the names are uncaptured; the four-condition case returns when Rule 5 is restored); a future timestamp gives unknown age and never idle; FR-010 complete-negative join, the control (an 8 h old unmapped transcript T goes to Historical when the list is complete; its Given is the shared Given below), the three SPEC incomplete cases (an older transcript during an Orca outage, an older unjoined transcript after a full page with uncaptured continuation, an incomplete list after `call_failed`; each stays visible with `person_started` None and its `origin unknown:` note, never idle or Historical), and three more fixtures that are not SPEC fixtures (a Run that is not confirmed; a Run never reached because of the budget, which counts as `call_failed`; and the SPEC's tab-map reason, which the SPEC names but gives no fixture), pinned by seven `test_fr010_*` fixtures plus the control: the three SPEC fixtures, `test_fr010_unknown_run_empty_list_unknown`, `test_fr010_run_not_reached_budget_unknown` and `test_fr010_tab_map_unreadable_older_transcript_unkn [line cut for the brief; re-Read the file]
| `tests/sweep/test_report.py` | FR-011, FR-016, NFR-005, NFR-008, NFR-015, SP-23, SP-24, FR-020 header line, FR-006 (rule 6 wording), SP-16, WC-13, SPEC section 11 remote coverage | Heading order equals section 7.5; (a) sort with 3 ages plus one unknown, tie-break by ID; (b) never prints question text; injection fixture (`a\|b`, ANSI, bidi override, `<script>`, a Markdown link) keeps the column count and leaves no active tag or link; a 300-character cell prints 200 characters ending `...` while the JSON value is whole; render twice gives equal bytes and equal JSON apart from `report_path`; source-loss fixture gives could not determine with the `unscanned:` reason, never finished, failed, not frozen or a recommendation; version line for `1.4.245-aidev02.780594c521aa`, `1.4.246` and a missing file; the `bound_reached` line text; the SP-24 footnote; the empty-section string; the `next inspection` map has an entry for every rule name and no stop, retry, release, merge or removal word; rule 6 wording: a finished row's report text and JSON contain neither `admitted` nor `accepted` (SPEC line 259); the remote-coverage fixture: `## Source coverage` has the `remote hosts` row with coverage `unknown` and the Scope line carries `(lower bound: remote hosts not scanned)`, never a no-sessions line (454); the WC-13 row appears under `## Retained problems` (380); the SP-16 literal `could not join Orca workers to transcripts (tab map empty or stale)` appears under `## Could not determine` (236); a True row with the `origin not proved` note prints the note in its row and in the JSON `notes` (D9); the lower-bound line: a result with `truncated` True (the 100-row case) prints `[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]` in the header and its JSON `summary.tot [line cut for the brief; re-Read the file]
| `tests/sweep/test_cli_registration.py` | FR-001, NFR-006 | `superclaude sweep --help` and `sweep run --help` exit 0 under `CliRunner`; importing `superclaude.cli.sweep` records no seam call and does not import `commands` until `sweep_group` is read |
| `tests/sweep/test_cli_contract.py` | FR-002, FR-003, FR-004, FR-005, FR-017, FR-018, FR-019, NFR-009, G-1 (section 3) | Run id cases (`""`, `'r;x'`, duplicate, unknown-Run then R2); the three binding tests and the fourth gated on 1.0a; disk-only continuation prints `unscanned: orca unavailable`; the FR-003 parser cases; the FR-004 output and root cases; the FR-005 fixture (4 rows, 2 worktrees, `(4/4)`) and the reconciliation equalities; golden v1 key set and types at every level; zero counts present; `waiting` lists hold ids only; two runs with one injected `now` give `stem.md` and `stem-2.md`; one test per exit code. Publication cases from section 3: a link failure, a full disk on write, `stem.md` to `stem-99.md` all taken, an existing temp name, and an output path that escapes after `makedirs` each exit 1 with no file at a report name and no success JSON; a print failure after the commit point exits 1 and leaves one complete report; `os.unlink` patched to raise after a successful `os.link` gives exit 1, no success JSON, exactly one complete report ending in `Report complete`, and a stderr line `[sweep publish] could not remove temp file <path>` naming the temp path; an existing earlier report is byte-identical afterwards |
| `tests/commands/test_sweep_command.py` (new, step 1.16) | FR-022, NFR-011, NFR-007 (static half) | The section 7.6 assertions |
| `tests/skills/test_worker_contract.py` (edit, step 1.19, same commit as step 1.18) | FR-023 | The section 8 pins |
| `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py` (edits); `tests/commands/test_routing_plugin_parity.py` (unchanged, must pass) | FR-024 | R1 to R5 of section 9 |

NFR-012 is checked by the gates of steps 1.25 to 1.27, not by a test file. Run line for the sweep tests: `uv run pytest tests/sweep -v`.

```

- Verification results (FR-4 hunk): artifact ref `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/post/audit/verify-logs/invocations.yaml` (four invocations: ruff exit 0; scoped pytest 1788 passed exit 0; `sweep --help` and `sweep run --help` exit 0; recheck of the two env failures exit 1 = `No module named ruff`).
- Runtime-surface ledger hunk (FR-RSR.9): artifact ref `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/post/audit/artifacts/runtime-surface-ledger.yaml` (three DEGRADE rows, no UNREACHED).
- Reuse audit ref: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/post/audit/artifacts/reuse-audit.yaml` (0 confident duplicates).

## Coverage slice

| Diff file | Hunks | Tasklist items naming the path | Status |
|---|---|---|---|
| tests/core/test_how_we_work_routing_table.py | 1 | ['13.3', '13.8', '13.9', '13.10', '13.11', '13.12', '13.13', '13.14'] | mapped (literal path) |
| tests/recommend/test_routing_refresh.py | 1 | ['10.24', '11.2', '11.5', '11.6', '11.7', '11.8', '11.9', '11.10'] | mapped (literal path) |
| tests/skills/test_worker_contract.py | 5 | ['1.4', '5.1', '5.5', '5.21', '11.21', '12.2', '12.3', '12.5'] | mapped (literal path) |
| tests/commands/test_sweep_command.py | 1 | ['11.4', '11.5', '11.6', '11.7', '11.8', '11.9', '11.10', '11.11'] | mapped (literal path) |
| tests/sweep/__init__.py | 0 | ['8.7', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19', '8.20'] | mapped (literal path) |
| tests/sweep/conftest.py | 1 | ['8.8', '8.11', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19'] | mapped (literal path) |
| tests/sweep/fixtures/SOURCES.md | 1 | ['7.18', '10.1', '14.49'] | mapped (literal path) |
| tests/sweep/fixtures/captured-run-current.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-tab-map-1.json | 1 | ['14.49'] | mapped (literal path) |
| tests/sweep/fixtures/captured-tab-map-2.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-tab-map-3.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-tab-map-4.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-tab-map-5.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-task-list-ready.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-task-list-unknown-run.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-task-list.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-worker-list-unknown-run.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-worker-list.json | 1 | ['14.49'] | mapped (literal path) |
| tests/sweep/fixtures/captured-worker-show-1.json | 1 | ['14.49'] | mapped (literal path) |
| tests/sweep/fixtures/captured-worker-show-2.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-worker-show-3.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-worker-show-4.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-worker-show-5.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/fixtures/captured-worktree-current.json | 1 | ['14.49'] | mapped (literal path) |
| tests/sweep/fixtures/captured-worktree-list.json | 1 | ['14.49'] | mapped (literal path) |
| tests/sweep/fixtures/captured-worktree-ps.json | 1 | [] | mapped by glob (item 7.16, captured-*.json) |
| tests/sweep/test_classify.py | 1 | ['2.5', '3.2', '4.3', '10.2', '14.49'] | mapped (literal path) |
| tests/sweep/test_cli_contract.py | 1 | ['10.7', '14.49'] | mapped (literal path) |
| tests/sweep/test_cli_registration.py | 1 | ['10.6'] | mapped (literal path) |
| tests/sweep/test_probes_allowlist.py | 1 | ['2.5', '10.3', '14.49'] | mapped (literal path) |
| tests/sweep/test_readonly.py | 1 | ['8.9', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19', '8.20'] | mapped (literal path) |
| tests/sweep/test_report.py | 1 | ['10.5', '14.49'] | mapped (literal path) |

Rows are file-level. Tasklist: 355 items, 353 ticked; unticked 14.48 (this audit) and 14.49 (status Done).
