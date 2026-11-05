38ad79cd28c69908e88e28dc0db47801e54880b8
Review one task for spec compliance.

Task brief: T2 (AC ids in order of the "Acceptance criteria:" bullets: T2.AC1,T2.AC2,T2.AC3,T2.AC4,T2.AC5). Plan file: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/TASK-WF-devGuideFenceFix-20261104-204854.md, lines 39-50:
## Task 2: Fix the five section 10 template fences

Depends on: Task 1

In section 10 "Complete Examples" of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, read each of these templates and change its outer opening fence to four backticks plus `markdown` and its outer closing fence to four backticks (guide line numbers as of today): Example 1 command file (1322, 1379); Example 2 command file (1435, 1501); Example 2 skill file `src/superclaude/skills/sc-pr-review/SKILL.md` (1505, 1605); Example 3 command file `src/superclaude/commands/adversarial.md` (1615, 1674); Example 3 `src/superclaude/skills/sc-adversarial/refs/agent-specs.md` (1828, 1884). If a line number has moved, locate the pair by its `**File**:` line and template and record the actual lines in `./artifacts/t2-notes.txt`. Then run the whole-change checks below and save their outputs.

Acceptance criteria:
- `uv run python -I ./artifacts/fence-check.py docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, saved as `./artifacts/fence-after.txt`, prints `none` under "Inner fence closes outer fence"; shows `### 2.2 Create a Minimal Agent`, every `### Example N:` heading of section 10 and `## Appendix C: Agent Template` outside any fence; and shows `## Appendix B: Command Template`'s template headings inside its four-backtick fence, as in `./artifacts/fence-before.txt`.
- `diff ./artifacts/guide-before.md docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, saved as `./artifacts/guide-diff.txt`, changes exactly twelve lines, each a lone outer-fence line (```` ``` ```` to ````` ```` ````` or ```` ```markdown ```` to ````` ````markdown `````), and nothing else.
- The changed lines contain no em dash or en dash, checked with `LC_ALL=C grep -P '\xE2\x80[\x93\x94]'` over the `>` lines of `./artifacts/guide-diff.txt` (no output), saved as `./artifacts/dash-check.txt`.
- `uv run pytest tests/docs -q` passes, output saved as `./artifacts/pytest-docs.txt`.
- `git status --porcelain -- docs src plugins tests` shows no change outside the guide other than the already-staged `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, saved as `./artifacts/changed-files.txt`.

Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/TASK-WF-devGuideFenceFix-20261104-204854.md lines 17-24)
## Constraints

- Only `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` changes, and only on the twelve outer-fence lines the source lists (the opening and closing line of each of the six templates). No prose line, inner code block or other fence changes. Scripts and evidence go under this package's `./artifacts/`.
- Each opening line becomes four backticks followed by `markdown`; each closing line becomes four backticks and nothing else.
- The archived script `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py` is copied, never edited; the copy lives at `./artifacts/fence-check.py` and runs with `uv run python -I`.
- The earlier guide refactor is still uncommitted, so "the guide before this plan" means the copy `./artifacts/guide-before.md` saved before the first edit, not `HEAD`.
- No em dash and no en dash in changed lines.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.

Start sha: 38ad79cd28c69908e88e28dc0db47801e54880b8
Diff against the start snapshot: (git diff 38ad79cd28c69908e88e28dc0db47801e54880b8 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/ listed after the diff)
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 18769966..34b69f86 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -1319,7 +1319,7 @@ A command that generates a project summary report.
 
 **File**: `src/superclaude/commands/summary.md`
 
-```markdown
+````markdown
 ---
 name: summary
 description: "Generate a concise project summary with file counts and key metrics"
@@ -1376,7 +1376,7 @@ personas: [analyzer]
 - Modify any files
 - Access external services or APIs
 - Execute project code or tests
-```
+````
 
 **File**: `src/superclaude/agents/summary-reporter.md`
 
@@ -1432,7 +1432,7 @@ A command that reviews pull request changes with compliance-tiered analysis.
 
 **File**: `src/superclaude/commands/pr-review.md`
 
-```markdown
+````markdown
 ---
 name: pr-review
 description: "Review pull request changes with compliance-tiered analysis depth"
@@ -1498,11 +1498,11 @@ personas: [analyzer, qa, security]
 - Modify any code or auto-fix issues
 - Approve or reject the PR (advisory only)
 - Access external PR systems or APIs
-```
+````
 
 **File**: `src/superclaude/skills/sc-pr-review/SKILL.md`
 
-```markdown
+````markdown
 ---
 name: sc-pr-review
 description: "Pull request review with compliance-tiered analysis and multi-persona evaluation"
@@ -1602,7 +1602,7 @@ security_paths: <boolean>
 - Modify any code or apply fixes
 - Access external PR platforms
 - Make approval/rejection decisions
-```
+````
 
 ---
 
@@ -1612,7 +1612,7 @@ This example shows the full `/sc:adversarial` implementation as it exists in the
 
 **File**: `src/superclaude/commands/adversarial.md`
 
-```markdown
+````markdown
 ---
 name: adversarial
 description: "Structured adversarial debate, comparison, and merge pipeline for 2-10 artifacts"
@@ -1671,7 +1671,7 @@ Executes a 5-step protocol producing 6 artifacts:
 - Participate in debates (delegates to advocate agents)
 - Override scoring without documented justification
 - Skip protocol steps
-```
+````
 
 **File**: `src/superclaude/skills/sc-adversarial/SKILL.md`
 
@@ -1825,7 +1825,7 @@ If top variants score within 5% of each other:
 
 **File**: `src/superclaude/skills/sc-adversarial/refs/agent-specs.md`
 
-```markdown
+````markdown
 # Agent Specification Reference
 
 ## Agent Spec Format
@@ -1881,7 +1881,7 @@ Each advocate produces a structured argument:
 ### Response to Opposing Arguments
 - Re: [opposing point]: [steelman response]
 ```
-```
+````
 
 **File**: `src/superclaude/agents/debate-orchestrator.md`
 

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/fence-after.txt ===
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
L1332: # /sc:summary - Project Summary Generator  [inside fence opened at line 1322 (````markdown)]
L1334: ## Triggers  [inside fence opened at line 1322 (````markdown)]
L1338: ## Usage  [inside fence opened at line 1322 (````markdown)]
L1346: ## Options  [inside fence opened at line 1322 (````markdown)]
L1353: ## Behavioral Flow  [inside fence opened at line 1322 (````markdown)]
L1361: ## Examples  [inside fence opened at line 1322 (````markdown)]
L1369: ## Boundaries  [inside fence opened at line 1322 (````markdown)]
L1390: # Summary Reporter  [inside fence opened at line 1383 (```markdown)]
L1392: ## Triggers  [inside fence opened at line 1383 (```markdown)]
L1396: ## Behavioral Mindset  [inside fence opened at line 1383 (```markdown)]
L1400: ## Tools  [inside fence opened at line 1383 (```markdown)]
L1405: ## Outputs  [inside fence opened at line 1383 (```markdown)]
L1412: ## Does NOT  [inside fence opened at line 1383 (```markdown)]
L1417: ## Boundaries  [inside fence opened at line 1383 (```markdown)]
L1429: ### Example 2: Medium Command + Skill with Compliance (Intermediate)  [outside]
L1445: # /sc:pr-review - Pull Request Review  [inside fence opened at line 1435 (````markdown)]
L1447: ## Triggers  [inside fence opened at line 1435 (````markdown)]
L1451: ## Usage  [inside fence opened at line 1435 (````markdown)]
L1459: ## Options  [inside fence opened at line 1435 (````markdown)]
L1467: ## Behavioral Flow  [inside fence opened at line 1435 (````markdown)]
L1478: ## MCP Integration  [inside fence opened at line 1435 (````markdown)]
L1482: ## Examples  [inside fence opened at line 1435 (````markdown)]
L1490: ## Boundaries  [inside fence opened at line 1435 (````markdown)]
L1519: # PR Review Skill  [inside fence opened at line 1505 (````markdown)]
L1521: ## Purpose  [inside fence opened at line 1505 (````markdown)]
L1525: ## Compliance Tier Classification  [inside fence opened at line 1505 (````markdown)]
L1527: ### Auto-Detection  [inside fence opened at line 1505 (````markdown)]
L1544: ### Tier Workflows  [inside fence opened at line 1505 (````markdown)]
L1571: ## Output Format  [inside fence opened at line 1505 (````markdown)]
L1574: # PR Review: <branch-name>  [inside fence opened at line 1505 (````markdown)]
L1576: ## Classification  [inside fence opened at line 1505 (````markdown)]
L1581: ## Findings  [inside fence opened at line 1505 (````markdown)]
L1583: ### Critical (must fix)  [inside fence opened at line 1505 (````markdown)]
L1586: ### Warning (should fix)  [inside fence opened at line 1505 (````markdown)]
L1589: ### Info (consider)  [inside fence opened at line 1505 (````markdown)]
L1592: ## Summary  [inside fence opened at line 1505 (````markdown)]
L1596: ## Will Do  [inside fence opened at line 1505 (````markdown)]
L1601: ## Will Not Do  [inside fence opened at line 1505 (````markdown)]
L1609: ### Example 3: Complex Command + Skill + Agents with Refs (Advanced)  [outside]
L1625: # /sc:adversarial - Adversarial Debate & Merge Pipeline  [inside fence opened at line 1615 (````markdown)]
L1627: ## Required Input  [inside fence opened at line 1615 (````markdown)]
L1631: ## Usage  [inside fence opened at line 1615 (````markdown)]
L1634: # Mode A: Compare existing files  [inside fence opened at line 1615 (````markdown)]
L1637: # Mode B: Generate variants from source + compare  [inside fence opened at line 1615 (````markdown)]
L1641: ## Options  [inside fence opened at line 1615 (````markdown)]
L1654: ## Behavioral Summary  [inside fence opened at line 1615 (````markdown)]
L1663: ## Boundaries  [inside fence opened at line 1615 (````markdown)]
L1692: # Adversarial Debate & Merge Pipeline  [inside fence opened at line 1678 (```markdown)]
L1694: ## Purpose  [inside fence opened at line 1678 (```markdown)]
L1702: ## Input Contract  [inside fence opened at line 1678 (```markdown)]
L1704: ### Mode A: Compare existing artifacts (STOP if invalid)  [inside fence opened at line 1678 (```markdown)]
L1708: ### Mode B: Generate + compare (STOP if invalid)  [inside fence opened at line 1678 (```markdown)]
L1714: ## 5-Step Protocol  [inside fence opened at line 1678 (```markdown)]
L1716: ### Step 1: Diff Analysis  [inside fence opened at line 1678 (```markdown)]
L1720: ### Step 2: Adversarial Debate  [inside fence opened at line 1678 (```markdown)]
L1726: ### Step 3: Base Selection  [inside fence opened at line 1678 (```markdown)]
L1733: ### Step 4: Refactoring Plan  [inside fence opened at line 1678 (```markdown)]
L1737: ### Step 5: Merge Execution  [inside fence opened at line 1678 (```markdown)]
L1742: ## Delegation Pattern  [inside fence opened at line 1678 (```markdown)]
L1750: ## Return Contract  [inside fence opened at line 1678 (```markdown)]
L1760: ## Error Handling  [inside fence opened at line 1678 (```markdown)]
L1770: ## Output Collision Protocol  [inside fence opened at line 1678 (```markdown)]
L1773: ## Will Do  [inside fence opened at line 1678 (```markdown)]
L1778: ## Will Not Do  [inside fence opened at line 1678 (```markdown)]
L1788: # Scoring Protocol Reference  [inside fence opened at line 1787 (```markdown)]
L1790: ## Hybrid Scoring Algorithm  [inside fence opened at line 1787 (```markdown)]
L1794: ### Quantitative Metrics (Deterministic)  [inside fence opened at line 1787 (```markdown)]
L1800: ### Qualitative Rubric (LLM with CEV Protocol)  [inside fence opened at line 1787 (```markdown)]
L1812: ### Position-Bias Mitigation  [inside fence opened at line 1787 (```markdown)]
L1819: ### Tiebreaker Protocol  [inside fence opened at line 1787 (```markdown)]
L1829: # Agent Specification Reference  [inside fence opened at line 1828 (````markdown)]
L1831: ## Agent Spec Format  [inside fence opened at line 1828 (````markdown)]
L1837: ### Examples  [inside fence opened at line 1828 (````markdown)]
L1842: ## Advocate Prompt Template  [inside fence opened at line 1828 (````markdown)]
L1858: ## Strengths (with evidence)  [inside fence opened at line 1828 (````markdown)]
L1859: ## Weaknesses (with mitigation)  [inside fence opened at line 1828 (````markdown)]
L1860: ## Unique Contributions  [inside fence opened at line 1828 (````markdown)]
L1861: ## Response to Opposing Arguments  [inside fence opened at line 1828 (````markdown)]
L1864: ## Advocate Output Format  [inside fence opened at line 1828 (````markdown)]
L1869: ## Advocate Report: Variant {N}  [inside fence opened at line 1828 (````markdown)]
L1871: ### Strengths  [inside fence opened at line 1828 (````markdown)]
L1875: ### Weaknesses (with mitigation)  [inside fence opened at line 1828 (````markdown)]
L1878: ### Unique Contributions  [inside fence opened at line 1828 (````markdown)]
L1881: ### Response to Opposing Arguments  [inside fence opened at line 1828 (````markdown)]
L1895: # Debate Orchestrator  [inside fence opened at line 1888 (```markdown)]
L1897: ## Triggers  [inside fence opened at line 1888 (```markdown)]
L1901: ## Behavioral Mindset  [inside fence opened at line 1888 (```markdown)]
L1906: ## Model Preference  [inside fence opened at line 1888 (```markdown)]
L1909: ## Tools  [inside fence opened at line 1888 (```markdown)]
L1917: ## Responsibilities  [inside fence opened at line 1888 (```markdown)]
L1927: ## Outputs  [inside fence opened at line 1888 (```markdown)]
L1934: ## Does NOT  [inside fence opened at line 1888 (```markdown)]
L1939: ## Boundaries  [inside fence opened at line 1888 (```markdown)]
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
none

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/guide-diff.txt ===
136c136
< ```markdown
---
> ````markdown
177c177
< ```
---
> ````
1322c1322
< ```markdown
---
> ````markdown
1379c1379
< ```
---
> ````
1435c1435
< ```markdown
---
> ````markdown
1501c1501
< ```
---
> ````
1505c1505
< ```markdown
---
> ````markdown
1605c1605
< ```
---
> ````
1615c1615
< ```markdown
---
> ````markdown
1674c1674
< ```
---
> ````
1828c1828
< ```markdown
---
> ````markdown
1884c1884
< ```
---
> ````

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/dash-check.txt ===
$ grep '^>' ./artifacts/guide-diff.txt | LC_ALL=C grep -P '\xE2\x80[\x93\x94]'
rc=1 (1 with no output = no em or en dash)

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/pytest-docs.txt ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 8 items

tests/docs/test_chrome_devtools_mcp_removed.py .                         [ 12%]
tests/docs/test_retired_docs_absent.py ..                                [ 37%]
tests/docs/test_tavily_doc_alignment.py .....                            [100%]

============================== 8 passed in 0.69s ===============================

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-devGuideFenceFix-20261104-204854/artifacts/changed-files.txt ===
 M docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
M  docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md

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
