| Status | Result |
|---|---|
| DONE | Scored the card on the five reflect-rubric dimensions. Calibrated confidence is 0.83; the card reported 0.72 for itself. Verdict: ESCALATE (low_confidence). |
| DONE | Checked 24 groups of the card's file:line citations in the repository. All matched, none were wrong, and the ones I couldn't check are listed below. |
| DONE | Sent the full report to team-lead by message. It is also below. |
| NEXT | Orchestrator saves this report and acts on the ESCALATE verdict. |

# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/t1-card.md
**Rubric**: /home/coder/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 1
**Timestamp**: 2026-11-08T04:45:00Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|---|---|---|
| Citation grounding | 0.90 | Nearly every C-row and A-row has file:line anchors, and all 24 groups I checked matched. Deductions: C3b's evidence column is empty (its anchors are only in the location column). A1, A6, A7 and A10 are marked [INFERRED]. I could not check the tasklist, spec and decision-file line numbers. C4c's "unreachable" claim is only partly traced: the path through `_reclaim` at cycle.py:914 is not shown. |
| Coverage completeness | 0.75 | In the 0.60-0.84 band (partial coverage with an explicit list of gaps). The card re-checks 11 requirement line ranges plus IE-01 to IE-05 (card lines 64-77) and lists what it did not re-check (lines 79-83). It gives no coverage percentage and does not go through every spec requirement or tasklist item. Entry-point reachability is assessed (C9, DEGRADE). |
| Deviation-classification clarity | 0.65 | In the 0.40-0.69 band. Every row has a rationale, but none of the labels come from the rubric's four categories (Aligned, Refinement, Drift, Regression). The C-register uses "Authorized expansion", "Necessary deviation", "Authorized" and "Grounding Gap". The A-table uses one-off labels such as "Fail-open on skew", "Design limit", "Gap", "Dead code", "Hardening", "Operational trap" and "Reporting regression". Two rows hedge between categories: C4c ("Authorized omission + Drift") and C6 ("Drift (alt reading: Regression of NFR-014)"). |
| Risk surface coverage | 0.95 | Meets the 1.00 description in substance. It has a risk register R1-R6 with blast radius (lines 115-121), seven untested invariants (lines 122-129), likely regressions (A3, and C6's alternative reading) and a fail-open case (A1). Small deduction: R1 (real gh and Orca reply formats) and A6 rest on inference, and the only next evidence named is "the live test". |
| Recommendation actionability | 0.90 | All 15 recommendations name a target file and a check, either a command or a test (lines 133-147). The weaker ones: #13 is partly advice ("Consider start_new_session=True"), #11 names no new test case, #2 is checked only by a grep, and #5, #8 and #15 depend on owner decisions (the card says so). |

## Confidence

- **Self-reported (in card)**: 0.72. Read, but NOT used as an input.
- **Calibrated (this report)**: 0.83
- **Formula applied**: the reflect rubric's average of the five scores: (0.90 + 0.75 + 0.65 + 0.95 + 0.90) / 5 = 4.15 / 5 = 0.83. No other limits applied.
- **Delta**: +0.11. The card rates itself too low. Its citations held up and its risk and recommendation sections are strong. What holds the score down is that its category labels are not the rubric's and two rows hedge, and that its coverage comes from spot checks, not a full mapping.

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: rubric line 80, "`C < 0.85` is an automatic ESCALATE." (0.83 < 0.85). The reflect rubric has no § Escalation Decision section, so this threshold line is the rule that applies. `--depth deep` points the same way.
- **Execution restriction**: none. `--no-escalate` is false and depth is not quick.

## Notes

- **Rubric used**: the reflect rubric (five dimensions, simple average). I skipped the troubleshoot-only parts as instructed: the runtime-check cross-table, the structural assertion rules and the Stage-2 gated-minimum trace. No assertions_path was given, so there is no Structural assertions section.
- **Claim class**: the card's frontmatter says claim_class runtime_behavior, evidence_class source_static, verdict_direction AFFIRM. That is consistent: the card ran nothing and says so (frontmatter line 3). For reference, the troubleshoot formula's 0.84 cap for AFFIRM cards would not change 0.83.
- **Checked and matched (24 citation groups)**:
  1. record.py:23-29 imports ApprovalResult plus four functions from predicates.
  2. record.py:182-183 has the inline reason and calls valid_operation_id.
  3. predicates.py:20, 54, 57-67.
  4. launch.py:30, 33, 36, 84-102, 119-132.
  5. cycle.py:635-641, the re-approved branch.
  6. cycle.py:685-690: `_locked_body` catches only `_Stop`.
  7. cycle.py:693, 1010-1016, 1024-1026, 1031, 1033, 1039-1049, 1052-1062.
  8. audit.py:55-64 and 81-101.
  9. audit.py:393-397, a wall-clock read.
  10. cli.py:121-129 and cli.py:319.
  11. record.py:423 compared with 425-431 (`lexists` against `os.stat`; only FileNotFoundError is caught).
  12. record.py:689-703, plus design lines 500 and 505.
  13. Design lines 114 (`once` has no exit 1), 239, 242 and 362.
  14. runner.py:15, 35, 89-129.
  15. test_module_boundaries.py:15-22, 57-61, 72-75. Its docstring says "three functions and one type", but record imports four functions, which backs up C1b.
  16. test_launch.py:198-200.
  17. test_cli.py:967 and 1070.
  18. cycle.py:35 (defined; I did not grep for whether it is used).
  19. cycle.py:307-324.
  20. cycle.py:468 and github.py:134 hold the same regex.
  21. test_audit.py:473 and 484.
  22. test_crash_injection.py:327-339.
  23. cycle.py:1225-1230 and 1235-1244.
  24. cycle.py:901-914.
- **Did not match**: nothing of substance. One small point: C4c talks about `_approve`, but the branch at cycle.py:635-641 is in `_issue_line`.
- **Could not check**:
  - Task file lines: 199-975, 332, 847, 883, 907-908, 969, 975, 998, 1046, 1050.
  - spec-final.md lines (it is untracked).
  - Line numbers in 06-gap-fill-decisions.md, and setup.md.
  - github.py:61-65, 175-262, 437-463, 592-702, 828.
  - atomic.py:28-32.
  - record.py:378, 503-525, 538-568, 748.
  - launch.py:251-259, 274, 320-321, 343-355.
  - cycle.py:755-756, 814-815, 1134-1137.
  - Lines in test_cycle.py, test_record.py:739-760, main.py:563-565 and runtime-surface.md:40-42.
  - Every count the card got from grep. I have no grep tool here.
- **Unverifiable remote links**: none. The card cites no URLs.

I edited no files. The citations I could not check (listed above) count against the citation-grounding score only as unconfirmed, not as wrong.
