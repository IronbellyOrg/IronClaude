# Calibration Report

**Card under calibration**: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post/reviewer-cards/reviewer-1-card.md
**Rubric**: /home/coder/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md
**Card tier**: 2
**Timestamp**: 2026-11-08T04:50:00Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Citation grounding | 0.72 | Almost every row and gap has a file:line, and 27 of the 29 citation groups I checked match. Two do not match, and one of them backs the headline claim that no issue can be launched twice: the "At-most-once launch" note cites `cycle.py:335-337`, but the code is at 1060-1062. Correctness gap 3 also cites the wrong lines and is partly wrong on the facts (see Notes). Rows 8, 9, 10 and 12 and gap 13 rest mainly on "brief" codes, which the reviewer says openly it did not re-read. |
| Coverage completeness | 0.68 | All eight production modules were read in full, and there is an explicit list of what was not read: spec-final.md, the decision register, tasklist OQ text, the tests, `__init__.py`, `main.py` and `swarm/atomic.py`. But the adherence summary is a self-declared estimate ("38 units ... about 30 adherent") with no mapping of each spec requirement. That is partial coverage with an explicit gap list, which is the 0.60-0.84 band. |
| Deviation-classification clarity | 0.75 | Every row uses the required four categories (authorized expansion, necessary deviation, drift, regression), and the tally (3 / 4 / 5 / 0) matches the table. Deductions: row 6 hedges between two categories ("Drift (alternative reading: NFR-014 regression)"). Row 12 is called a necessary deviation although "I did not read the tests". Row 2 says the change "arguably contradicted" AC-17 and that "no owner decision authorizes it" but stops at Drift without saying why it is not a Regression. The header says "1 MEDIUM, 11 LOW", but rows 1 and 2 are both MEDIUM. |
| Risk surface coverage | 0.85 | Strong. There is an explicit trace of the launch-once guarantee. The 13 correctness gaps cover the kill switch, the crash path that skips `_commit`, the day cap failing open on clock skew, untested invariants (login-regex parity, only one copy of the issue-number bound pinned), output-cap effects and dead code. Most of them verified. Deductions: gap 3 misdescribes the kill-switch window, and the reasoning about how far each risk reaches is light on several gaps. |
| Recommendation actionability | 0.50 | The card has no recommendations section. Only row 6 ("`cli.py` could pass `cycle.SystemClock().now()`") and gap 3 (a re-check before `mark_pending`) name a concrete change. Rows 2, 3, 4 and 5 and most gaps give a location but no action and no success test (for example, row 2 never says to amend design 4.3 or the spec reason list). Several items end in "flag it for triage". |

The reflect rubric's five dimensions were used, and C is their arithmetic mean.

## Confidence

- **Self-reported (in card)**: none. The card states no confidence number, so there was nothing to ignore.
- **Calibrated (this report)**: **0.70**
- **Formula applied**: mean(0.72, 0.68, 0.75, 0.85, 0.50) = 3.50 / 5 = 0.70. No caps, because the reflect rubric defines none for this case.
- **Delta**: not computable, because the card reports no confidence. Why the score is moderate: the findings are mostly well grounded and the risk coverage is good, but coverage is estimated, there are almost no actionable recommendations, and two citations are wrong (one on the headline claim).

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: "`C < 0.85` is an automatic ESCALATE." (rubric, Threshold guidance). `--depth deep` would also favour escalation, but the low-confidence rule fires first.
- **Execution restriction**: none (`--no-escalate: false`).

## Notes

- **Rubric used**: the reflect rubric (five dimensions, plain mean). The troubleshoot-only steps were skipped as instructed: the runtime-check cross-tab, the structural C-rules, the gated-minimum Stage-2 trace and the claim-class handling. The card has no claim_class or evidence_class frontmatter; this is not applicable under the reflect rubric.
- **Citations verified (27 groups; repo root `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher`, files under `src/superclaude/cli/issue_watch/`)**:
  1. `audit.py:55-64`: `cycle_crashed` (57) and `cycle_complete` (64), each with a `[PROPOSAL]` comment.
  2. `cli.py:35`: `_EXIT_CRASH = 1 # [PROPOSAL] C-3`.
  3. `cli.py:123-129`: catches `Exception`; line 128 prints only `type(exc).__name__`.
  4. `cycle.py:1134-1137`: returns `cycle_complete`.
  5. `docs/designs/issue-watcher.md:114`: the `once` row lists exit codes 0, 2, 3, 4, 5, 6, 7 and 75, with no 1.
  6. Reason-table count: I counted 59 names in `audit.py:28-101`.
  7. `cycle.py:635-641`: the `re-approved` branch. Whether it can be reached was checked against `record.py:466-487` (a new entry has no ids) and `record.py:503-525` (`fail` never sets approval ids). Approval ids are written only by `mark_pending` (`record.py:566`) and `mark_claimed`, so the card's "unreachable" claim holds.
  8. `cycle.py:859-875` (`_approve`), called from 891 and 926.
  9. `cli.py:26,319`, together with `cycle.py:29` (re-exports `format_utc` from predicates).
  10. Issue-number bound: `predicates.py:20,54`, `launch.py:30,90`, `audit.py:203,236`, `record.py:132`.
  11. Login regex copies: `cycle.py:468` and `github.py:134` are the same pattern.
  12. `predicates.py:57` and `launch.py:36`: identical `OPERATION_ID_PATTERN`.
  13. `audit.py:381-404`: reads the wall clock when `ts` is None (395-397). `cli.py:79,127,219` pass no `ts`; `cli.py:266` does; `cli.py:317-319` matches.
  14. `launch.py:251-259`, `272`, `332`.
  15. `record.py:23-29`: imports `format_utc`, `parse_utc`, `valid_issue_number` and `valid_operation_id`, which is consistent with rows 8 and 9.
  16. `record.py:183,585,607`.
  17. `audit.py:81,82,98,99,101`: `marker_unreadable`, `edits_unreadable`, `dry_run_shadow_reset`, `reset_refused`, `operator_reset`.
  18. Row 11: `cycle.py:644-649`, `738-742`, `814-815`, `1010-1016`; `launch.py:119-132`, `343-355`; `runner.py:70-72`.
  19. Gap 1: `record.py:689-703` (window `now - 24h < t <= now`) and `cycle.py:755-756`.
  20. Gap 2: `record.py:423` (`lexists`) versus `425-431` (`os.stat`, catches only `FileNotFoundError`).
  21. Gap 4: `cycle.py:685-690`; only `_Stop` is caught, so another exception skips `_commit` at 690.
  22. Gaps 5 and 12: `runner.py:15`, `57-64`, `91-101`, `126` (stderr is capped before it reaches `launch.py:322`).
  23. Gaps 9 and 10: `launch.py:318-319` and `326-334`; `_first_hit` searches `("error","operation_id")` (`launch.py:42-45`).
  24. Gap 6: `cycle.py:35`, `1235`, `1244`, `1255`; `record.py:748`; `cli.py:173`; `runner.py:35`.
  25. Gap 7: `record.py:208` and `538-568` (state checked only).
  26. Gap 8: `predicates.py:205-209`.
  27. Gap 13: `cycle.py:307-324` (`lstat` at 307, `O_NOFOLLOW` open at 321, `fdopen` at 322, no `fstat`).
- **Citations that did not match**:
  - **"At-most-once launch" note**: the card cites `mark_pending` at `cycle.py:335`, `_save()` at 336 and `launcher.launch` at 337. Lines 335-337 are actually the approvers-file line parser. The real lines are `cycle.py:1060` (`mark_pending`), `1061` (`_save`) and `1062` (`launch`). The claim itself is true.
  - **Correctness gap 3**:
    - The card says DISABLED is "checked once at `cycle.py:308`". Line 308 is `except OSError:` in the approvers loader.
    - DISABLED is actually checked at `cycle.py:693` and checked again at `cycle.py:1033-1034` (`disabled_mid_cycle`), so "checked once" is wrong.
    - The real unprotected window is 1033 to 1060. It holds the second origin git call (`cycle.py:1041-1045`, up to `GIT_TIMEOUT_S = 10.0` at `cycle.py:39`), and there is no re-check after that call.
    - The cited `cycle.py:335-337` should be 1060-1062.
  - **Card header**: "0 HIGH, 1 MEDIUM, 11 LOW" contradicts the table, which has two MEDIUM rows (1 and 2) and ten LOW rows.
- **Not checked**: `setup.md:318,331,344`; the test lines in row 12 (`test_cli.py:967,1070`, `test_record.py:739`, `test_cycle.py:735,4694`); TL:332 and TL:998; the design D: lines other than D:114; the spec S:92, S:94 and S:272; the brief codes (C1a to C10, A7, A11, A12); the DF-xx decision register; OQ-49.
- **Structure**: there is no recommendations section, which is what drives the low actionability score. Spec coverage is estimated rather than mapped requirement by requirement.

---

| Status | Result |
|---|---|
| DONE | Scored the card at 0.70 (escalate because of low confidence) after checking 29 citation groups against the repository: 27 matched, 2 did not. |
| NEXT | The orchestrator saves this report. The reviewer should correct the two wrong citations (launch-once note and correctness gap 3) and the MEDIUM count in the header. |

I did not read the test files, the setup runbook or the decision register, so rows 10 and 12 and the DF-xx anchors remain unchecked.
