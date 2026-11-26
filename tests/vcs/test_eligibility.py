"""Tests for the pure commit-state core of ``vcs_plan`` (DD-8, design section 4.4).

First part (Task 9): the ledger reader. ``parse_ledger`` copies the nine line regexes of
``archive_workspace.py`` (the design's DD-8 lists seven; ``_HEADER`` and ``_ARCH`` are the
recorded override, because a fresh ledger holds only its header line and a managed ledger
can end in ``ARCHIVE: failed``). The parity test loads both files and compares the
pattern strings, so the two readers of one closed grammar cannot drift.

Second part (Task 10): the ``commits.md`` parser, ``ledger_k`` and run segments. Third part
(Task 11): boundary identity, eligibility, batches and the boundary key.
"""

from __future__ import annotations

import importlib
import re
import shutil

import pytest

NINE = (
    "_HEADER",
    "_PLAN",
    "_START",
    "_VERDICT",
    "_RULING",
    "_RETRY",
    "_HALT",
    "_FINAL",
    "_ARCH",
)


@pytest.fixture
def plan(scripts_dir):
    return importlib.import_module("vcs_plan")


def build(ledger_builder, steps):
    """Return the ledger text of a builder after ``steps(builder)`` ran."""
    b = ledger_builder()
    b.header()
    steps(b)
    return b.text()


# --- parity with the archive helper -------------------------------------------------------
@pytest.mark.parametrize("name", NINE)
def test_regex_parity_with_archive_helper(plan, archive_mod, name):
    ours, theirs = getattr(plan, name), getattr(archive_mod, name)
    assert ours.pattern == theirs.pattern
    assert ours.flags == theirs.flags


# --- shapes the reader must accept --------------------------------------------------------
def test_header_only_ledger_parses(plan, ledger_builder):
    view = plan.parse_ledger(build(ledger_builder, lambda b: b))
    assert view.tasks == {}


def test_empty_text_is_an_empty_view(plan):
    assert plan.parse_ledger("").tasks == {}


def test_ledger_ending_in_archive_failed_parses(plan, archive_mod, ledger_builder):
    def steps(b):
        b.plan().start("1").complete("1").final()
        b.archive("failed id=TASK-WF-x-20261001-063000 token=0123456789abcdef reason=x")

    text = build(ledger_builder, steps)
    # the archive helper accepts the same text, so the two readers agree
    path = ledger_builder().path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    archive_mod._parse_ledger(path)
    view = plan.parse_ledger(text)
    assert list(view.tasks) == ["1"]
    assert view.tasks["1"][0].anchor_line_no == 4


def test_unknown_last_line_is_corrupt(plan, ledger_builder):
    text = build(ledger_builder, lambda b: b.start("1").add("Task 1: done"))
    with pytest.raises(plan.LedgerCorrupt):
        plan.parse_ledger(text)


def test_truncated_last_line_is_corrupt(plan, ledger_builder):
    text = build(ledger_builder, lambda b: b.start("1").complete("1"))
    with pytest.raises(plan.LedgerCorrupt):
        plan.parse_ledger(text[: -len("files=src/foo.py\n")])


def test_unterminated_but_complete_last_line_parses(plan, ledger_builder):
    text = build(ledger_builder, lambda b: b.start("1").complete("1"))
    view = plan.parse_ledger(text.rstrip("\n"))
    assert view.tasks["1"][0].anchor_line_no == 3


# --- generations ---------------------------------------------------------------------------
def test_generation_fields(plan, ledger_builder):
    def steps(b):
        b.plan().start("1", sha="a" * 40).complete("1", files="src/a b.py,docs/x.md")

    gen = plan.parse_ledger(build(ledger_builder, steps)).tasks["1"][0]
    assert gen.start_ordinal == 1
    assert gen.start_sha == "a" * 40
    assert gen.start_line_no == 3
    assert gen.anchor_line_no == 4
    assert gen.verdict == "compliant"
    assert gen.files == ["src/a b.py", "docs/x.md"]


def test_start_without_complete_has_no_anchor(plan, ledger_builder):
    gen = plan.parse_ledger(build(ledger_builder, lambda b: b.start("1"))).tasks["1"][0]
    assert (gen.anchor_line_no, gen.verdict, gen.files) == (None, None, [])


def test_nogit_start_sha(plan, ledger_builder):
    gen = plan.parse_ledger(
        build(ledger_builder, lambda b: b.start("1", sha="nogit"))
    ).tasks["1"][0]
    assert gen.start_sha == "nogit"


def test_rereview_complete_does_not_add_a_generation_or_move_the_anchor(
    plan, ledger_builder
):
    def steps(b):
        b.start("1").complete("1", files="src/a.py").final("issues")
        b.complete("1", files="src/other.py")  # re-review line after FINAL

    gens = plan.parse_ledger(build(ledger_builder, steps)).tasks["1"]
    assert len(gens) == 1
    assert gens[0].anchor_line_no == 3
    assert gens[0].files == ["src/a.py"]


def test_restart_after_halt_creates_the_next_generation(plan, ledger_builder):
    def steps(b):
        b.start("1").blocked("1").retry_open("1", 3).retry_revert("1", 3)
        b.retry_review("1", 3).halt("1", 2, "budget")
        b.start("1", sha="b" * 40).complete("1", files="src/b.py")

    gens = plan.parse_ledger(build(ledger_builder, steps)).tasks["1"]
    assert [g.start_ordinal for g in gens] == [1, 2]
    assert gens[0].anchor_line_no is None
    assert gens[0].files == []
    assert gens[1].start_sha == "b" * 40
    assert gens[1].start_line_no == 8
    assert gens[1].anchor_line_no == 9
    assert gens[1].files == ["src/b.py"]


def test_tasks_keep_source_order_and_are_separate(plan, ledger_builder):
    def steps(b):
        b.start("2").start("1").complete("2").complete("1")

    view = plan.parse_ledger(build(ledger_builder, steps))
    assert list(view.tasks) == ["2", "1"]
    assert view.tasks["2"][0].anchor_line_no == 4
    assert view.tasks["1"][0].anchor_line_no == 5


def test_noncompliant_complete_needs_a_ruling_to_anchor(plan, ledger_builder):
    def steps(b):
        b.start("1").blocked("1", "missing").complete("1", "missing")

    gen = plan.parse_ledger(build(ledger_builder, steps)).tasks["1"][0]
    assert gen.anchor_line_no is None  # no Ruling: not a valid complete

    def ruled(b):
        b.start("1").blocked("1", "missing").ruling("1").complete("1", "missing")

    gen = plan.parse_ledger(build(ledger_builder, ruled)).tasks["1"][0]
    assert (gen.anchor_line_no, gen.verdict) == (5, "missing")


def test_ruling_before_a_later_blocked_does_not_authorize(plan, ledger_builder):
    def steps(b):
        b.start("1").blocked("1", "missing").ruling("1").blocked("1", "extra")
        b.complete("1", "extra")

    gen = plan.parse_ledger(build(ledger_builder, steps)).tasks["1"][0]
    assert gen.anchor_line_no is None


# =============================================================================================
# Second part (Task 10): the commits.md parser, ledger_k and run segments (FR-100..FR-102,
# FR-120). The line forms are hand-copied from the requirements, not from the parser.
# =============================================================================================
KEY = "a" * 64
HEAD = "b" * 40


def sidecar_text(sidecar_builder, steps, trailing_newline=True):
    steps(sidecar_builder)
    sidecar_builder.write(trailing_newline=trailing_newline)
    return sidecar_builder.path.read_text(encoding="utf-8")


def runs_of(plan, sidecar_builder, *ks, mode="on"):
    for n, k in enumerate(ks, 1):
        sidecar_builder.run(n, mode, ledger_lines=k)
    sidecar_builder.write()
    return plan.parse_sidecar(sidecar_builder.path.read_text(encoding="utf-8")).runs


# --- the regex table -----------------------------------------------------------------------
def test_resolved_regexes_equal_the_text_of_fr_120(plan):
    abandoned = (
        r"^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=abandoned "
        r'at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$'
    )
    adopted = (
        r"^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=adopted "
        r"head=[0-9a-f]{40} basis=(candidate|accepted) differs=[0-9]+ "
        r'at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$'
    )
    assert plan.SIDECAR_FORMS["resolved_abandoned"].pattern == abandoned
    assert plan.SIDECAR_FORMS["resolved_adopted"].pattern == adopted


def test_one_table_holds_every_line_form(plan):
    assert set(plan.SIDECAR_FORMS) == {
        "run",
        "prepared",
        "commit",
        "skipped",
        "refused",
        "resolved_abandoned",
        "resolved_adopted",
    }


# --- every line form parses and round-trips ------------------------------------------------
def test_run_line_round_trip(plan, sidecar_builder):
    def steps(b):
        b.run(
            1,
            "on",
            ledger_lines=3,
            args="--commit-tasks --depth deep",
            source="inline:0a1b2c3d",
        )
        b.run(2, "off", ledger_lines=9, branch="-", revoked=True, worktree="wt-9")

    runs = plan.parse_sidecar(sidecar_text(sidecar_builder, steps)).runs
    one, two = runs
    assert (one.run, one.flag, one.revoked, one.ledger_lines) == (1, "on", False, 3)
    assert one.branch == "refs/heads/feature/x"
    assert one.at == "2026-10-01T06:30:00Z"
    assert one.args == "--commit-tasks --depth deep"
    assert one.source == "inline:0a1b2c3d"
    assert one.worktree == "wt1"
    assert (two.run, two.flag, two.revoked, two.branch) == (2, "off", True, "-")
    assert two.worktree == "wt-9"


def test_prepared_round_trip(plan, sidecar_builder):
    def steps(b):
        b.prepared(
            "1,2", key=KEY, attempt=3, parent=HEAD, paths="c" * 64,
            accepted="refs/x/a,refs/x/b", plan="d" * 64, source="e" * 64,
        )  # fmt: skip

    sc = plan.parse_sidecar(sidecar_text(sidecar_builder, steps))
    (att,) = sc.attempts[KEY]
    assert att.ids == "1,2"
    assert (att.attempt, att.parent, att.paths) == (3, HEAD, "c" * 64)
    assert att.branch == "refs/heads/feature/x"
    assert att.accepted == ["refs/x/a", "refs/x/b"]
    assert (att.plan, att.source) == ("d" * 64, "e" * 64)


def test_prepared_with_dash_hashes(plan, sidecar_builder):
    sc = plan.parse_sidecar(
        sidecar_text(sidecar_builder, lambda b: b.prepared("1", key=KEY))
    )
    assert (sc.attempts[KEY][0].plan, sc.attempts[KEY][0].source) == ("-", "-")


def test_commit_sha_and_recovered_round_trip(plan, sidecar_builder):
    def steps(b):
        b.prepared("1", key=KEY, attempt=1)
        b.commit("1", key=KEY, attempt=1, sha=HEAD, outside_changed=2, wt="refs/x/wt")

    term = plan.parse_sidecar(sidecar_text(sidecar_builder, steps)).terminal[KEY]
    assert (term.kind, term.sha, term.attempt) == ("sha", HEAD, 1)
    assert (term.outside_changed, term.wt) == (2, "refs/x/wt")

    sidecar_builder.lines.clear()
    sidecar_builder.commit("1", key=KEY, attempt=2, sha=HEAD, recovered=True)
    sidecar_builder.write()
    term = plan.parse_sidecar(
        sidecar_builder.path.read_text(encoding="utf-8")
    ).terminal[KEY]
    assert (term.kind, term.outside_changed, term.wt) == ("recovered", None, None)


def test_skipped_round_trip(plan, sidecar_builder):
    sc = plan.parse_sidecar(
        sidecar_text(
            sidecar_builder,
            lambda b: b.skipped("1", key=KEY, reason="mixed-authorization"),
        )
    )
    assert (sc.terminal[KEY].kind, sc.terminal[KEY].reason) == (
        "skipped",
        "mixed-authorization",
    )


def test_refused_and_uncertain_round_trip(plan, sidecar_builder):
    def steps(b):
        b.refused("1", key=KEY, attempt=1, reason="hook-failed")
        b.refused(
            "1",
            key="f" * 64,
            attempt=2,
            reason="hook-rewrite",
            rewritten="refs/x/rw",
            uncertain=True,
        )

    sc = plan.parse_sidecar(sidecar_text(sidecar_builder, steps))
    assert (sc.terminal[KEY].kind, sc.terminal[KEY].reason) == (
        "refused",
        "hook-failed",
    )
    other = sc.terminal["f" * 64]
    assert (other.kind, other.attempt, other.rewritten) == ("uncertain", 2, "refs/x/rw")


def test_resolved_round_trip(plan, sidecar_builder):
    def steps(b):
        b.resolved_abandoned("1", key=KEY, quote='say "no" \\ ok')
        b.resolved_adopted(
            "2", key="f" * 64, head=HEAD, basis="accepted", differs=4, quote="adopt"
        )

    sc = plan.parse_sidecar(sidecar_text(sidecar_builder, steps))
    gone = sc.resolved[KEY]
    assert (gone.as_, gone.head, gone.basis, gone.differs) == (
        "abandoned",
        None,
        None,
        None,
    )
    assert gone.quote == 'say "no" \\ ok'  # decoded
    took = sc.resolved["f" * 64]
    assert (took.as_, took.head, took.basis, took.differs) == (
        "adopted",
        HEAD,
        "accepted",
        4,
    )
    assert took.at == "2026-10-02"


def test_later_terminal_line_replaces_an_earlier_one(plan, sidecar_builder):
    def steps(b):
        b.prepared("1", key=KEY, attempt=1)
        b.refused("1", key=KEY, attempt=1)
        b.prepared("1", key=KEY, attempt=2)
        b.commit("1", key=KEY, attempt=2)

    sc = plan.parse_sidecar(sidecar_text(sidecar_builder, steps))
    assert [a.attempt for a in sc.attempts[KEY]] == [1, 2]
    assert sc.terminal[KEY].kind == "sha"


def test_empty_sidecar_is_empty(plan):
    sc = plan.parse_sidecar("")
    assert (sc.runs, sc.attempts, sc.terminal, sc.resolved) == ([], {}, {}, {})


# --- corrupt sidecars are refused, never repaired -------------------------------------------
@pytest.mark.parametrize(
    "line",
    [
        "not a form",
        "",
        "run 1: commit-tasks=maybe ledger-lines=0 branch=refs/heads/x at=2026-10-01T06:30:00Z"
        ' args="" source=./p.md worktree=w',
        f"T1: commit sha={'a' * 39} key={KEY} attempt=1",  # 39-hex sha
        f"T1: commit sha={HEAD} key={'a' * 12} attempt=1",  # 12-hex key
        f"T1: commit skipped key={KEY} reason=other",
        f"T1: commit prepared key={KEY} attempt=1",  # missing fields
    ],
)
def test_unknown_or_malformed_line_is_corrupt(plan, sidecar_builder, line):
    sidecar_builder.run(1, "on", ledger_lines=2)
    sidecar_builder.raw(line)
    with pytest.raises(plan.SidecarCorrupt) as info:
        plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b))
    assert info.value.reason == "sidecar-corrupt"


def test_half_written_last_line_is_corrupt(plan, sidecar_builder):
    sidecar_builder.run(1, "on", ledger_lines=2)
    sidecar_builder.skipped("1", key=KEY)
    text = sidecar_text(sidecar_builder, lambda b: b)
    with pytest.raises(plan.SidecarCorrupt):
        plan.parse_sidecar(text[: -len("ty\n")])  # cut inside the reason token


def test_unterminated_last_line_is_corrupt_even_if_it_parses(plan, sidecar_builder):
    # a cut at a token boundary can still parse (attempt=1 from attempt=12); only the
    # missing newline shows the truncation
    sidecar_builder.run(1, "on", ledger_lines=2)
    text = sidecar_text(sidecar_builder, lambda b: b)
    with pytest.raises(plan.SidecarCorrupt):
        plan.parse_sidecar(text.rstrip("\n"))


@pytest.mark.parametrize(
    "quote", ["", "x" * 201, "a\tb", "a\x00b"], ids=["empty", "too-long", "tab", "nul"]
)
def test_resolved_quote_limits(plan, sidecar_builder, quote):
    sidecar_builder.resolved_abandoned("1", key=KEY, quote=quote)
    with pytest.raises(plan.SidecarCorrupt):
        plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b))


def test_resolved_quote_of_200_code_points_is_accepted(plan, sidecar_builder):
    sidecar_builder.resolved_abandoned("1", key=KEY, quote="é" * 200)
    sc = plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b))
    assert len(sc.resolved[KEY].quote) == 200


def test_adoption_fields_on_an_abandoned_line_are_rejected(plan, sidecar_builder):
    sidecar_builder.raw(
        f"T1: commit resolved key={KEY} as=abandoned head={HEAD} basis=candidate differs=0"
        ' at=2026-10-02 quote="x"'
    )
    with pytest.raises(plan.SidecarCorrupt):
        plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b))


@pytest.mark.parametrize("missing", ["head", "basis", "differs"])
def test_adopted_line_without_a_required_field_is_rejected(
    plan, sidecar_builder, missing
):
    fields = {
        "head": f"head={HEAD}",
        "basis": "basis=candidate",
        "differs": "differs=0",
    }
    kept = " ".join(v for k, v in fields.items() if k != missing)
    sidecar_builder.raw(
        f'T1: commit resolved key={KEY} as=adopted {kept} at=2026-10-02 quote="x"'
    )
    with pytest.raises(plan.SidecarCorrupt):
        plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b))


# --- branch=- and revoked bindings ---------------------------------------------------------
def test_dash_branch_is_valid_only_on_an_off_run_line(plan, sidecar_builder):
    sidecar_builder.run(1, "on", ledger_lines=2, branch="-")
    with pytest.raises(plan.SidecarMismatch) as info:
        plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b))
    assert info.value.reason == "sidecar-mismatch"


def test_revoked_reason_is_valid_only_on_an_off_run_line(plan, sidecar_builder):
    sidecar_builder.run(1, "on", ledger_lines=2, revoked=True)
    with pytest.raises(plan.SidecarMismatch):
        plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b))


# --- ledger_k ------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "text,expected",
    [("", 0), ("a\n", 1), ("a\nb\n", 2), ("a\nb", 2), ("a", 1), ("a\n\n", 2)],
)
def test_ledger_k_counts_newlines_plus_an_unterminated_tail(plan, text, expected):
    assert plan.ledger_k(text) == expected


def test_ledger_k_agrees_with_the_ledger_reader_line_count(plan, ledger_builder):
    text = build(ledger_builder, lambda b: b.start("1").complete("1"))
    assert plan.ledger_k(text) == plan.parse_ledger(text).line_count == 3
    assert (
        plan.ledger_k(text.rstrip("\n"))
        == plan.parse_ledger(text.rstrip("\n")).line_count
        == 3
    )


# --- segment_of ----------------------------------------------------------------------------
def test_positions_at_or_before_the_first_offset_have_no_grant(plan, sidecar_builder):
    runs = runs_of(plan, sidecar_builder, 3)
    assert [plan.segment_of(p, runs) for p in (1, 2, 3)] == [None, None, None]
    assert plan.segment_of(4, runs).run == 1


def test_line_belongs_to_the_last_run_line_with_a_smaller_offset(plan, sidecar_builder):
    runs = runs_of(plan, sidecar_builder, 2, 5, 9)
    assert [plan.segment_of(p, runs).run for p in (3, 5, 6, 9, 10)] == [1, 1, 2, 2, 3]


def test_equal_offsets_resolve_by_sidecar_order(plan, sidecar_builder):
    runs = runs_of(plan, sidecar_builder, 3, 3, 3)
    assert plan.segment_of(3, runs) is None
    assert plan.segment_of(4, runs).run == 3  # the last of the equal offsets wins


def test_off_segment_run_is_returned_like_any_other(plan, sidecar_builder):
    sidecar_builder.run(1, "on", ledger_lines=2)
    sidecar_builder.run(2, "off", ledger_lines=4, branch="-")
    runs = plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b)).runs
    assert plan.segment_of(4, runs).flag == "on"
    assert plan.segment_of(5, runs).flag == "off"


def test_unterminated_parseable_last_ledger_line_is_counted_in_the_earlier_segment(
    plan, ledger_builder, sidecar_builder
):
    ledger = build(ledger_builder, lambda b: b.start("1").complete("1")).rstrip("\n")
    k = plan.ledger_k(ledger)  # 3: the unterminated line 3 is counted
    assert k == 3
    sidecar_builder.run(1, "on", ledger_lines=2)
    sidecar_builder.run(2, "on", ledger_lines=k)  # appended after line 3 was written
    runs = plan.parse_sidecar(sidecar_text(sidecar_builder, lambda b: b)).runs
    assert plan.segment_of(3, runs).run == 1
    assert plan.segment_of(4, runs).run == 2


# --- validate_runs: decreasing and out-of-range offsets ------------------------------------
def test_validate_runs_accepts_equal_and_growing_offsets(
    plan, ledger_builder, sidecar_builder
):
    ledger = build(ledger_builder, lambda b: b.start("1").complete("1"))
    runs = runs_of(plan, sidecar_builder, 0, 2, 2, 3)
    plan.validate_runs(runs, ledger)


def test_decreasing_offsets_are_a_mismatch(plan, ledger_builder, sidecar_builder):
    ledger = build(ledger_builder, lambda b: b.start("1").complete("1"))
    runs = runs_of(plan, sidecar_builder, 3, 2)
    with pytest.raises(plan.SidecarMismatch) as info:
        plan.validate_runs(runs, ledger)
    assert info.value.reason == "sidecar-mismatch"


def test_offset_beyond_the_current_ledger_is_a_mismatch(
    plan, ledger_builder, sidecar_builder
):
    ledger = build(ledger_builder, lambda b: b.start("1").complete("1"))  # k == 3
    runs = runs_of(plan, sidecar_builder, 2, 4)
    with pytest.raises(plan.SidecarMismatch):
        plan.validate_runs(runs, ledger)


# =============================================================================================
# Third part (Task 11): boundary identity (FR-058, FR-103, DD-1). A boundary is the original
# overlapping start-to-first-verdict window set; its key is a SHA-256 over a canonical tuple.
# Ledger lines: header is line 1 and ``plan()`` is line 2, so the first ``start`` is line 3.
# =============================================================================================
REPO_ID = "repo:wt1"
LEDGER_ID = "managed:TASK-WF-x-20261001-063000"
SOURCE_ID = "e" * 64


def boundaries_of(
    plan,
    ledger_builder,
    sidecar_builder,
    steps,
    runs=(("on", 0),),
    ledger_id=LEDGER_ID,
):
    """Build the boundaries of a ledger; ``runs`` is a list of ``(mode, offset)``."""
    text = build(ledger_builder, steps)
    for n, (mode, k) in enumerate(runs, 1):
        sidecar_builder.run(n, mode, ledger_lines=k)
    sidecar_builder.write()
    side = plan.parse_sidecar(sidecar_builder.path.read_text(encoding="utf-8"))
    return plan.build_boundaries(
        plan.parse_ledger(text), side.runs, REPO_ID, ledger_id, SOURCE_ID
    )


def test_sequential_tasks_give_one_boundary_each(plan, ledger_builder, sidecar_builder):
    def steps(b):
        b.plan().start("1").complete("1").start("2").complete("2")

    one, two = boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    assert (one.members, one.anchors, one.eligible) == (["1"], [4], True)
    assert (two.members, two.anchors, two.eligible) == (["2"], [6], True)
    assert one.key != two.key


def test_a_three_member_batch_is_one_boundary_listing_every_member(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").start("2").start("3")
        b.complete("3").complete("1").complete("2")

    (only,) = boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    assert only.members == ["1", "2", "3"]  # start order, not completion order
    assert only.anchors == [7, 8, 6]
    assert (only.complete, only.eligible, only.mixed) == (True, True, False)


def test_a_batch_with_members_in_mixed_segments_is_not_eligible(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").start("2").complete("1").complete("2")  # anchors 5 and 6

    (only,) = boundaries_of(
        plan, ledger_builder, sidecar_builder, steps, runs=(("on", 0), ("off", 5))
    )
    assert only.on == [True, False]
    assert (only.complete, only.eligible, only.mixed) == (True, False, True)


@pytest.mark.parametrize(
    "runs",
    [(), (("off", 0),), (("on", 9),)],
    ids=["no-sidecar", "off-segment", "feature-started-later"],
)
def test_a_task_completed_outside_an_on_segment_is_never_eligible(
    plan, ledger_builder, sidecar_builder, runs
):
    def steps(b):
        b.plan().start("1").complete("1")

    (only,) = boundaries_of(plan, ledger_builder, sidecar_builder, steps, runs=runs)
    assert only.on == [False]
    assert (only.complete, only.eligible, only.mixed) == (True, False, False)


def test_a_later_on_segment_does_not_re_authorize_an_earlier_completion(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").complete("1").final("issues")
        b.complete("1")  # re-review line after FINAL, inside the later on segment

    (only,) = boundaries_of(
        plan, ledger_builder, sidecar_builder, steps, runs=(("off", 0), ("on", 4))
    )
    assert only.anchors == [4]
    assert only.eligible is False


def test_a_batch_with_an_unfinished_member_is_not_complete(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").start("2").complete("1")

    (only,) = boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    assert only.members == ["1", "2"]
    assert only.anchors == [5, None]
    assert (only.complete, only.eligible, only.mixed) == (False, False, False)


def test_membership_does_not_change_when_a_halted_member_completes_on_resume(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").start("2").blocked("1").halt("1", 2, "batch")
        b.complete("2")
        b.complete("1")  # resume: a fresh operator review of the same generation
        b.start("3").complete("3")

    first, second = boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    assert first.members == ["1", "2"]
    assert first.anchors == [8, 7]
    assert (first.complete, first.eligible) == (True, True)
    assert second.members == ["3"]


def test_a_crashed_generation_does_not_swallow_the_tasks_after_its_restart(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1")  # crash: no verdict
        b.start("1").complete("1")  # restart
        b.start("2").complete("2")

    first, second, third = boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    assert [(x.members, x.complete) for x in (first, second, third)] == [
        (["1"], False),
        (["1"], True),
        (["2"], True),
    ]
    assert len({first.key, second.key, third.key}) == 3


def test_boundaries_are_listed_in_start_order(plan, ledger_builder, sidecar_builder):
    def steps(b):
        b.plan().start("2").complete("2").start("1").complete("1")

    got = boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    assert [x.members for x in got] == [["2"], ["1"]]


# --- the key -------------------------------------------------------------------------------
def test_key_is_64_lowercase_hex_and_deterministic(plan):
    members = [("1", 1, "a" * 40), ("2", 1, "b" * 40)]
    key = plan.boundary_key(REPO_ID, LEDGER_ID, SOURCE_ID, members)
    assert re.fullmatch(r"[0-9a-f]{64}", key)
    assert key == plan.boundary_key(REPO_ID, LEDGER_ID, SOURCE_ID, list(members))


@pytest.mark.parametrize(
    "change",
    [
        {"repo_id": "repo:other"},
        {"ledger_id": "legacy:TASK-WF-x-20261001-063000"},
        {"ledger_id": "managed:TASK-WF-y-20261001-063000"},
        {"source_id": "f" * 64},
        {"members": [("2", 1, "a" * 40)]},  # task id
        {"members": [("1", 2, "a" * 40)]},  # start ordinal
        {"members": [("1", 1, "c" * 40)]},  # start sha
        {"members": [("1", 1, "a" * 40), ("2", 1, "b" * 40)]},  # one more member
    ],
    ids=[
        "repo",
        "ledger-kind",
        "ledger-slug",
        "source",
        "id",
        "ordinal",
        "sha",
        "more",
    ],
)
def test_every_part_of_the_tuple_changes_the_key(plan, change):
    base = {
        "repo_id": REPO_ID,
        "ledger_id": LEDGER_ID,
        "source_id": SOURCE_ID,
        "members": [("1", 1, "a" * 40)],
    }
    assert plan.boundary_key(**base) != plan.boundary_key(**{**base, **change})


def test_member_order_is_part_of_the_key(plan):
    one, two = ("1", 1, "a" * 40), ("2", 1, "b" * 40)
    args = (REPO_ID, LEDGER_ID, SOURCE_ID)
    assert plan.boundary_key(*args, [one, two]) != plan.boundary_key(*args, [two, one])


def test_key_survives_a_managed_package_moving_to_done(
    plan, ledger_builder, sidecar_builder, tmp_path
):
    todo = tmp_path / "to-do" / "TASK-WF-x-20261001-063000"
    ledger = ledger_builder(todo / "progress.md")
    ledger.header().plan().start("1").complete("1").write()
    slug = todo.name

    def keys():
        folder = ledger.path.parent
        view = plan.parse_ledger((folder / "progress.md").read_text(encoding="utf-8"))
        ident = plan.ledger_identity("managed", slug)  # the slug, never the folder
        return [b.key for b in plan.build_boundaries(view, [], REPO_ID, ident, "s")]

    before = keys()
    done = tmp_path / "done"
    done.mkdir()
    shutil.move(str(todo), str(done / todo.name))
    ledger.path = done / todo.name / "progress.md"
    assert keys() == before


def test_ledger_identity_is_a_token_never_a_path(plan):
    assert plan.ledger_identity("managed", "TASK-WF-x-20261001-063000") == (
        "managed:TASK-WF-x-20261001-063000"
    )
    assert plan.ledger_identity("legacy", "my-prompt-0a1b2c3d") == (
        "legacy:my-prompt-0a1b2c3d"
    )
    for kind, slug in [
        ("other", "x"),
        ("managed", ""),
        ("managed", "a/b"),
        ("legacy", "../x"),
    ]:
        with pytest.raises(ValueError):
            plan.ledger_identity(kind, slug)


def test_boundaries_refuse_a_path_as_the_ledger_identity(
    plan, ledger_builder, sidecar_builder
):
    with pytest.raises(ValueError):
        boundaries_of(
            plan,
            ledger_builder,
            sidecar_builder,
            lambda b: b.plan().start("1").complete("1"),
            ledger_id=".dev/tasks/to-do/x/progress.md",
        )


def test_same_task_in_two_generations_gets_different_keys(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").blocked("1").halt("1", 2, "budget")
        b.start("1").complete("1")  # same task id, same start sha, next ordinal

    first, second = boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    assert first.members == second.members == ["1"]
    assert first.key != second.key


def test_key_ignores_runs_anchors_and_re_review_lines(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").complete("1")

    plain = boundaries_of(plan, ledger_builder, sidecar_builder, steps)[0]

    def again(b):
        b.plan().start("1").complete("1").final("issues")
        b.complete("1", files="src/other.py")

    sidecar_builder.lines.clear()
    later = boundaries_of(
        plan,
        ledger_builder,
        sidecar_builder,
        again,
        runs=(("off", 0), ("on", 2)),
    )[0]
    assert later.key == plain.key
    assert later.eligible is True and later.anchors == plain.anchors


# --- display label and prefix selection ----------------------------------------------------
K1 = "a" * 12 + "0" + "b" * 51
K2 = "a" * 12 + "1" + "b" * 51
K3 = "c" * 64


def test_label_is_the_display_prefix_when_that_is_unique(plan):
    assert plan.DISPLAY_LEN == 12
    assert plan.display_label(K3, [K1, K2, K3]) == "c" * 12


def test_label_grows_until_it_is_unique(plan):
    assert plan.display_label(K1, [K1, K2, K3]) == "a" * 12 + "0"
    assert plan.display_label(K2, [K1, K2, K3]) == "a" * 12 + "1"


def test_label_of_an_unknown_key_is_refused(plan):
    with pytest.raises(ValueError):
        plan.display_label("d" * 64, [K1, K2, K3])


def test_every_label_resolves_back_to_its_key(plan):
    keys = [K1, K2, K3]
    for key in keys:
        assert plan.resolve_prefix(plan.display_label(key, keys), keys) == key


def test_a_full_key_and_a_longer_unique_prefix_resolve(plan):
    assert plan.resolve_prefix(K3, [K1, K2, K3]) == K3
    assert plan.resolve_prefix(K1[:20], [K1, K2, K3]) == K1


def test_an_ambiguous_prefix_is_refused(plan):
    with pytest.raises(plan.KeyPrefixError) as info:
        plan.resolve_prefix("a" * 12, [K1, K2, K3])
    assert info.value.reason == "ambiguous-key"


def test_a_prefix_shorter_than_the_display_length_is_refused(plan):
    with pytest.raises(plan.KeyPrefixError) as info:
        plan.resolve_prefix("c" * 11, [K1, K2, K3])  # unique, but too short
    assert info.value.reason == "prefix-too-short"


@pytest.mark.parametrize("prefix", ["d" * 12, "C" * 12, "g" * 12, "c" * 65, ""])
def test_an_unknown_or_malformed_prefix_is_refused(plan, prefix):
    with pytest.raises(plan.KeyPrefixError) as info:
        plan.resolve_prefix(prefix, [K1, K2, K3])
    assert info.value.reason in {"unknown-boundary", "prefix-too-short"}


# =============================================================================================
# Fourth part (Task 12): ``derive_state`` and the action table (FR-107, design section 5.4,
# DD-5, DD-11). One pure function: (boundary, sidecar, git facts, flag) -> (state, action).
# DD-11 (open item O1 of the design): a prepared line without its pins is ``pending`` and a
# new attempt when HEAD still equals the prepared parent, ``uncertain`` when HEAD moved.
# =============================================================================================
PARENT = "a" * 40
MOVED = "b" * 40
STATES = {"due", "pending", "refused", "uncertain", "settled", "out-of-protocol"}
ACTIONS = {
    "none",
    "prepare",
    "retry",
    "record-recovered",
    "record-skipped",
    "stop-unsettled",
    "stop-out-of-protocol",
    "stop-uncertain",
}
ON = (("on", 0),)


def one(b):
    b.plan().start("1").complete("1")


def mixed(b):
    b.plan().start("1").start("2").complete("1").complete("2")  # anchors 5 and 6


def later_start(b):
    b.plan().start("1").complete("1").start("2")  # task 2 starts after task 1's anchor


def unfinished(b):
    b.plan().start("1")


def derived(plan, ledger_builder, sidecar_builder, steps, runs, lines, facts, flag):
    """Build the first boundary, append sidecar ``lines(side, ids, key)`` and derive."""
    text = build(ledger_builder, steps)
    for n, (mode, k) in enumerate(runs, 1):
        sidecar_builder.run(n, mode, ledger_lines=k)
    sidecar_builder.write()
    read = lambda: plan.parse_sidecar(sidecar_builder.path.read_text(encoding="utf-8"))  # noqa: E731
    found = plan.build_boundaries(
        plan.parse_ledger(text), read().runs, REPO_ID, LEDGER_ID, SOURCE_ID
    )
    first = found[0]
    if lines:
        lines(sidecar_builder, ",".join(first.members), first.key)
        sidecar_builder.write()
    base = {"head": PARENT, "q0_head": PARENT, "pins_complete": True}
    return plan.derive_state(first, read(), plan.GitFacts(**{**base, **facts}), flag)


def prep(s, ids, key, attempt=1):
    s.prepared(ids, key=key, attempt=attempt, parent=PARENT)


def refused(s, ids, key, attempt=1):
    prep(s, ids, key, attempt)
    s.refused(ids, key=key, attempt=attempt, reason="hook-failed")


def refused_then_again(s, ids, key):
    refused(s, ids, key)
    prep(s, ids, key, 2)


def uncertain(s, ids, key):
    prep(s, ids, key)
    s.refused(ids, key=key, attempt=1, reason="history-moved", uncertain=True)


def uncertain_resolved(s, ids, key):
    uncertain(s, ids, key)
    s.resolved_abandoned(ids, key=key)


# (id, steps, runs, sidecar lines, git facts, expected with the flag, expected without it)
DUE = ("due", "prepare")
STOP_UNSETTLED = ("due", "stop-unsettled")
SETTLED = ("settled", "none")
OUT = ("out-of-protocol", "stop-out-of-protocol")
UNCERTAIN = ("uncertain", "stop-uncertain")
RETRY_OK = {"retry_allowed": True}
ROWS = [
    # due: FR-107 rows 1 and 2, design 5.4 rows 2 to 5
    ("due-crash-explained", one, ON, None, {}, DUE, STOP_UNSETTLED),
    ("due-empty-set", one, ON, None, {"s_empty": True}, ("due", "record-skipped"), STOP_UNSETTLED),
    ("due-mixed-authorization", mixed, (("on", 0), ("off", 5)), None, {}, ("due", "record-skipped"), STOP_UNSETTLED),
    ("due-later-start", later_start, ON, None, {}, OUT, OUT),
    # a boundary that was never eligible is nothing to settle (FR-103); a running one is not due
    ("never-eligible-off-segment", one, (("off", 0),), None, {}, SETTLED, SETTLED),
    ("never-eligible-no-sidecar-run", one, (), None, {}, SETTLED, SETTLED),
    ("not-complete-yet", unfinished, ON, None, {}, SETTLED, SETTLED),
    # pending: prepared, no terminal line
    ("pending-head-at-parent-retry-ok", one, ON, prep, RETRY_OK, ("pending", "retry"), ("pending", "stop-unsettled")),
    ("pending-head-at-parent-candidate-changed", one, ON, prep, {}, ("pending", "stop-unsettled"), ("pending", "stop-unsettled")),
    ("pending-dd11-no-pins-head-at-parent", one, ON, prep, {"pins_complete": False, **RETRY_OK}, ("pending", "retry"), ("pending", "stop-unsettled")),
    ("pending-dd11-no-pins-head-moved", one, ON, prep, {"head": MOVED, "pins_complete": False}, UNCERTAIN, UNCERTAIN),
    ("pending-dd11-no-pins-head-moved-even-if-proved", one, ON, prep, {"head": MOVED, "pins_complete": False, "proves_commit": MOVED}, UNCERTAIN, UNCERTAIN),
    ("pending-proved-existing-commit", one, ON, prep, {"head": MOVED, "proves_commit": MOVED}, ("pending", "record-recovered"), ("pending", "record-recovered")),
    ("pending-head-moved-not-proved", one, ON, prep, {"head": MOVED}, UNCERTAIN, UNCERTAIN),
    ("pending-head-unknown-fails-closed", one, ON, prep, {"head": None}, UNCERTAIN, UNCERTAIN),
    # refused: terminal refused line
    ("refused-head-at-parent-retry-ok", one, ON, refused, RETRY_OK, ("refused", "retry"), ("refused", "stop-unsettled")),
    ("refused-head-at-parent-candidate-changed", one, ON, refused, {}, ("refused", "stop-unsettled"), ("refused", "stop-unsettled")),
    ("refused-head-moved", one, ON, refused, {"head": MOVED, **RETRY_OK}, ("refused", "stop-unsettled"), ("refused", "stop-unsettled")),
    ("refused-head-moved-proved-is-not-recovered", one, ON, refused, {"head": MOVED, "proves_commit": MOVED}, ("refused", "stop-unsettled"), ("refused", "stop-unsettled")),
    ("refused-then-new-attempt-is-pending", one, ON, refused_then_again, RETRY_OK, ("pending", "retry"), ("pending", "stop-unsettled")),
    # uncertain: never retried, never committed
    ("uncertain-line", one, ON, uncertain, RETRY_OK, UNCERTAIN, UNCERTAIN),
    # settled lines, and an owner answer over an unsettled state
    ("settled-sha", one, ON, lambda s, i, k: (prep(s, i, k), s.commit(i, key=k)), {}, SETTLED, SETTLED),
    ("settled-recovered", one, ON, lambda s, i, k: (prep(s, i, k), s.commit(i, key=k, recovered=True)), {}, SETTLED, SETTLED),
    ("settled-skipped", one, ON, lambda s, i, k: s.skipped(i, key=k), {}, SETTLED, SETTLED),
    ("settled-abandoned", one, ON, lambda s, i, k: s.resolved_abandoned(i, key=k), {}, SETTLED, SETTLED),
    ("settled-adopted", one, ON, lambda s, i, k: (prep(s, i, k), s.resolved_adopted(i, key=k)), {}, SETTLED, SETTLED),
    ("settled-uncertain-then-resolved", one, ON, uncertain_resolved, {}, SETTLED, SETTLED),
]  # fmt: skip


@pytest.mark.parametrize("flag", [True, False], ids=["flag", "no-flag"])
@pytest.mark.parametrize("row", ROWS, ids=[r[0] for r in ROWS])
def test_derive_state_table(plan, ledger_builder, sidecar_builder, row, flag):
    _, steps, runs, lines, facts, with_flag, without_flag = row
    got = derived(
        plan, ledger_builder, sidecar_builder, steps, runs, lines, facts, flag
    )
    assert got == (with_flag if flag else without_flag)
    assert got[0] in STATES and got[1] in ACTIONS


def test_an_unflagged_run_never_prepares_retries_or_skips():
    for _, _, _, _, _, _, without_flag in ROWS:
        assert without_flag[1] not in {"prepare", "retry", "record-skipped"}


def test_every_action_and_state_of_the_closed_lists_is_reached():
    seen = {x for row in ROWS for x in (row[5], row[6])}
    assert {s for s, _ in seen} == STATES
    assert {a for _, a in seen} == ACTIONS


def test_a_later_start_blocks_preparation_even_with_an_empty_set(
    plan, ledger_builder, sidecar_builder
):
    got = derived(
        plan,
        ledger_builder,
        sidecar_builder,
        later_start,
        ON,
        None,
        {"s_empty": True},
        True,
    )
    assert got == OUT


# --- purity -------------------------------------------------------------------------------
def test_derive_state_takes_the_four_inputs_and_nothing_that_reads_the_repository(plan):
    import inspect

    params = list(inspect.signature(plan.derive_state).parameters)
    assert params == ["boundary", "sidecar", "git_facts", "flag"]
    fields = {f.name for f in plan.GitFacts.__dataclass_fields__.values()}
    assert fields == {
        "head",
        "q0_head",
        "s_empty",
        "pins_complete",
        "proves_commit",
        "retry_allowed",
    }


def test_same_inputs_give_byte_identical_output_and_start_no_process(
    plan, ledger_builder, sidecar_builder, monkeypatch
):
    import subprocess

    def boom(*a, **k):
        raise AssertionError("derive_state started a process")

    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    outputs = [
        repr(
            derived(
                plan, ledger_builder, sidecar_builder, one, ON, prep, RETRY_OK, True
            )
        )
        for _ in range(2)
    ]
    sidecar_builder.lines.clear()
    assert outputs[0] == outputs[1] == repr(("pending", "retry"))


# --- crash-explained: the ledger part of FR-105, carried on the boundary ---------------------
def crash_flags(plan, ledger_builder, sidecar_builder, steps):
    return [
        b.crash_explained
        for b in boundaries_of(plan, ledger_builder, sidecar_builder, steps)
    ]


def test_a_boundary_with_nothing_after_it_is_crash_explained(
    plan, ledger_builder, sidecar_builder
):
    assert crash_flags(plan, ledger_builder, sidecar_builder, one) == [True]


def test_a_later_start_means_not_crash_explained(plan, ledger_builder, sidecar_builder):
    def steps(b):
        b.plan().start("1").complete("1").start("2").complete("2")

    assert crash_flags(plan, ledger_builder, sidecar_builder, steps) == [False, True]


def test_an_open_task_means_not_crash_explained(plan, ledger_builder, sidecar_builder):
    assert crash_flags(plan, ledger_builder, sidecar_builder, later_start) == [
        False,
        False,
    ]


def test_a_restart_of_a_member_after_its_anchor_is_a_later_start(
    plan, ledger_builder, sidecar_builder
):
    def steps(b):
        b.plan().start("1").complete("1").start("1")

    assert crash_flags(plan, ledger_builder, sidecar_builder, steps) == [False, False]


def test_a_batch_is_crash_explained_when_nothing_starts_after_its_anchors(
    plan, ledger_builder, sidecar_builder
):
    assert crash_flags(plan, ledger_builder, sidecar_builder, mixed) == [True]
