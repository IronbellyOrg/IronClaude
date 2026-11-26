"""Shared set-up of the pre-pass tests: the F-REPO repository, the F-PLAN-1 plan and its source in a candidate folder."""

import hashlib
import json
import shutil
from pathlib import Path
from types import SimpleNamespace

from fixtures.repos.build_repo import build_repo
from sweep import prepass

SW = Path(__file__).resolve().parents[1]
PLANS = SW / "fixtures" / "plans"


def make_inputs(root):
    """root/repo (F-REPO), root/cand/candidate.md (p_basic.md) and root/cand/source.md; root is under /tmp."""
    root = Path(root)
    built = build_repo(root)
    cand = root / "cand"
    cand.mkdir()
    shutil.copy(PLANS / "p_basic.md", cand / "candidate.md")
    shutil.copy(PLANS / "source.md", cand / "source.md")
    return SimpleNamespace(
        root=root,
        built=built,
        repo=built.repo,
        candidate=cand / "candidate.md",
        source=cand / "source.md",
    )


def run(inp, out, seed=1, source=True, panel="primary"):
    return prepass.run(
        inp.candidate,
        inp.source if source else None,
        inp.repo,
        seed=seed,
        out=out,
        panel=panel,
    )


def file_hashes(folder):
    """{relative path: sha256} of every file under folder."""
    folder = Path(folder)
    return {
        str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    }


def load(folder, name):
    return json.loads((Path(folder) / name).read_text(encoding="utf-8"))


def strings(obj):
    """Every string in a JSON value, keys included."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from strings(k)
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)
