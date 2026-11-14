import json
import os
import subprocess

from conftest import CONTROL, R3


def mkrepo(tmp_path):
    src = tmp_path / "src"
    (src / ".dev/tasks/done" / CONTROL).mkdir(parents=True)
    (src / ".dev/reflect").mkdir(parents=True)
    (src / ".dev/eval-workspaces/x").mkdir(parents=True)
    (src / ".dev/research").mkdir(parents=True)
    (src / ".dev/tasks/done" / CONTROL / "source.md").write_text("s\n")
    (src / ".dev/reflect/r.md").write_text("r\n")
    (src / ".dev/eval-workspaces/x/e.md").write_text("e\n")
    (src / ".dev/research/q.md").write_text("q\n")
    (src / "tests/skills").mkdir(parents=True)
    (src / "tests/skills/test_worker_contract.py").write_text("base\n")
    (src / "keep.txt").write_text("k\n")
    (src / "tracked.log").write_text("tracked although ignored\n")
    subprocess.run(
        "git init -q && git add -A && git -c user.name=t -c user.email=t@x commit -q -m base",
        shell=True,
        cwd=src,
        check=True,
    )
    (src / ".gitignore").write_text(
        "*.log\n"
    )  # tracked.log stays tracked but now matches .gitignore
    subprocess.run(
        "git add .gitignore && git -c user.name=t -c user.email=t@x commit -q -m ignore",
        shell=True,
        cwd=src,
        check=True,
    )
    base = subprocess.run(
        ["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    pk = json.loads((R3 / "config/packages.json").read_text())
    pk["packages"][CONTROL]["base"] = base
    (tmp_path / "packages.json").write_text(json.dumps(pk))
    return src


def build(tmp_path, src):
    e = {
        **os.environ,
        "R3_SRC_REPO": str(src),
        "R3_PACKAGES_FILE": str(tmp_path / "packages.json"),
        "R3_SB_ROOT": str(tmp_path / "sb"),
    }
    return subprocess.run(
        ["bash", str(R3 / "bin/build-sandbox.sh"), CONTROL],
        capture_output=True,
        text=True,
        env=e,
    )


def test_build(tmp_path):
    src = mkrepo(tmp_path)
    r = build(tmp_path, src)
    assert r.returncode == 0, r.stderr
    repo = tmp_path / "sb" / CONTROL / "repo"
    for d in (
        ".dev/tasks/done",
        ".dev/eval-workspaces",
        ".dev/research",
        ".dev/reflect",
    ):
        assert not (repo / d).exists()
    assert (repo / "keep.txt").exists()
    tracked = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "tracked.log"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert (
        tracked == "tracked.log"
    )  # in the snapshot, so `git clean -fdX` cannot remove it
    log = subprocess.run(
        ["git", "-C", str(repo), "rev-list", "--count", "HEAD"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert (
        log == "1"
        and subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain"],
            capture_output=True,
            text=True,
        ).stdout
        == ""
    )
    assert build(tmp_path, src).returncode == 0  # reused
    (repo / "dirty.txt").write_text("x")
    r = build(tmp_path, src)
    assert r.returncode == 2 and "E_SANDBOX_DIRTY" in r.stderr


def test_masked_path_differs_fails(tmp_path):
    src = mkrepo(tmp_path)
    (src / "tests/skills/test_worker_contract.py").write_text("repaired\n")
    subprocess.run(
        "git -c user.name=t -c user.email=t@x commit -qam fix",
        shell=True,
        cwd=src,
        check=True,
    )
    pk = json.loads((tmp_path / "packages.json").read_text())
    # base stays at the first commit, but the archive comes from a commit carrying the repaired text
    pk["packages"][CONTROL]["base"] = subprocess.run(
        ["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    (tmp_path / "packages.json").write_text(json.dumps(pk))
    r = build(tmp_path, src)
    assert r.returncode == 0  # masked file equals its own base: allowed
    repo = tmp_path / "sb" / CONTROL / "repo"
    (repo / "tests/skills/test_worker_contract.py").write_text("tampered\n")
    subprocess.run(
        "git -c user.name=t -c user.email=t@x commit -qam t",
        shell=True,
        cwd=repo,
        check=True,
    )
    r = build(tmp_path, src)
    assert r.returncode == 2 and "masked path differs" in r.stderr
