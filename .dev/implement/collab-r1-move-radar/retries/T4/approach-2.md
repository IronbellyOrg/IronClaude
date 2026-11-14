Implementer claims (attempt 2, executor):
- Built tools/run-reviewer.sh (H1 brief, sandbox cwd, hang guard via timeout --kill-after=5, one isolated retry, H2 + one re-ask on the same session), tools/h2_normalize.py (truncate anchor/anchor2/claim, parse_block, kept/dropped lines), tools/values.py (R-42 k, finish/guard/hang offsets, A-2/A-3, Spike 4 turn extraction, deadlines helper).
- Test kit: stub claude (tests/fixtures/bin/claude) replaying canned JSON, sleeping, exiting 127 or running the --settings hook; Runner fixture in tests/conftest.py.
- Believed T4.AC1 met by the 2.6/2.7 behaviour above; T4.AC2 met by test_settings_and_cmd.py (cmd part), test_h2.py, test_values.py, test_runner_retry.py, test_faults.py F-8/F-9/F-10/F-13 (97 passed).
- A1 review: dropped_lines counted parser errors -> fixed to count block lines (kept/dropped in h2.json).
- A2 review: split('\n') vs splitlines() line numbering -> fixed with splitlines(keepends=True).
- Open: report read in universal-newline mode, so CRLF/CR terminators are rewritten to LF (F3.2).
