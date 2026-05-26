# rf-task-executor Tavily Refactor — Review

**Target file:** `/config/workspace/IronClaude/src/superclaude/agents/rf-task-executor.md`
**Source proposal:** `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-task-executor-tavily-refactor.md`
**Option applied:** Option A (recommended) — keep WebFetch/WebSearch, add Tavily entries + Critical Rule 7
**Verification method:** Re-Read of edited file (lines 1-373)

---

## Acceptance Criteria (7)

### 1. Frontmatter `tools:` includes both Tavily entries AND both WebFetch/WebSearch still present — **PASS**

Re-Read confirms lines 15-18 of edited file:

```
  - mcp__tavily__tavily-search
  - mcp__tavily__tavily-extract
  - WebFetch
  - WebSearch
```

All four tools present.

### 2. Tavily entries precede WebFetch/WebSearch — **PASS**

Line ordering: `mcp__tavily__tavily-search` (L15) → `mcp__tavily__tavily-extract` (L16) → `WebFetch` (L17) → `WebSearch` (L18). Tavily strictly precedes both legacy web tools.

### 3. "Critical Rules" contains new rule 7 titled "Tavily-first for any web operation" with "protocol violation" framing — **PASS**

Line 353: `7. **Tavily-first for any web operation** - ...` and the rule's final sentence reads: `Silently using \`WebSearch\` / \`WebFetch\` when Tavily is available is a protocol violation.`

Numbering is sequential after existing rule 6 (BROADCAST COMPLETION).

### 4. New rule explicitly names web operations as NOT part of documented workflow — defensive guardrail framing — **PASS**

Line 353 opens: `Web search and web fetch are NOT part of your documented workflow. If a recovery scenario forces you to consult the web...` This is the defensive guardrail framing required by the proposal (matches the reflection-note framing about safety net for off-script behavior).

### 5. At least three explicit fallback conditions enumerated — **PASS**

Line 353 enumerates three conditions verbatim:

- (a) the Tavily tool is not loaded / unavailable
- (b) Tavily returns a tool-level error after one retry
- (c) Tavily returns an explicit rate-limit signal

All three present, parenthetically labeled, matching proposal language.

### 6. "What NOT To Do" contains bullet pointing back to new Critical Rule — **PASS**

Line 363: `- Do NOT use \`WebSearch\` / \`WebFetch\` as a primary web tool — Tavily-first per Critical Rule 7.`

Explicit back-reference to "Critical Rule 7" present.

### 7. No new workflow steps added; primary loop untouched — **PASS**

Re-Read confirms the workflow section (lines 63-206) is unchanged: Step 1 Receive Task → Step 2 Validate → Step 3 Claim → Step 4 Signal Start → Step 5 Execute → Step 6 Monitor → Step 7 Report Completion. No new steps inserted. The Step 5 inner "CRITICAL RULES" block (lines 155-159) is also untouched. Edits are localized to (a) frontmatter tools list, (b) new entry appended to top-level Critical Rules list, (c) new bullet appended to What NOT To Do list.

---

## Provenance log format check — **PASS**

Required format: `web-lookup: provider=<tavily|WebSearch reason=...>`

- Present in new Critical Rule 7 (line 353): `Log the provider in your \`EXECUTION_PROGRESS\` or \`EXECUTION_ERROR\` message using the format: \`web-lookup: provider=<tavily|WebSearch reason=...>\`.`
- Rule explicitly names `EXECUTION_PROGRESS` and `EXECUTION_ERROR` as the message types that should carry the log line (satisfies the proposal's minimal requirement: "the rule states which message types should carry it").

---

## Anomalies

None. All three Edit operations applied cleanly with no unrelated diff drift. The executor's defensive-guardrail framing (rule is acknowledged to govern off-script behavior, not workflow steps) is preserved verbatim from the proposal.

**Overall Verdict:** PASS
