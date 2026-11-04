"""Hermetic real-git tests for the conflict scripts (design section 12.4).

This module covers ``scripts/probe-merge.sh`` (cases P1 to P12),
``scripts/finish-merge.sh`` (cases F1 to F12) and
``scripts/collect-conflict-evidence.sh`` (cases E1 to E4) and
``scripts/poll-ci-checks.sh --evidence-sha`` (cases C1 to C4). Every git call runs
inside a pytest temporary directory, with a local bare repository as ``origin`` and a
``gh`` stub first on ``PATH``. ``GIT_CONFIG_GLOBAL=/dev/null``, ``GIT_CONFIG_NOSYSTEM=1``
and a fixed author and committer are set for every git call; ``HOME`` points into the
temporary directory. Nothing here touches the network or the operator's ``~/.claude``.
Probe output is parsed with ``conflicts.parse_probe`` and ``conflicts.conflict_plan``.
"""

from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from superclaude.pr_submit.conflicts import (
    MAX_PROBE_BYTES,
    MergeTreeListing,
    conflict_plan,
    finish_manifest,
    group_entries,
    merge_parent_ok,
    merge_preflight_ok,
    parse_probe,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
PROBE = SKILL_DIR / "scripts" / "probe-merge.sh"
PROBE_REL = "src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh"
FINISH = SKILL_DIR / "scripts" / "finish-merge.sh"
FINISH_REL = "src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh"

GIT = shutil.which("git")

_FIXED_IDENTITY = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Probe Test",
    "GIT_AUTHOR_EMAIL": "probe-test@example.com",
    "GIT_COMMITTER_NAME": "Probe Test",
    "GIT_COMMITTER_EMAIL": "probe-test@example.com",
    "GIT_TERMINAL_PROMPT": "0",
    "LC_ALL": "C",
}


def _base_env(home: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(_FIXED_IDENTITY)
    env["HOME"] = str(home)
    return env


def _merge_tree_works() -> bool:
    """Capability by behaviour (never a version parse): ``merge-tree --write-tree``."""
    if GIT is None or shutil.which("jq") is None or shutil.which("bash") is None:
        return False
    with tempfile.TemporaryDirectory() as scratch:
        env = _base_env(Path(scratch))
        repo = Path(scratch) / "r"
        try:
            for argv in (
                ["init", "-q", "-b", "main", str(repo)],
                ["-C", str(repo), "commit", "-q", "--allow-empty", "-m", "seed"],
                ["-C", str(repo), "merge-tree", "--write-tree", "HEAD", "HEAD"],
            ):
                subprocess.run(
                    [GIT, *argv], env=env, check=True, capture_output=True, timeout=30
                )
        except (subprocess.SubprocessError, OSError):
            return False
    return True


pytestmark = pytest.mark.skipif(
    not _merge_tree_works(),
    reason="git merge-tree --write-tree (or jq) is not available here",
)


# ---------------------------------------------------------------------------
# Fixture helper (design section 12.4)
# ---------------------------------------------------------------------------


@dataclass
class Repos:
    root: Path
    origin: Path  # bare repository used as `origin`
    seed: Path  # second clone that advances the base branch on origin
    work: Path  # clone with the PR branch `pr` checked out
    bin_dir: Path  # first on PATH; holds the gh stub
    gh_calls: Path
    env: dict[str, str]

    @property
    def repo_slug(self) -> str:
        """What the probe resolves from the origin URL (the `.git` suffix stripped)."""
        return re.sub(r"\.git$", "", str(self.origin))

    def git(self, cwd: Path, *args: str, check: bool = True) -> str:
        res = subprocess.run(
            [GIT, *args],
            cwd=cwd,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=60,
        )
        if check and res.returncode != 0:
            raise AssertionError(f"git {args} failed: {res.stderr}")
        return res.stdout

    def write(self, repo: Path, files: dict[str, bytes | str | None]) -> None:
        for rel, content in files.items():
            if content is None:
                self.git(repo, "rm", "-q", "--", rel)
                continue
            path = repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, bytes):
                path.write_bytes(content)
            else:
                path.write_text(content, encoding="utf-8")
        added = [rel for rel, content in files.items() if content is not None]
        if added:
            self.git(repo, "add", "--", *added)

    def commit(self, repo: Path, files: dict[str, bytes | str | None], msg: str) -> str:
        self.write(repo, files)
        self.git(repo, "commit", "-q", "-m", msg)
        return self.git(repo, "rev-parse", "HEAD").strip()

    def advance_base(self, files: dict[str, bytes | str | None]) -> str:
        sha = self.commit(self.seed, files, "base advance")
        self.git(self.seed, "push", "-q", "origin", "main:main")
        return sha

    def pr_commit(self, files: dict[str, bytes | str | None]) -> str:
        return self.commit(self.work, files, "pr change")

    def gh_call_lines(self) -> list[str]:
        if not self.gh_calls.exists():
            return []
        return self.gh_calls.read_text(encoding="utf-8").splitlines()


def make_repos(tmp_path: Path, base_files: dict[str, bytes | str] | None = None):
    """Create `origin.git` (bare), a `seed` clone on `main` and a `work` clone with
    the PR branch `pr` checked out, plus a `gh` stub on PATH that records calls and
    serves canned JSON."""
    home = tmp_path / "home"
    home.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    gh_calls = tmp_path / "gh-calls.log"
    gh = bin_dir / "gh"
    gh.write_text(
        "#!/usr/bin/env bash\n"
        f"printf '%s\\n' \"$*\" >> '{gh_calls}'\n"
        "printf '{}\\n'\n",
        encoding="utf-8",
    )
    gh.chmod(0o755)
    env = _base_env(home)
    env["PATH"] = f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"
    repos = Repos(
        root=tmp_path,
        origin=tmp_path / "origin.git",
        seed=tmp_path / "seed",
        work=tmp_path / "work",
        bin_dir=bin_dir,
        gh_calls=gh_calls,
        env=env,
    )
    repos.git(tmp_path, "init", "-q", "--bare", "-b", "main", str(repos.origin))
    repos.git(tmp_path, "init", "-q", "-b", "main", str(repos.seed))
    repos.git(repos.seed, "remote", "add", "origin", str(repos.origin))
    repos.commit(
        repos.seed,
        base_files or {"README.md": "readme\n", "f.txt": "line1\nline2\nline3\n"},
        "base",
    )
    repos.git(repos.seed, "push", "-q", "origin", "main:main")
    repos.git(tmp_path, "clone", "-q", str(repos.origin), str(repos.work))
    repos.git(repos.work, "checkout", "-q", "-b", "pr")
    return repos


# ---------------------------------------------------------------------------
# Probe runner
# ---------------------------------------------------------------------------


@dataclass
class ProbeRun:
    returncode: int
    stdout: str
    stderr: str

    @property
    def payload(self) -> dict:
        assert self.returncode == 0, self.stderr
        lines = self.stdout.splitlines()
        assert len(lines) == 1, self.stdout
        return json.loads(lines[0])


def _status(repos: Repos) -> str:
    """`git status --porcelain=v1 -z` without the optional index refresh, so the
    test itself never rewrites the index it compares."""
    return repos.git(
        repos.work, "--no-optional-locks", "status", "--porcelain=v1", "-z"
    )


def _snapshot(repos: Repos) -> tuple[str, str, bytes]:
    status = _status(repos)
    head = repos.git(repos.work, "rev-parse", "HEAD", check=False)
    index = repos.work / ".git" / "index"
    return status, head, index.read_bytes() if index.exists() else b""


def run_probe(repos: Repos, *args: str, env: dict[str, str] | None = None) -> ProbeRun:
    """Run the probe from its source path in `work`; assert it changed nothing."""
    before = _snapshot(repos)
    res = subprocess.run(
        [str(PROBE), *args],
        cwd=repos.work,
        env=env or repos.env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert _snapshot(repos) == before, "the probe changed status, HEAD or the index"
    assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
    assert repos.gh_call_lines() == [], "the probe must not call gh"
    return ProbeRun(res.returncode, res.stdout, res.stderr)


def full(repos: Repos, *extra: str, env: dict[str, str] | None = None) -> ProbeRun:
    return run_probe(
        repos, "--repo", repos.repo_slug, "--base", "main", *extra, env=env
    )


def _decode(payload: dict, key: str) -> str:
    return base64.b64decode(payload[key], validate=True).decode("utf-8")


def _content_conflict(repos: Repos) -> None:
    repos.advance_base({"f.txt": "line1\nTHEIRS\nline3\n"})
    repos.pr_commit({"f.txt": "line1\nOURS\nline3\n"})


# ---------------------------------------------------------------------------
# P1 to P12
# ---------------------------------------------------------------------------


def test_p1_base_advanced_without_overlap_is_clean(tmp_path):
    repos = make_repos(tmp_path)
    base_sha = repos.advance_base({"other.txt": "from base\n"})
    head_sha = repos.pr_commit({"pr.txt": "from pr\n"})
    payload = full(repos).payload
    probe = parse_probe(payload)
    assert payload["clean"] is True
    assert payload["numstat_ours_b64"] is None
    assert payload["numstat_theirs_b64"] is None
    assert probe.clean is True
    assert probe.behind > 0 and probe.behind == 1
    assert probe.ahead == 1
    assert probe.listing is not None and probe.listing.records == ()
    assert probe.base_sha == base_sha and probe.head_sha == head_sha
    assert probe.base_ref == "origin/main"
    assert probe.foreign_op is None and payload["merge_head"] is None
    plan = conflict_plan(hint="conflicting", probe=payload)
    assert (plan.tier, plan.reason) == (0, "no_conflict")


def test_p2_content_conflict_parses_stages_123(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    payload = full(repos).payload
    probe = parse_probe(payload)
    assert probe.clean is False
    entries = group_entries(probe.listing, probe.binary_paths)
    assert [(e.path, e.stages) for e in entries] == [("f.txt", "123")]
    plan = conflict_plan(hint="conflicting", probe=payload)
    assert re.fullmatch(r"[0-9a-f]{40}", plan.merge_tree_oid)
    assert (plan.tier, plan.reason) == (2, "text_conflict")
    assert plan.text_paths == ("f.txt",)


def test_p3_deleted_on_base_modified_on_pr_is_stages_12(tmp_path):
    repos = make_repos(tmp_path, {"d.txt": "keep\n", "README.md": "r\n"})
    repos.advance_base({"d.txt": None})
    repos.pr_commit({"d.txt": "modified\n"})
    payload = full(repos).payload
    probe = parse_probe(payload)
    entries = group_entries(probe.listing, probe.binary_paths)
    assert [(e.path, e.stages) for e in entries] == [("d.txt", "12")]
    plan = conflict_plan(hint="conflicting", probe=payload)
    assert plan.paths[0].cls == "text:modify_delete"


def test_p4_binary_changed_on_both_sides_is_binary(tmp_path):
    repos = make_repos(tmp_path, {"blob.bin": b"\x00\x01base\x00\xff", "r.md": "r\n"})
    repos.advance_base({"blob.bin": b"\x00\x02theirs\x00\xfe"})
    repos.pr_commit({"blob.bin": b"\x00\x03ours\x00\xfd"})
    payload = full(repos).payload
    probe = parse_probe(payload)
    assert "blob.bin" in probe.binary_paths
    plan = conflict_plan(hint="conflicting", probe=payload)
    assert (plan.tier, plan.reason) == (3, "halt:binary")


@pytest.mark.parametrize("staged", [True, False], ids=["staged", "unstaged"])
def test_p5_dirty_tracked_file_is_not_tree_clean(tmp_path, staged):
    repos = make_repos(tmp_path)
    (repos.work / "f.txt").write_text("dirty\n", encoding="utf-8")
    if staged:
        repos.git(repos.work, "add", "--", "f.txt")
    payload = full(repos).payload
    probe = parse_probe(payload)
    assert payload["tree_clean"] is False and probe.tree_clean is False
    assert "f.txt" in _decode(payload, "status_b64")
    assert "f.txt" in probe.status_porcelain


def test_p6_untracked_file_only_is_tree_clean(tmp_path):
    repos = make_repos(tmp_path)
    (repos.work / "untracked.txt").write_text("new\n", encoding="utf-8")
    payload = full(repos).payload
    assert payload["tree_clean"] is True
    assert payload["status_b64"] == ""
    assert parse_probe(payload).tree_clean is True


def test_p7_half_finished_rebase_is_a_foreign_op(tmp_path):
    repos = make_repos(tmp_path)
    (repos.work / ".git" / "rebase-merge").mkdir()
    payload = full(repos).payload
    assert payload["foreign_op"] == "rebase-merge"
    assert parse_probe(payload).foreign_op == "rebase-merge"
    ops = run_probe(repos, "--repo", repos.repo_slug, "--ops-only").payload
    assert ops == {
        "ok": True,
        "mode": "ops",
        "foreign_op": "rebase-merge",
        "merge_head": None,
    }


def _setup_clean(repos):
    repos.advance_base({"other.txt": "b\n"})
    repos.pr_commit({"pr.txt": "p\n"})


def _setup_conflict(repos):
    _content_conflict(repos)


def _setup_dirty(repos):
    _content_conflict(repos)
    (repos.work / "README.md").write_text("unstaged\n", encoding="utf-8")
    (repos.work / "f.txt").write_text("staged\n", encoding="utf-8")
    repos.git(repos.work, "add", "--", "f.txt")
    (repos.work / "untracked.txt").write_text("u\n", encoding="utf-8")


def _setup_rebase_dir(repos):
    _content_conflict(repos)
    (repos.work / ".git" / "rebase-merge").mkdir()


@pytest.mark.parametrize(
    "setup",
    [_setup_clean, _setup_conflict, _setup_dirty, _setup_rebase_dir],
    ids=["clean", "conflict", "dirty", "rebase-dir"],
)
def test_p8_probe_leaves_status_head_and_index_unchanged(tmp_path, setup):
    repos = make_repos(tmp_path)
    setup(repos)
    status_before = _status(repos)
    head_before = repos.git(repos.work, "rev-parse", "HEAD")
    branch_before = repos.git(repos.work, "branch", "--show-current")
    index_before = (repos.work / ".git" / "index").read_bytes()
    res = full(repos)
    assert res.returncode == 0, res.stderr
    assert _status(repos) == status_before
    assert repos.git(repos.work, "rev-parse", "HEAD") == head_before
    assert repos.git(repos.work, "branch", "--show-current") == branch_before
    assert (repos.work / ".git" / "index").read_bytes() == index_before
    assert not (repos.work / ".git" / "MERGE_HEAD").exists()


def _remote_main(repos: Repos) -> str:
    return repos.git(
        repos.work, "rev-parse", "-q", "--verify", "refs/remotes/origin/main"
    )


@pytest.mark.parametrize(
    "args, reason",
    [
        (("--base", "main"), "usage"),
        (("--repo", "IronbellyOrg/IronClaude", "--base", "main"), "origin_mismatch"),
        (("--repo", "IronbellyOrg/IronClaude", "--ops-only"), "origin_mismatch"),
    ],
    ids=["repo-missing", "repo-mismatch", "repo-mismatch-ops"],
)
def test_p9_usage_and_origin_mismatch_exit_2_without_fetch(tmp_path, args, reason):
    repos = make_repos(tmp_path)
    repos.advance_base({"other.txt": "b\n"})
    remote_before = _remote_main(repos)
    fetch_head = repos.work / ".git" / "FETCH_HEAD"
    fetch_head_before = fetch_head.exists()
    res = run_probe(repos, *args)
    assert res.returncode == 2
    assert res.stdout == f"PROBE_FAIL {reason}\n"
    assert _remote_main(repos) == remote_before, "a fetch happened"
    assert fetch_head.exists() == fetch_head_before, "a fetch happened"


def test_p10_unreachable_origin_is_fetch_failed(tmp_path):
    repos = make_repos(tmp_path)
    shutil.rmtree(repos.origin)
    res = full(repos)
    assert res.returncode == 2
    assert res.stdout == "PROBE_FAIL fetch_failed\n"
    assert "cannot reach remote origin" in res.stderr


def test_p11_merge_tree_unsupported_reports_null_clean(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    wrap_dir = tmp_path / "gitwrap"
    wrap_dir.mkdir()
    wrapper = wrap_dir / "git"
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        "mt=0; wt=0\n"
        'for a in "$@"; do\n'
        '  [ "$a" = merge-tree ] && mt=1\n'
        '  [ "$a" = --write-tree ] && wt=1\n'
        "done\n"
        'if [ "$mt" = 1 ] && [ "$wt" = 1 ]; then\n'
        "  echo 'error: unknown option write-tree' >&2; exit 129\n"
        "fi\n"
        f'exec "{GIT}" "$@"\n',
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    env = dict(repos.env)
    env["PATH"] = f"{wrap_dir}{os.pathsep}{env['PATH']}"
    payload = full(repos, env=env).payload
    assert payload["merge_tree_supported"] is False
    assert payload["clean"] is None
    for key in ("merge_tree_b64", "numstat_ours_b64", "numstat_theirs_b64"):
        assert payload[key] is None
    probe = parse_probe(payload)
    assert probe.merge_tree_supported is False and probe.clean is None
    plan = conflict_plan(hint="conflicting", probe=payload)
    assert (plan.tier, plan.reason) == (None, "merge_tree_unsupported")


def test_p12_conflict_listing_above_limit_is_truncated_tier3(tmp_path):
    names = [
        f"dir/conflicting-file-with-a-rather-long-name-{i:04d}.txt" for i in range(400)
    ]
    repos = make_repos(tmp_path, {n: "base\n" for n in names})
    repos.advance_base({n: "theirs\n" for n in names})
    repos.pr_commit({n: "ours\n" for n in names})
    payload = full(repos).payload
    assert payload["truncated"] is True
    for key in (
        "status_b64",
        "merge_tree_b64",
        "numstat_ours_b64",
        "numstat_theirs_b64",
    ):
        assert payload[key] is None
    assert payload["clean"] is False
    with pytest.raises(ValueError):
        parse_probe(payload)
    plan = conflict_plan(hint="conflicting", probe=payload)
    assert (plan.tier, plan.reason) == (3, "probe_malformed")
    # The untruncated listing really is above the limit (guards the setup).
    listing = subprocess.run(
        [GIT, "merge-tree", "--write-tree", "-z", "HEAD", "origin/main"],
        cwd=repos.work,
        env=repos.env,
        capture_output=True,
        timeout=60,
    ).stdout
    assert len(listing) > MAX_PROBE_BYTES


# ---------------------------------------------------------------------------
# Further contract rows of section 7.1
# ---------------------------------------------------------------------------


def test_ops_only_reports_a_real_merge_in_progress(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    clean_ops = run_probe(repos, "--repo", repos.repo_slug, "--ops-only").payload
    assert clean_ops == {
        "ok": True,
        "mode": "ops",
        "foreign_op": None,
        "merge_head": None,
    }
    repos.git(repos.work, "fetch", "-q", "origin", "main")
    base_sha = repos.git(repos.work, "rev-parse", "origin/main").strip()
    repos.git(repos.work, "merge", "--no-commit", "--no-ff", base_sha, check=False)
    ops = run_probe(repos, "--repo", repos.repo_slug, "--ops-only").payload
    assert ops["foreign_op"] == "MERGE_HEAD"
    assert ops["merge_head"] == base_sha


@pytest.mark.parametrize("base", ["a..b", "-main", "bad name"])
def test_bad_base_exits_2(tmp_path, base):
    repos = make_repos(tmp_path)
    res = run_probe(repos, "--repo", repos.repo_slug, "--base", base)
    assert res.returncode == 2
    assert res.stdout == "PROBE_FAIL bad_base\n"


def test_no_merge_base_exits_2(tmp_path):
    repos = make_repos(tmp_path)
    repos.git(repos.work, "checkout", "-q", "--orphan", "unrelated")
    repos.git(repos.work, "rm", "-q", "-r", "--cached", ".")
    for child in repos.work.iterdir():
        if child.name != ".git":
            child.unlink()
    repos.commit(repos.work, {"solo.txt": "solo\n"}, "unrelated root")
    res = full(repos)
    assert res.returncode == 2
    assert res.stdout == "PROBE_FAIL no_merge_base\n"


def test_missing_base_branch_on_origin_is_fetch_failed(tmp_path):
    repos = make_repos(tmp_path)
    res = run_probe(repos, "--repo", repos.repo_slug, "--base", "no-such-branch")
    assert res.returncode == 2
    assert res.stdout == "PROBE_FAIL fetch_failed\n"


def test_outside_a_work_tree_is_not_a_worktree(tmp_path):
    repos = make_repos(tmp_path)
    outside = tmp_path / "plain"
    outside.mkdir()
    env = dict(repos.env)
    env["GIT_CEILING_DIRECTORIES"] = str(tmp_path)
    res = subprocess.run(
        [str(PROBE), "--repo", repos.repo_slug, "--base", "main"],
        cwd=outside,
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert res.returncode == 2
    assert res.stdout == "PROBE_FAIL not_a_worktree\n"


def test_programs_lists_only_programs_on_path(tmp_path):
    repos = make_repos(tmp_path)
    payload = full(
        repos, "--program", "bash", "--program", "no-such-program-xyz-305"
    ).payload
    assert payload["programs"] == ["bash"]
    assert parse_probe(payload).programs == frozenset({"bash"})


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/IronbellyOrg/IronClaude.git",
        "git@github.com:IronbellyOrg/IronClaude.git",
        "ssh://git@github.com/IronbellyOrg/IronClaude.git",
        "https://github.com/IronbellyOrg/IronClaude",
    ],
)
def test_origin_url_forms_resolve_to_owner_repo(tmp_path, url):
    """The sed expression of the SKILL resolves every URL form; ops mode never fetches."""
    repos = make_repos(tmp_path)
    repos.git(repos.work, "remote", "set-url", "origin", url)
    ops = run_probe(repos, "--repo", "IronbellyOrg/IronClaude", "--ops-only").payload
    assert ops["ok"] is True and ops["mode"] == "ops"


# ---------------------------------------------------------------------------
# Static rules for the script (design section 7 preamble)
# ---------------------------------------------------------------------------


def test_probe_script_static_rules():
    text = PROBE.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env bash\n")
    assert "\nset -u -o pipefail\n" in text
    assert os.access(PROBE, os.X_OK)
    for pattern in (
        r"\bgit\s+push\b",
        r"\bstash\b",
        r"\bgit\s+config\b",
        r"--no-verify\b",
        r"--amend\b",
        r"--force\b",
        r"src/superclaude",
        r"\bgit\s+(checkout|switch|reset|commit|add|worktree|rebase)\b",
        r"\bgit\s+merge(\s|$)",
        r"\bgh\b",
    ):
        assert re.search(pattern, text) is None, pattern
    ls = subprocess.run(
        [GIT, "ls-files", "-s", "--", PROBE_REL],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    ).stdout
    if ls:  # the index entry exists once the path is staged
        assert ls.startswith("100755 "), ls


# ---------------------------------------------------------------------------
# finish-merge.sh helpers (design section 7.2)
# ---------------------------------------------------------------------------


@dataclass
class MergeSetup:
    base_sha: str
    old_head: str
    merge_tree_oid: str
    listing: MergeTreeListing


def _merge_head(repos: Repos) -> Path:
    return repos.work / ".git" / "MERGE_HEAD"


def _head(repos: Repos) -> str:
    return repos.git(repos.work, "rev-parse", "HEAD").strip()


def start_merge(repos: Repos) -> MergeSetup:
    """Probe (as the SKILL does), then run a real `git merge --no-commit --no-ff`."""
    payload = full(repos).payload
    probe = parse_probe(payload)
    assert probe.listing is not None
    old_head = _head(repos)
    repos.git(
        repos.work, "merge", "-q", "--no-commit", "--no-ff", probe.base_sha, check=False
    )
    assert _merge_head(repos).exists(), "the setup merge did not start"
    return MergeSetup(
        base_sha=probe.base_sha,
        old_head=old_head,
        merge_tree_oid=probe.listing.tree_oid,
        listing=probe.listing,
    )


def resolve(repos: Repos, files: dict[str, str]) -> None:
    repos.write(repos.work, files)


def run_finish(repos: Repos, *args: str) -> ProbeRun:
    res = subprocess.run(
        [str(FINISH), *args],
        cwd=repos.work,
        env=repos.env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
    assert repos.gh_call_lines() == [], "finish-merge must not call gh"
    assert len(res.stdout.splitlines()) == 1, res.stdout
    return ProbeRun(res.returncode, res.stdout, res.stderr)


MESSAGE = "Merge origin/main into pr (sc:pr-submit sync-1)\n\nResolved: f.txt\n"


def finish_commit(
    repos: Repos,
    setup: MergeSetup,
    resolved: list[str],
    *,
    base_sha: str | None = None,
) -> ProbeRun:
    manifest = repos.root / "manifest.txt"
    manifest.write_text(finish_manifest(setup.listing, resolved), encoding="utf-8")
    message = repos.root / "message.txt"
    message.write_text(MESSAGE, encoding="utf-8")
    return run_finish(
        repos,
        "--base-sha",
        base_sha or setup.base_sha,
        "--merge-tree-oid",
        setup.merge_tree_oid,
        "--manifest",
        str(manifest),
        "--message-file",
        str(message),
    )


def precheck(repos: Repos, base_sha: str) -> ProbeRun:
    return run_finish(repos, "--base-sha", base_sha, "--precheck")


def assert_fail(res: ProbeRun, reason: str) -> None:
    assert res.returncode == 2, (res.stdout, res.stderr)
    assert res.stdout == f"FINISH_FAIL {reason}\n", res.stderr


def assert_no_commit(repos: Repos, setup: MergeSetup) -> None:
    assert _head(repos) == setup.old_head, "a commit was made"
    assert _merge_head(repos).exists(), "the merge is no longer in progress"


def _two_file_conflict(repos: Repos) -> None:
    repos.advance_base({"f.txt": "line1\nTHEIRS\nline3\n", "g.txt": "g\nTHEIRS\n"})
    repos.pr_commit({"f.txt": "line1\nOURS\nline3\n", "g.txt": "g\nOURS\n"})


_BASE_FG = {
    "README.md": "readme\n",
    "f.txt": "line1\nline2\nline3\n",
    "g.txt": "g\n2\n",
}
RESOLVED_F = "line1\nOURS and THEIRS\nline3\n"


# ---------------------------------------------------------------------------
# F1 to F12
# ---------------------------------------------------------------------------


def test_f1_one_path_left_unmerged_is_unmerged(tmp_path):
    repos = make_repos(tmp_path, _BASE_FG)
    _two_file_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    res = finish_commit(repos, setup, ["f.txt", "g.txt"])
    assert_fail(res, "unmerged")
    assert "g.txt" in res.stderr
    assert_no_commit(repos, setup)


@pytest.mark.parametrize(
    "content",
    [None, "line1\n=======\nline3\n"],
    ids=["git-markers-left", "one-introduced-marker"],
)
def test_f2_introduced_marker_is_markers(tmp_path, content):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    if content is None:  # stage the file exactly as the merge left it
        repos.git(repos.work, "add", "--", "f.txt")
    else:
        resolve(repos, {"f.txt": content})
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "markers")
    assert_no_commit(repos, setup)


def test_f3_marker_already_in_stage1_blob_is_not_introduced(tmp_path):
    repos = make_repos(tmp_path, {"README.md": "r\n", "f.txt": "a\n=======\nb\n"})
    repos.advance_base({"f.txt": "a\n=======\nTHEIRS\n"})
    repos.pr_commit({"f.txt": "a\n=======\nOURS\n"})
    setup = start_merge(repos)
    manifest = finish_manifest(setup.listing, ["f.txt"])
    assert not manifest.startswith("-\t"), "f.txt must have a stage-1 blob"
    resolve(repos, {"f.txt": "a\n=======\nRESOLVED\n"})
    res = finish_commit(repos, setup, ["f.txt"])
    assert res.returncode == 0, res.stderr
    assert re.fullmatch(r"[0-9a-f]{40}", res.payload["merge_sha"])
    assert not _merge_head(repos).exists()


def test_f4_extra_staged_path_is_staged_unexpected(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F, "README.md": "sneaked in\n"})
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "staged_unexpected")
    assert "README.md" in res.stderr
    assert_no_commit(repos, setup)


def test_f5_auto_merged_path_reverted_to_head_is_staged_unexpected(tmp_path):
    repos = make_repos(tmp_path)
    repos.advance_base(
        {"f.txt": "line1\nTHEIRS\nline3\n", "README.md": "readme from base\n"}
    )
    repos.pr_commit({"f.txt": "line1\nOURS\nline3\n"})
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    # Undo the auto-merged base change in both the index and the work tree.
    repos.git(repos.work, "checkout", "-q", "HEAD", "--", "README.md")
    assert (repos.work / "README.md").read_text(encoding="utf-8") == "readme\n"
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "staged_unexpected")
    assert "README.md" in res.stderr
    assert_no_commit(repos, setup)


@pytest.mark.parametrize(
    "value, width",
    [("9", 9), ("010", 10), ("+9", 9), ("08", 8), ("9x", 9)],
    ids=["9", "leading-zero-010", "plus-sign", "leading-zero-08", "trailing-text"],
)
def test_wider_conflict_marker_size_left_in_place_is_markers(tmp_path, value, width):
    """git writes markers at the path's conflict-marker-size width, read as C atoi()
    reads it; the gate counts markers at that same width, so staging the file as the
    merge left it fails."""
    repos = make_repos(
        tmp_path,
        {
            "README.md": "readme\n",
            "f.txt": "line1\nline2\nline3\n",
            ".gitattributes": f"f.txt conflict-marker-size={value}\n",
        },
    )
    _content_conflict(repos)
    setup = start_merge(repos)
    left = (repos.work / "f.txt").read_text(encoding="utf-8")
    assert "<" * width + " " in left, f"git did not write {width}-wide markers"
    assert "<" * (width + 1) not in left
    repos.git(repos.work, "add", "--", "f.txt")
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "markers")
    assert_no_commit(repos, setup)


def test_unrelated_mode_change_is_staged_unexpected(tmp_path):
    """A staged mode change keeps the blob id; the gate compares the index with the
    merge tree entry by entry (mode included), so it fails."""
    repos = make_repos(
        tmp_path,
        {"README.md": "readme\n", "f.txt": "line1\nline2\nline3\n", "run.sh": "x\n"},
    )
    _content_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    (repos.work / "run.sh").chmod(0o755)
    repos.git(repos.work, "add", "--", "run.sh")
    assert repos.git(repos.work, "ls-files", "-s", "--", "run.sh").startswith("100755")
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "staged_unexpected")
    assert "run.sh" in res.stderr
    assert_no_commit(repos, setup)


def test_file_swapped_for_symlink_with_same_bytes_is_staged_unexpected(tmp_path):
    """A symlink whose target text equals the file content has the same blob id; the
    entry type differs from the merge tree, so the gate fails."""
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    readme = repos.work / "README.md"
    blob_before = repos.git(repos.work, "rev-parse", ":0:README.md").strip()
    readme.unlink()
    os.symlink("readme\n", readme)
    repos.git(repos.work, "add", "--", "README.md")
    assert repos.git(repos.work, "rev-parse", ":0:README.md").strip() == blob_before
    assert repos.git(repos.work, "ls-files", "-s", "--", "README.md").startswith(
        "120000"
    )
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "staged_unexpected")
    assert "README.md" in res.stderr
    assert_no_commit(repos, setup)


@pytest.mark.parametrize("mode", ["commit", "precheck"])
def test_f6_foreign_merge_and_no_merge_head(tmp_path, mode):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    payload = full(repos).payload
    probe = parse_probe(payload)
    setup = MergeSetup(
        base_sha=probe.base_sha,
        old_head=_head(repos),
        merge_tree_oid=probe.listing.tree_oid,
        listing=probe.listing,
    )

    def run(base_sha: str) -> ProbeRun:
        if mode == "precheck":
            return precheck(repos, base_sha)
        return finish_commit(repos, setup, ["f.txt"], base_sha=base_sha)

    # No merge in progress.
    assert_fail(run(setup.base_sha), "no_merge_head")
    assert _head(repos) == setup.old_head
    # A merge of something other than the recorded base tip.
    repos.git(
        repos.work, "merge", "-q", "--no-commit", "--no-ff", setup.base_sha, check=False
    )
    resolve(repos, {"f.txt": RESOLVED_F})
    other = repos.git(repos.work, "rev-parse", "HEAD~1").strip()
    assert_fail(run(other), "foreign_merge")
    assert_no_commit(repos, setup)


def test_f7_unstaged_edit_to_tracked_file_is_tree_dirty(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    (repos.work / "README.md").write_text("operator edit\n", encoding="utf-8")
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "tree_dirty")
    assert_no_commit(repos, setup)


def test_f8_precheck_tree_dirty_and_ok(tmp_path):
    repos = make_repos(tmp_path, _BASE_FG)
    _two_file_conflict(repos)
    setup = start_merge(repos)
    # Only the unmerged paths differ between the work tree and the index.
    ok = precheck(repos, setup.base_sha)
    assert ok.returncode == 0, ok.stderr
    assert ok.payload == {"precheck": "ok"}
    # A resolved, staged path is fine too.
    resolve(repos, {"f.txt": RESOLVED_F})
    assert precheck(repos, setup.base_sha).payload == {"precheck": "ok"}
    # An operator edit to a non-conflicted tracked file is not.
    (repos.work / "README.md").write_text("operator edit\n", encoding="utf-8")
    res = precheck(repos, setup.base_sha)
    assert_fail(res, "tree_dirty")
    assert "README.md" in res.stderr
    assert_no_commit(repos, setup)


def test_f9_failing_pre_commit_hook_is_hook_rejected(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    hook = repos.work / ".git" / "hooks" / "pre-commit"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook_output = "pre-commit: lint failed on f.txt\n  detail line 2 (#305)\n"
    hook.write_text(
        "#!/usr/bin/env bash\n"
        "printf 'pre-commit: lint failed on f.txt\\n'\n"
        "printf '  detail line 2 (#305)\\n' >&2\n"
        "exit 1\n",
        encoding="utf-8",
    )
    hook.chmod(0o755)
    res = finish_commit(repos, setup, ["f.txt"])
    assert_fail(res, "hook_rejected")
    assert hook_output in res.stderr
    assert_no_commit(repos, setup)


def test_f10_clean_resolution_is_the_exact_merge_commit(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    # --base-sha is compared case-insensitively with MERGE_HEAD.
    res = finish_commit(repos, setup, ["f.txt"], base_sha=setup.base_sha.upper())
    assert res.returncode == 0, res.stderr
    payload = res.payload
    assert set(payload) == {"merge_sha", "parents"}
    assert payload["merge_sha"] == _head(repos)
    assert payload["parents"] == [setup.old_head, setup.base_sha]
    rev_list = repos.git(repos.work, "rev-list", "--parents", "-n", "1", "HEAD").split()
    assert rev_list[0] == payload["merge_sha"]
    parents = rev_list[1:]
    assert parents == [setup.old_head, setup.base_sha]
    assert merge_parent_ok(parents, setup.old_head, setup.base_sha) is True
    assert _status(repos) == ""
    assert not _merge_head(repos).exists()
    body = repos.git(repos.work, "log", "-1", "--format=%B")
    assert body.rstrip("\n") == MESSAGE.rstrip("\n")
    assert repos.git(repos.work, "show", "HEAD:f.txt") == RESOLVED_F


def test_f11_merge_abort_after_a_halt_restores_the_pre_merge_state(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    (repos.work / "untracked.txt").write_text("keep me\n", encoding="utf-8")
    files = ("README.md", "f.txt", "untracked.txt")

    def state() -> tuple:
        return (
            _head(repos),
            repos.git(repos.work, "ls-files", "-s", "-z"),
            _status(repos),
            {p: (repos.work / p).read_bytes() for p in files},
        )

    before = state()
    setup = start_merge(repos)
    repos.git(repos.work, "add", "--", "f.txt")  # markers left: the gate halts
    assert_fail(finish_commit(repos, setup, ["f.txt"]), "markers")
    repos.git(repos.work, "merge", "--abort")
    assert state() == before
    assert not _merge_head(repos).exists()


def test_f12_dirty_pyproject_before_the_merge_blocks_it(tmp_path):
    repos = make_repos(
        tmp_path,
        {
            "README.md": "readme\n",
            "f.txt": "line1\nline2\nline3\n",
            "pyproject.toml": '[project]\nname = "x"\nversion = "0.1.0"\n',
        },
    )
    _content_conflict(repos)
    pr_head = _head(repos)
    (repos.work / "pyproject.toml").write_text(
        '[project]\nname = "x"\nversion = "0.2.0-local"\n', encoding="utf-8"
    )
    payload = full(repos).payload
    probe = parse_probe(payload)
    assert payload["tree_clean"] is False
    ok, paths = merge_preflight_ok(probe.status_porcelain)
    assert (ok, paths) == (False, ["pyproject.toml"])
    # The gate is false, so the flow never starts the merge: nothing was merged.
    assert not _merge_head(repos).exists()
    assert _head(repos) == pr_head
    ancestor = subprocess.run(
        [GIT, "merge-base", "--is-ancestor", probe.base_sha, "HEAD"],
        cwd=repos.work,
        env=repos.env,
        capture_output=True,
        timeout=30,
    )
    assert ancestor.returncode == 1
    assert_fail(precheck(repos, probe.base_sha), "no_merge_head")
    assert "0.2.0-local" in (repos.work / "pyproject.toml").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Further contract rows of section 7.2
# ---------------------------------------------------------------------------


def test_path_resolved_by_deletion_skips_the_marker_check(tmp_path):
    repos = make_repos(tmp_path, {"d.txt": "keep\n", "README.md": "r\n"})
    repos.advance_base({"d.txt": None})
    repos.pr_commit({"d.txt": "modified\n"})
    setup = start_merge(repos)
    repos.git(repos.work, "rm", "-q", "--", "d.txt")
    res = finish_commit(repos, setup, ["d.txt"])
    assert res.returncode == 0, res.stderr
    assert res.payload["parents"] == [setup.old_head, setup.base_sha]
    assert repos.git(repos.work, "ls-files", "--", "d.txt") == ""


@pytest.mark.parametrize(
    "extra",
    [
        ("--precheck", "--manifest", "m.txt"),
        ("--precheck", "--merge-tree-oid", "a" * 40),
        ("--precheck", "--message-file", "msg.txt"),
        ("--merge-tree-oid", "a" * 40, "--manifest", "m.txt"),
        ("--precheck", "--bogus"),
        ("--precheck", "--base-sha", "abc"),
    ],
    ids=[
        "precheck-manifest",
        "precheck-tree",
        "precheck-message",
        "commit-missing-message",
        "unknown",
        "short-sha",
    ],
)
def test_usage_errors(tmp_path, extra):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    (repos.work / "m.txt").write_text("-\tf.txt\n", encoding="utf-8")
    (repos.work / "msg.txt").write_text("msg\n", encoding="utf-8")
    res = run_finish(repos, "--base-sha", setup.base_sha, *extra)
    assert_fail(res, "usage")
    assert_no_commit(repos, setup)


@pytest.mark.parametrize(
    "manifest",
    ["no tab here\n", "short\tf.txt\n", "-\t\n", "-\tf.txt\n-\tf.txt\n"],
    ids=["no-tab", "bad-oid", "empty-path", "duplicate"],
)
def test_malformed_manifest_is_usage(tmp_path, manifest):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    setup = start_merge(repos)
    resolve(repos, {"f.txt": RESOLVED_F})
    (repos.root / "bad-manifest.txt").write_text(manifest, encoding="utf-8")
    (repos.root / "msg.txt").write_text(MESSAGE, encoding="utf-8")
    res = run_finish(
        repos,
        "--base-sha",
        setup.base_sha,
        "--merge-tree-oid",
        setup.merge_tree_oid,
        "--manifest",
        str(repos.root / "bad-manifest.txt"),
        "--message-file",
        str(repos.root / "msg.txt"),
    )
    assert_fail(res, "usage")
    assert_no_commit(repos, setup)


def test_finish_script_static_rules():
    text = FINISH.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env bash\n")
    assert "\nset -u -o pipefail\n" in text
    assert os.access(FINISH, os.X_OK)
    # The only commit is one `git commit -F`, with hooks on.
    assert len(re.findall(r"\bgit\s+commit\b", text)) == 1
    assert len(re.findall(r"\bgit commit -F \"\$MESSAGE_FILE\"", text)) == 1
    for pattern in (
        r"\bgit\s+push\b",
        r"(?i)stash",
        r"(?i)force",
        r"\bgit\s+config\b",
        r"--no-verify\b",
        r"--amend\b",
        r"\bcommit\s+(-a|--all|--only)\b",
        r"src/superclaude",
        r"\bgit\s+(checkout|switch|reset|add|worktree|rebase|merge)\b",
        r"\bgh\b",
    ):
        assert re.search(pattern, text) is None, pattern
    ls = subprocess.run(
        [GIT, "ls-files", "-s", "--", FINISH_REL],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    ).stdout
    if ls:  # the index entry exists once the path is staged
        assert ls.startswith("100755 "), ls


# ---------------------------------------------------------------------------
# collect-conflict-evidence.sh helpers (design section 7.3)
# ---------------------------------------------------------------------------

EVIDENCE = SKILL_DIR / "scripts" / "collect-conflict-evidence.sh"
EVIDENCE_REL = (
    "src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh"
)
ALL_EVIDENCE_FILES = [
    "stage1",
    "stage2",
    "stage3",
    "worktree",
    "log.txt",
    "diff-ours.txt",
    "diff-theirs.txt",
]


@dataclass
class EvidenceMerge:
    base_sha: str
    merge_base: str
    old_head: str


def start_zdiff3_merge(repos: Repos) -> EvidenceMerge:
    """Fetch the base tip and start a real merge with the zdiff3 conflict style for
    this one invocation (as the Tier 2 flow does), leaving the conflicts in place."""
    repos.git(repos.work, "fetch", "-q", "origin", "main")
    base_sha = repos.git(repos.work, "rev-parse", "origin/main").strip()
    merge_base = repos.git(repos.work, "merge-base", "HEAD", base_sha).strip()
    old_head = _head(repos)
    repos.git(
        repos.work,
        "-c",
        "merge.conflictStyle=zdiff3",
        "merge",
        "-q",
        "--no-commit",
        "--no-ff",
        base_sha,
        check=False,
    )
    assert _merge_head(repos).exists(), "the setup merge did not start"
    return EvidenceMerge(base_sha=base_sha, merge_base=merge_base, old_head=old_head)


def run_evidence(
    repos: Repos,
    path: str,
    out: Path,
    merge: EvidenceMerge,
    *extra: str,
    base_sha: str | None = None,
) -> ProbeRun:
    """Run the collector from its source path; assert it left the repository as-is."""
    before = _snapshot(repos)
    merge_head_before = (
        _merge_head(repos).read_bytes() if _merge_head(repos).exists() else None
    )
    res = subprocess.run(
        [
            str(EVIDENCE),
            "--path",
            path,
            "--out",
            str(out),
            "--base-sha",
            base_sha or merge.base_sha,
            "--merge-base",
            merge.merge_base,
            *extra,
        ],
        cwd=repos.work,
        env=repos.env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert _snapshot(repos) == before, "the collector changed status, HEAD or the index"
    merge_head_after = (
        _merge_head(repos).read_bytes() if _merge_head(repos).exists() else None
    )
    assert merge_head_after == merge_head_before
    assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
    assert repos.gh_call_lines() == [], "the collector must not call gh"
    assert len(res.stdout.splitlines()) == 1, res.stdout
    return ProbeRun(res.returncode, res.stdout, res.stderr)


def assert_evidence_fail(res: ProbeRun, reason: str) -> None:
    assert res.returncode == 2, (res.stdout, res.stderr)
    assert res.stdout == f"EVIDENCE_FAIL {reason}\n", res.stderr


def _listing(directory: Path) -> list[str]:
    return sorted(p.name for p in directory.iterdir())


# ---------------------------------------------------------------------------
# E1 to E4
# ---------------------------------------------------------------------------


def test_e1_content_conflict_writes_exactly_the_seven_files(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    out = tmp_path / "evidence" / "sync" / "sync-1" / "1"
    res = run_evidence(repos, "f.txt", out, merge)
    assert res.returncode == 0, res.stderr
    assert res.payload == {
        "dir": str(out),
        "files": ALL_EVIDENCE_FILES,
        "missing": [],
        "truncated": False,
    }
    assert _listing(out) == sorted(ALL_EVIDENCE_FILES)
    read = {
        name: (out / name).read_text(encoding="utf-8") for name in ALL_EVIDENCE_FILES
    }
    assert read["stage1"] == "line1\nline2\nline3\n"
    assert read["stage2"] == "line1\nOURS\nline3\n"
    assert read["stage3"] == "line1\nTHEIRS\nline3\n"
    # zdiff3: the work-tree file shows all three sides.
    for marker in ("<<<<<<< ", "||||||| ", "=======\n", ">>>>>>> "):
        assert marker in read["worktree"], marker
    assert "OURS" in read["worktree"] and "THEIRS" in read["worktree"]
    assert "line2" in read["worktree"]
    log_lines = read["log.txt"].splitlines()
    assert any(line.startswith("< ") and "pr change" in line for line in log_lines)
    assert any(line.startswith("> ") and "base advance" in line for line in log_lines)
    assert "-line2\n+OURS\n" in read["diff-ours.txt"]
    assert "-line2\n+THEIRS\n" in read["diff-theirs.txt"]
    for name in ALL_EVIDENCE_FILES:
        assert "[sc:pr-submit: truncated" not in read[name], name


def test_e2_modify_delete_lists_the_missing_stage(tmp_path):
    repos = make_repos(tmp_path, {"d.txt": "keep\n", "README.md": "r\n"})
    repos.advance_base({"d.txt": None})
    repos.pr_commit({"d.txt": "modified\n"})
    merge = start_zdiff3_merge(repos)
    out = tmp_path / "evidence-e2"
    res = run_evidence(repos, "d.txt", out, merge)
    assert res.returncode == 0, res.stderr
    payload = res.payload
    assert payload["missing"] == ["stage3"]
    expected = [name for name in ALL_EVIDENCE_FILES if name != "stage3"]
    assert payload["files"] == expected
    assert payload["truncated"] is False
    assert _listing(out) == sorted(expected)
    assert (out / "stage1").read_text(encoding="utf-8") == "keep\n"
    assert (out / "stage2").read_text(encoding="utf-8") == "modified\n"
    assert (out / "worktree").read_text(encoding="utf-8") == "modified\n"
    assert "-keep\n" in (out / "diff-theirs.txt").read_text(encoding="utf-8")
    assert "+modified\n" in (out / "diff-ours.txt").read_text(encoding="utf-8")


def test_e3_max_bytes_cuts_each_file_with_the_marker_line(tmp_path):
    base = "".join(f"base line {i:03d} of the shared file\n" for i in range(10))
    ours = base.replace("base line 005", "OURS line 005")
    theirs = base.replace("base line 005", "THEIRS line 005")
    repos = make_repos(tmp_path, {"README.md": "r\n", "f.txt": base})
    repos.advance_base({"f.txt": theirs})
    repos.pr_commit({"f.txt": ours})
    merge = start_zdiff3_merge(repos)
    out = tmp_path / "evidence-e3"
    res = run_evidence(repos, "f.txt", out, merge, "--max-bytes", "64")
    assert res.returncode == 0, res.stderr
    payload = res.payload
    assert payload["truncated"] is True
    assert payload["files"] == ALL_EVIDENCE_FILES
    marker = "[sc:pr-submit: truncated at 64 bytes]\n"
    originals = {"stage1": base, "stage2": ours, "stage3": theirs}
    for name, original in originals.items():
        data = (out / name).read_bytes()
        assert data.endswith(marker.encode()), name
        cut = original.encode()[:64]
        assert data.startswith(cut), name
        assert data[len(cut) :] in (marker.encode(), b"\n" + marker.encode()), name
    for name in ("worktree", "diff-ours.txt", "diff-theirs.txt"):
        text = (out / name).read_text(encoding="utf-8")
        assert text.splitlines()[-1] == marker.rstrip("\n"), name
    # A file at or under the limit is copied unchanged, without the marker.
    small = run_evidence(
        repos, "f.txt", tmp_path / "evidence-e3-big", merge, "--max-bytes", "100000"
    ).payload
    assert small["truncated"] is False
    assert (tmp_path / "evidence-e3-big" / "stage1").read_text(encoding="utf-8") == base


@pytest.mark.parametrize("kind", ["non-empty-dir", "regular-file"])
def test_e4_non_empty_out_is_out_not_empty_and_writes_nothing(tmp_path, kind):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    out = tmp_path / "evidence-e4"
    if kind == "non-empty-dir":
        out.mkdir()
        (out / "keep.txt").write_text("operator file\n", encoding="utf-8")
    else:
        out.write_text("a file, not a directory\n", encoding="utf-8")
    parent_before = _listing(tmp_path)
    res = run_evidence(repos, "f.txt", out, merge)
    assert_evidence_fail(res, "out_not_empty")
    assert _listing(tmp_path) == parent_before
    if kind == "non-empty-dir":
        assert _listing(out) == ["keep.txt"]
        assert (out / "keep.txt").read_text(encoding="utf-8") == "operator file\n"
    else:
        assert out.read_text(encoding="utf-8") == "a file, not a directory\n"


# ---------------------------------------------------------------------------
# Further contract rows of section 7.3
# ---------------------------------------------------------------------------


def test_existing_empty_out_directory_is_accepted(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    out = tmp_path / "empty-out"
    out.mkdir()
    res = run_evidence(repos, "f.txt", out, merge)
    assert res.returncode == 0, res.stderr
    assert _listing(out) == sorted(ALL_EVIDENCE_FILES)


def test_foreign_merge_and_no_merge_head(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    repos.git(repos.work, "fetch", "-q", "origin", "main")
    base_sha = repos.git(repos.work, "rev-parse", "origin/main").strip()
    merge = EvidenceMerge(
        base_sha=base_sha,
        merge_base=repos.git(repos.work, "merge-base", "HEAD", base_sha).strip(),
        old_head=_head(repos),
    )
    out = tmp_path / "evidence-foreign"
    # No merge in progress.
    assert_evidence_fail(run_evidence(repos, "f.txt", out, merge), "foreign_merge")
    assert not out.exists()
    # A merge of the base tip, checked against another commit.
    start_zdiff3_merge(repos)
    res = run_evidence(repos, "f.txt", out, merge, base_sha=merge.old_head)
    assert_evidence_fail(res, "foreign_merge")
    assert not out.exists()
    # The recorded base tip is compared case-insensitively.
    ok = run_evidence(repos, "f.txt", out, merge, base_sha=base_sha.upper())
    assert ok.returncode == 0, ok.stderr


@pytest.mark.parametrize(
    "path, extra",
    [
        ("/etc/passwd", ()),
        ("../f.txt", ()),
        ("./f.txt", ()),
        ("f.txt", ("--max-bytes", "0")),
        ("f.txt", ("--max-bytes", "12k")),
        ("f.txt", ("--bogus",)),
    ],
    ids=["absolute", "dotdot", "dot", "zero-bytes", "bad-bytes", "unknown"],
)
def test_evidence_usage_errors(tmp_path, path, extra):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    out = tmp_path / "evidence-usage"
    res = run_evidence(repos, path, out, merge, *extra)
    assert_evidence_fail(res, "usage")
    assert not out.exists()


def test_missing_work_tree_file_is_unreadable(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    (repos.work / "f.txt").unlink()
    res = run_evidence(repos, "f.txt", tmp_path / "evidence-unreadable", merge)
    assert_evidence_fail(res, "unreadable")


def test_a_command_hitting_the_time_bound_is_timeout(tmp_path):
    """A `timeout` stub reports exit 124 for the log read, as the real `timeout`
    does when the 60-second budget runs out; the collector maps it to `timeout`."""
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    real_timeout = shutil.which("timeout")
    if real_timeout is None:
        pytest.skip("timeout is not on PATH")
    stub = repos.bin_dir / "timeout"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        'for a in "$@"; do [ "$a" = log ] && exit 124; done\n'
        f'exec "{real_timeout}" "$@"\n',
        encoding="utf-8",
    )
    stub.chmod(0o755)
    res = run_evidence(repos, "f.txt", tmp_path / "evidence-timeout", merge)
    assert_evidence_fail(res, "timeout")
    assert "60-second budget" in res.stderr


_NO_TIMEOUT_TOOLS = (
    "bash", "jq", "tr", "cut", "wc", "head", "tail", "ls", "mkdir", "rmdir", "cat",
    "rm", "printf", "sed", "grep", "mktemp", "env", "dirname", "basename", "sleep",
)  # fmt: skip


def _run_evidence_without_timeout(
    repos: Repos, merge: EvidenceMerge, out: Path, *, hang_on_show: bool
) -> tuple[ProbeRun, float]:
    """Run the collector with a PATH that has no `timeout`; git is a wrapper that,
    when asked, replaces itself with a 90-second sleep on `show`."""
    import time

    bin_dir = repos.root / "bin-no-timeout"
    bin_dir.mkdir()
    for tool in _NO_TIMEOUT_TOOLS:
        found = shutil.which(tool)
        if found is None:
            pytest.skip(f"{tool} is not on PATH")
        (bin_dir / tool).symlink_to(found)
    hang = 'for a in "$@"; do [ "$a" = show ] && exec sleep 90; done\n'
    wrapper = bin_dir / "git"
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        + (hang if hang_on_show else "")
        + f'exec "{GIT}" "$@"\n',
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    env = dict(repos.env, PATH=str(bin_dir))
    started = time.monotonic()
    res = subprocess.run(
        [
            str(EVIDENCE),
            "--path",
            "f.txt",
            "--out",
            str(out),
            "--base-sha",
            merge.base_sha,
            "--merge-base",
            merge.merge_base,
        ],
        cwd=repos.work,
        env=env,
        text=True,
        capture_output=True,
        timeout=150,
    )
    elapsed = time.monotonic() - started
    assert not (repos.work / ".git" / "sc-pr-submit-tmp").exists()
    assert len(res.stdout.splitlines()) == 1, res.stdout
    return ProbeRun(res.returncode, res.stdout, res.stderr), elapsed


@pytest.mark.slow
def test_without_timeout_a_hung_read_is_stopped_at_the_budget(tmp_path):
    """No `timeout` on PATH: a git read that would hang for 90 seconds is stopped at
    the 60-second budget and reported as `timeout` (PR #378 review finding)."""
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    res, elapsed = _run_evidence_without_timeout(
        repos, merge, tmp_path / "evidence-hang", hang_on_show=True
    )
    assert_evidence_fail(res, "timeout")
    assert "60-second budget" in res.stderr
    assert elapsed < 75, f"the run took {elapsed:.1f}s; the budget is 60s"


def test_without_timeout_a_normal_run_still_succeeds(tmp_path):
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    out = tmp_path / "evidence-no-timeout"
    res, elapsed = _run_evidence_without_timeout(repos, merge, out, hang_on_show=False)
    assert res.returncode == 0, res.stderr
    assert res.payload["files"] == ALL_EVIDENCE_FILES
    assert elapsed < 30, f"the run took {elapsed:.1f}s"


def test_restart_attempt_collects_into_a_fresh_attempt_directory(tmp_path):
    """Illustrates the attempt-directory convention at the script level (the script
    itself did not change for this finding; the guards are conflict_attempt, the
    protocol pin and the e2e restart test): a resume restart keeps its cycle id, so
    attempt 1's evidence is still in `sync/<cycle_id>/a1/`; attempt 2 collects into
    `sync/<cycle_id>/a2/` and succeeds (refs/conflict-mechanical.md step 3)."""
    repos = make_repos(tmp_path)
    _content_conflict(repos)
    merge = start_zdiff3_merge(repos)
    cycle = tmp_path / "out" / "sync" / "sync-1"
    first = run_evidence(repos, "f.txt", cycle / "a1" / "1", merge)
    assert first.returncode == 0, first.stderr
    kept = {
        name: (cycle / "a1" / "1" / name).read_bytes() for name in ALL_EVIDENCE_FILES
    }
    again = run_evidence(repos, "f.txt", cycle / "a1" / "1", merge)
    assert_evidence_fail(again, "out_not_empty")
    second = run_evidence(repos, "f.txt", cycle / "a2" / "1", merge)
    assert second.returncode == 0, second.stderr
    assert _listing(cycle / "a2" / "1") == sorted(ALL_EVIDENCE_FILES)
    assert {
        name: (cycle / "a1" / "1" / name).read_bytes() for name in ALL_EVIDENCE_FILES
    } == kept


def test_evidence_script_static_rules():
    text = EVIDENCE.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env bash\n")
    assert "\nset -u -o pipefail\n" in text
    assert os.access(EVIDENCE, os.X_OK)
    for pattern in (
        r"(?i)\bpush\b",
        r"(?i)stash",
        r"(?i)force",
        r"\bgit\s+config\b",
        r"--no-verify\b",
        r"--amend\b",
        r"src/superclaude",
        r"\bgit\s+(checkout|switch|reset|commit|add|rm|worktree|rebase|merge)\b",
        r"\bgh\b",
    ):
        assert re.search(pattern, text) is None, pattern
    ls = subprocess.run(
        [GIT, "ls-files", "-s", "--", EVIDENCE_REL],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    ).stdout
    if ls:  # the index entry exists once the path is staged
        assert ls.startswith("100755 "), ls


# ---------------------------------------------------------------------------
# poll-ci-checks.sh --evidence-sha (cases C1 to C4)
# ---------------------------------------------------------------------------

POLL_CI = SKILL_DIR / "scripts" / "poll-ci-checks.sh"
EVIDENCE_SHA = "0123456789abcdef0123456789abcdef01234567"
EVIDENCE_REPO = "IronbellyOrg/IronClaude"
EVIDENCE_CALLS = [
    f"api repos/{EVIDENCE_REPO}/commits/{EVIDENCE_SHA}/check-runs?per_page=1"
    " --jq .total_count",
    f"api repos/{EVIDENCE_REPO}/commits/{EVIDENCE_SHA}/status --jq .total_count",
]


def install_ci_gh_stub(repos: Repos) -> None:
    """Replace the recording `gh` stub with one that also serves the two counts.

    ``GH_STUB_RUNS`` and ``GH_STUB_STATUSES`` hold what each read prints (the value
    `--jq .total_count` would yield); ``FAIL`` makes that read exit 1 with no stdout.
    Any other call is unexpected and fails."""
    stub = repos.bin_dir / "gh"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        f"printf '%s\\n' \"$*\" >> '{repos.gh_calls}'\n"
        'case "$1 $2" in\n'
        '  "api repos/"*"/check-runs?per_page=1") out="$GH_STUB_RUNS" ;;\n'
        '  "api repos/"*"/status") out="$GH_STUB_STATUSES" ;;\n'
        "  *) printf 'unexpected gh call: %s\\n' \"$*\" >&2; exit 1 ;;\n"
        "esac\n"
        "if [ \"$out\" = FAIL ]; then printf 'HTTP 502\\n' >&2; exit 1; fi\n"
        "printf '%s\\n' \"$out\"\n",
        encoding="utf-8",
    )
    stub.chmod(0o755)


def run_evidence_poll(
    repos: Repos, *args: str, runs: str = "0", statuses: str = "0"
) -> ProbeRun:
    """Run poll-ci-checks.sh from its source path with `--evidence-sha` and `--repo`
    only (never `--pr`); assert evidence mode made no `gh pr checks` call."""
    install_ci_gh_stub(repos)
    env = {**repos.env, "GH_STUB_RUNS": runs, "GH_STUB_STATUSES": statuses}
    res = subprocess.run(
        [str(POLL_CI), *args],
        cwd=repos.work,
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert "--pr" not in args
    for line in repos.gh_call_lines():
        assert not line.startswith("pr "), f"evidence mode called gh pr: {line}"
        assert "pr checks" not in line, line
    return ProbeRun(res.returncode, res.stdout, res.stderr)


def _evidence(repos: Repos, runs: str, statuses: str) -> ProbeRun:
    return run_evidence_poll(
        repos,
        "--evidence-sha",
        EVIDENCE_SHA,
        "--repo",
        EVIDENCE_REPO,
        runs=runs,
        statuses=statuses,
    )


def test_c1_two_check_runs_and_no_statuses_is_two(tmp_path):
    repos = make_repos(tmp_path)
    res = _evidence(repos, runs="2", statuses="0")
    assert res.payload == {
        "evidence_sha": EVIDENCE_SHA,
        "evidence_checks": 2,
        "source": "ci",
    }
    assert repos.gh_call_lines() == EVIDENCE_CALLS


def test_c1_statuses_are_added_to_check_runs(tmp_path):
    repos = make_repos(tmp_path)
    res = _evidence(repos, runs="1", statuses="3")
    assert res.payload["evidence_checks"] == 4


def test_c2_no_check_runs_and_no_statuses_is_zero(tmp_path):
    repos = make_repos(tmp_path)
    res = _evidence(repos, runs="0", statuses="0")
    assert res.payload == {
        "evidence_sha": EVIDENCE_SHA,
        "evidence_checks": 0,
        "source": "ci",
    }
    assert repos.gh_call_lines() == EVIDENCE_CALLS


@pytest.mark.parametrize(
    ("runs", "statuses"),
    [
        ("FAIL", "0"),  # failing check-runs read
        ("2", "FAIL"),  # failing status read
        ("FAIL", "FAIL"),
        ("null", "0"),  # unparsable: not a non-negative integer
        ("2", "-1"),
        ("", "0"),
    ],
)
def test_c3_failed_or_unparsable_read_is_minus_one(tmp_path, runs, statuses):
    repos = make_repos(tmp_path)
    res = _evidence(repos, runs=runs, statuses=statuses)
    assert res.payload == {
        "evidence_sha": EVIDENCE_SHA,
        "evidence_checks": -1,
        "source": "ci",
    }
    assert repos.gh_call_lines() == EVIDENCE_CALLS


@pytest.mark.parametrize(
    "args",
    [
        ("--evidence-sha", "abc123"),
        ("--evidence-sha", EVIDENCE_SHA + "0"),  # 41 characters
        ("--evidence-sha", EVIDENCE_SHA[:-1] + "g"),  # 40 characters, not hex
        ("--evidence-sha", ""),
        ("--evidence-sha",),  # flag given without a value
    ],
)
def test_c4_invalid_sha_exits_2_naming_it(tmp_path, args):
    repos = make_repos(tmp_path)
    res = run_evidence_poll(repos, "--repo", EVIDENCE_REPO, *args)
    assert res.returncode == 2, res.stderr
    assert res.stdout == ""
    bad = args[1] if len(args) > 1 else ""
    assert "invalid --evidence-sha" in res.stderr
    assert f"'{bad}'" in res.stderr
    # Rejected before any gh call: no capability probe, no api read.
    assert repos.gh_call_lines() == []


def test_poll_ci_evidence_mode_static_rules():
    text = POLL_CI.read_text(encoding="utf-8")
    assert re.search(r"(?i)force", text) is None
    for line in text.splitlines():
        if re.search(r"\bgh\s+api\b", line):
            assert "repos/${REPO}/" in line, line
    # The evidence branch exits before the `pr checks` capability probe.
    assert text.index('if [ "$EVIDENCE_MODE" -eq 1 ]; then') < text.index(
        "gh pr checks --repo"
    )
