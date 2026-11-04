# Wave 1A grounding hunks (read-only, captured 2026-11-03T05:53:40Z)

## H1 src/superclaude/cli/install_core.py:10-27
```
    10	from typing import List, Tuple
    11	
    12	# Core files this version ships; list_installed_core_files reports only these.
    13	KNOWN_CORE_FILES = frozenset(
    14	    {
    15	        "BASH_INSPECTION_POLICY.md",
    16	        "BUSINESS_PANEL_EXAMPLES.md",
    17	        "BUSINESS_SYMBOLS.md",
    18	        "CLAUDE.md",
    19	        "CODEGRAPH.md",
    20	        "HOW-WE-WORK.md",
    21	        "ISSUE-BACKLOG.md",
    22	        "ISSUE-HANDOFF.md",
    23	        "PRINCIPLES.md",
    24	        "RESEARCH_CONFIG.md",
    25	        "RULES.md",
    26	    }
    27	)
```
## H2 src/superclaude/cli/install_core.py:150-156
```
   150	    claude_dir = Path.home() / ".claude"
   151	
   152	    if not claude_dir.exists():
   153	        return []
   154	
   155	    return sorted(f.name for f in claude_dir.glob("*.md") if f.name in KNOWN_CORE_FILES)
```
## H3 tests/cli/test_how_we_work_install.py (lines mentioning KNOWN_CORE_FILES)
```
42-
43-def test_known_core_set_matches_shipped():
44:    assert install_core.KNOWN_CORE_FILES == frozenset(install_core.list_core_files())
45-
46-
47-def _seed(path: Path, data: bytes) -> bytes:
48-    path.parent.mkdir(parents=True, exist_ok=True)
```
## H4 scripts/build_superclaude_plugin.py (core-related lines)
```
```
## H5 plugins/superclaude/core listing
```
BUSINESS_PANEL_EXAMPLES.md
BUSINESS_SYMBOLS.md
CODEGRAPH.md
PRINCIPLES.md
RESEARCH_CONFIG.md
RULES.md
__init__.py
```
## H6 Makefile verify-sync target
```
166:verify-sync:
167-	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
168-	@drift=0; \
169-	echo ""; \
170-	echo "=== Skills ==="; \
171-	for skill_dir in src/superclaude/skills/*/; do \
172-		name=$$(basename "$$skill_dir"); \
173-		case "$$name" in __*) continue;; esac; \
174-		if [ ! -d ".claude/skills/$$name" ]; then \
175-			echo "  ❌ MISSING in .claude/skills/: $$name"; \
176-			drift=1; \
177-		else \
178-			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
```
## H7 tests/core/test_claude_md_routing_block.py (asserts)
```
1:"""The always-loaded core/CLAUDE.md carries a copy of the guide's level table.
16:_CLAUDE = _CORE / "CLAUDE.md"
17:_GUIDE = _CORE / "HOW-WE-WORK.md"
28:def test_level_table_copy_matches_guide():
30:        "core/CLAUDE.md level table differs from HOW-WE-WORK.md; "
35:def test_routing_block_rule_and_pointer():
42:    assert "`~/.claude/HOW-WE-WORK.md`" in text
48:    assert "`~/.claude/HOW-WE-WORK.md`" in tail
51:    assert not re.search(r"^\s*@\S*HOW-WE-WORK", text, re.M)
54:def test_imports_resolve_to_shipped_core_files():
61:def test_removed_sections_stay_removed():
79:def test_mcp_flag_column_is_advisory():
84:def test_always_loaded_policy_keeps_workflow_default_and_mdtm_boundary():
```
## H8 '## Unattended mode' in src/superclaude/commands (expect none)
```
(no matches)
```
## H9 git/gh write-verb hit counts under src/superclaude/{skills,commands,agents}
```
git add: 21
git commit: 6
git push: 2
git merge: 8
git worktree add: 3
git worktree remove: 1
git stash: 4
git update-ref: 6
gh pr: 40
gh api: 30
```
## H10 ~/.claude/skills/sc-implement-protocol/refs/qa.md:286-289 and SKILL.md:79,97
```
7. `E-ARCHIVE-BLOCKED` (managed): FINAL `issues` naming a blocking defect at the end state (see "FINAL derived test" below), `--skip-final-review` on a managed package, or a helper refusal. Kept because FINAL is never waived.

No other path may stop automation or prompt the user. Every halt message and Ruling request lists blocking findings only. A minors-only replay writes no `halt` and no `Ruling:` line.

Ignore MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) except `independent`. Phase-N tasklists are accepted as markdown. MDTM-shaped files still use **this** protocol. Do not auto-handoff.
Default sequential in source order. Parallel only when the source marks a set independent (literal `independent`, `parallel-ok`, or heading `Independent`) **and** set size ≤ 3. Unmarked = sequential. If overlap is obvious (`same file`), stay sequential. (a) A batch is formed only from tasks that h
```
## H11 baseline test dirs present
```
tests/cli
tests/commands
tests/core
tests/recommend
tests/skills
```
## H12 Orca install path for AC-0.7
```
/opt/Orca/resources/app.asar.unpacked/out
```
