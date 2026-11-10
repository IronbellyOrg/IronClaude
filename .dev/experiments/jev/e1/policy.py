"""Truth table of plan section 2.3.  Pure functions.  Jev can only AUTO_CLOSE; every other outcome is a fallback or an OPEN by code."""
import _boot  # noqa: F401
from types import SimpleNamespace

OPEN = "OPEN"
NOT_ELIGIBLE = "NOT_ELIGIBLE"
FALLBACK = "FALLBACK"
AUTO_CLOSE = "AUTO_CLOSE"
DECISIONS = (OPEN, NOT_ELIGIBLE, FALLBACK, AUTO_CLOSE)

# starting values (plan 2.3), data of record in decision.toml [thresholds]
DEFAULT_THR = {"t_present_low": 0.3, "t_obl_high": 0.7, "t_contra_low": 0.3, "t_ctx_high": 0.7}
YES_NO_P = {"yes": 1.0, "no": 0.0, "uncertain": 0.5}   # contract J8
NOT_ELIGIBLE_PRECHECKS = ("stale", "unmapped", "deps", "oversize")


def band(p, low, high) -> str:
    """'low' (p < low), 'high' (p >= high), else 'mid'.  Used by the exhaustive band tests."""
    return "low" if p < low else ("high" if p >= high else "mid")


def _p(answers, name):
    a = (answers or {}).get(name)
    if not isinstance(a, dict) or a.get("type") != "noul":
        return None
    p = a.get("p")
    return p if isinstance(p, (int, float)) and not isinstance(p, bool) else None


def decide(precheck: str, result, thr: dict, n_deps: int = 0) -> str:
    """precheck: ok | noop | regressed | stale | unmapped | deps | oversize.  result: object with .status and .answers (jevlib Result) or None."""
    if precheck in ("noop", "regressed"):
        return OPEN
    if precheck in NOT_ELIGIBLE_PRECHECKS:
        return NOT_ELIGIBLE
    if precheck != "ok":
        raise ValueError(f"unknown precheck {precheck!r}")
    if result is None or getattr(result, "status", None) != "ok":
        return FALLBACK
    ans = result.answers
    present, obl, ctx = _p(ans, "defect_still_present"), _p(ans, "obligation_still_required"), _p(ans, "context_sufficient")
    contra = [_p(ans, f"contradicts_d{k}") for k in range(1, n_deps + 1)]
    if present is None or obl is None or ctx is None or any(c is None for c in contra):
        return FALLBACK
    if (present < thr["t_present_low"] and obl >= thr["t_obl_high"] and ctx >= thr["t_ctx_high"]
            and all(c < thr["t_contra_low"] for c in contra)):
        return AUTO_CLOSE
    return FALLBACK


def conventional_decide(precheck: str, answers: dict, thr: dict, n_deps: int = 0) -> str:
    """The conventional checker's yes/no/uncertain answers through the SAME table; OPEN replaces FALLBACK for non-closure rows."""
    ps = {}
    for name, v in (answers or {}).items():
        ps[name] = {"type": "noul", "p": YES_NO_P.get(str(v).strip().lower(), 0.5)}
    for name in ["defect_still_present", "obligation_still_required", "context_sufficient"] + [f"contradicts_d{k}" for k in range(1, n_deps + 1)]:
        ps.setdefault(name, {"type": "noul", "p": 0.5})   # a missing answer is uncertain
    d = decide(precheck, SimpleNamespace(status="ok", answers=ps), thr, n_deps)
    return OPEN if d == FALLBACK else d
