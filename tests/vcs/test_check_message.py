"""Tests for the ``check-message`` verb and the shared header rule (FR-039, FR-066, T-06).

The rule: ``<type>[(<scope>)][!]: <summary>``, at most 72 Unicode code points of the
decoded header (no normalization), a blank second line. With ``--implement`` the body
has one ``T<id>: <title>`` line per task and the trailer block carries
``Implement-Plan``, one ``Implement-Task`` per member, ``Implement-Boundary`` (64 hex)
and ``Implement-Ledger``. ``cut_header`` is the drafting side of the same count.
"""

from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import sys

import pytest

from .conftest import SCRIPTS, SHA64

ALLOWED_TYPES = (
    "feat", "fix", "refactor", "docs", "test", "build", "ci", "chore", "perf", "style",
)  # fmt: skip


@pytest.fixture
def plan(scripts_dir):
    return importlib.import_module("vcs_plan")


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


def header_of(length: int, fill: str = "a", prefix: str = "feat: ") -> str:
    return prefix + fill * (length - len(prefix))


def implement_message(
    header="feat: add the commit step",
    tasks=(("1", "compliant", "Add the step"), ("2", "compliant", "Wire the flag")),
    plan_slug="TASK-WF-x-20261001-063000",
    key=SHA64,
    ledger=".dev/tasks/to-do/x/progress.md",
    after="",
):
    body = "\n".join(f"T{tid}: {title}" for tid, _, title in tasks)
    trailers = [f"Implement-Plan: {plan_slug}"]
    trailers += [f"Implement-Task: T{tid} ({verdict})" for tid, verdict, _ in tasks]
    trailers += [f"Implement-Boundary: {key}", f"Implement-Ledger: {ledger}"]
    text = header + "\n\n" + body + "\n\n" + "\n".join(trailers) + "\n"
    return text + after


# --- the plain rule (no --implement) ------------------------------------------------------
@pytest.mark.parametrize("kind", ALLOWED_TYPES)
def test_every_allowed_type_is_accepted(plan, kind):
    out = plan.check_message(f"{kind}: do the thing\n")
    assert out["status"] == "ok", out
    assert out["header_len"] == len(f"{kind}: do the thing")


@pytest.mark.parametrize(
    "header",
    [
        "feat(scope): add it",
        "fix!: break it on purpose",
        "refactor(core)!: rename the thing",
    ],
)
def test_scope_and_bang_forms_are_accepted(plan, header):
    assert plan.check_message(header + "\n")["status"] == "ok"


def test_header_of_72_code_points_with_an_em_dash_is_accepted(plan):
    header = header_of(71) + "—"  # 71 chars + em dash = 72 code points, 74 bytes
    assert len(header) == 72 and len(header.encode()) > 72
    out = plan.check_message(header + "\n")
    assert out["status"] == "ok", out
    assert out["header_len"] == 72


def test_header_of_73_code_points_is_refused(plan):
    out = plan.check_message(header_of(72) + "—\n")
    assert out["status"] == "refused"
    assert out["reason"] == out["rule"] == "header-length"
    assert out["header_len"] == 73


def test_length_is_counted_without_normalization(plan):
    # "e" + combining acute is two code points; it must not be folded into one.
    header = header_of(71, prefix="feat: ") + "é"
    assert len(header) == 73
    assert plan.check_message(header + "\n")["rule"] == "header-length"


def test_missing_blank_second_line_is_refused(plan):
    out = plan.check_message("feat: add it\nbody right away\n")
    assert out["status"] == "refused"
    assert out["reason"] == out["rule"] == "blank-second-line"
    assert out["header_len"] == len("feat: add it")


def test_header_alone_and_header_with_a_blank_line_are_accepted(plan):
    assert plan.check_message("feat: add it")["status"] == "ok"
    assert plan.check_message("feat: add it\n\nwhy it matters\n")["status"] == "ok"


def test_unknown_type_is_refused(plan):
    out = plan.check_message("wip: add it\n")
    assert out["reason"] == out["rule"] == "unknown-type"
    assert out["header_len"] == len("wip: add it")


@pytest.mark.parametrize(
    "header", ["", "add it", "feat add it", "feat:add it", "feat: ", "Feat: add it"]
)
def test_malformed_headers_are_refused_with_header_format(plan, header):
    out = plan.check_message(header + "\n")
    assert out["status"] == "refused"
    assert out["reason"] == out["rule"] == "header-format"
    assert out["header_len"] == len(header)


def test_every_refusal_carries_header_len_rule_and_reason(plan):
    cases = [
        "",
        "wip: x\n",
        header_of(80) + "\n",
        "feat: x\nno blank\n",
        b"feat: \xff\xfe\n".decode("utf-8", "replace"),
    ]
    for text in cases:
        out = plan.check_message(text)
        if out["status"] == "refused":
            assert isinstance(out["header_len"], int)
            assert out["rule"] and out["reason"] == out["rule"]


# --- the drafting side ---------------------------------------------------------------------
def test_cut_header_keeps_a_short_header(plan):
    assert plan.cut_header("feat: short") == "feat: short"
    exact = header_of(72)
    assert plan.cut_header(exact) == exact


def test_cut_header_cuts_at_the_last_space_at_or_before_code_point_72(plan):
    words = "feat: " + " ".join(["word"] * 20)
    cut = plan.cut_header(words)
    assert len(cut) <= 72
    assert cut == words[: len(cut)]
    assert words[len(cut)] == " "
    assert not cut.endswith(" ")
    # the space may sit exactly at code point 72: the cut keeps the 71 before it
    spaced = header_of(71) + " tail"
    assert len(spaced) > 72
    assert plan.cut_header(spaced) == header_of(71)


def test_cut_header_without_a_space_in_the_summary_cuts_hard_at_72(plan):
    # the only space is the one after "feat:"; cutting there would leave "feat:"
    assert plan.cut_header(header_of(90)) == header_of(72)
    assert plan.check_message(plan.cut_header(header_of(90)) + "\n")["status"] == "ok"


def test_a_cut_header_always_passes_the_check(plan):
    long = "feat(core): " + " ".join(["longer"] * 30) + " — ends here"
    assert plan.check_message(plan.cut_header(long) + "\n")["status"] == "ok"


# --- --implement -----------------------------------------------------------------------------
def test_a_complete_implement_message_is_accepted(plan):
    out = plan.check_message(implement_message(), implement=True)
    assert out["status"] == "ok", out


def test_implement_accepts_attribution_trailers_after_the_helper_trailers(plan):
    text = implement_message(after="Co-Authored-By: Someone <s@example.invalid>\n")
    assert plan.check_message(text, implement=True)["status"] == "ok"


def test_the_plain_check_ignores_trailers(plan):
    assert plan.check_message("feat: add it\n\nT1: x\n")["status"] == "ok"


@pytest.mark.parametrize(
    "trailer, rule",
    [
        ("Implement-Plan:", "trailer-plan"),
        ("Implement-Task:", "trailer-task"),
        ("Implement-Boundary:", "trailer-boundary"),
        ("Implement-Ledger:", "trailer-ledger"),
    ],
)
def test_a_missing_trailer_is_refused_with_its_rule(plan, trailer, rule):
    lines = implement_message().splitlines(keepends=True)
    kept = [ln for ln in lines if not ln.startswith(trailer)]
    out = plan.check_message("".join(kept), implement=True)
    assert out["status"] == "refused"
    assert out["reason"] == out["rule"] == rule
    assert isinstance(out["header_len"], int)


def test_no_trailer_block_at_all_is_refused(plan):
    out = plan.check_message("feat: add it\n\nT1: Add the step\n", implement=True)
    assert out["reason"] == out["rule"] == "trailer-plan"


def test_a_12_hex_boundary_key_is_refused(plan):
    out = plan.check_message(implement_message(key=SHA64[:12]), implement=True)
    assert out["reason"] == out["rule"] == "trailer-boundary"
    assert out["header_len"] == len("feat: add the commit step")


def test_an_upper_case_boundary_key_is_refused(plan):
    out = plan.check_message(implement_message(key=SHA64.upper()), implement=True)
    assert out["rule"] == "trailer-boundary"


@pytest.mark.parametrize("ledger", ["/abs/progress.md", "../up/progress.md", ""])
def test_a_ledger_path_that_is_not_repo_relative_is_refused(plan, ledger):
    out = plan.check_message(implement_message(ledger=ledger), implement=True)
    assert out["rule"] == "trailer-ledger"


def test_trailers_out_of_order_are_refused(plan):
    text = implement_message()
    lines = text.splitlines()
    i, j = lines.index(f"Implement-Boundary: {SHA64}"), len(lines) - 1
    lines[i], lines[j] = lines[j], lines[i]
    out = plan.check_message("\n".join(lines) + "\n", implement=True)
    assert out["status"] == "refused"
    assert out["rule"].startswith("trailer-")


def test_a_bad_implement_task_line_is_refused(plan):
    text = implement_message().replace("(compliant)", "compliant", 1)
    assert plan.check_message(text, implement=True)["rule"] == "trailer-task"


def test_body_lines_must_match_the_task_trailers_in_order(plan):
    swapped = implement_message(
        tasks=(("1", "compliant", "A"), ("2", "compliant", "B"))
    ).replace("T1: A\nT2: B", "T2: B\nT1: A")
    assert plan.check_message(swapped, implement=True)["rule"] == "body-task-lines"
    missing = implement_message().replace("T2: Wire the flag\n", "")
    assert plan.check_message(missing, implement=True)["rule"] == "body-task-lines"
    prose = implement_message().replace("T2: Wire the flag", "wired the flag")
    assert plan.check_message(prose, implement=True)["rule"] == "body-task-lines"


def test_header_rules_run_before_trailer_rules_in_implement_mode(plan):
    out = plan.check_message(implement_message(header="wip: add it"), implement=True)
    assert out["rule"] == "unknown-type"


def test_the_helper_adds_no_attribution_trailer(plan):
    out = plan.check_message(implement_message(), implement=True)
    assert "Co-Authored-By" not in json.dumps(out)


# --- the verb ------------------------------------------------------------------------------------
def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "vcs.py"), *args],
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_verb_ok_prints_one_json_object(tmp_path):
    path = tmp_path / "msg.txt"
    path.write_text("feat: add it\n", encoding="utf-8")
    done = run_cli("check-message", "--file", str(path))
    assert done.returncode == 0, done.stderr
    assert done.stdout.count("\n") == 1
    data = json.loads(done.stdout)
    assert (data["vcs_contract"], data["verb"], data["status"]) == (
        "1",
        "check-message",
        "ok",
    )
    assert data["header_len"] == len("feat: add it")


def test_verb_refusal_is_exit_0_with_rule_and_header_len(tmp_path):
    path = tmp_path / "msg.txt"
    path.write_text("wip: add it\n", encoding="utf-8")
    done = run_cli("check-message", "--file", str(path))
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert data["status"] == "refused"
    assert data["reason"] == data["rule"] == "unknown-type"
    assert data["header_len"] == len("wip: add it")


def test_verb_implement_flag(tmp_path):
    path = tmp_path / "msg.txt"
    path.write_text(implement_message(), encoding="utf-8")
    assert (
        json.loads(run_cli("check-message", "--file", str(path)).stdout)["status"]
        == "ok"
    )
    done = run_cli("check-message", "--file", str(path), "--implement")
    assert json.loads(done.stdout)["status"] == "ok"
    path.write_text("feat: add it\n", encoding="utf-8")
    done = run_cli("check-message", "--file", str(path), "--implement")
    assert json.loads(done.stdout)["rule"] == "trailer-plan"


def test_verb_refuses_a_message_that_is_not_utf8(tmp_path):
    path = tmp_path / "msg.txt"
    path.write_bytes(b"feat: caf\xe9\n")
    data = json.loads(run_cli("check-message", "--file", str(path)).stdout)
    assert data["status"] == "refused"
    assert data["reason"] == data["rule"] == "encoding"
    assert isinstance(data["header_len"], int)


def test_verb_missing_file_exits_69(tmp_path):
    done = run_cli("check-message", "--file", str(tmp_path / "absent.txt"))
    assert done.returncode == 69
    assert done.stdout == ""
    assert "lookup failed" in done.stderr


def test_verb_without_file_is_a_usage_error():
    done = run_cli("check-message")
    assert done.returncode == 64
    assert done.stdout == ""


def test_verb_is_registered(vcs):
    assert "check-message" in vcs.VERBS


# --- the hook's own type list --------------------------------------------------------------
@pytest.mark.skipif(
    shutil.which("conventional-pre-commit") is None,
    reason="conventional-pre-commit is not installed",
)
@pytest.mark.parametrize("kind", ALLOWED_TYPES)
def test_pinned_hook_accepts_every_allowed_type(tmp_path, kind):
    """UNVERIFIED: that the default type list of conventional-pre-commit (pinned at
    ``rev: v3.0.0`` in ``.pre-commit-config.yaml``) holds all ten types is not yet
    confirmed; this test runs the installed hook with no ``types`` argument, so the
    hook's own default list decides. The call form (message file as the last
    argument) is also UNVERIFIED."""
    path = tmp_path / "msg.txt"
    path.write_text(f"{kind}: do the thing\n", encoding="utf-8")
    done = subprocess.run(
        ["conventional-pre-commit", str(path)], capture_output=True, text=True
    )
    assert done.returncode == 0, done.stdout + done.stderr
