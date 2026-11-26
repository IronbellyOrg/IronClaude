"""Extractor core (DESIGN 4.1, DD-10, 5.1 step 2) and the repository search helper, on invented candidates.

The two-phase flow is tested with extractors defined in this file and handed to run_extractors (and, once, put
into the real registry with monkeypatch), so no real extractor is needed. Git runs only inside a repository built
by fixtures/repos/build_repo.py under /tmp.
"""

import hashlib
import json
import subprocess

import pytest

from fixtures.repos.build_repo import EDITED, SEARCH_STRINGS, _git, build_repo
from scaffold import cards
from sweep import extractors, plan
from sweep.extractors import Candidate, Ctx

N_SENTENCES = 40


def sentence(i):
    return f"Sentence number {i:03d} says every row is covered."


def make_doc():
    lines = ["# Plan", "", "## Task 1: demo", ""]
    lines += [sentence(i) for i in range(N_SENTENCES)]
    return plan.parse("\n".join(lines) + "\n")


def cand(eid, cls, i, pre, **over):
    return Candidate(
        extractor=eid,
        cls=cls,
        kind="test",
        anchor_text=sentence(i),
        location={"task": "T1", "line_start": 5 + i, "line_end": 5 + i},
        pre_priority=pre,
        **over,
    )


def registry(n_first=30, n_second=0, pre=lambda i: 3 * i):
    """Two local extractors: E1 finds n_first candidates of class C1, E2 finds n_second of class C4."""
    seen = {"E1": [], "E2": []}

    def finder(eid, cls, first, count):
        def find(doc, ctx):
            return [cand(eid, cls, first + i, pre(i)) for i in range(count)]

        def attach(batch, ctx):
            seen[eid].append([c.anchor_text for c in batch])
            for c in batch:
                c.evidence = [
                    {"path": "plan", "line": c.location["line_start"], "text": "hit"}
                ]
                c.priority = c.pre_priority + 5

        return find, attach

    reg = {"E1": finder("E1", "C1", 0, n_first)}
    if n_second:
        reg["E2"] = finder("E2", "C4", 30, n_second)
    return reg, seen


def run(reg, **kw):
    return extractors.run_extractors(Ctx(make_doc(), **kw), reg)


def attached(cands, cls):
    return [c for c in cands if c.cls == cls and c.evidence_computed]


def test_attach_only_for_top_k():
    reg, seen = registry(30, 5)
    ctx = Ctx(make_doc(), seed=1)
    assert (
        ctx.constants["K"] == 8 and ctx.constants["K_single"] == 12
    )  # config/values.json
    out = extractors.run_extractors(ctx, reg)
    c1 = [c for c in out if c.cls == "C1"]
    top = sorted(c1, key=lambda c: -c.pre_priority)[:8]
    assert len(c1) == 30
    assert {c.anchor_text for c in attached(out, "C1")} == {c.anchor_text for c in top}
    assert len(attached(out, "C4")) == 5  # fewer than K: all attached
    # attach never saw a candidate below the top K
    assert [len(b) for b in seen["E1"]] == [8] and [len(b) for b in seen["E2"]] == [5]
    for c in c1:
        if c.evidence_computed:
            assert (
                c.status == "attached"
                and c.evidence
                and c.priority == c.pre_priority + 5
            )
        else:
            assert c.status == "dropped:pre_rank" and c.evidence == []
            assert (
                c.anchor_text not in seen["E1"][0] and c.priority is None
            )  # no final rank


def test_single_class_attaches_top_12():
    reg, seen = registry(30)
    out = run(reg, seed=1)
    top = sorted(out, key=lambda c: -c.pre_priority)[:12]
    assert {c.anchor_text for c in attached(out, "C1")} == {c.anchor_text for c in top}
    assert [len(b) for b in seen["E1"]] == [
        12
    ]  # one attach call, bounded at 12 lookups
    assert sum(c.status == "dropped:pre_rank" for c in out) == 18


def test_k_values_come_from_the_constants():
    reg, _ = registry(30, 5)
    two = run(reg, constants={"K": 3, "K_single": 5})
    assert len(attached(two, "C1")) == 3 and len(attached(two, "C4")) == 3
    one = run(registry(30)[0], constants={"K": 3, "K_single": 5})
    assert len(attached(one, "C1")) == 5


def test_all_candidates_logged():
    for n_second, kept_first, dropped in ((5, 8, 22), (0, 12, 18)):
        reg, _ = registry(30, n_second)
        out = run(reg, seed=1)
        log = json.loads(json.dumps([c.to_dict() for c in out]))
        c1 = [e for e in log if e["class"] == "C1"]
        assert len(c1) == 30 and len(log) == 30 + n_second
        assert {e["anchor_text"] for e in c1} == {sentence(i) for i in range(30)}
        assert sum(e["status"] == "dropped:pre_rank" for e in c1) == dropped
        assert sum(e["evidence_computed"] for e in c1) == kept_first
        assert all(e["status"] and "evidence_computed" in e for e in log)
        assert all(e["status"] == "attached" for e in log if e["evidence_computed"])


def test_pre_rank_ties_earlier_line_then_seeded_hash():
    # all pre_priority equal: earlier plan line first
    reg, _ = registry(30, pre=lambda i: 50)
    out = run(reg, seed=1)
    assert {c.location["line_start"] for c in attached(out, "C1")} == set(range(5, 17))


def test_hash_breaks_a_tie_on_the_same_line():
    doc = make_doc()
    a, b = sentence(5), sentence(6)  # two anchors reported at one line and one priority

    def find(d, ctx):
        return [
            Candidate("E1", "C1", "k", t, {"task": "T1", "line_start": 9, "line_end": 9}, pre_priority=50)
            for t in (a, b)
        ]  # fmt: skip

    picks = set()
    for seed in range(1, 9):
        ctx = Ctx(doc, seed=seed, constants={"K": 1, "K_single": 1})
        out = extractors.run_extractors(ctx, {"E1": (find, lambda batch, c: None)})
        winner = next(x for x in out if x.evidence_computed)
        want = min(
            (a, b), key=lambda t: hashlib.sha256((str(seed) + t).encode()).hexdigest()
        )
        assert winner.anchor_text == want
        picks.add(winner.anchor_text)
    assert picks == {a, b}  # the seed really moves the pick


def test_route_is_copied_from_the_class_card():
    out = run(registry(30, 5)[0])
    routes = cards.routes()
    assert {c.route for c in out if c.cls == "C1"} == {routes["C1"]}
    assert {c.route for c in out if c.cls == "C4"} == {routes["C4"]}


def test_registered_pairs_are_used_when_no_registry_is_given(monkeypatch):
    reg, seen = registry(3)
    monkeypatch.setitem(extractors.EXTRACTORS, "E1", reg["E1"])
    out = extractors.run_extractors(Ctx(make_doc()))
    assert len(out) == 3 and seen["E1"]


@pytest.mark.parametrize(
    "mutate, why",
    [
        (lambda c: setattr(c, "anchor_text", "too short"), "characters"),
        (lambda c: setattr(c, "anchor_text", "x" * 201), "characters"),
        (lambda c: setattr(c, "anchor_text", "A sentence that the plan never wrote."), "exact quote"),
        (lambda c: setattr(c, "cls", "C9"), "class"),
        (lambda c: setattr(c, "pre_priority", 101), "pre_priority"),
        (lambda c: setattr(c, "evidence", [{"path": "plan", "line": 1, "text": "x"}] * 6), "evidence entries"),
        (lambda c: setattr(c, "evidence", [{"path": "plan", "line": 1, "text": "x" * 161}]), "evidence text"),
        (lambda c: setattr(c, "evidence", [{"path": "/etc/passwd", "line": 1, "text": "x"}]), "repo-relative"),
        (lambda c: setattr(c, "evidence", [{"path": "a", "line": 1}]), "evidence entry"),
        (lambda c: setattr(c, "location", {"task": "T1"}), "location"),
    ],
)  # fmt: skip
def test_candidate_limits_are_enforced(mutate, why):
    c = cand("E1", "C1", 0, 10)
    mutate(c)
    ctx = Ctx(make_doc())
    with pytest.raises(ValueError, match=why):
        c.validate(ctx)
    with pytest.raises(ValueError):
        extractors.run_extractors(ctx, {"E1": (lambda d, x: [c], lambda b, x: None)})


def test_find_must_return_its_own_extractor_id():
    with pytest.raises(ValueError, match="E2"):
        extractors.run_extractors(
            Ctx(make_doc()),
            {"E1": (lambda d, x: [cand("E2", "C1", 0, 1)], lambda b, x: None)},
        )


def test_priority_is_clamped_and_defaults_to_pre_priority():
    def attach(batch, ctx):
        batch[0].priority = 250

    reg = {
        "E1": (lambda d, x: [cand("E1", "C1", 0, 40), cand("E1", "C1", 1, 30)], attach)
    }
    a, b = run(reg)
    assert (a.priority, b.priority) == (100, 30)


# ---- the repository search helper ----

PLAN_TEXT = (
    f"## Task 1: Edit the exporter\n\nEdit `{EDITED}` to write 3 report formats.\n"
)


def repo_ctx(root, extra=None, text=PLAN_TEXT, seed=1):
    built = build_repo(root, extra=extra)
    return built, Ctx(plan.parse(text), snapshot=built.repo, seed=seed)


class Spy:
    """Records every `git grep` the helper starts (rev-parse and ls-files, which build the scope, are not grep)."""

    def __init__(self, monkeypatch):
        self.calls = []
        real = subprocess.Popen

        def popen(argv, **kw):
            if argv[3] == "grep":
                self.calls.append((list(argv), kw))
            return real(argv, **kw)

        monkeypatch.setattr(extractors.subprocess, "Popen", popen)


def test_search_runs_one_git_grep_with_the_designed_command(tmp_roots, monkeypatch):
    built, ctx = repo_ctx(tmp_roots.root)
    spy = Spy(monkeypatch)
    hits = extractors.search(ctx, ["report_exporter", "retention_policy"])
    assert hits
    ((argv, kw),) = spy.calls
    assert argv[:9] == [
        "git",
        "-C",
        str(built.repo),
        "grep",
        "-n",
        "-I",
        "-F",
        "--no-color",
        "-f",
    ]
    assert argv[10] == "--" and argv[11:] == list(ctx.scope.pathspecs)
    assert kw["env"]["LC_ALL"] == "C"
    assert not [k for k in kw["env"] if k.startswith("GIT_DIR") or k == "GIT_WORK_TREE"]
    assert not argv[9].startswith(
        str(built.repo)
    )  # the patterns file is scratch, outside the snapshot


def test_search_matched_pattern_is_the_first_given_that_the_line_holds(tmp_roots):
    _, ctx = repo_ctx(
        tmp_roots.root,
        extra={"tests/both.txt": "a retention_policy and report_exporter\n"},
    )
    for order in (
        ["report_exporter", "retention_policy"],
        ["retention_policy", "report_exporter"],
    ):
        both = [h for h in extractors.search(ctx, order) if h.path == "tests/both.txt"]
        assert [(h.line, h.pattern) for h in both] == [(1, order[0])]
    readme = [
        h for h in extractors.search(ctx, ["retention_policy"]) if h.path == "README.md"
    ]
    assert readme and all(
        h.pattern == "retention_policy" and "retention_policy" in h.text for h in readme
    )


def test_search_caps_three_hits_per_file(tmp_roots):
    _, ctx = repo_ctx(
        tmp_roots.root,
        extra={"tests/many.txt": "".join(f"needle {i}\n" for i in range(10))},
    )
    many = [h for h in extractors.search(ctx, ["needle"]) if h.path == "tests/many.txt"]
    assert [h.line for h in many] == [1, 2, 3]


def test_search_reads_only_the_first_5000_lines(tmp_roots):
    big = {
        f"tests/big_{i}.txt": "".join(f"needle {n}\n" for n in range(1000))
        for i in range(6)
    }
    _, ctx = repo_ctx(tmp_roots.root, extra=big)
    hits = extractors.search(ctx, ["needle"])
    # 5 files fill the 5,000 lines (3 hits kept from each); the 6th file is never read
    assert sorted({h.path for h in hits}) == [f"tests/big_{i}.txt" for i in range(5)]
    assert len(hits) == 15


def test_search_is_deterministic_and_ordered(tmp_roots):
    _, ctx = repo_ctx(tmp_roots.root)
    first = extractors.search(ctx, list(SEARCH_STRINGS))
    assert first == extractors.search(ctx, list(SEARCH_STRINGS))
    assert [(h.path, h.line) for h in first] == sorted((h.path, h.line) for h in first)


def test_search_ignores_empty_and_multiline_patterns(tmp_roots, monkeypatch):
    _, ctx = repo_ctx(tmp_roots.root)
    spy = Spy(monkeypatch)
    assert extractors.search(ctx, ["", "a\nb", "c\rd"]) == []
    assert spy.calls == []  # nothing usable: git grep is not started
    assert (
        extractors.search(ctx, ["no such string anywhere"]) == []
    )  # git exit 1 is "no match"


def test_non_git_snapshot_raises(tmp_path, tmp_roots):
    plain = tmp_path / "plain"
    plain.mkdir()
    (plain / "tests").mkdir()
    (plain / "tests" / "a.txt").write_text("needle\n")
    ctx = Ctx(plan.parse(PLAN_TEXT), snapshot=plain)
    with pytest.raises(extractors.NotAGitRepo):
        extractors.search(ctx, ["needle"])
    with pytest.raises(extractors.NotAGitRepo):
        extractors.search(ctx, [])  # no patterns does not hide it
    with pytest.raises(extractors.NotAGitRepo):
        ctx.scope  # noqa: B018
    with pytest.raises(extractors.NotAGitRepo):
        extractors.search(
            Ctx(plan.parse(PLAN_TEXT), snapshot=tmp_path / "missing"), ["needle"]
        )


def test_snapshot_inside_another_repository_raises(tmp_roots):
    built, _ = repo_ctx(tmp_roots.root)
    ctx = Ctx(
        plan.parse(PLAN_TEXT), snapshot=built.repo / "tests"
    )  # a folder of the repo, not its top
    with pytest.raises(extractors.NotAGitRepo):
        extractors.search(ctx, ["test_render"])


def test_no_snapshot_means_no_search():
    ctx = Ctx(make_doc())
    with pytest.raises(extractors.SearchError):
        extractors.search(ctx, ["needle"])
    assert ctx.scope_string == "no snapshot: no repository search"


def test_search_never_reads_outside_the_snapshot_root(tmp_roots):
    outside = tmp_roots.root / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("outside-secret needle\n")
    text = (
        PLAN_TEXT
        + "Also read ../outside/secret.txt and ../outside/ and ../../ for the rest.\n"
    )
    built, ctx = repo_ctx(tmp_roots.root, text=text)
    # a tracked symlink to a file outside the snapshot, and one to an outside folder
    (built.repo / "tests" / "link.txt").symlink_to(outside / "secret.txt")
    (built.repo / "docs" / "linkdir").symlink_to(outside)
    _git(built.repo, "add", "-f", "tests/link.txt", "docs/linkdir")
    _git(built.repo, "commit", "-q", "-m", "links")
    assert not any(
        p.startswith(("/", "..")) or ".." in p.split("/") for p in ctx.named_paths
    )
    assert extractors._clean_named("/etc/hosts") is None
    assert extractors._clean_named("a/../../b.py") is None
    assert extractors.search(ctx, ["outside-secret"]) == []
    assert all(
        not h.path.startswith(("/", ".."))
        for h in extractors.search(ctx, ["report_exporter"])
    )


def test_search_does_not_start_inside_a_redirected_git_dir(tmp_roots, monkeypatch):
    built, ctx = repo_ctx(tmp_roots.root)
    other = tmp_roots.root / "other"
    other.mkdir()
    (other / "tests").mkdir()
    (other / "tests" / "o.txt").write_text("report_exporter\n")
    _git(other, "init", "-q")  # a second repository
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(other))
    paths = {h.path for h in extractors.search(ctx, ["report_exporter"])}
    assert "README.md" in paths and "tests/o.txt" not in paths
