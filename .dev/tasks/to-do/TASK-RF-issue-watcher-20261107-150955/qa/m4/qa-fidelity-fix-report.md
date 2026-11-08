# Fidelity fix report (M4 gate, fix cycle 1)

**Step:** 9.M5. **Date:** 2026-11-08. **Fix agent:** one `rf-qa` agent with `fix_authorization: true` (the only agent that modified files).
**Input:** `qa/m4/qa-fidelity-consolidated-findings.md` (blocking: 1, minor: 65). Minor findings M-2 to M-66 are notes and were not touched.

## Blocking findings

| id | result | files changed | what changed |
|---|---|---|---|
| M-1 | FIXED | `src/superclaude/cli/issue_watch/cycle.py`; `tests/issue_watch/test_cycle.py`; `docs/designs/issue-watcher-setup.md` | See below. |

### M-1 detail

Source: spec line 100 (the cycle line records the offset every cycle; only the `clock_skew` warning line has the 60 s threshold) and design line 715 (`clock_skew_s` is "yes" in the cycle-line column).

- `cycle.py` `_login_step` (about lines 751-756): `self.clock_skew_s = int(round(skew))` is now set on every cycle where the GitHub `Date` header parsed. The `_warn("clock_skew", ...)` call stays guarded by `skew > SKEW_WARN_S`. When the server date is unknown (`server is None`, e.g. an unparseable header, DF-35) the attribute stays `None` and `audit.py` leaves the key out of the line, as before. The value is the absolute offset, as before.
- `audit.py` needed no change: `_optional` drops only `None` (not `0`), `_TYPES` has `clock_skew_s: (int, False)` and `_RULES` has no rule for it, so `0` is accepted. Proven by the new `[0-0]` case below.
- `tests/issue_watch/test_cycle.py`:
  - The test that asserted the omission (was line 1710, `assert "clock_skew_s" not in _the_cycle_line(lines)`) is now `test_clock_skew_warning_is_absent_up_to_60_seconds_but_the_cycle_line_records_it__df22`, parametrized over skew 0, 59, 60 and -60 with expected `(0, 59, 60, 60)`. It still asserts no warning line, and now asserts the cycle line holds the exact rounded `int` value.
  - The 61 s boundary was already covered by `test_clock_skew_warning_is_present_from_61_seconds__df22` (61, -61, 300): warning present and the cycle line carries the value. Unchanged.
  - `test_unparseable_date_header_skips_the_skew_check__df35` now also asserts `"clock_skew_s" not in` the cycle line (server date missing).
  - `test_idle_cycle_makes_two_gh_calls_and_writes_one_cycle_line__fr001` compares the whole cycle line; its expected dict gained `"clock_skew_s": 0`. That is the spec-required consequence of M-1, not a weakened assertion.
- `docs/designs/issue-watcher-setup.md` section 10.3 table (about line 414): the `cycle` row said only "optional `discovery_count`, `clock_skew_s`". It now says `clock_skew_s` is the offset in whole seconds on every cycle that read GitHub's date, and that the `clock_skew` warning is written only above 60 seconds. The `warning` row and section 10 reason table already matched.

No assertion was weakened or deleted. No authorized departure (DF-01 to DF-60 list) was touched: DF-22 (boundary tests, warning reason) and DF-35 (unparseable date skips the check) still hold.

## Needs owner decision

None.

## Results

| check | result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` | 2635 passed (before the fix: 1 failed, 2634 passed, the whole-line idle test, fixed as above) |
| `make lint` | ruff "All checks passed!" (architecture policy: 5 warnings, none new) |
| `uvx --offline ruff@0.15.20 check` on `cycle.py` and `test_cycle.py` | All checks passed |
| `uvx --offline ruff@0.15.20 format --check` on the same two files | 2 files already formatted (one `format` run was needed on `test_cycle.py` for the new parametrize line) |

## Mutant check

A copy of `src/`, `tests/` and `pyproject.toml` was placed in `/tmp/m4-mutant` and `_login_step` there was changed back to apply the threshold to the cycle line (`if skew > SKEW_WARN_S:` around the `self.clock_skew_s = ...` assignment). Run with `PYTHONPATH=/tmp/m4-mutant/src`, selecting the clock-skew and idle-cycle tests:

- mutant: 5 failed, 5 passed. The failures are the four new `...records_it__df22[0-0|59-59|60-60|-60-60]` cases (`KeyError: 'clock_skew_s'`) and `test_idle_cycle_makes_two_gh_calls_and_writes_one_cycle_line__fr001`. The 61/-61/300 cases still pass on the mutant, as expected.
- real tree: 2635 passed.
- `/tmp/m4-mutant` removed. The repository was never mutated; `cycle.py` line 755 holds the fixed form.

## Files changed (deliverables only)

- `src/superclaude/cli/issue_watch/cycle.py`
- `tests/issue_watch/test_cycle.py`
- `docs/designs/issue-watcher-setup.md`
