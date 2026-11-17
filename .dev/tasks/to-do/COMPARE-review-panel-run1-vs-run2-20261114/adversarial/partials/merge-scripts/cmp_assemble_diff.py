import re, sys, datetime, json
from pathlib import Path

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
PART = ROOT / "partials"
parts = ["A", "B", "C", "D"]
secmap = {"Structural": "S", "Content": "C", "Contradictions": "X", "Unique": "U", "Shared Assumptions": "A"}
idre = re.compile(r"\b([SCXUA])-([ABCD])-(\d{3})\b")

rows = {k: [] for k in "SCXUA"}  # list of (old_id, cells)
notes = []  # (partial, section, lines)
verif = {}  # old id -> cells (C partial 3-col verification table)
seen_x = set()

def cells_of(line):
    s = line.strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") else s
    # split on pipes outside backtick spans and not escaped
    out, cur, incode, i = [], [], False, 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("\\|")
            i += 2
            continue
        if ch == "`":
            incode = not incode
        if ch == "|" and not incode:
            out.append("".join(cur))
            cur = []
        else:
            cur.append("|" if False else ch)
        i += 1
    out.append("".join(cur))
    return [c.strip().replace("|", "\\|") if "\\|" not in c else c.strip() for c in out]

for p in parts:
    text = (PART / f"diff-partial-{p}.md").read_text().splitlines()
    sec = "preamble"
    buf = []
    def flush():
        global buf
        if buf and any(l.strip() for l in buf):
            notes.append((p, sec, buf))
        buf = []
    for line in text:
        if line.startswith("## "):
            flush()
            title = line[3:].strip()
            sec = "other:" + title
            for k, v in secmap.items():
                if title.startswith(k):
                    sec = v
            buf = []
            if sec.startswith("other:"):
                buf.append(line)
            continue
        if line.startswith("# ") and sec == "preamble":
            buf.append(line)
            continue
        m = re.match(r"^\|\s*([SCXUA])-([ABCD])-(\d{3})\b", line)
        if m and sec in "SCXUA" and len(sec) == 1:
            cs = cells_of(line)
            oid = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            if sec == "X" and (len(cs) == 3 or oid in seen_x):
                verif[oid] = [cs[0], cs[1], " | ".join(cs[2:])]
            else:
                rows[sec].append((oid, cs, p))
                if sec == "X":
                    seen_x.add(oid)
            continue
        if re.match(r"^\|\s*#\s*\|", line) and sec in "SCXUA" and len(sec) == 1:
            continue  # header
        if re.match(r"^\|[\s:|-]+\|\s*$", line):
            continue  # separator
        buf.append(line)
    flush()

# renumber
newid = {}
for k in "SCXUA":
    for i, (oid, cs, p) in enumerate(rows[k], start=1):
        newid[oid] = f"{k}-{i:03d}"

def remap(s):
    return idre.sub(lambda m: newid.get(m.group(0), m.group(0)), s)

def sev(cell):
    m = re.match(r"\W*(High|Medium|Low)", cell, re.I)
    return m.group(1).capitalize() if m else "Unrated"

out = []
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
counts = {k: len(rows[k]) for k in "SCXUA"}
total = sum(counts.values())

# classification of shared assumptions
def acls(cs):
    c = cs[3] if len(cs) > 3 else ""
    cu = c.upper()
    if "CONTRADICTED" in cu:
        return "CONTRADICTED"
    if "UNSTATED" in cu:
        return "UNSTATED"
    return "STATED"
acount = {"STATED": 0, "UNSTATED": 0, "CONTRADICTED": 0}
for oid, cs, p in rows["A"]:
    acount[acls(cs)] += 1

out.append("# Diff Analysis: Research Report Comparison (review-panel unification, run 1 vs run 2)\n")
out.append("## Metadata")
out.append(f"- Generated: {now}")
out.append("- Variants compared: 2 (Variant 1 = run 1 report, 4,476 lines; Variant 2 = run 2 report, 5,098 lines)")
out.append(f"- Total differences found: {total}")
out.append(f"- Categories: structural ({counts['S']}), content ({counts['C']}), contradictions ({counts['X']}), unique ({counts['U']}), shared assumptions ({counts['A']})")
out.append("- Assembly: four analysts (A: ToC + Sec 1, 3, 4; B: Sec 2, 5; C: Sec 6; D: Sec 7-10 + appendices) wrote partials under `adversarial/partials/diff-partial-{A,B,C,D}.md` using ids with a partition letter (for example S-A-001). This file renumbers them contiguously; each row carries its source id in `[src ...]`, so a row can be traced back. Cross-references inside rows were remapped to the new ids.")
out.append("- Naming: V1 = Variant 1 = run 1 (`RESEARCH-REPORT-review-panel-unification.md`); V2 = Variant 2 = run 2 (`RESEARCH-REPORT-review-panel-unification-run2.md`). Cross-report ids such as `C-05` mean different conflicts in the two reports; they are always written with V1 or V2 in front.")
out.append("- Line numbers cite the original input reports; the copies `variant-1-original.md` and `variant-2-original.md` are byte-identical to them.")
out.append("- Coverage limits: see the Analyst Notes appendix (the Coverage note of each partial states which line ranges were read in full and which were sampled).")
out.append("")

def table(title, header, key, last_idx_fn=None):
    out.append(f"## {title}\n")
    out.append(header)
    out.append("|" + "---|" * (header.count("|") - 1))
    for oid, cs, p in rows[key]:
        cs2 = [remap(c) for c in cs]
        cs2[0] = f"{newid[oid]} [src {oid}]"
        out.append("| " + " | ".join(cs2) + " |")
    out.append("")

table("Structural Differences", "| # | Area | Variant 1 (run 1) | Variant 2 (run 2) | Severity |", "S")
table("Content Differences", "| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |", "C")
table("Contradictions", "| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |", "X")

# verification table for X rows
vrows = []
for oid, cs in verif.items():
    vrows.append((newid.get(oid, oid), oid, cs))
if vrows:
    out.append("### Contradiction verification evidence (from analyst C; other partials carry the evidence inside the rows)\n")
    out.append("| # | Verdict | Command or file used and result |")
    out.append("|---|---|---|")
    for nid, oid, cs in sorted(vrows):
        out.append("| " + " | ".join([f"{nid} [src {oid}]"] + [remap(c) for c in cs[1:]]) + " |")
    out.append("")

table("Unique Contributions", "| # | Variant | Contribution | Value Assessment |", "U")

out.append("## Shared Assumptions\n")
out.append("Classification per skill: STATED / UNSTATED / CONTRADICTED. UNSTATED and CONTRADICTED rows are promoted to `[SHARED-ASSUMPTION]` diff points (advocates must answer ACCEPT / REJECT / QUALIFY); STATED rows are documented only.\n")
out.append("| # | Assumption | Source Agreement | Classification | Impact | Promoted |")
out.append("|---|---|---|---|---|---|")
promoted = []
for oid, cs, p in rows["A"]:
    cs2 = [remap(c) for c in cs]
    cs2[0] = f"{newid[oid]} [src {oid}]"
    pr = "Yes" if acls(cs) in ("UNSTATED", "CONTRADICTED") or "unstated part" in cs[3].lower() else "No"
    if pr == "Yes":
        promoted.append(newid[oid])
    while len(cs2) < 5:
        cs2.append("")
    out.append("| " + " | ".join(cs2[:5] + [pr]) + " |")
out.append("")

# summary
def highs(k):
    return [newid[oid] for oid, cs, p in rows[k] if sev(cs[-1]) == "High"]
out.append("## Summary")
out.append(f"- Total structural differences: {counts['S']}")
out.append(f"- Total content differences: {counts['C']}")
out.append(f"- Total contradictions: {counts['X']}")
out.append(f"- Total unique contributions: {counts['U']} (Variant 1: {sum(1 for o,c,p in rows['U'] if re.search(r'V1|Variant 1|run 1', c[1]) and not re.search(r'V2|Variant 2|run 2', c[1]))}, Variant 2: {sum(1 for o,c,p in rows['U'] if re.search(r'V2|Variant 2|run 2', c[1]) and not re.search(r'V1|Variant 1|run 1', c[1]))})")
out.append(f"- Total shared assumptions surfaced: {counts['A']} (UNSTATED: {acount['UNSTATED']}, STATED: {acount['STATED']}, CONTRADICTED: {acount['CONTRADICTED']}; promoted to debate points: {len(promoted)})")
out.append(f"- Debate-point denominator per the skill (S + C + X + promoted A): {counts['S']+counts['C']+counts['X']+len(promoted)} (S {counts['S']} + C {counts['C']} + X {counts['X']} + promoted A {len(promoted)}; the {counts['A']-len(promoted)} STATED assumptions are documented, not debated)")
for k, name in (("S", "structural"), ("C", "content"), ("X", "contradictions"), ("U", "unique"), ("A", "shared assumptions")):
    h = highs(k)
    out.append(f"- High-severity {name} ({len(h)}): {', '.join(h) if h else 'none'}")
out.append(f"- Promoted shared assumptions: {', '.join(promoted) if promoted else 'none'}")
out.append("")

out.append((PART / "orchestrator-verification.md").read_text().strip("\n"))
out.append("")

# notes appendix
out.append("## Appendix: Analyst Notes, Extra Tables and Coverage (verbatim from the partials, ids remapped)\n")
for p, sec, lines in notes:
    label = {"preamble": "Preamble", "S": "after Structural", "C": "after Content", "X": "after Contradictions", "U": "after Unique", "A": "after Shared Assumptions"}.get(sec, sec.replace("other:", "Section: "))
    out.append(f"### Partial {p} - {label}\n")
    body = "\n".join(remap(l) for l in lines).strip("\n")
    # demote headings inside body to keep structure
    body = re.sub(r"(?m)^#{1,3} ", "#### ", body)
    out.append(body)
    out.append("")

(ROOT / "diff-analysis.md").write_text("\n".join(out) + "\n")
(ROOT / "partials" / "id-map.json").write_text(json.dumps(newid, indent=1))
print(json.dumps({"counts": counts, "total": total, "acount": acount, "promoted": len(promoted), "verif": len(verif)}))
