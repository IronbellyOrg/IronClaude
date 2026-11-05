# Wave 3C calibrations (blind, confidence-calibrator on opus; calibrator_diversity: degraded, because every available class also reviewed)

Persisted by the orchestrator from the three returned reports. Rubric: `refs/reflection-rubric.md`, five dimensions, C = arithmetic mean.

| Reviewer | Persona / model | C | Citation grounding | Coverage | Severity clarity | Risk surface | Actionability |
|---|---|---|---|---|---|---|---|
| 1 | analyzer / sonnet | 0.81 | 0.85 | 0.65 | 0.85 | 0.80 | 0.90 |
| 2 | qa / haiku | 0.80 | 0.85 | 0.70 | 0.85 | 0.75 | 0.85 |
| 3 | refactorer / opus | 0.82 | 0.88 | 0.70 | 0.85 | 0.78 | 0.88 |

All three are below the 0.85 floor, so the ensemble escalates (it already had).

## Reviewer 1 (C = 0.81)

- Citations: 8 mismatches or unsupported claims, none material to the verdicts:
  - R1-01 says "both skills write the contract only when `--output-dir` is set"; true for graph (`sc-graph-protocol/SKILL.md:64`, `:85`), wrong for impact (`--output-dir` has a default at `sc-impact-protocol/SKILL.md:29`, and step 10 always writes the contract). The remaining R1-01 claims hold: impact's step 1 validates a closed flag table and "bad flags" ends blocked; graph's table has no row for the new flags; both skills' contract text names only `--output-dir`. Calibrator keeps R1-01 blocking.
  - R1-02: plan:171 adds only `--report-dir` to the init-lite skill's Inputs table (not both flags).
  - R1-06: spec:142 says brainstorm passes the flag "from P2", which cuts against the downgrade.
  - R1-13: the `graph.md:39-53` range is off by a few lines; the order it describes is right.
  - R1-07 and R1-09 rest on uncited claims.
- Per finding: R1-02, 03, 04, 05, 08, 10, 11, 12 CONFIRMED; R1-01, 06, 07, 13 PARTLY; R1-09 NOT CONFIRMED (matrix not read).

## Reviewer 2 (C = 0.80)

- Citations: two slips. R2-01 says business-panel has 6 key lines (it has 5, lines 5-9); the "at most 4 deleted lines" conclusion holds. R2-07's line 43 of the parity test is the docstring (the pin is lines 41-47).
- Added by the calibrator: `business-panel.md:6` has trailing spaces; if an executor strips them, a fifth line is deleted and Task 11's limit fails. `tests/test_cleanup_audit_structure.py` tests `src/superclaude/cli/cleanup_audit`, not the file Task 6 edits, so it should be dropped from Task 6.
- Per finding: R2-02, 03, 04, 05, 06 CONFIRMED; R2-01, 07 PARTLY.

## Reviewer 3 (C = 0.82)

- Citations: 22 of 22 match. One wrong fact: R3-06 says seven of the sixteen pre-existing tests are under `tests/skills/`; plan:42 lists six.
- The card's note says `t1_ref` is null on every finding, but R3-01 has `t1_ref: F-001`.
- Per finding: R3-01, 02, 03, 04, 05, 07, 08, 09, 10 CONFIRMED; R3-06 PARTLY.
