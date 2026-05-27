# Refactor: rf-task-executor → Tavily-first

## Current state

**Frontmatter `tools:` (lines 8-27)** lists `WebFetch` (line 15) and `WebSearch` (line 16). **Tavily MCP tools are NOT in the list.**

**Body workflow** (lines 30-368) was read end-to-end. Findings:

- The documented workflow is **entirely local**: receive `TASK_READY` from builder → validate task file → claim task → run `bash .gfdoc/scripts/automated_qa_workflow.sh <task_file> <batch_size> <max_iterations>` → monitor → report.
- There is **no body reference** to `WebSearch`, `WebFetch`, Tavily, or any external lookup — neither as a documented step, nor as an escalation path, nor as a "What NOT To Do" prohibition.
- The "Critical Rules" (lines 343-359) and "What NOT To Do" (lines 352-359) say nothing about web operations.
- The "Handling Issues" section (lines 208-257) routes QA failures into the correction loop and execution errors to `rf-team-lead`; no path involves the executor going to the web for context.

**Current pattern**: `WebSearch` and `WebFetch` are **listed in frontmatter but never invoked by any documented workflow.** They are latent / dormant capabilities. The executor's job, as written, is to drive a shell script and report — no external research surface area.

This puts the executor in a gray zone for this refactor: there is no *current* Tavily-first behavior to enforce because there is no *current* web behavior at all. But because the tools are still in the frontmatter, an executor under context pressure could improvise a `WebSearch:` call to investigate (say) an obscure error from `automated_qa_workflow.sh` — and that improvisation would today go straight to WebSearch with no Tavily mention anywhere in the agent's spec.

## Proposed refactor

This is a **defensive / consistency refactor**, not a behavior change. Goal: bring executor's frontmatter and rule set into consistency with researcher and builder so that *if* the executor ever does step outside its lane and consult the web, the same Tavily-first contract applies.

Two options were considered. The recommendation is Option A.

### Option A (recommended): keep web tools in frontmatter, add Tavily-first rule

**Frontmatter `tools:` edit** — same shape as researcher / builder:

```diff
 tools:
   - Read
   - Write
   - Edit
   - Bash
   - Glob
   - Grep
+  - mcp__tavily__tavily-search
+  - mcp__tavily__tavily-extract
   - WebFetch
   - WebSearch
   - NotebookEdit
   ...
```

**Body edit — add a single short rule to "Critical Rules" (after current rule 6, lines 343-350):**

> 7. **Tavily-first for any web operation** — Web search and web fetch are NOT part of your documented workflow. If a recovery scenario forces you to consult the web (e.g., investigating an obscure `automated_qa_workflow.sh` error before reporting `EXECUTION_ERROR`), the call MUST go through `mcp__tavily__tavily-search` or `mcp__tavily__tavily-extract` first. `WebSearch` / `WebFetch` are fallbacks; fall back ONLY when Tavily is unavailable (tool not loaded), returns a tool-level error after one retry, or returns an explicit rate-limit signal. Log the provider in your `EXECUTION_PROGRESS` or `EXECUTION_ERROR` message: `web-lookup: provider=<tavily|WebSearch reason=...>`. Silently using WebSearch when Tavily is available is a protocol violation.

**Body edit — add one bullet to "What NOT To Do" (lines 352-359):**

> - Do NOT use `WebSearch` / `WebFetch` as a primary web tool — Tavily-first per Critical Rule 7.

### Option B (alternative, NOT recommended): remove web tools from frontmatter entirely

Drop `WebFetch` and `WebSearch` from the tools list, and do not add Tavily either. Rationale: executor has no documented use for any of them. **Why not recommended:** it changes the executor's capability surface, which is a behavior change requiring coordination with whoever currently relies on these tools being present (if anyone). Within the scope of "make all three agents Tavily-first," Option A is the lower-risk, higher-consistency move.

## Acceptance criteria

- [ ] Frontmatter `tools:` includes `mcp__tavily__tavily-search` AND `mcp__tavily__tavily-extract`, AND both `WebFetch` and `WebSearch` are still present.
- [ ] Tavily entries precede `WebFetch` / `WebSearch` in the list.
- [ ] "Critical Rules" contains a new rule (numbered 7) titled "Tavily-first for any web operation" (or equivalent) with the phrase "protocol violation" or equivalent strong enforcement.
- [ ] The new rule explicitly names that web operations are NOT part of the documented workflow — i.e., the rule is framed as a defensive guardrail for recovery scenarios, not as a workflow step.
- [ ] At least three explicit fallback conditions are enumerated (tool-missing, tool-error after one retry, rate-limit).
- [ ] "What NOT To Do" contains a bullet pointing back to the new Critical Rule.
- [ ] No new workflow steps are added — the executor's primary loop (validate → claim → run script → report) is untouched.
- [ ] The provenance log format (`web-lookup: provider=<tavily|WebSearch reason=...>`) appears in BOTH the new rule AND is referenced from the EXECUTION_PROGRESS / EXECUTION_ERROR message templates (or, minimally, the rule states which message types should carry it — `EXECUTION_PROGRESS` and `EXECUTION_ERROR`).

## Reflection notes

`/sc:reflect --session --analyze` raised two concerns that I addressed:

1. **"Is this refactor worth doing at all?"** Reflection challenge: if the executor has no documented web behavior, adding a Tavily-first rule could be seen as cargo-culting consistency with the other two agents. Resolved: kept the refactor but reframed it as a **defensive guardrail**, not a workflow change. The framing is explicit ("Web search and web fetch are NOT part of your documented workflow. If a recovery scenario forces you…"). This makes the rule honest about its purpose — it's a safety net for off-script behavior, not a new step. The alternative (Option B: remove the tools entirely) is documented as a real option so a reviewer can pick the more conservative path if they prefer.

2. **"Where does the provenance annotation go in executor's message stream?"** Reflection: builder annotates checklist items (HTML comments); researcher annotates research notes (provenance line). Executor doesn't write either of those — it writes `EXECUTION_*` messages. Tightened: provenance log is carried in `EXECUTION_PROGRESS` or `EXECUTION_ERROR` (whichever message accompanies the web lookup), using a single-line format `web-lookup: provider=<tavily|WebSearch reason=...>` that matches the existing message style. This keeps the audit trail in the executor's natural output medium.

Reflection confirmed the refactor preserves executor's core responsibility (drive `automated_qa_workflow.sh`, report, never interrupt). The rule does not interfere with the "NEVER use timeout" / "NEVER run in background" / "LET IT COMPLETE" rules, and does not add any web operation to the workflow loop. It only constrains the form of any improvised web lookup if one occurs — which, by the rule's own framing, is acknowledged to be off-script.
