#!/usr/bin/env python3
"""Curated model data for ccsession: profiles plus the shim's picker rules.

The data changes whenever models are added or retired, far more often than
the code, so it lives in ccsession-models.json instead of in the scripts.
Every ccsession launch asks GitHub whether a newer copy exists (a
conditional request that returns "not modified" when nothing changed) and
caches it, so existing installs get new models and profiles without a
reinstall. The file is data only: it is validated and never executed.

Active copy = the newest valid one of the downloaded cache and the copy
shipped with this skill; if neither is usable, a minimal built-in default.

Commands (used by the ccsession script):
  refresh [--wait SECONDS]  fetch a newer copy if one exists; prints one line
                            when the active data changed; never fails
  resolve PROFILE           print a profile's settings as KEY=value lines
  profiles                  print name, aliases, label, needs-shim per profile
  status                    print where the active data came from
"""

import json
import os
import re
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

SUPPORTED_SCHEMA = 1
DEFAULT_URL = (
    "https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/"
    "src/superclaude/skills/ccsession-tag/ccsession-models.json"
)
BUNDLED = Path(__file__).resolve().parent / "ccsession-models.json"
_MAX_BYTES = 256 * 1024
_ID = re.compile(r"^[A-Za-z0-9._/:\-\[\]]{1,128}$")
_NAME = re.compile(r"^[A-Za-z0-9._-]{1,32}$")
_LABEL = re.compile(r"^[^\x00-\x1f`$\\]{0,80}$")
_MINIMAL = {
    "schema": SUPPORTED_SCHEMA,
    "version": "0",
    "profiles": {
        "claude": {
            "aliases": [],
            "model": "claude-opus-5-5[1m]",
            "context": 1000000,
            "compact_window": 1000000,
            "requires_shim": False,
            "label": "Opus 5.5 and 1M context",
        }
    },
    "picker": {
        "remove": [],
        "pinned": [],
        "tail": [],
        "one_million_context": [],
        "display_overrides": {},
    },
}


def cache_dir() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "ccsession"


def _ids(value, limit=500):
    return (
        isinstance(value, list)
        and len(value) <= limit
        and all(isinstance(v, str) and _ID.match(v) for v in value)
    )


def validate(data) -> str:
    """Return an empty string for valid data, else the first problem found."""
    if not isinstance(data, dict):
        return "not a JSON object"
    if data.get("schema") != SUPPORTED_SCHEMA:
        return f"unsupported schema {data.get('schema')!r}"
    if not isinstance(data.get("version"), str) or not _NAME.match(data["version"]):
        return "missing or invalid version"
    profiles = data.get("profiles")
    if not isinstance(profiles, dict) or not profiles or len(profiles) > 100:
        return "profiles must be a non-empty object"
    seen = set()
    for name, p in profiles.items():
        if not _NAME.match(name) or not isinstance(p, dict):
            return f"invalid profile {name!r}"
        names = [name] + list(p.get("aliases", []))
        if not _ids(p.get("aliases", []), 10) or seen & set(names):
            return f"profile {name!r} has invalid or duplicate aliases"
        seen.update(names)
        if not isinstance(p.get("model"), str) or not _ID.match(p["model"]):
            return f"profile {name!r} has an invalid model"
        for key in ("context", "compact_window"):
            v = p.get(key)
            if (
                not isinstance(v, int)
                or isinstance(v, bool)
                or not 1000 <= v <= 2000000
            ):
                return f"profile {name!r} has an invalid {key}"
        if not isinstance(p.get("requires_shim"), bool):
            return f"profile {name!r} needs requires_shim true or false"
        if not isinstance(p.get("label", ""), str) or not _LABEL.match(
            p.get("label", "")
        ):
            return f"profile {name!r} has an invalid label"
    picker = data.get("picker")
    if not isinstance(picker, dict):
        return "picker must be an object"
    for key in ("remove", "pinned", "tail", "one_million_context"):
        if not _ids(picker.get(key)):
            return f"picker.{key} must be a list of model ids"
    labels = picker.get("display_overrides")
    if not isinstance(labels, dict) or not all(
        _ID.match(k) and isinstance(v, str) and _LABEL.match(v)
        for k, v in labels.items()
    ):
        return "picker.display_overrides must map model ids to labels"
    return ""


def _read(path: Path):
    try:
        if path.stat().st_size > _MAX_BYTES:
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if not validate(data) else None


def load():
    """Return (data, source) for the active copy."""
    candidates = []
    cached = _read(cache_dir() / "models.json")
    if cached:
        candidates.append((cached, "downloaded"))
    bundled = _read(BUNDLED)
    if bundled:
        candidates.append((bundled, "bundled"))
    if not candidates:
        return _MINIMAL, "built-in minimum"
    # Version strings are date-serials ("2026-09-30.1"), so they sort by age.
    return max(candidates, key=lambda c: c[0]["version"])


def _summary(data) -> set:
    names = set(data["profiles"])
    return {f"profile {n}" for n in names} | {f"{m}" for m in data["picker"]["pinned"]}


def _change_line(old, new) -> str:
    added = sorted(_summary(new) - _summary(old))
    removed = sorted(_summary(old) - _summary(new))
    parts = [f"+{a}" for a in added] + [f"-{r}" for r in removed]
    detail = ": " + ", ".join(parts) if parts else ""
    return f"[ccsession] model list updated to {new['version']}{detail}"


def _fetch(url: str, result: dict) -> None:
    directory = cache_dir()
    etag_file = directory / "models.etag"
    headers = {"User-Agent": "ccsession"}
    try:
        if (directory / "models.json").is_file() and etag_file.is_file():
            headers["If-None-Match"] = etag_file.read_text().strip()
    except OSError:
        pass
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers=headers), timeout=10
        ) as response:
            body = response.read(_MAX_BYTES + 1)
            etag = response.headers.get("ETag", "")
        if len(body) > _MAX_BYTES:
            result["status"] = "too large"
            return
        data = json.loads(body)
        problem = validate(data)
        if problem:
            result["status"] = f"rejected: {problem}"
            return
        directory.mkdir(parents=True, exist_ok=True)
        for name, content in (("models.json", body), ("models.etag", etag.encode())):
            fd, tmp = tempfile.mkstemp(dir=directory, prefix=f".{name}.")
            with os.fdopen(fd, "wb") as handle:
                handle.write(content)
            os.replace(tmp, directory / name)
        result["status"] = "downloaded"
    except urllib.error.HTTPError as exc:
        result["status"] = "not modified" if exc.code == 304 else f"HTTP {exc.code}"
    except (OSError, ValueError) as exc:
        result["status"] = f"failed: {exc.__class__.__name__}"


def refresh(wait: float) -> str:
    """Fetch a newer copy within `wait` seconds; return the status text."""
    url = os.environ.get("CCSESSION_MODELS_URL", DEFAULT_URL)
    before, _ = load()
    result = {"status": "timed out"}
    worker = threading.Thread(target=_fetch, args=(url, result), daemon=True)
    worker.start()
    worker.join(wait)
    try:
        (cache_dir() / "models.checked").parent.mkdir(parents=True, exist_ok=True)
        (cache_dir() / "models.checked").write_text(
            f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')} {result['status']}\n"
        )
    except OSError:
        pass
    after, _ = load()
    if after["version"] != before["version"]:
        print(_change_line(before, after))
    return result["status"]


def resolve(name: str) -> int:
    data, _ = load()
    for profile_name, p in data["profiles"].items():
        if name == profile_name or name in p.get("aliases", []):
            print(f"PROFILE_MODEL={p['model']}")
            print(f"PROFILE_CONTEXT={p['context']}")
            print(f"PROFILE_COMPACT_WINDOW={p['compact_window']}")
            print(f"PROFILE_REQUIRES_SHIM={int(p['requires_shim'])}")
            return 0
    return 3


def main(argv) -> int:
    command = argv[1] if len(argv) > 1 else ""
    if command == "refresh":
        wait = float(argv[3]) if len(argv) > 3 and argv[2] == "--wait" else 2.0
        status = refresh(wait)
        if os.environ.get("CCSESSION_MODELS_VERBOSE"):
            print(f"[ccsession] model data check: {status}")
        return 0
    if command == "resolve" and len(argv) > 2:
        return resolve(argv[2])
    if command == "profiles":
        data, _ = load()
        for name, p in data["profiles"].items():
            aliases = ",".join(p.get("aliases", []))
            # \x1f (unit separator) cannot appear in a valid label, and unlike
            # a tab, bash `read` keeps empty fields between two of them.
            fields = (name, aliases, p.get("label", ""), str(int(p["requires_shim"])))
            print("\x1f".join(fields))
        return 0
    if command == "status":
        data, source = load()
        checked = cache_dir() / "models.checked"
        last = checked.read_text().strip() if checked.is_file() else "never"
        print(f"Model data version: {data['version']} ({source})")
        print(
            f"Source URL:         {os.environ.get('CCSESSION_MODELS_URL', DEFAULT_URL)}"
        )
        print(f"Cache:              {cache_dir() / 'models.json'}")
        print(f"Last check:         {last}")
        print(f"Profiles:           {', '.join(data['profiles'])}")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
