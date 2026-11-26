"""Extractor E2 (class C4, DESIGN 4.3): a literal pattern against the text the plan orders.

Each extractor test has a positive case, a negative case, a near-miss case and a determinism case. `find_e2` is
lexical; `attach_e2` reads the snapshot built by fixtures/repos/build_repo.py under /tmp (git runs there only).
"""

import json
from pathlib import Path

import pytest

from fixtures.repos.build_repo import build_repo
from sweep import extractors, plan
from sweep.extractors import Ctx

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
ORDER_SENTENCE = 'Edit `docs/ops.md` and add the heading "Retry policy" to it.'
TESTS_FILE = """import pytest


def test_purge_keeps_held():
    pass


def test_purge_removes_expired():
    pass


@pytest.mark.slow
def test_scan_everything():
    pass


class TestNotice:
    def test_notice_text(self):
        pass
"""


def mkplan(criterion, ordered=ORDER_SENTENCE):
    """A one-task plan: line 3 is the ordering sentence and line 6 the criterion bullet."""
    return plan.parse(
        f"## Task 1: Document the policy\n\n{ordered}\n\nAcceptance criteria:\n- {criterion}\n"
    )


def find(doc, **kw):
    return extractors.find_e2(doc, Ctx(doc, **kw))


def run(doc, snapshot=None, **kw):
    """find, then attach the candidates (all of them: the tests here have few)."""
    ctx = Ctx(doc, snapshot=snapshot, **kw)
    cands = extractors.find_e2(doc, ctx)
    extractors.attach_e2(cands, ctx)
    return cands


@pytest.fixture
def repo(tmp_path):
    return build_repo(
        tmp_path,
        extra={
            "docs/ops.md": "# Operations\n\n## Retry policy\n\nRetries stop after three attempts.\n",
            "tests/test_retention.py": TESTS_FILE,
        },
    ).repo


def texts(c):
    return [e["text"] for e in c.evidence]


# ---------------------------------------------------------------- positive: the pattern matches the ordered string


def test_positive_literal_match_is_a_low_priority_pair(repo):
    (c,) = run(mkplan("`grep -ci 'retry policy' docs/ops.md` prints at least 1."), repo)
    assert (c.extractor, c.cls, c.kind) == ("E2", "C4", "pattern")
    assert c.features["no_match"] == 0 and c.features["near_miss"] == 0
    assert c.features["pattern_kind"] == "literal"
    assert c.pre_priority == 25 and c.priority == 25
    assert c.anchor_text == "`grep -ci 'retry policy' docs/ops.md` prints at least 1."
    assert c.location == {"task": "T1", "line_start": 6, "line_end": 6}
    assert texts(c) == [
        'the task orders the heading "Retry policy"',
        "pattern 'retry policy' (case-insensitive) against ordered string 'Retry policy': MATCH",
        "base checkout: git grep -c -F -e 'retry policy' -- docs/ops.md gives 0",
    ]
    assert [(e["path"], e["line"]) for e in c.evidence] == [
        ("plan", 3),
        ("plan", 3),
        ("docs/ops.md", 0),
    ]


def test_no_match_without_a_near_miss_ranks_70():
    (c,) = find(mkplan("`grep -c 'retry limit' docs/ops.md` prints at least 1."))
    assert c.features["no_match"] == 1 and c.features["near_miss"] == 0
    assert c.pre_priority == 25 + 45 == 70
    (c2,) = run(mkplan("`grep -c 'retry limit' docs/ops.md` prints at least 1."))
    assert c2.priority == 70
    assert texts(c2)[1].endswith(": NO MATCH")


# ---------------------------------------------------------------- near miss: MATCH only after collapsing


def test_near_miss_heading_matches_only_after_collapsing(repo):
    doc = mkplan("`grep -c 'retry-policy' docs/ops.md` prints at least 1.")
    (c,) = run(doc, repo)
    assert c.features["no_match"] == 1 and c.features["near_miss"] == 1
    assert c.pre_priority == 25 + 45 + 20 == 90 and c.priority == 90
    # the evidence lines of DESIGN 4.3, in the order the example prints them
    assert texts(c) == [
        'the task orders the heading "Retry policy"',
        "pattern 'retry-policy' (case-sensitive) against ordered string 'Retry policy': NO MATCH",
        "after lowercasing and collapsing hyphens, spaces and underscores: MATCH",
        "base checkout: git grep -c -F -e 'retry-policy' -- docs/ops.md gives 0",
    ]
    assert c.evidence[0] == {
        "path": "plan",
        "line": 3,
        "text": 'the task orders the heading "Retry policy"',
    }


@pytest.mark.parametrize(
    "pattern, string",
    [
        ("retry_policy", "Retry policy"),
        ("RETRY-POLICY", "Retry policy"),
        ("retry  policy", "Retry-Policy"),
        ("retry-policy", "retry_policy"),
    ],
)
def test_near_miss_collapsing_rule(pattern, string):
    ordered = f'Edit `docs/ops.md` and add the heading "{string}" to it.'
    (c,) = find(mkplan(f"`grep -c '{pattern}' docs/ops.md` prints 1.", ordered))
    assert c.features["near_miss"] == 1 and c.pre_priority == 90


def test_a_literal_hit_is_not_a_near_miss():
    (c,) = find(mkplan("`grep -c 'Retry policy' docs/ops.md` prints 1."))
    assert c.features["near_miss"] == 0 and c.features["no_match"] == 0


# ---------------------------------------------------------------- negative: nothing to extract


@pytest.mark.parametrize(
    "criterion",
    [
        "`make test` exits 0.",
        "`test_notice_text` passes and `src/exporter/notice.py` exists.",
        "`pytest tests/test_retention.py -q` exits 0.",  # no selector
        "`pytest tests/` exits 0.",
        "`test -f docs/ops.md` exits 0.",  # `test` without a grep inside
        "`grep -c 'unrelated words' docs/ops.md` prints 1.",  # nothing the plan orders shares a word with it
        "`grep -f patterns.txt docs/ops.md` prints 1.",  # patterns from a file are computed
        '`grep -c "$PATTERN" docs/ops.md` prints 1.',  # so are patterns from the shell
        "`grep -c 'retry-policy` docs/ops.md prints 1.",  # unbalanced quotes
        "`rg --files docs` lists the file.",
        "The heading is `Retry policy` and the file is `docs/ops.md`.",
    ],
)
def test_negative_nothing_extracted(criterion):
    assert find(mkplan(criterion)) == []


def test_negative_strings_that_are_not_ordered():
    # the sentence holds no ordering verb, a string of a later task, and a path-like backticked span
    cmd = "`grep -c 'retry-policy' docs/ops.md` prints 1."
    assert find(mkplan(cmd, 'The page shows "Retry policy" today.')) == []
    later = (
        "## Task 1: Check\n\nRun the check.\n\nAcceptance criteria:\n"
        f"- {cmd}\n\n## Task 2: Docs\n\n{ORDER_SENTENCE}\n\nAcceptance criteria:\n- The page exists.\n"
    )
    assert find(plan.parse(later)) == []
    assert (
        find(
            mkplan(
                "`grep -c 'ops.md' docs/ops.md` prints 1.",
                "Add `docs/ops.md` to the tree.",
            )
        )
        == []
    )


def test_negative_short_anchor_is_skipped():
    assert (
        find(mkplan("`grep -c a x`")) == []
    )  # the whole bullet is under 12 characters


def test_earlier_task_strings_are_used_and_the_goal_sees_every_task():
    text = (
        "Goal: `grep -c 'retry-policy' docs/ops.md` prints 1.\n\n"
        f"## Task 1: Docs\n\n{ORDER_SENTENCE}\n\nAcceptance criteria:\n- The page exists.\n\n"
        "## Task 2: Check\n\nRun the check.\n\nAcceptance criteria:\n"
        "- `grep -c 'retry-policy' docs/ops.md` prints 1.\n"
    )
    cands = find(plan.parse(text))
    assert [(c.location["task"], c.pre_priority) for c in cands] == [
        (None, 90),
        ("T2", 90),
    ]


# ---------------------------------------------------------------- the literal test and the command flags


def pair(criterion, ordered=ORDER_SENTENCE):
    (c,) = find(mkplan(criterion, ordered))
    return c


def test_flags_fixed_ignore_case_whole_word():
    s = 'Edit `docs/ops.md` and add the heading "a.b Retry policy2" to it.'
    assert pair("`grep -F 'a.b' docs/ops.md` prints 1.", s).features["no_match"] == 0
    assert (
        pair("`grep 'a.b' docs/ops.md` prints 1.", s).features["pattern_kind"]
        == "regex"
    )
    assert (
        pair("`grep -c 'retry policy' docs/ops.md` prints 1.", s).features["no_match"]
        == 1
    )
    assert (
        pair("`grep -ci 'retry policy' docs/ops.md` prints 1.", s).features["no_match"]
        == 0
    )
    assert (
        pair("`grep -wi 'retry policy' docs/ops.md` prints 1.", s).features["no_match"]
        == 1
    )  # policy2
    assert (
        pair("`grep -wi 'retry policy2' docs/ops.md` prints 1.", s).features["no_match"]
        == 0
    )
    assert (
        pair("`grep -e 'a.b' -e x docs/ops.md` prints 1.", s).features["pattern"]
        == "a.b"
    )


def test_basic_and_extended_syntax():
    s = 'Edit `docs/ops.md` and add the heading "retry policy" to it.'
    # basic syntax: `\|` and `\(` are operators, a bare `|` and `+` are plain characters
    assert (
        pair(r"`grep 'retry\|nothing' docs/ops.md` prints 1.", s).features["no_match"]
        == 0
    )
    assert (
        pair(r"`grep 'policy\(x\)*' docs/ops.md` prints 1.", s).features["no_match"]
        == 0
    )
    assert (
        pair("`grep 'retry|policy' docs/ops.md` prints 1.", s).features["no_match"] == 1
    )
    assert pair("`grep 'retry+' docs/ops.md` prints 1.", s).features["no_match"] == 1
    # extended syntax (-E, egrep, rg): the same characters are operators
    for cmd in ("grep -E", "egrep", "rg"):
        c = pair(f"`{cmd} 'retry+|nothing' docs/ops.md` prints 1.", s)
        assert c.features["pattern_kind"] == "regex" and c.features["no_match"] == 0, (
            cmd
        )
    assert (
        pair("`grep '[[:alpha:]]* policy' docs/ops.md` prints 1.", s).features[
            "no_match"
        ]
        == 0
    )
    assert (
        pair("`grep -c '^retry policy$' docs/ops.md` prints 1.", s).features["no_match"]
        == 0
    )
    assert (
        pair("`grep -c '^policy' docs/ops.md` prints 1.", s).features["no_match"] == 1
    )


def test_unparsable_regex_has_no_match_line():
    doc = mkplan("`grep -c 'retry[a' docs/ops.md` prints 1.")
    (c,) = run(doc)
    assert c.features["pattern_kind"] == "regex_unparsed"
    assert (
        c.features["no_match"] == 0
        and c.features["near_miss"] == 0
        and c.pre_priority == 25
    )
    assert texts(c) == ['the task orders the heading "Retry policy"']
    long_pattern = "retry " + "x*" * 120
    c = pair(f"`grep -c '{long_pattern}' docs/ops.md` prints 1.")
    assert c.features["pattern_kind"] == "regex_unparsed"


@pytest.mark.parametrize(
    "cmd",
    [
        "grep -c 'retry policy' docs/ops.md",
        "egrep -c 'retry policy' docs/ops.md",
        "rg -c 'retry policy' docs/ops.md",
        "git grep -c 'retry policy' -- docs/ops.md",
        "grep -c 'retry policy' docs/ops.md | wc -l",
        "grep -c 'retry policy' docs/ops.md > /dev/null",
        "test \"$(grep -c 'retry policy' docs/ops.md)\" -ge 1",
    ],
)
def test_command_families(cmd):
    c = pair(f"`{cmd}` is run.")
    assert c.features["pattern"] == "retry policy" and c.features["paths"] == [
        "docs/ops.md"
    ]


def test_paths_are_repo_relative_only():
    c = pair(
        "`grep -c 'retry policy' /etc/passwd ../x.md ./docs/ops.md $HOME/y docs/*.md` is run."
    )
    assert c.features["paths"] == ["docs/ops.md"]


# ---------------------------------------------------------------- attach: the base checkout, never outside it


def test_base_checkout_count_skips_dev_and_dependency_noise(tmp_path):
    repo = build_repo(tmp_path).repo
    ordered = 'Add the name "report_exporter" to the plan.'
    doc = mkplan("`grep -rc 'report_exporter' .` prints 2.", ordered)
    (c,) = run(doc, repo)
    # README.md and scripts/export.sh hold it once each; .dev/, node_modules/ and ground-truth.json are left out
    assert (
        texts(c)[-1]
        == "base checkout: git grep -c -F -e 'report_exporter' -- . gives 2"
    )
    assert c.evidence[-1]["path"] == "."


def test_attach_without_a_snapshot_or_a_file_never_raises(repo):
    doc = mkplan("`grep -c 'retry-policy' docs/missing.md` prints 1.")
    (c,) = run(doc)  # no snapshot: no base-checkout line
    assert len(c.evidence) == 3
    (c,) = run(doc, repo)  # a path that is not in the snapshot counts 0
    assert texts(c)[-1].endswith("-- docs/missing.md gives 0")
    sel = mkplan("`pytest tests/test_absent.py -k purge` exits 0.")
    (c,) = run(
        sel, repo
    )  # no count of test names; the base-checkout line is information only
    assert texts(c) == [
        "base checkout: git grep -c -F -e 'purge' -- tests/test_absent.py gives 0"
    ]
    assert c.priority == 25
    (c,) = run(sel)
    assert c.evidence == [] and c.priority == 25


def test_non_git_snapshot_raises(tmp_path):
    folder = tmp_path / "plain"
    folder.mkdir()
    doc = mkplan("`grep -c 'retry-policy' docs/ops.md` prints 1.")
    ctx = Ctx(doc, snapshot=folder)
    with pytest.raises(extractors.NotAGitRepo):
        extractors.attach_e2(extractors.find_e2(doc, ctx), ctx)


# ---------------------------------------------------------------- selectors, counted with ast


def selector(cmd, repo):
    (c,) = run(mkplan(f"`{cmd}` exits 0."), repo)
    return c


def test_selector_k_counts_test_names(repo):
    c = selector("pytest tests/test_retention.py -k purge_keeps_held", repo)
    assert c.kind == "selector" and c.pre_priority == 25 and c.priority == 25
    assert c.features["no_match"] == 0 and c.features["near_miss"] == 0
    assert texts(c) == [
        "1 of 4 test names in tests/test_retention.py match the selector",
        "base checkout: git grep -c -F -e 'purge_keeps_held' -- tests/test_retention.py gives 1",
    ]
    assert c.evidence[0]["path"] == "tests/test_retention.py"
    assert (
        selector("pytest tests/test_retention.py -k purge", repo)
        .evidence[0]["text"]
        .startswith("2 of 4")
    )
    assert (
        selector("pytest tests/test_retention.py -k 'purge and not removes'", repo)
        .evidence[0]["text"]
        .startswith("1 of 4")
    )
    assert (
        selector("pytest tests/test_retention.py -k 'notice or scan'", repo)
        .evidence[0]["text"]
        .startswith("2 of 4")
    )
    # the module name is a keyword too: `-k test_retention` picks every test of the file
    assert (
        selector("pytest tests/test_retention.py -k test_retention", repo)
        .evidence[0]["text"]
        .startswith("4 of 4")
    )


def test_selector_m_and_id(repo):
    assert (
        selector("pytest tests/test_retention.py -m slow", repo)
        .evidence[0]["text"]
        .startswith("1 of 4")
    )
    assert (
        selector("pytest tests/test_retention.py -m 'not slow'", repo)
        .evidence[0]["text"]
        .startswith("3 of 4")
    )
    assert (
        selector("pytest tests/test_retention.py::test_notice_text", repo)
        .evidence[0]["text"]
        .startswith("0 of 4")
    )
    assert (
        selector("pytest tests/test_retention.py::TestNotice::test_notice_text", repo)
        .evidence[0]["text"]
        .startswith("1 of 4")
    )
    assert (
        selector("pytest tests/test_retention.py::TestNotice", repo)
        .evidence[0]["text"]
        .startswith("1 of 4")
    )
    assert (
        selector("pytest -x tests/test_retention.py::test_scan_everything[a-1]", repo)
        .evidence[0]["text"]
        .startswith("1 of 4")
    )


def test_selector_with_zero_matches_adds_5(repo):
    c = selector("pytest tests/test_retention.py -k no_such_test", repo)
    assert (
        texts(c)[0] == "0 of 4 test names in tests/test_retention.py match the selector"
    )
    assert c.pre_priority == 25 and c.priority == 30


def test_selector_file_that_does_not_parse_gives_no_count(tmp_path):
    repo = build_repo(tmp_path, extra={"tests/test_broken.py": "def test_x(:\n"}).repo
    c = selector("pytest tests/test_broken.py -k x", repo)
    assert c.evidence == [] or "test names" not in c.evidence[0]["text"]
    assert c.priority == 25


def test_selector_in_a_file_that_is_not_python_uses_the_def_regex(tmp_path):
    repo = build_repo(
        tmp_path,
        extra={"tests/check.txt": "def test_a():\n def test_b():\ndef helper():\n"},
    ).repo
    c = selector("pytest tests/check.txt -k test_a", repo)
    assert texts(c)[0] == "1 of 2 test names in tests/check.txt match the selector"


def test_selector_is_never_read_outside_the_snapshot(tmp_path, repo):
    secret = tmp_path / "outside.py"
    secret.write_text("def test_secret():\n    pass\n")
    link = repo / "tests" / "test_link.py"
    link.symlink_to(secret)
    c = selector("pytest tests/test_link.py -k secret", repo)
    assert c.evidence == [] or "test names" not in c.evidence[0]["text"]


# ---------------------------------------------------------------- the two plan fixtures, and determinism


def dump(cands):
    return json.dumps([c.to_dict() for c in cands], sort_keys=True)


def test_p_basic_emits_the_pattern_and_the_selector(tmp_path):
    doc = plan.read(PLANS / "p_basic.md")
    repo = build_repo(tmp_path).repo
    cands = run(doc, repo, seed=1)
    assert [(c.kind, c.location["task"], c.pre_priority) for c in cands] == [
        ("pattern", "T2", 90),
        ("selector", "T3", 25),
    ]
    near = cands[0]
    assert near.features["near_miss"] == 1
    assert texts(near) == [
        'the task orders the heading "Retention window"',
        "pattern 'retention-window' (case-sensitive) against ordered string 'Retention window': NO MATCH",
        "after lowercasing and collapsing hyphens, spaces and underscores: MATCH",
        "base checkout: git grep -c -F -e 'retention-window' -- docs/guide.md gives 0",
    ]
    assert near.evidence[0]["line"] == 40  # the plan line that orders the heading
    assert cands[
        1
    ].evidence == [  # tests/test_retention.py does not exist at the base commit
        {
            "path": "tests/test_retention.py",
            "line": 0,
            "text": "base checkout: git grep -c -F -e 'purge_keeps_held' -- tests/test_retention.py gives 0",
        }
    ]


def test_p_clean_emits_nothing(tmp_path):
    doc = plan.read(PLANS / "p_clean.md")
    assert find(doc) == []
    assert run(doc, build_repo(tmp_path).repo) == []


def test_determinism_on_p_basic_and_p_clean(tmp_path):
    repo = build_repo(tmp_path).repo
    for name in ("p_basic.md", "p_clean.md"):
        doc = plan.read(PLANS / name)
        assert dump(run(doc, repo, seed=1)) == dump(run(doc, repo, seed=1))
        assert dump(find(doc, seed=1)) == dump(
            find(doc, seed=2)
        )  # the seed only orders, in select


def test_evidence_holds_no_claim_no_severity_no_defect(repo):
    basic = plan.read(PLANS / "p_basic.md")
    docs = [
        basic,
        mkplan("`grep -c 'retry-policy' docs/ops.md` prints at least 1."),
        mkplan("`pytest tests/test_retention.py -k no_such_test` exits 0."),
    ]
    cands = [(doc, c) for doc in docs for c in run(doc, repo)]
    blob = " ".join(e["text"] for _, c in cands for e in c.evidence).lower()
    assert blob
    for word in ("defect", "severity", "blocking", "wrong", "bug"):
        assert word not in blob
    for doc, c in cands:
        c.validate(
            Ctx(doc)
        )  # every limit of DESIGN 4.1: anchor, location, priority, at most 5 entries, 160 chars


# ---------------------------------------------------------------- the registry


def test_registered_and_driven_by_run_extractors(tmp_path):
    assert extractors.EXTRACTORS["E2"] == (extractors.find_e2, extractors.attach_e2)
    doc = plan.read(PLANS / "p_basic.md")
    ctx = Ctx(doc, snapshot=build_repo(tmp_path).repo, seed=1)
    out = [
        c for c in extractors.run_extractors(ctx, {"E2": extractors.EXTRACTORS["E2"]})
    ]
    assert [
        (c.cls, c.route, c.status, c.evidence_computed, c.priority) for c in out
    ] == [
        ("C4", "search", "attached", True, 90),
        ("C4", "search", "attached", True, 25),
    ]
    clean = extractors.run_extractors(
        Ctx(plan.read(PLANS / "p_clean.md")), {"E2": extractors.EXTRACTORS["E2"]}
    )
    assert clean == []
