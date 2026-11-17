a0631eddb02483330971ea8b8975b77010ddb517 tree=a3c699ad6101b6f799a1bdd97fcaa7142923341f
T4.AC1 met tests/sweep/test_cli_contract.py:1138
T4.AC2 met tests/sweep/test_cli_contract.py:1118-1160
T4.AC3 met tests/sweep/test_cli_contract.py:1094-1095
F1.1 sev=blocking trigger=B4 ac=scope at=tests/sweep/test_cli_contract.py:1142-1148 anchor="assert the recorded argv list contains no template outside ALLOWED_ORCA" chk=n,n,n,y family=allowlist-assert fix=check each recorded argv with probes.check_orca_argv first=start origin=new: the test checks only that the first two tokens are one of four verbs; a worktree ps --agent-wait call would still pass
F1.1 resolved
