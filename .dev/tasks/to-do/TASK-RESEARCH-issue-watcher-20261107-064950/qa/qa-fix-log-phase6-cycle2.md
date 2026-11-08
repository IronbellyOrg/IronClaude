# QA fix log: Phase 6, fix cycle 2 (Gate 3)

Report edited: `RESEARCH-REPORT-issue-watcher.md` (targeted Edit calls only).
Input: `qa/qa-consolidated-findings-phase6-cycle2.md` (2 blocking findings: 1 = NEW-1/B1, 2 = NEW-2).
Name note: the cycle prompt names `qa-fix-log-cycle2.md`; this file uses `qa-fix-log-phase6-cycle2.md` because a freshness hook blocks the literal name.

## Entries

### Finding 1 (NEW-1 / B1): unreachable `launched` retry branch. FIXED

Cause: step 3 dropped every `launched` and `abandoned` entry with no lease condition, so the `may_dispatch` and test branches that retry or abandon a `launched` entry after the lease could never run.

Changes in `RESEARCH-REPORT-issue-watcher.md` (Section 8, Phase 5, plus two cross-references):
- Step 5.1 `DispatchEntry.state`: added the terminal state `claimed`.
- Step 5.1 `may_dispatch`: one "wait window" rule: `pending`, `launched` and `unknown` give `wait` only while `now - last_at < lease` and become eligible after it (`launch`, `retry-launch` or `abandon` as before); `abandoned` and `claimed` give `wait` (terminal). Added: `launched` means "Orca started the session"; a claim stopping after the launch (`E-TIER-UNAVAILABLE`, `claim.md:20`, read) is retried or reported `abandoned` after the lease; `claimed` is set only when the own marker exists (`claim.md:88`, read); step 3 and step 7 apply the same table [DESIGN].
- Step 5.2 `CycleReport`: added `claimed: list[int]`.
- Algorithm step 3: drop `claimed` and `abandoned` always and `pending`, `launched`, `unknown` only inside the lease; past-lease entries stay candidates; stated the bound (at most one candidate slot before an entry is terminal or retried) [DESIGN].
- Algorithm step 6: a found marker sets the entry to `claimed` (new entry with attempts 0, or the existing entry keeps its attempts), whatever its state; replaces the old "write `launched` with `marker-found`" rule.
- Algorithm step 7: states which entries can reach `may_dispatch`.
- Phase 5 intro: replaced "selected again every cycle" with the lease, retry, cap and `claimed` behaviour.
- Test scenarios: "Second cycle" (launched entry; retry after the lease with `now` advanced; abandon after `max_attempts`; marker variant gives `claimed`), "Lost record" (writes a `claimed` entry), "Unknown outcome" (advance `now` past the lease explicitly), "Many already-handled candidates" (three cases; case 3 is a past-lease entry with a marker that becomes `claimed` and then consumes no slot).
- Section 4 G9 (last cell) and SC-10: now state the same lease, retry and `claimed` rule.

Verified by: Grep for `` `launched` `` over the report (all hits at 691, 1650, 1661, 1665, 1670, 1701, 1702, 1709 read and consistent); Read of `claim.md:14-91`; Read of the `may_dispatch` text after the edits.

### Finding 2 (NEW-2): `resolve_orca` and the PATH-stub tests. FIXED

Cause: `resolve_orca` used the real `shutil.which` with names `orca-ide`, `orca`, while the e2e stub installer replaced only `gh`, `git`, `orca` and prefixed the real `PATH`.

Changes:
- Step 3.4: `resolve_orca(orca, *, which=shutil.which, names=("orca-ide","orca"))`; `launch_claim(..., which=shutil.which)` passes it on; a `CommandError` from the probe (`E-TIMEOUT`, `E-TOOL-MISSING`) disqualifies that candidate (as `_find_orca` continues on `OSError` and `SubprocessError`, `install_user_setup.py:217-218`, read; names from `_ORCA_CLIS`, l.35, read), so a probe timeout is a probe failure and never `unknown`; the launch-timeout rule is limited to the launch call. Host fact recorded from `which -a orca-ide` and `which -a orca` run on 2026-11-07.
- Step 5.2 `run_cycle(..., which=shutil.which)`; algorithm step 12 passes `which=which`.
- Step 3.5 `FakeOrca`: added the `probe_timeout` mode; `timeout` mode times out the launch call only.
- Step 3.6 tests: `resolve_orca` always gets a fake `which`; added the probe-timeout cases (next candidate or `E-ORCA-NOT-FOUND`, never `unknown`) and `launch_claim` probe timeout (`failed`) versus launch timeout (`unknown`).
- Step 6.1: stub installer also writes `orca-ide`; `PATH` is set to the stub directory only, not prefixed [DESIGN].
- Step 6.2: e2e runs with the default `which` against the restricted `PATH`; each stub logs its program name; asserts the probe and launch are logged under `orca-ide`.
- Test plan summary: `test_cli_once.py` also monkeypatches `shutil.which`.

## Not changed
- Minor notes (unescaped pipes in code spans, `str(int(number))` wording, `D1..` default IDs, `pending` wording, `-L 100` truncation) stay notes per the findings file.
- No heading changed, so the Table of Contents was not regenerated. Owner decisions D1-D3 untouched. No `[CONTRADICTION` token in the report (Grep count 0).
- Research, synthesis and `research-notes.md` files were not edited.

Status: Complete
