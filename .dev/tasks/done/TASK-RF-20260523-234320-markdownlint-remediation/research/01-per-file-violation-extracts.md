# Research: Per-File Markdownlint Violation Extracts

**Topic type:** File Inventory
**Scope:** 9 src/superclaude/agents/*.md files
**Status:** In Progress
**Date:** 2026-05-23
---

## src/superclaude/agents/deep-research.md

**Total violations: 1** (MD040×1)

### MD040 (fenced-code-language)

- `src/superclaude/agents/deep-research.md:61 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "   ```"]`

### Remediation summary

Single MD040 violation — add a language tag (e.g. `text`/`bash`/`json`) to one fenced code block at line 61. **Effort: trivial.**

---

## src/superclaude/agents/deep-research-agent.md

**Total violations: 15** (MD036×15)

### MD036 (no-emphasis-as-heading)

- `src/superclaude/agents/deep-research-agent.md:59 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Entity Expansion"]`
- `src/superclaude/agents/deep-research-agent.md:65 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Temporal Progression"]`
- `src/superclaude/agents/deep-research-agent.md:70 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Conceptual Deepening"]`
- `src/superclaude/agents/deep-research-agent.md:75 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Causal Chains"]`
- `src/superclaude/agents/deep-research-agent.md:93 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Quality Monitoring"]`
- `src/superclaude/agents/deep-research-agent.md:100 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Replanning Triggers"]`
- `src/superclaude/agents/deep-research-agent.md:109 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Result Evaluation"]`
- `src/superclaude/agents/deep-research-agent.md:116 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Citation Requirements"]`
- `src/superclaude/agents/deep-research-agent.md:126 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Tavily-First Rule (mandatory)"]`
- `src/superclaude/agents/deep-research-agent.md:135 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Search Strategy"]`
- `src/superclaude/agents/deep-research-agent.md:142 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Extraction Routing"]`
- `src/superclaude/agents/deep-research-agent.md:150 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Fallback Policy — when to fall..."]`
- `src/superclaude/agents/deep-research-agent.md:161 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Parallel Optimization"]`
- `src/superclaude/agents/deep-research-agent.md:170 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Pattern Recognition"]`
- `src/superclaude/agents/deep-research-agent.md:177 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Memory Usage"]`

### Remediation summary

Uniform MD036 cluster — each bold/italic line acts as a section label inside a larger H2/H3 block. Convert to actual headings (`####` likely) OR preserve as bold-then-paragraph if the surrounding semantic flow demands inline labels. Sample classification of convert-vs-preserve is researcher-2's job. **Effort: small** (15 mechanical edits, identical pattern).

---

## src/superclaude/agents/rf-task-researcher.md

**Total violations: 18** (MD040×18)

### MD040 (fenced-code-language)

- `src/superclaude/agents/rf-task-researcher.md:66 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:80 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:99 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:108 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:117 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:137 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:175 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:189 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:209 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:223 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:231 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:370 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:389 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:406 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:426 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:466 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:483 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-researcher.md:499 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`

### Remediation summary

Pure MD040 cluster — 18 fences need language tags. Executor must read each fence's content to pick the right tag (`text`, `bash`, `json`, `yaml`, `markdown`, `python`). **Effort: small** (mechanical but requires inspection of each block).

---

## src/superclaude/agents/rf-task-builder.md

**Total violations: 21** (MD040×14, MD013×7)

### MD040 (fenced-code-language)

- `src/superclaude/agents/rf-task-builder.md:94 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:110 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:132 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:150 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:184 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:219 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:232 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:260 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:345 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:453 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:475 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:490 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:505 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-builder.md:521 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`

### MD013 (line-length, expected ≤500)

- `src/superclaude/agents/rf-task-builder.md:372:501 MD013/line-length Line length [Expected: 500; Actual: 956]`
- `src/superclaude/agents/rf-task-builder.md:384:501 MD013/line-length Line length [Expected: 500; Actual: 907]`
- `src/superclaude/agents/rf-task-builder.md:386:501 MD013/line-length Line length [Expected: 500; Actual: 661]`
- `src/superclaude/agents/rf-task-builder.md:429:501 MD013/line-length Line length [Expected: 500; Actual: 605]`
- `src/superclaude/agents/rf-task-builder.md:431:501 MD013/line-length Line length [Expected: 500; Actual: 566]`
- `src/superclaude/agents/rf-task-builder.md:558:501 MD013/line-length Line length [Expected: 500; Actual: 804]`
- `src/superclaude/agents/rf-task-builder.md:559:501 MD013/line-length Line length [Expected: 500; Actual: 1232]`

### Remediation summary

Mixed MD040 + MD013. The 14 MD040 fences each need a language tag. The 7 MD013 lines are long enough (566-1232 chars) that they are likely embedded JSON/example blocks — verify whether they live inside an already-fenced code block (which would suppress MD013) or are prose. If prose, reflow; if inside a code block, the fix is usually wrapping the parent in a fence with appropriate language so MD013 ignores it. **Effort: small-to-medium** (MD040 trivial; MD013 needs context inspection).

---

## src/superclaude/agents/rf-task-executor.md

**Total violations: 17** (MD040×16, MD013×1)

### MD040 (fenced-code-language)

- `src/superclaude/agents/rf-task-executor.md:69 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:84 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:99 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:112 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:126 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:137 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:173 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:186 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:192 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:217 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:231 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:248 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:287 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:300 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:310 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`
- `src/superclaude/agents/rf-task-executor.md:334 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]`

### MD013 (line-length, expected ≤500)

- `src/superclaude/agents/rf-task-executor.md:356:501 MD013/line-length Line length [Expected: 500; Actual: 813]`

### Remediation summary

Heavy MD040 (16) + 1 MD013. Same pattern as rf-task-researcher — inspect each fence and add the right language tag. Single MD013 at line 356 is 813 chars — probably a long sample-output block. **Effort: small.**

---

## src/superclaude/agents/rf-assembler.md

**Total violations: 2** (MD040×2)

### MD040 (fenced-code-language)

- `src/superclaude/agents/rf-assembler.md:173 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "   ```"]`
- `src/superclaude/agents/rf-assembler.md:261 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "   ```"]`

### Remediation summary

Two MD040 fences, both indented (3 leading spaces, suggesting nested-list code blocks). Add language tags. **Effort: trivial.**

---

## src/superclaude/agents/rf-analyst.md

**Total violations: 7** (MD024×5, MD040×1, MD013×1)

### MD013 (line-length, expected ≤500)

- `src/superclaude/agents/rf-analyst.md:74:501 MD013/line-length Line length [Expected: 500; Actual: 768]`

### MD024 (no-duplicate-heading)

- `src/superclaude/agents/rf-analyst.md:224 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Output Format"]`
- `src/superclaude/agents/rf-analyst.md:259 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Process"]`
- `src/superclaude/agents/rf-analyst.md:268 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Output Format"]`
- `src/superclaude/agents/rf-analyst.md:314 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Process"]`
- `src/superclaude/agents/rf-analyst.md:330 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Process"]`

### MD040 (fenced-code-language)

- `src/superclaude/agents/rf-analyst.md:397 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "   ```"]`

### Remediation summary

Mixed-rule small batch. MD024 dominates (5 dupes of `### Output Format` / `### Process`) — these repeat across multiple agent role sections and need disambiguation (e.g., scope the heading by role name or upgrade/demote). The MD024 fix likely requires preserving the section semantics so adjusting headings to `### Process (Role A)` etc. is preferable to renaming-by-rote. **Effort: small** (5 disambiguations + 1 fence + 1 long-line).

---

## src/superclaude/agents/rf-qa.md

**Total violations: 22** (MD029×12, MD013×6, MD024×3, MD040×1)

### MD013 (line-length, expected ≤500)

- `src/superclaude/agents/rf-qa.md:82:501 MD013/line-length Line length [Expected: 500; Actual: 757]`
- `src/superclaude/agents/rf-qa.md:312:501 MD013/line-length Line length [Expected: 500; Actual: 537]`
- `src/superclaude/agents/rf-qa.md:325:501 MD013/line-length Line length [Expected: 500; Actual: 517]`
- `src/superclaude/agents/rf-qa.md:337:501 MD013/line-length Line length [Expected: 500; Actual: 1441]`
- `src/superclaude/agents/rf-qa.md:339:501 MD013/line-length Line length [Expected: 500; Actual: 887]`
- `src/superclaude/agents/rf-qa.md:370:501 MD013/line-length Line length [Expected: 500; Actual: 536]`

### MD024 (no-duplicate-heading)

- `src/superclaude/agents/rf-qa.md:180 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa.md:251 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa.md:296 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`

### MD029 (ol-prefix, expected ordered list numbering 1/2/3)

- `src/superclaude/agents/rf-qa.md:275:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 16; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:276:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 17; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:277:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 18; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:278:1 MD029/ol-prefix Ordered list item prefix [Expected: 4; Actual: 19; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:325:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 21; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:327:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 22; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:329:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 23; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:331:1 MD029/ol-prefix Ordered list item prefix [Expected: 4; Actual: 24; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:333:1 MD029/ol-prefix Ordered list item prefix [Expected: 5; Actual: 25; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:335:1 MD029/ol-prefix Ordered list item prefix [Expected: 6; Actual: 26; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:337:1 MD029/ol-prefix Ordered list item prefix [Expected: 7; Actual: 27; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa.md:339:1 MD029/ol-prefix Ordered list item prefix [Expected: 8; Actual: 28; Style: 1/2/3]`

### MD040 (fenced-code-language)

- `src/superclaude/agents/rf-qa.md:428 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "   ```"]`

### Remediation summary

Mixed four-rule profile. MD029 dominant (12 items, continuation-numbered lists 16-19, 21-28 that should restart at 1) — fix is to renumber sub-lists to 1/2/3 style OR break into separate lists with blank-line separators. MD024 (3 repeats of `### What You Verify`) needs scoping. MD013 (6 long lines) and MD040 (1 fence). Note lines 325, 337, 339 have **both** MD013 and MD029 stacked — those edits must coordinate. **Effort: medium** (renumbering ordered lists with intent preservation is non-trivial).

---

## src/superclaude/agents/rf-qa-qualitative.md

**Total violations: 131** (MD029×67, MD024×29, MD036×24, MD013×10, MD040×1)

### MD013 (line-length, expected ≤500)

- `src/superclaude/agents/rf-qa-qualitative.md:83:501 MD013/line-length Line length [Expected: 500; Actual: 656]`
- `src/superclaude/agents/rf-qa-qualitative.md:106:501 MD013/line-length Line length [Expected: 500; Actual: 580]`
- `src/superclaude/agents/rf-qa-qualitative.md:579:501 MD013/line-length Line length [Expected: 500; Actual: 1094]`
- `src/superclaude/agents/rf-qa-qualitative.md:580:501 MD013/line-length Line length [Expected: 500; Actual: 758]`
- `src/superclaude/agents/rf-qa-qualitative.md:581:501 MD013/line-length Line length [Expected: 500; Actual: 733]`
- `src/superclaude/agents/rf-qa-qualitative.md:582:501 MD013/line-length Line length [Expected: 500; Actual: 945]`
- `src/superclaude/agents/rf-qa-qualitative.md:583:501 MD013/line-length Line length [Expected: 500; Actual: 1050]`
- `src/superclaude/agents/rf-qa-qualitative.md:589:501 MD013/line-length Line length [Expected: 500; Actual: 580]`
- `src/superclaude/agents/rf-qa-qualitative.md:591:501 MD013/line-length Line length [Expected: 500; Actual: 871]`
- `src/superclaude/agents/rf-qa-qualitative.md:914:501 MD013/line-length Line length [Expected: 500; Actual: 1219]`

### MD024 (no-duplicate-heading)

- `src/superclaude/agents/rf-qa-qualitative.md:233 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa-qualitative.md:263 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Self-Audit (MANDATORY befo..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:272 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Verdict"]`
- `src/superclaude/agents/rf-qa-qualitative.md:284 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa-qualitative.md:328 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Severity Ratings"]`
- `src/superclaude/agents/rf-qa-qualitative.md:334 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Self-Audit (MANDATORY befo..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:343 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Verdict"]`
- `src/superclaude/agents/rf-qa-qualitative.md:355 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa-qualitative.md:361 MD024/no-duplicate-heading Multiple headings with the same content [Context: "#### Checklist (12 items)"]`
- `src/superclaude/agents/rf-qa-qualitative.md:395 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Severity Ratings"]`
- `src/superclaude/agents/rf-qa-qualitative.md:401 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Self-Audit (MANDATORY befo..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:410 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Verdict"]`
- `src/superclaude/agents/rf-qa-qualitative.md:422 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa-qualitative.md:428 MD024/no-duplicate-heading Multiple headings with the same content [Context: "#### Checklist (14 items)"]`
- `src/superclaude/agents/rf-qa-qualitative.md:466 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Severity Ratings"]`
- `src/superclaude/agents/rf-qa-qualitative.md:472 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Self-Audit (MANDATORY befo..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:481 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Verdict"]`
- `src/superclaude/agents/rf-qa-qualitative.md:493 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa-qualitative.md:499 MD024/no-duplicate-heading Multiple headings with the same content [Context: "#### Checklist (12 items)"]`
- `src/superclaude/agents/rf-qa-qualitative.md:533 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Severity Ratings"]`
- `src/superclaude/agents/rf-qa-qualitative.md:539 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Self-Audit (MANDATORY befo..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:548 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Verdict"]`
- `src/superclaude/agents/rf-qa-qualitative.md:569 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa-qualitative.md:650 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Severity Ratings"]`
- `src/superclaude/agents/rf-qa-qualitative.md:656 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Self-Audit (MANDATORY befo..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:665 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Verdict"]`
- `src/superclaude/agents/rf-qa-qualitative.md:681 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### What You Verify"]`
- `src/superclaude/agents/rf-qa-qualitative.md:694 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Self-Audit (MANDATORY befo..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:703 MD024/no-duplicate-heading Multiple headings with the same content [Context: "### Verdict"]`

### MD029 (ol-prefix, expected ordered list numbering 1/2/3)

- `src/superclaude/agents/rf-qa-qualitative.md:162:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 4; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:164:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 5; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:166:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 6; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:168:1 MD029/ol-prefix Ordered list item prefix [Expected: 4; Actual: 7; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:170:1 MD029/ol-prefix Ordered list item prefix [Expected: 5; Actual: 8; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:172:1 MD029/ol-prefix Ordered list item prefix [Expected: 6; Actual: 9; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:174:1 MD029/ol-prefix Ordered list item prefix [Expected: 7; Actual: 10; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:178:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 11; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:180:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 12; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:182:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 13; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:184:1 MD029/ol-prefix Ordered list item prefix [Expected: 4; Actual: 14; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:186:1 MD029/ol-prefix Ordered list item prefix [Expected: 5; Actual: 15; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:190:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 16; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:192:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 17; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:194:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 18; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:196:1 MD029/ol-prefix Ordered list item prefix [Expected: 4; Actual: 19; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:198:1 MD029/ol-prefix Ordered list item prefix [Expected: 5; Actual: 20; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:200:1 MD029/ol-prefix Ordered list item prefix [Expected: 6; Actual: 21; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:202:1 MD029/ol-prefix Ordered list item prefix [Expected: 7; Actual: 22; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:204:1 MD029/ol-prefix Ordered list item prefix [Expected: 8; Actual: 23; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:304:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 5; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:306:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 6; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:308:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 7; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:310:1 MD029/ol-prefix Ordered list item prefix [Expected: 4; Actual: 8; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:314:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 9; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:316:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 10; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:318:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 11; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:322:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 12; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:324:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 13; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:326:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 14; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:375:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 5; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:377:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 6; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:379:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 7; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:383:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 8; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:385:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 9; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:387:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 10; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:391:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 11; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:393:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 12; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:444:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 6; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:446:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 7; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:448:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 8; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:452:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 9; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:454:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 10; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:456:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 11; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:460:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 12; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:462:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 13; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:464:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 14; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:513:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 5; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:515:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 6; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:517:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 7; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:521:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 8; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:523:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 9; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:525:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 10; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:529:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 11; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:531:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 12; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:605:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 4; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:607:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 5; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:609:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 6; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:613:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 7; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:615:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 8; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:619:1 MD029/ol-prefix Ordered list item prefix [Expected: 1; Actual: 9; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:621:1 MD029/ol-prefix Ordered list item prefix [Expected: 2; Actual: 10; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:623:1 MD029/ol-prefix Ordered list item prefix [Expected: 3; Actual: 11; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:625:1 MD029/ol-prefix Ordered list item prefix [Expected: 4; Actual: 12; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:626:1 MD029/ol-prefix Ordered list item prefix [Expected: 5; Actual: 13; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:627:1 MD029/ol-prefix Ordered list item prefix [Expected: 6; Actual: 14; Style: 1/2/3]`
- `src/superclaude/agents/rf-qa-qualitative.md:628:1 MD029/ol-prefix Ordered list item prefix [Expected: 7; Actual: 15; Style: 1/2/3]`

### MD036 (no-emphasis-as-heading)

- `src/superclaude/agents/rf-qa-qualitative.md:141 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Scope Appropriateness (Feature..."]`
- `src/superclaude/agents/rf-qa-qualitative.md:160 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Content Quality"]`
- `src/superclaude/agents/rf-qa-qualitative.md:176 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Logical Consistency"]`
- `src/superclaude/agents/rf-qa-qualitative.md:188 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Red Flags"]`
- `src/superclaude/agents/rf-qa-qualitative.md:292 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "PRD-to-TDD Fidelity"]`
- `src/superclaude/agents/rf-qa-qualitative.md:302 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Internal Consistency"]`
- `src/superclaude/agents/rf-qa-qualitative.md:312 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Specificity and Actionability"]`
- `src/superclaude/agents/rf-qa-qualitative.md:320 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Red Flags"]`
- `src/superclaude/agents/rf-qa-qualitative.md:363 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Code-to-Document Fidelity"]`
- `src/superclaude/agents/rf-qa-qualitative.md:373 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Structural Accuracy"]`
- `src/superclaude/agents/rf-qa-qualitative.md:381 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Completeness"]`
- `src/superclaude/agents/rf-qa-qualitative.md:389 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Red Flags"]`
- `src/superclaude/agents/rf-qa-qualitative.md:430 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Procedural Correctness"]`
- `src/superclaude/agents/rf-qa-qualitative.md:442 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Environment and Configuration"]`
- `src/superclaude/agents/rf-qa-qualitative.md:450 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Monitoring and Recovery"]`
- `src/superclaude/agents/rf-qa-qualitative.md:458 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Operational Hygiene"]`
- `src/superclaude/agents/rf-qa-qualitative.md:501 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Getting Started Experience"]`
- `src/superclaude/agents/rf-qa-qualitative.md:511 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Navigation and Links"]`
- `src/superclaude/agents/rf-qa-qualitative.md:519 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Audience Appropriateness"]`
- `src/superclaude/agents/rf-qa-qualitative.md:527 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Completeness and Freshness"]`
- `src/superclaude/agents/rf-qa-qualitative.md:595 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Operational Simulation"]`
- `src/superclaude/agents/rf-qa-qualitative.md:603 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Code Compatibility"]`
- `src/superclaude/agents/rf-qa-qualitative.md:611 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Test and Verification Quality"]`
- `src/superclaude/agents/rf-qa-qualitative.md:617 MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Failure Mode Analysis"]`

### MD040 (fenced-code-language)

- `src/superclaude/agents/rf-qa-qualitative.md:833 MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "   ```"]`

### Remediation summary

**Largest and most complex file by far** — 131 violations across all 5 rules. Dominant rules: MD029 (67) + MD024 (29) + MD036 (24). The file appears to be structured as repeated role-section templates (`### What You Verify` / `### Severity Ratings` / `### Self-Audit (MANDATORY...)` / `### Verdict` recur ~5-6 times) — meaning the MD024 fix needs systematic disambiguation by role (e.g., per-section scoping via heading prefix or anchor IDs). MD029 violations cluster around long ordered lists that continue numbering across emphasized "headings" (line numbers like 162→204, 304→326, 375→393, 444→464, 513→531, 605→628) — restructuring these likely involves the SAME edits that fix the MD036 emphasis-as-heading issues (converting `**Section**` to `#### Section` will naturally reset the OL numbering). **Effort: large** (this file accounts for 56% of total violations; coordinated MD036+MD029 edits across ~7 sections; MD024 disambiguation across 29 duplicated headings).

---

## Summary

### Per-file totals (cross-checked against raw output)

| File | Total | MD040 | MD036 | MD024 | MD029 | MD013 |
|---|---|---|---|---|---|---|
| deep-research.md | 1 | 1 | - | - | - | - |
| deep-research-agent.md | 15 | - | 15 | - | - | - |
| rf-task-researcher.md | 18 | 18 | - | - | - | - |
| rf-task-builder.md | 21 | 14 | - | - | - | 7 |
| rf-task-executor.md | 17 | 16 | - | - | - | 1 |
| rf-assembler.md | 2 | 2 | - | - | - | - |
| rf-analyst.md | 7 | 1 | - | 5 | - | 1 |
| rf-qa.md | 22 | 1 | - | 3 | 12 | 6 |
| rf-qa-qualitative.md | 131 | 1 | 24 | 29 | 67 | 10 |
| **Grand total** | **234** | **54** | **39** | **37** | **79** | **25** |

### Cross-check

- Per-file totals sum: 1+15+18+21+17+2+7+22+131 = **234** OK
- Per-rule totals sum: 54+39+37+79+25 = **234** OK
- Matches the BUILD_REQUEST headline figure exactly.

### Effort tiering (for Phase 2 sequencing recommendation)

| Tier | Files | Rationale |
|---|---|---|
| **Trivial** (<=2 violations) | deep-research.md, rf-assembler.md | Single-rule, <=2 edits |
| **Small** (single-rule cluster, 7-18 violations) | deep-research-agent.md (MD036x15), rf-task-researcher.md (MD040x18), rf-analyst.md (mixed-7), rf-task-executor.md (MD040x16 + 1 MD013) | Mechanical with light inspection |
| **Small-medium** (mixed rules, ~20 violations) | rf-task-builder.md (MD040x14 + MD013x7) | Two rules, MD013 needs context inspection |
| **Medium** | rf-qa.md (22 violations across 4 rules, including stacked MD013+MD029 at lines 325/337/339) | Coordinated edits required |
| **Large** | rf-qa-qualitative.md (131 violations, 5 rules, 7 repeated role sections) | Bulk of effort; coordinated MD036->MD029 restructuring |

### Key observations for the task builder

1. **rf-qa-qualitative.md alone = 56% of all violations.** Phase 2 should likely allocate its own dedicated item with multi-step sub-checklist (one per role-section, ~6 sections).
2. **MD036 -> MD029 cascade:** in rf-qa-qualitative.md, the emphasis-as-heading clusters (e.g., line 160 `**Content Quality**` followed by ordered list at lines 162-174 numbered 4-10) are likely the *same* structural defect. Converting `**Foo**` to `#### Foo` (MD036 fix) inserts a heading boundary, which restarts the OL count (MD029 fix). Researcher-2 will confirm the convert-vs-preserve classification.
3. **MD013 inside code fences:** several MD013 violations (e.g., rf-qa-qualitative.md lines 579-583, 914) sit in clusters that look like long JSON/example blocks. If they live inside a fence, MD040+language-tag may already suppress MD013; verify before reflowing prose.
4. **MD024 systematic duplication:** rf-qa-qualitative.md has 6+ recurrences of `### What You Verify`, `### Verdict`, `### Self-Audit`, `### Severity Ratings` — clearly a templated role-block. Fix pattern: prefix with role name OR demote inner duplicates to a deeper level.

**Status:** Complete
