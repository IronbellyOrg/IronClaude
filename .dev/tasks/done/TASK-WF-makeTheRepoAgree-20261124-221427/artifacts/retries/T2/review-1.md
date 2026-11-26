32b0e98738e39a2ef10629d21ef15a37e01567c5
tree=8a83270ec519800375a2a8cafe78e3901fd72e69
T2.AC1 unmet: tests/hooks/test_launch_level_pre_push.py:462-466; T2.AC2 unmet: :469-474,:490-498,:501-515 (findings F1.1)
F1.1 sev=blocking trigger=B1 ac=T2.AC2 at=tests/hooks/test_launch_level_pre_push.py:49 anchor="`uv run pytest tests/hooks -q` passes" chk=amiss:y,false:n,harm:n,constraint:n family=fixture-remote-seed fix=seed refs/heads/integration on the remote in the Repo fixture first=A1 origin=new: widened BRANCHES makes t01..t08 fail because remote lacks integration
