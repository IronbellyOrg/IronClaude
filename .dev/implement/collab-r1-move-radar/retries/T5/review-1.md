start=9166c23cce094921f5b1d325c7ebb588998125b4 tree=5e02bad6d1cd9f1d769eac2c0bf372b08d8a8057
## Acceptance criteria

T5.AC1: **unmet** (F1.1).
- 2.8 post-run checks are present. Validator re-run over the (board line, logged text) pairs, plus orphan line or event checks: `tools/collab_summary.py:213`. The `task_hint` check runs just below it. The 12-character ground-truth window check: `tools/collab_summary.py:221`. Tele naming `.dev/reflect` or `ground-truth`: `tools/collab_summary.py:224`. `git status --porcelain`: `tools/collab_summary.py:228`. Candidate sha256: `tools/collab_summary.py:237`. QUARANTINED plus exit 3: `tools/collab_summary.py:338-341`. `anon_leak` written to both collab.json and audit.json: `tools/collab_summary.py:345-360`.
- 2.9 collab.json: every R-23 key is present, with null or 0 where F3 has no value (`tools/collab_summary.py:29`, `:286-290`, `:297`, `:321-328`).
- 2.10 detections in collab_summary.py: spot-check (`tools/collab_summary.py:255`, `:265`), `move_executed` (`:297`) and `ALARM hook_calls=0` (`:299`).
- 2.9 alarms: SNAPSHOT (`tools/alarms.py:54-55`), SLO budget (`:62`), drift (`:80`) and SAME_GAPS (`:84`).
- One defect in the 2.9 CONVERGENCE ledger rule (`tools/alarms.py:35-36`; F1.1).
- 5.3: `anon.sh` follows the stated order (`tools/anon.sh:18-35`).
- 5.4: `results.py` row and package fields and null sums (`tools/results.py:121-123`), plus the duplicate refusal (`tools/results.py:151`).
- R-46 cleanup: `tools/cleanup-sessions.sh:15-20`.

T5.AC2: **unmet** (F1.2).
- The pytest command passes (120 passed).
- Test locations:
  - T-14: `tests/test_anon.py:8`
  - T-15: `tests/test_judge_path.py:17`
  - T-16: `tests/test_results.py:36`, `:49`
  - T-17: `tests/test_collab_summary.py:32-106`
  - T-18 and F-2: `tests/test_alarms.py:24-41`
  - T-19: `tests/test_cleanup.py:8`
  - F-1, F-3, F-4 and the F-8 slo_breach part: `tests/test_faults.py:88`, `:107`, `:128`, `:142`
- T-17's "post adds … anon_leak" check is vacuous (F1.2).

F1.1 sev=blocking trigger=B1 ac=T5.AC1 at=tools/alarms.py:35 anchor="the five tools implement the behaviour of DESIGN.md sections 2.8, 2.9, 2.10 (summary and alarm detections), 5.3 and 5.4" chk=y,n,n,n family=alarm-partial-sum fix=make row_ledger return None unless every package of the row has status ok (or compare per-package means), so CONVERGENCE never compares a partial sum with complete-row sums first=A1 origin=new covers="its `ledger_rows` fall more than 20% below the collab-0 mean": `row_ledger` sums `ledger_rows` over the `ok` packages only (`tools/alarms.py:35-36`). An incomplete collab-1 row with the same per-package ledger rows as the baseline therefore fires CONVERGENCE. Probe: 3 packages × 10 rows in collab 0 and DE invalid in collab 1 gives `ledger_rows 20 < 0.8 x 30.0`, fired. An incomplete collab-0 row likewise pulls the collab-0 mean down. This contradicts DESIGN.md:361, "sums are then `null`, never a partial number". It can also spend the "at most 2 of 12" independence guard on runs that only lost a package.
F1.2 sev=blocking trigger=B1 ac=T5.AC2 at=tests/test_collab_summary.py:40 anchor="`post` adds `ledger_rows` and `anon_leak`" chk=y,n,n,n family=vacuous-test-check fix=in T-17 add a case that writes label-key.json and a merged-anon.md (or runs anon.sh), runs post, and asserts anon_leak == 0, plus a planted row id or reviewer id giving anon_leak > 0 in both collab.json and audit.json first=A1 origin=new covers="T-17 … `post` adds `ledger_rows` and `anon_leak`": the only anon_leak assertion is `"anon_leak" in c`. `pre` already writes `"anon_leak": None` (`tools/collab_summary.py:326`), so the assertion holds even if `post` never computed anything. No test creates `label-key.json` or `merged-anon.md` for `post`, so the leak count (`tools/collab_summary.py:345-360`) is never run by the suite. My scratch probe shows the code works; the check DESIGN 6.1 T-17 lists is missing.
F1.3 sev=minor trigger=none ac=T5.AC1 at=tools/results.py:114 anchor=DESIGN.md:361 chk=n,n,n,n family=counter-aggregation first=A1 origin=new fix=state the max rule in DESIGN 5.4, or keep it and note it as an adaptation: `hook_ms_p95` takes the worst package p95, not a sum. DESIGN says "Counters are summed over packages except `own_line_jaccard`". Summing p95 values would be meaningless and the docstring comment explains the choice, so this is non-blocking.
F1.4 sev=minor trigger=none ac=T5.AC2 at=tests/test_faults.py:113 anchor=DESIGN.md:397 chk=n,n,n,n family=test-indirection first=A1 origin=new fix=optionally run results.py in the F-3 test and assert collab_counters.observable_moves_executed == 0: F-3's "counted in observable_moves_executed = 0" is checked by recomputing the sum from collab.json slots, not by reading the results.py field. The field uses the same expression (`tools/results.py:93`), so this is non-blocking.
F1.5 sev=minor trigger=none ac=T5.AC2 at=tests/test_faults.py:142 anchor=DESIGN.md:402 chk=n,n,n,n family=test-coverage first=A1 origin=new fix=optionally parametrise test_f8_slo_breach_from_hang over collab 0 and 1: F-8's "same result with collab 0" is covered for `hang_kill` by the runner test (`tests/test_faults.py:39`), but `slo_breach` is asserted only for collab 1. The expression does not depend on collab (`tools/collab_summary.py:327`), so this is non-blocking.
F1.6 sev=minor trigger=none ac=T5.AC1 at=tools/collab_summary.py:220 anchor=DESIGN.md:213 chk=n,n,n,n family=fail-open-audit first=A1 origin=new fix=treat a missing ground-truth.json as a hard failure (or record it in audit.json): the 12-character ground-truth audit is skipped silently when `<a1>/<pkg>/ground-truth.json` is absent, for example when `--a1` points at a wrong path. With the default A1DIR the three real files exist, so this is non-blocking.
F1.1 resolved
F1.2 resolved
