# Pipeline Hardening Closure (Wave 4.5)

Added after REPORT.md was finalized: the earlier pass of this run skipped Wave 4.5 without recording HC0. Recorded here so the run is complete; REPORT.md is otherwise unchanged.

## HC0 — Applicability + boundary scan
| boundary_type | producer / transformers / consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|
| CLI/subprocess | session -> scripts/finish-merge.sh -> `git commit` | probe-finish.out:1-9 | the gate proves a weaker property than the commit records | applicable | the defect is in a script gate in front of a subprocess commit |
| gate-status-enum | finish-merge.sh tokens `markers`, `staged_unexpected` -> refs/conflict-mechanical.md step 9 table | finish-merge.sh:24-26 | a false pass publishes an unreviewed change | applicable | the gate controls HALT vs commit |

pipeline_hardening_applicable: true
Mechanism statement: a pre-commit gate compared a narrower view of each index entry (fixed marker width, blob id only) than the commit records, so inputs differing only outside that view passed.
known_escapes_caught: []

## HC1 — Runtime-entrypoint verification: PASS
The regression tests run the real script (tests/pr_submit/test_conflict_scripts.py test_wider_conflict_marker_size_left_in_place_is_markers, test_unrelated_mode_change_is_staged_unexpected, test_file_swapped_for_symlink_with_same_bytes_is_staged_unexpected); all three fail against the HEAD script (negative witness run 2026-11-04T22:19Z).

## HC2 — Contract enumeration: PASS
Tokens `markers` and `staged_unexpected`, exit 2 and the one-line stdout are unchanged; the step 9 token table needs no change; exactly one `git commit` remains (test_finish_script_static_rules).

## HC3 — Unmask and sweep: N/A
Rationale: the marker regex is built from an exact width read from git's own attribute, not widened by substring matching; no generated-artifact parser changes.

## HC4 — Effective-input proof: N/A
Rationale: no review/audit selector is involved.

## HC5 — Off-path review
off_path_review_decision: performed (independent troubleshoot-analyst self-review lens over the full fix diff)

## Verdict
waiver_status: none; HC3, HC4 N/A with rationale -> pipeline_hardening_verdict: advisory (row 6). backtest_status: not_run.
