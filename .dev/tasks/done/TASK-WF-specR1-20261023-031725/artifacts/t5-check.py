"""Task 5 structural checks for .github/workflows/boundary-guard.yml (run with: uv run python)."""
import difflib
import pathlib
import subprocess
import sys

import yaml

PKG = pathlib.Path(".dev/tasks/to-do/TASK-WF-specR1-20261023-031725")
BASE_REV = (PKG / "artifacts/t1-head.txt").read_text().strip()
PATH = ".github/workflows/boundary-guard.yml"
base = subprocess.run(["git", "show", f"{BASE_REV}:{PATH}"], check=True, capture_output=True, text=True).stdout
new = pathlib.Path(PATH).read_text()
bl, nl = base.split("\n"), new.split("\n")
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        fails.append(name)


def idx(lines, needle, start=0):
    return next(i for i in range(start, len(lines)) if needle in lines[i])


def on_block(lines):
    s = lines.index("on:")
    e = max(i for i, l in enumerate(lines) if "'tests/swarm/test_no_scoring_engine.py'" in l)
    return "\n".join(lines[s:e + 1])


# Structure
by, ny = yaml.safe_load(base), yaml.safe_load(new)
bon, non = by.get(True, by.get("on")), ny.get(True, ny.get("on"))
check("structure: parsed on-block equal", bon == non and bon is not None)
check("structure: raw 'on:' .. last paths entry byte-identical", on_block(bl) == on_block(nl))
check("structure: workflow name and job keys unchanged", by["name"] == ny["name"] and list(by["jobs"]) == list(ny["jobs"]))


# Header comment block (text anchored, between the 'apply and what to verify' line and '# This is the CI side')
def header(lines):
    a = idx(lines, "#     apply and what to verify on review,") + 1
    b = idx(lines, "# This is the CI side")
    return "\n".join(lines[a:b])


h = header(nl)
check("header: contains 'advisory'", "advisory" in h)
check("header: no 'gates'", "gates" not in h)
check("header: no 'requiring this check'", "requiring this check" not in h)
check("header: base block was the unedited text (anchor sanity)", "requiring this check" in header(bl) and "gates" in header(bl))
check("header: no half-edit, no leftover 'combined with branch protection'", "combined with branch protection" not in h and "merge until a human" not in h)

# Job name
name = ny["jobs"]["flag-boundary-touch"]["name"]
check("job name: contains 'boundary' and 'advisory', no 'required'",
      "boundary" in name and "advisory" in name and "required" not in name.lower(), name)
check("job name: ci.py rule \"boundary\" in name.lower()", "boundary" in name.lower())

# ::warning line
warn = [l for l in nl if "::warning" in l]
check("warning: exactly one ::warning line", len(warn) == 1)
w = warn[0].lstrip(" ")
check("warning: starts with echo \"::warning title=Mechanical-merge boundary touched::",
      w.startswith('echo "::warning title=Mechanical-merge boundary touched::'))
check("warning: contains 'advisory'", "advisory" in w)
check("warning: no 'Human review is required' and no 'before merge'",
      "Human review is required" not in w and "before merge" not in w)

# Summary item 3
a = idx(nl, "3. **PR-review discipline**")
b = idx(nl, "4. **Boundary test**")
item3 = "\n".join(nl[a:b])
check("item 3: contains 'advisory'", "advisory" in item3)
check("item 3: no 'branch protection must require'", "branch protection must require" not in item3)

# Diff line
DL = 'git diff --name-only "$BASE_SHA...$HEAD_SHA" -- \\'
dls = [i for i, l in enumerate(nl) if DL in l]
check("diff: exactly one three-dot diff line", len(dls) == 1)
check("diff: no two-dot '\"$BASE_SHA\" \"$HEAD_SHA\"' left", not any('"$BASE_SHA" "$HEAD_SHA"' in l for l in nl))
bd = idx(bl, 'git diff --name-only "$BASE_SHA" "$HEAD_SHA" -- \\')
check("diff: five pathspec lines after it equal the base's", nl[dls[0] + 1:dls[0] + 6] == bl[bd + 1:bd + 6] and len(nl[dls[0] + 1:dls[0] + 6]) == 5)


# Checklist block byte-identical
def checklist(lines):
    s = idx(lines, "### Required reviewer checks")
    e = next(i for i in range(s, len(lines)) if lines[i].strip() == "EOF")
    return "\n".join(lines[s:e + 1])


check("checklist: '### Required reviewer checks' .. EOF byte-identical", checklist(bl) == checklist(nl))

# Only the expected places changed
allowed_prefixes = ("#   * (combined", "#     merge until a human", "    name: Mechanical-merge boundary touched",
                    '          echo "::warning', "             touch; branch protection must require",
                    '          git diff --name-only "$BASE_SHA" "$HEAD_SHA"')
bad = []
sm = difflib.SequenceMatcher(None, bl, nl, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    for l in bl[i1:i2]:
        if not l.startswith(allowed_prefixes):
            bad.append(l)
check("scope: every changed base line is one of the five intended places", not bad, "; ".join(bad))
check("scope: file name kept (boundary-guard.yml) and top-level name unchanged", ny["name"] == by["name"])

print("RESULT", "FAIL " + ", ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
