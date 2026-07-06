# QA Report — Phase 2 Evidence Quality

**Topic:** Locked Detection Contract Setup Flow for `/sc:reflect` and `/sc:pr-submit`
**Date:** 2026-07-01
**Phase:** synthesis-gate-equivalent / task-integrity evidence-quality
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

Implementation is not evidence-safe. ContractState names match exactly, and assigned source paths/symbols exist, but multiple implemented behaviors are either not traceable to the requirements/design or contradict explicit requirements. PASS is blocked by fabricated/unimplemented `superclaude reflect contract-status`, accepting empty evidence as a loaded bundle, an invalid `decline_validation` enum value, missing required lock metadata, and a gate that does not actually verify that a validation report was written.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Assigned file inventory | PASS | Read all 11 assigned files plus design and merged requirements: `contract_setup/__init__.py`, `states.py`, `diagnosis.py`, `evidence.py`, `questions.py`, `candidate.py`, `validation.py`, `lockgate.py`, `writer.py`, `sc-pr-submit-protocol/SKILL.md`, `commands/pr-submit.md`, `design.md`, `merged-requirements.md`. |
| 2 | Behavior traces to design/requirements | FAIL | Traced module responsibilities to requirements/design. Failures found: `load_evidence()` accepts empty directories despite design requiring FileNotFoundError for no payload; `decline_validation` emits `exercised`; lock metadata omits `generated_at` and `validation_report`; `LockGate.report_written` checks no written report path. |
| 3 | No fabricated file paths or symbols | FAIL | `diagnosis._next_command()` and command/skill docs emit `superclaude reflect contract-status`; `rg` over `src/superclaude/cli/reflect`, `src/superclaude/commands`, and reflect skill files found only `reflect run` in `cli/reflect/commands.py`, no `contract-status` command implementation. |
| 4 | Nine `ContractState` names match exactly | PASS | `rg` comparison showed `states.py` lines 11-19 match design lines 143-151 exactly: MISSING, UNLOCKED, UNPARSEABLE, EVIDENCE_MISSING, VALIDATION_MISSING, VALIDATION_FAILED, STALE, READY, DECLINED_BY_USER. |
| 5 | Existing seam claims verified | PASS | Read `detection.py` and `classifier.py`: `DetectionContract.load(... prefer_local_override=True)` and `for_arming()` exist, `DetectionContractLocked` exists, `classify(payload, contract, *, watermark=None)` exists, and result literals are present. |
| 6 | No fabricated assigned source symbols | PASS | `rg` verified exported facade symbols (`diagnose`, `load_evidence`, `derive_candidate`, `validate_candidate`, `write_report`, `write_lock`, `LockGate`, `ContractState`) exist under assigned `contract_setup` files. |
| 7 | Runtime spot checks for evidence-quality claims | FAIL | `uv run python` probe showed empty directory `load_evidence()` returned `EvidenceBundle(surfaces=[], combined_payload={'reviews': [], 'comments': [], 'check_runs': []})` instead of raising; bot-only evidence caused `required_unobserved()` to return `['augment_app_slug']` despite requirements allowing `augment_app_slug: <observed-or-null>`. |

## Summary
- Checks passed: 4 / 7
- Checks failed: 3
- Critical issues: 4
- Important issues: 2
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization=false)
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 0 | Glob: 0 | Bash: 9 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- UNCHECKED items: none
- UNVERIFIABLE items: none

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py:313-325`; `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:61`; `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:90` | Fabricated/unimplemented command surface: code and docs emit `superclaude reflect contract-status [--validate] --repo --pr`, but `rg` found no `contract-status` Click command; fresh read of `cli/reflect/commands.py:47-118` shows only the `reflect` group and `run` subcommand start. This violates requirements §10 and design §10.3 recommendation B1 unless the command is implemented. | Implement `superclaude reflect contract-status [--validate] --repo --pr` in the reflect CLI and wire it to `contract_setup.diagnose()` / validation, or change all emitted next-command strings/docs to an actually implemented command. |
| 2 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py:54-97` | `load_evidence()` does not raise when no payload exists. It fabricates an empty `combined_payload` with empty review/comment/check_run lists, making `combined_payload` truthy and bypassing the `if not present_surfaces and not combined_payload` guard. Runtime probe returned a bundle for an empty temp directory. This contradicts design §4 facade contract and requirements §6.1/§7 Evidence. | Track whether any JSON payload file existed before synthesizing combined payload. Raise `FileNotFoundError` when no `combined-payload.json` and no surface JSON files are present. Add regression test for empty probe dir. |
| 3 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/candidate.py:18-26`, `:48-57` | `MUST_OBSERVE_FIELDS` requires `augment_app_slug` independently. Requirements §5 says `augment_app_slug: <observed-or-null>`, while §6 must-never-guess requires `augment_bot_login / app identity` rather than both. Runtime probe with observed `augment_bot_login` and no app slug returned `['augment_app_slug']`, blocking a bot-login-backed lock that requirements allow. | Change required identity logic to require at least one observed Augment identity (`augment_bot_login` or `augment_app_slug`) and allow `augment_app_slug=None` when bot login is observed. Add test for bot-only evidence. |
| 4 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py:89-95`; `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py:46`, `:129` | Invalid `decline_validation` value. Requirements §5 metadata permits `passed|not_exercised|failed`; design §3.5 says `"passed" | "not_exercised" | "failed"`. Implementation emits `"exercised"` when classifier result is declined, and writer persists that invalid value. | Replace `exercised` with `passed` for exercised-and-successful decline validation; reserve `failed` for exercised-but-wrong behavior; keep `not_exercised` when no decline sample exists. Add enum assertion test. |
| 5 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py:120-130` | Locked-contract metadata omits required provenance fields `generated_at` and `validation_report`, both required by merged requirements §5 and design §9. It therefore writes an incomplete lock artifact while claiming `generated_by` provenance. | Add ISO-8601 `generated_at` and a `validation_report` path to lock metadata. Ensure `write_lock()` receives or derives the report path from `write_report()` output. |
| 6 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py:153-158` | `LockGate.report_written` does not verify a report was written. It passes when `report.passed` and `report.evidence_sha256` are truthy, even if no `validation-report.yaml` exists. This contradicts safe-locking policy requirement §6.10 and design §7 check 10: validation report exists/references evidence hash. | Make `ValidationReport` carry `validation_report_path` or pass report path to `LockGate.evaluate()`, then require the file exists and contains the expected evidence hash. Add negative test where report object exists but no file was written. |

## Actions Taken
- No source fixes applied because `fix_authorization=false`.
- Wrote this QA report to the requested output path.

## Recommendations
- Do not proceed to Phase 3 until all CRITICAL and IMPORTANT findings are corrected.
- Prioritize implementing or removing the `superclaude reflect contract-status` surface first, because it is user-facing and currently emitted as a next safe step.
- Add regression tests for every finding above; especially empty evidence, decline enum values, bot-only identity evidence, missing metadata, and report-written gate behavior.

## QA Complete
