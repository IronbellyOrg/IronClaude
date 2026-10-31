import pathlib, re, sys
bad = []
for root in ("src/superclaude", "plugins/superclaude", "commands", "agents"):
    for p in sorted(pathlib.Path(root).rglob("*.md")):
        t = p.read_text(errors="ignore")
        m = re.match(r"---\n(.*?)\n---\n", t, re.S)
        line = m and re.search(r"^(?:tools|allowed-tools):\s*(.*)$", m.group(1), re.M)
        if not line:
            continue
        roster = set(re.findall(r"mcp__[\w-]+__[\w-]+", line.group(1)))
        named = set(re.findall(r"mcp__[\w-]+__[\w-]+", t[m.end():]))
        bad += [f"{p}: {n}" for n in sorted(named - roster)]
print("\n".join(bad))
sys.exit(1 if bad else 0)
