"""Append the question and body-comparison record of a contradiction run to runs/<name>/record.md.

Usage: contradiction_report.py <run name>
Records, from raw files only: the question text and its options (screen-question-N.txt), the answer from the transcript's
tool result, the number of AskUserQuestion calls, the draft body at question time against the posted body (unified diff),
and whether each false file name still appears in the posted body.
"""

import difflib
import json
import re
import sys
from pathlib import Path

SC = Path("/tmp/createQuestionEv-scratch")
name = sys.argv[1]
run = SC / "runs" / name
summary = json.loads((run / "summary.json").read_text())
out = ["", "## Question, answer and body comparison", ""]
screens = sorted(run.glob("screen-question-*.txt"))
out.append(f"- AskUserQuestion calls (tool calls in the transcripts): {summary['observed']['questions_as_tool_calls']}; question screens seen by the driver: {len(screens)}")
questions = []
for tf in sorted((run / "transcripts").rglob("*.jsonl")):
    for raw in tf.read_text(errors="replace").splitlines():
        if '"AskUserQuestion"' in raw:
            rec = json.loads(raw)
            if rec.get("type") != "assistant":
                continue
            for b in (rec.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion":
                    questions.append((tf.name, b.get("input") or {}))
for n, (tfn, payload) in enumerate(questions, 1):
    for q in payload.get("questions", []):
        text = q.get("question", "")
        opts = " / ".join(o.get("label", "") for o in q.get("options", []))
        out.append(f"- question {n} (full text from the tool call in `transcripts/{tfn}`): {text}")
        out.append(f"  - options: {opts}")
        named = [f for f in ("create_issue.py", "issue_logger.py") if f in (summary.get("description") or "")]
        out.append("  - contradicted items named in the question: " + ", ".join(f"`{f}` {'yes' if f in text else 'NO'}" for f in named))
answers = []
for tf in sorted((run / "transcripts").rglob("*.jsonl")):
    for raw in tf.read_text(errors="replace").splitlines():
        if "have been answered" in raw:
            rec = json.loads(raw)
            if rec.get("type") != "user":
                continue
            for b in (rec.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    answers.append((tf.name, str(b.get("content"))))
for n, (tfn, ans) in enumerate(answers, 1):
    picked = re.findall(r'"="([^"]+)"', ans.replace('\\"', '"'))
    out.append(f"- answer {n} (tool result in `transcripts/{tfn}`): selected {picked or ans[-120:]}")
for s in screens:
    lines = [ln for ln in s.read_text().splitlines() if re.match(r"^\s*[❯>]?\s*\d+\.\s", ln)]
    out.append(f"- options on `{s.name}`: " + " / ".join(ln.strip()[:40] for ln in lines))
at_q = sorted(run.glob("at-question-1-issue-body.md"))
posted = sorted((run / "gh-posted").glob("posted-issue-*.md"))
if at_q and posted:
    a, b = at_q[0].read_text(), posted[-1].read_text()
    out += ["", f"Draft body at question time (`{at_q[0].name}`) against the posted body (`gh-posted/{posted[-1].name}`):", "", "```diff"]
    out += list(difflib.unified_diff(a.splitlines(), b.splitlines(), "draft body at question time", "posted body", lineterm="", n=0))[:80]
    out.append("```")
    for f in ("create_issue.py", "issue_logger.py"):
        out.append(f"- `{f}` in the draft body at question time: {a.count(f)} time(s); in the posted body: {b.count(f)} time(s)")
else:
    out.append("- body comparison: not evidenced (no body captured at question time or no posted body)")
record = run / "record.md"
base = record.read_text().split("\n## Question, answer and body comparison")[0] if record.exists() else ""
record.write_text(base.rstrip("\n") + "\n" + "\n".join(out) + "\n")
print("\n".join(out)[:3000])
