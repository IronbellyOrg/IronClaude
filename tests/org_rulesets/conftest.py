"""Shared test support for scripts/apply_org_rulesets.py.

Tests never call GitHub: every ``gh`` call goes through the fake runner below, which
subclasses the real ``Runner`` and overrides only ``_execute``, so each call still passes
the real allowlist. Names are synthetic (``acme-one``). Every shared fixture is defined
in this file only: a fixture imported into several test modules is listed more than
once by ``pytest --fixtures``, which crashes on the tie (CI runs that command).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "apply_org_rulesets.py"


def load_script():
    spec = importlib.util.spec_from_file_location("apply_org_rulesets", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["apply_org_rulesets"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def orr():
    """The script module, loaded once."""
    return load_script()


@pytest.fixture(scope="session")
def fake_runner_cls(orr):
    """A Runner that never starts a process.

    ``replies`` maps ``(method, path)`` to an answer. The path is the full path with its
    query or, failing that, without it. An answer is a ``Result``, a callable
    ``(argv, stdin) -> Result``, or a list of those served in order (so three POSTs to
    ``rulesets`` can return three ids). A call with no canned answer gets return code
    127. ``executed`` lists every call that reached ``_execute`` (a refused call never
    does).
    """

    class FakeRunner(orr.Runner):
        def __init__(self, replies=None, read_only=False):
            super().__init__(read_only=read_only)
            self.replies = dict(replies or {})
            self.executed = []

        @staticmethod
        def ok(data):
            return orr.Result(0, json.dumps(data), "")

        @staticmethod
        def pages(*pages):
            """What ``gh api --paginate`` prints: one JSON array per page."""
            return orr.Result(0, "".join(json.dumps(p) for p in pages), "")

        @staticmethod
        def http(status):
            """A failed call, as ``gh`` reports it."""
            return orr.Result(1, '{"message": "m"}', f"gh: m (HTTP {status})")

        @staticmethod
        def method_of(argv):
            return argv[argv.index("--method") + 1] if "--method" in argv else "GET"

        @staticmethod
        def path_of(argv):
            return next(t for t in argv[2:] if t.startswith("repos/"))

        def _execute(self, argv, stdin):
            self.executed.append((list(argv), stdin))
            method, full = self.method_of(argv), self.path_of(argv)
            for key in ((method, full), (method, full.partition("?")[0])):
                if key in self.replies:
                    answer = self.replies[key]
                    if isinstance(answer, list):
                        if not answer:
                            break
                        answer = answer.pop(0)
                    return answer(argv, stdin) if callable(answer) else answer
            return orr.Result(127, "", f"no canned reply for {argv}")

    return FakeRunner


_REPO = "repos/acme/acme-one"
_SERVER = {"source": "acme-one", "source_type": "Repository", "created_at": "2026"}


def _activity(branch):
    return f"{_REPO}/activity?ref=refs/heads/{branch}&time_period=quarter&per_page=100"


@pytest.fixture
def world(fake_runner_cls):
    """A factory for a fake GitHub holding one repo, ``acme/acme-one``: default branch
    ``master`` and an ``integration`` branch, no direct pushes, no protection, no
    rulesets, two v* tags. ``gets`` replaces or adds canned GET answers (by path);
    ``post`` replaces the POST answer; other keywords change the repo answer. A POST
    stores the body under ids 101, 102, ... and ``GET rulesets/<id>`` returns it with
    server keys added, as GitHub does."""
    ok, http = fake_runner_cls.ok, fake_runner_cls.http

    def build(*, gets=None, post=None, **repo_changes):
        store = {}

        def default_post(argv, stdin):
            number = 101 + len(store)
            store[number] = json.loads(stdin)
            return ok({"id": number})

        def readback(number):
            def reply(argv, stdin):
                return ok({**store[number], "id": number, **_SERVER})

            return reply

        repo = {
            "owner": {"login": "acme"},
            "name": "acme-one",
            "archived": False,
            "default_branch": "master",
            "permissions": {"admin": True},
            **repo_changes,
        }
        answers = {
            _REPO: ok(repo),
            f"{_REPO}/branches/master": ok({}),
            f"{_REPO}/branches/integration": ok({}),
            _activity("master"): ok([]),
            _activity("integration"): ok([]),
            f"{_REPO}/branches/master/protection": http(404),
            f"{_REPO}/branches/integration/protection": http(404),
            f"{_REPO}/rulesets?per_page=100": ok([]),
            f"{_REPO}/git/matching-refs/tags/v?per_page=100": ok([{}, {}]),
            **{f"{_REPO}/rulesets/{n}": readback(n) for n in range(101, 104)},
            **(gets or {}),
        }
        replies = {("GET", path): answer for path, answer in answers.items()}
        replies[("POST", f"{_REPO}/rulesets")] = post or default_post
        runner = fake_runner_cls(replies)
        runner.store = store
        return runner

    return build
