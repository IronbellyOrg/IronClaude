"""Strict, all-or-nothing response validator (contract J1.3)."""
import json
import math

from .config import MODEL, PROB_SUM_TOL


class Invalid(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _fin(x):
    return _num(x) and math.isfinite(x)


def validate_response(req: dict, status: int, raw: bytes) -> dict:
    if status != 200:
        raise Invalid(f"http_{status}", "non-200 status")
    try:
        body = json.loads(raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw)
    except (ValueError, UnicodeDecodeError) as e:
        raise Invalid("not_json", str(e))
    if not isinstance(body, dict):
        raise Invalid("not_object", type(body).__name__)
    if body.get("model") != MODEL:
        raise Invalid("model_mismatch", f"returned {body.get('model')!r}, expected {MODEL!r}")
    answers = body.get("answers")
    if not isinstance(answers, dict) or not answers:
        raise Invalid("answers_missing")
    questions = req["questions"]
    if set(answers) != set(questions):
        raise Invalid("keys_mismatch", f"answers {sorted(answers)} vs questions {sorted(questions)}")
    names = sorted(questions)
    # type checks (a known type that differs from the question's is type_mismatch; an unknown type is unknown_type)
    for n in names:
        a = answers[n]
        if not isinstance(a, dict):
            raise Invalid("type_mismatch", f"{n}: answer is not an object")
        t = a.get("type")
        if t not in ("noul", "choice"):
            raise Invalid("unknown_type", f"{n}: {t!r}")
        if t != questions[n]["type"]:
            raise Invalid("type_mismatch", f"{n}: answer {t} vs question {questions[n]['type']}")
    for n in names:
        if questions[n]["type"] == "noul":
            v = answers[n].get("noul")
            if not _fin(v) or not 0.0 <= v <= 1.0:
                raise Invalid("noul_bad", f"{n}: {v!r}")
    for n in names:
        if questions[n]["type"] == "choice":
            a = answers[n]
            opts = set(questions[n]["criteria"])
            if not isinstance(a.get("choice"), str) or a["choice"] not in opts:
                raise Invalid("choice_bad", f"{n}: {a.get('choice')!r}")
    for n in names:
        if questions[n]["type"] == "choice":
            probs = answers[n].get("probabilities")
            if not isinstance(probs, dict) or set(probs) != set(questions[n]["criteria"]):
                raise Invalid("prob_keys_mismatch", n)
    for n in names:
        if questions[n]["type"] == "choice":
            for k, v in answers[n]["probabilities"].items():
                if not _fin(v) or not 0.0 <= v <= 1.0:
                    raise Invalid("prob_bad", f"{n}.{k}: {v!r}")
    for n in names:
        if questions[n]["type"] == "choice":
            s = sum(answers[n]["probabilities"].values())
            if abs(s - 1.0) > PROB_SUM_TOL + 1e-9:
                raise Invalid("prob_sum", f"{n}: {s}")
    for n in names:
        if questions[n]["type"] == "choice":
            probs = answers[n]["probabilities"]
            if probs[answers[n]["choice"]] < max(probs.values()) - 1e-9:
                raise Invalid("choice_not_argmax", n)
    for n in names:
        if questions[n]["type"] == "choice":
            c = answers[n].get("confidence")
            if not _fin(c) or not 0.0 <= c <= 1.0:
                raise Invalid("confidence_bad", f"{n}: {c!r}")
    usage = body.get("usage")
    if not isinstance(usage, dict) or "input_tokens" not in usage or "output_tokens" not in usage:
        raise Invalid("usage_missing")
    for k in ("input_tokens", "output_tokens"):
        v = usage[k]
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise Invalid("usage_bad", f"{k}: {v!r}")
    out = {}
    for n in names:
        a = answers[n]
        if a["type"] == "noul":
            out[n] = {"type": "noul", "p": float(a["noul"])}
        else:
            out[n] = {"type": "choice", "choice": a["choice"],
                      "probs": {k: float(v) for k, v in a["probabilities"].items()},
                      "confidence": float(a["confidence"])}
    return {"model": body["model"], "answers": out,
            "usage": {"input_tokens": usage["input_tokens"], "output_tokens": usage["output_tokens"]}}
