"""``superclaude sweep run`` takes its Run ids from the Run ledger when none is given or bound.

Reuses the Orca seams and helpers of ``test_cli_contract.py``. The autouse fixture of
``conftest.py`` points ``SUPERCLAUDE_RUN_LEDGER`` at a missing file; each test here sets its own.
"""

# ruff: noqa: F811, F401  (the ``env`` fixture is imported from test_cli_contract and used by name)

from __future__ import annotations

import json

import pytest

from superclaude.cli.sweep.ledger import compute_counts
from tests.sweep.test_cli_contract import (
    RUN,
    RUN2,
    RUN_CURRENT,
    STEM,
    _failed,
    _orca_calls,
    _payload,
    _ps,
    _run,
    _worker_list,
    _world,
    env,
)

HINT = 'no Run bound: pass --run <id> run "superclaude sweep ledger" first\n'


def put_ledger(
    monkeypatch, tmp_path, run_ids, generated="2026-11-08T11:30:00Z", raw=None
):
    path = tmp_path / "run-ledger.json"
    runs = [{"id": r, "source": "build", "reasons": ["new"]} for r in run_ids]
    path.write_text(
        raw
        if raw is not None
        else json.dumps(
            {
                "version": 1,
                "generated_at": generated,
                "orca": {"runs_listed": 0, "worktrees_listed": 0},
                "counts": compute_counts(runs),
                "runs": runs,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("SUPERCLAUDE_RUN_LEDGER", str(path))
    return path


def report_text(env) -> str:
    return (env.sweeps / f"{STEM}.md").read_text("utf-8")


def test_sweep_reads_ledger_when_no_run_and_no_binding(env, monkeypatch, tmp_path):
    put_ledger(monkeypatch, tmp_path, [RUN, RUN2])
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _world(env, RUN, RUN2)

    payload = _payload(_run(env))

    assert payload["scope"]["runs"] == [RUN, RUN2]
    assert (
        "Run ids from the Run ledger built 2026-11-08T11:30:00Z"
        in report_text(env).splitlines()
    )


def test_explicit_run_ignores_ledger(env, monkeypatch, tmp_path):
    put_ledger(monkeypatch, tmp_path, [RUN2])
    _world(env, RUN)

    payload = _payload(_run(env, "--run", RUN))

    assert payload["scope"]["runs"] == [RUN]
    assert RUN_CURRENT not in _orca_calls(env)
    assert "Run ledger" not in report_text(env)


def test_missing_ledger_exit_2_with_hint(env):
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _failed(_run(env), 2, HINT)


def test_corrupt_ledger_exit_2_with_hint(env, monkeypatch, tmp_path):
    put_ledger(monkeypatch, tmp_path, [], raw="{not json")
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _failed(_run(env), 2, HINT)


def test_empty_runs_ledger_sweeps_with_empty_scope_exit_0(env, monkeypatch, tmp_path):
    put_ledger(monkeypatch, tmp_path, [])
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _ps(env)

    payload = _payload(_run(env))

    assert payload["scope"]["runs"] == []
    text = report_text(env)
    assert "Scope: Runs none" in text
    assert "Run ids from the Run ledger built" in text


def test_malformed_id_in_ledger_rejected(env, monkeypatch, tmp_path):
    put_ledger(monkeypatch, tmp_path, [RUN + "x"])
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _failed(_run(env), 2, HINT)


def test_duplicate_ids_in_ledger_swept_once(env, monkeypatch, tmp_path):
    put_ledger(monkeypatch, tmp_path, [RUN, RUN, RUN2, RUN])
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _world(env, RUN, RUN2)

    payload = _payload(_run(env))

    assert payload["scope"]["runs"] == [RUN, RUN2]
    assert _orca_calls(env).count(_worker_list(RUN)) == 1


@pytest.mark.parametrize(
    ("generated", "minutes"),
    [
        ("2026-11-08T10:00:00Z", 120),
        ("2026-11-08 10:28:00", 92),
    ],  # ISO form and SQLite form
)
def test_stale_ledger_over_90_minutes_adds_age_to_header(
    env, monkeypatch, tmp_path, generated, minutes
):
    # 2026-11-08 12:00:00 is the fixed clock of the ``env`` fixture.
    put_ledger(monkeypatch, tmp_path, [RUN], generated=generated)
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _world(env, RUN)

    _payload(_run(env))

    line = (
        f"Run ids from the Run ledger built {generated} . ledger is {minutes} min old"
    )
    assert line in report_text(env).splitlines()


@pytest.mark.parametrize(
    "generated", ["2026-11-08T11:45:00Z", "2026-11-08 10:30:00"]
)  # 15 min, exactly 90
def test_fresh_ledger_header_has_no_age(env, monkeypatch, tmp_path, generated):
    put_ledger(monkeypatch, tmp_path, [RUN], generated=generated)
    env.orca.respond(RUN_CURRENT, kind="no_binding")
    _world(env, RUN)

    _payload(_run(env))

    text = report_text(env)
    assert f"Run ids from the Run ledger built {generated}" in text.splitlines()
    assert "ledger is" not in text
