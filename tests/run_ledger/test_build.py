"""Orca reader and implausible-result guards (``build_ledger``) with a fake runner."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone

import pytest

from superclaude.cli.sweep import ledger
from superclaude.cli.sweep.ledger import Implausible, OrcaFailure, build_ledger

GEN = datetime(2026, 11, 26, 18, 0, 0, tzinfo=timezone.utc)
OLD = "2026-11-01 10:00:00"
WT = {"id": "repoA::/home/u/feature", "isMainWorktree": False}
ARGV_TEMPLATES = [
    r"orchestration run-list --json",
    r"worktree list --json",
    r"orchestration task-list --run run_[0-9a-f]{12} --json",
    r"orchestration worker-list --run run_[0-9a-f]{12} --json --limit 100( --cursor \S+)?",
]


def rid(n: int) -> str:
    return f"run_{n:012x}"


def run(
    n: int, created: str = OLD, updated: str | None = None, legacy: int = 0
) -> dict:
    return {
        "id": rid(n),
        "objective": f"run {n}",
        "legacy": legacy,
        "created_at": created,
        "updated_at": updated or created,
    }


def ok(result: dict) -> tuple[int, str]:
    return 0, json.dumps({"ok": True, "result": result})


class FakeOrca:
    """Answers the four read calls from canned data and records every argv."""

    def __init__(self, runs, worktrees=(WT,), tasks=None, workers=None, events=None):
        self.runs, self.worktrees = list(runs), list(worktrees)
        self.tasks = tasks or {}
        self.workers = (
            workers or {}
        )  # run id -> list of pages (each a list of worker rows)
        self.calls: list[list[str]] = []
        self.events = events

    def __call__(self, args):
        self.calls.append(list(args))
        if self.events is not None:
            self.events.append("call")
        line = " ".join(args)
        assert any(re.fullmatch(t, line) for t in ARGV_TEMPLATES), (
            f"unexpected argv: {line}"
        )
        if args[:2] == ["orchestration", "run-list"]:
            return ok({"runs": self.runs})
        if args[:2] == ["worktree", "list"]:
            return ok({"worktrees": self.worktrees})
        run_id = args[3]
        if args[1] == "task-list":
            return ok({"runId": run_id, "tasks": self.tasks.get(run_id, [])})
        pages = self.workers.get(run_id, [[]])
        index = int(args[args.index("--cursor") + 1][1:]) if "--cursor" in args else 0
        page = {"hasMore": index + 1 < len(pages)}
        if page["hasMore"]:
            page["nextCursor"] = f"c{index + 1}"
        return ok({"workers": pages[index], "page": page})


def worker(worktree_id: str) -> dict:
    return {"resource": {"worktreeId": worktree_id}}


def fixed_now():
    return GEN


def test_worker_list_pagination():
    fake = FakeOrca(
        [run(1)],
        workers={rid(1): [[worker("x")], [worker("y")], [worker(WT["id"])]]},
    )
    data = build_ledger(fake, None, fixed_now)
    pages = [c for c in fake.calls if c[1] == "worker-list"]
    assert len(pages) == 3
    assert "--cursor" not in pages[0]
    assert pages[1][-2:] == ["--cursor", "c1"]
    assert pages[2][-2:] == ["--cursor", "c2"]
    assert [e["id"] for e in data["runs"]] == [rid(1)]
    assert data["runs"][0]["reasons"] == ["live_worktree"]


class LoopingCursor(FakeOrca):
    def __init__(self, runs, cursors):
        super().__init__(runs)
        self.cursors = iter(cursors)

    def __call__(self, args):
        if len(args) > 1 and args[1] == "worker-list":
            self.calls.append(list(args))
            return ok(
                {
                    "workers": [],
                    "page": {"hasMore": True, "nextCursor": next(self.cursors)},
                }
            )
        return super().__call__(args)


def test_repeated_cursor_fails():
    fake = LoopingCursor([run(1)], ["same", "same"])
    with pytest.raises(OrcaFailure, match="^orca-failure:"):
        build_ledger(fake, None, fixed_now)


def test_page_cap_fails():
    fake = LoopingCursor([run(1)], (f"c{i}" for i in range(1000)))
    with pytest.raises(OrcaFailure, match="^orca-failure:.*more than 50 pages"):
        build_ledger(fake, None, fixed_now)
    assert (
        len([c for c in fake.calls if c[1] == "worker-list"]) == ledger.MAX_WORKER_PAGES
    )


@pytest.mark.parametrize("mode", ["exit", "timeout", "not_ok"])
def test_orca_failure_raises(mode):
    def runner(args):
        if mode == "exit":
            return 1, ""
        if mode == "timeout":
            raise subprocess.TimeoutExpired(["orca", *args], 30)
        return 0, json.dumps({"ok": False, "error": "boom"})

    with pytest.raises(OrcaFailure, match="^orca-failure:"):
        build_ledger(runner, None, fixed_now)


def test_missing_binary_message(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    with pytest.raises(
        OrcaFailure, match="orca not found or Orca app not running"
    ) as info:
        build_ledger(ledger.orca_runner, None, fixed_now)
    assert str(info.value).startswith("orca-failure:")


def test_empty_worktree_list_implausible():
    with pytest.raises(Implausible, match="^implausible:"):
        build_ledger(FakeOrca([run(1)], worktrees=[]), None, fixed_now)


def test_empty_run_list_with_previous_implausible():
    previous = {"generated_at": "2026-11-26T17:00:00Z", "runs": []}
    with pytest.raises(Implausible, match="^implausible:"):
        build_ledger(FakeOrca([]), previous, fixed_now)
    # no previous ledger: an empty Orca is a plausible first build
    assert build_ledger(FakeOrca([]), None, fixed_now)["runs"] == []


PREVIOUS = {"generated_at": "2026-11-26T17:00:00Z", "runs": [{"id": rid(9)}]}


def test_zero_included_implausible_needs_recent_run():
    # A SQLite-form updated_at (3 h before the ISO generated_at) counts as recent.
    recent = [run(1, updated="2026-11-26 15:00:00")]
    with pytest.raises(Implausible, match="^implausible:"):
        build_ledger(FakeOrca(recent), PREVIOUS, fixed_now)
    # Only old Runs, or only legacy ones: nothing recent, so zero included is plausible.
    assert build_ledger(FakeOrca([run(1)]), PREVIOUS, fixed_now)["runs"] == []
    legacy_recent = [run(2, created="2026-11-26 17:30:00", legacy=1)]
    assert build_ledger(FakeOrca(legacy_recent), PREVIOUS, fixed_now)["runs"] == []
    # An unparseable time never counts as recent and never raises.
    assert (
        build_ledger(FakeOrca([run(3, created="garbage")]), PREVIOUS, fixed_now)["runs"]
        == []
    )
    # With no previous Runs the guard does not apply.
    empty_previous = {"generated_at": "2026-11-26T17:00:00Z", "runs": []}
    assert build_ledger(FakeOrca(recent), empty_previous, fixed_now)["runs"] == []


def test_accept_empty_overrides_only_the_zero_included_guard():
    recent = [run(1, updated="2026-11-26 15:00:00")]
    data = build_ledger(FakeOrca(recent), PREVIOUS, fixed_now, accept_empty=True)
    assert data["runs"] == []
    with pytest.raises(Implausible):
        build_ledger(
            FakeOrca(recent, worktrees=[]), PREVIOUS, fixed_now, accept_empty=True
        )
    with pytest.raises(Implausible):
        build_ledger(FakeOrca([]), PREVIOUS, fixed_now, accept_empty=True)
    with pytest.raises(OrcaFailure):
        build_ledger(lambda args: (1, ""), PREVIOUS, fixed_now, accept_empty=True)


def test_generated_at_taken_before_first_call():
    events: list[str] = []

    def now():
        events.append("now")
        return GEN

    data = build_ledger(FakeOrca([run(1)], events=events), None, now)
    assert events[0] == "now"
    assert events.count("now") == 1
    assert data["generated_at"] == "2026-11-26T18:00:00Z"


def test_workers_not_fetched_for_runs_already_in():
    in_by_task, in_by_new, out = run(1), run(2, created="2026-11-26 17:50:00"), run(3)
    fake = FakeOrca(
        [in_by_task, in_by_new, out],
        tasks={rid(1): [{"status": "ready", "created_at": OLD}]},
    )
    data = build_ledger(
        fake,
        {"generated_at": "2026-11-26T17:00:00Z", "runs": [{"id": rid(9)}]},
        fixed_now,
    )
    fetched = {c[3] for c in fake.calls if c[1] == "worker-list"}
    assert fetched == {rid(3)}
    assert sorted(e["id"] for e in data["runs"]) == [rid(1), rid(2)]
    assert data["orca"] == {"runs_listed": 3, "worktrees_listed": 1}
    assert data["version"] == 1


@pytest.mark.parametrize(
    ("configured", "installed", "expected"),
    [
        (
            None,
            {"orca-ide", "orca"},
            "/bin/orca-ide",
        ),  # the sweep's default comes first
        (None, {"orca"}, "/bin/orca"),  # ... and plain orca is the fallback
        (None, {"orca-ide"}, "/bin/orca-ide"),
        (
            "my-orca",
            {"my-orca", "orca-ide", "orca"},
            "/bin/my-orca",
        ),  # ORCA_CLI_COMMAND wins
        ("my-orca", {"orca-ide", "orca"}, None),  # and is the only name tried
        (None, set(), None),
    ],
)
def test_orca_binary_resolved_like_the_sweep(
    monkeypatch, configured, installed, expected
):
    monkeypatch.delenv("ORCA_CLI_COMMAND", raising=False)
    if configured:
        monkeypatch.setenv("ORCA_CLI_COMMAND", configured)
    monkeypatch.setattr(
        shutil, "which", lambda name: f"/bin/{name}" if name in installed else None
    )
    assert ledger.orca_binary_path() == expected
