"""The reviewer's own tool-result overflow file is not a forbidden read; another project's folder still is (2026-11-14 false-alarm fix)."""
from r5 import audit

OWN = '{"file_path":"/home/coder/.claude/projects/-tmp-evalsb-collab-r5-TASK-WF-makeTheAliasOnly-20261105-051649-repo/26c53456-a424-455d-bb6c-ce1a3eb103fb/tool-results/ba2c10zeb.txt"}'
OTHER = '{"file_path":"/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-other/26c53456-a424-455d-bb6c-ce1a3eb103fb/x.jsonl"}'
OTHER_R5 = '{"file_path":"/home/coder/.claude/projects/-tmp-evalsb-collab-r5-TASK-WF-x-repo/26c53456-a424-455d-bb6c-ce1a3eb103fb/other-session.jsonl"}'


def _hits(s):
    s = audit.OWN_OVERFLOW.sub("", s)
    return [f for f in audit.FORBIDDEN if f in s]


def test_own_overflow_is_allowed():
    assert _hits(OWN) == []


def test_other_projects_stay_forbidden():
    assert ".claude/projects" in _hits(OTHER)
    assert ".claude/projects" in _hits(OTHER_R5)
