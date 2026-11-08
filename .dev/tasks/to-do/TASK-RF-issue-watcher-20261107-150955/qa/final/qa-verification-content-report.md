# QA Report: Final gate content verification (cycle 1)

**Topic:** issue-watch implementation, Final gate, fix cycle 1
**Date:** 2026-11-08
**Phase:** fix-cycle (content verification, report-only, `fix_authorization: false`)
**Fix cycle:** 1

---

## Overall Verdict: PASS

All ten blocking findings (F-1 to F-10) are FIXED. No assertion was weakened or deleted, no skip was introduced, and no new blocking content issue was found. Minor notes are listed at the end and never fail the review.

## Blocking findings

| id | Result | Evidence (what I ran or read myself) |
|---|---|---|
| F-1 detect-secrets | FIXED | `# pragma: allowlist secret` is on `tests/issue_watch/test_cli.py:633`, `test_cycle.py:381` and `test_origin_parity.py:55`. I ran `uvx --offline --from detect-secrets detect-secrets-hook --baseline </tmp copy with version 1.5.0>` over the 51 untracked `.py`/`.json`/`.md` files of the package, tests and `docs/designs/` plus `main.py`: exit 0. The strings and the assertions around them are unchanged (`assert secret not in error.detail`, `assert secret not in result.output`); the parametrize row in `test_origin_parity.py` keeps its expected value `None`. `final-gate-record.md` line 21 no longer claims G-11 stands in for the hooks (it says G-11 covers whitespace, CR and the final newline only) and has G-12 and G-13 rows. `git diff` of `.secrets.baseline` against HEAD is empty (its mtime is newer, the bytes equal HEAD). |
| F-2 runbook lock_missing vs store_missing | FIXED | Runbook lines 156, 336, 398-399, 529 now say: before `init-state` a cycle ends `lock_missing`; `store_missing` only when the lock exists and `dispatch.json` does not. I replayed it on /tmp dirs with the copied package: a missing dir and an empty dir give `LockError lock_missing`; a dir holding only `lock` gives lock ok then `StoreError store_missing`; `init_state` on the lock-only dir raises `StateExists`; on an empty dir it creates the state. This matches `cycle.py:663-683` (lock taken before `_load` at line 695), `record.py:392-397`, `record.py:357-358` and `record.py:773-775`, and `cli.py:208-210` (exit 6 with "a store already exists"). |
| F-3 runbook precedence | FIXED | Line 340 no longer claims "7 with 5 / 7 with 3 occur". It states the precedence rule and that a 7 ends the cycle's work. Code check: the only `_cond` calls for 7 are `_fail` (`cycle.py:1002`, called at 1026 and 1030) and `launch_unknown` / `spawn_error` (1071, 1074), all inside `_launch`, which sets `c.launching = True` (1009); `_candidates` then sets `self.halt` (814-815) and breaks the loop (797-798). Nothing in `_steps` after `_candidates` (704-718) calls GitHub, and only `_commit` can still add a 6. Claim true. |
| F-4 stale report statements | FIXED | `deviation-register.md` line 13 (DF-05 row) and line 60 (Table 3 note) now point at `final-gate-record.md` line 20; I read that line: "- full suite: CI only (the whole `make test` run is left to CI, decision DF-05)." `final-change-set.md` line 178 quotes the register verbatim ("PASS (the literal sentence is in final-gate-record.md line 20)"). `ac-trace.md` line 91 now says Steps 9.4 to 9.16 were re-run after the docstring edits. No "does not exist yet" or "pending Step" remains in the three files (grep). |
| F-5 retry only for unknown | FIXED | New `test_status_retry_lists_only_unknown_entries_with_an_id_and_a_cwd__ac9_fr015` (`test_cli.py:885`). Seeds `launched`, `claimed`, `abandoned(claim_not_observed)` entries that each carry an operation id and a cwd, plus one `unknown`; asserts the exact `counts`, the exact one-element `retry` list (issue, operation_id, cwd, argv), and in the text form `retry: 1`, one `run from`, none of `op-5/6/7`. I replayed mutant Q19 (`cycle.py:1271` without `entry.state == "unknown" and`) on a /tmp copy: the new test FAILS. A second mutant (`entry.state != "launched" and ...`) also FAILS. Design 10.2 and AC-9 are exercised. |
| F-6 considered not pruned on idle | FIXED | New `test_an_idle_cycle_does_not_prune_the_considered_map__fr023` (`test_cycle.py:3609`) and `test_an_all_budget_exhausted_cycle_does_not_prune_the_considered_map__fr023` (3638). Both seed `considered` entries outside the discovery set and assert the map is unchanged, and the idle test also asserts the cycle did save (`last_completed_cycle_at == CYCLE_NOW`), so the test cannot pass by "nothing was written". Mutant C49/V19 (`cycle.py:1097` reduced to `if self.discovered is not None:`): BOTH tests FAIL. |
| F-7 consumed_log pruning | FIXED | New `test_a_saving_cycle_prunes_the_consumed_log__design_7_5` (`test_cycle.py:3623`): seed `(now-24h, now-24h+1s)`, assert the seed holds both, run a saving cycle, assert only the later time remains (boundary `t <= now-24h` per design 7.5). Mutant V21 (`cycle.py:1105` `self.doc = doc`): FAILS. |
| F-8 once on another platform | FIXED | New `test_once_exits_2_on_an_unsupported_platform_and_runs_nothing__design_4_1` (`test_cli.py:655`), parametrized real and dry-run: `sys.platform = "darwin"`, `build_deps` and `cycle.run_cycle` replaced by recorders, asserts exit 2, the `platform_unsupported` fallback line and `calls == []`. No skip, no root guard. Mutant K13 (`cli.py:120` `_load_config(config_path, platform=False)`): both cases FAIL (the `check-config` cases still pass, as expected). Design line 69 honoured. |
| F-9 lock inode compare | FIXED | `test_ac11_lock_replaced_or_unlinked_after_flock_is_lock_held__fr017` (`test_record.py:791`) gained `rename_aside`: the lock is renamed to `lock.aside` and a fresh file is written at the path (so `st_nlink` stays 1 and the path stat succeeds); the old `replace` and `unlink` cases are kept with their assertions (`LockHeld`, `done == [True]`, follow-up `hold` or `lock_missing`). Mutant R4/R20 (`record.py:411` condition replaced by `if False:`): the `rename_aside` case FAILS with `DID NOT RAISE LockHeld`, `replace` and `unlink` still pass. Design 7.6 lock identity is now pinned. No source change. |
| F-10 runbook 14.1 vs 0/8.5/8.6 | FIXED | Line 587 (14.1) no longer offers a real `once` with `enabled: true` before the live test. It says: launch the test by hand with the Orca CLI while `enabled` is `false`; do not run a real `once` with `enabled` true for the test, because a cycle examines up to 10 candidates and launches the first eligible one (checked: `MAX_CANDIDATES = 10` at `cycle.py:34`, used at 717; `halt` after the first launch, 814-815); the 8.6 safeguards apply only after the test has passed; `enabled` changes to `true` only in 8.6. I read lines 5, 270-282, 307, 580-587 together: they now agree (enabled stays `false` until the committed live-test record; 8.6 is the only place it flips; 8.6 keeps "list the issues carrying both labels first, keep the kill switch at hand"). |

## Checks requested beyond the finding rows

| Check | Result | Evidence |
|---|---|---|
| Fix only silences tests or rewords text? | No | Each of the five code-side findings gained a test that fails on the cited mutant, replayed by me on /tmp copies (`/tmp/qv`, a copy of `src/superclaude` and `tests/`; the repo was never mutated; after the run `diff -r` of the copy against the repo package printed no difference). The shipped source is unchanged: `find -newer qa-consolidated-findings.md` lists only `test_cli.py`, `test_record.py`, `test_cycle.py`, `test_origin_parity.py`, the runbook, the three report files and the task file (plus caches); no file under `src/` changed. |
| No assertion weakened or deleted | Confirmed | Test functions went from 844 (the `ac-trace.md` figure) to 849 (`grep -c "def test_"`): exactly the five new functions. Collected cases went from 2628 to 2635: 2 (platform) + 1 (`rename_aside`) + 1 (retry) + 1 (idle) + 1 (budget) + 1 (prune) = 7. Nothing was removed. The edited existing tests keep every prior assertion (read: `test_origin_parity.py` row, `test_cli.py:633`, `test_cycle.py:381`, `test_record.py:790-828`). |
| No skip introduced | Confirmed | Skip markers: `test_cli.py:967, 1070`, `test_record.py:739`, `test_cycle.py:735, 4688`; the same five sites as the F-11 inventory (line numbers only moved by the inserted tests). I ran the full `tests/issue_watch/` on the unmutated copy as uid 1000: 2635 passed, no skip, no failure. |
| Every test the reports cite still exists | Confirmed | I extracted all 1000 distinct `test_*` names from `ac-trace.md`, `deviation-register.md`, `final-gate-record.md` and `final-change-set.md` and matched them against `tests/issue_watch/`; the only three misses (`test_cli_registration`, `test_model_alias_policy`, `test_retired_docs_absent`) are the G-2 files that live in `tests/cli`, `tests/swarm`, `tests/recommend`, `tests/skills`, `tests/docs` (Glob confirmed). |
| AC trace and register still match the code | Yes, with minor stale counts (note M-1) | The 25 AC rows, 29 FR rows and 14 NFR rows name tests that exist and pass; behaviour claims checked against `cycle.py`, `record.py`, `cli.py` above. |
| New blocking content issue (wrong behaviour, false claim, missing deliverable, security or data-loss risk) | None found | The new tests only add assertions on shipped behaviour; the runbook edits were checked against code line by line (rows above); `final-gate-record.md` gains G-12 and G-13 with the true results (I reproduced G-12; G-13 not re-run here, it is a structural lens item). |

## Minor notes (not blocking, not rechecked in later rounds)

- M-1. `ac-trace.md` line 5 ("all 844 test functions", "2628 passed" from `p9-g1`) and `final-change-set.md` lines 72, 118-120 (2628 / 2658) plus its per-file line counts (for example `test_cli.py` 1593) describe the pre-fix snapshot and are dated to their own steps; the tree now has 849 functions and 2635 passed. `final-gate-record.md` records both states. Refresh the counts when Step 9.F13 re-runs G-1 to G-11 and overwrites `p9-*`. Line anchors in the register for `test_cli.py` (after line 654), `test_cycle.py` (after 3608) and `test_record.py` (after 790) moved by the inserted tests (moved line numbers on true claims).
- M-2. Runbook line 587 says "The design says only 'one owner-run launch on a test issue'"; that wording is FU-1 in `spec-final.md:400`, not in `docs/designs/issue-watcher.md` (line 33 says "owner-run live test"). Same attribution class as F-17.
- M-3. Runbook line 336 sends "a `lock_missing` that appears where the directory still exists" to section 11. On a new setup an existing but empty directory also gives `lock_missing`, and `init-state` handles it directly (verified: creates the state in an empty directory). Section 11.5 also works, just heavier. Wording only.
- M-4. `.secrets.baseline` has a newer mtime (03:10) than the consolidation but is byte-identical to HEAD (git reports no change).
- M-5. markdownlint (G-13) was not re-run by me; it is a structural lens item.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No inherited structural verdict was supplied in the spawn prompt; I relied on the structural verifier (Step 9.F11) for Python 3.10 compatibility, `make lint`, pinned-ruff and `issue-watch --help` results and did not re-run them.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Mutant replay of Q19, V19/C49, V21, K13, R4/R20 (plus a second Q19 variant) on a /tmp copy, each run only against the new test: all killed (`/tmp/qv_mut.sh` output: Q19 1 failed, Q19b 1 failed, V19 2 failed, V21 1 failed, K13 2 failed, R4 `rename_aside` failed with `DID NOT RAISE LockHeld`). The extra variant R4b (`not ... ==`) is the same condition written another way, so it passing is expected and is not a survivor.
- Runbook F-2/F-3/F-10 claims re-derived from `cycle.py:663-718, 797-815, 999-1075`, `record.py:347-414, 755-802`, `cli.py:201-214` and an executed /tmp experiment.
- detect-secrets hook re-run on the change set (exit 0).
- Full `tests/issue_watch/` suite on the unmutated copy: 2635 passed, 0 skipped.

**Confidence:** Verified: 10 findings + 6 extra checks = 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 24 | Grep: 9 | Glob: 1 | Bash: 10 (the mutant batch, suite run, detect-secrets and experiment are the load-bearing ones)
**Web research:** none performed (no Tavily or fallback call).

## QA Complete
