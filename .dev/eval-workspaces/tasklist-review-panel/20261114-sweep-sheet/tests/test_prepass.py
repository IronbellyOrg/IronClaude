"""REQ-18: the pre-pass is read-only, deterministic and model-free (TESTING REQ-18), plus the CLI it is run through."""

import json
import socket
import subprocess
import sys

import pytest
from prepass_support import SW, file_hashes, load, make_inputs, run, strings

from sweep import cli, prepass

CLI = SW / "sweep" / "cli.py"
FILES = {
    "assignment.json",
    "candidates.json",
    "items.json",
    "prepass.json",
    "prepass.log",
}


def test_byte_identical_same_seed(tmp_path):
    """Two runs with seed 1, on two copies of the input at different paths, give identical hashes for every file."""
    a, b = make_inputs(tmp_path / "a"), make_inputs(tmp_path / "b")
    ha = file_hashes(run(a, tmp_path / "out-a", seed=1))
    hb = file_hashes(run(b, tmp_path / "out-b", seed=1))
    assert FILES <= set(ha) and any(n.startswith("sheets/") for n in ha)
    assert ha == hb
    assert not (tmp_path / "out-a" / "prepass.tmp").exists()


def test_other_seed_changes_only_order(tmp_path):
    """Seed 2 changes assignment.json and the order inside each sheet, not the ids and statuses or who gets what."""
    inp = make_inputs(tmp_path / "in")
    one = run(inp, tmp_path / "s1", seed=1)
    two = run(inp, tmp_path / "s2", seed=2)
    assert file_hashes(one)["assignment.json"] != file_hashes(two)["assignment.json"]

    def facts(folder):
        items, cands = load(folder, "items.json"), load(folder, "candidates.json")
        return (
            [(i["item_id"], i["class"]) for i in items["items"]],
            [
                (c["anchor_text"], c["class"], c["status"], c["item_id"])
                for c in cands["candidates"]
            ],
        )

    assert facts(one) == facts(two)
    a1, a2 = load(one, "assignment.json"), load(two, "assignment.json")
    for key in (
        "item_reviewers",
        "replicas",
        "caps",
        "loads",
        "replica_dropped",
        "dropped",
    ):
        assert a1[key] == a2[key], key
    assert {r: sorted(v) for r, v in a1["reviewers"].items()} == {
        r: sorted(v) for r, v in a2["reviewers"].items()
    }
    moved = 0
    for sheet in sorted((one / "sheets").glob("*.md")):
        t1, t2 = (
            sheet.read_text(encoding="utf-8"),
            (two / "sheets" / sheet.name).read_text(encoding="utf-8"),
        )
        blocks1, blocks2 = t1.split("\n\n"), t2.split("\n\n")
        assert sorted(blocks1[1:]) == sorted(
            blocks2[1:]
        )  # the same item blocks, only the order can differ
        moved += t1 != t2
    assert (
        moved >= 1
    )  # with 8 items on each sheet a changed seed reorders at least one of three


def test_no_absolute_paths_in_json(tmp_path):
    """No JSON string starts with `/` and no output file holds the run's temporary root."""
    inp = make_inputs(tmp_path / "in")
    out = run(inp, tmp_path / "out")
    seen = 0
    for p in sorted(out.rglob("*")):
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        assert str(tmp_path) not in text, p.name
        if p.suffix == ".json":
            seen += 1
            assert text.endswith("\n") and not text.endswith("\n\n")
            assert not [s for s in strings(json.loads(text)) if s.startswith("/")], (
                p.name
            )
    assert seen >= 7


def tree_hash(root):
    """One hash over every file of root, `.git` included."""
    return file_hashes(root)


def test_snapshot_unchanged(tmp_path):
    """The files and the git state of the snapshot are the same after the run; `git status` is clean."""
    inp = make_inputs(tmp_path / "in")
    before = tree_hash(inp.repo)
    run(inp, tmp_path / "out")
    assert tree_hash(inp.repo) == before
    r = subprocess.run(
        ["git", "-C", str(inp.repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert r.stdout == ""


def test_no_network_no_model(tmp_path, monkeypatch):
    """With sockets blocked and no API key, the only processes are git rev-parse, ls-files and grep on the snapshot."""
    inp = make_inputs(tmp_path / "in")
    for name in (
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_BASE_URL",
        "OPENAI_API_KEY",
        "OPENAI_BASE_URL",
    ):
        monkeypatch.delenv(name, raising=False)

    def no_net(*a, **k):
        raise AssertionError("network access")

    for name in ("connect", "connect_ex", "sendto"):
        monkeypatch.setattr(socket.socket, name, no_net)
    for name in ("getaddrinfo", "gethostbyname", "create_connection"):
        monkeypatch.setattr(socket, name, no_net)

    calls = []
    real = subprocess.Popen

    class Guarded(real):
        def __init__(self, args, *a, **k):
            argv = [args] if isinstance(args, (str, bytes)) else list(args)
            calls.append(argv)
            if not (
                argv[:2] == ["git", "-C"]
                and argv[2] == str(inp.repo.resolve())
                and argv[3] in ("grep", "ls-files", "rev-parse")
            ):
                raise AssertionError(f"process not allowed: {argv}")
            super().__init__(args, *a, **k)

    monkeypatch.setattr(subprocess, "Popen", Guarded)
    monkeypatch.setattr("os.system", no_net)
    run(inp, tmp_path / "out")
    verbs = {c[3] for c in calls}
    assert {"grep", "ls-files"} <= verbs and verbs <= {"grep", "ls-files", "rev-parse"}


def test_failure_leaves_no_prepass_folder(tmp_path):
    """A pre-pass error removes prepass.tmp, never makes prepass/, and writes prepass.error.json (DESIGN 10 row 1)."""
    inp = make_inputs(tmp_path / "in")
    out = tmp_path / "out"
    prepass.run(inp.candidate, inp.source, inp.repo, seed=1, out=out)
    assert (out / "prepass").is_dir()
    with pytest.raises(Exception):  # noqa: B017  # the snapshot is not a directory, so the search scope raises
        prepass.run(inp.candidate, inp.source, tmp_path / "missing", seed=1, out=out)
    assert (
        out / "prepass"
    ).is_dir()  # the earlier good result is untouched until a new one is complete
    assert not (out / "prepass.tmp").exists()
    err = json.loads((out / "prepass.error.json").read_text(encoding="utf-8"))
    assert err == {"error": "NotAGitRepo", "extractor": None, "stage": "find"}
    prepass.run(inp.candidate, inp.source, inp.repo, seed=1, out=out)
    assert not (out / "prepass.error.json").exists()


def cli_run(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True
    )


def test_cli_prepass_help_runs_as_a_script():
    r = cli_run("prepass", "--help")
    assert r.returncode == 0, r.stderr
    assert "--candidate" in r.stdout and "--seed" in r.stdout


def test_cli_has_check_subcommand():
    """`check` was added by Task 25 and `clock` by Task 27: both are in the parser and answer `--help` with exit 0."""
    choices = cli.build_parser()._subparsers._group_actions[0].choices
    assert set(choices) == {"prepass", "lint", "brief", "normalise", "check", "clock"}
    r = cli_run("check", "--help")
    assert r.returncode == 0 and "--run" in r.stdout
    r = cli_run("clock", "plan", "--help")
    assert r.returncode == 0 and "--panel" in r.stdout
    r = cli_run("prepass", "--help")
    assert r.returncode == 0 and "--available" in r.stdout


def test_cli_prepass_and_delegates(tmp_path):
    """prepass runs through the script; lint, brief and normalise reach their scaffold modules."""
    inp = make_inputs(tmp_path / "in")
    out = tmp_path / "out"
    r = cli_run(
        "prepass", "--candidate", inp.candidate, "--source", inp.source,
        "--repo", inp.repo, "--seed", 1, "--out", out,
    )  # fmt: skip
    assert r.returncode == 0, r.stderr
    assert FILES <= set(file_hashes(out / "prepass"))
    bad = cli_run(
        "prepass",
        "--candidate",
        inp.candidate,
        "--repo",
        tmp_path,
        "--seed",
        1,
        "--out",
        tmp_path / "o2",
    )
    assert bad.returncode == 1 and (tmp_path / "o2" / "prepass.error.json").is_file()
    assert not (tmp_path / "o2" / "prepass").exists()

    assert "--gt-glob" in cli_run("lint", "--help").stdout

    sheet = next((out / "prepass" / "sheets").glob("*.md"))
    brief = tmp_path / "briefs" / "r1.txt"
    r = cli_run(
        "brief", "--arm", "SS", "--candidate-sb", inp.candidate, "--source", inp.source,
        "--sheet", sheet, "--out", brief,
    )  # fmt: skip
    assert r.returncode == 0, r.stderr
    meta = json.loads(r.stdout)
    assert meta["no_trigger"] is False and "sheet-block" in meta["parts"]
    assert sheet.read_text(encoding="utf-8").splitlines()[0] in brief.read_text(
        encoding="utf-8"
    )
    assert (
        brief.with_suffix(".sha256").read_text(encoding="utf-8").strip()
        == meta["sha256"]
    )

    report = tmp_path / "rep.md"
    report.write_text("## Findings block\n\n```findings-v1\n```\n", encoding="utf-8")
    r = cli_run(
        "normalise", "--report", report, "--out-dir", tmp_path / "norm", "--rid", "r1"
    )
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "norm" / "r1.md").is_file() and (
        tmp_path / "norm" / "h2.json"
    ).is_file()
