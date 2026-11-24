32b0e98738e39a2ef10629d21ef15a37e01567c5
family=fixture-remote-seed
defect form: a protected branch used in BRANCHES but not seeded on the fixture remote
command: grep -n -F -e refs/heads/master -- tests/hooks/test_launch_level_pre_push.py
before:
135:            "push", "-q", "origin", "HEAD:refs/heads/main", "HEAD:refs/heads/master"
coupled sites: line 134-136 (initial push)
after: line 134-141 now pushes HEAD:refs/heads/integration too; grep -c integration -> 1
