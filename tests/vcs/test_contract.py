"""The helper envelope, checked across all seven verbs (FR-010 to FR-013, NFR-006 to NFR-009;
design sections 4.1 and 4.3).

Every verb is run through its command line on a real temporary repository that holds a real
ledger, sidecar and prepared attempt. The checks here are the ones every verb shares: one JSON
line, ``vcs_contract``, sorted keys, at most 64 KiB, lists cut at 200 with ``truncated``, the
same bytes for the same inputs, the exit codes 0, 64 and 69, the verb list of ``--help``, and
the result fields the design lists for each verb (one table, ``FIELDS``). What each verb
decides has its own test module.
"""

from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
import sys

import pytest

from .conftest import SCRIPTS
from .test_crash_points import PKG, Exec
from .test_stage_plan import PIN, Scene

VERBS = (
    "check-message",
    "preflight",
    "reconcile",
    "resolve-check",
    "stage-plan",
    "submodules",
    "verify",
)
STATUSES = {
    "preflight": {"ok", "refused"},
    "stage-plan": {"ok", "nothing", "refused"},
    "check-message": {"ok", "refused"},
    "verify": {
        "committed",
        "pending",
        "uncertain",
        "interrupted",
        "refused",
        "blocked-by-host",
        "hook-failed",
        "hook-rewrite",
        "hook-rewrite-evidence",
        "hook-rewrite-committed",
        "hook-rewrite-pinned",
        "commit-error",
    },
    "reconcile": {"ok", "refused"},
    "resolve-check": {"ok", "refused"},
    "submodules": {"ok", "refused"},
}
ENVELOPE = ("vcs_contract", "verb", "status", "reason", "truncated")
# The result fields of design section 4.3, beyond the envelope, one row per verb.
FIELDS = {
    "preflight": (
        "top branch symbolic_ref detached protected operation_in_progress index_lock "
        "hooks_path submodule_recurse push_recurse_submodules git_version min_git_ok "
        "default_branch_known"
    ).split(),
    "stage-plan": (
        "tasks commit_paths skipped add_argv commit_argv message_path pathspec_file "
        "s_count truncated"
    ).split(),
    "check-message": ["header_len"],
    "verify": "class sha outside_changed outside_paths changed_paths".split(),
    "reconcile": "boundaries runs segments".split(),
    "resolve-check": ("key state choices basis differs head parent quiescent").split(),
    "submodules": "superproject config rows".split(),
}
LISTS = {
    "tasks", "commit_paths", "skipped", "add_argv", "commit_argv", "outside_paths",
    "changed_paths", "boundaries", "runs", "segments", "choices", "rows",
}  # fmt: skip
BOUNDARY_FIELDS = "key members state action parent head reason".split()


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


@pytest.fixture(autouse=True)
def no_live_git(scripts_dir, monkeypatch):
    plan = importlib.import_module("vcs_plan")
    monkeypatch.setattr(plan, "_live_git_processes", lambda top: [])


@pytest.fixture
def make(repo, vcs):
    def build(managed=False):
        for name in ("a", "b", "c"):
            repo.write(f"src/{name}.py", "old\n")
        repo.commit("base")
        if managed:
            repo.write(f"{PKG}/plan1.md", "the plan\n")
            repo.write(f"{PKG}/source.md", "the source\n")
        return Exec(Scene(repo, vcs, managed), repo, vcs, managed)

    return build


def run_cli(*args, cwd=None):
    env = {**os.environ, "COLUMNS": "200"}
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "vcs.py"), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )


# --- one real command line for every verb (and the refusal and candidate variants) -----------
@pytest.fixture
def commands(make, repo, tmp_path):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="prepared")
    ex.new_run()
    ex.s.write()
    work = str(repo.work)
    parent = repo.git("rev-parse", "HEAD").strip()
    stem = f"{PIN}/plan1"
    good = tmp_path / "good.txt"
    good.write_text("feat: add the thing\n", encoding="utf-8")
    bad = tmp_path / "bad.txt"
    bad.write_text("Add the thing\n", encoding="utf-8")
    ledger = ["--ledger", str(ex.s.ledger_path)]
    side = ["--sidecar", str(ex.s.side_path)]
    run_dir = ["--run-dir", str(ex.s.run_dir)]
    return {
        "preflight": ["preflight", "--cwd", work],
        "stage-plan (path mode)": ["stage-plan", "--cwd", work, "--path", "src/a.py"],
        "stage-plan (ledger mode)": ["stage-plan", "--cwd", work, *ledger, *run_dir],
        "stage-plan (candidate)": [
            "stage-plan",
            "--cwd",
            work,
            *ledger,
            *run_dir,
            "--candidate",
        ],  # fmt: skip
        "check-message (ok)": ["check-message", "--file", str(good)],
        "check-message (refused)": ["check-message", "--file", str(bad)],
        "verify": [
            "verify",
            "--cwd",
            work,
            "--key",
            key,
            "--attempt",
            "1",
            "--parent",
            parent,
            "--candidate-ref",
            f"{stem}/boundary/{key}-a1",
            "--worktree-ref",
            f"{stem}/boundary-wt/{key}-a1",
            "--exit",
            "0",
            *ledger,
            *side,
        ],  # fmt: skip
        "reconcile": [
            "reconcile",
            "--cwd",
            work,
            *ledger,
            *side,
            *run_dir,
            "--flag",
            "on",
        ],  # fmt: skip
        "resolve-check": [
            "resolve-check",
            "--cwd",
            work,
            "--key",
            key[:12],
            *ledger,
            *side,
            *run_dir,
        ],  # fmt: skip
        "submodules": ["submodules", "--cwd", work],
    }


def result_of(name, argv, cwd):
    done = run_cli(*argv, cwd=cwd)
    assert done.returncode == 0, (name, done.stderr)
    assert done.stdout.count("\n") == 1 and done.stdout.endswith("\n"), name
    return done.stdout, json.loads(done.stdout)


# =============================================================================================
# The envelope
# =============================================================================================
def test_every_verb_prints_one_sorted_json_line_with_the_envelope(commands, repo):
    seen = set()
    for name, argv in commands.items():
        text, data = result_of(name, argv, repo.work)
        verb = argv[0]
        seen.add(verb)
        assert data["verb"] == verb and data["vcs_contract"] == "1", name
        assert all(field in data for field in ENVELOPE), name
        assert list(data) == sorted(data), name
        assert isinstance(data["truncated"], bool), name
        assert data["status"] in STATUSES[verb], (name, data["status"])
        assert len(text.encode("ascii")) <= 64 * 1024, name
    assert seen == set(VERBS)


def test_two_runs_on_the_same_inputs_give_the_same_bytes(commands, repo):
    for name, argv in commands.items():
        first, _ = result_of(name, argv, repo.work)
        second, _ = result_of(name, argv, repo.work)
        assert first == second, name


def test_every_verb_carries_the_fields_the_design_lists(commands, repo):
    for name, argv in commands.items():
        _, data = result_of(name, argv, repo.work)
        for field in FIELDS[argv[0]]:
            assert field in data, (name, field)
            if field in LISTS:
                assert isinstance(data[field], list), (name, field)


def test_check_message_refusals_carry_the_header_length_and_the_rule(commands, repo):
    _, data = result_of(
        "check-message (refused)", commands["check-message (refused)"], repo.work
    )
    assert data["status"] == "refused"
    assert data["rule"] == data["reason"] == "header-format"
    assert data["header_len"] == len("Add the thing")


def test_reconcile_carries_its_runs_segments_and_boundary_rows(commands, repo):
    _, data = result_of("reconcile", commands["reconcile"], repo.work)
    assert data["runs"] and data["segments"] and data["boundaries"]
    for row in data["boundaries"]:
        assert all(field in row for field in BOUNDARY_FIELDS)


def test_stage_plan_candidate_adds_the_candidate_tree(commands, repo):
    _, data = result_of(
        "stage-plan (candidate)", commands["stage-plan (candidate)"], repo.work
    )
    assert data["status"] == "ok" and re.fullmatch(
        r"[0-9a-f]{40}", data["candidate_tree"]
    )


def test_preflight_and_submodules_carry_their_nested_facts(commands, repo):
    _, pre = result_of("preflight", commands["preflight"], repo.work)
    assert set(pre["protected"]) == {"value", "reason"}
    _, sub = result_of("submodules", commands["submodules"], repo.work)
    assert set(sub["superproject"]) == {"branch", "head"}
    assert set(sub["config"]) == {"submodule_recurse", "push_recurse_submodules"}


# =============================================================================================
# The caps (NFR-006, NFR-007)
# =============================================================================================
def test_lists_stop_at_200_and_the_flag_says_so_while_s_stays_whole(repo):
    for n in range(250):
        repo.write(f"bulk/n{n:03d}.txt", "x\n")
    paths = [f"bulk/n{n:03d}.txt" for n in range(250)]
    done = run_cli("stage-plan", "--cwd", str(repo.work), "--path", *paths)
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["status"], data["truncated"], data["s_count"]) == ("ok", True, 250)
    assert data["commit_paths"] == paths[:200]
    # the cap is for display: the pathspec file the agent writes holds every path
    assert data["pathspec_file"]["content"].count("\0") == 250


def test_an_object_above_64_kib_is_replaced_by_a_short_refusal_and_still_exits_zero(
    repo,
):
    folder = os.path.join("a" * 120, "b" * 120)
    paths = [os.path.join(folder, f"f{n:03d}" + "x" * 100) for n in range(250)]
    for rel in paths:
        repo.write(rel, "x\n")
    done = run_cli("stage-plan", "--cwd", str(repo.work), "--path", *paths)
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["status"], data["reason"]) == ("refused", "output-too-large")
    assert (data["verb"], data["vcs_contract"]) == ("stage-plan", "1")
    assert len(done.stdout) < 1000


# =============================================================================================
# Exit codes 0, 64 and 69, and the verb list
# =============================================================================================
def test_a_refusal_is_a_result_and_exits_zero(commands, repo):
    done = run_cli(*commands["check-message (refused)"], cwd=repo.work)
    assert done.returncode == 0
    assert json.loads(done.stdout)["status"] == "refused"
    argv = list(commands["resolve-check"])
    argv[argv.index("--key") + 1] = "f" * 12
    done = run_cli(*argv, cwd=repo.work)
    assert done.returncode == 0
    assert json.loads(done.stdout)["reason"] == "unknown-boundary"


@pytest.mark.parametrize("verb", VERBS)
def test_an_unknown_option_is_a_usage_error_exit_64_with_nothing_on_stdout(verb):
    done = run_cli(verb, "--no-such-option")
    assert done.returncode == 64
    assert done.stdout == "" and done.stderr.strip()


@pytest.mark.parametrize("args", [[], ["no-such-verb"]])
def test_a_missing_or_unknown_verb_is_a_usage_error(args):
    done = run_cli(*args)
    assert done.returncode == 64 and done.stdout == ""


def test_a_failed_lookup_exits_69_with_nothing_on_stdout_for_every_verb(
    commands, tmp_path
):
    gone = str(tmp_path / "absent")
    for name, argv in commands.items():
        verb = argv[0]
        if verb == "check-message":
            argv = ["check-message", "--file", str(tmp_path / "absent.txt")]
        else:
            argv = list(argv)
            argv[argv.index("--cwd") + 1] = gone
        done = run_cli(*argv)
        assert done.returncode == 69, (name, done.stdout, done.stderr)
        assert done.stdout == "" and "lookup failed" in done.stderr, name


def test_help_lists_exactly_the_seven_verbs():
    done = run_cli("--help")
    assert done.returncode == 0
    # a verb name longer than the help column keeps its description on the next line
    listed = re.findall(r"^ {4}([a-z]+(?:-[a-z]+)*)(?: |$)", done.stdout, re.MULTILINE)
    assert sorted(listed) == sorted(VERBS)


def test_the_verb_table_of_the_entry_point_is_the_same_seven(vcs):
    assert sorted(vcs.VERBS) == sorted(VERBS)
