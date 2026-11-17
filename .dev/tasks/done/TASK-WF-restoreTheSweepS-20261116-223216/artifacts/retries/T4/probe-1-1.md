a0631eddb02483330971ea8b8975b77010ddb517
family: allowlist-assert
defect form: an allow-list assertion that compares a prefix of the argv, not the whole argv against ALLOWED_ORCA
command: git grep -n -F -e "a[:2]" -- tests/sweep/test_cli_contract.py
before:
tests/sweep/test_cli_contract.py:328:    lists = [a for a in _orca_calls(env) if a[:2] == ("orchestration", "worker-list")]
tests/sweep/test_cli_contract.py:350:    lists = [a for a in proc.argv() if a[:2] == ("orchestration", "worker-list")]
tests/sweep/test_cli_contract.py:1146:    assert {a[:2] for a in asked} <= {
coupled sites: tests/sweep/test_cli_contract.py asked list in test_a_captured_running_worker_is_reported_as_working only
after:
tests/sweep/test_cli_contract.py:328:    lists = [a for a in _orca_calls(env) if a[:2] == ("orchestration", "worker-list")]
tests/sweep/test_cli_contract.py:350:    lists = [a for a in proc.argv() if a[:2] == ("orchestration", "worker-list")]
