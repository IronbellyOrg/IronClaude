"""Extractor E3 (class C8, DESIGN 4.4): files that refer to a file the plan edits.

Each extractor test has a positive case, a negative case, a near-miss or boundary case and a determinism case.
`find_e3` reads the tracked-file list of the snapshot built by fixtures/repos/build_repo.py (git runs there only);
`attach_e3` makes one batched search over the DD-5 scope.
"""

import json
from pathlib import Path

import pytest

from fixtures.repos.build_repo import build_repo
from sweep import extractors, plan
from sweep.extractors import Candidate, Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
EDIT = (
    "Edit `src/exporter/report.py` so that `render` accepts the format name `ndjson`."
)
ZEBRA = "src/exporter/zebra_stripe.py"
ZEBRA_EDIT = f"Edit `{ZEBRA}` so that `paint` draws the stripes."


def mkplan(sentence=EDIT, gate="`make test` exits 0."):
    """A one-task plan: line 3 holds the edit sentence and line 6 the gate bullet."""
    return plan.parse(
        f"## Task 1: Change the module\n\n{sentence}\n\nAcceptance criteria:\n- {gate}\n"
    )


def find(doc, snapshot=None, **kw):
    return extractors.find_e3(doc, Ctx(doc, snapshot=snapshot, **kw))


def run(doc, snapshot=None, **kw):
    """find, then attach every candidate (the tests here have few)."""
    ctx = Ctx(doc, snapshot=snapshot, **kw)
    cands = extractors.find_e3(doc, ctx)
    extractors.attach_e3(cands, ctx)
    return cands


def texts(c):
    return [e["text"] for e in c.evidence]


def paths(c):
    return [e["path"] for e in c.evidence]


def dump(cands):
    return json.dumps([c.to_dict() for c in cands], sort_keys=True)


def zebra_repo(tmp_path, tests=0, docs=0, extra=None, target=ZEBRA):
    """F-REPO plus the file `target` (it does not hold its own stem) and files that hold that stem: `tests` test
    files (tests/test_z<i>.py) and `docs` other files (docs/note<ii>.md)."""
    stem = target.rpartition("/")[2].rpartition(".")[0]
    files = {target: "def paint():\n    pass\n", **(extra or {})}
    files.update(
        {f"tests/test_z{i}.py": f"import {stem}  # {i}\n" for i in range(tests)}
    )
    files.update(
        {f"docs/note{i:02d}.md": f"The {stem} helper, note {i}.\n" for i in range(docs)}
    )
    return build_repo(tmp_path, extra=files).repo


@pytest.fixture
def repo(tmp_path):
    return build_repo(tmp_path).repo


# ---------------------------------------------------------------- positive: a test names the stem and the plan does not name the test


def test_positive_unnamed_test_that_names_the_stem_is_found_first(repo):
    (c,) = run(mkplan(), repo)
    assert (c.extractor, c.cls, c.kind) == ("E3", "C8", "dependents")
    assert c.anchor_text == EDIT
    assert c.location == {"task": "T1", "line_start": 3, "line_end": 3}
    # tests/test_report.py holds `from exporter.report import render` (the stem, not the path) and no plan line names it
    assert c.evidence[0] == {
        "path": "tests/test_report.py",
        "line": 1,
        "text": "from exporter.report import render",
    }
    assert c.features["unnamed_test_files"] == 1
    # tests first, then the others in path order (4 files at most), then the gate line
    assert paths(c) == [
        "tests/test_report.py",
        "CHANGELOG.md",
        "README.md",
        "docs/guide.md",
        "plan",
    ]
    assert c.evidence[-1] == {"path": "plan", "line": 6, "text": "gate names: NONE"}


def test_positive_features_and_priority_terms(repo):
    (found,) = find(mkplan(), repo)
    assert found.features == {
        "stem_len": 6,
        "has_distinctive": 1,
        "path": "src/exporter/report.py",
        "stem": "report",
    }
    assert (
        found.pre_priority == 40 + 10
    )  # stem_len 6 < 8, one identifier (`render`) in the sentence
    assert found.evidence == [] and found.priority is None  # find adds no evidence
    (c,) = run(mkplan(), repo)
    f = c.features
    # `report` is in 8 files: the target itself, tests/test_report.py and 6 others (CHANGELOG.md, README.md,
    # docs/guide.md, plugins/.../report.py, scripts/export.sh, src/exporter/retention.py); none is named by the plan
    assert (f["unnamed_test_files"], f["unnamed_other_files"]) == (1, 6)
    assert f["stem_hits"] == 8
    assert c.priority == 50 + 15 * 1 + 5 * 2 + 10  # gate names NONE


def test_positive_counts_are_capped_in_the_formula_not_in_the_features(tmp_path):
    repo = zebra_repo(tmp_path, tests=5, docs=3)
    (c,) = run(mkplan(ZEBRA_EDIT), repo)
    assert (c.features["unnamed_test_files"], c.features["unnamed_other_files"]) == (
        5,
        3,
    )
    assert c.pre_priority == 40 + 10 + 10  # stem_len 12 >= 8 and `paint`
    assert c.priority == 100  # 60 + 45 + 10 + 10 = 125, clamped
    # 4 referencing files and the gate line: the 5 entries DESIGN 4.1 allows
    assert paths(c) == [f"tests/test_z{i}.py" for i in range(4)] + ["plan"]
    c.validate(Ctx(mkplan(ZEBRA_EDIT)))


SHORT = "src/exporter/zebra.py"
SHORT_EDIT = (
    f"Edit `{SHORT}` so that it paints."  # stem_len 5, no identifier: pre_priority 40
)


@pytest.mark.parametrize(
    "tests, docs, expected",
    [
        (0, 0, 40 + 10),
        (1, 0, 40 + 15 + 10),
        (3, 0, 40 + 45 + 10),
        (5, 0, 40 + 45 + 10),  # the test term stops at 3 files
        (0, 1, 40 + 5 + 10),
        (0, 2, 40 + 10 + 10),
        (0, 5, 40 + 10 + 10),  # the other term stops at 2 files
        (2, 3, 40 + 30 + 10 + 10),
    ],
)
def test_priority_formula_terms_and_caps(tmp_path, tests, docs, expected):
    repo = zebra_repo(tmp_path, tests=tests, docs=docs, target=SHORT)
    (c,) = run(mkplan(SHORT_EDIT), repo)
    assert c.pre_priority == 40
    assert (c.features["unnamed_test_files"], c.features["unnamed_other_files"]) == (
        tests,
        docs,
    )
    assert c.priority == expected


def test_positive_the_gate_that_names_a_referencing_file_removes_the_none_bonus(repo):
    gate = "`pytest tests/test_report.py -q` exits 0."
    (c,) = run(mkplan(gate=gate), repo)
    assert c.evidence[-1] == {
        "path": "plan",
        "line": 6,
        "text": "gate names: tests/test_report.py",
    }
    # the plan names the test now, so it is no longer an unnamed referencing file
    assert c.features[
        "unnamed_test_files"
    ] == 0 and "tests/test_report.py" not in paths(c)
    assert c.priority == 50 + 5 * 2 + 0  # no test bonus, no NONE bonus


def test_positive_two_targets_in_one_sentence_give_two_candidates(repo):
    sentence = "Edit `src/exporter/report.py` and `docs/guide.md` together."
    a, b = run(mkplan(sentence), repo)
    assert (a.features["path"], b.features["path"]) == (
        "docs/guide.md",
        "src/exporter/report.py",
    )  # path order
    assert a.anchor_text == b.anchor_text == sentence


# ---------------------------------------------------------------- negative: nothing to extract


def test_negative_a_target_the_plan_creates_is_not_a_candidate(repo):
    # src/exporter/retention.py exists in the snapshot (the implementation commit added it) but the plan creates it
    doc = mkplan("Create `src/exporter/retention.py` with a function `expired`.")
    assert doc.of("edit_target")[0]["creates"] is True
    assert find(doc, repo) == [] and run(doc, repo) == []


def test_negative_a_target_that_is_not_in_the_snapshot_is_not_a_candidate(repo):
    assert (
        find(mkplan("Edit `docs/absent.md` so that it lists the formats."), repo) == []
    )
    assert (
        find(mkplan("Edit `docs/` so that it lists the formats."), repo) == []
    )  # a folder is not a file


def test_negative_no_snapshot_means_no_target_is_present():
    assert find(mkplan()) == []


def test_negative_a_sentence_without_an_edit_target_gives_nothing(repo):
    assert find(mkplan("Run the test suite once more."), repo) == []


def test_negative_dev_dependency_and_ground_truth_files_are_never_evidence(tmp_path):
    repo = zebra_repo(
        tmp_path,
        extra={
            ".dev/notes/zebra.md": "zebra_stripe in a .dev note\n",
            "node_modules/pkg/zebra.js": "// zebra_stripe\n",
            "docs/ground-truth.json": '{"note": "zebra_stripe"}\n',
        },
    )
    (c,) = run(mkplan(ZEBRA_EDIT), repo)
    assert (
        c.features["unnamed_test_files"],
        c.features["unnamed_other_files"],
        c.features["stem_hits"],
    ) == (0, 0, 0)
    assert paths(c) == ["plan"]


def test_negative_the_edited_file_is_not_its_own_dependent(tmp_path):
    repo = zebra_repo(tmp_path, extra={ZEBRA: "ZEBRA = 'zebra_stripe'\n"})
    (c,) = run(mkplan(ZEBRA_EDIT), repo)
    assert paths(c) == ["plan"] and c.features["unnamed_other_files"] == 0
    assert (
        c.features["stem_hits"] == 1
    )  # stem_hits counts every file, the target included (DESIGN 4.4)


def test_negative_a_referencing_file_the_plan_names_is_not_unnamed(tmp_path):
    repo = zebra_repo(tmp_path, tests=1, docs=1)
    sentence = f"{ZEBRA_EDIT} The files `docs/note00.md` and `tests/test_z0.py` use it."
    (c,) = run(mkplan(sentence), repo)
    assert (
        c.features["unnamed_test_files"] == 0 and c.features["unnamed_other_files"] == 0
    )
    assert c.features["stem_hits"] == 2
    assert paths(c) == ["plan"]


# ---------------------------------------------------------------- boundaries and near misses


@pytest.mark.parametrize("n, penalty", [(39, 0), (40, 0), (41, 20), (60, 20)])
def test_a_stem_that_hits_more_than_40_files_lowers_priority_by_20(
    tmp_path, n, penalty
):
    repo = zebra_repo(tmp_path, docs=n)
    (c,) = run(mkplan(ZEBRA_EDIT), repo)
    assert c.features["stem_hits"] == n
    assert c.features["unnamed_other_files"] == n
    assert c.priority == 60 + 5 * 2 + 10 - penalty
    assert len(c.evidence) == 5  # 4 files and the gate line, however many files hit


def test_the_penalty_is_the_only_difference_between_40_and_41_hits(tmp_path):
    low = run(mkplan(ZEBRA_EDIT), zebra_repo(tmp_path / "a", docs=40))[0]
    high = run(mkplan(ZEBRA_EDIT), zebra_repo(tmp_path / "b", docs=41))[0]
    assert low.pre_priority == high.pre_priority
    assert low.priority - high.priority == 20


@pytest.mark.parametrize(
    "name, stem_len, base",
    [
        ("src/exporter/abcdefg.py", 7, 40),
        ("src/exporter/abcdefgh.py", 8, 50),
        ("src/exporter/abcdefghi.py", 9, 50),
    ],
)
def test_stem_length_8_is_the_long_stem_boundary(tmp_path, name, stem_len, base):
    repo = build_repo(tmp_path, extra={name: "x = 1\n"}).repo
    (c,) = find(mkplan(f"Edit `{name}` so that it is shorter."), repo)
    assert (c.features["stem_len"], c.features["has_distinctive"], c.pre_priority) == (
        stem_len,
        0,
        base,
    )


def test_stem_is_the_base_name_without_its_last_extension(tmp_path):
    repo = build_repo(
        tmp_path, extra={"docs/a.b.c.md": "x\n", "Makefile.local": "x\n"}
    ).repo
    sentence = "Edit `docs/a.b.c.md` so that it is shorter."
    assert find(mkplan(sentence), repo)[0].features["stem"] == "a.b.c"
    # no extension: the whole name is the stem
    assert (
        find(mkplan("Edit `scripts/export.sh` and tidy it."), repo)[0].features["stem"]
        == "export"
    )


@pytest.mark.parametrize(
    "sentence, distinctive",
    [
        ("Edit `src/exporter/report.py` so that `render` takes a format.", 1),
        ("Edit `src/exporter/report.py` so that it takes a format.", 0),
        (
            "Edit `src/exporter/report.py` and keep the word render in plain text.",
            0,
        ),  # not in backticks
        (
            "Edit `src/exporter/report.py` and call `report.py` again.",
            0,
        ),  # the file name, not an identifier
        ("Edit `src/exporter/report.py` and call `report` again.", 0),  # the stem
        (
            "Edit `src/exporter/report.py` and run `make test`.",
            0,
        ),  # a command, not an identifier
        ("Edit `src/exporter/report.py` and read `docs/guide.md` first.", 0),  # a path
    ],
)
def test_has_distinctive_is_a_backticked_identifier_of_the_sentence(
    repo, sentence, distinctive
):
    c = next(
        c
        for c in find(mkplan(sentence), repo)
        if c.features["path"] == "src/exporter/report.py"
    )
    assert c.features["has_distinctive"] == distinctive
    assert c.pre_priority == 40 + 10 * distinctive


def test_a_gate_that_runs_a_whole_folder_names_none_of_its_files(repo):
    (c,) = run(mkplan(gate="`pytest tests/` exits 0."), repo)
    assert (
        c.evidence[-1]["text"] == "gate names: NONE"
    )  # DESIGN 4.4 reads "names"; a folder token names no file


def test_a_plan_without_any_gate_still_gives_none_with_line_0(repo):
    doc = plan.parse(f"## Task 1: Change the module\n\n{EDIT}\n")
    assert doc.of("gate") == []
    (c,) = run(doc, repo)
    assert c.evidence[-1] == {"path": "plan", "line": 0, "text": "gate names: NONE"}


@pytest.mark.parametrize(
    "path, is_test",
    [
        ("tests/a.py", True),
        ("src/pkg/tests/a.py", True),
        ("src/test_a.py", True),
        ("src/a_test.py", True),
        ("src/a.spec.ts", True),
        ("src/specs/a.py", True),
        ("src/conftest.py", True),
        ("docs/guide.md", False),
        ("src/contest.py", False),
        ("src/latest.py", False),
        ("scripts/attest.sh", False),
        ("src/inspect.md", False),
    ],
)
def test_test_files_are_told_by_folder_or_file_name(path, is_test):
    assert bool(extractors._TEST_PATH.search(path)) is is_test


def test_long_sentence_anchor_is_a_prefix_and_long_hit_lines_are_cut(tmp_path):
    long_hit = "zebra_stripe " + "w" * 300 + "\n"
    repo = zebra_repo(tmp_path, extra={"docs/long.md": long_hit})
    sentence = (
        ZEBRA_EDIT.removesuffix(".") + " and " + "then add more words " * 15 + "to it."
    )
    doc = mkplan(sentence)
    (c,) = run(doc, repo)
    assert len(c.anchor_text) == 200 and sentence.startswith(c.anchor_text)
    assert c.evidence[0]["path"] == "docs/long.md" and len(c.evidence[0]["text"]) == 160
    c.validate(Ctx(doc))


def test_the_gate_line_is_cut_at_a_whole_path():
    names = [
        f"tests/some/very/long/folder/test_file_number_{i:02d}.py" for i in range(8)
    ]
    text = extractors._gate_names_text(names)
    assert (
        len(text) <= 160
        and text.startswith("gate names: tests/some")
        and text.endswith(" more")
    )
    assert all(
        n in names
        for n in text.removeprefix("gate names: ").split(", and ")[0].split(", ")
    )
    assert extractors._gate_names_text(names[:2]) == "gate names: " + ", ".join(
        names[:2]
    )
    assert extractors._gate_names_text([]) == "gate names: NONE"


# ---------------------------------------------------------------- the two plan fixtures, and determinism


def test_p_basic_emits_the_two_existing_targets(repo):
    doc = plan.read(PLANS / "p_basic.md")
    cands = run(doc, repo, seed=1)
    assert [
        (c.features["path"], c.location["task"], c.pre_priority, c.priority)
        for c in cands
    ] == [
        ("src/exporter/report.py", "T1", 50, 85),
        ("docs/guide.md", "T2", 40, 50),
    ]
    first = cands[0]
    assert (
        first.features["unnamed_test_files"],
        first.features["unnamed_other_files"],
    ) == (1, 4)
    assert first.evidence[0]["path"] == "tests/test_report.py"
    # the gate of p_basic (line 60) names tests/test_retention.py and `make test`, neither of which refers to the file
    assert first.evidence[-1] == {
        "path": "plan",
        "line": 60,
        "text": "gate names: NONE",
    }
    assert paths(cands[1]) == ["plan"]  # nothing else refers to `guide`


def test_p_clean_emits_nothing(repo):
    doc = plan.read(PLANS / "p_clean.md")
    assert find(doc) == [] and find(doc, repo) == []
    assert run(doc, repo) == []
    assert (
        extractors.run_extractors(
            Ctx(doc, snapshot=repo), {"E3": extractors.EXTRACTORS["E3"]}
        )
        == []
    )


def test_determinism_on_p_basic_and_p_clean(repo):
    for name in ("p_basic.md", "p_clean.md"):
        doc = plan.read(PLANS / name)
        assert dump(run(doc, repo, seed=1)) == dump(run(doc, repo, seed=1))
        assert dump(find(doc, repo, seed=1)) == dump(
            find(doc, repo, seed=2)
        )  # the seed only orders, in select


def test_determinism_does_not_depend_on_the_order_the_candidates_are_attached(tmp_path):
    repo = zebra_repo(tmp_path, tests=2, docs=3)
    doc = mkplan(f"{ZEBRA_EDIT} Edit `src/exporter/report.py` as well.")
    ctx = Ctx(doc, snapshot=repo)
    one = extractors.find_e3(doc, ctx)
    two = extractors.find_e3(doc, ctx)
    extractors.attach_e3(one, ctx)
    extractors.attach_e3(list(reversed(two)), ctx)
    assert dump(one) == dump(two)


def test_attach_needs_only_the_candidate_and_ctx(repo):
    doc = mkplan()
    ctx = Ctx(doc, snapshot=repo)
    (c,) = extractors.find_e3(doc, ctx)
    copy = Candidate(
        c.extractor,
        c.cls,
        c.kind,
        c.anchor_text,
        dict(c.location),
        features=dict(c.features),
        pre_priority=c.pre_priority,
    )
    extractors.attach_e3([c], ctx)
    extractors.attach_e3([copy], Ctx(doc, snapshot=repo))
    assert dump([c]) == dump([copy])


# ---------------------------------------------------------------- the snapshot and the evidence rules


def test_non_git_snapshot_raises(tmp_path):
    folder = tmp_path / "plain"
    folder.mkdir()
    with pytest.raises(extractors.NotAGitRepo):
        find(mkplan(), folder)


def test_attach_without_a_snapshot_never_raises_and_adds_no_evidence(repo):
    doc = mkplan()
    (c,) = find(doc, repo)
    extractors.attach_e3([c], Ctx(doc))
    assert c.evidence == [] and c.priority == c.pre_priority == 50


def test_evidence_holds_no_claim_no_severity_no_defect(repo, tmp_path):
    docs = [(plan.read(PLANS / "p_basic.md"), repo), (mkplan(), repo)]
    z = zebra_repo(tmp_path / "z", tests=6, docs=6)
    docs.append((mkplan(ZEBRA_EDIT), z))
    cands = [(doc, c) for doc, snap in docs for c in run(doc, snap)]
    assert cands
    blob = " ".join(e["text"] for _, c in cands for e in c.evidence).lower()
    assert blob
    for word in (
        "defect",
        "severity",
        "blocking",
        "wrong",
        "bug",
        "missing",
        "should",
        "must",
    ):
        assert word not in blob
    for doc, c in cands:
        c.validate(
            Ctx(doc)
        )  # every limit of DESIGN 4.1: anchor, location, priority, at most 5 entries, 160 chars
        assert all(
            e["path"] == "plan" or not e["path"].startswith((".dev/", "node_modules/"))
            for e in c.evidence
        )


# ---------------------------------------------------------------- the registry


def test_registered_and_driven_by_run_extractors(repo):
    assert extractors.EXTRACTORS["E3"] == (extractors.find_e3, extractors.attach_e3)
    doc = plan.read(PLANS / "p_basic.md")
    ctx = Ctx(doc, snapshot=repo, seed=1)
    out = extractors.run_extractors(ctx, {"E3": extractors.EXTRACTORS["E3"]})
    assert [
        (c.cls, c.route, c.status, c.evidence_computed, c.priority) for c in out
    ] == [
        ("C8", "search", "attached", True, 85),
        ("C8", "search", "attached", True, 50),
    ]
