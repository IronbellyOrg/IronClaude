# Task 3 static check. Reads the two Task 3 docs, the sample file and HEAD copies; does NOT import the memory code.
import json, re, subprocess, sys, os
POLICY = "docs/mcp/mcp-integration-policy.md"
REFL = "docs/reference/pm-agent-autonomous-reflection.md"
fails = []
def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)
def head(p): return subprocess.run(["git", "show", f"HEAD:{p}"], capture_output=True, text=True, check=True).stdout
pol, refl = open(POLICY).read(), open(REFL).read()
row1 = json.loads(open("docs/memory/reflexion.jsonl.example").readline())

# 1. retired claims must not appear as current text
POL_FORBIDDEN = ["Auto-Managed: true (internal", "PM Agent Role: Automatically used on errors", "Storage: docs/memory/reflexion.jsonl (local file)",
    "Search: Keyword-based (50% overlap threshold)", "Primary: Mindbase MCP (automatic)", "Secondary: None (fully automated)", "Mindbase auto-load (automatic)",
    "Mindbase: Automatic save", "Mindbase: Automatic (no explicit call)", "Memory: Mindbase (automatic)", "Falls back to ReflexionMemory",
    "Automatically selected by Claude when available", "SuperClaude works fully with ReflexionMemory alone",
    "❌ Mindbaseを明示的に操作", "❌ write_memory() / read_memory() 使用", "❌ docs/memory/ ディレクトリ作成", "Reason: Mindbaseと重複"]
for s in POL_FORBIDDEN: check(s not in pol, f"policy has no current-text '{s}'")
REFL_FORBIDDEN = ["docs/memory/reflexion.jsonl (ReflexionMemory", '{"error":"...","solution":"...","date":"..."}', "mindbase_search (if airis-mcp-gateway installed)",
    "Claude automatically selects best available tool", "Store in ReflexionMemory for future sessions", "(ReflexionMemory - ALWAYS)", "(if airis-mcp-gateway installed, automatic storage)",
    "Applying solution now", "30 seconds (vs 30 minutes", "Smart lookup: mindbase OR grep", "Apply solution immediately", "Cache lookup", "同じエラーは**2回目から即座に解決**", "過去の失敗から自動学習"]
for s in REFL_FORBIDDEN: check(s not in refl, f"reflection ref has no current-text '{s}'")
# old instructions that survive must be labelled superseded/historical on the same or neighbouring line
for s in ["Remove docs/memory/ references", "Remove write_memory() / read_memory() calls"]:
    check(all("(superseded)" in l for l in pol.splitlines() if s in l) and s in pol, f"policy migration item '{s}' is labelled (superseded)")

# 2. corrected contract present
for s in ["ReflexionPattern", "src/superclaude/pm_agent/reflexion.py", "solutions_learned.jsonl", "0.7", "first", "UNVERIFIED", "stub", "explicit", "memory_dir argument > non-empty REFLEXION_OUTPUT_DIR > docs/memory/"]:
    check(s in pol, f"policy states '{s}'")
for s in ["ReflexionPattern", "solutions_learned.jsonl", "0.7", "first stored row", "NOT implemented", "stub", "UNVERIFIED", "@pytest.mark.reflexion", "does not call", "Nothing is redacted", "docs/memory/reflexion.jsonl.example"]:
    check(s in refl, f"reflection ref states '{s}'")
# record fields line agrees with sample row 1
fields = [k for k in row1 if k != "synthetic"]
check(all(k in refl.split("Record fields")[1].split("Marked pytest capture")[0] for k in fields), "reflection ref 'Record fields' lists every sample-row field: " + ", ".join(fields))
check(all(k in re.search(r'Format: (\{"error_type".*?\})', refl).group(1) for k in ["error_type", "error_message", "test_name", "solution", "root_cause", "prevention", "timestamp"]), "reflection ref storage format line uses the live field names")
# example 4 agrees with sample row 1 and the 0.90 pair
ex4 = refl.split("### Example 4")[1].split("---")[0]
check(all(row1[k] in ex4 for k in ["solution", "root_cause", "prevention", "timestamp"]), "Example 4 returns sample row 1 solution/root_cause/prevention/timestamp")
check("9 of 10" in ex4 and "0.90" in ex4 and "invalid port value 9090 in config file" in ex4, "Example 4 uses the documented 9/10 = 0.90 pair")
def sig(e):
    p = []
    if "error_type" in e: p.append(e["error_type"])
    if "error_message" in e: p.append(re.sub(r"\d+", "N", e["error_message"])[:100])
    if "test_name" in e: p.append(e["test_name"])
    return " | ".join(p)
a = set(sig({"error_type": "ValueError", "error_message": "invalid port value 9090 in config file", "test_name": "test_load_config"}).lower().split())
b = set(sig(row1).lower().split())
check((len(a & b), len(a | b)) == (9, 10), f"Example 4 pair recomputed from sample row 1: {len(a&b)}/{len(a|b)}")
check("No time or token savings are claimed" in ex4, "Example 4 claims no time/token savings")

# 3. unmeasured promises are labelled
for s in ["unmeasured", "NOT measured", "UNVERIFIED", "target"]:
    check(s in refl, f"reflection ref labels figures with '{s}'")
for line in refl.splitlines():
    if re.search(r"<10%|75% reduction|100% on repeated", line):
        check(bool(re.search(r"(?i)unverified|target|estimate|earlier versions|derived|unmeasured|no measurement|not measured", line)) or "Error Recurrence (historical" in refl,
              f"recurrence/savings figure line is qualified: {line.strip()[:70]}")

# 4. unrelated sections unchanged: marker counts equal HEAD
UNREL_POL = ["Manual Override: --serena flag", "Manual Override: --c7 flag", "Manual Override: --tavily flag", "Serenaをタスク管理に使用", "Context7をプロジェクトドキュメントに使用", "Auto-Trigger Keywords", "## MCP Selection Matrix", "Complex (>10 files, architectural changes)", "#### Serena MCP", "Tavily"]
UNREL_REFL = ["Layer 1: Confidence Check", "Layer 2", "Layer 4: Token-Budget-Aware Reflection", "Example 1", "Example 2", "Example 3", "Hallucination Detection", "Budget: 2,500 tokens", "Phase 0 (Bootstrap)"]
for path, marks in ((POLICY, UNREL_POL), (REFL, UNREL_REFL)):
    old, new = head(path), open(path).read()
    for m in marks: check(old.count(m) == new.count(m), f"{path}: unrelated marker count unchanged ({m!r} x{old.count(m)})")

# 5. links: affected (memory/reflexion) ones resolve or are marked historical on the same line
OUT_OF_SCOPE = set()  # attempt 2: the token-efficiency link sits in an edited sentence, so it is checked too
for path in (POLICY, REFL):
    base = os.path.dirname(path)
    for n, line in enumerate(open(path).read().splitlines(), 1):
        refs = set(re.findall(r"`([^`\s]+\.md)`", line)) | set(re.findall(r"(?<![\w/.-])(docs/[\w./-]+\.md)", line)) | {os.path.normpath(os.path.join(base, t)) for t in re.findall(r"\]\(([^)#\s]+\.md)", line) if not t.startswith("http")}
        for r in refs:
            if r.startswith("~") or r in OUT_OF_SCOPE: continue
            ok = os.path.exists(r) or "historical" in line
            check(ok, f"{path}:{n} link/path {r} {'exists' if os.path.exists(r) else 'is marked historical'}")
print("RESULT:", "FAIL" if fails else "ALL PASS", f"({len(fails)} failures)")
sys.exit(1 if fails else 0)
