"""2026-11-14 false-alarm fixes: a reviewer's own overflow file is not a forbidden read, and judge_ok looks at the final result only."""
import json

from r3lib import metrics

OWN = '{"file_path":"/home/coder/.claude/projects/-tmp-evalsb-collab-r3-TASK-WF-makeTheAliasOnly-20261105-051649-repo/02b16972-6c8f-4f34-9061-692c9b26bc28/tool-results/bgd9a1ypa.txt"}'
OTHER = '{"file_path":"/home/coder/.claude/projects/-tmp-evalsb-collab-r3-TASK-WF-x-repo/02b16972-6c8f-4f34-9061-692c9b26bc28/other.jsonl"}'


def test_own_overflow_allowed_other_forbidden():
    assert "/.claude/projects/" not in metrics.OWN_OVERFLOW.sub("", OWN)
    assert "/.claude/projects/" in metrics.OWN_OVERFLOW.sub("", OTHER)


SCORE = {k: 1 for k in ("label", "combo", "package", "gt_total", "gt_covered_any", "gt_covered_blocking", "ledger_rows_total",
                        "ledger_rows_blocking", "blocking_rows_gt_matched", "wrong_blockers", "notes")}


def _judge(tmp_path, events):
    (tmp_path / "score.json").write_text(json.dumps(SCORE))
    (tmp_path / "judge.json").write_text(json.dumps(events))
    return metrics.judge_ok(tmp_path)


def test_failed_tool_call_inside_a_good_judge_is_ok(tmp_path):
    ev = [{"type": "user", "message": {"content": [{"type": "tool_result", "is_error": True, "content": "x"}]}},
          {"type": "result", "is_error": False, "result": "score.json written"}]
    assert _judge(tmp_path, ev) is True


def test_error_result_is_not_ok(tmp_path):
    assert _judge(tmp_path, [{"type": "result", "is_error": True, "result": "API Error: 500"}]) is False
