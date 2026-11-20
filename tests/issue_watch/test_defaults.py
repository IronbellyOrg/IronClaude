"""Task 17: the central defaults file; every path is under ``tmp_path``."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import cycle, defaults


def _write(tmp_path: Path, raw: object) -> Path:
    path = tmp_path / defaults.DEFAULTS_FILE
    path.write_text(raw if isinstance(raw, str) else json.dumps(raw), encoding="utf-8")
    return tmp_path


def test_an_absent_file_gives_the_built_in_values(tmp_path: Path) -> None:
    got = defaults.load_defaults(tmp_path)
    assert got.approver_logins == ("ironbelly", "clayphi")
    assert got.trigger_label == "issue-watch:trigger"
    assert (got.approval_field, got.approval_option) == ("Approved", "Yes")
    assert got.allowed_owners == ("IronbellyOrg",)
    assert got.projects == {}
    assert got == defaults.Defaults()


def test_a_valid_file_is_read(tmp_path: Path) -> None:
    _write(
        tmp_path,
        {
            "approver_logins": ["ironbelly", "clayphi", "a-maintainer"],
            "trigger_label": "watch:go",
            "approval_field": "Approved",
            "approval_option": "Yes",
            "allowed_owners": ["IronbellyOrg", "Other-Org"],
            "projects": {"IronbellyOrg/IronClaude": "PVT_kwDOabc-_1"},
        },
    )
    got = defaults.load_defaults(tmp_path)
    assert got.approver_logins == ("ironbelly", "clayphi", "a-maintainer")
    assert got.trigger_label == "watch:go"
    assert got.allowed_owners == ("IronbellyOrg", "Other-Org")
    assert got.projects == {"IronbellyOrg/IronClaude": "PVT_kwDOabc-_1"}


def test_a_key_the_file_leaves_out_takes_its_built_in_value(tmp_path: Path) -> None:
    _write(tmp_path, {"trigger_label": "watch:go"})
    got = defaults.load_defaults(tmp_path)
    assert got.trigger_label == "watch:go"
    assert got.approver_logins == defaults.BUILTIN_APPROVER_LOGINS
    assert got.allowed_owners == defaults.BUILTIN_ALLOWED_OWNERS


@pytest.mark.parametrize(
    "raw",
    [
        {"surprise": 1},
        {"approver_logins": ["-x"]},
        {"approver_logins": ["ironbelly", "IronBelly"]},  # a repeat, whatever the case
        {"approver_logins": []},
        {"approver_logins": "ironbelly"},
        {"approver_logins": ["a b"]},
        {"approver_logins": [5]},
        {"trigger_label": ""},
        {"trigger_label": "-lead"},
        {"trigger_label": "a,b"},
        {"trigger_label": "x" * 51},
        {"trigger_label": 3},
        {"approval_field": "two\nlines"},
        {"approval_field": "Other"},  # the approval reads use only the built-in field
        {"approval_option": "Maybe"},  # and the built-in option
        {"approval_option": None},
        {"allowed_owners": ["bad owner"]},
        {"allowed_owners": []},
        {"projects": []},
        {"projects": {"IronbellyOrg/IronClaude": "PVX_abc"}},
        {"projects": {"IronbellyOrg/IronClaude": "PVT_"}},
        {"projects": {"IronbellyOrg/IronClaude": 7}},
        {"projects": {"not-a-repo": "PVT_abc"}},
        {"projects": {"a/b/c": "PVT_abc"}},
        [],
        "not json at all",
        '{"a": 1',
        "\xff\xfe",
    ],
)
def test_a_bad_file_is_rejected_with_the_config_error(tmp_path: Path, raw) -> None:
    _write(tmp_path, raw)
    with pytest.raises(cycle.ConfigError) as err:
        defaults.load_defaults(tmp_path)
    assert err.value.reason == "config_invalid"
    assert defaults.DEFAULTS_FILE in err.value.detail


def test_an_unknown_key_name_never_reaches_the_error_text(tmp_path: Path) -> None:
    canary = "CANARY-17-KEY"
    _write(tmp_path, {canary: 1})
    with pytest.raises(cycle.ConfigError) as err:
        defaults.load_defaults(tmp_path)
    assert canary not in str(err.value) and canary not in err.value.detail


def test_a_bad_login_never_reaches_the_error_text(tmp_path: Path) -> None:
    canary = "CANARY-17-DO-NOT-ECHO;"
    _write(tmp_path, {"approver_logins": [canary]})
    with pytest.raises(cycle.ConfigError) as err:
        defaults.load_defaults(tmp_path)
    assert canary not in str(err.value) and canary not in err.value.detail


def test_a_file_that_is_too_large_or_not_a_regular_file_is_rejected(
    tmp_path: Path,
) -> None:
    big = tmp_path / "big"
    big.mkdir()
    _write(big, '{"trigger_label": "' + "x" * (70 * 1024) + '"}')
    with pytest.raises(cycle.ConfigError):
        defaults.load_defaults(big)
    directory = tmp_path / "dir"
    (directory / defaults.DEFAULTS_FILE).mkdir(parents=True)
    with pytest.raises(cycle.ConfigError):
        defaults.load_defaults(directory)


def test_the_default_config_dir_is_expanded_and_runs_nothing(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".config" / "superclaude").mkdir(parents=True)
    _write(tmp_path / ".config" / "superclaude", {"trigger_label": "from:home"})
    assert defaults.load_defaults().trigger_label == "from:home"
    # nothing under tmp_path was written by the read
    assert sorted(p.name for p in (tmp_path / ".config" / "superclaude").iterdir()) == [
        defaults.DEFAULTS_FILE
    ]


def test_the_module_imports_no_process_module() -> None:
    source = Path(defaults.__file__).read_text()
    for banned in ("subprocess", "os.system", "shell=True"):
        assert banned not in source
