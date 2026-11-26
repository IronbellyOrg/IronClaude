"""K3, REQ-34: the harness reads no ground truth. Render part: the lens render and the brief render never open a trap
file named like a ground-truth file in the F-REPO fixture. Row-check part: the same for `check`."""

import builtins
import io
import json
import os
from pathlib import Path

import pytest

from fixtures.reports import make_rl_reports as rep
from fixtures.repos.build_repo import build_repo
from rl import cli


@pytest.fixture
def opened(monkeypatch):
    """A read hook on `open`: the list of every path opened through builtins.open or io.open (pathlib uses io.open)."""
    seen: list[str] = []

    def spy(real):
        def hooked(file, *args, **kw):
            if not isinstance(file, int):
                seen.append(os.fspath(file))
            return real(file, *args, **kw)

        return hooked

    monkeypatch.setattr(builtins, "open", spy(builtins.open))
    monkeypatch.setattr(io, "open", spy(io.open))
    return seen


def traps(fx):
    found = [
        fx.repo / "ground-truth.json",
        fx.repo / ".dev" / "gt" / "ground-truth.json",
    ]
    assert all(t.is_file() for t in found)
    return found


def test_the_hook_sees_an_open_of_the_trap(tmp_path, opened):
    fx = build_repo(tmp_path)
    opened.clear()
    traps(fx)[0].read_text()
    open(traps(fx)[1]).close()
    assert opened == [str(t) for t in traps(fx)]


@pytest.mark.parametrize("fallback", [False, True])
def test_lens_and_brief_render_never_open_the_trap(tmp_path, opened, fallback):
    fx = build_repo(tmp_path)
    found = traps(fx)
    out = tmp_path / "run"
    opened.clear()
    argv = [
        "lens",
        "--panel",
        "primary",
        "--doc",
        fx.doc_id,
        "--candidate-sb",
        str(fx.repo / "README.md"),
        "--source",
        str(fx.repo / fx.source_rel),
        "--out",
        str(out),
    ]
    assert cli.main([*argv, "--fallback", "error"] if fallback else argv) == 0
    assert str(fx.repo / "README.md") in opened and opened  # the hook was live
    assert not [p for p in opened if "ground-truth" in Path(p).name]
    assert not set(map(str, found)) & set(opened)
    for p in out.rglob("*"):
        if p.is_file():
            assert fx.trap_marker not in p.read_text(encoding="utf-8")


def test_row_check_never_opens_the_trap(tmp_path, opened):
    fx = build_repo(tmp_path)
    found = traps(fx)
    cand, source = fx.repo / "README.md", fx.repo / fx.source_rel
    out = tmp_path / "run"
    lens_argv = ["lens", "--panel", "primary", "--doc", fx.doc_id]
    lens_argv += ["--candidate-sb", str(cand), "--source", str(source)]
    assert cli.main([*lens_argv, "--out", str(out)]) == 0
    (out / "reviews").mkdir()
    for rid, name in (("t2b-1", "good_ember"), ("t4-1", "good_luna1")):
        c = rep.build(name)  # t3-1 has no report: a dropped reviewer is part of the run
        (out / "reviews" / f"{rid}.md").write_text(c.report, encoding="utf-8")
        (out / "reviews" / f"{rid}.attempt1.json").write_text(
            json.dumps(c.transcript), encoding="utf-8"
        )
    opened.clear()
    argv = [
        "check",
        "--run",
        str(out),
        "--candidate",
        str(cand),
        "--source",
        str(source),
    ]
    assert cli.main(argv) == 0
    assert (
        str(cand) in opened and str(out / "reviews" / "t2b-1.md") in opened
    )  # the hook was live
    assert not [p for p in opened if "ground-truth" in Path(p).name]
    assert not set(map(str, found)) & set(opened)
    assert (out / "check" / "check.json").is_file()
    for p in out.rglob("*"):
        if p.is_file():
            assert fx.trap_marker not in p.read_text(encoding="utf-8")


def test_lens_brief_and_check_never_open_the_trap(tmp_path, opened):
    """REQ-34 / K3 (TESTING section 4): the lens render, the brief render of the Z0 arm and the row check, run one after
    the other over one F-REPO sandbox with the trap present, never open a file named like ground truth."""
    fx = build_repo(tmp_path)
    found = traps(fx)
    cand, source = fx.repo / "README.md", fx.repo / fx.source_rel
    out = tmp_path / "run"
    common = [
        "--panel",
        "primary",
        "--doc",
        fx.doc_id,
        "--candidate-sb",
        str(cand),
        "--source",
        str(source),
    ]
    opened.clear()
    assert cli.main(["lens", *common, "--out", str(out)]) == 0
    assert (
        cli.main(["briefs", "--arm", "Z0", *common, "--out", str(tmp_path / "z0")]) == 0
    )
    (out / "reviews").mkdir()
    for rid, name in (("t2b-1", "good_ember"), ("t4-1", "good_luna1")):
        c = rep.build(name)
        (out / "reviews" / f"{rid}.md").write_text(c.report, encoding="utf-8")
        (out / "reviews" / f"{rid}.attempt1.json").write_text(
            json.dumps(c.transcript), encoding="utf-8"
        )
    assert (
        cli.main(
            [
                "check",
                "--run",
                str(out),
                "--candidate",
                str(cand),
                "--source",
                str(source),
            ]
        )
        == 0
    )
    assert (
        str(cand) in opened and str(out / "reviews" / "t2b-1.md") in opened
    )  # the hook was live
    assert not [p for p in opened if "ground-truth" in Path(p).name]
    assert not set(map(str, found)) & set(opened)
    for p in (*out.rglob("*"), *(tmp_path / "z0").rglob("*")):
        if p.is_file():
            assert fx.trap_marker not in p.read_text(encoding="utf-8")
