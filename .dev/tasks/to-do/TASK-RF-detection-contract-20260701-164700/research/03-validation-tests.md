# Test & Verification Strategy for Locked Detection Contract Setup Flow

Status: Complete

## Findings Log

### Initial acceptance and existing test surface

- Acceptance source is `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`.
- The product boundary requires `/sc:pr-submit --monitor >=1` to keep the fail-closed arming gate and stop before arming when no locked contract resolves, while `/sc:reflect` only diagnoses/validates readiness and must not write by default (`merged-requirements.md:16-18`, `merged-requirements.md:33-45`).
- The setup flow has exactly 16 bounded questions/defaults to cover in tests (`merged-requirements.md:79-150`). The most important lock-safety assertions are: no monitor arming/PR mutation as part of setup (`merged-requirements.md:20`, `merged-requirements.md:143-150`), explicit write confirmation (`merged-requirements.md:201-203`), and no raw GitHub payload bodies in reflect status output (`merged-requirements.md:43-45`).
- Existing detection-contract tests live at `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py`. They already cover classifier states, fail-closed locked gate, local override arming, wrong-bot negatives, interleaved human/Augment handling, and decline classification (`test_detection_contract.py:44-125`, `test_detection_contract.py:128-182`, `test_detection_contract.py:192-240`).
- Existing shared test fixtures for `/config/workspace/IronClaude/tests/pr_submit/` include `load_fixture`, `mock_gh`, `mock_monitor`, `fixture_findings`, and `tmp_skill_dir`; these are the right patterns for in-process setup-flow tests (`conftest.py:20-81`).
- Pytest is configured to discover `tests/`, strict markers, and verbose output in `/config/workspace/IronClaude/pyproject.toml:104-145`. The package dependencies already include `pytest`, `click`, `pyyaml`, and `jsonschema` (`pyproject.toml:34-43`).
- UV-only commands are already encoded in the project Makefile for `make test` and lints (`Makefile:12-16`, `Makefile:47-55`); direct scoped test commands should still use `uv run pytest ...`.

## Existing patterns to extend

### Detection and classifier tests

- Extend `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py` for loader/classifier-adjacent behavior only. Existing `test_t210_locked_false_halts` proves the shipped contract and absent/unlocked explicit files raise `DetectionContractLocked`, while `require_locked=False` can inspect an unlocked contract (`test_detection_contract.py:76-97`). Keep this test intact as the regression that setup diagnostics must not weaken the arm gate.
- Existing `test_local_override_arms_without_touching_shipped_source` pins the local override path semantics: default `load()` ignores the override, but `DetectionContract.for_arming()`/`prefer_local_override=True` uses it (`test_detection_contract.py:100-125`). New safe-writer tests should assert the writer targets the same operator-local path contract, not the shipped ref.
- Existing wrong-bot/interleaved tests already provide negative-control shape: non-Augment bot stays `polling`, and human reviews are ignored (`test_detection_contract.py:128-182`). Reuse those payload ideas for setup validation negative controls.
- The pure classifier recognizes identities from `augment_bot_login` and `augment_app_slug` only, never prose (`classifier.py:46-61`, `classifier.py:177-208`). Setup validation should test that copied text by a human is ignored even if it contains Augment-like content.
- `poll_augment_review` is a test-friendly in-process seam: callers can inject payload/contract, and absent contract defaults to a neutral unlocked placeholder that stays fail-safe polling (`detection.py:219-250`). Use it for candidate validation tests rather than shelling out.

### FSM/no-side-effect patterns

- `/config/workspace/IronClaude/tests/pr_submit/test_monitor_arm.py` has a minimal `_ArmRecorder` seam and asserts L1 monitor arm count vs L0 no-arm behavior (`test_monitor_arm.py:16-43`). Reuse this style for “setup/diagnosis does not arm monitor”.
- `/config/workspace/IronClaude/tests/pr_submit/test_autonomy_gates.py` records push/reply/resolve seams with `_Recorder` and asserts they are not called at lower autonomy levels (`test_autonomy_gates.py:46-52`, `test_autonomy_gates.py:83-100`). Use identical recorders for setup no-side-effect assertions: no comments, pushes, retries, resolves, retriggers.
- `RunConfig` exposes all side-effect seams as injected callables with recording-only defaults (`fsm.py:717-760`), and `run_skill()` arms at `ordinal >= 1` before classification (`fsm.py:896-924`). Therefore setup-flow tests should stay outside `run_skill()` or explicitly prove the missing-contract halt happens before any `run_skill()`/arm seam can be reached.

### Reflect CLI test patterns

- Reflect CLI smoke tests patch `superclaude.cli.reflect.runner.ClaudeProcess` and assert dry-run/print-command paths never launch (`test_cli_smoke.py:51-72`). Use the same patching pattern for `--contract-status` / `--contract-status --validate` to prove readiness checks do not launch the reflect audit subprocess and do not mutate task files.
- Reflect CLI help coverage is centralized via `_SPEC9_FLAGS` and `test_run_help_shows_all_spec9_flags` (`test_cli_smoke.py:16-35`, `test_cli_smoke.py:44-49`). Add new contract-status flags there or create a focused sibling list so CLI exposure is pinned.
- CLI/docs parity already derives Click flags from `superclaude.cli.reflect.commands.run.params` and compares them with documented flags (`test_docs_cli_parity.py:36-45`, `test_docs_cli_parity.py:83-92`). If the implementation adds docs for `--contract-status`, `--repo`, `--pr`, or `--validate`, update this parity test or add a dedicated contract-status guide section parity test.
- Current reflect run command is tasklist-required and has no contract-status options yet (`commands.py:76-180`). If contract-status should run without a tasklist, tests must cover the Click shape explicitly because the current positional `tasklist` argument is required (`commands.py:76-80`).

## Proposed test files and test names by acceptance area

### 1. Shared helper diagnosis and state classification

Create `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_diagnosis.py`.

Recommended tests:

- `test_contract_status_missing_reports_setup_command_without_loading_shipped_as_ready`
  - Fixture: temp cwd with no `.dev/pr-monitor/detection-contract.locked.md`.
  - Assert state `missing`, checked paths include shipped ref and local override, recommended next step is diagnostic/setup only, and readiness is not `ready`.
  - Acceptance: UX states `missing`, `/sc:pr-submit` halt diagnosis (`merged-requirements.md:63-77`, `merged-requirements.md:298-305`).
- `test_contract_status_unlocked_local_contract_is_not_ready`
  - Local override exists with `locked: false`; assert state `unlocked`, no arming allowed.
  - Regression pairs with existing T-210 (`test_detection_contract.py:76-97`).
- `test_contract_status_unparseable_preserves_file_and_reports_regenerate_option`
  - Local override exists with malformed/no YAML; assert state `unparseable`, path reported, file content unchanged.
- `test_contract_status_evidence_missing_for_locked_contract_blocks_ready`
  - Locked contract names nonexistent `probe_evidence`; assert `evidence_missing` and no validation pass.
- `test_contract_status_validation_missing_blocks_ready_until_report_exists`
  - Evidence exists, but metadata lacks validation report; assert `validation_missing`.
- `test_contract_status_validation_failed_reports_blockers`
  - Validation report exists with failed result; assert `validation_failed` and blocker count/path, not raw body.
- `test_contract_status_ready_requires_locked_contract_evidence_and_passed_report`
  - Fully valid local override + evidence + passed validation report; assert `ready`.

### 2. Candidate derivation and 16 setup questions

Create `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_questions.py`.

Recommended tests:

- `test_setup_question_sequence_contains_all_16_questions_in_order`
  - Assert the helper’s question model/list has exactly 16 stable IDs in the acceptance order: repo, probe PR, operation, evidence source, surfaces, identity, author association, emission shape, findings locus, severity path, completeness signal, decline fields, expected classifier result, run validation, write local lock, next step (`merged-requirements.md:83-150`). This is the main “all 16 setup questions” guard.
- `test_setup_defaults_are_suggestions_not_lock_values_without_evidence`
  - Provide no observed identity/surface/path; assert defaults may be displayed but candidate cannot lock. Covers “must never be guessed” values (`merged-requirements.md:213-220`).
- `test_multiple_augment_identity_candidates_require_explicit_selection`
  - Payload has two plausible Augment identities; assert no default lock and prompt requires explicit choice (`merged-requirements.md:105-108`, `merged-requirements.md:241-245`).
- `test_unobserved_emission_shape_cannot_be_locked`
  - User selects `check_run` when evidence has only reviews/comments; assert validation blocks (`merged-requirements.md:114-118`, `merged-requirements.md:247-253`).
- `test_polling_expected_result_is_never_lockable`
  - Candidate + evidence classifies as `polling`; assert write is blocked (`merged-requirements.md:135-141`, `merged-requirements.md:197-199`, `merged-requirements.md:255-260`).
- `test_decline_validation_not_exercised_warns_but_does_not_block_otherwise_valid_lock`
  - No decline sample but other validation passes; assert warning `decline_validation: not_exercised` and pass (`merged-requirements.md:131-134`, `merged-requirements.md:184-185`).

### 3. Validation report, redaction, and raw payload body exclusion

Create `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_validation.py`.

Recommended tests:

- `test_validation_report_records_hash_repo_pr_surfaces_and_classifier_result`
  - Evidence file under `.dev/pr-monitor/probes/.../combined-payload.json`; assert report has hash, repo, PR, capture time, surfaces, classifier result, and validation result (`merged-requirements.md:232-260`, `merged-requirements.md:270-292`).
- `test_validation_summary_omits_raw_payload_bodies`
  - Payload contains unique sentinel body text such as `RAW_BODY_SENTINEL_DO_NOT_PRINT`; generated summary/status output must include counts, paths, hash, blockers, but must not include that sentinel or serialized `body` fields. Acceptance explicitly says summaries display status, paths, hashes, counts, blockers, not full raw payload bodies (`merged-requirements.md:294`).
- `test_validation_report_body_redaction_keeps_counts_and_blockers`
  - Same sentinel payload; assert summary still names the blocker category/field and evidence hash so redaction does not make diagnostics useless.
- `test_negative_controls_empty_and_non_augment_payload_stay_polling`
  - Validate candidate against empty payload and non-Augment-authored payload; both must not classify as reviewed (`merged-requirements.md:199-200`, `merged-requirements.md:257-260`). Reuse existing fixture style from `test_detection_contract.py:128-154`.
- `test_findings_locus_and_completion_signal_must_resolve_against_evidence`
  - Candidate field path points to missing location; assert validation fails for findings/completion paths (`merged-requirements.md:196-198`, `merged-requirements.md:247-253`).
- `test_severity_path_non_null_must_resolve_or_fail`
  - Non-null severity path missing; assert failure. If null, assert pass with “severity not field-backed” warning (`merged-requirements.md:123-125`, `merged-requirements.md:252`).

### 4. Omitted-surface and cross-PR/staleness behavior

Add to `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_validation.py` or split into `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_freshness.py`.

Recommended tests:

- `test_omitted_surfaces_are_recorded_in_validation_report`
  - Validate only reviews/comments while check-runs are supported but omitted; report must record omitted surfaces (`merged-requirements.md:101-103`, `merged-requirements.md:238-239`).
- `test_omitted_surface_prevents_ready_when_selected_surface_unvalidated`
  - Candidate selects check-run surface but validation omitted check-runs; assert not ready.
- `test_repo_mismatch_blocks_lock`
  - Evidence metadata repo differs from resolved repo; assert validation blocks (`merged-requirements.md:192-195`, `merged-requirements.md:262-265`).
- `test_missing_or_mismatched_evidence_hash_blocks_lock`
  - Evidence hash absent or mismatched; assert validation blocks (`merged-requirements.md:201`, `merged-requirements.md:264-265`).
- `test_cross_pr_evidence_requires_explicit_confirmation_and_shape_only`
  - Evidence PR differs from target PR. Without explicit confirmation, block. With confirmation, allow only shape validation/readiness warning, not “current review state ready” (`merged-requirements.md:193-194`, `merged-requirements.md:266-268`).
- `test_stale_evidence_over_30_days_warns_or_blocks_per_policy`
  - V1 default age warning threshold is 30 days unless tightened (`merged-requirements.md:268`). Test expected warning and no silent ready.

### 5. Safe writer and no shipped/.claude writes

Create `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_writer.py`.

Recommended tests:

- `test_write_locked_contract_requires_explicit_confirmation`
  - Validation passed but confirmation false; assert no file written and state `declined_by_user` or equivalent (`merged-requirements.md:77`, `merged-requirements.md:201-203`).
- `test_write_locked_contract_targets_dev_pr_monitor_only`
  - Confirmed write; assert path is `.dev/pr-monitor/detection-contract.locked.md`, not shipped ref and not `.claude/` (`merged-requirements.md:201-203`, `detection.py:35-53`).
- `test_writer_preserves_shipped_contract_locked_false`
  - After local write, `DetectionContract.load()` still halts on shipped source, while `DetectionContract.for_arming()` loads the local override. Mirrors existing local override test (`test_detection_contract.py:100-125`).
- `test_writer_outputs_metadata_validation_report_and_evidence_hash`
  - Written YAML includes metadata from recommended extension: schema version, repo, PR, evidence hash, validation report, validation result, classifier result, validated surfaces, decline validation (`merged-requirements.md:171-186`).

### 6. `/sc:pr-submit` missing-contract halt integration

Create `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_pr_submit_integration.py`.

Recommended tests:

- `test_pr_submit_monitor_missing_contract_halts_before_monitor_arm`
  - Patch/record monitor arm; no locked contract. Assert halt message/state includes checked paths and next safe setup command, and arm count is zero (`merged-requirements.md:298-305`).
- `test_pr_submit_missing_contract_prints_no_side_effects_sentence`
  - Assert exact or stable substring: “No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.” (`merged-requirements.md:304`).
- `test_pr_submit_after_lock_uses_existing_for_arming_path`
  - With local locked contract in place, assert no special setup path and `DetectionContract.for_arming()` succeeds (`merged-requirements.md:315`).
- `test_pr_submit_setup_does_not_execute_rerun_command`
  - Setup output may print a recommended `/sc:pr-submit --monitor >=1` command, but no run/arm occurs (`merged-requirements.md:37`, `merged-requirements.md:148-150`).

### 7. `/sc:reflect` contract-status CLI integration

Add to `/config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py` or create `/config/workspace/IronClaude/tests/cli/reflect/test_contract_status_cli.py`.

Recommended tests:

- `test_reflect_group_help_shows_contract_status_subcommand`
  - Canonical v1 surface is the design-recommended sibling Click command `superclaude reflect contract-status [--validate] --repo --pr`, not flags on `reflect run`. Assert group help lists `contract-status` and the subcommand help lists `--validate`, `--repo`, and `--pr`.
- `test_contract_status_diagnose_does_not_launch_claudeprocess`
  - Patch `ClaudeProcess`; invoke `reflect contract-status --repo <owner/repo> --pr <n>`; assert not called, exit code reflects diagnosis readiness, and output includes readiness/blockers (`test_cli_smoke.py:51-72`, `merged-requirements.md:326-333`).
- `test_contract_status_validate_does_not_write_lock_by_default`
  - Existing evidence validates; assert validation report may be written under `.dev/pr-monitor/probes/`, but `.dev/pr-monitor/detection-contract.locked.md` is not written unless explicit writer path is used (`merged-requirements.md:326-333`, `merged-requirements.md:337-343`).
- `test_contract_status_output_redacts_raw_payload_body`
  - Same sentinel-body strategy as helper summary test, but through Click output.
- `test_contract_status_can_run_without_tasklist`
  - Current `reflect run` requires a `tasklist` (`commands.py:76-80`), so the sibling `contract-status` command must be independently invocable without a tasklist and without launching normal reflect audit machinery.

## Regression/no-side-effect guard strategy

- Keep existing T-210 and local override tests unchanged; add new tests around them rather than replacing them. These are the hard guard that setup diagnostics do not make shipped `locked:false` armable (`test_detection_contract.py:76-125`).
- For every setup/diagnose/validate entry point, use recorder seams for arm, push, reply, resolve, retrigger, retry, and resume. The expected counts are all zero unless the test is deliberately testing `DetectionContract.for_arming()` after a lock exists.
- Add a static or path assertion that generated artifacts are under `/config/workspace/IronClaude/.dev/pr-monitor/` only, matching the required output layout (`merged-requirements.md:270-292`). Explicitly assert no writes to `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md` and no writes under `/config/workspace/IronClaude/.claude/`.
- Use sentinel payload values to detect raw-body leaks: put a unique string in `reviews[].body`, `comments[].body`, and `check_run.output.text`; assert summaries/status output do not contain the sentinel, while raw evidence JSON still does.
- For omitted surfaces, assert both positive recording (`validated_surfaces`, `omitted_surfaces`) and negative behavior (a candidate cannot select an omitted/unvalidated surface and become ready).
- For cross-PR evidence, split shape validation from current-state readiness: explicit confirmation may allow candidate field validation, but the report should clearly state cross-PR shape-only and should not present the target PR as reviewed/ready.

## UV-only validation commands

Scoped commands for the implementation branch:

```bash
uv run pytest /config/workspace/IronClaude/tests/pr_submit/test_contract_setup_diagnosis.py /config/workspace/IronClaude/tests/pr_submit/test_contract_setup_questions.py /config/workspace/IronClaude/tests/pr_submit/test_contract_setup_evidence.py /config/workspace/IronClaude/tests/pr_submit/test_contract_setup_validation.py /config/workspace/IronClaude/tests/pr_submit/test_contract_setup_writer.py /config/workspace/IronClaude/tests/pr_submit/test_contract_setup_pr_submit_integration.py -v
```

If reflect CLI changes are included:

```bash
uv run pytest /config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py /config/workspace/IronClaude/tests/cli/reflect/test_contract_status_cli.py /config/workspace/IronClaude/tests/cli/reflect/test_docs_cli_parity.py -v
```

Regression pack for existing pr-submit behavior:

```bash
uv run pytest /config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py /config/workspace/IronClaude/tests/pr_submit/test_monitor_arm.py /config/workspace/IronClaude/tests/pr_submit/test_autonomy_gates.py /config/workspace/IronClaude/tests/pr_submit/test_validation_gate.py -v
```

Project validation after source changes:

```bash
uv run pytest /config/workspace/IronClaude/tests/pr_submit/ /config/workspace/IronClaude/tests/cli/reflect/ -v
```

If Python source is changed, run scoped ruff rather than broad formatting:

```bash
uv run ruff check /config/workspace/IronClaude/src/superclaude/pr_submit /config/workspace/IronClaude/src/superclaude/cli/reflect /config/workspace/IronClaude/tests/pr_submit /config/workspace/IronClaude/tests/cli/reflect
```

If files under `src/superclaude/skills`, `src/superclaude/agents`, or `src/superclaude/commands` are edited, run sync validation after `make sync-dev`:

```bash
make sync-dev && make verify-sync
```

## Summary

The strongest strategy is to add focused unit tests around a new shared helper under `/config/workspace/IronClaude/src/superclaude/pr_submit/`, then thin integration tests for `/sc:pr-submit` and `superclaude reflect` CLI surfaces. Existing tests already provide the key safety patterns: T-210 fail-closed loading, local override preference, pure classifier negative controls, recorder-based no-side-effect seams, and reflect CLI “does not launch” patching. The new tests should make the setup contract impossible to lock from guessed values, impossible to mark ready from omitted/cross-PR/stale evidence, and impossible to leak raw payload bodies in summaries.

## Gaps and Questions

- [UNVERIFIED design decision] OQ-1/Fork A must be resolved or accepted as the package default before implementation of `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/` begins.
- [UNVERIFIED design decision] OQ-2/Fork B is normalized in this test plan to the recommended sibling CLI command `superclaude reflect contract-status [--validate] --repo --pr`; if the user instead chooses slash-command-only flags, the reflect CLI tests above must be rewritten before implementation.
- [UNVERIFIED design decision] OQ-3/V2 live capture is deferred. These tests cover file-based evidence loading and validation only.

## Key Takeaways

- [CODE-VERIFIED] The canonical no-side-effect halt sentence for tests is: “No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.”
- [CODE-VERIFIED] The scoped helper test command must include `test_contract_setup_evidence.py` so `EvidenceBundle`, SHA, omitted surfaces, and surface mapping are not skipped.
- [CODE-VERIFIED] Reflect contract-status tests should assert that `ClaudeProcess`/normal reflect audit machinery is not launched.
