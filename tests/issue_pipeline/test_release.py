"""The coordinator-side release of a bound worker (Plan B Task 14, design G2 route A)."""

from __future__ import annotations

import stat

import pytest
from click.testing import CliRunner

from superclaude.cli.issue_pipeline import release
from superclaude.cli.issue_pipeline.cli import issue_pipeline_group

SID = "sess-abc_123"


def _store(tmp_path, record: str | None = "worktree"):
    store = tmp_path / "store"
    sessions = store / "sessions"
    sessions.mkdir(parents=True)
    if record is not None:
        (sessions / SID).write_text(record)
    return store


def test_release_creates_one_empty_private_ok_file(tmp_path):
    store = _store(tmp_path)
    assert release.release(SID, store) == "released"
    ok = store / "sessions" / f"{SID}.ok"
    assert ok.read_bytes() == b""
    assert stat.S_IMODE(ok.stat().st_mode) == 0o600


def test_a_second_release_changes_nothing(tmp_path):
    store = _store(tmp_path)
    release.release(SID, store)
    assert release.release(SID, store) == "already-released"


@pytest.mark.parametrize("sid", ["", "../x", "a/b", "-x", "a b", "x" * 129, "ok\n"])
def test_an_id_the_guard_would_not_accept_is_refused(tmp_path, sid):
    with pytest.raises(release.ReleaseError) as err:
        release.release(sid, _store(tmp_path))
    assert err.value.reason == "bad-session-id"


def test_an_unbound_session_is_refused(tmp_path):
    with pytest.raises(release.ReleaseError) as err:
        release.release(SID, _store(tmp_path, record=None))
    assert err.value.reason == "not-bound"


@pytest.mark.parametrize("record", ["full", "full-submit", "degraded", ""])
def test_only_a_worktree_level_session_has_a_release(tmp_path, record):
    store = _store(tmp_path, record)
    with pytest.raises(release.ReleaseError) as err:
        release.release(SID, store)
    assert err.value.reason == "not-worktree-level"
    assert not (store / "sessions" / f"{SID}.ok").exists()


def test_a_missing_store_or_a_linked_record_or_directory_is_refused(tmp_path):
    with pytest.raises(release.ReleaseError) as err:
        release.release(SID, tmp_path / "none")
    assert err.value.reason == "no-store"
    store = _store(tmp_path, record=None)
    real = tmp_path / "real"
    real.write_text("worktree")
    (store / "sessions" / SID).symlink_to(real)
    with pytest.raises(release.ReleaseError) as err:
        release.release(SID, store)
    assert err.value.reason == "not-bound"
    linked = tmp_path / "linked"
    linked.mkdir()
    (linked / "sessions").symlink_to(store / "sessions")
    with pytest.raises(release.ReleaseError) as err:
        release.release(SID, linked)
    assert err.value.reason == "no-store"


def test_the_cli_verb_prints_closed_words_only(tmp_path):
    store = _store(tmp_path)
    run = CliRunner().invoke(
        issue_pipeline_group, ["release-worker", SID, "--store", str(store)]
    )
    assert (run.exit_code, run.output) == (0, "released\n")
    run = CliRunner().invoke(
        issue_pipeline_group, ["release-worker", "../x", "--store", str(store)]
    )
    assert (run.exit_code, run.output) == (1, "refused:bad-session-id\n")
