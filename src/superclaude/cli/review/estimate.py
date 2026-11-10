"""Capture-recapture estimators for the number of defects a review has not found.

Pure and stdlib-only. Occasions are independent whole-document reviews of one
document version (contract C7); a defect is "captured" by the occasions that
reported it. Estimators:

- Chapman's bias-corrected Lincoln-Petersen (k = 2 only);
- Chao2 (bias-corrected incidence estimator);
- first-order jackknife (Burnham-Overton, model Mh);
- second-order jackknife (point estimate only).

All of them are lower-bound-ish when detection is correlated across occasions
(same model, same prompt), which is why the stop rule is conservative.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from typing import Any

SCHEMA = "review-estimate/1"
CAPTURE_SCHEMA = "review-capture/1"
Z95 = 1.96
RULE = (
    "stop = open_blocking == 0 and unseen_upper95 < 1.0, where unseen_upper95 is the larger of the "
    "Chao2 and jackknife-1 95% upper bounds minus the distinct defects already captured; "
    "fewer than 2 occasions gives stop = null"
)
REASON_STOP = "estimated remainder below 1 and no open blocking"
REASON_OPEN = "open blocking findings remain"
REASON_UNSEEN = "estimated unseen defects: upper 95% bound is 1.0 or more"
REASON_BOTH = "open blocking findings remain and estimated unseen defects: upper 95% bound is 1.0 or more"
REASON_FEW = "insufficient occasions"


class CaptureError(ValueError):
    """The capture input is invalid."""


def _r(x: float) -> float:
    return round(float(x) + 0.0, 6)


def counts(rows: Sequence[Iterable[Any]], k: int) -> dict[str, Any]:
    """Return S_obs, Q (j -> number of defects captured by exactly j occasions) and q (occasion -> uniques)."""
    sets = [frozenset(r) for r in rows]
    sets = [s for s in sets if s]
    qc = {j: 0 for j in range(1, k + 1)}
    q: dict[Any, int] = {}
    for s in sets:
        j = len(s)
        if j > k:
            raise CaptureError(f"a defect is captured by {j} occasions but k = {k}")
        qc[j] += 1
        if j == 1:
            (o,) = tuple(s)
            q[o] = q.get(o, 0) + 1
    return {"S_obs": len(sets), "Q": qc, "q": q}


def chapman(n1: int, n2: int, m: int) -> dict[str, Any]:
    n = (n1 + 1) * (n2 + 1) / (m + 1) - 1
    var = (n1 + 1) * (n2 + 1) * (n1 - m) * (n2 - m) / ((m + 1) ** 2 * (m + 2))
    s_obs = n1 + n2 - m
    half = Z95 * math.sqrt(max(var, 0.0))
    return {
        "N": _r(n),
        "var": _r(var),
        "ci95": [_r(max(n - half, s_obs)), _r(n + half)],
    }


def chao2(s_obs: int, q1: int, q2: int, k: int) -> dict[str, Any]:
    a = (k - 1) / k
    if q2 > 0:
        f0 = a * q1 * q1 / (2 * q2)
        r = q1 / q2
        var = q2 * (a / 2 * r**2 + a**2 * r**3 + a**2 / 4 * r**4)
    else:
        f0 = a * q1 * (q1 - 1) / 2
        n = s_obs + f0
        var = a * q1 * (q1 - 1) / 2 + a**2 * q1 * (2 * q1 - 1) ** 2 / 4
        if n > 0:
            var -= a**2 * q1**4 / (4 * n)
    var = max(var, 0.0)
    t = f0
    if t <= 0 or var <= 0:
        lo = hi = s_obs + max(t, 0.0)
    else:
        c = math.exp(Z95 * math.sqrt(math.log(1 + var / t**2)))
        lo, hi = s_obs + t / c, s_obs + t * c
    return {"N": _r(s_obs + f0), "f0": _r(f0), "var": _r(var), "ci95": [_r(lo), _r(hi)]}


def jackknife1(s_obs: int, q1: int, q: dict[Any, int], k: int) -> dict[str, Any]:
    a = (k - 1) / k
    n = s_obs + a * q1
    var = a * (sum(v * v for v in q.values()) - q1 * q1 / k)
    var = max(var, 0.0)
    half = Z95 * math.sqrt(var)
    return {
        "N": _r(n),
        "var": _r(var),
        "ci95": [_r(max(n - half, s_obs)), _r(n + half)],
    }


def jackknife2(s_obs: int, q1: int, q2: int, k: int) -> dict[str, Any]:
    n = (
        s_obs
        + q1 * (2 * k - 3) / k
        - (q2 * (k - 2) ** 2 / (k * (k - 1)) if k > 1 else 0.0)
    )
    return {"N": _r(n)}


def estimate_matrix(
    rows: Sequence[Iterable[Any]], k: int, open_blocking: int = 0
) -> dict[str, Any]:
    """Estimate from per-defect capture sets (each an iterable of occasion ids)."""
    if k < 1:
        raise CaptureError("k must be at least 1")
    sets = [frozenset(r) for r in rows]
    c = counts(sets, k)
    s_obs, qcount, q = c["S_obs"], c["Q"], c["q"]
    q1, q2 = qcount.get(1, 0), qcount.get(2, 0)
    chap = None
    if k == 2:
        occ = sorted({o for s in sets for o in s}, key=str)
        # n1, n2 over the two occasions; occasions absent from every defect contribute 0
        if len(occ) == 2:
            o1, o2 = occ
        elif len(occ) == 1:
            o1, o2 = occ[0], object()
        else:
            o1, o2 = object(), object()
        n1 = sum(1 for s in sets if o1 in s)
        n2 = sum(1 for s in sets if o2 in s)
        m = sum(1 for s in sets if o1 in s and o2 in s)
        chap = chapman(n1, n2, m)
    ch = chao2(s_obs, q1, q2, k)
    jk1 = jackknife1(s_obs, q1, q, k)
    jk2 = jackknife2(s_obs, q1, q2, k)
    unseen = max(ch["ci95"][1], jk1["ci95"][1]) - s_obs
    unseen = _r(max(unseen, 0.0))
    if k < 2:
        stop, reason = None, REASON_FEW
    else:
        open_ = open_blocking > 0
        unseen_big = unseen >= 1.0
        stop = (not open_) and (not unseen_big)
        if stop:
            reason = REASON_STOP
        elif open_ and unseen_big:
            reason = REASON_BOTH
        elif open_:
            reason = REASON_OPEN
        else:
            reason = REASON_UNSEEN
    return {
        "schema": SCHEMA,
        "k": k,
        "S_obs": s_obs,
        "Q": {str(j): v for j, v in qcount.items()},
        "chapman": chap,
        "chao2": ch,
        "jackknife1": jk1,
        "jackknife2": jk2,
        "unseen_upper95": unseen,
        "stop": stop,
        "reason": reason,
        "rule": RULE,
    }


def validate_capture(cap: Any) -> list[str]:
    errs: list[str] = []
    if not isinstance(cap, dict):
        return ["capture must be a JSON object"]
    if cap.get("schema") != CAPTURE_SCHEMA:
        errs.append(f"schema must be {CAPTURE_SCHEMA!r}")
    occ = cap.get("occasions")
    if (
        not isinstance(occ, list)
        or not occ
        or not all(isinstance(o, str) and o for o in occ)
    ):
        errs.append("occasions must be a non-empty list of non-empty strings")
        occ = []
    elif len(set(occ)) != len(occ):
        errs.append("occasions must be unique")
    defects = cap.get("defects")
    if not isinstance(defects, list):
        errs.append("defects must be a list")
        return errs
    seen: set[str] = set()
    for i, d in enumerate(defects):
        if not isinstance(d, dict):
            errs.append(f"defects[{i}] must be an object")
            continue
        key = d.get("key")
        if not isinstance(key, str) or not key:
            errs.append(f"defects[{i}].key must be a non-empty string")
        elif key in seen:
            errs.append(f"defects[{i}].key {key!r} is duplicated")
        else:
            seen.add(key)
        if not isinstance(d.get("blocking"), bool):
            errs.append(f"defects[{i}].blocking must be a bool")
        cb = d.get("captured_by")
        if not isinstance(cb, list) or not all(isinstance(x, str) for x in cb):
            errs.append(f"defects[{i}].captured_by must be a list of strings")
        else:
            bad = [x for x in cb if x not in occ]
            if bad:
                errs.append(
                    f"defects[{i}].captured_by names unknown occasions {sorted(set(bad))}"
                )
    return errs


def estimate_capture(
    cap: Any, blocking_only: bool = False, open_blocking: int = 0
) -> dict[str, Any]:
    errs = validate_capture(cap)
    if errs:
        raise CaptureError("; ".join(errs))
    rows = [
        frozenset(d["captured_by"])
        for d in cap["defects"]
        if (d["blocking"] or not blocking_only)
    ]
    return estimate_matrix(rows, len(cap["occasions"]), open_blocking=open_blocking)
