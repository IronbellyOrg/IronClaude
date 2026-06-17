# IronbellyOrg/IronClaude Augment Open-PR Audit — 2026-06-12

## Scope and preflight

- Repository root: `/config/workspace/IronClaude`
- Target repository: `IronbellyOrg/IronClaude`
- Preflight status: ok
- `pr-submit` available: true
- Detection contract locked: true
- Deduplication rule: same PR + same Augment critique + same file/line is one finding.

## Open PR inventory

| PR | Title | Branch | Base | URL |
|---:|---|---|---|---|
| 174 | feat(pr-submit): PR-review auto-remediation monitor + V1.1 re-trigger/fallback | `feat/pr-submit-monitor-v11` | `master` | https://github.com/IronbellyOrg/IronClaude/pull/174 |
| 173 | feat(troubleshoot): Pipeline Hardening Closure mode (H0-H5 + waiver/no-re-greening latch) | `feat/troubleshoot-pipeline-hardening` | `master` | https://github.com/IronbellyOrg/IronClaude/pull/173 |
| 169 | fix(prd): two brittle-gate false-negatives that halt the heavyweight pipeline (verdict regex + assembly content-source) | `fix/prd-verdict-assembly-gates` | `master` | https://github.com/IronbellyOrg/IronClaude/pull/169 |
| 167 | fix(prd): tolerate decorated verdict lines in _check_verdict_field | `fix/prd-verdict-field-detection` | `master` | https://github.com/IronbellyOrg/IronClaude/pull/167 |

## Per-PR finding table

| PR | Branch | Status | File / line | Source | Deduped finding |
|---:|---|---|---|---|---|
| 174 | `feat/pr-submit-monitor-v11` | none found | N/A | N/A | No Augment findings were reported by discovery. |
| 173 | `feat/troubleshoot-pipeline-hardening` | validated_open | Entire PR / N/A | https://github.com/IronbellyOrg/IronClaude/pull/173#issuecomment-4691386968 | Augment refused review because the PR is too large. Current PR head `b9378c72e2d5acc12607316b10ef377110f7c5a3` still has 162 changed files, 18,184 additions, 11 deletions, and a 1,926,937-character diff, exceeding Augment's stated 300,000-character review limit. |
| 169 | `fix/prd-verdict-assembly-gates` | validated_open | `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py:379` | https://github.com/IronbellyOrg/IronClaude/pull/169#discussion_r3403275968 | The PR head still uses the broad exclusion `if match.name.upper().startswith("TASK-"):` when scanning candidate PRD markdown files. This can incorrectly skip legitimate assembled PRDs for product slugs beginning with `task-`, such as `task-tracker-prd.md`, rather than only excluding the intended `TASK-PRD-*.md` task-file pattern. |
| 167 | `fix/prd-verdict-field-detection` | validated_open | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:47` | https://github.com/IronbellyOrg/IronClaude/pull/167#discussion_r3400336435 | The markdown verdict regex still uses `[Vv]erdict` without `re.IGNORECASE`, despite adjacent comments claiming case-insensitive key handling. It accepts `Verdict: PASS` but rejects `VERDICT: PASS`. |
| 167 | `fix/prd-verdict-field-detection` | validated_open | `/config/workspace/IronClaude/src/superclaude/cli/prd/gates.py:61` | https://github.com/IronbellyOrg/IronClaude/pull/167#discussion_r3400336436 | The markdown verdict regex still lacks a trailing boundary after `(PASS|FAIL)`, so malformed values with valid prefixes are accepted, including `Verdict: FAILURE` as `FAIL` and `Verdict: PASSING` as `PASS`. |

## Counts by status

| Status | Count |
|---|---:|
| remediated | 0 |
| validated_open | 4 |
| discarded_stale | 0 |
| discarded_false_positive | 0 |
| needs_human_decision | 0 |

## Actionable PRs

| PR | Branch | Validated open findings | URL |
|---:|---|---:|---|
| 173 | `feat/troubleshoot-pipeline-hardening` | 1 | https://github.com/IronbellyOrg/IronClaude/pull/173 |
| 169 | `fix/prd-verdict-assembly-gates` | 1 | https://github.com/IronbellyOrg/IronClaude/pull/169 |
| 167 | `fix/prd-verdict-field-detection` | 2 | https://github.com/IronbellyOrg/IronClaude/pull/167 |

## Blocked / human decision

No preflight blockers and no findings classified as `needs_human_decision`.
