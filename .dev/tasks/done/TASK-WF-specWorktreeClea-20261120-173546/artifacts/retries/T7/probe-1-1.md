a1b599d43a85246ed89a2421040ce82e35134d50
family: runner-confinement
defect form: a real process (git, tar or xargs) can start with a working folder outside the test tmp folder
command: grep -n -E "super\(\)\._execute|real_git|def _execute" tests/worktree_cleanup/*.py
before:
tests/worktree_cleanup/conftest.py:46:    ``real_git`` is true (on throwaway folders only). A command with no canned reply
tests/worktree_cleanup/conftest.py:52:            self, replies=None, real_git=True, evidence_dir=None, landed_paths=(LANDED,)
tests/worktree_cleanup/conftest.py:58:            self.real_git = real_git
tests/worktree_cleanup/conftest.py:60:        def _execute(self, argv, cwd, stdin):
tests/worktree_cleanup/conftest.py:67:            if prog in ("git", "tar", "xargs") and self.real_git:
tests/worktree_cleanup/conftest.py:68:                return super()._execute(argv, cwd, stdin)
tests/worktree_cleanup/conftest.py:86:        def _execute(self, argv, cwd, stdin):
tests/worktree_cleanup/test_facts.py:295:        def _execute(self, argv, cwd, stdin):
coupled sites: RecordingRunner._execute at conftest.py:60 is the only real-process path; the never-run Guard at conftest.py:86 and the Fails runner at test_facts.py:295 never reach a real process; tests that pass cwd None to a real call (none expected, the full run shows any)
after:
tests/worktree_cleanup/conftest.py:46:    ``real_git`` is true (on throwaway folders only). A command with no canned reply
tests/worktree_cleanup/conftest.py:52:            self, replies=None, real_git=True, evidence_dir=None, landed_paths=(LANDED,)
tests/worktree_cleanup/conftest.py:58:            self.real_git = real_git
tests/worktree_cleanup/conftest.py:60:        def _execute(self, argv, cwd, stdin):
tests/worktree_cleanup/conftest.py:67:            if prog in ("git", "tar", "xargs") and self.real_git:
tests/worktree_cleanup/conftest.py:68:                self._require_throwaway(argv, cwd)
tests/worktree_cleanup/conftest.py:69:                return super()._execute(argv, cwd, stdin)
tests/worktree_cleanup/conftest.py:72:        def _require_throwaway(self, argv, cwd):
tests/worktree_cleanup/conftest.py:117:        def _execute(self, argv, cwd, stdin):
tests/worktree_cleanup/test_facts.py:295:        def _execute(self, argv, cwd, stdin):
