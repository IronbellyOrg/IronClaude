"""Live observations for the launch-level hook (issue #394), and tests of the log-only probe.

The ship gate (``launch.GOVERNED_LEVELS_ALLOWED``) is opened by the commit that holds the
committed evidence under ``.dev/launch-level-observations/evidence/``. The tests below
read that evidence and assert the pass criteria of
``.dev/launch-level-observations/plan.md`` (sections 4 to 6) and
``.dev/launch-level-observations/obs-ctx-plan.md`` (section 7). They check the shape of
the files; the review of the commit checks that the files are real.

Still pending (skipped, not run): OB-H1 items 2, 3, 4, 6, 7, 8 and 9. The synthetic
payloads in fixtures/launch_level/ob_h1 are not observations.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "launch_level" / "ob_h1"
PROBE = FIXTURES / "log-only-probe.sh"
BASH = shutil.which("bash") or "/bin/bash"
EVIDENCE = (
    Path(__file__).resolve().parents[2]
    / ".dev"
    / "launch-level-observations"
    / "evidence"
)
CHECKER = (
    Path(__file__).resolve().parent / "fixtures" / "launch_level" / "ob_ctx_check.py"
)
MARKER = re.compile(r"^\[sc-launch:v1:[0-9a-f]{32}\] ")
RELEASE = re.compile(r"/(sc:implement|task)(\s|$)")  # design section 6, FR-L-16


def _run_probe(payload: bytes, log: str | None, tmp_path: Path):
    env = {k: v for k, v in os.environ.items() if k != "LAUNCH_LEVEL_PROBE_LOG"}
    env["HOME"] = str(tmp_path)
    if log is not None:
        env["LAUNCH_LEVEL_PROBE_LOG"] = log
    return subprocess.run(
        [BASH, str(PROBE)], input=payload, capture_output=True, env=env, timeout=10
    )


def test_fixtures_are_nine_json_objects_with_an_event_name():
    files = sorted(FIXTURES.glob("item[1-9]-*.json"))
    assert [f.name[4] for f in files] == list("123456789")
    for f in files:
        data = json.loads(f.read_text())
        assert isinstance(data, dict) and isinstance(data["hook_event_name"], str), (
            f.name
        )
    assert (FIXTURES / "README.md").is_file()
    assert os.access(PROBE, os.X_OK)


def test_probe_appends_exactly_one_line_per_call(tmp_path):
    log = tmp_path / "probe.log"
    payload = (FIXTURES / "item2-skill-keys.json").read_bytes()
    for count in (1, 2):
        result = _run_probe(payload, str(log), tmp_path)
        assert result.returncode == 0
        assert result.stdout == b"" and result.stderr == b""
        lines = log.read_text().splitlines()
        assert len(lines) == count
    assert json.loads(lines[-1])["tool_name"] == "Skill"


def test_probe_flattens_a_multiline_payload_to_one_line(tmp_path):
    log = tmp_path / "probe.log"
    pretty = json.dumps(
        {"hook_event_name": "PreToolUse", "session_id": "s"}, indent=2
    ).encode()
    assert _run_probe(pretty, str(log), tmp_path).returncode == 0
    assert len(log.read_text().splitlines()) == 1


def test_probe_with_log_path_unset_prints_nothing_and_exits_zero(tmp_path):
    result = _run_probe(b'{"hook_event_name": "PreToolUse"}', None, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert list(tmp_path.iterdir()) == []


def test_probe_with_unwritable_log_path_exits_zero_silently(tmp_path):
    target_dir = tmp_path / "a-directory"
    target_dir.mkdir()
    for bad in (str(target_dir), str(tmp_path / "missing" / "dir" / "probe.log")):
        result = _run_probe(b'{"hook_event_name": "PreToolUse"}', bad, tmp_path)
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


# Observations that have not been run. The five that were run are no longer listed;
# each has its own evidence test below.
_PENDING = [f"OB-H1 item {n}" for n in (2, 3, 4, 6, 7, 8, 9)]


_GATE_ITEMS = ("OB-H1 item 1", "OB-H1 item 5", "OB-H2", "OB-H3", "OB-CTX")


def _gate_may_be_open(gate: bool, pending: list[str]) -> bool:
    """R33: the watcher's ship gate may be True only when no gate item is pending."""
    return not gate or not any(item in pending for item in _GATE_ITEMS)


def test_the_ship_gate_coupling_rule_itself__r33():
    assert _gate_may_be_open(False, list(_GATE_ITEMS))  # closed gate: always fine
    assert not _gate_may_be_open(True, list(_GATE_ITEMS))  # open, all pending
    assert _gate_may_be_open(True, _PENDING)  # the pending ones are not gate items
    for item in _GATE_ITEMS:  # any one of the five blocks it
        assert not _gate_may_be_open(True, [item])
    assert _gate_may_be_open(True, ["OB-H1 item 2"])  # none of the five


def test_the_ship_gate_opens_only_when_its_observations_are_run__r33():
    """A commit that flips ``launch.GOVERNED_LEVELS_ALLOWED`` while OB-H1 items 1 and
    5, OB-H2, OB-H3 or OB-CTX are still pending (skipped here) fails this test, so the
    gate opens in the commit that runs the observations."""
    from superclaude.cli.issue_watch import launch

    assert launch.GOVERNED_LEVELS_ALLOWED is True
    assert _gate_may_be_open(launch.GOVERNED_LEVELS_ALLOWED, _PENDING), (
        "GOVERNED_LEVELS_ALLOWED is True while its observations are still pending"
    )


# -- evidence readers ---------------------------------------------------------------


def _text(name: str) -> str:
    return (EVIDENCE / name).read_text(encoding="utf-8")


def _jsonl(name: str) -> list[dict]:
    return [json.loads(line) for line in _text(name).splitlines() if line.strip()]


def _probe_rows(name: str, sid: str | None = None) -> list[tuple[list[str], dict]]:
    """Rows of a probe TSV (column 4 is the hook payload), optionally of one session."""
    rows = []
    for line in _text(name).splitlines():
        cols = line.split("\t")
        event = json.loads(cols[3])
        if sid is None or event["session_id"] == sid:
            rows.append((cols, event))
    return rows


def _bash_commands(name: str, sid: str) -> dict[str, bool]:
    """Every Bash PreToolUse command of one session, mapped to: did a PostToolUse follow?

    A PreToolUse with no PostToolUse for the same ``tool_use_id`` is a refused call.
    """
    everything = [e for _, e in _probe_rows(name)]
    posted = {
        e["tool_use_id"] for e in everything if e["hook_event_name"] == "PostToolUse"
    }
    return {
        e["tool_input"]["command"]: e["tool_use_id"] in posted
        for e in everything
        if e["session_id"] == sid
        and e["hook_event_name"] == "PreToolUse"
        and e.get("tool_name") == "Bash"
    }


def _skill_calls(name: str, sid: str) -> list[bool]:
    """Every Skill PreToolUse of one session: did a PostToolUse follow it?"""
    everything = [e for _, e in _probe_rows(name)]
    posted = {
        e["tool_use_id"] for e in everything if e["hook_event_name"] == "PostToolUse"
    }
    return [
        e["tool_use_id"] in posted
        for e in everything
        if e["session_id"] == sid
        and e["hook_event_name"] == "PreToolUse"
        and e.get("tool_name") == "Skill"
    ]


def _first_prompt(name: str, sid: str) -> str:
    return next(
        e["prompt"]
        for _, e in _probe_rows(name, sid)
        if e["hook_event_name"] == "UserPromptSubmit"
    )


# -- OB-H1 ------------------------------------------------------------------------


def test_ob_h1_item_1_subagent_and_nested_lines_carry_the_main_session_id():
    """Reads evidence/ob-h1-item1.jsonl (plan section 4.1): the PreToolUse lines of
    `echo SUB` and `echo NESTED` carry the session_id of `echo MAIN` and an agent_id."""
    lines = _jsonl("ob-h1-item1.jsonl")

    def pre(word: str) -> list[dict]:
        return [
            e
            for e in lines
            if e["hook_event_name"] == "PreToolUse"
            and e.get("tool_name") == "Bash"
            and e["tool_input"].get("command") == f"echo {word}"
        ]

    main, sub, nested = pre("MAIN"), pre("SUB"), pre("NESTED")
    assert (len(main), len(sub), len(nested)) == (1, 1, 1)
    sid = main[0]["session_id"]
    assert isinstance(sid, str) and sid and "agent_id" not in main[0]
    for event in (sub[0], nested[0]):
        assert event["session_id"] == sid
        assert isinstance(event["agent_id"], str) and event["agent_id"]
        assert isinstance(event["agent_type"], str) and event["agent_type"]
    assert sub[0]["agent_id"] != nested[0]["agent_id"]
    assert {e["session_id"] for e in lines} == {sid}  # no identity loss anywhere


def test_ob_h1_item_5_self_started_turns_are_wrapped_and_none_releases():
    """Reads evidence/ob-h1-item5.jsonl (plan section 4.2): each self-started turn (the
    background Bash, the Monitor line `approved`, the background subagent) arrives
    wrapped in <task-notification>; none is exactly `approved` or matches the release
    pattern on its first line."""
    prompts = [
        e["prompt"]
        for e in _jsonl("ob-h1-item5.jsonl")
        if e["hook_event_name"] == "UserPromptSubmit"
    ]
    typed, *self_started = prompts
    assert not typed.startswith("<task-notification>")  # the person's own prompt
    assert len(self_started) == 3
    for prompt in self_started:
        assert prompt.startswith("<task-notification>")
        assert prompt.strip() != "approved"
        assert not RELEASE.match(prompt.split("\n", 1)[0])
    assert any("approved" in p for p in self_started)  # the Monitor line, wrapped


# -- OB-H2 ------------------------------------------------------------------------


def test_ob_h2_the_real_claim_was_bound_before_its_first_tool_call():
    """Reads evidence/ob-h2-real-claim-827-probe.tsv and ob-h2-real-claim-827-notes.md
    (plan section 5.3): the first prompt starts with the launch marker, HOME and
    CLAUDE_CONFIG_DIR are the supported ones, and the first tool call came seconds after
    the first prompt. The bind time itself (session file ctime equal to the first prompt
    line) is stated in the notes: this file's store column is empty."""
    rows = _probe_rows("ob-h2-real-claim-827-probe.tsv")
    assert len({e["session_id"] for _, e in rows}) == 1
    first_cols, first = rows[0]
    assert first["hook_event_name"] == "UserPromptSubmit"
    assert MARKER.match(first["prompt"])
    assert first["prompt"].endswith(
        "Read .dev/issues/827/launch-prompt.md and follow it."
    )
    assert {(c[1], c[2]) for c, _ in rows} == {("/home/coder", "unset")}
    first_tool = next(c for c, e in rows if e["hook_event_name"] == "PreToolUse")
    assert int(first_tool[0]) - int(first_cols[0]) >= 1_000_000_000  # ns
    notes = _text("ob-h2-real-claim-827-notes.md")
    assert "enforcement_hook installed" in notes
    assert "Bound 9 s before the first tool call" in notes
    assert "no Orca preamble precedes it" in notes


# -- OB-H3 ------------------------------------------------------------------------

_W_SID = "dc89127a-e029-4467-ac38-05a18a5f5b8c"
_F_SID = "3852709b-a75d-4700-b122-1bad0f82d54c"
_FS_SID = "937bb62b-a218-4168-96c1-f46b8552000f"


def test_ob_h3_w_the_commit_and_implement_are_refused_and_no_commit_landed():
    """Reads evidence/ob-h3-W-issue-829-probe.tsv, ob-h3-W-refusal-texts.txt and
    ob-h3-W-notes.md (plan section 6.2): both `git commit` calls have no PostToolUse,
    `git status` ran, Skill calls were refused until `/sc:implement x` unlocked one, and
    the refusal header names level worktree (approved after the unlock). The text file
    holds the five guard refusals with their Blocked lines; the notes quote two of them."""
    sid = _W_SID
    assert MARKER.match(_first_prompt("ob-h3-W-issue-829-probe.tsv", sid))
    commands = _bash_commands("ob-h3-W-issue-829-probe.tsv", sid)
    commits = {c: ran for c, ran in commands.items() if c.startswith("git commit")}
    assert len(commits) == 2 and not any(commits.values())  # none ran: no commit landed
    assert commands["git status"] is True
    skills = _skill_calls("ob-h3-W-issue-829-probe.tsv", sid)
    assert skills.count(True) >= 1 and skills.count(False) >= 2
    refusals = _text("ob-h3-W-refusal-texts.txt")
    headers = [x for x in refusals.splitlines() if x.startswith("Launch-level guard:")]
    assert len(headers) == 5  # three commits and two Skill calls refused
    assert all("started by /sc:issue --claim at level worktree" in h for h in headers)
    assert sum("(approved)" in h for h in headers) >= 1  # a commit refused after unlock
    assert refusals.count("Blocked: creating a commit") == 3
    assert refusals.count("Blocked: starting /sc:implement, /task or /sc:cleanup") == 2
    notes = _text("ob-h3-W-notes.md")
    assert "Blocked: creating a commit" in notes
    assert "Blocked: starting /sc:implement, /task or /sc:cleanup" in notes
    assert "No commit landed" in notes and "HEAD unchanged at 4e35750e7" in notes


def test_ob_h3_f_commit_and_push_are_refused_and_routine_git_is_not():
    """Reads evidence/ob-h3-F-issue-841-probe.tsv, ob-h3-F-refusal-texts.txt and
    ob-h3-F-notes.md (plan section 6.3): the typed commit and push have no PostToolUse,
    no git commit or git push of the session ran, and `git status` ran. The Blocked
    lines for F are quoted in the notes; the text file holds the header."""
    sid = _F_SID
    assert MARKER.match(_first_prompt("ob-h3-F-issue-841-probe.tsv", sid))
    commands = _bash_commands("ob-h3-F-issue-841-probe.tsv", sid)
    assert commands["git commit --allow-empty -m probe"] is False
    assert commands["git push --dry-run origin HEAD"] is False
    landed = [
        c for c, ran in commands.items() if ran and re.search(r"git (commit|push)", c)
    ]
    assert landed == []
    assert any(ran and c.startswith("git status") for c, ran in commands.items())
    assert any(_skill_calls("ob-h3-F-issue-841-probe.tsv", sid))  # /sc:implement ran
    header = _text("ob-h3-F-refusal-texts.txt").splitlines()[0]
    assert header.endswith("started by /sc:issue --claim at level full.")
    notes = _text("ob-h3-F-notes.md")
    assert (
        "Blocked: creating a commit (git commit, cherry-pick, revert, am, or moving a "
        "branch with update-ref)." in notes
    )
    assert "Blocked: a git push." in notes
    assert "No commit landed" in notes and "HEAD stayed d3a1059f0" in notes


def test_ob_h3_fs_unsafe_pushes_merge_and_gh_write_are_refused_a_plain_push_is_not():
    """Reads evidence/ob-h3-FS-issue-842-probe.tsv, ob-h3-FS-refusal-texts-first-pass.txt,
    ob-h3-FS-refusal-texts-probes.txt and ob-h3-FS-notes.md (plan section 6.4): the
    piped push, force push, other-remote push, merge and `gh api -X POST` have no
    PostToolUse; the plain `git push origin <branch>` and the commit did. The refusal
    texts hold the Blocked lines of the guard classes and the notes name pull request 845
    on the fork."""
    sid = _FS_SID
    probe = "ob-h3-FS-issue-842-probe.tsv"
    assert MARKER.match(_first_prompt(probe, sid))
    commands = _bash_commands(probe, sid)
    refused = [c for c, ran in commands.items() if not ran]
    for start in (
        "git push origin ironbelly/issue-842 2>&1 | tail -8",
        "git push --force origin",
        "git push /tmp/ll-scratch.",
        "git merge --no-commit --no-ff",
        "gh api -X POST",
    ):
        assert any(c.startswith(start) for c in refused), start
    assert commands["git push origin ironbelly/issue-842"] is True
    assert any(ran and c.startswith("git commit") for c, ran in commands.items())
    first_pass = _text("ob-h3-FS-refusal-texts-first-pass.txt")
    assert first_pass.count("at level full --submit.") == 3
    for blocked in (
        "Blocked: starting or messaging another agent or session",
        "Blocked: touching the launch-level state, the Claude Code settings or hooks",
        "Blocked: a push that is not one plain git push command",
    ):
        assert blocked in first_pass
    probes = _text("ob-h3-FS-refusal-texts-probes.txt")
    assert "at level full --submit." in probes
    assert "Blocked: a gh api call that is not one plain read command" in probes
    notes = _text("ob-h3-FS-notes.md")
    assert "https://github.com/IronbellyOrg/IronClaude/pull/845" in notes
    assert "never merged" in notes and "No launch level may merge" in notes
    assert "SuperClaude-Org" not in notes


# -- OB-CTX -----------------------------------------------------------------------

_CTX_A = "3b70b88c-4387-4c53-9b3e-9dc279e86cb0"
_CTX_C = "cceb3747-5849-4b20-b35a-dfa933a29f96"


def _checker():
    spec = importlib.util.spec_from_file_location("ob_ctx_check", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ob_ctx_runs_a_b_and_c_pass_the_checker_with_no_violations():
    """Reads evidence/ob-ctx-run-{a,b,c}-probe.jsonl, ob-ctx-human-concurrent.txt,
    ob-ctx-live-842-governed.jsonl and ob-ctx-existing-coverage.tsv through
    fixtures/launch_level/ob_ctx_check.py (obs-ctx-plan section 7, P1 to P8): zero
    violations on each run, resume keeps run A's session id, the fork has its own, the
    human shell reads ordinary beside a governed job child, and LIM-1 and LIM-2 read
    ordinary."""
    oc = _checker()
    human = _text("ob-ctx-human-concurrent.txt")
    run_a = oc.check(
        oc.jsonl_records(_text("ob-ctx-run-a-probe.jsonl")), [_CTX_A], human_text=human
    )
    run_b = oc.check(oc.jsonl_records(_text("ob-ctx-run-b-probe.jsonl")), [_CTX_A])
    run_c = oc.check(oc.jsonl_records(_text("ob-ctx-run-c-probe.jsonl")), [_CTX_C])
    for result in (run_a, run_b, run_c):
        assert result["violations"] == [] and result["scoped"] > 0
    assert run_a["governed"] == run_b["governed"] == {_CTX_A}
    assert run_c["governed"] == {_CTX_C} != run_a["governed"]
    combined = _text("ob-ctx-run-a-probe.jsonl") + _text(
        "ob-ctx-live-842-governed.jsonl"
    )
    complete = oc.check(
        oc.jsonl_records(combined),
        [_CTX_A, _FS_SID, _W_SID],
        human_text=human,
        complete=True,
    )
    assert complete["violations"] == [] and complete["scoped"] == 506  # P8: rows R1-R7
    assert "setsid child sleep 9 pid" in human and "monitor child sleep 4 pid" in human
    for label in ("setsid child", "monitor child", "human shell"):
        line = next(x for x in human.splitlines() if x.startswith(label))
        assert json.loads(line[line.index("{") :]) == {"status": "ordinary"}
    existing = re.findall(
        r"OB-CTX-CHECK violations=(\d+)", _text("ob-ctx-existing-coverage.tsv")
    )
    assert existing == ["0", "0", "0"]  # the real claims 827, 829 and 841
    notes = _text("ob-ctx-notes.md")
    assert "Run A alone: `OB-CTX-CHECK violations=0`" in notes
    assert "/clear" in notes and "Still not observed" in notes


@pytest.mark.parametrize("item", _PENDING)
def test_pending_live_observation(item):
    pytest.skip(f"{item}: needs a real governed session and has not been run")
