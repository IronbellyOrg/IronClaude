"""REQ-03, REQ-04, REQ-34 and DD-15: bin/build-sandbox.sh over the F-REPO fixture (TESTING section 3)."""

import json
import subprocess
from types import SimpleNamespace

import pytest
from helpers import SW

from fixtures.repos.build_repo import OTHER_DOC_ID, build_repo

SCRIPT = SW / "bin" / "build-sandbox.sh"


def run(fx, *args, **env):
    return subprocess.run(
        ["bash", str(SCRIPT), "--packages", str(fx.packages), *args, fx.doc],
        capture_output=True,
        text=True,
        env=fx.roots.with_env(SW_SRC_REPO=str(fx.repo), **env),
    )


def package_entry(fx, base, **over):
    e = {
        "kind": "plan",
        "set": "control",
        "base": base,
        "candidate": ".dev/eval-workspaces/cand/candidate.md",
        "source": fx.source_rel,
        "masked_paths": [fx.added, fx.edited],
    }
    e.update(over)
    return e


def write_packages(fx, entry):
    docs = {fx.doc: entry, OTHER_DOC_ID: dict(entry, set="other")}
    fx.packages.write_text(json.dumps({"schema": "sweep-packages/1", "packages": docs}))


@pytest.fixture
def fx(tmp_roots):
    built = build_repo(tmp_roots.root)
    # the candidate is a working-tree file of the source repository, as in a real run
    cand = built.repo / ".dev/eval-workspaces/cand/candidate.md"
    cand.parent.mkdir(parents=True)
    cand.write_text("# Candidate plan\n", encoding="utf-8")
    fx = SimpleNamespace(
        **vars(built),
        roots=tmp_roots,
        packages=tmp_roots.root / "packages.json",
        doc=built.doc_id,
        sandbox=tmp_roots.sb / built.doc_id / "repo",
        raw=tmp_roots.sb / built.doc_id / "repo-raw",
        cand=tmp_roots.sb / "cand" / built.doc_id,
    )
    write_packages(fx, package_entry(fx, built.base))
    return fx


@pytest.fixture
def built(fx):
    r = run(fx)
    assert r.returncode == 0, r.stderr
    return fx


def git_out(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout


def test_file_created_by_implementation_absent(built):
    assert built.added.endswith("retention.py")
    assert (built.repo / built.added).is_file()  # the head commit has it
    assert not (built.sandbox / built.added).exists()
    assert (built.sandbox / "src/exporter/__init__.py").is_file()


def test_masked_path_equals_base(built):
    base_text = git_out(built.repo, "show", f"{built.base}:{built.edited}")
    head_text = git_out(built.repo, "show", f"{built.head}:{built.edited}")
    assert base_text != head_text
    assert (built.sandbox / built.edited).read_text() == base_text
    # a clean sandbox: git status --porcelain is empty
    assert git_out(built.sandbox, "status", "--porcelain") == ""
    meta = json.loads((built.sandbox.parent / "sandbox.json").read_text())
    assert (meta["kind"], meta["base"]) == ("commit", built.base)
    assert meta["tree"] == git_out(built.sandbox, "rev-parse", "HEAD^{tree}").strip()
    # the candidate and its source are copied beside the sandbox
    assert (built.cand / "candidate.md").read_text() == "# Candidate plan\n"
    assert "Source of" in (built.cand / "source.md").read_text()
    # a second run finds the sandbox valid and changes nothing
    again = run(built)
    assert again.returncode == 0 and "sandbox valid" in again.stdout


def test_tree_snapshot_kind(fx):
    tree = fx.roots.root / "recorded-tree"
    (tree / "docs").mkdir(parents=True)
    (tree / "docs/spec.md").write_text("# Spec\n\nThe exporter writes 2 formats.\n")
    (tree / "keep.txt").write_text("kept\n")
    write_packages(fx, package_entry(fx, f"tree:{tree}", masked_paths=["docs/spec.md"]))
    r = run(fx)
    assert r.returncode == 0, r.stderr
    diff = subprocess.run(
        ["diff", "-r", "--exclude=.git", str(tree), str(fx.sandbox)],
        capture_output=True,
        text=True,
    )
    assert diff.returncode == 0, diff.stdout
    meta = json.loads((fx.sandbox.parent / "sandbox.json").read_text())
    assert meta["kind"] == "tree" and meta["base"] == f"tree:{tree}"
    assert meta["tree"] == git_out(fx.sandbox, "rev-parse", "HEAD^{tree}").strip()
    assert git_out(fx.sandbox, "status", "--porcelain") == ""


def test_dirty_sandbox_refused(built):
    f = built.sandbox / "README.md"
    original = f.read_text()
    extra = built.sandbox / "src/exporter/new_file.py"
    masked = built.sandbox / built.edited
    masked_original = masked.read_text()
    try:
        f.write_text(original + "edited by a reviewer\n")  # a tracked file modified
        r = run(built)
        assert r.returncode == 2 and "E_SANDBOX_DIRTY" in r.stderr
        f.write_text(original)
        extra.write_text("x = 1\n")  # an untracked file
        r = run(built)
        assert r.returncode == 2 and "E_SANDBOX_DIRTY" in r.stderr
        extra.unlink()
        # the masked path replaced by the head version
        masked.write_text((built.repo / built.edited).read_text())
        r = run(built)
        assert r.returncode == 2 and "masked path differs from base" in r.stderr
        assert "E_SANDBOX_DIRTY" in r.stderr
    finally:
        f.write_text(original)
        masked.write_text(masked_original)
        extra.unlink(missing_ok=True)
    assert run(built).returncode == 0


def test_no_reflect_artifacts_progress(built):
    gone = [
        ".dev/reflect",
        ".dev/tasks/done",
        ".dev/research",
        ".dev/eval-workspaces",
        ".dev/tasks/to-do/other/artifacts",
        "artifacts",
        "docs/progress.md",
        ".dev/tasks/to-do/other/progress.md",
    ]
    for rel in gone:
        assert not (built.sandbox / rel).exists(), rel
    names = {p.name for p in built.sandbox.rglob("*") if ".git" not in p.parts}
    assert "artifacts" not in names and "progress.md" not in names
    assert "reflect" not in names
    # everything else stays: code, tests, the mirror, root documents and the other noise
    for rel in (
        "tests/test_report.py",
        "scripts/export.sh",
        "docs/guide.md",
        "CHANGELOG.md",
        built.mirror,
        ".dev/notes/search-noise.md",
        "node_modules/pkg/index.js",
    ):
        assert (built.sandbox / rel).is_file(), rel


def test_no_doc_id_in_paths_or_contents(built, tmp_roots):
    for doc in (built.doc, OTHER_DOC_ID):
        paths = subprocess.run(
            ["find", ".", "-path", f"*{doc}*"],
            cwd=built.sandbox,
            capture_output=True,
            text=True,
        )
        assert paths.stdout == "", paths.stdout
    grep = subprocess.run(
        ["grep", "-rIl", "--exclude-dir=.git", "-F", built.doc, "."],
        cwd=built.sandbox,
        capture_output=True,
        text=True,
    )
    assert grep.returncode == 1 and grep.stdout == ""
    # a document id in the contents of a kept file refuses the build; nothing is left behind
    leaky_root = tmp_roots.root / "leaky"
    leaky_root.mkdir()
    leaky = build_repo(leaky_root, extra={"docs/leak.md": f"see {built.doc}\n"})
    fx2 = SimpleNamespace(
        **vars(leaky),
        roots=tmp_roots,
        packages=built.packages,
        doc=leaky.doc_id,
    )
    (leaky.repo / ".dev/eval-workspaces/cand").mkdir(parents=True)
    (leaky.repo / ".dev/eval-workspaces/cand/candidate.md").write_text("# C\n")
    write_packages(fx2, package_entry(fx2, leaky.base))
    r = run(fx2, SW_SB_ROOT=str(tmp_roots.root / "sb2"))
    assert r.returncode == 2 and "E_LEAK" in r.stderr and "docs/leak.md" in r.stderr
    assert not (tmp_roots.root / "sb2" / built.doc / "repo").exists()
    assert not (tmp_roots.root / "sb2" / built.doc / "repo.tmp").exists()


def test_no_ground_truth_file(built):
    found = [p for p in built.sandbox.rglob("ground-truth*") if ".git" not in p.parts]
    assert found == []
    assert (
        built.repo / "ground-truth.json"
    ).exists()  # the trap is in the source repository
    grep = subprocess.run(
        ["grep", "-rIl", "--exclude-dir=.git", built.trap_marker, str(built.sandbox)],
        capture_output=True,
        text=True,
    )
    assert grep.returncode == 1 and grep.stdout == ""
    # the trap is also absent from the committed snapshot
    assert "ground-truth" not in git_out(built.sandbox, "ls-files")


def test_raw_mode_removes_only_gt(fx):
    r = run(fx, "--raw")
    assert r.returncode == 0, r.stderr
    tracked = set(git_out(fx.repo, "ls-tree", "-r", "--name-only", fx.head).split())
    expected = {
        t
        for t in tracked
        if not t.startswith(".dev/eval-workspaces/") and "ground-truth" not in t
    }
    here = {
        str(p.relative_to(fx.raw))
        for p in fx.raw.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(fx.raw).parts
    }
    assert here == expected
    assert (fx.raw / ".dev/reflect/REFLECT-REPORT.md").is_file()
    assert (fx.raw / "artifacts/build.log").is_file()
    assert (fx.raw / "docs/progress.md").is_file()
    assert (fx.raw / fx.added).is_file()  # raw mode is HEAD, not the base
    assert not (fx.raw / "ground-truth.json").exists()
    assert not (fx.raw / ".dev/gt/ground-truth.json").exists()
    assert git_out(fx.raw, "status", "--porcelain") == ""
    meta = json.loads((fx.raw.parent / "sandbox-raw.json").read_text())
    assert (meta["kind"], meta["base"]) == ("raw", fx.head)
    # the raw sandbox is separate from the base sandbox, and it is reused when valid
    assert not fx.sandbox.exists()
    assert "sandbox valid" in run(fx, "--raw").stdout


def test_refusals(fx):
    r = subprocess.run(
        ["bash", str(SCRIPT), "--packages", str(fx.packages), "TASK-WF-unknown-0"],
        capture_output=True,
        text=True,
        env=fx.roots.with_env(SW_SRC_REPO=str(fx.repo)),
    )
    assert r.returncode == 2 and "unknown package" in r.stderr
    r = subprocess.run(
        ["bash", str(SCRIPT), "--packages", "/home/x/packages.json", fx.doc],
        capture_output=True,
        text=True,
        env=fx.roots.with_env(SW_SRC_REPO=str(fx.repo)),
    )
    assert r.returncode == 2 and "E_OVERRIDE" in r.stderr
    # SW_SRC_REPO outside /tmp/ stops the script before it reads anything
    r = subprocess.run(
        ["bash", str(SCRIPT), "--packages", str(fx.packages), fx.doc],
        capture_output=True,
        text=True,
        env={**fx.roots.with_env(), "SW_SRC_REPO": "/home/coder"},
    )
    assert r.returncode != 0 and "E_OVERRIDE" in r.stderr
    assert not fx.sandbox.exists()
    write_packages(fx, package_entry(fx, "0" * 40))
    r = run(fx)
    assert r.returncode == 2 and "E_BASE" in r.stderr
