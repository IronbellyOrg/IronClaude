import json
import shutil
import subprocess
import sys

from conftest import EVAL, PKGS, R3, REPO
from superclaude.cli.review import findings as F

REQ = (
    REPO / ".dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md"
)


def _gt_quotes():
    out = []
    for p in PKGS:
        for it in json.loads((EVAL / p / "ground-truth.json").read_text())["items"]:
            q = F.flat(it.get("plan_quote") or "")
            if len(q) >= 12:
                out.append(q)
    return out


def test_catalogue_matches_req():
    cat = json.loads((R3 / "config/catalogue.json").read_text())
    assert list(cat) == [f"M{i}" for i in range(1, 11)]
    lines = REQ.read_text().splitlines()[183:193]
    for ln, (k, v) in zip(lines, cat.items()):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        assert cells[0] == k and cells[1] == v


def test_no_ground_truth_text_in_frames_or_catalogue():
    qs = _gt_quotes()
    texts = [
        (R3 / "config" / n).read_text()
        for n in (
            "catalogue.json",
            "phase2-frame.txt",
            "fallback-frame.txt",
            "reask-frame.txt",
        )
    ]
    flat_texts = [F.flat(t) for t in texts]
    # The fallback frame quotes RR:17 verbatim (the A1 brief every reviewer already gets in both arms);
    # a 12-character run shared with RR's own text (", or when the") is not frame-added text.
    rr = F.flat((EVAL / "tools/run-reviewer.sh").read_text())
    for q in qs:
        for i in range(len(q) - 11):
            sub = q[i : i + 12]
            assert not any(sub in t for t in flat_texts) or sub in rr, sub
    import re

    for p in PKGS:
        for it in json.loads((EVAL / p / "ground-truth.json").read_text())["items"]:
            for path in re.findall(
                r"[\w./-]+\.(?:md|py|json|sh)\b", it.get("description", "")
            ):
                if "/" in path:
                    assert not any(path in t for t in texts), path


def test_pin_check_passes_and_detects_change(tmp_path):
    cli = [sys.executable, str(R3 / "r3lib/cli.py")]
    assert subprocess.run(cli + ["pin", "--check"], capture_output=True).returncode == 0
    cfg = tmp_path / "config"
    shutil.copytree(R3 / "config", cfg)
    assert (
        subprocess.run(
            cli + ["pin", "--check", "--config-dir", str(cfg)], capture_output=True
        ).returncode
        == 0
    )
    f = cfg / "routing.json"
    f.write_bytes(f.read_bytes() + b" ")
    r = subprocess.run(
        cli + ["pin", "--check", "--config-dir", str(cfg)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1 and "config/routing.json" in r.stdout
