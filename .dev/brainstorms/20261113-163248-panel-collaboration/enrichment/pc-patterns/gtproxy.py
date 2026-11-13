"""Keyword proxy for per-reviewer ground-truth hits; calibrated against the judged panel-level issue table.
shortcut: regex proxy, not a judge; precision/recall printed against issue-table per_row found lists."""
import json, re, glob, collections, itertools
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PKD = {"DS": "TASK-WF-designSpec-20261107-075614", "AL": "TASK-WF-makeTheAliasOnly-20261105-051649", "DE": "TASK-WF-design-20261108-041415"}
R = json.load(open("/tmp/pc-patterns/records.json"))
ORDER = ["ember", "luna", "haiku", "sonnet", "grok", "terra", "wonder"]

def body(r):
    md = open(f"{E}/{PKD[r['pkg']]}/reviews/combos/{r['run']}/{r['rid']}.md").read()
    md = re.sub(r"## Coverage.*?(?=\n## )", "", md, flags=re.S)  # drop the coverage statement (lists files checked)
    return md

def T(f, *ts):
    return any(t in f["tasks"] for t in ts)

# per-finding signatures: (label, pkg, kind, fn(finding_text, finding) -> bool)
I = re.I
SIG = {
 "B1": ("DS", "satisfiability", lambda s, f: T(f, "1") and re.search(r"stopping|unbounded|provabl|no bound|no (method|way) to (prove|show|know)|cannot (be )?(prove|proven|verif|show)|exhaustive", s, I)),
 "B2": ("DS", "satisfiability", lambda s, f: T(f, "1") and re.search(r"O3", s) and re.search(r"scope|four|files|found for", s, I)),
 "B3": ("DS", "satisfiability", lambda s, f: T(f, "9") and re.search(r"condition|word.?list|fails? (when|on)|itself", s, I)),
 "B4": ("DS", "contradiction", lambda s, f: re.search(r"unreadable|short timeline|incomplete read", s, I) and re.search(r"engage", s, I)),
 "B5": ("DS", "contradiction", lambda s, f: re.search(r"draft_guard_unavailable|\bunavailable\b", s) and re.search(r"released|exit.report|guard_status", s, I)),
 "I1": ("DS", "contradiction", lambda s, f: re.search(r"user_override", s)),
 "I2": ("DS", "contradiction", lambda s, f: re.search(r"resume_decision", s) and re.search(r"target_sha|applied_edits|signature|parameter|argument", s, I)),
 "I3": ("DS", "contradiction", lambda s, f: T(f, "10") and re.search(r"\bmint", s, I)),
 "I4": ("DS", "satisfiability", lambda s, f: (re.search(r"case.sensitiv", s, I) or (T(f, "12") and re.search(r"grep", s) and re.search(r"heading|Merge guard", s))) ),
 "I5": ("DS", "missing-task/cross-doc", lambda s, f: re.search(r"changelog", s, I)),
 "B6": ("AL", "contradiction", lambda s, f: re.search(r"slot|T\dModel|retry.ladder|sprint|auggie", s, I) and re.search(r"alias", s, I)),
 "B7": ("AL", "cross-doc", lambda s, f: T(f, "6") and re.search(r"nothing is set|real model ids?|glm|defaults file|exports? real|workspace defaults", s, I)),
 "B8": ("AL", "cross-doc", lambda s, f: re.search(r"all other primitives|no .?model:.? line|without a .?model|skip(s|ped)? (them|files)|have no model", s, I)),
 "I6": ("AL", "cross-doc", lambda s, f: T(f, "7") and re.search(r"real model ids?|defaults file|exports", s, I)),
 "I7": ("DE", "missing-task/cross-doc", lambda s, f: re.search(r"worker.contract|classification table|exact.line|test_issue_worker_agents|other test|full (test )?suite|whole (test )?suite|wider suite|rest of the (test )?suite|tests/skills/(?!test_issue_protocol)", s, I)),
 "I8": ("DE", "ambiguity", lambda s, f: re.search(r"single.select|option (id|name)|single_select_option|numeric (option )?id|\.name\b", s, I) or (re.search(r"read.?back", s, I) and re.search(r"match|compare|interpret|how to (tell|check|verify)|what (counts|value)", s, I) and re.search(r"field|complexity", s, I))),
}
PKG_OF = {k: v[0] for k, v in SIG.items()}

def hits(r):
    out = set()
    for f in r["findings"]:
        s = " ".join([f["claim"], f["anchor"], f["anchor2"], f["refs"]])
        for lab, (p, kind, fn) in SIG.items():
            if p == r["pkg"] and fn(s, f):
                out.add(lab)
    return out

for r in R:
    r["gt"] = sorted(hits(r))

# calibration vs judged per-row panel results
judged = {}
for jf in glob.glob(f"{E}/analysis/issue-table/issue-*.json"):
    if "legend" in jf or "direct" in jf:
        continue
    J = json.load(open(jf))
    for row, v in J.get("per_row", {}).items():
        judged[row] = set(v["found"])
LEG = {l.split("\t")[0]: l.split("\t")[1] for l in open(f"{E}/analysis/issue-table/issue-legend.tsv").read().splitlines()[1:]}
pkmap = {"designSpec": "DS", "alias": "AL", "control": "DE"}
tp = fp = fn = 0; perlab = collections.Counter(); perlab_fp = collections.Counter(); perlab_fn = collections.Counter()
for row, found in judged.items():
    rs = [r for r in R if r["run"] == row]
    if not rs:
        continue
    prox = set().union(*[set(r["gt"]) for r in rs])
    for lab in SIG:
        a, b = lab in prox, lab in found
        tp += a and b; fp += a and not b; fn += b and not a
        if a and b: perlab[lab] += 1
        if a and not b: perlab_fp[lab] += 1
        if b and not a: perlab_fn[lab] += 1
print(f"## Proxy calibration against judged panel rows ({len(judged)} rows): TP={tp} FP={fp} FN={fn} precision={tp/(tp+fp):.2f} recall={tp/(tp+fn):.2f}\n")
print("| label | TP | FP | FN |"); print("|---|---|---|---|")
for lab in SIG:
    print(f"| {lab} | {perlab[lab]} | {perlab_fp[lab]} | {perlab_fn[lab]} |")

by = collections.defaultdict(list)
for r in R:
    by[r["model"]].append(r)
print("\n## Proxy hit rate per reviewer run (share of that model's runs on the package whose findings match the issue)\n")
labs = list(SIG)
print("| model | " + " | ".join(f"{l} ({PKG_OF[l]}, {SIG[l][1]})" for l in labs) + " |"); print("|" + "---|" * (len(labs) + 1))
for m in ORDER:
    cells = []
    for l in labs:
        rs = [r for r in by[m] if r["pkg"] == PKG_OF[l]]
        cells.append(f"{100*sum(l in r['gt'] for r in rs)/len(rs):.0f}%" if rs else "-")
    print(f"| {m} | " + " | ".join(cells) + " |")

GROUPS = {"cross-doc / missing-task (I5, I7, B7, B8, I6)": ["I5", "I7", "B7", "B8", "I6"],
          "satisfiability (B1, B2, B3, I4)": ["B1", "B2", "B3", "I4"],
          "in-plan contradiction (B4, B5, I1, I2, I3, B6)": ["B4", "B5", "I1", "I2", "I3", "B6"]}
print("\n## Proxy hits per run by issue kind (mean number of issues of that kind matched per run on the relevant packages)\n")
print("| model | " + " | ".join(GROUPS) + " |"); print("|" + "---|" * (len(GROUPS) + 1))
for m in ORDER:
    cells = []
    for g, ls in GROUPS.items():
        tot = 0; denom = 0
        for l in ls:
            rs = [r for r in by[m] if r["pkg"] == PKG_OF[l]]
            tot += sum(l in r["gt"] for r in rs); denom += len(rs)
        cells.append(f"{tot/denom*len(ls):.2f} of {len(ls)}" if denom else "-")
    print(f"| {m} | " + " | ".join(cells) + " |")
json.dump(R, open("/tmp/pc-patterns/records_gt.json", "w"))
