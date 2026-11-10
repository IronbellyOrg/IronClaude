873c4222069ec08167ef4153612220811f9fc9db

## family=second-uid-test (F1.1)

- defect form: a root-only second-uid test whose git call cannot reach the hook (git refuses the root-owned repo as dubious ownership because GIT_CONFIG_GLOBAL=/dev/null), so it can never pass when enabled, and the map row claims real second-uid coverage.
- command: `grep -n -e setpriv -e safe.directory -- tests/hooks/test_launch_level_pre_push.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md`
- before:
  - tests/hooks/test_launch_level_pre_push.py:649:    os.geteuid() != 0 or shutil.which("setpriv") is None,
  - tests/hooks/test_launch_level_pre_push.py:650:    reason="T-16c second uid: needs root and setpriv to push as another uid; "
  - tests/hooks/test_launch_level_pre_push.py:659:        ["setpriv", "--reuid=65534", "--regid=65534", "--clear-groups",
  - .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md:28:| T-16c | `test_t16c_real_second_uid` | 653 | skip: "T-16c second uid: needs root and setpriv to push as another uid; the group-writable record above is the stand-in" | FR-100 T-16c with a real second uid |
- coupled sites: tests/hooks/test_launch_level_pre_push.py:93 (fixture GIT_CONFIG_GLOBAL=/dev/null), :663-664 (assertions), src/superclaude/hooks/scripts/launch-level-pre-push.sh:31 (`-O` owner check: a second uid fails the data-file check before any record is read), t4-matrix-map.md:28.
- after:
  - tests/hooks/test_launch_level_pre_push.py:649:    os.geteuid() != 0 or shutil.which("setpriv") is None,
  - tests/hooks/test_launch_level_pre_push.py:650:    reason="T-16c second uid: needs root and setpriv to push as another uid; "
  - tests/hooks/test_launch_level_pre_push.py:663:        # safe.directory is honoured only from global config, and a local push
  - tests/hooks/test_launch_level_pre_push.py:669:            ["setpriv", "--reuid=65534", "--regid=65534", "--clear-groups",
  - t4-matrix-map.md:28: row now says skip here, UNVERIFIED, and that the expected L2-UNKNOWN comes from the FR-020 data-file owner check (hook :31), not the record reason.
  - fix: the git call runs with GIT_CONFIG_GLOBAL pointing to a file with `[safe] directory = *` (:664-672), overriding the fixture's /dev/null (:93) for this one call; assertions add "no `rm '`" and keep main unchanged (:675-677).

## family=second-uid-test-chmod (F2.1)

- defect form: a test widens permissions on paths it does not own (every parent of its temp dir up to /tmp, including pytest's shared base temp dirs).
- command: `grep -n -e .chmod( -e parents -- tests/hooks/test_launch_level_pre_push.py`
- before (only the second-uid lines are in the family; the rest chmod paths the fixture created under its own temp dir):
  - tests/hooks/test_launch_level_pre_push.py:654:    for path in [repo.tmp, *repo.tmp.parents]:
  - tests/hooks/test_launch_level_pre_push.py:657:        path.chmod(path.stat().st_mode | 0o055)
  - other hits: :26 (REPO parents, read only), :84, :85, :89, :107, :124, :181, :189, :223, :229, :241, :308, :310, :698, :711, :811, :815, :826, :879, :890, :898 (all on fixture-created paths under the test temp dir).
- coupled sites: tests/hooks/test_launch_level_pre_push.py:78-80 (Repo takes its temp dir), :653 (test signature uses the shared `repo` fixture).
- after (lines 640-690 only; other hits unchanged and fixture-owned, those after :653 shifted by +17):
  - tests/hooks/test_launch_level_pre_push.py:657:        top.chmod(0o755)
  - tests/hooks/test_launch_level_pre_push.py:659:        repo.tmp.chmod(0o755)
  - tests/hooks/test_launch_level_pre_push.py:662:                path.chmod(path.stat().st_mode | (0o055 if path.is_dir() else 0o044))
  - tests/hooks/test_launch_level_pre_push.py:667:        config.chmod(0o644)
  - no `parents` hit in the test any more; every chmod is on a path under the test's own mkdtemp dir (:655), removed in finally (:680).
