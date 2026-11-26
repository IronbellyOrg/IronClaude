"""bin/build-sandbox.sh on the real pinned trees (slow: about 15 s), design 1.2 (H3, H4)."""

import hashlib
import json
import re
from pathlib import Path

from r4help import DS, EVAL, PKGS, R4, REPO, run

LEAKS = [".dev/reflect", ".dev/eval-workspaces", ".dev/research", ".dev/tasks/done"]


def test_build_and_rebuild_skip(env):
    r = run([R4 / "bin" / "build-sandbox.sh"], env=env, timeout=600)
    assert r.returncode == 0, r.stderr
    sbr, out = Path(env["R4_SBR"]), Path(env["R4_OUT"])
    man = json.load(open(out / "manifest.json"))
    trees = {p["id"]: p["base_tree"] for p in json.load(open(R4 / "frozen" / "packages.json"))}
    assert {p["package"]: p["base_tree"] for p in man["packages"]} == trees
    for p in PKGS:
        repo = sbr / "sb" / p / "repo"
        for d in LEAKS:
            assert not (repo / d).exists(), (p, d)
        assert run(["git", "-C", repo, "status", "--porcelain", "--ignored"]).stdout == ""
        assert hashlib.sha256((sbr / "cand" / p / "candidate.md").read_bytes()).hexdigest() == \
            hashlib.sha256((EVAL / p / "candidate.md").read_bytes()).hexdigest()
    # H3 spot check: a file the designSpec candidate's Tasks edit differs from REPO HEAD
    cand = (EVAL / DS / "candidate.md").read_text()
    paths = sorted(set(re.findall(r"`((?:src|tests|docs|\.claude)/[^`\s]+\.\w+)`", cand)))
    differs = [p for p in paths if (sbr / "sb" / DS / "repo" / p).is_file() and (REPO / p).is_file()
               and (sbr / "sb" / DS / "repo" / p).read_bytes() != (REPO / p).read_bytes()]
    assert differs, paths
    built = {p: (sbr / "sb" / p / "built.json").stat().st_mtime_ns for p in PKGS}
    r2 = run([R4 / "bin" / "build-sandbox.sh"], env=env, timeout=600)
    assert r2.returncode == 0
    assert {p: (sbr / "sb" / p / "built.json").stat().st_mtime_ns for p in PKGS} == built
