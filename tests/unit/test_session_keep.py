"""session_keep.py: classify (and, below it, prune) the sessions already saved.

The module is imported by path, as the other ccsession helpers are tested. Every
test builds its own tree in pytest's temporary folder; nothing reads or writes the
real ~/.claude.
"""

from __future__ import annotations

import fcntl
import importlib.util
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

SKILL_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "skills"
    / "ccsession-tag"
)
_spec = importlib.util.spec_from_file_location(
    "session_keep", SKILL_DIR / "session_keep.py"
)
assert _spec and _spec.loader
keep = importlib.util.module_from_spec(_spec)
sys.modules["session_keep"] = keep  # dataclasses looks its module up here
_spec.loader.exec_module(keep)

AUTO = "proj-fix-bug-1118-150248-ab12"  # an exact --auto-name label


def sid(n: int) -> str:
    return f"{n:08x}-0000-0000-0000-000000000000"


def snapshot(root: Path) -> dict[str, tuple]:
    """Every path under root with what a change would show: type, content or
    link target, and a file's modification time."""
    seen: dict[str, tuple] = {}
    if not root.exists():
        return seen
    for path in sorted(root.rglob("*")):
        rel = str(path.relative_to(root))
        if path.is_symlink():
            seen[rel] = ("link", os.readlink(path))
        elif path.is_dir():
            seen[rel] = ("dir",)
        else:
            seen[rel] = ("file", path.read_bytes(), path.stat().st_mtime_ns)
    return seen


def save(projects: Path, key: str, stem: str, session: str) -> Path:
    """A saved name: <projects>/<key>/topics/<stem>.txt holding the session id."""
    topics = projects / key / "topics"
    topics.mkdir(parents=True, exist_ok=True)
    path = topics / f"{stem}.txt"
    path.write_text(session + "\n")
    return path


def mark(projects: Path, key: str, session: str, value: str) -> None:
    folder = projects / key / "topics" / ".origin"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / session).write_text(value + "\n")


def marker_of(projects: Path, key: str, session: str) -> str | None:
    path = projects / key / "topics" / ".origin" / session
    return path.read_text().strip() if path.is_file() else None


@pytest.fixture
def projects(tmp_path: Path) -> Path:
    folder = tmp_path / "home" / ".claude" / "projects"
    folder.mkdir(parents=True)
    return folder


# --- auto_shaped ---------------------------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "proj-1118-150248-ab12",
        "proj-fix-bug-1118-150248-ab12",
        "proj-1118-150248-ab12-2",  # taken once already
        "proj-1118-150248-ab12-99",
        "a/b-1118-150248-ab12",
        "proj-0000-000000-0000",  # the stamp when `date` failed has the same shape
    ],
)
def test_an_exact_auto_name_stamp_is_auto_shaped(name: str) -> None:
    assert keep.auto_shaped(name)


@pytest.mark.parametrize(
    "name",
    [
        "fix-1118-notes",  # digits, no stamp
        "proj-1118-150248-AB12",  # upper-case hex
        "proj-1118-150248-ab1",  # three hex digits
        "proj-1118-150248-ab123",  # five hex digits
        "proj-1118-15024-ab12",  # five time digits
        "proj-11181-150248-ab12",  # five date digits
        "proj-1118-150248-ab12-notes",  # something after the stamp
        "proj-1118-150248-ab12-2-3",  # two suffixes
        "proj-1118-150248-ab12 ",  # a space
        "proj-1118-150248-ab1g",  # not hex
        "1118-150248-ab12",  # no hyphen before the date
        "my work",
        "",
    ],
)
def test_anything_else_is_not_auto_shaped(name: str) -> None:
    assert not keep.auto_shaped(name)


def test_file_names_read_back_as_the_names_ccsession_saved() -> None:
    assert keep.file_to_name("a%2Fb%25c") == "a/b%c"
    assert keep.file_to_name("%2Ehidden") == ".hidden"
    assert keep.file_to_name("plain") == "plain"


# --- the readers ---------------------------------------------------------------


def test_lists_finds_every_topics_folder_and_skips_hidden_and_linked(
    projects: Path, tmp_path: Path
) -> None:
    save(projects, "github.com-Org-Repo", "a", sid(1))
    save(projects, "-home-me-old-folder", "b", sid(2))  # an old per-folder list
    (projects / ".hidden" / "topics").mkdir(parents=True)
    (projects / "no-topics").mkdir()
    elsewhere = tmp_path / "elsewhere" / "topics"
    elsewhere.mkdir(parents=True)
    (projects / "linked").symlink_to(elsewhere.parent)
    found = [p.parent.name for p in keep.lists(projects)]
    assert found == ["-home-me-old-folder", "github.com-Org-Repo"]


def test_names_reads_regular_name_files_with_a_valid_session_id(
    projects: Path, tmp_path: Path
) -> None:
    save(projects, "k", "good", sid(1))
    save(projects, "k", "bad%2Fid", "../escape")  # not an id
    save(projects, "k", "empty", "")
    other = tmp_path / "real.txt"
    other.write_text(sid(3) + "\n")
    (projects / "k" / "topics" / "linked.txt").symlink_to(other)
    (projects / "k" / "topics" / ".hidden.txt").write_text(sid(4) + "\n")
    (projects / "k" / "topics" / "notes.md").write_text(sid(5) + "\n")
    rows = keep.names(projects / "k" / "topics")
    assert [(r.name, r.session) for r in rows] == [("good", sid(1))]


def test_marker_is_human_agent_or_nothing(projects: Path) -> None:
    topics = projects / "k" / "topics"
    mark(projects, "k", sid(1), "agent")
    mark(projects, "k", sid(2), "human")
    mark(projects, "k", sid(3), "robot")
    assert keep.marker(topics, sid(1)) == "agent"
    assert keep.marker(topics, sid(2)) == "human"
    assert keep.marker(topics, sid(3)) == ""
    assert keep.marker(topics, sid(4)) == ""
    assert keep.marker(topics, "../x") == ""


# --- classify ------------------------------------------------------------------


def build_mixed(projects: Path) -> None:
    """Sessions 1 to 9 in the repo's list (and an old per-folder list)."""
    repo, old = "github.com-Org-Repo", "-home-me-old-folder"
    save(projects, repo, AUTO, sid(1))  # auto-named, unmarked
    save(projects, old, AUTO, sid(1))  # the same session in an old list
    save(projects, repo, "release-1118-notes", sid(2))  # a person's name
    save(projects, repo, "other-1118-150248-cd34", sid(3))  # auto-named ...
    mark(projects, repo, sid(3), "agent")  # ... and already marked
    save(projects, repo, "third-1118-150248-ef56", sid(4))  # auto-named ...
    mark(projects, repo, sid(4), "human")  # ... but a person's by marker
    save(projects, repo, "x-1118-150248-0a0a", sid(5))  # auto-named in one list ...
    save(projects, old, "my-own-name", sid(5))  # ... renamed in another
    save(projects, repo, "x-1118-150248-AB12", sid(6))  # upper-case stamp
    save(projects, old, "only-old-1118-150248-1b2c", sid(7))  # only in an old list
    save(projects, repo, "y-1118-150248-9f9f-2", sid(8))  # a suffixed auto-name


def test_a_dry_run_writes_nothing_and_counts(projects: Path) -> None:
    build_mixed(projects)
    home = projects.parent.parent
    before = snapshot(home)
    result = keep.classify(projects)
    assert snapshot(home) == before
    # Sessions 1, 7 and 8 would be marked; 2, 5 and 6 stay unmarked; 3 and 4 have a
    # marker already (agent and human).
    assert (result.auto_shaped, result.left_unmarked, result.already_marked) == (
        3,
        3,
        2,
    )
    assert result.marked == 0
    assert sorted((p.parent.name, n) for p, n, _ in result.would_mark) == [
        ("-home-me-old-folder", "only-old-1118-150248-1b2c"),
        ("-home-me-old-folder", AUTO),
        ("github.com-Org-Repo", AUTO),
        ("github.com-Org-Repo", "y-1118-150248-9f9f-2"),
    ]


def test_apply_marks_only_the_exact_auto_named_sessions_in_every_list(
    projects: Path,
) -> None:
    build_mixed(projects)
    repo, old = "github.com-Org-Repo", "-home-me-old-folder"
    names_before = {
        p.relative_to(projects): p.read_text() for p in projects.glob("*/topics/*.txt")
    }
    result = keep.classify(projects, apply=True)
    assert (result.auto_shaped, result.left_unmarked, result.already_marked) == (
        3,
        3,
        2,
    )
    assert result.marked == 4 and result.skipped == []
    # marked in the list that names them, the old per-folder list included
    assert marker_of(projects, repo, sid(1)) == "agent"
    assert marker_of(projects, old, sid(1)) == "agent"
    assert marker_of(projects, old, sid(7)) == "agent"
    assert marker_of(projects, repo, sid(8)) == "agent"
    # left alone: a person's name, a human marker, a renamed session, an
    # upper-case stamp; an agent marker that already existed stays as it was
    assert marker_of(projects, repo, sid(2)) is None
    assert marker_of(projects, repo, sid(4)) == "human"
    assert marker_of(projects, repo, sid(5)) is None
    assert marker_of(projects, old, sid(5)) is None
    assert marker_of(projects, repo, sid(6)) is None
    assert marker_of(projects, repo, sid(3)) == "agent"
    # no name changed
    assert {
        p.relative_to(projects): p.read_text() for p in projects.glob("*/topics/*.txt")
    } == names_before


def test_running_apply_twice_changes_nothing_the_second_time(projects: Path) -> None:
    build_mixed(projects)
    keep.classify(projects, apply=True)
    home = projects.parent.parent
    before = snapshot(home)
    again = keep.classify(projects, apply=True)
    assert snapshot(home) == before
    assert (again.auto_shaped, again.marked, again.would_mark) == (0, 0, [])
    assert again.already_marked == 5  # sessions 1, 3, 4, 7 and 8
    assert again.left_unmarked == 3  # sessions 2, 5 and 6


def test_a_session_with_a_human_marker_in_any_list_is_never_marked(
    projects: Path,
) -> None:
    save(projects, "a", AUTO, sid(1))
    save(projects, "b", AUTO, sid(1))
    mark(projects, "b", sid(1), "human")
    result = keep.classify(projects, apply=True)
    assert result.left_unmarked == 1 and result.marked == 0
    assert marker_of(projects, "a", sid(1)) is None
    assert marker_of(projects, "b", sid(1)) == "human"


def test_a_marker_that_appears_before_the_write_is_not_replaced(
    projects: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    save(projects, "a", AUTO, sid(1))
    real = keep.locked

    def marked_meanwhile(folder: Path):
        mark(projects, "a", sid(1), "human")  # a person marked it after the scan
        return real(folder)

    monkeypatch.setattr(keep, "locked", marked_meanwhile)
    result = keep.classify(projects, apply=True)
    assert marker_of(projects, "a", sid(1)) == "human"
    assert result.marked == 0


def test_a_list_whose_lock_is_held_is_skipped_and_reported(
    projects: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(keep, "LOCK_WAIT", 0.2)
    save(projects, "busy", AUTO, sid(1))
    save(projects, "free", "z-1118-150248-ab12", sid(2))
    lock = projects / "busy" / "topics" / ".ccsession-lock"
    with open(lock, "a") as held:
        fcntl.flock(held, fcntl.LOCK_EX)
        result = keep.classify(projects, apply=True)
    assert marker_of(projects, "busy", sid(1)) is None
    assert marker_of(projects, "free", sid(2)) == "agent"
    assert result.marked == 1 and len(result.skipped) == 1
    assert "busy" in result.skipped[0]


def test_a_symlinked_marker_folder_is_never_written_through(
    projects: Path, tmp_path: Path
) -> None:
    save(projects, "a", AUTO, sid(1))
    outside = tmp_path / "outside"
    outside.mkdir()
    (projects / "a" / "topics" / ".origin").symlink_to(outside)
    result = keep.classify(projects, apply=True)
    assert list(outside.iterdir()) == []
    assert result.marked == 0 and len(result.skipped) == 1


def test_an_encoded_name_is_decoded_before_it_is_judged(projects: Path) -> None:
    save(projects, "a", "a%2Fb-1118-150248-ab12", sid(1))
    result = keep.classify(projects)
    assert result.auto_shaped == 1
    assert result.would_mark[0][1] == "a/b-1118-150248-ab12"


def test_main_prints_the_counts_and_the_dry_run_line(
    projects: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    build_mixed(projects)
    assert keep.main(["session_keep.py", "classify", str(projects)]) == 0
    out = capsys.readouterr().out
    assert "Would mark agent: 4 session names" in out
    assert "Auto-named sessions: 3." in out and "Already marked: 2." in out
    assert "not an auto-name): 3." in out
    assert "Dry run: nothing was written. Run with --apply to write the markers." in out
    assert keep.main(["session_keep.py", "classify", "--apply", str(projects)]) == 0
    out = capsys.readouterr().out
    assert "Marked agent: 4 session names" in out and "Dry run" not in out


@pytest.mark.parametrize(
    "argv",
    [
        ["session_keep.py"],
        ["session_keep.py", "frobnicate", "/x"],
        ["session_keep.py", "classify"],
        ["session_keep.py", "classify", "--bogus", "/x"],
        ["session_keep.py", "classify", "/x", "/y"],
    ],
)
def test_main_refuses_a_bad_command_line(argv: list[str]) -> None:
    assert keep.main(argv) == 2


# --- prune ---------------------------------------------------------------------
# Every tree is built in tmp_path. The Claude Code limit is read from the user
# settings of that home (365 unless a test says otherwise) and from a managed
# folder that is empty unless a test fills it: this machine's own never counts.

REPO = "github.com-Org-Repo"
NOW = float(int(time.time()))
DAY = 86400


@pytest.fixture(autouse=True)
def _isolated_settings(
    projects: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    managed = tmp_path / "managed"
    managed.mkdir()
    monkeypatch.setenv("CCSESSION_MANAGED_SETTINGS_DIR", str(managed))
    for name in ("CCSESSION_AGENT_KEEP_DAYS", "CLAUDE_SESSION_ID"):
        monkeypatch.delenv(name, raising=False)
    set_limit(projects, 365)


def set_limit(projects: Path, days: int | None) -> None:
    settings = projects.parent / "settings.json"
    if days is None:
        settings.unlink(missing_ok=True)
    else:
        settings.write_text('{"cleanupPeriodDays": %d}' % days)


def make(
    projects: Path,
    n: int,
    name: str,
    *,
    age_days: float = 40,
    origin: str | None = "agent",
    key: str = REPO,
    folder: str = "-work-a",
    tab: str | None = None,
) -> str:
    """A saved session with everything prune looks at: a name, a marker, a
    transcript of that age, its folder, its file history and (optionally) an Orca tab."""
    home = projects.parent.parent
    session = sid(n)
    save(projects, key, name, session)
    if origin:
        mark(projects, key, session, origin)
    store = projects / folder
    store.mkdir(parents=True, exist_ok=True)
    jsonl = store / f"{session}.jsonl"
    jsonl.write_text("x" * 100)
    os.utime(jsonl, (NOW - age_days * DAY,) * 2)
    (store / session).mkdir(exist_ok=True)
    (store / session / "tool.txt").write_text("y" * 50)
    history = home / ".claude" / "file-history" / session
    history.mkdir(parents=True, exist_ok=True)
    (history / "v1").write_text("z" * 20)
    if tab:
        tabs = orca_dir(projects)
        tabs.mkdir(parents=True, exist_ok=True)
        (tabs / tab).write_text(f"{session}\n/work\nterm\n")
    return session


def orca_dir(projects: Path) -> Path:
    return projects.parent.parent / ".local" / "state" / "ccsession" / "orca-tabs"


def panes(projects: Path) -> list[str]:
    """The tab records left (the lock file is not one)."""
    folder = orca_dir(projects)
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if not p.name.startswith("."))


def run(projects: Path, days: int = 30, apply: bool = False, current: str = "", **kw):
    home = projects.parent.parent
    return keep.prune(
        projects, home, days, apply, current, orca_dir(projects), now=NOW, **kw
    )


def test_a_dry_run_writes_nothing_and_lists_each_candidate(
    projects: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make(projects, 1, "auto-one", age_days=40, tab="pane1")
    make(projects, 2, "auto-two", age_days=100)
    make(projects, 3, "recent", age_days=5)
    make(projects, 4, "mine", age_days=100, origin=None)
    home = projects.parent.parent
    before = snapshot(home)
    result = run(projects)
    assert snapshot(home) == before  # not even a lock file or a migration stamp
    assert [c.names[0].name for c in result.candidates] == ["auto-one", "auto-two"]
    assert result.recent == 1 and result.kept == []
    keep.print_prune(result, apply=False)
    out = capsys.readouterr().out.splitlines()
    rows = [line for line in out if line.startswith("  auto-")]
    assert len(rows) == 2
    assert "40 days old" in rows[0] and "100 days old" in rows[1]
    assert "Would delete 2 agent sessions" in "\n".join(out)
    assert out[-1] == "Dry run: nothing was deleted. Run with --apply to delete."


def test_apply_removes_exactly_the_candidates_and_their_parts(projects: Path) -> None:
    gone = make(projects, 1, "agent-old", age_days=40, tab="pane1")
    other_tab = make(projects, 9, "agent-old-2", age_days=60, tab="pane2")
    unmarked = make(projects, 2, "unmarked-old", age_days=400, origin=None)
    human = make(projects, 3, "human-old", age_days=400, origin="human")
    recent = make(projects, 4, "agent-recent", age_days=10)
    result = run(projects, apply=True)
    assert result.deleted == 2
    home = projects.parent.parent
    for session in (gone, other_tab):
        assert not (projects / "-work-a" / f"{session}.jsonl").exists()
        assert not (projects / "-work-a" / session).exists()
        assert not (home / ".claude" / "file-history" / session).exists()
        assert not (projects / REPO / "topics" / ".origin" / session).exists()
    assert sorted(p.name for p in (projects / REPO / "topics").glob("*.txt")) == [
        "agent-recent.txt",
        "human-old.txt",
        "unmarked-old.txt",
    ]
    assert panes(projects) == []  # both tab records went
    for session in (unmarked, human, recent):  # everything of the others stays
        assert (projects / "-work-a" / f"{session}.jsonl").is_file()
        assert (projects / "-work-a" / session / "tool.txt").is_file()
        assert (home / ".claude" / "file-history" / session / "v1").is_file()
    assert (projects / REPO / "topics" / ".origin" / human).is_file()


def test_a_tab_record_of_another_session_stays(projects: Path) -> None:
    make(projects, 1, "agent-old", age_days=40, tab="pane1")
    keep_session = make(projects, 2, "agent-recent", age_days=3, tab="pane2")
    run(projects, apply=True)
    assert panes(projects) == ["pane2"]
    assert (orca_dir(projects) / "pane2").read_text().startswith(keep_session)


def test_a_session_named_in_two_lists_is_kept_unless_every_name_is_agent(
    projects: Path,
) -> None:
    both = make(projects, 1, "agent-everywhere", age_days=60)
    save(projects, "-old-folder", "agent-everywhere", both)  # the old list's copy
    mark(projects, "-old-folder", both, "agent")
    shared = make(projects, 2, "agent-here", age_days=60)
    save(projects, "-old-folder", "my-name-for-it", shared)  # unmarked there
    result = run(projects)
    assert [c.session for c in result.candidates] == [both]
    assert result.kept == ["agent-here: also saved in -old-folder"]
    run(projects, apply=True)
    # the first session is gone from both lists; the shared one keeps everything
    assert not (projects / "-old-folder" / "topics" / "agent-everywhere.txt").exists()
    assert (projects / "-old-folder" / "topics" / "my-name-for-it.txt").is_file()
    assert (projects / REPO / "topics" / "agent-here.txt").is_file()
    assert (projects / "-work-a" / f"{shared}.jsonl").is_file()
    assert (projects / REPO / "topics" / ".origin" / shared).is_file()


def test_a_session_with_a_human_marker_in_another_list_is_kept(projects: Path) -> None:
    session = make(projects, 1, "agent-here", age_days=60)
    save(projects, "-other", "agent-here", session)
    mark(projects, "-other", session, "human")
    assert run(projects).candidates == []
    run(projects, apply=True)
    assert (projects / "-work-a" / f"{session}.jsonl").is_file()


def test_a_recent_copy_in_any_folder_keeps_the_session(projects: Path) -> None:
    session = make(projects, 1, "agent-old", age_days=90)
    copy = projects / "-work-b" / f"{session}.jsonl"  # the same session, another folder
    copy.parent.mkdir()
    copy.write_text("newer")
    os.utime(copy, (NOW - 3 * DAY,) * 2)
    result = run(projects)
    assert result.candidates == [] and result.recent == 1
    run(projects, apply=True)
    assert (projects / "-work-a" / f"{session}.jsonl").is_file() and copy.is_file()


def test_a_marker_and_a_transcript_without_a_name_file_is_not_a_candidate(
    projects: Path,
) -> None:
    session = sid(5)
    store = projects / "-work-a"
    store.mkdir(parents=True)
    (store / f"{session}.jsonl").write_text("x")
    os.utime(store / f"{session}.jsonl", (NOW - 90 * DAY,) * 2)
    mark(projects, REPO, session, "agent")
    save(projects, REPO, "other", sid(6))  # the list exists
    assert run(projects).candidates == []
    run(projects, apply=True)
    assert (store / f"{session}.jsonl").is_file()


def test_a_symlink_or_a_path_outside_the_folder_is_skipped_and_reported(
    projects: Path, tmp_path: Path
) -> None:
    linked = make(projects, 1, "linked-transcript", age_days=60)
    outside = tmp_path / "outside.jsonl"
    outside.write_text("precious")
    transcript = projects / "-work-a" / f"{linked}.jsonl"
    transcript.unlink()
    transcript.symlink_to(outside)
    os.utime(outside, (NOW - 60 * DAY,) * 2)
    os.utime(transcript, (NOW - 60 * DAY,) * 2, follow_symlinks=False)
    folder_link = make(projects, 2, "linked-folder", age_days=60)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "keep.txt").write_text("precious")
    real = projects / "-work-a" / folder_link
    shutil.rmtree(real)
    real.symlink_to(elsewhere)
    result = run(projects)
    assert result.candidates == []
    assert len(result.skipped) == 2
    run(projects, apply=True)
    assert outside.read_text() == "precious" and transcript.is_symlink()
    assert (elsewhere / "keep.txt").read_text() == "precious" and real.is_symlink()
    assert (projects / REPO / "topics" / "linked-transcript.txt").is_file()
    assert (projects / REPO / "topics" / "linked-folder.txt").is_file()


def test_the_running_session_is_skipped(projects: Path) -> None:
    session = make(projects, 1, "agent-running", age_days=90)
    result = run(projects, current=session)
    assert result.candidates == []
    assert result.kept == ["agent-running: this is the running session"]
    run(projects, apply=True, current=session)
    assert (projects / "-work-a" / f"{session}.jsonl").is_file()
    assert (projects / REPO / "topics" / "agent-running.txt").is_file()


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores folder permissions")
def test_a_transcript_that_cannot_be_removed_keeps_its_name_and_marker(
    projects: Path,
) -> None:
    session = make(projects, 1, "agent-stuck", age_days=90, tab="pane1")
    store = projects / "-work-a"
    store.chmod(0o500)  # nothing can be unlinked in it
    try:
        result = run(projects, apply=True)
    finally:
        store.chmod(0o700)
    assert result.deleted == 0 and result.skipped
    assert (store / f"{session}.jsonl").is_file()
    assert (store / session / "tool.txt").is_file()  # its folder stays with it
    assert (projects / REPO / "topics" / "agent-stuck.txt").is_file()
    assert (projects / REPO / "topics" / ".origin" / session).is_file()
    assert (orca_dir(projects) / "pane1").is_file()


def test_a_list_whose_lock_is_held_keeps_its_name_for_the_next_run(
    projects: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(keep, "LOCK_WAIT", 0.2)
    session = make(projects, 1, "agent-busy", age_days=90)
    lock = projects / REPO / "topics" / ".ccsession-lock"
    with open(lock, "a") as held:
        fcntl.flock(held, fcntl.LOCK_EX)
        result = run(projects, apply=True)
    assert not (projects / "-work-a" / f"{session}.jsonl").exists()
    assert (projects / REPO / "topics" / "agent-busy.txt").is_file()
    assert any("busy" in line for line in result.skipped)


@pytest.mark.parametrize("days", [0, 1, 29, -5, True, "29", "abc", 30.0])
def test_prune_itself_refuses_a_value_below_the_floor(
    projects: Path, days: object
) -> None:
    make(projects, 1, "agent-old", age_days=90)
    with pytest.raises(ValueError):
        run(projects, days=days)  # type: ignore[arg-type]
    assert (projects / "-work-a" / f"{sid(1)}.jsonl").is_file()


def test_the_projects_folder_must_be_the_one_of_the_home_given(
    projects: Path, tmp_path: Path
) -> None:
    make(projects, 1, "agent-old", age_days=90)
    with pytest.raises(ValueError):
        keep.prune(projects, tmp_path / "another-home", 30, now=NOW)


@pytest.mark.parametrize(
    ("args", "env", "code"),
    [
        (["--days", "0"], {}, 2),
        (["--days", "abc"], {}, 2),
        (["--days", "29"], {}, 2),
        (["--days", "-3"], {}, 2),
        ([], {"CCSESSION_AGENT_KEEP_DAYS": "abc"}, 2),
        ([], {"CCSESSION_AGENT_KEEP_DAYS": "29"}, 2),
        (["--days", "45"], {"CCSESSION_AGENT_KEEP_DAYS": "29"}, 2),  # the variable too
        (["--days", "30"], {}, 0),
        (["--days=45"], {}, 0),
        ([], {"CCSESSION_AGENT_KEEP_DAYS": "45"}, 0),
        ([], {"CCSESSION_AGENT_KEEP_DAYS": ""}, 0),  # set but empty: not set
    ],
)
def test_main_checks_the_days_and_deletes_nothing_when_they_are_not_valid(
    projects: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    args: list[str],
    env: dict[str, str],
    code: int,
) -> None:
    session = make(projects, 1, "agent-old", age_days=500)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    argv = [
        "session_keep.py",
        "prune",
        "--apply",
        *args,
        str(projects),
        str(projects.parent.parent),
        str(orca_dir(projects)),
    ]
    assert keep.main(argv) == code
    err = capsys.readouterr().err
    survived = (projects / "-work-a" / f"{session}.jsonl").exists()
    if code == 2:
        assert survived and "at least 30" in err and "nothing was deleted" in err
    else:
        assert not survived and err == ""


@pytest.mark.parametrize(
    "argv",
    [
        ["session_keep.py", "prune", "--days"],
        ["session_keep.py", "prune"],
        ["session_keep.py", "prune", "/a", "/b"],
        ["session_keep.py", "prune", "--bogus", "/a", "/b", "/c"],
    ],
)
def test_main_refuses_a_malformed_prune_command_line(argv: list[str]) -> None:
    assert keep.main(argv) == 2


def test_a_claude_code_limit_at_or_below_the_days_means_it_deletes_first(
    projects: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make(projects, 1, "agent-old", age_days=40)
    managed = tmp_path / "managed"
    (managed / "managed-settings.json").write_text('{"cleanupPeriodDays": 30}')
    result = run(projects, days=30, apply=True)
    assert result.claude_deletes_first and result.candidates == []
    assert (projects / "-work-a" / f"{sid(1)}.jsonl").is_file()
    keep.print_prune(result, apply=True)
    out = capsys.readouterr().out
    assert "Claude Code already deletes saved sessions after 30 days here" in out
    assert "LOWERS THE LIMIT" not in out
    # No file sets a limit: Claude Code's own 30 counts, the same way.
    (managed / "managed-settings.json").unlink()
    set_limit(projects, None)
    assert run(projects, days=30).claude_deletes_first


@pytest.mark.parametrize(
    ("user", "managed", "days", "line"),
    [
        (365, None, 30, True),  # the owner's workspace: a user file with 365
        (None, 90, 30, True),  # this machine: a managed 90
        (365, None, 365, False),  # days equal to the limit: nothing lowered
        (365, None, 400, False),  # above the limit
        (60, None, 45, True),
    ],
)
def test_the_limit_line_appears_only_when_the_limit_is_lowered(
    projects: Path,
    tmp_path: Path,
    user: int | None,
    managed: int | None,
    days: int,
    line: bool,
) -> None:
    set_limit(projects, user)
    if managed is not None:
        (tmp_path / "managed" / "managed-settings.json").write_text(
            '{"cleanupPeriodDays": %d}' % managed
        )
    make(projects, 1, "agent-mid", age_days=days + 10)
    make(projects, 2, "agent-ancient", age_days=2000)
    result = run(projects, days=days)
    limit = managed if managed is not None else user
    assert result.limit == limit
    text = result.limit_line()
    if not line:
        assert text == ""
        return
    spared = [c for c in result.candidates if c.last_change > NOW - limit * DAY]
    assert text == (
        "LOWERS THE LIMIT: Claude Code keeps sessions %d days here; this removes "
        "%d agent sessions that are between %d and %d days old (%d bytes)."
        % (limit, len(spared), days, limit, sum(c.size for c in spared))
    )


def test_the_limit_line_is_printed_on_its_own_line_before_the_dry_run_line(
    projects: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make(projects, 1, "agent-mid", age_days=40)
    keep.print_prune(run(projects), apply=False)
    lines = capsys.readouterr().out.splitlines()
    assert lines[-2].startswith("LOWERS THE LIMIT: Claude Code keeps sessions 365")
    assert lines[-1].startswith("Dry run:")


def test_an_invalid_claude_code_limit_counts_as_its_default(
    projects: Path, tmp_path: Path
) -> None:
    for text in ('{"cleanupPeriodDays": "90"}', '{"cleanupPeriodDays": 0}', "[1]", "x"):
        (projects.parent / "settings.json").write_text(text)
        assert keep.claude_limit(projects.parent.parent) == 30, text


def test_stale_names_markers_and_tab_records_go_after_a_two_day_grace(
    projects: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make(projects, 1, "alive", age_days=1, origin=None)  # a conversation exists
    young = save(projects, REPO, "gone-young", sid(21))
    old = save(projects, REPO, "gone-old", sid(22))
    human = save(projects, REPO, "gone-human", sid(23))
    mark(projects, REPO, sid(23), "human")
    marker_only = projects / REPO / "topics" / ".origin" / sid(24)
    marker_only.write_text("agent\n")
    tabs = orca_dir(projects)
    tabs.mkdir(parents=True)
    (tabs / "stale").write_text(f"{sid(25)}\n/w\nt\n")
    (tabs / "fresh").write_text(f"{sid(26)}\n/w\nt\n")
    (tabs / "live").write_text(f"{sid(1)}\n/w\nt\n")
    for path, days in [
        (young, 1),
        (old, 3),
        (human, 3),
        (marker_only, 3),
        (tabs / "stale", 3),
        (tabs / "fresh", 1),
    ]:
        os.utime(path, (NOW - days * DAY,) * 2)
    os.utime(projects / REPO / "topics" / ".origin" / sid(23), (NOW - 3 * DAY,) * 2)
    result = run(projects)
    assert sorted(r.name for r in result.stale_names) == ["gone-human", "gone-old"]
    assert [p.name for p in result.stale_markers] == [sid(24)]
    assert [p.name for p in result.stale_tabs] == ["stale"]
    assert result.candidates == []
    keep.print_prune(result, apply=False)
    assert "Would remove 4 stale entries" in capsys.readouterr().out
    assert young.is_file() and old.is_file()  # a dry run removed nothing
    run(projects, apply=True)
    assert young.is_file() and not old.is_file() and not human.exists()
    assert not marker_only.exists()
    # the stale name took its marker with it
    assert not (projects / REPO / "topics" / ".origin" / sid(23)).exists()
    assert sorted(p.name for p in tabs.iterdir() if not p.name.startswith(".")) == [
        "fresh",
        "live",
    ]
    assert (projects / REPO / "topics" / "alive.txt").is_file()


def test_no_stale_name_is_removed_when_no_conversation_exists_anywhere(
    projects: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = save(projects, REPO, "gone-old", sid(22))
    os.utime(path, (NOW - 10 * DAY,) * 2)
    result = run(projects, apply=True)
    assert result.store_empty and result.stale_names == []
    assert path.is_file()
    keep.print_prune(result, apply=True)
    assert "No saved conversation found anywhere" in capsys.readouterr().out


def test_a_name_that_just_got_its_conversation_back_is_not_removed(
    projects: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    make(projects, 1, "alive", age_days=1, origin=None)
    old = save(projects, REPO, "came-back", sid(22))
    os.utime(old, (NOW - 10 * DAY,) * 2)
    result = run(projects)
    assert [r.name for r in result.stale_names] == ["came-back"]
    store = projects / "-work-a"
    (store / f"{sid(22)}.jsonl").write_text("it was only in use elsewhere")
    keep.apply_plan(result, projects, projects.parent.parent, orca_dir(projects))
    assert old.is_file()


def test_a_dry_run_leaves_no_bytecode_next_to_the_helper(
    projects: Path, tmp_path: Path
) -> None:
    make(projects, 1, "agent-old", age_days=90)
    tool = tmp_path / "tool"
    tool.mkdir()
    for name in ("session_keep.py", "retention.py"):
        shutil.copy(SKILL_DIR / name, tool / name)
    env = {
        k: v for k, v in os.environ.items() if k != "PYTHONDONTWRITEBYTECODE"
    }  # the default behaviour is what must not write
    done = subprocess.run(
        [
            sys.executable,
            str(tool / "session_keep.py"),
            "prune",
            str(projects),
            str(projects.parent.parent),
            str(orca_dir(projects)),
        ],
        env=env,
        text=True,
        capture_output=True,
    )
    assert done.returncode == 0, done.stderr
    assert "Dry run: nothing was deleted" in done.stdout
    assert not (tool / "__pycache__").exists()


# --- the listing hint ------------------------------------------------------------


def test_hint_counts_the_agent_sessions_past_the_days(projects: Path) -> None:
    home = projects.parent.parent
    make(projects, 1, "agent-old", age_days=1000)  # real mtimes: NOW is the start
    make(projects, 2, "agent-new", age_days=0)
    make(projects, 3, "mine", age_days=1000, origin=None)
    line = keep.hint(projects, home, {})
    assert line == (
        "1 agent sessions are older than 30 days: ccsession --prune shows what "
        "would be removed"
    )


def test_hint_uses_30_for_an_invalid_variable_and_never_raises(
    projects: Path,
) -> None:
    home = projects.parent.parent
    make(projects, 1, "agent-old", age_days=1000)
    for bad in ("29", "abc", "0", "-1", ""):
        assert " older than 30 days:" in keep.hint(
            projects, home, {"CCSESSION_AGENT_KEEP_DAYS": bad}
        ), bad
    set_limit(projects, 3650)  # Claude Code keeps sessions longer than 400 days
    assert " older than 400 days:" in keep.hint(
        projects, home, {"CCSESSION_AGENT_KEEP_DAYS": "400"}
    )
    assert keep.hint(projects, home / "elsewhere", {}) == ""  # a bad home: nothing
    assert keep.hint(projects / "missing", home, {}) == ""


def test_hint_is_empty_when_no_session_is_marked_agent(projects: Path) -> None:
    make(projects, 1, "mine", age_days=1000, origin=None)
    make(projects, 2, "human", age_days=1000, origin="human")
    assert keep.hint(projects, projects.parent.parent, {}) == ""


def test_hint_is_empty_when_claude_code_deletes_at_or_before_the_days(
    projects: Path,
) -> None:
    make(projects, 1, "agent-old", age_days=1000)
    set_limit(projects, 30)
    assert keep.hint(projects, projects.parent.parent, {}) == ""


def test_a_session_marked_or_renamed_after_the_plan_is_kept(projects: Path) -> None:
    # The plan is read first and the deleting comes later: whatever a person does in
    # between (mark it, rename it) is looked at again right before each delete.
    marked = make(projects, 1, "agent-marked", age_days=60)
    renamed = make(projects, 2, "agent-renamed", age_days=60)
    untouched = make(projects, 3, "agent-untouched", age_days=60)
    result = run(projects)
    assert len(result.candidates) == 3
    mark(projects, REPO, marked, "human")
    save(projects, "-another-list", "a-name-a-person-gave", renamed)
    keep.apply_plan(result, projects, projects.parent.parent, orca_dir(projects))
    assert result.deleted == 1
    for session in (marked, renamed):
        assert (projects / "-work-a" / f"{session}.jsonl").is_file()
        assert (projects / "-work-a" / session / "tool.txt").is_file()
    assert not (projects / "-work-a" / f"{untouched}.jsonl").exists()
    assert sum("renamed or marked while pruning" in s for s in result.skipped) == 2
    assert (projects / REPO / "topics" / "agent-marked.txt").is_file()
    assert (projects / REPO / "topics" / "agent-renamed.txt").is_file()
