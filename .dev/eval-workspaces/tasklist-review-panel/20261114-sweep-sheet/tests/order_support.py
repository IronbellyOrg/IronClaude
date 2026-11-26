"""Temporary git repositories with dated commits for the freeze and order tests (TESTING REQ-33, REQ-36, REQ-44, K5).

Git runs only inside the repository that a test creates under tmp_path; the tests write there and nowhere else.
"""

import os
import re
import subprocess
from pathlib import Path

CLEAN_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
IDENT = [
    "-c",
    "user.name=t",
    "-c",
    "user.email=t@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "tag.gpgsign=false",
]
FROZEN = {
    "cards/C1.json": '{"id": "C1"}\n',
    "cards/C2.json": '{"id": "C2"}\n',
    "briefs/base.txt": "a brief part\n",
    "sweep/extractors.py": "EXTRACTORS = {}\n",
    "sweep/words.py": "WORDS = ()\n",
    "sweep/formats.py": "FORMATS = {}\n",
    "sweep/rank.py": "TABLE = {}\n",
}


def git(repo, *args, when=None, check=True):
    env = dict(CLEAN_ENV)
    if when is not None:
        # "@<epoch seconds>": git does not read a bare small number as a date
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"@{when} +0000"
    r = subprocess.run(
        ["git", "-C", str(repo), *IDENT, *args], capture_output=True, text=True, env=env
    )
    if check:
        assert r.returncode == 0, (args, r.stderr)
    return r


def make_repo(root):
    repo = Path(root) / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    return repo


def write(repo, files):
    for rel, text in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def save(repo, files, when, msg="m"):
    """Write the files, record them in one commit dated `when` (epoch seconds), return the commit id."""
    write(repo, files)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg, when=when)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def mark(repo, name, when):
    """An annotated tag on HEAD dated `when`."""
    git(repo, "tag", "-a", name, "-m", "freeze", when=when)


def tags(repo):
    return git(repo, "tag", "-l").stdout.split()


# the check of the plan's Constraints (`gitcheck`), written out in Python so that a test can run it over any folder
GIT_WRITE = re.compile(r"\bgit\b[^|;&]*\b(add|commit|tag|push)\b")
SANDBOX_VAR = re.compile(r'git -C "\$\{?SB[A-Za-z_]*\}?')
SAID = re.compile(r"^\s*(#|echo|printf)")


def gitcheck(folder):
    """Lines of the files under folder that run git add, commit, tag or push, except `git -C "$SB..."` and printed or commented text."""
    hits = []
    for p in sorted(Path(folder).rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts:
            continue
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            if (
                GIT_WRITE.search(line)
                and not SANDBOX_VAR.search(line)
                and not SAID.match(line)
            ):
                hits.append(f"{p}:{n}:{line}")
    return hits
