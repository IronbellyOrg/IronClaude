"""Task 19: generate one repo's config, approvers file and state directory.

Every path is under ``tmp_path``; HOME is redirected there too, so a write to the real home
would show as a file under ``tmp_path / "home"`` and the tests assert there is none.
"""

from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import cycle, defaults, generate, repos

from .conftest import result

LAUNCH_ID = 1001
FIXED = {"ironbelly": 11, "clayphi": 22}


def _record(name: str = "IronClaude", slug: str = "IronbellyOrg/IronClaude"):
    return repos.OrcaRepo("id-1", name, f"/home/u/workspaces/{name}", slug)


def _projects_reply(*ids: str, more: bool = False) -> str:
    nodes = [{"id": i, "number": n} for n, i in enumerate(ids, 1)]
    connection = {"nodes": nodes, "pageInfo": {"hasNextPage": more}}
    return json.dumps({"data": {"repository": {"projectsV2": connection}}})


def _world(
    slug: str = "IronbellyOrg/IronClaude",
    *,
    account=LAUNCH_ID,
    projects=("PVT_one",),
    maintainers=(33,),
    fixed=None,
):
    """A scripted gh for one repo, keyed by the exact argv the module builds."""
    fixed = FIXED if fixed is None else fixed
    script = {
        tuple(generate.argv_account()): result(stdout=json.dumps({"id": account}))
        if account is not None
        else result(stderr="HTTP 401", returncode=1),
        tuple(generate.argv_projects(slug)): result(stdout=_projects_reply(*projects)),
        tuple(generate.argv_maintainers(slug)): result(
            stdout=json.dumps([{"id": m} for m in maintainers])
        ),
    }
    for login, ident in fixed.items():
        script[tuple(generate.argv_user_id(login))] = result(
            stdout=json.dumps({"id": ident})
        )
    return script


class Runner:
    def __init__(self, script: dict) -> None:
        self.script = script
        self.calls: list[tuple[str, ...]] = []

    def run(self, argv, timeout, *, cwd=None):
        key = tuple(argv)
        self.calls.append(key)
        assert key in self.script, f"unscripted argv: {argv}"
        return self.script[key]


@pytest.fixture
def base(tmp_path, monkeypatch) -> generate.Base:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    return generate.Base(
        tmp_path / "config", tmp_path / "state", tmp_path / "worktrees"
    )


def _no_write_under_home(tmp_path: Path) -> None:
    # HOME is redirected into tmp_path, so any write through "~" would create this directory
    assert not (tmp_path / "home").exists()


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def test_a_repo_with_one_project_gets_a_valid_disabled_config(tmp_path, base) -> None:
    runner = Runner(_world())
    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    assert out.status == "generated" and out.reason is None
    config = out.config_path
    assert config == base.config_dir / "issue-watch.d" / "IronClaude.json"
    raw = json.loads(config.read_text())
    assert raw["enabled"] is False
    assert raw["repo"] == "IronbellyOrg/IronClaude"
    assert raw["project_id"] == "PVT_one"
    assert raw["owner_account_id"] == LAUNCH_ID
    assert raw["worktree"] == str(base.worktrees_dir / "IronClaude" / "Coordinator")
    assert raw["state_dir"] == str(base.state_dir / "issue-watch" / "IronClaude")
    assert raw["approvers_file"] == str(
        base.config_dir / "issue-watch.d" / "IronClaude-approvers.txt"
    )
    loaded = cycle.load_config(config)  # the generated config passes the real loader
    assert loaded.enabled is False and loaded.repo == "IronbellyOrg/IronClaude"
    assert cycle.validate_approvers(loaded.approvers_file) == {11, 22, 33}
    _no_write_under_home(tmp_path)


def test_file_modes_are_600_and_the_directory_is_700(tmp_path, base) -> None:
    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
    assert _mode(out.config_path) == 0o600
    assert _mode(out.approvers_path) == 0o600
    assert _mode(out.config_path.parent) == 0o700
    assert list(out.config_path.parent.glob(".*")) == []  # no staged file is left


def test_no_project_is_a_skip_with_nothing_written(tmp_path, base) -> None:
    runner = Runner(_world(projects=()))
    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    assert (out.status, out.reason) == ("skipped", "no_project")
    assert not base.config_dir.exists()


def test_several_projects_without_a_defaults_entry_are_ambiguous(
    tmp_path, base
) -> None:
    runner = Runner(_world(projects=("PVT_a", "PVT_b")))
    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    assert (out.status, out.reason) == ("skipped", "project_ambiguous")
    assert not base.config_dir.exists()


def test_several_projects_use_the_id_of_the_defaults_map(tmp_path, base) -> None:
    runner = Runner(_world(projects=("PVT_a", "PVT_b")))
    mapped = defaults.Defaults(projects={"IronbellyOrg/IronClaude": "PVT_b"})
    out = generate.ensure_config(_record(), mapped, runner, base)
    assert out.status == "generated"
    assert json.loads(out.config_path.read_text())["project_id"] == "PVT_b"


def test_a_defaults_entry_that_is_not_one_of_the_projects_is_ambiguous(
    tmp_path, base
) -> None:
    runner = Runner(_world(projects=("PVT_a", "PVT_b")))
    mapped = defaults.Defaults(projects={"IronbellyOrg/IronClaude": "PVT_zzz"})
    out = generate.ensure_config(_record(), mapped, runner, base)
    assert (out.status, out.reason) == ("skipped", "project_ambiguous")


def test_a_failed_account_read_is_a_skip_before_any_other_call(tmp_path, base) -> None:
    runner = Runner(_world(account=None))
    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    assert (out.status, out.reason) == ("skipped", "account_read_failed")
    assert runner.calls == [tuple(generate.argv_account())]
    assert not base.config_dir.exists()


def test_a_non_numeric_account_id_is_a_failed_read(tmp_path, base) -> None:
    script = _world()
    script[tuple(generate.argv_account())] = result(stdout='{"id": "12"}')
    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(script), base)
    assert (out.status, out.reason) == ("skipped", "account_read_failed")


def test_maintainers_are_added_to_the_fixed_approvers(tmp_path, base) -> None:
    runner = Runner(_world(maintainers=(33, 44, 55)))
    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    assert cycle.validate_approvers(out.approvers_path) == {11, 22, 33, 44, 55}
    assert out.approvers_path.read_text() == "11\n22\n33\n44\n55\n"


def test_the_launch_account_id_is_never_written_to_the_approvers_file(
    tmp_path, base
) -> None:
    # a maintainer and a fixed login both resolve to the launch account
    runner = Runner(
        _world(
            maintainers=(33, LAUNCH_ID), fixed={"ironbelly": LAUNCH_ID, "clayphi": 22}
        )
    )
    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    assert out.status == "generated"
    ids = cycle.validate_approvers(out.approvers_path)
    assert LAUNCH_ID not in ids and ids == {22, 33}


def test_a_launch_account_that_is_the_only_approver_leaves_no_approvers(
    tmp_path, base
) -> None:
    runner = Runner(_world(maintainers=(LAUNCH_ID,), fixed={"ironbelly": LAUNCH_ID}))
    out = generate.ensure_config(
        _record(), defaults.Defaults(approver_logins=("ironbelly",)), runner, base
    )
    assert (out.status, out.reason) == ("skipped", "no_approvers")
    assert not base.config_dir.exists()


@pytest.mark.parametrize("failing", ["approver", "maintainers", "projects"])
def test_a_failed_read_is_a_skip_and_writes_nothing(tmp_path, base, failing) -> None:
    script = _world()
    key = {
        "approver": tuple(generate.argv_user_id("clayphi")),
        "maintainers": tuple(generate.argv_maintainers("IronbellyOrg/IronClaude")),
        "projects": tuple(generate.argv_projects("IronbellyOrg/IronClaude")),
    }[failing]
    script[key] = result(stderr="HTTP 502", returncode=1)
    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(script), base)
    assert out.status == "skipped"
    assert (
        out.reason
        == {
            "approver": "approver_read_failed",
            "maintainers": "maintainers_read_failed",
            "projects": "project_read_failed",
        }[failing]
    )
    assert not base.config_dir.exists()


def test_an_existing_config_is_left_untouched_and_no_call_is_made(
    tmp_path, base
) -> None:
    directory = base.config_dir / "issue-watch.d"
    directory.mkdir(parents=True)
    existing = directory / "IronClaude.json"
    existing.write_text("hand written, do not touch")
    runner = Runner({})
    out = generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    assert out.status == "exists" and out.config_path == existing
    assert existing.read_text() == "hand written, do not touch"
    assert runner.calls == []


def test_a_second_call_after_generation_changes_nothing(tmp_path, base) -> None:
    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
    before = out.config_path.read_bytes()
    again = generate.ensure_config(_record(), defaults.Defaults(), Runner({}), base)
    assert again.status == "exists" and out.config_path.read_bytes() == before


def test_a_leftover_approvers_file_is_never_overwritten(tmp_path, base) -> None:
    directory = base.config_dir / "issue-watch.d"
    directory.mkdir(parents=True)
    (directory / "IronClaude-approvers.txt").write_text("999\n")
    out = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
    assert (out.status, out.reason) == ("skipped", "approvers_file_exists")
    assert (directory / "IronClaude-approvers.txt").read_text() == "999\n"
    assert not (directory / "IronClaude.json").exists()


def test_two_repos_get_two_different_state_dirs(tmp_path, base) -> None:
    a = generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
    slug = "IronbellyOrg/Coder"
    b = generate.ensure_config(
        _record("Coder", slug), defaults.Defaults(), Runner(_world(slug)), base
    )
    assert a.status == b.status == "generated"
    assert a.state_dir != b.state_dir
    assert a.state_dir == base.state_dir / "issue-watch" / "IronClaude"
    assert b.state_dir == base.state_dir / "issue-watch" / "Coder"
    cfg_a, cfg_b = (cycle.load_config(o.config_path) for o in (a, b))
    assert cfg_a.state_dir != cfg_b.state_dir
    assert cfg_a.approvers_file != cfg_b.approvers_file
    assert cfg_b.repo == slug


def test_the_trigger_label_of_the_defaults_reaches_the_config(tmp_path, base) -> None:
    custom = defaults.Defaults(trigger_label="watch:go")
    out = generate.ensure_config(_record(), custom, Runner(_world()), base)
    assert cycle.load_config(out.config_path).trigger_label == "watch:go"
    plain = generate.ensure_config(
        _record("Coder", "IronbellyOrg/Coder"),
        defaults.Defaults(),
        Runner(_world("IronbellyOrg/Coder")),
        base,
    )
    assert "labels" not in json.loads(plain.config_path.read_text())


@pytest.mark.parametrize("name", ["bad name", "-lead", "a/b", "", "x" * 101])
def test_a_name_that_is_not_a_safe_file_name_is_skipped(tmp_path, base, name) -> None:
    runner = Runner({})
    out = generate.ensure_config(_record(name), defaults.Defaults(), runner, base)
    assert (out.status, out.reason) == ("skipped", "bad_name")
    assert runner.calls == [] and not base.config_dir.exists()


def test_every_call_is_a_read_and_each_rest_call_carries_method_get(
    tmp_path, base
) -> None:
    runner = Runner(_world())
    generate.ensure_config(_record(), defaults.Defaults(), runner, base)
    # the account, the Projects, the two fixed logins and the maintainers
    assert len(runner.calls) == 5
    for argv in runner.calls:
        text = " ".join(argv)
        assert argv[:2] == ("gh", "api")
        assert "POST" not in argv and "mutation" not in text.lower()
        if argv[2] == "graphql":
            assert any(a.startswith("query=query(") for a in argv)
        else:
            assert argv[2:4] == ("--method", "GET"), argv


def test_a_projects_list_with_a_next_page_is_a_failed_read_not_a_complete_list() -> (
    None
):
    assert "hasNextPage" in generate.PROJECTS_QUERY
    slug = "IronbellyOrg/IronClaude"
    script = {
        tuple(generate.argv_projects(slug)): result(
            stdout=_projects_reply("PVT_a", more=True)
        )
    }
    assert generate._projects(Runner(script), slug) is None


def test_the_projects_query_asks_for_ids_and_numbers_only() -> None:
    query = generate.PROJECTS_QUERY
    assert query.startswith("query(") and "mutation" not in query.lower()
    assert "title" not in query and "body" not in query
    assert query.count("String!") == 2  # $owner and $name, both non-null


def test_nothing_is_written_under_the_real_home(tmp_path, base) -> None:
    generate.ensure_config(_record(), defaults.Defaults(), Runner(_world()), base)
    _no_write_under_home(tmp_path)
