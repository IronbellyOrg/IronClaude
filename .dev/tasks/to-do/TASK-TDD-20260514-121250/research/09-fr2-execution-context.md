# Research: FR-CONV.2 (PR-01) Execution Context Header Insertion Points

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**CASE:** D (sc:tasklist has tasklist-wide context block; task-builder has per-item Context field — related but non-conflicting)
**Conflict-register row:** PR-01
**Protected invariant:** evidence-bound-item (per-item Context fields retain file:line citations; header strictly NO file paths)
**Lands:** 2nd of 6 FRs

---

## 1. Verified-Current Insertion Points

PRD §14.1 cites three insertion sites in `src/superclaude/skills/task-builder/SKILL.md`:
`228-238` (Tier Selection), `719` (Execution Overview anchor / BUILD_REQUEST format), and `1409-1485` (Builder Agent Prompt + generated-task-file template). Two of the three exhibit drift from the PRD-cited line numbers; the third matches.

### Site 1 — Tier Selection (PRD cites 228-238; current source: 86-103)

PRD cites `SKILL.md:228-238`, but the **only** `## Tier Selection` header in the current source is at **line 86**. The PRD-cited range (226-240) returns the **template-selection table** (Sub-section A.2), NOT the tier selection. The PRD note in §14.1 also references this drift indirectly (acknowledging ≤3-line drift across the release).

**Verbatim content at the current `## Tier Selection` anchor (lines 86-103):**

```
## Tier Selection

Match the tier to request complexity. **Default to Standard** unless the scope is clearly small (<5 files) or clearly large (20+ files, multiple subsystems).

| Tier | When | Researchers | Web Agents | Purpose |
|------|------|-------------|------------|---------|
| **Quick** | Small scope, <5 relevant files, single concern | 3 | 0 | Fast task file for simple requests |
| **Standard** | Most requests, 5-20 files, moderate complexity | 4-5 | 0-1 | Default — balanced depth and speed |
| **Deep** | Complex scope, 20+ files, multiple subsystems, multi-track | 6-8 | 1-2 | Thorough research for ambitious tasks |

**Tier selection rules:**
- If in doubt, pick Standard
- If the user says "thorough", "comprehensive", or "deep dive" — always Deep
- Only use Quick for genuinely small tasks (<5 files, single concern, no discovery needed)
- If the scope spans multiple subsystems, involves multi-track, or requires significant discovery — always Deep
```

**Verbatim content at PRD-cited range (lines 226-240) — actually a different section (A.2 template selection):**

```
**DEFAULT: Single track.** Only split when independence is clear. **MAXIMUM: 5 tracks.**

**Select MDTM template per track:**

| Signal in the Request | Template |
|-----------------------|----------|
| "Create these files" (known inputs, known outputs) | 01 |
| "Build X with tests" (need to discover, build, then test) | 02 |
| "Document all handlers" (need discovery scan first) | 02 |
| "Create a config file from this spec" (direct transformation) | 01 |
| "Refactor X and verify nothing breaks" (build + test + conditional fix) | 02 |
| When uncertain | **02 (safer)** |

When uncertain | **02 (safer)** |

### A.3: Perform Scope Discovery
```

**Drift verdict:** PRD line citation `228-238` is **STALE**. The PRD likely cites Tier Selection because tier-selection is the natural place to surface "header is mandatory at Tier Standard+, degrades at Tier Quick". The TDD should normalize to current line **86-103** for Tier Selection edits, and treat `226-240` as the A.2 template-selection table edit if a related anchor adjustment is needed.

### Site 2 — Execution Overview Anchor (PRD cites 719; current source: 139 anchor + 715-725 BUILD_REQUEST format)

PRD cites `SKILL.md:719` as an "Execution Overview anchor." The actual `## Execution Overview` header is at **line 139**. Line 719 is **inside** the BUILD_REQUEST format code block introduced at line 715 — specifically the `GOAL:` line.

**Verbatim content at lines 715-725 (BUILD_REQUEST format opening — this is the natural insertion point for prompting the builder to emit the Execution Context header):**

```
**BUILD_REQUEST format for the subagent prompt:**

\`\`\`
Agent:
  subagent_type: "rf-task-builder"
  mode: "bypassPermissions"
  prompt: |
    BUILD_REQUEST:
    ==============
    GOAL: [GOAL — what the task file should accomplish when executed]

    WHY: [WHY — context for why this task is needed]
```

**Verbatim content at `## Execution Overview` anchor (lines 139-148, first stanza):**

```
## Execution Overview

This skill operates in a single stage (Stage A only). Unlike the canonical document skills which have Stage A (create task file) + Stage B (delegate to `/task` for execution), this skill stops after task file creation. The user reviews the task file and executes it with `/task [path]` when ready.

**Stage A — Scope Discovery, Research, Quality Gate, Task File Creation:**
1. Check for an existing task folder or research directory (A.1)
2. Parse the user's request — triage into Scenario A vs B, determine track count (1-5), select MDTM template per track (A.2)
3. Perform scope discovery — map relevant files/directories, plan researcher assignments from 8 topic types (A.3)
4. Write scope discovery results to a structured research notes file with 7 categories (A.4)
5. Review research sufficiency — mandatory self-review gate (A.5)
```

**Drift verdict:** PRD line citation `719` is **STALE-BY-CONTEXT** — line 719 is the `GOAL:` line, which is a natural anchor for instructing the builder how to populate `References:` from GOAL/WHY. The PRD intent appears to be: append "Execution Context header construction guidance" to the BUILD_REQUEST prompt template. The current insertion point is the prompt body spanning roughly lines 715-803 (full BUILD_REQUEST template), not line 719 in isolation.

### Site 3 — Builder Agent Prompt + Generated Task-File Template (PRD cites 1409-1485; current source: 1407-1487, MATCH)

PRD cites `SKILL.md:1409-1485`. Current source has the generated-task-file template at **1407-1487** — a near-perfect match (±2 lines). This is the most accurate of the three PRD citations.

**Verbatim content at lines 1407-1487 (generated MDTM task file template — the canonical structural artifact the builder produces):**

```
This is what the generated MDTM task file looks like — NOT a tech reference document, but the task file that the builder produces:

\`\`\`markdown
---
id: "TASK-RF-YYYYMMDD-HHMMSS"
title: "[Task Title]"
description: "[Brief description of what the task accomplishes]"
status: "🟡 To Do"
type: "🔧 Refactor"  # or 📝 Documentation, ✨ Feature, etc.
priority: "🔼 High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/0[1|2]_mdtm_template_[generic|complex]_task.md"
estimation: "[estimated duration]"
task_type: static
related_docs:
- path: "[relevant file]"
  description: "[why it's relevant]"
tags:
- "[tag1]"
- "[tag2]"
---

# [Task Title]

## Task Overview

[1-2 paragraphs describing what the task accomplishes and why]

## Key Objectives

- [Objective 1]
- [Objective 2]
- [Objective 3]

## Prerequisites & Dependencies

- [Prerequisite 1]
- [Prerequisite 2]

---

## Phase 1: [Phase Name]

- [ ] **1.1 — [Step Title]**
  - **Context**: [What the executor needs to know]
  - **Action**: [Exactly what to do]
  - **Output**: [What gets created/modified]
  - **Verification**: [How to confirm it worked]
  - **Completion gate**: [When this item is done]
```

This is the **primary** insertion point. The `## Execution Context` block must be added to the template between **`## Prerequisites & Dependencies`** (currently ending around line 1448) and **`---` / `## Phase 1`** (line 1449-1450). The generated-task-file YAML frontmatter ends at line 1430; the prose sections (`# Title` / `## Task Overview` / `## Key Objectives` / `## Prerequisites & Dependencies`) run lines 1432-1448; and `## Phase 1` begins at line 1450.

**Insertion verdict:** Per the PRD-mandated structure ("after frontmatter, before checklist"), the `## Execution Context` block belongs **between line 1448 (end of Prerequisites & Dependencies) and line 1449 (`---` separator before Phase 1)** — or alternatively immediately after the frontmatter closing `---` at line 1430 if the spec prefers it ahead of the Task Overview prose. The PRD wording "after frontmatter, before checklist" is satisfied by either placement; the **after Prerequisites** placement is the more natural narrative location and is the recommendation.

---

## 2. Execution Context Header Structure (per PRD §14.1 FR-CONV.2 + §25.1)

The header is a single `## Execution Context` Markdown section containing **exactly 3 labeled lines** (the line ordering is normative for downstream grep verification):

```
## Execution Context

References: <BUILD_REQUEST GOAL summary>; <BUILD_REQUEST WHY summary>; <related-doc IDs from BUILD_REQUEST related_docs>
Source areas: <named modules/packages — STRICTLY NO specific file paths, NO file:line citations>
Key constraints: <top 1-3 invariants pulled verbatim from BUILD_REQUEST>
```

### Field semantics

| Field | Source | Format rule |
|---|---|---|
| `References:` | BUILD_REQUEST `GOAL` + `WHY` + `related_docs.path` IDs | Free prose; doc IDs may appear (e.g. `PRD §14.1`); raw file paths to *source code* are PROHIBITED |
| `Source areas:` | Named modules / packages / subsystems inferred from research scope | Module names only — e.g. `task-builder skill`, `rf-qa agent`, `MDTM templates`. **NO** `src/foo/bar.py` style paths, **NO** `file:line` citations |
| `Key constraints:` | Top 1-3 invariants extracted from BUILD_REQUEST (e.g. "self-contained-item, evidence-bound-item, parallel-research") | Comma-separated invariant names; brevity over completeness |

### Minimal-BUILD_REQUEST degradation (PR-01 failure-mode #2)

When BUILD_REQUEST is minimal (no WHY field, no related_docs, no explicit constraints listed):

```
## Execution Context

References: <GOAL only>
```

`Source areas:` and `Key constraints:` lines are **explicitly omitted** (not blank-but-present) when no source data exists. The header degrades to References-only and remains valid. The TB-Add-7 cross-validator (FR-CONV.1) MUST tolerate this degraded form and only fail when a header is structurally malformed (e.g. has `Source areas:` but its content contradicts what the items reference).

---

## 3. Acceptance Criteria (from PRD §14.1)

**Observable behavior:**
- Generated MDTM task files contain a `## Execution Context` block with **exactly 3 labeled lines** (`References:`, `Source areas:`, `Key constraints:`).
- When BUILD_REQUEST is minimal, the block **degrades to References-only** with WHY/source-area lines explicitly omitted (PR-01 failure-mode #2).
- Header placement is **after frontmatter, before checklist** (i.e. before the first `## Phase N:` section).

**Verification method:**
1. `grep -n "## Execution Context" <generated-task-file>` returns line N (block exists).
2. The next 10 lines after line N contain ≥1 of: `References:` / `Source areas:` / `Key constraints:` (degradation-tolerant: only 1 of 3 required for minimal-BUILD_REQUEST case).
3. `grep -E "src/|/.*:[0-9]+" <header-block-range>` returns **zero hits** — no source-code file paths and no `file:line` citations inside the header.

**Negative criteria:**
- Per-item Context fields elsewhere in the task file **MUST retain** `file:line` citations **OR justified-absence comments** (validated by TB-Add-8 introduced via FR-CONV.1). The header rule does not propagate to items.
- The per-item self-contained 5-field schema (`Context` / `Action` / `Output` / `Verification` / `Completion gate`) **MUST NOT** be altered. The Execution Context header is **additive** — it adds a task-level block, not item-level fields.

---

## 4. Scope-Confinement Rule

The "no specific paths" / "no file:line" rule is **HEADER-ONLY**.

**In scope (header MUST NOT contain):**
- `src/...` paths
- `file:line` style citations (e.g. `SKILL.md:228`)
- Any verbatim source-code identifier with line numbers

**Out of scope (the rule does NOT apply to):**
- Per-item `Context:` fields inside `## Phase N` checklist items — these **MUST** retain `file:line` citations to preserve the **evidence-bound-item** invariant.
- Files under `${TASK_DIR}research/*.md` — these are the verbatim file:line evidence sources; they MUST be unaffected by FR-CONV.2.
- The `related_docs:` frontmatter list — these are *document* IDs/paths, not source-code citations, and remain unaffected.

**INV-015 disposition:** INV-015 (per-item Context citation completeness gap) is **resolved by TB-Add-8** in FR-CONV.1 (a per-item check requiring `file:line` OR justified-absence comment). FR-CONV.2 is **only** the header; it does not touch per-item Context.

---

## 5. Dependencies on Other FRs

**Hard dependency on FR-CONV.1 (PR-06 Structural Gate Additions):**
- **TB-Add-7** (cross-validate that header `Source areas:` reappear as referenced modules in items) MUST be live in rf-qa task-integrity gate before FR-CONV.2 lands. Without TB-Add-7, header drift (header says X, items reference Y — risk K-002) goes uncaught.
- **TB-Add-8** (per-item Context field MUST have `file:line` citation OR justified-absence comment) MUST be live to satisfy the FR-CONV.2 negative-criteria "per-item Context fields retain file:line citations." Without TB-Add-8, the header's scope-confinement rule has no enforcement counterpart at item level.

**Sequencing per PRD §6 / release-spec §4.6:**
- PR-06 (FR-CONV.1, TB-Add-1..8 catalogue) lands **first**.
- PR-01 (FR-CONV.2, this FR) lands **second**.
- The serial sequencing is strict — FR-CONV.2 acceptance criteria reference TB-Add-7 and TB-Add-8 as the validation mechanism.

**Soft dependency on FR-CONV.4 (PR-07 Adversarial Category Naming):**
- TB-Add-7 cross-validation runs at A.10 (rf-qa task-integrity) before A.10.5 (rf-qa-qualitative). No direct content dependency, but the staging gate ordering is fixed.

**No dependency on:** FR-CONV.3 (PR-04 Gate Results Passthrough), FR-CONV.5 (PR-02 Retry Monotonicity), FR-CONV.6 (PR-03 DNSP Synthetic Finding).

---

## 6. Gaps and Questions

**G-1. Line-drift normalization.** PRD cites `SKILL.md:228-238` for Tier Selection but current `## Tier Selection` is at **line 86**. The PRD-cited range hits the A.2 template-selection table instead. **Question:** Does the TDD intend (a) to add Tier Selection guidance for header generation at the actual Tier Selection anchor (line 86), or (b) to add it at the A.2 template-selection anchor (line ~226), or (c) both? Recommendation: (a) — the header should be tier-aware (e.g. mandatory for Standard+, degraded for Quick), and tier-awareness belongs at the Tier Selection anchor.

**G-2. PRD line 719 is mid-code-block.** Line 719 is the `GOAL:` line inside the BUILD_REQUEST format template (which spans 715-803). **Question:** Is the intended edit (a) to append a `EXECUTION_CONTEXT_GUIDANCE:` field to the BUILD_REQUEST template (somewhere in 715-803), or (b) to add a separate "Execution Overview" stanza describing how the builder constructs the header? Recommendation: (a) — add an explicit field in BUILD_REQUEST near `GOAL`/`WHY` that the rf-task-builder agent reads to populate the header.

**G-3. Header placement granularity in the template.** The generated-task-file template (lines 1432-1448) has four prose sections (`Task Overview`, `Key Objectives`, `Prerequisites & Dependencies`) before `Phase 1`. **Question:** Should `## Execution Context` go (a) directly after the frontmatter closing `---` (line 1430, before `# Title`), (b) after `Prerequisites & Dependencies` (line 1448), or (c) after `# Title` and before `## Task Overview`? PRD §14.1 says "after frontmatter, before checklist" — all three options satisfy this. Recommendation: (b) — after Prerequisites & Dependencies, immediately before the `---` separator and `## Phase 1`. This keeps execution-time machine-readable context adjacent to the checklist, separated from human-readable narrative.

**G-4. Minimal-BUILD_REQUEST detection threshold.** PRD §14.1 says degrades to References-only when BUILD_REQUEST is "minimal." **Question:** What is the operational definition of "minimal"? Recommendation: minimal ≡ BUILD_REQUEST has GOAL only (no WHY, no related_docs, no constraints surfacable from research-notes.md).

**G-5. TB-Add-7 grep-pattern source.** The header's `Source areas:` is free-prose module names. **Question:** How does TB-Add-7 deterministically cross-validate that source-areas reappear in items (e.g. "task-builder skill" appearing in item Context fields)? Recommendation: substring match on each comma-separated source-area against the union of all item Context-field text; require ≥1 substring match per source-area. This is best specified in the FR-CONV.1 research file (research/08-fr1-* or similar).

---

## 7. Stale Documentation Found

1. **PRD line 228-238 for Tier Selection.** Current `## Tier Selection` header is at line 86, not 228-238. Drift: +142 lines. Cause: the PRD likely used a pre-restructure version of SKILL.md. **Action:** TDD should record the normalized line `86-103` (Tier Selection) and clarify whether the PRD-cited range `226-240` (A.2 template selection) is also in scope or was a mis-citation. Tag: `[CODE-CONTRADICTED]`.

2. **PRD line 719 = mid-code-block.** Line 719 is the `GOAL:` line inside the BUILD_REQUEST format code block (anchor at line 715). The PRD called this "Execution Overview anchor" but the `## Execution Overview` header is at line 139. **Action:** Treat the citation as "the BUILD_REQUEST template prose, near the GOAL/WHY fields, used to instruct the builder to emit the header." Tag: `[CODE-CONTRADICTED-BY-CONTEXT]` — the line number points into a code block, not a structural anchor.

3. **No staleness in PRD line 1409-1485** (generated task-file template). Current source 1407-1487 matches within ±2 lines. Tag: `[CODE-VERIFIED]`.

4. **No existing `## Execution Context` in sc-tasklist source confirmed.** `grep -rn "## Execution Context"` in `src/superclaude/skills/sc-tasklist/` returns no hits. The PRD's reference to "FINAL-REPORT §7-R2" describing the sc-tasklist mechanism is a behavioral-spec reference, not a code-anchor; this is a documentation/spec convention, not stale code. Tag: `[SPEC-ONLY — NOT IMPLEMENTED IN sc-tasklist SOURCE]`.

---

## 8. Summary

FR-CONV.2 (PR-01) adds a task-level `## Execution Context` header (References / Source areas / Key constraints — exactly 3 labeled lines, with References-only degradation for minimal BUILD_REQUEST) to every generated MDTM task file, with strict header-only "no file paths / no file:line" enforcement and INV-015 resolved by TB-Add-8 at the item level. The three PRD-cited insertion sites exhibit drift: `SKILL.md:228-238` for Tier Selection is **STALE** (current anchor at line 86, with 226-240 actually pointing at A.2 template selection); `SKILL.md:719` is mid-BUILD_REQUEST code block (not the `## Execution Overview` anchor at line 139); only `SKILL.md:1409-1485` (generated task-file template) is accurate within ±2 lines. The TDD must (a) normalize the line citations, (b) clarify whether Tier Selection or A.2 template selection is the intended anchor for tier-aware header policy, and (c) specify the operational definition of "minimal BUILD_REQUEST" for the degradation rule. FR-CONV.2 hard-depends on FR-CONV.1 (TB-Add-7 cross-validator + TB-Add-8 per-item evidence check); scope-confinement preserves the evidence-bound-item invariant by leaving per-item Context fields, research/*.md, and related_docs untouched. The five identified gaps (G-1..G-5) and three staleness findings should drive TDD design decisions before implementation begins.

---

**Status:** Complete
