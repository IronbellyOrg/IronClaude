51b1cdadf233041e33dabff1e2ca0dd7c955a03e
Review one task for spec compliance.

Task brief: T1 (AC ids in order of the "Acceptance criteria:" bullets: T1.AC1,T1.AC2,T1.AC3). Plan file: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/TASK-WF-devGuideFenceFix-20261104-204854.md, lines 28-35:
## Task 1: Save the baseline and fix the 2.1 Quick Start command template fence

Before any edit, copy `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` byte for byte to `./artifacts/guide-before.md`, copy `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py` to `./artifacts/fence-check.py`, and save `uv run python -I ./artifacts/fence-check.py docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` output as `./artifacts/fence-before.txt`. Then, in section 2.1 "Create a Minimal Command", read the `/sc:hello` command template and change its outer opening fence (guide line 136 today, ```` ```markdown ````) to four backticks plus `markdown` and its outer closing fence (guide line 177 today, the bare fence just before `### 2.2 Create a Minimal Agent`) to four backticks. If either line number has moved, locate the pair by the template and record the actual lines in `./artifacts/t1-notes.txt`.

Acceptance criteria:
- `./artifacts/guide-before.md` is byte-identical to the guide as it was before this task's edit (`cmp` against the task's start snapshot of the guide passes), and `./artifacts/fence-before.txt` lists the 2.1 spot (outer fence opened at line 136).
- The guide's 2.1 command template opens with ````` ````markdown ````` and closes with ````` ```` `````; running the script on the edited guide shows `### 2.2 Create a Minimal Agent` outside any fence and no spot whose outer fence opened at line 136 or 177; that output is saved as `./artifacts/fence-t1.txt`.
- `diff ./artifacts/guide-before.md docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` shows exactly two changed lines, the two fence lines, saved as `./artifacts/t1-diff.txt`.

Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/TASK-WF-devGuideFenceFix-20261104-204854.md lines 17-24)
## Constraints

- Only `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` changes, and only on the twelve outer-fence lines the source lists (the opening and closing line of each of the six templates). No prose line, inner code block or other fence changes. Scripts and evidence go under this package's `./artifacts/`.
- Each opening line becomes four backticks followed by `markdown`; each closing line becomes four backticks and nothing else.
- The archived script `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py` is copied, never edited; the copy lives at `./artifacts/fence-check.py` and runs with `uv run python -I`.
- The earlier guide refactor is still uncommitted, so "the guide before this plan" means the copy `./artifacts/guide-before.md` saved before the first edit, not `HEAD`.
- No em dash and no en dash in changed lines.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.

Start sha: 51b1cdadf233041e33dabff1e2ca0dd7c955a03e
Diff against the start snapshot: (git diff 51b1cdadf233041e33dabff1e2ca0dd7c955a03e -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index ea89d489..18769966 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -133,7 +133,7 @@ When Claude Code starts a session, it loads context in this priority order:
 
 Create a file at `src/superclaude/commands/hello.md`:
 
-```markdown
+````markdown
 ---
 name: hello
 description: "A minimal example command"
@@ -174,7 +174,7 @@ personas: []
 **Will Not:**
 - Execute any code or modify files
 - Access external services
-```
+````
 
 ### 2.2 Create a Minimal Agent
 

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/t1-baseline-cmp.txt ===
$ git show 51b1cdadf233041e33dabff1e2ca0dd7c955a03e:docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md | cmp - ./artifacts/guide-before.md
rc=0
$ cmp .dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py ./artifacts/fence-check.py
rc=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/fence-before.txt ===
# Fence state of docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
## Headings
L9: ## Table of Contents  [outside]
L25: ## 1. Introduction  [outside]
L27: ### What SuperClaude Is  [outside]
L39: ### The Three-Tier Architecture  [outside]
L61: ### The Activation Pattern  [outside]
L66: ## Activation  [inside fence opened at line 65 (```markdown)]
L77: ### Installation Locations  [outside]
L98: ### Path rules for primitives  [outside]
L117: ### Context Loading Sequence  [outside]
L130: ## 2. Quick Start  [outside]
L132: ### 2.1 Create a Minimal Command  [outside]
L146: # /sc:hello - Hello World Command  [inside fence opened at line 136 (```markdown)]
L148: ## Triggers  [inside fence opened at line 136 (```markdown)]
L152: ## Usage  [inside fence opened at line 136 (```markdown)]
L158: ## Behavioral Flow  [outside]
L162: ## Examples  [outside]
L169: ## Boundaries  [outside]
L179: ### 2.2 Create a Minimal Agent  [inside fence opened at line 177 (```)]
L190: # Greeter Agent  [inside fence opened at line 177 (```)]
L192: ## Triggers  [inside fence opened at line 177 (```)]
L196: ## Behavioral Mindset  [inside fence opened at line 177 (```)]
L200: ## Tools  [inside fence opened at line 177 (```)]
L204: ## Outputs  [inside fence opened at line 177 (```)]
L208: ## Boundaries  [inside fence opened at line 177 (```)]
L218: ### 2.3 Create a Minimal Skill  [outside]
L229: # Hello Skill  [inside fence opened at line 222 (```markdown)]
L231: ## Purpose  [inside fence opened at line 222 (```markdown)]
L234: ## Protocol  [inside fence opened at line 222 (```markdown)]
L240: ## Will Do  [inside fence opened at line 222 (```markdown)]
L244: ## Will Not Do  [inside fence opened at line 222 (```markdown)]
L249: ### 2.4 Sync and Test  [outside]
L252: # Copy new components from src/ to .claude/  [inside fence opened at line 251 (```bash)]
L255: # Verify sync succeeded  [inside fence opened at line 251 (```bash)]
L258: # Test the command in Claude Code  [inside fence opened at line 251 (```bash)]
L259: # Type: /sc:hello  [inside fence opened at line 251 (```bash)]
L264: ## 3. Commands Deep Dive  [outside]
L266: ### 3.1 Anatomy of a Command File  [outside]
L310: ### 3.2 Command Archetypes  [outside]
L314: #### Archetype 1: Analysis Pipeline  [outside]
L329: #### Archetype 2: Meta-Orchestrator  [outside]
L340: ## CRITICAL BOUNDARIES  [inside fence opened at line 339 (```)]
L346: #### Archetype 3: Unified Executor  [outside]
L363: ### 3.3 Command Processing Pipeline  [outside]
L375: ### 3.4 Performance Profiles  [outside]
L385: ### 3.5 Wave-Enabled Commands  [outside]
L389: ### 3.6 Registering a New Command  [outside]
L397: ## 4. Agents Deep Dive  [outside]
L399: ### 4.1 Anatomy of an Agent File  [outside]
L437: ### 4.2 Agent Patterns  [outside]
L443: #### Pattern 1: Constrained Worker  [outside]
L451: #### Pattern 2: Specialist Investigator  [outside]
L459: #### Pattern 3: Process Orchestrator  [outside]
L469: #### Pattern 4: Meta-Layer Agent  [outside]
L483: ### 4.3 Agent Spec Format (Dynamic Instantiation)  [outside]
L502: ### 4.4 Agent Activation Methods  [outside]
L514: ## 5. Skills Deep Dive  [outside]
L516: ### 5.1 Anatomy of a Skill  [outside]
L531: ### 5.2 SKILL.md Frontmatter  [outside]
L571: ### 5.3 Extended Metadata Comment  [outside]
L586: ### 5.4 Tool Allowlisting  [outside]
L602: ### 5.5 Skill Complexity Tiers  [outside]
L606: #### Tier 1: Simple (SKILL.md only)  [outside]
L626: #### Tier 2: Medium (SKILL.md + allowed-tools + compliance logic)  [outside]
L648: #### Tier 3: Complex (SKILL.md + refs/ + agents + multi-phase)  [outside]
L673: ### 5.6 The refs/ Pattern (Lazy Loading)  [outside]
L685: ## Wave 2: Analysis  [inside fence opened at line 684 (```markdown)]
L698: ### 5.7 The sc- Prefix Convention  [outside]
L710: ### 5.8 Machine-Readable Headers  [outside]
L726: ### 5.9 Input and Output Contracts  [outside]
L728: #### Input Contracts  [outside]
L733: ## Required Input (STOP if missing)  [inside fence opened at line 732 (```markdown)]
L735: ### Mode A: Compare existing artifacts  [inside fence opened at line 732 (```markdown)]
L738: ### Mode B: Generate variants from source  [inside fence opened at line 732 (```markdown)]
L747: #### Output / Return Contracts  [outside]
L752: ## Return Contract  [inside fence opened at line 751 (```markdown)]
L765: #### Worker contract (under `--unattended`)  [outside]
L774: ### 5.10 Skill-Authoring Checklist  [outside]
L802: ## 6. Multi-Phase Architecture  [outside]
L804: ### 6.1 Wave System  [outside]
L836: ### 6.2 Compliance Tiers  [outside]
L866: ### 6.3 Delegation Intelligence  [outside]
L888: ### 6.4 Resource Management Zones  [outside]
L902: ## 7. Integration Patterns  [outside]
L904: ### 7.1 Command + Skill + Agent Composition  [outside]
L930: ### 7.2 MCP Server Integration  [outside]
L950: ### 7.3 Persona Integration  [outside]
L975: ### 7.4 Thinking Depth Flags  [outside]
L985: ### 7.5 Dynamic Context Injection  [outside]
L990: ## Repository Context  [inside fence opened at line 989 (```markdown)]
L998: ### 7.6 Orca Orchestration: Commands as Workers  [outside]
L1002: #### How the pieces fit  [outside]
L1009: #### Rollout state  [outside]
L1015: #### Deciding whether a new command can be a worker  [outside]
L1022: #### What a command does under `--unattended`  [outside]
L1037: #### The worker session, not the command (WC-7)  [outside]
L1041: #### The `## Unattended mode` section of a converted command  [outside]
L1047: #### Skills and agents under a command  [outside]
L1056: ## 8. Development Workflow  [outside]
L1058: ### 8.1 Source of Truth  [outside]
L1071: ### 8.2 Sync Workflow  [outside]
L1076: # 1. Make your changes in src/superclaude/  [inside fence opened at line 1075 (```bash)]
L1077: # 2. Sync to .claude/  [inside fence opened at line 1075 (```bash)]
L1080: # 3. Verify sync succeeded  [inside fence opened at line 1075 (```bash)]
L1087: # 1. Copy changes back to src/superclaude/ manually  [inside fence opened at line 1086 (```bash)]
L1088: # 2. Verify both sides match  [inside fence opened at line 1086 (```bash)]
L1094: ### 8.3 Creating a New Component: Full Workflow  [outside]
L1097: # 1. Scaffold the component  [inside fence opened at line 1096 (```bash)]
L1098: #    Command:  [inside fence opened at line 1096 (```bash)]
L1101: #    Agent:  [inside fence opened at line 1096 (```bash)]
L1104: #    Skill (simple):  [inside fence opened at line 1096 (```bash)]
L1108: #    Skill (complex with refs):  [inside fence opened at line 1096 (```bash)]
L1113: # 2. Write the component (see templates in Section 10)  [inside fence opened at line 1096 (```bash)]
L1115: # 2a. Decide worker eligibility (WC-2, section 7.6)  [inside fence opened at line 1096 (```bash)]
L1116: #    If the command will accept --unattended, write its ## Unattended mode section  [inside fence opened at line 1096 (```bash)]
L1117: #    and add its name to UNATTENDED_COMMANDS in tests/skills/test_worker_contract.py  [inside fence opened at line 1096 (```bash)]
L1119: # 3. Sync to .claude/ for testing  [inside fence opened at line 1096 (```bash)]
L1122: # 4. Verify sync  [inside fence opened at line 1096 (```bash)]
L1125: # 5. Test in Claude Code  [inside fence opened at line 1096 (```bash)]
L1126: #    - Invoke the command/agent/skill  [inside fence opened at line 1096 (```bash)]
L1127: #    - Verify triggers activate correctly  [inside fence opened at line 1096 (```bash)]
L1128: #    - Validate output matches expected behavior  [inside fence opened at line 1096 (```bash)]
L1129: #    - Test edge cases and error conditions  [inside fence opened at line 1096 (```bash)]
L1131: # 6. Register the component (commands only)  [inside fence opened at line 1096 (```bash)]
L1132: #    Register it in src/superclaude/core/HOW-WE-WORK.md (a job row, or the Other commands table; see 3.6)  [inside fence opened at line 1096 (```bash)]
L1134: # 7. Commit  [inside fence opened at line 1096 (```bash)]
L1141: ### 8.4 Testing Components  [outside]
L1167: ### 8.5 Plugin Build Workflow (Future)  [outside]
L1172: # Build plugin artifacts  [inside fence opened at line 1171 (```bash)]
L1175: # Sync to plugin repository  [inside fence opened at line 1171 (```bash)]
L1183: ## 9. Best Practices  [outside]
L1185: ### 9.1 Command Design  [outside]
L1205: ### 9.2 Agent Design  [outside]
L1219: ### 9.3 Skill Design  [outside]
L1244: ### 9.4 Token Management  [outside]
L1257: ### 9.5 Error Handling  [outside]
L1262: ## Error Handling  [inside fence opened at line 1261 (```markdown)]
L1273: ### 9.6 Community Tips (from Research)  [outside]
L1291: ### 9.7 Anti-Patterns  [outside]
L1314: ## 10. Complete Examples  [outside]
L1316: ### Example 1: Simple Command + Agent (Beginner)  [outside]
L1332: # /sc:summary - Project Summary Generator  [inside fence opened at line 1322 (```markdown)]
L1334: ## Triggers  [inside fence opened at line 1322 (```markdown)]
L1338: ## Usage  [inside fence opened at line 1322 (```markdown)]
L1346: ## Options  [outside]
L1353: ## Behavioral Flow  [outside]
L1361: ## Examples  [outside]
L1369: ## Boundaries  [outside]
L1390: # Summary Reporter  [inside fence opened at line 1379 (```)]
L1392: ## Triggers  [inside fence opened at line 1379 (```)]
L1396: ## Behavioral Mindset  [inside fence opened at line 1379 (```)]
L1400: ## Tools  [inside fence opened at line 1379 (```)]
L1405: ## Outputs  [inside fence opened at line 1379 (```)]
L1412: ## Does NOT  [inside fence opened at line 1379 (```)]
L1417: ## Boundaries  [inside fence opened at line 1379 (```)]
L1429: ### Example 2: Medium Command + Skill with Compliance (Intermediate)  [outside]
L1445: # /sc:pr-review - Pull Request Review  [inside fence opened at line 1435 (```markdown)]
L1447: ## Triggers  [inside fence opened at line 1435 (```markdown)]
L1451: ## Usage  [inside fence opened at line 1435 (```markdown)]
L1459: ## Options  [outside]
L1467: ## Behavioral Flow  [outside]
L1478: ## MCP Integration  [outside]
L1482: ## Examples  [outside]
L1490: ## Boundaries  [outside]
L1519: # PR Review Skill  [inside fence opened at line 1501 (```)]
L1521: ## Purpose  [inside fence opened at line 1501 (```)]
L1525: ## Compliance Tier Classification  [inside fence opened at line 1501 (```)]
L1527: ### Auto-Detection  [inside fence opened at line 1501 (```)]
L1544: ### Tier Workflows  [inside fence opened at line 1501 (```)]
L1571: ## Output Format  [inside fence opened at line 1501 (```)]
L1574: # PR Review: <branch-name>  [inside fence opened at line 1501 (```)]
L1576: ## Classification  [inside fence opened at line 1501 (```)]
L1581: ## Findings  [inside fence opened at line 1501 (```)]
L1583: ### Critical (must fix)  [inside fence opened at line 1501 (```)]
L1586: ### Warning (should fix)  [inside fence opened at line 1501 (```)]
L1589: ### Info (consider)  [inside fence opened at line 1501 (```)]
L1592: ## Summary  [inside fence opened at line 1501 (```)]
L1596: ## Will Do  [outside]
L1601: ## Will Not Do  [outside]
L1609: ### Example 3: Complex Command + Skill + Agents with Refs (Advanced)  [inside fence opened at line 1605 (```)]
L1625: # /sc:adversarial - Adversarial Debate & Merge Pipeline  [inside fence opened at line 1605 (```)]
L1627: ## Required Input  [inside fence opened at line 1605 (```)]
L1631: ## Usage  [inside fence opened at line 1605 (```)]
L1634: # Mode A: Compare existing files  [inside fence opened at line 1605 (```)]
L1637: # Mode B: Generate variants from source + compare  [inside fence opened at line 1605 (```)]
L1641: ## Options  [outside]
L1654: ## Behavioral Summary  [outside]
L1663: ## Boundaries  [outside]
L1692: # Adversarial Debate & Merge Pipeline  [inside fence opened at line 1674 (```)]
L1694: ## Purpose  [inside fence opened at line 1674 (```)]
L1702: ## Input Contract  [inside fence opened at line 1674 (```)]
L1704: ### Mode A: Compare existing artifacts (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1708: ### Mode B: Generate + compare (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1714: ## 5-Step Protocol  [inside fence opened at line 1674 (```)]
L1716: ### Step 1: Diff Analysis  [inside fence opened at line 1674 (```)]
L1720: ### Step 2: Adversarial Debate  [inside fence opened at line 1674 (```)]
L1726: ### Step 3: Base Selection  [inside fence opened at line 1674 (```)]
L1733: ### Step 4: Refactoring Plan  [inside fence opened at line 1674 (```)]
L1737: ### Step 5: Merge Execution  [inside fence opened at line 1674 (```)]
L1742: ## Delegation Pattern  [inside fence opened at line 1674 (```)]
L1750: ## Return Contract  [inside fence opened at line 1674 (```)]
L1760: ## Error Handling  [inside fence opened at line 1674 (```)]
L1770: ## Output Collision Protocol  [inside fence opened at line 1674 (```)]
L1773: ## Will Do  [inside fence opened at line 1674 (```)]
L1778: ## Will Not Do  [inside fence opened at line 1674 (```)]
L1788: # Scoring Protocol Reference  [inside fence opened at line 1787 (```markdown)]
L1790: ## Hybrid Scoring Algorithm  [inside fence opened at line 1787 (```markdown)]
L1794: ### Quantitative Metrics (Deterministic)  [inside fence opened at line 1787 (```markdown)]
L1800: ### Qualitative Rubric (LLM with CEV Protocol)  [inside fence opened at line 1787 (```markdown)]
L1812: ### Position-Bias Mitigation  [inside fence opened at line 1787 (```markdown)]
L1819: ### Tiebreaker Protocol  [inside fence opened at line 1787 (```markdown)]
L1829: # Agent Specification Reference  [inside fence opened at line 1828 (```markdown)]
L1831: ## Agent Spec Format  [inside fence opened at line 1828 (```markdown)]
L1837: ### Examples  [inside fence opened at line 1835 (```)]
L1842: ## Advocate Prompt Template  [inside fence opened at line 1835 (```)]
L1858: ## Strengths (with evidence)  [outside]
L1859: ## Weaknesses (with mitigation)  [outside]
L1860: ## Unique Contributions  [outside]
L1861: ## Response to Opposing Arguments  [outside]
L1864: ## Advocate Output Format  [inside fence opened at line 1862 (```)]
L1869: ## Advocate Report: Variant {N}  [inside fence opened at line 1862 (```)]
L1871: ### Strengths  [inside fence opened at line 1862 (```)]
L1875: ### Weaknesses (with mitigation)  [inside fence opened at line 1862 (```)]
L1878: ### Unique Contributions  [inside fence opened at line 1862 (```)]
L1881: ### Response to Opposing Arguments  [inside fence opened at line 1862 (```)]
L1895: # Debate Orchestrator  [inside fence opened at line 1884 (```)]
L1897: ## Triggers  [inside fence opened at line 1884 (```)]
L1901: ## Behavioral Mindset  [inside fence opened at line 1884 (```)]
L1906: ## Model Preference  [inside fence opened at line 1884 (```)]
L1909: ## Tools  [inside fence opened at line 1884 (```)]
L1917: ## Responsibilities  [inside fence opened at line 1884 (```)]
L1927: ## Outputs  [inside fence opened at line 1884 (```)]
L1934: ## Does NOT  [inside fence opened at line 1884 (```)]
L1939: ## Boundaries  [inside fence opened at line 1884 (```)]
L1960: # Merge Executor  [inside fence opened at line 1953 (```markdown)]
L1962: ## Triggers  [inside fence opened at line 1953 (```markdown)]
L1966: ## Behavioral Mindset  [inside fence opened at line 1953 (```markdown)]
L1971: ## Tools  [inside fence opened at line 1953 (```markdown)]
L1976: ## Responsibilities  [inside fence opened at line 1953 (```markdown)]
L1985: ## Outputs  [inside fence opened at line 1953 (```markdown)]
L1989: ## Does NOT  [inside fence opened at line 1953 (```markdown)]
L1994: ## Boundaries  [inside fence opened at line 1953 (```markdown)]
L2008: ## Appendix A: SKILL.md Skeleton Template  [outside]
L2026: # <Skill Title>  [inside fence opened at line 2012 (```markdown)]
L2028: ## Purpose  [inside fence opened at line 2012 (```markdown)]
L2031: ## Input Contract  [inside fence opened at line 2012 (```markdown)]
L2033: ### Required Input (STOP if missing)  [inside fence opened at line 2012 (```markdown)]
L2036: ### Optional Input  [inside fence opened at line 2012 (```markdown)]
L2039: ## Protocol  [inside fence opened at line 2012 (```markdown)]
L2043: ### Step 1: <Name>  [inside fence opened at line 2012 (```markdown)]
L2047: ### Step 2: <Name>  [inside fence opened at line 2012 (```markdown)]
L2050: ## Delegation Pattern  [inside fence opened at line 2012 (```markdown)]
L2056: ## Return Contract  [inside fence opened at line 2012 (```markdown)]
L2065: ## Error Handling  [inside fence opened at line 2012 (```markdown)]
L2071: ## Will Do  [inside fence opened at line 2012 (```markdown)]
L2075: ## Will Not Do  [inside fence opened at line 2012 (```markdown)]
L2080: ## Appendix B: Command Template  [outside]
L2092: # /sc:<name> - <Title>  [inside fence opened at line 2082 (````markdown)]
L2094: ## Triggers  [inside fence opened at line 2082 (````markdown)]
L2098: ## Usage  [inside fence opened at line 2082 (````markdown)]
L2104: ## Options  [inside fence opened at line 2082 (````markdown)]
L2112: ## Behavioral Flow  [inside fence opened at line 2082 (````markdown)]
L2117: ## MCP Integration  [inside fence opened at line 2082 (````markdown)]
L2120: ## Examples  [inside fence opened at line 2082 (````markdown)]
L2127: ## Unattended mode  [inside fence opened at line 2082 (````markdown)]
L2139: ## Boundaries  [inside fence opened at line 2082 (````markdown)]
L2148: ## Appendix C: Agent Template  [outside]
L2157: # <Agent Title>  [inside fence opened at line 2150 (```markdown)]
L2159: ## Triggers  [inside fence opened at line 2150 (```markdown)]
L2163: ## Behavioral Mindset  [inside fence opened at line 2150 (```markdown)]
L2166: ## Model Preference  [inside fence opened at line 2150 (```markdown)]
L2169: ## Tools  [inside fence opened at line 2150 (```markdown)]
L2172: ## Responsibilities  [inside fence opened at line 2150 (```markdown)]
L2176: ## Outputs  [inside fence opened at line 2150 (```markdown)]
L2180: ## Does NOT  [inside fence opened at line 2150 (```markdown)]
L2184: ## Boundaries  [inside fence opened at line 2150 (```markdown)]
L2193: ## Appendix D: File Path Reference  [outside]
L2207: ## Appendix E: Glossary  [outside]
## Inner fence closes outer fence
outer fence opened at L136 (markdown); nested opening at L154; bare fence at L156 closes the OUTER fence
outer fence opened at L177 (); nested opening at L183; bare fence at L216 closes the OUTER fence
outer fence opened at L1322 (markdown); nested opening at L1340; bare fence at L1344 closes the OUTER fence
outer fence opened at L1379 (); nested opening at L1383; bare fence at L1425 closes the OUTER fence
outer fence opened at L1435 (markdown); nested opening at L1453; bare fence at L1457 closes the OUTER fence
outer fence opened at L1501 (); nested opening at L1573; bare fence at L1594 closes the OUTER fence
outer fence opened at L1605 (); nested opening at L1633; bare fence at L1639 closes the OUTER fence
outer fence opened at L1674 (); nested opening at L1678; bare fence at L1783 closes the OUTER fence
outer fence opened at L1862 (); nested opening at L1868; bare fence at L1883 closes the OUTER fence
outer fence opened at L1884 (); nested opening at L1888; bare fence at L1949 closes the OUTER fence

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/fence-t1.txt ===
# Fence state of docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
## Headings
L9: ## Table of Contents  [outside]
L25: ## 1. Introduction  [outside]
L27: ### What SuperClaude Is  [outside]
L39: ### The Three-Tier Architecture  [outside]
L61: ### The Activation Pattern  [outside]
L66: ## Activation  [inside fence opened at line 65 (```markdown)]
L77: ### Installation Locations  [outside]
L98: ### Path rules for primitives  [outside]
L117: ### Context Loading Sequence  [outside]
L130: ## 2. Quick Start  [outside]
L132: ### 2.1 Create a Minimal Command  [outside]
L146: # /sc:hello - Hello World Command  [inside fence opened at line 136 (````markdown)]
L148: ## Triggers  [inside fence opened at line 136 (````markdown)]
L152: ## Usage  [inside fence opened at line 136 (````markdown)]
L158: ## Behavioral Flow  [inside fence opened at line 136 (````markdown)]
L162: ## Examples  [inside fence opened at line 136 (````markdown)]
L169: ## Boundaries  [inside fence opened at line 136 (````markdown)]
L179: ### 2.2 Create a Minimal Agent  [outside]
L190: # Greeter Agent  [inside fence opened at line 183 (```markdown)]
L192: ## Triggers  [inside fence opened at line 183 (```markdown)]
L196: ## Behavioral Mindset  [inside fence opened at line 183 (```markdown)]
L200: ## Tools  [inside fence opened at line 183 (```markdown)]
L204: ## Outputs  [inside fence opened at line 183 (```markdown)]
L208: ## Boundaries  [inside fence opened at line 183 (```markdown)]
L218: ### 2.3 Create a Minimal Skill  [outside]
L229: # Hello Skill  [inside fence opened at line 222 (```markdown)]
L231: ## Purpose  [inside fence opened at line 222 (```markdown)]
L234: ## Protocol  [inside fence opened at line 222 (```markdown)]
L240: ## Will Do  [inside fence opened at line 222 (```markdown)]
L244: ## Will Not Do  [inside fence opened at line 222 (```markdown)]
L249: ### 2.4 Sync and Test  [outside]
L252: # Copy new components from src/ to .claude/  [inside fence opened at line 251 (```bash)]
L255: # Verify sync succeeded  [inside fence opened at line 251 (```bash)]
L258: # Test the command in Claude Code  [inside fence opened at line 251 (```bash)]
L259: # Type: /sc:hello  [inside fence opened at line 251 (```bash)]
L264: ## 3. Commands Deep Dive  [outside]
L266: ### 3.1 Anatomy of a Command File  [outside]
L310: ### 3.2 Command Archetypes  [outside]
L314: #### Archetype 1: Analysis Pipeline  [outside]
L329: #### Archetype 2: Meta-Orchestrator  [outside]
L340: ## CRITICAL BOUNDARIES  [inside fence opened at line 339 (```)]
L346: #### Archetype 3: Unified Executor  [outside]
L363: ### 3.3 Command Processing Pipeline  [outside]
L375: ### 3.4 Performance Profiles  [outside]
L385: ### 3.5 Wave-Enabled Commands  [outside]
L389: ### 3.6 Registering a New Command  [outside]
L397: ## 4. Agents Deep Dive  [outside]
L399: ### 4.1 Anatomy of an Agent File  [outside]
L437: ### 4.2 Agent Patterns  [outside]
L443: #### Pattern 1: Constrained Worker  [outside]
L451: #### Pattern 2: Specialist Investigator  [outside]
L459: #### Pattern 3: Process Orchestrator  [outside]
L469: #### Pattern 4: Meta-Layer Agent  [outside]
L483: ### 4.3 Agent Spec Format (Dynamic Instantiation)  [outside]
L502: ### 4.4 Agent Activation Methods  [outside]
L514: ## 5. Skills Deep Dive  [outside]
L516: ### 5.1 Anatomy of a Skill  [outside]
L531: ### 5.2 SKILL.md Frontmatter  [outside]
L571: ### 5.3 Extended Metadata Comment  [outside]
L586: ### 5.4 Tool Allowlisting  [outside]
L602: ### 5.5 Skill Complexity Tiers  [outside]
L606: #### Tier 1: Simple (SKILL.md only)  [outside]
L626: #### Tier 2: Medium (SKILL.md + allowed-tools + compliance logic)  [outside]
L648: #### Tier 3: Complex (SKILL.md + refs/ + agents + multi-phase)  [outside]
L673: ### 5.6 The refs/ Pattern (Lazy Loading)  [outside]
L685: ## Wave 2: Analysis  [inside fence opened at line 684 (```markdown)]
L698: ### 5.7 The sc- Prefix Convention  [outside]
L710: ### 5.8 Machine-Readable Headers  [outside]
L726: ### 5.9 Input and Output Contracts  [outside]
L728: #### Input Contracts  [outside]
L733: ## Required Input (STOP if missing)  [inside fence opened at line 732 (```markdown)]
L735: ### Mode A: Compare existing artifacts  [inside fence opened at line 732 (```markdown)]
L738: ### Mode B: Generate variants from source  [inside fence opened at line 732 (```markdown)]
L747: #### Output / Return Contracts  [outside]
L752: ## Return Contract  [inside fence opened at line 751 (```markdown)]
L765: #### Worker contract (under `--unattended`)  [outside]
L774: ### 5.10 Skill-Authoring Checklist  [outside]
L802: ## 6. Multi-Phase Architecture  [outside]
L804: ### 6.1 Wave System  [outside]
L836: ### 6.2 Compliance Tiers  [outside]
L866: ### 6.3 Delegation Intelligence  [outside]
L888: ### 6.4 Resource Management Zones  [outside]
L902: ## 7. Integration Patterns  [outside]
L904: ### 7.1 Command + Skill + Agent Composition  [outside]
L930: ### 7.2 MCP Server Integration  [outside]
L950: ### 7.3 Persona Integration  [outside]
L975: ### 7.4 Thinking Depth Flags  [outside]
L985: ### 7.5 Dynamic Context Injection  [outside]
L990: ## Repository Context  [inside fence opened at line 989 (```markdown)]
L998: ### 7.6 Orca Orchestration: Commands as Workers  [outside]
L1002: #### How the pieces fit  [outside]
L1009: #### Rollout state  [outside]
L1015: #### Deciding whether a new command can be a worker  [outside]
L1022: #### What a command does under `--unattended`  [outside]
L1037: #### The worker session, not the command (WC-7)  [outside]
L1041: #### The `## Unattended mode` section of a converted command  [outside]
L1047: #### Skills and agents under a command  [outside]
L1056: ## 8. Development Workflow  [outside]
L1058: ### 8.1 Source of Truth  [outside]
L1071: ### 8.2 Sync Workflow  [outside]
L1076: # 1. Make your changes in src/superclaude/  [inside fence opened at line 1075 (```bash)]
L1077: # 2. Sync to .claude/  [inside fence opened at line 1075 (```bash)]
L1080: # 3. Verify sync succeeded  [inside fence opened at line 1075 (```bash)]
L1087: # 1. Copy changes back to src/superclaude/ manually  [inside fence opened at line 1086 (```bash)]
L1088: # 2. Verify both sides match  [inside fence opened at line 1086 (```bash)]
L1094: ### 8.3 Creating a New Component: Full Workflow  [outside]
L1097: # 1. Scaffold the component  [inside fence opened at line 1096 (```bash)]
L1098: #    Command:  [inside fence opened at line 1096 (```bash)]
L1101: #    Agent:  [inside fence opened at line 1096 (```bash)]
L1104: #    Skill (simple):  [inside fence opened at line 1096 (```bash)]
L1108: #    Skill (complex with refs):  [inside fence opened at line 1096 (```bash)]
L1113: # 2. Write the component (see templates in Section 10)  [inside fence opened at line 1096 (```bash)]
L1115: # 2a. Decide worker eligibility (WC-2, section 7.6)  [inside fence opened at line 1096 (```bash)]
L1116: #    If the command will accept --unattended, write its ## Unattended mode section  [inside fence opened at line 1096 (```bash)]
L1117: #    and add its name to UNATTENDED_COMMANDS in tests/skills/test_worker_contract.py  [inside fence opened at line 1096 (```bash)]
L1119: # 3. Sync to .claude/ for testing  [inside fence opened at line 1096 (```bash)]
L1122: # 4. Verify sync  [inside fence opened at line 1096 (```bash)]
L1125: # 5. Test in Claude Code  [inside fence opened at line 1096 (```bash)]
L1126: #    - Invoke the command/agent/skill  [inside fence opened at line 1096 (```bash)]
L1127: #    - Verify triggers activate correctly  [inside fence opened at line 1096 (```bash)]
L1128: #    - Validate output matches expected behavior  [inside fence opened at line 1096 (```bash)]
L1129: #    - Test edge cases and error conditions  [inside fence opened at line 1096 (```bash)]
L1131: # 6. Register the component (commands only)  [inside fence opened at line 1096 (```bash)]
L1132: #    Register it in src/superclaude/core/HOW-WE-WORK.md (a job row, or the Other commands table; see 3.6)  [inside fence opened at line 1096 (```bash)]
L1134: # 7. Commit  [inside fence opened at line 1096 (```bash)]
L1141: ### 8.4 Testing Components  [outside]
L1167: ### 8.5 Plugin Build Workflow (Future)  [outside]
L1172: # Build plugin artifacts  [inside fence opened at line 1171 (```bash)]
L1175: # Sync to plugin repository  [inside fence opened at line 1171 (```bash)]
L1183: ## 9. Best Practices  [outside]
L1185: ### 9.1 Command Design  [outside]
L1205: ### 9.2 Agent Design  [outside]
L1219: ### 9.3 Skill Design  [outside]
L1244: ### 9.4 Token Management  [outside]
L1257: ### 9.5 Error Handling  [outside]
L1262: ## Error Handling  [inside fence opened at line 1261 (```markdown)]
L1273: ### 9.6 Community Tips (from Research)  [outside]
L1291: ### 9.7 Anti-Patterns  [outside]
L1314: ## 10. Complete Examples  [outside]
L1316: ### Example 1: Simple Command + Agent (Beginner)  [outside]
L1332: # /sc:summary - Project Summary Generator  [inside fence opened at line 1322 (```markdown)]
L1334: ## Triggers  [inside fence opened at line 1322 (```markdown)]
L1338: ## Usage  [inside fence opened at line 1322 (```markdown)]
L1346: ## Options  [outside]
L1353: ## Behavioral Flow  [outside]
L1361: ## Examples  [outside]
L1369: ## Boundaries  [outside]
L1390: # Summary Reporter  [inside fence opened at line 1379 (```)]
L1392: ## Triggers  [inside fence opened at line 1379 (```)]
L1396: ## Behavioral Mindset  [inside fence opened at line 1379 (```)]
L1400: ## Tools  [inside fence opened at line 1379 (```)]
L1405: ## Outputs  [inside fence opened at line 1379 (```)]
L1412: ## Does NOT  [inside fence opened at line 1379 (```)]
L1417: ## Boundaries  [inside fence opened at line 1379 (```)]
L1429: ### Example 2: Medium Command + Skill with Compliance (Intermediate)  [outside]
L1445: # /sc:pr-review - Pull Request Review  [inside fence opened at line 1435 (```markdown)]
L1447: ## Triggers  [inside fence opened at line 1435 (```markdown)]
L1451: ## Usage  [inside fence opened at line 1435 (```markdown)]
L1459: ## Options  [outside]
L1467: ## Behavioral Flow  [outside]
L1478: ## MCP Integration  [outside]
L1482: ## Examples  [outside]
L1490: ## Boundaries  [outside]
L1519: # PR Review Skill  [inside fence opened at line 1501 (```)]
L1521: ## Purpose  [inside fence opened at line 1501 (```)]
L1525: ## Compliance Tier Classification  [inside fence opened at line 1501 (```)]
L1527: ### Auto-Detection  [inside fence opened at line 1501 (```)]
L1544: ### Tier Workflows  [inside fence opened at line 1501 (```)]
L1571: ## Output Format  [inside fence opened at line 1501 (```)]
L1574: # PR Review: <branch-name>  [inside fence opened at line 1501 (```)]
L1576: ## Classification  [inside fence opened at line 1501 (```)]
L1581: ## Findings  [inside fence opened at line 1501 (```)]
L1583: ### Critical (must fix)  [inside fence opened at line 1501 (```)]
L1586: ### Warning (should fix)  [inside fence opened at line 1501 (```)]
L1589: ### Info (consider)  [inside fence opened at line 1501 (```)]
L1592: ## Summary  [inside fence opened at line 1501 (```)]
L1596: ## Will Do  [outside]
L1601: ## Will Not Do  [outside]
L1609: ### Example 3: Complex Command + Skill + Agents with Refs (Advanced)  [inside fence opened at line 1605 (```)]
L1625: # /sc:adversarial - Adversarial Debate & Merge Pipeline  [inside fence opened at line 1605 (```)]
L1627: ## Required Input  [inside fence opened at line 1605 (```)]
L1631: ## Usage  [inside fence opened at line 1605 (```)]
L1634: # Mode A: Compare existing files  [inside fence opened at line 1605 (```)]
L1637: # Mode B: Generate variants from source + compare  [inside fence opened at line 1605 (```)]
L1641: ## Options  [outside]
L1654: ## Behavioral Summary  [outside]
L1663: ## Boundaries  [outside]
L1692: # Adversarial Debate & Merge Pipeline  [inside fence opened at line 1674 (```)]
L1694: ## Purpose  [inside fence opened at line 1674 (```)]
L1702: ## Input Contract  [inside fence opened at line 1674 (```)]
L1704: ### Mode A: Compare existing artifacts (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1708: ### Mode B: Generate + compare (STOP if invalid)  [inside fence opened at line 1674 (```)]
L1714: ## 5-Step Protocol  [inside fence opened at line 1674 (```)]
L1716: ### Step 1: Diff Analysis  [inside fence opened at line 1674 (```)]
L1720: ### Step 2: Adversarial Debate  [inside fence opened at line 1674 (```)]
L1726: ### Step 3: Base Selection  [inside fence opened at line 1674 (```)]
L1733: ### Step 4: Refactoring Plan  [inside fence opened at line 1674 (```)]
L1737: ### Step 5: Merge Execution  [inside fence opened at line 1674 (```)]
L1742: ## Delegation Pattern  [inside fence opened at line 1674 (```)]
L1750: ## Return Contract  [inside fence opened at line 1674 (```)]
L1760: ## Error Handling  [inside fence opened at line 1674 (```)]
L1770: ## Output Collision Protocol  [inside fence opened at line 1674 (```)]
L1773: ## Will Do  [inside fence opened at line 1674 (```)]
L1778: ## Will Not Do  [inside fence opened at line 1674 (```)]
L1788: # Scoring Protocol Reference  [inside fence opened at line 1787 (```markdown)]
L1790: ## Hybrid Scoring Algorithm  [inside fence opened at line 1787 (```markdown)]
L1794: ### Quantitative Metrics (Deterministic)  [inside fence opened at line 1787 (```markdown)]
L1800: ### Qualitative Rubric (LLM with CEV Protocol)  [inside fence opened at line 1787 (```markdown)]
L1812: ### Position-Bias Mitigation  [inside fence opened at line 1787 (```markdown)]
L1819: ### Tiebreaker Protocol  [inside fence opened at line 1787 (```markdown)]
L1829: # Agent Specification Reference  [inside fence opened at line 1828 (```markdown)]
L1831: ## Agent Spec Format  [inside fence opened at line 1828 (```markdown)]
L1837: ### Examples  [inside fence opened at line 1835 (```)]
L1842: ## Advocate Prompt Template  [inside fence opened at line 1835 (```)]
L1858: ## Strengths (with evidence)  [outside]
L1859: ## Weaknesses (with mitigation)  [outside]
L1860: ## Unique Contributions  [outside]
L1861: ## Response to Opposing Arguments  [outside]
L1864: ## Advocate Output Format  [inside fence opened at line 1862 (```)]
L1869: ## Advocate Report: Variant {N}  [inside fence opened at line 1862 (```)]
L1871: ### Strengths  [inside fence opened at line 1862 (```)]
L1875: ### Weaknesses (with mitigation)  [inside fence opened at line 1862 (```)]
L1878: ### Unique Contributions  [inside fence opened at line 1862 (```)]
L1881: ### Response to Opposing Arguments  [inside fence opened at line 1862 (```)]
L1895: # Debate Orchestrator  [inside fence opened at line 1884 (```)]
L1897: ## Triggers  [inside fence opened at line 1884 (```)]
L1901: ## Behavioral Mindset  [inside fence opened at line 1884 (```)]
L1906: ## Model Preference  [inside fence opened at line 1884 (```)]
L1909: ## Tools  [inside fence opened at line 1884 (```)]
L1917: ## Responsibilities  [inside fence opened at line 1884 (```)]
L1927: ## Outputs  [inside fence opened at line 1884 (```)]
L1934: ## Does NOT  [inside fence opened at line 1884 (```)]
L1939: ## Boundaries  [inside fence opened at line 1884 (```)]
L1960: # Merge Executor  [inside fence opened at line 1953 (```markdown)]
L1962: ## Triggers  [inside fence opened at line 1953 (```markdown)]
L1966: ## Behavioral Mindset  [inside fence opened at line 1953 (```markdown)]
L1971: ## Tools  [inside fence opened at line 1953 (```markdown)]
L1976: ## Responsibilities  [inside fence opened at line 1953 (```markdown)]
L1985: ## Outputs  [inside fence opened at line 1953 (```markdown)]
L1989: ## Does NOT  [inside fence opened at line 1953 (```markdown)]
L1994: ## Boundaries  [inside fence opened at line 1953 (```markdown)]
L2008: ## Appendix A: SKILL.md Skeleton Template  [outside]
L2026: # <Skill Title>  [inside fence opened at line 2012 (```markdown)]
L2028: ## Purpose  [inside fence opened at line 2012 (```markdown)]
L2031: ## Input Contract  [inside fence opened at line 2012 (```markdown)]
L2033: ### Required Input (STOP if missing)  [inside fence opened at line 2012 (```markdown)]
L2036: ### Optional Input  [inside fence opened at line 2012 (```markdown)]
L2039: ## Protocol  [inside fence opened at line 2012 (```markdown)]
L2043: ### Step 1: <Name>  [inside fence opened at line 2012 (```markdown)]
L2047: ### Step 2: <Name>  [inside fence opened at line 2012 (```markdown)]
L2050: ## Delegation Pattern  [inside fence opened at line 2012 (```markdown)]
L2056: ## Return Contract  [inside fence opened at line 2012 (```markdown)]
L2065: ## Error Handling  [inside fence opened at line 2012 (```markdown)]
L2071: ## Will Do  [inside fence opened at line 2012 (```markdown)]
L2075: ## Will Not Do  [inside fence opened at line 2012 (```markdown)]
L2080: ## Appendix B: Command Template  [outside]
L2092: # /sc:<name> - <Title>  [inside fence opened at line 2082 (````markdown)]
L2094: ## Triggers  [inside fence opened at line 2082 (````markdown)]
L2098: ## Usage  [inside fence opened at line 2082 (````markdown)]
L2104: ## Options  [inside fence opened at line 2082 (````markdown)]
L2112: ## Behavioral Flow  [inside fence opened at line 2082 (````markdown)]
L2117: ## MCP Integration  [inside fence opened at line 2082 (````markdown)]
L2120: ## Examples  [inside fence opened at line 2082 (````markdown)]
L2127: ## Unattended mode  [inside fence opened at line 2082 (````markdown)]
L2139: ## Boundaries  [inside fence opened at line 2082 (````markdown)]
L2148: ## Appendix C: Agent Template  [outside]
L2157: # <Agent Title>  [inside fence opened at line 2150 (```markdown)]
L2159: ## Triggers  [inside fence opened at line 2150 (```markdown)]
L2163: ## Behavioral Mindset  [inside fence opened at line 2150 (```markdown)]
L2166: ## Model Preference  [inside fence opened at line 2150 (```markdown)]
L2169: ## Tools  [inside fence opened at line 2150 (```markdown)]
L2172: ## Responsibilities  [inside fence opened at line 2150 (```markdown)]
L2176: ## Outputs  [inside fence opened at line 2150 (```markdown)]
L2180: ## Does NOT  [inside fence opened at line 2150 (```markdown)]
L2184: ## Boundaries  [inside fence opened at line 2150 (```markdown)]
L2193: ## Appendix D: File Path Reference  [outside]
L2207: ## Appendix E: Glossary  [outside]
## Inner fence closes outer fence
outer fence opened at L1322 (markdown); nested opening at L1340; bare fence at L1344 closes the OUTER fence
outer fence opened at L1379 (); nested opening at L1383; bare fence at L1425 closes the OUTER fence
outer fence opened at L1435 (markdown); nested opening at L1453; bare fence at L1457 closes the OUTER fence
outer fence opened at L1501 (); nested opening at L1573; bare fence at L1594 closes the OUTER fence
outer fence opened at L1605 (); nested opening at L1633; bare fence at L1639 closes the OUTER fence
outer fence opened at L1674 (); nested opening at L1678; bare fence at L1783 closes the OUTER fence
outer fence opened at L1862 (); nested opening at L1868; bare fence at L1883 closes the OUTER fence
outer fence opened at L1884 (); nested opening at L1888; bare fence at L1949 closes the OUTER fence

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/t1-diff.txt ===
136c136
< ```markdown
---
> ````markdown
177c177
< ```
---
> ````

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/fence-check.py ===
"""Fence-state checker for one Markdown file (Task 8 evidence; not a delivery file).

A fence opens on a line of 3 or more backticks or tildes (optionally followed by an
info string) and closes only on a bare fence line of the same character that is at
least as long as the opening run. While a fence is open, a line that looks like a new
opening fence with an info string (for example ```bash inside a ```markdown block) is
recorded as a nested opening; when a bare fence then closes the outer fence, that spot
is reported as an inner fence closing the outer one.

Usage: uv run python -I t8-fence-check.py <file.md>
Prints every heading line with its fence state, then every inner-closes-outer spot.
"""
import re
import sys

OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def scan(lines):
    headings = []
    spots = []
    fence = None  # (char, length, open_line, info)
    nested = None  # line number of the latest nested opening-shaped line
    for n, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        m = OPEN_RE.match(line)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)), n, m.group(2).strip())
                nested = None
            elif re.match(r"^#{1,6} ", line):
                headings.append((n, line, "outside"))
            continue
        char, length, open_line, info = fence
        if m and m.group(1)[0] == char:
            run = len(m.group(1))
            rest = m.group(2).strip()
            if rest == "" and run >= length:
                if nested is not None:
                    spots.append((open_line, info, nested, n))
                fence = None
                nested = None
                continue
            if rest != "" and run >= length:
                # A shorter run is a valid nested fence; only a run at least as long
                # as the outer one marks a nested block whose bare close ends the outer.
                nested = n
                continue
        if re.match(r"^#{1,6} ", line):
            headings.append((n, line, f"inside fence opened at line {open_line} ({'`' * length if char == '`' else '~' * length}{info})"))
    if fence is not None:
        spots.append((fence[2], fence[3], None, None))
    return headings, spots


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    headings, spots = scan(lines)
    print(f"# Fence state of {path}")
    print("## Headings")
    for n, text, state in headings:
        print(f"L{n}: {text}  [{state}]")
    print("## Inner fence closes outer fence")
    if not spots:
        print("none")
    for open_line, info, nested, close in spots:
        if close is None:
            print(f"outer fence opened at L{open_line} ({info}) is never closed")
        else:
            print(f"outer fence opened at L{open_line} ({info}); nested opening at L{nested}; bare fence at L{close} closes the OUTER fence")


if __name__ == "__main__":
    main()

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 
Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
