"""A bound plan-writing worker can ask and be released (Plan B Task 14, design G2).

The worker is bound the way the guard binds any session: a first prompt that
holds ``[sc-launch:v1:<32 hex>]`` and a matching ``pending/<nonce>`` record the
test writes, never a ``sessions/<id>`` file written by hand. The release is the
coordinator-side ``release`` helper, which creates the session's ``.ok`` file.
"""

from __future__ import annotations

import time

import pytest

from superclaude.cli.issue_pipeline import release
from tests.hooks.test_launch_level_guard import (
    NONCE,
    SID,
    _assert_bound,
    _assert_decision,
    _bash,
    _marker,
    _pending,
    _prompt,
    _run,
    _skill,
    _store,
)

HEARTBEAT = (
    "orca orchestration send --from term_1d62 --type heartbeat --subject alive"
    " --task-id task_9b94 --dispatch-id ctx_e194 --phase implementing"
)
ASK = (
    "orca orchestration ask --from term_1d62 --question plan-ready --timeout-ms 600000"
)


def _bind_worker(tmp_path) -> None:
    _pending(tmp_path, "worktree", NONCE)
    result = _run(_prompt(_marker() + " write the plan for issue 9"), tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    _assert_bound(tmp_path, SID, "worktree")


def _allowed(result) -> bool:
    return (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_a_prompt_with_the_marker_binds_the_worker_and_one_without_does_not(tmp_path):
    _bind_worker(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    assert _allowed(_run(_prompt("write the plan for issue 9"), other))
    assert not (_store(other / "home") / "sessions" / SID).exists()


@pytest.mark.parametrize(
    "command",
    [
        HEARTBEAT,
        ASK,
        HEARTBEAT + " --to run:run_93bf",
        ASK + " --to run:run_93bf",
        HEARTBEAT + ' --body "the plan is ready for approval"',
        HEARTBEAT + ' --phase "<short: investigating|implementing|reviewing|waiting>"',
        "orca orchestration ask --from term_1d62 --question 'may I proceed? (yes or no)'",
        "orca orchestration send --type worker_done --subject done --outcome succeeded",
        HEARTBEAT + ' --body "ready; please approve (issue 9) & reply"',
        HEARTBEAT + ' --to "run:run_93bf"',
        ASK + " --to=run:run_93bf",
        HEARTBEAT + " --body 'do not use --to dispatch:x'",
        HEARTBEAT + " --json",
        "/usr/local/bin/" + HEARTBEAT,
    ],
)
def test_a_bound_worker_may_send_and_ask_its_coordinator(tmp_path, command):
    _bind_worker(tmp_path)
    assert _allowed(_run(_bash(command), tmp_path))


def test_the_address_check_ends_well_inside_the_hook_time_limit(tmp_path):
    _bind_worker(tmp_path)
    command = "orca orchestration send " + "--a b " * 1300
    started = time.monotonic()
    result = _run(_bash(command), tmp_path)
    assert time.monotonic() - started < 5
    _assert_decision(result, tmp_path, "LL-ESCAPE", "W", text=True)


@pytest.mark.parametrize(
    "command",
    [
        "git push origin x; " + "orca " * 12000,
        "git push origin x; " + "orca -x " * 4000,
        "git push origin x; " + "orca status " * 5000,
        "git push origin x; " + "orca worktree list " * 3000,
    ],
)
def test_a_command_with_very_many_orca_words_is_blocked_inside_the_time_limit(
    tmp_path, command
):
    _bind_worker(tmp_path)
    started = time.monotonic()
    result = _run(_bash(command), tmp_path)
    assert time.monotonic() - started < 3
    assert result.returncode == 2


@pytest.mark.parametrize(
    "command",
    [
        HEARTBEAT + " --to dispatch:ctx_other",
        HEARTBEAT + ' --to "@all"',
        HEARTBEAT + " --to @idle",
        HEARTBEAT + " --to @worktree:abc",
        HEARTBEAT + " --to term_other",
        HEARTBEAT + " --to=dispatch:ctx_other",
        HEARTBEAT + " --to run:run_93bf --to dispatch:ctx_other",
        HEARTBEAT + " --to",
        HEARTBEAT + " --run run_other",
        ASK + " --to dispatch:ctx_other",
        ASK + " --run=run_other",
        # a shell expansion that puts a --to on the real command line unseen
        HEARTBEAT + " --{to=dispatch:ctx_o,}",
        HEARTBEAT + " --t{o=dispatch:ctx_o,}",
        HEARTBEAT + " -{-to=dispatch:ctx_o,}",
        "X=to; " + HEARTBEAT + " --$X dispatch:ctx_o",
        "X=to; " + HEARTBEAT + " --${X} dispatch:ctx_o",
        HEARTBEAT + " --to run:r1 `echo --to dispatch:x`",
        HEARTBEAT + " --to run:r1 $(echo --to dispatch:x)",
        ASK + " --{to=dispatch:ctx_o,}",
        # a line continuation or a glob hides the --to from the word view
        HEARTBEAT + " \\\n--to dispatch:ctx_o",
        "orca orchestration send \\\n--to dispatch:ctx_o --type heartbeat",
        HEARTBEAT + " --t*",
        HEARTBEAT + " --t[o]",
        HEARTBEAT + " --t?",
        HEARTBEAT + " *",
        HEARTBEAT + ' --body "$HOME"',
        HEARTBEAT + " --body hi\n--to dispatch:ctx_o",
        "echo hi; " + HEARTBEAT,
        HEARTBEAT + " | cat",
        HEARTBEAT + " --body 'it'\"'\"'s' --to=@all",
        # a quoted ; | ( starts a new segment in the word view; the raw command does not
        HEARTBEAT + ' --phase "a|b" --to dispatch:ctx_o',
        ASK + " --question '(x)' --to dispatch:ctx_o",
        HEARTBEAT + ' --body "x; y" --to @all',
        HEARTBEAT + ' --to "run:r1,dispatch:ctx_o"',
        HEARTBEAT + ' "--to" "@all"',
        HEARTBEAT + " --body 'two\nlines'",
        # spellings Orca might read as --to or --run, bare words and other shapes
        HEARTBEAT + " --t dispatch:ctx_o",
        HEARTBEAT + " --=dispatch:ctx_o",
        HEARTBEAT + " -t dispatch:ctx_o",
        HEARTBEAT + " -- --to dispatch:ctx_o",
        ASK + " --ru run_other",
        HEARTBEAT + " --json dispatch:ctx_o",
        "orca orchestration send x",
        "X=1 " + HEARTBEAT,
        "env " + HEARTBEAT,
        HEARTBEAT + " --body " + "a" * 9000,
        # an option name in another case
        HEARTBEAT + " --To dispatch:ctx_o",
        HEARTBEAT + " --TO=dispatch:ctx_o",
        ASK + " --RUN run_other",
        # another Orca server is not the worker's own coordinator
        HEARTBEAT + " --environment other",
        ASK + " --pairing-code abc123",
        # an option before the verb words may take the next word as its value
        "orca --foo status orchestration send --to dispatch:ctx_o",
        "orca --foo status orchestration send --to @all",
        "orca --json orchestration send --to dispatch:ctx_o",
        "orca --version orchestration send --to dispatch:ctx_o",
        "orca *status orchestration send --to dispatch:ctx_o",
        "orca ?tatus orchestration ask --to @all",
    ],
)
def test_a_bound_worker_cannot_address_another_worker_or_a_group(tmp_path, command):
    _bind_worker(tmp_path)
    _assert_decision(
        _run(_bash(command), tmp_path), tmp_path, "LL-ESCAPE", "W", text=True
    )


@pytest.mark.parametrize(
    "command",
    [
        "orca orchestration dispatch x",
        "orca orchestration reply --id msg_x --body hi",
        "orca terminal send --text approved",
        "orca worktree create --name x",
        "orca agent launch --name w",
        # the same verbs behind an option, a flag value or a glob
        "orca --foo status orchestration dispatch x",
        "orca --foo status worktree create --name x",
        "orca --foo worktree list worktree create",
        "orca orchestration dispatch x --note --help",
        "orca * --help",
        "orca worktree list *",
        "orca * status orchestration send --to dispatch:ctx_o",
        "orca agent launch --name w --help",
    ],
)
def test_every_other_orca_word_stays_blocked_for_a_bound_worker(tmp_path, command):
    _bind_worker(tmp_path)
    _assert_decision(
        _run(_bash(command), tmp_path), tmp_path, "LL-ESCAPE", "W", text=True
    )


@pytest.mark.parametrize(
    "command",
    [
        "orca status",
        "orca --version",
        "orca worktree list",
        "orca list --help",
        "orca agent launch -h",
    ],
)
def test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker(tmp_path, command):
    _bind_worker(tmp_path)
    assert _allowed(_run(_bash(command), tmp_path))


@pytest.mark.parametrize(
    ("command", "msg_id"),
    [
        ("git push -u origin feature", "LL-PUSH"),
        ("gh pr create --repo IronbellyOrg/IronClaude --title x", "LL-SUBMIT"),
        ("git commit -m x", "LL-COMMIT"),
    ],
)
def test_a_bound_worker_is_still_blocked_from_publishing(tmp_path, command, msg_id):
    _bind_worker(tmp_path)
    assert _allowed(_run(_bash(HEARTBEAT), tmp_path))
    _assert_decision(_run(_bash(command), tmp_path), tmp_path, msg_id, "W", text=True)


def test_bound_send_ask_implement_blocked_release_implement_allowed(tmp_path):
    _bind_worker(tmp_path)
    assert _allowed(_run(_bash(HEARTBEAT), tmp_path))
    assert _allowed(_run(_bash(ASK), tmp_path))
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")
    store = _store(tmp_path / "home")
    assert release.release(SID, store) == "released"
    assert _allowed(_run(_skill("sc:implement"), tmp_path))
    assert _allowed(_run(_bash(HEARTBEAT), tmp_path))


def test_a_forged_release_from_the_workers_own_session_is_blocked_as_tampering(
    tmp_path,
):
    _bind_worker(tmp_path)
    forged = f"touch ~/.claude/state/launch-level/sessions/{SID}.ok"
    _assert_decision(
        _run(_bash(forged), tmp_path), tmp_path, "LL-TAMPER", "W", text=True
    )
    _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")


def test_a_brief_built_with_a_pending_nonce_binds_the_worker_and_one_without_does_not(
    tmp_path,
):
    import json
    import os
    import subprocess
    import sys

    from superclaude.cli.issue_pipeline import brief
    from tests.skills.test_issue_orca_worktree import SCRIPT

    home = tmp_path / "home"
    home.mkdir()
    env = dict(os.environ, HOME=str(home))
    out = subprocess.run(
        [sys.executable, str(SCRIPT), "pending", "--level", "worktree"],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    ).stdout
    nonce = json.loads(out)["nonce"]
    governed = brief.build(9, "feature", "simple", nonce)
    assert _allowed(_run(_prompt(governed), tmp_path))
    _assert_bound(tmp_path, SID, "worktree")
    other = tmp_path / "other"
    other.mkdir()
    assert _allowed(_run(_prompt(brief.build(9, "feature", "simple")), other))
    assert not (_store(other / "home") / "sessions" / SID).exists()
