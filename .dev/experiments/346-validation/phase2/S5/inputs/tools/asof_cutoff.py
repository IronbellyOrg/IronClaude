"""Cut the original executor session tree back to what existed when a final review was spawned.

usage: uv run --no-project python -I asof_cutoff.py <executor-session-dir> <cutoff-ISO-UTC> <outdir>
  <executor-session-dir>  the unpacked `executor-session` folder (aaee1ebf-....jsonl plus aaee1ebf-..../subagents/)
  cutoff                  R1 2026-11-04T09:09:08.436Z, R2 2026-11-04T12:11:17.000Z,
                          R3 2026-11-04T12:29:53.000Z, R4 2026-11-04T12:56:21.000Z
Keeps every line up to the last one before the first timestamp later than the cutoff; subagent logs that
start after the cutoff are dropped. Why: reviewers 2 to 4 audited the executor session tree, which itself
contains the earlier reviewers' tool calls, so the replay must show each reviewer the same tree.
"""
import json
import sys
from pathlib import Path

src, cutoff, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])


def cut(lines):
    keep = []
    for ln in lines:
        ts = json.loads(ln).get("timestamp")
        if ts and ts > cutoff:
            break
        keep.append(ln)
    return keep


out.mkdir(parents=True, exist_ok=True)
for f in sorted(src.rglob("*.jsonl")):
    rel = f.relative_to(src)
    kept = cut(f.read_text(encoding="utf-8").splitlines(keepends=True))
    if not any(json.loads(x).get("timestamp") for x in kept):
        continue  # started after the cutoff
    dst = out / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("".join(kept), encoding="utf-8")
    meta = f.with_name(f.name.replace(".jsonl", ".meta.json"))
    if meta.exists():
        (dst.parent / meta.name).write_bytes(meta.read_bytes())
    print(f"{rel}: kept {len(kept)} lines")
# not copied: tool-results/ (large saved tool outputs) and custom-title.json
