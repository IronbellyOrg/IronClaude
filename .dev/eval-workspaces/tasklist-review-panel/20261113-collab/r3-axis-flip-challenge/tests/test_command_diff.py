import json
import shlex
import subprocess

from conftest import EVAL, R3

PKGDIR = "/x/TASK-WF-design-20261108-041415"


def pc(form, model="gpt-6-luna"):
    out = subprocess.run(
        ["bash", str(R3 / "lib/reviewer.sh"), "print-cmd", PKGDIR, "t4-1", model, form],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return json.loads(out)


def rr_tokens():
    line = (EVAL / "tools/run-reviewer.sh").read_text().splitlines()[47]
    cmd = line.split("&& ", 1)[1].split(" <<<", 1)[0]
    return shlex.split(cmd.replace('"$MODEL"', "MODEL"))


def test_phase1_differs_only_by_allowed_items():
    rr = rr_tokens()
    mine = pc("phase1")["argv"]
    assert rr[:2] == ["timeout", "3000"] and mine[:3] == [
        "timeout",
        "--kill-after=5",
        "<T>",
    ]
    rr_rest = [t for t in rr[2:] if t != "--no-session-persistence"]
    mine_rest = [("MODEL" if t == "gpt-6-luna" else t) for t in mine[3:]]
    assert mine_rest == rr_rest
    assert "--no-session-persistence" in rr and "--no-session-persistence" not in mine


def test_other_forms():
    for form in ("reask", "phase2", "fallback", "p2reask"):
        d = pc(form)
        a = d["argv"]
        assert a[a.index("--model") + 1] == "gpt-6-luna"
        assert (
            "--permission-mode" in a
            and a[a.index("--permission-mode") + 1] == "bypassPermissions"
        )
        i = a.index("--disallowedTools")
        assert a[i + 1 : i + 4] == ["Edit", "Write", "NotebookEdit"]
        assert a[a.index("--output-format") + 1] == "stream-json" and "--verbose" in a
        assert "--no-session-persistence" not in a
        assert ("--resume" in a) == (form != "fallback")
        if form != "fallback":
            assert a[a.index("--resume") + 1] == "<id>"
        assert a[0] == "timeout" and "<T>" in a[:4]
        assert d["deadline"] == ("HANG_AT" if form == "reask" else "P2_DEADLINE")


def test_phase1_same_in_both_modes():
    # print-cmd does not read PANEL_COLLAB; the phase-1 argv is the same object in both arms
    import os

    a = subprocess.run(
        [
            "bash",
            str(R3 / "lib/reviewer.sh"),
            "print-cmd",
            PKGDIR,
            "t4-1",
            "gpt-6-luna",
            "phase1",
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "PANEL_COLLAB": "0"},
    ).stdout
    b = subprocess.run(
        [
            "bash",
            str(R3 / "lib/reviewer.sh"),
            "print-cmd",
            PKGDIR,
            "t4-1",
            "gpt-6-luna",
            "phase1",
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "PANEL_COLLAB": "1"},
    ).stdout
    assert a == b
