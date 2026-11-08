a71679b8baffe69f6b4fc5cc10faf788beaaf140
family nrm-mr-coverage
defect form: a T-NRM case of MR section 8.2 whose stated expectation (decoded input, or a level) has no test row
command: sed -n 1017,1024p .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md compared with grep -nE 'FS_ONLY|nrm[0-9]' tests/hooks/test_launch_level_guard.py
before-output:
rows T-NRM-1 to 8 compared one by one; gaps: T-NRM-4 (JSON \/ decode), T-NRM-5 push below FS, T-NRM-8 push below FS, T-NRM-2 push below FS; T-NRM-1, 3, 6, 7 and the other T-NRM-5 and T-NRM-8 items already have rows for every level they name
coupled sites: the strict xfail marks must be removed by Task 7 (push) and Task 9 (tamper)
after:
1336:def test_nrm4_json_escaped_slash_decoded(tmp_path, level):
1358:def test_nrm_push_blocked_below_fs(tmp_path, level, command):
