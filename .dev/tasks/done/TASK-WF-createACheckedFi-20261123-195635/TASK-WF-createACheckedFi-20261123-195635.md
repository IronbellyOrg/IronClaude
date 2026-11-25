---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-createACheckedFi-20261123-195635
version: "1"
priority: Medium
created_date: "2026-11-23"
---

# Publish swarm completion markers after terminal results

Source: ./source.md
Goal: Foreground and resumed swarm jobs that complete reduction publish the existing atomic completion marker when effective policy enables it, with the actual persisted result status and contract path.

## Constraints

- Only issue 540 is covered. The diagnostic package `.dev/troubleshoot/bug-issue540-completion-marker-20261123191058/` is immutable context; read `REPORT.md`, `evidence-validation.md`, `tier1-observation.md` and `contract-ledger.md` there when executing tasks. Its historical absolute paths refer to the old checkout and must not be used as live edit destinations.
- The user authorized this planning step after the recorded pre-fix planning ambiguity was explained. That does not clear the report's blocked repair closure or authorize implementation. Execute this plan only after a separate implementation request; do not repeat diagnosis merely to obtain a plan. Keep the original report unchanged.
- Preserve the recorded negative CLI witness from `artifacts/negative-witness.txt` in that diagnostic package. Successful repair requires new positive public-CLI evidence paired with it; neither the earlier diagnostic review PASS nor this plan certifies a repair. All new evidence belongs under this package's `./artifacts/`, using fresh isolated job output roots and an isolated HOME. Never overwrite the old foreground/resume evidence.
- Production edits are limited to the two completion continuations in `src/superclaude/cli/swarm/commands.py`. Reuse `reduce.emit_done_sentinel`, `ResultContract.status`, existing filename constants and atomic writers. Do not create a new marker schema, duplicate contract emission, change CLI exit/stdout contracts, or implement `print_contract_to_stdout`.
- Respect the effective foreground or rehydrated resume policy. Arbitrary original runtime override recovery on resume is incomplete and is not part of this fix: do not change `Manifest`, `preflight.resume_mode`, caller/lens metadata recovery, or persistence formats to address it. A disabled effective resume policy can be tested through a controlled rehydration seam, but must not be advertised as original-policy persistence.
- Detached parents only launch; children own completion. Preserve `_emit_killed_done_sentinel`, `kill_cmd`, the killed marker's empty contract path, existing writer atomicity and existing resume worker-skip/merge semantics. No new cleanup, stale-marker lifecycle protocol, or adjacent behavior change is included.
- Issues 501, 555 and 568, their task packages and shared diagnostic counters are outside scope. Do not import, edit or stage their files. Stage only this newly created task package as required by project policy; never stage generated `.claude/` mirrors. No commit, push, GitHub write or automatic implementation handoff is authorized.
- All future Python and test execution uses UV. Use stub transports, no live model calls or credentials; read any required credentials from the environment without logging values. A skipped or unavailable live detached check is not a pass and cannot establish complete detached repair coverage.

## Phase 1: Foreground completion

## Task 1: Wire foreground marker publication with reproducing CLI tests

Read the diagnostic report's Proposed Fix and repair acceptance, `run_cmd`'s post-dispatch continuation in `src/superclaude/cli/swarm/commands.py`, `reduce_wave3` and `emit_done_sentinel` in `src/superclaude/cli/swarm/reduce.py`, and `OnCompletion` in `src/superclaude/cli/swarm/models.py`. In `tests/swarm/test_e2e_user_guide.py`, replace the existing `test_quickstart_does_not_emit_done_sentinel` limitation assertion with a positive default-on regression, including a name/docstring that states the new behavior. Extend `tests/swarm/test_commands_run.py` using its `_runnable_spec` and `_write_spec` helpers for spec-file/stdin policy and boundary cases. Run the newly positive tests before the source change and save their expected missing-marker failures to `./artifacts/foreground-before.txt`.

In `run_cmd`, retain the contract returned by the existing reduction, persist terminal state through `_write_swarm_state`, then publish with the existing `emit_done_sentinel` only when reduction actually produced the persisted contract and `inline_job.runtime.on_completion.write_done_sentinel` enables it. Use the returned status and an absolute resolved path to that output directory's existing `return-contract.yaml`; do not move publication into the reducer or the generic state writer. Keep no-reduction branches explicit so there is no unbound contract or marker pointing at a missing result. Add no abstraction unless the existing code requires one.

Acceptance criteria:
- The new foreground marker-presence test fails on the unmodified continuation for the reported omission, then passes after this change. Save both command lines, exit codes and complete focused pytest output under `./artifacts/foreground-before.txt` and `./artifacts/foreground-after.txt`; an expected pre-fix failure is evidence, not a passing repaired test.
- Through the registered `swarm_group` CLI, a stub `--lens bare-review --target ... --output ...` run produces a parseable `done.json` with exactly `atomic_write`, `terminal_status` and `contract_path`; `atomic_write` is true, status equals the actual YAML contract status, and the absolute contract path resolves to the persisted contract in the same output root. Default-on spec-file and stdin runs behave equivalently, including a relative output-path case.
- Explicit foreground `write_done_sentinel=false` leaves no marker in a fresh output root while still producing the contract and terminal state. Controlled success/partial/failed worker outcomes exercise the real CLI continuation and reducer; each enabled terminal marker mirrors the persisted result rather than the CLI's exit-0 convention. Do not replace the reducer or writer with mocks for this status check.
- Ordering tests wrap and delegate to the real writers: at terminal-state publication the contract already exists and the new marker does not; at marker publication the contract is readable and the persisted state is terminal. A reducer/contract-write exception or terminal-state-write exception must not produce a new completion marker. Early preflight/transport errors, no-output execution and a no-normalization/no-reduction path must not acquire a fabricated marker.
- Capture one actual UV-launched `superclaude swarm run` with stub transport, isolated HOME and a fresh output directory under `./artifacts/foreground-cli/`; save argv, checkout/import provenance, stdout, stderr, exit code and parsed state/contract/marker comparisons under `./artifacts/foreground-cli-check.txt`. Pair this positive witness with the immutable diagnostic negative witness. Do not substitute a direct helper call or pytest success alone for the public-entrypoint capture.
- Run `uv run pytest tests/swarm/test_commands_run.py tests/swarm/test_e2e_user_guide.py tests/swarm/test_swarm_run_inputs.py tests/swarm/test_run_tui_integration.py tests/swarm/test_done_sentinel.py tests/swarm/test_imm6_atomic_write.py`; record results in `./artifacts/foreground-after.txt`. Registration in `src/superclaude/cli/swarm/__init__.py`, existing stdout signatures, TUI continuation, writer atomicity and kill's separate publication path stay compatible. Repair only failures caused by this scoped change; report unrelated failures without changing their code.

## Phase 2: Resumed completion

## Task 2: Wire resumed marker publication with skipped and redispatched tests

Depends on: Task 1

Read the diagnostic report's resume evidence and scope limits, `_run_resume_branch` and `discover_succeeded_slots` in `src/superclaude/cli/swarm/commands.py`, `resume_mode` in `src/superclaude/cli/swarm/preflight.py`, and the existing skipped-worker and redispatch scenarios in `tests/swarm/test_resume_crash_recovery.py`. Extend that test module with completion-marker assertions before editing the resume continuation. Use an independent manifest/sidecar fixture with no pre-existing marker so Task 1's new foreground marker cannot make a missing resume publication appear to pass. Record the resume regression's pre-change failure in `./artifacts/resume-before.txt`.

In `_run_resume_branch`, retain the returned `reduce_wave3(..., resume=True)` contract, retain the current terminal-state write, then call `emit_done_sentinel` with the actual result status and resolved persisted contract path when `rehydrated_spec.runtime.on_completion.write_done_sentinel` is enabled. Follow the foreground ordering without changing worker classification, redispatch mapping, manifest rehydration, merge regeneration or error exits.

Acceptance criteria:
- The new all-workers-skipped resume regression fails for a missing marker before this continuation changes and passes afterward; save commands, exit codes and outputs in `./artifacts/resume-before.txt` and `./artifacts/resume-after.txt`. Foreground publication must not satisfy the resume assertion accidentally.
- Both all-workers-already-succeeded and remaining-workers-redispatched CLI paths write the existing three-field marker after the contract and terminal state. The marker's status and absolute contract path match the persisted result. Succeeded sidecars/bodies are preserved, dispatch runs only for remaining indices, no duplicate slot outputs appear, and `merged.md` still regenerates.
- Parameterized real-reducer CLI tests cover success, partial and failed terminal results, including redispatched degraded outcomes. Explicitly supplying a disabled effective policy through a controlled `resume_mode` return object suppresses publication while preserving terminal state/contract; the normal manifest-based path uses its present default-on policy. No test or documentation claims arbitrary original opt-out recovery across resume.
- Delegating writer wrappers prove contract persistence precedes terminal-state persistence and marker emission follows it. Contract/reducer failure and terminal-state-write failure leave no new marker in clean fixtures; missing/malformed/mismatched manifests likewise do not manufacture completion.
- Capture a separate actual UV-launched `superclaude swarm run --resume ... --transport stub --output ...` with isolated HOME and output artifacts under `./artifacts/resume-cli/`. Seed the fixture independently or remove only this task's known prior marker before resume, recording that setup, so the positive witness demonstrates new resume publication. Save argv, provenance, stdout/stderr, exit code, skip/redispatch counts and parsed marker/state/contract comparisons in `./artifacts/resume-cli-check.txt`, paired with the diagnostic resume negative evidence.
- Run `uv run pytest tests/swarm/test_resume_crash_recovery.py tests/swarm/test_resume_regenerates_merge.py tests/swarm/test_resume_uses_manifest_lens.py tests/swarm/test_crash_recovery_e2e.py tests/swarm/test_force_relens.py`; retain results in `./artifacts/resume-after.txt`. `run_cmd`'s resume dispatch and the manifest lens snapshot/force-relens behavior remain compatible without changes outside this omission fix.

## Phase 3: Detached child ownership

## Task 3: Add detached launcher and child completion regression coverage

Depends on: Task 2

Read `_launch_detached_run` in `src/superclaude/cli/swarm/commands.py`, its snapshot/child argv contract, and the tmux gating and cleanup fixtures in `tests/swarm/test_tmux_detached.py`. Add regression tests to that module, using deterministic stub jobs with unique job IDs, absolute target/output paths and isolated HOME. Reuse the existing missing-tmux checks in `tests/swarm/test_tmux_fallback.py` rather than adding a new launcher implementation.

Add an always-runnable test that intercepts `swarm_tmux.launch_detached` to capture the actual staged child request without running a child yet. Assert the launcher has not published a marker. Then execute the captured snapshot through the real registered child CLI continuation with stub transport and assert publication, with enabled/disabled completion policy variants. This is deterministic launcher/child-boundary coverage, not proof of a live tmux session. Add a separate live tmux stub-child integration test using the module's existing availability rules; use a bounded wait that surfaces child failure/timeout and cleans up only the test-owned session.

Acceptance criteria:
- Before simulated or live child completion, the parent-created snapshot preserves the requested completion policy and no marker is produced by the parent. After successful child completion, enabled policy produces the existing marker with matching actual contract status/path and terminal state; disabled policy does not. The test exercises the child execution path, not a direct marker-writer call.
- The live test launches the actual detached CLI using UV, captures output and waits for the child-owned marker with a fixed deadline. It validates the contract and terminal state once the marker appears. Save command, environment capability (without secret values), stdout/stderr, observed artifacts and result under `./artifacts/detached-cli/` and `./artifacts/detached-check.txt`. If tmux is missing or nesting is unsupported, record the explicit skip and retain detached runtime acceptance as NOT PROVEN; deterministic simulation is not a substitute and full repair closure must not be claimed.
- Run `uv run pytest tests/swarm/test_tmux_detached.py tests/swarm/test_tmux_fallback.py tests/swarm/test_kill_cmd.py tests/swarm/test_done_sentinel.py tests/swarm/test_three_layer_artifacts.py tests/swarm/test_imm6_atomic_write.py tests/cli/reflect/test_ensemble_unit.py tests/cli/reflect/test_ensemble_stub_integration.py` and save results including skips in `./artifacts/completion-compatibility.txt`.
- `_launch_detached_run` remains launcher-only; `_emit_killed_done_sentinel` and `kill_cmd` keep their existing killed marker, empty contract path and idempotence. The existing `run_tier2_ensemble` caller in `src/superclaude/cli/reflect/ensemble.py` and direct helper tests still use the unchanged writer API/schema; do not add swarm-state prerequisites to that helper or broaden this task into reflect changes.

## Phase 4: Completion guidance

## Task 4: Update the run artifact reference and user guidance

Depends on: Task 3

Update only the completion-related passages in `docs/swarm/README.md` (opening summary, What a run emits table/count and resume note), `docs/swarm/command-reference.md` (Run artifacts table and fresh/resume publication text), and `docs/swarm/user-guide.md` (Pattern C completion caveat and No done.json troubleshooting row). Derive the replacement claims from Tasks 1-3 evidence and the real `run_cmd` / `_run_resume_branch` behavior, not from historical release prose. The existing quickstart absence test in `tests/swarm/test_e2e_user_guide.py` is replaced by Task 1; use its actual new name if linking to it.

Acceptance criteria:
- These three documents describe enabled default marker publication after persisted contract and terminal state for completed foreground and resumed reduction, and child-owned publication for detached execution. They explain explicit opt-out and preserve the separate killed result; no unconditional only-kill or inline-never statements remain in the affected sections.
- The artifact table includes the existing three marker fields and explains that terminal_status is the actual success/partial/failed result, not a guarantee that all workers succeeded. Update the documented default stub output count from observed Task 1 artifacts, not a guessed number.
- Scope qualifiers are truthful: early errors/no completed reduction do not imply a new completion marker; effective resume policy is used, with original runtime override recovery not guaranteed. No claim of full detached runtime verification is made when Task 3 recorded a skip.
- Run `uv run pytest tests/swarm/test_e2e_user_guide.py` against the updated docs/test contract and record the result and a targeted completion-claim search across these three files in `./artifacts/reference-doc-check.txt`. Existing related links resolve, and no unrelated setup, transport, metadata or stdout documentation is rewritten.

## Task 5: Align monitoring and operator guidance with the repaired behavior

Depends on: Task 4

Update only completion-related guidance in `docs/swarm/monitoring-patterns.md` (implementation warning and Pattern 1 scope), `docs/swarm/observability-procedure.md` (marker introduction/table, Layer 4, triage, absence explanations and affected verdict-reading recipes/use-case map), and `docs/swarm/operator-runbook.md` (resume artifact comparison). Align these passages with the reference docs from Task 4 and the actual marker behavior from Tasks 1-3. Preserve unrelated diagnostic recipes, command examples and kill semantics; correct inline-absence comments and the old negative-test citation only where this fix invalidates them.

Acceptance criteria:
- Polling guidance supports completed foreground/resume/detached-child jobs with effective marker policy enabled and fresh per-job output directories; it does not promise marker appearance for opt-out or failures before reduction/terminal persistence. State/contract inspection remains available when publication is disabled. Do not introduce a new polling feature or broadly redesign the runbook.
- Observability guidance no longer describes default inline marker absence as expected or restricts marker verdict reading to detached/resumed jobs. It retains the distinction between terminal completion and success, and between a result contract path and the killed marker's empty path.
- The operator-runbook no longer says resume uniquely adds artifacts now also emitted on a fresh completed reduction. The existing limitation on arbitrary original resume runtime overrides is stated consistently with Tasks 2 and 4, without changing persistence behavior.
- A targeted search across all six updated completion documents finds no remaining only-kill/default-inline-never claim or citation to `test_quickstart_does_not_emit_done_sentinel`; inspect hits in context, do not blindly replace matches. Retain search results and link checks in `./artifacts/monitoring-doc-check.txt`.
- Run `uv run pytest tests/swarm/test_e2e_user_guide.py tests/swarm/test_tmux_fallback.py` and save results in `./artifacts/monitoring-doc-check.txt`. The documentation's marker field names, status values, policy conditions and ordering agree with the parsed CLI evidence already captured; no new diagnosis is needed.
