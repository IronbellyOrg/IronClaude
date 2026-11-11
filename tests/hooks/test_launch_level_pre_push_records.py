"""Record-level tests T-D1..T-D5 for the L2 pre-push hook (issue #441).

Spec FR-003, FR-004, FR-006, FR-009/FR-010, FR-022 and source section 10.1.
The hook runs directly (as git runs it) from a temporary hooks directory, with
a stub identity selector that prints fixed bytes, so each case pins one actor
and one record stream without a git repository.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / "src/superclaude/hooks/scripts/launch-level-pre-push.sh"
SELECTOR = REPO / "src/superclaude/hooks/scripts/launch-job-identity.sh"
P = "launch-level pre-push:"
A = "a" * 40
Z = "0" * 40
ORDINARY = '{"status": "ordinary"}\n'
RELEASED = '{"status": "ordinary", "reason": "released"}\n'
GOVERNED = '{"status": "governed", "session_id": "old"}\n'
UNKNOWN = '{"status": "unknown"}\n'
PROTECTED = f"refs/heads/feature {A} refs/heads/main {Z}\n"
OTHER = f"refs/heads/feature {A} refs/heads/feature {Z}\n"


def refused_governed(ref):
    return (
        f"{P} L2-PROTECTED: a governed launch session may not push to {ref}; the "
        "whole push was refused. A person releases the session as the claim's "
        "launch result describes.\n"
    )


def refused_unknown(ref, why="identity unknown"):
    return (
        f"{P} L2-UNKNOWN: could not classify this push ({why}) and it targets "
        f"{ref}; the whole push was refused, and pushes to other refs are allowed."
    )


def malformed(n, check):
    return (
        f"{P} L2-MALFORMED: git sent pre-push record {n} that this hook cannot "
        f"read ({check}); the whole push was refused.\n"
    )


class Hook:
    """A hooks directory holding the hook, its data file and a stub selector."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.home = tmp / "home"
        self.uvdir = tmp / "uv"
        self.uvdir.mkdir()
        hooks = self.home / ".claude/hooks"
        hooks.mkdir(parents=True)
        self.out = tmp / "selector-out"
        self.selector = hooks / "launch-job-identity.sh"
        self.selector.write_text(f"#!/bin/sh\nexec /bin/cat '{self.out}'\n")
        self.selector.chmod(0o755)
        self.dir = tmp / "git-hooks"
        self.dir.mkdir()
        self.path = self.dir / "pre-push"
        shutil.copyfile(HOOK, self.path)
        self.path.chmod(0o755)
        data = self.dir / "pre-push.launch-level"
        data.write_text(f"{self.home}\n{self.uvdir}\n")
        data.chmod(0o600)
        self.actor(ORDINARY)

    def actor(self, line):
        self.out.write_bytes(line.encode())

    def run(self, records, args=("origin", "https://example.invalid/r.git")):
        return subprocess.run(
            [str(self.path), *args],
            input=records.encode(),
            capture_output=True,
            cwd=self.tmp,
            timeout=20,
        )


@pytest.fixture
def hook(tmp_path):
    return Hook(tmp_path)


def outcome(result):
    return result.returncode, result.stdout.decode(), result.stderr.decode()


# --- T-D1: selector bytes map to ordinary, governed and unknown --------------
def test_td1_real_identify_bytes_are_ordinary(tmp_path):
    home = tmp_path / "fresh"
    home.mkdir(mode=0o700)
    env = {
        "HOME": str(home),
        "PATH": os.environ["PATH"],
        "UV_PYTHON": sys.executable,
        "UV_PYTHON_DOWNLOADS": "never",
    }
    result = subprocess.run(
        ["/bin/bash", str(SELECTOR), "identify"],
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert (result.returncode, result.stdout) == (0, ORDINARY)


@pytest.mark.parametrize(
    "line, expected",
    [
        (ORDINARY, (0, "", "")),
        (RELEASED, (0, "", "")),
        (GOVERNED, (1, "", refused_governed("refs/heads/main"))),
    ],
)
def test_td1_actor_mapping(hook, line, expected):
    hook.actor(line)
    assert outcome(hook.run(PROTECTED)) == expected
    assert outcome(hook.run(OTHER)) == (0, "", "")


@pytest.mark.parametrize("line", [UNKNOWN, '{"status":"ordinary"}\n', ORDINARY * 2, ""])
def test_td1_unknown_mapping(hook, line):
    hook.actor(line)
    code, out, err = outcome(hook.run(PROTECTED))
    assert (code, out) == (1, "")
    assert err.splitlines()[0] == refused_unknown("refs/heads/main")
    assert outcome(hook.run(OTHER)) == (0, "", "")


# --- T-D2: malformed records refuse the whole push ----------------------------
HEX = "object id is not 40 or 64 lowercase hex"
MALFORMED = [
    (f"refs/heads/x {A} refs/heads/main\n", "fewer than three spaces"),
    (f"refs/heads/x {'g' * 40} refs/heads/main {Z}\n", HEX),
    (f"refs/heads/x {A} refs/heads/main {'A' * 40}\n", HEX),
    (f"refs/heads/x {A}  {Z}\n", "empty field"),
    (f"refs/heads/x {A} refs/heads/main {Z}\r\n", "tab, CR or NUL"),
]
THREE = MALFORMED[0][0]


@pytest.mark.parametrize("actor", [GOVERNED, UNKNOWN])
@pytest.mark.parametrize("record, check", MALFORMED)
def test_td2_malformed_record(hook, actor, record, check):
    hook.actor(actor)
    assert outcome(hook.run(record)) == (2, "", malformed(1, check))
    # A malformed record after a valid unprotected one still refuses the push.
    assert outcome(hook.run(OTHER + record)) == (2, "", malformed(2, check))


# --- T-D3: ordinary exits without reading stdin -------------------------------
def test_td3_ordinary_does_not_read_stdin(hook):
    proc = subprocess.Popen(
        [str(hook.path), "origin", "url"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=hook.tmp,
    )
    try:
        # stdin stays open and empty: a hook that read it would block here.
        assert proc.wait(timeout=15) == 0
        assert proc.stdout.read() == b"" and proc.stderr.read() == b""
    finally:
        proc.kill()
        proc.wait()
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            stream.close()
    # A malformed stream is never read either.
    assert outcome(hook.run(THREE)) == (0, "", "")


# --- T-D4: a final line without LF is still parsed ----------------------------
def test_td4_final_line_without_newline(hook):
    hook.actor(GOVERNED)
    assert outcome(hook.run(PROTECTED.rstrip("\n"))) == (
        1,
        "",
        refused_governed("refs/heads/main"),
    )
    assert outcome(hook.run(OTHER.rstrip("\n"))) == (0, "", "")
    last = THREE.rstrip("\n")
    expected = (2, "", malformed(2, "fewer than three spaces"))
    assert outcome(hook.run(OTHER + last)) == expected


# --- T-D5: the hook writes no file --------------------------------------------
def listing(root):
    rows = []
    for p in [root, *root.rglob("*")]:
        st = p.lstat()
        rows.append((str(p.relative_to(root)), st.st_mode, st.st_size, st.st_mtime_ns))
    return sorted(rows)


def test_td5_hook_writes_no_file(hook):
    for actor in (ORDINARY, GOVERNED, UNKNOWN):
        hook.actor(actor)
        before = listing(hook.tmp)
        for records in (PROTECTED, OTHER, THREE, ""):
            hook.run(records)
        assert listing(hook.tmp) == before


# --- FR-009/FR-010: arguments are ignored, including option-like names ---------
@pytest.mark.parametrize(
    "args",
    [("--force", "-x"), ("-o", "--no-verify"), ("--", "--delete"), ()],
)
def test_option_named_remote_and_args_are_ignored(hook, args):
    for actor, records, expected in [
        (ORDINARY, PROTECTED, (0, "", "")),
        (GOVERNED, PROTECTED, (1, "", refused_governed("refs/heads/main"))),
        (GOVERNED, OTHER, (0, "", "")),
        (UNKNOWN, THREE, (2, "", malformed(1, "fewer than three spaces"))),
    ]:
        hook.actor(actor)
        assert outcome(hook.run(records, args)) == expected
