"""Request builder (contract J1.2). Question wording lives ONLY in each experiment's questions.py (J7)."""
import hashlib
import json
import math
import re

from .config import MODEL, QNAME_RE

MAX_DEPTH = 64
_POSITIONAL = re.compile(r"^(a|b|c|d|option_?\d+|choice_?\d+|left|right|\d+)$", re.I)


class BuildError(ValueError):
    pass


def noul(instructions: str, true: str, false: str) -> dict:
    return {"type": "noul", "instructions": instructions, "criteria": {"true": true, "false": false}}


def choice(instructions: str, options: dict) -> dict:
    return {"type": "choice", "instructions": instructions, "criteria": dict(options)}


def _depth(obj, d=1):
    if isinstance(obj, dict):
        return max([d] + [_depth(v, d + 1) for v in obj.values()])
    if isinstance(obj, (list, tuple)):
        return max([d] + [_depth(v, d + 1) for v in obj])
    return d


def _check_numbers(obj, where):
    if isinstance(obj, bool):
        return
    if isinstance(obj, float) and not math.isfinite(obj):
        raise BuildError(f"non-finite number in {where}")
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise BuildError(f"non-string key in {where}")
            _check_numbers(v, where)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _check_numbers(v, where)


def _nonempty_str(x, what):
    if not isinstance(x, str) or not x.strip():
        raise BuildError(f"{what} must be a non-empty string")


def build_request(state: dict, questions: dict, model: str = MODEL) -> dict:
    if not isinstance(state, dict):
        raise BuildError("state must be a JSON object")
    if not isinstance(questions, dict) or not questions:
        raise BuildError("questions must be a non-empty dict")
    _check_numbers(state, "state")
    if _depth(state) > MAX_DEPTH:
        raise BuildError("state nests deeper than 64")
    qs = {}
    for name, q in questions.items():
        if not isinstance(name, str) or not re.match(QNAME_RE, name):
            raise BuildError(f"bad question name {name!r}")
        if not isinstance(q, dict):
            raise BuildError(f"question {name} must be a dict")
        t = q.get("type")
        if t not in ("noul", "choice"):
            raise BuildError(f"question {name}: type {t!r} not allowed (only noul and choice)")
        _nonempty_str(q.get("instructions"), f"question {name} instructions")
        crit = q.get("criteria")
        if not isinstance(crit, dict):
            raise BuildError(f"question {name}: criteria missing")
        if _depth(crit) > MAX_DEPTH:
            raise BuildError(f"question {name}: criteria nest deeper than 64")
        _check_numbers(crit, f"question {name}")
        if t == "noul":
            if set(crit) != {"true", "false"}:
                raise BuildError(f"question {name}: a noul needs exactly true and false criteria")
            _nonempty_str(crit["true"], f"question {name} true criterion")
            _nonempty_str(crit["false"], f"question {name} false criterion")
        else:
            if not 2 <= len(crit) <= 255:
                raise BuildError(f"question {name}: a choice needs 2..255 options")
            for oname, desc in crit.items():
                if _POSITIONAL.match(oname):
                    raise BuildError(f"question {name}: positional option name {oname!r}")
                _nonempty_str(desc, f"question {name} option {oname}")
        qs[name] = {"type": t, "instructions": q["instructions"], "criteria": crit}
    req = {"model": model, "state": state, "questions": qs}
    try:
        canonical_bytes(req)
    except (ValueError, TypeError) as e:
        raise BuildError(f"request not serializable: {e}")
    return req


def canonical_bytes(req: dict) -> bytes:
    return json.dumps(req, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def wire_bytes(req: dict) -> bytes:
    """The body actually sent: same JSON as canonical_bytes but with insertion order preserved (option order and key order reach the
    model, which is what the probe's option-order check needs).  Hashing and size checks use canonical_bytes."""
    return json.dumps(req, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def request_sha256(req: dict) -> str:
    return hashlib.sha256(canonical_bytes(req)).hexdigest()
