# Task-integrity QA consolidation — CI doctor task

**VERDICT: PASS (fix-cycle 2).** Initial report-only agents found structural defects; a single authorized fix pass and independent verification resolved them. See `qa-task-fix-round.md` and `qa-task-fix-verification.md`. No workflow or task execution occurred.

## Items Reviewed
| Check | Final verdict | Evidence |
|---|---|---|
| Task scope, one-workflow-only, no real-HOME install, no push | PASS | Both initial agents; unchanged by fix rounds |
| Isolated install→doctor verification exists in items | PASS | Both initial agents; unchanged by fix rounds |
| Frontmatter PRE sign-off | PASS | `qa-task-fix-verification.md` cycle 2: no driving CI spec, skipped/no-spec with run_id n/a |
| POST reflection runner full prompt, diff-file input, TCS/depth, disk gate | PASS | `qa-task-fix-verification.md` cycle 2: no contradictory --spec, full tier wave gate |
| Per-item Verify: and code context evidence | PASS | `qa-task-fix-round.md`: eight items bound to file:line and Verify prefixes |

## Consolidated fixes for ONE authorized fix agent

1. **Correct wrong SPEC metadata upstream:** BUILD-REQUEST.md WHY now clarifies the driving document is the CI diagnosis REPORT, not a CI feature spec; ccsession-native-install.md FR-1/FR-4 is a related contract only. Accordingly set task frontmatter `spec_path: ""`, `reflect_pre.verdict: skipped`, `skip_reason: no-spec`, `coverage_pct: null`, `report: null`; with no driving spec the A.10.7 mandatory-run/depth/tcs branch does not apply. Never fabricate a PRE report or TCS. Keep feature spec under related_docs and item evidence.
2. **Replace abbreviated Step 4.2 with the COMPLETE dedicated subagent skill-mode runner prompt from the task-builder skill Rule 20**, with explicit Skill invocation, tier-appropriate grounding/calibration/merge/evidence validator, `RUN_INCOMPLETE`, waves attestation, executor-side on-disk artifact verification, 2 bounded re-runs/fallback, no auto-silent PASS. The workflow change is deliberately uncommitted, so `--diff` MUST use the existing `workflow.diff` file from Step 4.1 (reflect supports diff paths); `BASE..HEAD` would audit the wrong artifact. Pass `--no-promote` so Step 4.3 can still read the to-do task file; do not stage/commit. Document these safety deviations from the stock Rule 20 placeholders explicitly inside Step 4.2, not as a hand-rolled audit.
3. **Apply `Verify:` prefix and source `file:line` Context evidence** to every checkbox item, including `doctor-check` workflow lines 195-219, CLI install main.py:180-198, doctor.py:52-103, test_update_command.py:113-151; no guessed citations.
4. Preserve one-workflow-step change, isolated tmp-HOME validation, no test/doctor changes unless necessary, and no task execution, commit, push or PR action during task-file repair. Do not invent remote CI success.

After fixes, the task file needs another QA verification; do not claim these defects resolved until re-read.
