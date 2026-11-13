"""Assemble debate-transcript.md from the round files and tallies. Usage: uv run python debate/transcript.py"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "debate-transcript.md"
SPEC = {1: "opus:architect", 2: "opus:analyzer", 3: "haiku:backend", 4: "opus:devops", 5: "sonnet:performance"}


def demote(text, by=2):
    return re.sub(r"^(#+) ", lambda m: "#" * min(6, len(m.group(1)) + by) + " ", text, flags=re.M)


def tally(tag):
    rows = {}
    for line in (HERE / f"{tag}-tally.md").read_text().splitlines():
        m = re.match(r"^\| ([SCXA]-\d{3}) \| (L\d) \| ([V\d -]+) \| (V\d) \| (\d)/5 \| (\w+) \|", line)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(4), int(m.group(5)), m.group(6))
    return rows


def reasons(tag):
    t = (HERE / tag).read_text().split("## Per-point positions", 1)[1]
    return {m.group(1): m.group(3).strip() for m in re.finditer(r"^\| ([SCXA]-\d{3}) \| \**(V\d)\** \| (.*?) \|\s*$", t, re.M)}


t1, t2, t3 = tally("round1"), tally("round2"), tally("round3")
why = reasons("round3-V1.md")
parts = [
    "# Adversarial Debate Transcript\n",
    "## Metadata\n- Depth: deep\n- Rounds completed: 3 (plus Round 2.5 invariant probe)\n"
    f"- Convergence achieved: {100 * sum(r[3] == 'agreed' for r in t3.values()) / len(t3):.0f}% ({sum(r[3] == 'agreed' for r in t3.values())}/{len(t3)} diff points)\n"
    "- Convergence threshold: 75%\n- Focus areas: All\n- Advocate count: 5 (V1 opus:architect, V2 opus:analyzer, V3 haiku:backend, V4 opus:devops, V5 sonnet:performance)\n"
    "- Run note: the first session was stopped by a timeout during Round 3 after round3-V1 and round3-V2; a resumed session wrote round3-V3, -V4 and -V5 sequentially (each saw all earlier Round 3 statements), the Round 3 tally and every later artifact. No completed file was rewritten.\n"
    "- Source files: `debate/round{1,2,3}-V{1..5}.md`, `debate/round{1,2,3}-tally.md`, `debate/round{2,3}-agenda.md`, `invariant-probe.md`; tallies computed by `debate/convergence.py`.\n",
    "## Round 1: Advocate Statements\n",
]
for i in range(1, 6):
    parts.append(f"### Variant {i} Advocate ({SPEC[i]})\n\n" + demote((HERE / f"round1-V{i}.md").read_text()))
parts.append("### Round 1 tally\n\n" + demote((HERE / "round1-tally.md").read_text()))
parts.append("## Round 2: Rebuttals\n\n### Round 2 agenda (orchestrator)\n\n" + demote((HERE / "round2-agenda.md").read_text()))
for i in range(1, 6):
    parts.append(f"### Variant {i} Rebuttal ({SPEC[i]})\n\n" + demote((HERE / f"round2-V{i}.md").read_text()))
parts.append("### Round 2 tally\n\n" + demote((HERE / "round2-tally.md").read_text()))
parts.append("## Round 2.5: Invariant Probe\n\nFull table and required resolutions: `invariant-probe.md`. Result: 33 findings; 8 HIGH UNADDRESSED (INV-001..INV-008) blocked convergence after Round 2 (diff-point agreement 43/43). 13 MEDIUM and 2 LOW UNADDRESSED items were warnings.\n")
parts.append("## Round 3: Final Arguments\n\n### Round 3 agenda (orchestrator)\n\n" + demote((HERE / "round3-agenda.md").read_text()))
for i in range(1, 6):
    parts.append(f"### Variant {i} Final Position ({SPEC[i]})\n\n" + demote((HERE / f"round3-V{i}.md").read_text()))
parts.append("### Round 3 tally and HIGH-invariant closure\n\n" + demote((HERE / "round3-tally.md").read_text()))
rows = ["## Scoring Matrix\n",
        "Confidence rule: 5/5 in Round 3 and agreed (>= 4/5) in every earlier round -> 95%; 5/5 in Round 3 after a Round 1 split -> 90%; 4/5 at the end -> 80%. No point is 100% (not every losing advocate explicitly conceded each point).\n",
        "| Diff Point | Level | Winner | Confidence | R1 / R2 / R3 support | Evidence Summary (R3-V1 reason) |", "|---|---|---|---|---|---|"]
for p, (lvl, win, k, st) in t3.items():
    conf = 80 if k < 5 else (95 if t1[p][3] == "agreed" and t2[p][3] == "agreed" else 90)
    rows.append(f"| {p} | {lvl} | {win} (variant-{win[1]}) | {conf}% | {t1[p][2]}/5 {t1[p][1]} / {t2[p][2]}/5 {t2[p][1]} / {k}/5 | {why.get(p, '')} |")
parts.append("\n".join(rows) + "\n")
won = {}
for p, r in t3.items():
    won[r[1]] = won.get(r[1], 0) + 1
parts.append("Points won: " + ", ".join(f"{v} {won.get(v, 0)}" for v in ["V1", "V2", "V3", "V4", "V5"]) + ".\n")
parts.append("## Convergence Assessment\n- Points resolved: {0} of {1}\n- Alignment: {2:.0f}%\n- Threshold: 75%\n- Taxonomy coverage: L1 3, L2 31, L3 9 (all levels covered)\n- Invariant gate: 8 HIGH items closed in Round 3 (INV-001, -003 MODIFY = R3-V1 5/5; INV-005 MODIFY = R3-V2 4/5; INV-002, -004, -006, -007, -008 ACCEPT 5/5); 0 HIGH unaddressed\n- Status: CONVERGED\n- Unresolved points: none\n- Round history: Round 1 37/43 (0.860); Round 2 43/43 (1.000) but BLOCKED_BY_INVARIANTS; Round 3 43/43 (1.000), CONVERGED\n- Base proposed by every advocate in every round: V4\n".format(sum(r[3] == 'agreed' for r in t3.values()), len(t3), 100 * sum(r[3] == 'agreed' for r in t3.values()) / len(t3)))
OUT.write_text("\n".join(parts))
print(OUT, len(OUT.read_text()))
