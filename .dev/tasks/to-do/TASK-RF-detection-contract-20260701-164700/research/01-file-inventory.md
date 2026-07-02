# File Inventory for Locked Detection Contract Setup Flow

Status: Complete

## Scope

- `/config/workspace/IronClaude/src/superclaude/pr_submit/`
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/`
- `/config/workspace/IronClaude/tests/pr_submit/`
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/`

## Findings

### Initial scoped inventory

- Scoped Python source contains existing `pr_submit` modules: `classifier.py`, `detection.py`, `fsm.py`, `loop_guard.py`, `models.py`, `recovery.py`, `run_log.py`, `severity_router.py`, plus package `__init__.py`.
- Scoped reflect CLI source contains `commands.py`, `config.py`, `contract.py`, `ensemble.py`, `models.py`, `runner.py`, plus package `__init__.py`.
- Scoped tests contain existing `tests/pr_submit/test_*.py` coverage plus JSON fixtures under `tests/pr_submit/fixtures/`.
- Design inputs under `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/` include `merged-requirements.md`, `design.md`, `seed-brief.md`, `brainstorm-summary.md`, `return-contract.yaml`, `agent-spec.txt`, `enrichment/codebase-context.md`, and adversarial design artifacts.

### Design target and expected new files

- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md` is the strongest file-inventory source for the intended package. Its frontmatter pins `target_module: src/superclaude/pr_submit/contract_setup/` at line 8, and its scope explicitly calls for a new `superclaude.pr_submit.contract_setup` package at lines 38-45.
- Expected new package root: `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/`.
- Expected new files from the design tree at `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md:67-82`:
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/__init__.py` — facade exporting `diagnose`, `load_evidence`, `derive_candidate`, `validate_candidate`, `write_report`, and `write_lock`.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/states.py` — `ContractState` enum with 9 UX states plus pure state-classification function.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py` — `Diagnosis` dataclass and read-only `diagnose()` path/lock/evidence probe.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py` — `EvidenceBundle`, `load_evidence()`, SHA-256 hashing, and surface mapping.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/candidate.py` — `CandidateContract`, `FieldProvenance`, and `derive_candidate()`.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py` — `ValidationReport`, `CheckResult`, and `validate_candidate()` dry-running the existing classifier.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py` — `LockGate` for ordered safe-locking preconditions.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` — `write_report()` and confirmation-gated `write_lock()`.
  - `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/questions.py` — declarative `SETUP_QUESTIONS` table and default derivation binders.
- The design explicitly says existing `DetectionContract.load()`, `DetectionContract.for_arming()`, and `classify()` semantics must not change; the setup flow consumes these seams rather than replacing them (`design.md:47-58`, `design.md:100-117`).

### Existing `pr_submit` files and symbols to consume or preserve

- `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py`
  - Purpose: detection-contract loader and poll-classification seam for `sc:pr-submit`; module docstring states it exposes `poll_augment_review` and `DetectionContract`, and raises `DetectionContractLocked` when the contract is not locked (`detection.py:1-10`).
  - Key symbols: `_CONTRACT_PATH` points to the shipped ref (`detection.py:27-33`); `_LOCAL_OVERRIDE_REL = Path(".dev/pr-monitor/detection-contract.locked.md")` (`detection.py:40`); `_local_override_path()` resolves the operator-local locked contract (`detection.py:44-53`); `DetectionContractLocked` is the T-210 exception (`detection.py:71-76`); `DetectionContract` fields and defaults span `detection.py:79-117`; `from_yaml()` parses YAML without lock enforcement (`detection.py:119-145`); `load()` resolves explicit path / local override / shipped ref and enforces `locked:true` when required (`detection.py:147-188`); `for_arming()` is the arm path and equals `load(prefer_local_override=True)` (`detection.py:190-199`); `poll_augment_review()` delegates to `classify()` over injected payload/contract (`detection.py:219-250`).
  - Role in implementation: the new setup package should inspect/load contracts through `DetectionContract.load(..., require_locked=False)` or parsing helpers where needed, write only the local override path, and preserve `for_arming()` as the fail-closed arm gate.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/classifier.py`
  - Purpose: pure four-state review classifier; docstring pins return states to `"polling"`, `"clean"`, `"findings"`, and `"declined"` and says it keys on contract-provided Augment identities, not literals (`classifier.py:1-15`).
  - Key exports/symbols: state literals `STATE_POLLING`, `STATE_CLEAN`, `STATE_FINDINGS`, `STATE_DECLINED` (`classifier.py:22-26`); identity helpers `_login_of()`, `_augment_identities()`, `_augment_entries()` (`classifier.py:29-61`); timestamp/staleness helpers `_entry_ts()` and `_is_newer()` (`classifier.py:64-88`); `is_decline()` (`classifier.py:105-140`); `classify(payload, contract, *, watermark=None)` (`classifier.py:158-232`).
  - Role in implementation: `validation.py` should call `classify()` directly for dry-run validation and negative controls; do not duplicate classifier logic in skill markdown or setup code.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/__init__.py`
  - Purpose: public import surface for the existing deterministic `pr_submit` core; docstring enumerates FSM, severity router, loop guard, classifier/detection, run-log, recovery, and models (`__init__.py:1-19`).
  - Key exports: `classify`, `is_decline`, `STATE_DECLINED`, `poll_augment_review`, `DetectionContract`, `DetectionContractLocked`, `run_skill`, `transition`, `parse_args`, `evaluate_push_decision`, `RunConfig`, `remap_severity`, `route`, and model types (`__init__.py:21-62`).
  - Role in implementation: either leave unchanged and expose the new package as `superclaude.pr_submit.contract_setup`, or optionally add facade re-exports only if callers need top-level imports. The design names the package facade as the stable import surface, not this module.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/fsm.py`
  - Purpose: deterministic monitor FSM and CLI flag parser; docstring emphasizes pure decision logic and no side-effecting I/O (`fsm.py:1-17`).
  - Key symbols adjacent to detection setup: `SkillArgs` and `armed` property (`fsm.py:48-68`), `build_arg_parser()` / `parse_args()` (`fsm.py:70-120`), `gate_arm()` (`fsm.py:128-130`), `gate_edit()` (`fsm.py:133-135`), `RunConfig` and `run_skill()` declarations are present later in the file (`fsm.py:717-896` from symbol scan), and `transition()` is the existing state transition entry (`fsm.py:597` from symbol scan).
  - Role in implementation: useful for no-monitor-side-effects tests and `--monitor 0` unaffected assertions. The contract setup flow should not arm monitor, push, reply, resolve, or retrigger.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/models.py`
  - Purpose: canonical enums/dataclasses for monitor events, severities, FSM states, findings, skill results, and push decisions; docstring asserts core purity (`models.py:1-12`).
  - Key symbols: `EventType` (`models.py:20-80`), `Severity` (`models.py:82-90`), `MonitorState` (`models.py:92-126`), `TERMINAL_STATES` (`models.py:128-138`), `Finding` (`models.py:141-175`), `SkillResult` (`models.py:177-216`), `PushDecision` (`models.py:218` onward).
  - Role in implementation: likely only referenced by integration/no-side-effect tests; the new contract setup dataclasses should live in the new package rather than extending monitor FSM dataclasses.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/run_log.py`
  - Purpose: write-ahead JSONL run-log substrate for monitor crash-safety, not contract setup (`run_log.py:1-14`).
  - Key symbols: `IDEMPOTENCY_SETS` (`run_log.py:27-34`), `fix_key()` (`run_log.py:54-56`), `_redact()` (`run_log.py:59-70`), `RunLog` (`run_log.py:73` onward).
  - Role in implementation: should remain out-of-scope except for grep-style no-side-effect/no-monitor tests; setup reports should not write monitor run logs.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/recovery.py`
  - Purpose: crash-window recovery decisions for monitor push flows (`recovery.py:1-20`).
  - Key symbols: `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS` (`recovery.py:27-30`), `resume()` (`recovery.py:33-54`), `detect_crash_window()` (`recovery.py:57-80`), `resolve_crash_window()` (`recovery.py:83-171`).
  - Role in implementation: not a dependency for contract setup; useful as a negative control for no push/resume side effects.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/severity_router.py`
  - Purpose: finding severity remap and troubleshoot routing for review remediation (`severity_router.py:1-13`).
  - Key symbols: route constants (`severity_router.py:53-56`), `remap_severity()` (`severity_router.py:88-137`), `route()` (`severity_router.py:140-160`).
  - Role in implementation: not expected to be consumed by contract setup.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/loop_guard.py`
  - Purpose from symbol inventory: monitor round limits; key symbols include `DEFAULT_MAX_ROUNDS`, `HARD_CAP_MAX_ROUNDS`, `should_halt()`, `user_label()`, and `RoundCounter` (`loop_guard.py:19-39` from symbol scan).
  - Role in implementation: not expected to be consumed by contract setup.

### Existing `reflect` CLI files and integration seams

- `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py`
  - Purpose: Click command group for `superclaude reflect run`; docstring says it exposes the thin fail-closed POST reflect gate and wires exit codes from `Verdict.exit_code` (`commands.py:1-13`).
  - Key symbols: `reflect_group()` (`commands.py:47-73`), `run()` Click subcommand (`commands.py:76-230`), existing options through `--reachability` (`commands.py:81-179`), and tmux helpers later in the file (`commands.py:297-360` from symbol scan).
  - Role in implementation: the design recommends adding a narrow contract readiness path for `/sc:reflect`/reflect CLI. A likely implementation location is a new Click subcommand in this file that calls the `contract_setup` facade and does not launch `ReflectRunner`.
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/config.py`
  - Purpose: resolves reflect run inputs into `ReflectConfig`, including git state and preflight STOPs (`config.py:1-14`).
  - Key symbols: `_git()` (`config.py:64-78`), `_resolve_base()` (`config.py:81-105`), `_audit_tree_dirty()` (`config.py:108-148`), `create_review_snapshot()` (`config.py:151-204`), `teardown_review_snapshot()` (`config.py:207-220`), `_is_under_claude_protected()` and `resolve_config()` later in the file (symbol scan shows `resolve_config` at `config.py:238`).
  - Role in implementation: probably not needed for contract readiness; avoid routing setup status through full reflect run config unless the new command needs shared repo-root resolution.
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/contract.py`
  - Purpose: pure parser/verdict mapper for `return-contract.yaml`; docstring says it is the single place for verdict map, FR-11 degradation routing, and contract-version gating (`contract.py:1-13`).
  - Key symbols: `parse_contract()` (`contract.py:65-82`), `derive_verdict()` (`contract.py:130-246`), `_degraded_reason()` (`contract.py:249` onward), `_halted_reason()` and `classify_fix()` later in file (symbol scan shows `contract.py:307` and `contract.py:331`).
  - Role in implementation: do not confuse reflect's `return-contract.yaml` verdict contract with PR-submit detection contracts. The new setup package should likely use its own validation-report schema rather than extending this verdict mapper.
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/models.py`
  - Purpose: reflect wrapper data models and verdict enum (`models.py:1-17`).
  - Key symbols: `Verdict` with exit-code mapping (`models.py:26-55`), `ReflectConfig` (`models.py:57-115`), `ReflectResult` (`models.py:117-157`).
  - Role in implementation: status-only contract readiness output may not need these types unless implemented as part of reflect wrapper result emission.
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/runner.py`
  - Purpose: reflect wrapper orchestration and atomic frontmatter/sidecar writers (`runner.py:1-18`).
  - Key symbols: `_atomic_write_text()` (`runner.py:71-90`), `write_reflect_post()` (`runner.py:120-188`), `write_sidecar()` (`runner.py:191-244`), `preflight()` and `ReflectRunner` later in the file (symbol scan shows `runner.py:273` and `runner.py:337`).
  - Role in implementation: `contract_setup.writer` can copy the safe atomic-write pattern if needed, but should not reuse reflect frontmatter write-back for `.dev/pr-monitor/` reports.
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/ensemble.py`
  - Purpose from symbol inventory: Tier-2 ensemble and reflect contract emission; key constants include `REFLECT_CONTRACT_VERSION`, `CONTRACT_FILENAME`, and `MZERO_CONTRACT_MISSING_SLUG`; key functions include `run_tier2_ensemble()`, `build_reflect_contract()`, and `_emit_reflect_contract()` (symbol scan shows `ensemble.py:60-70`, `ensemble.py:168`, `ensemble.py:492`, `ensemble.py:669`).
  - Role in implementation: not a dependency for detection-contract readiness; avoid coupling detection setup to reflect Tier-2 contract emission.

### Existing tests and likely new test locations

- `/config/workspace/IronClaude/tests/pr_submit/conftest.py`
  - Purpose: shared `tests/pr_submit` fixtures; docstring lists `load_fixture`, `mock_gh`, `mock_monitor`, `fixture_findings`, and `tmp_skill_dir` (`conftest.py:1-8`).
  - Key symbols: `FIXTURES_DIR` (`conftest.py:17`), `load_fixture()` (`conftest.py:20-27`), `mock_gh()` (`conftest.py:30-51`), `mock_monitor()` (`conftest.py:54-65`), `fixture_findings()` (`conftest.py:68-73`), `tmp_skill_dir()` (`conftest.py:76-81`).
  - Role in implementation: new setup tests can reuse `load_fixture`; may need new temporary evidence-directory fixtures local to a new test module.
- `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py`
  - Purpose: existing classifier and T-210 detection-contract regression coverage; docstring covers T-201/T-202/T-203/T-210/T-211/T-212 and notes fixture migration (`test_detection_contract.py:1-14`).
  - Key tests: `test_t210_locked_false_halts()` verifies shipped/default unlocked and absent contracts raise `DetectionContractLocked`, while `require_locked=False` permits inspection (`test_detection_contract.py:76-97`); `test_local_override_arms_without_touching_shipped_source()` verifies local override arming while default load still halts (`test_detection_contract.py:100-125`); decline and identity tests cover negative controls (`test_detection_contract.py:193-237`, `test_detection_contract.py:258-375`).
  - Role in implementation: extend or keep as regression anchor for unchanged `DetectionContract` behavior. The design explicitly says new tests live alongside this file (`design.md:538-557`).
- Likely new test modules under `/config/workspace/IronClaude/tests/pr_submit/`:
  - `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_diagnosis.py` — `ContractState`, `Diagnosis`, checked paths, shipped-only/unlocked/unparseable/evidence-missing states, and better halt summary.
  - `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_evidence.py` — `EvidenceBundle`, surface detection, canonical SHA-256, pagination/freshness metadata, missing/malformed evidence.
  - `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_candidate.py` — provenance, required-unobserved refusal, defaults-not-enough-to-lock, cross-PR shape-only behavior.
  - `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_validation.py` — dry-run `classify()` checks, expected-not-polling, negative controls for non-Augment copied text, clean/findings/declined distinction.
  - `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_writer.py` — report writing, local lock destination under `.dev/pr-monitor/`, confirmation gate, shipped ref remains unlocked.
  - `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_reflect_cli.py` or reflect-side tests if a Click `contract-status` subcommand is added.
  - `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_no_side_effects.py` — grep-style guard that setup paths do not arm Monitor or call push/reply/resolve/retrigger. This mirrors the design's critical invariant test at `design.md:559-561`.
- Existing test inventory already has broad monitor and static guards that should remain separate from setup tests: `test_monitor_arm.py` covers arm/no-arm behavior; `test_static_grep.py` covers repo-scoped GitHub calls and core-purity checks; `test_edge_cases.py` includes `test_ec11_contract_locked_false_halts_probe`; `test_skill_parse.py` covers `--monitor` parsing; these should be referenced briefly but not overloaded with setup logic.

### Design and requirement files in scope

- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`
  - Purpose: merged product requirements for locked detection contract setup.
  - Key requirements: `/sc:pr-submit --monitor >=1` keeps fail-closed arming and stops before arming on no locked contract (`merged-requirements.md:14-18` from retrieval); shared helper owns diagnosis, evidence loading/capture, derivation, validation, reports, and local locked-contract writing (`merged-requirements.md:53-55` from retrieval); `/sc:reflect --contract-status` and `--validate` readiness path is specified at `merged-requirements.md:317-333`; minimal implementation plan is at `merged-requirements.md:335-345`.
  - Role in implementation: source of acceptance criteria and integration boundaries.
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md`
  - Purpose: component design and file decomposition; it is design only and explicitly says implementation follows after approval (`design.md:11-17`).
  - Key sections: existing seam table (`design.md:19-32`), package decomposition (`design.md:60-82`), data model including `ContractState`, `Diagnosis`, `EvidenceBundle`, `FieldProvenance`, `CandidateContract`, `CheckResult`, and `ValidationReport` (`design.md:139-220`), test matrix (`design.md:538-557`), minimal implementation order (`design.md:563-575`).
  - Role in implementation: direct blueprint for new files, symbols, and test placement.
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/seed-brief.md`
  - Purpose: initial brief; codebase context notes existing seams: `DetectionContract`, lock enforcement, local override, pure `poll_augment_review`, protocol halt behavior, shipped unlocked schema, and reflect command delegation (retrieval cited `seed-brief.md:54-58`).
  - Role in implementation: background only; design/requirements are more actionable.
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/enrichment/codebase-context.md`
  - Purpose: enrichment scan; records that `detection.py` has `DetectionContract`, `from_yaml`, `load`, `for_arming`, `_extract_yaml_block`, and `poll_augment_review`, while `fsm.py` is separate from GitHub I/O (retrieval cited `codebase-context.md:7-9`).
  - Role in implementation: confirms reuse seams and non-overlap with FSM.
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/adversarial/*.md`, `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/brainstorm-summary.md`, `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/agent-spec.txt`, and `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/return-contract.yaml`
  - Purpose: supporting brainstorm/debate/audit artifacts. They are useful for rationale but should not override `merged-requirements.md` and `design.md` when building the task file.

### File inventory implications for task-builder

- Primary implementation files to create are all under `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/`; source-of-truth discipline does not require `.claude/` edits for these Python modules.
- Existing files most likely to edit for integration are `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py` for a readiness subcommand and possibly source skill/command files outside this research scope for `/sc:pr-submit` halt rendering. Within the scoped Python files, `detection.py` and `classifier.py` should be treated as consumed invariants, not modified seams.
- Existing tests most likely to extend are under `/config/workspace/IronClaude/tests/pr_submit/`, with new `test_contract_setup_*.py` modules preferable to bloating `test_detection_contract.py`.
- Do not put generated reports or locked contracts in source; design points reports/locks to `.dev/pr-monitor/` and keeps the shipped detection contract unlocked/generic.

## Gaps and Questions

- [UNVERIFIED design decision] Fork A remains a human-decision gate: the design recommends the package `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/`, while a single `contract_setup.py` module is an alternative with the same facade. The generated task should default to the package only after recording OQ-1 and should not silently remove the decision.
- [UNVERIFIED design decision] Fork B remains a human-decision gate: recommended implementation is the sibling CLI command `superclaude reflect contract-status [--validate] --repo --pr`, while the source requirements show `/sc:reflect --contract-status --validate --repo --pr` examples. The generated task must include OQ-2 before dependent reflect-surface implementation.
- [UNVERIFIED design decision] Live GitHub capture is V2/deferred unless explicitly accepted. File-based evidence loading/validation is the v1 implementation scope.

## Key Takeaways

- [CODE-VERIFIED] Existing `DetectionContract.load()`, `DetectionContract.for_arming()`, and `classify()` are consumed seams and should remain semantically unchanged.
- [CODE-VERIFIED] Primary implementation output is a new helper package under `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/`, gated by OQ-1.
- [CODE-VERIFIED] Tests should be added under `/config/workspace/IronClaude/tests/pr_submit/` and `/config/workspace/IronClaude/tests/cli/reflect/` rather than overloading existing detection/classifier tests.
