# Plan grounding

## Run state
index_state: fresh
checked_at: 2026-11-23T18:06:13Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s
projectPath: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s
access: mcp
degraded: []
One readiness call returned zero pending added/modified/removed files. Switch unset, no index build running (pgrep exit1=no-match). Plan-only Markdown writes do not alter indexed production code.

## Resolved symbols
- src/superclaude/cli/swarm/lenses/refactor_find.py: LENS, template line53. Outline from graph, source Read.
- src/superclaude/cli/swarm/commands.py: run_cmd (definition1558), actual recommendation builder2129-2157 Read; _build_spec_from_lens template929-930 and _resolve_input_mode call1178 Read.
- tests/swarm/test_commands_run.py: _runnable_spec, _write_spec, test_run_cmd_stub_transport_dispatches_workers_not_noop; graph outline and relevant source Read.
- tests/swarm/test_e2e_user_guide.py: target/runner fixtures and _run, baseline stub test and existing bare-review expectations Read during diagnosis; no new test helpers required.
- tests/swarm/test_bundled_lenses.py: test_lens_declares_full_dm010_field_set and test_validate_all_returns_no_failures_on_bundled_registry; graph outline and source seen in diagnosis, refresh before executor edit.
- docs/swarm/README.md:67, lens-catalog.md:25,49, user-guide.md:200 are active matching documentation. release-notes-v1.md:34 is historical caller text, not a current refactor-find instruction; leave historical records unchanged.
- Active adversarial input contract Read earlier in this session: 2-10 existing readable comma-separated files, no --apply. No actual adversarial execution authorized.

### Phase structure (standard depth: four phases)
| Phase | Goal | Inputs | Outputs | Checkpoint | deps |
|---|---|---|---|---|---|
| 1 | Make current defect reproducible in automated checks | source request, live lens, existing stub test patterns | availability/full-command regression tests and red output | tests fail on current exact defect without paid review | none |
| 2 | Replace unavailable follow-up | phase1 availability test, active command contract | refactor lens template update | availability check passes, experimental/suspect unchanged | 1 |
| 3 | Supply accepted refactor report inputs | phase1 full-command test, current run_cmd builder | bounded refactor-only argument mapping and edge-case tests | full default suggestion valid, overrides/siblings unchanged, red-to-green CLI evidence | 2 |
| 4 | Align active documentation | changed behavior and three existing user docs | matching follow-up documentation and checks | no active stale refactor instruction, historical evidence untouched | 3 |

## Dependents
- Graph run_cmd depth1 impact returned 70 symbols across CLI registration and input/status/resume/TUI/transport tests. It is broad because run_cmd owns the whole command; change only its existing post-normalization fresh-run handoff block, not those other subsystems.
- Verified registration at src/superclaude/cli/swarm/__init__.py:150: swarm_group.add_command(run_cmd,name='run') (call-site-verified).
- Graph _build_spec_from_lens returned seven rows including tests and two production leads; _resolve_input_mode call at commands.py:1178 confirmed (call-site-verified); scaffold path :3736 was seen in exact search only (dependent, not cited as independently verified call in plan).
- LENS enters lenses/__init__.py:60-62,110; preflight default copy at preflight.py:540-543 and materialized snapshot behavior are preserved, not reworked. Registry/preflight tests cover this existing contract.
- Bare-review and edge-case-hunt use the shared compare_files default. Reflect-review lens also shares fresh run; reflect ensemble has separate substitution builder. These siblings must remain unchanged; no blanket placeholder removal or reducer validation is planned.
- Executor's related checks: tests/swarm/test_commands_run.py, test_bundled_lenses.py, test_e2e_user_guide.py, test_lens_defaults.py, test_bare_review_parity.py, test_swarm_run_inputs.py. Production CLI stub replay, not only helper formatting, supplies repaired-state evidence.
- Resume already calls reduce_wave3 without next-command args (commands.py:2578-2586), a separate pre-existing path; do not expand issue501 to resume. Preserve resume tests, not assert repair of it.
- Active current-doc source search found three files/four stale refactor occurrences. Historical release and validation findings are evidence, not replacement targets.

## Pre-check
FULL_GATE=PASS (UV read-only validation): four phases, four contiguous tasks, fourteen distinct named existing repo files; required schema/frontmatter/dependencies, package-relative source/evidence, no checkbox/numbered subtask lines, no verification-only task and source coverage checked.
- Task1 names real existing lens/test/CLI/interface files; new test names are not invented as existing symbols. Public swarm_group registration is verified. Controlled count fixtures may mock dispatch only, never acceptance-path generation.
- Task2 changes the real LENS constant; registry/preflight/shortcut dependents named and preserved. No new public interface.
- Task3 isolates the high-blast-radius run_cmd edit to its verified existing recommendation block; explicitly protects custom precedence, sibling/default mapping, reducer/status and resume. Relevant existing test modules named; user-defined changed behavior stays refactor-only.
- Task4 names the three current user-facing files found by source search; historical release/testing records excluded intentionally.
Advisory dependents not individually named in task text: TUI/transport/status/resume and input error tests from run_cmd's broad graph impact. Those subsystems are outside the changed block and remain covered by existing suite as available; no claim of running their tests during planning. No missing source path or unresolved changed symbol was found.
Pre-check counts: tasks=4, missing-files=0, unresolved-changed-symbols=0. Codegraph is supporting source-location evidence only; actual ranges were Read. No product implementation, new regression execution, model-backed swarm or repaired-output sign-off occurred in this run.
