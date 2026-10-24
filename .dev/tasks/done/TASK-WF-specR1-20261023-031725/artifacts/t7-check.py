"""Task 7 checks for the Codecov step in .github/workflows/test.yml (run with: uv run python)."""
import copy
import pathlib
import re
import subprocess
import sys

import yaml

PKG = pathlib.Path(".dev/tasks/to-do/TASK-WF-specR1-20261023-031725")
BASE_REV = (PKG / "artifacts/t1-head.txt").read_text().strip()
PATH = ".github/workflows/test.yml"
base_txt = subprocess.run(["git", "show", f"{BASE_REV}:{PATH}"], check=True, capture_output=True, text=True).stdout
new_txt = pathlib.Path(PATH).read_text()
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        fails.append(name)


# F is read programmatically from the single Decision: line of Task 2's file
t2 = (PKG / "artifacts/t2-codecov-v4.md").read_text().splitlines()
dec = [l for l in t2 if l.startswith("Decision:")]
check("Task 2 file: exactly one Decision: line", len(dec) == 1)
m = re.findall(r"\bfiles?\b", dec[0])
check("Decision line names exactly one of file/files", len(m) == 1 and m[0] in ("file", "files"), str(m))
F = m[0]
print("F =", F)

by, ny = yaml.safe_load(base_txt), yaml.safe_load(new_txt)
STEP = "Upload coverage to Codecov"


def find(doc):
    hits = [(j, s) for j, job in doc["jobs"].items() for s in job["steps"] if s.get("name") == STEP]
    return hits


hits = find(ny)
check("exactly one 'Upload coverage to Codecov' step", len(hits) == 1)
jname, step = hits[0]
check("step uses codecov/codecov-action@v4", step["uses"] == "codecov/codecov-action@v4")
want = {F: "./coverage.xml", "token": "${{ secrets.CODECOV_TOKEN }}", "flags": "unittests",
        "name": "codecov-umbrella", "fail_ci_if_error": False}
check("with mapping equals exactly the expected mapping (no deprecated/second file input, no threshold)",
      step["with"] == want, str(step["with"]))
check("fail_ci_if_error is the boolean False", step["with"].get("fail_ci_if_error") is False)
check("no threshold-like keys", not any(re.search(r"thresh|target|min", k, re.I) for k in step["with"]))


def stripped(doc):
    d = copy.deepcopy(doc)
    for job in d["jobs"].values():
        for s in job["steps"]:
            if s.get("name") == STEP:
                s.pop("with")
    return d


check("rest of test.yml equal to base after removing that step's with mapping", stripped(by) == stripped(ny))
bon, non = by.get(True) or by.get("on"), ny.get(True) or ny.get("on")
check("on block, top-level keys, jobs, job-level keys and step counts equal base",
      bon == non and list(by) == list(ny) and list(by["jobs"]) == list(ny["jobs"])
      and all(list(by["jobs"][j]) == list(ny["jobs"][j]) and len(by["jobs"][j]["steps"]) == len(ny["jobs"][j]["steps"])
              for j in by["jobs"]))
check("no angle-bracket placeholder introduced", new_txt.count("<") == base_txt.count("<"))
print("RESULT", "FAIL " + ", ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
