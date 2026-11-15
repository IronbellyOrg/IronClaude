"""REQ-28 (unit part): the `ran` cross-check over run folders built from F-REPORT-RL and F-TRANSCRIPT-RL
(fixtures/runs/make_ran_runs.py). File under test: analysis/ran_check.py. The expected statuses are worked out by hand
below, not by calling the module. No test writes RL/results/ran.md: every run of the command uses --out under tmp_path.
"""

import pytest

from analysis import ran_check as rc
from fixtures.runs import make_ran_runs as mk
from fixtures.transcripts import make_transcripts as tr

V, U, N = "verified", "unverified", "not_a_tool_claim"

# Each row of the seven runs, by hand (word = command word named in `ran`; call = a call that carries the word and shares
# a token of four or more letters outside the command words, or whose result holds quote_other):
EXPECTED = {
    # ran-1: the one call is Bash `grep -rn 'purge_keeps_held' tests/`, result SEARCH_HIT (tokens purge keeps held tests)
    (
        "ran-1",
        "C4.1",
    ): U,  # words printf, grep; the call shares no token (heading retention window) and no quote in its result
    (
        "ran-1",
        "C4.2",
    ): N,  # "literal pattern matches the ordered text": no command word, class C4
    ("ran-1", "C5.1"): U,  # word grep; tokens {count}: not in the call
    (
        "ran-1",
        "C6.1",
    ): U,  # C6 is a search recipe, no word: tokens {both scopes}: not in the call
    (
        "ran-1",
        "C8.1",
    ): V,  # words git, grep; "tests" is in `ran` and in the call, and the call has grep
    # ran-2: Bash `git grep -n 'retention_hold' -- tests docs`, empty result; every ran is "NONE FOUND: searched the plan for Cn shapes"
    ("ran-2", "C4.1"): N,  # no command word, class C4
    (
        "ran-2",
        "C5.1",
    ): U,  # search recipe, a search call exists, but no shared token (searched, shapes)
    ("ran-2", "C6.1"): U,
    ("ran-2", "C8.1"): U,
    # ran-3: no tool call at all
    ("ran-3", "C4.1"): N,
    ("ran-3", "C4.2"): N,  # "read the task text"
    ("ran-3", "C5.1"): U,  # NONE FOUND, search recipe, no search call at all
    ("ran-3", "C6.1"): U,
    ("ran-3", "C8.1"): U,
    # ran-4 (luna): codegraph_node (search tool, input exporter/retention.py) and Bash `ls tests` (not a search)
    ("ran-4", "C1.1"): N,  # "compared the two scopes"
    (
        "ran-4",
        "C2.1",
    ): U,  # words printf, grep; the search call shares no token with ran or the legal quote, result lacks the quote
    (
        "ran-4",
        "C3.1",
    ): N,  # "searched for a value read and never written": no command word
    # ran-5: Grep {pattern "retention window", path docs}
    (
        "ran-5",
        "C5.1",
    ): V,  # word grep; a search tool carries any word; "retention" and "window" are shared
    (
        "ran-5",
        "C8.1",
    ): U,  # a search call exists; tokens {mentions hold flag test}: none in the call
    # ran-6: one Read call, which is not a search
    ("ran-6", "C4.1"): U,  # word grep, no Bash call and no search tool call
    ("ran-6", "C6.1"): U,  # search recipe with no search call at all
    # ran-7 (luna): codegraph_node, result an array of text blocks that holds the quote_other of the row
    ("ran-7", "C2.1"): V,  # word grep; the result (array shape) contains quote_other
}


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    return mk.build(tmp_path_factory.mktemp("ran"))


@pytest.fixture(scope="module")
def rows(runs):
    return [r for d in runs for r in rc.check_run(d)]


def test_verified_unverified_and_not_a_tool_claim(rows):
    got = {(r["run"], r["item"]): r["status"] for r in rows}
    assert got == EXPECTED
    assert {V, U, N} == set(got.values())


def test_search_recipe_without_bash_is_unverified(rows):
    # a Read-only transcript (ran-6) and a transcript whose only Bash call is `ls` give no support to a search row
    ls_only = rc.calls_of(tr.run(tr.EMBER, [tr.bash("ls tests", "test_retention.py")]))
    assert [c["search"] for c in ls_only] == [False]
    row = {"item": "C6.1", "ran": "grep -rn tests for the hold flag", "quote_other": ""}
    assert rc.ran_status(row, ls_only) == U
    assert rc.ran_status(row, []) == U
    assert {r["status"] for r in rows if r["run"] == "ran-6"} == {U}
    # a search by a tool other than Bash does count (Task 1 decision)
    grep_tool = rc.calls_of(
        tr.run(tr.EMBER, [("tool", "Grep", {"pattern": "hold flag"}, "x")])
    )
    assert rc.ran_status(row, grep_tool) == V


def test_none_found_for_search_recipe_without_call_is_unverified(rows):
    by = {(r["run"], r["item"]): r for r in rows}
    for item in ("C5.1", "C6.1", "C8.1"):
        row = by["ran-3", item]
        assert row["ran"].startswith("NONE FOUND") and row["status"] == U
    # the same words on a recipe that is not a search recipe are not a tool claim
    assert by["ran-3", "C4.1"]["status"] == N
    # a call that exists but shares nothing leaves the NONE FOUND row unverified too (ran-2)
    assert [by["ran-2", i]["status"] for i in ("C5.1", "C6.1", "C8.1")] == [U, U, U]


def test_report_per_class_and_reviewer(runs, tmp_path):
    out = tmp_path / "out" / "ran.md"
    assert rc.main([str(runs[0].parent), "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "heuristic" in text.split("\n## ")[0]
    s = rc.summarise([r for d in runs for r in rc.check_run(d)])

    def c(v, u, n):
        return {"not_a_tool_claim": n, "verified": v, "unverified": u}

    # per reviewer: t2b-1 has ran-1 (5 rows: 1 V, 3 U, 1 N), ran-2 (4: 0, 3, 1), ran-5 (2: 1, 1, 0), ran-6 (2: 0, 2, 0)
    #   = 13 rows, V 2, U 9, N 2;  t4-1 has ran-3 (5: 0, 3, 2);  t3-1 has ran-4 (3: 0, 1, 2) and ran-7 (1: 1, 0, 0) = 4 rows
    assert s["per_reviewer"] == {
        "t2b-1": c(2, 9, 2),
        "t3-1": c(1, 1, 2),
        "t4-1": c(0, 3, 2),
    }
    # per class, from the table above: C1 1 N; C2 ran-4 U + ran-7 V; C3 1 N; C4 U (ran-1, ran-6) and N (ran-1 C4.2, ran-2,
    #   ran-3 twice); C5 U x3 (ran-1, 2, 3) + V (ran-5); C6 U x4 (ran-1, 2, 3, 6); C8 V (ran-1) + U x3 (ran-2, 3, 5)
    assert s["per_class"] == {
        "C1": c(0, 0, 1),
        "C2": c(1, 1, 0),
        "C3": c(0, 0, 1),
        "C4": c(0, 2, 4),
        "C5": c(1, 3, 0),
        "C6": c(0, 4, 0),
        "C8": c(1, 3, 0),
    }
    assert s["rows"] == 22 and s["total"] == c(
        3, 13, 6
    )  # 13 + 5 + 4 rows; V 2+0+1, U 9+3+1, N 2+2+2
    # search-recipe rows are C5, C6 and C8: 4 + 4 + 4 = 12, of which 3 + 4 + 3 = 10 are unverified
    assert (s["search_rows"], s["search_unverified"]) == (12, 10)
    assert s["search_unverified_share"] == pytest.approx(10 / 12)
    # table columns follow STATUSES: not_a_tool_claim, verified, unverified
    assert "| t2b-1 | 13 | 2 | 2 | 9 |" in text
    assert "| C6 | 4 | 0 | 0 | 4 |" in text
    assert "10 of 12 (0.833)" in text
