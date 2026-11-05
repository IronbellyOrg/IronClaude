"""Deterministic quantitative layer for Step 3 (regenerated on resume).

Usage: uv run python quant_score.py <source.md> <variant-1> <variant-2> <variant-3>
RC: distinct spec H2 sections a card references (source.md:N[-M] citations mapped to the
    H2 range holding line N..M, plus explicit "section(s) N" mentions) / number of H2 sections.
IC: 1 - intra-card contradictions / claims (contradictions are entered by hand below, from the
    debate; claim-vs-claim only).
SR: concrete / (concrete + vague); concrete = citations; vague = hits of the protocol's vague list.
DC: resolved internal finding-id references / total (1.0 when there are none).
SC: top-level YAML keys / max across variants.
"""
import re
import sys

VAGUE = ["appropriate", "as needed", "properly", "adequate", "should consider", "might",
         "various", "etc.", "best practices", "industry standard"]
CONTRADICTIONS = {1: 0, 2: 0, 3: 0}


def h2_starts(src_lines):
    return [i + 1 for i, line in enumerate(src_lines) if line.startswith("## ")]


def section_of(line_no, starts):
    idx = 0
    for k, s in enumerate(starts):
        if s <= line_no:
            idx = k + 1
    return idx


def main():
    src = open(sys.argv[1], encoding="utf-8").read().splitlines()
    starts = h2_starts(src)
    total_sections = len(starts)
    rows = {}
    for vi, path in enumerate(sys.argv[2:], start=1):
        text = open(path, encoding="utf-8").read()
        secs = set()
        cites = re.findall(r"source\.md:(\d+)(?:-(\d+))?", text)
        for a, b in cites:
            lo, hi = int(a), int(b or a)
            for n in range(lo, hi + 1):
                secs.add(section_of(n, starts))
        for m in re.finditer(r"[Ss]ections? ((?:\d+(?:-\d+)?)(?:\s*(?:,|and)\s*\d+(?:-\d+)?)*)", text):
            for part in re.split(r"\s*(?:,|and)\s*", m.group(1)):
                if "-" in part:
                    a, b = part.split("-")
                    secs.update(range(int(a), int(b) + 1))
                else:
                    secs.add(int(part))
        secs.discard(0)
        secs = {s for s in secs if 1 <= s <= total_sections}
        all_cites = re.findall(r"(?:source\.md|plan|[\w./-]+\.(?:md|py|json|yaml)|Makefile):\d+", text)
        vague = sum(len(re.findall(re.escape(v), text, flags=re.I)) for v in VAGUE)
        ids = set(re.findall(r"id: ([A-Z]-\d+)", text))
        refs = re.findall(r"(?:blocking|rests on|and) ([A-Z]-\d+)", text.split("self_audit", 1)[-1])
        resolved = sum(1 for r in refs if r in ids)
        keys = [line.split(":")[0] for line in text.splitlines() if re.match(r"^[a-z_0-9]+:", line)]
        claims = len(re.findall(r"claim:", text)) + 2  # findings + verdict + self_audit
        rows[vi] = dict(
            RC=len(secs) / total_sections, secs=sorted(secs),
            IC=1 - CONTRADICTIONS[vi] / claims, claims=claims,
            SR=len(all_cites) / (len(all_cites) + vague) if all_cites else 0.0,
            cites=len(all_cites), vague=vague,
            DC=(resolved / len(refs)) if refs else 1.0, refs=refs,
            keys=len(keys), keylist=keys)
    maxkeys = max(r["keys"] for r in rows.values())
    print(f"spec H2 sections: {total_sections} at lines {starts}")
    for vi, r in rows.items():
        r["SC"] = r["keys"] / maxkeys
        q = r["RC"] * 0.30 + r["IC"] * 0.25 + r["SR"] * 0.15 + r["DC"] * 0.15 + r["SC"] * 0.15
        print(f"V{vi}: RC={r['RC']:.3f} sections={r['secs']} | IC={r['IC']:.3f} (claims {r['claims']}) | "
              f"SR={r['SR']:.3f} (cites {r['cites']}, vague {r['vague']}) | DC={r['DC']:.3f} refs={r['refs']} | "
              f"SC={r['SC']:.3f} ({r['keys']}/{maxkeys} keys {r['keylist']}) | quant={q:.4f}")


if __name__ == "__main__":
    main()
