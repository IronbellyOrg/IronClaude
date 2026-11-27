"""T-04: the ``verify`` verb and the hook-outcome classes of FR-036 (FR-064, FR-108, FR-113,
FR-130; design sections 5.5 and 6.1).

Each case builds a real repository, a real implement ledger and sidecar, and runs steps 1 to
6 of the commit procedure the way the executor does: plan, prepared line, candidate pin,
add, worktree snapshot pin. Step 7 is a real ``git commit --only`` under the hook emulator
of ``conftest.py`` (it replays the framework's stash-and-restore sequence), and ``verify``
is then asked what happened. ``verify`` reads only: nothing here retries, and no argv
carries ``--no-verify``.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from .conftest import SCRIPTS, SidecarBuilder, git_in
from .test_stage_plan import PIN, Scene, private_tree, refs_and_index

PKG = ".dev/tasks/to-do/plan1"
CLASSES = (
    "blocked-by-host",
    "hook-failed",
    "hook-rewrite",
    "hook-rewrite-evidence",
    "hook-rewrite-committed",
    "hook-rewrite-pinned",
    "commit-error",
)


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


@pytest.fixture
def vcs_plan(scripts_dir):
    return importlib.import_module("vcs_plan")


def sha256_of(repo, rel):
    return hashlib.sha256((repo.work / rel).read_bytes()).hexdigest()


class Flow:
    """One boundary, prepared the way the executor does, up to the commit call.

    ``Flow(...)`` records the task (Q0, an edit of ``src/a.py``, the accepted pin). A test may
    then edit the work tree (a person's edit, a staged entry) before ``ready()`` runs the
    plan, the prepared line, the candidate pin, the add and the worktree snapshot pin.
    """

    def __init__(self, repo, vcs, hook, managed=False):
        self.repo, self.vcs, self.hook, self.managed = repo, vcs, hook, managed
        repo.write("src/a.py", "old\n")
        repo.write("src/b.py", "old\n")
        repo.commit("base")
        if managed:
            repo.write(f"{PKG}/plan1.md", "the plan\n")
            repo.write(f"{PKG}/source.md", "the source\n")
            repo.write(f"{PKG}/artifacts/evidence.md", "evidence\n")
        self.s = Scene(repo, vcs, managed)
        self.s.start("1")
        repo.write("src/a.py", "new\n")
        self.s.accept("1", ["src/a.py"])

    def ready(self, pin_candidate=True, pin_worktree=True):
        s, repo = self.s, self.repo
        first = s.plan()
        assert first["status"] == "ok", first
        self.key, self.parent = first["key"], first["parent"]
        s.side.prepared(
            "1",
            key=self.key,
            parent=self.parent,
            paths=first["pathspec_file"]["sha256"],
            accepted=",".join(first["accepted"]),
            plan=sha256_of(repo, f"{PKG}/plan1.md") if self.managed else "-",
            source=sha256_of(repo, f"{PKG}/source.md") if self.managed else "-",
        )
        self.cand = s.plan(candidate=True)
        assert self.cand["status"] == "ok", self.cand
        spec = self.cand["pathspec_file"]
        assert spec["sha256"] == first["pathspec_file"]["sha256"]
        with open(spec["path"], "w", encoding="utf-8", newline="") as handle:
            handle.write(spec["content"])
        self.candidate_ref = self.cand["boundary_ref"]
        if pin_candidate:
            repo.git("update-ref", self.candidate_ref, self.cand["candidate_tree"])
        git_in(repo.work, *self.cand["add_argv"])
        self.worktree_ref = f"{PIN}/plan1/boundary-wt/{self.key}-a1"
        if pin_worktree:
            repo.git("update-ref", self.worktree_ref, private_tree(repo))
        return self

    def message(self, trailer=True):
        lines = [
            "feat: the first task",
            "",
            "T1: the first task",
            "",
            "Implement-Plan: plan1",
            "Implement-Task: T1 (compliant)",
        ]
        if trailer:
            lines.append(f"Implement-Boundary: {self.key}")
        ledger = os.path.relpath(self.s.ledger_path, self.repo.work)
        lines.append(f"Implement-Ledger: {ledger}")
        return "\n".join(lines) + "\n"

    def commit(self, action="pass", target=None, trailer=True):
        self.hook.set_action(action, target)
        return self.hook.commit(
            self.cand["commit_paths"], message=self.message(trailer)
        )

    def head(self):
        return self.repo.git("rev-parse", "HEAD").strip()

    def verify(self, rc, **over):
        args = dict(
            key=self.key,
            attempt=1,
            parent=self.parent,
            candidate_ref=self.candidate_ref,
            worktree_ref=self.worktree_ref,
            exit_code=rc,
            ledger=str(self.s.ledger_path),
            sidecar=str(self.s.side_path),
        )
        args.update(over)
        return self.vcs.run_verify(str(self.repo.work), **args)


@pytest.fixture
def flow(repo, vcs, hook_emulator):
    def make(managed=False):
        return Flow(repo, vcs, hook_emulator, managed)

    return make


MODES = pytest.mark.parametrize("managed", [False, True], ids=["legacy", "managed"])


def assert_refused_line(f, res, uncertain=False):
    """The executor's sidecar line for this result is one the parser accepts (FR-064)."""
    line = SidecarBuilder(Path("unused")).refused(
        "1",
        key=f.key,
        attempt=1,
        reason=res["reason"],
        rewritten=res.get("rewritten_ref"),
        uncertain=uncertain,
    )
    parsed = importlib.import_module("vcs_plan").parse_sidecar(line.lines[0] + "\n")
    done = parsed.terminal[f.key]
    assert done.reason == res["reason"]
    assert done.kind == ("uncertain" if uncertain else "refused")


# --- success ----------------------------------------------------------------------------------
@MODES
def test_a_clean_commit_is_proved_committed(flow, repo, managed):
    f = flow(managed).ready()
    done = f.commit()
    assert done.returncode == 0, done.stderr
    res = f.verify(0)
    assert res["status"] == "committed", res
    assert res["class"] is None and res["reason"] is None
    assert res["sha"] == f.head() == res["head_after"]
    assert res["head_before"] == f.parent
    assert "src/a.py" in res["changed_paths"]
    if not managed:
        assert res["changed_paths"] == ["src/a.py"]
    assert (res["outside_changed"], res["outside_paths"]) == (0, [])
    assert res["proof"]["parent"] and res["proof"]["trailer"]
    assert res["proof"]["candidate"] and res["proof"]["paths"]
    assert res["proof"]["plan_source"] is (True if managed else None)


# --- the classes with HEAD unchanged ------------------------------------------------------------
@MODES
def test_a_failing_hook_is_hook_failed_and_head_is_unchanged(flow, repo, managed):
    f = flow(managed).ready()
    done = f.commit("exit1")
    assert done.returncode == 1
    res = f.verify(1)
    assert (res["status"], res["class"], res["reason"]) == ("hook-failed",) * 3
    assert res["head_before"] == res["head_after"] == f.head() == f.parent
    assert res["changed_paths"] == [] and res["rewritten_tree"] is None
    assert res["sha"] is None
    assert_refused_line(f, res)


@MODES
def test_a_hook_that_rewrites_a_product_file_and_exits_1_is_hook_rewrite(
    flow, repo, managed
):
    f = flow(managed).ready()
    done = f.commit("rewrite_exit1", "src/a.py")
    assert done.returncode == 1
    res = f.verify(1)
    assert res["status"] == res["class"] == "hook-rewrite", res
    assert res["head_before"] == res["head_after"] == f.parent
    assert res["changed_paths"] == ["src/a.py"]
    # the executor pins the rewritten tree under the name the helper gives (FR-064)
    assert res["rewritten_ref"] == f"{PIN}/plan1/rewritten/{f.key}-a1"
    repo.git("update-ref", res["rewritten_ref"], res["rewritten_tree"])
    saved = repo.git("show", f"{res['rewritten_ref']}:src/a.py")
    assert saved.endswith("rewritten-by-hook\n")
    assert_refused_line(f, res)


def test_a_hook_that_rewrites_only_package_evidence_is_hook_rewrite_evidence(
    flow, repo
):
    f = flow(managed=True).ready()
    done = f.commit("rewrite_exit1", f"{PKG}/artifacts/evidence.md")
    assert done.returncode == 1
    res = f.verify(1)
    assert res["status"] == res["class"] == "hook-rewrite-evidence", res
    assert res["changed_paths"] == [f"{PKG}/artifacts/evidence.md"]
    assert res["head_after"] == f.parent
    assert res["rewritten_tree"] and res["rewritten_ref"]
    assert_refused_line(f, res)


@pytest.mark.parametrize("name", ["source.md", "plan1.md"])
def test_a_hook_that_rewrites_the_pinned_plan_or_source_is_hook_rewrite_pinned(
    flow, repo, name
):
    f = flow(managed=True).ready()
    done = f.commit("rewrite_exit1", f"{PKG}/{name}")
    assert done.returncode == 1
    res = f.verify(1)
    assert res["status"] == res["class"] == "hook-rewrite-pinned", res
    assert res["head_after"] == f.parent
    assert res["proof"]["plan_source"] is False
    assert_refused_line(f, res)


def test_a_failed_commit_call_with_exit_128_is_commit_error(flow, repo):
    f = flow().ready()
    (repo.work / ".git" / "index.lock").write_text("", encoding="utf-8")
    done = f.commit("pass")
    assert done.returncode == 128, done.stderr
    res = f.verify(128)
    assert res["status"] == res["class"] == "commit-error", res
    assert res["head_after"] == f.parent
    assert_refused_line(f, res)


def test_a_call_the_host_refused_is_blocked_by_host(flow, repo):
    f = flow().ready()  # the commit never ran: no exit status exists
    res = f.verify(-1)
    assert res["status"] == res["class"] == "blocked-by-host", res
    assert res["head_before"] == res["head_after"] == f.parent
    assert_refused_line(f, res)


def test_blocked_by_host_with_a_moved_head_is_not_taken_at_its_word(flow, repo):
    f = flow().ready()
    assert f.commit().returncode == 0
    res = f.verify(-1)
    assert res["status"] == "committed", res  # the history, not the claim, decides


# --- the class with HEAD moved ------------------------------------------------------------------
@MODES
def test_a_hook_that_rewrites_and_commits_is_hook_rewrite_committed(
    flow, repo, managed
):
    f = flow(managed).ready()
    done = f.commit("rewrite_add", "src/a.py")
    assert done.returncode == 0, done.stderr
    res = f.verify(0)
    assert res["status"] == res["class"] == "hook-rewrite-committed", res
    assert res["head_before"] == f.parent and res["head_after"] == f.head() != f.parent
    assert res["rewritten_tree"] == repo.git("rev-parse", "HEAD^{tree}").strip()
    assert res["sha"] is None  # the commit is not proved
    assert "src/a.py" in res["changed_paths"]
    assert_refused_line(f, res)


# --- pending, uncertain and the unclassified exits --------------------------------------------
def test_head_at_the_parent_after_a_good_exit_is_pending(flow, repo):
    f = flow().ready()
    for rc in (0, None):
        res = f.verify(rc)
        assert res["status"] == "pending", res
        assert res["class"] is None and res["head_after"] == f.parent


def test_a_prepared_attempt_without_its_pin_at_the_parent_is_pending(flow, repo):
    f = flow().ready(pin_candidate=False)  # DD-11: nothing was committed
    res = f.verify(1)
    assert res["status"] == "pending" and res["reason"] == "candidate-missing", res


def test_a_commit_without_the_candidate_pin_is_uncertain(flow, repo):
    f = flow().ready(pin_candidate=False)
    assert f.commit().returncode == 0
    res = f.verify(0)
    assert (res["status"], res["reason"]) == ("uncertain", "candidate-missing")
    assert_refused_line(f, res, uncertain=True)


def test_a_persons_later_commit_on_top_is_uncertain(flow, repo):
    f = flow().ready()
    assert f.commit().returncode == 0
    boundary_commit = f.head()
    repo.write("person.txt", "by hand\n")
    repo.commit("a commit by hand")
    res = f.verify(0)
    assert (res["status"], res["reason"]) == ("uncertain", "history-differs"), res
    assert res["head_before"] == f.parent and res["head_after"] != boundary_commit
    assert res["sha"] is None
    assert_refused_line(f, res, uncertain=True)


def test_a_commit_that_does_not_carry_the_key_is_uncertain(flow, repo):
    f = flow().ready()
    assert f.commit(trailer=False).returncode == 0
    res = f.verify(0)
    assert (res["status"], res["reason"]) == ("uncertain", "trailer-missing"), res


def test_a_commit_that_is_not_the_authorized_set_is_uncertain(flow, repo):
    f = flow().ready()
    path_file = Path(f.cand["pathspec_file"]["path"])
    path_file.write_text("src/other.py\0", encoding="utf-8", newline="")
    assert f.commit().returncode == 0
    res = f.verify(0)  # the path file no longer matches the prepared line's hash
    assert (res["status"], res["reason"]) == ("uncertain", "paths-mismatch"), res
    assert res["proof"]["paths"] is False


@pytest.mark.parametrize("rc", [137, 143, 255])
def test_an_exit_above_128_is_not_classified(flow, repo, rc):
    f = flow().ready()
    res = f.verify(rc)
    assert res["status"] == "interrupted" and res["reason"] == "commit-interrupted"
    assert res["class"] is None and res["sha"] is None
    assert res["outside"] == "deferred" and res["outside_changed"] is None


def test_a_killed_commit_leaves_head_and_is_not_classified(flow, repo, hook_emulator):
    f = flow().ready()
    hook_emulator.set_action("block")
    proc = hook_emulator.start_blocked_commit(
        f.cand["commit_paths"], message=f.message()
    )
    hook_emulator.kill_group(proc)
    res = f.verify(137)
    assert res["status"] == "interrupted" and res["head_after"] == f.parent


# --- the outside-S comparison (FR-113) ----------------------------------------------------------
def test_a_person_edit_outside_the_set_that_survives_gives_no_difference(flow, repo):
    f = flow()
    repo.write("src/b.py", "person edit\n")  # unstaged, outside the commit set
    f.ready()
    assert f.commit().returncode == 0
    assert (repo.work / "src/b.py").read_text(encoding="utf-8") == "person edit\n"
    res = f.verify(0)
    assert res["status"] == "committed"
    assert (res["outside"], res["outside_changed"]) == ("unchanged", 0)


def test_an_edit_the_hook_stash_overwrote_is_reported_and_the_commit_stays_proved(
    flow, repo
):
    f = flow()
    repo.write("src/b.py", "person edit\n")
    repo.git("update-index", "--assume-unchanged", "src/b.py")
    repo.write("README.md", "a visible unstaged edit\n")  # makes the hook check out
    f.ready()
    assert f.commit().returncode == 0
    assert (repo.work / "src/b.py").read_text(encoding="utf-8") == "old\n"
    res = f.verify(0)
    assert res["status"] == "committed" and res["sha"] == f.head()  # not relabelled
    assert (res["outside"], res["outside_changed"]) == ("outside-changed", 1)
    assert res["outside_paths"] == ["src/b.py"]


def test_deletions_additions_and_mode_changes_outside_the_set_are_all_reported(
    flow, repo
):
    repo.write("src/c.py", "c\n")  # the base commit of the flow holds both
    repo.write("src/run.sh", "#!/bin/sh\n")
    f = flow()
    f.ready()
    assert f.commit().returncode == 0
    os.remove(repo.work / "src/c.py")  # a deletion
    repo.write("src/new.txt", "added\n")  # an addition
    os.chmod(repo.work / "src/run.sh", 0o755)  # a mode change
    res = f.verify(0)
    assert res["outside_paths"] == ["src/c.py", "src/new.txt", "src/run.sh"], res


def test_a_symlink_swapped_for_a_file_outside_the_set_is_reported(flow, repo):
    repo.write("src/link", "target\n")  # the base commit of the flow holds it
    f = flow()
    f.ready()
    assert f.commit().returncode == 0
    os.remove(repo.work / "src/link")
    os.symlink("src/a.py", repo.work / "src/link")
    assert f.verify(0)["outside_paths"] == ["src/link"]


def test_a_comparison_that_cannot_complete_is_outside_unverified(flow, repo):
    f = flow().ready()
    assert f.commit().returncode == 0
    res = f.verify(0, worktree_ref=f"{PIN}/plan1/boundary-wt/missing-a1")
    assert res["status"] == "committed"  # the commit proof stands apart
    assert res["outside"] == "outside-unverified"
    assert res["outside_changed"] is None and res["outside_paths"] == []


def test_a_missing_worktree_pin_is_outside_unverified_for_a_class_too(flow, repo):
    f = flow().ready(pin_worktree=False)
    assert f.commit("exit1").returncode == 1
    res = f.verify(1)
    assert res["status"] == "hook-failed"
    assert res["outside"] == "outside-unverified"


def test_the_full_outside_set_is_counted_but_the_json_list_is_capped(flow, repo, vcs):
    f = flow().ready()
    assert f.commit().returncode == 0
    for n in range(250):
        repo.write(f"extra/f{n:03d}.txt", "x\n")
    res = f.verify(0)
    assert res["outside_changed"] == 250 and len(res["outside_paths"]) == 250
    shown = json.loads(vcs.emit_text(res))
    assert len(shown["outside_paths"]) == 200 and shown["truncated"] is True
    assert shown["outside_changed"] == 250


# --- verify writes nothing and never retries ---------------------------------------------------
@pytest.mark.parametrize(
    "action,target,rc",
    [("exit1", None, 1), ("rewrite_exit1", "src/a.py", 1), ("pass", None, 0)],
)
def test_verify_is_byte_identical_and_writes_nothing(
    flow, repo, vcs, action, target, rc
):
    f = flow().ready()
    f.commit(action, target)
    status = repo.git("status", "--porcelain")  # this call may refresh the index: first
    before = (refs_and_index(repo), f.head())
    first = vcs.emit_text(f.verify(rc))
    second = vcs.emit_text(f.verify(rc))
    assert first == second
    assert (refs_and_index(repo), f.head()) == before  # no ref, index entry or commit
    assert repo.git("status", "--porcelain") == status  # and no work-tree change


def test_verify_runs_only_reads_and_no_argv_names_no_verify(
    flow, repo, vcs_plan, hook_emulator
):
    f = flow().ready()
    assert f.commit("exit1").returncode == 1
    seen = []

    def make(top, **kw):
        runner = vcs_plan.GitRunner(top, record=True, **kw)
        seen.append(runner)
        return runner

    f.verify(1, make_runner=make)
    calls = [call for runner in seen for call in runner.calls]
    assert calls
    verbs = set()
    for call in calls:
        words = call[4:]
        if words[0] == "-C":
            words = words[2:]
        verbs.add(words[0])
        assert "--no-verify" not in call and "--amend" not in call
    reads = {
        "rev-parse",
        "cat-file",
        "diff",
        "ls-tree",
        "read-tree",
        "add",
        "write-tree",
    }
    assert verbs <= reads  # the last three run only on a private index
    assert "commit" not in verbs
    assert "--no-verify" not in hook_emulator._argv(["x"], "m")  # the tests' own argv


# --- the command line ---------------------------------------------------------------------------
def run_cli(repo, *args):
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "vcs.py"),
            "verify",
            "--cwd",
            str(repo.work),
            *args,
        ],
        capture_output=True,
        text=True,
    )


def cli_args(f, rc, **over):
    values = {
        "--key": f.key,
        "--attempt": "1",
        "--parent": f.parent,
        "--candidate-ref": f.candidate_ref,
        "--worktree-ref": f.worktree_ref,
        "--exit": str(rc),
        "--ledger": str(f.s.ledger_path),
        "--sidecar": str(f.s.side_path),
    }
    values.update(over)
    return [token for pair in values.items() for token in pair]


def test_cli_prints_one_json_object_and_exits_zero(flow, repo):
    f = flow().ready()
    assert f.commit().returncode == 0
    done = run_cli(repo, *cli_args(f, 0))
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["verb"], data["status"]) == ("verify", "committed")
    assert data["vcs_contract"] == "1" and data["sha"] == f.head()


def test_cli_takes_a_negative_exit_for_a_refused_host_call(flow, repo):
    f = flow().ready()
    done = run_cli(repo, *cli_args(f, -1))
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["status"] == "blocked-by-host"


def test_cli_without_ledger_and_sidecar_still_proves_the_commit(flow, repo):
    f = flow().ready()
    assert f.commit().returncode == 0
    args = cli_args(f, 0)
    for name in ("--ledger", "--sidecar"):
        at = args.index(name)
        del args[at : at + 2]
    done = run_cli(repo, *args)
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert data["status"] == "committed" and data["proof"]["paths"] is None


@pytest.mark.parametrize(
    "over",
    [
        {"--key": "abc"},
        {"--key": "G" * 64},
        {"--parent": "a" * 39},
        {"--attempt": "0"},
        {"--candidate-ref": "-x"},
        {"--worktree-ref": "heads/main"},
        {"--exit": "soon"},
    ],
    ids=[
        "short-key",
        "non-hex-key",
        "short-parent",
        "attempt-0",
        "dash-ref",
        "no-refs",
        "exit",
    ],
)
def test_cli_usage_errors_exit_64(flow, repo, over):
    f = flow().ready()
    done = run_cli(repo, *cli_args(f, 0, **over))
    assert done.returncode == 64 and done.stdout == ""


def test_cli_a_missing_required_option_exits_64(repo):
    done = run_cli(repo, "--key", "a" * 64)
    assert done.returncode == 64 and done.stdout == ""


def test_cli_outside_a_repository_is_refused(tmp_path):
    folder = tmp_path / "plain"
    folder.mkdir()
    args = [
        "--key", "a" * 64, "--attempt", "1", "--parent", "b" * 40,
        "--candidate-ref", "refs/x/c", "--worktree-ref", "refs/x/w", "--exit", "0",
    ]  # fmt: skip
    done = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "vcs.py"),
            "verify",
            "--cwd",
            str(folder),
            *args,
        ],
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0
    data = json.loads(done.stdout)
    assert (data["status"], data["reason"]) == ("refused", "not-a-repo")


def test_a_sidecar_that_does_not_hold_the_attempt_is_refused(flow, repo):
    f = flow().ready()
    res = f.verify(0, attempt=2)
    assert (res["status"], res["reason"]) == ("refused", "unknown-attempt")
    res = f.verify(0, parent="c" * 40)
    assert (res["status"], res["reason"]) == ("refused", "parent-mismatch")


def test_a_corrupt_sidecar_is_refused(flow, repo):
    f = flow().ready()
    with open(f.s.side_path, "a", encoding="utf-8") as handle:
        handle.write("not a line form\n")
    res = f.verify(0)
    assert (res["status"], res["reason"]) == ("refused", "sidecar-corrupt")


def test_every_class_the_helper_names_is_in_the_closed_list(vcs_plan):
    assert tuple(vcs_plan.HOOK_CLASSES) == CLASSES
