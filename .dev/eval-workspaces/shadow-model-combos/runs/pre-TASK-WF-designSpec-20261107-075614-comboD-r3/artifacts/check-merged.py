"""Check merged-findings.jsonl: JSON validity, limits, and every quote verbatim inside its cited line range.
usage: uv run python check-merged.py <out>   (repo root)   writes merged-findings.checked.jsonl with real paths"""
import json, pathlib, sys

out = pathlib.Path(sys.argv[1])
I = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/"
PATH = {"P": I + "TASK-WF-designSpec-20261107-075614.md", "S": I + "source.md"}
bad, rows = 0, []
for ln in (out / "artifacts" / "merged-findings.jsonl").read_text().splitlines():
    f = json.loads(ln)
    assert len(f["claim"]) <= 300, (f["id"], len(f["claim"]))
    assert 1 <= len(f["citations"]) <= 8
    for c in f["citations"]:
        c["path"] = PATH.get(c["path"], c["path"])
        lines = pathlib.Path(c["path"]).read_text().splitlines()
        rng = "\n".join(lines[c["line_start"] - 1:c["line_end"]])
        if "quote" in c:
            assert len(c["quote"]) <= 200
            if c["quote"] not in rng:
                bad += 1
                print("NOT FOUND", f["id"], c["path"][-12:], c["line_start"], c["line_end"], c["quote"][:70])
    rows.append(f)
(out / "artifacts" / "merged-findings.checked.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
print("findings", len(rows), "bad quotes", bad,
      "blocking", sum(r["blocking"] for r in rows), "major", sum(r["severity"] == "MAJOR" for r in rows))
