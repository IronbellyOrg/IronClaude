"""Fence-state checker for one Markdown file (Task 8 evidence; not a delivery file).

A fence opens on a line of 3 or more backticks or tildes (optionally followed by an
info string) and closes only on a bare fence line of the same character that is at
least as long as the opening run. While a fence is open, a line that looks like a new
opening fence with an info string (for example ```bash inside a ```markdown block) is
recorded as a nested opening; when a bare fence then closes the outer fence, that spot
is reported as an inner fence closing the outer one.

Usage: uv run python -I t8-fence-check.py <file.md>
Prints every heading line with its fence state, then every inner-closes-outer spot.
"""
import re
import sys

OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def scan(lines):
    headings = []
    spots = []
    fence = None  # (char, length, open_line, info)
    nested = None  # line number of the latest nested opening-shaped line
    for n, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        m = OPEN_RE.match(line)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)), n, m.group(2).strip())
                nested = None
            elif re.match(r"^#{1,6} ", line):
                headings.append((n, line, "outside"))
            continue
        char, length, open_line, info = fence
        if m and m.group(1)[0] == char:
            run = len(m.group(1))
            rest = m.group(2).strip()
            if rest == "" and run >= length:
                if nested is not None:
                    spots.append((open_line, info, nested, n))
                fence = None
                nested = None
                continue
            if rest != "" and run >= length:
                # A shorter run is a valid nested fence; only a run at least as long
                # as the outer one marks a nested block whose bare close ends the outer.
                nested = n
                continue
        if re.match(r"^#{1,6} ", line):
            headings.append((n, line, f"inside fence opened at line {open_line} ({'`' * length if char == '`' else '~' * length}{info})"))
    if fence is not None:
        spots.append((fence[2], fence[3], None, None))
    return headings, spots


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    headings, spots = scan(lines)
    print(f"# Fence state of {path}")
    print("## Headings")
    for n, text, state in headings:
        print(f"L{n}: {text}  [{state}]")
    print("## Inner fence closes outer fence")
    if not spots:
        print("none")
    for open_line, info, nested, close in spots:
        if close is None:
            print(f"outer fence opened at L{open_line} ({info}) is never closed")
        else:
            print(f"outer fence opened at L{open_line} ({info}); nested opening at L{nested}; bare fence at L{close} closes the OUTER fence")


if __name__ == "__main__":
    main()
