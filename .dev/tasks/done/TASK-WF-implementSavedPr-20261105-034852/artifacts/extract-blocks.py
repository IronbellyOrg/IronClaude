"""Print the fenced blocks that must not change when the saved-prompt rules are edited.

Usage: uv run python -I extract-blocks.py <qa|ledger> <path>

qa     the reviewer template block: the fenced block whose first line is
       "Review one task for spec compliance."
ledger every fenced block that follows a ledger-grammar-block marker comment
       (the marker line is printed too)
"""
import sys

FENCE = "```"


def fenced_after(lines, start):
    """Return (block_lines, next_index) for the fence that opens at lines[start]."""
    assert lines[start].startswith(FENCE), lines[start]
    end = start + 1
    while end < len(lines) and not lines[end].startswith(FENCE):
        end += 1
    return lines[start : end + 1], end + 1


def main(mode, path):
    lines = open(path, encoding="utf-8").read().split("\n")
    out = []
    if mode == "qa":
        for i, line in enumerate(lines):
            if line.startswith(FENCE) and i + 1 < len(lines) and lines[i + 1] == "Review one task for spec compliance.":
                block, _ = fenced_after(lines, i)
                out.extend(block)
                break
        else:
            sys.exit("template block not found")
    elif mode == "ledger":
        i = 0
        while i < len(lines):
            if lines[i].startswith("<!-- ledger-grammar-block:"):
                out.append(lines[i])
                j = i + 1
                while j < len(lines) and not lines[j].startswith(FENCE):
                    j += 1
                block, i = fenced_after(lines, j)
                out.extend(block)
            else:
                i += 1
        if not out:
            sys.exit("no ledger-grammar-block found")
    else:
        sys.exit("mode must be qa or ledger")
    print("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
