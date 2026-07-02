# QA Report — Template-Conformance Synthesis Gate Equivalent

**Topic:** Phase 2 detection-contract setup public interface conformance  
**Date:** 2026-07-01  
**Phase:** synthesis-gate-equivalent / task-integrity  
**Lens:** template-conformance  
**Fix cycle:** N/A  
**Fix authorization:** false  

---

## Overall Verdict: FAIL

FAIL on naming/public-interface drift. The package imports and facade exports are stable, and no exported symbol is missing/nonexistent, but the implemented validation dataclasses do not match the design’s public interface exactly.

---

## Confidence

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%  
**Tool engagement:** Read: 17 | Grep: 0 | Glob: 0 | Bash: 3  
**Web research:** Not used; all verification was local source-truth verification.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Module/function/dataclass names match design public interface exactly | FAIL | Read design public interface at `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md:213-296`; inspected implementation with `uv run python` signatures/dataclass fields. Function names/signatures match, but `CheckResult` and `ValidationReport` public fields drift from the design. |
| 2 | Imports are stable under `superclaude.pr_submit.contract_setup` | PASS | Ran `uv run python` imports for `states`, `diagnosis`, `evidence`, `questions`, `candidate`, `validation`, `lockgate`, and `writer`; all returned `OK`. |
| 3 | Facade `__init__.py` exports exactly design-named symbols plus Step 2.10 rendering helper | PASS | Read `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/__init__.py:15-63`; `__all__` includes design-named symbols plus `render_pr_submit_missing_contract_halt`. Runtime `getattr` for every `__all__` entry succeeded. |
| 4 | No symbol is exported that does not exist | PASS | Runtime verification of every `__all__` symbol in `superclaude.pr_submit.contract_setup` succeeded; no `AttributeError` or import failure. |

---

## Summary

- Checks passed: 3 / 4
- Checks failed: 1
- Critical issues: 2
- Important issues: 2
- Minor issues: 0
- Issues fixed in-place: 0

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py:15-22` | `CheckResult` does not match the design public interface. Design requires fields `name`, `passed`, `detail` at `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md:216-220`; implementation exposes `check_id`, `passed`, `message`, `severity`. This is naming/public-interface drift. | Change `CheckResult` to the design field names exactly: `name: str`, `passed: bool`, `detail: str`. If severity is still needed internally, keep it out of the public design surface or update the design before implementation. Update all call sites in `validation.py`, `lockgate.py`, and `writer.py`. |
| 2 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py:25-36` | `ValidationReport` does not match the design public interface. Design requires `result`, `classifier_result`, `expected_result`, `checks`, `negative_controls`, `decline_validation`, `evidence_sha256`, `validated_surfaces`, and `blockers` at `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md:222-232`. Implementation exposes `passed`, `checks`, `classifier_result`, `expected_result`, `evidence_sha256`, `omitted_surfaces`, `decline_validation`, `cross_pr_shape_only`. Missing design fields: `result`, `negative_controls`, `validated_surfaces`, `blockers`. Extra drift fields: `passed`, `omitted_surfaces`, `cross_pr_shape_only`. | Reshape `ValidationReport` to match the design exactly. Use `result: str` with `"passed" | "failed"` instead of public `passed: bool`; add `negative_controls`, `validated_surfaces`, and `blockers`; remove or internalize `omitted_surfaces` and `cross_pr_shape_only` unless the design is revised. Update `validate_candidate()`, `write_report()`, `LockGate`, and summary rendering accordingly. |
| 3 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py:18-34` | `EvidenceBundle` adds public dataclass fields not present in the design: `omitted_surfaces` and `cross_pr_shape_only`. The design lists `probe_dir`, `repo`, `pr_number`, `captured_at`, `surfaces`, `reviews`, `comments`, `check_runs`, `combined_payload`, `sha256`, and `pagination_complete` only. Since the checklist requires exact design public interface conformance, these extra public fields are drift. | Either remove these fields from the public dataclass or update the design/source requirements to explicitly include them. If retained only for internal reporting, store them in a non-public internal structure or metadata field that is design-approved. |
| 4 | IMPORTANT | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py:89-109` | `decline_validation` value vocabulary drifts from the design. Design states `"passed" | "not_exercised" | "failed"` at `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md:229`; implementation emits `"exercised"` when classifier result is declined. This is not one of the design-named literals. | Replace `"exercised"` with the design literal `"passed"` when decline evidence validates successfully; keep `"not_exercised"` and add `"failed"` where decline validation fails. |

---

## Positive Findings Verified

- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/__init__.py:15-38` exports all design-relevant public symbols and the rendering helper `render_pr_submit_missing_contract_halt`.
- Runtime import of all exported facade symbols succeeded.
- Runtime import of all assigned package modules under `superclaude.pr_submit.contract_setup` succeeded.
- Public function signatures for `diagnose`, `load_evidence`, `derive_candidate`, `validate_candidate`, `write_report`, and `write_lock` match the design shape at `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md:243-296`.
- `ContractState` values match the nine required UX states.
- `SETUP_QUESTIONS` contains 16 question IDs matching the design’s question sequence.

---

## Actions Taken

No file modifications were made. `fix_authorization: false`.

---

## Recommendations

- Do not proceed as PASS until `validation.py` public dataclasses conform to the design.
- Correct `CheckResult` and `ValidationReport` first; those are blocking CRITICAL naming/export drift defects.
- Decide whether `EvidenceBundle.omitted_surfaces` and `EvidenceBundle.cross_pr_shape_only` are approved public API. If yes, revise the design. If no, remove/internalize them.
- Normalize `decline_validation` to the design literal vocabulary: `"passed" | "not_exercised" | "failed"`.

---

## QA Complete

Verdict: FAIL. All 4 checklist items were verified with local source evidence and runtime import/signature inspection.
