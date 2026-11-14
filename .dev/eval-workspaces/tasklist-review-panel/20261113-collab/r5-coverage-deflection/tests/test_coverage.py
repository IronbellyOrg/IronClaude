"""T-2 to T-7: task index, Task of a finding, surface filter, uncovered, declared not-checked, rank and cards."""
import hashlib

from conftest import AL, CT, DS, cand_text, finding, heading_anchor
from r5 import coverage as cov

PAT = cov.surface_pattern()


def test_task_index_real_candidates():  # T-2
    for pkg, n in ((DS, 13), (AL, 9), (CT, 12)):
        text = cand_text(pkg)
        idx = cov.task_index(text)
        assert len(idx) == n
        lines = text.splitlines()
        for tid, s, e in idx:
            assert lines[s].startswith(f"## Task {tid[1:]}:")
            assert e == len(lines) or lines[e].startswith("## ")
            assert not any(x.startswith("## ") for x in lines[s + 1:e])


def test_tasks_of():  # T-3
    text = cand_text(CT)
    idx = cov.task_index(text)
    a9 = heading_anchor(CT, "T9")
    assert cov.tasks_of(finding("F1", a9), text, idx) == {"T9"}
    constraints = next(line for line in text.splitlines()[17:27] if len(line.strip()) > 30).strip()[:40]
    assert cov.tasks_of(finding("F2", constraints), text, idx) == set()
    assert cov.tasks_of(finding("F3", a9, anchor2=heading_anchor(CT, "T3")), text, idx) == {"T9", "T3"}
    reflow = a9.replace(" ", "\n   ", 2)
    assert cov.tasks_of(finding("F4", reflow), text, idx) == {"T9"}
    assert cov.tasks_of(finding("F5", "this text is not in the candidate", refs=["Task 12"]), text, idx) == {"T12"}


SURFACE = [
    "Task 12 writes the artifact outside the permitted edit locations.",
    "The plan edits files under .claude/ which is outside the allowed paths.",
    "The sha256 of the candidate is not checked.",
    "The citation points at the wrong line number.",
    "The output path for the report is not stated.",
    "Edits under .claude/ break the edit scope rule.",
    "The recorded hash of the plan differs.",
    "The reference to lines 40-52 is stale.",
    "The log path is relative, not absolute.",
]
REAL = [
    "The single-select read-back compares the option name with a numeric value.",
    "The mode label conflicts with the rule that only two writes happen.",
    "The criterion says every flag is documented but lists no finite check.",
    "The worker-contract test is never updated though its exact-line table changes.",
    "The halt reason mapping drops the budget input.",
]


def test_surface_filter():  # T-4
    assert sum(cov.is_surface({"claim": c}, PAT) for c in SURFACE) == 9
    assert sum(cov.is_surface({"claim": c}, PAT) for c in REAL) == 0


def test_uncovered_surface_only():  # T-5
    text = cand_text(CT)
    idx = cov.task_index(text)
    a12 = heading_anchor(CT, "T12")
    assert "T12" not in cov.covered([finding("F1", a12, claim=SURFACE[0])], text, idx, PAT)
    assert "T12" in cov.covered([finding("F1", a12, claim=REAL[1])], text, idx, PAT)


def test_declared_not_checked():  # T-6
    assert cov.declared_not_checked("I did not check Tasks 3 and 7.") == {"T3", "T7"}
    assert cov.declared_not_checked("Tasks 3-5 were skipped.") == {"T3", "T4", "T5"}
    assert cov.declared_not_checked("I checked Task 2.") == set()
    rep = "## Findings block\n```findings-v1\n{\"claim\":\"Task 8 not checked\"}\n```\n"
    assert cov.declared_not_checked(rep) == set()


def test_rank_and_cards():  # T-7
    unc = {"T2", "T5", "T7", "T9"}
    r = cov.rank(unc, {"T9": 1, "T7": 2}, "row", "pkg")
    assert r[:2] == ["T7", "T9"]
    rest = sorted(["T2", "T5"], key=lambda t: hashlib.sha256(f"row/pkg/{t}".encode()).hexdigest())
    assert r[2:] == rest
    assert cov.rank(unc, {}, "row", "pkg") == cov.rank(unc, {}, "row", "pkg")
    # card 1, card 2 keeps still-uncovered card-1 Tasks then fills, dup card, k=0, empty
    c1 = cov.next_card({}, ["a", "b", "c"], {"a", "b", "c"}, 2, ["R"], 0)
    assert c1 == {"R": (["a", "b"], "post")}
    c2 = cov.next_card({"R": ["a", "b"]}, ["b", "c"], {"b", "c"}, 2, ["R"], 0)
    assert c2 == {"R": (["b", "c"], "post")}
    assert cov.next_card({"R": ["a", "b"]}, ["a", "b", "c"], {"a", "b", "c"}, 2, ["R"], 0)["R"] == (None, "dup_card")
    assert cov.next_card({}, ["a"], {"a"}, 0, ["R"], 0)["R"] == (None, "k0")
    assert cov.next_card({}, [], set(), 2, ["R"], 0)["R"] == (None, "nothing_uncovered")
    # EL2 deal
    d0 = cov.next_card({}, ["a", "b", "c", "d"], set("abcd"), 2, ["A", "B"], 0)
    assert d0 == {"A": (["a", "c"], "post"), "B": (["b", "d"], "post")}
    d1 = cov.next_card({}, ["a", "b", "c", "d"], set("abcd"), 2, ["A", "B"], 1)
    assert d1 == {"A": (["b", "d"], "post"), "B": (["a", "c"], "post")}
    # rendered card: only "Task <n>" tokens from the template, no count
    txt = cov.render_card(["T9", "T12"], 2, False)
    assert "Task 9, Task 12" in txt and "T9" not in txt
    template = (cov.cfg() / "templates" / "card-1.txt").read_text()
    assert txt == template.replace("{TASKS}", "Task 9, Task 12").replace("{K}", "2")
    assert "covered" not in txt.lower() and "nobody" not in txt.lower()
