"""Shared test setup: import paths, a network guard, a fake key, and a guard on the real experiment folder."""
import pathlib
import socket
import sys

import pytest

EXP = pathlib.Path(__file__).resolve().parents[2]          # .dev/research/jev-vs-keyword-table-611
JEV = EXP.parent / "346-review-loop-experiments" / "p15" / "jev"   # parent folder of the jevlib package
for _p in (JEV, EXP):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

FAKE_KEY = "fake-test-key-0123456789abcdef"


def real_state_snapshot(root=EXP):
    """Existence, size and modification time of the state files under ``root``; for ``runs`` every file below it as well."""
    root = pathlib.Path(root)
    snap = {}
    for rel in ("events.jsonl", "manifest.json", "ledger/spend.json"):
        p = root / rel
        snap[rel] = (p.stat().st_size, p.stat().st_mtime_ns) if p.is_file() else None
    runs = root / "runs"
    if runs.is_dir():
        snap["runs"] = tuple(sorted((str(f.relative_to(runs)), f.stat().st_size, f.stat().st_mtime_ns)
                                    for f in runs.rglob("*") if f.is_file()))
        snap["runs/"] = runs.stat().st_mtime_ns
    else:
        snap["runs"] = None
    return snap


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Fail any test that opens a socket connection."""
    def refuse(self, *args, **kwargs):
        raise AssertionError("a test tried to open a network connection")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket.socket, "connect_ex", refuse)


@pytest.fixture(autouse=True)
def real_state_untouched():
    """The real events log, manifest, ledger and runs folder must be the same after each test as before it."""
    before = real_state_snapshot()
    yield
    assert real_state_snapshot() == before, "a test changed the real experiment state"


@pytest.fixture
def fake_key(monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", FAKE_KEY)
    return FAKE_KEY


@pytest.fixture
def snapshot_fn():
    return real_state_snapshot


def normalised_rule_text():
    """The committed rule file with its three open fields forced back to ``UNSET``, so a test never depends on whether the owner
    has filled them in yet."""
    import re

    from harness import loader
    text = loader.EXPERIMENT.joinpath("decision-rule.md").read_text(encoding="utf-8")
    return re.sub(r"^(noul_low_operator|noul_high_operator|unresolved_failure_invalid_count): .*$", r"\1: UNSET", text,
                  flags=re.MULTILINE)


def synthetic_corpus_rows():
    """Eight valid corpus rows: one per type, one ambiguous, one none-fit."""
    labels = ["bug", "build", "performance", "deployment", "security", "test", "ambiguous", "none-fit"]
    return [{"id": f"p{i}", "text": f"synthetic problem text number {i}", "source": f"https://example.org/post/{i}",
             "retrieved_on": "2026-11-26", "selection_reason": "synthetic", "label": lab, "label_basis": "synthetic",
             "labeller": "a test", "labelled_on": "2026-11-26", "seen_by_table": False} for i, lab in enumerate(labels)]


@pytest.fixture
def exp(tmp_path):
    """A loader.Paths on a temporary root, filled with small synthetic frozen files, code stand-ins, a jevlib stand-in folder and
    a copy of the committed rule file with its open fields set to UNSET.  Nothing here touches the real experiment folder."""
    import json

    from harness import loader
    jevlib = tmp_path / "jevlib"
    jevlib.mkdir()
    for name in ("a.py", "b.py"):
        (jevlib / name).write_text(f"# stand-in {name}\n")
    p = loader.Paths(tmp_path, jevlib_dir=jevlib)
    for f in p.code_files():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"# stand-in {f.name}\n")
    p.corpus.parent.mkdir(parents=True)
    p.corpus.write_text("\n".join(json.dumps(r) for r in synthetic_corpus_rows()) + "\n")
    p.selection_criteria.write_text("selection criteria\n")
    p.labelling_record.write_text("labelling record\n")
    p.table_answers.parent.mkdir(parents=True)
    p.table_answers.write_text("\n".join(json.dumps({"prompt_id": f"p{i}", "answer": None}) for i in range(8)) + "\n")
    p.table_provenance.write_text("table provenance\n")
    p.tests_dir.mkdir(parents=True, exist_ok=True)
    p.rule.write_text(normalised_rule_text(), encoding="utf-8")
    return p
