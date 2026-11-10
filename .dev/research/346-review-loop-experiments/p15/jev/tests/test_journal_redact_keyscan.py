import json
import os
import pathlib
import subprocess
import sys

import pytest

from jevlib.budget import Budget
from jevlib.client import JevClient
from jevlib.journal import Journal
from jevlib.questions import build_request, noul
from jevlib.redact import redact
from jevlib.transport import MockStep, MockTransport, TransportTimeout, fake_answer

JEV = pathlib.Path(__file__).resolve().parents[1]
KEY = "FAKEJEVKEY-" + "Z9" * 15
QS = {"q": noul("Is it so?", "It is so.", "It is not so.")}
ST = {"m": "hello"}


def client(tmp_path, steps):
    b = Budget(tmp_path / "b.json", ceiling_usd=1.0, ceiling_input_tokens=10**7)
    t = MockTransport(steps)
    return JevClient(experiment="T", phase="probe", budget=b, journal=Journal(tmp_path / "j" / "jev-probe.jsonl"),
                     transport=t, live=True, sleep=lambda s: None), t


def good():
    return fake_answer(build_request(ST, QS), 2, 0.4)


def test_journal_records_exact_request_and_no_headers(tmp_path, monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", KEY)
    c, t = client(tmp_path, [MockStep(200, good())])
    r = c.ask(ST, QS, case_id="a", qset_version="v1", data_classes={"synthetic"}, purpose="t")
    recs = [json.loads(x) for x in (tmp_path / "j" / "jev-probe.jsonl").read_text().splitlines()]
    assert recs[-1]["final"] and recs[-1]["request"] == build_request(ST, QS)
    assert recs[-1]["request_sha256"] == r.request_sha256
    for rec in recs:
        assert "headers" not in rec and "Authorization" not in json.dumps(rec)
        assert rec["schema"] == "jev-journal/1" and rec["experiment"] == "T"
    assert recs[0]["http_status"] == 200 and recs[0]["response_raw"]


def test_redact_replaces_key_everywhere(tmp_path, monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", KEY)
    steps = [MockStep(200, good()),
             MockStep(401, {"detail": f"bad key {KEY}"}),
             MockStep(500, f"echo {KEY}"), MockStep(500, f"echo {KEY}"),
             MockStep(exc=TransportTimeout(f"timeout {KEY}")), MockStep(exc=TransportTimeout(KEY)),
             MockStep(200, f"not json {KEY}")]
    c, t = client(tmp_path, steps)
    from jevlib.client import KeyRejected
    c.ask(ST, QS, case_id="1", qset_version="v", data_classes={"synthetic"}, purpose="t")
    with pytest.raises(KeyRejected):
        c.ask(ST, QS, case_id="2", qset_version="v", data_classes={"synthetic"}, purpose="t")
    c.ask(ST, QS, case_id="3", qset_version="v", data_classes={"synthetic"}, purpose="t")
    c.ask(ST, QS, case_id="4", qset_version="v", data_classes={"synthetic"}, purpose="t")
    c.ask({"m": "hello"}, QS, case_id="5", qset_version="v", data_classes={"synthetic"}, purpose=f"purpose {KEY}")
    blob = b"".join(p.read_bytes() for p in tmp_path.rglob("*") if p.is_file())
    assert KEY.encode() not in blob and KEY[:10].encode() not in blob
    assert b"[REDACTED]" in blob
    assert redact({"a": [KEY, {"b": KEY}]}) == {"a": ["[REDACTED]", {"b": "[REDACTED]"}]}


def test_redact_is_identity_without_key(monkeypatch):
    monkeypatch.delenv("JEV_API_KEY", raising=False)
    o = {"a": "x"}
    assert redact(o) is o


def run_scan(*args, env_key=None):
    env = {k: v for k, v in os.environ.items() if k != "JEV_API_KEY"}
    return subprocess.run(["uv", "run", "--no-project", "python", str(JEV / "keyscan.py"), *args],
                          capture_output=True, text=True, env=env)


def test_keyscan_detects_planted_key(tmp_path):
    (tmp_path / "clean.txt").write_text("nothing here")
    (tmp_path / "planted.bin").write_bytes(b"\x00" * 1_048_000 + KEY.encode() + b"\x01" * 50)   # straddles a 1 MB chunk edge
    p = run_scan("--fake", KEY, str(tmp_path))
    assert p.returncode == 1 and "KEYSCAN FAIL" in p.stdout and "planted.bin" in p.stdout
    assert "clean.txt" not in p.stdout


def test_keyscan_ok_on_clean_tree(tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    p = run_scan("--fake", KEY, str(tmp_path))
    assert p.returncode == 0 and p.stdout.strip().startswith("KEYSCAN OK files=1")


def test_keyscan_never_prints_key(tmp_path):
    (tmp_path / "x.txt").write_text(KEY + KEY[:10])
    p = run_scan("--fake", KEY, str(tmp_path))
    assert p.returncode == 1
    assert KEY not in p.stdout + p.stderr and KEY[:10] not in p.stdout + p.stderr


def test_keyscan_chunk_boundary_exact(tmp_path):
    (tmp_path / "e.bin").write_bytes(b"a" * (1024 * 1024 - 5) + KEY.encode())
    assert run_scan("--fake", KEY, str(tmp_path)).returncode == 1
