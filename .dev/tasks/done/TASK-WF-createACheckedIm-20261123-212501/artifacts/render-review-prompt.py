"""Render the installed closed review template without changing its criteria."""
import argparse
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("task", type=int)
parser.add_argument("start")
parser.add_argument("--template", type=Path, required=True)
parser.add_argument("--package", type=Path, required=True)
parser.add_argument("--files", nargs="+", required=True)
parser.add_argument("--attempt", type=int, default=1)
parser.add_argument("--review-index", type=int, default=1)
parser.add_argument("--checked-at", default="2026-11-24T15:14:41Z")
parser.add_argument("--previous-tree")
parser.add_argument("--prior", type=Path)
parser.add_argument("--recheck", default="")
args = parser.parse_args()
pkg = args.package.resolve()
root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
plan = (pkg / (pkg.name + ".md")).read_text()
constraints = plan.split("## Constraints\n", 1)[1].split("## Phase 1:", 1)[0].strip()
match = re.search(rf"^## Task {args.task}:.*?(?=^## Phase |\Z)", plan, re.M | re.S)
brief = match.group(0).strip()
body, ac = brief.split("Acceptance criteria:\n", 1)
criteria = ac.splitlines()
number = 0
for i, line in enumerate(criteria):
    if line.startswith("- "):
        number += 1
        criteria[i] = f"- T{args.task}.AC{number}: " + line[2:]
brief = body + "Acceptance criteria:\n" + "\n".join(criteria)
result = subprocess.run(["git", "diff", args.start, "--", *args.files], text=True, capture_output=True, check=True)
diff = result.stdout
for filename in args.files:
    path = root / filename
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", "--", filename], capture_output=True).returncode == 0
    if not tracked:
        diff += f"\nFull task-created file, source line numbers: {filename}\n" + "\n".join(f"{filename}:{n}: {line}" for n, line in enumerate(path.read_text().splitlines(), 1)) + "\n"
diff += "\nCodegraph context\nindex_state: fresh\naccess: mcp\nchecked_at: " + args.checked_at + "\nworktree_root:" + str(root) + "\nprojectPath: " + str(root) + "\ncall codegraph only when index_state: fresh, never to widen scope\n"
diff += "Graph rows are leads. Native Reads confirm public registration, schema/preflight field binding and unchanged runtime contracts. No direct function call is inferred from a callback-registration row.\n"
ref = args.template.read_text()
section = ref.split("## Subagent prompt (when not inline)", 1)[1]
template = re.search(r"```\n(Review one task for spec compliance\..*?)\n```", section, re.S).group(1)
delta = subprocess.check_output(["git", "diff", args.previous_tree, "--", *args.files], text=True) if args.previous_tree else ""
prior = "\n".join(line for line in args.prior.read_text().splitlines() if line.startswith("F") and "sev=blocking" in line) if args.prior else ""
slots = {"task_brief": brief, "global_constraints": constraints, "start_sha": args.start, "diff": diff, "delta_diff": delta, "prior_findings": prior, "recheck_list": args.recheck}
for key, value in slots.items():
    template = template.replace("{" + key + "}", value)
assert not any("{" + key + "}" in template for key in slots)
output = pkg / "artifacts" / "retries" / f"T{args.task}" / f"prompt-{args.attempt}-{args.review_index}.md"
output.parent.mkdir(parents=True, exist_ok=True)
with output.open("x") as stream:
    stream.write("start=" + args.start + "\n" + template + "\n")
print(output)
