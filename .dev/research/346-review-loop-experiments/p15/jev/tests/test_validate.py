import json

import pytest

from jevlib.questions import build_request, choice, noul
from jevlib.transport import fake_answer
from jevlib.validate import Invalid, validate_response


def req():
    return build_request({"m": "x"}, {
        "late": noul("Late?", "yes late", "not late"),
        "when": choice("When?", {"early": "came before the date", "on_time": "came on the date", "late": "came after the date"}),
    })


def good():
    return {"model": "jev-1.14.0",
            "answers": {"late": {"type": "noul", "noul": 0.8},
                        "when": {"type": "choice", "choice": "late", "confidence": 0.7,
                                 "probabilities": {"early": 0.1, "on_time": 0.2, "late": 0.7}}},
            "usage": {"input_tokens": 100, "output_tokens": 5}}


def run(body, status=200, r=None):
    raw = body if isinstance(body, bytes) else json.dumps(body).encode()
    return validate_response(r or req(), status, raw)


def code(body, status=200, r=None):
    with pytest.raises(Invalid) as e:
        run(body, status, r)
    return e.value.code


def test_valid_mixed_response_round_trip():
    r = req()
    out = validate_response(r, 200, json.dumps(fake_answer(r, 3)).encode())
    assert set(out["answers"]) == {"late", "when"}
    assert out["answers"]["late"]["type"] == "noul" and 0 <= out["answers"]["late"]["p"] <= 1
    w = out["answers"]["when"]
    assert w["choice"] == max(w["probs"], key=w["probs"].get) and w["confidence"] == max(w["probs"].values())
    assert out["usage"]["output_tokens"] == 5
    assert run(good())["answers"]["late"]["p"] == 0.8


def test_http_status():
    assert code(good(), status=500) == "http_500"


def test_not_json_and_not_object():
    assert code(b"<html>") == "not_json"
    assert code(b"[1,2]") == "not_object"


def test_model_mismatch_alias_drift():
    b = good(); b["model"] = "jev-latest"
    assert code(b) == "model_mismatch"
    b["model"] = "jev-1.13.0"
    assert code(b) == "model_mismatch"


def test_answers_missing():
    b = good(); del b["answers"]
    assert code(b) == "answers_missing"


def test_extra_answer_key():
    b = good(); b["answers"]["bonus"] = {"type": "noul", "noul": 0.5}
    assert code(b) == "keys_mismatch"


def test_missing_answer_key():
    b = good(); del b["answers"]["late"]
    assert code(b) == "keys_mismatch"


def test_type_mismatch():
    b = good(); b["answers"]["late"] = {"type": "choice", "choice": "x", "confidence": 1, "probabilities": {"x": 1}}
    assert code(b) == "type_mismatch"


def test_unknown_answer_type_invalidates_whole_set():
    b = good(); b["answers"]["late"] = {"type": "score", "score": 0.5}
    assert code(b) == "unknown_type"


def test_noul_out_of_range():
    for v in (1.5, -0.1, "0.5", None, True):
        b = good(); b["answers"]["late"]["noul"] = v
        assert code(b) == "noul_bad"


def test_infinite_value():
    raw = json.dumps(good()).replace('"noul": 0.8', '"noul": 1e999').encode()
    assert code(raw) == "noul_bad"
    raw = json.dumps(good()).replace('"noul": 0.8', '"noul": NaN').encode()
    assert code(raw) == "noul_bad"


def test_bool_is_not_a_number():
    b = good(); b["answers"]["when"]["probabilities"]["early"] = True
    assert code(b) == "prob_bad"
    b = good(); b["usage"]["input_tokens"] = True
    assert code(b) == "usage_bad"


def test_choice_bad():
    b = good(); b["answers"]["when"]["choice"] = "maybe"
    assert code(b) == "choice_bad"


def test_prob_keys_mismatch():
    b = good(); del b["answers"]["when"]["probabilities"]["early"]
    assert code(b) == "prob_keys_mismatch"


def test_prob_bad():
    b = good(); b["answers"]["when"]["probabilities"]["early"] = -0.1
    assert code(b) == "prob_bad"


def test_prob_sum_tolerance_edges():
    def with_sum(s):
        b = good()
        b["answers"]["when"]["probabilities"] = {"early": 0.0, "on_time": round(s - 0.7, 6), "late": 0.7}
        return b
    run(with_sum(0.98)); run(with_sum(1.02))
    for s in (0.979, 1.021):
        assert code(with_sum(s)) == "prob_sum"


def test_choice_not_argmax():
    b = good(); b["answers"]["when"]["choice"] = "early"
    assert code(b) == "choice_not_argmax"


def test_confidence_bad():
    for v in (None, 1.5, float("nan")):
        b = good(); b["answers"]["when"]["confidence"] = v
        raw = json.dumps(b).encode()
        assert code(raw) == "confidence_bad"
    b = good(); del b["answers"]["when"]["confidence"]
    assert code(b) == "confidence_bad"


def test_usage_missing():
    b = good(); del b["usage"]
    assert code(b) == "usage_missing"
    b = good(); del b["usage"]["output_tokens"]
    assert code(b) == "usage_missing"


def test_usage_bad():
    b = good(); b["usage"]["input_tokens"] = -3
    assert code(b) == "usage_bad"
    b = good(); b["usage"]["input_tokens"] = 1.5
    assert code(b) == "usage_bad"


def test_extra_top_level_keys_ignored():
    b = good(); b["extra"] = 1
    run(b)
