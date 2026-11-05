c966f12a5ee9e1dc2280747d741d4db032ac66a4
family rn4-name-form
defect form: a launch form the plan names for a saved label has no test
search: grep -n -F -e '"--name", "demo"' -e 'CCSESSION_NAME="demo"' tests/unit/test_ccsession_tag.py
before-output: 1532:    env = _orca_env(tmp_path, CCSESSION_NAME="demo")|
coupled sites: test_orca_saved_name_is_listed_and_resumes_at_the_question; test_orca_saved_name_in_ccsession_name_resumes_before_the_prompt
after: 1532:    env = _orca_env(tmp_path, CCSESSION_NAME="demo")|1555:    output, record = _orca_tty(tmp_path, "--name", "demo", "fix it", keys=None)|1560:    assert record["argv"] == [*ORCA_FLAGS, "--name", "demo", "fix it"]|
