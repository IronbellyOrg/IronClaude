# QA Report: M4 fidelity gate, content verification (cycle 1)

**Date:** 2026-11-08. **Phase:** fix-cycle content verification (Step 9.M7). **Fix authorization:** false (report-only; no file other than this report was written).
**Inputs read:** `qa/m4/qa-fidelity-consolidated-findings.md`, `qa/m4/qa-fidelity-fix-report.md`, spec `spec-final.md` line 100, design `docs/designs/issue-watcher.md` lines 698-720, `cycle.py` 715-775 and 1154, `audit.py` (grep), `test_cycle.py` 1285-1325 and 1660-1745, `docs/designs/issue-watcher-setup.md` (grep), `research/06-gap-fill-decisions.md` DF-22 / DF-35 text.

## Overall Verdict: PASS

## Per blocking finding

| id | Result | Evidence |
|---|---|---|
| M-1 | FIXED | See the checks below. |

### M-1 checks

1. **Source lines read by me.**
   - Spec line 100: "The cycle line records the offset between the local clock and the `Date` header ... and an offset above 60 s [PROPOSAL] writes a `clock_skew` warning line." Two duties; only the second has a threshold.
   - Design line 715: `clock_skew_s` is "yes" in the Cycle-line column (`discovery_count`, line 714, is "optional").
2. **Code is faithful.** `cycle.py:751-756`: when the `Date` header parsed (`server is not None`), `self.clock_skew_s = int(round(skew))` is set unconditionally, and only `self._warn("clock_skew", ...)` sits under `if skew > SKEW_WARN_S` (60). `_conclude` (line 1154) passes the attribute to the cycle line; `audit.py:195` types it `(int, False)` and `audit._optional` drops only `None`, so a value of 0 is kept (proved by the passing `[0-0]` case). An unparseable or missing `Date` leaves it `None`, so the key is left out (DF-35 intact).
3. **Warning behaviour above 60 s is unchanged.** The warning is still guarded by `skew > 60` (so 60 gives none and 61 gives one, as DF-22 requires) and still carries `clock_skew_s` with the same rounded absolute value. `test_clock_skew_warning_is_present_from_61_seconds__df22` (61, -61, 300) is unchanged and asserts `reason == "clock_skew"`, the value, the login, exit 0, exactly one warning and the argv list. It also asserts the cycle line carries the value.
4. **Mutant replay (my own, on a `/tmp` copy of `src/superclaude`, `tests/issue_watch` and `pyproject.toml`, removed afterwards).** I changed `_login_step` so the cycle-line assignment sits inside `if skew > SKEW_WARN_S:` again. Running `test_cycle.py -k "skew or idle_cycle or unparseable_date"`: 5 failed, 6 passed. The failures are the four `...records_it__df22` cases (0, 59, 60, -60; `KeyError: 'clock_skew_s'`) and `test_idle_cycle_makes_two_gh_calls_and_writes_one_cycle_line__fr001`. The 61 / -61 / 300 cases and the unparseable-date test still pass on the mutant, as they should. The tests therefore do pin the behaviour, not just silence.
5. **No assertion weakened or deleted.** The old assertion (`"clock_skew_s" not in cycle line`, skews 0, 59, 60, -60) was inverted into an exact-value and `int`-type assertion over the same four skews (`test_cycle.py:1701-1714`); the no-warning assertion was kept. `test_unparseable_date_header_skips_the_skew_check__df35` gained an assertion (`test_cycle.py:1743`). The idle-cycle whole-line comparison gained `"clock_skew_s": 0` (line 1307), the spec-required consequence, with the dict compared by equality as before. Real tree: `uv run pytest tests/issue_watch/ -q` gives 2635 passed (matches the fix report). The tree is untracked, so I could not diff against a prior revision; the comparison rests on the finding text (old line 1710 and its four skews) and the new code.
6. **Authorized departures not undone.** The relevant ones are DF-22 (61 s gives one `clock_skew` line, 60 s none, warning reason list) and DF-35 (unparseable `Date` skips the skew check). Both hold, per checks 3 and 2. The fix touched no other departure area; the diff scope in the fix report (`cycle.py`, `test_cycle.py`, `issue-watcher-setup.md` row 414) does not reach the other 27.
7. **Runbook is true to the code.** `issue-watcher-setup.md:414` now says `clock_skew_s` is "the offset in whole seconds between GitHub's clock and the machine's, on every cycle that read GitHub's date; the `clock_skew` warning is written only above 60 seconds". Line 376 (warning reason: differs by more than 60 seconds), line 416 (warning row carries `clock_skew_s`), line 236 and line 612 agree with the code.

## New blocking findings

None.

## Minor notes (not blocking; not rechecked later)

- N1. Runbook line 414 still prefixes the field with "optional" in the same sentence as `discovery_count`. It is correct in the sense that the key is absent when GitHub's date is unknown, and the parenthesis explains the rest, but the wording could say "present whenever GitHub's date was read" without "optional".
- N2. "On every cycle that read GitHub's date" is slightly wider than the code: a cycle that stops with `account_id_mismatch` (`cycle.py:749-750`) raises before the skew is computed, so its cycle line has no `clock_skew_s` even though the header was read. The spec sentence (line 100) does not cover that early-stop case either; no test pins it. Wording or a one-line move, at the owner's choice.

## Self-Audit

**(a) Reliance list:** No inherited structural verdict was supplied in the spawn prompt, so standalone behaviour applied and nothing was skipped on reliance. The fix report's own claims (2635 passed, mutant 5 failed) were not relied on; I re-ran both.

**(b) Independent semantic checks:**
- Spec line 100 and design line 715 read directly (Read) and compared to `cycle.py:751-756` (Read) and `audit.py:195, 304-318` (Grep).
- Mutant replay executed on a temp copy (Bash): 5 failed / 6 passed with the expected test names.
- Full suite on the real tree (Bash): 2635 passed.
- Test diff reasoning on `test_cycle.py:1307, 1701-1714, 1717-1731, 1743` (Read): same parameters kept, assertion inverted to a stronger exact-value check, one assertion added.
- DF-22 and DF-35 text grepped from `06-gap-fill-decisions.md` and compared to the final behaviour.
- Runbook lines 236, 376, 414, 416, 612 grepped and compared to the code.

**Confidence:** Verified: 7/7 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 4 (one blocked by the UV-only hook and rerun with `uv run python`)
**Web research:** none performed.
