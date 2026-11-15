"""REQ-37: the lens and the brief render for a specification target (with its parent as the source) and for a
documentation target (no source). Recipe Ledger has no extractors, so the test is that every recipe that applies
is present, C2 only with a source (DR-7), and every lens keeps at least 2 recipes."""

import hashlib

import pytest
from helpers import SW
from rl_support import B_MIN, CLASSES, PANELS, VALUES, recipe_paragraphs

from rl import lens, render

SPEC = SW / "fixtures" / "specs" / "spec1.md"
PARENT = SW / "fixtures" / "specs" / "parent1.md"
DOC_FIXTURE = SW / "fixtures" / "docs" / "doc1.md"
LENSES = SW / "config" / "lenses.json"


def doc_of(path):
    return {"cand_sb": str(path), "sha": hashlib.sha256(path.read_bytes()).hexdigest()}


def build(panel, candidate, source):
    """(lens roles, {role: brief}, run.json fields) of one panel for one target."""
    roles = lens.render(panel, bool(source), B_MIN[panel], VALUES["c"])
    briefs = {
        role: render.brief(r, doc_of(candidate), source and str(source))
        for role, r in roles.items()
    }
    fields = render.run_fields(
        roles,
        has_source=bool(source),
        b=B_MIN[panel],
        c_by_model=VALUES["c"],
        lenses_path=LENSES,
        briefs={roles[role]["rid"]: b for role, b in briefs.items()},
    )
    return roles, briefs, fields


def test_spec_and_doc_fixtures_exist():
    for p in (SPEC, PARENT, DOC_FIXTURE):
        assert p.is_file() and p.stat().st_size > 0, p
    assert "Parent: ./parent1.md" in SPEC.read_text(encoding="utf-8")


@pytest.mark.parametrize("panel", PANELS)
def test_lens_renders_for_spec_fixture(panel):
    roles, briefs, fields = build(panel, SPEC, PARENT)
    seen = set()
    for role, b in briefs.items():
        assert b["text"].count(f"Driving document: {PARENT}.") == 1
        ids = [c for c, _ in recipe_paragraphs(b["text"])]
        assert ids == roles[role]["recipes"] and len(ids) >= 2
        seen |= set(ids)
    assert seen == set(CLASSES)  # C2 included: the parent is the source
    assert fields["no_source"] is False and fields["c2_not_applicable"] is False


@pytest.mark.parametrize("panel", PANELS)
def test_lens_renders_for_doc_fixture(panel):
    roles, briefs, fields = build(panel, DOC_FIXTURE, None)
    seen = set()
    for role, b in briefs.items():
        assert "Driving document:" not in b["text"]
        ids = [c for c, _ in recipe_paragraphs(b["text"])]
        assert ids == roles[role]["recipes"] and len(ids) >= 2
        seen |= set(ids)
    assert seen == set(CLASSES) - {"C2"} and len(seen) == 7
    assert fields["no_source"] is True and fields["c2_not_applicable"] is True
