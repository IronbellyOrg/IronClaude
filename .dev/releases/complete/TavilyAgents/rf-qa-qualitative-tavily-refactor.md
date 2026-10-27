# Refactor: rf-qa-qualitative → Tavily-first

## Current state

**File:** `/config/workspace/IronClaude/src/superclaude/agents/rf-qa-qualitative.md`

**Frontmatter `tools:` (lines 6-30)** — web tools currently registered:

```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch          # line 13 — generic web fetch
  - WebSearch         # line 14 — generic web search
  - NotebookEdit
  - Agent
  - Task
  - ...
```

**Body web-research usage:** Like its sibling rf-qa, rf-qa-qualitative is a verifier — its philosophy (line 37) is to read documents "as a product manager, engineering lead, and stakeholder would" and find errors by adversarial reading. The checklists across all phases (prd-qualitative, tdd-qualitative, tech-ref-qualitative, ops-guide-qualitative, readme-qualitative, report-qualitative, task-qualitative, doc-qualitative, fix-cycle) are dominated by Read / Grep / Glob against local files plus cross-section reasoning. The single explicit external-lookup touchpoint is in the **Research Report Qualitative Review** phase, checklist item 7 (line 220):

> 7. **External research is relevant** — Do the web research findings actually inform the recommendation? Or are they padding?

This item **evaluates whether upstream-cited web research is relevant**, not whether the agent itself fetches new web content. So as with rf-qa, WebFetch/WebSearch are declared-but-unused in practice — there is no documented order, no fallback logic, no detection condition.

A secondary potential trigger: report-qualitative item 10 ("Evidence trail is complete") and tech-ref-qualitative item 7 ("Dependency versions match actual usage") could plausibly motivate spot-checking a vendor docs page or PyPI release, but the agent body does not prescribe this and the verification is normally done via local files (`requirements.txt`, `package.json`, `docker-compose.yml`).

**Current "pattern":** WebFetch/WebSearch are inherited capacity. No phase, checklist item, or self-audit step invokes them.

## Proposed refactor

### Frontmatter edits (lines 6-30)

**Before:**
```yaml
  - WebFetch
  - WebSearch
```

**After:**
```yaml
  - mcp__tavily__tavily-search    # PRIMARY web search (Tavily MCP first)
  - mcp__tavily__tavily-extract   # PRIMARY web fetch (Tavily MCP first)
  - WebFetch                      # FALLBACK only — when Tavily MCP unavailable
  - WebSearch                     # FALLBACK only — when Tavily MCP unavailable
```

Preserve relative ordering (Tavily lines BEFORE WebFetch/WebSearch).

### Body edits

**Insert a new `## Web Research Tooling (Tavily-first)` section after the Verification Principles block (after line 97 `---` fence, before the first QA Phase section at line 100).** Siting it at this scope ensures it governs every QA phase below it (prd-qualitative through doc-qualitative and fix-cycle).

Suggested wording:

> ## Web Research Tooling (Tavily-first)
>
> Most qualitative QA verification is local-file-bound — reading the document under review, the source PRD/TDD/research files, and the cited code surfaces. However, certain checks legitimately require external lookup: confirming a vendor doc page or an external standard says what the document claims it says (relevant to report-qualitative item 7 "external research is relevant"; tech-ref-qualitative item 7 "dependency versions"; ops-guide-qualitative item 9 "monitoring covers failure modes"); spot-checking that an external link in a README resolves (readme-qualitative item 5).
>
> When such external lookup is required, you MUST use Tavily MCP first.
>
> **Precedence:**
> 1. `mcp__tavily__tavily-search` — for queries / discovery.
> 2. `mcp__tavily__tavily-extract` — for fetching a specific URL's content.
> 3. **Fallback only:** `WebSearch` / `WebFetch` — and only when Tavily MCP is unavailable (see detection condition below).
>
> **Detection condition for "Tavily unavailable"** (any of):
> - The `mcp__tavily__tavily-search` or `mcp__tavily__tavily-extract` tool is not present in your runtime tool list this session (server not loaded).
> - The Tavily call returns a structured server error (e.g., 5xx, connection refused, "server not configured").
> - The Tavily call returns a rate-limit / quota error (HTTP 429 or equivalent payload).
>
> If any of these fire on a single call, record the failure mode in your QA report's Tool-engagement summary (e.g., `tavily_extract: 1 attempt, fell back to WebFetch (server-not-loaded)`), then issue the equivalent WebSearch/WebFetch call. **Silent fallback is forbidden** — the fallback condition and reason MUST appear in the report.
>
> **What this does NOT change:** rf-qa-qualitative remains adversarial-reader-first. Web research is supplementary; it never replaces reading the actual document or the actual source files. The five Adversarial Axes (AX-1..AX-5) and the closed-set Axis-column vocabulary remain unchanged.

**Augment the Self-Audit block (lines 184-188 and repeated at 232-236, 300-304, 364-368, 432-436, 496-500, 609-613, 644-648) — add a 4th question to each instance:**

> 4. If any web research was performed during this review, did you attempt Tavily MCP first, and is the tool used (Tavily vs fallback) recorded in your report's Tool-engagement summary?

(Either edit every Self-Audit block individually or — preferred — promote the Self-Audit block to a single "## Self-Audit (applies to every QA phase)" section and link each phase to it. The exact mechanism is an implementation detail; the acceptance criterion is that the Tavily-first audit question appears wherever Self-Audit is invoked.)

**Add a new Critical Rule (after the existing fix-cycle rules around line 677-678):**

> **Tavily-first for any external lookup** — When verifying a claim that requires fetching from the open web (a vendor doc page, an external standard, a third-party API surface, an external link in the document under review), you MUST attempt `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` before falling back to `WebSearch` / `WebFetch`. Silent fallback is a process violation; the fallback condition and reason MUST appear in your QA report.

### Fallback decision flow

```
need external lookup?
  └── tavily tool available in this session?
        ├── NO  → record "tavily-not-loaded" in report, use WebSearch/WebFetch
        └── YES → call mcp__tavily__tavily-search (or -extract)
              ├── success → use result
              ├── 5xx / connection error → record reason, fall back to WebSearch/WebFetch
              ├── 429 rate-limit → record reason, fall back to WebSearch/WebFetch
              └── auth/config error → record reason, fall back to WebSearch/WebFetch
```

## Acceptance criteria

- [ ] Frontmatter `tools:` block lists `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` BEFORE `WebFetch` and `WebSearch`.
- [ ] `WebFetch` and `WebSearch` remain in the `tools:` list (fallback role preserved).
- [ ] A new `## Web Research Tooling (Tavily-first)` body section exists at a scope that governs every QA phase (prd-qualitative through doc-qualitative and fix-cycle).
- [ ] The detection condition for "Tavily unavailable" enumerates: (1) tool not present in runtime tool list, (2) server error / connection refused, (3) rate-limit / quota error.
- [ ] Every Self-Audit block (or a single promoted Self-Audit section) includes a Tavily-first audit question requiring that the chosen tool (Tavily vs fallback) be recorded in the report's Tool-engagement summary.
- [ ] A new Critical Rule under the fix-cycle section codifies the Tavily-first requirement and bans silent fallback.
- [ ] The five Adversarial Axes (AX-1..AX-5) and the closed-set `{AX-1..AX-5, none}` Axis-column vocabulary for task-qualitative are unchanged.
- [ ] No existing qualitative checklist item is weakened or removed; the "Ban N/A" principle (line 94) and "Exhaustive verification" principle (line 95) remain intact.
- [ ] `make verify-sync` passes after editing `src/superclaude/agents/rf-qa-qualitative.md` and running `make sync-dev`.

## Reflection notes

**Adversarial validation against original intent:**

1. **Does Tavily-first contradict the "Ban N/A" / "Exhaustive verification" principles?** No — these principles govern *what* must be verified, not *which tool* performs an external fetch. Tavily-first only constrains tool precedence in the residual case where external lookup is required. Local-file verification (Read / Grep / Glob) — which is where Exhaustive verification primarily applies — is unchanged.

2. **Risk of qualitative-QA never invoking web research at all.** Across the eight QA phases, only report-qualitative (item 7), tech-ref-qualitative (item 7), ops-guide-qualitative (item 9), and readme-qualitative (item 5) plausibly motivate a web call. The other phases — prd-qualitative, tdd-qualitative, task-qualitative, doc-qualitative, fix-cycle — almost never need it. As with rf-qa, declaring web tools that may go unused is normal capacity declaration; the Tavily-first rule fires only when web research IS performed.

3. **Interaction with the canonical Axis-column vocabulary (lines 538-544).** The Tavily-first refactor adds NO new axis. The closed set `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` stays intact. If a Tavily-fallback decision surfaces a finding (e.g., an external standard's content contradicts a document claim), the finding is annotated with the most-specific existing axis (typically AX-1 drift or AX-2 contradictions, depending on whether the doc misquoted vs misaligned).

4. **drift-axis-inactive semantics unchanged.** The `drift-axis-inactive` Summary-block annotation (lines 532, 544) is orthogonal to web-tool selection — drift baseline depends on BUILD_REQUEST.GOAL availability, not on Tavily presence.

5. **Partition-instance compatibility.** Parallel qualitative-QA partitions (lines 50-79) each get their own tool list; Tavily-first applies identically per-instance. DNSP synthetic-finding emission (line 79) is not affected — synthetics arise from partition failure, not from tool-choice failure.

6. **Gap surfaced by reflection — Self-Audit duplication.** The Self-Audit block is currently duplicated across seven phases (lines 184, 232, 300, 364, 432, 496, 609, 644). Adding the Tavily-first question to each one individually risks drift between copies as future edits land. The cleanest refactor is to promote Self-Audit to a single canonical section and replace each phase-local copy with a reference. This is a separate hygiene improvement that pairs naturally with the Tavily-first edit but is not strictly required by the constraint. The acceptance criterion above accepts either approach.

7. **No interaction with FR-CONV.5 monotonicity / regression halt-guards** (these live in rf-qa, not rf-qa-qualitative). The fix-cycle rules in rf-qa-qualitative (lines 675-678) keep their 3-cycle cap and "issue count should decrease" guidance unchanged.
