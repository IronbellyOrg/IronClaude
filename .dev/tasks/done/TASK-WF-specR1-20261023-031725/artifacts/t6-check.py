"""Task 6 structural checks for .github/workflows/pull-sync-framework.yml (run with: uv run python)."""
import copy
import pathlib
import re
import subprocess
import sys

import yaml

PKG = pathlib.Path(".dev/tasks/to-do/TASK-WF-specR1-20261023-031725")
BASE_REV = (PKG / "artifacts/t1-head.txt").read_text().strip()
PATH = ".github/workflows/pull-sync-framework.yml"
base_txt = subprocess.run(["git", "show", f"{BASE_REV}:{PATH}"], check=True, capture_output=True, text=True).stdout
new_txt = pathlib.Path(PATH).read_text()
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        fails.append(name)


by, ny = yaml.safe_load(base_txt), yaml.safe_load(new_txt)
STEP = "Commit and Push Changes"
JOB = "sync-and-isolate"


def stripped(doc):
    d = copy.deepcopy(doc)
    job = d["jobs"][JOB]
    job.pop("permissions")
    job["steps"] = [s for s in job["steps"] if s.get("name") != STEP]
    return d


bs, ns = stripped(by), stripped(ny)
check("whole document: equal after removing permissions and the Commit step", bs == ns)
check("whole document: same name, on block, top-level keys, job-level keys",
      by["name"] == ny["name"] and (by.get(True) or by.get("on")) == (ny.get(True) or ny.get("on"))
      and list(by) == list(ny) and list(by["jobs"][JOB]) == list(ny["jobs"][JOB]))
check("whole document: step count unchanged", len(by["jobs"][JOB]["steps"]) == len(ny["jobs"][JOB]["steps"]))

check("permissions exactly {contents: write, pull-requests: write}",
      ny["jobs"][JOB]["permissions"] == {"contents": "write", "pull-requests": "write"})

bstep = next(s for s in by["jobs"][JOB]["steps"] if s["name"] == STEP)
nstep = next(s for s in ny["jobs"][JOB]["steps"] if s["name"] == STEP)
check("commit step: name, if, working-directory equal base",
      all(bstep[k] == nstep[k] for k in ("name", "if", "working-directory")))
check("commit step: env equals {GH_TOKEN: ${{ github.token }}} exactly", nstep.get("env") == {"GH_TOKEN": "${{ github.token }}"})
check("commit step: keys are exactly name, if, working-directory, env, run",
      set(nstep) == {"name", "if", "working-directory", "env", "run"})
brun, nrun = bstep["run"].split("\n"), nstep["run"].split("\n")
bi = next(i for i, l in enumerate(brun) if "git commit" in l)
ni = next(i for i, l in enumerate(nrun) if "git commit" in l)
check("commit step: run lines first..'git commit' equal base one for one", brun[:bi + 1] == nrun[:ni + 1] and bi == ni, f"{bi + 1} lines")
check("commit step: state-file block (git add -f docs/.framework-sync-commit) retained",
      any("git add -f docs/.framework-sync-commit" in l for l in nrun[:ni + 1]))

# Joined (backslash-continued) lines of the edited run body
joined, cur = [], ""
for l in nrun:
    if l.rstrip().endswith("\\"):
        cur += l.rstrip()[:-1] + " "
    else:
        joined.append(cur + l)
        cur = ""
check("lines: zero contain HEAD:master", not any("HEAD:master" in l for l in joined))
check("lines: exactly one 'git push --force origin HEAD:refs/heads/sync/framework'",
      sum("git push --force origin HEAD:refs/heads/sync/framework" in l for l in joined) == 1)
gh = [l for l in joined if "gh pr" in l]
check("lines: every 'gh pr' line carries --repo \"$GITHUB_REPOSITORY\"", len(gh) == 2 and all('--repo "$GITHUB_REPOSITORY"' in l for l in gh), f"{len(gh)} gh pr lines")
creates = [l for l in joined if "gh pr create" in l]
check("lines: exactly one 'gh pr create' with --base master and --head sync/framework",
      len(creates) == 1 and "--base master" in creates[0] and "--head sync/framework" in creates[0])
lists = [l for l in joined if "gh pr list" in l]
check("lines: exactly one 'gh pr list', a standalone assignment open_prs=$(gh pr list ...)",
      len(lists) == 1 and re.fullmatch(r"\s*open_prs=\$\(gh pr list [^)]*\)\s*", lists[0]) is not None)
check("gh pr list: filters --head sync/framework --base master --state open --json number --jq 'length'",
      all(t in lists[0] for t in ("--head sync/framework", "--base master", "--state open", "--json number", "--jq 'length'")))
li = next(i for i, l in enumerate(joined) if "gh pr list" in l)
ci = next(i for i, l in enumerate(joined) if "gh pr create" in l)
pi = next(i for i, l in enumerate(joined) if "git push" in l)
check("order: git commit < git push < gh pr list < gh pr create", ni < pi < li < ci)
gate = next(i for i, l in enumerate(joined) if l.strip() == 'if [ "$open_prs" = "0" ]; then')
check("create is gated on open_prs being 0 (if ... ; then .. else reuse echo .. fi)",
      gate < ci and any("reusing" in l for l in joined[ci:]) and joined[ci + 1].strip() == "else")
ifi = next(i for i, l in enumerate(joined) if l.strip() == "if ! git diff --cached --quiet; then")
elsei = max(i for i, l in enumerate(joined) if l.strip() == "else")
nochg = next(i for i, l in enumerate(joined) if 'echo "No changes detected."' in l)
check("else branch: echo \"No changes detected.\" still after the outer else", elsei < nochg and ifi < pi < elsei)
check("file contains no '<' placeholder", "<" not in new_txt)
check("file: no personal-access-token or app-token introduced",
      not re.search(r"secrets\.|app-id|create-github-app-token|PAT", new_txt))

print("RESULT", "FAIL " + ", ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
