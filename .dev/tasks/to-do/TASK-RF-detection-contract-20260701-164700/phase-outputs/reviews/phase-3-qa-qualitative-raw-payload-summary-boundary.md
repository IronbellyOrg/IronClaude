# QA Report — Raw Payload Summary Boundary

**Topic:** Detection contract readiness/status payload boundary
**Date:** 2026-07-02
**Phase:** synthesis-gate-equivalent / task-integrity
**Lens:** raw-payload-summary-boundary
**Fix authorization:** false

---

VERDICT: FAIL

## Scope

Reviewed only the assigned files:

- `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`
- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py`
- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

## Checklist Verdicts

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No doc example or status/summary shape includes raw GitHub payload bodies, review bodies, comment bodies, or check-run output bodies. | FAIL | `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md` contains a doc example naming `reviews[].body`, `comments[].body`, and `check_run.output` as default findings-locus paths. The requested verdict rule explicitly fails on any body-field example. |
| 2 | Readiness output shows only status, paths, hashes, counts, blockers, next commands, validation report paths, and summary metadata. | PASS | `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py` `_render_contract_status()` prints state, override booleans, checked paths, evidence hash/path, validation report/result, blocker count/list, next command, validation report written path, validation summary, and validation errors only. |
| 3 | Omitted surfaces are described distinctly from present/validated surfaces. | PASS | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py` tracks `surfaces` and `omitted_surfaces` separately; `summary()` renders both separately. `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` writes `validated_surfaces` and `omitted_surfaces` as distinct report fields. |
| 4 | Validation summaries and evidence summaries do not serialize `combined_payload`, `reviews[].body`, `comments[].body`, or `check_run.output` raw text. | PASS | `EvidenceBundle.summary()` in `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py` renders probe dir, repo, PR number, capture time, surfaces, omitted surfaces, counts, SHA, pagination, and cross-PR shape-only flag. `ValidationReport.summary()` in `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py` renders result, classifier result, expected result, counts, evidence SHA, validated surfaces, decline validation, and blocker count. Neither serializes raw payload text. |
| 5 | Reflect/pr-submit docs tell operators summaries should not dump raw payload bodies. | PASS | `/config/workspace/IronClaude/src/superclaude/commands/reflect.md` states the readiness path must not dump raw GitHub payload bodies and reports only status/paths/hashes/counts/blockers. `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md` states `contract-status` reports only readiness metadata and must not print raw GitHub payload bodies. `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md` states normal summaries should display status, paths, hashes, counts, and blockers, not full raw payload bodies. |
| 6 | Any validation report summary wording remains metadata-only and does not expose raw evidence bodies. | PASS | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` writes `validation-summary.md` from `report.summary()`, which is metadata-only; `validation-report.yaml` includes result/classifier metadata, evidence hash, repo/PR/captured_at, validated/omitted surfaces, blockers, checks, and negative controls, but not `combined_payload` or raw GitHub evidence bodies. |

## Findings

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md` §4, question 9 | The requirements doc gives body-bearing findings-locus defaults as `reviews[].body`, `comments[].body`, and `check_run.output`. Even though these are field paths rather than literal payload contents, the gate's PASS/FAIL rule explicitly fails on any body-field example, and this wording normalizes body-field exposure in operator-facing design material. | Replace the body-bearing path examples with redacted/abstract labels such as `<validated-review-finding-locus>`, `<validated-comment-finding-locus>`, and `<validated-check-run-finding-locus>`, or explicitly state that these are internal classifier paths never printed in readiness/status summaries. Prefer adding a note that normal summaries may report only path-resolution status/counts, not the body-bearing paths themselves. |

## Evidence Bullets

- Read `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`: the detection-contract readiness bypass documents `superclaude reflect contract-status` and says it prints readiness/blockers/checked paths/hashes/counts plus next safe command and must not dump raw GitHub payload bodies.
- Read `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`: the missing-contract halt is documented as readiness state, checked paths, blockers, approved next safe readiness command, and no monitor/PR mutation. No raw evidence payload dump appears in that halt wording.
- Read `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md`: §2.1 explicitly routes detection-contract readiness to the sibling CLI and says it reports only readiness state, blockers, checked paths, hashes, counts, and next command; no raw GitHub payload bodies.
- Read `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`: Wave 1 missing-contract halt calls diagnosis helpers and prints structured readiness state, checked paths, blockers, next safe command, and the no-side-effect guarantee.
- Read `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py`: `_render_contract_status()` prints metadata-only readiness fields and indents `report.summary()` output; no direct print of `combined_payload`, review/comment bodies, or check-run output.
- Read `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/evidence.py`: `EvidenceBundle.summary()` is metadata-only and separates `surfaces` from `omitted_surfaces`.
- Read `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/validation.py`: `ValidationReport.summary()` is metadata-only and reports `validated_surfaces`, counts, SHA, and blocker count. The classifier consumes `evidence.combined_payload`, but summaries do not serialize it.
- Read `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py`: `write_report()` writes a YAML report with metadata/check detail fields plus a summary file from `report.summary()`; it does not include `combined_payload`.
- Read `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/diagnosis.py`: `Diagnosis.summary()` and `render_pr_submit_missing_contract_halt()` render state, paths, hashes/report/result, blockers, and next command only.
- Read `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md`: it contains the failing body-field example in §4 question 9, while also correctly stating elsewhere that normal summaries should not dump raw payload bodies.

## Confidence and Tool Engagement

- Confidence: Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 14 | Grep/Bash: 6 | Glob: 0 | Bash: 6
- Unchecked items: none.
- Unverifiable items: none.

## Actions Taken

None. `fix_authorization: false`; no source files were modified.

## Recommendation

Resolve Finding 1 before treating the raw-payload summary boundary as passed. The implementation/status surfaces look metadata-only, but the requirements artifact still contains a body-field example that violates the explicit gate rule.

## QA Complete
