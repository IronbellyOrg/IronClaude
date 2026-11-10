"""Raw request/response journal, schema jev-journal/1 (contract J5). Headers are never written."""
import datetime
import json
import os
import pathlib

from .redact import redact

MAX_RAW = 1_000_000


class Journal:
    def __init__(self, path):
        self.path = pathlib.Path(path)

    def write(self, record: dict) -> None:
        rec = dict(record)
        rec.setdefault("schema", "jev-journal/1")
        rec.setdefault("ts_utc", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
        raw = rec.get("response_raw")
        if isinstance(raw, (bytes, bytearray)):
            raw = bytes(raw).decode("utf-8", errors="replace")
        if isinstance(raw, str) and len(raw) > MAX_RAW:
            raw = raw[:MAX_RAW]
        rec["response_raw"] = raw
        rec.pop("headers", None)
        rec = redact(rec)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(rec, ensure_ascii=False, default=str) + "\n"
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
