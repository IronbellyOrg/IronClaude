import json
import os
from pathlib import Path

import pytest
from conftest import CONTROL

from r3lib import values


def test_k():
    assert values.compute_k(116, 6.4, 6.4) == 2
    assert values.compute_k(116, 6.4, 11.0) == 1
    assert values.compute_k(100, 6.4, 13.8) == 1
    assert values.compute_k(100, 6.4, 13.9) == 0
    assert values.compute_k(273.7, 14, 51.7) == 1
    assert values.compute_k(273.7, 14, 51.9) == 0
    assert abs(values.finish_offset(116, 6.4, 6.4) - 143.8) < 1e-9


def test_turn_durations(tmp_path):
    f = tmp_path / "s.jsonl"
    ev = [
        ("user", "2026-11-13T10:00:00.000Z"),
        ("assistant", "2026-11-13T10:00:03.500Z"),
        ("user", "2026-11-13T10:00:04.000Z"),
        ("assistant", "2026-11-13T10:00:10.000Z"),
    ]
    f.write_text("\n".join(json.dumps({"type": t, "timestamp": ts}) for t, ts in ev))
    assert values.turn_durations(f) == pytest.approx([3.5, 6.0])
    assert values.p90([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 9


def test_freeze_refusals(tmp_path, monkeypatch):
    monkeypatch.setenv("R3_VALUES_FILE", str(tmp_path / "v" / "el2.json"))
    monkeypatch.setenv("R3_RUNS_ROOT", str(tmp_path / "runs"))
    with pytest.raises(SystemExit, match="at least 3"):
        values.freeze("el2", [tmp_path / "a", tmp_path / "b"])
    (tmp_path / "v").mkdir()
    (tmp_path / "v" / "el2.json").write_text("{}")
    with pytest.raises(SystemExit, match="exists"):
        values.freeze("el2", [tmp_path / "a", tmp_path / "b", tmp_path / "c"])


def test_freeze_from_runs(tmp_path, monkeypatch):
    monkeypatch.setenv("R3_VALUES_FILE", str(tmp_path / "v" / "el2.json"))
    runs = []
    for i, el in enumerate((100.0, 110.0, 120.0)):
        rd = tmp_path / f"el2-c0-{i}"
        pd = rd / CONTROL
        (pd / "reviews").mkdir(parents=True)
        (rd / "run.json").write_text(json.dumps({"panel": "el2"}))
        (pd / "pkg.json").write_text(json.dumps({"valid": True}))
        (pd / "collab.json").write_text(json.dumps({"panel": {"elapsed_s": el}}))
        for rid in ("t4-1", "t3-1", "t2b-1"):
            ev = [
                {"type": "user", "timestamp": "2026-11-13T10:00:00Z"},
                {"type": "assistant", "timestamp": "2026-11-13T10:00:05Z"},
            ]
            (pd / "reviews" / f"{rid}.p1.session.jsonl").write_text(
                "\n".join(json.dumps(e) for e in ev)
            )
        runs.append(rd)
    v = values.freeze("el2", runs)
    assert v["status"] == "frozen" and v["packages"][CONTROL]["B_f"] == 110.0
    assert v["turn_p90"]["gpt-6-luna"] == 5.0
    f = Path(os.environ["R3_VALUES_FILE"])
    assert (Path(str(f) + ".sha256")).read_text().split()[0] == values.sha256_file(f)
    with pytest.raises(SystemExit):
        values.freeze("el2", runs)
