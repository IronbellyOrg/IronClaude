# Task 4 final static check set (does NOT import the memory code). Runs from the repo root.
import json, os, re, subprocess, sys
EVID = ".dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/03-memory-docs/"
EIGHT = ["docs/user-guide/memory-system.md", "docs/memory/README.md", "docs/memory/reflexion.jsonl.example", "docs/mcp/mcp-integration-policy.md",
         "docs/reference/pm-agent-autonomous-reflection.md", "docs/memory/pm_context.md", "docs/memory/token_efficiency_validation.md", "docs/memory/WORKFLOW_METRICS_SCHEMA.md"]
MD = [p for p in EIGHT if p.endswith(".md")]
fails = []
def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)
def run(*a): return subprocess.run(a, capture_output=True, text=True)
txt = {p: open(p).read() for p in EIGHT}
allmd = "\n".join(txt[p] for p in MD)

# 1. earlier static checks still pass on the final text (sample parse + Task 3 claims)
for s in ("t2-sample-check.py", "t3-static-check.py"):
    r = run("python3", EVID + s); check(r.returncode == 0 and "ALL PASS" in r.stdout, f"{s} still passes on the final files ({r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[:80]})")

# 2. synthetic JSONL parses
rows = [json.loads(l) for l in txt["docs/memory/reflexion.jsonl.example"].splitlines()]
check(len(rows) == 6 and all(r.get("synthetic") is True and r["solution"] for r in rows), "reflexion.jsonl.example: six synthetic rows parse and carry solutions")

# 3. links and intended live source paths across the eight-file chain
SRC = ["src/superclaude/pm_agent/reflexion.py", "src/superclaude/pytest_plugin.py", "tests/conftest.py", "tests/unit/test_reflexion.py",
       "tests/unit/test_reflexion_pollution_guard.py", "src/superclaude/agents/pm-agent.md", "src/superclaude/__init__.py", "src/superclaude/pm_agent/__init__.py"]
for p in SRC: check(os.path.exists(p), f"intended live source exists: {p}")
for path in MD:
    base = os.path.dirname(path)
    for n, line in enumerate(txt[path].splitlines(), 1):
        refs = set(re.findall(r"`([^`\s]+\.md)`", line)) | set(re.findall(r"(?<![\w/.-])(docs/[\w./-]+\.md)", line)) \
             | {os.path.normpath(os.path.join(base, t)) for t in re.findall(r"\]\(([^)#\s]+\.md)", line) if not t.startswith("http")}
        for r in refs:
            if r.startswith("~") or r.startswith("/") or "<" in r: continue
            exists = os.path.exists(r) or os.path.exists(os.path.join(base, r))
            hist = bool(re.search(r"(?i)historical|no longer|earlier version|original text|refer to an earlier", line))
            check(exists or hist, f"{path}:{n} {r} {'exists' if exists else 'marked historical'}")

# 4. corrected key claims present (class/path/schema/matching/order/activation/privacy/backend)
CLAIMS = {"docs/user-guide/memory-system.md": ["REFLEXION_OUTPUT_DIR", "0.7", "first matching row", "stub", "does **not** remove", "synthetic"],
          "docs/memory/README.md": ["solutions_learned.jsonl", "0.7", "first matching row", "stub", "does **not** filter or redact", "Callers must redact"],
          "docs/mcp/mcp-integration-policy.md": ["ReflexionPattern", "UNVERIFIED", "superseded", "first match in file order"],
          "docs/reference/pm-agent-autonomous-reflection.md": ["ReflexionPattern", "NOT implemented", "Nothing is redacted", "UNVERIFIED"],
          "docs/memory/pm_context.md": ["historical design notes", "unmeasured", "Superseded", "explicit Python API"],
          "docs/memory/token_efficiency_validation.md": ["historical record", "superseded", "never measured", "explicit API"],
          "docs/memory/WORKFLOW_METRICS_SCHEMA.md": ["documented", "error_search_tool", "not automatically emitted", "separate data flow"]}
for p, ss in CLAIMS.items():
    for s in ss: check(s.lower() in txt[p].lower(), f"{p} states '{s}'")

# 5. retired active instructions absent across all eight files
RETIRED = ["ReflexionMemory (Built-in, Always Available)", "superclaude/core/pm_init/reflexion_memory.py`", "Auto-Managed: true (internal", "Mindbase MCP (automatic)",
           "Mindbase: Automatic save", "Mindbase auto-load (automatic)", "Search: Keyword-based (50% overlap", "Return entries with >50% overlap", "Sort by timestamp (most recent first)",
           "rm docs/memory/reflexion.jsonl", "jq -s 'unique_by(.mistake)'", "tail -100 docs/memory/reflexion.jsonl", "Copy this to `reflexion.jsonl`", "docs/memory/reflexion.jsonl (ReflexionMemory",
           "Built-in ReflexionMemory (Always Available)", "SuperClaude provides significant token savings with built-in ReflexionMemory", "\"mindbase_used\": false,\n  \"sub_agents\""]
LABEL = re.compile(r"(?i)superseded|historical|former|earlier|original")
def active_hits(s):  # lines containing s that are NOT labelled as superseded/historical
    return [(p, n) for p, t in txt.items() for n, l in enumerate(t.splitlines(), 1) if s in l and not LABEL.search(l)]
for s in RETIRED:
    if "\n" in s: check(all(s not in t for t in txt.values()), f"no retired active text {s[:40]!r}"); continue
    check(not active_hits(s), f"no unlabelled retired text '{s[:60]}'")
for p in EIGHT:
    check("reflexion.jsonl" not in re.sub(r"reflexion\.jsonl\.example|`reflexion\.jsonl`[^\n]*(superseded|earlier|original|old)[^\n]*", "", txt[p]) or "superseded" in txt[p],
          f"{p}: bare 'reflexion.jsonl' only appears inside superseded/historical text")
check(not re.search(r"(?i)\bstatus\b.{0,30}(affects|determines|decides) (whether|matching)", re.sub(r"(?i)no other field[^.]*\.", "", allmd)), "no claim that status affects matching (negations stripped)")
check(not re.search(r"(?i)auto(matically)? (loads?|loaded|saves?) .{0,40}(solutions_learned|mindbase)", re.sub(r"(?i)(no|not|never|nothing)[^.\n]*", "", allmd)), "no active automatic-load/save claim for memory")

# 6. workflow metrics: example and table agree on error_search_tool; separate from error learning; data untouched
sch = txt["docs/memory/WORKFLOW_METRICS_SCHEMA.md"]
ex = re.search(r"```jsonl\n(\{.*?\})\n```", sch, re.S).group(1)
rec = json.loads(ex)
check(rec.get("error_search_tool") == "none" and "mindbase_used" not in rec, "metrics example record uses error_search_tool: none and not mindbase_used")
row = [l for l in sch.splitlines() if l.startswith("| `error_search_tool`")][0]
check("Documented optional metric" in row and "not automatically emitted" in row and '"none"' in row and '"local_file"' in row and "mindbase_search" not in row and "ReflexionMemory" not in row, "metrics table row labels error_search_tool a documented optional metric with accurate local/none examples")
mb = [l for l in sch.splitlines() if "mindbase_used" in l]
check(len(mb) == 1 and "deliberately left unchanged" in mb[0], "mindbase_used appears on one line only: the note that the old data is left unchanged")
check("optional" in sch.split("### Optional Fields")[1].split("## Task Type")[0].lower() and "error_search_tool" not in sch.split("### Required Fields")[1].split("### Optional Fields")[0], "error_search_tool is in the Optional Fields table, not Required")

# 6b. no active "auto-generated / automatically recorded" claim for the two files nothing writes
rd = txt["docs/memory/README.md"]
check(not re.search(r"(?i)(workflow_metrics|patterns_learned)\.jsonl\s*\(Auto-generated\)", rd), "README: no '(Auto-generated)' heading for workflow_metrics/patterns_learned")
check("Generated by**: PM Agent" not in rd and "automatically created and managed" not in rd and "the system handles it" not in rd, "README: retired 'generated by PM Agent' / 'automatically created and managed' wording is gone")
check("nothing writes it" in rd and rd.lower().count("no tracked code") >= 3, "README: states no tracked code writes workflow_metrics.jsonl / patterns_learned.jsonl")
check("0.5-1 KB per entry" not in re.sub(r"Earlier text quoted[^\n]*", "", rd), "README: file-size figures only appear as unverified earlier estimates")
rr = txt["docs/reference/pm-agent-autonomous-reflection.md"]
check("Automatic best practice adoption" not in rr.replace("no automatic adoption exists", ""), "reflection reference: no 'Automatic best practice adoption' claim")
check("nothing in this repository writes the file" in rr and "no tracked code writes this file" in rr, "reflection reference: workflow metrics labelled documented design, not written by tracked code")
check("industry benchmark achieved" not in rr and "design target taken from an industry benchmark" in rr, "reflection reference: no 'benchmark achieved' claim")
check("Design sketch only: nothing in this repository writes `workflow_metrics.jsonl`" in rr and "the metrics file has no such field" in rr, "reflection reference: Monitoring block labelled design sketch, separate from error learning")
check("docs/pdca/` - PDCA cycle documentation per feature (historical" in txt["docs/memory/pm_context.md"], "pm_context: docs/pdca line marked historical")
# 6c. final-review pass: stale pm.md claims (B1), unlabelled figures (B2), minor wording
pmlen = len(open("plugins/superclaude/commands/pm.md").read().splitlines())
check(pmlen < 870 and not re.search(r"(?i)confidence|hallucination|self-check", open("plugins/superclaude/commands/pm.md").read()), f"pm.md is {pmlen} lines with no confidence/self-check text (so its old line refs are stale)")
check("**Status**: Production Ready" not in rr and "**Status**: Historical design document" in rr, "reflection reference: status is historical, not 'Production Ready'")
for ln in [l for l in rr.splitlines() if "Line 870-1016" in l]:
    check("historical" in ln.lower() or "earlier version" in ln, f"reflection reference: stale pm.md range marked: {ln.strip()[:60]}")
check("Historical: these line ranges refer to an earlier pm.md" in rr and "not re-verified" in rr.split("Implementation (")[1][:80], "reflection reference: Integration Points block marked historical")
check("(Complete ✅)" not in rr and "marked complete on 2025-10-17; not re-verified" in rr, "reflection reference: Phase 1 'Complete' marked as unverified claim")
exp = rr.split("## 📈 Expected Results")[1].split("## 🎓")[0]
check("None was measured in this repository" in exp and "Total Expected Savings (design targets, NOT measured)" in exp and "Confidence Accuracy (targets, NOT measured)" in exp, "reflection reference: Expected Results section and blocks labelled unmeasured")
for frag in ["Savings: 93% (2,150 tokens", "ROI: 25-250x", "Savings: 80-95% on reflection cost", "Savings: 80-98% token reduction", "(60-95% potential savings", "94% hallucination detection rate", "(94% detection rate", "= 46% savings", "Tokens Saved: 15-30K"]:
    ln = [l for l in rr.splitlines() if frag in l]
    check(ln and all(re.search(r"(?i)not measured|estimate|illustrative|quoted from", l) for l in ln), f"reflection reference: figure labelled unmeasured: {frag}")
check("Validation Metrics (targets; no measurement exists" in rr, "reflection reference: validation metrics labelled targets")
rd = txt["docs/memory/README.md"] = open("docs/memory/README.md").read()
check("**Workflow Metrics** - documented design" in rd and "**Pattern Learning** - legacy pattern records" in rd and "Historical 2025-10-17 design notes" in rd, "README: overview and pm_context description qualified")
pc = open("docs/memory/pm_context.md").read()
check("(design intent; no tracked code writes the file)" in pc and "None currently." not in pc, "pm_context: A/B pattern and Known Issues qualified")
sch2 = open("docs/memory/WORKFLOW_METRICS_SCHEMA.md").read()
check("-delete" not in sch2 and "mv docs/memory/workflow_metrics.jsonl" not in sch2 and "touch docs/memory/workflow_metrics.jsonl" not in sch2, "metrics schema: no move/touch/delete recipes against the real data file")
check("Design intent from 2025-10-17. No tracked code runs this A/B testing" in open("docs/memory/token_efficiency_validation.md").read(), "validation note: optimization framework labelled design intent")
w = run("grep", "-rlE", "workflow_metrics|patterns_learned", "src", "plugins", "tests").stdout.split()
check(not [p for p in w if "docs" not in p and "/test" not in p], f"no tracked src/plugins writer mentions the two files (hits: {w})")

# 7. exact eight-file product scope
changed = sorted(l for l in run("git", "diff", "--name-only", "HEAD", "--", ".", ":(exclude).dev").stdout.split() if l)
check(changed == sorted(EIGHT), f"changed product files == the eight allowed files ({len(changed)} changed)")
untracked = [l for l in run("git", "ls-files", "--others", "--exclude-standard").stdout.split() if not l.startswith(".dev/")]
check(not untracked, "no untracked files outside .dev/")
staged_non_task = [l for l in run("git", "diff", "--cached", "--name-only").stdout.split() if not l.startswith(".dev/tasks/")]
check(not staged_non_task, "nothing staged outside .dev/tasks/")

# 8. protected hashes + data
base = [l for l in open(EVID + "baseline-hashes.txt").read().splitlines() if l.split("  ", 1)[1] not in EIGHT]
open("/tmp/t4_protected.txt", "w").write("\n".join(base) + "\n")
r = run("sha256sum", "-c", "--quiet", "/tmp/t4_protected.txt"); check(r.returncode == 0, f"all {len(base)} protected baseline files unchanged (code, tests, guards, memory data, mistakes)")
for f in ("solutions_learned", "workflow_metrics", "patterns_learned"):
    a = [l.split()[0] for l in open(EVID + "baseline-hashes.txt") if l.strip().endswith(f"docs/memory/{f}.jsonl")][0]
    b = run("sha256sum", f"docs/memory/{f}.jsonl").stdout.split()[0]; check(a == b, f"docs/memory/{f}.jsonl byte-identical to baseline")
check(not os.path.exists("docs/mistakes"), "docs/mistakes/ was not created")
print("RESULT:", "FAIL" if fails else "ALL PASS", f"({len(fails)} failures)")
sys.exit(1 if fails else 0)
