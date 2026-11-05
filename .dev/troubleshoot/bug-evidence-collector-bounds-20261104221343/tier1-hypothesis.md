# Hypothesis: the collector's no-`timeout` branch has no deadline enforcement (A2), and a resume restart reuses its evidence directory under the same cycle_id (C1)

**Agent**: root-cause-analyst (lens; worker troubleshoot-analyst)
**Tier**: 1
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: missing fallback (A2) + path collision between two documented rules (C1)
**Claim class**: `mixed`
**Evidence class**: `runtime_observed` (parent probe, tier1-observation.md ## Probe)
**Verdict direction**: `AFFIRM` (confirms A2 and C1)
**Consistency with docs**: conflicts (A2's fix matches the script header :26 "bounded to 60 seconds"; C1's fix changes the `sync/<cycle_id>/` layout written into both refs and the design)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:82-85 @ bash, PATH without `timeout`; refs/conflict-intent.md:19 @ Tier 2 restart (conflict-mechanical.md:247, :249)

producer-citation-check: skipped — menu absent or empty (producers.md: observation-kind trace, header-only table)

## Claim
A2: when `timeout` is missing, `bounded()` runs `"$@"` in the foreground; `check_deadline` runs only before and after the command, so a hung read is waited out in full. C1: rows 5 and 7 restart under the same `cycle_id`; the restart passes the same `--out`, which already holds the first attempt's files, so the collector fails `out_not_empty` and the cycle escalates to Tier 3.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | command_output | tier1-observation.md `## Probe` | restart into `sync/sync-1/1/` gives `EVIDENCE_FAIL out_not_empty`, exit=2 |
| E2 | command_output | tier1-observation.md `## Probe` | no `timeout`, `git show` hangs 65 s: elapsed=65s (budget 60 s) |
| E3 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:82-86 | else branch `"$@"; rc=$?`, then `check_deadline` |
| E4 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:147-151 | an existing non-empty `--out` fails `out_not_empty` |
| E5 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh:185, :193-194 | callers redirect `bounded`'s stdout/stderr into `$TMP` files |
| E6 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md:19, :30 | `--out <output-dir>/sync/<cycle_id>/<n>/`; any EVIDENCE_FAIL escalates to Tier 3 |
| E7 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:71, :247, :249 | resume reuses the open cycle_id; rows 5 and 7 restart under the same cycle_id |
| E8 | test_assertion | tests/pr_submit/test_conflict_scripts.py:1393-1394 | the timeout test is skipped when `timeout` is missing; the fallback has no test |

## Proposed Fix
(A2) In `bounded()`: `local remaining rc pid`; replace the else branch with a background run `"$@" 3>&- 4>&- &`, `pid=$!`, a `while kill -0 "$pid"` poll with `sleep 0.2`; at `SECONDS >= DEADLINE`: `kill "$pid"`, `sleep 1`, `kill -s KILL "$pid"` if still alive, `wait "$pid"`, `fail timeout "'$*' did not finish within the ${LIMIT_SECONDS}-second budget"`; otherwise `wait "$pid"; rc=$?`. The caller's redirection covers the background job; `3>&- 4>&-` keeps a surviving child off the caller's pipes; fail writes only to fd 3; the job is reaped before the EXIT trap; no banned words. Test P-1: symlinked PATH without `timeout`, a git wrapper sleeping 90 s on `show`; assert `EVIDENCE_FAIL timeout`, "60-second budget", elapsed < 65 s, no temp dir.
(C1) conflict-mechanical.md step 3 (:71): `attempt :=` the number of `sync_started` records for this `cycle_id`, counting the one just appended; `cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/`. :97, :103: resolution.md, evidence `<cycle_dir><n>/`, message and manifest under `<cycle_dir>`. Row 5 (:247): the restart's step 3 writes into a new attempt directory. conflict-intent.md:19 `--out <cycle_dir><n>/`; :71, :99 `<cycle_dir>`; :95 every attempt's directories stay. test_conflict_e2e.py:610, :845 `run_log.output_dir / "sync" / cycle_id / "a1"`. Regression: fill `a1/1/`, collect into `a2/1/`, expect exit 0 and `a1/1/` unchanged.

## Confidence
Self-reported 0.85 (calibrator re-grades).

## Risks
- A killed git may leave its own children; the trap still removes $TMP.
- PID reuse between `kill -0` and `kill`: short window.
- `sleep 0.2` is not POSIX (GNU and BSD accept it).
- P-1 takes about 60 s.
- A miscounted attempt fails safe (`out_not_empty` -> Tier 3).

## If I'm wrong, it's probably because...
`kill -0` keeps succeeding on a finished child bash has not reaped, so every no-`timeout` run would wait until the deadline.

## Falsification standard
After the fix: (i) the A2 probe gives elapsed <= 62 s, stdout exactly `EVIDENCE_FAIL timeout`, no surviving wrapper; (ii) with no `timeout` and no hang the run exits 0 in under 5 s; (iii) collecting into `a2/1/` succeeds and leaves `a1/1/` unchanged. E4, the timeout-stub and static-rule tests still pass.

## Alternatives considered
- Require `timeout`: rejected (macOS does not ship it).
- Clear the directory on restart: rejected (conflict-intent.md:95 keeps evidence).
- Allow a non-empty --out: rejected (breaks E4, mixes old files).
- New cycle_id on restart: rejected (breaks prior_conflict_cycles, sync_cap, open-cycle tracking, :253).
