"""Deterministic TCS (task-builder SKILL.md 'Reflect Depth (Deterministic TCS)') over a task file.
Usage: uv run python -I tcs_compute.py <task.md> <spec.md> [<task2.md> ...]   (prints JSON per task file)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

spec = Path(sys.argv[2]).read_text()
PATHRE = re.compile(r"(?:[\w.-]+/)+[\w.-]+\.[\w]+")


def tcs(path):
    text = Path(path).read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    front = m.group(1) if m else ""
    body = text[m.end():] if m else text
    # drop fenced code blocks
    out, fence = [], False
    for ln in body.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(ln)
    # drop the ### Open Questions section (to the next heading of level <= 3)
    kept, skip = [], False
    for ln in out:
        if re.match(r"^###\s+Open Questions", ln):
            skip = True
            continue
        if skip and re.match(r"^#{1,3}\s", ln):
            skip = False
        if not skip:
            kept.append(ln)
    b = "\n".join(kept)
    files = set()
    for p in PATHRE.findall(b):
        p = re.sub(r":\d+$", "", p.lower())
        files.add(p)
    s1 = len(files)
    keys = set()
    for p in files:
        segs = p.split("/")
        dirs = segs[:-1]
        keys.add("/".join(dirs[:2]) if len(dirs) >= 2 else "/".join(segs))
    s2 = len(keys)
    s3 = len(set(re.findall(r"\b(?:N?FR)-\d+\b", spec)))
    s4 = len(re.findall(r"after Phase \d+|depends_on:", b, re.I))
    # S5: OQ tokens in a checklist item's Context line that also have an entry under ### Open Questions
    oq_sec = re.search(r"\n###\s+Open Questions\n(.*?)(?=\n#{2,3}\s|\Z)", body, re.S)
    oq_tokens = set(re.findall(r"OQ-\d+", oq_sec.group(1))) if oq_sec else set()
    ctx = [l for l in kept if l.lstrip().startswith("- **Context**:")]
    in_ctx = set()
    for l in ctx:
        in_ctx |= set(re.findall(r"OQ-\d+", l))
    s5 = len(in_ctx & oq_tokens)
    if oq_sec and s5 == 0 and not in_ctx:
        s5 = len([l for l in oq_sec.group(1).split("\n") if l.strip()])
    t = re.search(r"^type:\s*(.*)$", front, re.M)
    tv = re.sub(r"^[\"']|[\"']$", "", t.group(1).strip()) if t else ""
    tv = re.sub(r"^[^\w]+", "", tv)
    s6 = 1 if re.match(r"(refactor|remediation|code remediation)", tv, re.I) else 0
    total = 3 * s1 + 4 * s2 + 2 * s3 + 2 * s4 + 5 * s5 + 4 * s6
    depth = "deep" if (total >= 35 or s6) else "standard" if total >= 13 else "quick"
    if s5 > 0 and depth == "quick":
        depth = "standard"
    return {
        "file": str(path),
        "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "signals": {"S1": s1, "S2": s2, "S3": s3, "S4": s4, "S5": s5, "S6": s6},
        "type_field": tv,
        "tcs": total,
        "derived_depth": depth,
        "oq_tokens_in_open_questions": sorted(oq_tokens),
        "oq_tokens_in_context": sorted(in_ctx),
    }


for f in [sys.argv[1]] + sys.argv[3:]:
    print(json.dumps(tcs(f)))
