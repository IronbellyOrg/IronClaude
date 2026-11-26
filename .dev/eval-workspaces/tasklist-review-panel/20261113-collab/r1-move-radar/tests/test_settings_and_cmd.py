"""T-10 (settings part): settings-gen.sh output."""

import json

from conftest import TOOLS, run


def test_settings_json(tmp_path):
    board = str(tmp_path / "runs" / "el2-c1-r0" / "P" / "board")
    args = [board, "el2-c1-r0/P", "t4-1", "reader", "1763062000000", "1763062143800", "1763062109600", "2", "8", "12",
            "M3,M5,M6,M9,M8,M10", "P", ""]
    r = run(["bash", str(TOOLS / "settings-gen.sh"), *args])
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    h = d["hooks"]["PostToolUse"]
    assert len(h) == 1 and h[0]["matcher"] == "*" and len(h[0]["hooks"]) == 1
    cmd = h[0]["hooks"][0]
    assert cmd["type"] == "command" and cmd["timeout"] == 5
    assert "$" not in r.stdout
    for v in (board, "'t4-1'", "'1763062000000'", "'1763062143800'", str(TOOLS / "radar-hook.sh")):
        assert v in cmd["command"]
    assert cmd["command"].endswith(" ''")


def test_settings_refuses_unsafe_value(tmp_path):
    args = ["/b", "r", "t4-1", "reader", "0", "1", "1", "2", "8", "12", "M3", "P$(id)", ""]
    assert run(["bash", str(TOOLS / "settings-gen.sh"), *args]).returncode == 2


# ---------------------------------------------------------------- T-10 (cmd part, R-05)
def a1_tokens():
    import shlex

    from conftest import A1DIR
    line = (A1DIR / "tools" / "run-reviewer.sh").read_text().splitlines()[47]  # line 48
    inner = line[line.index("&& ") + 3: line.index(" <<<")]
    return shlex.split(inner)


def allowed(tokens, model, hang):
    """Apply exactly the R-05 allowed set to the A1 token list."""
    t = [model if x == "$MODEL" else x for x in tokens]
    i = t.index("timeout")
    assert t[i + 1] == "3000"
    t[i:i + 2] = ["timeout", "--kill-after=5", hang]
    t.remove("--no-session-persistence")
    return t


def test_print_cmd_collab0_matches_a1(runner):
    import json
    d = json.loads(runner.run(collab=0, print_cmd=True).stdout)
    argv = d["argv"]
    assert argv == allowed(a1_tokens(), "muse-ember-1.0", argv[2]) and argv[2].isdigit()
    assert "--settings" not in argv and "--no-session-persistence" not in argv
    assert d["cwd"] == str(runner.sb / runner.d.name / "repo")
    assert str(runner.sb / "cand" / runner.d.name / "candidate.md") in d["stdin"]
    assert "The plan's source document is " + str(runner.sb / "cand" / runner.d.name / "source.md") in d["stdin"]


def test_print_cmd_collab1_only_adds_settings(runner):
    import json
    s = runner.settings("t2b-1")
    argv = json.loads(runner.run(collab=1, print_cmd=True).stdout)["argv"]
    assert argv == allowed(a1_tokens(), "muse-ember-1.0", argv[2]) + ["--settings", s]
