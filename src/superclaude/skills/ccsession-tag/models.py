#!/usr/bin/env python3
"""Curated model data for ccsession: profiles, tiers, and the shim's picker rules.

The data changes whenever models are added or retired, far more often than
the code, so it lives in ccsession-models.json instead of in the scripts.
Every ccsession launch asks GitHub whether a newer copy exists (a
conditional request that returns "not modified" when nothing changed) and
caches it, so existing installs get new models and profiles without a
reinstall. The file is data only: it is validated and never executed.

Active copy = the newest valid one of the downloaded cache and the copy
shipped with this skill; if neither is usable, a minimal built-in default.

Tier mode (Coder workspaces): the model names and context windows of each tier
live in the workspace env file (`export T2Model01=...`, `T2_WINDOW=...`), read
on every launch so a changed file applies without a new shell. This file names
only which env variables make up each tier. Tier mode is on when a tier window
variable (`T<N>_WINDOW`) exists; the Mac has none and keeps the profiles.

Commands (used by the ccsession script):
  refresh [--wait SECONDS]  fetch a newer copy if one exists; prints one line
                            when the active data changed; never fails
  resolve PROFILE           print a profile's settings as KEY=value lines
  profiles                  print name, aliases, label, needs-shim per profile
  status                    print where the active data came from
  tier-mode                 exit 0 when tier mode is on, 1 when off
  tier-resolve TIER         print a tier's launch settings as KEY=value lines
  model-resolve MODEL       print launch settings for one named model
  compact-settings [MODEL WINDOW]
                            print Claude Code settings JSON with a per-tier and
                            per-model auto-compact window (tier mode); MODEL is
                            the launched model when no tier has it
  tiers                     print name, label, models per tier (for --help)
  shim-port BASE            print the shim port for this session's settings
  code-digest SHIM          print the fingerprint of the shim code (SHIM + this file)
"""

import hashlib
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

SUPPORTED_SCHEMA = 2
DEFAULT_URL = (
    "https://raw.githubusercontent.com/IronbellyOrg/IronClaude/master/"
    "src/superclaude/skills/ccsession-tag/ccsession-models.json"
)
BUNDLED = Path(__file__).resolve().parent / "ccsession-models.json"
_MAX_BYTES = 256 * 1024
_ID = re.compile(r"^[A-Za-z0-9._/:\-\[\]]{1,128}$")
_NAME = re.compile(r"^[A-Za-z0-9._-]{1,32}$")
_LABEL = re.compile(r"^[^\x00-\x1f`$\\]{0,80}$")
_TIER = re.compile(r"^tier([0-9]{1,2})$")
_SLOT = re.compile(r"^T([0-9]{1,2})Model[0-9]{2}$")
# Only these names are taken from the workspace env file; nothing is executed.
_ENV_NAME = re.compile(
    r"^(T[0-9]{1,2}Model[0-9]{2}(_WINDOW)?|T[0-9]{1,2}_WINDOW|CCSESSION_DEFAULT_TIER)$"
)
_ENV_LINE = re.compile(r"^\s*export\s+([A-Za-z_][A-Za-z0-9_]*)=(.*?)\s*$")
DEFAULTS_FILE = "/etc/aidev02/aienv.d/defaults.sh"
DEFAULT_WINDOW = 200000  # what Claude Code assumes for a model it does not know
ONE_MILLION = 1000000
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
    "tiers": {},
    "picker": {
        "show": ["claude-opus-5-5"],
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
    tiers = data.get("tiers")
    if not isinstance(tiers, dict) or len(tiers) > 20:
        return "tiers must be an object"
    for name, t in tiers.items():
        if not _TIER.match(name) or not isinstance(t, dict):
            return f"invalid tier {name!r}"
        slots = t.get("models_env")
        if (
            not isinstance(slots, list)
            or not 1 <= len(slots) <= 10
            or not all(isinstance(v, str) and _SLOT.match(v) for v in slots)
        ):
            return f"tier {name!r} needs models_env: 1-10 names like T2Model01"
        if not isinstance(t.get("label", ""), str) or not _LABEL.match(
            t.get("label", "")
        ):
            return f"tier {name!r} has an invalid label"
    picker = data.get("picker")
    if not isinstance(picker, dict):
        return "picker must be an object"
    for key in ("remove", "pinned", "tail"):
        if key in picker:
            return f"picker.{key} was replaced by picker.show"
    for key in ("show", "one_million_context"):
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


def _version_key(version: str) -> list:
    # Numeric runs compare as numbers, so "2026-10-02.10" beats "2026-10-02.9".
    # re.split with a group alternates text/digits, so positions never mix types.
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", version)]


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
    return max(candidates, key=lambda c: _version_key(c[0]["version"]))


def _summary(data) -> set:
    names = set(data["profiles"])
    return {f"profile {n}" for n in names} | {f"{m}" for m in data["picker"]["show"]}


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
        cached = _read(directory / "models.json")
        if cached and _version_key(data["version"]) < _version_key(cached["version"]):
            # A server rollback must not discard the newer copy we already have.
            result["status"] = "older than cached"
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


# --- tier mode ---------------------------------------------------------------


def defaults_path() -> Path:
    # Absolute, so two launches with the same relative path from different
    # directories never share a shim (abspath, not resolve: symlinks kept).
    value = os.environ.get("AIDEV_AI_DEFAULTS_PATH")
    return (
        Path(os.path.abspath(os.path.expanduser(value)))
        if value
        else Path(DEFAULTS_FILE)
    )


def gateway_alias(model: str) -> str:
    """The picker id the shim shows for a gateway model (claude-gw-...)."""
    return "claude-gw-" + re.sub(r"[^A-Za-z0-9.]+", "-", model).strip("-").lower()


def read_defaults_file(path: Path) -> dict:
    """Parse tier settings from the workspace env file. Never sources it.

    Takes only `export NAME=value` lines whose NAME is a tier setting; quotes
    around the value are dropped. Returns {} when the file cannot be read.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return {}
    out = {}
    for line in lines:
        m = _ENV_LINE.match(line)
        if not m or not _ENV_NAME.match(m.group(1)):
            continue
        value = m.group(2)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        out[m.group(1)] = value
    return out


def tier_env(env=None) -> dict:
    """Tier settings: the workspace env file when present, else the environment.

    The file is read fresh on every call, so a file pushed into a running
    workspace applies to the next launch (and the next shim request) without a
    new shell. Orca does not pass these variables to its terminals, so the
    file is also how Orca sessions see them.
    """
    path = defaults_path()
    if path.is_file():
        return read_defaults_file(path)
    env = os.environ if env is None else env
    return {k: v for k, v in env.items() if _ENV_NAME.match(k)}


def tier_mode(env=None, tenv=None) -> bool:
    """Tier mode is on when a tier window variable exists (T<N>_WINDOW).

    Not keyed on T0Model01: the Coder env set that long before tier windows
    existed, and keying on it would switch tier mode on with no windows.
    """
    env = os.environ if env is None else env
    if env.get("CCSESSION_TIERS", "1") == "0":
        return False
    tenv = tier_env(env) if tenv is None else tenv
    return any(re.match(r"^T[0-9]{1,2}_WINDOW$", k) for k in tenv)


def _window(tenv, name):
    raw = tenv.get(name, "")
    if not raw.isdigit() or not 1000 <= int(raw) <= 2000000:
        raise ValueError(f"{name} is missing or not a number of tokens (got {raw!r})")
    return int(raw)


def tier_number(name: str) -> str:
    m = _TIER.match(name) or re.match(r"^([0-9]{1,2})$", name)
    if not m:
        raise ValueError(f"unknown tier {name!r} (use tier0, tier1, ... or 0, 1, ...)")
    return m.group(1)


def resolve_tiers(data=None, tenv=None) -> dict:
    """Return {tier name: {label, window, models: [(slot, model, window)]}}.

    Raises ValueError naming the first missing or invalid variable.
    """
    data = load()[0] if data is None else data
    tenv = tier_env() if tenv is None else tenv
    out = {}
    for name, t in data["tiers"].items():
        n = tier_number(name)
        models = []
        for slot in t["models_env"]:
            model = tenv.get(slot, "")
            if not model:
                raise ValueError(f"{slot} is not set (needed by {name})")
            if not _ID.match(model):
                raise ValueError(f"{slot} has an invalid model name {model!r}")
            models.append((slot, model, _window(tenv, f"{slot}_WINDOW")))
        out[name] = {
            "label": t.get("label", f"Tier {n}"),
            "window": _window(tenv, f"T{n}_WINDOW"),
            "models": models,
        }
    return out


def compact_settings(data=None, tenv=None, extra=None) -> dict:
    """Claude Code settings with an auto-compact window per tier and per model.

    Claude Code looks up modelSettings.<model>.autoCompactWindow for the
    CURRENT model, so a /model switch to another tier takes that tier's
    window without a restart (a CLAUDE_CODE_AUTO_COMPACT_WINDOW env value
    would pin one window for the whole session). Keys: the tier ids, and each
    tier model by its own id and by the claude-gw- id the picker shows.
    `extra` (model id, window) adds a model launched by name that no tier has.
    """
    per_model = {}
    if extra:
        model, window = extra
        per_model[re.sub(r"\[1m\]$", "", model)] = window
    for name, tier in resolve_tiers(data, tenv).items():
        per_model[f"claude-gw-{name}"] = tier["window"]
        for _, model, window in tier["models"]:
            for key in (model, gateway_alias(model)):
                per_model.setdefault(key, window)
    return {
        "modelSettings": {
            key: {"autoCompactWindow": max(100000, min(window, 1000000))}
            for key, window in per_model.items()
        }
    }


def model_window(model: str, data=None, tenv=None) -> tuple:
    """(window, where it came from) for a model chosen by name."""
    data = load()[0] if data is None else data
    tenv = tier_env() if tenv is None else tenv
    # Accept the "[1m]" form users copy from the picker or the Mac profiles.
    model = model[: -len("[1m]")] if model.endswith("[1m]") else model
    for key, value in sorted(tenv.items()):
        # The real name, or the claude-gw- id the show-all picker shows.
        if _SLOT.match(key) and model in (value, gateway_alias(value)):
            return _window(tenv, f"{key}_WINDOW"), key
    if model in data["picker"]["one_million_context"]:
        return ONE_MILLION, "not in any tier; 1M list"
    return DEFAULT_WINDOW, "not in any tier"


def _settings_key(env=None, tenv=None) -> list:
    """What makes one session's shim different from another's.

    Sessions that read the same workspace env file share one shim (it re-reads
    the file per request). Show-all, a different file, or tier settings taken
    from the environment (no file) each need their own shim.
    """
    env = os.environ if env is None else env
    key = []
    if env.get("CCSESSION_SHOW_ALL_MODELS") == "1":
        key.append("show-all")
    # Settings the shim fixes at start: a session that sets them differently
    # needs its own shim.
    for name in (
        "CCSESSION_TIERS",
        "CCSESSION_COOLDOWN_SECONDS",
        "CCSESSION_FIRST_BYTE_TIMEOUT",
    ):
        if env.get(name):
            key.append(f"{name}={env[name]}")
    path = defaults_path()
    if path.is_file():
        if str(path) != DEFAULTS_FILE:
            key.append(f"file={path}")
    else:
        tenv = tier_env(env) if tenv is None else tenv
        key.extend(f"{k}={v}" for k, v in sorted(tenv.items()))
    return key


def settings_digest(env=None, tenv=None) -> str:
    """Short fingerprint of the shim settings; reported in shim health."""
    return hashlib.sha256("\n".join(_settings_key(env, tenv)).encode()).hexdigest()[:16]


def code_digest(shim_path: str) -> str:
    """Fingerprint of the shim code: the shim script plus this file.

    A running shim reports the value it started with; a launch reuses a shim
    only when the code on disk is the same (an upgrade starts a new shim).
    """
    h = hashlib.sha256()
    for path in (shim_path, os.path.abspath(__file__)):
        try:
            with open(path, "rb") as fh:
                h.update(fh.read())
        except OSError:
            h.update(b"-")
    return h.hexdigest()[:16]


def shim_port(base: int, env=None, tenv=None) -> int:
    """Port of the shim for this session's settings (base port when shared).

    A collision between two different settings is caught by the health check
    (settings_digest); the launch then moves to another port and never stops
    the shim that other sessions may be using.
    """
    key = _settings_key(env, tenv)
    if not key:
        return base
    digest = hashlib.sha256("\n".join(key).encode()).digest()
    return base + 1 + int.from_bytes(digest[:2], "big") % 97


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
    if command == "tier-mode":
        return 0 if tier_mode() else 1
    if command == "tier-resolve" and len(argv) > 2:
        try:
            name = f"tier{tier_number(argv[2])}"
            tier = resolve_tiers().get(name)
        except ValueError as exc:
            print(f"ccsession: {exc}", file=sys.stderr)
            return 3
        if not tier:
            print(f"ccsession: unknown tier {argv[2]!r}", file=sys.stderr)
            return 3
        print(f"PROFILE_MODEL=claude-gw-{name}[1m]")
        print(f"PROFILE_CONTEXT={tier['window']}")
        print(f"PROFILE_COMPACT_WINDOW={tier['window']}")
        print("PROFILE_REQUIRES_SHIM=1")
        print(
            f"PROFILE_LABEL={tier['label']}: "
            + ", ".join(m for _, m, _ in tier["models"])
        )
        return 0
    if command == "compact-settings":
        extra = (argv[2], int(argv[3])) if len(argv) > 3 and argv[3].isdigit() else None
        try:
            print(json.dumps(compact_settings(extra=extra), separators=(",", ":")))
        except ValueError as exc:
            print(f"ccsession: {exc}", file=sys.stderr)
            return 3
        return 0
    if command == "model-resolve" and len(argv) > 2:
        model = argv[2]
        if not _ID.match(model):
            print(f"ccsession: invalid model name {model!r}", file=sys.stderr)
            return 3
        try:
            window, where = model_window(model)
        except ValueError as exc:
            print(f"ccsession: {exc}", file=sys.stderr)
            return 3
        if where.startswith("not in any tier"):
            print(
                f"[ccsession] WARNING: {model} is {where}; using a {window} token window",
                file=sys.stderr,
            )
        # Claude-named models are known to Claude Code, which reads a long
        # window only from the "[1m]" suffix (the profiles do the same).
        native = model.startswith(("claude", "anthropic"))
        suffix = (
            "[1m]"
            if native and window > DEFAULT_WINDOW and not model.endswith("]")
            else ""
        )
        print(f"PROFILE_MODEL={model}{suffix}")
        print(f"PROFILE_CONTEXT={window}")
        print(f"PROFILE_COMPACT_WINDOW={window}")
        print("PROFILE_REQUIRES_SHIM=1")
        print(f"PROFILE_LABEL={model} ({where})")
        return 0
    if command == "tiers":
        try:
            tiers = resolve_tiers()
        except ValueError as exc:
            print(f"ccsession: {exc}", file=sys.stderr)
            return 3
        default = tier_env().get("CCSESSION_DEFAULT_TIER", "")
        for name, t in tiers.items():
            mark = "1" if name == default else "0"
            models = ", ".join(m for _, m, _ in t["models"])
            print("\x1f".join((name, t["label"], str(t["window"]), models, mark)))
        return 0
    if command == "default-tier":
        value = tier_env().get("CCSESSION_DEFAULT_TIER", "")
        if not value:
            print(
                "[ccsession] WARNING: CCSESSION_DEFAULT_TIER is not set in the workspace env; using tier2",
                file=sys.stderr,
            )
            value = "tier2"
        else:
            try:
                tier_number(value)
            except ValueError:
                print(
                    f"ccsession: CCSESSION_DEFAULT_TIER={value!r} is not a tier (use tier0, tier1, ...)",
                    file=sys.stderr,
                )
                return 3
            try:
                defined = resolve_tiers()
            except ValueError as exc:
                print(f"ccsession: {exc}", file=sys.stderr)
                return 3
            if value not in defined:
                names = ", ".join(defined) or "none"
                print(
                    f"ccsession: CCSESSION_DEFAULT_TIER={value!r} is not a defined tier (defined: {names})",
                    file=sys.stderr,
                )
                return 3
        print(value)
        return 0
    if command == "settings-digest":
        print(settings_digest())
        return 0
    if command == "code-digest" and len(argv) > 2:
        print(code_digest(argv[2]))
        return 0
    if command == "shim-port" and len(argv) > 2:
        print(shim_port(int(argv[2])))
        return 0
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
        path = defaults_path()
        if tier_mode():
            source = str(path) if path.is_file() else "environment"
            try:
                names = ", ".join(resolve_tiers(data))
            except ValueError as exc:
                names = f"invalid ({exc})"
            print(f"Tier mode:          on (settings from {source}); tiers: {names}")
        else:
            print("Tier mode:          off (no T<N>_WINDOW in the workspace env)")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
