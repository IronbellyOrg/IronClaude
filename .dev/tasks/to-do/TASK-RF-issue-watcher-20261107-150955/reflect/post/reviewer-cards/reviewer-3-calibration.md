| Status | Result |
|---|---|
| DONE | Scored reviewer 3's card against the five-dimension reflect rubric. Calibrated confidence is 0.76, so the verdict is ESCALATE (`low_confidence`). |
| DONE | Checked 35 of the card's citations: 34 match and 1 has the wrong path. The full report was also sent to team-lead by message. |
| NEXT | Save the report below to the calibration output path. |

# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/reviewer-cards/reviewer-3-card.md
**Rubric**: /home/coder/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T04:53:00Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|---|---|---|
| Citation grounding | 0.88 | Nearly every finding has a file:line, and 34 of the 35 I checked match. Points off for three things. Row 11 cites `src/superclaude/main.py:563-565`, which does not exist; the code is at `src/superclaude/cli/main.py:563-565`. Several authorities have no path or line: "deviation register Table 2 row 1", the decision-register (DF) rows, PRE-11, the "Phase 8 log", OQ-21 / DF-29. Row 9's "never read in production" rests on a search made before the context was summarized, and the card says it was not re-run. |
| Coverage completeness | 0.70 | The diff scope is a whole new package, and the card gives no coverage percentage and maps no diff hunks. It audits 18 units (NFR-001 to NFR-014 plus 4 design sections). It also keeps an explicit "Could not fully verify" list: NFR-001 to NFR-013 not checked clause by clause, `github.classify` and `CallBudget` not read, `record.mark_pending` not read. That is the rubric's 0.60-0.84 band: partial coverage with a listed gap register. |
| Deviation-classification clarity | 0.78 | Each of the 11 rows has exactly one category from the right set and a rationale, and the counts add up (6 Drift, 4 Necessary deviation, 1 Authorized expansion). Three weak spots. (a) Row 1 (`cycle_crashed`, Drift) and row 7 (`cycle_complete`, Necessary deviation) are both reason names the executor proposed, and row 1 itself cites design :722 ("used for a crash"), yet the two rows get different categories on thin reasoning. (b) Rows 8 and 10 describe structure that the design allows or forces (design :237-240), so they are closer to aligned than to deviations. (c) Row 6 puts three separate findings under one category. Its part (c) also misses that design 10.2 (`issue-watcher.md:726`) itself says `status` exits 0/1/6. |
| Risk surface coverage | 0.85 | The card raises real structural risks: a `DISABLED` symlink loop crashes `status` (traceback, exit 1 read as "unhealthy" instead of 6); "disabled since" is wrong for a dangling symlink; copied limits have no tests that pin them to the original; the import-boundary test cannot see access through another module's attributes; the retry list drops entries silently; the stderr fallback writes reset lines as `kind: cycle`. It also has a security-hygiene sweep. Points off: no test run or other evidence for possible regressions (Regression 0 is only asserted), and no reasoning on what the eager `main.py` import affects. |
| Recommendation actionability | 0.60 | Only row 10 gives an explicit next action ("do NOT consolidate `_fsync_dir`"). The Drift rows and the 5 correctness gaps point at exact locations but never say whether to fix the code or amend the design. They also give no success criterion, such as catching OSError in `status_command` or adding a test that pins `launch.MAX_ISSUE_NUMBER` to `predicates.MAX_ISSUE_NUMBER`. |

## Formula trace (reflect rubric)

| Step | Value | Notes |
|---|---|---|
| Mean of the five dimensions | 0.762 | (0.88 + 0.70 + 0.78 + 0.85 + 0.60) / 5 = 3.81 / 5 |
| **calibrated** | **0.76** | rounded to 2 decimals; the reflect rubric has no gates or caps |
| spot_check_unverifiable | none | the card cites no remote web addresses |
| structural_flags | skipped | no assertions file was passed, and the reflect rubric has no structural rules |

## Confidence

- **Self-reported (in card)**: none. The card gives no confidence number.
- **Calibrated (this report)**: 0.76.
- **Formula applied**: plain average of the five reflect-rubric dimensions (rubric lines 9-13), as the orchestrator instructed.
- **Delta**: cannot be computed because there is no self-report. The score is pulled down by actionability (0.60) and coverage (0.70), not by weak evidence.

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: "`C < 0.85` is an automatic ESCALATE." (reflection-rubric.md line 80). The reflect rubric has no "Escalation Decision" section, so this is its only rule.
- **Execution restriction**: none. `--no-escalate` is false and the depth is `deep`.

## Spot-check of citations (35 checked)

**Verified (34):**
1. `cli.py:35`
2. `cli.py:123-129` and `:124`
3. `issue-watcher.md:114`
4. `issue-watcher.md:153-164`
5. `issue-watcher.md:718`
6. `issue-watcher.md:722`
7. `issue-watcher-setup.md:318`, `:331`
8. `record.py:23-29` (one absolute import: one type plus four functions)
9. `test_module_boundaries.py:20-21` (the "three functions and one type" miscount is confirmed) and `:57-58`
10. `issue-watcher.md:239`
11. `cycle.py:468` and `github.py:134`: identical pattern
12. `cycle.py:76` and `predicates.py:23`: identical format
13. `audit.py:395-397`, plus the calls without `ts` at `cli.py:79`, `:127`, `:219`
14. `spec-final.md:231`
15. `cli.py:319`
16. `issue-watcher.md:242`
17. `issue-watcher-setup.md:53`
18. `cli.py:84-91`, `:169`, `:314`
19. `issue-watcher.md:115`, `:119`
20. `issue-watcher-setup.md:432`
21. `cycle.py:1134-1137`
22. `issue-watcher.md:157`, `:709`, and `issue-watcher-setup.md:344`
23. `cycle.py:1227`, `:1230`, `launch.py:22`, `issue-watcher.md:240-241`, `:741`
24. `runner.py:35`, `:89`, `:110`, `:120`, `:129`
25. `issue-watcher.md:235`, `:255-262`
26. `record.py:310-315` and `audit.py:110-115`: identical `_fsync_dir`
27. `audit.py:200`, `:203`, `:204-206`, `launch.py:30`, `predicates.py:20`
28. `issue-watcher.md:244`
29. `record.py:423`, `:428-430`, and `cli.py:175` (catches only `StoreError`)
30. `issue-watcher-setup.md:298`, `:302`
31. `cli.py:309-313`, `:311`
32. `cycle.py:1271`, `:1279-1280`, `issue-watcher.md:739`
33. `audit.py:402`, `cli.py:264`, `:266`, `:279`
34. `test_audit.py:473-484`. Also checked from the Notes: `audit.py:106-107`, `:133`, `:150-155` and `cycle.py:666-667`, `:679-683`, `:693-694`.

**Did not match (1):**
- Row 11 cites `src/superclaude/main.py:563-565`, which does not exist. The cited code is at `src/superclaude/cli/main.py:563-565`; the content is right and only the path is wrong.

**Could not check:**
- `github.py:37`, `:75`, `:89`
- `launch.py:90-92`, `:101-102`, `:127-130`, `:184`, `:229`, `:355`
- `record.py:376-378`, `:773-795`, `:863-865`
- Three claims that need a search across the whole repository: the Python 3.10 compatibility sweep, "subprocess only in runner.py", and "duration_s never read in production".
- Authorities cited with no path or line: the deviation register, the DF rows, PRE-11, the Phase 8 log, DF-29 / OQ-21.

## Notes

- I used the reflect rubric (five dimensions, plain average) as instructed. I skipped the troubleshoot-only parts of my agent definition: the runtime-check cross-table, the structural rules C1-C8, the gated minimum and the verdict-direction cap.
- The card has no frontmatter, so `claim_class`, `evidence_class` and `verdict_direction` are absent. They do not apply under the reflect rubric.
- Row 11's "Authorized expansion" label is half right: the departure from the design (an eager import instead of a lazy one) is authorized, but it is not an expansion.
- The card misses that the design contradicts itself on `status` exit codes: `issue-watcher.md:115` lists exit 2, while `:726` lists only 0, 1 and 6. The runbook follows `:726`.
- The card's Notes say "Nine hold and one is wrong", but items 1-10 are all listed as holding.
- Row 10 says `launch` "may import only `runner`". Design `:240` also allows `launch` to import `_ORCA_CLIS` from `install_user_setup`, and row 8 relies on that.
- The strongest verified finding is correctness gap 1. `disabled_since()` follows symlinks (`record.py:428`) while `disabled()` does not (`:423`), and `status` catches only `StoreError` (`cli.py:175`).

Not checked: the claims that need a repository-wide search, because I can only read files.
