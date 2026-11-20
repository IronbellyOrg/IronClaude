"""What the verb tests of B2 stand on: a fake ``gh`` and ``ccsession``, a repos.yaml, a run file, the golden wake.

``World`` is a ``Runner``. It answers the few calls the verbs make (``ccsession --help``,
``gh api user``, the comments of an issue, a comment post and edit, a repo and its branch)
from plain data and records every argv. ``install`` puts it behind ``ext.inner_runner``,
so the real ``limits.GuardedRunner`` still checks each call. ``call`` runs one verb through
the real click group and gives ``(exit code, parsed JSON)``.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

import yaml
from click.testing import CliRunner

from superclaude.cli.issue_watch.runner import CommandResult
from superclaude.cli.orchestrator import answer_check, ext, questions, state
from superclaude.cli.orchestrator.group import orchestrator_group
from tests.issue_watch.conftest import TIERS_TEXT

REPO = "IronbellyOrg/IronClaude"
ORCH = "ironclaude-1"
TAG = "orchestrator-ironclaude-1"
WID = "20261119T101500Z-3fa9c1d2"
GOLDEN = (
    Path(__file__).parents[1]
    / "issue_watch"
    / "fixtures"
    / "orchestrator_wake_golden.json"
)


def golden() -> dict:
    """A fresh copy of the golden wake file that PR A's writer and parser are tested against."""
    return json.loads(GOLDEN.read_text(encoding="utf-8"))


def _result(stdout: str = "", returncode: int = 0, stderr: str = "") -> CommandResult:
    return CommandResult(
        argv=(),
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        timed_out=False,
        spawn_error=None,
        duration_s=0.0,
    )


class World:
    """GitHub and ccsession as the B2 verbs see them."""

    def __init__(self, login: str = "clayphi") -> None:
        self.login = login
        self.comments: dict[tuple[str, int], list[dict]] = {}
        self.next_id = 1000
        self.repo_meta: dict[str, dict] = {}
        self.calls: list[tuple[str, ...]] = []
        self.unexpected: list[tuple[str, ...]] = []
        self.fail_when: list[Callable[[tuple[str, ...]], bool]] = []

    # -- data ------------------------------------------------------------------------------

    def add_comment(
        self, repo: str, number: int, body: str, login: str | None = None
    ) -> int:
        """A comment that somebody else (or an earlier run) wrote; returns its id."""
        self.next_id += 1
        self.comments.setdefault((repo, number), []).append(
            {"id": self.next_id, "login": login or self.login, "body": body}
        )
        return self.next_id

    def body_of(self, comment_id: int) -> str:
        for rows in self.comments.values():
            for row in rows:
                if row["id"] == comment_id:
                    return row["body"]
        raise KeyError(comment_id)

    def set_repo(
        self,
        repo: str,
        *,
        default_branch: str = "master",
        permissions: dict | None = None,
        methods: tuple[str, ...] = ("squash", "merge", "rebase"),
        protected: bool = False,
    ) -> None:
        self.repo_meta[repo] = {
            "default_branch": default_branch,
            "permissions": permissions
            if permissions is not None
            else {
                "admin": False,
                "maintain": True,
                "push": True,
                "triage": True,
                "pull": True,
            },
            "allow_squash_merge": "squash" in methods,
            "allow_merge_commit": "merge" in methods,
            "allow_rebase_merge": "rebase" in methods,
            "protected": protected,
        }

    def argvs(self, *prefix: str) -> list[tuple[str, ...]]:
        """Every call seen whose argv starts with ``prefix``."""
        return [c for c in self.calls if c[: len(prefix)] == prefix]

    # -- the Runner ------------------------------------------------------------------------

    def run(
        self, argv: list[str], timeout: float, *, cwd: str | None = None
    ) -> CommandResult:
        key = tuple(argv)
        self.calls.append(key)
        if any(pred(key) for pred in self.fail_when):
            return _result(returncode=1, stderr="fake: failed")
        if key == ("ccsession", "--help"):
            return _result(TIERS_TEXT)
        if key[:3] == ("gh", "api", "user"):
            return _result(self.login + "\n")
        if key[:3] == ("gh", "api", "--paginate") and key[3].endswith("/comments"):
            repo, number = self._issue(key[3])
            rows = self.comments.get((repo, number), [])
            return _result("".join(json.dumps(r) + "\n" for r in rows))
        if key[:4] == ("gh", "api", "-X", "POST") and key[4].endswith("/comments"):
            repo, number = self._issue(key[4])
            comment_id = self.add_comment(repo, number, key[6].removeprefix("body="))
            return _result(f"{comment_id}\n")
        if key[:4] == ("gh", "api", "-X", "PATCH") and "/issues/comments/" in key[4]:
            comment_id = int(key[4].rsplit("/", 1)[1])
            for rows in self.comments.values():
                for row in rows:
                    if row["id"] == comment_id:
                        row["body"] = key[6].removeprefix("body=")
                        return _result(json.dumps(row))
            return _result(returncode=1, stderr="fake: not found")
        if len(key) == 3 and key[:2] == ("gh", "api") and key[2].startswith("repos/"):
            parts = key[2].split("/")
            repo = "/".join(parts[1:3])
            meta = self.repo_meta.get(repo)
            if meta is None:
                return _result(returncode=1, stderr="fake: not found")
            if len(parts) == 3:
                return _result(
                    json.dumps({k: v for k, v in meta.items() if k != "protected"})
                )
            if parts[3] == "branches" and parts[4] == meta["default_branch"]:
                return _result(
                    json.dumps({"name": parts[4], "protected": meta["protected"]})
                )
        self.unexpected.append(key)
        return _result(returncode=99, stderr="fake: unscripted argv")

    @staticmethod
    def _issue(path: str) -> tuple[str, int]:
        _, owner, name, _, number, _ = path.split("/")
        return f"{owner}/{name}", int(number)


def install(monkeypatch, world: World) -> World:
    """Put ``world`` behind the guard of every verb."""
    monkeypatch.setattr(ext, "inner_runner", lambda: world)
    return world


def repos_text(**over) -> str:
    """The text of a repos.yaml with IronClaude enabled; keys in ``over`` replace top-level keys."""
    doc = {
        "schema_version": 1,
        "orgs": ["IronbellyOrg", "IronbellyGroup"],
        "repos": [
            {
                "repo": REPO,
                "enabled": True,
                "checkout": "/abs/ironclaude",
                "default_branch": "master",
                "merge_method": "squash",
                "can_merge": True,
            }
        ],
        "grants": ["issue.comment", "issue.assign"],
    }
    doc.update(over)
    return yaml.safe_dump(doc, sort_keys=False)


def make_root(
    tmp_path: Path,
    *,
    text: str | None = None,
    run: bool = True,
    run_id: str = "run_abc123",
    host: str = "ws-aidev02",
    ident: str = ORCH,
) -> Path:
    """An orchestrator repo: ``repos.yaml`` and (by default) ``runs/<id>.json`` written first."""
    (tmp_path / "repos.yaml").write_text(text if text is not None else repos_text())
    if run:
        state.create_run(tmp_path, ident, run_id, f"orchestrator-{ident}", REPO, host)
    return tmp_path


def put_wake(
    root: Path, doc: dict | None = None, wake_id: str = WID, raw: bytes | None = None
) -> Path:
    """Write ``wakes/<wake_id>.json`` (the golden wake unless ``doc`` or ``raw`` is given)."""
    path = root / ".orchestrator" / "wakes" / f"{wake_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        raw
        if raw is not None
        else (json.dumps(doc or golden(), indent=2) + "\n").encode()
    )
    return path


def call(
    root: Path, *args: str, tag: str | None = TAG, env: dict | None = None
) -> tuple[int, dict]:
    """Run one verb through the real click group; ``(exit code, the JSON it printed)``."""
    environment: dict[str, str | None] = {"CLAUDE_TOPIC": tag}
    environment.update(env or {})
    result = CliRunner().invoke(
        orchestrator_group, ["--root", str(root), *args], env=environment
    )
    if result.exception is not None and not isinstance(result.exception, SystemExit):
        raise AssertionError(f"verb crashed: {result.exception!r}\n{result.output}")
    return result.exit_code, json.loads(result.output)


def snapshot(root: Path) -> dict[str, bytes]:
    """Every file under ``root`` (the lock file apart), to compare before and after a refused write."""
    return {
        str(p.relative_to(root)): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name != "state.lock"
    }


ENTRY = "ironclaude-655.8.1"
KEY = "IronbellyOrg__IronClaude__655:8:merge"
ASKED = datetime(2026, 11, 19, 10, 0, 0, tzinfo=timezone.utc)
LATER = "2026-11-19T10:30:00Z"


def asked(
    root: Path, entry: str = ENTRY, key: str = KEY, row: int = 8, low: tuple = ()
) -> dict:
    """What ``escalate`` records when it asks Clay a question (the record ``answer-check`` reads)."""
    record, _ = questions.record_question(
        root,
        entry,
        question_key=key,
        row=row,
        issue=f"{REPO}#655",
        low_stakes=low,
        now=ASKED,
    )
    return record


def answer(
    root: Path, *, accepted: bool = True, entry: str = ENTRY, key: str | None = None
) -> str:
    """The id of an ``answer-check`` row that accepted (or refused) Clay's word, as ``--answer-ref``."""
    when = (
        LATER if accepted else "2026-11-19T09:00:00Z"
    )  # an answer older than the question is refused
    row = answer_check.check(
        root,
        entry=entry,
        source="session",
        answered_at=when,
        question_key=key,
        reply_to=entry,
    )
    assert row["accepted"] is accepted
    return row["ref"]
