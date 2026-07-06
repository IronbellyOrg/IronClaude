# QA Report — Research Gate

**Topic:** OQ-1 Opt-2a integrity Signal B PASS_RECOVERED exemption
**Date:** 2026-06-04
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

[PARTITION NOTE: Cross-file checks limited to assigned subset: 01-integrity-signalb-edit.md, 02-test-surface.md, 03-template-pr-discipline.md. Full cross-file verification requires merging all partition reports. Partition N/M was not provided in the spawn prompt.]

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | FAIL | Read all three assigned files. All declare Complete, but `02-test-surface.md` has no `## Summary` heading; `grep -R "^## Summary\|^Status:"` found Summary only in 01 and 03. |
| 2 | Evidence density | PASS | Independently verified dense core claims via `git show origin/master`: integrity Signal B lines 127-131, verdict line 150, recovered test lines 142-215, classifier lines 547-593, models lines 37-58, executor lines 997-1011 and 2321-2387. |
| 3 | Scope coverage | FAIL | Read `research-notes.md` EXISTING_FILES. Assigned research covers `integrity.py`, `executor.py`, `rerun_tasks.py`, `tests/sprint/test_resume.py`, template/CLAUDE discipline, but does not explicitly discuss `src/superclaude/cli/sprint/models.py` `TaskStatus.PASS_RECOVERED` + `is_success`, despite it being a listed key file. I verified the missing source separately on origin/master at models.py lines 46, 50, 57-58. |
| 4 | Documentation cross-validation | FAIL | `grep -R` found zero `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags in assigned research, despite doc/template/CLAUDE/base-selection claims in 01 and 03. I spot-verified several claims from local source, but the research files do not carry required tags. |
| 5 | Contradiction resolution | PASS | No unresolved contradiction found among assigned files. 01 and 02 agree current Signal B only accepts `TaskStatus.PASS`, and 02 correctly corrects the vacuous PASS_TRANSCRIPT test issue. |
| 6 | Gap severity | PASS | No `Gaps and Questions` sections in assigned research files. `research-notes.md` gaps for test shape, `derived_status`, and exact Signal B line numbers are addressed by the assigned files, except the models.py scope documentation gap recorded in check 3. |
| 7 | Depth appropriateness | PASS | Quick-tier question is answered: exact origin/master Signal B block, Opt-2a guarded edit shape, RED/GREEN test correction, classifier non-edit constraint, derived_status field, and validation/PR discipline are all covered. |
| 8 | Integration point coverage | PASS | Verified integration points across resume integrity, rerun classifier, executor PASS_RECOVERED source, BoundaryTask report field, tests, and PR/task validation process. |
| 9 | Pattern documentation | PASS | Research documents test conventions (`tmp_path`, fixture helpers, pytest classes), task-template conventions (B2/A3/I15/I16/M1), validation commands, worktree/fork PR constraints, and `.claude/` staging rule. |
| 10 | Incremental writing compliance | PASS | Assigned files show multiple independently sourced sections with concrete extracted blocks and corrections (notably 02's RED→GREEN correction). No one-shot data-loss signature severe enough to block was found. |

## Zero-Trust Source Verification Highlights

- Signal B on `origin/master:src/superclaude/cli/sprint/resume/integrity.py` is exactly:

```python
        derived = _classify_transcript(transcript)
        lc.derived_status = derived
        signal_b_pass = derived is TaskStatus.PASS
```

- The verdict on master is exactly `validated = signal_a_pass and signal_b_pass and artifacts_ok`, so a persisted `PASS_RECOVERED` last-completed with a recovered transcript currently fails via Signal B unless the transcript is an artificial clean PASS.
- I verified `tests/sprint/test_resume.py:test_resume_pass_recovered_counts_as_completed` currently writes `PASS_TRANSCRIPT` for T03.01, and extracted `PASS_TRANSCRIPT` as a success result with 42 output tokens. Executing the master classifier against it returned `TaskStatus.PASS`; therefore a naive `assert report.validated_last is True` would already pass on master and would not be a RED test.
- I verified researcher 2's correction: a transcript with `error_during_execution` plus `api_retry` classifies as `TaskStatus.FAIL_RECOVERABLE`, and a no-result partial transcript classifies as `TaskStatus.INCOMPLETE`. Changing T03.01 to the recovered/FAIL_RECOVERABLE shape makes `validated_last is True` RED pre-Opt-2a and GREEN post-Opt-2a, provided the source edit is PASS_RECOVERED-guarded.
- The proposed Opt-2a source edit in 01 is None-safe and scoped: only `lc.persisted_status is TaskStatus.PASS_RECOVERED` bypasses clean-PASS re-derivation; ordinary PASS remains in the `_classify_transcript` branch with `derived is not None and derived.is_success`; `lc.derived_status` is set in both branches.
- `_classify_transcript` was verified in `origin/master:src/superclaude/cli/sprint/rerun_tasks.py` and should remain untouched because `discover_failed_tasks_from_transcripts` consumes it.
- `BoundaryTask.derived_status` exists on master in `src/superclaude/cli/sprint/resume/models.py`.
- Validation discipline in 03 correctly forbids `uv run python -m py_compile`; it recommends `uv run python -c "import py_compile; ..."`, pytest, fork PR creation with `--repo IronbellyOrg/IronClaude`, and branch/worktree off `origin/master`.

## Summary
- Checks passed: 7 / 10
- Checks failed: 3
- Critical issues: 0
- Important issues: 2
- Minor issues: 1
- Issues fixed in-place: 0 (fix_authorization=false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `research/02-test-surface.md` | Missing required Summary section. File has `Status: Complete` but no `## Summary`, violating research-gate file inventory requirements. | Add a concise `## Summary` section covering the existing PASS_TRANSCRIPT vacuity, recovered/FAIL_RECOVERABLE RED→GREEN test shape, missing-artifact negative guard, ordinary-PASS non-overbroad guard, and validation command. |
| 2 | IMPORTANT | `research/01-integrity-signalb-edit.md`, `research/03-template-pr-discipline.md` | Documentation/spec/template/CLAUDE-sourced claims are not tagged `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`. `grep -R` found none of the required tags anywhere in assigned research. | Add validation tags to every doc-sourced claim. For local-code/local-doc claims already source-checked, use `[CODE-VERIFIED]` with the cited file/line evidence. Use `[UNVERIFIED]` only where no code/source verification was possible. |
| 3 | IMPORTANT | Assigned research vs `research-notes.md:17-22` | Scope coverage gap: `research-notes.md` lists `src/superclaude/cli/sprint/models.py` as a key file for `TaskStatus.PASS_RECOVERED` and `is_success`, but the assigned research does not explicitly discuss or cite this file. I independently verified master has `TaskStatus.PASS_RECOVERED` and `TaskStatus.is_success` includes it. | Add a short subsection to `01-integrity-signalb-edit.md` verifying `origin/master:src/superclaude/cli/sprint/models.py` `TaskStatus.PASS_RECOVERED` and `is_success` semantics, then connect that evidence to Signal A and the proposed PASS_RECOVERED-only guard. |

## Actions Taken
- No in-place fixes performed because `fix_authorization=false`.
- Wrote this QA report at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-OQ1-SIGNALB/qa/qa-research-gate-report.md`.

## Confidence and Tool Engagement
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 10 | Grep: 2 via Bash | Glob/find: 2 via Bash | Bash: 11 | Tavily: 0 | Web fallback: 0
- **Unchecked items:** None.
- **Unverifiable items:** None.

## Recommendations
- Resolve all three findings before synthesis/task assembly. Most important: add the doc-claim validation tags and close the `models.py` scope gap.
- Preserve researcher 2's corrected RED→GREEN plan; do not implement a vacuous `validated_last` assertion while retaining `PASS_TRANSCRIPT`.
- Keep source implementation localized to `integrity.py`; do not edit `_classify_transcript`.

## QA Complete
