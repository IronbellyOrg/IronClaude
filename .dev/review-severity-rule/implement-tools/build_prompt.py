"""Fill the closed /sc:implement reviewer template for one review and save it as prompt-<k>-<j>.md.

Usage (repo root): uv run python -I .dev/review-severity-rule/implement-tools/build_prompt.py <task-number> <k> <j> \
    [--delta <path>] [--prior <path>] [--recheck <path>]
Prints the saved prompt path. The diff slot names the saved diff file (artifacts/diffs/T<id>-r<k>-<j>.diff, written by
qdiff.sh) with its absolute path, because diffs of these tasks are too large to inline.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path.cwd()
S = "TASK-WF-removeTheAnyIssu-20261102-053741"
P = ROOT / ".dev/tasks/to-do" / S
TOOLS = ROOT / ".dev/review-severity-rule/implement-tools"

n, k, j = sys.argv[1], sys.argv[2], sys.argv[3]
opts = dict(zip(sys.argv[4::2], sys.argv[5::2]))
tid = f"T{n}"
plan = (P / f"{S}.md").read_text()
m = re.search(rf"^## Task {n}:.*?(?=^## )", plan + "\n## END", re.S | re.M)
brief = m.group(0).strip()
acs = len(re.findall(r"^- ", brief.split("Acceptance criteria:", 1)[1], re.M))
brief += "\n\nAC ids: " + ", ".join(f"{tid}.AC{i}" for i in range(1, acs + 1)) + " (the Acceptance criteria bullets, in order)."
if "--brief-extra" in opts:
    brief += "\n\n" + pathlib.Path(opts["--brief-extra"]).read_text().strip()
cons = re.search(r"^## Constraints\n(.*?)(?=^## )", plan, re.S | re.M).group(1).strip()
start = [ln.split("sha=")[1] for ln in (P / "progress.md").read_text().splitlines() if ln.startswith(f"{tid}: start sha=")][-1]
diff = P / "artifacts/diffs" / f"{tid}-r{k}-{j}.diff"
slots = {
    "task_brief": brief,
    "global_constraints": cons + f"\nRepository root: {ROOT}. Plan: {P / (S + '.md')}.",
    "start_sha": start,
    "diff": f"saved in full at {diff} (git diff of the start tree against the reviewed tree over src/, plugins/, tests/ "
            f"and CHANGELOG.md; new files appear in full). Read the whole file; read live files in the worktree as needed.",
    "delta_diff": pathlib.Path(opts["--delta"]).read_text() if "--delta" in opts else "",
    "prior_findings": pathlib.Path(opts["--prior"]).read_text() if "--prior" in opts else "",
    "recheck_list": pathlib.Path(opts["--recheck"]).read_text() if "--recheck" in opts else "",
}
text = (TOOLS / "reviewer-template.txt").read_text()
for key, val in slots.items():
    text = text.replace("{" + key + "}", val)
out = P / "artifacts/retries" / tid / f"prompt-{k}-{j}.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(start + "\n" + text)
# Reviewer-readable copy outside the retry folder (reviewers may not read artifacts/retries/).
copy = P / "artifacts/review-prompts" / f"{tid}-{k}-{j}.md"
copy.parent.mkdir(parents=True, exist_ok=True)
copy.write_text(text)
print(out)
print(copy)
