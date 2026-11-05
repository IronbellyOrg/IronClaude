"""Compare saved /sc:implement reviewer prompts with the reviewer template.

Usage (from the repository root):
    PYTHONDONTWRITEBYTECODE=1 uv run python -I <this file> <prompt path> [<prompt path> ...]

Prints one line per prompt: "<path> <class>", where class is
    match            the prompt equals the template outside the slots, byte for byte
    blank-line-only  it equals the template after dropping blank lines and trailing
                     whitespace, but not byte for byte
    differs          anything else (also: line 1 is not the start sha, a slot label is
                     missing or out of order, or the closing line is missing)

Rules follow refs/qa.md "## FINAL derived test" (saved prompts): line 1 of a saved
prompt is the task's start sha and is dropped after it is checked against the
"Start sha:" slot; the slots are cut out; the rest is compared with the template.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

QA = Path("src/superclaude/skills/sc-implement-protocol/refs/qa.md")
HEADING = "## Subagent prompt (when not inline)"
FIRST_LINE = "Review one task for spec compliance."
CLOSING = "Do not trust the implementer's report."
LABELS = (
    "Task brief:",
    "Global constraints:",
    "Start sha:",
    "Diff against the start snapshot:",
    "Delta diff from the previous reviewed tree (empty on the first review):",
    "Earlier blocking findings of this start (empty on the first review):",
    "Saved-probe re-check hit locations (may be empty):",
)
SHA_RE = re.compile(r"^(?:[0-9a-f]{40}|nogit)$")


def template_lines() -> list[str]:
    lines = QA.read_text(encoding="utf-8").splitlines()
    h = lines.index(HEADING)
    fences = [i for i in range(h + 1, len(lines)) if lines[i].startswith("```")]
    block = lines[fences[0] + 1 : fences[1]]
    if not block or block[0] != FIRST_LINE:
        raise SystemExit(f"template block does not begin with {FIRST_LINE!r}")
    return block


def cut_slots(lines: list[str]) -> tuple[list[str], str] | None:
    """Return (lines with slot contents removed, value of the 'Start sha:' slot)."""
    positions: list[int] = []
    at = 0
    for label in LABELS:
        found = next((i for i in range(at, len(lines)) if lines[i].startswith(label)), None)
        if found is None:
            return None
        positions.append(found)
        at = found + 1
    closing = next((i for i in range(positions[-1] + 1, len(lines)) if lines[i] == CLOSING), None)
    if closing is None:
        return None
    out = list(lines[: positions[0]])
    sha_value = ""
    for n, label in enumerate(LABELS):
        limit = positions[n + 1] if n + 1 < len(LABELS) else closing
        end = max(i for i in range(positions[n], limit) if lines[i].strip())
        if label == "Start sha:":
            sha_value = lines[positions[n]][len(label) :].strip()
        out.append(label)
        out.extend(lines[end + 1 : limit])
    out.extend(lines[closing:])
    return out, sha_value


def classify(prompt: Path, template: list[str]) -> str:
    text = prompt.read_text(encoding="utf-8").removesuffix("\n")
    lines = text.split("\n")
    first, rest = lines[0], lines[1:]
    cut = cut_slots(rest)
    if cut is None or not SHA_RE.match(first):
        return "differs"
    remainder, sha_value = cut
    if first != sha_value:
        return "differs"
    expected = cut_slots(template)
    if expected is None:
        raise SystemExit("template has no complete slot layout")
    want = expected[0]
    if remainder == want:
        return "match"
    squeeze = lambda ls: [x.rstrip() for x in ls if x.strip()]  # noqa: E731
    return "blank-line-only" if squeeze(remainder) == squeeze(want) else "differs"


def main(paths: list[str]) -> int:
    template = template_lines()
    for p in paths:
        print(f"{p} {classify(Path(p), template)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
