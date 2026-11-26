"""Format dictionaries and word lists (DESIGN sections 3 and 4, REQ-37).

The first tests need no extractor. The last two (`test_spec_fixture_e1_e2_e5`, `test_doc_fixture_e4_e1`, REQ-37) run
the extractors over fixtures/specs/spec1.md with its parent parent1.md and over fixtures/docs/doc1.md.
"""

import ast
import hashlib
import inspect
import re

import pytest
from helpers import SW

from sweep import extractors, formats, plan, words
from sweep.extractors import Ctx

TICKET = {
    "heads": {
        "task": r"^###\s+Story\s+(?P<id>S-\d+)\s*:\s*(?P<title>.*)$",
        "constraint": r"^##\s+Rules\b",
        "gate": r"^##\s+Release gate\b",
    },
    "label": r"^Done when\s*:\s*$",
    "kinds": {
        "task": [{"mode": "task_body"}],
        "criterion": [{"mode": "after_label", "in": "task"}],
        "constraint": [{"mode": "bullets", "under": "constraint"}],
        "dictated_text": [{"mode": "blockquote", "in": "task", "part": "body"}],
        "edit_target": [
            {
                "mode": "sentences",
                "in": "task",
                "part": "body",
                "words": ["touch"],
                "verbs": ["touch"],
                "explode_paths": True,
            }
        ],
        "gate": [{"mode": "bullets", "under": "gate"}],
    },
}
TICKET_TEXT = """# Tickets

## Rules

- Every ticket names an owner.

### Story S-1: Export button

Touch `ui/export.js` and the button label.

> Export as CSV

Done when:
- the button shows the label
- the file downloads

## Release gate

- the smoke run is green
"""


def source_hash():
    return hashlib.sha256(inspect.getsource(plan).encode()).hexdigest()


def test_new_format_is_data_only(monkeypatch):
    """A dictionary added in a test is all a new format needs: no function of sweep/plan.py changes."""
    before = source_hash()
    assert "ticket" not in formats.FORMATS
    monkeypatch.setitem(formats.FORMATS, "ticket", TICKET)
    d = plan.parse(TICKET_TEXT, "ticket")
    assert d.format == "ticket"
    got = {k: [(b["id"], b["text"]) for b in d.of(k)] for k in plan.KINDS}
    assert got["task"] == [
        ("TS-1", "Touch `ui/export.js` and the button label.\n\n> Export as CSV")
    ]
    assert got["criterion"] == [
        ("TS-1.C1", "the button shows the label"),
        ("TS-1.C2", "the file downloads"),
    ]
    assert got["constraint"] == [("K1", "Every ticket names an owner.")]
    assert got["dictated_text"] == [("TS-1.D1", "Export as CSV")]
    assert got["edit_target"] == [
        ("TS-1.E1", "Touch `ui/export.js` and the button label.")
    ]
    assert got["gate"] == [("G1", "the smoke run is green")]
    assert d.of("edit_target")[0]["path"] == "ui/export.js"
    # the same dictionary passed directly reads the same, and the plan format still reads as before
    assert plan.parse(TICKET_TEXT, TICKET).blocks == d.blocks
    assert plan.parse((SW / "fixtures/plans/p_basic.md").read_bytes()).of("task")
    assert source_hash() == before
    # sweep/plan.py holds no format-specific text, and formats.py holds no code
    literals = {
        n.value
        for n in ast.walk(ast.parse(inspect.getsource(plan)))
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    }
    assert not literals & {"plan", "spec", "doc"}
    vocab = (
        "Acceptance criteria",
        "Task",
        "Phase",
        "Constraints",
        "Source sections",
        "Goal",
    )
    assert not [s for s in literals if any(v in s for v in vocab)]
    tree = ast.parse(inspect.getsource(formats))
    assert not [
        n
        for n in ast.walk(tree)
        if isinstance(
            n, ast.FunctionDef | ast.ClassDef | ast.Lambda | ast.Import | ast.ImportFrom
        )
    ]


def test_every_format_names_known_kinds_and_modes():
    assert set(formats.FORMATS) >= {"plan", "spec", "doc"}
    assert formats.DEFAULT in formats.FORMATS
    for name, spec in formats.FORMATS.items():
        assert set(spec["kinds"]) <= set(plan.KINDS), name
        assert "task" in spec["heads"], name
        for rx in spec["heads"].values():
            re.compile(rx)
        for rules in spec["kinds"].values():
            for rule in rules:
                assert rule["mode"] in plan.MODES, (name, rule)
                for key in ("pattern", "label"):
                    if key in rule:
                        re.compile(rule[key])
                if rule["mode"] in ("bullets", "section"):
                    assert rule["under"] in spec["heads"], (name, rule)
    for rx in (formats.PATH_TOKEN, formats.SENTENCE_END, *formats.QUOTED_SPANS):
        re.compile(rx)


def test_the_plan_dictionary_names_every_part_of_the_workflow_plan_format():
    spec = formats.FORMATS["plan"]
    for cls in ("phase", "task", "constraint", "gate"):
        assert cls in spec["heads"]
    assert (
        "Acceptance criteria" in spec["label"]
        and "Source sections" in spec["citation"]["label"]
    )
    assert set(spec["kinds"]) == set(plan.KINDS)


def test_word_lists_are_lower_case_tuples_without_repeats():
    assert set(words.LISTS) == {
        "set_completeness",
        "set_universal",
        "limiters",
        "edit_verbs",
        "create_verbs",
        "dictation_verbs",
        "ordering_verbs",
        "stop",
    }
    for name, lst in words.LISTS.items():
        assert isinstance(lst, tuple) and lst, name
        assert list(lst) == [w.lower().strip() for w in lst], name
        assert len(set(lst)) == len(lst), name


def test_word_lists_hold_the_design_words():
    need = {
        "set_completeness": "every all each complete completely exhaustive exhaustively found covers cover".split()
        + ["no remaining"],
        "set_universal": ["only", "never", "no other"],
        "limiters": "skip ignore exempt allow-list only except unless excluding".split(),
        "edit_verbs": "edit update modify change rewrite rename delete remove replace extend create".split(),
        "dictation_verbs": "write state say wording verbatim exact".split()
        + ["must contain"],
        "ordering_verbs": "add write create insert rename name heading title section label".split(),
    }
    for name, want in need.items():
        assert set(want) <= set(words.LISTS[name]), name
    assert ("outside", "nothing") in words.SET_UNIVERSAL_PAIRS
    assert set(words.CREATE_VERBS) & set(words.EDIT_VERBS) >= {"create", "created"}
    assert "add a new" in words.CREATE_VERBS
    assert all(len(w) >= 4 for w in words.STOP)


@pytest.mark.parametrize(
    "sentence,found",
    [
        ("Edit the file.", True),
        ("The edited file.", True),
        ("Unchanged text.", False),
        ("Add a new test.", False),
    ],
)
def test_word_matching_is_on_word_boundaries(sentence, found):
    assert bool(plan._wre("edit_verbs").search(sentence)) is found


# ---------------------------------------------------------------- spec and documentation fixtures (REQ-37)

SPEC = SW / "fixtures" / "specs" / "spec1.md"
PARENT = SW / "fixtures" / "specs" / "parent1.md"
DOC = SW / "fixtures" / "docs" / "doc1.md"


def items(eid, doc, ctx):
    """The candidates of one extractor, with the evidence of its `attach` and the core limits checked."""
    find, attach = extractors.EXTRACTORS[eid]
    cands = find(doc, ctx)
    attach(cands, ctx)
    for c in cands:
        assert c.extractor == eid
        c.validate(ctx)
    return cands


def test_spec_fixture_e1_e2_e5():
    spec = plan.read(SPEC, "spec")
    parent = plan.read(PARENT, "spec")
    assert spec.format == "spec" and [t for t in spec.tasks] == ["T1", "T2", "T3"]
    assert spec.tasks["T2"]["citations"] == ["4.1", "4.2"]
    ctx = Ctx(spec, source=parent)
    got = {eid: items(eid, spec, ctx) for eid in ("E1", "E2", "E5")}
    assert all(got.values()), {k: len(v) for k, v in got.items()}
    # E5 reads the parent: the door rule names `door_open_ms` and `DoorTimeout`, which task 2 does not carry
    assert any(
        {"door_open_ms", "DoorTimeout"} <= set(c.features["missing"]) for c in got["E5"]
    )
    assert ctx.tasks_without_citations == ["T1"]
    # no parent, no E5 item; the other two still read the spec alone
    alone = Ctx(spec)
    assert items("E5", spec, alone) == []
    assert alone.not_applicable == {"C2": "no_source"}
    assert items("E1", spec, alone) and items("E2", spec, alone)


def test_doc_fixture_e4_e1():
    doc = plan.read(DOC, "doc")
    assert doc.format == "doc"
    ctx = Ctx(doc)
    got = {eid: items(eid, doc, ctx) for eid in ("E4", "E1")}
    assert all(got.values()), {k: len(v) for k, v in got.items()}
    assert any("3 report formats" in c.features["needle"] for c in got["E4"])
    assert {c.kind for c in got["E1"]} >= {"universal"}
