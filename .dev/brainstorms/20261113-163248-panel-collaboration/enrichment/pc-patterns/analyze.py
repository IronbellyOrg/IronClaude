"""Aggregate records.json into per-model tables (markdown to stdout)."""
import json, collections, statistics as st, itertools, re, sys
sys.path.insert(0, "/tmp/pc-patterns")
R = json.load(open("/tmp/pc-patterns/records.json"))
ORDER = ["ember", "luna", "haiku", "sonnet", "grok", "terra", "wonder", "sol"]
by = collections.defaultdict(list)
for r in R:
    by[r["model"]].append(r)

def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else float("nan")
def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")
def pct(n, d):
    return f"{100*n/d:.0f}%" if d else "-"

print("## T1 Tool-use profile per model (median per run unless marked)\n")
print("| model | runs | tool calls | Read | Bash | Grep+Glob | MCP (codegraph/augment/...) | Web | distinct repo files (Read or named in Bash) | runs reading source.md | runs touching a plan-named repo file | runs touching any test file | runs touching a plan-named test file | runs touching any .py/.sh code | turns | wall s | output tok |")
print("|" + "---|" * 17)
for m in ORDER:
    rs = by[m]; n = len(rs)
    g = lambda k: med([r["tools"].get(k, 0) for r in rs])
    print(f"| {m} | {n} | {med([r['n_tools'] for r in rs])} | {g('Read')} | {g('Bash')} | {med([r['tools'].get('Grep',0)+r['tools'].get('Glob',0) for r in rs])} | "
          f"{med([r['mcp_calls'] for r in rs])} (mean {mean([r['mcp_calls'] for r in rs]):.1f}) | {mean([r['tools'].get('WebFetch',0)+r['tools'].get('WebSearch',0) for r in rs]):.2f} mean | "
          f"{med([r['n_repo_files'] for r in rs])} (mean {mean([r['n_repo_files'] for r in rs]):.1f}) | {pct(sum(r['read_source'] for r in rs), n)} | "
          f"{pct(sum(bool(r['plan_named_opened']) for r in rs), n)} | {pct(sum(bool(r['test_opened']) for r in rs), n)} | {pct(sum(bool(r['plan_test_opened']) for r in rs), n)} | "
          f"{pct(sum(bool(r['code_opened']) for r in rs), n)} | {med([r['num_turns'] for r in rs])} | {med([r['wall_s'] for r in rs])} | {med([r['out_tok'] for r in rs])} |")

print("\n### T1a Method markers (share of runs)\n")
print("| model | invoked a Skill | Read the candidate with a tool | repo files via Read tool (mean) | searched or opened tests/ | ran pytest | ran code/make/ruff | used codegraph/augment MCP | median thinking tokens |")
print("|---|---|---|---|---|---|---|---|---|")
for m in ORDER:
    rs = by[m]; n = len(rs)
    print(f"| {m} | {pct(sum(r['used_skill'] for r in rs), n)} | {pct(sum(r['read_candidate'] for r in rs), n)} | {mean([len(r['read_repo_files']) for r in rs]):.1f} | "
          f"{pct(sum(r['searched_tests'] for r in rs), n)} | {pct(sum(r['ran_pytest'] for r in rs), n)} | {pct(sum(r['ran_code'] for r in rs), n)} | {pct(sum(r['mcp_calls'] > 0 for r in rs), n)} | {med([r['thinking_tok'] for r in rs])} |")

print("\n### T1b Tool-use per model per package (mean distinct repo files / share opening any test file / mean tool calls)\n")
print("| model | DS files | DS test% | DS calls | AL files | AL test% | AL calls | DE files | DE test% | DE calls |")
print("|" + "---|" * 10)
for m in ORDER:
    row = [m]
    for p in ["DS", "AL", "DE"]:
        rs = [r for r in by[m] if r["pkg"] == p]
        if not rs:
            row += ["-", "-", "-"]; continue
        row += [f"{mean([r['n_repo_files'] for r in rs]):.1f} (n={len(rs)})", pct(sum(bool(r['test_opened']) for r in rs), len(rs)), f"{mean([r['n_tools'] for r in rs]):.1f}"]
    print("| " + " | ".join(row) + " |")

# targeted cross-document probes
PROBES = {"DE": ["tests/skills/test_worker_contract.py", "tests/skills/test_issue_protocol.py"],
          "DS": ["CHANGELOG.md", "src/superclaude/pr_submit/fsm.py", "src/superclaude/pr_submit/run_log.py", "src/superclaude/pr_submit/models.py"],
          "AL": ["src/superclaude/skills/ccsession-tag/ccsession-models.json", "src/superclaude/cli/reflect/commands.py", "tests/skills/test_issue_worker_agents.py"]}
print("\n### T1c Share of runs that opened specific repo files tied to ground-truth issues\n")
hdr = [f"{p}:{f.split('/')[-1]}" for p, fs in PROBES.items() for f in fs]
print("| model | " + " | ".join(hdr) + " |"); print("|" + "---|" * (len(hdr) + 1))
for m in ORDER:
    cells = []
    for p, fs in PROBES.items():
        rs = [r for r in by[m] if r["pkg"] == p]
        for f in fs:
            cells.append(pct(sum(any(x.endswith(f) for x in r["repo_files"]) for r in rs), len(rs)) if rs else "-")
    print(f"| {m} | " + " | ".join(cells) + " |")

print("\n## T2 Report profile per model\n")
print("| model | findings/run (median, mean) | blocking/run (mean) | anchor located in candidate | findings citing source.md | findings spanning >=2 Tasks | findings spanning >=2 sections (incl. Constraints/Goal) | with anchor2 | citing a repo file in refs | contradiction | unpassable-check | missing-requirement | other | data-loss/safety | distinct Tasks anchored/run (mean) |")
print("|" + "---|" * 16)
for m in ORDER:
    rs = by[m]; F = [f for r in rs for f in r["findings"]]; nf = len(F)
    c = collections.Counter(f["cat"] for f in F)
    dt = mean([len({t for f in r["findings"] for t in f["tasks"]}) for r in rs])
    print(f"| {m} | {med([r['n_findings'] for r in rs])}, {mean([r['n_findings'] for r in rs]):.2f} | {mean([r['n_blocking'] for r in rs]):.2f} | {pct(sum(f['anchor_found'] for f in F), nf)} | "
          f"{pct(sum(f['src'] for f in F), nf)} | {pct(sum(f['cross_task'] for f in F), nf)} | {pct(sum(f['cross_sec'] for f in F), nf)} | {pct(sum(f['has_anchor2'] for f in F), nf)} | {pct(sum(f['ext'] for f in F), nf)} | "
          f"{pct(c['contradiction'], nf)} | {pct(c['unpassable-check'], nf)} | {pct(c['missing-requirement'], nf)} | {pct(c['other'], nf)} | {pct(c['data-loss']+c['safety'], nf)} | {dt:.2f} |")

# missing-task wording
MT = re.compile(r"\b(no task|not (?:updat|includ|cover|list)|never (?:updat|chang|mention)|omits?|does not (?:updat|includ|cover|plan|list)|missing|left stale|stays? (?:stale|red)|other (?:test|file)s?)\b", re.I)
TESTRE = re.compile(r"\btests?\b|test_\w+|pytest")
PATHRE = re.compile(r"[\w-]+/[\w./-]+\.(py|md|sh|json)")
print("\n### T2b Finding content markers (share of findings whose claim matches)\n")
print("| model | claim names a missing/omitted update | claim names a test/test file | claim names a repo path |")
print("|---|---|---|---|")
for m in ORDER:
    F = [f for r in by[m] for f in r["findings"]]; nf = len(F)
    a = pct(sum(bool(MT.search(f['claim'])) for f in F), nf)
    b = pct(sum(bool(TESTRE.search(f['claim'])) for f in F), nf)
    c = pct(sum(bool(PATHRE.search(f['claim'])) for f in F), nf)
    print(f"| {m} | {a} | {b} | {c} |")

print("\n## T3 Task anchoring: concentration per model per package\n")
print("Share of a model's task anchors (across all its runs on that package) that fall in its 3 most-cited tasks, and the top tasks with run share (share of runs citing that task).\n")
print("| model | pkg | runs | task anchors | top-3 share | top tasks (share of runs citing) | distinct tasks ever |")
print("|---|---|---|---|---|---|---|")
for p in ["DS", "AL", "DE"]:
    for m in ORDER:
        rs = [r for r in by[m] if r["pkg"] == p]
        if not rs:
            continue
        cnt = collections.Counter(t for r in rs for f in r["findings"] for t in f["tasks"])
        runcnt = collections.Counter(t for r in rs for t in {t for f in r["findings"] for t in f["tasks"]})
        tot = sum(cnt.values())
        top = cnt.most_common(3)
        share = sum(v for _, v in top) / tot if tot else 0
        tops = ", ".join(f"T{t} {100*runcnt[t]/len(rs):.0f}%" for t, _ in cnt.most_common(4))
        print(f"| {m} | {p} | {len(rs)} | {tot} | {100*share:.0f}% | {tops} | {len(cnt)} |")

# GT task coverage: share of runs anchoring the tasks where GT items live
GT_TASKS = {"DE": {"GT1(missing-task: T12 gate + T2/3/5 edits)": {"12"}, "GT2(ambiguity T1 read-back)": {"1"}},
            "DS": {"GT1/GT2(T1 AC3)": {"1"}, "GT3(T9)": {"9"}, "GT4/GT5(T8)": {"8"}, "GT8(T10)": {"10"},"GT6(T3)": {"3"}, "GT7(T4 resume sig)": {"4"}, "GT9(T12 grep)": {"12"}, "GT10(T2 changelog)": {"2"}},
            "AL": {"GT1/GT2(T6)": {"6"}, "GT3/GT4(T7)": {"7"}}}
print("\n### T3b Share of runs that anchor at least one finding in the task where a ground-truth issue lives\n")
cols = [(p, k) for p, d in GT_TASKS.items() for k in d]
print("| model | " + " | ".join(f"{p} {k}" for p, k in cols) + " |"); print("|" + "---|" * (len(cols) + 1))
for m in ORDER:
    cells = []
    for p, k in cols:
        rs = [r for r in by[m] if r["pkg"] == p]
        ts = GT_TASKS[p][k]
        cells.append(pct(sum(bool(ts & {t for f in r["findings"] for t in f["tasks"]}) for r in rs), len(rs)) if rs else "-")
    print(f"| {m} | " + " | ".join(cells) + " |")

print("\n## T4 Pairwise Jaccard of anchored Task sets between reviewers in the same row and package\n")
rowgrp = collections.defaultdict(list)
for r in R:
    rowgrp[(r["run"], r["pkg"])].append(r)
pj = collections.defaultdict(list)
for k, rs in rowgrp.items():
    for a, b in itertools.combinations(rs, 2):
        A = {t for f in a["findings"] for t in f["tasks"]}; B = {t for f in b["findings"] for t in f["tasks"]}
        if not A and not B:
            continue
        pj[tuple(sorted([a["model"], b["model"]]))].append(len(A & B) / len(A | B))
print("| pair | n pairs | mean Jaccard | share with zero overlap |")
print("|---|---|---|---|")
for k, v in sorted(pj.items(), key=lambda kv: -len(kv[1])):
    if len(v) >= 4:
        print(f"| {k[0]}+{k[1]} | {len(v)} | {mean(v):.2f} | {pct(sum(x == 0 for x in v), len(v))} |")

# within-model run-to-run Jaccard (same package, different rows) = how repeatable the focus is
print("\n### T4b Run-to-run Jaccard of anchored Task sets for the same model on the same package (all pairs of runs)\n")
print("| model | DS | AL | DE |"); print("|---|---|---|---|")
for m in ORDER:
    cells = []
    for p in ["DS", "AL", "DE"]:
        sets = [{t for f in r["findings"] for t in f["tasks"]} for r in by[m] if r["pkg"] == p]
        js = [len(a & b) / len(a | b) for a, b in itertools.combinations(sets, 2) if a | b]
        cells.append(f"{mean(js):.2f} (runs={len(sets)})" if js else "-")
    print(f"| {m} | " + " | ".join(cells) + " |")

# correlation: exploration depth vs number of findings / cross-task / src
print("\n## T5 Within-model link between exploration and report shape\n")
print("Runs split at the model's own median of distinct repo files read; mean findings per run, share of runs with a finding that names a test, share of runs anchoring any GT task.\n")
print("| model | low-explore runs | findings (low) | findings (high) | test-claim runs (low) | test-claim runs (high) |")
print("|---|---|---|---|---|---|")
for m in ORDER:
    rs = by[m]
    if len(rs) < 6:
        continue
    md = med([r["n_repo_files"] for r in rs])
    lo = [r for r in rs if r["n_repo_files"] <= md]; hi = [r for r in rs if r["n_repo_files"] > md]
    tc = lambda grp: pct(sum(any(TESTRE.search(f["claim"]) for f in r["findings"]) for r in grp), len(grp))
    print(f"| {m} | {len(lo)} (<= {md}) | {mean([r['n_findings'] for r in lo]):.2f} | {mean([r['n_findings'] for r in hi]):.2f} (n={len(hi)}) | {tc(lo)} | {tc(hi)} |")
