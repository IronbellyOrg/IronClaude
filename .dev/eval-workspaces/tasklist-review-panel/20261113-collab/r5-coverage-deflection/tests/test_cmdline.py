"""T-11 (AC-6): the A1 command and brief differ from run-reviewer.sh only by the allowed R-05 differences."""
import os
import re
import shlex

from conftest import CT, bin_, run, write_values
from r5 import now_ms


def dry(env, collab, kit, role="receiver", settings="/x/settings.json"):
    e = {"DRY_RUN": "1", "PANEL_COLLAB": str(collab), "PANEL_KIT": str(kit)}
    write_values(env["cfg"], "sl2", all={"hang_offset_s": 410.55})
    vals = str(env["cfg"] / "values" / "sl2" / f"{CT}.json")
    r = run(["bash", bin_("run-reviewer-r5.sh"), "/tmp/unused", CT, "t1b-1", "claude-sonnet-5-5", role, str(now_ms()), vals, settings],
            env={**os.environ, **e})
    assert r.returncode == 0, r.stderr
    out = r.stdout
    cmd = shlex.split(re.search(r"^CMD: (.*)$", out, re.M).group(1))
    brief = re.search(r"BRIEF-BEGIN\n(.*)\nBRIEF-END", out, re.S).group(1)
    return out, cmd, brief


def reference(env):
    lines = (env["eval"] / "tools" / "run-reviewer.sh").read_text().split("\n")
    m = re.search(r"timeout 3000 (claude .*?) <<<", lines[47])
    ref_cmd = ["timeout", "3000"] + shlex.split(m.group(1).replace('"$MODEL"', "claude-sonnet-5-5"))
    brief = "\n".join(lines[12:17])[len('BRIEF="'):-1]
    return ref_cmd, brief, lines[47]


def test_a1_command_and_brief(env):
    ref_cmd, ref_brief, line48 = reference(env)
    assert "cd /tmp/evalsb/repo" in line48
    out, cmd, brief = dry(env, 0, 0)
    assert re.search(r"^CWD: .*/sb/" + CT + "/repo$", out, re.M)
    allowed = ref_cmd.copy()
    allowed.remove("--no-session-persistence")
    assert cmd[0] == "timeout" and cmd[1].isdigit() and cmd[1] != "3000"
    assert cmd[2:] == allowed[2:]
    cand = str(env["sb"] / "cand" / CT / "candidate.md")
    src = str(env["sb"] / "cand" / CT / "source.md")
    sha = re.search(r"sha256 of the file: ([0-9a-f]{64})", brief).group(1)
    expect = ref_brief.replace("$CAND_SB", cand).replace("$SHA", sha)
    h1 = f" The source document this plan was written from is {src}; read both the candidate and the source document."
    first = "against the requirements it states, review 1 of 3."
    assert brief == expect.replace(first, first + h1, 1)
    assert "--settings" not in cmd


def test_kit_and_collab(env):
    _o, _c, a1 = dry(env, 0, 0)
    _o, cmd2, a2 = dry(env, 0, 1)
    kit = (env["cfg"] / "templates" / "brief-kit.txt").read_text() + "\n" + (env["cfg"] / "catalogue.md").read_text()
    assert a2 == a1 + "\n\n" + kit.rstrip("\n")
    assert "--settings" not in cmd2
    _o, cmd3, f6r = dry(env, 1, 0)
    line = (env["cfg"] / "templates" / "brief-receiver-f6.txt").read_text()
    assert f6r == a2 + "\n\n" + line
    assert cmd3[-2:] == ["--settings", "/x/settings.json"]
    _o, cmd4, f6s = dry(env, 1, 0, role="scout")
    assert f6s == a2 and "--settings" not in cmd4


def test_reask_command(env):
    out, _c, _b = dry(env, 0, 0)
    reask = re.search(r"^REASK_CMD: (.*)$", out, re.M).group(1)
    assert "--resume <session_id>" in reask and "--output-format stream-json --verbose" in reask
    assert re.search(r"^CMD2: .*", out, re.M) and "--settings" not in re.search(r"^CMD2: (.*)$", out, re.M).group(1)
