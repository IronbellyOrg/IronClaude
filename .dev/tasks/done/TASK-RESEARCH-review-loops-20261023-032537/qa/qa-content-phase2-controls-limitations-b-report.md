# QA Report: Controls and Limitations (Partition b of 3)

**Topic:** Phase 2 research screening and two dedicated session cases  
**Date:** 2026-10-23  
**Phase:** phase-gate  
**Lens:** controls-limitations  
**Fix cycle:** Initial review  
**Fix authorization:** false  
**Delivery:** Complete text return. No report file was written.

## Overall Verdict: PASS

**VERDICT: PASS**

No controls-and-limitations defects were found in the assigned targets.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Negative controls remain distinct from repeated repair failures | PASS | Read both screening files completely. Independently extracted actual skill invocations from the two unrelated negative sessions. Their observed commands concern troubleshooting or proposal comparison, not the target planning/execution repair sequence. |
| 2 | Successful one-repair cases remain visible | PASS | The second screening file preserves the comment-correction control. Original session records 1056, 1060 and 1078 independently show a missing criterion, the corrective edit, and a compliant re-review. The later Task 6 verification blocker is kept separate. |
| 3 | Accepted verification gaps are not called repairs | PASS | The documentation case explicitly distinguishes operator acceptance from successful rendering. Original records 430, 443 and 450 show the unchanged rendering blocker; records 506, 510 and 527 show explicit acceptance, preserved unverifiable status, and a final pass with the gap still unmet. |
| 4 | Concurrent writers and related sources constrain independence | PASS | Both screening files distinguish shared-worktree activity, overlapping plans and repeated rounds of one incident. Original session record 580 explicitly says the final review did not run because another plan was rewriting the same files. No predicted failure is counted as an observed verdict. |
| 5 | Modification-time selection does not imply representative sampling or immutable contents | PASS | Read the frozen manifest and source captures. The manifest defines selection by modification time; the first screening file says membership is fixed while live files may grow. The second file dates its stability observation. Neither target uses these observations to estimate general failure rates. |
| 6 | Unknown earlier-miss mechanisms and unavailable history remain bounded | PASS | Both dedicated cases retain explicit evidence limits. The documentation case preserves reviewer reliance on the executor’s baseline account. The planning case explicitly leaves earlier reviewers’ reasons unknown unless a narrower mechanism is visible. Missing historical evidence is not filled with invented psychology. |
| 7 | Historical endpoints and later observations remain separate | PASS | Read the complete planning case, including its separately timed outcome supplement. Independently extracted original record 1084: the review had finished with partial evidence status and a not-ready verdict; a further refactor or acceptance decision was pending, and the implementation command was explicitly not run. |
| 8 | Counterevidence limits claims about introduced defects | PASS | The planning case distinguishes substantial successful repairs, inherited weaknesses, optional hardening, corrected reviewer claims and the dependency-graph defect. The surviving final review independently labels two findings optional and excludes review-matrix bookkeeping from task defects. Proposed repairs are not described as applied changes. |

## Summary

- Checks passed: **8 / 8**
- Checks failed: **0**
- Critical issues: **0**
- Important issues: **0**
- Minor issues: **0**
- Issues fixed in-place: **0**
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 25 | Grep: 0 | Glob: 0 | Bash: 2
- Four Read attempts returned missing-file results; the historical control conclusions were checked through surviving original session records instead.
- No web research was required or performed.

[PARTITION NOTE: Cross-file checks were limited to the assigned subset. Full cross-file verification requires merging all partition reports.]

The confidence calculation covers the eight assigned lens checks. It does not certify every code, hash, chronology or classification claim for other review lenses.

## Checked Scope

Read these four assigned targets completely:

- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/03-session-6f744b87.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-01.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-02.md`

Also read the governing report template, prepared output stub, task acceptance paragraphs for Steps 2.1, 2.2, 2.9 and 2.10, frozen manifest, discovery notes, and relevant preserved screening captures.

## Issues Found

None within the assigned controls-and-limitations lens.

## Actions Taken

- Independently extracted 16 selected primary event records across five original session logs.
- Checked two additional negative sessions’ actual skill invocations within their historical screening boundaries.
- Checked the planning case’s final observed response and surviving final review.
- Made no target edits, report writes, Git operations, test runs, external requests or additional agent launches.

## Verification Limitations and Negative Evidence

Four supporting paths could not be read during this review:

- `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/progress.md`
- `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/to-do/TASK-WF-reviewAndPlanThe-20261022-204721/progress.md`
- `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md`
- `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/source.md`

These failed reads do not establish that the artifacts were absent during the analysts’ earlier observations. This review therefore used surviving original records to check acceptance, review outcomes and observation boundaries; it does not independently certify those packages’ present location or contents.

The surviving planning review was read at:

`/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md`

Historical source unavailability was not converted into a research finding where the relevant conclusion remained independently supported and bounded.

## Self-Audit

**(a) Reliance list: structural PASS items skipped for structural re-check**

- None. No inherited structural-verdict table was supplied. Other reviewers’ conclusions were not treated as independent verification.

**(b) Independent semantic checks**

- **Accepted versus repaired:** A bounded extraction of original documentation-session records 430, 443, 450, 506, 510 and 527 established that the rendering requirement remained unverified through final acceptance.
- **Successful repair versus joined incidents:** Original control-session records 1056, 1060 and 1078 established one successful comment repair. Records 1247 and 1250 established that the later CI-only criterion was a separate blocker.
- **Observed versus predicted failure:** Original overlapping-writer session record 580 explicitly says the final review was not run.
- **Planning versus implementation:** Original planning-session record 1084 explicitly labels the suggested implementation command “not run.” The invocation inventory through the documented endpoint contains planning and review skills, not implementation.
- **Counterevidence retained:** Direct reading of the surviving final review confirmed optional hardening and rejected bookkeeping claims, rather than treating all reported findings as confirmed new defects.

**Factual verification accounting:** Independently checked 20 primary evidence units: 16 selected event records, two negative-session invocation inventories, one final planning response and one surviving final-review artifact. No production-code runtime behavior is independently certified by this lens review.

**Why the clean result is justified:** The review actively tested the main ways this research could overclaim: accepted gaps called fixes, separate tasks joined into failure chains, parallel reviews counted as retries, predictions counted as verdicts, live logs treated as immutable, and later findings assumed to be repair-caused. The assigned targets preserve those distinctions.

## Recommendations

Preserve the observation cutoffs, successful-repair controls, accepted gaps and source-family boundaries when merging the partition reports. This PASS applies only to the assigned lens and files, not the full Phase 2 gate.

| Status | Result |
|---|---|
| DONE | Completed the assigned controls-and-limitations review with zero findings. |
| NEXT | Parent persists this exact report to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-content-phase2-controls-limitations-b-report.md` and verifies the disk artifact before counting delivery complete. |

## QA Complete

Review complete. Text returned for parent persistence; no disk-delivery or full-gate completion claim is made.