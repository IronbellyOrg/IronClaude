# Source-Fidelity — Requirements §1–8

**Lens:** requirements-1-8-fidelity | **Phase:** report-validation | **Fix authorization:** false | **Date:** 2026-07-02

Note: Agent A returned this matrix directly; the orchestrator persisted it at the required path.

## VERDICT: PASS

No dropped, mutated, or phantom requirement across §1–8. Every requirement traces to concrete implementation AND passing test evidence (82 helper/CLI/integration tests pass live). OQ-1/OQ-2/OQ-3 handled exactly as decided.

## Requirement → Evidence Matrix

| § | Requirement | Result | Evidence |
|---|---|---|---|
| §1.1 | pr-submit `--monitor>=1` keeps fail-closed arming; diagnosis + next-safe-cmd on missing lock | PASS | `for_arming()` raises `DetectionContractLocked` before arm (`detection.py:191`); halt renders diagnosis + `superclaude reflect contract-status` (`diagnosis.py:233-255`, `pr-submit.md:61`). Test: `test_missing_contract_for_arming_halts_before_monitor_arm` (arm recorder == 0). |
| §1.2 | reflect readiness; v1 does NOT write local lock by default | PASS | CLI `contract-status` calls diagnose/validate_candidate/write_report only — never `write_lock` (`commands.py:99-142`). Test: `test_contract_status_validate_does_not_write_lock_by_default`. |
| §1.3 | Shared helper owns diagnosis/evidence/candidate/validation/report+lock | PASS | 9-module package; all seams present. |
| §1.4 | Shipped contract stays `locked:false`; repo data only under `.dev/pr-monitor/` | PASS | Shipped ref `locked:false`; writer forces dest to `.dev/pr-monitor/…` (`writer.py:125-141`). Test: `test_lock_destination_is_exactly_dev_pr_monitor_under_cwd`. |
| §1.5 | Creation never arms/posts/pushes/resolves/resumes without confirm | PASS | Static import-graph audit: no fsm/monitor import in helper; `test_writer_package_imports_no_fsm_seams`, `test_diagnose_and_render_perform_no_side_effects`. |
| §2 | Ownership boundary | PASS | pr-submit.md keeps `for_arming()`; reflect.md routes to CLI; helper owns the five responsibilities; no FSM leakage. |
| §3 | 9 UX states | PASS | `ContractState` = 9 values (`states.py:11-19`); tests cover each in `test_contract_setup_diagnosis.py`. |
| §4 | 16 questions; defaults are suggestions only | PASS | `SETUP_QUESTIONS` = 16 IDs in order; `test_setup_question_sequence_contains_all_16...`; defaults-are-suggestions proven via provenance.observed=False. |
| §5 | Classifier-critical schema + v1 metadata extension | PASS | Writer emits all schema fields + metadata block; `test_lock_metadata_includes_evidence_hash_and_validation_report`. |
| §6 | 12 safe-lock preconditions; never-guess values | PASS | `LockGate.CHECK_IDS` = 12; `MUST_OBSERVE_FIELDS` enforces never-guess; refusal tests raise `ContractSetupRefused`. |
| §7 | Validation checklist families | PASS | `validate_candidate` runs structure/evidence/identity/surface-path/classifier-dry-run/freshness incl. negative controls + `classify()` reuse; `test_validation_reuses_classify_seam_dry_run_only` + mismatch/negative-control tests. |
| §8 | `.dev/pr-monitor/` layout; summaries metadata-only | PASS | `write_report` gates dest to probes; all `summary()` redact bodies; sentinel-on-disk redaction tests non-trivial. |
| OQ-1 | `package` | PASS | 9-module package with lazy facade. |
| OQ-2 | `sibling-cli-command` | PASS | Single Click subcommand; help exposes exactly `--validate`/`--repo`/`--pr`; no second surface. |
| OQ-3 | `file-based-v1-only` | PASS | grep confirms zero subprocess/requests/urllib/httpx/gh/socket/http in the helper package. |

## Findings

None. Two adversarial probes cleared: (1) the "not yet implemented" placeholder is gone (`test_contract_setup_next_commands_are_current_and_actionable` asserts absence); (2) the tautological no-side-effect test was genuinely replaced with a static import-graph audit + no-writes snapshot.

## Non-blocking observation

The `stale` state is produced by `_stale_blockers` (`diagnosis.py:329-356`) and reachable via repo/PR/hash mismatch; `test_contract_setup_diagnosis.py` lacks a dedicated `state is STALE` assertion (the other 8 states each have one). Stale *blocking* is covered at the validation layer (`test_repo_mismatch_blocks_lock`, `test_missing_evidence_hash_blocks_lock`). §3's 9-state classification requirement is met in code — this is a test-thoroughness note, not a dropped requirement.

Confidence: 15/15 verified = 100%. No files modified.
