import json
import pathlib

import pytest
from conftest import normalised_rule_text
from harness import loader
from harness.loader import LoadError, Paths

RULE = loader.EXPERIMENT / "decision-rule.md"
OPEN_FIELDS = {"noul_low_operator", "noul_high_operator", "unresolved_failure_invalid_count"}


def _rule_copy(tmp_path, old=None, new=None, drop_line=None, text=None):
    """A copy of the rule file with its open fields UNSET (unless ``text`` is given), whatever the live file holds now."""
    s = normalised_rule_text() if text is None else text
    if old is not None:
        assert old in s
        s = s.replace(old, new, 1)
    if drop_line is not None:
        s = "\n".join(line for line in s.splitlines() if not line.startswith(drop_line)) + "\n"
    p = tmp_path / "decision-rule.md"
    p.write_text(s, encoding="utf-8")
    return p


# ---- rule file (T-01 refusals, T-04)

def test_committed_rule_loads_and_only_the_three_open_fields_may_be_unset(tmp_path):
    rule = loader.load_rule(RULE)
    assert {k for k in loader.RULE_KEYS if rule[k] == "UNSET"} <= OPEN_FIELDS
    normal = loader.load_rule(_rule_copy(tmp_path))
    assert {k for k in loader.RULE_KEYS if normal[k] == "UNSET"} == OPEN_FIELDS
    assert rule["status"] == "AGREED" and rule["alpha_inverse"] == 20 and rule["attempt_timeout_s"] == 10.0
    assert rule["median_limit_s"] == 2.0 and rule["slowest_limit_s"] == 5.0 and rule["spend_cap_usd"] == 1.0


def test_committed_rule_holds_the_verbatim_agreement_and_marks_the_owner_words_relayed():
    text = RULE.read_text(encoding="utf-8")
    assert "I agree with all five of your amendments" in text and "56/1024 = 0.0547" in text
    assert "you and the agent debate whats correct way to handle this and do it" in text
    assert "relayed" in text.lower() and "did not type them" in text


@pytest.mark.parametrize("status", ["PROPOSED", "PENDING"])
def test_rule_refuses_a_status_other_than_agreed(tmp_path, status):
    with pytest.raises(LoadError, match="not AGREED"):
        loader.load_rule(_rule_copy(tmp_path, "status: AGREED", f"status: {status}"))


def test_rule_refuses_an_empty_agreement_text(tmp_path):
    s = RULE.read_text(encoding="utf-8")
    head, _, rest = s.partition("## Agreement text (verbatim)")
    _, _, tail = rest.partition("## Relayed owner words")
    p = _rule_copy(tmp_path, text=head + "## Agreement text (verbatim)\n\n## Relayed owner words" + tail)
    with pytest.raises(LoadError, match="agreement text"):
        loader.load_rule(p)


@pytest.mark.parametrize("key", ["agreed_by", "agreed_at", "relayed_owner_words"])
def test_rule_refuses_an_empty_who_when_or_words(tmp_path, key):
    lines = [(f"{key}:" if line.startswith(key + ":") else line) for line in RULE.read_text(encoding="utf-8").splitlines()]
    p = _rule_copy(tmp_path, text="\n".join(lines) + "\n")
    with pytest.raises(LoadError, match="empty"):
        loader.load_rule(p)


def test_rule_refuses_a_missing_key_and_a_missing_file(tmp_path):
    with pytest.raises(LoadError, match="lacks the key alpha_inverse"):
        loader.load_rule(_rule_copy(tmp_path, drop_line="alpha_inverse:"))
    with pytest.raises(LoadError, match="missing"):
        loader.load_rule(tmp_path / "nope.md")


def test_rule_refuses_scoring_while_a_value_is_unset_and_accepts_it_when_all_are_set(tmp_path):
    with pytest.raises(LoadError, match="UNSET"):
        loader.load_rule(_rule_copy(tmp_path), for_scoring=True)
    s = normalised_rule_text()
    s = s.replace("noul_low_operator: UNSET", "noul_low_operator: le").replace("noul_high_operator: UNSET", "noul_high_operator: ge")
    s = s.replace("unresolved_failure_invalid_count: UNSET", "unresolved_failure_invalid_count: 3")
    rule = loader.load_rule(_rule_copy(tmp_path, text=s), for_scoring=True)
    assert rule["noul_low_operator"] == "le" and rule["unresolved_failure_invalid_count"] == 3


def test_rule_refuses_an_operator_that_does_not_fit_its_edge(tmp_path):
    with pytest.raises(LoadError, match="noul_low_operator"):
        loader.load_rule(_rule_copy(tmp_path, "noul_low_operator: UNSET", "noul_low_operator: gt"))
    with pytest.raises(LoadError, match="noul_high_operator"):
        loader.load_rule(_rule_copy(tmp_path, "noul_high_operator: UNSET", "noul_high_operator: lt"))


# ---- corpus (T-04)

def _row(i, text, label, **kw):
    r = {"id": f"p{i}", "text": text, "source": "https://example.org/issue/" + str(i), "retrieved_on": "2026-11-26",
         "selection_reason": "r", "label": label, "label_basis": "b", "labeller": "a person", "labelled_on": "2026-11-26",
         "seen_by_table": False}
    r.update(kw)
    return r


def _good_rows():
    labels = list(loader.TYPES) + ["ambiguous", "none-fit"]
    return [_row(i, f"problem text number {i}", lab) for i, lab in enumerate(labels)]


def _write(tmp_path, rows):
    p = tmp_path / "corpus.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return p


def test_a_valid_corpus_loads(tmp_path):
    rows = loader.load_corpus(_write(tmp_path, _good_rows()))
    assert len(rows) == 8 and rows[0]["id"] == "p0"


def _bad(rows, i, **kw):
    rows[i] = dict(rows[i], **kw)
    return rows


@pytest.mark.parametrize("mutate,match", [
    (lambda r: _bad(r, 0, source=""), "no public source"),
    (lambda r: _bad(r, 1, id="p0"), "duplicate corpus id"),
    (lambda r: _bad(r, 1, text="problem text number 0"), "same text"),
    (lambda r: _bad(r, 2, label="urgent"), "outside the allowed set"),
    (lambda r: _bad(r, 3, label="bug"), "no row labelled deployment"),
    (lambda r: _bad(r, 6, label="bug"), "no row labelled ambiguous"),
    (lambda r: _bad(r, 7, label="bug"), "no row labelled none-fit"),
])
def test_corpus_rejects_each_rule_break(tmp_path, mutate, match):
    with pytest.raises(LoadError, match=match):
        loader.load_corpus(_write(tmp_path, mutate(_good_rows())))


@pytest.mark.parametrize("text,reason", [
    ("see https://github.com/example/project/issues/4 for details", "github_url"),
    ("the file is at /home/someone/project/main.py", "path_home"),
])
def test_corpus_refuses_a_prompt_the_privacy_screen_refuses_without_echoing_it(tmp_path, text, reason):
    rows = _bad(_good_rows(), 0, text=text)
    with pytest.raises(LoadError) as e:
        loader.load_corpus(_write(tmp_path, rows))
    msg = str(e.value)
    assert "p0" in msg and reason in msg and text not in msg and "someone" not in msg


def test_table_answers_load_and_need_a_prompt_id(tmp_path):
    p = tmp_path / "t.jsonl"
    p.write_text('{"prompt_id": "p0", "answer": null, "cues": [], "rows": [], "method": "m"}\n')
    assert loader.load_table_answers(p)[0]["prompt_id"] == "p0"
    p.write_text('{"answer": null}\n')
    with pytest.raises(LoadError, match="prompt_id"):
        loader.load_table_answers(p)


@pytest.mark.parametrize("field", list(loader.PROVENANCE_FIELDS))
@pytest.mark.parametrize("blank", ["", "   ", None])
def test_corpus_refuses_a_blank_provenance_field_by_row_and_field_name(tmp_path, field, blank):
    with pytest.raises(LoadError, match=f"corpus row p4 has an empty {field}"):
        loader.load_corpus(_write(tmp_path, _bad(_good_rows(), 4, **{field: blank})))


def test_corpus_refuses_a_seen_by_table_that_is_not_true_or_false(tmp_path):
    with pytest.raises(LoadError, match="p2 has a seen_by_table"):
        loader.load_corpus(_write(tmp_path, _bad(_good_rows(), 2, seen_by_table="no")))


IDS = ["a", "b", "c"]


def _answers(tmp_path, rows):
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return p


def test_table_answers_pass_when_every_corpus_id_has_one_explicit_answer(tmp_path):
    p = _answers(tmp_path, [{"prompt_id": "a", "answer": "bug"}, {"prompt_id": "b", "answer": None}, {"prompt_id": "c", "answer": "test"}])
    assert len(loader.load_table_answers(p, IDS)) == 3


@pytest.mark.parametrize("rows,match", [
    ([{"prompt_id": "a", "answer": "bug"}, {"prompt_id": "b"}, {"prompt_id": "c", "answer": None}], "b has no answer field"),
    ([{"prompt_id": "a", "answer": "bug"}, {"prompt_id": "a", "answer": None}, {"prompt_id": "b", "answer": None},
      {"prompt_id": "c", "answer": None}], "prompt a more than once"),
    ([{"prompt_id": "a", "answer": "urgent"}, {"prompt_id": "b", "answer": None}, {"prompt_id": "c", "answer": None}],
     "a has an answer that is neither null nor one of the six"),
    ([{"prompt_id": "a", "answer": None}, {"prompt_id": "b", "answer": None}, {"prompt_id": "c", "answer": None},
      {"prompt_id": "z", "answer": None}], "not in the corpus: z"),
    ([{"prompt_id": "a", "answer": None}, {"prompt_id": "b", "answer": None}], "lack a row for corpus prompt: c"),
])
def test_table_answers_are_refused_against_the_corpus(tmp_path, rows, match):
    with pytest.raises(LoadError, match=match):
        loader.load_table_answers(_answers(tmp_path, rows), IDS)


@pytest.mark.parametrize("value,ok", [("r1", True), ("run-2.a_b", True), ("..", False), (".", False), ("../x", False), ("/etc", False),
                                       ("a/b", False), ("", False), ("a b", False), (None, False)])
def test_is_plain_name(value, ok):
    assert loader.is_plain_name(value) is ok


# ---- paths and hashing

def test_paths_on_a_temporary_root_stay_under_it_except_jevlib(tmp_path):
    p = Paths(tmp_path)
    for name in ("corpus", "selection_criteria", "labelling_record", "questions_py", "rule", "table_answers", "table_provenance",
                 "manifest", "events", "ledger", "runs", "report", "decision_record", "rescores", "tests_dir"):
        assert tmp_path in getattr(p, name).parents, name
    assert all(tmp_path in c.parents for c in p.code_files())
    assert tmp_path not in p.jevlib_dir.parents


def test_jevlib_files_are_the_top_level_py_files_only(tmp_path):
    d = tmp_path / "jevlib"
    (d / "__pycache__").mkdir(parents=True)
    (d / "sub").mkdir()
    for f in ("b.py", "a.py", "notes.txt", "__pycache__/c.py", "sub/d.py"):
        (d / f).write_text("x")
    assert [f.name for f in Paths(tmp_path, jevlib_dir=d).jevlib_files()] == ["a.py", "b.py"]
    assert all(f.parent == pathlib.Path(d) for f in Paths(tmp_path, jevlib_dir=d).jevlib_files())


def test_sha256_file_is_the_sha256_of_the_bytes(tmp_path):
    p = tmp_path / "f"
    p.write_bytes(b"abc")
    assert loader.sha256_file(p) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
