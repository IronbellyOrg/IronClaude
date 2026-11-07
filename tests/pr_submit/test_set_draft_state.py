"""Tests for ``scripts/set-draft-state.sh`` (issue #375): read and set the PR draft state.

No test calls GitHub. A fake ``gh`` executable on ``PATH`` answers ``pr view``,
``pr ready``, the timeline call and ``repo view`` from files, and logs every call.
``FakeGh`` and the ``fake_gh`` fixture are importable by other test files (the
scenario tests use them).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

from tests.pr_submit.test_static_grep import _GH_CMD, _command_lines, _repo_scoped

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "skills"
    / "sc-pr-submit-protocol"
    / "scripts"
    / "set-draft-state.sh"
)

HEAD = "a" * 40
REPO = "acme/widgets"

FAKE_GH = r"""#!/usr/bin/env bash
dir="${FAKE_GH_DIR:?}"
printf '%s\n' "$*" >> "$dir/calls.log"
case "$1 $2" in
  "pr view")
    [ -e "$dir/fail_view" ] && exit 1
    cat "$dir/view.json" ;;
  "pr ready")
    [ -e "$dir/fail_ready" ] && exit 1
    if [ ! -e "$dir/no_effect" ]; then
      if [ "${*: -1}" = "--undo" ]; then draft=true; else draft=false; fi
      jq --argjson d "$draft" '.isDraft = $d' "$dir/view.json" > "$dir/view.tmp" \
        && mv "$dir/view.tmp" "$dir/view.json"
    fi ;;
  "api --paginate")
    [ -e "$dir/fail_timeline" ] && exit 1
    n="$(cat "$dir/timeline_count" 2>/dev/null || echo 0)"
    i=0
    while [ "$i" -lt "$n" ]; do echo convert_to_draft; i=$((i + 1)); done ;;
  "repo view") echo upstream/parent ;;
  *) echo "unexpected gh call: $*" >&2; exit 1 ;;
esac
"""

_NEEDED_TOOLS = ("bash", "env", "jq", "wc", "tr", "sed", "git", "cat", "mv", "dirname")


@dataclass
class Run:
    returncode: int
    stdout: str
    stderr: str

    @property
    def json(self) -> dict:
        lines = self.stdout.splitlines()
        assert len(lines) == 1, self.stdout
        return json.loads(lines[0])


class FakeGh:
    """A fake ``gh`` on ``PATH`` whose answers live in files under ``dir``."""

    def __init__(self, root: Path) -> None:
        self.dir = root / "fake-gh"
        self.bin = root / "fake-bin"
        self.dir.mkdir()
        self.bin.mkdir()
        gh = self.bin / "gh"
        gh.write_text(FAKE_GH, encoding="utf-8")
        gh.chmod(0o755)
        self.configure()

    def configure(
        self,
        *,
        state: str = "OPEN",
        is_draft: bool = False,
        head: str = HEAD,
        auto_merge: bool = False,
        transitions: int = 0,
    ) -> None:
        view = {
            "state": state,
            "isDraft": is_draft,
            "headRefOid": head,
            "autoMergeRequest": {"enabledBy": "x"} if auto_merge else None,
        }
        (self.dir / "view.json").write_text(json.dumps(view), encoding="utf-8")
        (self.dir / "timeline_count").write_text(str(transitions), encoding="utf-8")

    def flag(self, name: str, on: bool = True) -> None:
        path = self.dir / name
        if on:
            path.write_text("", encoding="utf-8")
        elif path.exists():
            path.unlink()

    def calls(self) -> list[str]:
        log = self.dir / "calls.log"
        return log.read_text(encoding="utf-8").splitlines() if log.exists() else []

    def is_draft(self) -> bool:
        return json.loads((self.dir / "view.json").read_text(encoding="utf-8"))[
            "isDraft"
        ]

    def run(self, *args: str, path: str | None = None) -> Run:
        env = {
            **os.environ,
            "PATH": path or f"{self.bin}{os.pathsep}{os.environ['PATH']}",
            "FAKE_GH_DIR": str(self.dir),
        }
        result = subprocess.run(
            [str(SCRIPT), *args],
            env=env,
            text=True,
            capture_output=True,
            timeout=30,
        )
        return Run(result.returncode, result.stdout, result.stderr)

    def restricted_path(self, root: Path, *, with_gh: bool, with_jq: bool) -> str:
        """A PATH holding only the tools the script needs, so one can be left out."""
        only = (
            root
            / ("path-gh" if with_gh else "path-nogh")
            / ("jq" if with_jq else "nojq")
        )
        only.mkdir(parents=True)
        for tool in _NEEDED_TOOLS:
            if tool == "jq" and not with_jq:
                continue
            found = shutil.which(tool)
            if found is None:
                pytest.skip(f"{tool} is not on PATH")
            (only / tool).symlink_to(found)
        if with_gh:
            (only / "gh").symlink_to(self.bin / "gh")
        return str(only)


@pytest.fixture
def fake_gh(tmp_path):
    for tool in ("bash", "jq"):
        if shutil.which(tool) is None:
            pytest.skip(f"{tool} is not on PATH")
    return FakeGh(tmp_path)


READ_FIELDS = {
    "ok",
    "state",
    "isDraft",
    "headRefOid",
    "autoMergeRequest",
    "transitions",
    "complete",
    "error",
}
TO_FIELDS = {"ok", "state", "isDraft", "headRefOid", "changed", "error"}


# --- --read ------------------------------------------------------------------


def test_read_prints_one_json_line_with_every_field(fake_gh):
    fake_gh.configure(is_draft=False, transitions=3)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--read")
    assert run.returncode == 0, run.stderr
    assert set(run.json) == READ_FIELDS
    assert run.json == {
        "ok": True,
        "state": "OPEN",
        "isDraft": False,
        "headRefOid": HEAD,
        "autoMergeRequest": False,
        "transitions": 3,
        "complete": True,
        "error": None,
    }


def test_read_reports_an_armed_auto_merge(fake_gh):
    fake_gh.configure(auto_merge=True)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--read")
    assert run.json["autoMergeRequest"] is True


def test_read_with_a_failing_timeline_call_is_incomplete(fake_gh):
    fake_gh.configure(transitions=4)
    fake_gh.flag("fail_timeline")
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--read")
    assert run.returncode == 0
    assert run.json["ok"] is True
    assert run.json["transitions"] is None
    assert run.json["complete"] is False


def test_read_with_a_failing_view_call_prints_ok_false_and_exits_1(fake_gh):
    fake_gh.flag("fail_view")
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--read")
    assert run.returncode == 1
    assert set(run.json) == READ_FIELDS
    assert run.json["ok"] is False
    assert run.json["error"] == "read_failed"
    assert run.json["transitions"] is None
    assert run.json["complete"] is False


# --- --to --------------------------------------------------------------------


def test_to_draft_on_a_draft_pr_makes_no_ready_call(fake_gh):
    fake_gh.configure(is_draft=True)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "draft")
    assert run.returncode == 0, run.stderr
    assert set(run.json) == TO_FIELDS
    assert run.json["ok"] is True
    assert run.json["changed"] is False
    assert run.json["isDraft"] is True
    assert not any(call.startswith("pr ready") for call in fake_gh.calls())


def test_to_ready_on_a_ready_pr_makes_no_ready_call(fake_gh):
    fake_gh.configure(is_draft=False)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "ready")
    assert run.json["changed"] is False
    assert not any(call.startswith("pr ready") for call in fake_gh.calls())


def test_to_draft_changes_the_pr_with_undo_and_verifies(fake_gh):
    fake_gh.configure(is_draft=False)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "draft")
    assert run.returncode == 0, run.stderr
    assert run.json["ok"] is True
    assert run.json["changed"] is True
    assert run.json["isDraft"] is True
    assert run.json["error"] is None
    ready_calls = [c for c in fake_gh.calls() if c.startswith("pr ready")]
    assert len(ready_calls) == 1 and ready_calls[0].endswith("--undo")
    assert fake_gh.is_draft() is True


def test_to_ready_changes_the_pr_without_undo_and_verifies(fake_gh):
    fake_gh.configure(is_draft=True)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "ready")
    assert run.returncode == 0, run.stderr
    assert run.json["changed"] is True
    assert run.json["isDraft"] is False
    ready_calls = [c for c in fake_gh.calls() if c.startswith("pr ready")]
    assert len(ready_calls) == 1 and "--undo" not in ready_calls[0]


@pytest.mark.parametrize("state", ["MERGED", "CLOSED"])
@pytest.mark.parametrize("target", ["draft", "ready"])
def test_to_on_a_pr_that_is_not_open_is_not_open(fake_gh, state, target):
    fake_gh.configure(state=state, is_draft=(target == "ready"))
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", target)
    assert run.returncode == 1
    assert run.json["ok"] is False
    assert run.json["error"] == "not_open"
    assert run.json["state"] == state
    assert run.json["changed"] is False
    assert not any(call.startswith("pr ready") for call in fake_gh.calls())


def test_a_mismatch_after_the_mutation_is_verify_failed(fake_gh):
    fake_gh.configure(is_draft=False)
    fake_gh.flag("no_effect")
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "draft")
    assert run.returncode == 1
    assert run.json["ok"] is False
    assert run.json["error"] == "verify_failed"
    assert run.json["isDraft"] is False
    assert run.json["changed"] is False


def test_a_failing_ready_call_is_a_failed_mutation(fake_gh):
    fake_gh.configure(is_draft=False)
    fake_gh.flag("fail_ready")
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "draft")
    assert run.returncode == 1
    assert run.json["ok"] is False
    assert run.json["error"] == "mutation_failed"


def test_to_with_a_failing_first_read_prints_ok_false_and_exits_1(fake_gh):
    fake_gh.flag("fail_view")
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "ready")
    assert run.returncode == 1
    assert set(run.json) == TO_FIELDS
    assert run.json["ok"] is False
    assert run.json["error"] == "read_failed"
    assert not any(call.startswith("pr ready") for call in fake_gh.calls())


def test_a_retry_after_a_landed_mutation_is_idempotent(fake_gh):
    """A second `--to draft` finds the PR already draft: `changed: false`, no call."""
    fake_gh.configure(is_draft=False)
    assert fake_gh.run("--pr", "7", "--repo", REPO, "--to", "draft").json["changed"]
    again = fake_gh.run("--pr", "7", "--repo", REPO, "--to", "draft")
    assert again.json["ok"] is True and again.json["changed"] is False
    assert len([c for c in fake_gh.calls() if c.startswith("pr ready")]) == 1


# --- exit codes --------------------------------------------------------------


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["--read"],
        ["--pr", "x", "--read"],
        ["--pr", "-3", "--read"],
        ["--pr", "", "--read"],
        ["--pr"],
        ["--pr", "7", "--repo", REPO],
        ["--pr", "7", "--repo", REPO, "--read", "--bogus"],
        ["--pr", "7", "--repo", REPO, "--to", "label"],
        ["--pr", "7", "--repo", REPO, "--to"],
        ["--bogus"],
    ],
)
def test_usage_errors_exit_2_and_print_no_json(fake_gh, args):
    run = fake_gh.run(*args)
    assert run.returncode == 2, (args, run.stderr)
    assert run.stdout == ""
    assert run.stderr.startswith("set-draft-state:")
    assert fake_gh.calls() == []


def test_missing_gh_exits_127(fake_gh, tmp_path):
    path = fake_gh.restricted_path(tmp_path, with_gh=False, with_jq=True)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--read", path=path)
    assert run.returncode == 127
    assert "gh CLI not found" in run.stderr
    assert run.stdout == ""


def test_missing_jq_exits_127(fake_gh, tmp_path):
    path = fake_gh.restricted_path(tmp_path, with_gh=True, with_jq=False)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--read", path=path)
    assert run.returncode == 127
    assert "jq not found" in run.stderr
    assert run.stdout == ""
    assert fake_gh.calls() == []


def test_the_restricted_path_runs_the_script_when_both_tools_are_present(
    fake_gh, tmp_path
):
    path = fake_gh.restricted_path(tmp_path, with_gh=True, with_jq=True)
    run = fake_gh.run("--pr", "7", "--repo", REPO, "--read", path=path)
    assert run.returncode == 0, run.stderr
    assert run.json["ok"] is True


# --- repo scope --------------------------------------------------------------


def test_every_recorded_call_is_repo_scoped(fake_gh):
    fake_gh.configure(is_draft=False, transitions=2)
    fake_gh.run("--pr", "7", "--repo", REPO, "--read")
    fake_gh.run("--pr", "7", "--repo", REPO, "--to", "draft")
    fake_gh.run("--pr", "7", "--repo", REPO, "--to", "ready")
    calls = fake_gh.calls()
    assert calls, "the fake gh recorded no call"
    for call in calls:
        assert f"--repo {REPO}" in call or f"repos/{REPO}/" in call, call


def test_every_gh_line_of_the_script_is_repo_scoped():
    """The existing poll-script test covers only that script; this one is the proof
    for the new script: every gh command line carries --repo or a repos/ path."""
    pr_lines = []
    api_lines = []
    offenders = []
    for lineno, line in _command_lines(SCRIPT):
        if not _GH_CMD.search(line):
            continue
        if not _repo_scoped(line):
            offenders.append(f"{lineno}: {line.strip()}")
        if " pr " in line:
            pr_lines.append(line)
        if " api " in line:
            api_lines.append(line)
    assert not offenders, offenders
    assert pr_lines and api_lines


def test_the_script_is_executable_and_strict():
    text = SCRIPT.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env bash\n")
    assert "\nset -euo pipefail\n" in text
    assert os.access(SCRIPT, os.X_OK)


def test_the_script_names_no_forbidden_operation():
    """It reads and flips the draft flag only: no push, force, stash or config."""
    text = SCRIPT.read_text(encoding="utf-8")
    for pattern in (
        r"\bgit\s+(push|stash|config|commit|checkout|reset)\b",
        r"--force\b",
        r"--no-verify\b",
        r"src/superclaude",
    ):
        assert re.search(pattern, text) is None, pattern
