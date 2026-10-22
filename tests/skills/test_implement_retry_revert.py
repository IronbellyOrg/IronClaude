"""Temp-repo tests for the ``sc_retry_revert`` block of refs/retry.md.

Each case extracts the fenced bash block from the shipped reference and runs it, so
the text the parent executes is the text these tests check. Every subprocess runs
with its cwd inside the temp repo, in an environment that holds no inherited
``GIT_*`` key.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

_RETRY_REF = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-implement-protocol/refs/retry.md"
)
SLUG = "s-12345678"
RUN = f".dev/implement/{SLUG}"
IDENTITY = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
}
OK = "extras=lint:skip,typecheck:skip,test:skip"


def _env(identity=True, **extra):
    """No inherited GIT_* key; only GIT_CONFIG_GLOBAL, the identity and ``extra``."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    if identity:
        env.update(IDENTITY)
    env.update(extra)
    return env


def block() -> str:
    text = _RETRY_REF.read_text(encoding="utf-8")
    blocks = [
        b
        for b in re.findall(r"```bash\n(.*?)```", text, re.S)
        if "sc_retry_revert()" in b
    ]
    assert len(blocks) == 1
    return blocks[0]


def git(repo, *args, env=None, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        env=env or _env(),
        cwd=repo,
        capture_output=True,
        text=True,
        check=check,
    )


def snapshot(repo, identity=True) -> str:
    """The Q0 temp-index sequence: a bare tree of the whole worktree."""
    idx = repo.parent / "snap.idx"
    e = _env(identity, GIT_INDEX_FILE=str(idx))
    git(repo, "read-tree", "HEAD", env=e)
    git(repo, "add", "-A", env=e)
    tree = git(repo, "write-tree", env=e).stdout.strip()
    idx.unlink()
    return tree


def make_repo(tmp_path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / "a.txt").write_text("base\n")
    git(repo, "add", "a.txt")
    git(repo, "commit", "-q", "-m", "init")
    (repo / RUN / "retries").mkdir(parents=True)
    return repo


def header(repo) -> Path:
    ledger = repo / RUN / "progress.md"
    ledger.write_text(
        "# implement ledger — source: notes.md — created: 2026-10-22T00:00:00Z\n"
    )
    return ledger


def write_ledger(ledger, tid, start, n=3, extra=()):
    lines = [
        f"T{tid}: start sha={start}",
        f"T{tid}: blocked verdict=missing ac=T{tid}.AC1 evidence=T{tid}.AC1 {OK} files=a.txt",
        f"T{tid}: retry n={n} step=open checkpoint={'a' * 40} tier=unknown",
        f"T{tid}: retry n={n} step=revert brief={RUN}/retries/T{tid}_brief-{n}.md supersedes=none",
        *extra,
    ]
    with open(ledger, "a") as f:
        f.write("\n".join(lines) + "\n")


def task_dir(repo, tid="1") -> Path:
    d = repo / RUN / "retries" / f"T{tid}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def setup(
    tmp_path,
    tid="1",
    start=None,
    evidence=True,
    q0_head=True,
    prep=None,
    ledger_rel=None,
):
    """A repo at Q0 plus a ledger whose tail is ``retry … step=revert``.

    ``prep(repo)`` builds the Q0 worktree state; ``ledger_rel`` puts the ledger
    somewhere other than the run folder.
    """
    repo = make_repo(tmp_path)
    ledger = header(repo)
    if ledger_rel:
        moved = repo / ledger_rel
        moved.parent.mkdir(parents=True, exist_ok=True)
        ledger.rename(moved)
        ledger = moved
    d = task_dir(repo, tid)
    if prep:
        prep(repo)
    if q0_head:
        (d / "q0-head").write_text(git(repo, "rev-parse", "HEAD").stdout)
    if evidence is True:
        (d / "review-2.md").write_text("verdict: missing\nT1.AC1 unmet\n")
    elif evidence == "empty":
        (d / "review-2.md").write_text("")
    q0 = snapshot(repo)
    write_ledger(ledger, tid, start or q0)
    return repo, ledger, q0


def run_block(repo, ledger, cwd=None, **inputs):
    env = _env(
        identity=False,
        LEDGER=str(ledger),
        RUN_DIR=RUN + "/",
        RETRIES=RUN + "/retries",
        SOURCE="",
        OWN_FILES="",
        ARTIFACTS="",
        SLUG=SLUG,
    )
    env.update(inputs)
    script = repo.parent / "blk.sh"
    script.write_text(block())
    return subprocess.run(
        ["bash", "-c", 'source "$1"; sc_retry_revert', "_", str(script)],
        env=env,
        cwd=cwd or repo,
        capture_output=True,
        text=True,
    )


def refs(repo) -> str:
    return git(repo, "for-each-ref", "--format=%(refname)", "refs/superclaude").stdout


def test_harness_env_holds_only_the_git_keys_it_sets(monkeypatch):
    monkeypatch.setenv("GIT_DIR", "/nonexistent")
    monkeypatch.setenv("GIT_INDEX_FILE", "/nonexistent")
    assert {k for k in _env(identity=False) if k.startswith("GIT_")} == {
        "GIT_CONFIG_GLOBAL"
    }
    assert {k for k in _env() if k.startswith("GIT_")} == {
        "GIT_CONFIG_GLOBAL",
        *IDENTITY,
    }


@pytest.mark.parametrize("evidence", [False, "empty"])
def test_revert_refused_without_evidence(tmp_path, evidence):
    repo, ledger, _ = setup(tmp_path, evidence=evidence)
    (repo / "a.txt").write_text("attempt\n")
    (repo / "new.txt").write_text("attempt\n")
    art = repo / RUN / "artifacts/t1-test.log"  # a cited artifact of the failed attempt
    art.parent.mkdir(parents=True)
    art.write_text("cited\n")
    before = snapshot(repo)
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log")
    assert r.returncode == 2 and "REFUSED no-evidence" in r.stdout, r
    assert "MOVED" not in r.stdout
    assert snapshot(repo) == before  # nothing restored, nothing written
    assert art.read_text() == "cited\n"  # still at its original path
    assert not (repo / RUN / "retries/T1/artifacts-2").exists()  # no move happened
    assert refs(repo) == ""  # no sweep ref
    assert refs(repo) == ""  # no sweep ref


@pytest.mark.parametrize("kind", ["commit", "nogit", "zero"])
def test_revert_refuses_non_tree_start(tmp_path, kind):
    repo, ledger, _ = setup(tmp_path)
    # rewrite the start line (the block binds to the latest start line)
    start = {
        "commit": git(repo, "rev-parse", "HEAD").stdout.strip(),
        "nogit": "nogit",
        "zero": "0" * 40,
    }[kind]
    text = ledger.read_text()
    ledger.write_text(re.sub(r"(T1: start sha=)\S+", rf"\g<1>{start}", text))
    (repo / "a.txt").write_text("attempt\n")
    before = snapshot(repo)
    r = run_block(repo, ledger)
    assert r.returncode == 2 and "REFUSED no-snapshot" in r.stdout, r
    assert snapshot(repo) == before and refs(repo) == ""


@pytest.mark.parametrize("tid", ["1.lock", "1..2"])
def test_rid_encoding_for_dotted_ids(tmp_path, tid):
    repo, ledger, q0 = setup(tmp_path, tid=tid)
    rid = tid.replace(".", "_2e")
    (repo / "a.txt").write_text("attempt\n")
    r = run_block(repo, ledger)
    sweep = f"refs/superclaude/implement/{SLUG}/retry/T{rid}/sweep-2-1"
    assert r.returncode == 0 and f"SWEEP {sweep}" in r.stdout, r
    assert git(repo, "cat-file", "-t", sweep).stdout.strip() == "tree"
    # the checkpoint ref name for the same id is writable too
    git(repo, "update-ref", f"refs/superclaude/implement/{SLUG}/retry/T{rid}/a2", q0)
    assert sweep in refs(repo)


def test_checkpoint_ref_holds_tree_without_identity(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "a.txt").write_text("attempt\n")
    noid = _env(identity=False)
    assert "GIT_AUTHOR_NAME" not in noid
    tree = snapshot(repo, identity=False)  # bare tree, no commit object
    ref = f"refs/superclaude/implement/{SLUG}/retry/T1/a2"
    git(repo, "update-ref", ref, tree, env=noid)
    git(repo, "gc", "--prune=now", "-q", env=noid)
    assert git(repo, "cat-file", "-t", tree, env=noid).stdout.strip() == "tree"
    assert git(repo, "rev-parse", ref, env=noid).stdout.strip() == tree
    # an unreferenced tree from the same sequence is gone after the same gc
    (repo / "b.txt").write_text("other\n")
    orphan = snapshot(repo, identity=False)
    git(repo, "gc", "--prune=now", "-q", env=noid)
    assert git(repo, "cat-file", "-e", orphan, env=noid, check=False).returncode != 0


# --- domain, restore and verify ---------------------------------------------------
def put(repo, rel, text="x\n", mode=None):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    if mode:
        p.chmod(mode)
    return p


def outside_run(repo, q0):
    """Paths that differ from the Q0 tree, ignoring the run folder."""
    out = git(repo, "diff", "--name-only", "--no-renames", q0, snapshot(repo)).stdout
    return [p for p in out.splitlines() if not p.startswith(RUN + "/")]


def test_restore_from_bare_tree(tmp_path):
    def prep(repo):
        put(repo, "a.txt", "q0 edit\n")  # uncommitted at Q0
        put(repo, "u.txt", "untracked at q0\n")
        put(repo, "tool.sh", "#!/bin/sh\n", 0o755)

    repo, ledger, q0 = setup(tmp_path, prep=prep)
    put(repo, "a.txt", "attempt\n")
    put(repo, "u.txt", "attempt\n")
    put(repo, "tool.sh", "attempt\n", 0o644)
    put(repo, "new.txt", "attempt\n")
    cached = git(repo, "diff", "--cached").stdout
    r = run_block(repo, ledger)
    assert r.returncode == 0, r
    for line in ("RESTORED a.txt", "RESTORED u.txt", "DELETED new.txt", "DONE"):
        assert line in r.stdout.splitlines(), r.stdout
    assert (repo / "a.txt").read_text() == "q0 edit\n"
    assert (repo / "u.txt").read_text() == "untracked at q0\n"
    assert not (repo / "new.txt").exists()
    assert os.access(repo / "tool.sh", os.X_OK)
    assert outside_run(repo, q0) == []
    assert git(repo, "diff", "--cached").stdout == cached  # user index untouched
    done = repo / RUN / "retries/T1/revert-2.done"
    assert done.read_text().strip() == q0


def test_restore_symlink_and_type_swaps(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "o.txt").write_text("outside\n")

    def prep(repo):
        put(repo, "real.txt", "real\n")
        (repo / "link").symlink_to("real.txt")
        put(repo, "f", "file\n")
        put(repo, "d/x.txt", "in dir\n")
        put(repo, "sd/s.txt", "in sd\n")

    repo, ledger, q0 = setup(tmp_path, prep=prep)
    (repo / "link").unlink()
    put(repo, "link", "now a file\n")  # symlink -> file
    (repo / "f").unlink()
    put(repo, "f/g.txt", "now a dir\n")  # file -> directory
    for p in (repo / "d/x.txt",):
        p.unlink()
    (repo / "d").rmdir()
    put(repo, "d", "now a file\n")  # directory -> file
    for p in (repo / "sd/s.txt",):
        p.unlink()
    (repo / "sd").rmdir()
    (repo / "sd").symlink_to(outside, target_is_directory=True)  # dir -> symlink out
    before = sorted(p.name for p in outside.iterdir())
    r = run_block(repo, ledger)
    assert r.returncode == 0, r
    assert (repo / "link").is_symlink() and os.readlink(repo / "link") == "real.txt"
    assert (repo / "f").is_file() and (repo / "f").read_text() == "file\n"
    assert (repo / "d").is_dir() and (repo / "d/x.txt").read_text() == "in dir\n"
    assert (repo / "sd").is_dir() and not (repo / "sd").is_symlink()
    assert (repo / "sd/s.txt").read_text() == "in sd\n"
    assert sorted(p.name for p in outside.iterdir()) == before  # nothing written out
    assert (outside / "o.txt").read_text() == "outside\n"
    assert outside_run(repo, q0) == []


@pytest.mark.parametrize("target", ["keep.txt", ".dev/x"])  # in scope / fixed exclusion
def test_post_revert_verify_reports_residue(tmp_path, target):
    # an rm shim that edits a path outside the domain
    def prep(repo):
        put(repo, target, "keep\n")

    repo, ledger, q0 = setup(tmp_path, prep=prep)
    put(repo, "new.txt", "attempt\n")
    shim = tmp_path / "shim"
    shim.mkdir()
    real_rm = subprocess.run(
        ["bash", "-c", "command -v rm"], capture_output=True, text=True
    ).stdout.strip()
    (shim / "rm").write_text(
        f'#!/bin/bash\n{real_rm} "$@"\necho tampered >> "{repo}/{target}"\n'
    )
    (shim / "rm").chmod(0o755)
    r = run_block(repo, ledger, PATH=f"{shim}:{os.environ['PATH']}")
    assert r.returncode == 3 and f"RESIDUE {target}" in r.stdout.splitlines(), r
    assert "DONE" not in r.stdout
    assert not (repo / RUN / "retries/T1/revert-2.done").exists()


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
def test_post_revert_verify_reports_residue_for_failed_restore(tmp_path):
    def prep(repo):
        put(repo, "ro/f.txt", "q0\n")

    repo, ledger, _ = setup(tmp_path, prep=prep)
    put(repo, "ro/f.txt", "attempt\n")
    (repo / "ro").chmod(0o555)  # restore cannot replace the file
    try:
        r = run_block(repo, ledger)
    finally:
        (repo / "ro").chmod(0o755)
    assert r.returncode == 3 and "RESIDUE ro/f.txt" in r.stdout.splitlines(), r
    assert not (repo / RUN / "retries/T1/revert-2.done").exists()


def test_foreign_dev_files_untouched_across_two_reverts(tmp_path):
    def prep(repo):
        put(repo, ".dev/x", "q0\n")
        put(repo, ".dev/own.txt", "q0\n")

    repo, ledger, q0 = setup(tmp_path, prep=prep)
    put(repo, ".dev/x", "foreign edit\n")  # someone else, after Q0
    put(repo, ".dev/own.txt", "attempt\n")  # this task's own file
    put(repo, "a.txt", "attempt 2\n")
    r = run_block(repo, ledger, OWN_FILES=".dev/own.txt")
    assert r.returncode == 0, r
    assert (repo / ".dev/x").read_text() == "foreign edit\n"
    assert (repo / ".dev/own.txt").read_text() == "q0\n"
    # attempt 3 fails too: a second revert, same task, k = 3
    put(repo, "a.txt", "attempt 3\n")
    put(repo, ".dev/own.txt", "attempt 3\n")
    put(repo, ".dev/x", "foreign edit 2\n")
    put(repo, "evidence", "review\n")
    (repo / RUN / "retries/T1/review-3.md").write_text("verdict: missing\n")
    write_ledger(ledger, "1", q0, n=4)
    r = run_block(repo, ledger, OWN_FILES=".dev/own.txt")
    assert r.returncode == 0, r
    assert (repo / ".dev/x").read_text() == "foreign edit 2\n"
    assert (repo / ".dev/own.txt").read_text() == "q0\n"
    assert (repo / "a.txt").read_text() == "base\n"
    assert not (repo / "evidence").exists()


def test_ledger_outside_run_dir_survives_revert(tmp_path):
    other = ".dev/implement/other/progress.md"
    repo, ledger, _ = setup(tmp_path, ledger_rel=other)
    put(repo, "a.txt", "attempt\n")
    lines = ledger.read_text()
    r = run_block(repo, ledger)
    assert r.returncode == 0, r
    assert ledger.read_text() == lines  # header, start line and every later line
    assert "T1: start sha=" in ledger.read_text()
    assert (repo / "a.txt").read_text() == "base\n"


def test_retries_and_troubleshoot_untouched(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    put(repo, "a.txt", "attempt\n")
    put(repo, RUN + "/retries/T1/approach-2.md", "claims\n")
    put(repo, RUN + "/retries/T1_brief-3.md", "brief\n")
    put(repo, ".dev/troubleshoot/report.md", "report\n")
    put(repo, RUN + "/notes.md", "run folder\n")
    r = run_block(repo, ledger)
    assert r.returncode == 0, r
    assert (repo / RUN / "retries/T1/approach-2.md").read_text() == "claims\n"
    assert (repo / RUN / "retries/T1_brief-3.md").read_text() == "brief\n"
    assert (repo / ".dev/troubleshoot/report.md").read_text() == "report\n"
    assert (repo / RUN / "notes.md").read_text() == "run folder\n"
    assert (repo / "a.txt").read_text() == "base\n"


def test_revert_from_subdirectory_covers_top_level(tmp_path):
    def prep(repo):
        put(repo, "sub/b.txt", "q0\n")

    repo, ledger, q0 = setup(tmp_path, prep=prep)
    put(repo, "a.txt", "attempt\n")
    put(repo, "sub/b.txt", "attempt\n")
    put(repo, "top-new.txt", "attempt\n")
    r = run_block(repo, ledger, cwd=repo / "sub")
    assert r.returncode == 0, r
    assert (repo / "a.txt").read_text() == "base\n"
    assert (repo / "sub/b.txt").read_text() == "q0\n"
    assert not (repo / "top-new.txt").exists()
    assert outside_run(repo, q0) == []


def test_glob_and_colon_paths_reverted_literally(tmp_path):
    def prep(repo):
        put(repo, "specs/[v2].md", "source q0\n")
        put(repo, "specs/v.md", "q0\n")
        put(repo, "specs/[v2].md.bak", "q0\n")
        put(repo, ":foo", "q0\n")

    repo, ledger, q0 = setup(tmp_path, prep=prep)
    for rel in ("specs/[v2].md", "specs/v.md", "specs/[v2].md.bak", ":foo"):
        put(repo, rel, "attempt\n")
    r = run_block(repo, ledger, SOURCE="specs/[v2].md")
    assert r.returncode == 0, r
    # only the source file itself is excluded; glob-lookalikes and ':foo' are reverted
    assert (repo / "specs/[v2].md").read_text() == "attempt\n"
    assert (repo / "specs/v.md").read_text() == "q0\n"
    assert (repo / "specs/[v2].md.bak").read_text() == "q0\n"
    assert (repo / ":foo").read_text() == "q0\n"


def test_source_outside_repo_needs_no_exclude(tmp_path):
    src = tmp_path / "elsewhere" / "spec.md"
    src.parent.mkdir()
    src.write_text("spec\n")
    repo, ledger, _ = setup(tmp_path)
    src.write_text("edited\n")
    put(repo, "a.txt", "attempt\n")
    r = run_block(repo, ledger, SOURCE="")
    assert r.returncode == 0, r
    assert src.read_text() == "edited\n"  # never in the diff, never touched
    assert (repo / "a.txt").read_text() == "base\n"


def test_rename_lists_both_sides(tmp_path):
    repo, ledger, q0 = setup(tmp_path)
    (repo / "a.txt").rename(repo / "b.txt")
    r = run_block(repo, ledger)
    assert r.returncode == 0, r
    lines = r.stdout.splitlines()
    assert "RESTORED a.txt" in lines and "DELETED b.txt" in lines
    assert (repo / "a.txt").read_text() == "base\n" and not (repo / "b.txt").exists()
    assert outside_run(repo, q0) == []


def test_submodule_paths_excluded_and_listed(tmp_path):
    sub = tmp_path / "repo" / "sub"
    sub.mkdir(parents=True)
    git(sub, "init", "-q")
    put(sub, "s.txt", "s\n")
    git(sub, "add", "s.txt")
    git(sub, "commit", "-q", "-m", "s1")
    c1 = git(sub, "rev-parse", "HEAD").stdout.strip()

    def prep(repo):
        git(repo, "add", "sub")  # a gitlink
        git(repo, "commit", "-q", "-m", "add sub")

    repo = tmp_path / "repo"
    (repo / "a.txt").write_text("base\n")
    git(repo, "init", "-q")
    git(repo, "add", "a.txt")
    git(repo, "commit", "-q", "-m", "init")
    git(repo, "add", "sub")
    git(repo, "commit", "-q", "-m", "add sub")
    (repo / RUN / "retries/T1").mkdir(parents=True)
    ledger = header(repo)
    (repo / RUN / "retries/T1/q0-head").write_text(
        git(repo, "rev-parse", "HEAD").stdout
    )
    (repo / RUN / "retries/T1/review-2.md").write_text("verdict: missing\n")
    q0 = snapshot(repo)
    write_ledger(ledger, "1", q0)
    put(sub, "s.txt", "attempt\n")
    git(sub, "commit", "-q", "-am", "s2")  # the submodule moves on
    put(repo, "a.txt", "attempt\n")
    r = run_block(repo, ledger)
    assert r.returncode == 0, r
    assert f"SUBMODULE sub {c1}" in r.stdout.splitlines()
    assert git(sub, "rev-parse", "HEAD").stdout.strip() != c1  # left where it was
    assert (repo / "a.txt").read_text() == "base\n"


def test_revert_idempotent_after_partial_attempt(tmp_path):
    repo, ledger, q0 = setup(tmp_path)
    put(repo, "a.txt", "attempt 2\n")
    r1 = run_block(repo, ledger)
    assert r1.returncode == 0, r1
    # a crash during the next attempt left partial writes, including new paths
    put(repo, "a.txt", "partial 3\n")
    put(repo, "partial/only-in-a3.txt", "partial\n")
    r2 = run_block(repo, ledger)
    assert r2.returncode == 0, r2
    assert (repo / "a.txt").read_text() == "base\n"
    assert not (repo / "partial/only-in-a3.txt").exists()
    assert outside_run(repo, q0) == []
    assert "SWEEP" in r1.stdout and "sweep-2-2" in r2.stdout


def test_sweep_ref_create_only_and_kept_after_complete(tmp_path):
    repo, ledger, q0 = setup(tmp_path)
    prefix = f"refs/superclaude/implement/{SLUG}/retry/T1"
    git(repo, "update-ref", f"{prefix}/sweep-2-1", q0)  # taken: never overwritten
    put(repo, "a.txt", "attempt bytes\n")
    r = run_block(repo, ledger)
    assert r.returncode == 0 and f"SWEEP {prefix}/sweep-2-2" in r.stdout, r
    assert git(repo, "rev-parse", f"{prefix}/sweep-2-1").stdout.strip() == q0
    # a resumed revert whose tree equals an existing sweep ref keeps it, no new seq
    put(repo, "a.txt", "attempt bytes again\n")
    same = snapshot(repo)  # the block's own `now` is this tree: guards change nothing
    git(repo, "update-ref", f"{prefix}/sweep-2-3", same)
    r = run_block(repo, ledger)
    assert f"SWEEP {prefix}/sweep-2-3" in r.stdout and "sweep-2-4" not in refs(repo)
    # complete: the Q0 pin and checkpoint refs go, sweep refs stay and still hold the bytes
    pin = f"refs/superclaude/implement/{SLUG}/T1"
    git(repo, "update-ref", pin, q0)
    git(repo, "update-ref", f"{prefix}/a2", q0)
    for ref in (pin, f"{prefix}/a2"):
        git(repo, "update-ref", "-d", ref)
    git(repo, "gc", "--prune=now", "-q")
    assert "sweep-2-1" in refs(repo) and "sweep-2-2" in refs(repo)
    assert git(repo, "show", f"{prefix}/sweep-2-2:a.txt").stdout == "attempt bytes\n"


def test_revert_binds_target_from_ledger(tmp_path):
    repo, ledger, q0 = setup(tmp_path)
    put(repo, "a.txt", "attempt\n")
    decoy = git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()
    # a Q0 pin re-pointed to another tree, a decoy START/K/RID in the environment,
    # a Ruling after the revert record, and another task's start line
    git(repo, "update-ref", f"refs/superclaude/implement/{SLUG}/T1", decoy)
    with open(ledger, "a") as f:
        f.write("T1: Ruling: x — y — z\n")
    text = ledger.read_text()
    ledger.write_text(
        text.replace("T1: blocked", f"TaT1: start sha={'0' * 40}\nT1: blocked")
    )
    r = run_block(repo, ledger, START=decoy, K="9", RID="zz", TASK_DIR="zz")
    assert r.returncode == 0, r
    assert (
        repo / "a.txt"
    ).read_text() == "base\n"  # the start line's tree, not the decoy
    # UNBOUND: tail is another task's record, a step=open record, or RUN_DIR is empty
    put(repo, "a.txt", "attempt again\n")
    before, refs_before = snapshot(repo), refs(repo)
    for tail in (
        f"T2: start sha={'1' * 40}\n",
        f"T1: retry n=3 step=open checkpoint={'a' * 40} tier=unknown\n",
    ):
        saved = ledger.read_text()
        with open(ledger, "a") as f:
            f.write(tail)
        r = run_block(repo, ledger)
        assert r.returncode == 3 and r.stdout.strip() == "UNBOUND", (tail, r)
        ledger.write_text(saved)  # the test's own tail is the only difference
        assert snapshot(repo) == before and refs(repo) == refs_before
    r = run_block(repo, ledger, RUN_DIR="")
    assert r.returncode == 3 and r.stdout.strip() == "UNBOUND"
    assert snapshot(repo) == before
    # an abbreviated start sha is not a tree name
    saved = ledger.read_text()
    ledger.write_text(re.sub(r"(T1: start sha=)\S+", rf"\g<1>{q0[:12]}", saved))
    r = run_block(repo, ledger)
    assert r.returncode == 2 and "REFUSED no-snapshot" in r.stdout
    ledger.write_text(saved)  # the test's own edit is the only difference
    assert snapshot(repo) == before and refs(repo) == refs_before


def test_revert_targets_ledger_worktree_only(tmp_path):
    main = make_repo(tmp_path)
    wt = main / ".dev/worktrees/wt"
    git(main, "worktree", "add", "-q", str(wt), "-b", "wtbranch")
    (wt / RUN / "retries/T1").mkdir(parents=True)
    ledger = wt / RUN / "progress.md"
    ledger.write_text(
        "# implement ledger — source: notes.md — created: 2026-10-22T00:00:00Z\n"
    )
    (wt / RUN / "retries/T1/q0-head").write_text(git(wt, "rev-parse", "HEAD").stdout)
    (wt / RUN / "retries/T1/review-2.md").write_text("verdict: missing\n")
    q0 = snapshot(wt)
    write_ledger(ledger, "1", q0)
    put(wt, "a.txt", "linked attempt\n")
    put(main, "a.txt", "main edit\n")
    main_before = snapshot(main)
    r = run_block(main, ledger, cwd=main)  # runs from the main worktree's directory
    assert r.returncode == 0, r
    assert (wt / "a.txt").read_text() == "base\n"
    assert (main / "a.txt").read_text() == "main edit\n"
    assert snapshot(main) == main_before


# --- failed-attempt artifacts ----------------------------------------------------
ART = RUN + "/artifacts"
SAVED = RUN + "/retries/T1/artifacts-2"


def art(repo, rel, text="cited\n"):
    return put(repo, f"{ART}/{rel}", text)


def move_head(repo):
    """HEAD moves after Q0 (a commit made during the attempt)."""
    (repo / "committed.txt").write_text("c\n")
    git(repo, "add", "committed.txt")
    git(repo, "commit", "-q", "-m", "attempt commit")


def test_head_moved_halts_before_revert(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    cited = art(repo, "t1-test.log")
    put(repo, "a.txt", "attempt\n")
    move_head(repo)
    before = snapshot(repo)
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log")
    assert r.returncode == 2 and "REFUSED head-moved" in r.stdout, r
    assert cited.read_text() == "cited\n"  # the cited file is still in place
    assert not (repo / SAVED).exists()
    assert (repo / "a.txt").read_text() == "attempt\n" and refs(repo) == ""
    assert snapshot(repo) == before


def test_failed_attempt_artifacts_moved(tmp_path):
    repo, ledger, q0 = setup(tmp_path)
    art(repo, "t1-test.log", "log one\n")
    art(repo, "sub/x.log", "nested\n")
    art(repo, "retries/T1_brief-3.md", "brief\n")
    put(repo, "a.txt", "attempt\n")
    tokens = "\n".join(
        [
            "./artifacts/t1-test.log",
            "./artifacts/sub/x.log",
            "./artifacts/retries/T1_brief-3.md",  # never moved
            "./artifacts/gone.log",  # no longer exists: skipped silently
            "./artifacts/../a.txt",  # not under artifacts/: refused
        ]
    )
    r = run_block(repo, ledger, ARTIFACTS=tokens)
    assert r.returncode == 0, r
    lines = r.stdout.splitlines()
    assert f"MOVED ./artifacts/t1-test.log -> {SAVED}/t1-test.log" in lines
    assert f"MOVED ./artifacts/sub/x.log -> {SAVED}/sub/x.log" in lines
    assert not any("gone.log" in x or "brief" in x or "a.txt ->" in x for x in lines)
    assert (repo / SAVED / "t1-test.log").read_text() == "log one\n"
    assert (repo / SAVED / "sub/x.log").read_text() == "nested\n"
    assert not (repo / ART / "t1-test.log").exists()
    assert (repo / ART / "retries/T1_brief-3.md").read_text() == "brief\n"
    # second revert (k = 3): a named file already moved by the first one is skipped
    art(repo, "t3.log", "attempt three\n")
    (repo / RUN / "retries/T1/review-3.md").write_text("verdict: missing\n")
    write_ledger(ledger, "1", q0, n=4)
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log\n./artifacts/t3.log")
    assert r.returncode == 0, r
    assert not any("t1-test.log" in x for x in r.stdout.splitlines())
    assert (
        repo / RUN / "retries/T1/artifacts-3/t3.log"
    ).read_text() == "attempt three\n"
    assert (repo / SAVED / "t1-test.log").read_text() == "log one\n"
    # no done file and an occupied destination: moved to <p>.dup-<seq>, nothing overwritten
    (tmp_path / "second").mkdir()
    repo2, ledger2, _ = setup(tmp_path / "second")
    old = repo2 / SAVED / "t1-test.log"
    old.parent.mkdir(parents=True)
    old.write_text("old\n")
    art(repo2, "t1-test.log", "new\n")
    r = run_block(repo2, ledger2, ARTIFACTS="./artifacts/t1-test.log")
    assert r.returncode == 0, r
    assert f"MOVED ./artifacts/t1-test.log -> {SAVED}.dup-1/t1-test.log" in r.stdout
    assert old.read_text() == "old\n"
    assert (repo2 / (SAVED + ".dup-1") / "t1-test.log").read_text() == "new\n"


def test_resumed_guard_refusal_moves_artifacts_back(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    # a crashed earlier run moved these into artifacts-2 and never wrote revert-2.done
    for rel in ("t1-test.log", "sub/x.log", "clash.log"):
        put(repo, f"{SAVED}/{rel}", f"saved {rel}\n")
    put(repo, f"{SAVED}.dup-1/dup.log", "saved dup\n")
    art(repo, "clash.log", "newer file at the original path\n")
    move_head(repo)
    r = run_block(repo, ledger)
    lines = r.stdout.splitlines()
    assert r.returncode == 2 and "REFUSED head-moved" in lines, r
    assert "UNMOVED ./artifacts/t1-test.log" in lines
    assert "UNMOVED ./artifacts/sub/x.log" in lines
    assert (
        "UNMOVED ./artifacts/dup.log" in lines
    )  # a collision-folder file goes back to its path below the folder
    assert (repo / ART / "dup.log").read_text() == "saved dup\n"
    assert "UNMOVED-CLASH ./artifacts/clash.log" in lines
    assert (repo / ART / "t1-test.log").read_text() == "saved t1-test.log\n"
    assert (repo / ART / "sub/x.log").read_text() == "saved sub/x.log\n"
    # a file already at the original path is not overwritten; the saved one stays put
    assert (repo / ART / "clash.log").read_text() == "newer file at the original path\n"
    assert (repo / SAVED / "clash.log").read_text() == "saved clash.log\n"
    assert not (repo / SAVED / "t1-test.log").exists()
    assert refs(repo) == ""  # still no sweep ref, nothing restored


def test_finished_revert_refusal_keeps_artifacts(tmp_path):
    repo, ledger, q0 = setup(tmp_path)
    art(repo, "t1-test.log", "log one\n")
    put(repo, "a.txt", "attempt\n")
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log")
    assert r.returncode == 0 and (repo / RUN / "retries/T1/revert-2.done").is_file(), r
    # procedure step 7 begins; the partial attempt n commits, then the run resumes
    put(repo, "a.txt", "partial attempt three\n")
    move_head(repo)
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log")
    lines = r.stdout.splitlines()
    assert r.returncode == 2 and "REFUSED head-moved" in lines, r
    assert f"ARTIFACTS-KEPT {RUN}/retries/T1/artifacts-2/" in lines
    assert not any(x.startswith("UNMOVED") for x in lines)
    assert (repo / SAVED / "t1-test.log").read_text() == "log one\n"  # stays saved
    assert not (repo / ART / "t1-test.log").exists()


def test_rerun_after_finished_revert_skips_artifact_move(tmp_path):
    repo, ledger, q0 = setup(tmp_path)
    art(repo, "t1-test.log", "attempt k file\n")
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log")
    assert r.returncode == 0, r
    saved = repo / SAVED / "t1-test.log"
    assert saved.read_text() == "attempt k file\n"
    # partial attempt n writes a file under the same name, then a resume runs the block
    art(repo, "t1-test.log", "attempt n file\n")
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log")
    assert r.returncode == 0, r
    assert "MOVE-SKIPPED revert-2.done" in r.stdout.splitlines()
    assert "MOVED" not in r.stdout
    assert saved.read_text() == "attempt k file\n"  # byte-identical
    assert (repo / ART / "t1-test.log").read_text() == "attempt n file\n"
    # a done file holding another sha does not skip the move (and never overwrites)
    (repo / RUN / "retries/T1/revert-2.done").write_text("f" * 40 + "\n")
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t1-test.log")
    assert "MOVE-SKIPPED" not in r.stdout
    assert f"MOVED ./artifacts/t1-test.log -> {SAVED}.dup-1/t1-test.log" in r.stdout
    assert saved.read_text() == "attempt k file\n"
    assert (repo / (SAVED + ".dup-1") / "t1-test.log").read_text() == "attempt n file\n"


# --- regression tests for the .dup-<n> move-back bug (appended to tests/skills/test_implement_retry_revert.py) ---
DUP1 = SAVED + ".dup-1"


def _crash_after_forward_move(tmp_path, names):
    """Cite and move ``names`` forward, then drop revert-2.done and move HEAD (a resumed refusal)."""
    repo, ledger, _ = setup(tmp_path)
    for n in names:
        art(repo, n, f"{n}\n")
    r = run_block(repo, ledger, ARTIFACTS="\n".join(f"./artifacts/{n}" for n in names))
    assert r.returncode == 0, r
    (repo / RUN / "retries/T1/revert-2.done").unlink()
    move_head(repo)
    return repo, ledger


def test_real_dup_named_artifact_moves_back_under_its_own_name(tmp_path):
    names = ["report.dup-1", "report", "report.dup-1.dup-1", "sub/x.dup-12"]
    repo, ledger = _crash_after_forward_move(tmp_path, names)
    r = run_block(repo, ledger)
    lines = r.stdout.splitlines()
    assert r.returncode == 2 and "REFUSED head-moved" in lines, r
    for n in names:
        assert f"UNMOVED ./artifacts/{n}" in lines, lines
        assert (repo / ART / n).read_text() == f"{n}\n"
    assert not any("CLASH" in x for x in lines), lines


def test_collision_copy_keeps_its_name_in_a_collision_folder(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    put(repo, f"{SAVED}/report", "occupant\n")
    art(repo, "report", "second\n")
    art(repo, "report.dup-1", "real name\n")
    r = run_block(
        repo, ledger, ARTIFACTS="./artifacts/report\n./artifacts/report.dup-1"
    )
    assert r.returncode == 0, r
    assert f"MOVED ./artifacts/report -> {DUP1}/report" in r.stdout
    assert f"MOVED ./artifacts/report.dup-1 -> {SAVED}/report.dup-1" in r.stdout
    (repo / RUN / "retries/T1/revert-2.done").unlink()
    move_head(repo)
    r = run_block(repo, ledger)
    lines = r.stdout.splitlines()
    assert (repo / ART / "report").read_text() == "occupant\n"  # base folder first
    assert (repo / ART / "report.dup-1").read_text() == "real name\n"
    assert (repo / DUP1 / "report").read_text() == "second\n"  # kept, never overwritten
    assert lines.count("UNMOVED-CLASH ./artifacts/report") == 1, lines


def test_symlink_artifact_moves_back_as_a_symlink(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    put(repo, f"{ART}/target.log", "t\n")
    (repo / ART / "link.log").symlink_to("target.log")
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/link.log")
    assert r.returncode == 0 and (repo / SAVED / "link.log").is_symlink(), r
    (repo / RUN / "retries/T1/revert-2.done").unlink()
    move_head(repo)
    r = run_block(repo, ledger)
    assert "UNMOVED ./artifacts/link.log" in r.stdout.splitlines(), r.stdout
    assert (repo / ART / "link.log").is_symlink()


def test_failed_moveback_is_named_on_stdout(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    put(repo, f"{SAVED}/sub/x.log", "saved\n")
    put(repo, f"{ART}/sub", "a file where the directory must be\n")
    move_head(repo)
    r = run_block(repo, ledger)
    assert r.returncode == 2
    assert "UNMOVED-CLASH ./artifacts/sub/x.log" in r.stdout.splitlines(), r.stdout
    assert (repo / SAVED / "sub/x.log").read_text() == "saved\n"


def test_symlinked_parent_never_moves_a_file_across_the_package(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "f.txt").write_text("outside\n")
    repo, ledger, _ = setup(tmp_path)
    (repo / ART).mkdir(parents=True)
    (repo / ART / "linkdir").symlink_to(outside, target_is_directory=True)
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/linkdir/f.txt")  # forward
    assert (outside / "f.txt").read_text() == "outside\n"
    assert not (repo / SAVED / "linkdir/f.txt").exists()
    (repo / RUN / "retries/T1/revert-2.done").unlink()  # a crashed run: never finished
    put(repo, f"{SAVED}/linkdir/deep/f.txt", "saved\n")  # move-back
    move_head(repo)
    r = run_block(repo, ledger)
    assert "UNMOVED-CLASH ./artifacts/linkdir/deep/f.txt" in r.stdout.splitlines(), (
        r.stdout
    )
    assert sorted(p.name for p in outside.iterdir()) == [
        "f.txt"
    ]  # nothing created behind the link


def test_forward_move_never_writes_through_a_symlinked_save_folder(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    repo, ledger, _ = setup(tmp_path)
    (repo / RUN / "retries/T1").mkdir(parents=True, exist_ok=True)
    (repo / SAVED).symlink_to(
        outside, target_is_directory=True
    )  # artifacts-2 -> outside
    art(repo, "t.log", "cited\n")
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t.log")
    assert r.returncode == 0, r
    assert list(outside.iterdir()) == []  # nothing written through the link
    assert f"MOVED ./artifacts/t.log -> {DUP1}/t.log" in r.stdout
    assert (repo / DUP1 / "t.log").read_text() == "cited\n"


def test_only_numeric_collision_folders_are_read_and_path_is_literal(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    put(repo, f"{SAVED}.dup-10/a.log", "ten\n")
    put(repo, f"{SAVED}.dup-notes/b.log", "operator backup\n")  # not ours
    put(repo, f"{RUN}/retries/T1/artifacts-20/c.log", "other k\n")
    move_head(repo)
    r = run_block(repo, ledger)
    lines = r.stdout.splitlines()
    assert "UNMOVED ./artifacts/a.log" in lines
    assert not any("b.log" in x or "c.log" in x for x in lines), lines
    assert (repo / f"{SAVED}.dup-notes/b.log").read_text() == "operator backup\n"


def test_done_file_keeps_every_saved_folder(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    art(repo, "t.log", "k\n")
    r = run_block(repo, ledger, ARTIFACTS="./artifacts/t.log")
    assert r.returncode == 0, r
    put(repo, f"{DUP1}/t.log", "dup\n")
    move_head(repo)
    r = run_block(repo, ledger)
    lines = r.stdout.splitlines()
    assert r.returncode == 2
    assert f"ARTIFACTS-KEPT {SAVED}/" in lines and f"ARTIFACTS-KEPT {DUP1}/" in lines, (
        lines
    )
    assert not any(x.startswith("UNMOVED") for x in lines)


def test_nothing_is_lost_or_overwritten_on_moveback(tmp_path):
    repo, ledger, _ = setup(tmp_path)
    put(repo, f"{SAVED}/r", "1\n")
    put(repo, f"{SAVED}/r.dup-1", "2\n")
    put(repo, f"{DUP1}/r", "3\n")
    put(repo, f"{DUP1}/r.dup-1", "4\n")
    art(repo, "r.dup-1", "pre-existing\n")
    move_head(repo)

    def bytes_under(root):
        return sorted(p.read_text() for p in root.rglob("*") if p.is_file())

    before = bytes_under(repo / RUN)
    r = run_block(repo, ledger)
    assert bytes_under(repo / RUN) == before, r.stdout
    assert (repo / ART / "r").read_text() == "1\n"
    assert (repo / ART / "r.dup-1").read_text() == "pre-existing\n"


def test_repo_path_with_glob_chars_and_failglob(tmp_path):
    base = tmp_path / "w[ab]*"
    base.mkdir()
    repo, ledger, _ = setup(base)
    put(repo, f"{SAVED}/a.log", "a\n")
    put(repo, f"{SAVED}.dup-1/y.log", "y\n")
    move_head(repo)
    r = run_block(repo, ledger, BASHOPTS="failglob")
    lines = r.stdout.splitlines()
    assert (
        r.returncode == 2
        and "UNMOVED ./artifacts/a.log" in lines
        and "UNMOVED ./artifacts/y.log" in lines
    ), r
