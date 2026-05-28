# Research: Remediation Pattern Samples (MD036/MD024/MD029)

**Task:** TASK-RF-20260523-234320-markdownlint-remediation
**Researcher:** researcher-2 (Patterns & Conventions)
**Status:** Complete
**Scope:** 3 heavy files — deep-research-agent.md, rf-qa.md, rf-qa-qualitative.md
**Goal:** Establish per-rule convert-vs-preserve playbook for ambiguous markdownlint rules

---

## Violation distribution across 3 sampled files

From `markdownlint-raw-output.txt` filtered to MD036/MD024/MD029 in the 3 target files:

| File | MD036 | MD024 | MD029 |
|---|---|---|---|
| `deep-research-agent.md` | 15 | 0 | 0 |
| `rf-qa.md` | 0 | 3 | 12 |
| `rf-qa-qualitative.md` | 24 | 29 | 67 |

---

## Sample analyses — MD036 (no-emphasis-as-heading)

### Sample 1: `deep-research-agent.md:59` — "Entity Expansion"

**File:line:** `src/superclaude/agents/deep-research-agent.md:59`

Surrounding context (lines 57–69):

```text
### Multi-Hop Reasoning Patterns

**Entity Expansion**

- Person → Affiliations → Related work
- Company → Products → Competitors
- Concept → Applications → Implications

**Temporal Progression**

- Current state → Recent changes → Historical context
```

**Classification:** `convert`

**Justification:** "Entity Expansion" is on its own line, immediately followed by a blank line and a bulleted list it labels. It introduces a parallel structural sibling alongside "Temporal Progression," "Conceptual Deepening," and "Causal Chains" — these four bold blobs are subsections of the `### Multi-Hop Reasoning Patterns` h3. The correct fix is to promote each from `**Foo**` to `#### Foo` so they are real children of the h3 in the document tree.

### Sample 2: `deep-research-agent.md:126` — "Tavily-First Rule (mandatory)"

**File:line:** `src/superclaude/agents/deep-research-agent.md:126`

Surrounding context (lines 124–135):

```text
### Tool Orchestration

**Tavily-First Rule (mandatory)**

All web search and HTML extraction MUST be attempted via Tavily MCP first:

- Search → `mcp__tavily__tavily-search`
- Page extraction → `mcp__tavily__tavily-extract`

`WebSearch` and `WebFetch` are **fallback tools only**. They are used solely when Tavily MCP is unavailable (see Fallback Policy below). Do not invoke `WebSearch` or `WebFetch` while Tavily MCP is operational.

**Search Strategy**
```

**Classification:** `convert`

**Justification:** Same structural signal as Sample 1 — standalone bold line immediately followed by prose/list, peer to several other bold blobs ("Search Strategy", "Extraction Routing", "Fallback Policy", "Parallel Optimization") all under `### Tool Orchestration`. The parenthetical "(mandatory)" is a heading modifier, not inline emphasis. Promote to `#### Tavily-First Rule (mandatory)`.

### Sample 3: `rf-qa-qualitative.md:141` — "Scope Appropriateness (Feature vs Platform)"

**File:line:** `src/superclaude/agents/rf-qa-qualitative.md:141`

Surrounding context (lines 139–146):

```text
#### Checklist (23 items)

**Scope Appropriateness (Feature vs Platform)**

1. **Platform content in feature PRDs** — If the document is a Feature PRD, scan for content that belongs in a Platform PRD:
   - Market sizing (TAM/SAM/SOM) or revenue projections in any section
   - Platform-wide pricing tiers or monetization strategy
```

**Classification:** `convert` — but to `##### Foo` (h5), not `#### Foo`

**Justification:** The parent here is already `#### Checklist (23 items)` (h4). The bold blobs "Scope Appropriateness", "Content Quality" (line 160), "Logical Consistency" (line 176), "Red Flags" (line 188) are sub-groupings of that checklist. They must promote one level *below* the parent h4 — so `##### Scope Appropriateness (Feature vs Platform)`. This same h5 pattern repeats inside every QA-phase checklist throughout the file (lines 292, 302, 312, 320, 363, 373, 381, 389, 430, 442, 450, 458, 501, 511, 519, 527, 595, 603, 611, 617 — every MD036 in this file is a sub-group of a `#### Checklist (N items)` heading and demotes to h5, not h4).

### Sample 4 (cross-check): `deep-research-agent.md:177` — "Memory Usage"

**File:line:** `src/superclaude/agents/deep-research-agent.md:177`

Surrounding context (lines 168–183):

```text
### Learning Integration

**Pattern Recognition**

- Track successful query formulations
- Note effective extraction methods
- Identify reliable source types
- Learn domain-specific patterns

**Memory Usage**

- Check for similar past research
- Apply successful strategies
- Store valuable findings
- Build knowledge over time
```

**Classification:** `convert` → `#### Memory Usage`

**Justification:** Confirms the h4-under-h3 pattern (parent is `### Learning Integration`, sibling is `**Pattern Recognition**`). All 15 MD036 hits in deep-research-agent.md follow the same shape — standalone `**Foo**` immediately above a bullet list, under an h3. None is genuine inline emphasis.

**Convert/preserve verdict across sampled MD036:** 100% `convert`. Zero preserve cases in the 3-file sample. The remediation depth depends on the parent heading level:

- Parent is `### h3` → promote to `#### h4`
- Parent is `#### h4` (e.g., inside `#### Checklist (N items)`) → promote to `##### h5`

---

## Sample analyses — MD024 (no-duplicate-heading)

### Sample 1: `rf-qa.md:180` & `:251` & `:296` — three "### What You Verify" headings

**File:line:** `src/superclaude/agents/rf-qa.md:180`, `:251`, `:296`

Surrounding context for `:180` (lines 175–180):

```text
## QA Phase: Synthesis Gate (Pre-Assembly Quality Gate)

**When:** After Phase 5 (Synthesis), before Phase 6 (Assembly).
**Purpose:** Ensure synthesis files are high-quality, evidence-based, and ready for assembly into the final report.

### What You Verify
```

For `:251`:

```text
## QA Phase: Report Validation (Post-Assembly Quality Gate)
...
### What You Verify
```

For `:296`:

```text
## QA Phase: Task Integrity Check
...
### What You Verify
```

**Classification:** `convert` via parent-suffix disambiguation (option A: keep h3, add suffix). NOT restructure-to-h4.

**Justification:** Each `### What You Verify` lives under a *different* `## QA Phase: X` parent. The headings serve identical structural roles within their own h2 sections — they are the proper h3 entry-point per phase. Restructuring to `#### What You Verify` under a single canonical `### Parent` would collapse three distinct QA phases into one, which destroys the section hierarchy. Correct fix: append the phase name in parentheses so each h3 becomes uniquely titled:

- `### What You Verify (Synthesis Gate)`
- `### What You Verify (Report Validation)`
- `### What You Verify (Task Integrity)`

This is the disambiguation-by-parent-context pattern.

### Sample 2: `rf-qa-qualitative.md:263, 334, 401, 472, 539, 656, 694` — seven "### Self-Audit (MANDATORY before writing verdict)" headings

**File:line:** seven instances; sampled at `:263` and `:334`

Surrounding context for `:263` (lines 261–266):

```text
12. **Conclusion is proportionate** — Does the confidence level...

### Self-Audit (MANDATORY before writing verdict)

Before issuing your verdict, answer these questions in your report:

1. How many factual claims did you independently verify against source code?
```

For `:334`:

```text
- **MINOR** — Design that is correct but could be improved...

### Self-Audit (MANDATORY before writing verdict)

Before issuing your verdict, answer these questions in your report:
```

**Classification:** `convert` via parent-suffix disambiguation.

**Justification:** Seven QA-phase blocks (PRD qualitative, research-report qualitative, TDD qualitative, tech-reference qualitative, README qualitative, integration qualitative, post-fix verification) each end with an identical `### Self-Audit` h3. Same pattern as Sample 1 — the heading is the correct h3 for each phase. Append the parent QA-phase name (e.g., `### Self-Audit — PRD Qualitative`, `### Self-Audit — TDD Qualitative`). Restructuring would destroy phase hierarchy; preserve as-is would leave MD024 unfixed.

### Sample 3: `rf-qa-qualitative.md:361, 428, 499` — "#### Checklist (12 items)" / "#### Checklist (14 items)" / "#### Checklist (12 items)"

**File:line:** `:361`, `:428`, `:499`

The raw lint output flags these as MD024 duplicates — but inspection shows the headings already include the item count, so for some pairs they are NOT textually identical (`(14 items)` vs `(12 items)` differ). The MD024 hits cluster on the *repeated* `(12 items)` pairs.

Surrounding context for `:361`:

```text
### What You Verify (TDD Qualitative)
...
#### Checklist (12 items)
```

**Classification:** `convert` via parent-context-aware suffix.

**Justification:** Because the item count differs across some sections, the simplest disambiguator is to incorporate the parent QA-phase: `#### TDD Qualitative Checklist (14 items)`, `#### Tech-Reference Qualitative Checklist (12 items)`, `#### README Qualitative Checklist (12 items)`. This stays at h4 (no restructure) and resolves all repeat-text collisions.

### Sample 4: `rf-qa-qualitative.md:272, 343, 410, 481, 548, 665, 703` — seven "### Verdict" headings

**File:line:** seven instances; same shape as Self-Audit cluster.

**Classification:** `convert` via parent-suffix disambiguation → `### Verdict — PRD Qualitative` etc.

**Convert/preserve verdict across sampled MD024:** 100% `convert` via *parent-context suffix*. Zero `restructure` (demote to h4) cases — restructuring would flatten meaningful per-phase hierarchy. Zero `preserve` cases — these are real lint violations, not false positives.

---

## Sample analyses — MD029 (ol-prefix)

### Sample 1: `rf-qa-qualitative.md:162–174` — "Content Quality" checklist sub-group continuing the parent ordered list

**File:line range:** `:162` (Expected 1, Actual 4) through `:174` (Expected 7, Actual 10)

Surrounding context (lines 160–175):

```text
**Content Quality**

4. **Executive summary is self-contained** — A reader should understand...

5. **Problem statement is specific** — S2 should describe a concrete problem...

6. **User personas are realistic** — Check that personas match the actual user base...

7. **User stories are testable** — Every user story's acceptance criteria...
```

**Classification:** `preserve` numbering (the numbering is correct as-authored; the violation is structural, not numeric).

**Justification:** The author *intended* one continuous numbered list 1–23 ("Checklist (23 items)") with bold sub-group labels grouping every 3–5 items. The numbering 4, 5, 6, 7… is correct — these are items 4 through 7 of the master checklist. markdownlint flags MD029 only because it sees `**Content Quality**` (a paragraph) interrupting the list, which it interprets as the start of a new list at item 4.

**Once MD036 is fixed** by converting `**Content Quality**` to `##### Content Quality` (h5), the heading still breaks the ordered list per markdownlint's parser — markdownlint treats any non-list-item block as a list terminator. So the MD029 remediation cannot be "renumber to 1/2/3" (that breaks the human-meaningful sequence) and cannot be "leave alone" (still fails lint after MD036 fix).

**Three workable resolutions, ranked:**

1. **`use 1/1/1 style` (recommended).** Change the list style from `ol-prefix: 1/2/3` to `ol-prefix: one` in `.markdownlint.json` — every item starts with `1.` and renderers auto-number. This preserves human readability and silences MD029 globally. Author intent of "one 23-item list" is honored at the source level.
2. **`renumber` and accept that headings split it into multiple shorter sequences.** After MD036 fixes promote bold blobs to h5, restart numbering at 1 under each h5. This is the strict-MD029-default fix but discards the "23 items" framing and forces updating the "(23 items)" parent heading.
3. **`preserve` via inline `<!-- markdownlint-disable-next-line MD029 -->` comments.** Verbose, but if the author wants both the literal numbers preserved AND the structural h5 promotion, this is the only way.

**Recommendation for the executor: option 1 (config change to `1/1/1` style).** It is one-line in `.markdownlint.json`, resolves all 79 MD029 hits across the file in one edit, and keeps the author's numbering intent visible.

### Sample 2: `rf-qa.md:275–278` — sub-list at end of a 19-item checklist

**File:line range:** `:275` (Expected 1, Actual 16) through `:278` (Expected 4, Actual 19)

Surrounding context (lines 273–287):

```text
#### Content Quality Checks

16. **Table of Contents accuracy** — Every entry in the ToC links to an actual section header
17. **Internal consistency** — No contradictions between sections
18. **Readability** — Report is scannable (tables, headers, bullet lists) not a prose wall
19. **Actionability** — A developer could begin work from the Implementation Plan section alone

### Fixing Issues (Always Authorized for Report Validation)

For report validation, you are always authorized to fix issues in-place:

1. Document the issue
2. Fix it using Edit tool
3. Verify the fix
4. Document the fix in your QA report
```

**Classification:** `preserve` numbering at source.

**Justification:** Lines 275–278 are items 16–19 of the parent "19-item" checklist, but the `#### Content Quality Checks` h4 on line 273 made markdownlint treat them as a new list starting at 16. Either drop the h4 (which damages content organization), promote it back to a bold-only label (re-introduces MD036), or change ol-prefix style to `1/1/1`.

### Sample 3: `rf-qa.md:325–339` — nested numbered sequence under "Fixing Issues (When Authorized)"

**File:line range:** `:325` (Expected 1, Actual 21) through `:339` (Expected 8, Actual 28)

This is the same pattern again — sub-headings inside QA-phase blocks split what the author intended as one continuous numbered sequence.

**Classification:** `preserve` numbering at source level; resolve globally via `.markdownlint.json` `ol-prefix: one` config change.

**Convert/preserve verdict across sampled MD029:** 100% `preserve` (numbering is correct as-authored). The cleanest fix is a single `.markdownlint.json` change — `MD029: { "style": "one" }` — rather than touching the 79+ violations individually. Per-list renumber-to-1/2/3 is feasible but discards author-intended continuous numbering and forces editing parent headings ("(23 items)" → "(5 items) + (5 items) + (5 items) + ...").

---

## Remediation Playbook

### MD036 playbook — Convert to heading vs preserve as emphasis

**Convert signals (use `#### Foo` or `##### Foo`):**

1. The `**Foo**` is on a standalone line (no other text on that line) AND
2. Is immediately followed by a blank line AND
3. Is immediately followed by a list, prose paragraph, or sub-block that it labels AND
4. Sits alongside ≥2 sibling `**Bar**`, `**Baz**` blobs under the same parent heading (i.e., it functions as a structural divider, not a one-off emphasis).

**Preserve as emphasis signals (leave `**Foo**` alone):**

1. The `**Foo**` is inline within a sentence (e.g., "use the **fallback policy** when…").
2. The bold text is a definition label inside a list item (`- **Term** — definition`) — these are bold-as-glossary-key, not headings. Markdownlint does NOT flag these.
3. The bold text is part of a multi-line paragraph wrapping it (not standalone).

**Depth rule (which heading level to promote to):**

- Parent is `## h2` → unusual; check whether intermediate h3 is missing first. If genuinely sibling of other h3s, use `### Foo`. If sub-section of an existing h3, use `#### Foo`.
- Parent is `### h3` → promote to `#### Foo` (most common case in deep-research-agent.md).
- Parent is `#### h4` (e.g., `#### Checklist (23 items)`) → promote to `##### Foo` (the dominant case in rf-qa-qualitative.md).

**Sampled file verdict:** 100% of the 39 MD036 hits in the three sampled files are `convert`. No preserves found.

### MD024 playbook — Suffix-disambiguate vs restructure-and-demote

**Suffix-disambiguate signals (recommended, `convert` via title rewrite):**

1. The duplicate headings live under *different* parent headings AND
2. Each occurrence serves the same structural role within its own parent (e.g., every QA phase has its own "### What You Verify") AND
3. Restructuring (demoting all to a single h4 under one canonical h3 parent) would collapse meaningfully distinct sections.

**Restructure-and-demote signals (`restructure`, demote to a sub-level):**

1. The duplicate headings appear within the *same* parent section AND
2. They are genuinely sub-aspects of one shared concept AND
3. A single canonical parent already exists or can be cleanly introduced (e.g., promote a paragraph to `### Parent` and demote the dupes to `#### child-A`, `#### child-B`).

**Preserve signals (`preserve` — false positive):**

- None observed in the three sampled files. In general, MD024 with `siblings_only: true` is rarely a false positive in well-structured docs.

**Sampled file verdict:** 100% of the 32 MD024 hits are `convert` via suffix-disambiguation. The suffix should encode the parent QA-phase name (e.g., `### What You Verify (Synthesis Gate)`, `### Self-Audit — TDD Qualitative`, `### Verdict — Research Report Qualitative`). For `#### Checklist (N items)` repeats where the count already differs, include the phase name to make every instance unique (e.g., `#### TDD Qualitative Checklist (14 items)`).

### MD029 playbook — Renumber vs restart vs config-change

**Config-change signals (recommended, `preserve` source content + global rule swap):**

1. The same list-splitting pattern appears in 5+ places in a file (or repo-wide) AND
2. The author's intent is "one logical sequence" expressed across headings/groupings AND
3. Manually renumbering would force updating parent headings ("(N items)") and reduce semantic clarity.

In this case: edit `.markdownlint.json` to set `"MD029": { "style": "one" }` (or `"ordered"` to match author's authored numbers verbatim — but `"one"` is the cleanest and is the markdownlint-documented "1/1/1" style). Every item then starts with `1.` at source level and renderers auto-number.

**Renumber-to-1/2/3 signals (`restructure`, restart each sub-list):**

1. The list-splitting is intentional (each sub-heading really does start a fresh, distinct sequence) AND
2. The "N items" framing in the parent heading is incidental, not load-bearing AND
3. Only a handful of MD029 hits exist (manual renumber is cheaper than a global config change).

**Preserve-via-inline-disable signals (`preserve`):**

- The list spans content where neither config change nor renumber is acceptable (rare). Use `<!-- markdownlint-disable-next-line MD029 -->` per violation. Verbose; last resort.

**Sampled file verdict:** 79 MD029 hits across `rf-qa.md` and `rf-qa-qualitative.md`. All stem from the same root cause: bold-blob sub-headings (which MD036-fix promotes to real h5 headings) split author-intended continuous numbered checklists. **Recommended single fix:** add `"MD029": { "style": "one" }` to `.markdownlint.json` and convert every numbered list to use `1.` for every item. This silences MD029 globally without touching content semantics.

---

## Per-file remediation profile

### `src/superclaude/agents/deep-research-agent.md` (15 MD036, 0 MD024, 0 MD029)

- **Apply:** MD036 convert-to-h4 playbook. Every flagged line (59, 65, 70, 75, 93, 100, 109, 116, 126, 135, 142, 150, 161, 170, 177) is a standalone `**Foo**` under an h3 parent. Promote each to `#### Foo` (depth: parent is `### h3`, so target is `#### h4`).
- **Do NOT apply:** MD024 or MD029 playbooks — no violations.
- **Estimated edits:** 15 single-line edits (each `**Foo**` → `#### Foo`).

### `src/superclaude/agents/rf-qa.md` (0 MD036, 3 MD024, 12 MD029)

- **Apply MD024 playbook:** All 3 hits are `### What You Verify` repeated across QA-phase parents (Synthesis Gate, Report Validation, Task Integrity Check). Use suffix-disambiguation: `### What You Verify (Synthesis Gate)`, `### What You Verify (Report Validation)`, `### What You Verify (Task Integrity)`.
- **Apply MD029 playbook:** All 12 hits are continuation-numbering false-positives caused by sub-headings splitting a continuous checklist. Resolve via the `.markdownlint.json` `"MD029": { "style": "one" }` config change recommended in the global playbook.
- **Estimated edits:** 3 heading suffix-rewrites + 1 config-file edit (if accepting the global fix); or 12+ list re-numberings if config change is rejected.

### `src/superclaude/agents/rf-qa-qualitative.md` (24 MD036, 29 MD024, 67 MD029)

- **Apply MD036 playbook (h5 depth):** All 24 hits sit under `#### Checklist (N items)` parents. Promote to `##### Foo` (e.g., `##### Scope Appropriateness (Feature vs Platform)`, `##### Content Quality`, `##### Red Flags`, `##### Code-to-Document Fidelity`, etc.).
- **Apply MD024 playbook (suffix-disambiguate, never restructure):** 29 hits cluster on four recurring labels — `### What You Verify` (7×), `### Self-Audit (MANDATORY before writing verdict)` (7×), `### Verdict` (7×), `#### Checklist (12 items)` and similar (8× — count varies). Disambiguate each with parent-QA-phase suffix: `### What You Verify (PRD Qualitative)`, `### Self-Audit — TDD Qualitative`, `### Verdict — README Qualitative`, `#### TDD Qualitative Checklist (14 items)`, etc.
- **Apply MD029 playbook (global config change strongly recommended):** 67 hits, all from the same root cause. The `.markdownlint.json` `"MD029": { "style": "one" }` single-line config change resolves the file plus any future occurrences. Alternative (renumber each sub-list 1/2/3 after MD036 fix) is feasible but high-toil (67+ edits) and discards the "(N items)" parent-heading framing.
- **Ordering note for executor:** Fix MD036 BEFORE attempting any per-instance MD029 renumber — once bold blobs become real h5 headings the list-split topology stabilizes. If using the config-change fix for MD029, ordering does not matter.
- **Estimated edits:** 24 single-line h-promotions + 29 heading suffix-rewrites + 1 config edit (or 67+ list renumbers); plus the same depth/suffix rules applied uniformly across the file.

---

## Cross-cutting note: `.markdownlint.json` config-change as a force multiplier

The single config addition `"MD029": { "style": "one" }` resolves **79 of the 234 total violations** (~34%) across all 9 RF agent files with one edit. This is the highest-leverage single change identified during sampling. The executor should evaluate it before attempting per-instance MD029 renumber across the codebase.

The current `.markdownlint.json` already loosens MD013 (line_length=500), MD040 (code_blocks=false), MD033/MD034 (tables=false), MD025 (headings=false). Adding an MD029 style override is consistent with that posture — pragmatic config tuning where the author's intent is clear and the default rule causes cascade violations.

---

**Status:** Complete

**Summary of findings:**

- MD036 (39 hits in sample): 100% `convert` — promote to heading at correct depth (h4 under h3 parents; h5 under h4 parents like `#### Checklist (N items)`). Zero preserves.
- MD024 (32 hits in sample): 100% `convert` via parent-context suffix-disambiguation. Never restructure-and-demote — that would flatten meaningfully distinct QA-phase hierarchies in rf-qa.md and rf-qa-qualitative.md.
- MD029 (79 hits in sample): 100% `preserve` author numbering. Recommended single fix is `.markdownlint.json` config change to `"MD029": { "style": "one" }` — resolves ~34% of total repo violations with one edit. Per-instance renumber is feasible but high-toil and discards the "(N items)" framing.
- Ordering for executor: MD036 fixes (heading promotion) must happen BEFORE per-instance MD029 renumber. If using config-change for MD029, ordering does not matter.
- Per-file profiles documented for deep-research-agent.md (15 MD036), rf-qa.md (3 MD024 + 12 MD029), rf-qa-qualitative.md (24 MD036 + 29 MD024 + 67 MD029).
