"""Transports (contract J1.4): urllib for live calls, a scripted mock for tests and dry runs."""
import json
import random
import socket
import ssl
import time
import urllib.error
import urllib.request
from typing import NamedTuple

from .config import MODEL
from .questions import canonical_bytes


class TransportTimeout(Exception):
    pass


class TransportError(Exception):
    """Connection reset, DNS, TLS, proxy refusal."""


class UrllibTransport:
    """urllib with ssl.create_default_context() (honours SSL_CERT_FILE) and HTTPS_PROXY from the environment."""

    def post(self, url: str, headers: dict, body: bytes, timeout: float):
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as resp:
                return resp.status, dict(resp.headers), resp.read()
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), e.read()
        except (socket.timeout, TimeoutError) as e:
            raise TransportTimeout(str(e))
        except urllib.error.URLError as e:
            if isinstance(e.reason, (socket.timeout, TimeoutError)):
                raise TransportTimeout(str(e))
            raise TransportError(str(e))
        except (ConnectionError, ssl.SSLError) as e:
            raise TransportError(str(e))


class MockStep(NamedTuple):
    status: int = 200
    body: object = None            # bytes | dict | None
    headers: dict = {}
    exc: Exception = None


class MockTransport:
    """Scripted: a list of MockStep consumed in order, or a callable(req_dict) -> MockStep.
    Records (url, headers_without_authorization, body) for every request; never stores Authorization."""

    def __init__(self, script, delay: float = 0.0, sleep=time.sleep):
        self.script = script
        self.calls = []
        self.delay = delay
        self.sleep = sleep
        self._i = 0

    def post(self, url, headers, body, timeout):
        safe = {k: v for k, v in dict(headers).items() if k.lower() != "authorization"}
        self.calls.append((url, safe, body))
        if self.delay:
            self.sleep(self.delay)
        if callable(self.script):
            step = self.script(json.loads(body.decode("utf-8")))
        else:
            if self._i >= len(self.script):
                raise AssertionError("MockTransport script exhausted")
            step = self.script[self._i]
            self._i += 1
        if step.exc is not None:
            raise step.exc
        b = step.body
        if b is None:
            b = b""
        elif isinstance(b, (dict, list)):
            b = json.dumps(b).encode("utf-8")
        elif isinstance(b, str):
            b = b.encode("utf-8")
        return step.status, dict(step.headers or {}), b


def fake_answer(req: dict, rng_seed: int = 0, p=None) -> dict:
    """A VALID response body for any request (tests and dry-run only)."""
    rng = random.Random(rng_seed)
    answers = {}
    for name in sorted(req["questions"]):
        q = req["questions"][name]
        if q["type"] == "noul":
            v = rng.random() if p is None else float(p)
            answers[name] = {"type": "noul", "noul": v}
        else:
            opts = list(q["criteria"])
            w = [rng.random() + 0.05 for _ in opts]
            s = sum(w)
            probs = {o: x / s for o, x in zip(opts, w)}
            best = max(opts, key=lambda o: probs[o])
            answers[name] = {"type": "choice", "choice": best, "confidence": probs[best], "probabilities": probs}
    return {"model": MODEL, "answers": answers,
            "usage": {"input_tokens": len(canonical_bytes(req)) // 4, "output_tokens": 5}}
