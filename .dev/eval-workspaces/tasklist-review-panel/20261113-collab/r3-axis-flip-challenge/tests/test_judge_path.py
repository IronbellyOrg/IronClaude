import json
import os
import subprocess

from conftest import EVAL, R3


def rel(row):
    return subprocess.run(
        [
            "realpath",
            "-m",
            "--relative-to",
            str(EVAL / "arms/scoring/combos"),
            str(row),
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def test_default_and_tmp_roots(tmp_path):
    for row in (R3 / "scoring" / "s0123456789", tmp_path / "scoring" / "sabcdef0123"):
        c = rel(row)
        assert os.path.normpath(
            str(EVAL / "arms/scoring/combos" / c)
        ) == os.path.normpath(str(row))
    assert (
        rel(R3 / "scoring" / "s0123456789")
        == "../../../../20261113-collab/r3-axis-flip-challenge/scoring/s0123456789"
    )


def test_judge_pin():
    import hashlib

    pins = json.loads((R3 / "config/pins.json").read_text())["sha256"]
    assert (
        hashlib.sha256(
            (EVAL / "tools/tmp-scripts/judge-one.sh").read_bytes()
        ).hexdigest()
        == pins["judge-one.sh"]
    )
