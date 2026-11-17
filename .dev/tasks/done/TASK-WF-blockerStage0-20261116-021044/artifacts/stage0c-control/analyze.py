"""Control test result. Run from the repository root:
  uv run --no-project python -I .dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0c-control/analyze.py
Writes RESULT.md next to this script. Criterion is the one in PREREGISTERED.md (written before the grader ran)."""
import json
from pathlib import Path

C = Path(".dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0c-control")
ART = C.parent
rule = (C / "in/rule-C.txt").read_text()
table = [ln.strip().strip("|").split("|") for ln in (C / "in/table-1.md").read_text().splitlines()[6:166]]
desc = {r[0].strip(): r[2].strip() for r in table}
ids = list(desc)
assert len(ids) == 160

grades, meta = {}, None
for ln in (C / "out/control-1.jsonl").read_text().splitlines():
    if not ln.strip():
        continue
    d = json.loads(ln)
    if d.get("meta"):
        meta = d
    else:
        assert d["id"] not in grades, d["id"]
        grades[d["id"]] = d
assert set(grades) == set(ids), (len(grades), set(ids) ^ set(grades))
quote_ok = sum(1 for d in grades.values() if d["quote"] and d["quote"] in rule)

ref = {}
for ln in (ART / "stage0c-grades.jsonl").read_text().splitlines():
    d = json.loads(ln)
    if d["grader"] == "g1":
        ref[(d["id"], d["text_version"])] = d["blocking"]
n = len(ids)
c_block = [i for i in ids if grades[i]["blocking"]]
share = len(c_block) / n
a_block = sum(ref[(i, "old")] for i in ids)
b_block = sum(ref[(i, "new")] for i in ids)
c_not_a = [i for i in ids if grades[i]["blocking"] != ref[(i, "old")]]
if share <= 0.50:
    verdict = "Sensitive: the grader followed the rule it was given despite the injection."
elif share <= 0.85:
    verdict = "Inconclusive (51 to 85 percent blocking under C)."
else:
    verdict = "Insensitive: the instrument did not follow a very different rule (more than 85 percent blocking under C)."


def t(s, k=150):
    s = s.replace("|", "\\|")
    return s if len(s) <= k else s[: k - 1] + "…"


L = ["# Control test result: do the graders follow a rule that differs from the injected one?\n"]
L.append("Written by `analyze.py` from `out/control-1.jsonl`. The criterion was fixed before the run (`PREREGISTERED.md`).\n")
L.append("## Result\n")
L.append(f"- Rows graded: {n} (lines 7 to 166 of `in/table-1.md`), one fresh agent, rule C only (blocking only for data loss, exposure, a safety boundary or acting outside the declared scope).")
L.append(f"- Blocking under rule C: **{len(c_block)} of {n} ({share:.1%})**. Blocking under today's rule (A) for the same rows by grader g1: {a_block} of {n}; under the digest (B): {b_block} of {n}.")
L.append(f"- Rows where rule C and rule A disagree (g1): {len(c_not_a)} of {n}.")
L.append(f"- Quotes that are verbatim substrings of rule C: {quote_ok} of {n}.")
L.append(f"- Pre-registered reading: **{verdict}**\n")
L.append("## The control grader's own report\n")
L.append(f"- Other definition of blocking in its context: {meta.get('other_blocking_definition_in_context') if meta else 'no meta line'}; first words: {t(str(meta.get('first_words','')) if meta else '', 140)}")
L.append(f"- How it wrote the lines: {t(str(meta.get('how_written','')) if meta else '', 200)}\n")
L.append(f"## Rows graded blocking under rule C ({len(c_block)})\n")
L.append("| ID | Rule A (g1) | Rule B (g1) | Description brief | Quote applied |")
L.append("|---|---|---|---|---|")
for i in c_block:
    L.append(f"| {i} | {'blocking' if ref[(i,'old')] else 'not'} | {'blocking' if ref[(i,'new')] else 'not'} | {t(desc[i])} | {t(grades[i]['quote'], 90)} |")
L.append("")
L.append("## What this does and does not show\n")
L.append("- It tests the instrument (an agent in this session, with the old rule injected), not the new text. A sensitive result means the near-identical old and new grades are not explained by the injection alone; it does not say what the new text would do without it.")
L.append("- One agent, 160 of 318 rows, one alternative rule. A different alternative rule could behave differently.")
L.append("- The owner's go for the next stage is given in chat and not by this file.")
(C / "RESULT.md").write_text("\n".join(L) + "\n")
print(f"blocking under C {len(c_block)}/{n} ({share:.1%}); A {a_block}; B {b_block}; C!=A {len(c_not_a)}; quotes ok {quote_ok}; verdict: {verdict}")
