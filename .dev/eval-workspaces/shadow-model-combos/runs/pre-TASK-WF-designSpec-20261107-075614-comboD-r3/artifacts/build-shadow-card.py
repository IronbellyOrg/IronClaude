"""Step 5: write panel/cards/reviewer-<N>.md = header + findings block (verbatim) + calibration per_finding map.
usage: uv run python build-shadow-card.py <out> <N> <calibration.json> [fenced|bare]"""
import json, re, sys, pathlib

out, n, calib = pathlib.Path(sys.argv[1]), sys.argv[2], json.loads(pathlib.Path(sys.argv[3]).read_text())
mode = sys.argv[4] if len(sys.argv) > 4 else "bare"
src = (out / "reviewer-cards" / f"reviewer-{n}-card.md").read_text()
header = "\n".join(src.split("\n## Findings block", 1)[0].strip().splitlines())
block = re.search(r"## Findings block\n+```findings-v2\n.*?\n```", src, re.S).group(0)
per = "\n".join(f"    {k}: {v}" for k, v in calib["per_finding"].items())
cal = f"calibration:\n  per_finding:\n{per}" if mode == "bare" else f"```yaml\ncalibration:\n  per_finding:\n{per}\n```"
(out / "panel" / "cards" / f"reviewer-{n}.md").write_text(f"{header}\n\n{block}\n\n{cal}\n")
print(f"wrote reviewer-{n}.md ({mode})")
