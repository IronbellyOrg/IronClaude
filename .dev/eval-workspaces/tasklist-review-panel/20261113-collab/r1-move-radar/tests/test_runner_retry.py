"""T-13: retry isolation and no fallback (R-44, NOFALLBACK)."""

from conftest import finding, jload, json_reply, report


def test_no_block_then_isolated_retry(runner):
    runner.settings("t2b-1")
    runner.plan(f"replay {runner.file(json_reply('no block here'))}", f"replay {runner.file(json_reply(report(finding())))}")
    r = runner.run(collab=1)
    assert r.returncode == 0, r.stderr
    assert "--settings" in runner.argv(1) and "--settings" not in runner.argv(2)
    m = runner.meta()
    assert m["retry_isolated"] is True and m["attempts"] == 2 and m["valid"] is True and m["retry_s"] is not None
    c = jload(runner.d / "reviews" / "t2b-1.cost.json")
    a1 = jload(runner.d / "reviews" / "t2b-1.attempt1.meta.json")
    a2 = jload(runner.d / "reviews" / "t2b-1.attempt2.meta.json")
    assert c["attempts"] == 2 and c["total_wall_s"] == (a1["wall_ms"] + a2["wall_ms"]) / 1000
    assert c["total_output_tokens_all"] == 200


def test_misroute_twice_invalid_no_fallback(runner):
    f = runner.file(json_reply(report(finding())))
    runner.plan(f"misroute {f}")
    r = runner.run(collab=0)
    assert r.returncode == 1
    assert runner.calls() == 2  # no third attempt
    for k in (1, 2):
        a = runner.argv(k)
        assert a[a.index("--model") + 1] == "muse-ember-1.0"  # no other model is ever invoked
    m = runner.meta()
    assert m["valid"] is False and m["model_ok"] is False and m["observed_model"] == "gpt-6.1-sol"


def test_refuses_without_nofallback(runner):
    runner.env.pop("NOFALLBACK")
    assert runner.run(collab=0).returncode == 2 and runner.calls() == 0
