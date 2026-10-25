"""Preserve an unborn nested Git fixture as files in an isolated retry index."""

import os
import stat
import subprocess
import tempfile
from pathlib import Path

ROOT = Path.cwd()


def git(*arguments, cwd=ROOT, env=None, data=None):
    return subprocess.check_output(["git", *arguments], cwd=cwd, env=env, input=data)


def entries(repo, prefix=""):
    names = git("ls-files", "--cached", "--others", "--exclude-standard", "-z", cwd=repo).split(b"\0")
    for raw in names:
        if not raw:
            continue
        name = os.fsdecode(raw).rstrip("/")
        path = repo / name
        if path.is_symlink() or path.is_file():
            yield prefix + name, path
        elif path.is_dir() and (path / ".git").exists():
            yield from entries(path, prefix + name + "/")


def main():
    descriptor, temporary = tempfile.mkstemp(prefix="ironclaude-retry-index-")
    os.close(descriptor)
    os.unlink(temporary)
    env = dict(os.environ, GIT_INDEX_FILE=temporary)
    try:
        git("read-tree", "HEAD", env=env)
        tracked = git("ls-files", "--stage", "-z")
        gitlinks = {}
        for row in tracked.split(b"\0"):
            if row.startswith(b"160000 "):
                metadata, name = row.split(b"\t", 1)
                gitlinks[os.fsdecode(name)] = metadata.split()[1]
        rows = {}
        for name, path in entries(ROOT):
            if name in gitlinks or any(name.startswith(link + "/") for link in gitlinks):
                continue
            assert not name.startswith("/") and ".." not in Path(name).parts
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                mode, content = "120000", os.fsencode(os.readlink(path))
            else:
                mode = "100755" if info.st_mode & 0o111 else "100644"
                content = path.read_bytes()
            digest = git("hash-object", "-w", "--stdin", data=content).strip()
            rows[name] = mode.encode() + b" " + digest + b"\t" + os.fsencode(name) + b"\0"
        for name, digest in gitlinks.items():
            rows[name] = b"160000 " + digest + b"\t" + os.fsencode(name) + b"\0"
        git("read-tree", "--empty", env=env)
        git("update-index", "-z", "--index-info", env=env, data=b"".join(rows[name] for name in sorted(rows)))
        tree = git("write-tree", env=env).decode().strip()
        assert len(tree) == 40
        print(tree)
    finally:
        Path(temporary).unlink(missing_ok=True)
        Path(temporary + ".lock").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
