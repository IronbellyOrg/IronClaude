"""Task 6: the eight rules, their reasons, and the table. All facts are built by hand;
``decide`` is pure, so no process, folder or network is touched here."""

from __future__ import annotations

import dataclasses
import json

import pytest

NOW = 2_000_000_000.0
DAY = 86400.0


@pytest.fixture
def good(wc):
    """Facts for a worktree that passes every rule."""
    wt = wc.GitWorktree(
        "/w/wts/topic", "/w/main", "a" * 40, "topic", False, False, False, False, False
    )
    facts = wc.WorktreeFacts(
        worktree=wt,
        head="a" * 40,
        origin=wc.OriginInfo("IronbellyOrg", "IronClaude"),
        state=wc.LocalState(),
        last_commit_ts=NOW - 20 * DAY,
        git_file_mtime=NOW - 20 * DAY,
        created_ts=NOW - 30 * DAY,
        size_bytes=3 * 1024 * 1024,
        git_dir="/w/main/.git/worktrees/topic",
    )
    pr = wc.PullRequest(
        9, "MERGED", "a" * 40, "x", "2026-11-01T00:00:00Z", "t", "", (), "topic"
    )
    return wc.RuleInputs(
        facts=facts,
        now=NOW,
        pr_lookup=wc.PrLookup(True, pr),
        landed=wc.Landed("MERGED", "installed copy"),
        after=wc.AfterPr("same", 0),
        issues=wc.IssueFacts((), ()),
        procs=wc.ProcScan(True, ()),
    )


def with_facts(wc, inp, **change):
    return dataclasses.replace(inp, facts=dataclasses.replace(inp.facts, **change))


def with_wt(wc, inp, **change):
    wt = dataclasses.replace(inp.facts.worktree, **change)
    return with_facts(wc, inp, worktree=wt)


def orca(wc, **change):
    base = dict(
        worktree_id="w", selector="id:w", path="/w/wts/topic", branch="b", repo="r",
        last_activity_ms=None, is_pinned=False, live_terminal_count=0, linked_pr_hint=None, comment="",
    )  # fmt: skip
    base.update(change)
    return wc.OrcaWorktree(**base)


def state(wc, **change):
    return dataclasses.replace(wc.LocalState(), **change)


def test_a_worktree_that_passes_everything_is_removable(wc, good):
    d = wc.decide(good)
    assert (d.decision, d.rule, d.reason, d.note) == ("removable", None, "", "")
    assert d.saved_copy == "none needed"


def test_decide_is_pure_and_repeatable(wc, good, never_run_runner):
    assert wc.decide(good) == wc.decide(good)
    assert wc.decide(dataclasses.replace(good, own_folder=True)) == wc.decide(
        dataclasses.replace(good, own_folder=True)
    )
    assert never_run_runner.commands == []


def case(wc, good, name):
    """One worktree that fails only one rule: (inputs, rule number, reason)."""
    s = lambda **c: with_facts(wc, good, state=state(wc, **c))  # noqa: E731
    pr = lambda **c: dataclasses.replace(  # noqa: E731
        good, pr_lookup=wc.PrLookup(True, dataclasses.replace(good.pr_lookup.pr, **c))
    )
    cases = {
        "main": (with_wt(wc, good, is_main=True), 1, "main checkout"),
        "origin-not-ours": (with_facts(wc, good, origin=wc.OriginInfo("Other", "x")), 1, "not our repo"),
        "origin-unknown": (with_facts(wc, good, origin=None), 1, "not our repo"),
        "own-folder": (dataclasses.replace(good, own_folder=True), 1, "this is where the script runs"),
        "locked": (with_wt(wc, good, locked=True), 1, "locked"),
        "missing": (with_facts(wc, good, present=False), 1, "folder missing (reported only)"),
        "guard": (with_wt(wc, good, path="/w/wts/orca-port-x"), 1, "on the name guard (infrastructure folder)"),
        "detached": (with_wt(wc, good, detached=True, branch=None), 1, "detached HEAD"),
        "no-pr": (dataclasses.replace(good, pr_lookup=wc.PrLookup(True, None)), 2, "no pull request"),
        "pr-lookup": (dataclasses.replace(good, pr_lookup=wc.PrLookup(False, None, "boom")), 2, "pull request lookup failed: boom"),
        "pr-open": (pr(state="OPEN"), 2, "pull request #9 is open"),
        "pr-closed": (pr(state="CLOSED"), 2, "pull request #9 closed, not merged"),
        "landed-unknown": (dataclasses.replace(good, landed=wc.Landed("UNKNOWN", "x")), 2, "landed check said UNKNOWN"),
        "landed-missing": (dataclasses.replace(good, landed=None), 2, "landed check said UNKNOWN"),
        "landed-open": (dataclasses.replace(good, landed=wc.Landed("OPEN", "x")), 2, "pull request #9 is open"),
        "after-3": (dataclasses.replace(good, after=wc.AfterPr("ahead", 3)), 3, "3 commits after the pull request"),
        "after-1": (dataclasses.replace(good, after=wc.AfterPr("ahead", 1)), 3, "1 commit after the pull request"),
        "after-unknown": (dataclasses.replace(good, after=wc.AfterPr("unknown", None)), 3, "HEAD is not the pull request's head"),
        "after-missing": (dataclasses.replace(good, after=None), 3, "HEAD is not the pull request's head"),
        "issue-open": (
            dataclasses.replace(good, issues=wc.IssueFacts((wc.Issue("o/r", 21, "OPEN", ("x",)),), ())),
            4, "issue #21 is open",
        ),
        "issue-failed": (
            dataclasses.replace(good, issues=wc.IssueFacts((), ("issue lookup failed: o/r#4",))),
            4, "issue lookup failed: o/r#4",
        ),
        "issue-missing": (dataclasses.replace(good, issues=None), 4, "issue lookup failed"),
        "changed": (s(changed_tracked=["a", "b"]), 5, "2 changed tracked files"),
        "untracked": (s(untracked_outside_dev=["a"]), 5, "1 untracked file outside .dev"),
        "ignored-local": (s(ignored_unknown=[".env", "x.key"]), 5, "ignored local state: .env, x.key"),
        "state-unread": (with_facts(wc, good, state=None), 5, "ignored local state: git status could not be read"),
        "save-failed": (
            dataclasses.replace(with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])), save_state="failed: push refused"),
            5, "saved copy failed: push refused",
        ),
        "save-unset": (with_facts(wc, good, state=state(wc, ignored_dev=[".dev/a"])), 5, "saved copy failed: no save state for the .dev files"),
        "process": (
            dataclasses.replace(good, procs=wc.ProcScan(True, ((412, "/w/wts/topic/sub", "node"),))),
            6, "in use: process 412 (node)",
        ),
        "scan-failed": (dataclasses.replace(good, procs=wc.ProcScan(False, failure="pid 5: boom")), 6, None),
        "no-scan": (dataclasses.replace(good, procs=None), 6, None),
        "nested": (with_facts(wc, good, nested_checkouts=["inner/.git"]), 6, "holds another checkout"),
        "operation": (with_facts(wc, good, operations=["MERGE_HEAD"]), 6, "git operation in progress"),
        "unread-folder": (with_facts(wc, good, failures=["3 folder entries could not be read"]), 6, "in use: the folder or its git folder could not be read in full"),
        "git-dir-unread": (with_facts(wc, good, git_dir=None), 6, "in use: the folder or its git folder could not be read in full"),
        "missing-real": (with_facts(wc, good, present=False, origin=None, head=None, state=None, git_dir=None), 1, "folder missing (reported only)"),
        "created-unknown": (with_facts(wc, good, created_ts=None), 7, "created time unknown (needs 7)"),
        "idle": (with_facts(wc, good, git_file_mtime=NOW - 2 * DAY, last_commit_ts=NOW - 3 * DAY), 7, "idle 2 days (needs 7)"),
        "idle-unknown": (with_facts(wc, good, git_file_mtime=None, last_commit_ts=None), 7, "idle time unknown (needs 7)"),
        "young": (with_facts(wc, good, created_ts=NOW - 3 * DAY), 7, "created 3 days ago (needs 7)"),
        "pinned": (dataclasses.replace(good, orca=orca(wc, is_pinned=True)), 8, "pinned in Orca"),
        "keep-file": (with_facts(wc, good, keep_file=True), 8, "keep file present"),
    }  # fmt: skip
    return cases[name]


CASE_NAMES = [
    "main", "origin-not-ours", "origin-unknown", "own-folder", "locked", "missing", "guard", "detached",
    "no-pr", "pr-lookup", "pr-open", "pr-closed", "landed-unknown", "landed-missing", "landed-open",
    "after-3", "after-1", "after-unknown", "after-missing", "issue-open", "issue-failed", "issue-missing",
    "changed", "untracked", "ignored-local", "state-unread", "save-failed", "save-unset",
    "process", "scan-failed", "no-scan", "nested", "operation", "unread-folder", "git-dir-unread",
    "missing-real", "created-unknown",
    "idle", "idle-unknown", "young", "pinned", "keep-file",
]  # fmt: skip


@pytest.mark.parametrize("name", CASE_NAMES)
def test_failing_only_one_rule_keeps_the_worktree_with_that_reason(wc, good, name):
    inp, rule, reason = case(wc, good, name)
    d = wc.decide(inp)
    assert d.decision == "kept" and d.rule == rule
    if reason is not None:
        assert d.reason == reason
    else:
        assert d.reason.startswith("in use: the process scan failed")


def test_an_unreadable_orca_list_keeps_the_worktree_and_is_a_lookup_failure(wc, good):
    d = wc.decide(dataclasses.replace(good, orca_known=False))
    assert (d.decision, d.rule, d.unread) == ("kept", 8, True)
    assert d.reason == "Orca unavailable, so whether it is pinned is unknown"
    # a worktree that Orca simply does not list, with a readable list, is still fine
    assert (
        wc.decide(dataclasses.replace(good, orca=None, orca_known=True)).decision
        == "removable"
    )


@pytest.mark.parametrize(
    "name",
    [
        "pr-lookup", "landed-unknown", "landed-missing", "after-unknown", "after-missing",
        "issue-failed", "issue-missing", "state-unread", "scan-failed", "no-scan",
        "unread-folder", "git-dir-unread", "idle-unknown", "created-unknown",
    ],
)  # fmt: skip
def test_a_reason_caused_by_an_unreadable_fact_is_flagged_unread(wc, good, name):
    inp, _rule, _reason = case(wc, good, name)
    d = wc.decide(inp)
    assert d.decision == "kept" and d.unread is True, d.reason


@pytest.mark.parametrize(
    "name",
    [
        "main", "origin-not-ours", "own-folder", "locked", "no-pr", "pr-open", "pr-closed",
        "after-3", "issue-open", "changed", "untracked", "ignored-local", "process", "nested",
        "operation", "idle", "young", "pinned", "keep-file",
    ],
)  # fmt: skip
def test_a_plain_verdict_is_not_flagged_unread(wc, good, name):
    inp, _rule, _reason = case(wc, good, name)
    d = wc.decide(inp)
    assert d.decision == "kept" and d.unread is False, d.reason


def test_the_first_failed_rule_is_the_one_shown(wc, good):
    inp = dataclasses.replace(
        with_facts(wc, good, keep_file=True, state=state(wc, changed_tracked=["a"])),
        pr_lookup=wc.PrLookup(True, None),
        own_folder=True,
    )
    d = wc.decide(inp)
    assert (d.rule, d.reason) == (1, "this is where the script runs")
    inp = dataclasses.replace(inp, own_folder=False)
    assert wc.decide(inp).rule == 2
    inp = dataclasses.replace(inp, pr_lookup=good.pr_lookup)
    assert wc.decide(inp).rule == 5


def test_reasons_are_the_strings_of_the_spec(wc):
    """Every reason the spec table names for rules 1 to 8 appears in the rule code."""
    import inspect

    text = (
        inspect.getsource(wc._rule1)
        + inspect.getsource(wc._rule2)
        + inspect.getsource(wc._rule3)
    )
    for words in ("main checkout", "not our repo", "this is where the script runs", "locked",
                  "folder missing (reported only)", "detached HEAD", "no pull request", "is open",
                  "closed, not merged", "landed check said UNKNOWN", "after the pull request",
                  "HEAD is not the pull request's head"):  # fmt: skip
        assert words in text, words
    text = (
        inspect.getsource(wc._rule4)
        + inspect.getsource(wc._rule5)
        + inspect.getsource(wc._rule6)
        + inspect.getsource(wc._rule7)
        + inspect.getsource(wc._rule8)
    )
    for words in ("is open", "issue lookup failed", "changed tracked file", "untracked file", "outside .dev",
                  "ignored local state:", "saved copy failed:", "in use: process", "holds another checkout",
                  "git operation in progress", "(needs", "pinned in Orca", "keep file present"):  # fmt: skip
        assert words in text, words


# -- rule 6: terminals, the save state, the dry run -------------------------------------------------


def test_a_process_inside_with_orca_terminals_open_passes_rule_6_with_the_note(
    wc, good
):
    inside = wc.ProcScan(True, ((7, "/w/wts/topic", "claude"),))
    inp = dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=2))
    d = wc.decide(inp)
    assert (
        d.decision == "removable"
        and d.note == "its Orca terminals will be closed first"
    )
    # the same process without an Orca terminal fails rule 6
    d = wc.decide(
        dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=0))
    )
    assert (d.decision, d.rule, d.reason) == ("kept", 6, "in use: process 7 (claude)")
    d = wc.decide(dataclasses.replace(good, procs=inside, orca=None))
    assert (d.rule, d.reason) == (6, "in use: process 7 (claude)")
    # terminals but no process: still the note
    d = wc.decide(dataclasses.replace(good, orca=orca(wc, live_terminal_count=1)))
    assert d.decision == "removable" and d.note == wc.TERMINALS_NOTE
    # terminals do not excuse another checkout or an operation, or a failed scan
    busy = with_facts(wc, good, operations=["index.lock"])
    assert (
        wc.decide(
            dataclasses.replace(
                busy, procs=inside, orca=orca(wc, live_terminal_count=2)
            )
        ).rule
        == 6
    )
    failed = wc.ProcScan(False, failure="x")
    assert (
        wc.decide(
            dataclasses.replace(
                good, procs=failed, orca=orca(wc, live_terminal_count=2)
            )
        ).rule
        == 6
    )


def test_a_process_in_a_sibling_folder_is_not_inside(wc, good):
    near = wc.ProcScan(True, ((7, "/w/wts/topic-2", "x"),))
    assert wc.decide(dataclasses.replace(good, procs=near)).decision == "removable"


@pytest.mark.parametrize(
    "files,save,decision,cell",
    [
        ({}, "not needed", "removable", "none needed"),
        ({"untracked_dev": [".dev/a"]}, "needed", "removable", "needed"),
        ({"ignored_dev": [".dev/a"]}, "verified", "removable", "saved and checked"),
        ({"untracked_dev": [".dev/a"]}, "failed: copy differs", "kept", "failed"),
    ],
)
def test_dev_files_need_a_verified_save_and_the_dry_run_shows_needed(
    wc, good, files, save, decision, cell
):
    inp = dataclasses.replace(
        with_facts(wc, good, state=state(wc, **files)), save_state=save
    )
    d = wc.decide(inp)
    assert (d.decision, d.saved_copy) == (decision, cell)


def test_a_failed_rule_before_the_save_still_shows_the_saved_copy_cell(wc, good):
    inp = dataclasses.replace(
        with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])),
        pr_lookup=wc.PrLookup(True, None),
        save_state="needed",
    )
    d = wc.decide(inp)
    assert d.rule == 2 and d.saved_copy == "needed"


# -- the table -----------------------------------------------------------------------------------------


def make_rows(wc, good):
    inp_a = dataclasses.replace(good, orca=orca(wc, live_terminal_count=1))
    inp_b = dataclasses.replace(good, own_folder=True)
    rows = [wc.table_row(i, wc.decide(i), "IronClaude") for i in (inp_a, inp_b)]
    return rows


def test_the_markdown_table_has_the_eleven_columns_and_the_json_the_same_rows(wc, good):
    rows = make_rows(wc, good)
    assert len(wc.TABLE_COLUMNS) == 11
    md = wc.render_markdown(rows).splitlines()
    assert (
        md[0]
        == "| repo | folder | branch | in orca | pull request | issues | idle days | size | saved copy | decision | reason |"
    )
    assert md[1] == "|" + "|".join(["---"] * 11) + "|"
    assert len(md) == 2 + len(rows)
    for line, row in zip(md[2:], rows):
        assert line.count(" | ") == 10
        assert row["decision"] in line and row["folder"] in line
    doc = json.loads(wc.render_json(rows))
    assert doc["columns"] == list(wc.TABLE_COLUMNS)
    assert doc["rows"] == rows
    assert all(set(r) == set(wc.TABLE_COLUMNS) for r in doc["rows"])


def test_row_cells_for_a_removable_and_a_kept_worktree(wc, good):
    a, b = make_rows(wc, good)
    assert a == {
        "repo": "IronClaude", "folder": "topic", "branch": "topic", "in_orca": "yes",
        "pull_request": "#9 MERGED", "issues": "none found", "idle_days": "20.0", "size": "3.0 MB",
        "saved_copy": "none needed", "decision": "removable", "reason": "its Orca terminals will be closed first",
    }  # fmt: skip
    assert (
        b["decision"] == "kept"
        and b["reason"] == "this is where the script runs"
        and b["in_orca"] == "no"
    )


def test_row_cells_for_failed_lookups_and_unknowns(wc, good):
    inp = dataclasses.replace(
        with_facts(
            wc,
            good,
            size_bytes=None,
            git_file_mtime=None,
            last_commit_ts=None,
            worktree=dataclasses.replace(
                good.facts.worktree, detached=True, branch=None
            ),
        ),
        pr_lookup=wc.PrLookup(False, None, "x"),
        issues=wc.IssueFacts(
            (wc.Issue("o/r", 4, "CLOSED", ()),), ("issue lookup failed: o/r#5",)
        ),
    )
    row = wc.table_row(inp, wc.decide(inp))
    assert (
        row["pull_request"],
        row["issues"],
        row["idle_days"],
        row["size"],
        row["branch"],
    ) == (
        "lookup failed",
        "#4 CLOSED, lookup failed",
        "?",
        "?",
        "(detached)",
    )
    assert row["repo"] == "main"
    none = dataclasses.replace(inp, pr_lookup=wc.PrLookup(True, None), issues=None)
    assert wc.table_row(none, wc.decide(none))["issues"] == "lookup failed"
    assert wc.table_row(none, wc.decide(none))["pull_request"] == "none"


def test_markdown_cells_never_break_the_table(wc, good):
    row = dict(make_rows(wc, good)[0], reason="a | b\nc")
    line = wc.render_markdown([row]).splitlines()[2]
    assert line.count("|") == 12 and "\n" not in line.strip()
    assert wc.render_markdown([]).count("\n") == 2


@pytest.mark.parametrize(
    "size,text",
    [
        (None, "?"),
        (0, "0 B"),
        (1023, "1023 B"),
        (1536, "1.5 KB"),
        (5 * 1024**3, "5.0 GB"),
        (3000 * 1024**3, "3000.0 GB"),
    ],
)
def test_size_text(wc, size, text):
    assert wc._size_text(size) == text


# --- Task 8: the removal and keep cases, on real throwaway facts ---------------------------------
#
# Each case below builds the facts from a real throwaway worktree (or from fake gh replies for
# the issue places) and changes one thing; the reason text is asserted, not only the decision.

from .conftest import git_in  # noqa: E402
from .test_facts import facts_for, gh_fake, issue_reply, write  # noqa: E402

SLUG = "IronbellyOrg/IronClaude"
NOT_FOUND = (
    1,
    "",
    "GraphQL: Could not resolve to an issue or pull request with the number",
)
OLD = {
    "git_file_mtime": NOW - 20 * DAY,
    "last_commit_ts": NOW - 20 * DAY,
    "created_ts": NOW - 30 * DAY,
}


def real_inputs(wc, runner_cls, repo, name, good, mutate=None, **change):
    """Inputs whose local facts come from a real throwaway worktree made old enough to pass rule 7."""
    path = repo.add_worktree(name)
    if mutate:
        mutate(path)
    _, facts = facts_for(wc, runner_cls, repo, path)
    facts = dataclasses.replace(
        facts, origin=wc.OriginInfo("IronbellyOrg", "IronClaude"), **OLD
    )
    facts = dataclasses.replace(facts, **change)
    return dataclasses.replace(good, facts=facts, after=wc.AfterPr("same", 0))


def test_removable_case_merged_clean_idle_8_days_no_process_no_terminal_issue_closed(
    wc, runner_cls, throwaway_repo, good
):
    inp = real_inputs(
        wc,
        runner_cls,
        throwaway_repo,
        "removable",
        good,
        git_file_mtime=NOW - 8 * DAY,
        last_commit_ts=NOW - 8 * DAY,
    )
    inp = dataclasses.replace(
        inp,
        issues=wc.IssueFacts(
            (wc.Issue("o/r", 5, "CLOSED", ("closing reference",)),), ()
        ),
    )
    d = wc.decide(inp)
    assert (d.decision, d.reason, d.note) == ("removable", "", "")
    row = wc.table_row(inp, d, "IronClaude")
    assert row["issues"] == "#5 CLOSED" and row["idle_days"] == "8.0"


@pytest.mark.parametrize(
    "name",
    ["orca-port-evidence", "orca-recipe-x", "orca-pristine-y", "orca-old-patched"],
)
def test_the_name_guard_keeps_infrastructure_folders(
    wc, runner_cls, throwaway_repo, good, name
):
    d = wc.decide(real_inputs(wc, runner_cls, throwaway_repo, name, good))
    assert (d.decision, d.rule, d.reason) == (
        "kept",
        1,
        "on the name guard (infrastructure folder)",
    )


def test_coder_orca_port_is_not_caught_by_the_name_guard(
    wc, runner_cls, throwaway_repo, good
):
    assert (
        wc.decide(
            real_inputs(wc, runner_cls, throwaway_repo, "coder-orca-port", good)
        ).decision
        == "removable"
    )


def test_a_real_main_checkout_is_kept(wc, runner_cls, throwaway_repo, good):
    _, facts = facts_for(wc, runner_cls, throwaway_repo, throwaway_repo.main)
    facts = dataclasses.replace(facts, origin=wc.OriginInfo("IronbellyOrg", "x"), **OLD)
    d = wc.decide(dataclasses.replace(good, facts=facts))
    assert (d.rule, d.reason) == (1, "main checkout")


def test_a_real_detached_head_and_a_real_locked_worktree_are_kept(
    wc, runner_cls, throwaway_repo, good
):
    wts = throwaway_repo.add_standard_worktrees()
    for name, reason in (("detached", "detached HEAD"), ("locked", "locked")):
        _, facts = facts_for(wc, runner_cls, throwaway_repo, wts[name])
        facts = dataclasses.replace(
            facts, origin=wc.OriginInfo("IronbellyOrg", "x"), **OLD
        )
        d = wc.decide(dataclasses.replace(good, facts=facts))
        assert (d.rule, d.reason) == (1, reason), name


def test_a_folder_that_is_gone_is_reported_and_never_pruned(
    wc, runner_cls, throwaway_repo, good
):
    import shutil

    path = throwaway_repo.add_worktree("vanished")
    shutil.rmtree(path)
    _, facts = facts_for(wc, runner_cls, throwaway_repo, path)
    d = wc.decide(dataclasses.replace(good, facts=facts))
    assert (d.decision, d.rule, d.reason) == (
        "kept",
        1,
        "folder missing (reported only)",
    )


def test_idle_six_days_and_created_three_days_ago(wc, runner_cls, throwaway_repo, good):
    six = real_inputs(
        wc,
        runner_cls,
        throwaway_repo,
        "six",
        good,
        git_file_mtime=NOW - 6 * DAY,
        last_commit_ts=NOW - 6 * DAY,
    )
    assert (wc.decide(six).rule, wc.decide(six).reason) == (7, "idle 6 days (needs 7)")
    young = real_inputs(
        wc, runner_cls, throwaway_repo, "young", good, created_ts=NOW - 3 * DAY
    )
    assert (wc.decide(young).rule, wc.decide(young).reason) == (
        7,
        "created 3 days ago (needs 7)",
    )
    custom = dataclasses.replace(six, idle_floor_days=5)
    assert wc.decide(custom).decision == "removable"


# -- rule 5, on real local state ------------------------------------------------------------------


@pytest.mark.parametrize(
    "mutate,reason",
    [
        (lambda p: write(p / "README.md", "edited\n"), "1 changed tracked file"),
        (lambda p: write(p / "loose.txt"), "1 untracked file outside .dev"),
        (
            lambda p: write(p / ".env", "NAME=placeholder\n"),
            "ignored local state: .env",
        ),
    ],
    ids=["tracked-edit", "untracked-outside-dev", "ignored-env-file"],
)
def test_unsaved_local_state_keeps_the_worktree_with_its_reason(
    wc, runner_cls, throwaway_repo, good, mutate, reason
):
    inp = real_inputs(wc, runner_cls, throwaway_repo, "dirty", good, mutate=mutate)
    d = wc.decide(inp)
    assert (d.decision, d.rule, d.reason) == ("kept", 5, reason)


def test_an_unknown_ignored_name_is_local_state(wc, runner_cls, throwaway_repo, good):
    def mutate(path):
        write(path / ".venv" / "lib" / "x.py")  # build output, allowed
        write(path / ".env", "NAME=placeholder\n")  # unknown, keeps it

    d = wc.decide(
        real_inputs(wc, runner_cls, throwaway_repo, "unknown", good, mutate=mutate)
    )
    assert d.reason == "ignored local state: .env"


def test_ignored_build_output_and_generated_copies_are_not_a_reason_to_keep(
    wc, runner_cls, throwaway_repo, good
):
    names = [
        "pkg/__pycache__/m.pyc", ".venv/lib/x.py", ".codegraph/db", ".ruff_cache/c", ".pytest_cache/c",
        ".mypy_cache/c", "node_modules/p/i.js", "dist/a.whl", "build/b.o", "uv.lock",
        ".serena/cache/c.json", ".claude/agents/a.md", ".claude/commands/c.md",
        ".claude/hooks/h.sh", ".claude/skills/s.md", ".claude/templates/t.md",
    ]  # fmt: skip

    def mutate(path):
        exclude = path.parent.parent / "main" / ".git" / "info" / "exclude"
        with exclude.open("a", encoding="utf-8") as handle:
            handle.write(
                ".codegraph/\n.ruff_cache/\n.pytest_cache/\n.mypy_cache/\nbuild/\nuv.lock\n"
            )
            handle.write(
                ".claude/commands/\n.claude/hooks/\n.claude/skills/\n.claude/templates/\n"
            )
        for rel in names:
            write(path / rel)

    inp = real_inputs(wc, runner_cls, throwaway_repo, "buildout", good, mutate=mutate)
    assert inp.facts.state.ignored_unknown == [], inp.facts.state.ignored_unknown
    assert len(inp.facts.state.ignored_build) + len(
        inp.facts.state.ignored_generated
    ) == len(names)
    assert wc.decide(inp).decision == "removable"


# -- rule 6, on real git operations and a fake process table ---------------------------------------


@pytest.mark.parametrize(
    "marker",
    [
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "rebase-merge",
        "rebase-apply",
        "BISECT_LOG",
        "index.lock",
    ],
)
def test_a_git_operation_in_progress_keeps_the_worktree(
    wc, runner_cls, throwaway_repo, good, marker
):
    from pathlib import Path

    path = throwaway_repo.add_worktree("busy")
    _, probe = facts_for(wc, runner_cls, throwaway_repo, path)
    target = Path(probe.git_dir) / marker
    if marker.startswith("rebase"):
        target.mkdir()
    else:
        write(target, "0" * 40 + "\n")
    clean = real_inputs(
        wc, runner_cls, throwaway_repo, "busy-clean", good
    )  # a clean sibling passes
    assert wc.decide(clean).decision == "removable"
    _, facts = facts_for(wc, runner_cls, throwaway_repo, path)
    facts = dataclasses.replace(facts, origin=wc.OriginInfo("IronbellyOrg", "x"), **OLD)
    d = wc.decide(dataclasses.replace(good, facts=facts))
    assert (d.decision, d.rule, d.reason) == ("kept", 6, "git operation in progress")


def test_a_real_fake_proc_process_inside_and_a_failing_scan(
    wc, runner_cls, throwaway_repo, good, tmp_path
):
    from .conftest import make_fake_proc

    inp = real_inputs(wc, runner_cls, throwaway_repo, "watched", good)
    wt = inp.facts.worktree.path
    inside = wc.scan_processes(str(make_fake_proc(tmp_path / "p1", {77: wt})))
    d = wc.decide(dataclasses.replace(inp, procs=inside))
    assert (d.rule, d.reason) == (6, "in use: process 77 (proc77)")
    bad = wc.scan_processes(str(make_fake_proc(tmp_path / "p2", {78: "file"})))
    d = wc.decide(dataclasses.replace(inp, procs=bad))
    assert d.decision == "kept" and d.rule == 6 and "scan failed" in d.reason
    # every worktree is kept while the scan fails
    other = real_inputs(wc, runner_cls, throwaway_repo, "other", good)
    assert wc.decide(dataclasses.replace(other, procs=bad)).rule == 6


# -- rules 2 and 3: squash merge and a reused branch -----------------------------------------------------


def test_a_squash_merged_pull_request_is_judged_landed_from_its_state(
    wc, runner_cls, throwaway_repo, good
):
    path = throwaway_repo.add_worktree("squashed")
    write(path / "feature.txt")
    git_in(path, "add", "feature.txt")
    git_in(path, "commit", "-q", "-m", "feature")
    head = git_in(path, "rev-parse", "HEAD").strip()
    on_base = git_in(throwaway_repo.main, "branch", "--contains", head).split()
    assert "main" not in on_base  # the commits are not on the base
    pr = dataclasses.replace(good.pr_lookup.pr, head_oid=head)
    runner = runner_cls()
    after = wc.commits_after_pr(runner, str(path), head, head)
    facts = dataclasses.replace(
        facts_for(wc, runner_cls, throwaway_repo, path)[1],
        origin=wc.OriginInfo("IronbellyOrg", "x"),
        **OLD,
    )
    decided = wc.decide(
        dataclasses.replace(
            good, facts=facts, pr_lookup=wc.PrLookup(True, pr), after=after
        )
    )
    assert decided.decision == "removable"
    assert runner.commands == []  # same commit: no ancestry question was asked


def test_a_merged_pull_request_whose_branch_was_reused_keeps_the_worktree(
    wc, runner_cls, throwaway_repo, good
):
    path = throwaway_repo.add_worktree("reused")
    pr_head = git_in(path, "rev-parse", "HEAD").strip()
    write(path / "later.txt")
    git_in(path, "add", "later.txt")
    git_in(path, "commit", "-q", "-m", "new work on the old branch")
    head = git_in(path, "rev-parse", "HEAD").strip()
    after = wc.commits_after_pr(runner_cls(), str(path), head, pr_head)
    facts = dataclasses.replace(
        facts_for(wc, runner_cls, throwaway_repo, path)[1],
        origin=wc.OriginInfo("IronbellyOrg", "x"),
        **OLD,
    )
    d = wc.decide(dataclasses.replace(good, facts=facts, after=after))
    assert (d.decision, d.rule, d.reason) == (
        "kept",
        3,
        "1 commit after the pull request",
    )


# -- rule 4, an open issue through each of the four places -------------------------------------------------


def test_an_open_issue_keeps_the_worktree_through_each_of_the_four_places(
    wc, runner_cls, good
):
    def decided(pr, branch, orca_row, table):
        runner = runner_cls(replies={"gh": gh_fake(wc, table)})
        found = wc.collect_issues(runner, SLUG, pr, branch, "/w/wts/plain", orca_row)
        return wc.decide(dataclasses.replace(good, issues=found))

    base = good.pr_lookup.pr

    def open_issue(n):
        return {
            ("pr", "view", str(n), SLUG): NOT_FOUND,
            ("issue", "view", str(n), SLUG): issue_reply("OPEN"),
        }

    # 1. closing reference
    pr = dataclasses.replace(base, closing=(wc.IssueRef(None, 31),))
    d = decided(pr, "topic", None, {("issue", "view", "31", SLUG): issue_reply("OPEN")})
    assert (d.rule, d.reason) == (4, "issue #31 is open")
    # 2. a #N in the pull request body
    pr = dataclasses.replace(base, body="Fixes #32.")
    assert decided(pr, "topic", None, open_issue(32)).reason == "issue #32 is open"
    # 3. a number in the branch name
    assert (
        decided(base, "docs-333-topic", None, open_issue(333)).reason
        == "issue #333 is open"
    )
    # 4. Orca's card comment
    card = dataclasses.replace(
        wc.parse_orca_worktrees(
            (
                __import__("pathlib").Path(__file__).parent
                / "fixtures"
                / "orca_worktree_ps.json"
            ).read_text()
        ).items[0],
        comment="sc:issue IronbellyOrg/IronClaude#34",
    )
    assert decided(base, "topic", card, open_issue(34)).reason == "issue #34 is open"
    # a closed issue in the same place does not keep it
    closed = {
        ("pr", "view", "34", SLUG): NOT_FOUND,
        ("issue", "view", "34", SLUG): issue_reply("CLOSED"),
    }
    assert decided(base, "topic", card, closed).decision == "removable"


def test_an_issue_lookup_that_fails_keeps_the_worktree(wc, runner_cls, good):
    runner = runner_cls(
        replies={"gh": gh_fake(wc, {("pr", "view", "44", SLUG): NOT_FOUND})}
    )
    pr = dataclasses.replace(good.pr_lookup.pr, body="see #44")
    found = wc.collect_issues(runner, SLUG, pr, "topic", "/w/wts/plain")
    d = wc.decide(dataclasses.replace(good, issues=found))
    assert (d.rule, d.reason) == (4, f"issue lookup failed: {SLUG}#44")


def test_rule_4_none_found_passes_and_the_table_says_so(wc, runner_cls, good):
    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
    found = wc.collect_issues(runner, SLUG, None, "topic", "/w/wts/plain")
    inp = dataclasses.replace(good, issues=found)
    assert wc.decide(inp).decision == "removable"
    assert wc.table_row(inp, wc.decide(inp))["issues"] == "none found"
