"""Response cache (contract J1.6): one JSON file per request_sha256; stores only validated ok results."""
import json
import pathlib

FIELDS = ("status", "error", "answers", "usage", "model", "attempts", "latency_ms")


class ResponseCache:
    def __init__(self, dir, phase=None):
        if phase == "live":
            raise ValueError("a response cache is never used in a live phase")
        self.dir = pathlib.Path(dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _p(self, sha):
        return self.dir / f"{sha}.json"

    def get(self, sha):
        p = self._p(sha)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text())
        except ValueError:
            return None

    def put(self, sha, result) -> None:
        if getattr(result, "status", None) != "ok":
            return
        rec = {k: getattr(result, k) for k in FIELDS}
        rec["request_sha256"] = sha
        self._p(sha).write_text(json.dumps(rec))
