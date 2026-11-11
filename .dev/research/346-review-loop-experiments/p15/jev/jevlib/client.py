"""JevClient: the only code path that talks to Jev (contract J1.5, J1.6)."""
import collections
import json
import math
import os
import time
from dataclasses import dataclass

from . import config as C
from .budget import Budget, BudgetExhausted, usd
from .cache import ResponseCache
from .journal import Journal
from .manifest import privacy_violation
from .questions import BuildError, build_request, canonical_bytes, request_sha256, wire_bytes
from .transport import TransportError, TransportTimeout, UrllibTransport
from .validate import Invalid, validate_response

RETRY_STATUS = {429, 529, 500, 502, 503, 504}


class KeyMissing(Exception):
    """JEV_API_KEY unset while live=True: a hard error, never a fallback."""


class KeyRejected(Exception):
    """401/403: configuration error, no retry, no fallback."""


@dataclass
class Result:
    status: str                  # "ok" | "invalid" | "unavailable" | "refused"
    error: object                # validator / transport / refusal code
    answers: object
    usage: object
    model: object
    attempts: int
    latency_ms: int
    logical_call_id: str
    request_sha256: str


def _hget(headers, name):
    for k, v in (headers or {}).items():
        if k.lower() == name.lower():
            return v
    return None


class JevClient:
    def __init__(self, *, experiment: str, phase: str, budget: Budget, journal: Journal,
                 transport=None, live: bool = False, cache=None,
                 allowed_classes=C.ALLOWED_DATA_CLASSES, clock=time.monotonic, sleep=time.sleep):
        if cache is not None and phase == "live":
            raise ValueError("the response cache is forbidden in a live phase")
        self.experiment, self.phase = experiment, phase
        self.budget, self.journal = budget, journal
        self.live = live
        self.transport = transport if transport is not None else (UrllibTransport() if live else None)
        self.cache = cache
        self.allowed = set(allowed_classes)
        self.clock, self.sleep = clock, sleep
        self._counter = collections.Counter()

    # ------------------------------------------------------------------
    def _next_id(self, case_id, qset_version):
        self._counter[(case_id, qset_version)] += 1
        return f"{self.experiment}:{self.phase}:{case_id}:{qset_version}:{self._counter[(case_id, qset_version)]}"

    def _log(self, base, **kw):
        rec = dict(base)
        rec.update(kw)
        try:
            rec["budget_after"] = {"spent_usd": self.budget.state()["spent_usd"]}
        except Exception:  # journalling must not break a call
            rec["budget_after"] = None
        self.journal.write(rec)

    def ask(self, state: dict, questions: dict, *, case_id: str, qset_version: str,
            data_classes, purpose: str, run=None, step=None) -> Result:
        lid = self._next_id(case_id, qset_version)
        t_start = self.clock()
        base = {"experiment": self.experiment, "phase": self.phase, "purpose": purpose, "case_id": case_id,
                "run": run, "step": step, "logical_call_id": lid, "qset_version": qset_version,
                "data_classes": sorted(data_classes or []), "attempt": 0, "final": False}

        def result(status, error, req_sha, attempts=0, answers=None, usage=None, model=None, **extra):
            lat = int((self.clock() - t_start) * 1000)
            r = Result(status, error, answers, usage, model, attempts, lat, lid, req_sha)
            self._log(base, final=True, attempt=attempts, request_sha256=req_sha,
                      validation="ok" if status == "ok" else error, usage=usage, model_returned=model,
                      result_status=status, error=error, latency_ms=lat, **extra)
            return r

        # (1) build
        req = build_request(state, questions)          # BuildError propagates: a caller bug
        sha = request_sha256(req)
        body = canonical_bytes(req)
        base["request_sha256"] = sha
        base["request"] = req
        est = int(math.ceil(len(body) / C.RESERVE_BYTES_PER_TOKEN))
        base["est_tokens"] = est
        # (2) privacy
        why = privacy_violation(req, data_classes, self.allowed)
        if why:
            return result("refused", "privacy", sha, detail=why)
        # (3) size
        if len(body) / C.SIZE_BYTES_PER_TOKEN > C.LIMIT_REQUEST_TOKENS:
            return result("refused", "oversize", sha)
        sb = len(canonical_bytes(req["state"]))
        for q in req["questions"].values():
            if (sb + len(canonical_bytes(q))) / C.SIZE_BYTES_PER_TOKEN > C.LIMIT_QUESTION_TOKENS:
                return result("refused", "oversize", sha)
        # (4) budget
        try:
            did = self.budget.draw(self.phase, est)
        except BudgetExhausted as e:
            return result("refused", "budget_exhausted", sha, detail=str(e))
        try:
            # (5) cache
            if self.cache is not None:
                hit = self.cache.get(sha)
                if hit is not None:
                    self.budget.settle(did, 0)
                    did = None
                    return result("ok", None, sha, attempts=0, answers=hit["answers"], usage=hit["usage"],
                                  model=hit["model"], cached=True)
            # (6) dry run
            if not self.live:
                self.budget.settle(did, 0)
                did = None
                return result("refused", "dry_run", sha)
            # (7) key
            key = os.environ.get(C.KEY_ENV)
            if not key:
                raise KeyMissing(f"{C.KEY_ENV} is not set (live call refused; never a fallback)")
            # (8)-(9) attempts
            return self._attempts(req, wire_bytes(req), sha, key, base, did, result, t_start)
        except BaseException:
            if did is not None:
                try:
                    self.budget.settle(did, 0)
                except Exception:
                    pass
            raise

    # ------------------------------------------------------------------
    def _attempts(self, req, body, sha, key, base, did, result, t_start):
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        deadline = t_start + C.LOGICAL_DEADLINE_S
        url = C.api_url()   # may raise ValueError on a bad $JEV_API_URL before anything is sent
        attempts = 0
        while True:
            attempts += 1
            t0 = self.clock()
            status, rheaders, raw, exc = None, {}, b"", None
            try:
                status, rheaders, raw = self.transport.post(
                    url, headers, body, timeout=max(1.0, min(C.ATTEMPT_TIMEOUT_S, deadline - t0)))
            except TransportTimeout as e:
                exc = ("timeout", e)
            except TransportError as e:
                exc = ("transport", e)
            lat = int((self.clock() - t0) * 1000)
            arec = dict(base, attempt=attempts, final=False, latency_ms=lat, http_status=status,
                        response_raw=raw if status is not None else (str(exc[1]) if exc else None))
            # classify
            retryable = exc is not None or status in RETRY_STATUS
            if exc is None and status == 200:
                try:
                    out = validate_response(req, status, raw)
                except Invalid as e:
                    self._log(arec, validation=e.code, usage=None, model_returned=None, result_status="invalid", error=e.code)
                    self.budget.settle(did, _usage_of(raw))
                    return result("invalid", e.code, sha, attempts=attempts, http_status=status, response_raw=raw)
                self._log(arec, validation="ok", usage=out["usage"], model_returned=out["model"],
                          result_status="ok", error=None)
                self.budget.settle(did, out["usage"]["input_tokens"])
                if self.cache is not None:
                    self.cache.put(sha, Result("ok", None, out["answers"], out["usage"], out["model"], attempts, lat,
                                               base["logical_call_id"], sha))
                return result("ok", None, sha, attempts=attempts, answers=out["answers"], usage=out["usage"],
                              model=out["model"], http_status=status, response_raw=raw)
            if exc is not None:
                code = exc[0]
            else:
                code = f"http_{status}"
            self._log(arec, validation=code, usage=None, model_returned=None, result_status="error", error=code)
            if exc is None and status in (401, 403):
                self.budget.settle(did, 0)
                raise KeyRejected(f"HTTP {status} from Jev: key missing, invalid or not permitted")
            if retryable:
                if attempts <= C.MAX_RETRIES:
                    ra = _hget(rheaders, "Retry-After")
                    try:
                        ra = float(ra) if ra is not None else 0.0
                    except ValueError:
                        ra = 0.0
                    wait = max(C.BACKOFF_S, min(ra, C.RETRY_AFTER_CAP_S))
                    if self.clock() + wait < deadline:
                        self.sleep(wait)
                        continue
                self.budget.settle(did, 0)
                return result("unavailable", code, sha, attempts=attempts, http_status=status)
            self.budget.settle(did, 0)
            if status == 400 and b"max_tokens_exceeded" in raw:
                return result("refused", "oversize_server", sha, attempts=attempts, http_status=status, response_raw=raw)
            return result("invalid", code, sha, attempts=attempts, http_status=status, response_raw=raw)


def _usage_of(raw):
    """Input tokens from a (possibly invalid) 200 body; None when absent (charged at the estimate)."""
    try:
        u = json.loads(raw.decode("utf-8")).get("usage")
        v = u.get("input_tokens")
        if isinstance(v, int) and not isinstance(v, bool) and v >= 0:
            return v
    except Exception:
        pass
    return None
