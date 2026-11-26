"""Plan reader (DESIGN section 3, IMPLEMENTATION step 6, REQ-37) and the two plan fixtures F-PLAN-1 and F-PLAN-2.

The trigger checks of p_basic.md use plain regular expressions on the blocks, not the extractors (those come later),
so a fixture that loses a trigger shape fails here first.
"""

import re
import subprocess
import sys

import pytest
from helpers import SW

from scaffold import fnd
from sweep import formats, plan, words

PLANS = SW / "fixtures" / "plans"
KEYS = {"kind", "id", "text", "line_start", "line_end", "task", "phase"}


@pytest.fixture(scope="module")
def basic():
    return plan.read(PLANS / "p_basic.md")


@pytest.fixture(scope="module")
def clean():
    return plan.read(PLANS / "p_clean.md")


def by_id(doc, bid):
    (b,) = [b for b in doc.blocks if b["id"] == bid]
    return b


def line_of(doc, needle, after=0):
    return next(i for i, ln in enumerate(doc.lines, 1) if i > after and needle in ln)


# ---------------------------------------------------------------- the plan format


def test_each_block_kind_is_recognised(basic):
    got = {k: [b["id"] for b in basic.of(k)] for k in plan.KINDS}
    assert got["task"] == ["T1", "T2", "T3", "T4", "T5"]
    assert got["criterion"] == [
        "goal",
        "T1.C1",
        "T1.C2",
        "T2.C1",
        "T2.C2",
        "T3.C1",
        "T3.C2",
        "T4.C1",
        "T5.C1",
        "T5.C2",
    ]
    # the nested bullet under the first constraint is part of it, not a constraint of its own
    assert got["constraint"] == ["K1", "K2", "K3"]
    assert got["dictated_text"] == ["T4.D1"]
    assert got["edit_target"] == ["T1.E1", "T2.E1", "T3.E1", "T3.E2", "T4.E1"]
    assert got["gate"] == ["T3.G1", "T5.G1", "T5.G2"]
    assert "no network access" in by_id(basic, "K1")["text"]


def test_block_fields_and_ranges(basic, clean):
    for doc in (basic, clean):
        assert doc.format == "plan"
        n = len(doc.lines)
        for b in doc.blocks:
            assert KEYS <= set(b) <= KEYS | {"path", "creates"}
            assert (b["kind"] == "edit_target") == ("path" in b)
            assert 1 <= b["line_start"] <= b["line_end"] <= n
            assert b["kind"] in plan.KINDS and b["text"].strip()
        ids = [b["id"] for b in doc.blocks]
        assert len(ids) == len(set(ids))


def test_task_and_phase_fields(basic):
    assert [(b["id"], b["phase"]) for b in basic.of("task")] == [
        ("T1", "P1"),
        ("T2", "P1"),
        ("T3", "P2"),
        ("T4", "P2"),
        ("T5", "P3"),
    ]
    assert (
        by_id(basic, "goal")["task"] is None and by_id(basic, "goal")["phase"] is None
    )
    assert by_id(basic, "K2")["task"] is None
    assert by_id(basic, "T4.D1")["task"] == "T4"
    assert by_id(basic, "T3.G1")["task"] == "T3"
    for b in basic.blocks:
        if b["task"]:
            assert b["id"] == b["task"] or b["id"].startswith(b["task"] + ".")


def test_line_numbers_are_right(basic):
    lines = basic.lines
    assert by_id(basic, "goal")["line_start"] == line_of(basic, "Goal:")
    assert by_id(basic, "K2")["line_start"] == line_of(basic, "A deletion notice must")
    k1 = by_id(basic, "K1")
    assert (k1["line_start"], k1["line_end"]) == (
        line_of(basic, "- Code lives under"),
        line_of(basic, "has no network access"),
    )
    assert by_id(basic, "T4.D1")["line_start"] == line_of(basic, "> Report id 41")
    assert by_id(basic, "T4.D1")["line_end"] == line_of(basic, "> Report id 41")
    # a task body runs from the line after its heading to the line before its label
    for tid, title in (
        ("T1", "## Task 1:"),
        ("T3", "## Task 3:"),
        ("T5", "## Task 5:"),
    ):
        head = line_of(basic, title)
        label = line_of(basic, "Acceptance criteria:", head)
        b = by_id(basic, tid)
        assert lines[b["line_start"] - 1].strip() and lines[b["line_end"] - 1].strip()
        assert b["line_start"] == head + 2 and b["line_end"] == label - 2
    # every block's text is what its lines say
    for b in basic.blocks:
        raw = "\n".join(lines[b["line_start"] - 1 : b["line_end"]])
        assert fnd.flat(b["text"]) in fnd.flat(raw)
        assert fnd.flat(b["text"]).split()[0] in lines[b["line_start"] - 1]


@pytest.mark.parametrize("name", ["p_basic.md", "p_clean.md"])
def test_anchor_cut_from_the_candidate_is_found_by_locate(name):
    doc = plan.read(PLANS / name)
    assert doc.blocks
    for b in doc.blocks:
        whole = fnd.locate(doc.text, b["text"])
        assert (b["line_start"] - 1, b["line_end"]) in whole, b["id"]
        t = fnd.flat(b["text"])
        # a prefix of at most 200 characters (the anchor limit) and a slice from the middle
        for anchor in (t[:200], t[len(t) // 3 : len(t) // 3 + 40].strip()):
            hits = fnd.locate(doc.text, anchor)
            assert hits, (b["id"], anchor)
            assert any(
                b["line_start"] - 1 <= lo and hi <= b["line_end"] for lo, hi in hits
            ), (b["id"], anchor)


def test_tasks_and_citations(basic, clean):
    assert {t: v["citations"] for t, v in basic.tasks.items()} == {
        "T1": ["2.1"],
        "T2": ["2.2"],
        "T3": ["2.3", "Q4"],
        "T4": ["2.4"],
        "T5": [],
    }
    assert basic.tasks["T3"]["title"] == "Create the retention job and its test"
    assert basic.tasks["T3"]["line"] == line_of(basic, "## Task 3:")
    assert all(v["citations"] == [] for v in clean.tasks.values())


def test_edit_targets_carry_path_and_creates(basic):
    got = [(b["path"], b["creates"]) for b in basic.of("edit_target")]
    assert got == [
        ("src/exporter/report.py", False),
        ("docs/guide.md", False),
        ("src/exporter/retention.py", True),
        ("tests/test_retention.py", True),
        ("src/exporter/notice.py", True),
    ]
    # a sentence that names no edit verb makes no edit target, and a criterion is not a task sentence
    assert not [b for b in basic.of("edit_target") if "Leave" in b["text"]]


def test_gate_blocks(basic):
    gates = basic.of("gate")
    # the last task is a run/sync task: all its criteria; plus any bullet that holds a pytest or make command
    assert {b["text"] for b in gates} == {
        "`pytest tests/test_retention.py -k purge_keeps_held` exits 0.",
        "`make test` exits 0.",
        "`pytest tests/test_retention.py -q` exits 0.",
    }
    assert by_id(basic, "goal") not in gates


def test_a_gate_section_is_a_gate():
    text = (
        "## Task 1: Do it\n\nCreate `a/b.py`.\n\nAcceptance criteria:\n- it works\n\n"
        "## Final checks\n\n- `make test` exits 0.\n- the log is clean\n"
    )
    d = plan.parse(text)
    assert [(b["id"], b["text"]) for b in d.of("gate")] == [
        ("G1", "`make test` exits 0."),
        ("G2", "the log is clean"),
    ]
    assert d.of("task")[0]["id"] == "T1"


def test_fence_hides_headings_and_bullets():
    text = (
        "## Task 1: A\n\nCreate `a/x.py`.\n\n```text\n## Task 2: not a task\nAcceptance criteria:\n- not a bullet\n```\n\n"
        "Acceptance criteria:\n- real one\n"
    )
    d = plan.parse(text)
    assert [b["id"] for b in d.of("task")] == ["T1"]
    assert [b["text"] for b in d.of("criterion")] == ["real one"]
    assert d.of("dictated_text")[0]["text"].startswith("## Task 2: not a task")


def test_crlf_and_bom_read_like_lf(basic):
    raw = (PLANS / "p_basic.md").read_bytes()
    crlf = plan.parse(raw.replace(b"\n", b"\r\n"))
    bom = plan.parse(b"\xef\xbb\xbf" + raw)
    assert crlf.blocks == basic.blocks and bom.blocks == basic.blocks
    assert all("\r" not in b["text"] for b in crlf.blocks)


def test_sentences_split_without_breaking_paths_or_numbers():
    s = [
        x[2]
        for x in plan.sentences(
            "Edit `docs/guide.md`. Then run it, v1.2 stays. See 2.3 for more."
        )
    ]
    assert s == [
        "Edit `docs/guide.md`.",
        "Then run it, v1.2 stays.",
        "See 2.3 for more.",
    ]
    assert plan.sentences("  \n ") == []
    text = "a b. C d"
    (a, b, sent), _ = plan.sentences(text)
    assert text[a:b] == sent == "a b."


def test_quoted_span_needs_a_dictation_verb_and_25_characters():
    d = plan.parse(
        '## Task 1: A\n\nWrite the title "This heading is long enough to count" now. '
        'Add the label "Short label" next. The doc has "Another long quoted span of text here".\n\n'
        "Acceptance criteria:\n- it passes\n"
    )
    assert [b["text"] for b in d.of("dictated_text")] == [
        "This heading is long enough to count"
    ]


# ---------------------------------------------------------------- failure and unknown structure


@pytest.mark.parametrize(
    "text",
    [
        "",
        "\n\n  \n",
        "just some words\n\nand some more words\n",
        '# A title\n\nProse with `code` and "a quoted span of more than twenty five characters".\n\n'
        "> a quote\n\n```\nfence\n```\n\n- a bullet\n",
        "Acceptance criteria:\n- a bullet outside any task\n",
        "## Task: no number\n\nbody\n",
        "---\nschema: x\n---\n",
        "\x0c\x1b[0m]\t\t:: ?? !! ## ###\n",
    ],
)
def test_unknown_structure_yields_zero_blocks_and_no_exception(text):
    d = plan.parse(text)
    assert d.blocks == [] and d.tasks == {}


@pytest.mark.parametrize(
    "raw", [b"\xff\xfe\x00\x01", b"abc\xc3(def", b"a\x00b", b"\x80\x81\x82"]
)
def test_unreadable_bytes_raise(raw, tmp_path):
    with pytest.raises(plan.ReadError):
        plan.parse(raw)
    p = tmp_path / "bad.md"
    p.write_bytes(raw)
    with pytest.raises(ValueError):
        plan.read(p)


def test_missing_file_and_unknown_format_raise(tmp_path):
    with pytest.raises(OSError):
        plan.read(tmp_path / "nope.md")
    with pytest.raises(ValueError):
        plan.parse("text", "no-such-format")
    with pytest.raises(plan.ReadError):
        plan.parse("a\x00b")


# ---------------------------------------------------------------- the other two format dictionaries (drafts)


def test_spec_and_doc_dictionaries_read_inline_text():
    spec = (
        "# Spec\n\n## 1. Intro\n\nThe tool shall export reports.\n"
        "This note applies to every report.\n\nThe tool must write a log line.\n\n"
        "### Message format\n\n```text\nreport done\n```\n\n"
        "## 2. Affects\n\n- `src/a/b.py` (new)\n- `docs/c.md`\n\n## 3. Verification\n\n- `make test` exits 0.\n"
    )
    d = plan.parse(spec, "spec")
    assert d.format == "spec"
    assert [b["text"] for b in d.of("criterion")] == [
        "The tool shall export reports.",
        "The tool must write a log line.",
    ]
    assert [b["text"] for b in d.of("constraint")] == [
        "This note applies to every report."
    ]
    assert {b["text"] for b in d.of("dictated_text")} >= {"report done"}
    assert [(b["path"], b["task"]) for b in d.of("edit_target")] == [
        ("src/a/b.py", None),
        ("docs/c.md", None),
    ]
    assert [b["text"] for b in d.of("gate")] == ["`make test` exits 0."]
    assert [b["id"] for b in d.of("task")] == ["T1"]
    doc = (
        "# How to export\n\nExport every report with one command.\n\n```bash\nexporter run\n```\n\n"
        "```text\nDone\n```\n"
    )
    e = plan.parse(doc, "doc")
    assert [b["text"] for b in e.of("criterion")] == [
        "Export every report with one command.",
        "exporter run",
    ]
    assert [b["text"] for b in e.of("dictated_text")] == ["Done"]
    assert e.of("constraint") == [] and e.of("edit_target") == [] and e.of("gate") == []


# ---------------------------------------------------------------- F-PLAN-1: a trigger for each of E1 to E7


def clauses(text):
    parts = re.split(r";|, and | and |,", text)
    return [p.strip() for p in parts if len(p.split()) >= 4]


def tokens(text):
    stop = set(words.STOP)
    return {w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in stop}


def path_tokens(text):
    return set(re.findall(formats.PATH_TOKEN, text))


def test_p_basic_has_an_e1_completeness_trigger(basic):
    b = by_id(basic, "T1.C2")
    assert re.search(r"\bevery\b", b["text"], re.I)
    task = by_id(basic, "T1")
    instr, sent = path_tokens(task["text"]), path_tokens(b["text"])
    assert instr and sent and instr != sent  # a narrower instruction scope
    assert (
        not any("*" in t for t in sent) and len(sent) < 2
    )  # no bound on the criterion


def test_p_basic_has_an_e1_universal_trigger_next_to_a_limiter(basic):
    b = by_id(basic, "T3.C1")
    assert re.search(r"\bonly\b", b["text"], re.I)
    (test_file,) = path_tokens(b["text"])
    assert test_file.startswith("tests/")
    limiter = re.compile(r"\b(?:%s)\b" % "|".join(words.LIMITERS), re.I)
    others = [
        ln
        for i, ln in enumerate(basic.lines, 1)
        if test_file in ln and not b["line_start"] <= i <= b["line_end"]
    ]
    assert any(limiter.search(ln) and "skips" in ln for ln in others)


def test_p_basic_has_an_e2_literal_that_misses_the_ordered_heading(basic):
    crit = by_id(basic, "T2.C1")
    (pattern,) = re.findall(r"grep -c '([^']+)'", crit["text"])
    ordered = re.findall(r'heading "([^"]+)"', by_id(basic, "T2")["text"])
    assert ordered
    assert pattern not in ordered[0] and pattern.lower() not in ordered[0].lower()
    norm = lambda s: re.sub(r"[-_\s]+", " ", s.lower())  # noqa: E731
    assert norm(pattern) == norm(ordered[0])
    assert re.search(r"pytest\b.* -k \w+", by_id(basic, "T3.C2")["text"])


def test_p_basic_has_an_e3_edit_target_that_no_named_test_covers(basic):
    (target,) = [b for b in basic.of("edit_target") if b["path"].endswith("report.py")]
    assert target["creates"] is False
    assert (
        "test_report" not in basic.text
    )  # the repository's own test for it stays unnamed
    assert not [b for b in basic.of("gate") if "report" in b["text"]]


def test_p_basic_has_an_e4_count_claim(basic):
    assert re.search(
        r"from 3 report formats to 4 report formats", by_id(basic, "T2")["text"]
    )
    assert "No remaining `3 report formats`" in by_id(basic, "T2.C2")["text"]


def test_p_basic_has_an_e5_cited_rule_whose_identifiers_the_task_lacks(basic):
    assert basic.tasks["T3"]["citations"][0] == "2.3"
    source = (PLANS / "source.md").read_text(encoding="utf-8")
    section = re.search(r"^## 2\.3 .*?(?=^## )", source, re.M | re.S).group(0)
    ids = re.findall(r"`(\w+)`", section)
    task_text = " ".join(b["text"] for b in basic.blocks if b["task"] == "T3")
    missing = [i for i in ids if i not in task_text]
    assert len(missing) >= 2 and "legal_hold" not in missing
    assert basic.text.count("./source.md") >= 2


def test_p_basic_has_an_e6_value_that_is_read_and_never_written(basic):
    spots = [i for i, ln in enumerate(basic.lines, 1) if "`legal_hold`" in ln]
    assert len(spots) == 1
    line = basic.lines[spots[0] - 1]
    assert "keys on" in line
    for verb in ("sets", "=", "gives", "writes", "assigns", "produces", "returns"):
        assert verb not in line


def test_p_basic_has_an_e7_constraint_clause_the_dictated_text_omits(basic):
    cl = clauses(by_id(basic, "K2")["text"])
    assert len(cl) == 3
    dictated = tokens(by_id(basic, "T4.D1")["text"])
    distinct = []
    for i, c in enumerate(cl):
        rest = set().union(*(tokens(o) for j, o in enumerate(cl) if j != i))
        distinct.append(tokens(c) - rest)
    shared = [len(d & dictated) for d in distinct]
    assert max(shared) >= 2 and 0 in shared
    assert distinct[shared.index(0)] & {"appeal", "address"}


# ---------------------------------------------------------------- F-PLAN-2: every criterion bounded, no trigger shape


def test_p_clean_has_no_trigger_shape(clean):
    set_words = re.compile(
        r"(?<![\w-])(?:%s)(?![\w-])"
        % "|".join(
            re.escape(w).replace(r"\ ", r"\s+")
            for w in (
                *words.SET_COMPLETENESS,
                *words.SET_UNIVERSAL,
                "outside",
                "nothing",
            )
        ),
        re.I,
    )
    for b in clean.blocks:
        assert not set_words.search(b["text"]), b["id"]
    crit = clean.of("criterion")
    assert len(crit) == 7
    for b in crit:
        assert "*" not in b["text"] and not re.search(
            r"\b(?:none|zero|no matches)\b", b["text"], re.I
        )
        assert not re.search(r"`(?:grep|egrep|rg|pytest|git grep|test)\b", b["text"])
        assert " -k " not in b["text"] and " -m " not in b["text"]
    assert clean.of("dictated_text") == []
    assert [b for b in clean.of("edit_target") if not b["creates"]] == []
    assert "Source sections" not in clean.text
    assert not re.search(
        r"\bkeys on\b|\bwhen\b|==|\bis read\b|\bdepends on\b|\breturns for\b",
        clean.text,
        re.I,
    )
    assert not re.search(r"\b\d+\s+[a-z]+s\b", " ".join(b["text"] for b in crit)), (
        "no count claim"
    )
    assert not [
        c
        for k in clean.of("constraint")
        for c in clauses(k["text"])
        if len(clauses(k["text"])) > 2
    ]
    assert clean.of("task") and clean.of("gate") and clean.of("constraint")


# ---------------------------------------------------------------- F-PLAN-3, F-SPEC and F-DOC (Task 10)

GEN = PLANS / "gen_setwords.py"
FIXTURES = SW / "fixtures"


def gen(n, tmp_path, *extra):
    out = tmp_path / f"gen{n}.md"
    cmd = [sys.executable, "-I", str(GEN), "--n", str(n), "--out", str(out), *extra]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return out


def set_word_classes(text):
    """The set of classes ('C1' completeness, 'C6' universal) whose words the sentence holds."""

    def hit(ws):
        rx = r"(?<![\w-])(?:%s)(?![\w-])" % "|".join(
            re.escape(w).replace(r"\ ", r"\s+") for w in ws
        )
        return re.search(rx, text, re.I)

    return {
        c
        for c, ws in (("C1", words.SET_COMPLETENESS), ("C6", words.SET_UNIVERSAL))
        if hit(ws)
    }


def test_setword_generator_makes_200_sentences_over_12_tasks(tmp_path):
    out = gen(200, tmp_path)
    doc = plan.read(out)
    assert doc.format == "plan"
    assert [b["id"] for b in doc.of("task")] == [f"T{i}" for i in range(1, 13)]
    crit = [b for b in doc.of("criterion") if b["id"] != "goal"]
    hits = [b for b in crit if set_word_classes(b["text"])]
    assert len(hits) >= 200 and len(hits) == len(crit) == 200
    per_task = {}
    for b in hits:
        per_task.setdefault(b["task"], []).append(set_word_classes(b["text"]))
        assert len(b["text"]) >= 12 and len(plan.sentences(b["text"])) == 1
    assert set(per_task) == {f"T{i}" for i in range(1, 13)}
    for classes in per_task.values():
        assert 16 <= len(classes) <= 17
        assert {"C1"} in classes and {
            "C6"
        } in classes  # each task has both kinds, never both in one sentence
    assert all(len(c) == 1 for cs in per_task.values() for c in cs)
    assert len({b["text"] for b in hits}) == 200
    # the Goal line holds no set word, so the count above is the generator's own
    assert not set_word_classes(by_id(doc, "goal")["text"])
    assert len(doc.of("edit_target")) == 12


def test_setword_generator_n_is_a_parameter_and_output_is_repeatable(tmp_path):
    small = plan.read(gen(30, tmp_path))
    assert len([b for b in small.of("criterion") if b["id"] != "goal"]) == 30
    assert len(small.of("task")) == 12
    few = plan.read(gen(5, tmp_path))  # no empty task: the task count is cut to n
    assert len(few.of("task")) == 5
    again = gen(200, tmp_path, "--tasks", "12")
    r = subprocess.run(
        [sys.executable, "-I", str(GEN), "--n", "200"], capture_output=True, text=True
    )
    assert r.returncode == 0 and r.stdout == again.read_text(encoding="utf-8")
    bad = subprocess.run(
        [sys.executable, "-I", str(GEN), "--n", "0"], capture_output=True, text=True
    )
    assert bad.returncode == 2 and "at least 1" in bad.stderr


def test_spec1_reads_with_the_spec_dictionary():
    doc = plan.read(FIXTURES / "specs" / "spec1.md", "spec")
    assert doc.format == "spec"
    crit = doc.of("criterion")
    assert len(crit) >= 6 and all(
        re.search(r"\b(?:shall|must|should)\b", b["text"]) for b in crit
    )
    assert [b["text"] for b in doc.of("constraint")] == [
        "This section applies to every locker model in the hall."
    ]
    assert [b["path"] for b in doc.of("edit_target")] == [
        "src/locker/door.py",
        "src/locker/log.py",
        "docs/locker-guide.md",
        "src/locker/alarm.py",
    ]
    assert "LOCKER 14 OPEN 2027-01-01T10:00:00" in [
        b["text"] for b in doc.of("dictated_text")
    ]
    assert len(doc.of("gate")) == 2
    # the numbered sections cite the parent's sections
    assert doc.tasks["T2"]["citations"] == ["4.1", "4.2"]
    assert doc.tasks["T3"]["citations"] == ["4.3", "Q2"]
    # the parent holds the cited sections and rules whose identifiers the citing sections leave out
    parent = (FIXTURES / "specs" / "parent1.md").read_text(encoding="utf-8")
    for sec in ("## 4.1 ", "## 4.2 ", "## 4.3 ", "Q2:"):
        assert sec in parent
    for ident in ("door_open_ms", "DoorTimeout", "code_ttl_min", "open_limit_s"):
        assert f"`{ident}`" in parent and ident not in doc.text
    assert "alarm_events" in doc.text


def test_doc1_reads_with_the_doc_dictionary():
    doc = plan.read(FIXTURES / "docs" / "doc1.md", "doc")
    assert doc.format == "doc"
    crit = doc.of("criterion")
    texts = [b["text"] for b in crit]
    # a count, a universal claim and a completeness word, each in a sentence of its own task section
    assert any(re.search(r"\b3 report formats\b", t) for t in texts)
    assert any("C6" in set_word_classes(t) for t in texts)
    assert any("C1" in set_word_classes(t) for t in texts)
    # the fenced command is a criterion block of its own, cut without the fence lines
    (cmd,) = [t for t in texts if t.startswith("exporter run")]
    assert "```" not in cmd and cmd == "exporter run --format csv --out reports/"
    fence = next(i for i, ln in enumerate(doc.lines, 1) if ln.startswith("```bash"))
    assert by_id(doc, [b["id"] for b in crit if b["text"] == cmd][0])["line_start"] == (
        fence + 1
    )
    assert doc.of("constraint") == [] and doc.of("edit_target") == []
    assert doc.of("gate") == []
