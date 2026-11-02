"""Mark sweep hits already covered by a plan site list (inventory.md rows or cap-edits.yaml rows).

Usage (repo root): uv run python -I .dev/review-severity-rule/sweep/classify_covered.py
Writes .dev/review-severity-rule/sweep/hits-premapped.tsv: id, file, line, source-of-coverage-or-"-", text.
"""
import pathlib
import re
import yaml

ROOT = pathlib.Path(".dev/review-severity-rule")
cover: dict[tuple[str, int], str] = {}


def add(file: str, line: int, tag: str) -> None:
    cover.setdefault((file, line), tag)


for row in yaml.safe_load((ROOT / "cap-edits.yaml").read_text())["rows"]:
    lines = row.get("lines") or [row.get("line")]
    for ln in lines:
        if isinstance(ln, int):
            add(row["file"], ln, f"cap-edits {row['id']}")
        elif isinstance(ln, str):
            for part in re.findall(r"\d+(?:-\d+)?", ln):
                a, _, b = part.partition("-")
                for n in range(int(a), int(b or a) + 1):
                    add(row["file"], n, f"cap-edits {row['id']}")

cell = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|yaml|contract|txt)):([0-9][0-9 ,\-–]*)")
for i, text in enumerate((ROOT / "inventory.md").read_text().splitlines(), 1):
    if not text.startswith("|"):
        continue
    first = text.split("|")[1]
    for path, nums in cell.findall(first):
        file = path if path.startswith(("src/", "plugins/", "tests/")) else f"src/superclaude/{path}"
        for part in re.findall(r"\d+(?:\s*[-–]\s*\d+)?", nums):
            a, _, b = re.split(r"\s*([-–])\s*", part) + [""] * 0 if False else (part.replace("–", "-").replace(" ", "").partition("-"))
            for n in range(int(a), int(b or a) + 1):
                add(file, n, f"inventory.md:{i}")

(ROOT / "sweep/coverage.tsv").write_text("".join(f"{f}:{n}\t{t}\n" for (f, n), t in sorted(cover.items())))
out = []
for raw in (ROOT / "sweep/hits.tsv").read_text().splitlines():
    pid, rest = raw.split("\t", 1)
    file, line, text = rest.split(":", 2)
    out.append("\t".join([pid, file, line, cover.get((file, int(line)), "-"), text.strip()[:220]]))
(ROOT / "sweep/hits-premapped.tsv").write_text("\n".join(out) + "\n")
covered = sum(1 for o in out if o.split("\t")[3] != "-")
print(f"{len(out)} hits; {covered} covered by a site list; {len(out) - covered} need a disposition")
