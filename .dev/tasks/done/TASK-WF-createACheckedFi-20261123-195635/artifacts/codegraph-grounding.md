# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-23T19:56:56Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
- access: mcp
- CLI version: 1.6.2 (matches installed guide pin)
- Change counts: 0 added, 0 modified, 0 removed.
- Degraded tokens: none.
- No diagnostic experiments are rerun. Source inspection below grounds future tasks only.

## Resolved symbols

Source bodies were read directly after graph leads; these are planning checks, not a repeated runtime diagnosis.

- `src/superclaude/cli/swarm/commands.py`: `run_cmd` at 1558-1682 and 2070-2178, `_run_resume_branch` at 2314-2599, `_write_swarm_state` at 763-796, `_launch_detached_run` at 1218-1336. Foreground reduction is conditional on an output root and normalization recipe. Do not fabricate a contract or completion marker on a path that did not reduce.
- `src/superclaude/cli/swarm/reduce.py`: existing `emit_done_sentinel` at 383-440 validates the three-field marker and uses the existing atomic writer. `reduce_wave3` at 671-704 emits and returns the result contract. No marker/schema/reducer redesign is planned.
- `src/superclaude/cli/swarm/models.py`: `OnCompletion` policy at 548-573 and `RuntimeSpec` at 576-619; marker default is enabled.
- `src/superclaude/cli/swarm/preflight.py`: `resume_mode` at 1888-1976 restores a subset from the manifest; runtime defaults are used. The plan must honor the effective rehydrated object, not claim recovery of arbitrary original overrides.
- Existing tests read: `tests/swarm/test_commands_run.py` fixtures `_runnable_spec` and `_write_spec`; `tests/swarm/test_e2e_user_guide.py` quickstart and the current absence assertion; `tests/swarm/test_resume_crash_recovery.py` manifest/sidecar helpers and skipped/redispatch tests; `tests/swarm/test_tmux_detached.py` live tmux gating/cleanup; `tests/swarm/test_tmux_fallback.py` unavailable-tmux and inline cases.
- Affected current documentation read: README overview and artifact list; command-reference run artifacts; user-guide detached caveat and troubleshooting row; monitoring-patterns warning and polling example; observability-procedure marker layers, triage and result recipes; operator-runbook resume artifacts. Documentation edits must be limited to these completion claims and associated counts/citations.

### Phase structure (standard depth, systematic strategy)

| Phase | Goal | Inputs | Outputs | Checkpoint | Dependencies |
|---|---|---|---|---|---|
| 1 | Publish foreground completion safely | Report proposal/acceptance; run_cmd, writer and policy; existing fresh-run tests | Foreground integration, failing-then-passing CLI tests, foreground evidence logs | Marker reflects persisted result and policy, after terminal state; early/no-reduction cases have no new marker | None |
| 2 | Publish resumed completion safely | Report resume evidence; _run_resume_branch, resume_mode and resume tests | Resume integration/tests, resume evidence logs | Skipped and redispatched completion use actual status and effective policy; successful prior outputs preserved | Phase 1 |
| 3 | Pin detached child ownership | _launch_detached_run; tmux tests and writer/kill compatibility tests | Deterministic launcher/child tests and a gated live stub-child test | Parent never publishes terminal marker; child does so only after completion; skipped live proof stays explicitly unproven | Phases 1 and 2 |
| 4 | Correct directly affected operator guidance | Results/limits of prior phases and six named docs | Updated completion reference and monitoring instructions | Guidance matches tested marker behavior, opt-out and resume limits; no old absence-test citation | Phases 1, 2 and 3 |

## Dependents

Graph counts are returned rows, not a claim of exhaustive runtime coupling. `_run_resume_branch` callers: 1/1. `emit_done_sentinel` callers: 15/15, including 3 import/file rows; only the concrete call sites below are asserted. `run_cmd` depth-1 impact reports 70 affected symbols, used as test/registration leads. Resume callee query returns 18/18 rows; calls relevant to the plan were confirmed in the directly read continuation. Caller confirmation is below the 5-per-symbol and 20-per-run limits.

| Relationship | Verified source | Resolution | Plan coverage |
|---|---|---|---|
| run_cmd invokes _run_resume_branch | commands.py:1664-1669 within run_cmd | call-site-verified | Task 2 |
| CLI registers run_cmd | swarm/__init__.py:136-150 | call-site-verified (registration, not execution) | Task 1 CLI integration |
| run_tier2_ensemble invokes emit_done_sentinel | reflect/ensemble.py:404-421 | call-site-verified | Task 3 compatibility, no reflect edits |
| helper test invokes emit_done_sentinel | tests/swarm/test_done_sentinel.py:47-55 | call-site-verified | Tasks 1 and 3 existing writer suite |
| foreground invokes reduce_wave3 then _write_swarm_state | commands.py:2145-2169 | call-site-verified | Task 1 |
| resume invokes reduce_wave3 then _write_swarm_state | commands.py:2578-2591 | call-site-verified | Task 2 |
| detached launcher passes snapshot to child CLI | commands.py:1297-1309 | call-site-verified (launch request) | Task 3 |
| quickstart test requires marker absence today | tests/swarm/test_e2e_user_guide.py:117-138 | directly read behavioral assertion | Task 1 replaces the assertion; Tasks 4 and 5 update citations |
| resume tests classify skipped and redispatched slots | tests/swarm/test_resume_crash_recovery.py:294-424 | directly read behavioral assertions | Task 2 |
| kill test checks killed marker and empty contract path | tests/swarm/test_kill_cmd.py:159-191 | directly read behavioral assertions | Task 3 preserves behavior |

Other impact leads not requiring product edits: status command tests, force-relens tests, TUI integration/opt-in tests, transport/input-mode tests, crash-recovery tests. Task 1 includes input-mode and TUI integration regression runs; Task 2 includes force-relens and crash recovery; Task 3 includes writer/atomicity, kill and reflect compatibility. `tests/swarm/test_status_cmd.py` and `tests/swarm/test_inv012_tui_opt_in.py` are additional graph leads not individually named in acceptance test commands; they are not evidence of another production completion continuation and are not silently claimed verified. The existing writer remains unchanged, so its other helper-test callers do not need coordinated source changes.

Six directly read documentation consumers are split across Tasks 4 and 5. No invocation, benchmark or test was rerun during planning.

## Pre-check

- Full standard-depth plan gate: PASS. Five contiguous tasks in four nonempty phases; backward-only dependencies; required workflow-plan/1.2 metadata; package-relative source/evidence paths; no unchecked placeholders, checkbox/numbered task syntax or generated primitive output paths.
- Mechanical existing-path and AST symbol check: 29 referenced source/test/doc files exist; 13 named source symbols resolve. Both source-edit continuations, the unchanged writer, launch boundary and compatibility dependents are accounted for. The unassigned impact leads are listed under Dependents rather than claimed absent.
- Source coverage mapping: foreground publication/policy/status/order/negative-positive evidence -> Task 1; skipped/redispatched resume/effective policy/no metadata expansion -> Task 2; detached child ownership, kill and atomic-writer compatibility, explicit live-skip handling -> Task 3; directly affected artifact guidance -> Task 4; monitoring/operator guidance -> Task 5. All phases' outputs/checkpoints map to task criteria.
- Initial mechanical gate attempt falsely rejected the valid quoted created_date because the temporary checker compared raw YAML scalar spelling. Corrected the checker to strip scalar quotes; the unchanged plan then passed. No plan defect was masked or altered after the generation gate.
- UV created a local ignored `.venv` while running the standard-library checker despite `--no-sync`; no dependencies were installed by that check and no product source/test/doc files were edited. The directory was not removed or staged.
- Initial edit of the grounding stub was refused by the freshness hook until a Read was performed; retried through Edit after reading, without bypass.
- This is a static planning pre-check, not execution or product repair proof. No test suite, swarm run, runtime diagnosis or GitHub operation was performed.
- Wave 4 independent advisory reflection was invoked with the source snapshot and plan. The delegated reviewer stopped before completing the protocol: its developer-level instructions prohibit writing Markdown reports, conflicting with the required on-disk review handoff. It reported no outputs; Glob of the agreed `./artifacts/reflect-pre-20261123200321/` subtree returned no files. This is an incomplete review, not a PASS or a zero-finding result.
- No permission workaround, substitute in-band review or replacement reviewer was used after that refusal. Reflect status is failed and reflect_report_path is null. Wave 4R could not route findings because there is no review contract or verified finding-count set; none were invented. No plan remediation, regeneration or archive action ran. Workflow Wave 5 records the valid generated plan separately from its failed advisory review. Independent plan quality review remains outstanding before claiming the planning unit complete.
