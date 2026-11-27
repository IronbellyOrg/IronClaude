"""Per-run record of the additions: is each New material item in the posted body and in the final output?

Usage: addition_report.py <run name>   (writes runs/<name>/record.md; deterministic, raw files cited)

Rule, stated in every record: for each addition (every non-empty line under `## New material` of draft-notes.md except
None, optional dash removed) take its distinctive tokens (4+ characters, paths and identifiers kept, common words
dropped). In a text, look at every single line and every window of three consecutive lines; the best window's share of
the addition's tokens is its score. Score 0.5 or more counts as "present" and the best window's line number and first
words are printed so that a reader can check the match by eye. This is an approximation: a paraphrase can score low
and a near-duplicate can score high, which is why the line is named.
"""

import json
import re
import sys
from pathlib import Path

SC = Path("/tmp/createQuestionEv-scratch")
name = sys.argv[1]
run = SC / "runs" / name
summary = json.loads((run / "summary.json").read_text())
STOP = set("""that this with from which when have will their there were than into only also each does such
about after because before between during other should these those through under where while would could still
its the and for are was has not but can may all any one two""".split())


def tokens(text: str) -> set[str]:
    return {t.lower().strip(".,:;()`'\"") for t in re.findall(r"[A-Za-z0-9_./:-]{4,}", text)} - STOP


def best_window(item: str, text: str) -> tuple[float, int, str]:
    want = tokens(item)
    if not want:
        return 0.0, 0, ""
    lines = text.splitlines()
    best = (0.0, 0, "")
    for size in (1, 2, 3):
        for i in range(0, max(1, len(lines) - size + 1)):
            window = " ".join(lines[i : i + size]).lower()
            score = len([t for t in want if t in window]) / len(want)
            if score > best[0]:
                best = (score, i + 1, lines[i].strip()[:50])
    return best


def verdict(score: float) -> str:
    """yes at 50 percent or more, probably (check the named line) from 33 percent, else no."""
    return "yes" if score >= 0.5 else ("probably" if score >= 0.33 else "no")


def notes_additions(text: str) -> tuple[list[str], list[str]]:
    clean = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out: dict[str, list[str]] = {"New material": [], "Contradictions": []}
    current = None
    for ln in clean.splitlines():
        if ln.startswith("## "):
            current = ln[3:].strip()
            continue
        item = re.sub(r"^[-*]\s+", "", ln.strip())
        if current in out and item and item != "None":
            if ln.startswith((" ", "\t")) and out[current]:  # an indented line continues the item above it
                out[current][-1] += " | " + item
            else:
                out[current].append(item)
    return out["New material"], out["Contradictions"]


notes_files = sorted((run / "dev-issues").glob("*/draft-notes.md"))
notes = notes_files[0].read_text() if notes_files else ""
additions, contradictions = notes_additions(notes)
posted = sorted((run / "gh-posted").glob("posted-issue-*.md"))
body = posted[-1].read_text() if posted else ""
final = (run / "final-output.txt").read_text()
kept = [ln for ln in final.splitlines() if re.sub(r"^[-*\s]+", "", ln).startswith("kept without approval:")]
listed, on = [], False
for ln in final.splitlines():
    if re.search(r"(?i)without (asking|approval)", ln) and not ln.lstrip().startswith(("- kept", "* kept")):
        on = True
        continue
    if on:
        if ln.strip().startswith(("- ", "* ")):
            listed.append(ln.strip())
        elif ln.strip().startswith("```") or (ln.strip() == "" and listed):
            break
shown = bool(re.search(r"(?i)approve this body|approval of the (full )?body|show(n)? the (full )?body", final))
lines = [
    f"# Record of run {name}",
    "",
    f"- depth {summary['depth']}, flags `{summary['flags']}`, marker `{summary['marker']}`",
    f"- expected questions {summary['expected']['questions']}, observed {summary['observed']['questions_as_tool_calls']} as tool calls ({summary['observed']['questions_answered']} answered), {summary['observed']['questions_as_plain_text']} as plain text",
    f"- expected issue create {summary['expected']['issue_create']}, observed {summary['observed']['issue_create']}; issue comment expected {summary['expected']['issue_comment']}, observed {summary['observed']['issue_comment']}",
    f"- raw files: fake gh log `runs/{name}/gh.log`, transcripts `runs/{name}/transcripts/`, notes `{notes_files[0].relative_to(SC) if notes_files else 'none'}`, posted body `{posted[-1].relative_to(SC) if posted else 'none'}`, final output `runs/{name}/final-output.txt`",
    f"- body shown to the user for approval: {'yes' if shown else 'no (no approval prompt appears in the final output or on the question screens)'}",
    f"- additions in `draft-notes.md` (New material): {len(additions)}; contradictions in the notes: {len(contradictions)}",
    f"- final output: literal `kept without approval: <item>` lines (the format of `refs/create.md` Wave 5 step 8): {len(kept)}; bullet lines listed under a \"without asking / without approval\" heading instead: {len(listed)}",
    "- how `present` is decided (approximate): the best single line or window of three lines of the text shares the given share of the addition's distinctive tokens: `yes` is 50 percent or more, `probably` is 33 to 49 percent (the named line is likely the same fact reworded; check it by eye), `no` is below 33 percent; the matching line number and its first words are printed so each answer can be checked",
    "",
    "| # | addition (first words) | in notes | in posted body (best line, score) | in final output (best line, score) |",
    "|---|---|---|---|---|",
]
for number, item in enumerate(additions, 1):
    bs, bl, bt = best_window(item, body)
    fs, fl, ft = best_window(item, final)
    lines.append(
        f"| {number} | {item[:60].replace('|', '/')} | yes | {verdict(bs)} (line {bl} \"{bt.replace('|', '/')}\", {bs:.0%}) | {verdict(fs)} (line {fl} \"{ft.replace('|', '/')}\", {fs:.0%}) |"
    )
(run / "record.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
