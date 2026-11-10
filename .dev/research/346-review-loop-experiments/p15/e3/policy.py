"""E3 truth table (contract J7): pure functions, every combination of answer bands has an outcome.

decide(code_outcome, result, thr) -> "RETAIN" | "CONFIRMED" | "VERIFIER".  There is no rejection output: Jev never rejects or
demotes; anything that is not an explicit joint confirmation goes to the conventional verifier.  Confidence is never read and
probabilities are never combined; each enters through its own threshold."""

RETAIN, CONFIRMED, VERIFIER = "RETAIN", "CONFIRMED", "VERIFIER"
DECISIONS = (RETAIN, CONFIRMED, VERIFIER)
CODE_OUTCOMES = ("EXCEPTION", "QUOTE_FAIL", "OK")

# Bands of one Noul answer against its own threshold: "high" (p >= t) or "low" (p < t).  Two bands per Noul keep the table
# exhaustive; a probability near 0.5 is below every frozen threshold and so routes to the verifier.


def _get(result, name):
    if result is None:
        return None
    if isinstance(result, dict):
        return result.get(name)
    return getattr(result, name, None)


def _p(answers, name):
    a = (answers or {}).get(name)
    if not isinstance(a, dict) or a.get("type") != "noul":
        return None
    v = a.get("p")
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return float(v)


def band(p, t):
    return "high" if p is not None and p >= t else "low"


def decide(code_outcome, result, thr, evidence_count=None):
    """`result`: a jevlib Result or a dict with `status` and `answers` (None when no call was made).  `evidence_count`: 1 or 2 when
    the caller knows it; None infers 'asked' from the presence of `texts_conflict` in the answers."""
    if code_outcome == "EXCEPTION":
        return RETAIN
    if code_outcome != "OK":
        return VERIFIER                     # QUOTE_FAIL, or anything unknown: the verifier decides
    if _get(result, "status") != "ok":
        return VERIFIER                     # invalid / unavailable / refused / missing result is never an answer
    answers = _get(result, "answers")
    suff, follows = _p(answers, "evidence_sufficient"), _p(answers, "outcome_follows")
    if suff is None or follows is None:
        return VERIFIER                     # missing answer
    conflict = _p(answers, "texts_conflict")
    asked = (evidence_count == 2) if evidence_count is not None else (conflict is not None)
    if asked and conflict is None:
        return VERIFIER
    if suff >= thr["t_suff"] and follows >= thr["t_follow"] and (not asked or conflict >= thr["t_conflict"]):
        return CONFIRMED
    return VERIFIER


def table_rows(thr):
    """Every band combination with its decision (documentation and exhaustive test)."""
    rows = []
    rows.append(("EXCEPTION", "-", "-", "-", "-", RETAIN))
    rows.append(("QUOTE_FAIL", "-", "-", "-", "-", VERIFIER))
    rows.append(("OK", "not ok", "-", "-", "-", VERIFIER))
    for s in ("high", "low"):
        for f in ("high", "low"):
            for c in ("high", "low", "not asked"):
                ok = s == "high" and f == "high" and c in ("high", "not asked")
                rows.append(("OK", "ok", s, f, c, CONFIRMED if ok else VERIFIER))
    return rows
