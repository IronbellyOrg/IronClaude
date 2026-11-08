"""Tests for ``cycle``, part A: configuration, approvers file, filesystem check,
exit precedence and the deadline (plan step 6.5).

This part needs no fakes beyond ``tmp_path``, ``monkeypatch`` and ``FakeClock``.
Every test that could touch HOME or XDG_STATE_HOME runs under the autouse
fixture below (decision DF-39), and no case reads the real
``/proc/self/mountinfo`` (DF-52). Expected values are literals.
"""

from __future__ import annotations

import itertools
import json
import os
import sys
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import audit, cycle, github, record
from superclaude.cli.issue_watch.predicates import format_utc

from .conftest import (
    APPROVER_ID,
    CYCLE_NOW,
    FIXED_NOW,
    FOREIGN_ORIGIN_URL,
    ORCA_PATH,
    OWN_ID,
    OWN_LOGIN,
    T_APPROVED,
    T_TRIGGER,
    FailingStore,
    FakeClock,
    FakeLauncher,
    label_event,
    launched_outcome,
    load_fixture,
    make_config,
    make_deps,
    marker_comment,
    spawn_error_outcome,
    unknown_outcome,
)
from .conftest import result as command_result

NOW = datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.utc)
PROJECT = "PVT_test_project_0001"

# The real reader, taken before the autouse fixture below replaces it, so that a
# test can run it against a file of its own (Gate C fix C-13).
_REAL_READ_MOUNTINFO = cycle._read_mountinfo

# One mountinfo line per case; field 5 is the mount point, the type follows " - ".
ROOT_LINE = "20 1 8:1 / / rw,relatime shared:1 - ext4 /dev/sda1 rw"


@pytest.fixture(autouse=True)
def _isolated_environment(tmp_path, monkeypatch):
    """Point HOME at tmp_path, unset XDG_STATE_HOME, and never read real /proc."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: ROOT_LINE + "\n")


def _expect(reason: str, fragment: str, fn, *args):
    """Call ``fn`` and require ``ConfigError(reason)`` whose detail holds ``fragment``."""
    with pytest.raises(cycle.ConfigError) as caught:
        fn(*args)
    assert caught.value.reason == reason
    assert fragment in caught.value.detail
    return caught.value


# ==============================================================================
# load_config
# ==============================================================================


def _write_config(tmp_path: Path, drop=(), **fields) -> Path:
    """A minimal valid config file with ``fields`` replacing or adding keys."""
    body = {
        "schema_version": 1,
        "project_id": PROJECT,
        "worktree": str(tmp_path / "wt"),
        "approvers_file": str(tmp_path / "approvers"),
    }
    body.update(fields)
    for key in drop:
        del body[key]
    path = tmp_path / "issue-watch.json"
    path.write_text(json.dumps(body), encoding="utf-8")
    return path


def test_load_config_minimal_applies_every_default__fr027(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    config = cycle.load_config(_write_config(tmp_path))
    assert config == cycle.Config(
        enabled=False,
        trigger_label="issue-watch:trigger",
        approval_label="issue-watch:approved",
        project_id=PROJECT,
        owner_account_id=None,
        worktree=tmp_path / "wt",
        approvers_file=tmp_path / "approvers",
        state_dir=tmp_path / "xdg" / "superclaude" / "issue-watch",
    )


def test_load_config_fully_populated__fr027(tmp_path):
    path = _write_config(
        tmp_path,
        enabled=True,
        labels={"trigger": "go", "approval": "ok"},
        owner_account_id=42,
        state_dir=str(tmp_path / "state"),
    )
    assert cycle.load_config(path) == cycle.Config(
        enabled=True,
        trigger_label="go",
        approval_label="ok",
        project_id=PROJECT,
        owner_account_id=42,
        worktree=tmp_path / "wt",
        approvers_file=tmp_path / "approvers",
        state_dir=tmp_path / "state",
    )


def test_load_config_accepts_a_path_string_and_a_path_object__fr027(tmp_path):
    path = _write_config(tmp_path, state_dir=str(tmp_path / "s"))
    assert cycle.load_config(str(path)) == cycle.load_config(path)


def test_default_state_dir_without_xdg_uses_home__df13(tmp_path):
    config = cycle.load_config(_write_config(tmp_path))
    assert config.state_dir == (
        tmp_path / "home" / ".local" / "state" / "superclaude" / "issue-watch"
    )


def test_default_state_dir_empty_xdg_falls_back_to_home__df13(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", "")
    config = cycle.load_config(_write_config(tmp_path))
    assert config.state_dir == (
        tmp_path / "home" / ".local" / "state" / "superclaude" / "issue-watch"
    )


def test_default_state_dir_relative_xdg_is_config_invalid__df13(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", "relative/state")
    _expect(
        "config_invalid",
        "XDG_STATE_HOME is relative",
        cycle.load_config,
        _write_config(tmp_path),
    )


def test_explicit_state_dir_ignores_xdg__df13(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    config = cycle.load_config(_write_config(tmp_path, state_dir=str(tmp_path / "own")))
    assert config.state_dir == tmp_path / "own"


def test_load_config_enabled_true_is_kept__fr027(tmp_path):
    assert cycle.load_config(_write_config(tmp_path, enabled=True)).enabled is True
    assert cycle.load_config(_write_config(tmp_path, enabled=False)).enabled is False


def test_load_config_owner_account_id_bounds_accepted__fr027(tmp_path):
    low = cycle.load_config(_write_config(tmp_path, owner_account_id=1))
    high = cycle.load_config(_write_config(tmp_path, owner_account_id=10**20 - 1))
    assert low.owner_account_id == 1
    assert high.owner_account_id == 99999999999999999999


def test_load_config_label_of_50_characters_is_accepted__fr027(tmp_path):
    config = cycle.load_config(
        _write_config(tmp_path, labels={"trigger": "t" * 50, "approval": "a" * 50})
    )
    assert config.trigger_label == "t" * 50
    assert config.approval_label == "a" * 50


def test_load_config_project_id_of_64_characters_is_accepted__fr027(tmp_path):
    pid = "PVT_" + "A" * 64
    assert cycle.load_config(_write_config(tmp_path, project_id=pid)).project_id == pid


INVALID_CONFIGS = [
    pytest.param({}, ("schema_version",), "schema_version", id="schema_missing"),
    pytest.param({"schema_version": True}, (), "schema_version", id="schema_bool_true"),
    pytest.param({"schema_version": 2}, (), "schema_version", id="schema_2"),
    pytest.param({"schema_version": 0}, (), "schema_version", id="schema_0"),
    pytest.param({"schema_version": "1"}, (), "schema_version", id="schema_string"),
    pytest.param({"schema_version": 1.0}, (), "schema_version", id="schema_float"),
    pytest.param({"enabled": "true"}, (), "enabled must be", id="enabled_string"),
    pytest.param({"enabled": 1}, (), "enabled must be", id="enabled_int"),
    pytest.param({"enabled": None}, (), "enabled must be", id="enabled_null"),
    pytest.param({"enable": True}, (), "unknown configuration key: enable", id="typo"),
    pytest.param(
        {"extra": 1, "enable": 2},
        (),
        "unknown configuration key: enable, extra",
        id="two_unknown_sorted",
    ),
    pytest.param({"labels": []}, (), "labels must be an object", id="labels_list"),
    pytest.param(
        {"labels": {"trigger_label": "x"}},
        (),
        "unknown labels key: trigger_label",
        id="unknown_label_key",
    ),
    pytest.param(
        {"labels": {"trigger": "same", "approval": "same"}},
        (),
        "must differ",
        id="labels_equal",
    ),
    pytest.param(
        {"labels": {"trigger": "issue-watch:approved"}},
        (),
        "must differ",
        id="trigger_equals_default_approval",
    ),
    pytest.param(
        {"labels": {"approval": "issue-watch:trigger"}},
        (),
        "must differ",
        id="approval_equals_default_trigger",
    ),
    pytest.param(
        {"labels": {"trigger": "x" * 51}}, (), "1 to 50", id="trigger_51_chars"
    ),
    pytest.param(
        {"labels": {"approval": "x" * 51}}, (), "labels.approval", id="approval_51"
    ),
    pytest.param({"labels": {"trigger": ""}}, (), "1 to 50", id="trigger_empty"),
    pytest.param({"labels": {"trigger": 5}}, (), "labels.trigger", id="trigger_int"),
    pytest.param(
        {"labels": {"trigger": "a\nb"}}, (), "control characters", id="trigger_newline"
    ),
    pytest.param(
        {"labels": {"approval": "a\tb"}}, (), "control characters", id="approval_tab"
    ),
    pytest.param(
        {"labels": {"trigger": "a\x7fb"}}, (), "control characters", id="trigger_del"
    ),
    pytest.param(
        {"labels": {"trigger": "a,b"}}, (), "comma or a quote", id="trigger_comma"
    ),
    pytest.param(
        {"labels": {"approval": 'a"b'}}, (), "comma or a quote", id="approval_quote"
    ),
    pytest.param(
        {"labels": {"trigger": "-flag"}}, (), "start with a dash", id="trigger_dash"
    ),
    pytest.param({}, ("project_id",), "project_id", id="project_missing"),
    pytest.param({"project_id": "PVX_abc"}, (), "project_id", id="project_prefix"),
    pytest.param({"project_id": "PVT_"}, (), "project_id", id="project_empty_tail"),
    pytest.param(
        {"project_id": "PVT_" + "A" * 65}, (), "project_id", id="project_65_tail"
    ),
    pytest.param({"project_id": "PVT_a b"}, (), "project_id", id="project_space"),
    pytest.param({"project_id": "PVT_abc\n"}, (), "project_id", id="project_newline"),
    pytest.param({"project_id": 7}, (), "project_id", id="project_int"),
    pytest.param({"owner_account_id": True}, (), "owner_account_id", id="owner_bool"),
    pytest.param({"owner_account_id": 0}, (), "owner_account_id", id="owner_zero"),
    pytest.param({"owner_account_id": -5}, (), "owner_account_id", id="owner_negative"),
    pytest.param(
        {"owner_account_id": 10**20}, (), "owner_account_id", id="owner_10_pow_20"
    ),
    pytest.param(
        {"owner_account_id": "1001"}, (), "owner_account_id", id="owner_string"
    ),
    pytest.param({"owner_account_id": 1.5}, (), "owner_account_id", id="owner_float"),
    pytest.param({"owner_account_id": None}, (), "owner_account_id", id="owner_null"),
    pytest.param({}, ("worktree",), "worktree must be", id="worktree_missing"),
    pytest.param({"worktree": "wt"}, (), "worktree must be", id="worktree_relative"),
    pytest.param({"worktree": ""}, (), "worktree must be", id="worktree_empty"),
    pytest.param(
        {"worktree": "~/wt"},
        (),
        "worktree must be an absolute path",
        id="worktree_tilde",
    ),
    pytest.param({"worktree": "/a\0b"}, (), "worktree must be", id="worktree_nul"),
    pytest.param({"worktree": 5}, (), "worktree must be", id="worktree_int"),
    pytest.param(
        {}, ("approvers_file",), "approvers_file must be", id="approvers_missing"
    ),
    pytest.param(
        {"approvers_file": "approvers"},
        (),
        "approvers_file must be",
        id="approvers_rel",
    ),
    pytest.param(
        {"approvers_file": "~/approvers"},
        (),
        "approvers_file must be an absolute path",
        id="approvers_tilde",
    ),
    pytest.param(
        {"state_dir": "state"}, (), "state_dir must be an absolute", id="state_relative"
    ),
    pytest.param(
        {"state_dir": "~/.local/state/x"},
        (),
        "state_dir must be an absolute path",
        id="state_tilde",
    ),
    pytest.param({"state_dir": ""}, (), "state_dir must be", id="state_empty"),
    pytest.param({"state_dir": None}, (), "state_dir must be", id="state_null"),
]


@pytest.mark.parametrize(("fields", "drop", "fragment"), INVALID_CONFIGS)
def test_load_config_rejects_invalid_rule__fr027_df13_df20(
    tmp_path, fields, drop, fragment
):
    path = _write_config(tmp_path, drop=drop, **fields)
    _expect("config_invalid", fragment, cycle.load_config, path)


def test_load_config_does_not_expand_tilde_via_home__df13(tmp_path, monkeypatch):
    # HOME has a real directory, yet "~/wt" must still fail the absolute rule.
    (tmp_path / "home" / "wt").mkdir(parents=True)
    path = _write_config(tmp_path, worktree="~/wt")
    _expect(
        "config_invalid", "worktree must be an absolute path", cycle.load_config, path
    )


def test_load_config_missing_file__fr027(tmp_path):
    _expect(
        "config_invalid",
        "missing or is not valid JSON",
        cycle.load_config,
        tmp_path / "absent.json",
    )


def test_load_config_directory_in_place_of_file__fr027(tmp_path):
    _expect(
        "config_invalid", "missing or is not valid JSON", cycle.load_config, tmp_path
    )


@pytest.mark.parametrize("text", ["", "{", "not json", "{'a': 1}", "{} {}"])
def test_load_config_non_json__fr027(tmp_path, text):
    path = tmp_path / "bad.json"
    path.write_text(text, encoding="utf-8")
    _expect("config_invalid", "missing or is not valid JSON", cycle.load_config, path)


def test_load_config_invalid_utf8__fr027(tmp_path):
    path = tmp_path / "bad.json"
    path.write_bytes(b'{"schema_version": 1, "x": "\xff\xfe"}')
    _expect("config_invalid", "missing or is not valid JSON", cycle.load_config, path)


def test_load_config_deeply_nested_json_is_config_invalid__fr027(tmp_path):
    path = tmp_path / "deep.json"
    path.write_text("[" * 100000 + "]" * 100000, encoding="utf-8")
    _expect("config_invalid", "missing or is not valid JSON", cycle.load_config, path)


@pytest.mark.parametrize("text", ["[]", '"text"', "7", "null", "true"])
def test_load_config_top_level_not_an_object__fr027(tmp_path, text):
    path = tmp_path / "bad.json"
    path.write_text(text, encoding="utf-8")
    _expect("config_invalid", "must be a JSON object", cycle.load_config, path)


def test_load_config_error_detail_never_echoes_the_value__fr027(tmp_path):
    secret = "SECRET-PROJECT-VALUE"  # pragma: allowlist secret
    path = _write_config(tmp_path, project_id=secret)
    error = _expect("config_invalid", "project_id", cycle.load_config, path)
    assert secret not in error.detail
    assert secret not in str(error)


# ==============================================================================
# fs_type_of and the network-filesystem check (DF-23, DF-52, DF-53)
# ==============================================================================


def _mnt(mount_point: str, fstype: str, optional: str = "") -> str:
    """A mountinfo line mounting ``fstype`` on ``mount_point``."""
    tail = f" {optional}" if optional else ""
    return f"36 20 0:30 / {mount_point} rw,noatime{tail} - {fstype} src rw"


def test_fs_type_of_decodes_an_escaped_space__df23():
    text = ROOT_LINE + "\n" + _mnt(r"/zz-mnt/my\040share", "nfs4") + "\n"
    assert cycle.fs_type_of("/zz-mnt/my share/state", text) == "nfs4"
    assert cycle.fs_type_of("/zz-mnt/my", text) == "ext4"


def test_fs_type_of_decodes_tab_newline_and_backslash__df23():
    text = "\n".join(
        [
            ROOT_LINE,
            _mnt(r"/zz-mnt/a\011b", "cifs"),
            _mnt(r"/zz-mnt/c\012d", "9p"),
            _mnt(r"/zz-mnt/e\134f", "nfs"),
        ]
    )
    assert cycle.fs_type_of("/zz-mnt/a\tb/x", text) == "cifs"
    assert cycle.fs_type_of("/zz-mnt/c\nd/x", text) == "9p"
    assert cycle.fs_type_of("/zz-mnt/e\\f/x", text) == "nfs"
    # The still-escaped text is not a mount point of that path.
    assert cycle.fs_type_of(r"/zz-mnt/e\134f/x", text) == "ext4"


def test_fs_type_of_longest_mount_point_prefix_wins__df23():
    text = "\n".join(
        [
            ROOT_LINE,
            _mnt("/zz-data", "nfs"),
            _mnt("/zz-data/local", "ext4"),
            _mnt("/zz-data/local/deep", "cifs"),
        ]
    )
    assert cycle.fs_type_of("/zz-data/x", text) == "nfs"
    assert cycle.fs_type_of("/zz-data/local/x", text) == "ext4"
    assert cycle.fs_type_of("/zz-data/local/deep/y", text) == "cifs"
    assert cycle.fs_type_of("/zz-other/y", text) == "ext4"


def test_fs_type_of_longest_wins_regardless_of_line_order__df23():
    text = "\n".join(
        [_mnt("/zz-data/local", "ext4"), _mnt("/zz-data", "nfs"), ROOT_LINE]
    )
    assert cycle.fs_type_of("/zz-data/local/x", text) == "ext4"
    assert cycle.fs_type_of("/zz-data/x", text) == "nfs"


def test_fs_type_of_prefix_must_end_at_a_path_boundary__df23():
    text = ROOT_LINE + "\n" + _mnt("/zz-mnt/state", "nfs")
    assert cycle.fs_type_of("/zz-mnt/state", text) == "nfs"
    assert cycle.fs_type_of("/zz-mnt/state/sub", text) == "nfs"
    assert cycle.fs_type_of("/zz-mnt/stateful/sub", text) == "ext4"
    assert cycle.fs_type_of("/zz-mnt", text) == "ext4"


def test_fs_type_of_later_line_wins_a_tie__df23():
    text = "\n".join([ROOT_LINE, _mnt("/zz-data", "ext4"), _mnt("/zz-data", "nfs4")])
    assert cycle.fs_type_of("/zz-data/x", text) == "nfs4"


def test_fs_type_of_reads_the_type_after_optional_fields__df23():
    text = _mnt("/zz-data", "fuse.sshfs", optional="shared:7 master:3 propagate_from:2")
    assert cycle.fs_type_of("/zz-data/x", text) == "fuse.sshfs"


def test_fs_type_of_no_match_is_none__df23():
    assert cycle.fs_type_of("/zz-other/x", _mnt("/zz-data", "nfs")) is None
    assert cycle.fs_type_of("/zz-other/x", "") is None


def test_fs_type_of_ignores_malformed_lines__df23():
    text = "\n".join(
        [
            "garbage",
            "36 20 0:30 / /zz-data rw",  # no separator
            "36 20 0:30 / /zz-data rw -",  # separator but no type
            "1 2 3",
            _mnt("/zz-data", "nfs"),
        ]
    )
    assert cycle.fs_type_of("/zz-data/x", text) == "nfs"
    only_bad = "36 20 0:30 / /zz-data rw -"
    assert cycle.fs_type_of("/zz-data/x", only_bad) is None


def test_fs_type_of_follows_symlinks_in_the_path__df23(tmp_path):
    real = tmp_path.resolve() / "real"
    real.mkdir()
    (tmp_path / "link").symlink_to(real)
    text = ROOT_LINE + "\n" + _mnt(str(real), "nfs")
    assert cycle.fs_type_of(tmp_path / "link" / "sub", text) == "nfs"
    assert cycle.fs_type_of(real / "sub", text) == "nfs"


def test_network_fs_deny_set_is_the_design_list__df23():
    assert cycle.NETWORK_FS_TYPES == frozenset(
        {"nfs", "nfs4", "cifs", "smb3", "sshfs", "fuse.sshfs", "9p"}
    )


def _mounted_state_config(tmp_path, monkeypatch, fstype: str) -> Path:
    text = ROOT_LINE + "\n" + _mnt("/zz-mnt/state", fstype) + "\n"
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: text)
    return _write_config(tmp_path, state_dir="/zz-mnt/state/issue-watch")


@pytest.mark.parametrize(
    "fstype", ["nfs", "nfs4", "cifs", "smb3", "sshfs", "fuse.sshfs", "9p"]
)
def test_load_config_refuses_each_deny_listed_filesystem__df23_df53(
    tmp_path, monkeypatch, fstype
):
    path = _mounted_state_config(tmp_path, monkeypatch, fstype)
    _expect("config_invalid", "network filesystem", cycle.load_config, path)


@pytest.mark.parametrize(
    "fstype", ["tmpfs", "ext4", "xfs", "btrfs", "overlay", "fuse", "fuse.gocryptfs"]
)
def test_load_config_allows_other_filesystems__df23_df53(tmp_path, monkeypatch, fstype):
    path = _mounted_state_config(tmp_path, monkeypatch, fstype)
    assert cycle.load_config(path).state_dir == Path("/zz-mnt/state/issue-watch")


def test_load_config_refuses_a_default_state_dir_on_a_network_fs__df53(
    tmp_path, monkeypatch
):
    text = ROOT_LINE + "\n" + _mnt("/zz-mnt/state", "nfs4") + "\n"
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: text)
    monkeypatch.setenv("XDG_STATE_HOME", "/zz-mnt/state")
    _expect(
        "config_invalid",
        "network filesystem",
        cycle.load_config,
        _write_config(tmp_path),
    )


def test_load_config_skips_the_check_when_mountinfo_is_unreadable__df52(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: None)
    path = _write_config(tmp_path, state_dir="/zz-mnt/state/issue-watch")
    assert cycle.load_config(path).state_dir == Path("/zz-mnt/state/issue-watch")


def test_load_config_uses_the_monkeypatched_reader_not_proc__df52(
    tmp_path, monkeypatch
):
    calls: list[int] = []

    def reader():
        calls.append(1)
        return ROOT_LINE

    monkeypatch.setattr(cycle, "_read_mountinfo", reader)
    cycle.load_config(_write_config(tmp_path))
    assert calls == [1]


def test_load_config_checks_nothing_after_a_field_error__df52(tmp_path, monkeypatch):
    calls: list[int] = []
    monkeypatch.setattr(cycle, "_read_mountinfo", lambda: calls.append(1))
    path = _write_config(tmp_path, project_id="bad")
    _expect("config_invalid", "project_id", cycle.load_config, path)
    assert calls == []


# ==============================================================================
# check_platform
# ==============================================================================


def test_check_platform_linux_passes__fr027(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    assert cycle.check_platform() is None


@pytest.mark.parametrize("name", ["darwin", "win32", "freebsd14", "cygwin", "linux2x"])
def test_check_platform_other_systems_are_refused__fr027(monkeypatch, name):
    monkeypatch.setattr(sys, "platform", name)
    error = _expect("platform_unsupported", "Linux only", cycle.check_platform)
    assert cycle.exit_for(error.reason) == 2


# ==============================================================================
# validate_approvers
# ==============================================================================


def _approvers(tmp_path: Path, content, mode: int = 0o600, name: str = "ap") -> Path:
    path = tmp_path / name
    path.write_bytes(content if isinstance(content, bytes) else content.encode())
    path.chmod(mode)
    return path


def test_validate_approvers_reads_ids__fr027(tmp_path):
    path = _approvers(tmp_path, "1001\n2002\n3003\n")
    assert cycle.validate_approvers(path) == frozenset({1001, 2002, 3003})


def test_validate_approvers_returns_a_frozenset__fr027(tmp_path):
    result = cycle.validate_approvers(_approvers(tmp_path, "1\n"))
    assert type(result) is frozenset
    assert result == frozenset({1})


def test_validate_approvers_accepts_a_str_path_and_no_final_newline__fr027(tmp_path):
    path = _approvers(tmp_path, "7\n8")
    assert cycle.validate_approvers(str(path)) == frozenset({7, 8})


def test_validate_approvers_ignores_comments_and_blank_lines__fr027(tmp_path):
    path = _approvers(tmp_path, "# header\n\n1001\n   \n#2002\n\n3003\n# trailing\n")
    assert cycle.validate_approvers(path) == frozenset({1001, 3003})


def test_validate_approvers_collapses_duplicates__fr027(tmp_path):
    path = _approvers(tmp_path, "5\n5\n6\n5\n")
    assert cycle.validate_approvers(path) == frozenset({5, 6})


def test_validate_approvers_accepts_a_20_digit_id__fr027(tmp_path):
    path = _approvers(tmp_path, "12345678901234567890\n")
    assert cycle.validate_approvers(path) == frozenset({12345678901234567890})


def test_validate_approvers_rejects_a_21_digit_id__fr027(tmp_path):
    path = _approvers(tmp_path, "123456789012345678901\n")
    _expect("approvers_invalid", "not an account id", cycle.validate_approvers, path)


@pytest.mark.parametrize(
    "line",
    [
        "0",
        "0123",
        "00",
        "-5",
        "+5",
        "1e3",
        "0x10",
        "octocat",
        "owner-login",
        "12 34",
        "1001 ",
        " 1001",
        "1001\r",
        "１２３",  # full-width digits
        "1_000",
    ],
)
def test_validate_approvers_rejects_a_bad_line__fr027(tmp_path, line):
    path = _approvers(tmp_path, f"1001\n{line}\n")
    _expect("approvers_invalid", "not an account id", cycle.validate_approvers, path)


def test_validate_approvers_one_bad_line_voids_the_whole_file__fr027(tmp_path):
    path = _approvers(tmp_path, "1001\n2002\noctocat\n3003\n")
    _expect("approvers_invalid", "not an account id", cycle.validate_approvers, path)


@pytest.mark.parametrize("content", ["", "\n", "\n\n   \n", "# only a comment\n"])
def test_validate_approvers_empty_after_filtering__fr027(tmp_path, content):
    path = _approvers(tmp_path, content)
    _expect("approvers_invalid", "no account id", cycle.validate_approvers, path)


@pytest.mark.parametrize("mode", [0o664, 0o620, 0o602, 0o666, 0o777, 0o660, 0o606])
def test_validate_approvers_group_or_other_writable__fr027(tmp_path, mode):
    path = _approvers(tmp_path, "1001\n", mode=mode)
    _expect("approvers_invalid", "writable", cycle.validate_approvers, path)


@pytest.mark.parametrize("mode", [0o600, 0o400, 0o640, 0o644, 0o444, 0o604])
def test_validate_approvers_readable_modes_are_accepted__fr027(tmp_path, mode):
    path = _approvers(tmp_path, "1001\n", mode=mode)
    assert cycle.validate_approvers(path) == frozenset({1001})


def test_validate_approvers_owned_by_another_user__fr027(tmp_path, monkeypatch):
    path = _approvers(tmp_path, "1001\n", mode=0o644)
    real_euid = os.geteuid()
    monkeypatch.setattr(os, "geteuid", lambda: real_euid + 1)
    _expect("approvers_invalid", "not owned", cycle.validate_approvers, path)


def test_validate_approvers_owner_matches_the_effective_uid__fr027(
    tmp_path, monkeypatch
):
    path = _approvers(tmp_path, "1001\n")
    owner = os.lstat(path).st_uid
    monkeypatch.setattr(os, "geteuid", lambda: owner)
    assert cycle.validate_approvers(path) == frozenset({1001})


def test_validate_approvers_missing_file__fr027(tmp_path):
    _expect(
        "approvers_invalid",
        "missing or unreadable",
        cycle.validate_approvers,
        tmp_path / "absent",
    )


def test_validate_approvers_symlink_is_refused__fr027(tmp_path):
    real = _approvers(tmp_path, "1001\n", name="real")
    link = tmp_path / "link"
    link.symlink_to(real)
    _expect("approvers_invalid", "not a regular file", cycle.validate_approvers, link)


def test_validate_approvers_directory_is_refused__fr027(tmp_path):
    _expect(
        "approvers_invalid", "not a regular file", cycle.validate_approvers, tmp_path
    )


def test_validate_approvers_invalid_utf8__fr027(tmp_path):
    path = _approvers(tmp_path, b"1001\n\xff\xfe\n")
    _expect("approvers_invalid", "UTF-8", cycle.validate_approvers, path)


def test_validate_approvers_exactly_one_mib_is_accepted__fr027(tmp_path):
    content = b"1\n" * (512 * 1024)
    assert len(content) == 1024 * 1024
    path = _approvers(tmp_path, content)
    assert cycle.validate_approvers(path) == frozenset({1})


def test_validate_approvers_one_byte_over_a_mib_is_refused__fr027(tmp_path):
    content = b"1\n" * (512 * 1024) + b"\n"
    assert len(content) == 1024 * 1024 + 1
    path = _approvers(tmp_path, content)
    _expect("approvers_invalid", "too large", cycle.validate_approvers, path)


@pytest.mark.skipif(os.geteuid() == 0, reason="root reads an unreadable file")
def test_validate_approvers_unreadable_file__fr027(tmp_path):
    path = _approvers(tmp_path, "1001\n", mode=0o200)
    _expect("approvers_invalid", "cannot be read", cycle.validate_approvers, path)


def test_validate_approvers_error_detail_never_echoes_the_content__fr027(tmp_path):
    path = _approvers(tmp_path, "SECRET-LOGIN\n")
    error = _expect(
        "approvers_invalid", "not an account id", cycle.validate_approvers, path
    )
    assert "SECRET-LOGIN" not in error.detail
    assert "SECRET-LOGIN" not in str(error)


def test_approvers_summary_gives_mtime_and_count__fr027(tmp_path):
    path = _approvers(tmp_path, "1001\n2002\n2002\n")
    stamp = datetime(2026, 5, 6, 7, 8, 9, tzinfo=timezone.utc).timestamp()
    os.utime(path, (stamp, stamp))
    assert cycle.approvers_summary(path) == ("2026-05-06T07:08:09Z", 2)


# ==============================================================================
# validate_setup
# ==============================================================================


def test_validate_setup_returns_the_approver_ids__fr027(tmp_path):
    config = make_config(tmp_path)
    assert cycle.validate_setup(config) == frozenset({1001})


def test_validate_setup_missing_worktree__fr027(tmp_path):
    config = make_config(tmp_path, worktree=tmp_path / "no-such-dir")
    _expect(
        "worktree_invalid", "not an existing directory", cycle.validate_setup, config
    )


def test_validate_setup_worktree_is_a_file__fr027(tmp_path):
    plain = tmp_path / "a-file"
    plain.write_text("x", encoding="utf-8")
    config = make_config(tmp_path, worktree=plain)
    _expect(
        "worktree_invalid", "not an existing directory", cycle.validate_setup, config
    )


def test_validate_setup_checks_the_worktree_before_the_approvers__fr027(tmp_path):
    config = make_config(
        tmp_path,
        worktree=tmp_path / "no-such-dir",
        approvers_file=tmp_path / "no-such-approvers",
    )
    _expect("worktree_invalid", "worktree", cycle.validate_setup, config)


def test_validate_setup_bad_approvers_with_a_good_worktree__fr027(tmp_path):
    bad = _approvers(tmp_path, "octocat\n", name="bad")
    config = make_config(tmp_path, approvers_file=bad)
    _expect("approvers_invalid", "not an account id", cycle.validate_setup, config)


def test_validate_setup_reasons_exit_2__fr027():
    assert cycle.exit_for("worktree_invalid") == 2
    assert cycle.exit_for("approvers_invalid") == 2
    assert cycle.exit_for("config_invalid") == 2
    assert cycle.exit_for("platform_unsupported") == 2


# ==============================================================================
# resolve_exit and exit_for (design 4.3, OD-10, DF-41)
# ==============================================================================

PRECEDENCE = [2, 6, 7, 5, 3, 4]
EVERY_CODE = [2, 3, 4, 5, 6, 7, 75]


def test_resolve_exit_empty_set_is_0__fr028():
    assert cycle.resolve_exit(frozenset()) == 0


def test_resolve_exit_only_zero_is_0__fr028():
    assert cycle.resolve_exit(frozenset({0})) == 0


@pytest.mark.parametrize("code", PRECEDENCE + [75])
def test_resolve_exit_a_single_condition_is_itself__fr028(code):
    assert cycle.resolve_exit(frozenset({code})) == code


@pytest.mark.parametrize(
    ("higher", "lower"), list(itertools.combinations(PRECEDENCE, 2))
)
def test_resolve_exit_precedence_over_every_pair__fr028(higher, lower):
    """AC-15, FR-022, NFR-007, FR-028: the exit precedence is 2, 6, 7, 5, 3, 4."""
    assert cycle.resolve_exit(frozenset({higher, lower})) == higher
    assert cycle.resolve_exit(frozenset({lower, higher})) == higher


@pytest.mark.parametrize("code", PRECEDENCE)
def test_resolve_exit_75_loses_to_every_other_code__fr028(code):
    assert cycle.resolve_exit(frozenset({75, code})) == code


def test_resolve_exit_75_with_zero_is_75__fr028():
    assert cycle.resolve_exit(frozenset({75, 0})) == 75


def test_resolve_exit_seven_with_five_is_seven__fr028():
    assert cycle.resolve_exit(frozenset({7, 5})) == 7


def test_resolve_exit_seven_with_three_is_seven__fr028():
    assert cycle.resolve_exit(frozenset({7, 3})) == 7


def test_resolve_exit_two_beats_everything__fr028():
    assert cycle.resolve_exit(frozenset({2, 6, 7, 5, 3, 4, 75})) == 2


def test_resolve_exit_six_beats_seven_five_three_four__fr028():
    assert cycle.resolve_exit(frozenset({6, 7, 5, 3, 4, 75})) == 6


def test_resolve_exit_five_beats_three_and_four__fr028():
    assert cycle.resolve_exit(frozenset({5, 3, 4})) == 5
    assert cycle.resolve_exit(frozenset({3, 4})) == 3


def test_resolve_exit_every_subset_follows_the_precedence_list__fr028():
    """AC-15, FR-022, NFR-007, FR-028: every set of codes resolves by the list."""
    for size in range(len(EVERY_CODE) + 1):
        for subset in itertools.combinations(EVERY_CODE, size):
            present = set(subset)
            expected = next((c for c in PRECEDENCE if c in present), None)
            if expected is None:
                expected = 75 if present == {75} else 0
            assert cycle.resolve_exit(frozenset(subset)) == expected, subset


@pytest.mark.parametrize(
    ("reason", "code"),
    [
        ("not_enabled", 0),
        ("disabled", 0),
        ("disabled_mid_cycle", 0),
        ("cycle_complete", 0),
        ("cycle_crashed", 1),
        ("config_invalid", 2),
        ("origin_mismatch", 2),
        ("orca_not_found", 2),
        ("account_id_mismatch", 2),
        ("login_invalid", 3),
        ("gh_auth_failed", 3),
        ("gh_timeout", 3),
        ("gh_non_json", 3),
        ("project_read_failed", 3),
        ("truncated", 4),
        ("discovery_duplicate", 4),
        ("rate_limited", 5),
        ("rate_limit_clamped", 5),
        ("store_invalid", 6),
        ("store_missing", 6),
        ("lock_missing", 6),
        ("lock_invalid", 6),
        ("state_dir_unwritable", 6),
        ("prompt_invalid", 7),
        ("revalidation_transient", 7),
        ("launch_unknown", 7),
        ("spawn_error", 7),
        ("lock_held", 75),
        ("not_approved", 0),
        ("claimed", 0),
        ("budget_exhausted", 0),
    ],
)
def test_exit_for_reads_the_reason_table__df41(reason, code):
    assert cycle.exit_for(reason) == code


def test_exit_for_unknown_reason_raises__df41():
    with pytest.raises(KeyError):
        cycle.exit_for("no_such_reason")


# ==============================================================================
# Deadline (design 8.5, FR-029)
# ==============================================================================


def _deadline(mono: float = 1000.0, **kwargs) -> tuple[FakeClock, cycle.Deadline]:
    clock = FakeClock(NOW, mono=mono)
    return clock, cycle.Deadline(clock, **kwargs)


def test_deadline_constants_are_the_design_values__fr029():
    assert cycle.DEADLINE_TOTAL_S == 240.0
    assert cycle.GH_FLOOR_S == 5.0
    assert cycle.LAUNCH_CUTOFF_S == 120.0


def test_deadline_starts_with_the_full_budget__fr029():
    _, deadline = _deadline()
    assert deadline.elapsed() == 0.0
    assert deadline.remaining() == 240.0


def test_deadline_measures_from_construction_not_from_zero__fr029():
    clock = FakeClock(NOW, mono=5000.0)
    clock.advance(1000)
    deadline = cycle.Deadline(clock)
    assert deadline.elapsed() == 0.0
    assert deadline.remaining() == 240.0
    clock.advance(30)
    assert deadline.elapsed() == 30.0
    assert deadline.remaining() == 210.0


def test_deadline_timeout_for_returns_the_configured_value_when_time_is_ample__fr029():
    _, deadline = _deadline()
    timeout = deadline.timeout_for(20)
    assert timeout == 20.0
    assert isinstance(timeout, float)


def test_deadline_timeout_for_never_exceeds_the_time_left__fr029():
    clock, deadline = _deadline()
    assert deadline.timeout_for(300) == 240.0
    clock.advance(235)
    assert deadline.timeout_for(300) == 5.0
    assert deadline.timeout_for(20) == 5.0


def test_deadline_timeout_for_is_the_lesser_of_configured_and_left__fr029():
    clock, deadline = _deadline()
    clock.advance(225)
    assert deadline.remaining() == 15.0
    assert deadline.timeout_for(20) == 15.0
    assert deadline.timeout_for(10) == 10.0
    assert deadline.timeout_for(15) == 15.0


def test_deadline_timeout_for_is_none_below_5_seconds_left__fr029():
    clock, deadline = _deadline()
    clock.advance(235.5)
    assert deadline.remaining() == 4.5
    assert deadline.timeout_for(20) is None
    assert deadline.timeout_for(1) is None


def test_deadline_timeout_for_at_exactly_5_seconds_left_still_runs__fr029():
    clock, deadline = _deadline()
    clock.advance(235)
    assert deadline.remaining() == 5.0
    assert deadline.timeout_for(20) == 5.0


def test_deadline_timeout_for_just_past_the_floor_is_none__fr029():
    clock, deadline = _deadline()
    clock.advance(235.001)
    assert deadline.timeout_for(20) is None


def test_deadline_remaining_is_clamped_at_zero__fr029():
    clock, deadline = _deadline()
    clock.advance(240)
    assert deadline.remaining() == 0.0
    clock.advance(500)
    assert deadline.remaining() == 0.0
    assert deadline.elapsed() == 740.0
    assert deadline.timeout_for(20) is None


def test_deadline_custom_total__fr029():
    clock, deadline = _deadline(total=10)
    assert deadline.remaining() == 10.0
    assert deadline.timeout_for(20) == 10.0
    clock.advance(5.5)
    assert deadline.timeout_for(20) is None


def test_deadline_total_below_the_floor_never_starts_a_call__fr029():
    _, deadline = _deadline(total=3)
    assert deadline.remaining() == 3.0
    assert deadline.timeout_for(20) is None


def test_deadline_launch_allowed_through_120_seconds__fr029():
    clock, deadline = _deadline()
    assert deadline.launch_allowed() is True
    clock.advance(119.9)
    assert deadline.launch_allowed() is True
    clock.advance(0.1)
    assert deadline.elapsed() == pytest.approx(120.0)
    assert deadline.launch_allowed() is True


def test_deadline_launch_allowed_is_false_after_120_seconds__fr029():
    clock, deadline = _deadline()
    clock.advance(120)
    assert deadline.launch_allowed() is True
    clock.advance(0.5)
    assert deadline.launch_allowed() is False
    clock.advance(200)
    assert deadline.launch_allowed() is False


def test_deadline_launch_cutoff_is_independent_of_the_total__fr029():
    clock, deadline = _deadline(total=1000)
    clock.advance(121)
    assert deadline.launch_allowed() is False
    assert deadline.timeout_for(20) == 20.0


# ==============================================================================
# Part B: shared inputs, rate limits, deadline and audit exits (plan step 6.6)
#
# Every test runs ``cycle.run_cycle`` over a ``GhWorld`` and a ``FakeClock``: no
# real clock, no sleep, no real gh, git or Orca. Audit lines are read back from
# ``audit.jsonl`` with ``json.loads``.
# ==============================================================================

_USER_ARGV = tuple(github.argv_user())
# One byte over the rotation size; only the file size matters to the rotation.
_PADDING = b"{}\n" * (audit.ROTATE_BYTES // 3 + 1)
_OTHER_OWNER = [
    OWN_LOGIN,
    "other-user",
]  # an assignee set that is not exactly {own login}


def _discover_argv(world, login=OWN_LOGIN):
    return tuple(github.argv_discover(world.config.trigger_label, login))


def _audit_lines(tmp_state) -> list[dict]:
    path = tmp_state.state_dir / "audit.jsonl"
    if not path.exists():
        return []
    return [json.loads(text) for text in path.read_text(encoding="utf-8").splitlines()]


def _of_kind(lines, kind) -> list[dict]:
    return [ln for ln in lines if ln["kind"] == kind]


def _the_cycle_line(lines) -> dict:
    found = _of_kind(lines, "cycle")
    assert len(found) == 1
    return found[0]


def _snapshot(tmp_state) -> dict[str, bytes]:
    """Every regular file of the state directory except the audit log."""
    return {
        p.name: p.read_bytes()
        for p in tmp_state.state_dir.iterdir()
        if p.is_file() and p.name != "audit.jsonl"
    }


def _run(tmp_path, tmp_state, world, *, dry_run=False, launcher=None):
    deps = world.deps(tmp_path, tmp_state, launcher=launcher)
    return cycle.run_cycle(deps, dry_run), deps


def _probed(world) -> bool:
    return any("skills" in argv for argv, _ in world.runner.calls)


# -- scenarios: shared by the table-driven tests and the DF-41 kind check ----


def _scenario(
    build=None, *, config=None, launcher=None, hold_lock=False, **world_kwargs
):
    """Return ``run(tmp_path, tmp_state, gh_world) -> (result, deps, world)``."""

    def run(tmp_path, tmp_state, gh_world):
        cfg = None if config is None else config(tmp_path)
        world = gh_world(config=cfg, **world_kwargs)
        if build is not None:
            build(world, tmp_state)
        deps = world.deps(
            tmp_path, tmp_state, launcher=None if launcher is None else launcher()
        )
        if hold_lock:
            with tmp_state.lock():
                res = cycle.run_cycle(deps, False)
        else:
            res = cycle.run_cycle(deps, False)
        return res, deps, world

    return run


def _c_not_enabled(p):
    return make_config(p, enabled=False)


def _c_no_worktree(p):
    return make_config(p, worktree=p / "missing")


def _c_empty_approvers(p):
    empty = p / "empty-approvers"
    empty.write_text("", encoding="utf-8")
    empty.chmod(0o600)
    return make_config(p, approvers_file=empty)


def _c_other_owner(p):
    return make_config(p, owner_account_id=OWN_ID + 1)


def _b_disabled(world, state):
    (state.state_dir / "DISABLED").write_text("", encoding="utf-8")


def _b_store_garbage(world, state):
    (state.state_dir / "dispatch.json").write_bytes(b"{not json")


def _b_store_missing(world, state):
    (state.state_dir / "dispatch.json").unlink()


def _b_foreign_origin(world, state):
    world.fail("origin", "foreign_origin")


def _b_login_failed(world, state):
    world.fail("user", "failed")


def _b_login_timeout(world, state):
    world.fail("user", "timeout")


def _b_discovery_timeout(world, state):
    world.fail("discover", "timeout")


def _b_discovery_non_json(world, state):
    world.fail("discover", "non_json")


def _b_scope_missing(world, state):
    world.issue(9)
    world.fail("items", "scope", n=9)


def _b_rate_on_login(world, state):
    world.fail("user", "rate")


def _b_rate_on_discovery(world, state):
    world.fail("discover", "rate")


def _b_rate_on_issue(world, state):
    world.issue(8, assignees=_OTHER_OWNER)
    world.issue(9)
    world.fail("events", "rate", n=9)


def _b_many(count):
    def build(world, state):
        world.issues_from(range(1, count + 1), assignees=_OTHER_OWNER)

    return build


def _b_duplicate(world, state):
    world.issue(9, listed=2)


def _b_one_eligible(world, state):
    world.issue(11)


def _b_mixed(world, state):
    only_trigger = [
        label_event(
            1,
            "labeled",
            world.config.trigger_label,
            T_TRIGGER,
            actor_id=2001,
            actor_login="issue-author",
        )
    ]
    world.issue(11, assignees=_OTHER_OWNER)
    world.issue(12, events=only_trigger)
    world.issue(13)


def _b_skew(seconds):
    def build(world, state):
        world.skew_s = seconds

    return build


def _b_budget_gone_after_discovery(world, state):
    world.issue(9)
    world.on("discover", lambda: world.clock.advance(236))


SCENARIOS = {
    "idle": _scenario(),
    "lock_held": _scenario(hold_lock=True),
    "disabled": _scenario(_b_disabled),
    "not_enabled": _scenario(config=_c_not_enabled),
    "worktree_invalid": _scenario(config=_c_no_worktree),
    "approvers_invalid": _scenario(config=_c_empty_approvers),
    "account_id_mismatch": _scenario(config=_c_other_owner),
    "login_invalid": _scenario(login="bad_login!"),
    "origin_mismatch": _scenario(_b_foreign_origin),
    "store_invalid": _scenario(_b_store_garbage),
    "store_missing": _scenario(_b_store_missing),
    "login_failed": _scenario(_b_login_failed),
    "login_timeout": _scenario(_b_login_timeout),
    "discovery_timeout": _scenario(_b_discovery_timeout),
    "discovery_non_json": _scenario(_b_discovery_non_json),
    "project_scope_missing": _scenario(_b_scope_missing),
    "rate_limit_on_login": _scenario(_b_rate_on_login),
    "rate_limit_on_discovery": _scenario(_b_rate_on_discovery),
    "rate_limit_on_issue": _scenario(_b_rate_on_issue),
    "truncated_100": _scenario(_b_many(100)),
    "truncated_101": _scenario(_b_many(101)),
    "discovery_duplicate": _scenario(_b_duplicate),
    "discovery_count_warning": _scenario(_b_many(80)),
    "clock_skew_warning": _scenario(_b_skew(61)),
    "launch_unknown": _scenario(
        _b_one_eligible, launcher=lambda: FakeLauncher([unknown_outcome()])
    ),
    "mixed_decisions_and_launch": _scenario(_b_mixed),
    "budget_gone_after_discovery": _scenario(_b_budget_gone_after_discovery),
}


# ==============================================================================
# FR-001, FR-002: the idle cycle and the own login
# ==============================================================================


def test_idle_cycle_makes_two_gh_calls_and_writes_one_cycle_line__fr001(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    res, deps = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]
    assert [argv[0] for argv, _ in world.runner.calls] == ["gh", "git", "gh"]
    assert deps.launcher.calls == []
    lines = _audit_lines(tmp_state)
    assert lines == list(res.lines)
    assert lines == [
        {
            "kind": "cycle",
            "ts": format_utc(CYCLE_NOW),
            "host": "test-host",
            "login": OWN_LOGIN,
            "cycle_id": res.cycle_id,
            "dry_run": False,
            "exit": 0,
            "reason": "cycle_complete",
            "gh_calls": 2,
            "duration_ms": 0,
            "discovery_count": 0,
            "clock_skew_s": 0,  # S 100: the offset is on every cycle line
        }
    ]
    assert tmp_state.load().last_completed_cycle_at == CYCLE_NOW


@pytest.mark.parametrize("how", ["failed", "auth"])
def test_gh_user_failure_is_exit_3_and_no_further_call__fr002(
    tmp_path, tmp_state, gh_world, how
):
    world = gh_world().fail("user", how)
    before = _snapshot(tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (3, "gh_auth_failed")
    assert world.runner.calls == [(_USER_ARGV, None)]
    assert deps.launcher.calls == []
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"]) == (3, "gh_auth_failed")
    assert line["login"] is None
    assert line["gh_calls"] == 1
    assert _snapshot(tmp_state) == before


def test_owner_account_id_mismatch_is_exit_2_and_no_further_call__fr002(
    tmp_path, tmp_state, gh_world
):
    world = gh_world(config=make_config(tmp_path, owner_account_id=OWN_ID + 1))
    before = _snapshot(tmp_state)
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (2, "account_id_mismatch")
    assert world.runner.calls == [(_USER_ARGV, None)]
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"], line["gh_calls"]) == (
        2,
        "account_id_mismatch",
        1,
    )
    assert _snapshot(tmp_state) == before


def test_owner_account_id_that_matches_lets_the_cycle_run__fr002(
    tmp_path, tmp_state, gh_world
):
    world = gh_world(config=make_config(tmp_path, owner_account_id=OWN_ID))
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]


@pytest.mark.parametrize("login", ["bad_login!", "a" * 40, "-leading-dash", "x y"])
def test_invalid_login_is_exit_3_and_no_discovery_call__fr002(
    tmp_path, tmp_state, gh_world, login
):
    world = gh_world(login=login)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (3, "login_invalid")
    assert world.gh_argvs == [_USER_ARGV]
    assert [argv[0] for argv, _ in world.runner.calls] == ["gh"]
    assert deps.launcher.calls == []
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"], line["gh_calls"]) == (3, "login_invalid", 1)
    assert line["login"] is None  # a rejected login is never written


def test_login_of_39_characters_is_accepted__fr002(tmp_path, tmp_state, gh_world):
    login = "a" * 39
    world = gh_world(login=login)
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world, login)]
    assert _the_cycle_line(_audit_lines(tmp_state))["login"] == login


# ==============================================================================
# Cycles that end before or at the first call
# ==============================================================================


def test_lock_held_is_exit_75_with_zero_calls_and_one_line__fr017_fr020(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    before = _snapshot(tmp_state)
    with tmp_state.lock():
        res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (75, "lock_held")
    assert world.runner.calls == []
    assert deps.launcher.calls == []
    lines = _audit_lines(tmp_state)
    assert len(lines) == 1
    assert lines[0]["kind"] == "cycle"
    assert (lines[0]["exit"], lines[0]["reason"]) == (75, "lock_held")
    assert (lines[0]["gh_calls"], lines[0]["login"]) == (0, None)
    assert _snapshot(tmp_state) == before


def test_lock_held_appends_but_never_rotates__fr020(tmp_path, tmp_state, gh_world):
    world = gh_world()
    path = tmp_state.state_dir / "audit.jsonl"
    path.write_bytes(_PADDING)
    with tmp_state.lock():
        res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 75
    assert not (tmp_state.state_dir / "audit.jsonl.1").exists()
    data = path.read_bytes()
    assert data.startswith(_PADDING)
    appended = json.loads(data[len(_PADDING) :])
    assert (appended["kind"], appended["exit"]) == ("cycle", 75)


def test_a_locked_cycle_rotates_a_full_audit_log_first__fr020(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    path = tmp_state.state_dir / "audit.jsonl"
    path.write_bytes(_PADDING)
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert (tmp_state.state_dir / "audit.jsonl.1").read_bytes() == _PADDING
    assert not (tmp_state.state_dir / "audit.jsonl.2").exists()
    assert _audit_lines(tmp_state) == list(res.lines)


def test_disabled_is_exit_0_with_zero_calls_and_no_health_stamp__fr018_fr021(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    (tmp_state.state_dir / "DISABLED").write_text("", encoding="utf-8")
    before = _snapshot(tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "disabled")
    assert world.runner.calls == []
    assert deps.launcher.calls == []
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"], line["gh_calls"]) == (0, "disabled", 0)
    assert tmp_state.load().last_completed_cycle_at is None
    assert _snapshot(tmp_state) == before


def test_enabled_false_is_exit_0_not_enabled_with_zero_calls__fr027(
    tmp_path, tmp_state, gh_world
):
    world = gh_world(config=make_config(tmp_path, enabled=False))
    before = _snapshot(tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "not_enabled")
    assert world.runner.calls == []
    assert deps.launcher.calls == []
    lines = _audit_lines(tmp_state)
    assert len(lines) == 1
    assert (lines[0]["exit"], lines[0]["reason"]) == (0, "not_enabled")
    assert tmp_state.load().last_completed_cycle_at is None
    assert _snapshot(tmp_state) == before


def test_dry_run_ignores_enabled_false__fr027(tmp_path, tmp_state, gh_world):
    world = gh_world(config=make_config(tmp_path, enabled=False))
    res, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    assert res.exit_code == 0
    assert res.reason != "not_enabled"
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert line["dry_run"] is True
    assert tmp_state.load().last_completed_cycle_at is None


@pytest.mark.parametrize(
    ("config", "reason"),
    [(_c_no_worktree, "worktree_invalid"), (_c_empty_approvers, "approvers_invalid")],
)
def test_bad_worktree_or_approvers_is_exit_2_with_zero_gh_calls__fr027(
    tmp_path, tmp_state, gh_world, config, reason
):
    world = gh_world(config=config(tmp_path))
    before = _snapshot(tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (2, reason)
    assert world.runner.calls == []
    assert deps.launcher.calls == []
    lines = _audit_lines(tmp_state)
    assert len(lines) == 1
    assert (lines[0]["kind"], lines[0]["exit"], lines[0]["reason"]) == (
        "cycle",
        2,
        reason,
    )
    assert lines[0]["gh_calls"] == 0
    assert _snapshot(tmp_state) == before


@pytest.mark.parametrize("how", ["foreign_origin", "timeout", "spawn_error", "failed"])
def test_origin_mismatch_is_exit_2_before_discovery__fr025(
    tmp_path, tmp_state, gh_world, how
):
    world = gh_world().fail("origin", how)
    before = _snapshot(tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (2, "origin_mismatch")
    assert [argv[0] for argv, _ in world.runner.calls] == ["gh", "git"]
    assert world.gh_argvs == [_USER_ARGV]
    assert deps.launcher.calls == []
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"], line["gh_calls"]) == (2, "origin_mismatch", 1)
    assert line["login"] == OWN_LOGIN
    assert _snapshot(tmp_state) == before


def _break_store_missing(tmp_state):
    (tmp_state.state_dir / "dispatch.json").unlink()


def _break_store_garbage(tmp_state):
    (tmp_state.state_dir / "dispatch.json").write_bytes(b"{not json")


def _break_store_wrong_shape(tmp_state):
    (tmp_state.state_dir / "dispatch.json").write_text('{"schema_version": 1}')


def _break_lock_missing(tmp_state):
    (tmp_state.state_dir / "lock").unlink()


def _break_lock_is_a_directory(tmp_state):
    (tmp_state.state_dir / "lock").unlink()
    (tmp_state.state_dir / "lock").mkdir()


@pytest.mark.parametrize(
    ("break_it", "reason"),
    [
        (_break_store_missing, "store_missing"),
        (_break_store_garbage, "store_invalid"),
        (_break_store_wrong_shape, "store_invalid"),
        (_break_lock_missing, "lock_missing"),
        (_break_lock_is_a_directory, "lock_invalid"),
    ],
)
def test_missing_or_invalid_store_is_exit_6_and_leaves_the_bytes__nfr011(
    tmp_path, tmp_state, gh_world, break_it, reason
):
    world = gh_world()
    break_it(tmp_state)
    before = _snapshot(tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (6, reason)
    assert world.runner.calls == []
    assert deps.launcher.calls == []
    lines = _audit_lines(tmp_state)
    assert len(lines) == 1
    assert (lines[0]["kind"], lines[0]["exit"], lines[0]["reason"]) == (
        "cycle",
        6,
        reason,
    )
    assert (lines[0]["gh_calls"], lines[0]["login"]) == (0, None)
    assert _snapshot(tmp_state) == before


# ==============================================================================
# NFR-007 and FR-022: a failed shared input voids the cycle
# ==============================================================================

SHARED_FAILURES = [
    ("login_timeout", 3, "gh_timeout"),
    ("login_failed", 3, "gh_auth_failed"),
    ("discovery_timeout", 3, "gh_timeout"),
    ("discovery_non_json", 3, "gh_non_json"),
    ("project_scope_missing", 3, "project_read_failed"),
    ("store_invalid", 6, "store_invalid"),
    ("store_missing", 6, "store_missing"),
    ("rate_limit_on_login", 5, "rate_limited"),
    ("rate_limit_on_discovery", 5, "rate_limit_clamped"),
]


@pytest.mark.parametrize(("name", "code", "reason"), SHARED_FAILURES)
def test_shared_failure_voids_the_cycle_with_zero_launches__nfr007_fr022(
    tmp_path, tmp_state, gh_world, name, code, reason
):
    res, deps, world = SCENARIOS[name](tmp_path, tmp_state, gh_world)
    assert (res.exit_code, res.reason) == (code, reason)
    assert deps.launcher.calls == []
    assert res.launched_issue is None
    assert not _probed(world)
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"]) == (code, reason)
    assert tmp_state.state_dir.joinpath("dispatch.json").exists() is (
        name != "store_missing"
    )
    if code != 6:
        assert tmp_state.load().entries == {}
        assert tmp_state.load().last_completed_cycle_at is None


def test_events_failure_of_one_issue_skips_only_that_issue__fr022(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(8)
    world.issue(9)
    world.fail("events", "failed", n=8)
    res, deps = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    decisions = _of_kind(_audit_lines(tmp_state), "decision")
    assert [(d["issue"], d["reason"]) for d in decisions] == [
        (8, "events_unreadable"),
        (9, "launched"),
    ]
    assert res.launched_issue == 9
    assert len(deps.launcher.calls) == 1


# ==============================================================================
# FR-004 and the two warnings (DF-22)
# ==============================================================================


def test_99_discovery_results_proceed__fr004(tmp_path, tmp_state, gh_world):
    world = gh_world()
    _b_many(99)(world, tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]
    lines = _audit_lines(tmp_state)
    decisions = _of_kind(lines, "decision")
    assert [d["issue"] for d in decisions] == list(range(1, 11))  # MAX_CANDIDATES
    assert {d["reason"] for d in decisions} == {"assigned_other"}
    assert _the_cycle_line(lines)["discovery_count"] == 99
    assert deps.launcher.calls == []


@pytest.mark.parametrize("count", [100, 101])
def test_100_or_more_discovery_results_are_exit_4_truncated__fr004(
    tmp_path, tmp_state, gh_world, count
):
    world = gh_world()
    _b_many(count)(world, tmp_state)
    before = _snapshot(tmp_state)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (4, "truncated")
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]
    assert deps.launcher.calls == []
    lines = _audit_lines(tmp_state)
    assert _of_kind(lines, "decision") == []
    line = _the_cycle_line(lines)
    assert (line["exit"], line["reason"], line["gh_calls"]) == (4, "truncated", 2)
    assert "discovery_count" not in line
    assert _snapshot(tmp_state) == before


def test_a_repeated_issue_number_is_exit_4_discovery_duplicate__fr004(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9, listed=2)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (4, "discovery_duplicate")
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]
    assert deps.launcher.calls == []
    assert _of_kind(_audit_lines(tmp_state), "decision") == []
    assert tmp_state.load().last_completed_cycle_at is None


def test_discovery_count_warning_is_absent_at_79__fr003_df22(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    _b_many(79)(world, tmp_state)
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    lines = _audit_lines(tmp_state)
    assert _of_kind(lines, "warning") == []
    assert _the_cycle_line(lines)["discovery_count"] == 79


def test_discovery_count_warning_is_present_at_80__fr003_df22(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    _b_many(80)(world, tmp_state)
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    lines = _audit_lines(tmp_state)
    (warning,) = _of_kind(lines, "warning")
    assert warning["reason"] == "discovery_count"
    assert warning["discovery_count"] == 80
    assert warning["login"] == OWN_LOGIN
    assert warning["cycle_id"] == res.cycle_id
    assert "issue" not in warning
    assert lines.index(warning) < lines.index(_the_cycle_line(lines))
    assert _the_cycle_line(lines)["discovery_count"] == 80


@pytest.mark.parametrize(("skew_s", "seen"), [(0, 0), (59, 59), (60, 60), (-60, 60)])
def test_clock_skew_warning_is_absent_up_to_60_seconds_but_the_cycle_line_records_it__df22(
    tmp_path, tmp_state, gh_world, skew_s, seen
):
    # Spec line 100: the cycle line records the offset every cycle; only the
    # warning line has the 60 s threshold.
    world = gh_world()
    world.skew_s = skew_s
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    lines = _audit_lines(tmp_state)
    assert _of_kind(lines, "warning") == []
    assert _the_cycle_line(lines)["clock_skew_s"] == seen
    assert isinstance(_the_cycle_line(lines)["clock_skew_s"], int)


@pytest.mark.parametrize(("skew_s", "seen"), [(61, 61), (-61, 61), (300, 300)])
def test_clock_skew_warning_is_present_from_61_seconds__df22(
    tmp_path, tmp_state, gh_world, skew_s, seen
):
    world = gh_world()
    world.skew_s = skew_s
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0  # a warning never changes the exit
    lines = _audit_lines(tmp_state)
    (warning,) = _of_kind(lines, "warning")
    assert warning["reason"] == "clock_skew"
    assert warning["clock_skew_s"] == seen
    assert warning["login"] == OWN_LOGIN
    assert _the_cycle_line(lines)["clock_skew_s"] == seen
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]


def test_unparseable_date_header_skips_the_skew_check__df35(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.date_text = "not a date"
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    lines = _audit_lines(tmp_state)
    assert _of_kind(lines, "warning") == []
    assert "clock_skew_s" not in _the_cycle_line(lines)  # server date unknown


# ==============================================================================
# FR-028: rate limits (DF-51)
# ==============================================================================


def test_retry_after_120_persists_next_permitted_at_and_blocks_the_next_cycle__fr028_df51(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.user_retry_after = "120"
    world.fail("user", "rate")
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (5, "rate_limited")
    assert world.runner.calls == [(_USER_ARGV, None)]
    stored = tmp_state.load()
    assert stored.next_permitted_at == CYCLE_NOW + timedelta(seconds=120)
    assert stored.last_completed_cycle_at is None
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"], line["gh_calls"]) == (5, "rate_limited", 1)

    # 60 s later the cycle is still inside the window: exit 5, zero calls.
    world.clock.advance(60)
    calls = len(world.runner.calls)
    again, _ = _run(tmp_path, tmp_state, world)
    assert (again.exit_code, again.reason) == (5, "rate_limited")
    assert len(world.runner.calls) == calls
    last = _audit_lines(tmp_state)[-1]
    assert (last["kind"], last["exit"], last["reason"], last["gh_calls"]) == (
        "cycle",
        5,
        "rate_limited",
        0,
    )
    assert tmp_state.load().next_permitted_at == CYCLE_NOW + timedelta(seconds=120)


def test_the_rate_limit_window_ends_exactly_at_next_permitted_at__fr028(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.user_retry_after = "120"
    world.fail("user", "rate")
    _run(tmp_path, tmp_state, world)
    world.clock.advance(119)
    calls = len(world.runner.calls)
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 5
    assert len(world.runner.calls) == calls
    world.clock.advance(1)
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert world.gh_argvs[-2:] == [_USER_ARGV, _discover_argv(world)]


@pytest.mark.parametrize(
    ("retry_after", "seconds", "reason"),
    [
        ("1", 1, "rate_limited"),
        ("3600", 3600, "rate_limited"),
        ("3601", 3600, "rate_limit_clamped"),
        ("86400", 3600, "rate_limit_clamped"),
        ("0", 3600, "rate_limit_clamped"),
        ("soon", 3600, "rate_limit_clamped"),
        (None, 3600, "rate_limit_clamped"),
    ],
)
def test_retry_after_is_clamped_to_3600_seconds__fr028(
    tmp_path, tmp_state, gh_world, retry_after, seconds, reason
):
    world = gh_world()
    world.user_retry_after = retry_after
    world.fail("user", "rate")
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (5, reason)
    assert tmp_state.load().next_permitted_at == CYCLE_NOW + timedelta(seconds=seconds)
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"]) == (5, reason)


@pytest.mark.parametrize(
    ("call", "how", "n"),
    [
        ("discover", "rate", None),
        ("comments", "rate_403", 9),
        ("events", "rate", 9),
        ("edits", "rate_graphql", 9),
        ("items", "rate_graphql", 9),
    ],
)
def test_a_rate_limit_on_any_call_but_g1_always_clamps_to_3600_s__fr028_df51(
    tmp_path, tmp_state, gh_world, call, how, n
):
    world = gh_world()
    world.issue(9)
    world.fail(call, how, n=n)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (5, "rate_limit_clamped")
    assert deps.launcher.calls == []
    stored = tmp_state.load()
    assert stored.next_permitted_at == CYCLE_NOW + timedelta(seconds=3600)
    assert stored.entries == {}
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"]) == (5, "rate_limit_clamped")


def test_a_rate_limit_keeps_the_stamps_of_candidates_already_examined__fr028(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    _b_rate_on_issue(world, tmp_state)
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (5, "rate_limit_clamped")
    stored = tmp_state.load()
    assert dict(stored.considered) == {8: CYCLE_NOW}  # 9 hit the limit: no stamp
    assert stored.next_permitted_at == CYCLE_NOW + timedelta(seconds=3600)


def test_an_entry_written_earlier_in_the_cycle_stands_when_a_read_is_rate_limited__fr028_df51(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    ctx = record.PendingContext(
        approver_id=APPROVER_ID,
        approval_event_id=2,
        approved_at=T_APPROVED,
        launch_cwd=str(world.config.worktree),
        launch_login=OWN_LOGIN,
        launch_account_id=OWN_ID,
    )
    crashed = record.mark_pending(
        tmp_state.load(), 5, ctx, CYCLE_NOW - timedelta(minutes=5)
    )
    tmp_state.save(crashed)
    world.fail("discover", "rate")  # the sweep (step 7) runs before discovery (8)
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (5, "rate_limit_clamped")
    stored = tmp_state.load()
    assert stored.entries[5].state == "abandoned"
    assert stored.entries[5].last_reason == "pending_orphan"
    assert stored.next_permitted_at == CYCLE_NOW + timedelta(seconds=3600)
    decisions = _of_kind(_audit_lines(tmp_state), "decision")
    assert [(d["issue"], d["reason"], d["state"]) for d in decisions] == [
        (5, "pending_orphan", "abandoned")
    ]


# ==============================================================================
# FR-029, AC-19 (DF-55 part d): the deadline, in process
# ==============================================================================


def test_timed_out_login_is_exit_3_gh_timeout_with_the_20_s_timeout__fr029_ac19(
    tmp_path, tmp_state, gh_world
):
    world = gh_world().fail("user", "timeout")
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (3, "gh_timeout")
    assert world.runner.calls == [(_USER_ARGV, None)]
    assert world.runner.timeouts == [20.0]


def test_timed_out_discovery_is_exit_3_gh_timeout__fr029_ac19(
    tmp_path, tmp_state, gh_world
):
    world = gh_world().fail("discover", "timeout")
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (3, "gh_timeout")
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]
    assert world.runner.timeouts == [20.0, 10.0, 20.0]  # gh, git origin, gh


def test_no_gh_call_starts_after_236_s_and_the_store_is_still_written__fr029_ac19(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.on("discover", lambda: world.clock.advance(236))
    res, deps = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert world.gh_argvs == [_USER_ARGV, _discover_argv(world)]  # nothing after 236 s
    assert deps.launcher.calls == []
    lines = _audit_lines(tmp_state)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["issue"], decision["reason"]) == (9, "budget_exhausted")
    assert "state" not in decision
    line = _the_cycle_line(lines)
    assert (line["gh_calls"], line["duration_ms"]) == (2, 236000)
    stored = tmp_state.load()
    assert stored.last_completed_cycle_at == CYCLE_NOW + timedelta(seconds=236)
    assert 9 not in stored.considered  # budget_exhausted is never stamped
    assert stored.entries == {}


def test_a_gh_call_still_starts_with_exactly_5_s_left_and_gets_a_5_s_timeout__fr029(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.on("discover", lambda: world.clock.advance(235))
    _run(tmp_path, tmp_state, world)
    argv, _ = world.runner.calls[3]  # after gh user, git origin, gh discovery
    assert argv == tuple(github.argv_comments(9, 1))
    assert world.runner.timeouts[3] == 5.0


def test_discovery_does_not_start_with_under_5_s_left__fr029_ac19(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.on("origin", lambda: world.clock.advance(236))
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (3, "gh_timeout")
    assert world.gh_argvs == [_USER_ARGV]
    assert deps.launcher.calls == []
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"], line["gh_calls"]) == (3, "gh_timeout", 1)


def test_no_launch_starts_at_121_s_elapsed__fr029_ac19(tmp_path, tmp_state, gh_world):
    world = gh_world()
    world.issue(9)
    world.on("reread", lambda: world.clock.advance(121), n=9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert deps.launcher.calls == []
    assert res.launched_issue is None
    lines = _audit_lines(tmp_state)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["issue"], decision["reason"]) == (9, "budget_exhausted")
    assert "state" not in decision
    stored = tmp_state.load()
    assert stored.entries == {}  # nothing was written before the launch
    assert 9 not in stored.considered
    assert stored.last_completed_cycle_at == CYCLE_NOW + timedelta(seconds=121)


def test_a_launch_still_starts_at_exactly_120_s_with_its_full_timeout__fr029_ac19(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.on("reread", lambda: world.clock.advance(120), n=9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.launched_issue) == (0, 9)
    assert len(deps.launcher.calls) == 1
    assert deps.launcher.calls[0][3] == 120.0  # never shortened
    assert tmp_state.load().entries[9].state == "launched"


# ==============================================================================
# AC-14, FR-020: one cycle line per exit, one decision line per examined issue
# ==============================================================================

EXIT_TABLE = [
    (
        0,
        "mixed_decisions_and_launch",
        [(11, "assigned_other"), (12, "not_approved"), (13, "launched")],
    ),
    (2, "worktree_invalid", []),
    (3, "discovery_non_json", []),
    (4, "truncated_100", []),
    # the candidate that stops the cycle gets no decision line (Gate C fix C-2)
    (5, "rate_limit_on_issue", [(8, "assigned_other")]),
    (6, "store_invalid", []),
    (7, "launch_unknown", [(11, "launch_unknown")]),
    (75, "lock_held", []),
]


@pytest.mark.parametrize(("code", "name", "expected"), EXIT_TABLE)
def test_every_exit_appends_one_cycle_line_and_one_decision_per_issue__ac14_fr020(
    tmp_path, tmp_state, gh_world, code, name, expected
):
    res, _, _ = SCENARIOS[name](tmp_path, tmp_state, gh_world)
    assert res.exit_code == code
    lines = _audit_lines(tmp_state)
    assert lines == list(res.lines)
    cycle_line = _the_cycle_line(lines)
    assert cycle_line["exit"] == code
    assert lines[-1] is cycle_line  # decision lines first, the cycle line last
    assert {ln["cycle_id"] for ln in lines} == {res.cycle_id}
    decisions = _of_kind(lines, "decision")
    assert [(d["issue"], d["reason"]) for d in decisions] == expected


# ==============================================================================
# DF-41: the exit and the line kind follow audit.REASON_TABLE
# ==============================================================================

_DECISION_TABLE_KINDS = frozenset({"skip", "entry", "skip/warning"})
_WARNING_TABLE_KINDS = frozenset({"warning", "skip/warning"})


def check_line_kinds(lines) -> None:
    """Assert every line's reason is allowed on its line kind (DF-41), strictly.

    Parts C and D call this over the lines their scenarios write. A ``cycle``
    line names a cycle-kind reason whose table exit is the line's exit; the one
    other kind it may carry is an entry reason with table exit 7 (the exit-7
    reasons of the failed entry, design 4.3). A skip reason never sits on a
    cycle line, and a cycle reason never sits on a ``decision`` line. A clean
    cycle's line names ``cycle_complete`` (Gate C fix C-2, [PROPOSAL]).
    """
    for ln in lines:
        reason = ln["reason"]
        table_kind, table_exit = audit.REASON_TABLE[reason]
        if ln["kind"] == "cycle":
            assert cycle.exit_for(reason) == table_exit == ln["exit"]
            assert table_kind == "cycle" or (table_kind == "entry" and table_exit == 7)
        elif ln["kind"] == "decision":
            assert table_kind in _DECISION_TABLE_KINDS
        else:
            assert ln["kind"] == "warning"
            assert table_kind in _WARNING_TABLE_KINDS


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_exit_and_kind_follow_reason_table__df41(tmp_path, tmp_state, gh_world, name):
    res, _, _ = SCENARIOS[name](tmp_path, tmp_state, gh_world)
    lines = _audit_lines(tmp_state)
    assert lines == list(res.lines)
    cycle_line = _the_cycle_line(lines)
    assert cycle_line["exit"] == res.exit_code
    assert cycle_line["reason"] == res.reason
    if res.exit_code != 0:
        assert cycle.exit_for(res.reason) == res.exit_code
        assert audit.REASON_TABLE[res.reason][1] == res.exit_code
    check_line_kinds(lines)


def test_check_line_kinds_rejects_a_skip_reason_on_a_failing_cycle_line__df41():
    base = {"ts": "2026-11-07T13:00:00Z", "host": "h", "login": None}
    bad = [{**base, "kind": "cycle", "reason": "not_approved", "exit": 3}]
    with pytest.raises(AssertionError):
        check_line_kinds(bad)


def test_check_line_kinds_rejects_a_warning_reason_on_a_decision_line__df41():
    base = {"ts": "2026-11-07T13:00:00Z", "host": "h", "login": None}
    lines = [
        {**base, "kind": "decision", "reason": "clock_skew", "issue": 9},
        {**base, "kind": "cycle", "reason": "cycle_complete", "exit": 0},
    ]
    with pytest.raises(AssertionError):
        check_line_kinds(lines)


@pytest.mark.parametrize("reason", ["not_approved", "launched", "already_dispatched"])
def test_check_line_kinds_rejects_a_skip_or_entry_reason_on_a_clean_cycle_line__df41(
    reason,
):
    base = {"ts": "2026-11-07T13:00:00Z", "host": "h", "login": None}
    with pytest.raises(AssertionError):
        check_line_kinds([{**base, "kind": "cycle", "reason": reason, "exit": 0}])


@pytest.mark.parametrize(
    "reason", ["rate_limit_clamped", "orca_not_found", "disabled_mid_cycle"]
)
def test_check_line_kinds_rejects_a_cycle_reason_on_a_decision_line__df41(reason):
    base = {"ts": "2026-11-07T13:00:00Z", "host": "h", "login": None}
    lines = [
        {**base, "kind": "decision", "reason": reason, "issue": 9},
        {**base, "kind": "cycle", "reason": reason, "exit": 0},
    ]
    with pytest.raises(AssertionError):
        check_line_kinds(lines)


def test_check_line_kinds_accepts_a_clean_cycle_and_an_exit_7_entry_reason__df41():
    base = {"ts": "2026-11-07T13:00:00Z", "host": "h", "login": None}
    check_line_kinds(
        [
            {**base, "kind": "decision", "reason": "launch_unknown", "issue": 9},
            {**base, "kind": "cycle", "reason": "launch_unknown", "exit": 7},
        ]
    )
    check_line_kinds(
        [
            {**base, "kind": "decision", "reason": "not_approved", "issue": 9},
            {**base, "kind": "cycle", "reason": "cycle_complete", "exit": 0},
        ]
    )


# ==============================================================================
# Part C: the per-candidate flow, launch order, dry-run and S1 (plan step 6.7)
#
# Same rules as part B: every scenario is a ``GhWorld`` over a ``FakeClock``, and
# every cycle's lines go through ``check_line_kinds`` (DF-41) via ``_lines_of``.
# ==============================================================================

_SEED_CWD = "/seed/worktree"
_OLD_LOGIN = "old-login"
_FULL_READS = ["comments", "events", "edits", "items"]  # r = 4, one page each
_LAUNCH_READS = [*_FULL_READS, "reread", "events", "items"]  # the 3 reserved calls
_LAUNCH_TRACE = [
    "user",
    "origin",
    "discover",
    "comments:9",
    "events:9",
    "edits:9",
    "items:9",
    "probe",
    "reread:9",
    "events:9",
    "items:9",
    "origin",
]
_CLAIM_9 = "/sc:issue --claim 9"
_T_MARK = T_APPROVED + timedelta(minutes=1)  # a claim marker after the approval
_SHADOW_AT = "2026-11-07T13:00:00Z"  # CYCLE_NOW, as dry-run.json writes it


def _trace(world) -> list[str]:
    """Every runner call of ``world`` as ``user``, ``origin``, ``discover``,
    ``probe`` or ``<read>:<issue>``, in call order."""
    names: dict[tuple[str, ...], str] = {
        _USER_ARGV: "user",
        _discover_argv(world): "discover",
    }
    for n in world.issues:
        for page in range(1, github.PAGE_CAP + 1):
            names[tuple(github.argv_events(n, page))] = f"events:{n}"
            names[tuple(github.argv_comments(n, page))] = f"comments:{n}"
        names[tuple(github.argv_edits(n))] = f"edits:{n}"
        names[tuple(github.argv_project_items(n))] = f"items:{n}"
        names[tuple(github.argv_reread(n))] = f"reread:{n}"
    out = []
    for argv, _ in world.runner.calls:
        if argv[0] == "git":
            out.append("origin")
        elif "skills" in argv:
            out.append("probe")
        else:
            out.append(names[argv])
    return out


def _reads(world, n) -> list[str]:
    """The per-issue ``gh`` reads made for issue ``n``, in call order."""
    return [t.split(":")[0] for t in _trace(world) if t.endswith(f":{n}")]


def _touched(world) -> set[int]:
    return {n for n in world.issues if _reads(world, n)}


def _decisions(lines) -> list[tuple[int, str]]:
    return [(d["issue"], d["reason"]) for d in _of_kind(lines, "decision")]


def _lines_of(tmp_state, res) -> list[dict]:
    """The lines of one cycle, checked against the reason table (DF-41)."""
    lines = [ln for ln in _audit_lines(tmp_state) if ln["cycle_id"] == res.cycle_id]
    assert lines == list(res.lines)
    check_line_kinds(lines)
    return lines


def _entry(tmp_state, n):
    return tmp_state.load().entries.get(n)


def _seed_doc(tmp_state, **fields) -> None:
    tmp_state.save(replace(tmp_state.load(), **fields))


def _ctx(login=OWN_LOGIN, account_id=OWN_ID) -> record.PendingContext:
    return record.PendingContext(
        approver_id=APPROVER_ID,
        approval_event_id=2,
        approved_at=T_APPROVED,
        launch_cwd=_SEED_CWD,
        launch_login=login,
        launch_account_id=account_id,
    )


def _seed(tmp_state, n, kind, at, *, login=OWN_LOGIN, op="op-seed-0001"):
    """Store an entry of ``kind`` for issue ``n`` written at ``at``; return it."""
    doc = tmp_state.load()
    if kind == "failed":
        doc = record.fail(doc, n, "revalidation_transient", at)
    elif kind == "exhausted":
        for _ in range(record.MAX_ATTEMPTS):
            doc = record.fail(doc, n, "revalidation_transient", at)
    elif kind == "claimed":
        doc = record.mark_claimed(doc, n, at)
    else:
        doc = record.mark_pending(doc, n, _ctx(login), at)
        if kind == "launched":
            doc = record.mark_launched(doc, n, op, at)
        elif kind == "unknown":
            doc = record.mark_unknown(doc, n, op, at)
        elif kind == "spawn_error":
            doc = record.mark_spawn_error(doc, n, at)
        else:
            assert kind == "pending"
    tmp_state.save(doc)
    return doc.entries[n]


def _ev(world, *, trigger=T_TRIGGER, approval=T_APPROVED, approver=APPROVER_ID):
    """The two label events of an approved issue; ``None`` leaves one out."""
    cfg = world.config
    out = []
    if trigger is not None:
        out.append(
            label_event(
                1,
                "labeled",
                cfg.trigger_label,
                trigger,
                actor_id=2001,
                actor_login="issue-author",
            )
        )
    if approval is not None:
        out.append(
            label_event(
                2,
                "labeled",
                cfg.approval_label,
                approval,
                actor_id=approver,
                actor_login=OWN_LOGIN,
            )
        )
    return out


def _mark(at, **over):
    return marker_comment(1, at, **over)


def _on_nth(world, call, n, k, fn):
    """Run ``fn`` just before the ``k``-th (1-based) ``call`` read of issue ``n``."""
    seen = {"count": 0}

    def hook():
        seen["count"] += 1
        if seen["count"] == k:
            fn()

    world.on(call, hook, n=n)


# ==============================================================================
# Every per-issue skip reason, through a whole cycle
# ==============================================================================

_T_BEFORE_INIT = FIXED_NOW - timedelta(minutes=1)  # the store was created at FIXED_NOW
_RENAMED = label_event(
    3, "renamed", None, _T_MARK, actor_id=None, actor_login=None, actor_type=None
)

SKIP_CASES = [
    pytest.param(
        lambda w: w.issue(9, events=_ev(w, approval=None)),
        "not_approved",
        ["comments", "events"],
        id="no_approval_event",
    ),
    pytest.param(
        lambda w: w.issue(9, events=_ev(w, approver=9999)),
        "not_approved",
        ["comments", "events"],
        id="approver_not_on_the_list",
    ),
    pytest.param(
        lambda w: w.issue(9, labels=[w.config.trigger_label]),
        "not_approved",
        ["comments", "events"],
        id="approval_label_no_longer_set",
    ),
    pytest.param(
        lambda w: w.issue(9, events=_ev(w, trigger=_T_MARK)),
        "approval_before_trigger",
        ["comments", "events"],
        id="approval_before_trigger",
    ),
    pytest.param(
        lambda w: w.issue(
            9,
            events=_ev(
                w,
                trigger=FIXED_NOW - timedelta(minutes=2),
                approval=_T_BEFORE_INIT,
            ),
        ),
        "approval_before_init",
        ["comments", "events"],
        id="approval_before_init",
    ),
    pytest.param(
        lambda w: w.issue(
            9,
            events=_ev(w, trigger=FIXED_NOW - timedelta(minutes=2), approval=FIXED_NOW),
        ),
        "approval_before_init",
        ["comments", "events"],
        id="approval_at_the_second_the_store_was_created",
    ),
    pytest.param(
        lambda w: w.issue(9, events=[*_ev(w), _ev(w)[0]]),
        "events_incomplete",
        ["comments", "events"],
        id="event_id_repeated",
    ),
    pytest.param(
        lambda w: w.issue(9, events=_ev(w, trigger=T_APPROVED)),
        "events_incomplete",
        ["comments", "events"],
        id="trigger_and_approval_in_the_same_second",
    ),
    pytest.param(
        lambda w: w.issue(9).fail("edits", "failed", n=9),
        "edits_unreadable",
        ["comments", "events", "edits"],
        id="edits_read_fails",
    ),
    pytest.param(
        lambda w: w.issue(9, edits={"edited_at": T_APPROVED}),
        "edited_after_approval",
        ["comments", "events", "edits"],
        id="body_edited_at_the_approval_second",
    ),
    pytest.param(
        lambda w: w.issue(9, edits={"edited_at": T_APPROVED + timedelta(seconds=1)}),
        "edited_after_approval",
        ["comments", "events", "edits"],
        id="body_edited_after_the_approval",
    ),
    pytest.param(
        lambda w: w.issue(
            9,
            edits={
                "comments": [
                    {
                        "id": 5,
                        "author": "other-user",
                        "created_at": _T_MARK,
                        "edited_at": None,
                    }
                ]
            },
        ),
        "edited_after_approval",
        ["comments", "events", "edits"],
        id="foreign_comment_after_the_approval",
    ),
    pytest.param(
        lambda w: w.issue(9, events=[*_ev(w), _RENAMED]),
        "edited_after_approval",
        ["comments", "events", "edits"],
        id="title_renamed_after_the_approval",
    ),
    pytest.param(
        lambda w: w.issue(9, items=[{"status": "In progress"}]),
        "project_mismatch",
        _FULL_READS,
        id="status_not_backlog",
    ),
    pytest.param(
        lambda w: w.issue(9, items=[{}, {}]),
        "project_mismatch",
        _FULL_READS,
        id="two_items_in_the_project",
    ),
    pytest.param(
        lambda w: w.issue(9, items=[{"archived": True}]),
        "project_mismatch",
        _FULL_READS,
        id="item_archived",
    ),
    pytest.param(
        lambda w: w.issue(9, items=[{"project_id": "PVT_other_project"}]),
        "project_mismatch",
        _FULL_READS,
        id="item_in_another_project",
    ),
    pytest.param(
        lambda w: w.issue(9, items=[{"status": None}]),
        "project_mismatch",
        _FULL_READS,
        id="item_without_a_status",
    ),
    pytest.param(
        lambda w: w.issue(9).fail("items", "failed", n=9),
        "project_unreadable",
        _FULL_READS,
        id="items_read_fails",
    ),
    pytest.param(
        lambda w: w.issue(9, assignees=[]), "unassigned", [], id="no_assignee"
    ),
    pytest.param(
        lambda w: w.issue(9, assignees=[OWN_LOGIN, "other-user"]),
        "assigned_other",
        [],
        id="own_and_other_assignee",
    ),
    pytest.param(
        lambda w: w.issue(9, assignees=["other-user"]),
        "assigned_other",
        [],
        id="only_another_assignee",
    ),
]


@pytest.mark.parametrize(("build", "reason", "reads"), SKIP_CASES)
def test_every_per_issue_skip_reason_through_a_whole_cycle__fr005_fr009_fr022(
    tmp_path, tmp_state, gh_world, build, reason, reads
):
    """AC-3, AC-4, FR-005, FR-007, FR-008, FR-009, FR-022: each skip row in a cycle."""
    world = gh_world()
    build(world)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(9, reason)]
    (decision,) = _of_kind(lines, "decision")
    assert "state" not in decision  # a skip writes no entry
    assert _reads(world, 9) == reads
    assert not _probed(world)
    assert deps.launcher.calls == []
    assert _the_cycle_line(lines)["gh_calls"] == 2 + len(reads)
    stored = tmp_state.load()
    assert stored.entries == {}
    assert dict(stored.considered) == {9: CYCLE_NOW}  # a skip is still examined
    assert stored.last_completed_cycle_at == CYCLE_NOW


@pytest.mark.parametrize(
    ("call", "how", "reason", "reads"),
    [
        ("events", "failed", "events_unreadable", ["comments", "events"]),
        ("comments", "failed", "marker_unreadable", ["comments"]),
        ("edits", "failed", "edits_unreadable", ["comments", "events", "edits"]),
        ("items", "failed", "project_unreadable", _FULL_READS),
        ("items", "non_json", "project_unreadable", _FULL_READS),
    ],
)
def test_an_unreadable_issue_skips_and_the_next_one_is_still_examined__fr007_fr022(
    tmp_path, tmp_state, gh_world, call, how, reason, reads
):
    world = gh_world()
    world.issue(8)
    world.issue(9)
    world.fail(call, how, n=8)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.launched_issue) == (0, 9)
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(8, reason), (9, "launched")]
    assert _reads(world, 8) == reads
    assert _reads(world, 9) == _LAUNCH_READS
    assert deps.launcher.calls == [
        (ORCA_PATH, str(world.config.worktree), _CLAIM_9, 120.0)
    ]
    assert _entry(tmp_state, 8) is None
    assert _entry(tmp_state, 9).state == "launched"
    assert dict(tmp_state.load().considered) == {8: CYCLE_NOW, 9: CYCLE_NOW}
    assert _the_cycle_line(lines)["gh_calls"] == 2 + len(reads) + 7


def test_a_marker_read_failure_never_counts_as_claimed__fr009_df02(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9, markers=[_mark(_T_MARK)])
    world.fail("comments", "failed", n=9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "marker_unreadable")]
    assert _entry(tmp_state, 9) is None  # not claimed, not launched
    assert deps.launcher.calls == []


# ==============================================================================
# Skips that come from the stored entry: already_dispatched, in_backoff, day_cap
# ==============================================================================

_PENDING_AT = CYCLE_NOW - timedelta(minutes=10)


@pytest.mark.parametrize("kind", ["launched", "unknown", "spawn_error"])
def test_a_dispatched_entry_without_a_fresh_marker_skips_already_dispatched__fr009(
    tmp_path, tmp_state, gh_world, kind
):
    """AC-9, FR-009, FR-015: no automatic retry of a launched or unknown entry."""
    world = gh_world()
    world.issue(9, markers=[_mark(_PENDING_AT - timedelta(seconds=301))])
    seeded = _seed(tmp_state, 9, kind, _PENDING_AT)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(9, "already_dispatched")]
    assert _reads(world, 9) == ["comments"]  # the marker only, no approval reads
    assert _entry(tmp_state, 9) == seeded
    assert deps.launcher.calls == []


def test_a_claimed_entry_skips_already_dispatched_without_a_call__fr009(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    seeded = _seed(tmp_state, 9, "claimed", _PENDING_AT)
    res, deps = _run(tmp_path, tmp_state, world)
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "already_dispatched")]
    assert _reads(world, 9) == []
    assert _entry(tmp_state, 9) == seeded
    assert deps.launcher.calls == []


def test_a_pending_entry_at_cycle_start_is_swept_then_skipped__fr011(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _seed(tmp_state, 9, "pending", _PENDING_AT)
    res, deps = _run(tmp_path, tmp_state, world)
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [
        (9, "pending_orphan"),
        (9, "already_dispatched"),
    ]
    sweep, skip = _of_kind(lines, "decision")
    assert sweep["state"] == "abandoned"
    assert "state" not in skip
    stored = _entry(tmp_state, 9)
    assert (stored.state, stored.last_reason, stored.launches) == (
        "abandoned",
        "pending_orphan",
        1,
    )
    assert deps.launcher.calls == []


@pytest.mark.parametrize("age_s", [0, 300, 599])
def test_a_failed_entry_inside_the_10_minute_backoff_skips_in_backoff__df43(
    tmp_path, tmp_state, gh_world, age_s
):
    world = gh_world()
    world.issue(9)
    seeded = _seed(tmp_state, 9, "failed", CYCLE_NOW - timedelta(seconds=age_s))
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "in_backoff")]
    assert _reads(world, 9) == ["comments", "events"]
    assert _entry(tmp_state, 9) == seeded
    assert deps.launcher.calls == []


def test_a_failed_entry_in_backoff_stays_in_backoff_when_the_approval_is_gone__df43(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9, events=_ev(world, approval=None))
    seeded = _seed(tmp_state, 9, "failed", CYCLE_NOW - timedelta(minutes=1))
    res, _ = _run(tmp_path, tmp_state, world)
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "in_backoff")]
    assert _entry(tmp_state, 9) == seeded


def test_a_failed_entry_in_backoff_stays_in_backoff_when_events_cannot_be_read__df43(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.fail("events", "failed", n=9)
    seeded = _seed(tmp_state, 9, "failed", CYCLE_NOW - timedelta(minutes=1))
    res, _ = _run(tmp_path, tmp_state, world)
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "in_backoff")]
    assert _entry(tmp_state, 9) == seeded


def _day_cap_entries(tmp_state, times):
    for n, at in enumerate(times, start=101):
        _seed(tmp_state, n, "unknown", at)


_HOUR = timedelta(hours=1)
_DAY = timedelta(hours=24)


@pytest.mark.parametrize(
    "times",
    [
        [CYCLE_NOW - _HOUR] * 6,
        [CYCLE_NOW - _HOUR] * 5 + [CYCLE_NOW - _DAY + timedelta(seconds=1)],
        [CYCLE_NOW] * 6,
    ],
    ids=["six_in_the_last_day", "oldest_one_second_inside_the_window", "six_now"],
)
def test_six_launches_in_the_rolling_day_skip_day_cap__fr024(
    tmp_path, tmp_state, gh_world, times
):
    world = gh_world()
    world.issue(9)
    _day_cap_entries(tmp_state, times)
    before = tmp_state.load().entries
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(9, "day_cap")]
    assert _reads(world, 9) == []  # a local check: no read at all
    assert tmp_state.load().entries == before
    assert deps.launcher.calls == []
    assert _the_cycle_line(lines)["gh_calls"] == 2


def test_the_day_cap_window_is_half_open_at_24_hours__fr024(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _day_cap_entries(tmp_state, [CYCLE_NOW - _HOUR] * 5 + [CYCLE_NOW - _DAY])
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.launched_issue) == (0, 9)  # 5 inside the window
    assert len(deps.launcher.calls) == 1


def test_the_consumed_log_counts_toward_the_day_cap__fr024(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _day_cap_entries(tmp_state, [CYCLE_NOW - _HOUR] * 5)
    _seed_doc(tmp_state, consumed_log=(CYCLE_NOW - 2 * _HOUR,))
    res, deps = _run(tmp_path, tmp_state, world)
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "day_cap")]
    assert deps.launcher.calls == []


# ==============================================================================
# AC-5, FR-009: the claimed paths
# ==============================================================================


def test_an_own_claim_marker_gives_claimed_and_no_launch__ac5_fr009(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9, markers=[_mark(_T_MARK)])
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.launched_issue) == (0, None)
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["issue"], decision["reason"], decision["state"]) == (
        9,
        "claimed",
        "claimed",
    )
    assert (
        decision["approver_id"],
        decision["approval_event_id"],
        decision["approved_at"],
    ) == (APPROVER_ID, 2, "2026-11-07T12:02:00Z")
    assert _reads(world, 9) == ["comments", "events"]  # claimed before the edit reads
    assert not _probed(world)
    assert deps.launcher.calls == []
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.launches, entry.attempts) == ("claimed", 0, 0)
    assert (entry.consumed_at, entry.pending_at) == (None, None)
    assert entry.last_reason == "claimed"
    assert (entry.approver_id, entry.approval_event_id, entry.approved_at) == (
        APPROVER_ID,
        2,
        T_APPROVED,
    )
    assert tmp_state.load().last_completed_cycle_at == CYCLE_NOW


def test_a_marker_edited_after_the_approval_still_claims__ac5_fr009(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(
        9,
        markers=[_mark(T_APPROVED - timedelta(minutes=1), updated_at=_T_MARK)],
    )
    res, deps = _run(tmp_path, tmp_state, world)
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "claimed")]
    assert deps.launcher.calls == []


@pytest.mark.parametrize(
    ("marker", "claimed"),
    [
        (_mark(T_APPROVED + timedelta(seconds=1)), True),
        (_mark(T_APPROVED), False),
        (_mark(T_APPROVED - timedelta(seconds=1)), False),
        (_mark(_T_MARK, login="other-user"), False),
        (_mark(_T_MARK, marker=False), False),
    ],
    ids=[
        "one_second_after",
        "at_the_approval_second",
        "before_the_approval",
        "another_author",
        "no_marker_text",
    ],
)
def test_the_marker_must_be_own_and_strictly_after_the_approval__ac5_fr009(
    tmp_path, tmp_state, gh_world, marker, claimed
):
    world = gh_world()
    world.issue(9, markers=[marker])
    res, deps = _run(tmp_path, tmp_state, world)
    expected = "claimed" if claimed else "launched"
    assert _decisions(_lines_of(tmp_state, res)) == [(9, expected)]
    assert len(deps.launcher.calls) == (0 if claimed else 1)
    assert _entry(tmp_state, 9).state == expected


@pytest.mark.parametrize(
    ("kind", "marker_at", "claimed"),
    [
        ("launched", _PENDING_AT + timedelta(minutes=1), True),
        ("launched", _PENDING_AT - timedelta(seconds=300), True),
        ("launched", _PENDING_AT - timedelta(seconds=301), False),
        ("unknown", _PENDING_AT + timedelta(minutes=1), True),
        ("unknown", _PENDING_AT - timedelta(seconds=301), False),
        ("spawn_error", _PENDING_AT + timedelta(minutes=1), True),
        ("spawn_error", _PENDING_AT - timedelta(seconds=301), False),
    ],
)
def test_a_marker_after_pending_at_claims_a_dispatched_entry__ac5_fr009(
    tmp_path, tmp_state, gh_world, kind, marker_at, claimed
):
    world = gh_world()
    world.issue(9, markers=[_mark(marker_at)])
    seeded = _seed(tmp_state, 9, kind, _PENDING_AT)
    res, deps = _run(tmp_path, tmp_state, world)
    lines = _lines_of(tmp_state, res)
    assert deps.launcher.calls == []
    assert _reads(world, 9) == ["comments"]
    entry = _entry(tmp_state, 9)
    if not claimed:
        assert _decisions(lines) == [(9, "already_dispatched")]
        assert entry == seeded  # an older marker leaves the state alone
        return
    (decision,) = _of_kind(lines, "decision")
    assert (decision["reason"], decision["state"]) == ("claimed", "claimed")
    assert entry == replace(
        seeded, state="claimed", updated_at=CYCLE_NOW, last_reason="claimed"
    )
    assert (entry.launches, entry.consumed_at) == (1, _PENDING_AT)  # kept


@pytest.mark.parametrize("age", [timedelta(minutes=30), timedelta(minutes=1)])
def test_a_failed_entry_with_a_marker_after_the_approval_becomes_claimed__ac5_fr009(
    tmp_path, tmp_state, gh_world, age
):
    world = gh_world()
    world.issue(9, markers=[_mark(_T_MARK)])
    _seed(tmp_state, 9, "failed", CYCLE_NOW - age)
    res, deps = _run(tmp_path, tmp_state, world)
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "claimed")]
    assert _reads(world, 9) == ["comments", "events"]
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.attempts, entry.launches) == ("claimed", 1, 0)
    assert (entry.consumed_at, entry.pending_at) == (None, None)
    assert (entry.approver_id, entry.approval_event_id, entry.approved_at) == (
        APPROVER_ID,
        2,
        T_APPROVED,
    )
    assert deps.launcher.calls == []


# ==============================================================================
# Tombstones: an abandoned entry with no pending_at (attempts_exhausted)
# ==============================================================================


def test_a_tombstone_with_an_own_marker_after_the_approval_becomes_claimed__df43(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9, markers=[_mark(_T_MARK)])
    seeded = _seed(tmp_state, 9, "exhausted", CYCLE_NOW - timedelta(hours=2))
    assert (seeded.state, seeded.last_reason) == ("abandoned", "attempts_exhausted")
    res, deps = _run(tmp_path, tmp_state, world)
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["reason"], decision["state"]) == ("claimed", "claimed")
    assert _reads(world, 9) == ["comments", "events"]
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.attempts, entry.launches) == ("claimed", 3, 0)
    assert (entry.consumed_at, entry.last_reason) == (None, "claimed")
    assert (entry.approver_id, entry.approval_event_id, entry.approved_at) == (
        APPROVER_ID,
        2,
        T_APPROVED,
    )
    assert deps.launcher.calls == []


@pytest.mark.parametrize(
    ("build", "reason", "reads"),
    [
        pytest.param(
            lambda w: w.issue(9, events=_ev(w, approval=None)),
            "already_dispatched",
            ["comments", "events"],
            id="no_approval_can_be_established",
        ),
        pytest.param(
            lambda w: w.issue(9).fail("events", "failed", n=9),
            "already_dispatched",
            ["comments", "events"],
            id="events_unreadable",
        ),
        pytest.param(
            lambda w: w.issue(9),
            "already_dispatched",
            ["comments", "events"],
            id="approved_but_no_marker",
        ),
        pytest.param(
            lambda w: w.issue(9, markers=[_mark(T_APPROVED)]),
            "already_dispatched",
            ["comments", "events"],
            id="marker_at_the_approval_second",
        ),
        pytest.param(
            lambda w: w.issue(9).fail("comments", "failed", n=9),
            "marker_unreadable",
            ["comments"],
            id="marker_unreadable",
        ),
    ],
)
def test_a_tombstone_without_a_claim_is_skipped_and_never_raises__df43(
    tmp_path, tmp_state, gh_world, build, reason, reads
):
    world = gh_world()
    build(world)
    seeded = _seed(tmp_state, 9, "exhausted", CYCLE_NOW - timedelta(hours=2))
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, reason)]
    assert _reads(world, 9) == reads
    assert _entry(tmp_state, 9) == seeded
    assert deps.launcher.calls == []


# ==============================================================================
# DF-47: entries are keyed by issue number, not by login
# ==============================================================================


@pytest.mark.parametrize("kind", ["launched", "unknown", "spawn_error"])
def test_an_entry_of_another_login_is_not_launched_again__df47_nfr005(
    tmp_path, tmp_state, gh_world, kind
):
    world = gh_world()  # discovery now runs under OWN_LOGIN
    world.issue(9)
    seeded = _seed(tmp_state, 9, kind, _PENDING_AT, login=_OLD_LOGIN)
    assert seeded.launch_login == _OLD_LOGIN
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "already_dispatched")]
    assert deps.launcher.calls == []
    assert not _probed(world)
    assert _entry(tmp_state, 9) == seeded  # still names the first login


# ==============================================================================
# FR-010 and FR-014: the launch steps, in order
# ==============================================================================


def test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_fr014(
    tmp_path, tmp_state, gh_world
):
    """AC-6, FR-010, FR-014: pending with launches 1 is saved before the launch."""
    world = gh_world()
    world.issue(9)
    stored_at_origin: list[dict] = []
    world.on("origin", lambda: stored_at_origin.append(dict(tmp_state.load().entries)))
    seen: list[tuple[dict, int]] = []

    def peek():
        raw = json.loads((tmp_state.state_dir / "dispatch.json").read_text("utf-8"))
        seen.append((raw["entries"], len(world.runner.calls)))

    launcher = FakeLauncher([launched_outcome()], on_call=peek)
    res, deps = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (res.exit_code, res.launched_issue) == (0, 9)
    assert _trace(world) == _LAUNCH_TRACE
    # Both origin checks (cycle start and just before pending) saw no entry yet.
    assert stored_at_origin == [{}, {}]
    # Every read and probe call is done when the launch call starts.
    ((entries, calls_at_launch),) = seen
    assert calls_at_launch == len(_LAUNCH_TRACE)
    assert entries == {
        "9": {
            "issue": 9,
            "state": "pending",
            "attempts": 0,
            "launches": 1,
            "operation_id": None,
            "approver_id": APPROVER_ID,
            "approval_event_id": 2,
            "approved_at": "2026-11-07T12:02:00Z",
            "launch_cwd": str(world.config.worktree),
            "launch_login": OWN_LOGIN,
            "launch_account_id": OWN_ID,
            "consumed_at": _SHADOW_AT,
            "pending_at": _SHADOW_AT,
            "created_at": _SHADOW_AT,
            "updated_at": _SHADOW_AT,
            "lease_expires_at": None,
            "last_reason": None,
        }
    }
    assert launcher.calls == [(ORCA_PATH, str(world.config.worktree), _CLAIM_9, 120.0)]
    assert world.runner.timeouts[_LAUNCH_TRACE.index("probe")] == 10.0
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.operation_id, entry.launches) == (
        "launched",
        "op-test-0001",
        1,
    )
    assert entry.lease_expires_at == CYCLE_NOW + timedelta(minutes=60)
    assert entry.last_reason == "launched"
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["reason"], decision["state"]) == ("launched", "launched")
    assert (decision["approver_id"], decision["approval_event_id"]) == (APPROVER_ID, 2)
    assert _the_cycle_line(lines)["gh_calls"] == 9
    assert tmp_state.load().last_completed_cycle_at == CYCLE_NOW


_UNKNOWN_OUTCOMES = [
    pytest.param(
        lambda: cycle.launch.outcome_of(command_result(timed_out=True)),
        None,
        id="timeout",
    ),
    pytest.param(
        lambda: cycle.launch.outcome_of(command_result(stdout="not json")),
        None,
        id="non_json",
    ),
    pytest.param(
        lambda: cycle.launch.outcome_of(command_result(returncode=1)),
        None,
        id="non_zero_exit",
    ),
    # Both Orca replies come from `_assumed_shape` fixtures (design 8.4, DF-32);
    # test_launch.py pins where each fixture holds, or lacks, its id.
    pytest.param(
        lambda: cycle.launch.outcome_of(
            command_result(
                stdout=json.dumps(
                    load_fixture("orca_launch_no_operation_id.json")["payload"]
                )
            )
        ),
        None,
        id="no_operation_id",
    ),
    pytest.param(
        lambda: cycle.launch.outcome_of(
            command_result(
                stdout=json.dumps(
                    load_fixture("orca_launch_empty_operation_id.json")["payload"]
                )
            )
        ),
        None,
        id="empty_operation_id",
    ),
    pytest.param(unknown_outcome, "op-test-0001", id="agent_session_operation_unknown"),
]


@pytest.mark.parametrize(("outcome", "operation_id"), _UNKNOWN_OUTCOMES)
def test_an_unknown_launch_outcome_is_exit_7_and_consumes_the_slot__fr014(
    tmp_path, tmp_state, gh_world, outcome, operation_id
):
    world = gh_world()
    world.issue(9)
    pending_seen: list[dict] = []

    def peek():
        raw = json.loads((tmp_state.state_dir / "dispatch.json").read_text("utf-8"))
        pending_seen.append(raw["entries"]["9"])

    launcher = FakeLauncher([outcome()], on_call=peek)
    res, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (res.exit_code, res.reason, res.launched_issue) == (
        7,
        "launch_unknown",
        None,
    )
    assert len(launcher.calls) == 1
    assert [(p["state"], p["launches"]) for p in pending_seen] == [("pending", 1)]
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.launches, entry.attempts) == ("unknown", 1, 0)
    assert entry.operation_id == operation_id
    assert entry.last_reason == "launch_unknown"
    assert (entry.consumed_at, entry.pending_at) == (CYCLE_NOW, CYCLE_NOW)
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["reason"], decision["state"]) == ("launch_unknown", "unknown")
    cycle_line = _the_cycle_line(lines)
    assert (cycle_line["exit"], cycle_line["reason"]) == (7, "launch_unknown")
    assert tmp_state.load().last_completed_cycle_at is None  # exit 7 is no health stamp


def test_a_spawn_error_is_abandoned_spawn_error_and_exit_7__fr014(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    launcher = FakeLauncher([spawn_error_outcome()])
    res, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (res.exit_code, res.reason, res.launched_issue) == (7, "spawn_error", None)
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.launches, entry.last_reason) == (
        "abandoned",
        1,
        "spawn_error",
    )
    assert entry.operation_id is None
    assert entry.pending_at == CYCLE_NOW
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["reason"], decision["state"]) == ("spawn_error", "abandoned")
    assert _the_cycle_line(lines)["exit"] == 7


@pytest.mark.parametrize("how", ["non_json", "timeout", "failed"])
def test_a_failing_probe_is_exit_2_orca_not_found_and_writes_no_entry__fr013_fr014(
    tmp_path, tmp_state, gh_world, how
):
    world = gh_world()
    world.issue(9)
    world.fail("probe", how)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (2, "orca_not_found")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == []  # the stopping candidate has no decision line (C-2)
    assert _reads(world, 9) == _FULL_READS  # the probe comes after the GitHub checks
    assert _trace(world)[-1] == "probe"
    assert deps.launcher.calls == []
    stored = tmp_state.load()
    assert stored.entries == {}
    assert dict(stored.considered) == {9: CYCLE_NOW}  # a launch-step stop still stamps
    assert stored.last_completed_cycle_at is None
    cycle_line = _the_cycle_line(lines)
    assert (cycle_line["exit"], cycle_line["reason"]) == (2, "orca_not_found")


def test_no_orca_cli_on_the_path_is_exit_2_without_a_probe_call__fr013(
    tmp_path, tmp_state, gh_world
):
    world = gh_world(which=lambda name: None)
    world.issue(9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (2, "orca_not_found")
    assert not _probed(world)
    assert _trace(world)[-1] == "items:9"
    assert deps.launcher.calls == []
    assert tmp_state.load().entries == {}


def test_a_prompt_value_error_writes_failed_prompt_invalid__fr012_fr014(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    def refuse(n):
        raise ValueError("no prompt")

    monkeypatch.setattr(cycle.launch, "build_claim_prompt", refuse)
    world = gh_world()
    world.issue(9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (7, "prompt_invalid")
    assert deps.launcher.calls == []
    assert _trace(world)[-1] == "probe"  # the prompt build precedes the re-read
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.attempts, entry.launches) == ("failed", 1, 0)
    assert (entry.consumed_at, entry.pending_at) == (None, None)
    assert (entry.last_reason, entry.updated_at) == ("prompt_invalid", CYCLE_NOW)
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["reason"], decision["state"]) == ("prompt_invalid", "failed")
    assert _the_cycle_line(lines)["exit"] == 7


def test_the_launch_steps_stop_at_the_first_launch_outcome__fr016_s1(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.issue(10)
    launcher = FakeLauncher([unknown_outcome()])
    res, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert res.exit_code == 7
    assert _touched(world) == {9}  # issue 10 is neither read nor stamped
    assert dict(tmp_state.load().considered) == {9: CYCLE_NOW}
    assert _entry(tmp_state, 10) is None


# ==============================================================================
# FR-011: the re-read just before the pending write
# ==============================================================================


@pytest.mark.parametrize(
    "reread",
    [
        {"state": "closed"},
        {"state": ""},
        {"labels": [cycle.DEFAULT_APPROVAL_LABEL]},
        {"labels": [cycle.DEFAULT_TRIGGER_LABEL]},
        {"labels": []},
    ],
    ids=[
        "closed",
        "empty_state",
        "trigger_label_gone",
        "approval_label_gone",
        "no_label",
    ],
)
def test_a_re_read_that_is_not_open_and_labelled_gives_revalidation_failed__fr011(
    tmp_path, tmp_state, gh_world, reread
):
    world = gh_world()
    world.issue(9, reread=reread)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(9, "revalidation_failed")]
    assert "state" not in _of_kind(lines, "decision")[0]
    assert _trace(world)[-2:] == ["probe", "reread:9"]  # nothing after the re-read
    assert deps.launcher.calls == []
    stored = tmp_state.load()
    assert stored.entries == {}
    assert dict(stored.considered) == {9: CYCLE_NOW}
    assert stored.last_completed_cycle_at == CYCLE_NOW


def test_an_open_state_in_capitals_still_launches__fr011(tmp_path, tmp_state, gh_world):
    world = gh_world()
    world.issue(9, reread={"state": "OPEN"})
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.launched_issue) == (0, 9)
    assert len(deps.launcher.calls) == 1


@pytest.mark.parametrize(
    ("assignees", "reason"),
    [
        ([OWN_LOGIN, "other-user"], "assigned_other"),
        ([], "unassigned"),
        (["other-user"], "assigned_other"),
    ],
)
def test_a_re_read_with_another_assignee_set_skips_that_reason__fr008_fr011(
    tmp_path, tmp_state, gh_world, assignees, reason
):
    world = gh_world()
    world.issue(9, reread={"assignees": assignees})
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(9, reason)]
    assert "state" not in _of_kind(lines, "decision")[0]
    assert _trace(world)[-2:] == ["probe", "reread:9"]
    assert deps.launcher.calls == []
    assert tmp_state.load().entries == {}


@pytest.mark.parametrize("how", ["timeout", "transient"])
def test_a_transient_re_read_failure_writes_failed_and_exit_7__fr011_fr014(
    tmp_path, tmp_state, gh_world, how
):
    world = gh_world()
    world.issue(9)
    world.issue(10)
    world.fail("reread", how, n=9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (7, "revalidation_transient")
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["issue"], decision["reason"], decision["state"]) == (
        9,
        "revalidation_transient",
        "failed",
    )
    entry = _entry(tmp_state, 9)
    assert (entry.state, entry.launches, entry.attempts) == ("failed", 0, 1)
    assert (entry.consumed_at, entry.pending_at) == (None, None)
    assert (entry.last_reason, entry.updated_at) == (
        "revalidation_transient",
        CYCLE_NOW,
    )
    assert deps.launcher.calls == []
    assert _touched(world) == {9}  # the launch step ended the cycle
    assert _trace(world)[-2:] == ["probe", "reread:9"]
    assert tmp_state.load().last_completed_cycle_at is None


@pytest.mark.parametrize("how", ["failed", "non_json", "auth"])
def test_a_permanent_re_read_failure_skips_without_an_entry__fr011(
    tmp_path, tmp_state, gh_world, how
):
    """AC-6, FR-011: a permanent re-read failure skips and writes no entry."""
    world = gh_world()
    world.issue(9)
    world.fail("reread", how, n=9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "revalidation_failed")]
    assert tmp_state.load().entries == {}
    assert deps.launcher.calls == []


def test_a_rate_limited_re_read_clamps_for_an_hour_and_writes_no_entry__fr011_fr028(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.fail("reread", "rate", n=9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (5, "rate_limit_clamped")
    assert _decisions(_lines_of(tmp_state, res)) == []  # the cycle line carries it
    stored = tmp_state.load()
    assert stored.next_permitted_at == CYCLE_NOW + timedelta(seconds=3600)
    assert stored.entries == {}
    assert deps.launcher.calls == []


def _unlabel_approval(world):
    cfg = world.config
    return label_event(
        3,
        "unlabeled",
        cfg.approval_label,
        _T_MARK,
        actor_id=APPROVER_ID,
        actor_login=OWN_LOGIN,
    )


def _relabel_approval(world):
    cfg = world.config
    return label_event(
        4,
        "labeled",
        cfg.approval_label,
        _T_MARK + timedelta(minutes=1),
        actor_id=APPROVER_ID,
        actor_login=OWN_LOGIN,
    )


def test_an_approval_voided_by_the_re_read_gives_revalidation_failed__fr011(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _on_nth(
        world,
        "events",
        9,
        2,  # the second events read is the re-read
        lambda: world.update(9, events=[*_ev(world), _unlabel_approval(world)]),
    )
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "revalidation_failed")]
    assert _trace(world)[-2:] == ["reread:9", "events:9"]
    assert tmp_state.load().entries == {}
    assert deps.launcher.calls == []


def test_a_newer_approval_found_by_the_re_read_gives_revalidation_failed__fr011(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    newer = [*_ev(world), _unlabel_approval(world), _relabel_approval(world)]
    _on_nth(world, "events", 9, 2, lambda: world.update(9, events=newer))
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "revalidation_failed")]
    assert _trace(world)[-2:] == ["reread:9", "events:9"]
    assert tmp_state.load().entries == {}
    assert deps.launcher.calls == []


def test_a_project_item_moved_out_of_backlog_by_the_re_read_fails__fr011(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _on_nth(
        world,
        "items",
        9,
        2,  # the second items read is the re-read
        lambda: world.update(9, items=[{"status": "In progress"}]),
    )
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "revalidation_failed")]
    assert _trace(world)[-3:] == ["reread:9", "events:9", "items:9"]
    assert tmp_state.load().entries == {}
    assert deps.launcher.calls == []


def test_a_refused_reserved_call_gives_budget_exhausted_and_no_entry__fr011_nfr009(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issues_from(range(1, 8), items=[{"status": "In progress"}])  # 7 x 4 = 28
    world.issue(8)
    padding = [
        label_event(
            100 + i,
            "labeled",
            "padding",
            FIXED_NOW + timedelta(seconds=10 + i % 30),
            actor_id=2001,
            actor_login="issue-author",
        )
        for i in range(99)
    ]
    # The re-read's events call now needs a second page: 33, 34, 35, then refused.
    _on_nth(
        world,
        "events",
        8,
        2,
        lambda: world.update(8, events=[*padding, *_ev(world)]),
    )
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines)[-1] == (8, "budget_exhausted")
    assert "state" not in _of_kind(lines, "decision")[-1]
    shared = ("user", "discover", "origin", "probe")
    per_issue = [t for t in _trace(world) if t not in shared]
    assert len(per_issue) == github.CALL_CAP
    assert _trace(world)[-1] == "events:8"  # the items re-read was refused
    assert _the_cycle_line(lines)["gh_calls"] == github.CALL_CAP + 2
    stored = tmp_state.load()
    assert stored.entries == {}
    assert sorted(stored.considered) == list(range(1, 8))  # 8 is not stamped
    assert deps.launcher.calls == []


# ==============================================================================
# FR-018 and FR-025 between discovery and the pending write
# ==============================================================================

_OLD_HEALTH = CYCLE_NOW - timedelta(minutes=5)


def test_disabled_created_after_discovery_stops_with_disabled_mid_cycle__fr018_fr014(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.issue(10)
    _seed_doc(tmp_state, last_completed_cycle_at=_OLD_HEALTH)
    world.on(
        "reread",
        lambda: (tmp_state.state_dir / "DISABLED").write_text("", encoding="utf-8"),
        n=9,
    )
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason, res.launched_issue) == (
        0,
        "disabled_mid_cycle",
        None,
    )
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == []  # the stopping candidate has no decision line
    cycle_line = _the_cycle_line(lines)
    assert (cycle_line["exit"], cycle_line["reason"]) == (0, "disabled_mid_cycle")
    assert deps.launcher.calls == []
    assert _trace(world)[-1] == "items:9"  # DISABLED is read before the origin re-check
    assert _trace(world).count("origin") == 1
    stored = tmp_state.load()
    assert stored.entries == {}
    assert dict(stored.considered) == {9: CYCLE_NOW}  # stamped, issue 10 never reached
    # No health refresh: a mid-cycle disable is not a completed cycle (step 14).
    assert stored.last_completed_cycle_at == _OLD_HEALTH


def test_disabled_mid_cycle_with_no_health_stamp_yet_leaves_it_empty__fr021(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.on(
        "reread",
        lambda: (tmp_state.state_dir / "DISABLED").write_text("", encoding="utf-8"),
        n=9,
    )
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.reason == "disabled_mid_cycle"
    assert tmp_state.load().last_completed_cycle_at is None


def test_an_origin_that_changes_before_the_pending_write_is_exit_2__fr025_fr014(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.issue(10)
    _seed_doc(tmp_state, last_completed_cycle_at=_OLD_HEALTH)

    def move_origin():
        world.origin_url = FOREIGN_ORIGIN_URL

    world.on("reread", move_origin, n=9)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (2, "origin_mismatch")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == []  # the stopping candidate has no decision line
    assert _trace(world)[-3:] == ["events:9", "items:9", "origin"]
    assert _trace(world).count("origin") == 2
    assert deps.launcher.calls == []
    stored = tmp_state.load()
    assert stored.entries == {}
    assert dict(stored.considered) == {9: CYCLE_NOW}
    assert stored.last_completed_cycle_at == _OLD_HEALTH


# ==============================================================================
# S1 (decision DF-50): FR-016 examines k per cycle when every candidate skips,
# and one only when a candidate launches
# ==============================================================================


def test_s1_case_a_fifteen_skipping_issues_examine_k_then_the_rest__fr016_df50(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issues_from(range(1, 16), items=[{"status": "In progress"}])  # r = 4
    launcher = FakeLauncher()
    res1, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines1 = _lines_of(tmp_state, res1)
    k = min(10, (github.CALL_CAP - github.RESERVED_CALLS) // 4)
    assert k == 8
    assert _decisions(lines1) == [
        *[(n, "project_mismatch") for n in range(1, k + 1)],
        (9, "budget_exhausted"),
        (10, "budget_exhausted"),
    ]
    assert _the_cycle_line(lines1)["gh_calls"] == 2 + 32
    t0 = CYCLE_NOW
    stored = tmp_state.load()
    assert dict(stored.considered) == {n: t0 for n in range(1, 9)}  # 9, 10 unstamped

    world.clock.advance(60)
    t1 = world.clock.now()
    res2, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines2 = _lines_of(tmp_state, res2)
    # Cycle 2 starts with the 7 never-examined issues, then the oldest examined.
    assert _decisions(lines2) == [
        *[(n, "project_mismatch") for n in range(9, 16)],
        (1, "project_mismatch"),
        (2, "budget_exhausted"),
        (3, "budget_exhausted"),
    ]
    assert dict(tmp_state.load().considered) == {
        **{n: t0 for n in range(2, 9)},
        **{n: t1 for n in (*range(9, 16), 1)},
    }
    assert launcher.calls == []
    assert tmp_state.load().entries == {}


def test_s1_case_b_fifteen_eligible_issues_examine_and_launch_exactly_one__fr016_df50(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issues_from(range(1, 16))
    launcher = FakeLauncher(
        lambda i: cycle.launch.LaunchOutcome("launched", f"op-s1-{i:04d}", "ok")
    )
    res1, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines1 = _lines_of(tmp_state, res1)
    assert (res1.exit_code, res1.launched_issue) == (0, 1)
    assert _decisions(lines1) == [(1, "launched")]
    assert [c[2] for c in launcher.calls] == ["/sc:issue --claim 1"]
    assert _touched(world) == {1}  # later candidates are neither read ...
    stored = tmp_state.load()
    assert dict(stored.considered) == {1: CYCLE_NOW}  # ... nor stamped
    assert sorted(stored.entries) == [1]
    assert _the_cycle_line(lines1)["gh_calls"] == 9

    world.clock.advance(60)
    res2, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert _decisions(_lines_of(tmp_state, res2)) == [(2, "launched")]
    assert [c[2] for c in launcher.calls] == [
        "/sc:issue --claim 1",
        "/sc:issue --claim 2",
    ]
    assert sorted(tmp_state.load().entries) == [1, 2]
    assert dict(tmp_state.load().considered) == {
        1: CYCLE_NOW,
        2: CYCLE_NOW + timedelta(seconds=60),
    }


# ==============================================================================
# FR-023: the considered map
# ==============================================================================

_T_OLD = CYCLE_NOW - timedelta(hours=3)
_T1 = CYCLE_NOW - timedelta(hours=2)
_T2 = CYCLE_NOW - timedelta(hours=1)


@pytest.mark.parametrize(
    ("considered", "order"),
    [
        ({6: _T_OLD, 7: _T1, 8: _T2}, [9, 7, 8]),
        ({6: _T_OLD, 7: _T2, 8: _T1}, [9, 8, 7]),
    ],
    ids=["seven_older", "eight_older"],
)
def test_candidates_are_new_first_then_oldest_and_the_map_is_stamped_and_pruned__fr023(
    tmp_path, tmp_state, gh_world, considered, order
):
    world = gh_world()
    for n in (7, 8, 9):
        world.issue(n, assignees=["other-user"])  # a local skip: examined, no read
    _seed_doc(tmp_state, considered=considered)
    res, _ = _run(tmp_path, tmp_state, world)
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(n, "assigned_other") for n in order]
    # Every examined issue holds the cycle time; 6 is no longer discovered.
    assert dict(tmp_state.load().considered) == {
        7: CYCLE_NOW,
        8: CYCLE_NOW,
        9: CYCLE_NOW,
    }


def test_an_issue_that_was_not_examined_keeps_its_old_stamp__fr023(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(7, assignees=["other-user"])
    world.issue(8, assignees=["other-user"])
    world.issue(9)
    _seed_doc(tmp_state, considered={6: _T_OLD, 7: _T1, 8: _T2})
    res, _ = _run(tmp_path, tmp_state, world)
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "launched")]
    assert dict(tmp_state.load().considered) == {7: _T1, 8: _T2, 9: CYCLE_NOW}


def test_an_idle_cycle_does_not_prune_the_considered_map__fr023(
    tmp_path, tmp_state, gh_world
):
    """FR-023, design step 13: `considered` is written only if something was examined."""
    world = gh_world()  # discovery returns no issue at all
    _seed_doc(tmp_state, considered={5: _T1, 6: _T_OLD})
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert _decisions(_lines_of(tmp_state, res)) == []
    stored = tmp_state.load()
    assert stored.last_completed_cycle_at == CYCLE_NOW  # the cycle did save
    assert dict(stored.considered) == {5: _T1, 6: _T_OLD}


def test_a_saving_cycle_prunes_the_consumed_log__design_7_5(
    tmp_path, tmp_state, gh_world
):
    """Design 7.5: `consumed_log` is pruned in every saving cycle (t <= now - 24 h)."""
    edge = CYCLE_NOW - timedelta(hours=24)
    kept = edge + timedelta(seconds=1)
    _seed_doc(tmp_state, consumed_log=(edge, kept))
    assert tuple(tmp_state.load().consumed_log) == (edge, kept)  # the seed holds both
    res, _ = _run(tmp_path, tmp_state, gh_world())
    assert res.exit_code == 0
    stored = tmp_state.load()
    assert stored.last_completed_cycle_at == CYCLE_NOW  # the cycle did save
    assert tuple(stored.consumed_log) == (kept,)


def test_an_all_budget_exhausted_cycle_does_not_prune_the_considered_map__fr023(
    tmp_path, tmp_state, gh_world
):
    """FR-023: a cycle whose only candidate is budget_exhausted examined nothing."""
    world = gh_world()
    world.issue(9)
    world.on("discover", lambda: world.clock.advance(236))
    _seed_doc(tmp_state, considered={5: _T1})  # 5 is not in the discovery set
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    (decision,) = _of_kind(_audit_lines(tmp_state), "decision")
    assert (decision["issue"], decision["reason"]) == (9, "budget_exhausted")
    assert dict(tmp_state.load().considered) == {5: _T1}


def test_a_dry_run_leaves_the_considered_map_byte_identical__fr023_fr019(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    for n in (7, 8, 9):
        world.issue(n, assignees=["other-user"])
    _seed_doc(tmp_state, considered={6: _T_OLD, 7: _T1, 8: _T2})
    store_file = tmp_state.state_dir / "dispatch.json"
    before = store_file.read_bytes()
    res, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    assert store_file.read_bytes() == before  # 6 not pruned, nothing stamped
    # The shadow map starts empty: new issues in number order, not the real map.
    assert _decisions(_lines_of(tmp_state, res)) == [
        (7, "assigned_other"),
        (8, "assigned_other"),
        (9, "assigned_other"),
    ]
    shadow = json.loads((tmp_state.state_dir / "dry-run.json").read_text("utf-8"))
    assert shadow["considered"] == {n: _SHADOW_AT for n in ("7", "8", "9")}


# ==============================================================================
# FR-019: dry-run
# ==============================================================================


def test_a_dry_run_reports_would_launch_and_writes_nothing_but_the_shadow__fr019(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    store_file = tmp_state.state_dir / "dispatch.json"
    before = store_file.read_bytes()
    res, deps = _run(tmp_path, tmp_state, world, dry_run=True)
    assert (res.exit_code, res.would_launch, res.launched_issue) == (0, 9, None)
    assert res.probe == "skipped"
    assert deps.launcher.calls == []
    assert not _probed(world)
    assert all(argv[0] != ORCA_PATH for argv, _ in world.runner.calls)
    # The read steps run, the re-read and the second origin check do not.
    assert _trace(world) == [
        "user",
        "origin",
        "discover",
        "comments:9",
        "events:9",
        "edits:9",
        "items:9",
    ]
    assert store_file.read_bytes() == before
    lines = _lines_of(tmp_state, res)
    (decision,) = _of_kind(lines, "decision")
    assert decision == {
        "kind": "decision",
        "ts": _SHADOW_AT,
        "host": "test-host",
        "login": OWN_LOGIN,
        "cycle_id": res.cycle_id,
        "dry_run": True,
        "reason": "launched",
        "issue": 9,
        "approver_id": APPROVER_ID,
        "approval_event_id": 2,
        "approved_at": "2026-11-07T12:02:00Z",
    }
    cycle_line = _the_cycle_line(lines)
    assert (cycle_line["dry_run"], cycle_line["exit"], cycle_line["gh_calls"]) == (
        True,
        0,
        6,
    )
    shadow = json.loads((tmp_state.state_dir / "dry-run.json").read_text("utf-8"))
    assert shadow == {
        "schema_version": 1,
        "considered": {"9": _SHADOW_AT},
        "shadow_launches": [_SHADOW_AT],
    }
    assert tmp_state.load().last_completed_cycle_at is None  # no health stamp


def test_a_dry_run_runs_with_enabled_false__fr019_fr027(tmp_path, tmp_state, gh_world):
    world = gh_world(config=make_config(tmp_path, enabled=False))
    world.issue(9)
    res, deps = _run(tmp_path, tmp_state, world, dry_run=True)
    assert (res.exit_code, res.would_launch) == (0, 9)
    assert deps.launcher.calls == []


def test_a_dry_run_reports_orphans_and_leaves_the_store_unchanged__fr019_fr011(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    _seed(tmp_state, 5, "pending", CYCLE_NOW - timedelta(minutes=5))
    _seed(tmp_state, 6, "launched", CYCLE_NOW - timedelta(hours=2))
    store_file = tmp_state.state_dir / "dispatch.json"
    before = store_file.read_bytes()
    res, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(5, "pending_orphan"), (6, "claim_not_observed")]
    assert all("state" not in d and d["dry_run"] for d in _of_kind(lines, "decision"))
    assert store_file.read_bytes() == before
    assert not (tmp_state.state_dir / "dry-run.json").exists()  # nothing examined

    # The same store, run for real: now the sweep is written.
    world.clock.advance(1)
    real, _ = _run(tmp_path, tmp_state, world)
    real_lines = _lines_of(tmp_state, real)
    assert [
        (d["issue"], d["reason"], d["state"]) for d in _of_kind(real_lines, "decision")
    ] == [(5, "pending_orphan", "abandoned"), (6, "claim_not_observed", "abandoned")]
    assert _entry(tmp_state, 5).state == "abandoned"
    assert _entry(tmp_state, 6).last_reason == "claim_not_observed"


def test_an_unparseable_shadow_file_is_replaced_with_one_warning__fr019_df22(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    shadow_file = tmp_state.state_dir / "dry-run.json"
    shadow_file.write_bytes(b"{not json")
    res, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    lines = _lines_of(tmp_state, res)
    warnings = _of_kind(lines, "warning")
    assert len(warnings) == 1
    assert (warnings[0]["reason"], warnings[0]["dry_run"]) == (
        "dry_run_shadow_reset",
        True,
    )
    assert warnings[0]["login"] == OWN_LOGIN
    assert [ln["kind"] for ln in lines] == ["warning", "decision", "cycle"]
    assert json.loads(shadow_file.read_text("utf-8")) == {
        "schema_version": 1,
        "considered": {"9": _SHADOW_AT},  # an empty shadow plus this cycle
        "shadow_launches": [_SHADOW_AT],
    }


def test_the_unparseable_shadow_is_replaced_even_when_nothing_was_examined__df22(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    shadow_file = tmp_state.state_dir / "dry-run.json"
    shadow_file.write_bytes(b"[]")
    res, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    lines = _lines_of(tmp_state, res)
    assert [(ln["kind"], ln["reason"]) for ln in _of_kind(lines, "warning")] == [
        ("warning", "dry_run_shadow_reset")
    ]
    assert json.loads(shadow_file.read_text("utf-8")) == {
        "schema_version": 1,
        "considered": {},
        "shadow_launches": [],
    }


def test_a_missing_or_valid_shadow_gives_no_warning__df22(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    first, _ = _run(tmp_path, tmp_state, world, dry_run=True)  # no file yet
    assert _of_kind(_lines_of(tmp_state, first), "warning") == []
    world.clock.advance(60)
    second, _ = _run(tmp_path, tmp_state, world, dry_run=True)  # a valid file
    assert _of_kind(_lines_of(tmp_state, second), "warning") == []


def test_a_real_cycle_never_opens_the_shadow_file__fr019(tmp_path, tmp_state, gh_world):
    world = gh_world()
    shadow_file = tmp_state.state_dir / "dry-run.json"
    shadow_file.write_bytes(b"{not json")
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.exit_code == 0
    assert _of_kind(_lines_of(tmp_state, res), "warning") == []
    assert shadow_file.read_bytes() == b"{not json"


@pytest.mark.parametrize(
    ("call", "how", "reason"),
    [
        ("user", "rate", "rate_limited"),
        ("discover", "rate", "rate_limit_clamped"),
        ("events", "rate", "rate_limit_clamped"),
    ],
)
def test_a_dry_run_never_persists_a_rate_limit__fr019_fr028(
    tmp_path, tmp_state, gh_world, call, how, reason
):
    world = gh_world()
    world.issue(9)
    world.fail(call, how, n=9 if call == "events" else None)
    store_file = tmp_state.state_dir / "dispatch.json"
    before = store_file.read_bytes()
    res, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    assert (res.exit_code, res.reason) == (5, reason)
    assert store_file.read_bytes() == before
    assert tmp_state.load().next_permitted_at is None
    assert not (tmp_state.state_dir / "dry-run.json").exists()


def test_a_dry_run_honours_a_persisted_next_permitted_time__fr019_fr028(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _seed_doc(tmp_state, next_permitted_at=CYCLE_NOW + timedelta(seconds=120))
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    res, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    assert (res.exit_code, res.reason) == (5, "rate_limited")
    assert world.runner.calls == []
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before


def test_a_dry_run_shadow_rotates_and_simulates_the_day_cap__fr019_fr024(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issues_from(range(1, 8))
    store_file = tmp_state.state_dir / "dispatch.json"
    before = store_file.read_bytes()
    t0 = CYCLE_NOW
    would = []
    for _ in range(7):
        res, deps = _run(tmp_path, tmp_state, world, dry_run=True)
        would.append(res.would_launch)
        assert deps.launcher.calls == []
        world.clock.advance(60)
    assert would == [1, 2, 3, 4, 5, 6, None]  # the 7th is the day cap
    assert store_file.read_bytes() == before
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [(n, "day_cap") for n in (7, 1, 2, 3, 4, 5, 6)]
    shadow = json.loads((tmp_state.state_dir / "dry-run.json").read_text("utf-8"))
    assert shadow["shadow_launches"] == [
        format_utc(t0 + timedelta(seconds=60 * k)) for k in range(6)
    ]

    # The oldest shadow launch leaves the half-open window at exactly 24 hours.
    world.clock.advance(24 * 3600 - 7 * 60 - 1)
    capped, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    assert capped.would_launch is None
    world.clock.advance(1)
    freed, _ = _run(tmp_path, tmp_state, world, dry_run=True)
    assert freed.would_launch == 1
    assert _lines_of(tmp_state, freed)


# ==============================================================================
# DF-43: pre-pending failures, backoff and attempts_exhausted
# ==============================================================================


def test_a_failed_entry_is_retried_after_the_backoff_and_the_third_failure_abandons_it__df43(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.fail("reread", "timeout", n=9, times=None)
    launcher = FakeLauncher()

    # Cycle 1: the first transient failure.
    one, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (one.exit_code, one.reason) == (7, "revalidation_transient")
    first = _entry(tmp_state, 9)
    assert (first.state, first.attempts, first.last_reason) == (
        "failed",
        1,
        "revalidation_transient",
    )

    # Cycle 2, 9 min 59 s after the failure: still in backoff, no probe, no re-read.
    world.clock.advance(599)
    calls = len(world.runner.calls)
    two, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (two.exit_code, two.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, two)) == [(9, "in_backoff")]
    assert _trace(world)[calls:] == [
        "user",
        "origin",
        "discover",
        "comments:9",
        "events:9",
    ]
    assert _entry(tmp_state, 9) == first

    # Cycle 3, exactly 10 minutes after: retried, the second failure.
    world.clock.advance(1)
    calls = len(world.runner.calls)
    three, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (three.exit_code, three.reason) == (7, "revalidation_transient")
    assert _trace(world)[calls + 3 :] == [
        "comments:9",
        "events:9",
        "edits:9",
        "items:9",
        "probe",
        "reread:9",
    ]
    second = _entry(tmp_state, 9)
    assert (second.state, second.attempts, second.launches) == ("failed", 2, 0)
    assert second.updated_at == world.clock.now()

    # Cycle 4, 10 minutes later: the third failure abandons the entry.
    world.clock.advance(600)
    four, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines = _lines_of(tmp_state, four)
    (decision,) = _of_kind(lines, "decision")
    assert (decision["reason"], decision["state"]) == (
        "attempts_exhausted",
        "abandoned",
    )
    cycle_line = _the_cycle_line(lines)
    # Exit 7 holds even when the third failure abandons the entry.
    assert (cycle_line["exit"], cycle_line["reason"]) == (7, "revalidation_transient")
    tomb = _entry(tmp_state, 9)
    assert (tomb.state, tomb.attempts, tomb.launches) == ("abandoned", 3, 0)
    assert (tomb.last_reason, tomb.pending_at, tomb.consumed_at) == (
        "attempts_exhausted",
        None,
        None,
    )

    # Cycle 5: the tombstone is never launched, whatever the time.
    world.clock.advance(3600)
    calls = len(world.runner.calls)
    five, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (five.exit_code, five.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, five)) == [(9, "already_dispatched")]
    assert _trace(world)[calls + 3 :] == ["comments:9", "events:9"]
    assert _entry(tmp_state, 9) == tomb
    assert launcher.calls == []


# ==============================================================================
# Part D: long-run and budget properties (plan step 6.8)
#
# Same rules as parts B and C: every scenario is a ``GhWorld`` over a
# ``FakeClock`` that only ever ``advance``s, and every cycle's lines go through
# ``check_line_kinds`` (DF-41) via ``_lines_of``.
# ==============================================================================

_HALF_HOUR = 30 * 60


def _numbered_launches(call_number: int) -> cycle.launch.LaunchOutcome:
    return cycle.launch.LaunchOutcome("launched", f"op-d-{call_number:04d}", "ok")


def _mixed_launches(call_number: int) -> cycle.launch.LaunchOutcome:
    """launched, unknown, spawn_error, launched, ... by launcher call number."""
    kind = call_number % 4
    if kind == 2:
        return unknown_outcome()
    if kind == 3:
        return spawn_error_outcome()
    return _numbered_launches(call_number)


def _prompt_numbers(launcher) -> list[int]:
    """The issue numbers the launcher was asked for, after checking each prompt."""
    numbers = []
    for _orca, _worktree, prompt, _timeout in launcher.calls:
        prefix, _, digits = prompt.rpartition(" ")
        assert prefix == "/sc:issue --claim"
        assert digits.isdigit() and digits == str(int(digits))
        numbers.append(int(digits))
    return numbers


# ==============================================================================
# NFR-005: 50 cycles over a changing world launch an issue at most once
# ==============================================================================

_FIFTY_STEPS = (60, 300, 900, 1800, 3600, 7200, 600)  # 14,460 s per 7 cycles


def _change_world(world, tmp_state, launcher, i) -> None:
    """The fixture world of cycle ``i``: issues come, go, fail, get claimed."""
    now = world.clock.now()
    if i == 0:
        world.issues_from(range(1, 5))
    if i % 3 == 0 and i > 0:
        world.issue(100 + i)  # a new eligible issue every third cycle
    if i % 5 == 2:
        world.fail("reread", "timeout", times=1)  # the next re-read times out
    if i % 7 == 3:
        world.update(2, listed=0)  # issue 2 leaves discovery ...
    if i % 7 == 5:
        world.update(2, listed=1)  # ... and comes back
    if i % 9 == 4 and launcher.calls:
        newest = _prompt_numbers(launcher)[-1]
        world.update(newest, markers=[marker_comment(1, now)])  # its own claim
    if i % 11 == 6:
        # Issue 1 is unlabelled and approved again, later than any launch.
        again = [
            label_event(
                3,
                "unlabeled",
                world.config.approval_label,
                now - timedelta(seconds=30),
                actor_id=APPROVER_ID,
                actor_login=OWN_LOGIN,
            ),
            label_event(
                4,
                "labeled",
                world.config.approval_label,
                now - timedelta(seconds=10),
                actor_id=APPROVER_ID,
                actor_login=OWN_LOGIN,
            ),
        ]
        world.update(1, events=[*_ev(world), *again])


def test_fifty_cycles(tmp_path, tmp_state, gh_world):
    """AC-22, NFR-005, FR-024: 50 cycles never launch an issue more than once."""
    world = gh_world()
    launch_times: list[datetime] = []
    launcher = FakeLauncher(
        _mixed_launches, on_call=lambda: launch_times.append(world.clock.now())
    )
    seen_states: set[str] = set()
    launches_by_cycle: list[int] = []
    for i in range(50):
        _change_world(world, tmp_state, launcher, i)
        before = len(launcher.calls)
        res, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
        _lines_of(tmp_state, res)
        made = len(launcher.calls) - before
        launches_by_cycle.append(made)
        assert made in (0, 1)
        assert res.launched_issue is None or made == 1  # unknown outcomes launch too
        assert res.exit_code in (0, 7)
        entries = tmp_state.load().entries
        for n, entry in entries.items():
            assert entry.launches <= 1, f"issue {n}: {entry.launches} launches"
            seen_states.add(entry.state)
        world.clock.advance(_FIFTY_STEPS[i % len(_FIFTY_STEPS)])

    numbers = _prompt_numbers(launcher)
    assert len(numbers) == len(set(numbers)), f"an issue launched twice: {numbers}"
    assert max(launches_by_cycle) == 1
    # Every launcher call is recorded as a launch by the store, and no other entry is.
    entries = tmp_state.load().entries
    assert sorted(n for n, e in entries.items() if e.launches == 1) == sorted(numbers)
    # The world really exercised the paths that could launch twice.
    assert {"launched", "unknown", "abandoned", "claimed"} <= seen_states
    # FR-024: no rolling 24 h window holds more than 6 launches.
    for start in launch_times:
        inside = [t for t in launch_times if start <= t < start + timedelta(hours=24)]
        assert len(inside) <= 6
    assert world.clock.now() - CYCLE_NOW > timedelta(hours=24)


# ==============================================================================
# PF-008: N eligible issues, 24 h of cycles, then 24 h later
# ==============================================================================


@pytest.mark.parametrize("count", [1, 2, 6, 7, 50, 99])
def test_acceptance_property(tmp_path, tmp_state, gh_world, count):
    """AC-10, FR-016, FR-024: one launch per cycle and six per rolling day."""
    world = gh_world()
    world.issues_from(range(1, count + 1))
    launcher = FakeLauncher(_numbered_launches)
    capped = min(count, 6)

    def one_cycle():
        before = len(launcher.calls)
        res, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
        lines = _lines_of(tmp_state, res)
        made = len(launcher.calls) - before
        assert made in (0, 1)  # at most one launch per cycle
        assert (res.exit_code, res.launched_issue is None) == (0, made == 0)
        if made:
            assert launcher.calls[-1][2] == f"/sc:issue --claim {res.launched_issue}"
        world.clock.advance(_HALF_HOUR)
        return res, lines

    # 48 cycles, one every 30 minutes: the first launch is 23.5 h old at the end.
    day_capped: set[int] = set()
    for k in range(48):
        res, lines = one_cycle()
        assert res.launched_issue == (k + 1 if k < capped else None)
        day_capped |= {n for n, why in _decisions(lines) if why == "day_cap"}
    assert _prompt_numbers(launcher) == list(range(1, capped + 1))
    assert sorted(tmp_state.load().entries) == list(range(1, capped + 1))
    # The rest skipped on the day cap, every one of them at least once.
    assert day_capped == set(range(capped + 1, count + 1))

    # Exactly 24 h after the first launch the oldest leaves the window, and each
    # later cycle frees one more slot: one more issue launches per cycle. The cap
    # is 6 per rolling 24 h, so the second day launches min(N - 6, 6) of the rest
    # and the others wait (for N > 12 the rest needs further days).
    second_day = min(count - capped, 6)
    for k in range(48):
        res, _ = one_cycle()
        assert (res.launched_issue is not None) == (k < second_day)
        assert len(launcher.calls) == capped + min(k + 1, second_day)
    numbers = _prompt_numbers(launcher)
    assert len(numbers) == capped + second_day
    assert len(set(numbers)) == len(numbers)  # each issue at most once
    assert numbers[:capped] == list(range(1, capped + 1))
    assert set(numbers) <= set(range(1, count + 1))
    entries = tmp_state.load().entries
    assert sorted(entries) == sorted(numbers)
    assert {e.launches for e in entries.values()} == {1}
    if count <= 12:
        assert sorted(numbers) == list(range(1, count + 1))  # all N launched


# ==============================================================================
# NFR-010: a second `once` against identical state launches nothing
# ==============================================================================


@pytest.mark.parametrize("advance_s", [0, 60])
def test_second_once_launches_nothing(tmp_path, tmp_state, gh_world, advance_s):
    """AC-22, NFR-010: a second once on identical state launches nothing."""
    world = gh_world()
    world.issue(9)
    launcher = FakeLauncher(_numbered_launches)
    first, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert (first.exit_code, first.launched_issue) == (0, 9)
    assert len(launcher.calls) == 1
    entries = tmp_state.load().entries
    assert entries[9].state == "launched"

    world.clock.advance(advance_s)
    second, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    lines = _lines_of(tmp_state, second)
    assert (second.exit_code, second.reason, second.launched_issue) == (
        0,
        "cycle_complete",
        None,
    )
    assert _decisions(lines) == [(9, "already_dispatched")]
    assert len(launcher.calls) == 1  # still the first cycle's launch only
    assert tmp_state.load().entries == entries  # the entry is byte-for-byte as it was
    # The second cycle read only the claim comments: no re-read, no probe.
    assert _reads(world, 9) == [*_LAUNCH_READS, "comments"]
    assert _trace(world).count("probe") == 1


# ==============================================================================
# NFR-009: at most 35 per-issue gh calls plus 2 shared, 3 kept for the re-read
# ==============================================================================


def _per_issue_calls(world) -> int:
    shared = {"user", "origin", "discover", "probe"}
    return len([t for t in _trace(world) if t not in shared])


def test_ten_skipping_candidates_stop_at_32_calls_and_leave_two_unread__nfr009(
    tmp_path, tmp_state, gh_world
):
    assert (github.CALL_CAP, github.RESERVED_CALLS) == (35, 3)
    world = gh_world()
    world.issues_from(range(1, 11), items=[{"status": "In progress"}])  # r = 4
    res, deps = _run(tmp_path, tmp_state, world)
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [
        *[(n, "project_mismatch") for n in range(1, 9)],
        (9, "budget_exhausted"),
        (10, "budget_exhausted"),
    ]
    assert _per_issue_calls(world) == 32  # the cap minus the 3 reserved calls
    assert _the_cycle_line(lines)["gh_calls"] == 2 + 32
    for n in range(1, 9):
        assert _reads(world, n) == _FULL_READS
    assert _reads(world, 9) == [] and _reads(world, 10) == []
    assert dict(tmp_state.load().considered) == {n: CYCLE_NOW for n in range(1, 9)}
    assert deps.launcher.calls == []


def test_the_three_reserved_calls_remain_for_the_re_read__nfr009(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issues_from(range(1, 8), items=[{"status": "In progress"}])  # 7 x 4 = 28
    world.issues_from(range(8, 11))  # the 8th candidate is the first eligible one
    res, deps = _run(tmp_path, tmp_state, world)
    lines = _lines_of(tmp_state, res)
    assert (res.exit_code, res.launched_issue) == (0, 8)
    assert _decisions(lines) == [
        *[(n, "project_mismatch") for n in range(1, 8)],
        (8, "launched"),
    ]
    # 28 for the seven skips + 4 for the checks of 8 = the 32 allowed, then the
    # reserved 3 (re-read, events, items) bring the per-issue total to exactly 35.
    assert _reads(world, 8) == [*_FULL_READS, "reread", "events", "items"]
    assert _per_issue_calls(world) == 35
    assert _the_cycle_line(lines)["gh_calls"] == 2 + 35
    assert _reads(world, 9) == [] and _reads(world, 10) == []
    assert [c[2] for c in deps.launcher.calls] == ["/sc:issue --claim 8"]
    assert _entry(tmp_state, 8).state == "launched"


# ==============================================================================
# Gate C fix tests
#
# C-1 and C-11 (no time left is not a mismatch; no None reaches a Runner),
# C-2 (a stopping candidate has no decision line; a clean cycle is
# ``cycle_complete``), C-6 to C-9 (write failures and the migrated store) and
# C-10 (S1 for every launch-step outcome), C-13 (the real mountinfo reader).
# ==============================================================================


def _stderr_fallback(capsys) -> dict:
    """The one stderr audit fallback line, parsed; it has exactly the five keys."""
    lines = [ln for ln in capsys.readouterr().err.splitlines() if ln.strip()]
    (text,) = lines
    parsed = json.loads(text)
    assert set(parsed) == {"kind", "ts", "host", "exit", "reason"}
    return parsed


def _jump_at_the_re_read_items(world, seconds=236):
    """Move the clock during the second ``items`` read, the reserved re-read."""
    _on_nth(world, "items", 9, 2, lambda: world.clock.advance(seconds))


# -- C-1: no time left is not an origin mismatch -------------------------------


def test_no_time_for_the_origin_check_at_cycle_start_is_gh_timeout__fr029_c1(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.on("user", lambda: world.clock.advance(236))
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (3, "gh_timeout")  # design 8.5, shared call
    assert [argv[0] for argv, _ in world.runner.calls] == ["gh"]  # no git call
    assert deps.launcher.calls == []
    assert _decisions(_lines_of(tmp_state, res)) == []
    line = _the_cycle_line(_audit_lines(tmp_state))
    assert (line["exit"], line["reason"], line["gh_calls"]) == (3, "gh_timeout", 1)


def test_a_236_s_jump_during_the_re_read_is_budget_exhausted_not_origin_mismatch__fr029_c1(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _jump_at_the_re_read_items(world)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "budget_exhausted")]
    assert _trace(world).count("origin") == 1  # the re-check never started a git call
    assert _trace(world)[-1] == "items:9"
    assert deps.launcher.calls == []
    stored = tmp_state.load()
    assert stored.entries == {}
    assert 9 not in stored.considered  # budget_exhausted is never stamped


def test_fewer_than_5_s_left_before_the_origin_re_check_is_budget_exhausted__fr029_c1_c11(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    # With the 120 s cut-off out of the way, only the 5 s floor can refuse the
    # git call: the guard on its own must skip the step and start no process.
    monkeypatch.setattr(cycle, "LAUNCH_CUTOFF_S", 1000.0)
    world = gh_world()
    world.issue(9)
    _jump_at_the_re_read_items(world)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "budget_exhausted")]
    assert _trace(world).count("origin") == 1
    assert _trace(world)[-1] == "items:9"
    assert None not in world.runner.timeouts
    assert deps.launcher.calls == []
    assert tmp_state.load().entries == {}


def test_fewer_than_5_s_left_before_the_probe_skips_the_step_without_a_probe__fr029_c11(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    _on_nth(world, "items", 9, 1, lambda: world.clock.advance(236))
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "budget_exhausted")]
    assert not _probed(world)
    assert _trace(world)[-1] == "items:9"
    assert None not in world.runner.timeouts
    assert deps.launcher.calls == []
    assert 9 not in tmp_state.load().considered


def test_a_clock_that_crosses_the_cut_off_inside_the_origin_call_starts_no_launch__fr029_n1(
    tmp_path, tmp_state, gh_world
):
    # 115 s at the reserved re-read: the pre-check passes (115 <= 120). The second
    # origin call then takes 10 s (125 s): the cut-off passed during the git call,
    # so no pending entry is written and the launcher is never called (design 647).
    world = gh_world()
    world.issue(9)
    _jump_at_the_re_read_items(world, seconds=115)
    seen = {"origin": 0}

    def slow_second_origin():
        seen["origin"] += 1
        if seen["origin"] == 2:
            world.clock.advance(10)

    world.on("origin", slow_second_origin)
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert _decisions(_lines_of(tmp_state, res)) == [(9, "budget_exhausted")]
    assert _trace(world).count("origin") == 2  # the git call did run
    assert deps.launcher.calls == []
    stored = tmp_state.load()
    assert stored.entries == {}  # no pending entry
    assert 9 not in stored.considered  # budget_exhausted is never stamped


@pytest.mark.parametrize("how", ["failed", "timeout", "spawn_error"])
def test_a_git_call_that_ran_and_failed_is_still_origin_mismatch__fr025_c1(
    tmp_path, tmp_state, gh_world, how
):
    world = gh_world()
    world.issue(9)
    world.fail("origin", how, after=1)  # the re-check, not the cycle-start check
    res, deps = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (2, "origin_mismatch")
    assert _trace(world).count("origin") == 2
    assert _decisions(_lines_of(tmp_state, res)) == []
    assert deps.launcher.calls == []
    assert tmp_state.load().entries == {}


def test_every_runner_call_of_a_launch_cycle_gets_its_configured_timeout__fr029_c11(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    res, _ = _run(tmp_path, tmp_state, world)
    assert res.launched_issue == 9
    assert _trace(world) == _LAUNCH_TRACE
    # gh 20 s, git and the probe 10 s: nothing shortened, nothing missing.
    assert world.runner.timeouts == [
        20.0,  # user
        10.0,  # origin
        20.0,  # discover
        20.0,  # comments
        20.0,  # events
        20.0,  # edits
        20.0,  # items
        10.0,  # probe
        20.0,  # reread
        20.0,  # events
        20.0,  # items
        10.0,  # origin
    ]


# -- C-2: strict DF-41 ----------------------------------------------------------


def test_a_clean_cycle_names_cycle_complete_and_its_decisions_keep_their_reasons__df41_c2(
    tmp_path, tmp_state, gh_world
):
    res, _, _ = SCENARIOS["mixed_decisions_and_launch"](tmp_path, tmp_state, gh_world)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == [
        (11, "assigned_other"),
        (12, "not_approved"),
        (13, "launched"),
    ]
    assert _the_cycle_line(lines)["reason"] == "cycle_complete"


def test_project_read_failed_ends_the_cycle_without_a_decision_line__df41_c2(
    tmp_path, tmp_state, gh_world
):
    res, _, _ = SCENARIOS["project_scope_missing"](tmp_path, tmp_state, gh_world)
    assert (res.exit_code, res.reason) == (3, "project_read_failed")
    lines = _lines_of(tmp_state, res)
    assert _decisions(lines) == []
    assert _the_cycle_line(lines)["reason"] == "project_read_failed"


# -- C-6, C-7: a failed write --------------------------------------------------


def test_a_failed_pending_save_launches_nothing_and_is_exit_6__fr010_nfr005_c6(
    tmp_path, tmp_state, gh_world, capsys
):
    world = gh_world()
    world.issue(9)
    before = _snapshot(tmp_state)
    store = FailingStore(tmp_state, fail_saves=(1,))  # save 1 is the pending save
    deps = replace(world.deps(tmp_path, tmp_state), store=store)
    res = cycle.run_cycle(deps, False)
    assert (res.exit_code, res.reason, res.launched_issue) == (
        6,
        "state_dir_unwritable",
        None,
    )
    assert deps.launcher.calls == []  # the launch call was never made
    assert store.saves == 1  # and nothing else was saved
    assert _snapshot(tmp_state) == before  # dispatch.json is exactly as it was
    assert _audit_lines(tmp_state) == []  # no launched line, no cycle line
    assert _stderr_fallback(capsys) == {
        "kind": "cycle",
        "ts": format_utc(CYCLE_NOW),
        "host": "test-host",
        "exit": 6,
        "reason": "state_dir_unwritable",
    }


def test_a_failed_outcome_save_after_the_launch_never_relaunches__fr010_nfr005_c6(
    tmp_path, tmp_state, gh_world, capsys
):
    world = gh_world()
    world.issue(9)
    launcher = FakeLauncher([launched_outcome()])  # a second launch has no outcome
    store = FailingStore(tmp_state, fail_saves=(2,))  # save 2 is the outcome save
    deps = replace(world.deps(tmp_path, tmp_state, launcher=launcher), store=store)
    res = cycle.run_cycle(deps, False)
    assert (res.exit_code, res.reason) == (6, "state_dir_unwritable")
    assert len(launcher.calls) == 1
    pending = _entry(tmp_state, 9)  # the pending write of save 1 is on disk
    assert (pending.state, pending.launches) == ("pending", 1)
    assert _audit_lines(tmp_state) == []
    assert _stderr_fallback(capsys)["exit"] == 6
    # The next cycles run on a working store and must not launch issue 9 again.
    for step in range(2):
        again, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
        assert again.launched_issue is None
        assert len(launcher.calls) == 1
        assert _entry(tmp_state, 9).launches == 1
        world.clock.advance(7200)
    assert _entry(tmp_state, 9).state == "abandoned"
    assert _entry(tmp_state, 9).last_reason == "pending_orphan"


@pytest.mark.parametrize(
    "build",
    [lambda w: None, lambda w: w.issue(9, assignees=["other-user"])],
    ids=["idle", "one_skipped_issue"],
)
def test_a_failed_final_save_is_exit_6_with_no_cycle_line_and_no_health_stamp__fr023_c7(
    tmp_path, tmp_state, gh_world, capsys, build
):
    world = gh_world()
    build(world)
    before = _snapshot(tmp_state)
    store = FailingStore(tmp_state, fail_saves=(1,))  # no launch: save 1 is the last
    deps = replace(world.deps(tmp_path, tmp_state), store=store)
    res = cycle.run_cycle(deps, False)
    assert (res.exit_code, res.reason) == (6, "state_dir_unwritable")
    assert store.saves == 1
    assert _snapshot(tmp_state) == before
    assert tmp_state.load().last_completed_cycle_at is None  # no health stamp
    assert _audit_lines(tmp_state) == []  # stderr only (FR-020)
    assert _stderr_fallback(capsys)["reason"] == "state_dir_unwritable"
    assert res.lines[-1]["exit"] == 6


# -- C-8: the audit log cannot be written --------------------------------------


@pytest.mark.parametrize(
    ("fail_login", "code", "reason"),
    [(False, 0, "cycle_complete"), (True, 3, "gh_auth_failed")],
    ids=["clean_cycle", "login_failure"],
)
def test_an_unwritable_audit_log_gives_one_stderr_line_and_the_same_exit__ac14_fr020_c8(
    tmp_path, tmp_state, gh_world, capsys, fail_login, code, reason
):
    world = gh_world()
    if fail_login:
        world.fail("user", "failed")
    (tmp_state.state_dir / "audit.jsonl").mkdir()  # a directory cannot be appended to
    res, _ = _run(tmp_path, tmp_state, world)
    assert (res.exit_code, res.reason) == (code, reason)
    assert _stderr_fallback(capsys) == {
        "kind": "cycle",
        "ts": format_utc(CYCLE_NOW),
        "host": "test-host",
        "exit": code,
        "reason": reason,
    }
    stored = tmp_state.load()  # the store is still written on a clean cycle
    assert stored.last_completed_cycle_at == (None if fail_login else CYCLE_NOW)


# -- C-9: a migrated store is saved by a real cycle, never by a dry-run -------------


def _v0_to_v1(doc: dict) -> dict:
    """A test-only v0 step: drop ``legacy_note``, bump the version."""
    return {**{k: v for k, v in doc.items() if k != "legacy_note"}, "schema_version": 1}


def _v0_store(tmp_state) -> record.FileStore:
    """Rewrite the store file as a version-0 document that waits out a rate limit.

    The rate limit ends the cycle right after the load, so the migration save is
    the only write a cycle can make.
    """
    path = tmp_state.state_dir / "dispatch.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw.update(
        schema_version=0,
        legacy_note="v0 only",
        next_permitted_at=format_utc(CYCLE_NOW + timedelta(hours=1)),
    )
    path.write_bytes(json.dumps(raw).encode())
    return record.FileStore(tmp_state.state_dir, migrations={0: _v0_to_v1})


def test_a_real_cycle_saves_a_migrated_store_at_the_current_version__df17_c9(
    tmp_path, tmp_state
):
    store = _v0_store(tmp_state)
    path = tmp_state.state_dir / "dispatch.json"
    before = path.read_bytes()
    deps = replace(make_deps(tmp_path, tmp_state), store=store)
    res = cycle.run_cycle(deps, False)
    assert (res.exit_code, res.reason) == (5, "rate_limited")
    written = json.loads(path.read_text(encoding="utf-8"))
    assert path.read_bytes() != before
    assert written["schema_version"] == 1
    assert "legacy_note" not in written
    assert deps.runner.calls == []


def test_a_dry_run_migrates_in_memory_and_never_writes_the_store__df17_fr019_c9(
    tmp_path, tmp_state
):
    store = _v0_store(tmp_state)
    path = tmp_state.state_dir / "dispatch.json"
    before = path.read_bytes()
    deps = replace(make_deps(tmp_path, tmp_state), store=store)
    res = cycle.run_cycle(deps, True)
    assert (res.exit_code, res.reason) == (5, "rate_limited")
    assert path.read_bytes() == before  # byte-identical: not even the migration
    assert json.loads(before)["schema_version"] == 0
    assert deps.runner.calls == []


# -- C-10: S1, nothing after a launch-step outcome ---------------------------------


def _refuse_prompt(monkeypatch):
    def refuse(n):
        raise ValueError("no prompt")

    monkeypatch.setattr(cycle.launch, "build_claim_prompt", refuse)


@pytest.mark.parametrize(
    ("setup", "code", "stamped"),
    [
        pytest.param(
            lambda w, mp: w.issue(9, reread={"state": "closed"}),
            0,
            [9],
            id="revalidation_failed",
        ),
        pytest.param(
            lambda w, mp: _refuse_prompt(mp),
            7,
            [9],
            id="prompt_invalid",
        ),
        pytest.param(
            lambda w, mp: w.on("reread", lambda: w.clock.advance(121), n=9),
            0,
            [],
            id="budget_exhausted_at_the_cutoff",
        ),
        pytest.param(
            lambda w, mp: w.issue(9, reread={"assignees": [OWN_LOGIN, "other-user"]}),
            0,
            [9],
            id="reread_assigned_other",
        ),
        pytest.param(
            lambda w, mp: w.issue(9, reread={"assignees": []}),
            0,
            [9],
            id="reread_unassigned",
        ),
    ],
)
def test_no_later_candidate_is_read_or_stamped_after_a_launch_step_outcome__fr016_s1_c10(
    tmp_path, tmp_state, gh_world, monkeypatch, setup, code, stamped
):
    world = gh_world()
    world.issue(9)
    world.issue(10)
    setup(world, monkeypatch)
    res, deps = _run(tmp_path, tmp_state, world)
    assert res.exit_code == code
    assert deps.launcher.calls == []
    assert _touched(world) == {9}  # issue 10 is neither read nor stamped
    assert sorted(tmp_state.load().considered) == stamped
    assert _entry(tmp_state, 10) is None


def test_no_later_candidate_is_read_or_stamped_after_a_spawn_error__fr016_s1_c10(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(9)
    world.issue(10)
    launcher = FakeLauncher([spawn_error_outcome()])
    res, _ = _run(tmp_path, tmp_state, world, launcher=launcher)
    assert res.exit_code == 7
    assert len(launcher.calls) == 1
    assert _touched(world) == {9}
    assert sorted(tmp_state.load().considered) == [9]
    assert _entry(tmp_state, 10) is None


# -- C-13: the real mountinfo reader -----------------------------------------------

_NFS_LINE = "20 1 0:30 / / rw,relatime shared:1 - nfs4 server:/export rw"


def test_the_mountinfo_path_is_the_proc_file__df52_c13():
    assert cycle._MOUNTINFO == "/proc/self/mountinfo"


def test_the_real_proc_mountinfo_gives_a_filesystem_type_for_the_root__df52_c13():
    if sys.platform != "linux":
        pytest.skip("/proc/self/mountinfo exists on Linux only")
    text = _REAL_READ_MOUNTINFO()
    assert text is not None
    assert cycle.fs_type_of("/", text) is not None


def test_read_mountinfo_returns_the_file_text_and_none_when_it_is_missing__df52_c13(
    tmp_path, monkeypatch
):
    source = tmp_path / "mountinfo"
    source.write_text(_NFS_LINE + "\n", encoding="utf-8")
    monkeypatch.setattr(cycle, "_MOUNTINFO", str(source))
    assert _REAL_READ_MOUNTINFO() == _NFS_LINE + "\n"
    monkeypatch.setattr(cycle, "_MOUNTINFO", str(tmp_path / "no-such-file"))
    assert _REAL_READ_MOUNTINFO() is None


def test_load_config_refuses_a_network_state_dir_through_the_real_reader__df52_c13(
    tmp_path, monkeypatch
):
    source = tmp_path / "mountinfo"
    source.write_text(_NFS_LINE + "\n", encoding="utf-8")
    monkeypatch.setattr(cycle, "_MOUNTINFO", str(source))
    monkeypatch.setattr(cycle, "_read_mountinfo", _REAL_READ_MOUNTINFO)
    path = _write_config(tmp_path, state_dir=str(tmp_path / "state"))
    _expect("config_invalid", "network filesystem", cycle.load_config, path)
    source.write_text(ROOT_LINE + "\n", encoding="utf-8")  # a local type passes
    assert cycle.load_config(path).state_dir == tmp_path / "state"
