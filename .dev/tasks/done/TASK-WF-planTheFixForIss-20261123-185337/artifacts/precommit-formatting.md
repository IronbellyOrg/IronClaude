# QA Report: Evidence Formatting Corrections

**Topic:** Issue 501 evidence formatting and exact-file exceptions
**Date:** 2026-11-23
**Phase:** precommit-formatting
**Fix cycle:** 1

---

## Overall Verdict: PASS

The two authored-note formatting mistakes are corrected. Fourteen specific captures retain justified formatting-only exceptions. Applicable configured checks pass without broadening exclusions to other files or issues; safety and syntax checks remain active. A fresh independent review found no defects. Git's separate unfiltered whitespace check still reports captured whitespace, as explicitly recorded below.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Regression before/after | PASS | New test file: 14 failed and 48 passed before exclusion changes; all 62 passed afterward. |
| 2 | Bug and formatting regressions together | PASS | `uv run --offline pytest tests/test_precommit_evidence_exclusions.py tests/swarm/test_commands_run.py tests/swarm/test_bundled_lenses.py tests/swarm/test_lens_defaults.py tests/swarm/test_e2e_user_guide.py tests/swarm/test_bare_review_parity.py tests/swarm/test_swarm_run_inputs.py tests/swarm/test_resume_crash_recovery.py tests/swarm/test_imm5_status.py -q`: 271 passed in 2.42s. |
| 3 | Applicable formatting hooks | PASS | Actual per-hook exclusions applied: trailing-whitespace 51 selected files; end-of-file-fixer 145; mixed-line-ending 148; yamllint 6. Mutating hooks ran only on copies. Python Ruff 0.15.20 lint and format checks passed for five selected Python files. |
| 4 | Syntax and file safety | PASS | YAML syntax 10 files, JSON syntax 16, JSONL validity, merge conflicts 148 files, private-key checks 148 files and maximum file size passed. |
| 5 | Secret scan | PASS | detect-secrets 1.4.0 with unchanged baseline, all 148 selected files, no new candidates; network verification disabled and no secret values printed. |
| 6 | Configuration scope | PASS | Parsed configuration comparison finds changes only to three `exclude` fields. Commands, arguments, versions and security/syntax filters unchanged. New tests prove nearby files and other issues are not exempted. |
| 7 | Evidence preservation and plan pins | PASS | Exactly two newline-only edits out of the original 145 delivery files; other 143 byte-identical. Approved plan/source pins match. Hashes and chronology below. |
| 8 | Independent review | PASS | A fresh reader inspected the five follow-up paths and both baselines, independently ran the 62-test file, rehashed all 145 originals, compared note edits with original index bytes, checked all capture classifications and parsed configuration equality. Six review checks passed with zero blocking or minor findings. Scope excludes original bug re-review and future staging. Full local report retained at `/tmp/issue-501-formatting-independent-review.md`; its substantive outcome and scope are recorded here for future readers. |
| 9 | Final delivery reconciliation | PASS | Exactly 148 staged paths match the extended delivery manifest, with staged bytes matching working files and no remaining unstaged tracked changes. Original HEAD unchanged; no commit or push. Source/config/test/doc-only Git whitespace check passed. Unfiltered Git whitespace check exited 2 with 81 warning locations, all within preserved evidence. |

## Summary
- Checks passed: 9 / 9 scoped checks above; checks failed: 0.
- Blocking findings: 0; minor findings from the fresh independent review: 0.
- Formatting mistakes corrected in-place: 2 authored notes, terminal blank lines only.
- Captures preserved with newly justified exact-file exceptions: 14 (7 whitespace, 3 final-newline, 4 YAML-style). No directory-wide exception.
- Additional checks: Markdown lint 0.38.0 passed for seven selected documents; case-conflict checks and `make verify-sync` passed. Additional configured/generic credential-pattern checks found zero candidates across all 148 files.
- Final delivery grows from 145 to 148 files by adding the hook configuration, regression test and this correction record. Existing files changed in this follow-up are only the two named notes.
- The independent review covers the formatting follow-up only. The original implementation's separate review remains historical. Direct pinned-hook execution is not a claim to have exercised the pre-commit runner.
- Git's unfiltered whitespace check still exits 2 because of preserved capture contents. This is disclosed, not treated as a passing Git check.

## Issues Found
The initial failures affected 16 files: two authored notes to correct and fourteen exact captures to preserve. There is no folder-wide exception.

Path aliases (repository-relative):
- A = `.dev/tasks/archive/TASK-WF-planTheFixForIss-20261123-180531`
- D = `.dev/tasks/done/TASK-WF-planTheFixForIss-20261123-185337`
- X = `.dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314`

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR, formatting | A/artifacts/codegraph-grounding.md; X/tier1-observation.md | Authored notes end with two and three newline bytes respectively. | Remove only excess terminal blank lines; retain one newline. Corrected below. |
| 2 | Captured content, not a defect | D/artifacts/plan.diff; D/artifacts/task-1.diff through task-4.diff | Unified patches contain the leading context marker on otherwise blank lines; task-2 also contains captured pytest diagnostic padding. | Preserve all five captures. Exclude exactly these five paths from trailing-whitespace. |
| 3 | Captured content, not a defect | D/artifacts/lens-template.txt; D/artifacts/regression-before.txt | Pytest writes spaces after its diagnostic `E` prefix. | Preserve both captures. Exclude exactly these two paths from trailing-whitespace. |
| 4 | Pinned input snapshot, not an authored-note defect | A/source.md | Byte-exact input has no final newline; its hash is retained in A/artifacts/reflect-pre-20261123181244/artifacts/input-snapshot.yaml:9. | Preserve it. Exclude exactly this path from end-of-file-fixer. |
| 5 | Captured content, not a defect | D/artifacts/repaired-cli/manifest.json; X/stub-run/manifest.json | CLI-generated JSON has no final newline. | Preserve both verbatim captures. Exclude exactly these paths from end-of-file-fixer; retain JSON syntax checks. |
| 6 | Valid captured serialization, not invalid YAML | A/artifacts/reflect-pre-20261123181244/artifacts/input-snapshot.yaml; A/artifacts/reflect-pre-20261123181244/return-contract.yaml; D/artifacts/repaired-cli/return-contract.yaml; X/stub-run/return-contract.yaml | Captured serializers use valid YAML sequence indentation rejected by the style checker. All four pass YAML syntax validation. | Preserve all four. Exclude exactly these paths from yamllint, not check-yaml. |

Existing Markdown exclusions already cover saved reviewer prompts and quoted diff text in re-review.md. They were not expanded. Git's separate whitespace check still reports whitespace inside these captures; it is not a formatting-hook result.

## Actions Taken
The person approved classifying failures, correcting genuine mistakes and justifying only captured-content exceptions. The earlier directory-wide proposal was withdrawn before any repository configuration change.

Only three hook `exclude` fields changed in `.pre-commit-config.yaml`: trailing-whitespace, end-of-file-fixer and yamllint. The new expressions match fourteen exact existing files in this issue's packages. Existing fixture/Markdown exclusions remain. Hook versions, commands, arguments, syntax checks, secret checks and mixed-line-ending are unchanged; a parsed before/after comparison verified that scope.

Only two of the original 145 selected files changed in this follow-up. Both edits remove trailing newline bytes, nothing else:

| File | Before SHA-256 | After SHA-256 | Byte change |
|---|---|---|---|
| A/artifacts/codegraph-grounding.md | `5615ccf659cb1a3e05974a5405e541b5747a526c784589044e631f582af5ad62` | `4a880cf8333d40324515f811d0e6de45b361a4b894528d8a3a80dd0705a9c8e8` | Two terminal newlines become one. |
| X/tier1-observation.md | `cdbce26479a4a7741fc6c647f0b77a71a2bb8fab7b4332db6eead965da62088f` | `7ae4b37d2f598241aeefe2d46fb98f45320e11ff11f05ec5160a27faee61f1d6` | Three terminal newlines become one. |

The other 143 pre-follow-up delivery files, including all fourteen excepted captures, remain byte-identical. The approved completed plan and its source still match their pinned hashes (`b81fd4e0e6676850dd229add73ba83afb8413f520babb9f958e156d9f350a89a` and `fd841c02d1a14066c4ed7df374624feef98384e196476807d222ee1ad2e11539`). The existing corrected review pointer was not edited again.

`transfer-inventory.json` and `transfer-reference-audit.md` remain unchanged historical observations made before these formatting corrections. Their original 87-file reconciliation was 86 byte-identical originals plus one authorized pointer change at that time. After this follow-up, the reconciliation is 84 byte-identical originals, the same authorized pointer change, and the two explicitly recorded terminal-newline normalizations above. Do not interpret the older inventory as a post-correction byte-identity claim.

Regression evidence: `uv run --offline pytest tests/test_precommit_evidence_exclusions.py -q --tb=no` before the configuration edit produced 14 failed and 48 passed. After the edit, the same file produced 62 passed. These tests cover exact capture matches, nearby/other-issue nonmatches, ordinary files and retained safety/syntax coverage. An initial pinned formatter check required formatting the new test; that new authored test is corrected before final validation.

## Recommendations
Keep exceptions exact-file and capture-specific. Newly authored notes should meet formatting rules when created, and newly generated captures receive no automatic exception from this change. Preserve all safety/syntax checks.

An unfiltered `git diff --cached --check` still detects meaningful whitespace inside captured patches, diagnostic output, saved prompts and quoted comparisons. This change does not configure or bypass that Git command, and no clean result for it is claimed. A source/config/test-only whitespace check should pass.

Applicable pinned hook implementations were run directly, not through an installed pre-commit runner. No TOML or shell files are selected, the commit-message hook has no message to validate, and the bare-review-specific mirror hook has no matching changed source. No commit or push is authorized or performed.

## Confidence Gate
- **Confidence:** Verified: 9/9 scoped checks | Unverifiable: 0 within these checks | Unchecked: 0 within these checks | Confidence: 100.0% checked-item coverage, not a probability of correctness.
- **Tool engagement at first complete index reconciliation:** Read: 4 | Bash: 12 | Write: 2 | Edit: 10 | Agent: 1. Subsequent edits complete this record, followed by final secret/byte reconciliation. The independent review records its own tool counts separately.
- Explicit exclusions: no original bug re-review, full repository test suite, downstream comparison, paid/model-backed swarm, upstream repository access, commit-message validation, commit or push. The secret scan is offline detection, not external credential-validity testing. The pre-commit runner itself was not invoked; applicable hook implementations and their configured selection rules were checked directly.

## QA Complete
Completed on 2026-11-23. The scoped formatting follow-up passed its tests, applicable checks and fresh independent review. Exactly 148 intended files are selected for staging, with two documented newline normalizations and preserved capture bytes. The finalized record is restaged and its bytes rechecked along with the delivery set. No commit or push is performed.
