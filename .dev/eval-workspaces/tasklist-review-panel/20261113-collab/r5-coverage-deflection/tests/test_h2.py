"""T-10: H2 truncation, real-parser errors and the re-ask decision (R-02, R-28)."""
import json

from conftest import CT, cand_text, finding, report
from r5 import h2
from superclaude.cli.review.findings import flat, locate


def long_anchor():
    text = cand_text(CT)
    flat_text = flat(text)
    i = flat_text.index("## Task 2:")
    return flat_text[i: i + 251].strip()


def test_truncation_and_errors():
    a = long_anchor()
    assert len(flat(a)) >= 249
    rep = report([finding("F1", a, claim="x" * 350)])
    text, errors = h2.normalise(rep)
    assert errors == []
    line = next(x for x in text.splitlines() if x.startswith('{"id": "F1"') or x.startswith('{"id":"F1"'))
    f = json.loads(line)
    assert len(flat(f["anchor"])) == 200 and a.startswith(f["anchor"])
    assert locate(cand_text(CT), f["anchor"])
    assert len(f["claim"]) == 300


def test_bad_lines_need_reask():
    a = long_anchor()[:60]
    bad_sev = dict(finding("F1", a), severity="HIGH")
    minor_blk = finding("F2", a, sev="MINOR", blocking=True)
    _text, errors = h2.normalise(report([bad_sev, minor_blk, finding("F3", a)]))
    assert len(errors) == 2
    assert "line" in h2.reask_prompt(errors) and "complete corrected report" in h2.reask_prompt(errors)


def test_decide():
    two, one, three = [{}] * 2, [{}], [{}] * 3
    assert h2.decide(two, one, True, False) == (True, "fewer_errors")
    assert h2.decide(two, three, True, False)[0] is False
    assert h2.decide(two, [], False, False) == (False, "reask_model_mismatch")
    assert h2.decide(two, [], True, True)[0] is False
