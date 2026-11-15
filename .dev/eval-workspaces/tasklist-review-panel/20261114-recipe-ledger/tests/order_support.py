"""Shared by test_freeze.py and test_order.py (Task 18): a synthetic RL root with invented frozen files, and a temporary git
repository with commits at explicit dates. The real repository is never touched: every git call runs `git -C <tmp>` with
its own identity, no global configuration and no signing."""

import os
import subprocess
from pathlib import Path

from helpers import SW

FREEZE = SW / "bin" / "freeze.sh"
ORDER = SW / "bin" / "check-order.sh"
DAY = 86400
T0 = 1_800_000_000  # a fixed epoch second; every date below is T0 plus whole days

FROZEN = {
    "recipes/recipes.json": '{"recipes": {}}\n',
    "recipes/rl-block.txt": "block text\n",
    "recipes/search-form.txt": "search text\n",
    "config/lenses.json": '{"panels": {}}\n',
    "cards/C1.json": '{"id": "C1"}\n',
    "cards/C2.json": '{"id": "C2"}\n',
    "briefs/base.txt": "base brief\n",
    "briefs/cb1.txt": "cb1\n",
    "rl/__init__.py": "",
    "rl/render.py": "X = 1\n",
}


def make_root(root: Path) -> Path:
    """Write the synthetic frozen files under root and return it."""
    for rel, text in FROZEN.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


def run(script: Path, root: Path, *args, env=None, **extra):
    e = {k: v for k, v in os.environ.items() if not k.startswith(("RL_", "GT_"))}
    e.update(RL_ROOT=str(root), PYTHONDONTWRITEBYTECODE="1", **(env or {}))
    return subprocess.run(
        ["bash", str(script), *map(str, args)],
        capture_output=True,
        text=True,
        env=e,
        **extra,
    )


def git(repo: Path, *args, day=None):
    """`git -C repo args`; with day, every date of the command is T0 + day days (commit and tag times)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
    if day is not None:
        stamp = f"{T0 + day * DAY} +0000"
        env.update(GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
    cfg = ["-c", "user.name=t", "-c", "user.email=t@example.invalid"]
    cfg += ["-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false"]
    r = subprocess.run(
        ["git", "-C", str(repo), *cfg, *map(str, args)],
        capture_output=True,
        text=True,
        env=env,
    )
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def commit(repo: Path, message: str, day: int):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message, day=day)


def init_repo(path: Path) -> Path:
    """An empty repository at path (it holds the RL root as a sub-folder `rl-root`, like the real tree)."""
    path.mkdir(parents=True)
    git(path, "init", "-q", "-b", "main")
    return path
