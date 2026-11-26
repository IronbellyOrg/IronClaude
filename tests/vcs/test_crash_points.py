"""T-22 crash points, the segment and eligibility cases of T-19, and the retry rules (FR-065,
FR-102 to FR-109, FR-116, FR-132, DD-5, DD-11; design sections 5.2, 5.4, 5.6).

``reconcile`` reads the ledger, ``commits.md`` and git, and prints what each boundary is and the
one action this run may take; it writes nothing. The tests below play the executor with a small
stand-in (``Exec``): it does what the commit step of the protocol does, one visible call at a
time, and a test can stop it after any step to model a crash. A "resume" is the executor's
Wave 0: append a ``run`` line, reconcile, and perform only the action reconcile names. Every
case runs on a real temporary repository with a real ledger, sidecar, pins and commits.

The quiescence probe (FR-116) is replaced by a stub in every case except the ones that test it:
a real process list is not a fact these cases should depend on.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import subprocess
import sys

import pytest

from .conftest import SCRIPTS, SidecarBuilder, git_in
from .test_stage_plan import PIN, Scene, private_tree, refs_and_index

PKG = ".dev/tasks/to-do/plan1"


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


@pytest.fixture
def plan_mod(scripts_dir):
    return importlib.import_module("vcs_plan")


@pytest.fixture(autouse=True)
def no_live_git(scripts_dir, monkeypatch):
    """No git or hook process is running (the real probe has its own case below).

    Returns the real probe, for the one test that needs it."""
    plan = importlib.import_module("vcs_plan")
    original = plan._live_git_processes
    monkeypatch.setattr(plan, "_live_git_processes", lambda top: [])
    return original


def sha256_of(repo, rel):
    return hashlib.sha256((repo.work / rel).read_bytes()).hexdigest()


def commits_for(repo, key):
    out = repo.git("rev-list", "--count", f"--grep=Implement-Boundary: {key}", "HEAD")
    return int(out.strip())


def work_digest(root):
    """Every byte of the work tree outside ``.git``: a verb that writes a file changes this."""
    seen = {}
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            path = os.path.join(folder, name)
            with open(path, "rb") as handle:
                seen[os.path.relpath(path, root)] = hashlib.sha256(
                    handle.read()
                ).hexdigest()
    return seen


class Exec:
    """The executor's side of the commit step (design 5.5), stoppable after any step."""

    def __init__(self, s, repo, vcs, managed):
        self.s, self.repo, self.vcs, self.managed = s, repo, vcs, managed
        self.runs = 1  # the scene starts with run 1 (on, offset 0)
        if managed:
            self.s.ledger.lines[1] = (
                f"PLAN: sha256={sha256_of(repo, f'{PKG}/plan1.md')} "
                f"source_sha256={sha256_of(repo, f'{PKG}/source.md')}"
            )

    # --- the ledger side -------------------------------------------------------------------
    def task(self, tid="1", path="src/a.py", text="new\n"):
        """Q0, an edit and the accepted pin: the task is complete (an anchor line)."""
        self.s.start(tid)
        self.repo.write(path, text)
        self.s.accept(tid, [path])

    def new_run(self, flag=True, revoked=False):
        """Wave 0 of a new invocation: a ``run`` line at the current ledger offset."""
        self.s.write()
        self.runs += 1
        self.s.side.run(
            self.runs,
            "on" if flag else "off",
            ledger_lines=SidecarBuilder.ledger_k(self.s.ledger_path),
            branch="refs/heads/main",
            revoked=revoked,
        )
        self.s.write()

    # --- the helper side -------------------------------------------------------------------
    def reconcile(self, flag=True):
        self.s.write()
        return self.vcs.run_reconcile(
            str(self.repo.work),
            str(self.s.ledger_path),
            str(self.s.side_path),
            str(self.s.run_dir),
            str(self.s.pkg) if self.s.pkg else None,
            flag,
        )

    def only(self, flag=True):
        out = self.reconcile(flag)
        assert out["status"] == "ok", out
        (b,) = out["boundaries"]
        return b

    # --- the commit procedure ----------------------------------------------------------------
    def attempt(self, stop_after=None):
        """Steps 1 to 9 of the commit procedure; ``stop_after`` is a step name to crash after:
        ``prepared`` (the prepared line), ``staged`` (pins and the add), ``committed``."""
        s, repo, vcs = self.s, self.repo, self.vcs
        first = s.plan()
        assert first["status"] == "ok", first
        key, parent, n = first["key"], first["parent"], first["attempt"]
        ids = ",".join(first["tasks"])
        s.side.prepared(
            ids,
            key=key,
            attempt=n,
            parent=parent,
            paths=first["pathspec_file"]["sha256"],
            accepted=",".join(first["accepted"]),
            plan=sha256_of(repo, f"{PKG}/plan1.md") if self.managed else "-",
            source=sha256_of(repo, f"{PKG}/source.md") if self.managed else "-",
        )
        s.write()
        if stop_after == "prepared":
            return key
        cand = s.plan(candidate=True)
        assert cand["status"] == "ok", cand
        spec = cand["pathspec_file"]
        with open(spec["path"], "w", encoding="utf-8", newline="") as handle:
            handle.write(spec["content"])
        repo.git("update-ref", cand["boundary_ref"], cand["candidate_tree"])
        git_in(repo.work, *cand["add_argv"])
        wt_ref = f"{PIN}/plan1/boundary-wt/{key}-a{n}"
        repo.git("update-ref", wt_ref, private_tree(repo))
        if stop_after == "staged":
            return key
        ledger = os.path.relpath(s.ledger_path, repo.work)
        message = (
            f"feat: the work of T{ids}\n\nT{ids}: the work\n\n"
            f"Implement-Plan: plan1\nImplement-Task: T{ids.split(',')[0]} (compliant)\n"
            f"Implement-Boundary: {key}\nImplement-Ledger: {ledger}\n"
        )
        with open(cand["message_path"], "w", encoding="utf-8") as handle:
            handle.write(message)
        git_in(repo.work, *cand["commit_argv"])
        if stop_after == "committed":
            return key
        res = vcs.run_verify(
            str(repo.work),
            key,
            n,
            parent,
            cand["boundary_ref"],
            wt_ref,
            0,
            ledger=str(s.ledger_path),
            sidecar=str(s.side_path),
        )
        assert res["status"] == "committed", res
        s.side.commit(ids, key=key, attempt=n, sha=res["sha"])
        s.write()
        return key

    def resume(self, flag=True):
        """A later invocation: ``run`` line, reconcile, then only the action reconcile names."""
        self.new_run(flag)
        out = self.reconcile(flag)
        assert out["status"] == "ok", out
        for b in out["boundaries"]:
            ids = ",".join(b["members"])
            if b["action"] in ("prepare", "retry"):
                self.attempt()
            elif b["action"] == "record-recovered":
                self.s.side.commit(
                    ids,
                    key=b["key"],
                    attempt=b["attempt"],
                    sha=b["sha"],
                    recovered=True,
                )
            elif b["action"] == "record-skipped":
                self.s.side.skipped(ids, key=b["key"], reason=b["reason"])
        if (
            self.managed
        ):  # every run appends a line of evidence after reconcile (FR-132)
            path = self.repo.work / PKG / "artifacts" / "codegraph.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a", encoding="utf-8") as handle:
                handle.write(f"run {self.runs}: codegraph ready\n")
        self.s.write()
        return out


@pytest.fixture
def make(repo, vcs):
    def build(managed=False):
        for name in ("a", "b", "c"):
            repo.write(f"src/{name}.py", "old\n")
        repo.commit("base")
        if managed:  # untracked, like a package the executor works in
            repo.write(f"{PKG}/plan1.md", "the plan\n")
            repo.write(f"{PKG}/source.md", "the source\n")
        return Exec(Scene(repo, vcs, managed), repo, vcs, managed)

    return build


MODES = pytest.mark.parametrize("managed", [False, True], ids=["legacy", "managed"])


def row(b):
    return (b["state"], b["action"], b["reason"])


# =============================================================================================
# T-22: a crash at each point, then two resumes (AC-16, FR-108, FR-130)
# =============================================================================================
CRASHES = [None, "prepared", "staged", "committed", "terminal"]
FIRST_ACTION = {
    None: "prepare",
    "prepared": "retry",
    "staged": "retry",
    "committed": "record-recovered",
    "terminal": "none",
}


@MODES
@pytest.mark.parametrize(
    "crash",
    CRASHES,
    ids=[
        "before-prepared",
        "after-prepared",
        "after-staging",
        "after-commit",
        "after-terminal",
    ],
)
def test_a_crash_at_each_point_then_two_resumes_gives_one_commit(
    make, repo, crash, managed
):
    ex = make(managed)
    ex.task()
    key = ex.s.plan()["key"]
    if crash == "terminal":
        ex.attempt()
    elif crash:
        ex.attempt(stop_after=crash)
    head = repo.git("rev-parse", "HEAD").strip()
    first = ex.resume()
    second = ex.resume()
    (b1,) = first["boundaries"]
    (b2,) = second["boundaries"]
    assert b1["key"] == b2["key"] == key
    assert b1["action"] == FIRST_ACTION[crash]
    assert b2["action"] == "none" and b2["state"] == "settled"
    assert commits_for(repo, key) == 1
    assert repo.git("rev-list", "--count", f"{head}..HEAD").strip() == (
        "0" if crash in ("committed", "terminal") else "1"
    )


@MODES
def test_a_commit_before_the_terminal_line_is_recovered_not_repeated(
    make, repo, managed
):
    ex = make(managed)
    ex.task()
    key = ex.attempt(stop_after="committed")
    sha = repo.git("rev-parse", "HEAD").strip()
    ex.new_run()  # the new run line changes the sidecar bytes after the commit was made
    (b,) = ex.reconcile()["boundaries"]
    assert row(b) == ("pending", "record-recovered", "commit-proved")
    assert (b["sha"], b["attempt"], b["head"]) == (sha, 1, sha)
    ex.resume()
    side = (ex.s.side_path).read_text(encoding="utf-8")
    assert f"commit recovered={sha} key={key} attempt=1" in side
    assert commits_for(repo, key) == 1


def test_a_managed_run_gives_no_false_hook_rewrite_committed_after_a_new_run_line(
    make, repo, vcs
):
    ex = make(managed=True)
    ex.task()
    key = ex.attempt(stop_after="committed")
    for _ in range(2):  # two new run lines, each changing the sidecar in the work tree
        ex.new_run()
    (b,) = ex.reconcile()["boundaries"]
    assert b["state"] == "pending" and b["action"] == "record-recovered"
    ex.s.side.commit("1", key=key, attempt=1, sha=b["sha"], recovered=True)
    assert ex.only()["state"] == "settled"


@MODES
def test_a_prepared_line_without_its_pins_at_the_parent_gives_attempt_n_plus_one(
    make, repo, managed
):
    ex = make(managed)
    ex.task()
    key = ex.attempt(stop_after="prepared")
    refs = repo.git("for-each-ref", f"{PIN}/plan1/boundary", f"{PIN}/plan1/boundary-wt")
    assert refs == ""  # no candidate pin and no worktree pin exist (DD-11)
    ex.new_run()
    b = ex.only()
    assert row(b) == ("pending", "retry", "retry-allowed")
    assert (b["attempt"], b["next_attempt"]) == (1, 2)
    ex.resume()
    side = ex.s.side_path.read_text(encoding="utf-8")
    assert f"commit prepared key={key} attempt=2" in side
    assert (
        f"commit sha={repo.git('rev-parse', 'HEAD').strip()} key={key} attempt=2"
        in side
    )


@MODES
def test_the_evidence_line_every_run_appends_never_blocks_a_retry(make, repo, managed):
    ex = make(managed)
    ex.task()
    ex.attempt(stop_after="prepared")
    path = repo.work / PKG / "artifacts" / "codegraph.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("a later line\n", encoding="utf-8")
    ex.new_run()
    assert ex.only()["action"] == "retry"


@MODES
def test_a_person_committing_on_top_of_the_boundary_commit_is_uncertain(
    make, repo, managed
):
    ex = make(managed)
    ex.task()
    ex.attempt(stop_after="committed")
    repo.write("src/z.py", "z\n")
    repo.git("add", "--", "src/z.py")
    repo.git("commit", "-q", "-m", "by hand")
    for flag in (True, False):
        ex.new_run(flag)
        b = ex.only(flag)
        assert row(b) == ("uncertain", "stop-uncertain", "uncertain")


@pytest.mark.parametrize("crash", ["prepared", "staged", "committed"])
@MODES
def test_git_gc_prune_now_between_the_crash_and_the_resume_loses_nothing(
    make, repo, crash, managed
):
    ex = make(managed)
    ex.task()
    key = ex.attempt(stop_after=crash)
    git_in(repo.work, "gc", "-q", "--prune=now")
    accepted = repo.git("rev-parse", f"{PIN}/plan1/accepted/T1-s1^{{tree}}").strip()
    git_in(repo.work, "cat-file", "-e", accepted)  # the pinned tree survived
    out = ex.resume()
    assert out["boundaries"][0]["action"] == FIRST_ACTION[crash]
    ex.resume()
    assert commits_for(repo, key) == 1


# =============================================================================================
# T-19: eligibility and segments, read through reconcile (FR-101 to FR-105, FR-109, FR-058)
# =============================================================================================
@MODES
def test_a_task_completed_outside_an_on_segment_is_never_committed(make, repo, managed):
    ex = make(managed)
    ex.s.side = SidecarBuilder(ex.s.side_path).run(
        1, "off", ledger_lines=0, branch="refs/heads/main"
    )
    ex.task()
    ex.new_run(True)
    b = ex.only()
    assert row(b) == ("settled", "none", "not-authorized")
    ex.resume()
    assert commits_for(repo, b["key"]) == 0


def test_a_re_review_line_in_a_later_on_segment_does_not_authorize(make, repo):
    ex = make()
    ex.s.side = SidecarBuilder(ex.s.side_path).run(
        1, "off", ledger_lines=0, branch="refs/heads/main"
    )
    ex.task()
    ex.new_run(True)
    ex.s.ledger.complete("1", files="src/a.py")  # a re-review line, written under `on`
    b = ex.only()
    assert row(b) == ("settled", "none", "not-authorized")


@MODES
def test_an_unflagged_resume_after_a_flagged_run_appends_no_commit_and_loses_no_pin(
    make, repo, managed
):
    ex = make(managed)
    ex.task()
    ex.new_run(False)
    ex.s.write()
    before = (refs_and_index(repo), work_digest(repo.work))
    out = ex.vcs.run_reconcile(
        str(repo.work),
        str(ex.s.ledger_path),
        str(ex.s.side_path),
        str(ex.s.run_dir),
        str(ex.s.pkg) if ex.s.pkg else None,
        False,
    )
    assert (refs_and_index(repo), work_digest(repo.work)) == before  # nothing written
    (b,) = out["boundaries"]
    assert row(b) == ("due", "stop-unsettled", "unsettled")
    repo.git(
        "rev-parse", "--verify", f"{PIN}/plan1/accepted/T1-s1"
    )  # the pin is still there
    assert commits_for(repo, b["key"]) == 0
    ex.resume(True)  # the flagged run that follows makes the one commit
    assert commits_for(repo, b["key"]) == 1


@MODES
def test_the_unflagged_reconcile_of_every_unsettled_state_returns_the_stop_action(
    make, repo, managed
):
    ex = make(managed)
    ex.task()
    ex.attempt(stop_after="prepared")  # pending, open, at the parent
    ex.new_run(False)
    assert row(ex.only(False)) == ("pending", "stop-unsettled", "unsettled")
    ex.s.side.refused("1", key=ex.only(False)["key"], attempt=1, reason="hook-failed")
    assert row(ex.only(False)) == ("refused", "stop-unsettled", "unsettled")


def test_an_unflagged_run_may_record_a_proved_existing_commit_but_never_commits(
    make, repo
):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="committed")
    ex.resume(False)
    assert "recovered=" in ex.s.side_path.read_text(encoding="utf-8")
    assert commits_for(repo, key) == 1


def test_a_mixed_batch_returns_record_skipped_and_commits_nothing(make, repo):
    ex = make()
    ex.s.start("1")
    ex.s.start("2")
    repo.write("src/a.py", "new\n")
    repo.write("src/b.py", "new\n")
    ex.s.accept("1", ["src/a.py"])
    ex.new_run(False)  # task 2 completes under `off`
    ex.s.accept("2", ["src/b.py"])
    ex.new_run(True)
    b = ex.only()
    assert b["members"] == ["1", "2"]
    assert row(b) == ("due", "record-skipped", "mixed-authorization")
    ex.resume()
    assert commits_for(repo, b["key"]) == 0
    assert ex.only()["state"] == "settled"
    assert "commit skipped" in ex.s.side_path.read_text(encoding="utf-8")


def test_an_empty_commit_set_returns_record_skipped(make, repo):
    ex = make()
    ex.s.start("1")
    ex.s.accept("1", ["src/a.py"])  # the task changed nothing
    ex.new_run(True)
    assert row(ex.only()) == ("due", "record-skipped", "empty")
    ex.new_run(False)
    assert row(ex.only(False)) == ("due", "stop-unsettled", "unsettled")


@MODES
def test_without_a_sidecar_and_without_the_flag_nothing_is_listed_or_written(
    make, repo, managed
):
    ex = make(managed)
    ex.task()
    ex.s.ledger.write()
    assert not ex.s.side_path.exists()
    before = (refs_and_index(repo), work_digest(repo.work))
    out = ex.vcs.run_reconcile(
        str(repo.work),
        str(ex.s.ledger_path),
        str(ex.s.side_path),
        str(ex.s.run_dir),
        str(ex.s.pkg) if ex.s.pkg else None,
        False,
    )
    assert out["status"] == "ok" and out["boundaries"] == []
    assert out["runs"] == [] and out["segments"] == []
    assert not ex.s.side_path.exists()
    assert (refs_and_index(repo), work_digest(repo.work)) == before


def test_a_revocation_stops_the_commits_of_the_tasks_after_it(make, repo):
    ex = make()
    ex.task("1", "src/a.py")
    key1 = ex.attempt()
    ex.new_run(False, revoked=True)
    ex.task("2", "src/b.py")
    ex.new_run(True)
    first, second = ex.reconcile()["boundaries"]
    assert first["key"] == key1 and row(first) == ("settled", "none", "committed")
    assert row(second) == ("settled", "none", "not-authorized")
    ex.resume()
    assert commits_for(repo, second["key"]) == 0


def test_a_revoked_run_gets_the_stop_action_for_a_due_boundary(make, repo):
    ex = make()
    ex.task()
    ex.new_run(False, revoked=True)
    assert row(ex.only(False)) == ("due", "stop-unsettled", "unsettled")
    runs = ex.reconcile(False)["runs"]
    assert [r["revoked"] for r in runs] == [False, True]


@pytest.mark.parametrize("flag", [True, False])
def test_a_later_start_by_a_stale_installed_copy_is_out_of_protocol(make, repo, flag):
    ex = make()
    ex.task()
    ex.s.start("2")  # an old copy ignores the flag and starts the next task
    ex.new_run(flag)
    first, second = ex.reconcile(flag)["boundaries"]
    assert row(first) == ("out-of-protocol", "stop-out-of-protocol", "out-of-protocol")
    assert row(second) == ("settled", "none", "incomplete")


def test_a_changed_managed_plan_refuses_before_anything_is_prepared(make, repo):
    ex = make(managed=True)
    ex.task()
    ex.new_run()
    assert ex.reconcile()["status"] == "ok"
    repo.write(f"{PKG}/plan1.md", "the plan, edited\n")
    before = refs_and_index(repo)
    out = ex.reconcile()
    assert (out["status"], out["reason"]) == ("refused", "plan-changed")
    assert out["boundaries"] == [] and "plan" in out["detail"]
    assert refs_and_index(repo) == before
    repo.write(f"{PKG}/plan1.md", "the plan\n")
    repo.write(f"{PKG}/source.md", "the source, edited\n")
    assert ex.reconcile()["reason"] == "plan-changed"


def test_a_plan_changed_before_the_first_start_is_not_a_refusal(make, repo):
    ex = make(managed=True)
    ex.new_run()
    repo.write(f"{PKG}/plan1.md", "edited before any task started\n")
    out = ex.reconcile()
    assert (out["status"], out["boundaries"]) == ("ok", [])


def test_a_resumed_batch_makes_one_commit_listing_every_member(make, repo):
    ex = make()
    for tid in "123":
        ex.s.start(tid)
    for tid, name in zip("123", "abc"):
        repo.write(f"src/{name}.py", "new\n")
    ex.s.accept("1", ["src/a.py"])
    ex.s.accept("2", ["src/b.py"])
    ex.s.ledger.halt("3")
    ex.new_run()
    halted = ex.only()
    assert row(halted) == ("settled", "none", "incomplete")  # a halt gives no commit
    assert commits_for(repo, halted["key"]) == 0
    ex.s.accept("3", ["src/c.py"])  # the resume completes it, still under run 2
    ex.new_run()
    b = ex.only()
    assert b["members"] == ["1", "2", "3"] and b["action"] == "prepare"
    assert b["key"] == halted["key"]
    ex.resume()
    assert commits_for(repo, b["key"]) == 1
    changed = repo.git("show", "--name-only", "--format=", "HEAD").split()
    assert {"src/a.py", "src/b.py", "src/c.py"} <= set(changed)


@pytest.mark.parametrize(
    ("order", "authorized"), [(("off", "on"), True), (("on", "off"), False)]
)
def test_equal_offsets_resolve_by_sidecar_order(make, repo, order, authorized):
    ex = make()
    ex.s.write()
    k = SidecarBuilder.ledger_k(ex.s.ledger_path)
    ex.s.side = SidecarBuilder(ex.s.side_path)  # no first run line: the pair below only
    for n, mode in enumerate(order, 1):
        ex.s.side.run(n, mode, ledger_lines=k, branch="refs/heads/main")
    ex.runs = 2
    ex.task()
    out = ex.reconcile(True)
    (b,) = out["boundaries"]
    assert (b["action"] == "prepare") is authorized
    first, second = out["segments"]
    assert (
        first["empty"] and not second["empty"]
    )  # the earlier of two equal offsets is empty
    assert second["flag"] == order[1]


def test_an_unterminated_last_ledger_line_is_counted_in_the_earlier_segment(make, repo):
    ex = make()
    ex.s.side = SidecarBuilder(ex.s.side_path).run(
        1, "off", ledger_lines=0, branch="refs/heads/main"
    )
    ex.task()
    ex.s.ledger.write()
    text = ex.s.ledger_path.read_text(encoding="utf-8")
    ex.s.ledger_path.write_text(
        text.rstrip("\n"), encoding="utf-8"
    )  # parseable, unterminated
    ex.s.side.run(
        2, "on", ledger_lines=SidecarBuilder.ledger_k(ex.s.ledger_path),
        branch="refs/heads/main",
    )  # fmt: skip
    ex.s.side.write()
    out = ex.vcs.run_reconcile(
        str(repo.work),
        str(ex.s.ledger_path),
        str(ex.s.side_path),
        str(ex.s.run_dir),
        None,
        True,
    )
    (b,) = out["boundaries"]
    assert row(b) == (
        "settled",
        "none",
        "not-authorized",
    )  # the last line is under run 1


def test_the_segments_cover_the_ledger_and_the_runs_are_listed(make, repo):
    ex = make()
    ex.task()
    ex.new_run(False)
    ex.s.ledger.add("T9: Ruling: a — b — c")
    ex.new_run(True)
    out = ex.reconcile(True)
    assert [r["run"] for r in out["runs"]] == [1, 2, 3]
    assert [r["flag"] for r in out["runs"]] == ["on", "off", "on"]
    total = SidecarBuilder.ledger_k(ex.s.ledger_path)
    spans = [(s["first_line"], s["last_line"], s["flag"]) for s in out["segments"]]
    assert spans[0][0] == 1 and spans[-1][1] == total
    assert all(a[1] + 1 == b[0] for a, b in zip(spans, spans[1:]))


# --- refusals before any boundary is read --------------------------------------------------------
def spoil_corrupt(ex):
    ex.s.side.raw("not a sidecar line")


def spoil_truncated(ex):
    """The sidecar is written below without its final newline (a cut write)."""


def spoil_decreasing(ex):
    ex.s.side.run(2, "on", ledger_lines=0, branch="refs/heads/main")
    ex.s.side.lines[0] = ex.s.side.lines[0].replace("ledger-lines=0", "ledger-lines=3")


def spoil_beyond(ex):
    ex.s.side.run(2, "on", ledger_lines=999, branch="refs/heads/main")


def spoil_dash_branch_on(ex):
    ex.s.side.run(2, "on", ledger_lines=1, branch="-")


@pytest.mark.parametrize(
    ("spoil", "reason"),
    [
        (spoil_corrupt, "sidecar-corrupt"),
        (spoil_truncated, "sidecar-corrupt"),
        (spoil_decreasing, "sidecar-mismatch"),
        (spoil_beyond, "sidecar-mismatch"),
        (spoil_dash_branch_on, "sidecar-mismatch"),
    ],
)
def test_a_corrupt_or_contradicting_sidecar_is_refused_and_nothing_is_listed(
    make, repo, spoil, reason
):
    ex = make()
    ex.task()
    ex.s.write()
    spoil(ex)
    ex.s.ledger.write()
    ex.s.side.write(trailing_newline=spoil is not spoil_truncated)
    before = (refs_and_index(repo), work_digest(repo.work))
    out = ex.vcs.run_reconcile(
        str(repo.work), str(ex.s.ledger_path), str(ex.s.side_path),
        str(ex.s.run_dir), None, True,
    )  # fmt: skip
    assert (out["status"], out["reason"], out["boundaries"]) == ("refused", reason, [])
    assert (refs_and_index(repo), work_digest(repo.work)) == before


def test_a_corrupt_ledger_is_refused(make, repo):
    ex = make()
    ex.task()
    ex.s.ledger.add("garbage")
    out = ex.reconcile(True)
    assert (out["status"], out["reason"]) == ("refused", "ledger-corrupt")


def test_reconcile_is_deterministic_and_writes_nothing(make, repo, vcs):
    ex = make(managed=True)
    ex.task()
    ex.attempt(stop_after="staged")
    ex.new_run()
    ex.s.write()
    before = (refs_and_index(repo), work_digest(repo.work))
    first = vcs.emit_text(ex.reconcile())
    second = vcs.emit_text(ex.reconcile())
    assert first == second
    assert (refs_and_index(repo), work_digest(repo.work)) == before


def test_a_settled_boundary_by_resolution_is_settled(make, repo):
    ex = make()
    ex.task()
    ex.attempt(stop_after="committed")
    repo.write("src/z.py", "z\n")
    repo.git("add", "--", "src/z.py")
    repo.git("commit", "-q", "-m", "by hand")
    ex.new_run()
    key = ex.only()["key"]
    ex.s.side.resolved_abandoned("1", key=key)
    ex.new_run()
    assert row(ex.only()) == ("settled", "none", "resolved")


# =============================================================================================
# The retry decision (FR-065, FR-107, FR-116, FR-132)
# =============================================================================================
@MODES
def test_a_product_file_changed_after_review_blocks_the_retry_and_stage_plan_agrees(
    make, repo, managed
):
    ex = make(managed)
    ex.task()
    ex.attempt(stop_after="prepared")
    repo.write("src/a.py", "a lint step rewrote it\n")
    ex.new_run()
    b = ex.only()
    assert row(b) == ("pending", "stop-unsettled", "candidate-changed")
    assert b["paths"] == ["src/a.py"]
    plan = ex.s.plan()
    assert (plan["status"], plan["reason"]) == ("refused", "candidate-changed")
    assert plan["add_argv"] == [] and plan["commit_argv"] == []


def test_a_refused_attempt_at_the_parent_is_retried_only_while_the_product_is_unchanged(
    make, repo
):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="staged")
    ex.s.side.refused("1", key=key, attempt=1, reason="hook-failed")
    ex.new_run()
    assert row(ex.only()) == ("refused", "retry", "retry-allowed")
    repo.write("src/a.py", "changed since\n")
    ex.new_run()
    assert row(ex.only()) == ("refused", "stop-unsettled", "candidate-changed")


def test_a_refused_attempt_whose_head_moved_is_never_retried(make, repo):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="committed")
    ex.s.side.refused("1", key=key, attempt=1, reason="hook-rewrite-committed")
    ex.new_run()
    assert row(ex.only()) == ("refused", "stop-unsettled", "unsettled")


def test_an_unproved_accepted_tree_blocks_the_retry(make, repo):
    ex = make()
    ex.task()
    ex.attempt(stop_after="prepared")
    repo.git("update-ref", "-d", f"{PIN}/plan1/accepted/T1-s1")
    ex.new_run()
    assert row(ex.only()) == ("pending", "stop-unsettled", "no-accepted-tree")


def test_a_hook_rewrite_is_retried_only_after_a_renewed_review_or_ruling(make, repo):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="staged")
    repo.write("src/a.py", "the hook rewrote this\n")
    rewritten = f"{PIN}/plan1/rewritten/{key}-a1"
    repo.git("update-ref", rewritten, private_tree(repo))
    ex.s.side.refused(
        "1", key=key, attempt=1, reason="hook-rewrite", rewritten=rewritten
    )
    ex.new_run()  # a flag typed before the person saw the disclosure is not a review
    b = ex.only()
    assert row(b) == ("refused", "stop-unsettled", "candidate-changed")
    assert b["rewritten"] == rewritten and b["paths"] == ["src/a.py"]
    plan = ex.s.plan()
    assert (plan["status"], plan["reason"]) == ("refused", "candidate-changed")
    ex.s.ledger.ruling("1")  # given after the refusal displayed the rewritten paths
    ex.new_run()
    assert row(ex.only()) == ("refused", "retry", "retry-allowed")
    plan = (
        ex.s.plan()
    )  # stage-plan reads the rewritten tree as the reference, so it agrees
    assert plan["status"] == "ok" and plan["attempt"] == 2, plan
    ex.attempt()
    assert commits_for(repo, key) == 1
    assert repo.git("show", "HEAD:src/a.py") == "the hook rewrote this\n"


def test_a_hook_rewrite_restored_to_the_accepted_tree_needs_no_review(make, repo):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="staged")
    ex.s.side.refused("1", key=key, attempt=1, reason="hook-rewrite")
    ex.new_run()
    assert row(ex.only()) == (
        "refused",
        "retry",
        "retry-allowed",
    )  # product == accepted


def test_a_hook_rewrite_of_evidence_only_is_retried_with_evidence_rebuilt(make, repo):
    ex = make(managed=True)
    ex.task()
    key = ex.attempt(stop_after="staged")
    repo.write(f"{PKG}/artifacts/evidence.md", "rewritten by a formatter\n")
    ex.s.side.refused("1", key=key, attempt=1, reason="hook-rewrite-evidence")
    ex.new_run()
    assert row(ex.only()) == ("refused", "retry", "retry-allowed")
    ex.resume()
    assert commits_for(repo, key) == 1


def test_an_uncertain_result_is_never_retried(make, repo):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="staged")
    ex.s.side.refused("1", key=key, attempt=1, reason="history-differs", uncertain=True)
    ex.new_run()
    assert row(ex.only()) == ("uncertain", "stop-uncertain", "uncertain")


# --- quiescence (FR-116) ---------------------------------------------------------------------------
def test_an_open_attempt_is_not_retried_while_an_index_lock_exists(make, repo):
    ex = make()
    ex.task()
    ex.attempt(stop_after="prepared")
    (repo.work / ".git" / "index.lock").write_text("", encoding="utf-8")
    ex.new_run()
    b = ex.only()
    assert row(b) == ("pending", "stop-unsettled", "index-locked")
    plan = ex.s.plan()
    assert (plan["status"], plan["reason"]) == ("refused", "index-locked")
    os.remove(repo.work / ".git" / "index.lock")
    assert ex.only()["action"] == "retry"


def test_an_open_attempt_is_not_retried_while_a_git_process_may_run(
    make, repo, plan_mod, monkeypatch
):
    ex = make()
    ex.task()
    ex.attempt(stop_after="staged")
    monkeypatch.setattr(plan_mod, "_live_git_processes", lambda top: ["4242"])
    ex.new_run()
    b = ex.only()
    assert row(b) == ("pending", "stop-unsettled", "commit-interrupted")
    monkeypatch.setattr(
        plan_mod, "_live_git_processes", lambda top: None
    )  # cannot look
    assert ex.only()["reason"] == "commit-interrupted"  # unknown is not proof


def test_a_finished_refused_attempt_needs_no_quiescence_proof(
    make, repo, plan_mod, monkeypatch
):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="staged")
    ex.s.side.refused("1", key=key, attempt=1, reason="hook-failed")
    monkeypatch.setattr(plan_mod, "_live_git_processes", lambda top: ["4242"])
    ex.new_run()
    assert ex.only()["action"] == "retry"


@pytest.mark.skipif(not os.path.isdir("/proc"), reason="needs /proc")
def test_the_real_probe_sees_a_git_process_a_hook_and_a_lock(
    repo, plan_mod, hook_emulator, monkeypatch, no_live_git
):
    monkeypatch.setattr(plan_mod, "_live_git_processes", no_live_git)  # the real probe
    git = plan_mod.GitRunner(repo.work)
    assert plan_mod.quiescence(git) == (True, "none-seen")
    idle = (
        subprocess.Popen(  # a git process that stays in the work tree, holding no lock
            ["git", "cat-file", "--batch"],
            cwd=repo.work,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
        )
    )
    try:
        assert plan_mod.quiescence(git) == (False, "git-process-running")
    finally:
        idle.stdin.close()
        idle.wait(timeout=30)
    assert plan_mod.quiescence(git) == (True, "none-seen")
    repo.write("README.md", "changed\n")
    proc = hook_emulator.start_blocked_commit(
        ["README.md"]
    )  # git and its hook, one lock
    try:
        seen = plan_mod._live_git_processes(str(repo.work))
        assert len(seen) >= 2  # the commit and the hook script
        assert plan_mod.quiescence(git) == (False, "index-locked")
    finally:
        hook_emulator.kill_group(proc)
    assert plan_mod._live_git_processes(str(repo.work)) == []
    lock = repo.work / ".git" / "index.lock"  # a killed commit leaves its lock behind
    lock.write_text("", encoding="utf-8")
    assert plan_mod.quiescence(git) == (False, "index-locked")
    lock.unlink()
    assert plan_mod.quiescence(git) == (True, "none-seen")


# --- the verb ---------------------------------------------------------------------------------------
def run_cli(repo, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "vcs.py"), "reconcile", *args],
        cwd=repo.work,
        capture_output=True,
        text=True,
    )


def test_the_cli_prints_one_json_object_and_exits_zero(make, repo):
    ex = make()
    ex.task()
    ex.new_run()
    ex.s.write()
    done = run_cli(
        repo,
        "--ledger", str(ex.s.ledger_path), "--sidecar", str(ex.s.side_path),
        "--run-dir", str(ex.s.run_dir), "--flag", "on",
    )  # fmt: skip
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["verb"], data["status"], data["vcs_contract"]) == (
        "reconcile",
        "ok",
        "1",
    )
    assert data["boundaries"][0]["action"] == "prepare"


@pytest.mark.parametrize(
    "args",
    [
        ["--ledger", "l", "--sidecar", "s", "--run-dir", "d"],  # no --flag
        ["--ledger", "l", "--sidecar", "s", "--run-dir", "d", "--flag", "maybe"],
        ["--sidecar", "s", "--run-dir", "d", "--flag", "on"],  # no --ledger
    ],
)
def test_the_cli_usage_errors_exit_64(repo, args):
    done = run_cli(repo, *args)
    assert done.returncode == 64 and done.stdout == ""


def test_the_cli_a_missing_ledger_is_a_failed_lookup(repo):
    done = run_cli(
        repo,
        "--ledger",
        "nope.md",
        "--sidecar",
        "c.md",
        "--run-dir",
        "d",
        "--flag",
        "on",
    )
    assert done.returncode == 69 and done.stdout == ""
