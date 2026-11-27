"""T-21 owner resolution, read through ``vcs resolve-check`` (FR-120 to FR-126, FR-116,
DD-5; design sections 4.3 and 6.2, AC-18).

``resolve-check`` resolves the key the person typed to one known unsettled boundary, says what
the history shows (``state``, ``parent``, ``head``, ``basis``, ``differs``, ``quiescent``) and
which answers may be recorded: ``abandon`` always, ``adopt`` only when the history allows it.
It writes nothing; the executor appends the one ``resolved`` line, and only after the person's
own reply (the protocol text and its tests, not this helper, enforce that).

Every case runs on a real temporary repository with a real ledger, sidecar, pins and commits.
The same stand-in executor as ``test_crash_points`` plays the commit step, so each unsettled
state is reached by the steps that really leave it.

The quiescence probe (FR-116) is replaced by a stub: a real process list is not a fact these
cases depend on. The index-lock half of the probe is real.
"""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys

import pytest

from .conftest import SCRIPTS, SidecarBuilder
from .test_crash_points import MODES, PKG, Exec, work_digest
from .test_stage_plan import PIN, Scene, refs_and_index


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


@pytest.fixture
def plan_mod(scripts_dir):
    return importlib.import_module("vcs_plan")


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
        if managed:  # untracked, like a package the executor works in
            repo.write(f"{PKG}/plan1.md", "the plan\n")
            repo.write(f"{PKG}/source.md", "the source\n")
        return Exec(Scene(repo, vcs, managed), repo, vcs, managed)

    return build


def resolve(ex, key, **kw):
    ex.s.write()
    return ex.vcs.run_resolve_check(
        str(ex.repo.work),
        key,
        str(ex.s.ledger_path),
        str(ex.s.side_path),
        run_dir=str(ex.s.run_dir),
        package=str(ex.s.pkg) if ex.s.pkg else None,
        **kw,
    )


def first_key(ex):
    return ex.reconcile()["boundaries"][0]["key"]


def by_hand(ex, text="z\n", path="src/z.py"):
    """A person's own commit of ``path`` (the index entries already staged go in too)."""
    ex.repo.write(path, text)
    ex.repo.git("add", "--", path)
    ex.repo.git("commit", "-q", "-m", "by hand")
    return ex.repo.git("rev-parse", "HEAD").strip()


def head_of(repo):
    return repo.git("rev-parse", "HEAD").strip()


# --- the unsettled states, each reached the way a real run reaches it -------------------------
def due(ex):
    ex.task()


def out_of_protocol(ex):
    ex.task()
    ex.s.start("2")  # an old copy ignores the flag and starts the next task


def pending(ex):
    ex.task()
    ex.attempt(stop_after="prepared")


def pending_proved(ex):
    ex.task()
    ex.attempt(stop_after="committed")


def refused(ex):
    ex.task()
    key = ex.attempt(stop_after="staged")
    ex.s.side.refused("1", key=key, attempt=1, reason="hook-failed")


def refused_moved(ex):
    ex.task()
    key = ex.attempt(stop_after="committed")
    ex.s.side.refused("1", key=key, attempt=1, reason="hook-rewrite-committed")


def uncertain(ex):
    ex.task()
    ex.attempt(stop_after="committed")
    by_hand(ex)


UNSETTLED = [
    pytest.param(due, "due", id="due"),
    pytest.param(out_of_protocol, "out-of-protocol", id="out-of-protocol"),
    pytest.param(pending, "pending", id="pending"),
    pytest.param(pending_proved, "pending", id="pending-commit-proved"),
    pytest.param(refused, "refused", id="refused-at-parent"),
    pytest.param(refused_moved, "refused", id="refused-head-moved"),
    pytest.param(uncertain, "uncertain", id="uncertain"),
]


# =============================================================================================
# Every unsettled state offers abandon, flagged and unflagged (FR-121, FR-126)
# =============================================================================================
@MODES
@pytest.mark.parametrize("flag", [True, False], ids=["flagged", "unflagged"])
@pytest.mark.parametrize("build,state", UNSETTLED)
def test_every_unsettled_state_offers_abandon_in_a_flagged_and_an_unflagged_run(
    make, build, state, flag, managed
):
    ex = make(managed)
    build(ex)
    ex.new_run(flag)
    key = first_key(ex)
    out = resolve(ex, key)
    assert (out["status"], out["state"], out["key"]) == ("ok", state, key)
    assert out["choices"][0] == "abandon"
    assert out["members"] and out["label"] and key.startswith(out["label"])


@MODES
def test_the_reported_parent_is_the_prepared_parent_or_the_q0_head(make, repo, managed):
    ex = make(managed)
    base = head_of(repo)
    ex.task()
    ex.new_run()
    key = first_key(ex)
    assert (
        resolve(ex, key)["parent"] == base
    )  # never prepared: the first member's q0-head
    ex.attempt(stop_after="prepared")
    out = resolve(ex, key)
    assert (out["parent"], out["attempt"], out["basis"]) == (base, 1, "candidate")


# =============================================================================================
# adopt: when it is offered, and the disclosed difference (FR-123, FR-124)
# =============================================================================================
@MODES
def test_adopt_is_offered_with_the_candidate_basis_when_a_person_committed_on_top(
    make, repo, managed
):
    ex = make(managed)
    base = head_of(repo)
    ex.task()
    ex.attempt(stop_after="committed")
    hand = by_hand(ex)
    ex.new_run()
    out = resolve(ex, first_key(ex))
    assert out["state"] == "uncertain" and out["reason"] is None
    assert out["choices"] == ["abandon", "adopt"]
    assert (out["basis"], out["differs"], out["quiescent"]) == ("candidate", 0, True)
    assert (out["head"], out["parent"]) == (hand, base)


EDITS = {
    "edit": lambda repo: repo.write("src/a.py", "mine\n"),
    "delete": lambda repo: (repo.work / "src/a.py").unlink(),
    "mode": lambda repo: os.chmod(repo.work / "src/a.py", 0o755),
}


@pytest.mark.parametrize("edit", EDITS)
def test_differs_counts_the_paths_of_s_whose_object_mode_or_presence_differ(
    make, repo, edit
):
    ex = make()
    ex.task()
    ex.attempt(stop_after="staged")  # S is staged: a.py holds the accepted text
    EDITS[edit](repo)
    repo.git("add", "-A", "--", "src/a.py")
    repo.git("commit", "-q", "-m", "the person's own version")
    ex.new_run()
    out = resolve(ex, first_key(ex))
    assert (out["state"], out["basis"], out["differs"]) == ("uncertain", "candidate", 1)
    assert out["choices"] == ["abandon", "adopt"]  # differs is disclosed, not a bar


@pytest.mark.parametrize("text,differs", [("new\n", 0), ("other\n", 1)])
def test_a_due_boundary_compares_with_the_accepted_tree(make, repo, text, differs):
    ex = make()
    ex.task()  # src/a.py is "new\n" in the accepted pin
    base = head_of(repo)
    hand = by_hand(ex, text, "src/a.py")
    ex.new_run()
    out = resolve(ex, first_key(ex))
    assert (out["state"], out["basis"], out["differs"]) == ("due", "accepted", differs)
    assert (out["parent"], out["head"]) == (base, hand)
    assert out["choices"] == ["abandon", "adopt"]


# =============================================================================================
# adopt refusals; abandon stays available (FR-123, FR-126)
# =============================================================================================
def only_abandon(out, reason):
    assert out["status"] == "ok"
    assert (out["reason"], out["choices"]) == (reason, ["abandon"])
    assert out["detail"]


def test_a_missing_candidate_pin_refuses_adopt_but_abandon_stays_available(make, repo):
    ex = make()
    ex.task()
    ex.attempt(stop_after="prepared")  # no candidate pin was ever made
    by_hand(ex)
    ex.new_run()
    out = resolve(ex, first_key(ex))
    only_abandon(out, "adopt-unverifiable")
    assert (out["basis"], out["differs"]) == ("candidate", None)  # unavailable, not 0


def test_a_candidate_pin_deleted_after_the_commit_refuses_adopt(make, repo):
    ex = make()
    ex.task()
    key = ex.attempt(stop_after="committed")
    by_hand(ex)
    repo.git("update-ref", "-d", f"{PIN}/plan1/boundary/{key}-a1")
    ex.new_run()
    only_abandon(resolve(ex, key), "adopt-unverifiable")


def test_a_missing_accepted_pin_refuses_adopt_for_a_due_boundary(make, repo):
    ex = make()
    ex.task()
    by_hand(ex, "new\n", "src/a.py")
    repo.git("update-ref", "-d", f"{PIN}/plan1/accepted/T1-s1")
    ex.new_run()
    out = resolve(ex, first_key(ex))
    only_abandon(out, "adopt-unverifiable")
    assert (out["basis"], out["differs"]) == ("accepted", None)


def test_unrelated_history_refuses_adopt(make, repo):
    ex = make()
    ex.task()
    ex.attempt(stop_after="committed")
    repo.git("checkout", "-q", "--orphan", "elsewhere")
    repo.git("commit", "-q", "-m", "a root commit that shares nothing")
    ex.new_run()
    only_abandon(resolve(ex, first_key(ex)), "adopt-not-descendant")


def test_a_head_that_is_still_the_parent_has_nothing_to_adopt(make):
    ex = make()
    ex.task()
    ex.attempt(stop_after="prepared")
    ex.new_run()
    out = resolve(ex, first_key(ex))
    only_abandon(out, "adopt-not-descendant")
    assert out["head"] == out["parent"]


@pytest.mark.parametrize(
    "recorded", ["0" * 40, None], ids=["parent-not-in-the-repository", "no-q0-head"]
)
def test_an_unknown_parent_is_unverifiable_never_a_success(make, repo, recorded):
    ex = make()
    ex.task()
    by_hand(ex, "new\n", "src/a.py")
    q0 = ex.s.retries / "T1" / "q0-head"
    if recorded is None:
        q0.unlink()
    else:
        q0.write_text(recorded, encoding="utf-8")  # merge-base exits 128 for it
    ex.new_run()
    out = resolve(ex, first_key(ex))
    only_abandon(out, "adopt-unverifiable")
    assert out["parent"] == recorded


def test_adopt_needs_proved_quiescence_and_abandon_does_not_need_it(
    make, repo, plan_mod, monkeypatch
):
    ex = make()
    ex.task()
    ex.attempt(stop_after="committed")
    by_hand(ex)
    ex.new_run()
    key = first_key(ex)
    lock = repo.work / ".git" / "index.lock"
    lock.write_text("", encoding="utf-8")  # a killed commit leaves its lock behind
    locked = resolve(ex, key)
    only_abandon(locked, "adopt-unverifiable")
    assert (locked["quiescent"], locked["quiescence"]) == (False, "index-locked")
    lock.unlink()
    assert resolve(ex, key)["choices"] == ["abandon", "adopt"]
    monkeypatch.setattr(plan_mod, "_live_git_processes", lambda top: ["4242"])
    running = resolve(ex, key)
    only_abandon(running, "adopt-unverifiable")
    assert (running["quiescent"], running["quiescence"]) == (
        False,
        "git-process-running",
    )
    monkeypatch.setattr(plan_mod, "_live_git_processes", lambda top: None)
    unknown = resolve(ex, key)  # a process table that cannot be read is never proof
    only_abandon(unknown, "adopt-unverifiable")
    assert (unknown["quiescent"], unknown["quiescence"]) == (None, "unknown")


def test_a_head_changed_after_the_disclosure_shows_in_the_next_check(make, repo):
    ex = make()
    ex.task()
    ex.attempt(stop_after="committed")
    seen = by_hand(ex)
    ex.new_run()
    key = first_key(ex)
    first = resolve(ex, key)
    assert (first["head"], first["differs"]) == (seen, 0)
    later = by_hand(ex, "edited after the disclosure\n", "src/a.py")
    second = resolve(ex, key)  # the executor compares head and differs and asks again
    assert (second["head"], second["differs"]) == (later, 1) and later != seen
    assert second["choices"] == ["abandon", "adopt"]
    repo.git("checkout", "-q", "--orphan", "elsewhere")
    repo.git("commit", "-q", "-m", "history that shares nothing")
    only_abandon(resolve(ex, key), "adopt-not-descendant")


# =============================================================================================
# Reading the key (FR-122, FR-123)
# =============================================================================================
def test_a_unique_displayed_prefix_resolves_to_the_full_key(make):
    ex = make()
    ex.task()
    ex.new_run()
    key = first_key(ex)
    out = resolve(ex, key[:12])
    assert (out["status"], out["key"]) == ("ok", key)
    assert resolve(ex, key)["key"] == key


def test_a_prefix_shorter_than_the_displayed_label_is_refused_and_says_so(make):
    ex = make()
    ex.task()
    ex.new_run()
    key = first_key(ex)
    for short in (key[:11], ""):
        out = resolve(ex, short)
        assert (out["status"], out["reason"]) == ("refused", "prefix-too-short")
        assert out["choices"] == [] and out["key"] is None


@pytest.mark.parametrize("typed", ["f" * 12, "not-a-hex-key", "z" * 64])
def test_an_unknown_key_is_refused(make, typed):
    ex = make()
    ex.task()
    ex.new_run()
    out = resolve(ex, typed)
    assert (out["status"], out["reason"], out["choices"]) == (
        "refused",
        "unknown-boundary",
        [],
    )


def test_a_prefix_shared_by_two_keys_is_ambiguous(make, plan_mod, monkeypatch):
    ex = make()
    ex.task("1", "src/a.py")
    ex.task("2", "src/b.py")
    ex.new_run()
    # sha-256 never collides on 12 hex characters: give the two boundaries one long prefix
    monkeypatch.setattr(
        plan_mod,
        "boundary_key",
        lambda repo_id, ledger_id, source_id, members: "ab" * 31 + "0" + members[0][0],
    )
    out = resolve(ex, "ab" * 6)
    assert (out["status"], out["reason"], out["choices"]) == (
        "refused",
        "ambiguous-key",
        [],
    )
    assert "2 boundary keys" in out["detail"]
    picked = resolve(ex, "ab" * 31 + "02")  # the full key still selects one
    assert (picked["status"], picked["members"]) == ("ok", ["2"])


def test_a_boundary_with_nothing_to_settle_is_not_an_unsettled_identity(make):
    ex = make()
    ex.s.side = SidecarBuilder(ex.s.side_path).run(
        1, "off", ledger_lines=0, branch="refs/heads/main"
    )
    ex.task()  # completed outside an `on` segment: never committed, never unsettled
    ex.new_run(True)
    out = resolve(ex, first_key(ex))
    assert (out["status"], out["reason"]) == ("refused", "unknown-boundary")
    assert "nothing to settle" in out["detail"]


def test_without_a_sidecar_no_key_is_known_and_nothing_is_created(make):
    ex = make()
    ex.task()
    ex.s.ledger.write()
    assert not ex.s.side_path.exists()
    out = ex.vcs.run_resolve_check(
        str(ex.repo.work),
        "ab" * 6,
        str(ex.s.ledger_path),
        str(ex.s.side_path),
        run_dir=str(ex.s.run_dir),
    )
    assert (out["status"], out["reason"]) == ("refused", "unknown-boundary")
    assert not ex.s.side_path.exists()


# =============================================================================================
# A settled boundary is never settled twice (FR-125; AC-18)
# =============================================================================================
def settle(ex, how, key, head):
    if how == "abandoned":
        ex.s.side.resolved_abandoned("1", key=key)
    elif how == "adopted":
        ex.s.side.resolved_adopted("1", key=key, head=head, basis="candidate")
    elif how == "committed":
        ex.s.side.commit("1", key=key, attempt=1, sha=head)
    else:
        ex.s.side.commit("1", key=key, attempt=1, sha=head, recovered=True)


@MODES
@pytest.mark.parametrize("how", ["abandoned", "adopted", "committed", "recovered"])
def test_after_the_settling_line_both_verbs_report_settled_and_a_second_answer_is_refused(
    make, repo, vcs, how, managed
):
    ex = make(managed)
    ex.task()
    ex.attempt(stop_after="committed")
    hand = by_hand(ex)
    ex.new_run()
    key = first_key(ex)
    # the state a crash after the resolution append and before the cleanup leaves: the
    # line is durable and every pin is still there
    settle(ex, how, key, hand if how == "adopted" else head_of_boundary(repo, hand))
    ex.s.write()
    before = (refs_and_index(repo), work_digest(repo.work))
    outs = [resolve(ex, key) for _ in range(2)]
    for out in outs:
        assert (out["status"], out["reason"], out["state"]) == (
            "refused",
            "already-settled",
            "settled",
        )
        assert out["choices"] == []
    assert vcs.emit_text(outs[0]) == vcs.emit_text(outs[1])
    assert resolve(ex, key[:12])["reason"] == "already-settled"
    (b,) = ex.reconcile()["boundaries"]
    assert (b["state"], b["action"]) == ("settled", "none")
    assert (
        b["reason"]
        == {
            "abandoned": "resolved",
            "adopted": "resolved",
            "committed": "committed",
            "recovered": "recovered",
        }[how]
    )
    assert (refs_and_index(repo), work_digest(repo.work)) == before  # pins survive


def head_of_boundary(repo, hand):
    """The boundary commit: the parent of the person's commit."""
    return repo.git("rev-parse", f"{hand}^").strip()


# =============================================================================================
# Corrupt or contradicting inputs refuse; a malformed line never settles (FR-102, FR-125)
# =============================================================================================
def test_a_corrupt_sidecar_is_refused_not_repaired(make, repo):
    ex = make()
    ex.task()
    ex.new_run()
    ex.s.side.raw("this line matches no form")
    ex.s.write()
    before = ex.s.side_path.read_bytes()
    out = resolve(ex, "ab" * 6)
    assert (out["status"], out["reason"], out["choices"]) == (
        "refused",
        "sidecar-corrupt",
        [],
    )
    assert ex.s.side_path.read_bytes() == before  # nothing was appended or repaired


@pytest.mark.parametrize(
    "line",
    [
        'T1: commit resolved key={short} as=abandoned at=2026-10-02 quote="x"',
        "T1: commit resolved key={key} as=abandoned head={head} basis=candidate "
        'differs=0 at=2026-10-02 quote="x"',
        'T1: commit resolved key={key} as=adopted at=2026-10-02 quote="x"',
        'T1: commit resolved key={key} as=abandoned at=2026-10-02 quote=""',
    ],
    ids=[
        "key-shorter-than-64",
        "adoption-fields-on-an-abandonment",
        "adoption-fields-missing",
        "empty-quote",
    ],
)
def test_a_malformed_resolution_line_is_corrupt_and_never_settles(make, plan_mod, line):
    ex = make()
    ex.task()
    ex.new_run()
    key = first_key(ex)
    text = line.format(key=key, short=key[:40], head="b" * 40)
    with pytest.raises(plan_mod.SidecarCorrupt):
        plan_mod.parse_sidecar(text + "\n")
    ex.s.side.raw(text)
    out = resolve(ex, key)
    assert (out["status"], out["reason"]) == ("refused", "sidecar-corrupt")


def test_a_changed_managed_plan_refuses_before_any_answer(make, repo):
    ex = make(managed=True)
    ex.task()
    ex.new_run()
    key = first_key(ex)
    repo.write(f"{PKG}/plan1.md", "the plan, edited\n")
    out = resolve(ex, key)
    assert (out["status"], out["reason"], out["choices"]) == (
        "refused",
        "plan-changed",
        [],
    )


def test_a_missing_ledger_and_a_foreign_sidecar_are_failed_lookups(make, vcs, tmp_path):
    ex = make()
    ex.task()
    ex.new_run()
    ex.s.write()
    args = (str(ex.repo.work), "ab" * 6)
    with pytest.raises(vcs.LookupFailed):
        vcs.run_resolve_check(
            *args,
            str(tmp_path / "none.md"),
            str(ex.s.side_path),
            run_dir=str(ex.s.run_dir),
        )
    with pytest.raises(vcs.LookupFailed):
        vcs.run_resolve_check(
            *args,
            str(ex.s.ledger_path),
            str(tmp_path / "commits.md"),
            run_dir=str(ex.s.run_dir),
        )


# =============================================================================================
# Read-only, deterministic, and the layout may be left out
# =============================================================================================
@MODES
def test_resolve_check_writes_nothing_and_two_calls_give_the_same_bytes(
    make, repo, vcs, managed
):
    ex = make(managed)
    ex.task()
    ex.attempt(stop_after="committed")
    by_hand(ex)
    ex.new_run()
    key = first_key(ex)
    ex.s.write()
    before = (refs_and_index(repo), work_digest(repo.work))
    first, second = (vcs.emit_text(resolve(ex, key)) for _ in range(2))
    assert first == second
    assert (refs_and_index(repo), work_digest(repo.work)) == before


@MODES
def test_the_layout_is_read_from_the_ledger_and_sidecar_when_not_given(
    make, vcs, managed
):
    ex = make(managed)
    ex.task()
    ex.attempt(stop_after="committed")
    by_hand(ex)
    ex.new_run()
    key = first_key(ex)
    given = resolve(ex, key)
    inferred = vcs.run_resolve_check(
        str(ex.repo.work), key, str(ex.s.ledger_path), str(ex.s.side_path)
    )
    assert given["status"] == "ok"
    assert vcs.emit_text(inferred) == vcs.emit_text(given)


# =============================================================================================
# The verb on the command line
# =============================================================================================
def run_cli(repo, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "vcs.py"), "resolve-check", *args],
        cwd=repo.work,
        capture_output=True,
        text=True,
    )


def test_the_cli_prints_one_json_object_and_exits_zero_even_when_refused(make, repo):
    ex = make()
    ex.task()
    ex.new_run()
    key = first_key(ex)
    paths = ["--ledger", str(ex.s.ledger_path), "--sidecar", str(ex.s.side_path)]
    done = run_cli(repo, "--key", key[:12], *paths, "--run-dir", str(ex.s.run_dir))
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["verb"], data["status"], data["vcs_contract"]) == (
        "resolve-check",
        "ok",
        "1",
    )
    assert data["choices"][0] == "abandon" and data["key"] == key
    done = run_cli(repo, "--key", "f" * 12, *paths)
    assert done.returncode == 0
    assert json.loads(done.stdout)["reason"] == "unknown-boundary"


@pytest.mark.parametrize(
    "args",
    [
        ["--ledger", "l", "--sidecar", "s"],  # no --key
        ["--key", "abc", "--sidecar", "s"],  # no --ledger
        ["--key", "abc", "--ledger", "l"],  # no --sidecar
        ["--key", "abc", "--ledger", "l", "--sidecar", "s", "--bogus"],
    ],
)
def test_the_cli_usage_errors_exit_64(repo, args):
    done = run_cli(repo, *args)
    assert done.returncode == 64 and done.stdout == ""


def test_the_cli_a_missing_ledger_is_a_failed_lookup(repo):
    done = run_cli(
        repo, "--key", "ab" * 6, "--ledger", "nope.md", "--sidecar", "commits.md"
    )
    assert done.returncode == 69 and done.stdout == ""
