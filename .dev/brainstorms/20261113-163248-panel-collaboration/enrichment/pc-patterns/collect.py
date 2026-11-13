"""Collect per-reviewer-run tool-use and report profiles for valid-era (source.md) rows."""
import json, os, glob, re, hashlib, collections

E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PK = {"TASK-WF-designSpec-20261107-075614": "DS", "TASK-WF-makeTheAliasOnly-20261105-051649": "AL",
      "TASK-WF-design-20261108-041415": "DE"}
SHORT = {"claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "gpt-6-luna": "luna", "gpt-6.1-terra": "terra",
         "gpt-6.1-sol": "sol", "grok-4.7": "grok", "grok-4.7-build": "grok","muse-wonder-1.0": "wonder", "muse-ember-1.0": "ember"}

allsets = json.load(open(f"{E}/analysis/allsets/allsets.json"))
runs = {}
for s in allsets:
    for r in s["runs"]:
        if r["era"] == "source.md":
            runs[r["run"]] = r["models"]

# candidate sections: line ranges -> label
def sections(pkg):
    lines = open(f"{E}/{pkg}/candidate.md").read().split("\n")
    secs = []  # (start_line_idx, label)
    for i, l in enumerate(lines):
        m = re.match(r"^## (Task (\d+)|Constraints|Phase \d+)", l)
        if m:
            secs.append((i, f"T{m.group(2)}" if m.group(2) else ("Constraints" if m.group(1) == "Constraints" else "Phase")))
        elif re.match(r"^# ", l):
            secs.append((i, "Goal"))
    return lines, secs

CAND = {p: sections(p) for p in PK}
# plan-named paths
PLAN_PATHS = {}
for p in PK:
    txt = open(f"{E}/{p}/candidate.md").read()
    toks = set(re.findall(r"`([^`\s]+)`", txt))
    paths = {t.split("::")[0].rstrip(".,;:") for t in toks if "/" in t or re.search(r"\.(py|sh|md|json|toml|yaml)$", t)}
    paths |= {x.rstrip(".,;:)") for x in re.findall(r"(?:src|tests|docs|plugins|scripts)/[\w./\-]+", txt)}
    paths = {x for x in paths if not x.startswith("./artifacts") and not x.startswith("<") and "<" not in x}
    PLAN_PATHS[p] = paths

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def locate(pkg, quote):
    if not quote:
        return None
    lines, secs = CAND[pkg]
    q = norm(quote)[:80]
    full = "\n".join(lines)
    # search line-by-line on normalized text
    for i, l in enumerate(lines):
        if q[:60] and q[:60] in norm(l):
            lab = None
            for st, lb in secs:
                if st <= i:
                    lab = lb
            return lab
    return None

def parse_findings(md):
    m = re.search(r"```findings-v1\n(.*?)```", md, re.S)
    if not m:
        return None
    out = []
    for l in m.group(1).splitlines():
        l = l.strip()
        if not l:
            continue
        try:
            out.append(json.loads(l))
        except Exception:
            out.append({"_bad": l})
    return out

def classify_path(fp, pkg):
    if not fp:
        return "none"
    if "/tmp/evalsb/cand/" in fp:
        b = os.path.basename(fp)
        if b == "candidate.md":
            return "candidate"
        if b == "source.md":
            return "source"
        return "cand-other"
    if "/.claude/" in fp:
        return "prompt"
    if "/tmp/evalsb/repo" in fp:
        return "repo"
    return "other"

def rel_repo(fp):
    return fp.split("/tmp/evalsb/repo/", 1)[1] if "/tmp/evalsb/repo/" in fp else fp

records = []
seen = set()
for run, models in sorted(runs.items()):
    for pkg, pk in PK.items():
        d = f"{E}/{pkg}/reviews/combos/{run}"
        for mf in sorted(glob.glob(f"{d}/t*.meta.json")):
            if ".attempt" in mf:
                continue
            meta = json.load(open(mf))
            rid = meta["reviewer_id"]
            md_path = f"{d}/{rid}.md"
            if not os.path.exists(md_path):
                continue
            md = open(md_path).read()
            h = hashlib.sha256(md.encode()).hexdigest()
            dup = h in seen
            seen.add(h)
            # pick attempt whose md matches final
            att = None
            for am in sorted(glob.glob(f"{d}/{rid}.attempt*.md"), key=lambda x: -int(re.search(r"attempt(\d+)", x).group(1))):
                if hashlib.sha256(open(am).read().encode()).hexdigest() == h:
                    att = int(re.search(r"attempt(\d+)", am).group(1)); break
            if att is None:
                att = meta.get("attempt")
            tj = f"{d}/{rid}.attempt{att}.json"
            model = SHORT.get(meta.get("observed_model") or meta["expected_model"], meta.get("observed_model"))
            rec = dict(run=run, pkg=pk, rid=rid, model=model, expected=SHORT.get(meta["expected_model"]),
                       model_ok=meta.get("model_ok"), attempt=att, dup=dup, wall_s=meta.get("wall_s"),
                       out_tok=meta.get("output_tokens_all"), md_match=att is not None)
            # transcript
            tools = collections.Counter(); sub_tools = 0
            reads = []; repo_files = set(); bash_cmds = []; grep_glob = []; bash_files = set()
            searched_tests = ran_pytest = ran_code = False
            num_turns = None; thinking = None
            if os.path.exists(tj):
                try:
                    arr = json.load(open(tj))
                except Exception:
                    arr = []
                for m in arr:
                    if m.get("type") == "assistant":
                        for b in m["message"].get("content", []):
                            if b.get("type") == "tool_use":
                                n = b["name"]; inp = b.get("input", {})
                                if m.get("parent_tool_use_id"):
                                    sub_tools += 1
                                tools[n] += 1
                                if n == "Read":
                                    fp = inp.get("file_path", "")
                                    reads.append(fp)
                                    if classify_path(fp, pkg) == "repo":
                                        repo_files.add(rel_repo(fp))
                                elif n == "Bash":
                                    c = inp.get("command", "")
                                    bash_cmds.append(c)
                                    for x in re.findall(r"/tmp/evalsb/repo/[\w./\-]+", c):
                                        if re.search(r"\.\w+$", x):
                                            repo_files.add(rel_repo(x)); bash_files.add(rel_repo(x))
                                    # relative paths (cwd is /tmp/evalsb/repo); file-like tokens only
                                    for x in re.findall(r"(?<![\w/.])((?:src|tests|docs|plugins|scripts)/[\w./\-]*\.(?:py|md|sh|json|toml|yaml|yml)|Makefile|CHANGELOG\.md|pyproject\.toml|\.gitignore)\b", c):
                                        repo_files.add(x); bash_files.add(x)
                                    # shell variable shortcut like S=src/...; captured above as a token
                                    if re.search(r"\b(grep|rg|find|ls)\b[^\n|;]*\btests\b", c):
                                        searched_tests = True
                                    if re.search(r"\bpytest\b", c):
                                        ran_pytest = True
                                    if re.search(r"python[^\n]*-c|uv run python|\bmake\b|ruff", c):
                                        ran_code = True
                                elif n in ("Grep", "Glob"):
                                    grep_glob.append(inp)
                    elif m.get("type") == "result":
                        num_turns = m.get("num_turns")
                        thinking = (m.get("usage", {}).get("output_tokens_details") or {}).get("thinking_tokens")
            rec["transcript"] = os.path.exists(tj)
            rec["n_tools"] = sum(tools.values())
            rec["tools"] = dict(tools)
            rec["sub_tools"] = sub_tools
            rec["num_turns"] = num_turns
            rec["thinking_tok"] = thinking
            kinds = collections.Counter(classify_path(r, pkg) for r in reads)
            rec["read_kinds"] = dict(kinds)
            rec["read_source"] = kinds.get("source", 0) > 0 or any("source.md" in c for c in bash_cmds)
            rec["read_repo_files"] = sorted(repo_files - bash_files | {rel_repo(r) for r in reads if classify_path(r, pkg) == "repo"})
            rec["searched_tests"] = searched_tests or any(f.startswith("tests/") for f in repo_files)
            rec["ran_pytest"] = ran_pytest
            rec["ran_code"] = ran_code
            rec["used_skill"] = tools.get("Skill", 0) > 0
            rec["read_candidate"] = kinds_c = any(classify_path(r, pkg) == "candidate" for r in reads) or any("candidate.md" in c and re.search(r"\b(cat|sed|head|nl|grep)\b", c) for c in bash_cmds)
            rec["repo_files"] = sorted(repo_files)
            rec["n_repo_files"] = len(repo_files)
            pp = PLAN_PATHS[pkg]
            def named(f):
                return any(f.endswith(x) or x.endswith(f) for x in pp if len(x) > 4) or any(os.path.basename(f) == os.path.basename(x) for x in pp if "/" in x)
            rec["plan_named_opened"] = sorted(f for f in repo_files if named(f))
            rec["test_opened"] = sorted(f for f in repo_files if f.startswith("tests/") or "/tests/" in f or os.path.basename(f).startswith("test_"))
            rec["code_opened"] = sorted(f for f in repo_files if re.search(r"\.(py|sh)$", f) and f not in rec["test_opened"])
            rec["plan_test_opened"] = sorted(set(rec["test_opened"]) & set(rec["plan_named_opened"]))
            rec["plan_code_opened"] = sorted(set(rec["code_opened"]) & set(rec["plan_named_opened"]))
            rec["bash_grep_repo"] = sum(1 for c in bash_cmds if re.search(r"\b(grep|rg|find|ls|sed|cat|head|nl)\b", c) and ("/tmp/evalsb/repo" in c or "cd " in c))
            rec["grep_glob_repo"] = sum(1 for g in grep_glob if "/tmp/evalsb/repo" in json.dumps(g) or not g.get("path"))
            rec["mcp_calls"] = sum(v for k, v in tools.items() if k.startswith("mcp__"))
            # report
            fs = parse_findings(md) or []
            fs = [f for f in fs if "_bad" not in f and "prior" not in f]
            rec["n_findings"] = len(fs)
            rec["n_blocking"] = sum(1 for f in fs if f.get("blocking"))
            fl = []
            for f in fs:
                refs = f.get("refs") or []
                rs = " ".join(map(str, refs))
                tasks = set(re.findall(r"\bTask\s*(\d+)", rs))
                tasks |= set(re.findall(r"\bT(\d+)\b", rs))
                secs = set()
                for q in (f.get("anchor"), f.get("anchor2")):
                    lab = locate(pkg, q or "")
                    if lab:
                        secs.add(lab)
                        if lab.startswith("T"):
                            tasks.add(lab[1:])
                if re.search(r"Constraint", rs): secs.add("Constraints")
                secs |= {f"T{t}" for t in tasks}
                ext = [r for r in refs if isinstance(r, str) and re.search(r"[\w-]+\.(py|md|sh|json|toml)|/", r) and "candidate" not in r.lower() and "source.md" not in r]
                srcref = any("source" in str(x).lower() for x in [rs, f.get("claim", "")])
                fl.append(dict(cat=f.get("category"), sev=f.get("severity"), blk=bool(f.get("blocking")),
                               tasks=sorted(tasks, key=int), secs=sorted(secs), cross_task=len(tasks) >= 2,
                               cross_sec=len(secs) >= 2, has_anchor2=bool(f.get("anchor2")), src=srcref,
                               ext=len(ext) > 0, anchor_found=locate(pkg, f.get("anchor") or "") is not None,
                               claim=f.get("claim", "")[:400], anchor=(f.get("anchor") or "")[:250],
                               anchor2=(f.get("anchor2") or "")[:250], refs=rs[:300]))
            rec["findings"] = fl
            records.append(rec)

json.dump(records, open("/tmp/pc-patterns/records.json", "w"), indent=1)
print(len(records), "records;", sum(r["dup"] for r in records), "dups;", sum(not r["md_match"] for r in records), "no md match;",
      sum(not r["transcript"] for r in records), "no transcript")
print({p: sorted(v) for p, v in PLAN_PATHS.items()})
