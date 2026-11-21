a1b599d43a85246ed89a2421040ce82e35134d50 tree=b550b4e324dfa34ec7ef8ac6e828b3d6de77d475
T7.AC1 met tests/worktree_cleanup/test_git_facts.py:141-237, tests/worktree_cleanup/conftest.py:115-139,183-188
T7.AC2 met tests/worktree_cleanup/conftest.py:50-69, tests/worktree_cleanup/test_git_facts.py:110-135
T7.AC3 met tests/worktree_cleanup/test_git_facts.py:22-46, tests/worktree_cleanup/fixtures/README.md:7-18
T7.AC4 met tests/worktree_cleanup/test_git_facts.py:141-165,167-183,186-225
F1.1 sev=blocking trigger=B4 ac=scope at=tests/worktree_cleanup/conftest.py:67 anchor="runs real `git`, `tar` and `xargs` only inside throwaway folders under `tmp_path`" chk=n,y,n,y family=runner-confinement fix=in RecordingRunner._execute require a real cwd or -C value under the test tmp folder before running git, tar or xargs, and refuse cwd None; add a test first=A1 origin=new: nothing enforces that the recording runner runs real git, tar and xargs only inside throwaway folders.
F1.1 resolved
