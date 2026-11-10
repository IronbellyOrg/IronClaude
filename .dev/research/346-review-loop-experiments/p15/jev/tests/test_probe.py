import json
import os
import pathlib
import secrets
import subprocess
import sys

import pytest

JEV = pathlib.Path(__file__).resolve().parents[1]


def parse_requests(stdout):
    dec = json.JSONDecoder()
    out = []
    for chunk in stdout.split("--- request ")[1:]:
        body = chunk.split("\n", 1)[1]
        obj, _ = dec.raw_decode(body)
        out.append(obj)
    return out


def test_probe_dry_run_prints_three_valid_requests(tmp_path):
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path)}
    p = subprocess.run(["uv", "run", "--no-project", "python", str(JEV / "probe.py"), "--workdir", str(tmp_path)],
                       capture_output=True, text=True, env=env)
    assert p.returncode == 0, p.stderr
    assert "DRY RUN OK" in p.stdout and "RESERVATION estimate" in p.stdout
    assert not (tmp_path / "budget").exists() and not (tmp_path / "journal").exists()      # no network object, no ledger, no key needed
    reqs = parse_requests(p.stdout)
    assert [list(r["questions"]) for r in reqs] == [["arrived_late"], ["delivery_timing", "timing_stated"], ["delivery_timing", "timing_stated"]]
    assert list(reqs[1]["questions"]["delivery_timing"]["criteria"]) == ["early", "on_time", "late"]
    assert list(reqs[2]["questions"]["delivery_timing"]["criteria"]) == ["late", "on_time", "early"]
    from jevlib.questions import build_request
    for r in reqs:
        assert build_request(r["state"], r["questions"]) == r and r["model"] == "jev-1.14.0"


def run_probe_with_mock(tmp_path, monkeypatch, model="jev-1.14.0", flip=False):
    sys.path.insert(0, str(JEV))
    import probe
    from jevlib import transport as T
    monkeypatch.setenv("JEV_API_KEY", "pr0be" + secrets.token_hex(16))
    seen = []

    def script(req):
        seen.append(list(req["questions"].get("delivery_timing", {}).get("criteria", {})))
        body = T.fake_answer(req, 5, 0.6)
        body["model"] = model
        if "delivery_timing" in body["answers"]:
            body["answers"]["delivery_timing"] = {"type": "choice", "choice": "late", "confidence": 0.7,
                                                  "probabilities": {"early": 0.2, "on_time": 0.1, "late": 0.7}}
        if flip and seen[-1] == ["late", "on_time", "early"]:
            body["answers"]["delivery_timing"]["choice"] = "early"
            body["answers"]["delivery_timing"]["probabilities"] = {"early": 0.9, "on_time": 0.05, "late": 0.05}
            body["answers"]["delivery_timing"]["confidence"] = 0.9
        return T.MockStep(200, body)

    monkeypatch.setattr(probe, "UrllibTransport", lambda: T.MockTransport(script))
    monkeypatch.setattr(probe.subprocess, "run", lambda *a, **k: type("P", (), {"stdout": "KEYSCAN OK files=1", "returncode": 0})())
    rc = probe.main(["--live", "--workdir", str(tmp_path)])
    return rc, json.loads((tmp_path / "probe-result.json").read_text()), seen


def test_probe_live_flow_with_mock_transport(tmp_path, monkeypatch, capsys):
    rc, res, seen = run_probe_with_mock(tmp_path, monkeypatch)
    out = capsys.readouterr().out
    assert rc == 0 and res["model_ok"] and res["validator_ok"] and res["order_consistent"] and len(res["latency_ms"]) == 3
    assert seen[1] == ["early", "on_time", "late"] and seen[2] == ["late", "on_time", "early"]          # order reaches the wire
    assert res["usd"] > 0 and (tmp_path / "journal/jev-probe.jsonl").exists() and "Authorization" not in out and "pr0be" not in out


def test_probe_flags_model_drift_and_order_inconsistency(tmp_path, monkeypatch):
    (tmp_path / "a").mkdir(); (tmp_path / "b").mkdir()
    rc, res, _ = run_probe_with_mock(tmp_path / "a", monkeypatch, model="jev-1.13.0")
    assert rc == 1 and res["model_ok"] is False and res["validator_ok"] is False
    rc, res, _ = run_probe_with_mock(tmp_path / "b", monkeypatch, flip=True)
    assert res["model_ok"] and res["validator_ok"] and res["order_consistent"] is False and rc == 0
