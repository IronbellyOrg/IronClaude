# Research: File Inventory + Anchor Identification

**Topic type:** File Inventory
**Scope:** sc:troubleshoot command file + sc-troubleshoot-protocol skill + 5 refs
**Status:** Complete
**Date:** 2026-05-22
---

## troubleshoot.md

**File:** `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md` (198 lines total)

### Frontmatter — lines 1-9

Lines 1-9 (delimited by `---` on lines 1 and 9). Field-by-field:

- Line 2: `name: troubleshoot`
- Line 3: `description: "Tiered debugging — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate, and an opt-in task-builder remediation chain"`
- Line 4: `category: analysis`
- Line 5: `complexity: advanced`
- Line 6: `mcp-servers: [auggie, serena, context7, tavily, sequential]`
- Line 7: `personas: [analyzer, performance, security, qa, refactorer, devops]`
- Line 8: `argument-hint: "[<issue description>] [--type bug|build|performance|deployment|security|test] [--depth quick|standard|deep] [--scope <path|symbol>] [--no-escalate] [--fix] [--models <tier:model,...>] [--output-dir <path>] [--no-mcp]"`

The `argument-hint` is the existing flag enumeration. **No new flag is required for Wave 1.5** — Wave 1.5 runs unconditionally inside the existing flow; it does NOT add a new top-level option. (Verified: the task is about adding a wave, not a flag. If the builder later decides to gate Wave 1.5 behind a flag, this is the line to extend.)

### Options table — lines 46-57

- Header row: line 48 — `| Flag | Default | Description |`
- Separator: line 49
- First flag row: line 50 (`--type`)
- Last flag row: line 57 (`--no-mcp`)

Verbatim flag rows for reference:

```
50: | `--type` | auto-detect | One of `bug`, `build`, `performance`, `deployment`, `security`, `test`. Auto-detected from keywords + structural cues in the issue description. |
51: | `--depth` | `standard` | `quick` (Tier 1 only, ~1-3 min, ~3-6k Claude tokens), `standard` (auto-escalate by rubric), `deep` (force Tier 2 with adversarial debate). |
52: | `--scope` | (none) | File, directory, or symbol to narrow auggie/serena queries against. |
53: | `--no-escalate` | `false` | Cap at Tier 1 regardless of confidence. Useful for quick second-opinion passes. |
54: | `--fix` | `false` | After diagnosis, offer the Tier 3 remediation chain ... |
55: | `--models` | (agent defaults) | Per-tier model override, e.g. `tier1:sonnet,hypothesis:opus`. |
56: | `--output-dir` | `.dev/troubleshoot/<slug>-<timestamp>/` | Where REPORT.md, hypothesis cards, fix proposals, adversarial artifacts, and audit log are written. |
57: | `--no-mcp` | `false` | Run in native-tools-only mode (skip auggie/serena/context7/tavily). Tier 1 quality degrades; surfaced in the report. |
```

### Behavioral Summary — lines 59-74

- Section header: line 59 (`## Behavioral Summary`)
- Lead paragraph + numbered steps: lines 61-66
- "Three tiers under the hood" prose anchor: line 68
- Tier table header: line 70 — `| Tier | When | What it does | Cost |`
- Separator: line 71
- Tier rows: lines 72-74 (Tier 1, Tier 2, Tier 3)

Note: this section describes TIERS, not waves. Wave 1.5 is internal to Tier 1; this section does NOT need to be edited unless the builder wants to mention "with documentation grounding" in the Tier 1 row. (Recommended: leave alone — Tier 1 cost band 3-6k tokens still applies.)

### MCP Integration — lines 83-89

- Section header: line 83
- Auggie row: line 85
- Serena row: line 86
- Context7 row: line 87 — currently reads "Tier 2 only, when the symptom mentions a framework or library by name or the stack trace ends in third-party code."
- Tavily row: line 88
- Sequential row: line 89

**RIPPLE-EFFECT FLAG:** The Context7 row (line 87) currently says "Tier 2 only". If Wave 1.5 introduces a Tier 1 Context7 call (documentation grounding), this row's "Tier 2 only" claim becomes false. Line 87 likely needs to be edited to "Tier 1 (Wave 1.5 documentation grounding) and Tier 2 (when ...)". The builder MUST decide whether Wave 1.5 uses Context7 directly or proxies through auggie. (Researcher 3 should confirm.)

### Tool Coordination — lines 91-101

- Section header: line 91
- Line 95: `**`mcp__context7__resolve-library-id` / `query-docs`**: external library docs (Tier 2)` — same ripple-effect concern as line 87. If Wave 1.5 calls context7 directly, change `(Tier 2)` to `(Tier 1 grounding + Tier 2 enrichment)`.

### Boundaries — lines 155-177

- Section header: line 155 (`## Boundaries`)
- "Will:" subsection header: line 157
- "Will:" bullet range: lines 159-166 (8 bullets)
- "Will Not:" subsection header: line 168
- "Will Not:" bullet range: lines 170-177 (8 bullets)

Wave 1.5 likely needs new bullets:

- A "Will" bullet stating "Ground every Tier 1 hypothesis in product documentation when the issue intersects a documented behavior" — insertion candidate: after line 162 (which already mentions auggie+serena grounding).
- A "Will Not" bullet stating "Recommend a code fix without first checking whether the observed behavior is the documented behavior" — insertion candidate: after line 170 or 171.

### CRITICAL BOUNDARIES — lines 179-189

- Section header: line 179
- Lead banner: line 181
- Body lines 183-189

No edit expected unless the builder decides documentation-grounded test_is_wrong demands a new CRITICAL BOUNDARY entry. Researcher 3 should confirm.

### Related Commands — lines 191-198

- Section header: line 191
- Six bullet entries: lines 193-198 (`/sc:adversarial`, `/sc:analyze`, `/sc:reflect --type task`, `task-builder` skill, `/sc:brainstorm`, `/sc:auggie-review`)

No edit expected.

### Skill activation — lines 76-81

- Section header: line 76 (`## Activation`)
- Mandate line: line 78
- The `> Skill sc:troubleshoot-protocol` block: line 79
- Body warning: line 81

No edit expected.

---

## SKILL.md

**File:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (385 lines total)

### Frontmatter — lines 1-5

- Line 1: `---`
- Line 2: `name: sc:troubleshoot-protocol`
- Line 3: `description: "Tiered debugging protocol — ..."` (long single-line description)
- Line 4: `allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking`
- Line 5: `---`

**Critical:** `allowed-tools` on line 4 already includes `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` — Wave 1.5 can use these without modifying the allowed-tools list. **No frontmatter edit required for tool authorization.**

### Extended-metadata comment — lines 7-12

```
7:  <!-- Extended metadata (for documentation, not parsed):
8:  category: utility
9:  complexity: advanced
10: mcp-servers: [auggie, serena, context7, tavily, sequential]
11: personas: [analyzer, performance, security, qa, refactorer, devops]
12: -->
```

No edit expected.

### Purpose — lines 14-25

- Section header: line 16
- Core contract paragraph: line 20 (mentions "Tier 1 is intended to feel close to 'just look at it'")
- "Why this works" paragraph: line 22
- "Hallucination contract" paragraph: line 24

No edit strictly required, but Researcher 3 may recommend adding a sentence about documentation grounding to the Purpose paragraph (line 20 or new paragraph after line 24).

### Required Input (STOP if missing) — lines 26-35

- Section header: line 26
- Bullet list: lines 30-31
- STOP rules: lines 33, 35

No edit expected.

### Output Contract — lines 37-65

- Section header: line 37
- Lead: line 39
- Table header: line 41 — `| Field | Type | Description |`
- Table separator: line 42
- First field row: line 43 (`status`)
- Last field row: line 56 (`remediation_accepted`)

**ALL FIELD ROWS (lines 43-56) — VERBATIM, the builder needs these for the new field's slot:**

```
43: | `status` | string | `success`, `partial` (some findings dropped for grounding), `failed` |
44: | `tier_reached` | int | 1, 2, or 3 |
45: | `report_path` | string | Absolute path to `REPORT.md` |
46: | `audit_log_path` | string | Absolute path to `audit.log` |
47: | `confidence` | float | 0.0-1.0, calibrated via `refs/escalation-rubric.md` |
48: | `escalation_reason` | string | If Tier 2 ran: which rubric condition triggered it (or `forced_by_depth_deep`) |
49: | `test_is_wrong` | bool | `true` when the diagnosis concludes the failing test is the bug (test asserts wrong behavior, stale invariant, or inverted policy claim) rather than the code under test. Set independent of tier. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a fix to the code when this is `true`; the remediation target is the test file. |
50: | `test_file_path` | string \| null | When `test_is_wrong=true`, the **repo-relative** path of the test file that must be updated (e.g., `tests/api/test_foo.py`), resolved against the repo root containing `.git/`. `null` otherwise. The format is intentionally fixed to repo-relative so downstream automation can compare/join paths without ambiguity; if the report is consumed outside the repo, the consumer is responsible for joining against the repo root recorded in the audit log. |
51: | `hypothesis_cards` | list[path] | Paths to per-agent hypothesis cards (Tier 2) |
52: | `adversarial_artifacts_dir` | string | `sc:adversarial` artifacts dir (Tier 2 only, when 2+ fix proposals were debated) |
53: | `task_file_path` | string | MDTM task file path (Tier 3 only) |
54: | `remediation_offered` | bool | Whether Tier 3 was offered |
55: | `remediation_accepted` | bool | If offered, user's response |
```

**INSERTION POINT for `behavior_is_documented`** (the new field): the cleanest semantic slot is **immediately after line 50** (after `test_file_path`), because `behavior_is_documented` is part of the same asymmetric-cost cluster with `test_is_wrong` / `test_file_path`. Inserting at line 51 (pushing `hypothesis_cards` down) preserves the logical grouping: status fields → confidence fields → asymmetric-cost flags → artifact paths.

Lines 49 and 50 are the closest precedent for the new field's row shape (bool flag with prose explanation; string|null path with derivation rule). Mirror line 49's style for a bool, line 50's style for a path.

### `test_is_wrong` derivation rule subsection — lines 57-65

- Lead line 57: `**`test_is_wrong`derivation rule** (applied during Wave 5 synthesis): set ... when ... AND one of these conditions holds:`
- Numbered list: lines 58-60 (three conditions)
- Compound case clarification: line 63
- Closing paragraph (purpose of flag): line 65

This subsection is the structural precedent for any new "behavior_is_documented derivation rule" subsection — Researcher 3 owns that downstream wiring, but the builder needs to know: insert the new derivation rule either immediately after line 65 (separate subsection, parallel structure) or extend line 65 to acknowledge both flags. Recommended: parallel subsection at line 66 (new) to keep each flag's derivation rule self-contained.

### Wave Structure code block — lines 67-79

- Section header: line 67 (`## Wave Structure`)
- Code fence open: line 69 (` ``` `)
- Wave listing: lines 70-77 (Wave 0 through Wave 6)
- Code fence close: line 77
- Trailing prose: line 79

**VERBATIM Wave listing (lines 70-77):**

```
70: Wave 0: Parse + Validate Input
71: Wave 1: Tier 1 — Triage          ← always; loads refs/triage-checklist.md on demand
72: Wave 2: Confidence Gate          ← decides escalation via refs/escalation-rubric.md
73: Wave 3: Tier 2 — Parallel Hypotheses (conditional)
74: Wave 4: Tier 2 — Adversarial Fix Debate (conditional, requires ≥2 viable fixes)
75: Wave 5: Synthesis + Report        ← always finalises; loads refs/report-template.md
76: Wave 6: Tier 3 — Remediation Chain (conditional, requires --fix + user accept)
```

**INSERTION POINT for Wave 1.5 listing:** between line 71 and line 72. The new line reads (suggested):

```
Wave 1.5: Documentation Grounding  ← always; loads refs/documentation-grounding-rules.md (or equivalent) on demand
```

Builder must decide whether Wave 1.5 is "always" or "conditional". Researcher 3 covers the downstream wiring decision.

### Wave 0 — lines 83-117

- Section header: line 83 (`### Wave 0: Parse + Validate Input`)
- Preconditions line: 85
- Steps list: lines 87-99
- Audit log header block: lines 102-113
- Exit criteria: line 115
- STOP conditions: line 117

No edit expected.

### Wave 1 — lines 121-143

- Section header: line 121 (`### Wave 1: Tier 1 — Triage`)
- Goal: line 123
- Preconditions: line 125
- Steps list (numbered 1-4): lines 127-139
  - Step 1 (ground in real code): lines 129-132
  - Step 2 (reproduce or observe): lines 133-136
  - Step 3 (form one hypothesis): line 137
  - Step 4 (calibrate confidence): lines 138-139
- Exit criteria: line 141
- Token budget: line 143

**CRITICAL — INSERTION POINT for Wave 1.5:** Wave 1 ends at line 143. The next section header `### Wave 2: Confidence Gate` is at line 147. The blank-line separator is line 144, the horizontal rule `---` is line 145, and the blank-line separator before Wave 2 is line 146.

**The Wave 1.5 block inserts at line 145 (replacing the existing horizontal rule with a new section, OR inserting after line 145 to keep it).** Recommended insertion: insert the new `### Wave 1.5: Documentation Grounding` block AFTER line 145 (preserving the horizontal rule as the Wave 1 → Wave 1.5 separator), and add a new horizontal rule + blank lines before the existing line 147 to separate Wave 1.5 from Wave 2.

In summary:

- **Wave 1 ends:** line 143
- **Horizontal rule separator:** line 145
- **Wave 2 begins:** line 147
- **Wave 1.5 insertion:** after line 145, before line 147 (push Wave 2 down by however many lines the new block requires + one new `---` separator)

### Wave 2 — lines 147-163

- Section header: line 147
- Goal: line 149
- Decision logic: lines 151-159
- On STOP: line 161
- On escalate: line 163

No edit expected unless Wave 1.5 returns a signal that influences the gate (it shouldn't — Wave 1.5 informs the hypothesis itself, not the gate).

### Wave 3 — lines 167-215 (the parallel-fan-out pattern Wave 1.5 mirrors)

- Section header: line 167 (`### Wave 3: Tier 2 — Parallel Hypotheses`)
- Goal: line 169
- Preconditions: line 171
- Agent-selection table (lines 173-183):
  - Lead line: line 173
  - Table header: line 175
  - Separator: line 176
  - Rows: lines 177-182 (bug, performance, security, build, deployment, test)
  - Cap-at-4 paragraph: line 184
- Steps list (lines 186-200):
  - Step 1 (MCP enrichment): lines 188-191
  - Step 2 (spawn hypothesis agents): lines 192-197
  - Step 3 (wait for all agents): line 198
  - Step 3.5 (calibrate each card): line 199
  - Step 4 (distill candidate fixes): line 200
- Exit criteria: lines 202-205
- Failure handling table: lines 209-215

**This is the canonical parallel-Task-spawn pattern Wave 1.5 will mirror.** Specifically, line 192 reads:

```
192:    2. **Spawn hypothesis agents** in parallel via `Task` (single message with multiple Task calls). Each agent receives:
```

If Wave 1.5 fans out parallel documentation lookups (e.g., parallel auggie + context7 + serena queries), the pattern is "issue N MCP calls in parallel in the same turn" (per Wave 1 step 1 lines 129-132) — NOT the Wave 3 multi-Task agent fan-out, because Wave 1.5's job is grounding, not hypothesis generation. Researcher 2 owns the pattern quote.

### Wave 4 — lines 219-244

- Section header: line 219
- Goal: line 221
- Preconditions: line 223
- Steps: lines 225-240
- Exit criteria: line 242
- Skip conditions: line 244

No edit expected.

### Wave 5 — lines 248-288 (REPORT.md composition; Documentation Context section inserts here)

- Section header: line 248 (`### Wave 5: Synthesis + Report`)
- Goal: line 250
- Steps: lines 252-285
  - Step 1 (load report-template): line 254
  - Step 2 (compose REPORT.md filling in sections): lines 255-263 — **this is the list of sections REPORT.md contains**. Verbatim section list from lines 256-263:

```
256:    - Header (target, tier reached, confidence, escalation reason)
257:    - Summary (2-4 sentence executive summary)
258:    - Diagnosis (the chosen hypothesis — from Tier 1 alone, or from the adversarial merge)
259:    - Evidence (cited `file:line` and command outputs)
260:    - Proposed Fix (the recommended change)
261:    - Alternative Fixes Considered (Tier 2 only — the losing proposals from the debate, with one-line reason each)
262:    - Risk + Rollback (what to watch after applying)
263:    - Next Steps (Tier 1: rerun with `--depth deep` if needed; Tier 2 without `--fix`: re-invoke with `--fix` to authorize remediation; Tier 2 with `--fix`: confirm to proceed to Wave 6)
```

- Step 3 (file:line validation): lines 264-265
- Step 4 (audit log footer): lines 266-279
- Step 5 (surface to user in chat): lines 281-286
- Exit criteria: line 288

**INSERTION POINT for "Documentation Context" in Wave 5 step 2:** between line 259 (Evidence) and line 260 (Proposed Fix). The Documentation Context section sits AFTER Evidence and BEFORE Proposed Fix, because it provides the documentation-derived constraint the Proposed Fix must respect.

Suggested new line at 259.5 (insert as new line, push 260+ down):

```
- Documentation Context (Wave 1.5 finding — cited docs and the documented-behavior verdict)
```

Researcher 3 owns the exact wording; the slot is clear.

### Wave 6 — lines 292-306

- Section header: line 292
- Preconditions: line 294
- Steps: lines 296-304
- Exit criteria: line 306

No edit expected.

### Tool Coordination Summary table — lines 310-323

- Section header: line 310
- Table header: line 312 — `| Tool | Tier 1 | Tier 2 | Tier 3 |`
- Separator: line 313
- Tool rows: lines 314-323

**Verbatim rows:**

```
314: | `mcp__auggie__codebase-retrieval` | ✓ (one focused query) | ✓ (per-hypothesis queries) | — |
315: | `mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview` | ✓ | ✓ | — |
316: | `mcp__context7__query-docs` | — | ✓ when framework/library named | — |
317: | `mcp__tavily__tavily-search` | — | ✓ rate-limited (≤2 queries) | — |
318: | `mcp__sequential-thinking__sequentialthinking` | — | ✓ for synthesis | — |
319: | `Task` (agent spawn) | ✓ (root-cause-analyst + confidence-calibrator) | ✓ (...) | ✓ (self-review for post-exec) |
320: | `Skill` | — | ✓ (`sc:adversarial-protocol`) | ✓ (`task-builder`, `/sc:reflect`) |
321: | `Read` / `Grep` / `Glob` | ✓ | ✓ | — |
322: | `Bash` | ✓ (repro when cheap) | ✓ (diagnostic commands) | — |
323: | `Write` | ✓ (hypothesis + report) | ✓ (hypothesis cards, fix proposals) | — |
```

**RIPPLE-EFFECT FLAG:** Line 316 currently shows `mcp__context7__query-docs` as `—` (NOT used) in Tier 1. If Wave 1.5 uses Context7, line 316 must be edited to show `✓ (Wave 1.5 documentation grounding)` in the Tier 1 column. This is the second authoritative place where the "Context7 is Tier 2 only" claim lives — first being line 87 of troubleshoot.md.

### Will Do — lines 325-334

- Section header: line 325
- Eight bullets: lines 327-334

No edit strictly required, but a bullet about documentation grounding would belong here. Insertion candidate: after line 330 (which mentions auggie/serena tier coverage) — new bullet "Always check product documentation before recommending a code fix that contradicts documented behavior".

### Will Not Do — lines 336-346

- Section header: line 336
- Eight bullets: lines 338-346

Insertion candidate: after line 338 — new bullet "Recommend a code change that contradicts documented behavior without surfacing the contradiction".

### Error Handling table — lines 348-362

- Section header: line 348
- Table header: line 350
- Rows: lines 352-362

**Two key precedent rows (lines 352-353) — verbatim, these are the patterns Wave 1.5 must mirror for graceful degradation:**

```
352: | All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality is degraded; native tools only | None |
353: | auggie unavailable (others OK) | Fall back to `Grep` + `Glob` for grounding; mark in audit | None |
```

**INSERTION POINT for Wave 1.5 degradation row:** anywhere in lines 352-362, semantically after line 353 (auggie-unavailable) makes sense. A new row would read approximately:

```
| context7 unavailable (Wave 1.5) | Skip documentation grounding; mark `documentation_grounded: false` in audit; do NOT block the Tier 1 hypothesis | Native `Grep` on docs/ if --scope intersects a documented behavior |
```

Researcher 2 owns the canonical format; Researcher 3 owns the actual decision text. Builder needs to know the row goes in this table.

### Token Cost Profile — lines 364-373

- Section header: line 364
- Table header: line 366
- Rows: lines 368-371
- Trailing prose: line 373

**RIPPLE-EFFECT FLAG:** Line 368 reads `| Tier 1 only | ~2-5k | ~3-6k | 1-3 min |`. If Wave 1.5 adds context7 calls, the auggie-tokens column may need a small bump (~+1-2k for the documentation lookup). The Claude-tokens column likely stays — Wave 1.5 is mostly retrieval offload. Builder must decide whether to bump these numbers.

### Refs loader table — lines 375-385

- Section header: line 375 (`## Refs`)
- Table header: line 377 — `| File | When loaded |`
- Separator: line 378
- Five existing rows: lines 379-383
- Closing prose: line 385

**Verbatim refs table:**

```
379: | `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1 (calibration) |
380: | `refs/triage-checklist.md` | Wave 1 (passed to root-cause-analyst as part of the brief) |
381: | `refs/hypothesis-card-template.md` | Wave 1 and Wave 3 (passed to agents) |
382: | `refs/report-template.md` | Wave 5 |
383: | `refs/remediation-handoff.md` | Wave 6 |
```

**Sort order observation:** the table is **NOT alphabetical** (`escalation-rubric` comes before `hypothesis-card-template` alphabetically, but the table puts `triage-checklist` between them). It is **wave-order** (escalation/triage are Wave 1-2, hypothesis-card is Wave 1+3, report is Wave 5, remediation is Wave 6). The new Wave 1.5 ref slots between `triage-checklist` (Wave 1) and `hypothesis-card-template` (Wave 1+3), OR after `triage-checklist` (Wave 1) but still before `hypothesis-card-template` (Wave 1+3) — wave-order dictates it goes between lines 380 and 381.

**INSERTION POINT for new ref:** after line 380, before line 381. New row reads approximately:

```
| `refs/documentation-grounding-rules.md` | Wave 1.5 (documentation grounding) |
```

The new ref file path will be `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/documentation-grounding-rules.md` (or whatever the builder names it — `docs-grounding.md` is a plausible shorter alternative; Researcher 4 confirms naming convention from prior tasks).

---

## refs/hypothesis-card-template.md

**File:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (107 lines total)

The template body is inside a fenced code block (lines 9-69 — opens line 9, closes line 69). Field-by-field:

### Field list with line citations

- **Header** (`# Hypothesis: <claim>`): line 10
- **Agent metadata** (Agent / Tier / Timestamp / Cause class): lines 12-15
- **## Claim** section: lines 17-19
- **## Evidence** section: lines 21-27
- **## Proposed Fix** section: lines 29-39
- **## Confidence** section: lines 41-52 (includes per-dimension self-assessment lines 48-52)
- **## Risks** section: lines 54-56
- **## If I'm wrong, it's probably because...** section: lines 58-60
- **## Alternatives considered** section: lines 62-64
- **## Grounding gaps** section: lines 66-68

Verbatim per-dimension self-assessment lines (48-52):

```
48: - Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
49: - Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
50: - Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
51: - Fix directness: <0.0|0.5|1.0> — <one-line reason>
52: - Domain coherence: <0.0|0.5|1.0> — <one-line reason>
```

These are the five existing rubric dimensions. Researcher 3 may recommend adding a sixth dimension `Consistency with documentation` here — if so, the insertion point is line 53 (push later sections down by 1 line). The indentation is `-` (list item dash, then space).

### Recommended slot for new `consistency_with_docs` field

There are TWO reasonable interpretations of "where consistency_with_docs slots":

**Interpretation A — New per-dimension item under Confidence section (line 53 insertion):**

```
- Consistency with documentation: <0.0|0.5|1.0> — <one-line reason>
```

This treats documentation grounding as a sixth rubric dimension. **Caveat:** this requires a parallel edit to `refs/escalation-rubric.md` (lines 11-17) to add the new row to the dimensions table. Researcher 3 owns the cross-file ripple.

**Interpretation B — New top-level section after Evidence (line 28 insertion, push Proposed Fix down):**

```
## Consistency with documentation

State whether the observed behavior matches the documented behavior. Cite the doc(s). If they conflict, the hypothesis MUST address the conflict explicitly — either the doc is stale, or the code violates the doc.

- Documented behavior: <one-line quote with `path/to/doc.md:NN` citation>
- Observed behavior: <one-line>
- Verdict: <documented | undocumented | conflicting>
```

Interpretation B is the cleaner slot because it groups documentation grounding with Evidence (also a grounding section) and keeps the rubric dimensions (Confidence section) untouched. **Recommended: Interpretation B.** Final decision is Researcher 3's, but the builder should anticipate both interpretations.

### "Worked example" code block — lines 80-107

The worked example illustrates the structure; if a new section is added, the example may need a parallel extension. Insertion candidate: after line 95 (end of Evidence example) and before line 97 (start of Proposed Fix example) — add a 2-3 line example of the new Consistency with documentation section.

### Filling rules — lines 71-77

These are constraints on the template. The "≤ 1 page (~60 lines)" rule (line 73) means adding a new section will push closer to the cap; builder may want to keep the new section terse (3-5 lines max).

---

## refs/report-template.md

**File:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` (153 lines total)

The template body is inside a fenced code block (lines 7-125 — opens line 7, closes line 125).

### Section header list with line citations

Within the fenced template:

- **Title** (`# Troubleshoot Report`): line 8
- **Header fields** (Target, Type, Tier reached, Confidence, Status, Escalation reason, Test is wrong, Test file to update, Duration, Date): lines 10-19
- **`---` separator**: line 21
- **## Summary** section: lines 23-28
- **## Diagnosis** section: lines 30-37
- **## Evidence** section: lines 39-47
- **## Proposed Fix** section: lines 49-63
- **## Alternative Fixes Considered** section: lines 65-74
- **## Risk + Rollback** section: lines 76-84
- **## Follow-up tasks** section: lines 86-96
- **## Grounding Gaps** section: lines 98-106
- **## Next Steps** section: lines 108-116
- **## Audit** section: lines 118-124

After fenced block:

- **## Rendering rules**: lines 127-132
- **## Test-is-wrong rule**: lines 134-153

### Verbatim `test_is_wrong` / `test_file_path` header field lines (16-17)

These are the closest precedent for the new `behavior_is_documented` header line:

```
16: **Test is wrong**: <true|false> <!-- See "Test-is-wrong rule" below. When true, surface `Test file to update` on its own line and DO NOT recommend code changes as the primary fix. -->
17: **Test file to update**: <absolute or repo-relative path when test_is_wrong=true, otherwise omit this line>
```

**The new header field** (mirroring shape) — insertion point after line 17, before line 18 (Duration). Suggested verbatim:

```
**Behavior is documented**: <true|false|n/a> <!-- See "Behavior-is-documented rule" below. When true, the Documentation Context section is REQUIRED. When false (observed behavior contradicts docs), the asymmetric-cost rules apply — test_is_wrong becomes more likely. -->
**Documentation references**: <bullet list of `path/to/doc.md:NN` citations when behavior_is_documented=true, otherwise "None"; "n/a" if --no-mcp suppressed Wave 1.5>
```

Researcher 3 owns the exact wording; the slot is clear.

### Cleanest insertion point for the Documentation Context section

The section list within the fenced template is:

```
8:   # Troubleshoot Report  (title)
23:  ## Summary
30:  ## Diagnosis
39:  ## Evidence
49:  ## Proposed Fix
65:  ## Alternative Fixes Considered
76:  ## Risk + Rollback
86:  ## Follow-up tasks
98:  ## Grounding Gaps
108: ## Next Steps
118: ## Audit
```

The user task says "the Documentation Context section inserts somewhere here; identify the cleanest insertion point with rationale."

**Recommended: insert between Evidence (line 47 end) and Proposed Fix (line 49 start).**

Rationale:

1. **Logical flow**: Evidence → Documentation Context → Proposed Fix mirrors the new derivation order. The Proposed Fix MUST respect the Documentation Context (which says what the documented behavior is); putting Documentation Context BEFORE Proposed Fix makes that respect-order visually obvious.
2. **Symmetry with Wave 5 prose**: Wave 5 step 2 list (SKILL.md lines 256-263) will need to insert "Documentation Context" between "Evidence" and "Proposed Fix" — same slot. Keeping the template and the Wave 5 list in lock-step prevents drift.
3. **Cited evidence still owned by Evidence**: the Documentation Context references docs cited in Evidence (line 39-47); putting it right after Evidence lets a reader scan Evidence → Doc Context → Fix as a single flow.

**Alternative considered:** between Diagnosis (line 37) and Evidence (line 39). Rejected because Diagnosis is the verdict; Documentation Context is a finding that feeds the verdict — it belongs BEFORE Diagnosis OR AFTER Evidence. Putting Documentation Context before Diagnosis breaks the existing flow (Diagnosis is the "answer", and the answer should follow the Summary directly). Putting it after Evidence is the cleaner placement.

**Insertion mechanics:** insert a new section between lines 47 and 49. The new section is approximately 8-12 lines (header + 3-5 bullets). Pushes all subsequent line numbers down by N (where N = lines inserted).

Suggested verbatim new section:

```
## Documentation Context

Wave 1.5 documentation grounding result. Cited docs and verdict.

- **Documented behavior**: <one-line quote with `path/to/doc.md:NN` citation> (or "No relevant documentation found")
- **Observed behavior**: <one-line — how the code actually behaves>
- **Verdict**: <documented | undocumented | conflicting>
- **Implication for fix**: <one-line on how this verdict constrains the Proposed Fix below>

If `Behavior is documented: false` (conflicting): the Proposed Fix MUST NOT silently change the documented behavior — either update the docs in lockstep, or treat as a test-is-wrong case (see Test-is-wrong rule).
```

### "Apply with" / "Alternative Fixes Considered" / "Risk + Rollback" boundary

The boundary is line 63 / line 65 (end of Proposed Fix, start of Alternative Fixes Considered). The Documentation Context section is NOT recommended for this slot because by the time we reach Proposed Fix, the documentation constraint has already been applied — putting Doc Context AFTER Proposed Fix would mean "here's what the docs say… by the way, the fix already ignored/respected this." That's backwards.

### Test-is-wrong rule subsection — lines 134-153

This is the structural precedent for any new "Behavior-is-documented rule" subsection at the end of the file. Insertion point: after line 153 (end of file), as a new `## Behavior-is-documented rule` subsection. Mirror the shape of lines 134-153.

---

## refs/escalation-rubric.md

**File:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (52 lines total)

**Brief summary:** This file defines the 5-dimension rubric used in Wave 1 (calibration) and the escalation decision tree used in Wave 2. Lines 11-17 are the 5-dimension table; lines 28-42 are the escalation decision rules.

**Ripple-effect verdict for Wave 1.5:**

- **If the builder adopts Interpretation A (new rubric dimension):** lines 11-17 MUST be extended with a 6th row `| **Consistency with documentation** | ... | ... | ... |`. Researcher 3 owns this decision.
- **If Interpretation B (new template section, not a rubric dimension):** this file is **NOT touched**. Wave 1.5 produces a verdict that gets recorded in REPORT.md but does NOT change the Wave 1 calibration math.
- **Possible new escalation rule** in lines 28-42: "If `behavior_is_documented=false` (conflicting docs) → ESCALATE (`escalation_reason: docs_conflict`)" — this would be a new bullet under "Signal-driven escalation" (lines 34-39). Researcher 3 owns this call.

**Recommended position (mine, not authoritative):** keep this file untouched unless adopting Interpretation A. Wave 1.5 is grounding, not gating.

---

## refs/triage-checklist.md

**File:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md` (65 lines total)

**Brief summary:** Passed to `root-cause-analyst` in Wave 1. Lists pre-investigation grounding bullets (lines 7-14), the cause-class scan table (lines 20-34), the evidence-or-drop check (lines 38-44), the fix sketch rules (lines 48-54), and the "when to refuse Tier 1" list (lines 58-63).

**Ripple-effect verdict for Wave 1.5:**

- Lines 7-14 ("Before forming a hypothesis, the agent should have read:") — list of 4 grounding steps. Currently mentions only stack trace + auggie + serena + a test. **Adding a 5th bullet** "The product documentation for the symptom's behavior, if it intersects a documented feature" would be the cleanest ripple. Insertion point: after line 13, before line 14.
- The "fix sketch" subsection (lines 48-54) currently says nothing about respecting documented behavior. A new line at 54.5 reading "If the fix would change documented behavior, flag it explicitly" would tie Wave 1.5 back to the triage checklist.

**The "before recommending a fix" prompt the task spec mentions:** This file's line 47 (Fix sketch header) and line 53 (multi-domain signal) are the only places that come close to "before recommending a fix". Wave 1.5 doesn't change the literal meaning of either — the agent still produces a fix sketch, just with documentation context added. **Verdict: low ripple, the file's existing prompts still hold.**

**Recommended position:** add 1 bullet at line 13.5 (between current "at least one test" and "If any of these were not possible") so the documentation read is treated as the same kind of grounding as the auggie+serena reads. Optional.

---

## refs/remediation-handoff.md

**File:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` (122 lines total)

**Brief summary:** Loaded in Wave 6 only. Describes the Tier 3 task-builder offer, Phase A (build task), Phase B (pre-execution review), Phase C (execution gate), Phase D (post-execution validation).

**Ripple-effect verdict for Wave 1.5:**

- The `BUILD_REQUEST` template (lines 43-56) currently constructs from REPORT.md sections. If Wave 1.5 adds a "Documentation Context" section to REPORT.md, the task-builder consuming the BUILD_REQUEST might benefit from passing the doc citations to the new task file. Specifically, the `REFERENCES` block (lines 53-56) could gain a 4th line:

```
- Documentation cited in REPORT.md: <list of doc paths from Documentation Context section>
```

  Insertion candidate: after line 55, before line 56 (or extend line 56 to include both audit log and docs).

- The template-selection criteria (lines 58-64) currently keys on file count, regression likelihood, schema/migration/API change. If `behavior_is_documented=false` flips to "use complex template", that's a 4th criterion — recommended bullet: "Behavior-is-documented is false (documented behavior conflict requires careful sequencing)."

**Verdict: low-to-medium ripple, optional.** Researcher 3 owns the call on whether to touch this file in the same task. Reasonable scope decision is to NOT touch this file in the Wave 1.5 task (out of scope — Wave 6 is downstream of Wave 1.5 and the existing wiring continues to work; the new REPORT.md section is purely additive in the Wave 6 consumer's view).

**Recommended position:** Out of scope for the Wave 1.5 task; defer to a future iteration if needed.

---

## Discovery surfaces (sanity check)

Confirmed all three exist:

- `.dev/releases/current/` — confirmed (contains: `cliEval`, `CLIPRD-schemaMismatch`, `roadmap-cli-skill-converge`, `task-builder-merge`, `task-sc-task-directional-merge`)
- `.dev/releases/complete/` — confirmed (contains: `auggie-first`, `cleanup-audit-v2-UNIFIED-SPEC`, `cross-framework-deep-analysis`, `freshness-system`, `hook-sync-and-matcher-fix`, `obligation-vocab-alignment`, `reflect-path-regression`, `release-split`, `release-split-workspace-rca`, `sc-reflect-rescrutiny-design.md`, `sc-reflect-rescrutiny-workflow.md`, `unified-audit-gating-v1.2.1`, `unified-audit-gating-v2`, `v.1.05-MemoryOpt`, `v.1.06-CleanupAudit`, `v1.0-mcp-installer`, `v1.4-roadmap-gen`, `v1.7-adversarial`, `v2.01-Architecture-Refactor`, `v2.02-Roadmap-v3`)
- `docs/` — confirmed (contains: `agents`, `analysis`, `analysis-sc-tasklist.md`, `debates`, `developer-guide`, `eval`, `generated`, `getting-started`, `guides`, `mcp`, `memory`, `reference`, `research`, `sprint-budget-architecture.md`, `sprint-cli-deep-dive.md`, `Templates`, `testing`, `troubleshooting`, `user-guide`)

All three required subdirectories under `docs/` (reference, developer-guide, analysis) exist. The `docs/troubleshooting/` directory also exists and may be a candidate Wave 1.5 search target.

---

## Summary

All edit anchors the builder will reference (cited by file:line):

### troubleshoot.md (command file, 198 lines)

- Frontmatter: lines 1-9 (argument-hint at line 8 — likely UNCHANGED)
- Options table: header line 48, rows 50-57 (likely UNCHANGED unless a new flag is added)
- Behavioral Summary tier table: header 70, rows 72-74 (likely UNCHANGED)
- MCP Integration: line 87 (Context7 row — POTENTIAL EDIT to remove "Tier 2 only" claim)
- Tool Coordination: line 95 (Context7 entry — same POTENTIAL EDIT as line 87)
- Boundaries Will: insertion candidate after line 162
- Boundaries Will Not: insertion candidate after line 170 or 171

### SKILL.md (protocol skill, 385 lines)

- Frontmatter allowed-tools: line 4 (already permits context7 — NO EDIT needed)
- Output Contract table: header 41, rows 43-56 — **INSERT `behavior_is_documented` (and possibly `documentation_references`) after line 50**; mirror style of lines 49-50
- `test_is_wrong` derivation rule subsection: lines 57-65 — **INSERT parallel "behavior_is_documented derivation rule" after line 65**
- Wave Structure code block: lines 70-77 — **INSERT new "Wave 1.5: Documentation Grounding" line between line 71 and line 72**
- **Wave 1 ends line 143; horizontal rule line 145; Wave 2 begins line 147 — INSERT new ### Wave 1.5 block AFTER line 145, BEFORE line 147** ← THIS IS THE PRIMARY INSERTION POINT
- Wave 3 parallel-Task pattern: line 192 (precedent for fan-out spawn syntax — Wave 1.5 likely uses Wave 1's parallel-MCP-call pattern instead, lines 129-132)
- Wave 5 REPORT.md section list: lines 256-263 — **INSERT "Documentation Context" between line 259 (Evidence) and line 260 (Proposed Fix)**
- Tool Coordination Summary table: line 316 — **EDIT to add `✓ (Wave 1.5)` in Tier 1 column**
- Will Do bullets: lines 327-334 — **INSERT new bullet after line 330**
- Will Not Do bullets: lines 338-346 — **INSERT new bullet after line 338**
- Error Handling table: lines 352-353 (precedent rows for graceful degradation) — **INSERT new Wave 1.5 row after line 353**
- Token Cost Profile: line 368 (Tier 1 row — POTENTIAL bump to auggie tokens)
- Refs loader table: lines 379-383 — **INSERT new row for `refs/documentation-grounding-rules.md` between line 380 and line 381** (wave-order, between triage-checklist and hypothesis-card-template)

### refs/hypothesis-card-template.md (107 lines)

- Field list: lines 10-68 (within fenced block at lines 9-69)
- Confidence per-dimension self-assessment: lines 48-52 (Interpretation A insertion point at line 53)
- Top-level section insertion (Interpretation B — RECOMMENDED): after line 27 (end of Evidence section), before line 29 (start of Proposed Fix section)
- Worked example parallel extension: candidate after line 95

### refs/report-template.md (153 lines)

- Header fields: lines 10-19 — **INSERT `Behavior is documented` and `Documentation references` after line 17** (mirror lines 16-17 shape exactly)
- Section list within fenced template: titles at lines 23, 30, 39, 49, 65, 76, 86, 98, 108, 118
- **CLEANEST INSERTION POINT for Documentation Context section: between line 47 (end of Evidence) and line 49 (start of Proposed Fix)** — rationale: Evidence → Documentation Context → Proposed Fix preserves derivation-order legibility
- Test-is-wrong rule subsection: lines 134-153 — **INSERT parallel "Behavior-is-documented rule" after line 153**

### refs/escalation-rubric.md (52 lines)

- 5-dimension table: lines 11-17 (Interpretation A would extend; Interpretation B leaves untouched)
- Escalation decision rules: lines 28-42 (potential new rule under signal-driven escalation, lines 34-39)
- **Verdict: NO ripple required unless Interpretation A is chosen**

### refs/triage-checklist.md (65 lines)

- Pre-investigation grounding list: lines 7-14 — **OPTIONAL insertion of 5th bullet after line 13**
- **Verdict: LOW ripple, optional**

### refs/remediation-handoff.md (122 lines)

- BUILD_REQUEST REFERENCES block: lines 53-56 — potential addition of doc citations line
- Template-selection criteria: lines 58-64 — potential addition of "behavior_is_documented=false" criterion
- **Verdict: OUT OF SCOPE for Wave 1.5 task, defer**

### New file

- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/documentation-grounding-rules.md` — to be created (Researcher 4 confirms filename convention)

### Discovery sanity check

- `.dev/releases/current/`, `.dev/releases/complete/`, `docs/{reference,developer-guide,analysis,troubleshooting}/` all confirmed present.
