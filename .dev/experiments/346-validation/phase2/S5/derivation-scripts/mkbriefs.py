"""Materialise final-prompt-2/3/4.md exactly as the executor built them (sed + cat >> heredoc).
usage: mkbriefs.py <log> <base final-prompt.md> <outdir>
"""
import json
import re
import sys
from pathlib import Path

log, base, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
lines = log.read_text(encoding="utf-8").splitlines()
base_text = base.read_text(encoding="utf-8")
EXPECT = {2142: ("2", "state3.json", 6011), 2335: ("3", "state5.json", None), 2487: ("4", "state7.json", 8373)}
for n, (rnd, state, size) in EXPECT.items():
    rec = json.loads(lines[n - 1])
    cmd = [b for b in rec["message"]["content"] if b.get("type") == "tool_use"][0]["input"]["command"]
    m = re.search(r"sed -e 's\|/tmp/ironclaude-p0live/state1.json\|/tmp/ironclaude-p0live/(state\d+\.json)\|'", cmd)
    assert m and m.group(1) == state, (n, m)
    body = cmd.split("<<'EOF'\n", 1)[1].rsplit("\nEOF", 1)[0] + "\n"
    text = base_text.replace("/tmp/ironclaude-p0live/state1.json", f"/tmp/ironclaude-p0live/{state}") + body
    dst = outdir / f"R{rnd}-reviewer-brief-L{n}-final-prompt-{rnd}.md"
    dst.write_text(text, encoding="utf-8")
    print(dst.name, len(text.encode()), "expected", size)
