adeb4a04f7b6501deb77d04d2550897a2a18771a
Review one task for spec compliance.

Task brief: ## Task 7: Create the GitHub I/O script `set-draft-state.sh`

Depends on: Task 1

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` following ./source.md section 4.4 and modelled on `scripts/retrigger-review.sh` (same `die`, `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing, executable bit). Modes `--read` and `--to draft|ready` with the exact calls, the one-line JSON shapes and the exit codes 0, 1, 2, 127 of section 4.4; every `gh` call carries `--repo "$REPO"` or a `repos/${REPO}/...` path; the timeline count uses `gh api --paginate` with a `jq` filter on `convert_to_draft` and `ready_for_review` piped to `wc -l`; `--to` re-reads state first (non-`OPEN` gives `error:"not_open"`), is idempotent (`changed:false` when already in the target state) and verifies after the mutation (`verify_failed`). Create `tests/pr_submit/test_set_draft_state.py` using a fake `gh` on `PATH` that logs its arguments (the fake-executable approach of `tests/pr_submit/test_conflict_scripts.py`), exposing the fake as a helper or fixture that other test files may import. Add the script to `_RESOLUTION_SCRIPTS` in `tests/pr_submit/test_static_grep.py` only after reading the purpose of that list (Task 1 O2), and to any script list that Task 1 O2 shows is required for a new script. As the last step, once the script text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the script that matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- T7.AC1: Fake-`gh` tests assert: `--read` prints one JSON line with `ok`, `state`, `isDraft`, `headRefOid`, `autoMergeRequest`, `transitions`, `complete`; a failing timeline call prints `transitions: null` and `complete: false`; `--to draft` on a draft PR makes no `pr ready` call and prints `changed:false`; `--to ready` on a merged PR prints `ok:false` with `error:"not_open"`; a mismatch after the mutation prints `ok:false` with `error:"verify_failed"`.
- T7.AC2: Exit codes are asserted: 0 on success, 1 on a failing `gh` (JSON still printed with `ok:false`), 2 for a missing or non-numeric `--pr` and for an unknown argument, 127 with `gh` absent from `PATH` and a separate case with `jq` absent from `PATH`.
- T7.AC3: The recorded fake-`gh` argument log shows `--repo` or a `repos/` path on every call, and `test_set_draft_state.py` also statically scans the script and asserts every `gh` line carries `--repo` or a `repos/` path (the existing `test_t105_runtime_repo_pin` covers only the poll script and is not the proof); the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests.
- T7.AC4: `uv run pytest tests/pr_submit/test_set_draft_state.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/skills/test_worker_contract.py -q` passes (the classification and stale-entry tests included) and `make verify-sync` exits 0.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: adeb4a04f7b6501deb77d04d2550897a2a18771a
Diff against the start snapshot: NEW FILE src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh (full contents, 6110 bytes):
#!/usr/bin/env bash
#
# set-draft-state.sh — read or set the draft state of a pull request for the
# sc:pr-submit merge guard (issue #375).
#
# Purpose : The merge guard turns a PR into a draft while a fix cycle runs and marks
#           it ready again once the fix push is confirmed. All GitHub I/O of that
#           guard is isolated here; the decisions live in the pure module
#           superclaude.pr_submit.merge_guard (NFR-6). Every call is idempotent, so
#           a retry or a resume re-issue is safe.
# Usage   : set-draft-state.sh --pr <N> [--repo <owner/repo>] --read
#           set-draft-state.sh --pr <N> [--repo <owner/repo>] --to draft|ready
# Output  : exactly one JSON line on stdout.
#           --read : {"ok":true,"state":"OPEN","isDraft":false,"headRefOid":"<sha>",
#                     "autoMergeRequest":false,"transitions":3,"complete":true,
#                     "error":null}. When only the timeline call fails the line has
#                     "transitions":null and "complete":false.
#           --to   : {"ok":true,"state":"OPEN","isDraft":true,"headRefOid":"<sha>",
#                     "changed":true,"error":null}. The state is read first: a PR that
#                     is not OPEN gives "ok":false and "error":"not_open"; a PR already
#                     in the target state gives "changed":false and no mutation; after
#                     a mutation the state is read again and a mismatch gives
#                     "error":"verify_failed".
# Exit    : 0 on success; 1 when a CLI call fails or a check fails (the JSON line is
#           still printed, with "ok":false); 2 on usage error (missing or non-numeric
#           --pr, missing mode, unknown argument); 127 when the CLI or jq is missing
#           (an environment failure, not misuse).
# Spec    : the merge-guard protocol reference (refs/merge-guard.md). The repo is the
#           RESOLVED origin owner/repo, never the upstream parent: every call carries
#           --repo "$REPO" or a repos/${REPO}/... path.

set -euo pipefail

die() { printf 'set-draft-state: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
REPO=""
MODE=""
TO=""
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) [ $# -ge 2 ] || die "missing value for --pr <N>" 2; PR="$2"; shift 2 ;;
        --repo) [ $# -ge 2 ] || die "missing value for --repo <owner/repo>" 2; REPO="$2"; shift 2 ;;
        --read) MODE="read"; shift ;;
        --to)
            [ $# -ge 2 ] || die "missing value for --to draft|ready" 2
            case "$2" in draft|ready) ;; *) die "invalid --to value (must be draft or ready): $2" 2 ;; esac
            MODE="to"; TO="$2"; shift 2 ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done

[ -n "$PR" ] || die "missing required --pr <N>" 2
case "$PR" in ''|*[!0-9]*) die "invalid --pr value (must be a positive integer): $PR" 2 ;; esac
[ -n "$MODE" ] || die "missing mode (--read or --to draft|ready)" 2
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 127
command -v jq >/dev/null 2>&1 || die "jq not found on PATH" 127

# Resolve the target repo (owner/repo): the origin remote first, then the CLI default.
REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
[ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2

VIEW='{"state":null,"isDraft":null,"headRefOid":null,"autoMergeRequest":null}'

# Read the PR into VIEW; return 1 when the call fails or the answer has no state.
fetch_view() {
    local answer
    answer="$(gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest 2>/dev/null)" || return 1
    printf '%s' "$answer" | jq -e 'has("state") and has("isDraft")' >/dev/null 2>&1 || return 1
    VIEW="$answer"
}

# One JSON line for --read. $1 = ok (true|false), $2 = transitions (number|null),
# $3 = complete (true|false), $4 = error text (empty for none).
emit_read() {
    jq -c --argjson ok "$1" --argjson transitions "$2" --argjson complete "$3" --arg error "$4" \
        '{ok:$ok,state:.state,isDraft:.isDraft,headRefOid:.headRefOid,autoMergeRequest:(.autoMergeRequest != null),transitions:$transitions,complete:$complete,error:(if $error == "" then null else $error end)}' \
        <<<"$VIEW"
}

# One JSON line for --to. $1 = ok (true|false), $2 = changed (true|false), $3 = error text.
emit_to() {
    jq -c --argjson ok "$1" --argjson changed "$2" --arg error "$3" \
        '{ok:$ok,state:.state,isDraft:.isDraft,headRefOid:.headRefOid,changed:$changed,error:(if $error == "" then null else $error end)}' \
        <<<"$VIEW"
}

if [ "$MODE" = "read" ]; then
    fetch_view || { emit_read false null false read_failed; exit 1; }
    transitions="null"
    complete="false"
    # Count the draft/ready transitions on the PR timeline (all pages).
    if count="$(gh api --paginate "repos/${REPO}/issues/${PR}/timeline" --jq '.[] | select(.event=="convert_to_draft" or .event=="ready_for_review") | .event' 2>/dev/null | wc -l | tr -d ' ')"; then
        transitions="$count"
        complete="true"
    fi
    emit_read true "$transitions" "$complete" ""
    exit 0
fi

# --to draft|ready: read first, change only when needed, verify after.
if [ "$TO" = "draft" ]; then want="true"; else want="false"; fi
fetch_view || { emit_to false false read_failed; exit 1; }
if [ "$(jq -r '.state' <<<"$VIEW")" != "OPEN" ]; then
    emit_to false false not_open
    exit 1
fi
if [ "$(jq -r '.isDraft' <<<"$VIEW")" = "$want" ]; then
    emit_to true false ""
    exit 0
fi
if [ "$TO" = "draft" ]; then
    gh pr ready "$PR" --repo "$REPO" --undo >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }
else
    gh pr ready "$PR" --repo "$REPO" >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }
fi
fetch_view || { emit_to false false verify_failed; exit 1; }
if [ "$(jq -r '.isDraft' <<<"$VIEW")" != "$want" ]; then
    emit_to false false verify_failed
    exit 1
fi
emit_to true true ""
exit 0

NEW FILE tests/pr_submit/test_set_draft_state.py (full contents, 14176 bytes):
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

diff --git a/tests/pr_submit/test_static_grep.py b/tests/pr_submit/test_static_grep.py
index fbca9a29..d99412ab 100644
--- a/tests/pr_submit/test_static_grep.py
+++ b/tests/pr_submit/test_static_grep.py
@@ -483,6 +483,7 @@ _RESOLUTION_SCRIPTS = (
     SKILL_DIR / "scripts" / "poll-ci-checks.sh",
     SKILL_DIR / "scripts" / "retrigger-review.sh",
     SKILL_DIR / "scripts" / "reply-resolve-thread.sh",
+    SKILL_DIR / "scripts" / "set-draft-state.sh",
 )
 
 # Every remote-URL shape `git remote get-url origin` can emit, → the expected owner/repo.

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index bb01c70c..17ea43d0 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -1882,6 +1882,38 @@ WRITE_VERB_CLASSIFICATION = {
         "never-worker",
         "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
     ),
+    (
+        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
+        "gh pr",
+        'answer="$(gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest 2>/dev/null)" || return 1',
+    ): (
+        "never-worker",
+        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
+    ),
+    (
+        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
+        "gh api",
+        'if count="$(gh api --paginate "repos/${REPO}/issues/${PR}/timeline" --jq \'.[] | select(.event=="convert_to_draft" or .event=="ready_for_review") | .event\' 2>/dev/null | wc -l | tr -d \' \')"; then',
+    ): (
+        "never-worker",
+        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
+    ),
+    (
+        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
+        "gh pr",
+        'gh pr ready "$PR" --repo "$REPO" --undo >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }',
+    ): (
+        "never-worker",
+        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
+    ),
+    (
+        "src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh",
+        "gh pr",
+        'gh pr ready "$PR" --repo "$REPO" >/dev/null 2>&1 || { emit_to false false mutation_failed; exit 1; }',
+    ): (
+        "never-worker",
+        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
+    ),
     (
         "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
         "git worktree add",

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
