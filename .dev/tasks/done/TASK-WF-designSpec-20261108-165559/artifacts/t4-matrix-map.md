# Task 4 evidence: FR-100 matrix map

File: `tests/hooks/test_launch_level_pre_push.py`. Line numbers are the `def` lines.
Matrix source: `.dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md` (FR-100 table, FR-101 leak pins).
Actors are `governed` (a real launch job from the selector's `prepare`/`run`), `unknown` (that job with its record damaged, or a planted record) and `human` (no job). Every push snapshots the remote with `for-each-ref` before and after.

| T-ID | Test function | Line | Status | Requirement / AC |
|---|---|---|---|---|
| T-01 | `test_t01_create_protected_ref` | 422 | pass (6) | FR-100 T-01; AC-1, AC-2 (refused, remote unchanged; human allowed); AC-3/OD-2 |
| T-02 | `test_t02_fast_forward_update` | 431 | pass (6) | FR-100 T-02; AC-1, AC-2, AC-3 |
| T-03 | `test_t03_delete` (`:main` and `--delete`) | 439 | pass (6) | FR-100 T-03 |
| T-04 | `test_t04_force` (`+src:main` and `--force`) | 452 | pass (6) | FR-100 T-04 |
| T-05 | `test_t05_configured_mapping` (`remote.origin.push` and `push.default=upstream`) | 461 | pass (6) | FR-100 T-05 |
| T-06 | `test_t06_mixed_and_atomic` | 476 | pass (6) | FR-100 T-06 (the whole push is refused) |
| T-07 | `test_t07_exact_name_edges_allowed` | 489 | pass (3) | FR-100 T-07; OD-2 (only the exact refs are protected) |
| T-08 | `test_t08_empty_stream` (up-to-date, stale lease, known non-ff) | 498 | pass (6) | FR-100 T-08 |
| T-09 | `test_t09_fetch_first` | 517 | pass (6) | FR-100 T-09 |
| T-10 | `test_t10_six_field_source` (`HEAD@{0 days ago}`) | 531 | pass (6) | FR-100 T-10; FR-004 (split from the right) |
| T-11 | `test_t11_sha256_repository` | 538 | pass (6) | FR-100 T-11; FR-006 (64-hex oids) |
| T-12 | `test_t12_dry_run` | 548 | pass (6) | FR-100 T-12 |
| T-13 | `test_t13_linked_worktree` | 556 | pass (6) | FR-100 T-13 |
| T-14 | `test_t14_agent_and_human_same_linked_worktree` | 564 | pass (2) | FR-100 T-14 |
| T-15 | `test_t15_release_while_job_live` | 585 | pass (2) | FR-100 T-15 (release while the job is live) |
| T-16 | `test_t16_stale_record` (start ticks, boot id) | 599 | pass (4) | FR-100 T-16; FR-025 (record left byte-identical); FR-008 diagnostic with `rm` line |
| T-16a | `test_t16a_killed_supervisor_orphaned` | 608 | pass (2) | FR-100 T-16a (orphaned, no `rm` line, feature allowed) |
| T-16b | `test_t16b_sibling_session_beside_governed_job` | 618 | pass (2) | FR-100 T-16b |
| T-16c | `test_t16c_group_writable_record_unreadable` | 639 | pass (2) | FR-100 T-16c stand-in (unreadable, no `rm` line); LIM-15 |
| T-16c | `test_t16c_real_second_uid` | 653 | skip here (needs root and setpriv; this environment runs as uid 1000 without root), so UNVERIFIED | FR-100 T-16c optional real second uid: own temp dir, `safe.directory` through GIT_CONFIG_GLOBAL; expects L2-UNKNOWN through the FR-020 data-file owner check (not the record reason), main unchanged, no `rm` line; the record-reason coverage stays with the stand-in above |
| T-STALE-1 | `test_t_stale_1_planted_record_then_rm` | 685 | pass (2) | FR-100 T-STALE-1 (the printed `rm` is run, then the push is allowed) |
| T-17 | `test_t17_human_without_uv_on_path_and_no_store` | 704 | pass (2) | FR-100 T-17; research SC-23 |
| T-18 | `test_t18_invalid_data_file_or_selector` (5 data-file faults, 2 script faults, wrong uv dir, timeout) | 749 | pass (9) | FR-100 T-18; FR-020; FR-022 whys; AC-3/OD-2 (FR-008 diagnostic, feature allowed) |
| T-19 | `test_t19_t19a_malformed_stdin` (governed, unknown) | 793 | pass (2) | FR-100 T-19; FR-006; NFR-010 (no final LF parsed normally; stream over 4096 bytes) |
| T-19 | `test_t19_t19a_ordinary_never_reads_stdin` | 805 | pass (1) | FR-100 T-19/T-19a human column (stdin not read, exit 0) |
| T-19a | `test_t19_t19a_malformed_stdin` | 793 | pass (in T-19 cases) | FR-100 T-19a (malformed after protected wins) |
| T-20 | `test_t20_selector_lines_pinned_and_mapped` | 826 | pass (1) | FR-100 T-20; FR-022; FR-025 |
| T-21 | `test_t21_hardened_selector_call` (a) to (d) | 923 | pass (16) | FR-100 T-21; FR-021 |
| T-22 | `test_t22_pusher_home_elsewhere` | 935 | pass (4) | FR-100 T-22 |
| T-23 | `test_t23_hook_sha256_pinned_with_version_line` | 946 | pass (1) | FR-100 T-23 (pins in `tests/cli/test_install_hooks.py`) |
| T-24 | `test_t24_no_bypass_hint_in_any_refusal` | 954 | pass (1) | FR-100 T-24 (all refusal stderr and current REMEDY values) |
| T-24 | `test_t24_fr045_remedy_text` | 995 | skip: "Task 7: FR-045 W-L2-ABSENT remedy text is not written yet" | FR-045 |
| (Task 8) | `test_hook_placed_by_install_l2` | 988 | skip: "Task 8: the fixture places the hook by install_l2 instead of a test-local copy" | FR-100 fixture placement |
| FR-101 | `test_fr101_bypass_reaches_remote_under_governed_actor` | 1007 | pass (6) | FR-101 leak pins: LIM-4 (`--no-verify`, `-c core.hooksPath`, `--config-env`, `GIT_CONFIG_COUNT`), LIM-6 (`config.worktree` hooksPath), LIM-7 (`git send-pack`) |

```
================== 134 passed, 3 skipped in 89.04s (0:01:29) ===================
```
