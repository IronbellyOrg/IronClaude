"""Task 20: the trigger label and the ``Approved`` field check, over a scripted ``gh``."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import defaults, repo_init

from .conftest import result

REPO = "IronbellyOrg/IronClaude"
DEFAULTS = defaults.Defaults()
LABEL = DEFAULTS.trigger_label


class Gh:
    """A scripted runner keyed by argv; it records every call."""

    def __init__(self, script: dict) -> None:
        self.script = script
        self.calls: list[tuple[str, ...]] = []

    def run(self, argv, timeout, *, cwd=None):
        key = tuple(argv)
        self.calls.append(key)
        assert key in self.script, f"unscripted argv: {argv}"
        return self.script[key]


def _labels(*names: str):
    return result(stdout=json.dumps([{"name": n} for n in names]))


def _creates(gh: Gh) -> list[tuple[str, ...]]:
    return [c for c in gh.calls if c[:3] == ("gh", "label", "create")]


def test_a_missing_label_is_created_with_one_create_call() -> None:
    gh = Gh(
        {
            tuple(repo_init.argv_label_list(REPO)): _labels("bug", "feature"),
            tuple(repo_init.argv_label_create(REPO, LABEL)): result(),
        }
    )
    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "created"
    assert _creates(gh) == [tuple(repo_init.argv_label_create(REPO, LABEL))]


def test_a_present_label_makes_no_create_call() -> None:
    gh = Gh({tuple(repo_init.argv_label_list(REPO)): _labels("bug", LABEL)})
    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "present"
    assert _creates(gh) == []


def test_a_second_call_after_a_create_is_idempotent() -> None:
    state = {"labels": ["bug"]}

    class World(Gh):
        def run(self, argv, timeout, *, cwd=None):
            self.calls.append(tuple(argv))
            if argv[:3] == ["gh", "label", "list"]:
                return _labels(*state["labels"])
            state["labels"].append(argv[3])
            return result()

    gh = World({})
    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "created"
    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "present"
    assert len(_creates(gh)) == 1


def test_a_failed_create_is_reported_failed() -> None:
    gh = Gh(
        {
            tuple(repo_init.argv_label_list(REPO)): _labels("bug"),
            tuple(repo_init.argv_label_create(REPO, LABEL)): result(
                stderr="HTTP 403", returncode=1
            ),
        }
    )
    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "failed"


@pytest.mark.parametrize(
    "reply",
    [
        result(stderr="HTTP 502", returncode=1),
        result(timed_out=True),
        result(spawn_error="FileNotFoundError"),
        result(stdout="not json"),
        result(stdout='{"name": "x"}'),
        result(stdout='[{"nome": "x"}]'),
        result(stdout=json.dumps([{"name": f"l{i}"} for i in range(500)])),
    ],
)
def test_a_failed_or_unreadable_or_full_list_never_creates(reply) -> None:
    gh = Gh({tuple(repo_init.argv_label_list(REPO)): reply})
    assert repo_init.ensure_trigger_label(REPO, DEFAULTS, gh) == "failed"
    assert _creates(gh) == []


def test_the_read_only_state_check_never_creates() -> None:
    gh = Gh({tuple(repo_init.argv_label_list(REPO)): _labels("bug")})
    assert repo_init.trigger_label_state(REPO, DEFAULTS, gh) == "missing"
    assert _creates(gh) == []
    gh = Gh({tuple(repo_init.argv_label_list(REPO)): _labels(LABEL)})
    assert repo_init.trigger_label_state(REPO, DEFAULTS, gh) == "present"


def test_the_label_name_comes_from_the_defaults() -> None:
    custom = defaults.Defaults(trigger_label="watch:go")
    gh = Gh(
        {
            tuple(repo_init.argv_label_list(REPO)): _labels(
                LABEL
            ),  # the built-in is NOT it
            tuple(repo_init.argv_label_create(REPO, "watch:go")): result(),
        }
    )
    assert repo_init.ensure_trigger_label(REPO, custom, gh) == "created"
    assert _creates(gh)[0][3] == "watch:go"


def test_no_name_is_a_literal_in_the_module() -> None:
    source = Path(repo_init.__file__).read_text()
    for literal in ("issue-watch:trigger", '"Approved"', '"Yes"'):
        assert literal not in source


@pytest.mark.parametrize("bad", ["a/b/c", "", "a b/c", "-a/b"])
def test_a_bad_repo_raises_before_any_call(bad) -> None:
    gh = Gh({})
    with pytest.raises(ValueError):
        repo_init.ensure_trigger_label(bad, DEFAULTS, gh)
    assert gh.calls == []


# --- the Approved field ------------------------------------------------------------------


def _fields(*rows: dict):
    return result(stdout=json.dumps(list(rows)))


def _approved(options=("Yes",), kind="single_select", name="Approved") -> dict:
    return {
        "name": name,
        "data_type": kind,
        "options": [{"name": o} for o in options],
    }


def _check(reply) -> str:
    argv = tuple(repo_init.argv_issue_fields("IronbellyOrg"))
    gh = Gh({argv: reply})
    out = repo_init.check_approved_field("IronbellyOrg", DEFAULTS, gh)
    assert gh.calls == [argv]  # one read, nothing else
    return out


def test_the_approved_field_present_with_the_yes_option() -> None:
    assert _check(_fields(_approved(), {"name": "Other"})) == "approved_field_present"
    # the object form with a "fields" list is read too
    obj = result(stdout=json.dumps({"fields": [_approved(("No", "Yes"))]}))
    assert _check(obj) == "approved_field_present"


def test_the_approved_field_missing() -> None:
    assert _check(_fields({"name": "Other"})) == "approved_field_missing"
    assert _check(_fields()) == "approved_field_missing"


def test_the_approved_field_present_without_the_yes_option() -> None:
    assert _check(_fields(_approved(("No", "Maybe")))) == "approved_field_missing"
    assert _check(_fields(_approved(()))) == "approved_field_missing"


def test_a_field_named_approved_that_is_not_single_select_does_not_count() -> None:
    assert _check(_fields(_approved(kind="text"))) == "approved_field_missing"


@pytest.mark.parametrize(
    "reply",
    [
        result(stderr="HTTP 404", returncode=1),
        result(timed_out=True),
        result(stdout="not json"),
        result(stdout='"a string"'),
    ],
)
def test_a_failed_organization_read_is_reported_failed(reply) -> None:
    assert _check(reply) == "failed"


def test_the_field_check_never_writes() -> None:
    argv = repo_init.argv_issue_fields("IronbellyOrg")
    assert argv == ["gh", "api", "--method", "GET", "orgs/IronbellyOrg/issue-fields"]
    for bad in ("a/b", "", "-x", "a b"):
        with pytest.raises(ValueError):
            repo_init.argv_issue_fields(bad)
