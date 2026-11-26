"""R-05: run-reviewer2.sh --print-cmd differs from RR:48 only by cd target, timeout value, the missing
--no-session-persistence and the brief; a receiver adds only --settings <file>; no fallback code path exists."""
import difflib
import json
import shlex
import time

from conftest import BIN, CANDIDATE, REAL_EVAL, SOURCE, run

RR = REAL_EVAL / "tools/run-reviewer.sh"


def rr_tokens(model):
    line = RR.read_text().splitlines()[47]
    inner = line[line.index("( ") + 2:line.rindex(" )")]
    toks = []
    for t in shlex.split(inner):
        if t.startswith("<<<"):
            toks += ["<<<", t[3:]]
        else:
            toks.append("" + t.replace("$MODEL", model))
    return toks


def ours(tmp, settings=None, model="gpt-6-luna"):
    sb = tmp / "sb"
    (sb / "cand").mkdir(parents=True, exist_ok=True)
    (sb / "cand/candidate.md").write_text(CANDIDATE)
    (sb / "cand/source.md").write_text(SOURCE)
    args = ["bash", str(BIN / "run-reviewer2.sh"), "--pkgdir", str(tmp / "pd"), "--sb", str(sb), "--pkg", "P", "--rid", "t4-1",
            "--model", model, "--deadline-ms", str(int(time.time() * 1000) + 174_000), "--print-cmd"]
    if settings:
        args += ["--settings", settings]
    r = run(args)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def changes(a, b):
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal":
            out.append((op, tuple(a[i1:i2]), tuple(b[j1:j2])))
    return out


def test_a1_diff_exactly_the_allowed_list(tmp_path):
    a, b = rr_tokens("gpt-6-luna"), ours(tmp_path)
    ch = changes(a, b)
    kinds = [(op, x) for op, x, _ in ch]
    assert kinds == [("replace", ("/tmp/evalsb/repo",)), ("replace", ("3000",)), ("delete", ("--no-session-persistence",)),
                     ("replace", ("$BRIEF",))], ch
    assert ch[0][2] == (str(tmp_path / "sb/repo"),)
    assert 173 <= float(ch[1][2][0]) <= 174
    assert "Its source document is " + str(tmp_path / "sb/cand/source.md") in ch[3][2][0]


def test_receiver_adds_only_settings(tmp_path):
    base, rec = ours(tmp_path), ours(tmp_path, settings="/x/settings.json")
    ch = changes(base, rec)
    assert [(op, y) for op, x, y in ch if op != "replace" or x[0][:1] not in "0123456789"] == [("insert", ("--settings", "/x/settings.json"))]


def test_nonreceiver_identical_to_a1(tmp_path):
    a, b = ours(tmp_path), ours(tmp_path)
    assert [c for c in changes(a, b) if not (c[0] == "replace" and len(c[1]) == 1 and c[1][0].replace(".", "").isdigit())] == []


def test_no_fallback_code_path():
    r = run(["grep", "-cE", r"FALLBACK\[|fallback\.log", str(BIN / "run-reviewer2.sh")])
    assert r.stdout.strip() == "0"
