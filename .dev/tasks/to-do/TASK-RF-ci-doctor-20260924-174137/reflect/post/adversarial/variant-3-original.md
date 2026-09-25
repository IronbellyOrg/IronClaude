---
card_id: t1-ci-doctor-post
mode: post
claim_class: static_defect
evidence_class: source_plus_captured_logs
self_reported_confidence: 0.88
---

# Tier 1 reflection card — TASK-RF-ci-doctor POST

## Scope
One unstaged hunk in `.github/workflows/test.yml` inserts `Install native components` (`superclaude install`) between `Install dependencies` and `Run doctor command` in job `doctor-check`. Production doctor/install code is unchanged.

## Tasklist-vs-diff
| Item | Status | Map |
| Step 1.1 | done | task frontmatter/log only |
| Step 2.1 | done | `.github/workflows/test.yml:217-219` |
| Step 3.1 | done | `test-results/install-integration.txt` (8 passed, EXIT=0) |
| Step 3.2 | done | `test-results/isolated-install-doctor.txt` PRE=1, INSTALL=0, POST=0, CONTRACT=PASS |
| Step 3.3 | done | `test-results/workflow-checks.txt` cached quiet, diffs agree, verify-sync=0 |
| Step 4.1 | done | `test-results/workflow.diff` equals `git diff HEAD -- .github/workflows/test.yml` |
| Step 4.2 | in-progress | this POST run |
| Step 4.3 | blocked-on-4.2 | closeout |

`tasklist_completion_pct` over all checklist items = 6/8 = 0.75. Execution items 1.1–4.1 = 1.0. Remaining items are the POST gate and Done closeout.

## Related contract (not `--spec`)
`.dev/specs/ccsession-native-install.md` FR-1 (`superclaude install` wires ccsession) and FR-4 (doctor fail-on-missing). CI step order implements FR-1 then FR-4 on a clean runner. Doctor implementation not modified.

## Deviation candidates
1. **Necessary** — POST `--diff` is a file path (`workflow.diff`), not `{BASE}..HEAD`. Task Step 4.2 + skill `refs/input-resolution.md` allow a diff file; stock git-range would miss the unstaged hunk.
2. **Necessary** — `--no-promote` keeps the to-do path. Task Step 4.2 forbids Wave 7 move before Step 4.3.
3. **Necessary** — workflow change remains uncommitted. Task forbids commit/push without separate authorization.
4. **none** — the YAML hunk itself maps to Step 2.1; doctor command still `superclaude doctor --verbose`; neighboring jobs untouched.

No Regression candidate in the hunk: doctor fail-on-missing is preserved (`isolated-install-doctor.txt` PRE_INSTALL_DOCTOR_EXIT=1 then POST=0).

## Risk
Remote GitHub `doctor-check` is not rerun. Task records that as a follow-up, not this change's acceptance. Reflect live verification triangle skipped (`execute_shell_command` unavailable); captured task-log tests used instead.

## Recommendation
Treat the one-step workflow insert as complete vs Step 2.1. Do not promote. Do not remediate production code. Escalate to Tier 2 because `--depth deep`.
