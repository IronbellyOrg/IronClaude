# Final gate: fix report (cycle 1)

Single fix agent (`rf-qa`, `fix_authorization: true`). Input: `qa/final/qa-consolidated-findings.md`, blocking findings F-1 to F-10. Minor findings F-11 to F-51 were not touched.

## Per-finding fixes

| id | Files changed | What changed |
|---|---|---|
| F-1 | `tests/issue_watch/test_cli.py` (the `secret = "issue title ..."` line in `test_once_turns_an_unexpected_exception_into_exit_1_and_one_fallback_line`), `tests/issue_watch/test_cycle.py` (`secret = "SECRET-PROJECT-VALUE"` in `test_load_config_error_detail_never_echoes_the_value__fr027`), `tests/issue_watch/test_origin_parity.py` (the `https://user:token@github.com/...` parametrize row, now a multi-line tuple as `ruff format` requires); `phase-outputs/reports/final-gate-record.md`, `phase-outputs/reports/final-change-set.md` (section 5 statement) | The three lines carry the repo's own convention `# pragma: allowlist secret` (same form as `tests/cli/test_install_mcp_tavily.py:137`); test meaning and assertions unchanged. `.secrets.baseline` is untouched. The false "hook-equivalent" sentence is replaced: G-11 covers only whitespace, CR and the final newline; the record has a new "Final-gate fix pass" table with G-12 (detect-secrets) and G-13 (markdownlint) results. |
| F-2 | `docs/designs/issue-watcher-setup.md` (section 5 text after the `init-state` block; section 10.1 item "6."; the `store_missing` and `lock_missing` rows of the exit-6 table in 10.2; the first sentence of section 11.5) | Experiment on a /tmp copy (`/tmp/f2exp`, config with `state_dir` missing, then present without a lock): `once --dry-run` printed `cycle: lock_missing`, exit 6 in both cases. Runbook now says a cycle before `init-state` ends `lock_missing` (the cycle takes the lock before it reads the store); `store_missing` only when the lock exists and `dispatch.json` does not (`record.py:357-358`, `392-397`); a new-setup `lock_missing` goes to `init-state`; `store_missing`, `store_invalid`, `lock_invalid` and a `lock_missing` where the directory still exists go to section 11. Also stated: `init-state` refuses when either file exists (`record.py:773-775`). |
| F-3 | `docs/designs/issue-watcher-setup.md` (section 10.1 "Precedence") | Removed the "7 with 5 / 7 with 3 occur in practice, both audited" claim. The text now states the precedence rule, that a 7 (a `failed` entry, `launch_unknown`, `spawn_error`) ends the cycle's work (`cycle.py:813-815`, `_fail`/`_cond` calls only inside `_launch`, lines 1026, 1030, 1071, 1074) so no `gh` call or rate-limit stop can follow it, and that only a 6 can still follow (the final write), and then 6 wins. |
| F-4 | `phase-outputs/reports/deviation-register.md` (DF-05 row, Table 3 note), `phase-outputs/reports/final-change-set.md` (section 7 DF-05 row; section 5 pre-commit statement), `phase-outputs/reports/ac-trace.md` (last paragraph of the Result section) | DF-05 row and note now say the sentence "full suite: CI only" is in `final-gate-record.md` line 20 (verified); the `final-change-set.md` DF-05 verdict quotes the register text verbatim; the stale `ac-trace.md` paragraph now says Steps 9.4 to 9.16 were re-run after the docstring edits (p9 result mtimes 02:20:30 to 02:21:16 follow the edits, last edit 02:16:15). The register already held the 59-name count and the Python 3.10.20 fact (Table 2 rows 1 and 9; verified, unchanged). |
| F-5 | `tests/issue_watch/test_cli.py` (new helper `_launched_like` and test `test_status_retry_lists_only_unknown_entries_with_an_id_and_a_cwd__ac9_fr015`) | New store with `launched`, `claimed`, `abandoned` (`claim_not_observed`) entries each carrying an operation id and a cwd, plus one `unknown` control. Asserts the JSON `retry` list holds only the `unknown` entry and the text form prints one `run from` block and none of the other ids. |
| F-6 | `tests/issue_watch/test_cycle.py` (two tests after `test_an_issue_that_was_not_examined_keeps_its_old_stamp__fr023`: `test_an_idle_cycle_does_not_prune_the_considered_map__fr023`, `test_an_all_budget_exhausted_cycle_does_not_prune_the_considered_map__fr023`) | Seed `considered` with entries outside the discovery set; an idle cycle (discovery empty, cycle still saves) and a cycle whose only candidate is `budget_exhausted` must leave `considered` unchanged. |
| F-7 | `tests/issue_watch/test_cycle.py` (`test_a_saving_cycle_prunes_the_consumed_log__design_7_5`) | Seed `consumed_log = (now - 24h, now - 24h + 1s)`, assert both survive the seed, run a saving cycle, assert only the later time remains. |
| F-8 | `tests/issue_watch/test_cli.py` (`test_once_exits_2_on_an_unsupported_platform_and_runs_nothing__design_4_1`, parametrized `real` and `dry_run`) | `sys.platform = "darwin"`, `build_deps` and `cycle.run_cycle` replaced by recorders: exit 2, one `platform_unsupported` fallback line, no call recorded, no file under `tmp_path` changed. No `skip`, no chmod, no root guard. |
| F-9 | `tests/issue_watch/test_record.py` (`test_ac11_lock_replaced_or_unlinked_after_flock_is_lock_held__fr017`: new `swap` value `rename_aside`, docstring added) | After the flock the lock is renamed to `lock.aside` and a fresh empty file is written at the path, so `st_nlink` stays 1 and the path stat succeeds: only the `(st_dev, st_ino)` comparison raises `LockHeld`. Afterwards a normal `hold` on the new file works. No source change. |
| F-10 | `docs/designs/issue-watcher-setup.md` (section 14.1, last paragraph) | Removed the "single `once` with `enabled` set to `true`" option. The text now says: launch the test by hand with the Orca CLI while `enabled` is still `false`, say how in the record; a real `once` examines up to 10 candidates and launches the first eligible one, which need not be the test issue; the 8.6 safeguards (list issues with both labels, keep the kill switch at hand) apply only after the test has passed; `enabled` changes to `true` only in section 8.6. Now consistent with sections 0, 8.5 and 8.6. |

## Mutants re-run on a /tmp copy (`/tmp/mut`, a copy of `src/` and `tests/issue_watch/`; the repo was never mutated)

| Finding | Mutant (as named in the finding) | Result on the copy |
|---|---|---|
| F-5 | Q19: `if entry.operation_id and entry.launch_cwd:` | KILLED: `test_status_retry_lists_only_unknown_entries_with_an_id_and_a_cwd__ac9_fr015` fails |
| F-6 | C49/V19: `if self.discovered is not None:` | KILLED: `test_an_idle_cycle_does_not_prune_the_considered_map__fr023` fails (stale entry 5 pruned) |
| F-7 | V21: `self.doc = doc` | KILLED: `test_a_saving_cycle_prunes_the_consumed_log__design_7_5` fails (the expired time survives) |
| F-8 | K13: `_load_config(config_path, platform=False)` in `once_command` | KILLED: both `real` and `dry_run` cases of the new test fail (exit is not 2) |
| F-9 | R4/R20: inode compare replaced by `pass` and by `if False:` | KILLED (both forms): `...[rename_aside]` fails with `DID NOT RAISE LockHeld`; the `replace` and `unlink` cases still pass, as before |

After the runs `diff -r src /tmp/mut/src` printed no difference, so the copy was restored, and `git status` shows no change to `src/` besides the existing `main.py` registration and the new package.

## Final results

| Check | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` | 2635 passed, 0 skipped (2628 before plus 7 new cases), as a non-root user |
| `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto -q tests/issue_watch/` | 2635 passed |
| G-2 command (issue_watch plus the five registration test files) | 2665 passed, 1 skipped (the pre-existing `tests/swarm/test_cli_registration.py:127`) |
| `make lint` | exit 0 (0 errors, 5 pre-existing warnings, `ruff check .` all passed) |
| `uvx --offline ruff@0.15.20 check` on `src/superclaude/cli/issue_watch`, `tests/issue_watch`, `main.py` | All checks passed |
| `uvx --offline ruff@0.15.20 format --check` on the same paths, and on `src/ tests/` | 31 files and 1234 files already formatted (`test_origin_parity.py` first failed, then was reshaped; now clean) |
| detect-secrets-hook 1.5.0 (offline, `uvx --offline --from detect-secrets`) over the 49 `.py`/`.json` files of the package and tests plus `main.py` and both design documents, with a /tmp copy of `.secrets.baseline` whose version stamp was changed 1.4.0 to 1.5.0 (the repo baseline is untouched; run against the repo copy directly, the tool exits 3 only to rewrite that version stamp) | exit 0. The three fixed files alone, with no baseline: exit 0. Negative control (`secret = "SECRET-PROJECT-VALUE"` in a /tmp file): exit 1 "Secret Keyword" |
| markdownlint 0.38.0 (`~/.cache/pre-commit/reposcxph1ch/node_env-system/bin/markdownlint`) with the repo `.markdownlint.json`, on a /tmp copy of the runbook, no `--fix` | exit 0 |
| `uv run superclaude issue-watch --help` | lists exactly check-config, init-state, once, reset, status |
| whitespace, CR and final-newline check on the four changed test files and the runbook | no hit |
| `git status` for `pyproject.toml`, `Makefile`, `.github`, `.claude`, `.secrets.baseline` | no change |

Not touched: the task file, `docs/designs/issue-watcher.md`, the spec, research files, `pyproject.toml`, `Makefile`, workflows, `.claude/`. Minor findings F-11 to F-51 are unchanged notes. The `.pyc`-free /tmp scratch (`/tmp/mut`, `/tmp/f2exp`, `/tmp/mut_run.sh`, baseline copies) is outside the repo.
