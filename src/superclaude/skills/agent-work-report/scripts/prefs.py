#!/usr/bin/env python3
"""Record what the person tells the helper, so no file is ever edited by hand (FR-17, FR-20).

usage (the person's own words are always read from standard input, never from the command line):
  prefs.py priority <run_folder> <item_url> <Urgent|High|Medium|Low|clear>   < why
  prefs.py answer <run_folder> <item_url|-> <session|clickup-dm>            < answer text

`priority` writes .dev/coordinator/priorities.json and logs the change; it applies from the next sort.
`answer` logs a recorded answer from the person, with where it came from.
"""

import re
import sys

from common import read_json, state_dir, write_json
from run import log_action

LEVELS = {"Urgent", "High", "Medium", "Low", "clear"}
SOURCES = {"session", "clickup-dm"}
URL = re.compile(r"^https://(github\.com|app\.clickup\.com)/\S+$")


def words():
    text = sys.stdin.read().strip()
    if not text:
        sys.exit("give the person's words on standard input")
    return text


def check_url(url, allow_none=False):
    if not (URL.match(url) or (allow_none and url == "-")):
        sys.exit(f"not an item URL: {url!r}")


def set_priority(run, url, level):
    check_url(url)
    if level not in LEVELS:
        sys.exit(f"level must be one of {sorted(LEVELS)}")
    why = words()
    path = state_dir() / "priorities.json"
    prefs = read_json(path, {})
    if level == "clear":
        prefs.pop(url, None)
    else:
        prefs[url] = {"level": level, "why": why}
    write_json(path, prefs)
    log_action(run, "priority-change", url, f"{level}: {why}")


def record_answer(run, url, source):
    check_url(url, allow_none=True)
    if source not in SOURCES:
        sys.exit(f"source must be one of {sorted(SOURCES)}")
    log_action(run, "answer", url, f"from {source}: {words()}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["priority"] and len(a) == 4:
        set_priority(*a[1:])
    elif a[:1] == ["answer"] and len(a) == 4:
        record_answer(*a[1:])
    else:
        sys.exit(__doc__)
