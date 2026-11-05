# Reviewer 2 card (persona: qa; model class: haiku). Persisted by the orchestrator from the reviewer's returned text, condensed; claims and evidence refs are unchanged. Paths below are relative to the repo root; the reviewer cited them absolute.
reviewer: 2
persona: qa
findings:
  - id: F1
    claim: Task 2's first acceptance criterion is self-contradictory ("no CCSESSION_ASK_TIMEOUT set" vs "the test sets the limit to 1 second"), so the 30-second default inside ask_session_name is verified only through hint text; if the hint number were hardcoded every named criterion would pass with the default left unlimited (today's default is 0 at ccsession:1471).
    tag: grounded
    evidence: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md:46 and :94; src/superclaude/skills/ccsession-tag/ccsession:1471
    severity: minor
    deviation_class: drift
    recommendation: Task 6 adds a test running `ccsession --ask` with CCSESSION_ASK_TIMEOUT=2 asserting the hint reads "auto-named after 2s" (the hint follows the actual limit), failing against the current ccsession.
  - id: F2
    claim: Task 5 misses test_orca_invalid_name_asks_again, whose bad inputs (246 x's, 82 CJK chars) currently assert "invalid label ... asks again" but become exit-3 first-message text under Task 2; the catch-all clause does not describe its failing assertion.
    tag: grounded
    evidence: tests/unit/test_ccsession_tag.py:1592-1610; plan:43 and :84
    severity: minor
    deviation_class: none
    recommendation: Add the test to Task 5's list with its new expectation (both long inputs reach Claude as the last positional argument with an auto-name); verify with `uv run pytest tests/unit/test_ccsession_tag.py -k orca`.
  - id: F3
    claim: Task 3 reclassifies --session-id as task-carried while README:266 still groups it with the resume choices, but Task 9's acceptance criterion pins only the --fork-session statement.
    tag: grounded
    evidence: plan:57 and :128; src/superclaude/skills/ccsession-tag/README.md:266
    severity: minor
    deviation_class: none
    recommendation: Extend Task 9's criterion to "the --fork-session and --session-id statements match the code" and give the Task 9 table an explicit --session-id row; verify by grepping README.md for session-id.
  - id: F4
    claim: The five matrix rows the matcher left unmatched are covered in the plan body, so no spec requirement is taskless (INF-007/008 in Tasks 2 and 4; INF-014 in Task 7 and Constraints; INF-015 and INF-016 in Constraints and Task 11).
    tag: grounded
    evidence: plan:19-20, :25, :43, :69, :104, :147; .dev/reflect/pre-fixGitHubIssue31-20261105031639/artifacts/coverage-matrix.md:11-12, :18-20
    severity: minor
    deviation_class: none
    recommendation: No plan change; note that the matcher's blindness to the Constraints section causes the five unmatched rows.
  - id: F5
    claim: Auto-name uniqueness is pinned only against already-saved topic files with a month-day-hour-minute stamp, so two same-task launches inside one minute before either hook records rely on the hook-side -2 suffix, which no acceptance criterion or test covers.
    tag: grounded
    evidence: plan:31; src/superclaude/skills/ccsession-tag/hooks/session-name.sh:10-12
    severity: minor
    deviation_class: none
    recommendation: Add a Task 6 test calling `ccsession --auto-name "same task"` twice in one minute with no saved topics and asserting distinct labels, or state that the hook's -2 suffix is the concurrency guarantee and pin it with a test.
matrix_gaps: []
verdict: ready-with-notes
self_confidence: 0.82
calibration:
  calibrator_model_class: opus
  calibrated_confidence: 0.78
  note: blind calibration; F1,F2,F3 verified, F5 hook citation does not show a -2 suffix
