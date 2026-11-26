"""K3 and REQ-34: the pre-pass reads only the candidate, the source and the snapshot, and no ground truth."""

import builtins
import inspect
import io
import os
import re
import tempfile
from pathlib import Path

import pytest
from prepass_support import SW, file_hashes, load, make_inputs, run

from fixtures.repos.build_repo import TRAP_MARKER
from sweep import extractors, prepass

GT_NAME = re.compile(r"ground[-_]?truth", re.IGNORECASE)
GT_WORDS = re.compile(r"ground[-_ ]?truth|plan_quote|gt_marker", re.IGNORECASE)


@pytest.fixture
def opened(monkeypatch):
    """A read hook on `open` (builtins and io, so Path.open and read_text too): [(real path, mode)] of every call."""
    seen = []
    real = builtins.open

    def hook(file, mode="r", *a, **k):
        if isinstance(file, (str, bytes, os.PathLike)):
            seen.append((os.path.realpath(os.fsdecode(file)), mode))
        return real(file, mode, *a, **k)

    monkeypatch.setattr(builtins, "open", hook)
    monkeypatch.setattr(io, "open", hook)
    return seen


def test_only_three_inputs():
    """The entry point takes the candidate, the source and the repository; everything else is the seed, the run
    folder, the panel name and (Task 27, DESIGN 7.3) the reviewer ids still available, and nothing else names a root."""
    sig = inspect.signature(prepass.run)
    pos = [p.name for p in sig.parameters.values() if p.kind is p.POSITIONAL_OR_KEYWORD]
    kw = [p.name for p in sig.parameters.values() if p.kind is p.KEYWORD_ONLY]
    assert pos == ["candidate", "source", "repo"]
    assert kw == ["seed", "out", "panel", "available"]
    assert (
        sig.parameters["available"].default is None
    )  # ids, not a path; None means the whole panel


def test_ground_truth_trap_not_read(tmp_path, opened):
    """The trap files named like ground truth (in the snapshot, beside the candidate and in the run folder) are never
    opened, git never searches them, and every file Python opens lies under an input, the run folder or SW."""
    inp = make_inputs(tmp_path / "in")
    decoys = [
        inp.candidate.parent / "ground-truth.json",
        inp.candidate.parent / "reviews.md",
    ]
    for d in decoys:
        d.write_text(f"{TRAP_MARKER}\n", encoding="utf-8")
    out = tmp_path / "out"
    (out).mkdir()
    (out / "ground-truth-score.json").write_text(f'"{TRAP_MARKER}"\n', encoding="utf-8")
    opened.clear()
    run(inp, out)
    paths = [p for p, _ in opened]
    assert paths, "the read hook saw nothing"
    assert not [p for p in paths if GT_NAME.search(Path(p).name)]
    assert not [p for p in paths if Path(p) in {d.resolve() for d in decoys}]
    roots = [
        inp.candidate.resolve(),
        inp.source.resolve(),
        inp.repo.resolve(),
        out.resolve(),
        SW,
    ]
    tmpdir = Path(tempfile.gettempdir()).resolve()
    stray = [
        p
        for p in paths
        if not any(Path(p) == r or r in Path(p).parents for r in roots)
        and not (
            tmpdir in Path(p).parents and Path(p).parent.name.startswith("sweep-grep-")
        )
    ]
    assert stray == []
    # the hook is live: it saw both documents being read
    assert {inp.candidate.resolve(), inp.source.resolve()} <= {Path(p) for p in paths}
    # the search excludes ground-truth names by pathspec, so git never opened the trap either
    ctx = extractors.Ctx(
        extractors.plan.parse(inp.candidate.read_bytes()), snapshot=inp.repo
    )
    assert any("ground[-_]truth" in s for s in ctx.scope.pathspecs)
    assert not any(GT_NAME.search(Path(f).name) for f in ctx.scope.files)
    for p in sorted((out / "prepass").rglob("*")):
        if p.is_file():
            assert TRAP_MARKER not in p.read_text(encoding="utf-8"), p.name


def test_sheets_hold_no_gt_markers(tmp_path):
    """No sheet and no item file holds a ground-truth file name, the field name `plan_quote` or the trap's text."""
    inp = make_inputs(tmp_path / "in")
    out = run(inp, tmp_path / "out")
    checked = 0
    for p in sorted(out.rglob("*")):
        if p.is_file() and (
            p.parent.name == "sheets" or p.name in ("items.json", "candidates.json")
        ):
            text = p.read_text(encoding="utf-8")
            assert not GT_WORDS.search(text), p.name
            assert TRAP_MARKER not in text, p.name
            checked += 1
    assert checked >= 8


def test_scope_string_and_no_source_in_prepass_json(tmp_path):
    """prepass.json holds the DD-5 scope string (REQ-24) and, with no source, class C2 as not applicable (REQ-01)."""
    inp = make_inputs(tmp_path / "in")
    with_src = load(run(inp, tmp_path / "with", source=True), "prepass.json")
    no_src = load(run(inp, tmp_path / "without", source=False), "prepass.json")
    scope = extractors.Ctx(
        extractors.plan.parse(inp.candidate.read_bytes()), snapshot=inp.repo
    ).scope_string
    assert with_src["scope"] == no_src["scope"] == scope
    assert (
        "excluded: .dev/" in scope
        and "node_modules" in scope
        and "root-level files" in scope
    )
    assert "/tmp" not in scope
    assert with_src["no_source"] is False and with_src["not_applicable"] == {}
    assert with_src["source_sha256"] and "C2" in with_src["classes_triggered"]
    assert no_src["no_source"] is True and no_src["not_applicable"] == {
        "C2": "no_source"
    }
    assert no_src["source_sha256"] is None and "C2" not in no_src["classes_triggered"]
    cands = load(tmp_path / "without" / "prepass", "candidates.json")
    assert all(c["class"] != "C2" for c in cands["candidates"])
    assert "tasks_without_citations" in with_src
    assert file_hashes(tmp_path / "with" / "prepass") != file_hashes(
        tmp_path / "without" / "prepass"
    )
