"""Extractor E4 (class C5, DESIGN 4.5): a count or "no remaining" claim and the places that still carry it.

Each extractor test has a positive case, a negative case, a near-miss or boundary case and a determinism case.
`find_e4` is lexical (no repository access); `attach_e4` makes one batched search over the DD-5 scope of the snapshot
built by fixtures/repos/build_repo.py (git runs there only). In that repository the root documents README.md and
CHANGELOG.md and docs/guide.md all carry the string `3 report formats`; `.dev/` and `node_modules/` repeat it too.
"""

import json
from pathlib import Path

import pytest

from fixtures.repos.build_repo import MIRROR, build_repo
from sweep import extractors, plan
from sweep.extractors import Candidate, Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
COUNT = "Edit `docs/guide.md` and update the count from 3 report formats to 4 report formats."
NEG = "No remaining `3 report formats` text exists in `docs/guide.md`."
HITS_LINE = "hits: 3 in 3 files (1 named by the plan)"


def mkplan(sentence=COUNT, criterion="`make test` exits 0."):
    """A one-task plan: line 3 holds the sentence and line 6 the criterion bullet."""
    return plan.parse(
        f"## Task 1: Change the guide\n\n{sentence}\n\nAcceptance criteria:\n- {criterion}\n"
    )


def find(doc, snapshot=None, **kw):
    return extractors.find_e4(doc, Ctx(doc, snapshot=snapshot, **kw))


def run(doc, snapshot=None, **kw):
    ctx = Ctx(doc, snapshot=snapshot, **kw)
    cands = extractors.find_e4(doc, ctx)
    extractors.attach_e4(cands, ctx)
    return cands


def needles(doc):
    return [(c.kind, c.features["needle"]) for c in find(doc)]


def paths(c):
    return [e["path"] for e in c.evidence]


def dump(cands):
    return json.dumps([c.to_dict() for c in cands], sort_keys=True)


def zebra_repo(tmp_path, extra, needle="7 zebra stripes"):
    """F-REPO plus `extra` files; a file whose text is None holds the needle on one line."""
    files = {
        p: (f"The {needle} are here.\n" if t is None else t) for p, t in extra.items()
    }
    return build_repo(tmp_path, extra=files).repo


@pytest.fixture
def repo(tmp_path):
    return build_repo(tmp_path).repo


# ---------------------------------------------------------------- positive: a count change and a negative claim


def test_positive_count_change_finds_the_old_count_and_the_unnamed_root_documents(repo):
    (c,) = run(mkplan(), repo)
    assert (c.extractor, c.cls, c.kind) == ("E4", "C5", "count")
    assert c.anchor_text == COUNT
    assert c.location == {"task": "T1", "line_start": 3, "line_end": 3}
    assert (
        c.features["needle"] == "3 report formats"
    )  # the old value, not "4 report formats"
    # README.md and CHANGELOG.md are root documents the plan never names; docs/guide.md is named. Root documents and
    # change logs first, in path order, then the `hits:` line (3 hit lines in 3 files, 1 of them named)
    assert c.evidence == [
        {
            "path": "CHANGELOG.md",
            "line": 3,
            "text": "- 0.1.0: first release (3 report formats)",
        },
        {"path": "README.md", "line": 6, "text": "- 3 report formats"},
        {"path": "plan", "line": 3, "text": HITS_LINE},
    ]
    assert (c.features["unnamed_root_hits"], c.features["unnamed_hits"]) == (2, 2)
    assert c.pre_priority == 30 + 10 + 10  # a count change; three words
    assert c.priority == 50 + 20 + 10 * 2


def test_positive_negative_claim_takes_the_backticked_phrase(repo):
    doc = mkplan("Edit `docs/guide.md`.", criterion=NEG)
    (c,) = run(doc, repo)
    assert (c.kind, c.anchor_text) == ("negative", NEG)
    assert (
        c.features["needle"] == "3 report formats"
    )  # the phrase, not the path `docs/guide.md`
    assert c.location == {"task": "T1", "line_start": 6, "line_end": 6}
    assert c.pre_priority == 30 + 0 + 10  # not a count change; three words
    assert c.priority == 40 + 20 + 10 * 2
    assert c.evidence[-1] == {"path": "plan", "line": 6, "text": HITS_LINE}


@pytest.mark.parametrize(
    "trigger",
    [
        "No remaining",
        "None of",
        "It returns zero hits for",
        "It prints no matches for",
        "It prints 0 matches for",
    ],
)
def test_positive_each_negative_trigger_word(trigger):
    cs = find(mkplan(f"{trigger} `old banner text` appears in docs."))
    assert [(c.kind, c.features["needle"]) for c in cs] == [
        ("negative", "old banner text")
    ]


def test_positive_the_priority_terms_for_root_and_unnamed_hits(tmp_path):
    # one unnamed hit in a root document: +20 and +10; a plan-named copy gives neither
    repo = zebra_repo(tmp_path, {"NOTES.md": None, "docs/a.md": None})
    sentence = "Edit `docs/a.md` so that it lists 7 zebra stripes."
    (c,) = run(mkplan(sentence), repo)
    assert c.features["needle"] == "7 zebra stripes"
    assert (c.features["unnamed_root_hits"], c.features["unnamed_hits"]) == (1, 1)
    assert paths(c) == ["NOTES.md", "plan"]
    assert c.evidence[-1]["text"] == "hits: 2 in 2 files (1 named by the plan)"
    assert c.priority == c.pre_priority + 20 + 10


def test_positive_a_root_document_the_plan_names_gives_no_priority_bonus(repo):
    # README.md and CHANGELOG.md repeat the count. Naming one leaves the other, so the bonus stays ...
    one = f"{COUNT} The file `README.md` is in scope too."
    (c,) = run(mkplan(one), repo)
    assert (c.features["unnamed_root_hits"], c.features["unnamed_hits"]) == (1, 1)
    assert paths(c) == ["CHANGELOG.md", "plan"]
    assert c.priority == 50 + 20 + 10
    # ... naming both removes it: no unnamed hit is left, so the item stays at its pre-priority
    both = f"{COUNT} The files `README.md` and `CHANGELOG.md` are in scope too."
    (c,) = run(mkplan(both), repo)
    assert (c.features["unnamed_root_hits"], c.features["unnamed_hits"]) == (0, 0)
    assert paths(c) == ["plan"]
    assert c.evidence[0]["text"] == "hits: 3 in 3 files (3 named by the plan)"
    assert c.priority == c.pre_priority == 50


@pytest.mark.parametrize("token", ["./README.md", "README.md"])
def test_a_root_document_is_named_by_its_bare_name_or_a_dot_slash_path(repo, token):
    sentence = f"{COUNT} Do not touch `{token}` or `CHANGELOG.md`."
    (c,) = run(mkplan(sentence), repo)
    assert c.features["unnamed_hits"] == 0


def test_the_name_of_a_file_in_a_folder_does_not_name_the_root_document(tmp_path):
    repo = zebra_repo(tmp_path, {"NOTES.md": None, "docs/NOTES.md": None})
    sentence = "Edit `docs/NOTES.md` so that it lists 7 zebra stripes."
    (c,) = run(mkplan(sentence), repo)
    assert paths(c) == ["NOTES.md", "plan"] and c.features["unnamed_root_hits"] == 1
    assert c.evidence[-1]["text"] == "hits: 2 in 2 files (1 named by the plan)"


def test_the_plan_names_a_file_by_a_path_token_like_e3(tmp_path):
    repo = zebra_repo(tmp_path, {"docs/a.md": None, "docs/b.md": None})
    (c,) = run(mkplan("Edit `docs/a.md` so that it lists 7 zebra stripes."), repo)
    assert paths(c) == ["docs/b.md", "plan"]
    assert c.evidence[-1]["text"] == "hits: 2 in 2 files (1 named by the plan)"


def test_positive_the_two_sentences_of_p_basic_give_two_items(repo):
    doc = plan.read(PLANS / "p_basic.md")
    cands = run(doc, repo, seed=1)
    assert [
        (
            c.kind,
            c.features["needle"],
            c.location["task"],
            c.location["line_start"],
            c.pre_priority,
            c.priority,
        )
        for c in cands
    ] == [
        ("count", "3 report formats", "T2", 40, 50, 90),
        ("negative", "3 report formats", "T2", 46, 40, 80),
    ]
    for c in cands:
        assert paths(c) == ["CHANGELOG.md", "README.md", "plan"]
        assert c.evidence[-1]["text"] == HITS_LINE  # docs/guide.md is named by p_basic
        assert (c.features["unnamed_root_hits"], c.features["unnamed_hits"]) == (2, 2)


def test_positive_the_doc_format_finds_the_count_once(repo):
    doc = plan.read(PLANS.parent / "docs" / "doc1.md", "doc")
    assert [b["kind"] for b in doc.blocks if "3 report formats" in b["text"]] == [
        "task",
        "criterion",
    ]
    (c,) = run(
        doc, repo
    )  # the sentence is in a `task` block and in a `criterion` block: one item
    assert (c.kind, c.features["needle"], c.location["line_start"]) == (
        "count",
        "3 report formats",
        3,
    )
    assert paths(c) == ["CHANGELOG.md", "README.md", "docs/guide.md", "plan"]
    assert c.evidence[-1]["text"] == "hits: 3 in 3 files (0 named by the plan)"


def test_positive_a_goal_is_an_input_block(repo):
    doc = plan.parse(
        "# Plan\n\nGoal: The guide lists 3 report formats and the plan changes nothing else.\n\n"
        "## Task 1: Change the guide\n\nEdit `docs/guide.md`.\n\nAcceptance criteria:\n- `make test` exits 0.\n"
    )
    assert [
        b["id"] for b in doc.blocks if b["task"] is None and b["kind"] == "criterion"
    ] == ["goal"]
    (c,) = find(doc, repo)
    assert (c.location["task"], c.features["needle"]) == (None, "3 report formats")


# ---------------------------------------------------------------- negative: nothing to extract


def test_negative_p_clean_emits_nothing(repo):
    doc = plan.read(PLANS / "p_clean.md")
    assert find(doc) == [] and find(doc, repo) == []
    assert run(doc, repo) == []
    out = extractors.run_extractors(
        Ctx(doc, snapshot=repo), {"E4": extractors.EXTRACTORS["E4"]}
    )
    assert out == []


@pytest.mark.parametrize(
    "sentence",
    [
        "Create `src/exporter/notice.py` and tell the reader that report id 41 has expired.",  # a number and a verb
        "The notice for the report id 41 is written exactly as the quote.",  # a number and the end
        "The expiry date is 2027-01-01 and the build is 1.2.3 under section 2.1.",  # a date, a version, a decimal
        "Sentence number 007 says every row is covered.",  # an id with a leading zero
        "Run `pytest -k '3 report formats'` and `render(rows, 3 formats)` once.",  # numbers inside code spans
    ],
)
def test_negative_no_trigger_in_numbers_that_are_no_count(sentence):
    assert needles(mkplan(sentence)) == []


@pytest.mark.parametrize(
    "sentence",
    [
        "None of the work in this task is large.",  # a negative word with no backticked phrase
        "None of `docs/guide.md` and `src/exporter/` is touched.",  # only paths
        "No remaining `grep -c 'x' docs/guide.md` call is needed.",  # only a command
        "No remaining `ab` text is left.",  # shorter than 3 characters
        "Move the count from 3 to 4 in the guide.",  # a count change with no noun
        "Move the count from 3 to 4 and from 8 to 9.",
    ],
)
def test_negative_a_trigger_without_a_search_string_gives_no_item(sentence):
    assert needles(mkplan(sentence)) == []


def test_negative_a_short_sentence_gives_no_item():
    assert needles(mkplan("None `abc`.")) == []  # under 12 characters, so no anchor


def test_negative_no_snapshot_means_no_evidence():
    doc = mkplan()
    (c,) = find(doc)
    assert c.evidence == [] and c.priority is None
    extractors.attach_e4([c], Ctx(doc))
    assert c.evidence == [] and c.priority == c.pre_priority == 50


def test_negative_with_zero_unnamed_hits_the_item_keeps_its_pre_priority(tmp_path):
    repo = zebra_repo(
        tmp_path, {"docs/a.md": None}
    )  # the only hit is in the file the plan names
    (c,) = run(mkplan("Edit `docs/a.md` so that it lists 7 zebra stripes."), repo)
    assert paths(c) == ["plan"]
    assert c.evidence[0]["text"] == "hits: 1 in 1 files (1 named by the plan)"
    assert (c.features["unnamed_root_hits"], c.features["unnamed_hits"]) == (0, 0)
    assert c.priority == c.pre_priority


def test_negative_dev_dependency_and_ground_truth_files_are_never_evidence(tmp_path):
    repo = zebra_repo(
        tmp_path,
        {
            ".dev/notes/z.md": None,
            "node_modules/pkg/z.js": None,
            "docs/ground-truth.json": None,
            "docs/progress.md": "nothing here\n",
        },
    )
    (c,) = run(
        mkplan("Edit `docs/progress.md` so that it lists 7 zebra stripes."), repo
    )
    assert paths(c) == ["plan"]
    assert c.evidence[0]["text"] == "hits: 0 in 0 files (0 named by the plan)"
    assert c.priority == c.pre_priority


def test_negative_a_needle_that_is_nowhere_in_the_repository(repo):
    (c,) = run(
        mkplan("Edit `docs/guide.md` so that it lists 99 unicorn stripes."), repo
    )
    assert (
        paths(c) == ["plan"]
        and c.evidence[0]["text"] == "hits: 0 in 0 files (0 named by the plan)"
    )


# ---------------------------------------------------------------- boundaries and near misses


@pytest.mark.parametrize(
    "sentence, expected",
    [
        ("The guide lists 3 report formats.", [("count", "3 report formats")]),
        (
            "The guide lists 3 report formats exist.",
            [("count", "3 report formats")],
        ),  # two words at most
        (
            "The guide has 3 formats and 4 sections.",
            [("count", "3 formats"), ("count", "4 sections")],
        ),
        ("The panel is a 5-member panel.", [("count", "5-member")]),
        (
            "Raise the limit from 12 to 14 entries.",
            [("count", "12 entries")],
        ),  # the noun after M
        ("Raise it from 12 retries to 14 retries.", [("count", "12 retries")]),
        (
            "Raise it from 3 report formats to 4 report formats.",
            [("count", "3 report formats")],
        ),
        (
            "Raise it 3 report formats to 4 report formats.",
            [("count", "3 report formats")],
        ),
        ("Keep 12 entries, then stop.", [("count", "12 entries")]),
        ("The count is 3 and the formats are fixed.", []),  # `and` is no noun
        ("The count is 3 to the power of 2.", []),  # `to the` is no noun phrase either
    ],
)
def test_boundary_count_triggers(sentence, expected):
    assert needles(mkplan(sentence)) == expected


def test_boundary_a_count_change_is_one_trigger_not_two():
    # "from 3 report formats to 4 report formats" holds two `N noun` phrases but one trigger
    cs = find(mkplan("Raise it from 3 report formats to 4 report formats."))
    assert len(cs) == 1


def test_boundary_a_negative_trigger_is_not_read_again_as_a_count():
    assert needles(mkplan("It prints 0 matches for `old banner`.")) == [
        ("negative", "old banner")
    ]


def test_boundary_the_negative_phrase_is_the_nearest_backticked_phrase():
    s = "Both `first phrase` and `second phrase` are kept, but none of `third phrase` remains."
    assert needles(mkplan(s)) == [("negative", "third phrase")]
    s = "No remaining `near phrase` is left, unlike the `far phrase` in the other place."
    assert needles(mkplan(s)) == [("negative", "near phrase")]


def test_boundary_two_triggers_in_one_sentence_give_two_items():
    s = "Move from 3 report formats to 4 report formats; none of `3 report formats` stays."
    assert needles(mkplan(s)) == [
        ("count", "3 report formats"),
        ("negative", "3 report formats"),
    ]


def test_boundary_blank_lines_split_blocks_so_a_label_line_is_not_part_of_the_sentence():
    doc = plan.parse(
        "## Task 1: A\n\nDepends on: Task 0\n\nUpdate the guide to 4 report formats.\n\n"
        "Acceptance criteria:\n- `make test` exits 0.\n"
    )
    (c,) = find(doc)
    assert (
        c.anchor_text == "Update the guide to 4 report formats."
        and c.location["line_start"] == 5
    )


@pytest.mark.parametrize(
    "needle_sentence, pre",
    [
        ("Keep a 3-member panel.", 30 + 10 + 0),  # one word, one digit
        ("Keep a 12-member panel.", 30 + 10 + 10),  # one word, two digits
        ("Keep 3 entries.", 30 + 10 + 10),  # two words ("3 entries")
        ("Keep 3 report formats.", 30 + 10 + 10),  # two words
        ("None of `x-y-z` remains in the file.", 30 + 0 + 0),  # one word, no digit
        ("None of `old text` remains in the file.", 30 + 0 + 10),
        ("None of `v12` remains in the file.", 30 + 0 + 10),  # one word, two digits
        ("None of `v1b` remains in the file.", 30 + 0 + 0),
    ],
)
def test_boundary_pre_priority_terms(needle_sentence, pre):
    (c,) = find(mkplan(needle_sentence))
    assert c.pre_priority == pre


def test_boundary_the_unnamed_term_stops_at_three_hits_and_evidence_holds_five_entries(
    tmp_path,
):
    files = {f"docs/n{i}.md": None for i in range(6)}
    repo = zebra_repo(tmp_path, files)
    doc = mkplan("Edit `src/exporter/report.py` so that it lists 7 zebra stripes.")
    (c,) = run(doc, repo)
    assert c.features["unnamed_hits"] == 6 and c.features["unnamed_root_hits"] == 0
    assert c.priority == c.pre_priority + 10 * 3  # 6 unnamed hits, the term stops at 3
    # 4 listed files and the `hits:` line: the 5 entries DESIGN 4.1 allows
    assert paths(c) == [f"docs/n{i}.md" for i in range(4)] + ["plan"]
    assert c.evidence[-1]["text"] == "hits: 6 in 6 files (0 named by the plan)"
    c.validate(Ctx(doc))


@pytest.mark.parametrize(
    "n, priority_add", [(0, 0), (1, 10), (2, 20), (3, 30), (4, 30)]
)
def test_boundary_unnamed_hit_term_per_count(tmp_path, n, priority_add):
    repo = zebra_repo(
        tmp_path, {**{f"docs/n{i}.md": None for i in range(n)}, "docs/a.md": None}
    )
    (c,) = run(mkplan("Edit `docs/a.md` so that it lists 7 zebra stripes."), repo)
    assert c.features["unnamed_hits"] == n
    assert c.priority == c.pre_priority + priority_add


def test_boundary_the_helper_keeps_three_lines_per_file_so_the_count_is_a_floor(
    tmp_path,
):
    repo = zebra_repo(tmp_path, {"docs/many.md": "7 zebra stripes\n" * 5})
    (c,) = run(mkplan("Edit `docs/a.md` so that it lists 7 zebra stripes."), repo)
    assert c.features["unnamed_hits"] == 3
    assert c.evidence[-1]["text"] == "hits: 3 in 1 files (0 named by the plan)"
    assert paths(c) == [
        "docs/many.md",
        "plan",
    ]  # one entry per file: its first hit line


def test_boundary_listing_order_root_documents_and_change_logs_then_mirrors_then_the_rest(
    tmp_path,
):
    repo = zebra_repo(
        tmp_path,
        {
            "docs/aa.md": None,
            "scripts/run.sh": None,
            "Makefile": "test:\n\t# 7 zebra stripes\n",
            "NOTES.md": None,
            "docs/CHANGELOG.md": None,
            MIRROR: None,
        },
    )
    doc = mkplan("Edit `src/exporter/report.py` so that it lists 7 zebra stripes.")
    (c,) = run(doc, repo)
    # 6 unnamed files; the 4 listed are: the root document, the change log (path order), the mirror, then the rest
    assert paths(c) == ["NOTES.md", "docs/CHANGELOG.md", MIRROR, "Makefile", "plan"]
    # only a root-level DOCUMENT counts for the bonus: NOTES.md, not docs/CHANGELOG.md or Makefile
    assert c.features["unnamed_root_hits"] == 1 and c.features["unnamed_hits"] == 6
    assert c.evidence[-1]["text"] == "hits: 6 in 6 files (0 named by the plan)"


def test_boundary_a_root_file_that_is_not_a_document_gets_no_root_bonus(tmp_path):
    repo = zebra_repo(
        tmp_path, {"Makefile": "test:\n\t# 7 zebra stripes\n", "docs/a.md": None}
    )
    (c,) = run(mkplan("Edit `docs/a.md` so that it lists 7 zebra stripes."), repo)
    assert (c.features["unnamed_root_hits"], c.features["unnamed_hits"]) == (0, 1)
    assert c.priority == c.pre_priority + 10


def test_boundary_one_batched_search_for_all_needles(repo, monkeypatch):
    calls = []
    real = extractors.search

    def spy(ctx, patterns, scope=None):
        calls.append(list(patterns))
        return real(ctx, patterns, scope)

    monkeypatch.setattr(extractors, "search", spy)
    run(plan.read(PLANS / "p_basic.md"), repo)
    assert calls == [["3 report formats"]]  # two items, one needle, one search
    calls.clear()
    run(
        mkplan(
            "Raise it from 3 report formats to 4 report formats and keep 12 entries."
        ),
        repo,
    )
    assert calls == [["12 entries", "3 report formats"]]


def test_boundary_long_sentence_anchor_is_a_prefix(repo):
    sentence = (
        "Raise the count from 3 report formats to 4 report formats "
        + "and then add more words " * 12
        + "here."
    )
    doc = mkplan(sentence)
    (c,) = run(doc, repo)
    assert len(c.anchor_text) == 200 and sentence.startswith(c.anchor_text)
    c.validate(Ctx(doc))


# ---------------------------------------------------------------- determinism


def test_determinism_on_p_basic_p_clean_and_the_doc_fixture(repo):
    for path, fmt in (
        (PLANS / "p_basic.md", None),
        (PLANS / "p_clean.md", None),
        (PLANS.parent / "docs" / "doc1.md", "doc"),
    ):
        doc = plan.read(path, fmt)
        assert dump(run(doc, repo, seed=1)) == dump(run(doc, repo, seed=1))
        assert dump(find(doc, repo, seed=1)) == dump(
            find(doc, repo, seed=2)
        )  # the seed only orders, in select


def test_determinism_does_not_depend_on_the_order_the_candidates_are_attached(repo):
    doc = plan.read(PLANS / "p_basic.md")
    ctx = Ctx(doc, snapshot=repo)
    one, two = extractors.find_e4(doc, ctx), extractors.find_e4(doc, ctx)
    extractors.attach_e4(one, ctx)
    extractors.attach_e4(list(reversed(two)), ctx)
    assert dump(one) == dump(two)


def test_attach_needs_only_the_candidate_and_ctx(repo):
    doc = mkplan()
    ctx = Ctx(doc, snapshot=repo)
    (c,) = extractors.find_e4(doc, ctx)
    copy = Candidate(
        c.extractor,
        c.cls,
        c.kind,
        c.anchor_text,
        dict(c.location),
        features=dict(c.features),
        pre_priority=c.pre_priority,
    )
    extractors.attach_e4([c], ctx)
    extractors.attach_e4([copy], Ctx(doc, snapshot=repo))
    assert dump([c]) == dump([copy])


# ---------------------------------------------------------------- the snapshot and the evidence rules


def test_non_git_snapshot_raises_in_attach(tmp_path):
    folder = tmp_path / "plain"
    folder.mkdir()
    doc = mkplan()
    ctx = Ctx(doc, snapshot=folder)
    cands = extractors.find_e4(doc, ctx)  # find needs no repository
    assert len(cands) == 1
    with pytest.raises(extractors.NotAGitRepo):
        extractors.attach_e4(cands, ctx)


def test_evidence_holds_no_claim_no_severity_no_defect(repo, tmp_path):
    docs = [
        (plan.read(PLANS / "p_basic.md"), repo),
        (plan.read(PLANS.parent / "docs" / "doc1.md", "doc"), repo),
        (mkplan(), repo),
        (mkplan(criterion=NEG), repo),
        (
            mkplan("Edit `src/exporter/report.py` so that it lists 7 zebra stripes."),
            zebra_repo(tmp_path / "z", {f"docs/n{i}.md": None for i in range(6)}),
        ),
    ]
    cands = [(doc, c) for doc, snap in docs for c in run(doc, snap)]
    assert len(cands) >= 5
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
        "stale",
    ):
        assert word not in blob
    for doc, c in cands:
        c.validate(
            Ctx(doc)
        )  # every limit of DESIGN 4.1: anchor, location, priority, at most 5 entries, 160 chars
        assert len(c.evidence) <= 5 and c.evidence[-1]["text"].startswith("hits: ")
        assert all(
            e["path"] == "plan" or not e["path"].startswith((".dev/", "node_modules/"))
            for e in c.evidence
        )


# ---------------------------------------------------------------- the registry


def test_registered_and_driven_by_run_extractors(repo):
    assert extractors.EXTRACTORS["E4"] == (extractors.find_e4, extractors.attach_e4)
    doc = plan.read(PLANS / "p_basic.md")
    ctx = Ctx(doc, snapshot=repo, seed=1)
    out = extractors.run_extractors(ctx, {"E4": extractors.EXTRACTORS["E4"]})
    assert [
        (c.cls, c.route, c.status, c.evidence_computed, c.priority) for c in out
    ] == [
        ("C5", "search", "attached", True, 90),
        ("C5", "search", "attached", True, 80),
    ]
