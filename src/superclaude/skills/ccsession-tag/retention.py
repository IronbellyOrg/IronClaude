#!/usr/bin/env python3
"""Keep Claude Code from deleting named sessions after 30 days.

Claude Code deletes every saved conversation (a transcript file under
~/.claude/projects) whose file modification time is older than
``cleanupPeriodDays`` days. The default is 30. It has no exemption for a named
session, so a name in a ccsession list outlives its conversation after 30 days
and shows "(transcript missing)". The only protection is a larger value.

Claude Code reads the value from the first of these that sets it: its managed
settings (/etc/claude-code on Linux, /Library/Application Support/ClaudeCode on
macOS: managed-settings.json, then managed-settings.d/*.json in alphabetical
order, the last one wins), then the command line, the project's settings files,
then ~/.claude/settings.json. A managed value therefore cannot be overridden
from ~/.claude/settings.json. This script never writes under the managed
directory.

    retention.py ensure [<settings.json>]
        Install step: set cleanupPeriodDays in the user settings file
        (default ~/.claude/settings.json) to MIN_DAYS when the key is absent or
        lower. A larger value the user chose is never lowered. Nothing is
        written when managed settings already set the key (they win), when the
        file is not valid JSON, or when the value is not a whole number. A copy
        of an existing file is saved first as settings.json.bak.<UTC stamp>.
    retention.py check [<settings.json>]
        Print one line, and only when the value Claude Code will use is below
        MIN_DAYS, saying what it is, who set it and what to do. Prints nothing
        otherwise (including when the value cannot be read).

Both always exit 0, so a problem here never stops an install or a listing.
The command line and project settings files are not read: they apply to one
session or folder, and the managed and user files decide the rest.

CCSESSION_MANAGED_SETTINGS_DIR replaces the managed settings folder (for tests
and for a policy kept somewhere else).
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import stat
import sys
import tempfile
import time
from pathlib import Path

KEY = "cleanupPeriodDays"
# A year keeps a named session through any normal pause in the work and is still
# a limit. Disk is not the constraint: transcripts are a few GB at most.
MIN_DAYS = 365
DEFAULT_DAYS = 30  # Claude Code's own default when no file sets the key


def managed_dir() -> Path:
    override = os.environ.get("CCSESSION_MANAGED_SETTINGS_DIR")
    if override:
        return Path(override)
    if platform.system() == "Darwin":
        return Path("/Library/Application Support/ClaudeCode")
    return Path("/etc/claude-code")


def user_settings() -> Path:
    return Path.home() / ".claude" / "settings.json"


def is_days(value: object) -> bool:
    # bool is an int in Python; true is not a number of days.
    return isinstance(value, int) and not isinstance(value, bool)


def read_object(path: Path):
    """The JSON object in path, or None when it is missing, unreadable or not an object."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def managed_value():
    """(value, file) from managed settings, the last file that sets the key, or None."""
    root = managed_dir()
    files = [root / "managed-settings.json"]
    try:
        files += sorted(
            p
            for p in (root / "managed-settings.d").glob("*.json")
            if not p.name.startswith(".")
        )
    except OSError:
        pass
    found = None
    for path in files:
        data = read_object(path)
        if data is not None and KEY in data:
            found = (data[KEY], path)
    return found


def tilde(path: Path) -> str:
    text = str(path)
    home = str(Path.home())
    return "~" + text[len(home) :] if text.startswith(home + os.sep) else text


def check(settings: Path) -> str:
    """The warning line, or '' when retention is long enough or unknown."""
    managed = managed_value()
    if managed is not None:
        value, path = managed
        who = (
            "set by the managed settings file %s, which a value in %s cannot override"
            % (
                path,
                tilde(settings),
            )
        )
        advice = (
            "Ask whoever manages this machine to raise it to %d or more." % MIN_DAYS
        )
    else:
        data = read_object(settings)
        if data is not None and KEY in data:
            value = data[KEY]
            who = "set in %s" % tilde(settings)  # "<KEY> is set in <file>"
            advice = (
                "Raise it to %d or more (the ccsession installer does this)." % MIN_DAYS
            )
        else:
            value = DEFAULT_DAYS
            who = "not set, so Claude Code's default applies"
            advice = (
                'Run the ccsession installer (it sets %d) or add "%s": %d to %s.'
                % (MIN_DAYS, KEY, MIN_DAYS, tilde(settings))
            )
    if not is_days(value) or value >= MIN_DAYS:
        return ""
    return (
        "ccsession: Claude Code deletes saved sessions after %d days (%s is %s), "
        "so named sessions older than that lose their conversation. %s"
        % (value, KEY, who, advice)
    )


def write_settings(target: Path, data: dict) -> None:
    target = Path(os.path.realpath(target))  # a symlinked settings file stays a link
    mode = None
    if target.exists():
        mode = stat.S_IMODE(target.stat().st_mode)
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        shutil.copy2(target, target.with_name(target.name + ".bak." + stamp))
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, staged = tempfile.mkstemp(dir=str(target.parent), prefix=".settings-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        os.chmod(staged, 0o600 if mode is None else mode)
        os.replace(staged, target)
    finally:
        if os.path.exists(staged):
            os.unlink(staged)


def ensure(settings: Path) -> str:
    """Raise the user's value to MIN_DAYS when absent or lower; returns what happened."""
    managed = managed_value()
    if managed is not None:
        value, path = managed
        return (
            "%s is %s in the managed settings file %s; %s cannot override it, so it is left alone."
            % (KEY, value, path, tilde(settings))
        )
    data = {}
    if settings.exists():
        try:
            data = json.loads(settings.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return (
                'WARNING: %s is not valid JSON; %s left unset. Add "%s": %d yourself.'
                % (
                    tilde(settings),
                    KEY,
                    KEY,
                    MIN_DAYS,
                )
            )
        if not isinstance(data, dict):
            return "WARNING: %s is not a JSON object; %s left unset." % (
                tilde(settings),
                KEY,
            )
    current = data.get(KEY)
    if KEY in data and not is_days(current):
        return "WARNING: %s in %s is not a whole number (%r); left unchanged." % (
            KEY,
            tilde(settings),
            current,
        )
    if is_days(current) and current >= MIN_DAYS:
        return "%s is already %d in %s (at least %d); no change." % (
            KEY,
            current,
            tilde(settings),
            MIN_DAYS,
        )
    was = "not set" if KEY not in data else "was %d" % current
    data[KEY] = MIN_DAYS
    write_settings(settings, data)
    return (
        "Set %s to %d in %s (%s). Claude Code now keeps saved sessions for %d days."
        % (
            KEY,
            MIN_DAYS,
            tilde(settings),
            was,
            MIN_DAYS,
        )
    )


def main(argv: list) -> int:
    if len(argv) < 2 or argv[1] not in ("ensure", "check"):
        print("usage: retention.py ensure|check [<settings.json>]", file=sys.stderr)
        return 2
    settings = Path(argv[2]) if len(argv) > 2 else user_settings()
    try:
        text = ensure(settings) if argv[1] == "ensure" else check(settings)
    except OSError as exc:
        text = (
            "WARNING: could not update %s: %s" % (tilde(settings), exc)
            if argv[1] == "ensure"
            else ""
        )
    if text:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
