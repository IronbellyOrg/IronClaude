# Research: Target File State — confidence-calibrator.md

**Track:** 2 of 4 — Change C
**Researcher:** target-file-state
**Date:** 2026-05-27
**Status:** Complete

## Scope

Byte-level inventory of `src/superclaude/agents/confidence-calibrator.md` plus unique-match `old_string` candidates for every Edit-tool anchor required by Change C (per proposal L190-255).

## 1. File Metadata

- **Absolute path:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/agents/confidence-calibrator.md`
- **Repo-relative path:** `src/superclaude/agents/confidence-calibrator.md`
- **Line count:** 118 lines (verified via `wc -l`)
- **Trailing newline:** present (line 118 is the last content line, file ends with EOL after content)
- **Source-of-truth status:** SOURCE-OF-TRUTH. `src/superclaude/agents/*.md` is the canonical home; `.claude/agents/confidence-calibrator.md` is a sync-dev mirror. All edits land here; `make sync-dev` propagates to `.claude/`.
- **File purpose:** Agent prompt for the `confidence-calibrator` sub-agent. Independently re-grades a hypothesis card against a multi-dimension rubric and returns a calibrated confidence + escalation recommendation. Invoked by `sc-troubleshoot-protocol` in Wave 1.7 (Tier 1) and Wave 3 (per-card Tier 2). Tools: `Read` (read-only).
- **Format:** Markdown with YAML frontmatter (L1-9), then ten H2 sections plus one embedded fenced code block (L58-93, ` ```markdown ` ... ` ``` `) inside `## Output Format`.

## 2. Structural Map (verified line ranges)

| Section | Lines | Notes |
|---------|-------|-------|
| YAML frontmatter | L1-9 | `---` open L1, `---` close L9. Fields: name, description, category, tools, model, maxTurns, permissionMode. Description on L3 contains em-dash U+2014. |
| Blank line | L10 | separator |
| `# Confidence Calibrator — Rubric Scoring Agent` | L11 | H1, contains em-dash U+2014 |
| Blank | L12 | |
| `## Triggers` | L13 | header |
| Triggers body | L14-17 | 3 bullets (L15, L16, L17); L14 is blank line after header |
| Blank | L18 | |
| `## Role` | L19 | header |
| Blank | L20 | |
| Role body | L21 | single paragraph; contains em-dashes |
| Blank | L22 | |
| `## Independence Instruction` | L23 | header |
| Blank | L24 | |
| Independence body | L25-27 | L25 = first bold paragraph; L26 = blank; L27 = second bold paragraph |
| Blank | L28 | |
| `## Safety Constraint` | L29 | header |
| Blank | L30 | |
| Safety body | L31 | single bold paragraph |
| Blank | L32 | |
| `## Behavioral Mindset` | L33 | header |
| Blank | L34 | |
| Behavioral body | L35-37 | L35 paragraph; L36 blank; L37 paragraph (both contain em-dashes) |
| Blank | L38 | |
| `## Inputs` | L39 | header |
| Blank | L40 | |
| Inputs body | L41-45 | 5 bullets (`card_path`, `rubric_path`, `card_tier`, `flags_context`, `output_path`) |
| Blank | L46 | |
| `## Responsibilities` | L47 | header |
| Blank | L48 | |
| Responsibilities body | L49-54 | 6 numbered items, one line each |
| Blank | L55 | |
| `## Output Format` | L56 | header |
| Blank | L57 | |
| Fenced code block OPEN | L58 | ` ```markdown ` |
| Fenced block body | L59-92 | Report template — H1 + meta + Per-dimension scores + table + Confidence + Escalation recommendation + Notes |
| Fenced code block CLOSE | L93 | ` ``` ` |
| Blank | L94 | |
| `## Boundaries` | L95 | header |
| Blank | L96 | |
| Boundaries body | L97-111 | "Will:" L97 + 4 bullets L99-102; blank L103; "Will Not:" L104 + 7 bullets L106-111 |
| Blank | L112 | |
| `## Failure Modes (what the orchestrator should plan for)` | L113 | header |
| Blank | L114 | |
| Failure Modes body | L115-118 | 4 bullets |

### 2a. Fenced-block interior detail (L58-93)

| Line | Content (paraphrased) |
|------|------|
| L58 | ` ```markdown ` (fence open) |
| L59 | `# Calibration Report` |
| L60 | blank |
| L61 | `**Card under calibration**: <abs path>` |
| L62 | `**Rubric**: <abs path>` |
| L63 | `**Card tier**: <1\|2>` |
| L64 | `**Timestamp**: <ISO 8601>` |
| L65 | blank |
| L66 | `## Per-dimension scores` |
| L67 | blank |
| L68 | `\| Dimension \| Score \| Justification (cite card content) \|` |
| L69 | `\|-----------\|-------\|-----------------------------------\|` |
| L70 | `\| Evidence grounding \| 1.0 / 0.5 / 0.0 \| <one-line citing what in the card supports this> \|` |
| L71 | `\| Symptom coverage \| ... \| ... \|` |
| L72 | `\| Reproducibility fit \| ... \| ... \|` |
| L73 | `\| Fix directness \| ... \| ... \|` |
| L74 | `\| Domain coherence \| ... \| ... \|` |
| L75 | blank |
| L76 | `## Confidence` |
| L77 | blank |
| L78 | `- **Self-reported (in card)**: <X.XX>` |
| L79 | `- **Calibrated (this report)**: <Y.YY>` |
| L80 | `- **Delta**: <signed difference, and a one-line read on why it differs>` |
| L81 | blank |
| L82 | `## Escalation recommendation` |
| L83 | blank |
| L84 | `- **Verdict**: \`STOP\` \| \`ESCALATE\`` |
| L85 | `- **Reason**: \`none\` \| \`low_confidence\` \| \`multi_domain\` \| \`intermittent\` \| \`not_reproducible\` \| \`forced_by_depth_deep\` \| \`security_caution\`` |
| L86 | `- **Rubric rule fired**: <quote the rule from § Escalation Decision>` |
| L87 | blank |
| L88 | `## Notes` |
| L89 | blank |
| L90 | `- Any evidence the card cited that did not verify on spot-check ...` |
| L91 | `- Any dimension scored low ...` |
| L92 | `- Any structural pathology in the card ...` |
| L93 | ` ``` ` (fence close) |

## 3. Anchor Capture — Unique-Match `old_string` Candidates

Each anchor below is a verbatim slice from the live file. All slices have been confirmed unique within the file by inspection (no duplicate substrings). For each anchor I note the precise line span, the verbatim text, and whether the Edit operation is INSERT (replace anchor with `anchor + new content`) or REPLACE (replace anchor with revised content).

> CRITICAL: All snippets below use straight Markdown text exactly as it appears in the source. The Edit tool requires byte-exact matches, including the leading hyphen on bullets, the two-space indentation of code-block content (there is NO leading indentation in this file — the fenced block content is flush-left within the fence), and em-dashes (U+2014).

### (a) INSERT `## Claim-class handling` between Independence Instruction and Safety Constraint

Boundary spans L27 (last line of Independence Instruction body) → L28 (blank) → L29 (`## Safety Constraint` header). The unique-match slice MUST capture all three to be unambiguous (`## Safety Constraint` is a unique header; the L27 line is unique).

**Anchor (lines 27-29, verbatim):**

```
**Spot-check evidence citations.** Do NOT trust the card's quoted snippets without Reading the cited files. "Evidence grounding" can only be scored honestly if you've actually verified what's there.

## Safety Constraint
```

**Edit mode:** INSERT-BEFORE (replace anchor with `<original L27>\n\n<new ## Claim-class handling subsection from spec>\n\n## Safety Constraint`). The new subsection body is supplied by spec-extraction (Researcher 1) from proposal L190-255. The Edit replaces this 3-line slice with the original L27 + blank + new subsection content + blank + `## Safety Constraint`.

### (b) REPLACE Responsibilities item #1 (5-dimensions → 6-dimensions)

**Anchor (lines 49-50, verbatim):**

```
1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
2. **Read the card** at `card_path`.
```

**Edit mode:** REPLACE. The L49 string `5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence` is replaced with the 6-dim string per spec (the 6th is `Runtime check` per Change A). Including L50 in the anchor guarantees uniqueness AND fixes the boundary so the renumbering insertions below have an unambiguous footing. The replacement text MUST keep L50 intact (no edits to item #2 text in this operation).

Alternative minimal anchor (if Researcher 1's spec text replaces only the L49 content):

```
1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
```

This L49-only slice is unique in the file (only place that contains "5 dimensions" + the listed names).

### (c) INSERT new item #2a between current #2 (L50) and current #3 (L51)

**Anchor (lines 50-51, verbatim):**

```
2. **Read the card** at `card_path`.
3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches. This is essential to scoring "Evidence grounding" honestly. If a citation does not match, mark it in the Notes section and let that drive the Evidence grounding score.
```

**Edit mode:** INSERT-BETWEEN. Replace this 2-line slice with `<original L50>\n<new 2a line(s) from spec>\n<original L51>`. The new item per spec reads the card's frontmatter for `Claim class`, `Evidence class`, `Verdict direction` and notes them in the calibration report. Researcher 1 provides verbatim text.

Caveat: this slice uniqueness depends on the L51 spot-check sentence remaining intact. Item (d) below also anchors on L51, so operations (c) and (d) MUST NOT run simultaneously — see Section 6 for ordering.

### (d) INSERT new item #3a between current #3 (L51) and current #4 (L52)

**Anchor (lines 51-52, verbatim):**

```
3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches. This is essential to scoring "Evidence grounding" honestly. If a citation does not match, mark it in the Notes section and let that drive the Evidence grounding score.
4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
```

**Edit mode:** INSERT-BETWEEN. Replace this 2-line slice with `<original L51>\n<new 3a line from spec>\n<original L52>`. The new item per spec is the WebFetch-detection / `spot_check_unverifiable` mark (MARK-only — no actual WebFetch needed; tools list stays `Read`).

### (e) REPLACE Responsibilities item #4 (add Runtime-check dimension scoring)

**Anchor (lines 52-53, verbatim):**

```
4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
5. **Compute the arithmetic mean**, rounded to 2 decimals.
```

**Edit mode:** REPLACE. The L52 text is replaced with the spec's updated #4 (mentions the new Runtime check dimension explicitly, plus the verdict-direction modifier from Change A). L53 is included as anchor context only and MUST NOT be altered in this operation — the L53 #5 has its own dedicated REPLACE in (f).

### (f) REPLACE Responsibilities item #5 (arithmetic mean → gated-min formula)

**Anchor (lines 53-54, verbatim):**

```
5. **Compute the arithmetic mean**, rounded to 2 decimals.
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.
```

**Edit mode:** REPLACE. The L53 text is replaced with the spec's gated-minimum formula language (use the rubric's gated-min formula from Change A). L54 is anchor-only.

### (g) INSERT new item #5a between current #5 (L53) and current #6 (L54)

NOTE — operations (f) and (g) share the same anchor lines L53-54. They cannot use overlapping slices. Recommended approach: combine (f) and (g) into a single Edit operation that replaces the 2-line L53-54 slice with `<new #5 from (f)>\n<new #5a>\n<L54 unchanged>` and let (h) handle L54 separately. See Section 6 ordering.

**Anchor (lines 53-54, verbatim) — same as (f):**

```
5. **Compute the arithmetic mean**, rounded to 2 decimals.
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.
```

**Edit mode:** INSERT-BETWEEN, combined with (f). Single Edit replaces L53-54 with `<new #5>\n<new #5a>\n<L54 original>` — leaves operation (h) to mutate L54 in a subsequent Edit.

### (h) REPLACE Responsibilities item #6 (extend escalation_reason allowed-value set)

**Anchor (line 54, verbatim):**

```
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.
```

This single line is unique in the file (only line containing `Apply the escalation decision rules`). Including L55 (blank line) and L56 (`## Output Format`) in the anchor is OPTIONAL — single-line uniqueness is sufficient.

**Edit mode:** REPLACE. The spec extends the language describing the allowed-value set for `escalation_reason` to include `source_only_dynamic_claim` (Change A's new escalation reason). Researcher 1 provides exact text.

### (i) INSERT Runtime-check row in per-dimension table (inside fenced block)

The new Runtime-check row inserts between the Evidence-grounding row (L70) and the Symptom-coverage row (L71) per Change A's 6-dim table ordering.

**Anchor (lines 70-71, verbatim):**

```
| Evidence grounding | 1.0 / 0.5 / 0.0 | <one-line citing what in the card supports this> |
| Symptom coverage | ... | ... |
```

**Edit mode:** INSERT-BETWEEN. Replace this 2-line slice with `<L70 unchanged>\n<new Runtime check row>\n<L71 unchanged>`. The spec defines the exact pipe-separated row text.

### (j) INSERT `## Stage-2 trace (REQUIRED)` subsection between table end and `## Confidence`

The Stage-2 trace lands AFTER the per-dimension table (current end L74) and BEFORE `## Confidence` (L76), with the blank L75 between them.

**Anchor (lines 74-76, verbatim):**

```
| Domain coherence | ... | ... |

## Confidence
```

**Edit mode:** INSERT-BETWEEN. Replace this 3-line slice with `<L74 unchanged>\n\n<new Stage-2 trace subsection block from spec>\n\n## Confidence`. The spec provides a 7-row table verbatim (per research-notes.md L46).

NOTE: this slice is INSIDE the fenced ` ```markdown ` block (between L58 and L93). The Edit content must therefore be plain text — no extra fences. The Stage-2 trace becomes part of the template emitted by the agent.

### (k) REPLACE Confidence "Self-reported" bullet (insert clarifying parenthetical)

**Anchor (lines 78-79, verbatim):**

```
- **Self-reported (in card)**: <X.XX>
- **Calibrated (this report)**: <Y.YY>
```

**Edit mode:** REPLACE. The L78 text is replaced with the spec's clarifying language ("Self-reported … read but NOT used" per research-notes.md L46). L79 is anchor-only and MUST NOT be altered in this operation; operation (l) handles the post-Calibrated insertion.

### (l) INSERT "Formula applied" bullet between Calibrated (L79) and Delta (L80)

**Anchor (lines 79-80, verbatim):**

```
- **Calibrated (this report)**: <Y.YY>
- **Delta**: <signed difference, and a one-line read on why it differs>
```

**Edit mode:** INSERT-BETWEEN. Replace this 2-line slice with `<L79 unchanged>\n<new Formula applied bullet>\n<L80 unchanged>`. The bullet documents which gated-min branch fired (per Change A's formula). Researcher 1 provides exact bullet text.

### Cross-reference: operations affecting same anchor lines

| Lines | Operations | Resolution |
|-------|------------|------------|
| L49 | (b) | standalone |
| L50-51 | (c) | standalone |
| L51-52 | (d) | standalone — but (d) shares L51 with (c) → ORDER: (c) before (d) is risky; (c) and (d) must be sequenced so each Edit re-anchors against the post-(c) file. Safer: combine into one Edit replacing L50-L52. |
| L52-53 | (e) | (e)'s L53 anchor and (f)/(g)'s L53 anchor overlap. ORDER: do (e) first, then (f)+(g) combined; OR combine (e) + (f) + (g) into one larger Edit replacing L52-L54. |
| L53-54 | (f) + (g) | combine into one Edit |
| L54 | (h) | standalone after (f)+(g) (since (f)+(g) leaves L54 unchanged) |
| L70-71 | (i) | standalone |
| L74-76 | (j) | standalone |
| L78-79 | (k) | (k)'s L79 anchor overlaps with (l)'s L79 anchor. Combine into one Edit replacing L78-L80. |
| L79-80 | (l) | combine with (k) |

## 4. Fenced Code Block Boundaries

- **OPEN:** Line 58 — exact text: ` ```markdown ` (4 chars: three backticks + `markdown` = 11 chars total, no trailing space)
- **CLOSE:** Line 93 — exact text: ` ``` ` (three backticks, nothing else)
- **Interior span:** L59 through L92 (34 lines of report-template content)
- **CRITICAL implication:** insertions (i) Runtime-check row, (j) Stage-2 trace subsection, (k) Self-reported bullet replacement, and (l) Formula-applied bullet insertion ALL land INSIDE the fence. The new content MUST be plain Markdown (no nested fences, no triple-backtick within the new content) or the fence will be prematurely terminated and the rest of the template will fall outside the code block. The Stage-2 trace in (j) is a pipe-table (per research-notes.md L46 "Stage-2 trace table with all 7 rows verbatim") — pipe tables are safe inside fences.

- **Sole code block in the file:** grep confirmed exactly two fence lines (L58 and L93) — no other fenced blocks elsewhere. This makes the boundaries trivially anchorable.

## 5. Character Encoding / Unicode Inventory

Verified via `grep -nP '[^\x00-\x7F]'` (non-ASCII scan) and targeted searches:

- **Em-dash U+2014 ( — )**: appears on lines L3, L11, L21, L35, L109, L110, L111, L118 plus inside the frontmatter description on L3. NONE of the anchor lines captured for Change C edits ((a)-(l) span L27, L29, L49-54, L70-71, L74-76, L78-80) contain em-dashes — anchors are pure ASCII.
- **Section sign U+00A7 ( § )**: appears on L54 (inside Responsibilities #6: "rubric § Escalation Decision") and L86 (inside the fenced report template: "<quote the rule from § Escalation Decision>"). Anchor (h) on L54 INCLUDES the § character → byte-exact match required when supplying L54 as `old_string`.
- **Plus-minus U+00B1 ( ± )**: appears only on L118 (Failure Modes "±0.05"). Outside Change C edit scope.
- **No other non-ASCII codepoints in the file.** No smart quotes, no non-breaking spaces, no zero-width chars.
- **Line endings:** LF (Unix). No CRLF observed.
- **Trailing whitespace on edit-anchor lines:** None observed on any of L49-54, L70-71, L74-76, L78-80, L27, L29. (Verified via Read output — no trailing-space artifacts.)

**Edit-tool implication:** All anchor strings can be reproduced as pure ASCII text EXCEPT (h)'s L54 anchor, which must include the literal `§` character in the `old_string`. Copy-paste from this research file preserves the U+00A7 codepoint.

## 6. Recommended Edit Ordering

The optimal ordering minimizes anchor invalidation. After each Edit, downstream anchors may shift in line number, but the unique-substring property is what matters — line numbers are not used by the Edit tool.

### Ordering principle

Group edits by anchor region. Combine overlapping-anchor operations into single Edits where overlap exists. Independent regions can run in any order.

### Suggested sequence

1. **(a) Insert `## Claim-class handling`** — standalone, anchor L27-29. No conflicts.
2. **(b) REPLACE Responsibilities #1** — standalone, anchor L49 (or L49-50). No conflicts with subsequent steps because step 3 below re-anchors using the post-(b) content (which still contains the "Read the card" L50 substring unchanged).
3. **(c) + (d) combined: INSERT items #2a and #3a between L50/L51 and L51/L52** — combine into ONE Edit. Anchor:

   ```
   2. **Read the card** at `card_path`.
   3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches. This is essential to scoring "Evidence grounding" honestly. If a citation does not match, mark it in the Notes section and let that drive the Evidence grounding score.
   4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
   ```

   Replacement: `<L50>\n<new 2a>\n<L51>\n<new 3a>\n<L52>`. Single Edit; uniqueness guaranteed by full 3-line slice.

4. **(e) + (f) + (g) combined: REPLACE #4, REPLACE #5, INSERT #5a** — combine into ONE Edit. Anchor:

   ```
   4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
   5. **Compute the arithmetic mean**, rounded to 2 decimals.
   6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.
   ```

   Replacement: `<new #4 from spec>\n<new #5 from spec>\n<new #5a from spec>\n<L54 unchanged>`. Single Edit; uniqueness guaranteed by 3-line slice spanning L52-54.

5. **(h) REPLACE Responsibilities #6** — standalone, anchor L54. Run AFTER step 4 (step 4 left L54 untouched). Note: after step 4, L54 has shifted to a higher line number due to inserted #5a, but the substring `Apply the escalation decision rules` is still unique in the file, so Edit will find it. The replacement extends the `escalation_reason` allowed-value enumeration.

6. **(i) INSERT Runtime-check row in table** — standalone, anchor L70-71. No conflicts with step 7 (different region).

7. **(j) INSERT `## Stage-2 trace (REQUIRED)`** — standalone, anchor L74-76. No conflicts with step 6 (above) or step 8 (below) — anchors are non-overlapping rows of the same table / surrounding subsections. Run in any order relative to (i), but (i) BEFORE (j) is the natural top-down order.

   **Ordering dependency note (per task brief Section 6 prompt):** the task brief stated "(j) depends on (i) landing first if the unique-match slice spans the table". Verification: (j)'s anchor is `| Domain coherence | ... | ... |\n\n## Confidence` — which does NOT span the Evidence/Symptom rows where (i) lands. Therefore (j) does NOT depend on (i). Independent. Either order is safe.

8. **(k) + (l) combined: REPLACE Self-reported bullet, INSERT Formula-applied bullet** — combine into ONE Edit. Anchor:

   ```
   - **Self-reported (in card)**: <X.XX>
   - **Calibrated (this report)**: <Y.YY>
   - **Delta**: <signed difference, and a one-line read on why it differs>
   ```

   Replacement: `<new self-reported bullet with "read but NOT used" clarifier>\n<L79 unchanged>\n<new Formula applied bullet>\n<L80 unchanged>`. Single Edit; uniqueness guaranteed by 3-line slice.

### Total Edit operations

After combining overlapping-anchor operations: **8 Edit calls** (steps 1-8 above) instead of the 12 individual operations (a)-(l). Each call uses a unique multi-line anchor slice for safety.

### Alternative: single-shot Responsibilities rewrite

If the spec text supplied by Researcher 1 permits, an even safer collapse is to anchor on the entire L49-L54 block (6 lines, all 6 numbered items) and replace with the full new 9-item list (#1 revised, #2 unchanged, #2a new, #3 unchanged, #3a new, #4 revised, #5 revised, #5a new, #6 revised). This replaces steps 2-5 above with a single Edit. Trade-off: larger diff, but zero risk of inter-anchor drift. Recommended if Researcher 1 provides the complete revised list verbatim.

Likewise for Output Format inside the fence: L70-L80 could be anchored as one block (per-dimension rows + blank + Confidence header + 3 Confidence bullets) and replaced with the full revised version including the new Runtime-check row + Stage-2 trace subsection + revised Confidence bullets — collapsing steps 6-8 into one Edit.

**Final recommended ordering (most conservative, smallest blast radius per Edit):** 8 Edits as listed in steps 1-8.

**Final recommended ordering (fewest Edits, larger anchor slices):** 4 Edits — (1) Claim-class subsection insert, (2) full Responsibilities block rewrite L49-L54, (3) full Output Format interior rewrite L70-L80, (4) escalation_reason extension on L54 (or fold into Edit 2). Executor's call based on confidence in Researcher 1's verbatim spec text.

## Summary

- **Target file:** `src/superclaude/agents/confidence-calibrator.md` — 118 lines, source-of-truth (sync-dev to `.claude/`).
- **Structural map confirmed:** 11 H2 sections + 1 H1, with one fenced ` ```markdown ` block spanning L58-93 (open/close confirmed via grep). Line ranges in the task brief approximately matched but were verified line-by-line; corrections noted (e.g., Responsibilities body is L49-54, blank L48 between header L47 and content; per-dimension table runs L68-74, Confidence subsection L76-80 inside fence).
- **All 12 anchor slices captured** for operations (a)-(l). Every slice was verified unique within the file. Two anchor overlaps identified and resolved by combining into single Edits: (c)+(d), (e)+(f)+(g), (k)+(l).
- **Fenced-block insertions documented:** operations (i), (j), (k), (l) land INSIDE the fence; new content must not contain triple-backticks. (j)'s anchor does NOT overlap (i)'s anchor — they are independent (correcting the brief's tentative dependency note).
- **Unicode inventory:** em-dash U+2014 (8 occurrences, none in anchor regions), section sign U+00A7 (L54 inside Responsibilities #6 anchor AND L86 inside fence — anchor (h) must preserve `§`), plus-minus U+00B1 (L118 only, outside scope). No other non-ASCII.
- **Recommended ordering:** 8 Edits (conservative) or 4 Edits (fewer, larger anchor slices). Both safe. Executor chooses based on confidence in Researcher 1's verbatim replacement text.
- **No blockers found.** All anchors are clean; the file is straightforward to edit. The only cross-task hard dependency is that Change A MUST ship first (the 6th dimension, gated-min formula, and `source_only_dynamic_claim` escalation reason all come from Change A's rubric updates) — this is a sequencing concern, not an anchor-capture concern.
