"""The .dev archive step (Task 9; Task 10 adds the remaining cases).

Everything runs in throwaway repositories under ``tmp_path`` with local bare remotes. No
test pushes to a network remote or reads a credential file. Token-shaped test strings are
built at run time from two pieces, so no secret-looking literal is committed.
"""

from __future__ import annotations

import dataclasses
import hashlib
import os
from pathlib import Path

import pytest

from .conftest import git_in
from .test_facts import facts_for, write

AUTHOR = "example-user"
MERGED = "2026-11-10T12:00:00Z"
BASE = "IronClaude/example-user/2026-11-10_pr700_topic"
UNSET = object()


@pytest.fixture(autouse=True)
def git_identity(monkeypatch):
    """The evidence commit needs an identity; the throwaway one never leaves the tests."""
    for key, value in {
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.invalid",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
    }.items():
        monkeypatch.setenv(key, value)


def make_pr(wc, **change):
    base = dict(
        number=700, state="MERGED", head_oid="b" * 40, author=AUTHOR, merged_at=MERGED,
        title="Example title", body="", closing=(), branch=f"{AUTHOR}/topic",
    )  # fmt: skip
    base.update(change)
    return wc.PullRequest(**base)


class Case:
    """A throwaway worktree with .dev files, an evidence bare repo and a clone path."""

    def __init__(self, wc, runner_cls, repo, evidence_bare, tmp_path, replies=None):
        self.wc, self.bare = wc, evidence_bare
        self.clone = str(tmp_path / "evidence-clone")
        self.runner = runner_cls(evidence_dir=self.clone, replies=replies)
        self.path = repo.add_worktree("topic")
        write(self.path / ".dev" / "tasks" / "a b.md", "report\n")
        write(self.path / ".dev" / "local" / "run.log", "log line\n")
        write(self.path / ".dev" / "local" / "__pycache__" / "x.pyc", "skipped\n")
        self.repo, self.runner_cls = repo, runner_cls
        self.notes: list[str] = []

    def facts(self):
        _, facts = facts_for(self.wc, self.runner_cls, self.repo, self.path)
        return dataclasses.replace(
            facts, origin=self.wc.OriginInfo("IronbellyOrg", "IronClaude")
        )

    def run(self, pr=UNSET, facts=None):
        return self.wc.archive_worktree(
            self.runner, facts or self.facts(), make_pr(self.wc) if pr is UNSET else pr,
            self.clone, str(self.bare), log=self.notes.append,
        )  # fmt: skip

    def snapshot(self):
        """Every file of the worktree with its hash: unchanged means the step touched nothing."""
        seen = {}
        for dirpath, _dirs, names in os.walk(self.path):
            if ".git" in Path(dirpath).parts:
                continue
            for name in names:
                full = os.path.join(dirpath, name)
                seen[os.path.relpath(full, self.path)] = hashlib.sha256(
                    Path(full).read_bytes()
                ).hexdigest()
        return seen

    def remote_files(self, folder):
        out = git_in(self.bare, "ls-tree", "-r", "--name-only", "main", folder)
        return [n for n in out.splitlines() if n]


@pytest.fixture
def case(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return Case(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)


def tree_digest(folder: Path):
    return {
        str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    }


# -- the saved folder ---------------------------------------------------------------------------


def test_the_folder_appears_with_every_part_and_is_verified(case):
    before = case.snapshot()
    result = case.run()
    assert result.ok, result.reason
    assert result.folder == BASE
    folder = Path(case.clone) / BASE
    assert {p.name for p in folder.iterdir()} == {
        "MANIFEST.md",
        "files",
        "ignored.tar.gz",
        "saved-paths.txt",
    }
    assert (folder / "files" / ".dev" / "tasks" / "a b.md").read_text() == "report\n"
    saved = (folder / "saved-paths.txt").read_text().splitlines()
    assert saved == [
        ".dev/local/run.log",
        ".dev/tasks/a b.md",
    ]  # the pycache file is not saved
    assert result.saved_paths == frozenset(saved)
    n = sum(1 for p in folder.rglob("*") if p.is_file())
    assert result.verified == f"VERIFIED {BASE} files={n}" and result.files == n
    assert len(case.remote_files(BASE)) == n  # the same files are on origin/main
    assert case.snapshot() == before  # the worktree is untouched
    manifest = (folder / "MANIFEST.md").read_text()
    for field in (
        "source repo: IronbellyOrg/IronClaude", "branch: topic",
        "[#700 Example title](https://github.com/IronbellyOrg/IronClaude/pull/700)",
        "merge date: 2026-11-10", f"worktree head: {case.facts().head}", f"pull request head: {'b' * 40}",
        f"worktree folder: {case.path}", "saved at (UTC): ", "files saved: 2",
        "ignored.tar.gz", "saved-paths.txt",
    ):  # fmt: skip
        assert field in manifest, field
    for name in ("ignored.tar.gz", "saved-paths.txt"):
        digest = hashlib.sha256((folder / name).read_bytes()).hexdigest()
        assert f"| {name} | {digest} |" in manifest


def test_the_commit_message_follows_the_convention(case):
    assert case.run().ok
    subject = git_in(case.bare, "log", "-1", "--format=%s", "main").strip()
    assert subject == "archive(IronClaude): 2026-11-10 pr700 topic"


def test_the_step_refuses_without_a_merged_pull_request_and_with_nothing_to_save(
    wc, case
):
    for pr in (None, make_pr(wc, state="OPEN"), make_pr(wc, state="CLOSED")):
        result = case.run(pr=pr)
        assert (
            not result.ok
            and result.reason == "saved copy failed: no merged pull request"
        )
    assert not Path(case.clone).exists()
    empty = dataclasses.replace(case.facts(), state=wc.LocalState())
    result = case.run(facts=empty)
    assert result.ok and result.verified == "nothing to save" and result.folder == ""


def test_a_pull_request_without_an_author_or_merge_date_is_refused(wc, case):
    for change in ({"author": ""}, {"merged_at": None}, {"merged_at": "yesterday"}):
        result = case.run(pr=make_pr(wc, **change))
        assert result.reason.startswith(
            "saved copy failed: the pull request has no author"
        )


def test_the_branch_prefix_is_dropped_only_when_it_is_the_author(wc):
    pr = make_pr(wc, branch="example-user/docs-354-x/y")
    assert (
        wc.folder_name(pr, "IronbellyOrg/IronClaude")[0]
        == "IronClaude/example-user/2026-11-10_pr700_docs-354-x-y"
    )
    pr = make_pr(wc, branch="someone-else/docs-354")
    assert wc.folder_name(pr, "IronbellyOrg/IronClaude")[1] == "someone-else-docs-354"


# -- failures: each starts with "saved copy failed" and leaves the worktree alone --------------------


def _result(wc, code, out="", err=""):
    return wc.Result(code, out, err)


def test_a_push_refused_three_times_fails_with_push_refused(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    pushes = []

    def handler(argv, cwd):
        if "push" in argv:
            pushes.append(argv)
            return _result(wc, 1, "", "! [rejected] main -> main (fetch first)")
        return None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    before = c.snapshot()
    result = c.run()
    assert not result.ok and result.reason == "saved copy failed: push refused"
    assert len(pushes) == 3
    assert pushes[0][:4] == ["git", "-c", wc.CREDENTIAL_HELPER, "push"]
    assert c.snapshot() == before
    assert c.remote_files(BASE) == []  # nothing reached the remote


def test_a_push_that_fails_to_authenticate_names_the_credentials(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    def handler(argv, cwd):
        if "push" in argv:
            return _result(
                wc,
                128,
                "",
                "fatal: could not read Username for 'https://x.invalid': terminal prompts disabled",
            )
        return None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    result = c.run()
    assert result.reason == "saved copy failed: no credentials in the environment"


def test_a_refused_push_that_succeeds_on_the_second_try_after_a_rebase(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    seen = {"n": 0}

    def handler(argv, cwd):
        if "push" in argv:
            seen["n"] += 1
            if seen["n"] == 1:
                return _result(wc, 1, "", "! [rejected]")
        return None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    result = c.run()
    assert result.ok and seen["n"] == 2
    assert len(c.remote_files(BASE)) == result.files


@pytest.mark.parametrize(
    "verb,answer,reason",
    [
        ("diff", (1, "", ""), "saved copy failed: the copy differs from origin/main"),
        (
            "ls-tree",
            (0, "one\0", ""),
            "saved copy failed: the copy on origin/main has a different file count",
        ),
    ],
)
def test_a_folder_that_differs_after_the_push_fails(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, verb, answer, reason
):
    def handler(argv, cwd):
        return _result(wc, *answer) if verb in argv else None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    before = c.snapshot()
    result = c.run()
    assert not result.ok and result.reason == reason
    assert c.snapshot() == before


def test_a_failed_copy_leaves_a_named_scratch_folder_and_the_worktree_untouched(
    wc, case, monkeypatch
):
    def broken(src, dst, **kw):
        raise OSError("disk full")

    monkeypatch.setattr(wc.shutil, "copy2", broken)
    before = case.snapshot()
    result = case.run()
    assert result.reason == "saved copy failed: copy failed (OSError)"
    assert result.scratch and Path(result.scratch).is_dir()
    assert result.scratch in " ".join(case.notes)  # the log names it
    assert not (Path(case.clone) / BASE).exists()
    assert case.snapshot() == before


def test_the_evidence_clone_that_cannot_be_made_is_a_failure(
    wc, runner_cls, throwaway_repo, tmp_path
):
    c = Case(wc, runner_cls, throwaway_repo, tmp_path / "no-such-repo.git", tmp_path)
    result = c.run()
    assert result.reason == "saved copy failed: the evidence repo could not be cloned"


# -- split archives, repeats and -r2 ----------------------------------------------------------------


def test_a_large_ignored_archive_is_split_into_parts_that_join_back(
    wc, case, monkeypatch
):
    monkeypatch.setattr(wc, "ARCHIVE_PART_BYTES", 2048)
    blob = os.urandom(
        10_000
    )  # does not compress, so the archive is larger than one part
    (case.path / ".dev" / "local" / "big.bin").write_bytes(blob)
    result = case.run()
    assert result.ok, result.reason
    folder = Path(case.clone) / result.folder
    parts = sorted(p for p in folder.iterdir() if ".part-" in p.name)
    assert len(parts) >= 5 and not (folder / "ignored.tar.gz").exists()
    assert all(p.stat().st_size <= 2048 for p in parts)
    joined = b"".join(p.read_bytes() for p in parts)
    import io
    import tarfile

    with tarfile.open(fileobj=io.BytesIO(joined), mode="r:gz") as tar:
        assert tar.extractfile(".dev/local/big.bin").read() == blob
    assert set(wc.archive_parts(str(folder))) == {str(p) for p in parts}
    manifest = (folder / "MANIFEST.md").read_text()
    assert all(
        f"| {p.name} | {hashlib.sha256(p.read_bytes()).hexdigest()} |" in manifest
        for p in parts
    )
    assert ".dev/local/big.bin" in (folder / "saved-paths.txt").read_text()


def test_a_repeat_run_verifies_and_a_run_with_new_files_writes_r2(wc, case):
    first = case.run()
    assert first.ok and first.folder == BASE
    before = tree_digest(Path(case.clone) / BASE)
    commits = git_in(case.bare, "rev-list", "--count", "main").strip()
    again = case.run()
    assert again.ok and again.folder == BASE and again.verified == first.verified
    assert (
        git_in(case.bare, "rev-list", "--count", "main").strip() == commits
    )  # nothing new pushed
    write(case.path / ".dev" / "tasks" / "later.md", "new\n")
    second = case.run()
    assert second.ok and second.folder == f"{BASE}-r2"
    assert (
        tree_digest(Path(case.clone) / BASE) == before
    )  # the first folder is byte-identical
    saved = (
        (Path(case.clone) / second.folder / "saved-paths.txt").read_text().splitlines()
    )
    assert saved == [".dev/tasks/later.md"]
    assert second.saved_paths == frozenset(
        {".dev/local/run.log", ".dev/tasks/a b.md", ".dev/tasks/later.md"}
    )
    assert (
        git_in(case.bare, "log", "-1", "--format=%s", "main")
        .strip()
        .endswith("topic-r2")
    )
    third = case.run()
    assert (
        third.ok and third.folder == f"{BASE}-r2"
    )  # covered by the two folders together


def test_a_file_changed_since_the_save_is_saved_again_not_assumed_covered(wc, case):
    assert case.run().ok
    write(case.path / ".dev" / "tasks" / "a b.md", "edited after the save\n")
    result = case.run()
    assert result.ok and result.folder == f"{BASE}-r2"
    assert (
        Path(case.clone) / result.folder / "files" / ".dev" / "tasks" / "a b.md"
    ).read_text() == "edited after the save\n"
    assert (
        Path(case.clone) / BASE / "files" / ".dev" / "tasks" / "a b.md"
    ).read_text() == "report\n"


def test_an_existing_folder_is_never_overwritten_and_three_is_the_limit(wc, case):
    assert case.run().ok
    for name in ("two", "three", "four"):
        write(case.path / ".dev" / "tasks" / f"{name}.md", name)
        result = case.run()
        if name == "four":
            assert (
                result.reason
                == "saved copy failed: this pull request already has three saved folders"
            )
        else:
            assert result.ok
    assert sorted(p.name for p in (Path(case.clone) / "IronClaude" / AUTHOR).iterdir() if not p.name.startswith(".")) == [
        "2026-11-10_pr700_topic", "2026-11-10_pr700_topic-r2", "2026-11-10_pr700_topic-r3",
    ]  # fmt: skip


# -- the names-only secret check -----------------------------------------------------------------------


def token_like(prefix="gh" + "p_"):
    return (
        prefix + "A1b2C3d4" * 4
    )  # assembled at run time; no literal token is committed


def assert_value_in_no_clone_file(secret: str, clone: str) -> int:
    """Read every file of the evidence clone, the git folder included; return how many."""
    seen = 0
    for p in Path(clone).rglob("*"):
        if p.is_file():
            seen += 1
            assert secret.encode() not in p.read_bytes(), p
    return seen


def test_a_token_shaped_string_stops_the_save_and_is_never_shown(wc, case, capsys):
    secret = token_like()
    (case.path / ".dev" / "local" / "notes.log").write_text(
        f"line\nkey = {secret}\n", encoding="utf-8"
    )
    before = case.snapshot()
    result = case.run()
    assert not result.ok
    assert result.reason == "saved copy failed: possible secret in .dev/local/notes.log"
    assert secret not in result.reason and secret not in " ".join(case.notes)
    out = capsys.readouterr()
    assert secret not in out.out and secret not in out.err
    assert case.snapshot() == before
    # the check runs before the evidence clone is touched, so it was never made
    assert not Path(case.clone).exists()
    assert case.remote_files(BASE) == []
    # with a clone that already holds a save, every file of it is clean too
    clean = case.path / ".dev" / "local" / "notes.log"
    clean.write_text("line\n", encoding="utf-8")
    assert case.run().ok
    clean.write_text(f"line\nkey = {secret}\n", encoding="utf-8")
    assert not case.run().ok
    assert assert_value_in_no_clone_file(secret, case.clone) > 4


def test_the_secret_check_finds_a_token_split_across_read_blocks(wc, tmp_path):
    secret = token_like()
    path = tmp_path / "f.log"
    path.write_bytes(
        b"x" * ((1 << 20) - 10) + b" " + secret.encode() + b" " + b"y" * 50
    )
    assert wc.file_has_secret(str(path)) is True
    clean = tmp_path / "clean.log"
    clean.write_bytes(b"x" * ((1 << 20) + 5000))
    assert wc.file_has_secret(str(clean)) is False


@pytest.mark.parametrize(
    "prefix", ["github" + "_pat_", "sk" + "-", "AKIA", "xox" + "b-"]
)
def test_other_token_shapes_are_found(wc, tmp_path, prefix):
    path = tmp_path / "f.txt"
    tail = (
        "A1B2C3D4E5F6G7H8J9K0L1M2N3O4P5Q6R7S8"
        if prefix != "AKIA"
        else "A1B2C3D4E5F6G7H8"
    )
    path.write_text(f"v = {prefix}{tail}\n", encoding="utf-8")
    assert wc.file_has_secret(str(path))


@pytest.mark.parametrize(
    "name",
    [
        ".dev/.env",
        ".dev/x/.env.local",
        ".dev/id_rsa",
        ".dev/k.pem",
        ".dev/a.key",
        ".dev/credentials.json",
        ".dev/secrets.yaml",
        ".dev/.netrc",
    ],
)
def test_secret_looking_file_names_stop_the_save(wc, case, name):
    write(case.path / name, "harmless\n")
    result = case.run(
        facts=dataclasses.replace(case.facts(), state=_with_ignored(wc, case, name))
    )
    assert result.reason == f"saved copy failed: possible secret in {name}"


def _with_ignored(wc, case, name):
    state = case.facts().state
    return dataclasses.replace(state, untracked_dev=[*state.untracked_dev, name])


def test_ordinary_file_names_and_text_do_not_trip_the_check(wc, tmp_path):
    for name in (
        ".dev/tasks/report.md",
        ".dev/keys-notes.md",
        ".dev/skeleton.txt",
        ".dev/environment.md",
    ):
        assert not wc.SECRET_NAME_RE.search(name), name
    path = tmp_path / "ok.md"
    path.write_text(
        "a branch called ghp_x and sk-short are not tokens\n", encoding="utf-8"
    )
    assert not wc.file_has_secret(str(path))


def test_only_plain_regular_files_are_saved(wc, case):
    link = case.path / ".dev" / "tasks" / "link.md"
    link.symlink_to(case.path / ".dev" / "tasks" / "a b.md")
    state = case.facts().state
    state = dataclasses.replace(
        state, untracked_dev=[*state.untracked_dev, ".dev/tasks/link.md"]
    )
    result = case.run(facts=dataclasses.replace(case.facts(), state=state))
    assert (
        result.reason == "saved copy failed: .dev/tasks/link.md is not a regular file"
    )
    bad = dataclasses.replace(case.facts().state, untracked_dev=[".dev/../README.md"])
    assert case.run(
        facts=dataclasses.replace(case.facts(), state=bad)
    ).reason.startswith("saved copy failed: unusable file name")


def test_an_earlier_folder_that_was_never_pushed_is_not_counted_as_covered(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    for failing, first_reason, again_reason in (
        ("add", "the saved folder could not be staged", "the copy on origin/main"),
        ("commit", "the evidence commit failed", "the evidence clone could not be brought"),
    ):  # fmt: skip

        def fails(argv, cwd, failing=failing):
            return _result(wc, 1, "", "refused") if failing in argv else None

        sub = tmp_path / failing
        sub.mkdir()
        c = Case(
            wc, runner_cls, throwaway_repo, evidence_bare, sub, replies={"git": fails}
        )
        first = c.run()
        assert first.reason == f"saved copy failed: {first_reason}"
        assert (Path(c.clone) / BASE).is_dir()  # renamed into place, never pushed
        c.runner = runner_cls(
            evidence_dir=c.clone
        )  # the next run has a working add and commit
        write(c.path / ".dev" / "tasks" / "new.md", "new\n")
        again = c.run()
        assert not again.ok and again.reason.startswith(
            f"saved copy failed: {again_reason}"
        )
        assert not (Path(c.clone) / f"{BASE}-r2").exists()
        assert c.remote_files(BASE) == []
        throwaway_repo = type(throwaway_repo)(
            tmp_path / f"repo-{failing}"
        )  # a fresh repo for the next pass


@pytest.mark.skipif(os.geteuid() == 0, reason="root can read any file")
def test_an_unreadable_file_is_a_saved_copy_failed_result_not_an_exception(wc, case):
    secret_file = case.path / ".dev" / "local" / "locked.log"
    secret_file.write_text("x\n", encoding="utf-8")
    secret_file.chmod(0)
    try:
        result = case.run()
    finally:
        secret_file.chmod(0o644)
    assert not result.ok
    assert (
        result.reason == "saved copy failed: a file could not be read (PermissionError)"
    )
    assert not Path(case.clone).exists()


def test_a_file_name_that_cannot_be_written_is_a_saved_copy_failed_result(wc, case):
    odd = ".dev/tasks/" + "\udcff" + ".md"  # a name that is not valid UTF-8
    state = case.facts().state
    state = dataclasses.replace(state, untracked_dev=[*state.untracked_dev, odd])
    write_bytes = (
        case.path / ".dev" / "tasks" / (b"\xff.md".decode("utf-8", "surrogateescape"))
    )
    write_bytes.write_text("x\n", encoding="utf-8")
    result = case.run(facts=dataclasses.replace(case.facts(), state=state))
    assert not result.ok and result.reason.startswith("saved copy failed")


def test_ordinary_hyphenated_words_are_not_token_shaped(wc, tmp_path):
    path = tmp_path / "report.md"
    path.write_text(
        "disk-usage-report-for-the-workspace-today\n"
        "task-queue-length-summary-for-this-run\n"
        "mask-AKIA" + "0123456789ABCDEF\n"
        "my-ghp_" + "A1b2C3d4" * 4 + "\n",
        encoding="utf-8",
    )
    assert not wc.file_has_secret(str(path))
    real = tmp_path / "real.md"
    real.write_text(
        "key=sk" + "-" + "A1b2C3d4" * 4 + "\nid: AKIA" + "0123456789ABCDEF\n",
        encoding="utf-8",
    )
    assert wc.file_has_secret(str(real))


# -- Task 10: two clones pushing at the same time, the secret value in an existing clone ---------


def test_two_clones_pushing_different_folders_both_end_up_on_origin_main(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    from .conftest import ThrowawayRepo

    first_dir, second_dir = tmp_path / "one", tmp_path / "two"
    first_dir.mkdir()
    second_dir.mkdir()
    first = Case(wc, runner_cls, throwaway_repo, evidence_bare, first_dir)
    pushes = {"n": 0}

    def race(argv, cwd):
        """The second clone's first push loses: the first clone pushes in between."""
        if "push" in argv:
            pushes["n"] += 1
            if pushes["n"] == 1:
                assert first.run().ok  # origin/main moves under the second clone
                return _result(wc, 1, "", "! [rejected] main -> main (fetch first)")
        return None

    second = Case(
        wc,
        runner_cls,
        ThrowawayRepo(tmp_path / "repo2"),
        evidence_bare,
        second_dir,
        replies={"git": race},
    )
    result = second.run(pr=make_pr(wc, number=701))
    assert result.ok, result.reason
    assert (
        pushes["n"] == 2
    )  # refused once, then the retry after fetch and rebase went through
    folder_one, folder_two = BASE, "IronClaude/example-user/2026-11-10_pr701_topic"
    assert second.remote_files(folder_one) and second.remote_files(folder_two)
    assert result.folder == folder_two
    # a linear history: both archive commits are on main, the second on top of the first
    subjects = git_in(evidence_bare, "log", "--format=%s", "main").splitlines()
    assert subjects[:2] == [
        "archive(IronClaude): 2026-11-10 pr701 topic",
        "archive(IronClaude): 2026-11-10 pr700 topic",
    ]
    assert (
        git_in(evidence_bare, "rev-list", "--merges", "--count", "main").strip() == "0"
    )


def test_a_secret_stops_the_save_even_when_the_clone_already_exists(wc, case, capsys):
    assert case.run().ok  # the clone now exists and holds the first save
    secret = token_like()
    (case.path / ".dev" / "local" / "later.log").write_text(
        f"x {secret} y\n", encoding="utf-8"
    )
    result = case.run()
    assert result.reason == "saved copy failed: possible secret in .dev/local/later.log"
    out = capsys.readouterr()
    shown = [result.reason, " ".join(case.notes), out.out, out.err]
    assert all(secret not in text for text in shown)
    assert (
        assert_value_in_no_clone_file(secret, case.clone) > 4
    )  # every file, .git included
    assert case.remote_files(f"{BASE}-r2") == []


def test_no_test_here_pushes_to_a_network_remote_or_reads_a_credential_file():
    text = Path(__file__).read_text(encoding="utf-8")
    for needle in (
        "hosts" + ".yml",
        "git@" + "github",
        "push " + "https://",
        "~/." + "env",
        "gh auth " + "token",
    ):
        assert needle not in text, needle
    # every remote used by these tests is a local path made under tmp_path
    assert "evidence_bare" in text and "str(self.bare)" in text


def test_the_step_never_runs_a_command_the_runner_would_refuse(wc, case):
    assert case.run().ok
    verbs = {
        tuple(c.argv[:2]) if c.argv[0] != "git" else tuple(c.argv[1:2])
        for c in case.runner.commands
    }
    assert not any(
        "-D" in c.argv or "--force" in c.argv or "-f" in c.argv
        for c in case.runner.commands
    )
    assert ("add",) in verbs and ("commit",) in verbs and ("tar", "-tzf") in verbs
