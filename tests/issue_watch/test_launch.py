"""Tests for the Orca launcher: prompt, argv, Orca probe and origin check (part A).

Nothing here runs a real command: every ``git`` and ``orca`` call goes through
``FakeRunner`` and every path lookup through a dict-based ``which``.
"""

from __future__ import annotations

import copy
import inspect
import json
import shutil
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import launch, predicates
from superclaude.cli.issue_watch.launch import (
    OPERATION_ID_PATHS,
    ORCA_AGENT,
    LaunchOutcome,
    OrcaLauncher,
    build_claim_prompt,
    check_origin,
    find_orca,
    launch_argv,
    outcome_of,
    parse_origin,
    retry_argv,
)

from .conftest import result

ORCA = "/opt/orca/bin/orca-ide"
WORKTREE = "/work/tree"
PROMPT = "/sc:issue --claim 9"

# --- prompt (FR-012, design 9.3) ----------------------------------------------


def test_ac7_prompt_accepts_only_the_int_nine__fr012_nfr001():
    """AC-7 FR-012 NFR-001: of the spec's seven inputs only ``9`` returns a prompt."""
    assert build_claim_prompt(9) == "/sc:issue --claim 9"


@pytest.mark.parametrize("value", ["9", True, 0, -1, 10**9, 9.0])
def test_ac7_prompt_rejects_every_other_input__fr012_nfr001(value):
    """AC-7 FR-012 NFR-001: a str, bool, zero, negative, too large or float raises."""
    with pytest.raises(ValueError):
        build_claim_prompt(value)


@pytest.mark.parametrize("value", [None, "", "9; rm -rf /", [9], b"9", 9.5, False])
def test_ac7_prompt_rejects_hostile_non_ints__fr012_nfr001(value):
    """AC-7 FR-012 NFR-001: other types and hostile text raise, nothing is built."""
    with pytest.raises(ValueError):
        build_claim_prompt(value)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, "/sc:issue --claim 1"),
        (999999999, "/sc:issue --claim 999999999"),
    ],
)
def test_ac7_prompt_accepts_both_range_ends__fr012(value, expected):
    """AC-7 FR-012: 1 and 999999999 are the first and last accepted numbers."""
    assert build_claim_prompt(value) == expected


# --- launch argv (FR-013, threat T10) ------------------------------------------


def test_ac8_launch_argv_equals_the_literal_twelve_elements__fr013():
    """AC-8 FR-013: the argv is exactly the 12 elements, agent id ``claude``."""
    argv = launch_argv(ORCA, WORKTREE, PROMPT)
    assert argv == [
        "/opt/orca/bin/orca-ide",
        "agent",
        "launch",
        "--agent",
        "claude",
        "--worktree",
        "path:/work/tree",
        "--surface",
        "terminal",
        "--prompt",
        "/sc:issue --claim 9",
        "--json",
    ]
    assert len(argv) == 12


def test_ac8_launch_argv_takes_a_path_object_like_a_str__fr013():
    """AC-8 FR-013: a ``Path`` worktree gives the same ``path:`` selector."""
    assert launch_argv(ORCA, Path(WORKTREE), PROMPT) == launch_argv(
        ORCA, WORKTREE, PROMPT
    )


def test_ac8_launch_argv_has_no_extra_flag__fr013_t10():
    """AC-8 FR-013 T10: only five flags appear and no permission flag is added."""
    argv = launch_argv(ORCA, WORKTREE, PROMPT)
    flags = [item for item in argv if item.startswith("--")]
    assert flags == ["--agent", "--worktree", "--surface", "--prompt", "--json"]
    assert "--dangerously-skip-permissions" not in argv
    assert "--permission-mode" not in argv
    assert argv[-1] == "--json"


def test_ac8_orca_agent_constant_is_claude__fr013():
    """AC-8 FR-013: the agent id is the fixed constant ``claude`` (DF-11)."""
    assert launch.ORCA_AGENT == "claude"


@pytest.mark.parametrize(
    "prompt",
    [
        "",
        "/sc:issue --claim 0",
        "/sc:issue --claim 09",
        "/sc:issue --claim 1000000000",
        "/sc:issue --claim 9 --dangerously-skip-permissions",
        "/sc:issue --claim 9\n",
        "/sc:issue --claim 9\n/sc:issue --claim 10",
        " /sc:issue --claim 9",
        "/sc:issue --claim 9 ",
        "/sc:issue --claim -9",
        "/sc:issue --claim 9; id",
        "/sc:issue --claim $(id)",
        "/sc:issue --claim 9`id`",
        "/sc:issue --claim ９",
        "/SC:ISSUE --claim 9",
        "delete everything",
        None,
        9,
        b"/sc:issue --claim 9",
    ],
)
def test_ac7_launch_argv_refuses_any_prompt_not_from_build_claim_prompt__fr012_t1(
    prompt,
):
    """AC-7 FR-012 T1: ``launch_argv`` raises for every non-conforming prompt."""
    with pytest.raises(ValueError):
        launch_argv(ORCA, WORKTREE, prompt)


# --- retry argv (FR-015, design 741) -------------------------------------------


def test_ac9_retry_argv_puts_retry_launch_right_before_json__fr015():
    """AC-9 FR-015: ``--retry-launch <id>`` sits immediately before ``--json``."""
    argv = retry_argv(ORCA, WORKTREE, PROMPT, "op-1")
    assert argv == [
        "/opt/orca/bin/orca-ide",
        "agent",
        "launch",
        "--agent",
        "claude",
        "--worktree",
        "path:/work/tree",
        "--surface",
        "terminal",
        "--prompt",
        "/sc:issue --claim 9",
        "--retry-launch",
        "op-1",
        "--json",
    ]
    assert argv[-3:] == ["--retry-launch", "op-1", "--json"]


@pytest.mark.parametrize(
    "operation_id",
    ["", "op 1", "op;1", "$(id)", "a/b", "x" * 129, "op\n1", None, 1, b"op-1"],
)
def test_ac9_retry_argv_refuses_an_unsafe_operation_id__fr015(operation_id):
    """AC-9 FR-015: an id that could carry shell text never reaches the argv."""
    with pytest.raises(ValueError):
        retry_argv(ORCA, WORKTREE, PROMPT, operation_id)


@pytest.mark.parametrize("operation_id", ["a", "op-1", "A.b_c:d-9", "x" * 128])
def test_ac9_retry_argv_accepts_a_safe_operation_id__fr015(operation_id):
    """AC-9 FR-015: ids of 1 to 128 characters from the allowed set are kept."""
    assert retry_argv(ORCA, WORKTREE, PROMPT, operation_id)[-3:] == [
        "--retry-launch",
        operation_id,
        "--json",
    ]


def test_ac9_operation_id_pattern_matches_the_one_the_record_layer_enforces__fr015():
    """AC-9 FR-015: ``launch`` cannot import ``predicates`` (design 5.3), so it keeps a
    copy of the operation-id pattern; the two must never drift apart."""
    assert (
        launch.OPERATION_ID_PATTERN.pattern == predicates.OPERATION_ID_PATTERN.pattern
    )
    assert launch.OPERATION_ID_PATTERN.flags == predicates.OPERATION_ID_PATTERN.flags


def test_ac9_retry_argv_still_refuses_a_bad_prompt__fr015():
    """AC-9 FR-015: the retry argv checks the prompt as ``launch_argv`` does."""
    with pytest.raises(ValueError):
        retry_argv(ORCA, WORKTREE, "/sc:issue --claim 0", "op-1")


# --- Orca probe (FR-013, T17, DF-36, DF-54) -------------------------------------

ORCA_IDE = "/usr/local/bin/orca-ide"
ORCA_PLAIN = "/usr/bin/orca"
PROBE_IDE = (ORCA_IDE, "skills", "list", "--json")
PROBE_PLAIN = (ORCA_PLAIN, "skills", "list", "--json")
GOOD_REPLY = json.dumps({"topics": [{"name": "orca-cli"}, {"name": "other"}]})
BAD_REPLY = json.dumps({"topics": [{"name": "screen-reader"}]})


def _which(**found):
    """Return a dict-based ``which``; keys use ``_`` for the ``-`` in ``orca-ide``."""
    table = {name.replace("_", "-"): path for name, path in found.items()}
    return lambda name: table.get(name)


def test_fr013_probe_rejects_the_first_candidate_and_accepts_the_second(fake_runner):
    """FR-013 T17: ``orca-ide`` answers without the topic, ``orca`` is taken."""
    runner = fake_runner(
        {
            PROBE_IDE: result(stdout=BAD_REPLY),
            PROBE_PLAIN: result(stdout=GOOD_REPLY),
        }
    )
    found = find_orca(runner, which=_which(orca_ide=ORCA_IDE, orca=ORCA_PLAIN))
    assert found == "/usr/bin/orca"
    assert runner.calls == [(PROBE_IDE, None), (PROBE_PLAIN, None)]


def test_fr013_probe_tries_orca_ide_before_orca(fake_runner):
    """FR-013: with both binaries valid the first candidate, ``orca-ide``, wins."""
    runner = fake_runner(
        {
            PROBE_IDE: result(stdout=GOOD_REPLY),
            PROBE_PLAIN: result(stdout=GOOD_REPLY),
        }
    )
    found = find_orca(runner, which=_which(orca_ide=ORCA_IDE, orca=ORCA_PLAIN))
    assert found == "/usr/local/bin/orca-ide"
    assert runner.calls == [(PROBE_IDE, None)]


def test_fr013_probe_skips_a_candidate_missing_from_path(fake_runner):
    """FR-013: a candidate ``which`` cannot find is skipped without a probe."""
    runner = fake_runner({PROBE_PLAIN: result(stdout=GOOD_REPLY)})
    found = find_orca(runner, which=_which(orca=ORCA_PLAIN))
    assert found == "/usr/bin/orca"
    assert runner.calls == [(PROBE_PLAIN, None)]


def test_fr013_probe_returns_none_when_no_candidate_is_on_path(fake_runner):
    """FR-013: no binary on PATH means None and no process is started."""
    runner = fake_runner()
    assert find_orca(runner, which=_which()) is None
    assert runner.calls == []


def test_fr013_probe_passes_the_given_timeout_and_the_literal_argv(fake_runner):
    """FR-013: the probe argv is ``[path, skills, list, --json]`` with the timeout."""
    runner = fake_runner({PROBE_PLAIN: result(stdout=GOOD_REPLY)})
    assert find_orca(runner, which=_which(orca=ORCA_PLAIN), timeout=7.5) == ORCA_PLAIN
    assert runner.calls == [(("/usr/bin/orca", "skills", "list", "--json"), None)]
    assert runner.timeouts == [7.5]


def test_fr013_probe_default_timeout_is_ten_seconds(fake_runner):
    """FR-013: without a ``timeout`` argument the probe is bounded by 10 s."""
    runner = fake_runner({PROBE_PLAIN: result(stdout=GOOD_REPLY)})
    find_orca(runner, which=_which(orca=ORCA_PLAIN))
    assert runner.timeouts == [10.0]


def test_df54_probe_which_defaults_to_shutil_which():
    """DF-54: ``which`` is a keyword argument whose default is ``shutil.which``."""
    parameter = inspect.signature(find_orca).parameters["which"]
    assert parameter.default is shutil.which
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY


@pytest.mark.parametrize(
    ("reply", "why"),
    [
        (result(stdout="not json at all"), "non-JSON"),
        (result(stdout=""), "empty stdout"),
        (result(stdout=BAD_REPLY), "no orca-cli topic"),
        (result(stdout=json.dumps({"topics": []})), "empty topics"),
        (result(stdout=json.dumps({})), "no topics key"),
        (result(stdout=json.dumps({"topics": ["orca-cli"]})), "str element"),
        (result(stdout=json.dumps({"topics": [None]})), "null element"),
        (result(stdout=json.dumps({"topics": [["orca-cli"]]})), "list element"),
        (result(stdout=json.dumps({"topics": None})), "topics null"),
        (result(stdout=json.dumps({"topics": 5})), "topics int"),
        (result(stdout=json.dumps({"topics": "orca-cli"})), "topics str"),
        (result(stdout=json.dumps({"topics": {"name": "orca-cli"}})), "topics dict"),
        (result(stdout=json.dumps([{"name": "orca-cli"}])), "top-level list"),
        (result(stdout=json.dumps("orca-cli")), "top-level str"),
        (result(stdout=GOOD_REPLY, returncode=1), "non-zero exit"),
        (result(stdout=GOOD_REPLY, timed_out=True), "timed out"),
        (result(stdout=GOOD_REPLY, spawn_error="PermissionError"), "spawn error"),
    ],
    ids=lambda value: value if isinstance(value, str) else "",
)
def test_fr013_probe_rejects_a_reply_that_is_not_orca_cli__t17_df36(
    fake_runner, reply, why
):
    """FR-013 T17 DF-36: every malformed or foreign reply is a reject, never a raise."""
    runner = fake_runner({PROBE_PLAIN: reply})
    assert find_orca(runner, which=_which(orca=ORCA_PLAIN)) is None, why
    assert runner.calls == [(PROBE_PLAIN, None)]


@pytest.mark.parametrize(
    "relative", ["./orca-ide", "orca-ide", "bin/orca-ide", "../orca"]
)
def test_fr013_probe_skips_a_relative_path_without_a_probe__t17(fake_runner, relative):
    """FR-013 T17: ``which`` can return ``./orca-ide``; the launch runs with
    ``cwd`` set to the worktree, so such a path is never probed or returned (B-13)."""
    runner = fake_runner()
    assert find_orca(runner, which=_which(orca_ide=relative, orca=relative)) is None
    assert runner.calls == []


def test_fr013_probe_goes_on_to_the_next_candidate_after_a_relative_path(fake_runner):
    """FR-013 T17: a relative first candidate is skipped; an absolute second is probed."""
    runner = fake_runner({PROBE_PLAIN: result(stdout=GOOD_REPLY)})
    found = find_orca(runner, which=_which(orca_ide="./orca-ide", orca=ORCA_PLAIN))
    assert found == ORCA_PLAIN
    assert runner.calls == [(PROBE_PLAIN, None)]


def test_fr013_probe_returns_the_exact_path_it_probed(fake_runner):
    """FR-013: the returned path is the probed path, so the launch runs what was probed."""
    runner = fake_runner({PROBE_IDE: result(stdout=GOOD_REPLY)})
    found = find_orca(runner, which=_which(orca_ide=ORCA_IDE))
    assert found == ORCA_IDE == runner.calls[0][0][0]


def test_fr013_probe_timeout_none_starts_nothing_and_returns_none(fake_runner):
    """FR-013 NFR-008: ``timeout=None`` returns None and the runner records no call."""
    runner = fake_runner()
    found = find_orca(
        runner, which=_which(orca_ide=ORCA_IDE, orca=ORCA_PLAIN), timeout=None
    )
    assert found is None
    assert runner.calls == []
    assert runner.timeouts == []


def test_fr013_probe_timeout_callable_is_asked_before_each_probe_and_none_stops(
    fake_runner,
):
    """FR-013 NFR-008: a callable ``timeout`` is called right before each probe;
    its None (no time left) ends the search before the second candidate starts."""
    runner = fake_runner(
        {
            PROBE_IDE: result(stdout=BAD_REPLY),
            PROBE_PLAIN: result(stdout=GOOD_REPLY),
        }
    )
    answers = iter([7.0, None])
    asked_after_calls = []

    def allowance():
        asked_after_calls.append(len(runner.calls))
        return next(answers)

    found = find_orca(
        runner, which=_which(orca_ide=ORCA_IDE, orca=ORCA_PLAIN), timeout=allowance
    )
    assert found is None
    assert asked_after_calls == [
        0,
        1,
    ]  # asked before the first, and again before the second
    assert runner.calls == [(PROBE_IDE, None)]
    assert runner.timeouts == [7.0]


def test_fr013_probe_timeout_callable_gives_each_probe_its_own_allowance(fake_runner):
    """FR-013 NFR-008: the second probe gets the callable's second value."""
    runner = fake_runner(
        {
            PROBE_IDE: result(stdout=BAD_REPLY),
            PROBE_PLAIN: result(stdout=GOOD_REPLY),
        }
    )
    answers = iter([9.0, 4.5])
    found = find_orca(
        runner,
        which=_which(orca_ide=ORCA_IDE, orca=ORCA_PLAIN),
        timeout=lambda: next(answers),
    )
    assert found == ORCA_PLAIN
    assert runner.timeouts == [9.0, 4.5]


def test_fr013_probe_timeout_callable_is_not_asked_for_a_skipped_candidate(
    fake_runner,
):
    """FR-013 B-13: a candidate that is missing or relative starts no probe and asks nothing."""
    runner = fake_runner({PROBE_PLAIN: result(stdout=GOOD_REPLY)})
    asked = []

    def allowance():
        asked.append(1)
        return 3.0

    found = find_orca(
        runner, which=_which(orca_ide="./orca-ide", orca=ORCA_PLAIN), timeout=allowance
    )
    assert found == ORCA_PLAIN
    assert asked == [1]
    assert runner.timeouts == [3.0]


@pytest.mark.parametrize("bad", [0, -1.0, True, "5", float("nan")])
def test_fr013_probe_timeout_callable_result_is_validated_per_probe(fake_runner, bad):
    """FR-013: a callable's number must be positive like a plain timeout; no probe starts."""
    runner = fake_runner()
    with pytest.raises(ValueError):
        find_orca(runner, which=_which(orca_ide=ORCA_IDE), timeout=lambda: bad)
    assert runner.calls == []


# --- origin parsing (FR-025, NFR-003) --------------------------------------------


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/IronbellyOrg/IronClaude",
        "https://github.com/IronbellyOrg/IronClaude.git",
        "https://github.com/IronbellyOrg/IronClaude/",
        "https://github.com/IronbellyOrg/IronClaude.git/",
        "git@github.com:IronbellyOrg/IronClaude",
        "git@github.com:IronbellyOrg/IronClaude.git",
        "git@github.com:IronbellyOrg/IronClaude/",
        "https://github.com/IronbellyOrg/IronClaude\n",
    ],
)
def test_ac16_parse_origin_positive_table__fr025_nfr003(url):
    """AC-16 FR-025 NFR-003: the https and ssh forms give ``owner/repo``."""
    assert parse_origin(url) == "IronbellyOrg/IronClaude"


@pytest.mark.parametrize(
    "url",
    [
        "https://gitlab.com/IronbellyOrg/IronClaude.git",
        "git@bitbucket.org:IronbellyOrg/IronClaude.git",
        "https://github.com/IronbellyOrg",
        "/srv/git/IronClaude.git",
        "",
    ],
)
def test_ac16_parse_origin_negative_table__fr025_nfr003(url):
    """AC-16 FR-025 NFR-003: other hosts, a missing repo, a path and "" give None."""
    assert parse_origin(url) is None


@pytest.mark.parametrize(
    "url",
    [
        "ssh://git@github.com/IronbellyOrg/IronClaude.git",
        "http://github.com/IronbellyOrg/IronClaude",
        "https://user@github.com/IronbellyOrg/IronClaude",
        "https://GitHub.com/IronbellyOrg/IronClaude",
        "git@GitHub.com:IronbellyOrg/IronClaude",
    ],
)
def test_ac16_parse_origin_refuses_forms_the_original_does_not_accept__fr025(url):
    """AC-16 FR-025: ssh://, http://, a userinfo https and an upper-case host give None."""
    assert parse_origin(url) is None


@pytest.mark.parametrize(
    "value", [None, 5, b"https://github.com/IronbellyOrg/IronClaude"]
)
def test_ac16_parse_origin_non_str_is_none__fr025(value):
    """AC-16 FR-025: a value that is not a ``str`` gives None."""
    assert parse_origin(value) is None


# --- origin check (FR-025, DF-01) --------------------------------------------------


def _origin_script(worktree: Path, reply):
    """Return the script for the one ``git remote get-url origin`` call."""
    key = ("git", "-C", str(worktree), "remote", "get-url", "origin")
    return key, {key: reply}


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/IronbellyOrg/IronClaude\n",
        "https://github.com/IronbellyOrg/IronClaude.git\n",
        "git@github.com:IronbellyOrg/IronClaude.git\n",
        "https://github.com/IRONBELLYORG/IRONCLAUDE\n",
        "git@github.com:ironbellyorg/ironclaude\n",
    ],
)
def test_ac16_check_origin_matches_the_fork__fr025(fake_runner, tmp_path, url):
    """AC-16 FR-025: the fork's https, ssh and upper-case forms all match."""
    key, script = _origin_script(tmp_path, result(stdout=url))
    runner = fake_runner(script)
    assert check_origin(runner, tmp_path, 10.0) is None
    assert runner.calls == [(key, None)]
    assert runner.timeouts == [10.0]


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/IronbellyOrg/Other\n",
        "https://github.com/SuperClaude-Org/SuperClaude_Framework\n",
        "git@github.com:SuperClaude-Org/SuperClaude_Framework.git\n",
        "https://github.com/IronbellyOrg\n",
        "https://gitlab.com/IronbellyOrg/IronClaude\n",
    ],
)
def test_ac16_check_origin_mismatch_for_another_repository__fr025_nfr003(
    fake_runner, tmp_path, url
):
    """AC-16 FR-025 NFR-003: another repository or the upstream gives origin_mismatch."""
    _, script = _origin_script(tmp_path, result(stdout=url))
    runner = fake_runner(script)
    assert check_origin(runner, tmp_path, 10.0) == "origin_mismatch"


@pytest.mark.parametrize(
    "reply",
    [
        result(timed_out=True),
        result(stdout="https://github.com/IronbellyOrg/IronClaude\n", returncode=128),
        result(stdout="garbage output with no url"),
        result(stdout=""),
        result(spawn_error="FileNotFoundError"),
    ],
    ids=["timeout", "non-zero-exit", "garbage", "empty", "spawn-error"],
)
def test_ac16_check_origin_failures_are_origin_mismatch__fr025(
    fake_runner, tmp_path, reply
):
    """AC-16 FR-025: a timeout, failed git or garbage output is origin_mismatch."""
    _, script = _origin_script(tmp_path, reply)
    runner = fake_runner(script)
    assert check_origin(runner, tmp_path, 10.0) == "origin_mismatch"


def test_ac16_check_origin_argv_is_literal_with_no_cwd__fr025_df01(
    fake_runner, tmp_path
):
    """AC-16 FR-025 DF-01: ``git -C <abs> remote get-url origin`` and ``cwd`` None."""
    worktree = tmp_path / "wt"
    runner = fake_runner(
        {
            (
                "git",
                "-C",
                str(worktree),
                "remote",
                "get-url",
                "origin",
            ): result(stdout="https://github.com/IronbellyOrg/IronClaude\n")
        }
    )
    assert worktree.is_absolute()
    assert check_origin(runner, worktree, 4.0) is None
    assert runner.calls == [
        (("git", "-C", str(worktree), "remote", "get-url", "origin"), None)
    ]
    assert runner.timeouts == [4.0]


def test_ac16_check_origin_takes_a_str_worktree_too__fr025(fake_runner, tmp_path):
    """AC-16 FR-025: a ``str`` worktree builds the same argv as a ``Path``."""
    key, script = _origin_script(
        tmp_path, result(stdout="git@github.com:IronbellyOrg/IronClaude\n")
    )
    runner = fake_runner(script)
    assert check_origin(runner, str(tmp_path), 10.0) is None
    assert runner.calls == [(key, None)]


def test_ac16_check_origin_timeout_none_starts_nothing__fr025_nfr008(
    fake_runner, tmp_path
):
    """AC-16 FR-025 NFR-008: ``timeout=None`` is origin_mismatch with no runner call."""
    runner = fake_runner()
    assert check_origin(runner, tmp_path, None) == "origin_mismatch"
    assert runner.calls == []
    assert runner.timeouts == []


# ==============================================================================
# Part B: launcher outcomes, operation id and the agent pin (design 8.4 lines
# 627-636 and 9.2 line 689; decisions DF-01, DF-11, OQ-40, OQ-47).
# ==============================================================================

FIXTURES = Path(__file__).parent / "fixtures" / "_assumed_shape"
OP_ID = "op-test-0001"
OP_UNKNOWN = "agent_session_operation_unknown"
EXPECTED_AGENT = (
    "claude"  # decision DF-11: the literal lives here, never read from .dev/
)


def _fixture(name: str) -> dict:
    """Return one ``_assumed_shape`` fixture as a dict."""
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _success_result():
    """The exit-0 reply the success fixture describes, as a ``CommandResult``."""
    fixture = _fixture("orca_launch_success.json")
    return result(stdout=json.dumps(fixture["payload"]))


def _unknown_result():
    """The lost-reply error the unknown fixture describes (JSON text in stderr)."""
    fixture = _fixture("orca_launch_unknown.json")
    return result(stderr=fixture["stderr"], returncode=fixture["exit"])


def _success_payload() -> dict:
    """A private copy of the success fixture's reply object."""
    return copy.deepcopy(_fixture("orca_launch_success.json")["payload"])


def _id_holder(payload: dict) -> tuple[dict, str]:
    """Return the dict that holds the id at ``OPERATION_ID_PATHS[0]`` and its key."""
    *parents, last = OPERATION_ID_PATHS[0]
    node = payload
    for key in parents:
        node = node[key]
    return node, last


def _id_reply(operation_id: object) -> str:
    """Return launch stdout: the success fixture with ``operation_id`` at its path.

    No Orca reply shape is written in this file (design 636, 840, 847): the body
    comes from ``orca_launch_success.json`` and ``OPERATION_ID_PATHS[0]``, so a
    changed path or a replaced fixture (FU-1) is followed here.
    """
    payload = _success_payload()
    holder, key = _id_holder(payload)
    holder[key] = operation_id
    return json.dumps(payload)


def _no_id_reply() -> str:
    """Return launch stdout: the success fixture with the id removed."""
    payload = _success_payload()
    holder, key = _id_holder(payload)
    del holder[key]
    return json.dumps(payload)


# --- outcome table (design 629-634) ----------------------------------------------


def test_ac8_spawn_error_gives_spawn_error__fr013_fr014():
    """AC-8 FR-013 FR-014: a runner ``spawn_error`` maps to kind ``spawn_error``."""
    got = outcome_of(result(spawn_error="FileNotFoundError"))
    assert got == LaunchOutcome("spawn_error", None, "spawn_error")


def test_ac8_timed_out_gives_unknown_with_detail_timeout__fr013_fr014():
    """AC-8 FR-013 FR-014: ``timed_out`` is ``unknown`` with detail ``timeout``."""
    got = outcome_of(result(timed_out=True))
    assert got == LaunchOutcome("unknown", None, "timeout")


def test_ac8_success_fixture_gives_launched_with_its_operation_id__fr013_fr014():
    """AC-8 FR-013 FR-014: the success fixture is ``launched`` with the stored id."""
    got = outcome_of(_success_result())
    assert got == LaunchOutcome("launched", OP_ID, "ok")
    holder, key = _id_holder(_success_payload())
    assert got.operation_id == holder[key]


def test_ac8_exit_zero_without_an_id_is_unknown__fr014():
    """AC-8 FR-014: exit 0 and a JSON object with no id at any path is unknown."""
    stdout = _no_id_reply()
    assert OP_ID not in stdout
    got = outcome_of(result(stdout=stdout))
    assert got == LaunchOutcome("unknown", None, "no_operation_id")


@pytest.mark.parametrize("stdout", ["", "launched", "{not json", "[1, 2]", '"op-1"'])
def test_ac8_non_json_or_non_object_stdout_is_unknown__fr014(stdout):
    """AC-8 FR-014: stdout that is not a JSON object is unknown, never launched."""
    got = outcome_of(result(stdout=stdout))
    assert got == LaunchOutcome("unknown", None, "non_json")


def test_ac8_non_zero_exit_is_unknown_even_with_a_success_body__fr014():
    """AC-8 FR-014: exit 1 is unknown; an id parsed from stdout is kept."""
    got = outcome_of(result(stdout=_id_reply(OP_ID), returncode=1))
    assert got == LaunchOutcome("unknown", OP_ID, "exit_nonzero")


def test_ac8_non_zero_exit_without_an_id_is_unknown__fr014():
    """AC-8 FR-014: a plain failure (exit 2, empty stdout) is unknown, id None."""
    got = outcome_of(result(stderr="boom", returncode=2))
    assert got == LaunchOutcome("unknown", None, "exit_nonzero")


@pytest.mark.parametrize(
    ("stdout", "stderr"),
    [
        (OP_UNKNOWN, ""),
        ("", OP_UNKNOWN),
        (_id_reply(OP_ID) + OP_UNKNOWN, ""),
        (_id_reply(OP_ID), f"error: {OP_UNKNOWN}"),
    ],
    ids=["stdout", "stderr", "stdout-with-id", "stderr-with-id"],
)
def test_ac8_op_unknown_text_in_either_stream_is_unknown__fr014(stdout, stderr):
    """AC-8 FR-014: the lost-reply code wins at exit 0, even with an id present."""
    got = outcome_of(result(stdout=stdout, stderr=stderr, returncode=0))
    assert got.kind == "unknown"
    assert got.detail == "op_unknown"


def test_ac8_op_unknown_wins_over_a_valid_success_reply__fr014():
    """AC-8 FR-014: exit 0 with a valid id is not ``launched`` when the code shows."""
    reply = result(stdout=_id_reply(OP_ID), stderr=OP_UNKNOWN, returncode=0)
    got = outcome_of(reply)
    assert got.kind == "unknown"
    assert got.kind != "launched"
    assert got.operation_id == OP_ID


@pytest.mark.parametrize(
    "bad_id",
    ["bad id", "a;b", "$(id)", "a/b", "op\n1", "x" * 129, "", 123, ["op-1"], True],
)
def test_ac9_invalid_operation_id_gives_unknown_with_none__fr014_fr015(bad_id):
    """AC-9 FR-014 FR-015: an id failing the pattern is dropped; the outcome is unknown."""
    got = outcome_of(result(stdout=_id_reply(bad_id)))
    assert got == LaunchOutcome("unknown", None, "operation_id_invalid")


@pytest.mark.parametrize("good_id", ["a", "A.b_c:d-9", "x" * 128])
def test_ac9_boundary_operation_ids_are_launched__fr014_fr015(good_id):
    """AC-9 FR-014 FR-015: ids of 1 to 128 allowed characters are kept as ``launched``."""
    got = outcome_of(result(stdout=_id_reply(good_id)))
    assert got == LaunchOutcome("launched", good_id, "ok")


def test_ac9_invalid_operation_id_with_op_unknown_text_stores_none__fr015():
    """AC-9 FR-015: the lost-reply code plus an unsafe id still stores ``None``."""
    got = outcome_of(result(stdout=_id_reply("bad id"), stderr=OP_UNKNOWN))
    assert got == LaunchOutcome("unknown", None, "op_unknown")


# --- the unknown fixture and OQ-47 -----------------------------------------------


def test_ac9_unknown_fixture_keeps_its_id_from_the_json_text_in_stderr__fr014_fr015():
    """AC-9 FR-014 FR-015: the id is read from stderr's JSON through ``OPERATION_ID_PATHS``."""
    fixture = _fixture("orca_launch_unknown.json")
    reply = _unknown_result()
    assert reply.stdout == ""
    assert OP_UNKNOWN in reply.stderr
    got = outcome_of(reply)
    assert got == LaunchOutcome("unknown", OP_ID, "op_unknown")
    node: object = json.loads(fixture["stderr"])
    for key in OPERATION_ID_PATHS[1]:
        node = node[key]
    assert node == got.operation_id


@pytest.mark.parametrize(
    ("stdout", "stderr"),
    [
        ("", f"{OP_UNKNOWN}: operation op-test-0002 lost"),
        ("", f"{OP_UNKNOWN} op-test-0002"),
        (f"{OP_UNKNOWN} op-test-0002", ""),
        ("", f"operation_id=op-test-0002 {OP_UNKNOWN}"),
    ],
    ids=["colon", "space", "stdout", "key-value"],
)
def test_ac9_plain_text_never_yields_an_id__fr014_fr015_oq47(stdout, stderr):
    """AC-9 FR-014 FR-015 OQ-47: an id-like token in plain text is never scraped."""
    got = outcome_of(result(stdout=stdout, stderr=stderr, returncode=1))
    assert got == LaunchOutcome("unknown", None, "op_unknown")
    assert "op-test-0002" not in repr(got)


# --- cwd (DF-01) ---------------------------------------------------------------------


def test_ac8_launch_runner_call_records_cwd_equal_to_the_worktree__fr013_df01(
    fake_runner, tmp_path
):
    """AC-8 FR-013 DF-01: the launch runs the 12-element argv with ``cwd=str(worktree)``."""
    argv = launch_argv(ORCA, tmp_path, PROMPT)
    runner = fake_runner({tuple(argv): _success_result()})
    got = OrcaLauncher(runner).launch(ORCA, tmp_path, PROMPT, 120.0)
    assert got == LaunchOutcome("launched", OP_ID, "ok")
    assert runner.calls == [(tuple(argv), str(tmp_path))]
    assert runner.timeouts == [120.0]


def test_ac8_launch_maps_the_unknown_fixture_through_the_runner__fr014(
    fake_runner, tmp_path
):
    """AC-8 FR-014: ``OrcaLauncher.launch`` returns ``outcome_of`` of the runner reply."""
    argv = launch_argv(ORCA, tmp_path, PROMPT)
    runner = fake_runner({tuple(argv): _unknown_result()})
    got = OrcaLauncher(runner).launch(ORCA, tmp_path, PROMPT, 120.0)
    assert got == LaunchOutcome("unknown", OP_ID, "op_unknown")


def test_ac8_launch_with_a_bad_prompt_or_timeout_starts_nothing__fr012_fr013(
    fake_runner, tmp_path
):
    """AC-8 FR-012 FR-013: an unchecked prompt or timeout raises before the runner."""
    runner = fake_runner()
    launcher = OrcaLauncher(runner)
    with pytest.raises(ValueError):
        launcher.launch(ORCA, tmp_path, "/sc:issue --claim 0", 120.0)
    for timeout in (0, -1, None, True, "120"):
        with pytest.raises(ValueError):
            launcher.launch(ORCA, tmp_path, PROMPT, timeout)
    assert runner.calls == []


def test_df01_only_the_launch_passes_a_cwd__fr013_fr025(fake_runner, tmp_path):
    """FR-013 FR-025 DF-01: ``check_origin`` and ``find_orca`` record ``cwd`` None."""
    origin = ("git", "-C", str(tmp_path), "remote", "get-url", "origin")
    runner = fake_runner(
        {
            origin: result(stdout="https://github.com/IronbellyOrg/IronClaude\n"),
            PROBE_PLAIN: result(stdout=GOOD_REPLY),
            tuple(launch_argv(ORCA, tmp_path, PROMPT)): _success_result(),
        }
    )
    assert check_origin(runner, tmp_path, 10.0) is None
    assert find_orca(runner, which=_which(orca=ORCA_PLAIN)) == ORCA_PLAIN
    OrcaLauncher(runner).launch(ORCA, tmp_path, PROMPT, 120.0)
    assert [cwd for _, cwd in runner.calls] == [None, None, str(tmp_path)]


# --- operation id paths (design 636) ---------------------------------------------------


def test_ac9_operation_id_paths_are_tuples_of_strings__fr015():
    """AC-9 FR-015: ``OPERATION_ID_PATHS`` is a tuple of non-empty string tuples."""
    assert isinstance(OPERATION_ID_PATHS, tuple)
    assert len(OPERATION_ID_PATHS) >= 2
    for path in OPERATION_ID_PATHS:
        assert isinstance(path, tuple)
        assert path
        assert all(isinstance(key, str) and key for key in path)


def test_ac9_success_fixture_resolves_through_the_first_path__fr015():
    """AC-9 FR-015: ``orca_launch_success.json`` holds its id at ``OPERATION_ID_PATHS[0]``."""
    node: object = _fixture("orca_launch_success.json")["payload"]
    for key in OPERATION_ID_PATHS[0]:
        assert isinstance(node, dict) and key in node
        node = node[key]
    assert node == OP_ID


def test_ac9_no_operation_id_fixture_has_no_id_at_any_path__fr014_fr015():
    """FR-014 FR-015: ``orca_launch_no_operation_id.json`` yields no id at any path.

    Gate C fix C-4: ``test_cycle.py`` builds its "launched but no id" reply from
    this fixture, so a changed ``OPERATION_ID_PATHS`` cannot leave it passing for
    the wrong reason.
    """
    reply = _fixture("orca_launch_no_operation_id.json")["payload"]
    for path in OPERATION_ID_PATHS:
        node: object = reply
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
        assert node is None, path
    assert outcome_of(result(stdout=json.dumps(reply))) == LaunchOutcome(
        "unknown", None, "no_operation_id"
    )


def test_ac9_empty_operation_id_fixture_holds_the_empty_string_at_the_first_path__fr014():
    """FR-014 FR-015: ``orca_launch_empty_operation_id.json`` has "" at path 0."""
    reply = _fixture("orca_launch_empty_operation_id.json")["payload"]
    node: object = reply
    for key in OPERATION_ID_PATHS[0]:
        assert isinstance(node, dict) and key in node
        node = node[key]
    assert node == ""
    assert outcome_of(result(stdout=json.dumps(reply))) == LaunchOutcome(
        "unknown", None, "operation_id_invalid"
    )


# --- agent pin (DF-11, DF-31) ----------------------------------------------------------


def test_ac8_orca_agent_is_pinned_to_the_literal_claude__fr013_df11():
    """AC-8 FR-013 DF-11: the agent id equals the literal held in this file."""
    assert EXPECTED_AGENT == "claude"
    assert ORCA_AGENT == "claude"
    assert ORCA_AGENT == EXPECTED_AGENT
    assert launch_argv(ORCA, WORKTREE, PROMPT)[4] == EXPECTED_AGENT
