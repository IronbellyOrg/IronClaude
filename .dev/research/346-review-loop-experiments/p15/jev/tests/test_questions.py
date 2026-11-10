import pytest

from jevlib.questions import BuildError, build_request, canonical_bytes, choice, noul, request_sha256


def _n():
    return noul("Is it late?", "It is late.", "It is on time.")


def test_noul_shape():
    req = build_request({"message": "x"}, {"late": _n()})
    assert req["model"] == "jev-1.14.0"
    q = req["questions"]["late"]
    assert q == {"type": "noul", "instructions": "Is it late?", "criteria": {"true": "It is late.", "false": "It is on time."}}


def test_choice_shape():
    c = choice("When?", {"early": "arrived before the date", "late": "arrived after the date"})
    req = build_request({"m": 1}, {"when": c})
    assert req["questions"]["when"]["type"] == "choice"
    assert list(req["questions"]["when"]["criteria"]) == ["early", "late"]


@pytest.mark.parametrize("bad", ["a", "B", "option_1", "choice2", "left", "right", "3"])
def test_rejects_positional_option_names(bad):
    with pytest.raises(BuildError):
        build_request({}, {"q": choice("x?", {bad: "some situation", "late": "another situation"})})


def test_rejects_bad_question_name():
    for name in ("Late", "1late", "late-x", "", "x" * 65):
        with pytest.raises(BuildError):
            build_request({}, {name: _n()})


def test_rejects_nan_and_deep_nesting():
    with pytest.raises(BuildError):
        build_request({"x": float("nan")}, {"q": _n()})
    with pytest.raises(BuildError):
        build_request({"x": float("inf")}, {"q": _n()})
    deep = cur = {}
    for _ in range(70):
        cur["k"] = {}
        cur = cur["k"]
    with pytest.raises(BuildError):
        build_request(deep, {"q": _n()})
    with pytest.raises(BuildError):
        build_request("not a dict", {"q": _n()})


def test_rejects_score_and_box():
    for t in ("score", "box"):
        with pytest.raises(BuildError):
            build_request({}, {"q": {"type": t, "instructions": "x"}})


def test_canonical_bytes_stable_under_key_order():
    a = build_request({"a": 1, "b": 2}, {"q": _n()})
    b = build_request({"b": 2, "a": 1}, {"q": _n()})
    assert canonical_bytes(a) == canonical_bytes(b)
    assert request_sha256(a) == request_sha256(b)
    c = build_request({"a": 1, "b": 3}, {"q": _n()})
    assert request_sha256(a) != request_sha256(c)
