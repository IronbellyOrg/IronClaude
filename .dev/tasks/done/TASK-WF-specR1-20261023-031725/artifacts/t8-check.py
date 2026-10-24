"""Task 8 section checks for .github/workflows/README.md (run with: uv run python)."""
import difflib
import pathlib
import re
import subprocess
import sys

PKG = pathlib.Path(".dev/tasks/to-do/TASK-WF-specR1-20261023-031725")
BASE_REV = (PKG / "artifacts/t1-head.txt").read_text().strip()
PATH = ".github/workflows/README.md"
base = subprocess.run(["git", "show", f"{BASE_REV}:{PATH}"], check=True, capture_output=True, text=True).stdout
new = pathlib.Path(PATH).read_text()
bl, nl = base.split("\n"), new.split("\n")
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        fails.append(name)


def section(lines, heading):
    """Lines from the heading to (not including) the next line starting with '#'."""
    s = next(i for i, l in enumerate(lines) if l.startswith(heading))
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("#")), len(lines))
    return lines[s + 1:e]


# Badge line
badge = [l for l in nl if l.startswith("[![Tests]")]
check("badge: exactly one badge line", len(badge) == 1)
b = badge[0]
check("badge: 'IronbellyOrg/IronClaude/actions/workflows/test.yml' twice", b.count("IronbellyOrg/IronClaude/actions/workflows/test.yml") == 2)
check("badge: 'SuperClaude-Org' zero times", "SuperClaude-Org" not in b)
check("badge: image is /badge.svg and link ends test.yml)",
      "https://github.com/IronbellyOrg/IronClaude/actions/workflows/test.yml/badge.svg)" in b and b.endswith("(https://github.com/IronbellyOrg/IronClaude/actions/workflows/test.yml)"))
check("file: no 'SuperClaude-Org/SuperClaude_Framework/actions' anywhere", "SuperClaude-Org/SuperClaude_Framework/actions" not in new)

# Coverage troubleshooting bullet
cov = [l for l in section(nl, "### Coverage upload fails") if l.startswith("- ")]
other = [l for l in cov if "fail_ci_if_error" not in l]
check("coverage: exactly one bullet other than the fail_ci_if_error one", len(other) == 1 and len(cov) == 2)
check("coverage: that bullet contains CODECOV_TOKEN and secrets.CODECOV_TOKEN",
      "CODECOV_TOKEN" in other[0] and "secrets.CODECOV_TOKEN" in other[0])
check("coverage: the fail_ci_if_error bullet is unchanged", any(l in bl for l in cov if "fail_ci_if_error" in l))

# boundary-guard paragraph
bg = "\n".join(section(nl, "### 2. **boundary-guard.yml**"))
check("boundary-guard: contains 'advisory' and 'cannot block'", "advisory" in bg and "cannot block" in bg)
check("boundary-guard: no 'gates', no 'branch protection must require'", "gates" not in bg and "branch protection must require" not in bg)

# pull-sync paragraph
ps = "\n".join(section(nl, "### 4. **pull-sync-framework.yml**"))
check("pull-sync: contains 'sync/framework', 'pull request', 'does not push to master'",
      all(t in ps for t in ("sync/framework", "pull request", "does not push to master")))

# Only the four intended places changed
allowed = ("[![Tests](", "Flags PRs that touch the swarm mechanical-merge boundary", "Scheduled (every 6 hours)", "- Check Codecov token")
bad, changed = [], 0
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, bl, nl, autojunk=False).get_opcodes():
    if tag == "equal":
        continue
    changed += i2 - i1
    bad += [l for l in bl[i1:i2] if not l.startswith(allowed)]
    if (j2 - j1) != (i2 - i1):
        bad.append(f"line-count change at base line {i1 + 1}")
check("diff: only the badge line, Codecov bullet and the two entry paragraphs changed (4 base lines)", not bad and changed == 4, f"{changed} base lines changed; {bad}")
check("README: all heading lines identical to base",
      [l for l in bl if l.startswith("#")] == [l for l in nl if l.startswith("#")])
print("RESULT", "FAIL " + ", ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
