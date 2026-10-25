# Reads both guides, extracts backticked repo paths and markdown link targets, reports whether each exists.
import re, os
guides = ["docs/user-guide/memory-system.md", "docs/memory/README.md"]
for g in guides:
    text = open(g).read()
    base = os.path.dirname(g)
    items = set()
    for t in re.findall(r"`([^`\s]+)`", text):
        if "/" in t and re.search(r"\.(py|md|jsonl|example)$", t) and "<" not in t and "*" not in t:
            items.add(("path", t, t))
    for t in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
        if not t.startswith("http"):
            items.add(("link", t, os.path.normpath(os.path.join(base, t))))
    for kind, raw, resolved in sorted(items):
        print(f"{g}: {kind} {raw} -> {'OK' if os.path.exists(resolved) else 'MISSING'}")
