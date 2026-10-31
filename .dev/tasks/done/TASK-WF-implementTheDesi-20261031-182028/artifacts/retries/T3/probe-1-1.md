910485d71f37a7bb7cff4f4b65ffaa9c07e5b3cf
## family unspecified-state-key
defect form: a rebuild_state key or fold the design does not describe
command: grep -n -e rereview_watermarks -e watermark src/superclaude/pr_submit/run_log.py tests/pr_submit/test_run_log.py
before:
src/superclaude/pr_submit/run_log.py:173:        ``reviewer_absent`` events; ``rereview_watermarks`` maps each reviewer to
src/superclaude/pr_submit/run_log.py:174:        the ``cycle_id`` and ``watermark`` of its latest ``rereview_requested``
src/superclaude/pr_submit/run_log.py:175:        event that carried a watermark (a missing ``reviewer`` means augment).
src/superclaude/pr_submit/run_log.py:189:            "rereview_watermarks": {},
src/superclaude/pr_submit/run_log.py:210:                if ev.get("watermark") is not None:
src/superclaude/pr_submit/run_log.py:211:                    state["rereview_watermarks"][ev.get("reviewer") or "augment"] = {
src/superclaude/pr_submit/run_log.py:213:                        "watermark": ev["watermark"],
tests/pr_submit/test_run_log.py:233:    for reviewer, watermark in (
tests/pr_submit/test_run_log.py:242:                "watermark": watermark,
tests/pr_submit/test_run_log.py:247:    assert set(state["rereview_watermarks"]) == {"augment", "codex"}
tests/pr_submit/test_run_log.py:248:    assert state["rereview_watermarks"]["codex"]["cycle_id"] == "c1"
coupled sites: run_log.py docstring sentence, state seed, REREVIEW_REQUESTED fold branch; test_run_log.py watermark tuple values and two asserts
after:
(no hits)
