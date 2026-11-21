"""Facts the script reads: Orca (Task 3), then git and GitHub (Tasks 4 and 5).

Orca replies come from the hand-written files in ``fixtures/``; no real Orca is started.
"""

from __future__ import annotations

import ast
import inspect
import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def fixture_text(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


# --- Task 3: Orca, read only ----------------------------------------------------


def test_repo_list_fixture_gives_id_path_and_name(wc):
    read = wc.parse_orca_repos(fixture_text("orca_repo_list.json"))
    assert read.ok and read.unavailable is None
    assert [(r.name, r.path) for r in read.items] == [
        ("IronClaude", "/work/example/IronClaude"),
        ("Coder", "/work/example/Coder"),
    ]
    assert all(r.id for r in read.items)


def test_worktree_ps_fixture_gives_every_named_field(wc):
    read = wc.parse_orca_worktrees(fixture_text("orca_worktree_ps.json"))
    assert read.ok
    main, pinned, third = read.items
    assert main.selector == "id:" + main.worktree_id
    assert main.worktree_id.endswith("::/work/example/IronClaude")
    assert main.path == "/work/example/IronClaude"
    assert main.last_activity_ms == 1795095396714
    assert main.is_pinned is False and main.live_terminal_count == 2
    assert main.linked_pr_hint["state"] == "merged"
    assert main.comment == ""
    assert pinned.is_pinned is True and pinned.comment.startswith("keep until")
    assert pinned.linked_pr_hint is None and pinned.live_terminal_count == 0
    # a missing lastActivityAt and a null comment are accepted
    assert third.last_activity_ms is None and third.comment == ""
    assert third.linked_pr_hint["state"] == "open"


def test_reference_and_terminal_fixtures(wc):
    refs = wc.parse_orca_references(fixture_text("orca_reference_list.json"))
    assert refs.ok and [r.raw["number"] for r in refs.items] == [687, 700]
    terms = wc.parse_orca_terminals(fixture_text("orca_terminal_list.json"))
    assert terms.ok
    assert [t.handle for t in terms.items] == ["term_example_1", "term_example_2"]
    assert terms.items[0].title == "claude"


def test_empty_lists_are_a_valid_answer(wc):
    for parse, key in (
        (wc.parse_orca_repos, "repos"),
        (wc.parse_orca_worktrees, "worktrees"),
        (wc.parse_orca_references, "references"),
        (wc.parse_orca_terminals, "terminals"),
    ):
        read = parse(json.dumps({"ok": True, "result": {key: []}}))
        assert read.ok and read.items == ()


def _ps_with(**change):
    doc = json.loads(fixture_text("orca_worktree_ps.json"))
    doc["result"]["worktrees"][0].update(change)
    return json.dumps(doc)


MALFORMED = [
    ("repos", "not json at all"),
    ("repos", ""),
    ("repos", "null"),
    ("repos", "[1, 2]"),
    ("repos", '{"ok": false, "error": "boom"}'),
    ("repos", '{"ok": true, "result": {"worktrees": []}}'),
    ("repos", '{"ok": true, "result": {"repos": [{"id": "x"}]}}'),
    ("repos", '{"ok": true, "result": {"repos": "no"}}'),
    ("worktrees", '{"ok": true, "result": {"worktrees": [{"path": "/x"}]}}'),
    ("worktrees", _ps_with(isPinned="no")),
    ("worktrees", _ps_with(liveTerminalCount=-1)),
    ("worktrees", _ps_with(liveTerminalCount=True)),
    ("worktrees", _ps_with(liveTerminalCount="2")),
    ("worktrees", _ps_with(lastActivityAt="yesterday")),
    ("worktrees", _ps_with(linkedPR="merged")),
    ("worktrees", _ps_with(comment=5)),
    ("worktrees", _ps_with(path="")),
    ("references", '{"ok": true, "result": {"terminals": []}}'),
    ("references", '{"ok": true, "result": {"references": [1]}}'),
    ("terminals", '{"ok": true, "result": {"terminals": [{"title": "x"}]}}'),
    ("terminals", "{"),
]


@pytest.mark.parametrize(
    "kind,text", MALFORMED, ids=[f"{k}-{i}" for i, (k, _) in enumerate(MALFORMED)]
)
def test_a_malformed_reply_is_orca_unavailable_not_an_exception(wc, kind, text):
    parse = {
        "repos": wc.parse_orca_repos,
        "worktrees": wc.parse_orca_worktrees,
        "references": wc.parse_orca_references,
        "terminals": wc.parse_orca_terminals,
    }[kind]
    read = parse(text)
    assert read.ok is False and read.items == ()
    assert read.unavailable.startswith("Orca unavailable: ")


# --- the reads go through the runner ----------------------------------------------


@pytest.fixture
def orca_runner(wc, runner_cls):
    """Build a runner whose Orca answers come from ``{argv tuple: stdout or (code, stdout)}``."""

    def build(replies):
        def handler(argv, cwd):
            answer = replies.get(tuple(argv))
            if answer is None:
                return None
            code, out = answer if isinstance(answer, tuple) else (0, answer)
            return wc.Result(code, out, "")

        return runner_cls(replies={"orca": handler})

    return build


SEL = "id:11111111-1111-4111-8111-111111111111::/work/example/IronClaude"


def test_each_read_issues_only_its_read_verb_and_returns_rows(wc, orca_runner):
    runner = orca_runner(
        {
            ("orca", "repo", "list", "--json"): fixture_text("orca_repo_list.json"),
            ("orca", "worktree", "ps", "--json"): fixture_text("orca_worktree_ps.json"),
            (
                "orca",
                "reference",
                "list",
                "--worktree",
                SEL,
                "--json",
            ): fixture_text("orca_reference_list.json"),
            (
                "orca",
                "terminal",
                "list",
                "--worktree",
                SEL,
                "--json",
            ): fixture_text("orca_terminal_list.json"),
        }
    )
    assert wc.read_orca_repos(runner).ok
    worktrees = wc.read_orca_worktrees(runner)
    assert worktrees.ok and worktrees.items[0].selector == SEL
    assert wc.read_orca_references(runner, SEL).ok
    assert wc.read_orca_terminals(runner, SEL).ok
    verbs = [tuple(c.argv[1:3]) for c in runner.commands]
    assert verbs == [
        ("repo", "list"),
        ("worktree", "ps"),
        ("reference", "list"),
        ("terminal", "list"),
    ]
    flat = [t for c in runner.commands for t in c.argv]
    assert "close" not in flat and "rm" not in flat and "--force" not in flat


def test_a_failed_or_unanswered_read_is_orca_unavailable(wc, orca_runner):
    runner = orca_runner({("orca", "worktree", "ps", "--json"): (1, "")})
    read = wc.read_orca_worktrees(runner)
    assert read.ok is False and "exited with 1" in read.unavailable
    # no canned reply at all: the recording runner answers 127, as a missing program would
    assert wc.read_orca_repos(runner).unavailable.startswith("Orca unavailable")
    # a clean exit with a broken body
    runner = orca_runner({("orca", "worktree", "ps", "--json"): "<html>"})
    assert wc.read_orca_worktrees(runner).unavailable.startswith("Orca unavailable")


def test_repo_list_falls_back_to_the_current_checkout_and_says_so(wc):
    current = wc.OrcaRepo("current", "/work/example/IronClaude", "IronClaude")
    good = wc.parse_orca_repos(fixture_text("orca_repo_list.json"))
    repos, note = wc.repos_or_current(good, current)
    assert [r.name for r in repos] == ["IronClaude", "Coder"] and note == ""
    bad = wc.parse_orca_repos("nope")
    repos, note = wc.repos_or_current(bad, current)
    assert repos == [current]
    assert "Orca unavailable" in note and "current checkout" in note


def test_an_empty_repo_list_also_falls_back_to_the_current_checkout(wc):
    current = wc.OrcaRepo("current", "/work/example/IronClaude", "IronClaude")
    empty = wc.parse_orca_repos('{"result": {"repos": []}}')
    assert empty.ok and not empty.items
    repos, note = wc.repos_or_current(empty, current)
    assert repos == [current]
    assert "Orca lists no repos" in note and "current checkout" in note


# --- guard rails of Task 3 -------------------------------------------------------------


def test_the_read_functions_never_name_a_close_or_remove_verb(wc):
    for fn in (
        wc.read_orca_repos,
        wc.read_orca_worktrees,
        wc.read_orca_references,
        wc.read_orca_terminals,
        wc._orca_read,
    ):
        src = inspect.getsource(fn)
        for word in ('"close"', '"rm"', '"--force"', '"create"'):
            assert word not in src, (fn.__name__, word)


def test_linked_pr_hint_is_read_by_no_rule_function(wc):
    """Only the parser sets it; nothing else in the script reads it as proof of a merge."""
    tree = ast.parse(Path(wc.__file__).read_text(encoding="utf-8"))
    readers = []
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            for node in ast.walk(fn):
                if isinstance(node, ast.Attribute) and node.attr == "linked_pr_hint":
                    readers.append(fn.name)
    assert readers == []
    # the field is still part of the record
    assert "linked_pr_hint" in {f for f in wc.OrcaWorktree.__dataclass_fields__}
    assert "linkedPR" in Path(wc.__file__).read_text(encoding="utf-8")


def test_no_dash_characters_in_the_fixtures():
    for path in FIXTURES.iterdir():
        text = path.read_text(encoding="utf-8")
        assert chr(0x2013) not in text and chr(0x2014) not in text, path


# --- Task 4: git facts, local state and the process scan ----------------------------------

import os  # noqa: E402
import shutil  # noqa: E402

from .conftest import git_in, make_fake_proc  # noqa: E402


def write(path: Path, text: str = "x\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def facts_for(wc, runner_cls, repo, path, orca=None):
    runner = runner_cls()
    found = wc.discover_worktrees(runner, [wc.OrcaRepo("r", str(repo.main), "example")])
    entry = next(
        w for w in found.worktrees if os.path.realpath(w.path) == os.path.realpath(path)
    )
    return runner, wc.gather_facts(runner, entry, orca)


def test_discovery_finds_main_linked_detached_and_locked_worktrees(
    wc, runner_cls, throwaway_repo
):
    linked = throwaway_repo.add_worktree("topic")
    detached = throwaway_repo.root / "wts" / "loose"
    git_in(throwaway_repo.main, "worktree", "add", "-q", "--detach", str(detached))
    locked = throwaway_repo.add_worktree("held")
    git_in(throwaway_repo.main, "worktree", "lock", str(locked))
    gone = throwaway_repo.add_worktree("gone")
    shutil.rmtree(gone)  # a throwaway folder: the entry stays listed as prunable
    runner = runner_cls()
    repo = wc.OrcaRepo("r", str(throwaway_repo.main), "example")
    found = wc.discover_worktrees(
        runner, [repo, repo]
    )  # a repo listed twice counts once
    by_name = {os.path.basename(w.path): w for w in found.worktrees}
    assert set(by_name) == {"main", "topic", "loose", "held", "gone"}
    assert by_name["main"].is_main and by_name["main"].branch == "main"
    assert not by_name["topic"].is_main and by_name["topic"].branch == "topic"
    assert by_name["loose"].detached and by_name["loose"].branch is None
    assert by_name["held"].locked and not by_name["topic"].locked
    assert by_name["gone"].prunable
    assert all(len(w.head) == 40 for w in found.worktrees)
    assert found.failures == ()
    assert os.path.realpath(linked) == os.path.realpath(by_name["topic"].path)
    # facts of a missing folder: not present, nothing read, nothing raised
    _, gone_facts = facts_for(wc, runner_cls, throwaway_repo, gone)
    assert gone_facts.present is False and gone_facts.head is None


def test_a_failed_listing_is_a_note_not_an_exception(wc, never_run_runner):
    class Fails(type(never_run_runner)):
        def _execute(self, argv, cwd, stdin):
            return wc.Result(128, "", "not a git repository")

    found = wc.discover_worktrees(
        Fails(evidence_dir="/x"), [wc.OrcaRepo("r", "/nowhere", "n")]
    )
    assert found.worktrees == () and "git worktree list failed" in found.failures[0]


def test_clean_worktree_facts(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("clean")
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert f.present and f.failures == []
    assert f.head == git_in(path, "rev-parse", "HEAD").strip()
    assert f.origin.owner == "IronbellyOrg" and f.origin.is_ours
    assert f.state.changed_tracked == [] and f.state.untracked_outside_dev == []
    assert f.state.untracked_dev == [] and f.state.ignored_dev == []
    assert f.state.ignored_build == [] and f.state.ignored_unknown == []
    assert f.git_dir.endswith(os.path.join("worktrees", "clean"))
    assert f.keep_file is False and f.operations == [] and f.nested_checkouts == []
    assert f.size_bytes > 0
    assert f.last_commit_ts and f.git_file_mtime and f.created_ts
    assert f.idle_days(f.newest_activity() + 86400 * 3) == pytest.approx(3.0)


def test_changed_tracked_file_and_staged_file(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("edited")
    write(path / "README.md", "changed\n")
    write(path / "added.txt")
    git_in(path, "add", "added.txt")
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert sorted(f.state.changed_tracked) == ["README.md", "added.txt"]
    assert f.state.untracked_outside_dev == []


def test_untracked_file_outside_dev(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("loose-files")
    write(path / "notes.txt")
    write(path / "sub" / "deep.txt")
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert sorted(f.state.untracked_outside_dev) == ["notes.txt", "sub/deep.txt"]
    assert f.state.untracked_dev == [] and f.state.changed_tracked == []


def test_untracked_and_ignored_files_under_dev(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("devfiles")
    write(path / ".dev" / "tasks" / "a.md")
    write(path / ".dev" / "local" / "run.log")  # ignored by the tracked .gitignore
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert f.state.untracked_dev == [".dev/tasks/a.md"]
    assert f.state.ignored_dev == [".dev/local/run.log"]
    assert f.state.untracked_outside_dev == [] and f.state.ignored_unknown == []


def test_ignored_environment_file_outside_dev_is_unknown_local_state(
    wc, runner_cls, throwaway_repo
):
    path = throwaway_repo.add_worktree("envfile")
    write(path / ".env", "NAME=value\n")
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert f.state.ignored_unknown == [".env"]
    assert f.state.ignored_build == [] and f.state.ignored_generated == []


def test_only_build_output_and_generated_copies(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("buildonly")
    write(path / "pkg" / "__pycache__" / "m.pyc")
    write(path / ".venv" / "lib" / "x.py")
    write(path / "node_modules" / "p" / "i.js")
    write(path / "dist" / "a.whl")
    write(path / ".claude" / "agents" / "a.md")
    write(path / ".serena" / "cache" / "c.json")
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert sorted(f.state.ignored_build) == [
        ".venv/lib/x.py",
        "dist/a.whl",
        "node_modules/p/i.js",
        "pkg/__pycache__/m.pyc",
    ]
    assert sorted(f.state.ignored_generated) == [
        ".claude/agents/a.md",
        ".serena/cache/c.json",
    ]
    assert f.state.ignored_unknown == [] and f.state.changed_tracked == []


def test_classify_status_edge_cases(wc):
    raw = "\0".join(
        [
            "R  new name.txt",
            "old name.txt",
            " D gone.txt",
            "UU conflict.txt",
            "?? .dev/a.md",
            "!! .dev/pkg/__pycache__/x.pyc",
            "!! .env",
            "!! uv.lock",
            "",
        ]
    )
    s = wc.classify_status(raw)
    assert s.changed_tracked == ["new name.txt", "gone.txt", "conflict.txt"]
    assert s.untracked_dev == [".dev/a.md"]
    assert s.ignored_dev == [".dev/pkg/__pycache__/x.pyc"]
    assert s.ignored_unknown == [".env"] and s.ignored_build == ["uv.lock"]
    assert wc.classify_status("").changed_tracked == []
    assert wc.classify_status("junk\0??x\0").untracked_outside_dev == []


def test_keep_file_git_operation_and_nested_checkout(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("busy")
    write(path / ".worktree-keep", "")
    nested = path / "inner"
    nested.mkdir()
    git_in(nested, "init", "-q")
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert f.keep_file is True
    assert f.nested_checkouts == ["inner/.git"]
    write(Path(f.git_dir) / "MERGE_HEAD", "0" * 40 + "\n")
    write(Path(f.git_dir) / "index.lock", "")
    (Path(f.git_dir) / "rebase-merge").mkdir()
    _, again = facts_for(wc, runner_cls, throwaway_repo, path)
    assert again.operations == ["MERGE_HEAD", "rebase-merge", "index.lock"]


def test_the_git_reads_change_nothing(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("readonly")
    write(path / "untracked.txt")
    git_dir = Path(git_in(path, "rev-parse", "--absolute-git-dir").strip())
    before = {p.name: p.read_bytes() for p in git_dir.iterdir() if p.is_file()}
    head_before = git_in(path, "rev-parse", "HEAD")
    runner, _ = facts_for(wc, runner_cls, throwaway_repo, path)
    after = {p.name: p.read_bytes() for p in git_dir.iterdir() if p.is_file()}
    assert before == after
    assert git_in(path, "rev-parse", "HEAD") == head_before
    assert (path / "untracked.txt").exists()
    verbs = {tuple(c.argv[1:3]) for c in runner.commands}
    assert verbs <= {
        ("worktree", "list"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "--git-dir"),
        ("remote", "get-url"),
        ("status", "--porcelain"),
        ("log", "-1"),
    }
    assert verbs >= {("worktree", "list"), ("status", "--porcelain"), ("log", "-1")}


def test_a_worktree_with_no_origin_remote_is_a_verdict_not_an_unread_fact(
    wc, runner_cls, throwaway_repo
):
    path = throwaway_repo.add_worktree("no-origin")
    git_in(throwaway_repo.main, "remote", "remove", "origin")
    _, f = facts_for(wc, runner_cls, throwaway_repo, path)
    assert f.origin is None and f.origin_unread == ""
    assert "git remote get-url origin failed" not in f.failures


def test_a_failed_origin_read_is_recorded_as_unread(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("origin-broken")

    def git_reply(argv, cwd):
        if argv[1:4] == ["remote", "get-url", "origin"]:
            return wc.Result(128, "", "fatal: not a git repository")
        return None

    runner = runner_cls(replies={"git": git_reply})
    found = wc.discover_worktrees(
        runner, [wc.OrcaRepo("r", str(throwaway_repo.main), "example")]
    )
    entry = next(
        w for w in found.worktrees if os.path.realpath(w.path) == os.path.realpath(path)
    )
    f = wc.gather_facts(runner, entry)
    assert f.origin is None
    assert f.origin_unread == "git remote get-url origin exited with 128"
    assert "git remote get-url origin failed" in f.failures


def test_git_runs_with_optional_locks_off(runner_cls):
    assert runner_cls()._env_for(["git", "status"])["GIT_OPTIONAL_LOCKS"] == "0"


def test_orca_activity_joins_the_idle_time(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("watched")
    ps = wc.parse_orca_worktrees(fixture_text("orca_worktree_ps.json")).items[0]
    _, plain = facts_for(wc, runner_cls, throwaway_repo, path)
    _, with_orca = facts_for(wc, runner_cls, throwaway_repo, path, orca=ps)
    assert plain.orca_activity_ts is None
    assert with_orca.orca_activity_ts == 1795095396.714
    assert with_orca.newest_activity() == max(plain.newest_activity(), 1795095396.714)


def test_idle_and_age_arithmetic(wc):
    wt = wc.GitWorktree("/x", "/r", "h" * 40, "b", False, False, False, False, False)
    f = wc.WorktreeFacts(
        worktree=wt,
        git_file_mtime=1_000_000.0,
        last_commit_ts=1_050_000.0,
        orca_activity_ts=900_000.0,
        created_ts=500_000.0,
    )
    assert f.newest_activity() == 1_050_000.0
    assert f.idle_days(1_050_000.0 + 86400 * 8) == pytest.approx(8.0)
    assert f.age_days(500_000.0 + 86400) == pytest.approx(1.0)
    assert (
        f.idle_days(0) == 0.0
    )  # a clock before the activity never gives a negative age
    assert wc.WorktreeFacts(worktree=wt).idle_days(5.0) is None


@pytest.mark.parametrize(
    "url,owner,repo,ours",
    [
        (
            "https://github.com/IronbellyOrg/IronClaude.git",
            "IronbellyOrg",
            "IronClaude",
            True,
        ),
        (
            "https://github.com/IronbellyOrg/IronClaude",
            "IronbellyOrg",
            "IronClaude",
            True,
        ),
        (
            "https://user@github.com/ironbellygroup/Coder.git\n",
            "ironbellygroup",
            "Coder",
            True,
        ),
        (
            "git@github.com:IronbellyOrg/IronClaude.git",
            "IronbellyOrg",
            "IronClaude",
            True,
        ),
        ("ssh://git@github.com/IronbellyGroup/x.git/", "IronbellyGroup", "x", True),
        (
            "https://github.com/SuperClaude-Org/SuperClaude_Framework.git",
            "SuperClaude-Org",
            "SuperClaude_Framework",
            False,
        ),
        ("https://github.com/IronbellyOrgX/x.git", "IronbellyOrgX", "x", False),
    ],
)
def test_origin_owner(wc, url, owner, repo, ours):
    info = wc.parse_origin(url)
    assert (info.owner, info.repo, info.is_ours) == (owner, repo, ours)


def test_origin_that_is_not_github_or_not_a_url_is_none(wc):
    for url in (
        "https://example.com/IronbellyOrg/x.git",
        "",
        "github.com",
        "/local/path",
    ):
        assert wc.parse_origin(url) is None


@pytest.mark.parametrize(
    "url",
    [
        # github.com only appears inside the path of another host
        "https://mirror.example/github.com/IronbellyOrg/IronClaude.git",
        # github.com is only the tail of a look-alike host
        "https://evilgithub.com/IronbellyOrg/IronClaude.git",
        "https://github.com.evil.example/IronbellyOrg/IronClaude.git",
        "git@github.com.evil.example:IronbellyOrg/IronClaude.git",
        # more or fewer path parts than owner/repo
        "https://github.com/IronbellyOrg/IronClaude/extra.git",
        "https://github.com/IronbellyOrg",
        "git@github.com:IronbellyOrg",
    ],
)
def test_origin_with_a_lookalike_host_or_wrong_path_shape_is_none(wc, url):
    assert wc.parse_origin(url) is None


def test_name_guard_is_anchored_at_the_start(wc):
    for name in (
        "orca-port-evidence",
        "orca-recipe-x",
        "orca-pristine-y",
        "orca-old-patched",
    ):
        assert wc.name_guard(f"/some/dir/{name}"), name
    for name in (
        "coder-orca-port",
        "orca-old-patched-2",
        "my-orca-recipe-x",
        "issue-687",
    ):
        assert not wc.name_guard(f"/some/dir/{name}"), name
    assert wc.name_guard("/some/dir/orca-port-a/")


def test_the_script_own_folder_is_compared_by_real_path(wc, tmp_path):
    wt = tmp_path / "wt"
    (wt / "sub").mkdir(parents=True)
    other = tmp_path / "wt-sibling"
    other.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(wt)
    assert wc.is_own_folder(str(wt), [str(wt / "sub")])
    assert wc.is_own_folder(str(wt), [str(alias / "sub")])
    assert wc.is_own_folder(str(alias), [str(wt)])
    assert not wc.is_own_folder(str(wt), [str(other)])
    assert not wc.is_own_folder(str(wt), [])


# --- the process scan, on a fake /proc ------------------------------------------------------


fake_proc = make_fake_proc  # the builder lives in conftest.py


def test_scan_finds_a_process_inside_and_not_a_sibling_folder(wc, tmp_path):
    wt = tmp_path / "wt"
    (wt / "sub").mkdir(parents=True)
    sibling = tmp_path / "wt2"
    sibling.mkdir()
    proc = fake_proc(tmp_path / "proc", {101: wt / "sub", 102: sibling, 103: wt})
    scan = wc.scan_processes(str(proc))
    assert scan.ok and scan.failure == ""
    inside = wc.processes_inside(scan, str(wt))
    assert inside == [(101, "proc101"), (103, "proc103")]
    assert wc.processes_inside(scan, str(tmp_path / "elsewhere")) == []


def test_scan_ignores_a_vanished_entry_and_another_users_entry(wc, tmp_path):
    wt = tmp_path / "wt"
    wt.mkdir()
    proc = fake_proc(tmp_path / "proc", {201: wt, 202: None, 203: wt})

    def readlink(path):
        if "/203/" in path:
            raise PermissionError(13, "Permission denied", path)
        return os.readlink(path)

    scan = wc.scan_processes(
        str(proc), my_uid=1000, readlink=readlink, uid_of=lambda p: 0
    )
    assert scan.ok
    assert [pid for pid, _, _ in scan.cwds] == [
        201
    ]  # 202 vanished, 203 is another user's
    assert scan.notes == ("pid 203: another user's process, ignored",)

    def exits_while_checking(path):
        raise ProcessLookupError(3, "No such process", path)

    assert wc.scan_processes(str(proc), readlink=exits_while_checking).cwds == ()


def test_scan_fails_for_any_other_error(wc, tmp_path):
    wt = tmp_path / "wt"
    wt.mkdir()
    # a cwd that is not a link: readlink gives EINVAL, which is neither of the ignored cases
    proc = fake_proc(tmp_path / "p1", {301: wt, 302: "file"})
    scan = wc.scan_processes(str(proc))
    assert scan.ok is False and "pid 302" in scan.failure and scan.cwds == ()
    # permission denied for a process of our own user
    proc = fake_proc(tmp_path / "p2", {401: wt})

    def denied(path):
        raise PermissionError(13, "Permission denied", path)

    own = wc.scan_processes(str(proc), my_uid=7, readlink=denied, uid_of=lambda p: 7)
    assert own.ok is False and "401" in own.failure

    # the owner check itself fails for another reason
    def broken_owner(path):
        raise OSError(5, "Input/output error", path)

    scan = wc.scan_processes(str(proc), my_uid=7, readlink=denied, uid_of=broken_owner)
    assert scan.ok is False
    # the folder cannot be listed
    assert wc.scan_processes(str(tmp_path / "missing")).ok is False


def test_scan_reads_the_real_proc_without_failing_on_this_machine(wc):
    scan = wc.scan_processes()
    assert scan.ok or scan.failure  # a result either way, never an exception
    if scan.ok:
        mine = [pid for pid, _, _ in scan.cwds]
        assert os.getpid() in mine


# --- Task 5: GitHub facts, with a fake gh and a fake landed check -------------------------

import dataclasses  # noqa: E402

SLUG = "IronbellyOrg/IronClaude"


def gh_key(argv):
    """('pr', 'list') or ('issue', 'view', '373', 'owner/repo') from a full gh argument list."""
    repo = argv[argv.index("--repo") + 1] if "--repo" in argv else ""
    if argv[2] == "list":
        return (argv[1], "list", repo)
    return (argv[1], argv[2], argv[3], repo)


def gh_fake(wc, table):
    """A gh handler: ``table`` maps gh_key to (code, stdout, stderr); no entry means HTTP failure."""

    def handler(argv, cwd):
        code, out, err = table.get(gh_key(argv), (1, "", "HTTP 502: bad gateway"))
        return wc.Result(code, out, err)

    return handler


def pr_row(number, state, **extra):
    row = {
        "number": number,
        "state": state,
        "headRefOid": "a" * 40,
        "author": {"login": "someone"},
        "mergedAt": None,
        "title": "title",
        "body": "",
        "closingIssuesReferences": [],
        "headRefName": "topic",
    }
    row.update(extra)
    return row


NOT_FOUND = (
    1,
    "",
    "GraphQL: Could not resolve to an issue or pull request with the number",
)


def assert_every_gh_call_names_its_repo(runner):
    gh_calls = [c.argv for c in runner.commands if c.argv[0] == "gh"]
    assert gh_calls
    for argv in gh_calls:
        assert "--repo" in argv and argv[argv.index("--repo") + 1].count("/") == 1
        assert "api" not in argv and "{owner}/{repo}" not in argv


def test_newest_merged_pull_request_wins_and_fields_are_recorded(wc, runner_cls):
    rows = [
        pr_row(5, "OPEN"),
        pr_row(7, "MERGED", mergedAt="2026-11-01T00:00:00Z", headRefOid="b" * 40),
        pr_row(
            9,
            "MERGED",
            mergedAt="2026-11-10T00:00:00Z",
            headRefOid="c" * 40,
            title="Later title",
            body="Body #3",
            closingIssuesReferences=[
                {
                    "number": 12,
                    "repository": {
                        "name": "IronClaude",
                        "owner": {"login": "IronbellyOrg"},
                    },
                },
                {"number": 13},
            ],
        ),
    ]
    runner = runner_cls(
        replies={"gh": gh_fake(wc, {("pr", "list", SLUG): (0, json.dumps(rows), "")})}
    )
    found = wc.find_pull_request(runner, SLUG, "topic")
    assert found.ok and found.pr.number == 9 and found.pr.state == "MERGED"
    assert found.pr.head_oid == "c" * 40 and found.pr.author == "someone"
    assert (
        found.pr.merged_at == "2026-11-10T00:00:00Z" and found.pr.title == "Later title"
    )
    assert found.pr.body == "Body #3" and found.pr.branch == "topic"
    assert found.pr.closing == (
        wc.IssueRef("IronbellyOrg/IronClaude", 12),
        wc.IssueRef(None, 13),
    )
    argv = runner.commands[0].argv
    assert (
        argv[:3] == ["gh", "pr", "list"] and argv[argv.index("--head") + 1] == "topic"
    )
    assert argv[argv.index("--state") + 1] == "all"
    assert_every_gh_call_names_its_repo(runner)


def test_with_no_merged_pull_request_the_newest_is_returned_and_the_rest_are_edge_cases(
    wc, runner_cls
):
    reply = (0, json.dumps([pr_row(5, "OPEN"), pr_row(8, "CLOSED")]), "")
    runner = runner_cls(replies={"gh": gh_fake(wc, {("pr", "list", SLUG): reply})})
    assert wc.find_pull_request(runner, SLUG, "topic").pr.number == 8
    empty = runner_cls(
        replies={"gh": gh_fake(wc, {("pr", "list", SLUG): (0, "[]", "")})}
    )
    found = wc.find_pull_request(empty, SLUG, "topic")
    assert found.ok and found.pr is None
    assert wc.find_pull_request(empty, SLUG, None).ok  # a detached HEAD asks nothing
    assert len(empty.commands) == 1
    for reply in (
        (1, "", "HTTP 502"),
        (0, "not json", ""),
        (0, '{"a": 1}', ""),
        (0, '[{"state": "OPEN"}]', ""),
    ):
        bad = runner_cls(replies={"gh": gh_fake(wc, {("pr", "list", SLUG): reply})})
        result = wc.find_pull_request(bad, SLUG, "topic")
        assert result.ok is False and result.pr is None and result.reason
    # a branch name shaped like an option is refused by the runner and reported, not run
    refused = runner_cls(replies={"gh": gh_fake(wc, {})})
    assert wc.find_pull_request(refused, SLUG, "--web").ok is False
    assert refused.commands == []


def test_a_squash_merged_pull_request_is_merged_from_its_state_without_ancestry(
    wc, runner_cls
):
    """The pull request commits are not on the base; state alone answers, no git call is made."""
    rows = [pr_row(9, "MERGED", mergedAt="2026-11-10T00:00:00Z", headRefOid="d" * 40)]
    runner = runner_cls(
        replies={"gh": gh_fake(wc, {("pr", "list", SLUG): (0, json.dumps(rows), "")})}
    )
    found = wc.find_pull_request(runner, SLUG, "topic")
    assert found.pr.state == "MERGED"
    assert [c.argv[0] for c in runner.commands] == ["gh"]


def test_commits_after_the_pull_request(wc, runner_cls, throwaway_repo):
    path = throwaway_repo.add_worktree("after")
    first = git_in(path, "rev-parse", "HEAD").strip()
    write(path / "more.txt")
    git_in(path, "add", "more.txt")
    git_in(path, "commit", "-q", "-m", "second")
    write(path / "more2.txt")
    git_in(path, "add", "more2.txt")
    git_in(path, "commit", "-q", "-m", "third")
    head = git_in(path, "rev-parse", "HEAD").strip()
    runner = runner_cls()
    same = wc.commits_after_pr(runner, str(path), head, head)
    assert (same.relation, same.commits_after) == ("same", 0)
    ahead = wc.commits_after_pr(runner, str(path), head, first)
    assert (ahead.relation, ahead.commits_after) == ("ahead", 2)
    behind = wc.commits_after_pr(runner, str(path), first, head)
    assert (behind.relation, behind.commits_after) == ("ancestor", 0)
    missing = wc.commits_after_pr(runner, str(path), head, "e" * 40)
    assert (
        missing.relation == "unknown"
        and missing.commits_after is None
        and missing.reason
    )
    assert wc.commits_after_pr(runner, str(path), None, head).relation == "unknown"
    assert wc.commits_after_pr(runner, str(path), head, "").relation == "unknown"
    verbs = {tuple(c.argv[1:3]) for c in runner.commands}
    assert verbs <= {("merge-base", "--is-ancestor"), ("rev-list", "--count")}


# -- the landed check --------------------------------------------------------------------


def landed_setup(wc, runner_cls, tmp_path, present, answer, gh_table=None):
    places = [
        tmp_path / "home" / "b.sh",
        tmp_path / "checkout" / "b.sh",
        tmp_path / "src" / "b.sh",
    ]
    for index in present:
        write(places[index], "#!/bin/bash\n")

    def bash(argv, cwd):
        code, out = answer
        return wc.Result(code, out, "")

    runner = runner_cls(
        replies={"bash": bash, "gh": gh_fake(wc, gh_table or {})},
        landed_paths=tuple(str(p) for p in places),
    )
    return runner, places


def test_landed_check_runs_the_script_in_the_main_checkout_in_lookup_order(
    wc, runner_cls, tmp_path
):
    main = tmp_path / "main"
    main.mkdir()
    for present, label in (
        ([0, 1, 2], "installed copy"),
        ([1, 2], "checkout copy"),
        ([2], "in-checkout fallback"),
    ):
        runner, places = landed_setup(
            wc, runner_cls, tmp_path, present, (0, "MERGED\n")
        )
        got = wc.landed_check(
            runner, SLUG, 700, str(main), which=lambda name: "/usr/bin/jq"
        )
        assert (got.token, got.via) == ("MERGED", label)
        call = runner.commands[0]
        assert call.argv == [
            "bash",
            str(places[present[0]]),
            "700",
        ] and call.cwd == str(main)
        assert all(c.argv[0] != "gh" for c in runner.commands)
        for place in places:
            if place.exists():
                place.unlink()


@pytest.mark.parametrize("token", ["OPEN", "CLOSED", "NONE", "UNKNOWN"])
def test_landed_tokens_other_than_merged_are_passed_through(
    wc, runner_cls, tmp_path, token
):
    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (4, f"note\n{token}\n"))
    got = wc.landed_check(runner, SLUG, 5, str(tmp_path), which=lambda n: "/usr/bin/jq")
    assert got.token == token


# What the installed script really prints: one line, the token and then key=value fields
# (observed by running it on pull requests 301 and 700 of this repo on 2026-11-20).
REAL_LANDED_LINES = [
    ("MERGED pr=301 by=example-user merge=0123abc base=master head=4567def match=same "
     "url=https://github.com/IronbellyOrg/example/pull/301\n", 0, "MERGED"),
    ("OPEN pr=2 by=example-user base=master head=4567def match=same "
     "url=https://github.com/IronbellyOrg/example/pull/2\n", 1, "OPEN"),
    ("CLOSED pr=3 by=example-user base=master head=4567def match=same "
     "url=https://github.com/IronbellyOrg/example/pull/3\n", 4, "CLOSED"),
    ("NONE pr=4\n", 3, "NONE"),
    ("UNKNOWN reason=usage\n", 5, "UNKNOWN"),
]  # fmt: skip


@pytest.mark.parametrize("line,code,token", REAL_LANDED_LINES)
def test_the_real_one_line_answer_with_key_value_fields_is_read_by_its_first_word(
    wc, runner_cls, tmp_path, line, code, token
):
    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (code, line))
    got = wc.landed_check(
        runner, SLUG, 301, str(tmp_path), which=lambda n: "/usr/bin/jq"
    )
    assert got.token == token and got.via == "installed copy"


@pytest.mark.parametrize(
    "line", ["MERGEDX pr=1\n", "merged pr=1\n", "pr=1 MERGED\n", "\n"]
)
def test_a_line_that_does_not_start_with_a_token_is_no_answer(
    wc, runner_cls, tmp_path, line
):
    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (0, line))
    got = wc.landed_check(
        runner, SLUG, 301, str(tmp_path), which=lambda n: "/usr/bin/jq"
    )
    assert got.token == "UNKNOWN" and "no answer" in got.reason


def test_landed_check_with_no_answer_or_no_jq_is_unknown(wc, runner_cls, tmp_path):
    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (127, ""))
    got = wc.landed_check(runner, SLUG, 5, str(tmp_path), which=lambda n: "/usr/bin/jq")
    assert got.token == "UNKNOWN" and "no answer" in got.reason
    runner, _ = landed_setup(wc, runner_cls, tmp_path, [0], (0, "MERGED\n"))
    got = wc.landed_check(runner, SLUG, 5, str(tmp_path), which=lambda n: None)
    assert got.token == "UNKNOWN" and "jq" in got.reason
    assert runner.commands == []  # the script was not even started


def test_without_the_script_the_gh_pr_view_fallback_answers(wc, runner_cls, tmp_path):
    key = ("pr", "view", "700", SLUG)
    cases = [
        (
            (
                0,
                json.dumps({"state": "MERGED", "mergedAt": "2026-11-10T00:00:00Z"}),
                "",
            ),
            "MERGED",
        ),
        ((0, json.dumps({"state": "OPEN", "mergedAt": None}), ""), "OPEN"),
        ((0, json.dumps({"state": "CLOSED", "mergedAt": None}), ""), "CLOSED"),
        ((0, json.dumps({"state": "MERGED", "mergedAt": None}), ""), "UNKNOWN"),
        ((0, "garbage", ""), "UNKNOWN"),
    ]
    for reply, token in cases:
        runner, _ = landed_setup(wc, runner_cls, tmp_path, [], (0, ""), {key: reply})
        got = wc.landed_check(runner, SLUG, 700, str(tmp_path))
        assert got.token == token and got.via == "gh pr view"
        assert [c.argv[:3] for c in runner.commands] == [["gh", "pr", "view"]]
        assert_every_gh_call_names_its_repo(runner)


def test_when_the_fallback_also_fails_the_landed_check_said_unknown(
    wc, runner_cls, tmp_path
):
    runner, _ = landed_setup(wc, runner_cls, tmp_path, [], (0, ""), {})
    got = wc.landed_check(runner, SLUG, 700, str(tmp_path))
    assert got.token == "UNKNOWN" and got.reason.startswith("landed check said UNKNOWN")


# -- issues for rule 4 -------------------------------------------------------------------------


def make_orca(wc):
    ps = wc.parse_orca_worktrees(fixture_text("orca_worktree_ps.json")).items[0]
    return dataclasses.replace(
        ps,
        comment="sc:issue IronbellyOrg/IronClaude#669 and more",
        linked_issue=(None, 5),
    )


def issue_reply(state):
    return (0, json.dumps({"state": state}), "")


def test_issue_numbers_come_from_every_place_and_pull_request_numbers_are_dropped(
    wc, runner_cls
):
    coder = "IronbellyGroup/Coder"
    pr = wc.PullRequest(
        number=9, state="MERGED", head_oid="a" * 40, author="x", merged_at="2026-11-10T00:00:00Z",
        title="Fix thing (#20)",
        body=f"Fixes #21. Related: {SLUG}#373 and {coder}#373. See also {SLUG}#999.",
        closing=(wc.IssueRef(None, 10),), branch="docs-354-topic",
    )  # fmt: skip
    table = {
        # closing reference: a known issue
        ("issue", "view", "10", SLUG): issue_reply("CLOSED"),
        # #20 and #21 in the title and body: not pull requests, issues
        ("pr", "view", "20", SLUG): NOT_FOUND,
        ("issue", "view", "20", SLUG): issue_reply("CLOSED"),
        ("pr", "view", "21", SLUG): NOT_FOUND,
        ("issue", "view", "21", SLUG): issue_reply("OPEN"),
        # IronClaude 373 is a merged pull request, Coder 373 is an open issue
        ("pr", "view", "373", SLUG): (0, json.dumps({"state": "MERGED"}), ""),
        ("pr", "view", "373", coder): NOT_FOUND,
        ("issue", "view", "373", coder): issue_reply("OPEN"),
        # a number that is no issue anywhere is dropped
        ("pr", "view", "999", SLUG): NOT_FOUND,
        ("issue", "view", "999", SLUG): NOT_FOUND,
        # the branch name number 354, the folder name number 687
        ("pr", "view", "354", SLUG): NOT_FOUND,
        ("issue", "view", "354", SLUG): issue_reply("CLOSED"),
        ("pr", "view", "687", SLUG): NOT_FOUND,
        ("issue", "view", "687", SLUG): issue_reply("CLOSED"),
        # Orca card comment 669, linked issue 5
        ("pr", "view", "669", SLUG): NOT_FOUND,
        ("issue", "view", "669", SLUG): issue_reply("CLOSED"),
        ("issue", "view", "5", SLUG): issue_reply("CLOSED"),
    }
    runner = runner_cls(replies={"gh": gh_fake(wc, table)})
    refs = wc.parse_orca_references(fixture_text("orca_reference_list.json"))
    facts = wc.collect_issues(
        runner, SLUG, pr, "topic-354", "/w/issue-687", make_orca(wc), refs
    )
    got = {(i.repo, i.number): (i.state, i.sources) for i in facts.issues}
    assert facts.failures == ()
    assert set(got) == {
        (SLUG, 10), (SLUG, 20), (SLUG, 21), (coder, 373),
        (SLUG, 354), (SLUG, 687), (SLUG, 669), (SLUG, 5),
    }  # fmt: skip
    assert got[(SLUG, 10)][1] == ("closing reference",)
    assert got[(SLUG, 20)][1] == ("title or body",)
    assert got[(SLUG, 354)][1] == (
        "branch name",
    )  # branch topic-354 and PR branch agree
    assert got[(SLUG, 687)][1] == ("folder name", "Orca reference")
    assert got[(SLUG, 669)][1] == ("Orca card comment",)
    assert got[(SLUG, 5)][1] == ("Orca linked issue",)
    assert (SLUG, 373) not in got  # the pull request number is dropped
    assert [i.number for i in facts.open_issues] == [21, 373]
    assert_every_gh_call_names_its_repo(runner)


def test_a_failed_issue_lookup_is_recorded_and_none_found_passes(wc, runner_cls):
    pr = wc.PullRequest(9, "MERGED", "a" * 40, "x", "d", "t", "see #44", (), "topic")
    flaky = {
        ("pr", "view", "44", SLUG): NOT_FOUND
    }  # the issue view then fails (HTTP 502)
    runner = runner_cls(replies={"gh": gh_fake(wc, flaky)})
    facts = wc.collect_issues(runner, SLUG, pr, "topic", "/w/plain")
    assert facts.failures == (f"issue lookup failed: {SLUG}#44",)
    assert not facts.none_found
    # the pull request check itself fails
    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
    assert wc.collect_issues(runner, SLUG, pr, "topic", "/w/plain").failures
    # a known issue that cannot be found is a failure, not a pass
    pr2 = wc.PullRequest(
        9, "MERGED", "a" * 40, "x", "d", "t", "", (wc.IssueRef(None, 3),), "topic"
    )
    runner = runner_cls(
        replies={"gh": gh_fake(wc, {("issue", "view", "3", SLUG): NOT_FOUND})}
    )
    assert wc.collect_issues(runner, SLUG, pr2, "topic", "/w/plain").failures
    # nothing anywhere: passes with "none found"
    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
    plain = wc.collect_issues(runner, SLUG, None, "topic", "/w/plain")
    assert plain.none_found and plain.open_issues == [] and runner.commands == []


def test_an_unreadable_orca_reference_list_keeps_the_worktree(wc, runner_cls):
    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
    down = wc.parse_orca_references("not json")
    facts = wc.collect_issues(runner, SLUG, None, "topic", "/w/plain", None, down)
    assert not facts.none_found
    assert facts.failures == (f"issue lookup failed: {down.unavailable}",)
    assert runner.commands == []
    # a read that worked and held nothing is still "none found"; so is no read at all
    empty = wc.parse_orca_references('{"ok": true, "result": {"references": []}}')
    assert wc.collect_issues(
        runner, SLUG, None, "topic", "/w/plain", None, empty
    ).none_found
    assert wc.collect_issues(
        runner, SLUG, None, "topic", "/w/plain", None, None
    ).none_found


def test_a_reference_to_a_repo_that_is_not_ours_is_a_failed_lookup_and_never_run(
    wc, runner_cls
):
    pr = wc.PullRequest(
        9,
        "MERGED",
        "a" * 40,
        "x",
        "d",
        "t",
        "SuperClaude-Org/SuperClaude_Framework#5",
        (),
        "topic",
    )
    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
    facts = wc.collect_issues(runner, SLUG, pr, "topic", "/w/plain")
    assert facts.failures and facts.issues == ()
    assert runner.commands == []  # the runner refused it before any process


def test_text_and_name_parsers(wc):
    refs = wc.refs_in_text(
        "Fixes #1, see Org/Repo#22 and (#3). not a#4 and http://h/x#5"
    )
    assert [(r.repo, r.number) for r in refs] == [
        (None, 1),
        ("Org/Repo", 22),
        (None, 3),
    ]
    assert wc.numbers_in_name("docs-354-foo") == [354]
    assert wc.numbers_in_name("419-x-issue-655") == [419, 655]
    assert wc.numbers_in_name("a-1-b-12345-c-99") == [99]
    assert wc.numbers_in_name("") == []
