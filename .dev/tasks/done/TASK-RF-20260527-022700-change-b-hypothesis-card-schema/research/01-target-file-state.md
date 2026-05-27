# Research: Target File State
**Topic type:** File Inventory
**Scope:** src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md
**Status:** Complete
**Date:** 2026-05-27
---

## 1. File metadata

- **Absolute path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`
- **Total line count:** 108 lines (`wc -l` output: `108`). Note: prompt's stated "109 lines" was off by one — actual is 108. The file ends with a trailing newline after line 108 (closing ` ``` ` fence of worked example).
- **Source-of-truth location:** YES — lives in `src/superclaude/` (not `.claude/`). Edits here must be followed by `make sync-dev` per project rule #6.
- **Purpose (1 sentence):** Defines the canonical Hypothesis Card markdown template used by `root-cause-analyst` (Wave 1.7) and every Tier 2 agent in Wave 3 of the sc-troubleshoot-protocol, including a worked example.

## 2. Structural map (line ranges)

| Lines | Content |
|---|---|
| L1 | H1 title: `# Hypothesis Card Template` |
| L2 | blank |
| L3 | Intro paragraph (single line) about who uses the template |
| L4 | blank |
| L5 | Intro paragraph (single line) about "one proposed cause-and-fix" rule |
| L6 | blank |
| L7 | `## Template` heading |
| L8 | blank |
| L9 | Opening code fence: ` ```markdown ` |
| L10 | Card H1 placeholder: `# Hypothesis: <one-line claim, ...>` |
| L11 | blank |
| **L12-16** | **Frontmatter block** (Agent, Tier, Timestamp, Cause class, Consistency with docs) |
| L17 | blank |
| L18 | `## Claim` heading |
| L19 | blank |
| L20 | Claim guidance paragraph |
| L21 | blank |
| L22 | `## Evidence` heading |
| L23 | blank |
| L24 | Evidence guidance paragraph |
| L25 | blank |
| L26-28 | 3 bullet examples of evidence |
| L29 | blank |
| L30 | `## Proposed Fix` heading |
| L31 | blank |
| L32 | Fix guidance paragraph |
| L33 | blank |
| L34-35 | bullet examples of files changing |
| L36 | blank |
| L37 | "Include a test that would prove the fix:" prose |
| L38 | blank |
| L39-40 | bullet examples of tests |
| L41 | blank |
| L42 | `## Confidence` heading |
| L43 | blank |
| L44 | `Self-reported confidence: <0.0–1.0>` |
| L45 | blank |
| L46 | calibration note |
| L47 | blank |
| **L48-53** | **Per-dimension self-assessment block** (header L48, 5 bullets L49-53) |
| L54 | blank |
| L55 | `## Risks` heading |
| L56 | blank |
| L57 | Risks guidance paragraph |
| L58 | blank |
| **L59** | `## If I'm wrong, it's probably because...` heading |
| L60 | blank |
| **L61** | Body paragraph of "If I'm wrong" section |
| L62 | blank |
| L63 | `## Alternatives considered` heading |
| L64 | blank |
| L65 | Alternatives guidance paragraph |
| L66 | blank |
| L67 | `## Grounding gaps` heading |
| L68 | blank |
| L69 | Grounding-gaps guidance paragraph |
| L70 | Closing code fence: ` ``` ` |
| L71 | blank |
| L72 | `## Filling the card` heading |
| L73 | blank |
| L74-77 | 4 bullets (Length cap, No TODOs, One claim, Cite real files) |
| L78 | blank |
| L79 | `## Worked example (illustrative — not a real card)` heading |
| L80 | blank |
| L81 | Opening code fence: ` ```markdown ` |
| L82-107 | Worked example body |
| L108 | Closing code fence: ` ``` ` |

**Note vs prompt's anchors:** The prompt described frontmatter as L12-16 (confirmed), per-dimension self-assessment as L48-53 (confirmed: header L48 + 5 bullets L49-53), and "If I'm wrong" as L59-61 (confirmed: heading L59, blank L60, body L61).

## 3. Anchor verbatim capture

### 3a. Frontmatter block (L12-16)

Verbatim (each line ends with newline):

```
**Agent**: <agent-name>
**Tier**: <1|2>
**Timestamp**: <ISO 8601>
**Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
```

- L12: `**Agent**: <agent-name>`
- L13: `**Tier**: <1|2>`
- L14: `**Timestamp**: <ISO 8601>`
- L15: `**Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">`
- L16: `**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>`

No leading indentation. No trailing whitespace observed. All lines bold-key + colon + space + value.

### 3b. Per-dimension self-assessment (L48-53)

Verbatim:

```
Per-dimension self-assessment:
- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
- Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
- Fix directness: <0.0|0.5|1.0> — <one-line reason>
- Domain coherence: <0.0|0.5|1.0> — <one-line reason>
```

- L48: `Per-dimension self-assessment:`
- L49: `- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>`
- L50: `- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>`
- L51: `- Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>`
- L52: `- Fix directness: <0.0|0.5|1.0> — <one-line reason>`
- L53: `- Domain coherence: <0.0|0.5|1.0> — <one-line reason>`

Bullets use `- ` (hyphen + single space). Em-dash is U+2014 (`—`), not double-hyphen.

### 3c. "If I'm wrong" section (L59-61)

Verbatim:

```
## If I'm wrong, it's probably because...

One sentence. The agent's best guess at the next-most-likely explanation if this hypothesis is wrong. This is what the Tier 2 fan-out uses to choose complementary agents.
```

- L59: `## If I'm wrong, it's probably because...`
- L60: (blank)
- L61: `One sentence. The agent's best guess at the next-most-likely explanation if this hypothesis is wrong. This is what the Tier 2 fan-out uses to choose complementary agents.`

Apostrophes are straight ASCII `'` (U+0027), not curly.

## 4. Code-fence boundary analysis

Confirmed two fenced code blocks in the file:

- **Block 1 (Template):** opens at L9 ` ```markdown `, closes at L70 ` ``` `. All schema/template content (frontmatter, sections, per-dimension self-assessment, etc.) lives INSIDE this fence.
- **Block 2 (Worked example):** opens at L81 ` ```markdown `, closes at L108 ` ``` `.

**Critical implication for Change B edits:** All three insertion points (a, b, c) are INSIDE the L9-70 fence. The builder must place new content between L9 and L70. Edits MUST NOT land inside the L81-108 worked-example fence (unless we choose to also update the example, which the proposal's Migration note explicitly allows to be left as a v1-style example).

## 5. Worked-example assessment

Worked example (L79-108) currently shows the following frontmatter (L84-87):

```
**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:14:30Z
**Cause class**: Missing/wrong import
```

It omits `**Consistency with docs**:` (v1 of the schema, pre-Change-A) — already inconsistent with current template (L16). This suggests the worked example was not updated when `Consistency with docs` was added; per the proposal's Migration note (treating v1 cards as valid via defaults), this is tolerated.

Per-dimension self-assessment section (L107: `[per-dimension breakdown ...]`) is collapsed to a placeholder, so Runtime check insertion doesn't visibly contradict.

"If I'm wrong" section is entirely absent from the worked example (the example truncates after Confidence at L105).

**Would the worked example CONTRADICT the new schema if left unchanged?** No. It is already a partial/v1-style example (omits `Consistency with docs`, omits "If I'm wrong", collapses per-dimension breakdown). The proposal's Migration note treats v1 cards as valid via defaults. The example is illustrative only ("not a real card" per L79) and adding Claim class / Evidence class / Verdict direction / Runtime check / Falsification standard / Evidence classification would not be contradicted — they would simply be absent, same as the already-absent `Consistency with docs`.

**Recommendation:** Leave worked example untouched. Change B is additive-schema-only.

## 6. Surrounding-line context for Edit calls

### Insertion point (a): After L15, before L16

3 lines before (L13-15) + 3 lines after (L16-18):

```
**Tier**: <1|2>
**Timestamp**: <ISO 8601>
**Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>

## Claim
```

**Unique-match candidate `old_string` for Edit tool:**

```
**Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
```

This 2-line slice is unique in the file (verified — `**Cause class**` appears at L15 and at L87, but the L87 occurrence is NOT followed by `**Consistency with docs**` since the worked example omits that field).

### Insertion point (b): After L49, before L50

3 lines before (L47-49) + 3 lines after (L50-52):

```

Per-dimension self-assessment:
- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
- Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
- Fix directness: <0.0|0.5|1.0> — <one-line reason>
```

**Unique-match candidate `old_string` for Edit tool:**

```
- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
```

This 2-line slice is unique in the file (these specific dimension names appear only at L49-50).

### Insertion point (c): After L61, before L63

3 lines before (L59-61) + 3 lines after (L62-64):

```
## If I'm wrong, it's probably because...

One sentence. The agent's best guess at the next-most-likely explanation if this hypothesis is wrong. This is what the Tier 2 fan-out uses to choose complementary agents.

## Alternatives considered

Bullet list of 0–3 other hypotheses the agent considered and rejected. For each, one line on why it was rejected. Empty list is fine if there were no plausible alternatives.
```

**Unique-match candidate `old_string` for Edit tool:**

```
One sentence. The agent's best guess at the next-most-likely explanation if this hypothesis is wrong. This is what the Tier 2 fan-out uses to choose complementary agents.

## Alternatives considered
```

This 3-line slice is unique in the file (the prose sentence only appears at L61).

---

## Summary

- **File is 108 lines** (not 109 as prompt assumed); lives in `src/superclaude/` source of truth; edits require `make sync-dev` before commit.
- **Two fenced code blocks**: L9-70 (template — all Change B insertions go here) and L81-108 (worked example — leave untouched; already v1-style per Migration note).
- **All three anchor regions captured verbatim with unique-match 2-3 line `old_string` slices** ready for Edit tool calls:
  - (a) After `**Cause class**:...` / before `**Consistency with docs**:...` at L15-16 boundary — inserts Claim class / Evidence class / Verdict direction / Runtime check frontmatter keys.
  - (b) After `- Evidence grounding:...` / before `- Symptom coverage:...` at L49-50 boundary — inserts Runtime check dimension row.
  - (c) After "If I'm wrong" body / before `## Alternatives considered` at L61-63 boundary — inserts `## Falsification standard` and `## Evidence classification` sections.
- **Apostrophes are straight ASCII**, em-dashes are U+2014, bullets are `- ` (hyphen+space). Builder must preserve these exact characters in new content to avoid markdownlint diff.
